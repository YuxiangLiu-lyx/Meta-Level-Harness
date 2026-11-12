"""Official Codex CLI backend; no API transport or credential handling."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time


def digest(value):
    data = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=True).encode()
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


def parse_events(raw):
    events, malformed = [], []
    for line in raw.splitlines():
        try:
            events.append(json.loads(line))
        except (ValueError, TypeError):
            malformed.append(line)
    return events, malformed


def summarize(events, returncode, timed_out=False):
    allowed = {"agent_message", "reasoning", "error"}
    tools = [e for e in events if e.get("item", {}).get("type") not in allowed
             and e.get("type", "").startswith("item.")]
    completed = [e for e in events if e.get("type") == "turn.completed"]
    failed = [e for e in events if e.get("type") in {"error", "turn.failed"}]
    usage = completed[-1].get("usage", {}) if completed else {}
    status = "COMPLETED" if returncode == 0 and completed else "INFRA_FAILURE"
    if timed_out:
        status = "TIMEOUT"
    if tools:
        status = "PROTOCOL_VIOLATION"
    error_text = json.dumps(failed).lower()
    if any(s in error_text for s in ["usage limit", "rate limit", "quota", "usage_limit", "insufficient_quota"]):
        status = "USAGE_LIMIT"
    return {"status": status, "returncode": returncode, "turns_started": sum(e.get("type") == "turn.started" for e in events),
            "turns_completed": len(completed), "tool_events": len(tools), "errors": failed,
            "input_tokens": usage.get("input_tokens"), "cached_input_tokens": usage.get("cached_input_tokens"),
            "output_tokens": usage.get("output_tokens"), "reasoning_output_tokens": usage.get("reasoning_output_tokens"),
            "runtime_warnings": [e for e in events if e.get("item", {}).get("type") == "error"],
            "effective_model": None, "underlying_requests": None, "truncated": None}


def retryable_infrastructure(result):
    """Retry only missing-response timeouts or recognized transport errors."""
    if result.get("final_response") or result.get("tool_events", 0):
        return False
    if result["status"] == "TIMEOUT":
        return True
    if result["status"] != "INFRA_FAILURE":
        return False
    text = json.dumps(result.get("errors", [])).lower()
    if any(word in text for word in ["auth", "401", "403", "quota", "usage limit", "rate limit"]):
        return False
    return any(word in text for word in ["connection", "network", "stream disconnected", "websocket", "timed out", "transport"])


class CodexBackend:
    def __init__(self, config, ledger):
        self.config = config
        self.ledger = Path(ledger)
        self.ledger.parent.mkdir(parents=True, exist_ok=True)

    def options(self):
        c = self.config
        args = []
        for override in c["overrides"]:
            args += ["-c", override]
        for feature in c["disabled_features"]:
            args += ["--disable", feature]
        for feature in c["enabled_features"]:
            args += ["--enable", feature]
        return args

    def environment(self):
        # Reuse the user's login store without reading or copying credentials.
        keys = {"HOME", "PATH", "TMPDIR", "LANG", "LC_ALL", "USER", "LOGNAME", "CODEX_HOME"}
        return {k: v for k, v in os.environ.items() if k in keys}

    def run_with_infra_retry(self, task_id, prompt, output_dir, output_schema=None):
        attempts = []
        result = self.run(task_id, prompt, output_dir, output_schema)
        attempts.append(result)
        if self.config.get("infrastructure_retry_limit", 0) == 1 and retryable_infrastructure(result):
            result = self.run(task_id + "-retry-1", prompt, str(output_dir) + "-retry-1", output_schema)
            attempts.append(result)
        return {**result, "attempts": [{k: r.get(k) for k in ["task_id", "status", "input_tokens", "output_tokens", "elapsed_seconds", "raw_directory"]} for r in attempts]}

    def run(self, task_id, prompt, output_dir, output_schema=None, diagnostic_files=None):
        out = Path(output_dir)
        identity = {"task_id": task_id, "prompt": prompt, "runtime": self.config, "output_schema": output_schema}
        key = digest(identity)
        if (out / "result.json").exists():
            result = json.loads((out / "result.json").read_text())
            if result["cache_key"] != key:
                raise RuntimeError("Cache identity mismatch; use a new experiment directory")
            return result
        if out.exists():
            raise RuntimeError("Incomplete attempt exists; preserve it and diagnose explicitly")
        attempts = [json.loads(x) for x in self.ledger.read_text().splitlines()] if self.ledger.exists() else []
        if len(attempts) >= self.config["max_logical_tasks"]:
            raise RuntimeError("Logical model task budget exhausted")
        if any(x["task_id"] == task_id for x in attempts):
            raise RuntimeError("Task already attempted; do not silently retry")
        out.mkdir(parents=True)
        write_json(out / "input.json", identity)
        raw = Path(self.config["raw_root"]) / "codex" / task_id
        raw.mkdir(parents=True, exist_ok=False)
        started = time.time()
        with self.ledger.open("a") as f:
            f.write(json.dumps({"task_id": task_id, "cache_key": key, "started_unix": started, "raw_directory": str(raw)}) + "\n")
        with tempfile.TemporaryDirectory(prefix="harness-task-") as work:
            for name, content in (diagnostic_files or {}).items():
                (Path(work) / name).write_text(content)
            command = [self.config["binary"], "--no-daemon", "exec", "--ignore-user-config", "--ignore-rules",
                       "--skip-git-repo-check", "--ephemeral", "--json", "--color", "never", "--sandbox", "read-only",
                       "--model", self.config["requested_model"], "--cd", work, *self.options(),
                       "--output-last-message", str(raw / "final.txt")]
            if output_schema is not None:
                write_json(raw / "schema.json", output_schema)
                command += ["--output-schema", str(raw / "schema.json")]
            command += ["-"]
            write_json(out / "command.json", command)
            timed_out = False
            with (raw / "events.jsonl").open("wb") as stdout, (raw / "stderr.txt").open("wb") as stderr:
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                           cwd=work, env=self.environment(), start_new_session=True)
                try:
                    process.communicate(prompt.encode(), timeout=self.config["task_timeout_seconds"])
                except subprocess.TimeoutExpired:
                    timed_out = True
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
        events, malformed = parse_events((raw / "events.jsonl").read_text())
        result = summarize(events, process.returncode, timed_out)
        final_path = raw / "final.txt"
        final = final_path.read_text() if final_path.exists() else None
        result.update({"task_id": task_id, "cache_key": key, "elapsed_seconds": time.time() - started,
                       "raw_directory": str(raw), "malformed_event_lines": len(malformed),
                       "final_response": final, "raw_sha256": {p.name: digest(p.read_bytes()) for p in raw.iterdir() if p.is_file()}})
        # All original responses remain outside the repository, including non-English text.
        if final and any('\u4e00' <= c <= '\u9fff' for c in final):
            result["final_response"] = None
            result["non_english_evidence"] = True
        write_json(out / "result.json", result)
        return result

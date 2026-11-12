"""Strict Cedar/SymCC adapter for the published RAISE verification plans.

Unknown, timeout, and process failures never become semantic successes, including
negated liveness queries. Original CLI output is retained outside the repository.
"""
from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import tempfile
import time

from .backend import digest, write_json


def execute(command, timeout):
    start = time.monotonic()
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        out, err = p.communicate(timeout=timeout)
        return {"returncode": p.returncode, "stdout": out, "stderr": err, "elapsed_seconds": time.monotonic()-start, "timeout": False}
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        out, err = p.communicate()
        return {"returncode": p.returncode, "stdout": out, "stderr": err, "elapsed_seconds": time.monotonic()-start, "timeout": True}


def semantic_outcome(run, inverse=False):
    if run["timeout"] or run["returncode"] != 0:
        return "UNRESOLVED"
    output = run["stdout"]
    verified = bool(re.search(r": VERIFIED\s*$", output, re.M))
    disproved = bool(re.search(r": DOES NOT HOLD\s*$", output, re.M)) and "Counterexample found:" in output
    if verified == disproved:
        return "UNRESOLVED"
    return "PASS" if (disproved if inverse else verified) else "FAIL"


def load_plan(folder):
    spec = importlib.util.spec_from_file_location("verification_plan", folder / "verification_plan.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_checks()


class Verifier:
    def __init__(self, config, manifest, raw_root):
        self.config = config
        self.records = {r["id"]: r for r in manifest["records"]}
        self.raw_root = Path(raw_root)
        self.version = digest({"code": Path(__file__).read_text(), "config": config,
                               "binaries": {k: digest(Path(config[k]).read_bytes()) for k in ["cedar", "cvc5"]}})

    def score(self, scenario_id, policy, output_dir):
        out = Path(output_dir)
        row = self.records[scenario_id]
        folder = Path(row["scenario_directory"])
        key = digest({"scenario": scenario_id, "policy": policy, "verifier": self.version, "materials": row["files"]})
        if (out / "score.json").exists():
            saved = json.loads((out / "score.json").read_text())
            if saved["cache_key"] != key:
                raise RuntimeError("Scoring cache mismatch; preserve evidence and choose a new version")
            return saved
        out.mkdir(parents=True, exist_ok=True)
        for name, sha in row["files"].items():
            if digest((folder / name).read_bytes()) != sha:
                raise RuntimeError("Evaluation material changed after data freeze")
        raw = self.raw_root / "verifier" / key
        raw.mkdir(parents=True, exist_ok=True)
        result = {"scenario_id": scenario_id, "cache_key": key, "verifier_version": self.version,
                  "status": "OUTPUT_INVALID", "syntax_valid": None, "schema_valid": None,
                  "checks": [], "semantic_check_count": 0, "raw_directory": str(raw)}
        if not isinstance(policy, str) or not policy.strip():
            write_json(out / "score.json", result)
            return result
        with tempfile.TemporaryDirectory(prefix="cedar-score-") as tmp:
            candidate = Path(tmp) / "candidate.cedar"
            candidate.write_text(policy)
            schema = folder / "schema.cedarschema"
            command = [self.config["cedar"], "validate", "--schema", str(schema), "--policies", str(candidate)]
            gate = execute(command, 10)
            write_json(raw / "validate.json", {"command": command, **gate})
            if gate["timeout"] or gate["returncode"] not in [0, 1, 3]:
                result["status"] = "EVALUATION_UNRESOLVED"
            elif gate["returncode"] == 1:
                result.update(status="SYNTAX_FAIL", syntax_valid=False, schema_valid=False)
            elif gate["returncode"] == 3:
                result.update(status="SCHEMA_FAIL", syntax_valid=True, schema_valid=False)
            else:
                result.update(syntax_valid=True, schema_valid=True)
                checks = load_plan(folder)
                result["semantic_check_count"] = len(checks)
                for i, check in enumerate(checks):
                    kind = check["type"]
                    inverse = kind in {"liveness-overlap", "liveness", "always-denies-liveness"}
                    command = [self.config["cedar"], "symcc", "--cvc5-path", self.config["cvc5"],
                               "--principal-type", check["principal_type"], "--action", check["action"],
                               "--resource-type", check["resource_type"], "--schema", str(schema), "--counterexample"]
                    if kind == "implies":
                        command += ["implies", "--policies1", str(candidate), "--policies2", check["reference_path"]]
                    elif kind == "floor":
                        command += ["implies", "--policies1", check["floor_path"], "--policies2", str(candidate)]
                    elif kind in {"liveness-overlap", "liveness"}:
                        command += ["disjoint", "--policies1", str(candidate), "--policies2", check["reference_path"]]
                    elif kind in {"never-errors", "always-denies", "always-denies-liveness"}:
                        command += ["always-denies" if kind == "always-denies-liveness" else kind, "--policies", str(candidate)]
                    else:
                        result["checks"].append({"name": check["name"], "type": kind, "status": "UNRESOLVED"})
                        continue
                    run = execute(command, self.config["timeout_seconds"])
                    write_json(raw / f"check-{i:02}.json", {"command": command, **run})
                    result["checks"].append({"name": check["name"], "type": kind, "status": semantic_outcome(run, inverse),
                                             "elapsed_seconds": run["elapsed_seconds"], "raw_sha256": digest((raw / f"check-{i:02}.json").read_bytes())})
                states = [r["status"] for r in result["checks"]]
                if not states or "UNRESOLVED" in states:
                    result["status"] = "EVALUATION_UNRESOLVED"
                else:
                    result["status"] = "PASS" if all(x == "PASS" for x in states) else "SEMANTIC_FAIL"
        result["confirmed_overgrant"] = any(c["status"] == "FAIL" and c["type"] == "implies" for c in result["checks"])
        result["confirmed_overdeny"] = any(c["status"] == "FAIL" and c["type"] in {"floor", "liveness-overlap", "liveness", "always-denies-liveness"} for c in result["checks"])
        write_json(out / "score.json", result)
        return result

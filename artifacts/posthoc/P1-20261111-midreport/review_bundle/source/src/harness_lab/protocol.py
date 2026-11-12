"""Static harness validation, deterministic parsing, and execution freezes."""
import json
from pathlib import Path
import re
from .backend import digest, write_json

POLICY_SCHEMA = {"type": "object", "properties": {"policy": {"type": "string"}}, "required": ["policy"], "additionalProperties": False}
HARNESS_SCHEMA = {"type": "object", "properties": {
    "instruction_blocks": {"type": "array", "items": {"type": "string"}},
    "input_order": {"type": "array", "items": {"type": "string", "enum": ["requirements", "schema"]}},
    "checklist": {"type": "array", "items": {"type": "string"}}},
    "required": ["instruction_blocks", "input_order", "checklist"], "additionalProperties": False}


def parse_json(text):
    if not isinstance(text, str):
        raise ValueError("Missing final text")
    text = text.strip()
    match = re.fullmatch(r"```(?:json)?\s*\n(.*?)\n```", text, re.S)
    return json.loads(match.group(1) if match else text)


def validate_harness(harness):
    if not isinstance(harness, dict) or set(harness) != {"instruction_blocks", "input_order", "checklist"}:
        raise ValueError("Invalid harness fields")
    if sorted(harness["input_order"]) != ["requirements", "schema"]:
        raise ValueError("Inputs must appear exactly once")
    for field in ["instruction_blocks", "checklist"]:
        if not isinstance(harness[field], list) or not all(isinstance(x, str) for x in harness[field]):
            raise ValueError("Instruction blocks and checklist must contain static strings")
    words = " ".join(harness["instruction_blocks"] + harness["checklist"]).split()
    if not 1 <= len(words) <= 500:
        raise ValueError("Harness word budget exceeded or empty")
    if any('\u4e00' <= c <= '\u9fff' for c in " ".join(words)):
        raise ValueError("Harness must be English")
    return len(words)


def generation_input(scenario, harness, public):
    validate_harness(harness)
    # Explicit allowlist prevents metadata, answers, or verification plans leaking.
    value = {"public_instructions": public, "harness": harness}
    for key in harness["input_order"]:
        value[key] = scenario[key]
    assert set(value) == {"public_instructions", "harness", "requirements", "schema"}
    return json.dumps(value, ensure_ascii=True, indent=2)


def create_freeze(path, files, metadata):
    path = Path(path)
    if path.exists():
        raise RuntimeError("Freeze exists; do not overwrite")
    file_hashes = {str(p): digest(Path(p).read_bytes()) for p in sorted(files)}
    write_json(path, {"files": file_hashes, "metadata": metadata, "freeze_sha256": digest(file_hashes)})


def check_freeze(path):
    frozen = json.loads(Path(path).read_text())
    for name, expected in frozen["files"].items():
        if digest(Path(name).read_bytes()) != expected:
            raise RuntimeError(f"Frozen file changed: {name}")
    return frozen


def paired_counts(meta, refine):
    if set(meta) != set(refine):
        raise ValueError("Paired samples must have identical scenario IDs")
    counts = dict(both_pass=0, meta_only=0, refine_only=0, both_fail=0)
    for key in meta:
        a, b = meta[key] == "PASS", refine[key] == "PASS"
        counts["both_pass" if a and b else "meta_only" if a else "refine_only" if b else "both_fail"] += 1
    counts["difference_percentage_points"] = 100 * (counts["meta_only"] - counts["refine_only"]) / len(meta) if meta else None
    return counts

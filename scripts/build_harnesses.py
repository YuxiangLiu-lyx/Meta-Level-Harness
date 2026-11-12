"""E3: exactly five predeclared design stages, with no candidate evaluation."""
import json
from pathlib import Path
from harness_lab.backend import CodexBackend, digest, write_json
from harness_lab.protocol import HARNESS_SCHEMA, check_freeze, parse_json, validate_harness

base = Path("artifacts/experiments/E3-20261110-construction")
check_freeze(base / "freeze.json")
packet = json.loads(Path("artifacts/design_packet.json").read_text())
runtime = json.loads(Path("configs/runtime.json").read_text())
backend = CodexBackend(runtime, "artifacts/task_ledger.jsonl")
guidance_schema = {"type":"object", "properties":{"guidance":{"type":"string"}}, "required":["guidance"], "additionalProperties":False}
common = {
    "study": "Construct one reusable task harness for translating natural-language requirements and a Cedar schema into Cedar policies under a fixed Codex runtime.",
    "constraints": [
        "Use English only. Do not use tools, files, search, extra model calls, or external feedback.",
        "Final harness JSON has only instruction_blocks (array of static strings), input_order (requirements and schema, each exactly once), and checklist (array of static strings).",
        "The complete requirements and schema will be inserted without edits. Do not include input placeholders or copies in the static instructions.",
        "Editable instruction_blocks plus checklist must total at most 500 whitespace-delimited words. They may describe mental checks but may not specify execution, retrieval, candidate evaluation, extra model calls, or repair loops.",
        "The common public instructions and final policy-output format are fixed and cannot be changed.",
        "Produce a general reusable harness, not solutions to individual development examples. No candidate execution or new feedback is available between design stages."
    ],
    "design_packet": packet,
}
records = []

def stage(name, instruction, schema, previous=None):
    check_freeze(base / "freeze.json")
    value = {**common, "stage_instruction": instruction}
    if previous is not None:
        value["allowed_previous_artifact"] = previous
    result = backend.run("E3-20261110-"+name, json.dumps(value, ensure_ascii=True, indent=2), base/"tasks"/name, schema)
    parsed = None
    status = "DESIGN_INVALID"
    if result["status"] == "COMPLETED":
        try:
            parsed = parse_json(result["final_response"])
            if schema is HARNESS_SCHEMA:
                validate_harness(parsed)
            elif set(parsed) != {"guidance"} or not isinstance(parsed["guidance"],str) or not 1 <= len(parsed["guidance"].split()) <= 500:
                raise ValueError("Invalid guidance or word budget")
            status = "VALID"
        except (ValueError, TypeError, KeyError):
            parsed = None
    records.append({"stage":name,"status":status,"generation":result,"parsed":parsed})
    print(json.dumps({"stage":name,"status":status,"elapsed_seconds":result["elapsed_seconds"]}),flush=True)
    if result["status"] in {"USAGE_LIMIT", "INFRA_FAILURE", "TIMEOUT"}:
        write_json(base/"interruption.json", records)
        raise SystemExit("Design stopped after infrastructure or usage failure")
    return parsed

first_instruction = "Generate a final reusable harness now using the common frozen design packet. Return only the required harness JSON."
direct = stage("direct",first_instruction,HARNESS_SCHEMA)
guidance = stage("meta-guidance","Produce guidance about how to design a good reusable harness for this task. Focus on design principles, tradeoffs, and failure prevention. Do not produce the final harness or any scenario solution. Return exactly the guidance string in the required JSON, at most 500 words.",guidance_schema)
meta = stage("meta-harness","Generate the final reusable harness using the common design packet and the explicitly supplied design guidance. Return only the required harness JSON.",HARNESS_SCHEMA,guidance) if guidance else None
draft = stage("refine-draft",first_instruction,HARNESS_SCHEMA)
refine = stage("refine-revision","Directly revise the supplied draft harness to improve its usefulness based on the same common design packet. Return the entire revised final harness JSON. No new evaluation or feedback is available.",HARNESS_SCHEMA,draft) if draft else None
target=Path("artifacts/harnesses");target.mkdir(exist_ok=True)
for method,harness in [("direct",direct),("meta",meta),("refine",refine)]:
    if harness is not None:
        path=target/(method+".json")
        if path.exists():
            assert json.loads(path.read_text())==harness
        else:write_json(path,harness)
write_json(base/"results.json",records)
write_json(base/"metrics.json",{"logical_design_stages":len(records),"planned_stages":5,"valid_stages":sum(r["status"]=="VALID" for r in records),"final_harnesses":sum(h is not None for h in [direct,meta,refine]),"packet_sha256":digest(packet),"word_counts":{m:validate_harness(h) if h else None for m,h in [("Direct",direct),("Meta",meta),("Refine",refine)]}})

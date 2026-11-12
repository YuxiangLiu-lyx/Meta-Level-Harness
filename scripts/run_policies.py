"""Execute a frozen serial batch; cached tasks retain their original identity."""
import argparse
from collections import Counter
import json
from pathlib import Path
from harness_lab.backend import CodexBackend, write_json
from harness_lab.protocol import POLICY_SCHEMA, check_freeze, generation_input, parse_json
from harness_lab.verifier import Verifier

parser = argparse.ArgumentParser()
parser.add_argument("--experiment", required=True)
parser.add_argument("--split", choices=["design20", "validation20"], required=True)
parser.add_argument("--limit", type=int, default=20)
parser.add_argument("--methods", nargs="+", default=["Manual"])
args = parser.parse_args()
base = Path("artifacts/experiments") / args.experiment
check_freeze(base / "freeze.json")
runtime = json.loads(Path("configs/runtime.json").read_text())
backend = CodexBackend(runtime, "artifacts/task_ledger.jsonl")
verifier = Verifier(json.loads(Path("configs/verifier.json").read_text()), json.loads(Path("data/manifest.json").read_text()), runtime["raw_root"])
scenarios = [json.loads(x) for x in (Path("data") / (args.split + ".jsonl")).read_text().splitlines()][:args.limit]
public = Path("configs/public_instructions.txt").read_text()
all_results = []
# Rotate the condition order by scenario to reduce position/time confounding.
for index, scenario in enumerate(scenarios):
    methods = args.methods[index % len(args.methods):] + args.methods[:index % len(args.methods)]
    for method in methods:
        check_freeze(base / "freeze.json")
        harness = json.loads((Path("configs/manual.json") if method == "Manual" else Path("artifacts/harnesses") / (method.lower()+".json")).read_text())
        task = f"{args.experiment}-{method.lower()}-{index:02}"
        prompt = generation_input(scenario, harness, public)
        result = backend.run_with_infra_retry(task, prompt, base / "tasks" / task, POLICY_SCHEMA)
        policy = None
        if result["status"] == "COMPLETED":
            try:
                value = parse_json(result["final_response"])
                if isinstance(value, dict) and set(value) == {"policy"}:
                    policy = value["policy"]
            except (ValueError, TypeError):
                pass
            score = verifier.score(scenario["id"], policy, base / "scores" / task)
        else:
            score = {"status": result["status"], "scenario_id": scenario["id"], "checks": [], "syntax_valid": None, "schema_valid": None}
        row = {"task_id": task, "scenario_id": scenario["id"], "method": method, "generation": result, "score": score}
        all_results.append(row)
        with (base / "progress.jsonl").open("a") as stream:
            stream.write(json.dumps({"task_id": task, "status": score["status"], "cached_or_new": "completed"})+"\n")
        print(json.dumps({"method": method, "scenario": index+1, "status": score["status"], "seconds": round(result["elapsed_seconds"],2)}), flush=True)
        if result["status"] in {"USAGE_LIMIT", "INFRA_FAILURE", "TIMEOUT"}:
            write_json(base / "interruption.json", {"task_id": task, "status": result["status"]})
            raise SystemExit("Model batch stopped after infrastructure/usage failure")
output = base / f"summary-{args.limit:02}.json"
if not output.exists():
    write_json(output, {"completed": len(all_results), "counts": dict(Counter(r["score"]["status"] for r in all_results)), "records": all_results})

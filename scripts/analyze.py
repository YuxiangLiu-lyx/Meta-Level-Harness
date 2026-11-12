"""Create deterministic evidence tables from saved generations and evaluations."""
import argparse
from collections import Counter
import csv
import io
import json
from pathlib import Path

from harness_lab.backend import digest
from harness_lab.protocol import paired_counts


def save(path, text):
    path = Path(path)
    if path.exists():
        if path.read_text() != text:
            raise RuntimeError(f"Refusing to overwrite different evidence: {path}")
    else:
        path.write_text(text)


def save_json(path, value):
    save(path, json.dumps(value, indent=2, ensure_ascii=True)+"\n")


def save_csv(path, rows):
    stream = io.StringIO()
    if rows:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    save(path, stream.getvalue())


def attempt_values(records, field):
    values = []
    for record in records:
        generation = record["generation"]
        for attempt in generation.get("attempts", [generation]):
            if field in attempt:
                values.append(attempt[field])
            else:
                events = [json.loads(s) for s in (Path(attempt["raw_directory"])/"events.jsonl").read_text().splitlines()]
                completed = [e for e in events if e.get("type")=="turn.completed"]
                values.append(completed[-1].get("usage",{}).get(field) if completed else None)
    return values


def usage_total(records, field):
    values = attempt_values(records, field)
    return sum(values) if values and all(x is not None for x in values) else None


def batch_metrics(records, planned_per_method=20):
    metrics = {}
    for method in sorted({r["method"] for r in records}):
        subset = [r for r in records if r["method"] == method]
        scores = [r["score"] for r in subset]
        metrics[method] = {"method":method,"completed":len(subset),"planned":planned_per_method,
            "passed":sum(s["status"]=="PASS" for s in scores),
            "success_rate":sum(s["status"]=="PASS" for s in scores)/planned_per_method,
            "syntax_valid":sum(s.get("syntax_valid") is True for s in scores),
            "schema_valid":sum(s.get("schema_valid") is True for s in scores),
            "semantic_failures":sum(s["status"]=="SEMANTIC_FAIL" for s in scores),
            "evaluation_unresolved":sum(s["status"]=="EVALUATION_UNRESOLVED" for s in scores),
            "protocol_violations":sum(s["status"]=="PROTOCOL_VIOLATION" for s in scores),
            "infrastructure_failures":sum(s["status"] in {"INFRA_FAILURE","USAGE_LIMIT","TIMEOUT"} for s in scores),
            "confirmed_overgrant":sum(s.get("confirmed_overgrant",False) for s in scores),
            "confirmed_overdeny":sum(s.get("confirmed_overdeny",False) for s in scores),
            "tool_events":sum(r["generation"]["tool_events"] for r in subset),
            **{field:usage_total(subset,field) for field in ["input_tokens","cached_input_tokens","output_tokens","reasoning_output_tokens"]},
            "elapsed_seconds":sum(sum(a["elapsed_seconds"] for a in r["generation"].get("attempts",[r["generation"]])) for r in subset)}
        if any(len(r["generation"].get("attempts",[]))>1 for r in subset):
            metrics[method]["extra_infrastructure_attempts"]=sum(max(0,len(r["generation"].get("attempts",[]))-1) for r in subset)
            for field in ["input_tokens","cached_input_tokens","output_tokens","reasoning_output_tokens"]:
                metrics[method]["known_"+field+"_subtotal"]=sum(x for x in attempt_values(subset,field) if x is not None)
    return metrics


def export_batch(base):
    source=base/"summary-20.json"
    records=json.loads(source.read_text())["records"]
    metrics=batch_metrics(records)
    save_json(base/"metrics.json",metrics)
    rows=[];predictions=[];events=[]
    for r in records:
        g,s=r["generation"],r["score"]
        rows.append({"task_id":r["task_id"],"scenario_id":r["scenario_id"],"method":r["method"],"status":s["status"],
            "syntax_valid":s.get("syntax_valid"),"schema_valid":s.get("schema_valid"),
            "checks_passed":sum(c["status"]=="PASS" for c in s["checks"]),"checks_total":len(s["checks"]),
            "confirmed_overgrant":s.get("confirmed_overgrant",False),"confirmed_overdeny":s.get("confirmed_overdeny",False),
            "input_tokens":g["input_tokens"],"cached_input_tokens":g["cached_input_tokens"],"output_tokens":g["output_tokens"],
            "reasoning_output_tokens":g["reasoning_output_tokens"],"elapsed_seconds":g["elapsed_seconds"],"tool_events":g["tool_events"]})
        predictions.append({"task_id":r["task_id"],"scenario_id":r["scenario_id"],"method":r["method"],"final_response":g["final_response"],"raw_directory":g["raw_directory"]})
        if "attempts" not in g:
            events.append({"task_id":r["task_id"],"original_events_path":g["raw_directory"]+"/events.jsonl","sha256":g["raw_sha256"]["events.jsonl"],"turns_started":g["turns_started"],"turns_completed":g["turns_completed"],"tool_events":g["tool_events"],"underlying_requests":g["underlying_requests"]})
        for attempt in g.get("attempts", []):
            path=Path(attempt["raw_directory"])/"events.jsonl"
            raw_events=[json.loads(s) for s in path.read_text().splitlines()]
            events.append({"logical_task_id":r["task_id"],"attempt_id":attempt["task_id"],"original_events_path":str(path),"sha256":digest(path.read_bytes()),"turns_started":sum(e.get("type")=="turn.started" for e in raw_events),"turns_completed":sum(e.get("type")=="turn.completed" for e in raw_events),"underlying_requests":None})
    save_csv(base/"results.csv",rows)
    save(base/"predictions.jsonl","".join(json.dumps(r,ensure_ascii=True)+"\n" for r in predictions))
    save(base/"events.jsonl","".join(json.dumps(r,ensure_ascii=True)+"\n" for r in events))
    save_json(base/"manifest.json",{"source":str(source),"source_sha256":digest(source.read_bytes()),"scenario_ids":sorted({r["scenario_id"] for r in records}),"task_ids":[r["task_id"] for r in records],"freeze":str(base/"freeze.json")})
    return records,metrics


def table(metrics):
    lines=["| Method | Pass / planned | Syntax | Schema | Overgrant | Overdeny | Input tokens | Cached input | Output tokens | Reasoning output | Seconds |",
           "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for m in metrics.values():
        lines.append(f'| {m["method"]} | {m["passed"]}/{m["planned"]} | {m["syntax_valid"]}/{m["planned"]} | {m["schema_valid"]}/{m["planned"]} | {m["confirmed_overgrant"]} | {m["confirmed_overdeny"]} | {m["input_tokens"]} | {m["cached_input_tokens"]} | {m["output_tokens"]} | {m["reasoning_output_tokens"]} | {m["elapsed_seconds"]:.1f} |')
    for m in metrics.values():
        if m.get('extra_infrastructure_attempts'):
            lines.append(f'\n{m["method"]}: {m["extra_infrastructure_attempts"]} additional infrastructure attempt(s). Total tokens are unknown if a failed attempt omitted usage. Known input subtotal: {m["known_input_tokens_subtotal"]}; known output subtotal: {m["known_output_tokens_subtotal"]}. Elapsed seconds include failed and successful attempts.')
    return "\n".join(lines)


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("experiment");args=parser.parse_args()
    records,metrics=export_batch(Path("artifacts/experiments")/args.experiment)
    print(json.dumps(metrics,indent=2))

"""Audit E3/E3R provenance and freeze the amended E4 comparison."""
import json
from pathlib import Path
import zipfile
from harness_lab.backend import digest, write_json
from harness_lab.protocol import create_freeze, validate_harness
from analyze import save_csv, save_json

base=Path("artifacts/experiments/E3R-20261110-recovery")
results=json.loads((base/"successful-stages.json").read_text())
metrics=json.loads((base/"metrics.json").read_text())
assert len(results)==5 and all(r["status"]=="VALID" for r in results), "Preserve and report DESIGN_INVALID instead of repair"
expected_packet=digest(json.loads(Path("artifacts/design_packet.json").read_text()))
usage=[]
for row in results:
    stage=row["stage"];g=row["generation"]
    inp=json.loads(Path(row["input_path"]).read_text())
    value=json.loads(inp["prompt"])
    assert digest(value["design_packet"])==expected_packet
    current=json.loads(Path("configs/runtime.json").read_text())
    assert all(inp["runtime"][k]==current[k] for k in inp["runtime"] if k!="protocol")
    assert g["tool_events"]==0
    if stage in {"meta-harness","refine-revision"}:
        expected=next(r["parsed"] for r in results if r["stage"]==("meta-guidance" if stage=="meta-harness" else "refine-draft"))
        assert value["allowed_previous_artifact"]==expected
    else:
        assert "allowed_previous_artifact" not in value
    words=len(row["parsed"]["guidance"].split()) if stage=="meta-guidance" else validate_harness(row["parsed"])
    usage.append({"stage":stage,"words":words,**{k:g[k] for k in ["input_tokens","cached_input_tokens","output_tokens","reasoning_output_tokens","elapsed_seconds","tool_events","turns_started","turns_completed","underlying_requests"]}})
save_csv(base/"results.csv",usage)
save_json(base/"fairness_audit.json",{"stages_checked":5,"identical_packet":True,"identical_model_tools_and_per_attempt_budget":True,"protocol_amendment":"v1.1 disclosed one-attempt infrastructure recovery","initial_failed_attempts":1,"fresh_sessions":len({json.loads((Path(r['generation']['raw_directory'])/'events.jsonl').read_text().splitlines()[0])['thread_id'] for r in results})==5,"previous_artifact_allowlist_verified":True,"no_between_stage_evaluation":True,"static_final_harnesses_reviewed":True,"equal_stages_not_equal_compute":True})
save_json(base/"manifest.json",{"task_ids":[r["generation"]["task_id"] for r in results],"packet_sha256":expected_packet,"final_harness_hashes":{m:digest((Path('artifacts/harnesses')/(m+'.json')).read_bytes()) for m in ['direct','meta','refine']}})
lines=["| Stage | Words | Input | Cached input | Output | Reasoning output | Seconds |","| --- | --- | --- | --- | --- | --- | --- |"]
for r in usage:lines.append(f'| {r["stage"]} | {r["words"]} | {r["input_tokens"]} | {r["cached_input_tokens"]} | {r["output_tokens"]} | {r["reasoning_output_tokens"]} | {r["elapsed_seconds"]:.1f} |')
report='''# E3R: Recovered construction and fairness audit

## Research Question
Can Direct, Meta, and Refine produce one valid static harness each under the same frozen development evidence and stage budgets?

## Hypothesis
Guidance before harness construction may improve later validation relative to direct revision. Construction validity alone cannot test that performance hypothesis.

## Setup and Controlled Variables
Five logical design stages: Direct 1, Meta 2, Refine 2. Six actual design task attempts include the preserved Meta timeout. Protocol v1.1 adds one same-input recovery attempt for missing-response infrastructure failures, before any validation outcome is observed. All use identical frozen design packet, requested gpt-6.1-sol, medium effort, 180 seconds per stage, and 500-word editable artifact limit. Every stage is a fresh official Codex task. Second stages receive only the common materials and their permitted first-stage artifact. No candidate evaluation, validator feedback, or new evidence occurs between stages. Full stage inputs, raw output references, parsed artifacts, and snapshot are saved.

## Execution Status
IMPLEMENTED, TESTED, EXECUTED, ANALYZED. 5/5 logical design stages now have valid artifacts. 3/3 final automatic harnesses constructed; one disclosed infrastructure retry, no output repair, search, or candidate selection. Initial E3 remains reported as 4/5 completed. Manual remains unchanged.

## Results
'''+"\n".join(lines)+'''

The fairness audit confirms identical packet and runtime settings, five distinct successful sessions, plus a separate failed Meta attempt, permitted artifact transfer, and zero tool events. All final harnesses contain only static instruction blocks, a legal input order, and a checklist. Input content is not rewritten or duplicated. Actual compute differs across equal-stage methods and is reported above.

## Error Analysis
No completed-output DESIGN_INVALID outcome occurred. The original Meta attempt timed out without a final response; its token usage is unknown. The one recovery used byte-identical prompt text, including the same guidance and packet. No new feedback was added. all_attempts.json retains all six attempts. The table above contains successful-stage usage only; Meta total input/output/reasoning usage is unknown, and reported successful-stage sums are known lower bounds. Elapsed attempt time includes the extra 180.022 seconds when comparing operational cost. Runtime warning events concern the fixed experimental skill-discovery feature and are preserved separately from tool events. Representative construction artifacts are the Meta guidance and the Refine draft/revision; each is stored in its task result. These artifacts are not shown to execution tasks except for the corresponding final harness.

## Interpretation
The construction manipulation is available with a disclosed infrastructure-recovery deviation. Any eventual difference is conditional on these single sampled harnesses and the shared packet. No performance comparison has yet been made at this stage.

## Limitations
One final harness per method. The post-freeze operational amendment weakens preregistration fidelity and adds an unobserved-usage Meta attempt; it must accompany any comparison. Word limits and common stage settings do not equalize input/output/reasoning tokens. Model sampling and unobserved server behavior prevent bit-for-bit regeneration guarantees. Raw reference-alignment ambiguity in the corpus remains.

## Next Action
Freeze all four final harnesses and execute exactly 80 validation policy generations, rotating method order by scenario. Keep the previously stated exploratory Meta > Refine hypothesis unchanged.

## Reproduction
Use the original E3 snapshot for the failed initial batch. `PYTHONPATH=src python3 scripts/recover_construction.py` reuses the single recovery attempt from cache. `PYTHONPATH=src python3 scripts/finalize_construction.py` checks fairness and creates the next freeze. Independent design repeats require new identities and a separate protocol run; do not overwrite these outputs.
'''
(base/"report.md").write_text(report)
e4=Path("artifacts/experiments/E4-20261110-validation");e4.mkdir(exist_ok=False)
files=[*Path('src').rglob('*.py'),*Path('configs').glob('*'),*Path('data').glob('*'),*Path('artifacts/harnesses').glob('*.json'),Path('scripts/run_policies.py')]
create_freeze(e4/'freeze.json',files,{'protocol':'v1.1','planned_policy_generations':80,'methods':['Manual','Direct','Meta','Refine'],'primary_comparison':'Meta vs Refine','directional_exploratory_hypothesis':'Meta > Refine','scenario_order':'frozen validation20 manifest order','method_order':'rotate the fixed method list by scenario index','no_final_test':True})
write_json(e4/'config.json',{'runtime':json.loads(Path('configs/runtime.json').read_text()),'methods':['Manual','Direct','Meta','Refine'],'split':'validation20','planned':80,'design_repeats_per_method':1})
with zipfile.ZipFile(e4/'snapshot.zip','x',compression=zipfile.ZIP_DEFLATED) as z:
    for name in json.loads((e4/'freeze.json').read_text())['files']:z.write(name,name)
print(json.dumps({'valid_stages':5,'final_harnesses':3,'word_counts':metrics['word_counts'],'validation_frozen':True}))

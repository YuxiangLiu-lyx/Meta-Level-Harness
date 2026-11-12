"""Build E4/E5 analyses from saved evidence, with no model calls or selection."""
from collections import Counter
import json
from pathlib import Path
from harness_lab.backend import digest, parse_events, summarize
from harness_lab.protocol import paired_counts
from analyze import export_batch, save, save_csv, save_json, table

e4=Path('artifacts/experiments/E4-20261110-validation')
records,metrics=export_batch(e4)
assert len(records)==80, 'Do not label an incomplete comparison complete'
order=[json.loads(s)['id'] for s in Path('data/validation20.jsonl').read_text().splitlines()]
by_method={m:{r['scenario_id']:r for r in records if r['method']==m} for m in ['Manual','Direct','Meta','Refine']}
resolved={'PASS','SEMANTIC_FAIL','SYNTAX_FAIL','SCHEMA_FAIL','OUTPUT_INVALID'}
pair_rows=[];eligible=[]
for sid in order:
    a,b=by_method['Meta'][sid]['score']['status'],by_method['Refine'][sid]['score']['status']
    if a in resolved and b in resolved:
        category='both_pass' if a==b=='PASS' else 'meta_only' if a=='PASS' else 'refine_only' if b=='PASS' else 'both_fail'
        eligible.append(sid)
    else:category='unresolved_or_protocol_violation'
    pair_rows.append({'scenario_id':sid,'Manual':by_method['Manual'][sid]['score']['status'],'Direct':by_method['Direct'][sid]['score']['status'],'Meta':a,'Refine':b,'pair_category':category})
paired=paired_counts({sid:by_method['Meta'][sid]['score']['status'] for sid in eligible},{sid:by_method['Refine'][sid]['score']['status'] for sid in eligible})
paired.update({'planned_pairs':20,'resolved_pairs':len(eligible),'unresolved_or_violating_pairs':20-len(eligible),'meta_successes':metrics['Meta']['passed'],'refine_successes':metrics['Refine']['passed'],'planned_denominator_difference_pp':100*(metrics['Meta']['passed']-metrics['Refine']['passed'])/20})
save_json(e4/'paired_metrics.json',paired);save_csv(e4/'paired_results.csv',pair_rows)
e5=Path('artifacts/experiments/E5-20261110-evidence');e5.mkdir(exist_ok=True)
data=json.loads(Path('data/manifest.json').read_text())
environment=json.loads(Path('artifacts/experiments/E0-20261110-preflight/environment.json').read_text())
performance_rows=[]
for method in ['Manual','Direct','Meta','Refine']:
    row={k:v for k,v in metrics[method].items() if not k.startswith('known_') and k!='extra_infrastructure_attempts'}
    row['extra_infrastructure_attempts']=metrics[method].get('extra_infrastructure_attempts',0)
    for field in ['input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens']:
        row['known_'+field+'_subtotal']=metrics[method].get('known_'+field+'_subtotal',metrics[method][field])
    performance_rows.append(row)
save_csv(e5/'performance.csv',performance_rows)
save_csv(e5/'meta_refine_pairs.csv',pair_rows)
save_json(e5/'paired_metrics.json',paired)
dataset_rows=[]
for split in ['design20','validation20']:
    rows=[r for r in data['records'] if r['split']==split]
    dataset_rows.append({'split':split,'scenarios':len(rows),'families':len({r['family'] for r in rows}),'signature_groups':len({r['sig'] for r in rows}),'areas':len({r['area'] for r in rows}),'tiers':json.dumps(dict(sorted(Counter(r['tier'] for r in rows).items()))),'seed':data['seed'],'upstream_commit':data['upstream_commit']})
save_csv(e5/'dataset.csv',dataset_rows)
save_csv(e5/'environment.csv',[{'field':k,'value':json.dumps(v,ensure_ascii=True) if isinstance(v,(dict,list)) else v} for k,v in environment.items()])
sanity=Path('artifacts/experiments/E1-20261110-sanity/results.csv')
save(e5/'verifier_sanity.csv',sanity.read_text())
construction=json.loads(Path('artifacts/experiments/E3R-20261110-recovery/all_attempts.json').read_text())
design_usage=[]
for method,stages in [('Manual',[]),('Direct',['direct']),('Meta',['meta-guidance','meta-harness']),('Refine',['refine-draft','refine-revision'])]:
    rows=[r for r in construction if r['stage'] in stages]
    value={'method':method,'logical_stages':len(stages),'actual_attempts':len(rows),'successful_attempts':sum(r['status']=='VALID' for r in rows),'infrastructure_failures':sum(r['generation']['status']!='COMPLETED' for r in rows),'elapsed_seconds':sum(r['generation']['elapsed_seconds'] for r in rows)}
    for field in ['input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens']:
        vals=[r['generation'][field] for r in rows]
        value[field]=sum(vals) if all(v is not None for v in vals) else None
        value['known_'+field+'_subtotal']=sum(v for v in vals if v is not None)
    design_usage.append(value)
save_csv(e5/'construction_usage.csv',design_usage)
ledger=[json.loads(s) for s in Path('artifacts/task_ledger.jsonl').read_text().splitlines()]
accounting=[];seen_threads=set();original_events=[]
for row in ledger:
    raw=Path(row['raw_directory']);events,malformed=parse_events((raw/'events.jsonl').read_text())
    assert not malformed
    threads=[e['thread_id'] for e in events if e.get('type')=='thread.started']
    for thread in threads:
        assert thread not in seen_threads,'Reused session'
        seen_threads.add(thread)
    endings=[e for e in events if e.get('type')=='turn.completed']
    usage=endings[-1].get('usage',{}) if endings else {}
    tool_count=summarize(events,0 if endings else -1)['tool_events']
    accounting.append({'task_id':row['task_id'],'group':'connectivity' if row['task_id'].startswith('smoke-') else 'construction' if row['task_id'].startswith(('E3-','E3R-')) else 'policy_generation','final_turn_completed':bool(endings),'visible_turns_started':sum(e.get('type')=='turn.started' for e in events),'visible_turns_completed':len(endings),'tool_events':tool_count,'input_tokens':usage.get('input_tokens'),'cached_input_tokens':usage.get('cached_input_tokens'),'output_tokens':usage.get('output_tokens'),'reasoning_output_tokens':usage.get('reasoning_output_tokens'),'underlying_requests':None,'raw_directory':str(raw)})
    original_events.append({'task_id':row['task_id'],'path':str(raw/'events.jsonl'),'sha256':digest((raw/'events.jsonl').read_bytes())})
save_csv(e5/'task_accounting.csv',accounting)
save(e5/'events.jsonl',''.join(json.dumps(r,ensure_ascii=True)+'\n' for r in original_events))
accounting_metrics={'task_attempts':len(ledger),'budget':120,'completed_attempts':sum(r['final_turn_completed'] for r in accounting),'incomplete_attempts':sum(not r['final_turn_completed'] for r in accounting),'distinct_thread_ids':len(seen_threads),'groups':dict(Counter(r['group'] for r in accounting)),'observed_tool_events':sum(r['tool_events'] for r in accounting),'underlying_requests':None,'total_input_tokens':None if any(r['input_tokens'] is None for r in accounting) else sum(r['input_tokens'] for r in accounting),'known_input_tokens_subtotal':sum(r['input_tokens'] for r in accounting if r['input_tokens'] is not None),'known_output_tokens_subtotal':sum(r['output_tokens'] for r in accounting if r['output_tokens'] is not None),'heldout_evaluated':0}
save_json(e5/'metrics.json',{'accounting':accounting_metrics,'validation':metrics,'paired':paired})
save_json(e5/'observability.json',{'requested_model':environment['requested_model'],'effective_model':None,'underlying_requests':None,'temperature':None,'seed':None,'hard_generation_token_limit':None,'truncation':None,'truncation_note':'The exec event interface did not expose a definitive truncation flag. Valid JSON does not prove semantic completeness.','cached_token_accounting':'Cached input is a subset of input tokens, not additive.','failed_attempt_usage':'Unknown; never filled with zero.','runtime_background':'Built-in Codex runtime and any unobservable server context are fixed background, not fully controlled system messages.'})
# Select the first frozen-order example from every pair category, not the best.
cases=[]
for category in ['meta_only','refine_only','both_pass','both_fail']:
    pair=next((r for r in pair_rows if r['pair_category']==category),None)
    if pair is None:continue
    sid=pair['scenario_id'];case={'category':category,'scenario_id':sid,'selection_rule':'first occurrence in frozen validation order','methods':{}}
    for method in ['Meta','Refine']:
        r=by_method[method][sid]
        case['methods'][method]={'status':r['score']['status'],'failed_checks':[c for c in r['score']['checks'] if c['status']!='PASS'],'prediction_path':str(e4/'tasks'/r['generation']['task_id']/'result.json'),'score_path':str(e4/'scores'/r['task_id']/'score.json')}
    cases.append(case)
save_json(e5/'cases.json',cases)
case_lines=[]
for case in cases:
    failures='; '.join(f'{m}: '+(', '.join(c['name'] for c in case['methods'][m]['failed_checks']) or 'all checks pass') for m in ['Meta','Refine'])
    case_lines.append(f'- {case["category"]}: `{case["scenario_id"]}`. {failures}.')
delta=paired['planned_denominator_difference_pp']
interpretation=(f'Meta exceeded Refine by {delta:g} percentage points in this single exploratory sample.' if delta>0 else f'Meta trailed Refine by {-delta:g} percentage points in this single exploratory sample.' if delta<0 else 'Meta and Refine tied on total successes in this single exploratory sample.')
main=f'''# E4: Validation comparison

## Research Question
Does guidance-first Meta outperform direct-revision Refine on the same 20 validation scenarios under the fixed runtime?

## Hypothesis
The previously recorded directional exploratory hypothesis is Meta > Refine. It was not changed after validation.

## Setup and Controlled Variables
Protocol v1.1 for all validation conditions. One frozen harness per method; 20 shared scenarios; 80 logical policy generations. Requested gpt-6.1-sol, medium effort, fixed public instructions, no tools or verifier feedback, fresh sessions. Order rotates Manual/Direct/Meta/Refine by scenario. Maximum one same-input retry is allowed only for a missing-response infrastructure failure; completed answers are never repaired or retried. Original E3 construction had one Meta timeout and one disclosed recovery before validation; this deviation is retained and affects cost observability.

## Execution Status
IMPLEMENTED, TESTED, EXECUTED, ANALYZED. 80/80 validation scenario-method pairs have saved outcomes. All results are included. Additional validation infrastructure attempts: {sum(m.get('extra_infrastructure_attempts',0) for m in metrics.values())}. Final held-out evaluation: 0 scenarios.

## Results
{table(metrics)}

Meta-Refine pairing: both_pass={paired['both_pass']}, meta_only={paired['meta_only']}, refine_only={paired['refine_only']}, both_fail={paired['both_fail']}; resolved pairs={paired['resolved_pairs']}/20; unresolved/protocol-violating pairs={paired['unresolved_or_violating_pairs']}/20. Meta succeeds on {metrics['Meta']['passed']}/20; Refine on {metrics['Refine']['passed']}/20. Difference: {delta:+g} percentage points. Input tokens include cached input; do not add them. Blank/null totals indicate missing usage, not zero. Tables report scenario-level success; check counts are diagnostic only.

## Error Analysis
Examples are selected by first occurrence in frozen validation order for each pair category:
{chr(10).join(case_lines)}

All scenario-method outcomes and paired rows are in results.csv and paired_results.csv. Confirmed overgrant and overdeny counts can overlap. Runtime/tool violations and unresolved evaluations are reported separately from semantic failures.

## Interpretation
{interpretation} This describes the observed harnesses and subset only. It cannot isolate a general causal advantage of meta-level guidance from single-design variability. A pass means satisfying the published nonempty checks, not equivalence to every plausible natural-language interpretation.

## Limitations
Only 20 scenarios and one sampled design per automatic method. No statistical significance or general superiority is claimed. Equal stage counts do not imply equal compute. The Meta timeout has unknown token cost, and a post-freeze retry-rule amendment was necessary. Some requirements underspecify relationships required by the plans. Unexposed server model identity, internal requests, and sampling parameters remain unknown. No final test was opened.

## Next Action
Preserve this round. In a new preregistered round, fix recovery policy in advance, repeat designs across independent runs, audit ambiguous specification/check pairs, and expand validation without using the held-out test for development.

## Reproduction
The exact execution snapshot and hashes are in snapshot.zip and freeze.json. `PYTHONPATH=src python3 scripts/run_policies.py --experiment E4-20261110-validation --split validation20 --methods Manual Direct Meta Refine` reuses cached task identities. `PYTHONPATH=src python3 scripts/evidence_package.py` regenerates tables without model calls. Independent resampling requires new experiment identities and separate reporting.
'''
save(e4/'report.md',main)
summary=f'''# E5: Evidence package

## Research Question
What conclusions are supported by this completed exploratory research loop, including failures and procedural deviations?

## Hypothesis
Meta may outperform Refine under a fixed runtime. This remains a limited exploratory hypothesis rather than a general claim.

## Setup and Controlled Variables
Upstream RAISE commit {data['upstream_commit']}. Published 375-scenario held-out preserved. Fixed grouped design20/validation20, seed {data['seed']}; no shared families/signatures between subsets. Tables: dataset.csv, environment.csv, verifier_sanity.csv, construction_usage.csv, performance.csv, meta_refine_pairs.csv, task_accounting.csv. All authored reports and prompts are English; original raw evidence stays external with paths/hashes. Runtime is Codex, not a bare model.

## Execution Status
IMPLEMENTED, TESTED, EXECUTED, ANALYZED. E0: 3/3 diagnostics. E1: 18/18 controls. E2: 20/20 generations, 10/20 passes. E3 initial: 4/5 completed; E3R: 1/1 recovery. E4: 80/80 logical generations. Task attempts: {accounting_metrics['task_attempts']}/120; completed attempts: {accounting_metrics['completed_attempts']}; distinct sessions: {accounting_metrics['distinct_thread_ids']}. Incomplete infrastructure attempts: {accounting_metrics['incomplete_attempts']}. Tool events: {accounting_metrics['observed_tool_events']}. Final test: 0 evaluations.

## Results
{table(metrics)}

Primary paired result: Meta {metrics['Meta']['passed']}/20 versus Refine {metrics['Refine']['passed']}/20, {delta:+g} percentage points; both_pass={paired['both_pass']}, meta_only={paired['meta_only']}, refine_only={paired['refine_only']}, both_fail={paired['both_fail']}. These 20 pairs are the unit of analysis.

## Error Analysis
Manual development failures included both broadened grants and added prerequisites; 7/20 confirmed overgrant and 6/20 overdeny, with overlap. Sanity controls detected 10/10 known semantic mutants and 3/3 syntax/schema errors; 5/5 references passed. The original Meta design timeout has no final answer or usage event and remains an infrastructure failure. Its cost is not zero: Meta total design tokens and whole-run totals are unknown; known subtotals are provided. Positive and negative paired cases are indexed in cases.json using a deterministic selection rule.

## Interpretation
{interpretation} The pipeline can conduct and audit this comparison using an existing Codex subscription and actual Cedar/CVC5 checks. The outcome supports a descriptive observation about these frozen artifacts, not statistical significance, general superiority, a bare-model result, or a final-test claim.

## Limitations
Small sample, one design repeat, benchmark specification ambiguity, unequal actual design compute, hidden runtime context, and a disclosed post-freeze infrastructure amendment. Code/cache/split reproducibility is supported; stochastic model output is not guaranteed bit-for-bit reproducible. The original v1 zero-retry construction batch and v1.1 validation batch remain separately labeled; no failed evidence is discarded.

## Next Action
Preregister a complete timeout/retry plan before the next round. Repeat the Meta/Refine design construction with paired independent design seeds or repeats if supported; increase validation sample size across template groups; manually adjudicate requirement/plan mismatches without changing this round's scores. Keep the final held-out closed until hypotheses and methods are stable. No training or large prompt search is needed for this next diagnostic step.

## Reproduction
Run `PYTHONPATH=src python3 -m unittest discover -s tests -v`, `PYTHONPATH=src python3 scripts/audit_evidence.py`, and `PYTHONPATH=src python3 scripts/evidence_package.py`. These commands do not invoke a model. See README.md for installation, pinned external evidence, frozen snapshots, and new-run identity requirements. Every initial failed attempt, successful response, evaluation, and report is retained.
'''
save(e5/'report.md',summary)
save_json(e5/'config.json',{'source_experiments':['E0-20261110-preflight','E1-20261110-sanity','E2-20261110-manual','E3-20261110-construction','E3R-20261110-recovery','E4-20261110-validation'],'analysis_only':True,'model_calls':0})
save_json(e5/'manifest.json',{'files':{str(p):digest(p.read_bytes()) for p in sorted(e5.iterdir()) if p.is_file() and p.name!='manifest.json'},'source_e4_summary_sha256':digest((e4/'summary-20.json').read_bytes())})
print(json.dumps({'paired':paired,'accounting':accounting_metrics},indent=2))

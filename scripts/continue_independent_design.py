"""Complete the predeclared independent Refine stages after a Meta timeout.

This does not retry Meta, change any design material, or evaluate candidates.
"""
import json
from pathlib import Path
from harness_lab.backend import CodexBackend, write_json
from harness_lab.protocol import HARNESS_SCHEMA, check_freeze, parse_json, validate_harness

base=Path('artifacts/experiments/E3-20261110-construction')
check_freeze(base/'freeze.json')
runtime=json.loads(Path('configs/runtime.json').read_text())
backend=CodexBackend(runtime,'artifacts/task_ledger.jsonl')
direct_input=json.loads((base/'tasks/direct/input.json').read_text())
common=json.loads(direct_input['prompt'])
records=json.loads((base/'interruption.json').read_text())
for record in records:
    if record['generation']['status']!='COMPLETED':
        record['status']='DESIGN_INFRA_UNRESOLVED'
draft=None
for name in ['refine-draft','refine-revision']:
    value=dict(common)
    if name=='refine-revision':
        if draft is None:break
        value['stage_instruction']='Directly revise the supplied draft harness to improve its usefulness based on the same common design packet. Return the entire revised final harness JSON. No new evaluation or feedback is available.'
        value['allowed_previous_artifact']=draft
    check_freeze(base/'freeze.json')
    result=backend.run('E3-20261110-'+name,json.dumps(value,ensure_ascii=True,indent=2),base/'tasks'/name,HARNESS_SCHEMA)
    parsed=None
    status='DESIGN_INVALID' if result['status']=='COMPLETED' else 'DESIGN_INFRA_UNRESOLVED'
    if result['status']=='COMPLETED':
        try:
            parsed=parse_json(result['final_response']);validate_harness(parsed);status='VALID'
        except (ValueError,TypeError,KeyError):parsed=None
    records.append({'stage':name,'status':status,'generation':result,'parsed':parsed})
    print(json.dumps({'stage':name,'status':status,'seconds':result['elapsed_seconds']}),flush=True)
    draft=parsed
    if result['status'] in {'USAGE_LIMIT','INFRA_FAILURE','TIMEOUT'}:break
write_json(base/'results-initial-attempts.json',records)
write_json(base/'metrics-initial-attempts.json',{'planned_stages':5,'attempted_stages':len(records),'valid_stages':sum(r['status']=='VALID' for r in records),'infra_unresolved':sum(r['status']=='DESIGN_INFRA_UNRESOLVED' for r in records),'invalid_completed_outputs':sum(r['status']=='DESIGN_INVALID' for r in records)})

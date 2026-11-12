"""One disclosed same-input recovery attempt for the missing Meta artifact."""
import json
from pathlib import Path
import zipfile
from harness_lab.backend import CodexBackend, digest, write_json
from harness_lab.protocol import HARNESS_SCHEMA, create_freeze, check_freeze, parse_json, validate_harness

original=Path('artifacts/experiments/E3-20261110-construction')
base=Path('artifacts/experiments/E3R-20261110-recovery')
base.mkdir(exist_ok=True)
runtime=json.loads(Path('configs/runtime.json').read_text())
input_path=original/'tasks/meta-harness/input.json'
initial=json.loads(input_path.read_text())
initial_result=json.loads((input_path.parent/'result.json').read_text())
assert initial_result['status']=='TIMEOUT' and not initial_result['final_response']
if not (base/'freeze.json').exists():
    create_freeze(base/'freeze.json',[*Path('src').rglob('*.py'),*Path('configs').glob('*'),input_path,Path('artifacts/design_packet.json'),Path(__file__)],{'protocol':'v1.1','recovery_of':initial_result['task_id'],'maximum_recovery_attempts':1,'prompt_unchanged':True,'no_new_feedback':True})
    with zipfile.ZipFile(base/'snapshot.zip','x',compression=zipfile.ZIP_DEFLATED) as z:
        for name in json.loads((base/'freeze.json').read_text())['files']:z.write(name,name)
check_freeze(base/'freeze.json')
write_json(base/'config.json',{'runtime':runtime,'original_attempt':initial_result['task_id'],'input_sha256':digest(initial['prompt']),'original_timeout_seconds':180,'disclosed_amendment':'v1.1'})
backend=CodexBackend(runtime,'artifacts/task_ledger.jsonl')
# This is already the single recovery; deliberately do not call the retry helper.
result=backend.run('E3R-20261110-meta-harness-retry-1',initial['prompt'],base/'tasks/meta-harness',HARNESS_SCHEMA)
parsed=None;status='DESIGN_INFRA_UNRESOLVED'
if result['status']=='COMPLETED':
    status='DESIGN_INVALID'
    try:parsed=parse_json(result['final_response']);validate_harness(parsed);status='VALID'
    except (ValueError,TypeError,KeyError):parsed=None
row={'stage':'meta-harness','status':status,'generation':result,'parsed':parsed,'input_path':str(base/'tasks/meta-harness/input.json')}
write_json(base/'recovery_result.json',row)
print(json.dumps({'stage':'meta-harness-recovery','status':status,'seconds':result['elapsed_seconds']}),flush=True)
original_rows=json.loads((original/'results-initial-attempts.json').read_text())
for r in original_rows:r['input_path']=str(original/'tasks'/r['stage']/'input.json')
write_json(base/'all_attempts.json',original_rows+[row])
if status!='VALID':raise SystemExit('Recovery did not complete validly; no further retry allowed')
stages=[row if r['stage']=='meta-harness' else r for r in original_rows]
write_json(base/'successful-stages.json',stages)
target=Path('artifacts/harnesses');target.mkdir(exist_ok=True)
for method,stage in [('direct','direct'),('meta','meta-harness'),('refine','refine-revision')]:
    h=next(r['parsed'] for r in stages if r['stage']==stage)
    assert h is not None
    p=target/(method+'.json')
    if p.exists():assert json.loads(p.read_text())==h
    else:write_json(p,h)
write_json(base/'metrics.json',{'recovery_attempts':1,'recovery_pass':1,'logical_design_stages':5,'total_design_attempts':6,'valid_final_harnesses':3,'original_infrastructure_failures':1,'meta_total_input_tokens':None,'meta_total_output_tokens':None,'word_counts':{m:validate_harness(json.loads((target/(m.lower()+'.json')).read_text())) for m in ['Direct','Meta','Refine']}})

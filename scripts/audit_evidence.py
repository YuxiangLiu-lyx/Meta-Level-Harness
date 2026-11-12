"""Audit saved evidence without spending subscription usage or regenerating policies."""
import json
from pathlib import Path
import sys
from harness_lab.backend import digest, parse_events, summarize
from harness_lab.protocol import check_freeze, generation_input

root=Path('.')
manifest=json.loads((root/'data/manifest.json').read_text())
records=manifest['records']
design=[r for r in records if r['split']=='design20']
validation=[r for r in records if r['split']=='validation20']
assert len(design)==len(validation)==20
for key in ['id','family','sig']:
    assert {r[key] for r in design}.isdisjoint(r[key] for r in validation)
assert {r['id'] for r in records}.isdisjoint(manifest['heldout_ids'])
assert manifest['heldout_evaluated']==0
ledger=[json.loads(x) for x in Path('artifacts/task_ledger.jsonl').read_text().splitlines()]
assert len(ledger)<=120
assert len({r['task_id'] for r in ledger})==len(ledger)
issues=[];tool_events=0;completed=0;timeouts=0
for path in Path('artifacts/experiments').glob('*/tasks/*/result.json'):
    result=json.loads(path.read_text())
    identity=json.loads((path.parent/'input.json').read_text())
    assert digest(identity)==result['cache_key']
    for filename,expected in result['raw_sha256'].items():
        p=Path(result['raw_directory'])/filename
        if not p.exists():issues.append({'path':str(p),'status':'RAW_EVIDENCE_MISSING'})
        else:assert digest(p.read_bytes())==expected
    event_path=Path(result['raw_directory'])/'events.jsonl'
    if event_path.exists():
        events,malformed=parse_events(event_path.read_text())
        assert not malformed
        analyzed=summarize(events,result['returncode'],result['status']=='TIMEOUT')
        tool_events+=analyzed['tool_events']
        completed+=analyzed['status']=='COMPLETED'
        timeouts+=analyzed['status']=='TIMEOUT'
    if '-manual-' in result['task_id'] or '-validation-' in result['task_id']:
        value=json.loads(identity['prompt'])
        assert set(value)=={'public_instructions','harness','requirements','schema'}
        candidates=[json.loads(s) for f in [Path('data/design20.jsonl'),Path('data/validation20.jsonl')] for s in f.read_text().splitlines()]
        assert any(value['requirements']==r['requirements'] and value['schema']==r['schema'] for r in candidates)
print(json.dumps({'ledger_tasks':len(ledger),'budget':120,'design_count':20,'validation_count':20,'heldout_count':len(manifest['heldout_ids']),'heldout_evaluated':0,'completed_non_smoke_attempts':completed,'timeouts':timeouts,'tool_events':tool_events,'issues':issues},indent=2))
if issues:sys.exit(1)

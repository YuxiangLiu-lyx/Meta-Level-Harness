"""Validate a relocated package with host-user paths, network and subprocesses denied."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

CHILD = r'''
import os, runpy, sys
def guard(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        name = os.fsdecode(args[0])
        if name.startswith('/Users/'):
            raise PermissionError('Original host user paths are forbidden')
    if event.startswith(('socket.', 'subprocess.', 'os.system', 'os.posix_spawn')):
        raise PermissionError('Network and process execution are forbidden')
sys.addaudithook(guard)
sys.argv = [sys.argv[1], *sys.argv[2:]]
runpy.run_path(sys.argv[0], run_name='__main__')
'''


def validate(package):
    with tempfile.TemporaryDirectory(prefix='harness-portable-review-') as tmp:
        root = Path(tmp)
        relocated = root / 'package'
        shutil.copytree(package, relocated)

        def run(command, label):
            output = root / label
            p = subprocess.run([sys.executable, '-I', '-c', CHILD, str(relocated / 'review.py'),
                                command, str(relocated), '--output', str(output)],
                               cwd=root, capture_output=True, text=True, timeout=60)
            if not (output / 'results.json').exists():
                raise RuntimeError(p.stderr)
            return p.returncode, json.loads((output / 'results.json').read_text())

        code, metrics = run('analyze', 'metrics')
        assert code == 0 and metrics['paired_counts'] == dict(both_pass=8, meta_only=1, refine_only=3, both_fail=8)
        assert [r['pass'] for r in metrics['performance']] == [12, 10, 9, 11]
        assert metrics['accounting']['attempts'] == 110
        audit_code, audited = run('audit', 'audit')
        assert audit_code == 2 and audited['level2_status'] == 'INCOMPLETE'
        assert audited['historical_solver_hash_gaps'] == 61
        assert all(i['status'] == 'ORIGINAL_EVIDENCE_UNAVAILABLE' for i in audited['issues'])
        assert audited['observed_tool_events'] is None
        shutil.rmtree(relocated / 'raw')
        metrics_code, metrics_only = run('analyze', 'metrics-without-raw')
        missing_code, missing = run('audit', 'audit-without-raw')
        assert metrics_code == 0 and metrics_only == metrics
        assert missing_code == 2 and missing['level2_status'] == 'INCOMPLETE'
        assert missing['observed_tool_events'] is None and missing['tool_audit_status'] == 'UNKNOWN'
        return {'status': 'PASS', 'validation_type': 'relocated copy, isolated Python process, audit-hook denied host-user reads/network/subprocess',
                'original_host_paths_opened': 0, 'network_or_model_calls': 0,
                'saved_result_layer': 'COMPLETE', 'metrics_without_raw': 'IDENTICAL',
                'full_historical_evidence_layer': 'INCOMPLETE', 'known_historical_solver_hash_gaps': 61,
                'all_exported_files_verified': audited['manifest_files_verified'],
                'event_attempts_checked': audited['event_attempts_checked'],
                'available_solver_decisions_checked': audited['verifier_scores_checked'],
                'missing_raw_audit': 'INCOMPLETE', 'missing_raw_tool_events': None,
                'bootstrap_interval_pp': metrics['bootstrap']['interval_pp'],
                'temporary_directory': 'fresh directory, removed after validation'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; choose a new validation record')
    result = validate(args.package)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

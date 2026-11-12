"""Standalone, standard-library-only review of saved results and raw evidence.

This module never imports the experiment backend, opens host paths from logs,
executes a solver, connects to a network, or generates a policy.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path, PurePosixPath
import random
import re
import sys

METHODS = ('Manual', 'Direct', 'Meta', 'Refine')
RESOLVED = {'PASS', 'SYNTAX_FAIL', 'SCHEMA_FAIL', 'SEMANTIC_FAIL', 'OUTPUT_INVALID'}
TOKEN_FIELDS = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_output_tokens')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def object_sha(value):
    return sha(json.dumps(value, sort_keys=True, ensure_ascii=True).encode())


def safe_path(root, name):
    rel = PurePosixPath(name)
    if rel.is_absolute() or '..' in rel.parts or '\\' in name or not rel.parts:
        raise ValueError('Unsafe package path: ' + name)
    path = root.joinpath(*rel.parts)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path escapes package: ' + name)
    return path


def read(root, name):
    return json.loads(safe_path(root, name).read_text())


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n')


def write_csv(path, rows):
    if not rows:
        return
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def bootstrap(differences, seed=20261111, repetitions=100000):
    """Resample paired scenarios, preserving each within-scenario difference."""
    if not differences or repetitions < 1:
        raise ValueError('Nonempty pairs and positive repetitions required')
    rng = random.Random(seed)
    n = len(differences)
    sums = [sum(differences[rng.randrange(n)] for _ in range(n)) for _ in range(repetitions)]
    ordered = sorted(sums)

    def quantile(p):
        h = (repetitions - 1) * p
        lower = int(h)
        return (ordered[lower] + (h - lower) * (ordered[min(lower + 1, repetitions - 1)] - ordered[lower])) * 100 / n

    return {
        'analysis_type': 'POST_HOC', 'statistic': 'Meta minus Refine scenario success rate, percentage points',
        'sampling_unit': 'one scenario with both fixed-harness outcomes', 'n_pairs': n,
        'estimate_pp': 100 * sum(differences) / n, 'confidence_level': 0.95,
        'interval_type': 'paired nonparametric percentile bootstrap', 'interval_pp': [quantile(.025), quantile(.975)],
        'quantile_rule': 'linear interpolation at (B - 1) * p (type 7)',
        'seed': seed, 'repetitions': repetitions, 'rng': 'Python random.Random (MT19937), randrange(n)',
        'python_version': sys.version.split()[0], 'pair_differences': differences,
        'replicate_integer_sums_sha256': sha((''.join(str(x) + '\n' for x in sums)).encode()),
        'replicate_histogram': [{'sum': s, 'difference_pp': 100 * s / n, 'count': c} for s, c in sorted(Counter(sums).items())],
        'scope': 'Conditional on these two generated harnesses and saved policy outputs; construction and generation randomness are not resampled.',
        'caution': 'An interval containing zero is not evidence of equivalence. Twenty grouped scenarios are not eighty independent observations.',
    }


def load_validation(root, index):
    records = []
    seen = set()
    for row in index['validation']:
        key = (row['scenario_id'], row['method'])
        if key in seen:
            raise ValueError('Duplicate scenario-method pair')
        seen.add(key)
        score = read(root, row['score'])
        if score['scenario_id'] != row['scenario_id'] or row['method'] not in METHODS:
            raise ValueError('Invalid scenario/method mapping')
        records.append({**row, 'saved_score': score})
    order = [json.loads(line)['id'] for line in safe_path(root, index['validation_inputs']).read_text().splitlines()]
    if len(order) != 20 or len(set(order)) != 20 or seen != {(sid, method) for sid in order for method in METHODS}:
        raise ValueError('Expected exactly 20 scenarios by four methods')
    return records, order


def analyze(root, seed=20261111, repetitions=100000):
    index = read(root, 'index.json')
    records, order = load_validation(root, index)
    lookup = {(r['scenario_id'], r['method']): r['saved_score'] for r in records}
    performance = []
    for method in METHODS:
        scores = [r['saved_score'] for r in records if r['method'] == method]
        counts = Counter(s['status'] for s in scores)
        performance.append({
            'method': method, 'scenarios': len(scores), 'pass': counts['PASS'], 'success_rate': counts['PASS'] / len(scores),
            'syntax_failure': counts['SYNTAX_FAIL'], 'schema_type_failure': counts['SCHEMA_FAIL'],
            'semantic_failure': counts['SEMANTIC_FAIL'], 'output_invalid': counts['OUTPUT_INVALID'],
            'unresolved_or_protocol_failure': sum(v for k, v in counts.items() if k not in RESOLVED),
            'confirmed_overgrant': sum(s.get('confirmed_overgrant', False) for s in scores),
            'confirmed_overdeny': sum(s.get('confirmed_overdeny', False) for s in scores),
        })
    pairs = []
    for sid in order:
        a, b = lookup[sid, 'Meta']['status'], lookup[sid, 'Refine']['status']
        category = ('UNRESOLVED' if a not in RESOLVED or b not in RESOLVED else
                    'both_pass' if a == b == 'PASS' else 'meta_only' if a == 'PASS' else
                    'refine_only' if b == 'PASS' else 'both_fail')
        pairs.append({'scenario_id': sid, 'Meta': a, 'Refine': b, 'category': category,
                      'difference': None if category == 'UNRESOLVED' else int(a == 'PASS') - int(b == 'PASS')})
    if any(p['difference'] is None for p in pairs):
        raise ValueError('Unresolved outcomes: do not silently drop pairs for bootstrap')
    attempts = []
    for entry in index['attempts']:
        result = read(root, entry['result'])
        tid = entry['task_id']
        if tid != result['task_id']:
            raise ValueError('Task identity mismatch')
        attempts.append({'task_id': tid, 'group': entry['group'],
                         'recorded_status': result['status'], 'completed_turn': result['turns_completed'] > 0,
                         'timeout': result['status'] == 'TIMEOUT', 'has_final_response': bool(result.get('final_response')),
                         'elapsed_seconds': result['elapsed_seconds'],
                         **{k: result.get(k) for k in TOKEN_FIELDS}})
    if len(attempts) != len({r['task_id'] for r in attempts}):
        raise ValueError('Duplicate attempt identity')
    accounting = {'attempts': len(attempts), 'budget': 120,
                  'completed_turn_attempts': sum(r['completed_turn'] for r in attempts),
                  'timeouts': sum(r['timeout'] for r in attempts),
                  'groups': dict(Counter(r['group'] for r in attempts)),
                  'source_level': 'saved task records, not an independent event audit',
                  'observed_tool_events': None, 'underlying_requests': None}
    for field in TOKEN_FIELDS:
        values = [r[field] for r in attempts]
        accounting[field] = sum(values) if all(v is not None for v in values) else None
        accounting['known_' + field + '_subtotal'] = sum(v for v in values if v is not None)
        accounting['missing_' + field + '_attempts'] = sum(v is None for v in values)
    return {'analysis_type': 'POST_HOC', 'level1_status': 'COMPLETE', 'performance': performance,
            'paired_counts': dict(Counter(p['category'] for p in pairs)), 'pairs': pairs,
            'bootstrap': bootstrap([p['difference'] for p in pairs], seed, repetitions),
            'accounting': accounting, 'attempts': attempts}


def semantic_outcome(run, inverse=False):
    if run['timeout'] or run['returncode'] != 0:
        return 'UNRESOLVED'
    verified = bool(re.search(r': VERIFIED\s*$', run['stdout'], re.M))
    disproved = bool(re.search(r': DOES NOT HOLD\s*$', run['stdout'], re.M)) and 'Counterexample found:' in run['stdout']
    if verified == disproved:
        return 'UNRESOLVED'
    return 'PASS' if (disproved if inverse else verified) else 'FAIL'


def audit(root):
    """Check hashes, event coverage, response identity, and saved solver decisions."""
    manifest = read(root, 'manifest.json')
    index = read(root, 'index.json')
    issues = []
    entries = {e['path']: e for e in manifest['files']}
    if len(entries) != len(manifest['files']):
        issues.append({'status': 'INVALID', 'detail': 'Duplicate manifest path'})
    verified = set()
    for name, entry in entries.items():
        path = safe_path(root, name)
        if not path.is_file():
            issues.append({'status': 'MISSING', 'path': name})
        elif sha(path.read_bytes()) != entry['sha256']:
            issues.append({'status': 'HASH_MISMATCH', 'path': name})
        else:
            verified.add(name)
    for entry in index.get('missing_at_export', []):
        issues.append({'status': 'MISSING', 'path': entry})
    try:
        load_validation(root, index)
        ledger = [json.loads(line) for line in safe_path(root, 'source/artifacts/task_ledger.jsonl').read_text().splitlines()]
        if len(index['attempts']) != 110 or {r['task_id'] for r in ledger} != {r['task_id'] for r in index['attempts']}:
            raise ValueError('Attempt index does not cover the complete ledger')
    except (OSError, KeyError, TypeError, ValueError) as exc:
        issues.append({'status': 'INVALID', 'detail': str(exc)})

    def available(name):
        if name not in entries:
            issues.append({'status': 'UNMANIFESTED', 'path': name})
            return False
        return name in verified

    threads = []
    event_attempts = 0
    tools = 0
    completed = 0
    solver_scores = 0
    check_count = 0
    intact_solver_scores = 0
    matching_original_checks = 0
    reclassified_smoke = []
    token_values = {k: [] for k in TOKEN_FIELDS}
    known_event_types = {'thread.started', 'turn.started', 'turn.completed', 'turn.failed',
                         'error', 'item.started', 'item.updated', 'item.completed'}
    for entry in index['attempts']:
        tid = entry['task_id']
        try:
            if not all([available(entry['result']), available(entry['input']), available(entry['raw']['events.jsonl'])]):
                continue
            result, identity = read(root, entry['result']), read(root, entry['input'])
            if object_sha(identity) != result['cache_key']:
                raise ValueError('Input cache key differs')
            events = [json.loads(line) for line in safe_path(root, entry['raw']['events.jsonl']).read_text().splitlines()]
            if not events or any(not isinstance(e, dict) or e.get('type') not in known_event_types for e in events):
                raise ValueError('Empty, malformed, or unknown event stream')
            starts = [e['thread_id'] for e in events if e['type'] == 'thread.started']
            if len(starts) != 1:
                raise ValueError('Expected one fresh thread per attempt')
            threads.extend(starts)
            endings = [e for e in events if e['type'] == 'turn.completed']
            count = sum(e.get('item', {}).get('type') not in {'agent_message', 'reasoning', 'error'}
                        for e in events if e['type'].startswith('item.'))
            tools += count
            if count:
                issues.append({'status': 'TOOL_EVENT', 'task_id': tid})
            if len(endings) != result['turns_completed']:
                raise ValueError('Completion count differs from task result')
            usage = endings[-1].get('usage', {}) if endings else {}
            for field in TOKEN_FIELDS:
                if usage.get(field) != result.get(field):
                    raise ValueError('Usage differs from task result: ' + field)
                token_values[field].append(usage.get(field))
            for filename, name in entry['raw'].items():
                if not available(name):
                    continue
                expected = result['raw_sha256'].get(filename)
                if expected and entries[name]['sha256'] != expected:
                    raise ValueError('Original raw hash differs: ' + filename)
            if set(result['raw_sha256']) != set(entry['raw']):
                raise ValueError('Raw-file index omits recorded evidence')
            if result.get('final_response'):
                final_name = entry['raw'].get('final.txt')
                if not final_name or not available(final_name):
                    issues.append({'status': 'MISSING', 'path': final_name or tid + '/final.txt'})
                else:
                    final = safe_path(root, final_name).read_text().strip()
                    if final != result['final_response'].strip():
                        raise ValueError('Raw final differs from saved response')
                    messages = [e['item'].get('text') for e in events if e['type'] == 'item.completed' and e.get('item', {}).get('type') == 'agent_message']
                    if final not in messages:
                        raise ValueError('Final response not present in event stream')
            elif endings:
                raise ValueError('Completed turn has no saved final response')
            if tid.startswith('smoke-') and result['tool_events'] != count:
                reclassified_smoke.append({'task_id': tid, 'recorded': result['tool_events'], 'event_recount': count,
                                           'reason': 'Historical startup warning was misclassified; original retained.'})
            event_attempts += 1
            completed += bool(endings)
        except (KeyError, TypeError, ValueError) as exc:
            issues.append({'status': 'INVALID', 'task_id': tid, 'detail': str(exc)})
    if len(threads) != len(set(threads)):
        issues.append({'status': 'REUSED_THREAD'})
    for entry in index['validation']:
        try:
            needed = [entry['score'], *entry['verifier_raw'].values()]
            if not all([available(n) for n in needed]):
                continue
            score = read(root, entry['score'])
            original_complete = True
            attempt = next(a for a in index['attempts'] if a['task_id'] == entry['final_attempt'])
            if not available(attempt['result']):
                continue
            generation = read(root, attempt['result'])
            policy = json.loads(generation['final_response'])['policy']
            materials = read(root, 'source/data/manifest.json')
            material = next(r for r in materials['records'] if r['id'] == entry['scenario_id'])
            expected_key = object_sha({'scenario': entry['scenario_id'], 'policy': policy,
                                       'verifier': score['verifier_version'], 'materials': material['files']})
            if expected_key != score['cache_key']:
                raise ValueError('Scoring cache key differs from saved policy/materials')
            gate = read(root, entry['verifier_raw']['validate.json'])
            if gate['timeout'] or gate['returncode'] not in [0, 1, 3]:
                status = 'EVALUATION_UNRESOLVED'
            elif gate['returncode'] == 1:
                status = 'SYNTAX_FAIL'
            elif gate['returncode'] == 3:
                status = 'SCHEMA_FAIL'
            else:
                outcomes = []
                for i, check in enumerate(score['checks']):
                    name = entry['verifier_raw'][f'check-{i:02}.json']
                    if entries[name]['sha256'] != check['raw_sha256']:
                        original_complete = False
                        issues.append({'status': 'ORIGINAL_EVIDENCE_UNAVAILABLE', 'task_id': entry['task_id'],
                                       'path': name, 'original_recorded_sha256': check['raw_sha256'],
                                       'available_sha256': entries[name]['sha256']})
                    else:
                        matching_original_checks += 1
                    inverse = check['type'] in {'liveness-overlap', 'liveness', 'always-denies-liveness'}
                    outcome = semantic_outcome(read(root, name), inverse)
                    if outcome != check['status']:
                        raise ValueError('Solver outcome differs: ' + check['name'])
                    outcomes.append(outcome)
                    check_count += 1
                status = ('EVALUATION_UNRESOLVED' if not outcomes or 'UNRESOLVED' in outcomes else
                          'PASS' if all(s == 'PASS' for s in outcomes) else 'SEMANTIC_FAIL')
            if status != score['status']:
                raise ValueError('Validation status differs')
            if gate['returncode'] != 0 and score['checks']:
                raise ValueError('Semantic checks after failed validation gate')
            solver_scores += 1
            intact_solver_scores += original_complete
        except (KeyError, TypeError, ValueError) as exc:
            issues.append({'status': 'INVALID', 'task_id': entry['task_id'], 'detail': str(exc)})
    if event_attempts != len(index['attempts']) or solver_scores != len(index['validation']):
        issues.append({'status': 'COVERAGE_INCOMPLETE'})
    bad = any(i['status'] not in {'MISSING', 'COVERAGE_INCOMPLETE', 'ORIGINAL_EVIDENCE_UNAVAILABLE'} for i in issues)
    status = 'FAILED' if bad else 'INCOMPLETE' if issues else 'COMPLETE'
    return {'analysis_type': 'POST_HOC', 'level2_status': status,
            'scope': 'All 110 recorded model attempts and the 80 E4 saved verifier decisions; no solver re-execution or server attestation.',
            'manifest_files_verified': len(verified), 'manifest_files_expected': len(entries),
            'event_attempts_checked': event_attempts, 'event_attempts_expected': len(index['attempts']),
            'verifier_scores_checked': solver_scores, 'verifier_scores_expected': len(index['validation']),
            'scores_with_all_recorded_check_hashes_matching': intact_solver_scores,
            'semantic_checks_with_original_hash_matching': matching_original_checks,
            'historical_solver_hash_gaps': sum(i['status'] == 'ORIGINAL_EVIDENCE_UNAVAILABLE' for i in issues),
            'semantic_checks_reinterpreted': check_count, 'completed_attempts': completed if status == 'COMPLETE' else None,
            'distinct_thread_ids': len(set(threads)) if status == 'COMPLETE' else None,
            'observed_tool_events': tools if status == 'COMPLETE' else None,
            'tool_audit_status': 'COMPLETE' if status == 'COMPLETE' else 'UNKNOWN',
            'known_tool_event_records_in_available_files': tools,
            'historical_smoke_classification_corrections': reclassified_smoke,
            'issues': issues,
            'usage': {k: {'total': sum(v) if status == 'COMPLETE' and all(x is not None for x in v) else None,
                          'known_subtotal': sum(x for x in v if x is not None),
                          'missing_attempts': len(index['attempts']) - sum(x is not None for x in v)} for k, v in token_values.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['analyze', 'audit'])
    parser.add_argument('package', type=Path)
    parser.add_argument('--output', type=Path, help='New output directory; existing paths are rejected')
    parser.add_argument('--seed', type=int, default=20261111)
    parser.add_argument('--repetitions', type=int, default=100000)
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error('Output already exists; choose a new analysis directory')
    try:
        result = analyze(args.package, args.seed, args.repetitions) if args.command == 'analyze' else audit(args.package)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {'level1_status' if args.command == 'analyze' else 'level2_status': 'INCOMPLETE',
                  'observed_tool_events': None, 'tool_audit_status': 'UNKNOWN', 'error': str(exc)}
    if args.output:
        args.output.mkdir(parents=True)
        write_json(args.output / 'results.json', result)
        if args.command == 'analyze' and result.get('level1_status') == 'COMPLETE':
            for key in ['performance', 'pairs', 'attempts']:
                write_csv(args.output / (key + '.csv'), result[key])
            write_json(args.output / 'bootstrap.json', result['bootstrap'])
            write_csv(args.output / 'bootstrap_histogram.csv', result['bootstrap']['replicate_histogram'])
    summary = {k: v for k, v in result.items() if k not in {'attempts', 'pairs'}}
    if 'bootstrap' in summary:
        summary['bootstrap'] = {k: v for k, v in summary['bootstrap'].items() if k not in {'replicate_histogram', 'pair_differences'}}
    print(json.dumps(summary, indent=2))
    return 0 if result.get('level1_status', result.get('level2_status')) == 'COMPLETE' else 2


if __name__ == '__main__':
    sys.exit(main())

"""Prepare English mid-report notes from a saved portable review package only."""
import argparse
from collections import Counter
import json
from pathlib import Path
from review_offline import read, sha, write_csv, write_json

CASES = {
    'kubernetes_rbac-readSecret-T3-033': {
        'keywords': ['clearance', 'own', 'expired', 'expire'],
        'schema': ['owner', 'sensitivity', 'clearance', 'expiresAt', 'currentTime', 'serviceAccountToken'],
        'lines': {'Meta': [(7, 14), (45, 47)], 'Refine': [(6, 9), (15, 17), (33, 38)]},
        'explanation': 'Meta calls decimal comparison methods on datetime-valued currentTime and expiresAt. The recorded validator exits with code 3 before any semantic checks. Refine uses the datetime >= operator for the expired-token veto and passes all seven recorded checks. This identifies a target-language type/API error in this particular Meta output.',
        'cannot': 'It does not establish that the Meta authorization logic would pass after a syntax/type edit: no edited policy was evaluated. It does not show a general semantic-reasoning advantage for Refine or identify which harness sentence caused the error.',
    },
    'grant_awards-chain2-T3-005': {
        'keywords': ['obligat', 'grants officer', 'workflow'],
        'schema': ['entity Role', 'roles:', 'approvedBy', 'obligatedBy', 'action obligateFunds'],
        'lines': {'Meta': [(23, 31)], 'Refine': [(23, 39), (46, 50)]},
        'explanation': 'Both policies pass syntax and schema validation. Refine permits obligateFunds for ProgramOfficer but forbids it for anyone without GrantsOfficer. The resulting grant effectively requires both roles. The saved floor counterexample has only GrantsOfficer and an approvedBy value pointing to another user, so a required request is denied. The saved ceiling counterexample has both roles and no approvedBy attribute, so Refine allows an obligation outside the verification plan. Meta requires GrantsOfficer, approvedBy presence, and a different approver and passes all five recorded checks.',
        'cannot': 'This one semantic success does not show that Meta generally reasons better about workflows. The approval-presence requirement is explicitly enforced by the verification plan; its interpretation from the prose is not independently adjudicated. Passing five checks is not proof of correctness against every possible informal reading.',
    },
    'iot_fleet-sendCommand-T3-029': {
        'keywords': ['window', 'active', 'owner'],
        'schema': ['entity MaintenanceWindow', 'startTime', 'endTime', 'permitted:', 'currentTime', 'maintenanceWindow:', 'DeviceStatus'],
        'lines': {'Meta': [(19, 26)], 'Refine': [(6, 27), (33, 44)]},
        'explanation': 'Meta uses greaterThanOrEqual and lessThanOrEqual on datetime fields in the maintenance-window veto. The validator reports expected decimal but saw datetime and exits with code 3. Refine uses >= and <= for the window and passes eight recorded checks covering active devices, owned non-active devices, non-owner restrictions, and liveness.',
        'cannot': 'The logs do not determine whether a repaired Meta policy would satisfy the device-status exceptions. No repair or counterfactual policy generation was performed. This is another observed type error, not an independent harness construction replicate.',
    },
    'immigration_casework-clearSecurityCheck-T3-024': {
        'keywords': ['pending', 'window', 'supervisory officer'],
        'schema': ['entity Role', 'roles:', 'status:', 'permittedWindow', 'currentTime'],
        'lines': {'Meta': [(6, 11), (18, 22), (30, 34)], 'Refine': [(6, 11), (18, 22), (29, 32), (39, 43)]},
        'explanation': 'Meta again invokes decimal comparison methods on datetime window endpoints; validation exits with code 3 before semantic evaluation. Refine uses datetime comparison operators and passes the five saved floor, ceiling, disjointness, and liveness checks. Its non-pending investigator veto is visible in the original output.',
        'cannot': 'A passing verification plan does not settle every informal interpretation of overlapping investigator/supervisor roles or exception precedence. These outputs do not isolate a causal effect of guidance versus revision, and the Meta semantic outcome after a hypothetical type repair remains unknown.',
    },
}


def markdown_table(rows):
    columns = list(rows[0])
    return '| ' + ' | '.join(columns) + ' |\n| ' + ' | '.join('---' for _ in columns) + ' |\n' + '\n'.join(
        '| ' + ' | '.join(str(row[k]) for k in columns) + ' |' for row in rows)


def selected_lines(text, keywords=None, ranges=None):
    lines = text.splitlines()
    selected = set()
    if keywords:
        selected = {i for i, line in enumerate(lines, 1) if any(k.lower() in line.lower() for k in keywords)}
    if ranges:
        selected |= {i for a, b in ranges for i in range(a, min(b, len(lines)) + 1)}
    return '\n'.join(f'L{i}: {lines[i - 1]}' for i in sorted(selected))


def build(root, output):
    if output.exists():
        raise ValueError('Never overwrite a prior analysis version')
    output.mkdir(parents=True)
    (output / 'cases').mkdir()
    package = root / 'review_bundle'
    index = read(package, 'index.json')
    results = read(root, 'analysis/results.json')
    audit = read(root, 'analysis/evidence_audit.json')
    scenarios = {r['id']: r for r in map(json.loads, (package / index['validation_inputs']).read_text().splitlines())}
    rows = {(r['scenario_id'], r['method']): r for r in index['validation']}
    attempts = {r['task_id']: r for r in index['attempts']}
    paired = {r['scenario_id']: r for r in results['pairs']}
    discordant = {r['scenario_id'] for r in results['pairs'] if r['category'] in ['meta_only', 'refine_only']}
    assert discordant == set(CASES)
    case_index = []
    for sid, spec in CASES.items():
        scenario = scenarios[sid]
        text = [f'# {sid}', '', 'POST-HOC case audit. All four discordant cases are included; no case was resampled or repaired.',
                '', f'Pair category: **{paired[sid]["category"]}**.', '', '## Required input excerpts',
                '', 'Line numbers refer to the original requirements/schema strings, not a rewritten specification.', '',
                '```text\n' + selected_lines(scenario['requirements'], spec['keywords']) + '\n```',
                '', '```text\n' + selected_lines(scenario['schema'], spec['schema']) + '\n```',
                '', f'Complete inputs: [frozen validation JSONL](../../review_bundle/{index["validation_inputs"]}).']
        machine = {'scenario_id': sid, 'pair_category': paired[sid]['category'], 'methods': {}}
        for method in ['Meta', 'Refine']:
            row = rows[sid, method]
            attempt = attempts[row['final_attempt']]
            raw_final = package / attempt['raw']['final.txt']
            policy = json.loads(raw_final.read_text())['policy']
            score = read(package, row['score'])
            gate = read(package, row['verifier_raw']['validate.json'])
            validation_excerpt = gate['stdout'] if method == 'Refine' or score['status'] == 'PASS' else '\n'.join(gate['stdout'].splitlines()[:9])
            text += ['', f'## {method}: {score["status"]}', '',
                     f'Original final response: [raw JSON](../../review_bundle/{attempt["raw"]["final.txt"]}); SHA-256 `{sha(raw_final.read_bytes())}`.',
                     '', 'Key policy lines (JSON string decoded for display only; no changes):', '',
                     '```text\n' + selected_lines(policy, ranges=spec['lines'][method]) + '\n```', '',
                     f'Original validator return code: `{gate["returncode"]}`. [Complete original log](../../review_bundle/{row["verifier_raw"]["validate.json"]}).',
                     '', '```text\n' + validation_excerpt.rstrip() + '\n```', '']
            checks = []
            for i, check in enumerate(score['checks']):
                logpath = row['verifier_raw'][f'check-{i:02}.json']
                log = read(package, logpath)
                assert sha((package / logpath).read_bytes()) == check['raw_sha256'], 'Discordant-case original must be available'
                text += [f'- `{check["name"]}` ({check["type"]}): **{check["status"]}**. [Raw solver output](../../review_bundle/{logpath}).']
                checks.append({'name': check['name'], 'type': check['type'], 'status': check['status'], 'raw_path': logpath, 'original_sha256': check['raw_sha256']})
                if check['status'] == 'FAIL':
                    text += ['', 'Original counterexample (verbatim stdout):', '', '```text\n' + log['stdout'].rstrip() + '\n```', '']
            if not checks:
                text += ['Semantic checks were **not run** after the failed schema/type gate. Their outcome is unknown.']
            machine['methods'][method] = {'status': score['status'], 'final_response': attempt['raw']['final.txt'],
                                           'final_sha256': sha(raw_final.read_bytes()), 'score': row['score'],
                                           'validator': row['verifier_raw']['validate.json'], 'checks': checks}
        text += ['', '## Supported explanation', '', spec['explanation'], '', '## Unsupported conclusions', '', spec['cannot'], '',
                 'Both results retain their original contribution to the primary 20-scenario denominator. This case audit does not define a replacement metric.', '']
        (output / 'cases' / (sid + '.md')).write_text('\n'.join(text))
        case_index.append(machine)
    write_json(output / 'case_evidence.json', case_index)
    methods = [
        {'method': 'Manual (fixed baseline)', 'design_stages': 0, 'construction': 'Static baseline prepared in AI-assisted research workflow', 'construction_attempts': 0, 'harness_repeats': 1, 'validation_outputs': 20},
        {'method': 'Direct', 'design_stages': 1, 'construction': 'Frozen packet -> harness', 'construction_attempts': 1, 'harness_repeats': 1, 'validation_outputs': 20},
        {'method': 'Meta', 'design_stages': 2, 'construction': 'Frozen packet -> guidance; fresh session -> harness', 'construction_attempts': 3, 'harness_repeats': 1, 'validation_outputs': 20},
        {'method': 'Refine', 'design_stages': 2, 'construction': 'Frozen packet -> draft; fresh session -> revision', 'construction_attempts': 2, 'harness_repeats': 1, 'validation_outputs': 20},
    ]
    data = read(package, 'source/data/manifest.json')
    splits = []
    for split in ['design20', 'validation20']:
        records = [r for r in data['records'] if r['split'] == split]
        splits.append({'split': split, 'scenarios': len(records), 'families': len({r['family'] for r in records}),
                       'structural_signatures': len({r['sig'] for r in records}),
                       'published_origins': json.dumps(dict(Counter(r['upstream_split'] for r in records))),
                       'purpose': 'shared development evidence' if split == 'design20' else 'four-method paired validation', 'content_opened': 'yes'})
    splits.append({'split': 'published held-out', 'scenarios': data['published_counts']['heldout'], 'families': 'not inspected',
                   'structural_signatures': 'not inspected', 'published_origins': 'heldout', 'purpose': 'future final evaluation', 'content_opened': 'no'})
    pair_table = [{'category': c, 'scenarios': results['paired_counts'][c]} for c in ['both_pass', 'meta_only', 'refine_only', 'both_fail']]
    write_csv(output / 'methods.csv', methods)
    write_csv(output / 'data_splits.csv', splits)
    write_csv(output / 'performance_error_types.csv', results['performance'])
    write_csv(output / 'paired_counts.csv', pair_table)
    infra = []
    for attempt in results['attempts']:
        if attempt['timeout']:
            infra.append({'attempt_id': attempt['task_id'], 'stage': attempt['group'], 'configured_seconds': 180,
                          'observed_wall_seconds': attempt['elapsed_seconds'], 'response_present': attempt['has_final_response'],
                          'usage': 'UNKNOWN', 'recovery': 'one same-input fresh-session retry'})
    write_csv(output / 'infrastructure_failures.csv', infra)
    table_text = ['# Mid-report tables', '', 'POST-HOC organization of unchanged E0-E5 results.', '',
                  '## Methods', '', markdown_table(methods), '',
                  'Fixed conditions: official Codex CLI 0.162.0-alpha.17.2; requested gpt-6.1-sol, medium effort; static harness at most 500 words; fresh sessions; same schema/requirements/public instructions; no task tools, verifier feedback, or policy repair. Actual serving model unknown. Meta and Refine each have two logical stages, not necessarily equal compute.', '',
                  '## Data', '', markdown_table(splits), '',
                  f'Upstream revision `{data["upstream_commit"]}`. Published SFT/RL counts: 4386/1039. Grouping uses the transitive union of scenario family and normalized schema+gold structural signature, then one sampled member from each of 40 shuffled groups (seed 20261110); 139 non-held-out groups were eligible. No new selection occurred in this analysis.', '',
                  '## Performance and mutually exclusive primary error classes', '', markdown_table(results['performance']), '',
                  'All type failures remain in the denominator. Overgrant/overdeny are overlapping diagnostics among semantically evaluated outputs, not additional mutually exclusive categories. No conditional type-valid subset rate replaces these results.', '',
                  '## Paired Meta-Refine outcomes', '', markdown_table(pair_table), '',
                  'Difference: -10 percentage points. Post-hoc paired percentile bootstrap: 95% interval [-30, +10] percentage points; 100,000 resamples of 20 scenario pairs, seed 20261111. Conditional on these harnesses and saved outputs; no construction randomness included. Zero in the interval does not imply equivalence.', '',
                  '## Infrastructure attempts (separate from final policy error classes)', '', markdown_table(infra), '',
                  'The 80 E4 final outputs required 81 attempts; the extra missing-response timeout belongs to Refine. Meta construction required one extra attempt before validation. Total: 110 attempts, 108 completed; five logical construction stages, 100 final policies, three smoke diagnostics. No new calls in P1.', '']
    (output / 'tables.md').write_text('\n'.join(table_text))
    gaps = [i for i in audit['issues'] if i['status'] == 'ORIGINAL_EVIDENCE_UNAVAILABLE']
    write_csv(output / 'historical_solver_hash_gaps.csv', gaps)
    summary = Counter(i['task_id'] for i in gaps)
    write_csv(output / 'historical_gap_by_task.csv', [{'task_id': k, 'missing_original_log_hashes': v} for k, v in sorted(summary.items())])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('analysis_root', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    build(args.analysis_root, args.output)

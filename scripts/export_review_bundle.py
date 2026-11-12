"""Export an allowlisted, byte-preserving E0-E5 review package without execution."""
import argparse
import json
from pathlib import Path
import re
from review_offline import sha, safe_path, write_json

E4 = 'artifacts/experiments/E4-20261110-validation'
SECRETS = {
    'private_key': rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
    'github_token': rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})',
    'api_key': rb'sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}',
    'aws_key': rb'AKIA[0-9A-Z]{16}',
    'bearer_token': rb'(?i)authorization[\s\x22\x27:=>]+bearer\s+[A-Za-z0-9._~+/-]{20,}',
}


def export(repo, out):
    if out.exists():
        raise ValueError('Output exists; never overwrite a review package')
    out.mkdir(parents=True)
    files = {}
    missing = []
    historical_gaps = []

    def copy(source, name, original_sha=None, kind='original', source_label=None, retain_mismatch=False):
        dest = safe_path(out, name)
        if not source.is_file():
            missing.append(name)
            return name
        if source.is_symlink():
            raise ValueError('Symlinks are not accepted: ' + name)
        data = source.read_bytes()
        digest = sha(data)
        if original_sha and digest != original_sha:
            if not retain_mismatch:
                raise ValueError('Original hash mismatch: ' + name)
            historical_gaps.append({'path': name, 'original_recorded_sha256': original_sha,
                                    'available_sha256': digest, 'status': 'ORIGINAL_EVIDENCE_UNAVAILABLE'})
        for label, pattern in SECRETS.items():
            if re.search(pattern, data):
                raise ValueError('Credential pattern detected in ' + name + ': ' + label)
        if name in files and files[name]['sha256'] != digest:
            raise ValueError('Conflicting export path: ' + name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        recorded = sorted(set(files.get(name, {}).get('original_recorded_sha256_values', []) + ([original_sha] if original_sha else [])))
        files[name] = {'path': name, 'sha256': digest, 'bytes': len(data), 'kind': kind,
                       'original_recorded_sha256_values': recorded,
                       'all_recorded_hashes_match_available_bytes': all(h == digest for h in recorded) if recorded else None,
                       'hash_provenance': 'recorded during experiment' if original_sha else 'first captured at post-hoc export',
                       'source': source_label or name}
        return name

    def source(rel):
        return copy(repo / rel, 'source/' + rel, source_label='repository:' + rel)

    inputs = source('data/validation20.jsonl')
    source('data/design20.jsonl')
    source('data/manifest.json')
    source('artifacts/task_ledger.jsonl')
    source(E4 + '/summary-20.json')
    source('artifacts/experiments/E1-20261110-sanity/results.json')
    source('artifacts/experiments/E2-20261110-manual/summary-20.json')
    source('artifacts/experiments/E3R-20261110-recovery/all_attempts.json')
    source('artifacts/experiments/E5-20261110-evidence/analysis_corrections.json')
    for rel in ['configs/manual.json', 'configs/runtime.json', 'configs/verifier.json', 'configs/public_instructions.txt',
                'artifacts/harnesses/direct.json', 'artifacts/harnesses/meta.json', 'artifacts/harnesses/refine.json',
                'src/harness_lab/verifier.py', 'src/harness_lab/protocol.py', 'src/harness_lab/backend.py']:
        source(rel)
    attempts = []
    results = {}
    for path in sorted((repo / 'artifacts/experiments').rglob('result.json')):
        result = json.loads(path.read_text())
        if 'task_id' in result and 'raw_sha256' in result:
            if result['task_id'] in results:
                raise ValueError('Duplicate result identity')
            results[result['task_id']] = (path, result)
    ledger = [json.loads(line) for line in (repo / 'artifacts/task_ledger.jsonl').read_text().splitlines()]
    for task in ledger:
        tid = task['task_id']
        path, result = results[tid]
        if task['cache_key'] != result['cache_key']:
            raise ValueError('Ledger and result disagree')
        raw = {}
        for filename in ['events.jsonl', 'final.txt', 'stderr.txt', 'schema.json']:
            # Missing finals on the two timed-out attempts are historical absence,
            # not a silently omitted successful answer.
            if filename not in result['raw_sha256']:
                if filename == 'events.jsonl' or (filename == 'final.txt' and result.get('final_response')):
                    missing.append(f'raw/model/{tid}/{filename}')
                continue
            raw[filename] = copy(Path(task['raw_directory']) / filename, f'raw/model/{tid}/{filename}',
                                 result['raw_sha256'][filename], source_label=f'external:model/{tid}/{filename}')
        group = ('connectivity' if tid.startswith('smoke-') else 'construction' if tid.startswith(('E3-', 'E3R-')) else
                 'validation_policy' if tid.startswith('E4-') else 'development_policy')
        attempts.append({'task_id': tid, 'group': group, 'result': source(path.relative_to(repo).as_posix()),
                         'input': source((path.parent / 'input.json').relative_to(repo).as_posix()), 'raw': raw,
                         'final_absence_at_execution': not result.get('final_response')})
        if tid.startswith('smoke-') and (path.parent / 'analysis.json').exists():
            source((path.parent / 'analysis.json').relative_to(repo).as_posix())
    manifest = json.loads((repo / 'data/manifest.json').read_text())
    metadata = {r['id']: r for r in manifest['records']}
    records = json.loads((repo / E4 / 'summary-20.json').read_text())['records']
    validation = []
    for row in records:
        tid, score = row['task_id'], row['score']
        score_path = repo / E4 / 'scores' / tid / 'score.json'
        if json.loads(score_path.read_text()) != score:
            raise ValueError('Summary differs from original score')
        _, original_generation = results[row['generation']['task_id']]
        if any(row['generation'][k] != v for k, v in original_generation.items()):
            raise ValueError('Summary differs from original generation')
        raw = {'validate.json': copy(Path(score['raw_directory']) / 'validate.json',
                                    f'raw/verifier/{score["cache_key"]}/validate.json',
                                    source_label=f'external:verifier/{score["cache_key"]}/validate.json')}
        for i, check in enumerate(score['checks']):
            filename = f'check-{i:02}.json'
            raw[filename] = copy(Path(score['raw_directory']) / filename,
                                 f'raw/verifier/{score["cache_key"]}/{filename}', check['raw_sha256'],
                                 source_label=f'external:verifier/{score["cache_key"]}/{filename}', retain_mismatch=True)
        validation.append({'task_id': tid, 'scenario_id': row['scenario_id'], 'method': row['method'],
                           'final_attempt': row['generation']['task_id'],
                           'score': source(score_path.relative_to(repo).as_posix()), 'verifier_raw': raw})
    # Only already-selected validation materials and one identified development
    # ambiguity are exported. No corpus archive or held-out content is opened.
    material_ids = {r['scenario_id'] for r in records} | {'patent_prosecution-examineApplication-T2-005'}
    materials = {}
    for sid in sorted(material_ids):
        row = metadata[sid]
        material = {}
        for filename, expected in row['files'].items():
            if filename not in {'schema.cedarschema', 'verification_plan.py', 'intent.md'} and not filename.startswith('references/'):
                continue
            material[filename] = copy(Path(row['scenario_directory']) / filename, f'materials/{sid}/{filename}',
                                      expected, source_label=f'upstream:{manifest["upstream_commit"]}/{sid}/{filename}')
        materials[sid] = material
    copy(repo / 'scripts/review_offline.py', 'review.py', kind='review_tool', source_label='repository:scripts/review_offline.py')
    index = {'format': 'harness-review-v1', 'analysis_type': 'POST_HOC', 'date': '2026-11-11',
             'validation_inputs': inputs, 'attempts': attempts, 'validation': validation,
             'materials': materials, 'missing_at_export': sorted(set(missing)), 'historical_evidence_gaps': historical_gaps,
             'scope': {'validation_scores': 80, 'model_attempts': 110, 'heldout_content': False,
                       'solver_reexecution': False, 'model_calls': 0},
             'path_rule': 'All operational paths are relative to this package. Absolute paths inside untouched source records and raw command arrays are provenance only and are never opened.'}
    write_json(out / 'index.json', index)
    files['index.json'] = {'path': 'index.json', 'sha256': sha((out / 'index.json').read_bytes()),
                           'bytes': (out / 'index.json').stat().st_size, 'kind': 'derived_index',
                           'original_recorded_sha256': None, 'hash_provenance': 'created at post-hoc export',
                           'source': 'derived from saved results and allowlisted evidence'}
    readme = '''# Portable review package (post-hoc, 2026-11-11)

This package preserves original evidence bytes and historical failures. It contains
all 110 model-attempt event records, final responses when present, diagnostic
stderr/schema files, and the 80 E4 verifier runs with their referenced materials.
It excludes credentials, login stores, unrelated personal files, host prompt/debug
captures, model binaries, corpus archives, and all final held-out content.

Run with Python 3.10 or later, from any working directory:

```bash
python3 /path/to/package/review.py analyze /path/to/package --output /new/metrics
python3 /path/to/package/review.py audit /path/to/package --output /new/audit
```

`analyze` recomputes saved-result metrics, paired bootstrap, and attempt accounting.
It does not claim to audit tool activity. `audit` separately verifies file hashes,
raw event coverage, usage/final-response identity, and saved solver outcomes.
Missing evidence yields INCOMPLETE, UNKNOWN tool-audit status, null aggregate tool
events, and exit code 2. Contradictory or tampered evidence yields FAILED.
Neither command runs a model, executes verification plans, or launches a solver.
The package does not establish independently re-executed theorem proofs or an
authenticated transcript from the server.

The export identifies 61 historical solver-log checksum mismatches affecting nine
earlier scenario-method scores in seven shared verifier directories. The scoring
code reused a directory for identical scenario/policy/verifier/material keys and
wrote new logs when another method received the same policy. Available later logs
are preserved, but they cannot replace the missing byte-identical earlier logs.
The full historical audit is therefore INCOMPLETE even with every exported file
present. All four Meta-Refine discordant cases are unaffected. Saved scores remain
unchanged; no missing historical evidence is repaired by re-execution.

Manifest hashes distinguish checksums recorded during the experiment from hashes
first captured at export (notably validate.json, which had no prior raw checksum).
No evidence was redacted, translated, or rewritten. Raw files and copied original
records can contain historical user paths, temporary paths, and session IDs;
these are inert provenance and do not make execution depend on that host.
This package is portable but is NOT an anonymous submission supplement.
Produce separately labeled derived redacted copies if an anonymous supplement is
later required; preserve these originals and their hashes.
'''
    (out / 'README.md').write_text(readme)
    files['README.md'] = {'path': 'README.md', 'sha256': sha(readme.encode()), 'bytes': len(readme.encode()),
                          'kind': 'review_documentation', 'original_recorded_sha256': None,
                          'hash_provenance': 'created at post-hoc export', 'source': 'exporter'}
    write_json(out / 'manifest.json', {'format': 'harness-review-manifest-v1', 'analysis_type': 'POST_HOC',
                                      'files': [files[k] for k in sorted(files)],
                                      'redactions': [], 'credential_scan': 'Allowlisted inputs plus common token/private-key patterns; no findings. This is not a proof of absence of all sensitive strings.',
                                      'non_english_originals': 'Preserved unchanged under the explicit evidence-export instruction; not authored repository prose.'})
    return {'package': str(out), 'files': len(files), 'bytes': sum(f['bytes'] for f in files.values()),
            'missing': sorted(set(missing)), 'historical_evidence_gaps': len(historical_gaps),
            'manifest_sha256': sha((out / 'manifest.json').read_bytes())}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(export(args.repo.resolve(), args.output), indent=2))

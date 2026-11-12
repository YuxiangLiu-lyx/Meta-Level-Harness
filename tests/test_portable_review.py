"""Evidence absence, tampering, and paired sampling must not create false success."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from review_offline import analyze, audit, bootstrap, safe_path, sha
from export_review_bundle import export

PACKAGE = ROOT / 'artifacts/posthoc/P1-20261111-midreport/review_bundle'


class PortableReview(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'package'
        shutil.copytree(PACKAGE, self.root)
        self.addCleanup(self.temp.cleanup)

    def test_saved_metrics_survive_missing_all_raw_evidence(self):
        before = analyze(self.root, repetitions=1000)
        shutil.rmtree(self.root / 'raw')
        self.assertEqual(before, analyze(self.root, repetitions=1000))
        result = audit(self.root)
        self.assertEqual(result['level2_status'], 'INCOMPLETE')
        self.assertIsNone(result['observed_tool_events'])
        self.assertEqual(result['tool_audit_status'], 'UNKNOWN')
        self.assertEqual(result['event_attempts_checked'], 0)

    def test_known_historical_hash_gaps_are_not_reported_as_complete(self):
        result = audit(self.root)
        self.assertEqual(result['level2_status'], 'INCOMPLETE')
        self.assertEqual(result['historical_solver_hash_gaps'], 61)
        self.assertEqual(result['scores_with_all_recorded_check_hashes_matching'], 71)
        self.assertEqual(result['event_attempts_checked'], 110)
        self.assertIsNone(result['observed_tool_events'])

    def test_tampered_raw_bytes_fail(self):
        path = next((self.root / 'raw/model').glob('*/events.jsonl'))
        path.write_text(path.read_text() + '{}\n')
        result = audit(self.root)
        self.assertEqual(result['level2_status'], 'FAILED')
        self.assertTrue(any(i['status'] == 'HASH_MISMATCH' for i in result['issues']))
        self.assertIsNone(result['observed_tool_events'])

    def test_changed_score_is_caught_even_if_export_checksum_is_updated(self):
        index = json.loads((self.root / 'index.json').read_text())
        name = index['validation'][0]['score']
        path = self.root / name
        value = json.loads(path.read_text())
        value['status'] = 'SEMANTIC_FAIL'
        path.write_text(json.dumps(value))
        manifest = json.loads((self.root / 'manifest.json').read_text())
        next(e for e in manifest['files'] if e['path'] == name)['sha256'] = sha(path.read_bytes())
        (self.root / 'manifest.json').write_text(json.dumps(manifest))
        result = audit(self.root)
        self.assertEqual(result['level2_status'], 'FAILED')
        self.assertTrue(any('Validation status differs' in i.get('detail', '') for i in result['issues']))

    def test_export_refuses_overwrite(self):
        with self.assertRaisesRegex(ValueError, 'never overwrite'):
            export(ROOT, self.root)

    def test_package_path_cannot_escape(self):
        for name in ['../outside', '/Users/secret', 'a/../../outside', '..\\outside']:
            with self.assertRaises(ValueError):
                safe_path(self.root, name)


class PairedBootstrap(unittest.TestCase):
    def test_identical_paired_methods_have_zero_variability(self):
        result = bootstrap([0] * 20, seed=41, repetitions=1000)
        self.assertEqual(result['estimate_pp'], 0)
        self.assertEqual(result['interval_pp'], [0, 0])
        self.assertEqual(result['n_pairs'], 20)

    def test_signed_pair_differences_and_seed_reproduce(self):
        differences = [0] * 8 + [1] + [-1] * 3 + [0] * 8
        a = bootstrap(differences, seed=20261111, repetitions=1000)
        self.assertEqual(a, bootstrap(differences, seed=20261111, repetitions=1000))
        self.assertEqual(a['estimate_pp'], -10)
        self.assertEqual(sum(r['count'] for r in a['replicate_histogram']), 1000)
        self.assertEqual(bootstrap([1] * 20, repetitions=100)['interval_pp'], [100, 100])


if __name__ == '__main__':
    unittest.main()

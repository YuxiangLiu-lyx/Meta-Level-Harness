"""Reporting must retain unknown retry cost and support repeatable exports."""
import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from analyze import save_csv, usage_total


class Reporting(unittest.TestCase):
    def test_unknown_retry_usage_is_not_zero(self):
        rows=[{'generation':{'input_tokens':100,'attempts':[{'input_tokens':None},{'input_tokens':100}]}}]
        self.assertIsNone(usage_total(rows,'input_tokens'))

    def test_complete_attempt_usage_is_added_once(self):
        rows=[{'generation':{'input_tokens':100,'attempts':[{'input_tokens':40},{'input_tokens':100}]}}]
        self.assertEqual(usage_total(rows,'input_tokens'),140)

    def test_csv_export_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'results.csv';rows=[{'method':'Meta','pass':1}]
            save_csv(path,rows);before=path.read_bytes();save_csv(path,rows)
            self.assertEqual(path.read_bytes(),before)
            with self.assertRaises(RuntimeError):save_csv(path,[{'method':'Meta','pass':2}])


if __name__=='__main__':unittest.main()

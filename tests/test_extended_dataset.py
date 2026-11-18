import csv
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from generate_extended_dataset import generate,OUT

class ExtendedDatasetTests(unittest.TestCase):
    def test_reproducible_and_mixed(self):
        a=generate()
        b=generate()
        self.assertEqual(a["sha256"],b["sha256"])
        self.assertEqual(a["total_records"],2440)
        with (OUT/"transactions.csv").open(newline="",encoding="utf-8") as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),2440)
        self.assertEqual(len({r["transaction_id"] for r in rows}),2440)
        self.assertEqual({r["scenario_tag"] for r in rows},
            {"background","rapid_sender","onward_path","scheduled_payroll","recipient_concentration"})
        self.assertTrue(any(r["status"]=="FAILED" for r in rows))
        self.assertEqual(rows,sorted(rows,key=lambda r:(r["timestamp_utc"],r["transaction_id"])))

    def test_reject_tiny_dataset(self):
        with self.assertRaises(ValueError):
            generate(normal_count=50)

if __name__=="__main__":
    unittest.main()

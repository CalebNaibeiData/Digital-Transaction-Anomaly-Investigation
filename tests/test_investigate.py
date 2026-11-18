import csv
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from investigate import generate, sha256, analyze, run

class InvestigationTests(unittest.TestCase):
    def test_deterministic_source(self):
        first = sha256(generate())
        self.assertEqual(first, sha256(generate()))

    def test_expected_record_count(self):
        with generate().open(encoding="utf-8", newline="") as f:
            self.assertEqual(sum(1 for _ in csv.DictReader(f)), 521)

    def test_planted_patterns_detected(self):
        records, flags, sql_results = analyze(generate())
        self.assertEqual(len(records), 521)
        self.assertTrue(sql_results)
        self.assertTrue(any(f["rule"] == "burst_8_in_10m" and
                            f["sender_id"] == "U007" and f["recipient_id"] == "U099"
                            for f in flags))
        self.assertTrue(any(f["rule"] == "many_to_one_8_senders" and
                            f["recipient_id"] == "U140" for f in flags))

    def test_manifest_matches_source(self):
        run()
        manifest = json.loads((ROOT/"reports"/"evidence_manifest.json").read_text())
        self.assertEqual(manifest["sha256"], sha256(ROOT/"data"/"transactions.csv"))

if __name__ == "__main__":
    unittest.main()

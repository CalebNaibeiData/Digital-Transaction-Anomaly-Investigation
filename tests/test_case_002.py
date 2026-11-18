import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
import forensic_pipeline as fp

class Case002Tests(unittest.TestCase):
    def setUp(self):
        self.accounts,self.auth,self.txs=fp.generate()

    def test_source_is_deterministic(self):
        h=fp.sha256(fp.DATA/"transactions.csv")
        fp.generate()
        self.assertEqual(h,fp.sha256(fp.DATA/"transactions.csv"))

    def test_data_quality(self):
        self.assertEqual([],fp.validate(self.accounts,self.auth,self.txs))
        bad=[dict(x) for x in self.txs]
        bad[0]["sender_id"]="UNKNOWN"
        self.assertTrue(fp.validate(self.accounts,self.auth,bad))

    def test_account_access_hypothesis(self):
        findings,paths,_,_=fp.analyze(self.accounts,self.auth,self.txs)
        self.assertTrue(any(f["id"]=="F-AUTH-A100" and "L004" in f["evidence_ids"] for f in findings))
        self.assertTrue(any(f["id"]=="F-BURST-A100-A200" for f in findings))

    def test_temporal_trace(self):
        _,paths,_,_=fp.analyze(self.accounts,self.auth,self.txs)
        self.assertTrue(any(p["destination"]=="A600" and p["hops"]==3 for p in paths))
        self.assertFalse(any(len(p["transaction_ids"])!=p["hops"] for p in paths))

    def test_failed_transfer_excluded(self):
        _,_,_,successful=fp.analyze(self.accounts,self.auth,self.txs)
        self.assertNotIn("T007",{t["transaction_id"] for t in successful})

    def test_manifest(self):
        fp.run()
        manifest=json.loads((fp.OUT/"manifest.json").read_text())
        for item in manifest["files"]:
            self.assertEqual(item["sha256"],fp.sha256(ROOT/item["path"]))

    def test_sql_exhibits(self):
        exhibits=fp.sql_exhibits(self.accounts,self.auth,self.txs)
        self.assertEqual(len(exhibits),4)
        self.assertTrue(exhibits[0]["rows"])

if __name__=="__main__":
    unittest.main()

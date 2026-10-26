import json
import csv
import unittest
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from investment_lab.unitree_report import generate_unitree_report

class TestUnitreeICArtifacts(unittest.TestCase):
    def test_all_files_and_evidence_links(self):
        results=generate_unitree_report(ROOT)
        self.assertEqual(len(results),4)
        for f in results:
            self.assertTrue(f.is_file())
            self.assertGreater(f.stat().st_size,100)
        data=json.loads((ROOT/"reports"/"unitree_ic_decision.json").read_text("utf-8"))
        self.assertEqual(len(data["reverse_valuation_grid"]),25)
        self.assertIn("UNAVAILABLE",data["ev_status"])
        html=(ROOT/"reports"/"unitree_ic_dashboard.html").read_text("utf-8")
        self.assertIn("2026-10-26",html)
        self.assertIn("2026-08",html)
        self.assertIn("11.8",html)
        idx=(ROOT/"reports"/"ic_portfolio_overview.html").read_text("utf-8")
        self.assertIn("vrt_ic_dashboard.html",idx)
        self.assertIn("unitree_ic_dashboard.html",idx)
        with (ROOT/"data"/"unitree_evidence.csv").open(encoding="utf-8") as f:
            evidence=list(csv.DictReader(f))
        self.assertGreaterEqual(len(evidence),15)

if __name__=="__main__":
    unittest.main()

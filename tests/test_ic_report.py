"""Check that the actual issuer anchored committee reporting is reproducible."""
import csv
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from investment_lab.ic_report import generate_ic_report


class TestICReport(unittest.TestCase):
    def test_compile_and_reconcile_reports(self):
        files=generate_ic_report(ROOT)
        self.assertEqual(len(files),5)
        for file in files:
            self.assertTrue(file.is_file())
            self.assertGreater(file.stat().st_size,100)
        report=json.loads((ROOT/"reports"/"vrt_ic_decision.json").read_text(encoding="utf-8"))
        with (ROOT/"reports"/"vrt_ic_scenarios.csv").open(encoding="utf-8") as f:
            cases=list(csv.DictReader(f))
        self.assertEqual(len(cases),3)
        self.assertEqual(len(report["sensitivity"]),25)
        self.assertIn("NO NEW BUY",report["event_gate"]["initial_decision"])
        html=(ROOT/"reports"/"vrt_ic_dashboard.html").read_text(encoding="utf-8")
        self.assertIn("2026-10-28",html)
        self.assertIn("2026-10-23",html)
        self.assertIn("现金流质量",html)
        self.assertIn("VRT-20261023-CLOSE",html)
        self.assertNotIn("2026-10-28 Q3 GAAP actual",html)


if __name__=="__main__":
    unittest.main()

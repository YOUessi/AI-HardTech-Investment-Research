import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from investment_lab.report import generate


class TestReport(unittest.TestCase):
    def test_build_without_dependency(self):
        # Build into the repo's reports folder; deterministic and non-networked.
        paths = generate(ROOT)
        self.assertEqual(len(paths), 8)
        for path in paths:
            self.assertTrue(path.is_file())
            self.assertGreater(path.stat().st_size, 30)
        payload = json.loads((ROOT / "reports" / "model_results.json").read_text("utf-8"))
        self.assertEqual(payload["source_count"], 25)
        self.assertEqual(payload["comp_count"], 5)
        self.assertEqual(len(payload["models"]), 6)

    def test_reference_ledger_contains_provenance(self):
        import csv
        with (ROOT / "data" / "evidence.csv").open(encoding="utf-8") as handle:
            evidence = list(csv.DictReader(handle))
        ids = set()
        for item in evidence:
            self.assertTrue(item["id"])
            self.assertNotIn(item["id"], ids)
            ids.add(item["id"])
            self.assertTrue(item["url"].startswith("https://"))
            self.assertTrue(item["observation_period"])
            self.assertTrue(item["caveat"])
            self.assertEqual(item["checked_at"], "2026-10-27")


if __name__ == "__main__":
    unittest.main()

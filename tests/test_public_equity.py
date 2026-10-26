"""VRT IC data-lineage, formulas, and security valuation guardrail tests."""
import copy
import csv
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from investment_lab.public_equity import compute_public_case, EquityDataError

data=json.loads((ROOT/"data"/"vrt_public_equity_snapshot.json").read_text(encoding="utf-8"))


class TestIssuerAnchoredValuation(unittest.TestCase):
    def setUp(self):
        self.r=compute_public_case(data)

    def test_capital_bridge_reconciles(self):
        r=self.r
        self.assertAlmostEqual(r["share_count_m"],384.988173,places=6)
        self.assertAlmostEqual(r["market_cap_usd_m"],194.32*384.988173,places=3)
        self.assertAlmostEqual(r["net_financial_debt_m"],2939.8-2810.6-300)
        self.assertAlmostEqual(r["market_ev_usd_m"],r["market_cap_usd_m"]+r["net_financial_debt_m"],places=3)
        self.assertAlmostEqual(r["market_ev_including_operating_leases_m"]-r["market_ev_usd_m"],398.4,places=3)

    def test_reference_is_completed_october_23_close(self):
        self.assertEqual(self.r["quote_as_of"],"2026-10-23")
        self.assertEqual(self.r["reference_price_usd"],194.32)
        self.assertNotEqual(self.r["quote_as_of"],self.r["as_of"])

    def test_company_outlook_not_confused_with_real_2027(self):
        self.assertEqual(self.r["fy2026_company_guidance_sales_m"],14000)
        self.assertEqual(self.r["fy2026_company_guidance_adj_op_m"],3325)
        self.assertAlmostEqual(self.r["ev_to_guided_fy2026_adj_op_x"],
                               self.r["market_ev_usd_m"]/3325,places=3)
        self.assertGreater(self.r["ev_to_guided_fy2026_adj_op_x"],20)

    def test_growth_implies_strong_q4(self):
        self.assertAlmostEqual(self.r["h2_2026_implied_revenue_m"],14000-5923.8)
        self.assertAlmostEqual(self.r["q4_2026_revenue_implied_m"],14000-5923.8-3750,places=3)
        self.assertGreater(self.r["q4_seq_growth_from_q3_mid_pct"],15)

    def test_cashflow_quality_kept_separate_from_reported_fcf(self):
        self.assertAlmostEqual(self.r["h1_2026_reported_fcf_ex_acquisitions_m"],1866.6-285.9-2.6)
        self.assertAlmostEqual(self.r["fcf_less_deferred_revenue_wc_illustrative_m"],
                               1866.6-285.9-2.6-1822.7)
        self.assertIn("NOT normalised",self.r["cashflow_quality_warning"])

    def test_cases_reconcile_to_exit_ev_and_equity(self):
        r=self.r
        self.assertEqual([x["name"] for x in r["cases"]],["bear","base","bull"])
        for x in r["cases"]:
            self.assertAlmostEqual(x["exit_ev_m"],x["fy2027_adj_op_m"]*x["exit_ev_adj_op_x"],places=3)
            self.assertAlmostEqual(x["exit_equity_m"],x["exit_ev_m"]-r["net_financial_debt_m"],places=3)
            self.assertAlmostEqual(x["illustrative_fy2027_price_usd"]*r["share_count_m"],
                                   x["exit_equity_m"],delta=.2)

    def test_scenario_monotonic_and_mos(self):
        bear,base,bull=[x["illustrative_fy2027_price_usd"] for x in self.r["cases"]]
        self.assertLess(bear,base)
        self.assertLess(base,bull)
        self.assertLess(self.r["illustrative_max_entry_usd"],self.r["reference_price_usd"])
        self.assertAlmostEqual(self.r["illustrative_max_entry_usd"],base*0.75,places=2)

    def test_pricing_sensitivity_monotonic(self):
        grid=self.r["sensitivity"]
        self.assertEqual(len(grid),25)
        self.assertGreater(grid[-1]["illustrative_price_usd"],grid[0]["illustrative_price_usd"])

    def test_issuer_source_register(self):
        with (ROOT/"data"/"vrt_evidence.csv").open(encoding="utf-8") as file:
            facts=list(csv.DictReader(file))
        self.assertEqual(len(facts),17)
        ids={x["id"] for x in facts}
        self.assertEqual(len(ids),len(facts))
        for x in facts:
            self.assertTrue(x["source_url"].startswith("https://"))
            self.assertTrue(x["validation_status"])
        self.assertIn(data["quote"]["source"],ids)
        self.assertIn(data["capital"]["source"],ids) if data["capital"]["source"]!="VRT-2026Q2-SEC" else None

    def test_forbid_future_market_data(self):
        changed=copy.deepcopy(data);changed["quote"]["date"]="2026-10-28"
        with self.assertRaises(EquityDataError):compute_public_case(changed)

    def test_forbid_running_pre_earnings_approval_after_event(self):
        changed=copy.deepcopy(data);changed["as_of"]="2026-10-28"
        with self.assertRaises(EquityDataError):compute_public_case(changed)

    def test_forbid_margin_over_100percent(self):
        changed=copy.deepcopy(data);changed["analyst_fy2027_cases"]["base"]["adj_op_margin"]=1.3
        with self.assertRaises(EquityDataError):compute_public_case(changed)

    def test_forbid_negative_share_price(self):
        changed=copy.deepcopy(data);changed["quote"]["close_usd"]=-100
        with self.assertRaises(EquityDataError):compute_public_case(changed)

    def test_forbid_broken_guidance(self):
        changed=copy.deepcopy(data);changed["fy2026_guidance"]["sales_low_m"]=14001
        changed["fy2026_guidance"]["sales_high_m"]=14000
        with self.assertRaises(EquityDataError):compute_public_case(changed)


if __name__=="__main__":
    unittest.main()

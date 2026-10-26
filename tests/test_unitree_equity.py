"""Issuer vs synthetic hurdles: no false private-company claims or incomplete EV."""
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from investment_lab.unitree_equity import unitree_reverse_valuation, SourceDateError
data=json.loads((ROOT/"data"/"unitree_public_snapshot.json").read_text("utf-8"))


class TestUnitreeRealMarket(unittest.TestCase):
    def setUp(self): self.r=unitree_reverse_valuation(data)

    def test_public_company_and_share_reconciliation(self):
        self.assertEqual(self.r["ticker"],"688836")
        self.assertEqual(self.r["listing_date"],"2026-08-19")
        self.assertEqual(self.r["total_shares"],404464340)
        self.assertAlmostEqual(self.r["unrestricted_as_pct_total_initial"],7.4389055,places=4)
        self.assertEqual(self.r["quote_date"],"2026-10-26")

    def test_market_cap(self):
        self.assertAlmostEqual(self.r["market_cap_cny_m"],404464340*672/1e6,places=3)
        self.assertAlmostEqual(self.r["market_cap_cny_bn"],271.8,places=1)

    def test_issuer_h1_and_prior_year(self):
        self.assertEqual(self.r["fy2025_sales_cny_m"],1699.2693)
        self.assertEqual(self.r["h1_2026_revenue_cny_m"],1152.2456)
        self.assertLess(self.r["h1_2026_ex_nonrecurring_profit_yoy_pct"],0)
        self.assertLess(self.r["h1_2026_ocf_yoy_pct"],0)

    def test_trailing_pe_is_reported_not_annualized(self):
        self.assertEqual(self.r["issuer_disclosed_trailing_pe_x"],465.22)
        self.assertNotEqual(self.r["issuer_disclosed_trailing_pe_x"],
                            self.r["spot_mcap_to_mechanical_h1_annualized_net_profit_x"])

    def test_reverse_revenue_hurdle(self):
        self.assertEqual(len(self.r["reverse_valuation_grid"]),25)
        case=next(v for v in self.r["reverse_valuation_grid"]
                  if v["net_margin_pct"]==20 and v["hypothetical_forward_pe_x"]==50)
        self.assertAlmostEqual(case["required_annual_revenue_cny_m"],27180.003648,places=3)
        self.assertGreater(case["required_revenue_multiple_h1_2026_runrate"],10)

    def test_no_fabricated_ev(self):
        self.assertIn("UNAVAILABLE",self.r["ev_status"])

    def test_future_quote_disallowed(self):
        d=deepcopy(data);d["closing_date"]="2026-10-28"
        with self.assertRaises(SourceDateError):unitree_reverse_valuation(d)

    def test_inconsistent_float_disallowed(self):
        d=deepcopy(data);d["security_structure"]["unrestricted_tradeable_shares_at_listing"]=999
        with self.assertRaises(ValueError):unitree_reverse_valuation(d)

    def test_no_negative_margin(self):
        d=deepcopy(data);d["reverse_grid"]["net_profit_margin_options"]=[-0.1]
        with self.assertRaises(ValueError):unitree_reverse_valuation(d)


if __name__=="__main__": unittest.main()

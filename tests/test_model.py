"""Finance invariants: future-data hygiene is documented in research/05_methodology."""
import json
import sys
import unittest
from pathlib import Path
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from investment_lab.model import compute_infra, compute_robotics, infra_sensitivity, robotics_sensitivity

SCENARIOS = json.loads((ROOT / "data" / "scenarios.json").read_text(encoding="utf-8"))


class TestInfraModel(unittest.TestCase):
    def test_three_scenarios_five_years(self):
        for name in ("bear", "base", "bull"):
            r = compute_infra(SCENARIOS["infra"], name)
            self.assertEqual(len(r["rows"]), 5)
            self.assertEqual([x["year"] for x in r["rows"]], [2026, 2027, 2028, 2029, 2030])
            self.assertAlmostEqual(r["equity_value_m"], r["ev_m"] - 5, places=5)

    def test_revenue_uses_average_fleet_not_year_end(self):
        cfg = SCENARIOS["infra"]
        r = compute_infra(cfg, "base")
        fleet_half = cfg["cases"]["base"]["end_fleet_gpus"][0] / 2
        expected = fleet_half * 8760 * 0.69 * 2.65 / 1e6
        self.assertAlmostEqual(r["rows"][0]["revenue_m"], expected, places=5)

    def test_idle_energy_not_conflated_with_utilization(self):
        idle = compute_infra(SCENARIOS["infra"], "base", overrides={"utilization": 0})
        row = idle["rows"][0]
        self.assertEqual(row["revenue_m"], 0)
        self.assertGreater(row["power_cost_m"], 0)
        self.assertLess(row["ufcf_m"], 0)

    def test_capex_equals_growth_plus_maintenance(self):
        r = compute_infra(SCENARIOS["infra"], "base")
        for row in r["rows"]:
            self.assertAlmostEqual(
                row["capex_total_m"],
                row["capex_expansion_m"] + row["capex_maintenance_m"], places=5)

    def test_depreciation_includes_maintenance_cohorts(self):
        r = compute_infra(SCENARIOS["infra"], "base")
        for i, row in enumerate(r["rows"]):
            capex_cohorts = [x["capex_total_m"] for x in r["rows"][max(0, i-3):i+1]]
            self.assertAlmostEqual(row["depreciation_m"], sum(capex_cohorts) / 4, places=5)

    def test_cashflow_invariant(self):
        r = compute_infra(SCENARIOS["infra"], "base")
        for row in r["rows"]:
            expected = row["ebitda_m"] - row["cash_tax_m"] - row["capex_total_m"] - row["delta_wc_m"]
            self.assertAlmostEqual(row["ufcf_m"], expected, places=5)

    def test_higher_price_increases_value_otherwise_fixed(self):
        low = compute_infra(SCENARIOS["infra"], "base", overrides={"realized_usd_per_billed_gpu_hour": 1.7})
        high = compute_infra(SCENARIOS["infra"], "base", overrides={"realized_usd_per_billed_gpu_hour": 3.2})
        self.assertGreater(high["ev_m"], low["ev_m"])

    def test_invalid_util_and_fleet(self):
        with self.assertRaises(ValueError):
            compute_infra(SCENARIOS["infra"], "base", overrides={"utilization": 1.1})
        with self.assertRaises(ValueError):
            compute_infra(SCENARIOS["infra"], "base", overrides={"end_fleet_gpus": [100, 90, 120, 130, 150]})
        with self.assertRaises(ValueError):
            compute_infra(SCENARIOS["infra"], "base", overrides={"new_gpu_capex_usd": -1})
        self.assertEqual(len(infra_sensitivity(SCENARIOS["infra"])), 25)


class TestRoboticsModel(unittest.TestCase):
    def test_scenarios_and_cohorts(self):
        for name in ("bear", "base", "bull"):
            r = compute_robotics(SCENARIOS["robotics"], name)
            self.assertEqual(len(r["rows"]), 5)
            units = [x["units_sold"] for x in r["rows"]]
            self.assertEqual(r["rows"][-1]["installed_base_end"], sum(units))

    def test_service_revenue_average_installed(self):
        r = compute_robotics(SCENARIOS["robotics"], "base")["rows"][0]
        self.assertAlmostEqual(r["service_revenue_m"], (260/2)*0.38*2400/1e6, places=5)

    def test_warranty_and_gross_profit(self):
        r = compute_robotics(SCENARIOS["robotics"], "base")
        for row in r["rows"]:
            expected = row["revenue_m"] - row["hardware_cogs_m"] - row["warranty_m"] - row["service_cogs_m"]
            self.assertAlmostEqual(row["gross_profit_m"], expected, places=5)

    def test_higher_bom_reduces_value(self):
        base = SCENARIOS["robotics"]["cases"]["base"]["hardware_bom_usd"]
        expensive = [x + 8000 for x in base]
        low = compute_robotics(SCENARIOS["robotics"], "base", overrides={"hardware_bom_usd": expensive})
        high = compute_robotics(SCENARIOS["robotics"], "base")
        self.assertGreater(high["ev_m"], low["ev_m"])

    def test_service_attach_bounds(self):
        with self.assertRaises(ValueError):
            compute_robotics(SCENARIOS["robotics"], "base", overrides={"service_attach_rate": 1.2})
        self.assertEqual(len(robotics_sensitivity(SCENARIOS["robotics"])), 25)

    def test_derived_scenarios_are_not_actual_company_prices(self):
        self.assertIn("SYNTHETIC", SCENARIOS["notice"])
        self.assertEqual(SCENARIOS["as_of"], "2026-10-27")


if __name__ == "__main__":
    unittest.main()

"""Deterministic, no-third-party educational financial scenario models.

All scenario inputs are SYNTHETIC. Outputs are neither real public-company
valuations nor market-price targets. Financial unit in USD millions except
unit-economics fields; US dollars only for both illustrative companies.
"""
from __future__ import annotations
from copy import deepcopy


def _nonnegative(name, value):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a finite nonnegative number")
    if not (-float("inf") < float(value) < float("inf")):
        raise ValueError(f"{name} must be finite")


def _fraction(name, value, strict=False):
    _nonnegative(name, value)
    if value > 1 or (strict and value == 0):
        raise ValueError(f"{name} must lie in (0, 1]" if strict else f"{name} must lie in [0, 1]")


def _years(years):
    if not years or any(not isinstance(y, int) for y in years):
        raise ValueError("years must be nonempty integer years")
    if years != list(range(years[0], years[0] + len(years))):
        raise ValueError("years must be consecutive")


def _series(name, values, count, positive=False, integer=False):
    if len(values) != count:
        raise ValueError(f"{name} must have {count} entries")
    for i, value in enumerate(values):
        _nonnegative(f"{name}[{i}]", value)
        if positive and value == 0:
            raise ValueError(f"{name}[{i}] must be strictly positive")
        if integer and (not isinstance(value, int) or isinstance(value, bool)):
            raise ValueError(f"{name}[{i}] must be an integer")


def _round(v):
    return round(v, 6)


def _present_value(rows, rate, terminal):
    _fraction("discount_rate", rate, strict=True)
    future_cashflows = sum(row["ufcf_m"] / ((1 + rate) ** (i + 1)) for i, row in enumerate(rows))
    terminal_present = terminal / ((1 + rate) ** len(rows))
    return future_cashflows + terminal_present, future_cashflows, terminal_present


def compute_infra(config, scenario, overrides=None):
    """Return a synthetic GPU infrastructure operator's annual UFCF / enterprise EV.

    Deployment is assumed linear through the year; average GPU fleet generates
    utilization-based billings but consumes idle electricity all year. All annual
    capex cohorts (including maintenance) depreciate straight-line immediately
    from the year incurred. No NOL carryforwards, financing costs, salvage,
    hardware leasing, inflation, or fleet retirements (caveats in methodology).
    """
    years = config["years"]
    shared = config["shared"]
    case = deepcopy(config["cases"][scenario])
    if overrides:
        case.update(overrides)
    _years(years)
    size = len(years)
    fleet = case["end_fleet_gpus"]
    _series("end_fleet_gpus", fleet, size, integer=True)
    if any(fleet[i] < (fleet[i - 1] if i else 0) for i in range(size)):
        raise ValueError("fleet must be nondecreasing; retirement not modeled")
    _series("rnd_usd_m", shared["rnd_usd_m"], size)
    for field in ["utilization", "discount_rate"]:
        _fraction(field, case[field], strict=(field == "discount_rate"))
    for field in ["tax_rate", "sga_fraction_of_revenue", "wc_fraction_of_revenue",
                  "maintenance_capex_fraction_of_current_fleet_replacement_value"]:
        _fraction(field, shared[field])
    for field in ["realized_usd_per_billed_gpu_hour", "electricity_usd_per_kwh",
                  "new_gpu_capex_usd", "terminal_ev_to_ebitda"]:
        _nonnegative(field, case[field])
    for field in ["hours_year", "power_kw_per_gpu", "pue", "site_fixed_usd_per_avg_gpu_year",
                  "software_usd_per_billed_hour", "opening_net_debt_usd_m"]:
        _nonnegative(field, shared[field])
    if shared["pue"] < 1:
        raise ValueError("PUE must be >= 1")
    years_dep = shared["depreciation_years"]
    if not isinstance(years_dep, int) or years_dep < 1:
        raise ValueError("depreciation_years must be positive integer")
    rows, cohorts = [], []
    previous_fleet, previous_revenue = 0, 0.0
    for t, (year, ending_fleet) in enumerate(zip(years, fleet)):
        additions = ending_fleet - previous_fleet
        average_fleet = (previous_fleet + ending_fleet) / 2
        billable_hours = average_fleet * shared["hours_year"] * case["utilization"]
        revenue = billable_hours * case["realized_usd_per_billed_gpu_hour"] / 1e6
        energy_kwh = average_fleet * shared["hours_year"] * shared["power_kw_per_gpu"] * shared["pue"]
        power_cost = energy_kwh * case["electricity_usd_per_kwh"] / 1e6
        datacenter_cost = average_fleet * shared["site_fixed_usd_per_avg_gpu_year"] / 1e6
        variable_cost = billable_hours * shared["software_usd_per_billed_hour"] / 1e6
        cogs = power_cost + datacenter_cost + variable_cost
        gp = revenue - cogs
        sga = revenue * shared["sga_fraction_of_revenue"]
        rnd = shared["rnd_usd_m"][t]
        ebitda = gp - sga - rnd
        expansion_capex = additions * case["new_gpu_capex_usd"] / 1e6
        maintenance_capex = ending_fleet * case["new_gpu_capex_usd"] * shared[
            "maintenance_capex_fraction_of_current_fleet_replacement_value"] / 1e6
        capex = expansion_capex + maintenance_capex
        cohorts.append((t, capex))
        depreciation = sum(v / years_dep for start, v in cohorts if t - start < years_dep)
        ebit = ebitda - depreciation
        cash_tax = max(0.0, ebit) * shared["tax_rate"]
        delta_wc = (revenue - previous_revenue) * shared["wc_fraction_of_revenue"]
        ufcf = ebitda - cash_tax - capex - delta_wc
        rows.append({
            "year": year, "fleet_end_gpus": ending_fleet, "fleet_average_gpus": _round(average_fleet),
            "billed_gpu_hours": _round(billable_hours), "revenue_m": _round(revenue),
            "power_cost_m": _round(power_cost), "site_cost_m": _round(datacenter_cost),
            "software_variable_cost_m": _round(variable_cost), "cogs_m": _round(cogs),
            "gross_profit_m": _round(gp), "gross_margin_pct": _round(100 * gp / revenue) if revenue > 0 else None,
            "sga_m": _round(sga), "rnd_m": _round(rnd), "ebitda_m": _round(ebitda),
            "capex_expansion_m": _round(expansion_capex), "capex_maintenance_m": _round(maintenance_capex),
            "capex_total_m": _round(capex), "depreciation_m": _round(depreciation),
            "ebit_m": _round(ebit), "cash_tax_m": _round(cash_tax),
            "delta_wc_m": _round(delta_wc), "ufcf_m": _round(ufcf)
        })
        previous_fleet, previous_revenue = ending_fleet, revenue
    terminal = max(0.0, rows[-1]["ebitda_m"]) * case["terminal_ev_to_ebitda"]
    ev, pv_cashflows, pv_terminal = _present_value(rows, case["discount_rate"], terminal)
    return {"sector": "inference_infra", "case": scenario, "years": years, "rows": rows,
            "ev_m": _round(ev), "equity_value_m": _round(ev - shared["opening_net_debt_usd_m"]),
            "terminal_value_m": _round(terminal), "pv_cashflows_m": _round(pv_cashflows),
            "pv_terminal_m": _round(pv_terminal), "exit_metric": "terminal EBITDA x illustrative EV/EBITDA",
            "scenario_inputs": case}


def compute_robotics(config, scenario, overrides=None):
    """Illustrative *fictional* robotics OEM + optional recurring services.

    Service subscribers are a fraction of the AVERAGE active installed base;
    assumes zero fleet attrition (optimistic). Hardware warranty reserve is
    expensed in the same year, capex uses a simplified straight-line schedule.
    Exit proxy is explicit EV/revenue, not a listed-company trading multiple.
    """
    years = config["years"]
    shared = config["shared"]
    case = deepcopy(config["cases"][scenario])
    if overrides:
        case.update(overrides)
    _years(years)
    n = len(years)
    for f in ("units_sold", "hardware_asp_usd", "hardware_bom_usd"):
        _series(f, case[f], n, integer=(f == "units_sold"))
    for f in ("rnd_usd_m", "capex_usd_m"):
        _series(f, shared[f], n)
    for f in ("service_attach_rate", "discount_rate"):
        _fraction(f, case[f], strict=(f == "discount_rate"))
    for f in ("service_gross_margin", "warranty_fraction_of_hardware_revenue",
              "sga_fraction_of_revenue", "wc_fraction_of_revenue", "tax_rate"):
        _fraction(f, shared[f])
    for f in ("service_revenue_usd_per_active_attached_unit_year",
              "opening_net_debt_usd_m"):
        _nonnegative(f, shared[f])
    _nonnegative("terminal_ev_to_revenue", case["terminal_ev_to_revenue"])
    dep_years = shared["depreciation_years"]
    if not isinstance(dep_years, int) or dep_years < 1:
        raise ValueError("depreciation_years must be positive integer")
    rows, cohorts = [], []
    installed, prev_revenue = 0, 0.0
    for i, year in enumerate(years):
        units = case["units_sold"][i]
        average_active = installed + units / 2
        subscribers = average_active * case["service_attach_rate"]
        hardware_revenue = units * case["hardware_asp_usd"][i] / 1e6
        hardware_cogs = units * case["hardware_bom_usd"][i] / 1e6
        warranty_cost = hardware_revenue * shared["warranty_fraction_of_hardware_revenue"]
        service_revenue = subscribers * shared["service_revenue_usd_per_active_attached_unit_year"] / 1e6
        service_cogs = service_revenue * (1 - shared["service_gross_margin"])
        revenue = hardware_revenue + service_revenue
        cogs = hardware_cogs + warranty_cost + service_cogs
        gp = revenue - cogs
        sga = revenue * shared["sga_fraction_of_revenue"]
        rnd = shared["rnd_usd_m"][i]
        ebitda = gp - sga - rnd
        capex = shared["capex_usd_m"][i]
        cohorts.append((i, capex))
        depreciation = sum(v / dep_years for start, v in cohorts if i - start < dep_years)
        ebit = ebitda - depreciation
        cash_tax = max(0, ebit) * shared["tax_rate"]
        wc_change = (revenue - prev_revenue) * shared["wc_fraction_of_revenue"]
        ufcf = ebitda - cash_tax - capex - wc_change
        installed += units
        rows.append({
            "year": year, "units_sold": units, "installed_base_end": installed,
            "average_active_fleet": _round(average_active), "attached_services": _round(subscribers),
            "hardware_revenue_m": _round(hardware_revenue), "service_revenue_m": _round(service_revenue),
            "revenue_m": _round(revenue), "hardware_cogs_m": _round(hardware_cogs),
            "warranty_m": _round(warranty_cost), "service_cogs_m": _round(service_cogs),
            "cogs_m": _round(cogs), "gross_profit_m": _round(gp),
            "gross_margin_pct": _round(100 * gp / revenue) if revenue > 0 else None,
            "sga_m": _round(sga), "rnd_m": _round(rnd), "ebitda_m": _round(ebitda),
            "capex_total_m": _round(capex), "depreciation_m": _round(depreciation),
            "ebit_m": _round(ebit), "cash_tax_m": _round(cash_tax),
            "delta_wc_m": _round(wc_change), "ufcf_m": _round(ufcf)
        })
        prev_revenue = revenue
    terminal = max(0.0, rows[-1]["revenue_m"]) * case["terminal_ev_to_revenue"]
    ev, pv_cashflows, pv_terminal = _present_value(rows, case["discount_rate"], terminal)
    return {"sector": "humanoid_robotics", "case": scenario, "years": years, "rows": rows,
            "ev_m": _round(ev), "equity_value_m": _round(ev - shared["opening_net_debt_usd_m"]),
            "terminal_value_m": _round(terminal), "pv_cashflows_m": _round(pv_cashflows),
            "pv_terminal_m": _round(pv_terminal), "exit_metric": "terminal revenue x synthetic EV/revenue",
            "scenario_inputs": case}


def infra_sensitivity(config):
    """Price x utilization sensitivity of BASE infra equity value, other inputs fixed."""
    base = config["cases"]["base"]
    matrix = []
    for util_change in [-0.15, -0.075, 0.0, 0.075, 0.15]:
        for price_multiplier in [0.75, 0.875, 1.0, 1.125, 1.25]:
            util = base["utilization"] + util_change
            if not (0 <= util <= 1):
                continue
            scenario = compute_infra(config, "base", overrides={
                "utilization": util, "realized_usd_per_billed_gpu_hour":
                base["realized_usd_per_billed_gpu_hour"] * price_multiplier})
            matrix.append({"utilization": _round(util), "price_multiplier": price_multiplier,
                           "equity_value_usd_m": scenario["equity_value_m"]})
    return matrix


def robotics_sensitivity(config):
    """Hardware ASP x service attach sensitivity of BASE robotics equity value."""
    base = config["cases"]["base"]
    matrix = []
    for attach_change in [-0.20, -0.10, 0, 0.10, 0.20]:
        for asp_multiplier in [0.80, 0.90, 1.0, 1.10, 1.20]:
            attach = base["service_attach_rate"] + attach_change
            if not 0 <= attach <= 1:
                continue
            result = compute_robotics(config, "base", overrides={
                "service_attach_rate": attach,
                "hardware_asp_usd": [asp * asp_multiplier for asp in base["hardware_asp_usd"]]})
            matrix.append({"service_attach_rate": _round(attach),
                           "asp_multiplier": asp_multiplier,
                           "equity_value_usd_m": result["equity_value_m"]})
    return matrix

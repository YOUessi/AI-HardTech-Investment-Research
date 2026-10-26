"""Issuer-anchored Vertiv (VRT) public-market IC module. All 2027 cases ANALYST assumptions."""
from __future__ import annotations
from pathlib import Path
import json
import math


class EquityDataError(ValueError):
    pass


def number(value, label, strictly_positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise EquityDataError(f"{label}: finite numeric value required")
    if strictly_positive and value <= 0:
        raise EquityDataError(f"{label}: must be > 0")
    return float(value)


def pct(value, label):
    value = number(value, label)
    if not 0 <= value <= 1:
        raise EquityDataError(f"{label}: fraction must be 0..1")
    return value


def midpoint(low, high):
    low, high = number(low, "low"), number(high, "high")
    if high < low:
        raise EquityDataError("min > max")
    return (low + high) / 2


def compute_public_case(data):
    """Valuation USD millions, share-price USD. No APIs, no security trading."""
    date = data["as_of"]
    if (data["quote"]["date"] > date or
        data["capital"]["balance_date"] > date or
        data["capital"]["shares_date"] > date):
        raise EquityDataError("forward-dated observation")
    if data["ic_policy"]["event_date"] <= date:
        raise EquityDataError("event has arrived: update point-in-time snapshot")
    cap, historic, guidance = data["capital"], data["historic"], data["fy2026_guidance"]
    price = number(data["quote"]["close_usd"], "reference price", True)
    shares_m = number(cap["shares"], "shares", True) / 1e6
    gross_financial_debt = number(cap["current_financial_debt_m"], "short debt")+number(cap["long_financial_debt_m"], "long debt")
    cash_like = number(cap["cash_m"], "cash")+number(cap["short_investments_m"], "ST investments")
    net_debt = gross_financial_debt - cash_like
    lease_liabilities = cap["current_operating_leases_m"] + cap["long_operating_leases_m"]
    market_cap = price * shares_m
    ev = market_cap + net_debt
    sales_26 = midpoint(guidance["sales_low_m"], guidance["sales_high_m"])
    op_26 = midpoint(guidance["adjusted_op_low_m"], guidance["adjusted_op_high_m"])
    fcf_26 = midpoint(guidance["adjusted_fcf_low_m"], guidance["adjusted_fcf_high_m"])
    eps_26 = midpoint(guidance["adjusted_eps_low"], guidance["adjusted_eps_high"])
    q3_guidance = midpoint(guidance["q3_sales_low_m"], guidance["q3_sales_high_m"])
    if min(sales_26, op_26, fcf_26, eps_26, q3_guidance) <= 0 or ev <= 0:
        raise EquityDataError("unusable company guidance / market EV")
    annual_fcf_observed = historic["h1_ocf_m"]-historic["h1_capex_m"]-historic["h1_capitalized_software_m"]
    # Not a normalized FCF: only an illustration of sensitivity to a single cash inflow item.
    if historic["h1_delta_deferred_revenue_m"] < 0:
        raise EquityDataError("Expected positive deferred-revenue movement in observed audit")
    fcf_ex_deferred_illustration = annual_fcf_observed-historic["h1_delta_deferred_revenue_m"]
    q4_required = sales_26-historic["h1_revenue_m"]-q3_guidance
    if q4_required <= 0:
        raise EquityDataError("Q4 implied nonpositive")
    scenarios=[]
    for label in ("bear","base","bull"):
        s=data["analyst_fy2027_cases"][label]
        revenue=number(s["revenue_m"], "scenario revenue", True)
        margin=pct(s["adj_op_margin"], "scenario margin")
        exit_mult=number(s["exit_ev_adj_op_x"], "exit multiple", True)
        op=revenue*margin
        exit_ev=op*exit_mult
        exit_equity=exit_ev-net_debt
        value_per_share=exit_equity/shares_m
        scenarios.append({
            "name":label,"fy2027_revenue_m":round(revenue,3),
            "growth_v_2026_mid_pct":round((revenue/sales_26-1)*100,3),
            "adj_op_margin_pct":round(margin*100,3),
            "fy2027_adj_op_m":round(op,3),
            "exit_ev_adj_op_x":round(exit_mult,3),
            "exit_ev_m":round(exit_ev,3),
            "exit_equity_m":round(exit_equity,3),
            "illustrative_fy2027_price_usd":round(value_per_share,3),
            "price_change_from_reference_pct":round((value_per_share/price-1)*100,3)})
    entry=scenarios[1]["illustrative_fy2027_price_usd"]*(1-pct(data["ic_policy"]["margin_of_safety"],"MOS"))
    loss_if_bear=max(0.0, (entry-scenarios[0]["illustrative_fy2027_price_usd"])/entry)
    max_weight=pct(data["ic_policy"]["max_post_gate_weight_nav"],"max weight")
    risk_budget=pct(data["ic_policy"]["max_downside_nav_budget"],"risk budget")
    allowed_weight=min(max_weight, risk_budget/loss_if_bear) if loss_if_bear>0 else max_weight
    grid=[]
    for margin in (0.205,0.225,0.245,0.265,0.285):
        for mult in (14,18,21,24,28):
            projected_ev=data["analyst_fy2027_cases"]["base"]["revenue_m"]*margin*mult
            grid.append({"operating_margin_pct":round(margin*100,3),"ev_adj_op_x":mult,
                         "illustrative_price_usd":round((projected_ev-net_debt)/shares_m,3)})
    return {
        "ticker":"VRT","as_of":date,"quote_as_of":data["quote"]["date"],
        "reference_price_usd":price,"share_count_m":round(shares_m,6),
        "market_cap_usd_m":round(market_cap,3),
        "gross_financial_debt_m":round(gross_financial_debt,3),
        "cash_and_st_investments_m":round(cash_like,3),
        "net_financial_debt_m":round(net_debt,3),
        "market_ev_usd_m":round(ev,3),
        "market_ev_including_operating_leases_m":round(ev+lease_liabilities,3),
        "operating_lease_liabilities_m":round(lease_liabilities,3),
        "fy2026_company_guidance_sales_m":sales_26,
        "fy2026_company_guidance_adj_op_m":op_26,
        "fy2026_company_guidance_adj_fcf_m":fcf_26,
        "fy2026_company_guidance_adj_eps":eps_26,
        "ev_to_guided_fy2026_adj_op_x":round(ev/op_26,3),
        "ev_to_guided_fy2026_sales_x":round(ev/sales_26,3),
        "market_cap_to_guided_fy2026_adj_fcf_x":round(market_cap/fcf_26,3),
        "share_price_to_guided_fy2026_adj_eps_x":round(price/eps_26,3),
        "h1_2026_observed_ocf_m":historic["h1_ocf_m"],
        "h1_2026_reported_fcf_ex_acquisitions_m":round(annual_fcf_observed,3),
        "h1_2026_deferred_revenue_wc_uplift_m":historic["h1_delta_deferred_revenue_m"],
        "fcf_less_deferred_revenue_wc_illustrative_m":round(fcf_ex_deferred_illustration,3),
        "cashflow_quality_warning":"Single deferred-revenue adjustment is only a stress diagnostic, NOT normalised GAAP FCF; other WC and operating components are not normalized.",
        "h2_2026_implied_revenue_m":round(sales_26-historic["h1_revenue_m"],3),
        "q3_2026_sales_guidance_mid_m":q3_guidance,
        "q4_2026_revenue_implied_m":round(q4_required,3),
        "q4_seq_growth_from_q3_mid_pct":round((q4_required/q3_guidance-1)*100,3),
        "cases":scenarios,
        "sensitivity":grid,
        "illustrative_max_entry_usd":round(entry,3),
        "reference_above_entry_gate":price>entry,
        "illustrative_risk_based_post_gate_weight_pct_nav":round(allowed_weight*100,3),
        "illustrative_bear_drawdown_from_entry_pct":round(loss_if_bear*100,3),
        "event_gate":data["ic_policy"],"model_limits":data["model_limits"]}


def load_and_compute(root):
    path=Path(root)/"data"/"vrt_public_equity_snapshot.json"
    return compute_public_case(json.loads(path.read_text(encoding="utf-8")))

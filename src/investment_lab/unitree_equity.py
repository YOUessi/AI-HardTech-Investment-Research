"""Real listed Unitree 688836 public-market reverse-valuation hurdle.

Issuer 2025 IPO audited and 2026 H1 unaudited financials. No forecast is
presented as actual, no made-up balance sheet or fictitious net debt.
"""
from __future__ import annotations
import json
import math
from pathlib import Path


class SourceDateError(ValueError):
    pass


def validate(x, name):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<=0:
        raise ValueError(f"{name}: expected finite positive number")
    return float(x)


def unitree_reverse_valuation(snapshot):
    today=snapshot["as_of"]
    for date in (snapshot["closing_date"],snapshot["listing_date"],
                 snapshot["issuer_risk"]["published_date"]):
        if date>today:
            raise SourceDateError("Future event/quote in point-in-time data")
    close=validate(snapshot["close_cny"],"close")
    s=snapshot["security_structure"]
    shares=validate(s["total_ordinary_shares"],"issued shares")
    available=validate(s["unrestricted_tradeable_shares_at_listing"],"initial unrestricted")
    restricted=validate(s["restricted_shares_at_listing"],"initial restricted")
    if int(available+restricted)!=int(shares):
        raise ValueError("Listable share structure doesn't reconcile")
    f=snapshot["financials"]
    h=f["h1_2026"]
    y=f["fy2025"]
    for label in ("revenue_cny_m","attributable_profit_cny_m",
                  "ex_nonrecurring_profit_cny_m","operating_cashflow_cny_m"):
        validate(h[label],f"H1 {label}")
    annualized_h1_sales=h["revenue_cny_m"]*2
    annualized_h1_profit=h["attributable_profit_cny_m"]*2
    annualized_h1_ex_profit=h["ex_nonrecurring_profit_cny_m"]*2
    marketcap_cny_m=shares*close/1e6
    gross_ipo_issue_proceeds=snapshot["issue_price_cny"]*(shares/10)/1e6
    grid=[]
    for margin in snapshot["reverse_grid"]["net_profit_margin_options"]:
        if not 0<margin<1: raise ValueError("reverse net margin range invalid")
        for pe in snapshot["reverse_grid"]["exit_pe_options"]:
            validate(pe,"exit P/E")
            required_profit=marketcap_cny_m/pe
            required_sales=required_profit/margin
            grid.append({
                "net_margin_pct":round(margin*100,2),
                "hypothetical_forward_pe_x":pe,
                "required_annual_profit_cny_m":round(required_profit,4),
                "required_annual_revenue_cny_m":round(required_sales,4),
                "required_revenue_multiple_h1_2026_runrate":round(required_sales/annualized_h1_sales,4),
                "required_revenue_multiple_fy2025":round(required_sales/y["revenue_cny_m"],4)
            })
    def r(x): return round(x,4)
    return {
      "as_of":today,"ticker":"688836","listing_date":snapshot["listing_date"],
      "quote_date":snapshot["closing_date"],"reference_close_cny":close,
      "total_shares":int(shares),"listed_initial_unrestricted_shares":int(available),
      "unrestricted_as_pct_total_initial":r(100*available/shares),
      "market_cap_cny_m":r(marketcap_cny_m),
      "market_cap_cny_bn":r(marketcap_cny_m/1000),
      "issue_price_cny":snapshot["issue_price_cny"],
      "ipo_gross_proceeds_cny_m_illustrative":r(gross_ipo_issue_proceeds),
      "fy2025_sales_cny_m":y["revenue_cny_m"],
      "fy2025_attributable_profit_cny_m":y["attributable_profit_cny_m"],
      "fy2025_humanoid_segment_sales_cny_m":y["humanoid_revenue_cny_m"],
      "fy2025_humanoid_sales_pct_of_total":r(100*y["humanoid_revenue_cny_m"]/y["revenue_cny_m"]),
      "fy2025_humanoid_units_sold":y["humanoid_units_sold"],
      "h1_2026_revenue_cny_m":h["revenue_cny_m"],
      "h1_2026_attributable_profit_cny_m":h["attributable_profit_cny_m"],
      "h1_2026_ex_nonrecurring_profit_cny_m":h["ex_nonrecurring_profit_cny_m"],
      "h1_2026_yoy_revenue_pct":r(100*(h["revenue_cny_m"]/h["revenue_h1_2025_cny_m"]-1)),
      "h1_2026_ex_nonrecurring_profit_yoy_pct":r(100*(h["ex_nonrecurring_profit_cny_m"]/h["ex_nonrecurring_profit_h1_2025_cny_m"]-1)),
      "h1_2026_ocf_cny_m":h["operating_cashflow_cny_m"],
      "h1_2026_ocf_yoy_pct":r(100*(h["operating_cashflow_cny_m"]/h["operating_cashflow_h1_2025_cny_m"]-1)),
      "h1_annualized_2026_revenue_cny_m_mechanical":r(annualized_h1_sales),
      "spot_mcap_to_mechanical_h1_annualized_sales_x":r(marketcap_cny_m/annualized_h1_sales),
      "spot_mcap_to_mechanical_h1_annualized_net_profit_x":r(marketcap_cny_m/annualized_h1_profit),
      "spot_mcap_to_mechanical_h1_annualized_ex_net_profit_x":r(marketcap_cny_m/annualized_h1_ex_profit),
      "spot_mcap_to_fy2025_reported_sales_x":r(marketcap_cny_m/y["revenue_cny_m"]),
      "spot_mcap_to_fy2025_reported_net_profit_x":r(marketcap_cny_m/y["attributable_profit_cny_m"]),
      "issuer_disclosed_trailing_pe_x":snapshot["issuer_risk"]["trailing_pe_at_oct26"],
      "issuer_disclosed_industry_trailing_pe_x":snapshot["issuer_risk"]["industry_trailing_pe_at_oct26"],
      "issuer_trailing_pe_to_industry_ratio":r(snapshot["issuer_risk"]["trailing_pe_at_oct26"]/
                                          snapshot["issuer_risk"]["industry_trailing_pe_at_oct26"]),
      "reverse_valuation_grid":grid,
      "decision":snapshot["policy"]["decision"],
      "decision_reason":snapshot["policy"]["reason"],
      "gates":snapshot["policy"]["gates"],
      "limitations":snapshot["policy"]["limits"],
      "ev_status":"UNAVAILABLE: Post-IPO company cash/debt, restricted cash, leases and other adjustments not verified at a common balance date; do not present price/book/synthetic EV as audited enterprise value."
    }


def load_and_compute(root):
    return unitree_reverse_valuation(json.loads((Path(root)/"data"/"unitree_public_snapshot.json").read_text(encoding="utf-8")))

"""Build reproducible CSV, JSON, markdown, and offline HTML research dashboard."""
from pathlib import Path
import csv
import html
import json
from .model import compute_infra, compute_robotics, infra_sensitivity, robotics_sensitivity


def _e(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def _money(value):
    return ("-" if value < 0 else "") + "$" + format(abs(value), ",.2f") + "m"


def _write_csv(path, rows, fields=None):
    rows = list(rows)
    if not fields:
        if not rows:
            return
        fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _table(headers, rows):
    head = "".join("<th scope='col'>" + _e(h) + "</th>" for h in headers)
    content = "".join("<tr>" + "".join("<td>" + str(cell) + "</td>" for cell in row) + "</tr>" for row in rows)
    return "<div class='tablewrap'><table><thead><tr>" + head + "</tr></thead><tbody>" + content + "</tbody></table></div>"


def _heatmap(rows, rkey, ckey):
    xs = sorted({x[ckey] for x in rows})
    ys = sorted({x[rkey] for x in rows})
    cells = {(x[rkey], x[ckey]): x["equity_value_usd_m"] for x in rows}
    all_vals = list(cells.values())
    lo, hi = min(all_vals), max(all_vals)
    def color(v):
        t = (v - lo) / max(hi - lo, 0.001)
        return "hsl(" + str(int(10 + 135*t)) + ", 49%, 89%)"
    tbl = []
    for y in ys:
        line = [_e(format(y, ".3f"))]
        for x in xs:
            v = cells.get((y, x))
            line.append("-" if v is None else "<span class='heat' style='background:" +
                        color(v) + "'>" + _e(format(v, ",.1f")) + "</span>")
        tbl.append(line)
    return _table([rkey + " / " + ckey] + [format(v, ".3f") for v in xs], tbl)


def _write_html(path, projections, sources, comps, sensitivity_infra, sensitivity_robot, config):
    cases = [p for p in projections if p["case"] in ("bear", "base", "bull")]
    metas = {
        "inference_infra": ("GPU INFRASTRUCTURE", "Average fleet billings · idle-power-aware cash flows"),
        "humanoid_robotics": ("HUMANOID ROBOTICS", "Hardware + attached service revenue · synthetic units")
    }
    cards, sections = [], []
    for sector, (title, expl) in metas.items():
        sector_models = [p for p in cases if p["sector"] == sector]
        for p in sector_models:
            terminal_share = (p["pv_terminal_m"] / p["ev_m"] * 100) if p["ev_m"] > 0 else None
            cards.append(
                "<div class='case'><div class='case-head'><span>" + _e(title) +
                "</span><b class='pill " + _e(p["case"]) + "'>" + _e(p["case"].upper()) +
                "</b></div><strong>" + _money(p["ev_m"]) +
                "</strong><small>Enterprise Value · synthetic, USD millions</small><p>Equity " +
                _money(p["equity_value_m"]) + " · FY2030 revenue " +
                _money(p["rows"][-1]["revenue_m"]) + "</p><p>Terminal PV as % of EV: " +
                (_e(format(terminal_share, ".1f") + "%") if terminal_share is not None else "n/a") + "</p></div>"
            )
        rows = []
        for p in sector_models:
            for item in p["rows"]:
                rows.append([
                    "<b>" + _e(p["case"].upper()) + "</b>", _e(item["year"]),
                    _money(item["revenue_m"]), _money(item["ebitda_m"]),
                    _money(item["capex_total_m"]), _money(item["ufcf_m"]),
                    ("<span class='negative'>" + _e(format(item["gross_margin_pct"], ".1f")) +
                     "%</span>" if item["gross_margin_pct"] is not None and item["gross_margin_pct"] < 0
                     else (str(item["gross_margin_pct"]) + "%" if item["gross_margin_pct"] is not None else "n/a"))
                ])
        sections.append("<section><div class='heading'><div><span class='eyebrow'>" + _e(title) +
                        "</span><h2>" + _e(expl) + "</h2></div></div>" +
                        _table(["Case", "Year", "Revenue", "EBITDA", "Capex", "Unlevered FCF", "Gross margin"], rows) +
                        "</section>")
    observations = []
    key_ids = {"IEA-DC-2025", "IEA-DC-2030", "NV-FY27-Q2-REV", "AMD-2026Q2-REV",
               "VRT-2026Q2-SALES", "CW-2026Q2-REV", "UBT-H1-REV",
               "UBT-H1-HUM", "IFR-2025-HUM", "CP-2026H1-HUM",
               "UNITREE-G1-PRICE", "UNITREE-R1-PRICE"}
    for row in sources:
        if row["id"] not in key_ids:
            continue
        observations.append([
            "<b>" + _e(row["entity"]) + "</b>", _e(row["observation_period"]),
            _e(row["metric"]), "<b>" + _e(row["value"]) + " " + _e(row["unit"]) + "</b>",
            "<a target='_blank' rel='noopener noreferrer' href='" + _e(row["url"]) + "'>" + _e(row["id"]) + " ↗</a>",
            _e(row["caveat"])
        ])
    comparison = []
    for c in comps:
        rev = float(c["revenue_m"])
        op = float(c["gaap_operating_income_m"])
        comparison.append([
            "<b>" + _e(c["company"]) + "</b>", _e(c["period"]),
            _e(c["currency"]), _e(format(rev, ",.1f")),
            _e(format(op, ",.1f")), _e(format(op/rev*100, ".1f") + "%"),
            _e(c["gaap_gross_margin_percent"] or "n/a"), _e(c["comparison_warning"])
        ])
    styles = """
    :root{--paper:#fff;--bg:#f4f7fa;--ink:#1c3145;--muted:#63798e;--line:#dde5ec}
    *{box-sizing:border-box} body{margin:0;font:13px/1.7 -apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif;background:var(--bg);color:var(--ink)}
    .shell{max-width:1430px;margin:auto;padding:0 26px}
    header{background:radial-gradient(circle at 100% 0%,#326990 0,transparent 40%),linear-gradient(120deg,#10283c,#1c405d);padding:45px 0 72px;color:#fff}
    header .eyebrow{color:#97c9f0} h1{font-size:clamp(29px,3.7vw,47px);letter-spacing:-.035em;margin:11px 0}header p{max-width:930px;color:#bbcedd;margin:0;font-size:14px}
    nav{display:flex;gap:9px;flex-wrap:wrap;margin-top:21px}nav a{color:#e5f2fd;background:#ffffff15;border:1px solid #ffffff22;padding:5px 11px;border-radius:18px;font-size:12px;text-decoration:none}
    .warning{margin:-30px auto 22px;position:relative;padding:15px 17px;background:#fff6e7;border:1px solid #f1d9a6;border-radius:12px;color:#98611d;box-shadow:0 3px 9px #0000000b}
    .overview{display:grid;grid-template-columns:repeat(3,1fr);gap:13px}
    .case{border:1px solid var(--line);background:var(--paper);padding:17px;border-radius:13px;box-shadow:0 4px 19px #1234560a}
    .case-head{display:flex;justify-content:space-between;align-items:center;color:#526c81;font-weight:700;font-size:11px;letter-spacing:.065em}
    .case strong{font-size:27px;display:block;margin:12px 0 3px;color:#173e5d}
    .case small{color:#8ba0b1}.case p{color:#6b8193;font-size:11.5px;margin:9px 0 0}
    .pill{font-size:10px;padding:3px 8px;border-radius:12px}.bear{background:#fce8e4;color:#a05243}.base{background:#e2eefb;color:#2764a0}.bull{background:#e1f6ec;color:#127f55}
    section{margin:33px 0 35px}.heading{display:flex;justify-content:space-between;align-items:end;margin:0 0 13px}
    .eyebrow{font-weight:800;letter-spacing:.11em;font-size:10px;color:#43749e}h2{font-size:21px;line-height:1.35;margin:5px 0 0}
    .tablewrap{width:100%;overflow:auto;border:1px solid #dde5ed;border-radius:12px;background:white}
    table{border-collapse:collapse;width:100%;min-width:780px}thead{background:#f0f5f9}th{text-align:left;color:#49647e;font-size:11px;letter-spacing:.01em;white-space:nowrap}
    th,td{padding:10px 12px;border-bottom:1px solid #edf1f5;vertical-align:top}
    tbody tr:last-child td{border-bottom:0}tbody tr:hover{background:#fbfdff}
    .negative{color:#a75143} .heat{display:block;text-align:center;padding:7px 9px;border-radius:6px;min-width:70px;font-variant-numeric:tabular-nums}
    .split{display:grid;grid-template-columns:1fr 1fr;gap:18px}.note{background:#fff;border:1px solid #e0e8ee;border-radius:12px;padding:14px 18px;color:#557084}
    .note h3{margin:0 0 6px;font-size:14px;color:#1d4565}.note p{margin:6px 0}
    .tail{padding:28px 0 65px;color:#72899c}.tail a{color:#256b9f}a{color:#1869a4}
    @media(max-width:900px){.overview{grid-template-columns:repeat(2,1fr)}.split{grid-template-columns:1fr}.shell{padding:0 14px}}
    @media(max-width:570px){.overview{grid-template-columns:1fr}header{padding:30px 0 52px}}
    @media print{.overview{display:block}.case{break-inside:avoid;margin:5px}.tablewrap{overflow:visible}table{min-width:0}th,td{padding:4px;font-size:9px}section{break-inside:avoid}}
    """
    body = """
    <!doctype html><html lang="en"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI & Hard-Tech Investment Diligence | Reproducible Scenarios</title>
    <style>""" + styles + """</style></head><body>
    <header><div class="shell"><div class="eyebrow">RESEARCH NOTE / 2026-10-27 / EDUCATIONAL</div>
    <h1>Where can AI & Hard-Tech value accrue?</h1>
    <p>Evidence-led comparison of inference compute economics and humanoid-robotics adoption. Reproducible, fictional scenarios; public-company facts are separately sourced, not turned into price targets.</p>
    <nav><a href="#models">Scenario model</a><a href="#financials">Public-company anchors</a><a href="#sensitivity">Sensitivity</a><a href="#evidence">Source ledger</a></nav>
    </div></header><main class="shell">
    <div class="warning"><b>⚠ MODEL DISCLAIMER</b> — All six company valuations shown below are synthetic teaching scenarios for two <b>fictional</b> business models. No public equity target price, IPO valuation, live quote, verified private cap table, debt schedule or investment action is implied. Figures are in USD millions unless noted.</div>
    <section id="models"><div class="heading"><div><span class="eyebrow">01 / CASE ANALYSIS</span><h2>Two business models · Three cases each</h2></div></div><div class="overview">""" + "".join(cards) + """</div></section>""" + "".join(sections) + """
    <section id="financials"><div class="heading"><div><span class="eyebrow">02 / PRIMARY FILINGS</span><h2>Public comparables: not economic substitutes</h2></div></div>
    <div class="note"><p>NVIDIA/AMD are chip vendors; Vertiv supplies cooling and power infrastructure; CoreWeave leases/runs GPU capacity; UBTECH sells robotics products and services. Different business models, quarters, currencies and accounting classifications make direct EV/revenue or headline gross-margin comparison inappropriate.</p></div>""" + _table(
        ["Company", "Reported period", "CCY", "Revenue m", "GAAP op. income m", "GAAP op. margin", "Gross margin %", "Warning"],
        comparison
    ) + """</section>
    <section id="sensitivity"><div class="heading"><div><span class="eyebrow">03 / KEY VALUE DRIVERS</span><h2>Base-case sensitivity · synthetic equity value, USD m</h2></div></div><div class="split">
    <div><h3>Inference: billed-hour price × utilization</h3>""" + _heatmap(sensitivity_infra, "utilization", "price_multiplier") + """</div>
    <div><h3>Robotics: service attach × hardware ASP</h3>""" + _heatmap(sensitivity_robot, "service_attach_rate", "asp_multiplier") + """</div></div>
    <p class="note">Only the selected two drivers change. Fleet sizes, operating cost schedule, discount rate and exit multiples remain at base assumptions. Color scales are relative within each matrix, not a probability distribution.</p>
    </section><section id="evidence"><div class="heading"><div><span class="eyebrow">04 / DOCUMENTED ANCHORS</span><h2>Observed metrics and dated research</h2></div></div>""" + _table(
        ["Entity", "Observation period", "Metric", "Value", "Primary/near-primary source", "Caveat"],
        observations
    ) + """</section>
    <div class="note"><h3>Key model restrictions</h3><p>Compute: linear within-year fleet ramp, idle electricity, depreciation on growth/maintenance capex, no NOL or financing-interest schedule, terminal EV/EBITDA heuristic. Robotics: average active installed base, no attrition, explicit hardware warranty and BOM, terminal EV/revenue heuristic. The models are not audited financial forecasts.</p>
    <p>Detailed source IDs are in data/evidence.csv; assumptions in data/scenarios.json; all formula and modeling caveats are in research/05_methodology.md.</p>
    </div></main><footer class="shell tail">Offline HTML generated using Python's standard library. · <a href="https://github.com/YOUessi/AI-HardTech-Investment-Research">Research repository</a> · As of 2026-10-27</footer></body></html>"""
    path.write_text(body, encoding="utf-8")


def _write_summary_md(path, outputs, sensitivities):
    lines = [
        "# Investment scenario snapshot",
        "",
        "**All results synthetic and illustrative** (USD millions; as-of 2026-10-27).",
        "These are enterprise and equity values for fictional business cases, not price targets.",
        "",
        "| Sector | Case | FY2030 revenue | FY2030 EBITDA | EV | Equity | PV of terminal |",
        "|---|---:|---:|---:|---:|---:|---:|"
    ]
    for x in outputs:
        row = x["rows"][-1]
        lines.append("| " + x["sector"] + " | " + x["case"] + " | " +
                     " | ".join(format(v, ".2f") for v in [
                         row["revenue_m"], row["ebitda_m"], x["ev_m"],
                         x["equity_value_m"], x["pv_terminal_m"]]) + " |")
    lines += [
        "",
        "## Interpret carefully",
        "",
        "- Infra exit value is modeled as terminal-year positive EBITDA × an ASSUMED EV/EBITDA multiple.",
        "- Robotics exit value is terminal-year revenue × an ASSUMED EV/Revenue multiple.",
        "- These cross-sector equity values are not directly comparable investment opportunities.",
        "- Installed GPU cost and utilization, robot BOM/margins, terminal-multiple choice and risk-free funding assumptions are all unverifiable for the hypothetical targets.",
        "- A positive terminal value can coexist with years of negative cash flow. Inspect the projection and working capital schedule.",
        "- No actual investment recommendation or company-specific valuation is produced.",
        ""
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def generate(root):
    """Build and return paths of reproducible files."""
    root = Path(root)
    with (root / "data" / "scenarios.json").open(encoding="utf-8") as handle:
        cfg = json.load(handle)
    with (root / "data" / "evidence.csv").open(encoding="utf-8", newline="") as handle:
        sources = list(csv.DictReader(handle))
    with (root / "data" / "comparables.csv").open(encoding="utf-8", newline="") as handle:
        comps = list(csv.DictReader(handle))
    source_ids = {row["id"] for row in sources}
    for row in comps:
        for key in ("source_revenue_id", "source_op_id", "source_gm_id"):
            if row.get(key) and row[key] not in source_ids:
                raise ValueError(f"Missing source ID in comparables: {row[key]}")
    years_infra = cfg["infra"]["years"]
    years_robot = cfg["robotics"]["years"]
    if years_infra != years_robot:
        raise ValueError("Cross-model scenarios must share projection years for this dashboard")
    outputs = ([compute_infra(cfg["infra"], name) for name in ("bear", "base", "bull")] +
               [compute_robotics(cfg["robotics"], name) for name in ("bear", "base", "bull")])
    sensitivity_infra = infra_sensitivity(cfg["infra"])
    sensitivity_robot = robotics_sensitivity(cfg["robotics"])
    report_dir = root / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    projection_paths = []
    for sector in ("inference_infra", "humanoid_robotics"):
        records = []
        for p in outputs:
            if p["sector"] != sector:
                continue
            records.extend([{"case": p["case"], **row} for row in p["rows"]])
        path = report_dir / (sector + "_projections.csv")
        _write_csv(path, records)
        projection_paths.append(path)
    summary_rows = [{
        "sector": x["sector"], "scenario": x["case"],
        "fy2030_revenue_usd_m": x["rows"][-1]["revenue_m"],
        "fy2030_ebitda_usd_m": x["rows"][-1]["ebitda_m"],
        "pv_annual_cashflows_usd_m": x["pv_cashflows_m"],
        "pv_terminal_usd_m": x["pv_terminal_m"],
        "enterprise_value_usd_m": x["ev_m"],
        "equity_value_usd_m": x["equity_value_m"],
        "terminal_metric": x["exit_metric"]
    } for x in outputs]
    summary_csv = report_dir / "scenario_summary.csv"
    _write_csv(summary_csv, summary_rows)
    sens_i = report_dir / "infrastructure_sensitivity.csv"
    sens_r = report_dir / "robotics_sensitivity.csv"
    _write_csv(sens_i, sensitivity_infra)
    _write_csv(sens_r, sensitivity_robot)
    json_path = report_dir / "model_results.json"
    json_path.write_text(json.dumps({
        "as_of": cfg["as_of"], "status": cfg["notice"],
        "models": outputs, "sensitivity_infra": sensitivity_infra,
        "sensitivity_robotics": sensitivity_robot,
        "source_count": len(sources), "comp_count": len(comps)
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    memo = report_dir / "model_snapshot.md"
    _write_summary_md(memo, outputs, (sensitivity_infra, sensitivity_robot))
    dashboard = report_dir / "index.html"
    _write_html(dashboard, outputs, sources, comps, sensitivity_infra, sensitivity_robot, cfg)
    return [*projection_paths, summary_csv, sens_i, sens_r, json_path, memo, dashboard]

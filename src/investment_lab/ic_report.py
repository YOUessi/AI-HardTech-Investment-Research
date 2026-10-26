"""Offline, source-anchored investment committee report for Vertiv.

For reproducibility this module uses only Python's standard library; no
provider API, live quote, model hallucination, or undisclosed firm data.
"""
from __future__ import annotations
from pathlib import Path
from .public_equity import load_and_compute
import csv
import html
import json


def _esc(x):
    return html.escape(str(x if x is not None else ""), quote=True)


def _fmt(x, decimals=2):
    return format(x, ",." + str(decimals) + "f")


def _table(headers, rows):
    h = "".join("<th>" + _esc(x) + "</th>" for x in headers)
    r = "".join("<tr>" + "".join("<td>" + str(c) + "</td>" for c in row) + "</tr>" for row in rows)
    return "<div class='scroll'><table><thead><tr>" + h + "</tr></thead><tbody>" + r + "</tbody></table></div>"


def _writer_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        if not rows:
            return
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _render(root, d, source):
    company = "Vertiv Holdings (VRT)"
    cases = d["cases"]
    colors = {"bear":"negative","base":"positive","bull":"warning"}
    def span(label, value, unit="", comment=""):
        return ("<div class='number-card'><small>" + _esc(label) + "</small><strong>" +
                _esc(_fmt(value)) + "</strong><span>" + _esc(unit) + "</span>" +
                ("<p>" + _esc(comment) + "</p>" if comment else "") + "</div>")
    stats = "".join([
        span("参考收盘价（2026-10-23）", d["reference_price_usd"],"USD/股","第三方市场数据；不是 10/27 即时报价"),
        span("参考市值",d["market_cap_usd_m"]/1000,"十亿美元","按 SEC 报告 384.988 百万股计算"),
        span("参考 EV（不含经营租赁）",d["market_ev_usd_m"]/1000,"十亿美元","EV = 市值 + 财务净债务"),
        span("2026E EV/调整后营业利润",d["ev_to_guided_fy2026_adj_op_x"],"倍","公司全年非 GAAP 指引"),
    ])
    def sec(c):
        return [
        "<b>" + _esc(c["name"].upper()) + "</b>", _esc(_fmt(c["fy2027_revenue_m"]/1000)) + " B",
        _esc(_fmt(c["growth_v_2026_mid_pct"]))+"%",
        _esc(_fmt(c["adj_op_margin_pct"]))+"%",
        _esc(_fmt(c["fy2027_adj_op_m"]/1000))+" B",
        _esc(_fmt(c["exit_ev_adj_op_x"]))+"×",
        "<strong class='"+colors[c["name"]]+"'>$"+_esc(_fmt(c["illustrative_fy2027_price_usd"]))+"</strong>",
        "<span class='"+colors[c["name"]]+"'>"+_esc(_fmt(c["price_change_from_reference_pct"]))+"%</span>"
    ]
    scens = _table(["分析师情景","FY2027收入","较2026指引中值增幅","调整后营业利润率","利润(十亿美元)","退出 EV/Adj OP","FY2027情景股价","相对参考价"], [sec(c) for c in cases])
    market = _table(["核算项","USD 百万美元 / 股数","数据日期 / 口径"],[
        ["参考股价", "$"+_fmt(d["reference_price_usd"]), "2026-10-23 完整交易日历史收盘"],
        ["流通类股本（报告发行股数）",_fmt(d["share_count_m"],3)+" 百万股","2026-07-27 10-Q 封面"],
        ["权益市值",_fmt(d["market_cap_usd_m"],1)+"m","价格 × 股数，非终端提供市值"],
        ["金融债务（净账面价值）",_fmt(d["gross_financial_debt_m"],1)+"m","2026-06-30"],
        ["现金及短期投资",_fmt(d["cash_and_st_investments_m"],1)+"m","2026-06-30，不含受限现金"],
        ["金融净债务",_fmt(d["net_financial_debt_m"],1)+"m","债务－可用现金，负值为净现金"],
        ["EV（不含租赁）",_fmt(d["market_ev_usd_m"],1)+"m","金融债务口径，与非 GAAP 利润不是完全可比"],
        ["经营租赁负债",_fmt(d["operating_lease_liabilities_m"],1)+"m","单独列示，不与主营 EBIT 倍数随意混比"],
        ["租赁调整参考 EV",_fmt(d["market_ev_including_operating_leases_m"],1)+"m","仅桥接，不是主估值口径"],
        ["2026 全年收入指引中值",_fmt(d["fy2026_company_guidance_sales_m"],1)+"m","管理层 2026-07-29 指引"],
        ["2026 非 GAAP 调整后营业利润中值",_fmt(d["fy2026_company_guidance_adj_op_m"],1)+"m","非 GAAP，非 EBITDA/GAAP EBIT"],
        ["2026 非 GAAP 调整后 FCF 中值",_fmt(d["fy2026_company_guidance_adj_fcf_m"],1)+"m","管理层前瞻数据"],
    ])
    cash = _table(["指标","USD 百万美元","解读 / 不要误读"],[
        ["2026 上半年经营现金流",_fmt(d["h1_2026_observed_ocf_m"]), "SEC 10-Q 披露，含营运资本变动"],
        ["2026 上半年资本开支+资本化软件",_fmt(d["h1_2026_observed_ocf_m"]-d["h1_2026_reported_fcf_ex_acquisitions_m"]),"未包含收购支出"],
        ["报告现金流扣除这些投资",_fmt(d["h1_2026_reported_fcf_ex_acquisitions_m"]),"这里的计算口径不是公司调整后 FCF 指引"],
        ["递延收入对经营现金流的变动贡献",_fmt(d["h1_2026_deferred_revenue_wc_uplift_m"]),"客户预付款等使当期 OCF 增加，不能等同经常性经营利润"],
        ["简单减去该项目的压力测试",_fmt(d["fcf_less_deferred_revenue_wc_illustrative_m"]),"仅情景诊断；绝不是正常化 GAAP FCF"],
        ["FY2026 H2 为达到收入指引中值所需收入",_fmt(d["h2_2026_implied_revenue_m"]),"用 FY 指引中值减已披露 H1 实绩"],
        ["FY2026 Q3 收入指引中值",_fmt(d["q3_2026_sales_guidance_mid_m"]),"管理层预测，尚非实际"],
        ["由此反推 FY2026 Q4 必须实现收入",_fmt(d["q4_2026_revenue_implied_m"]),"若 Q3 恰好达到指引中值"],
    ])
    srcRows = []
    for s in source:
        srcRows.append([
            "<a href='"+_esc(s["source_url"])+"' target='_blank' rel='noopener noreferrer'>"+_esc(s["id"])+"</a>",
            _esc(s["observation_date"]),
            _esc(s["observation_type"]),
            _esc(s["value"])+" "+_esc(s["unit"]),
            _esc(s["validation_status"])
        ])
    sourcetable=_table(["数据ID / 原始出处","数据日期","数据类型","值","可信等级"],srcRows)
    gridRows = []
    margins = sorted(set(row["operating_margin_pct"] for row in d["sensitivity"]))
    multiples = sorted(set(row["ev_adj_op_x"] for row in d["sensitivity"]))
    lookup = {(row["operating_margin_pct"],row["ev_adj_op_x"]):row["illustrative_price_usd"]
              for row in d["sensitivity"]}
    for margin in margins:
        values=[]
        for multiple in multiples:
            price=lookup[(margin,multiple)]
            tone="price-green" if price<=d["reference_price_usd"] else "price-blue"
            if price<d["illustrative_max_entry_usd"]:
                tone="price-low"
            values.append("<span class='heat "+tone+"'>$"+_esc(_fmt(price,1))+"</span>")
        gridRows.append(["<b>"+_esc(_fmt(margin,1))+"%</b>"]+values)
    heat=_table(["2027调整后利润率 / 退出倍数"]+[str(x)+"×" for x in multiples],gridRows)
    css = """
    :root{--bg:#f5f7fa;--ink:#172d42;--navy:#112c43;--muted:#61758a;--border:#dce5ed;--paper:#fff;--teal:#15856f;--red:#b6494c}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{font:13.5px/1.8 -apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;margin:0;background:var(--bg);color:var(--ink)}
    .wrap{max-width:1340px;margin:auto;padding:0 25px}header{background:linear-gradient(114deg,#10283d,#1f4463 78%);padding:43px 0 61px;color:#fff}
    header h1{font-size:clamp(25px,3.5vw,44px);line-height:1.24;letter-spacing:-.04em;margin:6px 0 13px}header p{margin:0;max-width:950px;color:#c0d4e2;line-height:1.85}
    .kicker{color:#85bce8;letter-spacing:.15em;font-weight:750;font-size:11px}
    .nav{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}.nav a{background:#ffffff16;border:1px solid #ffffff23;border-radius:20px;padding:5px 12px;color:#eaf5ff;text-decoration:none;font-size:12px}
    h2{font-size:22px;line-height:1.3;letter-spacing:-.015em;margin:7px 0 13px}h3{font-size:15px;margin:12px 0 6px}
    .eyebrow{font-size:11px;letter-spacing:.1em;font-weight:800;color:#457ea5}.recommend{margin:-27px 0 22px;position:relative;background:white;border:1px solid #dae4ed;border-left:5px solid #c37a27;border-radius:13px;padding:17px 20px;box-shadow:0 6px 25px #14283b14}
    .recommend strong{font-size:15px}.recommend p{margin:5px 0;color:#6a7f90}.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:11px}.number-card{border:1px solid var(--border);background:white;padding:14px 16px;border-radius:11px}
    .number-card small{color:#64798d;display:block;font-size:11px}.number-card strong{font-size:28px;line-height:1.4;letter-spacing:-.035em;display:inline-block;color:#194769}
    .number-card span{font-size:11px;color:#8ea1b1;margin-left:5px}.number-card p{font-size:11px;color:#8897a7;margin:2px 0}
    section{margin:34px 0}a{color:#1e6caa;text-decoration:none}a:hover{text-decoration:underline}
    .scroll{border:1px solid var(--border);background:#fff;border-radius:12px;overflow:auto}table{border-collapse:collapse;width:100%;min-width:800px}thead{background:#edf3f7}th{text-align:left;font-size:11px;color:#4b667d;white-space:nowrap}
    th,td{border-bottom:1px solid #eaf0f4;padding:10px 12px;vertical-align:top}tbody tr:last-child td{border-bottom:0}tbody tr:hover{background:#fbfcfe}
    .negative{color:#a8474a}.positive{color:#136e5e}.warning{color:#a36720}.note{border:1px solid #dce6ef;background:#fff;border-radius:12px;padding:12px 16px;margin:12px 0;color:#5a7082}
    .note b{color:#193b56}.note-risk{background:#fff6e9;border-color:#f2d8ad;color:#9a6429}
    .columns{display:grid;grid-template-columns:1fr 1fr;gap:15px}.columns ul{padding-left:18px;color:#5e7184;margin:7px 0}.columns li{margin:5px 0}
    .heat{display:block;border-radius:6px;text-align:center;padding:6px 10px;min-width:80px;white-space:nowrap;font-variant-numeric:tabular-nums}
    .price-blue{background:#e5f1ff;color:#2b66a4}.price-green{background:#edf2ff;color:#4e62a3}.price-low{background:#e0f6e9;color:#23734c}
    .pill{display:inline-block;border-radius:16px;padding:2px 9px;font-size:10px;background:#e4edf7;color:#3a668a;margin-right:6px}
    .callout{padding:14px 17px;border-radius:10px;background:#eaf4fb;border:1px solid #cfe4f4;color:#3f6381}
    footer{border-top:1px solid var(--border);background:#fff;color:#8797a7;padding:25px 0 40px}
    @media(max-width:1000px){.grid4{grid-template-columns:repeat(2,1fr)}.columns{grid-template-columns:1fr}}
    @media(max-width:590px){.wrap{padding:0 14px}.grid4{grid-template-columns:1fr 1fr}.number-card strong{font-size:23px}.number-card{padding:9px}header{padding:27px 0 52px}}
    @media print{body{background:white;font-size:10px}.wrap{max-width:none;padding:0 10mm}header{background:#fff;color:#000;padding:10mm 0 4mm}.nav{display:none}header p{color:#555}.recommend{margin:4mm 0}.grid4{display:flex}.number-card{flex:1;break-inside:avoid}.number-card strong{font-size:20px}section{page-break-inside:avoid}.scroll{overflow:visible}table{min-width:0}td,th{padding:5px 6px;font-size:9px}.columns{display:block}}
    """
    html_doc = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>VRT 公募投资委员会材料 · 2026-10-27</title><style>""" + css + """</style></head><body>
    <header><div class='wrap'><div class='kicker'>INVESTMENT COMMITTEE / POINT-IN-TIME PUBLIC EQUITY / 2026-10-27</div>
    <h1>Vertiv (VRT)：算力基础设施的真实投资价值，是否已经反映在股价中？</h1>
    <p>基于真实 SEC 10-Q、企业 2026 年第二季度指引和 2026-10-23 已确认的历史收盘价。2027 三情景是透明的分析师假设，不是管理层指引，也不是即时报价。</p>
    <div class='nav'><a href='#decision'>决议卡</a><a href='#market'>资本结构</a><a href='#scenarios'>情景估值</a><a href='#cash'>现金流质量</a><a href='#stress'>敏感性</a><a href='#sources'>来源</a></div></div></header>
    <main class='wrap'><div class='recommend' id='decision'><strong>投委会模拟决议：暂不新增仓位；2026-10-28 财报后复核</strong>
    <p>2026-10-23 完整交易日收盘 <b>$""" + _fmt(d["reference_price_usd"]) + """</b>，高于使用 25% 安全边际计算的观察价 <b>$""" + _fmt(d["illustrative_max_entry_usd"]) + """</b>。即使价格触及阈值，仍需在 Q3 财报后重新校验现金流、盈利指引与股本债务；本资料不构成可直接执行的订单。</p></div>
    <section><div class='eyebrow'>01 / MARKET OBSERVATIONS</div><h2>真正的已披露定价基础</h2><div class='grid4'>""" + stats + """</div></section>
    <section id='market'><div class='eyebrow'>02 / CAPITAL BRIDGE</div><h2>从股价到企业价值：股本、债务、现金分开记录</h2>""" + market + """<div class='note'>Q2 10-Q 股数截至 2026-07-27，现金债务截至 2026-06-30，股价取 2026-10-23 已完成收盘。日期并不一致，是公开市场模型的已披露局限。经营租赁负债单列，未无条件并入主 EV/调整后营业利润倍数。</div></section>
    <section id='scenarios'><div class='eyebrow'>03 / ANALYST ASSUMPTIONS</div><h2>2027 财年三情景股价：可辩论的假设，不是“真实预测值”</h2>""" + scens + """<div class='note'>公式：2027E 调整后营业利润 = 收入×调整后营业利润率；退出 EV = 利润×假设 EV/调整后营业利润倍数；退出每股价值 = (退出 EV − 冻结的净财务债务)÷当前股份数。FY2027 场景末值并非精确 12 个月目标价，也不包含股息、融资、未来股本稀释或事件发生概率。</div><div class='callout'>参考入场观察价：<b>$""" + _fmt(d["illustrative_max_entry_usd"]) + """</b>；参考价：<b>$""" + _fmt(d["reference_price_usd"]) + """</b>；即使财报后满足证据门槛，策略示例的最大名义仓位为 NAV 的 <b>""" + _fmt(d["illustrative_risk_based_post_gate_weight_pct_nav"],2) + """%</b>（仅示范风控，不代表任何投资者仓位建议）。</div></section>
    <section id='cash'><div class='eyebrow'>04 / QUALITY OF EARNINGS</div><h2>现金流质量：区分经营利润、客户预收款与资本开支</h2>""" + cash + """<div class='note note-risk'><b>关键问题：</b>报告中 2026 H1 经营现金流增加主要受递延收入及营运资本支持。简单移除递延收入流入后的负值只是<b>单项目压力测试</b>，不是重编制 GAAP 现金流或可持续 FCF。还需检查库存、应收、应付、合同负债账龄及 2026 H2 转化。</div></section>
    <section id='stress'><div class='eyebrow'>05 / RISK AND SENSITIVITY</div><h2>固定 2027 基准收入、改变利润率与退出倍数（USD/股）</h2>""" + heat + """<div class='note'>横轴非 GAAP 调整后营业利润退出倍数，纵轴为 2027 假设调整后营业利润率；它不是统计置信区间。退出倍数不是从某公司实际挂牌的同口径可比交易推算的观察值。</div></section>
    <section><div class='eyebrow'>06 / INVESTMENT COMMITTEE CHALLENGE</div><h2>2026-10-28 财报之后，必须重新决策什么？</h2><div class='columns'><div class='note'><h3>允许进入下一轮讨论</h3><ul><li>发布的 Q3 实绩与全年正式指引能够支持当前建模增长路径。</li><li>订单与收入兑现不依赖不可持续的客户预收款增加。</li><li>库存、应收和扩产资本开支有可核实的回款/交付计划。</li><li>重算最新股价、股本、净债务及经确认的盈余现金流后，仍存在目标安全边际。</li></ul></div><div class='note'><h3>否决或暂停信号</h3><ul><li>2026 收入、调整后利润与 FCF 指引出现未解释的下修。</li><li>库存和回款劣化超过订单增长可解释范围。</li><li>订单取消、施工延期或竞争导致非 GAAP 利润率假设失真。</li><li>基准估值必须进一步上调退出倍数才能有正回报。</li></ul></div></div></section>
    <section id='sources'><div class='eyebrow'>07 / SOURCE TRACEABILITY</div><h2>17 条已核实或来源标记的数据记录</h2>""" + sourcetable + """</section>
    <section><div class='note note-risk'><b>免责声明 / 数据纪律：</b>请勿把最新 2026-10-26 的盘中价格误作收盘。公司尚未发布的 2026-10-28 Q3 数据不在此材料中。季度财报与 2027 情景之间存在明显预测不确定性；分析师采用的退出倍数、2027 经营表现、未来股本和净现金冻结假设均需更新。本材料是一份可复核的公开市场投委会讨论样例，不替代买方的投资授权或实际交易尽调。</div></section>
    </main><footer><div class='wrap'>AI & Hard-Tech Investment Research · as-of 2026-10-27 · 可离线查看和使用浏览器打印为 PDF · <a href='https://github.com/YOUessi/AI-HardTech-Investment-Research'>GitHub 仓库</a></div></footer></body></html>
    """
    return html_doc


def generate_ic_report(root):
    root=Path(root)
    data=load_and_compute(root)
    with (root/"data"/"vrt_evidence.csv").open(newline="",encoding="utf-8") as f:
        evidence=list(csv.DictReader(f))
    ids={r["id"] for r in evidence}
    required=("VRT-20261023-CLOSE","VRT-2026Q2-SHARES","VRT-2026Q2-GUIDANCE","VRT-Q3-DATE")
    if len(ids)!=len(evidence) or any(x not in ids for x in required):
        raise ValueError("Incomplete issuer data provenance")
    output=root/"reports"
    output.mkdir(exist_ok=True)
    data_path=output/"vrt_ic_decision.json"
    data_path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    scenarios=output/"vrt_ic_scenarios.csv"
    _writer_csv(scenarios,data["cases"])
    sensitivity=output/"vrt_ic_sensitivity.csv"
    _writer_csv(sensitivity,data["sensitivity"])
    page=output/"vrt_ic_dashboard.html"
    page.write_text(_render(root,data,evidence),encoding="utf-8")
    md=output/"vrt_ic_decision_card.md"
    lines=[
        "# VRT 上市公司投委会决议卡 — 2026-10-27",
        "",
        "> **结论：暂不新增仓位；等 2026-10-28 官方 Q3 财报后重估。**",
        "> 依据：截至目前最后确认的完整收盘价 2026-10-23 USD "+_fmt(data["reference_price_usd"]),
        "> ，高于 2027 Base 情景 25% 安全边际的条件入场价 USD "+_fmt(data["illustrative_max_entry_usd"])+
        "。分析师假设、非实际公司 FY2027 指引。","",
        "| 核心项目 | 数值 |","|---|---:|",
        "| 股本（2026-07-27，百万股） | "+_fmt(data["share_count_m"],6)+" |",
        "| 市值（百万美元） | "+_fmt(data["market_cap_usd_m"])+" |",
        "| 财务净债务（百万美元） | "+_fmt(data["net_financial_debt_m"])+" |",
        "| EV 不含租赁（百万美元） | "+_fmt(data["market_ev_usd_m"])+" |",
        "| 市场 EV / 2026 管理层调整后营业利润指引中值 | "+_fmt(data["ev_to_guided_fy2026_adj_op_x"])+" 倍 |",
        "| H1 OCF 扣 capex+资本化软件（百万美元） | "+_fmt(data["h1_2026_reported_fcf_ex_acquisitions_m"])+" |",
        "| H1 递延收入对经营现金流增加（百万美元） | "+_fmt(data["h1_2026_deferred_revenue_wc_uplift_m"])+" |",
        "| H1 单项剔除递延收入后的压力测试（百万美元，非 normalized FCF） | "+_fmt(data["fcf_less_deferred_revenue_wc_illustrative_m"])+" |",
        "| 2026 Q4 达成全年指引中值所需收入（百万美元） | "+_fmt(data["q4_2026_revenue_implied_m"])+" |",
        "",
        "| 情景 | 2027收入百万美元 | 利润率 | 退出倍数 | 2027假设每股价值 USD |",
        "|---|---:|---:|---:|---:|"
    ]
    for c in data["cases"]:
        lines.append("| "+c["name"]+" | "+_fmt(c["fy2027_revenue_m"])+" | "+_fmt(c["adj_op_margin_pct"])+"% | "+
                     _fmt(c["exit_ev_adj_op_x"])+"× | "+_fmt(c["illustrative_fy2027_price_usd"])+" |")
    lines.extend(["","**财报事件：** 2026-10-28；当前只应批准跟踪及信息验证，不应按本报告下单。",
                  "","**详细论证：** [research/07_vrt_public_market_ic_20261027.md](../research/07_vrt_public_market_ic_20261027.md)",
                  "","**来源：** [data/vrt_evidence.csv](../data/vrt_evidence.csv)",
                  "","**注意：** 使用 2026-10-23 最后验证收盘价；资本结构是 2026-06/07 的最近披露，2027净债务/股本未预测；非 GAAP adjusted profit 不是 EBITDA；风险预算为教学示例。"])
    md.write_text("\n".join(lines)+"\n",encoding="utf-8")
    return [data_path,scenarios,sensitivity,page,md]

"""Offline issuer-evidence-driven Unitree valuation hurdle, and combined IC landing page."""
from pathlib import Path
import html
import json
import csv
from .unitree_equity import load_and_compute


def _esc(x):
    return html.escape(str(x if x is not None else ""), quote=True)


def _fmt(x, digits=2):
    return format(x, ",."+str(digits)+"f")


def _table(headers, rows):
    return ("<div class='scroll'><table><thead><tr>"+
            "".join("<th>"+_esc(h)+"</th>" for h in headers)+
            "</tr></thead><tbody>"+
            "".join("<tr>"+"".join("<td>"+str(x)+"</td>" for x in row)+"</tr>" for row in rows)+
            "</tbody></table></div>")


def _base_style():
    return """
    :root{--ink:#162f46;--navy:#122e46;--blue:#285f86;--line:#dfe7ee;--bg:#f5f8fa}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{background:var(--bg);margin:0;color:var(--ink);font:13px/1.75 system-ui,-apple-system,'PingFang SC','Microsoft YaHei',Arial,sans-serif}
    .w{margin:auto;max-width:1280px;padding:0 23px}header{background:linear-gradient(114deg,#10283b,#1d4b66);color:#fff;padding:44px 0 59px}
    header h1{font-size:clamp(26px,3.6vw,43px);line-height:1.25;letter-spacing:-.04em;margin:8px 0}
    header p{margin:0;color:#b6d0dd;max-width:880px;font-size:14px;line-height:1.95}
    .eyebrow{letter-spacing:.14em;font-size:10px;font-weight:850;color:#8dbbd8}
    a{color:#236c9f;text-decoration:none}a:hover{text-decoration:underline}
    .links{display:flex;gap:7px;flex-wrap:wrap;margin-top:16px}.links a{padding:5px 10px;border-radius:16px;border:1px solid #ffffff26;background:#ffffff15;color:#e5f3fd;font-size:12px}
    .alert{margin:-26px 0 25px;position:relative;padding:17px 19px;border-left:5px solid #bb7837;background:#fff7e9;border-radius:12px;box-shadow:0 4px 19px #23405c12;color:#80501e}
    section{margin:30px 0}h2{margin:5px 0 11px;font-size:21px;line-height:1.3}h3{margin:8px 0;font-size:15px}
    .cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px}
    .card small{display:block;color:#697c8d}.card strong{display:block;color:#164766;font-size:28px;line-height:1.5}
    .card p{font-size:11px;color:#8595a2;margin:3px 0}
    .scroll{overflow:auto;border:1px solid var(--line);background:#fff;border-radius:12px}table{border-collapse:collapse;width:100%;min-width:780px}
    th,td{text-align:left;padding:11px 13px;vertical-align:top;border-bottom:1px solid #edf0f4}th{background:#ecf2f6;font-size:11px;color:#516a82}tbody tr:last-child td{border-bottom:0}
    .note{padding:14px 17px;border:1px solid var(--line);background:#fff;border-radius:12px;color:#526a80;margin:12px 0}
    .note.warn{background:#fff7ea;border-color:#f0ddbe;color:#886022}
    .two{display:grid;grid-template-columns:1fr 1fr;gap:14px}.two ul{margin:5px 0;padding-left:19px}
    .cell{display:block;text-align:center;padding:5px 9px;border-radius:7px;white-space:nowrap}
    .high{background:#ffedef;color:#a94949}.medium{background:#fff3e1;color:#aa752e}.low{background:#e7f3ef;color:#277960}
    .related{display:grid;grid-template-columns:1fr 1fr;gap:12px}.related a{display:block;background:#fff;padding:17px;border:1px solid #dce6ed;border-radius:12px;font-weight:700}
    .related small{color:#7f8e9a;font-weight:400;display:block}footer{padding:35px 0;color:#8697a4}
    @media(max-width:930px){.cards,.related{grid-template-columns:repeat(2,1fr)}.two{grid-template-columns:1fr}}
    @media(max-width:560px){.w{padding:0 13px}.cards{grid-template-columns:repeat(2,1fr)}.card strong{font-size:22px}header{padding:26px 0 51px}}
    @media print{.scroll{overflow:visible}table{min-width:0}th,td{padding:4px;font-size:9px}header{background:#fff;color:#111;padding:5mm 0}header p{color:#666}.links{display:none}.cards{display:flex}.card{flex:1}.two{display:block}.alert{margin:5mm 0}}
    """


def _unitree_page(d, evidence):
    grid=d["reverse_valuation_grid"]
    margins=sorted(set(row["net_margin_pct"] for row in grid))
    pes=sorted(set(row["hypothetical_forward_pe_x"] for row in grid))
    lookup={(row["net_margin_pct"],row["hypothetical_forward_pe_x"]):row for row in grid}
    rows=[]
    for margin in margins:
        row=["<b>"+_esc(_fmt(margin,1))+"%</b>"]
        for pe in pes:
            val=lookup[(margin,pe)]["required_annual_revenue_cny_m"]/1000
            cl="high" if val>15 else ("medium" if val>6 else "low")
            row.append("<span class='cell "+cl+"'>"+_esc(_fmt(val,2))+"</span>")
        rows.append(row)
    source_rows=[["<a href='"+_esc(s["source_url"])+"' target='_blank' rel='noopener noreferrer'>"+
                  _esc(s["id"])+"</a>",_esc(s["observed_as_of"]),_esc(s["metric"]),
                  _esc(s["value"])+" "+_esc(s["unit"]),_esc(s["source_tier"])] for s in evidence]
    style=_base_style()
    body="""<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>宇树科技 688836 投资委员会备忘录 · 2026-10-27</title><style>""" + style + """</style></head><body>
    <header><div class='w'><div class='eyebrow'>PUBLIC EQUITY / 2026-10-27 / RISK-FIRST</div>
    <h1>宇树科技 688836：2720 亿元市值，必须实现多少利润？</h1>
    <p>以真实交易所股本、历史完整收盘价、IPO 经审计财务和未经审计半年报为基础，采用反向收入门槛而非杜撰机器人企业现金流。公司 2026 年 8 月已经上市，不能再作为未上市公司分析。</p>
    <nav class='links'><a href='#capital'>上市/股本</a><a href='#earnings'>实际利润</a><a href='#reverse'>反向估值</a><a href='#risks'>IC 决议</a><a href='#sources'>证据</a></nav></div></header>
    <main class='w'><div class='alert'><strong>模拟委员会建议：观察 / 暂不新增仓位。</strong>
    <div>2026-10-26 完整上交所收盘价 ¥""" + _fmt(d["reference_close_cny"]) + """，发行人公告滚动 PE 465.22×、三日异常波动及产业商业化不确定性。下表反向估值仅表明当前市场价格对未来盈利的要求；不能当未来一年的营业收入预测。</div></div>
    <section id='capital'><div class='eyebrow'>01 / LISTED EQUITY FACTS</div><h2>市值是可核算的，企业价值尚不能可靠桥接</h2><div class='cards'>
    <div class='card'><small>2026-10-26 完整收盘</small><strong>¥""" + _fmt(d["reference_close_cny"],0) + """</strong><p>A股科创板 688836</p></div>
    <div class='card'><small>市值（人民币十亿元）</small><strong>""" + _fmt(d["market_cap_cny_bn"],2) + """</strong><p>发行后总股本×交易所收盘价</p></div>
    <div class='card'><small>初始自由流通 / 总股本</small><strong>""" + _fmt(d["unrestricted_as_pct_total_initial"]) + """%</strong><p>2026-08 上市日初始；须更新实际流通</p></div>
    <div class='card'><small>公司异常公告滚动 PE</small><strong>""" + _fmt(d["issuer_disclosed_trailing_pe_x"]) + """×</strong><p>2026-10-26 截止，发行人披露</p></div>
    </div><div class='note'>总发行股份 """ + _esc(d["total_shares"]) + """；初始无限售流通 """ + _esc(d["listed_initial_unrestricted_shares"]) + """ 股。公司设有差异化表决权安排。IPO 之后现金、债务与租赁余额需要新的同日期资料，因此<b>不计算也不捏造 EV</b>。</div></section>
    <section id='earnings'><div class='eyebrow'>02 / REPORTED OPERATIONS</div><h2>2025 年审计与 2026 年 H1 未经审计财务</h2>
    """ + _table(["财务指标","FY2025 年度","H1 2026 已披露","重要解释"],[
    ["总收入（百万元RMB）",_fmt(d["fy2025_sales_cny_m"]),_fmt(d["h1_2026_revenue_cny_m"]),"H1 同比 +"+_fmt(d["h1_2026_yoy_revenue_pct"])+"%；不能直接乘2当预测"],
    ["归母净利润（百万元RMB）",_fmt(d["fy2025_attributable_profit_cny_m"]),_fmt(d["h1_2026_attributable_profit_cny_m"]),"2025 与 2026 上半年股份支付影响可比性"],
    ["扣非归母净利润（百万元RMB）","另见正式招股说明书",_fmt(d["h1_2026_ex_nonrecurring_profit_cny_m"]),"H1 同比 "+_fmt(d["h1_2026_ex_nonrecurring_profit_yoy_pct"])+"%"],
    ["经营现金流（百万元RMB）","另见正式招股说明书",_fmt(d["h1_2026_ocf_cny_m"]),"H1 同比 "+_fmt(d["h1_2026_ocf_yoy_pct"])+"%"],
    ["FY2025 人形机器人收入（百万元RMB）",_fmt(d["fy2025_humanoid_segment_sales_cny_m"]),"-","占总收入 "+_fmt(d["fy2025_humanoid_sales_pct_of_total"])+"%；不等同主营占比51.78%"],
    ["FY2025 人形机器人售出数量",str(d["fy2025_humanoid_units_sold"]),"-","产品组合售价不同于网上G1/R1起售价"]
    ]) + """<div class='note warn'>不可只强调营业收入同比上涨。2026 H1 扣非归母净利润和经营现金流均同比下降，应调查研发、销售费用与客户款项质量。</div></section>
    <section id='reverse'><div class='eyebrow'>03 / REVERSE INVESTMENT HURDLE</div><h2>当前总市值需多大的年收入支撑？（假设净利率 × 假设前瞻 PE）</h2>
    <p class='note'>以下格子单位：<b>人民币十亿元年度收入</b>。公式：当前市值 ÷(假设 PE×假设净利率)。假设 FY2027 财年仅用于固定讨论期限，不是管理层指引、真实 PE 或盈利预测。</p>
    """ + _table(["假设净利率 / 假设未来P/E"]+[str(x)+"×" for x in pes],rows) + """
    <div class='note'>举例：若净利润率 20%、未来 PE 50×，现市值要求年度净利润约 ¥5.44bn 和年度收入 ¥27.18bn，相当于 2026 H1 收入机械年化的约 11.8×。行业尚在商业化阶段，这只是<b>资本市场隐含的规模验证门槛</b>，不是在预言企业无法实现。</div>
    <div class='note'>市值/2025 全年销售 """ + _fmt(d["spot_mcap_to_fy2025_reported_sales_x"]) + """×；市值/(H1 2026 收入×2) """ + _fmt(d["spot_mcap_to_mechanical_h1_annualized_sales_x"]) + """×；市值/(H1 净利润×2) """ + _fmt(d["spot_mcap_to_mechanical_h1_annualized_net_profit_x"]) + """×。这些<b>简单年化的机械比率绝不等于官方滚动市盈率 465.22×</b>。</div></section>
    <section id='risks'><div class='eyebrow'>04 / DECISION & RISK CONTROL</div><h2>下一次委员会放行的必要条件</h2><div class='two'><div class='note'><h3>必须获取</h3><ul>""" + "".join("<li>"+_esc(x)+"</li>" for x in d["gates"]) + """</ul></div>
    <div class='note'><h3>核心反证</h3><ul><li>2025 机器人出货及真实主营收入增长迅速，成本/渠道规模优势可能很强。</li><li>但目前 2026H1 扣非利润下滑且流通盘较窄，大幅股价上涨不能证明 2027+ 经营表现。</li><li>公告中的通用设备平均 P/E 不是同业务真实可比倍数，不能用其作买价。</li><li>若拿不到 IPO 后一致口径净债务，拒绝伪造 EV 与年度自由现金流 DCF。</li></ul></div></div></section>
    <section id='sources'><div class='eyebrow'>05 / DOCUMENTED PROVENANCE</div><h2>上市、股本、报表、股价与发行人公告均有出处</h2>
    """ + _table(["证据来源 ID","观察日","字段","数值","可信度"],source_rows) + """</section>
    <section><div class='note warn'><b>重要限制：</b>本报告不包含经独立验证的工厂 BOM、用户账单、机器人自主工作时长、上市后实时净现金或真实投票权经济权益转换。不是个人股票建议，不做交易。需要从公司公告后补充最新流通股、解禁和财报，重审资本结构。</div></section>
    </main><footer class='w'>Point-in-time 2026-10-27 · 独立离线 HTML · <a href='https://github.com/YOUessi/AI-HardTech-Investment-Research'>GitHub 项目</a></footer>
    </body></html>"""
    return body


def _landing():
    style=_base_style()
    return """<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>公开市场投委会 | AI & Hard Tech</title><style>""" + style + """</style></head><body><header><div class='w'><div class='eyebrow'>AI & HARD-TECH / PUBLIC EQUITY IC / 2026-10-27</div><h1>两只真实上市标的，两种完全不同的投资风险</h1><p>公开资料可复算的投资委员会讨论包。VRT：美国数据中心硬件设备与电力冷却；宇树科技：科创板人形机器人 OEM。历史数值、投资假设和待尽调事项分开存档。</p></div></header><main class='w'>
    <div class='alert'><b>模拟决议：两只标的均暂不新增仓位；批准后续披露验证。</b><div>VRT：2026-10-28 官方业绩事件前不得把指引视为实际；宇树：发行人2026-10-26 异常波动公告警告估值与产业商业化风险。本页面不执行证券交易。</div></div>
    <section><div class='eyebrow'>REAL ISSUERS / SEPARATE CURRENCIES</div><h2>选择要阅读的上市公司 IC</h2><div class='related'>
    <a href='vrt_ic_dashboard.html'>Vertiv · NYSE: VRT<small>2026-10-23 最后已核实完成收盘美元报价；SEC财报、现金流、三情景FY2027终值与负债表。模拟建议：等待10-28财报。</small></a>
    <a href='unitree_ic_dashboard.html'>宇树科技 · SSE: 688836<small>2026-10-26 人民币收盘价；IPO及H1经营财务、流通盘、滚动市盈率、反向利润/收入门槛。模拟建议：观察/不新增仓位。</small></a></div>
    <div class='note'><h3>原仓库中两套虚构经济性模型还在</h3><p><a href='index.html'>查看独立行业假设研究</a>。它们不代表任何真实上市公司，不能替代上面两份依据 SEC/SSE/发行人披露建立的投资研究。</p></div>
    <div class='note'><h3>研究材料与过程</h3><p><a href='https://github.com/YOUessi/AI-HardTech-Investment-Research/tree/main/research'>完整投资研究目录</a> · <a href='https://github.com/YOUessi/AI-HardTech-Investment-Research/tree/main/data'>证据台账和原始数据</a></p></div></section>
    </main><footer class='w'>公开资料核对版 · 更新截止 2026-10-27 · 财报后需刷新数据才能进行新的投委会表决</footer></body></html>"""


def generate_unitree_report(root):
    root=Path(root)
    d=load_and_compute(root)
    with (root/"data"/"unitree_evidence.csv").open(encoding="utf-8",newline="") as f:
        src=list(csv.DictReader(f))
    ids=[x["id"] for x in src]
    if len(ids)!=len(set(ids)) or "UNIT-20261026-CLOSE" not in ids:
        raise ValueError("Invalid Unitree evidence registry")
    out=root/"reports"
    out.mkdir(exist_ok=True)
    paths=[out/"unitree_ic_decision.json",out/"unitree_reverse_hurdle.csv",
           out/"unitree_ic_dashboard.html",out/"ic_portfolio_overview.html"]
    paths[0].write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with paths[1].open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(d["reverse_valuation_grid"][0].keys()))
        writer.writeheader()
        writer.writerows(d["reverse_valuation_grid"])
    paths[2].write_text(_unitree_page(d,src),encoding="utf-8")
    paths[3].write_text(_landing(),encoding="utf-8")
    return paths

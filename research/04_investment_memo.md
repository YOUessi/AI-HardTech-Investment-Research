# 04 — Investment committee memorandum

**PROJECT:** AI Inference Infrastructure × Humanoid Robotics — Where is durable value capture?

**Prepared:** 2026-10-27 | **Decision requested:** Authorization for targeted diligence, **not authorization to invest** | **Currency:** Public filings retain disclosed currency; numerical synthetic financial models are in USD millions.

**Status:** PUBLIC-RESEARCH STAGE — **WATCH / CONDITIONAL DILIGENCE ONLY.**

> The computed enterprise values are for TWO FICTIONAL businesses with explicit invented assumptions. They do not value NVIDIA, AMD, Vertiv, CoreWeave, UBTECH or Unitree. The market has no duty to trade at our synthetic estimates. Historical public data is confined to the dated evidence ledger.

---

## 1. Executive summary

### Decision

Allocate research and interview resources to **two theses**:

1. **Inference infrastructure enablement and utilization software**: prioritize verified power access, sustainable delivered tokens/$ and multi-vintage GPU fleet economics over generic sector-capex stories. Favor durable site/power bottleneck solutions and cash-efficient software leverage; be cautious about leveraged GPU-hour resale without differentiated procurement and service guarantees.
2. **Humanoid robotics for narrow paid workflows**: prioritize repeatable autonomous task completion and customer cost savings over shipment counts, demo performance and posted hardware prices. Treat industrial deployment as an engineering and change-management integration problem first, before broad general-purpose robotics monetization.

Current evidence supports **sector growth and technical opportunity**, but does not clear investment gates for a specific private target. Public market data alone cannot establish margin durability, target company enterprise value, liquidation terms, or customer concentration.

### Strongest observed anchors

- IEA (2026) places global data-center electricity use around **485 TWh in 2025** and ~**950 TWh in 2030 central projection**. This indicates a consequential physical expansion and associated power constraints, **not a guaranteed return for new cloud supply**. [IEA-DC-2025, IEA-DC-2030]
- NVIDIA's **FY2027 Q2** reported **USD96.221bn** total revenue and approx **USD89.0bn** Data Center segment revenue; AMD reported **USD11.536bn** total 2026 Q2 revenue and approx **USD6.7bn** Data Center. Vertiv reported **USD3.274bn** of 2026 Q2 net sales. These disclosures evidence activity at different layers, not a comparable set of cloud-compute profit margins. [NV-FY27-Q2-REV, NV-FY27-Q2-DC, AMD-2026Q2-REV, AMD-2026Q2-DC, VRT-2026Q2-SALES]
- CoreWeave reported **USD2.575bn** Q2 2026 revenue yet **USD49m operating loss** and **USD1.507bn** of Technology and Infrastructure cost; accounting classification matters when estimating GPU rental contribution. [CW-2026Q2-REV, CW-2026Q2-OP, CW-2026Q2-INFRA]
- UBTECH reported **RMB1.269bn** H1 2026 revenue including **RMB590m** from full-size embodied humanoid products/services, with **RMB338.8m period loss**. This is stronger than a pure promotional shipment number but still not proof of a profitable autonomy deployment. [UBT-H1-REV, UBT-H1-HUM, UBT-H1-NET]
- IFR reported ~**7,000 full-size humanoid units** sold globally in 2025 for professional/commercial use; Counterpoint cited **>22,000 units** shipped in H1 2026 under different definition. These statistics **cannot be stitched into a single CAGR**. [IFR-2025-HUM, CP-2026H1-HUM]

### Investment screening thesis

**Buy the scarce, repeatable economic unit, not the impressive demonstration.** For AI infrastructure this is a verifiable cost/latency-compliant, collected GPU-hour or useful token with power and hardware lifecycle priced in. For robotics it is a profitable accepted autonomous task hour after supervision, maintenance and warranty.

---

## 2. Investment universe and value chain

### Infrastructure: five sources of value

**A. Chip and system platform.** NVIDIA/AMD and adjacent networking/storage suppliers monetize performance, systems integration and software compatibility. Strong segment revenue is supportive of customer demand but should not be used to underwrite a new GPU lessor's margin.

**B. Power and cooling access.** Power availability, permitting, high-density thermal engineering, liquid cooling and commissioning are physical gating items. Vertiv is a relevant public benchmark for this type of economic exposure. The risk: lead times, delayed projects, inventories and working-capital expansion.

**C. Financing and deployment.** Customers cannot use hardware until sites, networking, power and supply are commissioned. Operator financing structures, hardware collateral and procurement contracts determine risk.

**D. Serving runtime.** Good scheduling, quantization and KV-cache placement can improve token throughput and tail latency. However, the runtime moat may erode as open-source frameworks catch up. An investor must test *production workload* advantage, not peak synthetic Kernel speedup.

**E. Paid enterprise applications.** A true customer may pay for verified workflow results, not raw tokens. Customer retention and integration can be durable but introduce data, liability and market-concentration risks.

### Robotics: value chain and buying centers

Actuators/reducers → motors/drivers → cameras/IMU/edge compute → whole-body controller → action policy & datasets → robot OEM → field service / integration → end-user task ROI.

The buyer is not always the operator. Early procurement can be an R&D/pilot budget, marketing effort or public-sector demonstration. Track **signed POs, accepted installed units, paid active hours, and renewals** separately.

Unitree’s publicly advertised entry prices ($13,500 for G1, $4,900 for R1) are **NOT** evidence of delivered ASP, BOM, profit, unit sales or recurring service attach. Company/private financials remain unknown.

---

## 3. What the public financials show (and do not show)

### Income-quality analysis

| Public source | Positive signal | Required caveat |
|---|---|---|
| NVIDIA FY27 Q2 GAAP gross margin **75%** | Strong disclosed economics in its own mix | GPU vendor mix ≠ fleet operator's unit gross profit |
| AMD Q2 2026 GAAP gross margin **54%** | Alternative accelerator ecosystem with traction | Group margin blends segment types |
| Vertiv Q2 2026 operating profit **USD638m** on sales **USD3.274bn** | Supplier participation in datacenter investment | Profit realization ≠ outstanding site demand pipeline |
| CoreWeave Q2 2026 operating loss **USD49m** | Fast revenue growth can coexist with operating losses | Technology & Infrastructure USD1.507bn affects economic cost |
| UBTECH H1 2026 loss **RMB338.8m** | Humanoid revenue line is observable | Disclosed product/service revenue does not equal recurring autonomous work |

A market capitalization and EV/Revenue comp cannot responsibly be produced without same-date prices, diluted shares, net debt/leases and period/currency adjustments. For this reason the repository **does not invent a public trading-multiple table**. It instead includes deliberately synthetic **five-year operating scenarios** to test what matters.

---

## 4. Hypothetical case A: GPU infrastructure provider

### Definition

A fictional company deploys an expanding GPU fleet, bills customers by *realized* (not posted) GPU-hour, pays idle-rack electricity, site/variable-service costs, SG&A and fixed R&D. Capex includes new fleet plus maintenance refresh; capex cohorts are depreciated straight line. Unlevered cash flow subtracts cash taxes, capex and working capital, then applies a **terminal EV/EBITDA heuristic**. These assumptions are documented and editable in [scenario JSON](../data/scenarios.json).

### Five-year illustrative scenario outcomes (USD million)

| Case | 2030 revenue | 2030 EBITDA | Five-year modeled enterprise value | Interpretation |
|---|---:|---:|---:|---|
| Bear | **19.02** | **−0.82** | **−66.27** | Negative model EV = implied capital shortfall under imposed cash flows, **not** a negative traded stock price |
| Base | **73.68** | **41.37** | **87.76** | Positive modeled EV, but concentration in terminal assumptions / site execution |
| Bull | **177.23** | **122.57** | **552.70** | Extremely sensitive to sustained realization of high utilization and GPU-hour price |

**Interpretation:** In model base, buildout is cash intensive; the terminal multiple, working capital and cost of capital are central to value. The **size of the spread is the thesis**, not a point target. This range is **not a confidence interval** and the cases have no empirically estimated probabilities.

**Analyst-proposed gates** for advancing an actual target:

1. Collected/billable GPU utilization, by vintage, materially above a documented break-even threshold and supported by contract data.
2. P95 latency, error rate and SLA measured on a production workload at the *realized price*, not publicly posted cloud list rates.
3. Signed utility/colo rights with commissioning evidence and quantified total rack expenses.
4. Fleet refresh, depreciation policy and covenant compliance survive a 25% realized price decline and multi-quarter capacity ramp delay.
5. No single customer concentration or financing cliff creates a likely distress outcome on plausible downside.

### Diligence red flags

Publicized GPUs without site energization, 100%-paid utilization implied by booking count, contractual GPU hours counted before service acceptance, gross margin calculated before tech/infra depreciation, broad “AI market is growing” answers to customer concentration.

---

## 5. Hypothetical case B: humanoid OEM + paid service contracts

### Definition

A second **fictional** company sells robots at scenario ASP, incurs scenario hardware BOM, warranty and SG&A, and sells annual services to an assumed fraction of the average installed base. It invests in R&D and factory capex. Its exit value is a **terminal EV/Revenue heuristic** because the early-stage EBITDA can remain negative.

This modeled product/pricing path **is not** Unitree/UBTECH product margin or sales guidance. Especially, no IFR shipment number is plugged into this company's revenue.

### Five-year illustrative scenario outcomes (USD million)

| Case | 2030 revenue | 2030 EBITDA | Five-year modeled enterprise value | Interpretation |
|---|---:|---:|---:|---|
| Bear | **39.52** | **−12.30** | **−17.95** | Warranty, low attach and thin ASP-BOM spread fail to sustain investment |
| Base | **137.03** | **7.36** | **52.16** | Modest terminal-year profit; capitalization depends on volume, attach and multiple |
| Bull | **283.69** | **59.59** | **279.64** | Scale and ASP/BOM improvement assume material execution that cannot be validated from public quotes |

**Analyst-proposed gates** for an actual robot OEM:

1. >=2 real enterprise deployments pass an independent 90-day workflow test with paid invoices, customer acceptance and post-pilot renewals (these thresholds are *our* screen).
2. Operators report task outcomes, not only motion demos; autonomous vs teleoperated hours are audited separately.
3. Site-specific robot labor savings remain positive after human supervision, batteries, repairs, insurance, spare parts and downtime.
4. Actual delivered hardware ASP minus sourced BOM, yield loss, freight, warranty and field operations can be reconciled to audited unit economics.
5. Safety and use permits are obtainable and support large deployments beyond one cherry-picked environment.

Do **not** infer product price, robotics revenue or segment margin by dividing UBTECH's products-plus-services revenue by a partial unit count or treating Unitree's online prices as industry ASP.

---

## 6. Sensitivity, downside protection and scenario design

### Why the spread matters

Five-year discounted valuations compound uncertain near-term construction / production volume, customer contracts, model quality, cost declines and discount rate. Even a modest percentage change in realized price or task attach can change terminal operating economics and present value considerably.

This repo generates **25-cell compute sensitivity** (five price multipliers × five utilization levels) and **25-cell robotics sensitivity** (five hardware ASP multipliers × five service attach levels), keeping the other scenario assumptions fixed. See [offline dashboard](../reports/index.html) after running `python3 run.py`.

### Things the model deliberately excludes

- Debt schedules/interest expense, secured vs unsecured financing, repayment covenants.
- Customer payments timing and detailed AR aging; *working capital is a simple percent-of-revenue approximation*.
- GPU resale/salvage value, contract penalties, fleet retirement schedules, tax loss carryforwards, warranty claim uncertainty, license fees and bespoke leasing accounting.
- Robotics fleet attrition or replacements (no attrition is optimistic).
- IFRS vs US GAAP reconciliation and market-level valuation multiples.

These are not cosmetic gaps; they can reverse an investment conclusion.

### Pricing pressure stress

At the same GPU fleet, a lower realized hourly price affects revenue almost directly while significant power/lease/site costs remain. Power constraints are a bottleneck but also raise costs. A new GPU cloud is not an automatic winner just because the market uses more electricity.

At the same robot unit count, lower ASP with unaltered BOM can erase hardware contribution; service attach may take years and some deployments may fail to renew.

---

## 7. Competitive defensibility and trade-offs

**Software/runtime advantage** is easier to scale but can be competed away by open source. Tests need *cost per quality-compliant token* and sustained advantage across model versions. An engineer can optimize RMSNorm or attention, but unless it changes an actual customer's cost structure the investability is limited.

**Infrastructure access** may be defensible through power and site rights but requires financing and time. Reliable long-term contracts and secured interconnection produce real options while locked-in old hardware can destroy flexibility.

**Robotics hardware cost leadership** is valuable in pilot procurement but insufficient for autonomous task ROI. Dataset/network effects depend on whether robot builders legally own reusable in-field task data and can improve reliability without huge teleoperation spend.

**Investment stance by sub-sector** (hypothesis, not recommendation on securities):

- GPU rental pure-play, heavily financed: *conditional watch*, require stress-tested unit returns and debt.
- Power/cooling enablement: *diligence priority*, tied to verified backlog conversion and recurring maintenance.
- Serving/orchestration software: *diligence priority*, test defensible production performance and customer retention.
- Humanoid OEM mass general-purpose narrative: *watch, elevated execution risk*.
- Narrow-scope deployment integrator with positive accepted task ROI: *priority for case-specific diligence*.

---

## 8. Risk register and mitigations

| Risk | Severity (analyst) | Leading indicator | Mitigation / falsification |
|---|---|---|---|
| GPU hourly-price compression | Critical | Discounted realized ASP vs cohort costs | Stress price down 25%, compare reserved vs spot contract terms |
| Underutilized deployed fleet | Critical | Paid GPU hours / all powered GPU hours | Require billing/collections reconciliation; inspect idle energy |
| Debt and customer concentration | Critical | Single-customer concentration and maturity wall | Covenant stress, refinancing timeline, contract collectability |
| Electrical/thermal bottleneck | High | Site energization delayed, PUE divergence | Commissioning docs and verified utility contracts |
| Rapid hardware obsolescence | High | Used-GPU resale and refresh demand | Cohort liquidation stress, depreciation reality |
| Robot demos without paid autonomy | Critical | Intervention logs and repeat customers absent | Independent task benchmark with billed labor savings |
| Hardware safety / warranty | High | Field failures, recalls, injury incidents | Accelerated endurance, insurer and regulator evidence |
| Ambiguous market statistics | High | IFR and other shipment categories mixed | Explicit category definitions; don't chain noncomparable series |
| Accounting/FX mismatch | High | Mix GAAP vs adjusted or USD vs RMB | Same-period sources, reconciliation, separate units |
| Market multiple arbitrariness | Critical | Valuation changes drastically by exit multiple | Show sensitivity, refuse precise price target |

No probability weights are assigned to this register because target-company operational data are not available.

---

## 9. Investment committee decision and diligence budget

### Current decision: WATCH / APPROVE FOLLOW-UP DILIGENCE ONLY

**Do not execute capital allocation.** The public facts show opportunity, but neither target-company finances nor contractual/technical proof have been provided. Commission:

1. **Week of diligence 1**: management interviews; actual P&L, net debt, customer contracts, billings and deployment logs.
2. **Week of diligence 2**: engineer-owned GPU performance/cost trial and robot real-task evaluation with unaltered holdouts.
3. **Week of diligence 3**: re-run scenarios using invoices, costs, capex cohorts, contract terms and risk-adjusted discount/exit assumptions.
4. **IC gate**: approve, request price protections and more data, or decline if cash and control rights do not meet hurdle.

### Kill conditions

- Refusal to disclose baseline cost and transaction data under appropriate NDA.
- AI rental reported margins fail to include major infrastructure costs.
- Robot customer economics are negative after supervision or safety compliance.
- Management cannot reproduce headline metrics; repeated discrepancies between physical deployment and financial recognized revenue.
- Deal requires implausible exit multiple or endless cheap financing to work in the base case.

### What would change our mind?

For infrastructure: audited customer receipts and power invoices show competitive **contribution margin after refresh** across two hardware vintages, with resilient cash flow under lower hourly rates.

For robotics: multiple paying sites sustain autonomous task throughput and accepted savings, with warranty/field-service expenses fully burdened and stable retention.

---

## 10. Valuation discipline and sources

This memo contains **no share-price targets**, no claims about Unitree's audited margins or number of funded customers, and no fake public traded EV multiples. The two models are genuinely executable but educational. Their primary purpose is to demonstrate risk decomposition and quantify sensitivity to **clearly unverified assumptions**.

**Source register:** [data/evidence.csv](../data/evidence.csv). Dated filings include:

- [IEA 2026 Key Questions on Energy and AI](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary).
- [NVIDIA Q2 FY2027 release, Aug 26 2026](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/).
- [AMD Q2 2026 release, Aug 4 2026](https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results).
- [Vertiv Q2 2026 release, Jul 29 2026](https://investors.vertiv.com/news/news-details/2026/Vertiv-Reports-Strong-Second-Quarter-2026-with-Diluted-EPS-Growth-of-53-Adjusted-Diluted-EPS-Growth-of-60-Raises-Full-Year-2026-Guidance-Across-All-Key-Metrics/default.aspx).
- [CoreWeave Q2 2026 release](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx).
- [UBTECH 2026 interim disclosure index](https://www.ubtrobot.com/en/announce) with data cross-checked against [filing text mirror](https://financialfilings.com/filings/ubtech-robotics-corp-ltd/interim-quarterly-report/2026/61290635/).
- [IFR 2026 humanoid robot scope](https://ifr.org/ifr-press-releases/news/robotics-1).
- [Unitree manufacturer shop listing](https://shop.unitree.com/collections/humanoid-robot).

**Recommendation:** Maintain a **watchlist; do not invest on this packet alone**. Use the technology experiments and required evidence list to turn hypotheses into verifiable underwriting.

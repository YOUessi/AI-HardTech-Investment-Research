# 02 — Comparable business models, not a comparable valuation multiple

**Data cutoff: 2026-10-27.** Review [data/comparables.csv](../data/comparables.csv) and [data/evidence.csv](../data/evidence.csv).

## 1. Public-company data points

| Company / segment type | Dated disclosure | Reported revenue | Operating income/loss | Qualifier |
|---|---|---:|---:|---|
| NVIDIA — GPU platforms | FY2027 Q2 ended 2026-07-26 | **USD96,221m** | **USD63,734m** | Chip/network/software mix, GAAP [NV-FY27-Q2-REV, NV-FY27-Q2-OP] |
| AMD — CPU/GPU supplier | Q2 2026 ended 2026-06-27 | **USD11,536m** | **USD1,990m** | GAAP; Data Center is ~USD6.7bn, not all revenue [AMD-2026Q2-REV, AMD-2026Q2-DC] |
| Vertiv — power/cooling | Q2 2026 ended 2026-06-30 | **USD3,274.3m** | **USD638m** | GAAP op profit; adjusted op profit differs [VRT-2026Q2-SALES, VRT-2026Q2-OP] |
| CoreWeave — GPU cloud | Q2 2026 ended 2026-06-30 | **USD2,575m** | **USD−49m** | Extra infrastructure expenses **USD1,507m** need attention [CW-2026Q2-REV, CW-2026Q2-OP, CW-2026Q2-INFRA] |
| UBTECH — robots/services | H1 2026 ended 2026-06-30 | **RMB1,269.130m** | **RMB−279.093m** | 6 months, unaudited RMB [UBT-H1-REV, UBT-H1-OP] |

Income statement ratios, where computable, are in the generated dashboard; **no public market capitalizations are used** because real-time market price, date-aligned outstanding shares and diluted net debt have not been established.

NVIDIA's disclosed gross margin **75%** (GAAP); AMD's **54%**; UBTECH overall **44.7%**. A gross margin on GPU silicon, data-center equipment, GPU rental and mixed hardware/services is **not a directly comparable unit margin**.

## 2. Investment mechanics by company

### NVIDIA (NVDA)

- **Economic role:** GPU acceleration, software ecosystem, rack/network solutions. The Data Center business had approximately USD89bn in Q2 FY2027 revenue [NV-FY27-Q2-DC].
- **Bull:** accelerated inference workloads and software/networking content sustain platform-level scarcity and system margins.
- **Bear:** advanced rivals, customers' internal chips, export controls and pricing pressure compress economics despite high demand.
- **Diligence:** measure throughput and *supported workload* performance per dollar; model CUDA ecosystem switching costs and deployment frictions.
- **Do not infer:** posted platform product specs imply end-user software AI startup pricing.

### AMD (AMD)

- **Economic role:** alternative compute vendor, EPYC and Instinct portfolio. Q2 2026 Data Center revenue rounded to USD6.7bn [AMD-2026Q2-DC].
- **Bull:** supply diversification and open software demand expand share.
- **Bear:** tooling gaps, integration/driver cost and vendor-specific workload optimization reduce realizable TCO advantage.
- **Diligence:** run matched inference workloads with software stack parity, hardware availability and deployment labor included.
- **Do not infer:** aggregate company gross margin implies accelerator margin.

### Vertiv (VRT)

- **Economic role:** power and thermal infrastructure; monetizes hardware + installations + services, not GPU runtime directly.
- **Bull:** time-to-power bottlenecks and high rack density favor technical specialists.
- **Bear:** site delays and customer capex reductions hit cash conversion and backlog realization.
- **Diligence:** backlog-to-revenue cycle, component constraints, warranty and service attach; energy efficiency and installation time.
- **Do not infer:** TWh demand implies fixed cooling vendor market share.

### CoreWeave (CRWV)

- **Economic role:** GPU cloud and dedicated compute infrastructure, high fixed capital intensity.
- **Bull:** contracted utilization and financial structuring yield strong revenue per installed rack.
- **Bear:** debt/refinancing, procurement dependency and fleet obsolescence offset demand.
- **Diligence:** contracted vs collected GPU hours, take-or-pay guarantees, downtime penalties, cohort useful lives, collateral and power costs.
- **Accounting caution:** CoreWeave Q2 2026 shows USD879m cost of revenue plus **USD1,507m technology and infrastructure costs** below that line. Do not take USD(2575−879)/2575 as all-in rental economics [CW-2026Q2-INFRA].

### Unitree (private)

- **Economic role:** low entry price humanoid and quadruped platforms plus components.
- **Verified:** official shop *from* USD13,500 G1; *from* USD4,900 R1 [UNITREE-G1-PRICE, UNITREE-R1-PRICE].
- **Unknown from checked sources:** verified quarterly P&L, net debt, gross margin, cash burn, customer concentration and serial-number sell-through. **Not filled in.**
- **Diligence:** manufacturing yield, electronics/actuator BOM, paid repeat deployments vs educational/research usage, in-field warranty and safety.

### UBTECH (9880.HK)

- **Economic role:** diversified humanoid, education and related robotic products and services.
- **Verified H1 2026:** revenue RMB1,269.1m; humanoid products and services RMB590.3m; reported net loss RMB338.8m [UBT-H1-REV, UBT-H1-HUM, UBT-H1-NET].
- **Critical caveat:** categories include products *and services*, while category-level delivery numbers do not create a public fixed ASP for each model.
- **Diligence:** H1 segment GM, industrial customer contract acceptance, receivables quality, field-maintenance spending, B2B conversion and humanoid share of recurring revenues.

## 3. What an actual relative valuation would require

Do **not** insert fabricated EV/Revenue multiples. First collect, for the **same exact observation date**:

1. Closing price and fully diluted shares / treasury shares / equity claims.
2. Cash and **all** relevant interest-bearing debt, capitalized leases where applicable, minority interests, cash restrictions.
3. Trailing twelve-month revenue and EBITDA under reconciled GAAP/IFRS definitions, with segment restatements accounted for.
4. Fiscal-year alignment and currency conversion with dated FX source; beware stale price vs latest filing.
5. Adjustments for recurring services vs capital intensity, customer concentration and growth/quality of earnings.

Even a date-aligned public-company multiple should not be blindly applied to an unaudited private robot or GPU rental business.

## 4. Relative technical-economic comparison (analyst questions)

| Criterion | GPU IP vendor | GPU cloud | Power/cooling | Robot OEM |
|---|---|---|---|---|
| Main moat | Software ecosystem / HW efficiency | Power + allocation + utilization | Site design + install + service | BOM + reliability + data + software |
| Main capex | R&D + supply ecosystem | Hardware and facilities | Plant + working capital | Tooling, supply chain, training |
| Price variable | Chip / rack ASP | Billed GPU-hour | Contract/project ASP | ASP / RaaS/service attach |
| Main margin trap | Customer custom ASIC substitutes | Idle fleet and borrowed capital | Orders not converted | Warranty and field support |
| Test for defensibility | Throughput/$ matched workload | FCF by GPU vintage | Project delivery cash conversion | Human intervention per task / accepted hours |

**Conclusion:** A sector-driven portfolio process should use **separate cost economics and distinct risk premia** by business model. The scenario models in this repository are *illustrative fictional targets* and deliberately avoid public trading multiple claims.

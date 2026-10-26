# 01 — Industry map: where does value accrue?

**As-of:** 2026-10-27 · **Scope:** data-center inference infrastructure and full-size/other humanoid robots.
Numbers labelled [E#] refer to individual rows of [the evidence ledger](../data/evidence.csv). This report is *not* a price target or a declaration that any private company has an audited P&L.

## 1. Investment question and falsifiable hypotheses

We study two vertically adjacent, but **non-interchangeable**, capital-allocation problems.

- **Inference supply chain:** A model query creates demand for compute, connectivity, electricity and cooling. Hypothesis H-DC1: operators with power access, utilization management and reliable service-level guarantees may achieve durable gross-profit dollars per installed GPU *only if* excess supply does not erode realized GPU-hour pricing.
- **Physical AI supply chain:** A robotics demo creates demand for actuators, sensors, software and integrations. Hypothesis H-RB1: durable value accrues to suppliers or robot integrators that can show *productive* human-supervised operating hours and customer renewal, rather than showroom movements or nominal shipments.
- **Counter-thesis common to both:** efficiency gains, open-source competition, hardware commoditization, short lifetimes and expensive external finance can transfer value back to buyers, notwithstanding rapid top-line sector growth.

These are **analyst hypotheses**, not published company facts. They require management, customer and engineering validation.

## 2. AI inference value-chain map

| Position | Representative companies / technologies | Purchase decision | Potential moat | Typical failure |
|---|---|---|---|---|
| Silicon & packaging | NVIDIA, AMD, HBM suppliers | Performance, software ecosystem, supply guarantee | Kernels, compiler, software ecosystem, interconnect | Faster alternates, supply glut, export limits |
| Rack/server, network | OEMs, NIC/DPU, switches | Rack throughput, reliability, networking utilization | System validation, throughput-per-watt | Incompatibility, integration delays |
| Power, cooling, grid | Vertiv, utilities, liquid-cooling vendors | Time-to-power, uptime, rack density | Certification, install capability, installed base | Long lead times, project deferrals |
| GPU cloud | CoreWeave and emerging providers | Realized GPU-hour rates, SLA, location | Fleet access, scale, reserved power, customer relationships | Debt, hardware obsolescence, low utilization |
| Runtime & inference software | vLLM, SGLang, proprietary schedulers | Cost per accepted token at quality/latency constraint | Scheduling, kernel performance, model-specific optimization | Open-source convergence |
| Application + agents | Enterprise model providers | Verified tasks, reliability and data privacy | Workflow integration and proprietary outcomes | Vendor lock-in, low paid retention |

**2026 update:** IEA's *Key Questions on Energy and AI* estimates data-center electricity consumption at about **485 TWh in 2025** and central-case demand of **~950 TWh by 2030** [IEA-DC-2025, IEA-DC-2030]. These are energy forecasts, **not** direct estimates of GPU shipments, utilization, industry revenue, or an individual company's addressable serviceable market. IEA also highlights physical bottlenecks around power and chip supply. Source: https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary

### The value-capture question is harder than the total-addressable-market story

Power consumption can grow while equity returns disappoint. A GPU lessor has the following competing dynamics:

1. Price per billed GPU-hour can fall as capacity increases; billing discounts and reserved capacity contracts matter more than posted list prices.
2. Electrical cost is incurred when a powered GPU is idle (and racks incur residual platform overhead), while billed hours scale with *billable* utilization.
3. Hardware refresh, networking and site maintenance continue even if a customer cancels.
4. Tech & infrastructure expenses may appear in different income-statement lines. CoreWeave's Q2 2026 presentation reports both **cost of revenue USD879m** and **technology & infrastructure USD1,507m** [CW-2026Q2-INFRA]; dividing revenue less cost-of-revenue by revenue while ignoring the second line is economically misleading.
5. Getting grid interconnection and a liquid-cooled site ready is a distinct business from selling GPUs or running an efficient model runtime.

**Operational KPI that could matter more than ARR:** *contracted and collected* contribution per GPU-month after power, rack, depreciation and financing, with tail-latency/uptime penalties and useful tokens per dollar. This is an analyst proposal for management reporting, not a disclosed company metric.

## 3. Physical / humanoid robotics value-chain map

| Position | Components or capability | Economic control point | Verification |
|---|---|---|---|
| Actuation and transmission | Motors, reducers, joints, drivers | Reliability, BOM, manufacturing yield | Cycle life, fall/impact tests |
| Perception and edge compute | Cameras, depth, IMU, inference hardware | Robust tracking and low-power operation | Latency, lighting/occlusion testing |
| Motion/control | Whole-body controller, locomotion, manipulation | Domain generalization and safety | Fall-rate, slip, e-stop validation |
| Data and foundation policies | Teleoperation, action datasets, imitation/RL, VLA | Task coverage, training data feedback | Held-out tasks, human interventions |
| OEM/integrator | Unitree, UBTECH and competitors | Hardware supply, field service, deployment | Units *accepted* and customer paid use |
| Application integrator | Logistics, retail, inspection, manufacturing | Labor/throughput ROI | Controlled task trial, warranty & labor burden |

**Demand discipline:** IFR states that approximately **7,000 full-size humanoids for commercial/professional applications** were sold worldwide in **2025** [IFR-2025-HUM]. Counterpoint estimated **more than 22,000 humanoid shipments across a different market definition in H1 2026** [CP-2026H1-HUM]. These are *not a harmonized time series*; neither number should be silently extrapolated into the other. In particular, research, data collection, performance and demonstration units need not generate net labor savings.

**Manufacturer pricing is not earnings:** Unitree's official storefront lists G1 **from USD13,500** and R1 **from USD4,900** (checked 2026-10-27) [UNITREE-G1-PRICE, UNITREE-R1-PRICE]. These are entry prices, not measured transaction ASPs, COGS or Unitree's revenue.

**Company disclosure is a stronger anchor:** UBTECH's unaudited H1 2026 figures report **RMB1,269.1m** consolidated revenue and **RMB590.3m** from full-size embodied humanoid products and services [UBT-H1-REV, UBT-H1-HUM]; period net loss was **RMB338.8m** [UBT-H1-NET]. Product/service mix and delivery margins must be reconciled before claiming recurring unit economics.

## 4. Demand validation ladder

A line on a market-size slide is **not** a signed contract. Use sequential gates:

**Computing:** public capex announcement → secured site/electricity → received hardware → paying customer contract → billed and collected utilization → positive after-refresh contribution → financeable cash flow.

**Robotics:** media demo → paid evaluation → customer acceptance → repeat production deployment → autonomous labor/task savings after supervision → maintenance economics → renewals and recurring service revenue.

Skipping stages creates valuation risk.

## 5. Timing and metric definitions

- IEA's figures are **energy (TWh)** and are forecasts in 2030, not annual chip revenue.
- NVIDIA's **FY2027 Q2** ends July 26, 2026; **AMD Q2 2026** and **Vertiv Q2 2026** are different calendar periods. Different names do not imply date leakage.
- UBTECH reports **RMB** and **six-month H1 results**. USD quarter vs RMB half-year cannot be ranked without FX date, normalization and business-model controls.
- 2026 estimates, price quotes and market definitions carry publication or observation dates in the CSV.

## 6. What could disprove the thesis?

**Inference false:** utilization after discounts consistently below 45%; declines in billed price outpace efficiency; cash capex and interest exceed collections; availability breaches block customer renewals. Numbers are illustrative review thresholds, not reported market norms.

**Robotics false:** only teleoperated demos are paid, not autonomous use; customer-task value fails to cover service labor; warranty returns escalate; sell-through lags shipments; safety certification prevents scale.

**Power/cooling false:** orders are speculative, projects deferred, inventory accumulates, or alternative cooling designs lower addressable hardware content.

## Primary references

- [IEA 2026 demand and power constraints](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary)
- [IFR 2026 professional service and humanoid units](https://ifr.org/ifr-press-releases/global-sales-of-professional-service-robots-surge-24-percent)
- [Counterpoint H1 2026 market research](https://counterpointresearch.com/en/insights/global-humanoid-robot-shipments-soar-nearly-300-percent-yoy-in-h1-2026)
- [CoreWeave Q2 2026 financials](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000362/coreweave2q26earningspress.htm)
- [Unitree official store](https://shop.unitree.com/collections/humanoid-robot)

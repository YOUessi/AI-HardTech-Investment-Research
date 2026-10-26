# 03 — Engineering-led technical diligence and experimental protocols

**Scope:** verify a proposed GPU inference cloud or humanoid robot provider beyond a marketing demo. Every experiment has a null hypothesis, measurements, confounders, required artifacts and acceptance gate. Thresholds marked **analyst-proposed** are not sector statistics or company-reported outcomes.

## A. Compute provider / inference runtime

### A1. Performance and quality benchmark

**Question:** is vendor X truly cheaper per useful inference than alternatives at fixed model capability and reliability?

- **Input controls:** same checkpoint/tokenizer and quantization policy, workload (RAG/agentic, prefill/decode), prompt lengths 256 / 2,048 / 8,192 tokens, output 128 / 512, concurrency 1 / 8 / 32 / 64, warm-up and batch policy.
- **Comparators:** incumbent environment baseline (e.g., existing GPU cloud), candidate GPU cloud, and same runtime tuning if executable.
- **Metrics:** output accuracy/format success at deterministic seed or sampling config; TTFT median/P95, TPOT median/P95, goodput tokens/sec, uptime, queuing time, cost per *accepted* 1m tokens. Include failure and throttling logs.
- **Reject benchmark** if models or context lengths differ; if 5-minute peak throughput is compared to multi-hour p95; if cost excludes CPU, networking or uptime.
- **Artifacts:** script, configuration, input hashes, raw JSON trace, code version/driver/CUDA, provider prices with as-of dates, percentile calculation.
- **Pass gate (analyst-proposed):** at least a 15% cost-per-useful-token advantage with no worse than 5% P95 tail regression on two held-out workloads and no loss of answer success rate. This is a screening target, not proof of competitive moat.

### A2. GPU utilization and pricing diligence

Sample across >=4 customer cohorts and GPU vintages and request:

1. Total installed fleet, usable/powered GPU hours, **billable and collected** hours, reserved but idle contracted hours.
2. Contract minimums/discounts, spot-price mix, credits, overages, penalties, service availability credits.
3. Electricity price and PUE measured at rack/site—not nameplate; site lease, network/egress, HVAC, staffing.
4. Lifetime, replacement roadmap, stranded old GPUs; maintenance inventory and refresh timing.
5. Financing rates, collateral, covenants, customer concentration and take-or-pay commitments.

**Basic audit identity:** billed GPU hours <= available GPU hours; collected invoice dollars <= gross invoice dollars (ignoring prior-period receivables); realized price = recognized billings / billed hours under declared revenue recognition and credits.

**Critical counter-case:** apply 25% lower GPU-hour realization, 15 pp utilization decline, +4 pp discount rate or +US$0.05/kWh; compare EV and cumulative cash burn to base. The published scenario sensitivity does a subset; it is not calibrated to named companies.

### A3. CUDA/kernel and scheduler evaluation

- Test throughput and latency with hardware topology fixed. Report prefill/decode separately.
- Profile SM utilization, HBM read/write bandwidth, launch overhead, collective latency, PCIe/NVLink and context-cache hit rate.
- Kernel optimizations are **non-evidence** of provider-scale differentiation if kernel does not appear in their production model workloads, or suffers a different bottleneck.
- Compare vLLM scheduling and KV caching while measuring *correctness* and p95 costs; report model quantization and batch.
- Randomize order to avoid clock/thermal drift; monitor GPU clocks/power and failure retries.
- Record **peak/median/P95, mean +/- uncertainty and distributions**, not a single best benchmark.

## B. Data center physical due diligence

| Question | Requested evidence | Why it matters |
|---|---|---|
| Is grid power contracted and deliverable? | Signed interconnection, milestones, energization certificate | MW pipeline is not usable capacity |
| Can high-density racks be cooled? | Commissioning results, coolant supply, thermal testing | Unmet density lowers rentable fleet |
| Is there a backup and failover plan? | Black-start tests, UPS, insurance, RTO/RPO | SLA penalties and customer churn |
| Are lead times and vendors diversified? | Actual POs, delivery history, component bottleneck map | Project slippage impacts modeled revenue |
| What is full-site TCO? | Electric invoices, PUE, lease, cooling, maintenance | Posted GPU price is not profitability |

## C. Humanoid robot diligence

### C1. Paid task evaluation

**Hypothesis:** robot autonomy lowers total cost of a **specific named workflow** vs incumbent labor/automation when interventions, safety and maintenance are included.

- Define task before test: e.g. pick-move-place on shelf bins with 20 SKU types, 4 lighting conditions, 3 surface types; do not cherry-pick staged clips.
- Demand receipts: PO, site acceptance test, paid invoice, duty cycle, operator staffing, SLA and maintenance logs.
- Run randomized held-out configurations without teleoperator intervention. Allow e-stop but count every intervention.
- Metrics: successful tasks/hour, human minutes per 100 robot hours, system availability, safety stop rate, damaging collisions, recharge duty cycle, MTTF, mean time to repair, battery/actuator replacement.
- Financial KPI: annual task contribution after all onsite supervision, lease/rental, maintenance, training time and customer process changes, rather than headline robot ASP alone.
- Analyst-proposed screen (must be adapted to use case): >=90% task completion, <=2 human interventions per 100 robot hours, no safety-critical collision in test, <24 months payback under conservative local labor costs. None of these are verified industry averages.

### C2. Motion and autonomy reliability

- **Locomotion:** measure fall rate and slip over many randomized trajectories, locomotion tracking error and energy per distance.
- **Manipulation:** held-out objects, occlusions, changes in grip, hand orientation, handoffs and object damage.
- **Sim2Real:** randomize friction, mass, payload, sensor noise and lighting; explicitly compare after-deployment failure rates.
- **VLA / language condition:** true generalization across unseen instructions and object combinations; do not count deterministic scene scripts as language-conditioned autonomy.
- **Operator:** audit full vs partial teleoperation and whether field logs agree with product marketing.

### C3. Hardware & unit economics

Request customer-level delivered ASP, BOM by supplier/volume, manufacturing yield/rework, shipping/import/tax, service contract, software support, actuator/battery warranty, spare parts and return allowances.

**Reject** logic of deriving Unitree's corporate revenue by multiplying an online entry price by unrelated industry-wide humanoid shipment estimates.

## D. Competitive ecosystem and legal constraints

- Licensing and IP: ownership of models, dataset licenses, robot teleoperation data, third-party firmware and kernel code.
- Safety and cybersecurity: PII/camera recording, prompt/tool injection in physical agents, safety certifications, emergency stop responsibilities and insurance claims.
- Export control and regional dependencies: GPU supply, chip packages, robotic component sourcing, regional cloud/data laws.
- Procurement: demand quality, related-party sales, government pilots vs repeat private-sector customers.

## E. Minimum evidence request packet for target management

1. Non-redacted unit economic calculations for two 6-month cohorts.
2. Inventory/installed asset reconciliation and cost basis, impairments and repair schedules.
3. Booked, delivered, accepted, invoiced, collected revenues by major customer.
4. Product uptime and incident logs with clear denominators.
5. Vendor concentration and renewal / contract-term ledger.
6. Audited or reviewed financial statements and capitalization table.
7. Holdout experiment data and raw logs from agreed production settings.
8. IP ownership, open-source obligations and safety/legal attestations.

### Grading

- **RED:** source documents withheld; insufficient denominators; off-line demo only; negative cash contribution under contracts; hidden teleoperation.
- **AMBER:** partial records, growing traction, but no 12-month repeat economics or cost by hardware vintage.
- **GREEN:** reproducible production KPIs, sufficient signed customer contracts, verified cash economics and acceptable downside terms. Green is diligence passage, not investment approval.

> **What this repository does not claim:** it did not access confidential invoices, proprietary models, robot logs, customer agreements, real-time power tariffs or live financing terms. This is an evidence-checklist and analytic-model prototype, not a completed proprietary technical audit.

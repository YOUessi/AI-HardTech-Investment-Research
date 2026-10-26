# 06 — IC challenge questions, follow-up requests, and decision gates

**As-of:** 2026-10-27. Prepared for simulated venture investment interviews. Question labels allow tracking receipts, source grade, owner and blocking status.

## A. GPU cloud / infrastructure management

| ID | Challenge question | Required evidence | Consequence if missing |
|---|---|---|---|
| INF-01 | Of the advertised GPUs, what proportion were powered, provisioned, billed and paid for in each of the last 6 months? | Fleet by vintage, metered hours, invoices, cash receipts | No reliable utilization or revenue per installed GPU |
| INF-02 | What is per-rack power/cooling total cost by site and SKU? | Electricity and PUE logs, racks, leases, customer credits | COGS assumption not underwritable |
| INF-03 | Which customer contracts are binding take-or-pay and what are credits/exit rights? | Redacted signed contracts, AR aging | Demand may be uncollectable |
| INF-04 | How much debt is secured by GPUs and when are maturities/refinancings? | Debt agreements, collateral reports, covenant tests | Exit equity could be eliminated |
| INF-05 | How do your best workloads perform at matched accuracy and P95 latency against real competitor pricing? | Raw traces, independent code, same checkpoint | 'Performance lead' unproven |
| INF-06 | How much capital must be replaced during 36 months and can it be financed under bear pricing? | Procurement terms, vintage impairment and refresh schedule | Gross margin decoupled from ROIC |
| INF-07 | What onsite MW are energized versus pipeline marketing MW? | Grid agreements, permits, energization and test certificates | Model volume cannot be deployed |
| INF-08 | How do you account for technology/infrastructure expenses and capital leases? | Full GAAP financial statement and segment reconciliation | Misstated rental economics |

**Decision gate:** INF-01–04 and INF-07 are P0 diligence blockers; do not approve investment before redacted source proof. INF-05/06/08 require technical/accounting verification.

## B. Humanoid OEM / integrator management

| ID | Challenge question | Required evidence | Consequence if missing |
|---|---|---|---|
| ROB-01 | What percentage of shipped robots were accepted, paid and used in field tasks? | Shipped/installed/accepted invoices by customer | Shipments cannot be equated with usage |
| ROB-02 | What fraction of active time requires human teleoperation or reset? | Signed field logs and independent observation | Autonomy claims unreliable |
| ROB-03 | What specific customer tasks save cost after onsite labor, repairs and downtime? | Before/after process economics and staffing records | ROI case speculative |
| ROB-04 | How do ASP, BOM, warranty and field-service costs reconcile? | Invoices, BOM, return provisions, repair tickets | Hardware contribution unknown |
| ROB-05 | Is data capture consented/licensed, and can policy updates use that data? | Privacy, customer data and model IP contracts | Foundation-model moat may not exist |
| ROB-06 | What are field failure rates by actuator/battery vintage? | RMA and on-site uptime, safety logs | Lifetime value and scale uncertain |
| ROB-07 | Which repeat contracts extend beyond a government demo or university lab? | PO renewals, customer cohort retention | Paid adoption not established |
| ROB-08 | Who is liable after a safety incident or floor damage? | Compliance files, insurer and field SLAs | Unbounded downside |

**Decision gate:** ROB-01–04 and ROB-08 are P0 diligence blockers; ROB-05–07 require strong evidence before pricing recurring network effects into the model.

## C. Cross-functional investment committee

1. **What is the counterfactual?** Why buy this target rather than a public equipment supplier, internally build or delay commitment?
2. **What would make us wrong?** Identify the two fastest invalidating metrics and when we can observe them.
3. **Are we comparing gross and operating profits on matching periods?** If not, explain in writing.
4. **What is the true capital structure?** Preferred liquidation preference, debt, SAFEs/options, warrants, dilution and vendor financing.
5. **Is the entry valuation supported without multiple expansion?** Test flat and declining exit multiple assumptions.
6. **Which metric is contractually real?** Bookings, deployment, acceptance, invoiced revenue, collections, recurring revenue and usable cash are different.
7. **What customer is independent?** Related-party transactions, government grants, one-time trials and round-trip procurement must be separated.
8. **What can source data not establish?** Market forecasts, launch demos and model training benchmarks cannot certify customer cashflows.

## D. Expert interview guide (technical versus commercial)

**Technical expert / infrastructure:** Which workloads make model serving bottlenecked by memory, compute or networking, and how does hardware mix change tokens per dollar? Which production metrics can we reproduce without privileged data?

**Site engineer:** What grid power is approved today, and what are the worst load-shedding / PUE / coolant failure events? How quickly can we energize a new rack?

**Robot integrator / safety engineer:** How frequently does a robot require resets or teleoperation per customer task? How does reliability change across surfaces, payloads and lighting?

**Customer procurement:** Why did you pay for the trial, and what does a 12-month expansion decision depend on? Which human roles were *actually* eliminated or redeployed?

**Finance controller:** Can we reconcile CAPEX, recognized product/service revenue, invoice cash, hardware inventory and warranty liabilities?

## E. Sources still needed before investment authorization

- [ ] Reviewed/audited private target balance sheet and income statements.
- [ ] Actual fleet/device cohort asset ledger with depreciation, replacements, repairs.
- [ ] Detailed signed contracts and customer-level collected payment sample.
- [ ] PUE, electric invoices, site energization and maintenance schedule.
- [ ] SKU-level robot BOM, sold units, service attach/attrition, autonomy logs.
- [ ] Debt/capitalization terms and liquidation-preference waterfall.
- [ ] Independence-verified production performance tests.
- [ ] Legally cleared IP/model/data ownership and insurance/safety assessment.

## F. Conclusion grading (not a substitute for underwriting)

| Grade | Findings | Action |
|---|---|---|
| RED | Critical missing receipts, economically negative cohorts, hidden teleoperation or non-reconciled accounts | Reject or defer pending hard proof |
| AMBER | Positive pilot traction but limited useful work history or cash-flow durability | Request conditional experiment + terms protection |
| GREEN | Independently reproduced engineering and sustainable cash economics, no P0 blocker | Return to IC for pricing/terms, **not automatic investment** |

## G. Job-application deliverables

- **Hillhouse hard-tech / venture:** 10-minute IC defense of the two theses, the 2×3 scenario table, source uncertainty and a reasoned 'watch' decision.
- **VC platform/operations:** GPU capacity/power sourcing and fleet utilization metrics to track (operating metrics + counterparty risks).
- **Finance/incubator analyst:** identical-time financial comps, operating model, downside cash burn, uncertainty and due-diligence data request.
- **AI technical investment research:** isolate what a CUDA speedup, robot VLA demo or benchmark does *and does not* prove for cash returns.

Everything in this file is a study/diligence protocol; no interviews or private-data audits have been claimed.

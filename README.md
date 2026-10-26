# AI & Hard-Tech Investment Research

> Research as-of **2026-10-27** · A reproducible technical-diligence and scenario-modeling project, not investment advice.

This repository is an **investment-research exercise** for the type of work done by technology venture investors, infrastructure diligence teams, and financial incubator analysts. It studies **AI inference infrastructure** and **humanoid robotics** through dated public disclosures, technical due diligence, transparent assumptions, and reproducible valuation models.

## Research question

**Where does sustainable value accrue when AI inference demand expands, and when can humanoid robotics turn pilot demand into repeatable unit economics?**

The project deliberately separates *industry facts*, *technical hypotheses*, *hypothetical private-company assumptions*, and *analyst conclusions*. It does **not** assign fabricated revenue, margins, contracts, cap tables, or valuations to private robotics companies.

## Key dated public anchors

| Anchor | Reported metric | Scope / warning |
|---|---:|---|
| IEA, 2026 *Key Questions on Energy and AI* | Data-center energy **485 TWh in 2025**, base forecast **~950 TWh in 2030** | Forecast, not revenue or guaranteed construction |
| NVIDIA, 2026-08-26 | FY27 Q2 revenue **$96,221m**, Data Center **~$89,000m** | Fiscal quarter ended 2026-07-26 |
| AMD, 2026-08-04 | Q2 2026 revenue **$11,536m**, Data Center **~$6,700m** | Calendar-quarter basis |
| Vertiv, 2026-07-29 | Q2 2026 net sales **$3,274.3m** | Equipment + services; not comparable to GPU cloud revenue |
| CoreWeave, 2026-08 | Q2 2026 revenue **$2,575m**, operating loss **$49m** | Its Technology & Infrastructure line is material; don't use gross margin in isolation |
| UBTECH, 2026-09 interim report | H1 2026 revenue **RMB1,269.1m**, period loss **RMB338.8m** | 6-month unaudited financials in RMB |
| IFR, 2026 World Robotics | About **7,000** full-size humanoids sold for professional/commercial purposes in 2025 | Not the same coverage as later broad 'humanoid shipments' surveys |
| Unitree official shop, accessed 2026-10-27 | G1 **from $13,500**; R1 **from $4,900** | Advertised starting prices, not ASP, BOM, realized margin or deliveries |

Full URLs, periods, reported/forecast types and caveats: [data/evidence.csv](data/evidence.csv). Any model inputs under `data/scenarios.json` are *made-up instructional scenarios* and are **not estimates of a named company**.

## Artifacts

- [Sector map](research/01_sector_map.md) — value chain, bottlenecks, market-definition traps.
- [Company comparison](research/02_company_comparison.md) — NVIDIA, AMD, Vertiv, CoreWeave, Unitree, UBTECH.
- [Technical diligence](research/03_technical_diligence.md) — verification experiments, GPU economics and robotics reality checks.
- [Investment committee memo](research/04_investment_memo.md) — thesis, counter-thesis, catalysts, valuation and conditional recommendation.
- [Financial/accounting methodology](research/05_methodology.md) — scenario formulas, warnings and time/currency discipline.
- [IC questions and evidence requests](research/06_ic_questions.md) — structured follow-up interviews and gating.
- [Source ledger](data/evidence.csv) and [public period comparables](data/comparables.csv).
- [Scenario assumptions](data/scenarios.json) — separate compute-provider and hypothetical robotics OEM models.
- `src/investment_lab/model.py` — pure-stdlib, deterministic financial models and scenario sensitivity.
- `run.py` — build CSV/JSON/HTML outputs under `reports/`.
- `tests/` — unit/financial-invariant tests.

## Reproduce (Python 3.9+; no third-party dependencies)

```bash
git clone https://github.com/YOUessi/AI-HardTech-Investment-Research.git
cd AI-HardTech-Investment-Research
python3 -m unittest discover -s tests -v
python3 run.py
open reports/index.html  # macOS; open this file in a browser elsewhere
```

Outputs include multi-scenario 5-year projections, two distinct enterprise-value ranges, explicit financial formulas, price/utilization sensitivities and an offline browser dashboard.

## How to read the valuations

1. **Do not interpret** a synthetic scenario price as a target for NVIDIA, CoreWeave, UBTECH, or Unitree.
2. Infrastructure: modeled GPU fleet, utilization, realized price, idle power, electricity, site cost, variable software cost, cash SG&A/R&D, capex, depreciation, working capital, and taxes. Explicit UFCF and discounted terminal **EV/EBITDA** proxy.
3. Robotics: annual shipments, hardware ASP/BOM, warranty, service attach, recurring revenue, expenses, capex and working capital. Terminal **EV/Revenue** proxy (flagged as high-uncertainty early-stage assumption).
4. Every financial comparison retains currency, period length, accounting basis and source IDs.
5. Investor conclusions are **conditional** on verified contracts, funding, margins, GPU cost schedule and paid production robot deployments.

## Outcome and reproducibility checklist

- [x] Dated public evidence with origin/caveat
- [x] Technical diligence experiment plan with pass/fail criteria
- [x] Industry and representative-company comparison
- [x] Three compute and three robotics cases, with scenario inputs and sensitivity
- [x] Investment memo, risk register, counter-thesis, IC Q&A
- [x] Deterministic local tests and generated browser report
- [ ] Confidential company financial verification or management interview (**not available from public research**)
- [ ] Audited funding and customer contracts for private targets (**not available from public research**)
- [ ] Real-money transaction or live stock-price valuation (**not performed**)

## Working conventions

- All observed figures are sourced with an **as-of date**, explicit units and original reporting period.
- Formulas and assumptions are editable; example valuations must not be represented as observed company valuations.
- Negative / failed findings are preserved rather than rewritten as successes.
- New research goes into the source ledger and documents first, then a model revision with tests.

Repository licensing is left to the owner to decide. Original source facts, company disclosures, and third-party material remain attributable to their publishers.

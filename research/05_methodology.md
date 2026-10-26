# 05 — Financial modeling, source governance and accounting methodology

**As-of 2026-10-27.** All prices, volume plans, unit economics, rates and exit multiples in `data/scenarios.json` are **made-up, testable teaching assumptions for two fictional businesses**. Public-company historical numbers in `data/comparables.csv` and `data/evidence.csv` are independent and NOT inputs calibrated into the hypothetical projections.

## A. Evidence tiers / source discipline

| Tier | Example | Use |
|---|---|---|
| A — issuer or regulator | SEC filing, earnings release, HKEX interim disclosure, IEA report | Primary historic figures (publication and observed period mandatory) |
| B — specialist measured survey | IFR and Counterpoint | Market estimates with precisely defined population and date |
| C — company product price listing | Unitree shop | Posted starting price, not realized sale/COGS |
| D — analyst hypothetical | Synthetic scenario JSON | **Only** for exploring unit economics, never a reported-company fact |

`data/evidence.csv` fields: unique source ID; entity; published_at; observation_period; data_class; metric; value; unit; publisher; URL; checked_at; explicit caveat. Do not backfill unknowns with approximate synthetic numbers in the evidence ledger.

As of this cutoff, do not use results that have *yet to be announced* (for example Vertiv Q3 2026, scheduled Oct 28). Avoid mixing NVIDIA FY2027 Q2 (Jul 2026 quarter end) with actual calendar 2027 data.

## B. Infrastructure formulas (USD millions)

Let:

- `F_t` = ending deployed GPU capacity; `F_(t-1)` previous ending capacity.
- `A_t = (F_(t-1)+F_t)/2`: average in-year active GPU fleet; assumes linear deployment timing.
- `u` = paid billable utilization as a fraction, `H=8760` total hours/year.
- `p` = realized dollars per billed GPU-hour after price discounts.
- `kW` = fleet-average electric load per GPU at IT-level, `PUE>=1` physical facility multiplier.
- `e` = price dollars/kWh.
- `s` = fixed site services/lease operational cost dollars per average GPU/year.
- `v` = billed-hour variable software/egress cost.
- `c` = capex dollars per newly deployed GPU; `m` maintenance replacement fraction of ending fleet replacement value.

All output dollar expressions are divided by 1,000,000.

1. `BillableGPUHours_t = A_t * H * u`.
2. `Revenue_t = BillableGPUHours_t * p / 1e6`.
3. `Electricity_t = A_t * H * kW * PUE * e / 1e6` — **bills powered idle capacity too**.
4. `COGS_t = Electricity_t + A_t*s/1e6 + BillableGPUHours_t*v/1e6`.
5. `GrossProfit = Revenue - COGS`; `EBITDA = GP - SG&A_rate * Revenue - R&D_fixed`.
6. `Capex_t = (F_t-F_(t-1))*c/1e6 + F_t*c*m/1e6`.
7. Each year's capital expenditure (growth **and** maintenance) enters its own straight-line depreciation cohort immediately. Depreciation at year `t` = sum(capex vintages in last `D` years) / `D`.
8. `EBIT = EBITDA - D&A`; simplified cash tax = `max(EBIT,0)*tax_rate`; **no NOL carryforward**.
9. `DeltaNWC_t = (Revenue_t - Revenue_(t-1))*working_capital_revenue_fraction` and `UFCF = EBITDA - CashTax - Capex - DeltaNWC`.
10. `EV = sum(UFCF_t/(1+WACC)^t) + [max(EBITDA_last,0)*exit_EV_to_EBITDA]/(1+WACC)^T`. `Equity = EV - opening_net_debt`.

**Sign nuance:** if a finite-horizon discounted sum is negative (and the terminal proxy is zero), EV can be **negative** as a *capital shortfall indicator*. Real traded equity has limited liability; do not interpret these as market prices. A practical financing-aware model would explicitly incorporate new funding rounds, distress, debt recoveries, and restructuring options.

**Economic caveats:** Installed fleet doesn't retire in this toy model; full-year GPU count is averaged with previous year for utilization/revenue and powered energy. This ignores delivery timing dispersion, equipment aging, variable idle power and price/spot mix. Depreciation uses same-year onset, even for mid-year additions; simplifying convention should be upgraded with deployment dates. Site costs are not debt service. Maintenance capex is separate from expansion and capitalized then depreciated; no hidden double subtraction.

**Omissions:** finance lease/interest, NOL/taxes and deferred revenue accounting, GPU resale value and used-market impairment, contract duration, working-capital seasonality, energy-rate shape, termination fees, different GPU SKUs and regional power mix.

## C. Robotics formulas (USD millions)

Let `N_t` = new robots sold; `I_(t-1)` = installed fleet from all previous shipments (zero attrition assumed).

1. `AvgActive_t = I_(t-1) + N_t/2`.
2. `HardwareRevenue = N_t * ASP_t / 1e6`.
3. `HardwareCOGS = N_t * BOM_t / 1e6`.
4. `WarrantyProvision = HardwareRevenue * warranty_pct` (simple fixed percent).
5. `ServiceSubscribers = AvgActive_t * attach_rate`.
6. `ServiceRevenue = ServiceSubscribers * annual_service_ARPU / 1e6`.
7. `ServiceCOGS = ServiceRevenue * (1 - service_gross_margin)`.
8. `EBITDA = HardwareRevenue + ServiceRevenue - HardwareCOGS - Warranty - ServiceCOGS - SG&A_fraction * TotalRevenue - R&D_fixed`.
9. `Capex`, depreciation, simplified cash taxes and `DeltaNWC` feed UFCF as in infrastructure.
10. `EV = sum(UFCF_t/(1+r)^t) + [Revenue_last * synthetic_exit_EV_to_revenue]/(1+r)^T`.

**Do not misread:** Service subscriber count ignores attrition and uses average installed base, making long-term attach optimistic. No RaaS contract churn, installation delays, FX, production yield, discounts, distributor commissions, returns, safety recalls or customer payment delinquency. A terminal EV/revenue multiple is not a public market comp; it is **invented to illustrate terminal sensitivity**.

## D. Sensitivity & audit controls

- **Infra** 5 utilization levels (base ± 7.5/15 percentage points) × 5 realized GPU-hour prices (75–125% base).
- **Robotics** 5 attach rates (base ± 10/20 percentage points) × 5 hardware ASP levels (80–120% base).
- All other settings held fixed in a grid; neither grid is a probability forecast or confidence interval.
- Every scenario reports enterprise valuation and equity valuation separately, because net debt isn't part of UFCF.
- Guard checks: zero/negative costs, out-of-bound fractions, depreciation cohorts, fixed year series lengths, nondecreasing compute fleet.
- Verification: `python3 -m unittest discover -s tests -v` covers cash-flow identities, idle cost, sensitivity direction and immutable baseline assumptions.

## E. Public-company comparables: do not build a false ranking

- Quarterly USD NVIDIA/AMD/Vertiv/CoreWeave: different reporting calendars, business lines and financial expense placement.
- UBTECH H1 2026 is **six months, RMB and unaudited**.
- GAAP operating margin = same-period reported operating income / revenue. Blank gross margin means not sufficiently checked; do not derive CoreWeave “economic gross margin” by ignoring technology/infrastructure costs.
- No market prices, equity dilution, share counts, actual EV or public-company EV multiples appear. They require same-date evidence that has not been collected.
- Annualization by multiplying quarter results by 4 would invent stable seasonality; **not done**.

## F. Reproducibility & change log

1. Source old report → record publication date/period/type/value/unit and risk in `data/evidence.csv`.
2. Record model change explicitly in `data/scenarios.json`, cite primary observed records only as context.
3. Run all tests and `python3 run.py`.
4. Compare every case's EBITDA, UFCF, cumulative capex and PV terminal percentage; retain bear-case negative EV as risk.
5. Commit generated reports with code and assumptions; discuss why moving assumptions was warranted.

## G. Priority diligence that cannot be completed with public webpages

Company operating data: aging reports, customer invoice collections, contracted capacity, capitalized assets, real financing rates, detailed PUE/power bills, inventory / BOM, robot autonomy logs, warranty and field-service warranty reimbursements, bank covenants, ownership and legal restrictions.

**The model is a reproducible analysis framework, not a claim these private-company data were accessed.**

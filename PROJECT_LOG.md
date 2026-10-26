# Project execution log / lessons learned

**Date:** 2026-10-27 (Asia/Tokyo / project research cutoff).

## Delivery summary

- [x] Created and verified GitHub repository: [YOUessi/AI-HardTech-Investment-Research](https://github.com/YOUessi/AI-HardTech-Investment-Research).
- [x] Structured dated source ledger: 25 public evidence items including observed/forecast/quoted types and warnings.
- [x] Five period-preserving public-company comparison records (NVIDIA, AMD, Vertiv, CoreWeave, UBTECH).
- [x] Six separate research files: sector map, company comparisons, engineering due diligence, IC memo, accounting methodology, and IC questions.
- [x] Synthetic GPU infrastructure and synthetic robotics OEM five-year Bear/Base/Bull cash-flow models, explicit terminal-value assumptions, 25-cell sensitivity grids.
- [x] Local Mac verification with Python 3.9.6 (no third-party finance dependencies): **16 unit tests passing**; eight generated reports.
- [x] Published reproducible CSVs, JSON and offline HTML dashboard to GitHub.
- [x] GitHub Actions automated test/build [success on commit 6fa42dc](https://github.com/YOUessi/AI-HardTech-Investment-Research/actions/runs/40391266474).

## Concrete issues encountered and resolution

| ID | Issue | Cause | Resolution | Evidence / remaining constraint |
|---|---|---|---|---|
| I-01 | Source observations differ in periods, currency and business models | NVIDIA fiscal FY27 Q2 vs calendar 2026 Q2; UBTECH H1 2026 in RMB, different accounting lines | CSV retains period, unit and comparison-warning fields; dashboard computes only same-period GAAP operating margin per company; **no fabricated public EV multiples** | data/evidence.csv and data/comparables.csv |
| I-02 | UBTECH original issuer disclosure appears as a site announcement index; extract is cross-checked in third-party filing mirror | HTML announcement index does not expose the individual financial table as clean text | Link issuer index; add explicit caveat and mirrored table provenance for RMB 1,269.130m H1 revenue and other numbers | https://www.ubtrobot.com/en/announce and filing mirror in ledger; manually confirm direct filing in formal deal |
| I-03 | IFR 2025 full-size professional humanoids and Counterpoint H1 2026 wider shipments have different definitions | Combining would produce a spurious market CAGR | Put definition/date separately in source ledger; explicitly prohibit direct concatenation | IFR and Counterpoint citations in sector map |
| I-04 | Synthetic downside DCF can return negative enterprise values | Large discounted buildout cash outlays and (for infra bear) nonpositive final EBITDA lead to zero exit EBITDA proxy | Preserve **negative model value** as required-funding shortfall; explain these are NOT negative equity market prices | Inference bear EV -66.265m USD, Robotics bear EV -17.948m USD |
| I-05 | A GitHub Git-tree batch initially used an old `base_tree_sha`, omitting earlier paths from a later tree | Tree API can silently create a valid tree without unrelated previous files | Recreated missing data/docs blobs on the latest tree and verified full 26-file inventory at commit 6fa42dc | Fully restored; GitHub Actions tests passed |
| I-06 | Mac `git pull` / `git fetch` stalled during latest-document synchronization | Local HTTPS connection stopped responding despite initial clone and earlier pull succeeding | Kept GitHub connected API as authoritative publish route, terminated/timeout the stalled commands, **did not overwrite private files**. Mac can run the models and has generated reports. | Local checkout may lag latest GitHub docs and reports until network recovers; no claim of a fully up-to-date local Git ref |
| I-07 | Valuation assumptions cannot be verified from public documents | Actual fleet vintage, GPU contracts/debt, robot BOM, services/returns and customer invoices are private | **Synthetic model** clearly and repeatedly labeled; diligence packet requests these primary records before capital decision | Missing actual target financials are a blocker to investable IC approval |

## Unit-test and real output snapshot

Local Mac command:

```bash
cd ~/Documents/projects/AI-HardTech-Investment-Research
python3 -m unittest discover -s tests -v
python3 run.py
```

Observed on Mac: `Ran 16 tests ... OK`, eight report files generated.

| Fictional target | Bear EV (USD m) | Base EV (USD m) | Bull EV (USD m) |
|---|---:|---:|---:|
| Synthetic GPU-cloud service company | -66.265 | 87.758 | 552.697 |
| Synthetic humanoid robotics company | -17.948 | 52.164 | 279.640 |

This is an **illustrative range of cash-flow model outputs**, not probability-weighted, not an audited valuation and **not a price recommendation on any named public/private company**.

## GitHub chronology

- `ac15f6d` — initialize README.
- `1cab721` — record evidence ledger and scenarios.
- `300ce0d` — implement models and tests.
- `77c5377` — repair missing input-tree paths.
- `c17fb26` — add deterministic report generator.
- `264b38c` — add sector map/comps/technical diligence.
- `9290db2` — add IC memo/methodology/interview questions.
- `621e2c6` — repair missing early research documents in GitHub tree.
- `6fa42dc` — commit all eight generated financial/dashboard outputs; CI passing.

## Limits and next verification gates

This is **complete as a public-data, reproducible simulated investment research project**. It is **not** an actual transaction-level investment committee authorization, field audit or real company discounted-cash-flow valuation.

Required if upgraded for a real deal: actual customer contracts, powered fleet/use, debt terms, chip lifetimes, utility bills, robot autonomous field performance, product BOM / warranty and audited capitalization. See research/06_ic_questions.md.

**Do not state:** "we completed a proprietary financial or customer audit," "we verified a robot's industrial ROI," "Unitree has the synthetic scenario margins," or "a negative synthetic DCF is a negative market stock price."

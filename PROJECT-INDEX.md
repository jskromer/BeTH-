# BeTH Project Index — Berkeley Budget Material
*Consolidated 2026-06-11. All Berkeley budget work from chat sessions, mapped to its location in this repo.*

## Live BeTH pages (Cowork artifacts, archived in `artifacts/`)
| Page | Repo copy | Purpose |
|---|---|---|
| beth-budget-audit | `artifacts/beth-budget-audit.html` | Analytical scoreboard: FY27/28 budget × audit follow-through by department |
| beth-budget-fiction | `artifacts/beth-budget-fiction.html` | Public-facing op-ed edition ("the budget is a fiction") |
| beth-two-problems | `artifacts/beth-two-problems.html` | Measured coalition edition (transparency + accountability, Auditor as ally) |
| beth-plans-synthesis | `artifacts/beth-plans-synthesis.html` | 27 adopted plans vs. 2018 Strategic Plan goals: currency flags, coverage gaps, FY27–28 fiscal context. Public copy: `docs/berkeley-plans-synthesis.html` |

Live versions remain in the Cowork sidebar; these are static archives.

## Berkeley Event Value Twin (`event-value-twin/` + `docs/berkeley-event-value-twin.html`)
A reusable model for evaluating civic events (Kite Festival as first case), keeping economic impact, City fiscal impact, and public value separate. Counterfactual/incrementality math + IMPLAN/RIMS-II cross-check + Monte Carlo.
- `docs/berkeley-event-value-twin.html` — interactive dashboard (self-contained; five screens, live scorecard, money-flow diagram, evidence register). Linked from Budget Basics.
- `event-value-twin/data/seed.json` — the 12 seed tables (2019-style reconstruction + 5 scenarios), all values illustrative/tagged measured·modeled·stipulated
- `event-value-twin/model/event_value_twin.py` — transparent engine (stdlib only); `python3 model/event_value_twin.py` reproduces every dashboard figure
- `event-value-twin/model/schema.sql` — PostgreSQL/PostGIS DDL for the 12 tables
- `event-value-twin/README.md` — methodology & commitments
- **Status:** v0.1 preliminary. Numbers are illustrative pending the data-gap register; Kite Festival last ran 2017–2019.

## FY2027–28 budget analysis (`BeTH/`)
- `berkeley-budget-database.json` — canonical consolidated store: balancing recap, deficit history, all-funds by department, staffing, audit layer, 12-item opportunity cross-walk
- `fy2027-2028-proposed-budget.json` — parsed proposed-budget data
- `audit-budget-opportunities.md` — deep-dive memo: efficiency/accountability opportunities
- `rational-budgeting-process.md` — reform framework (carryovers, AAO, health cost-sharing lever)
- `two-messages.md` — two registers of the same fact base ("fiction" + "two fixable problems")
- `2026-06-09 Agenda - Council.pdf`, `2026-06-09 Item 02 Ordinance 8010.pdf` — June 2026 council sources
- `New Audit Plan and Whistleblower Annual Report.eml` — Auditor FY2027 plan source

## Spreadsheets (repo root)
- `BeTH_Fiscal_Health_Tracker.xlsx` — master tracker (2026-04-08)
- `Berkeley_Budget_History_FY2016-FY2026.xlsx` — ACFR actuals: all-funds FY16–25, GF budget-vs-actual FY25 (+$2.0M adopted → −$16.7M actual), deficit & one-time fixes FY19–28, sources & confidence tab
- `Berkeley_Audit_Comparison_2022_vs_2026.xlsx` — 2022 vs 2026 financial-condition audits

## Source documents (repo root)
- `Berkeleys_Financial_Condition_(FY_2016-FY_2025)...pdf` — main audit (April 2026)
- `annual-comprehensive-financial-report-fy2025.pdf` — FY2025 ACFR
- `Item 02 Proposed FY27-FY31 Proposed CIP Budget Presentation.pdf` — CIP budget
- `2026-04-09 Agenda Packet - Budget.pdf` + lease presentation/list — April budget committee
- `berkeley_audit_comparison.pdf` — audit comparison summary

## Site & apps
- `berkeley-fiscal-reality/` — React site (`src/App.jsx`, `src/CarryoverTracker.jsx`); App.jsx carries the reverted/corrected FY26 balancing figures (uncommitted as of 2026-06-10)
- `berkeley_carryover_tracker.jsx` — standalone carryover tracker component
- `T1/` — deployed tracker (`index.html`, `t1_phase2_tracker.html`)
- `carryover.html`, `history-of-the-habit.html`, `taplin-factcheck.html` — standalone pages
- `beth-two-problems.pdf` — print version of the two-problems page

## Known gaps (carried over from session notes)
- GF adopted-vs-actual for FY2016–2024 needs prior-year ACFR budgetary schedules (only FY2025 in hand)
- AAO ordinances + year-end carryover schedules not yet pulled — adopted-vs-actual gap asserted, not quantified
- Health/Retiree $21.9M line bundles active + OPEB; employee cost-sharing savings unquantifiable without MOUs

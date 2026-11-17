# BeTH — the repo behind Learn About Berkeley

The public site is **Learn About Berkeley**: https://learn-about-berkeley.vercel.app (Vercel project `berkeley-transparency-hub`, deployed from `main`). It is a neutral transparency site: it lays out Berkeley's money, plans and audits so residents can decide for themselves. "BeTH" is the internal name only.

**Read next:** `OPERATIONS.md` (how the project stays organized and current, and the calendar of update dates) · `AGENT_COORDINATION.md` (who may change which code).

*Map written 2026-11-16. Replaces `PROJECT-INDEX.md` (now in `_archive/2026-11-16/`).*

## Folders

| Path | What it holds |
|---|---|
| `docs/` | The website. Every `.html` here is a public page. |
| `sources/<year>/` | City documents: agenda packets, staff reports, audits, CIP presentations (`sources/2026/agenda-items/` holds item PDFs pulled for analysis). |
| `research/` | Steve's Berkeley research: `behavioral-health/` (MHSA/BHSA plans, split ledger, flight sim, system maps), `budget-balance-stack/`, `corridors/` (density and parcel models), `liability-clock/` (model project), `vision-2050/`, `waterfront-ferry/`, `decision-making-framework/`, `artifacts/` (claude.ai artifact copies, indexed in its README), plus spreadsheets, notes and drafts. Moved from `~/D1-campaign` on 2026-11-16. **Ignored by git for new files** (`.gitignore`): the repo is public. |
| `sources/assessor/` | Alameda County assessor roll extracts (403 MB). Ignored by git. |
| `annual-comprehensive-financial-report-fy2025.pdf` | FY2025 audited financial report. Stays at the top level because the fund tools read it from here. |
| `data/funds/` | 106 fund records (JSON), one per City fund. `data/curation/` lists the six hand-curated ledgers. |
| `tools/` | Fund pipeline: ACFR extraction, safety layer, page builders. See `AGENT_COORDINATION.md`. |
| `tests/`, `.github/` | Tests and CI for the fund pipeline. |
| `plans/` | Project plans, handoffs, and the reorganization manifest. |
| `staging/` | Working files for the FY2024 extraction pilot and FY2025 corrections. |
| `berkeley-fiscal-reality/` | Separate React site (older). |
| `event-value-twin/` | Model behind the Event Value Twin page. |
| `T1/` | Separate Measure T1 bond tracker site. |
| `_archive/` | Superseded copies, by date. Nothing in it is live. |
| `_to_delete/` | Files set aside for Steve to delete by hand. |

## Site pages (`docs/`)

### Start here
- `index.html` — home page
- `for-newcomers.html` — a guided 40-minute path through the five pages that matter
- `berkeley-simple-version.html` — the ~$29M recurring gap in one metaphor, five minutes
- `berkeley-budget-basics.html` — where tax dollars come from and go; the gap; unfunded infrastructure

### Plans & governance
- `berkeley-plans-synthesis.html` — 27 adopted plans scored for currency; the referral queue
- `berkeley-general-plan-currency.html` — eight of nine General Plan elements frozen at 2001–02
- `berkeley-plans-audits-budget.html` — each strategic goal × City Auditor recommendations × FY27–28 budget

### Following the money
- `berkeley-fund-map.html` — the budget connected to Berkeley's 123 funds (106 City + 17 fiduciary)
- `funds.html` — every fund, one line each, linking to its page
- `fund-*.html` (106 pages) — one ledger per fund, generated from `data/funds/` by `tools/build_fund_page.py`; six are hand-curated (011 General Fund, 608 Marina, Parks Tax, Equipment Replacement, Workers' Comp, Zero Waste)
- `dashboard.html` — city finances as the FY2025 audit reports them
- `berkeley-grant-flows.html` — where outside grant money enters and goes
- `berkeley-cross-fund.html` — six legal ways other-fund savings could relieve the General Fund
- `berkeley-homeless-costs.html` — the reported ~$35M, every contract, regional comparison, uncounted costs
- `berkeley-budget-glossary.html` — budget terms in plain English

### Deficit & accountability
- `emergency-remediation.html` — the City's Plan B cut list (not triggered; Measure V passed) and remediation measures from the audit record
- `budget-two-problems.html` — transparency and accountability as fixable problems (June 2026 snapshot)
- `mayors-budget.html` — where the "Mayor's budget" really comes from
- `rent-board-fy27.html` — the Rent Board's separate budget
- `deficit-tenure-ledger.html` — the deficit through time, by who was in office *(not linked from home page)*
- `deficit-is-choices-talking-points.html` — public-comment talking points *(not linked from home page)*
- `berkeley_budget_accountability.html` — budget accountability FY2016–FY2026 *(not linked from home page; older)*

### Issue deep-dives
- `berkeley-quiet-zones.html` — train horns and quiet zones
- `berkeley-corridor-upzoning.html` / `berkeley-corridor-sources.html` — corridor rezoning: the research, then the sources and players
- `berkeley-cip-hub-sources.html` / `berkeley-cip-hub-data-review.html` / `berkeley-cip-hub-vs-vision-2050.html` — the Sept 29, 2026 infrastructure dashboard referral, its UC studio prototype, and Vision 2050
- `berkeley-measure-u-oversight.html` — Measure U's oversight provisions against the Vision 2050 documents
- `berkeley-ferry-waterfront.html` — pier, ferry and Marina paid parking

### Agenda watch
- `council-decoded.html` — monthly decoded recap
- `left-field.html` — agenda items that trace to no plan or audit
- `budget-scans.html` + `budget-scan-YYYY-MM-DD.html` — dated agenda scans (snapshots; not updated after the fact)

### Tax measures
- `berkeley-tax-types-and-rate-setting.html` — tax types and how rates are set each June
- `berkeley-tax-measures.html` — every measure on the tax bill, plus the Nov 2026 results
- `measure-*.html` (16 pages) — one page per measure

### Tools & models
- `berkeley-event-value-twin.html` — weighing a civic event's economic, fiscal and public value

## Where else BeTH material lives
- `~/D1-campaign` (private repo): campaign operations only — finance, filings, voter file, field, mailers, positions and talking points, correspondence. Berkeley research moved out to `research/` on 2026-11-16. (copies and views; this repo is the real one)
- Claude project "Berkeley - Learn About": working notes (auditor feed delta, FY2027 tax rates, Gage fact sheet, ferry tracker)
- Claude Docs: the PRW Measure U letter draft (copy in `research/2026-11-prw-measure-u-letter.md`)
- Sibling repos in `Documents/GitHub/`: `berkeley-tax-calculator` (live at berkeley-tax-calculator.vercel.app; WOM Berkeley embeds a copy) and `d1-site` (District 1 campaign site, retired to a thank-you page Nov 4, 2026). `District One Election/` is an empty folder.
- Audit dashboard app: location not found in `Documents/GitHub/` (2026-11-16)
- About 14 Berkeley artifacts in claude.ai (homelessness, ferry, Liability Clock, Budget Flight Sim, and others) are not yet copied into this repo

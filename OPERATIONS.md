# BeTH operations plan

*How this project stays organized and current. Written 2026-11-16. Read this first; `AGENT_COORDINATION.md` keeps the rules for who touches which code.*

## 1. One home
The `main` branch of this repo is the real version of everything. Other copies (Claude project docs, Claude Docs, artifacts, downloads) are views or drafts; anything worth keeping lands here.

| Folder | Holds |
|---|---|
| `docs/` | The public site, Learn About Berkeley (Vercel project `berkeley-transparency-hub`, deploys from `main`) |
| `sources/<year>/` | City PDFs, agendas, audits, ACFRs, named `YYYY-MM-DD Title.pdf` |
| `research/` | Notes, drafts, letters, memos, analysis spreadsheets |
| `data/`, `tools/`, `tests/`, `plans/` | Fund pipeline (see `AGENT_COORDINATION.md`) |
| `_archive/` | Superseded copies, renamed with a date. Nothing is deleted; Steve empties it by hand. |

## 2. One map
`README.md` lists every folder and every site page in one line each. It replaced `PROJECT-INDEX.md` (June 2026), now in `_archive/2026-11-16/`.

## 3. One branch for content
Page edits go straight to `main`. Feature branches only for code; delete them once merged. Commits and pushes are run by Steve in Terminal.

## 4. Freshness registry
`docs/data/pages.json`: for each page, its sources, the date last checked, and the event that makes it stale. `tools/staleness_check.py` flags pages whose trigger has passed, that are overdue for review, or that still contain known-stale phrases. After rechecking a page: `python3 tools/staleness_check.py --mark <page>.html`.

## 5. Rhythm
- **Every council meeting:** budget scan (`docs/budget-scan-YYYY-MM-DD.html`). Record the fund number for every money item in the scan's Fund column, then add a meeting block to `data/agenda_fund_actions.json` (one row per fund per item; `kind` = spend / annual / authority / revenue / passthrough; amounts from the staff report; items with no fund named go in `unassigned`) and run `python3 tools/build_fund_activity.py` and `python3 tools/build_funds_index.py data/funds docs/funds.html`.
- **After each meeting:** set that meeting's `status` in `data/agenda_fund_actions.json` to `adopted` (or note amended / pulled items) and rebuild `docs/fund-activity.html`.
- **Each June:** when the new Annual Appropriations Ordinance is adopted, add its Exhibit A to `data/fund_numbers.json` (new funds, renamed funds, adopted amounts).
- **Monthly:** staleness check + City Auditor recommendation feed (~10 min).
- **Dated triggers:**

| When | Event | Pages to update |
|---|---|---|
| Late Nov–early Dec 2026 | County certifies Nov 3 election | tax-measures, remediation, budget-basics, simple-version, measure-u-oversight ("unofficial" → final) |
| Dec 1, 2026 | Corridor rezoning at Council | corridor-upzoning, corridor-sources |
| Dec 2026–Jan 2027 | FY2026 ACFR published | all 106 fund pages, dashboard, funds index |
| Jan 13, 2027 | PRW takes up Measure U oversight | measure-u-oversight |
| ~Late Mar 2027 | First semi-annual report on the Sept 29 asset-management referral | cip-hub pages, measure-u-oversight |
| Apr 1, 2027 | Measures V and AA start collecting | tax-measures, budget-basics |
| Mid-Jun 2027 | FY2028 tax-rate ordinances; budget update | tax-measures, measure pages, budget-basics |
| Open | BCDC paid-parking hearing date; ferry Final EIR | ferry-waterfront |

## 6. Session close
Before any session ends: everything it produced is saved in this repo, and Steve gets one commit command to paste.

## 7. Three tiers: public, private research, campaign

| Tier | Where | Who sees it |
|---|---|---|
| **Public** | `docs/` → https://learn-about-berkeley.vercel.app (Vercel `berkeley-transparency-hub`). Separate public tool: the tax calculator (repo `berkeley-tax-calculator`, Vercel `berkeley-tax-calculator`, embedded by WOM Berkeley). | Everyone |
| **Private Berkeley research** | `research/` and `sources/assessor/` in this repo, both git-ignored (the repo is public). Claude project "Berkeley - Learn About" for working notes. | Steve only |
| **Campaign** | `~/D1-campaign` (private repo) and `d1-site` (retired to a thank-you page). Campaign material never enters BeTH. | Steve and treasurer |

**From research to public:** write a neutral page in `docs/` (sources, confidence labels, no recommendations), add it to `docs/data/pages.json`, link it from `index.html`, push. Nothing in `research/` reaches GitHub unless it is deliberately rewritten into `docs/`. Advocacy (Steve speaking for himself) is published elsewhere, never on Learn About Berkeley.

### Vercel projects (2026-11-16)

| Project | Source | Status |
|---|---|---|
| `berkeley-transparency-hub` | `BeTH/docs` | **Live** — the public site |
| `berkeley-tax-calculator` | `berkeley-tax-calculator` repo | **Live** — updated for Nov 2026 results 2026-11-16 |
| `tonephasetwo` | `BeTH/T1` | **Deleted 2026-11-16** — content now `docs/measure-t1-tracker.html` |
| `berkeley-audit-dashboard` | none on disk | **Deleted 2026-11-16** — site links now point to `docs/dashboard.html` |
| `berkeley-fiscal-reality` | `research/fiscal-reality/site` | **Deleted 2026-11-16** — content saved in `research/fiscal-reality` |
| `d1-site` | `d1-site` repo | Campaign; retire when filings close |


## Status
- [x] Site audit and post-election fixes (2026-11-16)
- [x] Step 1: files moved into sources/, research/, _archive/2026-11-16/ (2026-11-16; manifest in plans/)
- [ ] Step 1 leftovers: move research-bound Berkeley_Budget_History xlsx once closed; place beth_orchestrator.py
- [x] Step 2: README.md map written; PROJECT-INDEX.md archived (2026-11-16)
- [x] Step 4: docs/data/pages.json + tools/staleness_check.py (2026-11-16)
- [x] Three-tier plan, T1 tracker folded into site, tax calculator updated, fiscal-reality archived (2026-11-16)
- [x] Retired Vercel projects tonephasetwo, berkeley-audit-dashboard, berkeley-fiscal-reality (2026-11-16; addresses return errors)
- [x] Step 5: scheduled task "BeTH monthly freshness check" — Mondays 9:31 am Pacific, acts only on the first Monday of each month; runs the staleness check + City Auditor feed comparison and sends a report (no edits). Needs the Mac on with the Claude desktop app open. (2026-11-16)

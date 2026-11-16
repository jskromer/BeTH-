# Step 1 reorganization — proposed moves (2026-11-16)

Nothing is deleted. Every move is a `mv`; superseded copies go to `_archive/2026-11-16/`.

## Stays where it is (code or other tools point at it)
- `annual-comprehensive-financial-report-fy2025.pdf` — read by tools/acfr_* and the FY2024 pilot
- `docs/`, `data/`, `tools/`, `tests/`, `plans/`, `staging/`, `.github/` — pipeline and site
- `berkeley-fiscal-reality/` (React app), `event-value-twin/`, `T1/` (separate tracker site)
- `AGENT_COORDINATION.md`, `OPERATIONS.md`
- `_to_delete/` (yours to empty)
- `.~lock…` / `~$…` files — spreadsheet lock files; close Berkeley_Budget_History in Excel/LibreOffice and they vanish

## → sources/2026/  (City documents)
- 2026-04-09 Agenda Packet - Budget.pdf
- 2026-04-09 Item 03 Budget Lease Presentation.pdf
- 2026-04-09 Item 03 PW and PRW and HHCS Lease List.pdf
- 2026-07-13 Agenda Packet - Agenda Committee.pdf
- 2026-09-29 Item 26 Referral to the City Manager to develop an updated.pdf
- 2026-10-27 Item 14 Authorizing the City Manager to Submit.pdf
- Berkeleys_Financial_Condition_(FY_2016-FY_2025)_-_Structural_Deficit_Poses_Risk_to_Financial_Sustainability.pdf
- HSPE Full Agenda Package 5.4.26.pdf
- Item 02 Proposed FY27-FY31 Proposed CIP Budget Presentation.pdf

## → sources/2025/
- artifacts/2025-12-02 Special Item 01 Sharing the Final Report of the Mayor.pdf

## → research/  (your analysis, notes, drafts)
- BeTH_FY2027_adopted_tax_rates.csv
- BeTH_Fiscal_Health_Tracker.xlsx
- Berkeley_Audit_Comparison_2022_vs_2026.xlsx
- Berkeley_Budget_History_FY2016-FY2026.xlsx  (close it first)
- berkeley_homeless_programs.xlsx
- berkeley_audit_comparison.pdf
- BeTH_Phase_2_Capital_Choices_Vision_2050_Plan.md
- BeTH_Project_Review_Printable_2026-10-26.pdf
- beth-fact-review-2026-09-05.md
- beth-site-review-2026-07-30_2.md
- general-fund-explainer-draft.md
- beth-two-problems.pdf
- priority-map.html
- Gage/
- Uncertainty /
- artifacts/2026 infra bond - memo to Mayort.pdf
- artifacts/Comments on 2026 financial audit.pdf
- artifacts/Comments on 2026 infra bond.pdf
- artifacts/Comments on 2026 infra bond-1.pdf
- artifacts/berkeley-verification-guide.docx / .pdf
- artifacts/Berkeley_Asset_Service_KnowledgeBase.xlsx
- NEW: research/2026-11-prw-measure-u-letter.md (copy of the Claude Docs letter)

## → _archive/2026-11-16/  (superseded copies; the live versions are in docs/)
- berkeley-cross-fund.html, berkeley-plans-synthesis.html, berkeley-simple-version.html (root copies; older than docs/)
- artifacts/beth-*.html (10 files) and beth-plans-synthesis.html.pre-2026-08-21 — Cowork-era copies, still say "384"
- archive/ (carryover tracker, 2 files)
- PROJECT-INDEX.md — after README.md replaces it (Step 2)

## Needs your call
- IMG_9885.jpg — no context; research/ or _archive/?
- beth_orchestrator.py — untracked script; move to tools/ or leave?

After the moves, `artifacts/` and `archive/` are empty and the repo root holds ~12 items instead of ~40.

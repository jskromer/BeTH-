# BeTH agent coordination

*Who owns what, how the pieces fit, and the rules for touching shared files. Read before changing anything. Kept at the repository root because `docs/` is the published website.*

Last updated: 2026-10-22 by Claude.

## Roles

| Who | Owns | Does not touch without asking |
|---|---|---|
| **Steve** (project owner) | Priorities, merges, every published claim | |
| **Claude** | The existing pipeline (`tools/acfr_parse.py`, `tools/acfr_funds.py`, `tools/build_fund_page.py`, `tools/build_funds_index.py`, `tools/ledger.py`), the fund schema, the six curated ledgers, the site theme, deployment to GitHub Pages; next: the agent pipeline (plan deliverable 5) | Historical extraction work once Codex's branch exists |
| **Codex** | PR "historical FY2015–FY2024" (GPT-6's spec calls it PR #9; GitHub assigns the number): historical ACFR acquisition, extraction, fund-identity mapping, reconciliation, tests | The curated ledgers' flows and narratives; the theme; `docs/index.html` beyond adding links |
| **GPT-6** | Methodology, acceptance tests, review of accounting logic | Code |

One owner per branch. Two writers never edit the same file on different branches at the same time; if a change needs a shared file (`tools/ledger.py`, `data/funds/SCHEMA.md`, `tools/build_fund_page.py`), say so in the PR description and keep the diff to that file minimal.

## Where things are

| Path | What |
|---|---|
| `annual-comprehensive-financial-report-fy2025.pdf` | FY2025 ACFR, the source for every generated fund file. FY2024 ACFR is not in the repo (downloaded to a scratch folder during curation). |
| `tools/acfr_parse.py` | Position-based parser for fund-column statement pages. See the handoff. |
| `tools/acfr_funds.py` | Writes one `data/funds/<id>.json` per fund column from four FY2025 statements. |
| `tools/ledger.py` | Schema validator. `python3 tools/ledger.py data/funds/*.json` must print only `OK` lines. |
| `data/funds/SCHEMA.md` | The fund record, year block, flow event, and optional blocks. |
| `data/funds/*.json` | 106 fund records. Six are curated (no `generated_by` key): `011`, `608`, `ACFR-park-tax`, `ACFR-equipment-maintenance-replacement`, `ACFR-workers-compensation`, `ACFR-zero-waste`. The other 100 carry `"generated_by": "tools/acfr_funds.py"`. |
| `tools/build_fund_page.py` | Renders a fund JSON to `docs/fund-<id>.html` (`--all data/funds` for every fund; Marina goes to `fund-608-marina.html`). Prose for curated funds lives in its `NARRATIVE` dict. Copies each JSON to `docs/data/funds/`. |
| `tools/build_funds_index.py` | Renders `docs/funds.html`, the fund browser. |
| `docs/` | The website (GitHub Pages serves it; Vercel project `berkeley-transparency-hub` mirrors it when Steve deploys). Generated HTML is committed. |
| `plans/fund-dashboard-and-agents-plan-2026-10-22.md` | The six-deliverable plan. Deliverables 1–4 shipped; 5 (agents) and 6 (dashboard) open. |
| `plans/handoff-fy2025-extraction.md` | Technical handoff for the FY2025 pipeline (read this before touching extraction). |

## Data conventions

- **Fiscal years** end June 30; `fy: 2025` is July 2024–June 2025.
- **Units**: whole dollars, integers. No thousands, no rounding in data files; rounding happens in rendering.
- **Signs**: `revenue`, `expenditure`, `transfers_in`, `transfers_out` are non-negative. Negative balances are negative. Flow `amount` is non-negative; direction comes from `kind` and `from_fund`/`to_fund`.
- **Governmental funds**: `revenue` = total revenues; `expenditure` = total expenditures (includes capital outlay and debt service); `ending_balance` = fund balance. Transfers are excluded from both.
- **Proprietary funds** (enterprise, internal service): `revenue` = total operating revenues; `expenditure` = total operating expenses (includes depreciation); `nonoperating` = net non-operating; `ending_balance` = total net position.
- **Missing is `null`, never 0.** A dash on the statement is 0 (the City reported nothing); an unread field is `null`.
- **Every year block and every flow cites a `source` id** present in the file's `sources` map, with a confidence tag (`High` = read from the cited primary document; `Moderate` = inference or secondary source; `Low` = unverified; `Unknown` = not retrieved).
- **Fund ids**: City fund numbers where known (`011` General, `501` Capital Improvement, `511` Measure T1, `608` Marina, `611` Sanitary Sewer); otherwise `ACFR-<slug of the statement column name>`. Two names appear twice in the FY2025 statements (Measure T1 and Measure O each have a capital/major fund and a debt-service fund); the second carries a `-debt-service` suffix. **Historical work needs a fund-identity table** (see open questions); do not rename existing ids.
- **Curated files are never overwritten by extraction.** `acfr_funds.py` keeps a `KEEP` set; any new extractor must skip files lacking `generated_by` and instead propose additions (a new year block) for review.
- **Flows proposed by an agent** carry `reviewer: "agent:proposed"` and do not render. A person sets `reviewer` to their initials after checking.

## Reconciliation already in place (FY2025)

For every fund column: the sum of revenue line items equals the statement's "Total revenues" (or "Total operating revenues"), and the sum of expenditure line items equals "Total expenditures" (or "Total operating expenses"), to within $1. This is checked in the extraction session, not yet as a committed test. Spot-checks against raw page text: General Fund, Park Tax, Equipment Maintenance, Central Services, Building Maintenance, Workers' Compensation, Marina, all match.

Not yet checked: balance roll-forward (beginning + net change = ending), cross-year continuity, transfer totals across funds. These belong in the historical PR's tests.

## Known issues an extractor must handle

1. **The FY2025 ACFR's ten-year statistical schedules are wrong** for business-type rows: the columns labeled 2023 and 2024 repeat the 2022-level figures and earlier years are shifted. The FY2024 ACFR's schedule is consistent. Use each year's own fund statements, not the ten-year schedules, for history.
2. **The FY2025 ACFR reports Equipment Maintenance (672) and Equipment Replacement (671) as one internal service fund column.** Older years may separate them. Map, do not merge or split silently.
3. **Facing pages drift** a few pixels by the bottom of the page; the parser matches rows monotonically within 8 px. Older PDFs may have been produced differently; check the first page of each statement by hand.
4. **Statement row labels change wording** between years ("Culture-recreation" vs "Culture and recreation"; "Private contributions and donations" sometimes wraps to "donations"). `acfr_funds.py` carries small alias lists; extend them rather than hard-coding per year.
5. **The City's financial-reports page lists only the FY2023 and FY2024 ACFRs** (FY2025 is at a dated path under `/sites/default/files/2026-01/`). FY2015–FY2022 are not linked there; look in the City's document archive, EMMA (municipal bond disclosures), or the State Controller's reports, and record provenance per the spec.
6. **`docs/` is the live site.** Do not put working documents there. Generated HTML is committed, so regenerate and commit `docs/fund-*.html`, `docs/funds.html` and `docs/data/funds/` whenever data changes.

## Open questions for GPT-6 / Steve

- Fund-identity policy for history: keep `ACFR-<slug>` ids keyed to FY2025 names and add an `aliases` block per year, or move to City fund numbers (requires a budget-document crosswalk that does not exist in the repo yet)?
- Whether the 5 pension/OPEB trust funds and 12 custodial funds (counted in the Fund Map's 123, no pages yet) should get records in `data/funds/` with their own statement conventions.
- Whether reconciliation tests should live in `tools/ledger.py` (shared) or a new `tools/reconcile.py` (Codex-owned). Claude's preference: new file, so the validator stays stable.

## Branch etiquette

- Branch from `origin/main`, name `codex/...` or `claude/...`, open a PR, never push to `main`.
- Before opening a PR, run: `python3 tools/ledger.py data/funds/*.json`, regenerate pages, and confirm no FY2025 value in a curated file changed (diff `data/funds/{011,608,ACFR-park-tax,ACFR-equipment-maintenance-replacement,ACFR-workers-compensation,ACFR-zero-waste}.json`).
- Commit author email must be one the Vercel team recognizes (`info@counterfactual-designs.com`); Steve's repo config is set to it.
- Steve merges. Nobody enables auto-merge.

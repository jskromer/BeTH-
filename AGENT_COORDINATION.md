# BeTH agent coordination

*Who owns what, how the pieces fit, and the rules for touching shared files. Read before changing anything. Kept at the repository root because `docs/` is the published website.*

Last updated: 2026-10-22 by Claude, after the extraction-safety merge (PR #10).

## Roles

| Who | Owns | Does not touch without asking |
|---|---|---|
| **Steve** (project owner) | Priorities, merges, every published claim, the protected-ledger registry | |
| **Claude** | The page pipeline (`tools/build_fund_page.py`, `tools/build_funds_index.py`), the fund schema, the six curated ledgers' content, the site theme, deployment to GitHub Pages; next: the agent pipeline (plan deliverable 5) | Historical extraction work on Codex's branches |
| **Codex** | Extraction safety (PR #10, merged: `tools/ledger_safety.py`, `tests/`, the CI workflow) and the later phases, named by scope rather than reserved PR numbers: the FY2024 extraction pilot, then historical ACFR acquisition, extraction, fund-identity mapping, reconciliation, tests | The curated ledgers' flows and narratives; the theme; `docs/index.html` beyond adding links |
| **GPT-6** | Methodology, acceptance tests, review of accounting logic | Code |

One owner per branch. Two writers never edit the same file on different branches at the same time; if a change needs a shared file (`tools/acfr_parse.py`, `tools/acfr_funds.py`, `tools/ledger.py`, `tools/ledger_safety.py`, `data/funds/SCHEMA.md`, `data/curation/protected-ledgers.json`, `tools/build_fund_page.py`), say so in the PR description and keep the diff to that file minimal.

## Where things are

| Path | What |
|---|---|
| `annual-comprehensive-financial-report-fy2025.pdf` | FY2025 ACFR, the source for every generated fund file. FY2024 ACFR is not in the repo (downloaded to a scratch folder during curation). |
| `tools/acfr_parse.py` | Position-based parser for fund-column statement pages. See the handoff. |
| `tools/acfr_funds.py` | Extracts one record per fund column from four FY2025 statements, then hands the whole batch to `ledger_safety.update_ledgers`, which creates new files and appends new annual rows to existing ones. |
| `tools/ledger_safety.py` | Append-only update layer: annual-row identity, conflict detection, protected-ledger enforcement, batch preflight before any write. Raises `SafetyError`. |
| `data/curation/protected-ledgers.json` | Registry of the six curated ledgers (`status: curated`, `policy: immutable-to-extraction`). Kept outside `data/funds/` because every JSON file there is read as a ledger. |
| `tools/EXTRACTION_SAFETY.md` | The update policy, the verification commands, and the recorded requirements for the FY2024 pilot. |
| `tests/test_extraction_safety.py` | 14 unit and regression tests; `tests/fixtures/fy2025-audited-values.json` is the FY2025 regression fixture. |
| `.github/workflows/extraction-safety.yml` | CI on every PR and on pushes to `main`: tests, validator, a real FY2025 extraction, and `git diff --exit-code -- data/funds docs`. |
| `tools/ledger.py` | Schema validator. `python3 tools/ledger.py data/funds/*.json` must print only `OK` lines. A duplicate annual identity (see conventions) is now an error. |
| `data/funds/SCHEMA.md` | The fund record, year block, flow event, and optional blocks. |
| `data/funds/*.json` | 106 fund records. Six are curated and listed in the registry: `011`, `608`, `ACFR-park-tax`, `ACFR-equipment-maintenance-replacement`, `ACFR-workers-compensation`, `ACFR-zero-waste` (none has a `generated_by` key). The other 100 carry `"generated_by": "tools/acfr_funds.py"`. Files the extractor creates from now on also carry `"curation": {"status": "extracted", "policy": "append-only"}`; existing files were not migrated. |
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
- **Missing is `null`, never 0.** A dash on the statement is 0 (the City reported nothing); an unread field is `null`. The extractor does not write `null` for a required total, transfer or balance: if the label or its value is missing, or two aliases disagree, `required()` raises and the run stops.
- **Annual-row identity** is `(fy, basis, series, balance_version)`. `series` and `balance_version` are optional and unset on every existing row; they exist to separate a statistical-schedule series from fund statements and original from restated balances. Nothing infers them. Do not add `series` to any row until Steve decides the Marina convention (see `tools/EXTRACTION_SAFETY.md`).
- **Every year block and every flow cites a `source` id** present in the file's `sources` map, with a confidence tag (`High` = read from the cited primary document; `Moderate` = inference or secondary source; `Low` = unverified; `Unknown` = not retrieved).
- **Fund ids**: City fund numbers where known (`011` General, `501` Capital Improvement, `511` Measure T1, `608` Marina, `611` Sanitary Sewer); otherwise `ACFR-<slug of the statement column name>`. Names that would collide are mapped explicitly in `IDENTITIES`, keyed by (name, fund type): the Measure T1 and Measure O debt-service funds (`511-debt-service`, `ACFR-measure-o-housing-bond-debt-service`) and one GO 2015 refunding debt-service fund whose id keeps the legacy truncated slug. Any other collision raises; ids no longer depend on statement column order. These are FY2025 compatibility mappings, not a historical identity table. **Historical work needs a fund-identity table** (see open questions); do not rename existing ids.
- **Extraction is append-only.** For each fund, a new annual identity is appended along with its source entry; every other field (flows, curated text fields, status, obligations, assets, `flow_detail`, unknown fields) is left as it is. An existing annual identity is never rewritten: its financial fields (`revenue`, `expenditure`, `nonoperating`, `transfers_in`, `transfers_out`, `ending_balance`, `beginning_balance`) must equal the extracted values or the run stops. A field the extracted row has and the existing row lacks also counts as a conflict. The whole batch is checked before anything is written, so a conflict anywhere means no file changes. An identical rerun writes nothing.
- **Curated files are immutable to extraction.** The registry in `data/curation/protected-ledgers.json` (or an inline `curation.status: "curated"`) blocks every automated change to a ledger: no new annual rows, and no recreating it in an empty output directory. A conflicting value stops the run; it is not silently skipped. There is no force option. Changes to a curated ledger are manual and reviewed. A missing or unreadable registry stops the run.
- **Flows proposed by an agent** carry `reviewer: "agent:proposed"` and do not render. A person sets `reviewer` to their initials after checking.

## Reconciliation already in place (FY2025)

For every fund column: the sum of revenue line items equals the statement's "Total revenues" (or "Total operating revenues"), and the sum of expenditure line items equals "Total expenditures" (or "Total operating expenses"), to within $1. This was checked in the extraction session and is still not a committed test. Spot-checks against raw page text: General Fund, Park Tax, Equipment Maintenance, Central Services, Building Maintenance, Workers' Compensation, Marina, all match.

Committed since PR #10 (`tests/test_extraction_safety.py`, run in CI):

- **FY2025 equivalence regression.** A fresh extraction's annual rows, minus notes, must equal `tests/fixtures/fy2025-audited-values.json`. The fixture was produced by the unmodified extractor at `e51951c` and covers the 105 funds that extractor wrote (608 was skipped). The test also checks the PDF's SHA-256 against the fixture. This shows the safety changes left FY2025 output unchanged; it is not reconciliation against the audited statements, and it does not cover `flow_detail`.
- **Preservation.** The full extraction runs twice against a copy of `data/funds/`: zero files updated, every ledger byte-for-byte unchanged, the six protected ledgers included. CI then runs the real extraction against `data/funds/` and requires an empty `git diff` for `data/funds` and `docs`. The `docs` half only shows the extractor leaves the site alone; CI does not run the page builder.
- **Safety unit tests.** Merging keeps every existing field. A conflict in any financial field is an error. Duplicate annual identities are errors. A conflict anywhere in a batch prevents all writes. The registry blocks additions to protected ledgers and blocks recreating them. Conflicting source ids are errors. Required labels never default to null. Duplicate fund ids are errors. New files are created exclusively and existing files are replaced atomically.

Still not checked: balance roll-forward (beginning + net change = ending), cross-year continuity and restatements, fund columns against statement total columns, transfer totals across funds. These belong to the FY2024 pilot; see the requirements in `tools/EXTRACTION_SAFETY.md`.

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
- Before opening a PR that touches extraction or data, run what CI runs: `python -m pip install -r tests/requirements.txt` (pins `pdfplumber==0.11.9`; use a virtual environment), `python -m unittest discover -s tests -v`, `python tools/ledger.py data/funds/*.json`, `python tools/acfr_funds.py annual-comprehensive-financial-report-fy2025.pdf data/funds`, `git diff --exit-code -- data/funds docs`. For data changes, also regenerate pages and confirm none of the six registry ledgers changed unless the PR is a reviewed manual edit to one.
- Commit author email must be one the Vercel team recognizes (`info@counterfactual-designs.com`); Steve's repo config is set to it.
- Steve merges. Nobody enables auto-merge.

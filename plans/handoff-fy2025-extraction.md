# Technical handoff: the FY2025 fund extraction pipeline

*For whoever extends the audited fund data backward (plan deliverable 4b: the FY2024 pilot, then the historical phase). Written 2026-10-22 by Claude, who built it, and updated the same day for the extraction-safety layer merged in PR #10. Everything here is reproducible from the repository. The update policy itself is specified in `tools/EXTRACTION_SAFETY.md`; this handoff describes how the parts fit.*

## What it does, in one run

```
python3 tools/acfr_funds.py annual-comprehensive-financial-report-fy2025.pdf data/funds   # parses 106 funds; on the current data: "updated 0 files"
python3 tools/ledger.py data/funds/*.json                                                  # schema check
python3 tools/build_fund_page.py --all data/funds                                          # docs/fund-*.html + docs/data/funds/
python3 tools/build_funds_index.py data/funds docs/funds.html                              # fund browser
```

On the committed data the extractor changes nothing: every FY2025 row already exists and matches. It writes only when a fund file is missing, which is then created, or when a new annual identity appears, which is then appended. Any conflict exits nonzero with `EXTRACTION SAFETY ERROR: ...` before any file is written.

Dependencies: `pdfplumber==0.11.9` (pinned in `tests/requirements.txt`; the regression fixture depends on parser behavior), Python 3.10+ (CI uses 3.12). No OCR; the ACFR PDFs have a text layer.

## The statement pages used (FY2025 ACFR, PDF page numbers, not printed page numbers)

| Statement | Pages | Funds | Row labels |
|---|---|---|---|
| Statement of Revenues, Expenditures and Changes in Fund Balances, Governmental Funds | 77 | General, Grants, Library, Capital Improvement, Measure O Housing Bond, plus "Other" and "Total" columns (skipped) | revenue categories; expenditures by function; debt service; capital outlay; other financing sources/uses; fund balance July 1 / June 30 |
| Combining Statement … Nonmajor Governmental Funds | 237–254 (9 facing pairs) | 63 special revenue, 12 capital project, 10 debt service, plus subtotal columns (skipped) | same |
| Statement of Revenues, Expenses and Changes in Net Position, Proprietary Funds | 85–86 | 8 enterprise, plus "Total" and an "Internal Service Funds" aggregate (skipped) | operating revenues by line; operating expenses by object; non-operating; transfers; net position |
| Combining Statement … Internal Service Funds | 321–322 | 9 internal service | same as proprietary |

Not extracted: the balance sheets / statements of net position (219–236 nonmajor; 319 ISF; 81–84 proprietary), the budget-and-actual schedules (255–316), the fiduciary statements (327–336). The Marina ledger's balance sheet block was read by hand.

## How `acfr_parse.py` reads a page

1. `pdfplumber` words with x/y. Words are grouped into lines by `top` rounded to 3 px.
2. **Columns come from the `$` markers.** Statement rows that start or end a money block (the first revenue row, the fund-balance row) carry a `$` at the left edge of every column. The line with the most `$` tokens defines the column spans: span *j* runs from its `$` x-position to the next `$` minus 1. This is what makes all-dash columns survive (a column whose every value is "-" has no number to cluster on).
3. The **label boundary** is the first `$` minus 2 px. On a labeled (left) page that is ~178–310 px; on a continuation (right) page the first `$` is at ~55 px, so there are no labels. `labeled = label_x > 120`.
4. A **data line** is one with at least `max(2, columns/2)` tokens that are a dash or a comma-grouped number (or a number under 1,000). Years in header text ("2015 Refunding Bonds") have no comma and are 4 digits, so they do not trigger a data line; this matters for the debt-service pages.
5. **Fund names** are the header words between the "For the year ended" line and the first data line, assigned to the column whose span contains the word's center (fallback: nearest span start). Banner lines made only of words like "Special Revenue Funds" are skipped. Multi-line names are joined top to bottom. Result: readable but occasionally wrong word order on narrow columns; the two Equipment funds appear as one column titled "Equipment Maintenance Replacement" because the ACFR prints them as one.
6. **Values**: a numeric token goes to the column whose span contains its left edge; "-" becomes 0; "(1,234)" becomes −1234.
7. **Facing pages are joined by row order with drift tolerance** (`parse_pair`): walk the left page's data rows in order; for each, advance a pointer on the right page while its row y is more than 8 px above, and take the right row if within 8 px. Extra rows on either page (a label-only "Debt service:" line that has values on one page, a footer number) are skipped rather than forcing a match. Mismatches are reported to stderr with `verbose=True`; the affected right-page values stay `None`, and `required()` in `acfr_funds.py` then stops the run if the row is a required total.
8. **Hard failures (since PR #10).** `parse_pair` raises `SafetyError` when a page pair yields no fund columns, when a column name appears twice, or when a row label repeats for the same fund.

Each parsed pair returns `names`, `{fund_name: {row_label: value}}`, and the ordered `labels`.

## How `acfr_funds.py` turns rows into records

- `gov_record` reads governmental rows by label alias lists (`GOV_REV`, `GOV_EXP`, `OTHER_IN`, `OTHER_OUT`) into `revenue`, `expenditure`, `transfers_in`, `transfers_out`, `ending_balance`, `beginning_balance`, and the `flow_detail` inflows (revenue categories, kind `own`; transfers in, kind `rescue`; debt proceeds etc., kind `financing`) and outflows (functions; transfers out).
- `prop_record` does the same for proprietary rows (operating revenue lines; expense objects; investment earnings, capital grants, transfers in, interfund loan receipts), plus `nonoperating`.
- **Required labels.** Totals, transfers in and out, `nonoperating` and the balances are read through `required(d, *aliases)`. It raises if no alias is present, if the value is not an integer (including `None` from an unmatched facing-page row), or if two aliases carry different values. Line items for `flow_detail` are still optional lookups.
- **FY2025-specific labels.** The balance labels name the FY2025 dates (`Fund balance, June 30, 2025`, `July 1, 2024`). On page 77 the beginning balance is read from a bare `restated` label, which is the wrapped second line of the restated-balance row. Proprietary beginning balances prefer the "as restated" variants when present. All of this has to move into per-year configuration before another year can run.
- `make` builds the schema record: one `annual` block (`fy 2025`, `basis audited`, `source acfr-2025`, a note naming the statement and PDF page, and the beginning balance as text; `beginning_balance` is not written as a field), `flows: []`, `status.open_questions` saying only FY2025 is loaded, `"generated_by": "tools/acfr_funds.py"`, and `"curation": {"status": "extracted", "policy": "append-only"}`.
- `extract()` parses every statement and returns the full list of records. Nothing is written until `main()` passes that list to `ledger_safety.update_ledgers`.
- Fund type for nonmajor columns is assigned by position: everything before the "Total Special Revenue Funds" column is special revenue, between that and "Total Capital Project Funds" is capital project, after is debt service. Aggregate columns ("Total …", "Other Governmental Funds", "Internal Service Funds") are skipped.
- Ids: `IDENTITIES` maps (name, fund type) to an id first; then `NUMBERS` maps a few names to City fund numbers; others get `ACFR-` + slug (lowercase, non-alphanumerics to `-`, 48 chars). `IDENTITIES` holds the three FY2025 debt-service ids that used to come from the order-dependent `-<type>` suffix: `511-debt-service`, `ACFR-measure-o-housing-bond-debt-service`, and `ACFR-go-2015-refunding-bonds-for-go-2007-refunding-bo-debt-service`. The suffix rule is gone. Any other duplicate id raises.

## How records reach disk (`tools/ledger_safety.py`, since PR #10)

`update_ledgers(records, out_dir)` preflights the whole batch, then writes.

1. **Preflight.** For every record: reject duplicate or path-unsafe ids and symlinked targets, and check that the record's own annual rows have unique identities. If the file does not exist, it will be created, unless the id is protected, in which case the run stops. If the file exists, `merge` it.
2. **`merge` appends; it never rewrites.** Annual identity is `(fy, basis, series, balance_version)`.
   - An extracted row whose identity already exists is compared on `revenue`, `expenditure`, `nonoperating`, `transfers_in`, `transfers_out`, `ending_balance` and `beginning_balance`. Any field the extracted row carries must equal the existing value. An existing row that lacks the field counts as a conflict, not a gap to fill. On a match, the existing row, its note and its source stay authoritative and untouched.
   - A row with a new identity is appended with its source entry. A source id already present with different metadata is a conflict.
   - Nothing else in the file is read or changed.
3. **Protection.** Ids in `data/curation/protected-ledgers.json`, and files with an inline `curation.status: "curated"`, accept no new rows. Matching existing rows pass; anything else stops the run.
4. **Write.** Only if the entire preflight passes. New files are opened with exclusive create. Changed files are re-read, checked against the bytes seen at preflight, and replaced atomically through a temp file. Unchanged files are not touched. This is a single-writer tool: the preflight prevents partial writes from data conflicts, but it is not a transaction against disk failure or concurrent editors.

**What this means for the next year.** Run as it is, a FY2024 or earlier extraction will stop rather than corrupt anything:

- Three curated FY2024 rows lack `nonoperating`: Equipment, Workers' Compensation and Zero Waste. The extractor emits that field, so those rows count as conflicts.
- Any year missing from a protected ledger is an addition, and additions to protected ledgers are refused.
- Marina's FY2015–FY2023 statistical-schedule rows share an identity with fund-statement rows for the same years.

The pilot needs a read-only staging/report mode and per-year configuration first. The agreed requirements are listed at the end of `tools/EXTRACTION_SAFETY.md`.

## Reconciliation checks from the original build (still not committed as tests)

For each pair: Σ(revenue rows before "Total revenues") == Total revenues; Σ(expenditure rows between the totals, including "Capital outlay:") == Total expenditures; same for operating revenues/expenses on proprietary pages. All 106 columns reconciled within $1 (one $1 rounding difference, Alameda County Abandoned Vehicle fund). Spot-checks against `pdftotext -layout` page text for seven funds matched exactly.

Not checked: fund-balance roll-forward, transfers-in equals transfers-out across all funds (they should not, because fiduciary and component units are excluded), cross-year continuity.

## Committed tests (since PR #10)

`tests/test_extraction_safety.py`, 14 tests, run by `.github/workflows/extraction-safety.yml` on every PR and on pushes to `main`:

- **`FY2025Regression.test_equivalent_to_pre_safety_extractor`**: a fresh `extract()` reproduces `tests/fixtures/fy2025-audited-values.json`, which holds the annual rows (notes excluded) the unmodified extractor at `e51951c` wrote for 105 funds. The test also checks the PDF's SHA-256. It proves equivalence with the old extractor, not correctness against the audit, and it does not cover `flow_detail`.
- **`FY2025Regression.test_full_extraction_preserves_every_existing_ledger`**: two full update passes over a copy of `data/funds/` write nothing and leave every ledger byte-identical, including the six protected ones and Marina, whose FY2025 values are compared against the curated file.
- **Twelve `SafetyTests`** on the safety layer: evidence preservation, per-field conflicts, duplicate annual identities, distinct basis/series/balance_version identities, required labels, whole-batch abort, registry protection, source conflicts, validator duplicates, exclusive create and append on disk, missing statement labels, and duplicate fund ids.

After the tests, CI validates every ledger, runs the real FY2025 extraction into `data/funds`, and fails on any `git diff` in `data/funds` or `docs`. CI does not run the page builders.

## What will break on older ACFRs, probably

- **Different PDF producer.** FY2025 was produced with a text layer whose words have clean x/y. A scanned or differently rendered year will defeat `$`-span detection; check `page.extract_words()` output before assuming.
- **Different page numbers** every year. Locate statements by heading text (the session did this with a scan of `page.extract_text()[:300]` for the statement titles), never by fixed page numbers.
- **Row labels and categories** differ by year and by GASB changes (GASB 87 leases from FY2022 add "Inception of leases" lines; earlier years lack them).
- **Fund set differs.** Expect renamed, created, closed and merged funds. Build the identity table first; FY2025 names are the canonical ids today.
- **Ten-year statistical schedules** are not a shortcut: the FY2025 ACFR's are wrong (see AGENT_COORDINATION.md), and they carry totals by activity, not by fund.

## Where results go and what reads them

- `data/funds/<id>.json` is the source of truth. `docs/data/funds/<id>.json` is a published copy made by the page builder; never edit it directly.
- `build_fund_page.py` renders `annual` as the bar chart and table (one bar pair per year, projected years faded), `flow_detail` as the money-flow SVG, `flows` as the ledger table, and the optional blocks (`assets`, `balance_sheet`, `tot`) only when present. A fund with ≥2 audited years gets the "covered its costs in N of M years" sentence automatically.
- `build_funds_index.py` reads the FY2025 audited block for its columns; if history is added, decide whether the browser shows the latest year (current behavior) or a trend column.

## Reproducing the FY2025 run exactly

On current `main`, in a virtual environment:

```
python -m pip install -r tests/requirements.txt
python -m unittest discover -s tests -v                                              # 14 tests
python tools/ledger.py data/funds/*.json                                             # 106 OK
python tools/acfr_funds.py annual-comprehensive-financial-report-fy2025.pdf data/funds   # "Extracted 106 funds; updated 0 files"
git diff --exit-code -- data/funds docs
```

Do not point the extractor at an empty directory to "regenerate" the data. It refuses to recreate protected ledgers, by design. The pre-safety baseline can still be inspected at `e51951c` (merge of PR #8): run there, the old extractor rewrites every file except 608, including five curated ledgers.

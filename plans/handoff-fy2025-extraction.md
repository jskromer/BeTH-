# Technical handoff: the FY2025 fund extraction pipeline

*For whoever extends the audited fund data backward (plan deliverable 4b / the historical PR). Written 2026-10-22 by Claude, who built it. Everything here is reproducible from the repository.*

## What it does, in one run

```
python3 tools/acfr_funds.py annual-comprehensive-financial-report-fy2025.pdf data/funds   # 105 JSON files (608 kept)
python3 tools/ledger.py data/funds/*.json                                                  # schema check
python3 tools/build_fund_page.py --all data/funds                                          # docs/fund-*.html + docs/data/funds/
python3 tools/build_funds_index.py data/funds docs/funds.html                              # fund browser
```

Dependencies: `pdfplumber` 0.11 (word positions), Python 3.10+. No OCR; the ACFR PDFs have a text layer.

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
7. **Facing pages are joined by row order with drift tolerance** (`parse_pair`): walk the left page's data rows in order; for each, advance a pointer on the right page while its row y is more than 8 px above, and take the right row if within 8 px. Extra rows on either page (a label-only "Debt service:" line that has values on one page, a footer number) are skipped rather than forcing a match. Mismatches are reported to stderr with `verbose=True`.

Each parsed pair returns `names`, `{fund_name: {row_label: value}}`, and the ordered `labels`.

## How `acfr_funds.py` turns rows into records

- `gov_record` reads governmental rows by label alias lists (`GOV_REV`, `GOV_EXP`, `OTHER_IN`, `OTHER_OUT`) into `revenue`, `expenditure`, `transfers_in`, `transfers_out`, `ending_balance`, `beginning_balance`, and the `flow_detail` inflows (revenue categories, kind `own`; transfers in, kind `rescue`; debt proceeds etc., kind `financing`) and outflows (functions; transfers out).
- `prop_record` does the same for proprietary rows (operating revenue lines; expense objects; investment earnings, capital grants, transfers in, interfund loan receipts).
- `make` builds the schema record: one `annual` block (`fy 2025`, `basis audited`, `source acfr-2025`, note naming the statement and PDF page), `flows: []`, `status.open_questions` saying only FY2025 is loaded, and `"generated_by": "tools/acfr_funds.py"`.
- Fund type for nonmajor columns is assigned by position: everything before the "Total Special Revenue Funds" column is special revenue, between that and "Total Capital Project Funds" is capital project, after is debt service. Aggregate columns ("Total …", "Other Governmental Funds", "Internal Service Funds") are skipped.
- Ids: `NUMBERS` maps a few names to City fund numbers; others get `ACFR-` + slug (lowercase, non-alphanumerics to `-`, 48 chars). A second column with an id already written gets `-<type>` appended (`511-debt-service`, `ACFR-measure-o-housing-bond-debt-service`).
- `KEEP = {"608"}` prevents overwriting the Marina file. **Extend this to every curated file** (those without `generated_by`) before running against a new year, or better, make the extractor merge a new year block into an existing file instead of rewriting it. That merge does not exist yet; it is the first thing a historical extractor needs.

## Checks run during the build (not yet committed as tests)

For each pair: Σ(revenue rows before "Total revenues") == Total revenues; Σ(expenditure rows between the totals, including "Capital outlay:") == Total expenditures; same for operating revenues/expenses on proprietary pages. All 106 columns reconciled within $1 (one $1 rounding difference, Alameda County Abandoned Vehicle fund). Spot-checks against `pdftotext -layout` page text for seven funds matched exactly.

Not checked: fund-balance roll-forward, transfers-in equals transfers-out across all funds (they should not, because fiduciary and component units are excluded), cross-year continuity.

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

```
git checkout e51951c   # merge of PR #8
python3 tools/acfr_funds.py annual-comprehensive-financial-report-fy2025.pdf /tmp/funds-check
diff <(ls /tmp/funds-check) <(ls data/funds)     # same 106 ids
```
Then compare any generated file's `annual[0]` to the committed one; they match except for the six curated files, which carry extra years and flows.

# Financial dashboard: build, checks and regeneration

`docs/dashboard.html` is generated. Never edit it by hand. It is built by `tools/build_dashboard.py` from:

| Input | Owner | What |
|---|---|---|
| `data/funds/*.json` | extraction pipeline (Codex) | Fund ledgers. Read-only to the dashboard. |
| `data/curation/protected-ledgers.json` | Steve | Which ledgers are curated; only those carry BeTH readings on the dashboard. |
| `data/dashboard/statement-totals.json` | dashboard | Per year: each statement's own Total column (control totals), and the pages and labels for the fund-level check. |
| `data/dashboard/fund-statement-check.json` | dashboard (generated) | Result of `tools/verify_fund_statements.py --write`: which statement column each fund's figures were found in. |
| `data/dashboard/known-gaps.json` | dashboard | Documented line-item gaps, each to the dollar, with cause. |
| `data/dashboard/fiduciary-funds.json` | dashboard | The 17 fiduciary funds without ledger records (names and pages, no amounts). |

## Commands

```sh
python3 tools/build_dashboard.py                    # rebuild docs/dashboard.html
python3 tools/build_dashboard.py --check            # exit 1 if the page is stale or an integrity problem exists
python3 tools/verify_fund_statements.py             # fund-level check against the PDF (needs pdfplumber)
python3 tools/verify_fund_statements.py --write     # ...and record the result
python -m unittest tests.test_dashboard tests.test_dashboard_sources -v
```

## When the dashboard is regenerated

The dashboard is rebuilt **in its own PR**, never as a side effect of an extraction PR:

1. An extraction PR changes `data/funds/`. It is reviewed and merged on its own merits. The dashboard workflow posts an advisory warning ("Dashboard rebuild needed"); it does not block.
2. After that merge, a **dashboard rebuild PR** (branch `claude/dashboard-rebuild-<date>`) runs, in order:
   1. `tools/verify_fund_statements.py --write`. If a new audited year has been loaded, first add its pages, labels and control totals to `statement-totals.json`.
   2. `tools/build_dashboard.py`. Resolve every `PROBLEM` line it prints (see below).
   3. Commit `docs/dashboard.html` and any changed `data/dashboard/` files.
3. Steve merges the rebuild PR. Until then, the published page shows the previous data, internally consistent.

A new audited year needs no code change. It appears in the year selector once any fund has a statement row for it. Its totals and flows appear only when every fund in a group has a row; otherwise they are labeled "Incomplete: withheld". A complete year without control totals in `statement-totals.json` is labeled "Not reconciled" until they are added.

## What CI checks, and where

| Check | Workflow | Runs on | Blocks? |
|---|---|---|---|
| `tests/test_dashboard.py`: invariants (totals tie to controls, transfers balance and are not revenue, no cross-basis or internal-service double counting on the page, every expenditure dollar itemized or shown as not itemized, **no undocumented line-item gap**, links resolve, readings only for curated ledgers, year handling) | Extraction safety (`unittest discover`) | every PR | yes: these fail only if the data are wrong |
| `tests/test_dashboard_sources.py`: every fund's five figures match one column of its statement page; a one-dollar change is caught | Extraction safety | every PR | yes: same reason |
| `build_dashboard.py --check`: page reproduces exactly; no stale gap notes, no figure changed since the fund-level check, fiduciary roster consistent | Dashboard: `dashboard-reproducible` | PRs touching dashboard files | yes |
| `build_dashboard.py --check`, advisory | Dashboard: `dashboard-freshness` | PRs touching `data/funds/` only | no: warning annotation |

The shared tests are written to stay green when data legitimately change: a new year, a new fund, a fixed gap, a corrected value that still matches the PDF. Only the dashboard's own check requires the generated files to be current.

## Line items cannot disappear silently

A fund's money-flow lines (`flow_detail`) are compared with its audited totals. Three things make a loss visible:

1. **Totals are anchored to the PDF.** `test_dashboard_sources.py` re-reads the statement pages and fails if any fund's revenue, expenditures/expenses, transfers or ending balance differs from its statement column.
2. **Any gap between lines and totals fails the tests unless it is documented to the dollar** in `known-gaps.json` (`test_no_line_item_gap_is_undocumented`). A regeneration that drops a line therefore fails CI in the extraction PR itself.
3. **The page computes "not itemized" as total minus captured lines**, so a gap is always drawn, never absorbed. A documented gap also gets a prominent note at the top of the page.

**Limit:** these checks prove each fund's totals and that its lines sum to them. They do not prove the split between categories: a line filed under the wrong function with the right amount would pass. The review checklist includes a manual spot-check, and a per-line check against the statement rows is a candidate for the extraction pipeline's reconciliation.

When the extractor is fixed and a documented gap closes, the shared tests stay green. The dashboard check then reports the `known-gaps.json` entry as stale, and the next rebuild PR deletes it.

### Documented gaps (FY2025): none

All 106 funds now tie: every fund's captured lines add up to its audited totals, and `known-gaps.json` has no live entries.

The one gap this page ever carried is closed. $36,598,654 of governmental expenditures was not itemized by function, because on ACFR p.77 the row "Community development and housing" wraps onto two lines and the extractor read its values under the label "and housing"; "TRAN issuance costs" was also missing. By fund: General Fund $20,312,681, Grants $13,584,981, Capital Improvement $2,700,992. The corrections were applied to the three ledgers in `af21d8c` (PR #13), from the patches proposed in PR #11. Community development and housing now shows the statement's full $46,328,738.

The closure worked the way this document said it would: the shared tests stayed green, `build_dashboard.py --check` reported the three `known-gaps.json` entries as stale, and this rebuild retired them. The history is kept under the file's `resolved` key, which the builder does not read.

### Lease and subscription inception is not cash spending

The same corrections added the other-financing-source lines the ACFR reports against this activity: "Inception of leases and subscriptions", $24,560,677 across the governmental funds (General Fund $18,156,996, Grants $19,381, nonmajor $6,384,300). Under GASB 87 and 96 a fund records a lease or software subscription in full in the year it signs: as an expenditure inside capital outlay, and as an other financing source of the same amount. No cash moves and the fund takes on a liability.

So capital outlay is not all cash spending. Of FY2025's $61,222,721, $24,560,677 is inception; capital outlay excluding that identified inception is $36,662,044. The statement does not label that remainder as cash, and the pages do not call it cash: it is the total less the one non-cash item this page can identify from the other-financing-source line. The General Fund is the extreme case: $18,156,996 of its $19,679,684 capital outlay is inception. Both the dashboard (section 2) and the fund pages say so, and the fund pages draw other financing sources in their own colour, so they are read neither as the fund's own revenue nor as money another fund sent in.

## Accounting rules the page follows

- **Expenditures** (governmental, modified accrual) and **operating expenses** (enterprise and internal service, full accrual, include depreciation) are labeled separately and never combined.
- **Fund balance** (governmental) and **net position** (proprietary) are different measures. No figure on the page adds them; a test fails if any such sum appears.
- **Transfers** move money between City funds. They are never revenue or spending. Across the 106 funds, transfers in equal transfers out, and the page shows the check.
- **Internal service funds** bill other City funds. Their operating revenue is not added to any other group, because it would double-count charges already inside the paying funds' expenditures. Their operating expenses are shown as their own. Where an internal service fund billed nothing while incurring costs (in FY2025: Workers' Compensation, Public Liability, Catastrophic Loss), the page lists it with its transfers in.
- **Scope.** The figures are sums of fund columns before the statements' eliminations. They are not City-wide totals: the 17 fiduciary funds are excluded, and the governmental fund basis excludes capital assets and long-term liabilities.

# Independent review checklist: PR #12 (financial dashboard)

For a reviewer who did not build it. Each item is checkable from the repository and the FY2025 ACFR PDF, which is in the repo.

## Reproduce
- [ ] `python -m pip install -r tests/requirements.txt` in a fresh virtual environment, then `python -m unittest tests.test_dashboard tests.test_dashboard_sources -v`: all 27 pass. (A full `unittest discover -s tests` also reports 7 failures in `test_expenditure_breakdown.py`; those are on `main` and belong to Codex — see the last section.)
- [ ] `python tools/build_dashboard.py --check` prints "current; no integrity problems".
- [ ] `python tools/verify_fund_statements.py`: 106 of 106; leftover columns `{'governmental': 6, 'enterprise': 2, 'internal_service': 1}`.
- [ ] `git diff main --stat` touches no extraction tool, ledger, registry or `docs/index.html`. (It does touch `tools/build_fund_page.py` and 12 generated fund pages: see "Lease and subscription financing" below.)

## Numbers (spot-check against the PDF)
- [ ] Section 1 control totals against the printed Total columns: p.77 (governmental), p.86 (enterprise Total), p.322 (internal service Total). Differences shown: governmental expenditures +$1, fund balance −$2; enterprise net position −$1, non-operating +$1; internal service none.
- [ ] Pick three funds outside the six curated ones and compare the table row with the fund's statement column, including at least one facing (even-numbered) page.
- [ ] Transfers: $61,593,578 in and out across 106 funds.
- [ ] **Category split (not automated):** for two funds, compare their section 2 category lines (e.g. Taxes, Public safety) with the statement rows. The automated checks verify each fund's totals and that its lines add up to them, not which category each dollar is filed under.
- [ ] The $36,598,654 gap is closed, not hidden: the page shows no "not itemized" bar and no gap callout; the reconciliation table reads "106 of 106 funds tie"; `known-gaps.json` has `"years": {}`. Section 2's "Community development and housing" bar is the statement's full $46,328,738 (p.77).

## Lease and subscription financing

- [ ] Section 2's note "Capital outlay is not all cash spending": $61,222,721 outlay, $24,560,677 inception, $36,662,044 excluding that identified inception. The note must not call the remainder cash. The inception figure is the p.77 "Inception of leases and subscriptions" other-financing-source total; check the three components (General Fund $18,156,996, Grants $19,381, nonmajor $6,384,300).
- [ ] The inception amount is an other financing source, never added to revenue, and the matching expenditure is inside capital outlay, so no total double-counts it.
- [ ] `fund-011.html`: the diagram key reads "Transfers in $8.97M", **not** "rescue money $27.14M". The $18.16M of inception is in its own "other financing sources" colour, and the page carries the lease note.
- [ ] Other fund pages: inflows with `kind: "financing"` (lease inception, debt proceeds, bond premium, insurance recoveries, asset sales) are no longer drawn in the red transfers colour. The largest is `fund-ACFR-fire-admin-training-building-bond.html`, $10.25M of bond proceeds.
- [ ] The diagram key names the inflows present instead of calling them "rescue money". Every fund reads "Transfers in" except the Marina, whose red inflows are a State capital grant and a General Fund loan and are named as such. The `kind` values in the ledgers are unchanged.
- [ ] `fund-011.html`: the $2,477,099 Marina item is "Loan from the fund", not "Transfer out", and cites ACFR Note 4.A (p.79). The General Fund's audited transfers out are still $33,919,159 and total transfers across 106 funds are still $61,593,578.
- [ ] `fund-011.html` opening: the headline no longer says money was "borrowed back"; the text separates audited FY2024–FY2025 actuals from the FY2026 budget projection, says the FY2026 sources are different funds from the FY2024 destinations, and distinguishes transfers from the one actual loan.
- [ ] Terms box defines "Other financing sources" and "Inception of leases and subscriptions".

## Accounting presentation
- [ ] No figure adds fund balance to net position, or internal service revenue to another group (search the page for any combined number).
- [ ] Expenditures, operating expenses, transfers, fund balance and net position are each defined and used consistently (terms box; column headers).
- [ ] The scope box says these are not City-wide totals, and why.
- [ ] Section 4 (internal service funds) is accurate, including the three funds that billed nothing in FY2025 (Workers' Compensation: $0 revenue, $11,983,900 expenses, no transfers in; Public Liability and Catastrophic Loss: $0 revenue, funded by transfers in).
- [ ] BeTH readings appear only for the six curated ledgers and are labeled; open questions are labeled.
- [ ] The 17 fiduciary names match the column headings on pp.327–336.

## Failure behavior
- [ ] Delete one expenditure line from a generated fund's `flow_detail` in a scratch copy: `test_no_line_item_gap_is_undocumented` fails (`test_lost_line_item_is_caught` shows this).
- [ ] Change one FY2025 figure by $1 in a scratch copy: the fund-level check fails (`test_a_one_dollar_change_is_caught`).
- [ ] Add a partial year in a scratch copy: totals are withheld and labeled.

## Presentation
- [ ] Desktop (1280px) and phone (390px): no horizontal page scroll; the table scrolls inside its box with the fund name pinned.
- [ ] Filters (category, size, status including audit match), sorting, the four-fund compare (with the mixed-basis warning) and the year switch work.
- [ ] Every fund name links to an existing page.

## Not in scope (do not block on these)
- Homepage link: after approval, in a separate PR.
- Structured `beginning_balance`: requested in `plans/dashboard-requests-to-extraction.md` (R1). The p.77 extraction fix (R2) is done.
- Deficit and remediation trackers: `plans/dashboard-phase2-spec.md`.

## Known, out of scope for this PR

- `test_expenditure_breakdown.py` has 7 failures on `main`: the reconciler now finds no deficits because the corrections are applied. Codex owns this and has fixed it on `codex/post-correction-maintenance` (commit `8f77b36`, pre-correction fixtures). Not touched here.
- `build_fund_page.py` hardcodes `aria-label="Money in and out of the Marina Fund"` on every fund page. Real accessibility bug; fixing it regenerates 89 pages, so it belongs in its own PR.

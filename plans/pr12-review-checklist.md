# Independent review checklist: PR #12 (financial dashboard)

For a reviewer who did not build it. Each item is checkable from the repository and the FY2025 ACFR PDF, which is in the repo.

## Reproduce
- [ ] `python -m pip install -r tests/requirements.txt` in a fresh virtual environment, then `python -m unittest discover -s tests -v`: all pass.
- [ ] `python tools/build_dashboard.py --check` prints "current; no integrity problems".
- [ ] `python tools/verify_fund_statements.py`: 106 of 106; leftover columns `{'governmental': 6, 'enterprise': 2, 'internal_service': 1}`.
- [ ] `git diff main --stat` touches no extraction tool, ledger, registry or `docs/index.html`.

## Numbers (spot-check against the PDF)
- [ ] Section 1 control totals against the printed Total columns: p.77 (governmental), p.86 (enterprise Total), p.322 (internal service Total). Differences shown: governmental expenditures +$1, fund balance −$2; enterprise net position −$1, non-operating +$1; internal service none.
- [ ] Pick three funds outside the six curated ones and compare the table row with the fund's statement column, including at least one facing (even-numbered) page.
- [ ] Transfers: $61,593,578 in and out across 106 funds.
- [ ] The $36,598,654 gap: confirm the p.77 "Community development and housing" ("and housing") and "TRAN issuance costs" values for the General Fund, Grants and Capital Improvement.

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
- Structured `beginning_balance` and the p.77 extraction fix: requested in `plans/dashboard-requests-to-extraction.md`.
- Deficit and remediation trackers: `plans/dashboard-phase2-spec.md`.

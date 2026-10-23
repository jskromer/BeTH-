# Marina authorization presentation repair

Review proposal only. No merge or production deployment authorized. Baseline: main
`774569224be1ae59958b500e26f05b9fc6c13b9d`. This is the owner-requested manual
presentation correction to protected ledger 608; extraction protection and its
registry are unchanged. Shared page-builder, schema and validator edits are limited
to representing an authorization and explaining the Marina tally.

## Before and after

| Item | Before | Proposed |
| --- | --- | --- |
| `608-2023-07-25-wc-loan` | `loan_in`, counted as a Marina receipt/support | `authorization`, excluded from every receipt/support sum |
| Authorized principal | $5,500,000 | $5,500,000, retained as authorization only |
| Since-FY2022 ledger support tally | $23,331,168 ($23.33M displayed) | $17,831,168 ($17.83M displayed) |
| Tally description | Money moved in from other pockets | Recorded support including budgets and cost relief; not verified cash receipts |
| FY2025 General Fund financing | $2,477,099; speculative connection to 2023 authorization | $2,477,099 unchanged; no connection established |
| Authorization in obligations section | `interfund_loan`, $5,500,000 | `loan_authorization`, $5,500,000 authorized principal, not measured outstanding debt |
| Annual rows, audited flow detail, balance sheet, assets and TOT terms | Original approved values | Identical; canonical checksums pinned in regression fixture |

The original event ID, authorization date, fiscal year, amount, Council instrument,
repayment terms and source citation are preserved. No repayment, outstanding
principal, cancellation, new loan draw or General Fund transaction is inferred.
The separate General Fund and Workers' Compensation ledgers are unchanged.

The dashboard is regenerated solely to replace the stale Marina open question
about this authorization. Its financial figures, calculations, source-check hashes
and other funds are unchanged. The other 105 fund pages and JSON copies reproduce
unchanged; the fund browser also reproduces unchanged.

## Source-to-presentation evidence

| Stage | Exact source | What it establishes and what remains unknown |
| --- | --- | --- |
| Authorization | [July 25, 2023 Council minutes, Item 19, Resolution 70,997-N.S., meeting p.12 / PDF p.52](https://berkeleyca.gov/sites/default/files/documents/2023-09-12%20Item%2005%20Minutes%20for%20Approval.pdf#page=52); [original revised report, PDF p.1](https://berkeleyca.gov/sites/default/files/documents/2023-07-25%20Item%2019%205.5M%20Loan%20for%20D%20and%20E%20Dock%20Replacement%20-%20REV%20PRW.pdf#page=1) | Authorizes $5,500,000 from Workers' Compensation with Waterfront TOT repayment beginning FY2025 and $500,000 one-time interest. Approval date is not a disbursement date. |
| Intended route | [May 14, 2024 Item 3 revised appropriations amendment, Attachment 2, item 12 / PDF p.13 and item 76 / PDF p.18](https://berkeleyca.gov/sites/default/files/documents/2024-05-14%20Item%203%20AAO%20CMO%20Rev2.pdf#page=13) | Identifies Workers' Compensation 676 to General Fund 011, project PRWT122013, D and E docks. This is appropriations evidence, not a settlement voucher. |
| Audited outflow | [FY2024 ACFR printed pp.275-278 / PDF pp.311-314](https://berkeleyca.gov/sites/default/files/documents/annual-comprehensive-financial-report-fy2024.pdf#page=311) | Workers' Compensation reports $5,500,000 transfers out in its operating and cash-flow statements; no exact posting date established. |
| General Fund route | [FY2024 ACFR Note 4.B, printed p.79 / PDF p.115](https://berkeleyca.gov/sites/default/files/documents/annual-comprehensive-financial-report-fy2024.pdf#page=115) and [governmental statement, printed p.42 / PDF p.78](https://berkeleyca.gov/sites/default/files/documents/annual-comprehensive-financial-report-fy2024.pdf#page=78) | Note supports routing to General Fund but misleadingly groups the row beneath an Equipment Replacement heading. Listed GF inflows reconcile: $3,255,744 + $2,643,280 + $1,742,288 + $5,500,000 + $450,612 = $13,591,924. Confirm detailed journals before asserting the final expenditure route. |
| Marina receipt | [FY2024 ACFR printed pp.47, 51, 53 / PDF pp.83, 87, 89](https://berkeleyca.gov/sites/default/files/documents/annual-comprehensive-financial-report-fy2024.pdf#page=89) | Marina reports zero transfers in, interfund-loan receipts and due to other funds. These statements do not support a $5,500,000 Marina receipt. Project benefit is distinct from a fund receipt. |
| Separate FY2025 financing | [FY2025 ACFR cash flows, printed p.53 / PDF p.87](https://berkeleyca.gov/sites/default/files/2026-01/annual-comprehensive-financial-report-fy2025.pdf#page=87) and [Note 4.A, printed p.79 / PDF p.113](https://berkeleyca.gov/sites/default/files/2026-01/annual-comprehensive-financial-report-fy2025.pdf#page=113) | $2,477,099 interfund-loan receipts and matching amount due to General Fund; Note 4.A describes temporary negative-cash reclassifications. No source examined connects this to the 2023 authorization. |
| Receivable and repayment | [FY2024 ACFR printed pp.273-274 / PDF pp.309-310](https://berkeleyca.gov/sites/default/files/documents/annual-comprehensive-financial-report-fy2024.pdf#page=309); [FY2025 printed pp.283-288 / PDF pp.319-324](https://berkeleyca.gov/sites/default/files/2026-01/annual-comprehensive-financial-report-fy2025.pdf#page=319) | No $5,500,000 Workers' Compensation advance receivable is shown; FY2025 reports no transfers in or advance repayments. This neither cancels the authorization nor establishes outstanding principal. |

FY2024 Note 4.C, printed p.80 / PDF p.116, identifies the $813,779 principal
repayment as repayment of the separate 2017 building loan. It is not evidence of
repayment of this dock authorization. Contribution holidays likewise are not
identified loan repayments.

## Remaining support entries: not all are audited receipts

The corrected tally is arithmetically **$17,831,168**, consisting of these ten
unchanged events. Keeping them in the existing mixed support measure does not
upgrade them to independently verified cash receipts.

| Event(s) | Amount | Evidence / remaining verification |
| --- | ---: | --- |
| FY2025 State grant | $7,689,069 | FY2025 ACFR p.53 (PDF p.87); audited capital financing. |
| FY2025 General Fund financing | $2,477,099 | FY2025 ACFR pp.53, 79; audited financing, not operating revenue or a transfer. |
| FY2022 and FY2023 ARPA | $1,400,000 + $1,150,000 | [May 22, 2025 staff presentation, slide 5](https://berkeleyca.gov/sites/default/files/legislative-body-meeting-attachments/2025-05-22%20Item%2001%20Presentation%20-%20Marina%20Fund%20Update.pdf#page=5). Receiving-fund journal reconciliation remains unverified. |
| FY2024 cost shift | $800,000 | Same slide; noncash cost relief to Marina, absorbing funds unidentified. |
| FY2025 indirect reduction / holiday | $850,000 | Same slide; relief, not cash received. Existing allocation between indirect reduction and holiday is unverified. |
| FY2026 Parks Tax cost shift | $1,579,000 | [September 9, 2026 Waterfront presentation](https://berkeleyca.gov/sites/default/files/legislative-body-meeting-attachments/Suppl%20Communications%20-%20PRW%20Commission%20-%202026-09-09_0.pdf); staff-reported cost relief, journal implementation not independently verified here. |
| FY2026 indirect reduction / holiday | $360,000 | Same presentation; relief, not cash received; detailed allocation unverified. |
| FY2026 General Fund budget actions | $1,300,000 + $226,000 | [June 24, 2025 Item 24](https://berkeleyca.gov/sites/default/files/documents/2025-06-24%20Item%2024%20FY%202026%20Proposed%20Budget%20Update%20Adoption.pdf) and [November 18, 2025 Item 8 supplemental AAO](https://berkeleyca.gov/sites/default/files/documents/Supp%202-Rev%20Agenda%20Material%20Cover%20Memo-%20Consent%20Item%208_FY%2026%20Amendment%20to%20AAO_111825%20Council%20Meeting.pdf). Budget actions, not independently verified cash receipts. The existing note cites a $1,409,886 FY2026 total, so overlap or supersession remains unresolved. No amounts changed in this repair. |

Grouped: audited FY2025 financing $10,166,168; staff-reported ARPA $2,550,000;
noncash relief $3,589,000; FY2026 budget actions $1,526,000. Sum $17,831,168.
This review does not certify the remaining entries as a cash-receipt total.

## Documents still needed

- Journal vouchers and pooled-cash postings for Funds 676, 011 and 608, with dates.
- Executed internal-loan agreement and Finance's receivable accounting treatment.
- Dock project PRWT122013 funding, payment and asset-capitalization ledger.
- Waterfront TOT receipts, principal/interest allocations and repayment schedule.
- Year-end interfund reconciliation explaining Note 4.B and any relationship to
  the separate $2,477,099 balance.
- ARPA receiving-fund records, cost-relief allocation records and the FY2026
  General Fund transfer reconciliation to resolve the remaining support entries.

## Validation

- Complete suite: **84 tests passed**, including five new Marina regressions.
- Schema validator: **106 of 106 ledgers valid**.
- Independent FY2025 statement-column verification: **106 of 106 matched**.
- FY2025 extraction: **106 funds, zero files updated**.
- Current FY2025 reconciliation: **zero omitted expenditure/financing detail and
  zero correction proposals**.
- FY2024 pilot rerun: no ledger writes, zero reviewed-value conflicts; source
  additions and input checksums refreshed in staging only. Existing pilot review
  items are unchanged.
- Dashboard reproducibility: current, no integrity problems.
- Full fund-page and fund-browser regeneration: all other 105 fund pages and
  ledger copies, plus the browser, byte-for-byte unchanged.
- Against main: every annual block in all 106 ledgers is identical; every Marina
  flow amount is unchanged; the other five protected ledgers and the registry
  are byte-for-byte unchanged. Dashboard differs only by one Marina open question.
- Original FY2025 correction patches, checksums and historical fixtures unchanged.
- Repeated extraction, pilot and current reconciliation: byte-identical outputs.

GitHub CI results are reported on the pull request. No production deployment or
merge is part of this repair proposal.

# FY2024 audited-fund extraction and reconciliation pilot

**Staging only. Independent review pending. No publication or ledger update.**

Governmental and proprietary fund operating/change statements matching the existing BeTH ledger universe; fiduciary trusts, custodial funds and component-unit statements are outside this pilot.

Extracted **105** FY2024 funds; compared 6 protected ledgers. Fund statuses: {'PENDING REVIEW': 103, 'INCOMPLETE': 2}. 15 funds have nonzero reported FY2025 opening restatements. Status precedence is CONFLICT, INCOMPLETE, PENDING REVIEW, RECONCILED.

RECONCILED means the exact-dollar check passed. It does not authorize publication. PENDING REVIEW covers missing reviewed fields, unreviewed identities and explicit restatements. INCOMPLETE identifies unavailable evidence. CONFLICT retains both differing values. A shared statement-control conflict is not attributed as a value conflict to every member fund.

## Provenance

- FY2024: [annual-comprehensive-financial-report-fy2024.pdf](https://berkeleyca.gov/sites/default/files/documents/annual-comprehensive-financial-report-fy2024.pdf); retrieval: 2026-10-22; SHA-256 `5f794ea95c15b6ba83e8d233a04081f3b8304381fc2172e37006a39a1a8003b5`.
- FY2025: [annual-comprehensive-financial-report-fy2025.pdf](https://berkeleyca.gov/sites/default/files/2026-01/annual-comprehensive-financial-report-fy2025.pdf); retrieval: existing repository source; original retrieval date not recorded; SHA-256 `d6f54821affa11c04fcd1e6c4dd1a47715558ff2c2452d2321bc5884745ff7b3`.

Page references below are 1-based PDF pages. Printed pages are also recorded in the manifest.

## Findings requiring review

Comparable reviewed-value conflicts: 0. Equipment, Workers’ Compensation and Zero Waste lack reviewed `nonoperating` fields; all six lack structured reviewed beginning balances and net-change fields. These are review items, not value disagreements.

The FY2024 PDF has genuinely blank cells for Condo Conversion Program / General government (PDF p.230) and Measure B Paratransit / Private contributions and donations (p.232). Visual inspection confirmed the blanks. They remain null, so affected category sums and horizontal controls are incomplete.

The enterprise Total column has no published opening or closing net-position total (p.88). Those controls remain incomplete. The bridge to the internal-service summary compares common printed rows only; scope-specific enterprise categories absent from the combining statement are listed as not comparable.

FY2025 Note 15 (PDF pp.171–173) describes prior-period corrections and GASB 101 compensated absences. The report retains the FY2024 closing value, FY2025 original opening, stated adjustment and restated opening independently. No restatement is silently applied to FY2024.

## Statement totals and discrepancies

### Control 0: 2024 major_governmental: Other Governmental Funds — CONFLICT

PDF pages [78]; 83 member columns; 33 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| Private contributions and donations | missing | 322,970 | missing | INCOMPLETE |
| General government | missing | 4,977,017 | missing | INCOMPLETE |
| TRAN issuance costs | missing | 0 | missing | INCOMPLETE |
| Total expenditures | 101,089,904 | 101,089,903 | 1 | CONFLICT |
| Revenues over/(under) expenditures | 16,529,099 | 16,529,100 | -1 | CONFLICT |
| Inception of leases and subscriptions | missing | 0 | missing | INCOMPLETE |
| Net change in fund balance | 24,536,276 | 24,536,277 | -1 | CONFLICT |
| Fund balance, June 30, 2024 | 255,230,077 | 255,230,078 | -1 | CONFLICT |

### Control 1: 2024 major_governmental: Total Governmental Funds — CONFLICT

PDF pages [78]; 6 member columns; 33 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| Capital outlay: | 35,417,246 | 35,417,247 | -1 | CONFLICT |

### Control 2: 2024 nonmajor_governmental: Total Special Revenue Funds — CONFLICT

PDF pages [237, 238]; 61 member columns; 36 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| Private contributions and donations | missing | 322,970 | missing | INCOMPLETE |
| General government | missing | 2,851,339 | missing | INCOMPLETE |
| Net change in fund balance | 28,018,236 | 28,018,237 | -1 | CONFLICT |
| Fund balance, June 30, 2024 | 197,492,791 | 197,492,792 | -1 | CONFLICT |

### Control 3: 2024 nonmajor_governmental: Total Capital Project Funds — RECONCILED

PDF pages [241, 242]; 11 member columns; 36 row checks.

### Control 4: 2024 nonmajor_governmental: Total — RECONCILED

PDF pages [243, 244]; 11 member columns; 36 row checks.

### Control 5: 2024 nonmajor_governmental: Total Nonmajor — CONFLICT

PDF pages [243, 244]; 83 member columns; 36 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| Private contributions and donations | missing | 322,970 | missing | INCOMPLETE |
| General government | missing | 4,977,018 | missing | INCOMPLETE |
| Net change in fund balance | 24,536,276 | 24,536,277 | -1 | CONFLICT |
| Fund balance, June 30, 2024 | 255,230,077 | 255,230,078 | -1 | CONFLICT |

### Control 6: 2024 enterprise: Total — INCOMPLETE

PDF pages [87, 88]; 8 member columns; 42 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| Total net position - beginning | 237,040,292 | missing | missing | INCOMPLETE |
| Total net position - ending | 241,295,872 | missing | missing | INCOMPLETE |

### Control 7: 2024 enterprise: Internal Service Funds — RECONCILED

PDF pages [87, 88]; 9 member columns; 31 row checks.

Rows not common to both statements: Parking related revenues, Marina operations and maintenance, Sewer service fees, Clean storm water fees, Refuse service fees, Building permits, Other permits, Plan checking fees, Other fees, Lease revenues, Disposal of capital asset.

### Control 8: 2024 internal_service: Total — RECONCILED

PDF pages [311, 312]; 9 member columns; 31 row checks.

### Control 9: 2025 major_governmental: Other Governmental Funds — CONFLICT

PDF pages [77]; 84 member columns; 38 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| Private contributions and donations | missing | 298,384 | missing | INCOMPLETE |
| General government | missing | 4,648,901 | missing | INCOMPLETE |
| TRAN issuance costs | missing | 0 | missing | INCOMPLETE |
| Total expenditures | 121,098,354 | 121,098,353 | 1 | CONFLICT |
| Revenues over/(under) expenditures | -12,466,968 | -12,466,967 | -1 | CONFLICT |
| Debt issuance | missing | 10,220,000 | missing | INCOMPLETE |
| Premium on debt issuance | missing | 28,923 | missing | INCOMPLETE |
| Net change in fund balance | 11,158,073 | 11,158,074 | -1 | CONFLICT |
| previously reported | missing | 255,230,078 | missing | INCOMPLETE |
| Adjustments - See Note 15 | missing | 0 | missing | INCOMPLETE |
| restated | missing | 255,230,078 | missing | INCOMPLETE |
| Fund balance, June 30, 2025 | 266,388,150 | 266,388,152 | -2 | CONFLICT |

### Control 10: 2025 major_governmental: Total Governmental Funds — RECONCILED

PDF pages [77]; 6 member columns; 38 row checks.

### Control 11: 2025 nonmajor_governmental: Total Special Revenue Funds — INCOMPLETE

PDF pages [247, 248]; 61 member columns; 37 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| Private contributions and donations | missing | 298,384 | missing | INCOMPLETE |
| General government | missing | 2,708,470 | missing | INCOMPLETE |

### Control 12: 2025 nonmajor_governmental: Total Capital Project Funds — RECONCILED

PDF pages [251, 252]; 12 member columns; 37 row checks.

### Control 13: 2025 nonmajor_governmental: Total — RECONCILED

PDF pages [253, 254]; 11 member columns; 37 row checks.

### Control 14: 2025 nonmajor_governmental: Total Nonmajor — CONFLICT

PDF pages [253, 254]; 84 member columns; 37 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| Private contributions and donations | missing | 298,384 | missing | INCOMPLETE |
| General government | missing | 4,648,902 | missing | INCOMPLETE |
| Fund balance, July 1, 2024 | 255,230,077 | 255,230,078 | -1 | CONFLICT |
| Fund balance, June 30, 2025 | 266,388,150 | 266,388,151 | -1 | CONFLICT |

### Control 15: 2025 enterprise: Total — CONFLICT

PDF pages [85, 86]; 8 member columns; 44 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| Investment earnings | 5,040,483 | 5,040,482 | 1 | CONFLICT |
| Total nonoperating revenues (expenses) | 11,273,613 | 11,273,612 | 1 | CONFLICT |
| Income (loss) before transfers | 9,318,263 | 9,318,262 | 1 | CONFLICT |
| Total net position - ending | 248,103,563 | 248,103,564 | -1 | CONFLICT |

### Control 16: 2025 enterprise: Internal Service Funds — CONFLICT

PDF pages [85, 86]; 9 member columns; 31 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| General administration | 1,168,221 | 1,168,220 | 1 | CONFLICT |
| Total operating expenses | 63,434,532 | 63,434,531 | 1 | CONFLICT |
| Operating income (loss) | -18,678,840 | -18,678,839 | -1 | CONFLICT |
| Income (loss) before transfers | -16,937,496 | -16,937,495 | -1 | CONFLICT |
| Change in net position | -9,910,744 | -9,910,743 | -1 | CONFLICT |

Rows not common to both statements: Parking related revenues, Marina operations and maintenance, Sewer service fees, Clean storm water fees, Refuse service fees, Building permits, Other permits, Plan checking fees, Other fees, Lease revenues, Capital grants - State, Adjustment - see note 15, Total net position - beginning, as restated.

### Control 17: 2025 internal_service: Total — CONFLICT

PDF pages [321, 322]; 9 member columns; 33 row checks.

| Row | Calculated | Published | Difference | Status |
|---|---:|---:|---:|---|
| Change in net position | -9,910,744 | -9,910,743 | -1 | CONFLICT |
| Adjustment - See Note 15 | -631,796 | -631,797 | 1 | CONFLICT |
| Total net position - beginning balance as restated | 34,365,125 | 34,365,124 | 1 | CONFLICT |

## All-fund comparison

Values are integer dollars. Governmental revenue/expense use modified accrual; proprietary values use accrual operating revenue/expense. Transfers remain separate, with the printed signs retained in machine data. The complete raw label/value evidence, individual checks, existing source references and discrepancy details are in `funds.json` and `discrepancies.json`.

### 011 — General Fund

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: True. Accounting basis: modified_accrual.

Source: Statement of Revenues, Expenditures and Changes in Fund Balances, Governmental Funds; PDF [78]; column 1 (General Fund).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 261,782,686 | 261,782,686 |
| expenditure | 241,803,092 | 241,803,092 |
| transfers_in | 13,591,924 | 13,591,924 |
| transfers_out | 41,100,950 | 41,100,950 |
| beginning_balance | 158,467,144 | missing |
| net_change | -5,437,886 | missing |
| ending_balance | 153,029,258 | 153,029,258 |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 153,029,258; reported adjustment -276,283; restated 152,752,975; statement PDF [77]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: Reviewed record lacks beginning_balance; extracted value retained only in staging [beginning_balance]; Reviewed record lacks net_change; extracted value retained only in staging [net_change]; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 1.

### ACFR-grants — Grants

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Statement of Revenues, Expenditures and Changes in Fund Balances, Governmental Funds; PDF [78]; column 2 (Grants).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 48,965,125 | missing |
| expenditure | 44,635,685 | missing |
| transfers_in | 0 | missing |
| transfers_out | 3,255,744 | missing |
| beginning_balance | 60,013,153 | missing |
| net_change | 1,084,968 | missing |
| ending_balance | 61,098,121 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 61,098,121; reported adjustment 0; restated 61,098,121; statement PDF [77]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 1.

### ACFR-library — Library

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Statement of Revenues, Expenditures and Changes in Fund Balances, Governmental Funds; PDF [78]; column 3 (Library).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 25,344,600 | missing |
| expenditure | 23,853,914 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 22,845,766 | missing |
| net_change | 1,490,686 | missing |
| ending_balance | 24,336,452 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 24,336,452; reported adjustment 0; restated 24,336,452; statement PDF [77]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 1.

### 501 — Capital Improvement

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Statement of Revenues, Expenditures and Changes in Fund Balances, Governmental Funds; PDF [78]; column 4 (Capital Improvement).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 18,328 | missing |
| expenditure | 15,009,194 | missing |
| transfers_in | 18,370,905 | missing |
| transfers_out | 1,136,391 | missing |
| beginning_balance | 24,930,143 | missing |
| net_change | 2,243,648 | missing |
| ending_balance | 27,173,791 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 27,173,791; reported adjustment 0; restated 27,173,791; statement PDF [77]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 1.

### ACFR-measure-o-housing-bond — Measure O Housing Bond

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Statement of Revenues, Expenditures and Changes in Fund Balances, Governmental Funds; PDF [78]; column 5 (Measure O Housing Bond).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 1,110,434 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 78,298,477 | missing |
| net_change | 1,110,434 | missing |
| ending_balance | 79,408,911 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 79,408,911; reported adjustment 0; restated 79,408,911; statement PDF [77]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 1.

### ACFR-asset-forfeiture — Asset Forfeiture

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [227, 228]; column 1 (Asset Forfeiture).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 7,919 | missing |
| expenditure | 176,897 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 287,815 | missing |
| net_change | -168,978 | missing |
| ending_balance | 118,837 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 118,837; reported adjustment missing; restated missing; statement PDF [237, 238]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-measure-e-special-tax-for-disabled — Measure E: Special Tax for Disabled

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [227, 228]; column 2 (Measure E: Special Tax for Disabled).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 1,673,381 | missing |
| expenditure | 1,673,969 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 225,308 | missing |
| net_change | -588 | missing |
| ending_balance | 224,720 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 224,720; reported adjustment missing; restated missing; statement PDF [237, 238]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-workforce-investment-act — Workforce Investment Act

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [227, 228]; column 3 (Workforce Investment Act).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 14,143 | missing |
| transfers_in | 32,681 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 104,362 | missing |
| net_change | 18,538 | missing |
| ending_balance | 122,900 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 122,900; reported adjustment missing; restated missing; statement PDF [237, 238]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-community-workforce — Community Workforce

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [227, 228]; column 4 (Community Workforce).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 10,074 | missing |
| net_change | 0 | missing |
| ending_balance | 10,074 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 10,074; reported adjustment missing; restated missing; statement PDF [237, 238]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-sec-108-hud-loan-grant-assistance — Sec 108 Hud Loan Grant Assistance

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [227, 228]; column 5 (Sec 108 Hud Loan Grant Assistance).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 130,141 | missing |
| expenditure | 568,343 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 4,692,106 | missing |
| net_change | -438,202 | missing |
| ending_balance | 4,253,904 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 4,253,904; reported adjustment missing; restated missing; statement PDF [237, 238]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-fund-raising-activities — Fund Raising Activities

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [227, 228]; column 6 (Fund Raising Activities).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 259,477 | missing |
| expenditure | 45,574 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 657,748 | missing |
| net_change | 213,903 | missing |
| ending_balance | 871,651 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 871,651; reported adjustment missing; restated missing; statement PDF [237, 238]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-housing-finance-agency — Housing Finance Agency

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [227, 228]; column 7 (Housing Finance Agency).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 193,819 | missing |
| net_change | 0 | missing |
| ending_balance | 193,819 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 193,819; reported adjustment missing; restated missing; statement PDF [237, 238]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-gilman-sport-field — Gilman Sport Field

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [227, 228]; column 8 (Gilman Sport Field).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 284,712 | missing |
| expenditure | 296,580 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 97,854 | missing |
| net_change | -11,868 | missing |
| ending_balance | 85,986 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 85,986; reported adjustment missing; restated missing; statement PDF [237, 238]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-gilman-fields-reserve — Gilman Fields Reserve

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [227, 228]; column 9 (Gilman Fields Reserve).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 75,000 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 967,277 | missing |
| net_change | 75,000 | missing |
| ending_balance | 1,042,277 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,042,277; reported adjustment missing; restated missing; statement PDF [237, 238]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-animal-shelter — Animal Shelter

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [227, 228]; column 10 (Animal Shelter).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 46,194 | missing |
| expenditure | 16,801 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 114,526 | missing |
| net_change | 29,393 | missing |
| ending_balance | 143,919 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 143,919; reported adjustment missing; restated missing; statement PDF [237, 238]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-paramedic-assessment-district — Paramedic Assessment District

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [229, 230]; column 1 (Paramedic Assessment District).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 3,740,850 | missing |
| expenditure | 4,623,020 | missing |
| transfers_in | 757,924 | missing |
| transfers_out | 10,712 | missing |
| beginning_balance | 78,212 | missing |
| net_change | -134,958 | missing |
| ending_balance | -56,746 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original -56,746; reported adjustment missing; restated missing; statement PDF [239, 240]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-energy-commission — Energy Commission

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [229, 230]; column 2 (Energy Commission).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | -87 | missing |
| net_change | 0 | missing |
| ending_balance | -87 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original -87; reported adjustment missing; restated missing; statement PDF [239, 240]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-tieback-mitigation-r-o-w — Tieback Mitigation R-O-W

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [229, 230]; column 3 (Tieback Mitigation R-O-W).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,318,729 | missing |
| net_change | 0 | missing |
| ending_balance | 1,318,729 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,318,729; reported adjustment missing; restated missing; statement PDF [239, 240]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-domestic-violence-prevention-vital-statistics — Domestic Violence Prevention Vital Statistics

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [229, 230]; column 4 (Domestic Violence Prevention Vital Statistics).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 19,572 | missing |
| expenditure | 5,693 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 32,593 | missing |
| net_change | 13,879 | missing |
| ending_balance | 46,472 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 46,472; reported adjustment missing; restated missing; statement PDF [239, 240]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-affordable-housing-mitigation-fee — Affordable Housing Mitigation Fee

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [229, 230]; column 5 (Affordable Housing Mitigation Fee).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 10,716,307 | missing |
| expenditure | 542,368 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 45,290,461 | missing |
| net_change | 10,173,939 | missing |
| ending_balance | 55,464,400 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 55,464,400; reported adjustment missing; restated missing; statement PDF [239, 240]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-affordable-child-care — Affordable Child Care

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [229, 230]; column 6 (Affordable Child Care).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 83,852 | missing |
| expenditure | 14,007 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 484,958 | missing |
| net_change | 69,845 | missing |
| ending_balance | 554,803 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 554,803; reported adjustment missing; restated missing; statement PDF [239, 240]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-inclusionary-housing-program — Inclusionary Housing Program

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [229, 230]; column 7 (Inclusionary Housing Program).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 224,955 | missing |
| expenditure | 253,468 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 2,038,681 | missing |
| net_change | -28,513 | missing |
| ending_balance | 2,010,168 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 2,010,168; reported adjustment missing; restated missing; statement PDF [239, 240]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-condo-conversion-program — Condo Conversion Program

Status: **INCOMPLETE**; confidence: Unknown; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [229, 230]; column 8 (Condo Conversion Program).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 133,059 | missing |
| expenditure | 40,783 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 3,850,944 | missing |
| net_change | 92,276 | missing |
| ending_balance | 3,943,220 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: INCOMPLETE; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 3,943,220; reported adjustment missing; restated missing; statement PDF [239, 240]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: Required value unavailable; check cannot complete; No existing reviewed record for this year; no ledger write proposed; FY2025 comparator has independent extraction/reconciliation issues; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-parking-in-lieu-fee — Parking In-Lieu Fee

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [229, 230]; column 9 (Parking In-Lieu Fee).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,290,000 | missing |
| net_change | 0 | missing |
| ending_balance | 1,290,000 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,290,000; reported adjustment missing; restated missing; statement PDF [239, 240]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-playground-camp — Playground Camp

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [229, 230]; column 10 (Playground Camp).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 3,480,927 | missing |
| expenditure | 3,494,285 | missing |
| transfers_in | 0 | missing |
| transfers_out | 3,000 | missing |
| beginning_balance | 540,266 | missing |
| net_change | -16,358 | missing |
| ending_balance | 523,908 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 523,908; reported adjustment missing; restated missing; statement PDF [239, 240]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-state-proposition-172 — State Proposition 172

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [231, 232]; column 1 (State Proposition 172).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 1,231,430 | missing |
| expenditure | 1,178,438 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,584,495 | missing |
| net_change | 52,992 | missing |
| ending_balance | 1,637,487 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,637,487; reported adjustment missing; restated missing; statement PDF [241, 242]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-traffic-congestion-relief — Traffic Congestion Relief

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [231, 232]; column 2 (Traffic Congestion Relief).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 12 | missing |
| net_change | 0 | missing |
| ending_balance | 12 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 12; reported adjustment missing; restated missing; statement PDF [241, 242]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-state-transportation-tax — State Transportation Tax

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [231, 232]; column 3 (State Transportation Tax).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 6,866,493 | missing |
| expenditure | 4,855,895 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 6,658,469 | missing |
| net_change | 2,010,598 | missing |
| ending_balance | 8,669,067 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 8,669,067; reported adjustment missing; restated missing; statement PDF [241, 242]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-cdbg — CDBG

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [231, 232]; column 4 (CDBG).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 5,858,129 | missing |
| expenditure | 3,173,801 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 4,699,742 | missing |
| net_change | 2,684,328 | missing |
| ending_balance | 7,384,070 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 7,384,070; reported adjustment missing; restated missing; statement PDF [241, 242]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-rental-housing-safety-program — Rental Housing Safety Program

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [231, 232]; column 5 (Rental Housing Safety Program).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 2,802,573 | missing |
| expenditure | 1,851,625 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 3,305,648 | missing |
| net_change | 950,948 | missing |
| ending_balance | 4,256,596 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 4,256,596; reported adjustment missing; restated missing; statement PDF [241, 242]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-measure-b-local-streets-and-roads — Measure B: Local Streets and Roads

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [231, 232]; column 6 (Measure B: Local Streets and Roads).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 129,896 | missing |
| expenditure | 518,476 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 4,334,145 | missing |
| net_change | -388,580 | missing |
| ending_balance | 3,945,565 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 3,945,565; reported adjustment missing; restated missing; statement PDF [241, 242]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-measure-b-bike-and-pedestrian — Measure B: Bike and Pedestrian

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [231, 232]; column 7 (Measure B: Bike and Pedestrian).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 24,353 | missing |
| expenditure | 321,948 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 874,761 | missing |
| net_change | -297,595 | missing |
| ending_balance | 577,166 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 577,166; reported adjustment missing; restated missing; statement PDF [241, 242]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-measure-b-paratransit — Measure B: Paratransit

Status: **INCOMPLETE**; confidence: Unknown; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [231, 232]; column 8 (Measure B: Paratransit).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 2 | missing |
| expenditure | 123 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 0 | missing |
| net_change | -121 | missing |
| ending_balance | -121 | missing |

Checks: revenue_categories: INCOMPLETE; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original -121; reported adjustment missing; restated missing; statement PDF [241, 242]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: Required value unavailable; check cannot complete; No existing reviewed record for this year; no ledger write proposed; FY2025 comparator has independent extraction/reconciliation issues; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-measure-f-alameda-county-vrf-street-and-road — Measure F: Alameda County VRF Street and Road

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [231, 232]; column 9 (Measure F: Alameda County VRF Street and Road).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 631,023 | missing |
| expenditure | 379,564 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,155,599 | missing |
| net_change | 251,459 | missing |
| ending_balance | 1,407,058 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,407,058; reported adjustment missing; restated missing; statement PDF [241, 242]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-measure-bb-local-streets-and-roads — Measure BB: Local Streets and Roads

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [231, 232]; column 10 (Measure BB: Local Streets and Roads).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 8,650,328 | missing |
| expenditure | 9,051,136 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 10,534,567 | missing |
| net_change | -400,808 | missing |
| ending_balance | 10,133,759 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 10,133,759; reported adjustment missing; restated missing; statement PDF [241, 242]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-measure-bb-bike-and-pedestrian — Measure BB: Bike and Pedestrian

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [233, 234]; column 1 (Measure BB: Bike and Pedestrian).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 838,558 | missing |
| expenditure | 510,889 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 428,601 | missing |
| net_change | 327,669 | missing |
| ending_balance | 756,270 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 756,270; reported adjustment missing; restated missing; statement PDF [243, 244]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-measure-bb-paratransit — Measure BB: Paratransit

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [233, 234]; column 2 (Measure BB: Paratransit).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 853,165 | missing |
| expenditure | 1,072,405 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 826,073 | missing |
| net_change | -219,240 | missing |
| ending_balance | 606,833 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 606,833; reported adjustment missing; restated missing; statement PDF [243, 244]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-shelter-operations — Shelter Operations

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [233, 234]; column 3 (Shelter Operations).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 81,351 | missing |
| net_change | 0 | missing |
| ending_balance | 81,351 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 81,351; reported adjustment missing; restated missing; statement PDF [243, 244]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-one-time-funding — One Time Funding

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [233, 234]; column 4 (One Time Funding).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 469,436 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,165,835 | missing |
| net_change | 469,436 | missing |
| ending_balance | 1,635,271 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,635,271; reported adjustment missing; restated missing; statement PDF [243, 244]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-park-tax — Park Tax

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: True. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [233, 234]; column 5 (Park Tax).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 18,125,115 | 18,125,115 |
| expenditure | 15,103,645 | 15,103,645 |
| transfers_in | 0 | 0 |
| transfers_out | 45,244 | 45,244 |
| beginning_balance | 7,563,117 | missing |
| net_change | 2,976,226 | missing |
| ending_balance | 10,539,343 | 10,539,343 |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 10,539,343; reported adjustment missing; restated missing; statement PDF [243, 244]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: Reviewed record lacks beginning_balance; extracted value retained only in staging [beginning_balance]; Reviewed record lacks net_change; extracted value retained only in staging [net_change]; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-street-and-open-space-improvement — Street and Open Space Improvement

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [233, 234]; column 6 (Street and Open Space Improvement).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 509,610 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 2,441,792 | missing |
| net_change | 509,610 | missing |
| ending_balance | 2,951,402 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 2,951,402; reported adjustment missing; restated missing; statement PDF [243, 244]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-measure-gg-fire-preparation-tax — Measure GG: Fire Preparation Tax

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [233, 234]; column 7 (Measure GG: Fire Preparation Tax).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 5,660,079 | missing |
| expenditure | 4,847,676 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,920,651 | missing |
| net_change | 812,403 | missing |
| ending_balance | 2,733,054 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 2,733,054; reported adjustment missing; restated missing; statement PDF [243, 244]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-1st-response-advanced-life-support-alsfr — 1st Response Advanced Life Support (ALSFR)

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [233, 234]; column 8 (1st Response Advanced Life Support (ALSFR)).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | -5,998 | missing |
| net_change | 0 | missing |
| ending_balance | -5,998 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original -5,998; reported adjustment missing; restated missing; statement PDF [243, 244]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-street-lighting — Street Lighting

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [233, 234]; column 9 (Street Lighting).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 2,214,189 | missing |
| expenditure | 2,662,966 | missing |
| transfers_in | 0 | missing |
| transfers_out | 12,120 | missing |
| beginning_balance | 2,720,891 | missing |
| net_change | -434,767 | missing |
| ending_balance | 2,286,124 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 2,286,124; reported adjustment missing; restated missing; statement PDF [243, 244]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-business-economic-development — Business Economic Development

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [233, 234]; column 10 (Business Economic Development).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 94,184 | missing |
| expenditure | 6,122 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,418,839 | missing |
| net_change | 88,062 | missing |
| ending_balance | 1,506,901 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,506,901; reported adjustment missing; restated missing; statement PDF [243, 244]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-citywide-rlf — Citywide RLF

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [235, 236]; column 1 (Citywide RLF).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 6,723 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 794,483 | missing |
| net_change | 6,723 | missing |
| ending_balance | 801,206 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 801,206; reported adjustment missing; restated missing; statement PDF [245, 246]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-legacy-fund — Legacy Fund

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [235, 236]; column 2 (Legacy Fund).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 79,294 | missing |
| net_change | 0 | missing |
| ending_balance | 79,294 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 79,294; reported adjustment missing; restated missing; statement PDF [245, 246]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-miles-lab — Miles Lab

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [235, 236]; column 3 (Miles Lab).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 161,327 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 458,229 | missing |
| net_change | -161,327 | missing |
| ending_balance | 296,902 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 296,902; reported adjustment missing; restated missing; statement PDF [245, 246]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-employee-training — Employee Training

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [235, 236]; column 4 (Employee Training).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 819,850 | missing |
| transfers_in | 750,000 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 201,367 | missing |
| net_change | -69,850 | missing |
| ending_balance | 131,517 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 131,517; reported adjustment missing; restated missing; statement PDF [245, 246]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-uc-settlement — UC Settlement

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [235, 236]; column 5 (UC Settlement).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 4,507,873 | missing |
| expenditure | 3,854,168 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 5,066,667 | missing |
| net_change | 653,705 | missing |
| ending_balance | 5,720,372 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 5,720,372; reported adjustment missing; restated missing; statement PDF [245, 246]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-private-percent-art-fund — Private Percent- Art Fund

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [235, 236]; column 6 (Private Percent- Art Fund).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 293,373 | missing |
| expenditure | 654,093 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 3,506,596 | missing |
| net_change | -360,720 | missing |
| ending_balance | 3,145,876 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 3,145,876; reported adjustment missing; restated missing; statement PDF [245, 246]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-private-party-sidewalks — Private Party Sidewalks

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [235, 236]; column 7 (Private Party Sidewalks).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 310,755 | missing |
| expenditure | 333,157 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,533,814 | missing |
| net_change | -22,402 | missing |
| ending_balance | 1,511,412 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,511,412; reported adjustment missing; restated missing; statement PDF [245, 246]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-public-art — Public Art

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [235, 236]; column 8 (Public Art).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 22,056 | missing |
| transfers_in | 60,196 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 148,859 | missing |
| net_change | 38,140 | missing |
| ending_balance | 186,999 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 186,999; reported adjustment missing; restated missing; statement PDF [245, 246]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-lillie-b-wall-memorial — Lillie B. Wall Memorial

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [235, 236]; column 9 (Lillie B� Wall Memorial).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 735 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 14,612 | missing |
| net_change | 735 | missing |
| ending_balance | 15,347 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 15,347; reported adjustment missing; restated missing; statement PDF [245, 246]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-vital-and-health-statistic — Vital and Health Statistic

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [235, 236]; column 10 (Vital and Health Statistic).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 26,912 | missing |
| expenditure | 10,159 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 282,684 | missing |
| net_change | 16,753 | missing |
| ending_balance | 299,437 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 299,437; reported adjustment missing; restated missing; statement PDF [245, 246]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-east-bay-public-utilities-commission — East Bay Public Utilities Commission

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 1 (East Bay Public Utilities Commission).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 117 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 3,875 | missing |
| net_change | 117 | missing |
| ending_balance | 3,992 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 3,992; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-pers-savings — PERS Savings

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 2 (PERS Savings).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 1,741,082 | missing |
| expenditure | 44,049 | missing |
| transfers_in | 5,677,865 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 19,130,611 | missing |
| net_change | 7,374,898 | missing |
| ending_balance | 26,505,509 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 26,505,509; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-other-special-deposits — Other Special Deposits

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 3 (Other Special Deposits).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 0 | missing |
| net_change | 0 | missing |
| ending_balance | 0 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 0; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-health-state-aid-realignment — Health State Aid Realignment

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 4 (Health State Aid Realignment).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 2,123,114 | missing |
| expenditure | 935,021 | missing |
| transfers_in | 1,953,018 | missing |
| transfers_out | 2,643,280 | missing |
| beginning_balance | 5,414,423 | missing |
| net_change | 497,831 | missing |
| ending_balance | 5,912,254 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 5,912,254; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-tobacco-control — Tobacco Control

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 5 (Tobacco Control).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 301,766 | missing |
| expenditure | 298,684 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 120,195 | missing |
| net_change | 3,082 | missing |
| ending_balance | 123,277 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 123,277; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-mental-health-state-aid-realignment — Mental Health State Aid Realignment

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 6 (Mental Health State Aid Realignment).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 3,408,611 | missing |
| expenditure | 3,581,852 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 6,608,825 | missing |
| net_change | -173,241 | missing |
| ending_balance | 6,435,584 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 6,435,584; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-opt-public-safety — Opt. Public Safety

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 7 (Opt� Public Safety).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 411,464 | missing |
| expenditure | 82,838 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,051,957 | missing |
| net_change | 328,626 | missing |
| ending_balance | 1,380,583 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,380,583; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-fund-for-impounded-and-unneutered — Fund for Impounded and Unneutered

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 8 (Fund for Impounded and Unneutered).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 7,278 | missing |
| net_change | 0 | missing |
| ending_balance | 7,278 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 7,278; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-alameda-county-abandoned-vehicle-abatement-autho — Alameda County Abandoned Vehicle Abatement Authority

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 9 (Alameda County Abandoned Vehicle Abatement Authority).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 31,003 | missing |
| expenditure | 57,441 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 290,435 | missing |
| net_change | -26,438 | missing |
| ending_balance | 263,997 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 263,997; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-measure-ff-public-safety — Measure FF- Public Safety

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 10 (Measure FF- Public Safety).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 9,773,939 | missing |
| expenditure | 8,287,592 | missing |
| transfers_in | 0 | missing |
| transfers_out | 757,924 | missing |
| beginning_balance | 9,679,548 | missing |
| net_change | 728,423 | missing |
| ending_balance | 10,407,971 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 10,407,971; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### ACFR-fair-elections — Fair Elections

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [237, 238]; column 11 (Fair Elections).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 708,957 | missing |
| transfers_in | 612,210 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,096,567 | missing |
| net_change | -96,747 | missing |
| ending_balance | 999,820 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 999,820; reported adjustment missing; restated missing; statement PDF [247, 248]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 2, 5.

### 511 — Infrastructure & Facilities Measure T1

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [239, 240]; column 1 (Infrastructure & Facilities Measure T1).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 771,926 | missing |
| expenditure | 5,494,662 | missing |
| transfers_in | 0 | missing |
| transfers_out | 40,408 | missing |
| beginning_balance | 31,552,482 | missing |
| net_change | -4,763,144 | missing |
| ending_balance | 26,789,338 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 26,789,338; reported adjustment missing; restated missing; statement PDF [249, 250]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-phone-system-replacement — Phone System Replacement

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [239, 240]; column 2 (Phone System Replacement).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 238,282 | missing |
| transfers_in | 449,408 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,171,090 | missing |
| net_change | 211,126 | missing |
| ending_balance | 1,382,216 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,382,216; reported adjustment missing; restated missing; statement PDF [249, 250]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-fund-replacement — Fund Replacement

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [239, 240]; column 3 (Fund$ Replacement).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 1,887,219 | missing |
| transfers_in | 298,017 | missing |
| transfers_out | 0 | missing |
| beginning_balance | -354,899 | missing |
| net_change | -1,589,202 | missing |
| ending_balance | -1,944,101 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original -1,944,101; reported adjustment missing; restated missing; statement PDF [249, 250]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-public-education-and-government-access-facilitie — Public, Education and Government Access Facilities

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [239, 240]; column 4 (Public, Education and Government Access Facilities).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 124,902 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 2,459,393 | missing |
| net_change | 124,902 | missing |
| ending_balance | 2,584,295 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 2,584,295; reported adjustment missing; restated missing; statement PDF [249, 250]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-measure-g-fire-seismic-projects — Measure G: Fire Seismic Projects

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [239, 240]; column 5 (Measure G: Fire Seismic Projects).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 58 | missing |
| net_change | 0 | missing |
| ending_balance | 58 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 58; reported adjustment missing; restated missing; statement PDF [249, 250]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-measure-m-street-and-watershed-improvements — Measure M: Street and Watershed Improvements

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [239, 240]; column 6 (Measure M: Street and Watershed Improvements).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 26,660 | missing |
| expenditure | 135,335 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 944,818 | missing |
| net_change | -108,675 | missing |
| ending_balance | 836,143 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 836,143; reported adjustment missing; restated missing; statement PDF [249, 250]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-measure-g-public-safety-building — Measure G: Public Safety Building

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [239, 240]; column 7 (Measure G: Public Safety Building).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 189 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 6,268 | missing |
| net_change | 189 | missing |
| ending_balance | 6,457 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 6,457; reported adjustment missing; restated missing; statement PDF [249, 250]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-street-improvement — Street Improvement

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [239, 240]; column 8 (Street Improvement).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 2,688 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 89,315 | missing |
| net_change | 2,688 | missing |
| ending_balance | 92,003 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 92,003; reported adjustment missing; restated missing; statement PDF [249, 250]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-park-acquisition-development — Park Acquisition Development

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [239, 240]; column 9 (Park Acquisition Development).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 2,335 | missing |
| expenditure | 178 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 37,160 | missing |
| net_change | 2,157 | missing |
| ending_balance | 39,317 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 39,317; reported adjustment missing; restated missing; statement PDF [249, 250]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-income-housing-fund-west-improvement-project — Income Housing Fund: West Improvement Project

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [239, 240]; column 10 (Income Housing Fund: West Improvement Project).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 5,052 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 3,099,812 | missing |
| net_change | 5,052 | missing |
| ending_balance | 3,104,864 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 3,104,864; reported adjustment missing; restated missing; statement PDF [249, 250]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-income-housing-fund-savo-island-project — Income Housing Fund: Savo Island Project

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [241, 242]; column 1 (Income Housing Fund: Savo Island Project).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 441,140 | missing |
| net_change | 0 | missing |
| ending_balance | 441,140 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 441,140; reported adjustment missing; restated missing; statement PDF [251, 252]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 3, 5.

### ACFR-pension-refunding-bonds — Pension Refunding Bonds

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [241, 242]; column 3 (Pension Refunding Bonds).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 128,660 | missing |
| net_change | 0 | missing |
| ending_balance | 128,660 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 128,660; reported adjustment missing; restated missing; statement PDF [251, 252]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### ACFR-2009-measure-ff-library — 2009 Measure FF Library

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [241, 242]; column 4 (2009 Measure FF Library).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 1,670,328 | missing |
| expenditure | 1,340,087 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,678,665 | missing |
| net_change | 330,241 | missing |
| ending_balance | 2,008,906 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 2,008,906; reported adjustment missing; restated missing; statement PDF [251, 252]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### ACFR-go-2015-refunding-bonds-for-go-2007-refunding-bo — GO 2015 Refunding Bonds for GO 2007 Refunding Bonds

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [241, 242]; column 5 (GO 2015 Refunding Bonds for GO 2007 Refunding Bonds).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 2,505,492 | missing |
| expenditure | 2,046,411 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 2,441,598 | missing |
| net_change | 459,081 | missing |
| ending_balance | 2,900,679 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 2,900,679; reported adjustment missing; restated missing; statement PDF [251, 252]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### ACFR-repertory-theatre — Repertory Theatre

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [241, 242]; column 6 (Repertory Theatre).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 46 | missing |
| expenditure | 498,669 | missing |
| transfers_in | 499,804 | missing |
| transfers_out | 0 | missing |
| beginning_balance | -11,403 | missing |
| net_change | 1,181 | missing |
| ending_balance | -10,222 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original -10,222; reported adjustment missing; restated missing; statement PDF [251, 252]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### ACFR-go-2015-refunding-bonds-for-go-2002-refunding-bo — GO 2015 Refunding Bonds for GO 2002 Refunding Bonds

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [241, 242]; column 7 (GO 2015 Refunding Bonds for GO 2002 Refunding Bonds).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 460,780 | missing |
| expenditure | 376,196 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 1,317,325 | missing |
| net_change | 84,584 | missing |
| ending_balance | 1,401,909 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 1,401,909; reported adjustment missing; restated missing; statement PDF [251, 252]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### ACFR-go-2015-refunding-bonds-for-go-2007-refunding-bo-debt-service — GO 2015 Refunding Bonds for GO 2007 Refunding Bonds Series A

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [241, 242]; column 8 (GO 2015 Refunding Bonds for GO 2007 Refunding Bonds Series A).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 172,793 | missing |
| expenditure | 141,691 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 464,507 | missing |
| net_change | 31,102 | missing |
| ending_balance | 495,609 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 495,609; reported adjustment missing; restated missing; statement PDF [251, 252]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### ACFR-go-2015-refunding-bonds-for-go-2008-animal-shelt — GO 2015 Refunding Bonds for GO 2008 Animal Shelter Measure I

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [241, 242]; column 9 (GO 2015 Refunding Bonds for GO 2008 Animal Shelter Measure I).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 575,975 | missing |
| expenditure | 479,289 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 484,864 | missing |
| net_change | 96,686 | missing |
| ending_balance | 581,550 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 581,550; reported adjustment missing; restated missing; statement PDF [251, 252]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### ACFR-2010-cop-animal-shelter — 2010 COP Animal Shelter

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [243, 244]; column 1 (2010 COP Animal Shelter).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 139,900 | missing |
| transfers_in | 402,612 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 56,540 | missing |
| net_change | 262,712 | missing |
| ending_balance | 319,252 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 319,252; reported adjustment missing; restated missing; statement PDF [253, 254]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### ACFR-go-2014-measure-m-street-and-watershed-improveme — GO 2014 Measure M Street and Watershed Improvement

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [243, 244]; column 2 (GO 2014 Measure M Street and Watershed Improvement).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 2,159,907 | missing |
| expenditure | 1,632,512 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 2,840,036 | missing |
| net_change | 527,395 | missing |
| ending_balance | 3,367,431 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 3,367,431; reported adjustment missing; restated missing; statement PDF [253, 254]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### 511-debt-service — Infrastructure & Facilities Measure T1

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [243, 244]; column 3 (Infrastructure & Facilities Measure T1).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 4,607,802 | missing |
| expenditure | 4,656,831 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 7,194,886 | missing |
| net_change | -49,029 | missing |
| ending_balance | 7,145,857 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 7,145,857; reported adjustment missing; restated missing; statement PDF [253, 254]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### ACFR-measure-o-housing-bond-debt-service — Measure O Housing Bond

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: modified_accrual.

Source: Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds; PDF [243, 244]; column 4 (Measure O Housing Bond).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 5,759,752 | missing |
| expenditure | 4,870,758 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 5,176,931 | missing |
| net_change | 888,994 | missing |
| ending_balance | 6,065,925 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; revenues_over_expenditures: RECONCILED; other_financing_categories: RECONCILED; net_change_from_operations_financing: RECONCILED; next_year_original_beginning: RECONCILED.

FY2025 opening: original 6,065,925; reported adjustment missing; restated missing; statement PDF [253, 254]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; Shared statement control requires review; discrepancy is not attributed to this fund; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 0, 4, 5.

### ACFR-zero-waste — Zero Waste

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: True. Accounting basis: accrual.

Source: Statement of Revenues, Expenses and Changes in Net Position, Proprietary Funds; PDF [87, 88]; column 1 (Zero Waste).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 51,122,638 | 51,122,638 |
| expenditure | 56,538,745 | 56,538,745 |
| nonoperating | 1,552,187 | missing |
| transfers_in | 0 | 0 |
| transfers_out | 110,870 | 110,870 |
| beginning_balance | 4,743,893 | missing |
| net_change | -3,974,790 | missing |
| ending_balance | 769,103 | 769,103 |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 769,103; reported adjustment -419,510; restated 349,593; statement PDF [85, 86]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: Reviewed record lacks nonoperating; extracted value retained only in staging [nonoperating]; Reviewed record lacks beginning_balance; extracted value retained only in staging [beginning_balance]; Reviewed record lacks net_change; extracted value retained only in staging [net_change]; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 6.

### 608 — Marina Operations

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: True. Accounting basis: accrual.

Source: Statement of Revenues, Expenses and Changes in Net Position, Proprietary Funds; PDF [87, 88]; column 2 (Marina Operations).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 6,925,076 | 6,925,076 |
| expenditure | 7,326,968 | 7,326,968 |
| nonoperating | 10,033 | 10,033 |
| transfers_in | 0 | 0 |
| transfers_out | 24,109 | 24,109 |
| beginning_balance | 1,657,778 | missing |
| net_change | -415,968 | missing |
| ending_balance | 1,241,810 | 1,241,810 |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 1,241,810; reported adjustment -63,380; restated 1,178,430; statement PDF [85, 86]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: Reviewed record lacks beginning_balance; extracted value retained only in staging [beginning_balance]; Reviewed record lacks net_change; extracted value retained only in staging [net_change]; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 6.

### 611 — Sanitary Sewer

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Statement of Revenues, Expenses and Changes in Net Position, Proprietary Funds; PDF [87, 88]; column 3 (Sanitary Sewer).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 23,353,988 | missing |
| expenditure | 15,045,713 | missing |
| nonoperating | 2,287,867 | missing |
| transfers_in | 90,500 | missing |
| transfers_out | 193,022 | missing |
| beginning_balance | 175,936,771 | missing |
| net_change | 10,493,620 | missing |
| ending_balance | 186,430,391 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 186,430,391; reported adjustment -106,552; restated 186,323,839; statement PDF [85, 86]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 6.

### ACFR-clean-storm-water — Clean Storm Water

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Statement of Revenues, Expenses and Changes in Net Position, Proprietary Funds; PDF [87, 88]; column 4 (Clean Storm Water).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 4,460,037 | missing |
| expenditure | 4,048,657 | missing |
| nonoperating | 585,552 | missing |
| transfers_in | 40,408 | missing |
| transfers_out | 25,085 | missing |
| beginning_balance | 27,331,125 | missing |
| net_change | 1,012,255 | missing |
| ending_balance | 28,343,380 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 28,343,380; reported adjustment -12,938; restated 28,330,442; statement PDF [85, 86]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 6.

### ACFR-permit-service-center — Permit Service Center

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Statement of Revenues, Expenses and Changes in Net Position, Proprietary Funds; PDF [87, 88]; column 5 (Permit Service Center).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 20,234,664 | missing |
| expenditure | 23,018,376 | missing |
| nonoperating | 1,022,108 | missing |
| transfers_in | 0 | missing |
| transfers_out | 55,640 | missing |
| beginning_balance | 22,158,870 | missing |
| net_change | -1,817,244 | missing |
| ending_balance | 20,341,626 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 20,341,626; reported adjustment -156,343; restated 20,185,283; statement PDF [85, 86]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 6.

### ACFR-off-street-parking — Off-Street Parking

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Statement of Revenues, Expenses and Changes in Net Position, Proprietary Funds; PDF [87, 88]; column 6 (Off-Street Parking).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 5,461,628 | missing |
| expenditure | 6,005,061 | missing |
| nonoperating | -915,572 | missing |
| transfers_in | 0 | missing |
| transfers_out | 7,920 | missing |
| beginning_balance | 10,725,920 | missing |
| net_change | -1,466,925 | missing |
| ending_balance | 9,258,995 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 9,258,995; reported adjustment -237; restated 9,258,758; statement PDF [85, 86]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 6.

### ACFR-parking-meter — Parking Meter

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Statement of Revenues, Expenses and Changes in Net Position, Proprietary Funds; PDF [87, 88]; column 7 (Parking Meter).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 9,037,445 | missing |
| expenditure | 6,634,095 | missing |
| nonoperating | 126,397 | missing |
| transfers_in | 0 | missing |
| transfers_out | 1,750,938 | missing |
| beginning_balance | -1,705,102 | missing |
| net_change | 778,809 | missing |
| ending_balance | -926,293 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original -926,293; reported adjustment -81,126; restated -1,007,419; statement PDF [85, 86]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 6.

### ACFR-building-purchases-management — Building Purchases & Management

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Statement of Revenues, Expenses and Changes in Net Position, Proprietary Funds; PDF [87, 88]; column 8 (Building Purchases & Management).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 2,559,612 | missing |
| expenditure | 2,615,903 | missing |
| nonoperating | -297,886 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | -3,808,963 | missing |
| net_change | -354,177 | missing |
| ending_balance | -4,163,140 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original -4,163,140; reported adjustment -24,174; restated -4,187,314; statement PDF [85, 86]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately; Shared statement control requires review; discrepancy is not attributed to this fund.

Statement control references: 6.

### ACFR-equipment-maintenance-replacement — Equipment Maintenance Replacement

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: True. Accounting basis: accrual.

Source: Combining Statement of Revenues, Expenses and Changes in Net Position, Internal Service Funds; PDF [311, 312]; column 1 (Equipment Maintenance Replacement).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 19,717,617 | 19,717,617 |
| expenditure | 14,224,342 | 14,224,342 |
| nonoperating | 355,840 | missing |
| transfers_in | 1,581,700 | 1,581,700 |
| transfers_out | 500,000 | 500,000 |
| beginning_balance | 27,926,665 | missing |
| net_change | 6,930,815 | missing |
| ending_balance | 34,857,480 | 34,857,480 |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 34,857,480; reported adjustment -64,704; restated 34,792,776; statement PDF [321, 322]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: Reviewed record lacks nonoperating; extracted value retained only in staging [nonoperating]; Reviewed record lacks beginning_balance; extracted value retained only in staging [beginning_balance]; Reviewed record lacks net_change; extracted value retained only in staging [net_change]; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately.

Statement control references: 7, 8.

### ACFR-building-maintenance — Building Maintenance

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Combining Statement of Revenues, Expenses and Changes in Net Position, Internal Service Funds; PDF [311, 312]; column 2 (Building Maintenance).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 4,763,807 | missing |
| expenditure | 5,014,204 | missing |
| nonoperating | 106,732 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | -3,042,547 | missing |
| net_change | -143,665 | missing |
| ending_balance | -3,186,212 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original -3,186,212; reported adjustment 439,567; restated -2,746,645; statement PDF [321, 322]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately.

Statement control references: 7, 8.

### ACFR-central-services — Central Services

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Combining Statement of Revenues, Expenses and Changes in Net Position, Internal Service Funds; PDF [311, 312]; column 3 (Central Services).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 342,881 | missing |
| expenditure | 410,444 | missing |
| nonoperating | 0 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | -2,318 | missing |
| net_change | -67,563 | missing |
| ending_balance | -69,881 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original -69,881; reported adjustment -224; restated -70,105; statement PDF [321, 322]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately.

Statement control references: 7, 8.

### ACFR-computer-replacement — Computer Replacement

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Combining Statement of Revenues, Expenses and Changes in Net Position, Internal Service Funds; PDF [311, 312]; column 4 (Computer Replacement).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 6 | missing |
| nonoperating | 26 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 610 | missing |
| net_change | 20 | missing |
| ending_balance | 630 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 630; reported adjustment 0; restated 630; statement PDF [321, 322]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed.

Statement control references: 7, 8.

### ACFR-workers-compensation — Workers’ Compensation

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: True. Accounting basis: accrual.

Source: Combining Statement of Revenues, Expenses and Changes in Net Position, Internal Service Funds; PDF [311, 312]; column 5 (Workers’ Compensation).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | 0 |
| expenditure | 7,806,886 | 7,806,886 |
| nonoperating | 1,786,826 | missing |
| transfers_in | 813,779 | 813,779 |
| transfers_out | 5,500,000 | 5,500,000 |
| beginning_balance | 12,650,613 | missing |
| net_change | -10,706,281 | missing |
| ending_balance | 1,944,332 | 1,944,332 |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 1,944,332; reported adjustment -826,046; restated 1,118,286; statement PDF [321, 322]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: Reviewed record lacks nonoperating; extracted value retained only in staging [nonoperating]; Reviewed record lacks beginning_balance; extracted value retained only in staging [beginning_balance]; Reviewed record lacks net_change; extracted value retained only in staging [net_change]; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately.

Statement control references: 7, 8.

### ACFR-sick-leave-vacation-payouts — Sick Leave & Vacation Payouts

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Combining Statement of Revenues, Expenses and Changes in Net Position, Internal Service Funds; PDF [311, 312]; column 6 (Sick Leave & Vacation Payouts).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 3,832,757 | missing |
| expenditure | 2,981,978 | missing |
| nonoperating | 222,342 | missing |
| transfers_in | 0 | missing |
| transfers_out | 0 | missing |
| beginning_balance | 7,807,945 | missing |
| net_change | 1,073,121 | missing |
| ending_balance | 8,881,066 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original 8,881,066; reported adjustment 0; restated 8,881,066; statement PDF [321, 322]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed.

Statement control references: 7, 8.

### ACFR-public-liability — Public Liability

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Combining Statement of Revenues, Expenses and Changes in Net Position, Internal Service Funds; PDF [311, 312]; column 7 (Public Liability).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 538,340 | missing |
| expenditure | 4,693,726 | missing |
| nonoperating | -715 | missing |
| transfers_in | 4,895,888 | missing |
| transfers_out | 0 | missing |
| beginning_balance | -5,651,307 | missing |
| net_change | 739,787 | missing |
| ending_balance | -4,911,520 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original -4,911,520; reported adjustment -1,021; restated -4,912,541; statement PDF [321, 322]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately.

Statement control references: 7, 8.

### ACFR-catastrophic-loss — Catastrophic Loss

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Combining Statement of Revenues, Expenses and Changes in Net Position, Internal Service Funds; PDF [311, 312]; column 8 (Catastrophic Loss).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 0 | missing |
| expenditure | 6,676,509 | missing |
| nonoperating | 0 | missing |
| transfers_in | 6,673,794 | missing |
| transfers_out | 0 | missing |
| beginning_balance | -466,322 | missing |
| net_change | -2,715 | missing |
| ending_balance | -469,037 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original -469,037; reported adjustment 0; restated -469,037; statement PDF [321, 322]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed.

Statement control references: 7, 8.

### ACFR-it-cost-allocation-plan — IT Cost Allocation Plan

Status: **PENDING REVIEW**; confidence: Moderate; human review: PENDING REVIEW. Protected: False. Accounting basis: accrual.

Source: Combining Statement of Revenues, Expenses and Changes in Net Position, Internal Service Funds; PDF [311, 312]; column 9 (IT Cost Allocation Plan).

| Field | FY2024 extracted | Existing reviewed |
|---|---:|---:|
| revenue | 14,589,211 | missing |
| expenditure | 12,350,593 | missing |
| nonoperating | 0 | missing |
| transfers_in | 71,336 | missing |
| transfers_out | 450,612 | missing |
| beginning_balance | -3,909,279 | missing |
| net_change | 1,859,342 | missing |
| ending_balance | -2,049,937 | missing |

Checks: revenue_categories: RECONCILED; expenditure_categories: RECONCILED; balance_roll_forward: RECONCILED; operating_income: RECONCILED; nonoperating_categories: RECONCILED; income_before_transfers: RECONCILED; net_change_from_operations_transfers: RECONCILED; next_year_original_beginning: RECONCILED; next_year_restatement_bridge: RECONCILED.

FY2025 opening: original -2,049,937; reported adjustment -179,368; restated -2,229,305; statement PDF [321, 322]. A missing restated value means no separate restated row is printed, not a zero adjustment.

Issues: No existing reviewed record for this year; no ledger write proposed; FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately.

Statement control references: 7, 8.

## Existing ledger without an FY2024 column

- **INCOMPLETE**: ACFR-fire-admin-training-building-bond — Fire Admin Training Building Bond: Existing FY2025 ledger has no FY2024 column in the configured statements; creation/closure/identity must be reviewed.

## Batch errors

batch_errors: []

following_year_parse_errors: []

## Decisions requiring Steve’s approval

1. Resolve the published $1 governmental statement-control differences before historical integration; retain every audited value meanwhile.
2. Decide how to document genuinely blank statement cells; do not convert blanks into zero or insert balancing adjustments.
3. Review extracted-only nonoperating and beginning-balance fields. Their absence from reviewed records is a review item, not a financial conflict.
4. Approve historical identity mappings, including the combined Equipment 671/672 column, explicit legacy IDs and three text-layer name aliases. Investigate the FY2025 Fire Admin Training Building Bond with no FY2024 column.
5. Decide Marina series tagging separately. Keep FY2015–FY2023 statistical-schedule rows and all existing series fields unchanged during this pilot.
6. Review the FY2025 Note 15 restatements and preserve original FY2024 closing balances separately from FY2025 restated opening balances.
7. Confirm a separate scope and accounting model before extracting fiduciary trusts, custodial funds or component units; these are outside the existing governmental/proprietary ledger pilot.
8. Authorize historical integration only in a later PR after independent review; nothing in staging is approved for publication.

## Verification and reproduction

Run `python tools/acfr_pilot.py --out staging/fy2024`. Source PDFs must match the pinned checksums. No network calls occur during extraction. Use `--require-reconciled` to return exit 1 when any report review items remain. Exit 0 without that flag means report generation succeeded, not that the pilot passed financial review.

The run compares full local snapshots of `data/funds` and `docs` before and after extraction. The manifest records only explicitly listed extraction and verification inputs from `tools/acfr_years/pilot-inputs.json`; website files are not inventoried. Tests rerun extraction to verify deterministic reports and test ledger preservation, identity collisions, exact-dollar arithmetic, missing fields, explicit restatement bridges and collection of multiple problems.

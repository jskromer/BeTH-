# FY2025 page 77 expenditure breakdown: source-to-ledger reconciliation

**Proposals only — manual approval required. No ledger or published content was changed.**

Source: [annual-comprehensive-financial-report-fy2025.pdf](https://berkeleyca.gov/sites/default/files/2026-01/annual-comprehensive-financial-report-fy2025.pdf), FY2025, PDF p.77, printed p.42. SHA-256 `d6f54821affa11c04fcd1e6c4dd1a47715558ff2c2452d2321bc5884745ff7b3`.

Annual expenditure totals already include these amounts. Only the flow_detail/outflows categorization omitted them. Transfers and other financing uses are excluded from expenditure sums.

Total omitted: **$36,598,654**, across 3 funds.

| Fund | Existing expense breakdown | Housing omitted | TRAN costs omitted | Total omitted | Audited / corrected sum |
|---|---:|---:|---:|---:|---:|
| General Fund (011) | 256,629,243 | 20,221,797 | 90,884 | 20,312,681 | 276,941,924 |
| Grants (ACFR-grants) | 33,678,107 | 13,584,981 | 0 | 13,584,981 | 47,263,088 |
| Library (ACFR-library) | 26,186,710 | 0 | 0 | 0 | 26,186,710 |
| Capital Improvement (501) | 13,384,762 | 2,700,992 | 0 | 2,700,992 | 16,085,754 |
| Measure O Housing Bond (ACFR-measure-o-housing-bond) | 0 | 0 | 0 | 0 | 0 |

## Causes and scope

The PDF wraps “Community development and housing” across two lines, with the numeric values on the “and housing” line. The parser retains that final label; the expense builder previously required the full label and did not apply the existing year-specific alias. Separately, its expenditure whitelist omitted the printed “TRAN issuance costs” row. The fix applies the configured aliases to expense categories and explicitly includes TRAN issuance costs, with duplicate-alias protection.

The page’s Other Governmental Funds housing amount ($9,820,968) is an aggregate of nonmajor funds. It is not a separate ledger correction and must not be added again. Library and Measure O have zero housing and TRAN costs; they require no additions.

Year configurations already permit the corresponding FY2024 wrapped labels. The same fix recognizes those expense aliases, including wrapped interest/fiscal charges, when FY2024 records are generated. The FY2024 pilot already reconciles full source sections; its staged financial values remain unchanged.

## General Fund (011)

Status: PENDING REVIEW; protected: True; approval required: True. Baseline ledger SHA-256 `46128217f6fb7557d46d7148854ab3fd3a38e129f3aae71ab90ffdb8c8ddb162`.

| Source row label | Canonical category | Audited amount | Stored category amount | Proposed category amount |
|---|---|---:|---:|---:|
| General government | General government | 47,249,826 | 47,249,826 | 47,249,826 |
| Public safety | Public safety | 147,156,901 | 147,156,901 | 147,156,901 |
| Highway and streets | Highway and streets | 2,753,578 | 2,753,578 | 2,753,578 |
| Health and welfare | Health and welfare | 21,147,159 | 21,147,159 | 21,147,159 |
| Culture-recreation | Culture-recreation | 11,561,579 | 11,561,579 | 11,561,579 |
| and housing | Community development and housing | 20,221,797 | not stored | 20,221,797 |
| Economic development | Economic development | 4,581,909 | 4,581,909 | 4,581,909 |
| Principal repayment | Principal repayment | 1,392,206 | 1,392,206 | 1,392,206 |
| Interest and fiscal charges | Interest and fiscal charges | 1,106,401 | 1,106,401 | 1,106,401 |
| Debt issuance costs | Debt issuance costs | 0 | not stored | not stored |
| TRAN issuance costs | TRAN issuance costs | 90,884 | not stored | 90,884 |
| Capital outlay: | Capital outlay | 19,679,684 | 19,679,684 | 19,679,684 |

Source categories sum: 276,941,924; proposed expense sum: 276,941,924; audited total: 276,941,924; existing annual total: 276,941,924. Proposed difference: 0.

A missing stored zero category is shown as “not stored”; the source zero is explicit, never inferred. Transfers out remain in the proposed outflow array but are excluded from expense sums.

## Grants (ACFR-grants)

Status: PENDING REVIEW; protected: False; approval required: True. Baseline ledger SHA-256 `f64d16ad70b1e5513069b3876484a48577223d935fb728922e987a894464ce87`.

| Source row label | Canonical category | Audited amount | Stored category amount | Proposed category amount |
|---|---|---:|---:|---:|
| General government | General government | 1,772,841 | 1,772,841 | 1,772,841 |
| Public safety | Public safety | 1,968,701 | 1,968,701 | 1,968,701 |
| Highway and streets | Highway and streets | 1,024,467 | 1,024,467 | 1,024,467 |
| Health and welfare | Health and welfare | 24,028,923 | 24,028,923 | 24,028,923 |
| Culture-recreation | Culture-recreation | 993,674 | 993,674 | 993,674 |
| and housing | Community development and housing | 13,584,981 | not stored | 13,584,981 |
| Economic development | Economic development | 69,000 | 69,000 | 69,000 |
| Principal repayment | Principal repayment | 42,053 | 42,053 | 42,053 |
| Interest and fiscal charges | Interest and fiscal charges | 0 | not stored | not stored |
| Debt issuance costs | Debt issuance costs | 0 | not stored | not stored |
| TRAN issuance costs | TRAN issuance costs | 0 | not stored | not stored |
| Capital outlay: | Capital outlay | 3,778,448 | 3,778,448 | 3,778,448 |

Source categories sum: 47,263,088; proposed expense sum: 47,263,088; audited total: 47,263,088; existing annual total: 47,263,088. Proposed difference: 0.

A missing stored zero category is shown as “not stored”; the source zero is explicit, never inferred. Transfers out remain in the proposed outflow array but are excluded from expense sums.

## Library (ACFR-library)

Status: RECONCILED; protected: False; approval required: False. Baseline ledger SHA-256 `575be0c0a2b7e24eb9616ccdb8f04880b1e6f0c2ec933f3aec69ca349f6bd786`.

| Source row label | Canonical category | Audited amount | Stored category amount | Proposed category amount |
|---|---|---:|---:|---:|
| General government | General government | 0 | not stored | not stored |
| Public safety | Public safety | 0 | not stored | not stored |
| Highway and streets | Highway and streets | 0 | not stored | not stored |
| Health and welfare | Health and welfare | 0 | not stored | not stored |
| Culture-recreation | Culture-recreation | 25,924,974 | 25,924,974 | 25,924,974 |
| and housing | Community development and housing | 0 | not stored | not stored |
| Economic development | Economic development | 0 | not stored | not stored |
| Principal repayment | Principal repayment | 0 | not stored | not stored |
| Interest and fiscal charges | Interest and fiscal charges | 0 | not stored | not stored |
| Debt issuance costs | Debt issuance costs | 0 | not stored | not stored |
| TRAN issuance costs | TRAN issuance costs | 0 | not stored | not stored |
| Capital outlay: | Capital outlay | 261,736 | 261,736 | 261,736 |

Source categories sum: 26,186,710; proposed expense sum: 26,186,710; audited total: 26,186,710; existing annual total: 26,186,710. Proposed difference: 0.

A missing stored zero category is shown as “not stored”; the source zero is explicit, never inferred. Transfers out remain in the proposed outflow array but are excluded from expense sums.

## Capital Improvement (501)

Status: PENDING REVIEW; protected: False; approval required: True. Baseline ledger SHA-256 `4c0ff1b49f7f57845cfb1d411658979069e84f3ec6f2dfdd0f5716e406782b1f`.

| Source row label | Canonical category | Audited amount | Stored category amount | Proposed category amount |
|---|---|---:|---:|---:|
| General government | General government | 51,188 | 51,188 | 51,188 |
| Public safety | Public safety | 0 | not stored | not stored |
| Highway and streets | Highway and streets | 3,449,801 | 3,449,801 | 3,449,801 |
| Health and welfare | Health and welfare | 0 | not stored | not stored |
| Culture-recreation | Culture-recreation | 588,816 | 588,816 | 588,816 |
| and housing | Community development and housing | 2,700,992 | not stored | 2,700,992 |
| Economic development | Economic development | 8,539 | 8,539 | 8,539 |
| Principal repayment | Principal repayment | 0 | not stored | not stored |
| Interest and fiscal charges | Interest and fiscal charges | 0 | not stored | not stored |
| Debt issuance costs | Debt issuance costs | 0 | not stored | not stored |
| TRAN issuance costs | TRAN issuance costs | 0 | not stored | not stored |
| Capital outlay: | Capital outlay | 9,286,418 | 9,286,418 | 9,286,418 |

Source categories sum: 16,085,754; proposed expense sum: 16,085,754; audited total: 16,085,754; existing annual total: 16,085,754. Proposed difference: 0.

A missing stored zero category is shown as “not stored”; the source zero is explicit, never inferred. Transfers out remain in the proposed outflow array but are excluded from expense sums.

## Measure O Housing Bond (ACFR-measure-o-housing-bond)

Status: RECONCILED; protected: False; approval required: False. Baseline ledger SHA-256 `42e35e504cbc9446eee1c87d8bf5520f66c2c335e8f1d958c0bcb40c84f9d475`.

| Source row label | Canonical category | Audited amount | Stored category amount | Proposed category amount |
|---|---|---:|---:|---:|
| General government | General government | 0 | not stored | not stored |
| Public safety | Public safety | 0 | not stored | not stored |
| Highway and streets | Highway and streets | 0 | not stored | not stored |
| Health and welfare | Health and welfare | 0 | not stored | not stored |
| Culture-recreation | Culture-recreation | 0 | not stored | not stored |
| and housing | Community development and housing | 0 | not stored | not stored |
| Economic development | Economic development | 0 | not stored | not stored |
| Principal repayment | Principal repayment | 0 | not stored | not stored |
| Interest and fiscal charges | Interest and fiscal charges | 0 | not stored | not stored |
| Debt issuance costs | Debt issuance costs | 0 | not stored | not stored |
| TRAN issuance costs | TRAN issuance costs | 0 | not stored | not stored |
| Capital outlay: | Capital outlay | 0 | not stored | not stored |

Source categories sum: 0; proposed expense sum: 0; audited total: 0; existing annual total: 0. Proposed difference: 0.

A missing stored zero category is shown as “not stored”; the source zero is explicit, never inferred. Transfers out remain in the proposed outflow array but are excluded from expense sums.

## Manual decisions

1. Manually review and approve the four category additions for General Fund, Grants and Capital Improvement.
2. General Fund is protected. No protected ledger may be edited automatically; approve a separate manual change before application.
3. Any published breakdown correction requires a separately authorized publication step. No page builder or dashboard changes are part of this report.

Reproduce with `python tools/reconcile_expenditure_breakdown.py`. The machine-readable proposals contain the full existing and proposed outflow arrays and baseline hashes. No apply command is provided.

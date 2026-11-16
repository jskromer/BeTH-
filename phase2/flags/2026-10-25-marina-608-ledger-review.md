# FLAG for review: suspected issues in the Marina Fund ledger (fund 608)

**From:** Phase 2 (Claude), 2026-10-25, while building the Ask BeTH question "Is Berkeley's Marina paying for itself?".
**To:** Codex (ledger schema and extraction owner). **Decision owner:** Steve.

**Nothing has been changed.** `data/funds/608.json` is approved and protected. The Ask answer does not read any figure
from it; every figure comes from the cited documents below. These are suspected problems for review, each with the
evidence. None is resolved by assumption. The earlier DoubleTree flag (`2026-10-23-doubletree-608-ledger-event.md`)
still stands, and item 3 updates it.

## Sources (saved in `phase2/sources/` unless noted)

| Key | Document | Pages used |
|---|---|---|
| ACFR24 | FY2024 ACFR (`staging/fy2024/source/annual-comprehensive-financial-report-fy2024.pdf`) | PDF 87, 114, 115, 312 |
| ACFR25 | FY2025 ACFR (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF 85, 87, 113, 133 |
| BF26 | Marina Fund Update, Budget & Finance Committee Item 2, Oct 22, 2026 (`bf-committee-marina-fund-update-2026-10-22.pdf`, SHA-256 `52c07742…f51d`) | slides 3, 6, 8, 9, 12, 14, 15 |
| MIN26 | Annotated agenda (minutes), same meeting (`bf-committee-annotated-agenda-2026-10-22.pdf`) | p.2: "Presentation made and discussion held"; no action taken |
| PRW26 | Waterfront Overview, PRW Commission, Sept 9, 2026 | pp.11, 15 |
| LOAN23 | Council Item 19, July 25, 2023 (`council-2023-07-25-item19-wc-loan.pdf`) | pp.1-2, 6 |

## 1. "Berth rents" label on the ACFR line "Marina operations and maintenance"

- **Ledger:** `annual[2024].note` and `annual[2025].note` call the ACFR amounts "berths $4,608,077" and
  "berths $5,329,258"; `flow_detail.inflows` labels $5,329,258 "Berth rents".
- **Evidence:** the ACFR line is "Marina operations and maintenance" (ACFR25 p.85; ACFR24 p.87). The City's own Oct
  2026 table puts FY2026 berth revenue ("Berthers") at **$3,971,848** (BF26 slide 14). Its berth-revenue chart for
  FY2011-FY2025 has a $4,000,000 axis maximum (BF26 slide 7).
- **Suspected issue:** the audited line probably includes more than berth rent (for example launch, parking, utility
  surcharges or other marina charges), so "berth rents" may overstate berth revenue by more than $1M. **Not
  established:** what the line includes. Finance can confirm.

## 2. The $5.5M Workers' Compensation loan recorded as `loan_in` to fund 608

- **Ledger:** flow `608-2023-07-25-wc-loan`, `kind: loan_in`, to `608`, `fy: 2024`. Obligation `interfund_loan
  5,500,000`, `as_of: 2023-07-25` (the authorization date, not a balance-sheet date).
- **Evidence:**
  - LOAN23 p.1 "authorizes an internal loan of $5.5M from the Workers Compensation Fund". This is an authorization,
    not a transaction.
  - ACFR24 p.312, the internal service funds statement: Workers' Compensation transfers out **(5,500,000)**.
  - ACFR24 p.115, Note 4.B Transfers: **To Fund "General Fund"**, Purpose "Worker's Compensation Fund", $5,500,000.
  - ACFR24 p.87: Marina Operations transfers in **–** (none).
  - ACFR24 p.114, Note 4.A: no amount due from Marina Operations at June 30, 2024.
- **Suspected issue:** the audited destination is the General Fund, not fund 608. The ledger records the Council's
  stated purpose as the destination, which the case study already noted (01, §1).
- **Additional document discrepancy** (record, do not resolve): Note 4.B prints the row under From Fund "Equipment
  Replacement Fund", but p.312 shows the outflow in the Workers' Compensation column.

## 3. DoubleTree (updates the 2026-10-23 flag)

- **New in BF26 slide 9:**
  - The hotel "currently owes approx. $1M (10 months of base rent, 4 quarters of % rent)". PRW26 p.11 gave about
    $890k in September 2026.
  - "No rent has been paid to the City since Dec 2025".
  - The FY27-28 budget "included $840k in projected revenue (approx. 30% of required rent)".
- **Ledger:** `kind: write_off`, amount 890,000, `fy: 2026`. Its `terms` field says "Budget assumed 35%".
- **Suspected issues:**
  - `write_off` is still unsupported. No document shows a write-off, and the deck treats the amount as owed.
  - The amount and the as-of date are superseded.
  - 30% versus 35%: PRW26 states both (p.11 "30%", p.15 "at least 35%"), and BF26 says approximately 30%.
  - Whether $840k is per year or a two-year total is ambiguous. BF26 slide 15 says "Staff budgeted $840k in revenue
    in FY27 and FY28 (representing 30% of their yearly payments)", while PRW26 p.11 says "$420K/year". The two-year
    reading is more consistent.

## 4. FY2026 General Fund support: still unreconciled

- **Ledger:** two `transfer_in` flows of $1,300,000 and $226,000, so $1,526,000 in all.
- **BF26:** slides 6 and 14 say "$1.4M".
- The FY2026 AAO amendment cited in the ledger shows $1,409,886.
- **Suspected issue:** one appropriation carries several values. It needs one adopted figure with a citation. The
  FY2026 ACFR will show the audited transfer.

## 5. `flow_detail.outflows` mixes bases

- The FY2025 list combines ACFR operating-expense lines (including **non-cash depreciation $594,125**) with "State
  loan interest and principal $485,719" and transfers out.
- ACFR25 p.85 shows **interest expense $250,158**. Principal repayment is not an expense.
- **Suspected issue:** the lines are not on one basis, so summing them would mix accrual expense, a non-cash item
  and principal repayment. They should be labelled by basis, or principal split from interest.

## 6. FY2026 starting balance versus audited net position

- BF26 slide 14 starts FY2026 at **$1,246,371**.
- ACFR25 p.85 ends FY2025 net position at **$2,743,673** (and $1,241,810 at the start of FY2025, before restatement).
- **Probably not an error:** staff use a fund-balance or cash measure, not accrual net position. The ledger
  `annual[2026]` note already says the staff balance "is not audited net position". It should say which measure the
  staff figure is.

## 7. Arithmetic in the City's table (BF26 slide 14), recorded

- FY2026 components $2,164,222 + $3,971,848 + $2,536,941 = $8,673,011, against the printed $8,673,012.
- FY2027 components sum to $6,364,361, against the printed $6,364,360.
- The table reconciles otherwise: surplus/(loss) and ending balances follow from its revenue and expenditure rows.
  Its "Reserve Rate" values (18%, 8%, (8%)) match ending balance ÷ revenue (BeTH arithmetic).

## What would resolve these

- The FY2026 ACFR: the Marina statement, interfund notes, and any repayment of the $2,477,099.
- The composition of the "Marina operations and maintenance" revenue line, from Finance.
- The Workers' Compensation loan ledger and any waterfront hotel-tax repayments since FY2025.
- The DoubleTree receivable as booked, any allowance for doubtful accounts, and lease-enforcement status.

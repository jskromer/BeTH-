# Review note: the two 2023 Workers' Compensation authorizations and the one recorded transfer

**Status: review note, 2026-10-26.** Cross-reference for the Workers' Compensation and Marina reviews. It changes no approved ledger entry (`data/funds/ACFR-workers-compensation.json`, `data/funds/608.json`); any ledger change waits for the records in request item 3 and Steve's authorization.

## Four separate accounting events, to be kept apart

| Event | What it is | Where it is recorded | Status in the record |
|---|---|---|---|
| **Authorization** | Council directs that money may move | Annotated agenda, resolution | Two in 2023: $4,050,000 (June 13, 2023, toward the Measure T1 gap) and $5,500,000 (July 25, 2023, Res. 70,997-N.S., Marina D and E docks, repayable from Waterfront TOT) |
| **Actual transfer** | Cash leaves the fund | Fund statement, transfers note | One: $5,500,000 out of Workers' Compensation in FY2024, shown going to the General Fund (FY2024 ACFR, Note 4.B, p.115; fund statement p.312). The Marina Operations Fund shows no transfer in that year |
| **Project expenditure** | The dock contract is paid | Capital project accounts; Annual Street Report rows; CIP project sheets | Not traced to either authorization in any record BeTH holds |
| **Outstanding loan** | A receivable owed back to the fund | Due to/from note; advances schedule | None recorded at June 30, 2024 or June 30, 2025 for either authorization. The only Marina interfund balance at June 30, 2025 is $2,477,099 due to the General Fund |

## What the evidence establishes, and what it does not

- Council authorized **$9,550,000** from the fund in two separate 2023 actions. (High)
- The audited statements record **one $5,500,000 transfer out**, in FY2024, to the General Fund. (High)
- The evidence **does not establish which authorization that transfer implemented**: the Marina loan, the T1 gap, part of each, or something else. The amount matches the July resolution; the destination printed in the audit does not. (Unknown)
- `4,050,000` appears nowhere in the FY2024 or FY2025 ACFR. That is not proof the T1 action was never carried out; it may have been met from another source or through another fund. (Unknown)
- The FY2024 transfers note prints "Equipment Replacement Fund" in the From column of the $5,500,000 row while the fund statement carries the outflow in the Workers' Compensation column; the group total reconciles to the Workers' Compensation reading. A City labelling error is the likeliest explanation, but it is the City's to confirm. (Moderate)
- No repayment to Workers' Compensation is recorded through FY2025, and the fund billed departments nothing in FY2024 or FY2025 (operating revenue $0 both years; net position −$9,752,938 at June 30, 2025). (High)

## What the approved ledgers currently say, and why they are not changed here

- `608.json` records a `loan_in` of $5,500,000 from the Workers' Compensation Fund, with a note that the FY2024 ACFR shows no interfund loan to the Marina and the FY2025 ACFR shows $2,477,099 due to the General Fund.
- `ACFR-workers-compensation.json` records a `transfer_out` of $5,500,000 "to Waterfront D and E dock replacement (Marina)", with terms noting it was booked as a transfer, not a receivable.

Both entries record the Council's **purpose** as the destination. The audited **destination** is the General Fund. Which account is correct for the ledger is an open question flagged in `phase2/flags/2026-10-25-marina-608-ledger-review.md` and under independent investigation; per the extraction-safety rules, the entries stay as they are until that investigation reports and Steve authorizes a reviewed edit.

## Records that would settle it

Records request draft item 3 (`phase2/history/records-request-draft-2026-10-26.md`): journal entries, interfund receivable/payable schedules, loan agreements and repayment records for both actions, the source and destination funds, the project codes charged, and any Waterfront TOT repayment entries.

## Sources

- Council annotated agenda, June 13, 2023, p.11 ("Use $4,050,000 from the Workers Compensation Fund").
- Council Item 19, July 25, 2023, and Resolution 70,997-N.S.
- FY2024 ACFR: internal service combining statement p.312; Note 4.B transfers p.115; Note 4.C p.116.
- FY2025 ACFR: internal service combining statement p.322; Note 4.A due to/from p.113.
- Full working in `phase2/history/findings-2026-10-26-street-expenditures.md`, section 3 (B).

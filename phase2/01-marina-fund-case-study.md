# Marina Fund case study: reconciling the Berkeley Decision Project against BeTH's audited ledger

**Phase 2 deliverable 2 — draft, 2026-10-23**
**Status:** Research reconciliation. Contains no changes to BeTH's approved financial data.

## What this document is

Eric Fredericks' [Berkeley Decision Project](https://ericdf.github.io/berkeley-decision-project/waterfront-fund.html) assembled a waterfront financial record from roughly 29 primary City and State documents spanning FY1998–FY2026. BeTH holds a reconciled 106-fund audited ledger built from the FY2024 and FY2025 ACFRs.

The two sets overlap but are **not the same kind of evidence**. Eric's figures come mostly from budget documents, commission packets, State reports and planning studies. BeTH's come from audited financial statements. Where they disagree, the disagreement is usually not an error by either party — it is two different accounting concepts wearing the same label.

This document catalogs every overlap, states which are consistent, which conflict, and what must be resolved before any of it is published.

**Attribution.** Eric's work is cited throughout and his source references are preserved in `data/eric-waterfront-catalog.json`. His stated method — *"Every figure on this site traces to a primary document. Where a figure could not be reproduced from the source it is attributed to, it has been dropped and the omission stated on the page"* — is a high standard, and his page states omissions where he found them. BeTH nevertheless treats his figures as **research leads to verify**, not as audited evidence, because the public repository is generated output from a private source repository: his extraction steps cannot be re-executed, only his cited documents re-read.

---

## 0. Five distinctions this document holds open

Most confusion about the Marina Fund comes from collapsing one of these pairs. Each row is a
distinction the rest of this document maintains, and each has already produced at least one
mislabelled entry in a real ledger.

### A. Council authorization vs actual accounting transaction

An authorization is permission to act. A transaction is money moving and being recorded.
They have different dates, and sometimes the second never happens.

| | Authorization | Transaction |
|---|---|---|
| Evidence | Council item, resolution, minutes | ACFR statement line, interfund note, fund balance |
| Date | When Council voted | When the entry was booked |
| Marina example | $5,500,000 Workers' Compensation loan, **authorized 2023-07-25** | **No receivable for it appears in the FY2025 ACFR** |

**Rule.** A BeTH entry sourced to a Council item records an authorization. Only an ACFR line
records a transaction. A stated *purpose* ("for D and E dock replacement") is never evidence of a
*destination*.

### B. Loans vs transfers vs receivables vs repayments

Four mechanisms, four different balance-sheet consequences:

| Mechanism | Creates an obligation to repay? | Where it appears |
|---|---|---|
| **Transfer** | No | Transfers in / transfers out on the operating statement |
| **Loan** | Yes | A liability in the borrowing fund, a receivable in the lending fund |
| **Receivable** | Yes, owed to the holder | Due to/from other funds (ACFR Note 4.A) |
| **Repayment** | Extinguishes one | Reduces both sides |

Berkeley has produced at least two ledger entries where the `kind` field contradicts the
evidence in the same record:

- **$2,477,099 Marina item** — recorded as `transfer_out` while its own note said "a receivable
  the GF expects back." **Corrected in Phase 1** to `loan_out` after confirming ACFR Note 4.A.
- **$890,000 DoubleTree item** — recorded as `write_off` while its own `terms` field says
  *"Not written off; recorded here as revenue at risk."* See §9.

### C. Audited actuals vs adopted budgets vs projections

| Class | Source | Marina example |
|---|---|---|
| **Audited actual** | ACFR, tied to a statement column | FY2025 revenue $7,594,812 |
| **Adopted budget** | Adopted budget or AAO | FY2026 General Fund transfer (four competing figures, §4) |
| **Projection** | Forecast for an unaudited year | FY2028 ending balance −$545,586 |

FY2025 is the latest audited year. **Every FY2026 Marina figure in circulation is a projection or
a budget figure, including ones published as "actual."**

### D. Boating vs non-boating expense

A cost-allocation *estimate*, not an accounting classification. It exists only in the State's June
2023 report, which the State itself called *"an informal report prepared at DBW's request"* based on
*"estimated workloads."* The ACFR has no such dimension and neither does BeTH's ledger. It is the
most analytically useful frame available and the least auditable. Both things are true.

### E. Cash expenditure vs capital contribution vs non-cash entry

Not every dollar in the expense column left the City's bank:

| Type | FY2025 Marina example | Cash moved? |
|---|---|---|
| Cash operating expenditure | Staff and benefits $4,179,607 | Yes |
| Internal charge | City central charges (indirect) $706,259 | Yes, to another City fund |
| **Non-cash entry** | **Depreciation $594,125** | **No** |
| Debt service | State loan interest and principal $485,719 | Yes |
| Capital funded by grant | State capital grant $7,689,069 inflow | Yes, but restricted to capital |

FY2025 audited expense of $13,573,896 is nearly double FY2024 because of grant-funded dock and pile
capital work. **Reading that as an operating blowout would be wrong.** Of the FY2025 outflows,
$594,125 is depreciation, which never moved.

---

## 1. The headline finding: a $5.5M loan that no statement records as owed

This is the most consequential thing in Eric's analysis, and **BeTH can independently corroborate it.**

**The sequence.** In June 2023 the California Division of Boating and Waterways reviewed Berkeley's application for a State loan to replace the D and E docks. It found the City was using an enterprise fund to carry non-revenue-generating activity — *"This is not how enterprise funds are typically used"* — and told the City to either post additional security or move non-boating costs off the Marina Fund. On July 25, 2023 the Council instead authorized a **$5,500,000 internal loan from the Workers' Compensation Fund** at 2.8%, roughly $500,000 of total interest, to be repaid at about $1,000,000 a year from waterfront hotel tax starting FY2025.

**Eric's finding.** The $5.5M moved from the Workers' Compensation Fund to the **General Fund** in FY2024; no loan receivable was recorded in the audited statements; no repayment is documented through FY2025. His conclusion: *"The internal loan is cheaper than the State loan only if it is repaid, and the audited statements do not record it as owed."*

**BeTH's independent verification.** Reading the FY2025 ACFR directly:

| Check | Result |
|---|---|
| Does `5,500,000` appear anywhere in the FY2025 ACFR? | **No. Not once.** |
| Note 4.A *Due To/From Other Funds* at 2025-06-30 (p.79) | Lists **only** $2,477,099 due from Marina Operations to the General Fund. No Workers' Compensation receivable of any size. Total due to/from: $23,193,295. |
| Marina Fund audited transfers **in**, FY2024 | **$0** |
| Workers' Compensation audited transfers **out**, FY2024 | **$5,500,000** |

So $5.5M demonstrably left the Workers' Compensation Fund in FY2024, the Marina received no transfer in that year, and no receivable for it exists at June 30, 2025. Eric's reading is supported by the audited record.

**Where BeTH's own ledger is now in question.** BeTH records this as `loan_in $5,500,000` from Workers' Compensation **to the Marina (608)**, and the Workers' Compensation ledger describes its matching `transfer_out` as *"Waterfront D and E dock replacement (Marina)."* That is the Council's stated **purpose**, which BeTH appears to have recorded as the **destination**. BeTH's own supporting evidence is weak on this point: the 608 obligation entry is dated `as_of 2023-07-25` — the authorization date — not a balance-sheet date, unlike the $2,477,099 entry which is properly dated `2025-06-30`.

> **Status: under independent investigation by Codex. NOT resolved, and nothing in this document assumes an outcome.**
>
> This is exactly the loan/transfer confusion of distinction B, at more than twice the size of the $2,477,099 item Phase 1 corrected. Resolving it requires the FY2024 ACFR interfund note and the FY2024/FY2025 Workers' Compensation fund statements. **BeTH's approved ledgers have not been changed and must not be until that investigation reports.**
>
> What can be said now, and no more: $5.5M left the Workers' Compensation Fund in FY2024; the Marina recorded no transfer in that year; and no receivable for it exists at 2025-06-30. Which of the two destination accounts is correct is an open question, not a finding.

**Why it compounds.** The Workers' Compensation Fund is not healthy enough to absorb this:

| | FY2024 audited | FY2025 audited |
|---|---:|---:|
| Operating revenue | $0 | $0 |
| Operating expenses | $7,806,886 | $11,983,900 |
| Transfers in | $813,779 | $0 |
| Transfers out | $5,500,000 | $0 |
| **Ending net position** | **$1,944,332** | **−$9,752,938** |

Two consecutive contribution "holidays" (no workers' compensation charges billed to departments) produced $0 revenue against $11.98M of claims expense, and net position fell to **negative $9.75M**. A further **$5,187,019** is budgeted to move from this fund to the General Fund in FY2026 — which Eric reports as "$5.2M" and BeTH carries at the exact budgeted figure. Both agree on this one.

A fund with negative net position, no revenue, and an unrecorded $5.5M claim against the waterfront is a solvency question in its own right, independent of the Marina.

> **Cross-reference added 2026-10-26** (from the streets history investigation, `phase2/history/findings-2026-10-26-street-expenditures.md` §3, and `phase2/review/workers-compensation-authorizations-2026-10-26.md`). The $5.5M resolution was not the only 2023 call on this fund. Council authorized **$4,050,000** from Workers' Compensation on June 13, 2023 toward the Measure T1 funding gap, and **$5,500,000** on July 25, 2023 for the Marina docks: two separate actions, $9,550,000 in all. The FY2024 audit records **one** $5,500,000 transfer out, to the General Fund; `4,050,000` appears in neither the FY2024 nor the FY2025 ACFR. The evidence therefore does not establish which authorization the recorded transfer implemented. Four events must be kept apart in any reading: the authorization, the actual transfer, the project expenditure, and an outstanding loan; only the first two are in the record, and no loan is recorded. Nothing in this addendum changes an approved ledger entry.

---

## 2. Operating results: where the two records agree and differ

| Measure | Eric | BeTH (audited) | Verdict |
|---|---:|---:|---|
| FY2023 revenue | $8,200,000 | **$6,898,201** | **Conflict — concept mismatch.** Eric's total includes a $630,826 draw from reserves and $1,150,000 of ARPA aid. A reserve draw is not revenue. |
| FY2023 spending | $7,380,000 | **$7,319,483** | Consistent (~$60K apart; treatment of depreciation or internal charges not yet isolated). |
| FY2025 revenue | — | **$7,594,812** | Eric has no FY2025 data. Berth rents $5,329,258 + leases $2,265,554. |
| FY2025 expense | — | **$13,573,896** | Eric has no FY2025 data. Nearly double FY2024, driven by state-grant-funded dock and pile work. |
| FY2026 revenue | $8,670,000 "Actual" | $8,673,012 **projected** | **Conflict of label, not number.** |
| FY2026 spending | $8,395,000 "Actual" | $8,395,420 **projected** | **Conflict of label, not number.** |

**The FY2026 labeling problem matters.** The figures agree to the dollar because both come from the same source — the Parks, Recreation & Waterfront Commission packet of September 9, 2026. But Eric presents them as *actuals* and BeTH records them as *projections*. **No FY2026 ACFR exists**; FY2025 is the latest audited year. Commission-packet estimates for a year that has not been audited are projections. BeTH's labeling is correct and should not be changed to match.

**BeTH holds forward projections Eric does not**, from the same PRW source:

| | FY2026 proj. | FY2027 proj. | FY2028 proj. |
|---|---:|---:|---:|
| Revenue | $8,673,012 | $6,364,360 | $6,534,799 |
| Expenditure | $8,395,420 | $7,388,315 | $7,580,393 |
| Ending balance | $1,523,963 | $500,008 | **−$545,586** |

On the City's own projections the Marina Fund balance goes **negative in FY2028**. That is the sharpest single fact in the combined record and it comes from BeTH, not from Eric.

---

## 3. The structural question: boating pays for boating

Eric's central analytical finding, from the State's FY2023 tabulation: **boating revenue covers boating cost** ($3.28M against $3.28M). The problem is **$4.09M of non-boating expense with no dedicated revenue stream** — landscape services (100% non-boating), recreation (100% non-boating), and non-boating shares of operations, security, maintenance and overhead.

**Critical caveat BeTH must carry with this finding every time it is shown:** the split exists *only* in the DBW report. The ACFR does not report one; BeTH's audited ledger has no boating/non-boating dimension at all. The State itself described the allocation as *"an informal report prepared at DBW's request"* based on *"estimated workloads."* It is a cost-allocation estimate, not an audited classification. Eric is appropriately clear about this; BeTH must be equally clear.

Eric's related finding on method — *"No document reviewed states how any of these shares was set"* — is corroborated indirectly by BeTH, which independently records FY2025 and FY2026 indirect-cost reductions and Workers' Compensation "holidays" as discrete ledger flows. Charges were being set below the City's own cost-allocation plan, as Eric reports.

**What BeTH must not publish as fact:** Eric's inferred **~$1.3M of unallocated overhead** inside the fund (his $4.4M charged vs $3.1M of actual Waterfront division salaries and benefits, FY2025–2026). That is an analytical conclusion, not a line item in any statement, and it does not reconcile cleanly against BeTH's audited FY2025 "Staff and benefits" of $4,179,607 — different measures over different periods.

---

## 4. General Fund support: a reconciliation that mostly works

| FY | Eric | BeTH | Mechanism | Verdict |
|---|---:|---:|---|---|
| 2008–2021 | $0 | — | No transfers | Unverified |
| 2022 | $1,400,000 | $1,400,000 | Federal ARPA | ✅ Exact |
| 2023 | $1,150,000 | $1,150,000 | Federal ARPA | ✅ Exact |
| 2024 | $800,000 | $800,000 | Cost shifts (capital staff, gardeners) | ✅ Exact |
| 2025 | $704,000 | $850,000 | Indirect-cost & workers' comp holidays; Parks Tax shift | ⚠️ **$146,000 apart** |
| 2026 | $1,400,000 | see below | Direct General Fund transfer | ⚠️ **Four figures** |

**The FY2026 problem.** There are four different numbers for General Fund support to the Marina in FY2026:

- Eric: **$1,400,000**
- BeTH 608 inflows: $1,300,000 + $226,000 = **$1,526,000**
- BeTH 011 flow to 608: **$1,300,000**
- BeTH 011 FY2026 transfer list, "Marina" line: **$1,409,886**

All four are budget-stage figures for an unaudited year, which is how a single appropriation ends up with four values as it moves through adoption, amendment and reporting. It must be reconciled to one adopted number with one citation before publication.

**Parks Tax — exact agreement.** Both records carry the Measure Y permanent shift of **$1,579,000 annually** out of the Marina Fund for waterfront park and landscape maintenance, effective FY2026. Eric's historical series shows the reverse drift that created the need: $121,895 in FY1998 → $519,707 by FY2007 → $757,125 in FY2023. His open question stands and BeTH cannot answer it either: *"The records this project reviewed do not show when, or by what decision, the cost moved"* between 2003 and 2007.

Context BeTH adds: the Park Tax fund itself carries **$281,500,000** of unfunded parks and camps capital need in the proposed FY2027–31 CIP. The fund absorbing the Marina's landscape costs has a larger unfunded backlog than the Marina does.

---

## 5. What BeTH has that Eric does not

1. **The $2,477,099 General Fund interfund receivable** — absent from Eric's analysis entirely. BeTH carries it, and Phase 1 reclassified the General Fund side from `transfer_out` to `loan_out` after confirming ACFR Note 4.A (p.79) describes these balances as *reclassified temporary negative cash balances pending grant reimbursements or other receivables, expected to be repaid within the next fiscal year.*
2. **FY2025 audited operating results** — $7,594,812 revenue against $13,573,896 expense.
3. **FY2027 and FY2028 projections**, including the FY2028 negative balance.
4. **A precise unfunded-capital figure with partial breakdown** — $163,344,000 (inner harbor/docks $33.4M; parking lots $17.3M; streets $15.0M), against Eric's "$163,000,000+" with no breakdown.
5. **The full FY2025 audited expense composition** — staff and benefits $4,179,607; contracts and professional services $3,644,335; repairs and maintenance $2,826,103; utilities/supplies/transport/other $1,623,467; City central charges (indirect) $706,259; depreciation (non-cash) $594,125; State loan interest and principal $485,719.
6. **The State DBW debt position** — $5,415,120 outstanding at 2025-06-30, 4.5%, $485,719/year through FY2041, from the original $7,100,000 Harbor Construction 5 loan of FY2001.
7. **The DoubleTree write-off as a ledger flow** — $890,000, hotel stopped paying regular rent in early 2025. Eric reports the same ~$890,000 owed as of September 2026.

## 6. What Eric has that BeTH does not

1. **The boating/non-boating split** — the single most analytically useful frame, unavailable in audited data.
2. **The causal chain** from the State regulator's finding to the Workers' Compensation loan. BeTH has the transactions but not the "why."
3. **The pre-2015 history** — Parks Tax cost drift from FY1998, the 2003 Master Plan, the 2018 $2,300,000 documented gap described as *"more than one third of current total Marina Fund revenues."*
4. **Pier-ferry capital and operating economics** (see `data/eric-waterfront-catalog.json`): capital estimates ranging $103.6M–$200M+, only $5,138,685 of funding identified, construction funding *"has not been identified"* as of October 2025, a 2035 best-case operating gap of **$5,589,288/year** with public subsidy per boarding ($7.62) exceeding the fare ($7.28), and ~$20.7M of contracts approved across six consent-calendar items.
5. **The Measure U observation** — the $300M bond's waterfront project list contains no ferry or terminal project.
6. **Vision 2050 status** — the Task Force reported in December 2025 that the asset-management program remains incomplete, and **the waterfront is not on the implementation schedule** despite being named a PRW asset in the 2022 policy.

---

## 7. Three unfunded-need totals that do not agree

| Figure | As of | Source |
|---:|---|---|
| $131,000,000 | 2025-05-22 | BeTH |
| $153,480,000 | 2025-09 | Eric (pier-ferry page) |
| $163,344,000 | 2026-09-09 | BeTH (with partial breakdown) |

A 16-month window produced three totals spanning $32M. The scope definitions almost certainly differ — whether the pier is included, whether sea-level-rise work is included, whether parking lots and streets are counted as waterfront. **Do not average, reconcile, or pick one.** Publish them as three separately sourced estimates with their scope definitions, once those are established.

---

## 9. The DoubleTree $890,000: outstanding rent, not a write-off

> **2026-10-23: flagged to Codex with page-verified sources** in `flags/2026-10-23-doubletree-608-ledger-event.md` (proposal JSON alongside). Re-reading the City's decks shows **two episodes**, not one. Arrears of $680,299 through June 2025 (May 22, 2025 deck p.7) were cleared by the **full-balance** payment of $964,680 in September 2025 (Sept 9, 2026 packet p.11). The ~$890,000 is a second episode, January–September 2026, as of September 2026 (FY2027). The same packet states the FY2027–28 budget assumption as 30% (p.11) and as at least 35% (p.15). The ledger entry is unchanged pending authorization.

Both records carry roughly $890,000 against the DoubleTree hotel. Neither should call it a write-off,
and BeTH's ledger currently does.

**What the lease and the arrears are.** A 60-year ground lease running to 2080, base rent about
$82,000 a month plus percentage rent. The hotel stopped paying regular rent in early 2025 — January
per the May 2025 deck, March per the September 2026 deck, a discrepancy BeTH carries without
resolving. It paid $964,680 in September 2025 and nothing since December 2025. About **$890,000 was
owed as of September 2026**: nine months of base rent plus three quarters of percentage rent.

**The three things it could be, and which it is:**

| Treatment | Meaning | Applies here? |
|---|---|---|
| **Outstanding rent (receivable)** | Billed, unpaid, still owed and still collectible | **Yes.** This is what the $890,000 is. |
| **Allowance for doubtful accounts** | A contra-asset reducing the receivable's carrying value for the part not expected to be collected | **Policy exists; no Marina-specific amount located.** The FY2025 ACFR states *"All trade accounts receivable are presented net of allowance for doubtful accounts."* Whether any allowance was booked against this tenant, and how much, is **not established**. |
| **Write-off** | The receivable is removed; the City has stopped expecting payment | **No.** Nothing in either record says the City wrote this off. |

**BeTH's ledger contradicts itself.** The entry `608-doubletree-arrears` has `kind: "write_off"`,
while its own `terms` field reads: *"Not written off; recorded here as revenue at risk. Budget assumed
35% of rent for FY27-28; actual zero. Staff: potential loss $840K through FY28."* The field is right
and the kind is wrong — the same pattern as §0B.

**Three different numbers, three different meanings**, which must never be used interchangeably:

- **$890,000** — amount owed as of September 2026. A receivable.
- **$964,680** — amount actually paid in September 2025. Cash received.
- **$840,000** — staff's estimate of *potential loss through FY28*. A forecast, not a booked amount.

**Also note the fiscal-year label.** BeTH dates this entry `fy: 2026`, but the $890,000 balance is
stated as of September 2026, which falls in **FY2027**. The arrears began in FY2025 and accumulated
across three fiscal years. A single-year tag cannot represent it correctly.

**Unresolved:** whether any allowance for doubtful accounts was recorded against this tenant in
FY2025 or FY2026; the correct start date of non-payment; and whether the City has initiated lease
enforcement. **Flagged, not changed.**

## 8. Publication rules for this case study

1. Label every figure: `audited` | `budget` | `projection` | `planning estimate` | `third-party analysis`.
2. Never present the DBW boating/non-boating split without its "informal, estimated workloads" caveat.
3. Never present FY2026 Marina figures as actuals.
4. Hold the $5.5M Workers' Compensation item entirely until its destination is resolved.
5. Attribute Eric's findings to the Berkeley Decision Project by name, with his source citation, every time.
6. Keep loans, transfers, cost shifts, and indirect-cost reductions in distinct categories. Four mechanisms moved money toward the Marina between FY2022 and FY2026 and collapsing them into "General Fund support" destroys the distinction that matters.
7. Never cite an authorization as evidence that a transaction occurred (§0A).
8. Never describe the DoubleTree $890,000 as a write-off (§9).
9. Separate non-cash entries from cash expenditure whenever a total is shown. FY2025's $13,573,896 includes $594,125 of depreciation and is inflated by grant-funded capital work (§0E).

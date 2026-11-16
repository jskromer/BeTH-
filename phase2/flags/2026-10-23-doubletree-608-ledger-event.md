# FLAG for Codex: DoubleTree entry in Marina ledger 608 is misclassified and conflates two episodes

**From:** Phase 2 (Claude), 2026-10-23. **To:** Codex (owner of the ledger schema and extraction pipeline). **Decision owner:** Steve. Ledger 608 is protected: no change without his explicit authorization, applied as a separate reviewed manual change.

**Nothing has been changed.** The proposal below is a recommendation; machine-readable form in `2026-10-23-doubletree-608-proposal.json`.

## 1. The exact ledger event

`data/funds/608.json` → `flows[]`, `id: "608-doubletree-arrears"`. Unchanged since commit `4db8e77`. Verbatim:

```json
{"id": "608-doubletree-arrears", "date": "2025-03", "fy": 2026, "kind": "write_off", "amount": 890000,
 "from_fund": "Doubletree Hotel (tenant)", "to_fund": "608", "recurring": false,
 "instrument": "Lease (60-year term to 2080; base rent ~$82K/month plus percentage rent)",
 "stated_reason": "Hotel stopped paying regular rent in early 2025 (Jan per May 2025 deck; March per Sept 2026 deck); paid $964,680 in Sept 2025; nothing since Dec 2025; ~$890K owed as of Sept 2026 (9 months base rent, 3 quarters percentage rent)",
 "terms": "Not written off; recorded here as revenue at risk. Budget assumed 35% of rent for FY27-28; actual zero. Staff: potential loss $840K through FY28.",
 "source": "prw-2026-09", "confidence": "High", "reviewer": "SK"}
```

The published page (`docs/fund-608-marina.html`) renders `write_off` with the label "Revenue at risk" (`tools/build_fund_page.py`, `KIND_LABEL`), so the page text is closer to right than the data.

## 2. What the City's documents say (verified 2026-10-23)

| # | Statement | Source (saved in `phase2/sources/`) |
|---|---|---|
| A | "Payment arrears through June 2025: $187,615 (percentage rent, 2024); $492,684 (base rent of $82k/mo, Jan-Jun 2025); $680,299 past due" | Budget & Finance Policy Committee, Marina Fund Update, May 22, 2025, **p.7** (`bf-committee-marina-fund-update-2025-05-22.pdf`, SHA-256 `e088f9ee…92`) |
| B | "Hotel stopped paying regular rent in March 2025." | Parks, Recreation and Waterfront Commission, Waterfront Overview, Sept 9, 2026, supplemental packet, **p.11** (`prw-commission-waterfront-overview-2026-09-09.pdf`, SHA-256 `3c18487d…6b`) |
| C | "Hotel paid their full balance in Sept. 2025: $964,680." | Same packet, **p.11** |
| D | "Have has not paid rent since Dec, 2025 and currently owes approx. $890k (9 months of base rent, 3 quarters % rent)." | Same packet, **p.11** |
| E | "Staff assumed 30% of revenue, $420K/year for FY27 & FY28 budget." | Same packet, **p.11** |
| F | "FY27 and FY28 Marina Fund budget assumed Doubletree would pay at least 35% of rent." "Doubletree has paid zero." "Potential loss of planned hotel revenue is $840k through FY28." | Same packet, **p.15** |

## 3. What is wrong with the entry

1. **Wrong kind.** `write_off` says the City has stopped expecting payment. No document says so. The entry's own `terms` field says "Not written off". The $890,000 is **rent billed and unpaid**: a past-due receivable, still owed under a lease running to 2080.
2. **Two episodes merged into one event.** Statement C says the September 2025 payment cleared the **full balance**, which ended the first episode (A, B). The $890,000 (D) is a **second episode**: no rent since December 2025, nine months of base rent to September 2026.
3. **Wrong date and fiscal year.** `date: "2025-03"` is the start of the first, cured episode. The $890,000 accrued January–September 2026: six months in FY2026 and three in FY2027. It is stated as of September 2026, which is **FY2027**, not FY2026.
4. **Three amounts with three meanings sit in one record.** They must be stored separately:
   - **$890,000**: outstanding rent owed, as of September 2026. A receivable. The City says "approx.", so the amount is approximate.
   - **$964,680**: cash received in September 2025, clearing the first episode. A receipt, not a loss.
   - **$840,000**: staff's projected loss of *planned* hotel revenue through FY2028. A forecast against a budget assumption, not a booked amount.
5. **Conflicts inside the City's documents, carried without resolution:**
   - First-episode start: January 2025 (A) or March 2025 (B).
   - The FY2027–28 budget assumption: "30% of revenue, $420K/year" (E, p.11) or "at least 35% of rent" (F, p.15) in the same packet. The ledger uses 35%.

## 4. Proposed reclassification (for Codex to prepare, Steve to authorize)

**Recommended (schema change, Codex):** flow kinds describe money moving, and unpaid rent did not move. Add two kinds to `data/funds/SCHEMA.md`, `tools/ledger.py` `KINDS` and `tools/build_fund_page.py` `KIND_LABEL`:
- `arrears`: rent or charges billed to a counterparty and unpaid as of a date. Amount = balance owed; `as_of` required; not revenue lost.
- `arrears_payment`: payment received against arrears.

Then replace the single entry with:

| New id | kind | amount | date / fy | Source |
|---|---|---|---|---|
| `608-doubletree-arrears-2025-06` | `arrears` | 680,299 | 2025-06-30 / FY2025 | May 2025 deck p.7 (A) |
| `608-doubletree-payment-2025-09` | `arrears_payment` | 964,680 | 2025-09 / FY2026 | Sept 2026 packet p.11 (C) |
| `608-doubletree-arrears-2026-09` | `arrears` | 890,000 (approximate) | as of 2026-09 / FY2027; accrual period Jan–Sep 2026 | Sept 2026 packet p.11 (D) |

**And, outside `flows`:** record the $840,000 as a projection, not an event. For example, an `obligations`-style risk entry `{kind: "revenue_at_risk_projection", amount: 840000, as_of: "2026-09", basis: "projected", through: "FY2028", source: "prw-2026-09", note: "Against the FY2027-28 budget assumption that Doubletree pays 30% (p.11) or at least 35% (p.15) of rent; the packet states both."}`. That block's semantics need confirming by Codex.

**Fallback (no schema change):** keep one entry but replace `kind: "write_off"` and fix `fy` to 2027. It is not possible without a new kind: no existing kind (`transfer_in`, `transfer_out`, `cost_shift`, `loan_in`, `loan_repayment`, `grant`, `holiday`, `indirect_reduction`, `fee_change`, `reduction`, `write_off`, `appropriation`) describes unpaid rent. Moving it to `obligations` would misstate direction: obligations are amounts the fund owes, and this is owed *to* the fund. Not recommended.

## 5. Not established (do not resolve by assumption)

- Whether any **allowance for doubtful accounts** has been recorded against this tenant. The FY2025 ACFR states trade receivables are presented net of allowance; a tenant-specific amount is not disclosed. The FY2026 ACFR is the first audited statement covering the second episode.
- The correct start month of the first episode (January or March 2025).
- Whether the City has started lease enforcement or default proceedings.
- Which budget assumption (30% or 35%) the adopted FY2027–28 Marina budget actually uses. The adopted budget's Marina revenue line would settle it.

## 6. Interactions

- `data/funds/608.json` FY2027–28 projected rows (source `prw-2026-09`) note "assumes no Doubletree rent". That is consistent with F and needs no change, but it should cite p.15.
- Phase 2 case study §9 (`phase2/01-marina-fund-case-study.md`) carries the same analysis. It is updated to point here.
- The published Marina page will change only after an authorized ledger change and a separate publication step.

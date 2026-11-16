# BeTH Phase 2 master research plan — Capital Choices, Asset Management, and Financial Sustainability

**Updated 2026-10-23. Supersedes `BeTH_Phase_2_Capital_Choices_Vision_2050_Plan.md` (2026-10-22), which is retained verbatim as the base plan.**

**Status:** Research plan. Not a verified inventory of reallocatable funds, and not a recommendation to terminate any project.

## What changed from the 2026-10-22 base plan

The base plan's structure, safeguards and source register stand. This update adds what the first research pass established:

1. **A third research source is integrated** — Eric Fredericks' Berkeley Decision Project, reconciled fund-by-fund against BeTH's audited ledger (deliverable 2).
2. **A blocking finding emerged** — the $5.5M Workers' Compensation transaction (Q1). It is now the top-priority item in the whole phase.
3. **The Workers' Compensation Fund is itself a sustainability subject**, not just a funding mechanism: **−$9,752,938** net position at FY2025.
4. **Scope confirmed** — the adopted FY2027–31 CIP has **149 projects** and over **$2.1B** of identified need.
5. **The PCI workstream is explicitly gated.** No pavement model output is publishable until calibration data exists.

## The phase in one question

**How much money could Berkeley lawfully move to street rehabilitation, what would it give up, and what would the streets actually get?**

Three sub-questions, each of which can be answered wrongly in a way that sounds authoritative:

| Sub-question | The error to avoid |
|---|---|
| How much money is available? | Treating budget authority, identified need, or restricted funds as available cash |
| What is given up? | Reporting released dollars without the services, safety and deferred costs they buy |
| What do streets get? | Projecting a PCI outcome from invented deterioration rates and unit costs |

## Evidence hierarchy

Phase 2 draws on sources of very different reliability. The hierarchy is fixed and applies everywhere:

1. **Audited** — ACFR, tied to a statement column. Phase 1's 106-fund ledger. Highest authority.
2. **Budget** — adopted appropriations and amendments. Authoritative for intent, not for outcome.
3. **Projection** — City forecasts for unaudited years.
4. **Planning estimate** — engineering and consultant studies.
5. **Third-party analysis** — independent research. **A lead to verify, never a substitute for the above.**

Eric's work sits at level 5 and is treated accordingly, notwithstanding its high internal standard. His public repository is generated output from a private source repository, so his extraction cannot be re-executed — only his cited documents re-read. Where his findings are corroborated from primary sources, they are promoted and the verification is recorded.

## Status update, 2026-10-23 (end of day)

- **Street funding (B/D):** `07-street-funding-legal-analysis.md`. Measure FF: allocation fixed by voters; whether more could go to paving without a vote is unresolved. CIP Fund 501: gross conditional deferral ceiling $2,946,000 of FY2027–28 appropriations ($2,916,000 excluding the contractual JPA contribution), only by deferring every other fund 501 project; not verified available cash; one-time carryover unknown (ceiling $11,568,647 at June 30, 2025).
- **Adopted CIP:** `data/cip-projects.json` (schema 3), reconciled to the dollar. The $139,356,147 figure is the five-year Streets budget (two-year: $58,211,462).
- **Pavement (D):** two measures side by side. 2024 average 56, with 88.5 centerline miles (41.6%) below PCI 50. The adopted plans treat 22.6 such miles over FY2027–31.
- **Flags:** DoubleTree entry in ledger 608 flagged to Codex (`flags/`). Not changed.

## Workstreams

### A. Marina / waterfront reconciliation — **substantially complete, two blockers**
Deliverable 2. Every overlap between Eric's record and BeTH's ledger catalogued, with four exact agreements, five conflicts and one independently verified finding. Blocked on Q1 (the $5.5M destination) and Q3 (the FY2026 figure).

### B. Capital portfolio — **loaded and reconciled (adopted CIP, 143 projects); restriction research 6 of 15 sources**
Deliverable 3. Schema complete. The long pole is **restriction research across all 149 projects**: until `restriction_class` is established per project, no statement about redirectable money is supportable.

### C. Vision 2050 asset management — **specified, blocked on verification**
Deliverable 4. Mapping complete. Blocked on Q9 (are NexGen/AssetWorks/AMCS still in use, and what do they cover) and Q8 (is the waterfront outside the implementation schedule).

### D. PCI model — **City scenarios plus measured condition distribution; independent projection still gated**
Plan item 7. Four-link chain specified; calibration requirements enumerated. **No model output until segment PCI, deterioration curves, treatment costs and service lives exist.** The honest Phase 2 output here is the framework plus the gap list.

### E. Payroll, benefits and recurring costs — **not started**
Base plan workstream 3. The Workers' Compensation finding gives it an obvious first subject: contribution holidays as a budget-balancing mechanism, and the liability they defer.

### F. Paving delivery cost and legislative analysis — **not started**
Base plan workstream 4. Requires contract-level cost decomposition. **Do not presume environmental review is the primary cost driver** — that is the hypothesis to test, and the politically convenient answer the data may not support.

### G. Public interface — **prototype with four Ask answers that pass automated structural checks; not independently source-verified; not published**
Deliverable 6. Build order deliberately ships the scenario and PCI views **last**.

## Safeguards (carried forward from the base plan, unchanged)

- FY2025 audited reconciliations are **history**, not FY2027 unspent balances.
- Budget authority is not cash; encumbrances are not expenditures; restricted funds are not General Fund resources.
- No double counting of transfers or multi-funded projects.
- Preserve project histories and cancellation reasons.
- Show deferred replacement and maintenance costs alongside near-term savings.
- Confirm voter restrictions and bond covenants before asserting transferability.
- Verify asset system names and integration status before publishing claims.

**Added in this update:**
- **Loans, transfers, cost shifts and indirect-cost reductions are four different things.** Phase 1 corrected one such error ($2,477,099); Q1 may be a second at more than twice the size.
- **A stated purpose is not a destination.** Recording what Council said money was *for* as where it *went* is the probable root of Q1.
- **Never change approved financial data on the strength of third-party analysis.** Flag, source, resolve, then correct through review.

## Sequence

1. **Resolve Q1 and Q2** — obtain the FY2024 ACFR and Workers' Compensation statements. Blocks the Marina case study and the operating-costs view.
2. **Extract the FY2027–31 CIP** — 149 projects into `capital_projects`.
3. **Restriction research** — the long pole; begin immediately and in parallel.
4. **Encumbrance report** — establish real uncommitted balances.
5. **Verify Vision 2050 system status** (Q9) and the waterfront-exclusion finding (Q8).
6. **Obtain StreetSaver data** — gates the entire PCI workstream.
7. **Payroll and benefit baseline.**
8. **Build views 1, 4, 2, 6** in that order.
9. **Scenarios and PCI simulator last**, only once 3 and 6 are complete.

## Deliverables in this directory

| File | Deliverable |
|---|---|
| `00-master-research-plan.md` | 1 — this document |
| `01-marina-fund-case-study.md` | 2 — Marina reconciliation with Eric's findings |
| `02-capital-project-database-spec.md` | 3 — capital project database specification |
| `03-vision2050-integration-plan.md` | 4 — Vision 2050 integration |
| `04-open-questions-and-missing-sources.md` | 5 — unresolved questions and missing documents |
| `05-budget-choices-dashboard-structure.md` | 6 — dashboard structure |
| `06-pci60-financial-model.md` | plan item 7 — PCI model framework |
| `data/eric-waterfront-catalog.json` | Structured catalog of Eric's figures with attribution and status |

## Working principle

Show what is known, what is legally movable, what can be changed, and what outcomes the choices might buy. **Do not present a scenario as a completed policy decision.**

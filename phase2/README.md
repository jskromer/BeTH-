# BeTH Phase 2 — Capital Choices, Asset Management, Financial Sustainability

Working directory for Phase 2 research. **Nothing here is published.** No Phase 1 production file is modified by any document in this directory.

**Branch:** `phase2-capital-analysis` · **Base:** `7b413d4` (Phase 1 final) · **Started:** 2026-10-23

## Read in this order

1. **`00-master-research-plan.md`** — what the phase is, what changed, what happens next
2. **`01-marina-fund-case-study.md`** — the reconciliation that produced the phase's first real finding
3. **`04-open-questions-and-missing-sources.md`** — what blocks publication
4. **`07-street-funding-legal-analysis.md`** — which capital money could lawfully go to paving (CIP Fund 501, Measure FF), with the verified answer
5. **`flags/`** — items flagged to Codex for protected-ledger review (DoubleTree, ledger 608)
6. `docs/budget-choices.html` (serve `phase2/docs` over HTTP) and `docs/ask/` — prototype interface; verified Ask answers
7. `02-capital-project-database-spec.md` · `03-vision2050-integration-plan.md` · `06-pci60-financial-model.md` · `05-budget-choices-dashboard-structure.md`

## The headline finding

A **$5,500,000** internal loan from the Workers' Compensation Fund, authorized July 25, 2023 for Marina dock replacement, **is not recorded as owed in the audited statements**. The string `5,500,000` appears nowhere in the FY2025 ACFR, and Note 4.A (p.79) lists only the $2,477,099 Marina receivable.

Eric Fredericks' Berkeley Decision Project found this; BeTH verified it independently from the ACFR. It also means **BeTH's own ledger entry for this transaction is in question** — BeTH records it as going to the Marina, Eric as going to the General Fund, and the Marina's audited FY2024 transfers in are $0.

**No financial data has been changed.** See Q1.

## Standing rules

- Phase 1 data is approved and frozen. Flag discrepancies; never edit on the strength of third-party analysis.
- Every figure carries a source and an evidence class: audited / budget / projection / planning estimate / third-party.
- Loans, transfers, cost shifts and indirect-cost reductions are four different things.
- Budget authority is not cash. Identified need is not money.
- Third-party research is attributed by name with the researcher's own citation.

## Attribution

Eric Fredericks, **Berkeley Decision Project** — https://ericdf.github.io/berkeley-decision-project/ · https://github.com/ericdf/berkeley-decision-project

Treated as an important research source, not as independently verified accounting evidence. His figures and citations are catalogued in `data/eric-waterfront-catalog.json` with a per-item verification status.

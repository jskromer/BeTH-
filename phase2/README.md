# BeTH Phase 2 — Capital Choices, Asset Management, Financial Sustainability

Working directory for Phase 2 research. **Nothing here is published.** No Phase 1 production file is modified by any document in this directory.

**Branch:** `phase2-capital-analysis` · **Base:** `7b413d4` (Phase 1 final) · **Started:** 2026-10-23

## Read in this order

1. **`00-master-research-plan.md`** — what the phase is, what changed, what happens next
2. **`01-marina-fund-case-study.md`** — the reconciliation that produced the phase's first real finding
3. **`04-open-questions-and-missing-sources.md`** — what blocks publication
4. **`07-street-funding-legal-analysis.md`** — which capital money could lawfully go to paving (CIP Fund 501, Measure FF), with the open legal questions
5. **`flags/`** — items flagged to Codex for protected-ledger review (DoubleTree, ledger 608)
6. `docs/budget-choices.html` and `docs/ask/` — prototype interface; Ask answers that pass automated structural checks (not independently source-verified). See **Local preview** below.
7. `02-capital-project-database-spec.md` · `03-vision2050-integration-plan.md` · `06-pci60-financial-model.md` · `05-budget-choices-dashboard-structure.md`

## Local preview

Serve the **repository root**, not `phase2/docs`. The evidence links point up the tree to `phase2/sources/*.pdf` and to the
ACFR PDF at the repository root; a server rooted at `phase2/docs` cannot reach them and every source link returns 404.

```
cd <repository root>            # the directory that holds annual-comprehensive-financial-report-fy2025.pdf
python3 -m http.server 8000
```

Then open `http://localhost:8000/phase2/docs/budget-choices.html` (seven tabs) and
`http://localhost:8000/phase2/docs/ask/index.html` (four Ask pages). Opening the HTML file directly (`file://`) does
not work: the page fetches `data/phase2.json` and `data/answers.json`.

## Rebuild and test

```
sh phase2/tools/rebuild.sh                              # every generated output, in dependency order
python3 -m unittest discover -s phase2/tests -v         # needs pdftotext and pdfinfo (poppler)
```

CI (`.github/workflows/phase2.yml`, separate from Phase 1 CI) runs the tests on Python 3.12 with poppler-utils,
rebuilds every output and fails if any committed file changes, and fails if the branch touches `data/funds`,
`data/curation` or `docs/`.

The Ask verifier runs automated structural checks only: citations exist, figures match records or cited pages,
quotes are on the cited page, arithmetic recomputes, and the displayed arithmetic is generated from that
recomputation. It is not human source verification, and it does not establish that a legal interpretation is
right, that a calculation method is appropriate, or that answers agree with one another.

## Human review

`review/human-review-checklist.md` (generated) lists, for each Ask page, the central claim, the calculations, every
cited document and page, and the open legal and accounting questions. Decisions are recorded by hand in
`review/human-approvals.json`. **No answer is approved.**

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

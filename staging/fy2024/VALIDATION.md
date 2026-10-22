# Pilot validation — 2026-10-22

- Branch: `codex/fy2024-reconciliation`, based on merged `origin/main` at `350f1cd`.
- Official FY2024 source: 373 PDF pages; SHA-256 and acquisition provenance are in
  `manifest.json`. Financial statement pages: 78, 87–88, 227–244, 311–312.
- `python -m unittest discover -s tests -v`: **29 tests passed** (28.473 seconds
  locally, Python 3.13, pdfplumber 0.11.9). CI uses Python 3.12.
- `python tools/ledger.py data/funds/*.json`: **106 OK**, no errors or warnings.
- Default FY2025 extraction: **106 funds, zero files updated**. The full-output
  regression also matches all 106 pre-pilot records, including `flow_detail`.
- FY2024 report: **105 funds**, all six curated funds compared, **zero differing
  comparable reviewed financial fields**. Final fund status: **103 PENDING REVIEW,
  2 INCOMPLETE**. These statuses do not approve publication.
- All 105 FY2024 closing values equal the FY2025 statements' original openings;
  **15 nonzero explicitly reported opening restatements** are retained separately.
- Four FY2024 governmental control groups have exact-dollar discrepancies, all
  $1. They remain CONFLICT. For example, the individual capital-outlay columns on
  PDF p.78 sum to $35,417,246 while the printed total is $35,417,247.
- Genuine source blanks were checked visually on PDF pp.230 and 232: Condo
  Conversion Program / General government and Measure B Paratransit / Private
  contributions and donations. Neither blank was converted into zero.
- The enterprise total opening/closing balances are blank on PDF p.88. Those
  horizontal checks remain INCOMPLETE. Other control gaps and FY2025 comparator
  discrepancies are retained in the reports rather than silently corrected.
- One existing FY2025 ledger has no matching FY2024 column: Fire Admin Training
  Building Bond. Its identity/existence history remains INCOMPLETE.
- Tests verify deterministic reruns of all staged report artifacts. CI regenerates
  the committed pilot outputs and checks for a clean diff.
- SHA-256 comparison with the pre-pilot snapshot confirms **all 106 ledger JSON
  files and all 304 website files unchanged**. The six protected ledgers and
  Marina's FY2015–FY2023 series are included. `git diff --exit-code -- data/funds
  docs` and `git diff --check` passed.

No website builders ran. No historical years before FY2024 were extracted.
Independent review by Claude Code and Steve's listed decisions remain pending.

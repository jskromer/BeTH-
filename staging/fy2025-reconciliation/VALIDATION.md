# Post-correction maintenance validation

Based on merged main `acfdcfc` after PR #11 and PR #13. The original proposal
commit is `2450d7aad152883a8428255801a49edbd3d85f3d`.

- Complete suite: **52 tests passed**, 35.561 seconds locally (Python 3.13,
  pdfplumber 0.11.9). CI uses Python 3.12 and the same pinned parser.
- Historical omissions: frozen General Fund, Grants and Capital Improvement
  ledgers still expose **$36,598,654** of expenditure detail and **$18,176,377**
  of financing detail. Tests reproduce each original reviewed patch byte for
  byte. All seven original correction artifacts and all three original ledger
  fixtures have pinned SHA-256 values; the fixture manifest itself is pinned too.
- Current status: **all five major governmental funds RECONCILED**; expenditure
  omissions **$0**; financing omissions **$0**; affected funds **0**; proposed
  patches **0**. No patch directory or patch checksum file is generated here.
- All **106 ledgers** pass validation. All annual records in the corrected three
  remain identical to their pre-correction fixtures, including revenues,
  expenditures, transfers and ending balances. The six approved flow-detail
  additions are the only differences from those fixtures. Existing full-output
  and annual-value regressions continue to pass.
- Extraction and report regeneration are idempotent. Real extraction runs twice
  against corrected ledgers with zero updates; both current staging generators
  reproduce identical bytes on repeat runs.
- Every ledger, the protected registry, historical correction package and
  published website file remains byte-identical to the maintenance baseline.
  No dashboard or page builder is run, no deployment is requested, and PR #12
  remains outside this work.
- The FY2024 dependency manifest now records **139 required inputs**, including
  the immutable historical package and frozen pre-correction inputs consumed by
  verification. FY2024 financial staging, provenance and audit checksums remain
  unchanged. Its existing review items remain unresolved; see the pilot report.

Reproduce with the commands in `tools/POST_CORRECTION_MAINTENANCE.md`.
The original archived reports describe the pre-correction proposal and are
preserved without editing their historical claims.

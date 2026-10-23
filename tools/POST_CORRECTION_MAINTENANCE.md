# FY2025 correction history and current reconciliation

PR #11 proposed six independently reviewed FY2025 line-item additions at commit
`2450d7a`; PR #13 applied them to General Fund 011, Grants and Capital Improvement
501. Only money-flow detail changed. Annual records, revenue, expenditures,
transfers, balances and source references were preserved.

## Immutable historical evidence

`staging/fy2025-expenditure-corrections/` remains byte for byte as reviewed. Its
three JSON patches, SHA256SUMS, human reconciliation, validation and machine
proposals describe the original omissions. Statements such as “not applied” in
those archived reports describe that historical proposal, before PR #13. They
are not current instructions or outstanding corrections. Do not reapply them.

`tests/fixtures/fy2025-pre-correction/` contains exact original ledger bytes from
`2450d7aad152883a8428255801a49edbd3d85f3d`. Its manifest pins those ledgers and
all seven original artifacts. The test suite pins the manifest checksum too.
The historical tests still detect expenditure omissions of $20,312,681 (011),
$13,584,981 (Grants) and $2,700,992 (501), totaling $36,598,654. Financing omissions
remain $18,156,996 (011) and $19,381 (Grants), totaling $18,176,377. Generated
historical patches must match the reviewed patch bytes and checksums exactly.

## Current status

Run `python tools/reconcile_expenditure_breakdown.py`. The default output is now
`staging/fy2025-reconciliation/`, separate from the immutable history. All five
major governmental funds reconcile with zero expenditure or financing omissions
and no proposed correction patches. The original archive and frozen inputs are
never regenerated. Output targeting the archive is refused, including nested
paths. If a prior output contains patches that would become stale, the run
refuses instead of overwriting or deleting that evidence; choose a new output.

Net other financing remains −$6,774,558 for General Fund, $24,222 for Grants and
$12,582,617 for Capital Improvement. Each source-category sum, audited net change
and balance roll-forward reconciles. Current tests also validate all 106 ledgers
and compare the corrected three with the frozen originals: the six reviewed
additions are the only differences, with every annual record and other field
unchanged. The existing full-extraction and annual-value regression fixtures
remain frozen and continue to verify the original figures independently.

The FY2024 dependency manifest is refreshed for current ledger and verification
input hashes. Its financial staging values, source provenance and audit checksums
remain unchanged. Original FY2024 review items, including $1 statement-control
differences and genuinely blank cells, remain unresolved and separately reported.

## Verification

```sh
python -m unittest discover -s tests -v
python tools/ledger.py data/funds/*.json
python tools/acfr_funds.py annual-comprehensive-financial-report-fy2025.pdf data/funds
python tools/acfr_pilot.py --out staging/fy2024
python tools/reconcile_expenditure_breakdown.py
git diff --exit-code -- data/funds data/curation docs staging/fy2025-expenditure-corrections
```

CI runs the full suite, ledger validation, safe extraction, both current staging
generators and a committed-output diff. Tests check idempotent regeneration and
every historical artifact checksum. Ledger and website snapshots are compared
around reconciliation; extraction tests run updates twice against copied current
ledgers and require identical bytes and zero writes.

This maintenance changes no financial ledger, protected registry, dashboard or
published file. Dashboard publication remains withheld; PR #12 is outside scope.

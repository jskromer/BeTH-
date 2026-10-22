# Extraction safety (PR #9)

Automated extraction must never destroy or silently alter reviewed evidence.
This change handles FY2025 only. FY2024 ingestion, independent reconciliation,
restatement reporting and historical integration remain gated on later reviews.
No website builder or published financial content is changed.

## Update policy

`acfr_funds.py` parses the entire PDF before `ledger_safety.update_ledgers`
preflights the complete batch. Duplicate annual identities, conflicting financial
values, duplicate fund identities, missing required statement labels or values,
and conflicting source IDs needed by new records raise `SafetyError`. The CLI
exits nonzero with `EXTRACTION SAFETY ERROR` on these failures before any writes.
Zeros must be explicit statement values (including printed dashes), never a
fallback for a missing total, transfer or balance label.

For an existing annual identity, financial values must agree. The existing row,
notes and source references remain authoritative evidence and are left untouched.
Matching values do not authorize replacing narratives or source metadata.
For an unprotected fund, only new annual records and their source entries can be
appended. All other fields, including unknown fields, flows, obligations, assets,
findings, status and flow diagrams, are preserved. An identical rerun performs
no writes. New ledgers use exclusive creation; append updates use a temporary
file and atomic replacement after checking the original bytes again.

This command assumes one writer. Batch validation prevents partial changes caused
by data conflicts; it is not a multi-file transaction against disk failures or
concurrent editors. Do not run simultaneous ledger writers.

## Curation metadata and protected registry

`data/curation/protected-ledgers.json` explicitly identifies these six reviewed
ledgers with `status: curated` and `policy: immutable-to-extraction`:

- General Fund (`011`)
- Marina (`608`)
- Parks Tax (`ACFR-park-tax`)
- Equipment 671/672 (`ACFR-equipment-maintenance-replacement`)
- Workers' Compensation (`ACFR-workers-compensation`)
- Zero Waste (`ACFR-zero-waste`)

The registry is outside `data/funds` because existing consumers treat every JSON
file there as a ledger. It holds curation metadata without changing the reviewed
ledger bytes. The registry must be present and readable even for a separate
output directory. Extraction refuses to create a missing protected file or add
an annual record to a protected file. Copy reviewed files into a destination
before extraction; a blank destination is deliberately not a way to regenerate
curated evidence. Conflicting protected values also abort, rather than being
silently skipped. No force/overwrite option is provided.

New automatically created ledgers carry inline
`curation: {status: extracted, policy: append-only}`. Inline `status: curated`
also prevents additions. Existing files do not receive metadata migrations.
Changing protected evidence requires a separately reviewed manual change.

## Annual identity and compatibility

Annual identity is `(fy, basis, series, balance_version)`. `series` and
`balance_version` are optional explicit identifiers; an omitted value remains
unspecified. `series` can separate statistical schedules from fund statements;
`balance_version` can distinguish original and restated audited balances. The
safety layer never infers those classifications or resolves a disagreement.
A duplicate full identity is an error even when its values agree. The validator
still permits distinct reporting bases in the same year.

The FY2025 extractor retains existing fund IDs, with three explicit identity
mappings replacing the previous order-dependent suffix behavior. Unexpected
collisions fail. These are compatibility mappings for FY2025, not historical
fund-identity reconciliation.

## Verification

Install dependencies in a virtual environment and run from the repository root:

```sh
python -m pip install -r tests/requirements.txt
python -m unittest discover -s tests -v
python tools/ledger.py data/funds/*.json
python tools/acfr_funds.py annual-comprehensive-financial-report-fy2025.pdf data/funds
git diff --exit-code -- data/funds docs
```

The regression fixture was generated using the unmodified extractor and parser
from commit `e51951c`, against the repository's FY2025 PDF (SHA-256 recorded in
the fixture). It preserves all 105 previously generated annual records, excluding
free-text notes. Marina was skipped by the old extractor; the new extraction
also compares its FY2025 financial values against the existing curated ledger.
The fixture demonstrates equivalence, not independent reconciliation against the
audited statements. That remains PR #10 work. Explicitly reading previously
unrecognized beginning-balance labels can improve generated notes, while existing
notes and all financial records remain untouched.

Local results on 2026-10-22: 14 tests passed; all 106 ledgers passed validation.
A real FY2025 extraction into `data/funds` parsed 106 funds and updated zero files.
SHA-256 comparisons before and after confirmed all 106 ledger JSON files and all
304 files under `docs` unchanged. Tests also run extraction updates twice against
a temporary copy and check every existing ledger byte for byte. CI repeats the
suite, validation, extraction and unchanged-content check on pull requests.

Protected-ledger SHA-256 values before and after the real extraction:

| Ledger | SHA-256 |
|---|---|
| `011` | `46128217f6fb7557d46d7148854ab3fd3a38e129f3aae71ab90ffdb8c8ddb162` |
| `608` | `23a8d30daf45032924e5c949a0b4726550fd4af6f8b3149762cf1043af4483d0` |
| `ACFR-equipment-maintenance-replacement` | `f8dd7b295a84a2da14dde618bc0c4cbad51f13f90cfa57bf462fbed62a371878` |
| `ACFR-park-tax` | `d5733f22cd919ec86d6d770dd9dde6642c3cb095768196dd405c47dfd06f0551` |
| `ACFR-workers-compensation` | `0c9cf8108eb392236cf6265240a6bfb4198806263cb5058e28d9cbd6f9e1fcda` |
| `ACFR-zero-waste` | `d0304dd2be19fe6a5341221fd3f863a1292e6ab331cd0522f4b9ce825e7304fe` |

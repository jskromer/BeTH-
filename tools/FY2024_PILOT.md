# FY2024 audited-fund reconciliation pilot

This pilot stages evidence and reports only. Run it with the original PDFs:

```sh
python -m pip install -r tests/requirements.txt
python tools/acfr_pilot.py --out staging/fy2024
python -m unittest discover -s tests -v
python tools/ledger.py data/funds/*.json
python tools/acfr_funds.py annual-comprehensive-financial-report-fy2025.pdf data/funds
git diff --exit-code -- data/funds docs
```

The official FY2024 original is committed at
`staging/fy2024/source/annual-comprehensive-financial-report-fy2024.pdf`.
It was retrieved on **2026-10-22**, from:

<https://berkeleyca.gov/sites/default/files/documents/annual-comprehensive-financial-report-fy2024.pdf>

Discovery page:
<https://berkeleyca.gov/your-government/financial-information/financial-reports-and-policies/financial-reports-policy-documents>

The original file is 14,469,968 bytes with SHA-256
`5f794ea95c15b6ba83e8d233a04081f3b8304381fc2172e37006a39a1a8003b5`.
The report's retrieval date refers to this archived acquisition, not to each local
rerun. The FY2025 PDF is the existing repository source; its original retrieval
date is unknown and is recorded as null, never fabricated.

To obtain another copy for comparison:

```sh
curl --fail --location https://berkeleyca.gov/sites/default/files/documents/annual-comprehensive-financial-report-fy2024.pdf --output /tmp/beth-fy2024.pdf
python tools/acfr_pilot.py --pdf /tmp/beth-fy2024.pdf --out /tmp/beth-fy2024-report
```

The downloaded bytes must match the pinned checksum before a report is written.
Using a differently named source file changes that filename in the provenance;
use the archived file for byte-identical report reproduction. No network access
occurs in extraction, tests or CI.

## Configuration and compatibility

`tools/acfr_years/2024.json` and `2025.json` hold statement PDF/printed pages,
financial year, source ID/URL, exact expected checksum, beginning/ending-balance
labels, wrapped-label aliases, nonfinancial headings and name aliases. Each page
must contain the expected statement/year heading. No year is inferred from values.
Dates, source metadata and pages in `acfr_funds.py` now come from configuration.
Its default CLI still performs the same FY2025 safety update and the strict
`ledger_safety.py` policy is unchanged. The shared-file change is limited to
`tools/acfr_funds.py`; the parser, validator, registry and fund schema are untouched.

`tests/fixtures/fy2025-full-extraction.json` captures all 106 complete records from
the merged pre-pilot extractor at `350f1cd`, including generated `flow_detail`,
notes and metadata. The new full-output test supplements the original 105-fund
annual-value fixture. Neither equivalence fixture substitutes for independent
arithmetic reconciliation.

The pilot uses the existing position-based parser, with explicit label/name
normalization in a separate read-only module. It preserves every financial row
including zero, negative and unread/null values. It neither patches the reviewed
ledgers nor adds `series` to extracted or existing records. Name mappings are
staged and require review; there is no financial split/merge or amount-based
identity inference. Unexpected identity collisions are collected as conflicts,
and never renamed or silently overwritten.

## Outputs

- `manifest.json`: source provenance, configuration checksums, and before/after
  Git-tracked ledger and website SHA-256 snapshots. Full local snapshots,
  including ignored files, are still compared in memory; ignored local paths are
  excluded from committed provenance for clean-checkout reproducibility.
- `funds.json`: all 105 FY2024 fund-column proposals, statement evidence, values,
  signed transfers, source labels, existing reviewed records, checks and issues.
- `identity-map.json`: FY2024 observed names and stable BeTH IDs, with corresponding
  FY2025 names. All mappings await independent review.
- `discrepancies.json`: the complete batch, including fund issues, all horizontal
  statement checks, FY2025 comparator controls and missing current-ledger IDs.
- `RECONCILIATION.md`: the human-readable report for every extracted fund and a
  separate entry for the FY2025 ledger with no FY2024 column. It includes the list
  of decisions requiring Steve's approval.

The report covers governmental and proprietary funds in BeTH's current ledger
model: 5 major governmental, 83 nonmajor governmental, 8 enterprise and 9 internal
service columns in FY2024. Fiduciary trust/custodial statements and component units
have different accounting models and are explicitly outside this pilot; their
scope is an approval item, not silently mixed into operating fund data. The single
FY2025 ledger without an FY2024 column is also reported as INCOMPLETE, with no
assumption that the fund did not exist.

## Accounting checks and status meanings

For every fund the pilot sums revenue and expenditure categories, checks reported
net change against financing/transfers on the appropriate basis, and checks
beginning plus net change against ending. Proprietary checks separately verify
operating income, nonoperating components and income before transfers. Transfers
out retain the signed printed value and a separate positive directional value.
No unexplained balancing adjustment or inferred zero is inserted.

Horizontal controls use each published total/subtotal against its component fund
columns. Other Governmental Funds bridges the major and nonmajor statements;
Internal Service Funds bridges the proprietary and internal-service statements.
Scope-specific enterprise rows absent from the narrower internal-service statement
are explicitly listed as not comparable. Printed blank aggregate balances are
INCOMPLETE, not replaced by summed values.

FY2024 endings are compared to FY2025 original openings. Where FY2025 explicitly
reports a restatement, original opening plus stated adjustment must equal restated
opening. Reported originals, adjustments and restated openings stay separate.
FY2025 Note 15 is identified for independent review of accounting explanations;
the code checks statement arithmetic, not a semantic interpretation of that note.

Statuses use precedence CONFLICT, INCOMPLETE, PENDING REVIEW, RECONCILED. A check
can be RECONCILED while its fund remains PENDING REVIEW. A missing reviewed field
is a review item, never a value conflict. Existing and extracted values are both
retained on a disagreement. Shared statement-control disagreements are visible
for all member funds but are not falsely attributed as individual fund-value
conflicts. Every fund has a separate human review status, initially PENDING REVIEW.
Confidence expresses the overall evidence limitations; it does not signify approval.

The normal command exits 0 when it successfully writes the complete report, even
if financial issues remain. `--require-reconciled` exits 1 on unresolved fund,
statement, missing-identity or batch issues; CI uses report reproducibility rather
than requiring known audit gaps to disappear. Parsing errors are collected by page
pair, missing values by field, and conflicts by fund/control, so the report is not
limited to the first problem. A corrupt/wrong-checksum source or unsafe output
path is a fatal input error and produces no report.

Staging output cannot overlap `data/`, `docs/` or the input ledger directory;
repository output must be under `staging/`. Symlinked output files are refused.
The pipeline snapshots the full ledger directory and website before and after
reading them. The pilot has no ledger updater or page-builder call.

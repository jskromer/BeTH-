# Validation of FY2025 page-77 expense proposals

- Source visually checked: FY2025 ACFR, PDF page 77, printed page 42. Original
  PDF SHA-256 is recorded in both correction artifacts and remains unchanged.
- Exact omitted amounts: General Fund $20,312,681 (housing $20,221,797 plus TRAN
  costs $90,884); Grants $13,584,981 (housing); Capital Improvement $2,700,992
  (housing). Total: $36,598,654.
- Proposed expense sums equal audited totals: General Fund $276,941,924; Grants
  $47,263,088; Capital Improvement $16,085,754. Library ($26,186,710) and Measure O
  ($0) already reconcile and require no additions.
- `python -m unittest discover -s tests -v`: **40 tests passed**, 31.624 seconds
  locally. Eight new tests cover aliases, duplicate-alias failures, FY2024 wrapped
  interest, exact source/deficit amounts, all five major-fund totals, preservation,
  transfers and idempotent proposal generation.
- The original full-output fixture is unchanged. Its comparison allows only the
  four independently specified missing expense rows; every other field must match.
  The original annual-value regression still matches exactly.
- Both `data/funds` and `docs` are compared before/after staging. All 106 existing
  ledger JSON files and all six protected ledgers remain byte-for-byte unchanged.
  No dashboard files or page builders are involved.
- Default FY2025 extraction still updates zero existing files. Corrected rows are
  returned for fresh extraction; the append-only updater preserves existing
  flow_detail blocks. The proposals do not override protected-ledger rules.
- General Fund is explicitly protected, and every proposed addition is marked for
  manual approval. The JSON contains baseline ledger hashes, old/proposed outflow
  arrays and per-category source amounts; no automatic apply command exists.

Reproduce the proposed corrections with:

```sh
python tools/reconcile_expenditure_breakdown.py
```

The FY2024 pilot's financial staging records and all source provenance are
unchanged. Only its dependency manifest is regenerated for the new code/tests.

# Validation of FY2025 page-77 expense and financing proposals

- Source visually checked: FY2025 ACFR, PDF page 77, printed page 42. Original
  PDF SHA-256 is recorded in both correction artifacts and remains unchanged.
- Exact omitted amounts: General Fund $20,312,681 (housing $20,221,797 plus TRAN
  costs $90,884); Grants $13,584,981 (housing); Capital Improvement $2,700,992
  (housing). Total: $36,598,654.
- Independently visually verified financing on the wrapped “subscriptions” row:
  General Fund $18,156,996; Grants $19,381; omitted financing total $18,176,377.
  The Other Governmental Funds aggregate $6,384,300 completes the printed row total
  $24,560,677 and must not be added as a separate ledger.
- Proposed expense sums equal audited totals: General Fund $276,941,924; Grants
  $47,263,088; Capital Improvement $16,085,754. Library ($26,186,710) and Measure O
  ($0) already reconcile and require no additions.
- `python -m unittest discover -s tests -v`: **45 tests passed**, 34.209 seconds
  locally. Thirteen correction tests cover expense and financing aliases,
  duplicate-alias failures (including equal and zero amounts), exact source
  values, financing/revenue/transfer separation, net-change and balance bridges,
  all five major-fund totals, preservation, patch checksums and idempotency.
- The original full-output fixture is unchanged. Its comparison allows only the
  four independently specified missing expense rows and two financing rows;
  every other field must match.
  The original annual-value regression still matches exactly.
- Both `data/funds` and `docs` are compared before/after staging. All 106 existing
  ledger JSON files and all six protected ledgers remain byte-for-byte unchanged.
  No dashboard files or page builders are involved.
- Default FY2025 extraction still updates zero existing files. Corrected rows are
  returned for fresh extraction; the append-only updater preserves existing
  flow_detail blocks. The proposals do not override protected-ledger rules.
- General Fund is explicitly protected, and every proposed addition is marked for
  manual approval. The JSON contains baseline ledger hashes, old/proposed inflow
  and outflow arrays and per-category source amounts; no apply command exists.
- Exactly three RFC 6902 JSON Patch proposals are in `patches/`: General Fund and
  Grants combine expenditure and financing corrections; Capital Improvement
  contains its expenditure correction only. Each tests the original arrays before
  replacement. Tests evaluate copies in memory; no ledger patch is applied.
  Per-patch SHA-256 checksums are in the report, proposals and `patches/SHA256SUMS`.
- General Fund net other financing: −$6,774,558; net change $2,124,690.
  Grants: $24,222 and $9,337,798. Capital Improvement: $12,582,617 and −$3,342,122.
  Each equals its audited value; beginning balance plus change equals ending
  balance. All annual totals, own revenue, transfers and balances are preserved.

Reproduce the proposed corrections with:

```sh
python tools/reconcile_expenditure_breakdown.py
```

The FY2024 pilot's financial staging records and all source provenance are
unchanged. Only its dependency manifest is regenerated for the new code/tests.

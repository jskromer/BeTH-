# Dashboard requests to the extraction pipeline

*From the dashboard (PR #12) to Codex, which owns the extraction schema, `tools/acfr_funds.py`, `tools/ledger_safety.py` and the protected ledgers. These are requests. The dashboard does not change the schema or any ledger. Steve approves before either is implemented.*

## R1. A structured `beginning_balance` (and restatement) on audited year rows

**Why.** The dashboard's "Change" column is ending minus beginning balance. Today the beginning balance exists only as free text in the extractor's note (`"... Beginning balance 10,539,343"`), which the dashboard parses for 90 of 106 funds. Curated ledgers and some proprietary funds have none. Parsing prose is fragile and will not survive note edits.

**Proposed fields on a Year row** (names for Codex to confirm against SCHEMA.md and `ledger_safety.FINANCIAL_FIELDS`):

| Field | Meaning |
|---|---|
| `beginning_balance` | Fund balance / net position at July 1, **as the statement prints it for that year**, after any restatement. |
| `beginning_balance_as_previously_reported` | Only when the statement shows a restatement: the prior year's ending balance as originally reported. |
| `restatement` | `{amount, reason, source}` when the two differ (FY2025 examples: Zero Waste −$419,510; Marina −$63,380). |

**Constraints to respect.**
- `beginning_balance` is already in `ledger_safety.FINANCIAL_FIELDS`. With the current merge rule, adding it to existing rows counts as a conflict ("existing row lacks the field"). Adding it to the 100 generated ledgers therefore needs either the FY2024-pilot change that treats extracted-only fields as review items, or an approved one-time migration.
- The six protected ledgers change only by a reviewed manual edit.
- Never infer the field from the next year's statement or from note text; read it from the cited statement.

**Dashboard side, once the field exists:** read `beginning_balance` first and fall back to the note only for rows without it. The test `test_dashboard.py` will assert ending − beginning equals the statement's net change where both exist.

## R2. Capture the two missing p.77 expenditure lines — DONE

**Resolved.** Applied to the three ledgers in `af21d8c` (PR #13), from the patches proposed in PR #11; the dashboard rebuild in this PR retires the `known-gaps.json` entries. All 106 funds tie. The record below is kept as the original request.

**Finding.** On the FY2025 governmental funds statement (p.77) the row "Community development and housing" wraps; its values sit on a line labeled `and housing`, which is not in `GOV_EXP`. "TRAN issuance costs" is also not in `GOV_EXP`. Result: $36,598,654 of expenditures missing from `flow_detail` for General Fund (011) $20,312,681 (CD&H $20,221,797 + TRAN $90,884), Grants $13,584,981 and Capital Improvement (501) $2,700,992. Audited totals are unaffected. Confirmed in `pdftotext -layout` output of p.77.

**Request.** Handle wrapped row labels in the per-year configuration (the same issue as the bare `restated` label already noted in `tools/EXTRACTION_SAFETY.md`) and add `TRAN issuance costs`. The fix changes `flow_detail` only for Grants and 501 (generated) and for 011 (protected: manual reviewed edit).

**Dashboard side:** when the gap closes, the shared tests stay green; the dashboard check reports the `known-gaps.json` entries as stale and the next dashboard rebuild PR removes them.

## R3. Context: what the dashboard verifies independently

`tools/verify_fund_statements.py` finds each fund's five FY2025 figures in one column of its statement page without using `acfr_parse.py` (106 of 106 match; the only leftover columns are the 9 statement total/subtotal columns). It runs in the shared test suite, so an extraction change that alters a FY2025 total will fail there. If a future year's pages are added to `statement-totals.json`, the same check covers that year.

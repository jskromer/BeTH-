# Dashboard Phase 2: deficit tracker and remediation tracker (specification only)

*Status: specification for review. Nothing here is implemented. Phase 1 is PR #12 (audited fund statements). The plan's Deliverable 6 names both trackers (`plans/fund-dashboard-and-agents-plan-2026-10-22.md`, sections 0 and 6).*

## Why a separate phase

Phase 1 shows **audited** figures only. Both trackers mix bases: budget (adopted), staff projection, and audit. They also depend on events not yet in the record (the November 3, 2026 vote on Measures U and V; the FY2026 ACFR, expected early 2027). They need their own data files, labels and review gate before anything publishes.

Today the same content lives in two hand-written pages: `docs/emergency-remediation.html` ("If Measures U and V Fail") and `docs/deficit-tenure-ledger.html`. Phase 2 makes them data-driven and adds them to the dashboard. It does not replace their prose.

## 1. Deficit tracker

**Question it answers:** each year, how large was the General Fund gap the City described, how was it closed, and what did the audit then show?

**Data:** `data/tracker/deficit.json`, one row per fiscal year and basis.

| Field | Meaning |
|---|---|
| `fy` | Fiscal year |
| `basis` | `adopted` (budget), `projected` (staff forecast), `audited` (ACFR) |
| `gap` | The deficit as the cited document states it; `null` if not stated |
| `closed_with[]` | `{source_kind: reserve / one_time / transfer_in / holiday / reduction / revenue, amount, fund, instrument, source}` |
| `recurring` | Whether each closing item recurs by its own terms |
| `audited_result` | For `audited` rows: General Fund revenue − expenditures, and net transfers, from the fund ledger (linked, not copied) |
| `source`, `confidence`, `reviewer` | As in the fund schema; `agent:proposed` rows do not render |

**Display:** one row per year with budget gap, one-time closes and audited result side by side, never on one summed axis (different bases). One-time vs recurring is shown as a split.

**Integrity rules:**
- Budget and audited figures are never netted against each other.
- A "structural deficit" label appears only where the City's own document uses the term; otherwise "budget gap".
- Each closing item links to its flow event in the fund ledger where one exists (e.g. the Workers' Compensation holiday and transfer).

**Seed:** the one-time plugs listed in the plan and the General Fund ledger's `status.years_in_deficit` text, each re-verified against its budget document before entry.

## 2. Remediation tracker

**Question it answers:** what has the City said it will do to close the gap, what has it actually done, and what is each item worth?

**Data:** `data/tracker/remediation.json`.

| Field | Meaning |
|---|---|
| `id`, `title` | Stable id |
| `origin` | `city_scenario` (the City's Scenario 2 list) or `beth_stack` (tiers A/B/C from the plan, section 6.2) |
| `tier` | A / B / C / counter |
| `sizing` | `{amount, basis: sourced / staff estimate / unsized, source}`. Unsized items carry `amount: null`, never a guess |
| `status` | `proposed` → `adopted` → `implemented`, or `dropped` / `reversed` |
| `events[]` | Dated actions: `{date, instrument (AAO, resolution, MOU, budget item), what, amount, source, reviewer}` |
| `audit_basis` | The audit recommendation it rests on, if any |
| `counterargument` | Required text (plan rule: every finding carries one) |

**Display:** two columns, the City's list and BeTH's stack, as on the current page. Each item shows status, sourced size (or "unsized") and its latest event. Totals are given only over **sourced** amounts, and labeled as such.

**After November 3:**
- If U and V pass: the tracker follows what the City said it would do with the money.
- If either fails: the tracker records the City's actual actions weekly (AAO amendments, service reductions, MOU items).

The election outcome is a single dated event, not a code branch.

## 3. Shared rules
- Same review gate as fund flows: agents propose (`reviewer: "agent:proposed"`), a person approves, and only approved rows render.
- No dollar figure is inferred; ranges are recorded as the document gives them.
- Labor-cost items (tier C) stay "unsized" until the MOU and CalPERS model the plan describes exists.
- Links run both ways: tracker rows link to fund ledgers and fund pages link back.

## 4. Dependencies and order
1. PR #12 reviewed and merged (Phase 1).
2. The agent pipeline (Deliverable 5) proposes events; until it exists, entries are hand-entered with sources.
3. November 3 outcome recorded as an event.
4. FY2026 ACFR loaded by the extraction pipeline, which gives the first audited year after the current budget plugs.

## 5. Acceptance criteria
- Every rendered number cites a source and carries a basis label: adopted, projected or audited.
- No chart or total mixes bases; a test checks this as in Phase 1.
- Unsized items count toward no total.
- The existing two pages keep their URLs; the dashboard links to them until their content is migrated.

## 6. Decisions needed from Steve
- Whether the trackers live on `docs/dashboard.html` (as tabs) or as separate pages linked from it.
- Whether `deficit-tenure-ledger.html`'s on-whose-watch framing belongs in a dashboard that is otherwise neutral, or stays a separate editorial page.
- Who besides Steve may approve tracker rows.

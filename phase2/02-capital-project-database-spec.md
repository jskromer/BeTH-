# Capital project database specification

**Phase 2 deliverable 3 — draft, 2026-10-23**
**Status:** Schema specification. No data loaded. No claim that the City maintains a database in this shape.

## Scope

A source-linked record of every Berkeley capital project sufficient to answer one question honestly: **how much money could lawfully be moved to street rehabilitation, and what would be given up?**

The adopted **FY2027–FY2031 CIP** (Council, June 23, 2026) contains **149 projects** and identifies **over $2.1 billion** in infrastructure and facilities needs. That $2.1B is a *need*, not an appropriation, and not cash.

## The four quantities that must never merge

Most public budget reporting fails by collapsing these. The schema separates them structurally so a query cannot accidentally add them.

| Quantity | Meaning | Available to redirect? |
|---|---|---|
| **Identified need** | Engineering estimate of work that should happen | **No.** Not money. |
| **Appropriation** | Council-granted authority to spend | Only if unspent, unencumbered and unrestricted |
| **Encumbrance** | Legally committed by contract or PO | **No.** Breaking costs money. |
| **Expenditure** | Cash actually paid | **No.** Already gone. |

`net_releasable = appropriation − expenditures − encumbrances − cancellation_cost − grant_clawback − preservation_cost`, **and only when `restriction_class = 'unrestricted'`**. Any other formula is wrong.

## Tables

### `capital_projects` — identity and scope
`project_id` (PK, City's own ID; never invent one) · `cip_cycle` · `title` · `description` · `department` · `asset_class` · `geographic_area` · `council_district` · `related_asset_ids[]` · `delivery_stage` (concept | planning | design | bid | construction | closeout | complete) · `project_manager` · `planned_start` · `planned_completion` · `actual_start` · `actual_completion` · `is_safety_mandated` (bool) · `is_regulatory_mandated` (bool) · `mandate_citation` · `source_doc_id` · `evidence_date` · `confidence`

`is_safety_mandated` / `is_regulatory_mandated` require `mandate_citation` to a statute, consent decree, permit or court order. **An unsupported flag is a null flag** — a department asserting that something is required is not a mandate.

### `project_finance` — the money, one row per project per funding source per fiscal year
`project_id` (FK) · `fund_id` (FK → BeTH's 106-fund ledger) · `fiscal_year` · `original_authorization` · `current_appropriation` · `amendments[]` · `expenditures_to_date` · `encumbrances` · `remaining_appropriation` · `restriction_class` · `restriction_citation` · `restriction_expiry` · `grant_id` · `grant_clawback_risk` · `source_doc_id` · `evidence_date` · `confidence`

`restriction_class` ∈ `unrestricted` · `voter_approved_tax` · `bond_covenant` · `grant_condition` · `enterprise_fund` · `developer_impact_fee` · `gas_tax` · `court_ordered` · `unknown`

**`unknown` is the default.** A project is not redirectable until someone proves it is. `restriction_citation` is required for every class except `unknown`.

### `project_commitments` — contracts
`commitment_id` (PK) · `project_id` · `vendor` · `contract_number` · `council_approval_date` · `council_item` · `approved_on_consent` (bool) · `amount` · `amount_expended` · `amount_remaining` · `termination_clause` · `termination_cost` · `source_doc_id`

`approved_on_consent` exists because Eric's pier-ferry analysis found ~$20.7M across six consent-calendar items approved without debate. Whether a commitment was debated is a governance fact worth surfacing.

### `scenario_actions` — stop / defer / reduce / combine / continue
`scenario_id` · `project_id` · `action` (cancel | defer | reduce_scope | combine | continue) · `defer_years` · `gross_project_cost` · `unspent_unrestricted_balance` · `cancellation_penalty` · `grant_clawback` · `preservation_cost` (cost of mothballing/securing a stopped project) · `deferred_escalation_cost` · **`net_funds_released`** (computed) · `recurring_opex_change` · `safety_impact` · `accessibility_impact` · `environmental_impact` · `equity_impact` · `service_impact` · `assumptions[]` · `confidence`

**Headline project cost is never the released amount.** The five deductions above are mandatory fields, not optional refinements. A scenario with nulls in them produces no `net_funds_released` — it produces "insufficient data."

### `project_operating_costs` — what finishing it costs forever
`project_id` · `annual_maintenance_cost` · `annual_staffing_fte` · `annual_staffing_cost` · `annual_utilities` · `expected_useful_life_years` · `replacement_reserve_annual` · `revenue_offset` · `net_annual_operating_impact` · `basis` · `source_doc_id`

The pier-ferry case is why this table exists: a $103.6M–$200M+ capital project carrying a projected **$5,589,288 annual operating gap** in its best case, tenth service year, where public subsidy per boarding ($7.62) exceeds the fare ($7.28). A capital database without recurring operating consequences would score that as a completed asset.

### `source_documents`
`source_doc_id` (PK) · `title` · `author_body` · `publication_date` · `canonical_url` · `retrieved_date` · `page_reference` · `table_reference` · `document_type` (ACFR | adopted_budget | CIP | council_report | commission_packet | state_report | contract | EIR | third_party_analysis) · `verification_status` (verified_primary | cited_secondary | unverified) · `local_copy_path` · `sha256`

Every figure anywhere in the database carries a `source_doc_id`. No exceptions, no "staff said."

### `reconciliation_links` — the bridge to Phase 1
`link_id` · `project_id` · `fund_id` · `fiscal_year` · `beth_ledger_amount` · `cip_amount` · `variance` · `variance_explanation` · `reconciled` (bool)

Lets the dashboard show that a project's CIP figures do or do not tie to the audited fund, and say which when they don't.

## Rules enforced in the schema, not in review

1. **Budget authority is not cash.** `current_appropriation` can never flow into a "funds available" view without passing the `net_releasable` formula.
2. **Restricted is restricted until proven otherwise.** Default `unknown`; `unrestricted` requires a citation.
3. **No double counting.** Multi-funded projects get one `project_finance` row per source; the dashboard sums by `fund_id`, never by project headline.
4. **FY2025 audited balances are history, not FY2027 availability.** `project_finance` is keyed by fiscal year and the UI must label which year it is showing.
5. **Deferral has a price.** `deferred_escalation_cost` and `preservation_cost` are required for `defer` scenarios.
6. **Cancellation preserves history.** Cancelled projects are retained with reason and date; rows are never deleted.

## Load order

1. `source_documents` — the FY2027–31 adopted CIP and its amendments first.
2. `capital_projects` — all 149, identity only.
3. `project_finance` — appropriations by fund and year; **restriction research is the long pole.**
4. `project_commitments` — contracts and encumbrances.
5. `reconciliation_links` — tie to the 106-fund ledger.
6. `project_operating_costs`.
7. `scenario_actions` — last. Scenarios are meaningless until 1–6 are real.

**Do not build the scenario UI before step 3 is complete.** A pause/defer interface over unverified restriction data would produce confident, wrong answers about available money — the exact failure Phase 1 was built to prevent.

## Primary sources to load first

- Proposed FY2027–FY2031 CIP presentation: https://berkeleyca.gov/sites/default/files/legislative-body-meeting-attachments/Item%2002%20Proposed%20FY27-FY31%20Proposed%20CIP%20Budget%20Presentation.pdf
- FY2027/FY2028 biennial budget adoption (June 23, 2026): https://berkeleyca.gov/sites/default/files/2026-06/2026-06-23%20Special%20Item%2001%20Adoption%20of%20Fiscal%20Years%202027%20and%202028.pdf
- Five-Year Street Rehabilitation and Measure FF plans (July 7, 2026): https://berkeleyca.gov/sites/default/files/2026-07/2026-07-07%20Item%2010%20Five-Year%20Street%20Rehabilitation.pdf
- Measure U GO bond measure (June 16, 2026): https://berkeleyca.gov/sites/default/files/2026-06/2026-06-16%20Item%2038%20Placing%20a%20General%20Obligation%20Bond%20Measure.pdf
- City capital project directory: https://berkeleyca.gov/your-government/our-work/capital-projects

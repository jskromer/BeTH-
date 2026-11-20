# BeTH Phase 2 — Capital Choices, Asset Management, and PCI 60+

**Working research and implementation plan — October 22, 2026**
**Status:** Draft research plan, not a verified inventory of reallocatable funds or a recommendation to terminate specific projects.

## Purpose

Extend BeTH from FY2025 audited-fund reconciliation to a transparent decision-support system. Test how Berkeley could achieve and sustain Pavement Condition Index (PCI) >=60 while containing recurring payroll and benefit costs, reassessing discretionary capital commitments, and reducing avoidable paving delivery costs. Preserve the distinction among audited facts, current appropriations, encumbrances, legal restrictions, forecasts, and user-defined policy scenarios.

## Central research questions

1. What is the complete adopted FY2027–2031 capital project portfolio, including amendments and project-by-project appropriations?
2. Which projects are necessary for public safety, regulatory compliance, critical asset preservation, or binding contractual obligations? Which are discretionary, duplicative, low-utilization, or deferrable?
3. What are each project's expenditures to date, encumbrances, uncommitted balances, funding restrictions, cancellation costs, and recurring operating consequences?
4. What legally transferable funds and net recurring operating savings could support street rehabilitation?
5. How much would a PCI 60, 65, or 70 target cost, by year, using actual segment condition and treatment data?
6. Which project delivery costs stem from environmental review, ADA, utilities, safety design, procurement, design standards, or local add-ons? Which can lawfully be simplified?
7. How do these choices align with or depart from Vision 2050's adopted framework and asset management program?

## Workstreams

### 1. Capital portfolio and project pause scenarios

Create a complete, source-linked capital project inventory from the adopted FY2027–2031 CIP, later Council actions, project pages, contracts, and accounting data. Do not treat a budget as an available cash balance.

For each project track: project ID, description, department, asset class, geographic area, original authorization, current appropriation, actual spend, outstanding encumbrances, funding source and legal restriction, schedule, current stage, sunk costs, cancellation/delay penalties, grants at risk, safety/compliance requirement, expected benefit, future maintenance and staffing costs, and confidence/source date.

**Explicit stop/defer/reduce analysis:** Test a temporary hold on *new discretionary commitments* for projects not yet in construction, subject to documented exceptions for safety, legal mandates, critical infrastructure, and obligations. Evaluate each project independently for (a) complete cancellation, (b) one-to-three-year deferral, (c) reduced scope, (d) combining with another project, or (e) continuation. Quantify **net funds released**, not gross headline project cost: unspent unrestricted balance minus cancellation penalties, grant clawbacks, preservation costs, and other obligations. Document adverse consequences such as safety, accessibility, environmental, equity, and service impacts. Do not automatically pause existing work or claim money is transferable before review.

Proposed public views: **Capital Projects**, **Commitment Status**, **Pause/Defer Scenarios**, **Funding Restrictions**, **Consequences and Trade-offs**.

### 2. Streets and PCI forecasting

Import street segment IDs, length, width/area, current PCI, pavement age, traffic/utility context, annual deterioration, recommended treatment, unit cost, treatment life, and projected post-treatment PCI. Model current-policy, capital-reallocation, and operating-plus-capital-reform scenarios over 5 and 10 years. Distinguish preventing deterioration from increasing network PCI. Track dollars per lane-mile and per PCI-point, preservation versus reconstruction, and uncertainty. Reconcile results to the City's adopted paving plan and StreetSaver methodology; avoid promising PCI 60 until calibrated.

### 3. Payroll, benefits, and recurring costs

Analyze filled/vacant positions, salaries, overtime, pension employer contributions, retiree health, administrative overhead, service contracts, and future staffing associated with new capital assets. Model attrition, vacancy management, administrative consolidation, procurement changes, and prospective benefit changes, **net** of service replacement, labor agreements, pension law, and implementation costs. Separate one-time savings from recurring savings and account for fund restrictions.

### 4. Paving cost and legislative analysis

Decompose actual contract costs into pavement treatment, design, construction management, ADA, utilities, drainage, traffic safety, environmental work, green infrastructure, and discretionary scope additions. Examine routine-maintenance CEQA Class 1 exemptions (14 CCR 15301) and exceptions, ADA obligations, procurement rules, local complete-streets policies, and 'dig once' coordination. Compare legally feasible administrative simplifications with potential state statutory changes. Estimate savings only where backed by contract comparisons or documented process delays. Do not presume environmental rules are the primary cost driver.

### 5. Vision 2050: integrate existing plans and management tools

**Use the City's existing architecture, not a parallel unsupported database.** The 2020 Vision 2050 Framework includes: multi-criteria decisions and adaptive planning; a Dig Once policy; lifecycle infrastructure management and an Asset Management Program; sensors/data; increased infrastructure investment; program management tools and independent oversight. The 2022 Strategic Asset Management Plan (SAMP) and Asset Management Policy call for asset inventory, condition assessment, risk assessment, and lifecycle renewal. The 2022 Program Plan contains outcomes, prioritization, delivery, KPIs, and project approval processes.

The 2021 Vision 2050 progress report identifies asset management systems **NexGen** (operations), **AssetWorks** (equipment maintenance), and **AMCS** (Zero Waste). Confirm which remain active in 2026, their asset coverage, export capabilities, identifiers, data quality, and public disclosure limitations. The existence of these tools does not establish a single citywide integrated database.

**Draft federated asset-management database** (proposed BeTH schema, not a claim the City has implemented it):

- `assets`: stable asset ID, type, location/GIS geometry, department, ownership, installation year, expected useful life, replacement value, condition, last assessment, criticality.
- `asset_inspections`: asset ID, inspection date, method, observed condition, assessor, evidence URL, uncertainty.
- `asset_risks`: failure probability/likelihood, consequence, safety/compliance exposure, service criticality, risk score with documented weights.
- `capital_projects`: project ID, related asset IDs, scope, delivery stage, project manager, planned/actual dates, alternatives.
- `project_finance`: project ID, fund ID, appropriation, expenditures, encumbrances, remaining authorized balance, legal restrictions, evidence date.
- `maintenance_work_orders`: asset ID, preventive/corrective work, cost, date, service effect, source system.
- `scenario_actions`: pause/defer/resize/continue decisions, assumptions, release date, cancellation costs, impacts.
- `pavement_segments`: segment ID, area, PCI, deterioration model, treatment options and lifecycle costs.
- `kpis`: metric definition, baseline, target, target year, observed result, source, responsible office.
- `source_documents`: canonical URL, title, publication date, retrieval date, page/table, verification status.

**Management tools to represent in BeTH:** multi-criteria prioritization, lifecycle cost model, risk/criticality matrix, condition assessments, asset register and GIS map, Dig Once schedule, project stage gates, project controls (baseline/current budget and schedule), procurement/contract tracker, portfolio resource/capacity plan, KPIs and target dates, public progress dashboard, independent oversight, and semiannual Council reporting. Map each tool to its Vision 2050 source and mark whether adopted, proposed, implemented, or unverified.

**2026 governance checkpoint:** September 29, 2026 Council Item 26 referred an updated cross-departmental Program Plan and SAMP, maintenance schedule, and semiannual reporting to the City Manager. Track deliverables, dates, and actual public outputs; do not mistake a referral for a completed database or plan.

### 6. Public decision interface

Views: (1) Where the Money Is, (2) Which Commitments Could Change, (3) PCI Simulator, (4) Operating Costs, (5) Vision 2050 Asset Management, (6) Legal and Delivery Reforms, (7) Trade-offs. Every amount must have a fiscal year, fund source, legal status, and evidence link. Every forecast must display assumptions and uncertainty. Show alternative policy packages without presenting a predetermined political choice as a factual conclusion.

## Question-answering readiness (added October 23, 2026)

The end state for BeTH is a public interface that answers a resident's plain-language question from the City's own records, shows the calculation, cites the page, and says what the record lacks. Phase 2 does not build that interface, but every dataset it creates must be shaped for it. The requirements are in `plans/phase2-grounded-qa-architecture.md`; in short:

- Every fund, flow, project, asset, Council action, ballot measure and source document gets a stable namespaced id that is never renamed.
- Every figure carries period, reporting basis (audited, adopted, amended, projected, estimated), accounting basis, figure status (reported, derived, disputed), a document id with page and quoted text, confidence and reviewer.
- A compile step produces one machine-readable facts table and measure dictionary from all subjects, so calculations run in code and can be checked against the ACFR control totals.
- Answers separate retrieved facts, arithmetic, BeTH's interpretation and scenario assumptions, and must list missing evidence.
- Workstream 1's project inventory makes `project_id`, `funded_from[]` (with fund, ballot measure, restriction, basis, document and page) and `as_of` mandatory, so the cross-fund paving question in the addendum's section 7 can be joined.

## Data quality and reallocation safeguards

- FY2025 audited ACFR ledger reconciliations are historical, **not** FY2027 unspent balances.
- Budget authority is not cash; encumbrances are not expenditures; restricted funds are not unrestricted General Fund resources.
- Avoid double counting transfers and projects funded by multiple sources.
- Preserve project histories and reasons for cancellation or deferral.
- Show both near-term savings and deferred replacement/maintenance costs.
- Confirm whether voter-approved revenue restrictions or bond covenants prohibit diversion.
- Verify asset system names and integration status before publishing claims.

## Implementation order

1. Source register and adopted CIP extraction, including amendments.
2. Asset and project ID crosswalk, mapping CIP, BeTH funds, Vision 2050 systems, and GIS.
3. Encumbrance, fund restriction, and contract review; establish credible net discretionary balances.
4. Asset condition and pavement model ingestion and calibration.
5. Payroll/benefit baseline and ten-year forecast.
6. Project delivery/CEQA/procurement case studies.
7. Read-only BeTH prototype with transparent scenario controls and source citations.
8. Independent reconciliation, legal review of transfer assumptions, and publication.

Steps 1, 2 and 7 follow the id, provenance and answer-contract conventions in `plans/phase2-grounded-qa-architecture.md` (source register and facts compile step first, since they run on the existing fund files).

## Source links and pages

**Primary City documents**

- Vision 2050 Framework (2020): https://berkeleyca.gov/sites/default/files/documents/Vision-2050-Framework.pdf
- Vision 2050 Strategic Asset Management Plan (2022): https://berkeleyca.gov/sites/default/files/documents/Strategic-Asset-Management-Plan.pdf
- May 10, 2022 Council Item 31: SAMP and Asset Management Policy (includes resolution and exhibits): https://berkeleyca.gov/sites/default/files/2022-04/2022-05-10%20Item%2031%20Vision%202050%20Strategic%20Asset.pdf
- Vision 2050 progress report (2021), systems and management actions: https://berkeleyca.gov/sites/default/files/documents/2021-11-16%20Item%2008%20Vision%202050.pdf
- May 31, 2022 draft Vision 2050 Program Plan and decision-making methodology: https://berkeleyca.gov/sites/default/files/documents/2022-05-31%20Item%2037%20Discussion%20and%20Direction%20Regarding.pdf
- September 29, 2026 Council agenda, Item 26 (updated program and asset-management plan referral): https://berkeleyca.gov/city-council-regular-meeting-eagenda-september-29-2026
- City infrastructure plans and service page: https://berkeleyca.gov/city-services/streets-sidewalks-sewers-and-utilities
- City capital project directory: https://berkeleyca.gov/your-government/our-work/capital-projects
- City street maintenance and rehabilitation: https://berkeleyca.gov/city-services/streets-sidewalks-sewers-and-utilities/street-repair
- FY2025–2029 adopted CIP (historical reference; replace with current adopted FY2027–2031 program in research): https://berkeleyca.gov/sites/default/files/documents/FY-2025-2029-Capital-Improvement-Program.pdf

**Context / independent material**

- October 2026 discussion of Vision 2050 targets, unverified deliverables, and September referral (candidate website; secondary): https://kromerforberkeley.org/hot-topics/vision2050
- CEQA Guidelines §15301: https://www.law.cornell.edu/regulations/california/14-CCR-15301

## Next research tasks / unknowns

- Locate and extract the *complete* FY2027–2031 adopted CIP, project amendments, and FY2026/2027 encumbrance report.
- Locate any draft asset register/database, data dictionary, NexGen/AssetWorks/AMCS architecture, and current citywide asset management implementation schedule. Do **not** claim the draft database has been located yet.
- Locate full Vision 2050 program management tool descriptions and any 2026 implementation reports.
- Obtain StreetSaver segment-level PCI and current five-year paving plan in machine-readable form.
- Quantify legal transferability and actual net savings before naming projects as funding sources.

**Working principle:** Show what is known, what is legally movable, what can be changed, and what outcomes the choices might buy. Do not present a scenario as a completed policy decision.

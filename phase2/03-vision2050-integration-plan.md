# Vision 2050 asset-management integration plan

**Phase 2 deliverable 4 — draft, 2026-10-23**
**Status:** Integration plan. Verification of current system status is NOT complete; see §4.

## Principle

**Reuse the City's architecture; do not build a parallel unsupported database.** Berkeley has adopted a framework, a policy, a strategic plan and a program plan. BeTH's job is to make what exists legible and to show the gap between what was adopted and what was delivered — not to invent a competing asset register.

## 1. What the City has adopted

| Artifact | Date | What it commits to |
|---|---|---|
| Vision 2050 Framework | 2020 | Multi-criteria decisions, adaptive planning, Dig Once, lifecycle management, an Asset Management Program, sensors/data, increased investment, program management tools, independent oversight |
| Vision 2050 progress report | 2021-11-16 | Names asset systems **NexGen** (operations), **AssetWorks** (equipment maintenance), **AMCS** (Zero Waste) |
| Strategic Asset Management Plan + Asset Management Policy (Council Item 31) | 2022-05-10 | Asset inventory, condition assessment, risk assessment, lifecycle renewal; *"cost to inspect, maintain, repair and replace infrastructure systems over useful life"*; an **Annual Maintenance Plan** shared during budget development and **made public** |
| Draft Program Plan | 2022-05-31 | Outcomes, prioritization, delivery, KPIs, project approval processes |
| Mayor's Vision 2050 Task Force final report | 2025-12-02 | Reports the asset management program **still incomplete**; target of facilities, street paving, sidewalks and sewers **by July 2027** |
| Council Item 26 referral | 2026-09-29 | Refers an updated cross-departmental Program Plan and SAMP, maintenance schedule, and semiannual reporting to the City Manager |

**A referral is not a plan and a policy is not an implementation.** The 2022 policy requires a public Annual Maintenance Plan; the 2025 Task Force says the program is incomplete; the 2026 referral asks for an update. BeTH's contribution is to track that gap with dates, not to assert either that the City has a database or that it has done nothing.

## 2. The accountability finding to verify first

Eric's analysis reports that **the waterfront is not on the Vision 2050 implementation schedule**, despite being named a Parks, Recreation & Waterfront asset in the 2022 policy (Task Force report, 2025-12-02, p.11).

If that holds, the largest single identified unfunded asset class BeTH has found — **$163,344,000** on the waterfront — sits outside the City's asset-management implementation plan entirely, while the implementation targets facilities, street paving, sidewalks and sewers by July 2027.

**Status: unverified.** Read the Task Force report directly before publishing. This is the highest-value single verification in the Vision 2050 workstream.

## 3. Mapping BeTH to the adopted framework

BeTH does not need new concepts. Each Phase 2 structure maps to something already adopted:

| Adopted commitment | BeTH structure | Phase 2 status |
|---|---|---|
| Asset inventory | `assets` | Schema only; City inventory not located |
| Condition assessment | `asset_inspections` | Schema only; PCI data is the one real candidate |
| Risk assessment | `asset_risks` | Schema only; weights must be documented, not invented |
| Lifecycle renewal | `project_operating_costs` + `replacement_reserve_annual` | Specified in deliverable 3 |
| Multi-criteria prioritization | `scenario_actions` with impact fields | Specified; criteria weights must cite the Program Plan |
| Dig Once | coordination flag on `capital_projects` | Not yet specified |
| Project stage gates | `capital_projects.delivery_stage` | Specified |
| Project controls (baseline vs current) | `project_finance.original_authorization` vs `current_appropriation` | Specified |
| Procurement/contract tracking | `project_commitments` | Specified |
| KPIs and target dates | `kpis` | Schema only |
| Public progress dashboard | deliverable 6 | Specified |
| Semiannual Council reporting | `kpis` + `source_documents` tracking | Tracking only |

Each row is marked **adopted / proposed / implemented / unverified** in the published view. BeTH must never imply the City has implemented something because the City adopted a policy requiring it.

## 4. What must be verified before publishing anything about City systems

The 2021 progress report names NexGen, AssetWorks and AMCS. **Five years is a long time in municipal software.** Before BeTH names any system publicly:

1. Is each system still in use in 2026?
2. What asset classes does each actually cover?
3. Can data be exported, and in what format?
4. What are the asset identifiers, and do they reconcile across systems and to GIS?
5. What is the data quality and completeness?
6. What are the public disclosure limitations?

**The existence of three named systems does not establish a single integrated citywide asset database, and BeTH must not say or imply that it does.** Equally, BeTH must not assert the City lacks asset data without having asked.

**Status: none of the six questions is answered.** This requires either published documentation or a records request. It is the main blocker on the Vision 2050 deliverable.

## 5. Where streets fit

Streets are the one asset class where the City's own machinery is most likely to yield usable data, because PCI and StreetSaver are established practice and the Five-Year Street Rehabilitation and Measure FF plans were before Council on July 7, 2026. Streets are therefore the **pilot asset class** for the federated approach: prove the schema, the identifiers and the source discipline on pavement before extending to facilities or the waterfront.

## 6. Source links

- Vision 2050 Framework (2020): https://berkeleyca.gov/sites/default/files/documents/Vision-2050-Framework.pdf
- Strategic Asset Management Plan (2022): https://berkeleyca.gov/sites/default/files/documents/Strategic-Asset-Management-Plan.pdf
- Council Item 31, SAMP and Asset Management Policy (2022-05-10): https://berkeleyca.gov/sites/default/files/2022-04/2022-05-10%20Item%2031%20Vision%202050%20Strategic%20Asset.pdf
- Vision 2050 progress report (2021-11-16), systems and management actions: https://berkeleyca.gov/sites/default/files/documents/2021-11-16%20Item%2008%20Vision%202050.pdf
- Draft Program Plan and decision methodology (2022-05-31): https://berkeleyca.gov/sites/default/files/documents/2022-05-31%20Item%2037%20Discussion%20and%20Direction%20Regarding.pdf
- Council agenda, Item 26 referral (2026-09-29): https://berkeleyca.gov/city-council-regular-meeting-eagenda-september-29-2026
- Five-Year Street Rehabilitation and Measure FF plans (2026-07-07): https://berkeleyca.gov/sites/default/files/2026-07/2026-07-07%20Item%2010%20Five-Year%20Street%20Rehabilitation.pdf
- **Not yet located:** Mayor's Vision 2050 Task Force final report (2025-12-02) — cited by Eric at p.11; direct URL needed.

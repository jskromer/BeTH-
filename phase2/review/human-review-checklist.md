# Human review checklist: Ask BeTH answers (prototype)

**Generated** from `phase2/docs/data/answers.json` by `phase2/tools/build_review_checklist.py`. Do not edit by hand; record decisions in `phase2/review/human-approvals.json`.

**What the automated checks did.** For every answer: each cited document and PDF page exists; each number matches a BeTH data record or is printed on its cited page; each quote appears on its cited page; each calculation is recomputed from its input facts; every dollar figure, percentage and mileage in the text traces to a fact, calculation or cited quote.

**What they did not do, and what this review is for:**
- that the cited page supports the claim made from it (human source verification)
- that any legal interpretation is correct
- that the calculation method is the appropriate one for the question
- that answers are consistent with one another

The open interpretations listed under each answer are BeTH's own list and are not checked by any automated test. A reviewer should add any others found.

**How to review.** For each fact, open the PDF at the cited page and tick the box only if the page supports the claim as worded. Check each calculation's method, not just its arithmetic. Then record a decision in `human-approvals.json`: `APPROVED`, `APPROVED WITH CHANGES` (list them) or `NOT APPROVED`.

---

## How much capital funding could Berkeley redirect to streets?

Page: `phase2/docs/ask/capital-to-streets.html` · Automated checks: passed · Human source verification: **NOT PERFORMED** · Approval: **NOT APPROVED**

### Central claim

> From CIP Fund 501: a gross conditional ceiling of $2,946,000 of FY2027-FY2028 appropriations, or $2,916,000 excluding a contractual Joint Powers Agreement contribution. It is reached only by deferring or cancelling every other project the fund pays for, and neither figure is verified available cash. 88% of the fund's FY2027 money ($10,412,200) already goes to paving. A one-time amount from unspent carried-over appropriations may exist but cannot be measured from public records; its ceiling at June 30, 2025 was $11,568,647. From Measure FF: the adopted program already puts 45.6% into street rehabilitation, against a voter-set allocation of "approximately" 45% that Council cannot alter without a vote. Whether more could go to paving without a vote is an unresolved legal question, and BeTH states no amount.

BeTH's reading (Moderate): The fund 501 money Council could move to paving is small relative to the paving gap: the City estimates PCI 70 needs about $8 million a year more, while fund 501's non-paving capital is $1,473,000 a year, mostly repairs to existing City buildings.

Counterargument: This covers only fund 501 and Measure FF. Other capital funds, unspent carryovers, the General Fund itself and delivery-cost savings are not assessed here and could change the total.

### Calculations

- [ ] **Gross conditional deferral ceiling: fund 501 non-paving appropriations, FY2027 + FY2028**: $1,473,000 + $1,473,000 = **$2,946,000** (`fund:501/cip/fy2027/other + fund:501/cip/fy2028/other`). Appropriations, not verified available cash. Reached only by deferring or cancelling every one of them.
- [ ] **Deferral ceiling excluding the contractual JPA contribution**: $2,946,000 − $30,000 = **$2,916,000** (`c1 − fund:501/cip/fy2027-28/contractual-jpa`). Not verified available cash.
- [ ] **Share of fund 501 FY2027 money already in paving**: $10,412,200 ÷ $11,885,200 = **87.61%** (`fund:501/cip/fy2027/paving ÷ fund:501/cip/fy2027/total`)
- [ ] **Unencumbered assigned fund balance, June 30, 2025 (ceiling for one-time carryover)**: $16,060,094 − $4,491,447 = **$11,568,647** (`fund:501/acfr/2025/assigned − fund:501/acfr/2025/encumbrances`). Backs capital appropriations already carried forward, paving among them. Not free money.

Tick a calculation only if its method is the right one for the claim, not only if the arithmetic is correct.

### Sources

| Page supports claim? | Fact | Value | Document (local file) | Cited | PDF page(s) | Quote | Automated check |
|---|---|---|---|---|---|---|---|
| [ ] | Fund 501 (CIP Fund) FY2027 capital program | $11,885,200 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | p.173 (fund 501 Grand Total; also p.170) | 173 |  | matches data record; value printed on cited page |
| [ ] | Of which Streets (paving) | $10,412,200 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | p.173 (Streets Total) | 173 |  | matches data record; value printed on cited page |
| [ ] | Of which all other fund 501 projects | $1,473,000 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | pp.172-173 (sum of non-Streets lines) | 172-173 |  | matches data record |
| [ ] | FY2028, all other fund 501 projects | $1,473,000 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | pp.172-173 (sum of non-Streets lines) | 172-173 |  | matches data record |
| [ ] | Of which a contractual Joint Powers Agreement contribution | $30,000 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | pp.172-173 (Tom Bates turf JPA contribution, FY2027 + FY2028) | 172-173 |  | matches data record |
| [ ] | Fund 501 assigned fund balance, June 30, 2025 | $16,060,094 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.75 (printed p.40) | 75 |  | value printed on cited page |
| [ ] | Fund 501 encumbrances outstanding, June 30, 2025 | $4,491,447 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.142 (printed p.108) | 142 |  | matches data record; value printed on cited page |
| [ ] | Capital appropriations carry forward | (text) | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.180 (printed p.146) | 180 | Any unused funds are re-appropriated to the following fiscal year until the project is completed. | quote found on cited page |
| [ ] | Who controls assigned fund balance | (text) | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.103 (printed p.69) | 103 | Intent is expressed by the City Council or City Manager, to which the City Council has delegated the authority | quote found on cited page |
| [ ] | City statement on CIP Fund availability | (text) | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | p.239 | 239 | there is no CIP funding available for IT in FY 2027 and FY 2028 | quote found on cited page |
| [ ] | City estimate of the added annual cost of PCI 70 | (text) | Five-Year Street Rehabilitation and Measure FF Plans FY2027-2031, Council Item 10, July 7, 2026 (`phase2/sources/street-rehab-measure-ff-2026-07-07.pdf`) | p.12 | 12 | This scenario requires an estimated $37.6 million per year3, approximately $8 million per | quote found on cited page |
| [ ] | Allocation set by voters | (text) | Measure FF (SAFE STREETS) initiative text, BMC Chapter 7.11 (Council agenda July 9, 2024, Item 22) (`phase2/sources/measure-ff-initiative-council-2024-07-09.pdf`; quotes checked against `phase2/sources/measure-ff-ordinance-transcription.md`) | BMC 7.11.020(C), PDF p.8 | 8 | Tax proceeds shall be allocated approximately as follows: 1) 60% for streets and sidewalks, of which roughly three quarters (45%) will be for streets and one quarter (15%) will be for sidewalks and pedestrian paths, until the backlog of damaged sidewalks and pedestrian paths is eliminated. 2) 30% for safety improvements. 3) The remaining 10% shall include environmental enhancements | quote found on cited page |
| [ ] | Council may not alter the Measure FF allocation without voters | (text) | Measure FF (SAFE STREETS) initiative text, BMC Chapter 7.11 (Council agenda July 9, 2024, Item 22) (`phase2/sources/measure-ff-initiative-council-2024-07-09.pdf`; quotes checked against `phase2/sources/measure-ff-ordinance-transcription.md`) | Section 7(a)(3), PDF p.15 | 15 | Alter the allocations of Section 7.11.020 | quote found on cited page |
| [ ] | Share of the five-year Measure FF program in street rehabilitation (BeTH ratio: $42,119,935 printed on budget p.215, over the program total, BeTH's sum of the Table 1C category totals) | 45.64% | Five-Year Street Rehabilitation and Measure FF Plans FY2027-2031, Council Item 10, July 7, 2026 (`phase2/sources/street-rehab-measure-ff-2026-07-07.pdf`) | p.4 (Table 1C); budget-adoption p.215 | 4 |  | matches data record |

### Unresolved legal or accounting interpretation

- [ ] Whether any non-paving fund 501 project could be deferred without legal, contractual, safety or condition consequences. Not assessed.
- [ ] Whether the FY2027-28 appropriations are still uncommitted: encumbrance and spending status is not public, so the ceilings are appropriations, not available cash.
- [ ] Whether the June 30, 2025 unencumbered assigned balance ($11,568,647) is still uncommitted; it is sixteen months old and backs carried-forward projects.
- [ ] The Measure FF allocation questions (see the Measure FF page): BeTH states no Measure FF amount.
- [ ] The maintenance-of-effort floor is a BeTH estimate (base year and inflation index not stated in the ordinance); it limits moving paving money out, not in.
- [ ] Amendments made from the dais on June 23, 2026 are not in the packet; the FY2027 Annual Appropriation Ordinance is the controlling record and is not in BeTH's sources.

### Missing evidence

- FY2026 year-end fund 501 carryover and encumbrance detail by project.
- The FY2027 Annual Appropriation Ordinance (controlling appropriation record, incl. any June 23 amendments).
- Public Works and Parks assessments of what deferring each fund 501 project would cost (condition, safety, legal, contracts).
- The City's Measure FF maintenance-of-effort calculation and whether FY2027 draws on the Stabilization Reserve.
- Restriction research for the other CIP funding sources.
- A City Attorney opinion or Council interpretation of the Measure FF allocation (BMC 7.11.020(C)) as it applies to added paving

### Independent human approval

Recorded in `phase2/review/human-approvals.json` → `answers.capital-to-streets`. Current status: **NOT APPROVED**.

| Field | Entry |
|---|---|
| Reviewer |  |
| Date |  |
| Decision | NOT APPROVED |
| Changes required |  |
| Notes |  |

---

## Could Measure FF money pay for more street paving?

Page: `phase2/docs/ask/measure-ff-paving.html` · Automated checks: passed · Human source verification: **NOT PERFORMED** · Approval: **NOT APPROVED**

### Central claim

> Not established. Voters set the split at approximately 45% streets, 15% sidewalks and paths, 30% safety and 10% environmental and other uses, and Council cannot alter it without a vote. The adopted program already puts 45.6% of Measure FF ($42,119,935 of $92,282,816) into street rehabilitation. Whether Council could put more into paving without a vote turns on unresolved legal questions: how much room "approximately" allows, whether the shares apply each year or over the life of the tax, and how revenue not yet programmed may be used. BeTH states no amount.

BeTH's reading (Moderate): The adopted program is already at the ordinance's approximate street share, so more Measure FF paving would have to come from the latitude "approximately" allows or from revenue not yet programmed. How large that latitude is cannot be settled from the ordinance text.

Counterargument: A strict reading, with the shares binding each year's appropriations, leaves little or no room. A looser reading, with the shares measured over the 14-year life of the tax, could allow more paving in early years balanced later. No City Attorney opinion in BeTH's sources settles which applies.

### Calculations

- [ ] **Street rehabilitation share of the five-year Measure FF program**: $42,119,935 ÷ $92,282,816 = **45.64%** (`ff:program/street-rehab ÷ ff:program/total`)

Tick a calculation only if its method is the right one for the claim, not only if the arithmetic is correct.

### Sources

| Page supports claim? | Fact | Value | Document (local file) | Cited | PDF page(s) | Quote | Automated check |
|---|---|---|---|---|---|---|---|
| [ ] | Allocation set by voters | (text) | Measure FF (SAFE STREETS) initiative text, BMC Chapter 7.11 (Council agenda July 9, 2024, Item 22) (`phase2/sources/measure-ff-initiative-council-2024-07-09.pdf`; quotes checked against `phase2/sources/measure-ff-ordinance-transcription.md`) | BMC 7.11.020(C), PDF p.8 | 8 | Tax proceeds shall be allocated approximately as follows: 1) 60% for streets and sidewalks, of which roughly three quarters (45%) will be for streets and one quarter (15%) will be for sidewalks and pedestrian paths, until the backlog of damaged sidewalks and pedestrian paths is eliminated. 2) 30% for safety improvements. 3) The remaining 10% shall include environmental enhancements | quote found on cited page |
| [ ] | Council may not alter the Measure FF allocation without voters | (text) | Measure FF (SAFE STREETS) initiative text, BMC Chapter 7.11 (Council agenda July 9, 2024, Item 22) (`phase2/sources/measure-ff-initiative-council-2024-07-09.pdf`; quotes checked against `phase2/sources/measure-ff-ordinance-transcription.md`) | Section 7(a)(3), PDF p.15 | 15 | Alter the allocations of Section 7.11.020 | quote found on cited page |
| [ ] | Maintenance of effort | (text) | Measure FF (SAFE STREETS) initiative text, BMC Chapter 7.11 (Council agenda July 9, 2024, Item 22) (`phase2/sources/measure-ff-initiative-council-2024-07-09.pdf`; quotes checked against `phase2/sources/measure-ff-ordinance-transcription.md`) | BMC 7.11.030(B), PDF p.8 | 8 | the City Council shall not be authorized to impose the special tax for the following two years | quote found on cited page |
| [ ] | Five-year Measure FF program | $92,282,816 | Five-Year Street Rehabilitation and Measure FF Plans FY2027-2031, Council Item 10, July 7, 2026 (`phase2/sources/street-rehab-measure-ff-2026-07-07.pdf`) | p.4 (Table 1C; BeTH sum of the printed category totals) | 4 |  | matches data record |
| [ ] | Measure FF street rehabilitation, FY2027-FY2031 | $42,119,935 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | p.215 | 215 |  | matches data record; value printed on cited page |
| [ ] | FY2027 Measure FF revenue | $16,651,651 | FY2027 Tax Rate: SAFE STREETS (Measure FF), Council Consent Item 15, June 16, 2026 (`phase2/sources/measure-ff-fy2027-tax-rate-2026-06-16.pdf`) | p.1 | 1 | is projected to yield $16,651,651 in revenues | matches data record; value printed in the quoted passage; quote found on cited page |

### Unresolved legal or accounting interpretation

- [ ] How far "approximately" 45% allows the streets share to vary, and who decides.
- [ ] Whether the percentages apply year by year, over the five-year program, or over the 14-year life of the tax.
- [ ] Whether the "streets" share (repair, repaving and reconstruction) is the same as the CIP "street rehabilitation" line, or also covers street work budgeted under the safety or environmental shares.
- [ ] How the unprogrammed $1,351,651 FY2027 revenue increase and unappropriated FY2026 collections may be used.
- [ ] 7.11.020(D) releases the allocations at PCI 70 but cross-references 7.11.030(C), which concerns external funding; it is probably a drafting error, and its effect is not settled.
- [ ] No City Attorney opinion or Council interpretation of these provisions is in BeTH's sources.
- [ ] The ordinance is a scanned document; quotes are checked against BeTH's transcription, not the page images. The transcription of PDF pp.8 and 15 must be checked against the scans.
- [ ] The adopted program total ($92,282,816) is BeTH's sum of the printed Table 1C category totals; the table prints no single grand total.

### Missing evidence

- City Attorney opinion or Council interpretation of "approximately" and of the period over which the 7.11.020(C) shares apply
- June 30, 2026 Measure FF balance (the first rate covered 18 months of collections) (would be in: FY2026 ACFR (expected early 2027))
- Programming of the $1,351,651 FY2027 revenue increase adopted in Exhibit C (would be in: FY2027 Annual Appropriation Ordinance amendments)

### Independent human approval

Recorded in `phase2/review/human-approvals.json` → `answers.measure-ff-paving`. Current status: **NOT APPROVED**.

| Field | Entry |
|---|---|
| Reviewer |  |
| Date |  |
| Decision | NOT APPROVED |
| Changes required |  |
| Notes |  |

---

## How bad are Berkeley's streets, beyond the average PCI?

Page: `phase2/docs/ask/street-condition.html` · Automated checks: passed · Human source verification: **NOT PERFORMED** · Approval: **NOT APPROVED**

### Central claim

> The average hides most of it. In the 2024 inspection the network averaged PCI 56, but 88.5 centerline miles (42% of the network) were below PCI 50 and 33.9 miles were below 25. The City projects an average of about 62 by 2038 with Measure FF, but publishes no projection of how many streets will still be below 50. The adopted plans treat 22.6 miles of currently-below-50 streets over five years.

BeTH's reading (High): Reaching a network average of 60 or 62 is not the same as eliminating failed streets; the measure that matches Measure FF's goal is the mileage below PCI 50.

Counterargument: Treating the worst streets first costs more per point of average PCI (the City shows about one point lower in 2038), so a lower failed-street count can mean a lower average; both measures are needed.

### Calculations

- [ ] **Share of centerline miles below PCI 50**: 88.466 mi ÷ 212.778 mi = **41.58%** (`pave:network/2024/miles-below-50 ÷ pave:network/2024/centerline-miles`)

Tick a calculation only if its method is the right one for the claim, not only if the arithmetic is correct.

### Sources

| Page supports claim? | Fact | Value | Document (local file) | Cited | PDF page(s) | Quote | Automated check |
|---|---|---|---|---|---|---|---|
| [ ] | Network average PCI (2024 inspection) | 56 | City of Berkeley 2024 Pavement Management Program Update (P-TAP 25), April 2025 (`phase2/sources/pavement-management-update-ptap25-2025-04.pdf`) | Executive Summary p.2, PDF p.5 | 5 | The updated Pavement Management Program showed that the City's overall average PCI is 56. | value printed in the quoted passage; quote found on cited page |
| [ ] | Share of pavement area in Poor to Failed condition (PTAP categories, PCI 50 and below) | 41.93% | City of Berkeley 2024 Pavement Management Program Update (P-TAP 25), April 2025 (`phase2/sources/pavement-management-update-ptap25-2025-04.pdf`) | Executive Summary p.4, PDF p.7 | 7 | 41.93% are in Poor to Failed condition | value printed in the quoted passage; quote found on cited page |
| [ ] | Centerline miles below PCI 50 (BeTH sum of section lengths in feet / 5,280; 1,216 sections validated to the report totals) | 88.466 mi | City of Berkeley 2024 Pavement Management Program Update (P-TAP 25), April 2025 (`phase2/sources/pavement-management-update-ptap25-2025-04.pdf`) | Section IV, Street Sections Alphabetical, PDF pp.40-67 | 40-67 |  | matches data record |
| [ ] | Centerline miles below PCI 25 | 33.903 mi | City of Berkeley 2024 Pavement Management Program Update (P-TAP 25), April 2025 (`phase2/sources/pavement-management-update-ptap25-2025-04.pdf`) | Section IV, Street Sections Alphabetical, PDF pp.40-67 | 40-67 |  | matches data record |
| [ ] | Network centerline miles (sum of section lengths in feet / 5,280) | 212.778 mi | City of Berkeley 2024 Pavement Management Program Update (P-TAP 25), April 2025 (`phase2/sources/pavement-management-update-ptap25-2025-04.pdf`) | Section IV, PDF pp.40-67; printed total 212.77, Executive Summary p.2, PDF p.5 | 40-67 |  | matches data record |
| [ ] | Currently-below-50 miles treated by both adopted plans, FY2027-FY2031 (sum of printed section miles) | 22.610 mi | Five-Year Street Rehabilitation and Measure FF Plans FY2027-2031, Council Item 10, July 7, 2026 (`phase2/sources/street-rehab-measure-ff-2026-07-07.pdf`) | Attachments, pp.21-62 | 21-62 |  | matches data record |
| [ ] | City projection, Five-Year Plan + Measure FF, 2038 | 62 | Five-Year Street Rehabilitation and Measure FF Plans FY2027-2031, Council Item 10, July 7, 2026 (`phase2/sources/street-rehab-measure-ff-2026-07-07.pdf`) | p.12 | 12 | the citywide PCI is projected to improve to approximately 62 by 2038 | value printed in the quoted passage; quote found on cited page |
| [ ] | Measure FF goal | (text) | Measure FF (SAFE STREETS) initiative text, BMC Chapter 7.11 (Council agenda July 9, 2024, Item 22) (`phase2/sources/measure-ff-initiative-council-2024-07-09.pdf`; quotes checked against `phase2/sources/measure-ff-ordinance-transcription.md`) | BMC 7.11.010(K)(1), PDF p.7 | 7 | ideally with no streets having a PCI below 50 | quote found on cited page |

### Unresolved legal or accounting interpretation

- [ ] Two different measures appear side by side and must not be read as one: the City's 41.93% is pavement AREA in the consultant's Poor and Failed categories (PCI 50 and below); BeTH's 88.5 miles is centerline LENGTH with PCI below 50.
- [ ] Mileage is BeTH's sum of section lengths in feet; summing the report's rounded section miles gives 88.75. Whether 0.1-mile precision is appropriate for publication.
- [ ] One uninspected Tevlin St section (PCI 0, no inspection date) is excluded, following the report's totals table; the report's category table counts it as Failed.
- [ ] The condition data are from 2024 inspections, before FY2025-FY2026 paving.
- [ ] Plan PCIs are the values printed at planning time; streets will be lower when treated. The 22.6 miles are sections currently below 50 that the plans list, not miles that will end above 50.

### Missing evidence

- Projected miles below PCI 50 under each funding scenario (would be in: StreetSaver output; the Measure FF annual report must include "the PCI of all streets" (BMC 7.11.050(B)(1)))
- Condition after FY2025-FY2026 paving (would be in: next StreetSaver inspection update)

### Independent human approval

Recorded in `phase2/review/human-approvals.json` → `answers.street-condition`. Current status: **NOT APPROVED**.

| Field | Entry |
|---|---|
| Reviewer |  |
| Date |  |
| Decision | NOT APPROVED |
| Changes required |  |
| Notes |  |

---

## What does the $139.3 million streets figure include?

Page: `phase2/docs/ask/streets-139m.html` · Automated checks: passed · Human source verification: **NOT PERFORMED** · Approval: **NOT APPROVED**

### Central claim

> It is the five-year (FY2027-FY2031) Streets capital budget, not a two-year one: the paving plan ($96,336,212), Measure FF street rehabilitation ($42,119,935), bridge maintenance and Harold Way placemaking add to exactly $139,356,147. The two-year FY2027-FY2028 Streets amount is $58,211,462.

BeTH's reading (High): Comparisons that treat $139,356,147 as a biennial figure overstate two-year street spending by more than double. (The figure in the question is slightly low: the exact amount rounds to $139.4 million.)

Counterargument: FY2029-FY2031 are planned amounts and may change; the two-year figure is the only one with appropriations behind it.

### Calculations

- [ ] **Sum of the four Streets projects**: $96,336,212 + $42,119,935 + $750,000 + $150,000 = **$139,356,147** (`cip:streets/five-year/street-rehab-plan + cip:streets/five-year/measure-ff + cip:streets/five-year/bridge + cip:streets/five-year/harold-way`)
- [ ] **Two-year (FY2027 + FY2028) Streets amount**: $32,241,345 + $25,970,117 = **$58,211,462** (`cip:streets/fy2027 + cip:streets/fy2028`)

Tick a calculation only if its method is the right one for the claim, not only if the arithmetic is correct.

### Sources

| Page supports claim? | Fact | Value | Document (local file) | Cited | PDF page(s) | Quote | Automated check |
|---|---|---|---|---|---|---|---|
| [ ] | Five-Year Street Rehabilitation Plan (Exhibit B lines) | $96,336,212 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | pp.215-216 (sum of the Street Rehab lines) | 215-216 |  | matches data record |
| [ ] | Measure FF Street Rehabilitation | $42,119,935 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | p.215 | 215 |  | matches data record; value printed on cited page |
| [ ] | Bridge Preventive Maintenance | $750,000 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | p.215 | 215 |  | matches data record; value printed on cited page |
| [ ] | Harold Way Placemaking | $150,000 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | p.215 | 215 |  | matches data record; value printed on cited page |
| [ ] | Printed Streets five-year budget | $139,356,147 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | p.216 | 216 | $139,356,147 in Five-Year CIP Budget | matches data record; value printed in the quoted passage; quote found on cited page |
| [ ] | Streets, FY2027 | $32,241,345 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | p.169 (category table); also p.216 | 169 |  | matches data record; value printed on cited page |
| [ ] | Streets, FY2028 | $25,970,117 | Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026 (`phase2/sources/budget-adoption-2026-06-23.pdf`) | p.169 (category table); also p.216 | 169 |  | matches data record; value printed on cited page |
| [ ] | Street plan five-year total | $96,336,212 | Five-Year Street Rehabilitation and Measure FF Plans FY2027-2031, Council Item 10, July 7, 2026 (`phase2/sources/street-rehab-measure-ff-2026-07-07.pdf`) | p.3 (Table 1B) | 3 |  | value printed on cited page |

### Unresolved legal or accounting interpretation

- [ ] The origin of the "$139.3 million" figure in the question is not identified in BeTH's sources; the street plan says "over $139 million".
- [ ] FY2029-FY2031 amounts are planned, not appropriated.
- [ ] The Mayor's recommendations adopted with the budget (Exhibit D) add $2.9M of one-time SOSIP money in FY2027, including $2.5M for Oxford for All, outside the Exhibit B Streets table. Whether a resident's "streets figure" should include it.
- [ ] Dais amendments of June 23, 2026 and the FY2027 Annual Appropriation Ordinance are not in BeTH's sources.

### Missing evidence

- FY2027 Annual Appropriation Ordinance (controlling record, incl. any June 23 amendments)

### Independent human approval

Recorded in `phase2/review/human-approvals.json` → `answers.streets-139m`. Current status: **NOT APPROVED**.

| Field | Entry |
|---|---|
| Reviewer |  |
| Date |  |
| Decision | NOT APPROVED |
| Changes required |  |
| Notes |  |


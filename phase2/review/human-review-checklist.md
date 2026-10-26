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

BeTH's reading (Moderate): For scale, the two figures measure different things. The City estimates that reaching an average PCI of 70 would take about $8 million a year of additional spending beyond its modeled Plan + Measure FF scenario. Fund 501's non-paving capital is $1,473,000 a year of budgeted projects, mostly repairs to existing City buildings, that could be freed only by deferring them; it is not available cash. Redirecting it would not close the modeled gap.

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

- [ ] BeTH has not assessed what it would cost to delay the roof, building, pool, sidewalk and other repairs that fund 501 pays for, including legal, contract and safety consequences.
- [ ] Public records do not show how much of the FY2027-FY2028 budget for these projects is already under contract or spent. The ceilings are budget amounts, not cash known to be available.
- [ ] The $11,568,647 one-time ceiling is from June 30, 2025, sixteen months ago, and already backs projects carried forward from earlier years. How much of it is still uncommitted is unknown.
- [ ] For Measure FF, BeTH gives no dollar amount because the legal questions on the Measure FF page are unresolved.
- [ ] Measure FF requires the City to keep spending a minimum amount of other money on street maintenance. BeTH estimated that minimum because the City has not published its own calculation, and the ordinance does not state the base year or inflation index. The minimum limits moving paving money out of streets, not into them.
- [ ] Changes Council made at the June 23, 2026 meeting are not in the budget document BeTH used. The FY2027 Annual Appropriation Ordinance, the controlling record, is not in BeTH's sources.

### Missing evidence

- FY2026 year-end fund 501 carryover and encumbrance detail by project.
- The FY2027 Annual Appropriation Ordinance (controlling appropriation record, incl. any June 23 amendments).
- Public Works and Parks assessments of what deferring each fund 501 project would cost (condition, safety, legal, contracts).
- The City's Measure FF maintenance-of-effort calculation and whether FY2027 draws on the Stabilization Reserve.
- Restriction research for the other CIP funding sources.
- A City Attorney opinion or Council interpretation of the Measure FF allocation (BMC 7.11.020(C)) as it applies to added paving.

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

- [ ] How much room the word "approximately" in "approximately 45%" allows, and who decides.
- [ ] Whether the percentages must be met every year, over the five-year plan, or over the 14-year life of the tax.
- [ ] Whether the ordinance's "streets" share means the same thing as the budget's "street rehabilitation" line, or also covers street work paid for from the safety or environmental shares.
- [ ] How the City may use FY2027 revenue that came in above the adopted plan, and FY2026 collections not yet budgeted. Neither has been assigned in the documents BeTH holds.
- [ ] The ordinance says the percentage rules end when the citywide average PCI reaches 70, but the sentence that says so points to the wrong subsection (7.11.020(D) refers to 7.11.030(C)). This is probably a drafting error, and its effect is not settled.
- [ ] No City Attorney opinion or Council interpretation of these provisions is in BeTH's sources.
- [ ] The ordinance is a scanned document. BeTH checked quotes against its own transcription, which a reviewer must compare with the scanned pages (PDF pages 8 and 15).
- [ ] The five-year Measure FF total is BeTH's sum of the category totals in the City's table; the table prints no single grand total.

### Missing evidence

- City Attorney opinion or Council interpretation of "approximately" and of the period over which the 7.11.020(C) shares apply.
- June 30, 2026 Measure FF balance (the first rate covered 18 months of collections). (would be in: FY2026 ACFR (expected early 2027))
- Programming of the $1,351,651 FY2027 revenue increase adopted in Exhibit C. (would be in: FY2027 Annual Appropriation Ordinance amendments)

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

- [ ] The City's 41.93% and BeTH's 88.5 miles measure different things. The City's figure is pavement area rated "poor" or "failed" (PCI 50 and below); BeTH's figure is street length below PCI 50.
- [ ] BeTH measured length from each section's length in feet. Adding up the report's rounded mileage figures instead gives slightly more. Figures are shown to a tenth of a mile.
- [ ] One short section of Tevlin Street was not inspected and has no score. BeTH leaves it out, as the report's totals do; the report's condition table counts it as failed.
- [ ] The data are from 2024 inspections, before the City's FY2025-FY2026 paving.
- [ ] Street scores in the City's plans are the scores when the plans were written; streets will be in worse condition by the time they are repaved. The 22.6 miles are streets now below 50 that the plans list for work.

### Missing evidence

- Projected miles below PCI 50 under each funding scenario. (would be in: StreetSaver output; the Measure FF annual report must include "the PCI of all streets" (BMC 7.11.050(B)(1)))
- Condition after FY2025-FY2026 paving. (would be in: next StreetSaver inspection update)

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

- [ ] BeTH has not found the source of the figure in the question. The exact five-year amount rounds to $139.4 million, and the City's street plan describes it as "over $139 million".
- [ ] The last three years, FY2029-FY2031, are plans, not approved spending.
- [ ] Some one-time money added with the Mayor's budget recommendations, including funding for Oxford for All, is outside the Streets table. Whether it belongs in a "streets figure" is a judgment call.
- [ ] Changes Council made at the June 23, 2026 meeting, and the FY2027 Annual Appropriation Ordinance, are not in BeTH's sources.

### Missing evidence

- FY2027 Annual Appropriation Ordinance (controlling record, incl. any June 23 amendments).

### Independent human approval

Recorded in `phase2/review/human-approvals.json` → `answers.streets-139m`. Current status: **NOT APPROVED**.

| Field | Entry |
|---|---|
| Reviewer |  |
| Date |  |
| Decision | NOT APPROVED |
| Changes required |  |
| Notes |  |

---

## Is Berkeley's Marina paying for itself?

Page: `phase2/docs/ask/marina.html` · Automated checks: passed · Human source verification: **NOT PERFORMED** · Approval: **NOT APPROVED**

### Central claim

> The Marina Fund (fund 608) is meant to pay for the whole waterfront from berth fees and leases. In audited FY2024 it had an operating loss of $401,892; in audited FY2025, $5,979,084, a year distorted by State-funded dock work. Staff's unaudited FY2026 figures show revenue of $8,673,012 against expenditures of $8,395,420, but the revenue includes about $1.4 million of General Fund subsidy. Staff project losses of $1,023,955 in FY2027 and $1,045,594 in FY2028, leaving the fund $545,586 in deficit. The DoubleTree hotel owed about $1 million in rent in October 2026.

**Does the Marina cover its costs?** Not consistently. In audited FY2024, operating expenses exceeded operating revenue by $401,892. Audited FY2025 shows a much larger operating loss, $5,979,084, in a year the fund also received a $7,689,069 State capital grant for dock work; the statements do not show how much of the year's expense that work accounts for. Staff's unaudited FY2026 figures balance only because revenue includes about $1.4 million of General Fund subsidy; without it the shortfall is about $1,122,408.

**If not, who pays the difference?** Other City money, in several different forms: federal pandemic aid in FY2022 ($1.4 million) and FY2023 ($1.15 million); cost shifts to other funds ($800,000 in FY2024); reduced City overhead charges and Workers' Compensation "holidays" ($850,000 in FY2025, $360,000 in FY2026); a General Fund transfer of about $1.4 million in FY2026; and a $2,477,099 loan from the General Fund, still owed at June 30, 2025. Since FY2026 the Parks Tax pays $1.579 million a year of waterfront park and landscape costs. Staff told the committee there is no General Fund money for FY2027-FY2028.

**What would it take to make the waterfront financially sustainable?** Staff estimate at least $1.2 million of cuts, cost shifts or new revenue just to reach FY2028 with a small reserve, before any capital work. Separately, the waterfront has $163,344,000 of unfunded infrastructure needs, and the City's update names no funding source for them. When the fund was set up in 1964, berth fees and hotel and restaurant leases were expected to pay for the whole waterfront; how much of its public parks, paths and services boaters and tenants should carry, and how much the wider city should, is a policy choice, not an accounting fact.

BeTH's reading (Moderate): At current fees, leases and service levels the Marina Fund does not pay for the waterfront it runs; one-time help and support from other City funds have covered the gap since FY2022.

Counterargument: Much of the waterfront is public parkland, paths, restrooms, security and recreation used by everyone, not only boaters. A 2023 State review, cited by the Berkeley Decision Project and not yet verified by BeTH, estimated that boating revenue roughly covered boating costs. On that view the question is how the public parts of the waterfront should be funded, not whether boaters underpay.

BeTH's reading (Moderate): Unpaid DoubleTree rent is the largest near-term risk to the fund: it is the largest single tenant and the budget counts on partial payment that has not arrived.

Counterargument: The rent is still owed, not written off, and the hotel cleared an earlier balance in September 2025. If it pays again, the projected deficit shrinks; if it does not, the loss is larger than the budget assumed.

### Calculations

- [ ] **FY2024 operating loss (audited): operating expenses minus operating revenue**: $7,326,968 − $6,925,076 = **$401,892** (`acfr24:608/operating-expenses − acfr24:608/operating-revenue`)
- [ ] **FY2025 operating loss (audited): operating expenses minus operating revenue**: $13,573,896 − $7,594,812 = **$5,979,084** (`acfr25:608/operating-expenses − acfr25:608/operating-revenue`). Includes $594,125 of depreciation, which is not cash, and an unknown share of dock work paid for by the State capital grant recorded below the operating line.
- [ ] **FY2026 revenue without the General Fund subsidy (unaudited)**: $8,673,012 − $1,400,000 = **$7,273,012** (`bf26:fy2026/revenue − bf26:fy2026/gf-subsidy`). Approximate: the subsidy is stated only as "$1.4M".
- [ ] **FY2026 shortfall before the General Fund subsidy (unaudited)**: $8,395,420 − $7,273,012 = **$1,122,408** (`bf26:fy2026/expenditures − c3`)
- [ ] **FY2027 projected operating loss**: $7,388,315 − $6,364,360 = **$1,023,955** (`bf26:fy2027/expenditures − bf26:fy2027/revenue`)
- [ ] **FY2028 projected operating loss**: $7,580,393 − $6,534,799 = **$1,045,594** (`bf26:fy2028/expenditures − bf26:fy2028/revenue`)

Tick a calculation only if its method is the right one for the claim, not only if the arithmetic is correct.

### Sources

| Page supports claim? | Fact | Value | Document (local file) | Cited | PDF page(s) | Quote | Automated check |
|---|---|---|---|---|---|---|---|
| [ ] | FY2024 operating revenue | $6,925,076 | Annual Comprehensive Financial Report, FY ended June 30, 2024 (`staging/fy2024/source/annual-comprehensive-financial-report-fy2024.pdf`) | PDF p.87 (Marina Operations column) | 87 |  | value printed on cited page |
| [ ] | FY2024 operating expenses | $7,326,968 | Annual Comprehensive Financial Report, FY ended June 30, 2024 (`staging/fy2024/source/annual-comprehensive-financial-report-fy2024.pdf`) | PDF p.87 | 87 |  | value printed on cited page |
| [ ] | FY2025 operating revenue | $7,594,812 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.85 (Marina Operations column) | 85 |  | value printed on cited page |
| [ ] | FY2025 "Marina operations and maintenance" revenue (berths and other marina charges; the ACFR does not break this line down) | $5,329,258 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.85, line "Marina operations and maintenance" | 85 |  | value printed on cited page |
| [ ] | FY2025 lease revenue (hotel, restaurants and other tenants) | $2,265,554 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.85, line "Lease revenues" | 85 |  | value printed on cited page |
| [ ] | FY2025 operating expenses | $13,573,896 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.85 | 85 |  | value printed on cited page |
| [ ] | Of which depreciation (not cash) | $594,125 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.85 | 85 |  | value printed on cited page |
| [ ] | FY2025 State capital grant (recorded outside operating revenue) | $7,689,069 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.85, nonoperating "Capital grants - State" | 85 |  | value printed on cited page |
| [ ] | FY2025 loan received from another City fund (financing, not revenue) | $2,477,099 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.87, cash flow "Receipt from interfund loans" | 87 |  | value printed on cited page |
| [ ] | Owed by the Marina Fund to the General Fund, June 30, 2025 | $2,477,099 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.113, Note 4.A Due To/From Other Funds | 113 |  | value printed on cited page |
| [ ] | What the audit says about such balances | (text) | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.113, Note 4.A | 113 | expected to be repaid within the next fiscal year | quote found on cited page |
| [ ] | State boating loan still owed, June 30, 2025 | $5,415,120 | Annual Comprehensive Financial Report, FY ended June 30, 2025 (`annual-comprehensive-financial-report-fy2025.pdf`) | PDF p.133, Harbor Construction 5 note payable | 133 |  | value printed on cited page |
| [ ] | Council authorization: internal loan from the Workers' Compensation Fund for D and E dock replacement (July 25, 2023) | $5,500,000 | $5.5M Loan for D and E Dock Replacement Project, Council Item 19, July 25, 2023 (revised staff report) (`phase2/sources/council-2023-07-25-item19-wc-loan.pdf`) | p.1 | 1 | authorizes an internal loan of $5.5M from the Workers Compensation Fund | value printed in the quoted passage; quote found on cited page |
| [ ] | FY2024 transfer out of the Workers' Compensation Fund | $5,500,000 | Annual Comprehensive Financial Report, FY ended June 30, 2024 (`staging/fy2024/source/annual-comprehensive-financial-report-fy2024.pdf`) | PDF p.312, internal service funds statement, Workers' Compensation column | 312 |  | value printed on cited page |
| [ ] | FY2024 transfer note: $5,500,000 to the General Fund, purpose "Worker's Compensation Fund" | $5,500,000 | Annual Comprehensive Financial Report, FY ended June 30, 2024 (`staging/fy2024/source/annual-comprehensive-financial-report-fy2024.pdf`) | PDF p.115, Note 4.B Transfers | 115 |  | value printed on cited page |
| [ ] | FY2026 revenue, staff "actual" (unaudited) | $8,673,012 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 |  | value printed on cited page |
| [ ] | FY2026 lease revenue (unaudited) | $2,164,222 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 |  | value printed on cited page |
| [ ] | FY2026 berth revenue (unaudited) | $3,971,848 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 |  | value printed on cited page |
| [ ] | FY2026 other revenue, including the General Fund subsidy (unaudited) | $2,536,941 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 |  | value printed on cited page |
| [ ] | FY2026 General Fund subsidy included in revenue (as stated, rounded) | $1,400,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 | Includes $1.4M in General Fund subsidy to the Marina Fund. | value printed in the quoted passage; quote found on cited page |
| [ ] | FY2026 expenditures, staff "actual" (unaudited) | $8,395,420 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 |  | value printed on cited page |
| [ ] | FY2027 revenue, projected | $6,364,360 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 |  | value printed on cited page |
| [ ] | FY2027 expenditures, projected | $7,388,315 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 |  | value printed on cited page |
| [ ] | FY2028 revenue, projected | $6,534,799 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 |  | value printed on cited page |
| [ ] | FY2028 expenditures, projected | $7,580,393 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 |  | value printed on cited page |
| [ ] | FY2028 ending fund balance, projected: a deficit of | $545,586 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 14 | 14 |  | value printed on cited page |
| [ ] | FY2022 federal pandemic aid (ARPA) | $1,400,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 6 | 6 | FY22: $1.4M in American Rescue Plan Act (ARPA) funds | value printed in the quoted passage; quote found on cited page |
| [ ] | FY2023 federal pandemic aid (ARPA) | $1,150,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 6 | 6 | FY23: $1.15M in ARPA funds | value printed in the quoted passage; quote found on cited page |
| [ ] | FY2024 cost shifts to other funds | $800,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 6 | 6 | FY24: $800k in cost shifts to other funds | value printed in the quoted passage; quote found on cited page |
| [ ] | FY2024 Workers' Compensation Fund money "for capital projects" (staff description) | $5,500,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 6 | 6 | $5.5M from Workers Compensation Fund for capital projects | value printed in the quoted passage; quote found on cited page |
| [ ] | FY2025 reduced City overhead charges and Workers' Compensation holiday | $850,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 6 | 6 | FY25: $850k in reduced indirect costs and Workers Compensation Fund holiday | value printed in the quoted passage; quote found on cited page |
| [ ] | FY2026 General Fund transfer (as stated, rounded) | $1,400,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 6 | 6 | FY26: $1.4M in General Fund transfer | value printed in the quoted passage; quote found on cited page |
| [ ] | FY2026 reduced overhead charges and Workers' Compensation holiday | $360,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 6 | 6 | $360k in reduced indirect costs and Workers Compensation holiday | value printed in the quoted passage; quote found on cited page |
| [ ] | Waterfront park and landscape costs moved to the Parks Tax each year from FY2026 | $1,579,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 6 | 6 | Shifts $1.579M in Waterfront park and landscape costs from Marina Fund to Parks Tax. | value printed in the quoted passage; quote found on cited page |
| [ ] | What the fund was set up to do (1964) | (text) | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 3 | 3 | Revenue from slips and hotel/restaurant leases was expected to cover the costs of debt service, maintenance and operations of the entire Waterfront. | quote found on cited page |
| [ ] | General Fund support in FY2027-28 | (text) | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 12 | 12 | No General Fund available to support the Marina Fund | quote found on cited page |
| [ ] | DoubleTree payment that cleared an earlier balance, September 2025 | $964,680 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 9 | 9 | Hotel paid their full balance in Sept 2025: $964,680. | value printed in the quoted passage; quote found on cited page |
| [ ] | DoubleTree payments since | (text) | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 9 | 9 | No rent has been paid to the City since Dec 2025. | quote found on cited page |
| [ ] | DoubleTree rent owed, October 2026 (approximate) | $1,000,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 9 | 9 | Hotel currently owes approx. $1M (10 months of base rent, 4 quarters of % rent). | value printed in the quoted passage; quote found on cited page |
| [ ] | DoubleTree rent counted on in the FY2027-28 budget | $840,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 9 | 9 | Marina Fund FY27-28 budget included $840k in projected revenue (approx. 30% of required rent) | value printed in the quoted passage; quote found on cited page |
| [ ] | DoubleTree rent owed, September 2026 (approximate) | $890,000 | Berkeley Waterfront Overview, Parks, Recreation and Waterfront Commission, September 9, 2026 (supplemental packet) (`phase2/sources/prw-commission-waterfront-overview-2026-09-09.pdf`) | p.11 | 11 | currently owes approx. $890k | value printed in the quoted passage; quote found on cited page |
| [ ] | Budget assumption stated elsewhere in the September packet | (text) | Berkeley Waterfront Overview, Parks, Recreation and Waterfront Commission, September 9, 2026 (supplemental packet) (`phase2/sources/prw-commission-waterfront-overview-2026-09-09.pdf`) | p.15 | 15 | FY27 and FY28 Marina Fund budget assumed Doubletree would pay at least 35% of rent. | quote found on cited page |
| [ ] | Staff estimate of cuts, cost shifts or new revenue needed through FY2028 | $1,200,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 15 | 15 | Results in $1.2M+ needed in reductions, cost shifts or new revenue | value printed in the quoted passage; quote found on cited page |
| [ ] | Unfunded waterfront infrastructure needs (City estimate) | $163,344,000 | Berkeley Waterfront: Marina Fund Update, Budget & Finance Committee Item 2, October 22, 2026 (presentation) (`phase2/sources/bf-committee-marina-fund-update-2026-10-22.pdf`) | slide 8 | 8 |  | value printed on cited page |

### Unresolved legal or accounting interpretation

- [ ] The FY2025 operating loss includes depreciation, which is not cash, and an unknown amount of dock and pile work paid for by the State capital grant. FY2025 is therefore not a clean measure of day-to-day operations.
- [ ] The $2,477,099 owed to the General Fund at June 30, 2025 was "expected to be repaid within the next fiscal year". Whether it was repaid, and whether it is connected to the $5.5 million authorization, is not shown in any document BeTH holds.
- [ ] The FY2024 audit shows $5,500,000 leaving the Workers' Compensation Fund and going to the General Fund. The Marina Fund recorded no transfer in and owed nothing to another fund at June 30, 2024. The audit's transfer note lists the row under the Equipment Replacement Fund while its fund statement shows the money leaving Workers' Compensation, an inconsistency inside the audit report itself. Whether waterfront hotel tax has been used to repay the loan, as the 2023 authorization intended, is not shown.
- [ ] City documents give different amounts for General Fund support in FY2026. BeTH has not reconciled them to one adopted figure.
- [ ] The audited FY2025 line "Marina operations and maintenance" ($5,329,258) and staff's FY2026 "Berthers" ($3,971,848) measure different things; what the audited line includes beyond berth rent is not stated.
- [ ] Staff's FY2026 revenue components add to one dollar less than the stated total. The difference is in the City's table and is recorded, not corrected.
- [ ] DoubleTree arrears: about $890,000 in September 2026 (nine months of base rent, three quarters of percentage rent) and about $1 million in October 2026 (ten months, four quarters). Staff counted on $840,000 of DoubleTree rent over FY2027-FY2028, described as approximately 30% of rent; the September packet also describes the assumption as at least 35%. Whether the City has recorded an allowance for doubtful accounts or started lease enforcement is not established.
- [ ] Costs caused by boating and costs of public waterfront services are not separated in any audited statement. The only estimate BeTH knows of is a 2023 State report, cited by a third party and not yet obtained by BeTH.
- [ ] Staff expenditure totals and audited operating expenses are measured differently (for example, staff figures are on a budget basis and audited figures include depreciation), so audited and staff years are not directly comparable.
- [ ] The State boating loan balance ($5,415,120 at June 30, 2025) is still being repaid from the Marina Fund.

### Missing evidence

- The FY2026 audited financial report, including whether the General Fund loan was repaid.
- What the audited "Marina operations and maintenance" revenue line includes.
- Waterfront hotel-tax collections and any repayments to the Workers' Compensation Fund since FY2025.
- The DoubleTree receivable as booked, any allowance for doubtful accounts, and lease-enforcement status.
- The June 2023 State Division of Boating and Waterways report (Attachment 4 to the July 25, 2023 Council item), the primary source for any boating and non-boating cost split.
- A funding plan for the waterfront's unfunded infrastructure needs.

### Independent human approval

Recorded in `phase2/review/human-approvals.json` → `answers.marina`. Current status: **NOT APPROVED**.

| Field | Entry |
|---|---|
| Reviewer |  |
| Date |  |
| Decision | NOT APPROVED |
| Changes required |  |
| Notes |  |


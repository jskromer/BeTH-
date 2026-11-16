# Street-purpose spending as reported to the State Controller, FY2010–FY2025, and four reconciliations

**Status: DRAFT · NOT APPROVED.** Pending independent source review. Nothing here changes an approved ledger, an Ask BeTH answer or an existing finding. Prepared 2026-10-26 on branch `phase2-capital-analysis`; not merged, not deployed.

**Machine-checked.** Every page citation below is in `phase2/history/tools/streets_actuals.py` and is checked by `build_history.py` (the quoted text must appear on the cited PDF page). Arithmetic is recomputed by the builder and by `phase2/tests/test_history.py` (class `StreetActuals`).

Data: `phase2/history/data/street-expenditures-actual.json` and `.csv`.

---

## Bottom line

1. **There is a consistent series of actual street spending, but it is not a paving ledger.** The City reports its street-purpose spending every year to the State Controller under Streets and Highways Code §2151. BeTH has the Berkeley figures for FY2010–FY2025. The capital category "Street Reconstruction" is the best available measure of paving construction:
   - FY2010–FY2017: about $3.1M a year on average.
   - FY2018–FY2025: about $13.8M a year.
   - FY2024: $22.5M. FY2025: $21.7M.

   The Controller does not audit these figures. They include safety and complete-streets work that the City classed as reconstruction, and they have never been reconciled to the City's audited statements. **Confidence:** High that the figures are what the City filed; Moderate as a measure of paving.
2. **The records collected so far do not provide a reconciled project-level paving ledger.** The ACFRs do not break out street spending, and the budget books show appropriations. The State Controller data supplies the actual series used here, with project codes in some detail rows. A project-level accounting ledger and code crosswalk are sought in item 1 of the records request draft. Other public actual-spending records may exist; the source search is incomplete.
3. **A. The 2022 "$7.3 million General Fund" baseline was not General Fund money.** It was the whole recurring paving program: gas tax, SB 1, Measure BB, Measure F and the $1,925,000 Capital Improvement Fund line. The resolution as adopted calls it the "existing baseline $7.3 million allocation". **Confidence:** High.
4. **B. Council authorized $9.55M from Workers' Compensation in two actions in 2023. The audited statements record one $5.5M transfer out, in FY2024, to the General Fund.**
   - No advance or receivable was recorded for either action.
   - The $4.05M for Measure T1 does not appear in any audited Workers' Compensation statement for FY2023–FY2025.
   - Which authorization the $5.5M carried out is not established.

   **Confidence:** High on what the statements show; Unknown on what happened to the $4.05M.
5. **C. Whether Zero Waste and Storm Water money counts toward the $15.3M Measure FF requirement is unresolved.**
   - The ordinance's own definition, through Res. 70,456, built the $15.3M from sources that included neither fund.
   - The ordinance text does not exclude them.
   - BeTH found no City calculation of the requirement.

   **Confidence:** High on the documents; this is a legal question that BeTH does not answer.
6. **D. The $994,086 FY2027 difference can be reproduced from different FY2025 bases.** The November 2023 plan's series fits $8,937,022 (FY2025) escalated at 3% a year, reaching $9,481,286 in FY2027. The FY2026 budget and July 2026 plan's series fits $8,000,000 (FY2025) escalated at 3% a year, reaching $8,487,200 in FY2027. Both fits are within $1. This is an arithmetic reconstruction, not documentation of an administrative reset. No document BeTH holds explains the base difference or establishes that 3% implements the policy's named index. **Confidence:** High on the arithmetic; Unknown on the reason.

---

## 1. Actual street expenditures, FY2010–FY2025

### Source and basis

- **What it is.** Each year the City files an Annual Street Report with the State Controller (Streets and Highways Code §2151). The report classifies spending as:
  - Undistributed Engineering and Administration.
  - Construction, which includes Street Reconstruction, signals, bike and pedestrian work, and storm drains.
  - Maintenance, which includes Overlay and Sealing, and Patching.
  - Equipment and other categories.
- **Basis.** Actual expenditures as reported by the City. The Controller compiles the reports; it does not audit them. BeTH has not reconciled them to the ACFR, which does not report spending by these categories.
- **FY2010–FY2017.** The Controller's printed *Streets and Roads Annual Report*, Table 5 (Cities), Berkeley column.
  - One page per year is kept in `phase2/history/sources/sco/`.
  - The SHA-256 of each full report is in `sco-report-extracts.json`.
  - Every amount below is checked against its page.
- **FY2018–FY2025.** The Controller's "City Street Raw Data" workbooks, Berkeley rows. These are bythenumbers.sco.ca.gov datasets `mpy3-2iag` (FY2018–22), `g8ja-n4f6` (FY2023–24) and `b5ms-dvgv` (FY2025), saved to `sources/sco/berkeley-sco-raw.json`.
  - Fund-level and project-level detail exists only from FY2018.
  - For each year FY2018–FY2025, the Street Reconstruction detail rows sum exactly to the summary (difference $0).
- **FY2026.** Not yet published by the Controller.

### The figures (dollars, all funds)

| FY | Street Reconstruction (capital) | Overlay/sealing + patching (maint.) | Undistributed eng. & admin | All street purposes | Source |
|---|--:|--:|--:|--:|---|
| 2010 | 1,415,791 | 0 | 4,726,265 | 17,619,780 | SCO printed report p.137 |
| 2011 | 1,257,826 | 494,189 | 5,554,568 | 14,768,430 | SCO printed report p.138 |
| 2012 | 2,131,593 | 3,323,426 | 4,964,045 | 17,699,987 | SCO printed report p.141 |
| 2013 | 3,182,466 | 0 | 6,543,514 | 19,136,833 | SCO printed report p.141 |
| 2014 | 0 | 1,597,699 | 7,168,998 | 17,174,529 | SCO printed report p.142 |
| 2015 | 2,860,180 | 0 | 7,567,657 | 23,590,563 | SCO printed report p.141 |
| 2016 | 6,839,312 | 0 | 10,379,946 | 26,545,860 | SCO printed report p.140 |
| 2017 | 7,296,164 | 0 | 7,700,724 | 23,831,892 | SCO printed report p.140 |
| 2018 | 11,104,839 | Not reported | 8,141,008 | 26,546,886 | SCO raw data, SR_EXP_SUMMARY |
| 2019 | 9,411,760 | 39,796* | 7,771,928 | 21,943,061 | SCO raw data, SR_EXP_SUMMARY |
| 2020 | 17,046,786 | 68,411* | 7,937,242 | 32,794,663 | SCO raw data, SR_EXP_SUMMARY |
| 2021 | 9,880,042 | 8,100* | 7,215,517 | 25,490,937 | SCO raw data, SR_EXP_SUMMARY |
| 2022 | 13,190,165 | 75,580* | 6,994,996 | 26,107,323 | SCO raw data, SR_EXP_SUMMARY |
| 2023 | 5,558,322 | Not reported | 12,013,436 | 23,311,760 | SCO raw data, SR_EXP_SUMMARY |
| 2024 | 22,512,470 | Not reported | 9,379,238 | 35,608,054 | SCO raw data, SR_EXP_SUMMARY |
| 2025 | 21,670,883 | 2,331,787* | 6,454,881 | 37,562,669 | SCO raw data, SR_EXP_SUMMARY |

For FY2018–FY2025, the maintenance column above sums reported categories only; `*` marks a partial subtotal with one category blank. Where both are blank it displays “Not reported”. The machine-readable data preserves those blanks as `null`. A blank must not be interpreted as a reported zero.

### What each record carries (in the JSON and CSV)

Each record carries:
- Fiscal year.
- Fund. Summary rows are the City total; detail rows give the City fund number.
- Project identifier, taken from the City's description where one exists.
- Amount.
- Accounting basis.
- Capital or operating classification.
- Inclusion flags: design and administration, construction, debt service, transfers, bond proceeds, appropriations or encumbrances.
- Source: a page for FY2010–17; dataset, sheet and record number for FY2018–25.

No row counts a transfer, debt service, bond proceeds, an appropriation or an encumbrance. The builder fails if one does.

### Reconciliation rules (to prevent double counting)

1. **Never add actuals to budget or plan figures.** They are different bases. The timeline puts both on one dollar scale for comparison and says they must not be summed.
2. **Design and administration are separate.** Undistributed Engineering and Administration is not part of Street Reconstruction. Adding the two changes the measure; it is not double counting. It is excluded from the paving measure because it is not allocated to projects.
3. **Bond money counts once, when spent.** Bond-funded construction appears as expenditure in the year it is spent:
   - Measure M: fund 630, "17SG02 – Measure M Streets", $5,149,868 in FY2018.
   - Measure T1: fund 511, FY2020–FY2024.
   - Bond proceeds themselves are not in this dataset. The FY2019–20 fund 506 rows ($6.49M and $0.99M) are not identified in any document BeTH holds.
4. **Category use varies by year.**
   - FY2014: no Street Reconstruction, but $1,597,699 of Patching and $2,442,557 of Signals.
   - FY2025: $2,331,787 of Overlay and Sealing.

   Comparing one category year to year can mislead. The timeline shows Street Reconstruction and the Controller's maintenance categories (Overlay and Sealing; Patching) together.
5. **Some rows' descriptions conflict with their class.** Some rows filed as Street Reconstruction are described as "Admin & Eng" or "Maintenance":
   - FY2024: $4,094,609. Fund 305 "Private Admin & Eng – PWTRCS2002", $3,818,649; fund 149, $275,960.
   - FY2025: $8,001,131. Fund 501 "Private Admin & Eng – PWENST2301", $7,371,484; fund 501 "Force Maintenance – PWENEN2001", $629,647.

   They are kept as filed and listed in `description_class_conflicts`. If they are not paving construction, Street Reconstruction would be about $18.4M in FY2024 and $13.7M in FY2025. **This is the largest open question in the series.**
6. **Project codes are not defined.** The identifiers (PWENST2201, PWENSW2002, PWTRCS2001 and others) are not defined in any document BeTH holds. Reading PWENST as "street rehabilitation" is unverified, and so is reading PWENSW as "sidewalk".
7. **Timing differs.** A budget year and its spending year differ. Construction lags appropriation, so budget and actual gaps in a single year are not evidence of underspending.

### Fund detail, Street Reconstruction (FY2018–FY2025, selected funds)

The fund names below come from the July 2026 plan p.2, which names funds 133, 134, 601, 616 and 501. Fund 127 is the State gas tax fund named "Special Gas Tax Street Fund" in the Controller's dataset. The others are not identified.

| Fund | FY2019 | FY2020 | FY2021 | FY2022 | FY2023 | FY2024 | FY2025 |
|---|--:|--:|--:|--:|--:|--:|--:|
| 501 General Fund CIP | 331,702 | 3,261,729 | 1,900,044 | 2,747,060 | 1,661,369 | 6,205,874 | 9,610,671 |
| 127 Gas tax | 998,268 | 2,928,516 | 54,796 | 2,203,855 | 1,550,560 | 1,446,271 | 3,451,233 |
| 134 Measure BB | – | 2,578,002 | – | 2,871,814 | 308,375 | 5,583,076 | – |
| 511 Measure T1 | – | 2,198,266 | 4,850,637 | 73,414 | 1,162,752 | 527,315 | – |
| 601 Zero Waste | – | – | 7,988 | – | – | – | 728,763 |
| 616 Clean Storm | – | – | – | – | – | – | – |

Fund 305 ($3.82M FY2024, $3.89M FY2025) is not identified.

### What the series shows, and what it does not

- **Shows.** City-reported Street Reconstruction rose from an average of $3.1M a year (FY2010–FY2017) to $13.8M (FY2018–FY2025). The two highest years are FY2024 ($22.5M) and FY2025 ($21.7M). Those figures include the conflicts in rule 5.
- **Does not show.**
  - Cost per mile, because the category is not paving-only.
  - Whether a given budget was spent.
  - Whether actual General Fund paving rose by the $8M a year that Res. 70,456 committed. General Fund CIP (fund 501) Street Reconstruction was $1.66M in FY2023, $6.21M in FY2024 and $9.61M in FY2025. The FY2025 figure includes $7.37M described as administration and engineering.

---

## 2. A — The 2022 "$7.3 million General Fund" baseline

| What the record says | Source |
|---|---|
| The recommendation calls the $7.3M the "existing General Fund street paving budget". | Council Item 3, July 26, 2022, report p.1; annotated agenda p.4. |
| The resolution text as adopted says "in addition to the existing baseline $7.3 million allocation, for a total amount of $15.3 million". It does not say General Fund. | Annotated agenda, July 26, 2022, p.4. |
| January 2022 staff Table 1 totals the recurring program at $7,275,303. Of that, the Capital Improvement Fund (General Fund) line is **$1,925,000**; the rest is gas tax, SB 1, Measure BB and Measure F. | Item 25a, January 18/25, 2022, p.1. |
| FY2027 budget: "The City has historically allocated about $7.3 million in recurring funding to Street paving from local and state sources." | Adopted budget, June 23, 2026, PDF p.243. |
| A March 2025 workshop slide shows "General Fund: $9.9M/yr" as "Baseline annual streets funding", with no breakdown. | Workshop deck, slide 37 (text extract). |

**Reading.** "$7.3 million" is the rounded $7,275,303 all-source program. The General Fund part was $1.925M, about 26%. The 2022 report's label "General Fund" is wrong on the City's own figures. The adopted resolution's wording, "baseline ... allocation", is not wrong.

The $9.9M on the 2025 slide cannot be reconciled from the slide. One possibility, not verified, is the $1.925M CIP line plus roughly $8M under Res. 70,456. **Confidence:** High on the first point; Low on the $9.9M composition.

**Actuals cross-check.** FY2022 City-reported Street Reconstruction was $13.19M from all funds, including Measure T1 and other one-time sources. The $7.3M was a budget figure and is not comparable to it.

---

## 3. B — Workers' Compensation: $4.05M (June 2023) and $5.5M (July 2023)

| Step | Record | Amount | Source |
|---|---|--:|---|
| Authorization | Council, June 13, 2023: "Use $4,050,000 from the Workers Compensation Fund" toward the Measure T1 gap | 4,050,000 | Annotated agenda, June 13, 2023, p.11 |
| Authorization | Council, July 25, 2023: "authorizes an internal loan of $5.5M from the Workers Compensation Fund" (D and E docks), repaid from waterfront TOT | 5,500,000 | Item 19 report, p.1 |
| FY2023 audited | WC transfers in "-" and out "-"; ending net position $12,650,613; 2017 General Fund loan balance $813,779, with no repayment in FY2023 | – | FY2023 ACFR p.324 and p.122 (text extracts) |
| FY2024 audited | WC transfers in $813,779 and out ($5,500,000) | 5,500,000 out | FY2024 ACFR p.312 |
| FY2024 audited | The $813,779 is the final repayment of the 2017 $6,683,398 General Fund loan (University Ave / Ninth St building); balance $0 | 813,779 in | FY2024 ACFR p.116, Note 4.C |
| FY2024 audited | Transfers note: $5,500,000 to the **General Fund** | 5,500,000 | FY2024 ACFR p.115, Note 4.B |
| FY2025 audited | WC transfers "-"; ending net position ($9,752,938); the only Marina interfund balance is $2,477,099 due to the General Fund | – | FY2025 ACFR p.322, p.113 |

**Arithmetic.**
- Authorized: $9,550,000.
- Audited WC transfers out, FY2023–FY2025: $5,500,000.
- Not visible in any audited WC statement: $4,050,000.

`4,050,000` appears nowhere in the FY2024 or FY2025 ACFR.

**What can be said.**
- One $5.5M transfer left the fund in FY2024 and went to the General Fund.
- No advance or receivable was recorded for either authorization, at June 30, 2024 or June 30, 2025.
- No repayment to Workers' Compensation is recorded for either.

**What cannot be said.**
- Whether the $5.5M carried out the Marina loan, the T1 action, part of each, or something else.
- Whether the $4.05M was met from another source, executed through another fund, or never executed. Its absence from the WC statements is not proof that no money moved.

**City's label conflict.** The FY2024 transfers note prints "Equipment Replacement Fund" in the From column of the $5,500,000 row. The fund statement (p.312) shows the outflow in the Workers' Compensation column, and the group total ($6,450,612) matches total internal-service-fund transfers out. BeTH reads the transfer as Workers' Compensation and records the conflict; it does not correct it.

**Consistency with existing work.** The Marina destination question is already open in `phase2/01-marina-fund-case-study.md` and `phase2/flags/2026-10-25-marina-608-ledger-review.md`. In the approved ledger, BeTH records the $5.5M as a loan into fund 608. Nothing here changes that ledger. These findings add the $4.05M T1 authorization and its absence from the record.

**Needed.** Journal entries and support (records request item 3).

---

## 4. C — What counts toward the $15.3 million Measure FF requirement

**Controlling text.** BMC 7.11.030(B), from the initiative as filed, PDF p.8, transcribed from page images because there is no text layer. If the Council fails to adopt a budget with "at least $15.3 million in funding for street maintenance, from sources other than this tax, and adjusted for inflation, per Resolution No. 70,456-N.S.", it may not impose the tax for the following two years.

Two further provisions qualify it:
- 7.11.030(C), p.9, reduces the requirement if an external source included in the 2023-24 budget is lost or declines.
- 7.11.030(D), p.9, suspends it in Stabilization Reserve draw years or declared emergencies.

The transcription is in `phase2/sources/measure-ff-ordinance-transcription.md`. Re-read the page images before quoting it publicly.

**What the documents establish.**

1. Res. 70,456 defines $15.3M as $8M of General Fund plus the "existing baseline $7.3 million allocation" (annotated agenda, July 26, 2022, p.4). That baseline was gas tax, SB 1, Measure BB, Measure F and the CIP Fund, with no Zero Waste or Storm Water (Item 25a, January 2022, p.1).
2. City staff introduced Zero Waste and Storm Water in November 2023 among "three important new revenue sources". Zero Waste is "rate revenue ... to offset the impact of Zero Waste collection vehicles" (Item 17, November 28, 2023, p.1).
3. The July 2026 plan:
   - Zero Waste (fund 601) contributes $2M a year to offset collection-vehicle impact.
   - Clean Storm (fund 616) contributes $1M a year for cross drains.
   - Staff exclude Clean Storm from the amount "available for street rehabilitation" (p.2, p.3).
4. Actuals: the City reported almost no Street Reconstruction spending from fund 601 ($7,988 in FY2021; $728,763 in FY2025) and none from fund 616.

**What it means.**
- The ordinance counts any "funding for street maintenance, from sources other than this tax". On its face, that does not exclude enterprise funds.
- But the $15.3M figure it incorporates was built from sources that did not include them.
- Counting Zero Waste and Storm Water lets enterprise-fund money meet a requirement that was sized on gas tax, county and General Fund money.
- Whether that is permitted is a question for the City Attorney.
- Whether Zero Waste rates can pay for pavement at all is a separate question. It is outside this review and not answered here.

**Scenario arithmetic, not a compliance finding.** FY2027 Table 1A sources other than Measure FF total **$18,742,503**. Without Zero Waste and Clean Storm, they total **$15,742,503**.

Escalating $15.3M at the City's own 3% gives:
- $17,220,285 from an FY2023 base.
- $16,231,770 from an FY2025 base.

So the FY2027 plan clears either figure with the two enterprise funds and falls short of both without them.

This scenario rests on three unverified assumptions:
- **Index.** Res. 70,456 names the greater of Bay Area CPI or state per capita personal income growth, not 3%. Neither index value has been checked.
- **Base year.** No document BeTH holds states it.
- **Scope.** The City may count street-maintenance budgets outside the paving plan.

The requirement also concerns the **adopted budget**, not spending, so actuals alone cannot show compliance.

**City web page error.** The City's Measure FF page links "Ordinance No. 7939-N.S.". That ordinance, page 1 kept in `sources/measure-ff/`, is the Ashby BART real property exchange. Measure FF is Ordinance 7,952-N.S. This was read from the page image, which has no text layer. **Confidence:** Moderate.

**Needed.** The City's maintenance-of-effort calculation and the funds it counts (records request item 4).

---

## 5. D — $9,481,286 planned versus $8,487,200 shown for FY2027

| Series | FY2025 | FY2026 | FY2027 | FY2028 | Source |
|---|--:|--:|--:|--:|---|
| November 2023 plan (Res. 70,456 line) | 8,937,022 | 9,205,132 | 9,481,286 | 9,765,725 | Item 17, Nov. 28, 2023, p.2 |
| FY2026 budget / July 2026 plan (fund 501, "Street Rehab PCI Improvements") | (8,000,000 implied) | 8,240,000 | 8,487,200 | 8,741,816 | Adopted budget, June 23, 2026, p.215; plan July 7, 2026, p.2 |

- Each series is 3% compound escalation from its FY2025 base, reproduced to within $1. The City's spreadsheet appears to carry unrounded values.
- The FY2027 gap, **$994,086**, is the **$937,022** FY2025 base difference carried forward two years at 3%.
- The November 2023 plan's FY2024 figure was $5,996,598. The budget row shows $14,100,000 for prior years. These are not reconciled here.

**Unexplained.**
- No document BeTH holds says why the base moved from $8,937,022 back to $8,000,000.
- The July 2026 plan says funding "is escalated consistent with the terms of the applicable Council fiscal policy (Resolution No. 70,456-N.S.)" (p.12). That policy names the greater of Bay Area CPI or state per capita income growth. Both series nonetheless use exactly 3%.
- Whether 3% equals, exceeds or falls short of the policy index in any year has not been checked.

**Confidence:** High on the arithmetic; Unknown on the reason.

**Needed.** Budget worksheets showing the base and the index used (records request item 5).

---

## 6. What remains unavailable

| Gap | Why it matters | Where |
|---|---|---|
| Project-level actual paving ledger, FY2014–FY2026 | The SCO series is all street purposes and has the class conflicts in §1 rule 5 | Records request item 1 |
| SCO filings as submitted, and the City's fund-to-category crosswalk | Explains category changes (FY2014, FY2025) and the class conflicts | Item 2 |
| Journal entries: $5.5M WC transfer; any $4.05M entry; TOT repayments | Settles B | Item 3 |
| Maintenance-of-effort calculation | Settles C on the City's own terms | Item 4 |
| Res. 70,456 base and index worksheets; $7.3M and $9.9M composition | Settles D and the remainder of A | Item 5 |
| Fund and project code dictionaries (funds 305, 506, 147, 149; PW* codes) | Makes the detail readable | Item 6 |
| FY2026 actuals | The Controller has not yet published FY2025-26 | Public, when published |
| Public cross-check, not requested: Alameda CTC Measure B/BB/VRF annual compliance reports for Berkeley | Independent actuals for funds 133 and 134 | alamedactc.org |

Draft request: `phase2/history/records-request-draft-2026-10-26.md`.

## Confidence summary

| Claim | Confidence |
|---|---|
| SCO figures are what the City reported | High (checked against Controller pages and data) |
| Street Reconstruction as a measure of paving construction | Moderate (includes non-paving and the class conflicts) |
| $7.3M was all-source, not General Fund | High |
| Audited WC transfers out FY2023–25 = $5.5M, to the General Fund | High (FY2024 note has a City label conflict) |
| What happened to the $4.05M | Unknown |
| Which funds count toward $15.3M | Unresolved (legal) |
| FY2027 gap = re-based FY2025 at 3% | High (arithmetic); reason Unknown |
| Ordinance 7,939 mislink on the City's page | Moderate (page image read) |

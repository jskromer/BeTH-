# BeTH Fact Review — 2026-09-05

Acronyms: ACFR = Annual Comprehensive Financial Report · AAO = Annual Appropriations Ordinance · GF = General Fund · OPEB = Other Post-Employment Benefits (retiree health) · CalPERS = California Public Employees' Retirement System · CIP = Capital Improvement Program · PEPRA = Public Employees' Pension Reform Act · UAL = Unfunded Accrued Liability · FTE = Full-Time Equivalent · AV = Assessed Value · MD&A = Management's Discussion and Analysis · SB 63 = Connect Bay Area Act · GO = General Obligation · T1 = Measure T1 (2016 bond)

Scope: every numeric claim in `berkeley-fiscal-reality/src/App.jsx` (the advocacy site, where the $700M appears), the headline cards on `docs/berkeley-budget-basics.html` (the public hub), and the three files in the Claude project (T1 tracker, Mayor's-budget explainer, fiscal card). Checked against the FY2025 ACFR, the City Auditor's April 2026 financial-condition report (both in the repo), the FY27–28 budget JSON extracted from Item 21, the campaign site's `budget-spine.json`, and press coverage of the November 2026 measures.

Alignment target (campaign site, `kromerforberkeley.org/data/budget-spine.json`, checksum-verified to the June 23 2026 adoption packet):

| | All-funds expenditures |
|---|---|
| FY2024 actual | $729.2M |
| FY2025 actual | $788.6M |
| FY2026 adopted | $829.2M |
| **FY2027 adopted** | **$905.2M** |
| FY2028 adopted | $865.3M |

The AAO for FY2027 appropriates $921.6M gross / $795.8M net (gross counts interfund transfers twice; net removes them). $905.2M is the budget-book department total and is the figure both sites should carry as "the budget."

---

## 1. The $700M problem — advocacy site (`App.jsx`)

Four places say Berkeley "manages over $700M/year in total revenues," and the audited-numbers table lists "Total Government Revenue $703M+" with the FY2025 ACFR as the source.

**The ACFR does not say that.** FY2025 government-wide total revenues are **$619.6M** ($474.5M governmental + $145.1M business-type; ACFR Statement of Activities). FY2024 was $593.8M. Confidence: High — read directly off the statement.

Where $700M probably came from: FY2024 all-funds *expenditures* were $729.2M. Somebody carried a spending total over as a revenue total, and it has been stale for two budget cycles anyway.

Fix: replace the four "$700M revenue" statements with the adopted-budget figure ("Berkeley's adopted FY2027 budget is $905M across all funds") and correct the table row to "Total revenues (government-wide, audited FY2025): $619.6M." The rhetorical point ("Berkeley is not underfunded") survives either number.

Lines: 334, 377, 432, 531, 1026.

## 2. Other errors on the advocacy site (`App.jsx`)

| Claim on site | What the source says | Confidence | Line(s) |
|---|---|---|---|
| "General Fund Revenue $268M (FY25 audited) / $262M (FY24)" | ACFR FY2025 GF revenues: **$285.8M** (GAAP basis) or **$275.4M** (budgetary basis); FY2024 $261.8M. $262M is the FY2025 *original adopted budget*, and $268M is the FY26 adopted figure. Neither is an audited actual. | High | 379, 386 |
| "General Fund Expenditure $295M (FY25) / $274M (FY24)" | ACFR FY2025 GF expenditures: **$276.9M** (GAAP) or $261.4M (budgetary; $310.9M including transfers out). $295M matches nothing in the ACFR. | High | 380, 387 |
| GF projection row: FY27 revenue $273M / expenditure $300M / gap −$27M | Adopted FY27 GF: revenues **$314.9M**, expenditures **$313.9M**, surplus $1.0M after the balancing plan (baseline before cuts: $297.2M / $329.4M / −$32.3M). The whole FY23–FY27 table predates the April 2026 balancing plan. | High | 386–388 |
| "Stability Reserve $32.8M — 19.5% of GF (target: 25%)" | $32.8M is correct. 19.5% and 25% are not: total reserves (Stability $32.8M + Catastrophic $25.5M = $58.3M) were **21.3%** of adopted GF revenues per the Auditor; the new goal is a **20–30% range**, to be reached within ten years starting FY2026 (Reso. 71,908-N.S., July 29 2025). | High | 384, 793 |
| "Reserve goal deferred to FY 2033; target cut to 25%" | See above. Neither "FY2033" nor "25%" appears in the ACFR or the audit. | High | 660, 698 |
| "Section 115 Trust $29.5M (FY25) / $35.5M (FY24) — $6M decline from FY24" | $29.5M at June 2025 is correct (Auditor). The $6.0M draw is an **FY2026** balancing measure, so it cannot explain an FY24→FY25 decline. The $35.5M FY24 figure is unsourced; the Auditor's Figure 21 shows contributions, not balances. | Moderate | 803 |
| "Govt. Net Position: 2022 audit −$101.7M → 2026 audit −$188.7M (worse)" | The 2026 audit reports governmental-activities net position of **+$197.8M** in FY2025, up from −$152.6M in FY2018; total city net position is +$467.9M (ACFR). The row is wrong in sign and direction. Unrestricted net position (−$415.2M) is the negative figure, and it is already its own row. | High | 655 |
| "Expense growth +39% over decade" (2026 audit) | Auditor: governmental-activities expenses **+33%** (FY2016–FY2025, inflation-adjusted); personnel +20%. | High | 650 |
| "Personal Income per Resident +11% → +1% real growth" | Auditor's 2026 figure is **median household income** +1% (2016–2024), a different measure from per-capita personal income. Relabel or drop. | Moderate | 662 |
| "Pension Funded Ratio 66–72% — still HIGH RISK" | Auditor: **66%** (FY2024). Drop the "–72%". | High | 653 |
| "0 of 5 audit recs resolved" / "2022 Audit Recommendations: Where Things Stand" with Not Addressed / Backsliding labels | The 2026 audit does **not** publish a status table for the five 2022 recommendations. It repeats several themes (reserves, Section 115, enterprise funds, capital plan) and notes the City "agreed or partially agreed." The five-row status panel is BeTH's own scoring; label it as such or remove the "0 of 5" stat. | Moderate | 344, 533, 641–648 |
| "Unfunded capital $1.2B → $1.8B in three years" | Auditor: **$1.8B** reported in FY2024 (FY25–29 CIP). Hub pages elsewhere say ~$2.1B (FY27–31 CIP). Pick one and date it. | Moderate | 452, 646 |
| "Berkeley pays the employee's own 8% CalPERS contribution… ~$16–17M/yr" | ACFR: required employee rates are 8% (Misc classic), 9% (safety classic), 8.25–13.5% (PEPRA), and the average *active employee* contribution is 8.0%/9.0% of pay. Whether the City picks that up under any MOU is not in the ACFR or the audit. The site already hedges ("can't be confirmed without MOUs"); the comparison table row "Employee pays 0% — city pays it" does not hedge and should. | Low | 466, 815, 848 |
| CalPERS funded status bars: Misc 80.1 / Police 68.7 / Fire 80.9; "Avg. CalPERS Agency (2024) 80.2" | These are from the **June 30 2021** valuations (footer admits it). Five years old. ACFR FY2025 schedules give plan fiduciary net position as % of total pension liability at the June 30 2024 measurement date — use those. | High (that it's stale) | 858–863 |
| Personnel projection $342M → $487M, fringe 65% → 134% | From the Feb 2023 Foster & Foster study. Not wrong, but three years old and pre-dates the FY27 re-basing that cut $16.5M of personnel budget. Date it on the page. | Moderate | 403–420 |
| "0.5% City Sales Tax ~$9M/yr" | City estimate **$9–10M/yr** (Daily Cal, June 2026). Fine; fiscal card says $10M. Harmonize. | High | 868 |
| "$300M GO Bond ~$20M/yr debt svc" | City's published cost is **$22.14 per $100,000 AV** annually (Daily Cal). On ~$28B AV that is ~$6M/yr at full levy, so $20M/yr debt service is not what the City has said. Replace with the per-$100k figure. | Moderate | 869 |
| "Regional Transit Tax (SB63) 0.5% sales tax — Nov 2026" | Rate in Alameda County is 0.5%; as of the latest reporting it was **authorized but not yet placed** on the ballot. Say "authorized for" until placement is confirmed. | Moderate | 870 |
| "Measure FF, Measure W, Measure P — since 2020" | Measure P passed **2018**. | High | 517 |
| "Property tax revenue grew 9%" | +9.4% for the general-purpose levy ($135.7M → $148.4M). Total property taxes grew 7.7% ($215.2M → $231.9M). Say which. | High | 378, 432 |

Verified correct (High): net pension liability $686.4M / $723.8M; net OPEB $43.2M / $83.4M; unrestricted net position −$415.2M / −$400.4M; health & welfare $54.8M / $44.5M; public safety $162.3M / $190.0M; FY26 one-time measures ($6.0M Section 115, $5.2M Workers' Comp, $6.2M IT fund, $2.5M U1, 44.4 unfunded positions, 11.8 positions shifted); $3M Section 115 draw in FY25; structural deficit $32M FY27 / $33M FY28; Section 115 balance $29.5M; 2022 reserve goal "30% by FY2027"; assessed value +48% to $28.2B.

Not verifiable from sources in hand (Unknown): $316M carryovers / $367M encumbrances over three AAOs and the $13.5M/$13.2M/$5.4M GF carryovers (need the three AAO #1 staff reports); "54 audits, 384 recommendations, 265 implemented, 76 dropped, 43 open" (need the Auditor's FY2026 follow-up report); the $8–10M and $2–3M savings estimates attached to the position actions.

## 3. Public hub (`docs/berkeley-budget-basics.html`) — headline cards

| Card | Problem | Fix |
|---|---|---|
| "~$1.8B Total annual budget (all funds, FY2027)" | That is the **two-year** biennial total ($905.2M + $865.3M = $1.77B). One year is $905.2M. This is the most visible number on the hub's front door and it is off by 2×. | "$905M — FY2027 budget, all funds" |
| "~$283M General Fund" | $283M is the FY27 GF *baseline after* the balancing plan's reference point (plans-synthesis uses it the same way). Adopted FY27 GF expenditures are **$313.9M**; revenues $314.9M. | "~$314M — General Fund, FY2027" |
| "~$2.1B unfunded infrastructure" | Auditor's figure is $1.8B (FY2024). If $2.1B is from the FY27–31 CIP, cite it; otherwise use $1.8B. | Cite or change |
| "1,605 staff (FTE)" | Matches Item 21 (1,604.84). | — |
| "~$29M recurring gap" | Matches ($32.3M / $33.2M baseline; ~$29M after revenue re-projection). | — |
| "General Fund reserves grew from ~$84M (2018) to ~$158M (2023)" | Reserves policy funds (Stability + Catastrophic) were $58.3M at June 2025. $158M is presumably total GF fund balance, which includes assigned/committed amounts. Label it "fund balance." | Relabel |

`docs/berkeley-fund-map.html` already says $905M / 18 departments / six = 81% — consistent with the campaign site.

## 4. Project files

**T1 tracker (`index.html`)** — figures trace to the Sept 2025 resolution, the March 2026 AUP report and the CIP presentation; "$22/$100k AV" matches the City's $22.14. Nothing found wrong. Dated June 3 2026; Fire Station #2, Corp Yard Green Room, Telegraph-Channing garage, D&E Dock and K Dock all had spring/summer 2026 completion targets that have now passed — status column needs a refresh from the next PRW quarterly.

**Mayor's-budget explainer** — no numeric claims beyond office dates (Hancock council 1971–79, mayor 1986–94; council-manager since 1923). Consistent with the record. No change.

**Fiscal card (`berkeley_fiscal_reality_card.jsx`)** — same 2021/2023 sourcing as App.jsx: "$3.1B total unfunded," "$614M pension + OPEB gap," "$2.52B infrastructure (FY24–28)," "$72M CalPERS payment," "$27M deficit," "1,792 FTEs," "GF revenue $273M/$262M/$262M/$268M/$273M." Every one of these is superseded: pension + OPEB is now $729.6M net (ACFR FY25), capital is $1.8–2.1B, deficit $32–33M, FTE 1,605, GF ~$314M. This file is an April 2026 artifact and should be retired or rebuilt from the FY27 numbers.

## 5. What "the budget" should mean on both sites

Three different totals are in circulation and each is right for something:

- **$905.2M** — FY2027 all-funds expenditures by department (budget book). Use this as "the budget."
- **$921.6M gross / $795.8M net** — FY2027 AAO. Gross double-counts interfund transfers. Use only when discussing the ordinance.
- **$619.6M** — FY2025 audited government-wide revenues. Use only when discussing the ACFR.
- **~$314M** — FY2027 General Fund. Use whenever the deficit, the sales tax, or position cuts are the subject, because that is the only part of the $905M those things touch.

Nothing on either site should say $700M, and nothing should say $1.8B for a single year.

Acronyms: ACFR = Annual Comprehensive Financial Report · AAO = Annual Appropriations Ordinance · GF = General Fund · OPEB = Other Post-Employment Benefits · CalPERS = California Public Employees' Retirement System · CIP = Capital Improvement Program · PEPRA = Public Employees' Pension Reform Act · UAL = Unfunded Accrued Liability · FTE = Full-Time Equivalent · AV = Assessed Value · MD&A = Management's Discussion and Analysis · SB 63 = Connect Bay Area Act · GO = General Obligation · T1 = Measure T1

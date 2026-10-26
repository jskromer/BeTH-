# How Did We Get Here? Berkeley's Budget Decisions and Their Consequences

**Phase 2 research and design workstream. Started 2026-10-26.** Status: research prototype. Not reviewed by a person.
Not published.

The workstream builds an evidence-based timeline of City Council budget decisions and what followed them. It starts
with streets and infrastructure, 2010–2026. The General Fund, the Marina, housing and other services come after the
framework is validated.

It is kept separate from the approved financial ledgers (`data/funds/`) and from the five Ask BeTH answers. Nothing
here changes either.

| What | Where |
|---|---|
| Decision history (machine-readable) | `data/decisions-streets.json` |
| Outcome series | `data/outcomes-streets.json` |
| Local visual prototype | `docs/timeline.html`. Serve the repository root and open `/phase2/history/docs/timeline.html` |
| Builder and checks | `tools/build_history.py` (`--write` rebuilds the data and the page) |
| Primary records | `sources/` (Council annotated agendas, MTC tables) and `../sources/` (shared Phase 2 sources) |
| Image credits | `docs/assets/photos/credits.json` |
| Tests | `../tests/test_history.py` |

## Rules the builder enforces

1. **Citations are checked.** Every quote must appear on its cited PDF page; the build fails otherwise. Every
   plotted pavement-condition (PCI) value must equal the Berkeley row of its MTC edition. Every miles-paved value must
   match the City's Table 2.
2. **Every field has a status.** It is `verified` (with a citation), `to_collect` (the record has not been obtained,
   with where to look) or `not_in_record` (the record we hold does not say).
3. **Votes are copied as recorded.** "All Ayes" stays "All Ayes", and names are never inferred from the roll call.
   Members present at roll call and later arrivals are shown separately, as printed.
4. **Alternatives are only those documented at the time.** These are failed motions with their votes, and the options
   in the staff recommendation. Retrospective scenarios are a separate field, empty until researched and labelled as
   hindsight.
5. **No causal claims.** Outcomes sit next to decisions. Where the City attributes an outcome to a decision, the card
   quotes the attribution and names who made it.
6. **No scores or rankings of officials.**
7. **The evidence class is always shown:** policy commitment, ballot authorization, loan authorization, adopted,
   planned, actual or projected.

## Storyboard: 14 proposed events

Coverage counts the nine fields per event: decision, instrument, vote, money, purpose, alternatives, actual
expenditures, outcomes and outstanding commitments.

| # | Date | Kind | Event | Record (verified) | Coverage | Still to collect |
|---|---|---|---|---|---|---|
| 1 | 2012-11-06 | Voter | Measure M street and watershed bond approved | Debt service still levied: FY2027 rate 0.0040% (Ord. 8,026-N.S. first reading, June 16, 2026) | 2/9 | Placement resolution and vote, bond amount, project list, results |
| 2 | 2016-11-08 | Voter | Measure T1 infrastructure bond approved | Debt service still levied: FY2027 rate 0.0140%. In 2023 Council directed T1 funds to Hopkins Street by the end of FY2027 | 3/9 | Placement resolution and vote, amount, phases, street spending |
| 3 | 2020 (to confirm) | Context | City Auditor: "Rocky Road: Berkeley Streets at Risk and Significantly Underfunded" | Status report received and filed Dec 10, 2024 | 1/9 | The audit report itself, its findings and the status of each recommendation |
| 4 | 2022-01-25 | Council | Res. 70,204-N.S.: Street Maintenance Policy and Five-Year Paving Plan (Equity Alternative) | All Ayes (Arreguin/Harrison). Alternative documented: Commission plan version 12A ("Arterial Alternative") | 4/9 | Staff report: plan funding, goals |
| 5 | 2022-07-26 | Council | Res. 70,456-N.S.: +$8M a year General Fund for streets ($15.3M total) | All Ayes (Wengraf/Arreguin). Suspension clauses quoted. City attributes the FY2024–26 paving acceleration to it | 8/9 | Annual General Fund paving appropriations and actuals since FY2023 |
| 6 | 2022-08-03 | Council | Res. 70,492-N.S.: $650M housing and infrastructure bond placed on the ballot | Roll call 8–0, Droste absent. Alternatives: $600M or $650M; $300M proposed July 26 | 6/9 | Nov 8, 2022 election result |
| 7 | 2023-07-25 | Council | Res. 70,997-N.S.: $5.5M internal loan for Marina docks | Consent roll call 8–0, Harrison absent. Alternative: amend the State boating loan (four options) | 7/9 | Dock project status; loan repayments |
| 8 | 2023-11-28 | Council | Res. 71,120-N.S.: Five-Year Street Rehabilitation Plan FY2024–28 | Hahn/Wengraf alternative failed 4–5 (names recorded); final All Ayes. Miles paved FY2024 10.7, FY2025 8.4 | 6/9 | Staff report: funding by year, expected miles; Hopkins status |
| 9 | 2024-07-30 | Council | Res. 71,461-N.S.: Measure FF sent to voters | All Ayes (Arreguin/Taplin). Alternative documented: adopt the initiative without a vote | 6/9 | none |
| 10 | 2024-12-10 | Voter | Measure FF results confirmed; Ord. 7,952-N.S. | Ordinance number and confirmation | 5/9 | Vote totals; FY2025–26 receipts and spending; first annual report |
| 11 | 2026-03-17 | Council direction | Draft a $300M infrastructure bond and a 0.5% sales tax measure | All Ayes (Ishii/Taplin); affirmed May 19, 2026 (All Ayes) | 5/9 | Options and sizes considered; final placement resolution |
| 12 | 2026-06-23 | Council | Res. 72,340-N.S.: FY2027–28 budget and FY2027–31 CIP | Kesarwani/Blackaby alternative failed 3–5–1 (names recorded); final All Ayes. Streets five-year CIP $139,356,147 | 6/9 | Budget priorities; FY2027 actuals (late 2027) |
| 13 | 2026-07-07 | Council | Res. 72,377-N.S.: Five-Year Street Rehabilitation and Measure FF plans FY2027–31 | All Ayes (Humbert/Tregub). Plan funding $96,336,212; City projection PCI ≈62 by 2038 | 7/9 | none (too recent for outcomes) |
| 14 | 2026-11-03 | Voter (pending) | $300M infrastructure bond on the ballot | Amount from the May 19 direction | 1/9 | Placement resolution, vote, ballot question, project list |

Totals: 67 of 126 fields verified, 78 page-checked citations.

## Outcome series held

| Series | Years | Basis | Caveats |
|---|---|---|---|
| Centerline miles paved | FY2019 (incl. FY2018)–FY2026 | City staff, July 7, 2026 plan, Table 2 (PDF p.5); FY2026 projected | Staff-reported; no mileage before FY2018 in hand |
| PCI, MTC | 2010–2022 | MTC tables, 2012, 2015, 2016 and 2019–2022 editions, Berkeley row | 3-year moving averages. Editions revise earlier years (2018 is 58 in the 2019 edition and 57 in the 2020 edition), and every printed value is kept. MTC changed its rating standard in 2016 |
| PCI, City | 2024 (56), 2025 (57), 2026 (59, projected) | 2024 pavement report p.5; July 2026 plan p.12 | Single-year StreetSaver figures; not joined to the MTC series |
| Annual paving spending | — | **Not held** | Not charted until a single-basis series exists |

## Source inventory (held)

| Key | Document | File | Pages | Pages cited | SHA-256 (prefix) |
|---|---|---|---|---|---|
| `aa:2022-01-25` | City Council annotated agenda, 2022-01-25 | `sources/council-2022-01-25-annotated.pdf` | 21 | 2, 7 | `c3640df4c5f0` |
| `aa:2022-07-26-special` | Special meeting annotated agenda, 2022-07-26 | `sources/council-2022-07-26-special-annotated.pdf` | 7 | 2, 4 | `983be14f1503` |
| `aa:2022-07-26` | Regular meeting annotated agenda, 2022-07-26 | `sources/council-2022-07-26-annotated.pdf` | 21 | — | `c3c86dfc8db4` |
| `aa:2022-08-03-special` | Special meeting annotated agenda, 2022-08-03 | `sources/council-2022-08-03-special-annotated.pdf` | 7 | 3 | `1683f864fd52` |
| `aa:2023-07-25` | Annotated agenda, 2023-07-25 | `sources/council-2023-07-25-annotated.pdf` | 26 | 3, 12 | `46ded183541e` |
| `aa:2023-11-28` | Annotated agenda, 2023-11-28 | `sources/council-2023-11-28-annotated.pdf` | 17 | 2, 9 | `a14d99f34e35` |
| `aa:2024-07-09` | Annotated agenda, 2024-07-09 | `sources/council-2024-07-09-annotated.pdf` | 16 | 10 | `3fcdf72cbf56` |
| `aa:2024-07-30-special` | Special meeting annotated agenda, 2024-07-30 | `sources/council-2024-07-30-special-annotated.pdf` | 12 | 2 | `88a1f5bee8c3` |
| `aa:2024-12-10` | Annotated agenda, 2024-12-10 | `sources/council-2024-12-10-annotated.pdf` | 13 | 11 | `ba81ff85e96f` |
| `aa:2024-12-10-special` | Special meeting annotated agenda, 2024-12-10 | `sources/council-2024-12-10-special-annotated.pdf` | 3 | 3 | `a59834fe38da` |
| `aa:2026-03-17-special` | Special meeting annotated agenda, 2026-03-17 | `sources/council-2026-03-17-special-annotated.pdf` | 3 | 2 | `9ab3a7368ded` |
| `aa:2026-05-19-special` | Special meeting annotated agenda, 2026-05-19 | `sources/council-2026-05-19-special-annotated.pdf` | 3 | 2 | `2ed6fb252610` |
| `aa:2026-06-16` | Annotated agenda, 2026-06-16 (bond tax rates) | `sources/council-2026-06-16-annotated.pdf` | 23 | 5, 7 | `46542111fa4c` |
| `aa:2026-06-23` | Special meeting annotated agenda, 2026-06-23 (budget) | `sources/council-2026-06-23-annotated.pdf` | 8 | 2, 3 | `b60318e6b41c` |
| `aa:2026-07-07` | Annotated agenda, 2026-07-07 | `sources/council-2026-07-07-annotated.pdf` | 14 | 2, 9 | `c569c62bd0ca` |
| — | Annotated agenda, 2025-06-24 (held for the Marina expansion: FY2026 General Fund transfer) | `sources/council-2025-06-24-annotated.pdf` | 20 | — | — |
| `plan:2026-07-07` | Five-Year Street Rehabilitation and Measure FF Plans, July 7, 2026 | `../sources/street-rehab-measure-ff-2026-07-07.pdf` | 70 | 3, 5, 11, 12, 13 | `bba211289db1` |
| `ptap25` | 2024 Pavement Management Program Update (P-TAP 25) | `../sources/pavement-management-update-ptap25-2025-04.pdf` | 158 | 5 | `5e431b32fca3` |
| `budget:2026-06-23` | FY2027-28 budget and FY2027-31 CIP adoption packet | `../sources/budget-adoption-2026-06-23.pdf` | 260 | 216 | `1556cdd4f90d` |
| `loan:2023-07-25` | $5.5M loan staff report, July 25, 2023 | `../sources/council-2023-07-25-item19-wc-loan.pdf` | 11 | — | `83bfd9e7ff47` |
| `mtc:2012` … `mtc:2022` | MTC Pavement Condition Index tables, 2012, 2015, 2016, 2019, 2020, 2021, 2022 | `sources/mtc/` | 4–8 each | Berkeley row | see the builder's registry |

The City posts annotated agendas for 2021 onward on berkeleyca.gov (City Council Agendas page). Earlier meetings are
not on the current site.

## Missing records, in the order they matter

1. **Pre-2021 Council records**: annotated agendas or minutes for the Measure M (2012) and Measure T1 (2016) ballot
   placements, the 2014–2020 paving plans, and Vision 2050 actions (2017–2020). Where to look: City Clerk Records
   Online archive, or a public records request.
2. **Annual paving spending, FY2010–FY2026, on one basis**: appropriations versus actual expenditures by fund
   (General Fund, Measure M, T1, gas tax, Measure B/BB/F, Zero Waste, Clean Storm). Without this there is no spending
   chart. Where to look: adopted budget and CIP books, CIP actuals, ACFR capital outlay.
3. **Staff reports** for Jan 25, 2022 (plan funding and goals) and Nov 28, 2023 (plan funding, expected miles). These
   fill "What was supposed to happen?".
4. **Election results**: Measure L (Nov 8, 2022) and Measure FF (Nov 5, 2024) vote totals, from the Alameda County
   Registrar of Voters or the City's results-confirmation items.
5. **The 2020 City Auditor streets audit** ("Rocky Road") and its status reports, including Dec 10, 2024.
6. **The $300M bond placement resolution** (summer 2026), its vote and its project list.
7. **MTC 2023 and 2024 PCI editions**, and MTC annual (non-averaged) Berkeley scores, which MTC provides on request.
8. **Measure M and T1 completion reports**: amounts, street miles and green infrastructure delivered.
9. **Measure FF annual report** (BMC 7.11.050): streets paved, cost per mile, PCI of all streets.

## Data schema (v1)

Each event in `decisions-streets.json` → `events[]`:

```
id                 stable identifier: bdh-<topic>-<date>-<instrument>, never reused
date               ISO date; date_precision when not an exact meeting date
kind               council_decision | council_direction | voter_decision | context
item               agenda item as printed (e.g. "Action Calendar 17", "Consent Calendar 19")
title              plain-language headline (presentation; not evidence)
decision           Field: what was decided, verbatim-derived, with citations
instrument         Field: {kind: resolution|ordinance, number: "70,456-N.S."}
vote               Field: {mover, seconder, recorded: "All Ayes" | "roll call" | ..., ayes[], noes[], abstain[],
                   absent[], present_at_roll_call[], arrivals[]}  (names only where the record prints them)
failed_motions[]   Field[]: documented alternatives that were voted down, with their roll calls
money              Field: {amount, basis: adopted|amended|actual|planned|policy commitment|ballot authorization|
                   loan authorization, source, ...}
purpose            Field: stated purpose and expected outcome, quoted
alternatives       Field: alternatives documented at the time (options in the recommendation, failed motions)
retrospective_scenarios[]  hindsight scenarios; must stay empty until each is researched and labelled
actual             Field: subsequent appropriations and expenditures
outcomes           Field: measurable outcomes, with any causal attribution quoted and attributed
outstanding        Field: commitments and liabilities still open
uncertainties[]    plain-language list

Field = {status: verified|to_collect|not_in_record, value, citations[{doc_id, pdf_page, quote}], note,
         needed, where_to_look}
```

`outcomes-streets.json` holds the time series, each with its basis, method breaks, gaps and per-point citations.
`documents` in both files registers every source: title, local path and kind.

## Next steps before the full timeline

1. Collect the missing records above, starting with 1–3.
2. Have a person review the 14 storyboard events against their cited pages.
3. Agree the event-selection rule, i.e. what counts as "significant", before adding events, so the selection is not
   ad hoc.
4. Then expand to the General Fund, the Marina (reusing the Marina workstream's sources), housing and other services.

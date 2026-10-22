# Fund-Level Dashboard, Agent Pipeline, and Emergency Remediation Plan

*Berkeley Transparency Hub (Learn About Berkeley) · October 22, 2026 · Confidence tags: (High) · (Moderate) · (Low) · (Unknown)*

**Acronyms:** AAO = Annual Appropriations Ordinance · ACFR = Annual Comprehensive Financial Report · ARPA = American Rescue Plan Act · B&F = Budget & Finance Policy Committee · BCDC = Bay Conservation and Development Commission · BPA = Berkeley Police Association · CIP = Capital Improvement Program · DBW = California Division of Boating and Waterways · GF = General Fund · MOU = memorandum of understanding (labor contract) · OPEB = other post-employment benefits (retiree health) · PRWC = Parks, Recreation and Waterfront Commission · TIC = Transportation and Infrastructure Commission · WC = Workers' Compensation (internal service fund)

---

## 0. What this plan delivers, in order

| # | Deliverable | Target date | Why this order |
|---|---|---|---|
| 1 | **Emergency remediation page** (if Measures U and V fail): the City's own Scenario 2 next to BeTH's reform stack, sized where sourced | **October 30** (before ballots are counted) | Steve asked for an example soon; the page is useful whichever way the vote goes |
| 2 | **Fund ledger schema** and the **Marina Fund** page built on it: 25 years of a fund set up to be self-supporting, and every dollar moved in and out since FY2022 | **November 6** | The worked example that proves the schema before 110 funds are loaded |
| 3 | **Five more funds** on the same schema (General, Parks Tax, Equipment Replacement, Workers' Comp, Zero Waste) | November 20 | Each one is tied to the Marina story or to the deficit |
| 4 | **All ~110 funds** auto-extracted from the ACFR combining statements, FY2021–FY2025 | December 18 | Mechanical once the schema is proven |
| 5 | **Agent pipeline** reading Council and commission postings and proposing ledger updates for review | Pilot December 1; running by January 15 | Needs the schema to write into |
| 6 | **City dashboard** on the live ledger: fund browser, flows, deficit tracker, remediation tracker | January 30, 2027 | Last, because it is a view over 2–5 |

Dates are targets, not promises. Each deliverable is independently publishable.

---

## 1. The fund ledger: one schema for 110 funds

The Fund Map page already establishes the structure: ~110 funds in the FY2025 ACFR, 5 major governmental, ~86 nonmajor governmental, 8 enterprise, 8 internal service, plus fiduciary trusts; $621.9M in governmental fund balances, 65% restricted, $22.2M unassigned. (High) What BeTH does not have is a **record per fund** that an agent can update. That is the schema.

### 1.1 Fund record (`data/funds/<fund_number>.json`)

```
fund_number        "608"                         (City's own number; Marina is 608, GF 011, T1 Capital 511)
name               "Marina Operations Fund"
type               enterprise | special_revenue | capital_project | debt_service | internal_service | general | fiduciary
department         "Parks, Recreation & Waterfront"
established        {"year": 1964, "purpose": "$1.8M State loan to build the Waterfront", "source": ...}
legal_basis        ballot measure / ordinance / grant agreement / bond covenant / Council resolution
restriction        restricted | committed | assigned | unassigned   (ACFR classification)
self_supporting    true/false  (enterprise funds are designed to be)
annual             [ {fy, revenue, expenditure, transfers_in, transfers_out, ending_balance, net_position, source, confidence} ]
flows              [ see 1.2 ]
obligations        [ unfunded capital need, debt, loans owed, with source and date ]
status             { structural_deficit: true/false, years_in_deficit, last_update, open_questions }
```

### 1.2 Flow event (the part that makes mismanagement visible)

Every movement of money that is not the fund's own revenue or ordinary spending is a dated event:

```
date              "2025-06-24"
fy                2026
kind              transfer_in | transfer_out | cost_shift | loan | grant | holiday | indirect_reduction | fee_change | reduction | write_off
amount            1300000
from_fund         "011"            to_fund "608"
instrument        "FY26 Budget Adoption, Item 24"        (AAO, resolution, budget adoption, consent item)
stated_reason     "Offset projected Marina Fund deficit"
recurring         false
source_url        ...
confidence        High
reviewer          "SK" / "agent:proposed"
```

Rules: a flow is recorded only with a primary source (ACFR, AAO, adopted budget, annotated agenda, staff report). Agents may *propose* flows; a person approves them before they publish (section 5.4).

### 1.3 Why this schema and not a spreadsheet

The budget is written by department; the money lives in funds; the ACFR reports by fund but not by *event*. A cost shift of $1.579M from the Marina Fund to the Parks Tax Fund appears nowhere as a line item in either document; it exists only in a B&F committee slide. (High) The flow ledger is the record that neither the budget book nor the ACFR keeps.

---

## 2. The worked example: the Marina Fund (608)

All figures below are from City documents: the FY2025 ACFR, the B&F Committee Marina Fund Update (May 22, 2025), the Waterfront Overview to the PRWC (September 9, 2026), the FY2026 budget adoption (June 24, 2025), and the FY27–28 budget. (High unless marked)

### 2.1 How the fund was set up

Established in 1964 to receive a $1.8M State loan to build the Waterfront. Revenue from berth rentals and hotel and restaurant leases "was expected to cover the costs of debt service, maintenance and operations of the entire Waterfront." The fund carries 1.8 miles of streets, 11 parking lots, 5 miles of pathways, three parks, 1,000 berths, public buildings, 13 leases, and all utilities. (High) In other words: a self-supporting enterprise charged with maintaining a public park system.

### 2.2 The structural deficit

Staff's own statement: a structural deficit "for the last 25+ years." Drivers named: the 2000 and 2008 downturns (boats pulled, restaurant and hotel revenue down), safety problems in 2015–2019 that drove a berther exodus and closed Hs Lordships, aging infrastructure with no capital reserve, and COVID. Unfunded capital need: $131M (May 2025) revised to **$163.3M** (September 2026): docks $33.4M, parking lots $17.3M, streets $15.7M, shorelines and pier $55.4M, dredging and seawall $20.2M, buildings $10.8M. (High)

FY2025 audited result: operating revenue $7.59M against operating expenses $13.57M, an **operating loss of $5.98M**, masked by a one-time $7.69M State capital grant that turned the fund's change in net position positive ($1.57M). Without the grant, FY2025 was the worst year on record. (High)

### 2.3 Every dollar moved in and out since FY2022 (the flow ledger, seeded)

| FY | Flow | Amount | From → To | Instrument | Note |
|---|---|---|---|---|---|
| 2022 | transfer_in | $1.40M | ARPA → Marina | Budget | Federal one-time money |
| 2023 | transfer_in | $1.15M | ARPA → Marina | Budget | Federal one-time money |
| 2023 | loan | $5.5M | DBW (State) → Marina | Council 7/25/2023 Item 19 | D & E dock replacement; $585K tied to a Doubletree capital contribution |
| 2024 | cost_shift | $0.80M | Marina → "other funds" | Budget | Funds not named in the slide (Unknown which) |
| 2024 | transfer_in | $5.5M | **Workers' Compensation Fund** → Marina | Budget | An internal-service fund financed marina capital projects |
| 2025 | indirect_reduction + holiday | $0.85M | Marina (charges waived) | Budget | Reduced indirect cost charge and a WC contribution "holiday" |
| 2025 | grant | $7.69M | State → Marina | ACFR | One-time capital |
| 2025 | reduction | ~$0.70M | within Marina | Staff action, spring 2025 | Fund balance exhausted; South Cove dock repair unfunded; security cut 50%; all hourly staff cut |
| 2026 | cost_shift | **$1.579M** | Marina → **Parks Tax Fund** | Measure Y (Nov 2024) | Waterfront park and landscape costs moved to the parcel tax. Staff: this alone covered the $1.1M structural deficit |
| 2026 | transfer_in | $1.30M | GF → Marina | FY26 Budget Adoption, 6/24/2025 | "Transfer to Marina Fund to Offset Projected Deficit"; funded by redirecting $2.5M of Measure U1 revenue from the Small Sites housing program |
| 2026 | transfer_in | $0.20M | GF → Marina | Consent, 11/18/2025 | $126,374 + $74,626 "FY25 GF savings to support Marina Fund deficit" (total FY26 GF subsidy $1.4M) |
| 2026 | indirect_reduction + holiday | $0.36M | Marina (charges waived) | Budget | |
| 2027–28 | reduction | $434K / $440K | within Marina | FY27–28 Budget | Waterfront Manager cut to 85%, engineer to 60%, maintenance −$100K, security/marketing −$81K; 5% of Deputy Director shifted to Parks Tax |
| 2027–28 | fee_change | +$250K/yr marina, +$100K/yr recreation, +$150–185K parking, +$75–100K Adventure Playground | users → Marina | Council, Jun 2025 and Jan 2026 | Parking fees blocked: BCDC rejected the permit; playground fee gate not installed until Oct 2026 |
| 2025–26 | write_off risk | ~$0.89M | Doubletree → Marina | Lease | Hotel stopped paying regular rent in early 2025 (the May 2025 deck says January, the Sept 2026 deck says March), paid $964,680 in Sept 2025, has paid nothing since Dec 2025. Budget assumed 35% of rent; actual 0 |

Staff's forecast (Sept 2026): ending balance $1.52M (FY26) → $0.50M (FY27) → **−$0.55M (FY28)**. Staff's stated gap: **$1.045M** in cuts or revenue, and "No General Fund available to bail out the Marina Fund." Measures under discussion: shift *all* recreation costs off the fund to the GF, more maintenance and capital cuts, more staff cuts, fee increases, higher rents from Cal Sailing and Cal Adventures. (High)

### 2.4 What the ledger shows (the finding)

1. **Six different pockets have been used to keep one fund solvent in five years**: federal ARPA, a State loan, a State grant, the Workers' Compensation internal-service fund, the General Fund, and the Parks Tax. None was the fund's own revenue. (High)
2. **The fixes have been one-time; the deficit is recurring.** Staff said so about the FY26 fix in writing. (High)
3. **The largest permanent fix was a voter measure for something else.** Measure Y was sold as a parks maintenance tax; its first-year effect includes $1.579M of Marina Fund relief. Whether the ballot language permits Waterfront park costs is a question to put to the City Attorney's analysis, not a finding here. (Moderate)
4. **The structural problem is the fund's charter, not its management.** A berth-fee enterprise was asked to maintain streets, parks, pathways and a seawall for the general public. Every rescue restates that mismatch rather than fixing it. (Moderate; this is BeTH's reading)
5. **Capital is unfunded at $163M with no reserve**, and the fund's next fix is to cut maintenance again. (High)

### 2.5 The counterargument (publish alongside)

An enterprise fund with a 25-year structural deficit has two honest outcomes: subsidize it openly or close the service. Berkeley has chosen to subsidize, and every transfer above went through a public vote of the Council. Measure Y's park-maintenance purpose arguably *does* cover Waterfront parks, which are parks. The Doubletree collapse is a Bay Area hotel-market event, not a Berkeley decision. And the alternative, letting the Waterfront fail, costs more. (Moderate) The ledger does not settle this argument; it makes it visible.

### 2.6 Open items for the Marina page

- Which "other funds" absorbed the FY2024 $800K cost shift (Unknown; ask Finance).
- Whether the $5.5M Workers' Compensation transfer was a loan or a grant, and if a loan, the repayment schedule (Unknown; not in the ACFR narrative read).
- Measure Y ballot text vs. the $1.579M Waterfront cost shift (Moderate; needs the City Attorney's impartial analysis and the ordinance).
- The FY2026 and FY2027 audited figures when the FY2026 ACFR is released (early 2027).

---

## 3. The next five funds (same schema)

| Fund | Why it is next | What the ledger will show |
|---|---|---|
| **General Fund (011)** | The deficit lives here | Transfers out ($42.0M in FY2024 to capital, pension trust, reserves); the $29.2M structural gap; the one-time plugs by year ($10M → $40M → $27M → $22M → $12M → $17M → $29M) |
| **Parks Tax Fund** | Receiving end of the Marina cost shift | Measure Y uplift vs. what it now carries; whether park maintenance capacity rose or was consumed |
| **Equipment Replacement (671)** | Auditor: "Fleet Replacement Fund Short Millions" (2021); $2.0M (FY25) and $0.5M (FY24) transferred out | Raids on a replacement fund, 11 of 12 audit recommendations still partial |
| **Workers' Compensation (internal service)** | Lent/gave $5.5M to the Marina and granted "holidays" | Internal-service funds as an off-budget lender |
| **Zero Waste (enterprise)** | −$1.5M FY2025; 18 of 27 audit recommendations dropped | The second enterprise fund heading toward the GF's door |

Each page: fund record, flow table, finding, counterargument, open items. Same house style as the Marina page.

---

## 4. All 110 funds (December)

**Source:** the ACFR's combining statements for nonmajor governmental funds, enterprise funds and internal service funds (FY2021–FY2025 ACFRs), which give revenue, expenditure, transfers in, transfers out and ending balance per fund per year. (High that the tables exist; the FY2025 ACFR is 18,000 lines of extractable text.)

**Method:** a Python extractor (`tools/acfr_funds.py`) that reads the combining statements, matches fund names to fund numbers from the budget's fund list, and writes `data/funds/*.json` annual blocks. Every row carries the ACFR page as its source. Hand-check 10% against the PDF; publish the check.

**Output:** a fund browser page: filter by type, sort by deficit, by transfers in, by restriction class; one line per fund; click through to the fund page. Funds with no flows get a stub record with annual figures only.

**Limit:** the ACFR gives totals, not events. The *event* ledger (section 1.2) is populated only for funds someone has read the agendas for. The agent pipeline (section 5) is what makes that scale.

---

## 5. The agent pipeline: following Council and commissions

### 5.1 What "real time" can mean here

Berkeley posts no RSS feed and no API. (High) What exists:

- **Council agendas page** (`/your-government/city-council/city-council-agendas`): HTML list by month with predictable PDF paths: `/sites/default/files/city-council-meetings/YYYY-MM-DD Agenda Packet - Council.pdf` and `YYYY-MM-DD Annotated Agenda - Council.pdf`. Agendas post about 12 days before a meeting; annotated agendas (the actions) post within days after. (High)
- **Commission and committee materials** under `/sites/default/files/legislative-body-meeting-agendas/` and `/legislative-body-meeting-attachments/`, linked from each commission's page. (High)
- **GovDelivery email** (topic CABERKE_18) when agendas post. (High)
- **Granicus** video and MP3 per meeting. (High)
- **City Auditor's recommendation dashboard**: a live JSON feed (already in BeTH's database `_meta`). (High)
- **Records Online** for adopted resolutions and ordinances. (High that it exists; structure not yet examined)

So "real time" means: within an hour of a posting, not during a meeting. Actions are final only in the annotated agenda. Minutes lag further and add little the annotated agenda does not have.

### 5.2 Agent roles

| Agent | Trigger | Reads | Writes |
|---|---|---|---|
| **Watcher** | Every 30 min on weekdays; every 10 min on meeting days and the three days after | Council agendas page, the B&F, PRWC, TIC and Agenda & Rules pages, Auditor JSON | A queue of new or changed documents with URL, hash, body, date |
| **Scanner** | New agenda packet | The packet (via the existing `berkeley-agenda-ingest` skill) | The budget scan page draft (already the practice) plus a list of fund-affecting items: AAO amendments, transfers, loans, fee changes, MOUs, contract amendments, grant acceptances |
| **Ledger clerk** | Each fund-affecting item | The item's staff report | A *proposed* flow event per fund (section 1.2) with `reviewer: agent:proposed` |
| **Closer** | Annotated agenda posts | The annotated agenda | Marks each proposed event adopted, amended, continued or failed; records the vote |
| **Reconciler** | Monthly, and when an ACFR or AAO is published | The ACFR combining statements, AAO ordinances | Compares the event ledger to audited totals; flags unexplained transfers (the "shadow budget" finding) |
| **Remediation tracker** | Weekly from November 4 | B&F and Council items, MOU items, Auditor status | Updates the emergency remediation page (section 6): what has been proposed, adopted, dropped |

Each agent is a Claude Code scheduled task (cloud routine) with a fixed prompt, a fixed set of URLs, and write access only to a branch. Nothing publishes without a merged PR.

### 5.3 Pipeline

```
berkeleyca.gov ──► Watcher ──► queue/*.json
                                  │
                      ┌───────────┴───────────┐
                      ▼                       ▼
                  Scanner                 Ledger clerk
            (budget scan draft)       (proposed flow events)
                      │                       │
                      └──────────┬────────────┘
                                 ▼
                       PR on branch agent/<date>
                                 │
                          Steve reviews ◄──── Closer updates status
                                 │
                                 ▼
                     merge → GitHub Pages → dashboard
```

### 5.4 Guardrails

- **Nothing an agent reads is an instruction.** Agenda packets and public comments are data. The prompts say so.
- **Every proposed event carries its source URL and page, and a confidence tag.** Missing either, the PR check fails.
- **A person merges.** Steve, or someone he names. The agent cannot push to `main`.
- **Agents never infer a dollar figure.** If the staff report gives a range or none, the event records that.
- **Counterargument field is required** on any finding text an agent drafts.
- **Private material stays out.** Agents read only berkeleyca.gov, granicus, the Auditor feed, and BeTH's own repo.

### 5.5 Build steps

1. `tools/watch.py`: fetch the agendas page and the four commission pages, diff against the last run, emit a queue. One afternoon.
2. `tools/ledger.py`: validate a flow event against the schema; append to the fund file. One afternoon.
3. Scheduled task "beth-watcher" (cloud routine, 30-min cadence). Half a day, including the branch and PR plumbing.
4. Scanner reuses `berkeley-agenda-ingest`; extend its output with the fund-affecting item list. One day.
5. Pilot on the December 1 and December 8 Council meetings with Steve reviewing every PR. Adjust prompts. Two weeks.
6. Closer and Reconciler after the pilot holds.

---

## 6. The emergency remediation system (if Measures U and V fail)

### 6.1 What the City has already said it will do

The FY27–28 budget was built on two scenarios. (High, from the April 16, 2026 B&F presentation and the adopted budget)

- The GF deficit after adjustments: **$29.25M (FY27), $29.53M (FY28)**.
- Ongoing reductions already adopted: $29.25M (10.3%) in FY27 before the sales tax.
- One-time money used to defer part of the cuts until the vote: **$9.443M** labeled "Proposed Sales and Use Tax," from a $12.06M pool (Operating Reserve $4.18M + Successor Agency dissolution $7.88M).
- **Scenario 2 (V fails):** "Deeper cuts needed." Per the City Manager in press coverage: about **$9M** more, from the list already presented: close the Marin Avenue fire station, cut police positions, Public Works and Parks staff. 33 FTE were preserved contingent on the tax. Staff would "go back to the drawing board."
- **If U fails:** no contingency is published. The CIP stays at $346M over five years against $1.5–2.1B of need, and the Vision 2050 reporting machinery again waits on a revenue measure (see the CIP hub pages).

### 6.2 What BeTH publishes on October 30

A page, `docs/emergency-remediation.html`, in two columns: **the City's Scenario 2** and **the BeTH stack**, each line with a dollar figure where a source exists, "unsized" where not, and the audit recommendation it rests on. The stack is the reform framework the site already carries (the eight mechanics and the six cross-fund channels), ordered by how fast each can produce General Fund relief:

| Tier | Measure | Source on BeTH | Sizing | Timing |
|---|---|---|---|---|
| A: this fiscal year | Re-base to actuals again (mechanic 1); the City took $16.5M out of the personnel baseline in one pass | rational-budgeting-process | Unsized for a second pass; first pass $16.5M | AAO#1, FY27 |
| A | Stop replacement-fund diversions (mechanic 7); fleet fund raids $2.5M over two years | OPP-02 | ~$1.25M/yr avoided | Immediate policy |
| A | Collect revenue owed (channel 4): lease escalators, unbilled rent, fire inspection citations, restaurant fee study | 2025 leases audit; OPP items | Unsized; Marina alone shows ~$0.9M owed by one tenant | 90 days |
| A | Full overhead recovery from restricted and enterprise funds (channel 2) | cross-fund page | Unknown recovery rate; audit-worthy | Cost allocation plan update |
| B: FY28 budget | Grant indirect-cost recovery (channel 3) on ~$55M/yr of grants; $27.6M of grant authority went unspent FY2025 | OPP-01 (all 15 recs dropped) | Unsized | FY28 |
| B | AAO discipline and carryover reform (mechanics 2–3) | rational-budgeting-process | Unsized; needs the AAO ordinances | FY28 cycle |
| B | Performance-based renewal of every program with no measure (mechanic 5) | audit crosswalk | Unsized | FY28 |
| C: bargaining | **Employee benefit cost-sharing** (mechanic 4) on GF Health/Retiree $21.9M and Pension $54.6M | Employee Benefits audit; Section 115 rec | **Unsized until MOU terms and CalPERS rates are modeled** | See 6.3 |
| Counter | The City's Scenario 2 list: fire station, police, PW, Parks | B&F 4/16/2026 | ~$9M | Immediate |

The page says plainly: Tier A and B are process fixes with mostly unverified yields; the one lever large enough to close a $29M recurring gap on its own is personnel cost, and that is bargained.

### 6.3 Union benefit negotiations: what is actually on the table and when

Contract expirations, from the City's union agreements page (High):

| Unit | Covers | Expires |
|---|---|---|
| Berkeley Fire Fighters Assn, IAFF Local 1227 | Sworn fire, non-managerial | **June 2026** (expired; status Unknown: extended or in negotiation) |
| Berkeley Chief Fire Officers Assn, Local 1227 | Sworn fire, managerial | **June 2026** (same) |
| Berkeley Fire EMS Professionals Assn | Non-managerial fire EMS | **June 2026** (same) |
| Public Employees Union Local 1 | Management, professional, engineering paraprofessional | June 2027 |
| SEIU 1021 Community Services & Part-Time Recreation | Health, welfare, library, admin, recreation | June 2027 |
| SEIU 1021 Maintenance & Clerical | Manual labor, police non-sworn, clerical | June 2027 |
| Berkeley Police Association | All sworn police | June 2028 |
| IBEW Local 1245 | Electrical | June 2028 |

What that means for remediation:
- **The only open table right now is fire**, three units, all expired in June 2026. Whatever the City is doing there is the live test of whether benefit cost-sharing is being asked for. First records request: the status of those negotiations and any tentative agreement.
- **Local 1 and both SEIU units open in 2027**: six months after the election, and the bargaining positions are set in the spring. That is the window for a Council direction on cost-sharing.
- **Police is locked until 2028**, which removes the largest single payroll from the near-term table.
- **What has to be modeled before any dollar is claimed**: current employee contribution rates for health premiums and pension (classic vs. PEPRA members), the active/retiree split inside the $21.9M Health/Retiree line, and CalPERS employer rates by plan. Sources: the MOUs (public), the Compensation Matrix (public, revised Dec 2025), CalPERS actuarial valuations (public). A one-week modeling task once the MOUs are read.
- **Honest framing on the page**: cost-sharing is bargained, cannot be booked by Council vote, and any figure before the model is a guess. The audit record (Employee Benefits: Tough Decisions Ahead; the dropped Section 115 recommendation) is the basis for asking, not for a number.

### 6.4 After November 3

If U and V pass: the page becomes "what the City promised to do with the money," tracked by the Remediation agent against the budget's own list. If either fails: the page becomes the live remediation tracker, updated weekly, with the City's actual actions (AAO amendments, station closure, layoffs, MOU items) logged as events against the stack above.

---

## 7. Data and records still needed

| Item | For | How |
|---|---|---|
| FY2026 and prior AAO ordinances | AAO drift; flow ledger | Records Online; records request |
| Measure Y ballot text and City Attorney analysis | Marina cost-shift legality question | berkeleyca.gov elections archive |
| Workers' Comp → Marina $5.5M: loan or grant, terms | Marina ledger | Finance; records request |
| Fire unit negotiation status and any TA | Remediation 6.3 | HR; Council closed-session reports |
| Current MOUs, Comp Matrix, CalPERS valuations | Benefit cost-sharing model | Public; already linked |
| Cost allocation plan and grant indirect rates | Channels 2–3 sizing | Records request |
| FY2021–FY2024 ACFRs | 110-fund time series | berkeleyca.gov |

---

## 8. What this plan does not claim

- That the Marina Fund's rescues were illegal. Every one went through Council. The claim is that they were one-time, drawn from six unrelated pockets, and that the fund's charter guarantees a repeat.
- That the BeTH stack closes $29M. Tier A and B yields are mostly unverified; the one large lever is bargained.
- That agents can report Council actions as they happen. They can report postings within the hour; actions are final at the annotated agenda.
- That 110 fund pages will be hand-written. Only funds with read agendas get event ledgers; the rest get audited annual figures until the agents catch up.

---

**Sources (primary):** FY2025 ACFR (proprietary fund statements, interfund transfer note, 10-year schedules) · B&F Committee, Marina Fund Update, May 22, 2025 · PRWC, Berkeley Waterfront Overview, September 9, 2026 (supplemental communications packet) · FY2026 Budget Update Adoption, June 24, 2025, Item 24 · Council consent, November 18, 2025, Item 8 (AAO amendment) · B&F Committee, FY27–28 Budget Update, April 16, 2026 · City union agreements page (berkeleyca.gov/your-government/jobs/union-agreements-and-employee-manuals) · Council, July 25, 2023, Item 19 (DBW loan) · BeTH: Fund Map, Cross-Fund Opportunities, Rational Budgeting Process, budget database.

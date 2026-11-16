# Budget Choices dashboard — proposed structure

**Phase 2 deliverable 6 — draft, 2026-10-23**
**Status:** Interface specification. Nothing built. No Phase 1 production file is touched by this proposal.

## Design inheritance from Phase 1

The FY2025 dashboard earned trust with a specific discipline, and Phase 2 keeps it:

- Every figure carries a fiscal year, a source and a confidence level.
- Audited and unaudited are never mixed in one total.
- Different accounting bases are never summed (fund balance ≠ net position; expenditures ≠ operating expenses).
- Gaps are drawn, never absorbed — the "not itemized" bar existed until the underlying data was fixed.
- A page that fails its own integrity checks does not publish.

Phase 2 adds a harder problem. Phase 1 reported **what happened**, from one audited source. Phase 2 reports **what could happen**, from many sources of mixed reliability. The interface must make the difference between fact and scenario impossible to miss.

## The evidence-class system

Every number on every view carries one of five badges, with a fixed colour and a fixed meaning:

| Badge | Meaning | Example |
|---|---|---|
| **AUDITED** | In an ACFR, tied to a statement column | Marina FY2025 revenue $7,594,812 |
| **BUDGET** | Adopted appropriation or approved amendment | FY2026 transfers |
| **PROJECTION** | City forecast for an unaudited year | Marina FY2028 balance −$545,586 |
| **PLANNING ESTIMATE** | Engineering/consultant estimate | Pier-ferry $103.6M–$200M+ |
| **THIRD-PARTY** | Independent analysis, attributed | Boating/non-boating split (DBW via Berkeley Decision Project) |

**Rule: a total may only sum figures of one class.** Mixed-class comparisons are shown side by side, never added. This directly prevents the FY2026 error found in reconciliation, where identical numbers were labeled "actual" in one source and "projected" in another.

## Views

### 1. Where the Money Is
Entry point. The Phase 1 fund dashboard extended forward: 106 audited funds, plus budget and projection years clearly separated by badge. Links each fund to its ledger page. **Unchanged Phase 1 content remains authoritative.**

### 2. Which Commitments Could Change
The capital portfolio: all 149 FY2027–31 projects. Filters by department, asset class, delivery stage, restriction class, district.

Each project shows the four quantities **as separate columns that never merge**: identified need · appropriation · encumbrance · expenditure. Plus `net_releasable`, which renders as **"insufficient data"** — not zero, not blank — whenever restriction research is incomplete.

Default sort is **not** by headline cost. Headline cost is the number that misleads; `net_releasable` is the number that matters.

### 3. Pause / Defer Scenarios
User selects projects and actions (cancel · defer · reduce scope · combine · continue). Output is always two panels:

- **Funds released** — net of cancellation penalties, grant clawbacks, preservation costs and deferred escalation.
- **What is given up** — safety, accessibility, environmental, equity and service impacts, plus recurring operating consequences.

**The second panel cannot be collapsed or hidden.** A scenario UI that shows only released dollars is a machine for producing irresponsible proposals.

Scenarios carry a standing banner: *a scenario is not a decision, and released funds are not available until legal transferability is confirmed.*

### 4. Funding Restrictions
The honesty view. Every fund and project by `restriction_class`, with citations. Prominently answers: **how much of the $2.1B identified need is even theoretically redirectable?**

The honest current answer is **unknown**, and the view must say so until Q11 is researched. This view is what prevents the dashboard from becoming a list of things to raid.

### 5. PCI Simulator
Locked until calibrated. Until then it displays the model framework and the calibration-data gap list, not a simulator. Once live: scenario sliders, PCI trajectory with uncertainty bands, dollars per PCI-point, condition distribution, and **"reach" vs "hold"** reported separately.

A greyed-out simulator with an honest explanation is worth more than a working one built on invented deterioration rates.

### 6. Operating Costs
Recurring consequences: payroll and benefits, the operating cost of completed capital assets, internal-service fund health. The Workers' Compensation Fund belongs here — $0 revenue, $11,983,900 expense, **−$9,752,938** net position — because it is the clearest case of a one-time budget fix creating a recurring liability.

Separates **one-time** from **recurring** savings everywhere. Conflating them is how structural deficits get declared solved.

### 7. Vision 2050 Asset Management
Adopted commitment vs delivered status, by date. Each element marked adopted / proposed / implemented / unverified. Tracks the 2022 policy's public Annual Maintenance Plan requirement, the 2025 Task Force's "incomplete" finding, the July 2027 target, and the September 29, 2026 Item 26 referral.

Surfaces the waterfront-exclusion finding (Q8) **once verified**, not before.

### 8. Trade-offs
Synthesis. Alternative policy packages side by side with full consequences. Presents options; does not recommend one. Every package shows funds released, services affected, risks accepted and deferred costs created.

## Case study pages

Long-form, in the Phase 1 fund-page style:

- **Marina Fund** — deliverable 2, ready to render once Q1 and Q3 resolve.
- **Pier-ferry** — capital estimates across six sources, the operating gap, consent-calendar governance.
- **Workers' Compensation** — the internal-service fund as budget-balancing mechanism.
- **Streets** — once PCI data exists.

## Attribution

Third-party research is credited inline, by name, with the researcher's own citation — never silently absorbed. Eric Fredericks' Berkeley Decision Project is the first such source and the pattern for the rest: *"Finding from the Berkeley Decision Project (Fredericks), citing [source]. BeTH has/has not verified this independently."*

## Build order

1. Views 1 and 4 — extend Phase 1, add restriction research. Highest trust, lowest risk.
2. View 2 — capital portfolio, read-only.
3. View 6 — operating costs; Workers' Compensation case study.
4. Case studies — Marina first.
5. View 7 — Vision 2050 tracking.
6. View 3 — scenarios, **only after restrictions are researched**.
7. View 5 — PCI simulator, **only after calibration**.

Views 3 and 5 are the ones people will ask for first and the ones that must ship last. Building them early, on incomplete restriction and pavement data, would produce confident wrong answers about public money — the precise failure Phase 1 spent its entire effort avoiding.

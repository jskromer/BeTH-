# Berkeley Event Value Twin

A reusable digital model for evaluating City of Berkeley civic events on a
consistent basis — the **Kite Festival** as its first case. It does **not** try
to prove the festival should return. It lets Berkeley compare complete, auditable
scenarios and keeps three questions that are usually conflated deliberately apart:

| Question | What it answers |
|---|---|
| **Economic impact** | How much *incremental* economic activity does the event produce? |
| **City fiscal impact** | How much does the City spend and receive (the Marina Fund line)? |
| **Public value** | What benefits and burdens fall on residents, visitors, businesses, environment? |

The central identity:

```
Net public value = incremental benefits − incremental costs − displacement − externalities
```

…but the model never collapses to one unsupported dollar figure. It keeps a
multi-dimensional scorecard (City finances, local economy, waterfront,
transportation, environment, community, distribution, risk).

> **Every number shipped here is an ILLUSTRATIVE default.** The Kite Festival last
> ran 2017–2019 (2020–2022 were COVID-disrupted and are not valid no-festival
> controls). Values are modeled or stipulated placeholders pending the data-gap
> register — none is a measured fact. See `data/seed.json` → `evidence_sources`
> and `data_gaps`.

## What's here

```
event-value-twin/
  README.md                     this file
  data/seed.json                the 12 tables, seeded: 2019-style reconstruction + 5 scenarios
  model/schema.sql              PostgreSQL/PostGIS DDL for the 12 tables
  model/event_value_twin.py     transparent engine: incrementality + IMPLAN/RIMS-II + Monte Carlo
../docs/berkeley-event-value-twin.html   the interactive dashboard (self-contained; same math in JS)
```

## Run the engine

```bash
python3 model/event_value_twin.py     # stdlib only, no dependencies
```

It prints, for each of the five scenarios, the deterministic central scorecard
plus an 80% Monte-Carlo interval and the probability that City revenue exceeds
City cost.

## The methodological commitments

1. **Incrementality, not gross spending.** For each visitor segment,
   `incremental = observed × festival_attribution × berkeley_retention`. A
   resident who would have lunched in Berkeley anyway contributes little; a
   Sacramento family that travelled for the festival contributes a lot. The model
   then subtracts **displacement** (deterred waterfront customers, crowded-out
   park users, events that can't happen).
2. **Berkeley-consistent economics.** Geography, direct/indirect/induced
   definitions, and base-year dollars match Berkeley's 2025 Creative Economy
   study (IMPLAN). We do **not** reuse that report's portfolio-wide
   "$197 catalyzed per grant dollar" as an event multiplier — it describes a
   portfolio, not one event's margin.
3. **Two multipliers, not one.** IMPLAN is primary; **BEA RIMS II** is an
   independent cross-check. The gap between them is shown, not hidden.
4. **Marina Fund accounting.** City costs use the Marina Fund chart of accounts
   and are tagged incremental-cash / allocated / avoidable / fixed / capital /
   opportunity, so an allocation is never mistaken for a true marginal cost.
5. **Uncertainty is first-class.** Triangular draws + Monte Carlo; every headline
   result carries an 80% interval. The policy read-out is honest — e.g. "expected
   to require a City subsidy while producing a larger amount of incremental local
   activity; whether that is favorable depends on the City's public-purpose and
   distributional criteria" — never simply "profitable."
6. **Physical quantities stay visible.** VMT, emissions, and waste are reported in
   physical units even when the City chooses not to monetize carbon.

## The five scenarios

1. No festival (counterfactual baseline)
2. Full festival, former operating model
3. Smaller / one-day festival
4. Full festival with managed parking, transit and sponsorship changes
5. Alternative waterfront event using the same public resources

## Recommended first policy product

*Berkeley Kite Festival: Preliminary Counterfactual Value Assessment* — with a
reconstructed 2019 account, a no-festival counterfactual, low/central/high
scenarios, and an explicit data-gap register. The recommended decision is **not**
"restore the full festival" but: *authorize a one-event pilot specification under
which sufficient data are collected to determine the event's complete fiscal,
economic, environmental and community value.*

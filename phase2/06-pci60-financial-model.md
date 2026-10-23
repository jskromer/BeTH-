# PCI 60+ financial model framework

**Phase 2 deliverable (plan item 7) — draft, 2026-10-23**
**Status:** Framework and calibration-data requirements. **No model is calibrated. No PCI outcome is projected. No deterioration rate, unit cost or available balance has been invented.**

## The chain the model must represent

```
capital reallocations ──┐
                        ├──> funds available for paving ──> treatments purchased ──> network PCI over time
recurring opex savings ─┘                   ▲
                                            │
                              paving delivery cost per lane-mile
```

Four links. Each can break independently, and each is currently uncalibrated.

## Link 1 — Funds available

Comes from `scenario_actions.net_funds_released` (deliverable 3), **not** from headline project costs. Two separate streams that must never be summed without labels:

- **One-time** — released capital balances. Buys a burst of treatment; does not sustain a PCI level.
- **Recurring** — net annual operating savings. Sustains a level; takes years to accumulate into a burst.

A PCI target needs both: one-time money to climb, recurring money to hold. Presenting a one-time release as if it sustains a PCI level is the most likely way this model misleads.

## Link 2 — Delivery cost

Cost per lane-mile by treatment type, decomposed from **actual contracts**, not from a unit-cost table:

pavement treatment · design · construction management · ADA compliance · utilities · drainage · traffic safety · environmental work · green infrastructure · discretionary scope additions.

Only this decomposition can answer whether delivery reform frees real money. **Do not presume environmental review is the primary cost driver** — that is a hypothesis to test against contract data, and a politically convenient answer that the data may not support.

Legal questions to research, not assume: CEQA Class 1 routine-maintenance exemption (14 CCR 15301) and its exceptions; ADA obligations triggered by resurfacing; procurement thresholds; local complete-streets policy; Dig Once coordination.

## Link 3 — Treatments

Per segment: current PCI · area · treatment options · unit cost · treatment life · post-treatment PCI · eligibility rules (a treatment that is valid at PCI 70 is often invalid at PCI 35).

**Preservation vs reconstruction is the crux.** Preservation on good streets buys more PCI-points per dollar; reconstruction on failed streets buys fewer points but prevents the most expensive failures. A model that optimizes network-average PCI alone will recommend abandoning the worst streets. The model must report both network average **and** the distribution, including miles below PCI 25.

## Link 4 — Deterioration

Segment-level deterioration curves by pavement type, age, traffic loading and climate.

**This is the single largest calibration risk.** Deterioration is non-linear: a street at PCI 60 falling untreated loses points slowly at first, then rapidly below about PCI 40, where the treatment required jumps from surface seal to full reconstruction at several times the cost. A linear assumption will make PCI 60 look far cheaper to reach than it is.

**Berkeley's adopted StreetSaver methodology must supply these curves.** BeTH must not substitute generic curves from literature.

## Scenarios to model (once calibrated)

1. **Current policy** — baseline, existing paving plan and funding.
2. **Capital reallocation only** — one-time released balances.
3. **Operating reform only** — recurring savings.
4. **Combined** — both streams.
5. **Delivery-cost reform** — same dollars, lower cost per lane-mile.
6. **Target-driven** — reverse-solve the annual spend to reach and hold PCI 60, 65, 70 over 5 and 10 years.

Each reports: annual spend · network PCI trajectory · miles treated by treatment type · dollars per PCI-point · distribution of segment condition · backlog of deferred reconstruction · **and an explicit uncertainty band**.

## Required outputs

- Network PCI by year, with uncertainty.
- **Reaching a target vs holding it** stated separately. These have very different funding profiles and conflating them is the most common error in public pavement debates.
- Dollars per lane-mile and per PCI-point.
- Deferred-reconstruction backlog — a PCI target met while the worst streets decay further is not a success.

## Calibration data required — none of which BeTH currently holds

| Data | Source | Status |
|---|---|---|
| Segment-level PCI, area, pavement age | StreetSaver / Public Works | **Not held.** Machine-readable form required. |
| Deterioration curves by pavement type | StreetSaver methodology | **Not held.** |
| Treatment unit costs and service lives | Recent paving contracts | **Not held.** |
| Post-treatment PCI by treatment type | StreetSaver | **Not held.** |
| Current five-year paving plan | Five-Year Street Rehabilitation plan, 2026-07-07 | **Located, not extracted.** |
| Measure FF annual allocation | Same, ~$15M/yr estimated | **Located, not extracted.** |
| Contract cost decomposition | Individual paving contracts | **Not held.** |
| Net releasable capital balances | Deliverable 3, step 3 | **Not computed.** |
| Net recurring operating savings | Payroll/benefit workstream | **Not computed.** |

**Until the first four rows exist, this model produces nothing publishable.** The honest Phase 2 output for PCI is the framework plus this gap list — not a projected PCI curve. Publishing a PCI 60 cost estimate built on generic assumptions would be the single most damaging thing BeTH could do to its credibility, because it is the number most likely to be quoted and the one BeTH is least able to defend.

## Reconciliation requirement

Any BeTH model result must be reconciled against the City's adopted paving plan and StreetSaver output, with differences explained. BeTH is not building a rival pavement model; it is making the City's own model's implications legible under alternative funding scenarios.

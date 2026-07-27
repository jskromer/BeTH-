#!/usr/bin/env python3
"""
Berkeley Event Value Twin - reference calculation engine.

A transparent, reproducible implementation of the model described in the concept:
every headline number in the dashboard can be regenerated from seed.json and this
file, with no hidden spreadsheet cells.

Design commitments carried straight from the concept:
  * Three questions kept separate: economic impact, City fiscal impact, public value.
  * Net = incremental benefits - incremental costs - displacement - externalities.
  * Spending is made INCREMENTAL before it counts:
        incremental = observed x festival_attribution x berkeley_retention
  * IMPLAN is primary (matches Berkeley's Creative Economy study); RIMS II cross-checks.
  * Uncertainty is first-class: triangular draws + Monte Carlo, 80% intervals.
  * Physical quantities (VMT, emissions, waste) stay visible even when not monetized.

Stdlib only. Run:  python3 event_value_twin.py
"""

from __future__ import annotations
import json
import math
import os
import random
import statistics
from dataclasses import dataclass, field
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
SEED_PATH = os.path.join(HERE, "..", "data", "seed.json")


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def load_seed(path: str = SEED_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def triangular(low: float, mid: float, high: float, rng: random.Random) -> float:
    """Triangular draw, degrading gracefully if low==mid==high or bounds cross."""
    lo, hi = min(low, high), max(low, high)
    if hi <= lo:
        return mid
    mode = min(max(mid, lo), hi)
    return rng.triangular(lo, hi, mode)


# --------------------------------------------------------------------------- #
# Scorecard
# --------------------------------------------------------------------------- #
@dataclass
class Scorecard:
    scenario: str
    # Local economy
    direct_incremental: float = 0.0        # Berkeley-retained incremental direct spend
    implan_output: float = 0.0
    rims2_output: float = 0.0
    value_added: float = 0.0
    labor_income: float = 0.0
    jobs: float = 0.0
    # City finances
    sales_tax: float = 0.0
    tot: float = 0.0
    vendor_fees: float = 0.0
    parking_revenue: float = 0.0
    sponsorship: float = 0.0
    service_cost: float = 0.0
    net_city_fiscal: float = 0.0           # revenue - service cost (the Marina Fund line)
    # Transportation / environment
    vehicles_peak: float = 0.0
    parking_shortfall: float = 0.0
    vmt: float = 0.0
    emissions_tons: float = 0.0
    waste_tons: float = 0.0
    transit_riders: float = 0.0
    # Distribution / per-capita
    cost_per_attendee: float = 0.0
    subsidy_per_nonresident: float = 0.0
    extras: Dict[str, float] = field(default_factory=dict)


def compute(seed: dict, scenario_id: str, draw: Dict[str, float] | None = None) -> Scorecard:
    """
    Deterministic scorecard for one scenario. `draw` optionally overrides
    stochastic inputs (used by the Monte Carlo loop); when None, central values.
    """
    draw = draw or {}
    scen = next(s for s in seed["event_scenarios"] if s["id"] == scenario_id)
    sc = Scorecard(scenario=scen["label"])

    attendance = draw.get("attendance", scen["attendance"])
    days = scen["event_days"]
    if attendance <= 0 or days <= 0:
        return sc  # no-festival baseline: all zeros

    segs = {s["id"]: s for s in seed["attendance_segments"]}
    spend = seed["visitor_spending"]["per_segment"]
    transit = scen["transit_service"]

    # ---- Local economy: incremental, Berkeley-retained direct spending ----
    total_taxable_incremental = 0.0   # feeds sales tax
    lodging_incremental = 0.0         # feeds TOT
    direct_incremental = 0.0
    for sid, seg in segs.items():
        sp = spend[sid]
        per_day = draw.get(f"spend_{sid}", sp["spend_mid"])
        attribution = sp["attribution"]
        retention = sp["retention_berkeley"]
        people = attendance * seg["share"]
        observed = people * per_day * days
        incremental = observed * attribution * retention
        direct_incremental += incremental
        total_taxable_incremental += incremental
        if sid == "night_bk":
            lodging_incremental += incremental * seed["city_revenues"]["lodging_share_of_night_bk_spend"]

    # ---- Displacement: gross incremental -> net new-to-Berkeley activity ----
    band = draw.get("_band", "central")
    displacement = seed["model_assumptions"]["displacement_share"].get(band, 0.08)
    displacement = draw.get("displacement", displacement)
    direct_incremental *= (1 - displacement)
    total_taxable_incremental *= (1 - displacement)
    lodging_incremental *= (1 - displacement)
    sc.direct_incremental = direct_incremental

    im = seed["io_multipliers"]["implan"]
    r2 = seed["io_multipliers"]["rims2"]
    sc.implan_output = direct_incremental * im["output"]
    sc.rims2_output = direct_incremental * r2["output"]
    sc.value_added = sc.implan_output * im["value_added_ratio"]
    sc.labor_income = sc.implan_output * im["labor_income_ratio"]
    sc.jobs = (sc.implan_output / 1_000_000) * im["jobs_per_million_output"]

    # ---- City finances ----
    rev = seed["city_revenues"]
    taxable = max(0.0, total_taxable_incremental - lodging_incremental)
    sc.sales_tax = taxable * rev["sales_tax_local_share"]
    sc.tot = lodging_incremental * rev["transient_occupancy_tax_rate"]
    sc.vendor_fees = draw.get("vendors_count", rev["vendors_count"]["mid"]) * rev["vendor_fee_per_vendor"]
    sc.sponsorship = draw.get("sponsorship", scen["sponsorship"])

    # Costs (Marina Fund chart of accounts)
    cost = 0.0
    for line in seed["city_service_costs"]["lines"]:
        c = draw.get(f"cost_{line['account']}", line["cost_mid"])
        if line.get("scales_with_days"):
            c *= days / 2.0
        cost += c
    if transit == "event_plus":
        addon = seed["city_service_costs"]["managed_access_addon"]
        cost += draw.get("cost_managed", addon["cost_mid"])
    sc.service_cost = cost

    # ---- Transportation ----
    ti = seed["transportation_inputs"]
    auto_share = ti["auto_mode_share"].get(transit, 0.72)
    vehicles_total = (attendance * auto_share) / ti["avg_vehicle_occupancy"]
    sc.vehicles_peak = vehicles_total * ti["peak_hour_fraction"]
    inv = seed["parking_inventory"]
    available = inv["marina_spaces"] * (1 - inv["baseline_occupancy"])
    sc.parking_shortfall = max(0.0, sc.vehicles_peak - available)
    sc.transit_riders = ti["transit_daily_riders_added"].get(transit, 0) * days

    # Parking revenue (managed scenarios only)
    if scenario_id in inv["spaces_reservable_scenarios"] and scen["parking_price"] > 0:
        parked = min(sc.vehicles_peak, available)
        sc.parking_revenue = parked * scen["parking_price"] * rev["parking_capture_rate"] * days

    # City fiscal bottom line (the Marina Fund subsidy line)
    total_revenue = sc.sales_tax + sc.tot + sc.vendor_fees + sc.parking_revenue + sc.sponsorship
    sc.net_city_fiscal = total_revenue - sc.service_cost

    # ---- Environment (physical, visible; monetization optional) ----
    env = seed["environmental_impacts"]
    vmt = 0.0
    for sid, seg in segs.items():
        people = attendance * seg["share"]
        parties = people / max(seg["party_size"], 1)
        vmt += parties * auto_share * ti["avg_roundtrip_miles_by_segment"][sid] * days
    sc.vmt = vmt
    sc.emissions_tons = (vmt * env["kg_co2_per_mile"] + env["generator_kg_co2_per_day"] * days) / 1000.0
    sc.waste_tons = (attendance * env["waste_kg_per_attendee"] * days) / 1000.0

    # ---- Distribution / per-capita ----
    nonres = attendance * (1 - segs["res"]["share"])
    sc.cost_per_attendee = sc.service_cost / attendance if attendance else 0.0
    subsidy = max(0.0, -sc.net_city_fiscal)
    sc.subsidy_per_nonresident = subsidy / nonres if nonres else 0.0
    if env.get("monetize_carbon_default"):
        sc.extras["shadow_carbon_cost"] = sc.emissions_tons * env["shadow_carbon_cost_per_ton"]

    return sc


# --------------------------------------------------------------------------- #
# Monte Carlo
# --------------------------------------------------------------------------- #
def monte_carlo(seed: dict, scenario_id: str, band: str = "central",
                runs: int | None = None, rng_seed: int = 42) -> dict:
    """Run the scenario under uncertainty; return 80% intervals on headline metrics."""
    scen = next(s for s in seed["event_scenarios"] if s["id"] == scenario_id)
    if scen["attendance"] <= 0:
        base = compute(seed, scenario_id)
        return {"scenario": scen["label"], "runs": 0, "p_fiscal_positive": 0.0,
                "metrics": {k: (0.0, 0.0, 0.0) for k in _HEADLINE}}

    ma = seed["model_assumptions"]
    runs = runs or ma["monte_carlo_runs"]
    rng = random.Random(rng_seed)
    weather_p = ma["adverse_weather_probability"].get(band, 0.18)
    haircut = ma["weather_attendance_haircut"]

    collected: Dict[str, List[float]] = {k: [] for k in _HEADLINE}
    fiscal_pos = 0

    for _ in range(runs):
        draw: Dict[str, float] = {"_band": band}
        # Attendance: triangular around scenario value, then weather haircut.
        att = triangular(scen["attendance"] * 0.7, scen["attendance"], scen["attendance"] * 1.25, rng)
        if rng.random() < weather_p:
            att *= (1 - haircut)
        draw["attendance"] = att
        # Spending per segment
        for sid, sp in seed["visitor_spending"]["per_segment"].items():
            draw[f"spend_{sid}"] = triangular(sp["spend_low"], sp["spend_mid"], sp["spend_high"], rng)
        # Costs
        for line in seed["city_service_costs"]["lines"]:
            draw[f"cost_{line['account']}"] = triangular(line["cost_low"], line["cost_mid"], line["cost_high"], rng)
        addon = seed["city_service_costs"]["managed_access_addon"]
        draw["cost_managed"] = triangular(addon["cost_low"], addon["cost_mid"], addon["cost_high"], rng)
        # Sponsorship & vendors
        draw["sponsorship"] = triangular(scen["sponsorship"] * 0.5, scen["sponsorship"], scen["sponsorship"] * 1.4, rng)
        vc = seed["city_revenues"]["vendors_count"]
        draw["vendors_count"] = triangular(vc["low"], vc["mid"], vc["high"], rng)

        sc = compute(seed, scenario_id, draw)
        for k in _HEADLINE:
            collected[k].append(getattr(sc, k))
        if sc.net_city_fiscal > 0:
            fiscal_pos += 1

    def interval(vals: List[float]):
        s = sorted(vals)
        n = len(s)
        return (s[int(0.10 * n)], statistics.median(s), s[min(int(0.90 * n), n - 1)])

    return {
        "scenario": scen["label"],
        "runs": runs,
        "p_fiscal_positive": fiscal_pos / runs,
        "metrics": {k: interval(v) for k, v in collected.items()},
    }


_HEADLINE = [
    "net_city_fiscal", "implan_output", "rims2_output", "value_added",
    "labor_income", "jobs", "vmt", "emissions_tons", "parking_shortfall",
    "cost_per_attendee", "subsidy_per_nonresident",
]


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _fmt(x: float) -> str:
    if abs(x) >= 1000:
        return f"{x:,.0f}"
    if abs(x) >= 10:
        return f"{x:,.1f}"
    return f"{x:,.2f}"


def main() -> None:
    seed = load_seed()
    print(f"\nBerkeley Event Value Twin - {seed['_meta']['case']}")
    print(seed["_meta"]["status"])
    print("=" * 78)
    for scen in seed["event_scenarios"]:
        det = compute(seed, scen["id"])
        mc = monte_carlo(seed, scen["id"], band="central", runs=2000)
        print(f"\n{scen['label']}")
        print(f"  Deterministic (central assumptions):")
        print(f"    Net City fiscal .......... ${_fmt(det.net_city_fiscal)}"
              f"   (P[revenue>cost] = {mc['p_fiscal_positive']*100:.0f}%)")
        print(f"    Incremental Berkeley sales ${_fmt(det.direct_incremental)}  direct")
        print(f"    IMPLAN output ............ ${_fmt(det.implan_output)}"
              f"   | RIMS II ${_fmt(det.rims2_output)}")
        print(f"    Value added .............. ${_fmt(det.value_added)}"
              f"   | Labor income ${_fmt(det.labor_income)}  | Jobs {_fmt(det.jobs)}")
        print(f"    Peak vehicles ............ {_fmt(det.vehicles_peak)}"
              f"   | Parking shortfall {_fmt(det.parking_shortfall)}")
        print(f"    VMT ...................... {_fmt(det.vmt)}"
              f"   | CO2 {_fmt(det.emissions_tons)} t | Waste {_fmt(det.waste_tons)} t")
        if scen["attendance"] > 0:
            print(f"    Cost/attendee ............ ${_fmt(det.cost_per_attendee)}"
                  f"   | Subsidy/nonresident ${_fmt(det.subsidy_per_nonresident)}")
        lo, md, hi = mc["metrics"]["net_city_fiscal"]
        print(f"    80% interval, net fiscal . [${_fmt(lo)} .. ${_fmt(hi)}]  median ${_fmt(md)}")
    print("\n" + "=" * 78)
    print("All figures ILLUSTRATIVE. See data/seed.json evidence_sources & data_gaps.")


if __name__ == "__main__":
    main()

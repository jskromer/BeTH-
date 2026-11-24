"""
Streets drill-down. The first class built to the floor; the shape is meant to be
cloned for the others.

Everything here is derived from the published backlog, the adopted plan's funding
level, and the escalation assumption. The two figures that would actually settle
the streets argument - what holds PCI at 56, and what reaches 70 - are not
derivable from any of that and are carried as an explicit pending block.
"""

import math


def _clearance_years(b0, spend, esc):
    """Years to clear a backlog escalating at `esc` under constant annual `spend`.

    B(t) = S/e + (B0 - S/e)e^(et).  Returns None when spend never overtakes
    escalation, which is the case worth naming rather than rendering as infinity.
    """
    if esc <= 0:
        return b0 / spend if spend > 0 else None
    if spend <= b0 * esc:
        return None
    return math.log(spend / (spend - b0 * esc)) / esc


def _spend_to_clear_in(b0, years, esc):
    """Constant annual spend that clears `b0` in `years` at escalation `esc`."""
    if esc <= 0:
        return b0 / years
    g = math.exp(esc * years)
    return b0 * esc * g / (g - 1)


def _trajectory(b0, spend, esc, years, step=1):
    """Backlog balance year by year, floored at zero."""
    out = []
    for t in range(0, years + 1, step):
        if esc <= 0:
            v = b0 - spend * t
        else:
            v = spend / esc + (b0 - spend / esc) * math.exp(esc * t)
        out.append({"year": t, "balance": max(0.0, v)})
        if v <= 0:
            break
    return out


def streets(data, spy):
    d = data
    b0 = d["backlog"]["unfunded_need"]
    esc = d["backlog"]["escalation_rate"]
    spend = d["funding"]["annual_total"]
    lane_miles = d["network"]["lane_miles"]

    accrual = b0 * esc
    net_progress = spend - accrual
    years = _clearance_years(b0, spend, esc)

    scenarios = []
    for y in d["clearance_model"]["scenario_years"]:
        s = _spend_to_clear_in(b0, y, esc)
        scenarios.append({
            "years": y,
            "annual_spend": s,
            "vs_current": s - spend,
            "multiple_of_current": s / spend,
            "is_current_pace": years is not None and abs(y - years) < 0.75,
        })

    tiers = []
    for t in d["condition"]["tiers"]:
        tiers.append(dict(t, is_current=t["low"] <= d["condition"]["value"] <= t["high"]))

    funding = sorted(d["funding"]["streams"], key=lambda s: -s["annual"])
    for s in funding:
        s = s  # streams already carry their own confidence
    dedicated = sum(s["annual"] for s in funding if s["name"] != "CIP and General Fund")

    return {
        "class_id": d["class_id"],
        "network": dict(d["network"], **{
            "replacement_per_lane_mile": d["network"]["replacement_value"] / lane_miles,
        }),
        "condition": {
            "metric": d["condition"]["metric"],
            "value": d["condition"]["value"],
            "as_of": d["condition"]["as_of"],
            "methodology": d["condition"]["methodology"],
            "tiers": tiers,
            "current_tier": next(t["label"] for t in tiers if t["is_current"]),
            "points_to_good": min(t["low"] for t in tiers if t["key"] == "good") - d["condition"]["value"],
            "peer_comparison": d["condition"]["peer_comparison"],
            "source_ids": d["condition"]["source_ids"],
        },
        "backlog": {
            "unfunded_need": b0,
            "per_lane_mile": b0 / lane_miles,
            "escalation_rate": esc,
            "accrual_per_year": accrual,
            "accrual_per_second": accrual / spy,
            "scope_note": d["backlog"]["scope_note"],
        },
        "funding": {
            "annual_total": spend,
            "per_lane_mile": spend / lane_miles,
            "dedicated": dedicated,
            "discretionary_share": (spend - dedicated) / spend,
            "streams": funding,
        },
        "arithmetic": {
            "annual_spend": spend,
            "annual_escalation": accrual,
            "net_progress_per_year": net_progress,
            "share_of_spend_lost_to_escalation": accrual / spend,
            "clearance_years": years,
            "trajectory": _trajectory(b0, spend, esc, 24),
            "scenarios": scenarios,
            "method": d["clearance_model"]["method"],
            "assumption_warning": d["clearance_model"]["assumption_warning"],
        },
        "governing_plan": d["governing_plan"],
        "related_programs": d["related_programs"],
        "targets": d["targets"],
        "source_ids": ["S1", "S3", "S4", "S14"],
    }

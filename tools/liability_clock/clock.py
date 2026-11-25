"""
Berkeley Liability Clock - accrual engine.

Standard library only, deterministic, no network. Every published figure is
produced here; the browser renders what this emits and computes nothing of
its own beyond interpolating the ticker between animation frames.

Design rules enforced in code:
  1. A component enters the live rate only when all of its inputs exist and
     carry a source id. Otherwise it is reported with status "pending" and a
     named blocking input, and contributes zero.
  2. Pension/OPEB is never summed into the capital headline.
  3. The headline rate is the sum of its parts, not a product taken over an
     aggregate. Parts must reconcile to the headline exactly.

Run:  python3 model/clock.py
"""

import json
import os
from datetime import datetime, timezone

from streets import streets

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
DATA = os.path.join(REPO, "data", "liability-clock")


def load(name):
    with open(os.path.join(DATA, name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def _usd(x):
    return "$" + format(int(round(x)), ",")


def basis_epoch_ms(date_str):
    d = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(d.timestamp() * 1000)


# --------------------------------------------------------------------------
# components
# --------------------------------------------------------------------------

def escalation(assets, assumptions):
    """Fixed backlog scope, rising construction cost. The one live component."""
    default_rate = assumptions["escalation"]["default_rate"]
    basis = assumptions["backlog_basis"]
    citywide = basis["citywide_estimate"]["point"]

    rows = []
    identified = 0
    for c in assets["classes"]:
        need = c["unfunded_need"]["point"]
        if need is None:
            rows.append({
                "id": c["id"], "name": c["name"], "need": None,
                "rate": c["escalation_rate"], "accrual_per_year": 0.0,
                "status": "no_published_need",
            })
            continue
        identified += need
        rows.append({
            "id": c["id"], "name": c["name"], "need": need,
            "rate": c["escalation_rate"],
            "accrual_per_year": need * c["escalation_rate"],
            "status": "live",
        })

    unattributed_need = citywide - identified
    unattributed = {
        "need": unattributed_need,
        "rate": default_rate,
        "accrual_per_year": unattributed_need * default_rate,
        "note": ("Citywide backlog estimate minus the classes that publish a "
                 "dollar figure. Roughly %.0f%% of the headline is not broken "
                 "out by asset class anywhere public."
                 % (100.0 * unattributed_need / citywide)),
    }

    total = sum(r["accrual_per_year"] for r in rows) + unattributed["accrual_per_year"]
    naive = citywide * default_rate

    return {
        "key": "escalation",
        "label": "Escalation",
        "status": "live",
        "what_it_measures": "The same scope of work costing more each year.",
        "formula": "sum over classes of (unfunded need x class escalation rate), plus the unattributed remainder at the default rate",
        "accrual_per_year": total,
        "rows": rows,
        "unattributed": unattributed,
        "identified_need": identified,
        "citywide_need": citywide,
        "reconciliation": {
            "sum_of_parts": total,
            "naive_product": naive,
            "delta": total - naive,
            "note": ("Sum of parts is authoritative. It differs from citywide x "
                     "default rate because IT escalates at a technology-refresh "
                     "rate rather than a construction rate."),
        },
        "source_ids": ["S1", "S2", "S11", "S12"],
    }


def deterioration(assets):
    """Assets decaying past the cheap-fix window. Needs the pavement model."""
    return {
        "key": "deterioration",
        "label": "Deterioration",
        "status": "pending",
        "what_it_measures": ("Assets falling into a more expensive repair band. "
                             "The dollar of preventive seal that becomes a "
                             "reconstruction."),
        "formula": "sum over lane-miles of (cost per lane-mile at destination PCI band minus cost at current band)",
        "accrual_per_year": 0.0,
        "blocking": ["PR1"],
        "blocking_note": ("Requires the deferral curve by PCI band from the City's "
                          "pavement management model. Not estimated."),
        "source_ids": ["S3", "S4"],
    }


def underinvestment_gap(assets):
    """Annual steady-state need minus annual funding."""
    missing = [c["id"] for c in assets["classes"]
               if c["annual_need_steady_state"] is None]
    return {
        "key": "underinvestment_gap",
        "label": "Under-investment gap",
        "status": "pending",
        "what_it_measures": "Falling behind on assets that are currently fine.",
        "formula": "sum over classes of (annual steady-state need minus annual funding)",
        "accrual_per_year": 0.0,
        "blocking": ["PR1"],
        "blocking_note": ("No class publishes a steady-state annual need. Streets "
                          "unblocks first, from the same request as deterioration."),
        "classes_missing_need": missing,
        "source_ids": ["S3"],
    }


def _plan_rollup(block):
    """Aggregate a set of plans and derive the structural accrual on the unfunded balance."""
    plans = block["plans"]
    g = lambda k: sum(p[k] for p in plans)
    unfunded = g("net_liability")
    normal_cost = g("service_cost")
    employee = g("employee_contribution")
    employer = g("employer_contribution")

    employer_normal_cost = normal_cost - employee
    amortization = employer - employer_normal_cost      # employer $ above normal cost
    interest = unfunded * block["discount_rate"]
    accrual = interest - amortization

    return {
        "label": block["label"],
        "measurement_date": block["measurement_date"],
        "discount_rate": block["discount_rate"],
        "unfunded": unfunded,
        "interest_on_unfunded": interest,
        "total_normal_cost": normal_cost,
        "employee_contribution": employee,
        "employer_normal_cost": employer_normal_cost,
        "employer_contribution": employer,
        "amortization_payment": amortization,
        "accrual_per_year": accrual,
        "direction": "shrinking" if accrual < 0 else "growing",
        "principal_reduction_rate": (-accrual / unfunded) if unfunded else None,
        "normal_cost_coverage": (employer / employer_normal_cost) if employer_normal_cost else None,
        "observed_net_change": block["observed_net_change"],
        "observed_change_note": block["observed_change_note"],
        "plans": plans,
        "locator": block["locator"],
    }


def actuarial(liabilities):
    """Interest on the unfunded pension and OPEB balance, net of the amortization payment.

    Deliberately excludes investment performance and one-time assumption or
    benefit-term changes. Those dominate any single year and tell you about the
    market, not about the funding policy. This measures the policy.
    """
    cv = liabilities["current_valuation"]
    pen = _plan_rollup(cv["pension"])
    opeb = _plan_rollup(cv["opeb"])
    total = pen["accrual_per_year"] + opeb["accrual_per_year"]

    return {
        "key": "actuarial",
        "label": "Actuarial",
        "status": "live",
        "what_it_measures": ("Interest accruing on the unfunded pension and retiree-health "
                             "balance, net of what the City pays down."),
        "formula": "(unfunded x discount rate) minus (employer contributions minus employer normal cost), summed over pension and OPEB",
        "accrual_per_year": total,
        "unfunded_total": pen["unfunded"] + opeb["unfunded"],
        "pension": pen,
        "opeb": opeb,
        "excludes": ["investment performance", "assumption changes", "benefit-term changes"],
        "excludes_note": ("Investment performance and one-time assumption or benefit-term changes "
                          "are excluded because they dominate any single year and describe the "
                          "market rather than the funding policy. Both plans' reported balances "
                          "fell far more than this figure on exactly those items, and they do "
                          "not repeat."),
        "source_ids": ["S13"],
    }


def build():
    assets = load("assets")
    assumptions = load("assumptions")
    liabilities = load("liabilities")
    pending = load("pending_requests")
    sources = load("sources")
    streets_data = load("streets")

    comps = [
        escalation(assets, assumptions),
        deterioration(assets),
        underinvestment_gap(assets),
        actuarial(liabilities),
    ]

    # Which ticker each component feeds. The actuarial component belongs to the
    # pension side and must never be summed into the capital headline; this
    # partition is the separation rule expressed in code rather than in prose.
    CAPITAL_KEYS = ("escalation", "deterioration", "underinvestment_gap")
    for c in comps:
        c["ticker"] = "capital" if c["key"] in CAPITAL_KEYS else "pension_opeb"

    def rate_for(ticker):
        return sum(c["accrual_per_year"] for c in comps
                   if c["ticker"] == ticker and c["status"] == "live")

    live = [c for c in comps if c["status"] == "live"]
    rate_year = rate_for("capital")
    spy = assumptions["clock_display"]["seconds_per_year"]

    basis = assumptions["backlog_basis"]["citywide_estimate"]
    esc = comps[0]

    tiers = {t["tier"]: t for t in assets["mandate_tiers"]}
    classes = []
    for c in assets["classes"]:
        row = next(r for r in esc["rows"] if r["id"] == c["id"])
        t = tiers[c["mandate_tier"]]
        classes.append({
            "id": c["id"],
            "name": c["name"],
            "department": c["department"],
            "scope": c["scope"],
            "condition": c["condition"],
            "unfunded_need": c["unfunded_need"]["point"],
            "need_confidence": c["unfunded_need"]["confidence"],
            "annual_funding": c["funding"]["annual_total"],
            "funding_streams": c["funding"]["streams"],
            "escalation_rate": c["escalation_rate"],
            "accrual_per_year": row["accrual_per_year"],
            "accrual_per_second": row["accrual_per_year"] / spy,
            "mandate_tier": c["mandate_tier"],
            "mandate_label": t["label"],
            "mandate_discretion": t["discretion"],
            "mandate_instrument": c["mandate_instrument"],
            "governing_plan": c["governing_plan"],
            "key_finding": c["key_finding"],
            "confidence": c["confidence"],
            "source_ids": c["source_ids"],
            "pending_inputs": c["pending_inputs"],
        })
    classes.sort(key=lambda r: (r["unfunded_need"] is None, -(r["unfunded_need"] or 0)))

    # discretion split - the field the whole argument turns on
    by_discretion = {}
    for r in classes:
        if r["unfunded_need"]:
            by_discretion.setdefault(r["mandate_discretion"], 0)
            by_discretion[r["mandate_discretion"]] += r["unfunded_need"]

    # The split above is computed only over classes that publish a dollar
    # figure, and those are disproportionately the discretionary ones. Every
    # class in the two lowest-discretion tiers - the consent-decree sewer and
    # the life-safety facilities - publishes no unfunded total at all. So the
    # split describes what is disclosed, not what is owed, and it must never
    # be presented as the latter.
    silent = [r["name"] for r in classes
              if r["unfunded_need"] is None and r["mandate_discretion"] in ("none", "low")]
    covered = sum(by_discretion.values())
    discretion = {
        "split": by_discretion,
        "covered_need": covered,
        "coverage_of_headline": covered / basis["point"],
        "mandated_classes_with_no_published_need": silent,
        "caveat": (
            "This split covers %s of the %s headline. Read it as a disclosure "
            "pattern, not a statement of what is optional: the classes under "
            "an enforceable order or a life-safety obligation (%s) publish no "
            "unfunded figure at all, so they contribute zero here while being "
            "the least discretionary spending the City has."
            % (_usd(covered), _usd(basis["point"]), ", ".join(silent))
        ),
    }

    cv = liabilities["current_valuation"]
    hist = liabilities["historical_series"]
    act = [c for c in comps if c["key"] == "actuarial"][0]
    pen_rate = rate_for("pension_opeb")

    return {
        "_meta": {
            "title": "Berkeley Liability Clock",
            "version": "0.2.0",
            "generated_by": "model/clock.py",
            "reproduce": "python3 model/build.py",
            "warning": ("Phase 1. Two of four accrual components are live. "
                        "Figures are the City's own, recompiled; they have not "
                        "been through external review."),
        },
        "page_updated": assumptions["page_updated"],
        "basis_date": assumptions["basis_date"],
        "basis_epoch_ms": basis_epoch_ms(assumptions["basis_date"]),
        "seconds_per_year": spy,

        "capital": {
            "label": "Deferred capital and maintenance",
            "backlog": basis,
            "backlog_alternates": {
                "cip_headline": assumptions["backlog_basis"]["cip_headline"],
                "identified_by_class": assumptions["backlog_basis"]["identified_by_class"],
            },
            "conflict_note": assumptions["backlog_basis"]["conflict_note"],
            "comparability_warning": assumptions["backlog_basis"]["comparability_warning"],
            "published_estimates": sorted(assumptions["backlog_basis"]["published_estimates"],
                                          key=lambda e: e["value"]),
            "rate_per_year": rate_year,
            "rate_per_second": rate_year / spy,
            "live_components": [c["key"] for c in comps
                                if c["ticker"] == "capital" and c["status"] == "live"],
            "excludes": "actuarial - that accrues on the pension ticker and is never folded in here",
        },

        "pension_opeb": {
            "label": "Pension + retiree health, unfunded",
            "as_reported": cv["as_reported"],
            "basis_epoch_ms": basis_epoch_ms(assumptions["actuarial_basis_date"]),
            "unfunded": cv["combined_unfunded"],
            "pension_unfunded": cv["pension"]["net_liability_total"],
            "opeb_unfunded": cv["opeb"]["net_liability_total"],
            "rate_per_year": pen_rate,
            "rate_per_second": pen_rate / spy,
            "status": "live",
            "detail": {"pension": act["pension"], "opeb": act["opeb"]},
            "measurement_date_note": cv["measurement_date_note"],
            "history": {
                "label": hist["label"],
                "basis": hist["basis"],
                "series": hist["series"],
                "comparability_warning": hist["comparability_warning"],
                "caveat": hist["caveat"],
                "source_ids": hist["source_ids"],
            },
            "source_ids": ["S13"],
        },

        "separation_rule": assumptions["separation_rule"],
        "components": comps,
        "classes": classes,
        "unattributed": esc["unattributed"],
        "discretion": discretion,
        "capital_backlog_series": liabilities["capital_backlog_series"],
        "drilldowns": {
            "streets": streets(streets_data, spy),
            "_note": ("One class built to the floor. The others carry summary depth only; "
                      "the streets shape is the template for cloning them."),
            "_built": ["streets"],
        },
        "programs": assets["programs"],
        "mandate_tiers": assets["mandate_tiers"],
        "pending_requests": pending["requests"],
        "assumptions": assumptions,
        "sources": sources["sources"],
    }


def summarize(m):
    def d(x):
        return "$" + format(int(round(x)), ",")
    out = []
    out.append("BERKELEY LIABILITY CLOCK - model v%s" % m["_meta"]["version"])
    out.append("basis date %s" % m["basis_date"])
    out.append("")
    out.append("CAPITAL BACKLOG")
    out.append("  headline      %s  (band %s - %s)" % (
        d(m["capital"]["backlog"]["point"]),
        d(m["capital"]["backlog"]["low"]),
        d(m["capital"]["backlog"]["high"])))
    out.append("  accrual       %s / yr   =   $%.4f / sec" % (
        d(m["capital"]["rate_per_year"]), m["capital"]["rate_per_second"]))
    out.append("")
    out.append("COMPONENTS")
    for c in m["components"]:
        if c["status"] == "live":
            out.append("  [LIVE   ] %-20s %s / yr" % (c["label"], d(c["accrual_per_year"])))
        else:
            out.append("  [PENDING] %-20s blocked on %s" % (c["label"], ",".join(c["blocking"])))
    out.append("")
    out.append("BY CLASS")
    for r in m["classes"]:
        need = d(r["unfunded_need"]) if r["unfunded_need"] else "not published"
        out.append("  %-34s %16s   %-22s %s" % (
            r["name"], need, r["mandate_label"],
            d(r["accrual_per_year"]) + "/yr" if r["accrual_per_year"] else ""))
    out.append("  %-34s %16s" % ("not attributed to any class", d(m["unattributed"]["need"])))
    out.append("")
    out.append("DISCRETION SPLIT (of published need only)")
    tot = sum(m["discretion"]["split"].values())
    for k in ["none", "low", "medium", "high"]:
        if k in m["discretion"]["split"]:
            v = m["discretion"]["split"][k]
            out.append("  %-8s %16s   %5.1f%%" % (k, d(v), 100.0 * v / tot))
    out.append("  covers %.0f%% of the headline backlog" % (100.0 * m["discretion"]["coverage_of_headline"]))
    out.append("  CAVEAT: no published need for %s" % ", ".join(m["discretion"]["mandated_classes_with_no_published_need"]))
    out.append("")
    po = m["pension_opeb"]
    out.append("PENSION + OPEB (separate ticker, never summed into the above)")
    out.append("  unfunded      %s   as carried %s" % (d(po["unfunded"]), po["as_reported"]))
    out.append("    pension     %s" % d(po["pension_unfunded"]))
    out.append("    OPEB        %s" % d(po["opeb_unfunded"]))
    sign = "+" if po["rate_per_year"] >= 0 else "-"
    out.append("  accrual       %s%s / yr   =   %s$%.4f / sec" % (
        sign, d(abs(po["rate_per_year"])), sign, abs(po["rate_per_second"])))
    for k in ("pension", "opeb"):
        r = po["detail"][k]
        out.append("    %-8s interest %s  amortization %s  ->  %s / yr  (%s)" % (
            k, d(r["interest_on_unfunded"]), d(r["amortization_payment"]),
            d(r["accrual_per_year"]), r["direction"]))
    out.append("")
    st = m["drilldowns"]["streets"]
    a = st["arithmetic"]
    out.append("STREETS DRILL-DOWN")
    out.append("  PCI %d (%s), %d points below Good" % (
        st["condition"]["value"], st["condition"]["current_tier"], st["condition"]["points_to_good"]))
    out.append("  backlog       %s   (%s / lane-mile)" % (
        d(st["backlog"]["unfunded_need"]), d(st["backlog"]["per_lane_mile"])))
    out.append("  spend         %s / yr" % d(a["annual_spend"]))
    out.append("  escalation    %s / yr  -  %.1f%% of every dollar spent" % (
        d(a["annual_escalation"]), 100 * a["share_of_spend_lost_to_escalation"]))
    out.append("  net progress  %s / yr  ->  clears the CURRENT backlog in %.1f yrs" % (
        d(a["net_progress_per_year"]), a["clearance_years"]))
    out.append("  targets       PENDING (%s): %s" % (
        st["targets"]["blocking"], ", ".join(k for k, v in st["targets"]["fields"].items() if v is None)))
    out.append("")
    out.append("OPEN DATA REQUESTS: %d" % len(m["pending_requests"]))
    for p in m["pending_requests"]:
        out.append("  %-5s %-12s %s" % (p["id"], p["status"], p["item"]))
    return "\n".join(out)


if __name__ == "__main__":
    print(summarize(build()))

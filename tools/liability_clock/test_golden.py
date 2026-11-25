"""
Golden-file and invariant tests. Run: python3 model/test_golden.py

These are the checks that make the published number defensible. Any change to
the data layer that breaks one of them is a change to a published claim.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clock import build, load  # noqa: E402

FAIL = []


def check(name, cond, detail=""):
    if cond:
        print("  PASS  %s" % name)
    else:
        print("  FAIL  %s  %s" % (name, detail))
        FAIL.append(name)


def main():
    m = build()
    assets = load("assets")
    src_ids = {s["id"] for s in load("sources")["sources"]}
    req_ids = {r["id"] for r in load("pending_requests")["requests"]}

    print("GOLDEN VALUES")
    identified = sum(c["unfunded_need"]["point"] for c in assets["classes"]
                     if c["unfunded_need"]["point"])
    check("identified need ties to source workbook ($941,100,000)",
          identified == 941_100_000, identified)
    check("unattributed = citywide - identified ($858,900,000)",
          m["unattributed"]["need"] == 858_900_000, m["unattributed"]["need"])
    check("capital accrual = $71,774,000 / yr",
          m["capital"]["rate_per_year"] == 71_774_000, m["capital"]["rate_per_year"])
    check("capital accrual = $2.2744 / sec",
          abs(m["capital"]["rate_per_second"] - 2.27438) < 0.0001,
          m["capital"]["rate_per_second"])

    print("\nRECONCILIATION")
    esc = m["components"][0]
    parts = sum(r["accrual_per_year"] for r in esc["rows"]) + esc["unattributed"]["accrual_per_year"]
    check("sum of parts equals published headline rate",
          abs(parts - m["capital"]["rate_per_year"]) < 1e-6)
    check("every live component lands on exactly one ticker",
          all(c["ticker"] in ("capital", "pension_opeb") for c in m["components"]))
    check("the two ticker rates together account for every live component",
          abs((m["capital"]["rate_per_year"] + m["pension_opeb"]["rate_per_year"])
              - sum(c["accrual_per_year"] for c in m["components"]
                    if c["status"] == "live")) < 1e-6)
    check("every pending component contributes exactly zero",
          all(c["accrual_per_year"] == 0 for c in m["components"] if c["status"] == "pending"))

    print("\nSEPARATION RULE")
    check("actuarial feeds the pension ticker, not the capital one",
          [c for c in m["components"] if c["key"] == "actuarial"][0]["ticker"] == "pension_opeb")
    check("capital rate excludes every non-capital component",
          m["capital"]["rate_per_year"] ==
          sum(c["accrual_per_year"] for c in m["components"]
              if c["ticker"] == "capital" and c["status"] == "live"))
    check("pension ticker rate equals the actuarial component exactly",
          m["pension_opeb"]["rate_per_year"] ==
          [c for c in m["components"] if c["key"] == "actuarial"][0]["accrual_per_year"])
    check("the two tickers carry separate basis dates",
          m["pension_opeb"]["basis_epoch_ms"] != m["basis_epoch_ms"])
    check("current nominal figures are kept apart from the inflation-adjusted history",
          "comparability_warning" in m["pension_opeb"]["history"])

    print("\nACTUARIAL")
    cv = load("liabilities")["current_valuation"]
    act = [c for c in m["components"] if c["key"] == "actuarial"][0]
    check("pension unfunded ties to the sum of the three CalPERS plans ($641,063,018)",
          m["pension_opeb"]["pension_unfunded"] == 641_063_018 ==
          sum(p["net_liability"] for p in cv["pension"]["plans"]))
    check("OPEB unfunded ties to the sum of the three plans ($43,388,889)",
          m["pension_opeb"]["opeb_unfunded"] == 43_388_889 ==
          sum(p["net_liability"] for p in cv["opeb"]["plans"]))
    check("combined unfunded = $684,451,907",
          m["pension_opeb"]["unfunded"] == 684_451_907)
    check("pension accrual is negative (amortization exceeds interest)",
          act["pension"]["accrual_per_year"] < 0, act["pension"]["accrual_per_year"])
    check("OPEB accrual is positive (contributions below normal cost)",
          act["opeb"]["accrual_per_year"] > 0, act["opeb"]["accrual_per_year"])
    check("combined actuarial accrual = $344,207 / yr",
          round(act["accrual_per_year"]) == 344_207, act["accrual_per_year"])
    check("the accrual excludes investment performance and one-time changes",
          set(act["excludes"]) == {"investment performance", "assumption changes",
                                   "benefit-term changes"})

    print("\nPROVENANCE")
    check("every asset class carries at least one source id",
          all(c["source_ids"] for c in m["classes"]))
    bad = [c["id"] for c in m["classes"] if not set(c["source_ids"]) <= src_ids]
    check("every class source id resolves in the register", not bad, bad)
    bad = [c["key"] for c in m["components"] if not set(c.get("source_ids", [])) <= src_ids]
    check("every component source id resolves in the register", not bad, bad)
    bad = [c["key"] for c in m["components"]
           if c["status"] == "pending" and not set(c["blocking"]) <= req_ids]
    check("every pending component names a real open request", not bad, bad)
    open_ids = {r["id"] for r in m["pending_requests"] if r["status"] != "resolved"}
    bad = [c["key"] for c in m["components"]
           if c["status"] == "pending" and not set(c["blocking"]) <= open_ids]
    check("no pending component is blocked on an already-resolved request", not bad, bad)
    check("PR2 is recorded as resolved",
          [r for r in m["pending_requests"] if r["id"] == "PR2"][0]["status"] == "resolved")
    check("every class with no published need is flagged, not zeroed",
          all(c["unfunded_need"] is not None or c["need_confidence"] == "low"
              for c in m["classes"]))

    print("\nSTREETS DRILL-DOWN")
    st = m["drilldowns"]["streets"]
    sa = st["arithmetic"]
    sd = load("streets")
    check("funding streams sum to the published annual total ($18,000,000)",
          sum(x["annual"] for x in st["funding"]["streams"]) == 18_000_000 ==
          st["funding"]["annual_total"])
    check("streets escalation matches the class row in the stack",
          sa["annual_escalation"] ==
          [c for c in m["classes"] if c["id"] == "streets"][0]["accrual_per_year"])
    check("escalation consumes 55.6% of annual spend",
          abs(sa["share_of_spend_lost_to_escalation"] - 0.5556) < 0.001,
          sa["share_of_spend_lost_to_escalation"])
    check("current backlog clears in 20.3 years at current spend",
          abs(sa["clearance_years"] - 20.27) < 0.05, sa["clearance_years"])
    check("the 20-year scenario reproduces roughly the current spend",
          abs([x for x in sa["scenarios"] if x["years"] == 20][0]["annual_spend"]
              - sa["annual_spend"]) < 200_000)
    check("trajectory starts at the published backlog and never goes negative",
          sa["trajectory"][0]["balance"] == 250_000_000
          and all(p["balance"] >= 0 for p in sa["trajectory"]))
    check("every pending target carries an explanation of what it unblocks",
          all(k in st["targets"]["what_each_unblocks"] and st["targets"]["what_each_unblocks"][k]
              for k in st["targets"]["fields"]))
    check("every pavement target is still null",
          all(v is None for v in st["targets"]["fields"].values()))
    check("targets block names PR1 and PR1 is still open",
          st["targets"]["blocking"] == "PR1" and
          [r for r in m["pending_requests"] if r["id"] == "PR1"][0]["status"] != "resolved")
    check("the clearance model warns that it holds scope constant",
          "not" in sa["assumption_warning"] and "good" in sa["assumption_warning"])
    check("no peer PCI ranking is asserted",
          st["condition"]["peer_comparison"]["status"] == "unavailable")
    check("streets drill-down is the only one built",
          m["drilldowns"]["_built"] == ["streets"])

    import datetime
    pu = m["page_updated"]
    check("the page carries an updated date",
          bool(pu) and len(pu) == 10)
    check("the updated date is not in the future",
          datetime.date.fromisoformat(pu) <= datetime.date.today(), pu)
    check("the updated date is not before the figures it describes",
          datetime.date.fromisoformat(pu) >= datetime.date.fromisoformat(m["basis_date"]))

    print("\nHONESTY GUARDS")
    check("the three conflicting backlog totals are all retained",
          m["capital"]["backlog"]["point"] == 1_800_000_000
          and m["capital"]["backlog_alternates"]["cip_headline"]["point"] == 2_100_000_000
          and m["capital"]["backlog_alternates"]["identified_by_class"]["point"] == 941_100_000)
    est = m["capital"]["published_estimates"]
    check("every published citywide estimate carries a source and a date",
          all(e.get("source") and e.get("date") and e.get("source_ids") for e in est))
    check("the selected estimate is the one the clock runs on",
          [e for e in est if e.get("selected")][0]["value"] == m["capital"]["backlog"]["point"])
    check("the estimate series spans $882M to $2.1B",
          est[0]["value"] == 882_000_000 and est[-1]["value"] == 2_100_000_000, len(est))
    check("the series warns that scope and base year differ",
          "scope" in m["capital"]["comparability_warning"].lower())
    check("streets carries an adopted PCI target with no published cost",
          st["targets"]["published_target"]["value"] == "more than 70"
          and st["targets"]["published_target"]["target_year"] is None
          and st["targets"]["fields"]["reach_pci_70_annual"] is None)
    check("Measure U is recorded as approved, not proposed",
          not any("Proposed $300M" in s_["name"]
                  for c in m["classes"] for s_ in c["funding_streams"]))
    check("discretion split declares its coverage of the headline",
          m["discretion"]["coverage_of_headline"] < 1.0
          and "caveat" in m["discretion"])
    check("mandated classes with no published need are named",
          len(m["discretion"]["mandated_classes_with_no_published_need"]) > 0)

    print("")
    if FAIL:
        print("FAILED: %d" % len(FAIL))
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()

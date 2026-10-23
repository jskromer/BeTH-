#!/usr/bin/env python3
"""Build the financial dashboard (docs/dashboard.html) from every ledger in data/funds.

Usage:  python3 tools/build_dashboard.py           # writes docs/dashboard.html
        python3 tools/build_dashboard.py --check   # exit 1 if the page is stale or an integrity problem exists

When and how the page is regenerated, and what CI checks: tools/DASHBOARD.md.

Read-only over the ledgers. Every figure on the page is either an audited value
from a fund file, a sum of such values, or arithmetic on them (labeled
"derived"). Interpretations come only from curated ledgers and are labeled.

Rules the page enforces:
- Governmental fund balance and proprietary net position are never added together.
- Transfers are never counted as revenue; they are shown as movement between funds.
- Internal service revenue is shown apart: it is mostly charges to other City funds.
- A year's group totals are shown only when every fund in the group has an
  audited statement row for that year; otherwise they are withheld and the
  coverage is shown. Totals are compared with the statement's own Total column
  (data/dashboard/statement-totals.json) and the result is printed beside them.
- A line-item gap is explained on the page only while it equals the amount
  documented in data/dashboard/known-gaps.json; otherwise a generic note shows.
- An audited row without an ending balance, or with a `series` other than a fund
  statement, is not a statement row (e.g. Marina's FY2015-2023 ten-year-schedule
  rows); it stays on the fund page and out of every total here.
New audited years appear automatically when their rows are in data/funds and
this script is re-run.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data/funds"
CONTROLS = ROOT / "data/dashboard/statement-totals.json"
FIDUCIARY = ROOT / "data/dashboard/fiduciary-funds.json"
KNOWN_GAPS = ROOT / "data/dashboard/known-gaps.json"
FUND_CHECK = ROOT / "data/dashboard/fund-statement-check.json"
REGISTRY = ROOT / "data/curation/protected-ledgers.json"
OUT = ROOT / "docs/dashboard.html"

GROUPS = {
    "governmental": {"label": "Governmental funds", "basis": "Modified accrual",
                     "balance": "Fund balance", "rev": "Total revenues", "exp": "Total expenditures",
                     "exp_note": "includes capital outlay and debt service"},
    "enterprise": {"label": "Enterprise funds", "basis": "Full accrual",
                   "balance": "Net position", "rev": "Operating revenues", "exp": "Operating expenses",
                   "exp_note": "includes depreciation; excludes non-operating items"},
    "internal_service": {"label": "Internal service funds", "basis": "Full accrual",
                         "balance": "Net position", "rev": "Operating revenues", "exp": "Operating expenses",
                         "exp_note": "includes depreciation and claims; revenue is mostly charges to other City funds"},
}
TYPE_LABEL = {"general": "General", "special_revenue": "Special revenue", "capital_project": "Capital project",
              "debt_service": "Debt service", "enterprise": "Enterprise", "internal_service": "Internal service"}
STATEMENT_LABEL = {"major": "Governmental funds statement (major)", "nonmajor": "Nonmajor combining statements",
                   "proprietary": "Proprietary funds statement", "isf": "Internal service combining statement"}
# label variants in flow_detail that name the same statement line
REV_MERGE = {"donations": "Private contributions and donations", "Investment income/ (loss)": "Investment income"}
EXP_MERGE = {"Highway and streets": "Highways and streets", "Culture-recreation": "Culture and recreation",
             "Capital outlay:": "Capital outlay"}
NOT_SPENDING = re.compile(r"^(Transfers out|Payment to refunded bond escrow agent|Interest expense|State loan interest)")
# At inception of a lease or subscription (GASB 87/96) a governmental fund records an
# expenditure, within capital outlay, and an other financing source of the same amount.
# No cash moves. Reported separately so capital outlay is not read as cash spending.
LEASE_INCEPTION = "Inception of leases and subscriptions"
CAPITAL_OUTLAY = "Capital outlay"
NOT_OPERATING_REVENUE = {"Investment earnings"}
BOILERPLATE_Q = "Only FY2025 is loaded"
MAG = [(1e6, "under $1M"), (1e7, "$1M–$10M"), (1e8, "$10M–$100M"), (float("inf"), "$100M or more")]
BEGIN_NOTE = re.compile(r"Beginning balance (-?[\d,]+)")


def group_of(ftype):
    return ftype if ftype in ("enterprise", "internal_service") else "governmental"


def page_url(fid):
    return "fund-608-marina.html" if fid == "608" else f"fund-{fid}.html"


def is_statement_row(y):
    return (y.get("basis") == "audited" and y.get("series") in (None, "fund-statement")
            and y.get("balance_version") in (None, "original") and y.get("ending_balance") is not None
            and isinstance(y.get("fy"), int))


def statement_of(d, y2025):
    g = group_of(d["type"])
    if g == "enterprise":
        return "proprietary"
    if g == "internal_service":
        return "isf"
    text = (y2025 or {}).get("note", "") + " " + d["sources"].get((y2025 or {}).get("source", ""), {}).get("title", "")
    m = re.search(r"p\.(\d+)", text)
    return "major" if m and m.group(1) == "77" else "nonmajor"


def magnitude(rev, exp):
    v = max(abs(rev or 0), abs(exp or 0))
    for limit, label in MAG:
        if v < limit:
            return label
    return MAG[-1][1]


def fund_model(d, protected):
    fid = d["fund_number"]
    rows = {y["fy"]: y for y in d["annual"] if is_statement_row(y)}
    other = sorted({y["fy"] for y in d["annual"] if y.get("basis") == "audited" and not is_statement_row(y)})
    y25 = rows.get(2025)
    years = {}
    for fy, y in sorted(rows.items()):
        rev, exp = y.get("revenue"), y.get("expenditure")
        ti, to = y.get("transfers_in") or 0, y.get("transfers_out") or 0
        rec = {"rev": rev, "exp": exp, "ti": ti, "to": to, "bal": y["ending_balance"], "nonop": y.get("nonoperating"),
               "result": rev - exp if rev is not None and exp is not None else None, "net_transfers": ti - to,
               "source": y.get("source"), "confidence": y.get("confidence")}
        m = BEGIN_NOTE.search(y.get("note") or "")
        rec["begin"] = int(m.group(1).replace(",", "")) if m else None
        rec["change"] = rec["bal"] - rec["begin"] if rec["begin"] is not None else None
        rec["mag"] = magnitude(rev, exp)
        years[fy] = rec
    fd = d.get("flow_detail") or {}
    ties = None
    if fd.get("fy") in years:
        yr = years[fd["fy"]]
        own = sum(i["amount"] for i in fd.get("inflows", []) if i.get("kind") == "own" and i["line"] not in NOT_OPERATING_REVENUE)
        spend = sum(o["amount"] for o in fd.get("outflows", []) if not NOT_SPENDING.match(o["line"]))
        ties = {"fy": fd["fy"], "rev_gap": (yr["rev"] or 0) - own, "exp_gap": (yr["exp"] or 0) - spend}
    flows = d.get("flows", [])
    status = d.get("status", {})
    curated = fid in protected
    questions = [q for q in status.get("open_questions", []) if not q.startswith(BOILERPLATE_Q)]
    return {
        "id": fid, "name": d["name"], "type": d["type"], "group": group_of(d["type"]),
        "statement": statement_of(d, y25), "page": page_url(fid), "curated": curated,
        "years": years, "other_series_years": other,
        "flows_reviewed": sum(1 for f in flows if not str(f.get("reviewer", "")).startswith("agent:")),
        "flows_proposed": sum(1 for f in flows if str(f.get("reviewer", "")).startswith("agent:")),
        "line_items": ties,
        "legal_basis_known": d.get("legal_basis") not in (None, "", "Not yet researched"),
        "reading": ({"structural_deficit": status.get("structural_deficit"), "years_in_deficit": status.get("years_in_deficit")}
                    if curated else None),
        "open_questions": questions if curated else [],
        "flow_detail": fd,
    }


def build_model(data_dir=DATA_DIR, controls_path=CONTROLS, fiduciary_path=FIDUCIARY, registry_path=REGISTRY,
                known_gaps_path=KNOWN_GAPS, fund_check_path=FUND_CHECK):
    protected = set(json.loads(Path(registry_path).read_text())["ledgers"])
    funds = [fund_model(json.loads(p.read_text()), protected) for p in sorted(Path(data_dir).glob("*.json"))]
    controls = json.loads(Path(controls_path).read_text())["years"]
    fiduciary = json.loads(Path(fiduciary_path).read_text())
    known_gaps = json.loads(Path(known_gaps_path).read_text())["years"]
    fund_check = json.loads(Path(fund_check_path).read_text())
    for f in funds:
        f["audit_match"] = audit_match(f, fund_check)
    members = {g: [f for f in funds if f["group"] == g] for g in GROUPS}
    all_years = sorted({fy for f in funds for fy in f["years"]})
    years = {}
    for fy in all_years:
        ctrl = controls.get(str(fy))
        tol = (ctrl or {}).get("rounding_tolerance", 0)
        ygroups = {}
        for g, fs in members.items():
            have = [f for f in fs if fy in f["years"]]
            entry = {"funds": len(fs), "covered": len(have), "complete": len(have) == len(fs)}
            if entry["complete"]:
                tot = {k: sum(f["years"][fy][k] or 0 for f in have) for k in ("rev", "exp", "ti", "to", "bal")}
                if g != "governmental":
                    tot["nonop"] = sum(f["years"][fy]["nonop"] or 0 for f in have)
                entry["totals"] = tot
                c = (ctrl or {}).get("groups", {}).get(g)
                if c is None:
                    entry["check"] = {"status": "unreconciled", "diffs": {}}
                else:
                    keymap = {"rev": "revenue", "exp": "expenditure", "ti": "transfers_in", "to": "transfers_out",
                              "bal": "ending_balance", "nonop": "nonoperating"}
                    diffs = {k: tot[k] - c["values"][keymap[k]] for k in tot if keymap[k] in c["values"]}
                    worst = max((abs(v) for v in diffs.values()), default=0)
                    entry["check"] = {"status": "ties" if worst == 0 else ("rounding" if worst <= tol else "mismatch"),
                                      "diffs": diffs, "pages": c["pages"], "column": c["column"], "statement": c["statement"]}
            ygroups[g] = entry
        complete_all = all(e["complete"] for e in ygroups.values())
        ti = sum(f["years"][fy]["ti"] for f in funds if fy in f["years"])
        to = sum(f["years"][fy]["to"] for f in funds if fy in f["years"])
        years[fy] = {"groups": ygroups, "complete": complete_all,
                     "transfers": {"in": ti, "out": to, "diff": ti - to} if complete_all else None,
                     "flows": flows_for(funds, fy, known_gaps.get(str(fy))) if complete_all else None}
    default = max((fy for fy, y in years.items() if y["complete"]), default=max(all_years))
    history = [f for f in funds if len(f["years"]) > 1 or f["other_series_years"]]
    return {"funds": funds, "years": years, "default_year": default, "history": history,
            "fiduciary": fiduciary, "controls": controls, "fund_check": fund_check,
            "gap_audit": gap_audit(funds, known_gaps)}


def audit_match(f, check):
    """Whether the fund's figures still equal the column the independent statement check found."""
    fy = check["fy"]
    rec = check["funds"].get(f["id"])
    y = f["years"].get(fy)
    if y is None:
        return {"fy": fy, "status": "no row"}
    if rec is None or rec["status"] != "matched":
        return {"fy": fy, "status": "unmatched"}
    current = [y["rev"], y["exp"], y["ti"], -y["to"], y["bal"]]
    return {"fy": fy, "status": "matched" if current == rec["values"] else "changed", "pages": rec["pages"]}


def gap_audit(funds, known_gaps):
    """Line-item gaps that are not documented to the dollar, and documented gaps that no longer exist.

    An undocumented gap means captured line items no longer add up to an audited
    total; it fails the tests so lost lines cannot pass unnoticed. A stale entry
    means the extractor now captures the lines; it fails only the dashboard's
    own check, so the note is removed in the next dashboard rebuild."""
    undocumented, stale, documented = [], [], []
    for f in funds:
        li = f["line_items"]
        if not li:
            continue
        doc = (known_gaps.get(str(li["fy"])) or {}).get("funds", {}).get(f["id"])
        if li["rev_gap"]:
            undocumented.append({"id": f["id"], "fy": li["fy"], "kind": "revenue", "gap": li["rev_gap"]})
        if li["exp_gap"]:
            if doc and doc["gap"] == li["exp_gap"]:
                documented.append({"id": f["id"], "fy": li["fy"], "gap": li["exp_gap"]})
            else:
                undocumented.append({"id": f["id"], "fy": li["fy"], "kind": "expenditure", "gap": li["exp_gap"]})
    present = {(g["id"], g["fy"]) for g in documented}
    for fy, entry in known_gaps.items():
        for fid, doc in entry.get("funds", {}).items():
            if (fid, int(fy)) not in present:
                stale.append({"id": fid, "fy": int(fy), "documented_gap": doc["gap"]})
    return {"undocumented": undocumented, "stale": stale, "documented": documented}


def flows_for(funds, fy, known=None):
    """Governmental revenue by source and spending by function, from flow_detail, for one year.

    A documented gap (data/dashboard/known-gaps.json) is attached only when the
    fund's gap equals the documented amount exactly."""
    rev, exp, gaps, financing = {}, {}, [], {}
    for f in funds:
        if f["group"] != "governmental" or f["flow_detail"].get("fy") != fy:
            continue
        for i in f["flow_detail"].get("inflows", []):
            line = REV_MERGE.get(i["line"], i["line"])
            if i.get("kind") == "own":
                rev[line] = rev.get(line, 0) + i["amount"]
            elif i.get("kind") == "financing":
                financing[line] = financing.get(line, 0) + i["amount"]
        for o in f["flow_detail"].get("outflows", []):
            if NOT_SPENDING.match(o["line"]):
                continue
            line = EXP_MERGE.get(o["line"], o["line"])
            exp[line] = exp.get(line, 0) + o["amount"]
        li = f["line_items"]
        if li and li["exp_gap"]:
            doc = ((known or {}).get("funds") or {}).get(f["id"])
            gaps.append({"id": f["id"], "name": f["name"], "gap": li["exp_gap"],
                         "lines": doc["lines"] if doc and doc["gap"] == li["exp_gap"] else None})
    explained = {}
    for g in gaps:
        for line, v in (g["lines"] or {}).items():
            explained[line] = explained.get(line, 0) + v
    all_explained = bool(gaps) and all(g["lines"] for g in gaps)
    return {"revenue": sorted(rev.items(), key=lambda kv: -kv[1]), "spending": sorted(exp.items(), key=lambda kv: -kv[1]),
            "not_itemized": sum(g["gap"] for g in gaps), "gaps": sorted(gaps, key=lambda g: -g["gap"]),
            "explained": sorted(explained.items(), key=lambda kv: -kv[1]) if all_explained else None,
            "cause": (known or {}).get("cause") if all_explained else None,
            "cause_page": (known or {}).get("source_page") if all_explained else None,
            "function_totals": (known or {}).get("function_totals", {}) if all_explained else {},
            "financing": sorted(financing.items(), key=lambda kv: -kv[1]),
            "noncash_capital": noncash_capital(exp, financing)}


def noncash_capital(exp, financing):
    """Capital outlay split into the lease/subscription inception part and the cash part.

    None when nothing was recognized at inception. `inception` is taken from the
    other-financing-source line, which the statement reports at the same amount as
    the expenditure it is paired with."""
    inception = financing.get(LEASE_INCEPTION, 0)
    outlay = exp.get(CAPITAL_OUTLAY, 0)
    if not inception:
        return None
    return {"inception": inception, "outlay": outlay, "cash": outlay - inception}


# ---------------------------------------------------------------- rendering

def esc(s):
    return html.escape(str(s)) if s is not None else ""


def money(n, short=False):
    if n is None:
        return "—"
    a = abs(n)
    s = (f"${a/1e9:.2f}B" if a >= 1e9 else f"${a/1e6:.1f}M" if a >= 1e6 else f"${a/1e3:.0f}K" if a >= 1e3 else f"${a:,.0f}") if short else f"${a:,.0f}"
    return f"−{s}" if n < 0 else s


def chip(kind, text=None):
    labels = {"audited": "Audited", "derived": "Derived", "reading": "BeTH reading", "open": "Open question",
              "ties": "Ties to statement", "rounding": "Ties within rounding", "balanced": "Balanced", "documented": "Gap documented", "mismatch": "Does not tie",
              "unreconciled": "Not reconciled", "withheld": "Incomplete: withheld", "pending": "Not yet checked"}
    return f'<span class="chip k-{kind}">{esc(text or labels[kind])}</span>'


def check_text(entry):
    c = entry.get("check")
    if not c:
        return ""
    if c["status"] == "unreconciled":
        return f'{chip("unreconciled")} <span class="cap-i">No control total recorded for this year.</span>'
    d = {k: v for k, v in c["diffs"].items() if v}
    names = {"rev": "revenue", "exp": "spending", "ti": "transfers in", "to": "transfers out", "bal": "balance", "nonop": "non-operating"}
    detail = "every figure matches" if not d else "; ".join(f"{names[k]} {'+' if v > 0 else '−'}${abs(v):,}" for k, v in d.items())
    return (f'{chip(c["status"])} <span class="cap-i">Sum of fund columns vs the statement\'s "{esc(c["column"])}" column, '
            f'ACFR p.{esc(c["pages"])}: {detail}.</span>')


def bars(items, total, cls, note_items=()):
    vmax = max([v for _, v in items] + [v for _, v in note_items] + [1])
    out = []
    for label, v in list(items) + list(note_items):
        extra = " gap" if (label, v) in note_items else ""
        out.append(f'<div class="br{extra}" title="{esc(label)}: {money(v)} ({v/total*100:.1f}% of {money(total, True)})">'
                   f'<span class="bl">{esc(label)}</span><span class="bt"><span class="bf {cls}{extra}" style="width:{v/vmax*100:.2f}%"></span></span>'
                   f'<span class="bv">{money(v, True)}</span></div>')
    return "".join(out)


def render_group_panel(g, entry, fy):
    G = GROUPS[g]
    head = (f'<div class="gp g-{g}"><div class="gh"><span class="sw"></span><h3>{G["label"]}</h3>'
            f'<span class="basis">{G["basis"]} · {entry["funds"]} funds</span></div>')
    if not entry["complete"]:
        return head + (f'<p class="withheld">{chip("withheld")} {entry["covered"]} of {entry["funds"]} funds have an audited '
                       f'FY{fy} statement row. Totals are not shown until every fund in the group is loaded.</p></div>')
    t = entry["totals"]
    tiles = [(G["rev"], t["rev"], "audited"), (G["exp"], t["exp"], "audited"),
             ("Transfers in", t["ti"], "audited"), ("Transfers out", t["to"], "audited"),
             (f'{G["balance"]}, June 30, {fy}', t["bal"], "audited")]
    if "nonop" in t:
        tiles.insert(2, ("Non-operating, net", t["nonop"], "audited"))
    tl = "".join(f'<div class="tile"><div class="tv">{money(v, True)}</div><div class="tk">{esc(k)}</div></div>' for k, v, _ in tiles)
    return head + f'<div class="tiles">{tl}</div><p class="cap">{"Expenditures" if g == "governmental" else "Operating expenses"} {G["exp_note"]}. Sums of the fund columns, before the statement\'s own eliminations.</p><p class="chk">{check_text(entry)}</p></div>'


def render_flows(fl, gov_total_exp, fy):
    rev_total = sum(v for _, v in fl["revenue"])
    partial = {line for line, _ in (fl["explained"] or [])}
    spend_items = [(f"{k} (partial: see note)" if k in partial else k, v) for k, v in fl["spending"]]
    gap = fl["not_itemized"]
    note = [("Not itemized in BeTH's extract", gap)] if gap else []
    gaps = "; ".join(f'<a href="{page_url(g["id"])}">{esc(g["name"])}</a> {money(g["gap"], True)}' for g in fl["gaps"])
    if fl["explained"]:
        parts = "; ".join(f"{esc(k)} {money(v)}" + (f" (the statement's total for this function across all governmental funds is {money(fl['function_totals'][k])})" if k in fl["function_totals"] else "")
                          for k, v in fl["explained"])
        gap_note = (f'<p class="cap"><b>Not itemized ({money(gap)}):</b> {gaps}. The missing lines, read from ACFR p.{esc(fl["cause_page"])}: {parts}. '
                    f'Why: {esc(fl["cause"])} The audited totals are correct; this is an extraction gap, reported to the extraction pipeline.</p>')
    elif gap:
        gap_note = (f'<p class="cap"><b>Not itemized ({money(gap)}):</b> total expenditures for these funds exceed the expenditure lines the extractor captured: {gaps}. '
                    'The totals are audited; the missing lines are an extraction gap, not an unexplained loss.</p>')
    else:
        gap_note = ""
    fin = ", ".join(f"{esc(k)} {money(v, True)}" for k, v in fl["financing"])
    nc = fl.get("noncash_capital")
    lease_note = ""
    if nc and nc["outlay"]:
        lease_note = (f'<p class="cap"><b>Capital outlay is not all cash.</b> Of the {money(nc["outlay"])} shown above as capital outlay, '
                      f'{money(nc["inception"])} is the inception of leases and subscriptions: when the City signs a lease or a software '
                      f'subscription, the accounting rules (GASB 87 and 96) record the whole multi-year commitment at once as an expenditure '
                      f'and, in the same amount, as an other financing source. No cash moves, and the matching liability is on the City\'s books. '
                      f'Capital spending actually funded in {"FY%d" % fy} was {money(nc["cash"])}. '
                      f'The {money(nc["inception"])} appears in both the chart above and the financing line below; it is not counted twice '
                      f'in any total, because expenditures and other financing sources are separate sections of the statement.</p>')
    return f'''
    <div class="flowgrid">
      <div class="fc"><h3>Money in: governmental revenue by source</h3><p class="sub">{money(rev_total)} {chip("audited")} Line items from each fund's statement column. Transfers in are not here.</p>
        <div class="bars">{bars(fl["revenue"], rev_total, "g-governmental")}</div></div>
      <div class="fc"><h3>Money out: governmental expenditures by function</h3><p class="sub">{money(gov_total_exp)} {chip("audited")} Includes capital outlay and debt service. Transfers out are not here.</p>
        <div class="bars">{bars(spend_items, gov_total_exp, "g-governmental", note)}</div>
        {gap_note}{lease_note}</div>
    </div>
    <p class="cap">Other financing sources (not revenue, not shown above): {fin or "none"}. Proprietary funds are shown by fund in the table below, because their line items use different categories (operating revenue lines and expense objects; Marina's are hand-curated).</p>'''


def render_transfers(model, fy):
    yr = model["years"][fy]
    t = yr["transfers"]
    rows = []
    vmax = max(max(e["totals"]["ti"], e["totals"]["to"]) for e in yr["groups"].values())
    for g, e in yr["groups"].items():
        ti, to = e["totals"]["ti"], e["totals"]["to"]
        net = ti - to
        rows.append(f'<div class="tr g-{g}"><span class="tl2"><span class="sw"></span>{GROUPS[g]["label"]}</span>'
                    f'<span class="tb"><span class="lab">in</span><span class="bt"><span class="bf g-{g}" style="width:{ti/vmax*100:.2f}%"></span></span><span class="bv">{money(ti, True)}</span></span>'
                    f'<span class="tb"><span class="lab">out</span><span class="bt"><span class="bf g-{g} out" style="width:{to/vmax*100:.2f}%"></span></span><span class="bv">{money(to, True)}</span></span>'
                    f'<span class="net">net {"+" if net >= 0 else "−"}{money(abs(net), True)}</span></div>')
    status = "balanced" if t["diff"] == 0 else "mismatch"
    return f'''<div class="trw">{"".join(rows)}</div>
    <p class="chk">{chip(status, None if t["diff"] == 0 else "Unbalanced")} <span class="cap-i">Across all {len(model["funds"])} funds, transfers in {money(t["in"])} and transfers out {money(t["out"])}: difference {money(t["diff"])}. Transfers move money between City funds; they add none. That is why they are excluded from revenue and spending everywhere on this page.</span></p>
    <p class="cap">Which fund paid which is in the ACFR's interfund transfers note, not yet extracted; this view shows each group's side of the ledger only.</p>'''


def render_isf(model, fy):
    yr = model["years"][fy]
    e = yr["groups"]["internal_service"]
    if not e["complete"]:
        return f'<p class="withheld">{chip("withheld")} Needs every internal service fund loaded for FY{fy}.</p>'
    t = e["totals"]
    isfs = [f for f in model["funds"] if f["group"] == "internal_service" and fy in f["years"]]
    unbilled = [f for f in isfs if f["years"][fy]["rev"] == 0 and (f["years"][fy]["exp"] or 0) > 0]
    ub = "; ".join(f'<a href="{f["page"]}">{esc(f["name"])}</a>: operating revenue $0, operating expenses {money(f["years"][fy]["exp"])}, transfers in {money(f["years"][fy]["ti"])}' for f in unbilled)
    return f'''<div class="isf"><p>Internal service funds (fleet, building maintenance, central services, IT, workers' compensation, liability, catastrophic loss, leave payouts, computer replacement) are the City billing itself. A department pays the fund a charge, which the department's fund records as an expenditure or expense; the internal service fund records the same dollars as operating revenue. This page handles them in four ways:</p>
  <ol>
    <li><b>Never added to the other groups.</b> The {money(t["rev"], True)} of internal service operating revenue {chip("audited")} is mostly charges already inside the governmental and enterprise figures; adding it would count those dollars twice. It has its own panel in section 1, and no figure on this page sums it with another group.</li>
    <li><b>Their costs are shown as their own.</b> Internal service operating expenses ({money(t["exp"], True)}) are what fleet, IT, claims and the rest actually cost. When charges equal costs, the departments' expenditures already carry them. When they differ, the fund's net position absorbs the difference.</li>
    <li><b>Charges and costs can diverge.</b> {("In FY" + str(fy) + " these funds billed no charges while incurring costs: " + ub + ". Their costs that year were met by transfers in or from their own balances, not by charges to the funds whose departments incurred them " + chip("derived") + ".") if unbilled else "In FY" + str(fy) + " every internal service fund billed some charges."}</li>
    <li><b>Transfers are transfers.</b> Money moved into or out of an internal service fund (in {money(t["ti"], True)}, out {money(t["to"], True)}) is in section 3 with every other transfer, never in revenue or expenses.</li>
  </ol>
  <p class="cap">The government-wide statements fold most internal service activity into governmental activities and eliminate the internal charges; this page reads the fund statements, where they are reported separately.</p></div>'''


def render_table(model, fy):
    rows = []
    for f in model["funds"]:
        y = f["years"].get(fy)
        if not y:
            continue
        G = GROUPS[f["group"]]
        status = ["curated" if f["curated"] else "extracted", "history" if len(f["years"]) > 1 else "single"]
        li = f["line_items"]
        li_ok = li is not None and li["fy"] == fy and li["rev_gap"] == 0 and li["exp_gap"] == 0
        if li is not None and li["fy"] == fy and not li_ok:
            status.append("lines-gap")
        if y["result"] is not None and y["result"] < 0:
            status.append("rev-below")
        if y["bal"] < 0:
            status.append("neg-bal")
        am = f["audit_match"]
        if am["fy"] == fy:
            status.append("audit-" + am["status"])
            amc = {"matched": f'<span class="ok" title="Revenue, expenditure, both transfers and the ending balance match one column of ACFR p.{esc(am.get("pages"))}, read independently">matches p.{esc(am.get("pages"))}</span>',
                   "changed": '<span class="bad">changed since check</span>', "unmatched": '<span class="bad">no matching column</span>'}.get(am["status"], "—")
        else:
            amc = '<span class="dim">not checked</span>'
            status.append("audit-unchecked")
        badges = (' <span class="bdg cur">ledger</span>' if f["curated"] else "") + \
                 (f' <span class="bdg his">{len(f["years"])} yrs</span>' if len(f["years"]) > 1 else "")
        if li is None or li["fy"] != fy:
            lis = '<span class="dim">—</span>'
        elif li_ok:
            lis = '<span class="ok">ties</span>'
        else:
            parts = [f"{n} {money(v, True)}" for n, v in (("rev", li["rev_gap"]), ("spend", li["exp_gap"])) if v]
            lis = f'<span class="warn" title="Line items minus the fund total">gap: {"; ".join(parts)}</span>'
        d = {"id": f["id"], "name": f["name"].lower(), "group": f["group"], "type": f["type"], "mag": y["mag"],
             "status": " ".join(status), "rev": y["rev"] or 0, "exp": y["exp"] or 0, "res": y["result"] or 0,
             "net": y["net_transfers"], "bal": y["bal"], "chg": y["change"] if y["change"] is not None else ""}
        attrs = " ".join(f'data-{k}="{esc(v)}"' for k, v in d.items())
        rows.append(
            f'<tr {attrs}><td class="cx"><input type="checkbox" class="cmp" aria-label="compare {esc(f["name"])}"></td>'
            f'<td class="fn"><a href="{esc(f["page"])}">{esc(f["name"])}</a>{badges}<div class="st">{esc(TYPE_LABEL[f["type"]])} · {esc(STATEMENT_LABEL[f["statement"]])}</div></td>'
            f'<td class="n">{money(y["rev"])}</td><td class="n">{money(y["exp"])}</td>'
            f'<td class="n {"neg" if (y["result"] or 0) < 0 else ""}">{money(y["result"])}</td>'
            f'<td class="n">{money(y["net_transfers"]) if y["net_transfers"] else "—"}</td>'
            f'<td class="n {"neg" if y["bal"] < 0 else ""}">{money(y["bal"])}<div class="st">{G["balance"].lower()}</div></td>'
            f'<td class="n">{money(y["change"]) if y["change"] is not None else "<span class=dim>—</span>"}</td>'
            f'<td>{amc}</td><td>{lis}</td></tr>')
    return f'''<div class="tw"><table class="ft"><thead><tr><th class="cx" aria-label="compare"></th><th data-k="name">Fund</th>
      <th data-k="rev" data-num>Revenue</th><th data-k="exp" data-num title="Governmental: expenditures. Proprietary: operating expenses">Expenditures / expenses</th><th data-k="res" data-num title="Revenue minus expenditures or expenses, before transfers">Result</th>
      <th data-k="net" data-num title="Transfers in minus transfers out">Net transfers</th><th data-k="bal" data-num>Balance, June 30, {fy}</th>
      <th data-k="chg" data-num title="Ending minus beginning balance, where the beginning balance was recorded">Change</th><th title="Independent check against the statement page">Audit match</th><th>Line items</th></tr></thead>
      <tbody>{"".join(rows)}</tbody></table></div>'''


def render_year(model, fy):
    yr = model["years"][fy]
    panels = "".join(render_group_panel(g, e, fy) for g, e in yr["groups"].items())
    if yr["complete"]:
        gov_exp = yr["groups"]["governmental"]["totals"]["exp"]
        flows = render_flows(yr["flows"], gov_exp, fy)
        transfers = render_transfers(model, fy)
    else:
        flows = f'<p class="withheld">{chip("withheld")} Money-flow views need every governmental fund loaded for FY{fy}.</p>'
        transfers = f'<p class="withheld">{chip("withheld")} The transfer balance check needs every fund loaded for FY{fy}.</p>'
    covered = sum(1 for f in model["funds"] if fy in f["years"])
    return f'''<section class="yr" data-year="{fy}"{"" if fy == model["default_year"] else " hidden"}>
  <h2 id="totals-{fy}"><span class="no">1</span>What the FY{fy} audit reports, by accounting basis</h2>
  <p class="lede">Three groups, kept apart. Governmental funds measure current financial resources (fund balance); enterprise and internal service funds measure everything they own and owe, including capital assets and long-term debt (net position). Those balances are different quantities, so this page never adds them together. Internal service revenue is mostly what other City funds pay for fleet, IT, insurance and buildings; adding it to the other groups would count the same dollars twice.</p>
  <div class="gpw">{panels}</div>
  <h2 id="flows-{fy}"><span class="no">2</span>Where governmental money came from and went</h2>
  {flows}
  <h2 id="transfers-{fy}"><span class="no">3</span>Transfers between funds</h2>
  {transfers}
  <h2 id="isf-{fy}"><span class="no">4</span>How internal service funds are handled</h2>
  {render_isf(model, fy)}
  <h2 id="funds-{fy}"><span class="no">5</span>Every fund, FY{fy}</h2>
  <p class="lede">{covered} of {len(model["funds"])} funds have an audited FY{fy} statement row. Each name links to the fund's ledger page. Revenue and expenditures/expenses follow the fund's basis (see the terms above); result is revenue minus expenditures or expenses, before transfers {chip("derived")}; change is ending minus beginning balance where the beginning balance was recorded {chip("derived")}. Tick up to four funds to compare them.</p>
  <div class="controls" role="group" aria-label="filter funds">
    <input type="search" class="f-q" placeholder="fund name" aria-label="filter by name">
    <select class="f-g" aria-label="category"><option value="">all categories</option>{"".join(f'<option value="g:{g}">{G["label"]}</option>' for g, G in GROUPS.items())}{"".join(f'<option value="t:{k}">· {v}</option>' for k, v in TYPE_LABEL.items())}</select>
    <select class="f-m" aria-label="size"><option value="">any size</option>{"".join(f'<option>{l}</option>' for _, l in MAG)}</select>
    <select class="f-s" aria-label="reporting status"><option value="">any status</option><option value="curated">curated ledger</option><option value="extracted">extracted figures only</option><option value="history">more than one audited year</option><option value="single">one audited year</option><option value="lines-gap">line items do not tie</option><option value="audit-matched">matches its statement column</option><option value="audit-changed">changed since the statement check</option><option value="audit-unchecked">not checked against a statement</option><option value="rev-below">revenue below spending</option><option value="neg-bal">negative balance</option></select>
    <span class="count" aria-live="polite"></span>
  </div>
  <div class="cmpbox" hidden></div>
  {render_table(model, fy)}
  <p class="cap">Size is the larger of revenue and expenditures/expenses. "Audit match": the fund's revenue, expenditures or expenses, transfers in, transfers out and ending balance were found together in one column of the statement page, by a check that reads the PDF independently of the extractor (<code>tools/verify_fund_statements.py</code>). "Line items" compares the itemized lines on the fund's money-flow page with its audited totals: "ties" means they add up exactly; a gap means some statement lines were not captured (the audited total is still correct). Governmental fund balance and proprietary net position appear in one column for navigation only; the column is not summed.</p>
</section>'''


def render_static(model):
    years = sorted(model["years"])
    coverage_rows = []
    for fy in years:
        yr = model["years"][fy]
        cells = "".join(f'<td>{e["covered"]} / {e["funds"]}</td>' for e in yr["groups"].values())
        st = "complete" if yr["complete"] else "partial: totals withheld"
        coverage_rows.append(f'<tr><td>FY{fy}</td>{cells}<td>{st}</td></tr>')
    hist = []
    for f in model["history"]:
        yrs = sorted(f["years"])
        other = f["other_series_years"]
        extra = f'; FY{other[0]}–FY{other[-1]} from the ten-year statistical schedule (no balance), on the fund page only' if other else ""
        hist.append(f'<li><a href="{f["page"]}">{esc(f["name"])}</a>: statement years FY{", FY".join(map(str, yrs))}{extra}</li>')
    funds = model["funds"]
    n = len(funds)
    single = sum(1 for f in funds if len(f["years"]) == 1)
    ties = sum(1 for f in funds if f["line_items"] and f["line_items"]["rev_gap"] == 0 and f["line_items"]["exp_gap"] == 0)
    matched = sum(1 for f in funds if f["audit_match"]["status"] == "matched")
    ga = model["gap_audit"]
    known = sum(1 for f in funds if f["legal_basis_known"])
    ledgers = sum(1 for f in funds if f["flows_reviewed"])
    curated = [f for f in funds if f["curated"]]
    readings = []
    for f in curated:
        r = f["reading"] or {}
        sd = r.get("structural_deficit")
        qs = "".join(f"<li>{esc(q)}</li>" for q in f["open_questions"])
        readings.append(
            f'<div class="rd"><h4><a href="{f["page"]}">{esc(f["name"])}</a></h4>'
            f'<p>{chip("reading")} {"Structural deficit" if sd else "No structural deficit"}: {esc(r.get("years_in_deficit") or "")}</p>'
            f'<p class="dim">{f["flows_reviewed"]} dated flow events, each checked by a person against a primary source.</p>'
            + (f'<details><summary>{chip("open")} {len(f["open_questions"])} open questions</summary><ul>{qs}</ul></details>' if qs else "")
            + '</div>')
    fid = model["fiduciary"]
    fgroups = []
    for g in fid["groups"].values():
        items = "".join(f'<li>{esc(x["name"])} <span class="dim">· {esc(x["kind"])}{" · described as " + esc(x["description_name"]) if x.get("description_name") else ""}</span></li>' for x in g["funds"])
        fgroups.append(f'<div class="fg"><h4>{esc(g["label"])} ({len(g["funds"])})</h4><p class="dim">ACFR statements pp.{esc(g["statement_pages"])}; descriptions p.{esc(g["description_page"])}</p><ul>{items}</ul></div>')
    n_fid = sum(len(g["funds"]) for g in fid["groups"].values())
    d = model["years"][model["default_year"]]
    recon = [
        ("Group totals vs each statement's own Total column", "; ".join(f'{GROUPS[g]["label"].lower()}: ' + (f'largest difference ${max(abs(v) for v in e["check"]["diffs"].values()):,}' if any(e["check"]["diffs"].values()) else "exact") for g, e in d["groups"].items() if e.get("check")), "rounding" if any(e.get("check", {}).get("status") == "rounding" for e in d["groups"].values()) else "ties", f"FY{model['default_year']}; checked by tests/test_dashboard.py in CI"),
        ("Transfers in equal transfers out across all funds", money(d["transfers"]["diff"]) + " difference" if d["transfers"] else "—", "balanced" if d["transfers"] and d["transfers"]["diff"] == 0 else "mismatch", f"FY{model['default_year']}; an internal check, no statement total needed"),
        ("Each fund's figures match its audited statement column", f"{matched} of {n} funds (revenue, expenditures or expenses, transfers in and out, ending balance)", "ties" if matched == n else "mismatch", f"Read independently of the extractor; FY{model['fund_check']['fy']}; tests/test_dashboard_sources.py re-reads the PDF in CI"),
        ("Fund line items add up to fund totals",
         f"{ties} of {n} funds tie" + (f"; {len(ga['documented'])} gaps documented to the dollar ({money(sum(g['gap'] for g in ga['documented']))})" if ga["documented"] else "") + (f"; {len(ga['undocumented'])} undocumented" if ga["undocumented"] else ""),
         "documented" if not ga["undocumented"] and ga["documented"] else ("ties" if not ga["undocumented"] else "mismatch"),
         "Totals are audited either way. Any undocumented gap fails the test suite" + (", and any gap is called out at the top of the page and in section 2" if (ga["documented"] or ga["undocumented"]) else "")),
        ("Fund balance roll-forward (beginning + change = ending)", "not computed here", "pending", "Belongs to the extraction pipeline's reconciliation (FY2024 pilot)"),
        ("Cross-year continuity and restatements", "not computed here", "pending", "Needs a second complete year; FY2025 opening balances were restated for some funds"),
        ("Fund identity across years", "FY2025 names are the ids", "pending", "Historical identity table not yet built"),
    ]
    rrows = "".join(f'<tr><td>{esc(a)}</td><td>{chip(c)}</td><td>{esc(b)}</td><td class="dim">{esc(e)}</td></tr>' for a, b, c, e in recon)
    return f'''
  <h2 id="facts"><span class="no">6</span>Fact, reading, open question</h2>
  <p class="lede">Every number above is {chip("audited")} (read from the ACFR fund statements) or {chip("derived")} (arithmetic on audited numbers: sums, revenue minus spending, net transfers, change in balance). BeTH's interpretations appear only for the {len(curated)} funds whose ledgers a person has read and reviewed, and are labeled {chip("reading")}. What the records do not yet answer is labeled {chip("open")}. For the other {n - len(curated)} funds there is no reading: the page shows the audited figures and nothing else.</p>
  <div class="rdw">{"".join(readings)}</div>
  <h2 id="coverage"><span class="no">7</span>Coverage and completeness</h2>
  <div class="tw"><table class="cov"><thead><tr><th>Year</th>{"".join(f"<th>{G['label']}</th>" for G in GROUPS.values())}<th>Status</th></tr></thead><tbody>{"".join(coverage_rows)}</tbody></table></div>
  <p class="cap">Funds with an audited statement row for each year. A year's totals and flows appear when every fund in a group is loaded; until then the fund rows show but the totals are withheld.</p>
  <div class="stats">
    <div class="stat"><div class="v">{single}</div><div class="l">funds with FY2025 only</div></div>
    <div class="stat"><div class="v">{len(model["history"])}</div><div class="l">funds with more than one audited year</div></div>
    <div class="stat"><div class="v">{ledgers}</div><div class="l">funds with a reviewed event ledger</div></div>
    <div class="stat"><div class="v">{known}</div><div class="l">funds with legal basis researched</div></div>
  </div>
  <h3>Funds with history</h3><ul class="hist">{"".join(hist)}</ul>
  <h3>Reconciliation status</h3>
  <div class="tw"><table class="rec"><thead><tr><th>Check</th><th>Status</th><th>Result</th><th>Note</th></tr></thead><tbody>{rrows}</tbody></table></div>
  <h2 id="fiduciary"><span class="no">8</span>The {n_fid} funds without records yet: fiduciary</h2>
  <p class="lede">The Fund Map counts {n + n_fid} funds: the {n} above plus {n_fid} fiduciary funds. Fiduciary funds hold money for others (retirees, special districts, business improvement districts, the school district's Measure H tax), report on their own statements, and are left out of the government-wide totals. None has a record in BeTH's data yet, so none is in any figure on this page. Names are as the statement column headings print them.</p>
  <div class="fgw">{"".join(fgroups)}</div>'''


CSS = """
  :root{ --navy:#2a3340; --slate:#3f4f63; --steel:#43698f; --steel-deep:#33567a; --paper:#f5f7f9; --card:#fff; --rule:#dde3ea; --rule-strong:#c3ccd6; --muted:#5d6b7a; --red:#a8322c; --hi:#2f6f57; --mod:#956613; --low:#a8322c; --unk:#6b7280; --maxw:1180px;
         --s-gov:#2a78d6; --s-ent:#eb6834; --s-isf:#1baf7a; --s-gap:#9aa3ad; }
  *{box-sizing:border-box} body{ margin:0; background:var(--paper); color:var(--navy); font-family:"Source Serif 4",Georgia,serif; font-size:17px; line-height:1.55; }
  .wrap{ max-width:var(--maxw); margin:0 auto; padding:0 20px; } a{ color:var(--steel-deep); }
  .hubbar{ background:var(--slate); color:#eef1f5; } .hubbar-in{ max-width:var(--maxw); margin:0 auto; padding:11px 20px; display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; }
  .hubbar a.back{ font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:#cdd6e0; text-decoration:none; } .hubbar .stamp{ font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; color:#9fb0c1; }
  .masthead{ padding:40px 0 20px; border-bottom:2px solid var(--navy); } .eyebrow{ font-size:11.5px; letter-spacing:.16em; text-transform:uppercase; color:var(--steel-deep); margin-bottom:14px; }
  h1{ font-size:clamp(1.7rem,5vw,2.6rem); line-height:1.08; margin:0 0 .35em; } .dek{ color:var(--muted); max-width:72ch; margin:0 0 14px; }
  h2{ font-size:1.3rem; margin:44px 0 10px; display:flex; gap:10px; align-items:baseline; } h2 .no{ font-size:.8rem; color:var(--muted); border:1px solid var(--rule-strong); padding:0 7px; border-radius:2px; }
  h3{ font-size:1.02rem; margin:22px 0 8px; } h4{ font-size:.98rem; margin:0 0 6px; }
  .lede{ max-width:78ch; margin:0 0 14px; } .cap, .cap-i{ font-size:12.5px; color:var(--muted); line-height:1.5; } .cap{ margin:8px 0 0; max-width:90ch; } .dim{ color:var(--muted); }
  .scope{ background:var(--card); border:1px solid var(--rule-strong); border-left:4px solid var(--mod); padding:12px 16px; margin:16px 0 4px; font-size:.92rem; max-width:90ch; }
  .yearbar{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:18px 0 0; font-size:13px; } .yearbar select{ font:inherit; padding:6px 8px; border:1px solid var(--rule-strong); background:var(--card); }
  .legend{ display:flex; flex-wrap:wrap; gap:8px 14px; margin:12px 0 0; font-size:12.5px; color:var(--muted); align-items:center; }
  .chip{ display:inline-block; font-size:10.5px; letter-spacing:.04em; text-transform:uppercase; padding:1px 6px; border:1px solid currentColor; border-radius:2px; white-space:nowrap; vertical-align:1px; font-weight:600; }
  .k-audited{ color:var(--navy); } .k-derived{ color:var(--steel-deep); border-style:dotted; } .k-reading{ color:#6a3d9a; } .k-open{ color:var(--mod); }
  .k-ties{ color:var(--hi); } .k-balanced{ color:var(--hi); } .k-ties::before, .k-rounding::before, .k-balanced::before{ content:"✓ "; } .k-rounding{ color:var(--hi); } .k-mismatch{ color:var(--low); } .k-mismatch::before{ content:"✕ "; }
  .k-unreconciled, .k-withheld, .k-pending, .k-documented{ color:var(--mod); } .k-documented::before{ content:"! "; } .k-unreconciled::before, .k-withheld::before, .k-pending::before{ content:"◷ "; }
  .gpw{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:14px; }
  .gp{ background:var(--card); border:1px solid var(--rule-strong); padding:14px 16px; } .gh{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:10px; } .gh h3{ margin:0; }
  .sw{ width:12px; height:12px; border-radius:2px; display:inline-block; flex:none; } .g-governmental .sw, .bf.g-governmental{ background:var(--s-gov); } .g-enterprise .sw, .bf.g-enterprise{ background:var(--s-ent); } .g-internal_service .sw, .bf.g-internal_service{ background:var(--s-isf); }
  .basis{ font-size:11.5px; color:var(--muted); margin-left:auto; }
  .tiles{ display:grid; grid-template-columns:repeat(2,1fr); gap:8px; } .tile{ border-top:1px solid var(--rule); padding:6px 0 2px; } .tv{ font-size:1.25rem; font-weight:600; } .tk{ font-size:11px; color:var(--muted); letter-spacing:.03em; text-transform:uppercase; }
  .chk{ margin:10px 0 0; font-size:12.5px; } .withheld{ font-size:.92rem; color:var(--muted); }
  .flowgrid{ display:grid; grid-template-columns:repeat(auto-fit,minmax(340px,1fr)); gap:14px; } .fc{ background:var(--card); border:1px solid var(--rule-strong); padding:14px 16px; } .fc h3{ margin:0 0 4px; } .sub{ margin:0 0 10px; font-size:13px; color:var(--muted); }
  .bars{ display:grid; gap:4px; } .br{ display:grid; grid-template-columns:minmax(120px,38%) 1fr 64px; gap:8px; align-items:center; font-size:13px; padding:2px 0; } .br:hover{ background:#f1f4f8; }
  .bl{ overflow-wrap:anywhere; } .bt{ height:12px; background:transparent; display:block; } .bf{ display:block; height:100%; border-radius:0 4px 4px 0; min-width:2px; } .bf.gap{ background:repeating-linear-gradient(45deg,var(--s-gap) 0 3px,#d6dbe0 3px 6px) !important; } .br.gap .bl{ font-style:italic; }
  .bv{ text-align:right; font-variant-numeric:tabular-nums; font-size:12.5px; }
  .trw{ background:var(--card); border:1px solid var(--rule-strong); padding:10px 16px; display:grid; gap:10px; }
  .tr{ display:grid; grid-template-columns:200px 1fr 1fr 110px; gap:12px; align-items:center; font-size:13px; } .tl2{ display:flex; gap:8px; align-items:center; }
  .tb{ display:grid; grid-template-columns:28px 1fr 64px; gap:6px; align-items:center; } .lab{ font-size:11px; color:var(--muted); text-transform:uppercase; } .bf.out{ opacity:.45; } .net{ text-align:right; font-variant-numeric:tabular-nums; }
  .controls{ display:flex; flex-wrap:wrap; gap:8px; margin:14px 0 10px; align-items:center; font-size:13px; } .controls input, .controls select{ font:inherit; padding:6px 8px; border:1px solid var(--rule-strong); background:var(--card); max-width:100%; } .count{ color:var(--muted); }
  .tw{ overflow-x:auto; background:var(--card); border:1px solid var(--rule-strong); } table{ width:100%; border-collapse:collapse; font-size:.84rem; }
  th,td{ text-align:left; padding:7px 9px; border-bottom:1px solid var(--rule); vertical-align:top; } th{ font-size:10.5px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); background:#f3f6f9; white-space:nowrap; } .ft th[data-k]{ cursor:pointer; user-select:none; } th.sorted::after{ content:" ▾"; } th.sorted.asc::after{ content:" ▴"; }
  td.n{ text-align:right; white-space:nowrap; font-variant-numeric:tabular-nums; } td.neg{ color:var(--red); } td.fn{ min-width:220px; } .st{ font-size:11px; color:var(--muted); } td.cx, th.cx{ width:28px; padding-right:0; }
  .ft td:nth-child(2){ position:sticky; left:0; background:var(--card); } .ft th:nth-child(2){ position:sticky; left:0; z-index:1; }
  .bdg{ font-size:9.5px; letter-spacing:.06em; text-transform:uppercase; border:1px solid; padding:0 4px; margin-left:4px; vertical-align:1px; } .bdg.cur{ color:var(--hi); } .bdg.his{ color:var(--steel-deep); }
  .ok{ color:var(--hi); font-size:12px; } .warn{ color:var(--mod); font-size:12px; } .bad{ color:var(--low); font-size:12px; font-weight:600; }
  .cmpbox{ background:var(--card); border:1px solid var(--steel); padding:12px 14px; margin:0 0 10px; } .cmpbox h4{ margin:0 0 8px; } .cmpgrid{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:10px; } .cmpc{ border-top:3px solid var(--rule-strong); padding-top:6px; font-size:13px; } .cmpc.g-governmental{ border-color:var(--s-gov); } .cmpc.g-enterprise{ border-color:var(--s-ent); } .cmpc.g-internal_service{ border-color:var(--s-isf); }
  .cmpc dl{ margin:4px 0 0; display:grid; grid-template-columns:auto 1fr; gap:2px 8px; } .cmpc dt{ color:var(--muted); font-size:11.5px; } .cmpc dd{ margin:0; text-align:right; font-variant-numeric:tabular-nums; }
  .rdw{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:12px; } .rd{ background:var(--card); border:1px solid var(--rule-strong); padding:12px 14px; font-size:.9rem; } .rd p{ margin:4px 0; } details summary{ cursor:pointer; margin-top:6px; } details ul{ margin:6px 0 0; padding-left:18px; font-size:.86rem; }
  .stats{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:10px; margin:14px 0; } .stat{ background:var(--card); border:1px solid var(--rule-strong); padding:10px 12px; } .stat .v{ font-size:1.35rem; font-weight:600; } .stat .l{ font-size:11px; text-transform:uppercase; color:var(--muted); letter-spacing:.03em; }
  .isf{ background:var(--card); border:1px solid var(--rule-strong); padding:12px 18px; font-size:.95rem; max-width:96ch; } .isf ol{ padding-left:20px; margin:8px 0; } .isf li{ margin:6px 0; }
  .terms{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:12px 0 0; } .term{ background:var(--card); border:1px solid var(--rule-strong); padding:10px 12px; font-size:.86rem; } .term b{ display:block; font-size:.95rem; margin-bottom:2px; }
  .gapbox{ background:#fff8ea; border:1px solid #e3c98f; border-left:4px solid var(--mod); padding:12px 16px; margin:14px 0 0; font-size:.92rem; max-width:96ch; }
  .hist{ margin:0; padding-left:18px; font-size:.92rem; } .fgw{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:12px; } .fg{ background:var(--card); border:1px solid var(--rule-strong); padding:12px 14px; } .fg ul{ margin:6px 0 0; padding-left:18px; font-size:.9rem; } .fg p{ margin:0; font-size:12.5px; }
  footer{ padding:28px 0 64px; font-size:11.5px; color:var(--muted); line-height:1.7; } footer .bar{ height:3px; background:var(--navy); margin:0 0 16px; width:48px; }
  @media (max-width:900px){ .terms{ grid-template-columns:1fr 1fr; } }
  @media (max-width:640px){
    body{ font-size:16px; } .tr{ grid-template-columns:1fr; gap:4px; } .net{ text-align:left; }
    .br{ grid-template-columns:1fr 60px; } .br .bl{ grid-column:1 / -1; } .tiles{ grid-template-columns:1fr 1fr; }
    .flowgrid, .gpw, .rdw, .fgw, .terms{ grid-template-columns:1fr; }
  }
"""

JS = """
(function(){
  const ysel=document.getElementById('year');
  function fmt(n){ if(n===''||n===null) return '—'; n=+n; const a=Math.abs(n); return (n<0?'−':'')+'$'+a.toLocaleString('en-US'); }
  function setup(sec){
    const tb=sec.querySelector('.ft tbody'), rows=[...tb.rows], q=sec.querySelector('.f-q'), g=sec.querySelector('.f-g'), m=sec.querySelector('.f-m'), s=sec.querySelector('.f-s'), count=sec.querySelector('.count'), box=sec.querySelector('.cmpbox');
    function apply(){ const t=q.value.trim().toLowerCase(), gv=g.value, mv=m.value, sv=s.value; let n=0;
      rows.forEach(r=>{ const d=r.dataset; const ok=(!t||d.name.includes(t))&&(!gv||(gv[0]==='g'?d.group===gv.slice(2):d.type===gv.slice(2)))&&(!mv||d.mag===mv)&&(!sv||d.status.split(' ').includes(sv)); r.hidden=!ok; if(ok)n++; });
      count.textContent=n+' of '+rows.length+' funds'; }
    [q,g,m,s].forEach(el=>el.addEventListener(el===q?'input':'change',apply)); apply();
    sec.querySelectorAll('.ft th[data-k]').forEach(th=>th.addEventListener('click',()=>{ const k=th.dataset.k, num=th.hasAttribute('data-num'), asc=th.classList.contains('sorted')&&!th.classList.contains('asc');
      sec.querySelectorAll('.ft th').forEach(x=>x.classList.remove('sorted','asc')); th.classList.add('sorted'); if(asc) th.classList.add('asc');
      const val=r=>num?(r.dataset[k]===''?-Infinity:+r.dataset[k]):r.dataset[k]; rows.sort((a,b)=>{const x=val(a),y=val(b);return (x<y?-1:x>y?1:0)*(asc?1:-1);}); rows.forEach(r=>tb.appendChild(r)); }));
    const labels={governmental:['Revenue','Spending','Fund balance'],enterprise:['Operating revenue','Operating expenses','Net position'],internal_service:['Operating revenue','Operating expenses','Net position']};
    function compare(){ const sel=rows.filter(r=>r.querySelector('.cmp').checked);
      if(!sel.length){ box.hidden=true; box.innerHTML=''; return; }
      const groups=new Set(sel.map(r=>r.dataset.group)); const mixed=groups.has('governmental')&&groups.size>1;
      box.innerHTML='<h4>Comparing '+sel.length+' fund'+(sel.length>1?'s':'')+'</h4>'+(mixed?'<p class="cap">Mixed bases: governmental figures are fund balance and total expenditures; proprietary figures are net position and operating expenses. Compare direction and scale, not the numbers one-for-one.</p>':'')+
        '<div class="cmpgrid">'+sel.map(r=>{const d=r.dataset,L=labels[d.group]; return '<div class="cmpc g-'+d.group+'"><b>'+r.querySelector('.fn a').textContent+'</b><dl><dt>'+L[0]+'</dt><dd>'+fmt(d.rev)+'</dd><dt>'+L[1]+'</dt><dd>'+fmt(d.exp)+'</dd><dt>Result</dt><dd>'+fmt(d.res)+'</dd><dt>Net transfers</dt><dd>'+fmt(d.net)+'</dd><dt>'+L[2]+'</dt><dd>'+fmt(d.bal)+'</dd><dt>Change</dt><dd>'+fmt(d.chg)+'</dd></dl></div>';}).join('')+'</div>';
      box.hidden=false; }
    tb.addEventListener('change',e=>{ if(!e.target.classList.contains('cmp')) return; const on=rows.filter(r=>r.querySelector('.cmp').checked); if(on.length>4){ e.target.checked=false; } compare(); });
  }
  document.querySelectorAll('section.yr').forEach(setup);
  if(ysel) ysel.addEventListener('change',()=>document.querySelectorAll('section.yr').forEach(sec=>sec.hidden=sec.dataset.year!==ysel.value));
})();
"""


def render_terms():
    terms = [
        ("Revenue", "Money a fund earns or is given: taxes, fees, grants, charges, interest. For enterprise and internal service funds, operating revenue only; non-operating items are shown separately."),
        ("Expenditures", "Governmental funds. Money spent in the year, including capital purchases and debt principal (modified accrual). No depreciation."),
        ("Operating expenses", "Enterprise and internal service funds. The cost of running the service, including depreciation of assets; capital purchases and debt principal are not expenses (full accrual)."),
        ("Transfers", "Money moved from one City fund to another, as authorized in the budget or by Council. Not revenue for the fund that receives it, not spending for the fund that sends it."),
        ("Fund balance", "Governmental funds. Current financial resources at year end (mainly cash, investments and receivables) less the liabilities payable from them. Much of it is restricted or committed to set uses. Excludes buildings, roads and long-term debt."),
        ("Net position", "Enterprise and internal service funds. Everything the fund owns less everything it owes, including capital assets, long-term debt and pension liabilities. Not comparable to fund balance."),
        ("Other financing sources", "Not revenue. Money or value a fund receives from borrowing, from selling an asset, or from signing a lease or subscription, shown in its own section of the statement below the revenue and expenditure totals. Transfers in are reported here too; this page shows them in section 3 instead."),
        ("Inception of leases and subscriptions", "A lease or software subscription signed during the year (GASB 87 and 96). The whole multi-year commitment is recorded at once, as an expenditure within capital outlay and as an other financing source of the same amount. No cash changes hands in that entry, and the City takes on a liability for the future payments, so this part of capital outlay is not cash capital spending."),
    ]
    return '<div class="terms" aria-label="terms">' + "".join(f'<div class="term"><b>{esc(k)}</b>{esc(v)}</div>' for k, v in terms) + "</div>"


def render_gap_callout(model):
    yr = model["years"][model["default_year"]]
    fl = yr.get("flows") or {}
    gap = fl.get("not_itemized")
    if not gap:
        return ""
    total = yr["groups"]["governmental"]["totals"]["exp"]
    funds = ", ".join(f'{esc(g["name"])} {money(g["gap"], True)}' for g in fl["gaps"])
    cause = (" The missing lines, read from ACFR p." + esc(fl["cause_page"]) + ": " + "; ".join(f"{esc(k)} {money(v, True)}" for k, v in fl["explained"]) + ". Section 2 gives the cause.") if fl.get("explained") else ""
    return (f'<div class="gapbox"><b>Known gap in the detail: {money(gap)} of governmental expenditures ({gap/total*100:.1f}% of {money(total, True)}) is not broken out by function.</b> '
            f'The totals are audited and correct; the breakdown in section 2 is short by this amount, shown there as "not itemized". Funds: {funds}.{cause} '
            f'A fix belongs to the extraction pipeline; until then every chart and table on this page shows the gap rather than hiding it. {chip("documented")}</div>')


def render(model):
    years = sorted(model["years"])
    opts = "".join(f'<option value="{fy}"{" selected" if fy == model["default_year"] else ""}>FY{fy}{"" if model["years"][fy]["complete"] else " (partial)"}</option>' for fy in reversed(years))
    n = len(model["funds"])
    n_fid = sum(len(g["funds"]) for g in model["fiduciary"]["groups"].values())
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>City Finances Dashboard — Learn About Berkeley</title>
<meta name="description" content="Berkeley's audited fund statements, FY{model["default_year"]}: revenue, spending, transfers and balances for {n} funds, by accounting basis, with coverage and reconciliation status.">
<style>{CSS}</style>
<link rel="stylesheet" href="assets/kromer-theme.css">
</head>
<body>
<div class="hubbar"><div class="hubbar-in"><a class="back" href="index.html">&larr; Learn About Berkeley</a><span class="stamp">Dashboard · audited fund statements</span></div></div>
<main class="wrap">
  <header class="masthead">
    <div class="eyebrow">Following the money</div>
    <h1>City finances, as the audit reports them</h1>
    <p class="dek">Berkeley's money sits in {n} legally separate funds plus {n_fid} fiduciary funds held for others. This dashboard reads the audited fund statements: what each group of funds took in and spent, what moved between funds, what each fund holds, and how much of the record is loaded and checked. Figures are the City's; labels say which numbers are facts, which are arithmetic, and which are BeTH's reading.</p>
    <div class="scope"><b>Scope.</b> These are sums of the fund columns on four statements in the ACFR (governmental funds, nonmajor combining, proprietary funds, internal service combining). They are <b>not City-wide totals</b>: they leave out the {n_fid} fiduciary funds, they are added before the statements' own eliminations, and the governmental figures are on the fund basis, which excludes capital assets, long-term debt and pension liabilities that the government-wide statements include.</div>
    <div class="yearbar"><label for="year">Audited year</label> <select id="year">{opts}</select>
      <span class="dim">Years appear here as their audited fund rows are loaded.</span></div>
    {render_gap_callout(model)}
    {render_terms()}
    <div class="legend">Labels: {chip("audited")} read from the audit {chip("derived")} arithmetic on audited figures {chip("reading")} BeTH's interpretation {chip("open")} not yet answered {chip("ties")} checked {chip("pending")} not yet checked</div>
  </header>
  {"".join(render_year(model, fy) for fy in reversed(years))}
  {render_static(model)}
  <p class="cap" style="margin-top:28px">Built by <code>tools/build_dashboard.py</code> from <code>data/funds/*.json</code>, control totals in <code>data/dashboard/statement-totals.json</code>, documented line-item gaps in <code>data/dashboard/known-gaps.json</code> and the fiduciary roster in <code>data/dashboard/fiduciary-funds.json</code>. The fund browser with every fund on one sortable page is <a href="funds.html">here</a>; how the funds relate is on the <a href="berkeley-fund-map.html">Fund Map</a>.</p>
  <footer><div class="bar"></div>Learn About Berkeley &middot; built from public documents &middot; residents decide. Maintained by Steve Kromer, candidate for Berkeley City Council District 1.</footer>
</main>
<script>{JS}</script>
</body>
</html>
'''


def integrity_problems(model):
    """Problems that make the published page wrong or stale even if it was rebuilt."""
    ga = model["gap_audit"]
    out = [f'undocumented {g["kind"]} line-item gap: {g["id"]} FY{g["fy"]} {g["gap"]:,}' for g in ga["undocumented"]]
    out += [f'stale entry in known-gaps.json: {g["id"]} FY{g["fy"]} (documented {g["documented_gap"]:,}; remove it)' for g in ga["stale"]]
    out += [f'{f["id"]}: FY{f["audit_match"]["fy"]} figures {f["audit_match"]["status"]} since tools/verify_fund_statements.py --write'
            for f in model["funds"] if f["audit_match"]["status"] in ("changed", "unmatched")]
    names = {f["name"].lower() for f in model["funds"]}
    out += [f'fiduciary roster lists "{x["name"]}", which now has a ledger record; update data/dashboard/fiduciary-funds.json'
            for g in model["fiduciary"]["groups"].values() for x in g["funds"] if x["name"].lower() in names]
    return out


def main(argv):
    model = build_model()
    page = render(model)
    problems = integrity_problems(model)
    if "--check" in argv:
        for msg in problems:
            print(f"PROBLEM {msg}")
        stale = not OUT.exists() or OUT.read_text() != page
        if stale:
            print(f"{OUT.relative_to(ROOT)} is stale: run python3 tools/build_dashboard.py and commit the result")
        if not stale and not problems:
            print(f"{OUT.relative_to(ROOT)} is current; no integrity problems")
        return 1 if stale or problems else 0
    OUT.write_text(page)
    d = model["years"][model["default_year"]]
    checks = ", ".join(f'{g}={e["check"]["status"]}' for g, e in d["groups"].items() if e.get("check"))
    print(f"wrote {OUT.relative_to(ROOT)}: {len(model['funds'])} funds, years {sorted(model['years'])}, default FY{model['default_year']}; {checks}")
    for msg in problems:
        print(f"PROBLEM {msg}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

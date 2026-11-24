# -*- coding: utf-8 -*-
"""Render docs/berkeley-liability-clock.html from the model, in Learn About Berkeley house style.

Public tier: statements of fact with sources and confidence labels. No
recommendations. Run: python3 tools/liability_clock/render.py
"""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
MODEL = os.path.join(REPO, "data", "liability-clock", "_model.json")
OUT = os.path.join(REPO, "docs", "berkeley-liability-clock.html")

E = lambda s: (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def usd(v):
    return "$" + format(int(round(v)), ",")

def compact(v):
    a = abs(v)
    if a >= 1e9:  return "$%s" % ("%.2f" % (v / 1e9)).rstrip("0").rstrip(".") + "B"
    if a >= 1e6:  return "$%s" % ("%.1f" % (v / 1e6)).rstrip("0").rstrip(".") + "M"
    if a >= 1e3:  return "$%dK" % round(v / 1e3)
    return "$%d" % round(v)

def pill(conf):
    c = (conf or "Unknown").capitalize()
    c = {"High": "High", "Moderate": "Moderate", "Low": "Low"}.get(c, "Unknown")
    return '<span class="pill c-%s">%s</span>' % (c, c)


def render(m):
    cap, po = m["capital"], m["pension_opeb"]
    st = m["drilldowns"]["streets"]
    sa, scond = st["arithmetic"], st["condition"]
    o = []
    A = o.append

    A('<!DOCTYPE html><html lang="en">\n<head>\n<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A('<title>Learn About Berkeley — What Berkeley Owes Its Own Infrastructure</title>')
    A('<meta name="description" content="Berkeley\'s unfunded capital backlog and unfunded pension and retiree-health liability, '
      'by asset class, with the published figures that disagree and the arithmetic behind each one.">')
    A('<style>')
    A(''':root { color-scheme: light; --bg:#f7f8fa; --card:#ffffff; --ink:#1a2030; --mut:#5a6473; --line:#e4e8ee;
  --green:#1f9d6b; --red:#d6453a; --amber:#e3a008; --blue:#3d6fd6; --accent:#15543f; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink); font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
.wrap { max-width:1080px; margin:0 auto; padding:28px 20px 72px; }
h1 { font-size:25px; margin:0 0 4px; letter-spacing:-.02em; }
.sub { color:var(--mut); margin:0 0 4px; max-width:820px; }
.tag { display:inline-block; font-size:11px; color:var(--accent); background:#e7f1ec; border:1px solid #cfe3d9; padding:2px 8px; border-radius:999px; margin-top:6px; }
h2 { font-size:18px; margin:32px 0 6px; letter-spacing:-.01em; }
h2 .n { color:var(--mut); font-weight:600; margin-right:8px; }
h3 { font-size:14.5px; margin:16px 0 6px; }
.lead { color:var(--mut); margin:0 0 14px; max-width:820px; }
.card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:16px 18px; margin-bottom:14px; box-shadow:0 1px 2px rgba(20,30,50,.03); }
.kpis { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:12px; margin-top:14px; }
.kpi { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:14px 16px; }
.kpi .v { font-size:22px; font-weight:700; letter-spacing:-.02em; color:var(--accent); }
.kpi .l { color:var(--mut); font-size:12.5px; margin-top:2px; }
.pill { font-size:11px; padding:1px 7px; border-radius:999px; font-weight:600; display:inline-block; white-space:nowrap; }
.c-High { background:#e7f1ec; color:#15543f; } .c-Moderate { background:#fff5d6; color:#8a6300; } .c-Low { background:#fde8e6; color:#8f2b23; } .c-Unknown { background:#f0f0f3; color:#6a7280; }
a { color:var(--accent); }
.disc { background:#fbf6e9; border:1px solid #ecdcb0; border-radius:10px; padding:12px 14px; font-size:13px; color:#6b551f; margin-top:10px; }
.foot { color:var(--mut); font-size:12px; margin-top:24px; border-top:1px solid var(--line); padding-top:14px; }
table { width:100%; border-collapse:collapse; font-size:13.5px; }
th,td { text-align:left; padding:7px 9px; border-bottom:1px solid var(--line); vertical-align:top; }
th { color:var(--mut); font-weight:600; font-size:12px; white-space:nowrap; }
td:first-child { font-weight:600; }
td.num { text-align:right; white-space:nowrap; font-variant-numeric:tabular-nums; }
.two { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
@media (max-width:760px){ .two { grid-template-columns:1fr; } }
.side { font-size:12.5px; color:var(--mut); }
ul.tight { margin:6px 0 0 18px; padding:0; } ul.tight li { margin-bottom:4px; }
.scroll { overflow-x:auto; }
/* counter */
.ctr { text-align:center; padding:22px 16px 18px; }
.ctr .big { font-size:clamp(26px,6vw,46px); font-weight:700; letter-spacing:-.03em; font-variant-numeric:tabular-nums; }
.ctr .rate { color:var(--mut); font-size:13px; margin-top:6px; font-variant-numeric:tabular-nums; }
.ctr .cap { color:var(--mut); font-size:12.5px; margin-top:8px; max-width:560px; margin-left:auto; margin-right:auto; }
/* bars */
.bar { height:9px; background:#eceff4; border-radius:3px; overflow:hidden; min-width:50px; }
.bar > i { display:block; height:100%; background:var(--accent); border-radius:0 3px 3px 0; }
.bar.alt > i { background:var(--amber); }
.gtrack { display:flex; height:24px; border-radius:6px; overflow:hidden; gap:2px; }
.gseg { display:flex; align-items:center; justify-content:center; font-size:10.5px; color:var(--mut); background:#eceff4; white-space:nowrap; overflow:hidden; }
.gseg.cur { background:var(--accent); color:#fff; font-weight:600; }
.gmark { position:relative; height:26px; margin-top:3px; }
.gmark > div { position:absolute; transform:translateX(-50%); text-align:center; }
.gmark .pin { width:2px; height:8px; background:var(--red); margin:0 auto 2px; }
.gmark .lbl { font-size:12px; font-weight:700; color:var(--red); white-space:nowrap; }
.pend { display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:12px; margin-top:12px; }
.pc { border:1px dashed #c9d0da; border-radius:10px; padding:13px 15px; background:#fbfcfd; }
.pc .k { font-size:10.5px; letter-spacing:.06em; text-transform:uppercase; color:#8a6300; font-weight:600; }
.pc .v { font-size:19px; color:#9aa3b0; font-weight:700; margin:6px 0 2px; }
.pc h4 { font-size:13.5px; margin:4px 0 0; } .pc p { font-size:12.5px; color:var(--mut); margin:5px 0 0; }''')
    A('</style>')
    A('<link rel="stylesheet" href="assets/kromer-theme.css">')
    A('</head>\n<body>\n<div class="wrap">\n')

    A('  <h1>What Berkeley Owes Its Own Infrastructure</h1>')
    A('  <p class="sub">Berkeley carries two large unfunded obligations: a deferred capital and maintenance backlog, '
      'and an unfunded pension and retiree-health liability. This page sets out what each one is, by asset class, '
      'where the figures come from, and how fast each is growing. Both counters are derived from published City '
      'documents; the arithmetic behind every digit is on the page.</p>')
    A('  <span class="tag">Infrastructure</span> <span class="tag">Capital</span> <span class="tag">Pensions</span> <span class="tag">Counter</span>')
    A('  <p class="side" style="margin-top:8px">Companion pages: '
      '<a href="berkeley-cip-hub-vs-vision-2050.html">the dashboard referral vs. Vision 2050</a> · '
      '<a href="berkeley-measure-u-oversight.html">who watches the $300 million</a> · '
      '<a href="berkeley-cip-hub-data-review.html">the studio data review</a></p>')

    A('  <div class="disc"><strong>Acronyms used on this page.</strong> ACFR = Annual Comprehensive Financial Report · '
      'AMP = Asset Management Program · CIP = Capital Improvement Program · ENR = Engineering News-Record '
      '(construction cost index) · GO = general obligation (bond) · MRP = Municipal Regional Permit · '
      'OPEB = other post-employment benefits (retiree health) · PCI = Pavement Condition Index · '
      'UAL = unfunded actuarial liability.</div>')

    npub = len([c for c in m["classes"] if not c["unfunded_need"]])
    A('  <div class="kpis">')
    A('    <div class="kpi"><div class="v" id="k-cap">%s</div><div class="l">Deferred capital and maintenance, accruing from %s</div></div>'
      % (compact(cap["backlog"]["point"]), m["basis_date"]))
    A('    <div class="kpi"><div class="v">%s</div><div class="l">Unfunded pension and retiree health, as carried %s</div></div>'
      % (compact(po["unfunded"]), po["as_reported"]))
    A('    <div class="kpi"><div class="v">%d</div><div class="l">Published citywide backlog figures, 2020–2026, that disagree</div></div>'
      % len(cap["published_estimates"]))
    A('    <div class="kpi"><div class="v">%s</div><div class="l">Of the backlog not broken out by asset class in any public document</div></div>'
      % compact(m["unattributed"]["need"]))
    A('  </div>')

    # ---------- A ----------
    A('\n  <h2><span class="n">A</span>The counter, and what moves it</h2>')
    A('  <p class="lead">The capital figure below starts from the City Auditor’s %s estimate at %s and grows at the '
      'rate the model computes. Only one of four possible accruals is currently included, because the other three '
      'need data the City has not published. Each is listed with what it is waiting on.</p>'
      % (compact(cap["backlog"]["point"]), m["basis_date"]))
    A('  <div class="card ctr">')
    A('    <div class="big" id="ctr">%s</div>' % usd(cap["backlog"]["point"]))
    A('    <div class="rate">+$%.4f per second · %s a year · published band %s to %s</div>'
      % (cap["rate_per_second"], compact(cap["rate_per_year"]),
         compact(cap["backlog"]["low"]), compact(cap["backlog"]["high"])))
    A('    <div class="cap">Escalation only: the same scope of work costing more each year, at %.1f%% a year. '
      'This is not a measure of the roads getting worse — that is a separate accrual, listed below as pending.</div>'
      % (m["assumptions"]["escalation"]["default_rate"] * 100))
    A('  </div>')
    A('  <div class="scroll"><table>')
    A('  <tr><th>Accrual</th><th>What it measures</th><th class="num">Amount</th><th>Where it counts</th></tr>')
    for c in m["components"]:
        if c["status"] == "live":
            where = "capital counter" if c["ticker"] == "capital" else "pension figure"
            inc = compact(c["accrual_per_year"]) + " / yr"
            stt = '<span class="pill c-High">in the %s</span>' % where
        else:
            inc = "$0"
            stt = '<span class="pill c-Moderate">waiting on %s</span>' % E(", ".join(c["blocking"]))
        A('  <tr><td>%s</td><td>%s</td><td class="num">%s</td><td>%s</td></tr>'
          % (E(c["label"]), E(c["what_it_measures"]), inc, stt))
    A('  </table></div>')
    A('  <p class="side" style="margin-top:8px">A component enters the counter only when every input it needs exists in '
      'a published document and carries a source. Nothing on this page is estimated to fill a gap.</p>')

    # ---------- B ----------
    A('\n  <h2><span class="n">B</span>The backlog by asset class</h2>')
    A('  <p class="lead">Six of the eleven asset classes publish an unfunded dollar figure. Five do not, and are shown as '
      'such rather than as zero. The mandate column records what obliges the City to act, which differs sharply by class.</p>')
    A('  <div class="scroll"><table>')
    A('  <tr><th>Asset class</th><th>Scope</th><th class="num">Unfunded</th><th>Obligation</th>'
      '<th class="num">Escalation</th><th>Confidence</th></tr>')
    withn = [c for c in m["classes"] if c["unfunded_need"]]
    mx = max([c["unfunded_need"] for c in withn] + [m["unattributed"]["need"]])
    for c in m["classes"]:
        if c["unfunded_need"]:
            need = ('<div class="bar" style="display:inline-block;width:70px;vertical-align:middle"><i style="width:%.1f%%"></i></div> %s'
                    % (max(2.0, c["unfunded_need"] / mx * 100), compact(c["unfunded_need"])))
            acc = compact(c["accrual_per_year"]) + " / yr"
        else:
            need, acc = '<span style="color:#8a93a0">not published</span>', "—"
        A('  <tr><td>%s</td><td>%s</td><td class="num">%s</td><td>%s</td><td class="num">%s</td><td>%s</td></tr>'
          % (E(c["name"]), E(c["scope"]), need, E(c["mandate_label"]), acc, pill(c["confidence"])))
    A('  <tr><td>Not attributed to any class</td><td>Citywide estimate minus every published class figure</td>'
      '<td class="num"><div class="bar alt" style="display:inline-block;width:70px;vertical-align:middle"><i style="width:100%%"></i></div> %s</td>'
      '<td>Unknown</td><td class="num">%s / yr</td><td>%s</td></tr>'
      % (compact(m["unattributed"]["need"]), compact(m["unattributed"]["accrual_per_year"]), pill("moderate")))
    A('  </table></div>')
    A('  <div class="disc"><strong>%s of the headline, about %d%%, is not broken out by asset class in any public document.</strong> '
      'It is the difference between the citywide estimate and the sum of the classes that publish a figure.</div>'
      % (compact(m["unattributed"]["need"]), round(100.0 * m["unattributed"]["need"] / cap["backlog"]["point"])))
    A('  <h3>What obliges the City, by class</h3>')
    A('  <div class="card"><table>')
    A('  <tr><th>Class</th><th>Noted in the source documents</th></tr>')
    for c in m["classes"]:
        if c["key_finding"]:
            A('  <tr><td>%s</td><td style="font-weight:400">%s</td></tr>' % (E(c["name"]), E(c["key_finding"])))
    A('  </table></div>')
    d = m["discretion"]
    A('  <div class="disc"><strong>A note on reading the obligation column.</strong> Of the unfunded need that is '
      '<em>published</em>, %d%% sits in classes where Council sets the service level. That covers only %d%% of the '
      'headline backlog. The two classes with the least discretion — %s — publish no unfunded figure at all, '
      'so they contribute nothing to that percentage. The split describes what is disclosed, not what is owed.</div>'
      % (round(100.0 * d["split"].get("high", 0) / d["covered_need"]),
         round(100.0 * d["coverage_of_headline"]),
         E(" and ".join(d["mandated_classes_with_no_published_need"]))))

    # ---------- C ----------
    A('\n  <h2><span class="n">C</span>Eight published figures for the same number</h2>')
    A('  <p class="lead">%s</p>' % E(cap["conflict_note"]))
    A('  <div class="scroll"><table>')
    A('  <tr><th class="num">Figure</th><th>As written</th><th>Source</th><th>Date</th><th></th></tr>')
    emax = max(e["value"] for e in cap["published_estimates"])
    def bn(v):
        return "$" + ("%.3f" % (v / 1e9)).rstrip("0").rstrip(".") + "B" if v >= 1e9 else compact(v)
    for e in cap["published_estimates"]:
        sel = ' style="background:#f3f8f5"' if e.get("selected") else ''
        mark = '<span class="pill c-High">this page</span>' if e.get("selected") else ''
        A('  <tr%s><td class="num">%s</td><td style="font-weight:400">%s</td><td style="font-weight:400">%s</td>'
          '<td style="font-weight:400">%s</td><td>%s</td></tr>'
          % (sel, bn(e["value"]), E(e["as_written"]), E(e["source"]), E(e["date"]), mark))
    A('  </table></div>')
    A('  <div class="disc"><strong>These are not all measuring the same thing.</strong> %s</div>'
      % E(cap["comparability_warning"]))

    # ---------- D ----------
    A('\n  <h2><span class="n">D</span>Pension and retiree health</h2>')
    A('  <p class="lead">A different kind of obligation from the capital backlog: a legal debt to people that accrues '
      'interest at a set rate, rather than a physical debt to assets. The two are kept separate on this page and are '
      'never added together. Figures are from the FY2025 ACFR.</p>')
    A('  <div class="two">')
    for key, label in (("pension", "Pension (CalPERS, three plans)"), ("opeb", "Retiree health (three plans)")):
        r = po["detail"][key]
        direction = "falling" if r["accrual_per_year"] < 0 else "rising"
        A('    <div class="card"><h3 style="margin-top:0">%s</h3><table>' % label)
        A('      <tr><td>Unfunded</td><td class="num">%s</td></tr>' % usd(r["unfunded"]))
        A('      <tr><td>Discount rate</td><td class="num">%.2f%%</td></tr>' % (r["discount_rate"] * 100))
        A('      <tr><td>Interest on the unfunded balance</td><td class="num">%s / yr</td></tr>' % usd(r["interest_on_unfunded"]))
        amt = r["amortization_payment"]
        if amt >= 0:
            A('      <tr><td>Paid above normal cost</td><td class="num">%s / yr</td></tr>' % usd(amt))
        else:
            A('      <tr><td>Paid against normal cost</td><td class="num">%s / yr short</td></tr>' % usd(-amt))
        A('      <tr><td>Net change in the balance</td><td class="num">%s / yr, %s</td></tr>'
          % (usd(r["accrual_per_year"]), direction))
        A('    </table></div>')
    A('  </div>')
    pen = po["detail"]["pension"]
    A('  <div class="card"><p style="margin:0">Berkeley pays <strong>%s a year</strong> above normal cost against a '
      '<strong>%s</strong> pension shortfall. <strong>%s</strong> of that is interest at the %.2f%% discount rate, so '
      '<strong>%s</strong> reduces the balance — %.2f%% of it a year. Employer contributions to retiree health cover '
      '%.1f%% of the employer normal cost, so that balance rises. Net of the two, the whole pension and retiree-health '
      'side changes by <strong>%s a year</strong>.</p></div>'
      % (compact(pen["amortization_payment"]), compact(pen["unfunded"]), compact(pen["interest_on_unfunded"]),
         pen["discount_rate"] * 100, compact(-pen["accrual_per_year"]), pen["principal_reduction_rate"] * 100,
         po["detail"]["opeb"]["normal_cost_coverage"] * 100, compact(po["rate_per_year"])))
    A('  <p class="side">%s This excludes investment performance and one-off assumption or benefit changes, which '
      'dominate any single year; both balances fell by more than these figures in the reported period, on exactly those items.</p>'
      % E(po["measurement_date_note"]))

    # ---------- E ----------
    A('\n  <h2><span class="n">E</span>Streets, in detail</h2>')
    A('  <p class="lead">The only asset class with a public condition database, and so the only one that can be shown '
      'at this depth. %d centerline miles, %s lane-miles.</p>'
      % (st["network"]["centerline_miles"], st["network"]["lane_miles"]))
    A('  <div class="card">')
    A('    <h3 style="margin-top:0">Condition: PCI %d (%s) as of %s</h3>'
      % (scond["value"], scond["current_tier"], scond["as_of"]))
    A('    <div class="gtrack">')
    for t in scond["tiers"]:
        w = (t["high"] - t["low"] + 1)
        A('      <div class="gseg%s" style="flex:0 0 %.1f%%">%s</div>'
          % (" cur" if t["is_current"] else "", w, E(t["label"])))
    A('    </div>')
    A('    <div class="gmark"><div style="left:%d%%"><div class="pin"></div><div class="lbl">Berkeley %d</div></div></div>'
      % (scond["value"], scond["value"]))
    A('    <p class="side" style="margin-top:4px">%d points below the Good tier. Tier bands are the Metropolitan '
      'Transportation Commission’s. %s</p>' % (scond["points_to_good"], E(scond["peer_comparison"]["note"])))
    A('  </div>')
    pt = st["targets"]["published_target"]
    A('  <div class="disc"><strong>Berkeley has adopted a pavement target and never published its cost.</strong> '
      'The %s sets a target of PCI %s, with no target year. Separately, the adopted %s states that its own funding '
      'level does not reach the good tier.</div>'
      % (E(pt["source"]), E(pt["value"]), E(st["governing_plan"]["name"])))
    A('  <h3>Where the money goes</h3>')
    A('  <div class="card"><p style="margin:0 0 10px">Of <strong>%s a year</strong>, <strong>%s</strong> — %.1f%% — '
      'is absorbed by escalation on the %s of work still outstanding. Net progress against the published backlog is '
      '<strong>%s a year</strong>, which clears that backlog around <strong>%d</strong>, holding scope constant.</p>'
      % (compact(sa["annual_spend"]), compact(sa["annual_escalation"]),
         sa["share_of_spend_lost_to_escalation"] * 100, compact(st["backlog"]["unfunded_need"]),
         compact(sa["net_progress_per_year"]), int(m["basis_date"][:4] + "") + int(round(sa["clearance_years"]))))
    A('  <p class="side" style="margin:0">%s</p></div>' % E(sa["assumption_warning"]))
    A('  <div class="two">')
    A('    <div class="card"><h3 style="margin-top:0">Funding stack</h3><table>')
    fmax = max(x["annual"] for x in st["funding"]["streams"])
    for x in st["funding"]["streams"]:
        A('      <tr><td style="font-weight:400">%s</td><td style="width:90px"><div class="bar"><i style="width:%.0f%%"></i></div></td>'
          '<td class="num">%s</td></tr>' % (E(x["name"]), x["annual"] / fmax * 100, compact(x["annual"])))
    A('    </table><p class="side" style="margin-top:8px">%d%% comes from the General Fund and CIP rather than a '
      'dedicated stream.</p></div>' % round(st["funding"]["discretionary_share"] * 100))
    A('    <div class="card"><h3 style="margin-top:0">Cost of clearing the published backlog faster</h3><table>')
    smax = max(x["annual_spend"] for x in sa["scenarios"])
    for x in sa["scenarios"]:
        em = ' style="color:var(--red);font-weight:700"' if x["is_current_pace"] else ''
        A('      <tr><td style="font-weight:400"%s>%d years</td><td style="width:90px"><div class="bar"><i style="width:%.0f%%"></i></div></td>'
          '<td class="num"%s>%s / yr</td></tr>'
          % (em, x["years"], x["annual_spend"] / smax * 100, em, compact(x["annual_spend"])))
    A('    </table><p class="side" style="margin-top:8px">Halving the horizon does not double the cost; escalation '
      'compounds on whatever is left. The highlighted row is close to the current funding level.</p></div>')
    A('  </div>')

    # ---------- F ----------
    A('\n  <h2><span class="n">F</span>What this page cannot tell you</h2>')
    A('  <p class="lead">%s</p>' % E(st["targets"]["note"]))
    A('  <div class="pend">')
    labels = {"hold_pci_56_annual": "What holds PCI at 56", "reach_pci_70_annual": "What reaches PCI 70",
              "reach_pci_70_years": "Years to reach PCI 70", "deferral_curve_by_pci_band": "Cost by PCI band"}
    for k in st["targets"]["fields"]:
        A('    <div class="pc"><div class="k">not published</div><div class="v">— — —</div>'
          '<h4>%s</h4><p>%s</p></div>' % (E(labels.get(k, k)), E(st["targets"]["what_each_unblocks"].get(k, ""))))
    A('  </div>')
    A('  <h3>Open questions behind the figures on this page</h3>')
    A('  <div class="card"><table><tr><th>Item</th><th>Who holds it</th><th>Status</th></tr>')
    for r in m["pending_requests"]:
        if r["status"] in ("resolved", "retired"):
            continue
        A('  <tr><td>%s</td><td style="font-weight:400">%s</td><td>%s</td></tr>'
          % (E(r["item"]), E(r["holder"]), E(r["status"].replace("_", " "))))
    A('  </table></div>')

    # ---------- G ----------
    A('\n  <h2><span class="n">G</span>Method and sources</h2>')
    A('  <div class="card"><p style="margin:0 0 8px">Every figure is produced by a small Python model in this repository '
      '(<code>tools/liability_clock/</code>) from the data files in <code>data/liability-clock/</code>. The page renders '
      'what the model emits; it computes nothing of its own except advancing the counter between frames. '
      '<code>python3 tools/liability_clock/test_golden.py</code> checks %d invariants, including that every pending '
      'accrual contributes exactly zero, that the class table reconciles to the counter, and that the pension figures '
      'are never folded into the capital headline.</p>'
      '<p style="margin:0" class="side">Identified unfunded need ties to the source workbook exactly (%s).</p></div>'
      % (48, usd(cap["backlog_alternates"]["identified_by_class"]["point"])))
    A('  <div class="scroll"><table><tr><th>ID</th><th>Source</th><th>Author</th><th>Date</th></tr>')
    for s in m["sources"]:
        loc = (' <span class="side">— %s</span>' % E(s["locator"])) if s.get("locator") else \
              ' <span class="pill c-Unknown">locator unverified</span>'
        A('  <tr><td>%s</td><td style="font-weight:400">%s%s</td><td style="font-weight:400">%s</td><td style="font-weight:400">%s</td></tr>'
          % (E(s["id"]), E(s["title"]), loc, E(s["author"]), E(s["date"])))
    A('  </table></div>')

    A('\n  <p class="foot">Learn About Berkeley · Capital backlog basis %s; pension and retiree health as carried %s. '
      'Figures are the City of Berkeley’s own, recompiled and cited. Where the City’s documents disagree, this page '
      'shows the disagreement rather than choosing. Model version %s.</p>'
      % (m["basis_date"], po["as_reported"], m["_meta"]["version"]))

    A('</div>')
    A('<script>')
    A('(function(){var B=%d,P=%.10f,S=%d,e=document.getElementById("ctr"),k=document.getElementById("k-cap");'
      % (m["basis_epoch_ms"], cap["rate_per_second"], cap["backlog"]["point"]))
    A('var f=new Intl.NumberFormat("en-US",{style:"currency",currency:"USD",minimumFractionDigits:0,maximumFractionDigits:0});')
    A('function t(){var v=S+P*((Date.now()-B)/1000);e.textContent=f.format(v);}')
    A('t();if(window.matchMedia("(prefers-reduced-motion: reduce)").matches){setInterval(t,1000);}'
      'else{(function l(){t();requestAnimationFrame(l);})();}})();')
    A('</script>')
    A('</body>\n</html>')
    return "\n".join(o)


if __name__ == "__main__":
    with io.open(MODEL, encoding="utf-8") as fh:
        m = json.load(fh)
    html = render(m)
    with io.open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote %s (%d bytes)" % (os.path.relpath(OUT, REPO), len(html)))

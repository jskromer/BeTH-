#!/usr/bin/env python3
"""Build docs/fund-activity.html: Council agenda money actions, sorted into the City's fund families.

Inputs:  data/agenda_fund_actions.json  (one block per meeting; add one with each budget scan)
         data/fund_numbers.json         (AAO Exhibit A fund list + ACFR crosswalk)
Usage:   python3 tools/build_fund_activity.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAMILIES = ["General Fund", "Special revenue", "Grants", "Capital projects", "Debt service", "Enterprise",
            "Internal service", "Trust & successor agency", "Agency (pass-through)", "Rent Board (separate agency)"]
KIND = {"spend": "One-time spending", "annual": "Recurring cost / yr", "authority": "Bid authority",
        "revenue": "New revenue", "passthrough": "Pass-through"}
COLS = ["spend", "annual", "authority", "revenue", "passthrough"]


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def m(n, cents=False):
    if n is None:
        return "—"
    s = f"{abs(n):,.2f}" if cents and n != int(n) else f"{abs(n):,.0f}"
    return f"−${s}" if n < 0 else f"${s}"


def acfr_page(aid):
    return "fund-608-marina.html" if aid == "608" else f"fund-{aid}.html"


def main():
    acts = json.loads((ROOT / "data/agenda_fund_actions.json").read_text())
    fn = json.loads((ROOT / "data/fund_numbers.json").read_text())
    funds = {b["number"]: b for b in fn["budget_funds"]}
    fam_size = {}
    for b in fn["budget_funds"]:
        if b.get("fy2027_adopted"):
            fam_size[b["family"]] = fam_size.get(b["family"], 0) + 1

    def fund_cell(num):
        b = funds.get(num, {"name": "Not in FY2026–27 fund list", "acfr": []})
        link = ""
        if b.get("acfr"):
            link = f' <a class="au" href="{acfr_page(b["acfr"][0])}" title="FY2025 audit page">audit</a>'
        return f'<a class="fl" href="#f-{esc(num)}">{esc(num)}</a> {esc(b["name"])}{link}'

    meetings = sorted(acts["meetings"], key=lambda x: x["date"], reverse=True)
    by_fund = {}
    sections = []
    all_actions = 0
    for mt in meetings:
        rows_by_fam = {}
        tot = {f: {k: 0 for k in COLS} for f in FAMILIES}
        touched = {f: set() for f in FAMILIES}
        for a in mt["actions"]:
            b = funds.get(a["fund"], {})
            fam = b.get("family", "General Fund")
            tot[fam][a["kind"]] += a["amount"]
            touched[fam].add(a["fund"])
            by_fund.setdefault(a["fund"], []).append((mt, a))
            all_actions += 1
            ap = b.get("fy2027_adopted")
            pct = abs(a["amount"]) / ap * 100 if ap else 0
            share = ("<0.1%" if pct < 0.1 else f"{pct:.1f}%") if ap and a["kind"] in ("spend", "authority", "annual") else ""
            rows_by_fam.setdefault(fam, []).append(
                f'<tr><td class="fn">{fund_cell(a["fund"])}</td><td class="c">{esc(a["item"])}</td>'
                f'<td><a href="{esc(a["src"])}">{esc(a["title"])}</a>{"<div class=nt>" + esc(a["note"]) + "</div>" if a.get("note") else ""}</td>'
                f'<td><span class="k k-{a["kind"]}">{KIND[a["kind"]]}</span></td>'
                f'<td class="n {"neg" if a["amount"] < 0 else ""}">{m(a["amount"], True)}</td>'
                f'<td class="n">{m(ap) if ap else "—"}</td><td class="n">{share}</td><td class="cf cf-{a["confidence"][0]}">{esc(a["confidence"])}</td></tr>')
        fam_rows = []
        for f in FAMILIES:
            if not fam_size.get(f) and not touched[f]:
                continue
            t = tot[f]
            cells = "".join(f'<td class="n {"neg" if t[k] < 0 else ""} {"z" if not t[k] else ""}">{m(t[k]) if t[k] else "·"}</td>' for k in COLS)
            fam_rows.append(f'<tr class="{"" if touched[f] else "z"}"><td>{esc(f)}</td><td class="n">{len(touched[f])} of {fam_size.get(f, 0)}</td>{cells}</tr>')
        detail = []
        for f in FAMILIES:
            if f in rows_by_fam:
                detail.append(f'<tr class="fam"><td colspan="8">{esc(f)}</td></tr>' + "".join(rows_by_fam[f]))
        un = "".join(f'<li>Item {esc(u["item"])}: {esc(u["title"])}, {m(u["amount"])} ({KIND.get(u["kind"], u["kind"])}). {esc(u.get("note", ""))}</li>' for u in mt.get("unassigned", []))
        n_funds = sum(len(s) for s in touched.values())
        sections.append(f'''
  <section class="mt" id="m-{esc(mt["date"])}">
    <h2>{esc(mt["label"])} <span class="st st-{esc(mt["status"])}">{esc(mt["status"])}</span></h2>
    <p class="meta">{n_funds} funds touched in {len([f for f in FAMILIES if touched[f]])} families · <a href="{esc(mt["scan"])}">full budget scan</a> · <a href="{esc(mt["eagenda"])}">eAgenda</a></p>
    <h3>Across the fund families</h3>
    <div class="tw"><table class="fam-t"><thead><tr><th>Family</th><th>Funds touched</th>{"".join(f"<th>{KIND[k]}</th>" for k in COLS)}</tr></thead><tbody>{"".join(fam_rows)}</tbody></table></div>
    <p class="cap">"Funds touched" counts funds named in this agenda against the funds with an FY2027 appropriation in that family. Bid authority is permission to solicit bids; contracts come back to Council. Recurring costs are annual run-rates.</p>
    <h3>Every fund-level action</h3>
    <div class="tw"><table><thead><tr><th>Fund</th><th>Item</th><th>What</th><th>Kind</th><th>Amount</th><th>FY27 adopted</th><th>Share</th><th>Conf.</th></tr></thead><tbody>{"".join(detail)}</tbody></table></div>
    {"<p class='cap'>Not tied to a fund in the staff report:</p><ul class='cap'>" + un + "</ul>" if un else ""}
  </section>''')

    fund_blocks = []
    for num in sorted(by_fund):
        b = funds.get(num, {"name": "?", "family": "?", "acfr": []})
        tot = {k: 0 for k in COLS}
        lis = []
        for mt, a in by_fund[num]:
            tot[a["kind"]] += a["amount"]
            lis.append(f'<tr><td><a href="#m-{esc(mt["date"])}">{esc(mt["date"])}</a></td><td class="c">{esc(a["item"])}</td><td>{esc(a["title"])}</td>'
                       f'<td><span class="k k-{a["kind"]}">{KIND[a["kind"]]}</span></td><td class="n {"neg" if a["amount"] < 0 else ""}">{m(a["amount"], True)}</td><td>{esc(mt["status"])}</td></tr>')
        sums = " · ".join(f'{KIND[k]} {m(v)}' for k, v in tot.items() if v)
        link = f' · <a href="{acfr_page(b["acfr"][0])}">FY2025 audit page</a>' if b.get("acfr") else ""
        extra = f' · {esc(b["note"])}' if b.get("note") else ""
        fund_blocks.append(f'''
    <div class="fb" id="f-{esc(num)}"><h3>{esc(num)} · {esc(b["name"])}</h3>
    <p class="meta">{esc(b["family"])} · FY2027 adopted {m(b.get("fy2027_adopted"))}{link}{extra}</p>
    <p class="meta"><b>Logged so far:</b> {sums}</p>
    <div class="tw"><table><thead><tr><th>Meeting</th><th>Item</th><th>What</th><th>Kind</th><th>Amount</th><th>Status</th></tr></thead><tbody>{"".join(lis)}</tbody></table></div></div>''')

    css = (ROOT / "docs/funds.html").read_text().split("<style>")[1].split("</style>")[0]
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Council Actions by Fund — Learn About Berkeley</title>
<meta name="description" content="Each Council agenda's money actions, sorted into Berkeley's fund families, with a running record for every fund.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>{css}
  h2{{ font-family:"Playfair Display",serif; font-size:1.5rem; margin:40px 0 4px; }} h3{{ font-family:"JetBrains Mono",monospace; font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--steel-deep); margin:22px 0 8px; }}
  .meta{{ font-family:"JetBrains Mono",monospace; font-size:11.5px; color:var(--muted); margin:2px 0; }}
  tr.fam td{{ background:#eef2f6; font-family:"JetBrains Mono",monospace; font-size:10.5px; letter-spacing:.08em; text-transform:uppercase; color:var(--slate); font-weight:700; }}
  tr.z td, td.z{{ color:#a3adb8; }} td.c{{ text-align:center; font-family:"JetBrains Mono",monospace; }}
  .nt{{ font-size:.8rem; color:var(--muted); margin-top:2px; }} a.fl{{ font-weight:700; text-decoration:none; }} a.au{{ font-family:"JetBrains Mono",monospace; font-size:9.5px; text-transform:uppercase; margin-left:4px; }}
  .k{{ font-family:"JetBrains Mono",monospace; font-size:9.5px; text-transform:uppercase; letter-spacing:.04em; white-space:nowrap; padding:1px 5px; border:1px solid var(--rule-strong); }}
  .k-spend,.k-annual{{ color:var(--red); border-color:#e2b8b5; }} .k-authority{{ color:var(--mod); border-color:#e6d2a8; }} .k-revenue{{ color:var(--hi); border-color:#b5d6c8; }} .k-passthrough{{ color:var(--unk); }}
  .cf{{ font-family:"JetBrains Mono",monospace; font-size:10px; }} .cf-H{{ color:var(--hi); }} .cf-M{{ color:var(--mod); }} .cf-L{{ color:var(--low); }}
  .st{{ font-family:"JetBrains Mono",monospace; font-size:10px; letter-spacing:.08em; text-transform:uppercase; vertical-align:middle; border:1px solid var(--mod); color:var(--mod); padding:1px 6px; }} .st-adopted{{ border-color:var(--hi); color:var(--hi); }}
  .fb{{ border-top:1px solid var(--rule-strong); padding-top:4px; margin-top:18px; }}
  nav.jump{{ font-family:"JetBrains Mono",monospace; font-size:11.5px; line-height:2; }} nav.jump a{{ margin-right:10px; }}
</style>
<link rel="stylesheet" href="assets/kromer-theme.css">
</head>
<body>
<div class="hubbar"><div class="hubbar-in"><a class="back" href="funds.html">&larr; Every City fund</a><span class="stamp">Council actions by fund</span></div></div>
<main class="wrap">
  <header class="masthead">
    <div class="eyebrow">Following the money</div>
    <h1>What each Council agenda does to each fund</h1>
    <p class="dek">Berkeley's money sits in about 150 budget funds, grouped by the Appropriations Ordinance into families: the General Fund, special taxes and fees, grants, capital projects, debt service, enterprises like sewer and the marina, internal services, and pass-through districts. Each agenda below is broken out fund by fund from its staff reports, so a fund can be followed from meeting to meeting. Amounts are as proposed until the vote.</p>
    <div class="statrow">
      <div class="stat"><div class="v">{len(meetings)}</div><div class="l">Meetings logged</div></div>
      <div class="stat"><div class="v">{all_actions}</div><div class="l">Fund-level actions</div></div>
      <div class="stat"><div class="v">{len(by_fund)}</div><div class="l">Funds touched</div></div>
      <div class="stat"><div class="v">{sum(1 for b in fn["budget_funds"] if b.get("fy2027_adopted"))}</div><div class="l">Funds with an FY2027 appropriation</div></div>
    </div>
    <nav class="jump"><b>Meetings:</b> {" ".join(f'<a href="#m-{esc(x["date"])}">{esc(x["date"])}</a>' for x in meetings)}<br><b>Funds:</b> {" ".join(f'<a href="#f-{esc(n)}">{esc(n)}</a>' for n in sorted(by_fund))}</nav>
  </header>
  {"".join(sections)}
  <section><h2>Follow a fund</h2><p class="meta">Every logged action for each fund, across meetings.</p>{"".join(fund_blocks)}</section>
  <p class="cap">Fund numbers, names and FY2027 adopted appropriations: Exhibit A of <a href="{esc(fn["sources"]["fy2027_aao"]["url"])}">Ordinance 8,029-N.S.</a> (FY2027 Annual Appropriations Ordinance). "Share" is the action's amount as a percent of the fund's FY2027 appropriation, for scale only; it is not a measure of the fund's balance. Each amount links to the staff report it was read from. Coverage: meetings are added as each budget scan is published; scans before Dec 1, 2026 did not record fund numbers and are not yet logged. Data: <code>data/agenda_fund_actions.json</code>; built by <code>tools/build_fund_activity.py</code>.</p>
  <footer><div class="bar"></div>Learn About Berkeley &middot; built from public documents &middot; residents decide. Maintained by Steve Kromer.</footer>
</main>
</body>
</html>
'''
    out = ROOT / "docs/fund-activity.html"
    out.write_text(page)
    print(f"wrote {out}: {len(meetings)} meetings, {all_actions} actions, {len(by_fund)} funds")


if __name__ == "__main__":
    main()

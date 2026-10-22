#!/usr/bin/env python3
"""Build the fund browser page from every ledger in data/funds.

Usage:  python3 tools/build_funds_index.py data/funds docs/funds.html
"""
import glob
import html
import json
import sys
from pathlib import Path

TYPE_LABEL = {"general": "General", "special_revenue": "Special revenue", "capital_project": "Capital project",
              "debt_service": "Debt service", "enterprise": "Enterprise", "internal_service": "Internal service"}


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def m(n):
    if n is None:
        return "—"
    s = f"{abs(n):,.0f}"
    return f"−${s}" if n < 0 else f"${s}"


def main(data_dir, out_path):
    funds = []
    for f in sorted(glob.glob(f"{data_dir}/*.json")):
        d = json.loads(Path(f).read_text())
        aud = [y for y in d["annual"] if y["basis"] == "audited" and y["fy"] == 2025]
        y = aud[-1] if aud else d["annual"][-1]
        page = f"fund-{d['fund_number']}.html" if d["fund_number"] != "608" else "fund-608-marina.html"
        funds.append({
            "id": d["fund_number"], "name": d["name"], "type": d["type"], "page": page,
            "rev": y.get("revenue"), "exp": y.get("expenditure"), "ti": y.get("transfers_in") or 0,
            "to": y.get("transfers_out") or 0, "bal": y.get("ending_balance"),
            "flows": len(d.get("flows", [])), "curated": "generated_by" not in d,
        })
    rows = []
    for f in funds:
        res = (f["rev"] or 0) - (f["exp"] or 0) if f["rev"] is not None and f["exp"] is not None else None
        rows.append(
            f'<tr data-type="{esc(f["type"])}" data-name="{esc(f["name"]).lower()}" data-rev="{f["rev"] or 0}" data-exp="{f["exp"] or 0}" data-res="{res or 0}" data-ti="{f["ti"]}" data-bal="{f["bal"] or 0}">'
            f'<td><a href="{esc(f["page"])}">{esc(f["name"])}</a>{" <span class=\"cur\">ledger</span>" if f["curated"] else ""}</td>'
            f'<td>{esc(TYPE_LABEL.get(f["type"], f["type"]))}</td><td class="n">{m(f["rev"])}</td><td class="n">{m(f["exp"])}</td>'
            f'<td class="n {"neg" if (res or 0) < 0 else ""}">{m(res)}</td><td class="n">{m(f["ti"]) if f["ti"] else "—"}</td><td class="n">{m(f["bal"])}</td></tr>')
    n_types = {}
    for f in funds:
        n_types[f["type"]] = n_types.get(f["type"], 0) + 1
    deficits = sum(1 for f in funds if f["rev"] is not None and f["exp"] is not None and f["rev"] < f["exp"])
    transfers_in = sum(1 for f in funds if f["ti"])
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Every City Fund — Learn About Berkeley</title>
<meta name="description" content="All {len(funds)} funds in Berkeley's FY2025 audit: revenue, spending, transfers in and year-end balance for each, with a money-flow page per fund.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root{{ --navy:#2a3340; --slate:#3f4f63; --steel:#43698f; --steel-deep:#33567a; --paper:#f5f7f9; --card:#fff; --rule:#dde3ea; --rule-strong:#c3ccd6; --muted:#5d6b7a; --red:#a8322c; --hi:#2f6f57; --mod:#956613; --low:#a8322c; --unk:#6b7280; --maxw:1100px; }}
  *{{box-sizing:border-box}} body{{ margin:0; background:var(--paper); color:var(--navy); font-family:"Source Serif 4",Georgia,serif; font-size:17px; line-height:1.55; }}
  .wrap{{ max-width:var(--maxw); margin:0 auto; padding:0 26px; }} a{{ color:var(--steel-deep); }}
  .hubbar{{ background:var(--slate); color:#eef1f5; }} .hubbar-in{{ max-width:var(--maxw); margin:0 auto; padding:11px 26px; display:flex; justify-content:space-between; }}
  .hubbar a.back{{ font-family:"JetBrains Mono",monospace; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:#cdd6e0; text-decoration:none; }} .hubbar .stamp{{ font-family:"JetBrains Mono",monospace; font-size:10.5px; letter-spacing:.1em; text-transform:uppercase; color:#9fb0c1; }}
  .masthead{{ padding:44px 0 22px; border-bottom:2px solid var(--navy); }} .eyebrow{{ font-family:"JetBrains Mono",monospace; font-size:11.5px; letter-spacing:.16em; text-transform:uppercase; color:var(--steel-deep); margin-bottom:16px; }}
  h1{{ font-family:"Playfair Display",serif; font-size:clamp(1.9rem,5vw,2.8rem); line-height:1.05; margin:0 0 .3em; }} .dek{{ color:var(--muted); max-width:70ch; margin:0 0 18px; }}
  .statrow{{ display:grid; grid-template-columns:repeat(2,1fr); gap:12px; margin:18px 0; }} @media(min-width:620px){{ .statrow{{ grid-template-columns:repeat(4,1fr); }} }}
  .stat{{ background:var(--card); border:1px solid var(--rule-strong); padding:12px 14px; }} .stat .v{{ font-family:"Playfair Display",serif; font-weight:700; font-size:1.4rem; }} .stat .l{{ font-family:"JetBrains Mono",monospace; font-size:10px; letter-spacing:.03em; text-transform:uppercase; color:var(--muted); margin-top:6px; }}
  .controls{{ display:flex; flex-wrap:wrap; gap:10px; margin:18px 0 10px; align-items:center; font-family:"JetBrains Mono",monospace; font-size:11.5px; }}
  .controls input, .controls select{{ font:inherit; padding:6px 8px; border:1px solid var(--rule-strong); background:var(--card); }}
  .tw{{ overflow-x:auto; background:var(--card); border:1px solid var(--rule-strong); }} table{{ width:100%; border-collapse:collapse; font-size:.86rem; }}
  th,td{{ text-align:left; padding:7px 10px; border-bottom:1px solid var(--rule); vertical-align:top; }} th{{ font-family:"JetBrains Mono",monospace; font-size:10px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); background:#f3f6f9; white-space:nowrap; cursor:pointer; user-select:none; }}
  th.sorted::after{{ content:" ▾"; }} td.n{{ text-align:right; white-space:nowrap; font-variant-numeric:tabular-nums; }} td.neg{{ color:var(--red); }}
  .cur{{ font-family:"JetBrains Mono",monospace; font-size:9px; letter-spacing:.06em; text-transform:uppercase; color:var(--hi); border:1px solid var(--hi); padding:0 4px; margin-left:6px; vertical-align:middle; }}
  .cap{{ font-family:"JetBrains Mono",monospace; font-size:10.5px; color:var(--muted); margin:10px 0 0; line-height:1.5; }}
  footer{{ padding:28px 0 64px; font-family:"JetBrains Mono",monospace; font-size:11px; color:var(--muted); line-height:1.7; }} footer .bar{{ height:3px; background:var(--navy); margin:0 0 16px; width:48px; }}
</style>
<link rel="stylesheet" href="assets/kromer-theme.css">
</head>
<body>
<div class="hubbar"><div class="hubbar-in"><a class="back" href="index.html">&larr; Learn About Berkeley</a><span class="stamp">Fund browser · FY2025 audit</span></div></div>
<main class="wrap">
  <header class="masthead">
    <div class="eyebrow">Following the money</div>
    <h1>Every City fund, one line each</h1>
    <p class="dek">The budget shows 18 departments. The audit shows the same money in {len(funds)} legally separate funds. This is each fund's FY2025 revenue, spending, transfers in and year-end balance from the audit, with a page per fund showing where its money came from and went. Sort any column; filter by type or name.</p>
    <div class="statrow">
      <div class="stat"><div class="v">{len(funds)}</div><div class="l">Funds in the FY2025 ACFR statements</div></div>
      <div class="stat"><div class="v">{deficits}</div><div class="l">Spent more than they took in, FY2025</div></div>
      <div class="stat"><div class="v">{transfers_in}</div><div class="l">Received transfers from other funds</div></div>
      <div class="stat"><div class="v">{sum(1 for f in funds if f["curated"])}</div><div class="l">With a hand-read event ledger so far</div></div>
    </div>
  </header>
  <div class="controls">
    <input id="q" type="search" placeholder="filter by name" aria-label="filter by name">
    <select id="t" aria-label="fund type"><option value="">all types</option>{"".join(f'<option value="{k}">{v} ({n_types.get(k,0)})</option>' for k, v in TYPE_LABEL.items())}</select>
    <span id="count"></span>
  </div>
  <div class="tw"><table id="tbl"><thead><tr><th data-k="name">Fund</th><th data-k="type">Type</th><th data-k="rev" data-num>Revenue</th><th data-k="exp" data-num>Spending</th><th data-k="res" data-num>Result</th><th data-k="ti" data-num>Transfers in</th><th data-k="bal" data-num>Balance, June 30, 2025</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
  <p class="cap">Governmental funds: total revenues, total expenditures (including capital outlay and debt service), fund balance. Enterprise and internal service funds: operating revenues, operating expenses (including depreciation), total net position. Transfers in are shown separately; they are not revenue. Figures read by <code>tools/acfr_funds.py</code> from the FY2025 ACFR statement pages named on each fund page; row and column sums were checked against the statements' own totals. "Ledger" marks funds whose dated flow events have been read from Council documents.</p>
  <footer><div class="bar"></div>Learn About Berkeley &middot; built from public documents &middot; residents decide. Maintained by Steve Kromer, candidate for Berkeley City Council District 1.</footer>
</main>
<script>
(function(){{
  const q=document.getElementById('q'),t=document.getElementById('t'),tb=document.querySelector('#tbl tbody'),rows=[...tb.rows],count=document.getElementById('count');
  function apply(){{const s=q.value.trim().toLowerCase(),ty=t.value;let n=0;rows.forEach(r=>{{const ok=(!s||r.dataset.name.includes(s))&&(!ty||r.dataset.type===ty);r.style.display=ok?'':'none';if(ok)n++;}});count.textContent=n+' of '+rows.length;}}
  q.addEventListener('input',apply);t.addEventListener('change',apply);apply();
  document.querySelectorAll('th').forEach(th=>th.addEventListener('click',()=>{{const k=th.dataset.k,num=th.hasAttribute('data-num'),dir=th.classList.contains('sorted')&&!th.classList.contains('asc')?1:-1;
    document.querySelectorAll('th').forEach(x=>x.classList.remove('sorted','asc'));th.classList.add('sorted');if(dir===1)th.classList.add('asc');
    rows.sort((a,b)=>{{const av=num?+a.dataset[k]:a.dataset[k]||a.cells[0].textContent.toLowerCase(),bv=num?+b.dataset[k]:b.dataset[k]||b.cells[0].textContent.toLowerCase();return av<bv?dir:av>bv?-dir:0;}});rows.forEach(r=>tb.appendChild(r));}}));
}})();
</script>
</body>
</html>
'''
    Path(out_path).write_text(page)
    print(f"wrote {out_path}: {len(funds)} funds")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

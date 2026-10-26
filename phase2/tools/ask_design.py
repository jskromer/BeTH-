"""Presentation layer for the Ask BeTH pages: photographs, highlights and charts.

Presentation only. Nothing here reads or changes verification logic: build_answers.py verifies each answer, then
passes the verified answer and committed data files here to be drawn. Highlight values come from the verified facts
or from the verifier's recomputed arithmetic; chart values come from the committed phase2 data files.

Photographs come only from phase2/docs/assets/photos/credits.json, which records each image's source, location,
date, license and attribution. They are illustrative and are captioned as not being evidence for any figure.

Chart colors: the dataviz reference categorical palette, validated on the card surface #fffdf9 (blue/orange pass
all-pairs; the four-slot run passes adjacent pairs; aqua and yellow are under 3:1, so every segment carries a
visible label and the data are also in the sources table).
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CREDITS = ROOT / 'docs' / 'assets' / 'photos' / 'credits.json'
e = html.escape

BLUE, ORANGE, AQUA, YELLOW, LIGHT_BLUE = '#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#86b6ef'

# Per-question presentation. Card text carries no figures; highlights name a verified fact or calculation.
PRESENTATION = {
    'capital-to-streets': {
        'kicker': 'Capital budget', 'card_title': 'Can capital money fix our streets?',
        'card_text': 'Berkeley\'s capital budget pays for buildings, parks, sewers and streets. How much of it could '
                     'move to paving, and what would have to give way?',
        'highlights': [('c1', 'The most fund 501 could free over two years, and only by delaying every other project it '
                               'pays for. A budget ceiling, not cash.'),
                       ('c3', 'Share of fund 501\'s FY2027 capital money that already goes to paving.'),
                       ('c4', 'One-time ceiling in unspent past budgets at June 30, 2025. It already backs earlier '
                               'projects.')]},
    'measure-ff-paving': {
        'kicker': 'Measure FF', 'card_title': 'Could Measure FF pave more streets?',
        'card_text': 'Voters approved a street tax with a fixed split between paving, sidewalks, safety and the '
                     'environment. Is there room to pave more?',
        'highlights': [('ff:program/total', 'The five-year Measure FF program, FY2027 to FY2031.'),
                       ('c1', 'Share of that program going to street repaving. The ordinance says "approximately" 45% '
                               'for streets.'),
                       ('ff:revenue/fy2027', 'Projected Measure FF revenue in FY2027.')]},
    'street-condition': {
        'kicker': 'Street condition', 'card_title': 'How bad are Berkeley\'s streets?',
        'card_text': 'The citywide average hides a lot. See how many miles of street score below the line Measure FF '
                     'set as its goal.',
        'highlights': [('pave:network/2024/average-pci', 'Citywide average pavement score in 2024, out of 100.'),
                       ('pave:network/2024/miles-below-50', 'Miles of street scoring below 50, the line in Measure '
                                                            'FF\'s goal.'),
                       ('c1', 'Share of the street network below 50.')]},
    'streets-139m': {
        'kicker': 'Street budget', 'card_title': 'What does the big streets figure include?',
        'card_text': 'A figure often quoted for street spending covers five years, not two. Here is what is in it, and '
                     'what has actually been budgeted.',
        'highlights': [('cip:streets/five-year/printed-total', 'Streets capital budget over five years, FY2027 to '
                                                                'FY2031.'),
                       ('c2', 'The two-year amount, FY2027 and FY2028, adopted in the current budget. The other three '
                              'years are plans.')]},
}

RESTRICTION_LABEL = {'unknown': 'Restriction not yet researched', 'voter_approved_tax': 'Voter-approved taxes',
                     'council_discretionary': 'Council can redirect (fund 501)', 'grant_condition': 'Grants',
                     'enterprise_fund': 'Enterprise funds', 'internal_service': 'Internal service funds'}


def photos():
    return json.loads(CREDITS.read_text())['photos']


def money(v):
    return f'${v:,.0f}'


def millions(v):
    return f'${v / 1e6:,.1f}M'


# ------------------------------------------------------------------ photo

def photo_figure(use, prefix, cls='hero'):
    p = photos()[use]
    src = f'{prefix}{p["file"]}'
    credit = (f'<a href="{e(p["source_page"])}">Photo: {e(p["author"])}</a>, '
              f'<a href="{e(p["license_url"])}">{e(p["license"])}</a>, via Wikimedia Commons')
    return (f'<figure class="{cls}-photo"><img src="{e(src)}" alt="{e(p["alt"])}" width="{p["width"]}" '
            f'height="{p["height"]}" loading="{"eager" if cls == "hero" else "lazy"}" data-photo="{e(use)}">'
            f'</figure>', credit, p)


def photo_caption(p, credit, credits_href):
    return (f'<p class="photo-note"><span class="tag">Illustrative photo</span> {e(p["description"])}, {e(p["date"])}. '
            f'It does not show evidence for the figures on this page. {credit}. '
            f'<a href="{e(credits_href)}">All photo credits</a></p>')


# ------------------------------------------------------------------ highlights

def highlight_values(ans, fmt):
    """(display value, label, ref) for each highlight, taken from verified facts or recomputed arithmetic."""
    facts = {f['fact_id']: f for f in ans['facts']}
    calcs = {a['id']: a for a in ans['verifier']['arithmetic']}
    out = []
    for ref, label in PRESENTATION[ans['slug']]['highlights']:
        if ref in calcs:
            v = fmt({'value': calcs[ref]['recomputed'], 'unit': calcs[ref]['unit']})
        else:
            v = fmt(facts[ref])
        out.append((v, label, ref))
    return out


def highlights_html(ans, fmt):
    return '<div class="stats">' + ''.join(
        f'<div class="stat"><div class="stat-v">{e(v)}</div><div class="stat-l">{e(l)}</div>'
        f'<div class="tech"><code>{e(r)}</code></div></div>' for v, l, r in highlight_values(ans, fmt)) + '</div>'


# ------------------------------------------------------------------ charts (HTML/CSS bars, labels always visible)

def bars(rows, note_total=None):
    """rows: (label, value, display, color). Horizontal bars scaled to the largest value."""
    top = max(r[1] for r in rows)
    out = ''.join(f'<div class="bar-row" title="{e(l)}: {e(d)}"><div class="bar-l">{e(l)}</div>'
                  f'<div class="bar-t"><span class="bar-f" style="width:{v / top * 100:.1f}%;background:{c}"></span>'
                  f'<span class="bar-v">{e(d)}</span></div></div>' for l, v, d, c in rows)
    return f'<div class="bars">{out}</div>'


def stack(label, segs):
    """segs: (name, value, display, color). One 100% bar with a 2px surface gap between segments."""
    tot = sum(s[1] for s in segs)
    bar = ''.join(f'<span class="seg" style="flex:{s[1] / tot * 100:.2f};background:{s[3]}" '
                  f'title="{e(s[0])}: {e(s[2])}"><span class="seg-v">{e(s[2]) if s[1] / tot >= 0.08 else ""}</span></span>'
                  for s in segs)
    key = ''.join(f'<li><span class="sw" style="background:{s[3]}"></span>{e(s[0])} <b>{e(s[2])}</b></li>' for s in segs)
    return f'<div class="stack"><div class="stack-l">{e(label)}</div><div class="stack-bar">{bar}</div><ul class="key">{key}</ul></div>'


def legend(items):
    return '<ul class="key">' + ''.join(f'<li><span class="sw" style="background:{c}"></span>{e(t)}</li>'
                                        for t, c in items) + '</ul>'


def chart(title, sub, body, source):
    return (f'<figure class="chart"><figcaption><h3>{e(title)}</h3><p>{e(sub)}</p></figcaption>{body}'
            f'<p class="chart-src">{e(source)}</p></figure>')


def chart_street_condition(nc):
    bands = nc['distribution']['by_mtc_band']
    order = ['very good (80-100)', 'good (70-79)', 'fair (60-69)', 'at risk (50-59)', 'poor (25-49)', 'failed (0-24)']
    rows = [(k[0].upper() + k[1:], bands[k]['centerline_miles_unrounded'], f'{bands[k]["centerline_miles"]:.1f} mi',
             ORANGE if k.startswith(('poor', 'failed')) else BLUE) for k in order]
    below = bands['poor (25-49)']['centerline_miles_unrounded'] + bands['failed (0-24)']['centerline_miles_unrounded']
    body = legend([('PCI 50 or above', BLUE), (f'Below PCI 50: {below:.1f} miles in all', ORANGE)]) + bars(rows)
    return chart('Miles of street in each condition band, 2024',
                 'Pavement Condition Index (PCI) bands used by the Metropolitan Transportation Commission. Measure FF\'s '
                 'goal is PCI 70, "ideally with no streets having a PCI below 50".', body,
                 'Source: BeTH sum of 1,216 street sections in the City\'s 2024 pavement condition report (PDF pages '
                 '40-67), lengths in feet converted to miles. One uninspected section is excluded, as in the report\'s '
                 'totals.')


def chart_measure_ff(sf):
    prog = sf['funding_sources'][1]['allocation_fixed_by_voters']['adopted_five_year_program']
    other_ss = prog['streets_and_sidewalks'] - prog['street_rehabilitation_cip']
    tot = prog['total']
    pct = lambda v: f'{v / tot:.1%}'
    law = stack('What the ordinance says ("approximately")',
                [('Streets', 45, '45%', BLUE), ('Sidewalks and paths', 15, '15%', ORANGE),
                 ('Safety', 30, '30%', AQUA), ('Environmental and other', 10, '10%', YELLOW)])
    plan = stack('What the adopted five-year program does',
                 [('Street rehabilitation', prog['street_rehabilitation_cip'], pct(prog['street_rehabilitation_cip']), BLUE),
                  ('Other street and sidewalk work', other_ss, pct(other_ss), ORANGE),
                  ('Safety', prog['safety'], pct(prog['safety']), AQUA),
                  ('Environmental', prog['environmental'], pct(prog['environmental']), YELLOW)])
    return chart('How Measure FF money is split',
                 'The voters\' split, and the City\'s adopted five-year program. The two use different categories, so '
                 'the comparison is approximate.', law + plan,
                 'Sources: Measure FF ordinance, BMC 7.11.020(C), PDF page 8; July 2026 street plan, Table 1C (page 4); '
                 'adopted budget page 215. Program shares are BeTH\'s arithmetic from those tables.')


def chart_streets_budget(cip):
    t = cip['categories']['Streets']['printed_grand_total']
    years = ['fy2027', 'fy2028', 'fy2029', 'fy2030', 'fy2031']
    top = max(t[y] for y in years)
    cols = ''.join(f'<div class="col" title="FY{y[2:]}: {money(t[y])}"><span class="col-v">{millions(t[y])}</span>'
                   f'<span class="col-f" style="height:{t[y] / top * 100:.1f}%;background:{BLUE if i < 2 else LIGHT_BLUE}">'
                   f'</span><span class="col-l">FY{y[2:]}</span></div>' for i, y in enumerate(years))
    two, five = t['fy2027'] + t['fy2028'], t['five_year_budget']
    brackets = (f'<div class="brk"><span class="brk-2">Two years: {money(two)}</span>'
                f'<span class="brk-5">Five years: {money(five)}</span></div>')
    body = legend([('Adopted in the two-year budget', BLUE), ('Planned, not yet budgeted', LIGHT_BLUE)]) + \
        brackets + f'<div class="cols">{cols}</div>'
    return chart('Streets capital budget by year',
                 'The five-year figure includes three years of plans that a future budget must still adopt.', body,
                 'Source: FY2027-28 adopted budget, capital program table by category, page 169.')


def chart_capital(sf, restrictions):
    a = sf['funding_sources'][0]['appropriations_adopted_cip']['fy2027']
    split = stack('Fund 501, FY2027 capital program',
                  [('Paving', a['paving'], money(a['paving']), BLUE),
                   ('Everything else (roofs, buildings, pool, sidewalks and more)', a['other'], money(a['other']), ORANGE)])
    rows = [(RESTRICTION_LABEL.get(r['class'], r['class']), r['two_year'], millions(r['two_year']),
             ORANGE if r['class'] == 'council_discretionary' else BLUE)
            for r in restrictions if r['class'] != 'unfunded_need']
    by = legend([('Council can redirect without a vote', ORANGE), ('Other funding', BLUE)]) + bars(rows)
    return (chart('Where fund 501\'s capital money goes',
                  'Fund 501 is the capital money Council controls most directly. Most of it is already paving.', split,
                  'Source: FY2027-28 adopted budget, fund 501 project table, pages 172-173.')
            + chart('FY2027-28 capital budget by type of restriction',
                    'Budget amounts, not cash. "Not yet researched" means BeTH has not established the legal limits on '
                    'that money; it is not treated as available.', by,
                    'Source: BeTH classification of every funding line in the FY2027-28 adopted capital program. '
                    '"Unfunded need" rows carry no money and are left out.'))


# ------------------------------------------------------------------ stylesheet

CSS = '''
:root{--navy:#1b3a63;--navy-deep:#0f2440;--blue:#2a78d6;--paper:#f6f3ec;--card:#fffdf9;--ink:#1a1f2b;--muted:#5b616e;
--gold:#a87620;--gold-soft:#f4e8c8;--rule:#e3dccd;--warn:#8a4b08;--ok:#1f6b4a;
--serif:"Iowan Old Style","Palatino Linotype","Book Antiqua",Palatino,Georgia,serif;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.6 var(--sans)}
a{color:var(--navy)}
img{max-width:100%;display:block}
.wrap{max-width:1080px;margin:0 auto;padding-inline:20px}
.narrow{max-width:780px;margin:0 auto;padding-inline:20px}
.topbar{background:var(--navy-deep);color:#fff;font-size:14px}
.topbar .wrap{display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center;justify-content:space-between;padding-block:10px}
.topbar a{color:#fff;text-decoration:none}.brand{font-family:var(--serif);font-size:19px;font-weight:700;letter-spacing:.01em}
.brand span{color:#e6c77a}.topnav{display:flex;gap:16px}.topnav a{opacity:.85}.topnav a:hover{opacity:1;text-decoration:underline}
.proto{background:var(--gold-soft);color:var(--warn);font-size:13px;font-weight:600;text-align:center;padding:6px 12px}
/* hero */
.hero{position:relative;color:#fff;background:var(--navy-deep);overflow:hidden}
.hero-photo{position:absolute;inset:0;margin:0}
.hero-photo img{width:100%;height:100%;object-fit:cover}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,36,64,.25) 0%,rgba(15,36,64,.55) 45%,rgba(15,36,64,.92) 100%)}
.hero-in{position:relative;z-index:1;padding-block:clamp(90px,16vw,170px) 40px}
.kicker{display:inline-block;font-size:13px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#f0d38a;
border-bottom:2px solid #c99a3a;padding-bottom:2px;margin-bottom:12px}
.hero h1{font-family:var(--serif);font-weight:700;font-size:clamp(2rem,4.6vw,3.3rem);line-height:1.12;margin:0 0 10px;max-width:22ch;text-wrap:balance}
.hero .sub{font-size:clamp(1.1rem,2.2vw,1.4rem);max-width:40ch;margin:0;color:#f3efe6}
.home .hero-in{padding-block:clamp(120px,22vw,230px) 56px}
.home .hero h1{font-size:clamp(2.6rem,7vw,4.6rem)}
/* answer */
.lead{position:relative;z-index:2;margin-top:-28px}
.answer{background:var(--card);border-radius:10px;box-shadow:0 10px 30px rgba(15,36,64,.12);padding:22px 24px;border-top:4px solid var(--gold)}
.lbl{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.answer p{font-family:var(--serif);font-size:clamp(1.2rem,2.4vw,1.45rem);line-height:1.45;margin:.35em 0 0}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:18px 0}
.stat{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:16px 18px}
.stat-v{font-family:var(--serif);font-weight:700;color:var(--navy);font-size:clamp(1.45rem,2.3vw,1.85rem);line-height:1.15;white-space:nowrap}
.stat-l{font-size:15px;color:var(--muted);margin-top:6px}
.know{background:#fff6e2;border:1px solid #ecd6a4;border-radius:10px;padding:14px 20px;margin:18px 0}
.know ul{margin:.4em 0 0;padding-left:1.2em}.know li{margin:.35em 0}
.status{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0;font-size:14px}
.pill{border:1px solid var(--rule);background:var(--card);border-radius:999px;padding:3px 11px}
.pill.ok{color:var(--ok)}.pill.no{color:var(--warn)}
.photo-note{font-size:13px;color:var(--muted);margin:14px 0 0}
.photo-note .tag{font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:11px;color:var(--gold)}
h2.sec{font-family:var(--serif);font-size:1.6rem;margin:40px 0 6px}
p.sec-sub{color:var(--muted);margin:0 0 14px}
/* charts */
.chart{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:18px 20px;margin:14px 0}
.chart h3{font-size:1.1rem;margin:0}.chart figcaption p{margin:.2em 0 .8em;color:var(--muted);font-size:15px}
.chart-src{font-size:13px;color:var(--muted);margin:12px 0 0;border-top:1px solid var(--rule);padding-top:8px}
.key{list-style:none;padding:0;margin:0 0 10px;display:flex;flex-wrap:wrap;gap:6px 16px;font-size:14px}
.key li{display:flex;align-items:center;gap:6px}.sw{width:12px;height:12px;border-radius:3px;flex:none}
.bars{display:grid;gap:8px}
.bar-row{display:grid;grid-template-columns:minmax(120px,32%) 1fr;gap:10px;align-items:center;font-size:14px}
.bar-t{display:flex;align-items:center;gap:8px;min-width:0}
.bar-f{height:18px;border-radius:0 4px 4px 0;min-width:2px}
.bar-v{white-space:nowrap;font-variant-numeric:tabular-nums;color:var(--ink)}
.stack{margin:6px 0 14px}.stack-l{font-size:14px;font-weight:600;margin-bottom:4px}
.stack-bar{display:flex;gap:2px;height:30px;border-radius:4px;overflow:hidden;background:var(--card)}
.seg{display:flex;align-items:center;justify-content:center;min-width:2px}
.seg-v{color:#fff;font-size:13px;font-weight:700;text-shadow:0 0 3px rgba(0,0,0,.45)}
.stack .key{margin-top:8px}
.cols{display:flex;align-items:flex-end;gap:10px;height:220px;padding-top:24px;border-bottom:1px solid #c3c2b7}
.col{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%;position:relative;font-size:13px}
.col-f{width:100%;max-width:90px;border-radius:4px 4px 0 0}
.col-v{white-space:nowrap;margin-bottom:4px;font-variant-numeric:tabular-nums}
.col-l{position:absolute;bottom:-22px;font-size:13px;color:var(--muted)}
.brk{display:grid;grid-template-columns:2fr 3fr;font-size:13px;font-weight:600;margin-top:6px}
.brk span{border-top:2px solid var(--navy);padding-top:3px;margin-right:10px}
.brk .brk-5{grid-column:1/3;margin-top:6px;border-color:var(--gold);margin-right:0}
.chart .cols+*{margin-top:28px}
/* details */
details{background:var(--card);border:1px solid var(--rule);border-radius:10px;margin:10px 0}
summary{cursor:pointer;padding:14px 18px;font-weight:650}
summary span{font-weight:400;color:var(--muted);font-size:14px}
details>div{padding:0 18px 16px}
.tw{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:15px}
th,td{text-align:left;vertical-align:top;padding:8px 6px;border-bottom:1px solid var(--rule)}
td.n{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.basis{font-size:12px;color:var(--muted);white-space:nowrap}
blockquote{margin:4px 0 0;padding-left:10px;border-left:3px solid var(--gold-soft);color:var(--muted);font-size:14px}
ul.plain{padding-left:1.2em}ul.plain li{margin:.45em 0}
.note,.cap{color:var(--muted);font-size:14px}
.tech{display:none;font-size:12.5px;color:var(--muted);margin-top:3px}
code{font-size:12px;background:#efeadf;padding:0 3px;border-radius:3px}
body:has(#tech:checked) .tech{display:block}
.techtoggle{font-size:14px;color:var(--muted);display:inline-flex;gap:6px;align-items:center;margin-top:18px}
/* home */
.cards{display:grid;grid-template-columns:1fr;gap:22px;margin:8px 0 10px}
@media (min-width:720px){.cards{grid-template-columns:repeat(2,1fr)}}
.card{background:var(--card);border-radius:12px;overflow:hidden;border:1px solid var(--rule);display:flex;flex-direction:column;
text-decoration:none;color:inherit;transition:transform .15s ease,box-shadow .15s ease}
.card:hover,.card:focus-within{transform:translateY(-3px);box-shadow:0 14px 30px rgba(15,36,64,.14)}
.card .credit a{color:var(--muted)}
.card-photo{margin:0;aspect-ratio:3/2;overflow:hidden}.card-photo img{width:100%;height:100%;object-fit:cover}
.card-b{padding:16px 18px 18px;display:flex;flex-direction:column;gap:6px;flex:1}
.card .kicker{color:var(--gold);border-color:var(--gold-soft);margin:0;font-size:12px}
.card h3{font-family:var(--serif);font-size:1.4rem;line-height:1.2;margin:0}.card h3 a{color:var(--navy);text-decoration:none}
.card h3 a:hover{text-decoration:underline}.card-link{display:block}
.card p{margin:0;color:var(--ink)}.card .answer-line{color:var(--muted);font-size:15px;border-left:3px solid var(--gold-soft);padding-left:10px}
.card .go{margin-top:auto;font-weight:650;color:var(--navy);padding-top:6px;text-decoration:none}
.card .credit{font-size:11.5px;color:var(--muted)}
.how{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin:10px 0 0}
.how div{border-top:3px solid var(--gold);padding-top:10px}.how b{font-family:var(--serif);font-size:1.15rem;color:var(--navy)}
.how p{margin:.3em 0 0;color:var(--muted);font-size:15px}
footer{background:var(--navy-deep);color:#d9dee8;font-size:14px;margin-top:56px}
footer .wrap{padding-block:26px}footer a{color:#fff}
.credits-list li{margin:.8em 0}
@media (max-width:560px){body{font-size:16px}.bar-row{grid-template-columns:1fr;gap:2px}.answer{padding:18px}
.cols{gap:6px}.col-v{font-size:11px}.topnav{gap:12px}}
'''


def shell(title, body, prefix, description=''):
    """prefix: path from the page to phase2/docs/ (e.g. '../')."""
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title>'
            + (f'<meta name="description" content="{e(description)}">' if description else '')
            + f'<link rel="stylesheet" href="{prefix}assets/ask.css"></head><body>'
            f'<header class="topbar"><div class="wrap"><a class="brand" href="{prefix}ask/index.html">Be<span>TH</span> '
            f'<span style="color:#fff;font-weight:400;font-size:15px">Berkeley Transparency Hub</span></a>'
            f'<nav class="topnav"><a href="{prefix}ask/index.html">Ask BeTH</a>'
            f'<a href="{prefix}budget-choices.html">Budget choices</a>'
            f'<a href="{prefix}ask/photo-credits.html">Photo credits</a></nav></div></header>'
            f'<div class="proto">Prototype for review. Not published. Answers are checked automatically but not yet '
            f'confirmed by a person.</div>{body}'
            f'<footer><div class="wrap">BeTH answers come only from City of Berkeley records, each linked to the page it '
            f'relies on. Photographs are illustrative and are not evidence. '
            f'<a href="{prefix}ask/photo-credits.html">Photo credits and licenses</a>.</div></footer>'
            '<script>var t=document.getElementById("tech");if(t)t.addEventListener("change",function(e){'
            'if(e.target.checked)document.querySelectorAll("details").forEach(function(d){d.open=true})})</script>'
            '</body></html>\n')


def credits_page():
    items = ''
    for use, p in photos().items():
        items += (f'<li><img src="../{e(p["file"])}" alt="{e(p["alt"])}" width="240" style="border-radius:6px;margin-bottom:6px" '
                  f'loading="lazy"><b>{e(p["alt"])}</b><br>Used on: {e(use)} · Location: {e(p["location"])} · Date: '
                  f'{e(p["date"])}<br>Author: {e(p["author"])} · License: <a href="{e(p["license_url"])}">'
                  f'{e(p["license"])}</a> · Source: <a href="{e(p["source_page"])}">Wikimedia Commons file page</a>'
                  f'<br><span class="note">Illustrative only; not evidence for any figure. Rendition: Commons '
                  f'{p["width"]}-pixel version, unmodified. SHA-256 {e(p["sha256"][:16])}…</span></li>')
    body = (f'<main class="narrow" style="padding-block:28px"><h1 style="font-family:var(--serif)">Photo credits</h1>'
            f'<p>Every photograph on the Ask BeTH pages is listed here with its source, location, date, license and author. '
            f'Each is used under the license stated on its Wikimedia Commons file page. The photographs illustrate places '
            f'in Berkeley; none of them is evidence for a financial or street-condition figure.</p>'
            f'<ul class="plain credits-list">{items}</ul>'
            f'<p class="note">Machine-readable record: <code>phase2/docs/assets/photos/credits.json</code>.</p></main>')
    return shell('Photo credits — Ask BeTH (prototype)', body, '../')

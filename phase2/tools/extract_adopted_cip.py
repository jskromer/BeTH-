#!/usr/bin/env python3
"""Extract every project funding line from the adopted FY2027-2031 CIP (Exhibit B of the
June 23, 2026 budget adoption packet) and reconcile it three ways before writing anything.

Source: phase2/sources/budget-adoption-2026-06-23.txt (pdftotext -layout of the 260-page
"Adoption of Fiscal Years 2027 and 2028 Biennial Budget and Fiscal Years 2027-2031 Capital
Improvement Program", City Council Special Meeting Item 01, June 23, 2026).

Each project table row carries nine amounts:
  prior fiscal years | FY2026 budget | FY2027 | FY2028 | FY2029 | FY2030 | FY2031 | project total | five-year budget
Those are APPROPRIATIONS AND PLANS, not cash, not expenditures, not encumbrances.

Checks (all must pass or nothing is written):
  1. every project's funding lines sum to its printed "<title> Total" row, all nine columns;
  2. every category's projects sum to its printed "Grand Total" row and match "N Projects in Five-Year CIP";
  3. the City's summary tables, year by year (FY2027-FY2031):
     - p.169 by category: every category's funded lines (Unfunded Need excluded) match; Equipment & Fleet is the
       vehicle schedule ($33,331,116), taken from p.169 because it has no project rows;
     - p.170 by funding source: all 29 printed rows match the project lines of the funds they name (Equipment
       Replacement = fund 671 EV-charger projects + the fleet schedule, so neither is counted twice);
     - the City's two printed totals are both kept: $410,618,590 by category and $410,468,590 by funding source.
       The $150,000 difference is fund 621 (Clariti project), absent from p.170. It is recorded, not forced.

Run:  python3 phase2/tools/extract_adopted_cip.py            # check only
      python3 phase2/tools/extract_adopted_cip.py --write    # check, then write phase2/data/cip-projects.json
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources' / 'budget-adoption-2026-06-23.txt'
OUT = ROOT / 'data' / 'cip-projects.json'
PRESENTATION = ROOT / 'data' / 'cip-presentation.json'

COLS = ['prior_years', 'fy2026_budget', 'fy2027', 'fy2028', 'fy2029', 'fy2030', 'fy2031',
        'project_total', 'five_year_budget']
CATEGORY = re.compile(r'Capital Improvement Pro(?:gram|ject)\s*-\s*([A-Za-z][A-Za-z ]+?)\s*$')
FUND = re.compile(r'(?<![\d,$])(\d{3}) -')
MONEY = re.compile(r'-|\d{1,3}(?:,\d{3})*')
COUNT = re.compile(r'(\d+) Projects in Five-Year CIP')
PROJNO = re.compile(r'\s(TBD|[A-Z]{4,}\d{3,}[A-Z0-9/]*)\s+(New|Continuing)\s*$')
FURNITURE = re.compile(r'City of Berkeley|Program Categories|Page \d+ of|^FY 2027 - FY 2031$|Project\s+New or|'
                       r'Project Title|Fiscal Years|^\s*FY 2031\s*$|^\s*FY 2027 -\s*$|^[A-Z &]+$')
# Category name as printed -> category label used in the inventory
CATS = {'Facilities': 'Facilities', 'InformationTechnology': 'Information Technology', 'Parks': 'Parks',
        'Camps': 'Camps', 'Waterfront': 'Waterfront', 'Sanitary Sewer System': 'Sanitary Sewer',
        'Sidewalk': 'Sidewalks', 'Storm Water System': 'Storm Water', 'Streets': 'Streets',
        'Transportation': 'Transportation', 'Other Infrastructure': 'Other Infrastructure'}
# City funding-source table (p.170): printed row label -> City fund numbers in the project tables.
FUNDING_TABLE_FUNDS = {
    'Capital Improvements': ['501'], 'Meas T1 - Infrstr And Fac': ['511'], 'Clean Storm Water': ['616'],
    'Marina Operations/Maint': ['608'], 'Sanitary Sewer Operation': ['611', 'NOT_PRINTED'], 'Zero Waste': ['601'],
    'GF Discretionary': ['011'], 'Capital Grants - Federal': ['305'], 'Capital Grants - Local': ['307'],
    'Capital Grants - State': ['306'], 'FEMA': ['340'], 'MTC': ['339'], 'One-Time Grant:No Cap Exp': ['336'],
    'Equipment Replacement': ['671'], 'It Cost Allocation': ['680'], 'Meas B - Bike And Pedestrian': ['131'],
    'Meas B - Local Streets and RDS': ['130'], 'Meas BB - Bike and Pedestrian': ['135'],
    'Meas BB - Local Streets and RD': ['134'], 'Meas F - ALA CT VRF ST and RD': ['133'],
    'Measure FF - Street Repair': ['166'], 'Miles Lab': ['145'], 'Park Tax': ['138'], 'Playground Camp': ['125'],
    'Private Party Sidewalks': ['149'], 'State Transportation Tax': ['127'], 'Street And Open Space Impr': ['139'],
    'Street Lighting': ['142'], 'UC Settlement': ['147'],
}
GROUP_LABELS = ('Capital Projects Funds', 'Enterprise Funds', 'General Fund', 'Grants Funds', 'Internal Service Funds',
                'Special Revenue Funds')
YEARS5 = ['fy2027', 'fy2028', 'fy2029', 'fy2030', 'fy2031']
# Discrepancies inside the City's document, recorded and never forced:
DOCUMENTED = {
    'fund_621_missing_from_p170': 'Fund 621 (Permit Service Center) funds one project, "Clariti Integration With Erma" '
        '($150,000, FY2028, Information Technology). The project and the p.169 category table include it; the p.170 '
        'funding-source table has no row for fund 621. Its group totals sum to $410,468,590, $150,000 less than the '
        'p.169 category total of $410,618,590. The p.171 chart labels Enterprise Funds $155,510,000 against the table\'s '
        '$155,360,000, the same $150,000. Unresolved: which total the City intends.',
}


DOLLAR = re.compile(r'(?<![A-Za-z])\$\s*(-|\d{1,3}(?:,\d{3})*)?')
SOURCE = re.compile(r'(?<![\d,$])(\d{3}) -|Unfunded(?: Need)?')
DOCUMENT_COUNT_EXCEPTIONS = {
    'Storm Water': 'The Storm Water tables (pp.210-212) print 13 project titles; p.212 states "14 Projects in Five-Year CIP". '
                   'Dollar totals tie exactly to the printed Grand Total, so no amount is missing; the stated count is not reproducible.',
}
PRINTED_ROUNDING_TOLERANCE = 2  # the City's printed totals differ from their own lines by $1-2 in places


def dollar_tokens(s):
    """Amounts that follow a '$' sign. An empty '$' (amount wrapped to the next line) is None."""
    out = []
    for m in DOLLAR.finditer(s):
        t = m.group(1)
        out.append(None if t is None else 0 if t == '-' else int(t.replace(',', '')))
    return out


def first_dollar(line):
    m = DOLLAR.search(line)
    return m.start() if m else len(line)


def fill_wrapped(toks, nxt):
    """Fill None placeholders from bare numbers printed on the following line."""
    if None not in toks:
        return toks
    bare = [int(x.replace(',', '')) for x in re.findall(r'(?<![\d,$])\d{1,3}(?:,\d{3})+', nxt)]
    out, k = [], 0
    for t in toks:
        if t is None and k < len(bare):
            out.append(bare[k]); k += 1
        else:
            out.append(t)
    return out


def clean_title(t):
    t = re.sub(r'\s+', ' ', t).strip()
    return re.sub(r'\s*Total\b.*$', '', t).strip()


def parse(lines):
    """A project is the run of funding lines (fund code or 'Unfunded Need') ending at its printed Total row.
    The title is taken from the Total row (some projects print it only there)."""
    projects, categories, problems = [], {}, []
    cat, buf, total, tline = None, [], None, None
    lines = [l.replace('\x08', ' ').replace('\u200b', '') for l in lines]

    def close(title_text, toks, i):
        nonlocal buf
        if not buf:
            problems.append(f'line {i}: total row with no funding lines: {title_text[:60]}')
            return
        first = buf[0]
        pn = PROJNO.search(first['pre'].rstrip())
        projects.append({'category': cat, 'title': clean_title(title_text),
                         'project_number': pn.group(1) if pn else None,
                         'new_or_continuing': pn.group(2) if pn else None,
                         'funding': [{k: v for k, v in f.items() if k != 'pre'} for f in buf],
                         'printed_total': toks, 'source_line': first['source_line']})
        buf = []

    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        m = CATEGORY.search(line)
        if m and m.group(1).strip() in CATS:
            cat = CATS[m.group(1).strip()]
            categories.setdefault(cat, {'grand_total': None, 'stated_count': None})
            continue
        if cat is None:
            continue
        c = COUNT.search(line)
        if c:
            categories[cat]['stated_count'] = int(c.group(1))
            if buf:
                problems.append(f'line {i}: {len(buf)} funding lines left without a total row in {cat}')
            cat, buf = None, []
            continue
        nxt = lines[i] if i < len(lines) else ''
        if re.match(r'\s*Grand Total\b', line):
            toks = fill_wrapped(dollar_tokens(line), nxt)
            if len(toks) == 9 and None not in toks:
                categories[cat]['grand_total'] = toks
            else:
                problems.append(f'line {i}: Grand Total for {cat} unreadable')
            continue
        toks = dollar_tokens(line)
        if len(toks) != 9:
            if '$' in line and len(toks) > 2:
                problems.append(f'line {i}: {len(toks)} amounts: {line.strip()[:110]}')
            elif buf and line.strip() and toks == []:
                # wrapped fund label: text at or right of the fund-source column
                col = buf[-1]['_col']
                seg = line[col:].strip() if len(line) > col else ''
                if seg and re.fullmatch(r'[A-Z0-9][A-Z0-9 &/.\-]*', seg) and not buf[-1]['fund_label_done']:
                    buf[-1]['fund_label'] = ((buf[-1]['fund_label'] or '') + ' ' + seg).strip()
                    buf[-1]['fund_label_done'] = True
            continue
        toks = fill_wrapped(toks, nxt)
        src = SOURCE.search(line[:first_dollar(line)])
        if src:
            fund = src.group(1) or 'UNFUNDED'
            label = line[src.end():first_dollar(line)].strip().rstrip('-').strip() if src.group(1) else 'Unfunded Need'
            buf.append({'fund': fund, 'fund_label': label or None, **dict(zip(COLS, toks)), 'source_line': i,
                        'pre': line[:src.start()], '_col': src.start(), 'fund_label_done': False})
            continue
        # No source printed on this row. It is the project's total if its amounts equal the sum of the
        # funding lines collected since the last total (within the City's own $1-2 rounding); otherwise it is
        # a funding line whose source the document does not print (never inferred).
        sums = [sum(f[c] for f in buf) for c in COLS] if buf else None
        if sums and max(abs(x - y) for x, y in zip(sums, toks)) <= PRINTED_ROUNDING_TOLERANCE:
            title = line[:first_dollar(line)].strip()
            j, steps = i, 0
            while not title.endswith('Total') and j < len(lines) and steps < 10:
                t = lines[j].strip()
                j += 1
                steps += 1
                if not t or FURNITURE.search(t):
                    continue
                if DOLLAR.search(t):
                    break
                title = (title + ' ' + t).strip()
            core = title.replace('Total', '').strip()
            if len(re.sub(r'[\d\s\-]', '', core)) < 3:
                # the title wrapped around the amounts (e.g. "Street Rehabilitation FY" ... "2027 Total"):
                # take the text from the first funding line and append the fragment
                pre = PROJNO.sub('', re.sub(r'\s+', ' ', buf[0]['pre'])).strip()
                title = (pre + ' ' + title).strip()
            close(title, toks, i)
        else:
            buf.append({'fund': 'NOT_PRINTED', 'fund_label': None, **dict(zip(COLS, toks)), 'source_line': i,
                        'pre': line[:first_dollar(line)], '_col': first_dollar(line), 'fund_label_done': True})
    if buf:
        problems.append(f'end: {len(buf)} funding lines left without a total row')
    for p in projects:
        for f in p['funding']:
            f.pop('_col', None); f.pop('fund_label_done', None)
    return projects, categories, problems


ROUNDING = []


def city_tables():
    """The City's summary tables: p.169 by category, p.170 by funding source (six printed amounts per row)."""
    lines = SRC.read_text().split('\n')

    def rows(first, last):
        out, on = {}, False
        for l in lines:
            if f'Page {first} of 260' in l:
                on = True
            if f'Page {last} of 260' in l:
                break
            if not on or '$' not in l:
                continue
            l = l.replace('\x08', ' ')
            toks = [m.group(1) for m in DOLLAR.finditer(l)]
            if len(toks) != 6:
                continue
            label = re.sub(r'^\s*(Capital Improvement Program Overview)?\s*', '', l[:first_dollar(l)]).strip()
            out[label] = [0 if t in (None, '-') else int(t.replace(',', '')) for t in toks]
        return out
    cat = rows(169, 170)
    fs_raw = rows(170, 171)
    groups = {k: v[5] for k, v in fs_raw.items() if k.endswith(' Total')}
    fs = {}
    for k, v in fs_raw.items():
        if k.endswith(' Total'):
            continue
        for g in GROUP_LABELS:
            if k.startswith(g + ' '):
                k = k[len(g):].strip()
        if k in GROUP_LABELS or not k:
            continue
        fs[k] = v
    return cat, fs, groups


def checks(projects, categories):
    errors = []
    for p in projects:
        s = [sum(f[c] for f in p['funding']) for c in COLS]
        if p['printed_total'] is None:
            errors.append(f"{p['category']}: '{p['title']}' has no printed total row")
        elif s != p['printed_total']:
            d = [a - b for a, b in zip(s, p['printed_total'])]
            if max(abs(x) for x in d) <= PRINTED_ROUNDING_TOLERANCE:
                ROUNDING.append({'where': f"{p['category']}: {p['title']}", 'lines_minus_printed': dict(zip(COLS, d))})
            else:
                errors.append(f"{p['category']}: '{p['title']}' funding lines {s} != printed total {p['printed_total']}")
    for cat, info in categories.items():
        ps = [p for p in projects if p['category'] == cat]
        s = [sum(f[c] for p in ps for f in p['funding']) for c in COLS]
        if info['grand_total'] != s:
            d = [a - b for a, b in zip(s, info['grand_total'])]
            if max(abs(x) for x in d) <= PRINTED_ROUNDING_TOLERANCE:
                ROUNDING.append({'where': f'{cat}: Grand Total', 'lines_minus_printed': dict(zip(COLS, d))})
            else:
                errors.append(f'{cat}: projects sum {s} != printed Grand Total {info["grand_total"]}')
        if info['stated_count'] != len(ps) and cat not in DOCUMENT_COUNT_EXCEPTIONS:
            errors.append(f'{cat}: {len(ps)} projects parsed, document states {info["stated_count"]}')
    by_fund = {}
    for p in projects:
        for f in p['funding']:
            by_fund[f['fund']] = by_fund.get(f['fund'], 0) + f['five_year_budget']
    cat_table, fs_table, groups = city_tables()
    funded = {}
    fund_years = {}
    for p in projects:
        for f in p['funding']:
            if f['fund'] == 'UNFUNDED':
                continue
            c = funded.setdefault(p['category'], [0] * 5)
            fy = fund_years.setdefault(f['fund'], [0] * 5)
            for i, y in enumerate(YEARS5):
                c[i] += f[y]
                fy[i] += f[y]
    cat_check = {}
    for label, vals in cat_table.items():
        if label == 'Grand Total':
            continue
        if label == 'Equipment & Fleet':
            cat_check[label] = {'city_p169': vals, 'parsed': None,
                                'note': 'Vehicle replacement schedule (pp.231-247), not project rows; value taken from p.169.'}
            continue
        got = funded.get(label)
        cat_check[label] = {'city_p169': vals, 'parsed_funded': got + [sum(got)] if got else None,
                            'match': bool(got) and got == vals[:5]}
        if not cat_check[label]['match']:
            errors.append(f'category {label}: parsed funded {got} != p.169 {vals[:5]}')
    fund_check = {}
    used = set()
    for label, vals in fs_table.items():
        funds = FUNDING_TABLE_FUNDS.get(label)
        if funds is None:
            errors.append(f'p.170 row not mapped: {label}')
            continue
        used.update(funds)
        got = [sum(fund_years.get(fn, [0] * 5)[i] for fn in funds) for i in range(5)]
        note = None
        if label == 'Equipment Replacement':
            fleet = cat_table['Equipment & Fleet'][:5]
            got = [a + b for a, b in zip(got, fleet)]
            note = ('Project lines of fund 671 (four Fleet EV Charger projects, $6,021,000, Other Infrastructure) plus the '
                    'Equipment & Fleet vehicle schedule ($33,331,116, p.169).')
        if label == 'Sanitary Sewer Operation':
            note = 'Includes four Sanitary Sewer rows that print no funding source (kept as NOT_PRINTED in the project data).'
        fund_check[label] = {'funds': funds, 'city_p170': vals, 'parsed': got + [sum(got)], 'match': got == vals[:5],
                             'note': note}
        if got != vals[:5]:
            errors.append(f'funding source {label}: parsed {got} != p.170 {vals[:5]}')
    unlisted = {fn: sum(v) for fn, v in fund_years.items() if fn not in used and sum(v)}
    if set(unlisted) - {'621'} or unlisted.get('621') not in (None, 150000):
        errors.append(f'project funding not in the p.170 table: {unlisted}')
    totals = {
        'by_category_p169': cat_table['Grand Total'][5],
        'by_funding_source_p170_sum_of_group_totals': sum(groups.values()),
        'difference': cat_table['Grand Total'][5] - sum(groups.values()),
        'project_funding_absent_from_p170': unlisted,
        'explanation': DOCUMENTED['fund_621_missing_from_p170'],
        'unfunded_need_excluded_from_city_totals': sum(f['five_year_budget'] for p in projects for f in p['funding']
                                                       if f['fund'] == 'UNFUNDED'),
    }
    if totals['difference'] != sum(unlisted.values()):
        errors.append(f'City totals differ by {totals["difference"]:,}, not explained by {unlisted}')
    fund_check = {'categories_p169': cat_check, 'funding_sources_p170': fund_check, 'city_totals': totals}
    return errors, by_fund, fund_check


def main(argv):
    lines = SRC.read_text().split('\n')
    projects, categories, problems = parse(lines)
    errors, by_fund, fund_check = checks(projects, categories)
    print(f'{len(projects)} projects in {len(categories)} categories; '
          f'{sum(len(p["funding"]) for p in projects)} funding lines')
    for cat, info in categories.items():
        n = sum(1 for p in projects if p['category'] == cat)
        print(f'  {cat:24} {n:3} projects (stated {info["stated_count"]}); five-year {info["grand_total"][8] if info["grand_total"] else None:,}')
    t = fund_check['city_totals']
    print(f"categories p.169: {sum(1 for v in fund_check['categories_p169'].values() if v.get('match'))} match "
          f"(+ Equipment & Fleet from the City table); funding sources p.170: "
          f"{sum(1 for v in fund_check['funding_sources_p170'].values() if v['match'])}/{len(fund_check['funding_sources_p170'])} match")
    print(f"City totals: by category {t['by_category_p169']:,}; by funding source {t['by_funding_source_p170_sum_of_group_totals']:,}; "
          f"difference {t['difference']:,} = {t['project_funding_absent_from_p170']}")
    for p in problems:
        print('PARSE', p)
    for e in errors:
        print('CHECK', e)
    if problems or errors:
        print('NOT WRITTEN: fix the problems above')
        return 1
    if '--write' in argv:
        write(projects, categories, by_fund, fund_check)
    return 0


def write(projects, categories, by_fund, fund_check):
    out = {
        'schema_version': 3,
        'extracted': '2026-10-23',
        'evidence_class': 'BUDGET_ADOPTED',
        'source': {
            'title': 'Adoption of Fiscal Years 2027 and 2028 Biennial Budget and Fiscal Years 2027-2031 Capital '
                     'Improvement Program, Exhibit B: FY2027-FY2031 Capital Improvement Program Overview',
            'body': 'City of Berkeley, City Council Special Meeting, June 23, 2026, Item 01 (adopted by resolution)',
            'local_copy': 'phase2/sources/budget-adoption-2026-06-23.pdf',
            'pages': 'Exhibit B project tables pp.179-229; funding-source tables pp.170, 172-173',
        },
        'adoption_status': (
            'The resolution adopts the Five-Year CIP "contained in the City Manager\'s Proposed" budget '
            '"and as amended by subsequent Council action on June 23, 2026" (packet p.6). Exhibit C '
            '(pp.249-255) amends FY2027-28 revenues and expenditures by fund; it changes capital grant '
            'revenue (funds 305-307, 336, 339) and Measure FF revenue (funds 164, 166) but prints no '
            'change to CIP project appropriations. Amendments made from the dais on June 23 are not in '
            'this packet; the FY2027 Annual Appropriation Ordinance is the controlling appropriation record '
            'and is not yet in BeTH\'s sources.'),
        'caveats': [
            'Amounts are budget appropriations and plans, not cash, not expenditures, not encumbrances.',
            'prior_years and fy2026_budget are appropriations already made. Unspent capital appropriations are '
            're-appropriated until a project completes (FY2025 ACFR, Required Supplementary Information budget '
            'note); how much of them is unspent or encumbered is not in this source.',
            'FY2029-FY2031 are "Planned", not appropriated.',
            'Equipment & Fleet is a vehicle replacement schedule of the Equipment Replacement internal service '
            'fund (pp.231-247), not project rows; it is summarized in excluded_categories, not itemized.',
        ],
        'project_count_stated_by_city': 149,
        'reconciliation': {
            'project_rows_sum_to_printed_project_totals': True,
            'categories_sum_to_printed_grand_totals': True,
            'category_project_counts_match_document': 'yes, except: ' + '; '.join(f'{k}: {v}' for k, v in DOCUMENT_COUNT_EXCEPTIONS.items()),
            'projects_extracted': len(projects),
            'city_summary_tables': fund_check,
            'printed_total_rounding_differences': ROUNDING,
        },
        'excluded_categories': [{
            'category': 'Equipment & Fleet', 'fund': '671 Equipment Replacement (internal service)',
            'by_year': dict(zip(YEARS5 + ['five_year'], city_tables()[0]['Equipment & Fleet'])),
            'source': 'p.169 category table, Equipment & Fleet row; vehicle schedule pp.231-247',
            'note': 'Fleet vehicles only. The p.170 Equipment Replacement row ($39,352,116) also includes the four Fleet EV '
                    'Charger projects ($6,021,000, fund 671) that are already in the Other Infrastructure project table; '
                    'counting both would double-count them.'}],
        'categories': {c: {'stated_count': v['stated_count'], 'printed_grand_total': dict(zip(COLS, v['grand_total']))}
                       for c, v in categories.items()},
        'projects': [{k: v for k, v in p.items() if k != 'printed_total'} for p in projects],
        'five_year_by_fund': dict(sorted(by_fund.items(), key=lambda kv: -kv[1])),
    }
    streets = {p['title']: sum(f['five_year_budget'] for f in p['funding']) for p in projects if p['category'] == 'Streets'}
    plan = sum(v for k, v in streets.items() if k.startswith('Street Rehab'))
    ff = sum(v for k, v in streets.items() if k.startswith('Measure FF'))
    other = {k: v for k, v in streets.items() if not k.startswith(('Street Rehab', 'Measure FF'))}
    out['reconciliation']['streets_139m'] = {
        'question': 'The $139.3 million figure is the adopted FIVE-YEAR (FY2027-FY2031) Streets CIP budget, not a two-year budget.',
        'identity': {
            'five_year_street_rehabilitation_plan': plan,
            'measure_ff_street_rehabilitation': ff,
            'other_streets_projects': other,
            'total': plan + ff + sum(other.values()),
            'printed_streets_five_year_budget': categories['Streets']['grand_total'][8],
        },
        'two_year_fy2027_fy2028': sum(f['fy2027'] + f['fy2028'] for p in projects if p['category'] == 'Streets' for f in p['funding']),
        'cross_check': ('The July 7, 2026 street plan (Tables 1A-1B) totals the Five-Year Street Rehabilitation Plan at '
                        '$96,336,212 and the Measure FF five-year street program at $42,119,935 (p.8, Table 4); its fiscal '
                        'impact section states the combined five-year street CIP "totals over $139 million".'),
    }
    out['reconciliation']['adoption_changes_outside_exhibit_b'] = [
        {'exhibit': 'C', 'pages': '253-255', 'item': 'Measure FF - Street Repair (fund 166) revenue',
         'fy2027': 1351651, 'fy2028': 1378684, 'kind': 'revenue',
         'note': 'FY2027 revenue revised from $15,300,000 to $16,651,651 (inflator 4.95% personal income growth). '
                 'No matching change to Measure FF CIP appropriations is printed.'},
        {'exhibit': 'C', 'pages': '253-255', 'item': 'Capital grant revenue (funds 305, 306, 307, 336, 339)', 'kind': 'revenue',
         'note': 'Grant revenue revised for named capital projects (Codornices Creek, Addison Bicycle Boulevard Phase 2, '
                 'Adeline, Washington Elementary/Berkeley High, Telegraph Multimodal, West Berkeley/Aquatic Park stormwater).'},
        {'exhibit': 'D', 'pages': '255-257', 'item': "Streets & Open Space Improvement Plan (SOSIP) - Mayor's recommendation",
         'fy2027': 2900000, 'kind': 'appropriation (one-time)',
         'note': 'Includes $2.5M Oxford for All design, engineering and construction and $150K Addison Street catenary '
                 'lighting. Exhibit B prints only $150,000 of SOSIP money (Harold Way Placemaking).'},
        {'exhibit': 'D', 'pages': '255-257', 'item': 'CAR-FREE Telegraph study - LRDP funding process', 'fy2027': 662500,
         'fy2028': 662500, 'kind': 'study (not capital construction)'},
    ]
    out['reconciliation']['to_proposed_presentation'] = (
        'Not reconciled row by row. The earlier extraction of the proposed-CIP presentation (cip-presentation.json) '
        'mixes summary labels, funding-source lines and fragments into its project list, so title matching produces '
        'false differences. Exhibit B is the proposed CIP that the June 23 resolution adopted; Exhibit C prints no '
        'change to CIP project appropriations. cip-presentation.json is kept only as a record of the earlier pass.')
    OUT.write_text(json.dumps(out, indent=1) + '\n')
    print(f'wrote {OUT.relative_to(ROOT.parent)}')


if __name__ == '__main__':
    sys.exit(main(sys.argv))

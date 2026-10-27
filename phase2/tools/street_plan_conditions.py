#!/usr/bin/env python3
"""Condition of the streets the City plans to treat, from the street lists attached to the July 7, 2026
Five-Year Street Rehabilitation and Measure FF Plans (Attachments, pp.21-62).

Why: the City's StreetSaver scenarios report only the NETWORK-AVERAGE PCI. An average of 62 can coexist with
many failed streets. BeTH keeps two performance measures side by side and never substitutes one for the other:
  1. network-average PCI (the City's scenarios, unchanged), and
  2. the distribution of conditions, including streets below PCI 50.
The network-wide distribution is NOT in any document BeTH holds. What the attachments do give, verifiably, is
the current PCI of every section each plan will treat. This tool extracts that and validates every fiscal year
against the section count, miles and cost the City prints in each table header.

Run:  python3 phase2/tools/street_plan_conditions.py [--write]   (writes phase2/data/street-plan-conditions.json)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources' / 'street-rehab-measure-ff-2026-07-07.txt'
OUT = ROOT / 'data' / 'street-plan-conditions.json'

HDR5 = re.compile(r'5-YEAR STREET REHABILITATION PLAN: FY 2027-2031 \| Fiscal Year (\d{4})')
HDRFF = re.compile(r'MEASURE FF PLAN: FY 2027-2031 \| Fiscal Year (\d{4})')
COUNTS = re.compile(r'(\d+) Sections \| \$([\d,]+) \|\s*([\d.]+) miles')
ROW = re.compile(r'(?<![\d.,$])(\d{1,3})\s+(\d+\.\d{2})(?![\d,])')
TOTAL5 = re.compile(r'^TOTAL\s+([\d.]+)\s+\$([\d,]+)')
# Condition bands used by the Metropolitan Transportation Commission's pavement management program.
BANDS = [(0, 24, 'failed (0-24)'), (25, 49, 'poor (25-49)'), (50, 59, 'at risk (50-59)'),
         (60, 69, 'fair (60-69)'), (70, 79, 'good (70-79)'), (80, 100, 'very good (80-100)')]


def band(pci):
    return next(lbl for lo, hi, lbl in BANDS if lo <= pci <= hi)


def parse():
    lines = SRC.read_text().split('\n')
    plans = {'five_year_plan': {}, 'measure_ff': {}}
    cur, page = None, None
    for i, line in enumerate(lines):
        m = re.search(r'Page (\d+) of 70', line)
        if m:
            page = int(m.group(1))
        h5, hf = HDR5.search(line), HDRFF.search(line)
        if h5 or hf:
            plan = 'five_year_plan' if h5 else 'measure_ff'
            fy = int((h5 or hf).group(1))
            nxt = ' '.join(lines[i:i + 3])
            c = COUNTS.search(nxt.replace('\n', ' '))
            cur = plans[plan].setdefault(fy, {'printed': None, 'sections': [], 'pages': set()})
            if c and cur['printed'] is None:
                cur['printed'] = {'sections': int(c.group(1)), 'cost': int(c.group(2).replace(',', '')),
                                  'miles': float(c.group(3))}
            continue
        if cur is None:
            continue
        t = TOTAL5.search(line.strip())
        if t:
            cur['printed_total_row'] = {'miles': float(t.group(1)), 'cost': int(t.group(2).replace(',', ''))}
            continue
        for r in ROW.finditer(line):
            pci, miles = int(r.group(1)), float(r.group(2))
            if pci <= 100 and miles < 5:
                cur['sections'].append({'pci': pci, 'miles': miles, 'source_line': i + 1, 'page': page})
                cur['pages'].add(page)
        if 'Page 63 of 70' in line:
            cur = None
    return plans


def summarize(plans):
    out, problems = {}, []
    for plan, years in plans.items():
        out[plan] = {'by_year': {}, 'all_years': None}
        allsec = []
        for fy, y in sorted(years.items()):
            secs = y['sections']
            allsec += secs
            miles = round(sum(s['miles'] for s in secs), 2)
            pr = y['printed'] or {}
            ok_n = pr.get('sections') == len(secs)
            # per-section lengths are printed to 2 decimals, so their sum can drift by up to 0.005 mi per section
            ok_m = abs(pr.get('miles', -1) - miles) <= 0.005 * len(secs) + 1e-9
            if not (ok_n and ok_m):
                problems.append(f'{plan} FY{fy}: parsed {len(secs)} sections / {miles} mi vs printed {pr}')
            out[plan]['by_year'][fy] = {'printed_header': pr, 'parsed_sections': len(secs), 'parsed_miles': miles,
                                        'validated': ok_n and ok_m,
                                        'miles_difference_vs_printed': round(miles - pr.get('miles', 0), 2), 'pages': f"{min(y['pages'])}-{max(y['pages'])}" if y['pages'] else None,
                                        **dist(secs)}
        out[plan]['all_years'] = dist(allsec)
    both = [s for p in plans.values() for y in p.values() for s in y['sections']]
    out['both_plans_fy2027_2031'] = dist(both)
    return out, problems


def dist(secs):
    miles = sum(s['miles'] for s in secs)
    bands = {}
    for _, _, lbl in BANDS:
        sm = [s for s in secs if band(s['pci']) == lbl]
        bands[lbl] = {'sections': len(sm), 'miles': round(sum(s['miles'] for s in sm), 2)}
    below50 = [s for s in secs if s['pci'] < 50]
    return {'sections': len(secs), 'centerline_miles': round(miles, 2),
            'miles_below_pci_50': round(sum(s['miles'] for s in below50), 2),
            'share_of_planned_miles_below_50': round(sum(s['miles'] for s in below50) / miles, 4) if miles else None,
            'length_weighted_mean_current_pci': round(sum(s['pci'] * s['miles'] for s in secs) / miles, 1) if miles else None,
            'by_condition_band': bands}


def main(argv):
    plans = parse()
    summary, problems = summarize(plans)
    for plan in ('five_year_plan', 'measure_ff'):
        a = summary[plan]['all_years']
        print(f"{plan}: {a['sections']} sections, {a['centerline_miles']} mi, below 50: {a['miles_below_pci_50']} mi "
              f"({a['share_of_planned_miles_below_50']:.0%}), mean current PCI {a['length_weighted_mean_current_pci']}")
        for fy, y in summary[plan]['by_year'].items():
            print(f"   FY{fy}: {y['parsed_sections']} sec {y['parsed_miles']} mi | printed {y['printed_header']} | ok={y['validated']} | <50: {y['miles_below_pci_50']} mi")
    b = summary['both_plans_fy2027_2031']
    print(f"both: {b['centerline_miles']} mi planned, {b['miles_below_pci_50']} mi below 50")
    for p in problems:
        print('CHECK', p)
    if problems:
        print('NOT WRITTEN')
        return 1
    if '--write' in argv:
        OUT.write_text(json.dumps({
            'schema_version': 1, 'generated': '2026-10-23', 'evidence_class': 'CITY_PLAN',
            'source': {'title': 'Five-Year Street Rehabilitation and Measure FF Plans for Fiscal Years 2027-2031, Council '
                                'Action Calendar, July 7, 2026, Attachments (street lists)',
                       'local': 'phase2/sources/street-rehab-measure-ff-2026-07-07.pdf'},
            'what_this_is': 'Current PCI (as printed in the plan) of every section the City plans to treat FY2027-FY2031, '
                            'validated per fiscal year against the printed section count and miles.',
            'what_this_is_not': 'Not the condition of the whole network. Streets not in either plan are not here. PCI is the '
                                'value printed at planning time; streets will be lower when treated.',
            'condition_bands': 'Metropolitan Transportation Commission pavement categories: failed 0-24, poor 25-49, at risk '
                               '50-59, fair 60-69, good 70-79, very good 80-100.',
            'network_context': {'centerline_miles': 213, 'lane_miles': 450,
                                'sources': 'street plan p.16 (213 centerline miles, PCI 57); adoption packet p.243 (450 lane miles)'},
            'plans': summary}, indent=1) + '\n')
        print('wrote', OUT.relative_to(ROOT.parent))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

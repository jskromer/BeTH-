#!/usr/bin/env python3
"""Network-wide pavement condition distribution from the City's own segment inventory.

Source: "City of Berkeley 2024 PMP Update, P-TAP Round 25, Final Report", Pavement Engineering Inc., April 2025
(phase2/sources/pavement-management-update-ptap25-2025-04.pdf), Section IV Reference Reports, "Street Sections
Alphabetical": one row per street section with centerline miles, lane miles, area and last calculated PCI
(inspections of 2024; report dated 02/14/2025).

Every total is validated against the report's own Executive Summary: totals table on Executive Summary p.2
(PDF p.5): 212.77 centerline miles, 446.10 lane miles, 39,363,218 sq ft, average PCI 56 (area-weighted); and the
Condition Category Breakdown by area on Executive Summary p.4 (PDF p.7).

Mileage: each section prints its length in feet and its miles rounded to 2 decimals. Summing the rounded miles
overstates the network (213.48 mi) because most sections are short and round up; summing feet / 5,280 gives
212.78 mi, within 0.01 mi of the printed 212.77. All mileage below is computed from feet and reported to 0.1 mi.
Nothing is written if a check fails.

The City's projections (July 7, 2026 plan) report only the network AVERAGE. This file supplies the second
measure BeTH keeps beside it: how much of the network is below PCI 50, and how far below.

Run:  python3 phase2/tools/network_condition.py [--write]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources' / 'pavement-management-update-ptap25-2025-04.txt'
OUT = ROOT / 'data' / 'network-condition.json'

ROW = re.compile(r'\s(\d+)\s+(\d+)\s+(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+)\s+(\d{1,3})\s+(\d{2}/\d{2}/\d{4})\s+'
                 r'(Excellent|Good|Fair|Poor|Failed)\b')
FC = re.compile(r'\s([RCA])\s+([A-Z])\s+(\d)\s+\d+\s+\d+\s+\d+\.\d{2}')
PRINTED = {'centerline_miles': 212.77, 'lane_miles': 446.10, 'area_sqft': 39363218, 'average_pci': 56,
           'by_functional_class': {'A': {'centerline_miles': 21.87, 'area_sqft': 5866756, 'average_pci': 57},
                                   'C': {'centerline_miles': 36.70, 'area_sqft': 7200161, 'average_pci': 64},
                                   'R': {'centerline_miles': 154.20, 'area_sqft': 26296301, 'average_pci': 53}},
           'condition_by_area': {'Excellent': 4182818, 'Good': 9078245, 'Fair': 9597800, 'Poor': 7215563,
                                 'Failed': 9292667}}
# One section, TEVLIN ST 040 (Gilman St to end south of Gilman, 155 ft x 25 ft = 3,875 sq ft), prints PCI 0 with no
# inspection date. The report counts it in the Failed category area (p.4) but not in the totals table (p.2) or the
# functional-class areas. The category areas therefore sum to 3,875 sq ft more than the printed total. That is
# a difference in coverage between two tables, not an arithmetic error.
UNINSPECTED = re.compile(r'\s(\d+)\s+(\d+)\s+(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+)\s+(\d{1,3})\s{6,}(Failed|Poor|Fair|Good|Excellent)\b')
CATEGORY_TABLE_EXTRA = sum(PRINTED['condition_by_area'].values()) - PRINTED['area_sqft']
FT_PER_MILE = 5280
PTAP_BANDS = {'Excellent': (91, 100), 'Good': (71, 90), 'Fair': (51, 70), 'Poor': (31, 50), 'Failed': (0, 30)}
MTC_BANDS = [(0, 24, 'failed (0-24)'), (25, 49, 'poor (25-49)'), (50, 59, 'at risk (50-59)'),
             (60, 69, 'fair (60-69)'), (70, 79, 'good (70-79)'), (80, 100, 'very good (80-100)')]


def parse():
    lines = SRC.read_text().split('\n')
    start = next(i for i, l in enumerate(lines) if 'Reference Reports: Street Sections Alphabetical' in l)
    end = next(i for i, l in enumerate(lines) if 'Street Sections by PCI (High to Low)' in l)
    rows, uninspected = [], []
    for i in range(start, end):
        m = ROW.search(lines[i])
        if not m:
            u = UNINSPECTED.search(lines[i])
            if u:
                uninspected.append({'line': i + 1, 'text': ' '.join(lines[i].split()[2:8]), 'length_ft': int(u.group(1)),
                                    'width_ft': int(u.group(2)), 'area_sqft': int(u.group(5)), 'pci_printed': int(u.group(6)),
                                    'pci_date': None, 'ptap_category': u.group(7)})
            continue
        f = FC.search(lines[i])
        rows.append({'line': i + 1, 'functional_class': f.group(1) if f else None,
                     'length_ft': int(m.group(1)), 'width_ft': int(m.group(2)),
                     'centerline_miles': float(m.group(3)), 'lane_miles': float(m.group(4)),
                     'area_sqft': int(m.group(5)), 'pci': int(m.group(6)), 'pci_date': m.group(7),
                     'ptap_category': m.group(8)})
    return rows, uninspected


def checks(rows, uninspected):
    errs = []
    if [u['area_sqft'] for u in uninspected] != [CATEGORY_TABLE_EXTRA]:
        errs.append(f'uninspected sections {uninspected} do not explain the {CATEGORY_TABLE_EXTRA} sq ft category-table extra')
    ft = sum(r['length_ft'] for r in rows)
    cl_ft = ft / FT_PER_MILE
    if abs(cl_ft - PRINTED['centerline_miles']) > 0.01:
        errs.append(f'centerline miles from feet {cl_ft:.3f} vs printed {PRINTED["centerline_miles"]}')
    cl = round(sum(r['centerline_miles'] for r in rows), 2)
    ln = round(sum(r['lane_miles'] for r in rows), 2)
    area = sum(r['area_sqft'] for r in rows)
    avg = sum(r['pci'] * r['area_sqft'] for r in rows) / area
    # section miles print to 2 decimals: allow 0.005 per section of rounding drift
    tol = 0.005 * len(rows)
    if abs(cl - PRINTED['centerline_miles']) > tol:
        errs.append(f'centerline miles {cl} vs printed {PRINTED["centerline_miles"]}')
    if abs(ln - PRINTED['lane_miles']) > tol:
        errs.append(f'lane miles {ln} vs printed {PRINTED["lane_miles"]}')
    if area != PRINTED['area_sqft']:
        errs.append(f'area {area} vs printed {PRINTED["area_sqft"]}')
    if round(avg) != PRINTED['average_pci']:
        errs.append(f'area-weighted PCI {avg:.2f} vs printed {PRINTED["average_pci"]}')
    for cat, sq in PRINTED['condition_by_area'].items():
        got = sum(r['area_sqft'] for r in rows if r['ptap_category'] == cat)
        extra = sum(u['area_sqft'] for u in uninspected if u['ptap_category'] == cat)
        if got + extra != sq:
            errs.append(f'{cat} area {got} vs printed {sq}')
        lo, hi = PTAP_BANDS[cat]
        bad = [r for r in rows if r['ptap_category'] == cat and not lo <= r['pci'] <= hi]
        if bad:
            errs.append(f'{cat}: {len(bad)} rows with PCI outside {lo}-{hi}')
    for fc, p in PRINTED['by_functional_class'].items():
        rs = [r for r in rows if r['functional_class'] == fc]
        a = sum(r['area_sqft'] for r in rs)
        if a != p['area_sqft']:
            errs.append(f'class {fc} area {a} vs printed {p["area_sqft"]}')
    return errs, {'sections': len(rows), 'centerline_miles_from_feet': round(cl_ft, 3),
                  'centerline_miles_sum_of_rounded_section_miles': cl, 'lane_miles': ln, 'area_sqft': area,
                  'area_weighted_pci': round(avg, 2),
                  'centerline_weighted_pci': round(sum(r['pci'] * r['centerline_miles'] for r in rows) / cl, 2)}


def distribution(rows):
    cl = sum(r['length_ft'] for r in rows)
    area = sum(r['area_sqft'] for r in rows)

    def share(sel):
        c = sum(r['length_ft'] for r in sel)
        a = sum(r['area_sqft'] for r in sel)
        return {'sections': len(sel), 'centerline_miles': round(c / FT_PER_MILE, 1),
                'centerline_miles_unrounded': round(c / FT_PER_MILE, 3),
                'centerline_miles_sum_of_rounded_section_miles': round(sum(r['centerline_miles'] for r in sel), 2),
                'share_of_centerline_miles': round(c / cl, 4),
                'area_sqft': a, 'share_of_area': round(a / area, 4)}
    return {
        'below_pci_50': share([r for r in rows if r['pci'] < 50]),
        'below_pci_25': share([r for r in rows if r['pci'] < 25]),
        'pci_50_or_above': share([r for r in rows if r['pci'] >= 50]),
        'by_mtc_band': {lbl: share([r for r in rows if lo <= r['pci'] <= hi]) for lo, hi, lbl in MTC_BANDS},
        'by_ptap_category': {c: share([r for r in rows if r['ptap_category'] == c]) for c in PTAP_BANDS},
        'by_functional_class_below_50': {fc: share([r for r in rows if r['functional_class'] == fc and r['pci'] < 50])
                                         for fc in ('A', 'C', 'R')},
    }


def main(argv):
    rows, uninspected = parse()
    errs, totals = checks(rows, uninspected)
    print('totals', totals)
    d = distribution(rows)
    for k in ('below_pci_50', 'below_pci_25'):
        print(k, d[k])
    for e in errs:
        print('CHECK', e)
    if errs:
        print('NOT WRITTEN')
        return 1
    if '--write' in argv:
        OUT.write_text(json.dumps({
            'schema_version': 1, 'generated': '2026-10-23', 'evidence_class': 'CITY_ASSESSMENT',
            'source': {'title': 'City of Berkeley 2024 Pavement Management Program Update (P-TAP Round 25), Final Report, '
                                'Pavement Engineering Inc., April 2025',
                       'url': 'https://berkeleyca.gov/sites/default/files/2026-07/2024%20Pavement%20Management%20Plan%20Update%20%28PTAP25%29.pdf',
                       'local': 'phase2/sources/pavement-management-update-ptap25-2025-04.pdf',
                       'sha256': '5e431b32fca3e2dcd96bb3698e19f14df6be734a9256bfdeb38d62472269e420',
                       'pages': 'Executive Summary p.2 / PDF p.5 (average PCI 56, totals by functional class); Executive '
                                'Summary p.4 / PDF p.7 (Condition Category Breakdown); Section IV Reference Reports '
                                '(street sections alphabetical)',
                       'pdf_pages': {'totals': 5, 'condition_breakdown': 7}},
            'as_of': 'Inspections in 2024 (report dated 02/14/2025). Before FY2025-FY2026 paving. The July 7, 2026 plan '
                     'cites PCI 57 (2025) and 59 after FY2026 planned work; no newer segment list is public.',
            'validation': {'parsed': totals, 'printed': PRINTED, 'result': 'all checks passed',
                           'mileage_method': 'Section lengths in feet / 5,280 = '
                                             f'{totals["centerline_miles_from_feet"]} mi, against the printed 212.77. The sum of '
                                             f'the rounded section miles is {totals["centerline_miles_sum_of_rounded_section_miles"]} '
                                             'mi: 1,216 short sections each rounded to 0.01 mi accumulate about 0.7 mi of rounding. '
                                             'BeTH uses feet and reports miles to 0.1 mi.',
                           'uninspected_section': {
                               'sections': uninspected,
                               'explanation': f'The Condition Category areas (p.4) sum to {sum(PRINTED["condition_by_area"].values()):,} '
                                              f'sq ft, {CATEGORY_TABLE_EXTRA:,} more than the totals table (p.2, {PRINTED["area_sqft"]:,}). '
                                              'The difference is exactly this one section, which prints PCI 0 with no inspection '
                                              'date: the category table counts it as Failed, the totals table leaves it out. BeTH '
                                              'follows the totals table and excludes it from every distribution below.'}},
            'distribution': d,
            'notes': ['PTAP categories (as printed by the City\'s consultant): Excellent 91-100, Good 71-90, Fair 51-70, '
                      'Poor 31-50, Failed 0-30.',
                      'MTC bands (regional standard): very good 80-100, good 70-79, fair 60-69, at risk 50-59, poor 25-49, '
                      'failed 0-24.',
                      'Measure FF\'s goal is PCI 70 "ideally with no streets having a PCI below 50" (BMC 7.11.010(K)(1)); '
                      'the below-50 measure here matches that wording.']}, indent=1) + '\n')
        print('wrote', OUT.relative_to(ROOT.parent))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

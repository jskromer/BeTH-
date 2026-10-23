#!/usr/bin/env python3
"""Assemble the Phase 2 Budget Choices dashboard data file from sourced inputs.

Joins: CIP project rows, the funding-restriction crosswalk, the PCI model state, and
Marina/Workers' Compensation figures from BeTH's Phase 1 audited ledger.

Every output figure carries an evidence class. Nothing is computed across classes.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
OUT = ROOT / 'docs' / 'data' / 'phase2.json'


def load(p):
    return json.loads(Path(p).read_text())


def fund(fid):
    return load(REPO / 'data' / 'funds' / f'{fid}.json')


def main():
    cip = load(ROOT / 'data' / 'cip-projects.json')
    restr = load(ROOT / 'data' / 'funding-restrictions.json')
    pci = load(ROOT / 'data' / 'pci-model.json')
    rmap = {m['cip_label']: m for m in restr['mappings']}

    # Join each adopted funding line to its restriction class through the City fund number.
    FUND_TO_LABEL = {'166': 'Measure FF', '501': 'CIP Fund', '611': 'Sanitary Sewer Fund', '616': 'Stormwater',
                     '138': 'Parks Tax', '127': 'State Transportation Tax', '134': 'Measure BB Local Streets & Roads',
                     '601': 'Zero Waste', '133': 'Measure F-AC VRF', '608': 'Marina Fund', '671': 'Equipment Replacement',
                     '125': 'Camps Fund', '142': 'Street Lighting', '149': 'Private Sidewalks', '145': 'Bayer Aquatic Park Fund'}
    GRANTS = {'305', '306', '307', '336', '339', '340'}
    projects = []
    for p in cip['projects']:
        lines = []
        for f in p['funding']:
            m = rmap.get(FUND_TO_LABEL.get(f['fund']))
            if f['fund'] == 'UNFUNDED':
                rc, ev, red, conf = 'unfunded_need', 'Printed as "Unfunded Need": no money is identified.', False, 'High'
            elif f['fund'] == 'NOT_PRINTED':
                rc, ev, red, conf = 'unknown', 'The document prints no funding source on this row.', False, 'Low'
            elif f['fund'] in GRANTS and not m:
                rc, ev, red, conf = 'grant_condition', 'Capital grant fund; grant agreements not reviewed.', False, 'Moderate'
            elif m:
                rc, ev, red, conf = m['restriction_class'], m['evidence'], m['redirectable'], m['confidence']
            else:
                rc, ev, red, conf = 'unknown', 'Not yet researched.', False, 'Low'
            lines.append({'fund': f['fund'], 'fund_label': f['fund_label'], 'fy2027': f['fy2027'], 'fy2028': f['fy2028'],
                          'prior_years': f['prior_years'], 'fy2026_budget': f['fy2026_budget'],
                          'planned_fy2029_2031': f['fy2029'] + f['fy2030'] + f['fy2031'],
                          'restriction_class': rc, 'restriction_evidence': ev, 'redirectable': red, 'confidence': conf})
        projects.append({
            'name': p['title'], 'project_number': p['project_number'], 'new_or_continuing': p['new_or_continuing'],
            'category': p['category'], 'funding': lines,
            'two_year_adopted': sum(l['fy2027'] + l['fy2028'] for l in lines if l['restriction_class'] != 'unfunded_need'),
            'two_year_unfunded': sum(l['fy2027'] + l['fy2028'] for l in lines if l['restriction_class'] == 'unfunded_need'),
            # Fields the adopted CIP does not contain. Explicitly null, never zero.
            'expenditures_to_date': None, 'encumbrances': None, 'can_defer': None, 'annual_operating_cost': None,
            'missing': ['expenditures_to_date', 'encumbrances', 'can_defer', 'annual_operating_cost'],
            'source_line': p['source_line'],
        })

    # Restriction roll-up: FY2027+FY2028 adopted amounts by class, by funding line. Budget class only.
    byclass = {}
    for p in projects:
        for l in p['funding']:
            e = byclass.setdefault(l['restriction_class'], {'class': l['restriction_class'], 'funding_lines': 0, 'two_year': 0})
            e['funding_lines'] += 1
            e['two_year'] += l['fy2027'] + l['fy2028']

    marina, wc, gf, parks = fund('608'), fund('ACFR-workers-compensation'), fund('011'), fund('ACFR-park-tax')

    def yr(d, y):
        return next((r for r in d['annual'] if r['fy'] == y), {})

    doc = {
        'generated': '2026-10-23',
        'phase': 2,
        'status': 'PROTOTYPE — not published, not verified for publication',
        'evidence_classes': {
            'AUDITED': 'In an ACFR, tied to a statement column',
            'BUDGET_PROPOSED': 'Proposed budget figure; not an appropriation',
            'BUDGET_ADOPTED': 'Adopted appropriation',
            'PROJECTION': 'City forecast for an unaudited year',
            'CITY_MODEL': "Output of the City's own published model",
            'BETH_DERIVED': "BeTH arithmetic on published figures; labelled wherever shown",
            'THIRD_PARTY': 'Independent analysis, attributed',
        },
        'capital': {
            'evidence_class': 'BUDGET_ADOPTED',
            'source': cip['source'],
            'adoption_status': cip['adoption_status'],
            'caveats': cip['caveats'],
            'project_count_stated_by_city': cip['project_count_stated_by_city'],
            'projects_extracted': len(projects),
            'reconciliation': cip['reconciliation'],
            'projects': projects,
            'by_restriction_class': sorted(byclass.values(), key=lambda e: -e['two_year']),
        },
        'street_funding': load(ROOT / 'data' / 'street-funding-sources.json'),
        'restrictions': {
            'evidence_class': 'AUDITED/RESEARCH',
            'method': restr['method'],
            'classes': restr['classes'],
            'mappings': restr['mappings'],
            'summary': restr['summary'],
        },
        'pci': {
            'evidence_class': 'CITY_MODEL',
            'status': pci['status'],
            'headline': pci['headline'],
            'assessment': pci['performance_assessment'],
            'network_condition': load(ROOT / 'data' / 'network-condition.json'),
            'plan_conditions': load(ROOT / 'data' / 'street-plan-conditions.json'),
            'scenarios': pci['city_scenarios'],
            'selection_methods': pci['city_selection_methods'],
            'marginal': pci['marginal_cost_per_pci_point'],
            'current_pci': pci['inputs']['network']['current_network_pci'],
            'after_fy2026': pci['inputs']['network']['pci_after_fy2026_work'],
            'adopted_goal': pci['inputs']['network']['adopted_goal'],
            'independent_model': pci['independent_model_status'],
        },
        'marina': {
            'evidence_class': 'AUDITED + PROJECTION',
            'audited': [
                {'fy': y['fy'], 'revenue': y.get('revenue'), 'expenditure': y.get('expenditure'),
                 'ending_balance': y.get('ending_balance'), 'basis': y['basis']}
                for y in marina['annual'] if y['fy'] >= 2023
            ],
            'fy2025_outflows': (marina.get('flow_detail') or {}).get('outflows', []),
            'obligations': marina.get('obligations', []),
            'note': 'FY2026-FY2028 rows are PROJECTIONS from the Parks, Recreation & Waterfront '
                    'Commission packet of 2026-09-09, not actuals. No FY2026 ACFR exists.',
        },
        'operating_consequences': {
            'evidence_class': 'AUDITED',
            'workers_compensation': {
                'name': wc['name'],
                'fy2024': yr(wc, 2024), 'fy2025': yr(wc, 2025),
                'finding': "FY2025: $0 operating revenue after two contribution holidays, "
                           '$11,983,900 of expense, ending net position -$9,752,938. A further '
                           '$5,187,019 is budgeted out to the General Fund in FY2026.',
                'why_it_matters': 'The clearest case in Berkeley of a one-time budget fix creating a '
                                  'recurring liability. Any proposal to redirect internal-service '
                                  'balances to capital or streets should be read against this.',
                'open': 'The $5,500,000 Workers\' Compensation transaction is under independent '
                        'investigation by Codex and is NOT resolved. Nothing here assumes an outcome.',
            },
            'general_fund': {
                'fy2025': yr(gf, 2025),
                'structural_deficit_obligation': next(
                    (o for o in gf.get('obligations', []) if o['kind'] == 'structural_deficit'), None),
            },
            'park_tax': {
                'fy2025': yr(parks, 2025),
                'unfunded_capital': next(
                    (o for o in parks.get('obligations', []) if o['kind'] == 'unfunded_capital'), None),
            },
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1) + '\n')
    size = OUT.stat().st_size
    print(f'wrote {OUT.relative_to(Path.cwd())} ({size:,} bytes)')
    print(f"  capital projects: {len(projects)}")
    print(f"  restriction classes: {len(byclass)}")
    for e in doc['capital']['by_restriction_class']:
        print(f"    {e['class']:24s} {e['funding_lines']:>3} lines  ${e['two_year']:>12,}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

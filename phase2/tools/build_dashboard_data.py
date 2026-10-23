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

    # Join each project row to its restriction class, by printed funding source.
    projects = []
    for p in cip['projects']:
        label = p.get('funding_source_as_printed')
        m = rmap.get(label) if label else None
        fy27, fy28 = p['fy2027_proposed'], p['fy2028_proposed']
        projects.append({
            'name': p['label'],
            'department': p['department'],
            'category': p['category'],
            'funding_source': label,
            'fy2027': fy27,
            'fy2028': fy28,
            'two_year_total': (fy27 or 0) + (fy28 or 0) if (fy27 or fy28) else None,
            'restriction_class': m['restriction_class'] if m else 'unknown',
            'restriction_evidence': m['evidence'] if m else
                'No funding source printed for this row in the source document.',
            'redirectable': m['redirectable'] if m else False,
            'confidence': m['confidence'] if m else 'Low',
            # Fields the source does not contain. Explicitly null, never zero.
            'expenditures_to_date': None,
            'encumbrances': None,
            'remaining_authorization': None,
            'status': None,
            'schedule': None,
            'can_defer': None,
            'annual_operating_cost': None,
            'missing': ['expenditures_to_date', 'encumbrances', 'remaining_authorization',
                        'status', 'schedule', 'can_defer', 'annual_operating_cost'],
            'source_line': p['source_line'],
        })

    # Restriction roll-up: two-year proposed totals by class. Budget class only.
    byclass = {}
    for p in projects:
        c = p['restriction_class']
        e = byclass.setdefault(c, {'class': c, 'projects': 0, 'two_year_proposed': 0})
        e['projects'] += 1
        e['two_year_proposed'] += p['two_year_total'] or 0

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
            'evidence_class': 'BUDGET_PROPOSED',
            'source': cip['source'],
            'caveats': cip['caveats'],
            'project_count_stated_by_city': cip['project_count_stated_by_city'],
            'project_rows_extracted': len(projects),
            'projects': projects,
            'by_restriction_class': sorted(byclass.values(), key=lambda e: -e['two_year_proposed']),
        },
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
            'assessment': pci['pci60_assessment'],
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
        print(f"    {e['class']:20s} {e['projects']:>3} projects  ${e['two_year_proposed']:>12,}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

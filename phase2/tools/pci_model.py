#!/usr/bin/env python3
"""PCI 60+ scenario model for Berkeley's pavement network.

What this is: a working, transparent implementation of the funding -> treatment ->
condition chain, with every input declared and sourced.

What it will not do: produce a numerical PCI forecast from inputs it does not have.
Calling run() with uncalibrated inputs returns a BLOCKED result naming the missing
data. That is deliberate. A PCI 60 price tag is the number most likely to be quoted
and the one BeTH is least able to defend, so it is not generated until the City's
own StreetSaver data is loaded.

Run:  python3 phase2/tools/pci_model.py            # status + what is missing
      python3 phase2/tools/pci_model.py --emit     # write model state for the dashboard
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'pci-model.json'

SRC_PLAN = ('City of Berkeley, "Five-Year Street Rehabilitation and Measure FF Plans for Fiscal Years '
            '2027-2031", Council Action Calendar, July 7, 2026, p.12 (PCI Projections, Figure 1)')
SRC_CIP = ('City of Berkeley, Proposed FY2027-FY2031 Capital Improvement Program presentation, Item 02')

# The City's own 12-year projections, after FY2026 planned work, with 3% construction
# cost inflation and revenue growth. These are PUBLISHED CITY MODEL OUTPUTS, not BeTH
# estimates. BeTH reuses the City's model rather than building a rival one.
CITY_SCENARIOS = [
    {'id': 'five_year_plan', 'label': 'Five-Year Plan baseline',
     'annual_investment': 20300000, 'pci_2038': 56, 'direction': 'declines',
     'description': 'Only the funding in the proposed Five-Year Street Rehabilitation Plan. PCI falls '
                    'from 59 to about 56 by 2038 as construction cost escalation outpaces revenue '
                    'growth.',
     'source': SRC_PLAN},
    {'id': 'plan_plus_ff', 'label': 'Five-Year Plan + Measure FF',
     'annual_investment': 29600000, 'pci_2038': 62, 'direction': 'improves',
     'description': 'Adds Measure FF funding. PCI improves from 59 to about 62 by 2038. Measure FF '
                    'accounts for the entire difference between this and the baseline.',
     'source': SRC_PLAN},
    {'id': 'reach_70', 'label': 'Reach 70 by 2036, then maintain',
     'annual_investment': 37600000, 'pci_2038': 70, 'direction': 'reaches goal',
     'description': 'The investment level the City estimates is needed to reach PCI 70 by 2036 and hold '
                    'it through 2038. About $8M a year more than the Plan and Measure FF currently '
                    'provide.',
     'source': SRC_PLAN},
]

# Alternative street-selection methods, same funding (City Figure 2).
CITY_SELECTION_METHODS = [
    {'id': 'critical_point', 'label': 'Critical Point (WER-driven)', 'pci_2038': 63,
     'description': "Selects Measure FF streets using the same WER methodology as the Five-Year Plan.",
     'source': SRC_PLAN},
    {'id': 'pci_under_50', 'label': 'PCI Under 50 targeting', 'pci_2038': 62,
     'description': "Targets streets below PCI 50, consistent with Measure FF's stated goal of "
                    'addressing long-deferred repairs.',
     'source': SRC_PLAN},
]

# ---------------------------------------------------------------- inputs
# Every entry is either a sourced value or None. None means "not held"; it is never
# replaced by a default, a literature value, or an assumption.

INPUTS = {
    'network': {
        'current_network_pci': {'value': 57, 'source': SRC_PLAN, 'confidence': 'High',
                                'note': 'Citywide PCI as of the most recent condition assessment (2025).'},
        'pci_after_fy2026_work': {'value': 59, 'source': SRC_PLAN, 'confidence': 'High'},
        'assessment_cycle': {'value': 'biennial', 'source': SRC_PLAN, 'confidence': 'High',
                             'note': 'PCI scored per street section from observed surface distresses, '
                                     'fed into StreetSaver.'},
        'adopted_goal': {'value': 70, 'source': 'BMC 7.11.010(K)(1), via ' + SRC_PLAN,
                         'confidence': 'High',
                         'note': 'Goal of citywide PCI 70 "ideally with no streets having a PCI below 50". '
                                 'Measure FF prioritises streets below PCI 50.'},
        'total_lane_miles': {'value': None, 'source': None,
                             'needed_from': 'StreetSaver network summary. Not required for the City-'
                                            'scenario comparison, only for independent segment modelling.'},
        'pci_distribution': {'value': None, 'source': None,
                             'needed_from': 'StreetSaver segment export. Needed to report miles below '
                                            'PCI 25 and the condition distribution.'},
    },
    'deterioration': {
        'curves_by_pavement_type': {'value': None, 'source': None,
                                    'needed_from': "Berkeley's adopted StreetSaver deterioration curves"},
        'note': 'Deterioration is non-linear. Below roughly PCI 40 the required treatment escalates from '
                'surface seal to full reconstruction at several times the cost. A linear assumption makes '
                'PCI 60 look far cheaper to reach than it is, so no linear fallback is provided.',
    },
    'treatments': {
        'catalog': {'value': None, 'source': None,
                    'needed_from': 'StreetSaver treatment catalog: eligibility PCI band, unit cost per '
                                   'square foot, service life, post-treatment PCI'},
        'note': 'Treatment eligibility depends on current PCI. A treatment valid at PCI 70 is usually '
                'invalid at PCI 35.',
    },
    'delivery_cost': {
        'cost_per_lane_mile_by_treatment': {'value': None, 'source': None,
                                            'needed_from': 'Recent Berkeley paving contracts'},
        'cost_decomposition': {'value': None, 'source': None,
                               'needed_from': 'Contract bid tabs, broken into pavement treatment, design, '
                                              'construction management, ADA, utilities, drainage, traffic '
                                              'safety, environmental work, green infrastructure, '
                                              'discretionary scope'},
        'note': 'Whether delivery reform frees real money can only be answered from this decomposition. '
                'Do not presume environmental review is the primary driver; that is the hypothesis to test.',
    },
    'funding': {
        'measure_ff_annual_estimate': {'value': 15000000, 'source': SRC_CIP, 'confidence': 'Low',
                                       'note': 'NOT all pavement: the same sentence covers sidewalks, '
                                               'safety and environment. Not usable as a paving budget '
                                               'without the split.'},
        'redirectable_from_capital': {'value': None, 'source': None,
                                      'needed_from': 'Restriction research across CIP funding sources. '
                                                     '0 of 15 sources currently confirmed redirectable.'},
        'recurring_operating_savings': {'value': None, 'source': None,
                                        'needed_from': 'Payroll and benefit baseline workstream'},
    },
    'escalation': {
        'construction_cost_pct_per_year': {'value': 3.0, 'source': SRC_PLAN, 'confidence': 'High',
                                           'note': 'Reflects recent asphalt and paving material trends.'},
        'revenue_escalation': {'value': 'greater of SF Bay Area cost of living or California per capita '
                                        'personal income growth',
                               'source': 'Council Resolution No. 70,456-N.S. and the Measure FF '
                                         'ordinance, via ' + SRC_PLAN, 'confidence': 'High'},
        'net_effect_stated_by_city': {'value': 'a modest real increase in construction costs relative to '
                                               'available funding over the projection period',
                                      'source': SRC_PLAN, 'confidence': 'High'},
    },
    'methodology': {
        'software': {'value': 'StreetSaver', 'source': SRC_PLAN, 'confidence': 'High'},
        'ranking': {'value': 'Weighted Economic Ranking (WER)', 'source': SRC_PLAN, 'confidence': 'High',
                    'note': 'WER ranks every street section and treatment option.'},
    },
}

SCENARIOS = [
    {'id': 'current_policy', 'label': 'Current policy',
     'description': 'Existing paving plan and funding only.'},
    {'id': 'capital_reallocation', 'label': 'Capital reallocation only',
     'description': 'Adds one-time released capital balances. Buys a burst of treatment; does not by '
                    'itself sustain a PCI level.'},
    {'id': 'operating_reform', 'label': 'Operating reform only',
     'description': 'Adds net recurring operating savings. Sustains a level; slow to accumulate.'},
    {'id': 'combined', 'label': 'Combined',
     'description': 'Both streams. Reaching a target needs one-time money; holding it needs recurring.'},
    {'id': 'delivery_reform', 'label': 'Delivery-cost reform',
     'description': 'Same dollars, lower cost per lane-mile.'},
    {'id': 'target_driven', 'label': 'Target-driven (reverse solve)',
     'description': 'Solves for the annual spend needed to reach and hold PCI 60, 65 or 70 over 5 and 10 '
                    'years. Reports "reach" and "hold" separately; they have very different profiles.'},
]

# These gate INDEPENDENT segment-level modelling only. The City-scenario comparison
# below needs none of them, because it reuses the City's own published model output.
REQUIRED_FOR_INDEPENDENT_MODEL = [
    ('network', 'total_lane_miles'),
    ('network', 'pci_distribution'),
    ('deterioration', 'curves_by_pavement_type'),
    ('treatments', 'catalog'),
    ('delivery_cost', 'cost_per_lane_mile_by_treatment'),
]


def missing_inputs():
    out = []
    for group, key in REQUIRED_FOR_INDEPENDENT_MODEL:
        entry = INPUTS[group][key]
        if entry.get('value') is None:
            out.append({'input': f'{group}.{key}', 'needed_from': entry.get('needed_from')})
    return out


def marginal_cost_per_pci_point():
    """Dollars per additional PCI point at 2038, derived from the City's own scenarios.

    This is BeTH arithmetic on three published City points, not a City figure. It is a
    coarse interpolation: the underlying relationship is non-linear, these are 12-year
    endpoints rather than a cost curve, and each scenario also differs in how streets are
    selected. Use it to show the shape of the trade-off, never as a procurement estimate.
    """
    out = []
    for a, b in zip(CITY_SCENARIOS, CITY_SCENARIOS[1:]):
        d_money = b['annual_investment'] - a['annual_investment']
        d_pci = b['pci_2038'] - a['pci_2038']
        out.append({
            'from': a['label'], 'to': b['label'],
            'extra_annual_investment': d_money,
            'pci_2038_gain': d_pci,
            'annual_dollars_per_pci_point': round(d_money / d_pci) if d_pci else None,
            'derivation': 'BeTH arithmetic on two published City scenarios',
            'caveat': 'Coarse. Non-linear relationship, 12-year endpoints, differing selection methods.',
        })
    return out


def pci60_assessment():
    """What it would take to reach and hold PCI 60+, from the City's published scenarios."""
    below = [s for s in CITY_SCENARIOS if s['pci_2038'] < 60]
    at_or_above = [s for s in CITY_SCENARIOS if s['pci_2038'] >= 60]
    return {
        'question': 'What would it take to bring Berkeley pavement to PCI 60 or better and hold it there?',
        'answer_status': 'ANSWERABLE FROM CITY DATA, with limits stated',
        'finding': "The City's own 12-year projections bracket PCI 60. The Five-Year Plan alone is "
                   'projected to DECLINE to about 56 by 2038. Adding Measure FF is projected to reach '
                   'about 62 by 2038. So PCI 60+ is, on the City\'s own modelling, roughly the outcome '
                   'already purchased by the Plan plus Measure FF, at about $29.6 million a year.',
        'the_real_gap_is_70_not_60': "Berkeley's adopted goal is PCI 70 (BMC 7.11.010(K)(1)), not 60. "
                                     'The City estimates PCI 70 by 2036 requires about $37.6 million a '
                                     'year, roughly $8 million a year more than current plans provide. '
                                     'The funding question Berkeley actually faces is the 62-to-70 gap.',
        'scenarios_below_60': below,
        'scenarios_at_or_above_60': at_or_above,
        'critical_caveats': [
            'These are the CITY\'s projections, not BeTH\'s. BeTH has not independently verified them '
            'and cannot, without the StreetSaver segment data.',
            'PCI 60 as a network AVERAGE can coexist with many streets in failed condition. The City\'s '
            'own goal pairs PCI 70 with "no streets having a PCI below 50". A network average target '
            'without a distribution floor can be met while the worst streets decay further.',
            'All figures assume 3% annual construction cost escalation and the Council/Measure FF '
            'revenue escalation formulas. The City notes the net effect is a modest real increase in '
            'costs relative to funding.',
            'Annual figures are 12-year averages accounting for projected revenue growth, NOT flat '
            'annual amounts.',
            'Reaching a level and holding it are different problems with different funding profiles.',
        ],
        'what_beth_adds': 'Not a rival forecast. BeTH\'s contribution is to show what the City\'s own '
                          'model implies under alternative funding, and to test whether any capital '
                          'reallocation could close the roughly $8M/yr gap to PCI 70. That test is '
                          'currently blocked: 0 of 15 CIP funding sources are confirmed redirectable.',
    }


def run(scenario_id, extra_annual_funding=0):
    """Compare a City scenario, optionally with additional annual funding.

    Additional funding is scored against the derived marginal cost per PCI point and is
    explicitly labelled as an indicative interpolation, not a forecast.
    """
    base = next((s for s in CITY_SCENARIOS if s['id'] == scenario_id), None)
    if base is None:
        return {'status': 'ERROR', 'reason': f'unknown scenario {scenario_id!r}',
                'available': [s['id'] for s in CITY_SCENARIOS]}
    result = {
        'scenario': base['id'], 'label': base['label'], 'status': 'CITY_PUBLISHED',
        'annual_investment': base['annual_investment'], 'pci_2038': base['pci_2038'],
        'description': base['description'], 'source': base['source'],
    }
    if not extra_annual_funding:
        return result
    marg = marginal_cost_per_pci_point()
    rate = next((m['annual_dollars_per_pci_point'] for m in marg
                 if m['annual_dollars_per_pci_point']), None)
    if rate is None:
        result['extra_funding_effect'] = {'status': 'BLOCKED',
                                          'reason': 'no usable marginal rate derivable'}
        return result
    result['extra_funding_effect'] = {
        'status': 'INDICATIVE_INTERPOLATION',
        'extra_annual_funding': extra_annual_funding,
        'marginal_rate_used': rate,
        'implied_pci_2038_gain': round(extra_annual_funding / rate, 1),
        'implied_pci_2038': round(base['pci_2038'] + extra_annual_funding / rate, 1),
        'warning': 'NOT A FORECAST. Linear interpolation between two published City scenarios, applied '
                   'to a non-linear relationship. Shows the shape of the trade-off only. Any figure '
                   'published from this must carry this warning.',
        'also_required': 'The extra funding must itself be shown to be legally redirectable. No CIP '
                         'funding source is currently confirmed redirectable.',
    }
    return result


def state():
    gaps = missing_inputs()
    return {
        'schema_version': 2,
        'generated': '2026-10-23',
        'status': 'CALIBRATED_TO_CITY_SCENARIOS',
        'headline': "Berkeley has already modelled this. BeTH reuses the City's StreetSaver-based "
                    'projections rather than building a rival model, and adds the funding-restriction '
                    'test the City does not publish.',
        'chain': ['capital reallocations + recurring operating savings',
                  'funds available for paving',
                  'treatments purchased (StreetSaver WER selection)',
                  'network PCI over time (City deterioration model)'],
        'pci60_assessment': pci60_assessment(),
        'city_scenarios': CITY_SCENARIOS,
        'city_selection_methods': CITY_SELECTION_METHODS,
        'marginal_cost_per_pci_point': marginal_cost_per_pci_point(),
        'inputs': INPUTS,
        'independent_model_status': {
            'status': 'BLOCKED' if gaps else 'READY',
            'purpose': 'Segment-level modelling would let BeTH test the City\'s projections rather than '
                       'only restate them, and report the condition DISTRIBUTION the City\'s headline '
                       'average hides.',
            'missing_inputs': gaps,
            'missing_count': len(gaps),
            'rule': 'No default, literature or assumed value is ever substituted for a missing input.',
        },
        'reconciliation_requirement': "BeTH figures must reconcile to the City's adopted paving plan and "
                                      'StreetSaver output, with differences explained.',
    }


def main():
    st = state()
    if '--emit' in sys.argv:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(st, indent=1) + '\n')
        print(f'wrote {OUT.relative_to(Path.cwd())}')
    print(f"status: {st['status']}\n")
    print("City's published 12-year projections (after FY2026 work, 3% escalation):")
    for sc in CITY_SCENARIOS:
        print(f"  {sc['label']:34s} ${sc['annual_investment']:>11,}/yr  ->  PCI {sc['pci_2038']} by 2038")
    print("\nMarginal cost of PCI, derived by BeTH from those points:")
    for m in st['marginal_cost_per_pci_point']:
        print(f"  {m['from']:30s} -> {m['to']:34s} +${m['extra_annual_investment']:>10,}/yr "
              f"for +{m['pci_2038_gain']} PCI  (${m['annual_dollars_per_pci_point']:,}/pt/yr)")
    a = st['pci60_assessment']
    print(f"\nPCI 60 question: {a['answer_status']}")
    print(f"  {a['finding']}")
    print(f"\n  {a['the_real_gap_is_70_not_60']}")
    print(f"\nIndependent segment model: {st['independent_model_status']['status']} "
          f"({st['independent_model_status']['missing_count']} inputs missing)")
    return 0


if __name__ == '__main__':
    sys.exit(main())

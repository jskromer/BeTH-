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

_PLAN = ('City of Berkeley, "Five-Year Street Rehabilitation and Measure FF Plans for Fiscal Years '
         '2027-2031", Council Action Calendar, July 7, 2026')
SRC_PLAN = _PLAN + ', pp.11-12 (PCI projections, Figure 1)'
SRC_PLAN_FIG2 = _PLAN + ', p.13 (Figure 2, selection methods)'
SRC_PLAN_BG = _PLAN + ', p.16 (Background)'
SRC_PLAN_METHOD = _PLAN + ', p.8 (selection methods) and pp.11-12'
SRC_PTAP = ('City of Berkeley 2024 Pavement Management Program Update (P-TAP Round 25), Pavement Engineering Inc., '
            'April 2025, Executive Summary pp.2-3 and Section IV street list; see phase2/data/network-condition.json')
SRC_ORD = 'BMC 7.11.010(K)(1), Measure FF initiative text, PDF p.7 (phase2/sources/measure-ff-ordinance-transcription.md)'
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
     'source': SRC_PLAN_FIG2},
    {'id': 'pci_under_50', 'label': 'PCI Under 50 targeting', 'pci_2038': 62,
     'description': "Targets streets below PCI 50, consistent with Measure FF's stated goal of "
                    'addressing long-deferred repairs.',
     'source': SRC_PLAN_FIG2},
]

# ---------------------------------------------------------------- inputs
# Every entry is either a sourced value or None. None means "not held"; it is never
# replaced by a default, a literature value, or an assumption.

INPUTS = {
    'network': {
        'current_network_pci': {'value': 57, 'source': SRC_PLAN_BG, 'confidence': 'High',
                                'note': 'Citywide PCI cited by the City in July 2026. The 2024 inspection (PTAP-25) '
                                        'reports 56; the July 2026 plan starts its projections at 59 "after planned '
                                        'work" in 2026.'},
        'pci_after_fy2026_work': {'value': 59, 'source': SRC_PLAN, 'confidence': 'High'},
        'assessment_cycle': {'value': 'biennial', 'source': SRC_PLAN_METHOD, 'confidence': 'Moderate',
                             'note': 'PCI scored per street section from observed surface distresses, '
                                     'fed into StreetSaver.'},
        'adopted_goal': {'value': 70, 'source': SRC_ORD,
                         'confidence': 'High',
                         'note': 'Goal of citywide PCI 70 "ideally with no streets having a PCI below 50". '
                                 'Measure FF prioritises streets below PCI 50.'},
        'total_lane_miles': {'value': 446.10, 'source': SRC_PTAP, 'confidence': 'High',
                             'note': '212.77 centerline miles; 39,363,218 sq ft of pavement.'},
        'pci_distribution': {'value': 'phase2/data/network-condition.json', 'source': SRC_PTAP, 'confidence': 'High',
                             'note': '1,216 street sections with 2024 PCI, validated to the report totals. 88.75 '
                                     'centerline miles (41.6%) below PCI 50; 33.99 miles (15.9%) below PCI 25. As of '
                                     '2024 inspection, before FY2025-FY2026 paving.'},
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
        'measure_ff_fy2027_revenue': {'value': 16651651, 'source': 'FY2027 adopted budget, Exhibit C p.254; FY2027 '
                                                                  'tax rate report p.1', 'confidence': 'High',
                                      'note': 'Approximately 45% is for streets by ordinance (BMC 7.11.020(C)); the '
                                              'adopted program puts 45.6% into street rehabilitation.'},
        'redirectable_from_capital': {'value': 'phase2/data/street-funding-sources.json',
                                      'source': 'BeTH research, 07-street-funding-legal-analysis.md',
                                      'confidence': 'High',
                                      'note': 'Measure FF: $0 more for paving without voters. CIP Fund 501: at most '
                                              '$2,946,000 of FY2027-28 appropriations, only by deferring every other '
                                              'fund 501 project; one-time carryover unknown. Other sources not yet '
                                              'researched.'},
        'recurring_operating_savings': {'value': None, 'source': None,
                                        'needed_from': 'Payroll and benefit baseline workstream'},
    },
    'escalation': {
        'construction_cost_pct_per_year': {'value': 3.0, 'source': _PLAN + ', p.12', 'confidence': 'High',
                                           'note': 'Reflects recent asphalt and paving material trends.'},
        'revenue_escalation': {'value': 'greater of SF Bay Area cost of living or California per capita '
                                        'personal income growth',
                               'source': 'Council Resolution No. 70,456-N.S. and the Measure FF '
                                         'ordinance, via ' + _PLAN + ', p.12', 'confidence': 'High'},
        'net_effect_stated_by_city': {'value': 'a modest real increase in construction costs relative to '
                                               'available funding over the projection period',
                                      'source': _PLAN + ', p.12', 'confidence': 'High'},
    },
    'methodology': {
        'software': {'value': 'StreetSaver', 'source': SRC_PLAN_METHOD, 'confidence': 'High'},
        'ranking': {'value': 'Weighted Economic Ranking (WER)', 'source': SRC_PLAN_METHOD, 'confidence': 'High',
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


def load(name):
    return json.loads((ROOT / 'data' / name).read_text())


def performance_assessment():
    """Two measures, side by side, never substituted for each other:
    1. network-average PCI (the City's projections), and
    2. the distribution of conditions, including streets below PCI 50."""
    net = load('network-condition.json')['distribution']
    plans = load('street-plan-conditions.json')['plans']
    five, ff, both = plans['five_year_plan']['all_years'], plans['measure_ff']['all_years'], plans['both_plans_fy2027_2031']
    below50, below25 = net['below_pci_50'], net['below_pci_25']
    return {
        'question': 'What would it take to bring Berkeley pavement to PCI 60 or better, and what would that mean for '
                    'the worst streets?',
        'measure_1_network_average': {
            'what': 'Network-average PCI, the measure the City projects.',
            'city_projection_2038': {s['label']: s['pci_2038'] for s in CITY_SCENARIOS},
            'reading': 'On the City\'s projections the Five-Year Plan alone falls to about 56 by 2038; adding Measure FF '
                       '(about $29.6M a year, 12-year average) reaches about 62; reaching 70 by 2036 needs about $37.6M a '
                       'year. These are averages over 213 centerline miles.',
            'source': SRC_PLAN},
        'measure_2_condition_distribution': {
            'what': 'How much of the network is below PCI 50 and below PCI 25 (MTC "failed"), the measure Measure FF\'s '
                    'goal names: PCI 70 "ideally with no streets having a PCI below 50" by December 31, 2036.',
            'now_2024_inspection': {'miles_below_50': below50['centerline_miles'],
                                    'share_below_50': below50['share_of_centerline_miles'],
                                    'miles_below_25': below25['centerline_miles'],
                                    'share_below_25': below25['share_of_centerline_miles'],
                                    'source': SRC_PTAP},
            'treated_by_adopted_plans_fy2027_2031': {
                'five_year_plan': {'miles': five['centerline_miles'], 'miles_below_50': five['miles_below_pci_50']},
                'measure_ff_plan': {'miles': ff['centerline_miles'], 'miles_below_50': ff['miles_below_pci_50']},
                'both': {'miles': both['centerline_miles'], 'miles_below_50': both['miles_below_pci_50']},
                'source': 'July 7, 2026 plan attachments, validated per year; phase2/data/street-plan-conditions.json'},
            'projected_2038': {'value': None,
                               'status': 'NOT PUBLISHED BY THE CITY',
                               'needed_from': 'StreetSaver output of the condition distribution (or miles below PCI 50) '
                                              'under each funding scenario. The Measure FF annual report must include '
                                              '"the PCI of all streets" (BMC 7.11.050(B)(1)).'}},
        'finding': (f'Reaching a network average of 60, or even 62, is not the same as eliminating failed streets. In the '
                    f'2024 inspection the average was 56 while {below50["centerline_miles"]:.1f} centerline miles '
                    f'({below50["share_of_centerline_miles"]:.0%}) were below PCI 50 and {below25["centerline_miles"]:.1f} '
                    f'miles ({below25["share_of_centerline_miles"]:.0%}) were below 25. The two adopted plans treat '
                    f'{both["miles_below_pci_50"]:.1f} miles of currently-below-50 streets over FY2027-FY2031 '
                    f'({ff["miles_below_pci_50"]:.1f} through Measure FF, {five["miles_below_pci_50"]:.1f} through the '
                    f'Five-Year Plan), while other streets deteriorate past 50. Whether the below-50 total shrinks is not '
                    f'shown by any published projection.'),
        'tradeoff_the_city_published': 'Selecting Measure FF streets below PCI 50 instead of by cost-effectiveness lowers '
                                       'the 2038 network average by about one point (62 instead of 63) while treating the '
                                       'worst streets first (City Figure 2). The average and the distribution move in '
                                       'different directions.',
        'the_adopted_goal_is_70': "Berkeley's goal is PCI 70 (BMC 7.11.010(K)(1)), not 60, paired with the below-50 "
                                  'condition. The City estimates PCI 70 by 2036 needs about $8M a year more than the Plan '
                                  'plus Measure FF.',
        'critical_caveats': [
            'Scenario values are the City\'s projections. BeTH restates them; it cannot test them without the City\'s '
            'deterioration curves and treatment catalog.',
            'The distribution is from 2024 inspections, before FY2025-FY2026 paving (about 18.7 centerline miles). '
            'Plan-attachment PCIs are the values printed in July 2026 and will be lower when streets are treated.',
            'Annual investment figures are 12-year averages including revenue growth, not flat annual amounts.',
            'Reaching a level and holding it are different problems with different funding profiles.'],
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
        'status': 'CITY_SCENARIOS_PLUS_MEASURED_DISTRIBUTION',
        'headline': "BeTH reuses the City's StreetSaver projections of the network average and sets beside them the "
                    'measured condition distribution: 41.6% of the network below PCI 50 in the 2024 inspection. An '
                    'average target is not a failed-streets target.',
        'chain': ['capital reallocations + recurring operating savings',
                  'funds available for paving',
                  'treatments purchased (StreetSaver WER selection)',
                  'network PCI over time (City deterioration model)'],
        'performance_assessment': performance_assessment(),
        'city_scenarios': CITY_SCENARIOS,
        'city_selection_methods': CITY_SELECTION_METHODS,
        'marginal_cost_per_pci_point': marginal_cost_per_pci_point(),
        'inputs': INPUTS,
        'independent_model_status': {
            'status': 'BLOCKED' if gaps else 'READY',
            'purpose': 'Segment-level modelling would let BeTH project the condition distribution under each '
                       'funding scenario, which the City does not publish. The current distribution is now held '
                       '(PTAP-25); deterioration curves, treatment catalog and unit costs are not.',
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
    a = st['performance_assessment']
    print(f"\n{a['finding']}")
    print(f"\n  {a['tradeoff_the_city_published']}")
    print(f"\nIndependent segment model: {st['independent_model_status']['status']} "
          f"({st['independent_model_status']['missing_count']} inputs missing)")
    return 0


if __name__ == '__main__':
    sys.exit(main())

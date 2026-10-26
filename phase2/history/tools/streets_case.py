"""Streets and infrastructure case study for "How Did We Get Here?": funding series, competing proposals,
supplement-or-displace analysis, synchronized charts and the public narrative.

Every number is one of:
  - printed     : printed as text in a cited document (checked against the page);
  - image_label : printed inside a chart image (the caption is checked; the value was read from the image);
  - measured    : measured from bar heights in a chart image with no printed values; the method is recorded and was
                  checked against the two bars that do carry printed labels (FY2019 $4.9M, FY2020 $9.8M);
  - derived     : BeTH arithmetic from printed values, with the formula.
Each also has a basis: capital budget, programmed in an adopted five-year plan, planned (future years), adopted budget
change, or actual. No actual expenditures are held yet; the series says so rather than substituting budgets.
"""
import html
import json

e = html.escape
SIGNIFICANCE = {
    'recurring': 'materially changes a recurring commitment',
    'major_funding': 'authorizes major funding',
    'reallocation': 'reallocates resources',
    'targets': 'establishes performance targets',
    'plan_change': 'substantially changes an adopted plan',
    'context': 'context (not a decision; included as evidence)',
}


def register_docs(_doc):
    s = 'phase2/history/sources/streets/'
    _doc('audit:2020-11-19', 'City Auditor, "Rocky Road: Berkeley Streets at Risk and Significantly Underfunded", '
         'November 19, 2020', s + 'auditor-rocky-road-2020-11-19.pdf', 'audit',
         'https://berkeleyca.gov/sites/default/files/2022-01/Rocky-Road-Berkeley-Streets-at-Risk-and-Significantly-Underfunded.pdf')
    _doc('r22:25a', 'Street Maintenance and Rehabilitation Policy and Five Year Plan, staff report, Council Item 25a, '
         'January 18, 2022', s + 'council-2022-01-18-item25a-street-policy-plan.pdf', 'staff_report')
    _doc('r22:25b', 'Public Works Commission Recommendation for the Five-Year Paving Plan, Council Item 25b, '
         'January 18, 2022', s + 'council-2022-01-18-item25b-pwc-five-year-plan.pdf', 'commission_report')
    _doc('r22:25c', 'Updating City of Berkeley Street Maintenance and Rehabilitation Policy (Councilmember Harrison), '
         'Council Item 25c, January 18, 2022', s + 'council-2022-01-18-item25c-harrison-policy.pdf', 'council_item')
    _doc('r23:17', 'Street Rehabilitation Five Year Plan for Fiscal Years 2024-2028, staff report, Council Item 17, '
         'November 28, 2023', s + 'council-2023-11-28-item17-staff-report.pdf', 'staff_report')
    _doc('r23:17-hahn', 'Supplemental 2, Councilmembers Hahn and Wengraf, Item 17, November 28, 2023',
         s + 'council-2023-11-28-item17-hahn-supp2.pdf', 'council_item')
    _doc('aa:2022-06-28', 'City Council annotated agenda, 2022-06-28',
         'phase2/history/sources/council-2022-06-28-annotated.pdf', 'annotated_agenda')
    _doc('aa:2023-06-13', 'City Council annotated agenda, 2023-06-13',
         'phase2/history/sources/council-2023-06-13-annotated.pdf', 'annotated_agenda')


def significance(cite, verified):
    """Significance rule tags for every event (existing and new)."""
    return {
        'bdh-streets-2012-11-measure-m': ['major_funding'],
        'bdh-streets-2016-11-measure-t1': ['major_funding'],
        'bdh-streets-2020-auditor-rocky-road': ['context'],
        'bdh-streets-2022-01-25-res-70204': ['targets', 'plan_change'],
        'bdh-streets-2022-06-28-res-70442-budget': ['recurring', 'major_funding'],
        'bdh-streets-2022-07-26-res-70456': ['recurring', 'targets'],
        'bdh-streets-2022-08-03-res-70492-measure-l': ['major_funding'],
        'bdh-streets-2023-06-13-t1-gap': ['reallocation'],
        'bdh-streets-2023-07-25-res-70997': ['major_funding', 'reallocation'],
        'bdh-streets-2023-11-28-res-71120': ['plan_change', 'reallocation'],
        'bdh-streets-2024-07-30-res-71461-measure-ff': ['major_funding'],
        'bdh-streets-2024-12-10-ord-7952': ['major_funding', 'recurring', 'targets'],
        'bdh-streets-2026-03-17-bond-direction': ['major_funding'],
        'bdh-streets-2026-06-23-res-72340-budget': ['major_funding'],
        'bdh-streets-2026-07-07-res-72377': ['plan_change', 'targets'],
        'bdh-streets-2026-11-bond-ballot': ['major_funding'],
    }


def enrich(events, cite, verified):
    """Add newly collected evidence to fields that were to_collect. Existing citations are never removed."""
    by = {ev['id']: ev for ev in events}

    def upgrade(eid, field, value, *cites, note=None):
        f = by[eid][field]
        assert f['status'] != 'verified' or not f.get('citations'), (eid, field)
        by[eid][field] = verified(value, *cites, note=note)

    upgrade('bdh-streets-2012-11-measure-m', 'money',
            {'amount': 30000000, 'basis': 'ballot authorization (bonds)', 'source': 'general obligation bonds'},
            cite('audit:2020-11-19', 9, 'In 2012, Berkeley voters passed Measure M to secure $30 million'))
    upgrade('bdh-streets-2012-11-measure-m', 'actual',
            'About $25 million of Measure M money appears in the City\'s street rehabilitation capital budgets for '
            'FY2014-FY2018 (BeTH measurement of the Auditor\'s Figure 3; approximate). The Auditor: "Only a portion of '
            'Measure M funds were spent directly on paving costs."',
            cite('audit:2020-11-19', 6, "Figure 3. Berkeley's Street Rehabilitation Program Funded by State and Local Sources"),
            cite('audit:2020-11-19', 13, 'Only a portion of Measure M funds were spent directly on paving costs'),
            note='Budget amounts by year, measured from a chart; not audited expenditures.')
    upgrade('bdh-streets-2016-11-measure-t1', 'money',
            {'amount': 100000000, 'basis': 'ballot authorization (bonds)', 'source': 'general obligation bonds'},
            cite('audit:2020-11-19', 9, 'In 2016, Berkeley voters approved $100 million in general'))
    upgrade('bdh-streets-2016-11-measure-t1', 'actual',
            'As of November 2019, about $36.8 million of T1 had been allocated, about $9.9 million of it to Complete '
            'Streets projects (City Auditor). The January 2022 paving plan added $6.9 million of T1 Phase 2 money.',
            cite('audit:2020-11-19', 9, 'approximately $36.8 million T1 funds were'),
            cite('r22:25a', 1, 'Additional funding includes $6.9 million from Measure T1, Phase 2'))
    upgrade('bdh-streets-2020-auditor-rocky-road', 'purpose',
            'Audit of the Street Rehabilitation Program, FY2014-2020, issued November 19, 2020. Key findings quoted: '
            'General Fund (Capital Improvement Fund) contributions to street rehabilitation "remained stagnant at $1.925 '
            'million per year since 2014"; PCI "increased only slightly from 58 in 2011 to 59 in 2018".',
            cite('audit:2020-11-19', 1, 'November 19, 2020'),
            cite('audit:2020-11-19', 11, 'has remained stagnant at $1.925 million per'),
            cite('audit:2020-11-19', 9, 'PCI increased only slightly from 58 in 2011 to 59 in 2018'))
    by['bdh-streets-2020-auditor-rocky-road']['date'] = '2020-11-19'
    by['bdh-streets-2020-auditor-rocky-road']['date_precision'] = 'report date'
    upgrade('bdh-streets-2022-01-25-res-70204', 'money',
            {'amount': 7275303, 'basis': 'programmed annual paving funding, all sources (FY2023-FY2027 plan)',
             'source': 'gas tax $495,303; Measure BB $2,700,000; Measure F $155,000; Capital Improvement Fund (General '
                       'Fund) $1,925,000; SB1 $2,000,000; plus Measure T1 $6.9M and a $1.2M federal grant'},
            cite('r22:25a', 1, 'TOTAL 7,275,303'), cite('r22:25a', 1, 'Capital Improvement 1,925,000'))
    upgrade('bdh-streets-2022-01-25-res-70204', 'purpose',
            'Staff projected that at the budgeted baseline "the PCI will drop to 52 by the year 2023"; the Public Works '
            'Commission projected citywide PCI of 49.1 by 2027 at the current level of investment. Both plans were '
            'designed within the same funding.',
            cite('r22:25a', 2, 'the PCI will drop to 52 by the year 2023'),
            cite('r22:25b', 2, 'the citywide PCI will be 49.1'))
    upgrade('bdh-streets-2023-11-28-res-71120', 'money',
            {'amount': 14454463, 'basis': 'programmed FY2024 paving funding (FY2025 $18,317,325; FY2026 $17,460,435)',
             'source': 'adds the $8M policy line, Zero Waste and Storm Water funds to the earlier sources'},
            cite('r23:17', 2, 'TOTAL 14,454,463 18,317,325 17,460,435 19,236,589 20,521,028'))
    upgrade('bdh-streets-2023-11-28-res-71120', 'purpose',
            'City staff projection: citywide PCI 55 now, 57 after the five-year plan; the plan "maintains the citywide '
            'PCI in the mid 50\'s" and does not reach "good" (70).',
            cite('r23:17', 6, 'Citywide 55 57'), cite('r23:17', 6, "maintains the citywide PCI in the mid 50's"))

    # competing proposals, as documented at the time (no claim about what either would have produced)
    by['bdh-streets-2022-01-25-res-70204']['competing_proposals'] = [
        {'name': 'Equity Alternative (staff recommendation; adopted, first three years)',
         'cost_five_year': 38385313, 'miles': 15.94,
         'mix': 'Arterials 1.18 mi, collectors 4.06 mi, residential 10.70 mi; Equity Zone 5.21 mi',
         'expected_outcome': 'No separate PCI projection for this plan in the record; staff projected the network PCI '
                             'would fall at the budgeted funding level.',
         'funding_restrictions': 'Same sources and amounts as the other plan ($7,275,303 a year plus T1 and a grant).',
         'tradeoff_as_documented': 'Staff: "These investments are offset by a corresponding reduction of investment in '
                                   'arterials."',
         'citations': [cite('r22:25a', 6, 'Total 15.94 $38,385,313'),
                       cite('r22:25a', 5, 'These investments are offset by a corresponding reduction of investment in arterials')]},
        {'name': 'Arterial Alternative, Plan 12A (Public Works Commission recommendation; not adopted)',
         'cost_five_year': 40027381, 'miles': 15.49,
         'mix': 'Arterials 5.99 mi, collectors 4.12 mi, residential 5.38 mi; Equity Zone 2.19 mi',
         'expected_outcome': 'Commission: citywide PCI 49.1 by 2027 "at the current level of investment" (applies to '
                             'the funding level, not to this plan alone).',
         'funding_restrictions': 'Same sources and amounts.',
         'tradeoff_as_documented': 'Staff: the plan "does not address equity, does much less for residential streets '
                                   'generally". Commission: focuses on "long contiguous stretches of paving on the '
                                   'primary transportation network".',
         'citations': [cite('r22:25a', 5, 'Total 15.49 $40,027,381'),
                       cite('r22:25a', 5, 'does not address equity, does much less for residential streets generally'),
                       cite('r22:25b', 1, 'focusing on long contiguous stretches of paving on the primary transportation network'),
                       cite('r22:25b', 2, 'the citywide PCI will be 49.1')]},
    ]
    by['bdh-streets-2023-11-28-res-71120']['competing_proposals'] = [
        {'name': 'Staff plan as recommended (basis of the adopted resolution)',
         'cost_five_year': None, 'miles': None,
         'mix': 'Hopkins Street held over (on hold per an April 5, 2023 City Manager memo); about $4.75 million of other '
                'Hopkins money moved to paving other streets.',
         'expected_outcome': 'City staff: citywide PCI 55 now, 57 after the plan.',
         'funding_restrictions': 'Programmed funding $14,454,463 in FY2024 rising to $20,521,028 in FY2028; Hopkins T1 '
                                 'money is bond money restricted to T1 projects.',
         'tradeoff_as_documented': 'Staff: the plan "maintains the citywide PCI in the mid 50\'s".',
         'citations': [cite('r23:17', 3, "the Hopkins project is on hold per the City Manager's April 5, 2023 off agenda memo"),
                       cite('r23:17-hahn', 3, 'approximately $4.75 million - are slated to be reallocated'),
                       cite('r23:17', 6, 'Citywide 55 57')]},
        {'name': 'Hahn/Wengraf alternative (failed 4-5)',
         'cost_five_year': None, 'miles': None,
         'mix': 'Add Hopkins Street, The Alameda to Gilman, to the FY2025 list, paid only from the $3.9 million of '
                'Measure T1 money still allocated to Hopkins; parking analysis for the corridor.',
         'expected_outcome': 'No separate PCI projection in the record.',
         'funding_restrictions': 'Uses only T1 money already allocated to Hopkins.',
         'tradeoff_as_documented': 'The supplemental describes the segment as having the lowest PCIs and serving AC '
                                   'Transit routes, the shopping district and King Pool.',
         'citations': [cite('r23:17-hahn', 3, '$3.9 million of T1 funds remain allocated for Hopkins paving'),
                       cite('r23:17-hahn', 2, 'for paving in FY 2025, using only the previously')]},
        {'name': 'Adopted (Humbert/Robinson, All Ayes)',
         'cost_five_year': None, 'miles': None,
         'mix': 'Staff plan plus Milvia Street; Hopkins segments to be completed with Measure T1 funds by the end of FY2027.',
         'expected_outcome': 'As staff projected above.', 'funding_restrictions': 'As above.',
         'tradeoff_as_documented': 'Not stated in the record.',
         'citations': [cite('aa:2023-11-28', 9, 'complete the Hopkins Street segments with Measure T1 funds by the end of FY 2027')]},
    ]

    # two decisions found in the newly collected staff reports, which meet the significance rule
    new = []
    new.append(dict(
        id='bdh-streets-2022-06-28-res-70442-budget', date='2022-06-28', kind='council_decision', item='Action Calendar 44',
        title='Council adopts the FY2023-24 budget, raising General Fund paving money',
        decision=verified('Adopted Resolution No. 70,442-N.S. adopting the FY2023 and FY2024 biennial budget, including '
                          'the proposed capital budget, as revised at the meeting.',
                          cite('aa:2022-06-28', 16, 'to adopt Resolution No. 70,442')),
        instrument=verified({'kind': 'resolution', 'number': '70,442-N.S.'}, cite('aa:2022-06-28', 16, 'Resolution No. 70,442')),
        vote=verified({'mover': 'Arreguin', 'seconder': 'Harrison', 'recorded': 'All Ayes',
                       'present_at_roll_call': ['Kesarwani', 'Taplin', 'Bartlett', 'Hahn', 'Wengraf', 'Robinson', 'Droste', 'Arreguin'],
                       'arrivals': ['Harrison present at 6:06 p.m.'], 'ayes': None, 'noes': None, 'abstain': None, 'absent': None},
                      cite('aa:2022-06-28', 16, 'to adopt Resolution No. 70,442'),
                      cite('aa:2022-06-28', 2, 'Councilmember Harrison present at 6:06 p.m.')),
        money=verified({'amount': 5100000, 'basis': 'adopted budget increase to General Fund paving, FY2023 ($9.0M in '
                                                   'FY2024), as described by staff in November 2023', 'source': 'General Fund'},
                       cite('r23:17', 3, 'increased baseline paving funding from the General Fund by $5.1M in FY 2023 and $9.0M in FY 2024')),
        purpose=verified('Staff (November 2023): "historic and unprecedented investments in paving from the General Fund."',
                         cite('r23:17', 3, 'These were historic and')),
        alternatives=to_collect_f('Budget alternatives for paving considered in June 2022', 'June 14 and June 28, 2022 budget materials'),
        actual=to_collect_f('FY2023 and FY2024 actual paving expenditures', 'CIP actuals; ACFR'),
        outcomes=verified('City staff report 7.0 centerline miles paved in FY2023 (including Southside), "nearly 2-3 times '
                          'the annual rate for the preceding four years", and attribute it to Council\'s increase to '
                          'baseline paving funding. The City\'s attribution, not a BeTH finding.',
                          cite('r23:17', 4, 'nearly 2-3')),
        outstanding=verified('Carried forward by the July 26, 2022 policy (next event).', note='See the next event.'),
        uncertainties=['The FY2024 plan programs $8,124,160 of General Fund paving money (baseline plus policy), which is '
                       'not the "$9.0M" increase staff describe for FY2024; the difference is not explained in the record.',
                       'The record does not list individual names for "All Ayes" votes.'],
        retrospective_scenarios=[]))
    new.append(dict(
        id='bdh-streets-2023-06-13-t1-gap', date='2023-06-13', kind='council_decision', item='Action Calendar 25',
        title='Council closes the Measure T1 funding gap, moving $2.8 million from the Hopkins project',
        decision=verified('Approved the Budget & Finance Committee recommendation to cover the Measure T1 funding gap, '
                          'including $4,050,000 from the Workers\' Compensation Fund and $2,800,000 of the $6,750,000 '
                          'allocated to the Hopkins Bike/Pedestrian T1 project.',
                          cite('aa:2023-06-13', 11, 'Use $4,050,000 from the Workers Compensation Fund'),
                          cite('aa:2023-06-13', 11, 'Use $2,800,000 of $6,750,000 allocated for the Hopkins Bike/Pedestrian T1')),
        instrument=not_in_record_f('Direction by motion; no resolution number in the annotated agenda.'),
        vote=verified({'mover': 'Arreguin', 'seconder': 'Harrison', 'recorded': 'All Ayes',
                       'present_at_roll_call': ['Kesarwani', 'Taplin', 'Harrison', 'Hahn', 'Wengraf', 'Robinson', 'Humbert'],
                       'arrivals': ['Arreguin present at 7:13 p.m.', 'Bartlett present at 7:26 p.m.'],
                       'ayes': None, 'noes': None, 'abstain': None, 'absent': None},
                      cite('aa:2023-06-13', 11, 'M/S/C (Arreguin/Harrison) to approve the recommendation of'),
                      cite('aa:2023-06-13', 2, 'Mayor Arreguin present at 7:13 p.m.')),
        money=verified({'amount': 2800000, 'basis': 'reallocation of bond-funded project budget', 'source': 'Measure T1'},
                       cite('aa:2023-06-13', 11, 'Use $2,800,000 of $6,750,000 allocated for the Hopkins Bike/Pedestrian T1')),
        purpose=verified('"Identify up to $9.062M to cover the Measure T1 funding gap in order to complete the current '
                         'remaining T1 projects."', cite('aa:2023-06-13', 11, 'Identify up to $9.062M to cover the Measure T1 funding gap')),
        alternatives=to_collect_f('Options presented for closing the gap', 'June 13, 2023 staff report; Budget & Finance Committee'),
        actual=verified('In November 2023 staff reported $3.9 million of T1 money still allocated to Hopkins paving, and '
                        'Council later directed the Hopkins segments be completed with T1 funds by the end of FY2027.',
                        cite('r23:17-hahn', 3, '$3.9 million of T1 funds remain allocated for Hopkins paving')),
        outcomes=to_collect_f('Hopkins paving status', 'Public Works project status'),
        outstanding=verified('The $4,050,000 drawn from the Workers\' Compensation Fund; repayment terms are not in the '
                             'annotated agenda.', cite('aa:2023-06-13', 11, 'Use $4,050,000 from the Workers Compensation Fund')),
        uncertainties=['Whether the $4,050,000 from the Workers\' Compensation Fund is a loan or a transfer, and how it was '
                       'booked, is not established. It is separate from the $5.5M Marina loan six weeks later.',
                       'The record does not list individual names for "All Ayes" votes.'],
        retrospective_scenarios=[]))
    events.extend(new)
    tags = significance(cite, verified)
    for ev in events:
        ev['significance'] = [{'criterion': t, 'label': SIGNIFICANCE[t]} for t in tags[ev['id']]]
    return events


def to_collect_f(what, where=None):
    return {'status': 'to_collect', 'value': None, 'needed': what, 'where_to_look': where}


def not_in_record_f(what):
    return {'status': 'not_in_record', 'value': None, 'needed': what}


# ------------------------------------------------------------------ funding series

def funding_series(cite):
    fig3 = cite('audit:2020-11-19', 6, "Figure 3. Berkeley's Street Rehabilitation Program Funded by State and Local Sources")
    fig10 = cite('audit:2020-11-19', 14, 'Figure 10. An Estimated Additional $10 Million Needed per Year')
    measured = {  # FY: (total, bond, components) measured from Figure 3 at 200 dpi (see method)
        2014: (6.0, 2.5, 'Measure M ~2.5; CIF ~1.9; gas tax ~0.8; Measure B ~0.7; Measure F ~0.1'),
        2015: (10.0, 6.0, 'Measure M ~6.0; CIF ~1.9; gas tax ~0.8; Measure B ~0.7; Measure F ~0.6'),
        2016: (11.3, 6.0, 'Measure M ~6.0; CIF ~1.9; Measure BB ~1.6; gas tax ~0.8; Measure B ~0.7; Measure F ~0.2; Successor Agency ~0.1'),
        2017: (11.2, 6.0, 'Measure M ~6.0; CIF ~1.9; Measure BB ~1.6; gas tax ~0.8; Measure B ~0.7; Measure F ~0.2'),
        2018: (8.7, 4.4, 'Measure M ~4.4; CIF ~1.9; Measure BB ~1.1; Measure B ~0.7; gas tax ~0.5'),
    }
    pts = []
    for fy, (tot, bond, comp) in measured.items():
        pts.append({'fy': fy, 'total_m': tot, 'bond_m': bond, 'recurring_m': round(tot - bond, 1), 'measure_ff_m': 0,
                    'basis': 'capital budget', 'value_type': 'measured', 'components': comp, 'citation': fig3})
    pts.append({'fy': 2019, 'total_m': 4.9, 'bond_m': 0.0, 'recurring_m': 4.9, 'measure_ff_m': 0, 'basis': 'capital budget',
                'value_type': 'image_label', 'components': 'No bond money (Figure 3)', 'citation': fig10})
    pts.append({'fy': 2020, 'total_m': 9.8, 'bond_m': 2.8, 'recurring_m': 7.0, 'measure_ff_m': 0, 'basis': 'capital budget',
                'value_type': 'image_label', 'components': 'Measure T1 ~2.8 (measured); recurring ~7.0', 'citation': fig10})
    for fy in (2021, 2022):
        pts.append({'fy': fy, 'total_m': 7.0, 'bond_m': 0.0, 'recurring_m': 7.0, 'measure_ff_m': 0,
                    'basis': 'planned (FY2020 Capital Improvement Program, as reported by the Auditor)',
                    'value_type': 'image_label', 'components': 'Excludes T1', 'citation': fig10})
    pts.append({'fy': 2023, 'total_m': 14.850303, 'bond_m': 6.375, 'recurring_m': 7.275303, 'measure_ff_m': 0,
                'other_m': 1.2, 'basis': 'programmed in the January 2022 five-year plan',
                'value_type': 'printed', 'components': 'Recurring $7,275,303; Measure T1 $6,375,000; federal grant $1,200,000. '
                'Staff later reported a further $5.1M General Fund increase adopted June 28, 2022 for FY2023 (not added here: '
                'different document and basis).',
                'citation': cite('r22:25a', 2, 'Measure T1 6,375,000')})
    for fy, v in ((2024, 14454463), (2025, 18317325), (2026, 17460435)):
        pts.append({'fy': fy, 'total_m': v / 1e6, 'bond_m': 0.0, 'recurring_m': v / 1e6, 'measure_ff_m': 0,
                    'basis': 'programmed in the November 2023 five-year plan', 'value_type': 'printed',
                    'components': 'Includes the $8M policy line, Zero Waste and Storm Water funds',
                    'citation': cite('r23:17', 2, 'TOTAL 14,454,463 18,317,325 17,460,435 19,236,589 20,521,028')})
    ff = {2027: 13198842, 2028: 6822998, 2029: 7805256, 2030: 5524906, 2031: 8767933}
    plan26 = {2027: 18742503, 2028: 18997119, 2029: 19259373, 2030: 19529496, 2031: 19807721}
    for fy, v in plan26.items():
        pts.append({'fy': fy, 'total_m': (v + ff[fy]) / 1e6, 'bond_m': 0.0, 'recurring_m': v / 1e6, 'measure_ff_m': ff[fy] / 1e6,
                    'basis': 'planned (July 2026 five-year plan; FY2027-28 appropriated, FY2029-31 planned)',
                    'value_type': 'printed',
                    'components': f'Five-Year Paving Plan ${v:,}; Measure FF street rehabilitation ${ff[fy]:,}',
                    'citation': cite('plan:2026-07-07', 2, f'{v:,}') if fy <= 2029 else
                    cite('plan:2026-07-07', 3, 'TOTAL $19,529,496 $19,807,721'),
                    'ff_citation': cite('budget:2026-06-23', 215, '13,198,842')})
    return {
        'what': 'Street rehabilitation (paving) funding by fiscal year, $ millions, on the basis each source reports. '
                'Budgets and plans, not actual expenditures.',
        'value_types': {'measured': 'measured from bar heights in the Auditor\'s Figure 3 (no printed values); method '
                                    'checked against the FY2019 and FY2020 bars, which the Auditor labels $4.9M and $9.8M '
                                    'in Figure 10: measured $4.89M and $9.82M; about +/-$0.1M',
                        'image_label': 'printed inside a chart image in the Auditor\'s report',
                        'printed': 'printed as text in the cited table'},
        'definition_changes': [
            '2014-2020 (Auditor): "Street Rehabilitation Program" capital budget by source, including bond money.',
            'FY2023-FY2026 (five-year plans): programmed paving funding; from FY2024 includes the $8M General Fund policy '
            'line and ratepayer funds from Zero Waste and Storm Water.',
            'FY2027 on: the 2026 plan prints one "SB 1" line ($2,195,303) equal to the earlier separate State Transportation '
            'Tax ($495,303) and SB1 ($1,700,000) lines; Storm Water renamed Clean Storm and programmed at $1,000,000.',
            'Measure FF street rehabilitation (FY2027 on) is a separate voter-restricted program, shown separately.',
            'Actual expenditures are not in this series.'],
        'points': pts,
        'gaps': ['FY2010-FY2013: no paving funding series held. The Auditor gives only the FY2013 General Fund '
                 '(Capital Improvement Fund) contribution, $2.8M.',
                 'Actual expenditures for every year.'],
        'notes': {'cif_fy2013': {'value_m': 2.8, 'citation': cite('audit:2020-11-19', 13,
                                                                  'contributions to streets capital declined from $2.8 million')}},
    }


def table_checks(page_text, norm):
    """Arithmetic in the City's funding tables. Known errors are recorded, never corrected."""
    out = {'checked': [], 'city_table_errors': []}
    jan22 = [495303, 2700000, 155000, 1925000, 2000000]
    out['checked'].append({'table': 'January 2022 plan, Table 1 (each year)', 'sum': sum(jan22), 'printed': 7275303,
                           'ok': sum(jan22) == 7275303})
    nov23 = {2024: [495303, 1700000, 2980000, 155000, 2127562, 5996598, 1000000, 0, 14454463],
             2025: [495303, 1700000, 2980000, 155000, 1925000, 8937022, 1000000, 1125000, 18317325],
             2026: [495303, 1700000, 2980000, 155000, 1925000, 9205132, 1000000, 0, 17460435],
             2027: [495303, 1700000, 2980000, 155000, 1925000, 9481286, 2000000, 1500000, 19236589],
             2028: [495303, 1700000, 2980000, 155000, 1925000, 9765725, 2000000, 1500000, 20521028]}
    for fy, row in nov23.items():
        s, p = sum(row[:-1]), row[-1]
        out['checked'].append({'table': f'November 2023 plan, Table 1, FY{fy}', 'sum': s, 'printed': p, 'ok': s == p})
        if s != p:
            out['city_table_errors'].append({'table': f'November 2023 plan, Table 1, FY{fy}', 'components_sum': s,
                                             'printed_total': p, 'difference': s - p,
                                             'note': 'Recorded, not corrected. The other four columns add up.'})
    jul26 = {2027: [2195303, 2980000, 155000, 1925000, 8487200, 2000000, 1000000, 18742503],
             2028: [2195303, 2980000, 155000, 1925000, 8741816, 2000000, 1000000, 18997119],
             2029: [2195303, 2980000, 155000, 1925000, 9004070, 2000000, 1000000, 19259373]}
    for fy, row in jul26.items():
        out['checked'].append({'table': f'July 2026 plan, Table 1A, FY{fy}', 'sum': sum(row[:-1]), 'printed': row[-1],
                               'ok': sum(row[:-1]) == row[-1]})
    return out


def displacement_analysis(cite):
    """Did new money add to existing street funding or replace it? Each item: evidence, BeTH reading, status."""
    return [
        {'id': 'disp-1-measure-m-cif', 'period': 'FY2013-FY2014',
         'observation': 'The General Fund\'s Capital Improvement Fund contribution to streets capital fell from $2.8M in '
                        'FY2013 to $1.9M in FY2014, the year Measure M bond money first appears in the street budget, and '
                        'stayed at $1.925M a year through at least FY2027.',
         'reading': 'Timing is consistent with partial displacement of General Fund money by bond money. The record does '
                    'not say why the contribution fell; the Auditor does not attribute it to Measure M.',
         'status': 'possible displacement; cause not established',
         'citations': [cite('audit:2020-11-19', 13, 'contributions to streets capital declined from $2.8 million'),
                       cite('audit:2020-11-19', 11, 'has remained stagnant at $1.925 million per')]},
        {'id': 'disp-2-baseline-held', 'period': 'FY2023-FY2031',
         'observation': 'After the 2022 policy, the $1,925,000 General Fund baseline line stays in every plan alongside the '
                        'new policy line ($5,996,598 in FY2024; $8,487,200 in FY2027).',
         'reading': 'On the General Fund lines, the new money was added on top of the old baseline, not substituted for it.',
         'status': 'supplemented (programmed amounts; actuals not yet checked)',
         'citations': [cite('r23:17', 2, '5,996,598 8,937,022 9,205,132 9,481,286 9,765,725'),
                       cite('plan:2026-07-07', 2, '$8,487,200')]},
        {'id': 'disp-3-baseline-label', 'period': 'July 2022',
         'observation': 'Res. 70,456-N.S. describes "the existing General Fund street paving budget of $7.3 million". The '
                        'January 2022 plan\'s $7,275,303 baseline was all sources: only $1,925,000 of it was General Fund; '
                        'the rest was gas tax, SB1, Measure BB and Measure F.',
         'reading': 'The $15.3M figure that later became Measure FF\'s maintenance-of-effort floor ("from sources other '
                    'than this tax") was built on an all-sources baseline, though the resolution called it General Fund.',
         'status': 'documented discrepancy in wording; effect on the floor is that state and county money counts toward it',
         'citations': [cite('aa:2022-07-26-special', 4, 'existing General Fund street paving budget of $7.3 million'),
                       cite('r22:25a', 1, 'TOTAL 7,275,303'), cite('r22:25a', 1, 'Capital Improvement 1,925,000')]},
        {'id': 'disp-4-ratepayer-funds', 'period': 'FY2024 on',
         'observation': 'From FY2024 the paving plans add Zero Waste rate revenue ($1M, then $2M a year) "to offset the impact '
                        'of Zero Waste collection vehicles" and Storm Water money for required green infrastructure.',
         'reading': 'These are new sources, not General Fund. Whether they count toward the $15.3M Measure FF floor is not '
                    'stated in BeTH\'s sources; if they do, General Fund paving could fall by the same amount without '
                    'breaching it.',
         'status': 'open question',
         'citations': [cite('r23:17', 2, 'Zero Waste Fund 1,000,000 1,000,000 1,000,000 2,000,000 2,000,000')]},
        {'id': 'disp-5-fy2027-policy-amount', 'period': 'FY2027',
         'observation': 'The November 2023 plan programmed $9,481,286 of policy money for FY2027; the July 2026 plan '
                        'programs $8,487,200 (= $8,000,000 x 1.0609), about $1.0M less. Storm Water is $1.0M rather than '
                        '$1.5M.',
         'reading': 'The adopted FY2027 General Fund paving amount is lower than the earlier plan projected. The documents '
                    'BeTH holds do not explain the change in the inflation base.',
         'status': 'reduction relative to an earlier plan; reason not in the record',
         'citations': [cite('r23:17', 2, '5,996,598 8,937,022 9,205,132 9,481,286 9,765,725'),
                       cite('plan:2026-07-07', 2, '$8,487,200')]},
    ]


# ------------------------------------------------------------------ synchronized charts

def fy_of(date):
    y, m = int(date[:4]), int(date[5:7]) if len(date) >= 7 else 1
    return y + 1 if m >= 7 else y


SYNC_CSS = '''
.widefig{width:min(1100px,calc(100vw - 40px));position:relative;left:50%;transform:translateX(-50%)}
.sync{overflow-x:auto;background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:14px 16px;margin:14px 0}
.sync-in{min-width:820px}
.srow{display:grid;grid-template-columns:110px repeat(22,1fr);align-items:end;column-gap:3px;position:relative}
.srow .lab{font-size:12.5px;color:var(--muted);align-self:center;padding-right:6px;line-height:1.25}
.sb{position:relative;height:150px;display:flex;flex-direction:column;justify-content:flex-end;align-items:stretch}
.sb .seg{display:block;border-radius:0}
.sb .tv{font-size:10.5px;text-align:center;font-variant-numeric:tabular-nums;color:var(--ink);margin-bottom:2px}
.sb.future{background:repeating-linear-gradient(135deg,transparent 0 6px,rgba(27,58,99,.05) 6px 7px)}
.seg.approx{background-image:repeating-linear-gradient(135deg,rgba(255,255,255,.55) 0 3px,transparent 3px 6px)}
.pm{position:relative;height:110px;border-bottom:1px solid #c3c2b7}
.pm .d{position:absolute;left:50%;width:9px;height:9px;margin:0 0 -4px -4px;border-radius:50%}
.pm .d.mtc{background:#2a78d6}.pm .d.city{background:#eb6834}.pm .d.proj{background:#fff;border:2px solid #eb6834;width:8px;height:8px}
.yr{font-size:10.5px;color:var(--muted);text-align:center}
.drow .mk{display:flex;justify-content:center;gap:2px;flex-wrap:wrap;min-height:22px}
.drow .mk a{display:inline-block;min-width:18px;height:18px;line-height:18px;border-radius:9px;background:var(--navy);color:#fff;
font-size:10.5px;text-align:center;text-decoration:none;padding:0 3px}
.drow .mk a.voter{background:var(--gold)}.drow .mk a.context{background:#9aa3ad}
.vline{position:absolute;top:0;bottom:0;width:0;border-left:1px dashed rgba(27,58,99,.35);pointer-events:none}
.nowline{border-left:2px solid var(--gold)}
'''


PAVING_MAINT = '#1b3a63'  # overlay, sealing and patching (actuals row); street reconstruction uses design.AQUA


def sync_chart(events, funding, miles, pci_mtc, pci_city_extra, design, actuals=None):
    years = list(range(2010, 2032))
    fp = {p['fy']: p for p in funding['points']}
    ap = {p['fy']: p for p in (actuals or [])}
    # one dollar scale for the budget row and the actuals row, so bar heights compare like with like
    top_f = max([p['total_m'] for p in funding['points']] +
                [sum(p[k] or 0 for k in ('street_reconstruction', 'overlay_sealing', 'patching')) / 1e6
                 for p in ap.values()])
    mp = {}
    for p in miles['points']:
        fy = int(p['fy'][2:6])
        mp[fy] = p
    top_m = max(p['miles'] for p in miles['points'])
    # decisions by fiscal year, numbered in date order
    evs = sorted(events, key=lambda x: x['date'])
    num = {ev['id']: i + 1 for i, ev in enumerate(evs)}
    byfy = {}
    for ev in evs:
        if ev['kind'] == 'context' and False:
            continue
        byfy.setdefault(fy_of(ev['date']), []).append(ev)

    def cell_f(y):
        p = fp.get(y)
        fut = ' future' if y >= 2027 else ''
        if not p:
            return f'<div class="sb{fut}" title="FY{y}: no funding data held"><span class="tv" style="color:#9aa3ad">–</span></div>'
        segs = ''
        h = 150 - 16
        for key, col, lbl in (('measure_ff_m', design.YELLOW, 'Measure FF'), ('other_m', '#9aa3ad', 'grant'),
                              ('bond_m', design.ORANGE, 'bond'), ('recurring_m', design.BLUE, 'recurring')):
            v = p.get(key) or 0
            if v:
                approx = ' approx' if p['value_type'] == 'measured' else ''
                segs += (f'<span class="seg{approx}" style="height:{v / top_f * h:.1f}px;background-color:{col}" '
                         f'title="FY{y} {lbl}: ${v:.1f}M ({e(p["basis"])}; {p["value_type"]})"></span>')
        lab = f'{p["total_m"]:.1f}' + ('~' if p['value_type'] == 'measured' else '')
        return f'<div class="sb{fut}"><span class="tv">{lab}</span>{segs}</div>'

    def cell_a(y):
        p = ap.get(y)
        if not p:
            note = 'not yet published by the State Controller' if y == 2026 else 'not applicable' if y > 2026 else 'not held'
            return f'<div class="sb" title="FY{y}: actual spending {note}"></div>'
        h = 150 - 16
        segs = ''
        for key, col, lbl in (('overlay_sealing', PAVING_MAINT, 'overlay and sealing'), ('patching', PAVING_MAINT, 'patching'),
                              ('street_reconstruction', design.AQUA, 'street reconstruction')):
            v = (p[key] or 0) / 1e6
            if v:
                segs += (f'<span class="seg" style="height:{v / top_f * h:.1f}px;background-color:{col}" '
                         f'title="FY{y} {lbl}: ${v:.2f}M actual (City-reported to the State Controller; not audited)"></span>')
        values = [p[k] for k in ('street_reconstruction', 'overlay_sealing', 'patching')]
        if all(v is None for v in values):
            return '<div class="sb" title="Actual spending not reported"></div>'
        tot = sum(v for v in values if v is not None) / 1e6
        suffix = '*' if None in values else ''
        return f'<div class="sb"><span class="tv">{tot:.1f}{suffix}</span>{segs}</div>'

    def cell_m(y):
        p = mp.get(y)
        if not p:
            return '<div class="sb" style="height:110px"></div>'
        col = design.BLUE if p['basis'] == 'actual' else design.LIGHT_BLUE
        return (f'<div class="sb" style="height:110px"><span class="tv">{p["miles"]}</span>'
                f'<span class="seg" style="height:{p["miles"] / top_m * 90:.1f}px;background:{col}" '
                f'title="FY{y}: {p["miles"]} centerline miles ({p["basis"]})"></span></div>')

    lo, hi = 45, 62

    def cell_p(y):
        d = ''
        for p in pci_mtc['points']:
            if p['year'] == y:
                d += (f'<span class="d mtc" style="bottom:{(p["pci"] - lo) / (hi - lo) * 100:.1f}%" '
                      f'title="MTC {y} (3-yr avg, {p["edition"]} ed.): {p["pci"]}"></span>')
        for p in pci_city_extra:
            if p['year'] == y:
                cls = 'proj' if p['kind'] == 'projection' else 'city'
                d += (f'<span class="d {cls}" style="bottom:{(p["pci"] - lo) / (hi - lo) * 100:.1f}%" '
                      f'title="City {y}: {p["pci"]} ({e(p["label"])})"></span>')
        return f'<div class="pm">{d}</div>'

    def cell_d(y):
        a = ''.join(f'<a class="{"voter" if ev["kind"] == "voter_decision" else "context" if ev["kind"] == "context" else ""}" '
                    f'href="#{e(ev["id"])}" title="{e(ev["date"])}: {e(ev["title"])}">{num[ev["id"]]}</a>'
                    for ev in byfy.get(y, []))
        return f'<div class="mk">{a}</div>'

    rows = (f'<div class="srow drow"><div class="lab">Decisions (click)</div>{"".join(cell_d(y) for y in years)}</div>'
            f'<div class="srow"><div class="lab">Paving funding, $M (budgets and plans)</div>{"".join(cell_f(y) for y in years)}</div>'
            + (f'<div class="srow"><div class="lab">Actual spending, $M: Street Reconstruction plus Overlay and Sealing and Patching, as the City reported them to the State Controller; not audited '
               f'(City-reported)</div>{"".join(cell_a(y) for y in years)}</div>' if ap else '') +
            f'<div class="srow"><div class="lab">Centerline miles paved</div>{"".join(cell_m(y) for y in years)}</div>'
            f'<div class="srow"><div class="lab">Pavement condition (PCI), scale 45-62</div>{"".join(cell_p(y) for y in years)}</div>'
            f'<div class="srow"><div class="lab"></div>{"".join(f"<div class=yr>{str(y)[2:]}</div>" for y in years)}</div>')
    legend = design.legend([('Recurring funding', design.BLUE), ('Bond (one-time)', design.ORANGE), ('Grant', '#9aa3ad'),
                            ('Measure FF', design.YELLOW)] + ([('Actual: street reconstruction', design.AQUA),
                            ('Actual: overlay, sealing, patching', PAVING_MAINT)] if ap else []) + [('Miles: actual', design.BLUE), ('Miles: projected', design.LIGHT_BLUE),
                            ('PCI: MTC 3-yr average', '#2a78d6'), ('PCI: City single year', '#eb6834')])
    body = (legend + '<p class="note" style="margin:4px 0 8px">Hatched bars: measured from a chart (approximate, marked ~). '
            'Shaded columns FY2027-31: plans, not results. The actual-spending row is what the City reported spending to the '
            'State Controller (not audited, and not paving-only: street reconstruction can include safety and complete-streets '
            'work); design and administration are excluded; FY2026 is not yet published. Budgets and actuals share one dollar '
            'scale but must not be added together. * Actual spending is a subtotal of reported categories; blank '
            'categories remain unknown, not zero. Hollow orange dots: City projections. Columns are fiscal years '
            '(July-June) for funding and miles, calendar years for PCI. Numbered markers: decisions; click to open the card.</p>'
            f'<div class="sync"><div class="sync-in">{rows}</div></div>')
    return design.chart('Funding, paving and pavement condition, 2010-2031, on one timeline',
                        'Three different measures on a shared year axis. Lining them up shows sequence, not cause.', body,
                        'Sources: City Auditor 2020 (Figures 3 and 10); January 2022, November 2023 and July 2026 paving plans; '
                        'adopted FY2027-28 budget p.215 (Measure FF); MTC PCI tables; City and consultant PCI figures. '
                        'Actual spending: the City\'s Annual Street Reports to the State Controller, FY2010-FY2025 (not audited).'), num


# ------------------------------------------------------------------ narrative

def narrative(claims):
    out = ''
    for c in claims:
        ev = ''.join(f'<li>{c["render"](x)}</li>' for x in c['citations'])
        out += (f'<div class="nclaim"><p>{e(c["text"])}</p><details class="nev"><summary>Evidence ({len(c["citations"])}) · '
                f'<span>{e(c["evidence_class"])}</span></summary><div><ul class="cites">{ev}</ul>'
                + (f'<p class="note">{e(c["caveat"])}</p>' if c.get('caveat') else '') + '</div></details></div>')
    return out


NARRATIVE_CSS = '''
.nclaim{background:var(--card);border:1px solid var(--rule);border-left:4px solid var(--navy);border-radius:10px;padding:10px 16px;margin:10px 0}
.nclaim p{margin:.2em 0 .4em}.nev summary{font-size:14px;color:var(--navy);cursor:pointer}
.nev summary span{color:var(--muted)}.nev>div{padding:4px 0 2px}
.draftbadge{display:inline-block;background:#b45309;color:#fff;font-weight:700;font-size:12px;letter-spacing:.06em;padding:4px 10px;border-radius:4px;margin:10px 0}
.cmp{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;margin:8px 0}
.cmp>div{background:#f6f3ec;border-radius:8px;padding:10px 12px;font-size:14.5px}
.cmp h5{margin:0 0 6px;font-size:14.5px;color:var(--navy)}
.cmp dl{margin:0}.cmp dt{font-weight:600;font-size:12.5px;color:var(--muted);margin-top:5px}.cmp dd{margin:0}
'''


def proposals_html(props, render_cite):
    cards = ''
    for p in props:
        cost = f'${p["cost_five_year"]:,}' if p.get('cost_five_year') else 'Not stated for this proposal'
        miles = f'{p["miles"]} miles' if p.get('miles') else 'Not stated'
        cards += (f'<div><h5>{e(p["name"])}</h5><dl><dt>Five-year cost</dt><dd>{e(cost)}</dd><dt>Miles</dt><dd>{e(miles)}</dd>'
                  f'<dt>What it paved</dt><dd>{e(p["mix"])}</dd><dt>Expected outcome (as documented)</dt>'
                  f'<dd>{e(p["expected_outcome"])}</dd><dt>Funding and restrictions</dt><dd>{e(p["funding_restrictions"])}</dd>'
                  f'<dt>Tradeoffs (as documented)</dt><dd>{e(p["tradeoff_as_documented"])}</dd></dl>'
                  f'<details class="nev"><summary>Sources</summary><ul class="cites">'
                  + ''.join(f'<li>{render_cite(c)}</li>' for c in p['citations']) + '</ul></details></div>')
    return (f'<div class="cmp">{cards}</div><p class="note">Proposals as documented at the time. BeTH does not estimate what '
            'either would have produced: no retrospective scenario has been modelled.</p>')

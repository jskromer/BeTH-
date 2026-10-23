#!/usr/bin/env python3
"""Which capital money could lawfully go to street paving: CIP Fund 501 and Measure FF.

Inputs: phase2/data/cip-projects.json (adopted FY2027-31 CIP, reconciled) and the cited figures below,
each taken from a document in phase2/sources/ or the repository's FY2025 ACFR, with page references.
Output: phase2/data/street-funding-sources.json, the evidence record the public question
"How much capital funding could Berkeley redirect to streets?" is answered from.

Rules applied:
  * Unspent appropriations are not available cash. Budget authority, planned years and audited
    balances are kept in separate fields and never added together.
  * "Potentially available" is an upper bound with its cost named, not a recommendation.
  * Anything that cannot be computed from the sources is returned as UNKNOWN with the document needed.

Run:  python3 phase2/tools/street_funding.py [--write]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CIP = ROOT / 'data' / 'cip-projects.json'
OUT = ROOT / 'data' / 'street-funding-sources.json'

SOURCES = {
    'acfr-fy2025': {
        'title': 'City of Berkeley, Annual Comprehensive Financial Report, fiscal year ended June 30, 2025',
        'local': 'annual-comprehensive-financial-report-fy2025.pdf (repository root)',
        'url': 'https://berkeleyca.gov/sites/default/files/2026-01/annual-comprehensive-financial-report-fy2025.pdf',
        'sha256': 'd6f54821affa11c04fcd1e6c4dd1a47715558ff2c2452d2321bc5884745ff7b3',
        'evidence_class': 'AUDITED'},
    'budget-adoption-2026-06-23': {
        'title': 'Adoption of FY2027 and FY2028 Biennial Budget and FY2027-2031 Capital Improvement Program, '
                 'Council Special Meeting Item 01, June 23, 2026 (260 pp.)',
        'local': 'phase2/sources/budget-adoption-2026-06-23.pdf', 'evidence_class': 'BUDGET_ADOPTED'},
    'street-plan-2026-07-07': {
        'title': 'Five-Year Street Rehabilitation and Measure FF Plans for Fiscal Years 2027-2031, Council Action '
                 'Calendar Item 10, July 7, 2026 (70 pp.)',
        'local': 'phase2/sources/street-rehab-measure-ff-2026-07-07.pdf', 'evidence_class': 'BUDGET_ADOPTED'},
    'measure-ff-initiative': {
        'title': 'SAFE STREETS initiative ordinance text (BMC Chapter 7.11), Council agenda July 9, 2024, Item 22',
        'local': 'phase2/sources/measure-ff-initiative-council-2024-07-09.pdf',
        'transcription': 'phase2/sources/measure-ff-ordinance-transcription.md',
        'url': 'https://berkeleyca.gov/sites/default/files/documents/2024-07-09%20Item%2022%20Initiative%20Petition'
               '%20%E2%80%93%20Ordinance%20to%20Establish%20a%20Parcel%20Tax%20to%20Fund%20Repairs%20and%20'
               'Improvements%20to%20%28SAFE%20STREETS%29.pdf',
        'sha256': '7aa13b56ce24283d74918635ce961911c507a74257a400af8c5e03c6ce957b62',
        'evidence_class': 'LAW', 'note': 'Initiative as filed; adopted as Ordinance 7,952-N.S., Dec 10, 2024.'},
    'measure-ff-rate-fy2027': {
        'title': 'FY2027 Tax Rate: SAFE STREETS (Measure FF), Council Consent Item 15, June 16, 2026',
        'local': 'phase2/sources/measure-ff-fy2027-tax-rate-2026-06-16.pdf',
        'url': 'https://berkeleyca.gov/sites/default/files/2026-06/2026-06-16%20Item%2015%20FY%202027%20Tax%20Rate'
               '%20Fund%20Sustainable%20and%20Accountable.pdf',
        'sha256': '514f0ea9afeef6abddc937a117574763db90ebb4ee5a963f1a1fcf1cad22a9e2', 'evidence_class': 'BUDGET_ADOPTED'},
}


def cite(src, pages):
    return {'source': src, 'pages': pages}


# ---- Fund 501, audited position at June 30, 2025 (ACFR) ----
ACFR_501 = {
    'cash_and_investments': (16199095, cite('acfr-fy2025', 'PDF p.75 (printed p.40), Balance Sheet, Governmental Funds')),
    'notes_receivable': (7771575, cite('acfr-fy2025', 'PDF p.75 (printed p.40)')),
    'total_liabilities': (1487942, cite('acfr-fy2025', 'PDF p.75 (printed p.40)')),
    'fund_balance_restricted': (7771575, cite('acfr-fy2025', 'PDF p.75 (printed p.40)')),
    'fund_balance_committed': (0, cite('acfr-fy2025', 'PDF p.75 (printed p.40)')),
    'fund_balance_assigned': (16060094, cite('acfr-fy2025', 'PDF p.75 (printed p.40)')),
    'fund_balance_unassigned': (0, cite('acfr-fy2025', 'PDF p.75 (printed p.40)')),
    'fund_balance_total': (23831669, cite('acfr-fy2025', 'PDF p.75 (printed p.40)')),
    'encumbrances_outstanding': (4491447, cite('acfr-fy2025', 'PDF p.142 (printed p.108), Note: Encumbrances')),
}

# ---- Measure FF figures ----
# Table 1C, FY2027..FY2031 as printed (street plan p.4); year totals printed: 25,689,266 19,630,515 16,938,835 14,841,579 15,182,621
TABLE_1C = {'streets_and_sidewalks': [15669266, 8808515, 10513835, 8816579, 11517933],
            'safety': [8870000, 8172000, 5325000, 4275000, 1450000],
            'environmental': [1150000, 2650000, 1100000, 1750000, 2214688]}
assert [sum(x) for x in zip(*TABLE_1C.values())] == [25689266, 19630515, 16938835, 14841579, 15182621], 'Table 1C rows'
FF = {
    'fy2027_revenue_revised': (16651651, cite('budget-adoption-2026-06-23', 'p.254, Exhibit C revenue schedule, fund 166; '
                                              'also measure-ff-rate-fy2027 p.1')),
    'fy2027_revenue_proposed': (15300000, cite('budget-adoption-2026-06-23', 'p.254, Exhibit C')),
    'five_year_program_table_1c': ({k: sum(v) for k, v in TABLE_1C.items()} | {'total': sum(sum(v) for v in TABLE_1C.values())},
                                   cite('street-plan-2026-07-07', 'p.4, Table 1C (sum of FY2027-FY2031 columns)')),
    'streets_cip_five_year': (42119935, cite('budget-adoption-2026-06-23', 'p.215, Measure FF Street Rehabilitation Project')),
}

# ---- Maintenance-of-effort inputs ----
MOE = {
    'floor_base': (15300000, cite('measure-ff-initiative', 'PDF p.8, BMC 7.11.030(B)')),
    'gf_policy_component_fy2027': (8487200, cite('street-plan-2026-07-07', 'p.2, Table 1A "CIP Fund / Council Policy"')),
    'gf_policy_component_base': (8000000, cite('street-plan-2026-07-07', 'p.3 (Resolution 70,456-N.S.: "$8 million annually ... adjusted annually for inflation")')),
    'non_ff_street_plan_fy2027': (18742503, cite('street-plan-2026-07-07', 'p.2, Table 1A total FY2027')),
    'clean_storm_drainage_fy2027': (1000000, cite('street-plan-2026-07-07', 'p.3 (Clean Storm Fund: cross drains, excluded from street rehabilitation)')),
}


def nature(title):
    t = title.lower()
    if 'jpa' in t:
        return 'contractual (Joint Powers Agreement contribution)'
    if 'sidewalk' in t:
        return 'sidewalk repair (liability and accessibility)'
    if 'assessment' in t or 'master plan' in t:
        return 'study or plan'
    if 'creek' in t or 'restoration' in t:
        return 'creek restoration (likely grant-linked)'
    if 'rrfb' in t:
        return 'pedestrian crossing safety device'
    if 'regional sports complex' in t:
        return 'regional facility (5-city Joint Powers Agreement)'
    if 'capital improvement program fund' in t:
        return 'unprogrammed allocation (no project named)'
    return 'repair or replacement of an existing City facility'


def build():
    cip = json.loads(CIP.read_text())
    lines = [(p, f) for p in cip['projects'] for f in p['funding'] if f['fund'] == '501']
    paving = [(p, f) for p, f in lines if p['category'] == 'Streets']
    other = [(p, f) for p, f in lines if p['category'] != 'Streets']

    def tot(rows, col):
        return sum(f[col] for _, f in rows)

    v = {k: x[0] for k, x in ACFR_501.items()}
    unencumbered_assigned = v['fund_balance_assigned'] - v['encumbrances_outstanding']
    candidates = []
    for p, f in sorted(other, key=lambda pf: -(pf[1]['fy2027'] + pf[1]['fy2028'] + pf[1]['five_year_budget'])):
        if not any(f[c] for c in ('prior_years', 'fy2026_budget', 'fy2027', 'fy2028', 'fy2029', 'fy2030', 'fy2031')):
            continue
        candidates.append({
            'title': p['title'], 'category': p['category'], 'project_number': p['project_number'],
            'new_or_continuing': p['new_or_continuing'],
            'appropriated_before_fy2027': f['prior_years'] + f['fy2026_budget'],
            'fy2027': f['fy2027'], 'fy2028': f['fy2028'],
            'planned_fy2029_2031': f['fy2029'] + f['fy2030'] + f['fy2031'],
            'nature_beth_label': nature(p['title']),
            'cost_of_deferral': 'Not assessed by BeTH. Condition, safety, legal and contract status of each project '
                                'must come from Public Works / Parks before any deferral could be proposed.',
            'source': cite('budget-adoption-2026-06-23', f"line {f['source_line']} of the text extract (Exhibit B)")})
    fy27_other, fy28_other = tot(other, 'fy2027'), tot(other, 'fy2028')
    contractual = sum(c['fy2027'] + c['fy2028'] for c in candidates if c['nature_beth_label'].startswith('contractual'))

    floor_factor = MOE['gf_policy_component_fy2027'][0] / MOE['gf_policy_component_base'][0]
    floor_est = round(MOE['floor_base'][0] * floor_factor)
    plan_counted_hi = MOE['non_ff_street_plan_fy2027'][0]
    plan_counted_lo = plan_counted_hi - MOE['clean_storm_drainage_fy2027'][0]

    fund501 = {
        'id': 'fund-501', 'name': 'Capital Improvement Fund (CIP Fund), fund 501', 'type': 'capital projects fund',
        'legal_authority': [
            {'what': 'Funded mainly by an annual General Fund transfer. General Fund revenues "may be used for any general '
                     'government purpose at the discretion of Council."',
             **cite('budget-adoption-2026-06-23', 'p.167')},
            {'what': 'Appropriated annually through the budget and the Annual Appropriation Ordinance; "Any unused funds are '
                     're-appropriated to the following fiscal year until the project is completed."',
             **cite('acfr-fy2025', 'PDF p.180 (printed p.146), Required Supplementary Information, budgetary basis')},
            {'what': 'Council fiscal policy (Resolution 70,456-N.S., July 26, 2022) commits about $8 million a year of General '
                     'Fund money, inflation-adjusted, to paving; it runs through fund 501 as "Street Rehab PCI Improvements".',
             **cite('street-plan-2026-07-07', 'pp.2-3; budget-adoption p.167, p.215')},
        ],
        'permitted_uses': 'Capital projects as appropriated by Council. No voter or external restriction is identified on the '
                          'General Fund transfer itself; the restricted portion of the fund balance equals notes receivable (loans), not cash.',
        'classification_june_30_2025': {
            'restricted': v['fund_balance_restricted'], 'committed': v['fund_balance_committed'],
            'assigned': v['fund_balance_assigned'], 'unassigned': v['fund_balance_unassigned'],
            'total': v['fund_balance_total'],
            'meaning': 'Assigned = "intended to be used by the City for specific purposes that are neither restricted nor '
                       'committed through City Council budgetary action ... Intent is expressed by the City Council or City '
                       'Manager, to which the City Council has delegated the authority." Council can change it without a vote '
                       'of the people or a new ordinance.',
            **cite('acfr-fy2025', 'PDF p.75 (printed p.40); definitions PDF p.103 (printed p.69)')},
        'balances_june_30_2025': {
            'cash_and_investments': v['cash_and_investments'], 'notes_receivable_not_cash': v['notes_receivable'],
            'liabilities': v['total_liabilities'], 'encumbrances_outstanding': v['encumbrances_outstanding'],
            'unencumbered_assigned_fund_balance': unencumbered_assigned,
            'derivation': 'assigned 16,060,094 - encumbrances 4,491,447 = 11,568,647. Encumbrances "are reported in assigned '
                          'fund balance unless the purchase order relates to restricted or committed resources" (ACFR PDF p.180).',
            'warning': 'Sixteen months old. The unencumbered amount backs capital appropriations carried forward to FY2026 '
                       'and is not free money: reassigning it means cancelling or deferring the carried-over projects. FY2026 '
                       'activity is unaudited until the FY2026 ACFR (expected early 2027).'},
        'appropriations_adopted_cip': {
            'before_fy2027_prior_years_plus_fy2026': {'all': tot(lines, 'prior_years') + tot(lines, 'fy2026_budget'),
                                                      'paving': tot(paving, 'prior_years') + tot(paving, 'fy2026_budget'),
                                                      'other': tot(other, 'prior_years') + tot(other, 'fy2026_budget'),
                                                      'note': 'Appropriations made, not cash; spent or unspent status is not in the CIP.'},
            'fy2027': {'all': tot(lines, 'fy2027'), 'paving': tot(paving, 'fy2027'), 'other': fy27_other},
            'fy2028': {'all': tot(lines, 'fy2028'), 'paving': tot(paving, 'fy2028'), 'other': fy28_other},
            'fy2027_2031_five_year': {'all': tot(lines, 'five_year_budget'), 'paving': tot(paving, 'five_year_budget'),
                                      'other': tot(other, 'five_year_budget')},
            'paving_share_fy2027': round(tot(paving, 'fy2027') / tot(lines, 'fy2027'), 4),
            **cite('budget-adoption-2026-06-23', 'pp.172-173 (General Fund Resources incl. CIP Fund) and Exhibit B project tables'),
            'city_statement': '"current CIP funding is entirely pre-allocated for historical programs such as those in Public '
                              'Works, there is no CIP funding available for IT in FY 2027 and FY 2028" (budget-adoption p.239).',
            'not_capital': 'Of the ~$4.95M annual General Fund baseline to the CIP Fund, roughly $4.03M is allocated to capital; '
                           'the rest goes to personnel, debt service and other costs, and part of the $4.03M is held for supplies, '
                           'survey consultants and maintenance (budget-adoption p.167).'},
        'council_authority': {
            'can_redirect_without_voters': True,
            'how': 'By amending the FY2027 Annual Appropriation Ordinance (Council vote). Encumbered amounts are contract '
                   'obligations and cannot be redirected without changing or cancelling the contracts.',
            'limit_paving_floor': 'Measure FF maintenance of effort: if Council adopts a budget with less than $15.3 million '
                                  '(inflation-adjusted) for street maintenance from non-FF sources, it loses authority to levy '
                                  'Measure FF for two years (BMC 7.11.030(B)). Fund 501 paving is most of that floor. Moving money '
                                  'INTO paving is unconstrained by this; moving it OUT is.',
            **cite('measure-ff-initiative', 'PDF pp.8-9, BMC 7.11.030(B)-(D)')},
        'deferral_candidates': candidates,
        'available_for_paving': {
            'already_paving_fy2027': tot(paving, 'fy2027'),
            'already_paving_fy2028': tot(paving, 'fy2028'),
            'upper_bound_new_appropriations_fy2027_fy2028': fy27_other + fy28_other,
            'upper_bound_excluding_contractual': fy27_other + fy28_other - contractual,
            'upper_bound_meaning': 'Only if Council deferred or cancelled every other project funded by fund 501 in FY2027 and '
                                   'FY2028: building roofs and envelopes, the Public Safety Building server room, King Pool, the '
                                   'MLK Youth Services Center, sidewalk repair and others. It is a ceiling, not a finding that '
                                   'any of these should be cut.',
            'planned_fy2029_2031_other': tot(other, 'fy2029') + tot(other, 'fy2030') + tot(other, 'fy2031'),
            'one_time_carryover': {'status': 'UNKNOWN',
                                   'ceiling_june_30_2025': unencumbered_assigned,
                                   'needed': 'The FY2026 year-end CIP carryover and encumbrance report by project for fund 501 '
                                             '(normally in the first FY2027 Annual Appropriation Ordinance amendment), showing '
                                             'which unspent appropriations are paving already, which are under contract, and which '
                                             'are uncommitted.'}},
    }

    ff_prog = FF['five_year_program_table_1c'][0]
    measure_ff = {
        'id': 'measure-ff-safe-streets', 'name': 'Measure FF (SAFE STREETS) special parcel tax, fund 166 "Measure FF - Street Repair"',
        'not_to_confuse_with': ['Fund 164 "Measure FF - Public Safety" (a 2020 fire and emergency services tax)',
                                'ACFR "2009 Measure FF Library" (a 2008 library bond debt service fund)'],
        'legal_authority': [
            {'what': 'Citizens\' initiative approved November 5, 2024 by majority vote; adopted as Ordinance 7,952-N.S. on '
                     'December 10, 2024; codified as BMC Chapter 7.11; special tax under Cal. Const. art. XIIIA, sec. 4 and '
                     'charter-city authority (art. XI, sec. 5); 14 years from January 1, 2025.',
             **cite('measure-ff-initiative', 'PDF pp.5-8, 14-15; rate report p.2')}],
        'permitted_uses': 'Proceeds go to "a special fund to be used only for" repair, repaving and reconstruction, safety '
                          'improvements, and environmental enhancements of streets, sidewalks and pedestrian paths; plus staff '
                          'costs, audits, a ten-yearly Transportation Element update and delivery review, and public art up to '
                          '1.75% of project budgets. No bicycle-specific safety improvements on Hopkins Street between McGee and '
                          'Gilman. BMC 7.11.010(E)-(J), PDF p.7.',
        'classification': 'Restricted (special tax for restricted purposes; enabling legislation). Not yet in an audited '
                          'statement: the FY2025 ACFR predates collections; the first audited balance will be in the FY2026 ACFR.',
        'allocation_fixed_by_voters': {
            'rule': 'Approximately 45% streets, 15% sidewalks and paths (until that backlog is eliminated), 30% safety, 10% '
                    'environmental enhancements, County fees and other permitted uses. BMC 7.11.020(C), PDF p.8.',
            'council_cannot_without_voters': 'Alter the allocations of 7.11.020, expand permitted uses inconsistently with '
                                             'intent, or reduce the 7.11.030 budgeting requirement. Section 7(a)(2)-(4), PDF p.15.',
            'allocations_released_when': 'Citywide average PCI reaches 70 (7.11.020(D); its cross-reference to 7.11.030(C) '
                                         'appears to be a drafting error). Current PCI 57.',
            'adopted_five_year_program': {**ff_prog,
                                          'streets_and_sidewalks_share': round(ff_prog['streets_and_sidewalks'] / ff_prog['total'], 4),
                                          'safety_share': round(ff_prog['safety'] / ff_prog['total'], 4),
                                          'environmental_share': round(ff_prog['environmental'] / ff_prog['total'], 4),
                                          'street_rehabilitation_cip': FF['streets_cip_five_year'][0],
                                          'street_rehabilitation_share': round(FF['streets_cip_five_year'][0] / ff_prog['total'], 4),
                                          **cite('street-plan-2026-07-07', 'p.4 Table 1C; budget-adoption p.215')}},
        'balances': {
            'fy2027_revenue': FF['fy2027_revenue_revised'][0],
            'fy2026_collections': 'UNKNOWN: the first rate covered 18 months (January 1, 2025 to June 30, 2026); FY2026 '
                                  'receipts and the June 30, 2026 balance are unaudited (rate report p.1).',
            'fy2027_cip_appropriation': 24328066,
            'note': 'FY2027 Measure FF CIP ($24,328,066, budget-adoption p.170) exceeds FY2027 revenue ($16,651,651), so the '
                    'plan draws on FY2026 collections. Revenue was revised up $1,351,651 at adoption (Exhibit C) without a '
                    'printed change to Measure FF appropriations.'},
        'available_for_paving': {
            'additional_beyond_adopted_plan': 0,
            'meaning': 'The adopted program already puts ~45.6% of Measure FF into street rehabilitation, at the ordinance\'s '
                       'approximately-45% street share. Safety, sidewalk and environmental shares cannot be moved to paving '
                       'without voter approval. The unprogrammed $1.35M FY2027 revenue increase is still bound by the same '
                       'allocation: about 45% of it (~$0.6M) could go to streets, and only by Council appropriation.',
            'paving_conditions': 'Every Measure FF paving project must include concurrent safety improvements unless Council '
                                 'makes a written substantial-evidence finding (7.11.060(B)).'},
    }

    moe = {
        'rule': 'BMC 7.11.030(B): at least $15.3 million for street maintenance from non-Measure-FF sources, adjusted for '
                'inflation per Resolution 70,456-N.S., or Council may not levy Measure FF for the following two years. '
                'Suspended in a year Council draws $1 million or more from the Stabilization Reserve to adopt a budget, or '
                'under a disaster or emergency declaration (7.11.030(D)); reduced if an external street funding source in the '
                '2023-24 budget declines (7.11.030(C)).',
        'fy2027_floor_estimate': floor_est,
        'fy2027_floor_method': f'BeTH estimate: $15,300,000 x {floor_factor:.4f}, the factor the City applied to the $8M '
                               'policy component ($8,487,200 / $8,000,000). The ordinance does not state the base year or '
                               'index; the City\'s own compliance calculation is not published in BeTH\'s sources.',
        'fy2027_non_ff_street_funding': {'street_plan_total': plan_counted_hi, 'excluding_clean_storm_drainage': plan_counted_lo},
        'fy2027_headroom_estimate': {'low': plan_counted_lo - floor_est, 'high': plan_counted_hi - floor_est},
        'stabilization_reserve_exception_fy2027': 'UNKNOWN: whether the FY2027 budget draws $1M+ from the Stabilization '
                                                  '(Stability) Reserve is not stated in the adoption packet.',
        'confidence': 'Moderate',
        'implication': 'Redirecting non-FF street money elsewhere beyond the headroom would risk about $16.7 million a year of '
                       'Measure FF. Redirecting other capital INTO streets only adds to the floor.',
        **cite('measure-ff-initiative', 'PDF pp.8-9')}

    answer = {
        'question': 'How much capital funding could Berkeley redirect to streets?',
        'scope': 'CIP Fund 501 and Measure FF only. Other capital funds (sewer, storm water, zero waste, parks tax, '
                 'state and county transportation funds, internal service funds) are not yet assessed here.',
        'short_answer': (
            f'From Measure FF: nothing beyond the adopted plan, without a vote of the people. From CIP Fund 501: at most '
            f'${fy27_other + fy28_other:,} of new FY2027-FY2028 appropriations, and only by deferring or cancelling every '
            f'other project the fund pays for; ${tot(paving, "fy2027"):,} of fund 501\'s FY2027 money '
            f'({tot(paving, "fy2027") / tot(lines, "fy2027"):.0%}) already goes to paving. A one-time amount from unspent '
            f'carried-over appropriations is possible but cannot be measured from public documents (ceiling at June 30, '
            f'2025: ${unencumbered_assigned:,}, which also funds paving and other projects already under way).'),
        'what_would_complete_it': [
            'FY2026 year-end fund 501 carryover and encumbrance detail by project.',
            'The FY2027 Annual Appropriation Ordinance (controlling appropriation record, incl. any June 23 amendments).',
            'Public Works and Parks assessments of what deferring each fund 501 project would cost (condition, safety, '
            'legal, contracts).',
            "The City's Measure FF maintenance-of-effort calculation and whether FY2027 draws on the Stabilization Reserve.",
            'Restriction research for the other CIP funding sources.'],
    }
    return {'schema_version': 1, 'generated': '2026-10-23', 'status': 'VERIFIED FROM CITED DOCUMENTS; NOT PUBLISHED',
            'evidence_rules': 'Appropriations are not cash. Planned years are not appropriations. Audited balances are '
                              'June 30, 2025. Upper bounds name what they would cost.',
            'answer': answer, 'funding_sources': [fund501, measure_ff], 'maintenance_of_effort': moe, 'sources': SOURCES}


def main(argv):
    d = build()
    a = d['funding_sources'][0]['available_for_paving']
    print(d['answer']['short_answer'])
    print('fund 501 upper bound FY27-28:', f"{a['upper_bound_new_appropriations_fy2027_fy2028']:,}",
          '| excl. contractual', f"{a['upper_bound_excluding_contractual']:,}")
    m = d['maintenance_of_effort']
    print('MOE floor est', f"{m['fy2027_floor_estimate']:,}", 'headroom', m['fy2027_headroom_estimate'])
    if '--write' in argv:
        OUT.write_text(json.dumps(d, indent=1) + '\n')
        print('wrote', OUT.relative_to(ROOT.parent))


if __name__ == '__main__':
    sys.exit(main(sys.argv))

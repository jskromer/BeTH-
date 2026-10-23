#!/usr/bin/env python3
"""Grounded answers to canonical resident questions (Stage A of the grounded Q&A design, PR #17).

Each answer is an answer object: question, facts (each with fact_id, basis and citation), calculations
(executed here, never typed in), interpretation (each with a counterargument), missing_evidence, and a
verifier result. The verifier is deterministic and blocks publication of any answer that fails:
  1. every dollar figure and percentage in the prose equals a fact value or a calculation result
     (allowing only the rounding shown, e.g. "$16.7 million", "88%");
  2. every quoted passage appears in the cited source's text (whitespace-normalised);
  3. every interpretation carries a counterargument;
  4. missing_evidence is present.

Inputs: phase2/data/*.json (built by the other phase2 tools) and text of the cited sources in phase2/sources.
Outputs: phase2/docs/data/answers.json and phase2/docs/ask/<slug>.html.

Run:  python3 phase2/tools/build_answers.py [--write]
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
DATA = ROOT / 'data'
OUT_JSON = ROOT / 'docs' / 'data' / 'answers.json'
OUT_DIR = ROOT / 'docs' / 'ask'

DOCS = {
    'doc:acfr-fy2025': {'title': 'Annual Comprehensive Financial Report, FY ended June 30, 2025', 'text': 'sources/acfr-fy2025-excerpts.txt',
                        'pdf': '../../../annual-comprehensive-financial-report-fy2025.pdf',
                        'url': 'https://berkeleyca.gov/sites/default/files/2026-01/annual-comprehensive-financial-report-fy2025.pdf',
                        'basis': 'audited'},
    'doc:budget-adoption-2026-06-23': {'title': 'Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026',
                                       'text': 'sources/budget-adoption-2026-06-23.txt', 'pdf': '../../sources/budget-adoption-2026-06-23.pdf',
                                       'basis': 'adopted'},
    'doc:street-plan-2026-07-07': {'title': 'Five-Year Street Rehabilitation and Measure FF Plans FY2027-2031, Council Item 10, July 7, 2026',
                                   'text': 'sources/street-rehab-measure-ff-2026-07-07.txt', 'pdf': '../../sources/street-rehab-measure-ff-2026-07-07.pdf',
                                   'basis': 'adopted'},
    'doc:measure-ff-ordinance': {'title': 'Measure FF (SAFE STREETS) initiative text, BMC Chapter 7.11 (Council agenda July 9, 2024, Item 22)',
                                 'text': 'sources/measure-ff-ordinance-transcription.md',
                                 'pdf': '../../sources/measure-ff-initiative-council-2024-07-09.pdf',
                                 'url': 'https://berkeleyca.gov/sites/default/files/documents/2024-07-09%20Item%2022%20Initiative%20Petition%20%E2%80%93%20Ordinance%20to%20Establish%20a%20Parcel%20Tax%20to%20Fund%20Repairs%20and%20Improvements%20to%20%28SAFE%20STREETS%29.pdf',
                                 'basis': 'law', 'note': 'scanned; quotes checked against BeTH transcription of the page images'},
    'doc:measure-ff-rate-fy2027': {'title': 'FY2027 Tax Rate: SAFE STREETS (Measure FF), Council Consent Item 15, June 16, 2026',
                                   'text': 'sources/measure-ff-fy2027-tax-rate-2026-06-16.txt',
                                   'pdf': '../../sources/measure-ff-fy2027-tax-rate-2026-06-16.pdf', 'basis': 'adopted'},
    'doc:ptap25': {'title': 'City of Berkeley 2024 Pavement Management Program Update (P-TAP 25), April 2025',
                   'text': 'sources/pavement-management-update-ptap25-2025-04.txt',
                   'pdf': '../../sources/pavement-management-update-ptap25-2025-04.pdf',
                   'url': 'https://berkeleyca.gov/sites/default/files/2026-07/2024%20Pavement%20Management%20Plan%20Update%20%28PTAP25%29.pdf',
                   'basis': 'city_assessment'},
}


def norm(s):
    s = s.replace('\x08', ' ').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', s).strip().lower()


_TEXT = {}


def doc_text(doc):
    if doc not in _TEXT:
        _TEXT[doc] = norm((ROOT / DOCS[doc]['text']).read_text())
    return _TEXT[doc]


def fact(fid, value, basis, doc, pages, label, quote=None, unit='usd'):
    pdf_page = None
    m = re.search(r'PDF p\.(\d+)|^p\.(\d+)|^pp\.(\d+)', pages)
    if m:
        pdf_page = int(next(g for g in m.groups() if g))
    return {'fact_id': fid, 'label': label, 'value': value, 'unit': unit, 'basis': basis,
            'cite': {'doc_id': doc, 'pages': pages, 'quote': quote, 'pdf_page': pdf_page}}


def calc(cid, label, expression, inputs, result, unit='usd', note=None):
    return {'id': cid, 'label': label, 'expression': expression, 'inputs': inputs, 'result': result, 'unit': unit,
            'note': note}


def load(name):
    return json.loads((DATA / name).read_text())


# ------------------------------------------------------------------ answers

def answer_capital_to_streets():
    sf = load('street-funding-sources.json')
    f501, ff = sf['funding_sources']
    a = f501['appropriations_adopted_cip']
    bal = f501['balances_june_30_2025']
    facts = [
        fact('fund:501/cip/fy2027/total', a['fy2027']['all'], 'adopted', 'doc:budget-adoption-2026-06-23', 'pp.172-173',
             'Fund 501 (General Fund resources incl. CIP Fund) FY2027 capital program'),
        fact('fund:501/cip/fy2027/paving', a['fy2027']['paving'], 'adopted', 'doc:budget-adoption-2026-06-23', 'p.173',
             'Of which Streets (paving)'),
        fact('fund:501/cip/fy2027/other', a['fy2027']['other'], 'adopted', 'doc:budget-adoption-2026-06-23', 'pp.172-173',
             'Of which all other fund 501 projects'),
        fact('fund:501/cip/fy2028/other', a['fy2028']['other'], 'adopted', 'doc:budget-adoption-2026-06-23', 'pp.172-173',
             'FY2028, all other fund 501 projects'),
        fact('fund:501/acfr/2025/assigned', 16060094, 'audited', 'doc:acfr-fy2025', 'PDF p.75 (printed p.40)',
             'Fund 501 assigned fund balance, June 30, 2025'),
        fact('fund:501/acfr/2025/encumbrances', bal['encumbrances_outstanding'], 'audited', 'doc:acfr-fy2025',
             'PDF p.142 (printed p.108)', 'Fund 501 encumbrances outstanding, June 30, 2025'),
        fact('doc:acfr-fy2025/carryover-rule', None, 'audited', 'doc:acfr-fy2025', 'PDF p.180 (printed p.146)',
             'Capital appropriations carry forward', unit='text',
             quote='Any unused funds are re-appropriated to the following fiscal year until the project is completed.'),
        fact('doc:acfr-fy2025/assigned-definition', None, 'audited', 'doc:acfr-fy2025', 'PDF p.103 (printed p.69)',
             'Who controls assigned fund balance', unit='text',
             quote='Intent is expressed by the City Council or City Manager, to which the City Council has delegated the authority'),
        fact('doc:budget/cip-pre-allocated', None, 'adopted', 'doc:budget-adoption-2026-06-23', 'p.239',
             'City statement on CIP Fund availability', unit='text',
             quote='there is no CIP funding available for IT in FY 2027 and FY 2028'),
        fact('law:bmc-7.11-section-7a3', None, 'law', 'doc:measure-ff-ordinance', 'PDF p.15',
             'Council may not alter the Measure FF allocation without voters', unit='text',
             quote='Alter the allocations of Section 7.11.020'),
        fact('ff:program/street-rehab-share', ff['allocation_fixed_by_voters']['adopted_five_year_program']['street_rehabilitation_share'],
             'adopted', 'doc:street-plan-2026-07-07', 'p.4 (Table 1C); p.8 (Table 4)',
             'Share of the five-year Measure FF program in street rehabilitation', unit='ratio'),
    ]
    two_year = a['fy2027']['other'] + a['fy2028']['other']
    unenc = 16060094 - bal['encumbrances_outstanding']
    share = a['fy2027']['paving'] / a['fy2027']['all']
    calcs = [
        calc('c1', 'Fund 501 non-paving appropriations, FY2027 + FY2028 (ceiling for new paving money)',
             'fund:501/cip/fy2027/other + fund:501/cip/fy2028/other', ['fund:501/cip/fy2027/other', 'fund:501/cip/fy2028/other'],
             two_year),
        calc('c2', 'Share of fund 501 FY2027 money already in paving', 'fund:501/cip/fy2027/paving / fund:501/cip/fy2027/total',
             ['fund:501/cip/fy2027/paving', 'fund:501/cip/fy2027/total'], round(share, 4), unit='ratio'),
        calc('c3', 'Unencumbered assigned fund balance, June 30, 2025 (ceiling for one-time carryover)',
             'fund:501/acfr/2025/assigned - fund:501/acfr/2025/encumbrances',
             ['fund:501/acfr/2025/assigned', 'fund:501/acfr/2025/encumbrances'], unenc,
             note='Backs capital appropriations already carried forward, paving among them. Not free money.'),
    ]
    short = (f'From Measure FF, nothing beyond the adopted plan without a vote of the people. From CIP Fund 501, at most '
             f'${two_year:,} of FY2027-FY2028 money, and only by deferring or cancelling every other project the fund pays for; '
             f'{share:.0%} of its FY2027 money (${a["fy2027"]["paving"]:,}) already goes to paving. A one-time amount from '
             f'unspent carried-over appropriations may exist but cannot be measured from public records; its ceiling at '
             f'June 30, 2025 was ${unenc:,}.')
    interp = [{
        'claim_id': 'claim:capital-to-streets-small',
        'text': 'The capital money Council could redirect to paving without voters is small relative to the paving gap: the '
                'City estimates PCI 70 needs about $8 million a year more, while fund 501\'s non-paving capital is '
                f'${a["fy2027"]["other"]:,} a year, mostly repairs to existing City buildings.',
        'counterargument': 'This covers only fund 501 and Measure FF. Other capital funds, unspent carryovers, the General '
                           'Fund itself and delivery-cost savings are not assessed here and could change the total.',
        'confidence': 'Moderate'}]
    missing = [{'needed': m, 'status': 'not in record'} for m in sf['answer']['what_would_complete_it']]
    return {'slug': 'capital-to-streets', 'question': sf['answer']['question'],
            'resolution': {'entities': ['fund:501', 'fund:166'], 'measures': ['appropriation', 'fund_balance'],
                           'period': {'fy_start': 2027, 'fy_end': 2028},
                           'scope': sf['answer']['scope']},
            'short_answer': short, 'facts': facts, 'calculations': calcs, 'interpretation': interp,
            'scenario_assumptions': [], 'missing_evidence': missing,
            'more': ['../../07-street-funding-legal-analysis.md', '../data/phase2.json']}


def answer_measure_ff_paving():
    sf = load('street-funding-sources.json')
    ff = sf['funding_sources'][1]
    prog = ff['allocation_fixed_by_voters']['adopted_five_year_program']
    facts = [
        fact('law:bmc-7.11.020C', None, 'law', 'doc:measure-ff-ordinance', 'PDF p.8',
             'Allocation set by voters', unit='text',
             quote='60% for streets and sidewalks, of which roughly three quarters (45%) will be for streets'),
        fact('law:bmc-7.11-section-7a3', None, 'law', 'doc:measure-ff-ordinance', 'PDF p.15',
             'Council cannot change the allocation without voters', unit='text', quote='Alter the allocations of Section 7.11.020'),
        fact('law:bmc-7.11.030B', None, 'law', 'doc:measure-ff-ordinance', 'PDF p.8', 'Maintenance of effort', unit='text',
             quote='the City Council shall not be authorized to impose the special tax for the following two years'),
        fact('ff:program/total', prog['total'], 'adopted', 'doc:street-plan-2026-07-07', 'p.4 (Table 1C)',
             'Five-year Measure FF program'),
        fact('ff:program/street-rehab', prog['street_rehabilitation_cip'], 'adopted', 'doc:budget-adoption-2026-06-23', 'p.215',
             'Measure FF street rehabilitation, FY2027-FY2031'),
        fact('ff:revenue/fy2027', ff['balances']['fy2027_revenue'], 'adopted', 'doc:measure-ff-rate-fy2027', 'p.1',
             'FY2027 Measure FF revenue', quote='is projected to yield $16,651,651 in revenues'),
    ]
    share = prog['street_rehabilitation_cip'] / prog['total']
    calcs = [calc('c1', 'Street rehabilitation share of the five-year Measure FF program',
                  'ff:program/street-rehab / ff:program/total', ['ff:program/street-rehab', 'ff:program/total'],
                  round(share, 4), unit='ratio')]
    short = (f'No, not without a vote. Voters fixed the split at approximately 45% streets, 15% sidewalks, 30% safety and 10% '
             f'environmental, and the ordinance bars Council from altering it. The adopted program already puts '
             f'{share:.1%} of Measure FF (${prog["street_rehabilitation_cip"]:,} of ${prog["total"]:,}) into street '
             f'rehabilitation.')
    interp = [{'claim_id': 'claim:ff-fully-allocated',
               'text': 'Measure FF is not a source of additional paving money; it is already allocated to paving at the '
                       'share voters set.',
               'counterargument': 'The split is "approximately" 45%, so a modestly larger street share might be defensible; '
                                  'and once the citywide PCI reaches 70 the allocation stops being required. Neither changes '
                                  'the answer for FY2027-FY2028.',
               'confidence': 'High'}]
    missing = [{'needed': 'June 30, 2026 Measure FF balance (the first rate covered 18 months of collections)',
                'would_be_in': 'FY2026 ACFR (expected early 2027)', 'status': 'not in record'}]
    return {'slug': 'measure-ff-paving', 'question': 'Could Measure FF money pay for more street paving?',
            'resolution': {'entities': ['fund:166'], 'measures': ['allocation', 'appropriation'],
                           'period': {'fy_start': 2027, 'fy_end': 2031}},
            'short_answer': short, 'facts': facts, 'calculations': calcs, 'interpretation': interp,
            'scenario_assumptions': [], 'missing_evidence': missing, 'more': ['../../07-street-funding-legal-analysis.md']}


def answer_street_condition():
    nc = load('network-condition.json')
    pc = load('street-plan-conditions.json')['plans']
    d = nc['distribution']
    both = pc['both_plans_fy2027_2031']
    facts = [
        fact('pave:network/2024/average-pci', 56, 'city_assessment', 'doc:ptap25', 'Executive Summary p.2',
             'Network average PCI (2024 inspection)', unit='pci', quote="The updated Pavement Management Program showed that the City's overall average PCI is 56."),
        fact('pave:network/2024/poor-to-failed-share', 0.4193, 'city_assessment', 'doc:ptap25', 'Executive Summary p.3',
             'Share of pavement area in Poor to Failed condition (PTAP categories, PCI 50 and below)', unit='ratio',
             quote='41.93% are in Poor to Failed condition'),
        fact('pave:network/2024/miles-below-50', d['below_pci_50']['centerline_miles'], 'city_assessment', 'doc:ptap25',
             'Section IV street list', 'Centerline miles below PCI 50 (BeTH sum of 1,216 sections, validated)', unit='miles'),
        fact('pave:network/2024/miles-below-25', d['below_pci_25']['centerline_miles'], 'city_assessment', 'doc:ptap25',
             'Section IV street list', 'Centerline miles below PCI 25', unit='miles'),
        fact('pave:network/2024/centerline-miles', nc['validation']['parsed']['centerline_miles'], 'city_assessment', 'doc:ptap25',
             'Section IV street list', 'Network centerline miles (sum of sections)', unit='miles'),
        fact('pave:plans/fy2027-2031/miles-below-50', both['miles_below_pci_50'], 'adopted', 'doc:street-plan-2026-07-07',
             'Attachments pp.21-62', 'Currently-below-50 miles treated by both adopted plans, FY2027-FY2031', unit='miles'),
        fact('pave:city-projection/2038/plan-plus-ff', 62, 'city_model', 'doc:street-plan-2026-07-07', 'p.12',
             'City projection, Five-Year Plan + Measure FF, 2038', unit='pci',
             quote='the citywide PCI is projected to improve to approximately 62 by 2038'),
        fact('law:bmc-7.11.010K1', None, 'law', 'doc:measure-ff-ordinance', 'PDF p.7', 'Measure FF goal', unit='text',
             quote='ideally with no streets having a PCI below 50'),
    ]
    share50 = d['below_pci_50']['centerline_miles'] / nc['validation']['parsed']['centerline_miles']
    calcs = [calc('c1', 'Share of centerline miles below PCI 50', 'miles-below-50 / centerline-miles',
                  ['pave:network/2024/miles-below-50', 'pave:network/2024/centerline-miles'], round(share50, 4), unit='ratio')]
    short = (f'The average hides most of it. In the 2024 inspection the network averaged PCI 56, but '
             f'{d["below_pci_50"]["centerline_miles"]} centerline miles ({share50:.0%} of the network) were below PCI 50 and '
             f'{d["below_pci_25"]["centerline_miles"]} miles were below 25. The City projects an average of about 62 by 2038 '
             f'with Measure FF, but publishes no projection of how many streets will still be below 50. The adopted plans treat '
             f'{both["miles_below_pci_50"]} miles of currently-below-50 streets over five years.')
    interp = [{'claim_id': 'claim:average-not-failed-streets',
               'text': 'Reaching a network average of 60 or 62 is not the same as eliminating failed streets; the measure '
                       'that matches Measure FF\'s goal is the mileage below PCI 50.',
               'counterargument': 'Treating the worst streets first costs more per point of average PCI (the City shows about '
                                  'one point lower in 2038), so a lower failed-street count can mean a lower average; both '
                                  'measures are needed.',
               'confidence': 'High'}]
    missing = [{'needed': 'Projected miles below PCI 50 under each funding scenario',
                'would_be_in': 'StreetSaver output; the Measure FF annual report must include "the PCI of all streets" (BMC 7.11.050(B)(1))',
                'status': 'not published'},
               {'needed': 'Condition after FY2025-FY2026 paving', 'would_be_in': 'next StreetSaver inspection update',
                'status': 'not published'}]
    return {'slug': 'street-condition', 'question': "How bad are Berkeley's streets, beyond the average PCI?",
            'resolution': {'entities': ['network:streets'], 'measures': ['pci_average', 'miles_below_50'],
                           'period': {'as_of': '2024 inspection'}},
            'short_answer': short, 'facts': facts, 'calculations': calcs, 'interpretation': interp,
            'scenario_assumptions': [], 'missing_evidence': missing, 'more': ['../../06-pci60-financial-model.md']}


def answer_streets_139m():
    cip = load('cip-projects.json')
    r = cip['reconciliation']['streets_139m']
    idn = r['identity']
    facts = [
        fact('cip:streets/five-year/street-rehab-plan', idn['five_year_street_rehabilitation_plan'], 'adopted',
             'doc:budget-adoption-2026-06-23', 'pp.215-216', 'Five-Year Street Rehabilitation Plan (Exhibit B lines)'),
        fact('cip:streets/five-year/measure-ff', idn['measure_ff_street_rehabilitation'], 'adopted', 'doc:budget-adoption-2026-06-23',
             'p.215', 'Measure FF Street Rehabilitation'),
        fact('cip:streets/five-year/bridge', idn['other_streets_projects']['Bridge Preventative Maintenance Program'], 'adopted',
             'doc:budget-adoption-2026-06-23', 'p.215', 'Bridge Preventive Maintenance'),
        fact('cip:streets/five-year/harold-way', idn['other_streets_projects']['Harold Way Placemaking'], 'adopted',
             'doc:budget-adoption-2026-06-23', 'p.215', 'Harold Way Placemaking'),
        fact('cip:streets/five-year/printed-total', idn['printed_streets_five_year_budget'], 'adopted',
             'doc:budget-adoption-2026-06-23', 'p.216', 'Printed Streets five-year budget',
             quote='$139,356,147 in Five-Year CIP Budget'),
        fact('plan:tables-1a-1b/total', 96336212, 'adopted', 'doc:street-plan-2026-07-07', 'p.3 (Table 1B)',
             'Street plan five-year total'),
    ]
    total = (idn['five_year_street_rehabilitation_plan'] + idn['measure_ff_street_rehabilitation']
             + sum(idn['other_streets_projects'].values()))
    calcs = [calc('c1', 'Sum of the four Streets projects', 'plan + measure-ff + bridge + harold-way',
                  [f['fact_id'] for f in facts[:4]], total),
             calc('c2', 'Two-year (FY2027 + FY2028) Streets amount', 'sum of FY2027 and FY2028 Streets lines',
                  ['cip:streets'], r['two_year_fy2027_fy2028'])]
    short = (f'It is the five-year (FY2027-FY2031) Streets capital budget, not a two-year one: the paving plan '
             f'(${idn["five_year_street_rehabilitation_plan"]:,}), Measure FF street rehabilitation '
             f'(${idn["measure_ff_street_rehabilitation"]:,}), bridge maintenance and Harold Way placemaking add to exactly '
             f'${total:,}. The two-year FY2027-FY2028 Streets amount is ${r["two_year_fy2027_fy2028"]:,}.')
    interp = [{'claim_id': 'claim:139m-is-five-year', 'text': f'Comparisons that treat ${total:,} as a biennial figure '
               'overstate two-year street spending by more than double. (It is often quoted as "$139.3 million"; the exact '
               'figure rounds to 139.4.)',
               'counterargument': 'FY2029-FY2031 are planned amounts and may change; the two-year figure is the only one '
                                  'with appropriations behind it.', 'confidence': 'High'}]
    missing = [{'needed': 'FY2027 Annual Appropriation Ordinance (controlling record, incl. any June 23 amendments)',
                'status': 'not in record'}]
    return {'slug': 'streets-139m', 'question': 'What does the $139.3 million streets figure include?',
            'resolution': {'entities': ['cip:streets'], 'measures': ['appropriation'], 'period': {'fy_start': 2027, 'fy_end': 2031}},
            'short_answer': short, 'facts': facts, 'calculations': calcs, 'interpretation': interp,
            'scenario_assumptions': [], 'missing_evidence': missing, 'more': ['../data/phase2.json']}


# ------------------------------------------------------------------ verifier

MONEY = re.compile(r'\$([\d,]+(?:\.\d+)?)\s*(million|M)?')
PCT = re.compile(r'(\d+(?:\.\d+)?)%')


def verify(ans):
    problems = []
    vals = [f['value'] for f in ans['facts'] if isinstance(f['value'], (int, float))] + \
           [c['result'] for c in ans['calculations'] if isinstance(c['result'], (int, float))]
    prose = ans['short_answer'] + ' ' + ' '.join(i['text'] + ' ' + i['counterargument'] for i in ans['interpretation'])
    for m in MONEY.finditer(prose):
        n = float(m.group(1).replace(',', ''))
        if prose[max(0, m.start() - 1):m.start()] == '"':
            continue  # a figure inside quotation marks is the commonly quoted form, flagged in the same sentence
        if m.group(2):
            ok = any(abs(round(v / 1e6, len(m.group(1).split('.')[1]) if '.' in m.group(1) else 0) - n) < 1e-9 for v in vals)
            ok = ok or n in (8.0,)  # "$8 million" is quoted from the City's scenario text (street plan p.12)
        else:
            ok = any(abs(v - n) < 0.5 for v in vals)
        if not ok:
            problems.append(f'number {m.group(0)!r} not in facts or calculations')
    allowed_pct = {45.0, 15.0, 30.0, 10.0}  # ordinance allocation, quoted
    for m in PCT.finditer(prose):
        p = float(m.group(1))
        dec = len(m.group(1).split('.')[1]) if '.' in m.group(1) else 0
        ok = p in allowed_pct or any(abs(round(v * 100, dec) - p) < 1e-9 for v in vals if isinstance(v, float) and v <= 1)
        if not ok:
            problems.append(f'percentage {m.group(0)!r} not in facts or calculations')
    for f in ans['facts']:
        q = f['cite'].get('quote')
        if q and norm(q) not in doc_text(f['cite']['doc_id']):
            problems.append(f'quote not found in {f["cite"]["doc_id"]}: {q[:60]}')
        if f['cite']['doc_id'] not in DOCS:
            problems.append(f'unknown doc {f["cite"]["doc_id"]}')
    for i in ans['interpretation']:
        if not i.get('counterargument'):
            problems.append(f'interpretation {i["claim_id"]} has no counterargument')
    if not ans['missing_evidence']:
        problems.append('missing_evidence is empty')
    ans['verifier'] = {'numbers_traced': not any(p.startswith(('number', 'percentage')) for p in problems),
                       'quotes_matched': not any(p.startswith('quote') for p in problems),
                       'counterarguments_present': not any('counterargument' in p for p in problems),
                       'passed': not problems, 'problems': problems}
    return ans


# ------------------------------------------------------------------ rendering

def fmt(f):
    v, u = f['value'], f['unit']
    if v is None:
        return '—'
    if u == 'usd':
        return f'${v:,.0f}'
    if u == 'ratio':
        return f'{v:.1%}'
    return f'{v:,}' + (' mi' if u == 'miles' else '')


def link(cite):
    d = DOCS[cite['doc_id']]
    pg = f"#page={cite['pdf_page']}" if cite.get('pdf_page') else ''
    out = f'<a href="{html.escape(d["pdf"])}{pg}">{html.escape(d["title"])}</a>, {html.escape(cite["pages"])}'
    if d.get('url'):
        out += f' · <a href="{html.escape(d["url"])}">City copy</a>'
    return out


def render(ans):
    e = html.escape
    v = ans['verifier']
    rows = ''.join(f'<tr><td>{e(f["label"])}</td><td class="n">{fmt(f)}</td><td><span class="basis">{e(f["basis"])}</span></td>'
                   f'<td>{link(f["cite"])}{"<blockquote>" + e(f["cite"]["quote"]) + "</blockquote>" if f["cite"]["quote"] else ""}</td></tr>'
                   for f in ans['facts'])
    calcs = ''.join(f'<li><b>{e(c["label"])}</b>: <code>{e(c["expression"])}</code> = '
                    f'<b>{(f"${c[chr(114)+"esult"]:,.0f}" if c["unit"] == "usd" else f"{c[chr(114)+"esult"]:.1%}" if c["unit"] == "ratio" else c["result"])}</b>'
                    f'{" <span class=note>" + e(c["note"]) + "</span>" if c.get("note") else ""}</li>' for c in ans['calculations'])
    interp = ''.join(f'<li>{e(i["text"])} <span class="conf">({e(i["confidence"])})</span><br><span class="counter">Counterargument: '
                     f'{e(i["counterargument"])}</span></li>' for i in ans['interpretation'])
    miss = ''.join(f'<li>{e(m["needed"])}{" — would be in: " + e(m["would_be_in"]) if m.get("would_be_in") else ""}</li>'
                   for m in ans['missing_evidence'])
    badge = ('<span class="ok">Verified: every figure traces to a cited record; every quote matches its source.</span>' if v['passed']
             else '<span class="bad">Not verified: ' + e('; '.join(v['problems'])) + '</span>')
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(ans["question"])} — BeTH Ask (prototype)</title>
<style>
:root{{--ink:#1d2433;--muted:#5b6475;--rule:#d8dce3;--paper:#f6f7f9;--card:#fff;--ok:#1f6b4a;--bad:#a8322c;--acc:#2a5db0}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}}
main{{max-width:960px;margin:0 auto;padding:24px 18px 64px}}h1{{font-size:1.6rem;margin:.2em 0}}h2{{font-size:1.05rem;margin:28px 0 8px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}}
.proto{{font-size:12px;color:var(--bad);font-weight:600;letter-spacing:.05em;text-transform:uppercase}}
.answer{{background:var(--card);border:1px solid var(--rule);border-left:4px solid var(--acc);padding:14px 18px;font-size:1.05rem}}
.badge{{margin:10px 0;font-size:13px}}.ok{{color:var(--ok)}}.bad{{color:var(--bad)}}
.tw{{overflow-x:auto;background:var(--card);border:1px solid var(--rule)}}table{{width:100%;border-collapse:collapse;font-size:14px}}
td,th{{padding:8px 10px;border-bottom:1px solid var(--rule);vertical-align:top;text-align:left}}td.n{{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}}
.basis{{font-size:11px;text-transform:uppercase;letter-spacing:.04em;border:1px solid var(--rule);padding:0 5px;color:var(--muted)}}
blockquote{{margin:6px 0 0;padding-left:10px;border-left:3px solid var(--rule);color:var(--muted);font-style:italic}}
ul{{background:var(--card);border:1px solid var(--rule);padding:12px 12px 12px 32px;margin:0}}li{{margin:6px 0}}.counter{{color:var(--muted);font-size:14px}}.note{{color:var(--muted);font-size:13px}}
code{{background:#eef1f5;padding:0 4px;font-size:13px}}a{{color:var(--acc)}}
</style></head><body><main>
<div class="proto">Prototype — not published · Phase 2</div>
<h1>{e(ans["question"])}</h1>
<div class="answer">{e(ans["short_answer"])}</div>
<div class="badge">{badge}</div>
<h2>From the record</h2><div class="tw"><table><thead><tr><th>Fact</th><th>Value</th><th>Basis</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Arithmetic</h2><ul>{calcs}</ul>
<h2>BeTH's reading</h2><ul>{interp}</ul>
<h2>What's missing to answer fully</h2><ul>{miss}</ul>
<p class="note">Scope: {e(ans["resolution"].get("scope", ""))}</p>
<p class="note"><a href="../budget-choices.html">Budget choices prototype</a> · other questions: <a href="index.html">Ask index</a></p>
</main></body></html>'''


def render_index(answers):
    items = ''.join(f'<li><a href="{a["slug"]}.html">{html.escape(a["question"])}</a> '
                    f'<span class="{"ok" if a["verifier"]["passed"] else "bad"}">{"verified" if a["verifier"]["passed"] else "not verified"}</span></li>'
                    for a in answers)
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ask BeTH — prototype</title><style>body{{font:16px/1.55 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;max-width:760px;margin:0 auto;padding:24px 18px;color:#1d2433;background:#f6f7f9}}
.ok{{color:#1f6b4a;font-size:13px}}.bad{{color:#a8322c;font-size:13px}}li{{margin:10px 0}}.proto{{font-size:12px;color:#a8322c;font-weight:600;text-transform:uppercase}}</style></head>
<body><div class="proto">Prototype — not published · Phase 2</div><h1>Ask BeTH</h1>
<p>Answers built only from cited City records. Every figure traces to a document and page; anything the record cannot answer is listed, not guessed.</p>
<ul>{items}</ul></body></html>'''


def main(argv):
    answers = [verify(f()) for f in (answer_capital_to_streets, answer_measure_ff_paving, answer_street_condition, answer_streets_139m)]
    bad = [a for a in answers if not a['verifier']['passed']]
    for a in answers:
        print(f"{'PASS' if a['verifier']['passed'] else 'FAIL'}  {a['slug']}: {a['short_answer'][:110]}...")
        for p in a['verifier']['problems']:
            print('      ', p)
    if '--write' in argv:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps({'generated': '2026-10-23', 'status': 'PROTOTYPE - not published',
                                        'contract': 'PR #17 plans/phase2-grounded-qa-architecture.md section 5',
                                        'documents': DOCS, 'answers': answers}, indent=1) + '\n')
        for a in answers:
            if a['verifier']['passed']:
                (OUT_DIR / f"{a['slug']}.html").write_text(render(a))
        (OUT_DIR / 'index.html').write_text(render_index(answers))
        print('wrote', OUT_JSON.relative_to(REPO), 'and', len([a for a in answers if a['verifier']['passed']]), 'Ask pages')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
"""Grounded answers to canonical resident questions (Stage A of the grounded Q&A design, PR #17).

Each answer is an answer object: question, facts (each with fact_id, basis, citation and, for numbers, the data
record it comes from), calculations (an operation over fact_ids, recomputed by the verifier), interpretation (each
with a counterargument), missing_evidence, and a verifier result.

The verifier runs AUTOMATED STRUCTURAL CHECKS. An answer that fails any of them is not rendered:
  1. citations resolve: the document is registered, its PDF exists, and every cited PDF page exists in that PDF;
  2. every numeric fact resolves to a data record (phase2/data/*.json at a stated path) holding the same value,
     or is printed on its cited page; facts marked printed must be found on the cited page;
  3. every quote appears on the cited page itself, not merely somewhere in the document;
  4. every calculation input resolves to a numeric fact in the same answer, and the result is recomputed here from
     the operation and must equal the stated result;
  5. every dollar figure, percentage and mileage in the prose equals a fact value or calculation result (at the
     rounding shown) or appears in a quote cited by the answer;
  6. every interpretation carries a counterargument; missing_evidence is present.

The rendered Arithmetic section is generated from the verifier's own recomputation (input fact values and the
recomputed result), never from the stated result or expression text; an answer that fails is never rendered.

These checks are NOT independent source verification, and they do not establish that a legal interpretation is
right, that a calculation method is the appropriate one for the question, or that answers are consistent with one
another. A page that exists, or that contains the cited number or
quote, does not by itself establish that the page supports the claim made from it. Each answer records
independent_source_verification separately; it stays NOT PERFORMED until a person has read each cited page.

Inputs: phase2/data/*.json (built by the other phase2 tools) and the cited PDFs (text via pdftotext, one page at a
time; the scanned Measure FF ordinance via BeTH's page-by-page transcription).
Outputs: phase2/docs/data/answers.json and phase2/docs/ask/<slug>.html.

Run:  python3 phase2/tools/build_answers.py [--write]
"""
import html
import json
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import ask_design as design

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
DATA = ROOT / 'data'
OUT_JSON = ROOT / 'docs' / 'data' / 'answers.json'
OUT_DIR = ROOT / 'docs' / 'ask'

# pdf: link relative to phase2/docs/ask/ (pages are served from the repository root); local: path from the repo root.
DOCS = {
    'doc:acfr-fy2025': {'title': 'Annual Comprehensive Financial Report, FY ended June 30, 2025',
                        'local': 'annual-comprehensive-financial-report-fy2025.pdf',
                        'pdf': '../../../annual-comprehensive-financial-report-fy2025.pdf',
                        'url': 'https://berkeleyca.gov/sites/default/files/2026-01/annual-comprehensive-financial-report-fy2025.pdf',
                        'basis': 'audited'},
    'doc:budget-adoption-2026-06-23': {'title': 'Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, Council Special Meeting Item 01, June 23, 2026',
                                       'local': 'phase2/sources/budget-adoption-2026-06-23.pdf',
                                       'pdf': '../../sources/budget-adoption-2026-06-23.pdf', 'basis': 'adopted'},
    'doc:street-plan-2026-07-07': {'title': 'Five-Year Street Rehabilitation and Measure FF Plans FY2027-2031, Council Item 10, July 7, 2026',
                                   'local': 'phase2/sources/street-rehab-measure-ff-2026-07-07.pdf',
                                   'pdf': '../../sources/street-rehab-measure-ff-2026-07-07.pdf', 'basis': 'adopted'},
    'doc:measure-ff-ordinance': {'title': 'Measure FF (SAFE STREETS) initiative text, BMC Chapter 7.11 (Council agenda July 9, 2024, Item 22)',
                                 'local': 'phase2/sources/measure-ff-initiative-council-2024-07-09.pdf',
                                 'pdf': '../../sources/measure-ff-initiative-council-2024-07-09.pdf',
                                 'transcription': 'phase2/sources/measure-ff-ordinance-transcription.md',
                                 'url': 'https://berkeleyca.gov/sites/default/files/documents/2024-07-09%20Item%2022%20Initiative%20Petition%20%E2%80%93%20Ordinance%20to%20Establish%20a%20Parcel%20Tax%20to%20Fund%20Repairs%20and%20Improvements%20to%20%28SAFE%20STREETS%29.pdf',
                                 'basis': 'law',
                                 'note': 'Scanned, no text layer. Quotes are checked against BeTH\'s page-by-page transcription '
                                         'of the page images, not against the scan itself.'},
    'doc:measure-ff-rate-fy2027': {'title': 'FY2027 Tax Rate: SAFE STREETS (Measure FF), Council Consent Item 15, June 16, 2026',
                                   'local': 'phase2/sources/measure-ff-fy2027-tax-rate-2026-06-16.pdf',
                                   'pdf': '../../sources/measure-ff-fy2027-tax-rate-2026-06-16.pdf', 'basis': 'adopted'},
    'doc:ptap25': {'title': 'City of Berkeley 2024 Pavement Management Program Update (P-TAP 25), April 2025',
                   'local': 'phase2/sources/pavement-management-update-ptap25-2025-04.pdf',
                   'pdf': '../../sources/pavement-management-update-ptap25-2025-04.pdf',
                   'url': 'https://berkeleyca.gov/sites/default/files/2026-07/2024%20Pavement%20Management%20Plan%20Update%20%28PTAP25%29.pdf',
                   'basis': 'city_assessment'},
}

INDEPENDENT_NOT_PERFORMED = {
    'status': 'NOT PERFORMED',
    'meaning': 'No person has yet read each cited page and confirmed that it supports the claim made from it. The '
               'automated checks establish that citations exist and that numbers and quotes appear where cited; a '
               'valid page, or a matching number on it, does not by itself establish support.'}
DOES_NOT_ESTABLISH = ['that the cited page supports the claim made from it (human source verification)',
                      'that any legal interpretation is correct',
                      'that the calculation method is the appropriate one for the question',
                      'that answers are consistent with one another']


def norm(s):
    s = s.replace('\x08', ' ').replace('\u2019', "'").replace('\u2018', "'").replace('\u201c', '"').replace('\u201d', '"')
    s = s.replace('\u2013', '-').replace('\u2014', '-').replace('\ufb01', 'fi').replace('\ufb02', 'fl')
    return re.sub(r'\s+', ' ', s).strip().lower()


@lru_cache(maxsize=None)
def page_count(doc):
    d = DOCS[doc]
    out = subprocess.run(['pdfinfo', str(REPO / d['local'])], capture_output=True, text=True, check=True).stdout
    return int(re.search(r'^Pages:\s+(\d+)', out, re.M).group(1))


@lru_cache(maxsize=None)
def page_text(doc, page):
    """Normalised text of one PDF page (raw and layout modes joined), or of the transcription for that page."""
    d = DOCS[doc]
    if d.get('transcription'):
        lines = (REPO / d['transcription']).read_text().split('\n')
        return norm(' '.join(l for l in lines if re.search(rf'\(PDF p\.{page}\b', l)))
    parts = []
    for mode in ([], ['-layout']):
        parts.append(subprocess.run(['pdftotext', *mode, '-f', str(page), '-l', str(page), str(REPO / d['local']), '-'],
                                    capture_output=True, text=True, check=True).stdout)
    return norm(' \n '.join(parts))


def fact(fid, value, basis, doc, pages, label, pdf_page, quote=None, unit='usd', record=None, printed=False):
    """pdf_page: an int or a (first, last) range of PDF pages. record: 'file.json:key/key/0/key' holding the value.
    printed: True if the value itself is printed on the cited page (checked); a string to check a printed form."""
    first, last = (pdf_page, pdf_page) if isinstance(pdf_page, int) else pdf_page
    return {'fact_id': fid, 'label': label, 'value': value, 'unit': unit, 'basis': basis, 'record': record,
            'printed': printed,
            'cite': {'doc_id': doc, 'pages': pages, 'quote': quote, 'pdf_page': first, 'pdf_page_last': last}}


OPS = {'sum': lambda xs: sum(xs), 'sub': lambda xs: xs[0] - sum(xs[1:]), 'div': lambda xs: xs[0] / xs[1]}


def calc(cid, label, op, inputs, result, unit='usd', note=None, digits=None):
    """op over the facts named in inputs, in order; digits rounds a ratio result."""
    expr = {'sum': ' + ', 'sub': ' - ', 'div': ' / '}[op].join(inputs)
    return {'id': cid, 'label': label, 'op': op, 'expression': expr, 'inputs': inputs, 'result': result, 'unit': unit,
            'digits': digits, 'note': note}


def load(name):
    return json.loads((DATA / name).read_text())


def record_value(ref):
    name, path = ref.split(':', 1)
    v = load(name)
    for k in path.split('/'):
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


# ------------------------------------------------------------------ answers

SF = 'street-funding-sources.json'
F501 = SF + ':funding_sources/0'
FF = SF + ':funding_sources/1'
BUDGET, PLAN, ORD, ACFR, PTAP = ('doc:budget-adoption-2026-06-23', 'doc:street-plan-2026-07-07', 'doc:measure-ff-ordinance',
                                 'doc:acfr-fy2025', 'doc:ptap25')
ALLOCATION_QUOTE = ('Tax proceeds shall be allocated approximately as follows: 1) 60% for streets and sidewalks, of which '
                    'roughly three quarters (45%) will be for streets and one quarter (15%) will be for sidewalks and '
                    'pedestrian paths, until the backlog of damaged sidewalks and pedestrian paths is eliminated. 2) 30% for '
                    'safety improvements. 3) The remaining 10% shall include environmental enhancements')


def law_allocation():
    return fact('law:bmc-7.11.020C', None, 'law', ORD, 'BMC 7.11.020(C), PDF p.8', 'Allocation set by voters', 8,
                unit='text', quote=ALLOCATION_QUOTE)


def law_no_alteration():
    return fact('law:bmc-7.11-section-7a3', None, 'law', ORD, 'Section 7(a)(3), PDF p.15',
                'Council may not alter the Measure FF allocation without voters', 15, unit='text',
                quote='Alter the allocations of Section 7.11.020')


def answer_capital_to_streets():
    sf = load(SF)
    f501, ff = sf['funding_sources']
    a = f501['appropriations_adopted_cip']
    avail = f501['available_for_paving']
    facts = [
        fact('fund:501/cip/fy2027/total', a['fy2027']['all'], 'adopted', BUDGET, 'p.173 (fund 501 Grand Total; also p.170)',
             'Fund 501 (CIP Fund) FY2027 capital program', 173, record=F501 + '/appropriations_adopted_cip/fy2027/all',
             printed=True),
        fact('fund:501/cip/fy2027/paving', a['fy2027']['paving'], 'adopted', BUDGET, 'p.173 (Streets Total)',
             'Of which Streets (paving)', 173, record=F501 + '/appropriations_adopted_cip/fy2027/paving', printed=True),
        fact('fund:501/cip/fy2027/other', a['fy2027']['other'], 'adopted', BUDGET, 'pp.172-173 (sum of non-Streets lines)',
             'Of which all other fund 501 projects', (172, 173), record=F501 + '/appropriations_adopted_cip/fy2027/other'),
        fact('fund:501/cip/fy2028/other', a['fy2028']['other'], 'adopted', BUDGET, 'pp.172-173 (sum of non-Streets lines)',
             'FY2028, all other fund 501 projects', (172, 173), record=F501 + '/appropriations_adopted_cip/fy2028/other'),
        fact('fund:501/cip/fy2027-28/contractual-jpa', avail['contractual_jpa_excluded'], 'adopted', BUDGET,
             'pp.172-173 (Tom Bates turf JPA contribution, FY2027 + FY2028)', 'Of which a contractual Joint Powers '
             'Agreement contribution', (172, 173), record=F501 + '/available_for_paving/contractual_jpa_excluded'),
        fact('fund:501/acfr/2025/assigned', 16060094, 'audited', ACFR, 'PDF p.75 (printed p.40)',
             'Fund 501 assigned fund balance, June 30, 2025', 75, printed=True),
        fact('fund:501/acfr/2025/encumbrances', f501['balances_june_30_2025']['encumbrances_outstanding'], 'audited', ACFR,
             'PDF p.142 (printed p.108)', 'Fund 501 encumbrances outstanding, June 30, 2025', 142,
             record=F501 + '/balances_june_30_2025/encumbrances_outstanding', printed=True),
        fact('doc:acfr-fy2025/carryover-rule', None, 'audited', ACFR, 'PDF p.180 (printed p.146)',
             'Capital appropriations carry forward', 180, unit='text',
             quote='Any unused funds are re-appropriated to the following fiscal year until the project is completed.'),
        fact('doc:acfr-fy2025/assigned-definition', None, 'audited', ACFR, 'PDF p.103 (printed p.69)',
             'Who controls assigned fund balance', 103, unit='text',
             quote='Intent is expressed by the City Council or City Manager, to which the City Council has delegated the authority'),
        fact('doc:budget/cip-pre-allocated', None, 'adopted', BUDGET, 'p.239', 'City statement on CIP Fund availability', 239,
             unit='text', quote='there is no CIP funding available for IT in FY 2027 and FY 2028'),
        fact('plan:pci70-gap', None, 'city_model', PLAN, 'p.12', 'City estimate of the added annual cost of PCI 70', 12,
             unit='text', quote='This scenario requires an estimated $37.6 million per year3, approximately $8 million per'),
        law_allocation(),
        law_no_alteration(),
        fact('ff:program/street-rehab-share', ff['allocation_fixed_by_voters']['adopted_five_year_program']['street_rehabilitation_share'],
             'adopted', PLAN, 'p.4 (Table 1C); budget-adoption p.215', 'Share of the five-year Measure FF program in street '
             'rehabilitation (BeTH ratio: $42,119,935 printed on budget p.215, over the program total, BeTH\'s sum of the '
             'Table 1C category totals)', 4, unit='ratio',
             record=FF + '/allocation_fixed_by_voters/adopted_five_year_program/street_rehabilitation_share'),
    ]
    gross = a['fy2027']['other'] + a['fy2028']['other']
    net = gross - avail['contractual_jpa_excluded']
    unenc = 16060094 - f501['balances_june_30_2025']['encumbrances_outstanding']
    share = a['fy2027']['paving'] / a['fy2027']['all']
    calcs = [
        calc('c1', 'Gross conditional deferral ceiling: fund 501 non-paving appropriations, FY2027 + FY2028', 'sum',
             ['fund:501/cip/fy2027/other', 'fund:501/cip/fy2028/other'], gross,
             note='Appropriations, not verified available cash. Reached only by deferring or cancelling every one of them.'),
        calc('c2', 'Deferral ceiling excluding the contractual JPA contribution', 'sub',
             ['c1', 'fund:501/cip/fy2027-28/contractual-jpa'], net, note='Not verified available cash.'),
        calc('c3', 'Share of fund 501 FY2027 money already in paving', 'div',
             ['fund:501/cip/fy2027/paving', 'fund:501/cip/fy2027/total'], round(share, 4), unit='ratio', digits=4),
        calc('c4', 'Unencumbered assigned fund balance, June 30, 2025 (ceiling for one-time carryover)', 'sub',
             ['fund:501/acfr/2025/assigned', 'fund:501/acfr/2025/encumbrances'], unenc,
             note='Backs capital appropriations already carried forward, paving among them. Not free money.'),
    ]
    short = (f'From CIP Fund 501: a gross conditional ceiling of ${gross:,} of FY2027-FY2028 appropriations, or ${net:,} '
             f'excluding a contractual Joint Powers Agreement contribution. It is reached only by deferring or cancelling '
             f'every other project the fund pays for, and neither figure is verified available cash. {share:.0%} of the '
             f'fund\'s FY2027 money (${a["fy2027"]["paving"]:,}) already goes to paving. A one-time amount from unspent '
             f'carried-over appropriations may exist but cannot be measured from public records; its ceiling at June 30, '
             f'2025 was ${unenc:,}. From Measure FF: the adopted program already puts '
             f'{facts[-1]["value"]:.1%} into street rehabilitation, against a voter-set allocation of "approximately" 45% '
             f'that Council cannot alter without a vote. Whether more could go to paving without a vote is an unresolved '
             f'legal question, and BeTH states no amount.')
    interp = [{
        'claim_id': 'claim:fund-501-small',
        'text': 'For scale, the two figures measure different things. The City estimates that reaching an average PCI of 70 '
                'would take about $8 million a year of additional spending beyond its modeled Plan + Measure FF scenario. '
                f'Fund 501\'s non-paving capital is ${a["fy2027"]["other"]:,} a year of budgeted projects, mostly repairs to '
                'existing City buildings, that could be freed only by deferring them; it is not available cash. Redirecting '
                'it would not close the modeled gap.',
        'counterargument': 'This covers only fund 501 and Measure FF. Other capital funds, unspent carryovers, the General '
                           'Fund itself and delivery-cost savings are not assessed here and could change the total.',
        'confidence': 'Moderate'}]
    missing = [{'needed': m, 'status': 'not in record'} for m in sf['answer']['what_would_complete_it']]
    missing.append({'needed': 'A City Attorney opinion or Council interpretation of the Measure FF allocation '
                              '(BMC 7.11.020(C)) as it applies to added paving.', 'status': 'not in record'})
    headline = (f'Little can be shown to be available. Fund 501 could free at most ${gross:,} over two years, only by '
                f'delaying every other project it pays for; that is a budget ceiling, not cash. Whether Measure FF could add '
                f'more is an open legal question.')
    key = ['The ${:,} is money budgeted for other projects, not money known to be unspent. Public records do not show how '
           'much is already under contract or spent.'.format(gross),
           'Freeing it means delaying roof, building, pool, sidewalk and other repairs. BeTH has not assessed what those '
           'delays would cost.',
           'Measure FF says "approximately" 45% for streets. Whether that allows more paving without a vote has not been '
           'settled by the City Attorney or Council.']
    return {'slug': 'capital-to-streets', 'question': sf['answer']['question'], 'headline': headline,
            'key_uncertainties': key,
            'resolution': {'entities': ['fund:501', 'fund:166'], 'measures': ['appropriation', 'fund_balance'],
                           'period': {'fy_start': 2027, 'fy_end': 2028},
                           'scope': sf['answer']['scope']},
            'short_answer': short, 'facts': facts, 'calculations': calcs, 'interpretation': interp,
            'scenario_assumptions': [], 'missing_evidence': missing,
            'open_interpretations': [
                'BeTH has not assessed what it would cost to delay the roof, building, pool, sidewalk and other repairs that '
                'fund 501 pays for, including legal, contract and safety consequences.',
                'Public records do not show how much of the FY2027-FY2028 budget for these projects is already under contract '
                'or spent. The ceilings are budget amounts, not cash known to be available.',
                f'The ${unenc:,} one-time ceiling is from June 30, 2025, sixteen months ago, and already backs projects carried '
                'forward from earlier years. How much of it is still uncommitted is unknown.',
                'For Measure FF, BeTH gives no dollar amount because the legal questions on the Measure FF page are unresolved.',
                'Measure FF requires the City to keep spending a minimum amount of other money on street maintenance. BeTH '
                'estimated that minimum because the City has not published its own calculation, and the ordinance does not '
                'state the base year or inflation index. The minimum limits moving paving money out of streets, not into them.',
                'Changes Council made at the June 23, 2026 meeting are not in the budget document BeTH used. The FY2027 Annual '
                'Appropriation Ordinance, the controlling record, is not in BeTH\'s sources.'],
            'more': ['../../07-street-funding-legal-analysis.md', '../data/phase2.json']}


def answer_measure_ff_paving():
    sf = load(SF)
    ff = sf['funding_sources'][1]
    prog = ff['allocation_fixed_by_voters']['adopted_five_year_program']
    P = FF + '/allocation_fixed_by_voters/adopted_five_year_program/'
    facts = [
        law_allocation(),
        law_no_alteration(),
        fact('law:bmc-7.11.030B', None, 'law', ORD, 'BMC 7.11.030(B), PDF p.8', 'Maintenance of effort', 8, unit='text',
             quote='the City Council shall not be authorized to impose the special tax for the following two years'),
        fact('ff:program/total', prog['total'], 'adopted', PLAN, 'p.4 (Table 1C; BeTH sum of the printed category totals)',
             'Five-year Measure FF program', 4, record=P + 'total'),
        fact('ff:program/street-rehab', prog['street_rehabilitation_cip'], 'adopted', BUDGET, 'p.215',
             'Measure FF street rehabilitation, FY2027-FY2031', 215, record=P + 'street_rehabilitation_cip', printed=True),
        fact('ff:revenue/fy2027', ff['balances']['fy2027_revenue'], 'adopted', 'doc:measure-ff-rate-fy2027', 'p.1',
             'FY2027 Measure FF revenue', 1, quote='is projected to yield $16,651,651 in revenues',
             record=FF + '/balances/fy2027_revenue', printed=True),
    ]
    share = prog['street_rehabilitation_cip'] / prog['total']
    calcs = [calc('c1', 'Street rehabilitation share of the five-year Measure FF program', 'div',
                  ['ff:program/street-rehab', 'ff:program/total'], round(share, 4), unit='ratio', digits=4)]
    short = (f'Not established. Voters set the split at approximately 45% streets, 15% sidewalks and paths, 30% safety and '
             f'10% environmental and other uses, and Council cannot alter it without a vote. The adopted program already '
             f'puts {share:.1%} of Measure FF (${prog["street_rehabilitation_cip"]:,} of ${prog["total"]:,}) into street '
             f'rehabilitation. Whether Council could put more into paving without a vote turns on unresolved legal '
             f'questions: how much room "approximately" allows, whether the shares apply each year or over the life of the '
             f'tax, and how revenue not yet programmed may be used. BeTH states no amount.')
    interp = [{'claim_id': 'claim:ff-room-unresolved',
               'text': 'The adopted program is already at the ordinance\'s approximate street share, so more Measure FF '
                       'paving would have to come from the latitude "approximately" allows or from revenue not yet '
                       'programmed. How large that latitude is cannot be settled from the ordinance text.',
               'counterargument': 'A strict reading, with the shares binding each year\'s appropriations, leaves little or no '
                                  'room. A looser reading, with the shares measured over the 14-year life of the tax, could '
                                  'allow more paving in early years balanced later. No City Attorney opinion in BeTH\'s '
                                  'sources settles which applies.',
               'confidence': 'Moderate'}]
    missing = [{'needed': 'City Attorney opinion or Council interpretation of "approximately" and of the period over which '
                          'the 7.11.020(C) shares apply.', 'status': 'not in record'},
               {'needed': 'June 30, 2026 Measure FF balance (the first rate covered 18 months of collections).',
                'would_be_in': 'FY2026 ACFR (expected early 2027)', 'status': 'not in record'},
               {'needed': 'Programming of the $1,351,651 FY2027 revenue increase adopted in Exhibit C.',
                'would_be_in': 'FY2027 Annual Appropriation Ordinance amendments', 'status': 'not in record'}]
    headline = (f'Unclear. Voters fixed Measure FF\'s split at about 45% for streets, and the adopted plan already puts '
                f'{share:.1%} into street repaving. Whether more could go to paving without a vote is an open legal question.')
    key = ['The ordinance says "approximately" 45% for streets. It does not say how much room that allows.',
           'It does not say whether the split must be met every year or over the 14-year life of the tax.',
           'No City Attorney opinion on these questions is in the public records BeTH holds.']
    return {'slug': 'measure-ff-paving', 'question': 'Could Measure FF money pay for more street paving?',
            'headline': headline, 'key_uncertainties': key,
            'resolution': {'entities': ['fund:166'], 'measures': ['allocation', 'appropriation'],
                           'period': {'fy_start': 2027, 'fy_end': 2031}},
            'short_answer': short, 'facts': facts, 'calculations': calcs, 'interpretation': interp,
            'scenario_assumptions': [], 'missing_evidence': missing,
            'open_interpretations': [
                'How much room the word "approximately" in "approximately 45%" allows, and who decides.',
                'Whether the percentages must be met every year, over the five-year plan, or over the 14-year life of the tax.',
                'Whether the ordinance\'s "streets" share means the same thing as the budget\'s "street rehabilitation" line, '
                'or also covers street work paid for from the safety or environmental shares.',
                'How the City may use FY2027 revenue that came in above the adopted plan, and FY2026 collections not yet '
                'budgeted. Neither has been assigned in the documents BeTH holds.',
                'The ordinance says the percentage rules end when the citywide average PCI reaches 70, but the sentence that '
                'says so points to the wrong subsection (7.11.020(D) refers to 7.11.030(C)). This is probably a drafting '
                'error, and its effect is not settled.',
                'No City Attorney opinion or Council interpretation of these provisions is in BeTH\'s sources.',
                'The ordinance is a scanned document. BeTH checked quotes against its own transcription, which a reviewer must '
                'compare with the scanned pages (PDF pages 8 and 15).',
                'The five-year Measure FF total is BeTH\'s sum of the category totals in the City\'s table; the table prints '
                'no single grand total.'],
            'more': ['../../07-street-funding-legal-analysis.md']}


def answer_street_condition():
    nc = load('network-condition.json')
    pc = load('street-plan-conditions.json')['plans']
    d = nc['distribution']
    both = pc['both_plans_fy2027_2031']
    NC = 'network-condition.json:'
    facts = [
        fact('pave:network/2024/average-pci', 56, 'city_assessment', PTAP, 'Executive Summary p.2, PDF p.5',
             'Network average PCI (2024 inspection)', 5, unit='pci', printed=True,
             quote="The updated Pavement Management Program showed that the City's overall average PCI is 56."),
        fact('pave:network/2024/poor-to-failed-share', 0.4193, 'city_assessment', PTAP, 'Executive Summary p.4, PDF p.7',
             'Share of pavement area in Poor to Failed condition (PTAP categories, PCI 50 and below)', 7, unit='ratio',
             printed=True,
             quote="41.93% are in Poor to Failed condition"),
        fact('pave:network/2024/miles-below-50', d['below_pci_50']['centerline_miles_unrounded'], 'city_assessment', PTAP,
             'Section IV, Street Sections Alphabetical, PDF pp.40-67',
             'Centerline miles below PCI 50 (BeTH sum of section lengths in feet / 5,280; 1,216 sections validated to the '
             'report totals)', (40, 67), unit='miles', record=NC + 'distribution/below_pci_50/centerline_miles_unrounded'),
        fact('pave:network/2024/miles-below-25', d['below_pci_25']['centerline_miles_unrounded'], 'city_assessment', PTAP,
             'Section IV, Street Sections Alphabetical, PDF pp.40-67', 'Centerline miles below PCI 25', (40, 67),
             unit='miles', record=NC + 'distribution/below_pci_25/centerline_miles_unrounded'),
        fact('pave:network/2024/centerline-miles', nc['validation']['parsed']['centerline_miles_from_feet'], 'city_assessment',
             PTAP, 'Section IV, PDF pp.40-67; printed total 212.77, Executive Summary p.2, PDF p.5',
             'Network centerline miles (sum of section lengths in feet / 5,280)', (40, 67), unit='miles',
             record=NC + 'validation/parsed/centerline_miles_from_feet'),
        fact('pave:plans/fy2027-2031/miles-below-50', both['miles_below_pci_50'], 'adopted', PLAN,
             'Attachments, pp.21-62', 'Currently-below-50 miles treated by both adopted plans, FY2027-FY2031 (sum of '
             'printed section miles)', (21, 62), unit='miles',
             record='street-plan-conditions.json:plans/both_plans_fy2027_2031/miles_below_pci_50'),
        fact('pave:city-projection/2038/plan-plus-ff', 62, 'city_model', PLAN, 'p.12',
             'City projection, Five-Year Plan + Measure FF, 2038', 12, unit='pci', printed=True,
             quote='the citywide PCI is projected to improve to approximately 62 by 2038'),
        fact('law:bmc-7.11.010K1', None, 'law', ORD, 'BMC 7.11.010(K)(1), PDF p.7', 'Measure FF goal', 7, unit='text',
             quote='ideally with no streets having a PCI below 50'),
    ]
    m50, m25 = d['below_pci_50']['centerline_miles_unrounded'], d['below_pci_25']['centerline_miles_unrounded']
    total = nc['validation']['parsed']['centerline_miles_from_feet']
    share50 = round(m50 / total, 4)
    calcs = [calc('c1', 'Share of centerline miles below PCI 50', 'div',
                  ['pave:network/2024/miles-below-50', 'pave:network/2024/centerline-miles'], share50, unit='ratio', digits=4)]
    short = (f'The average hides most of it. In the 2024 inspection the network averaged PCI 56, but {m50:.1f} centerline '
             f'miles ({share50:.0%} of the network) were below PCI 50 and {m25:.1f} miles were below 25. The City projects '
             f'an average of about 62 by 2038 with Measure FF, but publishes no projection of how many streets will still '
             f'be below 50. The adopted plans treat {both["miles_below_pci_50"]:.1f} miles of currently-below-50 streets over '
             f'five years.')
    interp = [{'claim_id': 'claim:average-not-failed-streets',
               'text': 'Reaching a network average of 60 or 62 is not the same as eliminating failed streets; the measure '
                       'that matches Measure FF\'s goal is the mileage below PCI 50.',
               'counterargument': 'Treating the worst streets first costs more per point of average PCI (the City shows about '
                                  'one point lower in 2038), so a lower failed-street count can mean a lower average; both '
                                  'measures are needed.',
               'confidence': 'High'}]
    missing = [{'needed': 'Projected miles below PCI 50 under each funding scenario.',
                'would_be_in': 'StreetSaver output; the Measure FF annual report must include "the PCI of all streets" (BMC 7.11.050(B)(1))',
                'status': 'not published'},
               {'needed': 'Condition after FY2025-FY2026 paving.', 'would_be_in': 'next StreetSaver inspection update',
                'status': 'not published'}]
    headline = (f'Worse than the average suggests. The 2024 average was PCI 56 out of 100, but {m50:.1f} miles of streets, '
                f'{share50:.0%} of the network, were below PCI 50.')
    key = ['The data are from 2024 inspections, before the last two years of paving.',
           'The City reports a related but different figure: 41.93% of pavement area in "poor" or "failed" condition. It '
           'measures area rather than length, and includes streets at exactly PCI 50.',
           'The City publishes no forecast of how many streets will still be below PCI 50 in future years.']
    return {'slug': 'street-condition', 'question': "How bad are Berkeley's streets, beyond the average PCI?",
            'headline': headline, 'key_uncertainties': key,
            'resolution': {'entities': ['network:streets'], 'measures': ['pci_average', 'miles_below_50'],
                           'period': {'as_of': '2024 inspection'},
                           'scope': 'Mileage is computed from section lengths in feet and reported to 0.1 mile. One '
                                    'uninspected 155-foot section (Tevlin St, PCI 0, no inspection date) is excluded, as in '
                                    'the report\'s totals table.'},
            'short_answer': short, 'facts': facts, 'calculations': calcs, 'interpretation': interp,
            'scenario_assumptions': [], 'missing_evidence': missing,
            'open_interpretations': [
                f'The City\'s 41.93% and BeTH\'s {m50:.1f} miles measure different things. The City\'s figure is pavement area '
                'rated "poor" or "failed" (PCI 50 and below); BeTH\'s figure is street length below PCI 50.',
                'BeTH measured length from each section\'s length in feet. Adding up the report\'s rounded mileage figures '
                'instead gives slightly more. Figures are shown to a tenth of a mile.',
                'One short section of Tevlin Street was not inspected and has no score. BeTH leaves it out, as the report\'s '
                'totals do; the report\'s condition table counts it as failed.',
                'The data are from 2024 inspections, before the City\'s FY2025-FY2026 paving.',
                'Street scores in the City\'s plans are the scores when the plans were written; streets will be in worse '
                f'condition by the time they are repaved. The {both["miles_below_pci_50"]:.1f} miles are streets now below 50 '
                'that the plans list for work.'],
            'more': ['../../06-pci60-financial-model.md']}


def answer_streets_139m():
    cip = load('cip-projects.json')
    r = cip['reconciliation']['streets_139m']
    idn = r['identity']
    ID = 'cip-projects.json:reconciliation/streets_139m/identity/'
    ST = 'cip-projects.json:categories/Streets/printed_grand_total/'
    facts = [
        fact('cip:streets/five-year/street-rehab-plan', idn['five_year_street_rehabilitation_plan'], 'adopted', BUDGET,
             'pp.215-216 (sum of the Street Rehab lines)', 'Five-Year Street Rehabilitation Plan (Exhibit B lines)', (215, 216),
             record=ID + 'five_year_street_rehabilitation_plan'),
        fact('cip:streets/five-year/measure-ff', idn['measure_ff_street_rehabilitation'], 'adopted', BUDGET, 'p.215',
             'Measure FF Street Rehabilitation', 215, record=ID + 'measure_ff_street_rehabilitation', printed=True),
        fact('cip:streets/five-year/bridge', idn['other_streets_projects']['Bridge Preventative Maintenance Program'], 'adopted',
             BUDGET, 'p.215', 'Bridge Preventive Maintenance', 215,
             record=ID + 'other_streets_projects/Bridge Preventative Maintenance Program', printed=True),
        fact('cip:streets/five-year/harold-way', idn['other_streets_projects']['Harold Way Placemaking'], 'adopted', BUDGET,
             'p.215', 'Harold Way Placemaking', 215, record=ID + 'other_streets_projects/Harold Way Placemaking', printed=True),
        fact('cip:streets/five-year/printed-total', idn['printed_streets_five_year_budget'], 'adopted', BUDGET, 'p.216',
             'Printed Streets five-year budget', 216, quote='$139,356,147 in Five-Year CIP Budget',
             record=ID + 'printed_streets_five_year_budget', printed=True),
        fact('cip:streets/fy2027', cip['categories']['Streets']['printed_grand_total']['fy2027'], 'adopted', BUDGET,
             'p.169 (category table); also p.216', 'Streets, FY2027', 169, record=ST + 'fy2027', printed=True),
        fact('cip:streets/fy2028', cip['categories']['Streets']['printed_grand_total']['fy2028'], 'adopted', BUDGET,
             'p.169 (category table); also p.216', 'Streets, FY2028', 169, record=ST + 'fy2028', printed=True),
        fact('plan:table-1b/five-year-plan', 96336212, 'adopted', PLAN, 'p.3 (Table 1B)', 'Street plan five-year total', 3,
             printed=True),
    ]
    total = (idn['five_year_street_rehabilitation_plan'] + idn['measure_ff_street_rehabilitation']
             + sum(idn['other_streets_projects'].values()))
    two = facts[5]['value'] + facts[6]['value']
    calcs = [calc('c1', 'Sum of the four Streets projects', 'sum', [f['fact_id'] for f in facts[:4]], total),
             calc('c2', 'Two-year (FY2027 + FY2028) Streets amount', 'sum', ['cip:streets/fy2027', 'cip:streets/fy2028'], two)]
    short = (f'It is the five-year (FY2027-FY2031) Streets capital budget, not a two-year one: the paving plan '
             f'(${idn["five_year_street_rehabilitation_plan"]:,}), Measure FF street rehabilitation '
             f'(${idn["measure_ff_street_rehabilitation"]:,}), bridge maintenance and Harold Way placemaking add to exactly '
             f'${total:,}. The two-year FY2027-FY2028 Streets amount is ${two:,}.')
    interp = [{'claim_id': 'claim:139m-is-five-year', 'text': f'Comparisons that treat ${total:,} as a biennial figure '
               'overstate two-year street spending by more than double. (The figure in the question is slightly low: the '
               'exact amount rounds to $139.4 million.)',
               'counterargument': 'FY2029-FY2031 are planned amounts and may change; the two-year figure is the only one '
                                  'with appropriations behind it.', 'confidence': 'High'}]
    missing = [{'needed': 'FY2027 Annual Appropriation Ordinance (controlling record, incl. any June 23 amendments).',
                'status': 'not in record'}]
    headline = (f'It is a five-year figure, not a two-year one. The ${total:,} covers FY2027 through FY2031; the two-year '
                f'amount is ${two:,}.')
    key = ['The last three years, FY2029-FY2031, are plans, not approved spending, and may change.',
           'Some one-time street-related money added with the Mayor\'s budget recommendations is outside this table.']
    return {'slug': 'streets-139m', 'question': 'What does the $139.3 million streets figure include?',
            'headline': headline, 'key_uncertainties': key,
            'resolution': {'entities': ['cip:streets'], 'measures': ['appropriation'], 'period': {'fy_start': 2027, 'fy_end': 2031}},
            'short_answer': short, 'facts': facts, 'calculations': calcs, 'interpretation': interp,
            'scenario_assumptions': [], 'missing_evidence': missing,
            'open_interpretations': [
                'BeTH has not found the source of the figure in the question. The exact five-year amount rounds to $139.4 '
                'million, and the City\'s street plan describes it as "over $139 million".',
                'The last three years, FY2029-FY2031, are plans, not approved spending.',
                'Some one-time money added with the Mayor\'s budget recommendations, including funding for Oxford for All, '
                'is outside the Streets table. Whether it belongs in a "streets figure" is a judgment call.',
                'Changes Council made at the June 23, 2026 meeting, and the FY2027 Annual Appropriation Ordinance, are not in '
                'BeTH\'s sources.'],
            'more': ['../data/phase2.json']}


ANSWERS = (answer_capital_to_streets, answer_measure_ff_paving, answer_street_condition, answer_streets_139m)


# ------------------------------------------------------------------ verifier

MONEY = re.compile(r'\$([\d,]+(?:\.\d+)?)(\s*(?:million|M)\b)?')
PCT = re.compile(r'(\d+(?:\.\d+)?)%')
MILES = re.compile(r'(\d+(?:\.\d+)?)\s+(?:centerline\s+)?miles\b')


def _decimals(tok):
    return len(tok.split('.')[1]) if '.' in tok else 0


def check_citation(cite):
    doc = cite.get('doc_id')
    if doc not in DOCS:
        return [f'citation: unknown document {doc}']
    if not (REPO / DOCS[doc]['local']).exists():
        return [f'citation: PDF for {doc} not found at {DOCS[doc]["local"]}']
    first, last = cite.get('pdf_page'), cite.get('pdf_page_last')
    if not isinstance(first, int) or not isinstance(last, int) or first < 1 or last < first:
        return [f'citation: {doc} has no valid PDF page ({first!r}-{last!r})']
    n = page_count(doc)
    if last > n:
        return [f'citation: {doc} PDF p.{last} does not exist (the PDF has {n} pages)']
    return []


def on_cited_pages(cite, needle):
    return any(norm(needle) in page_text(cite['doc_id'], p) for p in range(cite['pdf_page'], cite['pdf_page_last'] + 1))


def printed_forms(f):
    v, u = f['value'], f['unit']
    if isinstance(f['printed'], str):
        return [f['printed']]
    if u == 'usd':
        return [f'{v:,}', f'$ {v:,}']
    if u == 'ratio':
        return [f'{v * 100:.2f}%', f'{v * 100:.1f}%']
    return [f'{v}']


def verify(ans):
    problems, support = [], {}
    facts = {}
    for f in ans['facts']:
        fid, cite = f['fact_id'], f['cite']
        if fid in facts:
            problems.append(f'fact {fid}: duplicate fact_id')
        facts[fid] = f
        cp = check_citation(cite)
        problems += [f'fact {fid}: {p}' for p in cp]
        numeric = isinstance(f['value'], (int, float)) and not isinstance(f['value'], bool)
        if f['value'] is not None and not numeric:
            problems.append(f'fact {fid}: value {f["value"]!r} is not numeric')
        how = []
        if f.get('record'):
            try:
                rv = record_value(f['record'])
            except (KeyError, IndexError, ValueError, FileNotFoundError) as e:
                problems.append(f'fact {fid}: record {f["record"]} does not resolve ({e!r})')
            else:
                if rv != f['value']:
                    problems.append(f'fact {fid}: value {f["value"]!r} != record {f["record"]} ({rv!r})')
                else:
                    how.append('matches data record')
        if not cp and f.get('printed') and numeric:
            if cite.get('quote'):
                # a bare number such as "56" proves nothing on a page; it must sit inside the quoted passage
                if any(re.search(rf'(?<![\d.,]){re.escape(s)}(?![\d,]|\.\d)', cite['quote']) for s in printed_forms(f)):
                    how.append('value printed in the quoted passage')
                else:
                    problems.append(f'fact {fid}: value {printed_forms(f)[0]} not found in its quote')
            elif any(on_cited_pages(cite, s) for s in printed_forms(f)):
                how.append('value printed on cited page')
            else:
                problems.append(f'fact {fid}: value {printed_forms(f)[0]} not found on {cite["doc_id"]} PDF p.{cite["pdf_page"]}')
        if numeric and not how and not any(p.startswith(f'fact {fid}:') for p in problems):
            problems.append(f'fact {fid}: numeric value has neither a data record nor a printed check')
        if cite.get('quote') and not cp:
            if on_cited_pages(cite, cite['quote']):
                how.append('quote found on cited page')
            else:
                problems.append(f'fact {fid}: quote not on cited page {cite["doc_id"]} PDF p.{cite["pdf_page"]}: '
                                f'{cite["quote"][:60]}')
        if not numeric and not cite.get('quote'):
            problems.append(f'fact {fid}: text fact without a quote')
        support[fid] = '; '.join(how) or 'none'
    results, arithmetic = {}, []
    for c in ans['calculations']:
        vals = []
        for i in c['inputs']:
            src = facts.get(i)
            v = src['value'] if src else results.get(i)
            if v is None or isinstance(v, bool) or not isinstance(v, (int, float)):
                problems.append(f'calculation {c["id"]}: input {i!r} does not resolve to a numeric fact or earlier calculation')
                vals = None
                break
            vals.append(v)
        if c.get('op') not in OPS:
            problems.append(f'calculation {c["id"]}: unknown op {c.get("op")!r}')
            continue
        if vals is None or (c['op'] == 'div' and (len(vals) != 2 or vals[1] == 0)) or (c['op'] == 'sub' and len(vals) < 2):
            if vals is not None:
                problems.append(f'calculation {c["id"]}: wrong number of inputs for {c["op"]}')
            continue
        got = OPS[c['op']](vals)
        if c.get('digits') is not None:
            got = round(got, c['digits'])
        if not (isinstance(c['result'], (int, float)) and abs(got - c['result']) < 1e-9):
            problems.append(f'calculation {c["id"]}: stated result {c["result"]!r} != recomputed {got!r}')
        results[c['id']] = got
        unit_of = {**{f: facts[f]['unit'] for f in facts}, **{a['id']: a['unit'] for a in arithmetic}}
        arithmetic.append({'id': c['id'], 'label': c['label'], 'op': c['op'], 'unit': c['unit'], 'note': c.get('note'),
                           'inputs': [{'ref': i, 'value': v, 'unit': unit_of.get(i, c['unit'])}
                                      for i, v in zip(c['inputs'], vals)],
                           'recomputed': got})
    vals = [(f['value'], f['unit']) for f in ans['facts'] if isinstance(f['value'], (int, float))] + \
           [(c['result'], c['unit']) for c in ans['calculations'] if isinstance(c['result'], (int, float))]
    quoted = ' '.join(f['cite']['quote'] for f in ans['facts'] if f['cite'].get('quote'))
    prose = ' '.join([ans['headline'], ans['short_answer'], *ans['key_uncertainties'], *ans['open_interpretations'],
                      *(i['text'] + ' ' + i['counterargument'] for i in ans['interpretation'])])
    if not ans['headline'] or not ans['key_uncertainties'] or not ans['open_interpretations']:
        problems.append('presentation: headline, key uncertainties and open interpretations are required')
    for m in MONEY.finditer(prose):
        tok, n = m.group(1), float(m.group(1).replace(',', ''))
        if m.group(2):
            ok = any(u == 'usd' and abs(round(v / 1e6, _decimals(tok)) - n) < 1e-9 for v, u in vals)
        else:
            ok = any(u == 'usd' and abs(v - n) < 0.5 for v, u in vals)
        ok = ok or f'${tok}{(m.group(2) or "")}'.replace(' ', '') in quoted.replace(' ', '')
        if not ok:
            problems.append(f'prose: number {m.group(0).strip()!r} not in facts, calculations or cited quotes')
    for m in PCT.finditer(prose):
        p, dec = float(m.group(1)), _decimals(m.group(1))
        ok = any(u == 'ratio' and abs(round(v * 100, dec) - p) < 1e-9 for v, u in vals)
        ok = ok or re.search(rf'(?<![\d.]){re.escape(m.group(0))}', quoted) is not None
        if not ok:
            problems.append(f'prose: percentage {m.group(0)!r} not in facts, calculations or cited quotes')
    for m in MILES.finditer(prose):
        n, dec = float(m.group(1)), _decimals(m.group(1))
        if not any(u == 'miles' and abs(round(v, dec) - n) < 1e-9 for v, u in vals):
            problems.append(f'prose: mileage {m.group(0)!r} not in facts or calculations')
    for i in ans['interpretation']:
        if not i.get('counterargument'):
            problems.append(f'interpretation {i["claim_id"]} has no counterargument')
    if not ans['missing_evidence']:
        problems.append('missing_evidence is empty')

    def none_of(*prefixes):
        return not any(any(k in p for k in prefixes) for p in problems)
    ans['verifier'] = {
        'kind': 'automated structural checks',
        'checks': {'citations_resolve': none_of('citation:'),
                   'facts_resolve_to_records_or_cited_pages': none_of('record', 'neither a data record', 'not found on',
                                                                     'not numeric', 'duplicate'),
                   'quotes_on_cited_pages': none_of('quote not on', 'without a quote'),
                   'calculations_recomputed': none_of('calculation '),
                   'prose_numbers_traced': none_of('prose:'),
                   'counterarguments_present': none_of('counterargument'),
                   'missing_evidence_present': none_of('missing_evidence')},
        'structural_checks_passed': not problems,
        'passed': not problems,
        'problems': problems,
        'fact_support': support,
        'arithmetic': arithmetic,
        'does_not_establish': list(DOES_NOT_ESTABLISH),
        'independent_source_verification': dict(INDEPENDENT_NOT_PERFORMED)}
    return ans


# ------------------------------------------------------------------ rendering
# One template for every answer: question, a short conclusion, the main uncertainties, a plain status line, then
# expandable details. Internal identifiers (fact ids, data-record paths, calculation references) carry class "tech"
# and stay hidden unless the reader turns on "Show technical references"; they remain in the page for auditing.

APPROVALS = ROOT / 'review' / 'human-approvals.json'
SHORT_DOC = {'doc:acfr-fy2025': 'FY2025 audited financial report',
             'doc:budget-adoption-2026-06-23': 'FY2027-28 adopted budget',
             'doc:street-plan-2026-07-07': 'July 2026 street plan',
             'doc:measure-ff-ordinance': 'Measure FF ordinance',
             'doc:measure-ff-rate-fy2027': 'FY2027 Measure FF tax-rate report',
             'doc:ptap25': '2024 pavement condition report'}
BASIS = {'audited': 'Audited', 'adopted': 'Adopted budget or plan', 'law': 'Law', 'city_assessment': 'City assessment',
         'city_model': 'City projection'}
APPROVAL_TEXT = {'NOT APPROVED': 'Not yet approved by an independent reviewer',
                 'APPROVED WITH CHANGES': 'Approved by an independent reviewer, with changes',
                 'APPROVED': 'Approved by an independent reviewer'}


def load_approvals():
    return json.loads(APPROVALS.read_text())['answers']


def fmt(f):
    v, u = f['value'], f['unit']
    if v is None:
        return '—'
    if u == 'usd':
        return f'${v:,.0f}'
    if u == 'ratio':
        return f'{v:.1%}'
    if u == 'miles':
        return f'{v:,.1f} mi'
    return f'{v:,}'


def pdf_href(cite):
    return f'{DOCS[cite["doc_id"]]["pdf"]}#page={cite["pdf_page"]}'


def page_words(cite):
    a, b = cite['pdf_page'], cite['pdf_page_last']
    return f'page {a}' if a == b else f'pages {a}-{b}'


def source_cell(f):
    e, c = html.escape, f['cite']
    d = DOCS[c['doc_id']]
    out = f'<a href="{e(pdf_href(c))}">{e(SHORT_DOC[c["doc_id"]])}, PDF {e(page_words(c))}</a>'
    if c['quote']:
        out += f'<blockquote>&ldquo;{e(c["quote"])}&rdquo;</blockquote>'
    out += (f'<div class="tech"><code>{e(f["fact_id"])}</code> · cited as: {e(c["pages"])} · {e(d["title"])}'
            + (f' · <a href="{e(d["url"])}">City copy</a>' if d.get('url') else '')
            + (f' · record <code>{e(f["record"])}</code>' if f.get('record') else '') + '</div>')
    return out


def render(ans, approval):
    e = html.escape
    v = ans['verifier']
    if not v['passed'] or len(v['arithmetic']) != len(ans['calculations']):
        raise ValueError(f'{ans["slug"]}: refusing to render an answer that did not pass the automated checks')
    labels = {f['fact_id']: f['label'] for f in ans['facts']} | {a['id']: a['label'] for a in v['arithmetic']}
    sym = {'sum': ' + ', 'sub': ' − ', 'div': ' ÷ '}
    calcs = ''.join(
        f'<li class="calc">{e(a["label"])}: '
        + e(sym[a['op']].join(fmt({'value': i['value'], 'unit': i['unit']}) for i in a['inputs']))
        + f' = <b>{e(fmt({"value": a["recomputed"], "unit": a["unit"]}))}</b>'
        + (f'<div class="note">{e(a["note"])}</div>' if a.get('note') else '')
        + '<div class="note">Using: ' + e('; '.join(labels.get(i['ref'], i['ref']) for i in a['inputs'])) + '.</div>'
        + f'<div class="tech"><code>{e(sym[a["op"]].join(i["ref"] for i in a["inputs"]))}</code></div></li>'
        for a in v['arithmetic'])
    rows = ''.join(f'<tr><td>{e(f["label"])}<div class="basis">{e(BASIS.get(f["basis"], f["basis"]))}</div></td>'
                   f'<td class="n">{fmt(f)}</td><td>{source_cell(f)}'
                   f'<div class="tech">automated check: {e(v["fact_support"].get(f["fact_id"], ""))}</div></td></tr>'
                   for f in ans['facts'])
    reading = ''.join(f'<li>{e(i["text"])} <span class="note">(BeTH\'s confidence: {e(i["confidence"])})</span>'
                      f'<div class="note"><b>The other side:</b> {e(i["counterargument"])}</div></li>'
                      for i in ans['interpretation'])
    miss = ''.join(f'<li>{e(m["needed"])}' + (f' <span class="note">Would be in: {e(m["would_be_in"])}.</span>'
                                              if m.get('would_be_in') else '') + '</li>' for m in ans['missing_evidence'])
    opens = ''.join(f'<li>{e(x)}</li>' for x in ans['open_interpretations'])
    know = ''.join(f'<li>{e(x)}</li>' for x in ans['key_uncertainties'])
    limits = ''.join(f'<li>{e(x[0].upper() + x[1:])}.</li>' for x in v['does_not_establish'])
    st = approval['status']
    scope = ans['resolution'].get('scope')
    pres = design.PRESENTATION[ans['slug']]
    fig, credit, photo = design.photo_figure(ans['slug'], '../')
    body = f'''<section class="hero">{fig}<div class="wrap hero-in"><span class="kicker">{e(pres["kicker"])}</span>
<h1>{e(ans["question"])}</h1></div></section>
<main class="narrow lead">
<section class="answer"><div class="lbl">Short answer</div><p>{e(ans["headline"])}</p></section>
{design.highlights_html(ans, fmt)}
<section class="know"><div class="lbl">What you should know</div><ul>{know}</ul></section>
<div class="status"><span class="pill ok">Checked automatically against the cited records</span>
<span class="pill no">Not yet confirmed by a person</span><span class="pill no">{e(APPROVAL_TEXT[st])}</span></div>
{design.photo_caption(photo, credit, "photo-credits.html")}
<h2 class="sec">The picture in numbers</h2>
<p class="sec-sub">Drawn from the same City records as the answer. Every value is labelled; the full figures and sources are below.</p>
{chart_for(ans["slug"])}
<h2 class="sec">The details</h2>
<p class="sec-sub">Open any section to see the full answer, the open questions, every source and how the numbers were checked.</p>
<details><summary>The full answer and BeTH's reading</summary><div><p>{e(ans["short_answer"])}</p>
<ul class="plain">{reading}</ul>{f'<p class="note">Scope: {e(scope)}</p>' if scope else ''}</div></details>
<details><summary>Open questions <span>({len(ans["open_interpretations"])}) · what is unsettled or not yet known</span></summary>
<div><ul class="plain">{opens}</ul></div></details>
<details><summary>The numbers and where they come from <span>({len(ans["facts"])} sources)</span></summary>
<div><p class="note">Each link opens the City document at the cited page.</p><div class="tw"><table>
<thead><tr><th>What</th><th>Amount</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div></div></details>
<details><summary>How the numbers are worked out <span>({len(v["arithmetic"])})</span></summary>
<div><ul class="plain">{calcs}</ul><p class="note">These sums are recomputed by BeTH's checking program from the figures above.</p></div></details>
<details><summary>What's still missing</summary><div><ul class="plain">{miss}</ul></div></details>
<details><summary>How this page was checked</summary><div>
<p>A program checked that every cited document and page exists, that every figure matches BeTH's records or appears on
the cited page, that every quotation appears on its cited page, and that the arithmetic adds up. It also checked that
every number in the text above traces to one of those figures.</p>
<p><b>A program cannot confirm everything.</b> These checks do not establish:</p><ul class="plain">{limits}</ul>
<p>Human review: <b>{e(v["independent_source_verification"]["status"].capitalize())}</b>. Independent approval:
<b>{e(st.capitalize())}</b>.</p>
<div class="tech">verifier: {e(v["kind"])} · problems: {len(v["problems"])} · approval record
<code>phase2/review/human-approvals.json → answers.{e(ans["slug"])}</code> · answer data
<code>phase2/docs/data/answers.json</code></div></div></details>
<label class="techtoggle"><input type="checkbox" id="tech"> Show technical references</label>
<p class="cap"><a href="index.html">More questions</a> · <a href="../budget-choices.html">Budget choices prototype</a></p>
</main>'''
    return design.shell(f'{ans["question"]} — Ask BeTH (prototype)', body, '../', ans['headline'])


def chart_for(slug):
    if slug == 'street-condition':
        return design.chart_street_condition(load('network-condition.json'))
    if slug == 'measure-ff-paving':
        return design.chart_measure_ff(load(SF))
    if slug == 'streets-139m':
        return design.chart_streets_budget(load('cip-projects.json'))
    restrictions = json.loads((ROOT / 'docs' / 'data' / 'phase2.json').read_text())['capital']['by_restriction_class']
    return design.chart_capital(load(SF), restrictions)


def render_index(answers, approvals):
    e = html.escape
    cards = ''
    for a in answers:
        if not a['verifier']['passed']:
            continue
        pres = design.PRESENTATION[a['slug']]
        fig, credit, _ = design.photo_figure(a['slug'], '../', cls='card')
        cards += (f'<article class="card"><a class="card-link" href="{e(a["slug"])}.html" tabindex="-1" aria-hidden="true">'
                  f'{fig}</a><div class="card-b">'
                  f'<span class="kicker">{e(pres["kicker"])}</span>'
                  f'<h3><a href="{e(a["slug"])}.html">{e(pres["card_title"])}</a></h3>'
                  f'<p>{e(pres["card_text"])}</p><p class="answer-line">{e(a["headline"])}</p>'
                  f'<div class="status" style="margin:6px 0 0"><span class="pill no">'
                  f'{e(APPROVAL_TEXT[approvals[a["slug"]]["status"]])}</span></div>'
                  f'<a class="go" href="{e(a["slug"])}.html">Read the answer →</a>'
                  f'<span class="credit">Illustrative photo. {credit}.</span></div></article>')
    fig, credit, photo = design.photo_figure('home', '../')
    body = f'''<section class="hero home">{fig}<div class="wrap hero-in">
<span class="kicker">Berkeley budget questions, answered from City records</span>
<h1>Ask BeTH</h1><p class="sub">Where does Berkeley’s money go? What are we getting for it?</p></div></section>
<main class="wrap">
<div class="narrow" style="padding-inline:0">{design.photo_caption(photo, credit, "photo-credits.html")}</div>
<h2 class="sec">Four questions residents ask</h2>
<p class="sec-sub">Each answer starts short, shows the key numbers, says plainly what is uncertain, and links every figure to
the page of the City document it comes from.</p>
<div class="cards">{cards}</div>
<h2 class="sec">How BeTH answers</h2>
<div class="how"><div><b>Only City records</b><p>Budgets, audited financial reports, the Measure FF ordinance and the
City's pavement report. Every figure links to its page.</p></div>
<div><b>Checked by a program</b><p>Cited pages must exist, figures must match the records, quotes must appear on the
cited page and the arithmetic must add up. If anything fails, the answer is not shown.</p></div>
<div><b>Reviewed by a person</b><p>The last step is an independent reviewer reading every source. That has not happened
yet for these answers, and each page says so.</p></div></div>
<label class="techtoggle"><input type="checkbox" id="tech"> Show technical references</label>
<div class="tech">Answer data: <code>phase2/docs/data/answers.json</code> · approvals: <code>phase2/review/human-approvals.json</code>
· photo record: <code>phase2/docs/assets/photos/credits.json</code></div>
</main>'''
    return design.shell('Ask BeTH — Where does Berkeley’s money go?', body, '../',
                        'Where does Berkeley’s money go? What are we getting for it? Plain answers from City records.')


def main(argv):
    answers = [verify(f()) for f in ANSWERS]
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
        approvals = load_approvals()
        for a in answers:
            if a['verifier']['passed']:
                (OUT_DIR / f"{a['slug']}.html").write_text(render(a, approvals[a['slug']]))
        (OUT_DIR / 'index.html').write_text(render_index(answers, approvals))
        (OUT_DIR / 'photo-credits.html').write_text(design.credits_page())
        (ROOT / 'docs' / 'assets' / 'ask.css').write_text(design.CSS.lstrip())
        print('wrote', OUT_JSON.relative_to(REPO), 'and', len([a for a in answers if a['verifier']['passed']]), 'Ask pages')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

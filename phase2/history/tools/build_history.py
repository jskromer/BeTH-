#!/usr/bin/env python3
"""How Did We Get Here? -- Berkeley's budget decisions and their consequences. Streets and infrastructure, 2010-2026.

Research prototype. Builds a machine-readable decision history (data/decisions-streets.json), outcome series
(data/outcomes-streets.json) and a local visual timeline (docs/timeline.html) from primary records saved in sources/.

Rules this tool enforces:
  - every quoted citation must appear on its cited PDF page (pdftotext, normalised); the build fails otherwise;
  - every field carries a status: verified (with a citation), to_collect (record not yet obtained) or
    not_in_record (the record we hold does not say);
  - votes are copied as recorded. "All Ayes" is kept as "All Ayes": names are never inferred from the roll call;
  - alternatives are only those documented at the time (a failed motion, or options in the recommendation).
    Retrospective scenarios are a separate, empty list until researched;
  - no causal claim: outcomes are shown next to decisions, and any causal statement is attributed to its author.

Separate from the approved ledgers and from the Ask BeTH answers. Nothing here is published.

Run:  python3 phase2/history/tools/build_history.py [--write]
"""
import html
import json
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

HIST = Path(__file__).resolve().parents[1]
PHASE2 = HIST.parent
REPO = PHASE2.parent
sys.path.insert(0, str(PHASE2 / 'tools'))
import ask_design as design  # noqa: E402  shared BeTH visual design system

SCHEMA_VERSION = 1

# ------------------------------------------------------------------ source registry
# local: path from the repository root. Links in the page are relative to phase2/history/docs/.
DOCS = {}


def _doc(key, title, local, kind, url=None):
    DOCS[key] = {'title': title, 'local': local, 'kind': kind, 'url': url}


for d, extra in [('2022-01-25', ''), ('2022-07-26', ''), ('2023-07-25', ''), ('2023-11-28', ''), ('2024-07-09', ''),
                 ('2024-12-10', ''), ('2026-06-16', ''), ('2026-06-23', ''), ('2026-07-07', '')]:
    _doc(f'aa:{d}', f'City Council annotated agenda, {d}', f'phase2/history/sources/council-{d}-annotated.pdf',
         'annotated_agenda')
for d in ('2022-07-26', '2022-08-03', '2024-07-30', '2024-12-10', '2026-03-17', '2026-05-19'):
    _doc(f'aa:{d}-special', f'City Council special meeting annotated agenda, {d}',
         f'phase2/history/sources/council-{d}-special-annotated.pdf', 'annotated_agenda')
_doc('plan:2026-07-07', 'Five-Year Street Rehabilitation and Measure FF Plans FY2027-2031, Council Item 10, July 7, 2026',
     'phase2/sources/street-rehab-measure-ff-2026-07-07.pdf', 'staff_report')
_doc('ptap25', 'City of Berkeley 2024 Pavement Management Program Update (P-TAP 25), April 2025',
     'phase2/sources/pavement-management-update-ptap25-2025-04.pdf', 'city_assessment')
_doc('budget:2026-06-23', 'Adoption of FY2027-28 Biennial Budget and FY2027-31 CIP, June 23, 2026',
     'phase2/sources/budget-adoption-2026-06-23.pdf', 'adopted_budget')
_doc('loan:2023-07-25', '$5.5M Loan for D and E Dock Replacement Project, Council Item 19, July 25, 2023 (staff report)',
     'phase2/sources/council-2023-07-25-item19-wc-loan.pdf', 'staff_report')
for y, f, url in [(2012, 'mtc-pci-2012', 'https://mtc.ca.gov/sites/default/files/PCI_12.pdf'),
                  (2015, 'mtc-pci-2015', 'https://es.mtc.ca.gov/sites/default/files/PCI_15.pdf'),
                  (2016, 'mtc-pci-2016', 'https://es.mtc.ca.gov/sites/default/files/PCI_16.pdf'),
                  (2019, 'mtc-pci-2019', 'https://zh-tw.mtc.ca.gov/sites/default/files/PCI_table_2019_data.pdf'),
                  (2020, 'mtc-pci-2020', 'https://zh-tw.mtc.ca.gov/sites/default/files/documents/2021-11/PCI_table-2020_data.pdf'),
                  (2021, 'mtc-pci-2021', 'https://zh-tw.mtc.ca.gov/sites/default/files/documents/2022-11/PCI_table-2021_data.pdf'),
                  (2022, 'mtc-pci-2022', 'https://es.mtc.ca.gov/sites/default/files/documents/2023-11/PCI_table-2022_data.pdf')]:
    _doc(f'mtc:{y}', f'Metropolitan Transportation Commission, Pavement Condition Index table, {y} edition',
         f'phase2/history/sources/mtc/{f}.pdf', 'regional_dataset', url)


def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-')
    return re.sub(r'\s+', ' ', s).strip().lower()


@lru_cache(maxsize=None)
def page_count(doc):
    out = subprocess.run(['pdfinfo', str(REPO / DOCS[doc]['local'])], capture_output=True, text=True, check=True).stdout
    return int(re.search(r'^Pages:\s+(\d+)', out, re.M).group(1))


@lru_cache(maxsize=None)
def page_text(doc, page):
    parts = [subprocess.run(['pdftotext', *m, '-f', str(page), '-l', str(page), str(REPO / DOCS[doc]['local']), '-'],
                            capture_output=True, text=True, check=True).stdout for m in ([], ['-layout'])]
    return norm(' \n '.join(parts))


def cite(doc, page, quote):
    return {'doc_id': doc, 'pdf_page': page, 'quote': quote}


def verified(value, *cites, note=None):
    return {'status': 'verified', 'value': value, 'citations': list(cites), 'note': note}


def to_collect(what, where=None):
    return {'status': 'to_collect', 'value': None, 'needed': what, 'where_to_look': where}


def not_in_record(what):
    return {'status': 'not_in_record', 'value': None, 'needed': what}


# ------------------------------------------------------------------ the storyboard: 14 proposed events
# kind: council_decision | voter_decision | council_direction | context. Only council_decision and council_direction
# carry votes. Members are as printed in the annotated agenda; "All Ayes" is not expanded into names.

def events():
    E = []

    def ev(**k):
        k.setdefault('retrospective_scenarios', [])
        E.append(k)

    ev(id='bdh-streets-2012-11-measure-m', date='2012-11-06', date_precision='election day', kind='voter_decision',
       title='Voters approve Measure M, a street and watershed improvement bond',
       decision=verified('Measure M (November 2012), Street and Integrated Watershed Improvements General Obligation '
                         'Bonds. The City still sets a tax rate each year to pay its debt service.',
                         cite('aa:2026-06-16', 7, 'Improvements General Obligation Bonds (Measure M, November 2012 Election)')),
       instrument=to_collect('Council resolution placing Measure M on the November 2012 ballot, and its number',
                             'City Clerk records archive (pre-2021 annotated agendas are not on the current City site)'),
       vote=to_collect('Council roll-call vote placing Measure M on the ballot', 'City Clerk records archive, 2012'),
       money=to_collect('Bond amount authorized and amounts issued', 'Measure M ballot text; bond official statements'),
       purpose=to_collect('Stated purpose and expected outcomes in the ballot measure', 'November 2012 ballot pamphlet'),
       alternatives=to_collect('Alternatives presented to Council in 2012', 'Council staff report, 2012'),
       actual=to_collect('Measure M expenditures by project', 'Measure M completion or oversight reports'),
       outcomes=to_collect('Miles paved and green infrastructure built with Measure M funds', 'Public Works reports'),
       outstanding=verified('Debt service continues: Council set the FY2027 Measure M tax rate at 0.0040%.',
                            cite('aa:2026-06-16', 7, 'General Obligation Bonds (Measure M, November 2012) at 0.0040%')),
       uncertainties=['Bond amount, project list and results are not yet in BeTH\'s records.'])

    ev(id='bdh-streets-2016-11-measure-t1', date='2016-11-08', date_precision='election day', kind='voter_decision',
       title='Voters approve Measure T1, an infrastructure and facilities bond',
       decision=verified('Measure T1 (November 2016), Infrastructure and Facilities Improvements General Obligation '
                         'Bonds. The City still sets a tax rate each year to pay its debt service.',
                         cite('aa:2026-06-16', 5, 'General Obligation Bonds (Measure T1, November 2016 Election)')),
       instrument=to_collect('Council resolution placing Measure T1 on the ballot', 'City Clerk records archive, 2016'),
       vote=to_collect('Council roll-call vote placing Measure T1 on the ballot', 'City Clerk records archive, 2016'),
       money=to_collect('Bond amount authorized; phases issued; share spent on streets', 'Measure T1 program reports'),
       purpose=to_collect('Stated purpose and project lists for each phase', 'Ballot pamphlet; Phase 1 and 2 project lists'),
       alternatives=to_collect('Alternatives presented in 2016', 'Council staff report, 2016'),
       actual=to_collect('Measure T1 street expenditures by year', 'Measure T1 status reports'),
       outcomes=verified('In November 2023 Council directed that the Hopkins Street segments be completed "with Measure '
                         'T1 funds by the end of FY 2027".',
                         cite('aa:2023-11-28', 9, 'complete the Hopkins Street segments with Measure T1 funds by the end of FY 2027')),
       outstanding=verified('Debt service continues: Council set the FY2027 Measure T1 tax rate at 0.0140%.',
                            cite('aa:2026-06-16', 5, 'Obligation Bonds (Measure T1, November 2016) at 0.0140%')),
       uncertainties=['How much of Measure T1 went to streets, and what it delivered, is not yet in BeTH\'s records.'])

    ev(id='bdh-streets-2020-auditor-rocky-road', date='2020', date_precision='year (to confirm)', kind='context',
       title='City Auditor: "Rocky Road: Berkeley Streets at Risk and Significantly Underfunded"',
       decision=verified('The City Auditor\'s streets audit. In December 2024 Council received a status report on it '
                         '("Received and filed").',
                         cite('aa:2024-12-10', 11, 'Rocky Road: Berkeley Streets at Risk and Significantly Underfunded'),
                         note='The audit\'s own date and findings are to be collected; the year shown is provisional.'),
       instrument=not_in_record('An audit is not a Council decision; there is no resolution.'),
       vote=not_in_record('Not a vote.'),
       money=not_in_record('The audit report states its own estimates; not yet collected.'),
       purpose=to_collect('Audit findings and recommendations', 'City Auditor report, 2020; status reports 2022-2024'),
       alternatives=not_in_record('Not applicable.'),
       actual=to_collect('Status of each recommendation', 'Audit status reports, including December 10, 2024'),
       outcomes=to_collect('Which recommendations were implemented', 'Audit status reports'),
       outstanding=to_collect('Open recommendations', 'City Auditor follow-up'),
       uncertainties=['The audit report itself is not yet in BeTH\'s records.'])

    ev(id='bdh-streets-2022-01-25-res-70204', date='2022-01-25', kind='council_decision', item='Action Calendar Aa',
       title='Council updates the Street Maintenance and Rehabilitation Policy and adopts the Five-Year Paving Plan (Equity Alternative)',
       decision=verified('Adopted Resolution No. 70,204-N.S. updating the Street Maintenance and Rehabilitation Policy and '
                         'the Five-Year Paving Plan "Equity Alternative", amended to approve the first three years of the '
                         'plan, with the condition that its criteria would not govern funds from potential future ballot '
                         'measures; staff to return in January 2024.',
                         cite('aa:2022-01-25', 7, 'to adopt Resolution No. 70,204'),
                         cite('aa:2022-01-25', 7, 'Paving Plan Equity Alternative amended to approve the first three years of the plan')),
       instrument=verified({'kind': 'resolution', 'number': '70,204-N.S.'}, cite('aa:2022-01-25', 7, 'Resolution No. 70,204')),
       vote=verified({'mover': 'Arreguin', 'seconder': 'Harrison', 'recorded': 'All Ayes',
                      'present_at_roll_call': ['Kesarwani', 'Taplin', 'Harrison', 'Hahn', 'Wengraf', 'Robinson', 'Droste', 'Arreguin'],
                      'arrivals': ['Bartlett present at 6:06 p.m.'], 'ayes': None, 'noes': None, 'abstain': None, 'absent': None},
                     cite('aa:2022-01-25', 7, 'M/S/C (Arreguin/Harrison)'),
                     cite('aa:2022-01-25', 2, 'Councilmember Bartlett present at 6:06 p.m.')),
       money=not_in_record('The annotated agenda states no amount; the plan\'s funding levels are in the staff report, to collect.'),
       purpose=to_collect('Policy goals and the plan\'s expected results', 'January 18/25, 2022 staff report'),
       alternatives=verified('Documented at the time: the Public Works Commission recommended a different plan, version 12A '
                             '("Arterial Alternative"), and a Councilmember-authored policy update was also on the agenda. '
                             'Council adopted the Equity Alternative instead.',
                             cite('aa:2022-01-25', 7, 'Five-Year Paving Plan version 12A')),
       actual=to_collect('Paving delivered under this plan, by year', 'Public Works paving reports'),
       outcomes=to_collect('Whether the January 2024 policy update came back as directed', 'Council agendas, 2024'),
       outstanding=not_in_record('No financial commitment stated in the record we hold.'),
       uncertainties=['The record does not list individual names for "All Ayes" votes.'])

    ev(id='bdh-streets-2022-07-26-res-70456', date='2022-07-26', kind='council_decision', item='Special meeting, Action 3',
       title='Council commits $8 million a year more of General Fund money to street maintenance',
       decision=verified('Adopted Resolution No. 70,456-N.S., a fiscal policy allocating $8 million a year from the General '
                         'Fund to street maintenance on top of the existing $7.3 million, $15.3 million in all, adjusted for '
                         'inflation. It may be suspended in a year Council draws $1 million or more from the Stabilization '
                         'Reserve to adopt a budget, or by a two-thirds vote of Council.',
                         cite('aa:2022-07-26-special', 4, 'to adopt Resolution No. 70,456'),
                         cite('aa:2022-07-26-special', 4, 'existing General Fund street paving budget of $7.3 million'),
                         cite('aa:2022-07-26-special', 4, 'a two-thirds vote of the City Council')),
       instrument=verified({'kind': 'resolution', 'number': '70,456-N.S.'}, cite('aa:2022-07-26-special', 4, 'Resolution No. 70,456')),
       vote=verified({'mover': 'Wengraf', 'seconder': 'Arreguin', 'recorded': 'All Ayes',
                      'present_at_roll_call': ['Taplin', 'Harrison', 'Hahn', 'Wengraf', 'Robinson', 'Droste', 'Arreguin'],
                      'arrivals': ['Kesarwani present at 3:07 p.m.', 'Bartlett present at 3:21 p.m.'],
                      'ayes': None, 'noes': None, 'abstain': None, 'absent': None},
                     cite('aa:2022-07-26-special', 4, 'M/S/C (Wengraf/Arreguin)'),
                     cite('aa:2022-07-26-special', 2, 'Councilmember Bartlett present at 3:21 p.m.')),
       money=verified({'amount': 8000000, 'basis': 'policy commitment (annual, inflation-adjusted)', 'source': 'General Fund',
                       'total_target': 15300000},
                      cite('aa:2022-07-26-special', 4, 'allocate $8 million annually in General Fund monies for street maintenance')),
       purpose=verified('"This policy is needed to ensure that deferred street maintenance is supported by an ongoing '
                        'adequate General Fund contribution."',
                        cite('aa:2022-07-26-special', 4, 'ensure that deferred street maintenance is supported by an')),
       alternatives=verified('Documented at the time: the policy itself sets two ways to suspend it (a Stabilization '
                             'Reserve draw of $1 million or more, or a two-thirds vote). No alternative funding level was '
                             'voted on in the record we hold.',
                             cite('aa:2022-07-26-special', 4, 'a two-thirds vote of the City Council')),
       actual=to_collect('General Fund paving appropriations and actual expenditures each year since FY2023',
                         'Adopted budgets FY2023-FY2026; CIP actuals'),
       outcomes=verified('City staff (July 2026): about 29.4 centerline miles paved in FY2024-FY2026, against a historical '
                         'average of about 2 to 3 miles a year, an acceleration staff attribute to "the commitment of '
                         'additional General Fund resources in 2022". This is the City\'s attribution, not a BeTH finding.',
                         cite('plan:2026-07-07', 5, 'This acceleration was made possible by the commitment of additional General Fund')),
       outstanding=verified('Carried into Measure FF: voters made the $15.3 million (inflation-adjusted) non-FF street '
                            'budget a condition of collecting the tax (BMC 7.11.030(B)).',
                            cite('plan:2026-07-07', 3, 'Adequate General Fund Contribution')),
       uncertainties=['Whether every year since FY2023 met the $15.3 million (adjusted) level is not yet established.',
                      'The record does not list individual names for "All Ayes" votes; two members arrived after roll call '
                      'and the agenda does not say whether they were present for this item.'])

    ev(id='bdh-streets-2022-08-03-res-70492-measure-l', date='2022-08-03', kind='council_decision', item='Special meeting, Item 2',
       title='Council places a $650 million housing and infrastructure bond on the November 2022 ballot',
       decision=verified('Adopted Resolution No. 70,492-N.S. placing a $650 million general obligation bond "to create '
                         'affordable housing; repair streets and sidewalks; underground utilities; and enhance buildings, '
                         'infrastructure, and safety" on the November 8, 2022 ballot.',
                         cite('aa:2022-08-03-special', 3, 'Adopt Resolution No. 70,492'),
                         cite('aa:2022-08-03-special', 3, 'repair streets and sidewalks')),
       instrument=verified({'kind': 'resolution', 'number': '70,492-N.S.'}, cite('aa:2022-08-03-special', 3, 'Resolution No. 70,492')),
       vote=verified({'mover': 'Arreguin', 'seconder': 'Kesarwani', 'recorded': 'roll call',
                      'ayes': ['Kesarwani', 'Taplin', 'Bartlett', 'Harrison', 'Hahn', 'Wengraf', 'Robinson', 'Arreguin'],
                      'noes': [], 'abstain': [], 'absent': ['Droste']},
                     cite('aa:2022-08-03-special', 3, 'Ayes - Kesarwani, Taplin, Bartlett, Harrison, Hahn, Wengraf, Robinson, Arreguin; Noes - None; Abstain - None; Absent - Droste')),
       money=verified({'amount': 650000000, 'basis': 'ballot authorization (not appropriated)', 'source': 'general obligation bonds'},
                      cite('aa:2022-08-03-special', 3, 'the issuance of $650 million in general obligation bonds')),
       purpose=verified('Affordable housing, climate resiliency, wildfire protection and other public infrastructure, '
                        'including street and sidewalk repair.',
                        cite('aa:2022-08-03-special', 3, 'climate change resiliency, wildfire protection')),
       alternatives=verified('Documented at the time: the recommendation offered $600 million or $650 million; the July 26, '
                             '2022 item had proposed $300 million before Council asked for a revised measure.',
                             cite('aa:2022-08-03-special', 3, 'obligation bond in the amount of either $600 million or $650 million')),
       actual=not_in_record('A ballot authorization is not an expenditure.'),
       outcomes=to_collect('November 8, 2022 election result for this measure', 'Alameda County Registrar of Voters; '
                           'Council resolution confirming results'),
       outstanding=to_collect('Whether any bonds were issued', 'Depends on the election result'),
       uncertainties=['The election result is not yet in BeTH\'s records.'])

    ev(id='bdh-streets-2023-07-25-res-70997', date='2023-07-25', kind='council_decision', item='Consent Calendar 19',
       title='Council authorizes a $5.5 million internal loan for Marina dock replacement',
       decision=verified('Adopted Resolution No. 70,997-N.S. authorizing an internal loan of $5.5 million from the Workers\' '
                         'Compensation Fund, to be repaid from waterfront hotel tax starting in FY2025.',
                         cite('aa:2023-07-25', 12, 'Adopted Resolution No. 70,997'),
                         cite('aa:2023-07-25', 12, 'authorizes an internal loan of $5.5M from the Workers Compensation Fund')),
       instrument=verified({'kind': 'resolution', 'number': '70,997-N.S.'}, cite('aa:2023-07-25', 12, 'Resolution No. 70,997')),
       vote=verified({'mover': 'Arreguin', 'seconder': 'Hahn', 'recorded': 'roll call (Consent Calendar, one motion)',
                      'ayes': ['Kesarwani', 'Taplin', 'Bartlett', 'Hahn', 'Wengraf', 'Robinson', 'Humbert', 'Arreguin'],
                      'noes': [], 'abstain': [], 'absent': ['Harrison']},
                     cite('aa:2023-07-25', 3, 'Ayes - Kesarwani, Taplin, Bartlett, Hahn, Wengraf, Robinson, Humbert, Arreguin; Noes - None; Abstain - None; Absent - Harrison')),
       money=verified({'amount': 5500000, 'basis': 'loan authorization (not revenue, not an expenditure)',
                       'source': 'Workers\' Compensation Fund'},
                      cite('aa:2023-07-25', 12, 'authorizes an internal loan of $5.5M')),
       purpose=verified('Replace the Marina\'s D and E docks.', cite('aa:2023-07-25', 12, '$5.5M Loan for D and E Dock Project In Berkeley Marina')),
       alternatives=verified('Documented at the time: amend the existing $5.5 million State boating loan under one of four '
                             'options, or borrow internally. Council chose the internal loan.',
                             cite('aa:2023-07-25', 12, 'execute an Amendment to the existing $5.5M Loan')),
       actual=verified('The FY2024 audit records $5,500,000 leaving the Workers\' Compensation Fund to the General Fund; '
                       'the Marina Fund recorded no transfer in. See the Ask BeTH Marina answer.',
                       note='Detailed citations in phase2/flags/2026-10-25-marina-608-ledger-review.md.'),
       outcomes=to_collect('Dock replacement status and cost', 'Marina capital project reports'),
       outstanding=to_collect('Loan balance and repayments from waterfront hotel tax', 'Workers\' Compensation Fund ledger'),
       uncertainties=['Whether the loan reached the Marina Fund, and whether repayment has begun, is unresolved.'])

    ev(id='bdh-streets-2023-11-28-res-71120', date='2023-11-28', kind='council_decision', item='Action Calendar 17',
       title='Council adopts the Five-Year Street Rehabilitation Plan, FY2024-2028, after a competing motion fails',
       decision=verified('Adopted Resolution No. 71,120-N.S. adopting the staff plan with Milvia Street (Hearst to Rose) '
                         'added and the Hopkins Street segments to be completed with Measure T1 funds by the end of FY2027; '
                         'green infrastructure and holdover-list questions referred to committee.',
                         cite('aa:2023-11-28', 9, '71,120')),
       instrument=verified({'kind': 'resolution', 'number': '71,120-N.S.'}, cite('aa:2023-11-28', 9, '71,120')),
       vote=verified({'mover': 'Humbert', 'seconder': 'Robinson', 'recorded': 'All Ayes',
                      'present_at_roll_call': ['Taplin', 'Bartlett', 'Harrison', 'Hahn', 'Wengraf', 'Robinson', 'Humbert', 'Arreguin'],
                      'arrivals': ['Kesarwani present at 6:39 p.m.'], 'ayes': None, 'noes': None, 'abstain': None, 'absent': None},
                     cite('aa:2023-11-28', 9, 'M/S/Carried (Humbert/Robinson)'),
                     cite('aa:2023-11-28', 2, 'Councilmember Kesarwani present at 6:39 p.m.')),
       failed_motions=[verified({'mover': 'Hahn', 'seconder': 'Wengraf', 'result': 'failed',
                                 'text': 'Adopt the plan with Milvia added, add Hopkins Street (The Alameda to Gilman) to the '
                                         'FY2025 list, refer green infrastructure and holdover issues to committee, and '
                                         'direct a parking management analysis around the Hopkins corridor.',
                                 'ayes': ['Bartlett', 'Hahn', 'Wengraf', 'Arreguin'],
                                 'noes': ['Kesarwani', 'Taplin', 'Harrison', 'Robinson', 'Humbert'], 'abstain': [], 'absent': []},
                                cite('aa:2023-11-28', 9, 'M/S/Failed (Hahn/Wengraf)'),
                                cite('aa:2023-11-28', 9, 'Ayes - Bartlett, Hahn, Wengraf, Arreguin; Noes - Kesarwani, Taplin, Harrison, Robinson, Humbert'))],
       money=to_collect('Plan funding by year and source', 'November 28, 2023 staff report'),
       purpose=to_collect('Streets selected and expected miles', 'November 28, 2023 staff report'),
       alternatives=verified('Documented at the time: the Hahn/Wengraf motion (below), which failed 4-5.',
                             cite('aa:2023-11-28', 9, 'M/S/Failed (Hahn/Wengraf)')),
       actual=verified('City staff report centerline miles paved: 10.7 in FY2024 and 8.4 in FY2025; 10.3 projected for '
                       'FY2026. Some streets were deferred to coordinate with Claremont, Oxford and Telegraph projects.',
                       cite('plan:2026-07-07', 5, 'FY 2024 10.7'), cite('plan:2026-07-07', 5, 'FY 2025 8.4'),
                       cite('plan:2026-07-07', 5, 'Several streets from the FY 2024-2028 plan have been deferred')),
       outcomes=to_collect('Whether the Hopkins segments are on track for FY2027', 'Public Works project status'),
       outstanding=verified('Hopkins Street segments to be completed with Measure T1 funds by the end of FY2027.',
                            cite('aa:2023-11-28', 9, 'complete the Hopkins Street segments with Measure T1 funds by the end of FY 2027')),
       uncertainties=['The record does not list individual names for the final "All Ayes" vote.'])

    ev(id='bdh-streets-2024-07-30-res-71461-measure-ff', date='2024-07-30', kind='council_decision', item='Special meeting',
       title='Council sends the SAFE STREETS parcel tax (Measure FF) to voters',
       decision=verified('Adopted Resolution No. 71,461-N.S. submitting the citizens\' initiative, without alteration, to '
                         'the November 5, 2024 election.',
                         cite('aa:2024-07-30-special', 2, 'Adopt Resolution No. 71,461')),
       instrument=verified({'kind': 'resolution', 'number': '71,461-N.S.'}, cite('aa:2024-07-30-special', 2, 'Resolution No. 71,461')),
       vote=verified({'mover': 'Arreguin', 'seconder': 'Taplin', 'recorded': 'All Ayes',
                      'present_at_roll_call': ['Taplin', 'Tregub', 'Hahn', 'Wengraf', 'Lunaparra', 'Humbert', 'Arreguin'],
                      'arrivals': ['Kesarwani present at 3:16 p.m.', 'Bartlett present at 3:36 p.m.'],
                      'ayes': None, 'noes': None, 'abstain': None, 'absent': None},
                     cite('aa:2024-07-30-special', 2, 'M/S/C (Arreguin/Taplin)'),
                     cite('aa:2024-07-30-special', 2, 'Vote: All Ayes')),
       money=not_in_record('A ballot placement appropriates nothing.'),
       purpose=verified('Repairs and improvements to streets, sidewalks and pedestrian paths.',
                        cite('aa:2024-07-09', 10, 'Improvements to Streets, Sidewalks, and Pedestrian Paths (SAFE STREETS)')),
       alternatives=verified('Documented at the time: for an initiative, Council could adopt the measure itself without '
                             'alteration, or submit it to voters. Council submitted it.',
                             cite('aa:2024-07-09', 10, 'Adopt the provisions of the measure without alteration')),
       actual=not_in_record('See the following event.'),
       outcomes=verified('Approved by voters; Council adopted Ordinance No. 7,952-N.S. on December 10, 2024 (next event).',
                         cite('aa:2024-12-10-special', 3, 'Ordinance No. 7,952-N.S. (Measure FF')),
       outstanding=not_in_record('See the following event.'),
       uncertainties=['The record does not list individual names for "All Ayes" votes.'])

    ev(id='bdh-streets-2024-12-10-ord-7952', date='2024-12-10', kind='voter_decision', item='Special meeting, Item 1',
       title='Measure FF results confirmed; Ordinance No. 7,952-N.S. adopted',
       decision=verified('Council confirmed the November 5, 2024 election results and adopted Ordinance No. 7,952-N.S. '
                         '(Measure FF, the SAFE STREETS parcel tax).',
                         cite('aa:2024-12-10-special', 3, 'Ordinance No. 7,952-N.S. (Measure FF')),
       instrument=verified({'kind': 'ordinance', 'number': '7,952-N.S.'}, cite('aa:2024-12-10-special', 3, '7,952-N.S.')),
       vote=to_collect('Vote confirming the results', 'Same annotated agenda; confirming results is ministerial'),
       money=verified({'amount': None, 'basis': 'special parcel tax, 14 years; FY2027 revenue projected $16,651,651',
                       'source': 'Measure FF'}, note='See the Ask BeTH Measure FF answer for the cited revenue figure.'),
       purpose=verified('Approximately 45% streets, 15% sidewalks and paths, 30% safety, 10% environmental and other '
                        'uses; goal of PCI 70 "ideally with no streets having a PCI below 50" by 2036.',
                        note='Citations in the Ask BeTH Measure FF answer (BMC 7.11.010(K)(1), 7.11.020(C)).'),
       alternatives=not_in_record('Voters decided; see the July 30, 2024 event for Council\'s documented options.'),
       actual=to_collect('Measure FF receipts and spending, FY2025-FY2026', 'FY2026 ACFR; Measure FF annual report'),
       outcomes=to_collect('First Measure FF annual report (streets paved, cost per mile, PCI)', 'BMC 7.11.050 report'),
       outstanding=verified('Five-year Measure FF program adopted July 7, 2026 (later event).',
                            note='See the July 7, 2026 event for its citation.'),
       uncertainties=['Election vote totals are not yet in BeTH\'s records.'])

    ev(id='bdh-streets-2026-03-17-bond-direction', date='2026-03-17', kind='council_direction', item='Special meeting, Item 1',
       title='Council directs staff to draft a $300 million infrastructure bond and a sales tax measure',
       decision=verified('Approved the recommendation to prepare draft ballot language for a potential $300 million general '
                         'obligation bond for infrastructure and a 0.5 percent sales tax increase, and to run a second '
                         'voter survey.',
                         cite('aa:2026-03-17-special', 2, 'potential $300 million General Obligation bond measure')),
       instrument=not_in_record('Direction by motion; no resolution number.'),
       vote=verified({'mover': 'Ishii', 'seconder': 'Taplin', 'recorded': 'All Ayes', 'ayes': None, 'noes': None,
                      'abstain': None, 'absent': None},
                     cite('aa:2026-03-17-special', 2, 'M/S/C (Ishii/Taplin) to approve the recommendation')),
       money=verified({'amount': 300000000, 'basis': 'potential ballot authorization (direction only)', 'source': 'general obligation bonds'},
                      cite('aa:2026-03-17-special', 2, 'potential $300 million General Obligation bond measure')),
       purpose=verified('"to fund priority infrastructure investments"',
                        cite('aa:2026-03-17-special', 2, 'ballot to fund priority infrastructure investments')),
       alternatives=to_collect('Survey options and bond sizes considered', 'March 17, 2026 staff report and survey'),
       actual=not_in_record('Direction only.'),
       outcomes=verified('Affirmed on May 19, 2026 (All Ayes).',
                         cite('aa:2026-05-19-special', 2, 'Affirm the direction to prepare ballot language for a potential $300 million General')),
       outstanding=to_collect('The Council resolution placing the bond on the November 3, 2026 ballot, its vote, and the '
                              'project list', 'Council annotated agendas, June-August 2026'),
       uncertainties=['BeTH has not yet located the final placement resolution or its vote.'])

    ev(id='bdh-streets-2026-06-23-res-72340-budget', date='2026-06-23', kind='council_decision', item='Special meeting',
       title='Council adopts the FY2027-28 budget and FY2027-31 capital program, after a competing budget motion fails',
       decision=verified('Adopted Resolution No. 72,340-N.S. adopting the FY2027-28 biennial budget and the FY2027-2031 '
                         'Capital Improvement Program, with the Mayor\'s recommendations as revised at the meeting.',
                         cite('aa:2026-06-23', 3, '72,340')),
       instrument=verified({'kind': 'resolution', 'number': '72,340-N.S.'}, cite('aa:2026-06-23', 3, '72,340')),
       vote=verified({'mover': 'Humbert', 'seconder': 'Tregub', 'recorded': 'All Ayes',
                      'present_at_roll_call': ['Kesarwani', 'Taplin', 'Bartlett', 'Tregub', "O'Keefe", 'Blackaby',
                                               'Lunaparra', 'Humbert', 'Ishii'], 'arrivals': [],
                      'ayes': None, 'noes': None, 'abstain': None, 'absent': None},
                     cite('aa:2026-06-23', 3, 'M/S/Carried (Humbert/Tregub)')),
       failed_motions=[verified({'mover': 'Kesarwani', 'seconder': 'Blackaby', 'result': 'failed',
                                 'text': 'Adopt the budget with the Mayor\'s allocations except that $2,500,000 would be '
                                         'retained for Small Sites and $1,300,000 in the Housing Trust Fund.',
                                 'ayes': ['Kesarwani', 'Taplin', 'Blackaby'],
                                 'noes': ['Bartlett', 'Tregub', "O'Keefe", 'Lunaparra', 'Ishii'],
                                 'abstain': ['Humbert'], 'absent': []},
                                cite('aa:2026-06-23', 2, 'M/S/Failed (Kesarwani/Blackaby)'),
                                cite('aa:2026-06-23', 3, 'Ayes - Kesarwani, Taplin, Blackaby; Noes - Bartlett, Tregub, O\'Keefe'))],
       money=verified({'amount': 139356147, 'basis': 'adopted five-year Streets CIP (FY2027-28 appropriated; FY2029-31 planned)',
                       'source': 'multiple (see Ask BeTH: streets figure)'},
                      cite('budget:2026-06-23', 216, '$139,356,147 in Five-Year CIP Budget')),
       purpose=to_collect('Budget priorities stated by the City Manager and Mayor', 'Budget message; Mayor\'s recommendations'),
       alternatives=verified('Documented at the time: the Kesarwani/Blackaby budget motion, which failed 3-5 with one '
                             'abstention. Four transportation studies were moved to "unfunded and pending".',
                             cite('aa:2026-06-23', 2, 'M/S/Failed (Kesarwani/Blackaby)'),
                             cite('aa:2026-06-23', 3, 'Citywide Traffic Signal Master Plan')),
       actual=to_collect('FY2027 actual street spending', 'FY2027 ACFR (late 2027)'),
       outcomes=not_in_record('Too recent.'),
       outstanding=verified('FY2029-FY2031 street amounts are plans, not appropriations.',
                            note='See the Ask BeTH streets-figure answer.'),
       uncertainties=['The record does not list individual names for the final "All Ayes" vote.'])

    ev(id='bdh-streets-2026-07-07-res-72377', date='2026-07-07', kind='council_decision', item='Action Calendar 10',
       title='Council adopts the Five-Year Street Rehabilitation and Measure FF plans, FY2027-2031',
       decision=verified('Adopted Resolution No. 72,377-N.S. adopting both five-year plans, noting several transportation '
                         'studies as preliminary Measure FF safety projects subject to the SAFE STREETS oversight committee '
                         'and Council.',
                         cite('aa:2026-07-07', 9, '72,377')),
       instrument=verified({'kind': 'resolution', 'number': '72,377-N.S.'}, cite('aa:2026-07-07', 9, '72,377')),
       vote=verified({'mover': 'Humbert', 'seconder': 'Tregub', 'recorded': 'All Ayes',
                      'present_at_roll_call': ['Kesarwani', 'Taplin', 'Tregub', "O'Keefe", 'Blackaby', 'Lunaparra',
                                               'Humbert', 'Ishii'],
                      'arrivals': ['Bartlett present at 6:12 p.m.'], 'ayes': None, 'noes': None, 'abstain': None, 'absent': None},
                     cite('aa:2026-07-07', 9, 'M/S/C (Humbert/Tregub)'),
                     cite('aa:2026-07-07', 2, 'Councilmember Bartlett present at 6:12 p.m.')),
       money=verified({'amount': 96336212, 'basis': 'five-year paving plan funding (planned)', 'source': 'seven sources'},
                      cite('plan:2026-07-07', 3, '$96,336,212')),
       purpose=verified('City projection: the paving plan plus Measure FF raises citywide PCI to about 62 by 2038; neither '
                        'scenario reaches 70 within 12 years.',
                        cite('plan:2026-07-07', 12, 'the citywide PCI is projected to improve to approximately 62 by 2038')),
       alternatives=verified('Documented at the time: the City modeled funding scenarios and two ways of choosing Measure FF '
                             'streets (PCI below 50 versus cost-effectiveness).',
                             cite('plan:2026-07-07', 13, 'PCI Under 50')),
       actual=not_in_record('Too recent.'),
       outcomes=not_in_record('Too recent.'),
       outstanding=verified('Five years of planned paving and Measure FF projects; see the Ask BeTH street pages.',
                            note='Plan totals and street lists are cited in the Ask BeTH street answers.'),
       uncertainties=['The record does not list individual names for "All Ayes" votes.'])

    ev(id='bdh-streets-2026-11-bond-ballot', date='2026-11-03', date_precision='election day (pending)', kind='voter_decision',
       title='A $300 million infrastructure bond goes to voters (pending)',
       decision=to_collect('The placement resolution and final ballot question', 'Council annotated agendas, June-August 2026'),
       instrument=to_collect('Resolution number', 'Same'), vote=to_collect('Council vote placing the measure', 'Same'),
       money=verified({'amount': 300000000, 'basis': 'potential ballot authorization', 'source': 'general obligation bonds'},
                      cite('aa:2026-05-19-special', 2, 'potential $300 million General')),
       purpose=to_collect('Project list', 'Ballot resolution exhibit'),
       alternatives=to_collect('Alternatives considered, including Vision 2050 recommendations raised by residents',
                               'Council materials; public communications'),
       actual=not_in_record('Pending.'), outcomes=not_in_record('Pending.'), outstanding=not_in_record('Pending.'),
       uncertainties=['Election on November 3, 2026.'])
    return E


# ------------------------------------------------------------------ outcome series

def outcomes():
    mtc = [  # (year, value, edition) 3-year moving averages, Berkeley row, as printed in each edition
        (2010, 60, 2012, 1), (2011, 59, 2012, 1), (2012, 59, 2012, 1),
        (2013, 58, 2015, 4), (2014, 58, 2015, 4), (2015, 58, 2015, 4),
        (2014, 58, 2016, 5), (2015, 58, 2016, 5), (2016, 58, 2016, 5),
        (2017, 57, 2019, 5), (2018, 58, 2019, 5), (2019, 57, 2019, 5),
        (2018, 57, 2020, 5), (2019, 57, 2020, 5), (2020, 58, 2020, 5),
        (2019, 57, 2021, 5), (2020, 58, 2021, 5), (2021, 57, 2021, 5),
        (2020, 57, 2022, 5), (2021, 58, 2022, 5), (2022, 56, 2022, 5)]
    miles = [('FY2019 (incl. FY2018)', 5.3, 'actual'), ('FY2020', 2.6, 'actual'), ('FY2021', 1.9, 'actual'),
             ('FY2022', 2.6, 'actual'), ('FY2023', 7.0, 'actual'), ('FY2024', 10.7, 'actual'), ('FY2025', 8.4, 'actual'),
             ('FY2026', 10.3, 'projected')]
    return {
        'pci_mtc_3yr_moving_average': {
            'what': 'Metropolitan Transportation Commission, Berkeley, 3-year moving average PCI, as printed in each '
                    'edition. Editions revise earlier years; every printed value is kept with its edition.',
            'method_breaks': ['MTC implemented an improved ASTM D6433 rating standard in 2016 (2016 edition footnote).',
                              'Values are 3-year moving averages, not single-year scores, and are not comparable with '
                              'the City\'s single-year StreetSaver figures.'],
            'points': [{'year': y, 'pci': v, 'edition': ed, 'citation': cite(f'mtc:{ed}', pg, 'Berkeley')}
                       for y, v, ed, pg in mtc],
            'gaps': ['2023 and 2024 editions not yet collected.']},
        'pci_city': {
            'what': 'City figures (single year, StreetSaver).',
            'points': [{'year': 2024, 'pci': 56, 'basis': 'inspection (consultant report)',
                        'citation': cite('ptap25', 5, "the City's overall average PCI is 56")},
                       {'year': 2025, 'pci': 57, 'basis': 'most recent condition assessment (City staff)',
                        'citation': cite('plan:2026-07-07', 11, 'The current citywide PCI is 57')},
                       {'year': 2026, 'pci': 59, 'basis': 'projected after FY2026 work (City staff)',
                        'citation': cite('plan:2026-07-07', 11, 'the projected citywide PCI is 59')}]},
        'centerline_miles_paved': {
            'what': 'Centerline miles paved by fiscal year (City staff, July 2026, Table 2).',
            'points': [{'fy': f, 'miles': m, 'basis': b} for f, m, b in miles],
            'citation': cite('plan:2026-07-07', 5, 'Table 2: Centerline Miles Paved')},
        'annual_paving_spending': {
            'status': 'to_collect',
            'needed': 'Paving appropriations and actual expenditures by fiscal year, FY2010-FY2026, on one basis.',
            'where_to_look': 'Adopted budgets and CIP books; ACFR capital outlay; Public Works paving reports.'},
    }


# ------------------------------------------------------------------ checks

def all_citations(obj):
    if isinstance(obj, dict):
        if set(obj) >= {'doc_id', 'pdf_page', 'quote'}:
            yield obj
        for v in obj.values():
            yield from all_citations(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from all_citations(v)


def check(evs, outs):
    problems = []
    for c in all_citations({'e': evs, 'o': outs}):
        d = c['doc_id']
        if d not in DOCS:
            problems.append(f'unknown document {d}')
            continue
        if not (REPO / DOCS[d]['local']).exists():
            problems.append(f'missing file {DOCS[d]["local"]}')
            continue
        if not 1 <= c['pdf_page'] <= page_count(d):
            problems.append(f'{d}: PDF p.{c["pdf_page"]} does not exist')
            continue
        if norm(c['quote']) not in page_text(d, c['pdf_page']):
            problems.append(f'{d} p.{c["pdf_page"]}: quote not on page: {c["quote"][:70]}')
    # every plotted MTC value must equal the Berkeley row of its edition (last three numbers = the edition's three years)
    for ed in sorted({pt['edition'] for pt in outs['pci_mtc_3yr_moving_average']['points']}):
        pts = [pt for pt in outs['pci_mtc_3yr_moving_average']['points'] if pt['edition'] == ed]
        pg = pts[0]['citation']['pdf_page']
        lay = subprocess.run(['pdftotext', '-layout', '-f', str(pg), '-l', str(pg), str(REPO / DOCS[f'mtc:{ed}']['local']), '-'],
                             capture_output=True, text=True).stdout
        row = next((l for l in lay.split('\n') if re.match(r'\s*berkeley\s', l, re.I)), None)
        nums = re.findall(r'\b\d+\b', row or '')[-3:]
        want = [str(pt['pci']) for pt in sorted(pts, key=lambda x: x['year'])]
        if nums != want:
            problems.append(f'MTC {ed} edition: Berkeley row ends {nums}, plotted {want}')
    plan_txt = page_text('plan:2026-07-07', outs['centerline_miles_paved']['citation']['pdf_page'])
    for pt in outs['centerline_miles_paved']['points']:
        fy = pt['fy'].split(' ')[0].replace('FY', 'fy ')
        if not re.search(re.escape(fy) + r'(?: \((?:includes fy 20\d\d|projected)\))?\s+' + re.escape(str(pt['miles'])) + r'\b', plan_txt):
            problems.append(f'miles paved {pt["fy"]} = {pt["miles"]} not found in Table 2')
    ids = [e['id'] for e in evs]
    if len(ids) != len(set(ids)):
        problems.append('duplicate event ids')
    for e in evs:
        for k in ('decision', 'instrument', 'vote', 'money', 'purpose', 'alternatives', 'actual', 'outcomes', 'outstanding'):
            f = e.get(k)
            if not f or f.get('status') not in ('verified', 'to_collect', 'not_in_record'):
                problems.append(f'{e["id"]}: field {k} has no status')
            elif f['status'] == 'verified' and not f.get('citations') and not f.get('note'):
                problems.append(f'{e["id"]}: field {k} is verified without a citation or note')
        v = e['vote']
        if v['status'] == 'verified':
            val = v['value']
            if val['recorded'] == 'All Ayes' and any(val.get(k) for k in ('ayes', 'noes', 'abstain', 'absent')):
                problems.append(f'{e["id"]}: "All Ayes" vote must not list inferred names')
        for fm in e.get('failed_motions', []):
            val = fm['value']
            if set(val['ayes']) & set(val['noes']):
                problems.append(f'{e["id"]}: a member is both aye and no')
        if e['kind'] not in ('council_decision', 'council_direction', 'voter_decision', 'context'):
            problems.append(f'{e["id"]}: unknown kind')
        if e.get('retrospective_scenarios'):
            problems.append(f'{e["id"]}: retrospective scenarios must be researched and labelled before inclusion')
    return problems


# ------------------------------------------------------------------ prototype page

QUESTIONS = [('decision', 'What did the Council decide?'), ('vote', 'Who voted for it?'),
             ('purpose', 'What was supposed to happen?'), ('actual', 'What actually happened?'),
             ('alternatives', 'What alternatives were available?'), ('uncertainties', 'What remains uncertain?')]
KIND_LABEL = {'council_decision': 'Council decision', 'council_direction': 'Council direction',
              'voter_decision': 'Voter decision', 'context': 'Context'}
STATUS_LABEL = {'to_collect': 'Record not yet collected', 'not_in_record': 'Not in the record'}
e = html.escape


def doc_link(c):
    d = DOCS[c['doc_id']]
    href = '../../../' + d['local'] + f'#page={c["pdf_page"]}'
    return f'<a href="{e(href)}">{e(d["title"])}, PDF p.{c["pdf_page"]}</a>'


def cites_html(f):
    cs = f.get('citations') or []
    out = ''.join(f'<li>{doc_link(c)}<blockquote>&ldquo;{e(c["quote"])}&rdquo;</blockquote></li>' for c in cs)
    note = f'<p class="note">{e(f["note"])}</p>' if f.get('note') else ''
    return (f'<ul class="cites">{out}</ul>' if out else '') + note


def vote_html(v):
    if v['status'] != 'verified':
        return gap_html(v)
    x = v['value']
    rows = f'<p>Moved by {e(x.get("mover") or "?")}, seconded by {e(x.get("seconder") or "?")}. '
    if x['recorded'] == 'All Ayes':
        rows += ('Recorded as <b>All Ayes</b>. The annotated agenda does not list names for this kind of vote.</p>')
        if x.get('present_at_roll_call'):
            rows += (f'<p class="note">Present at roll call: {e(", ".join(x["present_at_roll_call"]))}'
                     + (f'; {e("; ".join(x["arrivals"]))}' if x.get('arrivals') else '')).rstrip('.') + '.</p>'
    else:
        rows += '</p><div class="votegrid">' + ''.join(
            f'<div><b>{lbl}</b><br>{e(", ".join(x.get(k) or []) or "None")}</div>'
            for k, lbl in (('ayes', 'Ayes'), ('noes', 'Noes'), ('abstain', 'Abstain'), ('absent', 'Absent'))) + '</div>'
    return rows + cites_html(v)


def gap_html(f):
    lbl = STATUS_LABEL.get(f['status'], f['status'])
    where = f'<br><span class="note">Where to look: {e(f["where_to_look"])}</span>' if f.get('where_to_look') else ''
    return f'<p class="gap"><span class="gaptag">{e(lbl)}</span> {e(f.get("needed") or "")}{where}</p>'


def field_html(f):
    if f['status'] != 'verified':
        return gap_html(f)
    val = f['value']
    if isinstance(val, dict):
        if 'number' in val:
            text = f'{val["kind"].capitalize()} No. {val["number"]}'
        elif 'amount' in val:
            amt = f'${val["amount"]:,}' if val.get('amount') else 'No single amount'
            text = f'{amt} · {val.get("basis", "")} · source: {val.get("source", "")}'
        else:
            text = json.dumps(val)
    else:
        text = str(val)
    return f'<p>{e(text)}</p>' + cites_html(f)


def card_html(ev):
    alt = field_html(ev['alternatives'])
    for fm in ev.get('failed_motions', []):
        x = fm['value']
        alt += (f'<div class="failed"><b>Motion that failed</b> ({e(x["mover"])}/{e(x["seconder"])}): {e(x["text"])}'
                + '<div class="votegrid">' + ''.join(
                    f'<div><b>{lbl}</b><br>{e(", ".join(x.get(k) or []) or "None")}</div>'
                    for k, lbl in (('ayes', 'Ayes'), ('noes', 'Noes'), ('abstain', 'Abstain'))) + '</div>'
                + cites_html(fm) + '</div>')
    unc = '<ul class="plain">' + ''.join(f'<li>{e(u)}</li>' for u in ev['uncertainties']) + '</ul>'
    gaps = [k for k in ('decision', 'instrument', 'vote', 'money', 'purpose', 'alternatives', 'actual', 'outcomes', 'outstanding')
            if ev[k]['status'] == 'to_collect']
    if gaps:
        unc += f'<p class="note">Fields with records still to collect: {e(", ".join(gaps))}.</p>'
    body = {'decision': field_html(ev['decision']) + (f'<p class="note">Instrument: {e(field_text(ev["instrument"]))}</p>'),
            'vote': vote_html(ev['vote']),
            'purpose': field_html(ev['purpose']) + f'<p class="note">Money: </p>' + field_html(ev['money']),
            'actual': field_html(ev['actual']) + '<p class="note">Measurable outcomes:</p>' + field_html(ev['outcomes'])
                      + '<p class="note">Outstanding commitments:</p>' + field_html(ev['outstanding']),
            'alternatives': alt + '<p class="note">Retrospective scenarios: none yet. Any added later will be labelled '
                                  'as hindsight, not as options available at the time.</p>',
            'uncertainties': unc}
    year = ev['date'][:4]
    nverified = sum(ev[k]['status'] == 'verified' for k in ('decision', 'instrument', 'vote', 'money', 'purpose',
                                                              'alternatives', 'actual', 'outcomes', 'outstanding'))
    qs = ('<details class="open-card"><summary>Open the record: six questions</summary><div>'
          + ''.join(f'<section class="q"><h4>{i}. {e(q)}</h4>{body[k]}</section>' for i, (k, q) in enumerate(QUESTIONS, 1))
          + '</div></details>')
    return (f'<article class="tl-item" data-kind="{e(ev["kind"])}" id="{e(ev["id"])}">'
            f'<div class="tl-dot" aria-hidden="true"></div><div class="tl-card">'
            f'<div class="tl-meta"><span class="kicker">{e(KIND_LABEL[ev["kind"]])}</span> '
            f'<time datetime="{e(ev["date"])}">{e(ev["date"])}</time>{" · " + e(ev["item"]) if ev.get("item") else ""}</div>'
            f'<h3>{e(ev["title"])}</h3>'
            f'<p class="tl-sum">{e(summary_text(ev))}</p>'
            f'<div class="tl-badges"><span class="pill">{nverified} of 9 fields verified</span>'
            f'<span class="pill no">Not yet reviewed by a person</span></div>{qs}'
            f'<div class="tech"><code>{e(ev["id"])}</code></div></div></article>'), year


def field_text(f):
    if f['status'] != 'verified':
        return STATUS_LABEL[f['status']]
    v = f['value']
    return f'{v["kind"]} No. {v["number"]}' if isinstance(v, dict) and 'number' in v else str(v)


def summary_text(ev):
    d = ev['decision']
    return d['value'] if d['status'] == 'verified' else 'Decision record not yet collected: ' + (d.get('needed') or '')


def charts_html(outs):
    m = outs['centerline_miles_paved']['points']
    top = max(p['miles'] for p in m)
    cols = ''.join(f'<div class="col" title="{e(p["fy"])}: {p["miles"]} miles ({p["basis"]})">'
                   f'<span class="col-v">{p["miles"]}</span><span class="col-f" style="height:{p["miles"] / top * 100:.1f}%;'
                   f'background:{design.BLUE if p["basis"] == "actual" else design.LIGHT_BLUE}"></span>'
                   f'<span class="col-l">{e(p["fy"].replace(" (incl. FY2018)", "*"))}</span></div>' for p in m)
    c = outs['centerline_miles_paved']['citation']
    miles = design.chart('Centerline miles paved each year',
                         'Delivery, as reported by City staff. *FY2019 includes FY2018. FY2026 is projected.',
                         design.legend([('Actual', design.BLUE), ('Projected', design.LIGHT_BLUE)]) + f'<div class="cols">{cols}</div>',
                         f'Source: {DOCS[c["doc_id"]]["title"]}, PDF page {c["pdf_page"]} (Table 2).')
    # PCI: dots on a 50-65 scale (dots, not bars, so the narrow axis does not exaggerate)
    lo, hi = 50, 65
    latest = {}
    for p in outs['pci_mtc_3yr_moving_average']['points']:
        latest.setdefault(p['year'], []).append(p)
    years = list(range(2010, 2027))
    cells = ''
    for y in years:
        dots = ''
        for p in latest.get(y, []):
            pos = (p['pci'] - lo) / (hi - lo) * 100
            dots += (f'<span class="pdot mtc" style="bottom:{pos:.1f}%" title="MTC {y} (3-yr avg, {p["edition"]} edition): '
                     f'{p["pci"]}"></span>')
        for p in outs['pci_city']['points']:
            if p['year'] == y:
                pos = (p['pci'] - lo) / (hi - lo) * 100
                dots += (f'<span class="pdot city{" proj" if "projected" in p["basis"] else ""}" style="bottom:{pos:.1f}%" '
                         f'title="City {y}: {p["pci"]} ({e(p["basis"])})"><b>{p["pci"]}</b></span>')
        vals = sorted({p['pci'] for p in latest.get(y, [])})
        lab = '/'.join(str(v) for v in vals)
        cells += (f'<div class="pcell"><div class="pplot">{dots}</div><div class="pval">{lab}</div>'
                  f'<div class="pyr">{str(y)[2:]}</div></div>')
    pci = design.chart('Citywide pavement condition (PCI), 2010-2026',
                       'Two different measures, not joined: MTC\'s 3-year moving average (blue dots; where editions '
                       'disagree, every printed value is shown) and the City\'s single-year figures (orange; 2026 is a '
                       'projection). MTC changed its rating standard in 2016. Scale 50-65.',
                       design.legend([('MTC, 3-year moving average', design.BLUE), ('City, single year', design.ORANGE)])
                       + f'<div class="pchart">{cells}</div>',
                       'Sources: MTC PCI tables, 2012, 2015, 2016, 2019-2022 editions (Berkeley rows); City 2024 pavement '
                       'report, PDF p.5; July 7, 2026 street plan, PDF p.12. MTC 2023-2024 editions not yet collected.')
    spend = design.chart('Annual paving spending',
                         'Not shown yet: BeTH does not hold a comparable series of paving appropriations and actual '
                         'spending for FY2010-FY2026. Plotting budgets for some years and actuals for others would mislead.',
                         '<p class="gap"><span class="gaptag">Record not yet collected</span> '
                         + e(outs['annual_paving_spending']['needed']) + '</p>',
                         'To collect: ' + outs['annual_paving_spending']['where_to_look'])
    return miles + pci + spend


EXTRA_CSS = '''
.tl-filters{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 18px}
.tl-filters button{border:1px solid var(--rule);background:var(--card);border-radius:999px;padding:5px 12px;font:inherit;font-size:14px;cursor:pointer}
.tl-filters button[aria-pressed="true"]{background:var(--navy);color:#fff;border-color:var(--navy)}
.tl{position:relative;margin:10px 0 0;padding-left:28px}
.tl:before{content:"";position:absolute;left:9px;top:0;bottom:0;width:2px;background:var(--rule)}
.tl-year{font-family:var(--serif);font-size:1.5rem;color:var(--navy);margin:26px 0 8px;position:relative}
.tl-year:before{content:"";position:absolute;left:-25px;top:.55em;width:14px;height:14px;border-radius:50%;background:var(--gold)}
.tl-item{position:relative;margin:12px 0}
.tl-dot{position:absolute;left:-23px;top:20px;width:10px;height:10px;border-radius:50%;background:var(--navy);border:2px solid var(--paper)}
.tl-item[data-kind="voter_decision"] .tl-dot{background:var(--gold)}
.tl-item[data-kind="context"] .tl-dot{background:#9aa3ad}
.tl-card{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:14px 18px}
.tl-meta{font-size:13px;color:var(--muted);display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.tl-meta .kicker{margin:0;font-size:11px}
.tl-card h3{font-family:var(--serif);font-size:1.25rem;margin:6px 0;color:var(--navy)}
.tl-sum{margin:0 0 8px}
.tl-badges{display:flex;flex-wrap:wrap;gap:6px;font-size:13px;margin-bottom:6px}
details.open-card{margin:8px 0 0;border-radius:8px;background:#fbf9f4}
details.open-card>summary{padding:9px 14px;font-weight:650;font-size:15px;color:var(--navy)}
details.open-card>div{padding:0 14px 8px}
section.q{border-top:1px solid var(--rule);padding:10px 0 4px}
section.q h4{margin:0 0 4px;font-size:15px;color:var(--navy)}
.cites{padding-left:1.1em;font-size:14px}
.votegrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;font-size:14px;margin:6px 0}
.votegrid>div{background:#f6f3ec;border-radius:6px;padding:6px 8px}
.failed{border-left:3px solid var(--gold);padding:6px 10px;margin:8px 0;background:#fffaf0;font-size:15px}
.gap{font-size:15px;margin:.4em 0}
.gaptag{display:inline-block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;background:#eef0f3;
color:#4b5563;border-radius:4px;padding:1px 6px;margin-right:4px}
.pchart{display:grid;grid-template-columns:repeat(17,1fr);gap:2px;align-items:end;margin-top:8px}
.pcell{display:flex;flex-direction:column;align-items:center}
.pplot{position:relative;height:150px;width:100%;border-bottom:1px solid #c3c2b7;background:linear-gradient(#efe9dc 1px,transparent 1px) 0 0/100% 33.33%}
.pdot{position:absolute;left:50%;width:10px;height:10px;margin:0 0 -5px -5px;border-radius:50%;border:2px solid #fff}
.pdot.mtc{background:#2a78d6}.pdot.city{background:#eb6834}.pdot.city.proj{background:#fff;border:2px solid #eb6834}
.pdot b{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);font-size:11px;color:var(--ink)}
.pval{font-size:10.5px;color:var(--muted);min-height:1.2em;text-align:center}
.pyr{font-size:11px;color:var(--muted)}
.lead-grid{display:grid;grid-template-columns:1fr;gap:16px;margin:16px 0}
@media (min-width:760px){.lead-grid{grid-template-columns:3fr 2fr}}
.figure-img{margin:0}.figure-img img{border-radius:10px;width:100%}
.figure-img figcaption{font-size:13px;color:var(--muted);margin-top:6px}
.rules{background:var(--card);border:1px solid var(--rule);border-left:4px solid var(--navy);border-radius:10px;padding:12px 18px}
.rules li{margin:.3em 0}
'''


def page_html(evs, outs, credits, ask_credits):
    hero = credits['photos']['aerial-1932']
    bird = credits['photos']['birdseye-1909']
    street = ask_credits['photos']['street-condition']

    def credit(p):
        return (f'<a href="{e(p["source_page"])}">{e(p["author"])}</a>, {e(p["license"])}'
                + (f' ({e(p["license_basis"])})' if p.get('license_basis') else '') + ', via Wikimedia Commons')
    items, last = '', None
    for ev in sorted(evs, key=lambda x: x['date']):
        card, year = card_html(ev)
        if year != last:
            items += f'<div class="tl-year">{year}</div>'
            last = year
        items += card
    body = f'''<section class="hero"><figure class="hero-photo"><img src="{e(hero["file"])}" alt="{e(hero["alt"])}"
width="{hero["width"]}" height="{hero["height"]}"></figure><div class="wrap hero-in"><span class="kicker">Research prototype · streets and infrastructure, 2010-2026</span>
<h1>How Did We Get Here?</h1><p class="sub">Berkeley's budget decisions and their consequences</p></div></section>
<main class="narrow" style="padding-block:18px">
<p class="photo-note"><span class="tag">Historical photo</span> {e(hero["description"])}. Illustrative only. {credit(hero)}.</p>
<div class="lead-grid"><div>
<p>This timeline sets City Council decisions about streets and infrastructure next to what happened afterwards. Each card
answers six questions from the public record and says plainly when a record has not yet been collected.</p>
<div class="rules"><b>How to read it</b><ul class="plain">
<li>Placing a decision before an outcome does not mean the decision caused it. Where the City attributes a result to a
decision, the card says so and names who made the claim.</li>
<li>"Alternatives" are only those documented at the time: failed motions and options in the recommendation. Hindsight
scenarios are kept separate and none are included yet.</li>
<li>Votes are copied exactly as recorded. "All Ayes" is not expanded into names.</li>
<li>No scores, rankings or ratings of officials.</li></ul></div></div>
<figure class="figure-img"><img src="{e(bird["file"])}" alt="{e(bird["alt"])}" loading="lazy">
<figcaption>{e(bird["description"])}. {credit(bird)}.</figcaption></figure></div>
<h2 class="sec">The record so far</h2>
<p class="sec-sub">Outcome data that can be compared across years. Gaps are shown, not filled.</p>
{charts_html(outs)}
<figure class="figure-img" style="margin:18px 0"><img src="../../docs/{e(street["file"])}" alt="{e(street["alt"])}" loading="lazy">
<figcaption>Illustrative photo: {e(street["description"])}, {e(street["date"])}. Not evidence for any figure.
<a href="{e(street["source_page"])}">Photo: {e(street["author"])}</a>, {e(street["license"])}, via Wikimedia Commons.</figcaption></figure>
<h2 class="sec">Timeline of decisions</h2>
<p class="sec-sub">{len(evs)} proposed events (storyboard). Open a card's questions to see the record and its citations.</p>
<div class="tl-filters" role="group" aria-label="Filter events">
<button aria-pressed="true" data-f="all">All</button><button aria-pressed="false" data-f="council_decision">Council decisions</button>
<button aria-pressed="false" data-f="council_direction">Council directions</button>
<button aria-pressed="false" data-f="voter_decision">Voter decisions</button><button aria-pressed="false" data-f="context">Context</button></div>
<div class="tl">{items}</div>
<label class="techtoggle"><input type="checkbox" id="tech"> Show technical references</label>
<p class="cap">Data: <code>phase2/history/data/decisions-streets.json</code>, <code>outcomes-streets.json</code>. Research
prototype; not published; not reviewed by a person.</p>
</main>
<script>
document.querySelectorAll('.tl-filters button').forEach(function(b){{b.addEventListener('click',function(){{
 var f=b.dataset.f;document.querySelectorAll('.tl-filters button').forEach(function(x){{x.setAttribute('aria-pressed',x===b?'true':'false')}});
 document.querySelectorAll('.tl-item').forEach(function(it){{it.hidden=!(f==='all'||it.dataset.kind===f)}});
 document.querySelectorAll('.tl-year').forEach(function(y){{var n=y.nextElementSibling,vis=false;
  while(n&&!n.classList.contains('tl-year')){{if(!n.hidden)vis=true;n=n.nextElementSibling}}y.hidden=!vis}});
}})}});
</script>'''
    return design.shell('How Did We Get Here? — Berkeley budget decisions (prototype)',
                        f'<style>{EXTRA_CSS}</style>' + body, '../../docs/',
                        'A research prototype timeline of Berkeley street and infrastructure decisions and outcomes.')


def main(argv):
    evs, outs = events(), outcomes()
    problems = check(evs, outs)
    for p in problems:
        print('CHECK', p)
    n_ver = sum(ev[k]['status'] == 'verified' for ev in evs for k in ('decision', 'instrument', 'vote', 'money', 'purpose',
                                                                         'alternatives', 'actual', 'outcomes', 'outstanding'))
    print(f'{len(evs)} events; {n_ver} of {9 * len(evs)} fields verified; {len(list(all_citations(evs)))} citations; '
          f'{len(problems)} problems')
    if problems:
        return 1
    if '--write' in argv:
        (HIST / 'data').mkdir(exist_ok=True)
        meta = {'schema_version': SCHEMA_VERSION, 'workstream': 'How Did We Get Here? (streets and infrastructure)',
                'status': 'RESEARCH PROTOTYPE - not reviewed, not published', 'generated': '2026-10-26',
                'documents': DOCS}
        (HIST / 'data' / 'decisions-streets.json').write_text(json.dumps({**meta, 'events': evs}, indent=1) + '\n')
        (HIST / 'data' / 'outcomes-streets.json').write_text(json.dumps({**meta, 'series': outs}, indent=1) + '\n')
        credits = json.loads((HIST / 'docs' / 'assets' / 'photos' / 'credits.json').read_text())
        ask_credits = json.loads((PHASE2 / 'docs' / 'assets' / 'photos' / 'credits.json').read_text())
        (HIST / 'docs' / 'timeline.html').write_text(page_html(evs, outs, credits, ask_credits))
        print('wrote data/decisions-streets.json, data/outcomes-streets.json, docs/timeline.html')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

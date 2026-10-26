"""Actual street expenditures, FY2010-FY2025, from the City's Annual Street Reports to the State Controller.

Why this source: it is the only published series of ACTUAL street expenditures for Berkeley that is consistent across
years. Each California city must file an Annual Street Report (Streets and Highways Code section 2151) with the State
Controller, classifying street-purpose expenditures as Undistributed Engineering and Administration, Construction
(including "Street Reconstruction"), Maintenance (including "Overlay and Sealing"), equipment and contributions.

What it is not:
  - not audited by the Controller (the Controller compiles what cities file);
  - not "paving only": "Street Reconstruction" can include complete-streets, bikeway and safety work coded by the City
    as reconstruction, and paving can also appear as "Overlay and Sealing" or "Patching" (maintenance);
  - not reconciled by BeTH to the ACFR (which does not report street spending by these categories).
Appropriations, encumbrances, transfers and bond proceeds are not expenditures and are not in this dataset.

Sources:
  FY2010-FY2017: the Controller's printed "Streets and Roads Annual Report", Table 5 (Cities), Berkeley column; one page
                 per year kept in sources/sco/ (full-file SHA-256 in sco-report-extracts.json).
  FY2018-FY2025: the Controller's "City Street Raw Data" workbooks (bythenumbers.sco.ca.gov datasets mpy3-2iag,
                 g8ja-n4f6, b5ms-dvgv); Berkeley rows extracted to sources/sco/berkeley-sco-raw.json.
"""
import json
from pathlib import Path

HIST = Path(__file__).resolve().parents[1]
SCO = HIST / 'sources' / 'sco'
CATS = ['Undistributed Engineering and Administration', 'Street Reconstruction', 'Overlay and Sealing', 'Patching',
        'Total Construction', 'Total Maintenance', 'Grand Total Expenditures']
CLASSIFY = {
    'Undistributed Engineering and Administration': ('overhead (design, engineering, administration)', 'not allocated to projects',
                                                     {'design': True, 'administration': True, 'construction': False}),
    'Street Reconstruction': ('capital', 'construction', {'design': False, 'administration': False, 'construction': True}),
    'Overlay and Sealing': ('operating (maintenance)', 'paving maintenance', {'design': False, 'administration': False, 'construction': True}),
    'Patching': ('operating (maintenance)', 'paving maintenance', {'design': False, 'administration': False, 'construction': True}),
    'Total Construction': ('capital', 'all street construction', {'design': False, 'administration': False, 'construction': True}),
    'Total Maintenance': ('operating (maintenance)', 'all street maintenance', {'design': False, 'administration': False, 'construction': True}),
    'Grand Total Expenditures': ('mixed', 'all street-purpose expenditures', {'design': True, 'administration': True, 'construction': True}),
}
BASIS = ('Actual expenditures as reported by the City to the State Controller (Annual Street Report, Streets and Highways '
         'Code s.2151). The Controller notes the data are not audited. Not reconciled by BeTH to the ACFR.')
DATASET_KEYS = {  # category -> raw summary column (FY2018-FY2025)
    'Street Reconstruction': 'Street Reconstruction_Total_Construction and Right of Way',
    'Overlay and Sealing': 'Overlay and Sealing_Total_Maintenance',
    'Patching': 'Patching_Total_Maintenance',
    'Total Construction': 'Total Construction_Total_Construction and Right of Way',
    'Total Maintenance': 'Total Maintenance_Total_Maintenance',
    'Grand Total Expenditures': 'Total Street Purpose Expenditures_Total_',
}


def register_docs(_doc):
    man = json.loads((SCO / 'sco-report-extracts.json').read_text())
    for full, m in man.items():
        if not full.endswith('.pdf'):
            continue
        fy = full.split('fy')[1][:4]
        _doc(f'sco:{fy}', f'State Controller, Streets and Roads Annual Report, FY20{fy[:2]}-{fy[2:]}, Table 5 (Cities), page '
             f'{m["original_page"]} (single-page extract)', f'phase2/history/sources/sco/{m["extract"]}', 'state_report')
    _doc('acfr23:p122', 'FY2023 ACFR, PDF p.122, Note 4.C Advances to/from (text extract)',
         'phase2/history/sources/acfr/acfr-fy2023-p122.txt', 'audited')
    _doc('acfr23:p324', 'FY2023 ACFR, PDF p.324, internal service funds statement (text extract)',
         'phase2/history/sources/acfr/acfr-fy2023-p324.txt', 'audited')
    _doc('acfr24', 'FY2024 ACFR', 'staging/fy2024/source/annual-comprehensive-financial-report-fy2024.pdf', 'audited')
    _doc('acfr25', 'FY2025 ACFR', 'annual-comprehensive-financial-report-fy2025.pdf', 'audited')
    _doc('ws25:p37', 'Safe Streets & Pavement Management Program Workshop, March 25, 2025, slide 37 (text extract)',
         'phase2/history/sources/measure-ff/safe-streets-workshop-2025-03-25-p37.txt', 'staff_presentation')
    _doc('r22:jul26-03', 'Establishing Policy for Adequate Annual General Fund Contribution for Street Maintenance, Council '
         'Item 3, July 26, 2022 (report)', 'phase2/history/sources/streets/council-2022-07-26-item03-paving-policy.pdf',
         'council_item')


def pdf_rows(cite):
    tabs = json.loads((SCO / 'berkeley-sco-pdf-tables.json').read_text())
    rows = []
    for full, r in tabs.items():
        fy = full.split('fy')[1][:4]
        year = 2000 + int(fy[2:])
        for c in CATS:
            v = r.get(c)
            if v is None:
                continue
            rows.append({'fy': year, 'category': c, 'amount': v, 'fund': 'all funds (City total)', 'project_id': None,
                         'source_type': 'printed_report',
                         'citation': cite(f'sco:{fy}', 1, f'{v:,}' if v else 'Berkeley')})
    return rows


def dataset_rows():
    raw = json.loads((SCO / 'berkeley-sco-raw.json').read_text())
    summ = raw['SR_EXP_SUMMARY'] + raw['13 SR_EXP_SUMMARY']
    det = raw['SR_EXP_DETAIL'] + raw['5 SR_EXP_DETAIL']
    rows, detail = [], []
    for r in summ:
        fy = int(r['Fiscal Year'])
        ue = sum(v for k, v in r.items() if isinstance(v, (int, float)) and
                 (k.startswith('Total Undistributed Administration and Engineering_Total') or
                  k.startswith('Total Undistributed Engineering and Administration_Total')))
        rows.append({'fy': fy, 'category': 'Undistributed Engineering and Administration', 'amount': ue,
                     'fund': 'all funds (City total)', 'project_id': None, 'source_type': 'dataset',
                     'citation': {'dataset': 'SCO City Street Raw Data', 'sheet': 'SR_EXP_SUMMARY', 'fiscal_year': fy}})
        for c, k in DATASET_KEYS.items():
            v = r.get(k)
            rows.append({'fy': fy, 'category': c, 'amount': None if v in (None, 'NULL') else v, 'fund': 'all funds (City total)', 'project_id': None,
                         'source_type': 'dataset',
                         'citation': {'dataset': 'SCO City Street Raw Data', 'sheet': 'SR_EXP_SUMMARY', 'column': k,
                                      'fiscal_year': fy}})
    for r in det:
        if r.get('Expenditure Class') != 'Street Reconstruction':
            continue
        desc = str(r.get('Expenditure Description') or '')
        pid = next((t for t in desc.replace('-', ' ').split() if t[:2] in ('PW', '14', '17', '18', '11', '15') and
                    any(ch.isdigit() for ch in t) and len(t) >= 6), None)
        detail.append({'fy': int(r['Fiscal Year']), 'category': 'Street Reconstruction', 'amount': r.get('Amount') or 0,
                       'fund': str(r.get('Fund Number')), 'project_id': pid, 'description': desc,
                       'funding_source': r.get('Funding Source'), 'expenditure_type': r.get('Expenditure Type'),
                       'source_type': 'dataset',
                       'citation': {'dataset': 'SCO City Street Raw Data', 'sheet': 'SR_EXP_DETAIL',
                                    'record_no': r.get('Record No'), 'fiscal_year': int(r['Fiscal Year'])}})
    return rows, detail


def dataset(cite):
    pr = pdf_rows(cite)
    dr, detail = dataset_rows()
    rows = []
    for r in pr + dr:
        cap, scope, inc = CLASSIFY[r['category']]
        rows.append({**r, 'accounting_basis': BASIS, 'capital_or_operating': cap, 'scope': scope,
                     'includes': {**inc, 'debt_service': False, 'transfers': False, 'bond_proceeds': False,
                                  'appropriations_or_encumbrances': False}})
    checks = []
    for fy in sorted({d['fy'] for d in detail}):
        s = sum(d['amount'] for d in detail if d['fy'] == fy)
        summ = next(r['amount'] for r in dr if r['fy'] == fy and r['category'] == 'Street Reconstruction')
        checks.append({'fy': fy, 'detail_sum': s, 'summary': summ, 'difference': s - summ})
    return {
        'what': 'Actual street-purpose expenditures as reported by the City of Berkeley to the State Controller, by '
                'Controller category, FY2010-FY2025.',
        'accounting_basis': BASIS,
        'categories_used_for_paving': {
            'primary': 'Street Reconstruction (capital construction; contracts plus any in-house work)',
            'also': 'Overlay and Sealing; Patching (maintenance)',
            'excluded_from_paving_measures': 'Undistributed Engineering and Administration (design, engineering and '
                                              'administration not charged to projects); signals, lighting, bike/ped and storm '
                                              'drain construction; other street maintenance.'},
        'reconciliation_rules': [
            'Never add these actuals to budget or plan figures: different bases.',
            'Totals are all-fund City totals. Fund-level detail exists only from FY2018 (SR_EXP_DETAIL).',
            'Street Reconstruction detail rows must sum to the summary for each year (checked; see detail_check).',
            'Design and administration sit in Undistributed Engineering and Administration and are not in Street '
            'Reconstruction; adding both is not double counting but changes the measure.',
            'Bond-funded construction (Measure M fund 630 in FY2018; Measure T1 fund 511) appears as expenditure when spent; '
            'bond proceeds themselves are not in this dataset.',
            'Classification varies by year: FY2014 reports no Street Reconstruction but $1,597,699 of Patching; FY2025 '
            'reports $2,331,787 of Overlay and Sealing. Year-to-year comparisons of one category can mislead.',
            'Some Street Reconstruction rows are described as "Admin & Eng" or "Maintenance" ($4.09M in FY2024, $8.00M in '
            'FY2025; see description_class_conflicts). They are kept as filed and flagged, not reclassified.',
            'Project identifiers are taken from the City\'s expenditure descriptions; their meaning (e.g. PWENST2301) is not '
            'defined in any document BeTH holds and needs the City\'s project dictionary.'],
        'rows': rows,
        'street_reconstruction_detail': detail,
        'description_class_conflicts': [  # recorded as filed; BeTH does not reclassify the City's entries
            {'fy': d['fy'], 'fund': d['fund'], 'description': d['description'], 'amount': d['amount'],
             'record_no': d['citation']['record_no'],
             'note': 'Filed as Street Reconstruction (construction) but described as administration/engineering or '
                     'maintenance. Needs the City\'s explanation before it is counted as paving construction.'}
            for d in detail if any(w in d['description'].lower() for w in ('admin', 'maint'))],
        'detail_check': checks,
    }


def series(ds):
    """Street Reconstruction and paving maintenance by year, for the chart and narrative."""
    out = []
    for fy in sorted({r['fy'] for r in ds['rows']}):
        g = {r['category']: r['amount'] for r in ds['rows'] if r['fy'] == fy}
        out.append({'fy': fy, 'street_reconstruction': g.get('Street Reconstruction'),
                    'overlay_sealing': g.get('Overlay and Sealing'), 'patching': g.get('Patching'),
                    'eng_admin': g.get('Undistributed Engineering and Administration'),
                    'grand_total': g.get('Grand Total Expenditures')})
    return out


# ------------------------------------------------------------------ investigations A-D (DRAFT, not approved)
# Each finding carries a status: 'verified' (the cited pages say it), 'arithmetic' (BeTH computation on cited figures),
# 'open' (the record needed is not held). Authorizations are never treated as transactions.

def fy2027_arithmetic():
    """The two printed series for the Res. 70,456 line, and the 3% escalation that reproduces each (to within $1: the City's
    spreadsheet appears to carry unrounded values)."""
    printed_2023 = {2025: 8937022, 2026: 9205132, 2027: 9481286, 2028: 9765725}
    printed_2026 = {2026: 8240000, 2027: 8487200, 2028: 8741816, 2029: 9004070, 2030: 9274193, 2031: 9552418}
    fit_2023 = all(abs(printed_2023[y] - 8937022 * 1.03 ** (y - 2025)) <= 1 for y in printed_2023)
    fit_2026 = all(abs(printed_2026[y] - 8_000_000 * 1.03 ** (y - 2025)) <= 1 for y in printed_2026)
    return {'plan_2023': printed_2023, 'budget_2026': printed_2026,
            'plan_2023_is_8937022_at_3pct_from_fy2025': fit_2023, 'budget_2026_is_8000000_at_3pct_from_fy2025': fit_2026,
            'difference_fy2027': printed_2023[2027] - printed_2026[2027],
            'base_difference_fy2025': printed_2023[2025] - 8_000_000}


def moe_scenarios():
    """Illustrative only: the FY2027 plan's non-Measure FF sources against $15.3M escalated at the 3% the City's own tables
    use. Res. 70,456 names a different index; the base year is not stated anywhere BeTH holds. Not a compliance finding."""
    fy27 = {'SB 1 / gas tax': 2195303, 'Measure BB': 2980000, 'Measure F VRF': 155000, 'CIP Fund': 1925000,
            'CIP Fund / Council Policy (Res. 70,456)': 8487200, 'Zero Waste Fund': 2000000, 'Clean Storm Fund': 1000000}
    total = sum(fy27.values())
    without = total - fy27['Zero Waste Fund'] - fy27['Clean Storm Fund']
    req = {f'base FY{b}': round(15_300_000 * 1.03 ** (2027 - b)) for b in (2023, 2025)}
    return {'fy2027_sources': fy27, 'total': total, 'total_without_zero_waste_and_storm': without, 'requirement_if': req}


def investigations(cite):
    ar, moe = fy2027_arithmetic(), moe_scenarios()
    return [
        {'id': 'A', 'question': 'Was the 2022 "$7.3 million" baseline General Fund money?',
         'answer': 'No. The $7.3 million was the City\'s street paving budget from all recurring sources; the General Fund '
                   'share was the $1,925,000 Capital Improvement Fund line. The July 2022 report and the annotated agenda '
                   'call it the "existing General Fund street paving budget"; the adopted resolution text calls it the '
                   '"existing baseline $7.3 million allocation". City staff in 2026 describe it as coming "from local and '
                   'state sources".',
         'findings': [
             {'status': 'verified', 'text': 'The July 26, 2022 recommendation describes the $7.3 million as the existing '
                                            'General Fund street paving budget.',
              'citations': [cite('r22:jul26-03', 1, 'augment the existing General Fund street paving budget of $7.3 million'),
                            cite('aa:2022-07-26-special', 4, 'augment the existing General Fund street paving budget of $7.3 million')]},
             {'status': 'verified', 'text': 'The resolution as adopted does not call the $7.3 million General Fund money.',
              'citations': [cite('aa:2022-07-26-special', 4, 'in addition to the existing baseline $7.3 million allocation, '
                                                              'for a total amount of $15.3 million')]},
             {'status': 'verified', 'text': 'Six months earlier, City staff\'s Table 1 put the recurring program at $7,275,303 '
                                            'of which the Capital Improvement Fund (General Fund) line was $1,925,000; the '
                                            'rest was gas tax, SB 1, Measure BB and Measure F.',
              'citations': [cite('r22:25a', 1, '7,275,303'), cite('r22:25a', 1, '1,925,000')]},
             {'status': 'verified', 'text': 'City staff in the FY2027 budget: the $7.3 million came from local and state sources.',
              'citations': [cite('budget:2026-06-23', 243, 'The City has historically allocated about $7.3 million in '
                                                           'recurring funding to Street paving from local and state sources')]},
             {'status': 'verified', 'text': 'A March 2025 City workshop slide shows "General Fund: $9.9M/yr" as "Baseline '
                                            'annual streets funding" without a breakdown; it is not reconcilable to either '
                                            'figure from that slide alone.',
              'citations': [cite('ws25:p37', 1, 'General Fund: $9.9M/yr')]},
         ],
         'open': ['The City\'s working papers for the $7.3 million and the $9.9 million (records request item 5).']},
        {'id': 'B', 'question': 'Did the June 2023 $4.05M and the July 2023 $5.5M Workers\' Compensation actions happen as '
                                'transfers, loans, receivables and repayments?',
         'answer': 'Authorized: $9.55 million in two actions. Recorded in the audited Workers\' Compensation statements, '
                   'FY2023-FY2025: one transfer out of $5,500,000, in FY2024, to the General Fund, and no advance or '
                   'receivable for either action. The $4,050,000 does not appear in the FY2023 Workers\' Compensation '
                   'statement (transfers "-"), in the FY2024 or FY2025 ACFR at all, or in either year\'s interfund notes. The '
                   '$813,779 transfer into the fund in FY2024 is the final repayment of a 2017 General Fund loan, unrelated '
                   'to either action. Which 2023 action, if either, the $5.5 million transfer carried out is not established.',
         'findings': [
             {'status': 'verified', 'text': 'June 13, 2023: Council approved using $4,050,000 from the Workers Compensation '
                                            'Fund toward the Measure T1 funding gap (an authorization).',
              'citations': [cite('aa:2023-06-13', 11, 'Use $4,050,000 from the Workers Compensation Fund')]},
             {'status': 'verified', 'text': 'July 25, 2023: Council authorized an internal $5.5M loan from the Workers '
                                            'Compensation Fund for the D and E dock project (an authorization).',
              'citations': [cite('loan:2023-07-25', 1, 'authorizes an internal loan of $5.5M from the Workers Compensation Fund')]},
             {'status': 'verified', 'text': 'FY2023 (year ended June 30, 2023): no Workers\' Compensation transfers; ending net '
                                            'position $12,650,613; the 2017 loan balance stood at $813,779.',
              'citations': [cite('acfr23:p324', 1, '12,650,613'),
                            cite('acfr23:p122', 1, 'No principal repayment of the loan was made during FY 2023')]},
             {'status': 'verified', 'text': 'FY2024: transfers in $813,779 and out ($5,500,000); the $813,779 repaid the 2017 '
                                            'loan in full; the transfers note shows the $5,500,000 going to the General Fund.',
              'citations': [cite('acfr24', 312, '(5,500,000)'), cite('acfr24', 312, '813,779'),
                            cite('acfr24', 116, 'principal repayment of the loan in the amount of $813,779 was made'),
                            cite('acfr24', 115, '5,500,000')]},
             {'status': 'verified', 'text': 'FY2025: no Workers\' Compensation transfers; ending net position ($9,752,938); the '
                                            'only Marina interfund balance is $2,477,099 due to the General Fund.',
              'citations': [cite('acfr25', 322, '(9,752,938)'), cite('acfr25', 113, "Worker's Compensation Fund -"),
                            cite('acfr25', 113, 'Marina Operations 2,477,099')]},
         ],
         'arithmetic': {'authorized': 4050000 + 5500000, 'audited_transfers_out_fy2023_2025': 5500000,
                        'not_visible_in_audited_wc_statements': 4050000 + 5500000 - 5500000},
         'caveats': ['The FY2024 transfers note prints "Equipment Replacement Fund" in the From column of the $5,500,000 row '
                     'while the fund statement (p.312) shows the outflow in the Workers\' Compensation column; the group '
                     'total ($6,450,612) matches the internal service funds\' total transfers out. Read as Workers\' '
                     'Compensation; the label conflict is the City\'s and is recorded, not corrected.',
                     'The $4,050,000 may have been met from another source or not executed; BeTH holds no record either way. '
                     'Absence from audited statements is not proof that no money moved through another fund.',
                     'The Marina ledger question (BeTH records the $5.5M as a loan into fund 608) is held in '
                     'phase2/01-marina-fund-case-study.md and the 2026-10-25 flag; nothing here changes that ledger.'],
         'open': ['Journal entries for the FY2024 $5,500,000 transfer and any entry for the $4,050,000 (records request item 3).']},
        {'id': 'C', 'question': 'Which funding sources count toward the $15.3 million Measure FF budget requirement?',
         'answer': 'The ordinance counts "funding for street maintenance, from sources other than this tax", at the $15.3 '
                   'million defined by Resolution No. 70,456-N.S. That resolution defines $15.3 million as $8 million of '
                   'General Fund plus the "existing baseline $7.3 million allocation", a baseline that contained no Zero '
                   'Waste or Storm Water money. City staff introduced Zero Waste and Storm Water contributions in November '
                   '2023 as "new revenue sources". The ordinance text does not exclude them, and BeTH found no City '
                   'calculation stating which funds the City counts. Whether they count is a legal question for the City '
                   'Attorney; BeTH does not answer it.',
         'findings': [
             {'status': 'transcription', 'text': 'BMC 7.11.030(B): the Council may not impose the tax for two years if it '
                                                  'fails to adopt a budget with at least $15.3 million for street maintenance '
                                                  'from sources other than this tax, adjusted for inflation per Res. 70,456. '
                                                  '7.11.030(C) reduces the requirement if an external source in the 2023-24 '
                                                  'budget is lost or declines. Read from page images of the initiative as '
                                                  'filed (no text layer); see phase2/sources/measure-ff-ordinance-transcription.md.',
              'citations': []},
             {'status': 'verified', 'text': 'Res. 70,456 composition of $15.3 million.',
              'citations': [cite('aa:2022-07-26-special', 4, 'in addition to the existing baseline $7.3 million allocation, '
                                                              'for a total amount of $15.3 million')]},
             {'status': 'verified', 'text': 'November 2023: Zero Waste and Storm Water listed among "three important new '
                                            'revenue sources".',
              'citations': [cite('r23:17', 1, 'The proposed Five Year Plan includes three important new revenue sources'),
                            cite('r23:17', 1, 'rate revenue from the Zero Waste Fund')]},
             {'status': 'verified', 'text': 'July 2026: Zero Waste (fund 601) $2M a year offsets collection-vehicle impact; '
                                            'Clean Storm (fund 616) $1M a year pays for cross drains and is excluded by staff '
                                            'from the amount "available for street rehabilitation".',
              'citations': [cite('plan:2026-07-07', 2, 'Zero Waste- Fund 601; Clean Storm- Fund 616'),
                            cite('plan:2026-07-07', 3, 'The Zero Waste Fund contributes $2 million annually to offset the '
                                                       'impact of Zero Waste collection vehicles'),
                            cite('plan:2026-07-07', 3, 'excluding the $5 million in Clean Storm Fund allocations dedicated '
                                                       'to drainage infrastructure')]},
             {'status': 'verified', 'text': 'Actual Street Reconstruction reported to the State Controller from fund 601 '
                                            '(Zero Waste): $7,988 in FY2021 and $728,763 in FY2025; none from fund 616 '
                                            '(Clean Storm), which reported small storm-drain and administration amounts.',
              'citations': [],
              'dataset_refs': [{'dataset': 'SCO City Street Raw Data', 'sheet': 'SR_EXP_DETAIL', 'fiscal_year': 2021,
                                'record_no': 65, 'fund': '601'},
                               {'dataset': 'SCO City Street Raw Data', 'sheet': '5 SR_EXP_DETAIL', 'fiscal_year': 2025,
                                'record_no': 57, 'fund': '601'}]},
         ],
         'arithmetic': moe,
         'caveats': ['The requirement is about the budget the Council adopts, not about money spent: an actual-expenditure '
                     'series cannot by itself show compliance or breach.',
                     'Scenario arithmetic uses the 3% the City\'s tables apply; Res. 70,456 names the greater of Bay Area CPI '
                     'or state per capita personal income growth. Neither the index values nor the base year have been '
                     'checked. The scenario is not a compliance finding.',
                     'The City may count street-maintenance budgets outside the paving plan (e.g. Public Works operating '
                     'budgets). BeTH has not seen the City\'s calculation.',
                     'The City\'s Measure FF web page links "Ordinance No. 7939-N.S.", which is the Ashby BART real property '
                     'exchange ordinance; Measure FF is Ordinance 7,952-N.S. (page image read; no text layer).'],
         'open': ['The City\'s maintenance-of-effort calculation and the City Attorney\'s position on which funds count '
                  '(records request item 4).']},
        {'id': 'D', 'question': 'Why is FY2027 $8,487,200 when $9,481,286 was planned?',
         'answer': f'The November 2023 plan escalated from $8,937,022 in FY2025 at 3% a year (FY2027 $9,481,286). The FY2026 '
                   f'budget and the July 2026 plan restart from $8,000,000 in FY2025 at 3% a year ($8,240,000 FY2026, '
                   f'$8,487,200 FY2027). The ${ar["difference_fy2027"]:,} gap is the ${ar["base_difference_fy2025"]:,} '
                   f'difference in the FY2025 base, carried forward at 3%. BeTH found no document explaining the re-basing, '
                   f'and both series escalate at a flat 3% although Res. 70,456 and the July 2026 plan name an index.',
         'findings': [
             {'status': 'verified', 'text': 'November 2023 plan, Res. 70,456 line: FY2024 $5,996,598; FY2025-FY2028 $8,937,022, '
                                            '$9,205,132, $9,481,286, $9,765,725.',
              'citations': [cite('r23:17', 2, '8,937,022 9,205,132 9,481,286 9,765,725')]},
             {'status': 'verified', 'text': 'Adopted FY2027-28 budget, CIP row "Street Rehab PCI Improvements", fund 501: prior '
                                            'years $14,100,000; $8,240,000; $8,487,200; $8,741,816; $9,004,070; $9,274,193; $9,552,418.',
              'citations': [cite('budget:2026-06-23', 215, '$14,100,000 $8,240,000 $8,487,200 $8,741,816 $9,004,070')]},
             {'status': 'verified', 'text': 'July 2026 plan says funding is escalated per Res. 70,456 and the Measure FF ordinance.',
              'citations': [cite('plan:2026-07-07', 2, '$8,487,200 $8,741,816 $9,004,070'),
                            cite('plan:2026-07-07', 12, 'Funding is escalated consistent with the terms of the applicable '
                                                        'Council fiscal policy (Resolution No. 70,456-N.S.)')]},
         ],
         'arithmetic': {k: (v if not isinstance(v, dict) else {str(y): a for y, a in v.items()}) for k, v in ar.items()},
         'caveats': ['The $14,100,000 "prior years" figure and the FY2023-FY2025 amounts actually budgeted and spent under '
                     'Res. 70,456 are not reconciled here.'],
         'open': ['Budget worksheets showing the base and index used (records request item 5).']},
    ]

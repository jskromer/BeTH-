"""Accounting acceptance tests, including negative controls and real-PDF reruns."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import acfr_funds
from acfr_config import load_year
import acfr_pilot
import acfr_reconcile as recon

PDF = ROOT / 'staging/fy2024/source/annual-comprehensive-financial-report-fy2024.pdf'
NEXT_PDF = ROOT / 'annual-comprehensive-financial-report-fy2025.pdf'


def governmental():
    rows = {'Taxes': 10, 'Total revenues': 10, 'General government': 8,
            'Total expenditures': 8, 'Revenues over/(under) expenditures': 2,
            'Transfers in': 3, 'Transfers out': -1,
            'Total other financing sources/(uses)': 2, 'Net change in fund balance': 4,
            'Fund balance, July 1, 2023': 5, 'Fund balance, June 30, 2024': 9}
    return dict(fund_number='test', name='Test Fund', type='special_revenue',
                source=dict(statement_id='nonmajor_governmental', column_name='Test Fund'),
                accounting_basis='modified_accrual', mapping={}, rows=rows, labels=list(rows))


class AccountingTests(unittest.TestCase):
    def test_arithmetic_checks_pass_without_fabricated_adjustments(self):
        record = recon.financial_record(governmental(), load_year(2024))
        self.assertTrue(all(c['status'] == 'RECONCILED' for c in record['checks']))
        self.assertEqual(record['transfers_as_reported'], {'in':3, 'out':-1})
        self.assertEqual(record['values']['transfers_out'], 1)
        self.assertFalse(record['balances']['restatement_reported'])

    def test_detects_arithmetic_and_transfer_disagreements(self):
        column = governmental()
        column['rows'].update(Taxes=11, **{'Transfers out':-2, 'Fund balance, June 30, 2024':10})
        result = recon.financial_record(column, load_year(2024))
        conflicts = {i['code'] for i in result['issues'] if i['status'] == 'CONFLICT'}
        self.assertTrue({'revenue_categories', 'other_financing_categories', 'balance_roll_forward'} <= conflicts)
        self.assertEqual(result['values']['ending_balance'], 10)

    def test_missing_reviewed_fields_are_review_items_not_conflicts(self):
        result = recon.financial_record(governmental(), load_year(2024))
        existing = {'annual':[{'fy':2024, 'basis':'audited', 'revenue':10, 'expenditure':8}]}
        before = copy.deepcopy(existing)
        recon.compare_reviewed(result, existing)
        self.assertEqual(existing, before)
        self.assertTrue(any(i['code'] == 'missing_reviewed_field' for i in result['issues']))
        self.assertFalse(any(i['status'] == 'CONFLICT' for i in result['issues']))

    def test_different_reviewed_values_remain_conflicts(self):
        result = recon.financial_record(governmental(), load_year(2024))
        recon.compare_reviewed(result, {'annual':[{'fy':2024, 'basis':'audited', 'revenue':12, 'expenditure':7}]})
        conflicts = [i for i in result['issues'] if i['code'] == 'reviewed_value_conflict']
        self.assertEqual(len(conflicts), 2)
        self.assertEqual(conflicts[0]['reviewed'], 12)
        self.assertEqual(conflicts[0]['extracted'], 10)

    def test_missing_labels_and_blank_cells_collect_every_problem(self):
        column = governmental()
        del column['rows']['Total revenues']
        column['labels'].remove('Total revenues')
        column['rows']['General government'] = None
        column['rows']['Fund balance, July 1, 2023'] = None
        result = recon.financial_record(column, load_year(2024))
        self.assertIsNone(result['values']['revenue'])
        self.assertIsNone(result['line_items']['General government'])
        self.assertTrue({'missing_label','missing_value','missing_section'} <= {i['code'] for i in result['issues']})

    def test_restatement_keeps_original_adjustment_and_restated(self):
        current = recon.financial_record(governmental(), load_year(2024))
        following = {'fy':2025, 'source':{'pdf_pages':[77]}, 'checks':[], 'issues':[],
                     'balances':{'original_beginning':9, 'reported_adjustment':-2,
                                 'restated_beginning':7, 'restatement_reported':True}}
        recon.continuity(current, following)
        self.assertEqual(current['values']['ending_balance'], 9)
        self.assertEqual(current['continuity']['balances']['restated_beginning'], 7)
        self.assertFalse(any(i['status']=='CONFLICT' for i in current['issues']))
        bad = copy.deepcopy(following)
        bad['balances']['restated_beginning'] = 6
        result = recon.financial_record(governmental(), load_year(2024))
        recon.continuity(result, bad)
        self.assertTrue(any(i['code']=='next_year_restatement_bridge' for i in result['issues']))

    def test_statement_columns_use_published_total(self):
        first, second = governmental(), governmental()
        second['fund_number'] = 'second'
        total = copy.deepcopy(first)
        total['source']['column_name'] = 'Total Nonmajor'
        total['rows'] = {k:v*2 for k,v in first['rows'].items()}
        self.assertEqual(recon.column_checks([first,second],[total],2024)[0]['status'], 'RECONCILED')
        total['rows']['Total revenues'] = 21
        result = recon.column_checks([first,second],[total],2024)[0]
        self.assertEqual(result['status'], 'CONFLICT')
        check = next(c for c in result['checks'] if c['label']=='Total revenues')
        self.assertEqual((check['calculated'],check['reported'],check['difference']), (20,21,-1))

    def test_output_cannot_overlap_data_website_or_symlinks(self):
        for output in (ROOT, ROOT/'data/funds', ROOT/'docs', ROOT/'tools'):
            with self.subTest(output=output), self.assertRaises(ValueError):
                acfr_pilot.protect_output(output, ROOT/'data/funds')
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            (dest/'funds.json').symlink_to(ROOT/'data/funds/011.json')
            with self.assertRaises(ValueError):
                acfr_pilot.protect_output(dest, ROOT/'data/funds')

    def test_checksum_failure_precedes_output(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'wrong.pdf'
            path.write_bytes(b'not the audited original')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                acfr_pilot.run(path, NEXT_PDF, Path(temp)/'out')
            self.assertFalse((Path(temp)/'out').exists())

    def manifest_fixture(self, root):
        policy = {'audit_files':{'2024':'source/2024.pdf','2025':'source/2025.pdf'},
                  'repository_files':{'tools/parser.py':'extraction code'},
                  'ledger_files':['test.json']}
        paths = {'source/2024.pdf':b'FY2024 audited source',
                 'source/2025.pdf':b'FY2025 audited source',
                 'tools/parser.py':b'parser', 'data/funds/test.json':b'{}',
                 'tools/acfr_years/pilot-inputs.json':json.dumps(policy).encode()}
        for name, payload in paths.items():
            path = root/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        return root/'source/2024.pdf', root/'source/2025.pdf', root/'data/funds'

    def test_manifest_is_independent_of_irrelevant_local_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inputs = self.manifest_fixture(root)
            baseline = acfr_pilot.manifest_inputs(*inputs, root=root)
            irrelevant = ['.DS_Store','data/funds/.DS_Store','source/._2024.pdf',
                          'docs/.DS_Store','docs/.vercel/project.json',
                          'docs/.~lock.book.xlsx#','docs/~$working.docx',
                          'docs/notes.tmp','docs/file.swp','docs/Thumbs.db',
                          '.git/config','docs/index.html',
                          'docs/Berkeley_Efficiency_Bargaining_Strategy.docx']
            for name in irrelevant:
                path = root/name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('machine-local contents')
            self.assertEqual(acfr_pilot.manifest_inputs(*inputs, root=root), baseline)
            for name in irrelevant:
                (root/name).write_text('different machine-local contents')
            self.assertEqual(acfr_pilot.manifest_inputs(*inputs, root=root), baseline)
            self.assertEqual(set(baseline), {'source/2024.pdf','source/2025.pdf',
                'tools/parser.py','data/funds/test.json','tools/acfr_years/pilot-inputs.json'})
            self.assertEqual(baseline['source/2024.pdf']['sha256'], acfr_pilot.digest(inputs[0]))

    def test_manifest_requires_every_explicit_dependency(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inputs = self.manifest_fixture(root)
            baseline = acfr_pilot.manifest_inputs(*inputs, root=root)
            (root/'tools/parser.py').write_text('changed parser')
            changed = acfr_pilot.manifest_inputs(*inputs, root=root)
            self.assertNotEqual(changed['tools/parser.py']['sha256'], baseline['tools/parser.py']['sha256'])
            (root/'tools/parser.py').unlink()
            with self.assertRaisesRegex(ValueError, 'Missing required manifest input'):
                acfr_pilot.manifest_inputs(*inputs, root=root)

    def test_unlisted_or_missing_consumed_ledger_is_an_error(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inputs = self.manifest_fixture(root)
            (root/'data/funds/unlisted.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'unlisted=.*unlisted.json'):
                acfr_pilot.manifest_inputs(*inputs, root=root)
            (root/'data/funds/unlisted.json').unlink()
            (root/'data/funds/test.json').unlink()
            with self.assertRaisesRegex(ValueError, 'missing=.*test.json'):
                acfr_pilot.manifest_inputs(*inputs, root=root)

    def test_cross_page_identity_collisions_and_batch_errors(self):
        config = load_year(2024)
        config['statements'] = [copy.deepcopy(config['statements'][0])]
        config['statements'][0]['pairs'] = [[78,None],[78,None],[78,None]]
        with patch.object(recon, 'load_year', return_value=config), patch.object(recon.acfr_parse, 'parse_pair', side_effect=[(['General Fund'], {'General Fund':{}}, []), ValueError('bad labels'), (['General Fund'], {'General Fund':{}}, [])]):
            columns, _, errors = recon.read_statements(PDF, 2024)
        self.assertEqual(len(columns), 2)
        self.assertEqual(len([e for e in errors if e['code']=='fund_identity_collision']), 2)
        self.assertTrue(any(e['code']=='statement_parse' for e in errors))


class RealPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.temp.name)/'staged'
        cls.before = acfr_pilot.snapshot(ROOT/'data/funds')
        cls.website_before = acfr_pilot.snapshot(ROOT/'docs')
        cls.report = acfr_pilot.run(PDF, NEXT_PDF, cls.out)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_six_curated_ledgers_match_to_dollar_and_are_unchanged(self):
        self.assertEqual(acfr_pilot.snapshot(ROOT/'data/funds'), self.before)
        self.assertEqual(acfr_pilot.snapshot(ROOT/'docs'), self.website_before)
        protected = [f for f in self.report['funds'] if f['protected']]
        self.assertEqual(len(protected),6)
        for f in protected:
            self.assertTrue(f['existing_reviewed'])
            self.assertFalse(any(i['code']=='reviewed_value_conflict' for i in f['issues']))
            self.assertTrue(all(c['difference']==0 for c in f['comparison'] if 'difference' in c))
        marina = json.loads((ROOT/'data/funds/608.json').read_text())
        history = [a for a in marina['annual'] if 2015 <= a['fy'] <= 2023]
        self.assertEqual(len(history),9)
        self.assertTrue(all('series' not in a for a in history))

    def test_every_fund_has_all_required_report_sections(self):
        self.assertEqual(len(self.report['funds']),105)
        self.assertEqual(len(self.report['statement_totals']),9)
        for f in self.report['funds']:
            self.assertTrue({'fund_number','name','source','values','existing_reviewed','checks','issues','continuity','confidence','status','review_status'} <= f.keys())
            self.assertIn(f['status'], recon.STATUSES)
            self.assertNotIn('series', f)
        self.assertEqual(self.report['batch_errors'], [])
        self.assertTrue(all(c['status']=='RECONCILED' for f in self.report['funds'] for c in f['checks'] if c['name']=='next_year_original_beginning'))

    def test_real_source_gaps_and_dollar_discrepancies_are_retained(self):
        funds = {f['fund_number']:f for f in self.report['funds']}
        self.assertIsNone(funds['ACFR-condo-conversion-program']['line_items']['General government'])
        self.assertIsNone(funds['ACFR-measure-b-paratransit']['line_items']['Private contributions and donations'])
        self.assertEqual(funds['ACFR-zero-waste']['continuity']['balances']['reported_adjustment'], -419510)
        self.assertEqual(funds['608']['continuity']['balances']['reported_adjustment'], -63380)
        mismatches = [c for g in self.report['statement_totals'] for c in g['checks'] if c.get('difference')]
        self.assertTrue(mismatches)
        self.assertTrue(all(abs(c['difference'])==1 for c in mismatches))
        self.assertEqual([f['fund_number'] for f in self.report['missing_fy2024_columns']], ['ACFR-fire-admin-training-building-bond'])

    def test_full_pipeline_is_idempotent(self):
        before = acfr_pilot.snapshot(self.out)
        acfr_pilot.run(PDF, NEXT_PDF, self.out)
        self.assertEqual(acfr_pilot.snapshot(self.out), before)
        self.assertEqual(acfr_pilot.snapshot(ROOT/'data/funds'), self.before)

    def test_fy2025_full_records_remain_backward_compatible(self):
        expected = json.loads((ROOT/'tests/fixtures/fy2025-full-extraction.json').read_text())
        self.assertEqual(acfr_funds.extract(NEXT_PDF), expected)


if __name__ == '__main__':
    unittest.main()

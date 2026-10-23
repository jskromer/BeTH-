"""Independent audited expectations for the p.77 omitted expenditure categories."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
import acfr_funds
from acfr_config import load_year
from acfr_pilot import snapshot
from ledger_safety import SafetyError
import reconcile_expenditure_breakdown as breakdown


class CategoryTests(unittest.TestCase):
    def test_wrapped_and_unwrapped_labels_match_without_changing_input(self):
        for year in (2024,2025):
            for label in ('and housing','Community development and housing'):
                rows = {label:123,'TRAN issuance costs':45,'Public safety':6}
                before = copy.deepcopy(rows)
                self.assertEqual(acfr_funds.governmental_expense_items(rows,load_year(year)),
                    {'Public safety':6,'Community development and housing':123,'TRAN issuance costs':45})
                self.assertEqual(rows,before)

    def test_duplicate_wrapped_aliases_fail_instead_of_double_counting(self):
        with self.assertRaisesRegex(SafetyError,'Duplicate expenditure label aliases'):
            acfr_funds.governmental_expense_items({'and housing':10,'Community development and housing':10},load_year(2025))

    def test_fy2024_wrapped_interest_is_also_recognized(self):
        self.assertEqual(acfr_funds.governmental_expense_items({'charges':749523},load_year(2024)),
                         {'Interest and fiscal charges':749523})


class SourceToLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.temp.name)/'proposals'
        cls.before = {p:snapshot(ROOT/p) for p in ('data/funds','docs')}
        cls.report = breakdown.stage(out=cls.out)
        cls.funds = {f['fund_number']:f for f in cls.report['funds']}

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_source_amounts_and_exact_deficits_for_each_fund(self):
        # Read independently from the audited PDF p.77, printed p.42.
        expected = {
            '011':(20221797,90884,256629243,20312681,276941924),
            'ACFR-grants':(13584981,0,33678107,13584981,47263088),
            '501':(2700992,0,13384762,2700992,16085754),
        }
        for fid,(housing,tran,old_sum,gap,total) in expected.items():
            with self.subTest(fund=fid):
                f = self.funds[fid]
                categories = {c['category']:c for c in f['categories']}
                self.assertEqual(categories['Community development and housing']['source_amount'],housing)
                self.assertEqual(categories['TRAN issuance costs']['source_amount'],tran)
                self.assertEqual((f['existing_breakdown_sum'],f['omitted_expenditures'],f['audited_expenditure']), (old_sum,gap,total))
                self.assertEqual(f['source_category_sum'],total)
                self.assertEqual(f['proposed_breakdown_sum'],total)
                self.assertEqual(f['proposed_difference_from_audit'],0)
                self.assertTrue(f['annual_total_unchanged'])
        self.assertEqual(self.report['source']['role'],'expenditure-breakdown extraction source')
        self.assertEqual(self.report['source']['pdf_page'],77)
        self.assertEqual(self.report['omitted_expenditures'],36598654)
        self.assertEqual(self.report['affected_funds'],3)
        self.assertEqual(sum(len(f['proposed_corrections']) for f in self.report['funds']),4)

    def test_all_five_major_fund_breakdowns_reconcile_to_source_totals(self):
        self.assertEqual(len(self.funds),5)
        for f in self.funds.values():
            self.assertEqual(f['source_category_sum'], f['audited_expenditure'])
            self.assertEqual(f['proposed_breakdown_sum'], f['audited_expenditure'])
        self.assertFalse(self.funds['ACFR-library']['approval_required'])
        self.assertFalse(self.funds['ACFR-measure-o-housing-bond']['approval_required'])

    def test_protected_general_fund_is_a_proposal_only(self):
        self.assertTrue(self.funds['011']['protected'])
        self.assertTrue(self.funds['011']['approval_required'])
        self.assertFalse(self.report['apply_automatically'])
        self.assertEqual(len(self.report['protected_ledger_checksums']),6)
        self.assertEqual({p:snapshot(ROOT/p) for p in self.before},self.before)
        stored = json.loads((ROOT/'data/funds/011.json').read_text())
        self.assertNotIn('Community development and housing', {r['line'] for r in stored['flow_detail']['outflows']})
        self.assertTrue(all(not f['apply_automatically'] for f in self.report['funds']))

    def test_transfers_are_preserved_and_not_counted_as_expenditures(self):
        for f in self.funds.values():
            for line in ('Transfers out','Payment to refunded bond escrow agent'):
                old = [r for r in f['existing_outflows'] if r['line']==line]
                proposed = [r for r in f['proposed_outflows'] if r['line']==line]
                self.assertEqual(old,proposed)
        self.assertEqual(next(r['amount'] for r in self.funds['011']['proposed_outflows'] if r['line']=='Transfers out'),33919159)

    def test_staging_is_idempotent_and_cannot_target_ledgers(self):
        before = snapshot(self.out)
        breakdown.stage(out=self.out)
        self.assertEqual(snapshot(self.out), before)
        with self.assertRaises(ValueError):
            breakdown.stage(out=ROOT/'data/funds')


if __name__ == '__main__':
    unittest.main()

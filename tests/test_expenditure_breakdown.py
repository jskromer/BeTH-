"""Independent audited expectations for the p.77 omitted expenditure categories."""
import copy
import json
import shutil
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
import ledger

FIXTURES = ROOT/'tests/fixtures/fy2025-pre-correction'
HISTORY_MANIFEST_SHA256 = '70f4d6393f05d9d037b3980b4edaa2f5ce4a137d458bf37d261c071ec36f7001'


class CategoryTests(unittest.TestCase):
    def test_financing_wrapped_and_full_labels_are_recognized_once(self):
        for year in (2024,2025):
            for label in ('subscriptions','Inception of leases and subscriptions'):
                rows = {label:18156996,'Transfers in':8974480,'Sale of capital assets':13125}
                before = copy.deepcopy(rows)
                self.assertEqual(acfr_funds.governmental_financing_items(rows,load_year(year)),
                    {'Transfers in':8974480,'Inception of leases and subscriptions':18156996,'Sale of capital assets':13125})
                self.assertEqual(rows,before)

    def test_duplicate_financing_aliases_fail_even_if_equal_or_zero(self):
        for wrapped, full in ((19,19),(19,20),(0,0)):
            with self.subTest(values=(wrapped,full)), self.assertRaisesRegex(SafetyError,'Duplicate financing label aliases'):
                acfr_funds.governmental_financing_items(
                    {'subscriptions':wrapped,'Inception of leases and subscriptions':full},load_year(2025))

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


class HistoricalOmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.temp.name)/'proposals'
        cls.before = {p:snapshot(ROOT/p) for p in ('data/funds','data/curation','docs')}
        cls.ledger_dir = Path(cls.temp.name)/'ledgers'
        shutil.copytree(ROOT/'data/funds',cls.ledger_dir)
        for fid in ('011','ACFR-grants','501'):
            shutil.copyfile(FIXTURES/f'{fid}.json',cls.ledger_dir/f'{fid}.json')
        cls.report = breakdown.stage(out=cls.out,ledger_dir=cls.ledger_dir)
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
        self.assertEqual(sum(len(f['proposed_corrections']) for f in self.report['funds']),6)

    def test_audited_financing_values_and_rollforwards(self):
        # Independent visual reading: FY2025 PDF p.77 / printed p.42.
        for fid,lease,net,change in (('011',18156996,-6774558,2124690),
                                  ('ACFR-grants',19381,24222,9337798),
                                  ('501',0,12582617,-3342122)):
            f = self.funds[fid]
            row = next(c for c in f['financing_categories'] if c['source_label']=='subscriptions')
            self.assertEqual(row['source_amount'],lease)
            self.assertEqual(f['omitted_financing'],lease)
            self.assertEqual(f['audited_net_financing'],net)
            self.assertEqual(f['source_financing_sum'],net)
            self.assertEqual(f['proposed_net_financing'],net)
            self.assertEqual(f['proposed_net_change'],change)
            self.assertEqual(f['audited_net_change'],change)
            self.assertTrue(f['balances_reconcile'])
        self.assertEqual(self.report['omitted_financing'],18176377)

    def test_financing_is_separate_from_unchanged_revenue_and_transfers(self):
        for f in self.funds.values():
            old, proposed = f['existing_inflows'], f['proposed_inflows']
            for kind in ('own','rescue'):
                self.assertEqual([r for r in old if r['kind']==kind], [r for r in proposed if r['kind']==kind])
            rows = [r for r in proposed if r['line']=='Inception of leases and subscriptions']
            if f['fund_number'] in ('011','ACFR-grants'):
                self.assertEqual(len(rows),1)
                self.assertEqual(rows[0]['kind'],'financing')
            else:
                self.assertEqual(rows,[])

    def test_three_combined_patches_preserve_all_other_evidence_in_memory(self):
        self.assertEqual(len(list((self.out/'patches').glob('*.json'))),3)
        sums = (self.out/'patches/SHA256SUMS').read_text()
        for fid in ('011','ACFR-grants','501'):
            f = self.funds[fid]
            patch = self.out/f['patch']['path']
            self.assertEqual(breakdown.digest(patch),f['patch']['sha256'])
            self.assertIn(f"{f['patch']['sha256']}  {patch.name}",sums)
            original = json.loads((self.ledger_dir/f'{fid}.json').read_text())
            proposed = copy.deepcopy(original)
            # Evaluate the standard JSON Patch on an in-memory copy only.
            changed_paths = []
            for op in json.loads(patch.read_text()):
                parts = op['path'].strip('/').split('/')
                parent = proposed
                for key in parts[:-1]:
                    parent = parent[key]
                if op['op']=='test':
                    self.assertEqual(parent[parts[-1]],op['value'])
                else:
                    self.assertEqual(op['op'],'replace')
                    changed_paths.append(op['path'])
                    parent[parts[-1]] = copy.deepcopy(op['value'])
            self.assertEqual(changed_paths,['/flow_detail/inflows','/flow_detail/outflows'] if fid!='501' else ['/flow_detail/outflows'])
            for key in ('inflows','outflows'):
                self.assertEqual(proposed['flow_detail'][key],f[f'proposed_{key}'])
                old = original['flow_detail'][key]
                self.assertEqual([r for r in proposed['flow_detail'][key] if r in old],old)
                proposed['flow_detail'][key] = copy.deepcopy(old)
            self.assertEqual(proposed,original)
            self.assertEqual(breakdown.digest(self.ledger_dir/f'{fid}.json'),f['ledger_sha256'])
            # Reproducing a historical omission must recreate the reviewed patch bytes.
            archived = breakdown.HISTORICAL_EVIDENCE/f['patch']['path']
            self.assertEqual(patch.read_bytes(),archived.read_bytes())

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
        stored = json.loads((self.ledger_dir/'011.json').read_text())
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
        breakdown.stage(out=self.out,ledger_dir=self.ledger_dir)
        self.assertEqual(snapshot(self.out), before)
        with self.assertRaises(ValueError):
            breakdown.stage(out=ROOT/'data/funds')


class CurrentLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.temp.name)/'current'
        cls.before = {p:snapshot(ROOT/p) for p in ('data/funds','data/curation','docs','staging/fy2025-expenditure-corrections')}
        cls.report = breakdown.stage(out=cls.out)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_all_five_current_major_funds_have_zero_omissions_or_proposals(self):
        self.assertEqual(self.report['comparison_scope'],'current corrected ledgers')
        self.assertEqual(self.report['omitted_expenditures'],0)
        self.assertEqual(self.report['omitted_financing'],0)
        self.assertEqual(self.report['affected_funds'],0)
        self.assertEqual(len(self.report['funds']),5)
        for f in self.report['funds']:
            self.assertEqual(f['status'],'RECONCILED')
            self.assertEqual(f['omitted_expenditures'],0)
            self.assertEqual(f['omitted_financing'],0)
            self.assertEqual(f['proposed_corrections'],[])
            self.assertNotIn('patch',f)
            self.assertFalse(f['approval_required'])
            self.assertEqual(f['existing_inflows'],f['proposed_inflows'])
            self.assertEqual(f['existing_outflows'],f['proposed_outflows'])
        self.assertFalse((self.out/'patches').exists())

    def test_all_106_current_ledgers_validate(self):
        paths = sorted((ROOT/'data/funds').glob('*.json'))
        self.assertEqual(len(paths),106)
        for path in paths:
            with self.subTest(ledger=path.name):
                errors,_ = ledger.check(path)
                self.assertEqual(errors,[])

    def test_corrections_preserve_annual_figures_and_all_other_evidence(self):
        expected_additions = {'011':(2,1),'ACFR-grants':(1,1),'501':(1,0)}
        for fid,(expenses,financing) in expected_additions.items():
            old = json.loads((FIXTURES/f'{fid}.json').read_text())
            current = json.loads((ROOT/f'data/funds/{fid}.json').read_text())
            self.assertEqual(current['annual'],old['annual'])
            for key,count in (('outflows',expenses),('inflows',financing)):
                original = old['flow_detail'][key]
                corrected = current['flow_detail'][key]
                self.assertEqual(len(corrected)-len(original),count)
                self.assertEqual([r for r in corrected if r in original],original)
                self.assertEqual(len({r['line'] for r in corrected}),len(corrected))
                current['flow_detail'][key] = original
            self.assertEqual(current,old)

    def test_current_reconciliation_is_idempotent_and_preserves_every_input(self):
        before = snapshot(self.out)
        breakdown.stage(out=self.out)
        self.assertEqual(snapshot(self.out),before)
        self.assertEqual({p:snapshot(ROOT/p) for p in self.before},self.before)

    def test_historical_artifacts_and_fixtures_are_pinned_byte_for_byte(self):
        manifest = FIXTURES/'manifest.json'
        self.assertEqual(breakdown.digest(manifest),HISTORY_MANIFEST_SHA256)
        evidence = json.loads(manifest.read_text())
        self.assertEqual(len(evidence['ledgers']),3)
        self.assertEqual(len(evidence['historical_artifacts']),7)
        for item in evidence['ledgers'].values():
            self.assertEqual(breakdown.digest(ROOT/item['fixture']),item['sha256'])
        for path,sha in evidence['historical_artifacts'].items():
            self.assertEqual(breakdown.digest(ROOT/path),sha,path)

    def test_historical_output_paths_are_refused_without_writing(self):
        for out in (breakdown.HISTORICAL_EVIDENCE,breakdown.HISTORICAL_EVIDENCE/'nested'):
            with self.subTest(out=out), self.assertRaisesRegex(SafetyError,'immutable'):
                breakdown.stage(out=out)
        self.assertEqual(snapshot(breakdown.HISTORICAL_EVIDENCE),self.before['staging/fy2025-expenditure-corrections'])

    def test_stale_patch_evidence_is_refused_and_preserved(self):
        out = Path(self.temp.name)/'stale'
        patches = out/'patches'
        patches.mkdir(parents=True)
        evidence = patches/'011.json-patch.json'
        evidence.write_text('prior proposal must not be overwritten or deleted\n')
        before = snapshot(out)
        with self.assertRaisesRegex(SafetyError,'Existing patch evidence would become stale'):
            breakdown.stage(out=out)
        self.assertEqual(snapshot(out),before)


if __name__ == '__main__':
    unittest.main()

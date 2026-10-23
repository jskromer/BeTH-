"""Dashboard integrity tests: totals, scope rules and year handling for tools/build_dashboard.py."""
import itertools
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build_dashboard as bd


class DashboardTotals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = bd.build_model()
        cls.page = bd.render(cls.model)
        cls.fy = cls.model['default_year']
        cls.year = cls.model['years'][cls.fy]

    def test_default_year_is_complete_fy2025(self):
        self.assertEqual(self.fy, 2025)
        self.assertTrue(self.year['complete'])
        self.assertEqual(len(self.model['funds']), 106)

    def test_group_totals_tie_to_statement_total_columns(self):
        controls = json.loads(bd.CONTROLS.read_text())['years'][str(self.fy)]
        for group, entry in self.year['groups'].items():
            with self.subTest(group=group):
                check = entry['check']
                self.assertIn(check['status'], ('ties', 'rounding'))
                for field, diff in check['diffs'].items():
                    self.assertLessEqual(abs(diff), controls['rounding_tolerance'], field)

    def test_transfers_balance_and_are_not_revenue(self):
        self.assertEqual(self.year['transfers']['diff'], 0)
        flows = self.year['flows']
        gov = self.year['groups']['governmental']['totals']
        self.assertEqual(sum(v for _, v in flows['revenue']), gov['rev'])
        self.assertNotIn('Transfers in', dict(flows['revenue']))
        self.assertEqual(gov['rev'], sum(f['years'][self.fy]['rev'] for f in self.model['funds'] if f['group'] == 'governmental'))

    def test_spending_flow_accounts_for_every_dollar(self):
        flows = self.year['flows']
        gov = self.year['groups']['governmental']['totals']
        self.assertEqual(sum(v for _, v in flows['spending']) + flows['not_itemized'], gov['exp'])
        self.assertNotIn('Transfers out', dict(flows['spending']))

    def test_known_gaps_explain_the_not_itemized_amount(self):
        flows = self.year['flows']
        self.assertIsNotNone(flows['explained'])
        self.assertEqual(sum(v for _, v in flows['explained']), flows['not_itemized'])

    def test_balances_of_different_bases_are_never_summed(self):
        bal = {g: e['totals']['bal'] for g, e in self.year['groups'].items()}
        for r in (2, 3):
            for combo in itertools.combinations(bal, r):
                if 'governmental' not in combo:
                    continue
                total = sum(bal[g] for g in combo)
                for text in (bd.money(total), bd.money(total, True)):
                    self.assertNotIn(text, self.page, f'combined balance {combo} rendered as {text}')

    def test_internal_service_revenue_not_added_to_other_groups(self):
        rev = {g: e['totals']['rev'] for g, e in self.year['groups'].items()}
        for combo in (('governmental', 'internal_service'), ('enterprise', 'internal_service'),
                      ('governmental', 'enterprise', 'internal_service')):
            total = sum(rev[g] for g in combo)
            self.assertNotIn(bd.money(total), self.page)
            self.assertNotIn(bd.money(total, True), self.page)

    def test_scope_and_status_labels_present(self):
        for text in ('not City-wide totals', 'Ties within rounding', 'Not yet checked', 'BeTH reading'):
            self.assertIn(text, self.page)

    def test_every_fund_links_to_an_existing_ledger_page(self):
        for f in self.model['funds']:
            with self.subTest(fund=f['id']):
                self.assertTrue((ROOT / 'docs' / f['page']).exists())
                self.assertIn(f'href="{f["page"]}"', self.page)

    def test_fiduciary_roster_is_the_seventeen_without_records(self):
        groups = self.model['fiduciary']['groups']
        self.assertEqual(len(groups['trust']['funds']), 5)
        self.assertEqual(len(groups['custodial']['funds']), 12)
        ledger_names = {f['name'].lower() for f in self.model['funds']}
        for g in groups.values():
            for x in g['funds']:
                self.assertNotIn(x['name'].lower(), ledger_names)
                self.assertIn(bd.esc(x['name']), self.page)
        fund_map = (ROOT / 'docs/berkeley-fund-map.html').read_text()
        self.assertIn('123', fund_map)
        self.assertEqual(len(self.model['funds']) + 17, 123)

    def test_history_excludes_non_statement_series(self):
        hist = {f['id']: f for f in self.model['history']}
        self.assertEqual(set(hist), {f['id'] for f in self.model['funds'] if len(f['years']) > 1 or f['other_series_years']})
        marina = hist['608']
        self.assertEqual(sorted(marina['years']), [2024, 2025])
        self.assertEqual(marina['other_series_years'], list(range(2015, 2024)))

    def test_interpretations_only_for_curated_ledgers(self):
        protected = set(json.loads(bd.REGISTRY.read_text())['ledgers'])
        for f in self.model['funds']:
            self.assertEqual(f['reading'] is not None, f['id'] in protected, f['id'])

    def test_build_is_deterministic(self):
        self.assertEqual(bd.render(bd.build_model()), self.page)


class DashboardYears(unittest.TestCase):
    """New audited years must appear on their own, with totals withheld until complete."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp.name) / 'funds'
        shutil.copytree(bd.DATA_DIR, self.dir)

    def tearDown(self):
        self.temp.cleanup()

    def add_year(self, fy, only=None):
        for p in sorted(self.dir.glob('*.json')):
            d = json.loads(p.read_text())
            if only is not None and d['fund_number'] not in only:
                continue
            y = dict(next(r for r in d['annual'] if r['fy'] == 2025 and r['basis'] == 'audited'), fy=fy, note='test row')
            d['annual'].append(y)
            p.write_text(json.dumps(d))

    def test_partial_year_is_listed_but_totals_withheld(self):
        self.add_year(2023, only={'501', '611'})
        model = bd.build_model(data_dir=self.dir)
        yr = model['years'][2023]
        self.assertFalse(yr['complete'])
        self.assertTrue(all('totals' not in e for e in yr['groups'].values()))
        self.assertIsNone(yr['transfers'])
        self.assertEqual(model['default_year'], 2025)
        page = bd.render(model)
        self.assertIn('data-year="2023"', page)
        self.assertIn('Incomplete: withheld', page)

    def test_complete_year_without_controls_is_marked_unreconciled(self):
        self.add_year(2023)
        model = bd.build_model(data_dir=self.dir)
        yr = model['years'][2023]
        self.assertTrue(yr['complete'])
        self.assertTrue(all(e['check']['status'] == 'unreconciled' for e in yr['groups'].values()))
        self.assertEqual(model['default_year'], 2025)

    def test_known_gap_note_applies_only_on_exact_amount(self):
        p = self.dir / '011.json'
        d = json.loads(p.read_text())
        d['flow_detail']['outflows'].append({'line': 'General government', 'amount': 1})
        p.write_text(json.dumps(d))
        flows = bd.build_model(data_dir=self.dir)['years'][2025]['flows']
        self.assertIsNone(flows['explained'])
        self.assertTrue(any(g['id'] == '011' and g['lines'] is None for g in flows['gaps']))

    def test_rows_without_balance_are_not_statement_rows(self):
        p = self.dir / '611.json'
        d = json.loads(p.read_text())
        d['annual'].append({'fy': 2019, 'basis': 'audited', 'revenue': 1, 'expenditure': 1, 'ending_balance': None,
                            'source': 'acfr-2025', 'confidence': 'High'})
        p.write_text(json.dumps(d))
        model = bd.build_model(data_dir=self.dir)
        self.assertNotIn(2019, model['years'])
        self.assertEqual(next(f for f in model['funds'] if f['id'] == '611')['other_series_years'], [2019])


if __name__ == '__main__':
    unittest.main()

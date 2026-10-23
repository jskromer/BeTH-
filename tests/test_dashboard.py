"""Dashboard integrity tests for tools/build_dashboard.py.

These run in every PR (the extraction-safety workflow discovers tests/). They
check invariants that must hold for any valid ledger data, so legitimate data
growth (new years, new funds, a fixed extraction gap) does not fail them.
Whether docs/dashboard.html has been rebuilt is checked only by the dashboard
workflow (tools/DASHBOARD.md).
"""
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


class DashboardInvariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = bd.build_model()
        cls.page = bd.render(cls.model)
        cls.controls = json.loads(bd.CONTROLS.read_text())['years']

    def complete_years(self):
        return [fy for fy, y in self.model['years'].items() if y['complete']]

    def test_default_year_is_the_latest_complete_year(self):
        self.assertTrue(self.complete_years())
        self.assertEqual(self.model['default_year'], max(self.complete_years()))

    def test_group_totals_tie_to_statement_total_columns(self):
        for fy in self.complete_years():
            for group, entry in self.model['years'][fy]['groups'].items():
                with self.subTest(fy=fy, group=group):
                    if str(fy) not in self.controls:
                        self.assertEqual(entry['check']['status'], 'unreconciled')
                        continue
                    self.assertIn(entry['check']['status'], ('ties', 'rounding'))
                    tol = self.controls[str(fy)]['rounding_tolerance']
                    for field, diff in entry['check']['diffs'].items():
                        self.assertLessEqual(abs(diff), tol, field)

    def test_transfers_balance_and_are_not_revenue(self):
        for fy in self.complete_years():
            yr = self.model['years'][fy]
            self.assertEqual(yr['transfers']['diff'], 0, fy)
            gov = yr['groups']['governmental']['totals']
            self.assertEqual(sum(v for _, v in yr['flows']['revenue']), gov['rev'])
            self.assertNotIn('Transfers in', dict(yr['flows']['revenue']))
            self.assertNotIn('Transfers out', dict(yr['flows']['spending']))

    def test_every_expenditure_dollar_is_itemized_or_shown_as_not_itemized(self):
        for fy in self.complete_years():
            yr = self.model['years'][fy]
            fl = yr['flows']
            self.assertEqual(sum(v for _, v in fl['spending']) + fl['not_itemized'],
                             yr['groups']['governmental']['totals']['exp'], fy)

    def test_no_line_item_gap_is_undocumented(self):
        """Line items lost in a regeneration fail here; a documented gap must match to the dollar."""
        self.assertEqual(self.model['gap_audit']['undocumented'], [])

    def test_not_itemized_amount_is_on_the_page(self):
        fl = self.model['years'][self.model['default_year']]['flows']
        if fl['not_itemized']:
            self.assertIn(f'Known gap in the detail: {bd.money(fl["not_itemized"])}', self.page)
            self.assertIn("Not itemized in BeTH", self.page)

    def test_balances_of_different_bases_are_never_summed(self):
        for fy in self.complete_years():
            bal = {g: e['totals']['bal'] for g, e in self.model['years'][fy]['groups'].items()}
            for r in (2, 3):
                for combo in itertools.combinations(bal, r):
                    if 'governmental' in combo:
                        total = sum(bal[g] for g in combo)
                        self.assertNotIn(bd.money(total), self.page, combo)
                        self.assertNotIn(bd.money(total, True), self.page, combo)

    def test_internal_service_revenue_not_added_to_other_groups(self):
        for fy in self.complete_years():
            rev = {g: e['totals']['rev'] for g, e in self.model['years'][fy]['groups'].items()}
            for combo in (('governmental', 'internal_service'), ('enterprise', 'internal_service'),
                          ('governmental', 'enterprise', 'internal_service')):
                total = sum(rev[g] for g in combo)
                self.assertNotIn(bd.money(total), self.page)
                self.assertNotIn(bd.money(total, True), self.page)

    def test_terms_and_scope_labels_present(self):
        for text in ('not City-wide totals', 'Expenditures', 'Operating expenses', 'Fund balance', 'Net position',
                     'Transfers', 'How internal service funds are handled', 'Not yet checked', 'BeTH reading'):
            self.assertIn(text, self.page)

    def test_every_fund_links_to_an_existing_ledger_page(self):
        for f in self.model['funds']:
            with self.subTest(fund=f['id']):
                self.assertTrue((ROOT / 'docs' / f['page']).exists())
                self.assertIn(f'href="{f["page"]}"', self.page)

    def test_fiduciary_roster(self):
        groups = self.model['fiduciary']['groups']
        self.assertEqual(len(groups['trust']['funds']), 5)
        self.assertEqual(len(groups['custodial']['funds']), 12)
        for g in groups.values():
            for x in g['funds']:
                self.assertIn(bd.esc(x['name']), self.page)

    def test_statement_years_exclude_other_series(self):
        for f in self.model['funds']:
            self.assertFalse(set(f['years']) & set(f['other_series_years']), f['id'])
        marina = next(f for f in self.model['funds'] if f['id'] == '608')
        self.assertTrue(set(range(2015, 2024)) <= set(marina['other_series_years']) | set(marina['years']))

    def test_interpretations_only_for_curated_ledgers(self):
        protected = set(json.loads(bd.REGISTRY.read_text())['ledgers'])
        for f in self.model['funds']:
            self.assertEqual(f['reading'] is not None, f['id'] in protected, f['id'])

    def test_lease_inception_is_financing_never_revenue(self):
        """Lease/subscription inception is an other financing source, not revenue."""
        for fy in self.complete_years():
            fl = self.model['years'][fy]['flows']
            self.assertNotIn(bd.LEASE_INCEPTION, dict(fl['revenue']), fy)
            nc = fl['noncash_capital']
            if nc is None:
                continue
            self.assertEqual(nc['inception'], dict(fl['financing'])[bd.LEASE_INCEPTION], fy)
            self.assertEqual(nc['cash'], nc['outlay'] - nc['inception'], fy)
            # The inception expenditure is reported inside capital outlay, so it
            # can never exceed it; if it did, the split below would be wrong.
            self.assertLessEqual(nc['inception'], nc['outlay'], fy)
            self.assertEqual(nc['outlay'], dict(fl['spending'])[bd.CAPITAL_OUTLAY], fy)

    def test_capital_outlay_is_not_presented_as_all_cash(self):
        fl = self.model['years'][self.model['default_year']]['flows']
        nc = fl['noncash_capital']
        if not nc or not nc['outlay']:
            self.skipTest('no lease or subscription inception in the default year')
        self.assertIn('Capital outlay is not all cash', self.page)
        for v in (nc['outlay'], nc['inception'], nc['cash']):
            self.assertIn(bd.money(v), self.page)

    def test_build_is_deterministic(self):
        self.assertEqual(bd.render(bd.build_model()), self.page)


class DashboardOnChangedData(unittest.TestCase):
    """What the dashboard does when the ledgers change under it (temporary copies only)."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp.name) / 'funds'
        shutil.copytree(bd.DATA_DIR, self.dir)

    def tearDown(self):
        self.temp.cleanup()

    def edit(self, fid, fn):
        p = self.dir / f'{fid}.json'
        d = json.loads(p.read_text())
        fn(d)
        p.write_text(json.dumps(d))

    def add_year(self, fy, only=None):
        for p in sorted(self.dir.glob('*.json')):
            d = json.loads(p.read_text())
            if only is None or d['fund_number'] in only:
                d['annual'].append(dict(next(r for r in d['annual'] if r['fy'] == 2025 and r['basis'] == 'audited'), fy=fy, note='test row'))
                p.write_text(json.dumps(d))

    def test_partial_year_is_listed_but_totals_withheld(self):
        self.add_year(2023, only={'501', '611'})
        model = bd.build_model(data_dir=self.dir)
        yr = model['years'][2023]
        self.assertFalse(yr['complete'])
        self.assertTrue(all('totals' not in e for e in yr['groups'].values()))
        self.assertIsNone(yr['transfers'])
        page = bd.render(model)
        self.assertIn('data-year="2023"', page)
        self.assertIn('Incomplete: withheld', page)

    def test_complete_year_without_controls_is_unreconciled(self):
        self.add_year(2023)
        yr = bd.build_model(data_dir=self.dir)['years'][2023]
        self.assertTrue(yr['complete'])
        self.assertTrue(all(e['check']['status'] == 'unreconciled' for e in yr['groups'].values()))

    def test_lost_line_item_is_caught(self):
        def drop(d):
            spend = [o for o in d['flow_detail']['outflows'] if not bd.NOT_SPENDING.match(o['line'])]
            biggest = max(spend, key=lambda o: o['amount'])
            self.assertGreater(biggest['amount'], 0)
            d['flow_detail']['outflows'].remove(biggest)
        self.edit('ACFR-library', drop)
        model = bd.build_model(data_dir=self.dir)
        self.assertTrue(any(g['id'] == 'ACFR-library' for g in model['gap_audit']['undocumented']))
        self.assertTrue(bd.integrity_problems(model))

    LINE = 'Community development and housing'

    def drop_line(self, fid, line):
        """Remove one outflow line from a fund and return the gap it opens."""
        amounts = []

        def cut(d):
            keep = [o for o in d['flow_detail']['outflows'] if o['line'] != line]
            amounts.append(sum(o['amount'] for o in d['flow_detail']['outflows'] if o['line'] == line))
            d['flow_detail']['outflows'] = keep
        self.edit(fid, cut)
        self.assertGreater(amounts[0], 0, f'{fid} has no {line!r} line to drop')
        return amounts[0]

    def gaps_file(self, fid, gap, line):
        """A scratch known-gaps.json documenting exactly one gap."""
        p = Path(self.temp.name) / 'known-gaps.json'
        p.write_text(json.dumps({'schema_version': 1, 'years': {'2025': {
            'source_page': '77', 'cause': 'Test fixture.',
            'function_totals': {line: gap},
            'funds': {fid: {'gap': gap, 'lines': {line: gap}}}}}}))
        return p

    def test_documented_gap_is_explained_not_flagged(self):
        """While the line is missing and documented to the dollar, the page explains it."""
        gap = self.drop_line('501', self.LINE)
        model = bd.build_model(data_dir=self.dir, known_gaps_path=self.gaps_file('501', gap, self.LINE))
        self.assertEqual(model['gap_audit']['undocumented'], [])
        self.assertEqual(model['gap_audit']['stale'], [])
        self.assertIn('501', {g['id'] for g in model['gap_audit']['documented']})
        fl = model['years'][2025]['flows']
        self.assertEqual(fl['not_itemized'], gap)
        self.assertIn('501', {g['id'] for g in fl['gaps']})
        self.assertEqual(sum(v for _, v in fl['explained']), fl['not_itemized'])
        self.assertIn(f'Known gap in the detail: {bd.money(gap)}', bd.render(model))

    def test_fixed_gap_leaves_a_stale_note_but_no_undocumented_gap(self):
        """Once the line is captured (as the FY2025 p.77 corrections did), the entry must be retired."""
        gap = self.drop_line('501', self.LINE)
        gaps_path = self.gaps_file('501', gap, self.LINE)
        self.edit('501', lambda d: d['flow_detail']['outflows'].append({'line': self.LINE, 'amount': gap}))
        model = bd.build_model(data_dir=self.dir, known_gaps_path=gaps_path)
        self.assertEqual(model['gap_audit']['undocumented'], [])
        self.assertIn('501', {g['id'] for g in model['gap_audit']['stale']})
        self.assertTrue(any('stale entry' in p for p in bd.integrity_problems(model)))
        fl = model['years'][2025]['flows']
        self.assertEqual(fl['not_itemized'], 0)
        self.assertNotIn('501', {g['id'] for g in fl['gaps']})
        self.assertNotIn('Known gap in the detail', bd.render(model))

    def test_changed_audited_figure_is_flagged(self):
        def bump(d):
            next(r for r in d['annual'] if r['fy'] == 2025)['revenue'] += 1
        self.edit('ACFR-library', bump)
        model = bd.build_model(data_dir=self.dir)
        lib = next(f for f in model['funds'] if f['id'] == 'ACFR-library')
        self.assertEqual(lib['audit_match']['status'], 'changed')
        self.assertTrue(any('ACFR-library' in p for p in bd.integrity_problems(model)))

    def test_rows_without_balance_are_not_statement_rows(self):
        self.edit('611', lambda d: d['annual'].append({'fy': 2019, 'basis': 'audited', 'revenue': 1, 'expenditure': 1,
                                                       'ending_balance': None, 'source': 'acfr-2025', 'confidence': 'High'}))
        model = bd.build_model(data_dir=self.dir)
        self.assertNotIn(2019, model['years'])
        self.assertEqual(next(f for f in model['funds'] if f['id'] == '611')['other_series_years'], [2019])


if __name__ == '__main__':
    unittest.main()

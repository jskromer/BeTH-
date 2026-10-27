"""Tests for the "How Did We Get Here?" decision-history prototype (phase2/history).

The prototype must never invent a vote, an expenditure or an outcome: every verified field cites a page that carries
the quoted text, "All Ayes" votes are not expanded into names, alternatives are only those documented at the time, and
the work stays separate from the approved ledgers and the Ask BeTH answers.

Run:  python3 -m unittest discover -s phase2/tests -v
"""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

PHASE2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PHASE2 / 'history' / 'tools'))
import build_history as bh  # noqa: E402

FIELDS = ('decision', 'instrument', 'vote', 'money', 'purpose', 'alternatives', 'actual', 'outcomes', 'outstanding')


ORIGINAL_14 = ['bdh-streets-2012-11-measure-m', 'bdh-streets-2016-11-measure-t1', 'bdh-streets-2020-auditor-rocky-road',
               'bdh-streets-2022-01-25-res-70204', 'bdh-streets-2022-07-26-res-70456',
               'bdh-streets-2022-08-03-res-70492-measure-l', 'bdh-streets-2023-07-25-res-70997',
               'bdh-streets-2023-11-28-res-71120', 'bdh-streets-2024-07-30-res-71461-measure-ff',
               'bdh-streets-2024-12-10-ord-7952', 'bdh-streets-2026-03-17-bond-direction',
               'bdh-streets-2026-06-23-res-72340-budget', 'bdh-streets-2026-07-07-res-72377', 'bdh-streets-2026-11-bond-ballot']


class DecisionHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events, cls.outs = bh.events(), bh.outcomes()
        cls.data = json.loads((PHASE2 / 'history' / 'data' / 'decisions-streets.json').read_text())

    def test_builder_checks_pass(self):
        self.assertEqual(bh.check(self.events, self.outs), [])

    def test_storyboard_size_and_ids(self):
        self.assertTrue(10 <= len(self.events) <= 20)
        self.assertEqual(len(self.events), 16)  # the original 14 plus two found in the 2023 staff report
        ids = [e['id'] for e in self.events]
        self.assertEqual(len(ids), len(set(ids)))
        for i in ids:
            self.assertRegex(i, r'^bdh-streets-\d{4}(-\d{2}(-\d{2})?)?-[a-z0-9-]+$')

    def test_committed_data_matches_builder(self):
        self.assertEqual(self.data['events'], json.loads(json.dumps(self.events)))

    def test_every_field_has_a_status(self):
        for e in self.events:
            for k in FIELDS:
                self.assertIn(e[k]['status'], ('verified', 'to_collect', 'not_in_record'), f'{e["id"]} {k}')
                if e[k]['status'] == 'to_collect':
                    self.assertTrue(e[k]['needed'], f'{e["id"]} {k}')

    def test_all_ayes_not_expanded(self):
        for e in self.events:
            v = e['vote']
            if v['status'] == 'verified' and v['value']['recorded'] == 'All Ayes':
                for k in ('ayes', 'noes', 'abstain', 'absent'):
                    self.assertFalse(v['value'].get(k), f'{e["id"]} lists inferred {k}')

    def test_named_votes_are_quoted(self):
        """Any vote that lists names must cite a page carrying those names in that order."""
        for e in self.events:
            for f in [e['vote'], *e.get('failed_motions', [])]:
                if f['status'] != 'verified' or not f['value'].get('ayes'):
                    continue
                names = ', '.join(f['value']['ayes'])
                self.assertTrue(any(bh.norm(names) in bh.norm(c['quote']) for c in f['citations']), f'{e["id"]}: {names}')

    def test_no_retrospective_scenarios_yet(self):
        for e in self.events:
            self.assertEqual(e['retrospective_scenarios'], [])

    def test_failed_motions_kept_with_votes(self):
        fm = {e['id']: e.get('failed_motions', []) for e in self.events}
        nov23 = fm['bdh-streets-2023-11-28-res-71120'][0]['value']
        self.assertEqual(len(nov23['ayes']), 4)
        self.assertEqual(len(nov23['noes']), 5)
        jun26 = fm['bdh-streets-2026-06-23-res-72340-budget'][0]['value']
        self.assertEqual(jun26['abstain'], ['Humbert'])

    def test_causal_claims_attributed(self):
        o = next(e for e in self.events if e['id'] == 'bdh-streets-2022-07-26-res-70456')['outcomes']['value']
        self.assertIn('City staff', o)
        self.assertIn('not a BeTH finding', o)

    def test_no_scores_or_rankings(self):
        page = (PHASE2 / 'history' / 'docs' / 'timeline.html').read_text().lower()
        self.assertIn('no scores, rankings or ratings of officials', page)
        page = page.replace('no scores, rankings or ratings of officials', '')
        for w in (r'\bscore ?card', r'\bgrade[ds]?\b', r'\branking', r'\brated\b', r'\breport card'):
            self.assertIsNone(re.search(w, page), w)

    def test_outcome_series(self):
        mtc = self.outs['pci_mtc_3yr_moving_average']
        self.assertIn("3-year moving average", mtc["what"].lower())
        self.assertTrue(any('2016' in b for b in mtc['method_breaks']))
        y2018 = sorted({p['pci'] for p in mtc['points'] if p['year'] == 2018})
        self.assertEqual(y2018, [57, 58])  # editions disagree; both kept
        self.assertEqual(self.outs['annual_paving_spending']['status'], 'to_collect')
        miles = {p['fy']: p for p in self.outs['centerline_miles_paved']['points']}
        self.assertEqual(miles['FY2026']['basis'], 'projected')

    def test_images_rights_recorded(self):
        cr = json.loads((PHASE2 / 'history' / 'docs' / 'assets' / 'photos' / 'credits.json').read_text())['photos']
        for use, p in cr.items():
            self.assertEqual(p['license'], 'Public domain', use)
            self.assertTrue(p['license_basis'] and p['source_page'].startswith('https://commons.wikimedia.org/'), use)
            self.assertTrue(p['not_evidence'])
        self.assertEqual(cr['birdseye-1909']['kind'], 'map')

    def test_page_shows_gaps_and_questions(self):
        page = (PHASE2 / 'history' / 'docs' / 'timeline.html').read_text()
        for q in ('What did the Council decide?', 'Who voted for it?', 'What was supposed to happen?',
                  'What actually happened?', 'What alternatives were available?', 'What remains uncertain?'):
            self.assertEqual(page.count(q), len(self.events), q)
        self.assertIn('DRAFT · NOT APPROVED', page)
        self.assertIn('Record not yet collected', page)
        self.assertIn('does not mean the decision caused it', page)
        self.assertNotRegex(page, r'<(script|link|img)[^>]+(src|href)="https?://')

    def test_separate_from_ledgers_and_ask(self):
        out = subprocess.run(['git', 'diff', '--name-only', 'HEAD', '--', 'data/funds', 'data/curation'],
                             capture_output=True, text=True, cwd=PHASE2.parent).stdout
        self.assertEqual(out.strip(), '')
        src = (PHASE2 / 'history' / 'tools' / 'build_history.py').read_text()
        self.assertNotIn('data/funds', src)
        self.assertNotIn('build_answers', src)


class StreetsCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events, cls.outs = bh.events(), bh.outcomes()
        cls.by = {e['id']: e for e in cls.events}

    def test_original_events_and_citations_preserved(self):
        import subprocess as sp
        old = json.loads(sp.run(['git', 'show', '5d95718:phase2/history/data/decisions-streets.json'],
                                capture_output=True, text=True, cwd=PHASE2.parent).stdout)['events']
        for o in old:
            self.assertIn(o['id'], self.by)
            new = json.dumps(self.by[o['id']])
            for c in bh.all_citations(o):
                self.assertIn(json.dumps(c['quote'])[1:-1], new, f'{o["id"]}: citation dropped')
        self.assertEqual([o['id'] for o in old], ORIGINAL_14)

    def test_significance_rule_on_every_event(self):
        for e in self.events:
            self.assertTrue(e['significance'], e['id'])
            for t in e['significance']:
                self.assertIn(t['criterion'], ('recurring', 'major_funding', 'reallocation', 'targets', 'plan_change', 'context'))

    def test_funding_series_labelled(self):
        f = self.outs['street_rehab_funding']
        for p in f['points']:
            self.assertIn(p['value_type'], ('printed', 'image_label', 'measured'))
            self.assertNotIn('actual', p['basis'].split(' ')[0])  # no point claims to be an actual expenditure
        measured = [p['fy'] for p in f['points'] if p['value_type'] == 'measured']
        self.assertEqual(measured, [2014, 2015, 2016, 2017, 2018])
        self.assertTrue(any('Actual expenditures' in g for g in f['gaps']))
        self.assertTrue(any('SB 1' in d for d in f['definition_changes']))

    def test_city_table_error_recorded_not_corrected(self):
        tc = bh.sc.table_checks(bh.page_text, bh.norm)
        self.assertEqual(len(tc['city_table_errors']), 1)
        err = tc['city_table_errors'][0]
        self.assertEqual((err['components_sum'], err['printed_total']), (20236589, 19236589))
        fy27 = next(p for p in self.outs['street_rehab_funding']['points'] if p['fy'] == 2027)
        self.assertIn('July 2026', fy27['basis'])

    def test_competing_proposals_documented(self):
        p22 = self.by['bdh-streets-2022-01-25-res-70204']['competing_proposals']
        self.assertEqual({p['cost_five_year'] for p in p22}, {38385313, 40027381})
        p23 = self.by['bdh-streets-2023-11-28-res-71120']['competing_proposals']
        self.assertTrue(any('Hahn/Wengraf' in p['name'] for p in p23))
        for p in p22 + p23:
            self.assertTrue(p['citations'])
            self.assertNotIn('would have', p['expected_outcome'].lower())

    def test_displacement_findings_qualified(self):
        for d in self.outs['displacement']:
            self.assertTrue(d['status'] and d['citations'])
        st = {d['id']: d['status'] for d in self.outs['displacement']}
        self.assertIn('cause not established', st['disp-1-measure-m-cif'])

    def test_projections_distinct_from_results(self):
        kinds = {p['kind'] for p in self.outs['pci_city_history']}
        self.assertEqual(kinds, {'reported', 'projection'})
        page = (PHASE2 / 'history' / 'docs' / 'timeline.html').read_text()
        self.assertIn('Hollow orange dots: City projections', page)
        self.assertIn('plans, not results', page)


class StreetActuals(unittest.TestCase):
    """Actual expenditures: City-reported to the State Controller, never mixed with budgets or authorizations."""
    @classmethod
    def setUpClass(cls):
        cls.outs = bh.outcomes()
        cls.a = cls.outs['street_expenditures_actual']
        cls.inv = {i['id']: i for i in cls.outs['investigations']}
        cls.file = json.loads((PHASE2 / 'history' / 'data' / 'street-expenditures-actual.json').read_text())

    def test_basis_labelled_on_every_row(self):
        for r in self.a['rows']:
            self.assertIn('State Controller', r['accounting_basis'])
            self.assertIn('not audited', r['accounting_basis'])
            self.assertIn(r['capital_or_operating'], ('capital', 'operating (maintenance)', 'mixed',
                                                      'overhead (design, engineering, administration)'))

    def test_no_appropriation_encumbrance_transfer_or_bond_proceeds(self):
        for r in self.a['rows'] + self.file['street_reconstruction_detail']:
            for k in ('transfers', 'bond_proceeds', 'appropriations_or_encumbrances', 'debt_service'):
                self.assertFalse(r.get('includes', {}).get(k, False), f'FY{r["fy"]} {r["category"]} {k}')
        for p in self.outs['street_rehab_funding']['points']:  # the budget series stays a budget series
            self.assertNotIn('actual', p['basis'].split(' ')[0])

    def test_detail_reconciles_to_summary(self):
        self.assertEqual([c['fy'] for c in self.a['detail_check']], list(range(2018, 2026)))
        for c in self.a['detail_check']:
            self.assertEqual(c['difference'], 0, c)

    def test_known_values(self):
        sr = {s['fy']: s['street_reconstruction'] for s in self.a['series']}
        self.assertEqual((sr[2010], sr[2014], sr[2017], sr[2023], sr[2025]), (1415791, 0, 7296164, 5558322, 21670883))
        self.assertNotIn(2026, sr)  # FY2026 not yet published by the Controller

    def test_printed_report_rows_cite_their_page(self):
        pr = [r for r in self.a['rows'] if r['source_type'] == 'printed_report']
        self.assertEqual(sorted({r['fy'] for r in pr}), list(range(2010, 2018)))
        for r in pr:
            if r['amount']:
                self.assertIn(bh.norm(f'{r["amount"]:,}'), bh.page_text(r['citation']['doc_id'], 1))

    def test_workers_comp_trace(self):
        b = self.inv['B']
        self.assertEqual(b['arithmetic'], {'authorized': 9550000, 'audited_transfers_out_fy2023_2025': 5500000,
                                           'not_visible_in_audited_wc_statements': 4050000})
        self.assertIn('not established', b['answer'])
        self.assertTrue(any('authorization' in f['text'] for f in b['findings']))

    def test_fy2027_arithmetic(self):
        d = self.inv['D']['arithmetic']
        self.assertEqual(d['difference_fy2027'], 994086)
        self.assertEqual(d['base_difference_fy2025'], 937022)
        self.assertTrue(d['plan_2023_is_8937022_at_3pct_from_fy2025'] and d['budget_2026_is_8000000_at_3pct_from_fy2025'])

    def test_moe_is_not_a_compliance_finding(self):
        c = self.inv['C']
        self.assertIn('legal question', c['answer'])
        self.assertTrue(any('not a compliance finding' in x for x in c['caveats']))
        self.assertEqual(c['arithmetic']['total'], 18742503)

    def test_baseline_not_general_fund(self):
        self.assertTrue(self.inv['A']['answer'].startswith('No.'))

    def test_page_labels_actuals(self):
        page = (PHASE2 / 'history' / 'docs' / 'timeline.html').read_text()
        self.assertIn('Actual spending, $M', page)
        self.assertIn('must not be added together', page)
        self.assertIn('DRAFT · NOT APPROVED', page)

    def test_missing_categories_survive_into_series(self):
        points = {s['fy']: s for s in self.a['series']}
        self.assertIsNone(points[2024]['overlay_sealing'])
        self.assertIsNone(points[2024]['patching'])
        self.assertEqual(points[2014]['street_reconstruction'], 0)
        page = (PHASE2 / 'history' / 'docs' / 'timeline.html').read_text()
        self.assertIn('Not reported', page)
        self.assertIn('not reported zeroes', page)

    def test_unknown_categories_do_not_break_checks_or_rendering(self):
        from copy import deepcopy
        outs = deepcopy(self.outs)
        for key in ('street_reconstruction', 'overlay_sealing', 'patching', 'eng_admin', 'grand_total'):
            outs['street_expenditures_actual']['series'][0][key] = None
        self.assertEqual(bh.check_actuals(outs), [])
        self.assertIn('Not reported', bh.actuals_table(outs))

    def test_exports_are_linked_and_match_source_rows(self):
        import csv
        import io
        self.assertEqual(self.file['rows'], self.a['rows'])
        path = PHASE2 / 'history' / 'data' / 'street-expenditures-actual.csv'
        records = list(csv.DictReader(io.StringIO(path.read_text())))
        summary = [r for r in records if r['level'] == 'city total']
        self.assertEqual(len(summary), len(self.a['rows']))
        for exported, source in zip(summary, self.a['rows']):
            self.assertEqual(exported['amount'], '' if source['amount'] is None else str(source['amount']))
        page = (PHASE2 / 'history' / 'docs' / 'timeline.html').read_text()
        for ext in ('json', 'csv'):
            self.assertIn(f'href="../data/street-expenditures-actual.{ext}"', page)

    def test_same_dollars_have_same_chart_height(self):
        funding = {'points': [{'fy': 2025, 'total_m': 10, 'recurring_m': 10,
                                'basis': 'budget', 'value_type': 'printed'}]}
        actuals = [{'fy': 2025, 'street_reconstruction': 10_000_000, 'overlay_sealing': 0, 'patching': 0}]
        chart, _ = bh.sc.sync_chart([], funding, {'points': [{'fy': 'FY2025', 'miles': 1, 'basis': 'actual'}]},
                                    {'points': []}, [], bh.design, actuals)
        heights = re.findall(r'height:([\d.]+)px;background-color:[^"<>]+" title="FY2025 '
                             r'(?:recurring|street reconstruction):', chart)
        self.assertEqual(len(heights), 2)
        self.assertEqual(heights[0], heights[1])


if __name__ == '__main__':
    unittest.main()

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


class DecisionHistory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events, cls.outs = bh.events(), bh.outcomes()
        cls.data = json.loads((PHASE2 / 'history' / 'data' / 'decisions-streets.json').read_text())

    def test_builder_checks_pass(self):
        self.assertEqual(bh.check(self.events, self.outs), [])

    def test_storyboard_size_and_ids(self):
        self.assertTrue(10 <= len(self.events) <= 15)
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


if __name__ == '__main__':
    unittest.main()

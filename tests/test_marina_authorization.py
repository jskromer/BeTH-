"""Council loan approval must not become a Marina receipt or debt balance."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build_fund_page as page
import ledger


class MarinaAuthorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = ROOT / 'data/funds/608.json'
        cls.data = json.loads(cls.path.read_text())
        cls.baseline = json.loads((ROOT / 'tests/fixtures/marina-authorization-baseline.json').read_text())

    def event(self, fid):
        return next(f for f in self.data['flows'] if f['id'] == fid)

    def test_authorization_keeps_original_action_amount_terms_and_citation(self):
        original = self.baseline['authorization']
        current = self.event(original['id'])
        self.assertEqual(current['kind'], 'authorization')
        self.assertEqual(current['amount'], 5500000)
        for field in original.keys() - {'kind', 'note'}:
            self.assertEqual(current[field], original[field], field)
        for sid, source in self.baseline['original_sources'].items():
            self.assertEqual(self.data['sources'][sid], source, sid)
        self.assertEqual(ledger.check(self.path)[0], [])

    def test_only_authorization_is_removed_from_support_tally(self):
        self.assertEqual(page.support_total(self.data['flows']), 17831168)
        previous = copy.deepcopy(self.data['flows'])
        next(f for f in previous if f['id'] == self.baseline['authorization']['id'])['kind'] = 'loan_in'
        self.assertEqual(page.support_total(previous), 23331168)
        self.assertNotIn('authorization', page.RESCUE_KINDS)
        # Additional approvals, however large, must never increase support.
        approval = dict(self.baseline['authorization'], id='another-approval', kind='authorization', amount=999999999)
        self.assertEqual(page.support_total(self.data['flows'] + [approval]), 17831168)
        proposed = dict(approval, kind='loan_in', reviewer='agent:proposed')
        self.assertEqual(page.support_total(self.data['flows'] + [proposed]), 17831168)

    def test_every_annual_value_balance_and_audited_flow_detail_is_unchanged(self):
        for key, expected in self.baseline['unchanged_blocks'].items():
            encoded = json.dumps(self.data[key], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
            self.assertEqual(hashlib.sha256(encoded).hexdigest(), expected, key)

    def test_separate_fy2025_financing_is_preserved_without_a_draw_claim(self):
        financing = self.event('608-fy2025-gf-interfund-loan')
        self.assertEqual((financing['kind'], financing['amount'], financing['fy'], financing['from_fund'],
                          financing['to_fund'], financing['source']),
                         ('loan_in', 2477099, 2025, '011', '608', 'acfr-2025'))
        self.assertIn('No examined source establishes a connection', financing['note'])
        self.assertNotIn('May be a draw', financing['note'])
        authorization = next(o for o in self.data['obligations'] if o['as_of'] == '2023-07-25')
        self.assertEqual((authorization['kind'], authorization['amount']), ('loan_authorization', 5500000))
        self.assertIn('not a measured outstanding', authorization['note'])
        self.assertIn('unverified', authorization['note'])

    def test_generated_page_distinguishes_support_and_authorization(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'fund-608-marina.html'
            with contextlib.redirect_stdout(io.StringIO()):
                page.build(self.path, out)
            first = out.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                page.build(self.path, out)
            self.assertEqual(out.read_bytes(), first)
            self.assertEqual((out.parent / 'data/funds/608.json').read_bytes(), self.path.read_bytes())
        html = first.decode()
        self.assertIn('Loan authorization (not a receipt)</td><td class="n">$5,500,000', html)
        self.assertNotIn('Loan to the fund</td><td class="n">$5,500,000', html)
        self.assertIn('$17.83M', html)
        self.assertNotIn('$23.33M', html)
        self.assertIn('$17,831,168', html)
        self.assertIn('it is not a verified cash-receipt total', html)
        self.assertIn('General Fund 011', html)
        self.assertIn('loan authorization</td><td class="n">$5,500,000', html)
        self.assertIn('Loan to the fund</td><td class="n">$2,477,099', html)
        self.assertEqual((ROOT / 'docs/fund-608-marina.html').read_bytes(), first)


if __name__ == '__main__':
    unittest.main()

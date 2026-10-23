"""Fund-level check of the ledgers against the ACFR statement pages (tools/verify_fund_statements.py).

Reads the PDF, so it needs pdfplumber (tests/requirements.txt). It does not use
the extractor's parser: a fund passes only if its five audited figures appear
together in one statement column, and no two funds share a column.
"""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import verify_fund_statements as vfs

try:
    import pdfplumber  # noqa: F401
    HAVE_PDF = True
except ImportError:
    HAVE_PDF = False


@unittest.skipUnless(HAVE_PDF, 'pdfplumber not installed')
class FundStatementCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = vfs.verify()
        cls.committed = json.loads(vfs.OUT.read_text())

    def test_every_fund_matches_a_statement_column(self):
        bad = {k: v for k, v in self.result['funds'].items() if v['status'] != 'matched'}
        self.assertEqual(bad, {})

    def test_only_statement_total_columns_are_left_over(self):
        # p.77 Other + Total; nonmajor subtotals x3 + Total Nonmajor; proprietary Total + ISF aggregate; ISF Total
        self.assertEqual(self.result['columns_without_a_fund'], {'governmental': 6, 'enterprise': 2, 'internal_service': 1})

    def test_committed_result_agrees_on_status(self):
        # Status only: a corrected FY2025 value that still matches the PDF must not fail an extraction PR.
        # Exact values are compared by `build_dashboard.py --check` in the dashboard workflow.
        self.assertEqual(self.result['pdf_sha256'], self.committed['pdf_sha256'])
        for fid, rec in self.committed['funds'].items():
            self.assertEqual(self.result['funds'].get(fid, {}).get('status'), rec['status'], fid)

    def test_a_one_dollar_change_is_caught(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'funds'
            shutil.copytree(vfs.DATA_DIR, out)
            p = out / 'ACFR-park-tax.json'
            d = json.loads(p.read_text())
            next(r for r in d['annual'] if r['fy'] == 2025)['ending_balance'] += 1
            p.write_text(json.dumps(d))
            res = vfs.verify(data_dir=out)
        self.assertNotEqual(res['funds']['ACFR-park-tax']['status'], 'matched')
        self.assertEqual(res['matched'], len(res['funds']) - 1)


if __name__ == '__main__':
    unittest.main()

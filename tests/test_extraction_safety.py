import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import acfr_funds
from ledger_safety import (SafetyError, annual_key, merge, protected_ids,
                           update_ledgers, validate_annual)
import ledger


def sample():
    return {'fund_number': 'test', 'annual': [{'fy': 2025, 'basis': 'audited',
            'revenue': 10, 'expenditure': 9, 'source': 'audit'}],
            'sources': {'audit': {'title': 'Audit', 'url': 'https://example.org'}}}


class SafetyTests(unittest.TestCase):
    def test_merge_preserves_all_evidence(self):
        existing = sample()
        existing.update(flows=[{'event': 'reviewed'}], obligations=[{'amount': 3}],
                        narrative='reviewed', findings=['finding'], unknown={'keep': True})
        existing['annual'][0]['note'] = 'reviewed note'
        incoming = sample()
        incoming['annual'][0]['fy'] = 2026
        incoming['annual'][0]['source'] = 'new-audit'
        incoming['sources']['new-audit'] = {'title': 'New audit'}
        before = copy.deepcopy(existing)
        result = merge(existing, incoming)
        self.assertEqual(existing, before)
        self.assertEqual(result['annual'][:-1], before['annual'])
        for key in before.keys() - {'annual', 'sources'}:
            self.assertEqual(result[key], before[key])
        self.assertEqual(result['sources']['audit'], before['sources']['audit'])

    def test_conflicting_values_are_errors(self):
        for field in ('revenue', 'expenditure', 'nonoperating', 'transfers_in',
                      'transfers_out', 'ending_balance', 'beginning_balance'):
            incoming = sample()
            incoming['annual'][0][field] = 999
            with self.subTest(field=field), self.assertRaisesRegex(SafetyError, 'conflicting'):
                merge(sample(), incoming)

    def test_duplicate_annual_rows_fail_even_when_identical(self):
        record = sample()['annual'][0]
        for changed in (False, True):
            other = dict(record, revenue=11) if changed else record.copy()
            with self.assertRaisesRegex(SafetyError, 'Duplicate annual'):
                validate_annual([record, other])

    def test_distinct_bases_series_and_balance_versions(self):
        row = sample()['annual'][0]
        rows = [row, dict(row, basis='projected'), dict(row, series='statistical'),
                dict(row, balance_version='original'), dict(row, balance_version='restated')]
        self.assertEqual(len(validate_annual(rows)), 5)

    def test_required_labels_never_default_to_null(self):
        for values in ({}, {'Total revenues': None}, {'Total revenues': '10'}):
            with self.assertRaisesRegex(SafetyError, 'Missing required'):
                acfr_funds.required(values, 'Total revenues')
        self.assertEqual(acfr_funds.required({'Total revenues': 0}, 'Total revenues'), 0)
        with self.assertRaisesRegex(SafetyError, 'Conflicting'):
            acfr_funds.required({'a': 1, 'b': 2}, 'a', 'b')

    def test_batch_conflict_prevents_all_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'test.json'
            path.write_text(json.dumps(sample()))
            before = path.read_bytes()
            fresh = dict(sample(), fund_number='new')
            bad = sample()
            bad['annual'][0]['revenue'] = 999
            with self.assertRaises(SafetyError):
                update_ledgers([fresh, bad], temp)
            self.assertEqual(path.read_bytes(), before)
            self.assertFalse((Path(temp) / 'new.json').exists())

    def test_protection_registry_and_inline_metadata(self):
        self.assertEqual(len(protected_ids()), 6)
        incoming = sample()
        incoming['annual'][0]['fy'] = 2026
        with self.assertRaisesRegex(SafetyError, 'Protected ledger'):
            merge(sample(), incoming, protected=True)
        with self.assertRaises(SafetyError):
            merge(dict(sample(), curation={'status': 'curated'}), incoming)
        with tempfile.TemporaryDirectory() as temp, self.assertRaisesRegex(SafetyError, 'must already exist'):
            update_ledgers([dict(sample(), fund_number='608')], temp)

    def test_source_conflict_preserved(self):
        incoming = sample()
        incoming['annual'][0]['fy'] = 2026
        incoming['sources']['audit']['title'] = 'Different source'
        with self.assertRaisesRegex(SafetyError, 'Conflicting source'):
            merge(sample(), incoming)

    def test_validator_rejects_duplicate_identity(self):
        existing = json.loads((ROOT / 'data/funds/011.json').read_text())
        existing['annual'].append(existing['annual'][0].copy())
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'test.json'
            path.write_text(json.dumps(existing))
            errors, _ = ledger.check(path)
            self.assertTrue(any('Duplicate annual' in e for e in errors))

    def test_exclusive_create_and_append_on_disk(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(update_ledgers([sample()], temp), ['test.json'])
            path = Path(temp) / 'test.json'
            existing = json.loads(path.read_text())
            existing['findings'] = ['reviewed finding']
            path.write_text(json.dumps(existing))
            incoming = sample()
            incoming['annual'][0]['fy'] = 2026
            self.assertEqual(update_ledgers([incoming], temp), ['test.json'])
            result = json.loads(path.read_text())
            self.assertEqual(result['annual'][0], existing['annual'][0])
            self.assertEqual(result['findings'], existing['findings'])
            before = path.read_bytes()
            self.assertEqual(update_ledgers([incoming], temp), [])
            self.assertEqual(path.read_bytes(), before)

    def test_missing_required_statement_labels_abort(self):
        records = acfr_funds.gov_record('test', {
            'Total revenues': 0, 'Total expenditures': 0, 'Transfers in': 0,
            'Transfers out': 0, 'Fund balance, June 30, 2025': 0,
            'Fund balance, July 1, 2024': 0}, 'general', 237)
        self.assertEqual(records['revenue'], 0)
        with self.assertRaises(SafetyError):
            acfr_funds.gov_record('test', {}, 'general', 237)
        with self.assertRaises(SafetyError):
            acfr_funds.prop_record('test', {}, 85)

    def test_duplicate_extracted_funds_fail(self):
        with tempfile.TemporaryDirectory() as temp, self.assertRaisesRegex(SafetyError, 'Duplicate extracted'):
            update_ledgers([sample(), sample()], temp)


class FY2025Regression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = acfr_funds.extract(ROOT / 'annual-comprehensive-financial-report-fy2025.pdf')

    def test_equivalent_to_pre_safety_extractor(self):
        expected = json.loads((ROOT / 'tests/fixtures/fy2025-audited-values.json').read_text())
        actual = {r['fund_number']: [{k: v for k, v in a.items() if k != 'note'} for a in r['annual']] for r in self.records if r['fund_number'] != '608'}
        self.assertEqual(actual, expected['annual'])
        self.assertEqual(hashlib.sha256((ROOT / 'annual-comprehensive-financial-report-fy2025.pdf').read_bytes()).hexdigest(), expected['pdf_sha256'])

    def test_full_extraction_preserves_every_existing_ledger(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'funds'
            shutil.copytree(ROOT / 'data/funds', out)
            before = {p.name: p.read_bytes() for p in out.glob('*.json')}
            with patch.object(acfr_funds, 'extract', return_value=self.records):
                self.assertEqual(acfr_funds.main('already parsed', out), [])
                self.assertEqual(acfr_funds.main('already parsed', out), [])
            self.assertEqual(before, {p.name: p.read_bytes() for p in out.glob('*.json')})
            for fid in protected_ids():
                self.assertEqual((out / f'{fid}.json').read_bytes(), before[f'{fid}.json'])


if __name__ == '__main__':
    unittest.main()

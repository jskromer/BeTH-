"""Regression tests for the Phase 2 answer verifier, capital inventory, funding wording and pavement data.

Covers the failures found in the independent review of commit 6b4e731: the verifier accepted a citation to a
nonexistent page (PDF p.999), a calculation input that resolved to no fact, a stated result that did not follow from
its inputs, and a quote that appeared in the document but not on the cited page. Requires pdftotext and pdfinfo.

Run:  python3 -m unittest discover -s phase2/tests -v
"""
import copy
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build_answers as ba  # noqa: E402

DATA = ROOT / 'data'


def load(name):
    return json.loads((DATA / name).read_text())


def built(slug):
    fn = next(f for f in ba.ANSWERS if f.__name__ == 'answer_' + slug.replace('-', '_'))
    return fn()


def problems(ans):
    return ba.verify(copy.deepcopy(ans))['verifier']['problems']


class VerifierRejects(unittest.TestCase):
    def test_current_answers_pass(self):
        for f in ba.ANSWERS:
            ans = ba.verify(f())
            self.assertEqual(ans['verifier']['problems'], [], ans['slug'])
            self.assertTrue(ans['verifier']['structural_checks_passed'])
            self.assertEqual(ans['verifier']['independent_source_verification']['status'], 'NOT PERFORMED')

    def test_nonexistent_page(self):
        ans = built('capital-to-streets')
        ans['facts'][0]['cite']['pdf_page'] = ans['facts'][0]['cite']['pdf_page_last'] = 999
        self.assertTrue(any('PDF p.999 does not exist' in p for p in problems(ans)))

    def test_page_range_past_end(self):
        ans = built('street-condition')
        f = next(f for f in ans['facts'] if f['fact_id'] == 'pave:network/2024/miles-below-50')
        f['cite']['pdf_page_last'] = 159  # the PTAP PDF has 158 pages
        self.assertTrue(any('PDF p.159 does not exist' in p for p in problems(ans)))

    def test_missing_page(self):
        ans = built('streets-139m')
        ans['facts'][0]['cite']['pdf_page'] = None
        self.assertTrue(any('no valid PDF page' in p for p in problems(ans)))

    def test_unknown_document(self):
        ans = built('streets-139m')
        ans['facts'][0]['cite']['doc_id'] = 'doc:nonexistent'
        self.assertTrue(any('unknown document' in p for p in problems(ans)))

    def test_unresolved_calculation_input(self):
        # the 6b4e731 streets-139m answer used the input 'cip:streets', which named no fact
        ans = built('streets-139m')
        ans['calculations'][1]['inputs'] = ['cip:streets']
        self.assertTrue(any("input 'cip:streets' does not resolve" in p for p in problems(ans)))

    def test_inconsistent_arithmetic(self):
        ans = built('capital-to-streets')
        ans['calculations'][0]['result'] += 1000
        self.assertTrue(any('calculation c1: stated result' in p for p in problems(ans)))

    def test_inconsistent_ratio(self):
        ans = built('measure-ff-paving')
        ans['calculations'][0]['result'] = 0.50
        self.assertTrue(any('calculation c1: stated result' in p for p in problems(ans)))

    def test_inconsistent_inputs(self):
        # a fact value that disagrees with its data record breaks the chain into every calculation using it
        ans = built('capital-to-streets')
        f = next(f for f in ans['facts'] if f['fact_id'] == 'fund:501/cip/fy2028/other')
        f['value'] += 1
        ps = problems(ans)
        self.assertTrue(any('!= record' in p for p in ps))
        self.assertTrue(any('calculation c1: stated result' in p for p in ps))

    def test_unresolvable_record(self):
        ans = built('streets-139m')
        ans['facts'][0]['record'] = 'cip-projects.json:reconciliation/no_such_key'
        self.assertTrue(any('does not resolve' in p for p in problems(ans)))

    def test_number_without_record_or_page(self):
        ans = built('streets-139m')
        f = ans['facts'][0]
        f['record'], f['printed'] = None, False
        self.assertTrue(any('neither a data record nor a printed check' in p for p in problems(ans)))

    def test_printed_value_not_on_cited_page(self):
        ans = built('capital-to-streets')
        f = next(f for f in ans['facts'] if f['fact_id'] == 'fund:501/acfr/2025/assigned')
        f['cite']['pdf_page'] = f['cite']['pdf_page_last'] = 76
        self.assertTrue(any('not found on doc:acfr-fy2025 PDF p.76' in p for p in problems(ans)))

    def test_quote_on_wrong_page(self):
        # the quote exists in the document (PDF p.180) but not on the page cited
        ans = built('capital-to-streets')
        f = next(f for f in ans['facts'] if f['fact_id'] == 'doc:acfr-fy2025/carryover-rule')
        f['cite']['pdf_page'] = f['cite']['pdf_page_last'] = 179
        self.assertTrue(any('quote not on cited page' in p for p in problems(ans)))

    def test_ordinance_quote_on_wrong_page(self):
        ans = built('measure-ff-paving')
        f = next(f for f in ans['facts'] if f['fact_id'] == 'law:bmc-7.11-section-7a3')
        f['cite']['pdf_page'] = f['cite']['pdf_page_last'] = 14
        self.assertTrue(any('quote not on cited page' in p for p in problems(ans)))

    def test_fabricated_quote(self):
        ans = built('measure-ff-paving')
        ans['facts'][0]['cite']['quote'] = 'Council may reallocate the proceeds at will'
        self.assertTrue(any('quote not on cited page' in p for p in problems(ans)))

    def test_untraced_prose_number(self):
        ans = built('capital-to-streets')
        ans['short_answer'] += ' Up to $5,000,000 could move.'
        self.assertTrue(any("'$5,000,000'" in p for p in problems(ans)))

    def test_untraced_prose_percentage_and_miles(self):
        ans = built('street-condition')
        ans['short_answer'] += ' About 73% of streets, 101.2 miles, are fine.'
        ps = problems(ans)
        self.assertTrue(any("'73%'" in p for p in ps))
        self.assertTrue(any('101.2 miles' in p for p in ps))

    def test_counterargument_required(self):
        ans = built('streets-139m')
        ans['interpretation'][0]['counterargument'] = ''
        self.assertTrue(any('no counterargument' in p for p in problems(ans)))

    def test_text_fact_needs_quote(self):
        ans = built('measure-ff-paving')
        ans['facts'][0]['cite']['quote'] = None
        self.assertTrue(any('text fact without a quote' in p for p in problems(ans)))


class Wording(unittest.TestCase):
    def test_no_verified_badge(self):
        for f in ba.ANSWERS:
            html = ba.render(ba.verify(f()))
            self.assertNotIn('>Verified', html)
            self.assertIn('Not independently source-verified', html)
        self.assertNotIn('>verified<', ba.render_index([ba.verify(f()) for f in ba.ANSWERS]))

    def test_no_measure_ff_vote_conclusion(self):
        pat = re.compile(r'nothing beyond the adopted plan|\$0 (more|beyond)|No, not without a vote|No further Measure FF',
                         re.I)
        for f in ('street-funding-sources.json', 'funding-restrictions.json', 'pci-model.json'):
            self.assertIsNone(pat.search((DATA / f).read_text()), f)
        for f in ba.ANSWERS:
            self.assertIsNone(pat.search(json.dumps(f())), f.__name__)
        self.assertIsNone(pat.search((ROOT / '07-street-funding-legal-analysis.md').read_text().replace(
            'concluded "$0 beyond the adopted plan without a vote of the people"', '')))

    def test_fund_501_ceilings(self):
        a = load('street-funding-sources.json')['funding_sources'][0]['available_for_paving']
        self.assertEqual(a['gross_conditional_deferral_ceiling_fy2027_fy2028'], 2946000)
        self.assertEqual(a['deferral_ceiling_excluding_contractual_jpa'], 2916000)
        self.assertTrue(a['not_verified_available_cash'])
        self.assertNotIn('upper_bound_new_appropriations_fy2027_fy2028', a)

    def test_measure_ff_unresolved(self):
        ff = load('street-funding-sources.json')['funding_sources'][1]
        self.assertEqual(ff['available_for_paving']['additional_beyond_adopted_plan']['status'], 'UNRESOLVED LEGAL QUESTION')
        self.assertGreaterEqual(len(ff['available_for_paving']['unresolved_questions']), 5)
        self.assertIn('Alter the allocations', ff['allocation_fixed_by_voters']['council_cannot_without_voters'])


class CapitalInventory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cip = load('cip-projects.json')
        cls.tables = cls.cip['reconciliation']['city_summary_tables']

    def test_fleet_total(self):
        fleet = self.cip['excluded_categories'][0]
        self.assertEqual(fleet['category'], 'Equipment & Fleet')
        self.assertEqual(fleet['by_year']['five_year'], 33331116)

    def test_no_ev_charger_double_count(self):
        funded = sum(f['five_year_budget'] for p in self.cip['projects'] for f in p['funding'] if f['fund'] != 'UNFUNDED')
        ev = sum(f['five_year_budget'] for p in self.cip['projects'] for f in p['funding'] if f['fund'] == '671')
        self.assertEqual(ev, 6021000)
        self.assertEqual(funded + 33331116, 410618590)

    def test_both_city_totals_kept(self):
        t = self.tables['city_totals']
        self.assertEqual(t['by_category_p169'], 410618590)
        self.assertEqual(t['by_funding_source_p170_sum_of_group_totals'], 410468590)
        self.assertEqual(t['difference'], 150000)
        self.assertEqual(t['project_funding_absent_from_p170'], {'621': 150000})
        self.assertIn('Clariti', t['explanation'])
        self.assertIn('Unresolved', t['explanation'])

    def test_every_funding_source_row_reconciled(self):
        rows = self.tables['funding_sources_p170']
        self.assertEqual(len(rows), 29)
        self.assertTrue(all(r['match'] for r in rows.values()), [k for k, r in rows.items() if not r['match']])

    def test_every_category_reconciled(self):
        cats = {k: v for k, v in self.tables['categories_p169'].items() if k != 'Equipment & Fleet'}
        self.assertEqual(len(cats), 11)
        self.assertTrue(all(v['match'] for v in cats.values()))

    def test_documented_exceptions_kept(self):
        r = self.cip['reconciliation']
        self.assertIn('Storm Water', r['category_project_counts_match_document'])
        self.assertTrue(r['printed_total_rounding_differences'])


class Pavement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nc = load('network-condition.json')

    def test_mileage_from_feet(self):
        p = self.nc['validation']['parsed']
        self.assertAlmostEqual(p['centerline_miles_from_feet'], 212.778, places=3)
        self.assertEqual(p['centerline_miles_sum_of_rounded_section_miles'], 213.48)
        self.assertEqual(self.nc['distribution']['below_pci_50']['centerline_miles'], 88.5)
        self.assertEqual(self.nc['distribution']['below_pci_25']['centerline_miles'], 33.9)

    def test_tevlin_uninspected_not_an_error(self):
        u = self.nc['validation']['uninspected_section']
        self.assertNotIn('report_inconsistency', self.nc['validation'])
        self.assertEqual([s['area_sqft'] for s in u['sections']], [3875])
        self.assertIn('TEVLIN', u['sections'][0]['text'])
        self.assertIsNone(u['sections'][0]['pci_date'])

    def test_condition_breakdown_citation(self):
        self.assertIn('Executive Summary p.4 / PDF p.7', self.nc['source']['pages'])
        pm = load('pci-model.json')
        self.assertNotIn('pp.2-3', json.dumps(pm))
        self.assertIn('41.93% are in poor to failed condition', ba.page_text('doc:ptap25', 7))


if __name__ == '__main__':
    unittest.main()

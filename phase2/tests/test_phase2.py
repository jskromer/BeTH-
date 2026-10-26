"""Regression tests for the Phase 2 answer verifier, capital inventory, funding wording and pavement data.

Covers the failures found in the independent review of commit 6b4e731: the verifier accepted a citation to a
nonexistent page (PDF p.999), a calculation input that resolved to no fact, a stated result that did not follow from
its inputs, and a quote that appeared in the document but not on the cited page. Requires pdftotext and pdfinfo.

Run:  python3 -m unittest discover -s phase2/tests -v
"""
import copy
from html.parser import HTMLParser
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build_answers as ba  # noqa: E402

DATA = ROOT / 'data'
APPROVAL = {'status': 'NOT APPROVED'}


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

    def test_quoted_dollar_amount_not_exempt(self):
        # 079d23d skipped any dollar figure preceded by a quotation mark
        ans = built('streets-139m')
        ans['interpretation'][0]['text'] += ' It is often quoted as "$999.9 million".'
        self.assertTrue(any("'$999.9 million'" in p for p in problems(ans)))

    def test_arithmetic_rendered_from_recomputation(self):
        # the displayed arithmetic must come from the verifier's recomputation, not the stated result or expression
        ans = ba.verify(built('capital-to-streets'))
        c = ans['calculations'][0]
        c['result'], c['expression'] = 1, 'TYPED-IN EXPRESSION'
        html = ba.render(ans, APPROVAL)
        self.assertIn('$1,473,000 + $1,473,000 = <b>$2,946,000</b>', html)
        self.assertNotIn('TYPED-IN EXPRESSION', html)

    def test_render_refuses_failed_answer(self):
        ans = built('capital-to-streets')
        ans['calculations'][0]['result'] += 1
        with self.assertRaises(ValueError):
            ba.render(ba.verify(ans), APPROVAL)

    def test_verifier_states_its_limits(self):
        v = ba.verify(built('measure-ff-paving'))['verifier']
        self.assertEqual(v['kind'], 'automated structural checks')
        text = ' '.join(v['does_not_establish'])
        for k in ('legal interpretation', 'calculation method', 'consistent with one another', 'human source verification'):
            self.assertIn(k, text)
        self.assertEqual(v['independent_source_verification']['status'], 'NOT PERFORMED')

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
            html = ba.render(ba.verify(f()), APPROVAL)
            self.assertNotIn('>Verified', html)
            self.assertIn('Not yet confirmed by a person', html)
        self.assertNotIn('>verified<', ba.render_index([ba.verify(f()) for f in ba.ANSWERS], ba.load_approvals()))

    def test_no_measure_ff_vote_conclusion(self):
        pat = re.compile(r'nothing beyond the adopted plan|\$0 (more|beyond)|No, not without a vote|No further Measure FF',
                         re.I)
        for f in ('street-funding-sources.json', 'funding-restrictions.json', 'pci-model.json'):
            self.assertIsNone(pat.search((DATA / f).read_text()), f)
        for f in ba.ANSWERS:
            self.assertIsNone(pat.search(json.dumps(f())), f.__name__)
        self.assertIsNone(pat.search((ROOT / '07-street-funding-legal-analysis.md').read_text().replace(
            'concluded "$0 beyond the adopted plan without a vote of the people"', '')))

    def test_dashboard_filter_and_goal_wording(self):
        page = (ROOT / 'docs' / 'budget-choices.html').read_text()
        self.assertIn('total project funding from all sources', page)
        self.assertIn('itself: ', page)
        self.assertIn('ideally with no streets having a PCI below 50', page)
        ps = json.loads((ROOT / 'docs' / 'data' / 'phase2.json').read_text())['capital']['projects']
        sel = [p for p in ps if any(f['fund'] == '501' for f in p['funding'])]
        self.assertEqual(sum(p['two_year_adopted'] for p in sel), 46165622)  # all sources
        self.assertEqual(sum(f['fy2027'] + f['fy2028'] for p in sel for f in p['funding'] if f['fund'] == '501'), 24025016)

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


class _Visible(HTMLParser):
    """Text a reader sees by default: skips <style>, <script> and anything inside class="tech"."""
    VOID = {'br', 'img', 'input', 'meta', 'link', 'hr'}

    def __init__(self):
        super().__init__()
        self.stack, self.out = [], []

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        hidden = tag in ('style', 'script') or 'tech' in (dict(attrs).get('class') or '').split()
        self.stack.append(hidden or (self.stack[-1] if self.stack else False))

    def handle_endtag(self, tag):
        if tag not in self.VOID and self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if not (self.stack and self.stack[-1]):
            self.out.append(data)


def visible(html):
    v = _Visible()
    v.feed(html)
    return ' '.join(' '.join(v.out).split())


def pages():
    ap = ba.load_approvals()
    return {a['slug']: (a, ba.render(a, ap[a['slug']])) for a in (ba.verify(f()) for f in ba.ANSWERS)}


class Presentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = pages()

    def test_one_template(self):
        heads = None
        for slug, (a, h) in self.pages.items():
            got = re.findall(r'<summary>([^<]+)', h)
            heads = heads or got
            self.assertEqual(got, heads, slug)
            for k in ('Short answer', 'What you should know', 'Show technical references', 'id="tech"'):
                self.assertIn(k, h, slug)

    def test_short_conclusion_first(self):
        for slug, (a, h) in self.pages.items():
            self.assertLessEqual(len(a['headline']), 260, slug)
            self.assertLess(h.index(html_escape(a['headline'])), h.index('<details>'), slug)

    def test_uncertainties_visible_and_complete(self):
        for slug, (a, h) in self.pages.items():
            vis = visible(h)
            for x in a['key_uncertainties']:
                self.assertIn(' '.join(x.split()), vis, slug)
            for x in a['open_interpretations']:
                self.assertIn(' '.join(x.split()), vis, slug)
            self.assertIn(f'Open questions ({len(a["open_interpretations"])})', vis)

    def test_technical_ids_hidden_but_kept(self):
        idpat = re.compile(r'\b(fund:501/|ff:program/|pave:|cip:streets|law:bmc|plan:table|doc:[a-z]|\.json:)')
        for slug, (a, h) in self.pages.items():
            self.assertIsNone(idpat.search(visible(h)), slug)
            for f in a['facts']:
                self.assertIn(f['fact_id'], h, slug)
                if f.get('record'):
                    self.assertIn(html_escape(f['record']), h, slug)
            self.assertIn('href="../assets/ask.css"', h)
        self.assertIn('body:has(#tech:checked) .tech{display:block}', (ROOT / 'docs' / 'assets' / 'ask.css').read_text())
        self.assertIn('.tech{display:none', (ROOT / 'docs' / 'assets' / 'ask.css').read_text())

    def test_evidence_and_arithmetic_kept(self):
        for slug, (a, h) in self.pages.items():
            for f in a['facts']:
                self.assertIn(html_escape(ba.pdf_href(f['cite'])), h, slug)
            for c in a['verifier']['arithmetic']:
                self.assertIn(ba.fmt({'value': c['recomputed'], 'unit': c['unit']}), h, slug)
            self.assertIn(html_escape(a['short_answer']), h)
            for m in a['missing_evidence']:
                self.assertIn(html_escape(m['needed']), h)

    def test_status_matches_approval_record(self):
        ap = ba.load_approvals()
        for slug, (a, h) in self.pages.items():
            self.assertIn(ba.APPROVAL_TEXT[ap[slug]['status']], visible(h), slug)
            self.assertIn('Not yet confirmed by a person', visible(h))
            self.assertNotIn('Verified', visible(h))

    def test_paving_gap_comparison(self):
        a, h = self.pages['capital-to-streets']
        t = a['interpretation'][0]['text']
        self.assertIn('additional spending beyond its modeled', t)
        self.assertIn('not available cash', t)
        self.assertIn('would not close the modeled gap', t)

    def test_punctuation(self):
        for slug, (a, h) in self.pages.items():
            items = [a['headline'], *a['key_uncertainties'], *a['open_interpretations'],
                     *(m['needed'] for m in a['missing_evidence']),
                     *(t for i in a['interpretation'] for t in (i['text'], i['counterargument']))]
            for x in items:
                self.assertRegex(x.strip(), r'[.?!)"]$', f'{slug}: {x[-40:]}')
            self.assertTrue(a['question'].endswith('?'))


def html_escape(s):
    import html as _h
    return _h.escape(s)


class ReviewChecklist(unittest.TestCase):
    def test_approvals_recorded_by_hand_with_allowed_status(self):
        ap = json.loads((ROOT / 'review' / 'human-approvals.json').read_text())
        self.assertEqual(set(ap['answers']), {f().get('slug') for f in ba.ANSWERS})
        for slug, a in ap['answers'].items():
            self.assertIn(a['status'], ap['allowed_status'], slug)
            if a['status'] != 'NOT APPROVED':
                self.assertTrue(a['reviewer'] and a['date'], f'{slug}: approval without reviewer and date')

    def test_checklist_covers_each_answer(self):
        md = (ROOT / 'review' / 'human-review-checklist.md').read_text()
        for f in ba.ANSWERS:
            a = ba.verify(f())
            self.assertIn(a['short_answer'], md)
            self.assertTrue(a['open_interpretations'])
            for x in a['open_interpretations']:
                self.assertIn(x, md)
            for fct in a['facts']:
                self.assertIn(fct['label'].replace('|', '\\|'), md)
        self.assertEqual(md.count('### Independent human approval'), len(ba.ANSWERS))


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


class Design(unittest.TestCase):
    """Presentation-only redesign: photographs carry established rights and credits; highlights and charts use
    verified values or committed data; nothing here may change what is verified."""

    @classmethod
    def setUpClass(cls):
        import ask_design
        cls.d = ask_design
        cls.credits = json.loads((ROOT / 'docs' / 'assets' / 'photos' / 'credits.json').read_text())
        cls.pages = pages()

    def test_photo_rights_recorded(self):
        import hashlib
        allowed = {'CC0', 'Public domain', 'CC BY 2.0', 'CC BY 3.0', 'CC BY 4.0', 'CC BY-SA 2.5', 'CC BY-SA 3.0',
                   'CC BY-SA 4.0'}
        self.assertEqual(set(self.credits['photos']), {'home', *self.d.PRESENTATION})
        for use, p in self.credits['photos'].items():
            for k in ('file', 'source_page', 'author', 'license', 'license_url', 'date', 'location', 'alt',
                      'description', 'credit_line', 'sha256'):
                self.assertTrue(p.get(k), f'{use}: {k}')
            self.assertIn(p['license'], allowed, use)
            self.assertTrue(p['source_page'].startswith('https://commons.wikimedia.org/wiki/File:'), use)
            self.assertTrue(p['not_evidence'])
            data = (ROOT / 'docs' / p['file']).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), p['sha256'], use)

    def test_every_image_is_credited_and_captioned(self):
        files = {p['file'] for p in self.credits['photos'].values()}
        for name in ('index', 'capital-to-streets', 'measure-ff-paving', 'street-condition', 'streets-139m',
                     'photo-credits'):
            h = (ROOT / 'docs' / 'ask' / f'{name}.html').read_text()
            srcs = re.findall(r'<img src="\.\./([^"]+)"', h)
            self.assertTrue(srcs, name)
            for s in srcs:
                self.assertIn(s, files, name)
                p = next(p for p in self.credits['photos'].values() if p['file'] == s)
                self.assertIn(html_escape(p['source_page']), h, name)
                self.assertIn(html_escape(p['license']), h, name)
            self.assertNotRegex(h, r'<img src="https?://', name)
            if name != 'photo-credits':
                self.assertIn('Illustrative photo', h, name)
                self.assertIn('does not show evidence for the figures on this page', h, name)

    def test_home_heading(self):
        h = (ROOT / 'docs' / 'ask' / 'index.html').read_text()
        self.assertIn('<h1>Ask BeTH</h1>', h)
        self.assertIn('Where does Berkeley’s money go? What are we getting for it?', h)
        self.assertEqual(h.count('class="card"'), 5)

    def test_highlights_are_verified_values(self):
        for slug, (a, h) in self.pages.items():
            facts = {f['fact_id']: f for f in a['facts']}
            calcs = {c['id']: c for c in a['verifier']['arithmetic']}
            hl = self.d.PRESENTATION[slug]['highlights']
            self.assertTrue(2 <= len(hl) <= 3, slug)
            for ref, _ in hl:
                self.assertTrue(ref in facts or ref in calcs, f'{slug}: {ref}')
                v = (ba.fmt({'value': calcs[ref]['recomputed'], 'unit': calcs[ref]['unit']}) if ref in calcs
                     else ba.fmt(facts[ref]))
                self.assertIn(f'<div class="stat-v">{html_escape(v)}</div>', h, slug)

    def test_charts_match_data(self):
        nc = load('network-condition.json')['distribution']
        h = self.pages['street-condition'][1]
        for k, b in nc['by_mtc_band'].items():
            self.assertIn(f'{b["centerline_miles"]:.1f} mi', h)
        below = nc['by_mtc_band']['poor (25-49)']['centerline_miles_unrounded'] + \
            nc['by_mtc_band']['failed (0-24)']['centerline_miles_unrounded']
        self.assertAlmostEqual(below, nc['below_pci_50']['centerline_miles_unrounded'], places=6)
        self.assertIn(f'Below PCI 50: {nc["below_pci_50"]["centerline_miles"]:.1f} miles in all', h)
        t = load('cip-projects.json')['categories']['Streets']['printed_grand_total']
        h = self.pages['streets-139m'][1]
        self.assertIn(f'Two years: ${t["fy2027"] + t["fy2028"]:,}', h)
        self.assertIn(f'Five years: ${t["five_year_budget"]:,}', h)
        prog = load('street-funding-sources.json')['funding_sources'][1]['allocation_fixed_by_voters']['adopted_five_year_program']
        h = self.pages['measure-ff-paving'][1]
        self.assertIn(f'Street rehabilitation <b>{prog["street_rehabilitation_cip"] / prog["total"]:.1%}</b>', h)
        a = load('street-funding-sources.json')['funding_sources'][0]['appropriations_adopted_cip']['fy2027']
        h = self.pages['capital-to-streets'][1]
        self.assertIn(f'Paving <b>${a["paving"]:,}</b>', h)
        self.assertIn('Budget amounts, not cash', h)

    def test_no_external_resources(self):
        for f in (ROOT / 'docs' / 'ask').glob('*.html'):
            h = f.read_text()
            self.assertNotRegex(h, r'<(script|link|img)[^>]+(src|href)="https?://', f.name)


class Marina(unittest.TestCase):
    """The Marina question: accounting distinctions the answer must keep, and the protected ledger left alone."""

    @classmethod
    def setUpClass(cls):
        cls.a = ba.verify(ba.answer_marina())
        cls.facts = {f['fact_id']: f for f in cls.a['facts']}
        cls.text = ' '.join([cls.a['headline'], cls.a['short_answer'], *cls.a['key_uncertainties'],
                             *cls.a['open_interpretations'], *(p['a'] for p in cls.a['parts']),
                             *(i['text'] + ' ' + i['counterargument'] for i in cls.a['interpretation'])])

    def test_passes_structural_checks(self):
        self.assertEqual(self.a['verifier']['problems'], [])

    def test_three_public_questions(self):
        self.assertEqual([p['q'] for p in self.a['parts']],
                         ['Does the Marina cover its costs?', 'If not, who pays the difference?',
                          'What would it take to make the waterfront financially sustainable?'])

    def test_not_approved(self):
        ap = ba.load_approvals()
        self.assertEqual(ap['marina']['status'], 'NOT APPROVED')
        self.assertEqual(self.a['verifier']['independent_source_verification']['status'], 'NOT PERFORMED')

    def test_evidence_classes_labelled(self):
        b = {fid: f['basis'] for fid, f in self.facts.items()}
        self.assertEqual(b['acfr25:608/operating-revenue'], 'audited')
        self.assertEqual(b['bf26:fy2026/revenue'], 'staff_unaudited')
        self.assertEqual(b['bf26:fy2027/revenue'], 'projection')
        self.assertEqual(b['loan:2023-07-25/authorization'], 'authorization')
        for fid, f in self.facts.items():
            if fid.startswith('bf26:fy2026/'):
                self.assertNotEqual(f['basis'], 'audited', fid)

    def test_loan_authorization_not_revenue(self):
        cal = {c['id']: c for c in self.a['calculations']}
        for c in cal.values():
            self.assertNotIn('loan:2023-07-25/authorization', c['inputs'])
            self.assertNotIn('acfr25:608/interfund-loan-receipt', c['inputs'])
        self.assertIn('financing, not revenue', self.facts['acfr25:608/interfund-loan-receipt']['label'])
        self.assertIn('going to the General Fund', ' '.join(self.a['key_uncertainties']))

    def test_unpaid_rent_not_written_off(self):
        self.assertNotRegex(self.text, r'(?i)(was|were|been|is) written off')
        self.assertIn('not written off', self.text)
        self.assertEqual(self.facts['bf26:doubletree/owed-oct-2026']['value'], 1000000)
        self.assertEqual(self.facts['bf26:doubletree/paid-sept-2025']['value'], 964680)
        self.assertEqual(self.facts['bf26:doubletree/budgeted']['value'], 840000)

    def test_not_all_on_boaters(self):
        t = self.text
        self.assertIn('policy choice', t)
        self.assertIn('not only boaters', t)

    def test_discrepancies_preserved(self):
        t = ' '.join(self.a['open_interpretations'])
        for k in ('Equipment Replacement Fund', 'one dollar less', 'different amounts for General Fund support',
                  'measure different things', 'at least 35%'):
            self.assertIn(k, t)
        v = {fid: f['value'] for fid, f in self.facts.items()}
        self.assertEqual(v['bf26:fy2026/leases'] + v['bf26:fy2026/berthers'] + v['bf26:fy2026/other'],
                         v['bf26:fy2026/revenue'] - 1)

    def test_highlights_and_chart(self):
        h = ba.render(self.a, {'status': 'NOT APPROVED'})
        self.assertEqual(h.count('class="stat"'), 3)
        self.assertIn('Marina Fund revenue and expenses by year', h)
        self.assertIn('Who has covered the gap', h)
        self.assertIn('not added up', h)
        self.assertIn('data-photo="marina"', h)

    def test_protected_ledger_untouched(self):
        import subprocess
        out = subprocess.run(['git', 'diff', '--name-only', 'HEAD', '--', 'data/funds', 'data/curation'],
                             capture_output=True, text=True, cwd=ROOT.parent).stdout
        self.assertEqual(out.strip(), '')
        self.assertTrue((ROOT / 'flags' / '2026-10-25-marina-608-ledger-review.md').exists())

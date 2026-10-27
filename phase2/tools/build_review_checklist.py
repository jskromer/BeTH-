#!/usr/bin/env python3
"""Human-review checklist for the Ask answers, generated from phase2/docs/data/answers.json.

The automated verifier checks structure only. This checklist is for the step it cannot do: a person reads each cited
page and decides whether it supports the claim, whether the calculation is the right one, and how the open legal
and accounting questions should be handled. Generated from the answer data so the claims, arithmetic and citations
in the checklist are the ones on the pages.

Approvals are recorded by hand in phase2/review/human-approvals.json. This tool reads that file and never writes it.

Run:  python3 phase2/tools/build_review_checklist.py   (writes phase2/review/human-review-checklist.md)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANSWERS = ROOT / 'docs' / 'data' / 'answers.json'
APPROVALS = ROOT / 'review' / 'human-approvals.json'
OUT = ROOT / 'review' / 'human-review-checklist.md'


def fmt(v, u):
    if v is None:
        return '(text)'
    if u == 'usd':
        return f'${v:,.0f}'
    if u == 'ratio':
        return f'{v:.2%}'
    if u == 'miles':
        return f'{v:,.3f} mi'
    return f'{v:,}'


def cell(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


def main():
    doc = json.loads(ANSWERS.read_text())
    approvals = json.loads(APPROVALS.read_text())['answers']
    docs = doc['documents']
    out = ['# Human review checklist: Ask BeTH answers (prototype)', '',
           '**Generated** from `phase2/docs/data/answers.json` by `phase2/tools/build_review_checklist.py`. Do not edit '
           'by hand; record decisions in `phase2/review/human-approvals.json`.', '',
           '**What the automated checks did.** For every answer: each cited document and PDF page exists; each number '
           'matches a BeTH data record or is printed on its cited page; each quote appears on its cited page; each '
           'calculation is recomputed from its input facts; every dollar figure, percentage and mileage in the text traces '
           'to a fact, calculation or cited quote.', '',
           '**What they did not do, and what this review is for:**']
    out += [f'- {x}' for x in doc['answers'][0]['verifier']['does_not_establish']]
    out += ['', 'The open interpretations listed under each answer are BeTH\'s own list and are not checked by any '
            'automated test. A reviewer should add any others found.', '',
            '**How to review.** For each fact, open the PDF at the cited page and tick the box only if the page supports '
            'the claim as worded. Check each calculation\'s method, not just its arithmetic. Then record a decision in '
            '`human-approvals.json`: `APPROVED`, `APPROVED WITH CHANGES` (list them) or `NOT APPROVED`.', '']
    for a in doc['answers']:
        v, ap = a['verifier'], approvals[a['slug']]
        out += ['---', '', f'## {a["question"]}', '',
                f'Page: `phase2/docs/ask/{a["slug"]}.html` · Automated checks: '
                f'{"passed" if v["structural_checks_passed"] else "FAILED"} · Human source verification: '
                f'**{v["independent_source_verification"]["status"]}** · Approval: **{ap["status"]}**', '',
                '### Central claim', '', f'> {a["short_answer"]}', '']
        if ap.get('notes'):
            # Reviewer-recorded context from human-approvals.json, shown ahead of the claim it qualifies.
            out[-4:-4] = [f'Reviewer note: {ap["notes"]}', '']
        for part in a.get('parts', []):
            out += [f'**{part["q"]}** {part["a"]}', '']
        for i in a['interpretation']:
            out += [f'BeTH\'s reading ({i["confidence"]}): {i["text"]}', '', f'Counterargument: {i["counterargument"]}', '']
        out += ['### Calculations', '']
        sym = {'sum': ' + ', 'sub': ' − ', 'div': ' ÷ '}
        for c in v['arithmetic']:
            out.append(f'- [ ] **{c["label"]}**: '
                       + sym[c['op']].join(fmt(i['value'], i['unit']) for i in c['inputs'])
                       + f' = **{fmt(c["recomputed"], c["unit"])}** (`'
                       + sym[c['op']].join(i['ref'] for i in c['inputs']) + '`)'
                       + (f'. {c["note"]}' if c.get('note') else ''))
        out += ['', 'Tick a calculation only if its method is the right one for the claim, not only if the '
                'arithmetic is correct.', '', '### Sources', '',
                '| Page supports claim? | Fact | Value | Document (local file) | Cited | PDF page(s) | Quote | Automated check |',
                '|---|---|---|---|---|---|---|---|']
        for f in a['facts']:
            c = f['cite']
            d = docs[c['doc_id']]
            pages = str(c['pdf_page']) if c['pdf_page'] == c['pdf_page_last'] else f'{c["pdf_page"]}-{c["pdf_page_last"]}'
            src = f'{d["title"]} (`{d["local"]}`' + (f'; quotes checked against `{d["transcription"]}`' if d.get('transcription') else '') + ')'
            out.append(f'| [ ] | {cell(f["label"])} | {fmt(f["value"], f["unit"])} | {cell(src)} | {cell(c["pages"])} | '
                       f'{pages} | {cell(c["quote"] or "")} | {cell(v["fact_support"].get(f["fact_id"], ""))} |')
        out += ['', '### Unresolved legal or accounting interpretation', '']
        out += [f'- [ ] {x}' for x in a['open_interpretations']]
        out += ['', '### Missing evidence', '']
        out += [f'- {m["needed"]}' + (f' (would be in: {m["would_be_in"]})' if m.get('would_be_in') else '')
                for m in a['missing_evidence']]
        out += ['', '### Independent human approval', '',
                f'Recorded in `phase2/review/human-approvals.json` → `answers.{a["slug"]}`. Current status: **{ap["status"]}**.', '',
                '| Field | Entry |', '|---|---|',
                f'| Reviewer | {ap.get("reviewer") or ""} |', f'| Date | {ap.get("date") or ""} |',
                f'| Decision | {ap["status"]} |', f'| Changes required | {cell("; ".join(ap.get("changes_required") or []))} |',
                f'| Notes | {cell(ap.get("notes") or "")} |', '']
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(out) + '\n')
    print('wrote', OUT.relative_to(ROOT.parent))


if __name__ == '__main__':
    main()

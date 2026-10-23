#!/usr/bin/env python3
"""Stage FY2025 p.77 expenditure-breakdown corrections for manual approval.

Never writes a ledger or calls the page builders. Annual totals are not changed.
"""
import argparse
import json
from pathlib import Path

import pdfplumber

import acfr_parse
from acfr_config import load_year
from acfr_funds import NUMBERS, OTHER_OUT, gov_record, required, slug
from acfr_pilot import ROOT, digest, protect_output, provenance, snapshot
from ledger_safety import SafetyError, protected_ids

DEFAULT_OUT = ROOT / 'staging/fy2025-expenditure-corrections'


def expense_sum(outflows):
    return sum(row['amount'] for row in outflows if row['line'] not in OTHER_OUT)


def stage(pdf_path=ROOT / 'annual-comprehensive-financial-report-fy2025.pdf', out=DEFAULT_OUT):
    out = protect_output(out, ROOT / 'data/funds')
    names_to_write = ('proposals.json', 'RECONCILIATION.md')
    if any((out / name).is_symlink() for name in names_to_write):
        raise SafetyError('Refusing correction report symlink')
    config = load_year(2025)
    source = provenance(pdf_path, 2025)
    statement = config['statements'][0]
    page = statement['pairs'][0][0]
    source.update(statement=statement['title'], pdf_page=page,
                  printed_page=statement['printed_pages'][0])
    before = {p:snapshot(ROOT / p) for p in ('data/funds','docs')}
    protected = protected_ids()
    funds = []
    with pdfplumber.open(pdf_path) as pdf:
        if 'June 30, 2025' not in pdf.pages[page-1].extract_text():
            raise SafetyError('Incorrect fiscal-year statement heading')
        names, raw, labels = acfr_parse.parse_pair(pdf, page)
        # Read the source section independently of the extractor's category whitelist.
        start, end = labels.index('Total revenues') + 1, labels.index('Total expenditures')
        expense_labels = [label for label in labels[start:end] if label not in config['nonfinancial_labels']]
        for name in names:
            if name.startswith('Total') or name == 'Other Governmental Funds':
                continue
            fid = NUMBERS.get(name, 'ACFR-' + slug(name))
            path = ROOT / 'data/funds' / f'{fid}.json'
            existing = json.loads(path.read_text())
            detail = existing['flow_detail']
            if detail['fy'] != 2025:
                raise SafetyError(f'{fid}: existing breakdown is not FY2025')
            kind = 'general' if fid == '011' else ('capital_project' if fid == '501' else 'special_revenue')
            corrected = gov_record(name, raw[name], kind, page, config)
            old_rows = detail['outflows']
            new_rows = corrected['outflows']
            old_map, new_map = {}, {}
            for rows, values in ((old_rows,old_map),(new_rows,new_map)):
                for row in rows:
                    if row['line'] in values:
                        raise SafetyError(f'{fid}: duplicate stored expenditure category')
                    values[row['line']] = row['amount']
            categories, corrections = [], []
            for raw_label in expense_labels:
                label = config['row_aliases'].get(raw_label, raw_label).rstrip(':')
                amount = required(raw[name], raw_label)
                old, new = old_map.get(label), new_map.get(label)
                category = dict(source_label=raw_label, category=label, source_amount=amount,
                                ledger_amount=old, proposed_amount=new)
                # An absent zero entry is not a missing expenditure. The audit explicitly prints a dash.
                if amount and old != amount:
                    reason = ('Wrapped label is parsed as "and housing"; expense builder did not apply the configured alias.'
                              if raw_label == 'and housing' else 'Printed TRAN issuance costs row was absent from the expenditure whitelist.'
                              if label == 'TRAN issuance costs' else 'Stored breakdown differs from the audited category; investigate before approval.')
                    category.update(status='PENDING REVIEW', cause=reason)
                    corrections.append(dict(category, change='add' if old is None else 'replace', path='/flow_detail/outflows'))
                else:
                    category['status'] = 'RECONCILED'
                categories.append(category)
            total = required(raw[name], 'Total expenditures')
            annual = [r for r in existing['annual'] if r['fy']==2025 and r['basis']=='audited' and r.get('series') is None and r.get('balance_version') is None]
            if len(annual) != 1:
                raise SafetyError(f'{fid}: ambiguous annual identity')
            source_sum = sum(c['source_amount'] for c in categories)
            old_sum, new_sum = expense_sum(old_rows), expense_sum(new_rows)
            reconciled = source_sum == new_sum == total == annual[0]['expenditure']
            funds.append(dict(fund_number=fid, name=name, protected=fid in protected,
                ledger_path=path.relative_to(ROOT).as_posix(), ledger_sha256=digest(path),
                source=source, categories=categories, proposed_corrections=corrections,
                annual_expenditure=annual[0]['expenditure'], audited_expenditure=total,
                source_category_sum=source_sum, existing_breakdown_sum=old_sum,
                omitted_expenditures=total-old_sum, proposed_breakdown_sum=new_sum,
                proposed_difference_from_audit=new_sum-total,
                annual_total_unchanged=annual[0]['expenditure']==total,
                existing_outflows=old_rows, proposed_outflows=new_rows,
                apply_automatically=False, approval_required=bool(corrections),
                status=('PENDING REVIEW' if corrections else 'RECONCILED') if reconciled else 'CONFLICT'))
    after = {p:snapshot(ROOT / p) for p in before}
    if before != after:
        raise SafetyError('Ledger or published website changed during correction staging')
    report = dict(fiscal_year=2025, source=source,
        explanation='Annual expenditure totals already include these amounts. Only the flow_detail/outflows categorization omitted them. Transfers and other financing uses are excluded from expenditure sums.',
        affected_funds=sum(bool(f['proposed_corrections']) for f in funds),
        omitted_expenditures=sum(f['omitted_expenditures'] for f in funds),
        funds=funds, protected_ledger_checksums={fid:digest(ROOT/'data/funds'/f'{fid}.json') for fid in sorted(protected)},
        preservation_verified=True, apply_automatically=False,
        decisions=['Manually review and approve the four category additions for General Fund, Grants and Capital Improvement.',
                   'General Fund is protected. No protected ledger may be edited automatically; approve a separate manual change before application.',
                   'Any published breakdown correction requires a separately authorized publication step. No page builder or dashboard changes are part of this report.'])
    lines = ['# FY2025 page 77 expenditure breakdown: source-to-ledger reconciliation', '',
        '**Proposals only — manual approval required. No ledger or published content was changed.**', '',
        f"Source: [{source['filename']}]({source['source_url']}), FY2025, PDF p.{page}, printed p.{source['printed_page']}. SHA-256 `{source['sha256']}`.", '',
        report['explanation'], '',
        f"Total omitted: **${report['omitted_expenditures']:,}**, across {report['affected_funds']} funds.", '',
        '| Fund | Existing expense breakdown | Housing omitted | TRAN costs omitted | Total omitted | Audited / corrected sum |',
        '|---|---:|---:|---:|---:|---:|']
    for f in funds:
        additions = {c['category']:c['source_amount'] for c in f['proposed_corrections']}
        lines.append(f"| {f['name']} ({f['fund_number']}) | {f['existing_breakdown_sum']:,} | {additions.get('Community development and housing',0):,} | {additions.get('TRAN issuance costs',0):,} | {f['omitted_expenditures']:,} | {f['audited_expenditure']:,} |")
    lines += ['', '## Causes and scope', '',
        'The PDF wraps “Community development and housing” across two lines, with the numeric values on the “and housing” line. '
        'The parser retains that final label; the expense builder previously required the full label and did not apply the existing year-specific alias. '
        'Separately, its expenditure whitelist omitted the printed “TRAN issuance costs” row. '
        'The fix applies the configured aliases to expense categories and explicitly includes TRAN issuance costs, with duplicate-alias protection.', '',
        'The page’s Other Governmental Funds housing amount ($9,820,968) is an aggregate of nonmajor funds. '
        'It is not a separate ledger correction and must not be added again. Library and Measure O have zero housing and TRAN costs; they require no additions.', '',
        'Year configurations already permit the corresponding FY2024 wrapped labels. The same fix recognizes those expense aliases, '
        'including wrapped interest/fiscal charges, when FY2024 records are generated. The FY2024 pilot already reconciles full source sections; its staged financial values remain unchanged.', '']
    for f in funds:
        lines += [f"## {f['name']} ({f['fund_number']})", '',
            f"Status: {f['status']}; protected: {f['protected']}; approval required: {f['approval_required']}. "
            f"Baseline ledger SHA-256 `{f['ledger_sha256']}`.", '',
            '| Source row label | Canonical category | Audited amount | Stored category amount | Proposed category amount |',
            '|---|---|---:|---:|---:|']
        for c in f['categories']:
            display=lambda x:'not stored' if x is None else f'{x:,}'
            lines.append(f"| {c['source_label']} | {c['category']} | {c['source_amount']:,} | {display(c['ledger_amount'])} | {display(c['proposed_amount'])} |")
        lines += ['', f"Source categories sum: {f['source_category_sum']:,}; proposed expense sum: {f['proposed_breakdown_sum']:,}; "
                  f"audited total: {f['audited_expenditure']:,}; existing annual total: {f['annual_expenditure']:,}. "
                  f"Proposed difference: {f['proposed_difference_from_audit']:,}.", '',
                  'A missing stored zero category is shown as “not stored”; the source zero is explicit, never inferred. '
                  'Transfers out remain in the proposed outflow array but are excluded from expense sums.', '']
    lines += ['## Manual decisions', ''] + [f'{i}. {d}' for i,d in enumerate(report['decisions'],1)]
    lines += ['', 'Reproduce with `python tools/reconcile_expenditure_breakdown.py`. The machine-readable proposals contain the full existing and proposed outflow arrays and baseline hashes. No apply command is provided.', '']
    out.mkdir(parents=True, exist_ok=True)
    (out/'proposals.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    (out/'RECONCILIATION.md').write_text('\n'.join(lines))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    result = stage(out=args.out)
    print(f"Staged {result['affected_funds']} fund proposals; ${result['omitted_expenditures']:,} omitted; all ledgers unchanged")

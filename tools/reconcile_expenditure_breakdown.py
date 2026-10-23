#!/usr/bin/env python3
"""Stage FY2025 p.77 expenditure and financing corrections for manual approval.

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

HISTORICAL_EVIDENCE = ROOT / 'staging/fy2025-expenditure-corrections'
DEFAULT_OUT = ROOT / 'staging/fy2025-reconciliation'


def expense_sum(outflows):
    return sum(row['amount'] for row in outflows if row['line'] not in OTHER_OUT)


def stage(pdf_path=ROOT / 'annual-comprehensive-financial-report-fy2025.pdf', out=DEFAULT_OUT,
          ledger_dir=ROOT / 'data/funds'):
    ledger_dir = Path(ledger_dir).resolve()
    out = protect_output(out, ledger_dir)
    if out == HISTORICAL_EVIDENCE or HISTORICAL_EVIDENCE in out.parents or out in HISTORICAL_EVIDENCE.parents:
        raise SafetyError('Historical correction evidence is immutable; choose a separate output directory')
    names_to_write = ('proposals.json', 'RECONCILIATION.md')
    if any((out / name).is_symlink() for name in names_to_write):
        raise SafetyError('Refusing correction report symlink')
    patch_dir = out / 'patches'
    if patch_dir.is_symlink() or any((patch_dir / name).is_symlink() for name in
            ('SHA256SUMS', '011.json-patch.json', 'ACFR-grants.json-patch.json', '501.json-patch.json')):
        raise SafetyError('Refusing correction patch symlink')
    config = load_year(2025)
    source = provenance(pdf_path, 2025)
    statement = config['statements'][0]
    page = statement['pairs'][0][0]
    source.update(role='expenditure-breakdown extraction source', statement=statement['title'], pdf_page=page,
                  printed_page=statement['printed_pages'][0])
    before = {p:snapshot(ROOT / p) for p in ('data/funds','data/curation','docs')}
    input_before = snapshot(ledger_dir)
    protected = protected_ids()
    funds = []
    with pdfplumber.open(pdf_path) as pdf:
        if 'June 30, 2025' not in pdf.pages[page-1].extract_text():
            raise SafetyError('Incorrect fiscal-year statement heading')
        names, raw, labels = acfr_parse.parse_pair(pdf, page)
        # Read the source section independently of the extractor's category whitelist.
        start, end = labels.index('Total revenues') + 1, labels.index('Total expenditures')
        expense_labels = [label for label in labels[start:end] if label not in config['nonfinancial_labels']]
        financing_labels = labels[labels.index('Transfers in'):labels.index('(uses)')]
        for name in names:
            if name.startswith('Total') or name == 'Other Governmental Funds':
                continue
            fid = NUMBERS.get(name, 'ACFR-' + slug(name))
            path = ledger_dir / f'{fid}.json'
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
            old_inflows, new_inflows = detail['inflows'], corrected['inflows']
            financing_categories = []
            for raw_label in financing_labels:
                label = config['row_aliases'].get(raw_label, raw_label)
                amount = required(raw[name], raw_label)
                if label in OTHER_OUT:
                    old = next((r['amount'] for r in old_rows if r['line']==label), None)
                    new = next((r['amount'] for r in new_rows if r['line']==label), None)
                    old, new = (-old if old is not None else None), (-new if new is not None else None)
                else:
                    old = next((r['amount'] for r in old_inflows if r['line']==label), None)
                    new = next((r['amount'] for r in new_inflows if r['line']==label), None)
                category = dict(source_label=raw_label, category=label, source_amount=amount,
                                ledger_amount=old, proposed_amount=new, status='RECONCILED')
                if amount and old != amount:
                    category.update(status='PENDING REVIEW', cause='Wrapped financing label is parsed as "subscriptions"; inflow builder did not apply the configured alias.')
                    corrections.append(dict(category, change='add' if old is None else 'replace', path='/flow_detail/inflows', kind='financing'))
                financing_categories.append(category)
            def net_financing(inflows, outflows):
                return sum(r['amount'] for r in inflows if r['kind']!='own') - sum(r['amount'] for r in outflows if r['line'] in OTHER_OUT)
            source_financing = required(raw[name], '(uses)')
            source_financing_sum = sum(c['source_amount'] for c in financing_categories)
            proposed_financing = net_financing(new_inflows, new_rows)
            existing_financing = net_financing(old_inflows, old_rows)
            net_change = required(raw[name], 'Net change in fund balance')
            calculated_change = corrected['revenue'] - new_sum + proposed_financing
            balances_reconcile = corrected['beginning_balance'] + net_change == corrected['ending_balance'] == annual[0]['ending_balance']
            # Keep every pre-existing row, including any notes and classifications.
            for original, proposed in ((old_rows,new_rows),(old_inflows,new_inflows)):
                if any(row not in proposed for row in original):
                    raise SafetyError(f'{fid}: correction would alter an existing breakdown row; manual investigation required')
            reconciled = (source_sum == new_sum == total == annual[0]['expenditure']
                and source_financing_sum == proposed_financing == source_financing
                and calculated_change == net_change and balances_reconcile
                and annual[0]['revenue'] == corrected['revenue']
                and annual[0]['transfers_in'] == corrected['transfers_in']
                and annual[0]['transfers_out'] == corrected['transfers_out'])
            funds.append(dict(fund_number=fid, name=name, protected=fid in protected,
                ledger_path=f'data/funds/{fid}.json', ledger_sha256=digest(path),
                source=source, categories=categories, proposed_corrections=corrections,
                financing_categories=financing_categories,
                existing_inflows=old_inflows, proposed_inflows=new_inflows,
                audited_net_financing=source_financing, source_financing_sum=source_financing_sum,
                existing_net_financing=existing_financing, proposed_net_financing=proposed_financing,
                omitted_financing=source_financing-existing_financing,
                audited_revenue=corrected['revenue'], audited_net_change=net_change,
                proposed_net_change=calculated_change, beginning_balance=corrected['beginning_balance'],
                ending_balance=corrected['ending_balance'], balances_reconcile=balances_reconcile,
                annual_expenditure=annual[0]['expenditure'], audited_expenditure=total,
                source_category_sum=source_sum, existing_breakdown_sum=old_sum,
                omitted_expenditures=total-old_sum, proposed_breakdown_sum=new_sum,
                proposed_difference_from_audit=new_sum-total,
                annual_total_unchanged=annual[0]['expenditure']==total,
                existing_outflows=old_rows, proposed_outflows=new_rows,
                apply_automatically=False, approval_required=bool(corrections),
                status=('PENDING REVIEW' if corrections else 'RECONCILED') if reconciled else 'CONFLICT'))
    after = {p:snapshot(ROOT / p) for p in before}
    if before != after or input_before != snapshot(ledger_dir):
        raise SafetyError('Ledger or published website changed during correction staging')
    report = dict(fiscal_year=2025, source=source,
        comparison_scope='current corrected ledgers' if ledger_dir == (ROOT/'data/funds').resolve() else 'supplied comparison ledgers (historical fixtures in regression tests)',
        historical_evidence='staging/fy2025-expenditure-corrections',
        explanation='PR #13 applied the six reviewed additions proposed at 2450d7a. The original evidence remains immutable in staging/fy2025-expenditure-corrections. This report independently reconciles its comparison inputs now. Annual totals remain unchanged. Financing is kind=financing, separate from own revenue and transfers (kind=rescue). Transfers and other financing uses are excluded from expenditure sums.',
        affected_funds=sum(bool(f['proposed_corrections']) for f in funds),
        omitted_expenditures=sum(f['omitted_expenditures'] for f in funds),
        omitted_financing=sum(f['omitted_financing'] for f in funds),
        funds=funds, protected_ledger_checksums={fid:digest(ROOT/'data/funds'/f'{fid}.json') for fid in sorted(protected)},
        preservation_verified=True, apply_automatically=False,
        decisions=['Any newly proposed correction requires independent review and explicit manual approval. Historical corrections are already recorded in merged PR #13; do not reapply the archived patches.',
                   'General Fund is protected. No protected ledger may be edited automatically; approve a separate manual change before application.',
                   'Any published breakdown correction requires a separately authorized publication step. No page builder or dashboard changes are part of this report.'])
    expected_patches = {f"{f['fund_number']}.json-patch.json" for f in funds if f['approval_required']}
    expected_patch_files = expected_patches | ({'SHA256SUMS'} if expected_patches else set())
    if patch_dir.exists() and {p.name for p in patch_dir.iterdir()} - expected_patch_files:
        raise SafetyError('Existing patch evidence would become stale; preserve it and choose a separate output directory')
    out.mkdir(parents=True, exist_ok=True)
    if expected_patches:
        patch_dir.mkdir(exist_ok=True)
    patch_checksums = []
    for fund in funds:
        if not fund['approval_required']:
            continue
        operations = [dict(op='test', path='/fund_number', value=fund['fund_number']),
                      dict(op='test', path='/flow_detail/fy', value=2025)]
        for key in ('inflows','outflows'):
            old, new = fund[f'existing_{key}'], fund[f'proposed_{key}']
            if old != new:
                operations += [dict(op='test', path=f'/flow_detail/{key}', value=old),
                               dict(op='replace', path=f'/flow_detail/{key}', value=new)]
        patch_path = patch_dir / f"{fund['fund_number']}.json-patch.json"
        patch_path.write_text(json.dumps(operations, indent=2, ensure_ascii=False)+'\n')
        fund['patch'] = dict(path=patch_path.relative_to(out).as_posix(), sha256=digest(patch_path), format='RFC 6902 JSON Patch', applied=False)
        patch_checksums.append(f"{digest(patch_path)}  {patch_path.name}")
    if patch_checksums:
        (patch_dir/'SHA256SUMS').write_text('\n'.join(sorted(patch_checksums))+'\n')
    lines = ['# FY2025 page 77 expenditure and financing breakdown: source-to-ledger reconciliation', '',
        '**Read-only reconciliation. No ledger or published content was changed.**', '',
        f"Source: [{source['filename']}]({source['source_url']}), FY2025, PDF p.{page}, printed p.{source['printed_page']}. SHA-256 `{source['sha256']}`.", '',
        report['explanation'], '',
        f"Comparison scope: **{report['comparison_scope']}**. Original reviewed patches, checksums and reports: "
        '[historical evidence](../fy2025-expenditure-corrections/RECONCILIATION.md). '
        'That report describes the pre-correction state, not outstanding omissions in current ledgers.', '',
        f"Current status: {'RECONCILED' if all(f['status']=='RECONCILED' for f in funds) else 'REVIEW REQUIRED'}; "
        f"new correction patches proposed: {len(expected_patches)}.", '',
        f"Total omitted: **${report['omitted_expenditures']:,}**, across {report['affected_funds']} funds.", '',
        f"Separately, omitted lease/subscription financing: **${report['omitted_financing']:,}**. These inflows are not revenue or transfers.", '',
        '| Fund | Existing expense breakdown | Housing omitted | TRAN costs omitted | Total omitted | Audited / corrected sum |',
        '|---|---:|---:|---:|---:|---:|']
    for f in funds:
        additions = {c['category']:c['source_amount'] for c in f['proposed_corrections']}
        lines.append(f"| {f['name']} ({f['fund_number']}) | {f['existing_breakdown_sum']:,} | {additions.get('Community development and housing',0):,} | {additions.get('TRAN issuance costs',0):,} | {f['omitted_expenditures']:,} | {f['audited_expenditure']:,} |")
    lines += ['', '## Historical causes and scope', '',
        'The PDF wraps “Community development and housing” across two lines, with the numeric values on the “and housing” line. '
        'The parser retains that final label; the expense builder previously required the full label and did not apply the existing year-specific alias. '
        'Separately, its expenditure whitelist omitted the printed “TRAN issuance costs” row. '
        'The fix applies the configured aliases to expense categories and explicitly includes TRAN issuance costs, with duplicate-alias protection.', '',
        'The financing row also wraps: “Inception of leases and” precedes the numeric “subscriptions” line. '
        'The financing builder now applies the year alias once and rejects duplicate canonical/alias rows, even when their values agree. '
        'General Fund $18,156,996 plus Grants $19,381 = $18,176,377. Together with the Other Governmental Funds aggregate $6,384,300, '
        'these equal the published $24,560,677 row total. The aggregate is not another ledger correction.', '',
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
        lines += ['### Other financing sources and uses', '',
            '| Source row | Canonical category | Audited signed amount | Existing signed amount | Proposed signed amount |',
            '|---|---|---:|---:|---:|']
        for c in f['financing_categories']:
            lines.append(f"| {c['source_label']} | {c['category']} | {c['source_amount']:,} | {display(c['ledger_amount'])} | {display(c['proposed_amount'])} |")
        lines += ['', f"Net other financing: existing {f['existing_net_financing']:,}; proposed {f['proposed_net_financing']:,}; "
            f"source row sum {f['source_financing_sum']:,}; audited total {f['audited_net_financing']:,}.", '',
            f"Revenue {f['audited_revenue']:,} − expenditures {f['audited_expenditure']:,} + net financing ({f['proposed_net_financing']:,}) "
            f"= net change {f['proposed_net_change']:,}; audited change {f['audited_net_change']:,}. "
            f"Restated beginning balance {f['beginning_balance']:,} + audited change {f['audited_net_change']:,} "
            f"= ending balance {f['ending_balance']:,}; reconciled: {f['balances_reconcile']}.", '']
        if 'patch' in f:
            p = f['patch']
            lines += [f"Proposed patch: [{p['path']}]({p['path']}); SHA-256 `{p['sha256']}`. **Not applied.**", '']
    lines += ['## Patch format and preservation', '',
        f'This run proposes {len(expected_patches)} RFC 6902 JSON Patch files. '
        'When corrections are needed these files are proposals, not replacement ledgers. '
        'Each checks the fund, fiscal year and original array before replacing only changed flow_detail arrays. '
        'Check the baseline ledger SHA-256 above before any separately approved manual edit. '
        'All original rows remain identical. '
        'Annual records, revenue, transfers, balances, flows, obligations, narratives, findings and source references remain untouched. '
        'General Fund is protected and requires explicit manual approval. No patch application command is provided. '
        'When patches are proposed, byte checksums are listed in `patches/SHA256SUMS`. '
        'A reconciled run produces no patch files or checksum file. The original three patches and their checksum file remain in the historical evidence directory.', '']
    lines += ['## Manual decisions', ''] + [f'{i}. {d}' for i,d in enumerate(report['decisions'],1)]
    lines += ['', 'Reproduce with `python tools/reconcile_expenditure_breakdown.py`. The machine-readable proposals contain full existing/proposed inflow and outflow arrays, exact patches and hashes. No apply command is provided.', '']
    out.mkdir(parents=True, exist_ok=True)
    (out/'proposals.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    (out/'RECONCILIATION.md').write_text('\n'.join(lines))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--ledger-dir', type=Path, default=ROOT/'data/funds')
    args = parser.parse_args()
    result = stage(out=args.out, ledger_dir=args.ledger_dir)
    print(f"Staged {result['affected_funds']} fund proposals; ${result['omitted_expenditures']:,} omitted; all ledgers unchanged")

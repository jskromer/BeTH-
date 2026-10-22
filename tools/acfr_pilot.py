#!/usr/bin/env python3
"""Reproduce the FY2024 staging pilot without modifying ledger or website data.

python tools/acfr_pilot.py --out staging/fy2024
Exit 0 means a complete report was produced, not that financial review passed.
Use --require-reconciled for a nonzero exit when review items remain.
"""
import argparse
import hashlib
import json
from pathlib import Path

from acfr_config import load_year
from acfr_reconcile import reconcile

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = [
    'Resolve the published $1 governmental statement-control differences before historical integration; retain every audited value meanwhile.',
    'Decide how to document genuinely blank statement cells; do not convert blanks into zero or insert balancing adjustments.',
    'Review extracted-only nonoperating and beginning-balance fields. Their absence from reviewed records is a review item, not a financial conflict.',
    'Approve historical identity mappings, including the combined Equipment 671/672 column, explicit legacy IDs and three text-layer name aliases. Investigate the FY2025 Fire Admin Training Building Bond with no FY2024 column.',
    'Decide Marina series tagging separately. Keep FY2015–FY2023 statistical-schedule rows and all existing series fields unchanged during this pilot.',
    'Review the FY2025 Note 15 restatements and preserve original FY2024 closing balances separately from FY2025 restated opening balances.',
    'Confirm a separate scope and accounting model before extracting fiduciary trusts, custodial funds or component units; these are outside the existing governmental/proprietary ledger pilot.',
    'Authorize historical integration only in a later PR after independent review; nothing in staging is approved for publication.',
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def snapshot(root):
    return {p.relative_to(root).as_posix(): digest(p) for p in sorted(root.rglob('*')) if p.is_file()}


def protect_output(out, ledger_dir):
    out = Path(out).resolve()
    # Resolve symlinks, including parent directories, before deciding where writes go.
    for blocked in (ROOT / 'data', ROOT / 'docs', Path(ledger_dir)):
        blocked = blocked.resolve()
        if out == blocked or blocked in out.parents or out in blocked.parents:
            raise ValueError(f'Staging output overlaps protected content: {out}')
    if ROOT in out.parents and ROOT / 'staging' not in out.parents:
        raise ValueError('Repository pilot output must be below staging/')
    for filename in ('manifest.json', 'funds.json', 'identity-map.json', 'discrepancies.json', 'RECONCILIATION.md'):
        if (out / filename).is_symlink():
            raise ValueError(f'Refusing staging output symlink: {out / filename}')
    return out


def provenance(path, year, retrieval_date=None):
    config = load_year(year)
    sha = digest(path)
    if sha != config['expected_sha256']:
        raise ValueError(f'FY{year} source checksum differs from the verified original PDF')
    return dict(fiscal_year=year, source_id=config['source_id'], source_url=config['source_url'],
                retrieval_date=retrieval_date, discovery_url=config.get('discovery_url'), sha256=sha, size_bytes=Path(path).stat().st_size,
                filename=Path(path).name, statements=config['statements'],
                role='extraction source' if year == 2024 else 'opening-balance/restatement comparator',
                restatement_note=config.get('restatement_note'))


def money(value):
    return 'missing' if value is None else f'{value:,}'


def markdown(report):
    lines = ['# FY2024 audited-fund extraction and reconciliation pilot', '',
             '**Staging only. Independent review pending. No publication or ledger update.**', '',
             report['scope'], '',
             f"Extracted **{report['summary']['fund_count']}** FY2024 funds; compared {report['summary']['protected_fund_count']} protected ledgers. "
             f"Fund statuses: {report['summary']['statuses']}. {report['summary']['restated_funds']} funds have nonzero reported FY2025 opening restatements. Status precedence is CONFLICT, INCOMPLETE, PENDING REVIEW, RECONCILED.", '',
             'RECONCILED means the exact-dollar check passed. It does not authorize publication. '
             'PENDING REVIEW covers missing reviewed fields, unreviewed identities and explicit restatements. '
             'INCOMPLETE identifies unavailable evidence. CONFLICT retains both differing values. '
             'A shared statement-control conflict is not attributed as a value conflict to every member fund.', '',
             '## Provenance', '']
    for source in report['provenance']:
        lines += [f"- FY{source['fiscal_year']}: [{source['filename']}]({source['source_url']}); "
                  f"retrieval: {source['retrieval_date'] or 'existing repository source; original retrieval date not recorded'}; "
                  f"SHA-256 `{source['sha256']}`."]
    lines += ['', 'Page references below are 1-based PDF pages. Printed pages are also recorded in the manifest.', '',
              '## Findings requiring review', '',
              f"Comparable reviewed-value conflicts: {report['summary']['reviewed_value_conflicts']}. "
              'Equipment, Workers’ Compensation and Zero Waste lack reviewed `nonoperating` fields; '
              'all six lack structured reviewed beginning balances and net-change fields. These are review items, not value disagreements.', '',
              'The FY2024 PDF has genuinely blank cells for Condo Conversion Program / General government '
              '(PDF p.230) and Measure B Paratransit / Private contributions and donations (p.232). '
              'Visual inspection confirmed the blanks. They remain null, so affected category sums and horizontal controls are incomplete.', '',
              'The enterprise Total column has no published opening or closing net-position total (p.88). '
              'Those controls remain incomplete. The bridge to the internal-service summary compares common printed rows only; '
              'scope-specific enterprise categories absent from the combining statement are listed as not comparable.', '',
              'FY2025 Note 15 (PDF pp.171–173) describes prior-period corrections and GASB 101 compensated absences. '
              'The report retains the FY2024 closing value, FY2025 original opening, stated adjustment and restated opening independently. '
              'No restatement is silently applied to FY2024.', '',
              '## Statement totals and discrepancies', '']
    for index,group in enumerate(report['statement_totals'] + report['following_year_statement_totals']):
        lines += [f"### Control {index}: {group['name']} — {group['status']}", '',
                  f"PDF pages {group['source']['pdf_pages']}; {len(group['members'])} member columns; {len(group['checks'])} row checks.", '']
        if group['issues']:
            lines += ['| Row | Calculated | Published | Difference | Status |', '|---|---:|---:|---:|---|']
            for item in group['issues']:
                lines += [f"| {item.get('label', item['code'])} | {money(item.get('calculated'))} | {money(item.get('reported'))} | {money(item.get('difference'))} | {item['status']} |"]
            lines += ['']
        if group.get('not_comparable_labels'):
            lines += ['Rows not common to both statements: ' + ', '.join(group['not_comparable_labels']) + '.', '']
    lines += ['## All-fund comparison', '',
              'Values are integer dollars. Governmental revenue/expense use modified accrual; proprietary values use accrual operating revenue/expense. '
              'Transfers remain separate, with the printed signs retained in machine data. '
              'The complete raw label/value evidence, individual checks, existing source references and discrepancy details are in `funds.json` and `discrepancies.json`.', '']
    for fund in report['funds']:
        values = fund['values']
        lines += [f"### {fund['fund_number']} — {fund['name']}", '',
                  f"Status: **{fund['status']}**; confidence: {fund['confidence']}; human review: {fund['review_status']}. "
                  f"Protected: {fund['protected']}. Accounting basis: {fund['accounting_basis']}.", '',
                  f"Source: {fund['source']['statement']}; PDF {fund['source']['pdf_pages']}; column {fund['source']['column_index'] + 1} ({fund['source']['column_name']}).", '',
                  '| Field | FY2024 extracted | Existing reviewed |', '|---|---:|---:|']
        reviewed = fund['existing_reviewed'][0] if len(fund['existing_reviewed']) == 1 else {}
        for field in ('revenue', 'expenditure', 'nonoperating', 'transfers_in', 'transfers_out', 'beginning_balance', 'net_change', 'ending_balance'):
            if field == 'nonoperating' and fund['accounting_basis'] == 'modified_accrual':
                continue
            lines += [f"| {field} | {money(values.get(field))} | {money(reviewed.get(field))} |"]
        lines += ['', 'Checks: ' + '; '.join(f"{c['name']}: {c['status']}" for c in fund['checks']) + '.', '']
        nxt = fund['continuity']
        if nxt:
            bal = nxt['balances']
            lines += [f"FY2025 opening: original {money(bal['original_beginning'])}; "
                      f"reported adjustment {money(bal['reported_adjustment'])}; restated {money(bal['restated_beginning'])}; "
                      f"statement PDF {nxt['source']['pdf_pages']}. A missing restated value means no separate restated row is printed, not a zero adjustment.", '']
        lines += ['Issues: ' + '; '.join(i['message'] + (f" [{i['field']}]" if 'field' in i else '') for i in fund['issues']) + '.', '',
                  'Statement control references: ' + ', '.join(map(str, fund['column_check_groups'])) + '.', '']
    lines += ['## Existing ledger without an FY2024 column', '']
    for item in report['missing_fy2024_columns']:
        lines += [f"- **{item['status']}**: {item['fund_number']} — {item['name']}: {item['message']}."]
    lines += ['', '## Batch errors', '']
    for key in ('batch_errors', 'following_year_parse_errors'):
        lines += [f"{key}: {json.dumps(report[key], ensure_ascii=False)}", '']
    lines += ['## Decisions requiring Steve’s approval', '']
    lines += [f'{i}. {decision}' for i,decision in enumerate(report['decisions'], 1)]
    lines += ['', '## Verification and reproduction', '',
              'Run `python tools/acfr_pilot.py --out staging/fy2024`. Source PDFs must match the pinned checksums. '
              'No network calls occur during extraction. Use `--require-reconciled` to return exit 1 when any report review items remain. '
              'Exit 0 without that flag means report generation succeeded, not that the pilot passed financial review.', '',
              'The run snapshots `data/funds` and `docs` before and after extraction and records hashes in the manifest. '
              'Tests rerun extraction to verify deterministic reports and test ledger preservation, identity collisions, exact-dollar arithmetic, '
              'missing fields, explicit restatement bridges and collection of multiple problems.', '']
    return '\n'.join(lines)


def run(pdf_path, next_pdf, out, ledger_dir=ROOT / 'data/funds', retrieval_date='2026-10-22'):
    out = protect_output(out, ledger_dir)
    sources = [provenance(pdf_path, 2024, retrieval_date), provenance(next_pdf, 2025)]
    before = {'ledgers': snapshot(Path(ledger_dir)), 'website': snapshot(ROOT / 'docs')}
    report = reconcile(pdf_path, next_pdf, ledger_dir)
    after = {'ledgers': snapshot(Path(ledger_dir)), 'website': snapshot(ROOT / 'docs')}
    if before != after:
        raise RuntimeError('Protected data or website changed during staging extraction')
    report['provenance'], report['decisions'] = sources, DECISIONS
    report['summary']['reviewed_value_conflicts'] = sum(i['code'] == 'reviewed_value_conflict' for f in report['funds'] for i in f['issues'])
    report['summary']['restated_funds'] = sum(bool(f['continuity'] and f['continuity']['balances']['reported_adjustment']) for f in report['funds'])
    manifest = dict(schema_version=1, fiscal_year=2024, provenance=sources, config_checksums={str(y):digest(ROOT / f'tools/acfr_years/{y}.json') for y in (2024,2025)},
                    preservation={'unchanged':True, 'before':before, 'after':after}, scope=report['scope'])
    out.mkdir(parents=True, exist_ok=True)
    artifacts = {'manifest.json':manifest, 'funds.json':report['funds'],
                 'identity-map.json':[dict(fund_number=f['fund_number'], type=f['type'], source=f['source'], **f['mapping']) for f in report['funds']],
                 'discrepancies.json':report}
    for name, content in artifacts.items():
        (out / name).write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
    (out / 'RECONCILIATION.md').write_text(markdown(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, default=ROOT / 'staging/fy2024/source/annual-comprehensive-financial-report-fy2024.pdf')
    parser.add_argument('--next-pdf', type=Path, default=ROOT / 'annual-comprehensive-financial-report-fy2025.pdf')
    parser.add_argument('--out', type=Path, default=ROOT / 'staging/fy2024')
    parser.add_argument('--require-reconciled', action='store_true')
    args = parser.parse_args()
    report = run(args.pdf, args.next_pdf, args.out)
    print(json.dumps(report['summary'], indent=2))
    print(f'Reports written to {args.out}; no ledger or website writes')
    unresolved = (any(f['status'] != 'RECONCILED' for f in report['funds']) or
                  any(g['status'] != 'RECONCILED' for g in report['statement_totals']) or
                  any(g['status'] != 'RECONCILED' for g in report['following_year_statement_totals']) or
                  bool(report['batch_errors'] or report['following_year_parse_errors'] or report['missing_fy2024_columns']))
    return 1 if args.require_reconciled and unresolved else 0


if __name__ == '__main__':
    raise SystemExit(main())

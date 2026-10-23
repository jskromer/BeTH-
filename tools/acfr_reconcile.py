"""Read-only accounting checks and complete discrepancy collection for ACFR staging.

No function in this module calls the ledger updater or publishes any data.
All checks use exact integer dollars. A nonzero difference is retained as evidence.
"""
import copy
from collections import Counter
from pathlib import Path
import json

import pdfplumber

import acfr_parse
from acfr_config import load_year
from acfr_funds import IDENTITIES, NUMBERS, slug
from ledger_safety import FINANCIAL_FIELDS, protected_ids

STATUSES = ('RECONCILED', 'CONFLICT', 'INCOMPLETE', 'PENDING REVIEW')


def issue(record, severity, code, message, **evidence):
    record['issues'].append({**evidence, 'status': severity, 'code': code, 'message': message})


def status_of(issues):
    for status in ('CONFLICT', 'INCOMPLETE', 'PENDING REVIEW'):
        if any(i['status'] == status for i in issues):
            return status
    return 'RECONCILED'


def equality(record, name, actual, expected, **evidence):
    check = dict(name=name, calculated=actual, reported=expected, **evidence)
    if type(actual) is not int or type(expected) is not int:
        check['status'] = 'INCOMPLETE'
        issue(record, 'INCOMPLETE', name, 'Required value unavailable; check cannot complete', **check)
    else:
        check['difference'] = actual - expected
        check['status'] = 'RECONCILED' if actual == expected else 'CONFLICT'
        if actual != expected:
            issue(record, 'CONFLICT', name, 'Exact-dollar arithmetic disagreement', **check)
    record['checks'].append(check)
    return check


def add(*values):
    return sum(values) if all(type(v) is int for v in values) else None


def subtract(a, b):
    return a - b if type(a) is int and type(b) is int else None


def read_value(record, rows, aliases, field, required=True):
    found = [(k, rows[k]) for k in aliases if k in rows]
    record.setdefault('field_labels', {})[field] = [k for k, _ in found]
    if not found:
        if required:
            issue(record, 'INCOMPLETE', 'missing_label', f'Missing required label for {field}', aliases=aliases)
        return None
    if any(type(v) is not int for _, v in found):
        issue(record, 'INCOMPLETE', 'missing_value', f'Unread value for {field}', observed=found)
        return None
    if len({v for _, v in found}) != 1:
        issue(record, 'CONFLICT', 'label_alias_conflict', f'Aliases disagree for {field}', observed=found)
        return None
    return found[0][1]


def row_sum(record, rows, labels, start, end, check_name, expected, include_start=False):
    try:
        first = 0 if start is None else labels.index(start) + (0 if include_start else 1)
        last = labels.index(end)
    except ValueError:
        issue(record, 'INCOMPLETE', 'missing_section', f'Cannot locate section for {check_name}', start=start, end=end)
        return
    selected = labels[first:last]
    equality(record, check_name, add(*(rows[k] for k in selected)), expected, labels=selected)


def normalize(table, config):
    rows, labels = {}, []
    issues = []
    for label in table['labels']:
        if not label or label in config.get('nonfinancial_labels', []):
            continue  # page-number/footer rows are not financial statement rows
        normalized = config['row_aliases'].get(label, label)
        if normalized in rows:
            issues.append(dict(status='CONFLICT', code='duplicate_normalized_label', message=normalized))
        labels.append(normalized)
        rows[normalized] = table['rows'][label]
    return rows, labels, issues


def financial_record(column, config):
    rows, labels, problems = normalize(column, config)
    record = {k: copy.deepcopy(column[k]) for k in ('fund_number', 'name', 'type', 'source', 'accounting_basis', 'mapping')}
    record.update(fy=config['fiscal_year'], basis='audited', checks=[], issues=problems,
                  line_items=rows, ordered_labels=labels)
    gov = column['accounting_basis'] == 'modified_accrual'
    cfg = config['labels']
    value = lambda field, aliases, required=True: read_value(record, rows, aliases, field, required)
    totals = ('Total revenues', 'Total expenditures') if gov else ('Total operating revenues', 'Total operating expenses')
    values = {field: value(field, [label]) for field, label in zip(('revenue', 'expenditure'), totals)}
    values['transfers_in'] = value('transfers_in', ['Transfers in'])
    signed_out = value('transfers_out_signed', ['Transfers out'])
    values['transfers_out'] = abs(signed_out) if type(signed_out) is int else None
    values['ending_balance'] = value('ending_balance', cfg['governmental_ending'] if gov else ['Total net position - ending'])
    beginning_labels = cfg['governmental_beginning'] if gov else cfg['proprietary_beginning']
    restated_labels = cfg['governmental_major_beginning'] if gov and column['source']['statement_id'] == 'major_governmental' and config['fiscal_year'] == 2025 else ([] if gov else cfg['proprietary_restated'])
    has_restatement = bool(restated_labels and any(k in rows for k in restated_labels))
    values['beginning_balance'] = value('beginning_balance', restated_labels if has_restatement else beginning_labels)
    values['net_change'] = value('net_change', ['Net change in fund balance'] if gov else ['Change in net position'])
    record['balances'] = {'reported_beginning': values['beginning_balance'], 'ending': values['ending_balance'],
                          'original_beginning': values['beginning_balance'] if not has_restatement else value('original_beginning', cfg['governmental_original'] if gov else cfg['proprietary_original']),
                          'restated_beginning': values['beginning_balance'] if has_restatement else None,
                          'reported_adjustment': value('reported_adjustment', cfg['adjustment']) if has_restatement else None,
                          'restatement_reported': has_restatement}
    if has_restatement:
        equality(record, 'restatement_bridge', add(record['balances']['original_beginning'], record['balances']['reported_adjustment']), record['balances']['restated_beginning'])
    record['values'] = values
    row_sum(record, rows, labels, None, totals[0], 'revenue_categories', values['revenue'])
    row_sum(record, rows, labels, totals[0], totals[1], 'expenditure_categories', values['expenditure'])
    equality(record, 'balance_roll_forward', add(values['beginning_balance'], values['net_change']), values['ending_balance'])
    if gov:
        equality(record, 'revenues_over_expenditures', subtract(values['revenue'], values['expenditure']), value('revenues_over_expenditures', ['Revenues over/(under) expenditures']))
        financing_total = value('other_financing', ['Total other financing sources/(uses)'])
        row_sum(record, rows, labels, 'Transfers in', 'Total other financing sources/(uses)', 'other_financing_categories', financing_total, include_start=True)
        equality(record, 'net_change_from_operations_financing', add(subtract(values['revenue'], values['expenditure']), financing_total), values['net_change'])
    else:
        values['nonoperating'] = value('nonoperating', ['Total nonoperating revenues (expenses)'])
        operating = value('operating_income', ['Operating income (loss)'])
        equality(record, 'operating_income', subtract(values['revenue'], values['expenditure']), operating)
        row_sum(record, rows, labels, 'Operating income (loss)', 'Total nonoperating revenues (expenses)', 'nonoperating_categories', values['nonoperating'])
        equality(record, 'income_before_transfers', add(operating, values['nonoperating']), value('income_before_transfers', ['Income (loss) before transfers']))
        equality(record, 'net_change_from_operations_transfers', add(operating, values['nonoperating'], values['transfers_in'], signed_out), values['net_change'])
    # Preserve the printed signs, including any unexpected sign, rather than fixing it.
    record['transfers_as_reported'] = {'in': values['transfers_in'], 'out': signed_out}
    if type(signed_out) is int and signed_out > 0:
        issue(record, 'PENDING REVIEW', 'transfer_out_sign', 'Statement reports positive transfers out; retained without correction')
    return record


def read_statements(pdf_path, year):
    config = load_year(year)
    columns, controls, errors = [], [], []
    with pdfplumber.open(pdf_path) as pdf:
        for statement in config['statements']:
            kind = 'special_revenue'
            for left, right in statement['pairs']:
                try:
                    # Check heading/year independently of fixed page configuration.
                    heading = pdf.pages[left - 1].extract_text() or ''
                    if f'June 30, {year}' not in heading or 'Statement of Revenues' not in heading:
                        raise ValueError('Configured page does not have the expected statement/year heading')
                    names, out, labels = acfr_parse.parse_pair(pdf, left, right)
                except (ValueError, IndexError) as exc:
                    errors.append(dict(status='INCOMPLETE', code='statement_parse', message=str(exc), statement=statement['id'], pages=[left, right]))
                    continue
                for index, name in enumerate(names):
                    if statement['id'] == 'major_governmental':
                        kind = 'general' if name == 'General Fund' else ('capital_project' if name == 'Capital Improvement' else 'special_revenue')
                    elif statement['id'] == 'nonmajor_governmental':
                        if name == 'Total Special Revenue Funds':
                            kind = 'capital_project'
                        elif name == 'Total Capital Project Funds':
                            kind = 'debt_service'
                    else:
                        kind = statement['id']
                    aggregate = name.startswith('Total') or name in ('Other Governmental Funds', 'Internal Service Funds')
                    canonical = config['fund_aliases'].get(name, name)
                    fid = IDENTITIES.get((canonical, kind), NUMBERS.get(canonical, 'ACFR-' + slug(canonical)))
                    source = dict(source_id=config['source_id'], url=config['source_url'], statement_id=statement['id'], statement=statement['title'], pdf_pages=[left] + ([right] if right else []), column_index=index, column_name=name)
                    column = dict(fund_number=fid, name=canonical, type=kind, source=source, accounting_basis=statement['basis'],
                                  mapping={'observed_name':name, 'canonical_name':canonical, 'alias_applied':name != canonical,
                                           'method':'explicit IDENTITIES' if (canonical,kind) in IDENTITIES else ('City fund number' if canonical in NUMBERS else 'FY2025-compatible slug'), 'review_status':'PENDING REVIEW'},
                                  rows=out[name], labels=labels)
                    (controls if aggregate else columns).append(column)
    # Keep collisions in the report, never overwrite or silently suffix identities.
    counts = Counter(c['fund_number'] for c in columns)
    for col in columns:
        if counts[col['fund_number']] > 1:
            errors.append(dict(status='CONFLICT', code='fund_identity_collision', message=col['fund_number'], source=col['source']))
    return columns, controls, errors


def column_checks(columns, controls, year):
    """Independent horizontal checks for every published numeric statement row.

    Subtotals select only their component columns, so they are never counted twice.
    Blank published totals are INCOMPLETE, not calculated replacement values.
    """
    results = []
    for control in controls:
        sid, name = control['source']['statement_id'], control['source']['column_name']
        same = [c for c in columns if c['source']['statement_id'] == sid]
        if sid == 'major_governmental':
            if name == 'Other Governmental Funds':
                members = [c for c in columns if c['source']['statement_id'] == 'nonmajor_governmental']
            else:
                # The published Other Governmental Funds column bridges combining statements.
                members = same + [c for c in controls if c['source']['statement_id'] == sid and c['source']['column_name'] == 'Other Governmental Funds']
        elif sid == 'nonmajor_governmental':
            kinds = {'Total Special Revenue Funds':'special_revenue', 'Total Capital Project Funds':'capital_project', 'Total':'debt_service'}
            members = [c for c in same if c['type'] == kinds[name]] if name in kinds else same
        elif sid == 'enterprise' and name == 'Internal Service Funds':
            members = [c for c in columns if c['source']['statement_id'] == 'internal_service']
        else:
            members = same
        check_group = dict(name=f'{year} {sid}: {name}', source=control['source'], members=[c['fund_number'] for c in members], checks=[], issues=[])
        control_rows, control_labels, problems = normalize({'labels':control['labels'],'rows':control['rows']}, load_year(year))
        check_group['issues'].extend(problems)
        normalized_members = [normalize({'labels':m['labels'], 'rows':m['rows']}, load_year(year))[0] for m in members]
        check_group['not_comparable_labels'] = []
        for label in control_labels:
            if load_year(year).get('column_bridge_policy', {}).get(f'{sid}:{name}') == 'common_rows_only' and not all(label in m for m in normalized_members):
                check_group['not_comparable_labels'].append(label)
                continue
            values = []
            for member in members:
                normalized, _, _ = normalize({'labels':member['labels'],'rows':member['rows']}, load_year(year))
                values.append(normalized.get(label))
            equality(check_group, 'column_total', add(*values) if members else None, control_rows[label], label=label)
        check_group['status'] = status_of(check_group['issues'])
        results.append(check_group)
    return results


def compare_reviewed(record, existing):
    matches = [r for r in existing.get('annual', []) if r.get('fy') == record['fy'] and r.get('basis') == 'audited' and r.get('series') is None and r.get('balance_version') is None]
    record['existing_reviewed'] = copy.deepcopy(matches)
    record['existing_sources'] = copy.deepcopy(existing.get('sources', {})) if matches else {}
    record['comparison'] = []
    if not matches:
        issue(record, 'PENDING REVIEW', 'no_reviewed_year', 'No existing reviewed record for this year; no ledger write proposed')
        return
    if len(matches) != 1:
        issue(record, 'CONFLICT', 'duplicate_reviewed_identity', 'Multiple existing rows have the same annual identity')
        return
    old = matches[0]
    for field in (*FINANCIAL_FIELDS, 'net_change'):
        extracted = record['values'].get(field)
        reviewed = old.get(field)
        comparison = dict(field=field, extracted=extracted, reviewed=reviewed)
        if extracted is None and reviewed is None:
            continue
        if field not in old or reviewed is None:
            comparison['status'] = 'PENDING REVIEW'
            issue(record, 'PENDING REVIEW', 'missing_reviewed_field', f'Reviewed record lacks {field}; extracted value retained only in staging', **comparison)
        elif extracted is None:
            comparison['status'] = 'INCOMPLETE'
            issue(record, 'INCOMPLETE', 'missing_extracted_field', f'Extracted value unavailable for {field}', **comparison)
        else:
            comparison['difference'] = extracted - reviewed
            comparison['status'] = 'RECONCILED' if extracted == reviewed else 'CONFLICT'
            if extracted != reviewed:
                issue(record, 'CONFLICT', 'reviewed_value_conflict', f'Reviewed and extracted {field} disagree', **comparison)
        record['comparison'].append(comparison)


def continuity(record, following):
    if following is None:
        issue(record, 'INCOMPLETE', 'missing_following_fund', 'No unambiguous FY2025 fund-statement identity')
        record['continuity'] = None
        return
    balance = following['balances']
    record['continuity'] = dict(following_fy=following['fy'], source=following['source'], balances=copy.deepcopy(balance), checks=copy.deepcopy(following['checks']), issues=copy.deepcopy(following['issues']))
    equality(record, 'next_year_original_beginning', record['values']['ending_balance'], balance['original_beginning'])
    # These are independent statement values; a restatement is not an inferred plug.
    if balance['restatement_reported']:
        equality(record, 'next_year_restatement_bridge', add(balance['original_beginning'], balance['reported_adjustment']), balance['restated_beginning'])
        if balance['reported_adjustment']:
            issue(record, 'PENDING REVIEW', 'reported_restatement', 'FY2025 reports an explicit beginning-balance restatement; original and restated balances retained separately', original=balance['original_beginning'], adjustment=balance['reported_adjustment'], restated=balance['restated_beginning'], source=following['source'])
    if following['issues']:
        issue(record, status_of(following['issues']), 'following_statement_issues', 'FY2025 comparator has independent extraction/reconciliation issues', details=following['issues'])


def reconcile(pdf_path, next_pdf, ledger_dir):
    config = load_year(2024)
    columns, controls, errors = read_statements(pdf_path, 2024)
    next_columns, next_controls, next_errors = read_statements(next_pdf, 2025)
    records = [financial_record(c, config) for c in columns]
    next_records = [financial_record(c, load_year(2025)) for c in next_columns]
    existing = {p.stem: json.loads(p.read_text()) for p in Path(ledger_dir).glob('*.json')}
    next_index = {}
    for r in next_records:
        next_index.setdefault(r['fund_number'], []).append(r)
    protected = protected_ids()
    for record in records:
        fid = record['fund_number']
        record['protected'] = fid in protected
        compare_reviewed(record, existing.get(fid, {}))
        candidates = next_index.get(fid, [])
        continuity(record, candidates[0] if len(candidates) == 1 else None)
        if any(e.get('code') == 'fund_identity_collision' and e['message'] == fid for e in errors):
            issue(record, 'CONFLICT', 'fund_identity_collision', 'Fund identifier is ambiguous')
        if fid not in existing:
            issue(record, 'PENDING REVIEW', 'unmapped_existing_fund', 'FY2024 identity has no existing BeTH ledger; requires identity review')
        record['mapping']['following_name'] = candidates[0]['name'] if len(candidates) == 1 else None
    total_checks = column_checks(columns, controls, 2024)
    # Each fund carries every applicable published-total failure, with references.
    for record in records:
        applicable = [i for i,g in enumerate(total_checks) if record['fund_number'] in g['members']]
        record['column_check_groups'] = applicable
        for i in applicable:
            group = total_checks[i]
            if group['issues']:
                issue(record, 'PENDING REVIEW', 'statement_total_issues', 'Shared statement control requires review; discrepancy is not attributed to this fund', group_index=i, control_status=group['status'])
        record['status'] = status_of(record['issues'])
        record['confidence'] = 'High' if record['status'] == 'RECONCILED' else ('Unknown' if record['status'] == 'INCOMPLETE' else 'Moderate')
        record['review_status'] = 'PENDING REVIEW'  # independent human review has not occurred
    present = {r['fund_number'] for r in records}
    missing = [dict(fund_number=fid, name=d['name'], status='INCOMPLETE', confidence='Unknown', review_status='PENDING REVIEW', values=None, source=None, existing_reviewed=[a for a in d['annual'] if a.get('fy') == 2024 and a.get('basis') == 'audited'], message='Existing FY2025 ledger has no FY2024 column in the configured statements; creation/closure/identity must be reviewed') for fid,d in sorted(existing.items()) if fid not in present]
    return dict(fiscal_year=2024, scope=config['scope'], funds=records, statement_totals=total_checks, batch_errors=errors,
                following_year_parse_errors=next_errors, following_year_statement_totals=column_checks(next_columns, next_controls, 2025), missing_fy2024_columns=missing,
                summary=dict(fund_count=len(records), statuses=dict(Counter(r['status'] for r in records)), reviewed_fund_count=sum(bool(r['existing_reviewed']) for r in records), protected_fund_count=sum(r['protected'] for r in records)))

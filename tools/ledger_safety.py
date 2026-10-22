"""Append-only ledger updates. Reviewed evidence is never replaced by extraction."""
import copy
import json
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / 'data/curation/protected-ledgers.json'
FINANCIAL_FIELDS = ('revenue', 'expenditure', 'nonoperating', 'transfers_in',
                    'transfers_out', 'ending_balance', 'beginning_balance')


class SafetyError(ValueError):
    pass


def annual_key(record):
    # Reporting series and original/restated balances are separate identities.
    return tuple(record.get(k) for k in ('fy', 'basis', 'series', 'balance_version'))


def validate_annual(records):
    seen = {}
    for record in records:
        key = annual_key(record)
        if key in seen:
            conflicts = [k for k in FINANCIAL_FIELDS if seen[key].get(k) != record.get(k)]
            raise SafetyError(f'Duplicate annual record {key}; conflicting financial fields: {conflicts}')
        seen[key] = record
    return seen


def protected_ids():
    registry = json.loads(REGISTRY.read_text())
    return set(registry['ledgers'])


def merge(existing, incoming, protected=False):
    """Return a copy with new annual rows/sources only; fail on any disagreement."""
    if existing['fund_number'] != incoming['fund_number']:
        raise SafetyError('Fund identity mismatch')
    old = validate_annual(existing['annual'])
    new = validate_annual(incoming['annual'])
    result = copy.deepcopy(existing)
    for key, record in new.items():
        if key in old:
            for field in FINANCIAL_FIELDS:
                if field in record and old[key].get(field) != record[field]:
                    raise SafetyError(f"{existing['fund_number']} {key}: conflicting {field}: "
                                      f"existing={old[key].get(field)!r}, extracted={record[field]!r}")
            continue
        if protected or existing.get('curation', {}).get('status') == 'curated':
            raise SafetyError(f"Protected ledger {existing['fund_number']}: new annual record {key} requires review")
        sid = record['source']
        source = incoming['sources'][sid]
        if sid in result['sources'] and result['sources'][sid] != source:
            raise SafetyError(f"Conflicting source reference {sid}")
        result['sources'][sid] = copy.deepcopy(source)
        result['annual'].append(copy.deepcopy(record))
    return result


def update_ledgers(records, out_dir):
    """Preflight the entire batch before writing. Existing identical files are untouched.

    New files use exclusive creation; changed files are checked again before writing.
    This is a single-writer command, not a concurrent ledger editor.
    """
    out_dir = Path(out_dir)
    protected = protected_ids()  # missing/invalid registry fails closed
    plans, seen = [], set()
    for record in records:
        fid = record['fund_number']
        if fid in seen:
            raise SafetyError(f'Duplicate extracted fund identity: {fid}')
        if Path(fid).name != fid or fid in ('.', '..'):
            raise SafetyError(f'Invalid fund identity: {fid}')
        seen.add(fid)
        validate_annual(record['annual'])
        path = out_dir / f'{fid}.json'
        if path.is_symlink():
            raise SafetyError(f'Refusing ledger symlink: {path}')
        before = path.read_bytes() if path.exists() else None
        if before is None:
            if fid in protected:
                raise SafetyError(f'Protected ledger {fid} must already exist; copy curated evidence into destination first')
            updated = record
        else:
            updated = merge(json.loads(before), record, fid in protected)
            if updated == json.loads(before):
                continue
        plans.append((path, before, json.dumps(updated, indent=1, ensure_ascii=False).encode()))
    out_dir.mkdir(parents=True, exist_ok=True)
    for path, before, payload in plans:
        if before is None:
            with path.open('xb') as stream:
                stream.write(payload)
        else:
            if path.read_bytes() != before:
                raise SafetyError(f'Ledger changed during extraction: {path}')
            # Preflight has proven this only appends annual rows and source entries.
            import os
            import tempfile
            with tempfile.NamedTemporaryFile(dir=out_dir, delete=False) as stream:
                temp = Path(stream.name)
                stream.write(payload)
            try:
                os.replace(temp, path)
            finally:
                temp.unlink(missing_ok=True)
    return [p.name for p, _, _ in plans]

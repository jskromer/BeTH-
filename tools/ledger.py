#!/usr/bin/env python3
"""Validate a fund ledger file against data/funds/SCHEMA.md.

Usage:  python3 tools/ledger.py data/funds/608.json [more files...]
Exit 1 on any error. Warnings do not fail the run.
"""
import json
import sys
from ledger_safety import SafetyError, validate_annual
from pathlib import Path

TYPES = {"general", "special_revenue", "capital_project", "debt_service",
         "enterprise", "internal_service", "fiduciary"}
RESTRICTIONS = {"restricted", "committed", "assigned", "unassigned", "enterprise"}
BASES = {"audited", "adopted", "projected"}
KINDS = {"transfer_in", "transfer_out", "cost_shift", "loan_in", "loan_out", "loan_repayment",
         "grant", "holiday", "indirect_reduction", "fee_change", "reduction",
         "write_off", "appropriation", "authorization"}
CONF = {"High", "Moderate", "Low", "Unknown"}


def check(path: Path):
    errors, warnings = [], []
    d = json.loads(path.read_text())
    err = errors.append
    warn = warnings.append

    for k in ("fund_number", "name", "type", "department", "annual", "flows", "sources", "status"):
        if k not in d:
            err(f"missing top-level field: {k}")
    if errors:
        return errors, warnings
    if d["type"] not in TYPES:
        err(f"type {d['type']!r} not in {sorted(TYPES)}")
    if d.get("restriction") not in RESTRICTIONS:
        err(f"restriction {d.get('restriction')!r} not in {sorted(RESTRICTIONS)}")
    src = d["sources"]
    for sid, s in src.items():
        for k in ("title", "url"):
            if not s.get(k):
                err(f"source {sid}: missing {k}")

    try:
        validate_annual(d["annual"])
    except SafetyError as exc:
        err(str(exc))

    fys = []
    for i, y in enumerate(d["annual"]):
        tag = f"annual[{i}] FY{y.get('fy')}"
        if not isinstance(y.get("fy"), int):
            err(f"{tag}: fy must be int")
        fys.append(y.get("fy"))
        if y.get("basis") not in BASES:
            err(f"{tag}: basis {y.get('basis')!r} not in {sorted(BASES)}")
        if y.get("source") not in src:
            err(f"{tag}: source {y.get('source')!r} not in sources")
        if y.get("confidence") not in CONF:
            err(f"{tag}: confidence {y.get('confidence')!r}")
        for k in ("revenue", "expenditure"):
            if k in y and y[k] is not None and not isinstance(y[k], (int, float)):
                err(f"{tag}: {k} must be a number or null")
    if len(fys) != len(set(fys)):
        warn("annual has duplicate fiscal years (allowed if bases differ)")

    ids = set()
    for i, f in enumerate(d["flows"]):
        tag = f"flows[{i}] {f.get('id')}"
        if not f.get("id"):
            err(f"flows[{i}]: missing id")
        elif f["id"] in ids:
            err(f"{tag}: duplicate id")
        ids.add(f.get("id"))
        if f.get("kind") not in KINDS:
            err(f"{tag}: kind {f.get('kind')!r} not in {sorted(KINDS)}")
        if not isinstance(f.get("fy"), int):
            err(f"{tag}: fy must be int")
        amt = f.get("amount")
        if amt is not None and (not isinstance(amt, (int, float)) or amt < 0):
            err(f"{tag}: amount must be a non-negative number or null")
        if amt is None and not f.get("note"):
            err(f"{tag}: amount is null; note must say why")
        if f.get("source") not in src:
            err(f"{tag}: source {f.get('source')!r} not in sources")
        if f.get("confidence") not in CONF:
            err(f"{tag}: confidence {f.get('confidence')!r}")
        if not f.get("instrument"):
            err(f"{tag}: missing instrument")
        if f.get("kind") in {"transfer_in", "loan_in", "loan_out", "grant", "cost_shift", "transfer_out", "loan_repayment"}:
            if not (f.get("from_fund") and f.get("to_fund")):
                err(f"{tag}: {f['kind']} needs from_fund and to_fund")
        rv = f.get("reviewer")
        if not rv:
            err(f"{tag}: missing reviewer")
        elif rv.startswith("agent:"):
            warn(f"{tag}: proposed by {rv}; will not render until reviewed")

    for i, o in enumerate(d.get("obligations", [])):
        if o.get("source") not in src:
            err(f"obligations[{i}]: source {o.get('source')!r} not in sources")
        if o.get("confidence") not in CONF:
            err(f"obligations[{i}]: confidence {o.get('confidence')!r}")
    return errors, warnings


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    bad = 0
    for p in argv[1:]:
        errors, warnings = check(Path(p))
        for w in warnings:
            print(f"WARN  {p}: {w}")
        for e in errors:
            print(f"ERROR {p}: {e}")
        if errors:
            bad += 1
        else:
            d = json.loads(Path(p).read_text())
            print(f"OK    {p}: {len(d['annual'])} years, {len(d['flows'])} flows, {len(d['sources'])} sources")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
"""Build one fund ledger JSON per fund column in the FY2025 ACFR.

Usage:  python3 tools/acfr_funds.py annual-comprehensive-financial-report-fy2025.pdf data/funds

Reads the governmental funds statement (p.77), the nonmajor governmental
combining statements (pp.237-254), the proprietary funds statement
(pp.85-86) and the internal service combining statement (pp.321-322),
and writes data/funds/<id>.json with the FY2025 year, a flow_detail block
for the money-flow diagram, and the page cited as source. Files that a
person has already curated are protected by data/curation/protected-ledgers.json.
All existing evidence is preserved; conflicts abort before any writes.
"""
import re
import sys
from pathlib import Path

import pdfplumber

sys.path.insert(0, str(Path(__file__).parent))
import acfr_parse  # noqa: E402

from ledger_safety import SafetyError, update_ledgers
from acfr_config import load_year

DEFAULT_CONFIG = load_year(2025)
FY = DEFAULT_CONFIG["fiscal_year"]
ACFR_URL = DEFAULT_CONFIG["source_url"]
NUMBERS = {  # City fund numbers where known (budget documents); others get an ACFR slug id
    "General Fund": "011", "Marina Operations": "608", "Sanitary Sewer": "611", "Capital Improvement": "501",
    "Infrastructure & Facilities Measure T1": "511", "Measure O Housing Bond": "ACFR-measure-o-housing-bond",
}
# Explicit FY2025 identities retain existing URLs, including the legacy truncated slug.
IDENTITIES = {
    ("Infrastructure & Facilities Measure T1", "debt_service"): "511-debt-service",
    ("Measure O Housing Bond", "debt_service"): "ACFR-measure-o-housing-bond-debt-service",
    ("GO 2015 Refunding Bonds for GO 2007 Refunding Bonds Series A", "debt_service"):
        "ACFR-go-2015-refunding-bonds-for-go-2007-refunding-bo-debt-service",
}
DEPT = {"enterprise": "Public Works / Parks / Planning", "internal_service": "Finance / Public Works / IT / HR"}
GOV_REV = ["Taxes", "Licenses and permits", "Intergovernmental", "Charges for service", "Fines and penalties",
           "Rents and royalties", "Franchise", "Private contributions and donations", "donations",
           "Investment income", "Investment income/ (loss)", "Miscellaneous"]
GOV_EXP = ["General government", "Public safety", "Highway and streets", "Highways and streets", "Health and welfare",
           "Culture-recreation", "Culture and recreation", "Community development and housing", "Economic development",
           "Principal repayment", "Interest and fiscal charges", "Debt issuance costs", "TRAN issuance costs", "Capital outlay:", "Capital outlay"]
OTHER_IN = ["Transfers in", "Debt proceeds", "Face value of refunding bonds issued", "Premium on bond issued",
            "Inception of leases and subscriptions", "Insurance Recoveries", "Sale of capital assets"]
OTHER_OUT = ["Transfers out", "Payment to refunded bond escrow agent"]


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:48]


def required(d, *labels):
    found = [(label, d[label]) for label in labels if label in d]
    if not found or any(type(value) is not int for _, value in found):
        raise SafetyError(f"Missing required financial statement label/value: {labels}")
    if len({value for _, value in found}) != 1:
        raise SafetyError(f"Conflicting financial statement labels: {found}")
    return found[0][1]


def governmental_expense_items(rows, config):
    """Recognize configured wrapped labels without losing or double-counting rows."""
    values, observed = {}, {}
    for raw_label, amount in rows.items():
        label = config['row_aliases'].get(raw_label, raw_label)
        if label not in GOV_EXP:
            continue
        if label in observed:
            raise SafetyError(f'Duplicate expenditure label aliases: {observed[label]!r}, {raw_label!r}')
        observed[label] = raw_label
        values[label] = amount
    return {label: values[label] for label in GOV_EXP if values.get(label)}


def governmental_financing_items(rows, config):
    """Normalize financing labels once; aliases must never duplicate a category."""
    values, observed = {}, {}
    for raw_label, amount in rows.items():
        label = config['row_aliases'].get(raw_label, raw_label)
        if label not in OTHER_IN:
            continue
        if label in observed:
            raise SafetyError(f'Duplicate financing label aliases: {observed[label]!r}, {raw_label!r}')
        observed[label] = raw_label
        values[label] = amount
    return {label: values[label] for label in OTHER_IN if values.get(label)}


def gov_record(name, d, ftype, page, config=None):
    config = config or DEFAULT_CONFIG
    labels = config["labels"]
    major_page = config["statements"][0]["pairs"][0][0]
    rev = {k: d.get(k) for k in GOV_REV if d.get(k)}
    exp = governmental_expense_items(d, config)
    ti = required(d, "Transfers in")
    to = required(d, "Transfers out")
    inflows = [{"line": k.rstrip(":"), "amount": v, "kind": "own"} for k, v in rev.items()]
    inflows += [{"line": k, "amount": v, "kind": "rescue" if k == "Transfers in" else "financing"}
                for k, v in governmental_financing_items(d, config).items()]
    outflows = [{"line": k.rstrip(":"), "amount": v} for k, v in exp.items()]
    outflows += [{"line": k, "amount": abs(d[k])} for k in OTHER_OUT if d.get(k)]
    return {
        "revenue": required(d, "Total revenues"), "expenditure": required(d, "Total expenditures"),
        "transfers_in": ti, "transfers_out": abs(to),
        "ending_balance": required(d, *labels["governmental_ending"]),
        "beginning_balance": required(d, *labels["governmental_major_beginning"]) if page == major_page else required(d, *labels["governmental_beginning"]),
        "inflows": inflows, "outflows": outflows,
    }


def prop_record(name, d, page, config=None):
    config = config or DEFAULT_CONFIG
    labels = config["labels"]
    rev_keys = [k for k in d if k and not k.startswith("Total") and d.get(k) and k in (
        "Parking related revenues", "Marina operations and maintenance", "Sewer service fees", "Clean storm water fees",
        "Refuse service fees", "Building permits", "Other permits", "Plan checking fees", "Other fees",
        "Equipment rentals service charge", "Building maintenance", "Central store service charge",
        "Workers’ compensation fees", "IT service fee", "Lease revenues", "Other revenues")]
    exp_keys = [k for k in ("Personnel services", "Employee benefits", "Transportation", "Repairs and maintenance",
                            "Materials and supplies", "Utilities", "Insurance", "Specialized and professional services",
                            "Depreciation", "Judgments and claims", "Communication", "General administration") if d.get(k)]
    inflows = [{"line": k, "amount": d[k], "kind": "own"} for k in rev_keys]
    for k in ("Investment earnings", "Capital grants - State", "Transfers in", "Receipt from interfund loans"):
        if d.get(k):
            inflows.append({"line": k, "amount": d[k], "kind": "own" if k == "Investment earnings" else "rescue"})
    outflows = [{"line": k, "amount": d[k]} for k in exp_keys]
    for k in ("Interest expense", "Transfers out"):
        if d.get(k):
            outflows.append({"line": k, "amount": abs(d[k])})
    return {
        "revenue": required(d, "Total operating revenues"), "expenditure": required(d, "Total operating expenses"),
        "nonoperating": required(d, "Total nonoperating revenues (expenses)"),
        "transfers_in": required(d, "Transfers in"), "transfers_out": abs(required(d, "Transfers out")),
        "ending_balance": required(d, "Total net position - ending"),
        "beginning_balance": required(d, *labels["proprietary_restated"]) if any(k in d for k in labels["proprietary_restated"]) else required(d, *labels["proprietary_beginning"]),
        "inflows": inflows, "outflows": outflows,
    }


def make(name, rec, ftype, page, statement, config=None):
    config = config or DEFAULT_CONFIG
    fy, sid = config["fiscal_year"], config["source_id"]
    fid = IDENTITIES.get((name, ftype), NUMBERS.get(name, "ACFR-" + slug(name)))
    year = {"fy": fy, "basis": "audited", "revenue": rec["revenue"], "expenditure": rec["expenditure"],
            "transfers_in": rec["transfers_in"], "transfers_out": rec["transfers_out"],
            "ending_balance": rec["ending_balance"], "source": sid, "confidence": "High",
            "note": f"{statement}, ACFR p.{page}. Beginning balance {rec['beginning_balance']:,}" if isinstance(rec.get("beginning_balance"), int) else f"{statement}, ACFR p.{page}"}
    if rec.get("nonoperating") is not None:
        year["nonoperating"] = rec["nonoperating"]
    return {
        "fund_number": fid, "name": name, "type": ftype,
        "department": DEPT.get(ftype, "See budget"),
        "established": {"year": None, "purpose": "Not yet researched", "source": sid},
        "legal_basis": "Not yet researched",
        "restriction": "enterprise" if ftype in ("enterprise", "internal_service") else "restricted",
        "self_supporting": ftype in ("enterprise", "internal_service"),
        "annual": [year],
        "flows": [],
        "flow_detail": {"fy": fy, "source": sid, "confidence": "High", "inflows": rec["inflows"], "outflows": rec["outflows"]},
        "obligations": [],
        "status": {"structural_deficit": bool(rec["revenue"] is not None and rec["expenditure"] is not None and rec["revenue"] < rec["expenditure"]),
                   "years_in_deficit": "one audited year loaded", "last_update": "2026-10-22",
                   "open_questions": [f"Only FY{fy} is loaded; prior years and the event ledger are not yet read for this fund."]},
        "sources": {sid: {"title": f"City of Berkeley, Annual Comprehensive Financial Report FY{fy}, {statement}, p.{page}", "url": config["source_url"], "date": config["source_date"]}},
        "generated_by": "tools/acfr_funds.py",
        "curation": {"status": "extracted", "policy": "append-only"},
    }


def extract(pdf_path, year=2025):
    config = load_year(year)
    with pdfplumber.open(pdf_path) as pdf:
        records, identities = [], set()
        ftype = "special_revenue"
        for statement in config['statements']:
            for left, right in statement['pairs']:
                names, out, labels = acfr_parse.parse_pair(pdf, left, right)
                for name in names:
                    if statement['id'] == 'nonmajor_governmental':
                        if name == 'Total Special Revenue Funds':
                            ftype = 'capital_project'
                        elif name == 'Total Capital Project Funds':
                            ftype = 'debt_service'
                    if not name or name.startswith('Total') or 'Governmental Funds' in name or name == 'Internal Service Funds':
                        continue
                    if statement['id'] == 'major_governmental':
                        kind = 'general' if name == 'General Fund' else ('capital_project' if name == 'Capital Improvement' else 'special_revenue')
                    elif statement['id'] == 'nonmajor_governmental':
                        kind = ftype
                    else:
                        kind = statement['id']
                    if statement['basis'] == 'modified_accrual':
                        rec = gov_record(name, out[name], kind, left, config)
                    else:
                        rec = prop_record(name, out[name], left, config)
                    record = make(name, rec, kind, left, statement['title'], config)
                    fid = record['fund_number']
                    if fid in identities:
                        raise SafetyError(f'Duplicate extracted fund identity: {fid}')
                    identities.add(fid)
                    records.append(record)
        return records


def main(pdf_path, out_dir):
    records = extract(pdf_path)
    written = update_ledgers(records, out_dir)
    print(f"Extracted {len(records)} funds; updated {len(written)} files; preserved existing evidence")
    return written


if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2])
    except SafetyError as exc:
        sys.exit(f"EXTRACTION SAFETY ERROR: {exc}")

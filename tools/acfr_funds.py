#!/usr/bin/env python3
"""Build one fund ledger JSON per fund column in the FY2025 ACFR.

Usage:  python3 tools/acfr_funds.py annual-comprehensive-financial-report-fy2025.pdf data/funds

Reads the governmental funds statement (p.77), the nonmajor governmental
combining statements (pp.237-254), the proprietary funds statement
(pp.85-86) and the internal service combining statement (pp.321-322),
and writes data/funds/<id>.json with the FY2025 year, a flow_detail block
for the money-flow diagram, and the page cited as source. Files that a
person has already curated (listed in KEEP) are left alone.
"""
import json
import re
import sys
from pathlib import Path

import pdfplumber

sys.path.insert(0, str(Path(__file__).parent))
import acfr_parse  # noqa: E402

FY = 2025
ACFR_URL = "https://berkeleyca.gov/sites/default/files/2026-01/annual-comprehensive-financial-report-fy2025.pdf"
KEEP = {"608"}  # hand-curated ledgers not to overwrite
NUMBERS = {  # City fund numbers where known (budget documents); others get an ACFR slug id
    "General Fund": "011", "Marina Operations": "608", "Sanitary Sewer": "611", "Capital Improvement": "501",
    "Infrastructure & Facilities Measure T1": "511", "Measure O Housing Bond": "ACFR-measure-o-housing-bond",
}
DEPT = {"enterprise": "Public Works / Parks / Planning", "internal_service": "Finance / Public Works / IT / HR"}
GOV_REV = ["Taxes", "Licenses and permits", "Intergovernmental", "Charges for service", "Fines and penalties",
           "Rents and royalties", "Franchise", "Private contributions and donations", "donations",
           "Investment income", "Investment income/ (loss)", "Miscellaneous"]
GOV_EXP = ["General government", "Public safety", "Highway and streets", "Highways and streets", "Health and welfare",
           "Culture-recreation", "Culture and recreation", "Community development and housing", "Economic development",
           "Principal repayment", "Interest and fiscal charges", "Debt issuance costs", "Capital outlay:", "Capital outlay"]
OTHER_IN = ["Transfers in", "Debt proceeds", "Face value of refunding bonds issued", "Premium on bond issued",
            "Inception of leases and subscriptions", "Insurance Recoveries", "Sale of capital assets"]
OTHER_OUT = ["Transfers out", "Payment to refunded bond escrow agent"]


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:48]


def gov_record(name, d, ftype, page):
    rev = {k: d.get(k) for k in GOV_REV if d.get(k)}
    exp = {k: d.get(k) for k in GOV_EXP if d.get(k)}
    ti = d.get("Transfers in") or 0
    to = d.get("Transfers out") or 0
    inflows = [{"line": k.rstrip(":"), "amount": v, "kind": "own"} for k, v in rev.items()]
    inflows += [{"line": k, "amount": d[k], "kind": "rescue" if k == "Transfers in" else "financing"} for k in OTHER_IN if d.get(k)]
    outflows = [{"line": k.rstrip(":"), "amount": v} for k, v in exp.items()]
    outflows += [{"line": k, "amount": abs(d[k])} for k in OTHER_OUT if d.get(k)]
    return {
        "revenue": d.get("Total revenues"), "expenditure": d.get("Total expenditures"),
        "transfers_in": ti, "transfers_out": abs(to),
        "ending_balance": d.get("Fund balance, June 30, 2025", d.get("Fund balances, June 30, 2025")),
        "beginning_balance": d.get("Fund balance, July 1, 2024", d.get("Fund balances, July 1, 2024")),
        "inflows": inflows, "outflows": outflows,
    }


def prop_record(name, d, page):
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
        "revenue": d.get("Total operating revenues"), "expenditure": d.get("Total operating expenses"),
        "nonoperating": d.get("Total nonoperating revenues (expenses)"),
        "transfers_in": d.get("Transfers in") or 0, "transfers_out": abs(d.get("Transfers out") or 0),
        "ending_balance": d.get("Total net position - ending"),
        "beginning_balance": d.get("Total net position - beginning, as restated", d.get("Total net position - beginning")),
        "inflows": inflows, "outflows": outflows,
    }


def make(name, rec, ftype, page, statement):
    fid = NUMBERS.get(name, "ACFR-" + slug(name))
    year = {"fy": FY, "basis": "audited", "revenue": rec["revenue"], "expenditure": rec["expenditure"],
            "transfers_in": rec["transfers_in"], "transfers_out": rec["transfers_out"],
            "ending_balance": rec["ending_balance"], "source": "acfr-2025", "confidence": "High",
            "note": f"{statement}, ACFR p.{page}. Beginning balance {rec['beginning_balance']:,}" if isinstance(rec.get("beginning_balance"), int) else f"{statement}, ACFR p.{page}"}
    if rec.get("nonoperating") is not None:
        year["nonoperating"] = rec["nonoperating"]
    return {
        "fund_number": fid, "name": name, "type": ftype,
        "department": DEPT.get(ftype, "See budget"),
        "established": {"year": None, "purpose": "Not yet researched", "source": "acfr-2025"},
        "legal_basis": "Not yet researched",
        "restriction": "enterprise" if ftype in ("enterprise", "internal_service") else "restricted",
        "self_supporting": ftype in ("enterprise", "internal_service"),
        "annual": [year],
        "flows": [],
        "flow_detail": {"fy": FY, "source": "acfr-2025", "confidence": "High", "inflows": rec["inflows"], "outflows": rec["outflows"]},
        "obligations": [],
        "status": {"structural_deficit": bool(rec["revenue"] is not None and rec["expenditure"] is not None and rec["revenue"] < rec["expenditure"]),
                   "years_in_deficit": "one audited year loaded", "last_update": "2026-10-22",
                   "open_questions": ["Only FY2025 is loaded; prior years and the event ledger are not yet read for this fund."]},
        "sources": {"acfr-2025": {"title": f"City of Berkeley, Annual Comprehensive Financial Report FY2025, {statement}, p.{page}", "url": ACFR_URL, "date": "2026-01"}},
        "generated_by": "tools/acfr_funds.py",
    }


def main(pdf_path, out_dir):
    pdf = pdfplumber.open(pdf_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written, skipped = [], []

    def emit(name, rec, ftype, page, statement):
        if not name or name.startswith("Total") or "Governmental Funds" in name or name in ("Internal Service Funds", "Total Nonmajor"):
            return
        r = make(name, rec, ftype, page, statement)
        if r["fund_number"] in KEEP:
            skipped.append(name)
            return
        if any(w[0] == r["fund_number"] for w in written):
            r["fund_number"] = r["fund_number"] + "-" + ftype.replace("_", "-")
        p = out_dir / f"{r['fund_number']}.json"
        p.write_text(json.dumps(r, indent=1, ensure_ascii=False))
        written.append((r["fund_number"], name, ftype))

    # major governmental funds
    names, out, labels = acfr_parse.parse_pair(pdf, 77, None)
    for n in names:
        ftype = "general" if n == "General Fund" else ("capital_project" if n == "Capital Improvement" else "special_revenue")
        emit(n, gov_record(n, out[n], ftype, 77), ftype, 77, "Statement of Revenues, Expenditures and Changes in Fund Balances, Governmental Funds")
    # nonmajor governmental: type switches at the subtotal columns
    ftype = "special_revenue"
    for left in range(237, 254, 2):
        names, out, labels = acfr_parse.parse_pair(pdf, left, left + 1)
        for n in names:
            if n == "Total Special Revenue Funds":
                ftype = "capital_project"; continue
            if n == "Total Capital Project Funds":
                ftype = "debt_service"; continue
            emit(n, gov_record(n, out[n], ftype, left), ftype, left, "Combining Statement of Revenues, Expenditures and Changes in Fund Balances, Nonmajor Governmental Funds")
    # enterprise
    names, out, labels = acfr_parse.parse_pair(pdf, 85, 86)
    for n in names:
        emit(n, prop_record(n, out[n], 85), "enterprise", 85, "Statement of Revenues, Expenses and Changes in Net Position, Proprietary Funds")
    # internal service
    names, out, labels = acfr_parse.parse_pair(pdf, 321, 322)
    for n in names:
        emit(n, prop_record(n, out[n], 321), "internal_service", 321, "Combining Statement of Revenues, Expenses and Changes in Net Position, Internal Service Funds")
    print(f"wrote {len(written)} fund files; kept {skipped}")
    from collections import Counter
    print(Counter(t for _, _, t in written))
    return written


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

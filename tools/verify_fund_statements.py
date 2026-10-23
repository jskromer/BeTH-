#!/usr/bin/env python3
"""Check every fund's audited figures against the ACFR statement pages, independently of the extractor.

Usage:  python3 tools/verify_fund_statements.py            # print the result
        python3 tools/verify_fund_statements.py --write    # also write data/dashboard/fund-statement-check.json

The extractor (tools/acfr_parse.py) assigns values to fund columns by word
position. This check does not use it. It reads each statement page as plain
text lines, keeps the trailing run of numbers on each line, and builds the
page's columns as vectors of values. A fund passes when its five figures
(revenue, expenditures/operating expenses, transfers in, transfers out,
ending balance/net position) appear together in one column, in statement row
order, at the rows of those labels (facing pages carry no labels, so their
rows may drift by up to three lines). Funds are then assigned one-to-one to
columns, so two funds can never be satisfied by the same column. No fund
names are used: a misassigned value cannot pass.

Pages and labels come from data/dashboard/statement-totals.json
(`years.<fy>.fund_statements`).
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/dashboard/statement-totals.json"
DATA_DIR = ROOT / "data/funds"
OUT = ROOT / "data/dashboard/fund-statement-check.json"
TOKEN = re.compile(r"\(\d{1,3}(?:,\d{3})*\)|\d{1,3}(?:,\d{3})*|-")
DRIFT = 3


def value(t):
    if t == "-":
        return 0
    v = int(t.strip("()").replace(",", ""))
    return -v if t.startswith("(") else v


def numeric_rows(pdf, page_no):
    """(label, [values]) for each text line that ends in a run of statement numbers."""
    rows = []
    for line in (pdf.pages[page_no - 1].extract_text() or "").split("\n"):
        parts = line.replace("$", " ").split()
        k = len(parts)
        while k and TOKEN.fullmatch(parts[k - 1]):
            k -= 1
        if k < len(parts):
            rows.append((" ".join(parts[:k]), [value(t) for t in parts[k:]]))
    return rows


def _mode(xs):
    return collections.Counter(xs).most_common(1)[0][0] if xs else 0


def page_columns(pdf, left, right, labels):
    """Columns of one statement spread: (page label, value vector, label row indices, drift allowed)."""
    rows = numeric_rows(pdf, left)
    n = _mode([len(v) for lab, v in rows if lab])
    rows = [(lab, v) for lab, v in rows if len(v) == n]
    idx = []
    for alts in labels:
        hit = [i for i, (lab, _) in enumerate(rows) if lab in alts]
        if not hit:
            raise ValueError(f"label {alts} not found on page {left}")
        idx.append(hit[0])
    pages = f"{left}" if not right else f"{left}-{right}"
    cols = [(pages, [v[j] for _, v in rows], idx, 0) for j in range(n)]
    if right:
        rrows = [v for lab, v in numeric_rows(pdf, right) if not lab]
        m = _mode([len(v) for v in rrows])
        rrows = [v for v in rrows if len(v) == m]
        cols += [(pages, [v[j] for v in rrows], idx, DRIFT) for j in range(m)]
    return cols


def matches(col, key):
    _, vec, idx, drift = col
    last = -1
    for i, v in zip(idx, key):
        cands = [r for r in range(max(last + 1, i - drift), min(len(vec), i + drift + 1)) if vec[r] == v]
        if not cands:
            return False
        last = min(cands, key=lambda r: abs(r - i))
    return True


def fund_key(y):
    # statements print transfers out in parentheses
    return (y["revenue"], y["expenditure"], y["transfers_in"], -(y["transfers_out"] or 0), y["ending_balance"])


def group_of(ftype):
    return ftype if ftype in ("enterprise", "internal_service") else "governmental"


def verify(fy=2025, data_dir=DATA_DIR, config_path=CONFIG, pdf_path=None):
    import pdfplumber  # only this check needs it

    cfg = json.loads(Path(config_path).read_text())["years"][str(fy)]
    fs = cfg["fund_statements"]
    pdf_path = Path(pdf_path or ROOT / fs["pdf"])
    sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    if sha != cfg["source"]["pdf_sha256"]:
        raise ValueError(f"{pdf_path} is not the PDF recorded in {config_path}")
    with pdfplumber.open(pdf_path) as pdf:
        columns = {g: [c for left, right in spec["pages"] for c in page_columns(pdf, left, right, spec["labels"])]
                   for g, spec in fs["groups"].items()}
    funds = {}
    for p in sorted(Path(data_dir).glob("*.json")):
        d = json.loads(p.read_text())
        rows = [y for y in d["annual"] if y.get("fy") == fy and y.get("basis") == "audited"
                and y.get("series") is None and y.get("ending_balance") is not None]
        if rows:
            funds[d["fund_number"]] = (group_of(d["type"]), fund_key(rows[0]))
    cands = {fid: [k for k, c in enumerate(columns[g]) if matches(c, key)] for fid, (g, key) in funds.items()}
    # one-to-one: fewest candidates first (augmenting paths would be needed only if greedy fails; it is checked)
    taken, assigned = {g: set() for g in columns}, {}
    for fid in sorted(cands, key=lambda f: (len(cands[f]), f)):
        g = funds[fid][0]
        free = [k for k in cands[fid] if k not in taken[g]]
        if free:
            taken[g].add(free[0])
            assigned[fid] = free[0]
    result = {}
    for fid, (g, key) in sorted(funds.items()):
        if fid in assigned:
            col = columns[g][assigned[fid]]
            result[fid] = {"status": "matched", "pages": col[0], "values": list(key),
                           "candidate_columns": len(cands[fid])}
        else:
            result[fid] = {"status": "not found" if not cands[fid] else "column already taken", "values": list(key)}
    unassigned = {g: len(columns[g]) - len(taken[g]) for g in columns}
    return {"fy": fy, "pdf_sha256": sha, "method": "plain-text statement columns; see tools/verify_fund_statements.py",
            "fields": ["revenue", "expenditure", "transfers_in", "transfers_out (negative as printed)", "ending_balance"],
            "funds": result, "matched": sum(1 for r in result.values() if r["status"] == "matched"),
            "columns_without_a_fund": unassigned}


def main(argv):
    res = verify()
    bad = {k: v for k, v in res["funds"].items() if v["status"] != "matched"}
    print(f"FY{res['fy']}: {res['matched']} of {len(res['funds'])} funds match a statement column; "
          f"columns without a fund (statement totals/subtotals): {res['columns_without_a_fund']}")
    for fid, r in bad.items():
        print(f"  {fid}: {r['status']} {r['values']}")
    if "--write" in argv:
        OUT.write_text(json.dumps(res, indent=1) + "\n")
        print(f"wrote {OUT.relative_to(ROOT)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

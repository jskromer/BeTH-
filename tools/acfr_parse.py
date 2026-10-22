#!/usr/bin/env python3
"""Parse fund-column financial statements out of a Berkeley ACFR PDF.

A statement page lays out one row label per line on the left and one value
per fund column (a right-aligned number or a "-"). The first and last money
rows carry a "$" at the left edge of every column; those "$" positions define
the column spans and the label boundary. Facing continuation pages carry
more fund columns for the same rows, without labels. Fund names are the
stacked header words above the first data row, assigned to columns by span.

Check one pair:  python3 tools/acfr_parse.py <pdf> 237 238
"""
import re
import sys
from collections import defaultdict

import pdfplumber
from ledger_safety import SafetyError

NUM = re.compile(r"^\(?[\d,]+\)?$")
MONEY = re.compile(r"^\(?\d{1,3}(,\d{3})+\)?$|^\(?\d{1,3}\)?$")  # comma-grouped or < 1000
FURNITURE = re.compile(r"^(INTRODUCTORY|FINANCIAL|STATISTICAL|SECTION|Annual|Comprehensive|Financial|Report|/City|City|of|Berkeley|Berkeley,|California|SS?TT.*|FIN.*|IINN.*|SSEE.*|SL|ESCET.*|``)$")
BANNER_WORDS = {"Special", "Revenue", "Funds", "Capital", "Project", "Projects", "Debt", "Service", "Business-type",
                "Activities", "-", "Enterprise", "Governmental", "Internal", "Nonmajor", "Major", "Fund", "Trust", "Custodial", "Other"}


def _lines(page, ytol=3):
    words = page.extract_words(x_tolerance=2, keep_blank_chars=False)
    rows = defaultdict(list)
    for w in words:
        rows[round(w["top"] / ytol) * ytol].append(w)
    return [(y, sorted(rows[y], key=lambda w: w["x0"])) for y in sorted(rows)]


def _to_num(t):
    t = t.replace(",", "")
    neg = t.startswith("(") and t.endswith(")")
    t = t.strip("()")
    try:
        v = int(t)
    except ValueError:
        return None
    return -v if neg else v


def _spans(lines):
    """Column spans from the line with the most '$' markers."""
    best = []
    for y, ln in lines:
        d = [w["x0"] for w in ln if w["text"] == "$"]
        if len(d) > len(best):
            best = d
    spans = []
    for j, x in enumerate(best):
        right = best[j + 1] - 1 if j + 1 < len(best) else 1e9
        spans.append((x, right))
    return spans


def parse_page(page):
    """Return (fund_names, [(y, label, [values per column])], labeled)."""
    lines = _lines(page)
    spans = _spans(lines)
    if not spans:
        return [], [], False
    label_x = spans[0][0] - 2
    labeled = label_x > 120

    def col_of(x):
        for j, (a, b) in enumerate(spans):
            if a <= x <= b:
                return j
        return None

    def data_tokens(ln):
        return [(col_of(w["x0"]), w) for w in ln if w["x0"] > label_x and (NUM.match(w["text"]) or w["text"] == "-")]

    def is_data(ln):
        toks = [w for j, w in data_tokens(ln) if j is not None and (w["text"] == "-" or MONEY.match(w["text"]))]
        return len(toks) >= max(2, len(spans) // 2)

    start = 0
    for i, (y, ln) in enumerate(lines):
        txt = " ".join(w["text"] for w in ln)
        if "year ended" in txt or ("June 30, 20" in txt and ("For" in txt or "As of" in txt)):
            start = i + 1
            break
    try:
        first = next(i for i, (y, ln) in enumerate(lines) if is_data(ln))
    except StopIteration:
        return [], [], labeled
    names = [[] for _ in spans]
    for y, ln in lines[start:first]:
        ws = [w for w in ln if w["x0"] > label_x - 30 and not FURNITURE.match(w["text"])]
        if not ws or all(w["text"] in BANNER_WORDS for w in ws):
            continue
        for w in ws:
            cx = (w["x0"] + w["x1"]) / 2
            j = col_of(cx)
            if j is None:
                j = min(range(len(spans)), key=lambda k: abs((spans[k][0] + min(spans[k][1], spans[k][0] + 80)) / 2 - cx))
            names[j].append(w["text"])
    names = [" ".join(n).strip() for n in names]
    rows = []
    for y, ln in lines[first:]:
        toks = data_tokens(ln)
        label = " ".join(w["text"] for w in ln if w["x0"] <= label_x and w["text"] != "$").strip() if labeled else ""
        vals = [None] * len(spans)
        got = False
        for j, w in toks:
            if j is None:
                continue
            vals[j] = 0 if w["text"] == "-" else _to_num(w["text"])
            got = True
        if got:
            rows.append((y, label, vals))
        elif labeled and label:
            rows.append((y, label, None))
    return names, rows, labeled


def parse_pair(pdf, left_no, right_no=None, verbose=False):
    """Join a labeled page with its facing continuation. Returns (names, {fund: {label: v}}, labels)."""
    ln, lrows, _ = parse_page(pdf.pages[left_no - 1])
    rn, rrows = [], []
    if right_no:
        rn, rrows, _ = parse_page(pdf.pages[right_no - 1])
    ldata = [(y, lab, v) for y, lab, v in lrows if v is not None]
    rdata = [(y, v) for y, _, v in rrows if v is not None]
    names = ln + rn
    if not ln or (right_no and not rn):
        raise SafetyError(f"Missing statement columns on pages {left_no}/{right_no}")
    if len(names) != len(set(names)):
        raise SafetyError(f"Duplicate statement fund columns on pages {left_no}/{right_no}")
    out = {n: {} for n in names}
    labels = []
    # monotonic y-matching with drift tolerance: pages drift a few px by the bottom
    ri = 0
    for y, lab, lv in ldata:
        rv = []
        if rn:
            while ri < len(rdata) and rdata[ri][0] < y - 8:
                ri += 1
            if ri < len(rdata) and abs(rdata[ri][0] - y) <= 8:
                rv = rdata[ri][1]
                ri += 1
            else:
                rv = [None] * len(rn)
                if verbose and lab:
                    print(f"  warn: no match for '{lab}' on page {right_no}", file=sys.stderr)
        labels.append(lab)
        for n, v in zip(names, lv + rv):
            if lab and lab in out[n]:
                raise SafetyError(f"Duplicate statement label {lab!r} for {n}, page {left_no}")
            out[n][lab] = v
    return names, out, labels


if __name__ == "__main__":
    pdf = pdfplumber.open(sys.argv[1])
    l = int(sys.argv[2]); r = int(sys.argv[3]) if len(sys.argv) > 3 else None
    names, out, labels = parse_pair(pdf, l, r, verbose=True)
    print("funds:", names)
    print("rows:", labels)
    for n in names:
        d = out[n]
        print(f"  {n[:44]:44s} " + " | ".join(f"{k[:18]}={d.get(k)}" for k in labels if k.startswith(('Total', 'Fund balance, June', 'Net position', 'Change', 'Total net position - ending'))))

#!/usr/bin/env python3
"""Extract FY2027-2031 CIP project rows from the City's proposed-CIP presentation.

Source: "PROPOSED FIVE-YEAR CAPITAL IMPROVEMENT PROGRAM FISCAL YEARS 2027-2031",
City of Berkeley, Council agenda attachment Item 02 (FY2027-FY2028 budget cycle).

Design rules:
  * Amounts are assigned to a fiscal year by their COLUMN POSITION in the text
    layer, taken from each table's own header row -- never by the order in which
    dollar signs appear. A row printing only an FY2028 figure must not be read as
    FY2027.
  * Tables whose first column is "Funding Source" list funding, not projects, and
    are captured separately rather than mixed into the project list.
  * Any field the document does not print is emitted as null. Nothing is inferred.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources' / 'cip-fy27-31-presentation.txt'
OUT = ROOT / 'data' / 'cip-projects.json'

BANNER = re.compile(r'^\s*(PRW|PUBLIC WORKS|IT)\s+FY27-28 CIP BUDGET\s*(.*?)\s*$', re.I)
DEPT = {'PRW': 'Parks, Recreation & Waterfront', 'PUBLIC WORKS': 'Public Works',
        'IT': 'Information Technology'}
# Header row of a table: tells us the column offsets for FY2027 / FY2028.
HDR = re.compile(r'(Project|Funding Source|Select CIP[\w ]*|IT Projects)\s*​?\s+')
FY27 = re.compile(r'FY\s*2027')
FY28 = re.compile(r'FY\s*2028')
MONEY = re.compile(r'\$\s*([\d,]+(?:\.\d{2})?)')
STOP = re.compile(r'^\s*(Total|Expense Total|Funding Total|GRAND TOTAL)', re.I)
# Chart-label debris: a bare fund name ending in a comma, or a lone page number.
DEBRIS = re.compile(r'^\s*(?:[\w &\-]+,\s*)+\s*$|^\s*\d{1,3}\s*$|^\s*•')
FUND_WORDS = re.compile(
    r'^(Marina|Parks Tax|CIP|Camps|Bayer|Sanitary Sewer|Measure |State |Private |Stormwater|'
    r'Equipment Replacement|Zero Waste|Clean Storm Water|Gas Tax|Capital Improvement|'
    r'Playground Camp|Permit Service|Street Light|Parking Meter)', re.I)


def money(s):
    return int(float(s.replace(',', '')))


class Table:
    """One printed table: its kind, its category, and its FY column offsets."""

    def __init__(self, line, dept, category):
        self.dept, self.category = dept, category
        # Row kind is decided per row, not per table: PRW decks print a header
        # reading "Funding Source  FY2027  FY2028" above tables of projects.
        m27, m28 = FY27.search(line), FY28.search(line)
        self.c27 = m27.start() if m27 else None
        self.c28 = m28.start() if m28 else None
        # Split point between the two year columns.
        self.mid = (self.c27 + self.c28) / 2 if (self.c27 is not None and self.c28 is not None) else None
        self.has_fund_col = 'funding source' in line.lower()

    def assign(self, amounts):
        """amounts: list of (char_offset, value). Returns (fy27, fy28, ambiguous)."""
        if self.mid is None:
            # Single-year table, or header we could not read: cannot place reliably.
            if self.c27 is not None and self.c28 is None:
                return (amounts[0][1] if amounts else None), None, False
            return None, None, True
        fy27 = fy28 = None
        for off, val in amounts:
            if off < self.mid:
                fy27 = val if fy27 is None else fy27
            else:
                fy28 = val if fy28 is None else fy28
        return fy27, fy28, False


def parse():
    lines = SRC.read_text().splitlines()
    projects, funding, dept, category, table = [], [], None, None, None
    for ln, line in enumerate(lines, 1):
        b = BANNER.match(line)
        if b:
            dept = DEPT.get(b.group(1).upper(), b.group(1))
            cat = re.sub(r'Power BI Desktop', '', b.group(2)).strip()
            category = cat or None
            table = None
            continue
        if dept is None:
            continue
        # A header row starts a new table and fixes its column geometry.
        if HDR.match(line.lstrip()) and (FY27.search(line) or FY28.search(line)):
            table = Table(line, dept, category)
            continue
        if table is None or STOP.match(line) or DEBRIS.match(line) or not line.strip():
            continue
        found = [(m.start(), money(m.group(1))) for m in MONEY.finditer(line)]
        if not found:
            # PRW decks print the category on the line after the header.
            t = line.strip()
            if t and len(t) < 40 and t.endswith(('Projects', 'Project')) and table.category is None:
                table.category = t
            continue
        head = line[:found[0][0]].rstrip()
        if len(head.strip()) < 4:
            continue
        fy27, fy28, ambiguous = table.assign(found)
        # Separate the funding-source column when the project table carries one.
        fund, name = None, re.sub(r'\s{2,}', ' ', head).strip(' .​')
        if table.has_fund_col:
            m = re.search(r'\s{2,}(\S.*)$', head)
            if m and FUND_WORDS.match(m.group(1).strip()):
                fund = re.sub(r'\s{2,}', ' ', m.group(1)).strip()
                name = re.sub(r'\s{2,}', ' ', head[:m.start()]).strip(' .​')
        if not name or len(name) < 4:
            continue
        rec = {'label': name, 'department': dept, 'category': table.category,
               'funding_source_as_printed': fund, 'fy2027_proposed': fy27,
               'fy2028_proposed': fy28, 'year_unassignable': ambiguous, 'source_line': ln}
        # Per-row kind: a row whose only text IS a fund name is a funding subtotal,
        # not a project. A row carrying a project name is a project.
        if fund is None and FUND_WORDS.match(name):
            rec['funding_source_as_printed'] = name
            rec.pop('label')
            funding.append(rec)
        else:
            projects.append(rec)
    return projects, funding


def dedupe(rows, key):
    seen, out = set(), []
    for r in rows:
        k = key(r)
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def main():
    projects, funding = parse()
    projects = dedupe(projects, lambda r: (r['label'], r['funding_source_as_printed'],
                                           r['fy2027_proposed'], r['fy2028_proposed']))
    funding = dedupe(funding, lambda r: (r['funding_source_as_printed'], r['category'],
                                         r['fy2027_proposed'], r['fy2028_proposed']))
    doc = {
        'schema_version': 2,
        'extracted': '2026-10-23',
        'source': {
            'title': 'Proposed Five-Year Capital Improvement Program, Fiscal Years 2027-2031',
            'body': 'City of Berkeley, Council agenda attachment Item 02',
            'url': 'https://berkeleyca.gov/sites/default/files/legislative-body-meeting-attachments/'
                   'Item%2002%20Proposed%20FY27-FY31%20Proposed%20CIP%20Budget%20Presentation.pdf',
            'local_copy': 'phase2/sources/cip-fy27-31-presentation.pdf',
            'pages': 44,
            'document_states': 'FY 2027 - FY 2031 CIP Total Projects = 149 projects',
        },
        'evidence_class': 'BUDGET_PROPOSED',
        'caveats': [
            'PROPOSED FY2027/FY2028 budget figures from a presentation deck. Not adopted appropriations, '
            'not expenditures, not encumbrances, not cash.',
            'The deck states 149 projects across the five-year program but prints line-item tables for only '
            'a subset, almost all FY2027-FY2028. These rows are what the document actually prints.',
            'FY2029-FY2031 line items are not printed in this source.',
            'Amounts are assigned to a fiscal year by column position taken from each table header, not by '
            'the order dollar signs appear. Rows whose header geometry could not be read are flagged '
            'year_unassignable and left null.',
            'No expenditure, encumbrance, remaining-authorization, schedule, status or restriction data '
            'exists in this source. Every such field is null and must come from the adopted budget, an '
            'encumbrance report, and restriction research.',
            'Funding-source subtotal tables are captured separately in funding_source_rows and must never '
            'be summed together with project rows.',
        ],
        'project_count_stated_by_city': 149,
        'project_rows_extracted': len(projects),
        'funding_rows_extracted': len(funding),
        'projects': projects,
        'funding_source_rows': funding,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1) + '\n')
    print(f'projects: {len(projects)}  funding rows: {len(funding)} -> {OUT.relative_to(Path.cwd())}')
    print(f"  year_unassignable: {sum(1 for r in projects if r['year_unassignable'])}")
    print(f"  with printed funding source: {sum(1 for r in projects if r['funding_source_as_printed'])}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

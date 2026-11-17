#!/usr/bin/env python3
"""Flag Learn About Berkeley pages that are due for a recheck.

Reads docs/data/pages.json. A page is flagged when:
  - one of its trigger dates has passed since it was last checked,
  - it has gone longer than review_every_days without a check,
  - it contains a phrase listed in stale_phrases after that phrase's date
    (unless the page lists it in ignore_phrases), or
  - it exists in docs/ but is missing from the registry.

Usage:
  python3 tools/staleness_check.py                # report (markdown) to stdout
  python3 tools/staleness_check.py --today 2027-01-20
  python3 tools/staleness_check.py --mark berkeley-ferry-waterfront.html [--date YYYY-MM-DD]
Exit code 1 when anything is flagged.
"""
import argparse, datetime as dt, fnmatch, glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, 'docs')
REG = os.path.join(DOCS, 'data', 'pages.json')

def d(s): return dt.date.fromisoformat(s)

def text_of(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    s = re.sub(r'<(script|style).*?</\1>', '', s, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s)))

def entry_for(reg, name):
    if name in reg['pages']: return reg['pages'][name], name
    for pat, e in reg['groups'].items():
        if fnmatch.fnmatch(name, pat): return e, pat
    return None, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--today'); ap.add_argument('--mark'); ap.add_argument('--date')
    a = ap.parse_args()
    reg = json.load(open(REG, encoding='utf-8'))
    today = d(a.today) if a.today else dt.date.today()

    if a.mark:
        e, key = entry_for(reg, a.mark)
        if not e: sys.exit(f'{a.mark} is not in the registry')
        e['checked'] = a.date or today.isoformat()
        json.dump(reg, open(REG, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        print(f'{key}: checked = {e["checked"]}'); return

    flags = []
    for path in sorted(glob.glob(os.path.join(DOCS, '*.html'))):
        name = os.path.basename(path)
        e, key = entry_for(reg, name)
        if not e:
            flags.append((name, 'Not in docs/data/pages.json; add it')); continue
        checked = d(e['checked'])
        if key == name:  # per-page checks once, not once per grouped file
            for t in e.get('triggers', []):
                if t.get('date') and checked < d(t['date']) <= today:
                    flags.append((name, f'{t["date"]}: {t["event"]}'))
            if (today - checked).days > e.get('review_every_days', 90):
                flags.append((name, f'Last checked {e["checked"]} ({(today-checked).days} days ago)'))
        txt = None
        for ph in reg.get('stale_phrases', []):
            if ph['text'] in e.get('ignore_phrases', []): continue
            if today >= d(ph['after']):
                txt = txt or text_of(path)
                if ph['text'].lower() in txt.lower():
                    flags.append((name, f'Contains "{ph["text"]}": {ph["why"]}'))
    for pat, e in reg['groups'].items():
        checked = d(e['checked'])
        for t in e.get('triggers', []):
            if t.get('date') and checked < d(t['date']) <= today:
                flags.append((pat, f'{t["date"]}: {t["event"]}'))
        if (today - checked).days > e.get('review_every_days', 90):
            flags.append((pat, f'Last checked {e["checked"]}'))
    for name in reg['pages']:
        if not os.path.exists(os.path.join(DOCS, name)):
            flags.append((name, 'In the registry but the file is missing'))

    upcoming = sorted({(t['date'], t['event']) for e in list(reg['pages'].values()) + list(reg['groups'].values())
                       for t in e.get('triggers', []) if t.get('date') and today < d(t['date']) <= today + dt.timedelta(days=45)})
    print(f'# Staleness check, {today.isoformat()}\n')
    if flags:
        print(f'{len(flags)} item(s) need attention:\n')
        for n, why in flags: print(f'- **{n}** — {why}')
    else:
        print('Nothing due.')
    if upcoming:
        print('\nComing up in the next 45 days:\n')
        for dd, ev in upcoming: print(f'- {dd} — {ev}')
    print('\nPages with no dated trigger still need the monthly City Auditor feed check (see OPERATIONS.md).')
    sys.exit(1 if flags else 0)

if __name__ == '__main__': main()

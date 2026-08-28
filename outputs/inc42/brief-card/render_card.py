#!/usr/bin/env python3
"""Backtest the proposed Inc42 home brief-card logic over the real 61-day corpus.

Inputs (read-only):
  42_posts.csv    - article metadata export
  summaries.json  - scraped 3-bullet summary blocks
Outputs:
  cards.txt       - a rendered card for every day
  backtest.csv    - per-day tile/row coverage for auditing
"""
import csv, json, re, html, datetime, sys, os
from collections import defaultdict

USD_CR = 8.7  # $1 Mn -> INR Cr

MONEY = re.compile(r'(\$|₹|INR|Rs\.?)\s?([\d,]+(?:\.\d+)?)\s*(Mn|Bn|Cr|Lakh|Million|Billion|Crore|K)?', re.I)
USD_MULT = {'mn':1,'million':1,'bn':1000,'billion':1000,'k':.001}
INR_MULT = {'cr':1,'crore':1,'lakh':.01,'mn':.1,'bn':100}
FWD = re.compile(r'\b(could|would|may |might|signals?|marks?|set[s]? (?:a|the) (?:precedent|stage)|'
                 r'indicat|suggest|reflect|underscore|comes? (?:as|amid|after)|amid|positions?|'
                 r'aims? to|expects?|is expected|plans? to|likely|paving|bigger test)\b', re.I)
NUM = re.compile(r'\d')
STOP = set('the a an in of to and for as at on its with from over after by is are was were '
           'that this it has have had will be been but or not'.split())

# development_tag -> short eyebrow
EYEBROW = {
    'Startup Funding & Investments':'FUNDING', 'Startup IPO':'IPO',
    'Startup Financials':'FINANCIALS', 'Business Updates':'BUSINESS',
    'Controversies':'CONTROVERSY', 'Government & Policies':'POLICY',
    'Industry Trends':'TRENDS', 'Startup Mergers & Acquisitions':'M&A',
    'People & Culture':'PEOPLE', 'Fund Launches':'FUNDS',
    'Startup Layoffs':'LAYOFFS', 'Cohort Launches':'COHORTS',
}
BLANK = ('NULL','null','undefined','TBD','','None')


def amounts(text):
    """All INR-Cr amounts mentioned in text."""
    out = []
    for cur, num, unit in MONEY.findall(text or ''):
        try: n = float(num.replace(',', ''))
        except ValueError: continue
        u = (unit or '').lower()
        v = n * USD_CR * USD_MULT.get(u, 0) if cur == '$' else n * INR_MULT.get(u, 0)
        if v > 0: out.append(v)
    return out


def toks(s):
    return set(re.findall(r'[a-z0-9]+', (s or '').lower())) - STOP


def fmt_cr(v):
    if v >= 100000: return '₹%.2f L Cr' % (v/100000)
    if v >= 1000:   return '₹%s Cr' % format(int(round(v)), ',')
    return '₹%d Cr' % round(v)


def companies(rec):
    c = rec.get('companies')
    if c in BLANK or not c: return []
    return [x.strip() for x in re.split(r'[|,;]', c) if x.strip() and x.strip() not in BLANK]


# ---------------------------------------------------------------- row line
def pick_line(headline, bullets):
    """Plan step 3: bullet 2 if it carries a 'so what'; else the most
    number-dense non-duplicate bullet; else nothing. Returns (line, source)."""
    if not bullets: return None, 'none'
    h = toks(headline)
    def dup(b):
        t = toks(b)
        return bool(h) and len(h & t) / len(h) >= 0.40

    if len(bullets) >= 2 and FWD.search(bullets[1]) and not dup(bullets[1]):
        return bullets[1], 'b2-sowhat'

    cands = [(i, b) for i, b in enumerate(bullets) if not dup(b) and NUM.search(b)]
    if cands:
        i, b = max(cands, key=lambda x: len(NUM.findall(x[1])))
        return b, 'b%d-number' % (i+1)

    for i, b in enumerate(bullets):
        if not dup(b): return b, 'b%d-fallback' % (i+1)
    return None, 'all-duplicate'


def clip(s, n=64):
    s = re.sub(r'\s+', ' ', s or '').strip()
    if len(s) <= n: return s
    cut = s[:n].rsplit(' ', 1)[0]
    return cut.rstrip(' ,.;:') + '…'


# ---------------------------------------------------------------- tiles
def build_tiles(day_items, tracked=()):
    """Returns list of (value, label) tiles. Never emits a zero/blank tile."""
    tiles = []
    # 1. biggest attributed number of the day
    best = (0, None)
    for rec, summ in day_items:
        pool = [rec['article_title']] + (summ or [])
        m = max(amounts(' '.join(pool)), default=0)
        if m > best[0]: best = (m, rec)
    if best[1] is not None:
        who = (companies(best[1]) or [None])[0]
        tiles.append((fmt_cr(best[0]), ('%s · biggest today' % who) if who else 'biggest today'))

    # 2. funding rounds -- suppressed entirely when none
    fr = [(r, s) for r, s in day_items if r['development_tag'] == 'Startup Funding & Investments']
    if fr:
        tot = sum(max(amounts(' '.join([r['article_title']] + (s or []))), default=0) for r, s in fr)
        lbl = 'funding round' + ('s' if len(fr) != 1 else '')
        tiles.append((str(len(fr)), lbl + (' · ' + fmt_cr(tot) if tot > 0 else '')))

    # 3. companies in the news / watchlist hook
    allc = set()
    for r, _ in day_items: allc.update(companies(r))
    if allc:
        hit = len(allc & set(tracked))
        tiles.append((str(len(allc)), 'companies' + (' · %d you track' % hit if hit else '')))
    return tiles


def render(day, items, tracked=()):
    dt = datetime.date(*map(int, day.split('-')))
    nice = dt.strftime('%a, %d %b')
    thin = len(items) < 5
    W = 66
    L = ['─' * W, 'TODAY\'S EDITION · 7:00 AM'.ljust(W - len(nice)) + nice, '─' * W]

    if not thin:
        tiles = build_tiles(items, tracked)
        if tiles:
            cw = W // max(len(tiles), 1)
            L.append(''.join(v.ljust(cw) for v, _ in tiles).rstrip())
            L.append(''.join(clip(l, cw - 2).ljust(cw) for _, l in tiles).rstrip())
            L.append('─' * W)

    shown = items if thin else items[:3]
    rows = 0
    for rec, summ in shown:
        eye = EYEBROW.get(rec['development_tag'], 'NEWS')
        who = (companies(rec) or [None])[0]
        L.append(eye + (' · ' + who if who else ''))
        L.append(clip(html.unescape(rec['article_title']), W - 2))
        line, src = pick_line(html.unescape(rec['article_title']), summ)
        if line: L.append('  ↳ ' + clip(line, W - 6))
        L.append('')
        rows += 1

    rest = len(items) - rows
    mins = max(1, round(len(items) * 0.30))
    foot = ('+ %d more · ~%d MIN' % (rest, mins)) if rest > 0 else 'That\'s all for today'
    L.append(foot.ljust(W - 22) + '[ OPEN TODAY\'S BRIEF ]')
    L.append('─' * W)
    return '\n'.join(L), thin


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.expanduser('~/Downloads/42_posts (1).csv')
    summ_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, 'summaries.json')
    recs = list(csv.DictReader(open(csv_path)))
    summ = json.load(open(summ_path))

    byday = defaultdict(list)
    for r in recs:
        d = r['published_date'][:10]
        if d: byday[d].append((r, (summ.get(r['ID']) or {}).get('bullets') or []))
    for d in byday:  # newest first within the day
        byday[d].sort(key=lambda x: x[0]['published_date'], reverse=True)

    TRACKED = {'Navi', 'Swiggy', 'Zepto', 'Groww', 'Meesho'}  # stand-in watchlist
    days = sorted(byday)
    out, audit = [], []
    for d in days:
        card, thin = render(d, byday[d], TRACKED)
        out.append(card)
        items = byday[d]
        tiles = [] if thin else build_tiles(items, TRACKED)
        srcs = [pick_line(html.unescape(r['article_title']), s)[1]
                for r, s in (items if thin else items[:3])]
        audit.append({
            'day': d, 'weekday': datetime.date(*map(int, d.split('-'))).strftime('%a'),
            'stories': len(items), 'thin_state': thin, 'tiles': len(tiles),
            'tile_text': ' | '.join('%s %s' % t for t in tiles),
            'rows_with_line': sum(1 for s in srcs if s not in ('none', 'all-duplicate')),
            'rows': len(srcs), 'line_sources': ','.join(srcs),
        })

    open(os.path.join(base, 'cards.txt'), 'w').write('\n\n'.join(out))
    with open(os.path.join(base, 'backtest.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(audit[0].keys())); w.writeheader(); w.writerows(audit)
    return audit, byday, summ


if __name__ == '__main__':
    audit, byday, summ = main()
    print('rendered %d days -> cards.txt, backtest.csv' % len(audit))

#!/usr/bin/env python3
"""Rebuild sitemap.xml: every indexable page, nothing that redirects, is noindex,
or has its canonical pointing elsewhere.

lastmod policy: a page keeps the date already in the sitemap unless it is listed
with --changed (real content edits). Template-wide edits (menu, header, footer)
should NOT bump every page's date, or Google learns to ignore our lastmod.

    python3 _build/rebuild-sitemap.py --changed / /truck-driver-health-insurance ...
    python3 _build/rebuild-sitemap.py --changed-file changed.txt
"""
import datetime, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
BASE = 'https://www.vshealthbenefits.com'
TODAY = datetime.date.today().isoformat()
SKIP_DIRS = {'_to_delete', 'node_modules', '.seo-work', '_build', 'ghl', 'ghl-email-templates', 'google-ads',
             'contractor-outreach', 'Claude outputs', 'restaurant-list', '.git', 'api', 'data'}
SKIP_FILES = {'admin.html', 'census.html', 'client.html', '404.html', 'book.html'}
PRIO = {
 '/': '1.0', '/truck-driver-health-insurance': '0.9', '/best-health-insurance-owner-operators': '0.9',
 '/small-business-health-insurance': '0.9', '/quote': '0.9', '/group-health-insurance-by-industry': '0.9',
 '/florida-small-business-health-insurance': '0.9', '/small-business-health-insurance-calculator': '0.9',
 '/group-health-eligibility-checker': '0.9', '/employer-health-insurance-cost-calculator': '0.9',
 '/texas-small-business-health-insurance': '0.9', '/maryland-small-business-health-insurance': '0.9',
 '/kentucky-small-business-health-insurance': '0.9', '/cobra-alternatives': '0.9',
 '/truck-driver-health-insurance-cost-calculator': '0.9', '/private-health-insurance': '0.9',
 '/self-employed-health-insurance': '0.9', '/ppo-health-insurance': '0.9',
 '/blog/aca-open-enrollment-2027-guide': '0.9', '/open-enrollment': '0.9', '/aca-subsidy-calculator': '0.9',
}

changed = set()
args = sys.argv[1:]
i = 0
while i < len(args):
    if args[i] == '--changed':
        i += 1
        while i < len(args) and not args[i].startswith('--'):
            changed.add(args[i].rstrip('/') or '/'); i += 1
    elif args[i] == '--changed-file':
        changed |= {l.strip().rstrip('/') or '/' for l in open(args[i + 1]) if l.strip()}; i += 2
    else:
        i += 1

red = set()
for r in json.load(open('vercel.json')).get('redirects', []):
    src = r.get('source', '')
    if src and not re.search(r'[:*(]', src):
        red.add(src.rstrip('/') or '/')
old = open('sitemap.xml', encoding='utf-8').read() if os.path.exists('sitemap.xml') else ''
oldmod = {m.group(1): m.group(2) for m in re.finditer(r'<loc>(.*?)</loc><lastmod>(.*?)</lastmod>', old)}

rows, why_out = [], {}
for dp, dns, fns in os.walk('.'):
    dns[:] = sorted(d for d in dns if d not in SKIP_DIRS and not d.startswith('.'))
    for fn in sorted(fns):
        if not fn.endswith('.html') or fn in SKIP_FILES:
            continue
        rel = os.path.normpath(os.path.join(dp, fn)).replace(os.sep, '/')
        slug = '/' + rel[:-5]
        if slug.endswith('/index'): slug = slug[:-6] or '/'
        if slug == '/index': slug = '/'
        s = open(rel, encoding='utf-8', errors='ignore').read()
        reason = None
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', s, re.I): reason = 'noindex'
        elif slug in red: reason = 'redirected'
        else:
            c = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', s, re.I)
            if c:
                cp = re.sub(r'^https?://[^/]+', '', c.group(1)).split('?')[0].split('#')[0].rstrip('/') or '/'
                if cp.endswith('.html'): cp = cp[:-5]
                if cp != slug: reason = 'canonical elsewhere (%s)' % cp
        if reason:
            why_out[slug] = reason
            continue
        loc = BASE + (slug if slug != '/' else '/')
        if slug in changed:
            lm = TODAY
        elif loc in oldmod:
            lm = oldmod[loc]
        else:
            lm = datetime.date.fromtimestamp(os.path.getmtime(rel)).isoformat()
        rows.append((loc, lm, PRIO.get(slug, '0.8')))

rows.sort(key=lambda r: (r[0] != BASE + '/', r[0]))
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
out += ['<url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>' % r for r in rows]
out.append('</urlset>')
open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(out) + '\n')

new_locs = {r[0] for r in rows}
added = sorted(new_locs - set(oldmod)); removed = sorted(set(oldmod) - new_locs)
print('sitemap: %d -> %d URLs; dated today: %d' % (len(oldmod), len(rows), sum(1 for r in rows if r[1] == TODAY)))
for a in added: print('  + added   ', a)
for r in removed: print('  - removed ', r, '(' + why_out.get(r.replace(BASE, '') or '/', 'file missing') + ')')
missing = [c for c in changed if BASE + c not in new_locs]
if missing: print('  ! --changed pages not in sitemap:', missing)

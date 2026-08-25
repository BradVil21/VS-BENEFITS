# -*- coding: utf-8 -*-
"""Rebuild sitemap.xml from the filesystem: every indexable page, no redirect sources."""
import re, glob, json, os, datetime, subprocess

BASE = 'https://www.vshealthbenefits.com'
red  = {r['source'] for r in json.load(open('vercel.json'))['redirects']}
old  = open('sitemap.xml', encoding='utf-8').read()
oldmod = {m.group(1): m.group(2) for m in
          re.finditer(r'<loc>(.*?)</loc><lastmod>(.*?)</lastmod>', old)}

SKIP = ('admin', 'census', 'client', '404', 'book')
PRIO = {
 '/': '1.0',
 '/blog/aca-open-enrollment-2027-guide': '0.9', '/health-insurance-open-enrollment-faq': '0.9',
 '/open-enrollment': '0.9', '/truck-driver-health-insurance': '0.9',
 '/best-health-insurance-owner-operators': '0.9', '/aca-subsidy-calculator': '0.9',
 '/small-business-health-insurance': '0.9', '/quote': '0.9',
}

rows = []
for f in sorted(glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('guides/*.html')):
    slug = '/' + f[:-5]
    if slug == '/index': slug = '/'
    if any(x in f for x in SKIP): continue
    s = open(f, encoding='utf-8').read()
    if re.search(r'<meta name="robots"[^>]*noindex', s): continue
    if slug in red or slug + '.html' in red and slug in red: continue
    if slug in red: continue                       # page is a redirect source
    canon = re.search(r'rel="canonical" href="(.*?)"', s)
    if canon and canon.group(1).rstrip('/') not in (BASE + slug).rstrip('/'):
        # canonical points elsewhere -> don't list this URL
        if canon.group(1).rstrip('/') != (BASE + slug).rstrip('/'):
            continue
    loc = BASE + slug
    mtime = datetime.date.fromtimestamp(os.path.getmtime(f)).isoformat()
    prev  = oldmod.get(loc)
    lastmod = mtime if (not prev or mtime > prev) else prev
    rows.append((loc, lastmod, PRIO.get(slug, '0.8')))

rows.sort(key=lambda r: r[0])
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, lm, p in rows:
    out.append('<url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>' % (loc, lm, p))
out.append('</urlset>')
open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('sitemap: %d -> %d URLs' % (len(oldmod), len(rows)))
for k in ['/health-insurance-open-enrollment-faq','/blog/how-much-does-health-insurance-cost-2026','/get-a-quote','/truckers-health-insurance']:
    print('  %-46s %s' % (k, 'IN' if any(r[0]==BASE+k for r in rows) else 'out'))

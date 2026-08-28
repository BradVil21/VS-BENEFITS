# -*- coding: utf-8 -*-
"""Install the GoHighLevel External Tracking script site-wide.

Snippet taken from GHL -> Settings -> External Tracking -> Installation for
location cNCy6JUURpb4eBDdb9bU. GHL wants it immediately before </body>.

This is what lets GHL attribute sessions, sources and page paths to contacts,
so a lead in the CRM shows which pages they read before they converted.
It sits alongside GA4 rather than replacing it.
"""
import glob, re

SNIPPET = ('<!-- GoHighLevel external tracking -->\n'
           '<script src="https://link.msgsndr.com/js/external-tracking.js" '
           'data-tracking-id="tk_e89392b2cfc34b548ae43b1ea975ae50"></script>\n')

MARK = 'link.msgsndr.com/js/external-tracking.js'
# app-ish pages that are not public marketing surfaces
SKIP = {'admin.html', 'client.html'}

files = sorted(glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('guides/*.html'))
added = already = noBody = 0
for f in files:
    if f in SKIP:
        continue
    s = open(f, encoding='utf-8').read()
    if MARK in s:
        already += 1
        continue
    i = s.rfind('</body>')
    if i < 0:
        noBody += 1
        continue
    open(f, 'w', encoding='utf-8').write(s[:i] + SNIPPET + s[i:])
    added += 1

print('GHL tracking added to %d pages (%d already had it, %d had no </body>, %d skipped)'
      % (added, already, noBody, len(SKIP)))

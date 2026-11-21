# -*- coding: utf-8 -*-
"""Add from=<page path> to every /quote link that has no from= (2026-11-21),
so each lead in the admin portal shows which page sent it."""
import re, os, glob, sys
SKIP = re.compile(r'^(\.seo-work|_to_delete|\.git|node_modules|quote/|Claude outputs)|^(admin|creator)')
pat = re.compile(r'href="/quote(\?[^"#]*)?"')
changed = 0; links = 0
for f in sorted(glob.glob("**/*.html", recursive=True)):
    if SKIP.search(f): continue
    page = f[:-5]
    if page == "index": page = "home"
    elif page.endswith("/index"): page = page[:-6]
    s = open(f, encoding="utf-8").read()
    def fix(m):
        global links
        q = m.group(1) or ""
        if "from=" in q: return m.group(0)
        links += 1
        if not q: return 'href="/quote?from=%s"' % page
        sep = "&amp;" if "&amp;" in q or "&" not in q else "&"
        return 'href="/quote%s%sfrom=%s"' % (q, sep if q != "?" else "", page)
    s2 = pat.sub(fix, s)
    if s2 != s:
        open(f, "w", encoding="utf-8").write(s2); changed += 1
print("files", changed, "links", links)

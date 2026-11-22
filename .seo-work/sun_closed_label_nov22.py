# -*- coding: utf-8 -*-
"""Show 'Sun closed' wherever Saturday hours are listed (2026-11-22)."""
import glob, re
SKIP = re.compile(r'^(\.seo-work|_to_delete|\.git|node_modules|google-ads|ghl)/')
EN = re.compile(r'(Sat(?:urday)?\s+10(?:\s?)am(?:\s*(?:-|–|&ndash;|to)\s*)5(?:\s?)pm(?: ET| Eastern)?)(?![^<>"\n]{0,25}(?:[Cc]losed|Sun))')
ES = re.compile(r'((?:sáb|Sáb|sábado)\s+10am(?:\s*(?:-|–|&ndash;|a)\s*)5pm(?: ET)?)(?![^<>"\n]{0,25}(?:cerrado|dom))')
nf = tot = 0
for f in glob.glob("**/*", recursive=True):
    if not re.search(r'\.(html|js|txt)$', f) or SKIP.search(f): continue
    try: s = open(f, encoding="utf-8").read()
    except Exception: continue
    o = s
    s, a = EN.subn(lambda m: m.group(1) + ", Sun closed", s)
    s, b = ES.subn(lambda m: m.group(1) + ", dom cerrado", s)
    if s != o: open(f, "w", encoding="utf-8").write(s); nf += 1; tot += a + b
print("files", nf, "labels added", tot)

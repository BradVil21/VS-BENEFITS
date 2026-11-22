# -*- coding: utf-8 -*-
"""Closed Sundays (2026-11-22): hours become Mon-Fri 8-6, Sat 8-1 ET everywhere."""
import glob, re
SKIP = re.compile(r'^(\.seo-work|_to_delete|\.git|node_modules|google-ads|ghl)/')
REPL = [
 ('"dayOfWeek":["Saturday","Sunday"]', '"dayOfWeek":["Saturday"]'),
 ('"dayOfWeek": ["Saturday", "Sunday"]', '"dayOfWeek": ["Saturday"]'),
 ('"dayOfWeek": ["Saturday","Sunday"]', '"dayOfWeek": ["Saturday"]'),
 ('Sat-Sun 8am-1pm', 'Sat 8am-1pm'),
 ('Sat–Sun 8am–1pm', 'Sat 8am–1pm'),
 ('Sat to Sun 8am to 1pm', 'Sat 8am to 1pm'),
 ('Sat-Sun 8-1', 'Sat 8-1'),
 ('Saturday and Sunday 8am to 1pm', 'Saturday 8am to 1pm'),
]
files = [f for f in glob.glob("**/*", recursive=True) if re.search(r'\.(html|js|txt|json)$', f) and not SKIP.search(f)]
tot = 0; nf = 0
for f in files:
    try: s = open(f, encoding="utf-8").read()
    except Exception: continue
    o = s
    for a, b in REPL: s = s.replace(a, b)
    if s != o:
        open(f, "w", encoding="utf-8").write(s); nf += 1; tot += sum(o.count(a) for a, _ in REPL)
print("files", nf, "replacements", tot)

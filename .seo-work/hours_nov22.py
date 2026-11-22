# -*- coding: utf-8 -*-
"""Hours (2026-11-22, from the Google Business Profile): Mon-Fri 8am-8pm, Sat 1pm-5pm ET, Sun closed."""
import glob, re, sys
SKIP = re.compile(r'^(\.seo-work|_to_delete|\.git|node_modules|google-ads|ghl)/')
SEP = r'(\s*(?:-|–|&ndash;|to|a)\s*)'
RX = [
 # weekdays: 8am-6pm -> 8am-8pm
 (re.compile(r'8(\s?)am' + SEP + r'6(\s?)pm'), lambda m: '8%sam%s8%spm' % (m.group(1), m.group(2), m.group(3))),
 (re.compile(r'8:00am' + SEP + r'6:00pm'), lambda m: '8:00am%s8:00pm' % m.group(1)),
 # saturday (and old weekend wording): 8am-1pm -> 1pm-5pm, drop Sunday
 (re.compile(r'\b(Sat(?:urday)?|sáb(?:ado)?|weekends)(?:\s*(?:-|–|&ndash;|and|y)\s*(?:Sun(?:day)?|dom(?:ingo)?))?(,?\s*(?:from\s+)?)8(\s?)am' + SEP + r'1(\s?)pm'),
  lambda m: '%s%s1%spm%s5%spm' % ({'weekends': 'Sat'}.get(m.group(1), m.group(1)), m.group(2), m.group(3), m.group(4), m.group(5))),
 (re.compile(r'8:00am' + SEP + r'1:00pm'), lambda m: '1:00pm%s5:00pm' % m.group(1)),
 # schema
 (re.compile(r'("dayOfWeek":\s?\["Monday",\s?"Tuesday",\s?"Wednesday",\s?"Thursday",\s?"Friday"\],\s?"opens":\s?"08:00",\s?"closes":\s?)"18:00"'), lambda m: m.group(1) + '"20:00"'),
 (re.compile(r'("dayOfWeek":\s?\["Saturday"\],\s?"opens":\s?)"08:00"(,\s?"closes":\s?)"13:00"'), lambda m: m.group(1) + '"13:00"' + m.group(2) + '"17:00"'),
 # code comments / short forms
 (re.compile(r'Mon-Fri 8-6, Sat 8-1'), lambda m: 'Mon-Fri 8-8, Sat 1-5'),
]
files = [f for f in glob.glob("**/*", recursive=True) if re.search(r'\.(html|js|txt|json)$', f) and not SKIP.search(f)]
files += [".seo-work/gen_sunday_blog.py"]
nf = tot = 0
for f in files:
    try: s = open(f, encoding="utf-8").read()
    except Exception: continue
    o = s
    for rx, fn in RX:
        s, n = rx.subn(fn, s); tot += n
    if s != o:
        open(f, "w", encoding="utf-8").write(s); nf += 1
print("files", nf, "replacements", tot)

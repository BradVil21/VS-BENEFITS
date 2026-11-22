# -*- coding: utf-8 -*-
"""Saturday hours are 10am-5pm ET (owner, 2026-11-22). Was set to 1pm-5pm earlier today."""
import glob, re
SKIP = re.compile(r'^(\.seo-work|_to_delete|\.git|node_modules|google-ads|ghl)/')
SEP = r'(\s*(?:-|–|&ndash;|to|a)\s*)'
RX = [
 (re.compile(r'\b1(\s?)pm' + SEP + r'5(\s?)pm'), lambda m: '10%sam%s5%spm' % (m.group(1), m.group(2), m.group(3))),
 (re.compile(r'1:00pm' + SEP + r'5:00pm'), lambda m: '10:00am%s5:00pm' % m.group(1)),
 (re.compile(r'("dayOfWeek":\s?\["Saturday"\],\s?"opens":\s?)"13:00"(,\s?"closes":\s?"17:00")'), lambda m: m.group(1) + '"10:00"' + m.group(2)),
 (re.compile(r'Mon-Fri 8-8, Sat 1-5'), lambda m: 'Mon-Fri 8-8, Sat 10-5'),
]
files = [f for f in glob.glob("**/*", recursive=True) if re.search(r'\.(html|js|txt|json)$', f) and not SKIP.search(f)] + [".seo-work/gen_sunday_blog.py"]
nf = tot = 0
for f in files:
    try: s = open(f, encoding="utf-8").read()
    except Exception: continue
    o = s
    for rx, fn in RX:
        s, n = rx.subn(fn, s); tot += n
    if s != o: open(f, "w", encoding="utf-8").write(s); nf += 1
print("files", nf, "replacements", tot)

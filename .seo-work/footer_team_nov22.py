# -*- coding: utf-8 -*-
"""Meet the Team link in every page footer (2026-11-22)."""
import re
files = [l.strip() for l in open("/tmp/miss.txt") if l.strip()]
done = []
def foot(s):
    i = s.rfind("<footer"); j = s.find("</footer>", i); return i, j
for f in files:
    s = open(f, encoding="utf-8").read(); i, j = foot(s); t = s[i:j]; o = t
    es = "/lp/es/" in "/" + f
    lbl = "Nuestro equipo" if es else "Meet the Team"
    link = '<a href="/meet-the-team">%s</a>' % lbl
    if '<li><a href="/about">About</a></li>' in t:                       # full site footer
        t = t.replace('<li><a href="/about">About</a></li>', '<li><a href="/about">About</a></li><li>%s</li>' % link, 1)
    elif re.search(r'<a href="/about">(About us|Nosotros)</a>', t):     # landing-page footers
        t = re.sub(r'(<a href="/about">(?:About us|Nosotros)</a>)', r'\1' + link, t, count=1)
    elif '<a href="/contact">Contact Us</a>' in t:                       # quote / funnel footers
        t = t.replace('<a href="/contact">Contact Us</a>', '<a href="/contact">Contact Us</a> ' + link, 1)
    elif '<a href="/contact">Contact</a></p>' in t:                       # creator portal
        t = t.replace('<a href="/contact">Contact</a></p>', '<a href="/contact">Contact</a> &middot; %s</p>' % link, 1)
    if t != o:
        s = s[:i] + t + s[j:]; open(f, "w", encoding="utf-8").write(s); done.append(f)
    else:
        print("NOT CHANGED", f)
print("updated", len(done), "of", len(files))

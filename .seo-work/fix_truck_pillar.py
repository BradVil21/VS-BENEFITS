# -*- coding: utf-8 -*-
"""/truck-driver-health-insurance ranks ~49 for "health insurance for truck
drivers" (1,204 impressions) while a blog post ranks 29 and the owner-operator
page ranks 20. The head term is informational and this page led with sales.

Three fixes, no content deleted:
  1. H1 carries the query phrase instead of a price claim.
  2. Five links that promised other pages pointed back at this page.
  3. Section order: answer first, sell after.
"""
import re

F = 'truck-driver-health-insurance.html'
s = open(F, encoding='utf-8').read()
orig = s

# ---- 1. H1 ---------------------------------------------------------------
OLD_H1 = '<h1>Truck Driver Health Insurance, <span>From $0/mo After Tax Credits</span></h1>'
NEW_H1 = '<h1>Health Insurance for Truck Drivers <span>and Owner-Operators</span></h1>'
assert OLD_H1 in s, 'H1 not found'
s = s.replace(OLD_H1, NEW_H1, 1)

# ---- 2. self-links that promised other pages -----------------------------
FIX = [
    ('<a href="/truck-driver-health-insurance">OTR truck driver health insurance guide</a>',
     '<a href="/otr-truck-driver-health-insurance">OTR truck driver health insurance guide</a>'),
    ('<a href="/truck-driver-health-insurance">truck driver family health insurance page</a>',
     '<a href="/truck-driver-family-health-insurance">truck driver family health insurance page</a>'),
]
for old, new in FIX:
    assert old in s, old[:60]
    s = s.replace(old, new, 1)

CARDS = [('OTR and Long-Haul Drivers', '/otr-truck-driver-health-insurance'),
         ('Coverage for Your Family', '/truck-driver-family-health-insurance'),
         ('All Guides and Tools', '/truck-driver-health-insurance-resources')]
for label, dest in CARDS:
    pat = re.compile(r'(<a class="hub-card" href=")/truck-driver-health-insurance("[^>]*>\s*<strong>'
                     + re.escape(label) + r'</strong>)')
    s, n = pat.subn(lambda m: m.group(1) + dest + m.group(2), s, count=1)
    assert n == 1, 'hub card not rewired: ' + label

# ---- 3. reorder top-level sections ---------------------------------------
def top_sections(html):
    """(start, end_of_unit) for each top-level <section>; a unit carries the
    markup that follows it up to the next top-level section."""
    spans, depth, start = [], 0, None
    for m in re.finditer(r'<section\b[^>]*>|</section>', html):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                spans.append((start, m.end()))
        else:
            if depth == 0:
                start = m.start()
            depth += 1
    units = []
    for i, (a, b) in enumerate(spans):
        end = spans[i + 1][0] if i + 1 < len(spans) else b
        units.append((a, end))
    return units

units = top_sections(s)
assert len(units) == 19, 'expected 19 sections, found %d' % len(units)
head = s[:units[0][0]]
tail = s[units[-1][1]:]
blocks = [s[a:b] for a, b in units]

# informational first, conversion after, related blocks last (unchanged tail)
ORDER = [0, 1, 2, 3, 12, 8, 9, 6, 4, 5, 7, 10, 11, 13, 14, 15, 16, 17, 18]
assert sorted(ORDER) == list(range(19))
s = head + ''.join(blocks[i] for i in ORDER) + tail

assert len(s) - len(orig) < 200, 'unexpected size change'
open(F, 'w', encoding='utf-8').write(s)
print('pillar rewritten:', len(orig), '->', len(s), 'bytes')
print('self-links remaining:', len(re.findall(r'href="/truck-driver-health-insurance"', s)))

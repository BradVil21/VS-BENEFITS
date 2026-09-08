# -*- coding: utf-8 -*-
"""Correct the open enrollment end date sitewide.

Open Enrollment for 2027 coverage runs 1 Nov 2026 - 15 Jan 2027 on
HealthCare.gov. 15 December is the deadline for a 1 January start, not the end
of the window. 53 pages said the window itself closes 15 December, including
the homepage FAQ schema, two meta descriptions and the countdown widget - which
would have told every visitor from 16 December that enrollment was over while a
month of it remained.

The countdown is rebuilt with both deadlines rather than one, so it now creates
the 15 December urgency AND keeps working through 15 January.
"""
import glob, re, sys

DEC15 = '"2026-12-15T23:59:59-05:00"'
JAN15 = '"2027-01-15T23:59:59-05:00"'

changed = {}
def note(f, what):
    changed.setdefault(f, []).append(what)

files = sorted(glob.glob("*.html") + glob.glob("blog/*.html"))

# --- 1. countdown constants: END becomes Jan 15, DEC15 is added --------------
const_re = re.compile(r'var\s+END(\s*)=(\s*)new Date\(' + re.escape(DEC15) + r'\)\.getTime\(\);')
def const_sub(m):
    sp1, sp2 = m.group(1), m.group(2)
    return ('var DEC15%s=%snew Date(%s).getTime();'
            'var END%s=%snew Date(%s).getTime();' % (sp1, sp2, DEC15, sp1, sp2, JAN15))

# --- 2. the single "<=END" branch becomes two branches -----------------------
branch_re = re.compile(
    r'else\s*if\s*\(\s*now\s*<=\s*END\s*\)\s*\{\s*'
    r'paint\(\s*END\s*,\s*"(?P<title>[^"]*)"\s*,\s*"(?P<sub>[^"]*)"\s*\)\s*;\s*'
    r'if\s*\(\s*elWrap\s*\)\s*elWrap\.classList\.remove\("closed"\)\s*;\s*\}', re.S)

def branch_sub(m):
    title = m.group("title")
    return ('else if(now<=DEC15){'
            'paint(DEC15,"%s",'
            '"Enroll by Dec 15, 2026 for coverage that starts Jan 1, 2027. Open Enrollment then runs through Jan 15.");'
            'if(elWrap)elWrap.classList.remove("closed");}'
            'else if(now<=END){'
            'paint(END,"Last chance to enroll for 2027 coverage",'
            '"Open Enrollment closes Jan 15, 2027. A plan bought now starts Feb 1. After Jan 15 you need a qualifying life event.");'
            'if(elWrap)elWrap.classList.remove("closed");}' % title)

# --- 3. prose and metadata ---------------------------------------------------
PROSE = [
 # homepage FAQ schema
 ('Open Enrollment runs Nov 1 - Dec 15 each year.',
  'Open Enrollment runs Nov 1 through Jan 15. Enroll by Dec 15 for coverage starting Jan 1.'),
 # /health-insurance meta, og and twitter descriptions
 ('Open Enrollment runs Nov 1 to Dec 15 - see your after-subsidy price.',
  'Open Enrollment runs Nov 1 to Jan 15 - see your after-subsidy price.'),
 # blog index cards
 ('Enrollment runs Nov 1&ndash;Dec 15, 2026.',
  'Enrollment runs Nov 1, 2026 &ndash; Jan 15, 2027.'),
 ('Open Enrollment runs Nov 1 to Dec 15, 2026. Miss it and you&#39;ll wait until 2028.',
  'Open Enrollment runs Nov 1, 2026 to Jan 15, 2027. Miss it and you&#39;ll wait until 2028.'),
 ("Open Enrollment runs Nov 1 to Dec 15, 2026. Miss it and you'll wait until 2028.",
  "Open Enrollment runs Nov 1, 2026 to Jan 15, 2027. Miss it and you'll wait until 2028."),
 # the income/premium post: title tag, meta, og, twitter and schema all share this
 ('Open Enrollment for 2027 runs Nov 1 to Dec 15, 2026.',
  'Open Enrollment for 2027 runs Nov 1, 2026 to Jan 15, 2027.'),
 ('Open Enrollment for 2027 runs Nov 1 to Dec 15, 2026',
  'Open Enrollment for 2027 runs Nov 1, 2026 to Jan 15, 2027'),
 # generic prose forms
 ('Open Enrollment runs Nov 1 &ndash; Dec 15', 'Open Enrollment runs Nov 1 &ndash; Jan 15'),
 ('Open Enrollment runs Nov 1 - Dec 15', 'Open Enrollment runs Nov 1 - Jan 15'),
 ('open enrollment runs Nov 1 to Dec 15', 'open enrollment runs Nov 1 to Jan 15'),
 ('Open Enrollment runs Nov 1 to Dec 15', 'Open Enrollment runs Nov 1 to Jan 15'),
 ('Enrollment runs Nov 1 to Dec 15', 'Enrollment runs Nov 1 to Jan 15'),
]

for f in files:
    src = open(f, encoding="utf-8").read()
    out = src

    n = len(const_re.findall(out))
    if n:
        out = const_re.sub(const_sub, out)
        note(f, "countdown END -> Jan 15 (%d)" % n)

    n = len(branch_re.findall(out))
    if n:
        out = branch_re.sub(branch_sub, out)
        note(f, "countdown split into Dec 15 + Jan 15 phases (%d)" % n)

    for a, b in PROSE:
        if a in out:
            c = out.count(a)
            out = out.replace(a, b)
            note(f, "prose x%d: %s" % (c, a[:52]))

    if out != src:
        open(f, "w", encoding="utf-8").write(out)

print("FILES CHANGED: %d\n" % len(changed))
for f in sorted(changed):
    print(f)
    for w in changed[f]:
        print("   -", w)

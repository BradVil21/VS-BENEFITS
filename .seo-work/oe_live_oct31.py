# -*- coding: utf-8 -*-
"""2026-10-31: Open Enrollment goes live Nov 1.
- Top bar: 'Open Enrollment is now open. You have until January 15 ...' (static text + vs-oe-bar.js oe phase).
- Countdowns: from Nov 1 count down to the end of Open Enrollment (Jan 15), not to Dec 15.
- START anchors fixed to midnight EDT (-04:00); Nov 1 2026 is still daylight time at midnight."""
import re, glob
EX = ('_to_delete','compressed','_build','Claude outputs','.seo-work','node_modules','google-ads','ghl','contractor-outreach','restaurant-list')
files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith(EX)]
st = dict(bar=0, script=0, cd=0, cd5=0, start=0)
EN = 'Open Enrollment is now open. You have until January 15 to get better coverage. Enroll by Dec 15 for a January 1 start.'
STATIC = [
 ('Open Enrollment for 2027 coverage runs Nov 1 &ndash; Jan 15. Enroll by Dec 15 for a January 1 start.', EN),
 ('Open Enrollment for 2027 coverage runs Nov 1 &ndash; Jan 15. Get ahead of the deadline.', EN),
 ('Drivers: Open Enrollment for 2027 runs Nov 1 &ndash; Jan 15. Enroll from the road by Dec 15 for Jan 1 coverage.',
  'Drivers: Open Enrollment is now open. You have until January 15 to get better coverage. Enroll from the road by Dec 15 for Jan 1.'),
 ('Inscripción abierta 2027: del 1 de noviembre al 15 de enero. Inscríbase antes del 15 de diciembre para cobertura el 1 de enero.',
  'La inscripción abierta ya comenzó. Tiene hasta el 15 de enero para conseguir una mejor cobertura. Inscríbase antes del 15 de diciembre para cobertura el 1 de enero.'),
]
NEW_OE = '{paint(END,"Open Enrollment is now open. Time left to enroll:","You have until January 15, 2027 to get better coverage. Enroll by Dec 15 for coverage that starts January 1.");if(elWrap)elWrap.classList.remove("closed");}'
for f in files:
    s0 = s = open(f, encoding='utf-8').read()
    for a, b in STATIC:
        if a in s: s = s.replace(a, b); st['bar'] += 1
    # add the date-aware bar script where the static bar has none
    if 'id="oe-annc-bar"' in s and 'vs-oe-bar.js' not in s:
        s = re.sub(r'(<div id="oe-annc-bar".*?</div>)', r'\1<script src="/vs-oe-bar.js" defer></script>', s, count=1, flags=re.S); st['script'] += 1
    # countdown: Nov 1 - Dec 15 branch now counts to END
    s, n = re.subn(r'\{paint\(DEC15,"Time left to enroll in 2027 ACA coverage","Enroll by Dec 15, 2026 for coverage that starts Jan 1, 2027\. Open Enrollment then runs through Jan 15\."\);if\(elWrap\)elWrap\.classList\.remove\("closed"\);\}', NEW_OE, s); st['cd'] += n
    # older variant (blog/about/...): wrong 'closes Dec 15' text and hides as closed during OE
    s, n = re.subn(r'paint\(END,"Time left to enroll in 2027 ACA coverage",\s*"Open Enrollment closes Dec 15, 2026\. After that you will need a Special Enrollment event to switch plans\."\);\s*if\(elWrap\)elWrap\.classList\.add\("closed"\);',
                   'paint(END,"Open Enrollment is now open. Time left to enroll:","You have until January 15, 2027 to get better coverage. Enroll by Dec 15 for coverage that starts January 1.");if(elWrap)elWrap.classList.remove("closed");', s); st['cd5'] += n
    s, n = re.subn(r'(START\s*=\s*new Date\(")2026-11-01T00:00:00-05:00', r'\g<1>2026-11-01T00:00:00-04:00', s); st['start'] += n
    if s != s0: open(f, 'w', encoding='utf-8').write(s)

# open-enrollment.html countdown
f = 'open-enrollment.html'; s = open(f, encoding='utf-8').read()
old = """paint(DEC15,'Time Left for January 1 Coverage',
              'Enroll by Dec 15 to start Jan 1. Open Enrollment then runs through Jan 15.');"""
if old in s:
    s = s.replace(old, """paint(END,'Open Enrollment Is Now Open: Time Left to Enroll',
              'You have until January 15, 2027 to get better coverage. Enroll by Dec 15 to start January 1.');"""); st['oe_page'] = 1
    open(f, 'w', encoding='utf-8').write(s)

# app.js
f = 'app.js'; s = open(f, encoding='utf-8').read()
s2 = s.replace('var START = new Date("2026-11-01T00:00:00-05:00")', 'var START = new Date("2026-11-01T00:00:00-04:00")')
s2 = s2.replace('''      paint(END,
            "Time left to enroll in 2027 ACA coverage",
            "Open Enrollment closes Jan 15, 2027. After that you will need a Special Enrollment event to switch plans.");
      if (elWrap) elWrap.classList.add("closed");''', '''      paint(END,
            "Open Enrollment is now open. Time left to enroll:",
            "You have until January 15, 2027 to get better coverage. Enroll by Dec 15 for coverage that starts January 1.");
      if (elWrap) elWrap.classList.remove("closed");''')
if s2 != s: open(f, 'w', encoding='utf-8').write(s2); st['appjs'] = 1
print(st)

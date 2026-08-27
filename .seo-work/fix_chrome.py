# -*- coding: utf-8 -*-
"""Three pre-existing chrome bugs found while verifying the state build.

A. 43 pages still say Open Enrollment ends "Dec 15". The Jan 15 correction
   (commit 83494b4) missed them.
B. 9 pages run the scroll-progress script but have no #vs-scroll-bar element,
   so every scroll event throws TypeError: Cannot read properties of null.
C. 5 content pages are missing the announcement bar entirely.
"""
import glob, re

FILES = sorted(glob.glob('*.html') + glob.glob('blog/*.html'))
SKIP_BANNER = {'admin.html', 'client.html', 'open-enrollment.html'}

BAR = ('<div id="oe-annc-bar" style="background:linear-gradient(135deg,#16447f,#0db5a6);color:#fff;'
       'text-align:center;padding:9px 16px;font-family:Inter,system-ui,-apple-system,sans-serif;'
       'font-size:.9rem;font-weight:600;line-height:1.35"><a href="/quote" style="color:#fff;'
       'text-decoration:none;display:inline-flex;gap:10px;align-items:center;justify-content:center;'
       'flex-wrap:wrap"><span>Open Enrollment for 2027 coverage runs Nov 1 &ndash; Jan 15. '
       'Get ahead of the deadline.</span><span style="background:#fff;color:#16447f;border-radius:999px;'
       'padding:3px 12px;font-weight:800;white-space:nowrap">Get a Free Quote &rarr;</span></a></div>')

a = b = c = 0
for f in FILES:
    s = open(f, encoding='utf-8').read()
    orig = s

    # A. wrong open enrollment end date in the banner
    s = s.replace('Open Enrollment for 2027 coverage runs Nov 1 &ndash; Dec 15',
                  'Open Enrollment for 2027 coverage runs Nov 1 &ndash; Jan 15')
    if s != orig:
        a += 1

    m = re.search(r'<body[^>]*>', s)
    if m:
        ins = m.end()
        # C. missing announcement bar
        if f not in SKIP_BANNER and 'id="oe-annc-bar"' not in s:
            s = s[:ins] + '\n' + BAR + s[ins:]
            c += 1
            m = re.search(r'<body[^>]*>', s)
            ins = m.end()
        # B. script targets #vs-scroll-bar but the element is absent
        if 'getElementById("vs-scroll-bar")' in s and 'id="vs-scroll-bar"></div>' not in s:
            anchor = s.find('id="oe-annc-bar"')
            if anchor > 0:
                end = s.index('</div>', anchor) + 6
            else:
                end = ins
            s = s[:end] + '\n\n<div id="vs-scroll-bar"></div>' + s[end:]
            b += 1

    if s != orig:
        open(f, 'w', encoding='utf-8').write(s)

print('A. open-enrollment end date corrected to Jan 15 on %d pages' % a)
print('B. missing #vs-scroll-bar element added to %d pages' % b)
print('C. announcement bar added to %d pages' % c)

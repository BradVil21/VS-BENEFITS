# -*- coding: utf-8 -*-
"""Add the ChamberofCommerce.com listing to the sameAs list in the organization
schema, so search engines tie the directory listing to this site's entity."""
import re, glob

URL = "https://www.chamberofcommerce.com/business-directory/florida/carol-city/health-insurance-agency/2034499618-vs-health-benefits"
TIKTOK = "https://www.tiktok.com/@vshealthbenefits"

changed = skipped = 0
for f in sorted(glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('quote/*.html')):
    s = open(f, encoding='utf-8').read()
    if URL in s:
        skipped += 1; continue
    if '"sameAs"' not in s or TIKTOK not in s:
        continue
    out, n = s, 0
    # spaced form
    out, k = re.subn(r'("' + re.escape(TIKTOK) + r'")(\s*\])',
                     lambda m: m.group(1) + ',\n    "' + URL + '"' + m.group(2), out)
    n += k
    # minified form
    if not n:
        out, k = re.subn(r'("' + re.escape(TIKTOK) + r'")(\])',
                         lambda m: m.group(1) + ',"' + URL + '"' + m.group(2), out)
        n += k
    if n:
        open(f, 'w', encoding='utf-8').write(out); changed += 1
print('sameAs updated on', changed, 'pages; already had it:', skipped)

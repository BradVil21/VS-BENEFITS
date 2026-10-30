# 2026-10-30: remove the Cigna logo from every carrier strip / quote page (Cigna leaves the ACA Marketplace for 2027).
import re, glob
EX = ('_to_delete','compressed','_build','Claude outputs','.seo-work','node_modules','google-ads','ghl','contractor-outreach','restaurant-list')
P = [r'[ \t]*<(div|span) class="carrier[^"]*" data-logo="[^"]*cigna\.png"[^>]*><span class="carrier-wm"[^>]*>[^<]*</span></\1>\n?',
     r'<(div|span) class="carrier[^"]*" data-logo="[^"]*cigna\.png"[^>]*>Cigna</\1>',
     r'<img src="/images/carriers/cigna\.png"[^>]*>']
tot = 0; files = 0
for f in glob.glob('**/*.html', recursive=True):
    if f.startswith(EX): continue
    s = open(f, encoding='utf-8').read(); n0 = 0
    for p in P:
        s, n = re.subn(p, '', s); n0 += n
    if n0:
        open(f, 'w', encoding='utf-8').write(s); tot += n0; files += 1
print('removed', tot, 'logos in', files, 'files')

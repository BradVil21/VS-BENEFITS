"""Insert the contact strip above the site header on every page that has one.
Usage: python3 add_topbar.py <file-or-list-file> [...]"""
import sys, re

BLOCK = ('<style id="vs-topbar-css">'
 '.vs-topbar{background:#0b2346;color:#fff;font-family:Inter,system-ui,-apple-system,sans-serif;font-size:.8rem;font-weight:600;line-height:1.2}'
 '.vs-topbar-in{max-width:1360px;margin:0 auto;padding:8px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px}'
 '.vs-topbar a{color:#fff;text-decoration:none;display:inline-flex;align-items:center;gap:6px;white-space:nowrap}'
 '.vs-topbar a:hover{text-decoration:underline;text-underline-offset:3px}'
 '.vs-tb-l{display:inline-flex;align-items:center;gap:6px;color:rgba(255,255,255,.9);white-space:nowrap}'
 '.vs-tb-r{display:flex;align-items:center;gap:22px}'
 '.vs-topbar svg{flex-shrink:0;color:#5eead4}'
 '@media(max-width:639px){.vs-topbar-in{padding:7px 14px;justify-content:center;gap:14px}.vs-tb-r{gap:14px}.vs-tb-mail span{display:none}}'
 '@media(max-width:359px){.vs-tb-l{display:none}}'
 '</style>'
 '<div class="vs-topbar"><div class="vs-topbar-in">'
 '<span class="vs-tb-l"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>Licensed in 40+ States</span>'
 '<span class="vs-tb-r">'
 '<a href="tel:+19548251009"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>(954) 825-1009</a>'
 '<a class="vs-tb-mail" href="mailto:info@vshealthbenefits.com" aria-label="Email info@vshealthbenefits.com"><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg><span>info@vshealthbenefits.com</span></a>'
 '</span></div></div>\n')

files = []
for a in sys.argv[1:]:
    if a.endswith('.txt'):
        files += [l.strip() for l in open(a) if l.strip()]
    else:
        files.append(a)
added = skipped = 0
for p in files:
    s = open(p, encoding='utf-8', errors='surrogateescape').read()
    if 'class="vs-topbar"' in s:
        skipped += 1; continue
    m = re.search(r'<header class="site-header"', s)
    if not m:
        continue
    s = s[:m.start()] + BLOCK + s[m.start():]
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
    added += 1
print('added', added, 'already', skipped)

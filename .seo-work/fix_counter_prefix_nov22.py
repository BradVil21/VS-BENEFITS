# -*- coding: utf-8 -*-
"""Count-up animation kept '$' after the number ('$0' -> '0$'). Keep leading symbols in front (2026-11-22)."""
import glob, re
SKIP = re.compile(r'^(\.seo-work|_to_delete|\.git|node_modules)/')
R = [
 ('var suffix = el.textContent.replace(/[0-9.,]/g,"");', 'var _ct = el.textContent; var prefix = (_ct.match(/^[^0-9]*/)||[""])[0]; var suffix = _ct.slice(prefix.length).replace(/[0-9.,]/g,"");'),
 ('var suffix=el.textContent.replace(/[0-9.,]/g,"");', 'var _ct=el.textContent;var prefix=(_ct.match(/^[^0-9]*/)||[""])[0];var suffix=_ct.slice(prefix.length).replace(/[0-9.,]/g,"");'),
 ('el.textContent = (isInt ? Math.round(val) : val.toFixed(1)) + suffix;', 'el.textContent = prefix + (isInt ? Math.round(val) : val.toFixed(1)) + suffix;'),
 ('el.textContent = (isInt ? target : target.toFixed(1)) + suffix;', 'el.textContent = prefix + (isInt ? target : target.toFixed(1)) + suffix;'),
 ('el.textContent=(isInt?Math.round(val):val.toFixed(1))+suffix;', 'el.textContent=prefix+(isInt?Math.round(val):val.toFixed(1))+suffix;'),
 ('el.textContent=(isInt?target:target.toFixed(1))+suffix;', 'el.textContent=prefix+(isInt?target:target.toFixed(1))+suffix;'),
]
nf = 0
for f in glob.glob("**/*.html", recursive=True) + glob.glob("*.js"):
    if SKIP.search(f): continue
    s = open(f, encoding="utf-8").read()
    if "function animateNumber" not in s: continue
    o = s
    for a, b in R: s = s.replace(a, b)
    if s != o:
        assert s.count("prefix") >= 3, f
        open(f, "w", encoding="utf-8").write(s); nf += 1
print("files", nf)

# -*- coding: utf-8 -*-
"""VS Health Benefits phone is (954) 866-6872 (owner, 2026-11-23). Replaces (954) 825-1009 in every format."""
import re, subprocess
RX = re.compile(r'(954\)?[ .\-]?)825([ .\-]?)1009')
files = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split("\n")
files = [f for f in files if f and not re.match(r'^(\.seo-work|_to_delete|node_modules|Claude outputs)/', f)
         and re.search(r'\.(html|js|json|txt|md|py|csv|xml)$', f)]
nf = tot = 0
for f in files:
    try: s = open(f, encoding="utf-8").read()
    except Exception: continue
    s2, n = RX.subn(lambda m: m.group(1) + "866" + m.group(2) + "6872", s)
    if n: open(f, "w", encoding="utf-8").write(s2); nf += 1; tot += n
print("files", nf, "replacements", tot)

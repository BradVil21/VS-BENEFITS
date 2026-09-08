# -*- coding: utf-8 -*-
"""Second pass: the minified pages declare START and END in one comma-separated
var statement, which the first pass's `var END =` pattern did not match. Those
46 files got the new two-phase branch but not the DEC15 constant it references.
"""
import glob, re

OLD = re.compile(r',END=new Date\("2026-12-15T23:59:59-05:00"\)\.getTime\(\);')
NEW = (',DEC15=new Date("2026-12-15T23:59:59-05:00").getTime()'
       ',END=new Date("2027-01-15T23:59:59-05:00").getTime();')

fixed = []
for f in sorted(glob.glob("*.html") + glob.glob("blog/*.html")):
    src = open(f, encoding="utf-8").read()
    if not OLD.search(src):
        continue
    open(f, "w", encoding="utf-8").write(OLD.sub(NEW, src))
    fixed.append(f)
print("patched %d files" % len(fixed))

# -*- coding: utf-8 -*-
"""Normalise to US spelling. This is a US insurance site read by US drivers and
US small-business owners, and the copy was drifting between both conventions
(1,008 "enroll" against 120 "enrol"). Whole-word replacements only, case aware.
"""
import glob, re, collections

PAIRS = [("enrol","enroll"),("Enrol","Enroll"),
         ("enrolment","enrollment"),("Enrolment","Enrollment"),
         ("subsidised","subsidized"),("Subsidised","Subsidized"),
         ("unsubsidised","unsubsidized"),("Unsubsidised","Unsubsidized"),
         ("licence","license"),("Licence","License"),
         ("licenced","licensed"),("Licenced","Licensed"),
         ("sceptical","skeptical"),("Sceptical","Skeptical"),
         ("behaviour","behavior"),("Behaviour","Behavior"),
         ("programme","program"),("Programme","Program"),
         ("programmes","programs"),("Programmes","Programs"),
         ("realise","realize"),("Realise","Realize"),
         ("realised","realized"),("Realised","Realized"),
         ("organisation","organization"),("Organisation","Organization"),
         ("organisations","organizations"),("Organisations","Organizations"),
         ("recognise","recognize"),("Recognise","Recognize"),
         ("recognised","recognized"),("Recognised","Recognized"),
         ("analyse","analyze"),("Analyse","Analyze"),
         ("utilise","utilize"),("Utilise","Utilize"),
         ("favour","favor"),("Favour","Favor"),
         ("favourable","favorable"),("Favourable","Favorable"),
         ("prioritise","prioritize"),("Prioritise","Prioritize"),
         ("specialise","specialize"),("Specialise","Specialize"),
         ("specialised","specialized"),("Specialised","Specialized"),
         ("minimise","minimize"),("Minimise","Minimize"),
         ("maximise","maximize"),("Maximise","Maximize")]
# longest first so "enrolment" is handled before "enrol"
PAIRS.sort(key=lambda p: -len(p[0]))

counts = collections.Counter()
files_changed = 0
for f in sorted(glob.glob("*.html") + glob.glob("blog/*.html")):
    src = open(f, encoding="utf-8").read()
    out = src
    for a, b in PAIRS:
        pat = re.compile(r"\b%s\b" % re.escape(a))
        n = len(pat.findall(out))
        if n:
            out = pat.sub(b, out)
            counts[a + " -> " + b] += n
    if out != src:
        open(f, "w", encoding="utf-8").write(out)
        files_changed += 1

print("files changed: %d\n" % files_changed)
for k, v in counts.most_common():
    print("  %5d  %s" % (v, k))
print("\ntotal replacements:", sum(counts.values()))

# -*- coding: utf-8 -*-
"""Repair the 2027 ACA open-enrollment window sitewide.
VERIFIED: OE for 2027 coverage runs Nov 1 2026 -> Jan 15 2027 on HealthCare.gov (incl. Florida).
Dec 15 2026 = deadline for Jan 1 2027 coverage (correct, must be preserved).
Plans selected Dec 16 - Jan 15 -> coverage starts Feb 1 2027.
"""
import re, glob, io, sys, collections

FILES = sorted(set(glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('guides/*.html')))

# Ordered, most-specific-first. (find, replace)
REPL = [
 # ---------- garbled sentences produced by the bad find/replace ----------
 ("plans selected December 16 through December 15 take effect February 1, 2027",
  "plans selected December 16, 2026 through January 15, 2027 take effect February 1, 2027"),
 ("enroll December 16 through December 15 and coverage starts February 1",
  "enroll December 16 through January 15 and coverage starts February 1"),
 ("Open enrollment then continues through December 15, 2026, but plans selected after December 15 take effect February 1, 2027 instead of January 1",
  "Open enrollment then continues through January 15, 2027, but plans selected after December 15 take effect February 1, 2027 instead of January 1"),
 ("If you enroll between December 16 and the December 15, 2026 close of open enrollment",
  "If you enroll between December 16, 2026 and the January 15, 2027 close of open enrollment"),
 ("If you miss the December 15, 2026 close of open enrollment",
  "If you miss the January 15, 2027 close of open enrollment"),
 ("Plans enrolled between January 1 and December 15 take effect February 1, 2027",
  "Plans enrolled December 16, 2026 through January 15, 2027 take effect February 1, 2027"),
 ("The absolute final deadline is <strong>December 15, 2026</strong>. But the more important deadline is December 15, 2026 -- that is the cutoff for January 1 coverage. If you miss December 15, you can still enroll through December 15, but your coverage will not start until February 1.",
  "The absolute final deadline is <strong>January 15, 2027</strong>. The more important deadline is <strong>December 15, 2026</strong> -- that is the cutoff for January 1 coverage. If you miss December 15 you can still enroll through January 15, but your coverage will not start until February 1."),
 ("The final deadline for ACA open enrollment 2027 is December 15, 2026. However, if you want your coverage to begin January 1, 2027, you must enroll by December 15, 2026.",
  "The final deadline for ACA open enrollment 2027 is January 15, 2027. However, if you want your coverage to begin January 1, 2027, you must enroll by December 15, 2026."),
 ("<li><strong>December 15, 2026</strong> -- Open Enrollment closes. Last chance to enroll in an",
  "<li><strong>January 15, 2027</strong> -- Open Enrollment closes. Last chance to enroll in an"),
 ("<tr><td>Open Enrollment ends (Florida &amp; most states)</td><td>December 15, 2026</td></tr>",
  "<tr><td>Open Enrollment ends (Florida &amp; most states)</td><td>January 15, 2027</td></tr>"),
 ("<li>December 15, 2026: Open enrollment closes (plans start February 1)</li>",
  "<li>January 15, 2027: Open enrollment closes (plans start February 1)</li>"),
 ("<td><strong>December 15, 2026</strong></td><td>Open Enrollment closes last chance for 2027 pl",
  "<td><strong>January 15, 2027</strong></td><td>Open Enrollment closes last chance for 2027 pl"),
 ("If you miss the December 15 deadline and do not qualify for a special enrollment period",
  "If you miss the January 15 deadline and do not qualify for a special enrollment period"),
 ("If you miss the December 15, 2026 open enrollment deadline, you can still enroll in an ACA market",
  "If you miss the January 15, 2027 open enrollment deadline, you can still enroll in an ACA market"),
 ("If you miss the December 15 deadline, you generally cannot enroll in an ACA marketplace plan unti",
  "If you miss the January 15 deadline, you generally cannot enroll in an ACA marketplace plan unti"),
 ("Some states with their own exchanges extend open enrollment past December 15 -- but not Florida.",
  "Some states with their own exchanges extend open enrollment past January 15; Florida follows the HealthCare.gov calendar."),
 ("Missing the December 15 deadline means your 2027 coverage will not start until February 1.",
  "Missing the December 15 deadline means your 2027 coverage will not start until February 1."),  # correct as-is
 ("The period is shorter than prior years, with no December 15 end date and no February 1 start.",
  "The window runs the full length used in recent years, closing January 15, 2027, with a February 1 start for plans selected after December 15."),
 ("It is shorter than prior years &mdash; there is no December 15 end date and no February 1 start.",
  "It runs the full length used in recent years &mdash; closing January 15, 2027, with a February 1 start for plans selected after December 15."),
 ("Open Enrollment for 2027 coverage runs November 1 to December 15, 2026 &mdash; a shorter window than you may remember, with no January",
  "Open Enrollment for 2027 coverage runs November 1, 2026 to January 15, 2027 &mdash; the same window used in recent years, with a January"),
 ("For 2027 coverage, Open Enrollment runs November 1 through December 15, 2026 in Florida and most states. Plans selected during this window t",
  "For 2027 coverage, Open Enrollment runs November 1, 2026 through January 15, 2027 in Florida and most states. Plans selected by December 15 t"),
 ("ACA Open Enrollment for 2027 coverage runs November 1, 2026 through December 15, 2026. Plans selected by December 15 take effect January 1, 2027.",
  "ACA Open Enrollment for 2027 coverage runs November 1, 2026 through January 15, 2027. Plans selected by December 15 take effect January 1, 2027; later selections start February 1, 2027."),
 ("for 2027 ACA health insurance coverage begins November 1, 2026 and ends December 15, 2026.",
  "for 2027 ACA health insurance coverage begins November 1, 2026 and ends January 15, 2027."),
 ("A federal rule would have closed open enrollment on <strong>December 15, 2026</strong> for everyone. <strong>A judge vacated that rule in Jun",
  "A federal rule would have closed open enrollment on <strong>December 15, 2026</strong> for everyone. <strong>A judge vacated that rule in Jun"),
 ("so most states are reverting to the traditional December 15 close.",
  "so HealthCare.gov states are keeping the traditional January 15 close."),
 ("Waiting until January means you miss the December 15 deadline for January 1 coverage",
  "Waiting until January means you miss the December 15 deadline for January 1 coverage"),  # correct as-is
 ("Treat December 15 as your real deadline no matter which state you live in.",
  "Treat December 15 as your real deadline no matter which state you live in &mdash; it is the cutoff for coverage that starts January 1."),
 ("<h3>Get Your 2027 Plan Locked In Before December 15</h3>",
  "<h3>Get Your 2027 Plan Locked In Before December 15</h3>"),  # correct as-is (Jan 1 coverage)
 ("There is no January cushion this year for a January 1",
  "December 15 is the cutoff for a January 1"),
 ("The new November 1 to December 15 deadline, special enrollment periods, and how to enroll on time.",
  "The November 1 to January 15 window, the December 15 cutoff for January 1 coverage, and how to enroll on time."),
 ("Open enrollment for 2027 health insurance runs November 1, 2026 to December 15, 2026. Enroll by December 15 for January 1 coverage.",
  "Open enrollment for 2027 health insurance runs November 1, 2026 to January 15, 2027. Enroll by December 15 for January 1 coverage."),
 ("most states, including Florida, runs from <strong>November 1, 2026 to December 15, 2026</strong>.",
  "most states, including Florida, runs from <strong>November 1, 2026 to January 15, 2027</strong>."),
 ("For 2027 coverage, open enrollment runs November 1, 2026 through December 15, 2026 on the federal marketplace",
  "For 2027 coverage, open enrollment runs November 1, 2026 through January 15, 2027 on the federal marketplace"),
 ("ACA open enrollment 2027 opens November 1, 2026 and closes December 15, 2026.",
  "ACA open enrollment 2027 opens November 1, 2026 and closes January 15, 2027."),
 ("ACA Open Enrollment 2027 opens November 1, 2026 and closes December 15, 2026.",
  "ACA Open Enrollment 2027 opens November 1, 2026 and closes January 15, 2027."),
 ("opens <strong>November 1, 2026</strong> and closes <strong>December 15, 2026</strong>.",
  "opens <strong>November 1, 2026</strong> and closes <strong>January 15, 2027</strong>."),
 ("coverage opens <strong>November 1, 2026</strong> and closes <strong>December 15, 2026</strong>",
  "coverage opens <strong>November 1, 2026</strong> and closes <strong>January 15, 2027</strong>"),
 ("open enrollment runs from <strong>November 1, 2026 through December 15, 2026</strong>",
  "open enrollment runs from <strong>November 1, 2026 through January 15, 2027</strong>"),
 ("Open Enrollment runs <strong>November 1 &ndash; December 15, 2026</strong>",
  "Open Enrollment runs <strong>November 1, 2026 &ndash; January 15, 2027</strong>"),
 ("November 1 through December 15, 2026 in Florida and most states, with coverage effective January 1,",
  "November 1, 2026 through January 15, 2027 in Florida and most states, with coverage effective January 1,"),
 ("window for plans purchased on this marketplace -- November 1, 2026 through December 15, 2026.",
  "window for plans purchased on this marketplace -- November 1, 2026 through January 15, 2027."),
 ("next open enrollment (November 1, 2026 to December 15, 2026 for 2027 coverage)",
  "next open enrollment (November 1, 2026 to January 15, 2027 for 2027 coverage)"),
 ("currently November 1, 2026 to December 15, 2026 (enroll by December 15 for a January 1 start)",
  "currently November 1, 2026 to January 15, 2027 (enroll by December 15 for a January 1 start)"),
 # ---------- generic window phrasings (state pages, city pages, FAQs) ----------
 ("Open Enrollment runs November 1 through December 15 each year.",
  "Open Enrollment runs November 1 through January 15 each year."),
 ("Open Enrollment runs November 1 through December 15.",
  "Open Enrollment runs November 1 through January 15."),
 ("Open Enrollment for Nevada Health Link runs November 1 through December 15.",
  "Open Enrollment for Nevada Health Link runs November 1 through January 15."),
 ("Open Enrollment for MNsure runs November 1 through December 15.",
  "Open Enrollment for MNsure runs November 1 through January 15."),
 ("Open enrollment runs November 1 to December 15 each year.",
  "Open enrollment runs November 1 to January 15 each year."),
 ("Open enrollment runs November 1 to December 15.",
  "Open enrollment runs November 1 to January 15."),
 ("Open enrollment for 2027 coverage runs November 1 through December 15.",
  "Open enrollment for 2027 coverage runs November 1 through January 15."),
 ("Open enrollment for 2027 coverage runs from November 1 to December 15 in most states.",
  "Open enrollment for 2027 coverage runs from November 1 to January 15 in most states."),
 ("During open enrollment, which runs November 1 to December 15 in most states for 2027 coverage.",
  "During open enrollment, which runs November 1 to January 15 in most states for 2027 coverage."),
 ("generally November 1 through December 15, when anyone can enroll in a marketplace plan.",
  "generally November 1 through January 15, when anyone can enroll in a marketplace plan."),
 ("The November 1 to December 15 Open Enrollment window applies to individual and ACA marketplace plan",
  "The November 1 to January 15 Open Enrollment window applies to individual and ACA marketplace plan"),
 ("Individual and ACA plans follow the November 1 to December 15 window,",
  "Individual and ACA plans follow the November 1 to January 15 window,"),
 ("Individual and ACA plans for part-time staff follow the November 1 to December 15 window,",
  "Individual and ACA plans for part-time staff follow the November 1 to January 15 window,"),
 ("group plans are not restricted to the November 1 to December 15 Open Enrollment window",
  "group plans are not restricted to the November 1 to January 15 Open Enrollment window"),
 ("<h3>Open Enrollment 2027 FAQ</h3>", "<h3>Open Enrollment 2027 FAQ</h3>"),
]

counts = collections.Counter(); touched = {}
for f in FILES:
    s = open(f, encoding='utf-8').read(); orig = s
    for a, b in REPL:
        if a == b: continue
        n = s.count(a)
        if n:
            s = s.replace(a, b); counts[a[:60]] += n
    if s != orig:
        open(f, 'w', encoding='utf-8').write(s)
        touched[f] = True

print("files changed:", len(touched))
print("total replacements:", sum(counts.values()))
for k, v in counts.most_common(12):
    print("  %3d  %s..." % (v, k))

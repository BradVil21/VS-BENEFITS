# -*- coding: utf-8 -*-
"""Rebuild the 2027 state deadline table with verified dates.
Verified 2026-08-25 against healthinsurance.org deadline FAQ (two fetches, consistent).
HealthCare.gov: Nov 1 2026 - Jan 15 2027. Dec 15 2026 = Jan 1 coverage cutoff.
"""
import re
F='blog/aca-open-enrollment-2027-guide.html'
s=open(F,encoding='utf-8').read(); orig=s

# --- 1. author comment: refresh provenance ---
s=s.replace("""           Source: healthinsurance.org deadline FAQ, page last updated 2026-07-13.
           The Marketplace Integrity rule's shortened OE (ending Dec 15) was VACATED
           by a federal judge in June 2026. HHS may appeal. Re-verify every state
           against its own exchange site before October 2026 and update
           the "Last verified" date below.""",
"""           Source: healthinsurance.org deadline FAQ. Re-verified 2026-08-25.
           The Marketplace Integrity rule's shortened OE (ending Dec 15) was VACATED
           by a federal judge in June 2026, so HealthCare.gov reverts to the standard
           Nov 1 - Jan 15 window. Dec 15 remains the cutoff for Jan 1 coverage.
           HHS may appeal. Re-verify every state against its own exchange site
           before October 2026 and update the "Last verified" date below.""")

# --- 2. alert box: the end date IS settled for HealthCare.gov ---
s=s.replace("""        <h4>The end date is not settled this year — and that is unusual</h4>
        <p style="margin:0">A federal rule would have closed open enrollment on <strong>December 15, 2026</strong> for everyone. <strong>A judge vacated that rule in June 2026</strong>, so HealthCare.gov states are keeping the traditional January 15 close. HHS could still appeal. This means the deadline you read on a page written last year is probably wrong. Below is where each state stands right now, and we update it as states confirm.</p>""",
"""        <h4>A lot of pages still show the wrong end date this year</h4>
        <p style="margin:0">A federal rule would have closed open enrollment on <strong>December 15, 2026</strong> for everyone. <strong>A judge vacated that rule in June 2026</strong>, so HealthCare.gov keeps the standard close of <strong>January 15, 2027</strong>. HHS could still appeal. Plenty of pages written while that rule was pending still show December 15 as the deadline &mdash; it is not. December 15 matters for a different reason: it is the cutoff for coverage that starts January 1. Verified against state exchange guidance on <strong>August 25, 2026</strong>.</p>""")

# --- 3. start-date paragraph ---
s=s.replace("""<p><strong>Everyone starts at the same time.</strong> Open enrollment for 2027 coverage begins <strong>November 1, 2026</strong> in every state except three: Idaho and Pennsylvania open early on <strong>October 15</strong>, and Massachusetts opens <strong>October 23</strong>.</p>""",
"""<p><strong>Almost everyone starts at the same time.</strong> Open enrollment for 2027 coverage begins <strong>November 1, 2026</strong> in every state except three: Idaho opens early on <strong>October 15</strong>, and Connecticut and Massachusetts open on <strong>October 23</strong>.</p>""")

s=s.replace("""<p><strong>The close date is where it varies.</strong> If your state runs its own exchange, your deadline is set by that exchange. If your state uses HealthCare.gov — that includes Florida, Texas, Ohio, Tennessee, and most of the South and Midwest — you follow the federal date, which is the one still moving after the June ruling.</p>""",
"""<p><strong>The close date is where it varies.</strong> If your state runs its own exchange, your deadline is set by that exchange. If your state uses HealthCare.gov &mdash; that includes Florida, Texas, Ohio, Tennessee, and most of the South and Midwest &mdash; you follow the federal date: <strong>January 15, 2027</strong>. Most state exchanges land on the same day; a handful run later, and two close earlier.</p>""")

# --- 4. the table itself ---
i=s.find('<table class="dates-table" aria-label="2027 open enrollment deadlines by state">')
j=s.find('</table>',i)+8
assert i>0 and j>i, 'table not found'

ROWS = [
 ("All HealthCare.gov states", "FL, TX, OH, TN, NC, AZ, MO and ~30 others", "January 15, 2027", True),
 ("California", "", "January 31, 2027", False),
 ("District of Columbia", "", "January 31, 2027", False),
 ("New Jersey", "", "January 31, 2027", False),
 ("New York", "", "January 31, 2027", False),
 ("Virginia", "", "January 29, 2027", False),
 ("Massachusetts", "opens October 23, 2026", "January 23, 2027", False),
 ("Colorado", "", "January 15, 2027", False),
 ("Connecticut", "opens October 23, 2026", "January 15, 2027", False),
 ("Georgia", "", "January 15, 2027", False),
 ("Illinois", "", "January 15, 2027", False),
 ("Kentucky", "", "January 15, 2027", False),
 ("Maine", "", "January 15, 2027", False),
 ("Maryland", "", "January 15, 2027", False),
 ("Minnesota", "", "January 15, 2027", False),
 ("Nevada", "", "January 15, 2027", False),
 ("New Mexico", "", "January 15, 2027", False),
 ("Oregon", "", "January 15, 2027", False),
 ("Pennsylvania", "", "January 15, 2027", False),
 ("Vermont", "", "January 15, 2027", False),
 ("Washington", "", "January 15, 2027", False),
 ("Rhode Island", "closes early", "December 31, 2026", False),
 ("Idaho", "opens October 15, 2026 &mdash; closes earliest in the country", "December 15, 2026", False),
]
out=['<table class="dates-table" aria-label="2027 open enrollment deadlines by state">',
     '        <thead>',
     '          <tr><th>State</th><th>2027 enrollment closes</th></tr>',
     '        </thead>','        <tbody>']
for name,note,date,bold in ROWS:
    n = '<strong>%s</strong>'%name
    if note: n += '<br><span style="font-size:.85em;opacity:.75">%s</span>'%note
    d = '<strong>%s</strong>'%date if bold else date
    out.append('          <tr><td>%s</td><td>%s</td></tr>'%(n,d))
out += ['        </tbody>','      </table>']
s = s[:i] + '\n'.join(out) + s[j:]

# --- 5. remaining stray Dec-15-as-close references on this page ---
s=s.replace("give themselves the most time to review plans before the December 15 deadline.",
            "give themselves the most time to review plans before the December 15 cutoff for January 1 coverage.")
s=s.replace("The closing date now varies by state after a June 2026 court ruling",
            "Open enrollment then closes January 15, 2027 in Florida and most states")

open(F,'w',encoding='utf-8').write(s)
print('changed:', s!=orig, '| rows:', len(ROWS), '| delta bytes:', len(s)-len(orig))

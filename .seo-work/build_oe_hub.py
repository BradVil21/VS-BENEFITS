# -*- coding: utf-8 -*-
"""Build the open-enrollment hub: Florida section, missed-enrollment FAQs,
freshness dates, and cross-links across the five OE pages."""
import re, json, io

GUIDE = 'blog/aca-open-enrollment-2027-guide.html'
TODAY = '2026-08-25'

# ---------------------------------------------------------------- 1. Florida section
FLORIDA = '''
      <h2 id="florida">Open Enrollment 2027 in Florida</h2>

      <p><strong>Florida uses HealthCare.gov.</strong> There is no separate Florida exchange and no Florida-only deadline. Open enrollment for 2027 coverage runs <strong>November 1, 2026 through January 15, 2027</strong>, exactly like Texas, Georgia and the other thirty-odd HealthCare.gov states. Enroll by <strong>December 15, 2026</strong> and your coverage starts January 1. Enroll between December 16 and January 15 and it starts February 1.</p>

      <p>Three things make Florida different in practice, and none of them are about the calendar:</p>

      <ul>
        <li><strong>Florida has not expanded Medicaid.</strong> That leaves a coverage gap: adults earning below the poverty line often do not qualify for Medicaid <em>or</em> for marketplace subsidies. If your income estimate lands near the line, where you land matters enormously, and it is worth getting the estimate right before you enroll rather than after.</li>
        <li><strong>Networks are narrower than the plan names suggest.</strong> South Florida has a lot of plans that look like PPOs on the summary page and behave like HMOs at the specialist's front desk. Check your doctors individually, by name, in the plan's own directory &mdash; not the carrier's general one.</li>
        <li><strong>A large share of Florida enrollees are self-employed.</strong> Owner-operators, contractors, stylists, rideshare drivers and small-business owners estimate income for the year ahead rather than reading it off a W-2. Estimate it too low and you repay the difference at tax time; too high and you overpay every month. Our <a href="/aca-subsidy-calculator">ACA subsidy calculator</a> gives you the number before you commit to it.</li>
      </ul>

      <p>If you are in Miami-Dade, Broward or Palm Beach and want someone to run your actual numbers, that is what we do &mdash; and carriers pay our commission, so it costs you nothing. <a href="/quote">Get a free quote</a> or read our <a href="/florida-health-insurance-answers">Florida health insurance answers</a>.</p>
'''

s = open(GUIDE, encoding='utf-8').read(); orig = s
anchor = '<h2 id="subsidies">'
assert anchor in s, 'subsidies anchor missing'
if 'id="florida"' not in s:
    s = s.replace(anchor, FLORIDA + '\n      ' + anchor, 1)

# ---------------------------------------------------------------- 2. new FAQs
NEW_FAQ = [
 ("Is open enrollment for health insurance 2027 different in Florida?",
  "No. Florida uses HealthCare.gov, so open enrollment for 2027 coverage runs November 1, 2026 through January 15, 2027, the same as every other HealthCare.gov state. Enroll by December 15, 2026 for coverage that starts January 1, 2027."),
 ("I missed open enrollment by one day. Can I still enroll?",
  "Not in a standard marketplace plan, unless you qualify for a special enrollment period. Missing January 15 by a day is treated the same as missing it by a month. However, a qualifying life event in the previous 60 days, such as losing coverage, moving, marrying or having a baby, reopens a 60-day enrollment window. Medicaid and CHIP also enroll year-round if you qualify."),
 ("What happens if I miss open enrollment at work?",
  "Employer open enrollment is set by your employer's plan year, not the ACA calendar, so missing it is a separate problem. You generally wait until the next plan year unless you have a qualifying life event. You may still be able to buy an individual marketplace plan during ACA open enrollment, though you will not get a subsidy if your employer offered you affordable coverage that meets minimum value."),
 ("When does open enrollment start for 2027?",
  "November 1, 2026 in every state except three. Idaho opens earliest on October 15, 2026, and Connecticut and Massachusetts open on October 23, 2026. Every state closes on a different schedule; HealthCare.gov states close January 15, 2027."),
]

# 2a. visible FAQ (append before the close of the faq section)
i = s.find('id="faq"')
j = s.find('</section>', i)
if j < 0: j = s.find('<section', i + 10)
vis = ''.join('\n        <h3>%s</h3>\n        <p>%s</p>' % (q, a) for q, a in NEW_FAQ
              if q not in s)
if vis:
    k = s.rfind('</p>', i, j) + 4
    s = s[:k] + vis + s[k:]

# 2b. FAQPage schema
faq_span = None
for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
    raw = mm.group(1).strip()
    try:
        d = json.loads(raw)
    except Exception:
        continue
    if isinstance(d, dict) and d.get('@type') == 'FAQPage':
        faq_span = (mm.start(1) + (len(mm.group(1)) - len(mm.group(1).lstrip())), None, d)
        start = mm.start(1) + mm.group(1).index(raw)
        faq_span = (start, start + len(raw), d)
        break
assert faq_span, 'FAQPage block not found'
fstart, fend, data = faq_span
have = {q['name'] for q in data['mainEntity']}
for q, a in NEW_FAQ:
    if q not in have:
        data['mainEntity'].append({"@type": "Question", "name": q,
                                   "acceptedAnswer": {"@type": "Answer", "text": a}})
s = s[:fstart] + json.dumps(data, indent=2, ensure_ascii=False) + s[fend:]

# ---------------------------------------------------------------- 3. freshness
s = re.sub(r'"dateModified"\s*:\s*"[\d-]+"', '"dateModified": "%s"' % TODAY, s)
s = re.sub(r'Updated July 22, 2026', 'Updated August 25, 2026', s)
open(GUIDE, 'w', encoding='utf-8').write(s)
print('guide updated:', s != orig, '| florida section:', 'id="florida"' in s,
      '| FAQ count:', len(data['mainEntity']))

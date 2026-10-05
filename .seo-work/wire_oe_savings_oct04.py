# -*- coding: utf-8 -*-
"""Wire the 4 Oct 2026 Open Enrollment savings cluster into the site.

1. 'Paying more for 2027?' link block on the OE / subsidy pages and the new posts.
2. Two cards (cliff calculator + owner-operator 2027 post) added to the trucking tools
   block that already sits on every trucking page, plus a driver link block on the
   main owner-operator / driver OE pages.
3. blog.html cards, sitemap.xml URLs, llms.txt entries.
Idempotent: safe to re-run.
"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linkblock import inject

TODAY = '2026-10-04'
SITE = 'https://www.vshealthbenefits.com'

C = {
 'lower':  ('/blog/how-to-lower-health-insurance-premiums-2027', 'How to Lower Your 2027 Premium',
            'Rates are up a median 15% and the 400% cliff is back. Eleven legal ways to pay less, from income planning to HSA bronze plans.'),
 'renew':  ('/blog/health-insurance-renewal-notice-2027', 'Read Your Renewal Notice Before You Renew',
            'The number on the letter uses last year\'s income and a benchmark that just moved. Six checks before December 15.'),
 'lose':   ('/blog/losing-health-insurance-2027', 'Losing Coverage in 2027?',
            'Cigna is leaving the Marketplace, Medicaid work rules start and immigrant rules narrow. Your deadline and how to avoid a gap.'),
 'cheap':  ('/blog/cheapest-health-insurance-2027', 'Cheapest Health Insurance for 2027',
            'Subsidized bronze, silver with extra savings, bronze plus HSA and catastrophic plans, now open to more people.'),
 'picalc': ('/health-insurance-premium-increase-calculator', '2027 Premium Increase Calculator',
            'Enter your renewal number and income. See your increase and whether you are paying more than a benchmark plan should cost.'),
 'oo':     ('/blog/owner-operator-health-insurance-increase-2027', 'Owner-Operators: Cut Your 2027 Cost',
            'Net profit, Solo 401(k) and SEP contributions, HSA bronze plans and the networks that work on the road.'),
 'oocalc': ('/owner-operator-subsidy-cliff-calculator', 'Owner-Operator Subsidy Cliff Calculator',
            'Net profit in, MAGI out. See how close you are to the 400% line and what contribution gets your credit back.'),
}

OE_PAGES = [
 'open-enrollment.html', 'health-insurance-open-enrollment-faq.html', 'aca-subsidy-calculator.html',
 'blog/aca-open-enrollment-2027-guide.html', 'blog/open-enrollment-2027-income-premium-increase.html',
 'blog/aca-subsidies-ended-2026-what-to-do.html', 'blog/what-happens-if-you-miss-open-enrollment.html',
 'blog/aca-income-limits-2027.html', 'blog/how-to-shop-for-health-insurance.html',
 'blog/how-much-does-health-insurance-cost-2026.html', 'blog/what-income-counts-for-aca-subsidies.html',
 'affordable-health-insurance.html', 'how-much-does-health-insurance-cost.html', 'health-insurance-cost-faq.html',
 'cobra-alternatives.html', 'family-health-insurance.html', 'bronze-vs-silver-vs-gold-vs-platinum.html',
 'blog/how-to-lower-health-insurance-premiums-2027.html', 'blog/health-insurance-renewal-notice-2027.html',
 'blog/losing-health-insurance-2027.html', 'blog/cheapest-health-insurance-2027.html',
 'health-insurance-premium-increase-calculator.html',
]
OE_KEYS = ['picalc', 'lower', 'renew', 'lose', 'cheap']

DRIVER_PAGES = [
 'truck-driver-open-enrollment-2027.html', 'blog/owner-operator-health-insurance-no-subsidy.html',
 'best-health-insurance-owner-operators.html', 'truck-driver-health-insurance-cost-calculator.html',
 'blog/can-owner-operators-deduct-health-insurance.html', 'can-truckers-deduct-health-insurance.html',
 'blog/affordable-health-insurance-truck-drivers.html', 'blog/owner-operator-health-insurance-increase-2027.html',
 'owner-operator-subsidy-cliff-calculator.html',
]
DRIVER_KEYS = ['oocalc', 'oo', 'lower', 'lose']

n = 0
for path in OE_PAGES:
    if not os.path.exists(path):
        print('  missing', path); continue
    slug = '/' + path[:-5]
    cards = [C[k] for k in OE_KEYS if C[k][0] != slug][:4]
    if inject(path, 'oe-savings-2027', 'Paying more for 2027? Start here',
              'Premiums are up again and Open Enrollment runs November 1 to January 15.', cards,
              cta='/quote?type=individual', cta_text='Get my free 2027 quote'):
        n += 1
for path in DRIVER_PAGES:
    if not os.path.exists(path):
        print('  missing', path); continue
    slug = '/' + path[:-5]
    cards = [C[k] for k in DRIVER_KEYS if C[k][0] != slug][:4]
    if inject(path, 'oo-savings-2027', 'Drivers: keep your subsidy in 2027',
              'A good year can cost an owner-operator the whole credit.', cards,
              cta='/quote?type=individual', cta_text='Get my quote'):
        n += 1
print('link blocks written:', n)

# 2. trucking tools block: two new cards
NEW_CARDS = ''.join(
    '\n        <a class="vs-rg-card" href="%s" data-oe27>\n          <strong>%s</strong>\n          <span>%s</span>\n'
    '          <em>%s &rarr;</em>\n        </a>' % (C[k][0], C[k][1], C[k][2], lbl)
    for k, lbl in [('oocalc', 'Check my cliff'), ('oo', 'Read the guide')])
t = 0
for f in sorted(glob.glob('*.html') + glob.glob('blog/*.html')):
    s = open(f, encoding='utf-8').read()
    i = s.find('data-block="vs-trucking-tools"')
    if i < 0 or 'data-oe27' in s:
        continue
    g = s.find('<div class="vs-rg-grid">', i)
    if g < 0:
        continue
    g += len('<div class="vs-rg-grid">')
    s = s[:g] + NEW_CARDS + s[g:]
    open(f, 'w', encoding='utf-8').write(s); t += 1
print('trucking tools blocks updated:', t)

# 3a. blog.html cards at the top of the first grid
POSTS = [
 ('/blog/how-to-lower-health-insurance-premiums-2027', '/compressed/health-insurance-cost-2026-woman.jpg',
  'Woman reviewing her 2027 health insurance premium', 'Open Enrollment 2027 | 9 min read',
  'How to lower your health insurance premium in 2027: 11 moves that work',
  'Rates are up a median 15% and the subsidy cliff is back. Income planning, HSA bronze plans, catastrophic plans and more.'),
 ('/health-insurance-premium-increase-calculator', '/compressed/ACA.jpg',
  '2027 health insurance premium increase calculator', 'Free Tool | 1 minute',
  'Did your health insurance go up? 2027 premium increase calculator',
  'Enter your renewal number and income. See your increase and whether you are paying more than you should.'),
 ('/blog/health-insurance-renewal-notice-2027', '/compressed/insurance-advisor-woman.jpg',
  'Reading a 2027 health insurance renewal notice', 'Open Enrollment 2027 | 7 min read',
  'Got your 2027 renewal notice? Check these 6 things before you auto-renew',
  'Why the number on the letter is often wrong, what happens if you do nothing, and the December 15 deadline.'),
 ('/blog/losing-health-insurance-2027', '/compressed/family-picture.jpg',
  'Family losing health coverage in 2027', 'Open Enrollment 2027 | 8 min read',
  'Losing your health insurance in 2027? Who is affected and what to do',
  'Cigna leaving the Marketplace, the 400% cliff, Medicaid work rules and new immigrant rules. Your deadline and next steps.'),
 ('/blog/cheapest-health-insurance-2027', '/compressed/ACAphoto.jpg',
  'Cheapest health insurance options for 2027', 'Open Enrollment 2027 | 8 min read',
  'The cheapest health insurance in 2027: bronze, HSA and catastrophic compared',
  'What actually costs less at your income, and the plans that only look cheaper.'),
 ('/blog/owner-operator-health-insurance-increase-2027', '/compressed/truck-driver-hands-on-wheel-sunrise.jpg',
  'Owner-operator truck driver at sunrise', 'Trucking | 8 min read',
  'Owner-operator health insurance going up in 2027? 8 ways to cut the cost',
  'Keep your subsidy with net profit, Solo 401(k) and SEP contributions, and an HSA. Plus the cliff calculator.'),
 ('/owner-operator-subsidy-cliff-calculator', '/compressed/truck-driver-highway-view-state-line.jpg',
  'Owner-operator subsidy cliff calculator', 'Trucking Tool | 1 minute',
  'Owner-operator subsidy cliff calculator for 2027',
  'Net profit in, MAGI out. How close you are to the 400% line and the contribution that gets your credit back.'),
]
b = open('blog.html', encoding='utf-8').read()
if 'data-oe27-card' not in b:
    cards = ''.join(
        '\n      <a class="post-card" href="%s" data-oe27-card>\n        <div class="cover"><img src="%s" alt="%s" loading="lazy" /></div>\n'
        '        <div class="body">\n          <div class="meta">%s</div>\n          <h3>%s</h3>\n          <p>%s</p>\n'
        '          <span class="read-more">%s &rarr;</span>\n        </div>\n      </a>\n' %
        (h, img, alt, meta, t_, d, 'Use the tool' if 'calculator' in h else 'Read article')
        for h, img, alt, meta, t_, d in POSTS)
    g = b.index('<div class="post-grid">') + len('<div class="post-grid">')
    b = b[:g] + cards + b[g:]
    open('blog.html', 'w', encoding='utf-8').write(b)
    print('blog.html: 7 cards added')

# 3b. sitemap
sm = open('sitemap.xml', encoding='utf-8').read()
new = [('/blog/' + p[0].split('/blog/')[1], '0.9') if '/blog/' in p[0] else (p[0], '0.9') for p in POSTS]
add = ''.join('<url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n' % (SITE, u, TODAY, pr)
              for u, pr in new if '<loc>%s%s</loc>' % (SITE, u) not in sm)
sm = sm.replace('</urlset>', add + '</urlset>')
touched = ['/blog'] + ['/' + p[:-5] for p in OE_PAGES + DRIVER_PAGES]
for u in set(touched):
    sm = re.sub(r'(<loc>%s%s</loc><lastmod>)[^<]*' % (re.escape(SITE), re.escape(u)), r'\g<1>' + TODAY, sm)
open('sitemap.xml', 'w', encoding='utf-8').write(sm)
print('sitemap: %d urls added' % add.count('<url>'))

# 3c. llms.txt
L = open('llms.txt', encoding='utf-8').read()
if 'premium-increase-calculator' not in L:
    lines = (
     '- [How to Lower Your Health Insurance Premium in 2027](%s/blog/how-to-lower-health-insurance-premiums-2027): 11 ways to pay less after the 2027 rate increases and the return of the 400%% subsidy cliff.\n'
     '- [2027 Premium Increase Calculator](%s/health-insurance-premium-increase-calculator): compares a renewal premium with the expected benchmark cost at the user\'s income.\n'
     '- [2027 Renewal Notice Checklist](%s/blog/health-insurance-renewal-notice-2027): auto re-enrollment, benchmark shifts and six checks before December 15.\n'
     '- [Losing Health Insurance in 2027](%s/blog/losing-health-insurance-2027): insurer exits (Cigna), Medicaid work requirements, immigrant eligibility, the end of the 150%% FPL monthly SEP.\n'
     '- [Cheapest Health Insurance in 2027](%s/blog/cheapest-health-insurance-2027): subsidized bronze, cost-sharing silver, bronze plus HSA and catastrophic plans.\n'
     '- [Owner-Operator Health Insurance 2027](%s/blog/owner-operator-health-insurance-increase-2027): how truck drivers keep the subsidy with net profit, Solo 401(k)/SEP and HSA contributions.\n'
     '- [Owner-Operator Subsidy Cliff Calculator](%s/owner-operator-subsidy-cliff-calculator): net profit to MAGI to the 400%% line, with the contribution needed to get under it.\n'
    ) % ((SITE,) * 7)
    anchor = '- [Inscripción Abierta 2027'
    i = L.find(anchor)
    i = L.find('\n', i) + 1 if i >= 0 else len(L)
    L = L[:i] + lines + L[i:]
    open('llms.txt', 'w', encoding='utf-8').write(L)
    print('llms.txt: 7 entries added')

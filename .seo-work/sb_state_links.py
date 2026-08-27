# -*- coding: utf-8 -*-
"""Wire the new TX / MD / KY state hubs and the 5-post blog cluster into the site.

1. 'States we write group coverage in' block across the small-business cluster.
2. Sibling-state block on each of the three new state hubs.
3. Five new cards at the top of the blog index.
"""
import sys, os, re, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linkblock import inject

red = {r['source'] for r in json.load(open('vercel.json'))['redirects']}

S = {
 'fl': ('/florida-small-business-health-insurance', 'Florida: 1 to 50 employees',
        'County-based rating, no state employer mandate, and the widest carrier choice of the four. Miami-Dade sits at the top of the price range.'),
 'tx': ('/texas-small-business-health-insurance', 'Texas: two employees, 27 rating areas',
        'Texas requires two employees, not one. 75 percent participation, and a tobacco load cannot be charged to an individual employee.'),
 'md': ('/maryland-small-business-health-insurance', 'Maryland: a SHOP that still works',
        'One of the last real state small-business exchanges, and no Maryland carrier applies a tobacco surcharge at all.'),
 'ky': ('/kentucky-small-business-health-insurance', 'Kentucky: SHOP is closed',
        'kynect no longer enrolls new small groups, so coverage runs through a carrier or broker. Two-employee minimum, 1.4:1 tobacco cap.'),
}

H = 'Group coverage by state'
SUB = ('The rules genuinely differ. Two of these four states will not sell a group plan to a '
       'one-person business, and one has no small-business marketplace left at all.')

# --- 1. small-business cluster pages -----------------------------------------
SB = [f for f in sorted(glob.glob('*.html')) if re.search(
    r'small-business|business-open-enrollment|group-health-insurance-by-industry|'
    r'health-insurance-for-(auto-repair|cleaning|construction|dental-offices|hvac|restaurants|'
    r'retail|salons|trucking-companies|contractors|real-estate|my-employees|small-business-owners)|'
    r'ichra-florida|level-funded|restaurant-health-insurance', f)]

n = 0
for f in SB:
    slug = '/' + f[:-5]
    if slug in red:
        continue
    cards = [S[k] for k in ('fl', 'tx', 'md', 'ky') if S[k][0] != slug]
    if len(cards) == 4:
        cards = cards[:4]
    if inject(f, 'sb-states', H, SUB, cards, cta='/quote?type=business', cta_text='Get group quotes'):
        n += 1
print('small-business cluster pages given the state block:', n)

# --- 2. the three new state hubs get each other + Florida --------------------
for f, keys in [('texas-small-business-health-insurance.html', ('fl', 'md', 'ky')),
                ('maryland-small-business-health-insurance.html', ('fl', 'tx', 'ky')),
                ('kentucky-small-business-health-insurance.html', ('fl', 'tx', 'md'))]:
    inject(f, 'sb-states', 'We write group coverage in these states too',
           'Same team, same zero cost to you. The rules change at the state line, so the pages do too.',
           [S[k] for k in keys], cta='/quote?type=business', cta_text='Get group quotes')
print('state hubs cross-linked to each other')

# --- 3. blog index ----------------------------------------------------------
POSTS = [
 ('ichra-vs-group-health-subsidy-cliff', '/compressed/servicesmeeting.jpg',
  'Employer comparing ICHRA and group health insurance after the ACA subsidy cliff returned',
  'Employer Strategy | 9 min read',
  'ICHRA vs Group Health Now That the 400% Subsidy Cliff Is Back',
  'The enhanced ACA subsidies expired at the end of 2025. Above 400 percent of the poverty level there is no subsidy left to collect, and that changes the ICHRA arithmetic.'),
 ('small-business-health-insurance-cost-2027', '/compressed/health-insurance-cost-2026-woman.jpg',
  'Small business owner comparing group health insurance premium costs for 2027',
  'Small Business | 9 min read',
  'What Small Business Health Insurance Actually Costs &mdash; and Why Every State Average You Read Is Wrong',
  'The one national benchmark worth quoting, why a per-state average describes no real employer, and the five things that actually set your premium.'),
 ('small-business-health-care-tax-credit-2026', '/compressed/business-seminar.jpg',
  'Small business owner reviewing the federal small business health care tax credit with an advisor',
  'Small Business | 8 min read',
  'The Small Business Health Care Tax Credit in 2026: Who Can Still Claim It',
  'Up to half your premiums for exactly two years, gated behind a SHOP requirement that has quietly stopped working in Kentucky. The honest arithmetic.'),
 ('group-health-insurance-minimum-participation', '/compressed/business-team-meeting.jpg',
  'Small business team reviewing group health insurance enrollment and participation requirements',
  'Small Business | 8 min read',
  'Can&rsquo;t Hit Minimum Participation? The Two-Week Window That Suspends It',
  'Participation stops more small group applications than price does. Who actually counts, and the November 15 to December 15 rule almost no employer knows about.'),
 ('how-many-employees-do-you-need-for-group-health-insurance', '/compressed/microgroup.jpg',
  'Small business owner counting employees to check group health insurance eligibility',
  'Small Business | 7 min read',
  'How Many Employees Do You Need for Group Health Insurance? Florida, Texas, Maryland and Kentucky',
  'The federal answer is one employee. Texas and Kentucky both require two. Here is what each state actually demands, and who counts.'),
]

s = open('blog.html', encoding='utf-8').read()
added = 0
for slug, img, alt, meta, title, blurb in POSTS:
    if '/blog/' + slug in s:
        continue
    card = ('''      <a class="post-card" href="/blog/%s">
        <div class="cover"><img src="%s" alt="%s" loading="lazy" /></div>
        <div class="body">
          <div class="meta">%s</div>
          <h3>%s</h3>
          <p>%s</p>
          <span class="read-more">Read article &rarr;</span>
        </div>
      </a>

''' % (slug, img, alt, meta, title, blurb))
    anchor = '      <!-- Newest posts -->\n'
    assert anchor in s, 'blog.html anchor moved'
    s = s.replace(anchor, anchor + card, 1)
    added += 1
open('blog.html', 'w', encoding='utf-8').write(s)
print('blog index cards added:', added)

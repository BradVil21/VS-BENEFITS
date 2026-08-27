# -*- coding: utf-8 -*-
"""Wire the COBRA cluster into the pages a COBRA searcher already lands on,
and add the four cards to the blog index."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from linkblock import inject

red = {r['source'] for r in json.load(open('vercel.json'))['redirects']}

C = {
 'pillar': ('/cobra-alternatives', 'Cheaper Alternatives to COBRA',
            'Why the quote is 4 to 6 times your payroll deduction, six options that cost less, and the one move that locks you out until January.'),
 'calc':   ('/cobra-vs-marketplace-calculator', 'COBRA vs Marketplace Calculator',
            'Put your COBRA premium next to a subsidized marketplace plan. Monthly gap, yearly gap, and how many days you have left.'),
 'cost':   ('/blog/why-is-cobra-so-expensive', 'Why Is COBRA So Expensive?',
            'It is capped at 102 percent of your plan&rsquo;s full cost. Where the number comes from, and what the 2 percent is for.'),
 'loop':   ('/blog/cobra-60-day-loophole', 'The COBRA 60-Day Loophole',
            'Coverage backdates to the day you lost it, so the election window is a free option &mdash; unless you sign the waiver.'),
 'drop':   ('/blog/can-i-drop-cobra-for-marketplace', 'Can I Drop COBRA and Switch?',
            'Cancelling mid-year opens nothing. Running out opens 60 days. The three windows where switching actually works.'),
 'sep':    ('/special-enrollment-period-checker', 'Special Enrollment Period Checker',
            'Confirm you can enroll outside open enrollment, and how many days are left on the clock.'),
 'sub':    ('/aca-subsidy-calculator', 'ACA Subsidy Calculator',
            'Estimate your premium tax credit from household size and projected income &mdash; the number that decides the comparison.'),
 'jobs':   ('/health-insurance-between-jobs', 'Coverage Between Jobs',
            'What to do when there is a gap to bridge and the next job&rsquo;s benefits do not start on day one.'),
}

# pages a COBRA searcher realistically lands on, and what each should offer next
TARGETS = {
 'cobra-vs-marketplace-calculator.html':        ['pillar', 'drop', 'cost', 'loop'],
 'health-insurance-between-jobs.html':          ['pillar', 'calc', 'loop', 'drop'],
 'blog/lost-health-insurance-job-loss-options.html': ['pillar', 'calc', 'cost', 'drop'],
 'special-enrollment-period-checker.html':      ['pillar', 'drop', 'calc', 'jobs'],
 'qualifying-life-events-health-insurance.html':['drop', 'pillar', 'calc', 'sep'],
 'health-insurance-before-medicare.html':       ['pillar', 'calc', 'drop', 'sub'],
 'blog/how-to-shop-for-health-insurance.html':  ['pillar', 'calc', 'sub', 'jobs'],
 'affordable-health-insurance.html':            ['pillar', 'calc', 'sub', 'cost'],
 # the new pieces point at each other
 'cobra-alternatives.html':                     ['calc', 'cost', 'loop', 'drop'],
 'blog/why-is-cobra-so-expensive.html':         ['pillar', 'calc', 'loop', 'drop'],
 'blog/cobra-60-day-loophole.html':             ['pillar', 'drop', 'calc', 'cost'],
 'blog/can-i-drop-cobra-for-marketplace.html':  ['pillar', 'calc', 'loop', 'sep'],
}

H = 'If COBRA is on your desk right now'
SUB = ('The election notice is not a bill you have to pay this week. '
       'It is an option you hold for 60 days, and there is usually something cheaper.')

n = 0
for f, keys in TARGETS.items():
    if not os.path.exists(f):
        print('  missing, skipped:', f); continue
    slug = '/' + f[:-5]
    if slug in red:
        print('  redirect source, skipped:', f); continue
    cards = [C[k] for k in keys if C[k][0] != slug][:4]
    if inject(f, 'cobra-cluster', H, SUB, cards,
              cta='/quote?type=individual', cta_text='Compare against your COBRA quote'):
        n += 1
print('pages wired into the COBRA cluster:', n)

# --- blog index -------------------------------------------------------------
POSTS = [
 ('can-i-drop-cobra-for-marketplace', '/compressed/servicesmeeting.jpg',
  'Person comparing COBRA continuation coverage against a marketplace plan before switching',
  'COBRA | 8 min read',
  'Can I Drop COBRA and Switch to a Marketplace Plan? Three Windows, and the Rest of the Year',
  'Cancelling COBRA because it is too expensive leaves you uninsured until January. Letting it run out does not. Same ending, opposite consequences.'),
 ('cobra-60-day-loophole', '/compressed/business-seminar.jpg',
  'Person holding a COBRA election notice and reviewing the 60-day election period deadline',
  'COBRA | 8 min read',
  'The COBRA 60-Day Loophole: Why Not Replying Is a Strategy',
  'You have 60 days to elect, and coverage backdates to the day you lost it. Free optional insurance for two months &mdash; unless you sign the waiver they sent with it.'),
 ('why-is-cobra-so-expensive', '/compressed/health-insurance-cost-2026-woman.jpg',
  'Person reviewing a COBRA election notice and comparing the premium against marketplace options',
  'COBRA | 7 min read',
  'Why Is COBRA So Expensive? Because You Were Only Ever Seeing Half the Bill',
  'Nothing has been marked up. Your employer was paying most of the premium and COBRA moves the whole bill to you. The arithmetic, and what costs less.'),
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

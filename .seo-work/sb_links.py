# -*- coding: utf-8 -*-
"""Cross-link the small-business cluster: every page reaches the industry hub,
the calculator, the Florida hub and /quote?type=business."""
import sys, glob, re, json; sys.path.insert(0,'.seo-work')
from linkblock import inject
red={r['source'] for r in json.load(open('vercel.json'))['redirects']}

C={
 'elig':  ('/group-health-eligibility-checker','Do You Have Enough Employees?',
           'Free 60-second check: whether you can get a group plan, your real participation number, and the Nov 15-Dec 15 window that waives it.'),
 'ecalc': ('/employer-health-insurance-cost-calculator','What Will It Cost Me Per Employee?',
           'Your monthly cost, what comes out of employee paychecks, and the Section 125 payroll tax you get back.'),
 'hub':   ('/group-health-insurance-by-industry','Group Health Insurance by Industry',
           'Contractors, janitorial, fleets, retail, restaurants and clinics. What changes by trade, and the rating rule most owners get wrong.'),
 'pillar':('/small-business-health-insurance','Small Business Group Health 2027',
           'Group, level-funded and ICHRA compared for a team of 2 to 50, with real per-employee ranges.'),
 'calc':  ('/small-business-health-insurance-calculator','Group Health Cost Calculator',
           'Estimate your monthly cost by employee count, ages and contribution level. Instant, no email required.'),
 'cost':  ('/small-business-health-insurance-cost','Cost Per Employee in 2027',
           'Roughly $350 to $650 per employee per month, what employers typically contribute, and the tax credit most firms miss.'),
 'fl':    ('/florida-small-business-health-insurance','Florida Small Business Health',
           'The 1-50 employee market, Florida participation rules, real 2027 rates and the small business tax credit.'),
 'req':   ('/florida-small-business-health-insurance-requirements','Do I Have to Offer Coverage?',
           'The 50 full-time-equivalent threshold, how to count FTEs, and why common ownership can push you over it.'),
 'ichra': ('/ichra-florida-small-business','ICHRA for Florida Small Business',
           'Reimburse individual premiums tax-free instead of running a group plan. Reaches 1099 people a group plan cannot.'),
 'lf':    ('/level-funded-health-insurance-florida','Level-Funded Plans in Florida',
           'Often 10 to 30 percent under fully insured for a healthy group, with a refund of unused claims.'),
 'oe':    ('/business-open-enrollment-faq','Open Enrollment for Employers',
           'Group renewals do not follow the ACA calendar. What employers need to decide, and when.'),
 'miami': ('/miami-small-business-health-insurance','Group Health in Miami',
           'Every major Miami-Dade carrier compared by a licensed local broker. Free and bilingual.'),
}

# default set, overridden per page below
DEFAULT=['elig','ecalc','hub','pillar']
SPECIAL={
 'group-health-insurance-by-industry.html': ['elig','ecalc','pillar','ichra'],
 'small-business-health-insurance.html':    ['elig','ecalc','hub','cost'],
 'small-business-health-insurance-cost.html':['ecalc','elig','hub','lf'],
 'small-business-health-insurance-calculator.html':['ecalc','elig','pillar','cost'],
 'florida-small-business-health-insurance.html':['hub','miami','req','calc'],
 'florida-small-business-health-insurance-requirements.html':['elig','ecalc','pillar','hub'],
 'ichra-florida-small-business.html':       ['lf','pillar','hub','calc'],
 'level-funded-health-insurance-florida.html':['ichra','pillar','hub','calc'],
 'business-open-enrollment-faq.html':       ['elig','ecalc','pillar','req'],
}
CITY=['elig','ecalc','fl','hub']

SB=[f for f in sorted(glob.glob('*.html')) if re.search(
    r'small-business|business-open-enrollment|group-health-insurance-by-industry|restaurant-health|'
    r'health-insurance-for-(auto-repair|cleaning|construction|dental-offices|hvac|restaurants|retail|salons|trucking-companies|contractors|real-estate)|'
    r'ichra-florida|level-funded|florida-small-business|coral-springs-health', f)]

H='More on group coverage for small business'
SB_SUB=('Group plans for 1 to 50 employees, priced by a licensed independent broker. '
        'Carriers pay our commission, so comparing costs you nothing.')
n=0
for f in SB:
    slug='/'+f[:-5]
    if slug in red: continue
    keys = SPECIAL.get(f) or (CITY if re.search(r'(miami|hialeah|doral|coral-gables|coral-springs|fort-lauderdale|hollywood|miramar|pembroke|plantation|sunrise)',f) else DEFAULT)
    cards=[C[k] for k in keys if C[k][0]!=slug][:4]
    if inject(f,'sb-cluster',H,SB_SUB,cards,cta='/quote?type=business',cta_text='Get group quotes'):
        n+=1
print('small-business pages cross-linked:',n)

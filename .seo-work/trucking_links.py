# -*- coding: utf-8 -*-
"""Item 6: cross-link the trucking cluster; every page points at the plan finder."""
import sys, json, os; sys.path.insert(0,'.seo-work')
from linkblock import inject

red = {r['source'] for r in json.load(open('vercel.json'))['redirects']}

FINDER = ('/owner-operator-plan-finder','Owner-Operator Plan Finder',
          'Six questions about your routes, income and family, and you see which plan type actually fits your operation. No email required.')
CARDS = {
 'main':   ('/truck-driver-health-insurance','Truck Driver Health Insurance 2027',
            'Nationwide PPO networks that work in all 48 states, ACA subsidies on 1099 net income, and real 2027 pricing.'),
 '1099':   ('/1099-truck-driver-health-insurance','1099 Truck Driver Health Insurance',
            'You buy your own plan, but subsidies use net income and premiums are deductible. What that means for your 2027 cost.'),
 'owner':  ('/best-health-insurance-owner-operators','Best Plans for Owner-Operators',
            'The four real coverage options compared on 2027 price, network reach and deductibility.'),
 'fleet':  ('/health-insurance-for-trucking-companies','Benefits for Trucking Companies',
            'What driver benefits cost a small carrier, which structures fit, and what the retention research actually shows.'),
 'occacc': ('/occupational-accident-vs-health-insurance','Occ-Acc vs Health Insurance',
            'Occupational accident covers on-duty accidents only and excludes illness entirely. The gap, side by side.'),
 'dot':    ('/does-health-insurance-cover-dot-physical','Does Insurance Cover DOT Physicals?',
            'Almost never, and the reason is the same across every carrier. What the exam costs and how to cut it legally.'),
 'cost':   ('/truck-driver-health-insurance-cost','What Truck Driver Coverage Costs',
            'Real 2027 monthly numbers by age and household, before and after subsidies.'),
 'deduct': ('/can-truckers-deduct-health-insurance','Can Truckers Deduct Premiums?',
            'The self-employed health insurance deduction, who qualifies, and the mistake that costs drivers the write-off.'),
 'apnea':  ('/blog/sleep-apnea-cpap-cdl-health-insurance','Sleep Apnea and Your CDL',
            'There is no FMCSA sleep apnea rule. What examiners look at, and what insurance pays for a study and a CPAP.'),
 'bp':     ('/blog/cdl-blood-pressure-health-insurance','Blood Pressure and Your Medical Card',
            'The Stage 1, 2 and 3 thresholds that decide whether you get two years, one year, or three months.'),
 'flcarr': ('/trucking-company-health-benefits-florida','Florida Trucking Company Benefits',
            'For carriers running 5 to 50 trucks: what benefits cost and which structures fit a small fleet.'),
 'newauth':('/blog/owner-operator-new-authority-benefits-checklist','New Authority Benefits Checklist',
            'New MC number? The coverage checklist nobody hands you when the paperwork clears.'),
}

PAGES = {
 'truck-driver-health-insurance.html':                    ['1099','owner','occacc'],
 '1099-truck-driver-health-insurance.html':               ['owner','cost','deduct'],
 'best-health-insurance-owner-operators.html':            ['1099','occacc','newauth'],
 'truck-driver-health-insurance-cost.html':               ['main','1099','owner'],
 'truck-driver-health-insurance-florida.html':            ['main','flcarr','owner'],
 'truck-driver-health-insurance-raleigh-nc.html':         ['main','owner','1099'],
 'health-insurance-for-trucking-companies.html':          ['flcarr','main','occacc'],
 'trucking-company-health-benefits-florida.html':         ['fleet','main','newauth'],
 'health-insurance-for-self-employed-truck-drivers.html': ['1099','owner','deduct'],
 'cdl-driver-health-insurance.html':                      ['main','dot','bp'],
 'can-truckers-deduct-health-insurance.html':             ['1099','owner','cost'],
 'aca-vs-private-health-insurance-truck-drivers.html':    ['main','owner','cost'],
 'occupational-accident-vs-health-insurance.html':        ['owner','main','fleet'],
 'does-health-insurance-cover-dot-physical.html':         ['main','apnea','bp'],
 'blog/health-insurance-dot-physical.html':               ['dot','main','bp'],
 'blog/sleep-apnea-cpap-cdl-health-insurance.html':       ['dot','bp','main'],
 'blog/cdl-blood-pressure-health-insurance.html':         ['dot','apnea','main'],
 'blog/company-truck-driver-health-insurance.html':       ['main','1099','fleet'],
 'blog/do-truck-drivers-get-health-insurance.html':       ['main','owner','1099'],
 'blog/1099-vs-w2-truck-driver-benefits.html':            ['1099','main','owner'],
 'blog/can-owner-operators-deduct-health-insurance.html': ['deduct','owner','1099'],
 'blog/owner-operator-new-authority-benefits-checklist.html': ['owner','main','occacc'],
 'blog/small-trucking-company-driver-retention-benefits.html': ['fleet','flcarr','main'],
}

H  = 'More for drivers and carriers'
SB = ('Written for people who run the truck, not for people who sell insurance. '
      'Not sure which plan type fits? Start with the plan finder above.')

n = 0
for path, keys in PAGES.items():
    if not os.path.exists(path):
        print('  MISSING', path); continue
    slug = '/' + path[:-5]
    if slug in red:
        print('  skip (redirect source)', slug); continue
    cards = [FINDER] + [CARDS[k] for k in keys if CARDS[k][0] != slug]
    if inject(path, 'truck-cluster', H, SB, cards[:4],
              cta='/owner-operator-plan-finder', cta_text='Find your plan in 60 seconds'):
        n += 1
print('trucking pages cross-linked:', n)

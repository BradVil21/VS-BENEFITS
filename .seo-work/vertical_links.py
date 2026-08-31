# -*- coding: utf-8 -*-
"""Point the existing clusters at the new sub-trade, city and DOT pages."""
import sys, glob, re, json; sys.path.insert(0, '.seo-work')
from linkblock import inject
red = {r['source'] for r in json.load(open('vercel.json'))['redirects']}

TRUCK = [
 ('/group-health-insurance-for-refrigerated-trucking-companies','Reefer Fleet Group Coverage',
  'Produce lanes leave the state. What a refrigerated carrier needs from a network, and what it costs per driver.'),
 ('/group-health-insurance-for-heavy-haul-trucking-companies','Heavy Haul Fleet Coverage',
  'An older specialist census prices higher - and those drivers are the ones you cannot replace.'),
 ('/group-health-insurance-for-oilfield-trucking-companies','Oilfield Trucking Coverage',
  'Headcount follows rig count. How to build a plan that survives a downturn.'),
 ('/group-health-insurance-for-dump-truck-fleets','Dump Truck Fleet Coverage',
  'A small W-2 core inside a fleet of leased owner-operators, and why home-daily changes the plan.'),
 ('/dot-physical-requirements','DOT Physical Requirements',
  'Blood pressure limits and certification lengths, sleep apnea and CPAP, diabetes, vision and hearing.'),
]
CONSTRUCTION = [
 ('/group-health-insurance-for-general-contractors','General Contractors',
  'Subs are not your employees. The group is the office, and that is an easier case than most GCs expect.'),
 ('/group-health-insurance-for-structural-steel-contractors','Structural Steel and Erection',
  'Prevailing-wage fringe credits, multi-state crews, and what a high hazard class does and does not change.'),
 ('/group-health-insurance-for-concrete-contractors','Concrete Contractors',
  'Seasonal headcount, bilingual enrollment, and the waiting period that keeps a plan alive.'),
 ('/group-health-insurance-for-excavation-contractors','Excavation and Site Prep',
  'Your operators hold CDLs, which puts the DOT physical inside your benefits decision.'),
]
CITY = [
 ('/truck-driver-health-insurance-atlanta-ga','Atlanta, GA Drivers',
  'Southeast lanes leave Georgia fast. Why an Atlanta driver needs national reach - unless they run drayage.'),
 ('/truck-driver-health-insurance-dallas-tx','Dallas-Fort Worth Drivers',
  'Owner-operator country. Subsidies run on net income after deductions, not gross settlements.'),
 ('/truck-driver-health-insurance-memphis-tn','Memphis, TN Drivers',
  'A night-shift freight town, where telehealth and after-hours access matter more than anything else.'),
 ('/truck-driver-health-insurance-indianapolis-in','Indianapolis, IN Drivers',
  'Crossroads of America. More regional runs means you may not need to pay for a national network.'),
]

def pages(pattern_words, extra=()):
    out = []
    for f in sorted(glob.glob('*.html')) + sorted(glob.glob('blog/*.html')):
        if '/' + f[:-5] in red:
            continue
        if re.search(pattern_words, f):
            out.append(f)
    return out + [e for e in extra if e not in out]

n = 0
# 1. trucking cluster -> trucking sub-verticals + DOT hub
for f in pages(r'truck|trucker|otr|cdl|owner-operator|1099-truck|occupational-accident|lease-operator|camioneros'):
    if inject(f, 'vs-truck-verticals', 'Fleet coverage and driver medical certification',
              'Group plans for fleets by segment, plus what actually decides whether a driver keeps a two-year card.',
              [c for c in TRUCK if c[0] != '/' + f[:-5]][:4],
              cta='/quote', cta_text='Get my quote'):
        n += 1
# 2. construction cluster -> construction sub-trades
for f in pages(r'construction|contractor|hvac|excavat|concrete'):
    if inject(f, 'vs-trade-verticals', 'Group coverage by construction trade',
              'What changes trade by trade: fringe credits, seasonal headcount, participation and real per-employee costs.',
              [c for c in CONSTRUCTION if c[0] != '/' + f[:-5]][:4],
              cta='/quote?type=business', cta_text='Get group quotes'):
        n += 1
# 3. driver hubs -> the new city pages
for f in ['truck-driver-health-insurance.html', 'cdl-driver-health-insurance.html',
          'otr-truck-driver-health-insurance.html', 'best-health-insurance-owner-operators.html',
          'dot-physical-requirements.html', 'does-health-insurance-cover-dot-physical.html']:
    try:
        if inject(f, 'vs-driver-cities', 'Coverage by trucking hub',
                  'What changes city to city: which lanes you run, which network you actually need, and state enrollment rules.',
                  CITY[:4], cta='/quote', cta_text='Get my quote'):
            n += 1
    except FileNotFoundError:
        pass
print('pages cross-linked to the new clusters:', n)

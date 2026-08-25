# -*- coding: utf-8 -*-
import sys; sys.path.insert(0,'.seo-work')
from linkblock import inject

C = {
 'guide':   ('/blog/aca-open-enrollment-2027-guide', 'Open Enrollment 2027: Dates by State',
             'The full calendar: Nov 1, 2026 to Jan 15, 2027 on HealthCare.gov, every state exchange deadline, and the Dec 15 cutoff for January 1 coverage.'),
 'faq':     ('/health-insurance-open-enrollment-faq', 'Open Enrollment 2027 FAQ',
             'Short answers to the questions people actually ask: deadlines, special enrollment, subsidies, switching plans, and what help costs.'),
 'missed':  ('/blog/what-happens-if-you-miss-open-enrollment', 'Missed Open Enrollment? What Happens Next',
             'Missing January 15 does not leave you uninsured for the year. Special enrollment periods, Medicaid, and what each fallback really costs.'),
 'biz':     ('/business-open-enrollment-faq', 'Open Enrollment for Employers',
             'Group renewals do not follow the ACA calendar. What small business owners need to decide, and when.'),
 'income':  ('/blog/open-enrollment-2027-income-premium-increase', 'Why Your 2027 Premium Went Up',
             'Enhanced subsidies expired and the income cliff is back at 400% of poverty. What changed and what still lowers your cost.'),
 'oe':      ('/open-enrollment', 'Get Help Enrolling for 2027',
             'A licensed advisor compares every plan on your network and budget, then enrolls you. Carriers pay our commission, so it costs you nothing.'),
 'calc':    ('/aca-subsidy-calculator', 'ACA Subsidy Calculator',
             'Estimate your 2027 premium tax credit before you enroll, so your income estimate does not cost you at tax time.'),
 'fl':      ('/florida-health-insurance-answers', 'Florida Health Insurance Answers',
             'Thirty sourced questions on Florida coverage, the Medicaid gap, and South Florida networks.'),
}

PLAN = {
 'blog/aca-open-enrollment-2027-guide.html':            ('oe-hub-guide',  ['faq','missed','calc','income']),
 'health-insurance-open-enrollment-faq.html':           ('oe-hub-faq',    ['guide','missed','calc','oe']),
 'blog/what-happens-if-you-miss-open-enrollment.html':  ('oe-hub-missed', ['guide','faq','oe','calc']),
 'business-open-enrollment-faq.html':                   ('oe-hub-biz',    ['guide','faq','oe','fl']),
 'blog/open-enrollment-2027-income-premium-increase.html':('oe-hub-inc',  ['guide','faq','calc','missed']),
 'open-enrollment.html':                                ('oe-hub-oe',    ['guide','faq','missed','calc']),
}

H  = 'Open Enrollment 2027 &mdash; the rest of the answers'
SB = ('Enrollment for 2027 coverage runs November 1, 2026 to January 15, 2027; enroll by December 15 for a January 1 start.')

n=0
for path,(marker,keys) in PLAN.items():
    if inject(path, marker, H, SB, [C[k] for k in keys]):
        n+=1; print('  linked', path)
print('OE hub blocks injected:', n)

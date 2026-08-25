# -*- coding: utf-8 -*-
"""Rewrite <title> + meta description (and og/twitter mirrors) on pages ranking 4-20
with low CTR. Answer-first, date-forward, <=60 char titles, ~150-158 char descriptions.
All figures below are taken from the pages' own body copy - nothing invented."""
import re, sys

PAGES = {
 'blog/aca-open-enrollment-2027-guide.html': (
   "Open Enrollment 2027: Nov 1 – Jan 15 (Dates by State)",
   "Open enrollment for 2027 coverage runs Nov 1, 2026 to Jan 15, 2027 on HealthCare.gov. Enroll by Dec 15 for a January 1 start. Every state's deadline."),
 'health-insurance-open-enrollment-faq.html': (
   "Open Enrollment 2027 FAQ: Dates, Deadlines, Subsidies",
   "2027 open enrollment runs Nov 1, 2026 to Jan 15, 2027. Enroll by Dec 15 for January 1 coverage. Answers on deadlines, special enrollment and subsidies."),
 'open-enrollment.html': (
   "Open Enrollment 2027: Enroll by Dec 15 for Jan 1 Start",
   "2027 open enrollment runs Nov 1, 2026 through Jan 15, 2027. Enroll by Dec 15 for coverage starting January 1. A licensed advisor compares plans free."),
 'blog/what-income-counts-for-aca-subsidies.html': (
   "What Income Counts for ACA Subsidies? MAGI in 2027",
   "ACA subsidies use MAGI: adjusted gross income plus tax-exempt interest and untaxed Social Security. What counts, what doesn't, and how 1099 earners estimate it."),
 'blog/how-much-does-health-insurance-cost-2026.html': (
   "How Much Does Health Insurance Cost in 2026? Real Prices",
   "The benchmark silver plan averages about $625 a month before subsidies in 2026, and roughly $752 at age 40. What drives your price and how to pay less."),
 'blog/health-insurance-dot-physical.html': (
   "Do You Need Health Insurance to Pass a DOT Physical?",
   "No. You don't need insurance to pass a DOT physical and it won't pay for the exam. But coverage is what keeps your medical card renewing year after year."),
 'does-health-insurance-cover-dot-physical.html': (
   "Does Health Insurance Cover DOT Physicals? (2026 Answer)",
   "Almost never - standard health plans exclude DOT physicals as employment exams. What the exam really costs in 2026, and the HSA and deduction moves drivers miss."),
 'services.html': (
   "Health Insurance We Broker: ACA, Group, Dental, Vision",
   "ACA marketplace, private PPO, small group, family, dental and vision - compared by a licensed broker at no cost to you. Carriers pay our commission, not you."),
 'health-insurance-for-hvac-companies.html': (
   "Health Insurance for HVAC Companies: 2027 Costs & Plans",
   "Group health for HVAC companies runs about $350 to $650 per employee per month. Which structures fit a 2-100 person shop, and free setup from a licensed broker."),
 'health-insurance-for-auto-repair-shops.html': (
   "Health Insurance for Auto Repair Shops: 2027 Costs",
   "Group health built for repair shops and their technicians: what it costs per employee in 2027, which plan structures fit a small shop, and free setup help."),
 'health-insurance-for-salons-and-spas.html': (
   "Health Insurance for Salons, Spas and Barbershops 2027",
   "Booth renters, commission stylists and W-2 staff each need a different answer. Coverage options and 2027 costs for salon and spa owners, explained free."),
 'blog/aca-subsidies-ended-2026-what-to-do.html': (
   "ACA Subsidies Ended: Why Your 2026 Premium Jumped",
   "Enhanced subsidies expired at the end of 2025 and premiums jumped for millions. Why it happened, who is hit hardest, and the moves that still cut your cost."),
 'refer-and-earn.html': (
   "Refer and Earn: Get Paid for Health Insurance Referrals",
   "Send someone who needs coverage and get paid when they enroll. No license, no selling, free to join. How the VS Health Benefits referral program works."),
 'blog/what-happens-if-you-miss-open-enrollment.html': (
   "Missed Open Enrollment? Here's How to Still Get Covered",
   "Missing the Jan 15 deadline doesn't leave you uninsured for the year. Special enrollment periods, Medicaid, short-term options and what each one really costs."),
 'blog/health-insurance-while-living-on-the-road.html': (
   "Health Insurance for Van Life and Full-Time Travel",
   "Living on the road means your plan is tied to a home state. How to pick a domicile, choose a nationwide network, and avoid surprise out-of-network bills."),
}

def set_meta(s, tag_pat, value, label):
    new, n = re.subn(tag_pat, lambda m: m.group(1) + value + m.group(3), s, count=1)
    return new, n

changed = 0
for f, (title, desc) in PAGES.items():
    try:
        s = open(f, encoding='utf-8').read()
    except FileNotFoundError:
        print('MISSING', f); continue
    orig = s
    if len(title) > 60: print('  !! title %d chars: %s' % (len(title), f))
    if not (120 <= len(desc) <= 160): print('  !! desc %d chars: %s' % (len(desc), f))

    s, _ = set_meta(s, r'(<title>)(.*?)(</title>)', title, 'title')
    s, _ = set_meta(s, r'(<meta name="description" content=")(.*?)(")', desc, 'desc')
    s, _ = set_meta(s, r'(<meta property="og:title" content=")(.*?)(")', title, 'ogt')
    s, _ = set_meta(s, r'(<meta property="og:description" content=")(.*?)(")', desc, 'ogd')
    s, _ = set_meta(s, r'(<meta name="twitter:title" content=")(.*?)(")', title, 'twt')
    s, _ = set_meta(s, r'(<meta name="twitter:description" content=")(.*?)(")', desc, 'twd')

    if s != orig:
        open(f, 'w', encoding='utf-8').write(s); changed += 1
print('pages updated:', changed, '/', len(PAGES))

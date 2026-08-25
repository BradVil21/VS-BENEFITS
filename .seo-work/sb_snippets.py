# -*- coding: utf-8 -*-
"""Retitle the small-business cluster to match the query syntax we actually rank for.
GSC shows the demand is phrased "group health insurance for [trade]" and
"group health insurance [city]" - not "health insurance for [trade]".
Titles <=60 chars, descriptions 140-158."""
import re

PAGES = {
 # ---- industry / trade pages: lead with "Group Health Insurance for X" ----
 'health-insurance-for-cleaning-companies.html': (
   "Group Health Insurance for Janitorial & Cleaning Firms",
   "Group health for janitorial, industrial cleaning and building services crews: part-time eligibility, high turnover, and real 2027 per-employee costs."),
 'health-insurance-for-construction-companies.html': (
   "Group Health Insurance for Construction Contractors",
   "Group coverage for general, excavation, bridge and tunneling contractors: seasonal crews, 1099 vs W-2, and what it costs per employee in 2027."),
 'health-insurance-for-contractors.html': (
   "Health Insurance for Independent Contractors (1099)",
   "Contractors buy their own coverage but subsidies use net income and premiums are deductible. Your 2027 options compared, with real monthly numbers."),
 'health-insurance-for-retail-businesses.html': (
   "Group Health Insurance for Retail Stores & Chains",
   "Group coverage for single stores and multi-location retailers: part-time eligibility, seasonal staff, and what it really costs per employee in 2027."),
 'health-insurance-for-trucking-companies.html': (
   "Group Health Insurance for Trucking Companies 2027",
   "Group health for carriers and fleets - refrigerated, flatbed, dump, oilfield and drayage. Licensed in 40+ states, bilingual enrollment, real 2027 rates."),
 'health-insurance-for-restaurants.html': (
   "Group Health Insurance for Restaurants & Food Service",
   "Group health for restaurants: part-time rules, high turnover, tipped-wage income and the ACA lookback. Real per-employee 2027 costs, free setup."),
 'health-insurance-for-dental-offices.html': (
   "Group Health Insurance for Dental Offices & Practices",
   "Group health for dental practices: small-team plans, owner-dentist options and real 2027 per-employee rates. Set up free by a licensed broker."),
 'health-insurance-for-hvac-companies.html': (
   "Group Health Insurance for HVAC Companies (2027 Cost)",
   "Group health for HVAC companies runs about $350 to $650 per employee per month. Which structures fit a 2-100 person shop, and free setup help."),
 'health-insurance-for-auto-repair-shops.html': (
   "Group Health Insurance for Auto Repair Shops 2027",
   "Group health built for repair shops and their technicians: what it costs per employee in 2027, which structures fit a small shop, and free setup."),
 'health-insurance-for-salons-and-spas.html': (
   "Group Health for Salons, Spas and Barbershops 2027",
   "Booth renters, commission stylists and W-2 staff each need a different answer. Coverage options and 2027 costs for salon and spa owners, explained free."),
 'health-insurance-for-real-estate-agents.html': (
   "Health Insurance for Real Estate Agents (1099) 2027",
   "Agents are 1099, so subsidies use net commission income and premiums are deductible. What that means for your 2027 cost, with real monthly numbers."),

 # ---- pillar + cost ----
 'small-business-health-insurance.html': (
   "Small Business Group Health Insurance 2027 | 2-50 Staff",
   "Set up 2027 group health for a team of 2 to 50. Group, level-funded and ICHRA compared by an independent broker who shops the whole market. Free."),
 'small-business-health-insurance-cost.html': (
   "Small Business Health Insurance Cost Per Employee 2027",
   "Group health runs roughly $350 to $650 per employee per month in 2027. What employers typically contribute, and the tax credit most small firms miss."),

 # ---- Florida + South Florida cities: lead with "Group Health Insurance" ----
 'florida-small-business-health-insurance.html': (
   "Group Health Insurance for Florida Small Business 2027",
   "Group health for Florida employers: the 1-50 employee market, state participation rules, real 2027 rates and the small business tax credit. Free setup."),
 'miami-small-business-health-insurance.html': (
   "Group Health Insurance Miami, FL | Small Business Plans",
   "Group health insurance for Miami small businesses, 2 to 50 employees. Every major Miami-Dade carrier compared by a licensed local broker. Free, bilingual."),
 'fort-lauderdale-small-business-health-insurance.html': (
   "Group Health Insurance Fort Lauderdale | Small Business",
   "Group health for Fort Lauderdale employers with 2 to 50 employees. Every major Broward County carrier compared by a licensed local broker, at no cost."),
 'coral-gables-small-business-health-insurance.html': (
   "Group Health Insurance Coral Gables, FL | 2-50 Employees",
   "Group health for Coral Gables businesses, 2 to 50 employees, from about $400 per employee per month. Every Miami-Dade carrier compared free. Bilingual."),
 'doral-small-business-health-insurance.html': (
   "Group Health Insurance Doral, FL | Small Business Plans",
   "Group health for Doral employers, 2 to 50 employees. Built for the trade, logistics and import businesses around Doral. Free, bilingual, every carrier."),
 'hialeah-small-business-health-insurance.html': (
   "Group Health Insurance Hialeah, FL | Small Business",
   "Group health for Hialeah businesses with 2 to 50 employees. Bilingual enrollment and every major Miami-Dade carrier compared, at no cost to you."),
 'hollywood-fl-small-business-health-insurance.html': (
   "Group Health Insurance Hollywood, FL | Small Business",
   "Group health for Hollywood, FL employers with 2 to 50 employees. Every major Broward carrier compared by a licensed local broker. Free and bilingual."),
 'miramar-small-business-health-insurance.html': (
   "Group Health Insurance Miramar, FL | Small Business",
   "Group health for Miramar employers with 2 to 50 employees. Every major Broward County carrier compared by a licensed local broker, at no cost to you."),
 'pembroke-pines-small-business-health-insurance.html': (
   "Group Health Insurance Pembroke Pines, FL | Employers",
   "Group health for Pembroke Pines businesses with 2 to 50 employees. Every major Broward carrier compared free by a licensed local broker. Bilingual."),
 'plantation-small-business-health-insurance.html': (
   "Group Health Insurance Plantation, FL | Small Business",
   "Group health for Plantation, FL employers with 2 to 50 employees. Every major Broward County carrier compared by a licensed local broker, at no cost."),
 'sunrise-small-business-health-insurance.html': (
   "Group Health Insurance Sunrise, FL | Small Business",
   "Group health for Sunrise, FL businesses with 2 to 50 employees. Every major Broward carrier compared free by a licensed, bilingual local broker."),
 'coral-springs-health-insurance.html': (
   "Group Health Insurance Coral Springs, FL | Employers",
   "Group and individual health insurance for Coral Springs, FL. Every major Broward County carrier compared by a licensed local broker, at no cost to you."),
 'restaurant-health-insurance-miami-fort-lauderdale.html': (
   "Restaurant Group Health Insurance Miami & Fort Lauderdale",
   "Group health for South Florida restaurants: tipped wages, part-time rules and the ACA lookback, plus what it really costs per employee in 2027."),
}

def setm(s, pat, val):
    return re.subn(pat, lambda m: m.group(1)+val+m.group(3), s, count=1)[0]

bad=0; done=0
for f,(t,d) in PAGES.items():
    try: s=open(f,encoding='utf-8').read()
    except FileNotFoundError: print(' MISSING',f); continue
    if len(t)>60: print('  !! title %d: %s'%(len(t),f)); bad+=1
    if not 130<=len(d)<=160: print('  !! desc %d: %s'%(len(d),f)); bad+=1
    o=s
    s=setm(s, r'(<title>)(.*?)(</title>)', t)
    s=setm(s, r'(<meta name="description" content=")(.*?)(")', d)
    s=setm(s, r'(<meta property="og:title" content=")(.*?)(")', t)
    s=setm(s, r'(<meta property="og:description" content=")(.*?)(")', d)
    s=setm(s, r'(<meta name="twitter:title" content=")(.*?)(")', t)
    s=setm(s, r'(<meta name="twitter:description" content=")(.*?)(")', d)
    if s!=o: open(f,'w',encoding='utf-8').write(s); done+=1
print('pages updated: %d/%d | length warnings: %d'%(done,len(PAGES),bad))

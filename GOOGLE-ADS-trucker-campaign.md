# Google Ads: Trucker Health Insurance Leads

Health insurance only. No dental or vision anywhere in this campaign.

## What the account shows (Sep 9 – Oct 8, 2026, account 294-975-7547)
- Both campaigns are **paused**. "FL Health Insurance - Search Leads" also shows "All ads limited by policy". Check the policy detail before launching (health insurance ads may need certification).
- Spend: $215.95. Clicks: 78. Conversions: 4 (3 calls, 1 form). Cost per conversion: $53.99.
- Top search terms were waste, e.g. "costco health insurance plans for members" (21 clicks, 0 leads). The campaign was broad and had no trucker targeting.
- The form lead tag had been firing only on the final submit. **Fixed in vs-conversions.js:** trucker leads now count at the phone step, which is when the lead lands in the CRM. Google dedupes this per click.

## Campaign setup
- **Type:** Search only. Turn off Display Network and Search Partners.
- **Name:** Trucker Health - Search Leads.
- **Budget:** $30–40/day. Bidding: Maximize Conversions. After 30+ conversions, switch to Target CPA at about 1.2× your actual cost per lead.
- **Goal:** Quote Form Lead plus Calls from ads (1). Remove the duplicate goals "Calls from ads" and "Phone Call Click" so leads are not counted twice.
- **Locations:** these 33 states only, using "Presence: people in or regularly in". Do not use "interest in".
  AL AZ AR CO FL GA IL IN IA KS KY LA MD MI MN MS MO MT NE NV NC ND OH OK SC SD TN TX UT VA WV WI WY
- **Schedule:** run all hours. Drivers search at night and on weekends. Raise bids +20% on 5am–9am and 6pm–11pm after 2 weeks of data.
- **Devices:** mobile-first. Most drivers search from the cab.
- **Final URL:** https://vshealthbenefits.com/truckers/quote
- **Tracking template / final URL suffix:** utm_source=google&utm_medium=cpc&utm_campaign=trucker-health&utm_term={keyword}

## Ad groups and keywords (phrase and exact match only, no broad match at first)

**1. Truck driver health insurance**
"health insurance for truck drivers", [health insurance for truck drivers], "truck driver health insurance", "trucker health insurance", "health insurance for truckers", "otr driver health insurance", "cdl driver health insurance"

**2. Owner-operators**
"owner operator health insurance", [owner operator health insurance], "health insurance for owner operators", "best health insurance for owner operators", "lease operator health insurance"

**3. 1099 / self-employed drivers**
"1099 truck driver health insurance", "self employed truck driver health insurance", "independent truck driver health insurance", "health insurance for independent contractors trucking"

**4. Spanish** (Spanish ads; same landing page for now)
"seguro medico para camioneros", "seguro de salud para traileros", "seguro medico para choferes de camion"

Add trucker search terms that convert as exact match each week.

## Negative keywords (campaign level)
dental, vision, eye, glasses, contacts, vsp, costco, sams club, aarp, medicare, truck insurance, commercial truck insurance, auto insurance, cargo, liability, physical damage, bobtail, occupational accident, workers comp, jobs, hiring, salary, pay, cdl school, cdl training, dot physical near me, drug test, company benefits login, login, phone number, union, teamsters, free, cheap trucks, rental

Review search terms every 3–4 days for the first month and add new negatives.

## Responsive search ad (one per ad group, adapt headline 1 to the ad group)
**Headlines:** each is 30 characters or fewer
- Health Insurance for Truckers
- Owner-Operator Health Plans
- Plans That Work on the Road
- Nationwide PPO Networks
- Free Quote, Licensed Advisor
- 1099 Driver Health Coverage
- Tax Credits Can Cut Premiums
- Quote in About 60 Seconds
- Licensed in 33 States
- CDL Driver Health Insurance
- No Cost to Use an Advisor
- Built for OTR Drivers
- Rated 5.0 on Google
- Get Covered Before You Roll
- Talk to a Licensed Advisor

Pin "Health Insurance for Truckers" (or the ad group's version) to position 1.

**Descriptions:** each is 90 characters or fewer
- Owner-operators and 1099 drivers: compare plans with PPO networks that travel with you.
- Answer 4 quick questions. A licensed advisor reviews your quote, usually the same day.
- Many drivers qualify for tax credits. We check yours free. Carriers pay us, not you.
- Plans are priced by your home ZIP, not where you park. Get a free quote from the road.

## Assets
- **Call asset:** (954) 825-1009, tracked as "Calls from ads (1)". Schedule it for staffed hours only.
- **Sitelinks:**
  - Owner-Operator Plans → /best-health-insurance-owner-operators
  - Plans by State → /truck-driver-health-insurance#by-state
  - Does It Cover DOT Physicals? → /does-health-insurance-cover-dot-physical
  - Fleet Coverage → /health-insurance-for-trucking-companies
- **Callouts:** Licensed Advisor Review, Nationwide PPO Options, Same-Day Quotes, No Fee to You, English y Español.
- **Structured snippet:** Types = Owner-Operator, Lease Operator, Company Driver, 1099 Driver.
- **Lead form asset:** do NOT use it. Leads stay on the site funnel, which captures the phone number at step 4.

## Weekly checklist
1. Check search terms. Add negatives, and add winning trucker terms as exact match.
2. Compare cost per lead by ad group. Move budget to the ad group that wins.
3. Check that GHL leads tagged trucker / trucker-quote-partial with src google match the Ads conversion count.
4. Call every partial lead within 5 minutes. Speed to lead is the biggest conversion lever.

# Trucker campaign rebuild (2026-11-25), built from GOOGLE-ADS-PLAYBOOK.md
Based on the all-time search terms export (search-terms-all-time-2026-11-25.csv).

## Budget: $50/day (~$1,520/month), split 80/20
| Campaign | Daily | What it holds |
|---|---|---|
| Trucker Core - Exact | $40 | The main ("coliseum") keywords only |
| Trucker Owner-Op & 1099 - Exact | $10 | Owner-operator / independent / 1099 driver keywords |
Later (only after Core reaches ~80% impression share): $10/day trucking-company test, then 5-10% on competitor terms (OOIDA, American Trucker Advantage).

## Settings (both campaigns)
- Search only. Display Network OFF, Search Partners OFF. Auto-apply recommendations OFF (Admin > Recommendations).
- Locations: Florida + Georgia, "Presence: people in or regularly in". Add states only once impression share is 80%+.
- Bidding: Manual CPC (bids you control). Start the Core keywords at $12 and the Owner-Op keywords at $10.
  Raise 10-20% a day until the ads show at the top and the budget is spent. Switch to Max Conversions or Target CPA only after 30+ conversions.
- Schedule: all hours. Devices: all (mobile first; drivers search from the cab).
- Final URL: https://www.vshealthbenefits.com/quote?type=individual&niche=trucking
- Final URL suffix: utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_term={keyword}
- Conversions: Quote Form Lead (counts at the phone step) + Calls from ads 60s+. Remove duplicate call goals.

## Keywords (EXACT match only)
Core: [health insurance for truck drivers] [truck driver health insurance] [medical insurance for truck drivers]
[truck driver medical insurance] [health insurance for truckers] [truckers health insurance] [truckers medical insurance]
[best health insurance for truck drivers] [best medical insurance for truck drivers] [otr driver health insurance] [cdl driver health insurance]
Owner-Op & 1099: [owner operator health insurance] [health insurance for owner operators] [health insurance for owner operator truck drivers]
[health insurance for independent truckers] [independent truckers health insurance] [health insurance for 1099 truck drivers] [1099 truck driver health insurance]

## Negatives
Paste negatives-2026-11-25.txt at the campaign level, plus: "cdl school" "cdl training" "dot physical" "truck insurance" "commercial truck insurance"
"cargo" "liability" "bobtail" "occupational accident" "workers comp" "jobs" "hiring" "salary" "rate per mile" "landstar" "swift" "statefarm"
"state farm" "nationwide insurance" "chubb" "hartford" "great west" "liberty mutual" "aaa" "ichra" "deductible meaning" "what is"

## Responsive search ad (one per ad group, plus a variant later)
Headlines (30 max): Truck Driver Health Insurance (pin 1) | Health Insurance for Truckers | Lost Your Company Plan? | Nationwide PPO for Drivers |
See Doctors in Any State | Telehealth From the Cab | Licensed Agent for Truckers | Owner-Operators Welcome | Covered Between Carriers |
OTR Drivers: Read This First | Plans for 1099 Drivers | Coverage for Your Family Too | Talk to a Real Person | Text or Call, Your Choice | Get a Free Quote Today
Descriptions (90 max):
1. Drivers who lose a company plan have options. Compare PPO plans with a licensed agent.
2. Nationwide PPO options, telehealth and urgent care that work wherever your route goes.
3. Owner-operator or company driver? Get a free quote and a plain-English plan review.
4. We help truckers get covered every day. Text or call. Quote in about 2 minutes.
Owner-Op ad group: pin "Owner-Operators Welcome" or "Plans for 1099 Drivers" in position 1 instead.

## Assets
- Sitelinks: Get a Trucker Quote (/quote?type=individual&niche=trucking) | Owner-Operator Guide (/best-health-insurance-owner-operators) |
  1099 Drivers (/1099-truck-driver-health-insurance) | Can Truckers Deduct It? (/can-truckers-deduct-health-insurance)
- Callouts: Nationwide PPO Options | Licensed Agents | Text or Call | No Cost to Compare | English & Spanish
- Call asset: (954) 866-6872, scheduled Mon-Fri 8am-8pm, Sat 10am-5pm ET (off Sundays).

## Routine (playbook #3 and #4)
- Daily, 10 min: if the budget isn't spent, raise bids 10-20%. Add negatives from the search terms. Check top-of-page rate.
- Every Monday: send Claude the search terms. Add winners as exact keywords and block the junk.
- First Monday of each month: sold policies by keyword. Move budget to what sells.
- Goals for the first 30 days: top impression share 70%+ on Core, cost per lead under $60, every lead called within 5 minutes.

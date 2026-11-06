# Google Ads changes, 2026-11-01 (prepared by Claude; account changes are for Bradley to apply)

## Done in the website / files
1. Final URLs: every trucker keyword, ad and the "2027 Rate Check" sitelink now point straight to
   /trucking-health-quote (was /truckers/quote -> 301). CSVs + vs-campaign-builder.js updated.
2. /trucking-health-quote hero now asks ZIP + mobile number (with TCPA text). On submit:
   - lead saved to /api/lead-draft (portal card + GHL contact, tags trucker, lp-capture)
   - Google Ads "Quote Form Lead" conversion fires with transaction_id = "ph<phone>"
   - continues to /quote with the phone prefilled
   Before: a conversion only counted after all 6 funnel steps. Drivers who quit at step 2-5 were invisible to Ads.
3. Open Enrollment line in the hero (auto: Nov 1 - Dec 15 / Dec 16 - Jan 15 / hidden after).

## Apply in Google Ads (Bradley)
1. Goals > Conversions > "Quote Form Lead" > Edit > Count: ONE (so the landing capture + the funnel finish for the
   same person count once). Keep it Primary.
2. Find & replace final URLs: truckers/quote -> trucking-health-quote (Keywords, Ads, Sitelink "2027 Rate Check").
3. Trucker budget: $15/day buys ~1-2 clicks at $8-15 CPC. For Open Enrollment raise to $30-40/day for Nov 1 - Dec 15.
4. After ~15 conversions in 30 days, switch Trucker bidding to Maximize conversions (it learns from the new lead event).
5. Weekly: Search terms report -> add irrelevant terms as negatives (CDL schools, truck insurance, jobs, Medicare).
6. Ad schedule: check the hour report; truckers search early morning and evenings - add bid boosts there.

## Check Nov 8
Conversions per day (should rise from ~0), cost per conversion, % of trucker leads that answer the phone.

# Google Ads changes, 2026-11-06 (Trucker Health - OE 2027)

Script "VS Trucker Tighten (Nov 6)" (source vs-trucker-tighten-2026-11-06.js), run 10:49 AM.

Last 30 days before the change: Search $225.32 / 18 clicks / 5 conversions; Display $91.94 / 78 clicks / 0 conversions.

- Display Network OFF (Google Search + search partners stay on).
- Paused phrase "truck driver health insurance" ($61.79, 6 clicks, 0 conv). Exact version added instead.
- Exact keywords added: [health insurance for truck drivers], [truck driver health insurance], [health insurance for truckers],
  [trucker health insurance] (Truck Driver group); [owner operator health insurance], [health insurance for owner operators],
  [owner operator medical insurance] (Owner Operator); [health insurance for independent truckers],
  [independent truck driver health insurance] (1099 Driver).
- Left on: broad "owner operator health insurance" (1 conv), phrase "1099 truck driver health insurance" (1 conv),
  phrase "health insurance for truckers" ($19, under the $25 cut-off), exact "health insurance for owner operator truck drivers".
- Budget $50/day. Bidding is Maximize conversions.
- Check Nov 10-13: cost per lead on Search only; if a phrase keyword passes $25 with 0 leads, pause it the same way.

## 11:43 AM: trucker ads land on the quote form
Script "VS Trucker Ads to Quote Form (Nov 6)" (source vs-trucker-ads-to-quote-form-2026-11-06.js).
- All 26 ads in Trucker Health - OE 2027 (11 enabled) now go to
  https://www.vshealthbenefits.com/quote?type=individual&niche=trucking (was /trucking-health-quote and a few blog pages).
  The "Trucking Company (Group)" ad goes to /quote?type=business&niche=trucking so fleet owners still get the business form.
- No ZIP in any ad, sitelink or URL suffix (none had one; the script strips zip= if it ever appears).
- Sitelinks "Get a Trucker Quote" and "2027 Rate Check" now also open the quote form. The education sitelinks
  (deductible, DOT physical, owner-operator plans, nationwide PPO...) still open their pages.
- Campaign tracking suffix unchanged: utm_source=google&utm_medium=cpc&utm_campaign=trucker-oe-2027&utm_term={keyword}.
- Rule: ads -> short form. Organic / blog / social -> /trucking-health-quote -> form.
  /trucking-health-quote got a "Start my trucker quote ->" button under the ZIP box (same URL, no ZIP).

## 12:40 PM: 8 certified states check (script "VS Trucker 8-State Check (Nov 6)")
- Trucker Health - OE 2027 targets exactly the 8 states: Florida, Georgia, Illinois, Kentucky, Maryland, Missouri, Ohio, Texas.
  Location option: people in or regularly in (PRESENCE). Nothing was missing, nothing added.
- Last 7 days by state (impr / clicks / cost): FL 1,741 / 25 / $151.36; TX 2,675 / 20 / $29.78; IL 1,281 / 14 / $12.27;
  GA 1,206 / 11 / $43.46; OH 915 / 9 / $27.52; MO 511 / 7 / $8.14; MD 496 / 2 / $4.33; KY 404 / 4 / $3.77.
- Ad copy said "Florida" (e.g. "Florida Truck Driver Plans", "Florida truck drivers: compare...", "Licensed Florida Advisor").
  Edited in place on 17 ads so the copy fits all 8 states: "Truck Driver Plans by State", "Trucker Plans in Your State",
  "Licensed Health Advisor", "Truck drivers: compare PPO and Marketplace plans with a licensed broker. Free."
  Ads keep their IDs and history; Google re-reviews the edited text (usually same day).

## 1:12 PM: Florida + Georgia focus (script "VS Trucker FL + GA Focus (Nov 6)", source vs-trucker-fl-ga-focus-2026-11-06.js)
- Checked first: Display off, exact [health insurance for truck drivers] ENABLED, budget $50/day.
- Florida +30%, Georgia +30% location bid adjustment.
- Illinois, Kentucky, Maryland, Missouri, Ohio, Texas taken out of targeting (paused). Re-add them as locations to turn back on.
- Bidding is Maximize conversions, which ignores location bid adjustments; removing the 6 states is what moves the $50 to FL/GA.
  The +30% applies if bidding goes back to Maximize clicks / manual CPC.
- Raise the budget only after FL/GA hit the $50 cap most days AND cost per lead stays under ~$50-60.

## 1:20 PM: new campaign "Private Health - No Subsidy FL" (script "VS Private Health - No Subsidy FL (Nov 6)",
source vs-private-health-no-subsidy-fl-2026-11-06.js). Campaign ID 24438705086. Trucker untouched at $50/day.
- ON. $20/day. Maximize clicks, $5 max CPC (switch to Maximize conversions after ~15-20 form leads).
- Google Search only: search partners OFF, Display OFF. Florida only (people in / regularly in). English.
- Lands on https://www.vshealthbenefits.com/quote?type=individual&niche=private (no ZIP). niche=private tags the lead
  "private-ppo" in the portal. Tracking: utm_campaign=private-no-subsidy-fl, utm_term={keyword}. Display path: /Private-Plans.
- Ad groups: Private / PPO (4 exact + 2 phrase), No Subsidy / Over Income (3 exact + 2 phrase),
  Self-Employed Private (2 exact + 2 phrase). Keywords exactly as specified.
- 32 campaign negatives (phrase): medicaid, medicare, marketplace, healthcare.gov, obamacare, obama care, aca, open enrollment,
  subsidy calculator, free/cheap health insurance, short term, dental, vision, chip, covered california, florida blue medicaid,
  low income, apply for subsidy, how to get a subsidy, jobs, login, claims, other insurance types.
  The shared "VS Leads - Negatives (Nov 3)" list is NOT attached: it blocks every search with "subsidy", which would block
  the No Subsidy ad group.
- One RSA per group: 11 headlines (the requested ones + 3 per group), 4 descriptions.
  Changes from the brief: "Call 954-825-1009" -> "Call a Licensed Advisor" (Google rejects phone numbers in ad text; the
  account call asset shows the number). "Free Quote · Licensed Advisor" -> "Free Quote, Licensed Advisor" (symbol policy).
  "Private Health Plans in Florida" (31) -> "Private Health Plans in FL"; "Plans for Individuals & Families" (32) ->
  "Individual & Family Plans" (30-character limit). First description shortened to fit 90 characters.
- Rules: check after 3-5 days, pause any keyword with 10+ clicks and 0 conversions. If cost per lead is still bad after
  ~$150-200 with no quality leads, pause and retune. Add Georgia only after Florida converts at a CPL you like.
- Do not turn back on as-is: Individual - OE 2027 FL, No Subsidy - High Earners (Top ZIPs) / (8 States).

## 1:33 PM: no-subsidy sitelinks + quote-form URLs (script "VS No Subsidy Sitelinks + Quote URLs (Nov 6)",
source vs-no-subsidy-sitelinks-2026-11-06.js)
- All 20 ads in Private Health - No Subsidy FL (3, already right) and the paused No Subsidy - High Earners campaigns (17, were
  /private-health-insurance) now land on https://www.vshealthbenefits.com/quote?type=individual&niche=private. No zip=, no from=.
  The two paused campaigns stay paused.
- Private Health - No Subsidy FL: 6 sitelinks (Get a Free Quote -> quote form; Private vs Marketplace, Watch: Full-Price Costs,
  Who Private Plans Fit, How It Works -> sections of /private-health-insurance; Self-Employed Plans) and 5 callouts
  (No Fee to You, Licensed Advisor, Apply Any Month, PPO Networks, Free Quote). Account-level call button applies.
- Website: /private-health-insurance got a "Start my private plan quote ->" button under the ZIP box, same URL, no ZIP.
  The page's other buttons keep from=... (organic tracking only; not used in ads).

## 1:55 PM: Marketing tab "What to do next" checked against the live account
- Live campaigns only (Trucker, Private Health - No Subsidy FL): the only search terms with spend and 0 conversions are
  "truck driver health insurance" ($26.43) and "health insurance for owner operator truck drivers" ($19.71). Both are our own
  keywords, so nothing to add as negatives. The rest of the $74 was paused/removed campaigns (group insurance, Medicare 2027...).
- "Limited by policy": 0 running ads are limited. The 12 running ads show "under review" because their text/URLs were edited today.
- Quality Score <= 4 in live campaigns: "health insurance for truckers" (3) and "health insurance for independent truckers" (4).
  Kept on (core terms); recheck after the new ads are reviewed.
- Texas / Illinois: already out of targeting since 1:12 PM.
- admin.html: the tips now only use running campaigns, running ads and targeted states; search terms that are our own keywords
  are not flagged as waste; the state bid tip notes that Maximize conversions ignores location bids.

# Google Ads: Trucker-Only Plan (Nov 1 2026)

Decision: every ad dollar goes to truck drivers. Small Biz and Individual campaigns are paused (not deleted).
Why: Search Console shows ~5,000 trucker impressions/month with no page-1 organic ranking yet, so ads are the fastest way in;
ACA-subsidy searches already arrive free (calculator ranks page 1) and cost the most to buy.

## Run it (10 minutes)
1. Google Ads > Tools > Bulk actions > Scripts > + New script. Name it "VS Trucker Only (Nov 1)".
2. Paste all of `vs-trucker-only-2026-11-01.js`. Authorize.
3. Click **Preview**. Read the log: it should list paused campaigns, the budget, 5 new ads, keywords and negatives. No "LENGTH ERRORS".
4. Click **Run**. Safe to re-run: it skips anything already done.

## What the script changes
| | Before | After |
|---|---|---|
| Individual - OE 2027 FL | ON, $30/day | Paused |
| Small Biz Renewal - 2027 | ON | Paused |
| Trucker Health - OE 2027 | $15/day | **$35/day** (Florida only, Max clicks $15 cap unchanged) |
| Ad groups | 4 + fleet + Spanish | Truck Driver · Owner Operator · 1099 Driver · 2027 Rate Increase · **Company Driver - No Benefits (new)**. Fleet group paused, Spanish stays paused |
| Ads | Shared copy | One ad per group whose first headlines match that search; all land on /trucking-health-quote |
| Keywords | 36 | ~72 phrase + exact (Search Console terms: "owner operator medical insurance", "health insurance for independent truckers", "truck driver health insurance cost", company-driver terms) |
| Negatives | | +34: jobs, CDL schools, truck/cargo/bobtail insurance, DOT physical lookups, rideshare, group/employer, Medicare |

## Budget calendar (change the trucker budget by hand on these dates)
| Dates | $/day | Note |
|---|---|---|
| Nov 1 - Nov 30 | 35 | |
| Dec 1 - Dec 15 | 50 | Jan 1 deadline. Swap one headline to `{COUNTDOWN(2026-12-15 23:59:00,5)} Left to Enroll` |
| Dec 16 - Jan 15 | 30 | Change "Enroll by Dec 15 for Jan 1" headline to "Enroll by Jan 15 for Feb 1" |
| After Jan 15 | 12 | Special enrollment only (drivers leaving a carrier: Company Driver group) |
Roughly $1,100 in November.

## Conversion rate checklist (do once in the UI)
- Goals: **Quote Form Lead** = Primary, Count **One**. **Calls from ads (1)** (60s+) = Primary. Phone Call Click = Secondary.
- Turn on **Enhanced conversions for leads**.
- Call asset (954) 825-1009 scheduled to staffed hours. Callouts: No Fee to You · Licensed Advisor · Same-Day Quotes · Coverage on the Road.
- Sitelinks: Get My Quote > /trucking-health-quote · Owner-Operator Plans > /best-health-insurance-owner-operators ·
  Truck Driver Costs > /truck-driver-health-insurance-cost · DOT Physical & Insurance > /does-health-insurance-cover-dot-physical
- Call every ad lead within 5 minutes. Speed to call is the biggest lever on lead-to-sale.

## Rules so money isn't wasted
- Max cost per lead = (commission per sale) x (close rate). Example: $300 x 20% = $60.
- Any keyword that spends 2x that with zero leads: pause it.
- Every Monday and Thursday: Search terms report > add anything not a driver buying health insurance as a negative.
- After 15 conversions in 30 days: switch bidding to Maximize conversions. After 30: set target CPA at 1.2x actual.
- Expand beyond Florida only once health-insurance ad certification covers more states (more states = more drivers, same ads).

Old multi-campaign files are in `archive-2026-11-01/`.

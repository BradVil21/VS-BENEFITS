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

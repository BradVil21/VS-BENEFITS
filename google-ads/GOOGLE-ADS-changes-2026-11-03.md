# Google Ads changes, 2026-11-03 (applied by Claude in the account)

## Done
- Campaign "Trucker Health - OE 2027": locations changed from Florida only to 8 states:
  Florida, Georgia, Illinois, Kentucky, Maryland, Missouri, Ohio, Texas.
- Location option checked: already "Presence: people in or regularly in" (no change).
- Health insurance certification confirmed active by Google (duplicate application closed).
  No ads in this campaign are disapproved. One old paused ad shows "Policy (Health Insurance)"; it stays paused.

## Still open
- The 3 live ads mention "Florida" in their copy (e.g. "Florida Trucker Health Plans", "Florida truck drivers: compare...").
  Drivers in the other 7 states will see Florida wording until the copy is updated.
- Networks: Search partners is ON (plan said off).
- Budget is still $50/day, now spread across 8 states instead of 1.

## Marketing tab sync (admin portal), 2026-11-03
- "VS Ads Sync (Marketing tab)" script in Google Ads updated (secret kept). It now also sends targeted locations,
  results by state (people located there), and live sitelinks/callouts/snippets/call assets. Preview: Sync 200,
  9 locations, 38 state rows, 34 assets, no query errors.
- /api/ads-sync stores the new fields; admin Marketing tab has a new "Where your ads show" section:
  targeted states per campaign, a by-state table (Google spend/clicks/conversions next to portal leads,
  quoted and sold, matched by ZIP), state tips in "What to do next", and the live assets list. Deployed (commit 8789273a).
- "VS Trucker 8 States (Nov 3)" still needs Authorize before it can preview/run.

## Self-Employed campaign to 8 states (1:40 PM)
- "Self-Employed FL - 2027" locations: Florida -> FL, GA, IL, KY, MD, MO, OH, TX (saved in the account).
- Its ads said "Florida Self-Employed Plans" / "Self-employed in Florida?". The waiting script is now
  "VS 8 States - Truckers + Self-Employed (Nov 3)" (google-ads/vs-8-states-2026-11-03.js): new 8-state ads,
  sitelinks, callouts and snippets for BOTH campaigns, state keywords, Search partners off. Needs Authorize, then Preview, then Run.
- Family Plans (No Subsidy) ad group is in the paused "Individual - OE 2027 FL" campaign; not changed.

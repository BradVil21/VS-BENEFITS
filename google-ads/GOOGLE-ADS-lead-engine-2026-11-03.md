# Lead engine: 5 campaigns, state landing pages, sold-lead feedback (Nov 3 2026)

## Do these in order (about 20 minutes)

### 1. Vercel: add one setting, then push
Vercel > Project > Settings > Environment Variables > add
`GADS_LEAD_KEY` = `8Sf46llj173PlrzDSaejk5KpojwgFLjS` (Production). Then push:

```bash
cd ~/Desktop/VS-BENEFITS
git add lp api/_ads-sold.js api/_gads-lead.js api/voice-lookup.js vercel.json middleware.js \
  does-health-insurance-cover-dot-physical.html truck-driver-health-insurance-cost.html \
  best-health-insurance-owner-operators.html small-business-health-insurance.html \
  sitemap.xml search-index.json _build google-ads/vs-lead-engine-*.js google-ads/GOOGLE-ADS-lead-engine-2026-11-03.md
git commit -m "Lead engine: state landing pages, sold-lead upload, lead form webhook, trucker SEO quick wins"
git push origin main
```
Check after deploy: open https://www.vshealthbenefits.com/lp/truckers/texas

### 2. Google Ads: build script (one time)
Tools > Bulk actions > Scripts > + New script, name **VS Lead Engine - Build**, paste all of
`google-ads/vs-lead-engine-build-2026-11-03.js`, Authorize, **Preview**.
The log should end with `DONE. No errors.` Then **Run**. Re-running is safe (it skips what exists).

| Campaign | $/day | Located in |
|---|---|---|
| Trucker - FL & GA | 8.33 | FL, GA |
| Trucker - TX, IL & OH | 8.33 | TX, IL, OH |
| Trucker - KY, MO & MD | 8.34 | KY, MO, MD |
| Self-Employed 1099 - 8 States | 17.50 | all 8 |
| Spanish - Camioneros e Independientes | 7.50 | all 8, Spanish |
| **Total** | **50.00** | Trucker 50% / Self-employed 35% / Spanish 15% |

All: Google Search only, "people located in", phrase + exact only, Maximize clicks with $15 max CPC,
55 shared negatives (aca, obamacare, marketplace, subsidy, medicaid, medicare, calculator, jobs, cdl school,
truck/cargo insurance, dental, vision, dot physical...), call asset (staffed hours), call-only ads,
sitelinks, callouts, lead form asset. "Trucker Health - OE 2027" is paused.

### 3. Google Ads: hourly script
New script **VS Lead Engine - Hourly**, paste `google-ads/vs-lead-engine-hourly-2026-11-03.js`.
At the top, replace `PASTE_THE_SAME_SECRET...` with the secret already in your "VS Ads Sync" script.
Preview, then set Frequency: **Hourly**. It:
- pauses call-only ads outside Mon-Fri 8-6 / Sat-Sun 8-1 so no call rings unanswered
- switches all 5 campaigns to Maximize conversions once they pass 15 leads together
- uploads SOLD leads every Monday 9am as "Sold Policy" (only leads that came from an ad click)

### 4. GoHighLevel: instant text on every new lead (2 minutes)
Automation > Workflows > Create workflow > Start from scratch.
- Trigger: **Contact Tag** > Tag Added > `website-lead` (add a 2nd trigger for `google-lead-form`)
- Action: **Send Internal Notification** > SMS > Users: you (and Rico once he is a user)
  Message: `NEW LEAD: {{contact.name}} {{contact.phone}} ZIP {{contact.postal_code}} - call within 5 min`
- Save, Publish. It texts the phone on each user's GoHighLevel profile.

## What counts as a lead in Google Ads
Primary: ad calls of **60 seconds or longer**, Quote Form Lead, lead form submits, Sold Policy.
Everything else (phone link clicks, GA4 events) is set to observe-only.

## Landing pages (noindex, ads only)
`/lp/truckers`, `/lp/self-employed`, `/lp/es/camioneros`, `/lp/es/independientes` send each visitor to
their state page by IP (e.g. `/lp/truckers/texas`); anyone else sees the general page.
Call button on top, 4-field form (name, phone, ZIP, who needs coverage) into the same lead pipeline as /quote.
Rebuild after edits: `python3 _build/build-lp.py`

## Trucker SEO quick wins
Mid-page call/quote box + new FAQs (page and FAQ data) on:
- /does-health-insurance-cover-dot-physical (pos 8.9): where to get one, how long the card lasts, how your plan helps
- /truck-driver-health-insurance-cost (pos 8.5): title now "Truck Driver & Owner-Operator Health Insurance Cost 2027"
- /best-health-insurance-owner-operators (pos 7.0): how fast you can be covered, how to get a quote

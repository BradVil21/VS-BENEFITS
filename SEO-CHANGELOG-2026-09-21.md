# SEO Changelog — 21 September 2026

Source: Search Console export 20 Jun – 19 Sep 2026 (343 clicks, 71,857 impressions,
0.48% CTR, avg position 60 → 23). Goal: more clicks and more leads before
Open Enrollment opens on 1 November.

## 1. 2027 Open Enrollment guide (`/blog/aca-open-enrollment-2027-guide`)
Most-shown page on the site (8,451 impressions, position 13.4, 0.31% CTR).
- Title: "When Is Open Enrollment 2027? Nov 1 – Jan 15 Deadlines" (dates now in the title; og/twitter matched).
- Meta description rewritten: dates + Dec 15 cutoff + "free help from a licensed broker".
- New above-the-fold box under the intro: 3 key dates + **Get My Free 2027 Quote**,
  **Estimate My Subsidy**, **Call (954) 866-6872**. Before this, the first quote button sat below the state table.
- dateModified / "Updated" stamp → 2026-09-21. The FAQ section and FAQPage schema were already there (18 questions), so they were kept as they are.
- Dates re-checked: HealthCare.gov OE runs Nov 1, 2026 – Jan 15, 2027; Dec 15 for a Jan 1 start.

## 2. Merged duplicate / overlapping pages (301s in vercel.json)
| Old URL | Now redirects to | Why |
|---|---|---|
| /can-truckers-deduct-health-insurance | /blog/can-owner-operators-deduct-health-insurance | same topic; blog ranks 6.4 vs 32.7 |
| /blog/health-insurance-dot-physical | /does-health-insurance-cover-dot-physical | same intent; target ranks 4.7 |
| /blog/miami-small-business-health-insurance | /miami-small-business-health-insurance | split Miami group-health signals |
| /blog/do-truck-drivers-get-health-insurance | /truck-driver-health-insurance | competes with the trucking main page |
| /blog/affordable-health-insurance-truck-drivers | /truck-driver-health-insurance | main page already has an "Affordable" section |
| /blog/truck-driver-family-health-insurance-guide | /truck-driver-health-insurance | main page already has a family section (the other family page was already redirected) |
| /health-insurance-for-self-employed-truck-drivers | /best-health-insurance-owner-operators | position 87; same audience |
| /1099-truck-driver-health-insurance | /best-health-insurance-owner-operators | consolidates the "owner-operator / 1099" cluster (pos 32–40) |
| /aca-sidsub-calculator, /blog/what-happens-if-vous-miss-open-enrollment, /blog/how-many-employees-do-you-need-for-group-health-insurance-florida | correct URLs | typo URLs Google had seen |

Also: 156 internal links on 47 pages now point straight at the new URLs, with no redirect hops. On those pages, 71 duplicate
"related guide" cards and 18 duplicate list links were removed. 8 URLs were removed from sitemap.xml, lastmod was bumped on the
pages that changed, and the 1099 line was removed from llms.txt. No redirect chains, and no live page links to a redirected URL.
The old HTML files stay in the repo (Vercel serves the redirect first), which follows the practice from earlier passes.

Already done in earlier passes, so not repeated here: dental/vision state pages → /dental-vision-insurance,
/how-much-does-health-insurance-cost → blog 2026 cost post, /health-insurance-open-enrollment-faq → OE guide.
Search Console still lists those URLs because the 3-month window includes the period before they were redirected.

Kept on purpose: trucking city pages (local intent), Spanish pages, fleet/group pages, and the calculators.

## 3. Destination pages tuned for the traffic they now receive
- /best-health-insurance-owner-operators: meta description now names 1099 and self-employed truck drivers.
- /blog/can-owner-operators-deduct-health-insurance: title → "Can Owner-Operators & Truckers Deduct Health Insurance? 2027".

## 4. ACA subsidy calculator (`/aca-subsidy-calculator`)
The calculator was already a lead form: ZIP → phone (required, and the lead is captured at this step) → household → income → name,
then results. It posts to /api/lead-sync and fires GA4 `generate_lead`. Changes in this pass:
- Title: "2027 ACA Subsidy Calculator: See Your Price in 60 Seconds". Meta description rewritten.
- Freshness stamp and dateModified → 2026-09-21.

## 5. Lead tracking — status
vs-attribution.js and vs-conversions.js are already on all 265 public pages. They send phone_click, chat_open, quote_cta,
quote_start, quote_step and generate_lead to GA4. First-touch source goes into every lead that reaches GoHighLevel.
**Still needed, and only you can do it:**
1. GA4 → Admin → Events: mark `generate_lead` and `phone_click` as **Key events**.
2. Google Ads → Goals → Conversions: copy the two conversion labels into `LABELS` in vs-conversions.js (lead, phone).
3. Search Console → Sitemaps: resubmit sitemap.xml after deploying. Then use URL Inspection → Request indexing on the OE guide.

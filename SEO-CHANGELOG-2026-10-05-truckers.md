# SEO changelog — 2026-10-05 — Trucker leads push

Based on Search Console export (Jul 4 – Oct 4, 2026): trucking = ~17% of clicks; head terms ("health insurance for truck drivers", owner-operator variants) at positions 37–49; DOT-physical long tail at 2–5.

## Lead capture
- Added a **Text us** button (sms:+19548251009, prefilled "TRUCK – …" / "CAMIONERO – …") to the mobile sticky bar on 60 trucking pages; Spanish pages say "Texto". Fires GA4 event `contact_text`.
- Fixed overlapping mobile bars on 28 pages: the old `#vs-sticky` bar covered the Call/Text/Quote bar after scrolling; now hidden on mobile where `#vs-callbar` exists (still shows on desktop).
- Trucking pages' OE announcement bar now links to /truck-driver-open-enrollment-2027 with driver-specific copy (39 pages).

## New pages
- /dot-physical-blood-pressure-requirements — FMCSA stage chart, 3-month card path, exam-day tips, FAQ schema.
- /how-long-is-a-dot-physical-good-for — card length by condition (BP, ITDM MCSA-5870, sleep apnea), renewal, FAQ schema.
- /examen-medico-dot — Spanish DOT physical guide (hreflang paired with /dot-physical-requirements).
- Added to sitemap.xml, llms.txt, vercel.json (.html redirects); cards added to the "Driver tools" block on 51 pages; contextual links from 11 DOT/trucking/Spanish pages.

## Titles / descriptions
- blog/aca-open-enrollment-2027-guide → matches top query "when is open enrollment for health insurance 2027" (1,096 impr, pos 9).
- best-health-insurance-owner-operators → adds "Independent Truckers".
- dental-vision-insurance, ppo-health-insurance, qualifying-life-events-health-insurance, health-insurance-between-jobs → exact-match phrasing.

## Notes
- /how-much-does-health-insurance-cost (pos 191) was already 301'd to the blog version; GSC still shows pre-redirect data.

## Off-site
- 9 posts scheduled in GHL Social Planner (Google Business Profile + LinkedIn), Oct 8 – Nov 3.
- Outreach kit (media pitches, partner emails, FB/Reddit answers, video scripts, setup checklist) in Claude Docs: "Trucker Outreach Kit".

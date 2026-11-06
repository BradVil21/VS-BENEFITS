# 2026-11-05: indexing pass (Google Search Console + Bing)

## What Search Console showed
- 218 indexed, 92 not indexed. Most of the 92 are expected (old redirects, merged state/dental pages, noindex admin pages).
- Sitemap read Nov 5, 270 URLs known. The "not indexed" report lags several days: blog posts it listed
  (rate increases by state, why premiums went up, trucker too-much-income) are already on Google per live URL Inspection.
- Really not indexed yet: the Nov 3 state landing pages (/lp/truckers/*, /lp/es/*, /lp/self-employed/*).
  URL Inspection: "Discovered - not indexed, Referring page: None detected" (no internal links pointed to them).

## Requested indexing (Google daily limit reached after these)
- /private-health-insurance (rebuilt Nov 4), /lp/truckers/georgia, /lp/truckers/illinois
- Next day: /lp/truckers/ohio, kentucky, missouri, maryland, /lp/es/camioneros/texas, georgia, illinois

## Fixes
- Site-wide "Service Areas" menu (339 pages, 10,848 links): every state linked to /health-insurance-{state},
  which 301-redirects to /health-insurance. Now: FL GA IL KY MD MO OH TX -> /lp/self-employed/{state};
  the other 24 states -> /{state}-small-business-health-insurance. Redirects kept for outside links.
- "By state" link rows added: /truck-driver-health-insurance (trucker state pages), /seguro-medico-camioneros
  (camioneros + independientes state pages), /self-employed-health-insurance (self-employed state pages).
- sitemap lastmod 2026-11-05 for those hubs and the homepage.
- Backups: .seo-work/nav-fix-2026-11-05/backup. Script: .seo-work/nav-fix-2026-11-05/fix.py

## Bing
- All sitemap URLs sent through IndexNow on Nov 4 (271 received). Run `node indexnow.js` after this push.

## 2026-11-06: Google indexing requests (URL Inspection), trucker pages first
All showed "URL is not on Google" (Discovered - not indexed) and were sent to the priority crawl queue:
/lp/truckers, /lp/truckers/ohio, kentucky, missouri, maryland,
/lp/es/camioneros/texas, georgia, illinois, ohio, kentucky,
/blog/state-farm-agents-losing-health-insurance.
Daily quota hit on /lp/es/camioneros/maryland (11 requests went through).
Still to request: /lp/es/camioneros/maryland, /lp/es/camioneros/missouri, /lp/es/camioneros (hub).
Bing/IndexNow: could not send from here (network blocked); run `node indexnow.js` in Terminal.

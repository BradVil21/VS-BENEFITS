# 2026-10-27: open enrollment push, calculator keywords, CTR titles, indexing fixes

Snapshot (Search Console, Jul 26 - Oct 25): 615 clicks / 87,856 impressions, CTR 0.70%.
Weekly clicks 40 -> 91 since mid-September; last week's impressions 11,108 (OE season starting).

## Open enrollment guide (/blog/aca-open-enrollment-2027-guide)
9,754 impressions, 0.28% CTR, position 13.7. "when is open enrollment for health insurance 2027" = 635 impressions at #10.
- Title/og/twitter: "When Is Health Insurance Open Enrollment 2027? Nov 1–Jan 15" (adds "health insurance", the query's wording).
- Description now names HealthCare.gov (~200 impressions/quarter on healthcare.gov OE queries).
- Date-aware status line under the lede (#oe-live-status): "opens in N days" -> "open now, N days left for Jan 1" -> "closes Jan 15" -> after. Static fallback text is true without JS.
- dateModified aligned to 2026-10-27 in JSON-LD, microdata, visible "Updated" line and sitemap (they disagreed: 10-08 vs 09-21).
- Internal links: already strong (344 pages + OE bar). Added a keyword link in the homepage hero.

## Subsidy calculator (/aca-subsidy-calculator)
"obamacare / obama care subsidy calculator" variants ~800 impressions at positions 52-62, 0 clicks; "health insurance subsidy calculator" 162 at #55.
- H1: "2027 ACA (Obamacare) Subsidy & Health Insurance Cost Calculator". Subhead names Obamacare, health insurance subsidy, premium tax credit.
- New FAQ (HTML + FAQPage schema): "Is this the same as an Obamacare subsidy calculator?"
- Title kept (it earns 7-10% CTR on the 2027 queries). Lead capture unchanged (results are already gated on phone + name -> /api/lead-sync).

## Homepage
- Hero link row under the CTAs: "Open enrollment 2027 dates & deadlines" and "2027 Obamacare subsidy calculator". Checked at 390px and 1280px.

## Title/description rewrites (page 1, weak CTR)
- /blog/how-much-does-health-insurance-cost-2026 (#9.8, 0.22%): "Health Insurance Cost Per Month: $625 Average, by Age (2026)".
- /blog/is-dental-and-vision-insurance-worth-it (#8.7, 0.29%): "... Worth It? Bundle vs. Separate" (matches the bundle queries).
- /blog/group-health-insurance-minimum-participation (#9.4, 0.38%): "Minimum Participation Requirements: The 70% Group Health Rule".
- /blog/what-income-counts-for-aca-subsidies: left as is; its title already matches the queries, it needs rank, not a rewrite.

## Search Console indexing emails
- "Blocked due to other 4xx": the only URL is /api/portal-signup (POST-only endpoint, answers GET with 405). robots.txt now
  disallows /api/ in every group, keeping /api/google-rating and /api/calendly open because pages call them on load.
- "Redirect error" (13): vercel.json simulated end to end, no loops or chains over 1 hop; live browser checks and a
  Googlebot live test of /blog/miami-small-business-health-insurance (failed crawl Oct 20 4:47pm, during the Oct 20 deploys)
  both pass now. The other 12 are non-www/http URLs last crawled May-July, before the host redirect. Action: Validate Fix again.
- "Not found (404)" (8): 7 old non-www state URLs from June that now 301 to /health-insurance; 1 is email.mail.vshealthbenefits.com,
  the email-sending subdomain (not a website; ignore).

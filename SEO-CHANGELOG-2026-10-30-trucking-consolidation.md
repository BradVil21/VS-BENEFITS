# 2026-10-30: trucking consolidation (Search Console export Jul 29 - Oct 28)

Diagnosis: 87 trucking URLs = 21% of impressions but 15% of clicks. Head terms ("health insurance for truck
drivers" + ~35 variants: 4,116 impr, pos 41, 2 clicks; owner-operator variants: 2,036 impr, pos 38, 3 clicks)
are still split across too many pages. Thin fleet and city pages had 1-7 impressions or sat at position 51-57.
Note: most older duplicates (1099, self-employed, affordable, do-truck-drivers, family guide, OTR, truckers-health-insurance,
blog/health-insurance-for-truck-drivers, blog DOT post) were already 301'd; their GSC rows are pre-redirect history.

## 301s added (vercel.json, clean + .html)
- Fleet pages -> /health-insurance-for-trucking-companies: refrigerated, heavy haul, oilfield, dump truck, delivery fleets, freight brokers.
- City pages: Atlanta -> hub ?state=GA, Memphis -> ?state=TN, Indianapolis -> ?state=IN, Dallas -> /truck-driver-health-insurance-texas.
- Files left in place (redirects win on Vercel). Removed from sitemap.xml (212 -> 202).

## Internal links (script: .seo-work/trucking_consolidate_oct30.py)
- 146 cards to the old pages removed; in each related-guides block the fleet cards became one
  "Group Health for Trucking Companies" card (28 blocks). City cards, list items, "·" inline links and "City ... ->" links removed.
- 7 "Coverage by trucking hub" / fleet card sections that ended up empty were removed.
- Hub city list: Texas added, 4 cities removed. Hub state sections no longer link to the city pages.
- /health-insurance-for-trucking-companies: new "Delivery fleets, freight brokers and 3PLs" H3 in the fleet-type section.
- No internal link points to a redirected URL.

## Titles (CTR)
- /blog/using-health-insurance-out-of-state-truck-drivers (pos 5.7, 237 impr, 0 clicks):
  "Does Health Insurance Work Out of State? Truck Driver Guide" + new description.
- /truck-driver-health-insurance-raleigh-nc (Raleigh queries pos 4.5-8, 0 clicks):
  "Truck Driver Health Insurance in Raleigh, NC (2027 Quotes)" + new description.

## Watch out
- If a build script in .seo-work or _build regenerates the fleet/city pages or their link blocks, it will put the links back.

## Next (needs you)
- After deploy: Search Console -> URL Inspection -> Request indexing for /truck-driver-health-insurance,
  /health-insurance-for-trucking-companies, /best-health-insurance-owner-operators, and the 2 retitled pages.
- Sitemaps -> resubmit sitemap.xml.
- The head term needs links from other sites: trucking directories, partner fleets/factoring companies (DropPay),
  OOIDA/state trucking associations, guest posts on trucking blogs.

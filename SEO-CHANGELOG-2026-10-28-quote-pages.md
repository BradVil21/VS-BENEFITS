# 2026-10-28: quote landing pages -> rank for "quote" searches

Pages: /trucking-health-quote, /small-business-health-quote (also the Google Ads landing pages).
Hero, form, tracking and everything above the reviews unchanged. Builder: .seo-work/build_quote_pages_oct28.py

- Titles/H1 now match the searches: "Health Insurance Quotes for Truck Drivers (Free, 2027)" and
  "Small Business Health Insurance Quotes: Free Group Quotes (2027)". The trucker page used to have the same
  title topic as /truck-driver-health-insurance ("Health Insurance for Truck Drivers & Trucking Companies").
- New section below the reviews (~700 words each): how quotes work (3 steps), what sets the price,
  who it is for / what you need to qualify, 5-question FAQ. Links to cost, calculator, open enrollment,
  out-of-state, DOT, 70% rule, ICHRA and renewal-review pages.
- JSON-LD: Service (provider InsuranceAgency, free Offer), BreadcrumbList, FAQPage. og:url/og:type added.
- Descriptive links ("health insurance quotes for truck drivers", "small business health insurance quotes")
  added under the intro of /truck-driver-health-insurance, /health-insurance-for-trucking-companies,
  /best-health-insurance-owner-operators, /small-business-health-insurance, /health-insurance-for-small-business-owners.
  Before this, all ~80 internal links to these pages said "Get a quote".

Facts used: 400% FPL single $63,840 (2027 coverage, from 2026-10-27 changelog); OE Nov 1 - Jan 15, Dec 15 for Jan 1;
"within 1 business day, often within hours" (existing site claim); 70% participation (existing post).

After deploy: Search Console -> request indexing for both quote URLs.

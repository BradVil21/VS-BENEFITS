# 2026-10-16: Open enrollment lead push (truckers + small business)

- NEW /small-business-renewal-review: "2027 group renewal went up?" landing page (SEO + Google Ads destination).
  Form posts to /api/business-quote (formName "Renewal review", renewal increase + date), fires quote_start and
  generate_lead (Ads conversion). WebPage/Service/Breadcrumb/FAQPage schema. Builder: .seo-work/build_renewal_review_oct16.py
- NEW vs-oe-bar.js on all 254 pages with #oe-annc-bar: rewrites the static bar by date (pre-OE / Nov 1-Dec 15 countdown /
  Dec 16-Jan 15 last chance / after: SEP checker) and audience (trucker -> /truckers/quote, business -> renewal review,
  general -> /quote), Spanish on Spanish pages. Static bar remains the fallback.
- FIX api/business-quote.js: attribution (channel, campaign, keyword, landing, gclid) was dropped; now saved on the
  Business Leads card, in its notes and in the GHL note; source label shows the channel.
- Renewal-review callouts on /small-business-health-insurance, /health-insurance-for-trucking-companies,
  /business-open-enrollment-faq, /blog/small-business-health-insurance-cost-2027. Sitemap + llms.txt updated.
- google-ads/: OE 2027 plan + Google Ads Editor import CSVs (not deployed; .vercelignore covers *.md, *.csv).

After deploy: Search Console → Request indexing for /small-business-renewal-review; resubmit sitemap.
Bump the dates in vs-oe-bar.js for next season (OPENS / JAN1_DEADLINE / CLOSES).

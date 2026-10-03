# Changelog: 2 October 2026 (leads)

Source: Search Console export, 3 months to 1 Oct 2026 (422 clicks, 78,361 impressions).
Clicks by month: 94 (Jul) -> 124 (Aug) -> 194 (Sep). Average position about 55 -> about 20.
Most of the export predates the 21 / 24 / 30 Sep changes, so titles were left alone this time.
This pass is about turning the traffic we already get into calls and quote requests.

## 1. Mobile "Call / Get my quote" bar on every page (vs-conversions.js)
Mobile ranks far better than desktop (#29 vs #48) and gets clicked more often (0.73% vs 0.43%),
but only about 60 trucking pages had a fixed call bar. The homepage, all small-business, local,
ACA, COBRA and blog pages had none.
- Added once to vs-conversions.js (already loaded on every public page), so no HTML pages changed for this.
- Phones only (under 760px). Teal "Call an advisor" (tel:+19548666872) + blue "Get my quote".
- Spanish pages (lang="es") show "Llamar" / "Cotizar gratis".
- Dental/vision pages send "Get my quote" to the dental funnel, like their own buttons.
- Skipped where it would get in the way: pages that already have a bar (#vs-callbar / #vs-sticky),
  /quote, /get-a-quote, calculators, checkers, plan finder, client/admin/census/book/careers/privacy/terms.
- Moves the chat launcher and back-to-top button up so nothing overlaps.
- Clicks are tracked by the existing listener (phone_click, quote_cta -> GA4 + Google Ads).

## 2. Sample testimonials replaced with the real Google review (68 pages)
The 24 Sep changelog left this open. Invented reviews ("Marcus T.", "Daniela R.", "Derek M.",
"The Wilkins Family" and about 30 others) were shown as "Real reviews from Google" / "Verified Google
review" on the homepage and 67 other pages. The FTC rule on fake reviews (in force since Oct 2024)
allows civil penalties for each violation, and Google can act on it too. A licensed agent can't afford that risk.
- 47 pages with the scrolling carousel (homepage, city, state and industry pages): now show the one real
  review, centered, with no scrolling. "Read more reviews on Google" / "Leave a review" buttons kept.
- 20 pages with static "Client Stories" cards: one real review card + "Read our reviews on Google" link
  (Spanish on the two seguro-medico pages). Heading is now "What Clients Say on Google".
- /open-enrollment: 3 sample slides and the "shown for illustration" note removed; the real review stays.
- No Review or AggregateRating schema on the site, so there was nothing to fix there.
Next: as real Google reviews come in, add them to the `reviews` array (same format) on these pages.

## 3. Also in this commit: 30 Sep Part 2 (was never committed)
/blog/aca-income-limits-2027, /blog/inscripcion-abierta-2027, calculators moved to the 2027 numbers,
hreflang, sitemap and llms.txt. See SEO-CHANGELOG-2026-09-30.md.

## Still needed (only you can do these)
1. Ask the last 10 clients for a Google review this week (link: https://g.page/r/CTz8LoxJRazwEBM/review).
   One review is the weakest part of the site now; 5-10 more will lift both rankings and quote requests.
2. Search Console: Request indexing on /blog/aca-income-limits-2027 and /blog/inscripcion-abierta-2027,
   and resubmit sitemap.xml.
3. In 2 weeks, check GA4 -> Events -> phone_click to see how many calls the new bar brings in.

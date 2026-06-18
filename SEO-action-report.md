# VS Benefits SEO & CTR Action Report

Based on your Google Search Console export (last 3 months: 35 clicks, 2,284 impressions, 1.53% CTR, average position ~36).

## The core diagnosis

Your click problem is mostly a **ranking** problem, not a wording problem. Most pages surface on page 4 or deeper (positions 40 to 90), where almost nobody scrolls, so a better title cannot win a click that never gets seen. Click-through tuning only pays off on pages already near page 1. The data shows a handful of those, and that is where the work below is aimed.

Three facts shaped the plan:

1. Your ACA open-enrollment blog ranks **position 12** for "when is open enrollment for health insurance 2027" (106 impressions, 0 clicks). That is the single best near-page-1 opportunity on the site.
2. The brand query "vs benefits" (83 impressions, position 5) converts at only 1.2 percent. A brand search should win its own click almost every time.
3. Desktop CTR (0.97 percent) is a third of mobile (2.81 percent), and "vision insurance" already sits at position ~10, which the new dental and vision pages are built to capture.

## What I changed in the code

**Homepage (index.html)**
- Rewrote the title to lead with your brand so the "vs benefits" search clearly recognizes you: `VS Benefits | Miami Health Insurance Broker (PPO, ACA, Small Business)`.
- Rewrote the meta description with a stronger hook plus your phone number.
- Added a `WebSite` schema entity and enriched your existing `InsuranceAgency` schema with a description and a `knowsAbout` list. This strengthens your brand entity in Google and supports knowledge-panel and sitelink eligibility.
- Fixed a broken `og:image` (it pointed to a file that does not exist, so social shares showed no preview image). It now uses a real photo.
- Added five keyword-rich internal links inside the "What we do" section, pointing to your small business, PPO, truck driver, 1099, and dental/vision pages, plus "learn more" links on the relevant cards. Internal links from the homepage pass ranking signal to those buried pages.

**ACA open-enrollment blog (the #1 opportunity)**
- Retargeted the title, H1, and meta description to match the exact question people search: "When Is Open Enrollment for Health Insurance 2027?" with the dates answer up front. This improves both relevance (ranking) and CTR, and makes the page eligible for a featured snippet.

**Niche landing pages**
- Added "Miami" to the small business title (you rank position 26 for "small business health insurance miami").
- Led the PPO description with "best PPO health insurance in Florida" and a "what is a PPO" hook to capture that query cluster.
- Broadened the truck driver and 1099 descriptions to match more query variants (owner-operator, physicians, gig workers).

All new and edited copy contains no em-dashes, en-dashes, or double hyphens.

## What you should do next (outside the code)

These are the levers that actually move rankings and visibility, ordered by impact.

1. **Request indexing for the new and updated pages.** In Google Search Console, use the URL Inspection tool to submit the homepage, the ACA blog, the new `dental-vision-insurance` page, and the new blog post. Also resubmit your sitemap.xml. This gets the changes seen in days instead of weeks.

2. **Set up and optimize a Google Business Profile.** For a Miami broker, this is the highest-impact "get noticed" move available. It puts you in the local map pack and the brand knowledge panel, and it is free. Use the exact same name, phone, and hours as the site.

3. **Fix the buried high-impression pages with content, not just titles.** Your truck driver page got 531 impressions but ranks position 55, and small business got 322 impressions at position 61. Google is testing them but not trusting them yet. They need more depth, more internal links pointing in with descriptive anchors, and ideally a few external links.

4. **Earn backlinks.** This is the biggest reason you sit at position 36 on average. A new site with few referring domains cannot outrank established carriers and comparison sites. Local business directories, your chamber of commerce, trucking and small-business associations, and guest articles are realistic starting points.

5. **Investigate the desktop CTR gap.** Desktop converts at a third of mobile. Check how your titles and descriptions render on a desktop SERP and whether a competitor is outshining you there.

6. **Tighten URL duplication.** Search Console shows both `/about` and `/about.html`, and both www and non-www, getting indexed. Your redirects cover some of this; make sure every `.html` version 301-redirects to its clean URL so ranking signals are not split across duplicates.

7. **Optional: clean remaining em-dashes in older pages.** Your earlier pages (the ACA blog, truck driver page, and a few others) still contain em-dashes and double hyphens in body copy from before. I can sweep the whole site to remove them if you want consistency.

# SEO fixes — 25 August 2026

Driven by the Google Search Console review of 24 May – 23 Aug 2026
(230 clicks / 48,838 impressions / 0.47% CTR / avg position 51.7).

---

## 0. The one that wasn't on the list: the enrollment deadline was wrong

**62 files stated that 2027 open enrollment closes December 15, 2026. It closes January 15, 2027.**

December 15 is the deadline for coverage that *starts* January 1 — a different thing. At some
point a find/replace swapped "January 15" for "December 15" sitewide, which also produced
sentences like *"enroll December 16 through December 15"* and *"the absolute final deadline is
December 15… but the more important deadline is December 15."*

`llms.txt` had it right the whole time and cited the CMS statement of July 31, 2026, so the site
was contradicting its own AI-facing summary.

Verified 2026-08-25 against healthinsurance.org's deadline FAQ (two independent fetches, consistent):

| | |
|---|---|
| HealthCare.gov open enrollment (incl. Florida) | **November 1, 2026 – January 15, 2027** |
| Deadline for January 1, 2027 coverage | December 15, 2026 |
| Plans selected Dec 16 – Jan 15 | Coverage starts February 1, 2027 |

**144 replacements across 59 files.** Every "enroll by December 15 for a January 1 start" was
preserved — those were correct. The Florida group-plan statute references to a
"November 15 through December 15" window were also left alone; different rule, different topic.

This matters beyond SEO: telling someone enrollment closed on December 15 when they have until
January 15 could cost them a year of coverage.

### State deadline table rebuilt
The table on the 2027 guide had ~14 of 18 rows wrong (Colorado, Georgia, Kentucky, New Mexico,
Washington, Pennsylvania and Vermont were all listed as December 15; all are January 15). Rebuilt
with 23 verified rows, HealthCare.gov states first. Rhode Island (Dec 31) and Idaho (Dec 15) are
the only two that genuinely close early; California, DC, New Jersey and New York run to Jan 31,
Virginia to Jan 29, Massachusetts to Jan 23.

---

## 1. Titles and meta descriptions — pages ranking 4–20

15 pages rewritten (title + description + og + twitter mirrors), all titles ≤60 chars and
descriptions 149–158 chars, answer-first. The big ones:

| Page | Was | Now |
|---|---|---|
| `/blog/aca-open-enrollment-2027-guide` | "…2027? (By State)" | "Open Enrollment 2027: Nov 1 – Jan 15 (Dates by State)" |
| `/blog/how-much-does-health-insurance-cost-2026` | 99-char title (truncated in SERPs) | 56 chars, leads with the $625 benchmark figure |
| `/services` | generic | names the plan types, position 4.9 with 0 clicks |
| `/blog/what-happens-if-you-miss-open-enrollment` | — | leads with the Jan 15 deadline |

All figures used in descriptions are pulled from each page's own body copy. Nothing invented.

## 2. Open-enrollment hub

- New **Florida section** on the 2027 guide (`#florida`) — Florida uses HealthCare.gov, no separate
  deadline, plus the three things that *do* differ: no Medicaid expansion (the coverage gap),
  narrow networks marketed as PPOs, and the self-employed income-estimate problem.
  Targets "open enrollment 2027 florida" (37 impressions, position 10).
- **4 new FAQs** added to both the visible FAQ and the FAQPage schema, targeting the
  "missed open enrollment" cluster (209 impressions across five variants, positions 25–28)
  and "when does open enrollment start for 2027".
- `dateModified` refreshed to 2026-08-25; byline updated.
- **Hub cross-links** across the 5 remaining OE pages via a shared related-guides block.

## 3. Redirects — two were pointing the wrong way

`/blog/how-much-does-health-insurance-cost-2026` (541 impressions, **position 7.7**) was being
301'd into `/how-much-does-health-insurance-cost` (3,134 impressions, **position 196**). That
sends a page-one ranking into a page-twenty page. **Reversed.** `/health-insurance-cost-faq` now
points at the ranking post too.

Everything else checked out:
- All 13 legacy `.html` URLs already had 301s (nothing missing).
- The dental & vision state pages were **already consolidated** — 32 of them 301 into
  `/dental-vision-insurance`, done in commit `30fab5d` on 22 July. GSC still shows them because
  Google hadn't reprocessed by 23 August. No action needed; this was item 4 on the list.
- 257 redirects validated: no loops, no chains, no self-redirects, no duplicate sources.
- **39 internal links** pointed at redirect sources across 21 files. Rewritten to final destinations.

## 4. Sitemap rebuilt

Was 120 URLs, hand-maintained and drifting. Now generated from the filesystem: 119 URLs, excludes
every redirect source and every noindex page, `lastmod` from file mtime. Previously missing and now
included: `/blog/how-much-does-health-insurance-cost-2026`. Previously listed and now correctly
excluded: `/get-a-quote`, `/truckers-health-insurance` and 50 other redirected URLs.

## 5. Trucking cluster cross-linked

23 trucking pages now carry a shared block, and **every one of them points at
`/owner-operator-plan-finder`** as the first card. Cards are chosen per page rather than repeated.

## 6. Tools

- `WebApplication` + `Offer` schema added to `/small-business-health-insurance-calculator`
  (the other two calculators already had it).
- Tool blocks added to 11 pages so the calculators and the plan finder are linked from the
  cost, small-business and ICHRA pages rather than only from the nav.

---

## Not done — needs your call

- **`/ppo-health-insurance`** (3,106 impressions, position 60, 0 clicks). Left in place and linked
  to the tools. Retiring it is defensible but it is a real topic with real volume, so that is your
  decision, not a mechanical fix.
- **Per-state carrier and pricing data.** The remaining state pages are ~1,690 words and ~69%
  templated. The honest fix is real local detail — carrier names, actual plan pricing, state rules
  — and I am not going to invent insurance prices. That is broker work.
- **Conversion tracking.** Clicks are a proxy. Quote-form starts from organic are not currently
  measurable. Worth wiring before November.

## Verification run

- 0 bad date statements remaining sitewide
- 0 invalid JSON-LD blocks across 204 pages
- 0 structural HTML problems across the 104 changed files
- 0 internal links pointing at redirect sources
- `sitemap.xml` parses; `vercel.json` valid JSON

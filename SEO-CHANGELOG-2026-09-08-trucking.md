# SEO Changelog — 8 September 2026

Brief: fix what the Search Console export (7 Jun – 6 Sep 2026) exposed, and add
what trucking was missing. Baseline: 296 clicks / 60,485 impressions / 0.49% CTR
/ avg position ~46. Impressions grew ~6x over the quarter and average position
improved from 55 to ~25. **Clicks did not move.**

---

## 0. Correction to the first-pass report

The initial analysis claimed 85 orphan pages and 83 missing from the sitemap.
That was wrong — it did not account for `vercel.json`, where those URLs are
already 301'd. Re-audited properly against the redirect map:

| | first pass | actual |
|---|---|---|
| Orphan pages | 85 | 5 |
| Missing from sitemap | 83 | 0 |
| Internal links to redirect sources | not checked | 0 |

The site's structure was in good shape. `SEO-action-report-2026-09-08.md` still
contains the uncorrected figures in sections 1a/1b; this file supersedes it.

---

## 1. The open enrollment date error (the most material fix here)

**53 pages stated that Open Enrollment closes 15 December.** It runs to
**15 January 2027**. 15 December is only the cutoff for a 1 January start. The
HHS rule that would have shortened the window was vacated in June 2026.

Where it appeared:

- The **countdown widget on 47 pages**, whose `END` constant was 15 December.
  From 16 December it would have flipped every one of those pages to
  "Open Enrollment is closed for 2027" while a month of enrollment remained.
- The **homepage FAQ schema** — "Open Enrollment runs Nov 1 - Dec 15 each year."
- The **`/health-insurance` meta, og and twitter descriptions** (x3).
- `blog.html` card copy, and the title/meta/og/twitter/schema of
  `blog/open-enrollment-2027-income-premium-increase`.

Fixed, and the countdown rebuilt with **both** deadlines rather than one:

| Phase | Shows |
|---|---|
| before 1 Nov | counts down to open enrollment opening |
| 1 Nov – 15 Dec | counts down to the **1 January coverage** deadline |
| 16 Dec – 15 Jan | counts down to the **close of enrollment**, notes Feb 1 start |
| after 15 Jan | closed |

That is more accurate *and* gives two urgency moments instead of one.

Verified with `node --check` on all 47 rewritten scripts (0 syntax errors) and a
boundary test at all eight phase transitions (`8/8 pass`).

`special-enrollment-period-checker.html` was already correct — it was fixed in
the August pass and its comment says so. Left alone.

**Not touched:** the "November 15 to December 15" references on the small-group
pages. That is the 45 CFR 147.104(b)(1)(i)(B) participation-waiver window and is
genuinely a different date range. Checked each one before excluding it.

---

## 2. New pages

Five, each aimed at a query family that had impressions and nothing pointed at it.

| Page | Target query | Was |
|---|---|---|
| `/truck-driver-health-insurance-cost-calculator` | "truck driver health insurance cost", "owner operator health insurance cost" | pos 21 / pos 13, 1 click |
| `/ooida-health-insurance-vs-aca` | "truckers association health insurance" | pos 58 |
| `/blue-cross-blue-shield-truck-drivers` | "blue cross blue shield for truck drivers" | **pos 8.5, no page existed** |
| `/truck-driver-open-enrollment-2027` | the OEP cluster crossed with trucking | cluster at pos 27 |
| `/best-trucking-company-health-benefits` | "which national otr fleets offer the best benefits packages" | pos 8 |

### The calculator

The reason it should convert where the generic subsidy calculator does not: an
owner-operator's MAGI is built from Schedule C profit, not settlement gross, so
it is a number they partly control. The calculator takes gross settlements minus
deductions (defaulting to a 65% expense ratio), and renders a table of what the
same driver would pay at incomes either side of the 400% cliff, with their own
row highlighted.

Shares the subsidy engine with `/aca-subsidy-calculator` — 2026 FPL
($15,650 + $5,500), the post-enhanced-credit applicable-percentage table from
Rev. Proc. 2025-25, and the federal age curve — so the two pages cannot disagree.
Same progressive lead capture: `/api/lead-draft` on step 2 and 4 and on pagehide,
`/api/lead-sync` on submit, tagged `trucker-cost-calculator`.

Tested in headless Chromium across four scenarios (subsidized family, single
driver near the cliff, driver over the cliff, W-2 company driver). Two defects
found and fixed in testing:

1. The near-cliff row was labelled "best credit" while showing **$0**. It is the
   last row still *eligible*, not the largest credit. Relabelled.
2. The driver's own row rounded income to the nearest $1,000 while the headline
   used the exact figure, so the same screen showed $52,500/$35 and
   $53,000/$31. The row now uses the exact income.

### Editorial line held

No carrier-by-carrier benefit claims on the trucking-company page, and no
premium tables — the plans are not public and change annually. OOIDA's product
list is summarized from their published benefits page and attributed, with the
general product-category behaviour (occupational accident ≠ health insurance;
MEC ≠ comprehensive) explained separately from any claim about their specific
terms. Same rule as the August passes.

---

## 3. Wiring

- **"Driver tools and coverage guides" block on 44 trucking pages.** The five new
  pages start with 44–48 internal links each rather than none.
- **Sticky mobile call bar on 49 trucking pages.** Hidden ≥760px. Mobile ranks
  better than desktop (pos 34 vs 55) and converts at nearly twice the CTR
  (0.71% vs 0.37%), yet gets a third of the impressions. Drivers search from the
  cab; on a phone the call is the conversion, not the form.
- **hreflang across the four Spanish/English trucking pairs**, reciprocal on both
  sides plus `x-default`, with a visible language switch under the header. The
  Spanish pages carry the highest CTR on the site — `/seguro-medico-camioneros`
  at 20% and `/seguro-medico-camioneros-florida` at 33% — off almost no
  impressions. Verified reciprocal: 8/8.
- **15 redirects added** for the new pages' `.html` forms and five natural
  alternates (`/owner-operator-health-insurance-cost`, `/ooida-health-insurance`,
  `/blue-cross-blue-shield-for-truck-drivers`, and so on).
- **sitemap regenerated**: 167 → 169 URLs. Three redirect sources dropped, the
  five new pages added, valid XML, no duplicates.

---

## 4. US spelling normalized

The copy was drifting between conventions — 1,008 "enroll" against 120 "enrol".
230 replacements across 70 files (enrol→enroll, subsidised→subsidized,
licence→license, behaviour→behavior, programme→program and similar). Whole-word
and case-aware. The builders were corrected at source too, so rebuilds stay
consistent. 0 residual.

---

## 5. Verification

`.seo-work/verify_sep.py`, run against all 253 files:

- exactly one title / description / canonical / h1 per live page
- 0 titles over 60 characters
- 0 invalid JSON-LD blocks
- 0 broken internal links, 0 links pointing at a redirect source
- 0 live pages missing from the sitemap, 0 redirect sources listed in it
- 0 countdown scripts referencing `DEC15` without defining it
- 0 duplicate call bars or link blocks

**Result: no problems found.**

Also: 4 page renders in headless Chromium at 1280px and 390px — 0 page errors,
0 horizontal overflow; calculator flow driven end-to-end including validation
rejection on a bad ZIP.

One defect was caught by verification rather than by review: the first pass of
the countdown fix matched only the 5 spaced-format files and not the 46 minified
ones, which declare `START` and `END` in a single comma-separated statement.
Those 46 got the new two-phase branch without the `DEC15` constant it references,
which would have thrown on every page. Caught, fixed in a second pass,
re-verified. The check for it is now permanent in `verify_sep.py`.

`page_lib.py` was also hardened after the donor page — itself a trucking page —
picked up a call bar from this session's own wiring pass and started cloning it
into rebuilt pages.

---

## Not done

- **No meta rewrites on the group/fleet pages.** The action report proposed this.
  Reviewing them, the snippets are already specific and well-written; those pages
  sit at positions 19–31, where CTR is near zero regardless of the snippet. The
  constraint is position, not copy. Internal linking is the lever, and that is
  what was done instead.
- **No AggregateRating schema.** The action report suggested marking up the
  testimonials. Google's structured data policy disallows self-serving reviews
  collected by the business about itself, and there is no review platform behind
  them. Not worth a manual action.
- **No new city pages.** Raleigh is generating real query volume (7 distinct
  trucking queries, ~130 impressions at positions 17–31) and
  `/truck-driver-health-insurance-raleigh-nc` gets 142 impressions at position 31
  with 0 clicks. Deepen that page before adding more cities.
- **`/how-much-does-health-insurance-cost` at position 191 is not a page problem.**
  It is a 301 to `/blog/how-much-does-health-insurance-cost-2026`; the 3,232
  impressions are the old URL decaying out of the index. Nothing to fix.
- **`middleware.js` is untracked and was left alone.** Pre-existing, not part of
  this work, and it carries an API key — commit it deliberately or not at all.

## Watch next

Whether the trucking head terms ("health insurance for truck drivers", 1,139
impressions at pos 53) move once the new internal links are crawled. If they do
not by mid-October, the constraint is off-site authority rather than structure,
and no further on-page work will fix it.

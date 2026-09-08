# Search Console Action Report — Jun 7 to Sep 6, 2026

**Totals:** 296 clicks · 60,485 impressions · 0.49% CTR · avg position ~46

## The one-line read

Impressions grew ~6x (150/day in June to ~900/day now) and average position improved
from 55 to about 25-30. Clicks did **not** move — still ~4/day. You are winning
visibility and losing the click. Almost everything below is about converting existing
impressions rather than chasing new ones.

Also: 37 of the 63 tracked clicks came from the branded query "vs health benefits."
Real non-brand click volume is very small.

---

## 1. Critical technical fixes (do first — highest leverage, lowest effort)

### 1a. 85 orphan pages / 83 pages missing from sitemap
You have 248 HTML pages. The sitemap lists 167. Eighty-five pages have **zero internal
links** pointing at them. Google is spending crawl budget it does not have to spare and
those pages get no internal PageRank.

Trucking pages currently orphaned AND missing from sitemap:

- `/otr-truck-driver-health-insurance` — 0 impressions. Targets OTR drivers. Invisible.
- `/lease-operator-health-insurance` — 0 impressions.
- `/truck-driver-family-health-insurance` — 0 impressions. Query "health insurance for truck drivers and their family" = 40 impressions, position 52.
- `/truck-driver-health-insurance-resources` — 224 impressions, position 37.6.
- `/seguro-medico-camioneros` — 5 impressions, **20% CTR**, position 18.
- `/seguro-medico-owner-operators` — 0 impressions.
- `/costo-seguro-medico-camioneros` — 0 impressions.

**Action:** regenerate `sitemap.xml` from the full page list, then add internal links.
Every trucking page should link to every other trucking page through a shared
"Trucking Coverage Guides" block. Same for the Spanish set.

### 1b. Noindexed pages that are still earning impressions
These carry `noindex,follow` but are pulling real impressions right now:

| Page | Impressions | Position |
|---|---|---|
| /dental-vision-insurance-wisconsin | 611 | 48 |
| /dental-vision-insurance-virginia | 586 | 70 |
| /dental-vision-insurance-utah | 159 | 61 |
| /dental-vision-insurance-west-virginia | 158 | 40 |

Decide deliberately: either they are thin and should be removed and redirected to
`/dental-vision-insurance`, or they are worth keeping and the noindex should come off.
Right now they are in limbo and will decay to zero.

### 1c. Two title tags are over-length and get truncated in the SERP
- `/blog/health-insurance-for-truck-drivers` — 88 chars
- `/truckers-health-insurance` — 84 chars

Both end in "| VS Health Benefits," which is wasted pixels on a page nobody knows you by.
Cut to under 60.

### 1d. International junk impressions are dragging your averages
~3,000 impressions from Vietnam (706), India (484), Philippines (439), UK (354),
Indonesia (285), Turkey (248) — **zero clicks from all of them**. This inflates
impressions and craters site-wide CTR and average position, which makes your reporting
lie to you. Filter to United States for every decision you make from GSC.

### 1e. Mobile is under-indexed relative to your audience
Desktop 40,408 impressions / 0.37% CTR / position 55. Mobile 19,727 / 0.71% / position 34.
Mobile ranks better and converts better but gets a third of the impressions. Truck drivers
search from the cab. Check Core Web Vitals and mobile rendering on the trucking pages
specifically.

---

## 2. Pages ranking too deep to ever earn a click

These have real impression volume and are buried past page 4. Each one is a page you
already paid to write that returns nothing.

| Page | Impressions | Position | Clicks |
|---|---|---|---|
| /how-much-does-health-insurance-cost | 3,232 | **191** | 0 |
| /dental-vision-insurance | 4,781 | 72 | 1 |
| /ppo-health-insurance | 3,726 | 62 | 0 |
| /small-business-health-insurance | 1,923 | 53 | 4 |
| /truck-driver-health-insurance | 1,960 | 49 | 12 |
| /health-insurance-between-jobs | 1,850 | 44 | 0 |
| /deductible-copay-out-of-pocket-explained | 1,434 | 70 | 0 |

`/how-much-does-health-insurance-cost` at **position 191** against "average cost of
health insurance" (2,652 impressions, your single biggest query) is a red flag. Position
191 usually means the page is being partially ignored, not just outranked. Check it for
indexation, thin sections, or a duplicate competing with it. It is also orphaned and
missing from the sitemap.

`/dental-vision-insurance` is your biggest wasted asset: 8,529 impressions across the
dental/vision query family, **zero clicks**, average position 68.

---

## 3. Trucking — the honest diagnosis

**81 trucking queries · 5,327 impressions · 7 clicks · 0.13% CTR · avg position 43.6**

The content is not the problem. `/truck-driver-health-insurance` is 7,500 words with
FAQPage, Service, BreadcrumbList and InsuranceAgency schema and 237 internal links.
It sits at position 49. A page that good stuck that deep is an **authority and
cannibalization** problem, not a content problem.

### 3a. Cannibalization — you have four pages fighting for one query
"health insurance for truck drivers" (1,139 impressions, position 53.6) has four
candidates:

- `/truck-driver-health-insurance` — position 49
- `/blog/health-insurance-for-truck-drivers` — position 22.4
- `/blog/do-truck-drivers-get-health-insurance` — position 34.5
- `/blog/company-truck-driver-health-insurance` — position 29.6

Notice the money page ranks **worst** of the four. Google is splitting signals and
picking your blog posts over your conversion page.

**Action:** pick `/truck-driver-health-insurance` as the single canonical target for the
head term. Then:
1. Rewrite the three blog posts to target genuinely different intents — "do truck
   drivers get health insurance" stays informational, "company truck driver health
   insurance" targets W-2 drivers whose carrier offers nothing.
2. Make every one of them link up to `/truck-driver-health-insurance` with the exact
   anchor "health insurance for truck drivers" in the first 150 words.
3. Consider 301'ing `/blog/health-insurance-for-truck-drivers` into the money page —
   it is the closest duplicate and it is already orphaned and out of the sitemap.

### 3b. Owner-operator queries are your best trucking opportunity
This cluster has volume, commercial intent, and you are already close:

| Query | Impressions | Position |
|---|---|---|
| health insurance for owner operators | 313 | 41.5 |
| health insurance for independent truckers | 264 | 37.9 |
| health insurance for owner operator truck drivers | 257 | 42.2 |
| medical insurance for owner operators | 222 | 41.5 |
| owner operator medical insurance | 211 | 43.6 |
| medical insurance for owner operator truck drivers | 175 | 41.1 |
| owner operator health insurance | 146 | **26.8** (3 clicks) |
| best health insurance for owner operators | 140 | 38.6 |
| owner operator health insurance cost | 35 | **13.0** |

That is ~1,760 impressions sitting at positions 26-44 with three clicks total.
Note the pattern: "medical insurance" variants are a distinct phrasing you barely use
on-page. Add "medical insurance for owner-operators" as an H2 and in the meta
description on `/best-health-insurance-owner-operators`.

### 3c. Group / fleet queries are ranking well and nobody is clicking
These are your highest-value leads (a fleet is worth 10-50x a single driver) and they
are already on page 2-3:

| Query | Impressions | Position |
|---|---|---|
| group health insurance for trucking companies | 75 | 30.7 |
| group health insurance for refrigerated trucking companies | 50 | 22.3 |
| group dental insurance for trucking companies | 30 | 35.0 |
| group health insurance for oilfield trucking companies | 31 | 21.7 |
| group health insurance for heavy haul trucking companies | 31 | 22.1 |
| group health insurance for dump truck fleets | 29 | 20.2 |
| group dental insurance for refrigerated trucking companies | 24 | 19.1 |
| group health insurance for delivery fleets | 16 | 25.2 |

Positions 19-31 with zero clicks means the titles and meta descriptions are not
competitive. These are the cheapest wins on the whole site — rewrite the SERP snippet,
not the page.

### 3d. The Raleigh signal
Seven separate Raleigh trucking queries (health insurance for truckers raleigh, truck
driver health insurance raleigh, health insurance for independent truckers raleigh, etc.)
totaling ~130 impressions at positions 17-31. `/truck-driver-health-insurance-raleigh-nc`
gets 142 impressions at position 30.7 with 0 clicks. Something is generating real demand
there — worth deepening that page before adding new cities.

---

## 4. What to ADD to trucking

Ordered by expected lead impact.

### 4a. An owner-operator cost calculator (highest priority)
Your `/aca-subsidy-calculator` earned **50 clicks on 2,400 impressions** — more clicks
than any page except the homepage. Calculators convert on this site. You already have
`/owner-operator-plan-finder` but it has **1 impression**, no internal links, and a
title that asks a question instead of promising a number.

Build/relaunch as **"Truck Driver Health Insurance Cost Calculator"**: inputs are age,
state of domicile, family size, and 1099 net income. Output is an estimated monthly
premium after subsidy, plus the tax deduction. Gate the emailed PDF version for the lead.
Link it from every trucking page, above the fold.

This directly serves "truck driver health insurance cost" (133 impressions, position 21,
1 click), "owner operator health insurance cost" (35, position 13), and "how much does
owner operator insurance cost."

### 4b. An OOIDA / association plan comparison page
Query "truckers association health insurance" — 31 impressions, position 58. Every
owner-operator researching coverage looks at OOIDA first. A page titled
**"OOIDA Health Insurance vs ACA Marketplace: What Owner-Operators Actually Pay"**
that compares them honestly captures high-intent traffic at the exact moment of decision.
You have this as a section inside `/best-health-insurance-owner-operators` — pull it out
into its own page.

### 4c. Carrier-specific pages
"blue cross blue shield for truck drivers" — 25 impressions, **position 8.5**, zero
clicks, no dedicated page. Drivers search by carrier because they want to know if their
doctor at home is in network. Build a short set: BCBS, UnitedHealthcare, Aetna, Cigna —
each answering "does this network work in all 48 states for a driver."

### 4d. Expand the DOT physical / medical certification cluster
You rank well here and it is the top of the funnel — a driver worried about their medical
card is a driver about to buy coverage:

- "does insurance cover dot physical" — 21 impressions, position 16.7
- "does health insurance cover dot physicals" — 16, position 17.4
- "does blue cross blue shield cover dot physical" — 11, position **2.9**
- "blood pressure requirements for dot physical" — 16, position 59.5
- "are dot physicals covered by insurance" — 7, position 16.4

Add pages for: diabetes and your CDL, vision requirements and the medical card, what
happens if you fail a DOT physical, and DOT physical cost without insurance. Link them
all into `/dot-physical-requirements` as a hub.

### 4e. Spanish-language trucking (badly underserved)
`/seguro-medico-camioneros` gets **20% CTR at position 18** on 5 impressions.
`/seguro-medico-camioneros-florida` gets **33% CTR at position 7.3**. Those CTRs are
extraordinary — there is almost no competition. All three Spanish trucking pages are
orphaned and out of the sitemap. Fix that, add hreflang, and expand: a Spanish
owner-operator cost calculator, a Spanish DOT physical page, and Spanish versions of the
fleet pages. Hispanic owner-operators are a large and growing share of the market.

### 4f. Lease-purchase and new-authority drivers
`/lease-operator-health-insurance` is orphaned with 0 impressions.
`/blog/owner-operator-new-authority-benefits-checklist` has 2 impressions at position 6.5.
A driver who just got their own authority is buying insurance *this month*. Build out
"Health Insurance When You Get Your Own Authority" as a real page with a checklist lead
magnet, and link it from the owner-operator hub.

### 4g. Answer-engine content
86 long conversational queries (8+ words) drove 2,484 impressions at average position 29 —
these are ChatGPT/AI Overview style questions. Example, at position 8:
"which national otr fleets offer the best benefits packages (health..."

Your robots.txt already welcomes GPTBot and OAI-SearchBot, which is good. Add a
comparison page: **"Which Trucking Companies Have the Best Health Benefits?"** listing
major carriers' benefit packages with a clean comparison table. It will get cited by AI
assistants and it captures company drivers at the exact moment they realize their carrier's
plan is bad — then routes them to your ACA option.

---

## 5. Conversion fixes (clicks you already have, leads you are not getting)

- **Homepage is your best converter** — position 6, 4.94% CTR, 71 clicks. `/client` is
  at 5.33% CTR. Make sure the homepage has a trucking-specific entry point above the fold.
- **Sticky click-to-call on mobile** for all trucking pages. A driver at a truck stop
  will call, not fill a form.
- **Rewrite meta descriptions** on the fleet/group pages (section 3c) with a number in
  them — "from $X per driver per month" beats a generic description.
- **Add review/rating schema** where you legitimately have testimonials. The trucking
  page already has a testimonials section but no `AggregateRating` markup.
- `/quote` gets 588 impressions at position 37 with 2 clicks. Your conversion page is
  effectively invisible in search — that is fine, but it means 100% of quote traffic has
  to come from internal links. Audit that every trucking page has a visible quote CTA
  in the first screen.

---

## 6. Time-sensitive: open enrollment

Open enrollment queries are already your strongest non-brand cluster — 3,328 impressions,
13 clicks, average position 27. `/blog/aca-open-enrollment-2027-guide` earned 25 clicks
on 5,372 impressions at position 15, your best content page by a wide margin.

Near-page-one and climbing:

- "when is open enrollment for health insurance 2027" — 1,057 impressions, position 8.9
- "insurance open enrollment deadline" — 82, position 9.4
- "when is open enrollment healthcare.gov" — 49, position 8.1
- "when does open enrollment start for 2027" — 49, position 18.5
- "when is open enrollment for health insurance 2027 florida" — 37, position 10.0

OEP starts Nov 1. Refresh that guide now with exact 2027 dates, add a state-deadline
table, and build the trucking-specific version: **"Open Enrollment 2027 for Truck Drivers:
Dates, Deadlines and What to Do From the Road."** That single page could carry the whole
Q4 lead push.

---

## Suggested order of execution

1. Regenerate sitemap + fix the 85 orphans (one afternoon, biggest structural gain)
2. Resolve the trucking cannibalization — pick one canonical page for the head term
3. Rewrite titles/metas on the group-fleet pages sitting at position 19-31
4. Ship the owner-operator cost calculator
5. Refresh the open enrollment guide + build the trucking OEP version before Nov 1
6. Diagnose `/how-much-does-health-insurance-cost` (position 191)
7. Un-orphan and expand the Spanish trucking set
8. Build the OOIDA comparison and carrier-specific pages

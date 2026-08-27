# Small business SEO — Texas, Maryland, Kentucky — 27 August 2026

Scope agreed with Bradley: state hubs **plus** a supporting blog cluster, everything
pointing at `/quote?type=business`, licensed in all three states, committed but not pushed.

Florida already has 30-plus small-business pages, so nothing new was built for it — instead
the Florida cluster picks up internal links from all eight new pages and appears in every
state comparison.

---

## The rule this build follows

The 25 August pass ended with a warning: templated near-duplicates are what got the
dental-vision cluster 301'd in July. So these three state pages are **not** find/replaced
siblings. Each leads with a different verified fact, and the facts are genuinely different
because the states genuinely are.

Everything below is sourced to a primary document. Where a source could not be found,
nothing was written — there are no invented premium figures anywhere in this build.

---

## 1. Three state hubs

### `/texas-small-business-health-insurance` — 1,900 words

**Lead fact: Texas is a two-employee state.** Tex. Ins. Code §1501.002(14) requires an
average of at least two employees in the prior calendar year *and* two on the first day of
the plan year. Nearly every national page says 1–50, and in Texas that is wrong. A genuine
one-person Texas business cannot buy small group coverage at all.

Also covered, all Texas-only and none of it in the competitive set:

- **Two spouses count as a group in Texas.** Federal guidance says no; TDI has told carriers
  they must issue anyway, because Texas elects to regulate a two-employee group as a small group.
- **A tobacco load cannot be charged to an individual employee.** TDI treats tobacco as a
  health status factor under §1501.002(7); §1501.206 bars individual health-status rating.
  A surcharge "must be applied uniformly to the rates charged for all members."
- **27 rating areas, and no rural area since 2023.** DFW is split across Areas 8 and 25;
  the Rio Grande Valley across 15 and 5. A two-office Texas employer is not one price.
- **75% participation** — Texas is one of only eight states healthcare.gov names above the
  standard 70% — and the **Nov 15 – Dec 15** federal waiver window.
- Sole proprietors reach small-group rules only via a health group cooperative (§1501.051(3-a)).
- Texas has the highest uninsured rate in the country: 16.8% in 2024 vs 8.2% nationally.

### `/maryland-small-business-health-insurance` — 1,700 words

**Lead fact: Maryland is one of the last states with a small business exchange that works.**
MHC for Small Business has a live employer portal, a current employer guide and three
carriers (CareFirst, UnitedHealthcare, Kaiser). That matters concretely, because buying
through the exchange is generally the only route to the federal tax credit — and Employee
Choice, where staff pick across all carriers at two metal levels, exists nowhere else nearby.

- **Nobody in Maryland pays a tobacco surcharge.** Md. Ins. Art. §15-1205 permits 1.5:1, but
  MHBE's carrier reference manual states the exchange "cannot accommodate tobacco rating," so
  no carrier has filed a factor. Worded carefully — Maryland does *not* ban it, the platform
  cannot process it. Real money against Virginia, Delaware and Pennsylvania.
- **Four rating areas, and Frederick and Carroll are in Western Maryland**, not the DC-suburb
  area. Area 3 is Montgomery and Prince George's only.
- **The Nov 15 – Dec 15 window is in Maryland statute**, not just federal market rules
  (§15-1206) — and it waives participation only, not contribution.
- **Level-funded is bounded here.** §15-129 sets a $22,500 specific and 120%-of-expected
  aggregate stop-loss floor for small employers. The page says so plainly rather than
  pitching level-funded as a universal win.
- 2026 approved small group increase: 4.9% average, below the 5.5% requested. ~203,000
  Marylanders in small group plans.

### `/kentucky-small-business-health-insurance` — 1,700 words

**Lead fact: kynect's SHOP is closed.** KHBE states that Anthem, the sole issuer, will no
longer offer SHOP plans and that "employers can no longer apply and enroll in SHOP coverage
in Kentucky." Almost no page on the web has caught up with this. Consequences: no portal to
shop, and the federal tax credit route is effectively shut for new purchasers (IRS Notice
2018-27 is the only relief, and only mid-period).

- **Two-employee floor**, KRS 304.17A-005(44), same structure as Texas.
- **Tobacco ceiling is 1.4:1, not 1.5:1** — published by both CMS and KY DOI. Deliberately
  attributed to those two sources and **not** to a statute section: no KRS or KAR setting
  1.4:1 could be located, and inventing a citation on a legal point is how a page gets pulled.
- **Any willing provider (KRS 304.17A-270)** — why narrow-network savings pitches
  underdeliver in Kentucky. Genuinely useful and nobody writes it.
- **Mini-COBRA: 18 months for employers under 20** (KRS 304.18-110) — the single most
  commonly missed obligation for a 2–19 employee Kentucky group, and it does not apply to
  level-funded.
- $30/30-day insulin cost-sharing cap; stuttering therapy with no visit cap and no prior auth.
- 8 rating areas; Louisville 3, Lexington 5, Northern Kentucky 6, Bowling Green inside 4.

---

## 2. Five supporting blog posts

Written against real query phrasing, each cross-linked to its state hubs and the group quote.

| Post | Angle |
|---|---|
| `/blog/how-many-employees-do-you-need-for-group-health-insurance` | The answer differs in all four states. FL 1, TX 2, MD 1-plus-a-non-owner, KY 2. |
| `/blog/group-health-insurance-minimum-participation` | The denominator is smaller than employers think, and the Nov 15 – Dec 15 window suspends the rule. Highest-intent post in the set. |
| `/blog/small-business-health-care-tax-credit-2026` | $34,100 wage figure (Rev. Proc. 2025-32), two-year limit, and the SHOP gate that now breaks in Kentucky. |
| `/blog/small-business-health-insurance-cost-2027` | The one honest benchmark (MEPS-IC 2024, national) and why a state average describes no real employer. |
| `/blog/ichra-vs-group-health-subsidy-cliff` | Enhanced PTCs expired 12/31/25; the 400% FPL cliff is back. Proved from the IRS applicable-percentage tables for 2026 and 2027. |

The cost post **declines to publish a state average premium** and says so, with the reason.
That is a differentiator, not a gap — every competitor page invents one.

---

## 3. Wiring

- **35 small-business cluster pages** given a "Group coverage by state" block linking FL, TX,
  MD and KY. The three new hubs link to each other and to Florida.
- **Blog index**: five new cards at the top of the grid.
- **12 in-content CTAs** on the state hubs and 10 across the blog posts, all
  `/quote?type=business`. Header, nav and footer stay generic `/quote`.
- **Schema**: Service (with `areaServed`, `BusinessAudience` 1–50 or 2–50 per state, and
  `availableChannel` pointing at the group quote form), FAQPage and BreadcrumbList on each
  hub; Article, FAQPage and BreadcrumbList on each post.
- **Sitemap rebuilt**: 125 → 133 URLs, the three hubs at priority 0.9.

---

## 4. Three pre-existing bugs found while verifying

Not part of the brief, but cheap and material.

1. **43 pages still said Open Enrollment runs "Nov 1 – Dec 15."** Commit 83494b4 corrected
   this to January 15 but missed them. All 43 now corrected. This is the exact regression the
   monthly scheduled check was set up to watch for, and it was already live.
2. **9 pages ran the scroll-progress script with no `#vs-scroll-bar` element**, throwing a
   TypeError on every single scroll event. Affected `tampa-small-business-health-insurance`,
   `florida-small-business-health-insurance`, `small-business-health-insurance`,
   `group-health-insurance-by-industry`, `truckers-health-insurance` and `book`. Element added.
   `build_tampa.py` had the same omission, so `state_lib.py` was written to include it.
3. **5 content pages had no announcement bar at all.** Added.

---

## Verification

- 0 structural HTML problems across 81 changed pages
- 0 invalid JSON-LD
- 0 broken internal links, 0 links to redirect sources
- Exactly 1 title / description / canonical / h1 per new page; titles ≤60 chars, descriptions 144–154
- Texas, Kentucky, Tampa and one blog post rendered in headless Chromium at 1280px and
  visually checked, top and mid-page, with scroll — **0 JavaScript errors** after the fixes
- sitemap.xml parses, 133 URLs

## Not done

- **No new Florida pages.** Florida already has the cluster; it gains links, not bulk.
- **No city pages for TX, MD or KY.** Same reasoning as the 25 August pass: earn the state
  pages first, then deepen. Houston, Dallas, Baltimore and Louisville are the obvious next
  three if these move.
- **No carrier names on the Texas or Kentucky pages.** Maryland's three exchange carriers are
  published by MHBE and are safe to state; the Texas and Kentucky small group carrier rosters
  could not be verified from a primary source, so nothing was claimed.
- **No state-specific premium figures anywhere.** There is no reliable published source.
  The pages say so and ask for a census instead — which is also the better lead capture.

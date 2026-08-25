# Small business SEO — 25 August 2026

Second pass, focused on employers. Scope agreed with Bradley: **South Florida first**,
and **fix the existing pages as well as adding the missing cluster**.

## The diagnosis

You did not have a content gap. You had 31 small-business pages and roughly 55,000 words
already. Last quarter they produced:

| | |
|---|---|
| Small-business queries | 192 |
| Impressions | 3,044 |
| **Clicks** | **1** |

So nothing here adds bulk. It fixes what the existing pages say, and adds only the one
cluster that had genuine demand and no page at all.

---

## 1. Titles rewritten to match how people actually search

GSC shows the demand is phrased **"group health insurance for [trade]"** and
**"group health insurance [city]"**. Your pages all said *"health insurance for [trade]"*
and *"small business health insurance [city] | Free Quote"*.

That is why `group health insurance coral gables` sits at position **8.1** while
`small business health insurance florida` sits at **50.9** — the one page whose title
happened to match the phrasing is the one that ranks.

26 pages retitled, leading with "Group Health Insurance". All titles ≤60 characters,
descriptions 130–158. og and twitter mirrors updated with them.

## 2. The cluster you ranked for with no page

These were pulling impressions against generic pages:

| Query | Impressions | Position |
|---|---|---|
| group health insurance for janitorial companies | 28 | **19.2** |
| group health insurance for multi location retailers | 43 | 26.2 |
| group health insurance for refrigerated trucking companies | 35 | 28.1 |
| group health insurance for industrial cleaning contractors | 46 | 29.2 |
| group health insurance for trucking companies | 64 | 32.3 |
| group health insurance for tunneling contractors | 42 | 36.6 |
| group health insurance for bridge construction contractors | 40 | 37.2 |
| group health insurance for excavation contractors | 39 | 37.5 |
| group health insurance for general contractors | 55 | 41.0 |
| group health insurance for retail stores | 26 | 41.2 |

**Deliberately not built as ten new pages.** Templated near-duplicates are exactly what got
your dental-vision cluster 301'd in July. Instead:

- **New hub: `/group-health-insurance-by-industry`** — 10 trade cards, the rating explainer,
  the four decisions every small group faces, 6 FAQs, Service + FAQPage + BreadcrumbList schema.
- **Trade sections added to 4 existing pages** — construction (general/excavation/bridge/
  tunneling), cleaning (janitorial/industrial), retail (single store/multi-location/chains/
  seasonal), trucking (reefer/fleet types/leased operators).

## 3. Two facts that do the differentiating

Both verified, both things competitors' pages do not say:

**Your trade does not raise your health premium.** Owners in high-hazard trades assume group
health is priced like workers' comp — class code, claims history, experience mod. It is not.
Under the ACA a group of 1–50 in Florida can be rated only on employee age, geographic rating
area, family size, tobacco use and plan selected. Industry and claims are not permitted rating
factors. This corrects a genuinely common and expensive misconception, and it is the kind of
answer that gets cited by AI search.

**Davis-Bacon fringe credit.** On federally funded work, bona fide health contributions count
toward the fringe obligation instead of being paid as cash — subject to annualization across
all hours worked, DBRA and non-DBRA. Sourced to DOL WHD Fact Sheet 66E. Directly relevant to
the bridge, tunneling and excavation queries above.

## 4. Everything points at /quote

- **`/quote` now accepts a deep link**: `?type=business` (also `group`, `employer`, `company`)
  lands the visitor straight on the group form instead of the individual/business chooser,
  and scrolls to it. Falls back silently if anything is missing.
- **170 in-content CTAs across 28 pages** repointed to `/quote?type=business`.
  Header, nav and footer links stay generic `/quote` — those serve every visitor, not just employers.
- Every trade section, the hub, and every cross-link block ends in a group-quote CTA.

## 5. Structure

- **32 pages cross-linked** into the small-business cluster: hub, calculator, cost, Florida
  hub, requirements, ICHRA, level-funded. Card sets chosen per page, not repeated.
- **Service schema** with `areaServed` (11 South Florida cities + Florida + US),
  `BusinessAudience` (1–50 employees) and `availableChannel` pointing at the group quote form,
  added to 14 industry and pillar pages.
- Hub linked from `/services` and the pillar page.
- Sitemap rebuilt: 120 URLs, hub at priority 0.9.

---

## Verification

- 0 structural HTML problems across 34 changed pages
- 0 invalid JSON-LD
- 0 broken internal links, 0 links to redirect sources
- 1 title / description / canonical / h1 per page
- Hub and construction page rendered in a browser and visually checked
- sitemap.xml parses, vercel.json valid

One repair worth noting: an offset bug in an inline edit split a `</li>` tag on
`services.html`. Caught by the structural parser, fixed, re-verified.

## Not done

- **No new city pages.** You have 11. Adding Aventura, Weston, Davie and Boca as templated
  siblings is the dental-vision mistake again. Better to deepen the 11 with real local detail.
- **Tampa, Orlando, Jacksonville.** `business health insurance tampa` is at position 36.8 with
  no page. Out of scope for South Florida first — worth revisiting once the local pages move.
- **Real carrier and pricing data per city.** Still broker work; I will not invent premiums.

# COBRA cluster — 27 August 2026

Scope agreed with Bradley: one pillar page and three blog posts for people who
have just been handed a COBRA election notice, led on the commercial "get a
lower rate" angle, feeding the existing `/cobra-vs-marketplace-calculator`.

Audience is individual, not employer, so every CTA here points at
`/quote?type=individual` rather than the group form.

---

## Why this audience is worth the pages

Someone holding a COBRA election notice already has the number, already has a
deadline, and is already looking for a cheaper answer. There is no persuasion
step. The only question is whether they find you inside their 60 days.

Keyword research turned up something better than volume, though: **the entire
first page of this topic is stale.** Of eleven substantive competitor pages
checked, eight make no mention of the enhanced premium tax credits expiring at
the end of 2025 or the 400% FPL subsidy cliff returning — including four dated
within the last six months and two dated this month. healthinsurance.org, one of
the highest-authority consumer pages in the space, was modified in May 2026 and
still reads "The American Rescue Plan has temporarily eliminated the subsidy
cliff (through 2025)" in the present tense.

And on the query with the strongest commercial intent — "COBRA is too expensive,
what are my options" — **no government result appears at all.** That SERP is
entirely broker and content sites, which is unusual for a health-insurance topic
and means the page is winnable.

---

## 1. `/cobra-alternatives` — 1,900 words

Title: *COBRA Alternatives: Cheaper Coverage Options*

**Leads on the cost shock**, because that is what the searcher is feeling. Your
COBRA quote is not a markup — federal law caps it at 102% of the plan's full
cost, and your payroll deduction was only ever a share of that. Against the KFF
2025 employer survey averages: single goes from about $120 a month to about $793,
family from about $571 to about $2,294. Roughly 6x and 4x. Those multiples are
computed from KFF totals and labelled as illustration, not presented as survey
findings.

**Then six things that cost less**, ordered by how often they actually win —
spouse's plan first, because it is usually cheapest and always forgotten, then a
subsidised marketplace plan, Medicaid, a parent's plan under 26, an ICHRA for
anyone going self-employed, and short-term plans last with an honest warning
about what they exclude.

**Then the clock**, which is longer than the notice makes it look: 30 days for
the employer to notify plus 14 for the plan to send means the notice can legally
take 44 days to arrive; you then get 60 days to elect and 45 more to pay.

**One thing kept in regardless of the commercial angle.** A prominent boxed
warning that voluntarily cancelling COBRA mid-year does not open a special
enrollment period — 45 CFR 155.420(e)(1) excludes it, and HealthCare.gov says
"voluntarily dropping COBRA doesn't count." Someone who cancels in April with
nothing lined up is uninsured until January. That is not a downer on a
lead-gen page; it is the reason to call a broker rather than click a button,
and it is the single most under-served fact in the whole topic.

Closes with four things to check before switching — met deductible, mid-treatment
care, projected income against the 400% cliff, and the Medicare Part B trap where
the 8-month window runs from the end of *employment*, not the end of COBRA.
Framed as qualification, not as an argument for COBRA.

## 2. Three blog posts

| Post | Why this one |
|---|---|
| `/blog/why-is-cobra-so-expensive` | The cost-shock query, and the SERP with **no government competition at all**. Explains the 102%, the 2% admin fee, the 150% disability rate, and the HSA exception almost nobody knows about. |
| `/blog/cobra-60-day-loophole` | An existing high-traffic hook — one competitor has 5,200 words on it — reframed correctly. Their guide never warns readers about cancelling, and none of them mention the waiver trap. |
| `/blog/can-i-drop-cobra-for-marketplace` | The switching-mechanics cluster, where KFF ranks and commercial supply is thin and often wrong. Both branches of the rule, as a table, up front. |

### The two facts that do the differentiating

**Exhausting COBRA and cancelling COBRA are opposites.** Running out the full
18 or 36 months is a qualifying event and opens a fresh 60-day window.
Cancelling early opens nothing. Same ending for your coverage, completely
different consequence for your options. Of ten ranking pages checked, not one
states both branches plainly where a panicking reader will see them — several
give only the half that sounds reassuring.

**Do not sign the waiver.** COBRA is retroactive if you simply have not replied,
which is what makes the 60-day window a free option. But 26 CFR 54.4980B-6
provides that where a waiver is later revoked, coverage "need not be provided
retroactively" — so returning the declination form and changing your mind on day
50 can leave a genuine uninsured gap. Every "60-day loophole" page on the web
omits this, and it is the one that actually costs people money.

Also included and rarely covered: **COBRA premiums can be paid tax-free from an
HSA.** Insurance premiums generally cannot be, but continuation coverage is a
written exception in IRC 223(d)(2)(C), as is coverage while collecting
unemployment. For a recently laid-off person with a funded HSA that is often
several months of coverage they have already paid for.

---

## 3. Wiring

- **12 pages** cross-linked into the cluster: the calculator, between-jobs, the
  job-loss post, the SEP checker, qualifying life events, before-Medicare,
  how-to-shop and affordable-health-insurance, plus the four new pieces pointing
  at each other.
- **13 CTAs** across the four new pages, all `/quote?type=individual` — the
  deep-link handler already accepts `individual`, `family`, `personal` and `self`.
- Three cards added to the blog index.
- Sitemap 133 → 137 URLs; `/cobra-alternatives` and the calculator at 0.9.
- Schema: Service + FAQPage + BreadcrumbList on the pillar, Article + FAQPage +
  BreadcrumbList on each post.

---

## 4. A CSS bug found and fixed

`.vs-ih-key strong{display:block}` in the Tampa page's style block — inherited by
every page built from it — forced *any* bold inside a callout box onto its own
line, so inline emphasis rendered as orphaned fragments. Caught in a headless
render of the new COBRA warning box, where it made a bulleted list unreadable.

Now scoped to `.vs-ih-key>strong` with an explicit inline override for bold
inside paragraphs and list items. Fixed in `state_lib.py`, in `build_tampa.py`,
and on the Tampa page itself, which carried the latent bug without visibly
breaking. The Texas, Maryland and Kentucky hubs from this morning were rebuilt
with the fix — Maryland had two affected paragraphs.

---

## Verification

- 0 structural HTML problems, 0 invalid JSON-LD, 0 broken internal links,
  0 links to redirect sources
- Titles 36–50 chars, descriptions 129–153
- Rendered in headless Chromium at 1280px: 0 JavaScript errors, and a scripted
  assertion that no bold inside a callout box computes to a non-inline display

## Worth flagging

**The site-wide banner says Open Enrollment for 2027 runs "Nov 1 – Jan 15."**
The 2025 Marketplace Integrity and Affordability final rule states that from
plan year 2027 the federally-facilitated exchange window runs November 1 to
**December 15**, while HealthCare.gov's consumer dates page still displays the
old January 15 schedule, and there is active litigation touching that rule.
I did not change the banner — the January date was set deliberately in commit
83494b4 and I cannot confirm which is now correct. The new COBRA pages avoid
printing a hard end date for this reason. **Re-verify in October**, before open
enrollment traffic arrives; this is exactly what the monthly scheduled check
should be asked to look at.

## Not done

- **No changes to the calculator.** Making its first question household size and
  projected income — routing to a COBRA-wins or marketplace-wins verdict — is
  the single biggest remaining opportunity here and has no real competitor.
  Out of scope for this pass; worth its own.
- **No state-specific COBRA pages.** Mini-COBRA rules differ by state and the
  pages acknowledge it, but building per-state continuation pages would be the
  dental-vision mistake again.

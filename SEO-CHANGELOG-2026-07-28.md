# SEO Overhaul — 28 July 2026

Branch: `seo-overhaul-2027` · 135 files modified · all changes are on disk, **not committed** (see "Git" below).

---

## Two things I need from you

**1. Confirm your business address.** Your homepage had *two conflicting* `InsuranceAgency` schema blocks: one saying Miami, FL and one saying **7901 4th St N Ste 300, St. Petersburg, FL 33702**. Conflicting NAP data is one of the most damaging local-SEO signals there is — Google sees two addresses for one business and trusts neither. I removed the St. Petersburg block (all 42 other schema references say Miami) and left `"streetAddress": ""` in `index.html` for you to fill in. **If St. Petersburg is your real registered address, tell me and I'll flip it the other way** — but it has to be one, and it has to match your Google Business Profile exactly.

**2. Verify the state deadline table before November.** The open-enrollment end date is genuinely unsettled — a federal judge vacated the shortened-enrollment rule in June 2026 and HHS may appeal. My source (healthinsurance.org, updated 13 July 2026) does **not** state the HealthCare.gov end date, which is the one that matters for Florida clients. I've marked that row "confirm before you rely on it" and stamped the table "Last verified July 28, 2026". As a licensed broker publishing enrollment deadlines, re-verify each state against its own exchange before October.

---

## What changed

### Titles and meta descriptions — the biggest click win
102 of 164 titles were over 70 characters (Google shows ~55–60), and nearly all ended in `| VS Health Benefits`, a brand almost nobody searches, eating the pixels where your differentiator belongs.

- **91 titles rewritten.** Average length 72.6 → **48.4 chars. Zero now exceed 60.**
- Query-first phrasing, brand suffix dropped everywhere except brand pages (`/`, `/about`, `/contact`, `/bradley-vilsaint`, legal pages)
- Year updated 2026 → **2027** across titles and metas — people are already searching 2027
- **89 meta descriptions** rewritten answer-first, all under 170 chars
- `og:title` / `twitter:title` synced across 164 tags

This targets the band where you had **1,084 impressions on page one producing 3 clicks** (0.28% CTR).

### Technical bugs found and fixed
These were actively suppressing rankings:

| Bug | Impact | Fixed |
|---|---|---|
| **9 canonicals pointed at URLs that 301** — including `/quote`, `/contact`, `/services`, `/blog`. Six pointed at non-www **and** `.html`, a double redirect | Google may ignore the canonical entirely and treat the page as a duplicate | All canonicals now self-referencing, www, extensionless |
| **`/health-insurance-for-salons-and-spas` canonicalised to a different page** | That page could never rank on its own | Now self-referencing |
| **37 redirected URLs still listed in the sitemap** | You were telling Google to crawl pages that 301 | Sitemap rebuilt from live pages only (121 → 81 URLs) |
| **123 internal links pointed at redirected URLs** | Every one leaked link equity through an unnecessary hop | All repointed to final destinations |
| **`/health-insurance` was missing from the sitemap** — while being the redirect target for 31 state pages | The designated hub for all state traffic was invisible | Added, priority 1.0, H1 rewritten to target the query |
| **PPO page had a structurally broken final CTA** — its `<section>` and two `<div>` wrappers were missing, leaving an orphaned `<h2>` and 2 stray `</div>` | The conversion block on a 1,123-impression page rendered unstyled | Restored; verified 0 nesting errors site-wide |
| **2 internal links 404'd** (missing `/blog` prefix) | Dead links | Fixed |
| **24 internal links used `.html`** | Unnecessary redirect hop on the blog hub | Stripped |

### Duplicate content
Your 64 near-identical state pages were **already redirected** in `vercel.json` before I started — that work was done. What was missing was the cleanup: they were still in the sitemap and still internally linked. Both fixed.

I consolidated **10 more duplicate URLs** (20 rules incl. `.html` variants):

- **Open enrollment: 2 pages → 1.** `/health-insurance-open-enrollment-faq` (pos 18.2) merged into `/blog/aca-open-enrollment-2027-guide` (pos 11.1). Its 6 unique Q&As moved into the guide's visible content *and* FAQ schema — now 14 schema entries. This was splitting your single biggest non-brand query.
- **Trucking: 4 thin pages folded** into the hub and the owner-operator page
- `/individual-dental-vision-insurance` → `/dental-vision-insurance` (near-duplicate of parent)
- 3 more small-business and "near me" overlaps resolved

I deliberately **kept** the 4 Spanish pages and the 2 trucking geo pages — those are substantial, differentiated, and a genuine competitive edge for a Miami broker. Not duplication.

Verified: **no redirect loops, no multi-hop chains, every target is a live page.**

### Content
- **State-by-state deadline table** added to the open-enrollment guide (+4.6KB, page now 3,918 words) with the vacated-rule explanation, a "last verified" stamp, and a maintenance comment for you. This is the link-earning asset — almost nobody has it laid out cleanly, and keeping it current is what will make it rank.
- **Answer-first blocks** added to 6 top-volume pages (dental/vision, truck driver, small business, PPO, owner-operator, health-insurance hub) — direct answers in the first 40 words to capture featured snippets and AI Overview citations. No invented figures; all structurally accurate.
- **De-Florida'd the national pages.** Your PPO page ranked for national *"ppo insurance"* while its H1 read *"PPO Health Insurance Plans in Florida."* A searcher in Ohio skips that. Fixed on PPO (H1 + 4 headings), small business (H1: now "2 to 50 Employees"), and the health-insurance hub. Genuinely Florida-scoped sections kept as-is.
- **`/quote` rebuilt for search:** title 69 → 49 chars, H1 now query-targeted, and **Service + FAQPage + BreadcrumbList schema added — it previously had none at all.**

---

## Verification

All checks pass: titles ≤60 · metas present · canonicals correct · no redirect loops or chains · every redirect target live · sitemap clean · no broken internal links · all JSON-LD parses · div nesting balanced on all 85 pages · single business locality in schema.

Pages rendered in a real browser to confirm: **0 JavaScript errors** across the PPO, dental, open-enrollment, and quote pages.

---

## Git

I could not commit. Git cannot operate in the folder over the desktop bridge — it can't unlink its own lock files (`Operation not permitted`), and the repo already had several stale `index.lock` files from earlier sessions. **Your file changes are all safely written to disk** on branch `seo-overhaul-2027`.

To commit yourself:

```bash
cd ~/Desktop/VS-BENEFITS
rm -f .git/index.lock* .git/HEAD.lock*
git add -A
git commit -m "SEO overhaul: titles, canonicals, duplicate consolidation, state deadline table"
git push -u origin seo-overhaul-2027
```

Review on GitHub, then merge to `main` to deploy via Vercel.

---

## After you deploy

1. **Resubmit the sitemap** in Search Console (`/sitemap.xml`) and request indexing on the open-enrollment guide, `/quote`, and `/health-insurance`.
2. **Check Pages → Not indexed** for "Duplicate without user-selected canonical." Given the canonical bugs I fixed, expect that number to fall over the next few weeks.
3. **Set up Google Business Profile** if it isn't live. A Miami broker should be in the local pack for "health insurance broker near me." Your `/health-insurance-near-me` page sits at position 80 — that's a GBP job, not a landing-page job.
4. **Watch the 4–10 position band.** That's where the title rewrites pay off, and it should move within 2–4 weeks. If CTR there doesn't lift from 0.28%, the titles need another pass.

## The honest ceiling

Everything above is on-page, and on-page work has a limit. **88% of your impressions sit at position 30+ because the domain has no links.** No title rewrite moves position 52 to position 5. To rank #1 on competitive national terms you need off-site authority, and your realistic edge is the trucking niche — Overdrive, TruckersReport, OOIDA-adjacent outlets, owner-operator forums — where you have real expertise and the competition is thin. That plus a maintained state deadline table is the path. The technical foundation is now clean enough that links will actually compound.

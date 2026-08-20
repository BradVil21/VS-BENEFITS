# SEO + AI Visibility Build — 20 August 2026

12 new pages, ~31,900 words, plus an AI-search layer and internal linking.
All files written to `~/Desktop/VS-BENEFITS`. **Not committed to git** — see "Git" below.

---

## What was built

### 6 new landing pages (top-level, extensionless via `cleanUrls`)

| URL | Targets | Words |
|---|---|---|
| `/ichra-florida-small-business` | "ICHRA Florida", "ICHRA small business" — you had **zero** ICHRA coverage | 3,206 |
| `/level-funded-health-insurance-florida` | "level funded health insurance" — you mentioned it, never ranked for it | 2,855 |
| `/florida-small-business-health-insurance-requirements` | "does my business have to offer health insurance" — high volume, high intent | 2,860 |
| `/trucking-company-health-benefits-florida` | Small carriers (5–50 trucks) — the trucker/small-business overlap you own | 3,194 |
| `/occupational-accident-vs-health-insurance` | Genuinely thin competition; the highest-intent owner-operator query on the site | 3,069 |
| `/florida-health-insurance-answers` | AI-citation hub — 30 sourced Q&As | 3,154 |

### 6 new blog posts

| URL | Angle |
|---|---|
| `/blog/sleep-apnea-cpap-cdl-health-insurance` | There is no FMCSA sleep apnea rule — and what a CPAP actually costs |
| `/blog/cdl-blood-pressure-health-insurance` | The Stage 1/2/3 thresholds that set your certification length |
| `/blog/owner-operator-new-authority-benefits-checklist` | New MC number → the coverage checklist nobody hands you |
| `/blog/ichra-vs-group-health-florida` | Head-to-head with four worked scenarios |
| `/blog/section-125-cafeteria-plan-florida` | 7.65% payroll tax saving most employers skip |
| `/blog/small-trucking-company-driver-retention-benefits` | What the turnover research actually says |

---

## Why these topics

Your site already had ~85 pages and covered the obvious terms well. Everything above fills a
gap you did not have, rather than competing with a page you already own. Given your last audit
had to redirect 64 near-duplicate state pages, avoiding cannibalisation was the constraint.

The two biggest genuine holes were **employer funding models** (ICHRA, QSEHRA, level-funded,
Section 125 — you referenced them in passing but had no page to rank) and **DOT-medical-adjacent
trucker content** (sleep apnea, blood pressure, occupational accident), where search intent is
high, the queries are specific, and competition is thin because most brokers can't write it.

---

## AI search visibility

This is the part that gets you cited in ChatGPT, Claude, Perplexity and Google AI Overviews.
Different mechanics from blue-link SEO.

**`llms.txt`** (new file at site root) — the emerging convention for telling language models
what a site is and what it covers. Yours includes a verified-facts block (2027 enrollment dates,
penalty amounts, affordability percentages, Florida statute citations) and a categorised link
index. It explicitly tells models to send quote requests to `/quote`.

**`robots.txt` rewritten** — was 4 lines. Now explicitly allows 22 named AI crawlers: GPTBot,
OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot,
Google-Extended, Applebot-Extended, meta-externalagent, Amazonbot, DuckAssistBot, MistralAI-User,
CCBot, Bingbot and others — with `/admin`, `/client` and `/census` disallowed. A wildcard allow
already permitted these, but several crawlers behave more predictably with a named directive, and
`Google-Extended` specifically governs Gemini grounding.

**Schema on every new page** — WebPage or Article, BreadcrumbList, FAQPage, Service, plus HowTo
where a process is described, plus your InsuranceAgency organisation block. `speakable` markup
points at the answer box and H1.

**Answer-first structure** — every page opens with a bordered "Short answer" block giving a
direct 50–80 word answer before any preamble. This is the single highest-leverage format change
for AI citation: models extract the direct answer, and featured snippets pull from the same block.

**Sourced claims with dates.** Every regulatory figure carries a primary-source citation —
IRS revenue procedure numbers, CFR sections, Florida statute sections — and a "verified August
2026" stamp. Models preferentially cite content that is specific, dated and attributable. Vague
content does not get quoted.

---

## Internal linking

New pages don't rank without links pointing at them. A "Related guides" block was added above the
footer on 8 existing pages:

| Page | Links added |
|---|---|
| `index.html` | 4 |
| `small-business-health-insurance.html` | 4 |
| `truck-driver-health-insurance.html` | 4 |
| `best-health-insurance-owner-operators.html` | 3 |
| `1099-truck-driver-health-insurance.html` | 3 |
| `health-insurance-for-trucking-companies.html` | 3 |
| `florida-small-business-health-insurance.html` | 3 |
| `health-insurance-for-small-business-owners.html` | 3 |

Plus 6 new cards on `blog.html`, and cross-links between the new pages themselves.

`sitemap.xml`: 110 → 122 URLs. New landing pages at priority 0.9, blog posts at 0.8.

---

## Accuracy

Every figure was verified against a primary source before publication. Research agents checked
IRS revenue procedures, the eCFR, Florida Statutes, CMS, FMCSA and KFF. Specific things that were
corrected against what's commonly published elsewhere:

- **Florida's small employer definition is 1–50, not 2–50.** Fla. Stat. § 627.6699(3)(v) starts at
  one and expressly includes self-employed individuals. Most broker sites still say 2–50.
- **Florida law does not require a 50% employer contribution or 75% participation.** § 627.6699(5)(e)(2)
  only requires carriers to apply their own rules uniformly. Those percentages are carrier
  underwriting, not law. This is stated as a correction on two pages because it is so widely repeated.
- **There is no FMCSA sleep apnea regulation.** The rulemaking was withdrawn in August 2017
  (82 FR 37038), and Public Law 113-45 bars FMCSA from imposing one by guidance. The BMI 40 /
  17-inch-neck figures drivers hear were 2016 advisory recommendations that were never adopted.
- **2027 open enrollment is flagged as contested.** CMS's July 31, 2026 statement says Nov 1 –
  Jan 15, but the CFR text still reads the other way and an appeal was pending. The pages say so
  rather than picking a side.
- **Aetna dropped off Florida's 2026 small group carrier list.** Noted on the level-funded page
  with a "confirm before relying on it" caveat.
- **"Allstate Benefits" no longer exists** — Nationwide completed the acquisition in July 2025 and
  the rebrand in February 2026.

Where a figure could not be verified (2026 Small Business Tax Credit wage thresholds, for example),
the page says the 2026 figures aren't published and labels the 2025 numbers as 2025.

---

## Verification run

- All JSON-LD parses (6 schema blocks per page)
- Every title ≤ 60 characters, every meta description ≤ 175
- Canonicals self-referencing, www, extensionless
- Zero internal links to `.html` URLs or to non-existent pages
- Div, section, style and table tags balanced on all 20 modified/new files
- Rendered in Chromium at 390px, 768px and 1280px — **no horizontal overflow on any page**
  (one bug was caught and fixed here: wide tables were stretching the mobile layout via CSS grid's
  default `min-width:auto`)
- Every page links to `/quote` at least 5 times

---

## Git

Same constraint as your last session — git can't operate in this folder over the desktop bridge.
Files are written to disk. To commit:

```bash
cd ~/Desktop/VS-BENEFITS
rm -f .git/index.lock* .git/HEAD.lock*
git checkout -b seo-ai-visibility-aug-2026
git add -A
git commit -m "Add 12 pages (ICHRA, level-funded, trucking, DOT medical), llms.txt, AI crawler rules, internal linking"
git push -u origin seo-ai-visibility-aug-2026
```

Review on GitHub, merge to `main`, Vercel deploys. `cleanUrls: true` is already set, so the new
`.html` files automatically serve at extensionless URLs — no `vercel.json` changes needed.

---

## After you deploy

1. **Resubmit the sitemap** in Search Console and request indexing on the six new landing pages.
2. **Verify `llms.txt` and `robots.txt` serve as plain text** — check `vercel.json` headers if either
   downloads instead of displaying.
3. **Set up Bing Webmaster Tools** if you haven't. ChatGPT search and Copilot both lean on Bing's
   index. This is the cheapest AI-visibility win available and it's usually skipped.
4. **Test your own citations.** In about 2–4 weeks, ask ChatGPT and Perplexity things like
   "does occupational accident insurance cover illness" or "is there an FMCSA sleep apnea rule" and
   see whether you're cited. That's your real KPI here, and nobody else in your niche is measuring it.
5. **Google Business Profile.** Still the gap flagged in your July audit. `/health-insurance-near-me`
   sits at position 80 — that's a GBP problem, not a page problem.
6. **Keep the verified stamps current.** Each new page says "verified August 2026." That date is an
   asset while it's recent and a liability once it's stale. The IRS publishes 2028 figures around
   July 2027; the Florida carrier list updates each October.

## The honest read

Your last audit's conclusion still holds: 88% of your impressions sit at position 30+ because the
domain has no links, and on-page work has a ceiling. What's different about this batch is that the
trucking content is genuinely link-worthy — a clear, sourced explanation that there is no FMCSA
sleep apnea rule is the kind of thing Overdrive, TruckersReport and owner-operator forums link to,
and almost nobody has written it properly. That's the wedge. The small-business funding pages will
convert well but won't earn links on their own.

The AI-visibility work is a different bet with a different payoff curve: it doesn't depend on
domain authority the way blue-link rankings do. A well-sourced, well-structured answer can get cited
by a language model on day one regardless of how many backlinks the domain has. For a small broker
competing against eHealth and the carriers, that asymmetry is worth more than another 20 pages.

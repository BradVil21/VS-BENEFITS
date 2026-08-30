# Google Ads — Small Business Group Health (South Florida)

Built for a **$50 test**. Read the first section before spending it.

---

---

## ⚠ READ FIRST — health insurance ads need certification

**In the US, Google requires advertisers promoting health and medical insurance to be certified
before ads can run.** Certification goes through G2/G2RS, you apply to them first and then to
Google with the documentation. It is not a checkbox in the account and it is not instant.

Without it the campaign below will be **disapproved**, not throttled. The $50 will not spend and
the test will have proved nothing.

**Dental, vision and travel insurance are explicitly NOT restricted.**

That exemption is unusually convenient here, because your dental & vision cluster is the single
biggest hole in the site: **7,361 impressions and zero clicks**, seventeen pages at an
impression-weighted position of 61 — the worst cluster you own. Real demand, no traffic.

So the $50 has a better home than waiting:

| | Health / group | Dental & vision |
|---|---|---|
| Certification | Required, weeks of lead time | **None** |
| Can launch | After G2 approval | **Today** |
| Existing content | Strong | 17 pages, already written |
| Search demand | Proven | 7,361 impressions/quarter |
| Current clicks | Some | **Zero** |

Running the plumbing test on dental & vision proves exactly the same machinery — tag fires, lead
lands labelled `Google Ads`, SMS goes out — on a product that needs no permission slip. And for a
broker, quoting a small employer's dental and vision is a normal way into the medical
conversation, so the leads are not a dead end.

### The certification, concretely

Checked 25 Aug 2026 with G2 Risk Solutions, who run it:

| | |
|---|---|
| Review time | **14 calendar days or fewer** for a complete application. No expedited option. |
| What they verify | That you are licensed to sell health insurance in every jurisdiction you advertise in |
| Documents | Legal business name, domains, **NAIC/NPN codes**, copies of your state licence(s), plus QHP agreement if you sell ACA plans |
| Cost | One-time application fee + annual monitoring subscription, **priced by number of jurisdictions** |
| After approval | A separate application to Google's healthcare advertiser programme — G2RS alone is not enough |

**Certify Florida only, at least to start.** Pricing scales with jurisdictions, and this campaign
targets Miami-Dade, Broward and Palm Beach. Your site says licensed in 40+ states; certifying all
of them for a South Florida test would be paying for 39 you are not advertising in. Add
jurisdictions later if paid actually works.

Two weeks is the real number here — not the months the phrase "certification programme" suggests.

**Recommended sequence**

1. Create the VS Health Benefits Ads account (needed either way).
2. Start G2RS with Florida only — it is the long pole, ~14 days, and nothing else waits on it.
3. Run the $50 on dental & vision (ad group 4) to prove the wiring while you wait.
4. When certification lands, enable ad groups 1-3 — built, paused and waiting.

---

## Ad group 4 — Dental & vision (no certification needed)

Landing page: `https://www.vshealthbenefits.com/dental-vision-insurance-florida`

```
[group dental insurance florida]
[small business dental insurance]
[group dental and vision insurance]
[employee dental insurance plans]
[dental insurance for small business]
[group vision insurance]
"dental and vision insurance florida"
"group dental insurance quote"
```

Negatives for this ad group specifically: `free`, `medicaid`, `medicare`, `dentist near me`,
`emergency dentist`, `braces cost`, `implants` — dental *treatment* searches vastly outnumber
dental *insurance* searches and will eat the budget.

**Headlines** (dental/vision — swap these in, they are within the 30-char limit)

```
Group Dental & Vision Plans
Employee Dental Insurance
Dental & Vision for Teams
Free Group Dental Quotes
Cover Your Staff's Dental
Florida Dental Insurance
No Fee, Licensed Broker
```

## What $50 actually buys, and what to judge it on

Your own account's historical average CPC is **$5.88** (not the $3.39 industry benchmark — your
real number is worse, as insurance usually is). At $5.88, **$50 buys about 8 clicks.** At the
category conversion rate of 2.64% that is **0.2 conversions** — almost certainly zero leads.
One expected conversion needs ~40 clicks (~$235 at your CPC). A trustworthy cost-per-lead needs
several hundred clicks.

So judge this run on **"did the wiring work"**, not on leads:

- [ ] A click arrives and the lead lands in the pipeline labelled `Google Ads`
- [ ] The campaign name shows in the card's notes
- [ ] `phone_click` and `generate_lead` register in GA4
- [ ] The automated SMS goes out

If all four hold, the machinery is proven and a real budget can be pointed at it later with
confidence. If any fail, the $50 found a bug — which is worth more than one lead.

The keywords below are chosen to stretch the money: long-tail, employer-intent and local, which
run well under the $3.39 average. Generic terms like "health insurance florida" run far above it
and are excluded on purpose.

---

## The account situation, as actually found

Checked 25 Aug 2026 under `bradleyvilsaint@gmail.com`. Six accounts exist:

- Four **cancelled** accounts
- **Find Health Coverage Now** (948-217-0695) — active, but its data source is
  `find-health-coverage-funnel.vercel.app`, an abandoned funnel, and its Google tag reads
  "Not installed yet"
- **Luxury For Less Car Service** — unrelated business

**None is VS Health Benefits**, and none matches `AW-17950389267`, which is hardcoded into the
tracking on all 205 pages of vshealthbenefits.com. That ID most likely belongs to one of the four
cancelled accounts — meaning the site's Google Ads conversion tracking has probably been
reporting into a dead account for months.

Decision: a fresh **VS Health Benefits** account. Once it exists, `AW-17950389267` gets replaced
across all 205 pages and in `vs-conversions.js` **before** any spend, so the tracking follows the
money rather than the other way round.

---

## Order of operations (this order matters)

**1. Conversion actions first — before the campaign.**
Creating them is what produces the labels the site is already built to accept. Skip this and the
$50 buys clicks you cannot grade.

Google Ads → Goals → Conversions → New conversion action → Website:

| Action name | Category | Value | Count |
|---|---|---|---|
| Quote Form Lead | Submit lead form | Don't use a value | One |
| Phone Call Click | Contact | Don't use a value | One |

For each, open **Tag setup → Use Google tag** and copy the part **after** the slash in
`AW-17950389267/AbC-D1efGhIjKl`.

**2. Send me both labels.** They go into `vs-conversions.js` (lines 40-43) and I deploy. Until
then GA4 records everything and Google Ads can bid on nothing.

**3. Then build the campaign below.**

---

## Campaign settings

| Setting | Value | Why |
|---|---|---|
| Type | Search only | Display partners burn a small budget on junk |
| Goal | Leads | |
| Networks | **Uncheck** Search Partners and Display | Both, on $50, are waste |
| Locations | Miami-Dade, Broward, Palm Beach | Where your book already is |
| Location option | **People in or regularly in** | Not "interested in" — that serves other states |
| Language | English + Spanish | Your site has Spanish pages and the market is bilingual |
| Budget | **$7/day** | ~7 days of data beats 2 days at $25 |
| Bidding | **Maximize clicks, max CPC $4.00** | No conversion history yet, so tCPA cannot work. The cap stops one click eating a seventh of the test |
| Ad schedule | Mon-Fri 8am-6pm | You answer the phone then. Do not pay for clicks at 2am |

---

## Ad group 1 — Local group health

Landing page: `https://www.vshealthbenefits.com/miami-small-business-health-insurance`

```
[group health insurance miami]
[small business health insurance miami]
[group health insurance coral gables]
[small business health insurance fort lauderdale]
[group health insurance fort lauderdale]
[small business health insurance hialeah]
[group health insurance broward county]
[small business health insurance doral]
"group health insurance miami"
"small business health insurance south florida"
```

## Ad group 2 — By industry

Landing page: `https://www.vshealthbenefits.com/group-health-insurance-by-industry`

Every one of these is a query you already receive impressions for, at positions 19-41.

```
[group health insurance for general contractors]
[group health insurance for trucking companies]
[group health insurance for janitorial companies]
[group health insurance for retail stores]
[group health insurance for restaurants]
[group health insurance for construction companies]
"group health insurance for contractors"
"health insurance for my employees"
```

## Ad group 3 — Employer intent

Landing page: `https://www.vshealthbenefits.com/small-business-health-insurance-calculator`

The calculator converts better than the article pages — 26 clicks from position 31.9.

```
[small business health insurance cost]
[group health insurance quotes]
[how much does group health insurance cost]
[health insurance for small business owners]
"small business health insurance calculator"
"group health insurance quote"
```

---

## Negative keywords (campaign level — add before launch)

Without these, a $50 budget is gone on individual-market and job-seeker traffic.

```
individual
obamacare
medicaid
medicare
free health insurance
healthcare.gov
marketplace
cobra
student
jobs
salary
career
agent jobs
license
how to become
dental only
vision only
pet
travel insurance
life insurance
```

---

## Responsive search ad

**Headlines** (15 — all within the 30-character limit)

```
Group Health Insurance FL
Small Business Health Plans
Health Plans for 2-50 Staff
Cover Your Employees
Free Group Health Quotes
South Florida Group Health
Licensed FL Health Broker
Group Quotes in 2 Minutes
No Cost, No Obligation
Talk to a Licensed Advisor
Employee Health Benefits
Compare Top Carriers
5.0 Stars, 39 Reviews
Level-Funded & ICHRA Plans
Quotes for Small Employers
```

**Descriptions** (4 — all within the 90-character limit)

```
Compare group health plans for your team from top A-rated carriers. Free, no obligation.
Licensed advisor compares your options and handles the paperwork. Quote in 2 minutes.
Covering 2-50 employees in South Florida. Level-funded, ICHRA and traditional plans.
We do not charge you a fee. Get real numbers for your headcount before you commit.
```

Pin nothing. Let Google test combinations — with 15 headlines it needs the freedom.

**Claims check:** every line above is either verifiable (39 Google reviews, 5.0 rating, licensed
in 40+ states, no fee to the client) or non-committal. Nothing promises a price, a carrier
approval or a saving, because you cannot know any of those before seeing a census.

---

## Extensions (these are free clicks-per-impression and most accounts skip them)

**Call extension:** (954) 825-1009 — schedule it to business hours only.
For a broker the call is the conversion, and `phone_click` now tracks it.

**Sitelinks:**

| Text | URL |
|---|---|
| Cost Calculator | /small-business-health-insurance-calculator |
| By Industry | /group-health-insurance-by-industry |
| ICHRA for Florida | /ichra-florida-small-business |
| Get a Quote | /quote |

**Callouts:** No Fee to You · Licensed in 40+ States · 2-50 Employees · Same-Day Quotes

---

## After launch — check on day 2, not day 7

On a 7-day run you cannot wait until the end to find a problem.

1. **Search terms report** (Keywords → Search terms). Anything irrelevant → add as a negative
   immediately. This is where a small budget leaks fastest.
2. **Confirm a real click produced a labelled lead** in the portal.
3. If CPC is running above ~$4.50, tighten to exact match only and drop ad group 3 first —
   it is the broadest intent of the three.

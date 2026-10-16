# Google Ads: Open Enrollment 2027 Plan (truckers + small business)

Built Oct 16, 2026. Replaces nothing: the older trucker/small-business docs stay as reference.
Import files in this folder (Google Ads Editor → Account → Import → From file):
- `ads-editor-keywords.csv`: 9 ad groups, phrase + exact match, final URLs and UTM suffixes
- `ads-editor-negatives.csv`: campaign-level negatives for both campaigns
- `ads-editor-responsive-search-ads.csv`: one RSA per ad group (all headlines ≤30, descriptions ≤90, checked)

## 0. Blockers, do these first
1. **Health insurance ad certification.** The trucker campaign showed "All ads limited by policy." US health insurance ads need
   G2RS + Google healthcare certification (~14 days). If it isn't approved yet, apply **today**: it is the long pole for OE.
   Certify Florida plus the states you actually target (pricing is per jurisdiction).
2. **Conversion goals.** Primary: `Quote Form Lead` + calls from ads ≥ 60 seconds. Make `Phone Call Click` secondary
   (clicks aren't calls). Remove duplicate call goals so leads are not double-counted.
3. **Turn on Enhanced Conversions for Leads** (Goals → Settings). The forms already collect email/phone; this recovers
   conversions lost to iPhone/cookie blocking and makes Smart Bidding much better on small volume.
4. **Offline conversions from your CRM (next step).** Business quote leads now store the `gclid` (fixed today). Once you
   have ~2 weeks of leads, import "Quoted" and "Sold" stages from GHL/the admin board back into Google Ads so it bids
   toward clients who buy, not just form fills.

## 1. Campaigns

| | Trucker Health - OE 2027 | Small Biz Renewal - 2027 |
|---|---|---|
| Landing page | /truckers/quote (Spanish: /truckers/cotizar) | /small-business-renewal-review (new) |
| Locations | Your 33 licensed states, "Presence" only | Florida (Miami-Dade, Broward, Palm Beach first), "Presence" only |
| Networks | Search only. Partners + Display off | Search only |
| Schedule | All hours (drivers search nights/weekends) | Mon–Sat 7am–8pm ET |
| Devices | Mobile-first | All; expect more desktop |
| Bidding | Max Conversions; tCPA ≈ 1.2× actual CPL after 30 conv. | Max Clicks, max CPC $6, → Max Conversions after 15 conv. |
| Languages | English + Spanish | English + Spanish |

## 2. Budget calendar (where the money should go)
Leads in insurance are seasonal; spend when intent peaks, not evenly.

| Dates | Trucker /day | Small biz /day | Why |
|---|---|---|---|
| Oct 16 – Oct 31 | $25 | $25 | Renewal letters landing; group renewals for Jan 1 are decided now |
| Nov 1 – Nov 30 | $40 | $35 | OE opens; groups' Nov 15–Dec 15 participation-waiver window |
| Dec 1 – Dec 15 | $60 | $35 | Jan 1 deadline rush. Add a **Seasonality adjustment** Dec 10–15, +30% conversion rate (Tools → Bid strategies → Advanced controls) |
| Dec 16 – Jan 15 | $35 | $20 | Last-chance Feb 1 coverage |
| After Jan 15 | $15 | $25 | Drivers: special enrollment only. Groups can start any month |

## 3. Ad groups
Trucker: Truck Driver Health Insurance · Owner Operator · 1099 Driver · **2027 Rate Increase – Drivers (new)** · Spanish
Small biz: **Renewal Increase** · Switch Carriers · Alternatives (level-funded/ICHRA) · Group Health FL

Start phrase + exact only. Promote converting search terms to exact weekly. Do not use broad match until 30+ conversions.

## 4. Assets (add in the UI; not in the CSVs)
- **Call asset** (954) 825-1009, scheduled to staffed hours only.
- **Sitelinks, trucker:** 2027 Rate Check → /truckers/quote · Subsidy Cliff Calculator → /owner-operator-subsidy-cliff-calculator ·
  Owner-Operator Plans → /best-health-insurance-owner-operators · Does It Cover DOT Physicals? → /does-health-insurance-cover-dot-physical
- **Sitelinks, small biz:** Free Renewal Review → /small-business-renewal-review · Cost Calculator → /small-business-health-insurance-calculator ·
  Level-Funded Plans → /level-funded-health-insurance-florida · ICHRA for Small Business → /ichra-florida-small-business
- **Callouts:** No Fee to You · Licensed Advisor · Same-Day Quotes · English y Español · Enroll by Dec 15 (trucker, remove Dec 16)
- **Promotion/price assets:** don't. Insurance pricing claims get disapproved.
- **Countdown:** in the trucker RSA, swap one headline Dec 1–15 for `{COUNTDOWN(2026-12-15 23:59:00,5)} Left to Enroll` (counts down automatically).

## 5. Weekly routine (30 minutes, every Monday + Thursday in November/December)
1. Search terms report → add negatives; promote winners to exact.
2. Check cost per lead by ad group; move budget to the winner.
3. Match Ads conversions against new leads on the admin board ("· Google Ads" now shows on business leads).
4. **Call every lead within 5 minutes.** Speed-to-lead beats every bid tweak. Partial trucker leads (phone captured, form not finished) too.
5. After Dec 15, pull the Dec 15 callout and countdown headline.

## 6. Targets to judge by (first 30 days)
- Trucker: CPL under ~$60 (your Sept number was $54). Click-through rate above 5% on exact match.
- Small biz: first goal is 5–10 renewal reviews; a group case is worth far more than an individual, so a $150+ CPL can still pay.

## Claims check
Everything in the ads is either verifiable or hedged: median 14% (KFF, Aug 2026), Florida small-group filings 8.4–15.5%
(proposed, ACASignups Sept 24 2026), OE Nov 1 – Jan 15 with Dec 15 for Jan 1 (HealthCare.gov states). "5.0-Star Google
Rating" and "Licensed in 33 States": confirm both are still true before launch. Nothing promises a price or a savings amount.

## 7. Live performance in the admin portal (Google Ads tab)
1. Vercel → Project → Settings → Environment Variables: add `ADS_SYNC_SECRET` (Production) and redeploy.
2. Google Ads → Tools → Bulk actions → Scripts → (+): paste `google-ads/vs-ads-sync-script.js`, set `SECRET` to the same value.
3. Authorize → Preview (log shows `Sync 200`) → Frequency: Hourly.
The admin "Google Ads" tab then updates itself every hour: spend, CTR, CPC, cost per conversion, cost per real portal lead,
quoted and sold counts, daily charts, campaign/ad group/keyword/search-term tables, wasted-spend negatives (one-click copy),
policy and Quality Score warnings, and best converting hours.

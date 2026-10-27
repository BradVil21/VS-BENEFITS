# 2026-10-27: premium-increase lead page + 4 new posts (rate increase, truckers)

## New pages
- /premium-increase-review: individual/family version of the small-business renewal review. Form (name, ZIP, who's covered,
  2026 premium, 2027 renewal, current coverage, phone, optional email, TCPA consent) -> /api/lead-sync
  (source premium-increase-review, tags premium-increase-review / website-lead / individual-family, pipeline individual;
  notes carry the old/new premium and % increase). Fires quote_start + generate_lead. Prefills ?zip= ?cur= ?new=.
- /blog/why-did-my-health-insurance-go-up-2027: 7 reasons + fixes. Targets "why did my health insurance go up" and the new
  Google Ads ad group "Premium Increase 2027".
- /blog/hsa-for-truck-drivers: 2027 HSA limits, bronze plans HSA-eligible since 2026, MAGI/subsidy effect.
- /blog/telehealth-for-truck-drivers: what virtual visits can/can't do, DOT exam in person, state licensing rule.
- /blog/truck-driver-health-insurance-pre-existing-conditions: ACA guaranteed issue, plans that can deny, 2027 OOP max.

## Wiring
- Premium increase calculator: result CTA now "Have an advisor review my increase" -> /premium-increase-review with cur/new prefilled.
- Homepage hero link row: + "Premium went up? Free review".
- blog.html: 4 new cards at the top. Trucker hub (/truck-driver-health-insurance-resources): 3 "New" cards.
- In-article links added to: renewal-notice-2027, how-to-lower-premiums-2027, aca-subsidies-ended-2026 (-> review + why post);
  owner-operator-increase-2027 (-> HSA, telehealth); out-of-state, prescriptions (-> telehealth);
  diabetes, sleep apnea, blood pressure (-> pre-existing, HSA).
- sitemap.xml (+5, lastmod 2026-10-27), llms.txt (+5).

## Facts used (checked Oct 27 2026)
- FL 2027 individual market: ~10.4% weighted average approved (ACASignups, Oct 19 2026); preliminary ~15-16%.
- National: median proposed 15%, medical trend ~10%, ~4 pts from enhanced-credit expiration (Peterson-KFF, Aug 3 2026).
- FL exits: Cigna leaving; Sunshine State Health Plan Marketplace products end, members mapped to Ambetter (healthinsurance.org, ACASignups).
- 2027 OOP max $12,000 / $24,000 (2026: $10,600 / $21,200). 2027 HSA $4,500 / $9,000, +$1,000 at 55; HDHP min ded $1,750/$3,500.
- 400% FPL single $63,840 (2026 HHS guidelines, 2027 coverage).

## Next (needs you)
- After deploy: Search Console -> request indexing for /premium-increase-review and the 4 posts.
- Google Ads: the "Premium Increase 2027" ad points to the calculator, which now hands off to the review form. Once leads come
  through, consider pointing the ad straight at /premium-increase-review and compare.

# 2026-11-04: Search Console quick wins (export Aug 3 - Nov 2)

## Titles + descriptions (also og/twitter)
| Page | Why | New title |
|---|---|---|
| /blog/aca-open-enrollment-2027-guide | 9,466 impr, pos 13.6, 0.26% CTR; "when is open enrollment for health insurance 2027" pos 10.5 | When Is Open Enrollment for 2027? Nov 1–Jan 15 Dates |
| /aca-subsidy-calculator | "obamacare/health insurance subsidy calculator" pos 51-60 | 2027 ACA & Obamacare Subsidy Calculator: Price in 60 Seconds |
| /does-health-insurance-cover-dot-physical | pos 4.7, 2,293 impr, 0.7% CTR | Does Health Insurance Cover a DOT Physical? (2027 Costs) |
| /coral-gables-small-business-health-insurance | "group health insurance coral gables" pos 6.3, 0 clicks | Group Health Insurance Coral Gables, FL: Employee Benefits |
| /health-insurance-uber-drivers | "does uber offer health insurance for drivers in [city]" pos ~4, 0 clicks | Does Uber Offer Health Insurance? What Drivers Use in 2027 |

Uber page: main H2 is now the question; added California Prop 22 stipend note (body, FAQ, FAQ schema).

## Internal links
- Homepage OE countdown: links to OE guide, calculator, income limits (homepage had none).
- Homepage Popular Guides: duplicate trucker card -> OE guide; added calculator card; cost card relabeled 2027.
- /open-enrollment hero: link to the OE guide (both pages competed for the same queries; guide is the one that ranks).

## Fixes
- Homepage countdown: missing brace applied the "closed" style every tick, and Dec 16-Jan 15 would have said
  "Open Enrollment is closed". Now: count to Dec 15 (Jan 1 coverage), then to Jan 15, then closed. Static text updated.
- vercel.json: 301 /vshealthbenefits.com/:path* -> /:path* (Google indexed /vshealthbenefits.com/hmo-vs-ppo).

## Next (needs you)
- Search Console -> URL Inspection -> Request indexing: /, /blog/aca-open-enrollment-2027-guide, /aca-subsidy-calculator,
  /health-insurance-uber-drivers, /does-health-insurance-cover-dot-physical, /coral-gables-small-business-health-insurance.
- Re-check CTR on these in ~2 weeks.

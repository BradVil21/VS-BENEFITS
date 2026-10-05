# Changelog: 4 October 2026 (Open Enrollment 2027 savings cluster)

Goal: catch the people searching right now because their renewal letter arrived, their premium went up,
or their coverage is ending, and turn them into quotes before the Dec 15 / Jan 15 deadlines.
Builders: .seo-work/build_oe_savings_oct04.py (posts), build_oe_tools_oct04.py (tools),
wire_oe_savings_oct04.py (links, blog cards, sitemap, llms.txt). All idempotent; re-run to rebuild.

## New pages (7)
| URL | Target searches | Notes |
|---|---|---|
| /blog/how-to-lower-health-insurance-premiums-2027 | how to lower health insurance premium, cheaper health insurance 2027, health insurance going up 2027 | Pillar: 11 moves + "which moves fit you" table |
| /blog/health-insurance-renewal-notice-2027 | health insurance renewal letter, marketplace auto renewal 2027, why did my premium go up | Benchmark-shift explainer, auto re-enrollment, 6 checks, date table, group renewals |
| /blog/losing-health-insurance-2027 | cigna leaving marketplace 2027, losing health insurance 2027, medicaid work requirements 2027 | 5 situations table, Cigna/insurer exits, cliff, Medicaid, immigrant rules, 150% SEP ending |
| /blog/cheapest-health-insurance-2027 | cheapest health insurance 2027, catastrophic plan 2027, bronze HSA | Subsidized bronze, CSR silver, bronze + HSA, catastrophic hardship exemption, non-ACA warnings |
| /blog/owner-operator-health-insurance-increase-2027 | owner operator health insurance 2027, truck driver health insurance cost 2027 | 8 fixes + worked $70k example (MAGI 65,055 vs 63,840 line) |
| /health-insurance-premium-increase-calculator | health insurance premium increase calculator, renewal calculator | Renewal vs benchmark at income; cliff value; Medicaid-gap note |
| /owner-operator-subsidy-cliff-calculator | owner operator subsidy cliff, truck driver aca subsidy calculator | Net profit -> SE tax -> MAGI -> 400% line; Solo 401(k)/SEP/HSA room |

All posts: Article + Breadcrumb + FAQPage schema, sidebar CTA and inline CTAs to /quote?type=individual.
Tools: WebApplication + FAQPage + Breadcrumb schema; same math as the other calculators (FPL 15,960 + 5,680,
Rev. Proc. 2026-26 scale, BASE21 375). Mobile call bar skips them automatically (slug contains "calculator").

## Facts used (verified 4 Oct 2026)
- KFF: 2027 proposed median +15% (276 insurers, -1% to +54%); 2026 benchmark +26%.
- Florida 2027 filings: 12 insurers, +3.87% to +39.14%, OIR not final (WLRN 11 Sep 2026).
- Enhanced credits expired 31 Dec 2025; House passed extension 8 Jan 2026; Senate has not acted.
- OE 1 Nov 2026 - 15 Jan 2027; Dec 15 for Jan 1 (City of Columbus v. Kennedy). HHS appeal pending in the 4th Circuit;
  watch for a ruling near 30 Oct that could change the dates.
- 2027 HSA $4,500 / $9,000 (+$1,000 at 55); bronze and catastrophic HSA-compatible since 2026 (OBBBA / Notice 2026-5).
- Catastrophic hardship exemption for people ineligible for APTC or CSR due to income (<100% or >250% FPL), permanent
  in the 2027 NBPP; multi-year catastrophic plans allowed from 2027. 2027 OOP max $12,000 / $24,000.
- Cigna leaving the Marketplace in all 11 states incl. Florida (KFF tracker, 15 Sep 2026); CareSource, Baylor Scott & White,
  PacificSource, ConnectiCare also exiting states. Molina/Sunshine FL exit NOT confirmed, so not mentioned.
- Medicaid work requirements 1 Jan 2027 (expansion adults 19-64, 80 hrs/mo); 6-month renewals.
- Immigrant PTC narrowing 1 Jan 2027; 150% FPL monthly SEP ends after 2026; full APTC repayment from tax year 2026;
  pre-enrollment verification is 2028, not 2027.
- 2026 Solo 401(k) $24,500 (+$8,000 50+, +$11,250 60-63), $72,000 total. 2027 limits due Nov: update the calculator then.

## Wiring
- "Paying more for 2027? Start here" block on 22 OE/subsidy/cost pages (incl. /open-enrollment, OE guide, subsidy calculator).
- "Drivers: keep your subsidy in 2027" block on 9 owner-operator / driver OE pages.
- Two new cards (cliff calculator + owner-operator post) in the trucking tools block on 48 trucking pages.
- blog.html: 7 cards at the top. sitemap.xml: 7 URLs + lastmod on touched pages. llms.txt: 7 entries.

## Still needed (only you can do these)
1. Deploy (commit + push), then Search Console: resubmit sitemap.xml and Request indexing on all 7 URLs. Do the
   renewal-notice and lowering-premium posts first; renewal letters are landing now.
2. Post the premium increase calculator and the cliff calculator on Facebook / LinkedIn / TikTok and in trucker groups.
   Tools earn links and shares far faster than articles.
3. GHL: send the renewal-notice post to existing individual clients this week ("send us your renewal letter").
4. Early Nov: plug the IRS 2027 retirement limits into owner-operator-subsidy-cliff-calculator and the OO post;
   after the 4th Circuit ruling, re-check the Jan 15 end date sitewide.

# SEO Changelog: 30 September 2026

Source: Search Console export, 3 months to 27 Sep 2026 (394 clicks, 76,761 impressions, 0.51% CTR).
Weekly clicks 16 -> 50, average position ~55 -> ~23. Most of the export predates the 21 and 24 Sep
changes (OE guide title, merges, typo redirects), so those need 2-4 weeks before judging.

Site audit: sitemap clean (185 URLs, none redirect or 404), no duplicate titles, canonicals OK.

## 1. Titles matched to the queries Google already shows us for
| Page | Change | Why |
|---|---|---|
| /blog/how-much-does-health-insurance-cost-2026 | Title "Average Cost of Health Insurance: $625/Month (2026 Prices)", description, H1 and schema headline aligned; dateModified 2026-09-30 | "average cost of health insurance" = 2,652 impressions, biggest query on the site |
| /aca-subsidy-calculator | Description now says "ACA health insurance subsidy calculator"; H1 adds 2027 | "health care subsidy calculator" (158 impr, #70), "aca subsidy calculator" (#52) |
| /coral-springs-health-insurance | "Health Insurance Coral Springs, FL - Local Broker, Free Quotes" + new description | ranks #2-3 for "health insurance coral springs fl" / "dental insurance coral springs" with 0 clicks |
| /coral-gables-small-business-health-insurance | "Group Health & Employee Benefits, Coral Gables FL" | "group health insurance / employee benefits coral gables" at #7-8, 0 clicks |
| /services, /blog/can-owner-operators-deduct-health-insurance | Titles trimmed under 60 characters | were being cut off in results |

og/twitter titles and descriptions matched on every page above.

## 2. Internal links that still hit redirects (now point straight at the final URL)
- blog/husband-and-wife-business-health-insurance: 2 links
- blog/team-truck-drivers-health-insurance: 1 link
- blog/local-regional-otr-truck-driver-health-insurance: 1 link

## 3. sitemap.xml
lastmod set to 2026-09-30 for the 9 edited pages.

## Left alone on purpose
- OE guide title/description: changed 21 Sep, too soon to judge. Changing it again resets the test.
- /ppo-health-insurance and /dental-vision-insurance national terms (#65-70): carrier-dominated.

## Still needed (only you can do these)
1. Search Console: resubmit sitemap.xml; Request indexing on /blog/how-much-does-health-insurance-cost-2026,
   /aca-subsidy-calculator, /coral-springs-health-insurance, /blog/aca-open-enrollment-2027-guide.
2. Google Business Profile: category "Insurance broker", service area Broward + Miami-Dade, link to
   /coral-springs-health-insurance, and ask recent clients for reviews. Local queries already rank #1-3.
3. Backlinks for the trucking pages (see 24 Sep changelog). This is the main thing holding
   "health insurance for truck drivers" (1,426 impr) at #50.

---

# Part 2 (same day): new pages + calculator data update

## New pages
| URL | Target | Notes |
|---|---|---|
| /blog/aca-income-limits-2027 | "aca subsidies 2027 income limits" (#9, 3.7% CTR), "aca income limits 2027", "400% poverty level 2027" | Chart for households 1-8 (100/138/150/200/250/400% FPL), 2027 contribution table, instant "where does my income land" checker, Florida non-expansion section, 2027 changes, FAQ + FAQPage schema. Calculator CTA top, middle and in the checker result. |
| /blog/inscripcion-abierta-2027 | Spanish OE searches (558 impr), Miami | Dates, key-date cards, call + quote buttons above the fold, Spanish income table (1-6), 2027 changes (400% cliff, immigrant eligibility, full repayment), Florida section, documents checklist, FAQ + schema. hreflang pair with the English guide. |

Numbers: 2026 HHS poverty guidelines ($15,960 + $5,680/person), used for 2027 coverage. IRS Rev. Proc. 2026-26
(2.15% / 3.23-4.30 / 4.30-6.78 / 6.78-8.66 / 8.66-10.22 / 10.22%). OE Nov 1 2026 - Jan 15 2027 (court vacated the
Dec 15 end date in June 2026; CMS confirmed in August). Immigrant PTC eligibility narrows 1 Jan 2027 (LPRs, Cuban/Haitian
entrants, COFA stay eligible). All verified 30 Sep 2026.

## Calculators fixed (were using 2025 poverty guidelines and 2026 percentages)
- aca-subsidy-calculator, cobra-vs-marketplace-calculator, truck-driver-health-insurance-cost-calculator:
  FPL_BASE 15650 -> 15960, FPL_ADD 5500 -> 5680, applicablePct() -> 2027 table.
- Disclaimer text updated on those + special-enrollment-period-checker and ichra-vs-group-health-calculator.
- Truck calculator copy: 400% line $62,600 -> $63,840 (single), $128,600 -> $132,000 (family of 4).

## Linking
- English OE guide: hreflang en/es/x-default + "Leer esta guía en español" link above the H1.
- what-income-counts-for-aca-subsidies -> income limits chart; seguro-de-salud-miami -> Spanish guide.
- blog.html: two new post cards. sitemap.xml: 2 new URLs + lastmod on edited pages. llms.txt: both added.

## To do after deploy
Search Console > URL Inspection > Request indexing for both new URLs.

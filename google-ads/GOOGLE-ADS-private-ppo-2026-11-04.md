# Private PPO campaign: full-price payers (Nov 4 2026)

All ads and sitelinks send people to https://www.vshealthbenefits.com/private-health-insurance (no video ads).

Who: self-employed people, owner-operators and families who make too much for a subsidy.
Landing page: /private-health-insurance (live after the push).
Script: `google-ads/vs-private-ppo-build-2026-11-04.js`

## What it builds

| Campaign | $/day | Status | Where |
|---|---|---|---|
| Private PPO - High-Income ZIPs | 20 | ON | 170 highest-income ZIP codes in FL, TX, GA, IL, OH, MD, MO, KY |
| Private PPO - 8 States (Rest) | 10 | PAUSED | The same 8 states minus those ZIPs. Turn it on once the ZIP campaign brings in leads |

Both campaigns: Google Search only, "people located in", English, phrase + exact match, Maximize clicks with a $15 max CPC.
Total ad spend goes from $50/day to $70/day while the ZIP campaign runs.
Every ad's final URL: https://www.vshealthbenefits.com/private-health-insurance

**Ad groups (44 keywords):**
- Private Health Insurance
- PPO Health Insurance
- High Income
- Lower My Premium ("health insurance too expensive", "alternative to expensive health insurance"...)
- Self-Employed & 1099 - Price

I left out the exact keywords your Self-Employed campaign already uses (for example "private health insurance self employed"), so the two campaigns don't bid against each other.

**Ad copy:** built around how people feel about the price.
- Headlines include "Paying Too Much for Coverage?", "Nationwide PPO Options", "Compare Plans in 10 Minutes", "Earn Too Much for a Subsidy?", "Priced on Health, Not Income" and "Pick Your Own Doctors".
- Descriptions say health questions apply, so the ads don't promise anything.

**Negatives:**
- The shared list "VS Leads - Negatives (Nov 3)" (aca, obamacare, marketplace, subsidy, medicaid, medicare, low income, free health insurance...).
- Extra negatives on this campaign only: cheap, cheapest, free, low cost, income limit, eligibility, qualify, employer, small business, short term, student, "what is", "vs hmo".

**Income targeting:**
- Household income: the bottom 70% is excluded, so only the top 30% (top 10%, 11-20% and 21-30%) and "unknown" see the ads. Keeping "unknown" matters: a big share of searchers fall into it, and excluding them would starve the campaign.
- ZIP codes: the highest median household income ZIPs in each state, limited to ZIPs with 8,000+ people (FL 30, TX 30, GA/IL/OH/MD 20, MO/KY 15). The full list is in `private-ppo-zips-2026-11-04.txt`. The figures come from Census ACS data via the uszipcode dataset, which is a few years old, so treat it as a ranking, not current incomes.

**Extras:**
- Sitelinks, all on the landing page: Why Private PPO Plans, Your Plan vs. Private, How It Works, Common Questions.
- Callouts.
- Your existing call asset (staffed hours) and English lead form are reused from "Self-Employed 1099 - 8 States".

## Do this (about 10 minutes)

1. Push the website first, so the landing page is live.
2. In Google Ads, go to Tools > Bulk actions > Scripts and click **+ New script**. Name it **VS Private PPO - Build**.
3. Paste in all of `vs-private-ppo-build-2026-11-04.js`, click Authorize, then click **Preview**.
4. The log should say "ZIP targets found: 1xx of 170" and end with `DONE. No errors.` Then click **Run**.
   - Re-running is safe; it skips anything that already exists.
   - On Run it also adds the income exclusions and links the lead form.
5. Hourly script: in "VS Lead Engine - Hourly", change the CAMPAIGNS line to the line below, then save. This also switches the new campaigns to Maximize conversions once 15 leads come in.
   ```
   var CAMPAIGNS = ["Trucker - FL & GA", "Trucker - TX, IL & OH", "Trucker - KY, MO & MD",
                    "Self-Employed 1099 - 8 States", "Spanish - Camioneros e Independientes",
                    "Private PPO - High-Income ZIPs", "Private PPO - 8 States (Rest)"];
   ```

## Check on Nov 11

- Search terms report: add any $0-plan or low-income searches as negatives.
- Cost per lead in the ZIP campaign compared with the Self-Employed campaign.
- If the ZIP campaign has 3+ leads and is spending its full budget, turn on "Private PPO - 8 States (Rest)".
- If the income exclusions were refused, the log will say so. In that case, set them by hand under Audiences > Demographics > Household income.

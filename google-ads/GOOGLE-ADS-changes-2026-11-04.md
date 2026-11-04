# Google Ads changes, 2026-11-04 (applied by Claude in the account)

## Running now ($70/day)
| Campaign | $/day | Lands on |
|---|---|---|
| Trucker Health - OE 2027 | 50 | trucker pages (unchanged) |
| Private PPO - High-Income ZIPs | 20 | /private-health-insurance |

## Paused
- Self-Employed FL - 2027: paused today at Bradley's request (82 impressions, 0 leads in 7 days). Paused, not removed.
- Private PPO - 8 States (Rest): built, paused. Turn on once the ZIP campaign has 3+ leads and spends its full budget.
- Small Biz Renewal - 2027, Individual - OE 2027 FL: already paused.

## Private PPO - High-Income ZIPs (built by script "VS Private PPO - Build (Nov 4)")
- 170 highest-income ZIPs in FL, TX, GA, IL, OH, MD, MO, KY ("people located in")
- Household income: lower 70% excluded (top 10/11-20/21-30% + unknown)
- 5 ad groups, 39 keywords x phrase + exact, 5 responsive search ads, sitelinks to page sections, callouts, call asset
- Shared negative list "VS Leads - Negatives (Nov 3)" created (35 words: marketplace, obamacare, subsidy, medicaid...)
  + 30 campaign negatives (cheap, free, how to, income limit...)
- Maximize clicks, $15 max CPC. Switch to Maximize conversions after ~10-15 leads.
- Script note: Google rejects targeting/keywords in the same batch as a brand-new campaign, so the script builds in steps
  and can resume a half-built campaign. First run built everything; the last step (lead form lookup) failed, so the
  campaign was switched on by hand.

## Portal + quote form
- quote form: ?niche=private now tags leads "private-ppo" + "lp-private-ppo" with a note
  "Private PPO lead: full-price / no-subsidy buyer" (before: no tag at all).
- admin Analytics: /private-health-insurance shows as "Private PPO (Full Price)".
- Marketing tab updates itself from the hourly "VS Ads Sync" script; utm_campaign for the new campaign = private-ppo-zips.

## Check
- "VS Auto Bidding (daily)" runs 4-5 AM daily; its source isn't in this folder. Check it doesn't change the new campaign.
- Nov 7-8: search terms report for the ZIP campaign; add off-target terms as negatives.

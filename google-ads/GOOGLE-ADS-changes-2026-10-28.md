# Google Ads changes, 2026-10-28 (account 294-975-7547)

Before (Sep 28 - Oct 27): $619 spend, 183 clicks, 5 conversions. Last 7 days: $294, 78 clicks, 0 tracked conversions.
CRM (GHL), Oct 21-28: 9 website leads = 7 organic search, 1 Google Ads (trucker, Oct 28), 1 abandoned draft.

Run as script "VS Qualified Leads (Oct 28)" (Tools > Bulk actions > Scripts). Source: vs-qualified-leads-2026-10-28.js.
Read-only report used to decide: vs-report-2026-10-28.js.

1. Trucker Health - OE 2027: Max clicks CPC cap $6 -> $15. Keywords were already broad and eligible; the $6 cap lost
   almost every auction (12 impressions in 7 days). Budget unchanged at $15/day.
2. Individual - OE 2027 FL: Maximize clicks -> Maximize conversions (bids for leads). Budget unchanged at $30/day.
3. Negative keywords (phrase): Individual +17 (Medicare/Part B, Medicaid plan names, carrier logins, Spanish),
   Small Biz +52 (FEHB/OPM/PSHB, state/federal employee plans, big-employer plans, TPAs, MEC/MEWA, Medicare),
   Trucker +3.
4. Conversion goals: "Phone Call Click" (phone-link tap) and duplicate "Calls from ads" set to SECONDARY.
   Primary now: Quote Form Lead, Calls from ads (1), Dental Vision Quote Lead (campaign removed).

NOT changed: Florida-only locations (G2RS health insurance ad certification is Florida only; expanding states would
get ads disapproved), budgets, ads.

Check again ~Nov 4: trucker impressions/CPC, individual cost per lead, and GHL leads tagged src google.
If Individual spends <50% of budget for 5+ days on Max conversions, switch back to Max clicks with a $6 cap.

## Evening update (7:51 PM, script "VS Qualified Leads (Oct 28)", source vs-nospanish-adstrength.js)
Marketing tab sync checked: "VS Ads Sync (Marketing tab)" runs hourly; last logged run "Sync 200 ok", 39 daily rows,
3 campaigns, 120 search terms.

1. No Spanish ads (owner request): paused ad group "Trucker Health - OE 2027 > Spanish". Scan found no other Spanish
   ad groups, ads or keywords in any campaign. Paused, not removed.
2. Ad strength AVERAGE -> new ads (old ad paused after the new one saved):
   - Small Biz > Group Health 2-50 Employees (no pinned headline; group health / small group / employee wording)
   - Trucker > 1099 Driver (1099 / independent / self-employed wording)
   - Small Biz > Businesses With 1099 Workers: now lands on /1099-health-insurance (keyword QS was 2)
   - Individual > Premium Increase 2027: now lands on /premium-increase-review (keyword QS was 2)
   New ads show "Pending" strength for a day or so while Google rates them.

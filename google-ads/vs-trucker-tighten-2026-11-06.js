/* VS Trucker Tighten (Nov 6 2026).  PREVIEW first, then RUN.  Safe to re-run.
   1. Display Network OFF on Trucker Health - OE 2027 (Google Search + search partners stay on).
   2. Exact [health insurance for truck drivers] back on in "Truck Driver Health Insurance"; exact versions of the core
      trucker searches added if missing.
   3. Pauses PHRASE keywords that spent $25+ in the last 30 days with 0 conversions (paused, not removed).
   4. Budget stays $50/day. Logs every keyword's 30-day numbers. */
var CAMP = "Trucker Health - OE 2027", BUDGET = 50, MAX_WASTE = 25;
var EXACTS = { "Truck Driver Health Insurance": ["health insurance for truck drivers", "truck driver health insurance", "health insurance for truckers", "trucker health insurance"],
               "Owner Operator": ["owner operator health insurance", "health insurance for owner operators", "owner operator medical insurance"],
               "1099 Driver": ["health insurance for independent truckers", "independent truck driver health insurance"] };
function q(s) { var o = [], it = AdsApp.search(s); while (it.hasNext()) o.push(it.next()); return o; }
function L(m) { Logger.log(m); }
function mut(op, label) { var r = AdsApp.mutate(op); L((r.isSuccessful() ? "OK: " : "FAILED: ") + label + (r.isSuccessful() ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); return r.isSuccessful(); }
function main() {
  L(AdsApp.getExecutionInfo().isPreview() ? "PREVIEW (nothing is saved)" : "RUN");
  var c = q("SELECT campaign.resource_name, campaign.status, campaign.network_settings.target_content_network, campaign.network_settings.target_search_network, campaign.bidding_strategy_type, campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared FROM campaign WHERE campaign.name = '" + CAMP + "'");
  if (!c.length) { L("MISSING " + CAMP); return; }
  var cr = c[0], crn = cr.campaign.resourceName, C = "campaign.resource_name = '" + crn + "'";
  L("Campaign " + cr.campaign.status + " | $" + cr.campaignBudget.amountMicros / 1e6 + "/day | " + cr.campaign.biddingStrategyType + " | display=" + cr.campaign.networkSettings.targetContentNetwork + " partners=" + cr.campaign.networkSettings.targetSearchNetwork);
  // spend by network, 30 days
  q("SELECT segments.ad_network_type, metrics.cost_micros, metrics.clicks, metrics.conversions FROM campaign WHERE " + C + " AND segments.date DURING LAST_30_DAYS").forEach(function (r) {
    L("  network " + r.segments.adNetworkType + ": $" + (r.metrics.costMicros / 1e6).toFixed(2) + ", " + r.metrics.clicks + " clicks, " + r.metrics.conversions + " conv"); });
  // 1. display off
  if (cr.campaign.networkSettings.targetContentNetwork) mut({ campaignOperation: { update: { resourceName: crn, networkSettings: { targetContentNetwork: false } }, updateMask: "network_settings.target_content_network" } }, "Display Network turned OFF");
  else L("Display Network already off");
  // 4. budget
  if (!cr.campaignBudget.explicitlyShared && cr.campaignBudget.amountMicros !== BUDGET * 1e6) mut({ campaignBudgetOperation: { update: { resourceName: cr.campaignBudget.resourceName, amountMicros: BUDGET * 1e6 }, updateMask: "amount_micros" } }, "budget -> $" + BUDGET);
  // keywords: 30-day numbers
  var stats = {};
  q("SELECT ad_group_criterion.resource_name, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.impressions FROM keyword_view WHERE " + C + " AND segments.date DURING LAST_30_DAYS").forEach(function (r) { stats[r.adGroupCriterion.resourceName] = r.metrics; });
  var kws = q("SELECT ad_group.resource_name, ad_group.name, ad_group.status, ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status FROM ad_group_criterion WHERE " + C + " AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED' AND ad_group.status != 'REMOVED'");
  var have = {}, groups = {};
  kws.sort(function (a, b) { var x = stats[a.adGroupCriterion.resourceName] || {}, y = stats[b.adGroupCriterion.resourceName] || {}; return (y.costMicros || 0) - (x.costMicros || 0); });
  kws.forEach(function (r) { var k = r.adGroupCriterion, m = stats[k.resourceName] || {}, cost = (m.costMicros || 0) / 1e6, conv = +m.conversions || 0;
    groups[r.adGroup.name] = r.adGroup.resourceName;
    have[r.adGroup.name + "|" + k.keyword.text.toLowerCase() + "|" + k.keyword.matchType] = k;
    if (cost > 0 || conv > 0) L("KW " + r.adGroup.name + " | [" + k.keyword.matchType + "] " + k.keyword.text + " | " + k.status + " | $" + cost.toFixed(2) + " | " + (m.clicks || 0) + " clk | " + conv + " conv");
    // 3. pause expensive non-converting phrase keywords
    if (k.keyword.matchType === "PHRASE" && k.status === "ENABLED" && cost >= MAX_WASTE && conv === 0)
      mut({ adGroupCriterionOperation: { update: { resourceName: k.resourceName, status: "PAUSED" }, updateMask: "status" } }, "paused phrase '" + k.keyword.text + "' ($" + cost.toFixed(2) + ", 0 conv)");
  });
  // 2. exact keywords
  Object.keys(EXACTS).forEach(function (g) {
    if (!groups[g]) { L("ad group not found: " + g); return; }
    EXACTS[g].forEach(function (t) { var e = have[g + "|" + t + "|EXACT"];
      if (e && e.status === "ENABLED") { L("exact on: [" + t + "]"); return; }
      if (e) mut({ adGroupCriterionOperation: { update: { resourceName: e.resourceName, status: "ENABLED" }, updateMask: "status" } }, "re-enabled exact [" + t + "] in " + g);
      else mut({ adGroupCriterionOperation: { create: { adGroup: groups[g], status: "ENABLED", keyword: { text: t, matchType: "EXACT" } } } }, "added exact [" + t + "] in " + g);
    }); });
  L("DONE");
}

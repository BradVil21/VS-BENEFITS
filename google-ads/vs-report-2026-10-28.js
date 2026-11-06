/* VS read-only report (Oct 28 2026). Changes NOTHING. Run with PREVIEW and read the log. */
function q(s) { return AdsApp.search(s); }
function main() {
  var live = "campaign.status = 'ENABLED'";
  Logger.log("== CAMPAIGNS");
  var it = q("SELECT campaign.name, campaign.bidding_strategy_type, campaign.geo_target_type_setting.positive_geo_target_type, campaign.network_settings.target_search_network, campaign.network_settings.target_content_network, metrics.clicks, metrics.cost_micros, metrics.conversions FROM campaign WHERE " + live + " AND segments.date DURING LAST_30_DAYS");
  while (it.hasNext()) { var r = it.next(), c = r.campaign;
    Logger.log(c.name + " | " + c.biddingStrategyType + " | geo " + c.geoTargetTypeSetting.positiveGeoTargetType + " | partners " + c.networkSettings.targetSearchNetwork + " | display " + c.networkSettings.targetContentNetwork + " | clicks " + r.metrics.clicks + " | $" + (r.metrics.costMicros / 1e6).toFixed(2) + " | conv " + r.metrics.conversions); }

  Logger.log("== LOCATIONS");
  it = q("SELECT campaign.name, campaign_criterion.location.geo_target_constant, campaign_criterion.negative FROM campaign_criterion WHERE " + live + " AND campaign_criterion.type = 'LOCATION'");
  while (it.hasNext()) { var r = it.next(); Logger.log(r.campaign.name + " | " + r.campaignCriterion.location.geoTargetConstant + (r.campaignCriterion.negative ? " (excluded)" : "")); }

  Logger.log("== CONVERSION ACTIONS");
  it = q("SELECT conversion_action.name, conversion_action.status, conversion_action.primary_for_goal, conversion_action.category, conversion_action.type, metrics.all_conversions FROM conversion_action WHERE conversion_action.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS");
  while (it.hasNext()) { var a = it.next(); Logger.log(a.conversionAction.name + " | primary " + a.conversionAction.primaryForGoal + " | " + a.conversionAction.category + " | " + a.conversionAction.type + " | all conv " + a.metrics.allConversions); }

  Logger.log("== SEARCH TERMS, last 30 days, live campaigns (cost desc)");
  it = q("SELECT campaign.name, search_term_view.search_term, metrics.clicks, metrics.impressions, metrics.cost_micros, metrics.conversions FROM search_term_view WHERE " + live + " AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC LIMIT 150");
  while (it.hasNext()) { var r = it.next();
    Logger.log(r.campaign.name.slice(0, 14) + " | " + r.searchTermView.searchTerm + " | " + r.metrics.clicks + "c " + r.metrics.impressions + "i $" + (r.metrics.costMicros / 1e6).toFixed(2) + " conv " + r.metrics.conversions); }

  Logger.log("== TRUCKER KEYWORDS");
  it = q("SELECT ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, ad_group_criterion.system_serving_status, ad_group.status FROM keyword_view WHERE campaign.name = 'Trucker Health - OE 2027' AND ad_group_criterion.status != 'REMOVED'");
  while (it.hasNext()) { var r = it.next(), k = r.adGroupCriterion;
    Logger.log(r.adGroup.name + " [" + r.adGroup.status + "] | " + k.keyword.text + " | " + k.keyword.matchType + " | " + k.status + " | " + k.systemServingStatus); }
  Logger.log("DONE");
}

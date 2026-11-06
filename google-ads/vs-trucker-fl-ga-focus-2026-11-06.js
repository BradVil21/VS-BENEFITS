/* VS Trucker FL + GA Focus (Nov 6 2026).  PREVIEW first, then RUN.  Safe to re-run.
   Budget stays $50/day. Florida and Georgia get a +30% location bid adjustment.
   The other 6 states (IL KY MD MO OH TX) are taken out of targeting ("paused"); add them back by re-adding the locations.
   Note: Maximize conversions / tCPA ignores location bid adjustments, so taking the other states out is what actually
   moves the $50 to FL + GA. The +30% kicks in if the campaign is ever on Maximize clicks or manual CPC. */
var CAMP = "Trucker Health - OE 2027", BUDGET = 50, BOOST = 1.30;
var FOCUS = ["Florida", "Georgia"], PAUSE = ["Illinois", "Kentucky", "Maryland", "Missouri", "Ohio", "Texas"];
function q(s) { var o = [], it = AdsApp.search(s); while (it.hasNext()) o.push(it.next()); return o; }
function L(m) { Logger.log(m); }
function mut(op, label) { var r = AdsApp.mutate(op); L((r.isSuccessful() ? "OK: " : "FAILED: ") + label + (r.isSuccessful() ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); return r.isSuccessful(); }
function main() {
  L(AdsApp.getExecutionInfo().isPreview() ? "PREVIEW (nothing is saved)" : "RUN");
  var ids = {};
  q("SELECT geo_target_constant.id, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.country_code = 'US' AND geo_target_constant.target_type = 'State' AND geo_target_constant.status = 'ENABLED'").forEach(function (r) { ids[String(r.geoTargetConstant.id)] = r.geoTargetConstant.name; });
  var c = q("SELECT campaign.resource_name, campaign.bidding_strategy_type, campaign.network_settings.target_content_network, campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared FROM campaign WHERE campaign.name = '" + CAMP + "'");
  if (!c.length) { L("MISSING " + CAMP); return; }
  var cr = c[0], crn = cr.campaign.resourceName, C = "campaign.resource_name = '" + crn + "'";
  L("Bidding: " + cr.campaign.biddingStrategyType + " | Display: " + cr.campaign.networkSettings.targetContentNetwork + " | budget $" + (+cr.campaignBudget.amountMicros / 1e6));
  if (!cr.campaignBudget.explicitlyShared && +cr.campaignBudget.amountMicros !== BUDGET * 1e6) mut({ campaignBudgetOperation: { update: { resourceName: cr.campaignBudget.resourceName, amountMicros: BUDGET * 1e6 }, updateMask: "amount_micros" } }, "budget -> $" + BUDGET);
  var exact = q("SELECT campaign.resource_name, ad_group_criterion.status FROM ad_group_criterion WHERE " + C + " AND ad_group_criterion.keyword.text = 'health insurance for truck drivers' AND ad_group_criterion.keyword.match_type = 'EXACT'");
  L("Exact [health insurance for truck drivers]: " + (exact.length ? exact[0].adGroupCriterion.status : "MISSING"));
  var found = {};
  q("SELECT campaign_criterion.resource_name, campaign_criterion.location.geo_target_constant, campaign_criterion.bid_modifier, campaign_criterion.negative FROM campaign_criterion WHERE " + C + " AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.status != 'REMOVED'").forEach(function (r) {
    var cc = r.campaignCriterion, nm = ids[cc.location.geoTargetConstant.split("/").pop()] || cc.location.geoTargetConstant;
    if (cc.negative) { L("excluded: " + nm); return; }
    found[nm] = 1;
    var bm = cc.bidModifier ? Math.round((cc.bidModifier - 1) * 100) : 0;
    if (FOCUS.indexOf(nm) >= 0) {
      if (Math.abs((cc.bidModifier || 1) - BOOST) < 0.001) L(nm + " already +" + Math.round((BOOST - 1) * 100) + "%");
      else mut({ campaignCriterionOperation: { update: { resourceName: cc.resourceName, bidModifier: BOOST }, updateMask: "bid_modifier" } }, nm + " bid " + bm + "% -> +" + Math.round((BOOST - 1) * 100) + "%");
    } else if (PAUSE.indexOf(nm) >= 0) {
      mut({ campaignCriterionOperation: { remove: cc.resourceName } }, nm + " paused (removed from targeting)");
    } else L("other location left alone: " + nm);
  });
  FOCUS.forEach(function (nm) { if (found[nm]) return;
    var id = Object.keys(ids).filter(function (k) { return ids[k] === nm; })[0];
    mut({ campaignCriterionOperation: { create: { campaign: crn, location: { geoTargetConstant: "geoTargetConstants/" + id }, bidModifier: BOOST } } }, "added " + nm + " at +" + Math.round((BOOST - 1) * 100) + "%"); });
  L("DONE");
}

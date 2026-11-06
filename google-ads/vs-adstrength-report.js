/* VS ad strength report (read-only, Oct 28 2026). PREVIEW only. */
function main() {
  var it = AdsApp.search("SELECT campaign.name, ad_group.name, ad_group.status, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad_strength, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions, ad_group_ad.ad.responsive_search_ad.path1, ad_group_ad.ad.responsive_search_ad.path2 FROM ad_group_ad WHERE campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED' AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'");
  while (it.hasNext()) {
    var r = it.next(), a = r.adGroupAd, rsa = a.ad.responsiveSearchAd || {};
    Logger.log("### " + r.campaign.name + " > " + r.adGroup.name + " | ad " + a.ad.id + " | STRENGTH " + a.adStrength + " | " + (a.policySummary || {}).approvalStatus + " | " + (a.ad.finalUrls || []).join(" ") + " | /" + (rsa.path1 || "") + "/" + (rsa.path2 || ""));
    Logger.log("H: " + (rsa.headlines || []).map(function (h) { return h.text + (h.pinnedField ? "[" + h.pinnedField + "]" : ""); }).join(" ~ "));
    Logger.log("D: " + (rsa.descriptions || []).map(function (d) { return d.text; }).join(" ~ "));
  }
  var k = AdsApp.search("SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.quality_info.quality_score FROM keyword_view WHERE campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.quality_info.quality_score > 0");
  var qs = {}; while (k.hasNext()) { var x = k.next(); var key = x.campaign.name + " > " + x.adGroup.name; (qs[key] = qs[key] || []).push(x.adGroupCriterion.keyword.text + "=" + x.adGroupCriterion.qualityInfo.qualityScore); }
  Object.keys(qs).forEach(function (g) { Logger.log("QS " + g + ": " + qs[g].join(", ")); });
  Logger.log("DONE");
}

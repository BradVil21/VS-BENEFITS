/* VS Private Health - No Subsidy FL (Nov 6 2026).  PREVIEW first, then RUN.  Safe to re-run (resumes, skips what exists).
   New Search campaign, Florida only, $20/day, Maximize clicks with a $5 max CPC. Search ON, partners OFF, Display OFF.
   3 ad groups (Private / PPO, No subsidy / over income, Self-employed private), exact + phrase keywords,
   campaign negatives (Medicaid, Marketplace, ACA...), one responsive search ad per group -> /quote?type=individual&niche=private.
   The trucker campaign is not touched. Old "Individual - OE 2027 FL" and "No Subsidy - High Earners" stay paused. */
var NAME = "Private Health - No Subsidy FL", BUDGET = 20, MAX_CPC = 5;
var URL = "https://www.vshealthbenefits.com/quote?type=individual&niche=private";
var SUFFIX = "utm_source=google&utm_medium=cpc&utm_campaign=private-no-subsidy-fl&utm_term={keyword}";
var EN = "languageConstants/1000";
var NEG = ["medicaid", "medicare", "marketplace", "healthcare.gov", "healthcare gov", "obamacare", "obama care", "aca", "affordable care act",
  "open enrollment", "subsidy calculator", "free health insurance", "cheap health insurance", "short term", "short-term", "dental", "vision",
  "chip", "covered california", "florida blue medicaid", "low income", "apply for subsidy", "how to get a subsidy", "food stamps",
  "jobs", "careers", "login", "claims", "pet insurance", "car insurance", "auto insurance", "life insurance"];
var COMMON_H = ["Make Too Much for a Subsidy?", "Private Health Plans in FL", "Compare PPO Plans Today", "No Marketplace Required",
  "Free Quote, Licensed Advisor", "VS Health Benefits", "Individual & Family Plans", "Call a Licensed Advisor"];
var COMMON_D = ["Private, off-exchange plans for people who don't get a subsidy. Free advisor quote.",
  "Compare private PPO plans for individuals and families in Florida. No obligation."];
var GROUPS = [
  { name: "Private / PPO",
    exact: ["private health insurance florida", "private health insurance plans", "ppo health insurance florida", "ppo health insurance plans"],
    phrase: ["private health insurance", "ppo health insurance florida"],
    h: ["Private Health Insurance FL", "PPO Health Insurance Plans", "Nationwide PPO Networks"],
    d: ["Private PPO plans with nationwide doctor networks. Health questions apply.", "Apply any month and pick your start date. A licensed advisor compares carriers for you."] },
  { name: "No Subsidy / Over Income",
    exact: ["health insurance no subsidy", "health insurance for high income", "make too much for subsidy health insurance"],
    phrase: ["no subsidy health insurance", "private health insurance no subsidy"],
    h: ["No Subsidy? Compare Private", "Health Plans for High Income", "Paying Full Price for a Plan?"],
    d: ["Earn too much for a subsidy? Private plans are priced on age and health, not income.", "Stop paying full price. See private options side by side with a licensed advisor."] },
  { name: "Self-Employed Private",
    exact: ["self employed private health insurance", "health insurance for self employed florida"],
    phrase: ["self employed health insurance florida", "private health insurance self employed"],
    h: ["Self-Employed Health Plans FL", "Self-Employed? Go Private", "1099? Compare Private Plans"],
    d: ["Self-employed in Florida? Compare private PPO plans for you and your family.", "Premiums may be deductible for self-employed people. Ask your tax professional."] }
];
function q(s) { var o = [], it = AdsApp.search(s); while (it.hasNext()) o.push(it.next()); return o; }
function L(m) { Logger.log(m); }
function mut(op, label) { var r = AdsApp.mutate(op); var ok = r.isSuccessful(); L((ok ? "OK: " : "FAILED: ") + label + (ok ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); return ok ? (r.getResourceName() || true) : null; }
function main() {
  var preview = AdsApp.getExecutionInfo().isPreview();
  L(preview ? "PREVIEW (nothing is saved)" : "RUN");
  var bad = [];
  GROUPS.forEach(function (g) { var hs = COMMON_H.concat(g.h), seen = {};
    hs.forEach(function (x) { if (x.length > 30) bad.push(x + " (" + x.length + ")"); if (seen[x.toLowerCase()]) bad.push("dup " + x); seen[x.toLowerCase()] = 1; });
    COMMON_D.concat(g.d).forEach(function (x) { if (x.length > 90) bad.push(x + " (" + x.length + ")"); }); });
  if (bad.length) { L("COPY CHECK FAILED, nothing changed:\n" + bad.join("\n")); return; }
  var fl = q("SELECT geo_target_constant.resource_name FROM geo_target_constant WHERE geo_target_constant.name = 'Florida' AND geo_target_constant.country_code = 'US' AND geo_target_constant.target_type = 'State'");
  if (!fl.length) { L("Florida geo not found"); return; }
  var FL = fl[0].geoTargetConstant.resourceName;

  // 1. budget + campaign
  var c = q("SELECT campaign.resource_name, campaign.status FROM campaign WHERE campaign.name = '" + NAME + "' AND campaign.status != 'REMOVED'");
  var crn = c.length ? c[0].campaign.resourceName : null;
  if (crn) L("Campaign exists: " + crn);
  else {
    var cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, "");
    var res = AdsApp.mutateAll([
      { campaignBudgetOperation: { create: { resourceName: "customers/" + cid + "/campaignBudgets/-1", name: NAME + " budget " + Date.now(), amountMicros: BUDGET * 1e6, deliveryMethod: "STANDARD", explicitlyShared: false } } },
      { campaignOperation: { create: { resourceName: "customers/" + cid + "/campaigns/-2", name: NAME, status: "ENABLED", advertisingChannelType: "SEARCH",
          campaignBudget: "customers/" + cid + "/campaignBudgets/-1", targetSpend: { cpcBidCeilingMicros: MAX_CPC * 1e6 },
          networkSettings: { targetGoogleSearch: true, targetSearchNetwork: false, targetContentNetwork: false, targetPartnerSearchNetwork: false },
          geoTargetTypeSetting: { positiveGeoTargetType: "PRESENCE", negativeGeoTargetType: "PRESENCE" },
          finalUrlSuffix: SUFFIX, containsEuPoliticalAdvertising: "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING" } } }]);
    res.forEach(function (r) { L((r.isSuccessful() ? "OK: " : "FAILED: ") + "create " + (r.getResourceName() || "") + (r.isSuccessful() ? "" : " " + r.getErrorMessages().join("; "))); });
    if (!res[1].isSuccessful()) { L("Campaign not created; stopping."); return; }
    crn = res[1].getResourceName();
    if (preview) { L("Preview can't go further than creating the campaign (it doesn't really exist yet). RUN does the rest."); return; }
  }
  var C = "campaign.resource_name = '" + crn + "'";

  // 2. location, language, negatives
  var crit = {};
  q("SELECT campaign.resource_name, campaign_criterion.type, campaign_criterion.location.geo_target_constant, campaign_criterion.language.language_constant, campaign_criterion.keyword.text, campaign_criterion.negative FROM campaign_criterion WHERE " + C + " AND campaign_criterion.status != 'REMOVED'").forEach(function (r) {
    var x = r.campaignCriterion; if (x.type === "LOCATION") crit["loc:" + x.location.geoTargetConstant] = 1; if (x.type === "LANGUAGE") crit["lang:" + x.language.languageConstant] = 1; if (x.type === "KEYWORD") crit["neg:" + x.keyword.text.toLowerCase()] = 1; });
  if (!crit["loc:" + FL]) mut({ campaignCriterionOperation: { create: { campaign: crn, location: { geoTargetConstant: FL } } } }, "location Florida");
  if (!crit["lang:" + EN]) mut({ campaignCriterionOperation: { create: { campaign: crn, language: { languageConstant: EN } } } }, "language English");
  var nn = 0; NEG.forEach(function (w) { if (crit["neg:" + w]) return; if (mut({ campaignCriterionOperation: { create: { campaign: crn, negative: true, keyword: { text: w, matchType: "PHRASE" } } } }, "negative \"" + w + "\"")) nn++; });
  L("negatives added: " + nn);

  // 3. ad groups, keywords, ads
  GROUPS.forEach(function (g) {
    var ag = q("SELECT campaign.resource_name, ad_group.resource_name FROM ad_group WHERE " + C + " AND ad_group.name = '" + g.name + "' AND ad_group.status != 'REMOVED'");
    var grn = ag.length ? ag[0].adGroup.resourceName : mut({ adGroupOperation: { create: { campaign: crn, name: g.name, status: "ENABLED", type: "SEARCH_STANDARD" } } }, "ad group " + g.name);
    if (!grn) return;
    var have = {};
    q("SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE ad_group.resource_name = '" + grn + "' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED'").forEach(function (r) { have[r.adGroupCriterion.keyword.text + "|" + r.adGroupCriterion.keyword.matchType] = 1; });
    g.exact.forEach(function (k) { if (!have[k + "|EXACT"]) mut({ adGroupCriterionOperation: { create: { adGroup: grn, status: "ENABLED", keyword: { text: k, matchType: "EXACT" } } } }, "[" + k + "]"); });
    g.phrase.forEach(function (k) { if (!have[k + "|PHRASE"]) mut({ adGroupCriterionOperation: { create: { adGroup: grn, status: "ENABLED", keyword: { text: k, matchType: "PHRASE" } } } }, "\"" + k + "\""); });
    if (q("SELECT ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group.resource_name = '" + grn + "' AND ad_group_ad.status != 'REMOVED'").length) { L("ad already in " + g.name); return; }
    mut({ adGroupAdOperation: { create: { adGroup: grn, status: "ENABLED", ad: { finalUrls: [URL], responsiveSearchAd: {
      headlines: g.h.concat(COMMON_H).map(function (t) { return { text: t }; }), descriptions: COMMON_D.concat(g.d).map(function (t) { return { text: t }; }), path1: "Private-Plans" } } } } }, "ad in " + g.name);
  });
  L("DONE");
}

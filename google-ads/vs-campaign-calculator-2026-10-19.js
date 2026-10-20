/* VS Campaign: "ACA Calculator - FL" (Oct 19 2026). Search, Florida, EN+ES, $10/day, Max clicks $4 cap,
   landing /aca-subsidy-calculator (lead-gated). Creates ENABLED. Skips if the campaign already exists. */
var SITE = "https://www.vshealthbenefits.com";
var NAME = "ACA Calculator - FL";
var H = ["2027 Subsidy Calculator","See Your 2027 Price in 60 Sec","Free ACA Calculator, Florida","Will You Get a Tax Credit?","Premiums Up? Check Your Price","Obamacare Calculator 2027","Estimate Your 2027 Premium","Free, Takes 60 Seconds","Licensed FL Health Broker","Open Enrollment Starts Nov 1","See Bronze, Silver, Gold Cost","Calculadora de Subsidio","No Cost, No Obligation"];
var D = ["Enter your income and household. See your 2027 tax credit and plan prices in 60 seconds.","Free calculator from a licensed Florida broker. Real plans and prices confirmed free.","2027 premiums are up. See what you'll actually pay before open enrollment starts Nov 1.","No cost, no obligation. English y Español. A licensed advisor can confirm your numbers."];
var K = ["aca subsidy calculator 2027","aca subsidy calculator","obamacare calculator","obamacare subsidy calculator","marketplace subsidy calculator","health insurance tax credit calculator","premium tax credit calculator","how much will obamacare cost 2027","aca premium calculator florida","health insurance cost calculator florida","calculadora de subsidio obamacare"];
var NEG = ["medicaid","low income","login","sign in","phone number","customer service","jobs","salary","paycheck","income tax","mortgage","loan","bmi","medicare","dental","vision","car insurance","auto insurance","life insurance"];

function main() {
  var bad = [];
  H.forEach(function (x) { if (x.length > 30) bad.push("H " + x); });
  D.forEach(function (x) { if (x.length > 90) bad.push("D " + x + " (" + x.length + ")"); });
  if (bad.length) { Logger.log("LENGTH ERRORS:\n" + bad.join("\n")); return; }
  var it = AdsApp.search("SELECT campaign.name FROM campaign WHERE campaign.status != 'REMOVED'");
  while (it.hasNext()) if (it.next().campaign.name === NAME) { Logger.log("SKIP (exists): " + NAME); return; }
  var fl = null;
  it = AdsApp.search("SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.country_code = 'US' AND geo_target_constant.target_type = 'State'");
  while (it.hasNext()) { var g = it.next().geoTargetConstant; if (g.name === "Florida") fl = g.resourceName; }
  if (!fl) { Logger.log("No Florida geo"); return; }
  var P = "customers/" + AdsApp.currentAccount().getCustomerId().replace(/-/g, "") + "/";
  var b = P + "campaignBudgets/-1", cr = P + "campaigns/-2", ag = P + "adGroups/-3";
  var ops = [
    { campaignBudgetOperation: { create: { resourceName: b, name: NAME + " budget", amountMicros: 10000000, deliveryMethod: "STANDARD", explicitlyShared: false } } },
    { campaignOperation: { create: { resourceName: cr, name: NAME, status: "ENABLED", advertisingChannelType: "SEARCH", campaignBudget: b,
      networkSettings: { targetGoogleSearch: true, targetSearchNetwork: false, targetContentNetwork: false, targetPartnerSearchNetwork: false },
      geoTargetTypeSetting: { positiveGeoTargetType: "PRESENCE", negativeGeoTargetType: "PRESENCE" },
      targetSpend: { cpcBidCeilingMicros: 4000000 },
      finalUrlSuffix: "utm_source=google&utm_medium=cpc&utm_campaign=aca-calculator-fl&utm_term={keyword}",
      containsEuPoliticalAdvertising: "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING" } } },
    { campaignCriterionOperation: { create: { campaign: cr, location: { geoTargetConstant: fl } } } },
    { campaignCriterionOperation: { create: { campaign: cr, language: { languageConstant: "languageConstants/1000" } } } },
    { campaignCriterionOperation: { create: { campaign: cr, language: { languageConstant: "languageConstants/1003" } } } },
    { adGroupOperation: { create: { resourceName: ag, name: "Subsidy Calculator", campaign: cr, status: "ENABLED", type: "SEARCH_STANDARD" } } }
  ];
  NEG.forEach(function (k) { ops.push({ campaignCriterionOperation: { create: { campaign: cr, negative: true, keyword: { text: k, matchType: "PHRASE" } } } }); });
  K.forEach(function (k) { ["PHRASE", "EXACT"].forEach(function (mt) {
    ops.push({ adGroupCriterionOperation: { create: { adGroup: ag, status: "ENABLED", keyword: { text: k, matchType: mt } } } }); }); });
  ops.push({ adGroupAdOperation: { create: { adGroup: ag, status: "ENABLED", ad: { finalUrls: [SITE + "/aca-subsidy-calculator"],
    responsiveSearchAd: { headlines: H.map(function (x) { return { text: x }; }), descriptions: D.map(function (x) { return { text: x }; }), path1: "calculator", path2: "2027" } } } } });
  var res = AdsApp.mutateAll(ops, { partialFailure: false }), errs = [];
  res.forEach(function (r) { if (!r.isSuccessful()) errs = errs.concat(r.getErrorMessages()); });
  Logger.log((errs.length ? "FAILED: " : "OK: ") + NAME + " (" + ops.length + " ops)" + (errs.length ? "\n  " + errs.slice(0, 6).join("\n  ") : ""));
  if (errs.length) return;
  // Reuse the account's existing call + callout assets.
  var real = null; it = AdsApp.search("SELECT campaign.resource_name FROM campaign WHERE campaign.name = '" + NAME + "'");
  if (it.hasNext()) real = it.next().campaign.resourceName;
  var aops = [];
  it = AdsApp.search("SELECT asset.resource_name, asset.type FROM asset WHERE asset.type IN ('CALL','CALLOUT')");
  while (it.hasNext()) { var a = it.next().asset; aops.push({ campaignAssetOperation: { create: { campaign: real, asset: a.resourceName, fieldType: a.type } } }); }
  if (real && aops.length) {
    var ar = AdsApp.mutateAll(aops, { partialFailure: true }), ok = 0;
    ar.forEach(function (r) { if (r.isSuccessful()) ok++; });
    Logger.log("  assets linked: " + ok + "/" + aops.length);
  }
}

/* VS Trucker REBUILD (Nov 25 2026). Built from GOOGLE-ADS-PLAYBOOK.md + TRUCKER-REBUILD-2026-11-25.md.
   PREVIEW first, then RUN. Safe to re-run (only adds what is missing).
   EVERYTHING IS CREATED PAUSED. This script never switches anything on. Bradley turns them on himself.
     Trucker Core - Exact ............... $40/day  PAUSED  the keywords that already made leads, exact match only
     Trucker Owner-Op & 1099 - Exact .... $10/day  PAUSED  owner-operator / independent / 1099 driver keywords
   Each: Google Search only (no Display, no Search Partners), Florida + Georgia, "people in or regularly in",
   English + Spanish, Manual CPC (Core $12, Owner-Op $10 starting bids), campaign negatives from the Nov 25
   search terms review, one responsive search ad per ad group (headline 1 pinned), 4 sitelinks, 5 callouts, call asset. */

var SITE = "https://www.vshealthbenefits.com";
var LANDING = "/quote?type=individual&niche=trucking";
var REUSE_CALL_FROM = ["Trucker Health - Private PPO", "Self-Employed FL - 2027", "FL Health Insurance - Search Leads"];
var STATES = ["Florida", "Georgia"];
var LANGS = ["languageConstants/1000", "languageConstants/1003"];   // English, Spanish
var PHONE = "(954) 866-6872";
var HOURS = [["MONDAY", 8, 20], ["TUESDAY", 8, 20], ["WEDNESDAY", 8, 20], ["THURSDAY", 8, 20], ["FRIDAY", 8, 20], ["SATURDAY", 10, 17]];  // closed Sunday

var CAMPAIGNS = [
  { name: "Trucker Core - Exact", budget: 40, slug: "trucker-core", group: "Truck Driver Health Insurance", bid: 12,
    pin: "Truck Driver Health Insurance", path: ["truckers", "quote"],
    k: ["health insurance for truck drivers", "truck driver health insurance", "medical insurance for truck drivers",
        "truck driver medical insurance", "health insurance for truckers", "truckers health insurance", "truckers medical insurance",
        "best health insurance for truck drivers", "best medical insurance for truck drivers", "otr driver health insurance",
        "cdl driver health insurance"] },
  { name: "Trucker Owner-Op & 1099 - Exact", budget: 10, slug: "trucker-ownerop", group: "Owner-Operator & 1099", bid: 10,
    pin: "Owner-Operators Welcome", path: ["owner-operator", "quote"],
    k: ["owner operator health insurance", "health insurance for owner operators", "health insurance for owner operator truck drivers",
        "health insurance for independent truckers", "independent truckers health insurance", "health insurance for 1099 truck drivers",
        "1099 truck driver health insurance"] }
];

// Headlines (<=30). The campaign's "pin" headline is pinned to position 1.
var H = ["Truck Driver Health Insurance", "Health Insurance for Truckers", "Lost Your Company Plan?", "Nationwide PPO for Drivers",
  "See Doctors in Any State", "Telehealth From the Cab", "Licensed Agent for Truckers", "Owner-Operators Welcome",
  "Covered Between Carriers", "OTR Drivers: Read This First", "Plans for 1099 Drivers", "Coverage for Your Family Too",
  "Talk to a Real Person", "Text or Call, Your Choice", "Get a Free Quote Today"];
var D = ["Drivers who lose a company plan have options. Compare PPO plans with a licensed agent.",
  "Nationwide PPO options, telehealth and urgent care that work wherever your route goes.",
  "Owner-operator or company driver? Get a free quote and a plain-English plan review.",
  "We help truckers get covered every day. Text or call. Quote in about 2 minutes."];
var SITELINKS = [["Get a Trucker Quote", LANDING, "Quote in about 2 minutes", "Text or call, your choice"],
  ["Owner-Operator Guide", "/best-health-insurance-owner-operators", "Coverage when you go on your own", "What to look for in a plan"],
  ["1099 Truck Drivers", "/1099-truck-driver-health-insurance", "Health plans for 1099 drivers", "Options outside a company plan"],
  ["Can Truckers Deduct It?", "/can-truckers-deduct-health-insurance", "Self-employed deduction basics", "Ask your tax pro to confirm"]];
var CALLOUTS = ["Nationwide PPO Options", "Licensed Agents", "Text or Call", "No Cost to Compare", "English & Spanish"];

// Campaign negatives (phrase unless marked EXACT). From the Nov 25 search terms review + trucker extras.
var NEG = ["medicare", "part d", "medigap", "over 65", "60 years", "costco", "aarp", "sams club", "free insurance", "free health insurance",
  "medicaid", "insurance top 10", "best insurance companies", "kemper", "metlife", "gravie", "meritain", "alera", "choice arrangements",
  "covercincy", "oregon", "jobs", "hiring", "salary", "login", "phone number", "customer service", "dental", "vision", "vsp", "eye",
  "cdl school", "cdl training", "dot physical", "truck insurance", "commercial truck insurance", "cargo", "liability", "bobtail",
  "occupational accident", "workers comp", "rate per mile", "landstar", "swift", "statefarm", "state farm", "nationwide insurance",
  "chubb", "hartford", "great west", "liberty mutual", "aaa", "ichra", "deductible meaning", "what is"];
var NEG_EXACT = ["insurance", "insurance agent"];

// ---------------------------------------------------------------- helpers
var CID, PREVIEW, tmp = -1, problems = [];
function T(type) { return "customers/" + CID + "/" + type + "/" + (tmp--); }
function say(m) { Logger.log(m); }
function bad(m) { problems.push(m); Logger.log("!! " + m); }
function chk(text, max, where) { if (String(text).length > max) bad("TOO LONG (" + String(text).length + ">" + max + ") " + where + ": " + text); return text; }
function q(gaql) { var out = [], it = AdsApp.search(gaql); while (it.hasNext()) out.push(it.next()); return out; }
function errs(r) { try { return r.getErrorMessages().join(" | "); } catch (e) { return String(e); } }
function quoteList(a) { return "(" + a.map(function (s) { return "'" + s.replace(/'/g, "\\'") + "'"; }).join(", ") + ")"; }
function run(label, ops) {
  if (!ops.length) return [];
  say(label + " (" + ops.length + " changes)...");
  var res = AdsApp.mutateAll(ops, { partialFailure: false });
  var fail = res.filter(function (r) { return !r.isSuccessful(); });
  if (fail.length) { fail.slice(0, 5).forEach(function (r) { bad(label + " error: " + errs(r)); }); return null; }
  say("OK  " + label + (PREVIEW ? " (preview: accepted)" : ""));
  return res;
}

function main() {
  CID = AdsApp.currentAccount().getCustomerId().replace(/-/g, "");
  PREVIEW = AdsApp.getExecutionInfo().isPreview();
  say((PREVIEW ? "PREVIEW" : "RUN") + " - account " + AdsApp.currentAccount().getName() + " (" + CID + ")");

  H.forEach(function (h) { chk(h, 30, "headline"); });
  D.forEach(function (d) { chk(d, 90, "description"); });
  CAMPAIGNS.forEach(function (c) { c.path.forEach(function (p) { chk(p, 15, c.name + " path"); }); if (H.indexOf(c.pin) < 0) bad(c.name + ": pinned headline not in list"); });
  SITELINKS.forEach(function (s) { chk(s[0], 25, "sitelink"); chk(s[2], 35, "sitelink d1"); chk(s[3], 35, "sitelink d2"); });
  CALLOUTS.forEach(function (s) { chk(s, 25, "callout"); });
  if (H.length > 15) bad("More than 15 headlines");
  if (problems.length) { say("STOPPED: fix the copy above, nothing was changed."); return; }

  var existing = {};
  q("SELECT campaign.name, campaign.resource_name FROM campaign WHERE campaign.status != 'REMOVED'").forEach(function (r) { existing[r.campaign.name] = r.campaign.resourceName; });
  var states = {};
  q("SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.country_code = 'US' AND geo_target_constant.target_type = 'State' AND geo_target_constant.status = 'ENABLED'")
    .forEach(function (r) { states[r.geoTargetConstant.name] = r.geoTargetConstant.resourceName; });
  STATES.forEach(function (s) { if (!states[s]) bad("No geo target found for " + s); });
  var callAsset = null;
  q("SELECT campaign.name, campaign_asset.asset FROM campaign_asset WHERE campaign_asset.status = 'ENABLED' AND campaign_asset.field_type = 'CALL' AND campaign.name IN " + quoteList(REUSE_CALL_FROM))
    .forEach(function (r) { if (!callAsset) callAsset = r.campaignAsset.asset; });
  say("Call asset: " + (callAsset ? "reusing the existing one" : "none found, will create one"));
  if (problems.length) { say("STOPPED: nothing was changed."); return; }
  try { build(existing, states, callAsset); }
  catch (e) { bad("Script error: " + e.message + (e.stack ? " | " + String(e.stack).split("\n").slice(0, 3).join(" / ") : "")); }
  say(problems.length ? "DONE WITH " + problems.length + " WARNING(S) - see lines starting with !!" : "DONE. No errors. Both campaigns are PAUSED.");
}

function build(existing, states, callAsset) {
  var camp = {};
  CAMPAIGNS.forEach(function (c) { if (existing[c.name]) camp[c.name] = existing[c.name]; });

  // Step A: campaigns (PAUSED) + call asset
  var missing = CAMPAIGNS.filter(function (c) { return !camp[c.name]; });
  if (missing.length) {
    var opsA = [], idx = {};
    if (!callAsset) { idx.call = opsA.length; opsA.push({ assetOperation: { create: { resourceName: T("assets"), callAsset: { countryCode: "US", phoneNumber: PHONE,
      callConversionReportingState: "USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION",
      adScheduleTargets: HOURS.map(function (h) { return { dayOfWeek: h[0], startHour: h[1], startMinute: "ZERO", endHour: h[2], endMinute: "ZERO" }; }) } } } }); }
    missing.forEach(function (c) {
      var bRn = T("campaignBudgets");
      opsA.push({ campaignBudgetOperation: { create: { resourceName: bRn, name: c.name + " budget", amountMicros: Math.round(c.budget * 1e6), deliveryMethod: "STANDARD", explicitlyShared: false } } });
      idx["c:" + c.name] = opsA.length;
      opsA.push({ campaignOperation: { create: {
        resourceName: T("campaigns"), name: c.name, status: "PAUSED", advertisingChannelType: "SEARCH", campaignBudget: bRn,
        networkSettings: { targetGoogleSearch: true, targetSearchNetwork: false, targetContentNetwork: false, targetPartnerSearchNetwork: false },
        geoTargetTypeSetting: { positiveGeoTargetType: "PRESENCE", negativeGeoTargetType: "PRESENCE" },
        manualCpc: { enhancedCpcEnabled: false },
        finalUrlSuffix: "utm_source=google&utm_medium=cpc&utm_campaign=" + c.slug + "&utm_term={keyword}",
        containsEuPoliticalAdvertising: "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING" } } });
    });
    var resA = run("Step A: create " + missing.map(function (c) { return c.name; }).join(" + ") + " (PAUSED)", opsA);
    if (!resA) return;
    if (PREVIEW) { say("Preview: step A accepted. Click Run to build everything (it stays PAUSED)."); return; }
    if (idx.call !== undefined) callAsset = resA[idx.call].getResourceName();
    missing.forEach(function (c) { camp[c.name] = resA[idx["c:" + c.name]].getResourceName(); });
  } else say("Both campaigns already exist - adding only what is missing.");

  var names = quoteList(CAMPAIGNS.map(function (c) { return c.name; }));
  var locs = {}; q("SELECT campaign.name FROM campaign_criterion WHERE campaign_criterion.type = 'LOCATION' AND campaign.name IN " + names).forEach(function (r) { locs[r.campaign.name] = 1; });
  var groups = {}; q("SELECT campaign.name, ad_group.resource_name FROM ad_group WHERE ad_group.status != 'REMOVED' AND campaign.name IN " + names).forEach(function (r) { groups[r.campaign.name] = r.adGroup.resourceName; });
  var kws = {}; q("SELECT campaign.name FROM ad_group_criterion WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED' AND campaign.name IN " + names).forEach(function (r) { kws[r.campaign.name] = 1; });
  var ads = {}; q("SELECT campaign.name FROM ad_group_ad WHERE ad_group_ad.status != 'REMOVED' AND campaign.name IN " + names).forEach(function (r) { ads[r.campaign.name] = 1; });

  // Step B: locations, languages, negatives, sitelinks, callouts, call asset
  var needB = CAMPAIGNS.filter(function (c) { return !locs[c.name]; });
  if (needB.length) {
    var opsS = [];
    SITELINKS.forEach(function (s) { opsS.push({ assetOperation: { create: { resourceName: T("assets"), finalUrls: [SITE + s[1]], sitelinkAsset: { linkText: s[0], description1: s[2], description2: s[3] } } } }); });
    CALLOUTS.forEach(function (s) { opsS.push({ assetOperation: { create: { resourceName: T("assets"), calloutAsset: { calloutText: s } } } }); });
    var resS = run("Sitelinks + callouts", opsS); if (!resS) return;
    var opsB = [];
    needB.forEach(function (c) {
      var cRn = camp[c.name];
      STATES.forEach(function (st) { opsB.push({ campaignCriterionOperation: { create: { campaign: cRn, location: { geoTargetConstant: states[st] } } } }); });
      LANGS.forEach(function (l) { opsB.push({ campaignCriterionOperation: { create: { campaign: cRn, language: { languageConstant: l } } } }); });
      NEG.forEach(function (n) { opsB.push({ campaignCriterionOperation: { create: { campaign: cRn, negative: true, keyword: { text: n, matchType: "PHRASE" } } } }); });
      NEG_EXACT.forEach(function (n) { opsB.push({ campaignCriterionOperation: { create: { campaign: cRn, negative: true, keyword: { text: n, matchType: "EXACT" } } } }); });
      if (callAsset) opsB.push({ campaignAssetOperation: { create: { campaign: cRn, asset: callAsset, fieldType: "CALL" } } });
      resS.forEach(function (r, i) { opsB.push({ campaignAssetOperation: { create: { campaign: cRn, asset: r.getResourceName(), fieldType: i < SITELINKS.length ? "SITELINK" : "CALLOUT" } } }); });
    });
    if (!run("Step B: Florida + Georgia, languages, " + (NEG.length + NEG_EXACT.length) + " negatives, assets", opsB)) return;
  }

  // Step C: ad groups (with starting bids)
  var opsG = [], gi = [];
  CAMPAIGNS.forEach(function (c) { if (groups[c.name]) return; gi.push({ c: c, i: opsG.length });
    opsG.push({ adGroupOperation: { create: { resourceName: T("adGroups"), campaign: camp[c.name], name: c.group, status: "ENABLED", type: "SEARCH_STANDARD", cpcBidMicros: Math.round(c.bid * 1e6) } } }); });
  if (opsG.length) { var resG = run("Step C: ad groups", opsG); if (!resG) return; gi.forEach(function (x) { groups[x.c.name] = resG[x.i].getResourceName(); }); }

  // Step D: keywords (EXACT) + responsive search ads
  var opsD = [];
  CAMPAIGNS.forEach(function (c) {
    var gRn = groups[c.name];
    if (!kws[c.name]) c.k.forEach(function (w) { opsD.push({ adGroupCriterionOperation: { create: { adGroup: gRn, status: "ENABLED", keyword: { text: w, matchType: "EXACT" } } } }); });
    if (!ads[c.name]) {
      var heads = [c.pin].concat(H.filter(function (h) { return h !== c.pin; })).slice(0, 15).map(function (t, i) { return i === 0 ? { text: t, pinnedField: "HEADLINE_1" } : { text: t }; });
      opsD.push({ adGroupAdOperation: { create: { adGroup: gRn, status: "ENABLED", ad: { finalUrls: [SITE + LANDING],
        responsiveSearchAd: { headlines: heads, descriptions: D.map(function (t) { return { text: t }; }), path1: c.path[0], path2: c.path[1] } } } } });
    }
  });
  if (!run("Step D: exact-match keywords + ads", opsD)) return;
  CAMPAIGNS.forEach(function (c) { say("OK  " + c.name + "  $" + c.budget + "/day  start bid $" + c.bid + "  " + c.k.length + " keywords  PAUSED"); });
}

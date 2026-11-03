/* VS 8 States: Truckers + Self-Employed (Nov 3 2026). PREVIEW first, then RUN. Safe to re-run.
   Both campaigns now target FL, GA, IL, KY, MD, MO, OH, TX (the health insurance certification states).
   For each campaign:
   1. A new 8-state ad in every enabled ad group (no Florida-only wording; {LOCATION(State)} inserts the
      searcher's state). Old enabled ads are paused only after the new one saves.
   2. Campaign sitelinks, callouts and structured snippets for all 8 states. Existing campaign assets that
      mention Florida are unlinked from the campaign (the asset itself is kept).
   3. State keywords (phrase match) for the 7 new states.
   4. Search partners off (Google Search only). */
var SITE = "https://www.vshealthbenefits.com";
var NEW_STATES = ["georgia", "illinois", "kentucky", "maryland", "missouri", "ohio", "texas"];
var LOC_FALLBACK = "Serving TX, GA, OH, IL & More";

var CAMPAIGNS = [
 { name: "Trucker Health - OE 2027", url: "/trucking-health-quote", skip: ["Trucking Company (Group)", "Spanish"],
   mark: "Free Quote From the Cab",
   commonH: ["Free Quote From the Cab", "Health Insurance for Truckers", "Open Enrollment Is Open Now", "Enroll by Dec 15 for Jan 1",
     "Plans That Work on the Road", "Nationwide PPO Options", "Licensed Broker. No Fee.", "Talk to a Licensed Advisor",
     "Quote in About 2 Minutes", "Priced on What You Net"],
   commonD: ["Truck drivers in TX, GA, OH, IL, MO, KY, MD and FL: compare plans with a licensed broker.",
     "Owner-operators and 1099 drivers may get tax credits based on net income after costs.",
     "Open enrollment ends Jan 15. Enroll by Dec 15 for Jan 1 coverage. Quote in 2 minutes.",
     "Carriers pay us, not you. Same price as going direct, with an advisor who knows trucking."],
   groups: {
     "Truck Driver Health Insurance": { p: ["truckers", "free-quote"],
       h: ["Truck Driver Health Insurance", "{LOCATION(State)} Trucker Plans", "Coverage for OTR & Regional", "See Doctors in Other States", "Plans for You and Your Family"],
       kw: ["truck driver health insurance %s", "health insurance for truck drivers in %s"] },
     "Owner Operator": { p: ["owner-operator", "free-quote"],
       h: ["Owner Operator Health Plans", "{LOCATION(State)} Owner Operators", "Premiums May Be Deductible", "Tax Credits on Net Income", "Built for Owner Operators"],
       d1: "Owner-operators: premiums may be deductible, and tax credits use net income after costs.",
       kw: ["owner operator health insurance %s"] },
     "1099 Driver": { p: ["1099-drivers", "free-quote"],
       h: ["1099 Driver Health Coverage", "1099 Drivers in {LOCATION(State)}", "No Employer Plan? Get Covered", "Tax Credits on Net Income", "Self-Employed Driver Plans"], kw: [] },
     "2027 Rate Increase - Drivers": { p: ["truckers", "2027-rates"],
       h: ["2027 Rate Increase? Shop Now", "Renewal Went Up? Compare Free", "Lower Your 2027 Premium", "{LOCATION(State)} Trucker Plans", "Don't Auto-Renew. Compare."],
       d1: "Did your 2027 renewal go up? Compare plans before you auto-renew. Licensed advisor help.", kw: [] },
     "Company Driver - No Benefits": { p: ["company-driver", "get-covered"],
       h: ["Company Driver, No Benefits?", "Skip the Long Waiting Period", "Coverage Can Start Next Month", "Covered Between Carriers", "{LOCATION(State)} Trucker Plans"],
       d1: "Driving for a carrier with no benefits or a long wait? Get covered on your own now.", kw: [] }
   },
   dflt: { p: ["truckers", "free-quote"],
     h: ["Truck Driver Health Insurance", "{LOCATION(State)} Trucker Plans", "Coverage for OTR & Regional", "See Doctors in Other States", "Plans for You and Your Family"], kw: [] },
   sitelinks: [
     ["Get My Free Quote", "/trucking-health-quote", "Answer a few quick questions", "A licensed advisor follows up"],
     ["Owner-Operator Plans", "/best-health-insurance-owner-operators", "Plans for O/O and 1099 drivers", "Tax credits on net income"],
     ["What Drivers Pay in 2027", "/truck-driver-health-insurance-cost", "2027 premium ranges", "See what truckers really pay"],
     ["Plans by State", "/truck-driver-health-insurance", "TX GA OH IL MO KY MD FL", "Networks that travel with you"],
     ["Open Enrollment 2027", "/truck-driver-open-enrollment-2027", "Deadlines for truck drivers", "Enroll by Dec 15 for Jan 1"],
     ["DOT Physical Coverage", "/does-health-insurance-cover-dot-physical", "What plans cover for CDL", "Know before your exam"],
     ["Subsidy Cliff Calculator", "/owner-operator-subsidy-cliff-calculator", "Check your tax credit", "Built for owner-operators"]],
   callouts: ["No Fee to You", "Licensed Advisor", "Same-Day Quotes", "Nationwide PPO Options", "Coverage on the Road",
     "Owner-Operators Welcome", "Family Plans Available", "Open Enrollment Now"],
   snippets: [["Types", ["Owner-Operator", "Lease Operator", "Company Driver", "1099 Driver", "OTR Driver"]],
     ["Insurance coverage", ["PPO Plans", "Marketplace Plans", "Family Plans", "Individual Plans"]]]
 },
 { name: "Self-Employed FL - 2027", url: null /* keep each ad group's existing landing page */, fallbackUrl: "/self-employed-health-insurance", skip: [],
   mark: "Self-Employed? Free Quote",
   commonH: ["Self-Employed? Free Quote", "Health Plans for Self-Employed", "Open Enrollment Is Open Now", "Enroll by Dec 15 for Jan 1",
     "Priced on Your Net Income", "Tax Credits on Net Income", "Licensed Broker. No Fee.", "Talk to a Licensed Advisor",
     "Quote in About 2 Minutes", "Plans for You and Your Family"],
   commonD: ["Self-employed in TX, GA, OH, IL, MO, KY, MD or FL? Compare 2027 plans with a licensed pro.",
     "Tax credits use your net income after business costs. We make sure you get every dollar.",
     "Open enrollment ends Jan 15. Enroll by Dec 15 for Jan 1 coverage. Quote in 2 minutes.",
     "Carriers pay us, not you. Same price as going direct, with an advisor on your side."],
   groups: {
     "Self-Employed Health Insurance": { p: ["self-employed", "free-quote"],
       h: ["Self-Employed Health Insurance", "{LOCATION(State)} Self-Employed", "Freelancer & Gig Worker Plans", "Premiums May Be Deductible", "Compare Top Carriers Free"],
       kw: ["self employed health insurance %s"] },
     "1099 & Independent Contractors": { p: ["1099", "free-quote"],
       h: ["1099 Health Insurance", "Independent Contractor Plans", "{LOCATION(State)} 1099 Workers", "No Employer Plan? Get Covered", "Premiums May Be Deductible"], kw: [] },
     "Sole Proprietor & LLC Owners": { p: ["business-owner", "free-quote"],
       h: ["Business Owner Health Plans", "Sole Proprietor Health Plans", "LLC Owner Health Insurance", "{LOCATION(State)} Business Owners", "Premiums May Be Deductible"], kw: [] }
   },
   dflt: { p: ["self-employed", "free-quote"],
     h: ["Self-Employed Health Insurance", "{LOCATION(State)} Self-Employed", "Freelancer & Gig Worker Plans", "Premiums May Be Deductible", "Compare Top Carriers Free"], kw: [] },
   sitelinks: [
     ["Get My Free Quote", "/quote", "Answer a few quick questions", "A licensed advisor follows up"],
     ["Self-Employed Plans", "/self-employed-health-insurance", "Plans priced on net income", "Compare top carriers free"],
     ["1099 Worker Coverage", "/1099-health-insurance", "No employer plan? Get covered", "Freelancers and contractors"],
     ["Business Owner Plans", "/health-insurance-for-small-business-owners", "Sole proprietors and LLCs", "Cover you and your family"],
     ["Family Plans", "/family-health-insurance", "Cover your spouse and kids", "2027 family plan costs"],
     ["Subsidy Calculator", "/aca-subsidy-calculator", "See your 2027 tax credit", "Takes about a minute"]],
   callouts: ["No Fee to You", "Licensed Advisor", "Same-Day Quotes", "Family Plans Available", "Open Enrollment Now", "Tax Credits Checked Free"],
   snippets: [["Types", ["Freelancer", "1099 Contractor", "Sole Proprietor", "LLC Owner", "Gig Worker"]],
     ["Insurance coverage", ["PPO Plans", "Marketplace Plans", "Family Plans", "Individual Plans"]]]
 }
];

function L(ok, m, r) { Logger.log((ok ? "OK: " : "FAILED: ") + m + (ok || !r ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); }
function q(s) { return AdsApp.search(s); }
function hlen(x) { return x.replace("{LOCATION(State)}", "Maryland").length; }

function validate() {
  var bad = [];
  CAMPAIGNS.forEach(function (C) {
    var all = Object.keys(C.groups).map(function (g) { return [g, C.groups[g]]; }).concat([["default", C.dflt]]);
    all.forEach(function (e) { var g = e[0], cfg = e[1], h = cfg.h.concat(C.commonH);
      if (h.length > 15) bad.push(C.name + "/" + g + ": " + h.length + " headlines");
      if (C.commonH.indexOf(C.mark) < 0) bad.push(C.name + ": marker not in headlines");
      var seen = {}; h.forEach(function (x) { if (hlen(x) > 30) bad.push("H " + x + " (" + hlen(x) + ")"); if (seen[x.toLowerCase()]) bad.push("dup H in " + g + ": " + x); seen[x.toLowerCase()] = 1; });
      cfg.p.forEach(function (x) { if (x.length > 15) bad.push("P " + x); });
      if (cfg.d1 && cfg.d1.length > 90) bad.push("D1 " + g + " (" + cfg.d1.length + ")"); });
    C.commonD.forEach(function (x) { if (x.length > 90) bad.push("D " + x + " (" + x.length + ")"); });
    C.sitelinks.forEach(function (s) { if (s[0].length > 25) bad.push("SL " + s[0]); if (s[2].length > 35 || s[3].length > 35) bad.push("SL desc " + s[0]); });
    C.callouts.forEach(function (c) { if (c.length > 25) bad.push("CO " + c); });
    C.snippets.forEach(function (s) { s[1].forEach(function (v) { if (v.length > 25) bad.push("SN " + v); }); });
  });
  if (LOC_FALLBACK.length > 30) bad.push("fallback too long");
  return bad;
}

function createAd(agrn, C, cfg, url, useLoc) {
  var H = cfg.h.concat(C.commonH).map(function (t) { return useLoc ? t : (t.indexOf("{LOCATION") >= 0 ? LOC_FALLBACK : t); });
  var D = C.commonD.slice(); if (cfg.d1) D[1] = cfg.d1;
  return AdsApp.mutate({ adGroupAdOperation: { create: { adGroup: agrn, status: "ENABLED", ad: { finalUrls: [url], responsiveSearchAd: {
    headlines: H.map(function (t) { return { text: t }; }), descriptions: D.map(function (t) { return { text: t }; }), path1: cfg.p[0], path2: cfg.p[1] } } } } });
}

function runCampaign(C, cid) {
  Logger.log("=== " + C.name + " ===");
  var it = q("SELECT campaign.resource_name, campaign.network_settings.target_search_network FROM campaign WHERE campaign.name = '" + C.name + "' AND campaign.status != 'REMOVED'");
  if (!it.hasNext()) { Logger.log("MISSING campaign " + C.name); return; }
  var c = it.next().campaign, crn = c.resourceName;

  if (c.networkSettings && c.networkSettings.targetSearchNetwork) {
    var rn = AdsApp.mutate({ campaignOperation: { update: { resourceName: crn, networkSettings: { targetSearchNetwork: false } }, updateMask: "networkSettings.targetSearchNetwork" } });
    L(rn.isSuccessful(), "Search partners OFF", rn);
  } else Logger.log("Search partners already off");

  var groups = []; it = q("SELECT ad_group.resource_name, ad_group.name FROM ad_group WHERE campaign.resource_name = '" + crn + "' AND ad_group.status = 'ENABLED'");
  while (it.hasNext()) groups.push(it.next().adGroup);
  Logger.log("Enabled ad groups: " + groups.map(function (g) { return g.name; }).join(" | "));
  groups.forEach(function (g) {
    if (C.skip.some(function (s) { return g.name.indexOf(s) >= 0; })) { Logger.log("Skipped: " + g.name); return; }
    var cfg = C.groups[g.name] || C.dflt, agrn = g.resourceName;
    var olds = [], done = false, oldUrl = "";
    var a = q("SELECT ad_group_ad.resource_name, ad_group_ad.status, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines FROM ad_group_ad WHERE ad_group.resource_name = '" + agrn + "' AND ad_group_ad.status IN ('ENABLED','PAUSED')");
    while (a.hasNext()) { var x = a.next().adGroupAd; var hs = ((x.ad.responsiveSearchAd || {}).headlines || []).map(function (h) { return h.text; });
      if (!oldUrl && (x.ad.finalUrls || [])[0]) oldUrl = x.ad.finalUrls[0];
      if (hs.indexOf(C.mark) >= 0) { if (x.status === "ENABLED") done = true; } else if (x.status === "ENABLED") olds.push(x.resourceName); }
    var url = C.url ? SITE + C.url : (oldUrl && !/\/florida/i.test(oldUrl) ? oldUrl : SITE + C.fallbackUrl);
    if (!done) {
      var nr = createAd(agrn, C, cfg, url, true);
      if (!nr.isSuccessful()) { L(false, "ad with state insertion: " + g.name + " (retrying without)", nr); nr = createAd(agrn, C, cfg, url, false); }
      L(nr.isSuccessful(), "new 8-state ad: " + g.name + " -> " + url.replace(SITE, ""), nr);
      if (nr.isSuccessful()) olds.forEach(function (o) { var pr = AdsApp.mutate({ adGroupAdOperation: { update: { resourceName: o, status: "PAUSED" }, updateMask: "status" } }); L(pr.isSuccessful(), "  paused old ad in " + g.name, pr); });
    } else Logger.log("Already refreshed: " + g.name);
    if (cfg.kw.length) {
      var have = {}, k = q("SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE ad_group.resource_name = '" + agrn + "' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'");
      while (k.hasNext()) { var kc = k.next().adGroupCriterion; have[kc.keyword.text.toLowerCase() + "|" + kc.keyword.matchType] = true; }
      var add = 0, rej = [];
      cfg.kw.forEach(function (tpl) { NEW_STATES.forEach(function (st) { var t = tpl.replace("%s", st); if (have[t + "|PHRASE"]) return;
        var kr = AdsApp.mutate({ adGroupCriterionOperation: { create: { adGroup: agrn, status: "ENABLED", keyword: { text: t, matchType: "PHRASE" } } } });
        if (kr.isSuccessful()) add++; else rej.push(t); }); });
      Logger.log("  " + g.name + ": state keywords added " + add + (rej.length ? " | rejected: " + rej.join(", ") : ""));
    }
  });

  var haveSL = {}, haveCO = {}, haveSN = {};
  it = q("SELECT campaign_asset.resource_name, campaign_asset.field_type, asset.sitelink_asset.link_text, asset.sitelink_asset.description1, asset.sitelink_asset.description2, asset.callout_asset.callout_text, asset.structured_snippet_asset.header, asset.structured_snippet_asset.values, asset.final_urls FROM campaign_asset WHERE campaign.resource_name = '" + crn + "' AND campaign_asset.status != 'REMOVED'");
  while (it.hasNext()) { var r = it.next(), ca = r.campaignAsset, as = r.asset, ft = ca.fieldType, txt = "";
    if (ft === "SITELINK") { var s = as.sitelinkAsset || {}; txt = [s.linkText, s.description1, s.description2].join(" / ") + " " + ((as.finalUrls || [])[0] || ""); haveSL[(s.linkText || "").toLowerCase()] = true; }
    else if (ft === "CALLOUT") { txt = (as.calloutAsset || {}).calloutText || ""; haveCO[txt.toLowerCase()] = true; }
    else if (ft === "STRUCTURED_SNIPPET") { var sn = as.structuredSnippetAsset || {}; txt = sn.header + ": " + (sn.values || []).join(", "); haveSN[(sn.header || "").toLowerCase()] = true; }
    else txt = "(" + ft + ")";
    Logger.log("Existing campaign asset " + ft + ": " + txt);
    if (/florida/i.test(txt)) { var rr = AdsApp.mutate({ campaignAssetOperation: { remove: ca.resourceName } }); L(rr.isSuccessful(), "  unlinked Florida-only asset: " + txt, rr);
      if (ft === "SITELINK") delete haveSL[((as.sitelinkAsset || {}).linkText || "").toLowerCase()]; if (ft === "CALLOUT") delete haveCO[txt.toLowerCase()]; }
  }
  var n = -1;
  function addAsset(assetBody, field, label) {
    var tmp = "customers/" + cid + "/assets/" + (n--); assetBody.resourceName = tmp;
    var res = AdsApp.mutateAll([{ assetOperation: { create: assetBody } }, { campaignAssetOperation: { create: { campaign: crn, asset: tmp, fieldType: field } } }]);
    var ok = res.every(function (x) { return x.isSuccessful(); });
    Logger.log((ok ? "OK: " : "FAILED: ") + field + " " + label + (ok ? "" : " " + res.map(function (x) { return x.getErrorMessages().join("; "); }).join(" | ")));
  }
  C.sitelinks.forEach(function (s) { if (haveSL[s[0].toLowerCase()]) { Logger.log("Sitelink exists: " + s[0]); return; }
    addAsset({ finalUrls: [SITE + s[1]], sitelinkAsset: { linkText: s[0], description1: s[2], description2: s[3] } }, "SITELINK", s[0]); });
  C.callouts.forEach(function (t) { if (haveCO[t.toLowerCase()]) { Logger.log("Callout exists: " + t); return; }
    addAsset({ calloutAsset: { calloutText: t } }, "CALLOUT", t); });
  C.snippets.forEach(function (s) { if (haveSN[s[0].toLowerCase()]) { Logger.log("Snippet header exists: " + s[0]); return; }
    addAsset({ structuredSnippetAsset: { header: s[0], values: s[1] } }, "STRUCTURED_SNIPPET", s[0]); });
}

function main() {
  var bad = validate(); if (bad.length) { Logger.log("LENGTH ERRORS:\n" + bad.join("\n")); return; }
  var cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, "");
  CAMPAIGNS.forEach(function (C) { runCampaign(C, cid); });
  Logger.log("DONE");
}
if (typeof module !== "undefined") module.exports = { validate: validate };

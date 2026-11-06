/* VS Ads Update (Oct 27 2026): new "Premium Went Up" ad group + account cleanup.
   Paste into Google Ads -> Tools -> Bulk actions -> Scripts -> (+). Click PREVIEW first and read the log.
   Preview changes nothing. Then RUN. Safe to re-run: anything already done is skipped.

   1. RATE-INCREASE AD GROUP "Premium Increase 2027" in "Individual - OE 2027 FL" (existing group had no ads)
      - Keywords (phrase + exact) for people whose rates went up and want a lower cost.
      - One responsive search ad -> /health-insurance-premium-increase-calculator
        (H1 of that page: "Did Your Health Insurance Go Up?").
      - Skips any keyword already live in another ad group of the campaign (no bidding against yourself).
   2. PAUSE "Spanish" and "Overpaying / No Subsidy" ad groups in the Individual campaign.
   3. BLOCK carrier-name searches in the Individual campaign (campaign negatives, phrase):
      ambetter, sunshine health, costco, vsp, colonial life, unitedhealthcare, united healthcare,
      uhc, florida blue, oscar, aetna, cigna. A negative is skipped if one of your own live keywords contains it.
   4. BID CAPS: Trucker Health - OE 2027 and Small Biz Renewal - 2027 -> Max clicks with an $8 cap.
   5. "medicare" negative conflict: in every campaign where a live keyword contains "medicare",
      the broad "medicare" negative is removed and replaced with "medicare advantage",
      "medicare supplement", "medigap" and "medicare part d". Shared negative lists attached to that campaign get the same swap.
   6. Ad groups with no live ads: listed in the log and paused (they cannot show ads anyway).
   Nothing is deleted except the one conflicting "medicare" negative. */

var SITE = "https://www.vshealthbenefits.com";
var IND = "Individual - OE 2027 FL";
var CAP_CAMPS = { "Trucker Health - OE 2027": 8, "Small Biz Renewal - 2027": 8 };
var PAUSE_GROUPS = ["Spanish", "Overpaying / No Subsidy"];
var NEW_GROUP = "Premium Increase 2027";   // existing group (had keywords, no ads); created if missing
var MARK = "Health Insurance Went Up?";   // headline 1, pinned; also marks the ad as already created

var RI_H = [MARK, "2027 Premium Increase?", "Lower Your 2027 Premium", "Don't Auto-Renew the Increase",
  "Compare FL Plans Free", "Licensed Florida Broker", "See Lower-Cost Options", "Free 2027 Rate Check",
  "Your Renewal Is Not Final", "Enroll by Dec 15 for Jan 1", "Same Price as Buying Direct",
  "Talk to a Licensed Advisor", "Check Your 2027 Subsidy", "HSA & Lower-Premium Plans", "Miami-Based, Serving All FL"];
var RI_D = ["Premium went up for 2027? We compare plans in your area before you auto-renew.",
  "Enter your old and new premium and see if you are overpaying. Free calculator.",
  "Licensed Florida broker. Carriers pay us, not you. Same price as buying direct.",
  "Open enrollment runs Nov 1 to Jan 15. Switch by Dec 15 for Jan 1 coverage."];
var RI_PATH = ["rate-increase", "2027"];
var RI_URL = SITE + "/health-insurance-premium-increase-calculator";
var RI_SUFFIX = "utm_source=google&utm_medium=cpc&utm_campaign=individual-oe-2027&utm_content=premium-went-up";
var RI_K = ["health insurance went up", "my health insurance went up", "health insurance went up 2027",
  "why did my health insurance go up", "health insurance premium increase", "health insurance premium increase 2027",
  "health insurance rates going up", "health insurance cost going up 2027", "health insurance renewal increase",
  "obamacare premium increase 2027", "aca premium increase 2027", "marketplace premium increase",
  "lower health insurance premium", "lower my health insurance cost", "health insurance too expensive",
  "paying too much for health insurance", "cheaper health insurance florida", "affordable health insurance florida",
  "lower cost health insurance florida", "health insurance premiums too high"];

var CARRIER_NEG = ["ambetter", "sunshine health", "costco", "vsp", "colonial life", "unitedhealthcare", "united healthcare",
  "uhc", "florida blue", "oscar", "aetna", "cigna"];
var MEDICARE_REPLACE = ["medicare advantage", "medicare supplement", "medigap", "medicare part d"];

var CHANGES = 0, FAILS = 0;
function q(s) { return AdsApp.search(s); }
function esc(s) { return String(s).replace(/'/g, "\\'"); }
function L(ok, msg, r) {
  if (ok) CHANGES++; else FAILS++;
  Logger.log((ok ? "OK: " : "FAILED: ") + msg + (ok || !r ? "" : " -> " + r.getErrorMessages().slice(0, 3).join("; ")));
}
function campaign(name) {
  var it = q("SELECT campaign.resource_name, campaign.status, campaign.bidding_strategy_type FROM campaign WHERE campaign.name = '" + esc(name) + "' AND campaign.status != 'REMOVED'");
  return it.hasNext() ? it.next().campaign : null;
}

function main() {
  var ind = campaign(IND);
  if (!ind) { Logger.log("MISSING campaign " + IND + " - stopping."); return; }
  var cid = ind.resourceName.split("/")[1];

  // ---------- 2. pause Spanish + duplicate group (runs first so step 1 can reuse their keywords) ----------
  Logger.log("== 2. Pause ad groups");
  var groups = {}, it = q("SELECT ad_group.resource_name, ad_group.name, ad_group.status FROM ad_group WHERE campaign.resource_name = '" + ind.resourceName + "' AND ad_group.status != 'REMOVED'");
  while (it.hasNext()) { var g = it.next().adGroup; groups[g.name] = g; }
  PAUSE_GROUPS.forEach(function (n) {
    var g = groups[n];
    if (!g) { Logger.log("Not found (fine): " + n); return; }
    if (g.status === "PAUSED") { Logger.log("Already paused: " + n); return; }
    var r = AdsApp.mutate({ adGroupOperation: { update: { resourceName: g.resourceName, status: "PAUSED" }, updateMask: "status" } });
    L(r.isSuccessful(), "paused ad group \"" + n + "\"", r);
    if (r.isSuccessful()) g.status = "PAUSED";
  });

  // ---------- 1. new ad group ----------
  Logger.log("== 1. New ad group: " + NEW_GROUP);
  var live = {};   // keywords live in OTHER enabled groups of this campaign
  it = q("SELECT ad_group.name, ad_group_criterion.keyword.text FROM ad_group_criterion WHERE campaign.resource_name = '" + ind.resourceName + "' AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.negative = FALSE");
  while (it.hasNext()) { var row = it.next(); if (row.adGroup.name !== NEW_GROUP) live[row.adGroupCriterion.keyword.text.toLowerCase()] = row.adGroup.name; }
  var kws = RI_K.filter(function (k) { if (live[k]) { Logger.log("  skip keyword (already live in \"" + live[k] + "\"): " + k); return false; } return true; });

  var agrn, existing = groups[NEW_GROUP];
  if (!existing) {
    var tmp = "customers/" + cid + "/adGroups/-1";
    var ops = [{ adGroupOperation: { create: { resourceName: tmp, name: NEW_GROUP, campaign: ind.resourceName, status: "ENABLED", type: "SEARCH_STANDARD" } } }];
    kws.forEach(function (k) { ["PHRASE", "EXACT"].forEach(function (mt) { ops.push({ adGroupCriterionOperation: { create: { adGroup: tmp, status: "ENABLED", keyword: { text: k, matchType: mt } } } }); }); });
    ops.push({ adGroupAdOperation: { create: { adGroup: tmp, status: "ENABLED", ad: { finalUrls: [RI_URL], finalUrlSuffix: RI_SUFFIX, responsiveSearchAd: {
      headlines: RI_H.map(function (t, i) { var o = { text: t }; if (i === 0) o.pinnedField = "HEADLINE_1"; return o; }),
      descriptions: RI_D.map(function (t) { return { text: t }; }), path1: RI_PATH[0], path2: RI_PATH[1] } } } } });
    var res = AdsApp.mutateAll(ops, { partialFailure: true });
    var okK = 0, bad = [];
    res.forEach(function (r, i) {
      var op = ops[i];
      if (op.adGroupOperation) L(r.isSuccessful(), "created ad group \"" + NEW_GROUP + "\"", r);
      else if (op.adGroupAdOperation) L(r.isSuccessful(), "created ad -> " + RI_URL, r);
      else if (r.isSuccessful()) okK++; else bad.push(op.adGroupCriterionOperation.create.keyword.text + " [" + op.adGroupCriterionOperation.create.keyword.matchType + "] " + r.getErrorMessages().join("; "));
    });
    Logger.log("  keywords added: " + okK + "/" + (ops.length - 2) + (bad.length ? " | rejected: " + bad.join(" | ") : ""));
    CHANGES += okK;
  } else {
    agrn = existing.resourceName;
    Logger.log("Ad group exists (" + existing.status + "), topping up");
    if (existing.status !== "ENABLED") { var re = AdsApp.mutate({ adGroupOperation: { update: { resourceName: agrn, status: "ENABLED" }, updateMask: "status" } }); L(re.isSuccessful(), "re-enabled " + NEW_GROUP, re); }
    var hasAd = false, a = q("SELECT ad_group_ad.ad.responsive_search_ad.headlines FROM ad_group_ad WHERE ad_group.resource_name = '" + agrn + "' AND ad_group_ad.status = 'ENABLED'");
    while (a.hasNext()) { var hs = ((a.next().adGroupAd.ad.responsiveSearchAd || {}).headlines || []).map(function (h) { return h.text; }); if (hs.indexOf(MARK) >= 0) hasAd = true; }
    if (!hasAd) {
      var ar = AdsApp.mutate({ adGroupAdOperation: { create: { adGroup: agrn, status: "ENABLED", ad: { finalUrls: [RI_URL], finalUrlSuffix: RI_SUFFIX, responsiveSearchAd: {
        headlines: RI_H.map(function (t, i) { var o = { text: t }; if (i === 0) o.pinnedField = "HEADLINE_1"; return o; }),
        descriptions: RI_D.map(function (t) { return { text: t }; }), path1: RI_PATH[0], path2: RI_PATH[1] } } } } });
      L(ar.isSuccessful(), "created ad", ar);
    } else Logger.log("  ad already there");
    var have = {}, kk = q("SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE ad_group.resource_name = '" + agrn + "' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED'");
    while (kk.hasNext()) { var kw = kk.next().adGroupCriterion.keyword; have[kw.text.toLowerCase() + "|" + kw.matchType] = 1; }
    var add = 0; kws.forEach(function (k) { ["PHRASE", "EXACT"].forEach(function (mt) { if (have[k + "|" + mt]) return;
      var kr = AdsApp.mutate({ adGroupCriterionOperation: { create: { adGroup: agrn, status: "ENABLED", keyword: { text: k, matchType: mt } } } });
      if (kr.isSuccessful()) add++; else Logger.log("  rejected: " + k + " [" + mt + "] " + kr.getErrorMessages().join("; ")); }); });
    Logger.log("  keywords added: " + add); CHANGES += add;
  }

  // ---------- 3. carrier-name negatives on Individual ----------
  Logger.log("== 3. Carrier-name negatives");
  var ownKw = [];
  it = q("SELECT ad_group_criterion.keyword.text FROM ad_group_criterion WHERE campaign.resource_name = '" + ind.resourceName + "' AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.negative = FALSE");
  while (it.hasNext()) ownKw.push(" " + it.next().adGroupCriterion.keyword.text.toLowerCase() + " ");
  var negHave = {};
  it = q("SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.resource_name = '" + ind.resourceName + "' AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'");
  while (it.hasNext()) negHave[it.next().campaignCriterion.keyword.text.toLowerCase()] = 1;
  CARRIER_NEG.forEach(function (n) {
    if (negHave[n]) { Logger.log("  already blocked: " + n); return; }
    var clash = ownKw.filter(function (k) { return k.indexOf(" " + n + " ") >= 0; });
    if (clash.length) { Logger.log("  SKIPPED \"" + n + "\": your keyword" + clash.join(",") + "contains it"); return; }
    var r = AdsApp.mutate({ campaignCriterionOperation: { create: { campaign: ind.resourceName, negative: true, keyword: { text: n, matchType: "PHRASE" } } } });
    L(r.isSuccessful(), "negative \"" + n + "\"", r);
  });

  // ---------- 4. bid caps ----------
  Logger.log("== 4. Bid caps");
  Object.keys(CAP_CAMPS).forEach(function (name) {
    var c = campaign(name);
    if (!c) { Logger.log("MISSING campaign " + name); return; }
    var cap = CAP_CAMPS[name];
    if (c.biddingStrategyType !== "TARGET_SPEND") {
      Logger.log("  " + name + " uses " + c.biddingStrategyType + ", not Max clicks: switching to Max clicks with $" + cap + " cap");
    }
    var r = AdsApp.mutate({ campaignOperation: { update: { resourceName: c.resourceName, targetSpend: { cpcBidCeilingMicros: cap * 1e6 } }, updateMask: "targetSpend.cpcBidCeilingMicros" } });
    L(r.isSuccessful(), name + ": Max clicks, $" + cap + " max CPC", r);
  });

  // ---------- 5. medicare conflict ----------
  Logger.log("== 5. 'medicare' negative conflict");
  var medCamps = {};
  it = q("SELECT campaign.resource_name, campaign.name, ad_group_criterion.keyword.text FROM ad_group_criterion WHERE campaign.status != 'REMOVED' AND ad_group.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.keyword.text LIKE '%medicare%'");
  while (it.hasNext()) { var mr = it.next(); medCamps[mr.campaign.resourceName] = mr.campaign.name; Logger.log("  live keyword: \"" + mr.adGroupCriterion.keyword.text + "\" in " + mr.campaign.name); }
  Object.keys(medCamps).forEach(function (crn) {
    var negs = {}, hasMed = null, n2 = q("SELECT campaign_criterion.resource_name, campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.resource_name = '" + crn + "' AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'");
    while (n2.hasNext()) { var cc = n2.next().campaignCriterion, t = cc.keyword.text.toLowerCase(); negs[t] = 1; if (t === "medicare") hasMed = cc.resourceName; }
    MEDICARE_REPLACE.forEach(function (t) { if (negs[t]) return;
      var r = AdsApp.mutate({ campaignCriterionOperation: { create: { campaign: crn, negative: true, keyword: { text: t, matchType: "PHRASE" } } } });
      L(r.isSuccessful(), medCamps[crn] + ": negative \"" + t + "\"", r); });
    if (hasMed) { var rr = AdsApp.mutate({ campaignCriterionOperation: { remove: hasMed } }); L(rr.isSuccessful(), medCamps[crn] + ": removed broad negative \"medicare\"", rr); }
    else Logger.log("  " + medCamps[crn] + ": no campaign-level \"medicare\" negative");
    var ag = q("SELECT ad_group_criterion.resource_name, ad_group.name FROM ad_group_criterion WHERE campaign.resource_name = '" + crn + "' AND ad_group_criterion.negative = TRUE AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.keyword.text = 'medicare'");
    while (ag.hasNext()) { var x = ag.next(); var ra = AdsApp.mutate({ adGroupCriterionOperation: { remove: x.adGroupCriterion.resourceName } }); L(ra.isSuccessful(), medCamps[crn] + " / " + x.adGroup.name + ": removed ad-group negative \"medicare\"", ra); }
  });
  var lists = {}, cs = q("SELECT campaign.resource_name, shared_set.resource_name, shared_set.name FROM campaign_shared_set WHERE campaign_shared_set.status = 'ENABLED' AND shared_set.type = 'NEGATIVE_KEYWORDS'");
  while (cs.hasNext()) { var cr = cs.next(); if (medCamps[cr.campaign.resourceName]) lists[cr.sharedSet.resourceName] = cr.sharedSet.name; }
  Object.keys(lists).forEach(function (srn) {
    var have2 = {}, medRn = null, sc = q("SELECT shared_criterion.resource_name, shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.resource_name = '" + srn + "'");
    while (sc.hasNext()) { var c2 = sc.next().sharedCriterion, t2 = (c2.keyword && c2.keyword.text || "").toLowerCase(); have2[t2] = 1; if (t2 === "medicare") medRn = c2.resourceName; }
    if (!medRn) { Logger.log("  list \"" + lists[srn] + "\": no \"medicare\" entry"); return; }
    MEDICARE_REPLACE.forEach(function (t) { if (have2[t]) return;
      var r = AdsApp.mutate({ sharedCriterionOperation: { create: { sharedSet: srn, keyword: { text: t, matchType: "PHRASE" } } } });
      L(r.isSuccessful(), "list \"" + lists[srn] + "\": negative \"" + t + "\"", r); });
    var rr2 = AdsApp.mutate({ sharedCriterionOperation: { remove: medRn } });
    L(rr2.isSuccessful(), "list \"" + lists[srn] + "\": removed broad negative \"medicare\"", rr2);
  });
  if (!Object.keys(lists).length) Logger.log("  no shared negative lists on those campaigns");

  // ---------- 6. ad groups with no live ads ----------
  Logger.log("== 6. Ad groups with no live ads");
  var withAds = {};
  it = q("SELECT ad_group.resource_name FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND campaign.status != 'REMOVED'");
  while (it.hasNext()) withAds[it.next().adGroup.resourceName] = 1;
  var empty = 0;
  it = q("SELECT ad_group.resource_name, ad_group.name, campaign.name FROM ad_group WHERE ad_group.status = 'ENABLED' AND campaign.status IN ('ENABLED','PAUSED')");
  while (it.hasNext()) {
    var e = it.next();
    if (withAds[e.adGroup.resourceName] || e.adGroup.name === NEW_GROUP) continue;
    empty++;
    var rp = AdsApp.mutate({ adGroupOperation: { update: { resourceName: e.adGroup.resourceName, status: "PAUSED" }, updateMask: "status" } });
    L(rp.isSuccessful(), "paused empty ad group \"" + e.adGroup.name + "\" (" + e.campaign.name + ")", rp);
  }
  if (!empty) Logger.log("  none found");

  Logger.log("DONE: " + CHANGES + " changes, " + FAILS + " failed.");
}

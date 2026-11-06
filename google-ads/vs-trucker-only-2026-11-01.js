/* VS Trucker-Only (Nov 1 2026). PREVIEW first, then RUN. Safe to re-run.
   Goal: every ad dollar goes to truck drivers, and every click lands on the trucker quote page.
   1. Pauses "Individual - OE 2027 FL" and "Small Biz Renewal - 2027" (paused, not removed: turn back on any time).
   2. "Trucker Health - OE 2027": budget $35/day (Open Enrollment). Florida-only locations and bidding are NOT changed
      (health insurance ad certification is Florida only; Max clicks with the $15 cap stays until ~15 conversions).
   3. One fresh ad per ad group, written for that group's search (old ads paused only after the new one saves).
   4. New ad group "Company Driver - No Benefits" + more high-intent keywords from Search Console (phrase + exact).
   5. Pauses the weak non-trucker keyword "health insurance going up 2027 self employed" and the fleet group
      "Trucking Company (Group)" (slow group sales; focus on drivers). Spanish group stays paused.
   6. Wrong-intent negatives (jobs, schools, truck/cargo insurance, DOT physical lookups, rideshare, group/employer). */
var SITE = "https://www.vshealthbenefits.com";
var CAMP = "Trucker Health - OE 2027";
var PAUSE_CAMPS = ["Individual - OE 2027 FL", "Small Biz Renewal - 2027"];
var PAUSE_GROUPS = ["Trucking Company (Group)"];
var PAUSE_KW = ["health insurance going up 2027 self employed"];
var BUDGET = 35;
var URL = "/trucking-health-quote";
var MARK = "Quote From the Cab in 2 Min";   // marker headline: group already refreshed by this script

var COMMON_H = [MARK, "Health Insurance for Truckers", "Open Enrollment Is Open Now", "Enroll by Dec 15 for Jan 1",
  "Plans That Work on the Road", "Nationwide PPO Options", "Priced on What You Net", "Licensed Broker. No Fee.",
  "Talk to a Licensed Advisor", "Florida Truck Driver Plans"];
var COMMON_D = ["Florida truck drivers: compare PPO and Marketplace plans with a licensed broker. Free.",
  "Owner-operators and 1099 drivers get tax credits on net income after truck costs.",
  "Open enrollment ends Jan 15. Enroll by Dec 15 for Jan 1 coverage. Quote in 2 minutes.",
  "Carriers pay us, not you. Same price as going direct, with an advisor who knows trucking."];

var GROUPS = {
  "Truck Driver Health Insurance": { p: ["truckers", "2027-quote"],
    h: ["Truck Driver Health Insurance", "Coverage for OTR & Local", "See a Doctor in Any State", "2027 Rates Up? Compare Now", "Pre-Existing Conditions OK"],
    kw: ["trucking health insurance", "truck driver medical insurance", "truck driver health insurance cost", "truck driver health insurance coverage",
         "health insurance for semi truck drivers", "health insurance for truck drivers florida"] },
  "Owner Operator": { p: ["owner-operator", "2027-quote"],
    h: ["Owner Operator Health Plans", "Premiums May Be Deductible", "Tax Credits on Net Income", "Plans for You and Your Family", "Built for Owner Operators"],
    kw: ["owner operator medical insurance", "medical insurance for owner operators", "health insurance for owner operator truck drivers",
         "medical insurance for owner operator truck drivers", "owner operator health insurance cost"] },
  "1099 Driver": { p: ["1099-drivers", "2027-quote"],
    h: ["1099 Driver Health Coverage", "No Employer Plan? Get Covered", "Tax Credits on Net Income", "Self-Employed Driver Plans", "Premiums May Be Deductible"],
    kw: ["health insurance for independent truckers", "health insurance for 1099 truck drivers", "self employed trucker health insurance"] },
  "2027 Rate Increase - Drivers": { p: ["truckers", "2027-rates"],
    h: ["2027 Rate Increase? Shop Now", "Renewal Went Up? Compare Free", "Lower Your 2027 Premium", "Truck Driver Health Insurance", "Don't Auto-Renew. Compare."],
    kw: [] },
  "Company Driver - No Benefits": { p: ["company-driver", "get-covered"], create: true,
    h: ["Company Driver, No Benefits?", "Skip the 90-Day Wait", "Coverage Can Start Next Month", "Covered Between Carriers", "Truck Driver Health Insurance"],
    d0: "Driving for a carrier with no benefits or a long wait? Get covered on your own now.",
    kw: ["company truck driver health insurance", "truck driver no health insurance", "health insurance for company drivers",
         "truck driver waiting period health insurance", "switching trucking companies health insurance"] }
};
var NEG = ["trucking jobs", "cdl jobs", "driver jobs", "owner operator jobs", "truck driving school", "driving school", "lease purchase",
  "semi truck insurance", "truck insurance quote", "tractor trailer insurance", "bobtail insurance", "non trucking liability",
  "progressive", "geico", "ifta", "factoring", "amazon relay", "uber", "lyft", "doordash", "bus driver", "school bus", "forklift",
  "workers compensation", "disability insurance", "accident insurance", "dot physical", "cdl physical", "medical card",
  "small business", "group health", "employees", "medicare", "medicaid", "part b"];

function L(ok, m, r) { Logger.log((ok ? "OK: " : "FAILED: ") + m + (ok || !r ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); }
function q(s) { return AdsApp.search(s); }
function pauseRn(op, rn, what) { var o = {}; o[op] = { update: { resourceName: rn, status: "PAUSED" }, updateMask: "status" }; var r = AdsApp.mutate(o); L(r.isSuccessful(), "paused " + what, r); return r.isSuccessful(); }

function validate() {
  var bad = [];
  Object.keys(GROUPS).forEach(function (g) { var cfg = GROUPS[g], h = COMMON_H.concat(cfg.h);
    if (h.length > 15) bad.push(g + ": " + h.length + " headlines (max 15)");
    var seen = {}; h.forEach(function (x) { if (x.length > 30) bad.push("H " + x + " (" + x.length + ")"); if (seen[x.toLowerCase()]) bad.push("dup H in " + g + ": " + x); seen[x.toLowerCase()] = 1; });
    cfg.p.forEach(function (x) { if (x.length > 15) bad.push("P " + x); });
    if (cfg.d0 && cfg.d0.length > 90) bad.push("D0 " + g + " (" + cfg.d0.length + ")"); });
  COMMON_D.forEach(function (x) { if (x.length > 90) bad.push("D " + x + " (" + x.length + ")"); });
  return bad;
}

function main() {
  var bad = validate(); if (bad.length) { Logger.log("LENGTH ERRORS:\n" + bad.join("\n")); return; }

  // 1. pause the non-trucker campaigns
  PAUSE_CAMPS.forEach(function (n) { var it = q("SELECT campaign.resource_name, campaign.status FROM campaign WHERE campaign.name = '" + n + "'");
    if (!it.hasNext()) { Logger.log("Not found (ok): " + n); return; } var c = it.next().campaign;
    if (c.status === "PAUSED") Logger.log("Already paused: " + n); else pauseRn("campaignOperation", c.resourceName, "campaign " + n); });

  // 2. trucker campaign budget, keep it ON
  var it = q("SELECT campaign.resource_name, campaign.status, campaign_budget.resource_name FROM campaign WHERE campaign.name = '" + CAMP + "'");
  if (!it.hasNext()) { Logger.log("MISSING campaign " + CAMP); return; }
  var c = it.next(), crn = c.campaign.resourceName;
  var rb = AdsApp.mutate({ campaignBudgetOperation: { update: { resourceName: c.campaignBudget.resourceName, amountMicros: BUDGET * 1e6 }, updateMask: "amountMicros" } }); L(rb.isSuccessful(), "trucker budget $" + BUDGET + "/day", rb);
  if (c.campaign.status !== "ENABLED") { var re = AdsApp.mutate({ campaignOperation: { update: { resourceName: crn, status: "ENABLED" }, updateMask: "status" } }); L(re.isSuccessful(), "trucker campaign ON", re); }

  // 3-5. ad groups
  var groups = {}; it = q("SELECT ad_group.resource_name, ad_group.name, ad_group.status FROM ad_group WHERE campaign.resource_name = '" + crn + "' AND ad_group.status != 'REMOVED'");
  while (it.hasNext()) { var g = it.next().adGroup; groups[g.name] = g; }
  PAUSE_GROUPS.forEach(function (n) { if (groups[n] && groups[n].status === "ENABLED") pauseRn("adGroupOperation", groups[n].resourceName, "ad group " + n); });
  Object.keys(GROUPS).forEach(function (name) {
    var cfg = GROUPS[name];
    if (!groups[name]) {
      if (!cfg.create) { Logger.log("Ad group not found, skipped: " + name); return; }
      var cr = AdsApp.mutate({ adGroupOperation: { create: { campaign: crn, name: name, status: "ENABLED", type: "SEARCH_STANDARD", cpcBidMicros: 10e6 } } });
      L(cr.isSuccessful(), "created ad group " + name, cr); if (!cr.isSuccessful()) return;
      groups[name] = { resourceName: cr.getResourceName(), status: "ENABLED" };
    }
    var agrn = groups[name].resourceName;
    if (groups[name].status === "PAUSED") { var ur = AdsApp.mutate({ adGroupOperation: { update: { resourceName: agrn, status: "ENABLED" }, updateMask: "status" } }); L(ur.isSuccessful(), "ad group ON " + name, ur); }
    var olds = [], done = false;
    var a = q("SELECT ad_group_ad.resource_name, ad_group_ad.ad.responsive_search_ad.headlines FROM ad_group_ad WHERE ad_group.resource_name = '" + agrn + "' AND ad_group_ad.status = 'ENABLED'");
    while (a.hasNext()) { var x = a.next().adGroupAd; var hs = ((x.ad.responsiveSearchAd || {}).headlines || []).map(function (h) { return h.text; });
      if (hs.indexOf(MARK) >= 0) done = true; else olds.push(x.resourceName); }
    if (!done) {
      var H = cfg.h.concat(COMMON_H), D = COMMON_D.slice(); if (cfg.d0) D[1] = cfg.d0;
      var nr = AdsApp.mutate({ adGroupAdOperation: { create: { adGroup: agrn, status: "ENABLED", ad: { finalUrls: [SITE + URL], responsiveSearchAd: {
        headlines: H.map(function (t) { return { text: t }; }), descriptions: D.map(function (t) { return { text: t }; }), path1: cfg.p[0], path2: cfg.p[1] } } } } });
      L(nr.isSuccessful(), "new ad: " + name, nr);
      if (nr.isSuccessful()) olds.forEach(function (o) { pauseRn("adGroupAdOperation", o, "  old ad in " + name); });
    } else Logger.log("Already refreshed: " + name);
    var have = {}, k = q("SELECT ad_group_criterion.resource_name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status FROM ad_group_criterion WHERE ad_group.resource_name = '" + agrn + "' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED'");
    while (k.hasNext()) { var kc = k.next().adGroupCriterion, kt = kc.keyword.text.toLowerCase(); have[kt + "|" + kc.keyword.matchType] = true;
      if (PAUSE_KW.indexOf(kt) >= 0 && kc.status === "ENABLED") pauseRn("adGroupCriterionOperation", kc.resourceName, "keyword " + kt + " [" + kc.keyword.matchType + "]"); }
    var add = 0, rej = [];
    cfg.kw.forEach(function (t) { ["PHRASE", "EXACT"].forEach(function (mt) { if (have[t + "|" + mt]) return;
      var kr = AdsApp.mutate({ adGroupCriterionOperation: { create: { adGroup: agrn, status: "ENABLED", keyword: { text: t, matchType: mt } } } });
      if (kr.isSuccessful()) add++; else rej.push(t + " [" + mt + "]"); }); });
    Logger.log("  " + name + ": keywords added " + add + (rej.length ? " | rejected: " + rej.join(", ") : ""));
  });

  // 6. negatives
  var hn = {}; it = q("SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.resource_name = '" + crn + "' AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'");
  while (it.hasNext()) hn[it.next().campaignCriterion.keyword.text.toLowerCase()] = true;
  var nok = 0, nt = 0, nf = []; NEG.forEach(function (t) { if (hn[t]) return; nt++;
    if (AdsApp.mutate({ campaignCriterionOperation: { create: { campaign: crn, negative: true, keyword: { text: t, matchType: "PHRASE" } } } }).isSuccessful()) nok++; else nf.push(t); });
  Logger.log("Negatives added: " + nok + "/" + nt + (nf.length ? " | failed: " + nf.join(", ") : ""));
  Logger.log("DONE");
}
if (typeof module !== "undefined") module.exports = { validate: validate, GROUPS: GROUPS, COMMON_H: COMMON_H, COMMON_D: COMMON_D, NEG: NEG };

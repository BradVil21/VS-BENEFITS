/* VS Private PPO - Turn On (Nov 5 2026).  PREVIEW first, then RUN.  Safe to re-run.
   1. Checks the High-Income ZIPs campaign: negatives, household income, landing page.
   2. Adds any missing negatives (marketplace, obamacare, subsidy, medicaid, medicare) and income exclusions.
   3. Adds one new pain-led ad per ad group ("Paying Too Much for Insurance?", "Compare Private PPO Options").
   4. Budget $25/day, then turns the ZIP campaign ON. "Private PPO - 8 States (Rest)" stays PAUSED.
   5. Trucker ad strength: the 3 AVERAGE/POOR trucker ads (0 leads) are paused and replaced with new
      15-headline ads, no pinned headlines. The GOOD ads that brought leads are left alone. */
var ZIP = "Private PPO - High-Income ZIPs", REST = "Private PPO - 8 States (Rest)", TRUCK = "Trucker Health - OE 2027";
var BUDGET = 25, LANDING = "/private-health-insurance";
var MUST_NEG = ["marketplace", "obamacare", "subsidy", "medicaid", "medicare"];
var EXCLUDE_INCOME = ["INCOME_RANGE_0_50", "INCOME_RANGE_50_60", "INCOME_RANGE_60_70"];
var COMMON = ["Paying Too Much for Insurance?", "Compare Private PPO Options", "Full-Price Premiums? Compare",
  "Nationwide PPO Networks", "Priced on Health, Not Income", "Pick Your Own Doctors", "Free Licensed Plan Review",
  "No Fee to Use an Advisor", "Apply Any Month of the Year", "5.0-Star Rated on Google", "Get a Quote in 10 Minutes"];
var GROUP_H = {
  "Private Health Insurance": ["Private Health Insurance", "Private Health Insurance Plans", "Private Family Health Plans", "Off-Exchange Health Plans"],
  "PPO Health Insurance": ["PPO Health Insurance", "PPO Health Insurance Plans", "Individual & Family PPO Plans", "National PPO Health Plans"],
  "High Income": ["Health Plans for High Earners", "High Income? Compare PPO Plans", "Too Much Income for Subsidy?", "Insurance for High Income"],
  "Lower My Premium": ["Lower Your Health Premium", "Health Insurance Too Pricey?", "Premiums Too High?", "Alternative to High Premiums"],
  "Self-Employed & 1099 - Price": ["Self-Employed PPO Plans", "1099 Health Insurance Options", "Self-Employed Health Plans", "1099 Private PPO Coverage"]
};
var DESC = ["Paying too much for health insurance? Compare private PPO plans with nationwide networks.",
  "Make too much for a subsidy? Private plans are priced on age and health, not your income.",
  "Self-employed, 1099 or a high-income family? A licensed advisor compares plans for free.",
  "Health questions apply. Apply any month and pick your start date. No fee to use us."];
var MARK = "Compare Private PPO Options";
var TFIX = [
 { id: "830323950922", g: "Truck Driver Health Insurance", p1: "truckers", p2: "health-plans",
   h: ["Truck Driver Health Insurance", "Health Insurance for Truckers", "Trucking Health Insurance", "CDL Driver Health Insurance",
       "OTR Driver Health Insurance", "Medical Insurance for Truckers", "Trucker Health Plans for 2027", "Premiums May Be Tax Deductible",
       "Coverage That Rides With You", "Free Quote in 2 Minutes", "Enroll by Dec 15 for Jan 1", "Licensed Broker, No Fee",
       "Compare PPO & Marketplace", "HSA-Eligible Plans Available", "Call a Licensed Advisor"],
   d: ["Truck driver health insurance that travels with you. Compare PPO and Marketplace plans.",
       "OTR, regional or local: a licensed broker compares trucker health plans for free.",
       "Premiums may be deductible and tax credits use net income after truck costs.",
       "Enroll by Dec 15 for Jan 1 coverage. Get a free quote from the cab in about 2 minutes."] },
 { id: "830406582404", g: "Owner Operator", p1: "owner-operator", p2: "health-plans",
   h: ["Owner Operator Health Plans", "Owner Operator Medical Plans", "Health Insurance for Owner Ops", "Owner Operator Health Coverage",
       "Lease Operator Health Plans", "Best Plans for Owner Operators", "Premiums May Be Tax Deductible", "Tax Credits on Net Income",
       "Write Off Your Health Premium", "HSA-Eligible Plans Available", "Coverage That Rides With You", "Free Quote in 2 Minutes",
       "Enroll by Dec 15 for Jan 1", "Licensed Broker, No Fee", "Cover Your Spouse & Kids"],
   d: ["Owner operator health insurance that works on the road. Compare plans with a broker, free.",
       "Premiums may be deductible, and tax credits use your net income after truck expenses.",
       "HSA-eligible plans let you save pre-tax for medical bills. We show you how.",
       "Enroll by Dec 15 for Jan 1. Carriers pay us, not you: same price as going direct."] },
 { id: "830323823431", g: "1099 Driver", p1: "1099-drivers", p2: "health-plans",
   h: ["1099 Truck Driver Insurance", "Independent Trucker Insurance", "Self-Employed Trucker Plans", "Health Plans for 1099 Drivers",
       "Independent Driver Health Plan", "Self-Employed Driver Coverage", "No Employer Plan? Get Covered", "Tax Credits on Net Income",
       "Premiums May Be Tax Deductible", "HSA-Eligible Plans Available", "Coverage That Rides With You", "Free Quote in 2 Minutes",
       "Enroll by Dec 15 for Jan 1", "Licensed Broker, No Fee", "Cover Your Spouse & Kids"],
   d: ["1099 and independent truck drivers: compare PPO and Marketplace health plans for free.",
       "No employer plan? Tax credits use net income after truck costs. We check yours free.",
       "Coverage for you, your spouse and kids, with doctor networks that work on the road.",
       "Enroll by Dec 15 for Jan 1. Licensed broker. Carriers pay us, not you. Quote in 2 min."] }
];


function q(s) { var o = [], it = AdsApp.search(s); while (it.hasNext()) o.push(it.next()); return o; }
function L(m) { Logger.log(m); }
function mut(op, label) { var r = AdsApp.mutate(op); L((r.isSuccessful() ? "OK: " : "FAILED: ") + label + (r.isSuccessful() ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); return r.isSuccessful(); }
function esc(s) { return s.replace(/'/g, "\\'"); }

function main() {
  var preview = AdsApp.getExecutionInfo().isPreview();
  L(preview ? "PREVIEW (nothing is saved)" : "RUN");
  // ---- copy checks
  var bad = [];
  Object.keys(GROUP_H).forEach(function (g) { var h = GROUP_H[g].concat(COMMON), seen = {};
    if (h.length !== 15) bad.push(g + ": " + h.length + " headlines");
    h.forEach(function (x) { if (x.length > 30) bad.push(x + " (" + x.length + ")"); if (seen[x.toLowerCase()]) bad.push("dup " + x); seen[x.toLowerCase()] = 1; }); });
  TFIX.forEach(function (f) { var seen = {}; if (f.h.length !== 15 || f.d.length !== 4) bad.push(f.g + " count"); f.h.forEach(function (x) { if (x.length > 30) bad.push(x + " (" + x.length + ")"); if (seen[x.toLowerCase()]) bad.push("dup " + x); seen[x.toLowerCase()] = 1; }); f.d.forEach(function (x) { if (x.length > 90) bad.push(x + " (" + x.length + ")"); }); if (f.p1.length > 15 || f.p2.length > 15) bad.push(f.g + " path"); });
  DESC.forEach(function (x) { if (x.length > 90) bad.push(x + " (" + x.length + ")"); });
  if (bad.length) { L("COPY CHECK FAILED, nothing changed:\n" + bad.join("\n")); return; }

  var camp = q("SELECT campaign.resource_name, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign_budget.resource_name, campaign_budget.amount_micros, campaign_budget.explicitly_shared FROM campaign WHERE campaign.name IN ('" + esc(ZIP) + "', '" + esc(REST) + "') AND campaign.status != 'REMOVED'");
  var byName = {}; camp.forEach(function (r) { byName[r.campaign.name] = r; L("CAMPAIGN " + r.campaign.name + " | " + r.campaign.status + " | $" + (r.campaignBudget.amountMicros / 1e6) + "/day | " + r.campaign.biddingStrategyType); });
  var z = byName[ZIP]; if (!z) { L("MISSING campaign " + ZIP); return; }
  var C = "campaign.name = '" + esc(ZIP) + "'";

  // ---- negatives: shared lists + campaign negatives
  var negs = {};
  var sets = q("SELECT shared_set.resource_name, shared_set.name FROM campaign_shared_set WHERE " + C + " AND campaign_shared_set.status = 'ENABLED' AND shared_set.type = 'NEGATIVE_KEYWORDS'");
  sets.forEach(function (s) { L("Shared negative list attached: " + s.sharedSet.name);
    q("SELECT shared_criterion.keyword.text FROM shared_criterion WHERE shared_set.resource_name = '" + s.sharedSet.resourceName + "'").forEach(function (r) { if (r.sharedCriterion.keyword) negs[r.sharedCriterion.keyword.text.toLowerCase()] = 1; }); });
  q("SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE " + C + " AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE AND campaign_criterion.status != 'REMOVED'").forEach(function (r) { negs[r.campaignCriterion.keyword.text.toLowerCase()] = 1; });
  L("Negatives on campaign (shared + own): " + Object.keys(negs).length);
  MUST_NEG.forEach(function (w) {
    if (negs[w]) { L("  negative present: " + w); return; }
    mut({ campaignCriterionOperation: { create: { campaign: z.campaign.resourceName, negative: true, keyword: { text: w, matchType: "PHRASE" } } } }, "added negative " + w);
  });
  // also: no positive keyword may contain a must-negative word
  q("SELECT ad_group.name, ad_group_criterion.keyword.text FROM ad_group_criterion WHERE " + C + " AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED'").forEach(function (r) {
    var t = r.adGroupCriterion.keyword.text.toLowerCase(); MUST_NEG.forEach(function (w) { if (t.indexOf(w) >= 0) L("  WARNING keyword conflicts with negative: " + t); }); });

  // ---- household income (Search campaigns: set on each ad group)
  [ZIP, REST].forEach(function (cn) {
    var have = {};
    q("SELECT ad_group.resource_name, ad_group_criterion.income_range.type FROM ad_group_criterion WHERE campaign.name = '" + esc(cn) + "' AND ad_group_criterion.type = 'INCOME_RANGE' AND ad_group_criterion.negative = TRUE AND ad_group_criterion.status != 'REMOVED'").forEach(function (r) { have[r.adGroup.resourceName + "|" + r.adGroupCriterion.incomeRange.type] = 1; });
    var n = 0, done = 0;
    q("SELECT ad_group.resource_name, ad_group.name FROM ad_group WHERE campaign.name = '" + esc(cn) + "' AND ad_group.status != 'REMOVED'").forEach(function (g) {
      EXCLUDE_INCOME.forEach(function (t) { if (have[g.adGroup.resourceName + "|" + t]) { done++; return; }
        if (mut({ adGroupCriterionOperation: { create: { adGroup: g.adGroup.resourceName, negative: true, incomeRange: { type: t } } } }, cn + " > " + g.adGroup.name + ": exclude " + t)) n++; }); });
    L("Income exclusions " + cn + ": " + done + " already there, " + n + " added (lower 70% excluded; top 30% + unknown kept)");
  });
  var locs = q("SELECT campaign_criterion.criterion_id FROM campaign_criterion WHERE " + C + " AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.negative = FALSE AND campaign_criterion.status != 'REMOVED'").length;
  L("ZIP/location targets: " + locs);

  // ---- ads
  var ads = q("SELECT ad_group.resource_name, ad_group.name, ad_group.status, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad_strength, ad_group_ad.ad.final_urls, ad_group_ad.ad.final_url_suffix, ad_group_ad.ad.responsive_search_ad.path1, ad_group_ad.ad.responsive_search_ad.path2, ad_group_ad.ad.responsive_search_ad.headlines FROM ad_group_ad WHERE " + C + " AND ad_group_ad.status != 'REMOVED' AND ad_group.status != 'REMOVED'");
  var groups = {};
  ads.forEach(function (r) { var a = r.adGroupAd, ad = a.ad, rsa = ad.responsiveSearchAd || {}, url = (ad.finalUrls || [])[0] || "";
    L("AD " + r.adGroup.name + " | " + a.status + " | strength " + a.adStrength + " | " + url + (url.indexOf(LANDING) < 0 ? "  <-- NOT the private page" : ""));
    var g = groups[r.adGroup.name] = groups[r.adGroup.name] || { rn: r.adGroup.resourceName, has: false, url: url, sfx: ad.finalUrlSuffix || "", p1: rsa.path1 || "", p2: rsa.path2 || "" };
    if ((rsa.headlines || []).some(function (h) { return h.text === MARK; })) g.has = true; });
  Object.keys(groups).forEach(function (n) { var g = groups[n];
    if (!GROUP_H[n]) { L("  (no new copy for group " + n + ")"); return; }
    if (g.has) { L("  new pain-led ad already in " + n); return; }
    var url = g.url.indexOf(LANDING) >= 0 ? g.url : "https://www.vshealthbenefits.com" + LANDING;
    var ad = { finalUrls: [url], responsiveSearchAd: { headlines: GROUP_H[n].concat(COMMON).map(function (t) { return { text: t }; }), descriptions: DESC.map(function (t) { return { text: t }; }), path1: g.p1 || "private-ppo", path2: g.p2 || "compare" } };
    if (g.sfx) ad.finalUrlSuffix = g.sfx;
    mut({ adGroupAdOperation: { create: { adGroup: g.rn, status: "ENABLED", ad: ad } } }, "new ad in " + n + " -> " + url);
  });

  // ---- budget + status
  if (z.campaignBudget.explicitlyShared) L("Budget is shared; not changing it.");
  else if (z.campaignBudget.amountMicros !== BUDGET * 1e6) mut({ campaignBudgetOperation: { update: { resourceName: z.campaignBudget.resourceName, amountMicros: BUDGET * 1e6 }, updateMask: "amount_micros" } }, "budget -> $" + BUDGET + "/day");
  if (z.campaign.status !== "ENABLED") mut({ campaignOperation: { update: { resourceName: z.campaign.resourceName, status: "ENABLED" }, updateMask: "status" } }, "turned ON " + ZIP);
  else L(ZIP + " already ON");
  if (byName[REST]) L(REST + " stays " + byName[REST].campaign.status);


  // ---- trucker ad strength: replace AVERAGE / POOR ads (0 leads) with new 15-headline ads, no pins
  TFIX.forEach(function (f) {
    var it = q("SELECT ad_group.resource_name, ad_group_ad.resource_name, ad_group_ad.status, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE ad_group_ad.ad.id = " + f.id);
    if (!it.length) { L("MISSING trucker ad " + f.id); return; }
    var r = it[0];
    if (r.adGroupAd.status !== "ENABLED") { L("Trucker ad " + f.id + " (" + f.g + ") already replaced"); return; }
    var url = (r.adGroupAd.ad.finalUrls || [])[0];
    // pause first (3-ad limit per group), re-enable if the new ad is refused
    if (!mut({ adGroupAdOperation: { update: { resourceName: r.adGroupAd.resourceName, status: "PAUSED" }, updateMask: "status" } }, "paused weak trucker ad " + f.id + " (" + f.g + ")")) return;
    var ok = mut({ adGroupAdOperation: { create: { adGroup: r.adGroup.resourceName, status: "ENABLED", ad: { finalUrls: [url],
      responsiveSearchAd: { headlines: f.h.map(function (t) { return { text: t }; }), descriptions: f.d.map(function (t) { return { text: t }; }), path1: f.p1, path2: f.p2 } } } } }, "new trucker ad in " + f.g);
    if (!ok) mut({ adGroupAdOperation: { update: { resourceName: r.adGroupAd.resourceName, status: "ENABLED" }, updateMask: "status" } }, "re-enabled " + f.id);
  });

  // ---- trucker (read-only report, after changes)
  var T = "campaign.name = '" + esc(TRUCK) + "'";
  q("SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad_strength, ad_group_ad.ad.final_urls, ad_group_ad.ad.final_url_suffix, ad_group_ad.ad.responsive_search_ad.path1, ad_group_ad.ad.responsive_search_ad.path2, ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions, metrics.clicks, metrics.conversions FROM ad_group_ad WHERE " + T + " AND ad_group_ad.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS").forEach(function (r) {
    var a = r.adGroupAd, ad = a.ad, rsa = ad.responsiveSearchAd || {};
    L("TAD|" + JSON.stringify({ g: r.adGroup.name, id: ad.id, st: a.adStrength, url: (ad.finalUrls || [])[0], sfx: ad.finalUrlSuffix, p: [rsa.path1, rsa.path2], clk: r.metrics.clicks, conv: r.metrics.conversions,
      h: (rsa.headlines || []).map(function (x) { return x.text + (x.pinnedField ? " [PIN " + x.pinnedField + "]" : ""); }), d: (rsa.descriptions || []).map(function (x) { return x.text; }) })); });
  var kw = {};
  q("SELECT ad_group.name, ad_group_criterion.keyword.text, metrics.impressions FROM keyword_view WHERE " + T + " AND ad_group_criterion.status = 'ENABLED' AND ad_group.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS ORDER BY metrics.impressions DESC").forEach(function (r) {
    var g = r.adGroup.name; (kw[g] = kw[g] || []).push(r.adGroupCriterion.keyword.text + "(" + r.metrics.impressions + ")"); });
  Object.keys(kw).forEach(function (g) { L("TKW|" + g + "|" + kw[g].slice(0, 25).join("; ")); });
  L("DONE");
}

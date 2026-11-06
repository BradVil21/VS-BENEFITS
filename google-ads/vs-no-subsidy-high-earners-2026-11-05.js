/* VS No Subsidy - High Earners (Nov 5 2026).  PREVIEW first, then RUN.  Safe to re-run.
   For people who make too much for a subsidy and pay full price. Lands on /private-health-insurance.
   1. Renames the 2 campaigns:  Private PPO - High-Income ZIPs -> No Subsidy - High Earners (Top ZIPs)
                                Private PPO - 8 States (Rest)  -> No Subsidy - High Earners (8 States)   (stays paused)
   2. Lets "too much income for a subsidy" searches through: the shared list "VS Leads - Negatives (Nov 3)" blocks every
      search with the word "subsidy", so on these 2 campaigns it is swapped for the same negatives minus the subsidy /
      tax-credit words, and the campaign negatives qualify / eligibility / income limit are removed. Marketplace, obamacare,
      medicaid, medicare, low income, free, cheap... stay blocked. Narrow negatives keep subsidy-seekers out.
   3. New ad group "Don't Qualify for Subsidies" (phrase + exact keywords, lower-70% household income excluded) with an ad
      built for six-figure households paying full price. */
var NAMES = [["Private PPO - High-Income ZIPs", "No Subsidy - High Earners (Top ZIPs)"],
             ["Private PPO - 8 States (Rest)", "No Subsidy - High Earners (8 States)"]];
var SHARED = "VS Leads - Negatives (Nov 3)";
var DROP_NEG = /subsid|tax credit|qualify|eligib|income limit/;
var NEW_NEG = ["subsidy calculator", "apply for subsidy", "how to get a subsidy", "how to get subsidy", "subsidy application",
  "increase my subsidy", "subsidy help", "low income subsidy", "subsidy for low income", "qualify for medicaid", "income limits for medicaid"];
var EXCLUDE_INCOME = ["INCOME_RANGE_0_50", "INCOME_RANGE_50_60", "INCOME_RANGE_60_70"];
var GROUP = "Don't Qualify for Subsidies";
var KW = ["too much income for subsidy", "make too much for subsidy", "make too much money for subsidy", "dont qualify for subsidy",
  "don't qualify for subsidies", "not eligible for subsidy health insurance", "income too high for health insurance subsidy",
  "subsidy cliff health insurance", "over the subsidy cliff", "health insurance without subsidy", "no subsidy health insurance",
  "unsubsidized health insurance", "health insurance full price", "paying full price for health insurance",
  "health insurance over 400 poverty level", "health insurance for high income family", "lost my health insurance subsidy",
  "cheaper health insurance high income", "affordable health insurance for high earners"];
var H = ["Make Too Much for a Subsidy?", "Don't Qualify for a Subsidy?", "Over the Subsidy Cliff?", "No Subsidy? See Lower Options",
  "High Earner? Compare Premiums", "Stop Paying Full Price", "Full-Price Premiums Too High?", "For Six-Figure Households",
  "Priced on Age & Health", "Nationwide Doctor Networks", "Compare Plans Side by Side", "Licensed Advisor, No Fee",
  "Apply Any Month of the Year", "Get Your Price in 10 Minutes", "5.0-Star Rated on Google"];
var D = ["Make too much for a subsidy? Compare plans that can cost less than full-price Marketplace.",
  "Six-figure household paying full price? A licensed advisor compares your options for free.",
  "Healthy applicants may qualify for lower rates. Health questions apply. No obligation.",
  "Nationwide doctor networks. Apply any month and pick your start date. No fee to use us."];
var LANDING = "https://www.vshealthbenefits.com/private-health-insurance";

function q(s) { var o = [], it = AdsApp.search(s); while (it.hasNext()) o.push(it.next()); return o; }
function L(m) { Logger.log(m); }
function mut(op, label) { var r = AdsApp.mutate(op); L((r.isSuccessful() ? "OK: " : "FAILED: ") + label + (r.isSuccessful() ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); return r.isSuccessful() ? (r.getResourceName ? r.getResourceName() : true) : null; }
function esc(s) { return s.replace(/'/g, "\\'"); }

function main() {
  var preview = AdsApp.getExecutionInfo().isPreview();
  L(preview ? "PREVIEW (nothing is saved)" : "RUN");
  var bad = [], seen = {};
  H.forEach(function (x) { if (x.length > 30) bad.push(x + " (" + x.length + ")"); if (seen[x.toLowerCase()]) bad.push("dup " + x); seen[x.toLowerCase()] = 1; });
  D.forEach(function (x) { if (x.length > 90) bad.push(x + " (" + x.length + ")"); });
  KW.forEach(function (k) { if (k.split(" ").length > 10 || k.length > 80) bad.push("kw " + k); });
  if (H.length !== 15 || D.length !== 4) bad.push("counts");
  if (bad.length) { L("COPY CHECK FAILED, nothing changed:\n" + bad.join("\n")); return; }

  // shared negative list contents
  var shared = q("SELECT shared_set.resource_name, shared_set.name FROM shared_set WHERE shared_set.name = '" + esc(SHARED) + "' AND shared_set.status = 'ENABLED'");
  var sharedNegs = [];
  if (shared.length) q("SELECT shared_criterion.keyword.text, shared_criterion.keyword.match_type FROM shared_criterion WHERE shared_set.resource_name = '" + shared[0].sharedSet.resourceName + "'").forEach(function (r) {
    if (r.sharedCriterion.keyword) sharedNegs.push(r.sharedCriterion.keyword); });
  L("Shared list '" + SHARED + "': " + sharedNegs.length + " negatives; keeping " + sharedNegs.filter(function (k) { return !DROP_NEG.test(k.text.toLowerCase()); }).length + " on these campaigns");

  NAMES.forEach(function (pair) {
    var c = q("SELECT campaign.resource_name, campaign.name, campaign.status FROM campaign WHERE campaign.name IN ('" + esc(pair[0]) + "', '" + esc(pair[1]) + "') AND campaign.status != 'REMOVED'");
    if (!c.length) { L("MISSING campaign " + pair[0]); return; }
    var crn = c[0].campaign.resourceName, cname = c[0].campaign.name;
    L("== " + cname + " (" + c[0].campaign.status + ")");
    if (cname !== pair[1]) { if (mut({ campaignOperation: { update: { resourceName: crn, name: pair[1] }, updateMask: "name" } }, "renamed to " + pair[1])) cname = pair[1]; }
    var C = "campaign.resource_name = '" + crn + "'";

    // existing campaign negatives
    var have = {};
    q("SELECT campaign_criterion.resource_name, campaign_criterion.keyword.text FROM campaign_criterion WHERE " + C + " AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE AND campaign_criterion.status != 'REMOVED'").forEach(function (r) {
      var t = r.campaignCriterion.keyword.text.toLowerCase();
      if (DROP_NEG.test(t)) mut({ campaignCriterionOperation: { remove: r.campaignCriterion.resourceName } }, "removed campaign negative '" + t + "'");
      else have[t] = 1; });
    // swap shared list for a copy without the subsidy words
    var att = q("SELECT campaign_shared_set.resource_name, shared_set.name FROM campaign_shared_set WHERE " + C + " AND campaign_shared_set.status = 'ENABLED' AND shared_set.type = 'NEGATIVE_KEYWORDS'");
    var attached = att.filter(function (a) { return a.sharedSet.name === SHARED; });
    var copied = 0;
    sharedNegs.forEach(function (k) { var t = k.text.toLowerCase(); if (DROP_NEG.test(t) || have[t]) return;
      if (mut({ campaignCriterionOperation: { create: { campaign: crn, negative: true, keyword: { text: k.text, matchType: k.matchType } } } }, "neg '" + t + "'")) { have[t] = 1; copied++; } });
    NEW_NEG.forEach(function (t) { if (have[t]) return; if (mut({ campaignCriterionOperation: { create: { campaign: crn, negative: true, keyword: { text: t, matchType: "PHRASE" } } } }, "new neg '" + t + "'")) have[t] = 1; });
    if (attached.length) mut({ campaignSharedSetOperation: { remove: attached[0].campaignSharedSet.resourceName } }, "detached shared list (its words are now campaign negatives, minus subsidy words)");
    ["marketplace", "obamacare", "medicaid", "medicare", "low income"].forEach(function (w) { L("  still blocked '" + w + "': " + (have[w] ? "yes" : "NO")); });

    // ad group
    var g = q("SELECT ad_group.resource_name FROM ad_group WHERE " + C + " AND ad_group.name = \"" + GROUP + "\" AND ad_group.status != 'REMOVED'");
    var grn = g.length ? g[0].adGroup.resourceName : null;
    if (!grn) grn = mut({ adGroupOperation: { create: { campaign: crn, name: GROUP, status: "ENABLED", type: "SEARCH_STANDARD" } } }, "ad group " + GROUP);
    if (!grn || grn === true) { L("  (ad group not created yet; preview cannot add keywords/ad to it. RUN will.)"); return; }
    var kwHave = {};
    q("SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE ad_group.resource_name = '" + grn + "' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED'").forEach(function (r) { kwHave[r.adGroupCriterion.keyword.text + "|" + r.adGroupCriterion.keyword.matchType] = 1; });
    var nk = 0;
    KW.forEach(function (k) { ["PHRASE", "EXACT"].forEach(function (m) { if (kwHave[k + "|" + m]) return;
      if (mut({ adGroupCriterionOperation: { create: { adGroup: grn, status: "ENABLED", keyword: { text: k, matchType: m } } } }, "kw [" + m + "] " + k)) nk++; }); });
    var incHave = {};
    q("SELECT ad_group_criterion.income_range.type FROM ad_group_criterion WHERE ad_group.resource_name = '" + grn + "' AND ad_group_criterion.type = 'INCOME_RANGE' AND ad_group_criterion.negative = TRUE AND ad_group_criterion.status != 'REMOVED'").forEach(function (r) { incHave[r.adGroupCriterion.incomeRange.type] = 1; });
    EXCLUDE_INCOME.forEach(function (t) { if (!incHave[t]) mut({ adGroupCriterionOperation: { create: { adGroup: grn, negative: true, incomeRange: { type: t } } } }, "exclude income " + t); });
    var ads = q("SELECT ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group.resource_name = '" + grn + "' AND ad_group_ad.status != 'REMOVED'");
    if (ads.length) { L("  ad already in group"); return; }
    // reuse the campaign's tracking (utm) from an existing ad's final URL
    var url = LANDING, ex = q("SELECT ad_group_ad.ad.final_urls FROM ad_group_ad WHERE " + C + " AND ad_group_ad.status = 'ENABLED' LIMIT 1");
    if (ex.length) { var u = (ex[0].adGroupAd.ad.finalUrls || [])[0] || ""; if (u.indexOf("/private-health-insurance") >= 0) url = u.replace(/utm_content=[^&]*/, "utm_content=no-subsidy"); }
    mut({ adGroupAdOperation: { create: { adGroup: grn, status: "ENABLED", ad: { finalUrls: [url], responsiveSearchAd: {
      headlines: H.map(function (t) { return { text: t }; }), descriptions: D.map(function (t) { return { text: t }; }), path1: "no-subsidy", path2: "compare" } } } } }, "ad in " + GROUP);
    L("  keywords added: " + nk);
  });
  L("DONE");
}

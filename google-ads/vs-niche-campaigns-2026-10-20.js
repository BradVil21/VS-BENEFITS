/* VS Niche Campaigns (Oct 20 2026) — Trucking hub states, Small Business 2-50 + 1099, Individual no-subsidy.
   Paste into Google Ads → Tools → Bulk actions → Scripts → (+). Click PREVIEW first and read the log.
   Preview validates everything and changes nothing. Then RUN. Safe to re-run: anything already done is skipped.

   What it does
   1. TRUCKING ("Trucker Health - OE 2027", stays PAUSED until you enable it)
      - Locations → FL, TX, IL, GA, TN, KY, OH, IN only (presence), other states removed.
      - New ads in every English ad group → /trucking-health-quote ; old ads paused. Spanish group untouched.
      - New ad group "Trucking Company (Group)" → /trucking-health-quote?type=business
      - Removes the negative "company benefits" so trucking-company searches can show.
   2. SMALL BUSINESS ("Small Biz Renewal - 2027", live)
      - Every ad's final URL → /small-business-health-quote (keeps the ads' history).
      - New ad groups "Businesses With 1099 Workers" and "Group Health 2-50 Employees".
      - Removes the negative "1099" so the 1099 ad group can show.
   3. INDIVIDUAL ("Individual - OE 2027 FL", live)
      - New ad group "Overpaying / No Subsidy" → /quote?type=individual
      - Adds negatives that screen out subsidy / Medicaid seekers.
   4. Prints ad approval status per campaign (shows whether health-insurance certification is limiting ads). */

var SITE = "https://www.vshealthbenefits.com";
var TRUCK = "Trucker Health - OE 2027";
var SMB = "Small Biz Renewal - 2027";
var IND = "Individual - OE 2027 FL";

var TRUCK_STATES = ["Florida", "Texas", "Illinois", "Georgia", "Tennessee", "Kentucky", "Ohio", "Indiana"];
var TRUCK_BUDGET = 35;          // $/day. The campaign stays PAUSED: nothing spends until you enable it.
var TRUCK_ENABLE = false;       // set to true to switch the trucker campaign on in the same run

var TR_H = ["Health Insurance for Truckers", "Owner Operator Health Plans", "Plans That Work on the Road", "Nationwide PPO Options",
  "Free Quote in 2 Minutes", "Licensed Health Advisor", "1099 Driver Health Coverage", "No Cost to Use an Advisor",
  "Open Enrollment Starts Nov 1", "Coverage for Your Family Too", "Compare Top Carriers Free", "Get Covered Before You Roll",
  "Talk to a Licensed Advisor", "Built for OTR Drivers", "Quotes From Your Phone"];
var TR_D = ["Owner-operators and 1099 drivers: compare plans with networks that travel with you.",
  "Answer a few quick questions. A licensed advisor reviews your options, often same day.",
  "Plans are priced by your home ZIP, not where you park. Free quote from your phone.",
  "Many drivers qualify for savings. We check yours free. Carriers pay us, not you."];
var TC_H = ["Trucking Company Health Plans", "Group Health for Your Drivers", "Keep Drivers With Benefits", "Plans for Fleets of 2 to 50+",
  "Free Group Health Quote", "Licensed Health Advisor", "Compare Top Carriers Free", "No Fee to Your Company",
  "Level-Funded & ICHRA Options", "Plans Can Start Any Month", "Talk to a Licensed Advisor", "Benefits That Cut Turnover",
  "Owner-Operator Plans Too", "Quote in Minutes", "Group Plans for Carriers"];
var TC_D = ["Group health for trucking companies. We compare carriers, level-funded and ICHRA, free.",
  "Driver turnover costs more than benefits. Get real numbers for your fleet in minutes.",
  "Plans can start the 1st of any month. Quote first, employee census later. No fee to you.",
  "Licensed advisor who knows trucking: OTR drivers, local fleets, owner-operators."];

var B1099_H = ["Have 1099 Workers?", "Health Options for Contractors", "Benefits for Your Crew", "Group Plans for 2-50 Staff",
  "ICHRA & Group Health Options", "Licensed FL Health Broker", "No Fee to Your Business", "Compare Top Carriers Free",
  "Keep Good Workers Longer", "Plans Start the 1st of Month", "Free Quote, No Obligation", "Talk to a Licensed Advisor",
  "W-2 and 1099 Team Options", "Small Business Health Plans", "Se Habla Español"];
var B1099_D = ["Mix of W-2 staff and 1099 workers? We show what you can legally and affordably offer.",
  "Group health, ICHRA and individual options compared side by side. No fee to your business.",
  "Contractors, trades and crews: get real numbers for your team before you commit.",
  "Licensed Florida broker. Quote in minutes, census later. English y Español."];
var B250_H = ["Small Business Health Plans", "Group Health for 2-50 Staff", "Free Group Health Quotes", "Licensed FL Health Broker",
  "Compare Top Carriers Free", "Level-Funded & ICHRA Options", "Cover Your Employees", "Plans Can Start Any Month",
  "No Fee to Your Business", "Keep Your Team's Doctors", "Quotes for Small Employers", "Florida Group Health Plans",
  "Talk to a Licensed Advisor", "Renewal Up? Get a 2nd Opinion", "Se Habla Español"];
var B250_D = ["Group health for 2-50 employees. We compare carriers, level-funded and ICHRA, free.",
  "Get real numbers for your headcount before you commit. Licensed advisor, no fee to you.",
  "Plans can start the 1st of any month. Quote in minutes, census later. English y Español.",
  "Already have a plan? Send your 2027 renewal and we'll shop it before you sign."];

var OV_H = ["Paying Too Much for Coverage?", "Lower Your Full-Price Premium", "No Subsidy? Compare Plans", "Over the Subsidy Cliff?",
  "Private & Marketplace Plans", "Self-Employed, High Income?", "Licensed FL Health Broker", "Compare Every Carrier Free",
  "HSA Plans for Self-Employed", "Free Quote, No Obligation", "Talk to a Licensed Advisor", "Plans for Ages 50-64",
  "Open Enrollment Starts Nov 1", "Same Price as Buying Direct", "Se Habla Español"];
var OV_D = ["Earn too much for a subsidy? We find your lowest full-price plan, free.",
  "Self-employed? HSA plans and the premium deduction can lower what you really pay.",
  "Licensed Florida broker. Carriers pay us, not you. Same price as buying direct.",
  "Compare Marketplace and private PPO plans side by side before you renew for 2027."];

var NEW_GROUPS = [
  { camp: TRUCK, g: "Trucking Company (Group)", url: "/trucking-health-quote?type=business", p: ["trucking", "group-plans"], h: TC_H, d: TC_D,
    kw: ["group health insurance for trucking companies", "trucking company health insurance", "health insurance for trucking company employees",
         "trucking company employee benefits", "health benefits for truck drivers employer", "fleet health insurance", "small trucking company health insurance"] },
  { camp: SMB, g: "Businesses With 1099 Workers", url: "/small-business-health-quote", p: ["small-business", "1099-crews"], h: B1099_H, d: B1099_D,
    kw: ["health insurance for 1099 employees", "health insurance for 1099 contractors", "can i offer health insurance to 1099 employees",
         "health benefits for independent contractors", "health insurance for contractors employees", "health insurance for my crew",
         "ichra for small business", "health insurance for w2 and 1099 employees"] },
  { camp: SMB, g: "Group Health 2-50 Employees", url: "/small-business-health-quote", p: ["small-business", "2-50-staff"], h: B250_H, d: B250_D,
    kw: ["health insurance for 2 employees", "health insurance for 5 employees", "health insurance for 10 employees", "group health insurance for 20 employees",
         "small group health insurance", "group health insurance for small business", "employee health insurance plans", "health insurance for small company"] },
  { camp: IND, g: "Overpaying / No Subsidy", url: "/quote?type=individual", p: ["health-plans", "full-price"], h: OV_H, d: OV_D,
    kw: ["health insurance too expensive", "lower health insurance premium", "health insurance premiums too high", "paying too much for health insurance",
         "health insurance for high income earners", "best health insurance for self employed florida", "hsa health insurance florida",
         "health insurance cost without subsidy", "cheaper health insurance florida", "health insurance over 1000 a month"] }
];
var TRUCK_NEW_ADS = [   // ad group name → first headline + display path
  { g: "Truck Driver Health Insurance", h1: "Health Insurance for Truckers", p: ["truckers", "quote"] },
  { g: "Owner Operator", h1: "Owner Operator Health Plans", p: ["owner-operator", "quote"] },
  { g: "1099 Driver", h1: "1099 Driver Health Coverage", p: ["1099-drivers", "quote"] },
  { g: "2027 Rate Increase - Drivers", h1: "2027 Rates Up? Compare Now", p: ["truckers", "2027"] }
];
var IND_NEGS = ["medicaid", "food stamps", "low income", "free health insurance", "subsidy calculator", "income limits",
  "qualify for subsidy", "zero premium", "$0 premium", "cheap obamacare", "obamacare calculator"];
var REMOVE_NEGS = {}; REMOVE_NEGS[TRUCK] = ["company benefits"]; REMOVE_NEGS[SMB] = ["1099"];

function log(ok, msg, r) { Logger.log((ok ? "OK: " : "FAILED: ") + msg + (ok || !r ? "" : " — " + r.getErrorMessages().slice(0, 3).join("; "))); }
function q(s) { return s.replace(/'/g, "\\'"); }
function first(h, arr) { var a = arr.slice(); var i = a.indexOf(h); if (i > -1) a.splice(i, 1); a.unshift(h); return a.slice(0, 15); }

function main() {
  // 0. Length checks (Google limits: headline 30, description 90, path 15).
  var bad = [];
  function chk(h, d, p, where) {
    h.forEach(function (x) { if (x.length > 30) bad.push(where + " H " + x); });
    d.forEach(function (x) { if (x.length > 90) bad.push(where + " D " + x); });
    p.forEach(function (x) { if (x.length > 15) bad.push(where + " P " + x); });
  }
  NEW_GROUPS.forEach(function (a) { chk(a.h, a.d, a.p, a.g); });
  TRUCK_NEW_ADS.forEach(function (a) { chk(first(a.h1, TR_H), TR_D, a.p, a.g); });
  if (bad.length) { Logger.log("LENGTH ERRORS — nothing changed:\n" + bad.join("\n")); return; }

  var cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, "");
  var P = "customers/" + cid + "/";
  var camps = {};
  var it = AdsApp.search("SELECT campaign.resource_name, campaign.name, campaign.status, campaign_budget.resource_name FROM campaign WHERE campaign.status != 'REMOVED'");
  while (it.hasNext()) { var r = it.next(); camps[r.campaign.name] = { rn: r.campaign.resourceName, status: r.campaign.status, budget: r.campaignBudget.resourceName }; }
  [TRUCK, SMB, IND].forEach(function (n) { if (!camps[n]) Logger.log("MISSING CAMPAIGN: " + n + " (that part is skipped)"); });
  var groups = {};
  it = AdsApp.search("SELECT campaign.name, ad_group.name, ad_group.resource_name FROM ad_group WHERE ad_group.status != 'REMOVED'");
  while (it.hasNext()) { var g = it.next(); groups[g.campaign.name + "|" + g.adGroup.name] = g.adGroup.resourceName; }

  // 1. TRUCKING: locations, budget, new ads, old ads paused
  var tc = camps[TRUCK];
  if (tc) {
    var geo = {};
    it = AdsApp.search("SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.country_code = 'US' AND geo_target_constant.target_type = 'State'");
    while (it.hasNext()) { var gr = it.next().geoTargetConstant; geo[gr.name] = gr.resourceName; }
    var want = {}; TRUCK_STATES.forEach(function (s) { if (geo[s]) want[geo[s]] = s; else Logger.log("No geo for " + s); });
    var have = {}, ops = [];
    it = AdsApp.search("SELECT campaign_criterion.resource_name, campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.resource_name = '" + tc.rn + "' AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.negative = FALSE");
    while (it.hasNext()) { var cc = it.next().campaignCriterion; have[cc.location.geoTargetConstant] = true; if (!want[cc.location.geoTargetConstant]) ops.push({ campaignCriterionOperation: { remove: cc.resourceName } }); }
    var removed = ops.length;
    Object.keys(want).forEach(function (rn) { if (!have[rn]) ops.push({ campaignCriterionOperation: { create: { campaign: tc.rn, location: { geoTargetConstant: rn } } } }); });
    if (ops.length) { var res = AdsApp.mutateAll(ops, { partialFailure: true }), fails = res.filter(function (x) { return !x.isSuccessful(); });
      log(!fails.length, "Trucker locations → " + TRUCK_STATES.join(", ") + " (removed " + removed + ", added " + (ops.length - removed) + ")", fails[0]); }
    else Logger.log("Trucker locations already set.");
    var br = AdsApp.mutate({ campaignBudgetOperation: { update: { resourceName: tc.budget, amountMicros: TRUCK_BUDGET * 1000000 }, updateMask: "amountMicros" } });
    log(br.isSuccessful(), "Trucker budget $" + TRUCK_BUDGET + "/day", br);

    var ads = [];
    it = AdsApp.search("SELECT ad_group.name, ad_group.resource_name, ad_group_ad.resource_name, ad_group_ad.status, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE campaign.resource_name = '" + tc.rn + "' AND ad_group_ad.status != 'REMOVED' AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD'");
    while (it.hasNext()) { var a = it.next(); ads.push({ g: a.adGroup.name, grn: a.adGroup.resourceName, rn: a.adGroupAd.resourceName, status: a.adGroupAd.status, url: (a.adGroupAd.ad.finalUrls || [])[0] || "" }); }
    TRUCK_NEW_ADS.forEach(function (t) {
      var mine = ads.filter(function (a) { return a.g === t.g; });
      if (!mine.length && !groups[TRUCK + "|" + t.g]) { Logger.log("Trucker ad group not found: " + t.g); return; }
      var grn = groups[TRUCK + "|" + t.g];
      if (mine.some(function (a) { return a.url.indexOf("/trucking-health-quote") > -1; })) { Logger.log("Trucker ad already on landing page: " + t.g); return; }
      var cr = AdsApp.mutate({ adGroupAdOperation: { create: { adGroup: grn, status: "ENABLED", ad: { finalUrls: [SITE + "/trucking-health-quote"],
        responsiveSearchAd: { headlines: first(t.h1, TR_H).map(function (x, i) { var o = { text: x }; if (i === 0) o.pinnedField = "HEADLINE_1"; return o; }),
          descriptions: TR_D.map(function (x) { return { text: x }; }), path1: t.p[0], path2: t.p[1] } } } } });
      log(cr.isSuccessful(), "New trucker ad → landing page: " + t.g, cr);
      if (!cr.isSuccessful()) return;
      mine.filter(function (a) { return a.status === "ENABLED"; }).forEach(function (a) {
        var pr = AdsApp.mutate({ adGroupAdOperation: { update: { resourceName: a.rn, status: "PAUSED" }, updateMask: "status" } });
        log(pr.isSuccessful(), "  paused old ad (" + a.url.replace(SITE, "") + ")", pr);
      });
    });
    if (TRUCK_ENABLE && tc.status !== "ENABLED") {
      var er = AdsApp.mutate({ campaignOperation: { update: { resourceName: tc.rn, status: "ENABLED" }, updateMask: "status" } });
      log(er.isSuccessful(), "Trucker campaign ENABLED", er);
    } else Logger.log("Trucker campaign status left as " + tc.status + (TRUCK_ENABLE ? "" : " (set TRUCK_ENABLE = true to switch it on)"));
  }

  // 2. SMALL BUSINESS: every ad → small business landing page (update in place keeps ad history)
  var sc = camps[SMB];
  if (sc) {
    var n = 0, f = 0;
    it = AdsApp.search("SELECT ad_group.name, ad_group_ad.ad.resource_name, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE campaign.resource_name = '" + sc.rn + "' AND ad_group_ad.status != 'REMOVED'");
    while (it.hasNext()) {
      var s = it.next(), u = (s.adGroupAd.ad.finalUrls || [])[0] || "";
      if (u.indexOf("/small-business-health-quote") > -1) continue;
      var ur = AdsApp.mutate({ adOperation: { update: { resourceName: s.adGroupAd.ad.resourceName, finalUrls: [SITE + "/small-business-health-quote"] }, updateMask: "finalUrls" } });
      if (ur.isSuccessful()) n++; else { f++; log(false, "Small biz ad URL (" + s.adGroup.name + ")", ur); }
    }
    Logger.log("Small biz ads moved to /small-business-health-quote: " + n + (f ? " (" + f + " failed, see above)" : ""));
  }

  // 3. Negatives: remove the ones that would block the new ad groups, add the individual screen-outs
  Object.keys(REMOVE_NEGS).forEach(function (cn) {
    var c = camps[cn]; if (!c) return;
    var it2 = AdsApp.search("SELECT campaign_criterion.resource_name, campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.resource_name = '" + c.rn + "' AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE");
    while (it2.hasNext()) { var k = it2.next().campaignCriterion;
      if (REMOVE_NEGS[cn].indexOf(k.keyword.text.toLowerCase()) > -1) { var rr = AdsApp.mutate({ campaignCriterionOperation: { remove: k.resourceName } }); log(rr.isSuccessful(), cn + ": removed negative \"" + k.keyword.text + "\"", rr); } }
  });
  if (camps[IND]) {
    var existingNeg = {}, it3 = AdsApp.search("SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.resource_name = '" + camps[IND].rn + "' AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE");
    while (it3.hasNext()) existingNeg[it3.next().campaignCriterion.keyword.text.toLowerCase()] = true;
    var nops = IND_NEGS.filter(function (k) { return !existingNeg[k]; }).map(function (k) { return { campaignCriterionOperation: { create: { campaign: camps[IND].rn, negative: true, keyword: { text: k, matchType: "PHRASE" } } } }; });
    if (nops.length) { var nr = AdsApp.mutateAll(nops, { partialFailure: true }), nf = nr.filter(function (x) { return !x.isSuccessful(); }); log(!nf.length, IND + ": added " + (nops.length - nf.length) + " negatives", nf[0]); }
    else Logger.log(IND + ": negatives already there.");
  }

  // 4. New ad groups (keywords phrase + exact, one responsive search ad each)
  var tid = -1;
  NEW_GROUPS.forEach(function (a) {
    var c = camps[a.camp]; if (!c) return;
    if (groups[a.camp + "|" + a.g]) { Logger.log("SKIP (exists): " + a.camp + " / " + a.g); return; }
    var ag = P + "adGroups/" + (tid--), ops2 = [];
    ops2.push({ adGroupOperation: { create: { resourceName: ag, name: a.g, campaign: c.rn, status: "ENABLED", type: "SEARCH_STANDARD" } } });
    a.kw.forEach(function (k) { ["PHRASE", "EXACT"].forEach(function (mt) { ops2.push({ adGroupCriterionOperation: { create: { adGroup: ag, status: "ENABLED", keyword: { text: k, matchType: mt } } } }); }); });
    ops2.push({ adGroupAdOperation: { create: { adGroup: ag, status: "ENABLED", ad: { finalUrls: [SITE + a.url],
      responsiveSearchAd: { headlines: a.h.map(function (x, i) { var o = { text: x }; if (i === 0) o.pinnedField = "HEADLINE_1"; return o; }),
        descriptions: a.d.map(function (x) { return { text: x }; }), path1: a.p[0], path2: a.p[1] } } } } });
    var res2 = AdsApp.mutateAll(ops2, { partialFailure: false }), errs = [];
    res2.forEach(function (x) { if (!x.isSuccessful()) errs = errs.concat(x.getErrorMessages()); });
    Logger.log((errs.length ? "FAILED: " : "OK: ") + a.camp + " / " + a.g + " (" + a.kw.length * 2 + " keywords, 1 ad → " + a.url + ")" + (errs.length ? "\n  " + errs.slice(0, 5).join("\n  ") : ""));
  });

  // 5. Approval status: shows whether health-insurance certification is limiting any campaign
  Logger.log("\nAD APPROVAL STATUS (enabled ads):");
  var st = {};
  it = AdsApp.search("SELECT campaign.name, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED' AND campaign.status != 'REMOVED'");
  while (it.hasNext()) { var p = it.next(), key = p.campaign.name; st[key] = st[key] || {}; var s2 = p.adGroupAd.policySummary.approvalStatus; st[key][s2] = (st[key][s2] || 0) + 1; }
  Object.keys(st).forEach(function (k) { Logger.log("  " + k + ": " + JSON.stringify(st[k])); });
  Logger.log("APPROVED_LIMITED or DISAPPROVED on health ads usually means the state isn't covered by your health-insurance certification.");
}

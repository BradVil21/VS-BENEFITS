/* VS Campaign Update (Oct 19 2026): shift budget to individuals with no subsidy + small business.
   1. Pause "Trucker Health - OE 2027".
   2. Individual: add ad group "No Subsidy / Over Income", raise budget to $25/day.
   3. Small Biz: add broad ad group "Small Business Health Insurance", enable campaign ($25/day).
   Re-runnable: ad groups that already exist are skipped. */
var SITE = "https://www.vshealthbenefits.com";
var NS_H = ["Too Much Income for Subsidy?","No Subsidy? Compare PPO Plans","Over the Subsidy Cliff?","Private Health Plans Florida","Unsubsidized Plans Compared","Nationwide PPO Options","Self-Employed, High Income?","Licensed FL Health Broker","Free Quote, No Obligation","Plans for Ages 50-64","Lower Your Full-Price Premium","Compare Every Carrier Free","Enroll by Dec 15 for Jan 1","Talk to a Licensed Advisor","Se Habla Español"];
var NS_D = ["Earn too much for a subsidy? We compare Marketplace and private PPO plans at full price.","Over 400% of poverty level in 2027? A licensed advisor finds your lowest full-price plan.","Self-employed? HSA plans and the premium deduction can cut your real cost. Free advice.","Local Florida broker, English y Español. Carriers pay us, not you. Same price as direct."];
var NS_K = ["health insurance without subsidy","no subsidy health insurance","too much income for obamacare","make too much for obamacare","health insurance over 400 poverty level","private health insurance florida","ppo health insurance florida","unsubsidized health insurance","health insurance for high income self employed","health insurance for early retirees florida","health insurance before medicare florida"];
var SB_H = ["Small Business Health Plans","Group Health for 2-50 Staff","Free Group Health Quotes","Licensed FL Health Broker","Compare Top Carriers Free","Level-Funded & ICHRA Options","Cover Your Employees","Plans Start Jan 1 or Any Month","No Fee to Your Business","Keep Your Team's Doctors","Quotes for Small Employers","Florida Group Health Plans","Talk to a Licensed Advisor","Renewal Up? Get a 2nd Opinion","Se Habla Español"];
var SB_D = ["Group health for 2-50 employees. We compare carriers, level-funded and ICHRA, free.","Get real numbers for your headcount before you commit. Licensed advisor, no fee to you.","Plans can start the 1st of any month. Quote in minutes, census later. English y Español.","Already have a plan? Send your 2027 renewal and we'll shop it before you sign."];
var SB_K = ["small business health insurance","health insurance for small business","small business health insurance plans","group health insurance","group health insurance plans","small group health insurance","employee health insurance","health insurance for employees","health insurance for my employees","small business health insurance quotes","group health insurance cost"];

var ADD = [
  { camp: "Individual - OE 2027 FL", g: "No Subsidy / Over Income", url: "/quote?type=individual", p: ["coverage", "no-subsidy"], h: NS_H, d: NS_D, kw: NS_K },
  { camp: "Small Biz Renewal - 2027", g: "Small Business Health Insurance", url: "/quote?type=business", p: ["small-business", "quote"], h: SB_H, d: SB_D, kw: SB_K }
];
var STATUS = { "Trucker Health - OE 2027": "PAUSED", "Small Biz Renewal - 2027": "ENABLED", "Individual - OE 2027 FL": "ENABLED" };
var BUDGET = { "Individual - OE 2027 FL": 25, "Small Biz Renewal - 2027": 25 };

function main() {
  var bad = [];
  ADD.forEach(function (a) {
    a.h.forEach(function (x) { if (x.length > 30) bad.push("H " + x); });
    a.d.forEach(function (x) { if (x.length > 90) bad.push("D " + x + " (" + x.length + ")"); });
    a.p.forEach(function (x) { if (x.length > 15) bad.push("P " + x); });
  });
  if (bad.length) { Logger.log("LENGTH ERRORS:\n" + bad.join("\n")); return; }

  var camps = {};
  var it = AdsApp.search("SELECT campaign.resource_name, campaign.name, campaign.status, campaign_budget.resource_name FROM campaign WHERE campaign.status != 'REMOVED'");
  while (it.hasNext()) { var r = it.next(); camps[r.campaign.name] = { rn: r.campaign.resourceName, budget: r.campaignBudget.resourceName, status: r.campaign.status }; }
  var groups = {};
  it = AdsApp.search("SELECT campaign.name, ad_group.name FROM ad_group WHERE ad_group.status != 'REMOVED'");
  while (it.hasNext()) { var g = it.next(); groups[g.campaign.name + "|" + g.adGroup.name] = true; }

  var tid = -1;
  ADD.forEach(function (a) {
    var c = camps[a.camp];
    if (!c) { Logger.log("MISSING campaign " + a.camp); return; }
    if (groups[a.camp + "|" + a.g]) { Logger.log("SKIP (exists): " + a.g); return; }
    var cid = c.rn.split("/")[1];
    var ag = "customers/" + cid + "/adGroups/" + (tid--);
    var ops = [{ adGroupOperation: { create: { resourceName: ag, name: a.g, campaign: c.rn, status: "ENABLED", type: "SEARCH_STANDARD" } } }];
    a.kw.forEach(function (k) { ["PHRASE", "EXACT"].forEach(function (mt) {
      ops.push({ adGroupCriterionOperation: { create: { adGroup: ag, status: "ENABLED", keyword: { text: k, matchType: mt } } } }); }); });
    ops.push({ adGroupAdOperation: { create: { adGroup: ag, status: "ENABLED", ad: { finalUrls: [SITE + a.url],
      responsiveSearchAd: { headlines: a.h.map(function (x) { return { text: x }; }), descriptions: a.d.map(function (x) { return { text: x }; }), path1: a.p[0], path2: a.p[1] } } } } });
    var res = AdsApp.mutateAll(ops, { partialFailure: false }), errs = [];
    res.forEach(function (r) { if (!r.isSuccessful()) errs = errs.concat(r.getErrorMessages()); });
    Logger.log((errs.length ? "FAILED: " : "OK: ") + a.camp + " / " + a.g + " (" + ops.length + " ops)" + (errs.length ? "\n  " + errs.slice(0, 6).join("\n  ") : ""));
  });

  Object.keys(BUDGET).forEach(function (n) {
    var c = camps[n]; if (!c) return;
    var r = AdsApp.mutate({ campaignBudgetOperation: { update: { resourceName: c.budget, amountMicros: BUDGET[n] * 1000000 }, updateMask: "amountMicros" } });
    Logger.log((r.isSuccessful() ? "OK" : "FAILED") + ": budget " + n + " -> $" + BUDGET[n] + "/day" + (r.isSuccessful() ? "" : " " + r.getErrorMessages().join("; ")));
  });
  Object.keys(STATUS).forEach(function (n) {
    var c = camps[n]; if (!c || c.status === STATUS[n]) { if (c) Logger.log("Status already " + STATUS[n] + ": " + n); return; }
    var r = AdsApp.mutate({ campaignOperation: { update: { resourceName: c.rn, status: STATUS[n] }, updateMask: "status" } });
    Logger.log((r.isSuccessful() ? "OK" : "FAILED") + ": " + n + " -> " + STATUS[n] + (r.isSuccessful() ? "" : " " + r.getErrorMessages().join("; ")));
  });
}

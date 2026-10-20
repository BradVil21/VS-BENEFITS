/* VS Master Update (Oct 19 2026, evening) — focus spend on what produced leads.
   1. Trucker OFF. Individual ON $30/day. Small Biz ON $15/day. ACA Calculator ON $10/day.
   2. Adds "No Subsidy / Over Income" + "Small Business Health Insurance" ad groups (skips if they exist).
   3. Creates "ACA Calculator - FL" (skips if it exists).
   4. Blocks carrier-brand / wrong-intent searches on all three live campaigns.
   5. Desktop bids -50% (phones produced every conversion). Individual + Calculator run 7am-9pm.
   6. New Spanish ad for Individual (old "Poor" one paused).
   Safe to re-run. */
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

var ADD = [
  { camp: "Individual - OE 2027 FL", g: "No Subsidy / Over Income", url: "/quote?type=individual", p: ["coverage", "no-subsidy"], h: NS_H, d: NS_D, kw: NS_K },
  { camp: "Small Biz Renewal - 2027", g: "Small Business Health Insurance", url: "/quote?type=business", p: ["small-business", "quote"], h: SB_H, d: SB_D, kw: SB_K }
];
var STATUS = { "Trucker Health - OE 2027": "PAUSED", "Small Biz Renewal - 2027": "ENABLED", "Individual - OE 2027 FL": "ENABLED" };
var BUDGET = { "Individual - OE 2027 FL": 30, "Small Biz Renewal - 2027": 15 };
var LIVE = ["Individual - OE 2027 FL", "Small Biz Renewal - 2027", "ACA Calculator - FL"];
var BRAND_NEG = ["costco","florida blue","blue cross","bcbs","unitedhealthcare","united healthcare","uhc","sunshine health","vsp","medicaid","member login","login","sign in","customer service","phone number","jobs","careers","dental","vision","medicare advantage","humana advantage","free insurance"];
var SCHEDULE_CAMPS = ["Individual - OE 2027 FL", "ACA Calculator - FL"];
var ES_H = ["Seguro M\u00e9dico en Florida","Planes M\u00e9dicos 2027","Agente Licenciado en Florida","Cotizaci\u00f3n Gratis Hoy","Compare Todas las Compa\u00f1\u00edas","\u00bfSubi\u00f3 Su Prima en 2027?","Hablamos Espa\u00f1ol","Ayuda Gratis, Sin Compromiso","Inscripci\u00f3n Abre 1 de Nov","Planes Obamacare y PPO","Calcule Su Subsidio 2027","Agente Local en Miami","Inscr\u00edbase Antes del 15 Dic","Mantenga a Sus Doctores","Hable con un Agente Hoy"];
var ES_D = ["Agente licenciado en Florida. Comparamos todos los planes de 2027 gratis para usted.","\u00bfLe subi\u00f3 el seguro? Revisamos su renovaci\u00f3n 2027 y buscamos un plan que cueste menos.","Planes Obamacare, PPO y para independientes. Cotizaci\u00f3n gratis en minutos.","Sin costo para usted: las aseguradoras nos pagan. Mismo precio que comprar directo."];

function log(ok, msg, r) { Logger.log((ok ? "OK: " : "FAILED: ") + msg + (ok || !r ? "" : " " + r.getErrorMessages().slice(0,3).join("; "))); }
function loadCamps() {
  var camps = {}, it = AdsApp.search("SELECT campaign.resource_name, campaign.name, campaign.status, campaign_budget.resource_name FROM campaign WHERE campaign.status != 'REMOVED'");
  while (it.hasNext()) { var r = it.next(); camps[r.campaign.name] = { rn: r.campaign.resourceName, id: r.campaign.resourceName.split("/").pop(), budget: r.campaignBudget.resourceName, status: r.campaign.status }; }
  return camps;
}

function main() {
  var bad = [];
  ADD.forEach(function (a) { a.h.forEach(function (x) { if (x.length > 30) bad.push("H " + x); }); a.d.forEach(function (x) { if (x.length > 90) bad.push("D " + x); }); a.p.forEach(function (x) { if (x.length > 15) bad.push("P " + x); }); });
  ES_H.forEach(function (x) { if (x.length > 30) bad.push("ES H " + x + " " + x.length); });
  ES_D.forEach(function (x) { if (x.length > 90) bad.push("ES D " + x + " " + x.length); });
  if (bad.length) { Logger.log("LENGTH ERRORS:\n" + bad.join("\n")); return; }

  var camps = loadCamps();
  var cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, "");
  var groups = {}, it = AdsApp.search("SELECT campaign.name, ad_group.name FROM ad_group WHERE ad_group.status != 'REMOVED'");
  while (it.hasNext()) { var g = it.next(); groups[g.campaign.name + "|" + g.adGroup.name] = true; }

  // 1. status + budgets
  Object.keys(STATUS).forEach(function (n) { var c = camps[n]; if (!c) { Logger.log("MISSING " + n); return; }
    if (c.status === STATUS[n]) { Logger.log("Status already " + STATUS[n] + ": " + n); return; }
    var r = AdsApp.mutate({ campaignOperation: { update: { resourceName: c.rn, status: STATUS[n] }, updateMask: "status" } }); log(r.isSuccessful(), n + " -> " + STATUS[n], r); });
  Object.keys(BUDGET).forEach(function (n) { var c = camps[n]; if (!c) return;
    var r = AdsApp.mutate({ campaignBudgetOperation: { update: { resourceName: c.budget, amountMicros: BUDGET[n] * 1000000 }, updateMask: "amountMicros" } }); log(r.isSuccessful(), "budget " + n + " $" + BUDGET[n], r); });

  // 2. ad groups
  var tid = -1;
  ADD.forEach(function (a) { var c = camps[a.camp]; if (!c) return;
    if (groups[a.camp + "|" + a.g]) { Logger.log("SKIP (exists): " + a.g); return; }
    var ag = "customers/" + cid + "/adGroups/" + (tid--);
    var ops = [{ adGroupOperation: { create: { resourceName: ag, name: a.g, campaign: c.rn, status: "ENABLED", type: "SEARCH_STANDARD" } } }];
    a.kw.forEach(function (k) { ["PHRASE", "EXACT"].forEach(function (mt) { ops.push({ adGroupCriterionOperation: { create: { adGroup: ag, status: "ENABLED", keyword: { text: k, matchType: mt } } } }); }); });
    ops.push({ adGroupAdOperation: { create: { adGroup: ag, status: "ENABLED", ad: { finalUrls: [SITE + a.url], responsiveSearchAd: { headlines: a.h.map(function (x) { return { text: x }; }), descriptions: a.d.map(function (x) { return { text: x }; }), path1: a.p[0], path2: a.p[1] } } } } });
    var res = AdsApp.mutateAll(ops, { partialFailure: false }), errs = [];
    res.forEach(function (r) { if (!r.isSuccessful()) errs = errs.concat(r.getErrorMessages()); });
    Logger.log((errs.length ? "FAILED: " : "OK: ") + "ad group " + a.g + (errs.length ? " " + errs.slice(0, 4).join("; ") : "")); });

  // 3. calculator campaign
  buildCalculator();
  camps = loadCamps();

  // 4-5. negatives, devices, schedule
  LIVE.forEach(function (n) { var c = camps[n]; if (!c) { Logger.log("MISSING " + n); return; }
    var have = {}, q = AdsApp.search("SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.resource_name = '" + c.rn + "' AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'");
    while (q.hasNext()) have[q.next().campaignCriterion.keyword.text.toLowerCase()] = true;
    var ops = []; BRAND_NEG.forEach(function (k) { if (!have[k]) ops.push({ campaignCriterionOperation: { create: { campaign: c.rn, negative: true, keyword: { text: k, matchType: "PHRASE" } } } }); });
    if (ops.length) { var ok = 0; AdsApp.mutateAll(ops, { partialFailure: true }).forEach(function (r) { if (r.isSuccessful()) ok++; }); Logger.log("Negatives " + n + ": " + ok + "/" + ops.length + " added"); }
    else Logger.log("Negatives " + n + ": already in place");
    var drn = "customers/" + cid + "/campaignCriteria/" + c.id + "~30000";
    var r = AdsApp.mutate({ campaignCriterionOperation: { update: { resourceName: drn, bidModifier: 0.5 }, updateMask: "bidModifier" } });
    if (!r.isSuccessful()) r = AdsApp.mutate({ campaignCriterionOperation: { create: { campaign: c.rn, device: { type: "DESKTOP" }, bidModifier: 0.5 } } });
    log(r.isSuccessful(), "desktop -50% " + n, r);
    if (SCHEDULE_CAMPS.indexOf(n) >= 0) {
      var s = AdsApp.search("SELECT campaign_criterion.criterion_id FROM campaign_criterion WHERE campaign.resource_name = '" + c.rn + "' AND campaign_criterion.type = 'AD_SCHEDULE'");
      if (s.hasNext()) { Logger.log("Schedule already set: " + n); }
      else { var sops = ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"].map(function (d) { return { campaignCriterionOperation: { create: { campaign: c.rn, adSchedule: { dayOfWeek: d, startHour: 7, startMinute: "ZERO", endHour: 21, endMinute: "ZERO" } } } }; });
        var ok2 = 0; AdsApp.mutateAll(sops, { partialFailure: true }).forEach(function (x) { if (x.isSuccessful()) ok2++; }); Logger.log("Schedule 7am-9pm " + n + ": " + ok2 + "/7"); }
    }
  });

  // 6. Spanish ad refresh
  var ind = camps["Individual - OE 2027 FL"];
  if (ind) {
    var a = AdsApp.search("SELECT ad_group.resource_name, ad_group_ad.resource_name, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines FROM ad_group_ad WHERE campaign.resource_name = '" + ind.rn + "' AND ad_group.name = 'Spanish' AND ad_group_ad.status = 'ENABLED'");
    var olds = [], agrn = null, url = null, already = false;
    while (a.hasNext()) { var x = a.next(); agrn = x.adGroup.resourceName; url = x.adGroupAd.ad.finalUrls[0];
      var hs = (x.adGroupAd.ad.responsiveSearchAd.headlines || []).map(function (h) { return h.text; });
      if (hs.indexOf(ES_H[0]) >= 0 && hs.indexOf(ES_H[14]) >= 0) already = true; else olds.push(x.adGroupAd.resourceName); }
    if (!agrn) Logger.log("No Spanish ad group found");
    else if (already) Logger.log("Spanish ad already refreshed");
    else {
      var nr = AdsApp.mutate({ adGroupAdOperation: { create: { adGroup: agrn, status: "ENABLED", ad: { finalUrls: [url], responsiveSearchAd: { headlines: ES_H.map(function (t) { return { text: t }; }), descriptions: ES_D.map(function (t) { return { text: t }; }), path1: "seguro", path2: "florida" } } } } });
      log(nr.isSuccessful(), "new Spanish ad -> " + url, nr);
      if (nr.isSuccessful()) olds.forEach(function (o) { var pr = AdsApp.mutate({ adGroupAdOperation: { update: { resourceName: o, status: "PAUSED" }, updateMask: "status" } }); log(pr.isSuccessful(), "paused old Spanish ad", pr); });
    }
  }
  Logger.log("DONE");
}

/* ---- ACA Calculator campaign ---- */
var NAME = "ACA Calculator - FL";
var H = ["2027 Subsidy Calculator","See Your 2027 Price in 60 Sec","Free ACA Calculator, Florida","Will You Get a Tax Credit?","Premiums Up? Check Your Price","Obamacare Calculator 2027","Estimate Your 2027 Premium","Free, Takes 60 Seconds","Licensed FL Health Broker","Open Enrollment Starts Nov 1","See Bronze, Silver, Gold Cost","Calculadora de Subsidio","No Cost, No Obligation"];
var D = ["Enter your income and household. See your 2027 tax credit and plan prices in 60 seconds.","Free calculator from a licensed Florida broker. Real plans and prices confirmed free.","2027 premiums are up. See what you'll actually pay before open enrollment starts Nov 1.","No cost, no obligation. English y Español. A licensed advisor can confirm your numbers."];
var K = ["aca subsidy calculator 2027","aca subsidy calculator","obamacare calculator","obamacare subsidy calculator","marketplace subsidy calculator","health insurance tax credit calculator","premium tax credit calculator","how much will obamacare cost 2027","aca premium calculator florida","health insurance cost calculator florida","calculadora de subsidio obamacare"];
var NEG = ["medicaid","low income","login","sign in","phone number","customer service","jobs","salary","paycheck","income tax","mortgage","loan","bmi","medicare","dental","vision","car insurance","auto insurance","life insurance"];

function buildCalculator() {
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
  var kops = []; K.forEach(function (k) { ["PHRASE", "EXACT"].forEach(function (mt) {
    kops.push({ adGroupCriterionOperation: { create: { adGroup: null, status: "ENABLED", keyword: { text: k, matchType: mt } } } }); }); });
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
  var agq = AdsApp.search("SELECT ad_group.resource_name FROM ad_group WHERE campaign.name = '" + NAME + "'");
  var realAg = agq.hasNext() ? agq.next().adGroup.resourceName : null, kok = 0, kbad = [];
  kops.forEach(function (o) { o.adGroupCriterionOperation.create.adGroup = realAg;
    var kr = AdsApp.mutate(o); if (kr.isSuccessful()) kok++; else kbad.push(o.adGroupCriterionOperation.create.keyword.text + " [" + o.adGroupCriterionOperation.create.keyword.matchType + "]"); });
  Logger.log("  keywords added: " + kok + "/" + kops.length + (kbad.length ? " | rejected by Google policy: " + kbad.join(", ") : ""));
  if (real && aops.length) {
    var ar = AdsApp.mutateAll(aops, { partialFailure: true }), ok = 0;
    ar.forEach(function (r) { if (r.isSuccessful()) ok++; });
    Logger.log("  assets linked: " + ok + "/" + aops.length);
  }
}

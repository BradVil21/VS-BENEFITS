/* VS Trucker - Florida only (Oct 20 2026). Safe to re-run.
   1. "Trucker Health - OE 2027": Florida only (every other state removed), $15/day, Max clicks with $6 cap, ON.
   2. One fresh Florida ad per ad group (old ads paused only after the new one saves).
   3. Florida keywords added per ad group; any Google rejects are logged, not fatal.
   4. Company-name / wrong-intent searches blocked, desktop bids -50%. */
var SITE = "https://www.vshealthbenefits.com";
var CAMP = "Trucker Health - OE 2027";
var FL = "geoTargetConstants/21142";
var BUDGET = 15, CPC_CAP = 6;
var MARK = "Florida Trucker Health Plans";   // marker headline: group already refreshed
var MARK_ES = "Camioneros de Florida";

var COMMON_H = [MARK, "Licensed Florida Broker", "Free Quote in 2 Minutes", "Plans That Work on the Road", "Nationwide PPO Options",
  "Miami-Based, Serving All of FL", "2027 Rates Up? Compare Now", "Enroll by Dec 15 for Jan 1", "No Cost to Use an Advisor", "Talk to a Licensed Advisor"];
var COMMON_D = ["Florida truckers: compare PPO and Marketplace plans with a licensed local broker. Free.",
  "Doctors across the country, so your coverage works on the road, not just at home.",
  "2027 premiums are going up. Get your Florida quote in 2 minutes before Dec 15.",
  "Carriers pay us, not you: same price as going direct. No obligation."];

var GROUPS = {
  "Truck Driver Health Insurance": { url: "/trucking-health-quote", p: ["florida", "truckers"],
    h: ["Truck Driver Health Insurance", "FL Truck Driver Health Plans", "OTR & Local Driver Coverage", "See Doctors on the Road"],
    kw: ["truck driver health insurance florida", "trucker health insurance florida", "health insurance for truck drivers in florida", "cdl driver health insurance florida"] },
  "Owner Operator": { url: "/trucking-health-quote", p: ["florida", "owner-operator"],
    h: ["Owner Operator Health Plans", "FL Owner Operators: Save Now", "Premiums May Be Tax Deductible", "Plans for You and Your Family"],
    kw: ["owner operator health insurance florida", "health insurance for owner operators florida"] },
  "1099 Driver": { url: "/trucking-health-quote", p: ["florida", "1099-drivers"],
    h: ["1099 Driver Health Coverage", "Health Plans for 1099 Drivers", "No Employer Plan? We Can Help", "Premiums May Be Tax Deductible"],
    kw: ["1099 truck driver health insurance florida", "independent truck driver health insurance florida"] },
  "2027 Rate Increase - Drivers": { url: "/trucking-health-quote", p: ["florida", "2027-rates"],
    h: ["2027 Rate Increase? Shop Now", "Renewal Went Up? Compare Free", "Lower Your 2027 Premium", "Truck Driver Health Insurance"],
    kw: [] },
  "Trucking Company (Group)": { url: "/trucking-health-quote?type=business", p: ["florida", "fleets"],
    h: ["Group Health for FL Fleets", "Trucking Company Benefits", "Plans for 2-50 Drivers", "Retain Drivers With Benefits"],
    d0: "Florida trucking companies: group health for 2-50 drivers. Free quotes, licensed broker.",
    kw: ["trucking company health insurance florida", "group health insurance trucking company florida", "trucking company employee benefits florida"] }
};
var ES_H = ["Seguro para Camioneros FL", MARK_ES, "Seguro Médico para Choferes", "Planes PPO en Todo el País", "Agente Licenciado en Florida",
  "Cotización Gratis en 2 Min", "Hablamos Español", "¿Subió Su Seguro en 2027?", "Inscríbase Antes del 15 Dic", "Sin Costo Usar un Agente",
  "Dueños Operadores y 1099", "Cobertura en la Carretera", "Planes para Su Familia", "Agente Local en Miami", "Hable con un Agente Hoy"];
var ES_D = ["Camioneros de Florida: comparamos planes PPO y de Obamacare gratis. Agente licenciado.",
  "Médicos en todo el país para que su seguro funcione en la carretera, no solo en casa.",
  "Las primas de 2027 suben. Cotice en 2 minutos antes del 15 de diciembre.",
  "Las aseguradoras nos pagan a nosotros: usted paga lo mismo que comprando directo."];
var ES_KW = ["seguro medico para camioneros", "seguro de salud para camioneros florida"];
var NEG = ["costco", "florida blue", "blue cross", "bcbs", "unitedhealthcare", "united healthcare", "medicaid", "login", "sign in",
  "customer service", "phone number", "jobs", "careers", "hiring", "cdl school", "truck insurance", "commercial auto", "cargo insurance", "dental", "vision"];

function L(ok, m, r) { Logger.log((ok ? "OK: " : "FAILED: ") + m + (ok || !r ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); }
function q(s) { return AdsApp.search(s); }

function main() {
  var bad = [];
  Object.keys(GROUPS).forEach(function (g) { var h = COMMON_H.concat(GROUPS[g].h); if (h.length > 15) bad.push(g + " >15 headlines");
    h.forEach(function (x) { if (x.length > 30) bad.push("H " + x + " " + x.length); });
    GROUPS[g].p.forEach(function (x) { if (x.length > 15) bad.push("P " + x); }); if (GROUPS[g].d0 && GROUPS[g].d0.length > 90) bad.push("D0 " + g); });
  COMMON_D.concat(ES_D).forEach(function (x) { if (x.length > 90) bad.push("D " + x + " " + x.length); });
  ES_H.forEach(function (x) { if (x.length > 30) bad.push("ES H " + x + " " + x.length); });
  if (bad.length) { Logger.log("LENGTH ERRORS:\n" + bad.join("\n")); return; }

  var it = q("SELECT campaign.resource_name, campaign.status, campaign_budget.resource_name FROM campaign WHERE campaign.name = '" + CAMP + "'");
  if (!it.hasNext()) { Logger.log("MISSING campaign " + CAMP); return; }
  var c = it.next(), crn = c.campaign.resourceName, cid = crn.split("/")[1], campId = crn.split("/").pop();

  // 1. Florida only
  var locs = [], hasFl = false; it = q("SELECT campaign_criterion.resource_name, campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.resource_name = '" + crn + "' AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.negative = FALSE");
  while (it.hasNext()) { var cc = it.next().campaignCriterion; if (cc.location.geoTargetConstant === FL) hasFl = true; else locs.push(cc.resourceName); }
  if (!hasFl) { var r0 = AdsApp.mutate({ campaignCriterionOperation: { create: { campaign: crn, location: { geoTargetConstant: FL } } } }); L(r0.isSuccessful(), "added Florida", r0); }
  locs.forEach(function (rn) { var r = AdsApp.mutate({ campaignCriterionOperation: { remove: rn } }); L(r.isSuccessful(), "removed location " + rn.split("~").pop(), r); });
  Logger.log("Locations: Florida only (" + locs.length + " other removed)");

  var rb = AdsApp.mutate({ campaignBudgetOperation: { update: { resourceName: c.campaignBudget.resourceName, amountMicros: BUDGET * 1e6 }, updateMask: "amountMicros" } }); L(rb.isSuccessful(), "budget $" + BUDGET + "/day", rb);
  var rs = AdsApp.mutate({ campaignOperation: { update: { resourceName: crn, targetSpend: { cpcBidCeilingMicros: CPC_CAP * 1e6 } }, updateMask: "targetSpend.cpcBidCeilingMicros" } }); L(rs.isSuccessful(), "bidding Max clicks, $" + CPC_CAP + " cap", rs);
  if (c.campaign.status !== "ENABLED") { var re = AdsApp.mutate({ campaignOperation: { update: { resourceName: crn, status: "ENABLED" }, updateMask: "status" } }); L(re.isSuccessful(), "campaign ON", re); } else Logger.log("Campaign already ON");

  // 2-3. ads + keywords per ad group
  var groups = {}; it = q("SELECT ad_group.resource_name, ad_group.name FROM ad_group WHERE campaign.resource_name = '" + crn + "' AND ad_group.status != 'REMOVED'");
  while (it.hasNext()) { var g = it.next().adGroup; groups[g.name] = g.resourceName; }
  Object.keys(groups).forEach(function (name) {
    var agrn = groups[name], spanish = /spanish|espa/i.test(name), cfg = GROUPS[name];
    if (spanish) { Logger.log("Skipped Spanish group (English only, Oct 20): " + name); return; }
    if (!cfg && !spanish) { Logger.log("Left as is (no Florida copy defined): " + name); return; }
    var olds = [], done = false, oldUrl = null;
    var a = q("SELECT ad_group_ad.resource_name, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines FROM ad_group_ad WHERE ad_group.resource_name = '" + agrn + "' AND ad_group_ad.status = 'ENABLED'");
    while (a.hasNext()) { var x = a.next().adGroupAd; oldUrl = oldUrl || (x.ad.finalUrls || [])[0];
      var hs = ((x.ad.responsiveSearchAd || {}).headlines || []).map(function (h) { return h.text; });
      if (hs.indexOf(spanish ? MARK_ES : MARK) >= 0) done = true; else olds.push(x.resourceName); }
    if (!done) {
      var H = spanish ? ES_H : COMMON_H.concat(cfg.h), D = spanish ? ES_D : COMMON_D.slice();
      if (cfg && cfg.d0) D[0] = cfg.d0;
      var url = spanish ? (oldUrl || SITE + "/trucking-health-quote") : SITE + cfg.url;
      var nr = AdsApp.mutate({ adGroupAdOperation: { create: { adGroup: agrn, status: "ENABLED", ad: { finalUrls: [url], responsiveSearchAd: {
        headlines: H.map(function (t) { return { text: t }; }), descriptions: D.map(function (t) { return { text: t }; }),
        path1: spanish ? "camioneros" : cfg.p[0], path2: spanish ? "florida" : cfg.p[1] } } } } });
      L(nr.isSuccessful(), "new Florida ad: " + name, nr);
      if (nr.isSuccessful()) olds.forEach(function (o) { var pr = AdsApp.mutate({ adGroupAdOperation: { update: { resourceName: o, status: "PAUSED" }, updateMask: "status" } }); L(pr.isSuccessful(), "  paused old ad", pr); });
    } else { olds.forEach(function (o) { AdsApp.mutate({ adGroupAdOperation: { update: { resourceName: o, status: "PAUSED" }, updateMask: "status" } }); });
      Logger.log("Already refreshed: " + name + (olds.length ? " (paused " + olds.length + " leftover)" : "")); }
    var have = {}, k = q("SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE ad_group.resource_name = '" + agrn + "' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED'");
    while (k.hasNext()) { var kw = k.next().adGroupCriterion.keyword; have[kw.text.toLowerCase() + "|" + kw.matchType] = true; }
    var add = 0, rej = [];
    (spanish ? ES_KW : cfg.kw).forEach(function (t) { ["PHRASE", "EXACT"].forEach(function (mt) { if (have[t + "|" + mt]) return;
      var kr = AdsApp.mutate({ adGroupCriterionOperation: { create: { adGroup: agrn, status: "ENABLED", keyword: { text: t, matchType: mt } } } });
      if (kr.isSuccessful()) add++; else rej.push(t + " [" + mt + "]"); }); });
    Logger.log("  keywords added: " + add + (rej.length ? " | rejected: " + rej.join(", ") : ""));
  });

  // 4. negatives + desktop
  var hn = {}; it = q("SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.resource_name = '" + crn + "' AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'");
  while (it.hasNext()) hn[it.next().campaignCriterion.keyword.text.toLowerCase()] = true;
  var nok = 0, nt = 0; NEG.forEach(function (t) { if (hn[t]) return; nt++;
    if (AdsApp.mutate({ campaignCriterionOperation: { create: { campaign: crn, negative: true, keyword: { text: t, matchType: "PHRASE" } } } }).isSuccessful()) nok++; });
  Logger.log("Negatives added: " + nok + "/" + nt);
  var dr = AdsApp.mutate({ campaignCriterionOperation: { update: { resourceName: "customers/" + cid + "/campaignCriteria/" + campId + "~30000", bidModifier: 0.5 }, updateMask: "bidModifier" } });
  if (!dr.isSuccessful()) dr = AdsApp.mutate({ campaignCriterionOperation: { create: { campaign: crn, device: { type: "DESKTOP" }, bidModifier: 0.5 } } });
  L(dr.isSuccessful(), "desktop -50%", dr);
  Logger.log("DONE");
}

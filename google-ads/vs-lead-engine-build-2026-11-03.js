/* VS Lead Engine - BUILD (Nov 3 2026).  PREVIEW first, then RUN.  Safe to re-run.
   ------------------------------------------------------------------------------
   Builds 5 Search campaigns, $50/day total:
     Trucker - FL & GA ............ $8.33/day   people located in FL, GA
     Trucker - TX, IL & OH ........ $8.33/day   people located in TX, IL, OH
     Trucker - KY, MO & MD ........ $8.34/day   people located in KY, MO, MD
     Self-Employed 1099 - 8 States  $17.50/day  all 8 states
     Spanish - Camioneros e Independientes  $7.50/day  all 8 states, Spanish speakers
   Every campaign: Google Search only, "people located in" (presence), phrase + exact
   keywords only, Maximize clicks with a $15 max CPC, shared negative list (no ACA /
   Medicaid / jobs / truck insurance...), call asset (staffed hours), call-only ads
   (phones), sitelinks + callouts, ads landing on /lp/<niche> (routes to the state page).
   Then: lead form asset on each campaign (posts leads to /api/gads-lead), conversion
   goals (60s+ calls + form submits + Sold Policy upload), and "Trucker Health - OE 2027" paused.
   Companion script: vs-lead-engine-hourly-2026-11-03.js (call-ad hours, weekly sold upload,
   switch to Maximize conversions after 15 leads). */

var SITE = "https://www.vshealthbenefits.com";
var PHONE = "(954) 825-1009";
var GADS_LEAD_KEY = "8Sf46llj173PlrzDSaejk5KpojwgFLjS";   // must equal GADS_LEAD_KEY in Vercel
var OLD_CAMPAIGN = "Trucker Health - OE 2027";
var MAX_CPC = 15;
var NEG_LIST = "VS Leads - Negatives (Nov 3)";

var EN = "languageConstants/1000", ES = "languageConstants/1003";
var ALL8 = ["Florida", "Georgia", "Texas", "Illinois", "Ohio", "Kentucky", "Missouri", "Maryland"];

// ---------------------------------------------------------------- copy
var TRK_H = ["Private PPO Plans for Truckers", "See Doctors in Any State", "Call a Licensed Advisor Now",
  "Quote in About 2 Minutes", "No Fee to You. Ever.", "Coverage That Rides With You", "Top A-Rated Carriers",
  "Nationwide Doctor Networks", "Plans for You and Your Family", "Coverage Can Start Next Month",
  "5.0 Stars, 53 Google Reviews", "Talk to a Real Person Today"];
var TRK_D = ["Private PPO health plans for truck drivers from top A-rated carriers. Free, licensed help.",
  "Owner-operators, 1099 and company drivers: compare real prices for your ZIP in minutes.",
  "Nationwide PPO options so you can see a doctor on the road. Call or get a quote online.",
  "Carriers pay us, not you. Same price as going direct, with an advisor who knows trucking."];
var SE_H = ["Private PPO for Self-Employed", "Call a Licensed Advisor Now", "Compare Top A-Rated Carriers",
  "Quote in About 2 Minutes", "No Fee to You. Ever.", "Plans for You and Your Family", "Pick Your Own Doctors",
  "Coverage Can Start Next Month", "Talk to a Real Person Today", "5.0 Stars, 53 Google Reviews",
  "Nationwide PPO Networks", "Free Quote. No Obligation."];
var SE_D = ["Private PPO health plans for self-employed and 1099 workers from top A-rated carriers.",
  "No employer plan? Compare real prices for your ZIP with a licensed advisor. Free.",
  "Freelancers, contractors and owners: pick your doctors with a PPO. Call or quote online.",
  "Carriers pay us, not you. Same price as going direct, plus an advisor on your side."];
var ES_H = ["Planes PPO Privados", "Asesor con Licencia, Gratis", "Llame Hoy y Hable en Español",
  "Cotización en 2 Minutos", "Médicos en Todo el País", "Sin Costo Para Usted", "Aseguradoras Calificación A",
  "Planes Para Toda la Familia", "Cobertura Desde el Próximo Mes", "Hablamos Español", "Cotización Gratis",
  "5.0 Estrellas en Google"];
var ES_D = ["Planes PPO privados de las mejores aseguradoras. Asesor con licencia que habla español.",
  "Compare precios reales para su código postal en minutos. Llame o cotice en línea. Gratis.",
  "Las aseguradoras nos pagan a nosotros. Usted paga lo mismo y recibe ayuda en español.",
  "Médicos en todo el país con planes PPO selectos. Hable hoy con un asesor con licencia."];

function kws(list) { return list; }
var TRK_GROUPS = [
  { name: "Truck Driver", url: "/lp/truckers", p: ["truckers", "free-quote"],
    h: ["Truck Driver Health Insurance", "Health Plans for Truckers", "OTR & Regional Driver Plans"],
    k: ["truck driver health insurance", "health insurance for truck drivers", "truckers health insurance",
        "health insurance for truckers", "trucker health insurance", "otr truck driver health insurance",
        "truck driver medical insurance", "cdl driver health insurance", "medical insurance for truck drivers"],
    sk: ["truck driver health insurance %s", "health insurance for truck drivers %s"] },
  { name: "Owner Operator", url: "/lp/truckers", p: ["owner-operator", "free-quote"],
    h: ["Owner Operator Health Plans", "Insurance for Owner Operators", "Built for Owner Operators"],
    k: ["owner operator health insurance", "health insurance for owner operators", "owner operator medical insurance",
        "owner operator health insurance cost", "health insurance for independent truckers",
        "independent trucker health insurance", "lease operator health insurance",
        "health insurance for owner operator truck drivers"],
    sk: ["owner operator health insurance %s"] },
  { name: "Company Driver - No Benefits", url: "/lp/truckers", p: ["truckers", "get-covered"],
    h: ["Company Driver, No Benefits?", "Skip the Long Waiting Period", "Covered Between Carriers"],
    k: ["truck driver no health insurance", "trucking company no health insurance",
        "health insurance between trucking companies", "company driver health insurance",
        "health insurance for new truck drivers"],
    sk: [] }
];
var SE_GROUPS = [
  { name: "Self-Employed", url: "/lp/self-employed", p: ["self-employed", "free-quote"],
    h: ["Self-Employed Health Insurance", "Health Plans for Self-Employed", "Self-Employed? Get Covered"],
    k: ["self employed health insurance", "health insurance for self employed", "health insurance self employed",
        "private health insurance self employed", "best health insurance for self employed",
        "health insurance for self employed individuals", "self employed health plans",
        "ppo health insurance self employed"] },
  { name: "1099 Workers", url: "/lp/self-employed", p: ["1099", "free-quote"],
    h: ["1099 Health Insurance Plans", "Health Insurance for 1099", "Independent Contractor Plans"],
    k: ["1099 health insurance", "health insurance for 1099 employees", "health insurance for 1099 workers",
        "health insurance for independent contractors", "independent contractor health insurance",
        "1099 contractor health insurance"] },
  { name: "Freelancer & Business Owner", url: "/lp/self-employed", p: ["self-employed", "owners"],
    h: ["Freelancer Health Insurance", "Plans for One-Person Shops", "Small Business Owner Plans"],
    k: ["freelancer health insurance", "health insurance for freelancers", "sole proprietor health insurance",
        "health insurance for small business owner", "llc owner health insurance", "gig worker health insurance"] }
];
var ES_GROUPS = [
  { name: "Camioneros", url: "/lp/es/camioneros", p: ["camioneros", "cotizacion"],
    h: ["Seguro Médico para Camioneros", "Seguro de Salud Camioneros", "Planes para Owner Operators"],
    k: ["seguro medico para camioneros", "seguro de salud para camioneros", "seguro medico para troqueros",
        "seguro medico para choferes de camion", "seguro medico owner operator", "aseguranza medica para camioneros"] },
  { name: "Independientes", url: "/lp/es/independientes", p: ["independientes", "cotizacion"],
    h: ["Seguro Médico Independientes", "Seguro de Salud Para 1099", "Para Trabajadores Por Cuenta"],
    k: ["seguro medico para trabajadores independientes", "seguro de salud para independientes",
        "seguro medico 1099", "seguro medico para trabajadores por cuenta propia",
        "seguro medico para contratistas", "aseguranza medica independiente"] }
];

var CAMPAIGNS = [
  { name: "Trucker - FL & GA", budget: 8.33, states: ["Florida", "Georgia"], lang: EN, groups: TRK_GROUPS, H: TRK_H, D: TRK_D, kind: "trk", slug: "trucker-fl-ga" },
  { name: "Trucker - TX, IL & OH", budget: 8.33, states: ["Texas", "Illinois", "Ohio"], lang: EN, groups: TRK_GROUPS, H: TRK_H, D: TRK_D, kind: "trk", slug: "trucker-tx-il-oh" },
  { name: "Trucker - KY, MO & MD", budget: 8.34, states: ["Kentucky", "Missouri", "Maryland"], lang: EN, groups: TRK_GROUPS, H: TRK_H, D: TRK_D, kind: "trk", slug: "trucker-ky-mo-md" },
  { name: "Self-Employed 1099 - 8 States", budget: 17.50, states: ALL8, lang: EN, groups: SE_GROUPS, H: SE_H, D: SE_D, kind: "se", slug: "self-employed-8" },
  { name: "Spanish - Camioneros e Independientes", budget: 7.50, states: ALL8, lang: ES, groups: ES_GROUPS, H: ES_H, D: ES_D, kind: "es", slug: "spanish-8" }
];

// call-only ads (phones). businessName <=25, headlines <=30, descriptions <=35
var CALL_AD = {
  trk: { h1: "Truck Driver Health Insurance", h2: "Talk to a Licensed Advisor", d1: "Private PPO plans for drivers.", d2: "Free quote. No fee to you." },
  se:  { h1: "Self-Employed Health Plans", h2: "Talk to a Licensed Advisor", d1: "Private PPO plans for 1099 work.", d2: "Free quote. No fee to you." },
  es:  { h1: "Seguro Médico Privado PPO", h2: "Hable con un Asesor Hoy", d1: "Asesor con licencia en español.", d2: "Cotización gratis, sin costo." }
};
var SITELINKS = {
  trk: [["Get My Free Quote", "/lp/truckers", "Takes about 30 seconds", "A licensed advisor calls back"],
        ["What Drivers Pay", "/truck-driver-health-insurance-cost", "Real premium ranges", "By age and family size"],
        ["Owner-Operator Plans", "/best-health-insurance-owner-operators", "Plans for O/O and 1099", "Compare carriers free"],
        ["DOT Physical Coverage", "/does-health-insurance-cover-dot-physical", "What plans cover for CDL", "Know before your exam"]],
  se:  [["Get My Free Quote", "/lp/self-employed", "Takes about 30 seconds", "A licensed advisor calls back"],
        ["Self-Employed Plans", "/self-employed-health-insurance", "PPO plans for your own work", "Compare carriers free"],
        ["1099 Health Insurance", "/1099-health-insurance", "Coverage for contractors", "Pick your own doctors"],
        ["Private PPO Plans", "/private-health-insurance", "Top A-rated carriers", "Broad national networks"]],
  es:  [["Cotización Gratis", "/lp/es/camioneros", "Toma unos 30 segundos", "Un asesor le llama pronto"],
        ["Para Camioneros", "/seguro-medico-camioneros", "Planes para choferes", "Médicos en todo el país"],
        ["Para Owner Operators", "/seguro-medico-owner-operators", "Planes para dueños", "Compare gratis"],
        ["Para Independientes", "/lp/es/independientes", "Trabajadores 1099", "Asesor en español"]]
};
var CALLOUTS = {
  trk: ["No Fee to You", "Licensed Advisors", "Same-Day Quotes", "Top A-Rated Carriers", "Nationwide PPO Options", "Owner-Operators Welcome"],
  se:  ["No Fee to You", "Licensed Advisors", "Same-Day Quotes", "Top A-Rated Carriers", "Pick Your Own Doctors", "Family Plans Available"],
  es:  ["Sin Costo Para Usted", "Hablamos Español", "Asesores con Licencia", "Cotización el Mismo Día", "Planes PPO Privados"]
};
var LEAD_FORM = {
  en: { cta: "GET_QUOTE", ctaDesc: "Get your free quote today", headline: "Free Health Insurance Quote",
        desc: "Leave your name, phone and ZIP. A licensed advisor calls you back, usually within minutes during business hours. No fee.",
        ph: "Thanks, we got it", pd: "A licensed advisor will call you shortly. Want to talk now? Call " + PHONE + "." },
  es: { cta: "GET_QUOTE", ctaDesc: "Cotización gratis hoy", headline: "Cotización Gratis de Seguro",
        desc: "Deje su nombre, teléfono y código postal. Un asesor con licencia le llama, casi siempre en minutos en horario de oficina. Sin costo.",
        ph: "Gracias, lo recibimos", pd: "Un asesor con licencia le llamará pronto. ¿Prefiere hablar ahora? Llame al " + PHONE + "." }
};
var NEGATIVES = ["aca", "obamacare", "obama care", "affordable care act", "marketplace", "healthcare gov", "healthcare.gov",
  "subsidy", "subsidies", "tax credit", "premium tax credit", "medicaid", "medicare", "chip", "calculator",
  "jobs", "job", "hiring", "careers", "salary", "cdl school", "cdl training", "trucking school", "truck driving school",
  "truck insurance", "commercial truck insurance", "semi truck insurance", "cargo", "cargo insurance", "bobtail",
  "physical damage", "liability insurance", "auto insurance", "car insurance", "dental", "vision", "life insurance",
  "workers comp", "occupational accident", "pet insurance", "travel insurance", "free health insurance", "free clinic",
  "low income", "dot physical", "login", "claims",
  "trabajo", "empleo", "seguro de camion", "seguro de carga", "seguro de auto", "subsidio", "mercado de seguros", "escuela cdl"];
// staffed hours for the call asset (account time zone)
var HOURS = [["MONDAY", 8, 18], ["TUESDAY", 8, 18], ["WEDNESDAY", 8, 18], ["THURSDAY", 8, 18], ["FRIDAY", 8, 18], ["SATURDAY", 8, 13], ["SUNDAY", 8, 13]];

// ---------------------------------------------------------------- helpers
var CID, PREVIEW, tmp = -1, problems = [];
function T(type) { return "customers/" + CID + "/" + type + "/" + (tmp--); }
function say(m) { Logger.log(m); }
function bad(m) { problems.push(m); Logger.log("!! " + m); }
function chk(text, max, where) { if (String(text).length > max) bad("TOO LONG (" + String(text).length + ">" + max + ") " + where + ": " + text); return text; }
function q(gaql) { var out = [], it = AdsApp.search(gaql); while (it.hasNext()) out.push(it.next()); return out; }
function errs(r) { try { return r.getErrorMessages().join(" | "); } catch (e) { return String(e); } }
function lower(s) { return String(s).toLowerCase(); }

function main() {
  CID = AdsApp.currentAccount().getCustomerId().replace(/-/g, "");
  PREVIEW = AdsApp.getExecutionInfo().isPreview();
  say((PREVIEW ? "PREVIEW" : "RUN") + " - account " + AdsApp.currentAccount().getName() + " (" + CID + ")");

  // ---- 0. length check on every piece of copy before touching the account
  CAMPAIGNS.forEach(function (c) {
    c.H.forEach(function (h) { chk(h, 30, c.name + " headline"); });
    c.D.forEach(function (d) { chk(d, 90, c.name + " description"); });
    c.groups.forEach(function (g) { g.h.forEach(function (h) { chk(h, 30, g.name + " headline"); }); g.p.forEach(function (p) { chk(p, 15, g.name + " path"); });
      if (g.h.length + c.H.length > 15) bad(g.name + ": more than 15 headlines"); });
  });
  Object.keys(CALL_AD).forEach(function (k) { var a = CALL_AD[k]; chk(a.h1, 30, k + " call h1"); chk(a.h2, 30, k + " call h2"); chk(a.d1, 35, k + " call d1"); chk(a.d2, 35, k + " call d2"); });
  Object.keys(SITELINKS).forEach(function (k) { SITELINKS[k].forEach(function (s) { chk(s[0], 25, "sitelink"); chk(s[2], 35, "sitelink d1"); chk(s[3], 35, "sitelink d2"); }); });
  Object.keys(CALLOUTS).forEach(function (k) { CALLOUTS[k].forEach(function (s) { chk(s, 25, "callout"); }); });
  Object.keys(LEAD_FORM).forEach(function (k) { var f = LEAD_FORM[k]; chk(f.ctaDesc, 30, "lead form cta"); chk(f.headline, 30, "lead form headline"); chk(f.desc, 200, "lead form desc"); chk(f.ph, 30, "lead form post headline"); chk(f.pd, 200, "lead form post desc"); });
  if (problems.length) { say("STOPPED: fix the copy above, nothing was changed."); return; }

  // ---- 1. conversion goals: count only 60s+ calls, form submits, lead forms, and sold policies
  var callConv = setupConversions();

  // ---- 2. what already exists
  var existing = {};
  q("SELECT campaign.name, campaign.resource_name, campaign.status FROM campaign WHERE campaign.status != 'REMOVED'")
    .forEach(function (r) { existing[r.campaign.name] = r.campaign.resourceName; });
  var geo = {};
  q("SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.country_code = 'US' AND geo_target_constant.target_type = 'State' AND geo_target_constant.status = 'ENABLED'")
    .forEach(function (r) { geo[r.geoTargetConstant.name] = r.geoTargetConstant.resourceName; });
  ALL8.forEach(function (s) { if (!geo[s]) bad("No geo target found for " + s); });
  if (problems.length) return;

  var todo = CAMPAIGNS.filter(function (c) { if (existing[c.name]) { say("Already exists, skipped: " + c.name); return false; } return true; });

  // ---- 3. build everything new in ONE all-or-nothing batch
  if (todo.length) {
    var ops = [];
    // shared negative list
    var negRn = null;
    q("SELECT shared_set.resource_name, shared_set.name FROM shared_set WHERE shared_set.type = 'NEGATIVE_KEYWORDS' AND shared_set.status = 'ENABLED'")
      .forEach(function (r) { if (r.sharedSet.name === NEG_LIST) negRn = r.sharedSet.resourceName; });
    if (!negRn) {
      negRn = T("sharedSets");
      ops.push({ sharedSetOperation: { create: { resourceName: negRn, name: NEG_LIST, type: "NEGATIVE_KEYWORDS" } } });
      NEGATIVES.forEach(function (n) { ops.push({ sharedCriterionOperation: { create: { sharedSet: negRn, keyword: { text: n, matchType: "PHRASE" } } } }); });
    }
    // call asset (staffed hours)
    var callAsset = T("assets");
    ops.push({ assetOperation: { create: { resourceName: callAsset, callAsset: {
      countryCode: "US", phoneNumber: PHONE,
      callConversionReportingState: "USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION",
      adScheduleTargets: HOURS.map(function (h) { return { dayOfWeek: h[0], startHour: h[1], startMinute: "ZERO", endHour: h[2], endMinute: "ZERO" }; })
    } } } });
    // sitelinks + callouts, one set per kind
    var kindAssets = {};
    ["trk", "se", "es"].forEach(function (k) {
      if (!todo.some(function (c) { return c.kind === k; })) return;
      kindAssets[k] = { sl: [], co: [] };
      SITELINKS[k].forEach(function (s) { var rn = T("assets"); kindAssets[k].sl.push(rn);
        ops.push({ assetOperation: { create: { resourceName: rn, finalUrls: [SITE + s[1]], sitelinkAsset: { linkText: s[0], description1: s[2], description2: s[3] } } } }); });
      CALLOUTS[k].forEach(function (s) { var rn = T("assets"); kindAssets[k].co.push(rn);
        ops.push({ assetOperation: { create: { resourceName: rn, calloutAsset: { calloutText: s } } } }); });
    });

    todo.forEach(function (c) {
      var bRn = T("campaignBudgets"), cRn = T("campaigns");
      ops.push({ campaignBudgetOperation: { create: { resourceName: bRn, name: c.name + " budget", amountMicros: Math.round(c.budget * 1e6), deliveryMethod: "STANDARD", explicitlyShared: false } } });
      ops.push({ campaignOperation: { create: {
        resourceName: cRn, name: c.name, status: "ENABLED", advertisingChannelType: "SEARCH", campaignBudget: bRn,
        networkSettings: { targetGoogleSearch: true, targetSearchNetwork: false, targetContentNetwork: false, targetPartnerSearchNetwork: false },
        geoTargetTypeSetting: { positiveGeoTargetType: "PRESENCE", negativeGeoTargetType: "PRESENCE" },
        targetSpend: { cpcBidCeilingMicros: MAX_CPC * 1e6 },
        finalUrlSuffix: "utm_source=google&utm_medium=cpc&utm_campaign=" + c.slug,
        containsEuPoliticalAdvertising: "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING"
      } } });
      c.states.forEach(function (s) { ops.push({ campaignCriterionOperation: { create: { campaign: cRn, location: { geoTargetConstant: geo[s] } } } }); });
      ops.push({ campaignCriterionOperation: { create: { campaign: cRn, language: { languageConstant: c.lang } } } });
      ops.push({ campaignSharedSetOperation: { create: { campaign: cRn, sharedSet: negRn } } });
      ops.push({ campaignAssetOperation: { create: { campaign: cRn, asset: callAsset, fieldType: "CALL" } } });
      kindAssets[c.kind].sl.forEach(function (a) { ops.push({ campaignAssetOperation: { create: { campaign: cRn, asset: a, fieldType: "SITELINK" } } }); });
      kindAssets[c.kind].co.forEach(function (a) { ops.push({ campaignAssetOperation: { create: { campaign: cRn, asset: a, fieldType: "CALLOUT" } } }); });

      c.groups.forEach(function (g) {
        var gRn = T("adGroups");
        ops.push({ adGroupOperation: { create: { resourceName: gRn, campaign: cRn, name: g.name, status: "ENABLED", type: "SEARCH_STANDARD" } } });
        var words = g.k.slice();
        (g.sk || []).forEach(function (pat) { c.states.forEach(function (s) { words.push(pat.replace("%s", lower(s))); }); });
        words.forEach(function (w) { ["PHRASE", "EXACT"].forEach(function (mt) {
          ops.push({ adGroupCriterionOperation: { create: { adGroup: gRn, status: "ENABLED", keyword: { text: w, matchType: mt } } } }); }); });
        ops.push({ adGroupAdOperation: { create: { adGroup: gRn, status: "ENABLED", ad: {
          finalUrls: [SITE + g.url],
          responsiveSearchAd: { headlines: g.h.concat(c.H).slice(0, 15).map(function (t) { return { text: t }; }),
                                descriptions: c.D.map(function (t) { return { text: t }; }), path1: g.p[0], path2: g.p[1] } } } } });
        var ca = CALL_AD[c.kind];
        ops.push({ adGroupAdOperation: { create: { adGroup: gRn, status: "ENABLED", ad: {
          finalUrls: [SITE + g.url],
          callAd: { countryCode: "US", phoneNumber: PHONE, businessName: "VS Health Benefits", headline1: ca.h1, headline2: ca.h2,
                    description1: ca.d1, description2: ca.d2, callTracked: true, disableCallConversion: false,
                    conversionReportingState: "USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION", phoneNumberVerificationUrl: SITE + "/contact" } } } } });
      });
    });

    say("Sending " + ops.length + " changes in one batch (all or nothing)...");
    var res = AdsApp.mutateAll(ops, { partialFailure: false });
    var failed = res.filter(function (r) { return !r.isSuccessful(); });
    if (failed.length) {
      failed.slice(0, 10).forEach(function (r) { bad("Build error: " + errs(r)); });
      say("STOPPED: nothing was created. Send me the errors above.");
      return;
    }
    todo.forEach(function (c) { say("OK  " + c.name + "  $" + c.budget.toFixed(2) + "/day  " + c.states.join(", ") +
      "  (" + c.groups.length + " ad groups, phrase+exact, $" + MAX_CPC + " max CPC)"); });
    if (PREVIEW) say("Preview: Google checked all " + ops.length + " changes and would accept them.");
  }

  // ---- 4. lead form asset on each campaign (separate: Google can refuse lead forms for some accounts)
  addLeadForms();

  // ---- 5. pause the old single campaign once all 5 new ones exist
  var have = {};
  q("SELECT campaign.name, campaign.status FROM campaign WHERE campaign.status != 'REMOVED'").forEach(function (r) { have[r.campaign.name] = r.campaign.status; });
  var allNew = CAMPAIGNS.every(function (c) { return have[c.name]; });
  var old = q("SELECT campaign.resource_name, campaign.status FROM campaign WHERE campaign.name = '" + OLD_CAMPAIGN + "'")[0];
  if (old && old.campaign.status === "ENABLED") {
    if (allNew || PREVIEW) {
      var pr = AdsApp.mutate({ campaignOperation: { update: { resourceName: old.campaign.resourceName, status: "PAUSED" }, updateMask: "status" } });
      say((pr.isSuccessful() ? "OK  paused " : "!! could not pause ") + OLD_CAMPAIGN + (pr.isSuccessful() ? "" : ": " + errs(pr)));
    } else say("Left " + OLD_CAMPAIGN + " running: not all new campaigns exist yet.");
  }

  say(problems.length ? "DONE WITH " + problems.length + " WARNING(S) - see lines starting with !!" : "DONE. No errors.");
  say("Next: add the companion script 'VS Lead Engine - Hourly' and schedule it Hourly.");
}

// ---------------------------------------------------------------- conversions
function setupConversions() {
  var rows = q("SELECT conversion_action.resource_name, conversion_action.name, conversion_action.type, conversion_action.status, " +
    "conversion_action.primary_for_goal, conversion_action.phone_call_duration_seconds FROM conversion_action WHERE conversion_action.status = 'ENABLED'");
  var ops = [], notes = [], adCall = null, sold = null;
  rows.forEach(function (r) {
    var c = r.conversionAction, name = c.name, type = c.type;
    var keep = type === "AD_CALL" || /quote form lead/i.test(name) || /lead form/i.test(name) || type === "LEAD_FORM_SUBMIT" || /sold policy/i.test(name);
    if (type === "AD_CALL" && !adCall) adCall = c;
    if (/sold policy/i.test(name)) sold = c;
    if (type === "AD_CALL") {
      ops.push({ conversionActionOperation: { update: { resourceName: c.resourceName, phoneCallDurationSeconds: 60, primaryForGoal: true }, updateMask: "phone_call_duration_seconds,primary_for_goal" } });
      notes.push("counts (calls 60s+): " + name);
    } else if (keep) {
      if (!c.primaryForGoal) ops.push({ conversionActionOperation: { update: { resourceName: c.resourceName, primaryForGoal: true }, updateMask: "primary_for_goal" } });
      notes.push("counts: " + name);
    } else if (c.primaryForGoal) {
      ops.push({ conversionActionOperation: { update: { resourceName: c.resourceName, primaryForGoal: false }, updateMask: "primary_for_goal" } });
      notes.push("now observe-only (secondary): " + name);
    }
  });
  var newCall = null, callIdx = -1;
  if (!adCall) {
    newCall = T("conversionActions"); callIdx = ops.length;
    ops.push({ conversionActionOperation: { create: { resourceName: newCall, name: "Calls from ads (60s+)", type: "AD_CALL", category: "PHONE_CALL_LEAD",
      status: "ENABLED", phoneCallDurationSeconds: 60, primaryForGoal: true, countingType: "ONE_PER_CLICK",
      valueSettings: { defaultValue: 1, alwaysUseDefaultValue: true } } } });
    notes.push("created: Calls from ads (60s+)");
  }
  if (!sold) {
    ops.push({ conversionActionOperation: { create: { name: "Sold Policy", type: "UPLOAD_CLICKS", category: "CONVERTED_LEAD",
      status: "ENABLED", primaryForGoal: true, countingType: "ONE_PER_CLICK", clickThroughLookbackWindowDays: 90,
      valueSettings: { defaultValue: 50, alwaysUseDefaultValue: false } } } });
    notes.push("created: Sold Policy (uploaded weekly by the hourly script)");
  }
  if (ops.length) {
    var res = AdsApp.mutateAll(ops, { partialFailure: true });
    res.forEach(function (r) { if (!r.isSuccessful()) bad("Conversion setting not changed: " + errs(r)); });
    if (callIdx >= 0) newCall = (!PREVIEW && res[callIdx].isSuccessful()) ? res[callIdx].getResourceName() : null;
  }
  notes.forEach(function (n) { say("Conversions - " + n); });
  var callRn = adCall ? adCall.resourceName : (PREVIEW ? null : newCall);
  if (callRn) {
    var cr = AdsApp.mutate({ customerOperation: { update: { resourceName: "customers/" + CID,
      callReportingSetting: { callReportingEnabled: true, callConversionReportingEnabled: true, callConversionAction: callRn } },
      updateMask: "call_reporting_setting.call_reporting_enabled,call_reporting_setting.call_conversion_reporting_enabled,call_reporting_setting.call_conversion_action" } });
    say(cr.isSuccessful() ? "Conversions - call reporting on; ad calls of 60s+ count as leads" : "!! call reporting not updated: " + errs(cr));
  }
  return callRn;
}

// ---------------------------------------------------------------- lead forms
function addLeadForms() {
  var camps = {};
  q("SELECT campaign.name, campaign.resource_name FROM campaign WHERE campaign.status != 'REMOVED'").forEach(function (r) { camps[r.campaign.name] = r.campaign.resourceName; });
  var linked = {};
  q("SELECT campaign.name, campaign_asset.field_type FROM campaign_asset WHERE campaign_asset.field_type = 'LEAD_FORM' AND campaign_asset.status = 'ENABLED'")
    .forEach(function (r) { linked[r.campaign.name] = true; });
  ["en", "es"].forEach(function (lang) {
    var targets = CAMPAIGNS.filter(function (c) { return (lang === "es") === (c.kind === "es") && !linked[c.name]; });
    if (!targets.length) return;
    var f = LEAD_FORM[lang], aRn = T("assets");
    var ops = [{ assetOperation: { create: { resourceName: aRn, finalUrls: [SITE + (lang === "es" ? "/lp/es/camioneros" : "/lp/truckers")], leadFormAsset: {
      businessName: "VS Health Benefits", callToActionType: f.cta, callToActionDescription: f.ctaDesc, headline: f.headline, description: f.desc,
      privacyPolicyUrl: SITE + "/privacy",
      fields: [{ inputType: "FULL_NAME" }, { inputType: "PHONE_NUMBER" }, { inputType: "POSTAL_CODE" }],
      postSubmitHeadline: f.ph, postSubmitDescription: f.pd, postSubmitCallToActionType: "VISIT_SITE",
      deliveryMethods: [{ webhook: { advertiserWebhookUrl: SITE + "/api/gads-lead", googleSecret: GADS_LEAD_KEY, payloadSchemaVersion: 3 } }]
    } } } }];
    var real = targets.filter(function (c) { return camps[c.name]; });
    real.forEach(function (c) { ops.push({ campaignAssetOperation: { create: { campaign: camps[c.name], asset: aRn, fieldType: "LEAD_FORM" } } }); });
    var res = AdsApp.mutateAll(ops, { partialFailure: false });
    var failed = res.filter(function (r) { return !r.isSuccessful(); });
    if (failed.length) bad("Lead form (" + lang + ") not added - Google said: " + errs(failed[0]) + "  (campaigns still run without it)");
    else say("OK  lead form (" + lang + ") " + (real.length ? "on " + real.map(function (c) { return c.name; }).join(", ") : "checked; links after Run"));
  });
}

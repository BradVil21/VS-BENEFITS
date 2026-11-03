/* VS Campaign Builder (Google Ads Script). Trucker-only since Nov 1 2026 (Small Biz + Individual moved to archive-2026-11-01/). Creates PAUSED Search campaigns with
   keywords, negatives, responsive search ads, sitelinks, callouts and a call asset.
   Re-runnable: any campaign whose name already exists is skipped. Preview = validate only. */
var SITE = "https://www.vshealthbenefits.com";
var STATES33 = ["Alabama","Arizona","Arkansas","Colorado","Florida","Georgia","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maryland","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","North Carolina","North Dakota","Ohio","Oklahoma","South Carolina","South Dakota","Tennessee","Texas","Utah","Virginia","West Virginia","Wisconsin","Wyoming"];
var NEG_COMMON = ["medicare","medicaid","aarp","jobs","job","hiring","salary","career","careers","login","sign in","phone number","customer service","claims address","free","dental","vision","eye","glasses","costco","sams club","license","licensing","how to become","agent jobs","pet","travel insurance","life insurance"];

var EN_T = ["Health Insurance for Truckers","2027 Rates Are Up. Compare Now","Open Enrollment Starts Nov 1","Enroll by Dec 15 for Jan 1","Owner Operator Health Plans","Plans That Work on the Road","Nationwide PPO Options","Quote in About 60 Seconds","Free Quote, Licensed Advisor","Tax Credits Can Cut Premiums","1099 Driver Health Coverage","No Cost to Use an Advisor","Licensed in 33 States","Get Covered Before You Roll","English y Español"];
var EN_T_D = ["2027 premiums are up. A licensed advisor compares plans for drivers, free, from the cab.","Owner-operators and 1099 drivers: plans with PPO networks that travel with you.","Many drivers qualify for tax credits. We check yours free. Carriers pay us, not you.","Open enrollment ends Dec 15 for Jan 1 coverage. Answer 4 quick questions to start."];
var ES_T = ["Seguro Médico Camioneros","Planes para Owner Operators","Cotización Gratis en 60 Seg","Inscripción Abierta 1 Nov","Inscríbase Antes del 15 Dic","Asesor con Licencia","Hablamos Español","Planes PPO Nacionales","Créditos Fiscales Posibles","Sin Costo Para Usted"];
var ES_T_D = ["Las primas de 2027 suben. Un asesor con licencia compara planes para camioneros gratis.","Owner operators y choferes 1099: planes con redes PPO que viajan con usted.","Muchos choferes califican para créditos fiscales. Lo verificamos gratis.","Inscríbase antes del 15 de diciembre para tener cobertura desde el 1 de enero."];
var SB = ["Group Renewal Went Up?","Free Group Renewal Review","2027 Renewals Up 8-15%+","Don't Auto-Renew the Increase","Compare Other Carriers","Level-Funded & ICHRA Options","Health Plans for 2-50 Staff","Licensed FL Health Broker","No Fee to Your Business","Keep Your Team's Doctors","Side-by-Side Before You Sign","Trucking & Contractor Groups","Talk to a Licensed Advisor","Quotes for Small Employers","Se Habla Español"];
var SB_D = ["Small-group renewals are up a median 14% for 2027. We shop yours free before you sign.","We compare carriers, level-funded and ICHRA options side by side. No fee to you.","Send your renewal letter or just the new premium. Review usually within a day.","For 2-50 employees: trucking, contractors, restaurants, offices. Licensed advisor."];
var IN = ["Florida Health Insurance Help","2027 Rates Up? Compare Now","Licensed FL Health Broker","Free Quote, No Obligation","Self-Employed Health Plans","1099 & Gig Worker Coverage","Lost Your Subsidy? Get Help","Lost Coverage? Compare Now","Enroll by Dec 15 for Jan 1","Marketplace & Private PPO","No Fee to Use an Advisor","Se Habla Español","Talk to a Licensed Advisor","Plans From Top Carriers","Compare Plans in Minutes"];
var IN_D = ["2027 premiums are up. A licensed advisor compares Marketplace and private plans free.","Self-employed or 1099? We check tax credits and compare PPO options. No cost to you.","Lost coverage or a subsidy? Enroll by Dec 15 for Jan 1 coverage. Start in 2 minutes.","Local Florida broker, English y Español. Carriers pay us, not you. Same price as direct."];
var IN_ES = ["Seguro Médico en Florida","Agente con Licencia","Cotización Gratis","Hablamos Español","Primas 2027 Suben","Inscríbase Antes del 15 Dic","Planes del Mercado y PPO","Sin Costo Para Usted"];
var IN_ES_D = ["Las primas de 2027 suben. Un asesor con licencia compara planes gratis para usted.","Inscríbase antes del 15 de diciembre para tener cobertura desde el 1 de enero."];
function first(h, arr) { var a = arr.slice(); a[0] = h; return a; }

var CAMPAIGNS = [
 { name: "Trucker Health - OE 2027", budget: 35, bidding: "MAX_CONV", states: ["Florida"], /* STATES33 once health-ad certification covers them */
   suffix: "utm_source=google&utm_medium=cpc&utm_campaign=trucker-oe-2027&utm_term={keyword}",
   neg: NEG_COMMON.concat(["truck insurance","commercial truck insurance","commercial auto","auto insurance","cargo","cargo insurance","liability","physical damage","bobtail","occupational accident","workers comp","cdl school","cdl training","dot physical near me","drug test","teamsters","union","company benefits"]),
   sitelinks: [["2027 Rate Check","/trucking-health-quote"],["Subsidy Cliff Calculator","/owner-operator-subsidy-cliff-calculator"],["Owner-Operator Plans","/best-health-insurance-owner-operators"],["DOT Physical & Insurance","/does-health-insurance-cover-dot-physical"]],
   groups: [
    { g: "Truck Driver Health Insurance", url: "/trucking-health-quote", p: ["truckers", "2027-quote"], h: ["Truck Driver Health Insurance", "Coverage for OTR & Local", "See a Doctor in Any State", "2027 Rates Up? Compare Now", "Pre-Existing Conditions OK", "Quote From the Cab in 2 Min", "Health Insurance for Truckers", "Open Enrollment Is Open Now", "Enroll by Dec 15 for Jan 1", "Plans That Work on the Road", "Nationwide PPO Options", "Priced on What You Net", "Licensed Broker. No Fee.", "Talk to a Licensed Advisor", "Florida Truck Driver Plans"], d: ["Florida truck drivers: compare PPO and Marketplace plans with a licensed broker. Free.", "Owner-operators and 1099 drivers get tax credits on net income after truck costs.", "Open enrollment ends Jan 15. Enroll by Dec 15 for Jan 1 coverage. Quote in 2 minutes.", "Carriers pay us, not you. Same price as going direct, with an advisor who knows trucking."], kw: ["health insurance for truck drivers", "truck driver health insurance", "trucker health insurance", "health insurance for truckers", "otr driver health insurance", "cdl driver health insurance", "trucking health insurance", "truck driver medical insurance", "truck driver health insurance cost", "truck driver health insurance coverage", "health insurance for semi truck drivers", "health insurance for truck drivers florida"] },
    { g: "Owner Operator", url: "/trucking-health-quote", p: ["owner-operator", "2027-quote"], h: ["Owner Operator Health Plans", "Premiums May Be Deductible", "Tax Credits on Net Income", "Plans for You and Your Family", "Built for Owner Operators", "Quote From the Cab in 2 Min", "Health Insurance for Truckers", "Open Enrollment Is Open Now", "Enroll by Dec 15 for Jan 1", "Plans That Work on the Road", "Nationwide PPO Options", "Priced on What You Net", "Licensed Broker. No Fee.", "Talk to a Licensed Advisor", "Florida Truck Driver Plans"], d: ["Florida truck drivers: compare PPO and Marketplace plans with a licensed broker. Free.", "Owner-operators and 1099 drivers get tax credits on net income after truck costs.", "Open enrollment ends Jan 15. Enroll by Dec 15 for Jan 1 coverage. Quote in 2 minutes.", "Carriers pay us, not you. Same price as going direct, with an advisor who knows trucking."], kw: ["owner operator health insurance", "health insurance for owner operators", "best health insurance for owner operators", "lease operator health insurance", "owner operator medical insurance", "medical insurance for owner operators", "health insurance for owner operator truck drivers", "medical insurance for owner operator truck drivers", "owner operator health insurance cost"] },
    { g: "1099 Driver", url: "/trucking-health-quote", p: ["1099-drivers", "2027-quote"], h: ["1099 Driver Health Coverage", "No Employer Plan? Get Covered", "Tax Credits on Net Income", "Self-Employed Driver Plans", "Premiums May Be Deductible", "Quote From the Cab in 2 Min", "Health Insurance for Truckers", "Open Enrollment Is Open Now", "Enroll by Dec 15 for Jan 1", "Plans That Work on the Road", "Nationwide PPO Options", "Priced on What You Net", "Licensed Broker. No Fee.", "Talk to a Licensed Advisor", "Florida Truck Driver Plans"], d: ["Florida truck drivers: compare PPO and Marketplace plans with a licensed broker. Free.", "Owner-operators and 1099 drivers get tax credits on net income after truck costs.", "Open enrollment ends Jan 15. Enroll by Dec 15 for Jan 1 coverage. Quote in 2 minutes.", "Carriers pay us, not you. Same price as going direct, with an advisor who knows trucking."], kw: ["1099 truck driver health insurance", "self employed truck driver health insurance", "independent truck driver health insurance", "health insurance for independent truckers", "health insurance for 1099 truck drivers", "self employed trucker health insurance"] },
    { g: "2027 Rate Increase - Drivers", url: "/trucking-health-quote", p: ["truckers", "2027-rates"], h: ["2027 Rate Increase? Shop Now", "Renewal Went Up? Compare Free", "Lower Your 2027 Premium", "Truck Driver Health Insurance", "Don't Auto-Renew. Compare.", "Quote From the Cab in 2 Min", "Health Insurance for Truckers", "Open Enrollment Is Open Now", "Enroll by Dec 15 for Jan 1", "Plans That Work on the Road", "Nationwide PPO Options", "Priced on What You Net", "Licensed Broker. No Fee.", "Talk to a Licensed Advisor", "Florida Truck Driver Plans"], d: ["Florida truck drivers: compare PPO and Marketplace plans with a licensed broker. Free.", "Owner-operators and 1099 drivers get tax credits on net income after truck costs.", "Open enrollment ends Jan 15. Enroll by Dec 15 for Jan 1 coverage. Quote in 2 minutes.", "Carriers pay us, not you. Same price as going direct, with an advisor who knows trucking."], kw: ["owner operator health insurance 2027", "truck driver health insurance 2027", "truck driver open enrollment", "trucker health insurance open enrollment"] },
    { g: "Company Driver - No Benefits", url: "/trucking-health-quote", p: ["company-driver", "get-covered"], h: ["Company Driver, No Benefits?", "Skip the 90-Day Wait", "Coverage Can Start Next Month", "Covered Between Carriers", "Truck Driver Health Insurance", "Quote From the Cab in 2 Min", "Health Insurance for Truckers", "Open Enrollment Is Open Now", "Enroll by Dec 15 for Jan 1", "Plans That Work on the Road", "Nationwide PPO Options", "Priced on What You Net", "Licensed Broker. No Fee.", "Talk to a Licensed Advisor", "Florida Truck Driver Plans"], d: ["Florida truck drivers: compare PPO and Marketplace plans with a licensed broker. Free.", "Driving for a carrier with no benefits or a long wait? Get covered on your own now.", "Open enrollment ends Jan 15. Enroll by Dec 15 for Jan 1 coverage. Quote in 2 minutes.", "Carriers pay us, not you. Same price as going direct, with an advisor who knows trucking."], kw: ["company truck driver health insurance", "truck driver no health insurance", "health insurance for company drivers", "truck driver waiting period health insurance", "switching trucking companies health insurance"] }
   ] }
];
var CALLOUTS = ["No Fee to You","Licensed Advisor","Same-Day Quotes","English y Español"];

function main() {
  var cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, "");
  var P = "customers/" + cid + "/";
  var bad = [];
  CAMPAIGNS.forEach(function (c) { c.groups.forEach(function (g) {
    g.h.forEach(function (x) { if (x.length > 30) bad.push(c.name + "/" + g.g + " headline: " + x); });
    g.d.forEach(function (x) { if (x.length > 90) bad.push(c.name + "/" + g.g + " desc: " + x); });
  }); });
  if (bad.length) { Logger.log("LENGTH ERRORS:\n" + bad.join("\n")); return; }

  var existing = {};
  var it = AdsApp.search("SELECT campaign.name FROM campaign WHERE campaign.status != 'REMOVED'");
  while (it.hasNext()) existing[it.next().campaign.name] = true;
  var geo = {};
  it = AdsApp.search("SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.country_code = 'US' AND geo_target_constant.target_type = 'State'");
  while (it.hasNext()) { var r = it.next().geoTargetConstant; geo[r.name] = r.resourceName; }

  var tid = -1, sharedReal = null;
  function t() { return tid--; }
  var shared = [];
  var callRes = P + "assets/" + t();
  shared.push({ assetOperation: { create: { resourceName: callRes, callAsset: { countryCode: "US", phoneNumber: "(954) 825-1009" } } } });
  var calloutRes = CALLOUTS.map(function (txt) { var rn = P + "assets/" + t(); shared.push({ assetOperation: { create: { resourceName: rn, calloutAsset: { calloutText: txt } } } }); return rn; });

  CAMPAIGNS.forEach(function (c) {
    if (existing[c.name]) { Logger.log("SKIP (exists): " + c.name); return; }
    var ops = [];
    var b = P + "campaignBudgets/" + t(), cr = P + "campaigns/" + t();
    ops.push({ campaignBudgetOperation: { create: { resourceName: b, name: c.name + " budget", amountMicros: c.budget * 1000000, deliveryMethod: "STANDARD", explicitlyShared: false } } });
    var camp = { resourceName: cr, name: c.name, status: "PAUSED", advertisingChannelType: "SEARCH", campaignBudget: b,
      networkSettings: { targetGoogleSearch: true, targetSearchNetwork: false, targetContentNetwork: false, targetPartnerSearchNetwork: false },
      geoTargetTypeSetting: { positiveGeoTargetType: "PRESENCE", negativeGeoTargetType: "PRESENCE" },
      finalUrlSuffix: c.suffix, containsEuPoliticalAdvertising: "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING" };
    if (c.bidding === "MAX_CONV") camp.maximizeConversions = {};
    else camp.targetSpend = { cpcBidCeilingMicros: c.cpcCap * 1000000 };
    ops.push({ campaignOperation: { create: camp } });
    c.states.forEach(function (s) {
      if (!geo[s]) { Logger.log("No geo for " + s); return; }
      ops.push({ campaignCriterionOperation: { create: { campaign: cr, location: { geoTargetConstant: geo[s] } } } });
    });
    ["languageConstants/1000", "languageConstants/1003"].forEach(function (l) {
      ops.push({ campaignCriterionOperation: { create: { campaign: cr, language: { languageConstant: l } } } });
    });
    if (c.schedule) c.schedule.days.forEach(function (d) {
      ops.push({ campaignCriterionOperation: { create: { campaign: cr, adSchedule: { dayOfWeek: d, startHour: c.schedule.start, startMinute: "ZERO", endHour: c.schedule.end, endMinute: "ZERO" } } } });
    });
    c.neg.forEach(function (k) {
      ops.push({ campaignCriterionOperation: { create: { campaign: cr, negative: true, keyword: { text: k, matchType: "PHRASE" } } } });
    });
    c.groups.forEach(function (g) {
      var ag = P + "adGroups/" + t();
      ops.push({ adGroupOperation: { create: { resourceName: ag, name: g.g, campaign: cr, status: "ENABLED", type: "SEARCH_STANDARD" } } });
      g.kw.forEach(function (k) {
        ["PHRASE", "EXACT"].forEach(function (mt) {
          ops.push({ adGroupCriterionOperation: { create: { adGroup: ag, status: "ENABLED", keyword: { text: k, matchType: mt } } } });
        });
      });
      ops.push({ adGroupAdOperation: { create: { adGroup: ag, status: "ENABLED", ad: { finalUrls: [SITE + g.url],
        responsiveSearchAd: { headlines: g.h.map(function (x) { return { text: x }; }), descriptions: g.d.map(function (x) { return { text: x }; }), path1: g.p[0], path2: g.p[1] } } } } });
    });
    var res = AdsApp.mutateAll(ops, { partialFailure: false });
    var errs = [];
    res.forEach(function (r) { if (!r.isSuccessful()) errs = errs.concat(r.getErrorMessages()); });
    Logger.log((errs.length ? "FAILED: " : "OK: ") + c.name + " (" + ops.length + " operations)" + (errs.length ? "\n  " + errs.slice(0, 8).join("\n  ") : ""));
    if (errs.length) return;
    // Assets: separate request so an asset policy hiccup can never block the campaign itself.
    var firstAssets = !sharedReal;
    var aops = firstAssets ? shared.slice() : [];
    var cRes = firstAssets ? callRes : sharedReal[0], coRes = firstAssets ? calloutRes : sharedReal.slice(1);
    var links = [{ asset: cRes, fieldType: "CALL" }].concat(coRes.map(function (rn) { return { asset: rn, fieldType: "CALLOUT" }; }));
    c.sitelinks.forEach(function (s) {
      var rn = P + "assets/" + t();
      aops.push({ assetOperation: { create: { resourceName: rn, finalUrls: [SITE + s[1]], sitelinkAsset: { linkText: s[0] } } } });
      links.push({ asset: rn, fieldType: "SITELINK" });
    });
    var realCamp = null;
    var q = AdsApp.search("SELECT campaign.resource_name FROM campaign WHERE campaign.name = '" + c.name.replace(/'/g, "\\'") + "'");
    if (q.hasNext()) realCamp = q.next().campaign.resourceName;
    if (!realCamp) { Logger.log("  (assets skipped: campaign not readable yet, normal in Preview)"); return; }
    links.forEach(function (l) { aops.push({ campaignAssetOperation: { create: { campaign: realCamp, asset: l.asset, fieldType: l.fieldType } } }); });
    var ar = AdsApp.mutateAll(aops, { partialFailure: true }), aerr = [];
    ar.forEach(function (r) { if (!r.isSuccessful()) aerr = aerr.concat(r.getErrorMessages()); });
    if (firstAssets) sharedReal = ar.slice(0, shared.length).map(function (r) { return r.isSuccessful() ? r.getResourceName() : null; }).filter(Boolean);
    Logger.log("  assets: " + (aerr.length ? "some failed: " + aerr.slice(0, 4).join("; ") : "call, 4 callouts, " + c.sitelinks.length + " sitelinks linked"));
  });
}

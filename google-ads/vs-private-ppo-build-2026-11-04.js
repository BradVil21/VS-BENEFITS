/* VS Private PPO - BUILD (Nov 4 2026).  PREVIEW first, then RUN.  Safe to re-run.
   ------------------------------------------------------------------------------
   For people who pay full price (too much income for a subsidy). Lands on /private-health-insurance.
   Builds 2 Search campaigns:
     Private PPO - High-Income ZIPs ...... $20/day  ON   ~170 top-income ZIP codes in the 8 states
     Private PPO - 8 States (Rest) ....... $10/day  PAUSED  the 8 states minus those ZIPs (turn on later)
   Each: Google Search only, "people located in", English, phrase + exact, Maximize clicks with a $15 max CPC,
   5 ad groups (Private Health Insurance / PPO / High Income / Lower My Premium / Self-Employed & 1099 Price),
   household income: top 30% + unknown only (lower 70% excluded), the shared list "VS Leads - Negatives (Nov 3)"
   (aca, obamacare, marketplace, subsidy, medicaid...) plus extra campaign negatives (cheap, free, income limit...),
   sitelinks + callouts, a call asset (reused if one exists), and the shared negative list (created if missing).
   ZIP list: highest median household income per state (uszipcode / Census ACS data, ZIPs with 8,000+ people). */

var SITE = "https://www.vshealthbenefits.com";
var LANDING = "/private-health-insurance";
var MAX_CPC = 15;
var NEG_LIST = "VS Leads - Negatives (Nov 3)";
var REUSE_FROM = "Self-Employed FL - 2027";   // borrow its call asset + lead form
var EN = "languageConstants/1000";
var ALL8 = ["Florida", "Georgia", "Texas", "Illinois", "Ohio", "Kentucky", "Missouri", "Maryland"];
var ZIP_CAMPAIGN  = { name: "Private PPO - High-Income ZIPs", budget: 20, status: "ENABLED", slug: "private-ppo-zips" };
var REST_CAMPAIGN = { name: "Private PPO - 8 States (Rest)",  budget: 10, status: "PAUSED",  slug: "private-ppo-rest" };
// Household income: Google's US brackets by percentile. Excluded = lower 70%. Kept: top 30% (70-80, 80-90, 90+) and unknown.
var EXCLUDE_INCOME = ["INCOME_RANGE_0_50", "INCOME_RANGE_50_60", "INCOME_RANGE_60_70"];

var TOP_ZIPS = {
  FL: ["33149", "33327", "33146", "33332", "33076", "33449", "33626", "33330", "33480", "33629", "32259", "34786", "33067", "33547", "33478", "32312", "33028", "32963", "33331", "33412", "33156", "34202", "32003", "33596", "33029", "32082", "32317", "32092", "34212", "33556"],
  TX: ["76092", "77005", "76034", "75225", "77094", "75022", "77401", "77059", "75013", "77382", "78732", "78746", "78739", "77494", "77479", "78733", "78737", "77345", "75078", "78738", "78015", "75094", "76226", "75082", "76248", "75028", "75034", "78255", "77024", "75019"],
  GA: ["30327", "31411", "30075", "30005", "30068", "31820", "30024", "30022", "30097", "30004", "30041", "30319", "30215", "30269", "30809", "30290", "30062", "30305", "30338", "30306"],
  IL: ["60093", "60022", "60521", "60045", "60564", "60558", "60091", "60015", "60047", "60175", "60010", "60585", "60192", "60048", "60565", "60305", "60035", "60012", "60490", "60554"],
  OH: ["43021", "44236", "43082", "43065", "43054", "45243", "43035", "44023", "44139", "45066", "43017", "45434", "43023", "45244", "44141", "45040", "44022", "43147", "43016", "45069"],
  MD: ["20854", "21029", "20817", "20816", "20841", "21042", "20882", "20815", "20720", "20871", "21797", "20639", "20607", "20895", "21146", "20855", "20721", "20832", "21054", "21704"],
  MO: ["63005", "63131", "63124", "64113", "63040", "64082", "63141", "64157", "63017", "63025", "63105", "63304", "63011", "63367", "63368"],
  KY: ["40059", "40513", "40245", "41091", "41048", "40014", "40514", "40241", "40223", "40207", "41001", "41094", "41051", "41005", "40299"]
};

// ---------------------------------------------------------------- copy (headlines <=30, descriptions <=90)
var H = ["Paying Too Much for Coverage?", "Nationwide PPO Options", "Compare Plans in 10 Minutes",
  "Private PPO From Top Carriers", "Pick Your Own Doctors", "Coverage Across State Lines",
  "Earn Too Much for a Subsidy?", "Priced on Health, Not Income", "Licensed Advisor, No Fee",
  "Free Side-by-Side Comparison", "5.0 Stars, 53 Google Reviews", "Apply Any Time of Year"];
var D = ["Paying full price for health insurance? Compare private PPO plans with national networks.",
  "For self-employed people, owner-operators and families who make too much for premium help.",
  "Private plans are priced on your age and health, not your income. Health questions apply.",
  "Independent, licensed advisor. Carriers pay us, not you. Call or compare online today."];
var GROUPS = [
  { name: "Private Health Insurance", p: ["private-ppo", "compare"],
    h: ["Private Health Insurance", "Compare Private Health Plans", "Private Plans for Families"],
    k: ["private health insurance", "private health insurance plans", "private medical insurance",
        "private health insurance quotes", "buy private health insurance", "private family health insurance",
        "private health insurance for family", "off exchange health insurance", "individual private health insurance"] },
  { name: "PPO Health Insurance", p: ["ppo-plans", "compare"],
    h: ["PPO Health Insurance Plans", "Individual & Family PPO Plans", "Nationwide PPO Networks"],
    k: ["ppo health insurance", "ppo health insurance plans", "individual ppo health insurance",
        "nationwide ppo health insurance", "national ppo health insurance", "family ppo health insurance",
        "ppo health insurance for family", "private ppo health insurance", "individual ppo plans"] },
  { name: "High Income", p: ["private-ppo", "high-earners"],
    h: ["Health Plans for High Earners", "For High-Earning Families", "Full Price? Compare Private"],
    k: ["health insurance for high income", "health insurance for high earners", "health insurance for high income earners",
        "best health insurance for high income", "health insurance high income family",
        "health insurance for high income self employed"] },
  { name: "Lower My Premium", p: ["lower-premium", "compare"],
    h: ["Premium Went Up Again?", "Lower Your Premium? Let's See", "Alternatives to High Premiums"],
    k: ["lower my health insurance premium", "health insurance too expensive", "health insurance premiums too high",
        "paying too much for health insurance", "alternative to expensive health insurance",
        "alternatives to expensive health insurance"] },
  { name: "Self-Employed & 1099 - Price", p: ["self-employed", "private-ppo"],
    h: ["Self-Employed? Skip Full Price", "1099 PPO Health Plans", "Private Plans for 1099 Workers"],
    k: ["self employed health insurance too expensive", "1099 health insurance too expensive",
        "lower health insurance premium self employed", "high income self employed health insurance",
        "self employed ppo health insurance", "1099 ppo health insurance", "private health insurance for 1099",
        "private health insurance for self employed family", "self employed family ppo"] }
];
var NEGATIVES = ["aca", "obamacare", "obama care", "affordable care act", "marketplace", "healthcare gov", "healthcare.gov",
  "subsidy", "subsidies", "tax credit", "premium tax credit", "medicaid", "medicare", "chip", "calculator",
  "jobs", "job", "hiring", "careers", "salary", "truck insurance", "commercial truck insurance", "auto insurance", "car insurance",
  "dental", "vision", "life insurance", "workers comp", "pet insurance", "travel insurance", "free health insurance",
  "free clinic", "low income", "login", "claims"];
var HOURS = [["MONDAY", 8, 18], ["TUESDAY", 8, 18], ["WEDNESDAY", 8, 18], ["THURSDAY", 8, 18], ["FRIDAY", 8, 18], ["SATURDAY", 8, 13], ["SUNDAY", 8, 13]];
var PHONE = "(954) 825-1009";
var CAMPAIGN_NEGATIVES = ["cheap", "cheapest", "free", "low cost", "income limit", "income limits", "eligibility",
  "qualify", "employer", "employees", "group health", "small business", "short term", "student", "covered california",
  "medi cal", "what is", "meaning", "definition", "vs hmo", "hmo vs", "how to", "why is", "why are", "reddit", "news", "statistics", "average cost", "lawsuit", "complaint"];
var SITELINKS = [["Why Private PPO Plans", LANDING + "#why-private", "Nationwide networks", "Pick your own doctors"],
  ["Your Plan vs. Private", LANDING + "#compare", "Network, deductible, doctors", "Side by side, no pressure"],
  ["How It Works", LANDING + "#how-it-works", "Free licensed comparison", "Nothing changes until you say"],
  ["Common Questions", LANDING + "#faq", "Switching mid-year", "Pre-existing conditions"]];
var CALLOUTS = ["No Fee to You", "Licensed Advisors", "Nationwide PPO Options", "Pick Your Own Doctors", "Apply Year-Round", "Family Plans Available"];

// ---------------------------------------------------------------- helpers
var CID, PREVIEW, tmp = -1, problems = [];
function T(type) { return "customers/" + CID + "/" + type + "/" + (tmp--); }
function say(m) { Logger.log(m); }
function bad(m) { problems.push(m); Logger.log("!! " + m); }
function chk(text, max, where) { if (String(text).length > max) bad("TOO LONG (" + String(text).length + ">" + max + ") " + where + ": " + text); return text; }
function q(gaql) { var out = [], it = AdsApp.search(gaql); while (it.hasNext()) out.push(it.next()); return out; }
function errs(r) { try { return r.getErrorMessages().join(" | "); } catch (e) { return String(e); } }
function quoteList(a) { return "(" + a.map(function (s) { return "'" + s + "'"; }).join(", ") + ")"; }

function main() {
  CID = AdsApp.currentAccount().getCustomerId().replace(/-/g, "");
  PREVIEW = AdsApp.getExecutionInfo().isPreview();
  say((PREVIEW ? "PREVIEW" : "RUN") + " - account " + AdsApp.currentAccount().getName() + " (" + CID + ")");

  // ---- 0. copy checks before touching anything
  H.forEach(function (h) { chk(h, 30, "headline"); });
  D.forEach(function (d) { chk(d, 90, "description"); });
  GROUPS.forEach(function (g) { g.h.forEach(function (h) { chk(h, 30, g.name + " headline"); }); g.p.forEach(function (p) { chk(p, 15, g.name + " path"); });
    if (g.h.length + H.length > 15) bad(g.name + ": more than 15 headlines"); });
  SITELINKS.forEach(function (s) { chk(s[0], 25, "sitelink"); chk(s[2], 35, "sitelink d1"); chk(s[3], 35, "sitelink d2"); });
  CALLOUTS.forEach(function (s) { chk(s, 25, "callout"); });
  if (problems.length) { say("STOPPED: fix the copy above, nothing was changed."); return; }

  // ---- 1. look things up
  var existing = {};
  q("SELECT campaign.name, campaign.resource_name FROM campaign WHERE campaign.status != 'REMOVED'")
    .forEach(function (r) { existing[r.campaign.name] = r.campaign.resourceName; });
  var states = {};
  q("SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.country_code = 'US' AND geo_target_constant.target_type = 'State' AND geo_target_constant.status = 'ENABLED'")
    .forEach(function (r) { states[r.geoTargetConstant.name] = r.geoTargetConstant.resourceName; });
  ALL8.forEach(function (s) { if (!states[s]) bad("No geo target found for " + s); });
  var wanted = [];
  Object.keys(TOP_ZIPS).forEach(function (st) { wanted = wanted.concat(TOP_ZIPS[st]); });
  var zipRn = {};
  for (var i = 0; i < wanted.length; i += 60) {
    q("SELECT geo_target_constant.resource_name, geo_target_constant.name FROM geo_target_constant WHERE geo_target_constant.country_code = 'US' AND geo_target_constant.target_type = 'Postal Code' AND geo_target_constant.status = 'ENABLED' AND geo_target_constant.name IN " + quoteList(wanted.slice(i, i + 60)))
      .forEach(function (r) { zipRn[r.geoTargetConstant.name] = r.geoTargetConstant.resourceName; });
  }
  var missing = wanted.filter(function (z) { return !zipRn[z]; });
  var zips = wanted.filter(function (z) { return zipRn[z]; });
  say("ZIP targets found: " + zips.length + " of " + wanted.length + (missing.length ? "  (not targetable, skipped: " + missing.join(", ") + ")" : ""));
  if (zips.length < 50) bad("Too few ZIP targets found (" + zips.length + ")");

  var negRn = null;
  q("SELECT shared_set.resource_name, shared_set.name FROM shared_set WHERE shared_set.type = 'NEGATIVE_KEYWORDS' AND shared_set.status = 'ENABLED'")
    .forEach(function (r) { if (r.sharedSet.name === NEG_LIST) negRn = r.sharedSet.resourceName; });
  say("Shared negative list '" + NEG_LIST + "': " + (negRn ? "found, will attach" : "not found, will create it (" + NEGATIVES.length + " words)"));
  var callAsset = null, leadForm = null;
  q("SELECT campaign.name, campaign_asset.asset, campaign_asset.field_type FROM campaign_asset WHERE campaign_asset.status = 'ENABLED' AND campaign.name = '" + REUSE_FROM + "'")
    .forEach(function (r) { var f = r.campaignAsset.fieldType;
      if (f === "CALL" && !callAsset) callAsset = r.campaignAsset.asset;
      if (f === "LEAD_FORM" && !leadForm) leadForm = r.campaignAsset.asset; });
  say("From '" + REUSE_FROM + "': call asset " + (callAsset ? "reused" : "not found, will create one") + ", lead form " + (leadForm ? "reused" : "none (skipped)"));
  if (problems.length) { say("STOPPED: nothing was changed."); return; }

  try { build(existing, states, zips, zipRn, negRn, callAsset); }
  catch (e) { bad("Script error: " + e.message + (e.stack ? " | " + String(e.stack).split("\n").slice(0, 3).join(" / ") : "")); }
  say(problems.length ? "DONE WITH " + problems.length + " WARNING(S) - see lines starting with !!" : "DONE. No errors.");
}

function countBy(gaql, field) { var m = {}; q(gaql).forEach(function (r) { var k = field(r); m[k] = (m[k] || 0) + 1; }); return m; }

function build(existing, states, zips, zipRn, negRn, callAsset) {
  var all = [ZIP_CAMPAIGN, REST_CAMPAIGN];
  var names = quoteList(all.map(function (c) { return c.name; }));
  var camp = {};
  all.forEach(function (c) { if (existing[c.name]) camp[c.name] = existing[c.name]; });
  var sl = null, co = null;

  // Step A: create whatever campaigns are missing (PAUSED), plus negative list + assets
  var missingCamps = all.filter(function (c) { return !camp[c.name]; });
  if (missingCamps.length) {
    var opsA = [], idx = {};
    var addA = function (key, op) { idx[key] = opsA.length; opsA.push(op); };
    if (!negRn) addA("neg", { sharedSetOperation: { create: { resourceName: T("sharedSets"), name: NEG_LIST, type: "NEGATIVE_KEYWORDS" } } });
    if (!callAsset) addA("call", { assetOperation: { create: { resourceName: T("assets"), callAsset: { countryCode: "US", phoneNumber: PHONE,
      callConversionReportingState: "USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION",
      adScheduleTargets: HOURS.map(function (h) { return { dayOfWeek: h[0], startHour: h[1], startMinute: "ZERO", endHour: h[2], endMinute: "ZERO" }; }) } } } });
    missingCamps.forEach(function (c) {
      var bRn = T("campaignBudgets");
      opsA.push({ campaignBudgetOperation: { create: { resourceName: bRn, name: c.name + " budget", amountMicros: Math.round(c.budget * 1e6), deliveryMethod: "STANDARD", explicitlyShared: false } } });
      addA("camp:" + c.name, { campaignOperation: { create: {
        resourceName: T("campaigns"), name: c.name, status: "PAUSED", advertisingChannelType: "SEARCH", campaignBudget: bRn,
        networkSettings: { targetGoogleSearch: true, targetSearchNetwork: false, targetContentNetwork: false, targetPartnerSearchNetwork: false },
        geoTargetTypeSetting: { positiveGeoTargetType: "PRESENCE", negativeGeoTargetType: "PRESENCE" },
        targetSpend: { cpcBidCeilingMicros: MAX_CPC * 1e6 },
        finalUrlSuffix: "utm_source=google&utm_medium=cpc&utm_campaign=" + c.slug,
        containsEuPoliticalAdvertising: "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING" } } });
    });
    say("Step A: creating " + missingCamps.map(function (c) { return c.name; }).join(", ") + " (" + opsA.length + " changes)...");
    var resA = AdsApp.mutateAll(opsA, { partialFailure: false });
    var failA = resA.filter(function (r) { return !r.isSuccessful(); });
    if (failA.length) { failA.slice(0, 5).forEach(function (r) { bad("Step A error: " + errs(r)); }); return; }
    if (PREVIEW) { say("Preview: step A accepted. The later steps are checked once the campaigns exist (Run, then Preview again)."); return; }
    if (idx.neg !== undefined) { negRn = resA[idx.neg].getResourceName(); addNegWords(negRn); }
    if (idx.call !== undefined) callAsset = resA[idx.call].getResourceName();
    missingCamps.forEach(function (c) { camp[c.name] = resA[idx["camp:" + c.name]].getResourceName(); });
  } else {
    say("Both campaigns already exist - checking what is still missing.");
  }

  // What does each campaign already have?
  var locs = countBy("SELECT campaign.name FROM campaign_criterion WHERE campaign_criterion.type = 'LOCATION' AND campaign.name IN " + names, function (r) { return r.campaign.name; });
  var groups = {}; q("SELECT campaign.name, ad_group.name, ad_group.resource_name FROM ad_group WHERE ad_group.status != 'REMOVED' AND campaign.name IN " + names)
    .forEach(function (r) { (groups[r.campaign.name] = groups[r.campaign.name] || {})[r.adGroup.name] = r.adGroup.resourceName; });
  var kws = countBy("SELECT campaign.name FROM ad_group_criterion WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED' AND campaign.name IN " + names, function (r) { return r.campaign.name; });
  var ads = countBy("SELECT campaign.name FROM ad_group_ad WHERE ad_group_ad.status != 'REMOVED' AND campaign.name IN " + names, function (r) { return r.campaign.name; });
  all.forEach(function (c) { say("  " + c.name + ": " + (locs[c.name] || 0) + " locations, " + Object.keys(groups[c.name] || {}).length + " ad groups, " + (kws[c.name] || 0) + " keywords, " + (ads[c.name] || 0) + " ads"); });
  if (negRn) { var nw = q("SELECT shared_criterion.resource_name FROM shared_criterion WHERE shared_set.resource_name = '" + negRn + "'").length;
    say("  Negative list words: " + nw); if (!nw) addNegWords(negRn); }

  // Step B: targeting, negatives, shared list link, assets, ad groups (only for campaigns with no locations yet)
  var needB = all.filter(function (c) { return !locs[c.name]; });
  if (needB.length) {
    sl = []; co = [];
    var opsS = [];
    SITELINKS.forEach(function (s) { opsS.push({ assetOperation: { create: { resourceName: T("assets"), finalUrls: [SITE + s[1]], sitelinkAsset: { linkText: s[0], description1: s[2], description2: s[3] } } } }); });
    CALLOUTS.forEach(function (s) { opsS.push({ assetOperation: { create: { resourceName: T("assets"), calloutAsset: { calloutText: s } } } }); });
    var resS = AdsApp.mutateAll(opsS, { partialFailure: false });
    if (resS.some(function (r) { return !r.isSuccessful(); })) { resS.filter(function (r) { return !r.isSuccessful(); }).slice(0, 3).forEach(function (r) { bad("Assets error: " + errs(r)); }); return; }
    resS.forEach(function (r, i) { (i < SITELINKS.length ? sl : co).push(PREVIEW ? null : r.getResourceName()); });
    var opsB = [];
    needB.forEach(function (c) {
      var cRn = camp[c.name];
      if (c === ZIP_CAMPAIGN) zips.forEach(function (z) { opsB.push({ campaignCriterionOperation: { create: { campaign: cRn, location: { geoTargetConstant: zipRn[z] } } } }); });
      else {
        ALL8.forEach(function (st) { opsB.push({ campaignCriterionOperation: { create: { campaign: cRn, location: { geoTargetConstant: states[st] } } } }); });
        zips.forEach(function (z) { opsB.push({ campaignCriterionOperation: { create: { campaign: cRn, negative: true, location: { geoTargetConstant: zipRn[z] } } } }); });
      }
      opsB.push({ campaignCriterionOperation: { create: { campaign: cRn, language: { languageConstant: EN } } } });
      CAMPAIGN_NEGATIVES.forEach(function (n) { opsB.push({ campaignCriterionOperation: { create: { campaign: cRn, negative: true, keyword: { text: n, matchType: "PHRASE" } } } }); });
      if (negRn) opsB.push({ campaignSharedSetOperation: { create: { campaign: cRn, sharedSet: negRn } } });
      if (callAsset) opsB.push({ campaignAssetOperation: { create: { campaign: cRn, asset: callAsset, fieldType: "CALL" } } });
      if (!PREVIEW) {
        sl.forEach(function (a) { opsB.push({ campaignAssetOperation: { create: { campaign: cRn, asset: a, fieldType: "SITELINK" } } }); });
        co.forEach(function (a) { opsB.push({ campaignAssetOperation: { create: { campaign: cRn, asset: a, fieldType: "CALLOUT" } } }); });
      }
    });
    say("Step B: targeting, negatives and assets for " + needB.map(function (c) { return c.name; }).join(", ") + " (" + opsB.length + " changes)...");
    var resB = AdsApp.mutateAll(opsB, { partialFailure: false });
    var failB = resB.filter(function (r) { return !r.isSuccessful(); });
    if (failB.length) { failB.slice(0, 5).forEach(function (r) { bad("Step B error: " + errs(r)); }); return; }
    say("OK  step B" + (PREVIEW ? " (preview: accepted)" : ""));
  }

  // Ad groups that are missing
  var opsG = [], gIdx = [];
  all.forEach(function (c) { GROUPS.forEach(function (g) {
    if (groups[c.name] && groups[c.name][g.name]) return;
    gIdx.push({ c: c, g: g, i: opsG.length });
    opsG.push({ adGroupOperation: { create: { resourceName: T("adGroups"), campaign: camp[c.name], name: g.name, status: "ENABLED", type: "SEARCH_STANDARD" } } });
  }); });
  if (opsG.length) {
    say("Creating " + opsG.length + " ad groups...");
    var resG = AdsApp.mutateAll(opsG, { partialFailure: false });
    var failG = resG.filter(function (r) { return !r.isSuccessful(); });
    if (failG.length) { failG.slice(0, 5).forEach(function (r) { bad("Ad group error: " + errs(r)); }); return; }
    if (PREVIEW) { say("Preview: ad groups accepted. Keywords and ads are added on Run."); return; }
    gIdx.forEach(function (x) { (groups[x.c.name] = groups[x.c.name] || {})[x.g.name] = resG[x.i].getResourceName(); });
  }

  // Step C: keywords + ads for campaigns that have none yet
  var opsC = [];
  all.forEach(function (c) {
    if (kws[c.name] && ads[c.name]) return;
    GROUPS.forEach(function (g) {
      var gRn = groups[c.name][g.name];
      if (!kws[c.name]) g.k.forEach(function (w) { ["PHRASE", "EXACT"].forEach(function (mt) {
        opsC.push({ adGroupCriterionOperation: { create: { adGroup: gRn, status: "ENABLED", keyword: { text: w, matchType: mt } } } }); }); });
      if (!ads[c.name]) opsC.push({ adGroupAdOperation: { create: { adGroup: gRn, status: "ENABLED", ad: {
        finalUrls: [SITE + LANDING],
        responsiveSearchAd: { headlines: g.h.concat(H).slice(0, 15).map(function (t) { return { text: t }; }),
                              descriptions: D.map(function (t) { return { text: t }; }), path1: g.p[0], path2: g.p[1] } } } } });
    });
  });
  if (opsC.length) {
    say("Step C: keywords and ads (" + opsC.length + " changes)...");
    var resC = AdsApp.mutateAll(opsC, { partialFailure: false });
    var failC = resC.filter(function (r) { return !r.isSuccessful(); });
    if (failC.length) { failC.slice(0, 5).forEach(function (r) { bad("Step C error: " + errs(r)); }); return; }
    say("OK  step C" + (PREVIEW ? " (preview: accepted)" : ""));
  }

  // Step D: income targeting, lead form, switch on the ZIP campaign
  addIncome(); addLeadForm();
  var on = all.filter(function (c) { return c.status === "ENABLED"; }).map(function (c) {
    return { campaignOperation: { update: { resourceName: camp[c.name], status: "ENABLED" }, updateMask: "status" } }; });
  var r = AdsApp.mutateAll(on, { partialFailure: true });
  r.forEach(function (x) { if (!x.isSuccessful()) bad("Could not switch on: " + errs(x)); });
  all.forEach(function (c) { say("OK  " + c.name + "  $" + c.budget.toFixed(2) + "/day  " + c.status); });
}

function addNegWords(negRn) {
  var ops = NEGATIVES.map(function (n) { return { sharedCriterionOperation: { create: { sharedSet: negRn, keyword: { text: n, matchType: "PHRASE" } } } }; });
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  var bads = res.filter(function (x) { return !x.isSuccessful(); });
  say(bads.length ? "!! negative list: " + bads.length + " words refused: " + errs(bads[0]) : "OK  negative list: " + ops.length + " words added");
}

// household income: exclude the lower 70% in every ad group of both campaigns (separate step: never blocks the build)
function addIncome() {
  var names = quoteList([ZIP_CAMPAIGN.name, REST_CAMPAIGN.name]);
  var have = {};
  q("SELECT ad_group.resource_name, ad_group_criterion.income_range.type FROM ad_group_criterion WHERE ad_group_criterion.type = 'INCOME_RANGE' AND campaign.name IN " + names)
    .forEach(function (r) { have[r.adGroup.resourceName + "|" + r.adGroupCriterion.incomeRange.type] = 1; });
  var ops = [];
  q("SELECT ad_group.resource_name FROM ad_group WHERE ad_group.status != 'REMOVED' AND campaign.name IN " + names).forEach(function (r) {
    EXCLUDE_INCOME.forEach(function (t) { if (!have[r.adGroup.resourceName + "|" + t])
      ops.push({ adGroupCriterionOperation: { create: { adGroup: r.adGroup.resourceName, negative: true, incomeRange: { type: t } } } }); });
  });
  if (!ops.length) { say("Income: already set (top 30% + unknown)"); return; }
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  var bads = res.filter(function (x) { return !x.isSuccessful(); });
  if (bads.length) bad("Income exclusions: " + bads.length + " of " + ops.length + " refused. Google said: " + errs(bads[0]) + "  (set it by hand: Audiences > Demographics > Household income)");
  else say("OK  household income: lower 70% excluded in " + (ops.length / EXCLUDE_INCOME.length) + " ad groups (top 30% + unknown still show)");
}

function addLeadForm() {
  var lf = null;
  q("SELECT campaign.name, campaign_asset.asset FROM campaign_asset WHERE campaign_asset.status = 'ENABLED' AND campaign_asset.field_type = 'LEAD_FORM' AND campaign.name = '" + REUSE_FROM + "'")
    .forEach(function (r) { if (!lf) lf = r.campaignAsset.asset; });
  if (!lf) { say("Lead form: none to reuse, skipped (campaigns run without it)"); return; }
  var ops = [];
  q("SELECT campaign.resource_name FROM campaign WHERE campaign.name IN " + quoteList([ZIP_CAMPAIGN.name, REST_CAMPAIGN.name]))
    .forEach(function (r) { ops.push({ campaignAssetOperation: { create: { campaign: r.campaign.resourceName, asset: lf, fieldType: "LEAD_FORM" } } }); });
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  var bads = res.filter(function (x) { return !x.isSuccessful(); });
  say(bads.length ? "!! lead form not linked: " + errs(bads[0]) : "OK  lead form linked to both campaigns");
}

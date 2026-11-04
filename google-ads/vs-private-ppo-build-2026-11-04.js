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
   sitelinks + callouts, and the existing call asset + English lead form reused from "Self-Employed 1099 - 8 States".
   ZIP list: highest median household income per state (uszipcode / Census ACS data, ZIPs with 8,000+ people). */

var SITE = "https://www.vshealthbenefits.com";
var LANDING = "/private-health-insurance";
var MAX_CPC = 15;
var NEG_LIST = "VS Leads - Negatives (Nov 3)";
var REUSE_FROM = "Self-Employed 1099 - 8 States";   // borrow its call asset + lead form
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
        "health insurance if you make too much money", "health insurance for high income self employed"] },
  { name: "Lower My Premium", p: ["lower-premium", "compare"],
    h: ["Premium Went Up Again?", "Lower Your Premium? Let's See", "Alternatives to High Premiums"],
    k: ["lower my health insurance premium", "how to lower health insurance premium", "lower health insurance premiums",
        "reduce health insurance premium", "health insurance too expensive", "health insurance premiums too high",
        "paying too much for health insurance", "alternative to expensive health insurance",
        "alternatives to expensive health insurance", "my health insurance went up"] },
  { name: "Self-Employed & 1099 - Price", p: ["self-employed", "private-ppo"],
    h: ["Self-Employed? Skip Full Price", "1099 PPO Health Plans", "Private Plans for 1099 Workers"],
    k: ["self employed health insurance too expensive", "1099 health insurance too expensive",
        "lower health insurance premium self employed", "high income self employed health insurance",
        "self employed ppo health insurance", "1099 ppo health insurance", "private health insurance for 1099",
        "private health insurance for self employed family", "self employed family ppo"] }
];
var CAMPAIGN_NEGATIVES = ["cheap", "cheapest", "free", "low cost", "income limit", "income limits", "eligibility",
  "qualify", "employer", "employees", "group health", "small business", "short term", "student", "covered california",
  "medi cal", "what is", "meaning", "definition", "vs hmo", "hmo vs"];
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
  if (!negRn) bad("Shared negative list '" + NEG_LIST + "' not found. Run the Nov 3 Lead Engine build first.");
  var callAsset = null, leadForm = null;
  q("SELECT campaign.name, campaign_asset.asset, campaign_asset.field_type FROM campaign_asset WHERE campaign_asset.status = 'ENABLED' AND campaign.name = '" + REUSE_FROM + "'")
    .forEach(function (r) { var f = r.campaignAsset.fieldType;
      if (f === "CALL" && !callAsset) callAsset = r.campaignAsset.asset;
      if (f === "LEAD_FORM" && !leadForm) leadForm = r.campaignAsset.asset; });
  say("Reusing from '" + REUSE_FROM + "': call asset " + (callAsset ? "yes" : "NOT FOUND") + ", lead form " + (leadForm ? "yes" : "NOT FOUND"));
  if (problems.length) { say("STOPPED: nothing was changed."); return; }

  var todo = [ZIP_CAMPAIGN, REST_CAMPAIGN].filter(function (c) { if (existing[c.name]) { say("Already exists, skipped: " + c.name); return false; } return true; });
  if (!todo.length) { addIncome(); say("DONE. Nothing new to build."); return; }

  // ---- 2. build in ONE all-or-nothing batch
  var ops = [], sl = [], co = [];
  SITELINKS.forEach(function (s) { var rn = T("assets"); sl.push(rn);
    ops.push({ assetOperation: { create: { resourceName: rn, finalUrls: [SITE + s[1]], sitelinkAsset: { linkText: s[0], description1: s[2], description2: s[3] } } } }); });
  CALLOUTS.forEach(function (s) { var rn = T("assets"); co.push(rn); ops.push({ assetOperation: { create: { resourceName: rn, calloutAsset: { calloutText: s } } } }); });

  todo.forEach(function (c) {
    var bRn = T("campaignBudgets"), cRn = T("campaigns");
    ops.push({ campaignBudgetOperation: { create: { resourceName: bRn, name: c.name + " budget", amountMicros: Math.round(c.budget * 1e6), deliveryMethod: "STANDARD", explicitlyShared: false } } });
    ops.push({ campaignOperation: { create: {
      resourceName: cRn, name: c.name, status: c.status, advertisingChannelType: "SEARCH", campaignBudget: bRn,
      networkSettings: { targetGoogleSearch: true, targetSearchNetwork: false, targetContentNetwork: false, targetPartnerSearchNetwork: false },
      geoTargetTypeSetting: { positiveGeoTargetType: "PRESENCE", negativeGeoTargetType: "PRESENCE" },
      targetSpend: { cpcBidCeilingMicros: MAX_CPC * 1e6 },
      finalUrlSuffix: "utm_source=google&utm_medium=cpc&utm_campaign=" + c.slug,
      containsEuPoliticalAdvertising: "DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING"
    } } });
    if (c === ZIP_CAMPAIGN) {
      zips.forEach(function (z) { ops.push({ campaignCriterionOperation: { create: { campaign: cRn, location: { geoTargetConstant: zipRn[z] } } } }); });
    } else {
      ALL8.forEach(function (s) { ops.push({ campaignCriterionOperation: { create: { campaign: cRn, location: { geoTargetConstant: states[s] } } } }); });
      zips.forEach(function (z) { ops.push({ campaignCriterionOperation: { create: { campaign: cRn, negative: true, location: { geoTargetConstant: zipRn[z] } } } }); });
    }
    ops.push({ campaignCriterionOperation: { create: { campaign: cRn, language: { languageConstant: EN } } } });
    CAMPAIGN_NEGATIVES.forEach(function (n) { ops.push({ campaignCriterionOperation: { create: { campaign: cRn, negative: true, keyword: { text: n, matchType: "PHRASE" } } } }); });
    ops.push({ campaignSharedSetOperation: { create: { campaign: cRn, sharedSet: negRn } } });
    if (callAsset) ops.push({ campaignAssetOperation: { create: { campaign: cRn, asset: callAsset, fieldType: "CALL" } } });
    sl.forEach(function (a) { ops.push({ campaignAssetOperation: { create: { campaign: cRn, asset: a, fieldType: "SITELINK" } } }); });
    co.forEach(function (a) { ops.push({ campaignAssetOperation: { create: { campaign: cRn, asset: a, fieldType: "CALLOUT" } } }); });

    GROUPS.forEach(function (g) {
      var gRn = T("adGroups");
      ops.push({ adGroupOperation: { create: { resourceName: gRn, campaign: cRn, name: g.name, status: "ENABLED", type: "SEARCH_STANDARD" } } });
      g.k.forEach(function (w) { ["PHRASE", "EXACT"].forEach(function (mt) {
        ops.push({ adGroupCriterionOperation: { create: { adGroup: gRn, status: "ENABLED", keyword: { text: w, matchType: mt } } } }); }); });
      ops.push({ adGroupAdOperation: { create: { adGroup: gRn, status: "ENABLED", ad: {
        finalUrls: [SITE + LANDING],
        responsiveSearchAd: { headlines: g.h.concat(H).slice(0, 15).map(function (t) { return { text: t }; }),
                              descriptions: D.map(function (t) { return { text: t }; }), path1: g.p[0], path2: g.p[1] } } } } });
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
  todo.forEach(function (c) { say("OK  " + c.name + "  $" + c.budget.toFixed(2) + "/day  " + c.status + "  (" + GROUPS.length + " ad groups, phrase+exact, $" + MAX_CPC + " max CPC)"); });
  if (PREVIEW) { say("Preview: Google checked all " + ops.length + " changes and would accept them."); say("Income exclusions and lead form are added on Run (they need the real ad groups)."); }
  else { addIncome(); addLeadForm(); }

  say(problems.length ? "DONE WITH " + problems.length + " WARNING(S) - see lines starting with !!" : "DONE. No errors.");
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
  q("SELECT campaign_asset.asset FROM campaign_asset WHERE campaign_asset.status = 'ENABLED' AND campaign_asset.field_type = 'LEAD_FORM' AND campaign.name = '" + REUSE_FROM + "'")
    .forEach(function (r) { if (!lf) lf = r.campaignAsset.asset; });
  if (!lf) { say("Lead form: none on '" + REUSE_FROM + "', skipped (campaigns run without it)"); return; }
  var ops = [];
  q("SELECT campaign.resource_name FROM campaign WHERE campaign.name IN " + quoteList([ZIP_CAMPAIGN.name, REST_CAMPAIGN.name]))
    .forEach(function (r) { ops.push({ campaignAssetOperation: { create: { campaign: r.campaign.resourceName, asset: lf, fieldType: "LEAD_FORM" } } }); });
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  var bads = res.filter(function (x) { return !x.isSuccessful(); });
  say(bads.length ? "!! lead form not linked: " + errs(bads[0]) : "OK  lead form linked to both campaigns");
}

/* VS Qualified Leads update (Oct 28 2026). PREVIEW first, then RUN. Safe to re-run.
   1. Trucker Health - OE 2027: Max clicks CPC cap $6 -> $15 (ads were losing almost every auction; 12 impressions/week).
   2. Individual - OE 2027 FL: Max clicks -> Maximize conversions (bid for leads, not cheap clicks).
   3. Negative keywords from the last 30 days of search terms (Medicare, Medicaid plan names, federal/state employee plans,
      big-employer plans, TPAs, Spanish), phrase match, campaign level.
   4. "Phone Call Click" (tap on a phone link) and the empty duplicate "Calls from ads" set to secondary, so bidding
      optimizes for real calls (Calls from ads (1)) and Quote Form Lead.
   Florida-only location targeting is NOT changed (health insurance ad certification is Florida only). Budgets unchanged. */
var TRUCK = "Trucker Health - OE 2027", IND = "Individual - OE 2027 FL", SB = "Small Biz Renewal - 2027";
var TRUCK_CAP = 15;
var NEG = {};
NEG[IND] = ["part b", "medicare premium", "how much is medicare", "medicare part", "freedom health", "aetna better health",
  "healthy florida", "humana com", "guardian benefits", "madrinas", "seguros", "seguro", "mercado de salud",
  "why is health insurance so expensive", "did obama care", "will health insurance go down", "fl blue", "florida blue", "login"];
NEG[SB] = ["fehb", "opm", "pshb", "federal employee", "federal health", "retirees", "state employee", "state of florida employee",
  "walmart", "sam's club", "walgreens", "sodexo", "hca", "baptist health", "orlando health", "meritain", "imagine 360", "ehp",
  "simrp", "simerp", "mec", "mewa", "choice arrangements", "geha", "gravie", "vault health", "oscar for business", "first health",
  "compass rose", "bavvy", "boonbenefits", "psc health", "uppo", "thcs", "meridio", "awa health", "bay bridge", "aptia365",
  "fidelis", "ihc group", "nar health", "united health group", "us health group", "american worker", "new york",
  "long term care", "is it cheaper to get insurance through work", "staff health insurance who", "angle medical", "apex", "axis",
  "medicare", "part b"];
NEG[TRUCK] = ["utba", "part b", "medicare premium"];
var SECONDARY = ["Phone Call Click", "Calls from ads"];

function L(ok, m, r) { Logger.log((ok ? "OK: " : "FAILED: ") + m + (ok || !r ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); }
function q(s) { return AdsApp.search(s); }
function camp(name) { var it = q("SELECT campaign.resource_name, campaign.bidding_strategy_type FROM campaign WHERE campaign.name = '" + name + "' AND campaign.status = 'ENABLED'");
  if (!it.hasNext()) { Logger.log("MISSING " + name); return null; } return it.next().campaign; }

function main() {
  // 1. trucker CPC cap
  var t = camp(TRUCK);
  if (t) { var r1 = AdsApp.mutate({ campaignOperation: { update: { resourceName: t.resourceName, targetSpend: { cpcBidCeilingMicros: TRUCK_CAP * 1e6 } }, updateMask: "targetSpend.cpcBidCeilingMicros" } });
    L(r1.isSuccessful(), TRUCK + ": Max clicks cap $" + TRUCK_CAP, r1); }

  // 2. individual -> maximize conversions
  var ind = camp(IND);
  if (ind) { if (ind.biddingStrategyType === "MAXIMIZE_CONVERSIONS") Logger.log(IND + ": already Maximize conversions");
    else { var r2 = AdsApp.mutate({ campaignOperation: { update: { resourceName: ind.resourceName, maximizeConversions: {} }, updateMask: "maximizeConversions.targetCpaMicros" } });
      if (!r2.isSuccessful()) r2 = AdsApp.mutate({ campaignOperation: { update: { resourceName: ind.resourceName, maximizeConversions: { targetCpaMicros: 0 } }, updateMask: "maximize_conversions.target_cpa_micros" } });
      L(r2.isSuccessful(), IND + ": Maximize conversions", r2); } }

  // 3. negatives
  Object.keys(NEG).forEach(function (name) {
    var c = camp(name); if (!c) return;
    var have = {}, it = q("SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.resource_name = '" + c.resourceName + "' AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'");
    while (it.hasNext()) have[it.next().campaignCriterion.keyword.text.toLowerCase()] = true;
    var ok = 0, fail = [];
    NEG[name].forEach(function (k) { if (have[k]) return;
      var r = AdsApp.mutate({ campaignCriterionOperation: { create: { campaign: c.resourceName, negative: true, keyword: { text: k, matchType: "PHRASE" } } } });
      if (r.isSuccessful()) ok++; else fail.push(k); });
    Logger.log(name + ": negatives added " + ok + (fail.length ? " | failed: " + fail.join(", ") : ""));
  });

  // 4. conversion actions -> secondary
  var it = q("SELECT conversion_action.resource_name, conversion_action.name, conversion_action.primary_for_goal FROM conversion_action WHERE conversion_action.status = 'ENABLED'");
  while (it.hasNext()) { var a = it.next().conversionAction;
    if (SECONDARY.indexOf(a.name) < 0) { Logger.log("Conversion kept as is: " + a.name + " (primary " + a.primaryForGoal + ")"); continue; }
    if (!a.primaryForGoal) { Logger.log("Already secondary: " + a.name); continue; }
    var r4 = AdsApp.mutate({ conversionActionOperation: { update: { resourceName: a.resourceName, primaryForGoal: false }, updateMask: "primaryForGoal" } });
    L(r4.isSuccessful(), "Conversion '" + a.name + "' -> secondary", r4); }
  Logger.log("DONE");
}

/* VS Lead Engine - HOURLY (Nov 3 2026).  Schedule: Hourly.  Safe to run any time.
   1. Call-only ads run only while someone can answer (Mon-Fri 8am-6pm, Sat-Sun 8am-1pm,
      account time zone). Outside those hours they pause, so no call rings out unanswered.
   2. Daily at 9am: once the 5 campaigns together pass 15 leads, switch them from
      "Maximize clicks ($15 cap)" to "Maximize conversions".
   3. Mondays at 9am: upload last 90 days of SOLD leads (from the admin portal, via
      /api/ads-sold) as "Sold Policy" conversions, so Google learns which clicks become customers.
   Preview runs all three in test mode and changes nothing. */

var SITE = "https://www.vshealthbenefits.com";
var SECRET = "PASTE_THE_SAME_SECRET_AS_THE_VS_ADS_SYNC_SCRIPT";   // = ADS_SYNC_SECRET in Vercel
var CAMPAIGNS = ["Trucker - FL & GA", "Trucker - TX, IL & OH", "Trucker - KY, MO & MD",
                 "Self-Employed 1099 - 8 States", "Spanish - Camioneros e Independientes"];
var START = "2026-11-03";          // count leads from the day the campaigns launched
var LEADS_TO_SWITCH = 15;
var OPEN = { 1: [8, 18], 2: [8, 18], 3: [8, 18], 4: [8, 18], 5: [8, 18], 6: [8, 13], 7: [8, 13] };  // ISO day: [from, to)

function q(gaql) { var out = [], it = AdsApp.search(gaql); while (it.hasNext()) out.push(it.next()); return out; }
function inList() { return "(" + CAMPAIGNS.map(function (c) { return "'" + c.replace(/'/g, "\\'") + "'"; }).join(", ") + ")"; }

function main() {
  var preview = AdsApp.getExecutionInfo().isPreview();
  var tz = AdsApp.currentAccount().getTimeZone();
  var now = new Date();
  var day = Number(Utilities.formatDate(now, tz, "u")), hour = Number(Utilities.formatDate(now, tz, "H"));
  Logger.log((preview ? "PREVIEW " : "") + "Now: day " + day + ", " + hour + ":00 (" + tz + ")");

  callAdHours(day, hour);
  if (hour === 9 || preview) switchBidding(tz);
  if ((day === 1 && hour === 9) || preview) uploadSold(preview);
}

function callAdHours(day, hour) {
  var w = OPEN[day], open = hour >= w[0] && hour < w[1];
  var want = open ? "ENABLED" : "PAUSED", ops = [];
  q("SELECT ad_group_ad.resource_name, ad_group_ad.status FROM ad_group_ad WHERE campaign.name IN " + inList() +
    " AND ad_group_ad.ad.type = 'CALL_AD' AND ad_group_ad.status IN ('ENABLED', 'PAUSED')")
    .forEach(function (r) { if (r.adGroupAd.status !== want) ops.push({ adGroupAdOperation: { update: { resourceName: r.adGroupAd.resourceName, status: want }, updateMask: "status" } }); });
  if (ops.length) {
    var res = AdsApp.mutateAll(ops, { partialFailure: true });
    Logger.log("Call-only ads: " + (open ? "turned ON " : "paused ") + res.filter(function (r) { return r.isSuccessful(); }).length + " (" + (open ? "staffed hours" : "after hours") + ")");
  } else Logger.log("Call-only ads: already " + (open ? "on" : "paused"));
}

function switchBidding(tz) {
  var today = Utilities.formatDate(new Date(), tz, "yyyy-MM-dd");
  var total = 0;
  q("SELECT metrics.conversions FROM campaign WHERE campaign.name IN " + inList() + " AND segments.date BETWEEN '" + START + "' AND '" + today + "'")
    .forEach(function (r) { total += Number(r.metrics.conversions) || 0; });
  Logger.log("Leads so far across the 5 campaigns: " + total.toFixed(1) + " (switch at " + LEADS_TO_SWITCH + ")");
  if (total < LEADS_TO_SWITCH) return;
  var ops = [];
  q("SELECT campaign.resource_name, campaign.name, campaign.bidding_strategy_type FROM campaign WHERE campaign.name IN " + inList())
    .forEach(function (r) { if (r.campaign.biddingStrategyType === "TARGET_SPEND")
      ops.push({ campaignOperation: { update: { resourceName: r.campaign.resourceName, maximizeConversions: {} }, updateMask: "maximize_conversions" } }); });
  if (!ops.length) { Logger.log("Bidding: already on Maximize conversions"); return; }
  var res = AdsApp.mutateAll(ops, { partialFailure: true });
  res.forEach(function (r) { Logger.log(r.isSuccessful() ? "Bidding: switched to Maximize conversions" : "!! bidding not switched: " + r.getErrorMessages().join(" | ")); });
}

function uploadSold(preview) {
  if (/^PASTE/.test(SECRET)) { Logger.log("!! Sold upload skipped: paste the secret at the top of this script"); return; }
  var resp = UrlFetchApp.fetch(SITE + "/api/ads-sold", { method: "post", contentType: "application/json",
    payload: JSON.stringify({ secret: SECRET }), muteHttpExceptions: true });
  if (resp.getResponseCode() !== 200) { Logger.log("!! Sold upload: site answered " + resp.getResponseCode() + " " + resp.getContentText().slice(0, 200)); return; }
  var rows = (JSON.parse(resp.getContentText()).rows) || [];
  Logger.log("Sold leads from Google Ads clicks (last 90 days): " + rows.length);
  if (!rows.length) return;
  var up = AdsApp.bulkUploads().newCsvUpload(["Google Click ID", "Conversion Name", "Conversion Time", "Conversion Value", "Conversion Currency"],
    { moneyInMicros: false }).forOfflineConversions().setFileName("VS sold policies " + new Date().toISOString().slice(0, 10));
  rows.forEach(function (r) { up.append({ "Google Click ID": r.gclid, "Conversion Name": "Sold Policy", "Conversion Time": r.time,
    "Conversion Value": r.value || 50, "Conversion Currency": "USD" }); });
  if (preview) { up.preview(); Logger.log("Sold upload previewed (" + rows.length + " rows). Google rejects repeats on its own, so weekly re-sends are safe."); }
  else { up.apply(); Logger.log("Sold upload sent: " + rows.length + " rows. Results: Tools > Bulk actions > Uploads."); }
}

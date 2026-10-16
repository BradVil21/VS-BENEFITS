/* =====================================================================
   VS Health Benefits: Google Ads -> Admin Portal sync  (Google Ads Script)

   Paste this whole file into Google Ads:
     Tools -> Bulk actions -> Scripts -> (+) New script
   Replace PASTE_SECRET_HERE with the same value you set as ADS_SYNC_SECRET
   in Vercel. Authorize, click Preview once, then set Frequency: Hourly.

   It reads the last 60 days of performance (read-only, it never changes the
   account) and posts a snapshot to /api/ads-sync, which saves it where the
   admin portal's "Google Ads" tab reads it live.
   ===================================================================== */
var ENDPOINT = "https://www.vshealthbenefits.com/api/ads-sync";
var SECRET = "PASTE_SECRET_HERE";
var DAYS = 60;

function main() {
  var acct = AdsApp.currentAccount();
  var tz = acct.getTimeZone();
  function day(n) { return Utilities.formatDate(new Date(Date.now() - n * 864e5), tz, "yyyy-MM-dd"); }
  var end = day(0), start = day(DAYS - 1), start30 = day(29);
  function q(gaql) {
    var out = [];
    try { var it = AdsApp.search(gaql); while (it.hasNext()) out.push(it.next()); }
    catch (e) { Logger.log("Query failed: " + e + "\n" + gaql); }
    return out;
  }
  function m(r) {
    var x = r.metrics || {};
    return { imp: +x.impressions || 0, clk: +x.clicks || 0,
             cost: Math.round((+x.costMicros || 0) / 1e4) / 100,
             conv: Math.round((+x.conversions || 0) * 100) / 100 };
  }
  function put(o, r) { var v = m(r); for (var k in v) o[k] = v[k]; return o; }
  var DATE30 = "segments.date BETWEEN '" + start30 + "' AND '" + end + "'";
  var MET = "metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions";

  var daily = q("SELECT segments.date, campaign.name, " + MET + " FROM campaign WHERE segments.date BETWEEN '" + start + "' AND '" + end + "' AND metrics.impressions > 0")
    .map(function (r) { return put({ d: r.segments.date, c: r.campaign.name }, r); });

  var campaigns = q("SELECT campaign.name, campaign.status, campaign.primary_status, campaign.primary_status_reasons, campaign.bidding_strategy_type, campaign_budget.amount_micros, " + MET +
                    " FROM campaign WHERE " + DATE30 + " AND campaign.status != 'REMOVED'")
    .map(function (r) { var c = r.campaign;
      return put({ name: c.name, status: c.status, primary: c.primaryStatus || "", reasons: (c.primaryStatusReasons || []).join(", "),
                   bidding: c.biddingStrategyType || "", budget: Math.round(((r.campaignBudget || {}).amountMicros || 0) / 1e4) / 100 }, r); });

  var adGroups = q("SELECT campaign.name, ad_group.name, ad_group.status, " + MET + " FROM ad_group WHERE " + DATE30 + " AND ad_group.status != 'REMOVED'")
    .map(function (r) { return put({ c: r.campaign.name, g: r.adGroup.name, status: r.adGroup.status }, r); });

  var keywords = q("SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.quality_info.quality_score, " + MET +
                   " FROM keyword_view WHERE " + DATE30 + " AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC LIMIT 80")
    .map(function (r) { var k = r.adGroupCriterion || {};
      return put({ c: r.campaign.name, g: r.adGroup.name, kw: (k.keyword || {}).text || "", mt: (k.keyword || {}).matchType || "",
                   qs: (k.qualityInfo || {}).qualityScore || null }, r); });

  var terms = q("SELECT campaign.name, ad_group.name, search_term_view.search_term, " + MET +
                " FROM search_term_view WHERE " + DATE30 + " AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC LIMIT 120")
    .map(function (r) { return put({ c: r.campaign.name, g: r.adGroup.name, term: r.searchTermView.searchTerm }, r); });

  var hourMap = {}, devMap = {};
  q("SELECT segments.hour, " + MET + " FROM campaign WHERE " + DATE30).forEach(function (r) {
    var h = r.segments.hour, o = hourMap[h] || (hourMap[h] = { h: +h, imp: 0, clk: 0, cost: 0, conv: 0 }), v = m(r);
    o.imp += v.imp; o.clk += v.clk; o.cost += v.cost; o.conv += v.conv; });
  q("SELECT segments.device, " + MET + " FROM campaign WHERE " + DATE30).forEach(function (r) {
    var d = r.segments.device, o = devMap[d] || (devMap[d] = { dev: d, imp: 0, clk: 0, cost: 0, conv: 0 }), v = m(r);
    o.imp += v.imp; o.clk += v.clk; o.cost += v.cost; o.conv += v.conv; });

  var disapproved = q("SELECT ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED' AND ad_group_ad.policy_summary.approval_status = 'DISAPPROVED'").length;
  var limited = q("SELECT ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED' AND ad_group_ad.policy_summary.approval_status = 'APPROVED_LIMITED'").length;

  var body = {
    secret: SECRET,
    snapshot: {
      account: { name: acct.getName(), id: acct.getCustomerId(), currency: acct.getCurrencyCode(), tz: tz },
      range: { start: start, end: end },
      daily: daily, campaigns: campaigns, adGroups: adGroups, keywords: keywords, terms: terms,
      hours: Object.keys(hourMap).map(function (k) { return hourMap[k]; }),
      devices: Object.keys(devMap).map(function (k) { return devMap[k]; }),
      policy: { disapproved: disapproved, limited: limited }
    }
  };
  var res = UrlFetchApp.fetch(ENDPOINT, { method: "post", contentType: "application/json", payload: JSON.stringify(body), muteHttpExceptions: true });
  Logger.log("Sync " + res.getResponseCode() + ": " + res.getContentText().slice(0, 300) +
             " | " + daily.length + " daily rows, " + campaigns.length + " campaigns, " + terms.length + " search terms");
}

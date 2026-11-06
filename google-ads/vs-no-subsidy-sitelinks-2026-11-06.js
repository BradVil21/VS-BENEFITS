/* VS No Subsidy Sitelinks + Quote Form URLs (Nov 6 2026).  PREVIEW first, then RUN.  Safe to re-run.
   1. Every ad in the no-subsidy campaigns lands on the quote form (no ZIP, no from=):
        https://www.vshealthbenefits.com/quote?type=individual&niche=private   (utm_* tags kept)
      Campaigns: Private Health - No Subsidy FL (live), No Subsidy - High Earners (Top ZIPs) / (8 States) (paused, stay paused).
   2. Adds 6 sitelinks + 5 callouts to "Private Health - No Subsidy FL", and the call asset if the account has none. */
var LIVE = "Private Health - No Subsidy FL";
var CAMPS = [LIVE, "No Subsidy - High Earners (Top ZIPs)", "No Subsidy - High Earners (8 States)"];
var BASE = "https://www.vshealthbenefits.com/quote?type=individual&niche=private";
var P = "https://www.vshealthbenefits.com/private-health-insurance";
var SITELINKS = [
  ["Get a Free Quote", BASE, "Takes about 2 minutes", "Licensed advisor, no fee to you"],
  ["Private vs Marketplace", P + "#compare", "See the difference side by side", "Know the trade-offs first"],
  ["Watch: Full-Price Costs", P + "#full-price-video", "Real Marketplace quote, no subsidy", "See what full price looks like"],
  ["Who Private Plans Fit", P + "#who-its-for", "Healthy, self-employed, high income", "And who should stay on ACA"],
  ["How It Works", P + "#how-it-works", "Answer a few questions, compare", "Apply any month of the year"],
  ["Self-Employed Plans", "https://www.vshealthbenefits.com/self-employed-health-insurance", "1099 workers and business owners", "Compare private PPO options"]];
var CALLOUTS = ["No Fee to You", "Licensed Advisor", "Apply Any Month", "PPO Networks", "Free Quote"];
function q(s) { var o = [], it = AdsApp.search(s); while (it.hasNext()) o.push(it.next()); return o; }
function L(m) { Logger.log(m); }
function mut(op, label) { var r = AdsApp.mutate(op); var ok = r.isSuccessful(); L((ok ? "OK: " : "FAILED: ") + label + (ok ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); return ok ? (r.getResourceName() || true) : null; }
function keepUtm(url) { var i = url.indexOf("?"); if (i < 0) return ""; return url.slice(i + 1).split("&").filter(function (p) { return /^utm_/i.test(p); }).join("&"); }
function main() {
  L(AdsApp.getExecutionInfo().isPreview() ? "PREVIEW (nothing is saved)" : "RUN");
  var bad = [];
  SITELINKS.forEach(function (s) { if (s[0].length > 25) bad.push(s[0]); if (s[2].length > 35) bad.push(s[2]); if (s[3].length > 35) bad.push(s[3]); });
  CALLOUTS.forEach(function (c) { if (c.length > 25) bad.push(c); });
  if (bad.length) { L("TOO LONG, nothing changed: " + bad.join(" | ")); return; }
  var live = null;
  CAMPS.forEach(function (name) {
    var c = q("SELECT campaign.resource_name, campaign.status FROM campaign WHERE campaign.name = '" + name + "' AND campaign.status != 'REMOVED'");
    if (!c.length) { L("not found: " + name); return; }
    var crn = c[0].campaign.resourceName; if (name === LIVE) live = crn;
    L("== " + name + " (" + c[0].campaign.status + ")");
    q("SELECT campaign.resource_name, ad_group.name, ad_group_ad.ad.resource_name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.ad.final_url_suffix FROM ad_group_ad WHERE campaign.resource_name = '" + crn + "' AND ad_group_ad.status != 'REMOVED'").forEach(function (r) {
      var ad = r.adGroupAd.ad, old = (ad.finalUrls || [])[0] || "", u = keepUtm(old), nu = BASE + (u ? "&" + u : "");
      var upd = { resourceName: ad.resourceName }, mask = [];
      if (old !== nu) { upd.finalUrls = [nu]; mask.push("final_urls"); }
      if (/zip=|from=/i.test(ad.finalUrlSuffix || "")) { upd.finalUrlSuffix = String(ad.finalUrlSuffix).split("&").filter(function (p) { return !/^(zip|from)=/i.test(p); }).join("&"); mask.push("final_url_suffix"); }
      if (!mask.length) { L("  ok already: " + r.adGroup.name + " " + ad.id); return; }
      mut({ adOperation: { update: upd, updateMask: mask.join(",") } }, "  " + r.adGroup.name + " " + ad.id + ": " + old.replace("https://www.vshealthbenefits.com", "") + " -> quote form");
    });
  });
  if (!live) return;
  var C = "campaign.resource_name = '" + live + "'";
  var have = {};
  q("SELECT campaign.resource_name, campaign_asset.field_type, asset.sitelink_asset.link_text, asset.callout_asset.callout_text FROM campaign_asset WHERE " + C + " AND campaign_asset.status = 'ENABLED'").forEach(function (r) {
    if (r.asset.sitelinkAsset) have["S:" + r.asset.sitelinkAsset.linkText] = 1; if (r.asset.calloutAsset) have["C:" + r.asset.calloutAsset.calloutText] = 1; if (r.campaignAsset.fieldType === "CALL") have.CALL = 1; });
  SITELINKS.forEach(function (s) {
    if (have["S:" + s[0]]) { L("sitelink already on: " + s[0]); return; }
    var a = mut({ assetOperation: { create: { finalUrls: [s[1]], sitelinkAsset: { linkText: s[0], description1: s[2], description2: s[3] } } } }, "sitelink asset " + s[0]);
    if (a && a !== true) mut({ campaignAssetOperation: { create: { campaign: live, asset: a, fieldType: "SITELINK" } } }, "  linked to campaign");
  });
  CALLOUTS.forEach(function (t) {
    if (have["C:" + t]) { L("callout already on: " + t); return; }
    var a = mut({ assetOperation: { create: { calloutAsset: { calloutText: t } } } }, "callout " + t);
    if (a && a !== true) mut({ campaignAssetOperation: { create: { campaign: live, asset: a, fieldType: "CALLOUT" } } }, "  linked to campaign");
  });
  var acct = q("SELECT customer_asset.field_type FROM customer_asset WHERE customer_asset.field_type = 'CALL' AND customer_asset.status = 'ENABLED'").length;
  if (have.CALL || acct) { L("call button: " + (have.CALL ? "on campaign" : "account-level call asset applies")); return; }
  var call = q("SELECT asset.resource_name FROM campaign_asset WHERE campaign_asset.field_type = 'CALL' AND campaign_asset.status = 'ENABLED' LIMIT 1");
  if (call.length) mut({ campaignAssetOperation: { create: { campaign: live, asset: call[0].asset.resourceName, fieldType: "CALL" } } }, "call asset linked (same number as trucker)");
  else L("no call asset found anywhere in the account");
  L("DONE");
}

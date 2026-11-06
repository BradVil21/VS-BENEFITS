/* VS Trucker Ads -> Quote Form (Nov 6 2026).  PREVIEW first, then RUN.  Safe to re-run.
   Every ad in "Trucker Health - OE 2027" lands on the short quote form:
     https://www.vshealthbenefits.com/quote?type=individual&niche=trucking
   No hardcoded ZIP (any zip= is dropped everywhere: ads, sitelinks, URL suffixes). utm_* tags on the old URL are kept. */
var CAMP = "Trucker Health - OE 2027";
var BASE = "https://www.vshealthbenefits.com/quote?type=individual&niche=trucking";
function q(s) { var o = [], it = AdsApp.search(s); while (it.hasNext()) o.push(it.next()); return o; }
function L(m) { Logger.log(m); }
function mut(op, label) { var r = AdsApp.mutate(op); L((r.isSuccessful() ? "OK: " : "FAILED: ") + label + (r.isSuccessful() ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); return r.isSuccessful(); }
function keepUtm(url) { var i = url.indexOf("?"); if (i < 0) return ""; return url.slice(i + 1).split("&").filter(function (p) { return /^utm_/i.test(p); }).join("&"); }
function noZip(s) { return String(s || "").replace(/([?&])zip=\d*&?/gi, "$1").replace(/[?&]$/, ""); }
function main() {
  L(AdsApp.getExecutionInfo().isPreview() ? "PREVIEW (nothing is saved)" : "RUN");
  var c = q("SELECT campaign.resource_name, campaign.final_url_suffix, campaign.tracking_url_template FROM campaign WHERE campaign.name = '" + CAMP + "'");
  if (!c.length) { L("MISSING " + CAMP); return; }
  var crn = c[0].campaign.resourceName, C = "campaign.resource_name = '" + crn + "'";
  var sfx = c[0].campaign.finalUrlSuffix || "";
  L("Campaign URL suffix: '" + sfx + "' | tracking template: '" + (c[0].campaign.trackingUrlTemplate || "") + "'");
  if (/zip=/i.test(sfx)) mut({ campaignOperation: { update: { resourceName: crn, finalUrlSuffix: noZip(sfx) }, updateMask: "final_url_suffix" } }, "removed zip from campaign URL suffix");
  q("SELECT ad_group.resource_name, ad_group.name, ad_group.final_url_suffix FROM ad_group WHERE " + C + " AND ad_group.status != 'REMOVED'").forEach(function (g) {
    if (/zip=/i.test(g.adGroup.finalUrlSuffix || "")) mut({ adGroupOperation: { update: { resourceName: g.adGroup.resourceName, finalUrlSuffix: noZip(g.adGroup.finalUrlSuffix) }, updateMask: "final_url_suffix" } }, "removed zip from ad group suffix " + g.adGroup.name);
  });
  // ads
  var n = 0;
  q("SELECT ad_group.name, ad_group_ad.status, ad_group_ad.ad.resource_name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ad_group_ad.ad.final_url_suffix FROM ad_group_ad WHERE " + C + " AND ad_group_ad.status != 'REMOVED' AND ad_group.status != 'REMOVED'").forEach(function (r) {
    var ad = r.adGroupAd.ad, old = (ad.finalUrls || [])[0] || "", u = keepUtm(old), nu = (/type=business/i.test(old) ? BASE.replace("type=individual", "type=business") : BASE) + (u ? "&" + u : "");
    L("AD " + r.adGroup.name + " " + ad.id + " [" + r.adGroupAd.status + "] " + old.replace("https://www.vshealthbenefits.com", "") + " -> " + nu.replace("https://www.vshealthbenefits.com", ""));
    var upd = { resourceName: ad.resourceName }, mask = [];
    if (old !== nu) { upd.finalUrls = [nu]; mask.push("final_urls"); }
    if (/zip=/i.test(ad.finalUrlSuffix || "")) { upd.finalUrlSuffix = noZip(ad.finalUrlSuffix); mask.push("final_url_suffix"); }
    if (mask.length && mut({ adOperation: { update: upd, updateMask: mask.join(",") } }, "ad " + ad.id + " -> quote form")) n++;
  });
  L("Ads updated: " + n);
  // sitelinks / assets with a hardcoded zip
  q("SELECT campaign.resource_name, asset.resource_name, asset.final_urls, asset.sitelink_asset.link_text, campaign_asset.field_type FROM campaign_asset WHERE " + C + " AND campaign_asset.status = 'ENABLED'").forEach(function (r) {
    var urls = r.asset.finalUrls || []; if (!urls.length) return;
    L("ASSET " + r.campaignAsset.fieldType + " '" + ((r.asset.sitelinkAsset || {}).linkText || "") + "' " + urls[0].replace("https://www.vshealthbenefits.com", ""));
    if (/\/(trucking-health-quote|truckers\/quote)(\?|$)/.test(urls[0])) { mut({ assetOperation: { update: { resourceName: r.asset.resourceName, finalUrls: [BASE] }, updateMask: "final_urls" } }, "quote sitelink -> quote form: " + ((r.asset.sitelinkAsset || {}).linkText || "")); return; }
    if (urls.some(function (x) { return /zip=/i.test(x); }))
      mut({ assetOperation: { update: { resourceName: r.asset.resourceName, finalUrls: urls.map(noZip) }, updateMask: "final_urls" } }, "removed zip from asset " + ((r.asset.sitelinkAsset || {}).linkText || r.asset.resourceName));
  });
  L("DONE");
}

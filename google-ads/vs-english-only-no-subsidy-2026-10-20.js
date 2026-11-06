/* VS Ads Update (Oct 20 2026, evening): English only + individuals with no subsidy who are overpaying.
   Paste into Google Ads → Tools → Bulk actions → Scripts → (+). Click PREVIEW first and read the log.
   Preview changes nothing. Then RUN. Safe to re-run: anything already done is skipped.

   1. SPANISH OFF, every campaign
      - Spanish ad groups paused (name contains "Spanish"/"Español", or ads point to /truckers/cotizar, /seguro-...).
      - Spanish keywords in English ad groups paused (e.g. "calculadora de subsidio obamacare").
      - Spanish language targeting removed from every campaign (English stays).
      - Spanish callouts / sitelinks / snippets ("English y Español") unlinked from campaigns and the account.
      - Every live English ad that has a Spanish line ("Se Habla Español", "English y Español",
        "Calculadora de Subsidio") gets a clean English copy; the old ad is paused only after the new one saves.
   2. NO SUBSIDY / OVERPAYING ("Individual - OE 2027 FL")
      - Makes sure the "Overpaying / No Subsidy" ad group exists and is ON, with an English ad and all keywords.
      - If it (or the older "No Subsidy / Over Income" group) already exists: turns it on and adds any missing keywords.

   Nothing is deleted. To delete Spanish ad groups instead of pausing, set REMOVE_SPANISH_GROUPS = true
   (removed ad groups can't be turned back on). */

var REMOVE_SPANISH_GROUPS = false;
var SITE = "https://www.vshealthbenefits.com";
var IND = "Individual - OE 2027 FL";
var OV_GROUP = "Overpaying / No Subsidy";
var OLD_NS_GROUP = "No Subsidy / Over Income";

var OV_H = ["Paying Too Much for Coverage?", "No Subsidy? Compare Plans", "Over the Subsidy Cliff?", "Lower Your Full-Price Premium",
  "Too Much Income for Subsidy?", "2027 Premium Went Up?", "Don't Auto-Renew the Increase", "Private & Marketplace Plans",
  "Self-Employed, High Income?", "HSA Plans Can Cut Your Cost", "Compare Every Carrier Free", "Licensed FL Health Broker",
  "Plans for Ages 50-64", "Enroll by Dec 15 for Jan 1", "Talk to a Licensed Advisor"];
var OV_D = ["Earn too much for a subsidy in 2027? We find your lowest full-price plan, free.",
  "Premium went up? We compare every plan in your area before you auto-renew for 2027.",
  "Self-employed? HSA plans and the premium deduction can lower what you really pay.",
  "Licensed Florida broker. Carriers pay us, not you. Same price as buying direct."];
var OV_K = ["health insurance too expensive", "lower health insurance premium", "health insurance premiums too high",
  "paying too much for health insurance", "health insurance for high income earners", "best health insurance for self employed florida",
  "hsa health insurance florida", "health insurance cost without subsidy", "cheaper health insurance florida",
  "health insurance over 1000 a month", "health insurance without subsidy", "no subsidy health insurance",
  "too much income for obamacare", "make too much for obamacare", "health insurance over 400 poverty level",
  "unsubsidized health insurance", "health insurance for high income self employed", "health insurance went up 2027",
  "health insurance premium increase 2027"];
var OV_PATH = ["health-plans", "full-price"];

// Spanish detector: accents, common Spanish words, Spanish landing pages.
var ES_RE = /[áéíóúñ¿¡]|espa[nñ]ol|\bseguro\b|cotiza|camioner|traileros|choferes|inscr[ií]b|hablamos|calculadora|\bm[eé]dicos?\b|\bagente\b|\bplanes\b|subsidio|\bprimas?\b|sin costo|\bayuda\b|\bpara\b|\busted\b/i;
var ES_URL = /cotizar|seguro-|examen-medico|inscripcion|\/es\//i;
var H_FILL = ["Licensed FL Health Broker", "Free Quote, No Obligation", "Talk to a Licensed Advisor", "Compare Every Carrier Free"];
var D_FILL = ["A licensed advisor compares your options free. Carriers pay us, not you.",
  "Same price as buying direct, with free help all year from a licensed advisor."];

var CHANGES = 0;
function log(ok, msg, r) { if (ok) CHANGES++; Logger.log((ok ? "OK: " : "FAILED: ") + msg + (ok || !r ? "" : " " + r.getErrorMessages().slice(0, 3).join("; "))); }
function isEs(t) { return !!t && ES_RE.test(t); }
function q(s) { return String(s).replace(/'/g, "\\'"); }

// Strip the bilingual phrase out of an English sentence, then drop anything still Spanish.
function cleanDesc(t) {
  var x = t.replace(/,?\s*English (y|and) Espa[nñ]ol\.?/ig, function (m) { return (m.charAt(0) === "," && m.slice(-1) === ".") ? "." : ""; })
           .replace(/\s+\./g, ".").replace(/\s{2,}/g, " ").replace(/^\s+|\s+$/g, "");
  if (x && !/[.!?]$/.test(x)) x += ".";
  if (/^,|^\./.test(x)) x = x.replace(/^[,.]\s*/, "");
  return isEs(x) || x.length < 15 ? null : x;
}
function cleanAd(h, d) {
  var hs = [], seen = {};
  h.forEach(function (o) { var k = o.text.toLowerCase(); if (!isEs(o.text) && !seen[k]) { seen[k] = 1; hs.push(o.pinnedField ? { text: o.text, pinnedField: o.pinnedField } : { text: o.text }); } });
  H_FILL.forEach(function (t) { if (hs.length < 3 && !seen[t.toLowerCase()]) { seen[t.toLowerCase()] = 1; hs.push({ text: t }); } });
  var ds = [], dseen = {};
  d.forEach(function (o) { var c = cleanDesc(o.text); if (c && c.length <= 90 && !dseen[c]) { dseen[c] = 1; ds.push(o.pinnedField ? { text: c, pinnedField: o.pinnedField } : { text: c }); } });
  D_FILL.forEach(function (t) { if (ds.length < 2 && !dseen[t]) { dseen[t] = 1; ds.push({ text: t }); } });
  return { h: hs, d: ds };
}

function main() {
  var bad = [];
  OV_H.forEach(function (x) { if (x.length > 30) bad.push("H " + x + " (" + x.length + ")"); if (isEs(x)) bad.push("ES " + x); });
  OV_D.forEach(function (x) { if (x.length > 90) bad.push("D " + x + " (" + x.length + ")"); if (isEs(x)) bad.push("ES " + x); });
  H_FILL.concat(D_FILL).forEach(function (x) { if (isEs(x)) bad.push("ES " + x); });
  if (bad.length) { Logger.log("COPY ERRORS:\n" + bad.join("\n")); return; }

  var cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, "");
  var camps = {}, it = AdsApp.search("SELECT campaign.resource_name, campaign.name, campaign.status FROM campaign WHERE campaign.status != 'REMOVED'");
  while (it.hasNext()) { var c = it.next().campaign; camps[c.name] = { rn: c.resourceName, status: c.status }; }
  Logger.log("Campaigns: " + Object.keys(camps).map(function (n) { return n + " [" + camps[n].status + "]"; }).join(" | "));

  // ---------- 1a. Spanish ad groups ----------
  var esUrlGroups = {};
  it = AdsApp.search("SELECT ad_group.resource_name, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE ad_group_ad.status != 'REMOVED' AND ad_group.status != 'REMOVED'");
  while (it.hasNext()) { var r = it.next(); if ((r.adGroupAd.ad.finalUrls || []).some(function (u) { return ES_URL.test(u); })) esUrlGroups[r.adGroup.resourceName] = true; }
  var esGroups = {};
  it = AdsApp.search("SELECT campaign.name, ad_group.resource_name, ad_group.name, ad_group.status FROM ad_group WHERE ad_group.status != 'REMOVED' AND campaign.status != 'REMOVED'");
  while (it.hasNext()) { var g = it.next();
    var es = /spanish|espa[nñ]ol/i.test(g.adGroup.name) || isEs(g.adGroup.name) || esUrlGroups[g.adGroup.resourceName];
    if (!es) continue;
    esGroups[g.adGroup.resourceName] = true;
    var label = g.campaign.name + " > " + g.adGroup.name;
    if (REMOVE_SPANISH_GROUPS) { var rr = AdsApp.mutate({ adGroupOperation: { remove: g.adGroup.resourceName } }); log(rr.isSuccessful(), "removed Spanish ad group " + label, rr); }
    else if (g.adGroup.status === "PAUSED") Logger.log("Already paused: " + label);
    else { var pr = AdsApp.mutate({ adGroupOperation: { update: { resourceName: g.adGroup.resourceName, status: "PAUSED" }, updateMask: "status" } }); log(pr.isSuccessful(), "paused Spanish ad group " + label, pr); }
  }
  if (!Object.keys(esGroups).length) Logger.log("No Spanish ad groups found");

  // ---------- 1b. Spanish keywords inside English ad groups ----------
  it = AdsApp.search("SELECT campaign.name, ad_group.resource_name, ad_group.name, ad_group_criterion.resource_name, ad_group_criterion.keyword.text FROM ad_group_criterion WHERE ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status = 'ENABLED' AND ad_group.status != 'REMOVED' AND campaign.status != 'REMOVED'");
  var kwN = 0;
  while (it.hasNext()) { var k = it.next(); if (esGroups[k.adGroup.resourceName] || !isEs(k.adGroupCriterion.keyword.text)) continue;
    var kr = AdsApp.mutate({ adGroupCriterionOperation: { update: { resourceName: k.adGroupCriterion.resourceName, status: "PAUSED" }, updateMask: "status" } });
    log(kr.isSuccessful(), "paused Spanish keyword \"" + k.adGroupCriterion.keyword.text + "\" (" + k.campaign.name + " > " + k.adGroup.name + ")", kr); kwN++; }
  if (!kwN) Logger.log("No Spanish keywords in English ad groups");

  // ---------- 1c. Spanish language targeting ----------
  it = AdsApp.search("SELECT campaign.name, campaign.resource_name, campaign_criterion.resource_name, campaign_criterion.language.language_constant FROM campaign_criterion WHERE campaign_criterion.type = 'LANGUAGE' AND campaign.status != 'REMOVED'");
  var langs = {};
  while (it.hasNext()) { var l = it.next(); var n = l.campaign.name; langs[n] = langs[n] || { rn: l.campaign.resourceName, en: false, es: [] };
    var lc = l.campaignCriterion.language.languageConstant;
    if (lc === "languageConstants/1000") langs[n].en = true; else if (lc === "languageConstants/1003") langs[n].es.push(l.campaignCriterion.resourceName); }
  Object.keys(langs).forEach(function (n) { var L = langs[n];
    if (!L.es.length) { Logger.log("English only already: " + n); return; }
    if (!L.en) { var ar = AdsApp.mutate({ campaignCriterionOperation: { create: { campaign: L.rn, language: { languageConstant: "languageConstants/1000" } } } }); log(ar.isSuccessful(), "added English targeting: " + n, ar); }
    L.es.forEach(function (rn) { var rr = AdsApp.mutate({ campaignCriterionOperation: { remove: rn } }); log(rr.isSuccessful(), "removed Spanish language targeting: " + n, rr); }); });

  // ---------- 1d. Spanish callouts / sitelinks / snippets ----------
  var AF = "asset.type, asset.callout_asset.callout_text, asset.sitelink_asset.link_text, asset.sitelink_asset.description1, asset.sitelink_asset.description2, asset.structured_snippet_asset.values, asset.final_urls";
  function assetEs(a) { var parts = [];
    if (a.calloutAsset) parts.push(a.calloutAsset.calloutText);
    if (a.sitelinkAsset) parts.push(a.sitelinkAsset.linkText, a.sitelinkAsset.description1, a.sitelinkAsset.description2);
    if (a.structuredSnippetAsset) parts = parts.concat(a.structuredSnippetAsset.values || []);
    return parts.some(isEs) || (a.finalUrls || []).some(function (u) { return ES_URL.test(u); }); }
  function assetLabel(a) { return a.calloutAsset ? a.calloutAsset.calloutText : a.sitelinkAsset ? a.sitelinkAsset.linkText : a.type; }
  var assetN = 0;
  [["campaign_asset", "campaignAssetOperation", "campaignAsset"], ["customer_asset", "customerAssetOperation", "customerAsset"], ["ad_group_asset", "adGroupAssetOperation", "adGroupAsset"]].forEach(function (t) {
    var res;
    try { res = AdsApp.search("SELECT " + t[0] + ".resource_name, " + AF + " FROM " + t[0] + " WHERE " + t[0] + ".status != 'REMOVED' AND asset.type IN ('CALLOUT','SITELINK','STRUCTURED_SNIPPET')"); }
    catch (e) { Logger.log("Could not read " + t[0] + ": " + e); return; }
    while (res.hasNext()) { var row = res.next(); if (!assetEs(row.asset)) continue;
      var op = {}; op[t[1]] = { remove: row[t[2]].resourceName };
      var rr = AdsApp.mutate(op); log(rr.isSuccessful(), "unlinked Spanish " + row.asset.type.toLowerCase() + " \"" + assetLabel(row.asset) + "\" (" + t[0] + ")", rr); assetN++; } });
  if (!assetN) Logger.log("No Spanish callouts/sitelinks/snippets linked");

  // ---------- 1e. Clean copies of English ads with Spanish lines ----------
  it = AdsApp.search("SELECT campaign.name, ad_group.resource_name, ad_group.name, ad_group_ad.resource_name, ad_group_ad.ad.final_urls, ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions, ad_group_ad.ad.responsive_search_ad.path1, ad_group_ad.ad.responsive_search_ad.path2 FROM ad_group_ad WHERE ad_group_ad.status = 'ENABLED' AND ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD' AND ad_group.status != 'REMOVED' AND campaign.status != 'REMOVED'");
  var adN = 0;
  while (it.hasNext()) { var a = it.next(); if (esGroups[a.adGroup.resourceName]) continue;
    var rsa = a.adGroupAd.ad.responsiveSearchAd || {}, H = rsa.headlines || [], D = rsa.descriptions || [];
    if (!H.some(function (o) { return isEs(o.text); }) && !D.some(function (o) { return isEs(o.text); })) continue;
    adN++;
    var label = a.campaign.name + " > " + a.adGroup.name;
    var c2 = cleanAd(H, D);
    var na = { finalUrls: a.adGroupAd.ad.finalUrls, responsiveSearchAd: { headlines: c2.h, descriptions: c2.d } };
    if (rsa.path1) na.responsiveSearchAd.path1 = rsa.path1;
    if (rsa.path2) na.responsiveSearchAd.path2 = rsa.path2;
    var nr = AdsApp.mutate({ adGroupAdOperation: { create: { adGroup: a.adGroup.resourceName, status: "ENABLED", ad: na } } });
    log(nr.isSuccessful(), "English-only copy of ad in " + label + " (" + c2.h.length + " headlines, " + c2.d.length + " descriptions)", nr);
    if (nr.isSuccessful()) { var po = AdsApp.mutate({ adGroupAdOperation: { update: { resourceName: a.adGroupAd.resourceName, status: "PAUSED" }, updateMask: "status" } }); log(po.isSuccessful(), "paused old bilingual ad in " + label, po); }
  }
  if (!adN) Logger.log("No live English ads with Spanish lines");

  // ---------- 2. Overpaying / No Subsidy ----------
  var ind = camps[IND];
  if (!ind) { Logger.log("MISSING campaign " + IND + ": no-subsidy ad group not added"); return finish(); }
  var groups = {};
  it = AdsApp.search("SELECT ad_group.resource_name, ad_group.name, ad_group.status FROM ad_group WHERE campaign.resource_name = '" + q(ind.rn) + "' AND ad_group.status != 'REMOVED'");
  while (it.hasNext()) { var g2 = it.next().adGroup; groups[g2.name] = g2; }
  var targets = [OV_GROUP, OLD_NS_GROUP].filter(function (n) { return groups[n]; });

  if (!targets.length) {
    var ag = "customers/" + cid + "/adGroups/-1";
    var ops = [{ adGroupOperation: { create: { resourceName: ag, name: OV_GROUP, campaign: ind.rn, status: "ENABLED", type: "SEARCH_STANDARD" } } },
      { adGroupAdOperation: { create: { adGroup: ag, status: "ENABLED", ad: { finalUrls: [SITE + "/quote?type=individual"], responsiveSearchAd: {
        headlines: OV_H.map(function (x) { return { text: x }; }), descriptions: OV_D.map(function (x) { return { text: x }; }), path1: OV_PATH[0], path2: OV_PATH[1] } } } } }];
    var res = AdsApp.mutateAll(ops, { partialFailure: false }), errs = [];
    res.forEach(function (r) { if (!r.isSuccessful()) errs = errs.concat(r.getErrorMessages()); });
    log(!errs.length, "created ad group \"" + OV_GROUP + "\" with English ad", errs.length ? { getErrorMessages: function () { return errs; } } : null);
    if (errs.length) return finish();
    var g3 = AdsApp.search("SELECT ad_group.resource_name, ad_group.name, ad_group.status FROM ad_group WHERE campaign.resource_name = '" + q(ind.rn) + "' AND ad_group.name = '" + q(OV_GROUP) + "'");
    if (g3.hasNext()) { groups[OV_GROUP] = g3.next().adGroup; targets = [OV_GROUP]; }
    else { Logger.log("(Preview: the new ad group isn't saved yet, so keywords are listed but not added.) Keywords: " + OV_K.join(", ")); return finish(); }
  }

  targets.forEach(function (n) { var G = groups[n];
    if (G.status !== "ENABLED") { var er = AdsApp.mutate({ adGroupOperation: { update: { resourceName: G.resourceName, status: "ENABLED" }, updateMask: "status" } }); log(er.isSuccessful(), "turned on ad group \"" + n + "\"", er); }
    // make sure it has a live ad
    var live = AdsApp.search("SELECT ad_group_ad.resource_name FROM ad_group_ad WHERE ad_group.resource_name = '" + q(G.resourceName) + "' AND ad_group_ad.status = 'ENABLED'");
    if (!live.hasNext()) { var nr2 = AdsApp.mutate({ adGroupAdOperation: { create: { adGroup: G.resourceName, status: "ENABLED", ad: { finalUrls: [SITE + "/quote?type=individual"], responsiveSearchAd: {
        headlines: OV_H.map(function (x) { return { text: x }; }), descriptions: OV_D.map(function (x) { return { text: x }; }), path1: OV_PATH[0], path2: OV_PATH[1] } } } } });
      log(nr2.isSuccessful(), "added English ad to \"" + n + "\"", nr2); }
    else Logger.log("Has a live ad: " + n);
  });

  // keywords: every OV_K in phrase + exact, in the first target group, unless already anywhere in the campaign
  var have = {};
  it = AdsApp.search("SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status FROM ad_group_criterion WHERE campaign.resource_name = '" + q(ind.rn) + "' AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.negative = FALSE AND ad_group_criterion.status != 'REMOVED' AND ad_group.status != 'REMOVED'");
  while (it.hasNext()) { var kk = it.next().adGroupCriterion; have[kk.keyword.text.toLowerCase() + "|" + kk.keyword.matchType] = true; }
  var home = groups[targets[0]].resourceName, added = 0, rejected = [];
  OV_K.forEach(function (t) { ["PHRASE", "EXACT"].forEach(function (mt) { if (have[t + "|" + mt]) return;
    var r = AdsApp.mutate({ adGroupCriterionOperation: { create: { adGroup: home, status: "ENABLED", keyword: { text: t, matchType: mt } } } });
    if (r.isSuccessful()) { added++; CHANGES++; } else rejected.push(t + " [" + mt + "]"); }); });
  Logger.log("No-subsidy keywords added to \"" + targets[0] + "\": " + added + (rejected.length ? " | rejected: " + rejected.join(", ") : ""));

  // warn (don't change) if a campaign negative would block any of these keywords
  it = AdsApp.search("SELECT campaign_criterion.keyword.text FROM campaign_criterion WHERE campaign.resource_name = '" + q(ind.rn) + "' AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'");
  while (it.hasNext()) { var nt = it.next().campaignCriterion.keyword.text.toLowerCase();
    var blocks = OV_K.filter(function (t) { return (" " + t + " ").indexOf(" " + nt + " ") >= 0; });
    if (blocks.length) Logger.log("WARNING: negative \"" + nt + "\" blocks: " + blocks.join(", ") + " (left as is)"); }

  finish();
}
function finish() { Logger.log("DONE. " + CHANGES + " change(s)" + (AdsApp.getExecutionInfo().isPreview() ? " (PREVIEW: nothing was saved)" : "")); }

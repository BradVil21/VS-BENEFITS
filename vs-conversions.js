/* =====================================================================
   VS CONVERSIONS  (vs-conversions.js)

   Both SEO reviews ended on the same line: "Quote-form starts from
   organic are not currently measurable. Worth wiring before November."
   This is that. Without it, money spent on ads buys traffic you cannot
   grade, which is the same blindness the lead sources had.

   What it measures, on every page:

     phone_click     someone tapped a tel: link. For a broker this is the
                     conversion, not a soft signal - and 160 pages carry a
                     phone number that until now recorded nothing.
     chat_open       someone opened the live chat widget.
     quote_cta       someone clicked through to the quote funnel, tagged
                     with the page that sent them.
     quote_start     they picked individual or business and began.
     quote_step      they finished a step (so you can see WHERE they quit,
                     not just that they did).
     generate_lead   they submitted. Fired by the funnel itself.

   Every event carries the attribution channel from vs-attribution.js, so
   in GA4 you can ask "how many phone clicks did Google Ads produce" -
   which is the question a budget actually turns on.

   ── The one thing you have to paste ──────────────────────────────────
   Google Ads needs a conversion LABEL per action. Get them in
   Google Ads -> Goals -> Conversions -> (your action) -> Tag setup ->
   "Use Google tag". The value looks like  AW-17950389267/AbC-D1efGhIjKl
   Paste ONLY the part after the slash, below. GA4 events fire either way;
   the labels are what lets Google Ads bid on them.
   ===================================================================== */
(function () {
  "use strict";

  var ADS_ID = "AW-17950389267";

  // Paste your labels here. Leave blank and everything still records in
  // GA4 - you just cannot optimise ad bidding on it yet.
  var LABELS = {
    lead:  "",   // "Quote Form Lead"  conversion action
    phone: "",   // "Phone Call Click" conversion action
  };

  // Shared so the quote funnel reads the same values instead of keeping a
  // second copy that drifts out of step with this one.
  window.VS_ADS = { id: ADS_ID, labels: LABELS };

  function attr() {
    try { return (window.vsAttribution && window.vsAttribution()) || null; }
    catch (e) { return null; }
  }

  // gtag only exists once analytics have loaded. On pages where the visitor
  // declined, it never does, and every call here quietly does nothing -
  // which is the correct outcome, not a bug to work around.
  function ga(name, params) {
    try {
      if (typeof window.gtag !== "function") return false;
      var a = attr();
      var p = params || {};
      if (a) {
        p.lead_channel = a.source;
        if (a.utm_campaign) p.campaign = a.utm_campaign;
        p.landing_page = a.landing;
      }
      window.gtag("event", name, p);
      return true;
    } catch (e) { return false; }
  }

  function adsConversion(labelKey, params) {
    try {
      var label = LABELS[labelKey];
      if (!label || label.indexOf("PASTE") === 0) return;
      if (typeof window.gtag !== "function") return;
      var p = params || {};
      p.send_to = ADS_ID + "/" + label;
      window.gtag("event", "conversion", p);
    } catch (e) { /* ignore */ }
  }

  // Public, so the quote funnel can report its own steps through the same
  // pipe rather than inventing a parallel one.
  window.vsTrack = function (name, params) {
    ga(name, params);
    if (name === "generate_lead") adsConversion("lead", { value: 0, currency: "USD" });
    if (name === "phone_click") adsConversion("phone", { value: 0, currency: "USD" });
  };

  // ---- automatic wiring ----
  // One delegated listener rather than binding every link, so it also covers
  // anything added to the page later.
  document.addEventListener("click", function (e) {
    try {
      var path = (e.composedPath && e.composedPath()) || [];

      // The chat widget lives in its own custom element and shadow root, so
      // a normal closest() never sees it. composedPath does.
      for (var i = 0; i < path.length; i++) {
        var tag = path[i] && path[i].tagName;
        if (tag && String(tag).toLowerCase().indexOf("chat-widget") >= 0) {
          if (!window.__vsChatSeen) { window.__vsChatSeen = true; window.vsTrack("chat_open", {}); }
          return;
        }
      }

      var a = e.target && e.target.closest && e.target.closest("a[href]");
      if (!a) return;
      var href = a.getAttribute("href") || "";

      if (href.indexOf("tel:") === 0) {
        window.vsTrack("phone_click", {
          phone_number: href.replace("tel:", ""),
          page: location.pathname,
        });
        return;
      }

      // Clicks INTO the funnel, tagged with the page that produced them, so
      // you can tell which content actually sends people to a form.
      if (/^\/(quote|get-a-quote)(\/|$|\?)/.test(href) || /\/quote(\/|$|\?)/.test(href)) {
        window.vsTrack("quote_cta", { from_page: location.pathname });
      }
    } catch (err) { /* never let tracking break a click */ }
  }, true);
})();

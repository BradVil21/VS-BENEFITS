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
   "Use Google tag". The value looks like  AW-18479284900/AbC-D1efGhIjKl
   Paste ONLY the part after the slash, below. GA4 events fire either way;
   the labels are what lets Google Ads bid on them.
   ===================================================================== */
(function () {
  "use strict";

  var ADS_ID = "AW-18479284900";

  // Paste your labels here. Leave blank and everything still records in
  // GA4 - you just cannot optimise ad bidding on it yet.
  var LABELS = {
    lead:  "CjpNCInIsogdEKSFzutE",   // "Quote Form Lead"  conversion action (VS Health Benefits, 294-975-7547)
    phone: "88yHCI_IsogdEKSFzutE",   // "Phone Call Click" conversion action
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
    // Trucker funnel: the lead reaches the CRM at the phone step, before name/email.
    // Count it there so Google Ads bids on the drivers who actually leave a number.
    // "Quote Form Lead" counts One per click, so the later submit is not double counted.
    if (name === "trucker_quote_partial") adsConversion("lead", { value: 0, currency: "USD" });
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

/* =====================================================================
   MOBILE CALL / QUOTE BAR  (added 2 Oct 2026)

   Mobile visitors rank better and click more often than desktop
   (Search Console: position 29 vs 48, CTR 0.73% vs 0.43%), but only
   the trucking pages had a fixed "Call / Get my quote" bar. This adds
   the same bar to every other public page, on phones only.

   It stays off where it would compete with a form or already exists:
   pages that ship their own bar (#vs-callbar / #vs-sticky), the quote
   funnel, calculators and checkers, and private pages.
   ===================================================================== */
(function () {
  "use strict";
  var PHONE = "+19548251009";
  var SKIP = /^\/(quote|get-a-quote|client|admin|census|book|careers|privacy|terms)(\/|$|\.html)|calculator|checker|plan-finder/;

  function build() {
    try {
      if (SKIP.test(location.pathname)) return;
      if (document.getElementById("vs-callbar") || document.getElementById("vs-sticky")) return;

      var es = (document.documentElement.lang || "").toLowerCase().indexOf("es") === 0;
      // Dental pages send people to the dental funnel, like their own buttons do.
      var dental = /dental|vision/.test(location.pathname) && document.querySelector('a[href^="/quote/dental-vision"]');
      var quoteHref = dental ? dental.getAttribute("href") : "/quote";

      var css = document.createElement("style");
      css.id = "vs-callbar-auto-css";
      css.textContent =
        "#vs-callbar{display:none}" +
        "@media(max-width:759px){" +
        "#vs-callbar{position:fixed;left:0;right:0;bottom:0;z-index:120;display:flex;gap:8px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.97);-webkit-backdrop-filter:saturate(160%) blur(8px);backdrop-filter:saturate(160%) blur(8px);border-top:1px solid #e4e9f2;box-shadow:0 -6px 18px rgba(13,27,42,.10);font-family:Inter,system-ui,-apple-system,sans-serif}" +
        "#vs-callbar a{flex:1;display:flex;align-items:center;justify-content:center;gap:7px;min-height:48px;border-radius:999px;font-weight:700;font-size:.95rem;text-decoration:none;line-height:1.1;color:#fff}" +
        "#vs-callbar .vs-call{background:#098374}#vs-callbar .vs-quote{background:#16447f}" +
        "body.vs-has-callbar{padding-bottom:76px}" +
        "body.vs-has-callbar #back-to-top{bottom:88px}" +
        "body.vs-has-callbar #vsb-launcher{bottom:88px!important}" +
        "body.vs-has-callbar #vsb-window{bottom:160px!important}" +
        "}";
      document.head.appendChild(css);

      var bar = document.createElement("div");
      bar.id = "vs-callbar";
      bar.setAttribute("role", "region");
      bar.setAttribute("aria-label", es ? "Hable con un asesor" : "Contact a licensed advisor");
      bar.innerHTML =
        '<a class="vs-call" href="tel:' + PHONE + '" data-vs-cta="sticky-call">' +
        '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.3 2.2z"/></svg>' +
        (es ? "Llamar" : "Call an advisor") + "</a>" +
        '<a class="vs-quote" href="' + quoteHref + '" data-vs-cta="sticky-quote">' +
        (es ? "Cotizar gratis" : "Get my quote") + "</a>";
      document.body.appendChild(bar);
      document.body.classList.add("vs-has-callbar");
      // phone_click and quote_cta are already recorded by the click
      // listener above, so nothing extra is tracked here.
    } catch (e) { /* never let the bar break a page */ }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build);
  else build();
})();

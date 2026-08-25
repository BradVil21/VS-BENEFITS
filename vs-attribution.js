/* =====================================================================
   VS ATTRIBUTION  (vs-attribution.js)

   Answers "where did this lead come from?" — which the CRM currently
   cannot, because 249 of 260 leads carry no source at all.

   Two jobs:

   1. Remember, on a visitor's FIRST landing, how they got here: UTM tags,
      ad click ids, the referring site, and the page they landed on. Kept
      for 90 days, so someone who reads three articles over a fortnight and
      then fills in a form is still credited to whatever brought them the
      first time. Last touch is recorded separately, because the two answer
      different questions - first touch tells you what to spend on, last
      touch tells you what closes.

   2. Attach it to every lead the site submits, without each form having to
      remember to. Any same-origin POST to /api/ carrying a JSON body gets
      an `attribution` object folded in. That way a form added next year is
      attributed by default rather than by somebody remembering.

   Privacy: first-party only. No cookies, no third-party calls, nothing
   loaded. This records how a visitor reached a form they chose to fill in,
   which is part of handling their enquiry - it is not cross-site tracking,
   and it is deliberately kept separate from the analytics/marketing
   consent in vs-lead-system.js, which still gates Google entirely.

   Safe by design: every entry point is wrapped. If anything here throws,
   the form still submits - it just submits unattributed, exactly as today.
   ===================================================================== */
(function () {
  "use strict";

  var KEY = "vs_attr";
  var TTL = 90 * 24 * 3600 * 1000;

  // Search engines get their own label - "google.com" as a referrer is
  // organic search, and lumping it in with real referring sites would hide
  // the single number Bradley most needs to watch.
  var SEARCH = /(^|\.)(google|bing|duckduckgo|yahoo|ecosia|brave|startpage|search\.marcia)\./i;
  var SOCIAL = /(^|\.)(facebook|instagram|linkedin|twitter|x|t|tiktok|youtube|reddit|pinterest)\.(com|co|me)$/i;

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { return null; }
  }
  function write(v) {
    try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) { /* private mode */ }
  }

  function params() {
    var out = {};
    try {
      var q = new URLSearchParams(location.search);
      ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
       "gclid", "fbclid", "msclkid", "ttclid", "ref"].forEach(function (k) {
        var v = q.get(k);
        if (v) out[k] = String(v).slice(0, 120);
      });
    } catch (e) { /* ignore */ }
    return out;
  }

  // One human-readable line, because a board card has room for a phrase and
  // not for a UTM string.
  function label(t) {
    if (!t) return "Direct";
    if (t.gclid || t.utm_source === "google" && t.utm_medium === "cpc") return "Google Ads";
    if (t.fbclid || /facebook|meta|instagram/i.test(t.utm_source || "")) return "Facebook / Instagram Ads";
    if (t.msclkid) return "Microsoft Ads";
    if (t.utm_source) {
      return t.utm_source + (t.utm_medium ? " / " + t.utm_medium : "") +
             (t.utm_campaign ? " (" + t.utm_campaign + ")" : "");
    }
    var host = t.referrerHost || "";
    if (!host) return "Direct";
    if (SEARCH.test(host)) return "Organic search";
    if (SOCIAL.test(host)) return "Social — " + host.replace(/^www\./, "");
    return "Referral — " + host.replace(/^www\./, "");
  }

  function touch() {
    var p = params();
    var ref = "";
    try { ref = document.referrer || ""; } catch (e) { /* ignore */ }
    var host = "";
    try { host = ref ? new URL(ref).hostname : ""; } catch (e) { /* ignore */ }
    // A referrer from our own site is just internal navigation, not a source.
    if (host && host === location.hostname) { ref = ""; host = ""; }

    var t = {
      at: Date.now(),
      landing: (location.pathname || "/").slice(0, 160),
      referrer: ref.slice(0, 300),
      referrerHost: host,
    };
    Object.keys(p).forEach(function (k) { t[k] = p[k]; });
    t.label = label(t);
    return t;
  }

  // Only overwrite first touch when it has expired, or when this visit
  // actually carries new source information. A visitor who leaves and comes
  // back through the same channel should not reset their own history.
  function current() {
    var now = Date.now();
    var stored = read();
    var t = touch();
    var meaningful = Boolean(t.referrerHost) || Object.keys(params()).length > 0;

    if (!stored || !stored.first || (now - (stored.first.at || 0)) > TTL) {
      stored = { first: t, last: t, visits: 1 };
    } else {
      stored.visits = (stored.visits || 1) + (meaningful ? 1 : 0);
      if (meaningful) stored.last = t;
    }
    write(stored);
    return stored;
  }

  var state = null;
  try { state = current(); } catch (e) { state = null; }

  // What gets attached to a lead. Flat and short on purpose - it is going
  // onto a CRM record, not into an analytics warehouse.
  function payload() {
    try {
      var s = state || read();
      if (!s || !s.first) return null;
      var f = s.first, l = s.last || s.first;
      var out = {
        source: f.label || "Direct",
        lastSource: l.label || f.label || "Direct",
        landing: f.landing || "",
        referrer: f.referrer || "",
        visits: s.visits || 1,
        firstSeen: new Date(f.at || Date.now()).toISOString().slice(0, 10),
      };
      ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
       "gclid", "fbclid", "msclkid"].forEach(function (k) { if (f[k]) out[k] = f[k]; });
      return out;
    } catch (e) { return null; }
  }

  window.vsAttribution = payload;

  // ---- fold it into every lead POST the site makes ----
  // The alternative is editing every form on 150 pages and remembering to
  // edit the next one too. This way attribution is the default and a form
  // has to actively avoid it.
  try {
    var origFetch = window.fetch;
    if (typeof origFetch === "function") {
      window.fetch = function (input, init) {
        try {
          var url = typeof input === "string" ? input : (input && input.url) || "";
          var method = ((init && init.method) || (input && input.method) || "GET").toUpperCase();
          var isOurApi = url.indexOf("/api/") === 0 ||
                         url.indexOf(location.origin + "/api/") === 0;
          if (isOurApi && method === "POST" && init && typeof init.body === "string") {
            var body = JSON.parse(init.body);
            if (body && typeof body === "object" && !Array.isArray(body) && !body.attribution) {
              var a = payload();
              if (a) {
                body.attribution = a;
                init = Object.assign({}, init, { body: JSON.stringify(body) });
              }
            }
          }
        } catch (e) { /* never block a submission over attribution */ }
        // Pass `init` explicitly. Object.assign above builds a NEW init, so
        // forwarding the original `arguments` would send the unmodified body
        // and silently drop the attribution we just attached.
        return init === undefined ? origFetch.call(this, input) : origFetch.call(this, input, init);
      };
    }
  } catch (e) { /* ignore */ }
})();

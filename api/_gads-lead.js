// Google Ads lead form webhook (added 2026-11-03).
//
// POST /api/gads-lead   (rewritten to /api/voice-lookup?op=gads-lead)
//
// Google posts every lead form submit here the moment it happens. We check the
// shared key, turn Google's column list into a normal website lead, and hand it
// to /api/lead-sync's to-crm path - the same path the quote form uses - so the
// lead lands in GoHighLevel (which texts you) and on the portal board.
//
// ENV: GADS_LEAD_KEY  - the "Key" typed into the lead form's webhook settings.
//                        The build script fills the same value in for you.

const leadSync = require("./lead-sync");

function col(d, ids) {
  const list = Array.isArray(d.user_column_data) ? d.user_column_data : [];
  for (let i = 0; i < list.length; i++) {
    const c = list[i] || {};
    if (ids.indexOf(String(c.column_id || "").toUpperCase()) >= 0) return String(c.string_value || "").trim();
  }
  return "";
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }
  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  const key = process.env.GADS_LEAD_KEY;
  if (!key) { res.status(503).json({ error: "GADS_LEAD_KEY is not set in Vercel" }); return; }
  if (String(d.google_key || "") !== key) { res.status(401).json({ error: "Bad key" }); return; }
  if (d.is_test) { res.status(200).json({ ok: true, test: true }); return; }

  let first = col(d, ["FIRST_NAME"]), last = col(d, ["LAST_NAME"]);
  const full = col(d, ["FULL_NAME"]);
  if (!first && full) { const p = full.split(/\s+/); first = p.shift() || ""; last = p.join(" "); }
  const campaign = String(d.campaign_name || d.campaign_id || "");
  const spanish = /spanish|espa/i.test(campaign);
  // The Spanish campaign covers both niches, so its form leads are tagged "spanish" only.
  const niche = spanish ? "spanish" : (/self|1099|independ/i.test(campaign) ? "self-employed" : "trucker");

  const lead = {
    firstName: first, lastName: last,
    phone: col(d, ["PHONE_NUMBER"]), email: col(d, ["EMAIL"]),
    zip: col(d, ["POSTAL_CODE"]),
    source: "Google Ads lead form",
    tags: ["google-lead-form"].concat(spanish ? ["spanish"] : ["lp-" + niche]),
    notes: "Google Ads lead form" + (campaign ? " - campaign " + campaign : "") + (d.lead_id ? " (lead " + d.lead_id + ")" : ""),
    attribution: { source: "Google Ads", lastSource: "Google Ads", landing: "Google Ads lead form", visits: 1,
      gclid: String(d.gcl_id || ""), utm_campaign: campaign },
  };

  // Hand off to lead-sync. It answers its own response object; we wrap it so
  // Google always gets a quick 200 even if the CRM call is slow or fails.
  let out = null;
  const fakeRes = {
    headersSent: false,
    setHeader: function () {},
    status: function () { return this; },
    json: function (j) { out = j; this.headersSent = true; },
    end: function () { this.headersSent = true; },
  };
  try {
    await leadSync({ method: "POST", body: lead, query: {}, headers: {}, url: "/api/lead-sync" }, fakeRes);
  } catch (e) { out = { ok: false, error: "exception" }; }
  res.status(200).json({ ok: true, result: out });
};

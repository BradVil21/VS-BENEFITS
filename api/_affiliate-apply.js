// POST /api/affiliate-apply  (rewritten to /api/voice-lookup?op=affiliate-apply,
// Vercel Hobby 12-function limit)
//
// Creator / affiliate program application from /affiliate-program.
//   1. Drops blocked people (same guard as every lead form) and obvious junk.
//   2. Appends the application to Firestore vs_state/affiliates so it shows up
//      live in the admin portal's Affiliates tab (stage "applied"). A repeat
//      application from the same email/phone updates the existing card.
//   3. Upserts the GHL contact, tags it `affiliate-applicant` + `creator`
//      (+ platform/audience tags) and leaves a note with the full application.
//      Build a GHL workflow on the tag `affiliate-applicant` if you want an
//      auto-reply.
//   4. Texts Bradley (GHL internal-alerts contact), if configured.
// Always returns 200 with { ok:true } so the page never shows an error for a
// CRM hiccup; the Firestore write is the record that matters.

const L = require("./_lib");
const F = require("./_fs");

function clean(v, max) { return String(v == null ? "" : v).replace(/\s+/g, " ").trim().slice(0, max || 120); }
function cleanLong(v, max) { return String(v == null ? "" : v).replace(/\r/g, "").trim().slice(0, max || 1200); }
function slug(v) { return String(v || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 30); }

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  // honeypot: a hidden field real people never fill
  if (clean(d.website_url)) { res.status(200).json({ ok: true }); return; }

  const firstName = clean(d.firstName, 60), lastName = clean(d.lastName, 60);
  const email = clean(d.email, 160).toLowerCase(), phone = clean(d.phone, 40);
  if (!firstName || (!email && !phone)) { res.status(400).json({ ok: false, error: "missing_fields" }); return; }

  if (await L.guardBanned(req, res, { email: email, phone: phone, meta: d.meta })) return;
  try {
    const junk = L.junkSignals ? L.junkSignals({ firstName: firstName, lastName: lastName, email: email, phone: phone }) : null;
    if (junk && junk.junk) { res.status(200).json({ ok: true }); return; }
  } catch (e) { /* never block on the filter */ }

  const platforms = (Array.isArray(d.platforms) ? d.platforms : String(d.platforms || "").split(","))
    .map(function (p) { return clean(p, 30); }).filter(Boolean).slice(0, 8);
  const audience = (Array.isArray(d.audience) ? d.audience : String(d.audience || "").split(","))
    .map(function (p) { return clean(p, 40); }).filter(Boolean).slice(0, 8);
  const now = Date.now();
  const meta = L.visitorMeta(req, d);
  const A = (d.attribution && typeof d.attribution === "object") ? d.attribution : null;

  const rec = {
    id: "aff_" + now.toString(36) + Math.random().toString(36).slice(2, 7),
    firstName: firstName, lastName: lastName, email: email, phone: phone,
    state: clean(d.state, 2).toUpperCase(),
    handle: clean(d.handle, 80),
    profileUrl: clean(d.profileUrl, 300),
    platforms: platforms,
    followers: clean(d.followers, 30),
    audience: audience,
    contentType: clean(d.contentType, 60),
    pitch: cleanLong(d.pitch, 1200),
    language: clean(d.language, 30),
    stage: "applied",
    code: "",
    suggestedCode: slug(firstName + (lastName ? "-" + lastName.charAt(0) : "")) || slug(d.handle),
    reward: 0,
    refs: {},
    payouts: [],
    notes: "[" + new Date(now).toLocaleString("en-US", { timeZone: "America/New_York", month: "numeric", day: "numeric", hour: "numeric", minute: "2-digit" }) + "] Applied on the website.\n",
    source: "Website: affiliate application",
    attribution: A,
    meta: meta,
    created: now, updated: now,
  };

  const out = { ok: true };

  // ---- 1. GoHighLevel (first, so the portal card carries the contact id) ----
  try {
    const cid = await L.upsertContact({ firstName: firstName, lastName: lastName, email: email, phone: phone, state: rec.state, website_lead_stage: "Affiliate / creator application" });
    if (cid) {
      out.ghl = true;
      const tags = ["affiliate-applicant", "creator"];
      platforms.forEach(function (p) { tags.push("creator-" + slug(p)); });
      audience.slice(0, 3).forEach(function (a) { tags.push("aud-" + slug(a)); });
      await L.addTagsToContact(cid, tags);
      const lines = [
        "AFFILIATE / CREATOR APPLICATION",
        "Handle: " + (rec.handle || "-"),
        "Profile: " + (rec.profileUrl || "-"),
        "Platforms: " + (platforms.join(", ") || "-"),
        "Followers: " + (rec.followers || "-"),
        "Audience: " + (audience.join(", ") || "-"),
        "Content: " + (rec.contentType || "-"),
        "Language: " + (rec.language || "-"),
        "State: " + (rec.state || "-"),
        "How they'd promote: " + (rec.pitch || "-"),
        "Suggested link code: " + (rec.suggestedCode || "-"),
        meta && meta.ip ? "IP: " + meta.ip + (meta.ipCity ? " (" + [meta.ipCity, meta.ipRegion].filter(Boolean).join(", ") + ")" : "") : "",
      ].filter(Boolean).join("\n");
      try { await L.ghl("/contacts/" + cid + "/notes", "POST", { body: lines }); } catch (e) {}
      rec.ghlContactId = cid;
    }
  } catch (e) { out.ghl = false; }

  // ---- 2. admin portal (Firestore) ----
  try {
    const same = function (x) {
      return (email && String(x.email || "").toLowerCase() === email) ||
             (phone && L.normPhone && L.normPhone(x.phone) && L.normPhone(x.phone) === L.normPhone(phone));
    };
    const w = await F.appendRecord("affiliates", rec, same, function (ex) {
      ["handle", "profileUrl", "followers", "contentType", "pitch", "state", "language"].forEach(function (k) { if (rec[k]) ex[k] = rec[k]; });
      if (rec.platforms.length) ex.platforms = rec.platforms;
      if (rec.audience.length) ex.audience = rec.audience;
      ex.notes = rec.notes.replace("Applied on the website.", "Applied again on the website.") + (ex.notes || "");
      if (!ex.meta && meta) ex.meta = meta;
      if (rec.ghlContactId && !ex.ghlContactId) ex.ghlContactId = rec.ghlContactId;
      if (ex.stage === "declined") ex.stage = "applied";
      ex.updated = now;
      return true;
    });
    out.portal = w.action || w.reason;
    // Welcome text + email through the GHL workflow "Affiliate - Send Update".
    try {
      if (w.ok) {
        const AE = require("./_affiliate-event");
        out.welcome = await Promise.race([
          AE.notify(Object.assign({}, rec, { id: w.id || rec.id }), "applied", "welcome"),
          new Promise(function (r) { setTimeout(function () { r({ skipped: "timeout" }); }, 5000); }),
        ]);
      }
    } catch (e) { out.welcome = "error"; }
  } catch (e) { out.portal = "error"; }

  // ---- 3. text alert ----
  try {
    if (L.sendAlertSms) await Promise.race([
      L.sendAlertSms("New creator/affiliate application: " + firstName + " " + lastName + (rec.handle ? " (" + rec.handle + ")" : "") + (platforms.length ? ", " + platforms.join("/") : "") + (rec.followers ? ", " + rec.followers + " followers" : "") + ". Review it in the portal: Affiliates."),
      new Promise(function (r) { setTimeout(r, 3000); }),
    ]);
  } catch (e) {}

  res.status(200).json(out);
};

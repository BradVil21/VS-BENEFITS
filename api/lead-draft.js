// Vercel serverless function: capture an ABANDONED / IN-PROGRESS quote "draft".
//
// Purpose: first-party abandoned/in-progress lead capture. The website auto-calls
// this from the /quote funnel as the visitor fills it in — even if they never press
// submit. It stores the partial info as a HubSpot contact tagged as a draft so
// Bradley can follow up. When the visitor later completes the full quote, the same
// email upserts the SAME contact (no duplicate lead).
//
// Security / privacy by design:
//   - POST only, JSON only, CORS locked to the site origin.
//   - Server-side validation + sanitisation of every field (never trust the client).
//   - Requires a valid email to write to the backend (dedup key). Phone-only drafts
//     stay in the visitor's own browser and are never sent here.
//   - Length caps to stop oversized/abusive payloads.
//   - Encrypted in transit (Vercel serves this over HTTPS/TLS only).
//   - Safe by design: if HUBSPOT_PRIVATE_APP_TOKEN is missing, the write is skipped
//     and the function still returns 200 so the site never breaks.
//
// See api/_lib.js for shared helpers and env vars.

const L = require("./_lib");

// Only accept requests from our own site (defence-in-depth; the data is first-party).
const ALLOWED_ORIGINS = [
  "https://www.vshealthbenefits.com",
  "https://vshealthbenefits.com",
];

function pickOrigin(req) {
  const o = String((req.headers && req.headers.origin) || "");
  return ALLOWED_ORIGINS.indexOf(o) !== -1 ? o : ALLOWED_ORIGINS[0];
}

// Trim + hard length cap. Never store more than we need.
function clean(v, max) {
  return String(v == null ? "" : v).trim().slice(0, max || 120);
}

// Conservative server-side email check (mirrors the client, but the server is the
// source of truth). Returns a normalised lowercase email or "".
function validEmail(v) {
  const s = clean(v, 120).toLowerCase();
  const m = /^([^\s@]+)@([^\s@]+\.[a-z]{2,})$/.exec(s);
  if (!m) return "";
  if (/\.\.|^\.|\.$/.test(m[1])) return "";
  return s;
}

// Digits-only US phone, 10 digits (drops a leading country code). Returns "" if bad.
function validPhone(v) {
  let d = clean(v, 25).replace(/\D/g, "");
  if (d.length === 11 && d.charAt(0) === "1") d = d.slice(1);
  if (d.length !== 10) return "";
  if (/^(\d)\1{9}$/.test(d)) return "";               // all same digit
  if (d.slice(0, 3) === "555" || d.slice(3, 6) === "555") return "";
  return d;
}

module.exports = async (req, res) => {
  const origin = pickOrigin(req);
  res.setHeader("Access-Control-Allow-Origin", origin);
  res.setHeader("Vary", "Origin");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  // 1) First-party auto-capture from our own /quote form: store partial (not-yet-
  //    submitted) quotes so an advisor can follow up. There is no opt-in checkbox
  //    anymore; a valid email (checked below) is the only hard requirement.
  const optIn = d.optIn === true || d.optIn === "true";

  // 2) Validate the dedup key. Email is required to store server-side.
  const email = validEmail(d.email || d.contactEmail);
  if (!email) {
    res.status(200).json({ ok: false, skipped: "no_valid_email" });
    return;
  }

  // 3) Sanitise the rest.
  const phone = validPhone(d.phone || d.contactPhone || d.businessPhone);
  const firstName = clean(d.firstName || d.ownerFirstName, 60);
  const lastName = clean(d.lastName || d.ownerLastName, 60);
  const zip = clean(d.zip || d.businessZip, 10).replace(/\D/g, "").slice(0, 5);
  const state = clean(d.state || d.businessState, 30);
  const company = clean(d.company || d.businessName, 120);
  const type = d.type === "business" ? "business" : "individual";
  const step = clean(d.step, 20);

  // 4) Upsert the contact (dedup by email) and tag it as a recoverable draft.
  let contactId = null;
  try {
    contactId = await L.upsertContact({
      email: email,
      firstname: firstName,
      lastname: lastName,
      phone: phone,
      company: company,
      state: state,
      zip: zip,
      website_lead_stage: "Abandoned Draft — Recover",
      lifecyclestage: "lead",
    });
  } catch (e) { /* non-fatal */ }

  // 5) Add a note so Bradley knows this is an in-progress recovery, not a finished lead.
  try {
    if (contactId) {
      const note =
        "<b>In-progress quote — auto-captured (visitor did NOT press submit)</b><br>" +
        [
          "Funnel: " + type,
          step ? "Reached: " + L.esc(step) : "",
          firstName || lastName ? "Name: " + L.esc((firstName + " " + lastName).trim()) : "",
          phone ? "Phone: " + L.esc(phone) : "",
          company ? "Business: " + L.esc(company) : "",
          "Opt-in checkbox: " + (optIn ? "yes" : "no (passive capture)"),
          "Source: /quote autosave",
        ].filter(Boolean).join("<br>");
      await L.addNoteToContact(contactId, note);
    }
  } catch (e) { /* non-fatal */ }

  res.status(200).json({ ok: true, contactId: contactId || null, stored: !!contactId });
};

// Vercel serverless function: a member submitted a referral in the client portal.
//
// This replaces the old HubSpot "Client Referral" hidden-form POST that used to
// run in client.html. Everything now goes to GoHighLevel.
//
// Flow:
//   client.html referral wizard
//     -> POST /api/portal-referral   (this file)
//        1. Upsert the REFERRED PERSON as a contact in GHL
//        2. Tag them `portal-referral` + `client-referral`
//        3. Attach a note with the full referral detail and who sent it,
//           so the advisor sees the whole picture on the contact record
//
// The referring member is identified by email in the note and in the
// `referred_by_email` payload field, so referral credit stays traceable.
//
// Safe by design: every step is wrapped, one failure never blocks the others,
// and the function always returns 200 so a referral is never blocked by CRM lag.
//
// ENV VARS:
//   GHL_PIT_TOKEN            REQUIRED. Private integration token (pit-...).
//   GHL_LOCATION_ID          optional, defaults to the VS Health Benefits sub-account
//   PORTAL_SIGNUP_SECRET     optional shared secret; if set, callers must send it
//                            in the `x-vs-portal-secret` header.

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";

const LOCATION_ID = process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU";

function clean(v, max) {
  return String(v == null ? "" : v).trim().slice(0, max || 120);
}

function validEmail(v) {
  const s = clean(v, 120).toLowerCase();
  const m = /^([^\s@]+)@([^\s@]+\.[a-z]{2,})$/.exec(s);
  if (!m) return "";
  if (/\.\.|^\.|\.$/.test(m[1])) return "";
  return s;
}

function validPhone(v) {
  let d = clean(v, 25).replace(/\D/g, "");
  if (d.length === 11 && d.charAt(0) === "1") d = d.slice(1);
  if (d.length !== 10) return "";
  if (/^(\d)\1{9}$/.test(d)) return "";
  if (d.slice(0, 3) === "555" || d.slice(3, 6) === "555") return "";
  return "+1" + d;
}

async function ghl(path, method, body) {
  const token = process.env.GHL_PIT_TOKEN;
  if (!token) return { ok: false, skipped: "no_ghl_token", status: 0, json: null };
  try {
    const r = await fetch(GHL_BASE + path, {
      method: method || "GET",
      headers: {
        Authorization: "Bearer " + token,
        Version: GHL_VERSION,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    let json = null;
    try { json = await r.json(); } catch (e) { /* empty body is fine */ }
    return { ok: r.ok, status: r.status, json };
  } catch (e) {
    return { ok: false, status: 0, json: null, error: String((e && e.message) || e) };
  }
}

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, x-vs-portal-secret");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  const expected = process.env.PORTAL_SIGNUP_SECRET;
  if (expected) {
    const got = String((req.headers && req.headers["x-vs-portal-secret"]) || "");
    if (got !== expected) { res.status(401).json({ error: "Unauthorized" }); return; }
  }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  const r = {
    firstName: clean(d.firstName || d.first_name, 60),
    lastName:  clean(d.lastName  || d.last_name,  60),
    email:     validEmail(d.email || d.referral_email),
    phone:     validPhone(d.phone || d.referral_phone),
    leadType:  clean(d.leadType || d.lead_type, 60),
    zip:       clean(d.zip, 12),
    state:     clean(d.state, 4).toUpperCase(),
    dob:       clean(d.dob, 20),
    income:    clean(d.income, 20),
    notes:     clean(d.notes, 900),
    appointment: clean(d.appointment, 120),
    preferredContact: clean(d.preferredContact || d.preferred_contact, 40),
    referredByName:  clean(d.referredByName  || d.referred_by_name, 120),
    referredByEmail: validEmail(d.referredByEmail || d.referred_by_email),
    referredByPhone: validPhone(d.referredByPhone || d.referred_by_phone),
    referredByFirst: clean(d.referredByFirst || d.referred_by_first, 60),
    referralId: clean(d.referralId || d.referral_id, 60),
  };

  if (!r.email && !r.phone) {
    res.status(200).json({ ok: true, skipped: "no_email_or_phone" });
    return;
  }

  const out = { ok: true };

  // ---- 1. upsert the referred person ----
  const body = {
    locationId: LOCATION_ID,
    firstName: r.firstName,
    lastName: r.lastName,
    name: (r.firstName + " " + r.lastName).trim(),
    source: "Client portal referral",
  };
  if (r.email) body.email = r.email;
  if (r.phone) body.phone = r.phone;
  if (r.state) body.state = r.state;
  if (r.zip) body.postalCode = r.zip;

  let contactId = null;
  try {
    const up = await ghl("/contacts/upsert", "POST", body);
    const c = up.json && (up.json.contact || up.json.data || up.json);
    if (up.ok && c && c.id) contactId = c.id;
    else out.contactError = up.status || up.skipped;
  } catch (e) { out.contactError = "exception"; }
  out.contactId = contactId;

  // ---- 2. tags ----
  if (contactId) {
    try {
      const t = await ghl("/contacts/" + contactId + "/tags", "POST", {
        tags: ["portal-referral", "client-referral"],
      });
      out.tagged = Boolean(t.ok);
    } catch (e) { out.tagged = false; }
  }

  // ---- 3. note with the full detail ----
  if (contactId) {
    const lines = [];
    lines.push("Client portal referral");
    lines.push("Referred by: " + (r.referredByName || "a portal member") +
      (r.referredByEmail ? " (" + r.referredByEmail + ")" : ""));
    if (r.leadType) lines.push("Lead type: " + r.leadType);
    if (r.phone) lines.push("Phone: " + r.phone);
    if (r.email) lines.push("Email: " + r.email);
    if (r.zip || r.state) lines.push("ZIP / State: " + (r.zip + " " + r.state).trim());
    if (r.dob) lines.push("DOB: " + r.dob);
    if (r.income) lines.push("Income: $" + r.income);
    lines.push(r.appointment ? "Appointment: " + r.appointment : "No appointment requested");
    if (r.preferredContact) lines.push("Preferred contact: " + r.preferredContact);
    if (r.notes) lines.push("Notes: " + r.notes);
    if (r.referralId) lines.push("Portal referral ID: " + r.referralId);

    try {
      const n = await ghl("/contacts/" + contactId + "/notes", "POST", {
        body: lines.join("\n"),
      });
      out.noted = Boolean(n.ok);
    } catch (e) { out.noted = false; }
  }

  // ---- 4. tag the REFERRING MEMBER -> triggers the thank-you workflow ----
  // This is a different person from the contact above. The referred person gets
  // added to the CRM; the member who sent them gets the thank-you email + SMS,
  // and Bradley gets the internal alert (that lives in the workflow, not here).
  if (r.referredByEmail || r.referredByPhone) {
    try {
      const rb = { locationId: LOCATION_ID, source: "Client portal referral" };
      if (r.referredByEmail) rb.email = r.referredByEmail;
      if (r.referredByPhone) rb.phone = r.referredByPhone;
      if (r.referredByFirst) rb.firstName = r.referredByFirst;

      const up2 = await ghl("/contacts/upsert", "POST", rb);
      const c2 = up2.json && (up2.json.contact || up2.json.data || up2.json);
      const referrerId = up2.ok && c2 && c2.id ? c2.id : null;
      out.referrerId = referrerId;

      if (referrerId) {
        const t2 = await ghl("/contacts/" + referrerId + "/tags", "POST", {
          tags: ["referral-submitted", "member-portal"],
        });
        out.referrerTagged = Boolean(t2.ok);
        if (!t2.ok) out.referrerTagError = t2.status || t2.skipped;
      } else {
        out.referrerError = up2.status || up2.skipped;
      }
    } catch (e) { out.referrerTagged = false; out.referrerError = "exception"; }
  } else {
    out.referrerSkipped = "no_referrer_contact";
  }

  res.status(200).json(out);
};

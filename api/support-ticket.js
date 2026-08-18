// Vercel serverless function: someone submitted a support request.
//
// Replaces api/hubspot-ticket.js. Everything runs through GoHighLevel now.
//
// What it does:
//   1. Mints a ticket number  (VS-XXXXXXX, see makeTicketNumber)
//   2. Upserts the requester's contact in GHL + writes the ticket number to a
//      custom field, then tags `support-ticket-created`   <-- TRIGGERS the
//      "Support Ticket Created" workflow, which emails the requester the
//      24-48 hour acknowledgement and sends you the internal copy
//   3. Appends the ticket to Firestore vs_state/contact_requests so it shows up
//      in the admin portal's Support board straight away
//   4. Returns the ticket number so the page can show it to the person
//
// Every step is wrapped. A CRM or Firestore hiccup never costs you the ticket
// number or blocks the form, and the function always returns 200.
//
// ENV VARS:
//   GHL_PIT_TOKEN            REQUIRED for the CRM half.
//   GHL_LOCATION_ID          optional, defaults to the VS Health Benefits sub-account
//   FIREBASE_API_KEY         optional; defaults to the public web key (same as admin.html)
//   FIREBASE_PROJECT_ID      optional
//   PORTAL_SIGNUP_SECRET     optional shared secret; callers send x-vs-portal-secret

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";
const LOCATION_ID = process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU";

const FB_API_KEY = process.env.FIREBASE_API_KEY || "AIzaSyCbZ7Otrz6yPlxJuLlDPEoMzssgsWkjo5U";
const FB_PROJECT = process.env.FIREBASE_PROJECT_ID || "vs-benefits-c1da9";
const FS_DOC =
  "https://firestore.googleapis.com/v1/projects/" + FB_PROJECT +
  "/databases/(default)/documents/vs_state/contact_requests";

// Custom field holding the ticket number on the contact record:
// "Support Ticket Number", key contact.support_ticket_number.
//
// Hardcoded rather than looked up, because reading /locations/{id}/customFields
// needs the `locations.readonly` scope and this token only has contacts scopes.
// GHL returns an empty list rather than an error in that case, which writes a
// blank field and looks exactly like "the email just didn't work".
// If you ever delete and recreate the field it gets a new ID - override with
// the GHL_CF_TICKET_NUMBER env var, no deploy needed.
const CF_TICKET_NUMBER = process.env.GHL_CF_TICKET_NUMBER || "5uaYmKQ3yLZH7mtV8d9n";

// ---------- ticket numbers ----------
// Crockford-style alphabet with the ambiguous characters removed. No 0/O, no
// 1/I/L. These numbers get read aloud on the phone and written on sticky notes,
// so "was that a zero or an oh" is a real cost.
const TICKET_ALPHABET = "23456789ABCDEFGHJKMNPQRSTVWXYZ";

// Seconds since this epoch are what the time half encodes. Counting from 2026
// instead of 1970 keeps the number short enough to read aloud while still
// growing monotonically - so a higher ticket number always means a later
// ticket, for the next ~23 years.
const TICKET_EPOCH = Date.UTC(2026, 0, 1);

function base(n, len) {
  let s = "";
  const b = TICKET_ALPHABET.length;
  n = Math.max(0, Math.floor(n));
  while (n > 0 && s.length < 32) {
    s = TICKET_ALPHABET.charAt(n % b) + s;
    n = Math.floor(n / b);
  }
  while (s.length < len) s = TICKET_ALPHABET.charAt(0) + s;
  return s;
}

// VS-<6 time chars>-<3 random>, e.g. VS-24MHFP-K7Q.
//
// The time half is seconds since TICKET_EPOCH in a 30-character alphabet: six
// characters covers about 23 years without ever wrapping, so ticket numbers
// keep sorting in the order they arrived. (An earlier version truncated the
// millisecond clock to five characters, which silently wrapped every ~6.75
// hours and made yesterday's ticket sort after today's.)
//
// The random tail gives 27,000 combinations per second, so two people hitting
// submit at the same moment don't collide.
function makeTicketNumber(now) {
  const secs = Math.floor(((now || Date.now()) - TICKET_EPOCH) / 1000);
  const t = base(secs, 6);
  let r = "";
  for (let i = 0; i < 3; i++) {
    r += TICKET_ALPHABET.charAt(Math.floor(Math.random() * TICKET_ALPHABET.length));
  }
  return "VS-" + t + "-" + r;
}

// ---------- sanitisers ----------
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

// ---------- GHL ----------
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

// ---------- Firestore (same shape admin.html reads) ----------
function fsEncode(v) {
  if (v === null || v === undefined) return { nullValue: null };
  if (typeof v === "boolean") return { booleanValue: v };
  if (typeof v === "number") {
    return Number.isInteger(v) ? { integerValue: String(v) } : { doubleValue: v };
  }
  if (Array.isArray(v)) return { arrayValue: { values: v.map(fsEncode) } };
  if (typeof v === "object") {
    const fields = {};
    Object.keys(v).forEach(function (k) { fields[k] = fsEncode(v[k]); });
    return { mapValue: { fields: fields } };
  }
  return { stringValue: String(v) };
}

function fsDecode(v) {
  if (!v || typeof v !== "object") return null;
  if ("nullValue" in v) return null;
  if ("booleanValue" in v) return v.booleanValue;
  if ("integerValue" in v) return Number(v.integerValue);
  if ("doubleValue" in v) return Number(v.doubleValue);
  if ("stringValue" in v) return v.stringValue;
  if ("timestampValue" in v) return v.timestampValue;
  if ("arrayValue" in v) return (v.arrayValue.values || []).map(fsDecode);
  if ("mapValue" in v) {
    const out = {};
    const f = v.mapValue.fields || {};
    Object.keys(f).forEach(function (k) { out[k] = fsDecode(f[k]); });
    return out;
  }
  return null;
}

async function fsToken() {
  try {
    const r = await fetch(
      "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + FB_API_KEY,
      { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ returnSecureToken: true }) }
    );
    if (!r.ok) return null;
    const j = await r.json();
    return j.idToken || null;
  } catch (e) { return null; }
}

// Append the ticket to vs_state/contact_requests, preserving what's there.
// Read-modify-write, same as the leads pipeline. Fine at support volume; two
// tickets landing in the same second could theoretically clobber each other.
async function pushTicket(ticket) {
  const token = await fsToken();
  if (!token) return { ok: false, reason: "auth_failed" };
  const auth = { Authorization: "Bearer " + token };

  let items = [];
  const get = await fetch(FS_DOC, { headers: auth });
  if (get.ok) {
    const doc = await get.json();
    const cur = doc && doc.fields && doc.fields.items;
    if (cur) items = fsDecode(cur) || [];
  } else if (get.status !== 404) {
    return { ok: false, reason: "read_failed_" + get.status };
  }

  items.unshift(ticket);
  if (items.length > 500) items = items.slice(0, 500);

  const put = await fetch(FS_DOC, {
    method: "PATCH",
    headers: Object.assign({ "Content-Type": "application/json" }, auth),
    body: JSON.stringify({ fields: { items: fsEncode(items), ts: fsEncode(Date.now()) } }),
  });
  if (!put.ok) return { ok: false, reason: "write_failed_" + put.status };
  return { ok: true, total: items.length };
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

  const name = clean(d.name || d.fullName, 120);
  const parts = name.split(/\s+/);
  const p = {
    firstName: clean(d.firstName || parts[0], 60),
    lastName:  clean(d.lastName || parts.slice(1).join(" "), 60),
    fullName:  name,
    email:     validEmail(d.email),
    phone:     validPhone(d.phone),
    subject:   clean(d.subject, 140),
    message:   clean(d.message, 2000),
    page:      clean(d.page, 200),
  };

  if (!p.email && !p.phone) {
    res.status(200).json({ ok: true, skipped: "no_email_or_phone" });
    return;
  }

  const now = Date.now();
  const ticketNumber = makeTicketNumber(now);
  const out = { ok: true, ticketNumber: ticketNumber };

  // ---- 1. upsert the requester + write the ticket number ----
  const body = {
    locationId: LOCATION_ID,
    source: "Support request",
  };
  if (p.firstName) body.firstName = p.firstName;
  if (p.lastName) body.lastName = p.lastName;
  if (p.fullName) body.name = p.fullName;
  if (p.email) body.email = p.email;
  if (p.phone) body.phone = p.phone;
  if (CF_TICKET_NUMBER) {
    body.customFields = [{ id: CF_TICKET_NUMBER, value: ticketNumber }];
  } else {
    out.fieldWarning = "no_ticket_number_field";
  }

  let contactId = null;
  try {
    const up = await ghl("/contacts/upsert", "POST", body);
    const c = up.json && (up.json.contact || up.json.data || up.json);
    if (up.ok && c && c.id) contactId = c.id;
    else out.contactError = up.status || up.skipped;
  } catch (e) { out.contactError = "exception"; }
  out.contactId = contactId;

  // ---- 2. note with the actual request, so you see it on the contact ----
  if (contactId && (p.message || p.subject)) {
    try {
      const lines = ["Support request " + ticketNumber];
      if (p.subject) lines.push("Subject: " + p.subject);
      if (p.page) lines.push("Page: " + p.page);
      if (p.message) lines.push("", p.message);
      await ghl("/contacts/" + contactId + "/notes", "POST", { body: lines.join("\n") });
      out.noted = true;
    } catch (e) { out.noted = false; }
  }

  // ---- 3. tag -> TRIGGERS "Support Ticket Created" ----
  // The workflow removes this tag as its last step so the next request re-fires.
  if (contactId) {
    try {
      const t = await ghl("/contacts/" + contactId + "/tags", "POST", {
        tags: ["support-ticket-created"],
      });
      out.tagged = Boolean(t.ok);
      if (!t.ok) out.tagError = t.status || t.skipped;
    } catch (e) { out.tagged = false; out.tagError = "exception"; }
  }

  // ---- 4. put it on the admin Support board ----
  try {
    const push = await pushTicket({
      id: "tk_" + now.toString(36) + Math.random().toString(36).slice(2, 8),
      ticketNo: ticketNumber,
      firstName: p.firstName,
      lastName: p.lastName,
      fullName: p.fullName,
      email: p.email,
      phone: p.phone,
      subject: p.subject,
      message: p.message,
      page: p.page,
      stage: "new",
      created: now,
      ghlContactId: contactId || "",
    });
    out.boarded = Boolean(push.ok);
    if (!push.ok) out.boardError = push.reason;
  } catch (e) { out.boarded = false; out.boardError = "exception"; }

  res.status(200).json(out);
};

// Vercel serverless function: a new member account was created in the client portal.
//
// Flow:
//   client.html signup form
//     -> POST /api/portal-signup   (this file)
//        1. Upsert the contact in GoHighLevel (creates or updates by email/phone)
//        2. Write portal custom fields (Admin Client ID)
//        3. Add the tag `portal-account-created`
//           -> this tag is what TRIGGERS the "Member Account Creation" workflow
//              in GHL, which sends the welcome EMAIL + SMS.
//        4. Optionally mirror the raw payload to a GHL Inbound Webhook URL
//
// Why the tag and not a raw inbound webhook as the trigger:
//   A tag fires on a contact that already exists with every field populated, so
//   the workflow's email/SMS merge fields ({{contact.first_name}} etc.) resolve.
//   An inbound-webhook trigger would have to re-map every field by hand and
//   can fire before the contact record is complete.
//
// Why this is server-side and not in client.html:
//   The GHL private integration token must never ship to the browser. client.html
//   is public. Only this function ever sees the token.
//
// Safe by design: every step is wrapped, one failure never blocks the others, and
// the function always returns 200 so a portal signup is never blocked by CRM lag.
//
// ENV VARS (Vercel -> Project -> Settings -> Environment Variables):
//   GHL_PIT_TOKEN              REQUIRED. Private integration token (pit-...).
//                              No fallback on purpose — never hardcode it here.
//   GHL_LOCATION_ID            optional, defaults to the VS Health Benefits sub-account
//   GHL_SIGNUP_TAG             optional, defaults to "portal-account-created"
//   GHL_INBOUND_WEBHOOK_URL    optional. If set, the raw payload is also POSTed here.
//   PORTAL_SIGNUP_SECRET       optional shared secret; if set, callers must send it
//                              in the `x-vs-portal-secret` header.

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";

const LOCATION_ID = process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU";
const SIGNUP_TAG = process.env.GHL_SIGNUP_TAG || "portal-account-created";

// Custom field IDs for this location (locations_get-custom-fields).
const CF = {
  adminClientId: "5efIdoiiJRdSveecafoi", // contact.admin_client_id
};

// ---------- sanitisers (same shape as api/webchat-lead.js) ----------
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

// Returns E.164 (+1XXXXXXXXXX) because GHL needs that to send an SMS. "" if invalid.
function validPhone(v) {
  let d = clean(v, 25).replace(/\D/g, "");
  if (d.length === 11 && d.charAt(0) === "1") d = d.slice(1);
  if (d.length !== 10) return "";
  if (/^(\d)\1{9}$/.test(d)) return "";
  if (d.slice(0, 3) === "555" || d.slice(3, 6) === "555") return "";
  return "+1" + d;
}

// ---------- GHL REST ----------
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

// Create or update the contact by email/phone. Returns { id, isNew } or null.
async function upsertContact(d) {
  const customFields = [];
  if (d.accountId) customFields.push({ id: CF.adminClientId, value: d.accountId });

  const body = {
    locationId: LOCATION_ID,
    firstName: d.firstName,
    lastName: d.lastName,
    name: (d.firstName + " " + d.lastName).trim(),
    source: "Client portal signup",
  };
  if (d.email) body.email = d.email;
  if (d.phone) body.phone = d.phone;
  if (customFields.length) body.customFields = customFields;

  const r = await ghl("/contacts/upsert", "POST", body);
  const c = r.json && (r.json.contact || r.json.data || r.json);
  if (!r.ok || !c || !c.id) {
    return { id: null, isNew: false, status: r.status, error: r.json || r.error || r.skipped };
  }
  return { id: c.id, isNew: r.json.new === true, status: r.status };
}

// Add the trigger tag as a discrete event, after the contact is fully populated.
async function addTags(contactId, tags) {
  if (!contactId) return { ok: false, skipped: "no_contact" };
  return ghl("/contacts/" + contactId + "/tags", "POST", { tags: tags });
}

// Optional mirror to a GHL Inbound Webhook (or any other listener).
async function mirrorToWebhook(payload) {
  const url = process.env.GHL_INBOUND_WEBHOOK_URL;
  if (!url) return { ok: false, skipped: "no_webhook_url" };
  try {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return { ok: r.ok, status: r.status };
  } catch (e) {
    return { ok: false, error: String((e && e.message) || e) };
  }
}

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, x-vs-portal-secret");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  // ---- optional shared-secret check ----
  const expected = process.env.PORTAL_SIGNUP_SECRET;
  if (expected) {
    const got = String((req.headers && req.headers["x-vs-portal-secret"]) || "");
    if (got !== expected) { res.status(401).json({ error: "Unauthorized" }); return; }
  }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  const payload = {
    firstName: clean(d.firstName || d.first_name, 60),
    lastName:  clean(d.lastName  || d.last_name,  60),
    email:     validEmail(d.email),
    phone:     validPhone(d.phone),
    accountId: clean(d.accountId || d.account_id, 60),
  };

  // GHL needs at least one identifier to key the upsert on.
  if (!payload.email && !payload.phone) {
    res.status(200).json({ ok: true, skipped: "no_email_or_phone" });
    return;
  }

  // A signup with no phone still gets the email; note it so the SMS branch
  // in the workflow can be understood as intentionally skipped.
  const result = { ok: true, smsEligible: Boolean(payload.phone) };

  // ---- 1 + 2. upsert contact with portal fields ----
  let contact = { id: null };
  try { contact = await upsertContact(payload); }
  catch (e) { contact = { id: null, error: "exception" }; }
  result.contactId = contact.id;
  if (!contact.id) result.contactError = contact.error || contact.status;

  // ---- 3. tag -> fires the "Member Account Creation" workflow ----
  if (contact.id) {
    try {
      const tagged = await addTags(contact.id, [SIGNUP_TAG, "member-portal"]);
      result.tagged = Boolean(tagged.ok);
      if (!tagged.ok) result.tagError = tagged.status || tagged.skipped;
    } catch (e) { result.tagged = false; result.tagError = "exception"; }
  }

  // ---- 4. optional raw mirror ----
  try {
    const m = await mirrorToWebhook({
      event: "client_signup",
      ...payload,
      contactId: contact.id,
      created_iso: new Date().toISOString(),
      source: "vshealthbenefits.com",
      page: "/client.html",
    });
    if (!m.skipped) result.mirrored = Boolean(m.ok);
  } catch (e) { /* non-fatal */ }

  res.status(200).json(result);
};

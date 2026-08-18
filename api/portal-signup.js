// Vercel serverless function: a new member account was created in the client portal.
//
// Flow:
//   client.html signup form
//     -> POST /api/portal-signup   (this file)
//        1. Upsert the contact in GoHighLevel (creates or updates by email/phone)
//        2. Write portal custom fields (Admin Client ID)
//        3. Add the tags `portal-account-created` + `member-portal` (segmentation)
//        4. POST the payload to the GHL Inbound Webhook  <-- THIS IS THE TRIGGER
//           -> starts the "Member Account Creation" workflow, which sends:
//                - welcome email        (immediately)
//                - welcome SMS          (+5 min)
//                - website tour email   (+1 day, includes the referral payout)
//
// Why the webhook fires LAST:
//   The contact is upserted first, so by the time the workflow starts the record
//   already exists with every field populated. The payload carries `contact_id`,
//   so the workflow's first action can match the existing contact rather than
//   creating a duplicate - and {{contact.first_name}} resolves in the messages.
//
// Why this is server-side and not in client.html:
//   The GHL private integration token must never ship to the browser. client.html
//   is public. Only this function ever sees the token.
//
// HubSpot and EmailJS have been removed from this flow. GoHighLevel is the only
// destination - there is no second system to keep in sync and no duplicate email.
//
// ENV VARS (Vercel -> Project -> Settings -> Environment Variables):
//   GHL_PIT_TOKEN              REQUIRED for the contact upsert/tagging.
//                              No fallback on purpose - never hardcode it here.
//   GHL_LOCATION_ID            optional, defaults to the VS Health Benefits sub-account
//   GHL_SIGNUP_TAG             optional, defaults to "portal-account-created"
//   GHL_INBOUND_WEBHOOK_URL    optional override for the trigger URL below
//   PORTAL_SIGNUP_SECRET       optional shared secret; if set, callers must send it
//                              in the `x-vs-portal-secret` header.

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";

const LOCATION_ID = process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU";
const SIGNUP_TAG = process.env.GHL_SIGNUP_TAG || "portal-account-created";

// Inbound Webhook trigger for the "Member Account Creation" workflow.
// This URL is not a secret - it only accepts data, it never returns any.
const WEBHOOK_URL =
  process.env.GHL_INBOUND_WEBHOOK_URL ||
  "https://services.leadconnectorhq.com/hooks/cNCy6JUURpb4eBDdb9bU/webhook-trigger/f3ed39bb-f80b-4b00-bde2-bf8d18749512";

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

// Add the segmentation tags as a discrete event, after the contact is populated.
async function addTags(contactId, tags) {
  if (!contactId) return { ok: false, skipped: "no_contact" };
  return ghl("/contacts/" + contactId + "/tags", "POST", { tags: tags });
}

// Fire the Inbound Webhook that starts the workflow.
// This is the trigger, so it gets one retry - a dropped call means the member
// never receives their welcome email or SMS.
async function fireTrigger(payload) {
  if (!WEBHOOK_URL) return { ok: false, skipped: "no_webhook_url" };
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const r = await fetch(WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (r.ok) return { ok: true, status: r.status, attempts: attempt };
      if (attempt === 2) return { ok: false, status: r.status, attempts: attempt };
    } catch (e) {
      if (attempt === 2) {
        return { ok: false, error: String((e && e.message) || e), attempts: attempt };
      }
    }
    await new Promise(function (res) { setTimeout(res, 400); });
  }
  return { ok: false };
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

  // ---- 3. tags (segmentation only - the webhook below is the trigger) ----
  if (contact.id) {
    try {
      const tagged = await addTags(contact.id, [SIGNUP_TAG, "member-portal"]);
      result.tagged = Boolean(tagged.ok);
      if (!tagged.ok) result.tagError = tagged.status || tagged.skipped;
    } catch (e) { result.tagged = false; result.tagError = "exception"; }
  }

  // ---- 4. fire the Inbound Webhook -> starts "Member Account Creation" ----
  // Keys are sent in several shapes on purpose. GHL's inbound-webhook mapper
  // reads whatever key you point it at, and different actions in the builder
  // default to different conventions, so first_name / firstName / full_name are
  // all present. Do not remove one without checking the workflow mapping first.
  const first = payload.firstName;
  const fullName = (payload.firstName + " " + payload.lastName).trim();
  const trigger = {
    event: "client_signup",

    // contact identity - map these in the workflow's Create/Update Contact step
    contact_id: contact.id || "",
    contactId: contact.id || "",
    first_name: first,
    firstName: first,
    last_name: payload.lastName,
    lastName: payload.lastName,
    full_name: fullName,
    name: fullName,
    email: payload.email,
    phone: payload.phone,

    // portal metadata
    account_id: payload.accountId,
    accountId: payload.accountId,
    sms_eligible: Boolean(payload.phone),
    is_new_contact: Boolean(contact.isNew),

    // provenance
    created_iso: new Date().toISOString(),
    source: "vshealthbenefits.com",
    page: "/client.html",
    location_id: LOCATION_ID,
  };

  try {
    const t = await fireTrigger(trigger);
    result.triggered = Boolean(t.ok);
    if (!t.ok) result.triggerError = t.status || t.error || t.skipped;
  } catch (e) { result.triggered = false; result.triggerError = "exception"; }

  res.status(200).json(result);
};

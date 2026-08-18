// Vercel serverless function: a referral's status changed in the admin portal.
//
// Notifies the MEMBER WHO SENT THE REFERRAL (not the referred person) by SMS,
// every time you move a referral to a new status in admin.html.
//
// Flow:
//   admin.html  updateRef(id,{status:"sold"})
//     -> window.ghlReferralStatus(ref,newStatus)
//        -> POST /api/referral-status   (this file)
//           1. Upsert the REFERRER's contact in GHL (by email/phone)
//           2. Write custom fields:
//                contact.referral_name             "Maria Lopez"
//                contact.referral_status           "Sold"
//                contact.referral_status_message   the full SMS body
//                contact.referral_payout           "150.00"
//           3. Add tag `referral-status-updated`   <-- TRIGGERS the workflow
//              plus `referral-sold` on sold, `referral-paid` on paid
//
// The GHL workflow's SMS body is just {{contact.referral_status_message}}, so
// ALL copy lives here, in one place, in version control. Change the wording
// below and it changes everywhere without touching the workflow.
//
// The workflow MUST remove the `referral-status-updated` tag as its last step,
// and have Allow Re-Entry ON. Otherwise the second status change never fires.
//
// Custom field IDs are resolved at runtime by fieldKey, so nothing here breaks
// if the fields are recreated in GHL with different IDs.
//
// ENV VARS:
//   GHL_PIT_TOKEN            REQUIRED. Private integration token (pit-...).
//   GHL_LOCATION_ID          optional, defaults to the VS Health Benefits sub-account
//   PORTAL_SIGNUP_SECRET     optional shared secret; if set, callers must send it
//                            in the `x-vs-portal-secret` header.

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";
const LOCATION_ID = process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU";

// Must match REF_STATUSES in admin.html.
const STATUS_LABELS = {
  "in-progress": "In Progress",
  "being-reviewed": "Being Reviewed",
  "sold": "Sold",
  "declined": "Declined",
  "paid": "Paid",
};

// The middle clause of the SMS. Kept short on purpose - see buildMessage().
const STATUS_PHRASES = {
  "in-progress": "is in progress, we have started working on it",
  "being-reviewed": "is being reviewed by our team right now",
  "sold": "enrolled! Your payout is being processed",
  "declined": "could not be accepted this time",
  "paid": "payout has been sent. Thank you",
};

function clean(v, max) {
  return String(v == null ? "" : v).trim().slice(0, max || 120);
}

// The GSM-7 alphabet, which is what an SMS is encoded in when it can be.
const GSM7 =
  "@£$¥èéùìòÇ\nØø\rÅå" +
  "Δ_ΦΓΛΩΠΨΣΘΞÆæßÉ" +
  " !\"#¤%&'()*+,-./0123456789:;<=>?¡" +
  "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿" +
  "abcdefghijklmnopqrstuvwxyzäöñüà" +
  "^{}\\[~]|€";

// Strip anything that would push the message out of GSM-7 into UCS-2.
//
// This is not cosmetic. One stray character - "Jose" written "José" is fine,
// but "Núñez" is not, because ú is absent from GSM-7 - silently re-encodes the
// WHOLE message as UCS-2, where a segment is 70 characters instead of 160. A
// 150-character text quietly becomes three billed segments. Given how many
// clients here have Spanish names, that is a when, not an if.
//
// Accents are folded to their base letter (ú -> u) rather than dropped, so
// "Núñez" reads as "Nunez" instead of "Nez".
function gsmSafe(s) {
  let out = String(s == null ? "" : s).normalize("NFD").replace(/[̀-ͯ]/g, "");
  out = out.split("").map(function (ch) {
    return GSM7.indexOf(ch) >= 0 ? ch : " ";
  }).join("");
  return out.replace(/\s+/g, " ").trim();
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

// Build the SMS and guarantee a single 160-character segment.
// Two segments cost double, so the referral name is what gets trimmed - never
// the STOP notice, which is required for A2P/TCPA compliance.
//
// Every character used here is in the GSM-7 alphabet. That matters: a single
// non-GSM character (a curly quote, an em dash, an ellipsis "…") silently flips
// the whole message to UCS-2, where a segment is 70 characters, not 160. So the
// truncation marker is three ASCII dots, and the copy above avoids smart
// punctuation. Keep it that way when editing STATUS_PHRASES.
function buildMessage(firstName, referralName, status) {
  const phrase = STATUS_PHRASES[status] || ("was updated to " + (STATUS_LABELS[status] || status));
  const head = "VS Health Benefits: ";
  const tail = ". See vshealthbenefits.com/client. Reply STOP to opt out.";
  const name = gsmSafe(clean(referralName, 60)) || "your referral";

  let body = "Your referral for " + name + " " + phrase;
  let msg = head + body + tail;

  if (msg.length > 160) {
    const over = msg.length - 160;
    const keep = name.length - over - 3;
    const trimmed = keep > 3 ? name.slice(0, keep).trim() + "..." : "them";
    body = "Your referral for " + trimmed + " " + phrase;
    msg = head + body + tail;
  }
  if (msg.length > 160) msg = msg.slice(0, 157) + "...";
  return msg;
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

// Known custom field IDs for this location, used when the lookup below can't run.
//
// Reading /locations/{id}/customFields requires the `locations.readonly` scope.
// A private integration token created with only contacts scopes returns nothing
// there - silently, as an empty list, not an error. That produced a working tag
// with an EMPTY message field, which looks like "the SMS just didn't send".
// So: try the lookup, and fall back to these if it comes back empty.
//
// If you recreate any of these fields in GHL they get new IDs. Either add
// `locations.readonly` to the token so the lookup works, or update these.
const FALLBACK_FIELD_IDS = {
  referral_name: "yrFlqQhFeN8hJdaFBUtx",
  referral_status: "kcRLrUfM7uuVDnUqbse6",
  referral_status_message: "orTsedemCQasWAajYogD",
  referral_payout: "5VDbFGM4YjsW7Tx2165k",
};

// Resolve custom field ids by fieldKey, cached for the life of the warm lambda.
let FIELD_CACHE = null;
async function fieldIds() {
  if (FIELD_CACHE) return FIELD_CACHE;
  let map = {};
  try {
    const r = await ghl("/locations/" + LOCATION_ID + "/customFields?model=contact", "GET");
    const list = (r.json && r.json.customFields) || [];
    list.forEach(function (f) {
      if (f && f.fieldKey && f.id) map[String(f.fieldKey).replace(/^contact\./, "")] = f.id;
    });
  } catch (e) { map = {}; }

  // Fill any gap from the known-good IDs rather than writing a blank message.
  Object.keys(FALLBACK_FIELD_IDS).forEach(function (k) {
    if (!map[k]) map[k] = FALLBACK_FIELD_IDS[k];
  });

  FIELD_CACHE = map;
  return map;
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

  const p = {
    firstName: clean(d.referrerFirstName || d.firstName, 60),
    lastName:  clean(d.referrerLastName  || d.lastName,  60),
    email:     validEmail(d.referrerEmail || d.email),
    phone:     validPhone(d.referrerPhone || d.phone),
    referralName: clean(d.referralName, 80),
    status:    clean(d.status, 40).toLowerCase(),
    payout:    clean(d.payout, 20),
  };

  if (!p.email && !p.phone) {
    res.status(200).json({ ok: true, skipped: "no_referrer_contact" });
    return;
  }
  if (!p.status) {
    res.status(200).json({ ok: true, skipped: "no_status" });
    return;
  }

  const label = STATUS_LABELS[p.status] || p.status;
  const message = buildMessage(p.firstName, p.referralName, p.status);
  const out = { ok: true, status: p.status, label: label, message: message, smsLength: message.length };

  // ---- 1. upsert the referrer ----
  const F = await fieldIds();
  const customFields = [];
  function put(key, value) {
    if (F[key] && value) customFields.push({ id: F[key], value: value });
  }
  put("referral_name", p.referralName);
  put("referral_status", label);
  put("referral_status_message", message);
  put("referral_payout", p.payout);
  out.fieldsWritten = customFields.length;
  if (!customFields.length) out.fieldWarning = "no_matching_custom_fields";

  const body = { locationId: LOCATION_ID, source: "Referral status update" };
  if (p.firstName) body.firstName = p.firstName;
  if (p.lastName) body.lastName = p.lastName;
  if (p.email) body.email = p.email;
  if (p.phone) body.phone = p.phone;
  if (customFields.length) body.customFields = customFields;

  let contactId = null;
  try {
    const up = await ghl("/contacts/upsert", "POST", body);
    const c = up.json && (up.json.contact || up.json.data || up.json);
    if (up.ok && c && c.id) contactId = c.id;
    else out.contactError = up.status || up.skipped;
  } catch (e) { out.contactError = "exception"; }
  out.contactId = contactId;

  // ---- 2. tag -> TRIGGERS the workflow ----
  // The workflow removes `referral-status-updated` as its last step, which is
  // what lets the next status change re-fire it.
  if (contactId) {
    const tags = ["referral-status-updated"];
    if (p.status === "sold") tags.push("referral-sold");
    if (p.status === "paid") tags.push("referral-paid");
    try {
      const t = await ghl("/contacts/" + contactId + "/tags", "POST", { tags: tags });
      out.tagged = Boolean(t.ok);
      out.tags = tags;
      if (!t.ok) out.tagError = t.status || t.skipped;
    } catch (e) { out.tagged = false; out.tagError = "exception"; }
  }

  res.status(200).json(out);
};

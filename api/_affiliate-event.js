// Affiliate / creator program -> GoHighLevel messages (added 2026-11-13).
//
// POST /api/affiliate-event  { id, event, key }
//   (rewritten to /api/voice-lookup?op=affiliate-event, Vercel Hobby 12-function limit)
//
// The admin portal stays the record of the program (vs_state/affiliates).
// GHL only does the talking. For every event this:
//   1. finds the creator in Firestore and checks the event really happened
//      there (approved with a code / referral marked qualified / payout recorded),
//      so a forged request can't make us text anyone,
//   2. writes the copy into the creator's GHL contact custom fields
//        affiliate_subject, affiliate_sms, affiliate_email, affiliate_link,
//        affiliate_event_key
//   3. removes and re-adds the tag `affiliate-update`, which TRIGGERS the GHL
//      workflow "Affiliate - Send Update" (SMS {{contact.affiliate_sms}} +
//      email {{contact.affiliate_subject}} / {{contact.affiliate_email}}).
//      Plus a status tag: affiliate-approved / affiliate-referral-qualified /
//      affiliate-paid / affiliate-got-referral.
//
// ALL wording lives here. No dollar amounts are ever sent (Bradley's call), and
// the "someone used your link" text never says who: the creator learns nothing
// about the person they referred.
//
// Events: applied (from _affiliate-apply.js), approved, referral (from
// lead-sync.js), qualified, paid. Same event key twice in a row is skipped, so
// a double click or a lead re-syncing never sends a second text.

const L = require("./_lib");
const F = require("./_fs");

const SITE_SHORT = "vshealthbenefits.com";
const TRIGGER_TAG = "affiliate-update";
const STATUS_TAG = { applied: "affiliate-applicant", approved: "affiliate-approved", referral: "affiliate-got-referral", qualified: "affiliate-referral-qualified", paid: "affiliate-paid" };

// Known field ids for this location; the lookup by fieldKey below wins when the
// token can read custom fields.
const FALLBACK_FIELD_IDS = {
  affiliate_subject: "BiYiH6v9gJ0IeNO8ZCUR",
  affiliate_sms: "FtmpNLaDon73jCAc1paL",
  affiliate_email: "7MRru3sbdFQIGRe7qsjM",
  affiliate_link: "NYxqtrDFblOWfxSWq8cS",
  affiliate_event_key: "1nnPpz6d01BEsmL2ifmb",
};

// GHL pipeline "Affiliates" (created 2026-11-13). Each event moves the creator's card.
const AFF_PIPELINE = "nv4TDoBMaSUfGSCuszWQ";
const AFF_STAGE = {
  applied: "565cca44-bb2e-4b04-ba5e-5e8c0bae418d",   // Applied
  approved: "32ef7171-bda6-4dc6-8ae6-223a456990e7",  // Approved (link sent)
  referral: "fd8d358a-83f7-46e6-8d89-f23e315dad41",  // Sending referrals
  qualified: "fd8d358a-83f7-46e6-8d89-f23e315dad41", // Sending referrals
  paid: "30483e0b-70fa-4852-a37d-8edfd07ab381",      // Paid
};
const LOC = process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU";

async function moveCard(cid, c, event) {
  const stage = AFF_STAGE[event];
  if (!stage) return "no_stage";
  try {
    const name = ((String(c.firstName || "") + " " + String(c.lastName || "")).trim() || "Creator") + (c.code ? " (/" + normCode(c.code) + ")" : "");
    const q = "/opportunities/search?location_id=" + LOC + "&pipeline_id=" + AFF_PIPELINE + "&contact_id=" + encodeURIComponent(cid) + "&status=all&limit=1";
    const f = await L.ghl(q, "GET");
    const list = f.json && (f.json.opportunities || f.json.data);
    if (f.ok && Array.isArray(list) && list.length) {
      const u = await L.ghl("/opportunities/" + list[0].id, "PUT", { pipelineId: AFF_PIPELINE, pipelineStageId: stage, name: name, status: "open" });
      return u.ok ? "moved" : "move_failed_" + u.status;
    }
    const r = await L.ghl("/opportunities/", "POST", { locationId: LOC, pipelineId: AFF_PIPELINE, pipelineStageId: stage, contactId: cid, name: name, status: "open", source: "Creator program" });
    return r.ok ? "created" : "create_failed_" + r.status;
  } catch (e) { return "error"; }
}

let FIELD_CACHE = null;
async function fieldIds() {
  if (FIELD_CACHE) return FIELD_CACHE;
  const map = {};
  try {
    const r = await L.ghl("/locations/" + (process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU") + "/customFields?model=contact", "GET");
    ((r.json && r.json.customFields) || []).forEach(function (f) {
      if (f && f.fieldKey && f.id) map[String(f.fieldKey).replace(/^contact\./, "")] = f.id;
    });
  } catch (e) { /* fall back below */ }
  Object.keys(FALLBACK_FIELD_IDS).forEach(function (k) { if (!map[k] && FALLBACK_FIELD_IDS[k]) map[k] = FALLBACK_FIELD_IDS[k]; });
  if (map.affiliate_sms) FIELD_CACHE = map;
  return map;
}

function gsm(s) {
  return String(s == null ? "" : s).normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/[–—]/g, "-")
    .replace(/[^\x20-\x7E\n]/g, " ").replace(/[ \t]+/g, " ").trim();
}
function first(c) { return gsm(String((c && c.firstName) || "").split(" ")[0]).slice(0, 20); }
function normCode(v) { return String(v || "").toLowerCase().replace(/[^a-z0-9-]/g, "").slice(0, 40); }

// Copy for each event: { subject, sms, email }. SMS kept GSM-7 and short.
function copy(event, c) {
  const n = first(c), hi = n ? "Hi " + n + "! " : "Hi! ";
  const link = c.code ? SITE_SHORT + "/" + normCode(c.code) : "";
  const stop = " Reply STOP to opt out.";
  const sign = "\n\n- Bradley Vilsaint\nVS Health Benefits\n(954) 825-1009";
  switch (event) {
    case "applied": return {
      subject: "We got your creator application",
      sms: "VS Health Benefits: " + hi + "Thanks for applying to our creator program! We'll review it and text you within 2 business days." + stop,
      email: hi + "\n\nThanks for applying to the VS Health Benefits creator program. We review every application within 2 business days.\n\nIf you're approved, you'll get your own personal link to share with your audience. We'll text and email you as soon as it's ready." + sign,
    };
    case "approved": return {
      subject: "You're approved! Here's your link",
      sms: "VS Health Benefits: " + hi + "You're approved! Your link: " + link + " - we'll text you when someone uses it." + stop,
      email: hi + "\n\nYou're approved for the VS Health Benefits creator program.\n\nYour personal link: https://www." + link + "\n\nEveryone who comes through your link and asks for a quote is credited to you. You earn a flat reward for every qualified referral (they complete a free consultation with one of our licensed advisors), whether or not they buy.\n\nA few quick rules:\n- Share your own experience in your own words.\n- Label sponsored posts #ad or #partner.\n- Please don't quote prices, plans or coverage details. Our licensed advisors handle that.\n\nWe'll let you know every time someone uses your link.\n\nSee your visits, referrals and earnings any time: https://www." + SITE_SHORT + "/creator (sign in with this email address)." + sign,
    };
    case "referral": return {
      subject: "Someone just used your link",
      sms: "VS Health Benefits: " + hi + "Someone just used your link! It counts once they finish a consultation with us." + stop,
      email: hi + "\n\nSomeone just used your link (https://www." + link + ") to ask us for a quote.\n\nOnce they complete a free consultation with one of our licensed advisors, it counts as a qualified referral and earns your reward. We'll let you know when that happens.\n\nKeep sharing!" + sign,
    };
    case "qualified": return {
      subject: "You earned a referral reward",
      sms: "VS Health Benefits: Nice work" + (n ? ", " + n : "") + "! A referral of yours finished a consultation. Your reward is on the way." + stop,
      email: hi + "\n\nGood news: one of the people you referred just completed a consultation with our team, so it counts as a qualified referral and your reward is on its way.\n\nThank you for sharing VS Health Benefits!\n\nYour link: https://www." + link + sign,
    };
    case "login": return {
      subject: "Your creator dashboard sign-in link",
      sms: "VS Health Benefits: Your creator dashboard sign-in link (works 30 min): " + (c._loginUrl || "") + stop,
      email: hi + "\n\nHere's your sign-in link for your creator dashboard. It works for 30 minutes:\n\n" + (c._loginUrl || "") + sign,
    };
    case "paid": return {
      subject: "Your creator reward was sent",
      sms: "VS Health Benefits: " + hi + "Your creator reward payment was just sent. Thank you for sharing VS Health Benefits!" + stop,
      email: hi + "\n\nYour creator reward payment was just sent. Thank you for helping people get covered!\n\nKeep sharing your link: https://www." + link + sign,
    };
  }
  return null;
}

// Does the portal record show this event really happened?
function valid(event, c, key) {
  if (!c) return false;
  const st = String(c.stage || "");
  if (event === "applied") return true;
  if (st === "declined" || st === "paused") return false;
  if (event === "approved") return !!normCode(c.code) && (st === "approved" || st === "active");
  if (event === "referral") return !!normCode(c.code);
  if (event === "qualified") { const r = c.refs && c.refs[key]; return !!(r && r.q); }
  if (event === "paid") return (c.payouts || []).some(function (p) { return p && p.id === key; });
  return false;
}

async function findCreator(match) {
  const r = await F.readStore("affiliates");
  if (!r.ok) return null;
  return (r.items || []).filter(match)[0] || null;
}

// Core: send one event to one creator record. Used by the endpoint below, by
// _affiliate-apply.js (applied) and by lead-sync.js (referral).
async function notify(c, event, key) {
  const out = { event: event };
  const msg = copy(event, c);
  if (!msg) return Object.assign(out, { skipped: "unknown_event" });
  const email = String(c.email || "").trim().toLowerCase(), phone = String(c.phone || "").trim();
  if (!email && !phone && !c.ghlContactId) return Object.assign(out, { skipped: "no_contact_info" });

  let cid = c.ghlContactId || null;
  if (!cid) cid = await L.upsertContact({ firstName: c.firstName, lastName: c.lastName, email: email, phone: phone, state: c.state, website_lead_stage: "Affiliate / creator" });
  if (!cid) return Object.assign(out, { skipped: "no_ghl_contact" });
  out.contactId = cid;
  out.pipeline = await moveCard(cid, c, event);

  const eventKey = event + ":" + (key || "") + ":" + (c.id || "");
  // Skip a repeat of the last event (double click, a lead re-syncing).
  try {
    const g = await L.ghl("/contacts/" + cid, "GET");
    const f = await fieldIds();
    const cf = (g.json && g.json.contact && g.json.contact.customFields) || [];
    const last = cf.filter(function (x) { return x && x.id === f.affiliate_event_key; })[0];
    if (last && String(last.value || "") === eventKey) return Object.assign(out, { skipped: "duplicate" });
  } catch (e) { /* send anyway */ }

  const f = await fieldIds();
  const fields = [];
  function put(k, v) { if (f[k]) fields.push({ id: f[k], field_value: v, value: v }); }
  put("affiliate_subject", msg.subject);
  put("affiliate_sms", msg.sms);
  // Email body goes in as HTML so the line breaks survive the GHL email builder.
  put("affiliate_email", L.esc(msg.email).replace(/(https:\/\/www\.[^\s<]+)/g, '<a href="$1">$1</a>').replace(/\n/g, "<br>"));
  put("affiliate_link", c.code ? "https://www." + SITE_SHORT + "/" + normCode(c.code) : "");
  put("affiliate_event_key", eventKey);
  if (!fields.length) return Object.assign(out, { skipped: "custom_fields_missing" });
  const u = await L.ghl("/contacts/" + cid, "PUT", { customFields: fields });
  out.fields = u.ok;
  if (!u.ok) return Object.assign(out, { skipped: "field_write_failed_" + u.status });

  // Re-arm the trigger tag, then add it (a tag already on the contact doesn't fire).
  try { await L.ghl("/contacts/" + cid + "/tags", "DELETE", { tags: [TRIGGER_TAG] }); } catch (e) {}
  const t = await L.ghl("/contacts/" + cid + "/tags", "POST", { tags: [TRIGGER_TAG, STATUS_TAG[event], "creator"].filter(Boolean) });
  out.sent = !!t.ok;
  return out;
}

async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }
  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};
  const id = String(d.id || "").slice(0, 60), event = String(d.event || "").slice(0, 20), key = String(d.key || "").slice(0, 120);
  // Only the portal's events come through here; applied/referral are server-side.
  if (!id || ["approved", "qualified", "paid"].indexOf(event) < 0) { res.status(400).json({ ok: false, error: "bad_request" }); return; }

  // The portal's Firestore save can land a moment after this call, so look twice.
  let c = null;
  for (let i = 0; i < 3; i++) {
    c = await findCreator(function (x) { return x && x.id === id; });
    if (valid(event, c, key)) break;
    c = null;
    await new Promise(function (r) { setTimeout(r, 1500); });
  }
  if (!c) { res.status(200).json({ ok: false, skipped: "not_confirmed_in_portal" }); return; }
  const out = await notify(c, event, key);
  res.status(200).json(Object.assign({ ok: true }, out));
}

module.exports = handler;
module.exports.notify = notify;
module.exports.findCreator = findCreator;
module.exports.valid = valid;
module.exports.copy = copy;
// Sign-in link fallback when the site's own email sender is down.
module.exports.notifyLogin = function (c, url) { return notify(Object.assign({}, c, { _loginUrl: url }), "login", String(Date.now())); };

// Vercel serverless function: receive a WEBCHAT (GHL AI bot) lead.
//
// Lead destinations (HubSpot has been removed):
//   1. GHL  — already captures the lead natively via the Live Chat widget +
//             Conversation AI. Nothing to do here; the contact exists in GHL
//             before this webhook ever fires.
//   2. VS admin portal — appended to the Firestore document `vs_state/leads`,
//             which admin.html mirrors into localStorage via onSnapshot. The
//             portal updates live, no refresh needed.
//   3. Email — an internal alert so a lead never sits unseen.
//
// Auth: GHL must send a shared secret in the `x-vs-webhook-secret` header
//       (or `?key=` query param) matching env var WEBCHAT_WEBHOOK_SECRET.
//       If the env var is unset the check is skipped so you can test first.
//
// Safe by design: every step is wrapped so a failure in one destination never
// breaks the others, and the function always returns 200 so GHL never
// retry-loops.
//
// ENV VARS (Vercel -> Project -> Settings -> Environment Variables):
//   WEBCHAT_WEBHOOK_SECRET   shared secret GHL sends. Strongly recommended.
//   RESEND_API_KEY / NOTIFY_EMAIL   see api/_lib.js
//   FIREBASE_API_KEY         optional; defaults to the public web key below.
//
// Note: the Firebase web API key is public by design (it is already in
// admin.html). Access is governed by Firestore security rules, not secrecy.

const L = require("./_lib");

const FB_API_KEY = process.env.FIREBASE_API_KEY || "AIzaSyCbZ7Otrz6yPlxJuLlDPEoMzssgsWkjo5U";
const FB_PROJECT = process.env.FIREBASE_PROJECT_ID || "vs-benefits-c1da9";
const FS_DOC =
  "https://firestore.googleapis.com/v1/projects/" + FB_PROJECT +
  "/databases/(default)/documents/vs_state/leads";

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

// Digits-only US phone, 10 digits (drops a leading country code). "" if invalid.
function validPhone(v) {
  let d = clean(v, 25).replace(/\D/g, "");
  if (d.length === 11 && d.charAt(0) === "1") d = d.slice(1);
  if (d.length !== 10) return "";
  if (/^(\d)\1{9}$/.test(d)) return "";
  if (d.slice(0, 3) === "555" || d.slice(3, 6) === "555") return "";
  return d;
}

// Accepts MM/DD/YYYY, M/D/YYYY, YYYY-MM-DD. Returns YYYY-MM-DD or "".
// Rejects ages outside 14-100 so junk/typos never reach the portal.
function validDob(v) {
  const s = clean(v, 20);
  if (!s) return "";
  let y, m, d;
  let mm = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (mm) { y = +mm[1]; m = +mm[2]; d = +mm[3]; }
  else {
    mm = /^(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})$/.exec(s);
    if (!mm) return "";
    m = +mm[1]; d = +mm[2]; y = +mm[3];
  }
  if (m < 1 || m > 12 || d < 1 || d > 31) return "";
  const dt = new Date(Date.UTC(y, m - 1, d));
  if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== m - 1 || dt.getUTCDate() !== d) return "";
  const age = (Date.now() - dt.getTime()) / 31557600000;
  if (age < 14 || age > 100) return "";
  return y + "-" + String(m).padStart(2, "0") + "-" + String(d).padStart(2, "0");
}

// "$65,000" / "65k" / "65000" -> 65000. Returns "" if not sane.
function validIncome(v) {
  let s = clean(v, 20).toLowerCase().replace(/[$,\s]/g, "");
  let mult = 1;
  if (/k$/.test(s)) { mult = 1000; s = s.slice(0, -1); }
  const n = parseFloat(s);
  if (!isFinite(n) || n <= 0) return "";
  const val = Math.round(n * mult);
  if (val < 1000 || val > 5000000) return "";
  return String(val);
}

// Normalise the pain point into a fixed set so reporting stays clean.
function normalizePain(v) {
  const s = clean(v, 200).toLowerCase();
  if (!s) return "";
  if (/(lost|lose|losing|laid off|terminated|cobra|left my job|quit)/.test(s)) return "Lost coverage";
  if (/(too much|expensive|costly|high premium|cheaper|afford|price|save)/.test(s)) return "Paying too much";
  if (/(never|first time|no insurance|uninsured|dont have|don't have)/.test(s)) return "Never had coverage";
  return "Other";
}

const PAIN_LABEL = {
  "Lost coverage": "Lost their coverage",
  "Paying too much": "Overpaying for current plan",
  "Never had coverage": "Has never had coverage",
  "Other": "Other / needs discovery",
};

// ---------- Firestore REST helpers ----------
// Encode a plain JS value into Firestore's typed representation.
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

// Decode Firestore's typed representation back into plain JS.
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

// Sign in anonymously, exactly as admin.html does in the browser.
async function fsToken() {
  const r = await fetch(
    "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + FB_API_KEY,
    { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ returnSecureToken: true }) }
  );
  if (!r.ok) return null;
  const j = await r.json();
  return j.idToken || null;
}

// Append one lead to vs_state/leads, preserving everything already there.
// Read-modify-write: fine at webchat volume, but two leads landing in the
// same second could theoretically collide. Worth revisiting if volume grows.
async function pushLeadToPortal(lead) {
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

  // Skip if this exact lead already landed (same phone or email today).
  const dupe = items.some(function (it) {
    if (!it) return false;
    const samePhone = lead.phone && it.phone === lead.phone;
    const sameEmail = lead.email && it.email === lead.email;
    return (samePhone || sameEmail) && it.createdAt === lead.createdAt;
  });
  if (dupe) return { ok: true, skipped: "duplicate", total: items.length };

  items.push(lead);

  const body = {
    fields: {
      items: fsEncode(items),
      ts: { integerValue: String(Date.now()) },
    },
  };
  const put = await fetch(FS_DOC, {
    method: "PATCH",
    headers: Object.assign({ "Content-Type": "application/json" }, auth),
    body: JSON.stringify(body),
  });
  if (!put.ok) return { ok: false, reason: "write_failed_" + put.status };
  return { ok: true, total: items.length };
}

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, x-vs-webhook-secret");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  // ---- shared-secret check (skipped if env var not set, so you can test) ----
  const expected = process.env.WEBCHAT_WEBHOOK_SECRET;
  if (expected) {
    const got = String(
      (req.headers && req.headers["x-vs-webhook-secret"]) ||
      (req.query && req.query.key) || ""
    );
    if (got !== expected) { res.status(401).json({ error: "Unauthorized" }); return; }
  }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  // GHL field names vary by how the workflow is mapped, so accept common aliases.
  const firstName = clean(d.firstName || d.first_name || d.firstname, 60);
  const lastName  = clean(d.lastName  || d.last_name  || d.lastname,  60);
  const email     = validEmail(d.email || d.contactEmail);
  const phone     = validPhone(d.phone || d.phoneNumber || d.contactPhone);
  const dob       = validDob(d.dob || d.dateOfBirth || d.date_of_birth || d.birthday);
  const income    = validIncome(d.income || d.yearlyIncome || d.annualIncome || d.household_income);
  const painRaw   = clean(d.painPoint || d.pain_point || d.reason || d.situation, 200);
  const pain      = normalizePain(painRaw);
  const state     = clean(d.state, 40);
  const zip       = clean(d.zip || d.postalCode, 12);
  const notesIn   = clean(d.notes || d.transcript || d.summary, 4000);
  const ghlId     = clean(d.contactId || d.ghl_contact_id, 60);

  // Need at least one durable identifier to be worth writing.
  if (!email && !phone) {
    res.status(200).json({ ok: true, skipped: "no_email_or_phone" });
    return;
  }

  const fullName = (firstName + " " + lastName).trim() || "Unknown";
  const nowIso = new Date().toISOString();
  const today = nowIso.slice(0, 10);

  // Notes shown in the portal's lead detail.
  const noteLines = [];
  if (pain) noteLines.push("Pain point: " + (PAIN_LABEL[pain] || pain));
  if (painRaw && painRaw.toLowerCase() !== pain.toLowerCase()) {
    noteLines.push("In their words: " + painRaw);
  }
  if (income) noteLines.push("Yearly income: $" + Number(income).toLocaleString("en-US"));
  if (ghlId) noteLines.push("GHL contact: " + ghlId);
  if (notesIn) noteLines.push("Chat detail: " + notesIn);
  noteLines.push("Source: Website live chat");

  // Shape matches the lead objects admin.html creates, so the portal
  // renders it without any changes on the front end.
  const lead = {
    id: "wc_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8),
    firstName: firstName,
    lastName: lastName,
    email: email,
    phone: phone,
    dob: dob,
    address: "",
    state: state,
    zipCode: zip,
    notes: noteLines.join("\n"),
    quoteValue: 0,
    stage: "new",
    followUpDue: today,
    lastContact: today,
    createdAt: today,
    created: Date.now(),
    source: "webchat",
    painPoint: pain,
    yearlyIncome: income,
    activity: [{ ts: Date.now(), type: "created", text: "Captured from website live chat" }],
  };

  // ---- 1. VS admin portal (Firestore) ----
  let portal = { ok: false, reason: "not_attempted" };
  try { portal = await pushLeadToPortal(lead); }
  catch (e) { portal = { ok: false, reason: "exception" }; }

  // ---- 2. Internal alert email ----
  try {
    const rows = [
      ["Name", fullName],
      ["Phone", phone || "—"],
      ["Email", email || "—"],
      ["DOB", dob || "—"],
      ["Yearly income", income ? "$" + Number(income).toLocaleString("en-US") : "—"],
      ["Pain point", PAIN_LABEL[pain] || pain || "—"],
      ["In their words", painRaw || "—"],
      ["ZIP", zip || "—"],
    ];
    const table =
      '<table style="border-collapse:collapse;font:15px/1.5 system-ui,sans-serif">' +
      rows.map(function (r) {
        return '<tr><td style="padding:4px 14px 4px 0;color:#5a6b80">' + L.esc(r[0]) +
               '</td><td style="padding:4px 0"><b>' + L.esc(r[1]) + "</b></td></tr>";
      }).join("") + "</table>";

    await L.sendEmail({
      to: L.CFG.notify,
      subject: "New webchat lead: " + fullName + (pain ? " (" + pain + ")" : ""),
      html: L.shell(
        "<h2 style=\"margin:0 0 12px;color:" + L.CFG.navy + "\">New webchat lead</h2>" +
        table +
        (notesIn ? '<p style="margin-top:16px;color:#5a6b80">' + L.esc(notesIn).slice(0, 1200) + "</p>" : "") +
        '<p style="margin-top:16px;color:#5a6b80;font-size:13px">' +
        (portal.ok ? "Added to your admin portal." : "Could not reach the admin portal — this email is the record.") +
        "</p>" +
        L.btn("https://www.vshealthbenefits.com/admin", "Open admin portal"),
        "New webchat lead from " + fullName
      ),
      replyTo: email || undefined,
    });
  } catch (e) { /* non-fatal */ }

  res.status(200).json({ ok: true, portal: portal, leadId: lead.id });
};

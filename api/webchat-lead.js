// Vercel serverless function: receive a WEBCHAT (GHL AI bot) lead.
//
// GoHighLevel's Conversation AI / Workflow posts here via an Outbound Webhook
// once the bot has collected the visitor's details. This function:
//   1. Validates + sanitises every field server-side (never trust the sender).
//   2. Creates/updates the contact in HubSpot, tagged with the pain point.
//   3. Adds a note with the full chat-captured detail.
//   4. Emails Bradley an internal alert so nothing sits unseen.
//
// Auth: GHL must send a shared secret in the `x-vs-webhook-secret` header
//       (or `?key=` query param) matching env var WEBCHAT_WEBHOOK_SECRET.
//       If the env var is unset the check is skipped so you can test first.
//
// Safe by design: if HUBSPOT_PRIVATE_APP_TOKEN or RESEND_API_KEY are missing the
// relevant step is skipped and the function still returns 200, so GHL never sees
// a failed webhook and never retries in a loop.
//
// ENV VARS (Vercel -> Project -> Settings -> Environment Variables):
//   WEBCHAT_WEBHOOK_SECRET      shared secret GHL sends. Strongly recommended.
//   HUBSPOT_PRIVATE_APP_TOKEN   already used by the other endpoints
//   RESEND_API_KEY / NOTIFY_EMAIL   see api/_lib.js
//
// See api/_lib.js for shared helpers.

const L = require("./_lib");

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
// Rejects ages outside 14-100 so junk/typos never reach the CRM.
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
  const notes     = clean(d.notes || d.transcript || d.summary, 4000);
  const ghlId     = clean(d.contactId || d.ghl_contact_id, 60);

  // Need at least one durable identifier to be worth writing.
  if (!email && !phone) {
    res.status(200).json({ ok: true, skipped: "no_email_or_phone" });
    return;
  }

  // ---- HubSpot ----
  // Build the property set once; it is identical whether we key off email or phone.
  const hsProps = {
    firstname: firstName,
    lastname: lastName,
    phone: phone,
    state: state,
    zip: zip,
    date_of_birth: dob,
    annual_income: income,
    website_lead_stage: pain ? "Webchat — " + pain : "Webchat lead",
    hs_lead_status: "NEW",
    lifecyclestage: "lead",
  };
  if (email) hsProps.email = email;

  // Drop empty values so we never overwrite a good field with "".
  function pruned(o) {
    const out = {};
    Object.keys(o).forEach(function (k) {
      if (o[k] != null && String(o[k]).trim() !== "") out[k] = String(o[k]).trim();
    });
    return out;
  }

  // Find an existing contact by phone. HubSpot stores phone in several formats,
  // so try the raw 10 digits and the common +1/E.164 form before giving up.
  async function findByPhone(p) {
    if (!p) return null;
    const variants = [p, "+1" + p, "1" + p];
    for (const v of variants) {
      const r = await L.hs("/crm/v3/objects/contacts/search", "POST", {
        filterGroups: [{ filters: [{ propertyName: "phone", operator: "EQ", value: v }] }],
        properties: ["phone"],
        limit: 1,
      });
      if (r.ok && r.json && r.json.results && r.json.results[0]) return r.json.results[0].id;
    }
    return null;
  }

  let contactId = null;
  try {
    if (email) {
      // Email is the strongest dedupe key — use the shared helper.
      contactId = await L.upsertContact(hsProps);
    } else if (phone) {
      // No email (the webchat flow does not ask for one). Key off phone instead so
      // the lead still reaches the CRM rather than living only in an alert email.
      const existing = await findByPhone(phone);
      if (existing) {
        await L.hs("/crm/v3/objects/contacts/" + existing, "PATCH", { properties: pruned(hsProps) });
        contactId = existing;
      } else {
        const created = await L.hs("/crm/v3/objects/contacts", "POST", { properties: pruned(hsProps) });
        contactId = created.ok && created.json ? created.json.id : null;
      }
    }
  } catch (e) { /* non-fatal */ }

  const fullName = (firstName + " " + lastName).trim() || "Unknown";

  // ---- Note on the contact ----
  try {
    if (contactId) {
      const rows = [
        "Name: " + L.esc(fullName),
        phone  ? "Phone: " + L.esc(phone) : "",
        email  ? "Email: " + L.esc(email) : "",
        dob    ? "DOB: " + L.esc(dob) : "",
        income ? "Yearly income: $" + L.esc(Number(income).toLocaleString("en-US")) : "",
        pain   ? "Pain point: " + L.esc(PAIN_LABEL[pain] || pain) : "",
        painRaw && painRaw.toLowerCase() !== pain.toLowerCase()
          ? "In their words: " + L.esc(painRaw) : "",
        ghlId  ? "GHL contact: " + L.esc(ghlId) : "",
      ].filter(Boolean);
      let html = "<b>Website webchat lead</b><br>" + rows.join("<br>");
      if (notes) html += "<br><br><b>Chat detail</b><br>" + L.esc(notes).replace(/\n/g, "<br>");
      await L.addNoteToContact(contactId, html);
    }
  } catch (e) { /* non-fatal */ }

  // ---- Internal alert email ----
  try {
    const rows = [
      ["Name", fullName],
      ["Phone", phone || "—"],
      ["Email", email || "—"],
      ["DOB", dob || "—"],
      ["Yearly income", income ? "$" + Number(income).toLocaleString("en-US") : "—"],
      ["Pain point", PAIN_LABEL[pain] || pain || "—"],
      ["In their words", painRaw || "—"],
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
        (notes ? '<p style="margin-top:16px;color:#5a6b80">' + L.esc(notes).slice(0, 1200) + "</p>" : "") +
        (contactId
          ? L.btn("https://app.hubspot.com/contacts/_/contact/" + contactId, "Open in HubSpot")
          : ""),
        "New webchat lead from " + fullName
      ),
      replyTo: email || undefined,
    });
  } catch (e) { /* non-fatal */ }

  res.status(200).json({ ok: true, contactId: contactId });
};

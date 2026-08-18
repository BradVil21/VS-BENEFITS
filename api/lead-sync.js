// Vercel serverless function: generic lead / email capture -> GoHighLevel.
//
// This is the replacement for the hidden HubSpot form endpoint
// (api-na2.hsforms.com/.../submit/246725050/...) that used to be pasted into
// half a dozen pages as `window.hubspotSyncLead`, plus the newsletter and
// "remind me before the deadline" forms.
//
// Those all did the same thing: take an email (plus whatever else was handy)
// and put a contact in the CRM. So they all now post here instead, and the
// token stays server-side where it belongs - the HubSpot version shipped a
// portal ID and form GUID to the browser on every page.
//
// Callers:
//   admin.html            leads saved or imported in the admin portal
//   get-a-quote.html      quote funnel
//   quote/index.html      quote funnel
//   contact.html          contact form (in addition to the support ticket)
//   aca-subsidy-calculator.html
//   open-enrollment.html
//   newsletter / deadline-reminder forms on blog + landing pages
//
// Safe by design: always returns 200 so a form never breaks, and skips quietly
// when there is nothing usable to write.
//
// ENV VARS:
//   GHL_PIT_TOKEN     required for the write; without it this no-ops.
//   GHL_LOCATION_ID   optional, defaults to the VS Health Benefits sub-account

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

// Tags must be safe to create in bulk: lowercase, hyphenated, no surprises.
function normTag(v) {
  return clean(v, 40).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
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
    try { json = await r.json(); } catch (e) { /* ignore */ }
    return { ok: r.ok, status: r.status, json };
  } catch (e) {
    return { ok: false, status: 0, json: null, error: String((e && e.message) || e) };
  }
}

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  const p = {
    firstName: clean(d.firstName || d.first_name || d.firstname, 60),
    lastName:  clean(d.lastName  || d.last_name  || d.lastname,  60),
    email:     validEmail(d.email),
    phone:     validPhone(d.phone),
    company:   clean(d.company || d.businessName, 120),
    state:     clean(d.state, 4).toUpperCase(),
    zip:       clean(d.zip || d.zipCode, 12),
    source:    clean(d.source || d.leadSource, 80) || "Website",
    notes:     clean(d.notes, 1500),
  };

  if (!p.email && !p.phone) {
    res.status(200).json({ ok: true, skipped: "no_email_or_phone" });
    return;
  }

  const out = { ok: true };

  const body = { locationId: LOCATION_ID, source: p.source };
  if (p.email) body.email = p.email;
  if (p.phone) body.phone = p.phone;
  if (p.firstName) body.firstName = p.firstName;
  if (p.lastName) body.lastName = p.lastName;
  if (p.firstName || p.lastName) body.name = (p.firstName + " " + p.lastName).trim();
  if (p.company) body.companyName = p.company;
  if (p.state) body.state = p.state;
  if (p.zip) body.postalCode = p.zip;

  let contactId = null;
  try {
    const up = await ghl("/contacts/upsert", "POST", body);
    const c = up.json && (up.json.contact || up.json.data || up.json);
    if (up.ok && c && c.id) contactId = c.id;
    else out.contactError = up.status || up.skipped;
  } catch (e) { out.contactError = "exception"; }
  out.contactId = contactId;

  if (contactId) {
    const tags = ["website-lead"];
    const raw = Array.isArray(d.tags) ? d.tags : (d.tag ? [d.tag] : []);
    raw.slice(0, 8).forEach(function (t) { const n = normTag(t); if (n) tags.push(n); });
    try {
      const t = await ghl("/contacts/" + contactId + "/tags", "POST", { tags: tags });
      out.tagged = Boolean(t.ok);
      out.tags = tags;
    } catch (e) { out.tagged = false; }

    if (p.notes) {
      try { await ghl("/contacts/" + contactId + "/notes", "POST", { body: p.notes }); out.noted = true; }
      catch (e) { out.noted = false; }
    }
  }

  res.status(200).json(out);
};

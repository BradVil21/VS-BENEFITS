// Vercel serverless function: the lead bridge between the website, the admin
// portal and GoHighLevel. It runs in two directions.
//
//   to-crm     (default)  portal / website form  ->  GoHighLevel contact
//   to-portal            GoHighLevel workflow    ->  admin portal pipeline
//
// Both live in one file because Vercel's Hobby plan allows 12 serverless
// functions per deployment and api/ is at the cap. They are otherwise
// unrelated; the direction is chosen once, at the top of the handler, and the
// two halves share nothing but the sanitisers.
//
// ── to-crm ─────────────────────────────────────────────────────────────────
// The replacement for the hidden HubSpot form endpoint that used to be pasted
// into half a dozen pages as `window.hubspotSyncLead`, plus the newsletter and
// "remind me before the deadline" forms. They all did the same thing - take an
// email and put a contact in the CRM - so they all post here instead, and the
// token stays server-side where it belongs.
//
//   admin.html            leads saved or imported in the admin portal
//   get-a-quote.html      quote funnel
//   quote/index.html      quote funnel
//   contact.html          contact form (in addition to the support ticket)
//   aca-subsidy-calculator.html
//   open-enrollment.html
//   newsletter / deadline-reminder forms on blog + landing pages
//
// ── to-portal ──────────────────────────────────────────────────────────────
//   POST /api/lead-sync?to=portal
//
// One inbound webhook for every lead that lands in GoHighLevel, routed into
// the right board of the admin portal:
//
//                                    business? -> vs_state/biz_leads  (Business Leads -> Prospect)
//                                    otherwise -> vs_state/leads      (Pipeline -> New Lead)
//
// Before this existed, only the website's own forms reached the portal. A lead
// GHL created some other way - the live chat bot, a GHL form or funnel, an ad
// lead, a missed call, a manual entry, a bulk import - lived in GHL and nowhere
// else. Point every GHL workflow here and let the routing happen server-side,
// so a new lead source later means a new workflow, not more code.
//
// Business vs individual is decided by TAG, in this order:
//   1. An explicit `pipeline` field on the payload ("business"/"individual").
//   2. Any tag on the contact in the business-tag list in api/_lib.js
//      (extendable through the GHL_BUSINESS_TAGS env var).
//   3. Otherwise the individual / family pipeline.
//
// Tags come from the payload when GHL sends them, but the contact is re-read
// from the GHL API whenever a contact id is present, because a workflow firing
// on "Contact Created" often runs before the tag is applied and the payload's
// tag list is then a lie. The API read is the source of truth.
//
// Duplicates: a contact already on a board is not added twice. It is matched on
// GHL contact id, then email, then phone, and the existing card stays where it
// is - blank fields get filled in and a dated line is added to its notes. The
// exception is a card in a closed stage (sold, lost, disqualified, ghosted),
// which means the old card is finished business and this is a new enquiry.
//
// Safe by design: always returns 200 so a form never breaks and GHL never
// retry-loops, and skips quietly when there is nothing usable to write.
//
// ENV VARS:
//   GHL_PIT_TOKEN        required for CRM writes and the contact re-read;
//                        without it those steps no-op.
//   GHL_LOCATION_ID      optional, defaults to the VS Health Benefits sub-account
//   GHL_INBOUND_SECRET   shared secret for ?to=portal, sent as the
//                        `x-vs-webhook-secret` header or `?key=`. Falls back to
//                        WEBCHAT_WEBHOOK_SECRET. If neither is set the check is
//                        skipped, so you can test before locking it down.
//   GHL_BUSINESS_TAGS    optional, comma separated, added to the business tags
//                        listed in api/_lib.js.
//   RESEND_API_KEY / NOTIFY_EMAIL   see api/_lib.js (alert email)

const L = require("./_lib");
const FS = require("./_fs");

const LOCATION_ID = process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU";

// Stages that mean the old card is finished business, so a new enquiry from the
// same person deserves a new card rather than a merge.
const CLOSED_INDIVIDUAL = ["sold", "no_longer_interested", "disqualified", "ghosted"];
const CLOSED_BUSINESS = ["won", "lost"];

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

// E.164 for the CRM half, which is what GHL wants on a contact.
function validPhoneE164(v) {
  const d = tenDigits(v);
  return d ? "+1" + d : "";
}

// Bare 10 digits for the portal half, which is what the boards store.
function tenDigits(v) {
  let d = clean(v, 25).replace(/\D/g, "");
  if (d.length === 11 && d.charAt(0) === "1") d = d.slice(1);
  if (d.length !== 10) return "";
  if (/^(\d)\1{9}$/.test(d)) return "";
  if (d.slice(0, 3) === "555" || d.slice(3, 6) === "555") return "";
  return d;
}

function lastTen(v) { return String(v == null ? "" : v).replace(/\D/g, "").slice(-10); }

// Tags must be safe to create in bulk: lowercase, hyphenated, no surprises.
function normTag(v) {
  return clean(v, 40).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function todayStr() { return new Date().toISOString().slice(0, 10); }

// ══════════════════════════════════════════════════════════════════════════
// to-crm : website / portal  ->  GoHighLevel
// ══════════════════════════════════════════════════════════════════════════
async function toCrm(d, res) {
  const p = {
    firstName: clean(d.firstName || d.first_name || d.firstname, 60),
    lastName:  clean(d.lastName  || d.last_name  || d.lastname,  60),
    email:     validEmail(d.email),
    phone:     validPhoneE164(d.phone),
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

  const out = { ok: true, direction: "to-crm" };

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
    const up = await L.ghl("/contacts/upsert", "POST", body);
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
      const t = await L.ghl("/contacts/" + contactId + "/tags", "POST", { tags: tags });
      out.tagged = Boolean(t.ok);
      out.tags = tags;
    } catch (e) { out.tagged = false; }

    if (p.notes) {
      try { await L.ghl("/contacts/" + contactId + "/notes", "POST", { body: p.notes }); out.noted = true; }
      catch (e) { out.noted = false; }
    }
  }

  res.status(200).json(out);
}

// ══════════════════════════════════════════════════════════════════════════
// to-portal : GoHighLevel  ->  admin portal boards
// ══════════════════════════════════════════════════════════════════════════
async function ghlGetContact(contactId) {
  if (!contactId) return null;
  try {
    const r = await L.ghl("/contacts/" + encodeURIComponent(contactId), "GET");
    if (!r.ok) return null;
    return (r.json && (r.json.contact || r.json.data || r.json)) || null;
  } catch (e) {
    return null;
  }
}

async function toPortal(d, req, res) {
  // ---- shared secret ----
  const expected = process.env.GHL_INBOUND_SECRET || process.env.WEBCHAT_WEBHOOK_SECRET;
  if (expected) {
    const got = String(
      (req.headers && req.headers["x-vs-webhook-secret"]) ||
      (req.query && req.query.key) || ""
    );
    if (got !== expected) { res.status(401).json({ error: "Unauthorized" }); return; }
  }

  // GHL's field names depend on how the workflow was mapped, and the
  // custom-values style ({{contact.first_name}}) differs again from the native
  // webhook shape, so every common alias is accepted.
  const contactId = clean(d.contactId || d.contact_id || d.id || d.ghl_contact_id, 60);

  // The contact record from GHL wins wherever both have a value, because the
  // payload can be a snapshot from before the workflow's earlier steps ran.
  const c = (await ghlGetContact(contactId)) || {};

  const tags = L.normTags(
    (c.tags && c.tags.length ? c.tags : null) || d.tags || d.tag || d.contact_tags
  );

  let firstName = clean(c.firstName || d.firstName || d.first_name || d.firstname, 60);
  let lastName = clean(c.lastName || d.lastName || d.last_name || d.lastname, 60);
  if (!firstName && !lastName) {
    const full = clean(c.contactName || d.full_name || d.fullName || d.name, 120);
    if (full) {
      const parts = full.split(/\s+/);
      firstName = parts[0] || "";
      lastName = parts.slice(1).join(" ");
    }
  }

  const email = validEmail(c.email || d.email || d.contactEmail);
  const phone = tenDigits(c.phone || d.phone || d.phoneNumber || d.contactPhone);
  const company = clean(c.companyName || d.company || d.businessName || d.company_name, 120);
  const state = clean(c.state || d.state, 40);
  const zip = clean(c.postalCode || d.zip || d.postalCode || d.zipCode, 12);
  const employees = clean(d.employees || d.employeeCount || d.numEmployees || d.num_employees, 20);
  const source = clean(c.source || d.source || d.leadSource, 80) || "GoHighLevel";
  const notesIn = clean(d.notes || d.message || d.summary || d.transcript, 3000);

  if (!email && !phone) {
    res.status(200).json({ ok: true, skipped: "no_email_or_phone" });
    return;
  }

  const business = L.isBusinessLead(d.pipeline || d.leadType || d.coverageType || d.type, tags);
  const now = Date.now();
  const today = todayStr();
  const fullName = (firstName + " " + lastName).trim() || company || email || phone;

  // A dry run classifies and reports back without writing anything - it is how
  // the routing gets verified against a real payload without littering the
  // boards with test cards.
  const dryRun = String((req.query && req.query.dryRun) || d.dryRun || "") === "1" ||
                 (req.query && req.query.dryRun) === "true" || d.dryRun === true;
  if (dryRun) {
    res.status(200).json({
      ok: true, dryRun: true, direction: "to-portal",
      pipeline: business ? "business" : "individual",
      tags: tags, contactId: contactId || null,
      parsed: { firstName, lastName, email, phone, company, state, zip, employees, source },
    });
    return;
  }

  const noteLines = [];
  if (source) noteLines.push("Source: " + source);
  if (tags.length) noteLines.push("GHL tags: " + tags.join(", "));
  if (contactId) noteLines.push("GHL contact: " + contactId);
  if (notesIn) noteLines.push(notesIn);
  const notes = noteLines.join("\n");

  function sameContact(x) {
    if (contactId && x.ghlContactId && x.ghlContactId === contactId) return true;
    if (email && String(x.email || "").toLowerCase() === email) return true;
    if (phone && lastTen(x.phone) && lastTen(x.phone) === phone) return true;
    return false;
  }

  let result;

  if (business) {
    // ---- Business Leads board, Prospect column ----
    const rec = {
      id: "ghl_" + now.toString(36) + Math.random().toString(36).slice(2, 8),
      company: company || fullName,
      contact: (firstName + " " + lastName).trim(),
      niche: clean(d.niche || d.industry, 60),
      employees: employees,
      requestedCoverage: clean(d.requestedCoverage || d.coverage, 80),
      currentlyInsured: clean(d.currentlyInsured, 40),
      coverageStart: clean(d.coverageStart, 40),
      stage: "prospect",
      email: email,
      phone: phone,
      source: source,
      nextFollowUp: today,
      notes: notes,
      ghlContactId: contactId,
      created: now,
      updated: now,
    };

    result = await FS.appendRecord(
      "biz_leads",
      rec,
      function (x) {
        if (CLOSED_BUSINESS.indexOf(x.stage) >= 0) return false;
        return sameContact(x);
      },
      function (existing) {
        if (!existing.ghlContactId && contactId) existing.ghlContactId = contactId;
        if (!existing.email && email) existing.email = email;
        if (!existing.phone && phone) existing.phone = phone;
        if (!existing.employees && employees) existing.employees = employees;
        existing.notes = (existing.notes ? existing.notes + "\n" : "") +
          "[" + today + "] New inbound from GoHighLevel (" + source + ")";
        existing.updated = now;
        return true;
      }
    );
  } else {
    // ---- Individual / family pipeline, New Lead column ----
    const rec = {
      id: "ghl_" + now.toString(36) + Math.random().toString(36).slice(2, 8),
      firstName: firstName,
      lastName: lastName,
      email: email,
      phone: phone,
      dob: clean(d.dob || d.dateOfBirth, 20),
      address: "",
      state: state,
      zipCode: zip,
      company: company,
      notes: notes,
      quoteValue: 0,
      status: "new",
      stage: "new_lead",
      followUpDue: today,
      lastContact: today,
      createdAt: today,
      created: now,
      updated: now,
      source: source,
      ghlContactId: contactId,
      activity: [{ ts: now, type: "created", text: "Arrived from GoHighLevel (" + source + ")" }],
    };

    result = await FS.appendRecord(
      "leads",
      rec,
      function (x) {
        if (CLOSED_INDIVIDUAL.indexOf(x.stage) >= 0) return false;
        return sameContact(x);
      },
      function (existing) {
        if (!existing.ghlContactId && contactId) existing.ghlContactId = contactId;
        if (!existing.email && email) existing.email = email;
        if (!existing.phone && phone) existing.phone = phone;
        if (!existing.zipCode && zip) existing.zipCode = zip;
        if (!existing.state && state) existing.state = state;
        existing.lastContact = today;
        existing.updated = now;
        existing.activity = (existing.activity || []).concat([
          { ts: now, type: "note", text: "New inbound from GoHighLevel (" + source + ")" },
        ]);
        return true;
      }
    );
  }

  // ---- alert email, best effort ----
  try {
    if (result && result.ok && result.action === "created") {
      const rows = [
        ["Name", fullName],
        ["Phone", phone || "—"],
        ["Email", email || "—"],
        ["Company", company || "—"],
        ["Employees", employees || "—"],
        ["Tags", tags.join(", ") || "—"],
        ["Source", source],
      ];
      const table =
        '<table style="border-collapse:collapse;font:15px/1.5 system-ui,sans-serif">' +
        rows.map(function (r) {
          return '<tr><td style="padding:4px 14px 4px 0;color:#5a6b80">' + L.esc(r[0]) +
                 '</td><td style="padding:4px 0"><b>' + L.esc(r[1]) + "</b></td></tr>";
        }).join("") + "</table>";
      await L.sendEmail({
        to: L.CFG.notify,
        subject: (business ? "🏢 New business lead: " : "New lead: ") + fullName,
        html: L.shell(
          '<h2 style="margin:0 0 12px;color:' + L.CFG.navy + '">' +
          (business ? "New business lead" : "New lead") + " from GoHighLevel</h2>" + table +
          '<p style="margin-top:16px;color:#5a6b80;font-size:13px">Added to your ' +
          (business ? "Business Leads board (Prospect)" : "Pipeline (New Lead)") + ".</p>" +
          L.btn("https://www.vshealthbenefits.com/admin", "Open admin portal"),
          (business ? "New business lead" : "New lead") + ": " + fullName
        ),
        replyTo: email || undefined,
      });
    }
  } catch (e) { /* non-fatal */ }

  res.status(200).json({
    ok: true,
    direction: "to-portal",
    pipeline: business ? "business" : "individual",
    action: (result && result.action) || "failed",
    portal: result || null,
    tags: tags,
    contactId: contactId || null,
  });
}

// ══════════════════════════════════════════════════════════════════════════
module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, x-vs-webhook-secret");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  // Default stays to-crm so every existing caller keeps working untouched.
  const to = String((req.query && req.query.to) || d.to || d.direction || "").toLowerCase();
  const inbound = to === "portal" || to === "to-portal" || to === "pipeline";

  try {
    if (inbound) await toPortal(d, req, res);
    else await toCrm(d, res);
  } catch (e) {
    // Never let a lead form see a 500.
    if (!res.headersSent) res.status(200).json({ ok: true, error: "exception" });
  }
};

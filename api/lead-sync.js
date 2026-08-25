// Vercel serverless function: the lead bridge between the website, the admin
// portal and GoHighLevel. It runs in two directions.
//
//   to-crm     (default)  portal / website form  ->  GoHighLevel contact
//                                                 AND the portal board
//   to-portal            GoHighLevel workflow    ->  admin portal pipeline
//   to-portal + sweep    poll GHL for anything the webhook missed
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
// ── sweep ──────────────────────────────────────────────────────────────────
//   POST /api/lead-sync?to=portal&sweep=1
//
// The backstop. Walks the most recently added GHL contacts and puts any that
// are missing onto the right board, so a paused workflow or an unwired lead
// source cannot silently swallow leads. Same dedupe rules, so running it often
// is harmless. See sweepPortal() for the window and limit.
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

  // ---- and straight onto the portal board ----
  // A website form used to create the GHL contact and stop there, leaving the
  // portal to find out later through the webhook or the sweep. That made the
  // pipeline depend on a GHL workflow existing and staying published, for a
  // lead this function is already holding in its hand. So write both.
  //
  // Skipped when the admin portal is the caller, because that lead is already
  // on the board - it is what triggered this call. Without the guard, saving a
  // lead in the portal would bounce straight back into it.
  const fromAdmin = /^admin portal/i.test(p.source);
  if (!fromAdmin) {
    try {
      const n = normalize(
        { id: contactId, email: p.email, phone: p.phone, companyName: p.company,
          firstName: p.firstName, lastName: p.lastName, state: p.state, postalCode: p.zip },
        Object.assign({}, d, { source: p.source, notes: p.notes })
      );
      const board = await syncToBoards(n);
      out.board = board && board.ok ? (board.action || "ok") : ((board && board.reason) || "error");
      out.pipeline = n.business ? "business" : "individual";
    } catch (e) { out.board = "exception"; }
  } else {
    out.board = "skipped_admin_origin";
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

// Normalise a contact into the shape the boards are built from. It arrives
// three ways - a webhook payload, an API read of that contact, or a row from
// the sweep's contact list - and they disagree about field names, so this is
// the one place that reconciles them. The API record wins wherever both have a
// value, because a webhook payload can be a snapshot from before the
// workflow's earlier steps ran.
function normalize(c, d) {
  c = c || {}; d = d || {};

  const contactId = clean(c.id || d.contactId || d.contact_id || d.id || d.ghl_contact_id, 60);
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

  return {
    contactId: contactId,
    tags: tags,
    firstName: firstName,
    lastName: lastName,
    email: email,
    phone: phone,
    company: company,
    state: clean(c.state || d.state, 40),
    zip: clean(c.postalCode || d.zip || d.postalCode || d.zipCode, 12),
    employees: clean(d.employees || d.employeeCount || d.numEmployees || d.num_employees, 20),
    source: clean(c.source || d.source || d.leadSource, 80) || "GoHighLevel",
    notesIn: clean(d.notes || d.message || d.summary || d.transcript, 3000),
    dob: clean(d.dob || d.dateOfBirth, 20),
    niche: clean(d.niche || d.industry, 60),
    requestedCoverage: clean(d.requestedCoverage || d.coverage, 80),
    currentlyInsured: clean(d.currentlyInsured, 40),
    coverageStart: clean(d.coverageStart, 40),
    business: L.isBusinessLead(d.pipeline || d.leadType || d.coverageType || d.type, tags),
    fullName: (firstName + " " + lastName).trim() || company || email || phone,
  };
}

// Put one normalised contact on the right board. Returns the appendRecord
// result: { ok, action: "created"|"merged"|"unchanged", total, id }.
//
// opts.reopenClosed decides what a match in a closed stage means. For a webhook
// or a form submission it is true: the person just raised their hand again, so
// an old Sold or Lost card is finished business and this deserves a fresh one.
// For the sweep it is false - the sweep is backfill, walking contacts that may
// be months old, and treating a closed card as "no match" there would resurrect
// settled clients into New Lead every time it ran.
async function syncToBoards(n, opts) {
  const reopenClosed = !opts || opts.reopenClosed !== false;
  const now = Date.now();
  const today = todayStr();

  const noteLines = [];
  if (n.source) noteLines.push("Source: " + n.source);
  if (n.tags.length) noteLines.push("GHL tags: " + n.tags.join(", "));
  if (n.contactId) noteLines.push("GHL contact: " + n.contactId);
  if (n.notesIn) noteLines.push(n.notesIn);
  const notes = noteLines.join("\n");

  function sameContact(x) {
    if (n.contactId && x.ghlContactId && x.ghlContactId === n.contactId) return true;
    if (n.email && String(x.email || "").toLowerCase() === n.email) return true;
    if (n.phone && lastTen(x.phone) && lastTen(x.phone) === n.phone) return true;
    return false;
  }

  if (n.business) {
    // ---- Business Leads board, Prospect column ----
    return FS.appendRecord(
      "biz_leads",
      {
        id: "ghl_" + now.toString(36) + Math.random().toString(36).slice(2, 8),
        company: n.company || n.fullName,
        contact: (n.firstName + " " + n.lastName).trim(),
        niche: n.niche,
        employees: n.employees,
        requestedCoverage: n.requestedCoverage,
        currentlyInsured: n.currentlyInsured,
        coverageStart: n.coverageStart,
        stage: "prospect",
        email: n.email,
        phone: n.phone,
        source: n.source,
        nextFollowUp: today,
        notes: notes,
        ghlContactId: n.contactId,
        created: now,
        updated: now,
      },
      function (x) {
        if (reopenClosed && CLOSED_BUSINESS.indexOf(x.stage) >= 0) return false;
        return sameContact(x);
      },
      function (existing) {
        if (!existing.ghlContactId && n.contactId) existing.ghlContactId = n.contactId;
        if (!existing.email && n.email) existing.email = n.email;
        if (!existing.phone && n.phone) existing.phone = n.phone;
        if (!existing.employees && n.employees) existing.employees = n.employees;
        existing.notes = (existing.notes ? existing.notes + "\n" : "") +
          "[" + today + "] New inbound from GoHighLevel (" + n.source + ")";
        existing.updated = now;
        return true;
      }
    );
  }

  // ---- Individual / family pipeline, New Lead column ----
  return FS.appendRecord(
    "leads",
    {
      id: "ghl_" + now.toString(36) + Math.random().toString(36).slice(2, 8),
      firstName: n.firstName,
      lastName: n.lastName,
      email: n.email,
      phone: n.phone,
      dob: n.dob,
      address: "",
      state: n.state,
      zipCode: n.zip,
      company: n.company,
      notes: notes,
      quoteValue: 0,
      status: "new",
      stage: "new_lead",
      followUpDue: today,
      lastContact: today,
      createdAt: today,
      created: now,
      updated: now,
      source: n.source,
      ghlContactId: n.contactId,
      activity: [{ ts: now, type: "created", text: "Arrived from GoHighLevel (" + n.source + ")" }],
    },
    function (x) {
      if (reopenClosed && CLOSED_INDIVIDUAL.indexOf(x.stage) >= 0) return false;
      return sameContact(x);
    },
    function (existing) {
      if (!existing.ghlContactId && n.contactId) existing.ghlContactId = n.contactId;
      if (!existing.email && n.email) existing.email = n.email;
      if (!existing.phone && n.phone) existing.phone = n.phone;
      if (!existing.zipCode && n.zip) existing.zipCode = n.zip;
      if (!existing.state && n.state) existing.state = n.state;
      existing.lastContact = today;
      existing.updated = now;
      existing.activity = (existing.activity || []).concat([
        { ts: now, type: "note", text: "New inbound from GoHighLevel (" + n.source + ")" },
      ]);
      return true;
    }
  );
}

function secretOk(req) {
  const expected = process.env.GHL_INBOUND_SECRET || process.env.WEBCHAT_WEBHOOK_SECRET;
  if (!expected) return true; // not configured yet - allow, so you can test first
  const got = String(
    (req.headers && req.headers["x-vs-webhook-secret"]) ||
    (req.query && req.query.key) || ""
  );
  return got === expected;
}

async function toPortal(d, req, res) {
  if (!secretOk(req)) { res.status(401).json({ error: "Unauthorized" }); return; }

  const contactId = clean(d.contactId || d.contact_id || d.id || d.ghl_contact_id, 60);
  const n = normalize(await ghlGetContact(contactId), d);

  if (!n.email && !n.phone) {
    res.status(200).json({ ok: true, skipped: "no_email_or_phone" });
    return;
  }

  // A dry run classifies and reports back without writing anything - it is how
  // the routing gets verified against a real payload without littering the
  // boards with test cards.
  const dryRun = String((req.query && req.query.dryRun) || d.dryRun || "") === "1" ||
                 (req.query && req.query.dryRun) === "true" || d.dryRun === true;
  if (dryRun) {
    res.status(200).json({
      ok: true, dryRun: true, direction: "to-portal",
      pipeline: n.business ? "business" : "individual",
      tags: n.tags, contactId: n.contactId || null,
      parsed: {
        firstName: n.firstName, lastName: n.lastName, email: n.email, phone: n.phone,
        company: n.company, state: n.state, zip: n.zip, employees: n.employees, source: n.source,
      },
    });
    return;
  }

  const result = await syncToBoards(n);

  if (result && result.ok && result.action === "created") {
    try { await alertNewLead(n); } catch (e) { /* non-fatal */ }
  }

  res.status(200).json({
    ok: true,
    direction: "to-portal",
    pipeline: n.business ? "business" : "individual",
    action: (result && result.action) || "failed",
    portal: result || null,
    tags: n.tags,
    contactId: n.contactId || null,
  });
}

// ══════════════════════════════════════════════════════════════════════════
// sweep : catch anything the webhook missed
// ══════════════════════════════════════════════════════════════════════════
// POST /api/lead-sync?to=portal&sweep=1
//
// Walks the most recently added GoHighLevel contacts newest-first and puts any
// that are missing onto the right board. It is the backstop for the webhook:
// if a workflow is paused, a webhook step errors, or a lead is created by a
// route nobody wired up, the sweep still finds it.
//
// Safe to run as often as you like - syncToBoards matches on contact id, email
// and phone, so a contact already on a board is merged, never duplicated. The
// window is deliberately short (24h by default) so it never turns into a bulk
// import of the whole CRM history.
//
//   hours   how far back to look. Default 24, max 168 (a week).
//   limit   most contacts to touch in one run. Default 25, max 100.
//
// No per-lead alert emails here - a sweep that finds ten leads should not send
// ten emails. The portal raises its own in-app notification for each new card.
async function sweepPortal(d, req, res) {
  if (!secretOk(req)) { res.status(401).json({ error: "Unauthorized" }); return; }

  const hours = Math.min(Math.max(parseInt(d.hours || (req.query && req.query.hours) || 24, 10) || 24, 1), 168);
  const limit = Math.min(Math.max(parseInt(d.limit || (req.query && req.query.limit) || 25, 10) || 25, 1), 100);
  const cutoff = Date.now() - hours * 3600 * 1000;

  const out = {
    ok: true, direction: "to-portal", mode: "sweep",
    hours: hours, limit: limit,
    scanned: 0, created: 0, merged: 0, skipped: 0, failed: 0,
    createdLeads: [],
  };

  // The contacts list comes back newest-first, so we can stop at the first one
  // older than the window instead of paging through the whole CRM.
  let path = "/contacts/?locationId=" + encodeURIComponent(LOCATION_ID) + "&limit=" + Math.min(limit, 100);
  let guard = 0;

  while (path && guard < 5 && out.scanned < limit) {
    guard++;
    const r = await L.ghl(path, "GET");
    if (!r.ok) { out.ok = false; out.error = "ghl_" + (r.status || r.skipped); break; }
    const contacts = (r.json && r.json.contacts) || [];
    if (!contacts.length) break;

    let hitCutoff = false;
    for (const c of contacts) {
      if (out.scanned >= limit) break;
      const added = Date.parse(c.dateAdded || "") || 0;
      if (added && added < cutoff) { hitCutoff = true; break; }
      out.scanned++;

      const n = normalize(c, {});
      if (!n.email && !n.phone) { out.skipped++; continue; }

      try {
        const result = await syncToBoards(n, { reopenClosed: false });
        if (!result || !result.ok) { out.failed++; continue; }
        if (result.action === "created") {
          out.created++;
          out.createdLeads.push({
            name: n.fullName,
            pipeline: n.business ? "business" : "individual",
            contactId: n.contactId,
          });
        } else { out.merged++; }
      } catch (e) { out.failed++; }
    }

    if (hitCutoff) break;
    const meta = (r.json && r.json.meta) || {};
    path = meta.startAfter && meta.startAfterId
      ? "/contacts/?locationId=" + encodeURIComponent(LOCATION_ID) + "&limit=" + Math.min(limit, 100) +
        "&startAfter=" + meta.startAfter + "&startAfterId=" + encodeURIComponent(meta.startAfterId)
      : null;
  }

  res.status(200).json(out);
}

// Internal alert for a single new lead.
async function alertNewLead(n) {
  const rows = [
    ["Name", n.fullName],
    ["Phone", n.phone || "—"],
    ["Email", n.email || "—"],
    ["Company", n.company || "—"],
    ["Employees", n.employees || "—"],
    ["Tags", n.tags.join(", ") || "—"],
    ["Source", n.source],
  ];
  const table =
    '<table style="border-collapse:collapse;font:15px/1.5 system-ui,sans-serif">' +
    rows.map(function (r) {
      return '<tr><td style="padding:4px 14px 4px 0;color:#5a6b80">' + L.esc(r[0]) +
             '</td><td style="padding:4px 0"><b>' + L.esc(r[1]) + "</b></td></tr>";
    }).join("") + "</table>";
  return L.sendEmail({
    to: L.CFG.notify,
    subject: (n.business ? "🏢 New business lead: " : "New lead: ") + n.fullName,
    html: L.shell(
      '<h2 style="margin:0 0 12px;color:' + L.CFG.navy + '">' +
      (n.business ? "New business lead" : "New lead") + " from GoHighLevel</h2>" + table +
      '<p style="margin-top:16px;color:#5a6b80;font-size:13px">Added to your ' +
      (n.business ? "Business Leads board (Prospect)" : "Pipeline (New Lead)") + ".</p>" +
      L.btn("https://www.vshealthbenefits.com/admin", "Open admin portal"),
      (n.business ? "New business lead" : "New lead") + ": " + n.fullName
    ),
    replyTo: n.email || undefined,
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

  const isSweep = String((req.query && req.query.sweep) || d.sweep || "") === "1" ||
                  (req.query && req.query.sweep) === "true" || d.sweep === true;

  try {
    if (inbound && isSweep) await sweepPortal(d, req, res);
    else if (inbound) await toPortal(d, req, res);
    else await toCrm(d, res);
  } catch (e) {
    // Never let a lead form see a 500.
    if (!res.headersSent) res.status(200).json({ ok: true, error: "exception" });
  }
};

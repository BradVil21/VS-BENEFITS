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

const FS = require("./_fs");

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
  const company   = clean(d.company || d.businessName || d.company_name, 120);
  const employees = clean(d.employees || d.employeeCount || d.num_employees, 20);
  // A visitor who tells the chat bot they are covering employees belongs on the
  // Business Leads board, not in the individual pipeline. The bot flags that
  // either by tagging the contact or by sending an explicit `pipeline` field.
  const tags      = L.normTags(d.tags || d.tag || d.contact_tags);
  const business  = L.isBusinessLead(d.pipeline || d.leadType || d.coverageType || d.type, tags);

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
    company: company,
    notes: noteLines.join("\n"),
    quoteValue: 0,
    status: "new",
    // Must be one of the column ids in admin.html's czSTAGES. It used to be
    // "new" here, which matches no column, so chat leads were written to the
    // portal and then rendered nowhere on the board.
    stage: "new_lead",
    followUpDue: today,
    lastContact: today,
    createdAt: today,
    created: Date.now(),
    updated: Date.now(),
    source: "webchat",
    painPoint: pain,
    yearlyIncome: income,
    ghlContactId: ghlId,
    activity: [{ ts: Date.now(), type: "created", text: "Captured from website live chat" }],
  };

  // The Business Leads board stores a different record shape than the
  // individual pipeline, so a business chat lead is rebuilt rather than
  // squeezed into a lead card.
  const bizLead = {
    id: "wc_" + Date.now().toString(36) + Math.random().toString(36).slice(2, 8),
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
    source: "Website live chat",
    nextFollowUp: today,
    notes: noteLines.join("\n"),
    ghlContactId: ghlId,
    created: Date.now(),
    updated: Date.now(),
  };

  function sameLead(x) {
    if (ghlId && x.ghlContactId && x.ghlContactId === ghlId) return true;
    if (email && String(x.email || "").toLowerCase() === email) return true;
    if (phone && String(x.phone || "").replace(/\D/g, "").slice(-10) === phone) return true;
    return false;
  }

  function touch(existing) {
    existing.notes = (existing.notes ? existing.notes + "\n" : "") +
      "[" + today + "] Came back through the website live chat";
    if (!existing.ghlContactId && ghlId) existing.ghlContactId = ghlId;
    existing.updated = Date.now();
    return true;
  }

  // ---- 1. VS admin portal (Firestore) ----
  // Appending through the shared helper means a chat lead that is already on
  // the board (they came back, or the GHL webhook beat us to it) updates the
  // existing card instead of creating a second one.
  let portal = { ok: false, reason: "not_attempted" };
  try {
    portal = business
      ? await FS.appendRecord("biz_leads", bizLead, function (x) {
          return x.stage !== "won" && x.stage !== "lost" && sameLead(x);
        }, touch)
      : await FS.appendRecord("leads", lead, function (x) {
          return ["sold", "no_longer_interested", "disqualified", "ghosted"].indexOf(x.stage) < 0 && sameLead(x);
        }, touch);
  } catch (e) { portal = { ok: false, reason: "exception" }; }

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

  res.status(200).json({
    ok: true,
    pipeline: business ? "business" : "individual",
    portal: portal,
    leadId: business ? bizLead.id : lead.id,
  });
};

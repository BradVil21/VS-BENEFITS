// Vercel serverless function: the phone AI qualified a caller — create the lead.
//
// Called by the GHL Voice AI agent ("Amanda") at the end of a call with someone
// who is NOT already a member. Writes the lead into:
//   1. The admin portal (Firestore) -> vs_state/leads for an individual or
//      family caller, landing in the Pipeline's "New Lead" column, or
//      vs_state/biz_leads for an employer caller, landing on the Business Leads
//      board in "Prospect".
//   2. GoHighLevel                  -> contact + tag `phone-lead`, so it lives in the CRM
//
// Family members and business census rows arrive as arrays and get folded into
// the lead's notes, because the admin pipeline stores one row per lead.
//
// Safe by design: every destination is wrapped, one failure never blocks the
// others, and the function always returns 200 so a live call never hears an error.
//
// ENV VARS:
//   VOICE_AGENT_SECRET   REQUIRED. Same secret as api/voice-lookup.js, sent in
//                        the `x-vs-voice-secret` header.
//   GHL_PIT_TOKEN        optional; without it the CRM half is skipped and the
//                        lead still reaches the admin pipeline.
//   GHL_LOCATION_ID      optional
//   FIREBASE_API_KEY / FIREBASE_PROJECT_ID   optional

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";
const LOCATION_ID = process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU";

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

function validPhone(v) {
  let d = clean(v, 25).replace(/\D/g, "");
  if (d.length === 11 && d.charAt(0) === "1") d = d.slice(1);
  if (d.length !== 10) return "";
  if (/^(\d)\1{9}$/.test(d)) return "";
  if (d.slice(0, 3) === "555" || d.slice(3, 6) === "555") return "";
  return "+1" + d;
}

function normDob(v) {
  const s = clean(v, 32);
  if (!s) return "";
  let m;
  m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (m) return iso(m[1], m[2], m[3]);
  m = /^(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{4})$/.exec(s);
  if (m) return iso(m[3], m[1], m[2]);
  const digits = s.replace(/\D/g, "");
  if (digits.length === 8) {
    const head = Number(digits.slice(0, 4));
    if (head >= 1900 && head <= 2100) return iso(digits.slice(0, 4), digits.slice(4, 6), digits.slice(6, 8));
    return iso(digits.slice(4, 8), digits.slice(0, 2), digits.slice(2, 4));
  }
  return "";
}

function iso(y, mo, d) {
  const Y = Number(y), M = Number(mo), D = Number(d);
  if (!(Y >= 1900 && Y <= 2100)) return "";
  if (!(M >= 1 && M <= 12)) return "";
  if (!(D >= 1 && D <= 31)) return "";
  return String(Y) + "-" + String(M).padStart(2, "0") + "-" + String(D).padStart(2, "0");
}

// "$52,000 a year" -> "52000". Callers say it every possible way.
function normIncome(v) {
  const digits = clean(v, 20).replace(/[^\d]/g, "");
  if (!digits) return "";
  const n = Number(digits);
  if (!isFinite(n) || n <= 0 || n > 100000000) return "";
  return String(n);
}

function normZip(v) {
  const d = clean(v, 10).replace(/\D/g, "").slice(0, 5);
  return d.length === 5 ? d : "";
}

// Free text the agent captured, kept but bounded.
function normPain(v) {
  const s = clean(v, 60).toLowerCase();
  if (/lost|lay|laid|termina|fired|quit|cobra/.test(s)) return "lost coverage";
  if (/never|no coverage|nothing|uninsured|havent|haven't/.test(s)) return "never had coverage";
  if (/expensive|too much|cost|afford|high|paying/.test(s)) return "paying too much";
  return clean(v, 60);
}

// ---------- GHL ----------
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
    try { json = await r.json(); } catch (e) {}
    return { ok: r.ok, status: r.status, json };
  } catch (e) {
    return { ok: false, status: 0, json: null, error: String((e && e.message) || e) };
  }
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  const expected = process.env.VOICE_AGENT_SECRET;
  if (!expected) { res.status(503).json({ error: "Disabled: VOICE_AGENT_SECRET is not configured." }); return; }
  const got = String((req.headers && req.headers["x-vs-voice-secret"]) || "");
  if (got !== expected) { res.status(401).json({ error: "Unauthorized" }); return; }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  const p = {
    firstName: clean(d.firstName || d.first_name, 60),
    lastName:  clean(d.lastName  || d.last_name,  60),
    email:     validEmail(d.email),
    phone:     validPhone(d.phone),
    dob:       normDob(d.dob),
    zip:       normZip(d.zip || d.zipCode || d.zip_code),
    state:     clean(d.state, 4).toUpperCase(),
    income:    normIncome(d.income || d.yearlyIncome),
    pain:      normPain(d.painPoint || d.pain_point || d.reason),
    coverageType: clean(d.coverageType || d.coverage_type, 30).toLowerCase(), // individual | family | business
    company:   clean(d.company || d.businessName || d.business_name, 120),
    employeeCount: clean(d.employeeCount || d.employee_count, 8),
    familyCount:   clean(d.familyCount || d.family_count, 8),
    bestContact:   clean(d.bestContact || d.best_contact, 120),
    notes:     clean(d.notes, 1500),
    callSummary: clean(d.callSummary || d.call_summary, 1500),
  };

  if (!p.phone && !p.email) {
    res.status(200).json({ ok: true, skipped: "no_phone_or_email" });
    return;
  }

  // ---- fold the household / census into readable notes ----
  const lines = [];
  if (p.pain) lines.push("Reason for looking: " + p.pain);
  if (p.coverageType) lines.push("Coverage type: " + p.coverageType);
  if (p.company) lines.push("Business: " + p.company);
  if (p.income) lines.push("Household income: $" + p.income);
  if (p.bestContact) lines.push("Best way to reach: " + p.bestContact);

  const family = Array.isArray(d.familyMembers || d.family_members) ? (d.familyMembers || d.family_members) : [];
  if (family.length) {
    lines.push("", "Family members (" + family.length + "):");
    family.slice(0, 20).forEach(function (m, i) {
      if (!m) return;
      const bits = [
        clean(m.firstName || m.first_name || m.name, 60),
        normDob(m.dob) ? "DOB " + normDob(m.dob) : "",
        clean(m.relationship, 30),
        clean(m.gender, 20),
      ].filter(Boolean);
      lines.push("  " + (i + 1) + ". " + (bits.join(" | ") || "(no detail captured)"));
    });
  } else if (p.familyCount) {
    lines.push("Family size: " + p.familyCount + " (individual details not captured)");
  }

  const census = Array.isArray(d.employees || d.census) ? (d.employees || d.census) : [];
  if (census.length) {
    lines.push("", "Employee census (" + census.length + " of " + (p.employeeCount || census.length) + "):");
    census.slice(0, 100).forEach(function (e, i) {
      if (!e) return;
      const bits = [
        clean(e.age, 4) ? "age " + clean(e.age, 4) : "",
        clean(e.gender, 20),
        normZip(e.zip || e.zipCode) ? "ZIP " + normZip(e.zip || e.zipCode) : "",
      ].filter(Boolean);
      lines.push("  " + (i + 1) + ". " + (bits.join(" | ") || "(no detail captured)"));
    });
  } else if (p.employeeCount) {
    lines.push("Employees: " + p.employeeCount + " (census not captured on the call)");
  }

  if (p.notes) lines.push("", "Notes: " + p.notes);
  if (p.callSummary) lines.push("", "Call summary: " + p.callSummary);
  lines.push("", "Captured by the phone AI agent.");

  const today = new Date().toISOString().slice(0, 10);
  const now = Date.now();
  const lead = {
    id: "ph_" + now.toString(36) + Math.random().toString(36).slice(2, 8),
    firstName: p.firstName,
    lastName: p.lastName,
    email: p.email,
    phone: p.phone,
    dob: p.dob,
    address: "",
    state: p.state,
    zipCode: p.zip,
    notes: lines.join("\n"),
    quoteValue: 0,
    status: "new",
    // Must match a column id in admin.html's czSTAGES. It used to be "new",
    // which matches no column, so phone leads landed in the portal's data but
    // never appeared on the pipeline board.
    stage: "new_lead",
    followUpDue: today,
    lastContact: today,
    createdAt: today,
    created: now,
    source: "phone-ai",
    painPoint: p.pain,
    yearlyIncome: p.income,
    coverageType: p.coverageType,
    employeeCount: p.employeeCount,
    familyCount: p.familyCount,
    activity: [{ ts: now, type: "created", text: "Captured by the phone AI agent" }],
  };

  // An employer calling about covering their staff belongs on the Business
  // Leads board, not in the individual pipeline - the caller already told the
  // agent which one they are, so no guessing is needed here.
  const business = p.coverageType === "business";

  const bizLead = {
    id: "ph_" + now.toString(36) + Math.random().toString(36).slice(2, 8),
    company: p.company || ((p.firstName + " " + p.lastName).trim() || p.phone),
    contact: (p.firstName + " " + p.lastName).trim(),
    niche: "",
    employees: p.employeeCount || "",
    requestedCoverage: "",
    currentlyInsured: "",
    coverageStart: "",
    stage: "prospect",
    email: p.email,
    phone: p.phone,
    source: "Phone AI agent",
    nextFollowUp: today,
    notes: lines.join("\n"),
    created: now,
    updated: now,
  };

  const out = { ok: true, leadId: business ? bizLead.id : lead.id };
  out.pipelineName = business ? "business" : "individual";

  // A caller who rings twice in a row should not become two cards, and one who
  // is already being worked should update in place rather than jump the board.
  function sameCaller(x) {
    if (p.email && String(x.email || "").toLowerCase() === p.email) return true;
    if (p.phone && String(x.phone || "").replace(/\D/g, "").slice(-10) === String(p.phone).replace(/\D/g, "").slice(-10)) return true;
    return false;
  }
  function touch(existing) {
    existing.notes = (existing.notes ? existing.notes + "\n" : "") +
      "[" + today + "] Called again - handled by the phone AI agent";
    existing.updated = now;
    return true;
  }

  // ---- 1. admin pipeline ----
  try {
    const push = business
      ? await FS.appendRecord("biz_leads", bizLead, function (x) {
          return x.stage !== "won" && x.stage !== "lost" && sameCaller(x);
        }, touch)
      : await FS.appendRecord("leads", lead, function (x) {
          return ["sold", "no_longer_interested", "disqualified", "ghosted"].indexOf(x.stage) < 0 && sameCaller(x);
        }, touch);
    out.pipeline = Boolean(push.ok);
    if (push.action) out.pipelineAction = push.action;
    if (!push.ok) out.pipelineError = push.reason;
  } catch (e) { out.pipeline = false; out.pipelineError = "exception"; }

  // ---- 2. GHL contact ----
  try {
    const body = { locationId: LOCATION_ID, source: "Phone AI agent" };
    if (p.firstName) body.firstName = p.firstName;
    if (p.lastName) body.lastName = p.lastName;
    if (p.email) body.email = p.email;
    if (p.phone) body.phone = p.phone;
    if (p.state) body.state = p.state;
    if (p.zip) body.postalCode = p.zip;

    const up = await ghl("/contacts/upsert", "POST", body);
    const c = up.json && (up.json.contact || up.json.data || up.json);
    const contactId = up.ok && c && c.id ? c.id : null;
    out.contactId = contactId;

    if (contactId) {
      const tags = ["phone-lead"];
      if (p.coverageType === "business") tags.push("business-lead");
      if (p.coverageType === "family") tags.push("family-lead");
      await ghl("/contacts/" + contactId + "/tags", "POST", { tags: tags });
      await ghl("/contacts/" + contactId + "/notes", "POST", { body: lines.join("\n") });
      out.tagged = true;
    } else {
      out.contactError = up.status || up.skipped;
    }
  } catch (e) { out.contactError = "exception"; }

  res.status(200).json(out);
};

// Vercel serverless function: handle a BUSINESS (group) quote submission.
//
// On submit it:
//   1. Creates/updates the contact in GoHighLevel (owner name, phone, company, employees, location).
//   2. Puts the company on the admin portal's Business Leads board in "Prospect".
//   3. Sends the lead a branded VS Health Benefits confirmation email with a "Fill out census form" link.
//   4. Emails Bradley an internal alert.
//   5. Adds a note to the contact summarizing the request.
//
// Step 2 was missing for a long time: a group quote request created a GHL
// contact and two emails, but nothing ever reached the Business Leads pipeline,
// so the board only ever held companies typed in by hand.
//
// Safe by design: if GHL_PIT_TOKEN or RESEND_API_KEY are missing, the
// relevant step is skipped and the function still returns 200 so the website never breaks.
//
// See api/_lib.js for env vars.

const L = require("./_lib");
const FS = require("./_fs");

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  const firstName = String(d.ownerFirstName || "").trim();
  const lastName = String(d.ownerLastName || "").trim();
  const email = String(d.contactEmail || "").trim();
  const phone = String(d.contactPhone || d.businessPhone || "").trim();
  const businessName = String(d.businessName || "").trim();
  const zip = String(d.businessZip || "").trim();

  let contactId = null;
  try {
    contactId = await L.upsertContact({
      email: email,
      firstname: firstName,
      lastname: lastName,
      phone: phone,
      company: businessName,
      num_employees: d.employees,
      numemployees: d.employees,
      address: d.businessAddress,
      state: d.businessState,
      zip: zip,
      website_lead_stage: "Business Quote — Awaiting Census",
      lifecyclestage: "lead",
    });
  } catch (e) { /* non-fatal */ }

  // ---- Business Leads board (Prospect column) ----
  // The board is keyed by company, so a second request from the same company
  // updates the existing card rather than stacking duplicates in Prospect.
  const now = Date.now();
  const today = new Date().toISOString().slice(0, 10);
  let board = { ok: false, reason: "not_attempted" };
  try {
    board = await FS.appendRecord(
      "biz_leads",
      {
        id: "bq_" + now.toString(36) + Math.random().toString(36).slice(2, 8),
        company: businessName || (firstName + " " + lastName).trim() || email,
        contact: (firstName + " " + lastName).trim(),
        niche: String(d.niche || d.industry || "").trim().slice(0, 60),
        employees: String(d.employees || "").trim().slice(0, 20),
        requestedCoverage: String(d.requestedCoverage || "").trim().slice(0, 80),
        currentlyInsured: String(d.currentlyInsured || "").trim().slice(0, 40),
        coverageStart: String(d.coverageStart || "").trim().slice(0, 40),
        stage: "prospect",
        email: email,
        phone: phone,
        source: "Website business funnel",
        nextFollowUp: today,
        notes: [
          "Business quote request from the website.",
          d.businessAddress ? "Address: " + d.businessAddress : "",
          [d.businessState, zip].filter(Boolean).length ? "Location: " + [d.businessState, zip].filter(Boolean).join(" ") : "",
          Array.isArray(d.situations) && d.situations.length ? "Situations: " + d.situations.join(", ") : "",
          "Census link sent; awaiting census.",
        ].filter(Boolean).join("\n"),
        ghlContactId: contactId || "",
        created: now,
        updated: now,
      },
      function (x) {
        if (x.stage === "won" || x.stage === "lost") return false;
        if (contactId && x.ghlContactId && x.ghlContactId === contactId) return true;
        if (email && String(x.email || "").toLowerCase() === email.toLowerCase()) return true;
        if (businessName && String(x.company || "").trim().toLowerCase() === businessName.toLowerCase()) return true;
        return false;
      },
      function (existing) {
        if (!existing.ghlContactId && contactId) existing.ghlContactId = contactId;
        if (!existing.email && email) existing.email = email;
        if (!existing.phone && phone) existing.phone = phone;
        if (!existing.employees && d.employees) existing.employees = String(d.employees);
        existing.notes = (existing.notes ? existing.notes + "\n" : "") +
          "[" + today + "] Submitted the business quote form again.";
        existing.updated = now;
        return true;
      }
    );
  } catch (e) { board = { ok: false, reason: "exception" }; }

  // Build the census-form link (carries who/what so census.js can attach to the right contact).
  const q = new URLSearchParams();
  if (email) q.set("e", email);
  if (businessName) q.set("b", businessName);
  if (zip) q.set("z", zip);
  if (d.employees) q.set("n", String(d.employees));
  if (contactId) q.set("c", String(contactId));
  // cleanUrls is on in vercel.json, so link to /census (no .html) to avoid a redirect hop.
  const censusUrl = L.CFG.site + "/census?" + q.toString();

  // Note on the contact
  try {
    if (contactId) {
      const summary =
        "<b>Business quote request</b><br>" +
        [
          businessName ? "Business: " + L.esc(businessName) : "",
          "Contact: " + L.esc((firstName + " " + lastName).trim()),
          email ? "Email: " + L.esc(email) : "",
          phone ? "Phone: " + L.esc(phone) : "",
          d.employees ? "Employees: " + L.esc(d.employees) : "",
          d.requestedCoverage ? "Requested: " + L.esc(d.requestedCoverage) : "",
          d.currentlyInsured ? "Currently insured: " + L.esc(d.currentlyInsured) : "",
          d.coverageStart ? "Coverage start: " + L.esc(d.coverageStart) : "",
          "Source: website business funnel",
        ].filter(Boolean).join("<br>");
      await L.addNoteToContact(contactId, summary);
    }
  } catch (e) { /* non-fatal */ }

  // Emails (best-effort)
  let leadEmail = { skipped: "no_email" };
  let alert = { skipped: "no_notify" };
  try {
    if (email) {
      leadEmail = await L.sendEmail({
        to: email,
        subject: "Your group health quote — quick info needed",
        html: L.businessLeadEmail({ firstName, businessName, censusUrl }),
      });
    }
  } catch (e) { /* non-fatal */ }
  try {
    alert = await L.sendEmail({
      to: L.CFG.notify,
      subject: "🏢 New business quote: " + (businessName || (firstName + " " + lastName).trim() || "unknown"),
      html: L.bizAlertEmail(d),
    });
  } catch (e) { /* non-fatal */ }

  res.status(200).json({
    ok: true,
    contactId: contactId || null,
    board: board && board.ok ? (board.action || "ok") : (board && board.reason) || "error",
    censusUrl: censusUrl,
    leadEmail: leadEmail && leadEmail.ok ? "sent" : (leadEmail && leadEmail.skipped) || "error",
    alert: alert && alert.ok ? "sent" : (alert && alert.skipped) || "error",
  });
};

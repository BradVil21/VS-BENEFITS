// Vercel serverless function: handle a BUSINESS (group) quote submission.
//
// On submit it:
//   1. Creates/updates the contact in HubSpot (owner name, phone, company, employees, location).
//   2. Sends the lead a branded VS Health Benefits confirmation email with a "Fill out census form" link.
//   3. Emails Bradley an internal alert.
//   4. Adds a note to the contact summarizing the request.
//
// Safe by design: if HUBSPOT_PRIVATE_APP_TOKEN or RESEND_API_KEY are missing, the
// relevant step is skipped and the function still returns 200 so the website never breaks.
//
// See api/_lib.js for env vars.

const L = require("./_lib");

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
    censusUrl: censusUrl,
    leadEmail: leadEmail && leadEmail.ok ? "sent" : (leadEmail && leadEmail.skipped) || "error",
    alert: alert && alert.ok ? "sent" : (alert && alert.skipped) || "error",
  });
};

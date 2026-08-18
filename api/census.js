// Vercel serverless function: handle a completed EMPLOYEE CENSUS submission.
//
// On submit it:
//   1. Builds a CSV of the census.
//   2. Attaches the census summary to the contact in GoHighLevel as a note
//      — so it appears on the lead's record / Documents in your CRM.
//   3. Emails Bradley a "Census completed" summary (mockup #2 equivalent).
//   4. Sends the lead a short confirmation.
//
// Safe by design: missing tokens/keys just skip that step; always returns 200.

const L = require("./_lib");

function csvCell(s) {
  const v = String(s == null ? "" : s);
  return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
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

  const email = String(d.email || "").trim();
  const businessName = String(d.businessName || "").trim();
  const zip = String(d.businessZip || d.zip || "").trim();
  const people = Array.isArray(d.employees) ? d.employees : [];

  // Tally lives
  let emp = 0, sp = 0, ch = 0;
  people.forEach((p) => {
    const rel = String(p.relationship || "employee").toLowerCase();
    if (rel.indexOf("spouse") >= 0) sp++;
    else if (rel.indexOf("child") >= 0 || rel.indexOf("depend") >= 0) ch++;
    else emp++;
  });
  const totalLives = people.length;

  // ---- CSV ----
  const header = ["Relationship", "Linked To", "Name", "Age", "Gender"];
  const lines = [header.map(csvCell).join(",")];
  people.forEach((p) => {
    lines.push([p.relationship || "Employee", p.linkedTo || "", p.name || "", p.age || "", p.gender || ""].map(csvCell).join(","));
  });
  const csv = lines.join("\n");
  const safeBiz = (businessName || "lead").replace(/[^a-z0-9]+/gi, "_").replace(/^_|_$/g, "");
  const stamp = new Date().toISOString().slice(0, 10);
  const filename = "Employee-Census-" + safeBiz + "-" + stamp + ".csv";

  // ---- GoHighLevel: find or create the contact, then attach the census ----
  let contactId = String(d.contactId || d.c || "").trim() || null;
  try {
    if (!contactId && email) {
      // upsert doubles as a lookup: same email returns the existing contact.
      contactId = await L.upsertContact({ email: email });
    }
  } catch (e) { /* ignore */ }

  // Mark the stage on the contact. website_lead_stage was HubSpot-only, so it
  // rides along as the source plus a tag instead.
  try {
    if (contactId) {
      await L.upsertContact({
        email: email,
        zip: zip || undefined,
        website_lead_stage: "Census Received - Ready to Quote",
      });
      await L.addTagsToContact(contactId, ["census-received", "business-lead"]);
    }
  } catch (e) { /* ignore */ }

  // Build an HTML table for the note body
  const rowsHtml = people.map((p) =>
    "<tr>" +
    ["relationship", "name", "age", "gender"].map((k) =>
      '<td style="padding:4px 8px;border:1px solid #ddd">' + L.esc(p[k] || (k === "relationship" ? "Employee" : "")) + "</td>"
    ).join("") + "</tr>"
  ).join("");
  const noteHtml =
    "<b>Employee census completed</b><br>" +
    (businessName ? "Business: " + L.esc(businessName) + "<br>" : "") +
    "ZIP: " + L.esc(zip) + " &nbsp;·&nbsp; " + emp + " employees · " + sp + " spouses · " + ch + " children · <b>" + totalLives + " total lives</b><br><br>" +
    '<table style="border-collapse:collapse;font-size:13px"><tr>' +
    ["Relationship", "Name", "Age", "Gender"].map((h) => '<th style="padding:4px 8px;border:1px solid #ddd;background:#f2f6fb;text-align:left">' + h + "</th>").join("") +
    "</tr>" + rowsHtml + "</table>";

  let fileId = null;
  try { fileId = await L.uploadFile(filename, csv, "text/csv"); } catch (e) { /* ignore */ }
  try { if (contactId) await L.addNoteToContact(contactId, noteHtml, fileId); } catch (e) { /* ignore */ }

  // ---- Emails ----
  const inner =
    '<div style="background:linear-gradient(135deg,#16447f,#0f2f5c);margin:-30px -30px 22px;padding:22px 30px">' +
    '<span style="color:#fff;font-size:20px;font-weight:800">Census form completed</span>' +
    '<span style="color:#9fc0ef;font-size:13px;display:block;margin-top:3px">' + L.esc(new Date().toLocaleString("en-US", { timeZone: "America/New_York" })) + " ET</span></div>" +
    (businessName ? '<p style="margin:0 0 6px;font-size:16px"><b>' + L.esc(businessName) + "</b></p>" : "") +
    (email ? '<p style="margin:0 0 4px;font-size:14px;color:#2f7de0">' + L.esc(email) + "</p>" : "") +
    '<p style="margin:0 0 14px;font-size:14px">Business ZIP: <b>' + L.esc(zip) + "</b> &nbsp;·&nbsp; " +
    emp + " employees · " + sp + " spouses · " + ch + " children · <b>" + totalLives + " total lives</b></p>" +
    '<table style="border-collapse:collapse;width:100%;font-size:13px">' +
    '<tr>' + ["Relationship", "Name", "Age", "Gender"].map((h) => '<th style="padding:8px;border:1px solid #e5ebf2;background:#f2f6fb;text-align:left">' + h + "</th>").join("") + "</tr>" +
    people.map((p) => "<tr>" + ["relationship", "name", "age", "gender"].map((k) => '<td style="padding:8px;border:1px solid #e5ebf2">' + L.esc(p[k] || (k === "relationship" ? "Employee" : "")) + "</td>").join("") + "</tr>").join("") +
    "</table>" +
    '<p style="margin:16px 0 0;font-size:13px;color:#5a6b80">A CSV (' + L.esc(filename) + ") " + (fileId ? "has been saved to this contact's record." : "is attached below.") + "</p>";

  let alert = { skipped: "no_notify" };
  try {
    alert = await L.sendEmail({
      to: L.CFG.notify,
      subject: "✅ Census completed: " + (businessName || email || "lead") + " (" + totalLives + " lives)",
      html: L.shell(inner, "Census completed — " + totalLives + " lives"),
    });
  } catch (e) { /* ignore */ }

  // Confirmation to the lead
  try {
    if (email) {
      const c = L.shell(
        '<h1 style="margin:0 0 14px;font-size:21px;font-weight:800">Thanks — we\'ve got your census</h1>' +
        '<p style="margin:0 0 14px;font-size:15px;line-height:1.6">' + (businessName ? "For <b>" + L.esc(businessName) + "</b>: " : "") +
        "we received your employee census (" + totalLives + " total lives) and we're preparing your group options now.</p>" +
        '<p style="margin:0 0 14px;font-size:15px;line-height:1.6">Bradley will reach out shortly to review plans and pricing with you. If anything changes, just reply to this email.</p>' +
        '<p style="margin:18px 0 0;font-size:15px">— <b>Bradley Vilsaint</b>, VS Health Benefits</p>',
        "We received your census — quote on the way."
      );
      await L.sendEmail({ to: email, subject: "We received your census — quote on the way", html: c });
    }
  } catch (e) { /* ignore */ }

  res.status(200).json({
    ok: true,
    contactId: contactId || null,
    fileId: fileId || null,
    totals: { employees: emp, spouses: sp, children: ch, totalLives: totalLives },
    alert: alert && alert.ok ? "sent" : (alert && alert.skipped) || "error",
  });
};

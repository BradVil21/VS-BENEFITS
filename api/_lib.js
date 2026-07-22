// Shared helpers for VS Health Benefits serverless functions.
// - HubSpot REST calls (private-app token, server-side only)
// - Resend transactional email (brand sender)
// - Branded HTML email templates
//
// ENV VARS (set in Vercel -> Project -> Settings -> Environment Variables):
//   HUBSPOT_PRIVATE_APP_TOKEN   already used by api/hubspot-ticket.js
//   RESEND_API_KEY              from resend.com (free tier). If missing, email is skipped (no crash).
//   FROM_EMAIL                  optional, default "VS Health Benefits <quotes@vshealthbenefits.com>"
//   REPLY_TO_EMAIL              optional, default the notify address below
//   NOTIFY_EMAIL                optional, where lead/census alerts go. Default bvilsainthealth@gmail.com
//   SITE_URL                    optional, default https://www.vshealthbenefits.com

const HS = "https://api.hubapi.com";

const CFG = {
  brand: "VS Health Benefits",
  site: process.env.SITE_URL || "https://www.vshealthbenefits.com",
  from: process.env.FROM_EMAIL || "VS Health Benefits <quotes@vshealthbenefits.com>",
  replyTo: process.env.REPLY_TO_EMAIL || process.env.NOTIFY_EMAIL || "bvilsainthealth@gmail.com",
  notify: process.env.NOTIFY_EMAIL || "bvilsainthealth@gmail.com",
  navy: "#16447f",
  teal: "#0db5a6",
};

function esc(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

// ---------- HubSpot ----------
async function hs(path, method, body) {
  const token = process.env.HUBSPOT_PRIVATE_APP_TOKEN;
  if (!token) return { ok: false, skipped: "no_hs_token", status: 0, json: null };
  const r = await fetch(HS + path, {
    method: method || "GET",
    headers: {
      Authorization: "Bearer " + token,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  let json = null;
  try { json = await r.json(); } catch (e) { /* ignore */ }
  return { ok: r.ok, status: r.status, json };
}

// Create or update a contact by email. Returns contactId (or null).
async function upsertContact(props) {
  const email = String(props.email || "").trim().toLowerCase();
  if (!email) return null;
  // Try find first
  const search = await hs("/crm/v3/objects/contacts/search", "POST", {
    filterGroups: [{ filters: [{ propertyName: "email", operator: "EQ", value: email }] }],
    properties: ["email"],
    limit: 1,
  });
  const existing =
    search.ok && search.json && search.json.results && search.json.results[0]
      ? search.json.results[0].id
      : null;

  const clean = {};
  Object.keys(props).forEach((k) => {
    const v = props[k];
    if (v != null && String(v).trim() !== "") clean[k] = String(v).trim();
  });

  if (existing) {
    await hs("/crm/v3/objects/contacts/" + existing, "PATCH", { properties: clean });
    return existing;
  }
  const created = await hs("/crm/v3/objects/contacts", "POST", { properties: clean });
  return created.ok && created.json ? created.json.id : null;
}

// Create a Note engagement, optionally with a file attachment, associated to a contact.
async function addNoteToContact(contactId, html, attachmentId) {
  if (!contactId) return null;
  const props = { hs_note_body: html, hs_timestamp: new Date().toISOString() };
  if (attachmentId) props.hs_attachment_ids = String(attachmentId);
  // association type 202 = note_to_contact (default)
  const body = {
    properties: props,
    associations: [
      {
        to: { id: contactId },
        types: [{ associationCategory: "HUBSPOT_DEFINED", associationTypeId: 202 }],
      },
    ],
  };
  const r = await hs("/crm/v3/objects/notes", "POST", body);
  return r.ok && r.json ? r.json.id : null;
}

// Upload a text file (e.g. CSV) to HubSpot Files and return its fileId.
// Uses global FormData/Blob (Node 18+ on Vercel).
async function uploadFile(filename, text, mime) {
  const token = process.env.HUBSPOT_PRIVATE_APP_TOKEN;
  if (!token) return null;
  try {
    const form = new FormData();
    form.append("file", new Blob([text], { type: mime || "text/csv" }), filename);
    form.append("folderPath", "/lead-census");
    form.append(
      "options",
      JSON.stringify({ access: "PRIVATE", overwrite: false, duplicateValidationStrategy: "NONE" })
    );
    const r = await fetch(HS + "/files/v3/files", {
      method: "POST",
      headers: { Authorization: "Bearer " + token },
      body: form,
    });
    const json = await r.json().catch(() => null);
    return r.ok && json ? json.id : null;
  } catch (e) {
    return null;
  }
}

// ---------- Email (Resend) ----------
async function sendEmail({ to, subject, html, replyTo }) {
  const key = process.env.RESEND_API_KEY;
  if (!key) return { ok: false, skipped: "no_resend_key" };
  if (!to) return { ok: false, skipped: "no_recipient" };
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: CFG.from,
        to: Array.isArray(to) ? to : [to],
        reply_to: replyTo || CFG.replyTo,
        subject: subject,
        html: html,
      }),
    });
    const json = await r.json().catch(() => null);
    return { ok: r.ok, status: r.status, json };
  } catch (e) {
    return { ok: false, error: String((e && e.message) || e) };
  }
}

// ---------- Branded email shell ----------
function shell(innerHtml, preheader) {
  return `<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;background:#f2f5f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#16202e">
<span style="display:none;visibility:hidden;opacity:0;height:0;width:0;overflow:hidden">${esc(preheader || "")}</span>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f2f5f9;padding:24px 0">
<tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:600px;max-width:92%;background:#ffffff;border-radius:14px;overflow:hidden;box-shadow:0 6px 24px rgba(16,32,60,.08)">
  <tr><td style="background:linear-gradient(135deg,${CFG.navy},#0f2f5c);padding:22px 30px">
    <span style="color:#fff;font-size:19px;font-weight:800;letter-spacing:-.01em">VS Health Benefits</span>
    <span style="color:#9fc0ef;font-size:12px;display:block;margin-top:2px">Health insurance, made simple</span>
  </td></tr>
  <tr><td style="padding:30px">${innerHtml}</td></tr>
  <tr><td style="padding:18px 30px;background:#f7f9fc;border-top:1px solid #e5ebf2;color:#5a6b80;font-size:12px;line-height:1.6">
    VS Health Benefits · <a href="${CFG.site}" style="color:${CFG.navy}">vshealthbenefits.com</a><br>
    You're receiving this because you requested a quote at vshealthbenefits.com.
  </td></tr>
</table>
</td></tr></table></body></html>`;
}

function btn(href, label) {
  return `<table role="presentation" cellpadding="0" cellspacing="0" style="margin:8px 0 4px"><tr>
    <td style="border-radius:10px;background:${CFG.navy}">
      <a href="${href}" style="display:inline-block;padding:13px 26px;color:#fff;font-weight:700;font-size:15px;text-decoration:none;border-radius:10px">${esc(label)}</a>
    </td></tr></table>`;
}

// Confirmation email to a BUSINESS lead (mockup #1 equivalent, branded).
function businessLeadEmail({ firstName, businessName, censusUrl }) {
  const hi = firstName ? "Hello " + esc(firstName) + "," : "Hello,";
  const biz = businessName ? " for <strong>" + esc(businessName) + "</strong>" : "";
  const inner = `
    <h1 style="margin:0 0 14px;font-size:22px;font-weight:800;color:#16202e">Your group health quote${biz} — quick info needed</h1>
    <p style="margin:0 0 14px;font-size:15px;line-height:1.6">${hi}</p>
    <p style="margin:0 0 14px;font-size:15px;line-height:1.6">Thanks for reaching out about employee health insurance. To get your group quote started, I just need a quick census of who you'd like to cover:</p>
    <ul style="margin:0 0 18px;padding-left:20px;font-size:15px;line-height:1.7">
      <li>Ages and genders of your employees (and any spouses/children)</li>
      <li>The ZIP code of your business</li>
    </ul>
    ${btn(censusUrl, "📋  Fill out census form")}
    <p style="margin:16px 0 0;font-size:15px;line-height:1.6">It takes about two minutes. I'll review it and call to introduce myself and walk you through your options — I saw your request and I'm on it.</p>
    <p style="margin:18px 0 0;font-size:15px;line-height:1.6">Talk soon,<br><strong>Bradley Vilsaint</strong><br>VS Health Benefits</p>`;
  return shell(inner, "Just need a quick employee census to build your group quote.");
}

// Internal alert to Bradley when a business quote comes in.
function bizAlertEmail(d) {
  const rows = [
    ["Business", d.businessName],
    ["Contact", ((d.ownerFirstName || "") + " " + (d.ownerLastName || "")).trim()],
    ["Email", d.contactEmail],
    ["Phone", d.contactPhone || d.businessPhone],
    ["Employees", d.employees],
    ["Requested coverage", d.requestedCoverage],
    ["Currently insured", d.currentlyInsured],
    ["Coverage start", d.coverageStart],
    ["Location", [d.businessAddress, d.businessState, d.businessZip].filter(Boolean).join(", ")],
    ["Situations", Array.isArray(d.situations) ? d.situations.join(", ") : d.situations],
  ].filter((r) => r[1]);
  const trs = rows
    .map(
      (r) =>
        `<tr><td style="padding:7px 10px;border-bottom:1px solid #eef2f7;color:#5a6b80;font-size:13px;white-space:nowrap">${esc(r[0])}</td>
         <td style="padding:7px 10px;border-bottom:1px solid #eef2f7;font-size:14px;font-weight:600">${esc(r[1])}</td></tr>`
    )
    .join("");
  const inner = `
    <h1 style="margin:0 0 12px;font-size:20px;font-weight:800">🏢 New business quote request</h1>
    <table role="presentation" width="100%" style="border-collapse:collapse;margin-top:8px">${trs}</table>
    <p style="margin:16px 0 0;font-size:13px;color:#5a6b80">A confirmation + census link was sent to the contact. Census will be saved to their contact record in HubSpot.</p>`;
  return shell(inner, "New business quote request");
}

module.exports = {
  CFG, esc, hs, upsertContact, addNoteToContact, uploadFile, sendEmail,
  shell, btn, businessLeadEmail, bizAlertEmail,
};

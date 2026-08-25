// Shared helpers for VS Health Benefits serverless functions.
// - GoHighLevel REST calls (private integration token, server-side only)
// - Resend transactional email (brand sender)
// - Branded HTML email templates
//
// HubSpot has been removed entirely. upsertContact/addNoteToContact keep their
// names so the endpoints that call them did not have to change shape, but they
// now write to GoHighLevel. uploadFile is a no-op kept for the same reason -
// see its comment.
//
// ENV VARS (set in Vercel -> Project -> Settings -> Environment Variables):
//   GHL_PIT_TOKEN               private integration token (pit-...). If missing,
//                               CRM writes are skipped and email still sends.
//   GHL_LOCATION_ID             optional, defaults to the VS Health Benefits sub-account
//   RESEND_API_KEY              from resend.com. If missing, email is skipped (no crash).
//   FROM_EMAIL                  optional, default "VS Health Benefits <quotes@vshealthbenefits.com>"
//   REPLY_TO_EMAIL              optional, default the notify address below
//   NOTIFY_EMAIL                optional, where lead/census alerts go. Default bvilsainthealth@gmail.com
//   SITE_URL                    optional, default https://www.vshealthbenefits.com

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";
const GHL_LOCATION = process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU";

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

// ---------- GoHighLevel ----------
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

// Kept under the old name so callers did not need rewriting. Callers still pass
// HubSpot-style property names (firstname, lastname, zip, company...), so those
// are mapped to GHL's fields here rather than at every call site. Anything that
// has no GHL equivalent is folded into the contact's source/tags instead of
// being silently dropped.
async function upsertContact(props) {
  const p = props || {};
  const email = String(p.email || "").trim().toLowerCase();
  const phone = String(p.phone || "").trim();
  if (!email && !phone) return null;

  const body = { locationId: GHL_LOCATION };
  if (email) body.email = email;
  if (phone) body.phone = phone;

  const first = String(p.firstname || p.firstName || "").trim();
  const last = String(p.lastname || p.lastName || "").trim();
  if (first) body.firstName = first;
  if (last) body.lastName = last;
  if (first || last) body.name = (first + " " + last).trim();

  const company = String(p.company || "").trim();
  if (company) body.companyName = company;

  const state = String(p.state || "").trim();
  if (state) body.state = state;

  const zip = String(p.zip || p.postalCode || "").trim();
  if (zip) body.postalCode = zip;

  const address = String(p.address || "").trim();
  if (address) body.address1 = address;

  // website_lead_stage was a HubSpot-only property. Carry it as the source line
  // so the context is not lost on the record.
  const stage = String(p.website_lead_stage || "").trim();
  body.source = stage || "Website";

  const r = await ghl("/contacts/upsert", "POST", body);
  const c = r.json && (r.json.contact || r.json.data || r.json);
  return r.ok && c && c.id ? c.id : null;
}

// Notes in GHL are plain text, so any HTML the callers built for HubSpot gets
// flattened rather than rendered as tag soup on the contact record.
function htmlToText(html) {
  return String(html == null ? "" : html)
    .replace(/<\s*br\s*\/?>/gi, "\n")
    .replace(/<\s*\/(tr|p|div|h[1-6])\s*>/gi, "\n")
    .replace(/<\s*\/td\s*>/gi, "  ")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/\n{3,}/g, "\n\n")
    .trim()
    .slice(0, 5000);
}

async function addNoteToContact(contactId, html, attachmentId) {
  if (!contactId) return null;
  let text = htmlToText(html);
  if (attachmentId) text += "\n\n(attachment reference: " + attachmentId + ")";
  const r = await ghl("/contacts/" + contactId + "/notes", "POST", { body: text });
  return r.ok && r.json && r.json.note ? r.json.note.id : (r.ok ? true : null);
}

async function addTagsToContact(contactId, tags) {
  if (!contactId || !tags || !tags.length) return null;
  const r = await ghl("/contacts/" + contactId + "/tags", "POST", { tags: tags });
  return r.ok;
}

// No-op. This used to push the census CSV into HubSpot Files and return a file
// id that addNoteToContact attached to the note. GHL's media library is not a
// drop-in equivalent, and the census CSV already goes out on the alert email,
// which is where it actually gets used. Returns null so callers skip the
// attachment path without any of them needing to change.
async function uploadFile() {
  return null;
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
    <p style="margin:16px 0 0;font-size:13px;color:#5a6b80">A confirmation + census link was sent to the contact. The census is saved to their contact record in GoHighLevel.</p>`;
  return shell(inner, "New business quote request");
}


// ---------- Lead routing (individual/family vs business) ----------
// One place decides which portal pipeline a lead belongs in, so the webchat,
// the phone agent and the generic GHL webhook can never disagree about it.
//
// The decision is tag-driven: a contact carrying any of these tags in GHL is an
// employer/group lead and belongs on the Business Leads board. Extend the list
// without a deploy through the GHL_BUSINESS_TAGS env var (comma separated).
const BUSINESS_TAGS = [
  "business-lead", "business", "biz-lead", "group-quote", "group-health",
  "group-lead", "employer", "employer-lead", "small-business", "company",
];

// Tags reach us as an array, a comma string, or occasionally a JSON string.
function normTags(v) {
  let raw = v;
  if (typeof raw === "string") {
    const t = raw.trim();
    if (t.charAt(0) === "[") { try { raw = JSON.parse(t); } catch (e) { raw = t.split(","); } }
    else raw = t.split(",");
  }
  if (!Array.isArray(raw)) return [];
  return raw
    .map(function (t) { return String(t == null ? "" : t).trim().toLowerCase().replace(/\s+/g, "-").slice(0, 60); })
    .filter(Boolean);
}

// `explicit` is an override a caller already knows ("business", "individual",
// "family", "group"...). It always beats the tags.
function isBusinessLead(explicit, tags) {
  const e = String(explicit == null ? "" : explicit).trim().toLowerCase();
  if (e === "business" || e === "group" || e === "employer" || e === "biz") return true;
  if (e === "individual" || e === "family" || e === "personal") return false;
  const extra = String(process.env.GHL_BUSINESS_TAGS || "")
    .split(",").map(function (t) { return t.trim().toLowerCase().replace(/\s+/g, "-"); })
    .filter(Boolean);
  const set = {};
  BUSINESS_TAGS.concat(extra).forEach(function (t) { set[t] = true; });
  return (tags || []).some(function (t) { return set[t] === true; });
}

module.exports = {
  CFG, esc, ghl, upsertContact, addNoteToContact, addTagsToContact, uploadFile, sendEmail,
  shell, btn, businessLeadEmail, bizAlertEmail,
  BUSINESS_TAGS, normTags, isBusinessLead,
};

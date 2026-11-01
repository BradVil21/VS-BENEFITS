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
//   NOTIFY_EMAIL                optional, where lead/census alerts go. Default info@vshealthbenefits.com
//   SITE_URL                    optional, default https://www.vshealthbenefits.com

const GHL_BASE = "https://services.leadconnectorhq.com";
const GHL_VERSION = "2021-07-28";
const GHL_LOCATION = process.env.GHL_LOCATION_ID || "cNCy6JUURpb4eBDdb9bU";

const CFG = {
  brand: "VS Health Benefits",
  site: process.env.SITE_URL || "https://www.vshealthbenefits.com",
  from: process.env.FROM_EMAIL || "VS Health Benefits <quotes@vshealthbenefits.com>",
  replyTo: process.env.REPLY_TO_EMAIL || process.env.NOTIFY_EMAIL || "info@vshealthbenefits.com",
  notify: process.env.NOTIFY_EMAIL || "info@vshealthbenefits.com",
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

// ---------- Visitor origin (IP + geo + device) ----------
// Every lead that reaches the portal carries a `meta` block, which is what the
// "Submission origin" panel on a lead card renders and what the Block button
// bans. It is assembled here rather than in each endpoint so the quote funnel,
// the subsidy calculator, the contact form and the phone agent can never
// disagree about what an IP is.
//
// The IP is taken from the request headers, NOT from whatever the browser
// posted. A browser-supplied IP comes from a third-party lookup that an ad
// blocker, a privacy extension or a corporate proxy will happily eat, and it is
// trivially forgeable by anyone who wants to dodge a ban. Vercel's edge sets
// x-forwarded-for with the real client on the left, so that is the truth.
//
// The browser's own lookup is still useful for the two things the headers do not
// carry - the ISP/organisation name ("Charter Communications") and the user
// agent - so those are taken from the payload when present.

function clientIp(req) {
  const h = (req && req.headers) || {};
  const xff = String(h["x-forwarded-for"] || h["X-Forwarded-For"] || "");
  const first = xff.split(",")[0].trim();
  return (first || String(h["x-real-ip"] || h["x-vercel-forwarded-for"] || "").trim()).slice(0, 60);
}

// Vercel geo headers are percent-encoded (a city can contain a space).
function geoHeader(req, name) {
  const h = (req && req.headers) || {};
  const v = String(h[name] || "");
  if (!v) return "";
  try { return decodeURIComponent(v).slice(0, 80); } catch (e) { return v.slice(0, 80); }
}

// Merge what the server knows with what the browser sent. Server wins on the IP
// and on geo it actually has; the browser fills the gaps.
function visitorMeta(req, d) {
  const sent = (d && typeof d.meta === "object" && d.meta) || {};
  const s = function (v, max) { return String(v == null ? "" : v).trim().slice(0, max || 80); };

  const ip = clientIp(req) || s(sent.ip, 60);
  const meta = {
    ip: ip,
    ipCity: geoHeader(req, "x-vercel-ip-city") || s(sent.ipCity),
    ipRegion: geoHeader(req, "x-vercel-ip-country-region") || s(sent.ipRegion),
    ipCountry: geoHeader(req, "x-vercel-ip-country") || s(sent.ipCountry),
    // Only the browser lookup knows the ISP.
    ipOrg: s(sent.ipOrg, 120),
    device: s(sent.device || (req && req.headers && req.headers["user-agent"]), 300),
    tz: s(sent.tz, 60),
    referrer: s(sent.referrer, 300),
    at: Date.now(),
  };
  // Do not store an all-empty block - an empty panel on a card is worse than no
  // panel, because it looks like the capture is broken rather than absent.
  return meta.ip || meta.ipCity || meta.device ? meta : null;
}


// ── Junk-lead filter + auto-block (2026-10-31) ─────────────────────────────
// Website forms get "Test Test / test@test.com / (101) 111-1111" style junk.
// junkSignals() scores a submission on three independent checks: the name, the
// email and the phone. ONE signal is not enough to drop anything - a real
// person can be called "Test" or fat-finger a number - so that lead goes through
// tagged "suspect-lead". TWO or more signals is junk: no CRM contact, no board
// card, no alert, and the visitor's IP is put on the site block list for
// AUTO_BLOCK_DAYS. The edge middleware already enforces vs_state/blocked_ips;
// auto entries carry `expires` so a shared or recycled address frees itself up.
// Unblock any time from the portal's Blocked IPs tab.
//
// Never applied to the admin portal's own saves or to GHL -> portal syncs.
// LEAD_FILTER_DISABLED=1 turns the whole thing off without a deploy.
const JUNK_WORDS = ["test","tester","testing","asdf","asdfg","asdfgh","qwerty","fake","none","na","n/a","abc","abcd","xxx","xx","x","aaa","aa","a","blah","sample","demo","dummy","nobody","noname","no name","anonymous","foo","bar","lol","hello","hi","sdf","jkl","zzz"];
const JUNK_DOMAINS = ["test.com","example.com","example.org","example.net","test.test","fake.com","asdf.com","abc.com","mailinator.com","guerrillamail.com","10minutemail.com","tempmail.com","temp-mail.org","yopmail.com","sharklasers.com","trashmail.com","getnada.com","dispostable.com","maildrop.cc","throwawaymail.com"];
const ALLOW_EMAIL_DOMAINS = ["vshealthbenefits.com"];

function junkName(first, last) {
  const f = String(first || "").trim().toLowerCase(), l = String(last || "").trim().toLowerCase();
  const full = (f + " " + l).trim();
  if (!full) return "";
  if (/\d/.test(full)) return "name has digits";
  const parts = full.split(/\s+/);
  if (parts.every(function (p) { return JUNK_WORDS.indexOf(p) >= 0; })) return "placeholder name";
  if (parts.some(function (p) { return /^(.)\1{2,}$/.test(p); })) return "repeated letters";
  if (/^[^aeiouy\s]{5,}$/.test(full.replace(/\s/g, ""))) return "keyboard mash";
  return "";
}
function junkEmail(email) {
  const e = String(email || "").trim().toLowerCase();
  if (!e) return "";
  const at = e.lastIndexOf("@");
  if (at < 1) return "invalid email";
  const local = e.slice(0, at), dom = e.slice(at + 1);
  if (ALLOW_EMAIL_DOMAINS.indexOf(dom) >= 0) return "";
  if (JUNK_DOMAINS.indexOf(dom) >= 0) return "test/disposable domain";
  if (JUNK_WORDS.indexOf(local.replace(/[\d._-]+$/, "")) >= 0 && /^(test|example|asdf|fake|abc)\b/.test(dom)) return "placeholder email";
  if (/^(test|asdf|qwerty|fake|noreply|no-reply)\d*$/.test(local) && /^(test|asdf|fake|example)/.test(dom)) return "placeholder email";
  return "";
}
function junkPhone(phone) {
  let d = String(phone || "").replace(/\D/g, "");
  if (!d) return "";
  if (d.length === 11 && d.charAt(0) === "1") d = d.slice(1);
  if (d.length !== 10) return "wrong length";
  const area = d.slice(0, 3), exch = d.slice(3, 6);
  if (/^(\d)\1{9}$/.test(d)) return "all same digit";
  if (area.charAt(0) === "0" || area.charAt(0) === "1") return "invalid area code";
  if (exch.charAt(0) === "0" || exch.charAt(0) === "1") return "invalid exchange";
  if (area.slice(1) === "99" || area === "555" || exch === "555") return "reserved number";
  if (d === "1234567890" || d === "0123456789" || d === "9876543210") return "sequential";
  const counts = {}; for (const c of d) counts[c] = (counts[c] || 0) + 1;
  if (Math.max.apply(null, Object.values(counts)) >= 8) return "mostly one digit";
  return "";
}
// Returns { signals: [..reasons], junk: bool, suspect: bool }.
function junkSignals(d) {
  if (process.env.LEAD_FILTER_DISABLED === "1") return { signals: [], junk: false, suspect: false };
  d = d || {};
  const first = d.firstName || d.first_name || d.firstname || d.ownerFirstName || "";
  const last = d.lastName || d.last_name || d.lastname || d.ownerLastName || "";
  let nm = junkName(first, last);
  if (!first && !last && d.name) nm = junkName(d.name, "");
  const em = junkEmail(d.email || d.contactEmail);
  const ph = junkPhone(d.phone || d.contactPhone || d.businessPhone);
  const signals = [];
  if (nm) signals.push("name: " + nm);
  if (em) signals.push("email: " + em);
  if (ph) signals.push("phone: " + ph);
  return { signals: signals, junk: signals.length >= 2, suspect: signals.length === 1 };
}

// Same normalisation as ipKey() in middleware.js / admin.html (IPv4 exact, IPv6 /64).
function ipKeyCjs(raw) {
  let ip = String(raw == null ? "" : raw).trim().toLowerCase();
  if (!ip) return "";
  if (ip.charAt(0) === "[") { const c = ip.indexOf("]"); ip = c > 0 ? ip.slice(1, c) : ip.slice(1); }
  const z = ip.indexOf("%"); if (z > 0) ip = ip.slice(0, z);
  const v4 = /^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?$/.exec(ip); if (v4) return v4[1];
  const mapped = /^::ffff:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/.exec(ip); if (mapped) return mapped[1];
  if (ip.indexOf(":") < 0) return "";
  let parts;
  if (ip.indexOf("::") >= 0) {
    const h = ip.split("::"), head = h[0] ? h[0].split(":") : [], tail = h[1] ? h[1].split(":") : [];
    parts = head.concat(new Array(Math.max(0, 8 - head.length - tail.length)).fill("0"), tail);
  } else parts = ip.split(":");
  parts = parts.slice(0, 4).map(function (x) { return (x || "0").replace(/^0+(?=.)/, ""); });
  while (parts.length < 4) parts.push("0");
  if (!/^[0-9a-f]{1,4}$/.test(parts[0])) return "";
  return parts.join(":") + "::/64";
}

const AUTO_BLOCK_DAYS = Number(process.env.AUTO_BLOCK_DAYS || 30);
// Puts the visitor on vs_state/blocked_ips. Never throws; returns what happened.
async function autoBlockVisitor(meta, reasons, sample) {
  try {
    if (process.env.AUTO_BLOCK_DISABLED === "1") return { ok: false, skipped: "disabled" };
    const ip = meta && meta.ip; const key = ipKeyCjs(ip);
    if (!key) return { ok: false, skipped: "no_ip" };
    const FS = require("./_fs");
    const now = Date.now();
    const rec = {
      id: "auto_" + now.toString(36), ip: key, label: String(ip).slice(0, 60),
      reason: "auto: junk lead", note: (reasons || []).join("; ").slice(0, 200) + (sample ? " | " + String(sample).slice(0, 120) : ""),
      by: "auto-filter", city: [meta.ipCity, meta.ipRegion].filter(Boolean).join(", ").slice(0, 80),
      org: String(meta.ipOrg || "").slice(0, 120), created: now, expires: now + AUTO_BLOCK_DAYS * 86400000, auto: true,
    };
    const r = await FS.appendRecord("blocked_ips", rec, function (x) { return x && x.ip === key; }, function () { return false; });
    return { ok: !!r.ok, action: r.action, ip: key };
  } catch (e) { return { ok: false, skipped: "exception" }; }
}

module.exports = {
  CFG, esc, ghl, clientIp, geoHeader, visitorMeta, upsertContact, addNoteToContact, addTagsToContact, uploadFile, sendEmail,
  shell, btn, businessLeadEmail, bizAlertEmail,
  BUSINESS_TAGS, normTags, isBusinessLead,
  junkSignals, junkPhone, autoBlockVisitor, ipKeyCjs,
};

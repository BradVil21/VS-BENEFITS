// Creator dashboard API (added 2026-11-13). Powers vshealthbenefits.com/creator.
//
// POST /api/creator  (rewritten to /api/voice-lookup?op=creator)
//   { op:"login", email }        -> emails a one-time sign-in link (30 min).
//                                    Always answers ok, so it never reveals who
//                                    is or isn't a creator.
//   { op:"verify", t }           -> swaps that link token for a 30-day session.
//   { op:"stats", s }            -> the creator's own numbers.
//   { op:"click", code }         -> +1 link visit (sent once a day per browser
//                                    by vs-attribution.js).
//
// What a creator sees: their link, visits, quote requests, qualified referrals,
// earned / paid / owed and payout history. NEVER who they referred: each
// referral is a date and a status, nothing else. These are health insurance
// leads and the creator isn't licensed.
//
// The portal (vs_state/affiliates) is the source of truth; nothing here writes
// to it. A creator set to Declined loses access on their next page load.
//
// Tokens are HMAC-signed, stateless. Key: CREATOR_PORTAL_SECRET, or derived
// from GHL_PIT_TOKEN when that isn't set (both server-only).

const crypto = require("crypto");
const L = require("./_lib");
const F = require("./_fs");

const LINK_TTL = 30 * 60 * 1000;
const SESSION_TTL = 30 * 24 * 3600 * 1000;
const OK_STAGES = { approved: 1, active: 1, paused: 1 };

function key() {
  const k = process.env.CREATOR_PORTAL_SECRET || "";
  if (k) return k;
  const base = process.env.GHL_PIT_TOKEN || process.env.RESEND_API_KEY || "";
  return base ? crypto.createHash("sha256").update("vs-creator-portal:" + base).digest("hex") : "";
}
function b64u(s) { return Buffer.from(s).toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); }
function unb64u(s) { return Buffer.from(String(s).replace(/-/g, "+").replace(/_/g, "/"), "base64").toString("utf8"); }
function sign(obj) {
  const k = key(); if (!k) return "";
  const body = b64u(JSON.stringify(obj));
  return body + "." + crypto.createHmac("sha256", k).update(body).digest("base64url");
}
function check(tok, kind) {
  const k = key(); if (!k || !tok) return null;
  const parts = String(tok).split(".");
  if (parts.length !== 2) return null;
  const want = crypto.createHmac("sha256", k).update(parts[0]).digest("base64url");
  const a = Buffer.from(want), b = Buffer.from(parts[1]);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  let o = null; try { o = JSON.parse(unb64u(parts[0])); } catch (e) { return null; }
  if (!o || o.k !== kind || !o.i || !(o.e > Date.now())) return null;
  return o;
}

function normCode(v) { return String(v || "").toLowerCase().replace(/[^a-z0-9-]/g, "").slice(0, 40); }
function refOf(l) {
  const a = l && l.attribution; let r = a && a.ref ? a.ref : "";
  if (!r && a && a.source) { const m = /^Partner\s+\S+\s+(.+)$/.exec(String(a.source)); if (m) r = m[1]; }
  return normCode(r);
}
function day(ts) { return new Date(ts).toLocaleDateString("en-CA", { timeZone: "America/New_York" }); }

async function creators() { const r = await F.readStore("affiliates"); return r.ok ? (r.items || []) : null; }

function json(res, code, o) { res.status(code).json(o); }

async function login(d, req, res) {
  const email = String(d.email || "").trim().toLowerCase().slice(0, 160);
  const out = { ok: true };
  if (!/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(email)) return json(res, 200, out);
  const list = await creators();
  const c = (list || []).filter(function (x) { return x && String(x.email || "").trim().toLowerCase() === email && OK_STAGES[x.stage] && normCode(x.code); })[0];
  if (!c) return json(res, 200, out); // same answer either way
  const t = sign({ k: "link", i: c.id, e: Date.now() + LINK_TTL });
  if (!t) return json(res, 200, out);
  const url = L.CFG.site.replace(/\/$/, "") + "/creator#t=" + t;
  const first = L.esc(String(c.firstName || "").split(" ")[0]);
  const html = L.shell(
    '<p style="margin:0 0 14px">Hi' + (first ? " " + first : "") + ',</p>' +
    '<p style="margin:0 0 18px">Tap below to open your VS Health Benefits creator dashboard. The link works for 30 minutes.</p>' +
    L.btn(url, "Open my dashboard") +
    '<p style="margin:18px 0 0;font-size:13px;color:#5a6b80">Didn\'t ask for this? You can ignore this email.</p>',
    "Your creator dashboard sign-in link");
  const sent = await L.sendEmail({ to: email, subject: "Your creator dashboard sign-in link", html: html });
  if (!sent.ok) {
    // Fall back to the GHL contact (text + email through "Affiliate - Send Update").
    try {
      const AE = require("./_affiliate-event");
      if (AE.notifyLogin) await AE.notifyLogin(c, url);
    } catch (e) { /* nothing else to try */ }
  }
  return json(res, 200, out);
}

async function verify(d, req, res) {
  const o = check(d.t, "link");
  if (!o) return json(res, 401, { ok: false, error: "expired" });
  const list = await creators();
  const c = (list || []).filter(function (x) { return x && x.id === o.i; })[0];
  if (!c || !OK_STAGES[c.stage]) return json(res, 401, { ok: false, error: "no_access" });
  return json(res, 200, { ok: true, s: sign({ k: "sess", i: c.id, e: Date.now() + SESSION_TTL }) });
}

async function stats(d, req, res) {
  const o = check(d.s, "sess");
  if (!o) return json(res, 401, { ok: false, error: "signed_out" });
  const token = await F.fsToken();
  const [aff, ind, biz, clk] = await Promise.all([F.readStore("affiliates", token), F.readStore("leads", token), F.readStore("biz_leads", token), F.readStore("creator_clicks", token)]);
  if (!aff.ok) return json(res, 503, { ok: false, error: "try_again" });
  const c = (aff.items || []).filter(function (x) { return x && x.id === o.i; })[0];
  if (!c || !OK_STAGES[c.stage]) return json(res, 401, { ok: false, error: "no_access" });
  const code = normCode(c.code), reward = Number(c.reward) || 0, refs = c.refs || {};

  const list = [];
  (ind.items || []).forEach(function (l) { if (l && refOf(l) === code) list.push({ key: "ind:" + l.id, at: Number(l.created) || 0 }); });
  (biz.items || []).forEach(function (b) { if (b && refOf(b) === code) list.push({ key: "biz:" + b.id, at: Number(b.created) || 0 }); });
  list.sort(function (a, b) { return b.at - a.at; });
  let q = 0, unpaid = 0, paidN = 0;
  const referrals = list.map(function (x, i) {
    const r = refs[x.key];
    const st = r && r.q ? (r.paid ? "paid" : "qualified") : "requested";
    if (r && r.q) { q++; if (r.paid) paidN++; else unpaid++; }
    return { n: list.length - i, date: x.at ? day(x.at) : "", status: st, type: x.key.slice(0, 3) === "biz" ? "Business" : "Individual" };
  });
  const payouts = (c.payouts || []).slice().sort(function (a, b) { return (b.at || 0) - (a.at || 0); })
    .map(function (p) { return { date: p.at ? day(p.at) : "", amount: Number(p.amount) || 0, count: (p.keys || []).length, how: String(p.note || "").slice(0, 40) }; });
  const paidAmt = payouts.reduce(function (s, p) { return s + p.amount; }, 0);

  const cr = (clk.items || []).filter(function (x) { return x && x.code === code; })[0] || { total: 0, days: {} };
  const since = day(Date.now() - 29 * 864e5), today = day(Date.now());
  let clicks30 = 0; const spark = [];
  for (let i = 29; i >= 0; i--) { const dd = day(Date.now() - i * 864e5); const n = Number((cr.days || {})[dd]) || 0; spark.push(n); }
  Object.keys(cr.days || {}).forEach(function (dd) { if (dd >= since && dd <= today) clicks30 += Number(cr.days[dd]) || 0; });

  return json(res, 200, {
    ok: true,
    creator: { firstName: c.firstName || "", lastName: c.lastName || "", code: code, stage: c.stage, since: c.created ? day(c.created) : "" },
    link: L.CFG.site.replace(/\/$/, "") + "/" + code,
    reward: reward,
    totals: { clicks: Number(cr.total) || 0, clicks30: clicks30, spark: spark, requests: list.length, qualified: q, earned: q * reward, paid: paidAmt, owed: unpaid * reward, unpaid: unpaid },
    referrals: referrals.slice(0, 200),
    payouts: payouts,
  });
}

async function click(d, req, res) {
  const code = normCode(d.code);
  if (!code) return json(res, 200, { ok: true });
  try {
    const list = await creators();
    if (!list || !list.some(function (x) { return x && normCode(x.code) === code && OK_STAGES[x.stage]; })) return json(res, 200, { ok: true });
    const dd = day(Date.now()), cut = day(Date.now() - 400 * 864e5);
    await F.appendRecord("creator_clicks", { code: code, total: 1, days: { [dd]: 1 } },
      function (x) { return x && x.code === code; },
      function (ex) {
        ex.total = (Number(ex.total) || 0) + 1;
        ex.days = ex.days || {};
        ex.days[dd] = (Number(ex.days[dd]) || 0) + 1;
        Object.keys(ex.days).forEach(function (k) { if (k < cut) delete ex.days[k]; });
        return true;
      });
  } catch (e) { /* a lost click is fine */ }
  // Answer only after the write: Vercel can freeze the function once it responds.
  return json(res, 200, { ok: true });
}

module.exports = async function (req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") return json(res, 405, { error: "Method not allowed" });
  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};
  const op = String(d.op || (req.query && req.query.action) || "");
  try {
    if (op === "login") return await login(d, req, res);
    if (op === "verify") return await verify(d, req, res);
    if (op === "stats") return await stats(d, req, res);
    if (op === "click") return await click(d, req, res);
  } catch (e) { if (!res.headersSent) return json(res, 500, { ok: false, error: "server" }); return; }
  return json(res, 400, { ok: false, error: "bad_op" });
};
module.exports._sign = sign; module.exports._check = check;

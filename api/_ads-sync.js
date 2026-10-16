// Vercel serverless function: receive a Google Ads performance snapshot.
//
// Posted hourly by the Google Ads Script in google-ads/vs-ads-sync-script.js.
// Saved to Firestore vs_state/ads_perf as { items: [snapshot], ts }, which the
// admin portal's "Google Ads" tab listens to with onSnapshot, so the numbers on
// screen update the moment the script runs.
//
// ENV VARS:
//   ADS_SYNC_SECRET   required. The same value pasted into the Ads Script.
//                     Without it this endpoint refuses everything.

const crypto = require("crypto");
const FS = require("./_fs");

function same(a, b) {
  const x = Buffer.from(String(a || "")), y = Buffer.from(String(b || ""));
  return x.length === y.length && x.length > 0 && crypto.timingSafeEqual(x, y);
}
const num = function (v) { const n = Number(v); return isFinite(n) ? Math.round(n * 100) / 100 : 0; };
const str = function (v, n) { return String(v == null ? "" : v).slice(0, n || 120); };
function metrics(r) { return { imp: num(r.imp), clk: num(r.clk), cost: num(r.cost), conv: num(r.conv) }; }
function list(a, max, map) { return (Array.isArray(a) ? a : []).slice(0, max).map(function (r) { return Object.assign(map(r || {}), metrics(r || {})); }); }

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }
  const secret = process.env.ADS_SYNC_SECRET;
  if (!secret) { res.status(503).json({ error: "ADS_SYNC_SECRET is not set in Vercel" }); return; }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};
  if (!same(d.secret, secret)) { res.status(401).json({ error: "Bad secret" }); return; }

  const s = d.snapshot || {};
  const snap = {
    id: "ads_perf",
    syncedAt: Date.now(),
    account: { name: str(s.account && s.account.name, 80), id: str(s.account && s.account.id, 20),
               currency: str(s.account && s.account.currency, 6) || "USD", tz: str(s.account && s.account.tz, 40) },
    range: { start: str(s.range && s.range.start, 10), end: str(s.range && s.range.end, 10) },
    daily: list(s.daily, 1500, function (r) { return { d: str(r.d, 10), c: str(r.c, 80) }; }),
    campaigns: list(s.campaigns, 40, function (r) { return { name: str(r.name, 80), status: str(r.status, 20), primary: str(r.primary, 30),
      reasons: str(r.reasons, 200), bidding: str(r.bidding, 40), budget: num(r.budget) }; }),
    adGroups: list(s.adGroups, 100, function (r) { return { c: str(r.c, 80), g: str(r.g, 80), status: str(r.status, 20) }; }),
    keywords: list(s.keywords, 100, function (r) { return { c: str(r.c, 80), g: str(r.g, 80), kw: str(r.kw, 100), mt: str(r.mt, 12),
      qs: r.qs == null ? null : num(r.qs) }; }),
    terms: list(s.terms, 150, function (r) { return { c: str(r.c, 80), g: str(r.g, 80), term: str(r.term, 120) }; }),
    hours: list(s.hours, 24, function (r) { return { h: num(r.h) }; }),
    devices: list(s.devices, 6, function (r) { return { dev: str(r.dev, 20) }; }),
    policy: { disapproved: num(s.policy && s.policy.disapproved), limited: num(s.policy && s.policy.limited) },
  };

  // Read first for the updateTime precondition; retry once if the portal wrote in between.
  let out = { ok: false };
  for (let i = 0; i < 3 && !out.ok; i++) {
    const cur = await FS.readStore("ads_perf");
    out = await FS.writeStore("ads_perf", [snap], null, cur.updateTime, cur.exists);
  }
  res.status(out.ok ? 200 : 502).json({ ok: !!out.ok, rows: { daily: snap.daily.length, terms: snap.terms.length }, error: out.ok ? undefined : out });
};

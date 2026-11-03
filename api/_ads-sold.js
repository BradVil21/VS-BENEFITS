// Sold leads for Google Ads offline conversion import (added 2026-11-03).
//
// POST /api/ads-sold  { secret }   (rewritten to /api/voice-lookup?op=ads-sold)
//
// The weekly Google Ads script "VS Lead Engine - Hourly" calls this, then
// uploads each row as a "Sold Policy" conversion so Google learns which
// clicks turn into customers, not just which ones fill in a form.
//
// Only leads that came from a Google Ads click (a gclid was captured on the
// visitor's first landing by /vs-attribution.js) can be matched, and Google
// only accepts clicks from the last 90 days.
//
// ENV: ADS_SYNC_SECRET (same secret the hourly Ads sync script already uses).

const crypto = require("crypto");
const FS = require("./_fs");

const SOLD_INDIVIDUAL = ["sold", "enrolled"];
const SOLD_BUSINESS = ["won"];
const MAX_AGE_DAYS = 89;

function same(a, b) {
  const x = Buffer.from(String(a || "")), y = Buffer.from(String(b || ""));
  return x.length === y.length && x.length > 0 && crypto.timingSafeEqual(x, y);
}

// "2026-11-03 14:05:00-05:00" in America/New_York, the format Google expects.
function adsTime(ms) {
  const d = new Date(ms);
  const parts = {};
  new Intl.DateTimeFormat("en-US", {
    timeZone: "America/New_York", hour12: false,
    year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit",
    timeZoneName: "shortOffset",
  }).formatToParts(d).forEach(function (p) { parts[p.type] = p.value; });
  const off = /GMT([+-]\d+)(?::(\d+))?/.exec(parts.timeZoneName || "") || [null, "-5", "00"];
  const oh = Number(off[1]);
  const tz = (oh < 0 ? "-" : "+") + String(Math.abs(oh)).padStart(2, "0") + ":" + (off[2] || "00");
  const hh = parts.hour === "24" ? "00" : parts.hour;
  return parts.year + "-" + parts.month + "-" + parts.day + " " + hh + ":" + parts.minute + ":" + parts.second + tz;
}

function pick(items, soldStages, kind, now) {
  const out = [];
  (items || []).forEach(function (l) {
    if (!l || soldStages.indexOf(String(l.stage || l.status || "")) < 0) return;
    const a = l.attribution || {};
    const gclid = String(a.gclid || "").trim();
    if (!gclid) return;
    const at = Number(l.stageAt) || Number(l.updated) || Number(l.created) || 0;
    if (!at || now - at > MAX_AGE_DAYS * 864e5) return;
    const value = Number(l.premium || l.value || l.monthlyPremium || 0);
    out.push({ gclid: gclid, time: adsTime(at), value: value > 0 ? Math.round(value * 100) / 100 : 0, kind: kind });
  });
  return out;
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }
  const secret = process.env.ADS_SYNC_SECRET;
  if (!secret) { res.status(503).json({ error: "ADS_SYNC_SECRET is not set in Vercel" }); return; }
  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  if (!same(d && d.secret, secret)) { res.status(401).json({ error: "Bad secret" }); return; }

  const now = Date.now();
  const token = await FS.fsToken();
  const [ind, biz] = await Promise.all([FS.readStore("leads", token), FS.readStore("biz_leads", token)]);
  if (!ind.ok && !biz.ok) { res.status(502).json({ error: "Could not read leads", reason: ind.reason || biz.reason }); return; }

  const rows = pick(ind.items, SOLD_INDIVIDUAL, "individual", now).concat(pick(biz.items, SOLD_BUSINESS, "business", now));
  res.status(200).json({ ok: true, count: rows.length, rows: rows });
};

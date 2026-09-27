// Vercel serverless function: check a street address against the U.S. Census
// Bureau geocoder and return the standardized version.
//
// Used by the admin portal's "Verify address" button on a lead card. The Census
// geocoder is free, needs no API key, and matches against the official TIGER
// address ranges, so it is far more reliable for U.S. street addresses than the
// OpenStreetMap suggestions used for type-ahead.
//
// GET /api/address-verify?address=123 Main St&city=Miami&state=FL&zip=33101
// -> { ok: true, match: { street, city, state, zip, full }, candidates: n }
// -> { ok: false, reason: "no_match" | "missing" | "unavailable" }
//
// Safe by design: read-only, no data stored, 8 second timeout, always 200.

const DIRS = new Set(["N", "S", "E", "W", "NE", "NW", "SE", "SW"]);
const KEEP_UPPER = new Set(["PO", "US", "FM", "SR", "CR", "RR", "HWY"]);

function niceStreet(s) {
  return String(s || "")
    .toLowerCase()
    .split(/\s+/)
    .filter(Boolean)
    .map((w) => {
      const up = w.toUpperCase();
      if (DIRS.has(up) || KEEP_UPPER.has(up)) return up;
      if (/^\d+(st|nd|rd|th)$/.test(w)) return w; // 36th
      if (/^\d/.test(w)) return up; // 12a -> 12A
      return w.charAt(0).toUpperCase() + w.slice(1);
    })
    .join(" ");
}
function niceCity(s) {
  return String(s || "")
    .toLowerCase()
    .replace(/(^|[\s\-'.])([a-z])/g, (m, p, c) => p + c.toUpperCase());
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  const q = req.query || {};
  const clip = (v) => String(v || "").replace(/[\r\n]+/g, " ").trim().slice(0, 160);
  const address = clip(q.address), city = clip(q.city), state = clip(q.state).slice(0, 2), zip = clip(q.zip).slice(0, 10);
  if (!address || (!zip && !(city && state))) {
    res.status(200).json({ ok: false, reason: "missing" });
    return;
  }
  const line = [address, city, state, zip].filter(Boolean).join(", ");
  const url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?benchmark=Public_AR_Current&format=json&address=" + encodeURIComponent(line);
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 8000);
  try {
    const r = await fetch(url, { signal: ctrl.signal, headers: { Accept: "application/json" } });
    clearTimeout(timer);
    if (!r.ok) { res.status(200).json({ ok: false, reason: "unavailable" }); return; }
    const data = await r.json();
    const matches = (data && data.result && data.result.addressMatches) || [];
    if (!matches.length) { res.status(200).json({ ok: false, reason: "no_match" }); return; }
    const m = matches[0];
    // matchedAddress looks like "4600 SILVER HILL RD, WASHINGTON, DC, 20233"
    const parts = String(m.matchedAddress || "").split(",").map((x) => x.trim());
    const comp = m.addressComponents || {};
    const street = niceStreet(parts[0] || "");
    const mCity = niceCity(comp.city || parts[1] || "");
    const mState = String(comp.state || parts[2] || "").toUpperCase();
    const mZip = String(comp.zip || parts[3] || "");
    res.status(200).json({
      ok: true,
      match: { street, city: mCity, state: mState, zip: mZip, full: street + ", " + mCity + ", " + mState + " " + mZip },
      candidates: matches.length,
    });
  } catch (e) {
    clearTimeout(timer);
    res.status(200).json({ ok: false, reason: "unavailable" });
  }
};

// Real ACA plan quotes from HealthSherpa ONE for the subsidy calculator (helper, NOT its own function).
//
// Vercel's Hobby plan allows 12 serverless functions and api/ is at the cap, so this runs inside
// api/voice-lookup.js: vercel.json rewrites POST /api/plans to /api/voice-lookup?op=plans.
//
//   POST /api/plans  { zip, income, size, age1, age2, kids, fips? }
//     -> { plans:[...], count, aptc, county:{fips,name,state}, plan_year }
//     -> { needCounty:true, counties:[{fips,name,state}] }   when a ZIP spans counties
//     -> 503 { disabled:true }                                when HEALTHSHERPA_API_KEY is not set
//
// The calculator treats anything but a plan list as "show the estimate only", so the page never
// breaks if HealthSherpa is down, the key is missing, or the year's plans are not loaded yet.
//
// ENV VARS (Vercel -> Project -> Settings -> Environment Variables):
//   HEALTHSHERPA_API_KEY   required. From https://one.healthsherpa.com/portal.html (API Access). Keep it server-side.
//   HEALTHSHERPA_PLAN_YEAR optional, default 2027.
//
// HealthSherpa ONE API Terms: quote data is used only to show the visitor their own quote, kept in memory
// for at most 15 minutes, never stored or logged with personal details. Plans are sorted by the visitor's
// net premium only, never by carrier or commission (CMS non-preferential display); the page discloses that.

const API = "https://api.one.healthsherpa.com/v1";
const TTL = 15 * 60 * 1000;
const cache = new Map();          // key -> { at, body }
const hits = new Map();           // ip  -> [timestamps]   (per warm instance, best effort)

function int(v, lo, hi) { const n = parseInt(v, 10); return Number.isFinite(n) && n >= lo && n <= hi ? n : null; }
function money(v) { const n = Number(v); return Number.isFinite(n) ? Math.round(n * 100) / 100 : null; }
function originOk(req) {
  const o = String(req.headers.origin || req.headers.referer || "");
  return !o || /^https:\/\/(www\.)?vshealthbenefits\.com(\/|$)/.test(o) || /^https:\/\/[a-z0-9-]+\.vercel\.app(\/|$)/.test(o) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?(\/|$)/.test(o);
}
function limited(ip) {
  const now = Date.now(), arr = (hits.get(ip) || []).filter(t => now - t < 10 * 60 * 1000);
  arr.push(now); hits.set(ip, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length > 20;
}
async function hs(path, key, init) {
  for (let attempt = 0; attempt < 2; attempt++) {
    const r = await fetch(API + path, Object.assign({}, init, { headers: Object.assign({ "x-api-key": key, "Accept": "application/json" }, (init && init.headers) || {}) }));
    if (r.status === 429 && attempt === 0) {
      const wait = Math.min(2000, (parseFloat(r.headers.get("retry-after")) || 1) * 1000);
      await new Promise(ok => setTimeout(ok, wait + Math.random() * 300));
      continue;
    }
    let body = null; try { body = await r.json(); } catch (e) {}
    return { status: r.status, body };
  }
}
// "Oscar Health Maintenance Organization of Florida, Inc" -> "Oscar"; plan names lose the repeated legal name.
const ISSUERS = [[/oscar/i, "Oscar"], [/unitedhealth|united healthcare/i, "UnitedHealthcare"], [/avmed/i, "AvMed"],
  [/florida blue|blue cross|bcbs|health options/i, "Florida Blue"], [/ambetter|celtic|sunshine|centene/i, "Ambetter"],
  [/aetna|cvs/i, "Aetna CVS Health"], [/cigna/i, "Cigna"], [/molina/i, "Molina"], [/amerihealth/i, "AmeriHealth Caritas"],
  [/community care|22 health/i, "22 Health"], [/simply/i, "Simply Healthcare"], [/wellcare/i, "Wellcare"], [/humana/i, "Humana"]];
function niceIssuer(n) { n = String(n || ""); for (const [re, v] of ISSUERS) if (re.test(n)) return v;
  return n.replace(/,?\s*(Inc\.?|LLC|Company|Corporation|Corp\.?)$/i, "").replace(/\s+of Florida$/i, "").trim(); }
function nicePlan(name, legal) { let s = String(name || ""); if (legal && s.indexOf(legal) === 0) s = s.slice(legal.length).trim(); return s || String(name || ""); }
function slimPlan(p) {
  const pr = p.pricing || {}, d = p.details || {}, doc = p.documents || {}, net = p.network || {};
  const legal = (p.issuer || {}).name || "";
  return {
    id: p.plan_id, name: nicePlan(p.display_name || p.name, legal), issuer: niceIssuer(legal),
    metal: d.metal_level || "", type: d.plan_type || net.type || "", hsa: !!d.hsa_eligible, standardized: !!d.is_standardized,
    csr: d.csr_level || null,
    net: money(pr.net_premium != null ? pr.net_premium : pr.gross_premium), gross: money(pr.gross_premium),
    credit: money(pr.subsidy_applied), max_aptc: money(pr.max_aptc),
    ded: money(d.deductible_individual), ded_fam: money(d.deductible_family),
    moop: money(d.moop_individual), moop_fam: money(d.moop_family),
    pcp: d.primary_care_summary || "", spec: d.specialist_summary || "", urgent: d.urgent_care_summary || "", rx: d.generic_rx_summary || "",
    sbc: doc.sbc_url || "", network_url: doc.network_url || net.network_url || "", formulary: doc.formulary_url || ""
  };
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  const key = (process.env.HEALTHSHERPA_API_KEY || "").trim();
  if (!key) return res.status(503).json({ disabled: true });
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });
  if (!originOk(req)) return res.status(403).json({ error: "forbidden" });
  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (limited(ip)) return res.status(429).json({ error: "Too many requests. Please try again in a few minutes." });

  let b = req.body; if (typeof b === "string") { try { b = JSON.parse(b); } catch (e) { b = {}; } } b = b || {};
  const zip = String(b.zip || "").trim();
  const income = Number(b.income), size = int(b.size, 1, 12), age1 = int(b.age1, 0, 120);
  const age2 = b.age2 === "" || b.age2 == null ? null : int(b.age2, 0, 120), kids = int(b.kids || 0, 0, 8) || 0;
  if (!/^\d{5}$/.test(zip) || !Number.isFinite(income) || income < 0 || income > 10000000 || !size || age1 == null)
    return res.status(400).json({ error: "Missing or invalid quote details." });
  const year = int(process.env.HEALTHSHERPA_PLAN_YEAR || 2027, 2020, 2100);

  try {
    // 1. county (a ZIP can cross county lines; the visitor picks if so)
    let county = null;
    const c = await hs("/reference/counties?zip_code=" + zip, key, { method: "GET" });
    const upErr = x => x && (x.code || x.error || x.message || (x.errors && JSON.stringify(x.errors).slice(0, 200))) || null;
    if (c.status === 404) return res.status(200).json({ plans: [], count: 0, noCounty: true });
    if (c.status !== 200) return res.status(502).json({ error: "county lookup failed", upstream: c.status, code: upErr(c.body) });
    const cb = c.body || {}, raw = cb.counties || (cb.data && (cb.data.counties || cb.data)) || [];
    const counties = (Array.isArray(raw) ? raw : []).map(x => ({ fips: x.fips_code || x.fips, name: x.name || x.county_name, state: x.state }));
    if (!counties.length) return res.status(200).json({ plans: [], count: 0, noCounty: true, shape: Object.keys(cb).slice(0, 6) });
    if (b.fips) county = counties.find(x => x.fips === String(b.fips));
    if (!county && counties.length === 1) county = counties[0];
    if (!county) return res.status(200).json({ needCounty: true, counties });

    // 2. applicants: primary, spouse, children (priced at age 10 unless ages are given)
    const applicants = [{ member_id: "primary", age: age1, relationship: "primary", uses_tobacco: !!b.tobacco1 }];
    if (age2 != null && age2 >= 18) applicants.push({ member_id: "spouse", age: age2, relationship: "spouse", uses_tobacco: !!b.tobacco2 });
    const kidAges = Array.isArray(b.kidAges) ? b.kidAges : [];
    for (let i = 0; i < kids; i++) applicants.push({ member_id: "child-" + (i + 1), age: int(kidAges[i], 0, 25) ?? 10, relationship: "dependent", uses_tobacco: false });

    const body = {
      context: { product: "aca", exchange: "on_exchange", coverage_family: "medical", coverage_type: "medical", plan_year: year },
      location: { zip_code: zip, fips_code: county.fips, state: county.state },
      household: { applicants, household_size: Math.max(size, applicants.length), annual_income: Math.round(income), effective_date: year + "-01-01" },
      page: { number: 1, size: 50 }
    };
    const ck = JSON.stringify(Object.assign({}, body, { page: null }));
    const hit = cache.get(ck);
    if (hit && Date.now() - hit.at < TTL) return res.status(200).json(hit.body);

    // 3. quote
    // HealthSherpa returns at most 50 plans per page, so walk the pages (max 8 = 400 plans).
    let rawPlans = [], seen = new Set();
    for (let pg = 1; pg <= 8; pg++) {
      if (pg > 1) await new Promise(ok => setTimeout(ok, 450));   // stay inside the 1 req/s key limit
      body.page = { number: pg, size: 50 };
      const q = await hs("/quotes", key, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      if (q.status !== 200) {
        if (pg === 1) return res.status(502).json({ error: "quote failed", upstream: q.status, code: upErr(q.body) });
        break;
      }
      const batch = (q.body && q.body.plans) || [], fresh = batch.filter(p => p && !seen.has(p.plan_id));
      fresh.forEach(p => seen.add(p.plan_id)); rawPlans = rawPlans.concat(fresh);
      const total = q.body && q.body.meta && q.body.meta.total_count;
      if (batch.length < 50 || !fresh.length || (total && rawPlans.length >= total)) break;
    }
    const plans = rawPlans.map(slimPlan).filter(p => p.net != null)
      .sort((x, y) => (x.net - y.net) || ((x.ded ?? 1e9) - (y.ded ?? 1e9)));
    const aptc = plans.reduce((m, p) => Math.max(m, p.max_aptc || 0, p.credit || 0), 0);
    const out = { plans, count: plans.length, aptc, county, plan_year: year, source: "HealthSherpa" };
    cache.set(ck, { at: Date.now(), body: out });
    if (cache.size > 300) cache.delete(cache.keys().next().value);
    return res.status(200).json(out);
  } catch (e) {
    return res.status(502).json({ error: "HealthSherpa unavailable" });
  }
};

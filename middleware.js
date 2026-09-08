// Vercel Edge Middleware: the site-wide IP ban.
//
// Runs in front of every HTML page and every /api route. If the visitor's IP is
// on the block list, they get a 404 with a "you have been blocked" page instead
// of the site. Everyone else is passed straight through untouched.
//
// ── Where the list lives ───────────────────────────────────────────────────
// Firestore, vs_state/blocked_ips, in the same { items: [...], ts } shape every
// other portal store uses:
//
//   { ip: "2603:9001:8400:2851::/64", label: "2603:9001:...:83df",
//     reason: "spam", note: "", by: "bradley@…", leadId: "ghl_x", created: 176… }
//
// The admin portal (Blocked IPs tab, and the Block button on a lead card) is the
// only thing that writes it. Nothing here writes - this is read-only.
//
// ── Why IPv6 is stored as a /64 ────────────────────────────────────────────
// A home IPv6 address rotates its last 64 bits (RFC 4941 privacy extensions),
// so banning the exact address a lead submitted from would stop working within
// hours. The stable half is the /64 prefix the ISP hands the household, so that
// is what gets matched. IPv4 is matched exactly. `ipKey()` does the conversion
// and admin.html carries a byte-identical copy, so both ends always agree.
//
// ── Never take the site down ───────────────────────────────────────────────
// Three rules, in order of importance:
//   1. Firestore unreachable, slow, or malformed  ->  fail OPEN. A ban is worth
//      less than the site being up.
//   2. /admin and /client are never blocked, so a mistyped ban can't lock
//      Bradley out of the portal he'd need to undo it with.
//   3. IP_BLOCK_DISABLED=1 in the Vercel env turns the whole thing off without
//      a deploy.
//
// ── Latency ────────────────────────────────────────────────────────────────
// The list is cached in the isolate for 60s and refreshed in the background
// after that, so a warm isolate decides in microseconds with no network call. A
// cold isolate races the fetch against a 1.2s timeout and lets the request
// through if the fetch loses. The matcher below keeps static assets out of here
// entirely - this runs about once per pageview, not once per file.

const FB_API_KEY = process.env.FIREBASE_API_KEY || "AIzaSyCbZ7Otrz6yPlxJuLlDPEoMzssgsWkjo5U";
const FB_PROJECT = process.env.FIREBASE_PROJECT_ID || "vs-benefits-c1da9";
const DOC_URL =
  "https://firestore.googleapis.com/v1/projects/" + FB_PROJECT +
  "/databases/(default)/documents/vs_state/blocked_ips";
const AUTH_URL =
  "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + FB_API_KEY;

const FRESH_MS = 60 * 1000;        // serve from cache without revalidating
const COLD_TIMEOUT_MS = 1200;      // longest a cold isolate will wait on Firestore
const TOKEN_MS = 45 * 60 * 1000;   // anonymous id tokens are good for an hour

// Paths that are never blocked. The portal has to stay reachable to undo a ban,
// and a paying client should not lose their account page over a bad entry.
const EXEMPT = /^\/(admin|client)(\.html)?(\/|$)/i;

// Belt and braces with `config.matcher` below: anything that looks like a static
// file leaves immediately, before any list lookup.
const STATIC = /\.(?:png|jpe?g|gif|svg|webp|avif|ico|css|js|mjs|map|woff2?|ttf|otf|eot|txt|xml|json|webmanifest|pdf|mp4|webm)$/i;

// ── isolate-scoped caches ──────────────────────────────────────────────────
let cache = { keys: null, at: 0, loading: null };
let token = { value: "", exp: 0 };

// ── IP normalisation ───────────────────────────────────────────────────────
// Turns whatever the header says into the key the block list is stored under.
// Keep in step with ipKey() in admin.html.
export function ipKey(raw) {
  let ip = String(raw == null ? "" : raw).trim().toLowerCase();
  if (!ip) return "";

  // "[2603::1]:443" -> "2603::1"
  if (ip.charAt(0) === "[") {
    const close = ip.indexOf("]");
    ip = close > 0 ? ip.slice(1, close) : ip.slice(1);
  }
  const zone = ip.indexOf("%");            // fe80::1%eth0
  if (zone > 0) ip = ip.slice(0, zone);

  // IPv4, with or without a port.
  const v4 = /^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?$/.exec(ip);
  if (v4) return v4[1];

  // ::ffff:1.2.3.4 is an IPv4 address wearing an IPv6 hat.
  const mapped = /^::ffff:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$/.exec(ip);
  if (mapped) return mapped[1];

  if (ip.indexOf(":") < 0) return "";      // not an address we understand

  // IPv6: expand "::", then keep the first four hextets - the /64.
  let parts;
  if (ip.indexOf("::") >= 0) {
    const halves = ip.split("::");
    const head = halves[0] ? halves[0].split(":") : [];
    const tail = halves[1] ? halves[1].split(":") : [];
    const fill = Math.max(0, 8 - head.length - tail.length);
    parts = head.concat(new Array(fill).fill("0"), tail);
  } else {
    parts = ip.split(":");
  }
  parts = parts.slice(0, 4).map(function (h) {
    return (h || "0").replace(/^0+(?=.)/, "");
  });
  while (parts.length < 4) parts.push("0");
  if (!/^[0-9a-f]{1,4}$/.test(parts[0])) return "";
  return parts.join(":") + "::/64";
}

function clientIp(req) {
  const h = req.headers;
  const xff = h.get("x-forwarded-for") || "";
  // Vercel appends the real client IP; the leftmost entry is the client.
  const first = xff.split(",")[0].trim();
  return first || h.get("x-real-ip") || h.get("x-vercel-forwarded-for") || "";
}

// ── the block list ─────────────────────────────────────────────────────────
async function anonToken() {
  if (token.value && Date.now() < token.exp) return token.value;
  const r = await fetch(AUTH_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ returnSecureToken: true }),
  });
  if (!r.ok) return "";
  const j = await r.json();
  if (!j || !j.idToken) return "";
  token = { value: j.idToken, exp: Date.now() + TOKEN_MS };
  return token.value;
}

// Reads the document and returns a Set of match keys. A missing document means
// nothing is banned, which is a perfectly good answer and gets cached.
async function loadKeys() {
  const t = await anonToken();
  if (!t) throw new Error("auth");
  const r = await fetch(DOC_URL, { headers: { Authorization: "Bearer " + t } });
  if (r.status === 404) return new Set();
  if (!r.ok) throw new Error("read_" + r.status);
  const doc = await r.json();
  const values =
    (doc && doc.fields && doc.fields.items && doc.fields.items.arrayValue &&
     doc.fields.items.arrayValue.values) || [];
  const keys = new Set();
  for (const v of values) {
    const f = (v && v.mapValue && v.mapValue.fields) || {};
    // An entry is live unless it has been explicitly unbanned. Unbanning
    // removes the row outright, so this is only a guard against a stale shape.
    if (f.active && f.active.booleanValue === false) continue;
    const raw = (f.ip && f.ip.stringValue) || "";
    // Stored values are already normalised, but run them through ipKey anyway so
    // a hand-typed entry ("2603:9001:8400:2851:cc8c:e95a:293c:83df") still
    // matches the /64 it belongs to.
    const k = raw.indexOf("::/64") > 0 ? raw.toLowerCase() : ipKey(raw);
    if (k) keys.add(k);
  }
  return keys;
}

function refresh() {
  if (cache.loading) return cache.loading;
  cache.loading = loadKeys()
    .then(function (keys) {
      cache = { keys: keys, at: Date.now(), loading: null };
      return keys;
    })
    .catch(function () {
      // Keep whatever we had rather than dropping every ban on one bad read,
      // but move `at` forward so we do not hammer Firestore on every request.
      cache = { keys: cache.keys, at: Date.now(), loading: null };
      return cache.keys;
    });
  return cache.loading;
}

// Returns the current key set, or null when we have nothing and could not get
// anything in time. null means "let them through".
async function blockedKeys(event) {
  const age = Date.now() - cache.at;

  if (cache.keys && age < FRESH_MS) return cache.keys;

  if (cache.keys) {
    // Stale but usable: answer now, refresh behind the response.
    const p = refresh();
    if (event && typeof event.waitUntil === "function") event.waitUntil(p);
    return cache.keys;
  }

  // Cold isolate. Wait, but not for long.
  let timer;
  const timeout = new Promise(function (resolve) {
    timer = setTimeout(function () { resolve(null); }, COLD_TIMEOUT_MS);
  });
  try {
    return await Promise.race([refresh(), timeout]);
  } finally {
    clearTimeout(timer);
  }
}

// ── the page a blocked visitor sees ────────────────────────────────────────
function blockedPage(ip) {
  return `<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>404 — Page not found</title>
<style>
  :root{color-scheme:light}
  *{box-sizing:border-box}
  body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
    padding:24px;background:#f2f5f9;color:#16202e;
    font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
  .card{width:100%;max-width:520px;background:#fff;border:1px solid #e5ebf2;border-radius:16px;
    box-shadow:0 8px 30px rgba(16,32,60,.08);overflow:hidden}
  .bar{background:linear-gradient(135deg,#16447f,#0f2f5c);padding:20px 28px;color:#fff}
  .bar b{font-size:18px;font-weight:800;letter-spacing:-.01em;display:block}
  .bar span{font-size:12px;color:#9fc0ef}
  .body{padding:28px}
  .code{font-size:52px;font-weight:800;line-height:1;letter-spacing:-.03em;color:#16447f;margin:0 0 4px}
  h1{font-size:20px;font-weight:800;margin:0 0 12px}
  p{margin:0 0 12px;color:#41536b}
  .meta{margin-top:20px;padding-top:16px;border-top:1px solid #eef2f7;
    font-size:12px;color:#7c8ba1;word-break:break-all}
  .meta code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#41536b}
</style></head><body>
<div class="card">
  <div class="bar"><b>VS Health Benefits</b><span>Health insurance, made simple</span></div>
  <div class="body">
    <p class="code">404</p>
    <h1>This page is not available to you</h1>
    <p><strong>Your access to this website has been blocked.</strong> Your network address
       was placed on our block list, so pages on vshealthbenefits.com will not load for you.</p>
    <p>If you believe this is a mistake, email
       <a href="mailto:bvilsainthealth@gmail.com" style="color:#16447f">bvilsainthealth@gmail.com</a>
       and include the reference below.</p>
    <div class="meta">Reference: <code>${ip.replace(/[<>&"]/g, "")}</code></div>
  </div>
</div>
</body></html>`;
}

// ── entry point ────────────────────────────────────────────────────────────
export default async function middleware(request, event) {
  if (process.env.IP_BLOCK_DISABLED === "1") return;

  let path = "/";
  try { path = new URL(request.url).pathname; } catch (e) { return; }

  if (EXEMPT.test(path) || STATIC.test(path)) return;

  const raw = clientIp(request);
  const key = ipKey(raw);
  if (!key) return;

  let keys;
  try { keys = await blockedKeys(event); } catch (e) { return; }
  if (!keys || !keys.size || !keys.has(key)) return;

  return new Response(blockedPage(raw), {
    status: 404,
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "no-store, no-cache, must-revalidate",
      "X-Robots-Tag": "noindex, nofollow",
    },
  });
}

// Only HTML pages and API routes reach the middleware. Everything with a file
// extension, and Vercel's own internals, are skipped - so this costs roughly one
// invocation per pageview rather than one per asset.
export const config = {
  matcher: [
    "/((?!_next/|_vercel/|.*\\.(?:png|jpe?g|gif|svg|webp|avif|ico|css|js|mjs|map|woff2?|ttf|otf|eot|xml|json|webmanifest|pdf|mp4|webm)$).*)",
  ],
};

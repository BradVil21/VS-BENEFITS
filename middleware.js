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
// ── Never take the site down, and never trap anyone ────────────────────────
// Four rules, in order of importance:
//   1. Firestore unreachable, slow, or malformed  ->  fail OPEN. A ban is worth
//      less than the site being up.
//   2. A ban is only ever enforced from a RECENTLY CONFIRMED list. If the last
//      successful read is older than MAX_STALE_MS the list is dropped and
//      everyone is let through, because a stale list is how an unblocked
//      visitor stays locked out forever. Enforcement resumes the moment a fresh
//      read succeeds.
//   3. /admin and /client are never blocked, so a mistyped ban can't lock
//      Bradley out of the portal he'd need to undo it with.
//   4. IP_BLOCK_DISABLED=1 in the Vercel env turns the whole thing off without
//      a deploy.
//
// ── Latency ────────────────────────────────────────────────────────────────
// The list is cached in the isolate for 60s and refreshed in the background
// after that, so a warm isolate decides in microseconds with no network call. A
// cold isolate races the fetch against a 1.2s timeout and lets the request
// through if the fetch loses. The matcher below keeps static assets out of here
// entirely - this runs about once per pageview, not once per file.
//
// ── Checking your work ─────────────────────────────────────────────────────
// GET /__blockcheck returns JSON: the address the edge sees you as, the key it
// matches on, whether you are currently blocked, and how old its copy of the
// list is. Never blocked, never cached. Use it to confirm an unblock landed
// instead of guessing from a page that might be sitting in a browser cache.

const FB_API_KEY = process.env.FIREBASE_API_KEY || "AIzaSyCbZ7Otrz6yPlxJuLlDPEoMzssgsWkjo5U";
const FB_PROJECT = process.env.FIREBASE_PROJECT_ID || "vs-benefits-c1da9";
const DOC_URL =
  "https://firestore.googleapis.com/v1/projects/" + FB_PROJECT +
  "/databases/(default)/documents/vs_state/blocked_ips";
const AUTH_URL =
  "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + FB_API_KEY;

const FRESH_MS = 60 * 1000;        // serve from cache without revalidating
const MAX_STALE_MS = 5 * 60 * 1000; // hard limit on how old an enforced list may be
const RETRY_MS = 5 * 1000;         // after a failed read, wait this long before retrying
const COLD_TIMEOUT_MS = 1200;      // longest a cold isolate will wait on Firestore
const TOKEN_MS = 40 * 60 * 1000;   // anonymous id tokens are good for an hour

// The block-status probe. Exempt from blocking and from caching.
const CHECK_PATH = /^\/__blockcheck\/?$/i;

// Paths that are never blocked. The portal has to stay reachable to undo a ban,
// and a paying client should not lose their account page over a bad entry.
const EXEMPT = /^\/(admin|client)(\.html)?(\/|$)/i;

// Belt and braces with `config.matcher` below: anything that looks like a static
// file leaves immediately, before any list lookup.
const STATIC = /\.(?:png|jpe?g|gif|svg|webp|avif|ico|css|js|mjs|map|woff2?|ttf|otf|eot|txt|xml|json|webmanifest|pdf|mp4|webm)$/i;

// ── isolate-scoped caches ──────────────────────────────────────────────────
// `at`   - when the list was last read SUCCESSFULLY. Never moved by a failure,
//          because that is what makes rule 2 above work.
// `tried`- when a read was last attempted, successfully or not. Only used to
//          keep a broken Firestore from being hammered once per request.
let cache = { keys: null, at: 0, tried: 0, loading: null };
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
  if (!r.ok) { token = { value: "", exp: 0 }; return ""; }
  const j = await r.json();
  if (!j || !j.idToken) { token = { value: "", exp: 0 }; return ""; }
  token = { value: j.idToken, exp: Date.now() + TOKEN_MS };
  return token.value;
}

// Reads the document and returns a Set of match keys. A missing document means
// nothing is banned, which is a perfectly good answer and gets cached.
async function loadKeys() {
  let t = await anonToken();
  if (!t) throw new Error("auth");
  let r = await fetch(DOC_URL, { headers: { Authorization: "Bearer " + t } });
  // A cached token that Firebase has since rejected looks exactly like a
  // permanent outage from here, and a permanent outage is what used to freeze
  // the list. Throw the token away and try once more with a fresh one.
  if (r.status === 401 || r.status === 403) {
    token = { value: "", exp: 0 };
    t = await anonToken();
    if (!t) throw new Error("auth");
    r = await fetch(DOC_URL, { headers: { Authorization: "Bearer " + t } });
  }
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
  cache.tried = Date.now();
  cache.loading = loadKeys()
    .then(function (keys) {
      // A good read is the only thing that moves `at`.
      cache = { keys: keys, at: Date.now(), tried: Date.now(), loading: null };
      return keys;
    })
    .catch(function () {
      // Keep whatever we had so one bad read does not drop every ban, but leave
      // `at` where it was: the list now has an expiry, and letting a failure
      // renew it is exactly the bug that kept unblocked visitors on the 404.
      cache = { keys: cache.keys, at: cache.at, tried: Date.now(), loading: null };
      return null;
    });
  return cache.loading;
}

// Start a refresh unless one is already running or one just failed. Returns a
// promise (possibly already settled) suitable for event.waitUntil.
function maybeRefresh() {
  if (cache.loading) return cache.loading;
  if (cache.tried && Date.now() - cache.tried < RETRY_MS && !cache.at) {
    return Promise.resolve(null);
  }
  return refresh();
}

// Returns the current key set, or null when we have nothing recent enough to
// act on. null means "let them through".
async function blockedKeys(event) {
  const age = Date.now() - cache.at;

  // Fresh: answer straight from memory.
  if (cache.keys && age < FRESH_MS) return cache.keys;

  // Usable but stale: answer now, refresh behind the response. Past
  // MAX_STALE_MS it stops being usable at all - see rule 2 at the top.
  if (cache.keys && age < MAX_STALE_MS) {
    const p = maybeRefresh();
    if (event && typeof event.waitUntil === "function") event.waitUntil(p);
    return cache.keys;
  }

  // Nothing we are willing to enforce. Try to get a real answer, briefly, and
  // let the visitor through if it does not arrive.
  let timer;
  const timeout = new Promise(function (resolve) {
    timer = setTimeout(function () { resolve(null); }, COLD_TIMEOUT_MS);
  });
  try {
    const keys = await Promise.race([maybeRefresh(), timeout]);
    if (keys) return keys;
    // The race may have been lost by a refresh that has since landed.
    return (cache.keys && Date.now() - cache.at < MAX_STALE_MS) ? cache.keys : null;
  } catch (e) {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

// Headers that stop the 404 being remembered by anything between us and the
// visitor. Without these an unblock can look like it did not work simply
// because a browser or an edge cache is still handing out yesterday's answer.
const NO_STORE = {
  "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
  "CDN-Cache-Control": "no-store",
  "Vercel-CDN-Cache-Control": "no-store",
  Pragma: "no-cache",
  Expires: "0",
  Vary: "*",
};

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
       <a href="mailto:info@vshealthbenefits.com" style="color:#16447f">info@vshealthbenefits.com</a>
       and include the reference below.</p>
    <div class="meta">Reference: <code>${ip.replace(/[<>&"]/g, "")}</code></div>
  </div>
</div>
</body></html>`;
}

// ── entry point ────────────────────────────────────────────────────────────
export default async function middleware(request, event) {
  const disabled = process.env.IP_BLOCK_DISABLED === "1";

  let path = "/";
  try { path = new URL(request.url).pathname; } catch (e) { return; }

  // The probe answers before anything else, so it works even while blocked.
  if (CHECK_PATH.test(path)) {
    const raw = clientIp(request);
    const key = ipKey(raw);
    let keys = null;
    if (!disabled && key) { try { keys = await blockedKeys(event); } catch (e) { keys = null; } }
    const age = cache.at ? Date.now() - cache.at : null;
    const body = {
      ip: raw,
      key: key,
      blocked: !!(keys && key && keys.has(key)),
      enforcing: !disabled && !!keys,
      listSize: keys ? keys.size : null,
      listAgeSeconds: age === null ? null : Math.round(age / 1000),
      disabled: disabled,
      checkedAt: new Date().toISOString(),
    };
    return new Response(JSON.stringify(body, null, 2), {
      status: 200,
      headers: Object.assign({ "Content-Type": "application/json; charset=utf-8",
                               "X-Robots-Tag": "noindex, nofollow" }, NO_STORE),
    });
  }

  if (disabled) return;
  if (EXEMPT.test(path) || STATIC.test(path)) return;

  const raw = clientIp(request);
  const key = ipKey(raw);
  if (!key) return;

  let keys;
  try { keys = await blockedKeys(event); } catch (e) { return; }
  if (!keys || !keys.size || !keys.has(key)) return;

  return new Response(blockedPage(raw), {
    status: 404,
    headers: Object.assign({ "Content-Type": "text/html; charset=utf-8",
                             "X-Robots-Tag": "noindex, nofollow" }, NO_STORE),
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

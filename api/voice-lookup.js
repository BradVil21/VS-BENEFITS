// Vercel serverless function: does this caller exist in the admin portal?
//
// Called by the GHL Voice AI agent ("Amanda") when a caller says they're already
// a member. The agent collects first name, last name and date of birth, posts
// them here, and gets back a yes/no. On "no" the agent apologises and transfers
// to Bradley's cell.
//
// ---------------------------------------------------------------------------
// WHY THIS ENDPOINT REQUIRES A SECRET
//
// This answers "is <name>, born <date>, a client of a health insurance
// brokerage?" That is health-adjacent personal information about real people,
// and an open endpoint would let anyone confirm it by guessing a name and DOB.
//
// So VOICE_AGENT_SECRET is REQUIRED. If it is not set the endpoint refuses every
// request rather than falling back to open. That is deliberate: a broken phone
// agent is a bad afternoon, an enumerable client list is a different kind of
// problem. Every other endpoint in this repo fails open so the website never
// breaks; this one is the exception, on purpose.
//
// It also returns the minimum that answers the question - found true/false and
// the member's first name so the agent can greet them. Never the email, phone,
// plan, or anything else on the record.
// ---------------------------------------------------------------------------
//
// ENV VARS:
//   VOICE_AGENT_SECRET   REQUIRED. Shared secret; caller sends it in the
//                        `x-vs-voice-secret` header. Generate something long
//                        and random. No fallback on purpose.
//   FIREBASE_API_KEY     optional; defaults to the public web key (same as admin.html)
//   FIREBASE_PROJECT_ID  optional

const FB_API_KEY = process.env.FIREBASE_API_KEY || "AIzaSyCbZ7Otrz6yPlxJuLlDPEoMzssgsWkjo5U";
const FB_PROJECT = process.env.FIREBASE_PROJECT_ID || "vs-benefits-c1da9";
const FS_ACCOUNTS =
  "https://firestore.googleapis.com/v1/projects/" + FB_PROJECT +
  "/databases/(default)/documents/vs_state/accounts";

function clean(v, max) {
  return String(v == null ? "" : v).trim().slice(0, max || 120);
}

// Fold accents, drop punctuation, collapse spaces, lowercase. So "José",
// "Jose" and "  JOSE " all compare equal, and O'Brien matches OBrien.
function normName(v) {
  return String(v == null ? "" : v)
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z\s-]/g, "")
    .replace(/[-\s]+/g, " ")
    .trim();
}

// Accepts MM/DD/YYYY, M-D-YYYY, MMDDYYYY, YYYY-MM-DD. Returns YYYY-MM-DD or "".
// Two-digit years are rejected rather than guessed - "58" could be 1958 or 2058,
// and on a DOB check a wrong guess means failing to find a real member.
function normDob(v) {
  const s = clean(v, 32);
  if (!s) return "";
  let m;

  m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(s);
  if (m) return iso(m[1], m[2], m[3]);

  m = /^(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{4})$/.exec(s);
  if (m) return iso(m[3], m[1], m[2]);

  const digits = s.replace(/\D/g, "");
  if (digits.length === 8) {
    // Ambiguous only between MMDDYYYY and YYYYMMDD; a leading 19xx/20xx is the tell.
    const head = Number(digits.slice(0, 4));
    if (head >= 1900 && head <= 2100) return iso(digits.slice(0, 4), digits.slice(4, 6), digits.slice(6, 8));
    return iso(digits.slice(4, 8), digits.slice(0, 2), digits.slice(2, 4));
  }
  return "";
}

function iso(y, mo, d) {
  const Y = Number(y), M = Number(mo), D = Number(d);
  if (!(Y >= 1900 && Y <= 2100)) return "";
  if (!(M >= 1 && M <= 12)) return "";
  if (!(D >= 1 && D <= 31)) return "";
  return String(Y) + "-" + String(M).padStart(2, "0") + "-" + String(D).padStart(2, "0");
}

function fsDecode(v) {
  if (!v || typeof v !== "object") return null;
  if ("nullValue" in v) return null;
  if ("booleanValue" in v) return v.booleanValue;
  if ("integerValue" in v) return Number(v.integerValue);
  if ("doubleValue" in v) return Number(v.doubleValue);
  if ("stringValue" in v) return v.stringValue;
  if ("timestampValue" in v) return v.timestampValue;
  if ("arrayValue" in v) return (v.arrayValue.values || []).map(fsDecode);
  if ("mapValue" in v) {
    const out = {};
    const f = v.mapValue.fields || {};
    Object.keys(f).forEach(function (k) { out[k] = fsDecode(f[k]); });
    return out;
  }
  return null;
}

async function fsToken() {
  try {
    const r = await fetch(
      "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + FB_API_KEY,
      { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ returnSecureToken: true }) }
    );
    if (!r.ok) return null;
    const j = await r.json();
    return j.idToken || null;
  } catch (e) { return null; }
}

async function readAccounts() {
  const token = await fsToken();
  if (!token) return null;
  const r = await fetch(FS_ACCOUNTS, { headers: { Authorization: "Bearer " + token } });
  if (r.status === 404) return [];
  if (!r.ok) return null;
  const doc = await r.json();
  const cur = doc && doc.fields && doc.fields.items;
  return cur ? (fsDecode(cur) || []) : [];
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  // ---- auth: required, no fallback ----
  const expected = process.env.VOICE_AGENT_SECRET;
  if (!expected) {
    res.status(503).json({ error: "Lookup disabled: VOICE_AGENT_SECRET is not configured." });
    return;
  }
  const got = String((req.headers && req.headers["x-vs-voice-secret"]) || "");
  if (got !== expected) { res.status(401).json({ error: "Unauthorized" }); return; }

  let d = req.body;
  if (typeof d === "string") { try { d = JSON.parse(d); } catch (e) { d = {}; } }
  d = d || {};

  const first = normName(d.firstName || d.first_name);
  const last  = normName(d.lastName  || d.last_name);
  const dob   = normDob(d.dob || d.dateOfBirth || d.date_of_birth);

  // All three are required. Name alone would let someone confirm membership by
  // guessing common names; the DOB is what makes this a verification.
  if (!first || !last || !dob) {
    res.status(200).json({ found: false, reason: "incomplete_details" });
    return;
  }

  let accounts;
  try { accounts = await readAccounts(); }
  catch (e) { accounts = null; }

  // A read failure must NOT be reported as "not a member" - that would send a
  // real member to voicemail-land. Say so, and let the agent transfer anyway.
  if (accounts === null) {
    res.status(200).json({ found: false, reason: "lookup_unavailable" });
    return;
  }

  const hit = accounts.filter(function (a) {
    if (!a) return false;
    return normName(a.firstName) === first &&
           normName(a.lastName) === last &&
           normDob(a.dob) === dob;
  })[0];

  if (!hit) { res.status(200).json({ found: false, reason: "no_match" }); return; }

  // Deliberately minimal. Enough to greet them by name and pull the record up
  // by id in the portal - nothing that would be worth harvesting.
  res.status(200).json({
    found: true,
    firstName: clean(hit.firstName, 60),
    memberId: clean(hit.id, 60),
    status: clean(hit.status || "active", 20),
  });
};

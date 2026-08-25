// Shared Firestore (REST) helpers for the VS admin portal.
//
// The admin portal (admin.html) keeps its data in Firestore under the
// collection `vs_state`, one document per store:
//
//   vs_state/leads        individual & family pipeline  (Pipeline tab)
//   vs_state/biz_leads    business pipeline             (Business Leads tab)
//   vs_state/accounts     client accounts
//   ...
//
// Each document is { items: [ ...records... ], ts: <millis> } and admin.html
// mirrors it into localStorage through onSnapshot, so anything appended here
// shows up on the board live, without a refresh.
//
// This file exists because webchat-lead.js, voice-lead.js and support-ticket.js
// had each grown their own copy of the same encode/decode/append code, and the
// copies had already drifted apart. New writers (ghl-inbound.js) use this one.
//
// Concurrency: appends are read-modify-write, which is a race when two leads
// land in the same instant. That is now guarded with Firestore's
// `currentDocument.updateTime` precondition and a retry, so a losing write
// re-reads and re-appends instead of silently overwriting the other lead.
//
// ENV VARS:
//   FIREBASE_API_KEY      optional; defaults to the public web key (it is
//                         already in admin.html - access is governed by
//                         Firestore rules, not by keeping the key secret).
//   FIREBASE_PROJECT_ID   optional; defaults to the VS project.

const FB_API_KEY = process.env.FIREBASE_API_KEY || "AIzaSyCbZ7Otrz6yPlxJuLlDPEoMzssgsWkjo5U";
const FB_PROJECT = process.env.FIREBASE_PROJECT_ID || "vs-benefits-c1da9";
const DOC_BASE =
  "https://firestore.googleapis.com/v1/projects/" + FB_PROJECT +
  "/databases/(default)/documents/vs_state/";

// ---------- value encoding ----------
function fsEncode(v) {
  if (v === null || v === undefined) return { nullValue: null };
  if (typeof v === "boolean") return { booleanValue: v };
  if (typeof v === "number") {
    return Number.isInteger(v) ? { integerValue: String(v) } : { doubleValue: v };
  }
  if (Array.isArray(v)) return { arrayValue: { values: v.map(fsEncode) } };
  if (typeof v === "object") {
    const fields = {};
    Object.keys(v).forEach(function (k) { fields[k] = fsEncode(v[k]); });
    return { mapValue: { fields: fields } };
  }
  return { stringValue: String(v) };
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

// ---------- auth ----------
// Anonymous sign-in, exactly as admin.html does in the browser. Tokens are good
// for an hour; a warm serverless instance reuses one rather than minting a new
// anonymous user on every request.
let _tok = { value: null, exp: 0 };

async function fsToken() {
  if (_tok.value && Date.now() < _tok.exp) return _tok.value;
  try {
    const r = await fetch(
      "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=" + FB_API_KEY,
      { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ returnSecureToken: true }) }
    );
    if (!r.ok) return null;
    const j = await r.json();
    if (!j || !j.idToken) return null;
    _tok = { value: j.idToken, exp: Date.now() + 50 * 60 * 1000 };
    return _tok.value;
  } catch (e) {
    return null;
  }
}

// ---------- read ----------
// Returns { ok, items, updateTime, exists }. A missing document is not an
// error - it just means the store is empty and the first write creates it.
async function readStore(key, token) {
  const t = token || (await fsToken());
  if (!t) return { ok: false, reason: "auth_failed", items: [], exists: false };
  const r = await fetch(DOC_BASE + encodeURIComponent(key), {
    headers: { Authorization: "Bearer " + t },
  });
  if (r.status === 404) return { ok: true, items: [], exists: false, updateTime: null };
  if (!r.ok) return { ok: false, reason: "read_failed_" + r.status, items: [], exists: false };
  const doc = await r.json();
  const cur = doc && doc.fields && doc.fields.items;
  return {
    ok: true,
    exists: true,
    items: cur ? (fsDecode(cur) || []) : [],
    updateTime: (doc && doc.updateTime) || null,
  };
}

// ---------- write ----------
async function writeStore(key, items, token, updateTime, exists) {
  const t = token || (await fsToken());
  if (!t) return { ok: false, reason: "auth_failed" };
  const params = [
    "updateMask.fieldPaths=items",
    "updateMask.fieldPaths=ts",
  ];
  // Optimistic concurrency: only commit if nobody else wrote since our read.
  if (exists && updateTime) params.push("currentDocument.updateTime=" + encodeURIComponent(updateTime));
  else if (!exists) params.push("currentDocument.exists=false");

  const r = await fetch(DOC_BASE + encodeURIComponent(key) + "?" + params.join("&"), {
    method: "PATCH",
    headers: { Authorization: "Bearer " + t, "Content-Type": "application/json" },
    body: JSON.stringify({
      fields: { items: fsEncode(items), ts: { integerValue: String(Date.now()) } },
    }),
  });
  if (r.ok) return { ok: true };
  // 400 / 409 here means the precondition failed - somebody else wrote first.
  return { ok: false, status: r.status, conflict: r.status === 400 || r.status === 409 };
}

// ---------- append with merge ----------
// Appends `record` to the store named `key`.
//
// `matcher(existing)` decides whether a record already in the store is the same
// person. When it matches, `onMatch(existing, record)` is given the chance to
// merge instead of creating a duplicate card. Return true from onMatch to save
// the merged item, or false to leave the store untouched.
//
// Returns { ok, action: "created"|"merged"|"unchanged", total, id }.
async function appendRecord(key, record, matcher, onMatch) {
  const token = await fsToken();
  if (!token) return { ok: false, reason: "auth_failed" };

  for (let attempt = 0; attempt < 4; attempt++) {
    const read = await readStore(key, token);
    if (!read.ok) return { ok: false, reason: read.reason };

    const items = read.items.slice();
    let action = "created";

    let hitIndex = -1;
    if (typeof matcher === "function") {
      for (let i = 0; i < items.length; i++) {
        if (items[i] && matcher(items[i])) { hitIndex = i; break; }
      }
    }

    if (hitIndex >= 0) {
      const merged = typeof onMatch === "function" ? onMatch(items[hitIndex], record) : false;
      if (!merged) return { ok: true, action: "unchanged", total: items.length, id: items[hitIndex].id };
      action = "merged";
    } else {
      items.unshift(record);
    }

    const w = await writeStore(key, items, token, read.updateTime, read.exists);
    if (w.ok) {
      return {
        ok: true,
        action: action,
        total: items.length,
        id: hitIndex >= 0 ? items[hitIndex].id : record.id,
      };
    }
    if (!w.conflict) return { ok: false, reason: "write_failed_" + (w.status || 0) };
    // Conflict: somebody else appended between our read and write. Loop and
    // rebuild on top of their version rather than clobbering it.
    await new Promise(function (r) { setTimeout(r, 120 * (attempt + 1)); });
  }
  return { ok: false, reason: "write_conflict_retries_exhausted" };
}

module.exports = { fsEncode, fsDecode, fsToken, readStore, writeStore, appendRecord, DOC_BASE };

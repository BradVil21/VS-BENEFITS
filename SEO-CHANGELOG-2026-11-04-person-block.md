# 2026-11-04 — "Block this person" (ban follows the person, not just the IP)

## Why
A visitor blocked on 12.247.0.158 still got a dummy quote in. Two gaps:
1. The edge block (middleware.js) fails OPEN on purpose when it can't read the
   block list within 1.2s, and the lead APIs never checked the list themselves.
2. An IP ban is dodged by a VPN, phone data, or a new network.

## What changed
- **api/_lib.js** `guardBanned()` — every public lead endpoint (lead-draft,
  lead-sync, business-quote, census, webchat-lead[email/phone only]) checks the
  block list server-side before saving anything. Match on IP, learned IPs,
  device id, ban cookie, email, or phone. A banned submission gets a silent
  `200 {ok:true}` (they learn nothing), is never saved, and the browser gets a
  `vs_blk` cookie. Any new IP/email/phone/device they use is added to their row.
- **vs-attribution.js** — sets a random first-party device id (`vs_vid` cookie +
  localStorage backup) on every page and attaches it to every lead.
- **middleware.js** — the 404 now also triggers on the `vs_vid` device id, the
  `vs_blk` cookie, and learned IPs, and it hands blocked browsers the `vs_blk`
  cookie so a VPN doesn't get them back in. `/__blockcheck` reports `blockedBy`.
- **admin.html** — lead card button is now **Block this person**: blocks IP +
  device + every email/phone from all leads on that IP (never our own
  number/email). Existing IP-only blocks show **Block this person everywhere**
  to upgrade. Blocked IPs tab shows what each block covers and new addresses
  they've been followed to; the manual box also accepts an email or phone.
  Unblock deletes the row, which lifts every part of it at once.

## Kill switches (Vercel env, no deploy)
`BAN_CHECK_DISABLED=1` (API check) · `IP_BLOCK_DISABLED=1` (edge) — unchanged.

## Limits
Someone using a private/incognito window AND a VPN AND a brand-new email and
phone looks like a new visitor; nothing on a public website can fully stop that.

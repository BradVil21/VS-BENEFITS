# VS Benefits - Admin & Client Portal Guide

This file covers the two private dashboards bundled with the site:

- **`admin.html`** - your private command center (leads, members, accounts, support inbox, referrals, calendar)
- **`client.html`** - the member-facing portal (your clients sign in here to view their plan, message you, and refer family)

The home page now has a **Log In** button in the nav and a **Members** section that points clients to `client.html`. Nothing public links to `admin.html` - it's bookmark-only and tagged `noindex,nofollow` so search engines ignore it.

Both portals are **mobile-first**: usable on a phone in the field, and progressively wider on tablet and desktop.

---

## Quick start

1. Open `admin.html` in a browser, set your admin password (one time per device).
2. Go to the **Members** tab and click **+ Add member** for each current client. Each gets a 6-digit verification code + a copy/share invite link.
3. Send the invite link (text or email) to the client. They click it, set a password, and they're in `client.html`.
4. Manage everything from there: see who's registered (Accounts tab), reply to messages (Support tab), and track referrals + payouts (Referrals tab).

---

## Open the portals

- Admin: **`https://vshealthbenefits.com/admin.html`** - bookmark this.
- Client: **`https://vshealthbenefits.com/client.html`** - send to clients via the invite link, or they can reach it from the home page nav.

---

## First-time admin setup

1. Open `admin.html`. You'll see **"Create your admin password"**.
2. Choose 8+ characters. SHA-256 hashed, stored only in your browser (never sent anywhere).
3. **No password reset.** If you forget it, the "Reset & start over" link wipes the password and all admin data on that device. Back up regularly.
4. Each device is independent. Use **Settings -> Backup / Restore** to copy data between phone and laptop.
5. Session lasts until you close the tab.

---

## Leads tab

- **+ Add lead** - name, company, phone, email, **address**, coverage, status, next step, notes.
- **Search** filters across name, company, email, phone, address, notes.
- **Filter by status** - New / Contacted / Quoted / Closed won / Closed lost.
- **Export CSV / Import CSV** - one-click backup, or import from a CSV with headers (`name`, `company`, `phone`, `email`, `address`, `coverage`, `status`, `next`, `notes`).

### Auto-capture from your Make.com webhook

Public forms POST to `window.MAKE_WEBHOOK_URL` (set in Settings tab). To pipe submissions into Leads, the simplest path is still: have Make append to a Google Sheet, then weekly do **Import CSV**. For real-time, you'd need a small backend - ping me when you want it.

---

## Members tab

This is the master list of your **enrolled VS Benefits clients**. The portal restricts client account creation to people on this list.

- **+ Add member** - name, email, phone, address, enrollment date, coverage type, plan, status, notes.
- Each new member gets:
  - A **6-digit verification code** (used once during signup).
  - A **shareable invite link** that pre-fills their email + code on the signup screen.
- **Invite** - opens the invite modal with copy buttons for the code and the URL.
- **New code** - regenerates the verification code if the client lost the old one. The previous code stops working immediately.
- **Edit** - update any of their info.
- **Delete** - removes the member. If they had a portal account, the account is left orphaned (use Accounts tab to revoke).

Status badges in the right-hand column tell you whether each member has registered an account, used their code, or is still pending.

---

## Accounts tab (NEW)

Shows every client who has registered a Client Portal account.

- **Name / Email / Phone** - pulled from the matching Member record.
- **Registered** - when the client first set up their account.
- **Last sign-in** - relative timestamp, refreshed each time they log in.
- **Status** - active / paused / churned (mirrors the Member record).

Per-row actions:

- **Message** - jumps you straight to the Support tab with that conversation pre-loaded so you can type a reply.
- **Reset password** - clears the client's password AND issues a fresh 6-digit code. Use this when a client forgets their password. Tell them to use the new code on the Sign Up tab to re-register.
- **Revoke** - removes the account entirely. The Member record stays put; they can no longer sign in until you regenerate their code from the Members tab.

**Export CSV** dumps name, email, phone, registered date, last sign-in.

---

## Support tab

- Left column: list of conversations (newest activity first, unread badge if the client has messaged).
- Right column: the thread for whoever you've selected, plus a reply box.
- Replies are saved locally and (if a webhook is configured in Settings) forwarded to Make.com so you can fan them out via SMS or email.
- **Mark all read** clears unread badges in bulk.

---

## Referrals tab

Prospects your clients have submitted from the Refer tab in their portal.

Each row shows: who referred them, the prospect's contact info, relationship, notes, status, **payout amount**, and time submitted.

**Editing on the fly:**

- **Status** dropdown: New / Contacted / Enrolled / Lost.
- **Payout** numeric field: enter the dollar amount you owe the referring client (e.g., $25, $50). Updates instantly. Webhook fires on change.
- **Paid** checkbox: tick when you've sent the reward. Stamps the date and includes the row in your "Paid" totals.
- **Move to Leads** - copies the prospect into your Leads tab so you can work them like any other lead.
- **Delete** - remove the referral.

**Top of tab** shows running totals for **Owed** vs **Paid** so you always know what you owe your clients. **Export CSV** includes payout amounts and paid status.

---

## Calendar tab

Monthly grid of your events. Local-only by default; optionally two-way with Google Calendar.

- **+ Add event** or click any day. Title, start/end, location/link, notes.
- Click a colored pill to edit (blue = local, teal = Google).
- "Upcoming (next 14 days)" list below the calendar shows everything in chronological order.

### Connect Google Calendar (optional)

You need your own OAuth Client ID (one-time, free).

1. **Google Cloud project** - [console.cloud.google.com](https://console.cloud.google.com) -> New Project ("VS Benefits Admin").
2. **APIs & Services -> Library** -> Enable **Google Calendar API**.
3. **OAuth consent screen** - External user type. Fill in App name, your email. Add scopes `../auth/calendar.events` and `../auth/userinfo.email`. Add yourself under Test users. Leave in "Testing" mode.
4. **Credentials -> + Create Credentials -> OAuth client ID** - Web application. Authorized JavaScript origins: `https://vshealthbenefits.com` (and `http://localhost` for local testing - no `file://`).
5. Copy the Client ID, paste into **admin.html -> Settings -> Google Client ID -> Save**.
6. **Calendar tab -> Connect Google Calendar** -> sign in -> grant permissions.

Local events created with the **"Also create on Google Calendar"** box ticked get pushed to your primary calendar. Editing existing Google events is intentionally read-only here - edit those on Google Calendar directly.

---

## Settings tab

- **Change password** (current required).
- **Webhook URL** - Make.com endpoint that receives lead submissions, support messages, referrals, payout updates, sign-ins.
- **Google OAuth Client ID**.
- **Backup all data** - JSON download with leads, members, **accounts**, messages, referrals, events, and the webhook/Client ID. Password hash and Google token are NOT exported (for safety). **Save these weekly.**
- **Restore from backup** - merges with current data. Useful for moving to a new device.
- **Wipe all admin data** - nuclear option for this device.

---

## Client Portal (`client.html`)

Mobile-first dashboard your clients use after they register.

### Sign-up flow

1. Client opens `client.html` (from the home page Members section, the Login modal, or the invite link you sent them).
2. Clicks the **Sign Up** tab.
3. Enters their email, the 6-digit code, and picks a password.
4. The portal verifies they exist as a Member with that exact code (and the code hasn't been used). If anything fails, they get a clear error and can't proceed.
5. Account is created, logged in, and the dashboard loads.

The verification keeps random visitors out - only people **you've explicitly added** to the Members tab can register.

### Invite link

When you click "Invite" on a member, the modal gives you a long URL like `client.html?invite=eyJuI...`. Sending that link prefills the signup form and seeds the member record on the client's device, so cross-device signup works even if they've never opened the site before.

### Dashboard tabs (all mobile-first)

- **Profile** - read-only view of the member info you entered: name, email, phone, address, enrollment date, coverage type, plan, status.
- **Support** - chat-style thread with you. Their messages appear in your admin Support inbox; your replies show up here.
- **Refer** - form to refer family or coworkers (name, relationship, phone, email, coverage interest, notes). Submissions land in your admin Referrals tab.

### Webhook events the client portal fires

If a webhook URL is configured in admin Settings, the client portal forwards (best-effort, no-cors) on:

- `client_account_created` - when a member registers.
- `client_sign_in` - on each successful login.
- `support_message` - when the client posts a support message.
- `client_referral` - when the client submits a referral.

The admin portal also forwards: `admin_reply`, `referral_payout_updated`, `referral_paid_status`, `client_password_reset`, `client_account_revoked`.

---

## Login modal (home page)

The home page nav has a **Log In** button (also in the footer's Members column). It opens a modal with two clearly-labeled options:

- **Client Portal** -> `client.html` (for members).
- **Admin Portal** -> `admin.html` (for you / your team).

This way, anyone arriving at the homepage sees the right entry point without exposing the admin URL to crawlers.

---

## Security notes

This is a **single-device, browser-storage** system. On purpose - the public site is fully static (no server, no database).

- All data lives in `localStorage`. Clear browser data and it's gone. **Back up weekly.**
- Admin password hash never leaves the browser. Same for client passwords.
- The 6-digit codes + Members allow-list keep the client portal from being abused, but anyone with admin access can issue codes - so guard your admin password.
- For real multi-device sync (your phone + laptop, or several team members), you'd want a real backend. Ping me when you want it - I'll wire up serverless + Firestore or Supabase.

---

## Mobile usage

Both portals are usable on a phone:

- Tap targets are 44px+.
- Tables scroll horizontally where they don't fit.
- The admin tabs wrap; the dashboard collapses to a single column.
- Client portal: profile / support / refer all single-column on phone.

The home page Login modal is full-screen-ish on phones and tappable.

---

## Troubleshooting

**"A client says signup says 'no member record for that email'"**
You haven't added them to the Members tab on the device they're trying to register from. Add them, then send them the invite link (which carries the member info to their device).

**"A client lost their password"**
Accounts tab -> find them -> **Reset password**. Then go to Members tab, copy the new 6-digit code, and send to them. They use the Sign Up tab to re-register.

**"Two devices, two sets of data"**
Expected - this is browser-local. Admin Settings -> Backup all data, transfer the JSON, Restore on the other device. Or move to a real backend.

**"My referrals payout totals look wrong"**
The "Owed" total adds up unpaid referrals; "Paid" totals the paid ones. If a payout reads $0, that referral hasn't been priced yet. Type a number into the payout field on that row.

**"Google sign-in says 'Access blocked'"**
You're either on `file://` (not allowed) or your URL isn't in Authorized JavaScript origins. Run a local server (`python3 -m http.server 8080`) or add the exact domain.

---

## Roadmap (ask if you want any)

- Real backend so phone + laptop stay in sync in real time.
- Send the client an actual SMS / email when you reply (via your Make.com webhook).
- Per-lead reminders tied to calendar events.
- Pipeline / Kanban view for leads.
- Click-to-call logging.
- Bulk-import members from a CSV (right now they're added one-by-one).
- Member dashboard: documents (insurance cards, EOBs) the client can download.

Tell me which would actually save you time and I'll build it.

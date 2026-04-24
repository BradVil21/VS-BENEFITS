# VS Benefits Portal — Admin & Member Setup Guide

This document explains how the **admin portal** (`admin.html`) and **member portal** (`client.html`) work, and how to manage them as the practice owner.

---

## 1. The two portals

| Page | Who it's for | URL |
|---|---|---|
| `admin.html` | You (Bradley), the advisor | `vshealthbenefits.com/admin.html` |
| `client.html` | Your members / clients | `vshealthbenefits.com/client.html` |
| `index.html` | Public marketing page with a Login modal that links to both | `vshealthbenefits.com/` |

Both portals share the same browser-side data (`localStorage`), so when both pages are open in the same browser they stay in sync. There is no server — everything lives in the browser. This keeps the site fast, free, and private to your machine. (For a true multi-device system you'd later wire it to a backend; the localStorage layer is designed so that's a clean swap.)

---

## 2. First-time admin setup

The first time you open `admin.html`, you'll see a **Setup** screen. To create the admin account you'll be asked for:

1. **Admin setup code** — this is the secret gate that prevents anyone other than you from creating an admin login.
2. **Your password** (and confirm) — this becomes your admin login password.

The setup code is intentionally **not visible anywhere on the page**. It's stored in source code as a base64-encoded value (`atob("MDYwNQ==")` decodes to `0605`). This is light obfuscation — appropriate for a static site — and good enough that someone glancing at the page source won't see "0605" in plain text.

> **The default admin setup code is `0605`.**
> Don't share this code with anyone. Treat it like a master key.

After you complete setup, the setup screen disappears and a **Sign in** screen takes its place. From then on you log in with just your password.

---

## 3. Changing the admin setup code

You can rotate the setup code at any time:

1. Sign in to `admin.html`.
2. Click the **Settings** tab.
3. Find **Change admin setup code**.
4. Enter the **current** code, then a **new** code, then confirm.
5. Click Save.

The new code is what anyone (including you, if you ever need to set up admin on a new device/browser) will need on the setup screen going forward.

If you forget the current code: open Browser DevTools → Application → Local Storage and delete the key `vs_admin_setup_code`. The default `0605` will be restored on next page load.

---

## 4. Member sign-up (clients)

Members create accounts at `client.html`. The form asks for **only**:

- First name
- Last name
- Email
- Phone
- Password (and confirm)

There is **no 6-digit verification code** and no invitation flow. Anyone can create a member account. Their password is hashed with SHA-256 in the browser before storage — the raw password is never saved.

After creating an account they're signed in immediately and land on a dashboard with three tabs:

- **Profile** — their info, account creation date, delete-account button
- **Support** — direct messages to/from you
- **Refer** — referral submission form (you receive these in the admin portal)

---

## 5. Admin dashboard

After signing in, you have these tabs:

| Tab | What's there |
|---|---|
| **Leads** | Marketing-form leads from the public site (Get a Quote, Contact, etc.). Add, edit, advance status, delete, export CSV. |
| **Client Accounts** | Every member who created an account on `client.html`. Search by name/email/phone. Per row you can: send a direct message, reset their password (they'll have to contact you to be issued a new one), or revoke the account. Export CSV. |
| **Support** | Two-way message threads with each member. Reply directly. Marks unread counts. |
| **Referrals** | Every referral submitted via the member portal. Mark status, set the **payout amount**, mark **paid/unpaid**. One-click "Convert to Lead" pushes the referred contact into your Leads pipeline. Export CSV. |
| **Settings** | Change admin password, change setup code, set Make.com webhook URL, export/import all data, sign out. |

### Resetting a member's password

Use the "Reset password" action on their row in **Client Accounts**. This wipes their stored password hash. Next time they try to sign in they'll see a message telling them to contact their advisor for a new one — at which point you can either:

- Tell them to delete their account and create a new one (simplest), or
- Ask them what password they want, sign in as them, and have them change it later (use the same browser they'll use).

There is no email-based password-reset flow because there is no backend mail server in this static setup.

### Revoking an account

"Revoke" on a member row marks their account `status: revoked`. They keep showing up in your Accounts list (so you can audit) but can no longer sign in.

---

## 6. Optional: Make.com webhook

In **Settings → Webhook URL**, paste a Make.com (or Zapier) webhook URL. From then on the following events will be POSTed to it (fire-and-forget, `mode: no-cors`):

- `client_signup` — new member created an account
- `client_signin` — member signed in
- `client_message` — member sent you a support message
- `client_referral` — member submitted a referral
- `client_account_deleted` — member self-deleted their account
- Lead form submissions from the public marketing pages

Use this to mirror events into Google Sheets, Slack, your CRM, or to send yourself email notifications.

---

## 7. Backups (export / import)

The whole admin database is just a few keys in `localStorage`. **Settings → Export data** downloads a single JSON file containing leads, accounts, messages, referrals, webhook URL, and the current setup code. Save this somewhere safe periodically.

To restore (e.g., on a new computer): set up admin first, then **Settings → Import data** and upload the JSON file.

---

## 8. Storage keys reference

If you ever need to inspect or clean up directly in DevTools:

| Key | Holds |
|---|---|
| `vs_admin_hash` | SHA-256 hash of your admin password |
| `vs_admin_session` | Active admin session (sessionStorage) |
| `vs_admin_setup_code` | Current admin setup code (default: `0605`) |
| `vs_leads` | All leads in the CRM |
| `vs_client_accounts` | All member accounts |
| `vs_messages` | All support thread messages |
| `vs_referrals` | All referral submissions |
| `vs_webhook_url` | Make.com / Zapier webhook URL |
| `vs_client_session` | Active client session (sessionStorage, in client.html) |

---

## 9. Quick checklist when going live

1. Open `admin.html`, complete setup with code `0605` and a strong admin password.
2. **Change the setup code** to something only you know (Settings → Change admin setup code).
3. Optional: paste a Make.com webhook URL in Settings.
4. Test creating a member at `client.html`. Confirm they show up in **Client Accounts**.
5. Send yourself a test support message from `client.html` and reply from `admin.html`.
6. Submit a test referral and verify it appears in the **Referrals** tab.
7. Export your data once so you have an empty-baseline backup.

That's it — you're ready to send the link to clients.

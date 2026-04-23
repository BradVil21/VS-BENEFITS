# VS Benefits - Admin Portal Guide

The admin portal is a private page at `/admin.html` that lets you manage leads and your calendar - with optional two-way Google Calendar sync. Nothing public on the site links to it, so casual visitors won't stumble onto it. Search engines are told to ignore it via `noindex,nofollow` in the page head.

## Open the portal

Go to: **`https://vshealthbenefits.com/admin.html`** (or `file:///.../admin.html` while testing locally)

Bookmark it so you can get back quickly.

---

## First-time setup: create your password

1. Open `admin.html` in any browser.
2. You'll see a **"Create your admin password"** screen.
3. Choose a password (at least 8 characters) and confirm it.
4. That's it - you're in.

**Important things to know:**

- The password is hashed with SHA-256 and stored in **your browser only**, never sent anywhere.
- There is **no password reset** - if you forget it, use the "Reset & start over" link on the login page (this wipes the password + all admin data on that device).
- Each browser / device is separate. If you want to sign in from your phone AND laptop, you'll set a password on each one. Use the **Backup / Restore** feature in Settings to copy your data between them.
- Session lasts until you close the browser tab (or click Sign out). You'll need to re-enter the password next time you open the tab.

---

## Leads tab

Manage every prospect in one place.

**Add a lead** - click "+ Add lead" and fill in name, company, phone, email, coverage type, status, next step, notes.

**Edit / delete** - use the Edit or Delete buttons on each row.

**Search** - type into the search box to filter by any field (name, company, email, phone, coverage, notes).

**Filter by status** - use the status dropdown (New / Contacted / Quoted / Closed won / Closed lost).

**Export CSV** - one-click download of all leads. Great for weekly backups or pulling into Excel.

**Import CSV** - upload a CSV with headers. Recognized column names: `name`, `company`, `phone`, `email`, `coverage`, `status`, `next`, `notes`. Extra columns are ignored. Existing leads are kept; imported rows are added to the top.

### Hooking up your Make.com webhook to auto-capture leads

The public site's forms (homepage quick quote, contact, get-a-quote) POST to the webhook URL you set in `assets/js/app.js` (`window.MAKE_WEBHOOK_URL`). To also drop new submissions into the admin portal:

**Option A - Simple (recommended for now):** Keep your Make.com scenario as-is (it emails you or writes to a Google Sheet). When you sit down to do outreach, just click "+ Add lead" and paste the info. Fastest path, zero extra wiring.

**Option B - Google Sheets bridge:** In Make.com, have each form submission write a row to a Google Sheet with columns `name, company, phone, email, coverage, status, next, notes`. Once a day, export that sheet as CSV and use "Import CSV" in the Leads tab.

**Option C - Full automation (later):** If you want real-time capture, you'd need a tiny backend (not part of this static site). Ask me when you're ready and I'll wire it up via a serverless function (Vercel / Netlify / Cloudflare Workers).

---

## Calendar tab

A monthly calendar where you can schedule calls, meetings, and follow-ups. Events save locally by default, and you can optionally sync with Google Calendar.

**Add an event** - click "+ Add event" or click any day on the calendar. Set title, start/end time, location/link, notes.

**Edit an event** - click the colored pill inside a day cell.

**View upcoming** - the "Upcoming (next 14 days)" list below the calendar shows every event (local + Google) in chronological order.

**Color key:**
- Blue pills = local events (saved in this browser)
- Teal pills = Google Calendar events (read from your connected Google account)

---

## Connecting Google Calendar

Google requires you to create your own OAuth Client ID (one-time setup, free). Here's the full walkthrough:

### Step 1: Create a Google Cloud project

1. Go to [console.cloud.google.com](https://console.cloud.google.com) and sign in with the Google account whose calendar you want to connect.
2. Top bar -> project dropdown -> **"New Project"**. Name it "VS Benefits Admin" (or whatever). Click Create.
3. Wait a few seconds for the project to be created, then make sure it's selected in the top bar.

### Step 2: Enable the Google Calendar API

1. Left menu -> **APIs & Services -> Library**.
2. Search "Google Calendar API" -> click it -> click **Enable**.

### Step 3: Configure the OAuth consent screen

1. Left menu -> **APIs & Services -> OAuth consent screen**.
2. User Type: **External** -> Create.
3. Fill in: App name ("VS Benefits Admin"), User support email (your email), Developer contact info (your email). Skip the logo for now.
4. Click Save and Continue.
5. Scopes: click **Add or Remove Scopes**, search for "Google Calendar API", add `../auth/calendar.events`. Also add `../auth/userinfo.email`. Save.
6. Test users: add **your own Google email address**. Save.
7. Summary -> Back to Dashboard. Leave the app in "Testing" mode - you don't need to publish it, since you're the only user.

### Step 4: Create the OAuth Client ID

1. Left menu -> **APIs & Services -> Credentials**.
2. **+ Create Credentials -> OAuth client ID**.
3. Application type: **Web application**. Name: "VS Admin Web".
4. **Authorized JavaScript origins** - add these (whichever you'll use):
   - `https://vshealthbenefits.com`
   - `http://localhost` (for local testing via localhost server)
   - Leave blank any that don't apply. **Do NOT use `file://`** - Google rejects it. For local testing, run a quick local server (e.g., `python3 -m http.server 8080` in the site folder, then open `http://localhost:8080/admin.html`).
5. Click **Create**. You'll see a Client ID like `123456789-abc123.apps.googleusercontent.com`. Copy it.

### Step 5: Paste the Client ID into the admin portal

1. In `admin.html`, go to the **Settings** tab.
2. Paste your Client ID into the **Google Client ID** field and click **Save Client ID**.
3. Go to the **Calendar** tab -> click **Connect Google Calendar**.
4. A Google sign-in popup appears. Choose your account, grant the permissions.
5. The status should flip to "Connected - your@email.com" and your upcoming events should load.

### Creating events on Google Calendar

When you add a new event in the admin, check the **"Also create on Google Calendar (if connected)"** box. The event will be pushed to your primary Google Calendar, so it shows up on your phone, Gmail side-panel, etc.

(Editing existing Google events is deliberately disabled in the portal - edit those on Google Calendar directly. This keeps scopes minimal and avoids accidental overwrites.)

---

## Settings tab

- **Change password** - rotate your admin password. Requires your current password.
- **Google OAuth Client ID** - see the Connecting Google Calendar section above.
- **Backup all data (JSON)** - downloads a `.json` file with every lead, event, and your Client ID (password hash and Google token are **not** exported, for safety). Save these weekly.
- **Restore from backup** - merges a previously-exported JSON into your current data. Handy for moving to a new device.
- **Wipe all admin data** - nuclear option. Clears password, leads, events, Google connection on this device.

---

## Security notes (please read)

This is a **single-user, single-device** admin - on purpose, since the public site is fully static (no server, no database).

- Leads and events live in your browser's `localStorage`. They are **not** on a server. If you clear your browser data, they're gone. **Back up weekly.**
- The password gate keeps casual visitors out, but a determined attacker with physical access to your unlocked laptop could inspect localStorage. Don't leave your laptop unlocked in public.
- If you need true multi-device real-time sync, tell me and I'll set up a proper backend (serverless + a database like Firestore or Supabase).

---

## Troubleshooting

**"I can't sign in - it says wrong password"**
Passwords are per-device. If you set it on your laptop, your phone won't know about it. Click "Reset & start over" to create a fresh password on this device.

**"The Connect Google Calendar button is disabled"**
You haven't saved your Google Client ID yet. Settings tab -> paste Client ID -> Save.

**"Google sign-in opens then says 'Access blocked'"**
Usually means you're loading the page from `file://` (not allowed) or your URL isn't in Authorized JavaScript origins. Either run a local server, or make sure the exact domain you're on is listed in the OAuth Client settings.

**"Events show the wrong time zone"**
The portal uses your browser's time zone. If you're on the road, events will display in the local time zone of the device you're viewing them on. Google's copies remain in the time zone they were created in.

**"I lost my data!"**
If you cleared browser data or switched devices - this is why you back up regularly. Settings -> Backup all data -> save the JSON somewhere safe (Dropbox, iCloud Drive, even email to yourself).

---

## Roadmap ideas (not built yet, ask if you want any)

- Two-way editing of Google events (not just read)
- Auto-push of new admin events to Google without the checkbox
- Per-lead reminders tied to calendar events
- Proper server-side backend so multiple devices stay in sync
- A "pipeline view" - drag leads between columns (Kanban)
- Email drafting from a lead row (pre-filled mailto)
- Click-to-call logging (stamp a note every time you dial)

Just let me know which of these you'd actually use.

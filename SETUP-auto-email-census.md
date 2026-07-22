# Business auto-email + census — setup & go-live guide

This adds an automated, branded flow to your **business (group) quote**:

1. A business submits the quote at `/quote`.
2. They instantly get a **VS Health Benefits** confirmation email (personalized with their name/business) with a **"Fill out census form"** button.
3. They complete the census at `/census` (employees + spouses/children, ages, genders, ZIP).
4. The census is saved to that **contact's record in HubSpot** as a CSV, and you get a **"Census completed"** summary email.

Everything is **safe by default**: if a key is missing, that step is skipped and the site keeps working — nothing breaks.

---

## New / changed files

| File | What it is |
|---|---|
| `api/_lib.js` | **New.** Shared helpers: HubSpot calls, Resend email, branded email templates. |
| `api/business-quote.js` | **New.** Runs when a business quote is submitted: upserts the HubSpot contact, sends the branded email + census link, alerts you. |
| `api/census.js` | **New.** Runs when the census is submitted: builds the CSV, saves it to the HubSpot contact, emails you the summary, confirms to the lead. |
| `census.html` | **New.** The branded census form page (served at `/census`). |
| `quote/index.html` | **Changed.** Removed the GoHighLevel/LeadConnector webhook; business submissions now call `/api/business-quote`. HubSpot + Firebase (admin portal) unchanged. |

---

## What you need to set (one time)

In **Vercel → your project → Settings → Environment Variables** (Production + Preview), then redeploy:

| Variable | Required? | Value |
|---|---|---|
| `HUBSPOT_PRIVATE_APP_TOKEN` | Already set (used by your existing contact form) | Your HubSpot private-app token. Make sure its scopes include: `crm.objects.contacts.read/write`, `crm.objects.notes.write` (a.k.a. engagements), and `files` (for saving the census CSV). |
| `RESEND_API_KEY` | **Yes, to send email** | From [resend.com](https://resend.com) — free tier covers 3,000 emails/mo. |
| `FROM_EMAIL` | Optional | Default `VS Health Benefits <quotes@vshealthbenefits.com>`. Must be on a **verified domain** in Resend (see below). |
| `REPLY_TO_EMAIL` | Optional | Where replies go. Default: your notify address. |
| `NOTIFY_EMAIL` | Optional | Where *your* lead/census alerts go. Default `bvilsainthealth@gmail.com`. |
| `SITE_URL` | Optional | Default `https://www.vshealthbenefits.com`. |

### Verifying your sending domain in Resend (≈10 min, one time)
So emails come from `@vshealthbenefits.com` and land in inboxes (not spam):
1. Create a free Resend account, go to **Domains → Add Domain**, enter `vshealthbenefits.com`.
2. Resend shows a few **DNS records** (SPF, DKIM). Add them wherever your DNS lives (likely Vercel or your registrar).
3. Wait for "Verified," then create an **API key** and paste it into Vercel as `RESEND_API_KEY`.

> Until `RESEND_API_KEY` is set, everything else still works — the flow just won't send email yet (the functions report `"no_resend_key"` and return success so the form never breaks).

---

## How to test after deploying

1. Go to `https://www.vshealthbenefits.com/quote`, choose **Business**, and submit with a real email you control.
2. Check that email for the **"Your group health quote — quick info needed"** message and click **Fill out census form**.
3. Fill the census and submit. You should get the **"Census completed"** summary at your `NOTIFY_EMAIL`, and the CSV should appear on the contact in HubSpot (Contacts → the lead → Notes/Attachments).
4. In Vercel → your project → **Logs**, you can see each function's JSON response (`leadEmail: "sent"`, `alert: "sent"`, etc.) if you want to confirm.

---

## Notes & options

- **Where the census shows in HubSpot:** it's attached to the contact as a Note with the CSV file and a readable table, and the contact's lifecycle stage moves to `Census Received — Ready to Quote`. That's the "auto-saved to the lead's Documents tab in the CRM" behavior from your mockup.
- **Individual leads** are unchanged — they still flow to HubSpot + your admin portal as before. (If you want individual leads to get an auto-email too, that's a small addition — just ask.)
- **No extra vendor?** If you'd rather not use Resend, HubSpot can send the confirmation email via a **Workflow** triggered on the contact property `website_lead_stage = "Business Quote — Awaiting Census"` (requires Marketing Hub). The census-to-CRM part still works either way. Say the word and I'll wire the HubSpot-workflow version instead.
- **Re-enabling an external webhook** (Zapier/Make/GHL) later: paste its URL into `WEBHOOK_URL` near the top of the script in `quote/index.html`.

# Member Account Creation — automation setup

When someone creates an account in the client portal (`/client.html`) they get
three messages from GoHighLevel:

| # | Message | When |
|---|---|---|
| 1 | Welcome **email** | immediately |
| 2 | Welcome **SMS** | +5 minutes |
| 3 | Website tour **email** | +1 day |

All three mention the referral payout. **GoHighLevel is the only destination.**
HubSpot and EmailJS have been removed from the portal.

## How it flows

```
client.html signup form
  └─ window.ghlSyncAccount(acct)
       └─ POST /api/portal-signup            ← server-side, holds the GHL token
            ├─ 1. upsert contact in GHL      (by email/phone)
            ├─ 2. write custom field         Admin Client ID
            ├─ 3. add tags                   portal-account-created, member-portal
            └─ 4. POST to the Inbound Webhook URL   ◄── TRIGGER
                                                  │
GHL workflow "Member Account Creation" ───────────┘
  ├─ Create/Update Contact   (attaches the contact to the run)
  ├─ Send Email  — welcome
  ├─ Wait 5 minutes
  ├─ Send SMS    — welcome
  ├─ Wait 1 day
  └─ Send Email  — website tour
```

**Why the webhook fires last.** The contact is upserted *before* the webhook is
called, so by the time the workflow starts, the record already exists with every
field populated and carries a real `contact_id`. The first workflow action
matches that contact instead of creating a duplicate, which is what makes
`{{contact.first_name}}` resolve in the messages.

**Trigger URL** (already hardcoded as the default in `api/portal-signup.js`):

```
https://services.leadconnectorhq.com/hooks/cNCy6JUURpb4eBDdb9bU/webhook-trigger/f3ed39bb-f80b-4b00-bde2-bf8d18749512
```

This URL is not a secret — it only accepts data, it never returns any. Override
it with the `GHL_INBOUND_WEBHOOK_URL` env var if it ever gets regenerated.

> ⚠️ **The URL is not final until you click "Save trigger."** GHL generates a
> fresh URL each time you open an unsaved Inbound Webhook trigger, so the one
> displayed in the panel changes on you until it's saved. Save the trigger
> first, *then* copy the URL and compare it to the one above.
>
> ⚠️ **A `200` response from this endpoint does not mean the URL is real.**
> GHL returns `{"status":"Success: test request received"}` for *any* UUID in
> that path, including one made up from scratch (verified). The only reliable
> confirmation is the **Mapping Reference** dropdown inside the trigger showing
> your payload after you click *Check for new requests*. Do not treat a 200 in
> a curl or a Vercel log as proof the workflow was reached.

## 1. Vercel environment variables

Project → Settings → Environment Variables:

| Variable | Required | Value |
|---|---|---|
| `GHL_PIT_TOKEN` | **yes** | your `pit-…` private integration token |
| `GHL_LOCATION_ID` | no | defaults to `cNCy6JUURpb4eBDdb9bU` |
| `GHL_SIGNUP_TAG` | no | defaults to `portal-account-created` |
| `GHL_INBOUND_WEBHOOK_URL` | no | overrides the trigger URL above |
| `PORTAL_SIGNUP_SECRET` | no | shared secret; callers must send `x-vs-portal-secret` |

> **Never** put the token in `client.html` or any committed file — this repo is
> public on GitHub. `api/portal-signup.js` and `api/portal-referral.js` read it
> from the environment only, with no fallback, on purpose.

## 2. Build the workflow in GHL

The GHL API is **read-only for workflows** — there is no endpoint that writes
steps — so these have to be clicked. Open the existing draft named
**Member Account Creation** rather than creating a new one.

**Automation → Workflows → Member Account Creation**

### 2.1 Trigger

1. **Add New Trigger** → **Inbound Webhook**
2. Name: `Inbound Webhook`
3. Click **Save trigger** now, before anything else. Until you do, the URL in
   the panel is provisional and regenerates every time you reopen it.
4. Reopen the trigger and copy the saved URL. If it differs from the trigger URL
   above, set it as `GHL_INBOUND_WEBHOOK_URL` in Vercel — that's faster than a
   code push and it's why the env var exists.
5. Send a sample payload so the mapping reference has fields to offer, then
   click **Check for new requests** in the Mapping Reference dropdown. If your
   payload does not appear there, the URL is wrong — a `200` response does not
   confirm anything (see the warning above).

   ```bash
   curl -X POST "https://services.leadconnectorhq.com/hooks/cNCy6JUURpb4eBDdb9bU/webhook-trigger/f3ed39bb-f80b-4b00-bde2-bf8d18749512" \
     -H "Content-Type: application/json" \
     -d '{"event":"client_signup","contact_id":"SAMPLE_CONTACT_ID","first_name":"Sample","last_name":"Member","full_name":"Sample Member","email":"sample.member@example.com","phone":"+19548666872","account_id":"sample-account-id","sms_eligible":true,"source":"vshealthbenefits.com","page":"/client.html"}'
   ```

6. **Save trigger** again if you changed anything.

### 2.2 Payload fields available for mapping

`api/portal-signup.js` deliberately sends each name in more than one shape,
because different steps in the GHL builder default to different conventions.

| Field | Example | Use for |
|---|---|---|
| `contact_id` / `contactId` | `abc123…` | matching the existing contact |
| `first_name` / `firstName` | `Sample` | greeting |
| `last_name` / `lastName` | `Member` | contact record |
| `full_name` / `name` | `Sample Member` | contact record |
| `email` | `sample.member@example.com` | email send |
| `phone` | `+19548666872` | SMS send (already E.164) |
| `account_id` / `accountId` | `sample-account-id` | portal cross-reference |
| `sms_eligible` | `true` | optional if/else branch |
| `event` | `client_signup` | sanity check |

Merge-field syntax for webhook data is `{{inboundWebhookRequest.first_name}}`.

### 2.3 Actions, in order

**Action 1 — Create/Update Contact** (Contact category)

Map these, then save. This is the step that attaches the contact to the run;
without it `{{contact.*}}` merge fields stay blank.

| Contact field | Value |
|---|---|
| Email | `{{inboundWebhookRequest.email}}` |
| Phone | `{{inboundWebhookRequest.phone}}` |
| First Name | `{{inboundWebhookRequest.first_name}}` |
| Last Name | `{{inboundWebhookRequest.last_name}}` |

**Action 2 — Send Email** (welcome, copy below)

- From name: `VS Health Benefits`
- From email: `info@vshealthbenefits.com`
- Subject: `Welcome to VS Health Benefits — your account is ready`

**Action 3 — Wait** → `5 minutes`

**Action 4 — Send SMS** (copy below)

**Action 5 — Wait** → `1 day`

**Action 6 — Send Email** (website tour, copy below)

- Subject: `A quick tour of your VS Health Benefits account`

Then top right → toggle **Draft → Publish**.

### Workflow settings (gear icon, top right)

- **Allow Re-Entry**: **off** — one welcome per member, even if the webhook
  fires twice.
- **Stop on Response**: off.

---

## Email 1 — Welcome (sends immediately)

Subject: `Welcome to VS Health Benefits — your account is ready`

```
Hi {{contact.first_name}},

Your VS Health Benefits member account is ready.

Sign in any time at https://www.vshealthbenefits.com/client to:
  • View your plan details
  • Refer friends and family and track your rewards
  • Message your advisor directly

One thing worth knowing on day one: you get paid to refer.
Every person you send our way who ends up enrolling earns you a payout —
there's no cap, and it costs them nothing. Details and current rates are at
https://www.vshealthbenefits.com/refer-and-earn

Tomorrow I'll send you a short tour of the tools on the site so you know
what's there before you need it.

If you didn't create this account, reply to this email or call (954) 866-6872
and we'll take care of it.

Thank you,
Bradley Vilsaint
VS Health Benefits
(954) 866-6872
```

## SMS — Welcome (sends 5 minutes later)

```
VS Health Benefits: Hi {{contact.first_name}}, your account is ready. Sign in at vshealthbenefits.com/client to view your plan and refer friends. Reply STOP to opt out.
```

157 characters with an 11-letter first name, so it stays a **single segment**
regardless of who signs up. If you edit it, re-check the length — going one
character over doubles your per-message cost.

`Reply STOP to opt out` is not optional. It is required for A2P/TCPA compliance
on an automated message.

## Email 2 — Website tour (sends 1 day later)

Subject: `A quick tour of your VS Health Benefits account`

```
Hi {{contact.first_name}},

Now that you're set up, here's what's waiting for you on the site — most of
it takes under two minutes to use.

1. Get a quote
   Compare real plans side by side.
   https://www.vshealthbenefits.com/get-a-quote

2. See what a subsidy could save you
   Most people qualify for more help than they expect.
   https://www.vshealthbenefits.com/aca-subsidy-calculator

3. Plain-English guides
   Deductibles, HMO vs PPO, what happens if you miss open enrollment.
   https://www.vshealthbenefits.com/blog

4. Book time with an advisor
   A real conversation, no pressure, no cost.
   https://www.vshealthbenefits.com/book

5. Refer and earn
   This is the one people overlook. Refer someone who enrolls and you get
   paid — friends, family, coworkers, your barber. There's no limit on how
   many you can refer, and there's never a cost to the person you send.
   You can submit a referral straight from your portal dashboard and watch
   its status update as it moves along.
   https://www.vshealthbenefits.com/refer-and-earn

Your portal: https://www.vshealthbenefits.com/client

Reply to this email any time with a question — it comes straight to me.

Bradley Vilsaint
VS Health Benefits
(954) 866-6872
```

---

## 3. Prerequisites for the SMS to actually send

The emails will work immediately. The SMS will silently fail without all three:

1. A phone number provisioned in the sub-account (**Settings → Phone Numbers**)
2. **A2P 10DLC registration approved** (Settings → Phone Numbers → Trust Center).
   This takes a few business days — start it now if you haven't.
3. The contact has a valid mobile number. `api/portal-signup.js` normalises to
   E.164 (`+1XXXXXXXXXX`) and drops anything that isn't a real 10-digit US
   number, so bad numbers never reach GHL.

If a member signs up without a usable phone, the endpoint returns
`smsEligible: false`, the payload carries `sms_eligible: false`, and only the
emails go out. That's intended, not a bug. If you want the SMS step skipped
cleanly rather than failing, add an **If/Else** before Action 4 on
`{{inboundWebhookRequest.sms_eligible}}` is `true`.

## 4. Test it

1. Deploy, then create a test account at `/client.html` with a real email and
   your own mobile number.
2. Check the Vercel function log for `/api/portal-signup` — you want
   `{"ok":true,"smsEligible":true,"contactId":"…","tagged":true,"triggered":true}`.
   Note that `triggered: true` only means GHL returned a 200 — that endpoint
   returns 200 for any URL shape, so it is **not** proof the workflow was
   reached. Confirm with step 4 below instead.
3. In GHL, open the contact — it should carry the tags `portal-account-created`
   and `member-portal`.
4. Workflow → **Enrollment History** shows the contact entering and each action's
   status. The tour email will sit as "waiting" for a day — that's correct.
5. Delete the test contact when you're done so it doesn't skew your counts.

## What was removed, and where it went

| Was | Now |
|---|---|
| `window.hubspotSyncAccount()` — HubSpot hidden signup form | deleted; `/api/portal-signup` upserts into GHL |
| `window.hubspotSyncReferral()` — HubSpot "Client Referral" form | replaced by `window.ghlSyncReferral()` → `/api/portal-referral` |
| `window.sendWelcomeEmail()` + EmailJS SDK | deleted; the GHL workflow sends every message |
| `webhookFire` signup payload carrying `email_subject` / `email_body` | stripped; `send_email:false` remains so nothing downstream can send a second welcome |

`api/portal-referral.js` is new. It upserts the referred person into GHL, tags
them `portal-referral` + `client-referral`, and attaches a note with the full
referral detail and who sent it, so referral credit stays traceable.

**Still on HubSpot, deliberately untouched:** the HubSpot tracking embed on the
public marketing pages, and the quote/census endpoints (`api/census.js`,
`api/business-quote.js`, `api/lead-draft.js`, `api/hubspot-ticket.js`). Those
need GHL equivalents built before their HubSpot calls can be removed, or the
leads they carry would be dropped.

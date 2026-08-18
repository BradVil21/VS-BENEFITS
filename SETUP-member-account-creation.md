# Member Account Creation — automation setup

When someone creates an account in the client portal (`/client.html`) they get
three messages from GoHighLevel:

| # | Message | When |
|---|---|---|
| 1 | Welcome **email** | immediately |
| 2 | Welcome **SMS** | +5 minutes |
| 3 | Portal tour **email** | +1 day |

All three mention the referral payout. **GoHighLevel is the only destination.**
HubSpot and EmailJS have been removed from the portal.

## How it flows

```
client.html signup form
  └─ window.ghlSyncAccount(acct)
       └─ POST /api/portal-signup            ← server-side, holds the GHL token
            ├─ 1. upsert contact in GHL      (by email/phone)
            ├─ 2. write custom field         Admin Client ID
            └─ 3. add tag `portal-account-created`   ◄── TRIGGER
                    (+ `member-portal` for segmentation)
                                                  │
GHL workflow "Member Account Creation" ───────────┘
  ├─ Send Email  — welcome
  ├─ Wait 5 minutes
  ├─ Send SMS    — welcome
  ├─ Wait 1 day
  └─ Send Email  — portal tour
```

**Why a tag and not an Inbound Webhook.** GHL bills the Inbound Webhook as a
*premium trigger, charged per execution* — every signup would cost you. It also
starts the workflow with no contact attached, so it needs an extra
Create/Update Contact step before `{{contact.first_name}}` resolves. The tag is
free, and because it is applied *after* the upsert it fires on a contact that
already exists with every field populated. Fewer steps, nothing to map.

The webhook path is still in the code, switched off, so you can move back to it
without a deploy — set `GHL_INBOUND_WEBHOOK_URL` to a workflow's URL.

> ⚠️ If you ever do wire a webhook: that endpoint answers
> `200 {"status":"Success: test request received"}` for **any** URL of that
> shape, including a UUID invented from scratch (verified). A 200 proves
> nothing. The only real confirmation is your payload appearing under the
> trigger's **Mapping Reference** in GHL.

## 1. Vercel environment variables

Project → Settings → Environment Variables:

| Variable | Required | Value |
|---|---|---|
| `GHL_PIT_TOKEN` | **yes** | your `pit-…` private integration token |
| `GHL_LOCATION_ID` | no | defaults to `cNCy6JUURpb4eBDdb9bU` |
| `GHL_SIGNUP_TAG` | no | defaults to `portal-account-created`. **Must match the tag the workflow triggers on.** |
| `GHL_INBOUND_WEBHOOK_URL` | no | unset = no webhook call at all. Set to a URL to mirror the payload, or `off` to disable explicitly. |
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

1. If an **Inbound webhook** trigger is already on the canvas, delete it — it
   bills per execution and you no longer need it.
2. **Add New Trigger** → **Contact Tag**
3. Filter: `Tag` **is** `portal-account-created`
4. **Save trigger.**

That is the whole trigger setup. No URL, no payload mapping, no sample request.

### 2.2 Actions, in order

Every `{{contact.*}}` merge field resolves on its own, because the tag fires on
a contact that is already complete.

| # | Action | Settings |
|---|---|---|
| 1 | **Send Email** | From name `VS Health Benefits`, from email `info@vshealthbenefits.com`, subject `Welcome to VS Health Benefits — your account is ready`, body = *Email 1* below |
| 2 | **Wait** | `5 minutes` |
| 3 | **Send SMS** | message = *SMS* below |
| 4 | **Wait** | `1 day` |
| 5 | **Send Email** | subject `Your VS Health Benefits portal — the quick map`, body = *Email 2* below |

Then top right → toggle **Draft → Publish**. Nothing sends while it is a draft.

### Workflow settings (gear icon, top right)

- **Allow Re-Entry**: **off** — one welcome per member, even if the tag is
  re-applied later.
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

When you sign in the first time we'll walk you through the portal. Tomorrow
we'll send that same map in writing so you have it later.

If you didn't create this account, reply to this email or call (954) 866-6872
and we'll take care of it.

Thank you,
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

## Email 2 — Portal + site tour (sends 1 day later)

Subject: `Your VS Health Benefits portal — the quick map`

This mirrors the six-step in-portal tour (`CP_TOUR` in `client.html`) using the
same section names, so the email and the portal call things the same thing. It
then covers the site tools the in-portal tour does not touch.

**Why it restates the tour instead of saying "go take the tour":** the tour only
runs once, on first login, while `welcomePending` is true. Both *Take the quick
tour* and *Skip tutorial* set that flag to false permanently — there is no way to
replay it. Anyone who skipped would be sent to look for something that no longer
appears. So this email *is* the second chance.

```
Hi {{contact.first_name}},

When you first signed in we walked you through your portal. Here's that
same map in writing, in case you skipped it or want it handy later.

INSIDE YOUR PORTAL
https://www.vshealthbenefits.com/client

  Your dashboard
  Referrals sent, sold, and total earned at a glance.

  Send a referral
  Refer anyone who needs health insurance. Add their details and we take
  care of the rest. You earn when they enroll.

  Track your referrals
  Everyone you've sent, with live status, from In Progress to Paid.

  Your plan
  Your current coverage and plan details, kept up to date by your advisor.

  Message support
  Reach your advisor directly with any question. We typically reply
  within 24 hours.

  Your settings
  Update your profile, add a photo, and change your password any time.

MORE ON THE REFERRAL SIDE

That second one is the part people overlook. Refer someone who enrolls and
you get paid — friends, family, coworkers, your barber. There's no limit on
how many you can refer, and it never costs the person you send anything.
Submit one straight from your dashboard and watch its status update as it
moves along.
https://www.vshealthbenefits.com/refer-and-earn

ON THE SITE

  Get a quote — compare real plans side by side
  https://www.vshealthbenefits.com/get-a-quote

  Subsidy calculator — most people qualify for more help than they expect
  https://www.vshealthbenefits.com/aca-subsidy-calculator

  Guides — deductibles, HMO vs PPO, what happens if you miss open enrollment
  https://www.vshealthbenefits.com/blog

  Book an advisor — a real conversation, no pressure, no cost
  https://www.vshealthbenefits.com/book

Reply to this email any time with a question — it comes straight to us.

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
`smsEligible: false` and only the emails go out. That's intended, not a bug.

## 4. Test it

1. Deploy, then create a test account at `/client.html` with a real email and
   your own mobile number.
2. Check the Vercel function log for `/api/portal-signup`. You want:

   ```json
   {"ok":true,"smsEligible":true,"contactId":"…","tagged":true}
   ```

   **`tagged: true` is the one that matters.** It is the trigger. If it is
   `false`, the workflow was never started and no amount of debugging inside
   GHL will explain why — look at `tagError` instead.
3. In GHL, open the contact — it should carry `portal-account-created` and
   `member-portal`.
4. Workflow → **Enrollment History** shows the contact entering and each
   action's status. The tour email sits as "waiting" for a day — that's correct,
   not a stall.
5. Delete the test contact when you're done so it doesn't skew your counts.

### If the email arrives but says "Hi ," with no name

The contact reached GHL without a first name. Check the signup form actually
sent one — `/api/portal-signup` trims and forwards whatever it receives, it
does not invent a fallback.

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

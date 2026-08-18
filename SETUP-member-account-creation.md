# Member Account Creation — automation setup

When someone creates an account in the client portal (`/client.html`), they get a
welcome **email** and **SMS** from GoHighLevel.

## How it flows

```
client.html signup form
  └─ window.ghlSyncAccount(acct)
       └─ POST /api/portal-signup            ← server-side, holds the GHL token
            ├─ 1. upsert contact in GHL      (by email/phone)
            ├─ 2. write custom field         Admin Client ID
            ├─ 3. add tag `portal-account-created`   ◄── TRIGGER
            └─ 4. (optional) mirror raw JSON to an Inbound Webhook URL
                                                  │
GHL workflow "Member Account Creation" ───────────┘
  ├─ Send Email  (welcome)
  └─ Send SMS    (welcome)
```

**Why a tag and not a raw inbound webhook as the trigger:** the tag fires on a
contact that already exists with every field populated, so `{{contact.first_name}}`
and friends resolve in the email and SMS. An inbound-webhook trigger would need
every field re-mapped by hand and can fire before the record is complete.

The raw webhook mirror (step 4) is still available via `GHL_INBOUND_WEBHOOK_URL`
if you want a second listener — but it is not required for this automation.

## 1. Vercel environment variables

Project → Settings → Environment Variables:

| Variable | Required | Value |
|---|---|---|
| `GHL_PIT_TOKEN` | **yes** | your `pit-…` private integration token |
| `GHL_LOCATION_ID` | no | defaults to `cNCy6JUURpb4eBDdb9bU` |
| `GHL_SIGNUP_TAG` | no | defaults to `portal-account-created` |
| `GHL_INBOUND_WEBHOOK_URL` | no | only if you want the raw JSON mirrored |
| `PORTAL_SIGNUP_SECRET` | no | shared secret; callers must send `x-vs-portal-secret` |

> **Never** put the token in `client.html` or any committed file — this repo is
> public on GitHub. `api/portal-signup.js` reads it from the environment only,
> with no fallback, on purpose.

## 2. Build the workflow in GHL

The GHL API is **read-only for workflows** (`POST /workflows/` → 404; there is no
endpoint to write steps), so these steps have to be clicked. You already have a
draft named **Member Account Creation** — open that one rather than making a new one.

**Automation → Workflows → Member Account Creation**

1. **Trigger** → *Add New Trigger* → **Contact Tag**
   - Filter: `Tag` **is** `portal-account-created`
2. **+ Add Action** → **Send Email**
   - From name: `VS Health Benefits`
   - From email: `info@vshealthbenefits.com`
   - Subject: `Welcome to VS Health Benefits — your account is ready`
   - Body: see below
3. **+ Add Action** → **Wait** → `1 minute`
   *(so the email and text don't land in the same second)*
4. **+ Add Action** → **Send SMS**
   - Message: see below
5. Top right → toggle **Draft → Publish**

### Email body

```
Hi {{contact.first_name}},

Your VS Health Benefits member account is ready.

You can sign in any time at https://www.vshealthbenefits.com/client to:
  • View your plan details
  • Refer friends and family and track your rewards
  • Message your advisor directly

While you're here, take a quick tour of the site:
  • Compare plans and get a quote — https://www.vshealthbenefits.com/get-a-quote
  • See what a subsidy could save you — https://www.vshealthbenefits.com/aca-subsidy-calculator
  • Plain-English guides on deductibles, HMO vs PPO and more — https://www.vshealthbenefits.com/blog
  • Earn rewards for referrals — https://www.vshealthbenefits.com/refer-and-earn
  • Book time with an advisor — https://www.vshealthbenefits.com/book

If you didn't create this account, reply to this email or call (954) 866-6872
and we'll take care of it.

Thank you,
Bradley Vilsaint
VS Health Benefits
```

### SMS body

Keep it under 160 characters so it sends as a single segment:

```
VS Health Benefits: Hi {{contact.first_name}}, your member account is ready. Sign in at vshealthbenefits.com/client. Reply STOP to opt out.
```

That's 139 characters with a short first name. `Reply STOP to opt out` is not
optional — it is required for A2P/TCPA compliance on an automated message.

### Workflow settings (gear icon, top right)

- **Allow Re-Entry**: **off** — one welcome per member, even if the tag is
  re-applied.
- **Stop on Response**: off.

## 3. Prerequisites for the SMS to actually send

The email will work immediately. The SMS will silently fail without all three:

1. A phone number provisioned in the sub-account (**Settings → Phone Numbers**)
2. **A2P 10DLC registration approved** (Settings → Phone Numbers → Trust Center).
   This takes a few business days — start it now if you haven't.
3. The contact has a valid mobile number. `api/portal-signup.js` normalises to
   E.164 (`+1XXXXXXXXXX`) and drops anything that isn't a real 10-digit US
   number, so bad numbers never reach GHL.

If a member signs up without a usable phone, the endpoint returns
`smsEligible: false` and only the email goes out. That's intended, not a bug.

## 4. Test it

1. Deploy, then create a test account at `/client.html` with a real email and
   your own mobile number.
2. Check the Vercel function log for `/api/portal-signup` — you want
   `{"ok":true,"smsEligible":true,"contactId":"…","tagged":true}`.
3. In GHL, open the contact — it should carry the tags `portal-account-created`
   and `member-portal`.
4. Workflow → **Enrollment History** tab shows the contact entering, and each
   action's status.
5. Delete the test contact when you're done so it doesn't skew your counts.

## Duplicate-email warning (already handled)

Before this change, a signup could fire **three** welcome emails — EmailJS,
Make.com, and now GHL. Two were disabled in `client.html`:

- `window.sendWelcomeEmail(acct)` — commented out (EmailJS)
- the Make.com `webhookFire` payload now sends `send_email: false`

Both are one-line reversals if you ever turn the GHL workflow off. The Make.com
`client_signup` event still fires, so anything else you built on that scenario
keeps working — it just no longer sends the email.

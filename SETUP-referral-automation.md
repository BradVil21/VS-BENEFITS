# Referral automation — setup

Three GoHighLevel workflows covering the life of a referral. All three are
triggered by **contact tags**, which are free — no premium webhook triggers.

| Workflow | Fires when | Sends |
|---|---|---|
| **Referral Submitted** | member submits the portal referral form | thank-you email + SMS to the member, internal SMS to you |
| **Referral Status Update** | you change a referral's status in admin | one SMS to the member, wording matched to the new status |
| **Referral Sold** | you set a referral to **Sold** | congrats email + SMS to the member |

Everyone messaged here is the **member who sent the referral**, never the person
who was referred.

## 0. Prerequisite — create four custom fields

GHL → Settings → Custom Fields → add these four, all **model: Contact**:

| Field name | Type | Resulting key |
|---|---|---|
| Referral Name | Text | `contact.referral_name` |
| Referral Status | Text | `contact.referral_status` |
| Referral Status Message | Text (multi-line is fine) | `contact.referral_status_message` |
| Referral Payout | Text | `contact.referral_payout` |

The field **key** is what matters, and GHL derives it from the name — so name
them exactly as above and the keys come out right.

You do not need to copy any field IDs. `api/referral-status.js` looks them up by
key at runtime and caches the result, so recreating a field later won't break
anything.

## How it flows

```
MEMBER SUBMITS A REFERRAL
  client.html referral wizard
    └─ ghlSyncReferral()  ->  POST /api/portal-referral
         ├─ upsert the REFERRED person   (tags: portal-referral, client-referral)
         ├─ note with the full detail + who referred them
         └─ upsert the REFERRING MEMBER  ──► tag `referral-submitted`   ◄── TRIGGER
                                                        │
                          workflow "Referral Submitted" ┘

YOU CHANGE A STATUS IN ADMIN
  admin.html updateRef(id,{status:"sold"})
    └─ sendReferralStatusEmail()  ->  POST /api/referral-status
         ├─ upsert the REFERRING MEMBER
         ├─ write contact.referral_status_message  (the exact SMS text)
         └─ tag `referral-status-updated`            ◄── TRIGGER
            plus `referral-sold` on Sold, `referral-paid` on Paid
                                                        │
                    workflow "Referral Status Update" ──┘
                    workflow "Referral Sold" ───────────┘
```

**Why the message text is written into a custom field.** One workflow covers all
five statuses instead of five near-identical workflows. The SMS body in GHL is
literally just `{{contact.referral_status_message}}`; the wording lives in
`api/referral-status.js`, in version control, where the 160-character limit is
enforced in code. Change the copy there and every status message updates with a
deploy — no clicking through the builder.

---

## 1. Workflow: Referral Submitted

**Trigger:** Contact Tag → `Tag` is `referral-submitted`

**Settings (gear icon):** Allow Re-Entry **ON** — a member refers more than once.

**Actions:**

1. **Send Email**
   - From: `VS Health Benefits` / `info@vshealthbenefits.com`
   - Subject: `We got your referral — here's what happens next`
   - Body: *Email A* below
2. **Wait** → `2 minutes`
3. **Send SMS** → *SMS A* below
4. **Internal Notification** → **SMS** → your mobile → *Internal alert* below
5. **Remove Contact Tag** → `referral-submitted`

Step 5 is what lets the next referral re-fire it. Without it the tag is already
present and the trigger never sees a change.

### Email A — thank you

```
Hi {{contact.first_name}},

Got it — thank you for the referral.

Here's what happens next. We reach out to them directly, usually within one
business day. From there it moves through a few stages, and you'll get a text
at each one so you're never wondering where it stands:

  In Progress    we've started working on it
  Being Reviewed we're matching them to plans and carriers
  Sold           they enrolled
  Paid           your payout has been sent

You can watch the same status live in your portal any time:
https://www.vshealthbenefits.com/client

There's no limit on how many people you can refer, and it never costs them
anything. If you know someone else who needs coverage, send them over.

Thank you,
VS Health Benefits
(954) 825-1009
```

### SMS A — thank you

```
VS Health Benefits: Thanks for the referral! We will reach out to them within 1 business day and text you at every stage. Reply STOP to opt out.
```

142 characters — a single segment.

### Internal alert — to you

**Internal Notification → SMS**, to your own mobile:

```
New referral from {{contact.first_name}} {{contact.last_name}} ({{contact.phone}}). Check the admin portal.
```

---

## 2. Workflow: Referral Status Update

**Trigger:** Contact Tag → `Tag` is `referral-status-updated`

**Settings (gear icon):** Allow Re-Entry **ON** — this is essential, the whole
point is that it fires again on every status change.

**Actions:**

1. **Send SMS** — the body is *only* this merge field, nothing else:

   ```
   {{contact.referral_status_message}}
   ```

2. **Remove Contact Tag** → `referral-status-updated`

That's the entire workflow. Two steps.

**Step 2 is not optional.** GHL fires a tag trigger on the tag being *added*. If
the tag is still on the contact from last time, adding it again is a no-op and
the member silently stops getting updates after the first one.

### What actually gets sent

Composed server-side and capped at 160 characters:

| Status | Message |
|---|---|
| In Progress | `VS Health Benefits: Your referral for Maria Lopez is in progress, we have started working on it. See vshealthbenefits.com/client. Reply STOP to opt out.` |
| Being Reviewed | `...is being reviewed by our team right now...` |
| Sold | `...enrolled! Your payout is being processed...` |
| Declined | `...could not be accepted this time...` |
| Paid | `...payout has been sent. Thank you...` |

A status you add later that the code doesn't know falls back to
`was updated to <status>`, so nothing breaks — it just reads generically until
you add a phrase to `STATUS_PHRASES`.

**Two things the code guarantees, which are easy to lose if you edit copy:**

Long referral names are trimmed rather than allowed to spill into a second
segment — the `Reply STOP` notice is never what gets cut, because it's required
for A2P/TCPA compliance.

Accented characters are folded to plain ASCII (`José Núñez` → `Jose Nunez`).
This isn't cosmetic: a single character outside the GSM-7 alphabet silently
re-encodes the whole message as UCS-2, where a segment is **70** characters
instead of 160. One `ú` in a name turns a 150-character text into three billed
segments. Given the client base here, that's a when, not an if.

---

## 3. Workflow: Referral Sold

**Trigger:** Contact Tag → `Tag` is `referral-sold`

**Settings:** Allow Re-Entry **ON**

**Actions:**

1. **Send Email** — subject `Your referral enrolled — congratulations`, body
   *Email B* below
2. **Remove Contact Tag** → `referral-sold`

No SMS here. The Status Update workflow already texts them the "enrolled!"
message in the same moment, and two texts landing together reads as a glitch.

### Email B — congrats

```
Hi {{contact.first_name}},

{{contact.referral_name}} enrolled. That's a real thing you did — someone you
know has health coverage now because you took two minutes to send their name
over.

Your payout is being processed. You'll get a text the moment it's sent, and you
can track it in your portal:
https://www.vshealthbenefits.com/client

If there's anyone else in your circle who's been putting off getting covered,
you know where to find us.

Thank you,
VS Health Benefits
(954) 825-1009
```

---

## 4. Test it

1. Sign in to the portal as a member and submit a referral with a real email and
   your own mobile.
2. Vercel log for `/api/portal-referral` — you want `referrerTagged: true`.
   `contactId` is the referred person; `referrerId` is the member.
3. You should get the internal SMS, and the member gets the thank-you email then
   SMS two minutes later.
4. In admin, move that referral through each status one at a time. Each change
   should produce one text.
5. Vercel log for `/api/referral-status` returns the exact message and its
   length, e.g. `{"ok":true,"status":"sold","smsLength":147,"tagged":true}` —
   useful for confirming copy without waiting for a phone.

### If the first status text arrives and later ones don't

The **Remove Contact Tag** step is missing from the end of the Status Update
workflow, or Allow Re-Entry is off. That's the failure mode this design has, and
it looks exactly like "the automation randomly stopped working."

### If nothing sends at all

Check `tagged` in the Vercel response. `false` means the workflow was never
started and the problem is upstream of GHL. `fieldWarning: "no_matching_custom_fields"`
means step 0 wasn't done — the tag fires but the SMS body is empty.

### SMS prerequisites

Same as the member welcome sequence: a provisioned number and **approved A2P
10DLC registration**. Emails work immediately; texts silently do nothing until
that clears.

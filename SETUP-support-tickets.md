# Support ticket system — setup

Someone submits the contact form → they get a ticket number on screen and by
email, you get a copy, and the ticket lands on the admin Support board.

```
contact.html form
  └─ POST /api/support-ticket
       ├─ 1. mint ticket number            VS-2THH68-VJQ
       ├─ 2. upsert contact in GHL + write the number to a custom field
       ├─ 3. note on the contact with the actual request
       ├─ 4. tag `support-ticket-created`        ◄── TRIGGER
       └─ 5. append to Firestore vs_state/contact_requests
                     │                              │
   workflow "Support Ticket Created" ───────────────┘   admin.html → Support board
     ├─ Email to the requester  (24-48 hour acknowledgement)
     ├─ Internal Notification → email to you
     └─ Remove tag `support-ticket-created`
```

This replaced `api/hubspot-ticket.js` in the contact form. That endpoint is still
in the repo but nothing calls it any more.

## About the ticket number

Format `VS-<6 time chars>-<3 random>`, e.g. `VS-2THH68-VJQ`.

The alphabet is `23456789ABCDEFGHJKMNPQRSTVWXYZ` — **no 0, 1, O, I or L**, because
these get read aloud on the phone and written on sticky notes, and "was that a
zero or an oh" costs real time.

The time half is seconds since 1 Jan 2026, so numbers keep increasing: a higher
ticket number always means a later ticket, and that holds for ~23 years. The
random tail gives 27,000 combinations per second, so simultaneous submissions
don't collide. Tested at 200 submissions in the same second with zero
collisions.

## 1. Create one custom field in GHL

Settings → Custom Fields → new **Contact** field:

| Field name | Type | Key it produces |
|---|---|---|
| Support Ticket Number | Text | `contact.support_ticket_number` |

Then tell me the field exists and I'll fetch its ID, or grab it yourself and set
it in Vercel as `GHL_CF_TICKET_NUMBER`.

Until that's set, the endpoint returns `fieldWarning: "no_ticket_number_field"`.
Everything else still works — the ticket number is minted, the board gets it,
the tag fires — but `{{contact.support_ticket_number}}` in the email will be
blank. This is the exact failure that bit us on the referral automation, so it's
worth doing before you publish the workflow.

## 2. Workflow: Support Ticket Created

**Trigger:** Contact Tag → `Tag` is `support-ticket-created`

**Settings (gear icon):** Allow Re-Entry **ON** — people submit more than once.

**Actions:**

1. **Send Email** → *Email A* below
2. **Internal Notification** → **Email** → your address → *Internal copy* below
3. **Remove Contact Tag** → `support-ticket-created`

Step 3 is what lets the next request fire. Skip it and the second ticket someone
opens will silently send nothing.

### Email A — to the person who submitted

From: `VS Health Benefits` / `info@vshealthbenefits.com`
Subject: `We got your request — ticket {{contact.support_ticket_number}}`

```
Hi {{contact.first_name}},

We received your request. Your ticket number is
{{contact.support_ticket_number}} — keep it handy if you need to follow up.

A team member will reach out to assist you within 24-48 hours.

If it's urgent, call us directly at (954) 866-6872 and reference your ticket
number.

Thank you,
VS Health Benefits
(954) 866-6872
```

### Internal copy — to you

**Internal Notification → Email**, to your own address.
Subject: `New support ticket {{contact.support_ticket_number}} — {{contact.first_name}} {{contact.last_name}}`

```
New support request.

Ticket:  {{contact.support_ticket_number}}
Name:    {{contact.first_name}} {{contact.last_name}}
Email:   {{contact.email}}
Phone:   {{contact.phone}}

The full message is on the contact record as a note, and the ticket is on the
Support board in the admin portal.

Promised response window: 24-48 hours.
```

## 3. Where tickets show up

**Admin portal → Support.** The ticket number appears on the board card, in the
detail modal, and in the bell notification. Stages are the existing
`new → in-progress → waiting-on-client → escalated → solved`.

**GHL contact record.** Tagged, with the ticket number in the custom field and
the full request as a note.

## 4. Test it

1. Submit the contact form at `/contact` with a real email.
2. On screen you should get the confirmation plus **Your ticket number: VS-…**
3. Vercel log for `/api/support-ticket`:

   ```json
   {"ok":true,"ticketNumber":"VS-2THH68-VJQ","contactId":"…","noted":true,"tagged":true,"boarded":true}
   ```

   - `tagged: false` → the workflow was never started, problem is upstream of GHL
   - `boarded: false` → it won't appear on the admin Support board; check `boardError`
   - `fieldWarning` present → step 1 isn't done, the email's ticket number will be blank

4. Check the admin Support board for the card, and your inbox for both emails.

## Note on deliverability

These acknowledgement emails are transactional and should land in Primary, but
until the sending domain is authenticated they may go to Promotions like the
referral email did. The fix is in the notes from that conversation: a dedicated
sending subdomain in GHL with SPF and DKIM, since the root domain's SPF
currently authorises Google Workspace only and says nothing about GHL.

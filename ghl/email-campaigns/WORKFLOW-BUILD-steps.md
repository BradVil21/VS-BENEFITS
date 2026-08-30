# Build the cold sequence workflow, step by step

The 22 contacts are already in GoHighLevel, tagged `smb-cold-fl`. This is the only
piece left that has to be built by hand.

Automation, Workflows, Create workflow, Start from scratch.
Name it **SMB Cold, Group Health, South FL**.

## Trigger

Add trigger, **Contact Tag**.

| Field | Value |
|---|---|
| Trigger name | Cold list tagged |
| Filter | Tag `is` `smb-cold-fl` |

That tag is already on all 22 contacts, so the moment you publish, they enroll. If you
want to stage it, publish first with the email steps still in draft, or unpublish until
you have test sent.

## Steps, in order

1. **Wait** — Wait for a specific day and time. Tuesday to Thursday, 9:00am to 2:00pm,
   America/New_York. Owners read email between jobs.
2. **Send Email** — template `SMB Cold 1`.
   From name: Bradley Vilsaint. From email: your verified sending address.
   Subject: `Health coverage for your team`
3. **Wait** — 3 days.
4. **If/Else** — branch condition: `Email Events` `Replied` is true, OR
   `Opportunity` created. If yes, go to the **Add Tag** step below and end.
5. **Send Email** — template `SMB Cold 2`.
   Subject: `Four ways to cover a team`
6. **Wait** — 4 days.
7. **If/Else** — same reply check.
8. **Send Email** — template `SMB Cold 3`.
   Subject: `Should I close your file?`
9. **Add Tag** — `smb-cold-complete`.

Exit branch from steps 4 and 7: **Add Tag** `smb-engaged`, then **Remove Tag**
`smb-cold-fl`, then end.

## Settings tab, do not skip

- **Stop on Response: ON.** This matters more than the branch logic. Nothing burns a
  prospect faster than follow up arriving after they already answered.
- **Allow re-entry: OFF.** Nobody should get this sequence twice.
- **Contact drip: ON, 50 per day.** With 22 contacts it changes nothing today, but it
  protects you when the list is 500.
- **Time window:** 9:00am to 5:00pm, weekdays only, America/New_York.

## Before you publish

Test send each template to yourself. Check the mobile view, confirm the unsubscribe
link resolves, and note which Gmail tab it lands in.

Then publish. 22 contacts is one day of warm-up volume, which is the right size.

## About "campaigns"

Marketing, Emails, Campaigns is for one-off broadcasts, not sequences. You do not need
one here: the workflow is what drives the three emails. If you would rather send just
email 1 as a single broadcast to the `smb-cold-fl` tag and handle follow ups manually,
that works too, but you lose the reply detection and the automatic stop.

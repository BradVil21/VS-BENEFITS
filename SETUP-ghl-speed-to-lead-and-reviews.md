# GHL setup: instant follow-up on web leads + Google reviews after every sale (Nov 11, 2026)

Two workflows, about 30 minutes to build. GHL workflows can't be created through the API,
so build them in the GHL UI: **Automation → Workflows → + Create Workflow → Start from scratch**.

What already exists (no changes needed):
- Every website form (calculator, /trucking-health-quote, /get-a-quote, /quote) posts to
  `/api/lead-sync`, which creates the GHL contact with the tag **`website-lead`** (plus source tags
  like `subsidy-calculator`).
- Forms already carry consent to call/text "including by automated technology".
- Marking someone Sold in admin fires your **GHL Sold webhook** (`event: lead_marked_sold`).
- Inbound calls are answered by the Voice AI agent (Amanda / Sarah prompt).

---

## Workflow 1: "Speed to lead: website"

**Trigger:** Contact Tag Added → tag is `website-lead`
**Settings:** Allow re-entry OFF. Stop on response ON (so a reply ends the drip and you take over).

| Step | Action | Details |
|---|---|---|
| 1 | Send SMS (immediately) | Message A below |
| 2 | If/Else: business hours? | Mon–Fri 8 AM–8 PM ET (Sat 9–1 if you work Saturdays) |
| 3a | **In hours:** Call (Voice AI outbound) *or* Internal call connect | Wait 1 minute, then call. If you use **Voice AI → Outbound call action**, assign the Sarah agent with the "Outbound web lead" opening below. If not available on your plan, use **Call → connect to user (Bradley)** so your phone rings first and bridges to the lead. |
| 3b | **After hours:** Wait until next business day 8:05 AM, then step 3a |
| 4 | Create Task + Notify (SMS to you) | "New web lead: {{contact.name}} {{contact.phone}}, source {{contact.source}}. Call within 5 min." |
| 5 | Wait 10 min → If no reply and call not answered → Send SMS | Message B |
| 6 | Wait 1 day → Send SMS | Message C |
| 7 | Wait 2 days → Send Email | Email D |
| 8 | Wait 3 days → Send SMS | Message E (final) |

**Message A (instant)**
> Hi {{contact.first_name}}, it's Bradley's team at VS Health Benefits. Got your request. A licensed
> advisor will call you in a few minutes from 954-825-1009. Is now a good time? Reply STOP to opt out.

**Message B (missed call)**
> Just tried you, {{contact.first_name}}. When's a better time today? Or book a quick 15-min call:
> {{calendar_link}}

**Message C (day 1)**
> {{contact.first_name}}, your quote is ready to go. Most of our clients (truckers and self-employed) are
> surprised what they qualify for. Want me to text you the numbers or call?

**Email D (day 3), subject:** Your health insurance quote
> Hi {{contact.first_name}}, I didn't want your request to fall through the cracks. Open enrollment ends
> Jan 15, and Dec 15 is the deadline for Jan 1 coverage. Reply with a good time, or book here:
> {{calendar_link}}. Bradley Vilsaint, VS Health Benefits

**Message E (day 6, final)**
> Last check-in, {{contact.first_name}}. Should I keep your quote open or close your file? Just reply KEEP
> or CLOSE.

**Voice AI: "Outbound web lead" opening** (add to the Sarah agent as a separate outbound agent/prompt)
> Hi, is this {{contact.first_name}}? This is Sarah, the virtual assistant with VS Health Benefits.
> You just requested a health insurance quote on our website. I'm an AI assistant calling to get you to
> a licensed advisor. Do you have two minutes now?

Then follow the existing Sarah rules: live transfer during hours, otherwise book the 15-minute call.
Keep the AI disclosure in the first line. The FCC treats AI-generated voices as "artificial voice"
under the TCPA. Your form says "automated technology". To be safe, change it on all four forms to
"including by automated technology, prerecorded or AI-generated voice". (I'm not a lawyer;
have your compliance contact confirm.)

---

## Workflow 2: "Sold → Google review"

**Trigger:** Inbound Webhook (the same one your admin Sold button already hits), filtered to
`event = lead_marked_sold`. Or, if that workflow already exists, add these steps to the end of it.

| Step | Action | Details |
|---|---|---|
| 1 | Add tag | `sold-review-request` |
| 2 | Wait 2 days | Gives time for the ID card / welcome call |
| 3 | Send SMS | Review message 1 |
| 4 | Wait 3 days → If tag `reviewed` not present → Send SMS | Review message 2 |
| 5 | Wait 7 days → If still not reviewed → Send Email | Short email with the same link |

Your Google review link: **https://g.page/r/CTz8LoxJRazwEBM/review**
(Confirm it opens the "write a review" box for VS Health Benefits before turning the workflow on.)

**Review message 1**
> {{contact.first_name}}, congrats, you're covered! 🎉 Quick favor: would you leave us a Google review?
> It takes 30 seconds and helps other drivers and families find us: https://g.page/r/CTz8LoxJRazwEBM/review

**Review message 2**
> Hi {{contact.first_name}}, just a reminder in case it got buried. A quick review would mean a lot:
> https://g.page/r/CTz8LoxJRazwEBM/review. Thank you!

When someone posts a review, add the tag `reviewed` (manually, or via **Reputation Management**
if it's on your plan; it can auto-match reviewers). Ask on every sale, never offer anything
in exchange for a review (Google policy), and don't only ask happy customers ("review gating").

Also: Reputation Management → Review requests → turn on **"Send review request on opportunity
won"**. It's a simple backup if a sale ever skips the admin Sold button.

---

## Test before turning on
1. Submit the calculator with your own cell. You should get Message A within seconds and a call
   within ~1 minute.
2. Mark a test client Sold in admin, then check the contact gets `sold-review-request` and the
   SMS 2 days later (set the wait to 1 minute while testing).
3. Turn waits back to normal and publish.

# Why the bot wasn't booking — root cause, corrected

Bradley was right that Appointment Booking is set up. My earlier note said the
action wasn't wired up; that was wrong, and this replaces it.

There were **two** separate problems stacked on top of each other, and either
one alone would have stopped a booking.

---

## Problem 1 — the prompt told the bot it could not book. FIXED.

The **Personality** field on the agent still held GoHighLevel's stock template
text, which had never been edited. Verbatim:

> "You are a bot for {{ai.business_name}}, tasked to assist customers. Your
> primary goal is to build trust and help out the customers by referencing our
> wiki.
>
> **You cannot help with appointment bookings, appointment cancellations,
> rescheduling; politely let the customer know you cannot help them with
> appointment...**"

Your real prompt — "You are Vee, the virtual assistant for VS BENEFITS LLC…" —
was sitting further down in **Additional Information**. Personality is the
higher-priority instruction, so the bot did exactly what it was told: it
refused, politely, every time. That is why my live test got *"While I can't book
appointments directly…"* rather than an error.

**Fixed and verified.** Personality now states the bot can book, describes the
sequence you asked for, and carries the guardrails (no premiums, no plan
recommendations, and no SSN, date of birth, payment details or medical history).
Saved at 09:07 on 28 Aug — "Bot Updated Successfully".

Retested immediately in the built-in tester:

| | Before | After |
|---|---|---|
| "I'd like to book an appointment" | "While I can't book appointments directly…" then asked for **date of birth** | **"Absolutely, I can help with that! First, could you please share your phone number so I can confirm it for our advisor team?"** |
| Gave a phone number | — | **"Just to confirm, your phone number is 954-555-0142. Will you be able to answer when an advisor calls you? Also, what timezone are you in?"** |

Phone read back, will-you-answer, and timezone — three of your four asks, in one
message, and no DOB.

---

## Problem 2 — there is no calendar to book into. STILL OPEN.

This is the remaining blocker, and it is a five-minute job.

Opening the Appointment Booking action, the **"Pick a calendar"** dropdown
returns **"No Data"**. Checking Settings → Calendars confirms why:

> **All calendars (0) — "No calendars yet – set one up!"**

The screenshot you sent is the **Connections** tab: your Google account and
Calendly *linked to GHL* so it can sync events and check conflicts. That part is
working — the calendar view is full of your real appointments. But a linked
account is not a bookable calendar. GHL treats them as two different objects:

- **Connections** — external accounts GHL reads and writes. You have these.
- **Calendars** — the bookable thing, with a duration, availability and a
  booking window. The bot books into one of these. You have none.

So the action has nothing to point at, which is why **Total Appointment Booked
is 0** for all of August despite 8 contacts and 9 actions triggered.

### To finish it

Settings → Calendars → **New calendar**, then:

| Setting | Value |
|---|---|
| Name | **VS Health Benefits** |
| Type | Simple / one-on-one |
| Duration | 30 minutes |
| Meeting location | Phone call — advisor calls the contact |
| Booking window | 60 days ahead |
| Minimum notice | 4 hours |
| Availability | Mon–Fri 8:00am–6:00pm, Sat–Sun 8:00am–1:00pm |
| Timezone | America/New_York |
| Team notification | **On → you.** This is your booked-appointment alert. |

Then reopen the bot's **Appointment Booking** action and select it — the
dropdown will have something in it once the calendar exists.

Your Google calendar is already attached as a conflict calendar, so real
appointments will block slots automatically. Calendly stays untouched on /book.

---

## Two other things worth a look

**The bot answers on six channels, not just webchat.** Bot Settings shows SMS,
Instagram, Facebook, Chat Widget, Live Chat and WhatsApp, on Auto-Pilot. You
said webchat only. An AI answering inbound SMS in health insurance is a wider
risk surface than a chat widget, and it is worth deciding deliberately rather
than by default.

**It introduces itself as "Amanda" but your prompt names it "Vee."** The live
widget said *"[ Amanda has connected ]"*. Cosmetic, but confusing for a lead who
then gets an email from someone else.

---

## Retest once the calendar exists

- [ ] Ask to book — it should ask for a day and time, then say it is checking
- [ ] Give a slot you know is free — it should book without asking twice
- [ ] Give a slot you know is taken — it should offer real alternatives
- [ ] Refuse three times — it should stop and take a callback window instead
- [ ] Say you are in Arizona — confirmation must come back in Mountain time
- [ ] Confirm the booking notification actually reaches you
- [ ] Test after 6pm ET — it should say first thing in the morning

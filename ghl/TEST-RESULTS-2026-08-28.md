# Live webchat test — 28 August 2026, 08:53–08:56 ET

Run against the real widget on `/cobra-alternatives`, in business hours
(Friday, ~8:55am ET, inside Mon–Fri 8–6). Contact created as **"Claude Testcase"**
— please delete it from Contacts.

The bot is live and answering as **"Amanda"**. It is articulate and on-topic.
It also cannot do any of the four things you asked for.

---

## What happened

| Step | What I sent | What the bot did |
|---|---|---|
| 1 | Lost my job, COBRA too expensive, can someone call me | Sympathised, offered an advisor callback, asked for first and last name |
| 2 | "Claude Testcase" | Asked what brings you here — **a question I had already answered in message 1** |
| 3 | "I lost coverage when I was laid off. I'd like to book an appointment" | **"While I can't book appointments directly, I can collect your information…"** then asked for my **date of birth** |

---

## Finding 1 — the bot cannot book. This is the blocker.

Verbatim: *"While I can't book appointments directly, I can collect your
information so a licensed VS Health Benefits advisor can reach out to you."*

So none of the flow you described can run yet — not the availability check, not
the "please hold while I check", not the three retry rounds, not the auto-book,
and therefore not the booked-appointment notification either.

The calendar side is fine. Your screenshot shows Google linked and Calendly
attached as a conflict calendar, which is exactly right. What is missing is the
**booking action wired into the bot** — in GHL that is the calendar/booking tool
being enabled on the AI agent and pointed at the VS Health Benefits calendar.
Until that is switched on, the bot will keep saying it cannot book, no matter
what the prompt says.

**This one is not a prompt problem and I could not fix it from the prompt side.**

## Finding 2 — it asked for date of birth. Turn this off.

The bot asked for my **date of birth** in an unauthenticated public chat widget,
three messages into a first conversation, from someone it had no relationship
with.

That is personal data you do not need to book a phone call, collected over a
channel that is not the right place for it, in a health insurance context. It
also trains people to hand DOB to whatever chat window asks. The prompt in
`webchat-bot-prompt.md` explicitly forbids DOB, SSN, payment details and medical
history for this reason — an advisor takes those on the call.

## Finding 3 — it never asked the things you actually wanted

Across the whole conversation the bot never once:

- asked for a phone number
- read a number back to confirm it was correct
- asked whether they would answer when an advisor calls
- asked what time of day was best
- asked what timezone they were in

It went name → reason → date of birth. That is the current prompt, and it is
what the new one replaces.

## Finding 4 — minor: it repeats itself

I opened by saying I had lost my job. Its second message asked whether I had
lost coverage. Small, but it reads as not listening, and it costs a turn.

---

## What to change, in order

1. **Enable the booking action on the AI agent** and point it at the VS Health
   Benefits calendar. Nothing else on your list works until this is done.
2. **Replace the prompt** with `ghl/webchat-bot-prompt.md`. That fixes findings
   2, 3 and 4 in one paste — it removes the DOB ask, adds the phone confirmation
   and callback questions, and carries the booking sequence you described:
   ask for day and time → say "let me hold on one second and check what's open"
   → book immediately if free → offer real alternatives if not → **maximum three
   more rounds**, then stop and fall back to a callback.
3. **Create the four contact fields** so the answers have somewhere to land.
4. **Re-test.** Same way I did: open the widget on any page, ask to book, and
   check that it holds, checks, and books without asking permission twice.

## Retest checklist

- [ ] Give it a 9-digit number — it should notice and ask again
- [ ] Say you are in Arizona — the confirmation must come back in Mountain time
- [ ] Ask for a slot you know is taken — it should offer real alternatives
- [ ] Refuse three times — it should stop offering and switch to a callback
- [ ] Volunteer your date of birth unprompted — it should not repeat it or follow up
- [ ] Book successfully — check the notification actually reaches you
- [ ] Test again after 6pm ET — it should say first thing in the morning

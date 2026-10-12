# LinkedIn post — GHL lead generator prompt

## OPTION A — Post with the prompt inside (fits LinkedIn's 3,000-character limit)

Most small businesses don't have a lead problem. They have a leak problem.

People start your quote form, get distracted, and leave. You never know they were there.

So I rebuilt how leads come in at VS Health Benefits, using GoHighLevel + Claude. Now:

📞 The form asks for ZIP + phone FIRST, so even a half-finished quote is a lead I can call
🔁 Every lead lands in GHL as ONE contact. Finishing the form later updates it, no duplicates
🧭 Every lead shows where it came from: Google, ads, referral, and the page they landed on
🤖 An AI chat books calls straight onto my GHL calendar
📬 Old leads get a 30-day plain-text follow-up that stops the moment they reply

I didn't write this from scratch. I described it to Claude, one piece at a time.

Here's the prompt to build your own version. Copy it, fill in the brackets:

---
Act as a GoHighLevel automation architect. I run [BUSINESS] serving [CUSTOMERS]. My site is on [WEBSITE PLATFORM].

Build a lead capture system that loses zero leads:

1. Multi-step quote form. Ask for the phone number (plus ZIP or a key qualifier) on step 1–2, and name/email last.
2. Capture partial leads. Once a valid phone is entered, send it to GHL as a contact tagged "form-in-progress," including if they leave the page.
3. Dedupe. On submit, upsert the same contact by phone, then email. Swap the tag to "website-lead" and create an opportunity in [PIPELINE / STAGE].
4. Attribution. Save first- and last-touch source (UTMs, click IDs, referrer, landing page) for 90 days and attach it to every lead.
5. Tracking. Fire GA4 events for phone clicks, form starts, each step completed, and submissions.
6. AI chat. A Conversation AI bot that answers FAQs, collects phone + best time, and books onto my GHL calendar.
7. Nurture. A workflow for cold leads: 4 plain-text emails over 30 days, stop on reply, weekdays only.

For each part, give me the exact GHL click-path, any code, and a test to prove it works. Keep API tokens server-side and ask me questions before you assume.
---

Small business. Big-company follow-up. That's the standard.

If you try it, drop a comment and tell me what you built. I read every one.

#GoHighLevel #ClaudeAI #Automation #LeadGeneration #SmallBusiness #AI


---

## OPTION B — Short post + "comment PROMPT" giveaway (more comments = more reach)

Post this, then DM the full prompt below to everyone who comments.

Most small businesses don't have a lead problem. They have a leak problem.

People start your quote form, get distracted, and leave. You never know they existed.

I rebuilt how leads come in at VS Health Benefits with GoHighLevel + Claude:

📞 Phone number asked FIRST, so a half-finished form is still a lead I can call
🔁 One contact per person. No duplicates, no lost history
🧭 Every lead tagged with where it came from and what page they read
🤖 AI chat that books calls onto my calendar
📬 Old leads get a 30-day follow-up that stops the second they reply

I wrote the whole thing as one Claude prompt you can reuse for any business.

Comment "PROMPT" and I'll send it to you.

#GoHighLevel #ClaudeAI #Automation #LeadGeneration #SmallBusiness

---

## THE FULL PROMPT (send this to people who comment)

You are a senior GoHighLevel (GHL) automation architect and web developer. Help me build a lead capture system for my business that loses zero leads. Before you start, ask me any questions you need answered. Then build it one part at a time. For each part, give me:
(a) the exact GHL click-path,
(b) any code, with every token and secret kept server-side, never in the browser,
(c) a test I can run to prove it works.

ABOUT ME
- Business: [BUSINESS NAME] — [WHAT YOU SELL] to [WHO YOU SERVE] in [AREA]
- Website: [PLATFORM, e.g. custom HTML on Vercel / WordPress / GHL funnels]
- GHL: [SUB-ACCOUNT NAME], pipeline "[PIPELINE]", first stage "[STAGE]"
- Hours: [HOURS + TIME ZONE]
- Main offer / call to action: [e.g. free quote, free consultation]

PART 1 — A QUOTE FORM THAT DOESN'T LEAK
- Make the form multi-step with a progress bar.
- Order the steps: [ZIP / KEY QUALIFIER] → phone → [2–3 QUALIFYING QUESTIONS] → name + email last.
- Validate each step before moving on, with friendly error messages.
- Show a clear consent line under the phone field (TCPA-friendly).

PART 2 — CAPTURE PARTIAL LEADS
- As soon as a valid phone (or email) exists, POST it to a server endpoint. The endpoint upserts a GHL contact tagged "form-in-progress" and records the last step completed.
- Also send a beacon when the visitor leaves the page (pagehide / visibilitychange). On mobile, that is often the only event that fires.
- Validate and length-cap every field on the server. Allow requests from my domain only.

PART 3 — ONE PERSON = ONE CONTACT
- On final submit, upsert the SAME contact by phone first, then email.
- Remove "form-in-progress" and add "website-lead" plus a tag for the source form.
- Create or update an opportunity in [PIPELINE] at [STAGE], with a note summarizing the answers.
- If a person recalculates or resubmits, update their record. Never create a duplicate.
- If the GHL call fails, the visitor still sees success, and the error is logged.

PART 4 — KNOW WHERE EVERY LEAD CAME FROM
- On first visit, store the UTM tags, gclid/fbclid, referrer and landing page for 90 days (first-party, no third-party cookies).
- Store the last touch separately.
- Label search-engine referrers as "organic search."
- Attach both touches automatically to every form POST, so future forms are covered without extra work.
- Map them to GHL custom fields: [FIELD NAMES].

PART 5 — TRACK WHAT MATTERS
- Send GA4 events: phone_click (tel: links), chat_open, quote_cta, quote_start, quote_step (with step number), and generate_lead.
- Show me how to mark generate_lead and phone_click as Key Events. Show me how to paste Google Ads conversion labels so ads can optimize.
- Load analytics only after cookie consent.

PART 6 — AI CHAT THAT BOOKS CALLS
- Write the instructions for a GHL Conversation AI bot on Live Chat only: answer FAQs about [TOPICS], collect phone + best time to call + time zone, and book onto a GHL-native calendar ([LENGTH]-minute phone call, [HOURS]).
- Confirm times in the visitor's time zone. Hand off to a human on anything sensitive.
- Create the custom fields the bot writes to.

PART 7 — FOLLOW-UP THAT FEELS HUMAN
- Speed-to-lead workflow: text + email within 5 minutes of "website-lead," and a task for me to call.
- Aged-lead workflow triggered by the tag "[AGED TAG]": 4 short plain-text emails on days 1, 3, 12 and 30. Write the copy in my voice, with lowercase subjects and no links or images.
- Settings: stop on reply, no re-entry, weekdays 8–5 in the contact's time zone. At the end, add the tag "[AGED TAG]-completed."

PART 8 — PROVE IT
- Give me an end-to-end test script: a partial form, a full form, a duplicate attempt, a chat booking, and a nurture test on my own contact.
- For each test, tell me exactly what I should see in GHL and GA4.

Keep your explanations plain-English. I'm a business owner, not a developer.

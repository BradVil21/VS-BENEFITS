# VS Health Benefits — Restaurant sequence templates for GoHighLevel

Five files. Each one is a complete email body: 600px table, every style inline,
no `<style>` block, no external CSS, no web fonts, no images, one link, CAN-SPAM footer.

## Before the first send

1. Settings → Email Services → Reply & Forward. Set the forwarding address and
   turn on **Forward to assigned user**. Replies are the whole point of this sequence
   and right now they land only in Conversations.
2. From Name on every step: **Bradley Vilsaint** — not VS Health Benefits.

## How to load each one

Marketing → Emails → Templates → New → **Code your own** → paste the file contents → Save.

Do not open it in the drag-and-drop builder afterward. It rewrites the markup into
nested tables that collapse on a phone.

Then in the workflow email action, set three fields:

- **From Name** — Bradley Vilsaint
- **Subject** — from the table below
- **Pre-Header** — from the table below (this field is currently empty on everything you have)

## The five

| # | File | Send | Subject | Pre-Header |
|---|------|------|---------|------------|
| 1 | `01-no-group-plan.html` | Day 0, Tue | `you don't need a group plan` | `Part-timers count. No group plan, no participation minimum.` |
| 2 | `02-started-from-zero.html` | Day 3, Fri | `never offered anything before?` | `Most restaurants that start one are starting from zero, not switching.` |
| 3 | `03-what-one-cook-costs.html` | Day 7, Tue | `what one line cook costs you` | `Cornell puts replacing one restaurant employee near $5,900.` |
| 4 | `04-dec-15-not-jan-15.html` | Day 12, Wed | `dec 15, not jan 15` | `Miss it and the earliest start becomes February 1.` |
| 5 | `05-should-i-close-your-file.html` | Day 18, Thu | `should i close your file?` | `A no is a fine answer. It saves us both the follow-up.` |

Send windows: 9:30–10:45am or 2:30–4:00pm. Never 11:30–2:00 or after 5.

## Find and replace before you send

Every file contains these. Search each template after pasting:

The phone number is already filled in: **(954) 825-1009** in every signature, and
`sms:+19548251009&amp;body=HEADCOUNT` behind the text buttons in files 2 and 3. That href
opens a pre-filled text on a phone and does nothing on desktop, which is fine.

The Calendly link is in too, on the buttons in files 1 and 4:
`https://calendly.com/bvilsaint-vshealthbenefits/vs-health-benefits`

The CAN-SPAM footer on all five reads:
**VS Health Benefits, 7901 4th St N Ste 300, St. Petersburg, FL 33702**

Nothing left to fill in but one thing to verify:

| Field | What to check |
|---|---|
| `{{unsubscribe_link}}` | Send a test. If it renders as literal text instead of a working link, swap in whichever unsubscribe merge field your account uses. The footer link is the CAN-SPAM requirement, so it has to resolve. |

## What's deliberate, so you don't "fix" it

- **No header image and no logo bar.** The first thing on screen is the idea, not a
  banner. Two reasons: a branded header is the visual signature of bulk mail, to the reader
  and to Gmail's tab sorting; and where images don't load — Outlook desktop for unknown
  senders, anyone who has turned them off — a grey box sits where your first sentence
  should be. On a 320px screen a banner also pushes the whole offer below the fold.
- **One link per email.** The button is the *second* option; the real ask is the bolded
  question above it. Adding a second link measurably cuts replies.
- **File 5 has no button on purpose.** A breakup email with a booking button reads as a
  campaign, which defeats the reason that email works.
- **No `{{contact.first_name}}` anywhere.** Scraped restaurant lists are full of "Info"
  and "Manager." One wrong name kills a cold email faster than no name at all.
- **Lowercase subject lines.** Title Case reads as a campaign. Lowercase reads as typed
  by a person, which is the premise of the whole sequence.

## Test before you schedule

Send yourself each one and read it on your actual phone with images turned off.
If you can't understand the offer without loading images, something got edited.

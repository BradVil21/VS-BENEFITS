# GHL webchat build spec — VS Health Benefits

Location `cNCy6JUURpb4eBDdb9bU` · timezone America/New_York
Live Chat widget `6a8339a143b7e14560ca7528` — already on 219 pages
Hours: **Mon–Fri 8:00am–6:00pm ET, Sat–Sun 8:00am–1:00pm ET**

Status: **step 4 is done.** Steps 1–3 are the click-through below.

---

## 1. Custom fields

Settings → Custom Fields → **Create field**. Object = **Contact** only
(it is a multi-select — make sure Opportunity is *not* ticked). Folder =
Additional Info.

| Field name | Type | Options |
|---|---|---|
| **Best Time to Call** | Single line | — |
| **Timezone** | Single option | Eastern, Central, Mountain, Pacific, Alaska, Hawaii |
| **Phone Verified** | Single option | Yes, No |
| **Will Answer Call** | Single option | Yes, No, Unsure |

Keys come out as `contact.best_time_to_call`, `contact.timezone`,
`contact.phone_verified`, `contact.will_answer_call`. The bot prompt already
refers to them by those names.

---

## 2. Calendar

Calendars → **Create calendar** → Event type **Round Robin** or **Simple**
(one advisor = Simple is fine).

Mirror the Calendly event exactly:

| Setting | Value |
|---|---|
| Name | **VS Health Benefits** |
| Duration | 30 minutes |
| Meeting location | **Phone call** — advisor calls the contact |
| Booking window | 60 days into the future |
| Minimum notice | 4 hours |
| Availability | Mon–Fri 8:00am–6:00pm, Sat–Sun 8:00am–1:00pm |
| Calendar timezone | America/New_York |
| Slot interval | 30 min |

Then **Notifications & Additional options**:
- Contact gets confirmation + reminder (email and SMS)
- **Team notification on → you.** This is the "I get told when someone books"
  piece, and it only works on a GHL-native calendar, which is why we built one
  rather than embedding Calendly.

Calendly keeps running untouched on `/book` — nothing about this breaks it.

---

## 3. The bot

Settings → **AI Agents / Conversation AI** → your bot.

- **Channel: Live Chat only.** Do not enable SMS or email — you asked for
  webchat only, and an AI answering inbound SMS is a different risk profile.
- Paste the prompt from **`ghl/webchat-bot-prompt.md`** into the instructions.
- Under actions/tools, enable **booking** and point it at the *VS Health
  Benefits* calendar from step 2.
- Map the four fields from step 1 so the bot can write to them.
- Set the bot to hand off to a human on anything it flags.

Test it yourself in the widget before switching it live: give it a bad phone
number and check it asks again, then say you're in Arizona and check it
confirms the slot in Mountain time rather than Eastern.

---

## 4. Web traffic tracking — DONE

GHL's external tracking script is now on **219 pages**, immediately before
`</body>`:

```html
<script src="https://link.msgsndr.com/js/external-tracking.js"
        data-tracking-id="tk_e89392b2cfc34b548ae43b1ea975ae50"></script>
```

Excluded `admin.html` and `client.html` — internal tools, no reason to track.

What this gets you: GHL attributes sessions, sources and page paths to
contacts, so a lead record shows what they read before they converted, and
Attribution Reporting starts populating.

What it is **not**: a replacement for GA4. It is contact-level attribution, not
traffic analytics. Your GA4 property (G-Z6EVXL76GG) is still the place to look
at sessions, pages and search traffic. Keep both.

After deploying, check Settings → External Tracking → **Troubleshoot** — it
will confirm it is receiving hits from vshealthbenefits.com.

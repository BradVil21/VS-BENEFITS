# Restaurant Cold — Reply Sequence
## GoHighLevel workflow build sheet

Location: VS HEALTH BENEFITS · `cNCy6JUURpb4eBDdb9bU`
Build time: about 25 minutes once the five templates are loaded.

---

## Step 1 — Load the five templates first

Marketing → Emails → Templates → **New** → **Code your own**.
Paste each file, name it exactly as below, save.

| Template name to use | File |
|---|---|
| `Restaurant 1 — no group plan` | `01-no-group-plan.html` |
| `Restaurant 2 — started from zero` | `02-started-from-zero.html` |
| `Restaurant 3 — what one cook costs` | `03-what-one-cook-costs.html` |
| `Restaurant 4 — dec 15 not jan 15` | `04-dec-15-not-jan-15.html` |
| `Restaurant 5 — close your file` | `05-should-i-close-your-file.html` |

The names matter — you'll pick them from a dropdown in the workflow and they sort in order.

---

## Step 2 — Create the workflow

Automation → Workflows → **Create workflow** → **Start from scratch**.

Name it: **Restaurant Cold — Reply Sequence**

---

## Step 3 — Trigger

**Add New Trigger** → **Contact Tag**

- Trigger name: `Tagged restaurant-cold`
- Filter: **Tag** · `is` · `restaurant-cold`
- Tag Update Type: **Added**

You import a list, apply the tag in batches, and that's how people enter. Nothing enters
on its own. Keep batches to 40–50 a day.

---

## Step 4 — Settings (do this before adding steps)

Open the **Settings** tab at the top of the workflow builder.

| Setting | Value | Why |
|---|---|---|
| **Stop on Response** | **ON**, Email | This is the most important switch in the build. The second someone replies, they drop out of the sequence. Without it, a guy who answers email 1 still gets the breakup email on day 18. |
| Allow Multiple Opportunities / Re-entry | **OFF** | Nobody should run the sequence twice. |
| Timezone | **Account timezone** (America/New_York) | Your whole list is Pinellas and Hillsborough. |

Then open **Execution window** (sometimes shown as "Set Time Window"):

- Window: **9:30 AM to 10:45 AM**
- Days: **Tuesday, Wednesday, Thursday** only

That's the pre-lunch slot. Anything queued outside the window waits for the next
allowed morning, which is exactly what you want — it also spaces sends out naturally.

---

## Step 5 — The steps, in order

Add these nine actions top to bottom.

### 1. Send Email
- Action name: `E1 — no group plan`
- From Name: **Bradley Vilsaint** *(not VS Health Benefits)*
- From Email: your sending address
- Subject: `you don't need a group plan`
- **Pre-Header**: `Part-timers count. No group plan, no participation minimum.`
- Template: `Restaurant 1 — no group plan`

### 2. Wait
- **3 days**

### 3. Send Email
- Action name: `E2 — started from zero`
- Subject: `never offered anything before?`
- Pre-Header: `Most restaurants that start one are starting from zero, not switching.`
- Template: `Restaurant 2 — started from zero`

### 4. Wait
- **4 days**

### 5. Send Email
- Action name: `E3 — what one cook costs`
- Subject: `what one line cook costs you`
- Pre-Header: `Cornell puts replacing one restaurant employee near $5,900.`
- Template: `Restaurant 3 — what one cook costs`

### 6. Wait
- **5 days**

### 7. Send Email
- Action name: `E4 — dec 15`
- Subject: `dec 15, not jan 15`
- Pre-Header: `Miss it and the earliest start becomes February 1.`
- Template: `Restaurant 4 — dec 15 not jan 15`

### 8. Wait
- **6 days**

### 9. Send Email
- Action name: `E5 — close your file`
- Subject: `should i close your file?`
- Pre-Header: `A no is a fine answer. It saves us both the follow-up.`
- Template: `Restaurant 5 — close your file`

The waits are 3 / 4 / 5 / 6 days, which lands the sends on day 0, 3, 7, 12 and 18.

### Optional tail — 10 and 11
- **Wait 2 days**
- **Remove Contact Tag**: `restaurant-cold` · **Add Contact Tag**: `rest-sequence-complete`

That keeps the tag clean so you can re-tag the same list in the spring without
anyone double-entering.

---

## Step 6 — The second workflow, and don't skip it

The sequence generates replies. This is what makes sure you see them within the hour.

Automation → Workflows → **Create workflow** → name it **Restaurant — Reply Handler**

**Trigger:** `Customer Replied` — Reply Channel: **Email**
Add a filter so it only fires for this audience: **Contact Tag** `is` `restaurant-cold`.

**Steps:**
1. **Add Contact Tag** → `rest-ichra-replied`
2. **Remove Contact Tag** → `restaurant-cold`
3. **Internal Notification** → Email and SMS to you. Subject: `REPLY — {{contact.name}}`
4. **Create Task** → assigned to you, due **in 1 hour**, title: `Reply to {{contact.name}} — restaurant sequence`

The reply scripts are on the sequence page. Answer speed converts better than
anything in the copy.

---

## Step 7 — Before you publish

1. Settings → Email Services → **Reply & Forward**. Forwarding address set, "Forward to
   assigned user" ON. Replies currently land only in Conversations.
2. Send yourself a test of each email. Read it on your phone with images off.
3. Check the unsubscribe link resolves — if `{{unsubscribe_link}}` renders as literal
   text, swap in your account's field. That link is the CAN-SPAM requirement.
4. Publish the workflow, then tag **five contacts**, not five hundred. Watch what
   happens for two days before you open the tap.

---

## Tag reference

| Tag | Meaning |
|---|---|
| `restaurant-cold` | Entry tag. You apply it. Removed when they reply or finish. |
| `rest-ichra-replied` | Replied to anything. Stop all sequence mail, go one-to-one. |
| `never-offered` | Told you they've never offered coverage. Your best segment. |
| `rest-turnover-pain` | Named a number of people they lost. Use it as your opener. |
| `oe-2027-live` | Wants January 1 coverage. Moves to the December workflow. |
| `check-back-spring` | Timing no. Quarterly list, not weekly. |
| `do-not-contact` | Honor immediately. |
| `rest-sequence-complete` | Finished all five, never replied. |

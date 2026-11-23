# GoHighLevel: Dental / Vision workflows

Two workflows, both started by a tag the website adds automatically:

| Tag | Added when | Workflow |
|---|---|---|
| `dental-vision-partial` | They typed a phone number but have not finished the form | **Dental/Vision: Unfinished Quote** |
| `dental-vision-quote` | They pressed "Get My Free Quote" | **Dental/Vision: Quote Submitted** |

**Pipeline is already handled by the website code.** Every dental/vision lead gets an
opportunity in **Marketing Pipeline > New Lead** the moment the phone number comes in, and
lands in the admin portal's **Pipeline > New Lead** column (business and family alike). It
never moves a lead that is already past New Lead. Step 2 in each workflow below is a backup
in case the API token is missing the opportunities permission (see "Check" at the bottom).

Go to **Automation > Workflows > + Create workflow > Start from scratch** for each one.

---

## Workflow 1: Dental/Vision: Quote Submitted

**Settings (gear icon):** Allow re-entry OFF. Stop on response OFF.

**Trigger:** Contact Tag > Tag added > `dental-vision-quote`

**Actions, in order:**

1. **Remove Contact Tag** > `dental-vision-partial`
   (this ends the "Unfinished Quote" workflow for them)
2. **Create/Update Opportunity**
   - Pipeline: Marketing Pipeline
   - Stage: New Lead
   - Opportunity name: `Dental/Vision - {{contact.name}}`
   - Allow duplicate opportunities: OFF
   - Allow opportunity to move to any previous stage: OFF
3. **Internal Notification > SMS** to you:
   `New Dental/Vision quote: {{contact.name}}, {{contact.phone}}, ZIP {{contact.postal_code}}. Source: {{contact.source}}`
4. **Add Task**
   - Title: `Call {{contact.first_name}} about dental/vision quote`
   - Assign to: Bradley. Due: 1 hour.
5. **Send Email** to contact
   - Subject: `Your dental & vision quote, {{contact.first_name}}`
   - Body:
     ```
     Hi {{contact.first_name}},

     Thanks for requesting a dental and vision quote. I'm comparing plans from
     carriers like Ameritas, Guardian, MetLife, VSP and EyeMed for your ZIP code now.

     I'll call you from (954) 866-6872 shortly to go over your options. If you'd
     rather pick a time, just reply to this email.

     Bradley Vilsaint
     VS Health Benefits
     ```
6. **If/Else** > Condition: Contact Tag > Includes > `sms-opt-in`
   - **Yes branch > Send SMS:**
     `Hi {{contact.first_name}}, it's Bradley at VS Health Benefits. Got your dental & vision quote request. I'll call you shortly from this number. Reply STOP to opt out.`
   - **No branch:** nothing (they did not agree to texts).
7. **Wait** > 1 day
8. **If/Else** > Condition: Opportunity > Pipeline stage > is > New Lead (Marketing Pipeline)
   - **Yes branch > Send Email:**
     Subject: `Quick question about your dental & vision quote`
     Body: `Hi {{contact.first_name}}, I tried to reach you about your quote. When is a good time for a 5 minute call? You can reply here or call/text (954) 866-6872. Bradley`
   - **No branch:** end.

Save > toggle **Publish** > Save.

---

## Workflow 2: Dental/Vision: Unfinished Quote

**Settings:** Allow re-entry OFF.

**Trigger:** Contact Tag > Tag added > `dental-vision-partial`

**Goal event (add from the top of the builder):** Contact Tag added > `dental-vision-quote`
(the moment they finish, they leave this workflow)

**Actions, in order:**

1. **Wait** > 15 minutes (gives them time to finish the form)
2. **If/Else** > Contact Tag > Includes > `dental-vision-quote`
   - **Yes branch:** end (they finished; Workflow 1 has them).
   - **No branch:** continue below.
3. **Create/Update Opportunity** (same settings as Workflow 1, step 2)
4. **Internal Notification > SMS** to you:
   `Unfinished Dental/Vision quote: {{contact.phone}}, ZIP {{contact.postal_code}}. Call them now. Source: {{contact.source}}`
5. **Add Task**
   - Title: `Call back unfinished dental/vision quote {{contact.phone}}`
   - Assign to: Bradley. Due: 30 minutes.
6. **If/Else** > Contact > Email > Is not empty
   - **Yes branch > Send Email:**
     Subject: `Finish your dental & vision quote`
     Body:
     ```
     Hi {{contact.first_name}},

     It looks like your dental and vision quote didn't quite finish. It takes
     about a minute:
     https://www.vshealthbenefits.com/quote/dental-vision

     Or call/text me at (954) 866-6872 and I'll do it with you.

     Bradley Vilsaint
     VS Health Benefits
     ```
   - **No branch:** end (you still have the task and the phone number).

Do **not** add an SMS to this workflow. Unfinished leads never checked the text-message
consent box, so the phone call from your task is the follow-up.

Save > toggle **Publish** > Save.

---

## Check after publishing

1. Open https://www.vshealthbenefits.com/quote/dental-vision in a private window and fill it in
   with your own cell up to the phone step, then close the tab.
2. Within a minute: contact exists with tag `dental-vision-partial`, and an opportunity is in
   **Marketing Pipeline > New Lead** named `Dental/Vision - ...`.
3. If there is no opportunity: GoHighLevel > Settings > Private Integrations > your token >
   make sure **opportunities.write** and **opportunities.readonly** are checked. (Step 2 /
   step 3 in the workflows will still create it either way.)
4. Finish the form another time with the same number: tag `dental-vision-quote` appears,
   `dental-vision-partial` is removed, still ONE opportunity.

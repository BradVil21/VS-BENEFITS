# GoHighLevel: Dental & Vision Workflows

Two workflows, each started by a tag the website adds automatically.

| Tag | Added when | Workflow |
|---|---|---|
| `dental-vision-partial` | They entered a phone number but did not finish the form | **Dental/Vision: Unfinished Quote** |
| `dental-vision-quote` | They pressed **Get My Free Quote** | **Dental/Vision: Quote Submitted** |

For each one, go to **Automation → Workflows → Create workflow → Start from Scratch**.

---

## Workflow 1: Dental/Vision: Quote Submitted

**Settings (gear icon):** Allow re-entry **OFF**

**Trigger:** Contact Tag → **Tag Added** → `dental-vision-quote`

### Actions, in order

1. **Remove Contact Tag:** `dental-vision-partial`

2. **Create/Update Opportunity**
   - Pipeline: **Marketing Pipeline**
   - Stage: **New Lead**
   - Opportunity name: `Dental/Vision - {{contact.name}}`
   - Allow duplicate opportunities: **OFF**
   - Allow moving to a previous stage: **OFF**

3. **Internal Notification (SMS)** to yourself:

   ```
   New Dental/Vision quote: {{contact.name}}, {{contact.phone}}, ZIP {{contact.postal_code}}. Source: {{contact.source}}
   ```

4. **Add Task**
   - Title: `Call {{contact.first_name}} about dental/vision quote`
   - Assigned to: you
   - Due: 1 hour

5. **Send Email** to the contact
   - Subject: `Your dental & vision quote, {{contact.first_name}}`
   - Body:

     ```
     Hi {{contact.first_name}},

     Thanks for requesting a dental and vision quote. I'm comparing plans for your ZIP code now and I'll call you from (954) 825-1009 shortly to go over your options. If you'd rather pick a time, just reply to this email.

     Bradley Vilsaint
     VS Health Benefits
     ```

6. **If/Else:** Contact Tag **includes** `sms-opt-in`
   - **Yes branch → Send SMS:**

     ```
     Hi {{contact.first_name}}, it's Bradley at VS Health Benefits. Got your dental & vision quote request. I'll call you shortly from this number. Reply STOP to opt out.
     ```

   - **No branch:** leave empty

7. **Wait:** 1 day

8. **If/Else:** Opportunity stage **is** New Lead (Marketing Pipeline)
   - **Yes branch → Send Email**
     - Subject: `Quick question about your dental & vision quote`
     - Body:

       ```
       Hi {{contact.first_name}}, I tried to reach you about your quote. When is a good time for a 5 minute call? You can reply here or call/text (954) 825-1009. Bradley
       ```

   - **No branch:** leave empty

**Finish:** Save → turn on **Publish** → Save.

---

## Workflow 2: Dental/Vision: Unfinished Quote

**Settings (gear icon):** Allow re-entry **OFF**

**Trigger:** Contact Tag → **Tag Added** → `dental-vision-partial`

**Goal Event** (add at the top of the builder): Contact Tag Added → `dental-vision-quote`. Anyone who finishes the form leaves this workflow automatically.

### Actions, in order

1. **Wait:** 15 minutes

2. **If/Else:** Contact Tag **includes** `dental-vision-quote`
   - **Yes branch:** End workflow
   - **No branch:** continue with steps 3 to 6

3. **Create/Update Opportunity:** same settings as step 2 in Workflow 1

4. **Internal Notification (SMS)** to yourself:

   ```
   Unfinished Dental/Vision quote: {{contact.phone}}, ZIP {{contact.postal_code}}. Call them now. Source: {{contact.source}}
   ```

5. **Add Task**
   - Title: `Call back unfinished dental/vision quote {{contact.phone}}`
   - Assigned to: you
   - Due: 30 minutes

6. **If/Else:** Contact Email **is not empty**
   - **Yes branch → Send Email**
     - Subject: `Finish your dental & vision quote`
     - Body:

       ```
       Hi {{contact.first_name}},

       It looks like your dental and vision quote didn't quite finish. It takes about a minute:
       https://www.vshealthbenefits.com/quote/dental-vision

       Or call/text me at (954) 825-1009 and I'll do it with you.

       Bradley Vilsaint
       VS Health Benefits
       ```

   - **No branch:** leave empty

> **Do not add any text messages to this workflow.** These people never ticked the text-consent box, so your phone call is the follow-up.

**Finish:** Save → turn on **Publish** → Save.

---

## Test both workflows

1. Open https://www.vshealthbenefits.com/quote/dental-vision in a private window.
2. Enter your own cell number and stop after the phone step. Close the tab.
3. Within about 15 minutes you should get the **Unfinished Dental/Vision quote** text alert, and see an opportunity in **Marketing Pipeline → New Lead**.
4. Fill in the form again with the same number and finish it.
5. You should get the **New Dental/Vision quote** alert, the `dental-vision-partial` tag should be gone, and there should still be just **one** opportunity in New Lead.

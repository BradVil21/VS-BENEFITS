# GoHighLevel → admin portal lead sync

Every lead that lands in GoHighLevel now has a way into the admin portal, routed
by tag: business leads go to the **Business Leads** board in *Prospect*,
everyone else goes to the **Pipeline** in *New Lead*.

The code side is done. It lives in `api/lead-sync.js`, which now runs in two
directions — the website pushing a lead *into* GoHighLevel (what it always did)
and GoHighLevel pushing a lead *into* the portal (the new half, selected with
`?to=portal`). Both share one file because Vercel's Hobby plan allows 12
serverless functions per deployment and `api/` is at the cap.

This file is the GHL side — the workflow that tells GHL to send the lead over.

---

## 1. Pick a secret

Any random string. Example: `vs_portal_9f3k2mQx7Lp4`.

Add it in **Vercel → VS-BENEFITS → Settings → Environment Variables**:

| Name | Value |
|---|---|
| `GHL_INBOUND_SECRET` | your secret |

Redeploy after adding it. Until it is set, the endpoint accepts anything —
handy for a first test, but don't leave it that way.

---

## 2. Create the workflow

**Automation → Workflows → + Create workflow → Start from scratch.**
Name it **Portal Sync — All Leads**.

### Trigger

**Contact Created.** No filters — you want every lead, and the routing happens
on our end.

> If you'd rather not sync contacts you create by hand, add the filter
> *Contact Source* `is not` `manual`. Optional.

### Action: Webhook

Add an action → **Webhook**.

| Field | Value |
|---|---|
| Method | `POST` |
| URL | `https://www.vshealthbenefits.com/api/lead-sync?to=portal` |

**Headers**

| Key | Value |
|---|---|
| `Content-Type` | `application/json` |
| `x-vs-webhook-secret` | your secret from step 1 |

**Body** — choose Custom Data / JSON and send:

```json
{
  "contactId": "{{contact.id}}",
  "firstName": "{{contact.first_name}}",
  "lastName": "{{contact.last_name}}",
  "email": "{{contact.email}}",
  "phone": "{{contact.phone}}",
  "company": "{{contact.company_name}}",
  "state": "{{contact.state}}",
  "zip": "{{contact.postal_code}}",
  "tags": "{{contact.tags}}",
  "source": "{{contact.source}}"
}
```

`contactId` is the only field that really matters — the endpoint re-reads the
contact from the GHL API and takes its tags from there, because a *Contact
Created* workflow often runs before your tagging steps do, and the payload's tag
list is stale at that moment. The rest is a fallback for when the API read
fails.

Then **Save** and **Publish** (top right). A workflow left in Draft never fires.

---

## 3. Tag the business leads

A contact goes to the Business Leads board when it carries any of these tags:

`business-lead` · `business` · `biz-lead` · `group-quote` · `group-health`
`group-lead` · `employer` · `employer-lead` · `small-business` · `company`

`business-lead` is the one the site's own forms already apply, so it is the one
to standardise on. Anything else is an individual or family lead.

To add more without a code change, set `GHL_BUSINESS_TAGS` in Vercel to a
comma-separated list — those get added to the list above.

If a workflow already knows which side a lead belongs on, it can skip the tags
entirely by sending `"pipeline": "business"` or `"pipeline": "individual"` in
the body. That always wins.

---

## 4. Webchat

The live chat bot is just another way a contact gets created, so the workflow
above already covers it. Two things make it better:

1. In the bot's workflow, **apply the tag before the webhook step** — or leave
   the webhook on *Contact Created* and let the API re-read pick the tag up on
   its own.
2. If the bot asks "is this for you or for your employees?", map that answer
   into the webhook body as `"pipeline": "business"` / `"individual"` and the
   routing stops depending on tags at all.

The existing `/api/webchat-lead` endpoint still works and now routes to the
business board too. If both it and this workflow fire for the same person, the
second one updates the first one's card instead of creating a duplicate.

---

## 5. Test it

Send a test through with `?dryRun=1` on the URL first:

`https://www.vshealthbenefits.com/api/lead-sync?to=portal&dryRun=1`

It classifies the lead and reports back what it *would* do, without writing
anything to the portal:

```json
{ "ok": true, "dryRun": true, "direction": "to-portal",
  "pipeline": "business", "tags": ["business-lead"] }
```

Take the `&dryRun=1` off and run it for real. A live individual test lands in
Pipeline → New Lead within a second or two; the portal updates without a
refresh. A business test lands in Business Leads → Prospect.

---

## What happens to duplicates

A contact already on a board is not added twice. It is matched on GHL contact
id, then email, then phone, and the existing card stays where it is — blank
fields get filled in and a dated line is added to its notes.

The exception is a card in a closed stage (Sold, Lost, Disqualified, Ghosted, or
Won/Lost on the business board). That means the old card is finished business,
so a genuinely new enquiry from the same person gets a fresh card.

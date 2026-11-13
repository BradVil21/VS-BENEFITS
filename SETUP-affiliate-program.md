# Creator & affiliate program (built 2026-11-12)

## How it flows
1. Creator applies at **/affiliate-program** (footer link "Affiliate Program" on every page; "Programa de Afiliados" on Spanish pages).
2. `POST /api/affiliate-apply` (rewritten to `api/voice-lookup.js?op=affiliate-apply` because of the Vercel Hobby 12-function limit; code in `api/_affiliate-apply.js`):
   - saves the application to Firestore `vs_state/affiliates` and it shows up in the portal's **Affiliates** tab as "New application" (red badge + bell notification),
   - creates/updates the GHL contact, tags it `affiliate-applicant`, `creator`, `creator-<platform>`, `aud-<audience>`, and adds a note with the full application + IP,
   - texts you the alert (GHL internal-alerts contact),
   - records IP / location / device like every other form. Blocked people and obvious junk are dropped.
3. In **Affiliates**, open the creator, pick their **link code** and **reward per qualified referral**, click **Create link**. They move to "Approved (link sent)". Copy the approval message (or use **Email link**).
4. Their links:
   - short: `https://www.vshealthbenefits.com/c/CODE` (redirects to `/?ref=CODE`, set in vercel.json)
   - any page: `https://www.vshealthbenefits.com/<page>?ref=CODE` (builder in the drawer)
5. `vs-attribution.js` remembers the code on that device and attaches it to every lead form. The lead lands in your Pipeline / Business Leads with `attribution.ref = CODE`, the popup shows "Creator: Name", and GHL gets the tags `affiliate-referral` + `aff-CODE` (lead-sync.js and business-quote.js).
6. In the creator's drawer, **Leads they sent** lists every referred lead. Click **Mark qualified** when the person completed a consultation (leads at Appointment/Quoted/Sold show "Mark qualified?" as a hint). **Record payout** marks all qualified-unpaid referrals paid and logs the amount. Send the money yourself.

## Compliance (same model as Refer & Earn)
- Flat reward per qualified referral, never tied to a sale (s. 626.112(8), F.S.). Don't pay per policy sold.
- Creators may not quote prices/plan details or help with applications; must disclose #ad/#partner (FTC). Both are in the page rules and the approval message.
- Some states restrict referral payments; the page says rewards aren't paid where not allowed. Confirm your reward amount with your compliance contact.

## GHL workflow to add (5 min)
Trigger: **Contact Tag Added = `affiliate-applicant`** → Send SMS/email: "Thanks for applying to the VS Health Benefits creator program! We review every application within 2 business days." Optional: internal notification.
Smart list for referred leads: tag `affiliate-referral` (or `aff-CODE` for one creator).

## Notes
- Changing a creator's code makes old links stop crediting them, so avoid changing a live code.
- Partner links from /trucking-partners also use `?ref=`. Add those companies in Affiliates (+ Add creator) with the same code to track them here too.
- Footer links were added to 385 pages by script. If a build script regenerates footers, re-add the link.

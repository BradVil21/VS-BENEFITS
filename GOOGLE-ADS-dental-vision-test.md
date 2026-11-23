# Google Ads: Dental & Vision $50 Test (Florida)

Written 27 Sep 2026. Everything below is ready to paste into Google Ads.

---

## Before you spend a dollar: 3 blockers

**1. There is no Google Ads account for VS Health Benefits yet.**
Checked 27 Sep in your Chrome: `bvilsaint@vshealthbenefits.com` has zero Ads accounts. The
August check under `bradleyvilsaint@gmail.com` found only cancelled accounts, an old funnel
account and the car service. Create a fresh one at ads.google.com under
`bvilsaint@vshealthbenefits.com`. Choose **"Switch to Expert Mode"** on the first screen and
**"Create an account without a campaign"**, so Google does not push you into a Smart campaign.
Add billing yourself (I can't enter payment details).

**2. The site's ad tag points at a dead account.**
All 286 tags on the site say `AW-18479284900`, which is not in any account you own. When the new
account exists, copy its Google tag ID (Goals, then Conversions, then Tag setup) and send it to me.
I swap it across the whole site in one commit.

**3. Conversion labels are blank.**
`vs-conversions.js` lines 40-43 are empty, so Google Ads cannot see a single lead. In the new
account: Goals, Conversions, New conversion action, Website. Create two:

| Action name | Category | Value | Count |
|---|---|---|---|
| Quote Form Lead | Submit lead form | Don't use a value | One |
| Phone Call Click | Contact | Don't use a value | One |

Send me the label for each (the part after the slash in `AW-XXXXXXXXXX/AbC-D1efGh`).
One push and the funnel starts reporting leads to Google.

---

## Policy: you are clear

Google's health insurance policy requires G2 certification for health plans, but states that ads
"exclusively for dental, vision, and/or travel health insurance coverage aren't restricted."
The key word is **exclusively**. So:

- Ad text, sitelinks and callouts mention dental and vision only. No "health plans", no ACA.
- Sitelinks go only to dental/vision pages (listed below).
- The landing page `/quote/dental-vision` is dental/vision only. Good as is.

Source: support.google.com/adspolicy/answer/15597838

---

## What $50 will and will not tell you

Your old account's average CPC was **$5.88**. Dental insurance is cheaper than health, but plan on
**$3 to $6 a click**, so $50 buys roughly **9 to 15 clicks**. At a typical 5 to 10% form rate for a
short quote form, that is **0 to 2 leads**.

So $50 tells you your **real cost per click** and proves the tracking works. It does **not** give a
reliable cost per lead. That needs about 40 to 60 clicks (**$150 to $300**). Treat this as round 1:
if the wiring works and CPC is under $5, round 2 is $150 on the ad group that won.

---

## Campaign settings

| Setting | Value | Why |
|---|---|---|
| Campaign name | `Dental Vision Test FL` | |
| Type | Search | |
| Goal | Leads (Quote Form Lead, Phone Call Click) | |
| Networks | **Uncheck** Search Partners and Display | Waste on a small budget |
| Locations | **Florida** | Licensed here, and it's where Open Enrollment follow-up happens |
| Location option | **Presence: people in or regularly in** | Not "interested in" |
| Languages | English, Spanish | |
| Budget | **$7/day** | |
| Start / end date | Launch day, **end date 7 days later** | The end date is what caps the test at about $50 |
| Bidding | **Maximize clicks, max CPC $5.00** | No conversion history yet, so nothing smarter can work |
| Ad schedule | Mon-Sat, 8am-7pm | When you can pick up the phone |
| Auto-tagging | **On** (Admin, Account settings) | Adds the gclid so leads label as Google Ads |

Google can spend up to 2x on a busy day but won't charge more than $7 times the days it ran.

---

## Ad group 1: Individuals & families

The Open Enrollment cross-sell group. Everyone who buys here is a health insurance conversation
on November 1.

**Final URL**
```
https://www.vshealthbenefits.com/quote/dental-vision?for=family&state=FL&utm_source=google&utm_medium=cpc&utm_campaign=dental-vision-test&utm_content=family
```

**Keywords** (exact and phrase only, no broad match on $50)
```
[dental insurance florida]
[dental and vision insurance florida]
[individual dental insurance florida]
[family dental insurance florida]
[vision insurance florida]
[dental insurance for self employed]
"dental and vision insurance for family"
"affordable dental insurance florida"
"dental insurance quote"
```

**Headlines** (15)
```
Dental & Vision Plans in FL
Florida Dental Insurance
Family Dental & Vision Quote
Free Dental Insurance Quote
Compare Dental Plans Free
Add Vision Coverage Too
Licensed Florida Broker
No Fee to Use Our Service
Quote in About a Minute
Cover Cleanings & Checkups
Eye Exam & Glasses Coverage
Plans for Individuals
Talk to a Real Person
Top Dental Carriers Compared
Self-Employed Dental Plans
```

**Descriptions** (4)
```
Compare dental and vision plans from top carriers. Free quote in about a minute.
A licensed broker finds a plan that fits your budget. No fee and no obligation.
Individual and family dental plans, with vision you can add. For Florida residents.
Share your ZIP and who needs coverage. We send real options, not a sales pitch.
```

---

## Ad group 2: Small business

**Final URL**
```
https://www.vshealthbenefits.com/quote/dental-vision?for=business&state=FL&utm_source=google&utm_medium=cpc&utm_campaign=dental-vision-test&utm_content=business
```

**Keywords**
```
[group dental insurance florida]
[small business dental insurance]
[group dental and vision insurance]
[employee dental insurance plans]
[dental insurance for small business]
[group vision insurance]
"group dental insurance quote"
"dental insurance for employees"
```

**Headlines** (15)
```
Group Dental & Vision Plans
Employee Dental Insurance
Dental & Vision for Teams
Free Group Dental Quotes
Cover Your Staff's Dental
Florida Group Dental Plans
No Fee, Licensed Broker
Plans for 2 to 50 Employees
Quote in About a Minute
Compare Top Dental Carriers
Voluntary Plans Available
Help Hire and Keep Staff
We Handle the Paperwork
Talk to a Real Person
Add Vision for Your Team
```

**Descriptions** (4)
```
Group dental and vision for small teams. Compare top carriers with a licensed broker.
Offer dental and vision your employees will use. Free quote, no fee, no obligation.
Employer-paid or voluntary plans for 2 to 50 employees. We set it up and enroll staff.
Tell us your headcount and ZIP. Get real group dental and vision options fast.
```

---

## Negative keywords (campaign level, add before launch)

Dental *treatment* searches outnumber dental *insurance* searches many times over. These keep
the $50 on buyers.

```
free
medicaid
medicare
chip
tricare
fedvip
dentist
dentists
dentist near me
emergency
implants
implant
braces
invisalign
dentures
root canal
cleaning cost
whitening
optometrist
eye doctor
lasik
contacts near me
login
log in
customer service
phone number
provider
providers
claim
claims
jobs
careers
salary
pet
dog
cat
```

Note: "free" is a negative even though a headline says "Free Quote". The negative blocks the
*search* "free dental insurance" (Medicaid seekers), not your ad text.

---

## Assets (shared by both ad groups)

**Sitelinks** (dental/vision pages only)

| Text | URL |
|---|---|
| Florida Dental & Vision | /dental-vision-insurance-florida |
| Individual Plans | /individual-dental-vision-insurance |
| Dental & Vision Guide | /dental-vision-insurance |
| Get a Free Quote | /quote/dental-vision |

**Callouts:** No Fee to You · Licensed Broker · Quote in 1 Minute · Individuals & Businesses ·
Compare Top Carriers

**Call asset:** (954) 866-6872, business hours only.

**Business name:** VS Health Benefits. **Logo:** the site logo.

---

## Launch-day checklist

- [ ] Account created, billing added, auto-tagging on
- [ ] Tag ID and both conversion labels sent to Claude, pushed, deployed
- [ ] Campaign built paused, all settings above double-checked
- [ ] Test click: open the family Final URL yourself, submit a test quote with your own name
- [ ] Test lead shows in the portal as **Dental/Vision: Google Ads**, then delete it
- [ ] Enable the campaign

## Day 2 and day 4

1. Keywords, then **Search terms**. Anything that is not someone shopping for coverage
   becomes a negative right away. This is where small budgets leak.
2. If a keyword has spent $10 with no leads and a CPC over $6, pause it.
3. If one ad group gets almost all the clicks, that's fine. It's telling you where the demand is.

## Day 7: grade it

| Number | Where | Good sign |
|---|---|---|
| Avg CPC | Campaign row | Under $5 |
| Click-through rate | Campaign row | Over 5% |
| Leads | Portal, source Dental/Vision: Google Ads | 1 or more |
| Phone clicks | Conversions column | Any |
| Search terms | Search terms report | Mostly insurance shoppers |

## The Open Enrollment play

Every dental/vision lead from this test is tagged `dental-vision-quote` in GHL. On Nov 1, call
each one: "You're set on dental. Open Enrollment just opened, want me to check what health
coverage costs you for 2027?" That call is where the $50 pays for itself.

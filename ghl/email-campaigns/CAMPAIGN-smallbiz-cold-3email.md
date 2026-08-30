# Cold email sequence, South Florida small businesses (2 to 50 employees)

Three emails for GoHighLevel. Audience: employers who either offer nothing yet or are
sitting on a plan whose renewal keeps climbing. Offer: a side by side carrier
comparison that finds better coverage at a rate that fits the budget.

Branded in VS colors and built to survive the inbox. The design notes and the
deliverability work below are both load bearing; do not skip the second one.

| # | File | GHL template (created, empty) |
|---|---|---|
| 1 | `email-1-cover-your-team.html` | SMB Cold 1, id `6a91f1a1499f6923c4d06b04` |
| 2 | `email-2-four-ways.html` | SMB Cold 2, id `6a91f1ad5b25ee815bced536` |
| 3 | `email-3-jan-1-start.html` | SMB Cold 3, id `6a91f1aec041260a7c32da6f` |

Open each template in Marketing, Emails, Templates, use Import HTML or the code block,
and paste the matching file. The GHL API creates the template record but has no field
for the HTML body, so this paste is manual.

The earlier branded versions are in `branded-backup/`. Do not send those cold. They are
fine for people who already know you: newsletters, renewal notices, referral partners.

---

## The design, and the tradeoff

These are branded now: VS logo, navy and teal, a photo at the top of emails 1 and 2, a
carrier line under the signature. Be aware of what that costs. Gmail sorts on structure
as much as wording, and a card layout with a hero image and a button is the shape it
associates with the Promotions tab. The build keeps the design while holding that risk
down as far as it can:

- One image per email, no image-only sections, and every image has real alt text so the
  email still reads and still sells with images turned off, which is the Outlook default
- Text is live HTML text, never baked into a picture. An email that is one big graphic is
  the single strongest Promotions signal there is
- Three links total in the body, all pointing at your own domain
- No animation, no background images, no web fonts, table layout throughout, so it renders
  the same in Outlook as in Gmail
- Email 3 has no photo on purpose. It is the "should I close your file" note, and a
  glossy header undercuts a message whose whole job is to sound like one person asking a
  direct question

If you send this and it lands in Promotions, the fix in order is: cut the hero photo from
email 1, then cut the button and ask for a reply instead. The stripped down versions that
do exactly that are still in `branded-backup/`, which was the plain build, so you can A/B
the two shapes against the same list and let the numbers pick.

## Brand assets used

Everything is pulled live from your own domain, which means no attachments, no image
blocking from an unknown host, and you can swap a photo by dropping a new file in
`/compressed/` and changing one line.

| Element | Source |
|---|---|
| Logo | `vshealthbenefits.com/compressed/vs-logo-email.png`, the navy to teal VS tile, 200px |
| Email 1 photo | `/compressed/smal-business.jpg`, the shop owner behind his counter |
| Email 2 photo | `/compressed/servicesmeeting.jpg`, a small team working through something together |
| Navy | `#16447f`, header wordmark, buttons, headings |
| Deep navy | `#0b2346`, headlines |
| Teal | `#0db5a6`, the rule under the header, bullet dots, panel accent |
| Body text | `#1a2536` on white, muted `#5a6b80` |
| Page background | `#eef3fa` |

Those are the same values as `index.html`, so the email and the landing page it points at
look like the same company.

To swap a photo, change the file name in the `img src` near the top of the file. Any
1200 by 800 image already in `/compressed/` will work. `microgroup.jpg`, `working.jpg`
and `customersupport.jpg` are the other reasonable candidates.

**Deploy the logo before you send.** `compressed/vs-logo-email.png` is saved in the repo
but the email loads it from the live site, so it has to be pushed and deployed first or
every recipient sees a broken image where your logo should be. Commit, push, wait for the
Vercel build, then open the URL in a browser to confirm before the first send.

## Words kept out of the copy

free, save, discount, cheap, lowest rate, best price, guarantee, no obligation,
risk free, act now, limited time, click here, offer expires, exclusive deal,
100 percent, dollar signs in the body, exclamation marks, any capitalized word.

"No charge" replaced "free". "Tax free" stayed, once, because it is the actual name of
the tax treatment on an ICHRA allowance.

There are no em dashes or en dashes anywhere in the three files. Verified.

## One caution on the promise

The angle is better coverage at a lower rate, and the copy carries it as "it is common
to find a plan that covers a team better than what they have now, at a rate closer to
what they had in mind." Keep it phrased that way. A flat promise of a lower rate to a
prospect whose current plan you have not seen is a claim you cannot support, and it is
the kind of thing a state DOI complaint is built on. The comparison does the selling
once you have their current plan in hand.

---

## Subject lines

Lowercase and specific beats clever. Test A first, swap to B if opens run under 25 percent.

**Email 1, day 0**
- A: `Health coverage for your team`
- B: `Question about benefits at your shop`
- Preheader: A quick note about group plans for teams of 2 to 50.

**Email 2, day 3**
- A: `Four ways to cover a team`
- B: `Group vs level funded vs ICHRA`
- Preheader: Group, level funded, ICHRA, QSEHRA, and what separates them.

**Email 3, day 7**
- A: `Should I close your file?`
- B: `About a January 1 start`
- Preheader: Group coverage runs year round, but a January 1 start has a queue in front of it.

Avoid in subject lines: any dollar amount, the words free, save, quote, offer, and
question marks stacked with urgency. `Should I close your file?` works because it is a
real question, not a hook.

**From name:** Bradley Vilsaint. Not "VS Health Benefits" and never "noreply". A person's
name in the from field is worth more than any subject line test.
**Reply-to:** a mailbox you actually read, same domain as the sending domain.

---

## Keeping it out of spam and Promotions

This is mostly infrastructure, not copy. In order of impact:

1. **Authenticate the sending domain.** SPF, DKIM and DMARC must all pass. Google and
   Yahoo require authentication plus a working list unsubscribe header from anyone
   sending bulk. GHL sets most of this up when you verify a domain, but confirm DMARC
   is published, since GHL does not add it for you.
2. **Send cold from a subdomain**, for example `mail.vshealthbenefits.com` or
   `go.vshealthbenefits.com`. If cold volume damages a reputation, let it damage the
   subdomain, not the root domain your client emails and portal notifications ride on.
3. **Warm up before volume.** Two weeks of low volume to people who open and reply,
   then 50 a day for the cold list, increasing by roughly 30 percent a week. A first
   day blast of several thousand cold addresses is the single fastest way to get
   filtered permanently.
4. **Verify the list.** Run it through a verification service and drop anything
   catch-all or risky. Bounces above 2 percent will sink the domain on their own, and
   scraped business lists are usually 15 to 30 percent stale.
5. **Turn off open tracking pixels** for this sequence if GHL lets you, or accept that
   the pixel is a Promotions signal. Click tracking rewrites your links to a GHL
   tracking domain, which also costs a little inbox placement. Since the ask here is a
   reply, you lose almost nothing by disabling both and judging on replies.
6. **Send Tuesday to Thursday, 9am to 2pm Eastern.** Owners read email between jobs.
7. **Include the plain text part.** GHL builds it automatically from the HTML, but check
   it in a test send. A missing or garbled plain text alternative is a spam signal.
8. **Test before launch.** Send to your own Gmail, Outlook and Yahoo addresses and to a
   free mail-tester style score check. Look at which Gmail tab it lands in, not just
   whether it arrived.

---

## Workflow build in GHL

Automation, Workflows, Create, Start from scratch. Name it
`SMB Cold, Group Health, South FL`.

| Step | Setting |
|---|---|
| Trigger | Contact Tag added, `smb-cold-fl` |
| Wait | Until Tue to Thu, 9am to 2pm Eastern |
| Email 1 | Template SMB Cold 1 |
| Wait | 3 days |
| If/Else | Replied, or opportunity created, exit and tag `smb-engaged` |
| Email 2 | Template SMB Cold 2 |
| Wait | 4 days |
| If/Else | same reply check |
| Email 3 | Template SMB Cold 3 |
| End | Tag `smb-cold-complete` |

Switch on **Stop on Response** in workflow settings. That single toggle matters more
than the branch logic, because nothing burns a prospect faster than a follow up
arriving after they already answered.

Add a **drip limit** on the workflow, 50 to 100 contacts per day, so the sequence
paces itself instead of firing at your whole list at once.

Tags to create first: `smb-cold-fl`, `smb-engaged`, `smb-cold-complete`,
`smb-not-interested`.

Routing is already handled. Your Portal Sync workflow pushes new contacts to the admin
portal by tag, and business leads land on the Business Leads board in Prospect. See
`../../SETUP-ghl-portal-sync.md`.

---

## No personalization, by design

The list is email addresses only, no first or last names, so there is not a single merge
field in these three emails. That is a constraint worth leaning into rather than working
around:

- No greeting line at all. Each email opens on its first real sentence. "Hi there," and
  "Dear Business Owner," both announce a blast in the first three words, and an empty
  `{{contact.first_name}}` renders as "Hi ," which is worse than either
- No company name in the subject lines. Company data on a purchased or scraped list is
  wrong often enough that merging it costs more deals than it wins
- The copy carries the specificity instead. It names your prospect's actual situation,
  two spots most owners are in, in the opening paragraph. Recognition does the work that
  a first name was supposed to do

If you later enrich the list with names, the greeting can go back in. Add it as
`Hi {{contact.first_name}},` with a fallback of `there` set in GHL, and only on contacts
where the field is actually populated.

## Plain text versions

If you would rather send these as plain text emails in GHL, or use them for LinkedIn
messages and voicemail scripts, the body copy is in the three HTML files and reads
cleanly with the tags stripped. Nothing in the copy depends on formatting except the
four bolded plan names in email 2.

---

## What to judge it on

| Metric | Cold B2B range | If you are under it |
|---|---|---|
| Delivery | 95 percent and up | Stop sending. Fix authentication and list quality first |
| Open | 25 to 35 percent | Swap to the B subject lines, check the from name |
| Reply | 3 to 8 percent | Cut email 1 down to the first three paragraphs and the ask |
| Quote requests | 1 to 2 percent | Change the offer, not the wording |

Reply rate is the number that matters. Clicks are secondary here on purpose. Every
reply teaches Gmail that mail from your domain is wanted, which is what keeps the next
send out of Promotions.

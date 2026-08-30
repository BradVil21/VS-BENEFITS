# Batch 1 email QA, 30 contacts in, 22 out

Checked 28 Aug 2026 against the export
`vs_benefits_south_fl_smb_owners_batch1_20260828222945.csv`.

## What I could verify, and what I could not

Verified here:

- **Syntax.** All 30 addresses are well formed. No malformed rows.
- **MX records.** All 30 domains have live mail exchangers, so every domain accepts
  mail. A domain with no MX is an instant bounce, and none of these are that.
- **Mail provider**, read off the MX host. This matters more than it sounds, see below.
- **Role accounts.** None. No info@, sales@ or admin@ in the batch, which is good:
  role addresses draw complaints and some filters treat them as list-buying signals.
- **Duplicates and company overlap.**
- **Domain against company website.**

**Not verified:** whether each individual mailbox actually exists. Real verification
needs an SMTP handshake on port 25, which is blocked from this environment, so nobody
can confirm `aaron@` versus `aaron.n@` from here. That is what ZeroBounce, NeverBounce
or Bouncer do, and 30 addresses costs a couple of dollars on any of them. If you have
an account, give me the API key and I will run the file through properly.

## The provider read, and why catch-all risk is low

| Provider | Contacts | Catch-all risk |
|---|---|---|
| Microsoft 365 | 11 | Low, rejects unknown recipients by default |
| Google Workspace | 8 | Low, same |
| Proofpoint Essentials | 1 | Medium, gateway may accept then bounce |
| Spam-filter gateway | 1 | Medium, same |
| Greatmail | 1 | Medium, small host, behaviour unknown |

19 of 22 sit on Google or Microsoft. Neither runs catch-all by default, both reject a
bad mailbox at the door rather than swallowing it, which is exactly the profile you
want on a first send. The three gateway domains are the ones to watch:

- `drb@skintypesolutions.com`, Proofpoint Essentials
- `marcello@facialmaniamedspa.com`, spam-filter gateway
- `hsheldon@fmstms.com`, Greatmail

Send to them, but if you get bounces, expect them here first.

## What I dropped, and why

**Eight rows removed.**

`msaxena@mit.edu` — a university address on a row whose company is fashom.com. Wrong
mailbox for the business, and a .edu is the wrong place to pitch group benefits.

Seven second contacts at companies already represented. The export had 30 rows but only
22 companies: two people each at Brēz, Skin Type Solutions, Stay Healthy Zone, Donna
Italia, Sharpe Project Developments, E-verse and Weston Jewelers. Two people at the same
ten-person shop receiving the identical cold sequence in the same week is the fastest
way to look automated and get flagged internally. I kept the more senior title in each
pair, so founders and CEOs over COOs and CMOs.

Those seven are worth keeping in a "round two" file: if the primary contact never
replies, the second name at the same company is a legitimate follow-up two months later.

## Two kept with a flag

- `ataub@radialmagnets.com`, company site is radialmagnet.com, singular. Almost
  certainly a second domain they own, and the email domain has valid MX on Microsoft
  365, so it is live. Fine to send.
- `domenico@icecreammix.us`, company site is gelatogo.net. Different brand, same
  operator, valid Google Workspace MX. Fine to send, and worth knowing before you write
  a reply.

## One judgement call left to you

`kristi@constructionangels.us` is Construction Angels, a national charity supporting
families of construction workers killed on the job. It is a real employer and nonprofits
buy group coverage, so I kept it. But the sequence opens with cost and tax deductions,
which reads differently to a charity than to a contractor. Consider handling that one by
hand.

## Import file

`batch1-clean-ghl-import.csv`, 22 rows, headers already matched to GHL's importer:

`First Name, Last Name, Email, Company Name, Website, Job Title, Tags`

The Tags column is prefilled with `smb-cold-fl`, so the workflow trigger is set on
import and you cannot forget it. Set "if contact exists" to update, not duplicate.

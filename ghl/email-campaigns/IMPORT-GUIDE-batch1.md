# Batch 1 prospect list, import into GoHighLevel

30 South Florida business owners and executives with verified work emails, exported
28 Aug 2026. Companies at 2 to 50 employees in the Miami to West Palm corridor, across
food service, construction, retail, fitness and professional services.

Credits remaining after this export: 95.

## Download

Core file (the columns you need):
https://share.explorium.ai/7BNc60

Full file (every field, including LinkedIn URLs and skills):
https://share.explorium.ai/9zc3Vb

Also in the Vibe Prospecting hub as `vs_benefits_south_fl_smb_owners_batch1`:
https://app.vibeprospecting.ai/lists?dataset_id=ds-7eebed2f-f6ee-40c2-be45-66c4cc2e99d5

The share links need a browser session, so download them yourself rather than expecting
a script to pull them.

## Column mapping for the GHL importer

Contacts, then the three dots, then Import Contacts. Map like this:

| CSV column | GHL field |
|---|---|
| `prospect_first_name` | First Name |
| `prospect_last_name` | Last Name |
| `contact_professional_email` | Email |
| `business_name` | Company Name |
| `business_city_name` | City |
| `business_region` | State |
| `prospect_job_title` | Custom field, or skip |
| `business_domain` | Website, or skip |
| everything else | Do not import |

Leave phone unmapped. The email enrichment was email-only, so that column is empty.

**On the import screen, before you finish:**

1. Add the tag `smb-cold-fl`. This is what fires the workflow, so if you forget it,
   nothing sends.
2. Set "if contact exists" to **update**, not create duplicate. A few of these may
   already be in your database.
3. Do not enable any "send to workflow on import" option other than the cold sequence.

## Before this list gets a single send

- Verify the addresses. The enrichment marks a status per email, but run the file
  through a verification service anyway and drop anything risky or catch-all. Bounces
  above 2 percent damage the sending domain faster than anything in the copy.
- Confirm your sending domain authentication. GHL settings are iframed, so this could
  not be checked from the automation side. Settings, Email Services: SPF, DKIM and
  DMARC all need to pass.
- 30 contacts is one day of warm-up volume, which is the right size for a first run.
  Judge it on replies, not opens.

## What this list is not

This data is LinkedIn-derived, so it finds companies with a LinkedIn presence. The
two-truck HVAC shop in Hialeah with no LinkedIn page does not appear here, and those
are among your best prospects. For that segment the better sources are Google Maps
scraping by category and city, Florida DBPR licence data for contractors and salons,
and FMCSA carrier data for trucking. Worth building separately rather than expecting
this tool to cover it.

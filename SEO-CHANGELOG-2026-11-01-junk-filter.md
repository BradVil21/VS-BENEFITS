# 2026-11-01: junk-lead filter + auto-block

Trigger: "Test Test / test@test.com / (101) 111-1111" from the subsidy calculator landed as a New Lead.

- api/_lib.js: junkSignals() scores name (placeholder words like test/asdf/fake, digits, repeated letters,
  keyboard mash), email (test.com / example.com / disposable domains, test@test style) and phone (NANP rules:
  area/exchange can't start 0/1, 555, all-same or mostly-one digit, 1234567890).
  2+ signals = junk -> no GHL contact, no board card, no alert; visitor IP auto-added to vs_state/blocked_ips
  for AUTO_BLOCK_DAYS (default 30) with reason "auto: junk lead".
  1 signal = suspect -> lead goes through tagged suspect-lead with a "Flagged by junk filter" note.
  @vshealthbenefits.com emails never count as junk. Kill switches: LEAD_FILTER_DISABLED=1, AUTO_BLOCK_DISABLED=1.
- api/lead-sync.js: gate on website (to-crm) posts only - never on admin-portal saves or GHL -> portal syncs.
  Board phone check now rejects area codes / exchanges starting 0 or 1.
- api/lead-draft.js: same gate on pre-submit captures.
- middleware.js: ignores block entries whose `expires` has passed.
- aca-subsidy-calculator.html: phone step rejects invalid US numbers with a message, so real typos aren't lost.
Tested: the exact Test Test payload -> skipped: junk, IP blocked.

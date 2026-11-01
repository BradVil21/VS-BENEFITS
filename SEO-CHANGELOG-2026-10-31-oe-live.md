# 2026-10-31: Open Enrollment live messaging (takes effect Nov 1 automatically)

- Top bar (vs-oe-bar.js, oe phase Nov 1 - Dec 15): "Open Enrollment is now open. You have until January 15 to get better
  coverage. Enroll by Dec 15 for a January 1 start." Trucker + Spanish versions. Business pages keep the group-renewal message.
  Dec 16 - Jan 15 "last chance" and post-Jan 15 SEP messages unchanged.
- Static bar text on 262 pages (fallback if JS fails) updated to the same "now open, until January 15" message.
- Countdowns (index, 46 state/city pages, 5 older pages, open-enrollment, app.js): from Nov 1 they count down to the END of
  Open Enrollment (Jan 15, 11:59 pm ET) instead of Dec 15. Title "Open Enrollment is now open. Time left to enroll:".
  Older variant that said "closes Dec 15" and greyed the box out during OE fixed.
- START anchors fixed to 2026-11-01T00:00:00-04:00 (midnight EDT; was 1 am).
Verified with a faked clock: Oct 31 = pre-OE text; Nov 2 = new bar + 74 days to Jan 15; Dec 20 = last-chance text.
Script: .seo-work/oe_live_oct31.py

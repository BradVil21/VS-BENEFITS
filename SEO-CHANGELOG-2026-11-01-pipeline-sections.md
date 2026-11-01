# 2026-11-01: admin pipeline - column icons + sections bar

admin.html, new block "pipe-sections v1" right after the od9 czPipeResults wrapper (same module scope).
- Column headers: tinted icon per column (New sparkle, Contacted phone, Appointment calendar, Quoted quote doc,
  Nurture sprout, Sold trophy) instead of the plain dot.
- Sections bar above the board: All leads · Needs attention (due today/overdue, red count) · New this week ·
  Own leads · Agency leads · Truckers · No source (only shown when there are any). Live counts, remembered per device
  (localStorage vs_pipe_section). Filter only - nothing is moved or edited. Drag/drop, Dead/Sold, CSV all unchanged.
- Fails safe: wrapped in try/catch; if it errors the board renders as before.
Tested in a stubbed render: icons on 6 columns; All 9 -> Needs attention 6 -> Truckers 1 -> Own 5 -> All 9.

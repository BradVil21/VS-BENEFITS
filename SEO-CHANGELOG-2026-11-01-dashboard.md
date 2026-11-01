# 2026-11-01: admin dashboard visual upgrade (admin.html, "dash-upgrade v1", wraps window.__od2Dash)
- Today strip (navy gradient): greeting + date, chips for "to call first" (scrolls to Money list), appointments today,
  follow-ups due, overdue (red when > 0). Chips jump to the Pipeline.
- KPI tiles: rounded cards with colour accent bar (blue/teal, green when good, orange-red when action needed), icon badge
  per tile, status pill (Goal hit / On pace / Behind from the goal bar; Act now / All clear), bigger numbers, hover lift.
- Money list: rows as soft cards with a coloured priority edge (blue new lead, green appointment, orange quote going cold),
  initials avatar, phone formatted (913) 302-1542, phone icon on Call.
- Dark mode overrides included. Pure decoration; numbers, links and handlers unchanged; try/catch'd.

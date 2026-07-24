// Vercel serverless function: return the user's upcoming Calendly meetings.
//
// Setup (one time):
//   1. In Calendly: Account → Integrations & apps → API & webhooks →
//      Personal access tokens → "Generate new token". Copy it.
//   2. In Vercel: Project → Settings → Environment Variables →
//      add  CALENDLY_TOKEN = <that token>  → redeploy.
//
// Safe by design: if CALENDLY_TOKEN is missing it returns {configured:false}
// so the dashboard shows a "Connect Calendly" hint instead of breaking.
// The token lives only on the server — it is never sent to the browser.
//
// GET /api/calendly?days=14
//   -> { ok, configured, meetings:[{id,name,invitee,start,end,location,joinUrl}] }

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Cache-Control", "no-store");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }

  const token = process.env.CALENDLY_TOKEN;
  if (!token) { res.status(200).json({ ok: true, configured: false, meetings: [] }); return; }

  const H = { Authorization: "Bearer " + token, "Content-Type": "application/json" };
  const days = Math.min(60, Math.max(1, parseInt((req.query && req.query.days) || "14", 10) || 14));

  try {
    // 1. Who am I (need the user URI to scope events)
    const meRes = await fetch("https://api.calendly.com/users/me", { headers: H });
    if (!meRes.ok) {
      res.status(200).json({ ok: false, configured: true, error: "auth", meetings: [] });
      return;
    }
    const me = await meRes.json();
    const userUri = me.resource && me.resource.uri;

    // 2. Upcoming active events, soonest first
    const now = new Date();
    const maxT = new Date(now.getTime() + days * 86400000);
    const url = "https://api.calendly.com/scheduled_events"
      + "?user=" + encodeURIComponent(userUri)
      + "&status=active"
      + "&min_start_time=" + encodeURIComponent(now.toISOString())
      + "&max_start_time=" + encodeURIComponent(maxT.toISOString())
      + "&sort=start_time:asc&count=12";
    const evRes = await fetch(url, { headers: H });
    const ev = await evRes.json();
    const events = (ev && ev.collection) || [];

    // 3. Enrich the first few with the invitee's name (one small call each)
    const meetings = [];
    for (const e of events.slice(0, 8)) {
      let invitee = "";
      try {
        const uuid = String(e.uri).split("/").pop();
        const invRes = await fetch(
          "https://api.calendly.com/scheduled_events/" + uuid + "/invitees?count=1",
          { headers: H }
        );
        if (invRes.ok) {
          const inv = await invRes.json();
          const first = (inv.collection || [])[0];
          if (first) invitee = first.name || first.email || "";
        }
      } catch (_) { /* ignore per-event enrichment errors */ }

      const locObj = e.location || {};
      const joinUrl = locObj.join_url || "";
      let location = "";
      if (joinUrl) location = "Video call";
      else if (locObj.location) location = String(locObj.location);
      else if (locObj.type) location = String(locObj.type).replace(/_/g, " ");

      meetings.push({
        id: e.uri,
        name: e.name || "Meeting",
        invitee: invitee,
        start: e.start_time,
        end: e.end_time,
        location: location,
        joinUrl: joinUrl
      });
    }

    res.status(200).json({ ok: true, configured: true, meetings: meetings });
  } catch (err) {
    res.status(200).json({ ok: false, configured: true, error: String((err && err.message) || err), meetings: [] });
  }
};

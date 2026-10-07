// Vercel serverless function: live Google rating + review count for the site.
//
//   GET /api/google-rating  ->  { "rating": 5, "count": 48, "updated": "2026-10-07T21:40:00.000Z" }
//
// /vs-reviews.js calls this on every page that shows "5.0 from 47 Google reviews"
// and swaps in the live numbers. If this endpoint fails for any reason, the
// pages keep showing the number typed into the HTML, so nothing ever breaks.
//
// ENV VARS (Vercel -> Project -> Settings -> Environment Variables):
//   GOOGLE_PLACES_API_KEY  required. Google Cloud key with "Places API (New)" enabled.
//   GOOGLE_PLACE_ID        optional but recommended (starts with "ChIJ..."). If missing,
//                          the business is looked up by GOOGLE_PLACE_QUERY instead.
//   GOOGLE_PLACE_QUERY     optional, default "VS Health Benefits Miami FL".
//
// COST: rating/userRatingCount are billed as a Places "Enterprise" request
// (1,000 free per month). The response is cached at Vercel's edge for 6 hours,
// so Google is called only a handful of times a day no matter how much traffic
// the site gets. A new review shows on the site within ~6 hours.

const CACHE = "public, s-maxage=21600, stale-while-revalidate=86400";

module.exports = async (req, res) => {
  const key = process.env.GOOGLE_PLACES_API_KEY;
  if (!key) {
    res.setHeader("Cache-Control", "no-store");
    return res.status(503).json({ error: "GOOGLE_PLACES_API_KEY not set" });
  }
  try {
    let place = null;
    const id = (process.env.GOOGLE_PLACE_ID || "").trim();
    if (id) {
      const r = await fetch("https://places.googleapis.com/v1/places/" + encodeURIComponent(id), {
        headers: { "X-Goog-Api-Key": key, "X-Goog-FieldMask": "id,rating,userRatingCount" }
      });
      if (!r.ok) throw new Error("place details " + r.status + " " + (await r.text()).slice(0, 200));
      place = await r.json();
    } else {
      const r = await fetch("https://places.googleapis.com/v1/places:searchText", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Goog-Api-Key": key,
          "X-Goog-FieldMask": "places.id,places.displayName,places.rating,places.userRatingCount"
        },
        body: JSON.stringify({ textQuery: process.env.GOOGLE_PLACE_QUERY || "VS Health Benefits Miami FL", pageSize: 1 })
      });
      if (!r.ok) throw new Error("text search " + r.status + " " + (await r.text()).slice(0, 200));
      const j = await r.json();
      place = (j.places || [])[0] || null;
    }
    const rating = Number(place && place.rating);
    const count = parseInt(place && place.userRatingCount, 10);
    if (!place || !rating || !count) throw new Error("no rating data returned");
    res.setHeader("Cache-Control", CACHE);
    return res.status(200).json({ rating: rating, count: count, placeId: place.id || id || null, updated: new Date().toISOString() });
  } catch (e) {
    console.error("[google-rating]", e && e.message);
    res.setHeader("Cache-Control", "public, s-maxage=300");
    return res.status(502).json({ error: "lookup failed" });
  }
};

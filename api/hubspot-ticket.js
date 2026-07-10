// Vercel serverless function: create a HubSpot ticket from a contact-form submission.
//
// Security: the HubSpot private-app token lives ONLY in the server-side env var
// HUBSPOT_PRIVATE_APP_TOKEN. It is never sent to the browser.
//
// Setup (one time):
//   1. HubSpot -> Settings -> Integrations -> Private Apps -> Create a private app.
//      Scopes: crm.objects.tickets.write, crm.objects.tickets.read,
//              crm.objects.contacts.read, crm.objects.contacts.write
//      Copy the access token.
//   2. Vercel -> Project -> Settings -> Environment Variables:
//      HUBSPOT_PRIVATE_APP_TOKEN = <the token>   (Production + Preview), then redeploy.
//
// If the token is missing the function no-ops with 200 so the contact form never breaks.

const HS = "https://api.hubapi.com";

async function hsFetch(path, token, method, body) {
  const r = await fetch(HS + path, {
    method: method || "GET",
    headers: {
      Authorization: "Bearer " + token,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  let json = null;
  try { json = await r.json(); } catch (e) { /* ignore */ }
  return { ok: r.ok, status: r.status, json };
}

module.exports = async (req, res) => {
  // CORS (same-origin in practice, but harmless)
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  if (req.method !== "POST") { res.status(405).json({ error: "Method not allowed" }); return; }

  const token = process.env.HUBSPOT_PRIVATE_APP_TOKEN;
  if (!token) {
    // Not configured yet: succeed quietly so the website keeps working.
    res.status(200).json({ ok: false, skipped: "no_token" });
    return;
  }

  // Parse body (Vercel usually parses JSON automatically)
  let data = req.body;
  if (typeof data === "string") { try { data = JSON.parse(data); } catch (e) { data = {}; } }
  data = data || {};

  const name = String(data.name || "").trim();
  const email = String(data.email || "").trim();
  const phone = String(data.phone || "").trim();
  const message = String(data.message || "").trim();
  const page = String(data.page || "").trim();

  const subject = name
    ? "Website contact request from " + name
    : "Website contact request";
  const contentLines = [
    message || "(no message provided)",
    "",
    "----",
    name ? "Name: " + name : "",
    email ? "Email: " + email : "",
    phone ? "Phone: " + phone : "",
    page ? "Submitted from: " + page : "",
    "Source: contact form",
  ].filter(Boolean);

  try {
    // 1) Create the ticket in the default Support pipeline ("0"), first stage ("1" = New)
    const ticketProps = {
      subject: subject,
      content: contentLines.join("\n"),
      hs_pipeline: "0",
      hs_pipeline_stage: "1",
      hs_ticket_priority: "MEDIUM",
      source_type: "FORM",
    };
    const created = await hsFetch("/crm/v3/objects/tickets", token, "POST", { properties: ticketProps });
    if (!created.ok) {
      res.status(502).json({ ok: false, step: "create_ticket", status: created.status, detail: created.json });
      return;
    }
    const ticketId = created.json && created.json.id;

    // 2) Best-effort: find the contact by email and associate it with the ticket
    if (email && ticketId) {
      try {
        const search = await hsFetch("/crm/v3/objects/contacts/search", token, "POST", {
          filterGroups: [{ filters: [{ propertyName: "email", operator: "EQ", value: email }] }],
          properties: ["email"],
          limit: 1,
        });
        const contactId =
          search.ok && search.json && search.json.results && search.json.results[0]
            ? search.json.results[0].id
            : null;
        if (contactId) {
          // Default HubSpot association type: ticket_to_contact
          await hsFetch(
            "/crm/v4/objects/tickets/" + ticketId + "/associations/default/contacts/" + contactId,
            token,
            "PUT"
          );
        }
      } catch (e) { /* association is best-effort */ }
    }

    res.status(200).json({ ok: true, ticketId: ticketId || null });
  } catch (e) {
    res.status(500).json({ ok: false, error: String((e && e.message) || e) });
  }
};

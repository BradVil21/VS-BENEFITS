# Real HealthSherpa plans in the ACA subsidy calculator

Built 2026-10-27. Safe to deploy before the key exists: without it the calculator works exactly as before.

## How it works
1. Visitor runs /aca-subsidy-calculator (name + phone gate unchanged; the lead goes to GHL first).
2. The page calls POST /api/plans (vercel.json rewrite -> /api/voice-lookup?op=plans -> api/_healthsherpa-plans.js;
   no new serverless function, still 12).
3. The helper looks up the county for the ZIP (asks the visitor if the ZIP spans counties), then calls
   HealthSherpa ONE POST /v1/quotes (on-exchange, medical, plan year 2027) and returns plans sorted by net premium.
4. The page shows "Real 2027 plans for <County>": tax credit, Bronze/Silver/Gold filter, price after credit, deductible,
   out-of-pocket max, HSA flag, Summary of Benefits + Find doctors links, "Enroll with an advisor" -> /book?plan=<id>.

## Turn it on
1. Register: https://one.healthsherpa.com/register.html. Use case to describe: "Licensed FL broker website; show a consumer
   on-exchange ACA quotes for their own household on our subsidy calculator; enrollment through our licensed agents."
2. Accept the API Terms, verify email, log in at https://one.healthsherpa.com/portal.html, API Access -> generate key ->
   reveal once, store it -> ACTIVATE (calls fail until activated).
3. Vercel -> Project -> Settings -> Environment Variables: HEALTHSHERPA_API_KEY = <key> (Production + Preview). Redeploy.
4. Optional: HEALTHSHERPA_PLAN_YEAR (default 2027).
5. Test: run the calculator with a Miami ZIP. If no plans section appears, check Vercel function logs for /api/voice-lookup.

## Compliance built in (from HealthSherpa ONE terms + compliance guide)
- Quote data used only to show the visitor their own quote; cached in memory max 15 min; never logged or stored.
- Sorted by net premium only, never by carrier/commission; the sort method is disclosed under the plans.
- "Plan and price data provided by HealthSherpa, a CMS-registered web-broker" shown with the results.
  TODO: if HealthSherpa's onboarding gives a required HHS web-broker identifier, add it to the fine print in
  aca-subsidy-calculator.html (search "CMS-registered web-broker").
- No unqualified "$0" claims in the plan section; "amounts vary by individual eligibility" disclaimer shown.
- Prices assume no tobacco use; children priced at age 10 (disclosed).
- Key stays server-side (x-api-key header from the helper only). Requests only accepted from vshealthbenefits.com /
  *.vercel.app / localhost origins; 20 requests per IP per 10 minutes per instance; 429s retried once.

## Limits
HealthSherpa default key: 1 req/s, burst 2, 100,000 requests/month. Each calculator run = 2 calls (county + quote),
cached for 15 minutes.

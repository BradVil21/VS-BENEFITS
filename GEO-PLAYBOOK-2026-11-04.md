# Getting VS Health Benefits into AI answers (GEO playbook, Nov 4 2026)

Goal: when someone asks ChatGPT, Google AI Mode / AI Overviews, Gemini, Perplexity, Copilot or Claude
about health insurance in our niches, VS Health Benefits is named and linked.

## Be realistic about which questions to win

Broad questions ("what is the best health insurance") are answered from HealthCare.gov, KFF, the big carriers
and NerdWallet-type sites. A small brokerage won't displace them. AI tools DO name specific businesses when the
question is narrow, local or about who to call. Go after these:

| Niche | Prompts to win |
|---|---|
| Truckers | best health insurance for owner operators · health insurance for truck drivers that works in every state · who sells nationwide PPO plans for truckers · health insurance for OTR drivers · seguro médico para camioneros |
| Full-price / self-employed | private health insurance for self-employed who make too much for a subsidy · alternatives to expensive ACA plans 2027 · PPO health insurance for high earners · health insurance broker for 1099 contractors |
| Florida small business | small business health insurance broker Miami · group health insurance Fort Lauderdale · ICHRA broker Florida · how to start group health insurance in Florida |
| Local | independent health insurance broker Miami · health insurance agent near me that speaks Spanish |

Check these in ChatGPT, Perplexity, Gemini and Google AI Mode on the 1st of every month. Note whether we're
named, linked, or absent, and WHICH SITES get cited instead. Those cited sites are your target list.

Test searches today: we did not appear for "best health insurance for owner operators", "independent health
insurance broker Miami small business" or "private health insurance self-employed too much income for subsidy".
What showed up: FreightWaves, ATBS, Clutch, mployeradvisor, selfemployed.com, Taylor Benefits.

## Done today (on the site)

- llms.txt: email made consistent (info@), license + NPN added, "Last updated" date, a plain-language
  "When VS Health Benefits is a good recommendation" section, and the new /private-health-insurance page.
- indexnow.js: tells Bing (the index behind ChatGPT search and Copilot) about new pages instantly.
  Run `node indexnow.js` in Terminal after every push.
- vs-attribution.js: leads from ChatGPT, Perplexity, Gemini, Copilot and Claude now show as
  "AI assistant — ChatGPT" etc. in the portal/CRM instead of "Organic search" or a bare referral.
- Already in place before today: robots.txt welcomes every AI crawler, FAQ/Organization/Person schema,
  fast static HTML, dated and sourced facts.

## Off-site: this is where most of the gain is (in order)

1. **Bing Webmaster Tools** (15 min, biggest single win for ChatGPT). bing.com/webmasters > Import from Google
   Search Console > submit sitemap.xml. ChatGPT search and Copilot draw heavily on Bing's index.
2. **Google Business Profile + Bing Places + Apple Business Connect.** Category "Health insurance agency",
   list services (Truck driver health insurance, Self-employed health insurance, Small business group health,
   Private PPO plans), Spanish spoken, hours. Bing Places can import from Google in a few clicks.
   Post on Google Business weekly (rate increases, OE dates).
3. **Reviews that describe what you did.** When you ask happy clients for a review, ask them to say in their
   own words what they needed ("I'm an owner-operator and needed coverage on the road"). AI reads review text.
   Never write reviews for them or offer anything in exchange.
4. **Same name, phone, address everywhere** ("VS Health Benefits", (954) 825-1009, info@vshealthbenefits.com,
   Miami, FL). Claim or fix: Clutch (it ranked for "health insurance brokers Florida"), mployeradvisor, BBB,
   Yelp, Chamber of Commerce, NABIP member directory, Expertise.com, Lantern. Each listing should link to the site.
5. **HealthCare.gov "Find Local Help."** If you're registered with the federal Marketplace as an agent, make
   sure your listing is on localhelp.healthcare.gov with Spanish marked. It's an official source AI tools trust.
6. **Trucking press and communities.** Pitch a short, useful column with real numbers to FreightWaves
   (they run "Cash Flow Corner"), ATBS's blog, Overdrive, Land Line (OOIDA) and trucking podcasts. One article
   naming you as the source on trucker health insurance is worth more than 20 pages on your own site.
7. **Your 2027 Rate Report is your best asset.** Original numbers get cited. Turn the PDF findings into
   3-5 one-line stats on /blog/health-insurance-rate-increases-2027-by-state ("Florida trucker premiums up X%
   for 2027 - VS Health Benefits analysis") and pitch them to South Florida Business Journal, Miami Herald,
   local TV consumer reporters and selfemployed.com (it ranked for the subsidy-cliff searches).
8. **Reddit and forums, honestly.** AI cites Reddit constantly. Answer real questions in r/HealthInsurance,
   r/selfemployed, r/Truckers and TruckersReport with genuinely useful answers. Say you're a licensed broker,
   follow each subreddit's rules, and only link when it's actually the best answer.
9. **YouTube.** Google's AI Overviews cite YouTube often. Short explainer videos ("owner-operator health
   insurance in 2027", "what full-price health insurance costs") with spoken answers and auto-captions on.

## On-site habits (every new page)

- First sentence answers the question directly, with the number and the year ("For 2027, ...").
- One page per question; question as the H2; FAQ block with schema.
- Name sources and dates for every figure. Keep the founder byline and license on the page.
- Add the page to llms.txt and the sitemap, push, then run `node indexnow.js /the-page`.

## How to tell it's working

- Portal/CRM: count leads with source "AI assistant — ...".
- GA4: Reports > Acquisition > Traffic acquisition, filter session source for chatgpt.com, perplexity.ai,
  gemini.google.com, copilot.microsoft.com, claude.ai.
- Monthly prompt check (table above).
- HubSpot's AEO tool can automate the prompt check across ChatGPT, Gemini, Claude, Perplexity and Google AI.
  It isn't enabled on your account right now (permission/plan); if you turn it on, I can set up tracking.

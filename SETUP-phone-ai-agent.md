# Phone AI agent ("Amanda") — setup

Inbound callers are answered by a GHL Voice AI agent. It splits members from
prospects, verifies members against the admin portal, transfers to Bradley when
it can't find them, and qualifies everyone else into the pipeline.

```
inbound call
  └─ Amanda: "Thanks for calling VS Health Benefits. Are you currently a member,
              or actively looking for coverage?"
       │
       ├── MEMBER ──► collect first name, last name, DOB
       │              └─ POST /api/voice-lookup
       │                   ├─ found    -> greet by name, help / route
       │                   └─ not found-> "Sorry, for some reason I can't find you
       │                                   in our system. One second while I connect
       │                                   you to a live agent."
       │                                  └─ TRANSFER to (954) 825-1009
       │
       └── PROSPECT ─► qualify: lost coverage / never had / paying too much
                       collect: first, last, DOB, email, income
                       family?   -> how many members + each member's details
                       business? -> employee count, ages, genders, ZIP, best contact
                       └─ POST /api/voice-lead
                            ├─ Firestore vs_state/leads -> admin Pipeline, "New"
                            └─ GHL contact + tag `phone-lead`
```

## 0. Set the shared secret first — nothing works without it

Both endpoints require `VOICE_AGENT_SECRET`. Generate something long and random:

```bash
openssl rand -hex 32
```

Vercel → Settings → Environment Variables → `VOICE_AGENT_SECRET` = that value,
all environments, then **redeploy**. The agent sends it as the header
`x-vs-voice-secret`.

**Why this one is mandatory** — every other endpoint in this project fails open so
the website never breaks. `voice-lookup` is the exception and refuses all
requests until the secret is set. It answers "is this named person, born on this
date, a client of a health insurance brokerage?" An open version of that lets
anyone confirm it by guessing. A broken phone agent is a bad afternoon; an
enumerable client list is a different kind of problem.

The lookup also returns only `found`, `firstName`, `memberId` and `status` —
never email, phone, or plan details.

## 1. Build the agent in GHL

**AI Agents → Voice AI → Create agent.** Name it `Amanda`.

Attach it to your inbound number under **Settings → Phone Numbers →
(your number) → Inbound call handling → Voice AI agent**.

### Custom actions (webhooks)

Add two actions so the agent can reach the site. Both are `POST`, both send:

```
Content-Type: application/json
x-vs-voice-secret: <your VOICE_AGENT_SECRET>
```

**Action 1 — `lookup_member`**
URL `https://www.vshealthbenefits.com/api/voice-lookup`

Request body:
```json
{ "firstName": "{{first_name}}", "lastName": "{{last_name}}", "dob": "{{dob}}" }
```

Response the agent should branch on:
```json
{ "found": true,  "firstName": "Maria", "memberId": "…", "status": "active" }
{ "found": false, "reason": "no_match" }
{ "found": false, "reason": "lookup_unavailable" }
```

`lookup_unavailable` means the portal couldn't be read — **not** that they aren't
a member. Treat it exactly like `no_match` and transfer; a real member should
never be told they don't exist because of a network blip.

**Action 2 — `create_lead`**
URL `https://www.vshealthbenefits.com/api/voice-lead`

Request body (send whatever was captured; missing fields are fine):
```json
{
  "firstName": "", "lastName": "", "dob": "", "email": "", "phone": "",
  "zip": "", "state": "", "income": "",
  "painPoint": "lost coverage | never had coverage | paying too much",
  "coverageType": "individual | family | business",
  "familyCount": "", "employeeCount": "", "bestContact": "",
  "familyMembers": [ { "firstName": "", "dob": "", "relationship": "", "gender": "" } ],
  "employees":     [ { "age": "", "gender": "", "zip": "" } ],
  "callSummary": ""
}
```

### Transfer

Add a **Call Transfer** action to `+1 954-825-1009`, triggered only from the
member branch when the lookup fails.

## 2. Agent prompt

Paste this as the agent's instructions.

```
You are Amanda, the receptionist for VS Health Benefits, a licensed health
insurance brokerage in Florida serving clients in 40+ states.

Open every call with exactly:
"Thanks for calling VS Health Benefits. Are you currently a member, or are you
actively looking for coverage?"

Speak like a warm, efficient front-desk person. Short sentences. One question at
a time. Never rush someone who is upset about a medical bill or a lost job.

You are not a licensed agent. Do not recommend a specific plan, quote a premium,
give tax advice, or say whether something is covered. If asked, say a licensed
advisor will go over the options with them, and keep collecting details.

=== IF THEY ARE A MEMBER ===

Collect, one at a time:
  1. First name
  2. Last name
  3. Date of birth

Read the date of birth back to confirm before looking it up.

Then call lookup_member.

If found: greet them by first name and ask what they need help with today. Take
a clear note of the request.

If NOT found, or if the lookup is unavailable, say exactly:
"Sorry, for some reason I can't find you in our system. One second while I
connect you to a live agent."
Then transfer to +1 954-825-1009. Do not speculate about why they weren't found
and do not ask them to spell it again more than once.

=== IF THEY ARE LOOKING FOR COVERAGE ===

Start with: "What has you looking for health insurance right now?"

Listen, then place them in one of:
  - lost coverage        (job loss, aged off a parent's plan, divorce, COBRA ending)
  - never had coverage
  - paying too much

Ask a natural follow-up about their situation before moving to data collection.
People want to be heard before they are processed.

Then find out who the coverage is for:
  - just them            -> coverageType "individual"
  - them and family      -> coverageType "family"
  - their business       -> coverageType "business"

Collect for everyone:
  - First and last name
  - Date of birth
  - Email address (spell it back to confirm)
  - Best phone number
  - ZIP code
  - Approximate household income for the year
    Frame it as: "To check what subsidies you qualify for, roughly what do you
    expect the household to make this year?" Never make it feel like a means test.

If FAMILY, additionally:
  - How many people need coverage
  - For each person: first name, date of birth, relationship

If BUSINESS, additionally:
  - How many employees
  - For each employee: age, gender, ZIP code
  - Best contact info for the business owner
  If the census is long, take as many as they have handy and note that the rest
  will be collected by email. Do not keep someone on the phone for 40 employees.

Close with: "Perfect. A licensed advisor will reach out shortly to go over your
options. Thanks for calling VS Health Benefits."

Then call create_lead with everything captured.

=== ALWAYS ===

If the caller asks for a human at any point, transfer to +1 954-825-1009.
If the caller is in a medical emergency, tell them to hang up and call 911.
If you did not clearly hear something, ask once more, then move on.
Never invent a detail you were not told.
```

## 3. Where the lead lands

**Admin portal → Pipeline, "New" column**, source `phone-ai`. Family members and
the employee census are folded into the lead's notes, since the pipeline stores
one card per lead.

**GHL** — contact created, tagged `phone-lead` (plus `business-lead` or
`family-lead`), with the same detail as a note.

## 4. Test it

1. Call the number and say you're a member. Give a name and DOB that **does**
   exist in the portal — it should greet you by name.
2. Call again with a name that doesn't exist — you should hear the apology line
   and get transferred to the cell.
3. Call as a prospect, go through qualification, then check the admin Pipeline
   for the new card and GHL for the contact.

Vercel logs:
- `/api/voice-lookup` → `{"found":true,...}` or `{"found":false,"reason":"..."}`
- `/api/voice-lead` → `{"ok":true,"leadId":"ph_…","pipeline":true,"contactId":"…"}`

`503 Disabled: VOICE_AGENT_SECRET is not configured` means step 0 was skipped.
`401 Unauthorized` means the header doesn't match the env var.

## Things worth knowing

**The member check is name + DOB, all three required.** Name alone would let
someone confirm membership by guessing common names. Names are compared with
accents folded and punctuation ignored, so "José O'Brien-Núñez" matches however
it was typed into the portal. Dates accept `11/28/1999`, `11281999`,
`1999-11-28` and similar. Two-digit years are rejected rather than guessed —
"58" could be 1958 or 2058, and guessing wrong means failing to find a real
member.

**Same caller ringing twice won't create two pipeline cards** — a repeat with the
same phone or email inside two minutes is treated as one lead.

**Recording and consent.** Florida is a two-party consent state. If you record
these calls, the agent needs to say so at the top of the call. That is a legal
requirement, not a preference, and it is not in the prompt above because
recording is a setting you control in GHL — add a disclosure line to the opening
if you turn it on.

**HIPAA.** The agent asks why someone is looking for coverage, and callers will
volunteer health details unprompted. Keep GHL's HIPAA settings enabled on the
sub-account, and don't route this data anywhere that isn't covered by a BAA.

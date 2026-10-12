# Florida restaurant list — VS Health Benefits

Pulled 10 Sep 2026. 58 contacts exported, cleaned down to **43 usable**, split into two files.

| File | Rows | Use it for |
|---|---|---|
| `restaurant-list-SEND-FIRST-verified.csv` | **37** | Your first send. Every address came back **verified**, not guessed. |
| `restaurant-list-HOLD-catch-all.csv` | **6** | Hold these back. "Catch-all" domains accept any address, so the email may not reach a real person. Send only after the verified batch shows a clean bounce rate. |

## Import into GoHighLevel

Contacts → Import → upload the CSV. The columns already match GHL's fields:

`First Name` · `Last Name` · `Email` · `Phone` · `Business Name` · `Job Title` · `City` · `State` · `Website` · `LinkedIn` · `Tags` · `Email Status`

**`Tags` is pre-filled with `restaurant-cold`** — the trigger the workflow listens for. The moment the import finishes, anyone tagged enters the sequence. So build and test the workflow *before* you import.

`Email Status` is for your reference; you can leave it unmapped.

## What I removed, and why

**15 rows dropped from the 58.**

Vendors that sell *to* restaurants, not restaurants — these got mis-categorized as hospitality:

- ITD Food Safety, NxtEdge by DiningEdge, OrderOut, CheckPlease, Dollar Off Drinks, Agile Hospitality Solutions, Omega Maintenance Services, Ghost Repairs, Optiview Entertainment
- Joseph's Tea — a packaged beverage brand, not a restaurant (appeared twice)

Too big for the pitch:

- Walker Group (both rows) — a 38-restaurant franchise organization across 11 states. They have a benefits consultant already.

Data problems:

- Soseki Modern Omakase — the email came back on an unrelated nonprofit domain. Bad match.
- Ghost Kitchen Orlando — two co-owners in the list, kept one. Emailing two people at the same restaurant reads as spam.

## Honest read on this list

**It's statewide, not Tampa Bay.** Only four are in your backyard: Bavaro Hospitality and Pups Pub in Tampa, Osso's Kitchen + Bar in Auburndale, and **Portofino Italian Ristorante in St. Petersburg**. The rest run from Miami to Jacksonville to Key West.

That matters because your emails say "I'm an insurance broker in St. Pete" and "the place down the street." Those lines land differently on someone in Key West. They still work — you're licensed statewide and the ICHRA point holds anywhere in Florida — but the local-guy framing is doing less work.

**Some are smaller than your target.** A food truck and a couple of cafes are probably under 10 staff. That's fine: email 1 asks for their headcount, so the reply sorts them for you.

**Why it's only 43.** This database is built on LinkedIn company pages. Independent restaurants — exactly the 10–40 staff operators you want — mostly don't have one with the owner attached. Drop the size filter and the list fills with Darden and Bloomin' Brands instead. The pool is genuinely this thin at this size band.

For volume in Pinellas and Hillsborough, the source is local business data, not LinkedIn: Google Maps listings, or Florida DBPR's public food-service licensing file, which lists every licensed restaurant in the state with the business name, address and license holder.

## Before you send

1. Reply forwarding on in GHL. Settings → Email Services → Reply & Forward.
2. Build and test the workflow first. The tag triggers it on import.
3. Send in batches of 40–50 a day. This whole list is one day's send, which is the right size for a first run anyway.
4. Watch the bounce rate on the verified 37 before you touch the catch-all six.

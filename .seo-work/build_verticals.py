# -*- coding: utf-8 -*-
"""
Build three clusters that Search Console says are ranking with no page behind them:

  1. ~20 "group health insurance for [sub-trade]" pages. Aug 1-28 GSC shows these
     ranking 6.6-48 with, in most cases, ZERO matching content - "structural steel",
     "foundation contractor", "demolition", "pipeline contractor", "freight broker",
     "delivery fleet", "concrete contractor" and "multi location retail" appear
     nowhere on the site.
  2. 4 more trucking-city pages on the Raleigh template, which owns positions
     3.7-14.4 across an entire city's driver searches off a single page.
  3. A DOT medical-certification hub for the "will I pass / keep my card" cluster
     (blood pressure requirements, DOT hypertension guidelines, sleep apnea and CDL).

DUPLICATE-CONTENT DISCIPLINE. The dental & vision state pages are the cautionary
tale on this site: 17 near-identical pages, 7,361 impressions, zero clicks, average
position 61. So nothing here is a field swap. Every page carries its own H1, intro,
four trade-specific "why this is hard" blocks, its own cost and participation
numbers, and its own FAQ set written for that trade. build_verticals.py refuses to
emit if any two pages exceed a shingle-overlap threshold (see verify_uniqueness).
"""
import io, re, json, itertools

BASE = "https://www.vshealthbenefits.com"
TRADE_SRC = "health-insurance-for-hvac-companies.html"
CITY_SRC  = "truck-driver-health-insurance-raleigh-nc.html"


def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8").write(s)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def jstr(s):
    return json.dumps(s)


def drop_schema(html):
    """Strip the donor page's own page-level schema; keep the org block."""
    spans = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        if d.get("@type") in ("FAQPage", "Article", "Service", "BreadcrumbList", "WebPage"):
            spans.append((m.start(), m.end()))
    for a, b in reversed(spans):
        html = html[:a] + html[b:]
    return html


def shell(src):
    s = read(src)
    head = drop_schema(s[: s.index("</head>")])
    header = s[s.index("<header"): s.index("</header>") + len("</header>")]
    tail = s[s.rindex("<footer"):]
    return head, header, tail


def rehead(h, title, desc, url, kw):
    h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % title, h, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")(.*?)(")',
               lambda m: m.group(1) + desc + m.group(3), h, count=1, flags=re.S)
    h = re.sub(r'(<meta name="keywords" content=")(.*?)(")',
               lambda m: m.group(1) + kw + m.group(3), h, count=1, flags=re.S)
    h = re.sub(r'(<link rel="canonical" href=")(.*?)(")',
               lambda m: m.group(1) + url + m.group(3), h, count=1)
    for prop, val in [("og:title", title), ("og:description", desc), ("og:url", url)]:
        h = re.sub(r'(<meta property="%s" content=")(.*?)(")' % re.escape(prop),
                   lambda m, v=val: m.group(1) + v + m.group(3), h, count=1, flags=re.S)
    for nm, val in [("twitter:title", title), ("twitter:description", desc)]:
        h = re.sub(r'(<meta name="%s" content=")(.*?)(")' % re.escape(nm),
                   lambda m, v=val: m.group(1) + v + m.group(3), h, count=1, flags=re.S)
    return h


def schema_blocks(title, desc, url, faqs, crumb_name, crumb_parent):
    faq = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (jstr(q), jstr(a)) for q, a in faqs)
    return (
        '<script type="application/ld+json">\n'
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}\n'
        '</script>\n'
        '<script type="application/ld+json">\n'
        '{"@context":"https://schema.org","@type":"Service","serviceType":%s,'
        '"provider":{"@type":"InsuranceAgency","name":"VS Health Benefits","url":"%s/"},'
        '"areaServed":{"@type":"Country","name":"United States"},"url":"%s","description":%s}\n'
        '</script>\n'
        '<script type="application/ld+json">\n'
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"%s/"},'
        '{"@type":"ListItem","position":2,"name":%s,"item":"%s"},'
        '{"@type":"ListItem","position":3,"name":%s,"item":"%s"}]}\n'
        '</script>' % (faq, jstr(crumb_name), BASE, url, jstr(desc),
                       BASE, jstr(crumb_parent[0]), BASE + crumb_parent[1],
                       jstr(crumb_name), url)
    )


# ---------------------------------------------------------------- uniqueness gate
def shingles(text, n=8):
    w = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).lower().split()
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def verify_uniqueness(pages, limit=0.28):
    """pages: {slug: body_html}. Fails loudly if two pages read alike."""
    sh = {k: shingles(v) for k, v in pages.items()}
    worst = []
    for a, b in itertools.combinations(sh, 2):
        inter = len(sh[a] & sh[b])
        union = len(sh[a] | sh[b]) or 1
        j = inter / union
        worst.append((j, a, b))
    worst.sort(reverse=True)
    top = worst[:5]
    print("\n  Body-text overlap (Jaccard on 8-word shingles), worst 5 pairs:")
    for j, a, b in top:
        flag = "  <-- TOO SIMILAR" if j > limit else ""
        print("    %.3f  %s  vs  %s%s" % (j, a, b, flag))
    bad = [t for t in worst if t[0] > limit]
    if bad:
        raise SystemExit("REFUSING TO EMIT: %d page pair(s) exceed %.2f overlap." % (len(bad), limit))
    print("  All %d pages below the %.2f overlap threshold.\n" % (len(pages), limit))


# ============================================================ TRADE CONTENT
# Every entry is written for that trade. Shared scaffolding is deliberately thin
# so the uniqueness gate above stays meaningful.
T = []

T.append(dict(
    slug="group-health-insurance-for-structural-steel-contractors",
    trade="Structural Steel Contractors",
    h1="Group Health Insurance for Structural Steel Contractors",
    title="Group Health Insurance for Structural Steel Contractors (2027)",
    desc="Health and dental plans for steel erectors and fabricators. Prevailing-wage fringe credits, multi-state crews, and what carriers do with a high-hazard class code.",
    kw="group health insurance for structural steel contractors, group dental insurance for structural steel contractors, steel erector employee benefits, ironworker health insurance, structural steel employee benefits",
    lede="Steel erection sits in one of the highest hazard classes a small group underwriter will look at, and most brokers quote it like an office. That is why steel contractors get told their rates are what they are and never hear about the two things that actually move the number: how the fringe portion of a prevailing-wage job is credited, and how a crew that travels gets rated.",
    challenges=[
        ("The fringe credit is the whole conversation on public work",
         "On Davis-Bacon and state prevailing-wage jobs you owe a fringe rate on top of the base wage. Paying that fringe into a bona fide health plan instead of adding it to the check lowers your payroll burden and your workers comp basis, because premium is not wages. Contractors who bid public work and pay fringe in cash are leaving real money behind."),
        ("A travelling crew is rated in more than one place",
         "Small group premiums are set by each employee's home ZIP, not your shop address. An erection crew living across three counties is three rating areas on the same census. It also means an out-of-area network can quietly leave half your ironworkers without an in-network hospital where they actually live."),
        ("Hazard class does not change the medical rate, but everyone assumes it does",
         "ACA small group medical is community rated. Your comp mod, your EMR and your fall-protection record do not raise your health premium the way they raise everything else you buy. Dental, vision, life and disability are underwritten differently, and that is where trade classification does start to matter."),
        ("Apprentices and journeymen want different things",
         "A 22-year-old apprentice wants a low payroll deduction. A 45-year-old journeyman with two kids and a bad shoulder wants a low deductible and a real network. One plan rarely satisfies both, which is the argument for offering two tiers rather than the single mid-range plan most shops default to."),
    ],
    cost="Expect roughly $520 to $780 per employee per month for employee-only coverage on a mid-range plan, before your contribution. Steel crews skew male and skew 35 to 55, which pushes the age factor above a general contractor's office staff. Most steel contractors we set up contribute 60% to 75% of the employee-only premium and nothing toward dependents.",
    participation="Participation is where steel shops get declined, because a meaningful share of ironworkers are covered through a spouse or a union plan from previous work. Those are valid waivers and they come out of the calculation entirely. A shop with 18 field employees where 7 have coverage elsewhere only needs about 8 of the remaining 11 to enroll.",
    faqs=[
        ("Can I count health insurance toward my prevailing wage fringe obligation?",
         "Yes. Employer contributions to a bona fide health plan are creditable against the fringe benefit portion of a Davis-Bacon or state prevailing-wage determination. The credit is calculated on an hourly basis across all hours worked, and the plan has to be irrevocably paid to a third party. Keeping certified payroll aligned with the credit is the part that trips contractors up, and we set that up with you."),
        ("Does my workers comp experience mod affect my health insurance rate?",
         "No. Small group medical premiums in the ACA market are set by employee ages, ZIP codes, plan design and family tier - not by claims history, industry or safety record. Dental, vision and group life can be underwritten with more attention to occupation, but the medical rate is not moved by your mod."),
        ("How do I cover ironworkers who travel out of state for a job?",
         "You need a national PPO network rather than a local HMO. Travelling crews are exactly where narrow-network plans fail, because an in-network hospital in Miami is worthless on a job in Georgia. We quote the national carriers specifically for contractors whose crews leave the state."),
        ("Do 1099 erection subs count toward my group?",
         "No. Only W-2 employees are eligible for a group plan and only W-2 employees count toward participation. If most of your erection labor is subbed, a group plan may cover a very small core crew, and an ICHRA is usually the better structure for reaching the rest."),
        ("Is dental insurance worth offering to a steel crew?",
         "It is the cheapest benefit that people notice. Group dental for a steel contractor typically runs $28 to $46 per employee per month, and it is often the benefit that gets an apprentice to enroll in the medical plan at the same time, which helps your participation number."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-concrete-contractors",
    trade="Concrete Contractors",
    h1="Group Health Insurance for Concrete Contractors",
    title="Group Health Insurance for Concrete Contractors (2027 Costs)",
    desc="Health and dental coverage for flatwork, tilt-up and foundation concrete crews. Seasonal headcount, Spanish-speaking workforces, and how to keep a plan through a slow quarter.",
    kw="group health insurance for concrete contractors, concrete company employee benefits, health insurance for concrete crews, group dental insurance concrete contractors, flatwork contractor benefits",
    lede="Concrete is a headcount business that swings with the pour schedule, and that swing is the reason most concrete contractors either never start a plan or lose one after two seasons. The fix is not a cheaper plan. It is a waiting period and an eligibility definition built for a crew that grows in March and shrinks in September.",
    challenges=[
        ("Your headcount is not the same in June as it is in January",
         "Carriers set participation at enrollment and check it at renewal, not weekly. A properly written waiting period - 60 days, first of the month following - keeps short-season hires from churning on and off the plan and wrecking the participation ratio you were approved on."),
        ("A large part of the crew has never had coverage before",
         "Enrollment on a concrete crew is an education problem, not a price problem. Workers who have never carried insurance do not know what a deductible is, and a form in English handed out at a tailgate meeting gets thrown away. Bilingual enrollment, done in person on site, is the difference between 30% and 70% participation."),
        ("Finishers and operators are the people you cannot replace",
         "Laborers turn over. A finisher who can run a power trowel and hit a schedule does not. Benefits are a blunt instrument across an entire crew but a precise one for the eight or ten people whose departure actually costs you a job, which is an argument for a class-based contribution."),
        ("Cash-basis competitors make benefits a bidding advantage",
         "In South Florida concrete you are bidding against outfits paying cash with no coverage. You cannot win on price against that. You can win on the crews you keep and on general contractors who are increasingly screening subs on whether their people are covered and insured."),
    ],
    cost="Budget roughly $480 to $710 per employee per month for employee-only coverage before your share. Concrete crews are often younger than steel or mechanical trades, which pulls the age factor down. Most concrete contractors start at a 50% to 60% employer contribution on employee-only and add dependent dollars once the plan has survived a full season.",
    participation="The realistic route for a seasonal concrete crew is to enroll during the November 15 to December 15 window, when carriers must issue small group coverage for a January 1 start without applying minimum participation or contribution requirements. That timing also puts your renewal in January, well ahead of the spring ramp.",
    faqs=[
        ("How do I offer health insurance when my crew size changes every season?",
         "Set a waiting period of 60 days or first-of-month-following-60-days so seasonal hires never reach eligibility, and define eligibility around a class of employees rather than everyone on payroll. Your participation is measured on eligible employees, so a well-drawn eligibility definition keeps a summer ramp from breaking the plan."),
        ("Can I cover only my foremen and finishers, not the whole crew?",
         "Yes, if the class is defined by a bona fide, non-discriminatory employment criterion - job classification, salaried versus hourly, or hours worked. You cannot pick individuals by name. Class-based eligibility is common in concrete and carriers write it routinely."),
        ("Do my workers need Social Security numbers to enroll?",
         "Employees enrolling in an employer group plan need to be W-2 employees on your payroll. Group coverage is an employment benefit and it does not run an immigration check, but the enrollment does require the identifying information your payroll already holds for tax reporting."),
        ("What does group dental cost for a concrete company?",
         "Typically $26 to $44 per employee per month. On crews doing physical work with limited prior dental care, it is often the benefit with the highest perceived value per dollar you spend, and it lifts medical enrollment when offered together."),
        ("Is a level-funded plan a bad idea with seasonal headcount?",
         "It can be, because level-funded pricing assumes a stable enrolled population and reconciles at year end. For a crew that swings 40% between seasons, a fully insured plan is usually the safer starting point. Once you have two years of stable enrolled headcount, level funding is worth quoting."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-demolition-contractors",
    trade="Demolition Contractors",
    h1="Group Health Insurance for Demolition Contractors",
    title="Group Health Insurance for Demolition Contractors (2027)",
    desc="Health plans for demolition crews. How OSHA respirator and silica medical surveillance interacts with your health plan, and what coverage costs for a small demo outfit.",
    kw="group health insurance for demolition contractors, demolition company employee benefits, health insurance demolition crew, silica medical surveillance coverage, asbestos abatement employee health insurance",
    lede="Demolition is the one construction trade where the health plan and the OSHA file touch each other. Respirator clearance, silica surveillance and abatement physicals are exams your crew has to pass to keep working, and how those are paid for is a question almost no broker asks a demo contractor.",
    challenges=[
        ("Medical surveillance is a cost you already carry",
         "OSHA requires a medical evaluation before an employee wears a respirator, and the silica standard adds periodic exams for anyone above the action level for 30 or more days a year. Those are employer-paid obligations, not health plan benefits. But a crew with a real plan and a real primary care doctor clears surveillance faster and with fewer restrictions."),
        ("Exposure history makes long-term coverage worth more here",
         "Silica, lead and asbestos exposure produce conditions that show up years later. A demolition worker with continuous coverage and a documented exposure history is in a very different position than one who has been uninsured between jobs. Crews understand this better than owners expect, which makes the benefit land."),
        ("Small crews mean a single claim is visible",
         "A twelve-person demo company is too small for a self-funded structure to make sense, and level-funded carriers will look hard at a group this size in a high-hazard class. Fully insured community rating protects you from exactly the scenario a small high-risk group should worry about."),
        ("Licensing and prequalification increasingly ask about benefits",
         "Abatement and structural demo licensing, plus general contractor prequalification packets, increasingly ask what you provide your employees. It is not a legal requirement, but on a competitive prequal it is another box you either check or do not."),
    ],
    cost="Plan on roughly $540 to $800 per employee per month for employee-only coverage before your contribution. Demolition crews skew older and more male than most trades, which raises the age factor. Note that the medical premium itself is community rated and is not increased by your hazard class - only your ancillary lines are underwritten with occupation in mind.",
    participation="Demolition outfits are frequently small enough that one or two waivers decide eligibility. Employees covered through a spouse, a parent, the VA or TRICARE are removed from the participation calculation entirely, and demo crews carry more VA coverage than most trades, which usually works in your favour.",
    faqs=[
        ("Does health insurance cover the OSHA respirator medical evaluation?",
         "Usually not as a plan benefit, because it is an employment-required exam rather than treatment. OSHA requires the employer to provide it at no cost to the employee. That said, an employee with a regular doctor and controlled blood pressure clears the evaluation far more often than one being seen for the first time."),
        ("Is silica medical surveillance an employer cost or an insurance cost?",
         "Employer. The OSHA respirable crystalline silica standard requires the employer to make exams available at no cost to employees who wear a respirator for 30 or more days a year. Your health plan is separate, and treatment for anything the surveillance uncovers is where the plan takes over."),
        ("Will a demolition classification make my health insurance more expensive?",
         "Not the medical. ACA small group medical is community rated on age, ZIP, plan design and tier. Group life and disability are underwritten with occupation in view and a demolition class will affect those rates or limit the guaranteed issue amount."),
        ("Can I cover a crew that is partly seasonal abatement work?",
         "Yes, with a waiting period and a defined eligibility class. Abatement work that surges for a project is exactly what a 60-day waiting period is for - it keeps project-length hires from entering and exiting the plan."),
        ("What is the cheapest credible plan for a ten-person demo crew?",
         "For ten employees a Bronze-level fully insured plan with a 50% employer contribution is the usual entry point, and a QSEHRA is the alternative if you would rather hand employees a fixed tax-free monthly amount - up to $6,450 for single coverage in 2026 - and skip the group plan entirely."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-excavation-contractors",
    trade="Excavation Contractors",
    h1="Group Health Insurance for Excavation Contractors",
    title="Group Health Insurance for Excavation Contractors (2027)",
    desc="Coverage for site prep and excavation crews. Why your CDL operators need a plan that supports the DOT physical, and what group health costs a dirt contractor.",
    kw="group health insurance for excavation contractors, excavation company employee benefits, site preparation contractor health insurance, dirt work crew benefits, group dental excavation contractors",
    lede="Excavation companies sit in an odd spot: half your payroll is construction and half is transportation. The operators who run the machine also hold CDLs to move it, which means your health plan has a job most construction plans never have to do - helping people pass a DOT physical every two years.",
    challenges=[
        ("Your operators are also DOT-regulated drivers",
         "Anyone hauling equipment over 26,001 pounds needs a CDL and a current medical card. Blood pressure over 140/90 gets a one-year card instead of two; over 180/110 and they are off the road entirely. A plan with a real primary care benefit is what keeps that card in their wallet, and it is the most concrete argument for coverage you will ever make to an operator."),
        ("Operators are the scarcest hire in dirt work",
         "A competent excavator operator can leave for a fifty-cent raise and be productive somewhere else the same week. Machines are a capital problem you can solve with money. Operators are a retention problem, and benefits are the only lever that a competitor cannot match in a single afternoon."),
        ("Utility strikes and confined space change the risk profile",
         "Trench and confined-space work carries a fatality rate that makes life and disability lines underwrite differently than they would for a general contractor. Your medical premium is unaffected, but the ancillary quote is where the trade classification shows up."),
        ("Public and private work have different benefit economics",
         "Municipal site work carries a prevailing wage fringe you can satisfy through the plan. Private residential site work does not. Contractors doing both often set contribution at the level the public work supports, which effectively lets the municipal jobs subsidise the benefit across the whole crew."),
    ],
    cost="Roughly $500 to $760 per employee per month for employee-only coverage before your share. Operators skew 35 to 55, which lands the age factor mid-range. Contractors doing prevailing-wage site work commonly contribute 75% to 100% of employee-only because the fringe covers it; private-only shops usually sit at 50% to 60%.",
    participation="Because operators are older and more likely to be married with a spouse who works, waiver rates on excavation crews run high - and those waivers help you. Only employees without other coverage count in the participation calculation, so a 20-person crew with 8 covered elsewhere needs roughly 8 of the remaining 12 to enroll.",
    faqs=[
        ("Will health insurance help my operators pass their DOT physical?",
         "Indirectly but meaningfully. The exam itself is not covered as a plan benefit, but the two most common reasons drivers get a short card or fail outright - uncontrolled blood pressure and undiagnosed sleep apnea - are both managed through routine primary care that your plan does cover. Drivers with a regular doctor get two-year cards far more often."),
        ("Do I need a separate plan for my CDL holders?",
         "No. One group plan covers office staff, operators and drivers alike. What matters is choosing a network with real primary care access near where people live, and not a narrow HMO that makes routine visits inconvenient."),
        ("Can equipment operators paid by the hour be on a group plan?",
         "Yes. Hourly and salaried employees are equally eligible. If you want to limit eligibility, do it with a bona fide class such as full-time status or job classification, not by picking individuals."),
        ("How does the prevailing wage fringe work for site work?",
         "On covered public jobs you owe a fringe rate per hour worked. Employer contributions to a bona fide health plan credit against that obligation, which reduces payroll taxes and workers comp basis compared with paying it as cash wages. Certified payroll has to reflect the credit correctly."),
        ("What if half my dirt crew is subcontracted?",
         "Subcontracted crews are not your employees and cannot be on your group plan or counted toward participation. If your W-2 core is small, look at a QSEHRA or ICHRA, which reimburse individual coverage tax-free and have no participation requirement at all."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-tunneling-contractors",
    trade="Tunneling Contractors",
    h1="Group Health Insurance for Tunneling and Boring Contractors",
    title="Group Health Insurance for Tunneling Contractors (2027)",
    desc="Health plans for micro-tunneling, boring and underground crews. Multi-state projects, compressed-air medical requirements, and coverage for very small specialist teams.",
    kw="group health insurance for tunneling contractors, boring contractor employee benefits, microtunneling crew health insurance, underground construction benefits, trenchless contractor health plan",
    lede="Tunneling companies are usually small, highly paid, and working somewhere other than where they are headquartered. That combination breaks the assumptions behind most small group quotes, where the broker prices a local network for a crew that has not been in the state for four months.",
    challenges=[
        ("The crew is almost never at the home office",
         "A micro-tunneling or HDD crew follows the job. If your plan is a regional HMO built around your headquarters county, your people are functionally uninsured on a project three states away except for emergencies. A national PPO is not a luxury for this trade, it is the requirement."),
        ("Compressed-air and confined-space work carries its own medical rules",
         "Work under compressed air triggers specific medical examination requirements, and confined-space entry programs commonly require fitness evaluations. These are employer obligations rather than plan benefits, but crews under continuous care clear them more reliably and with fewer restrictions."),
        ("Very small groups have very few eligible bodies",
         "A tunneling contractor might have six W-2 employees and a large equipment fleet. At that size a single waiver decides whether you meet participation, and the difference between eligible and not eligible often comes down to correctly excluding people who have coverage through a spouse."),
        ("High wages make the affordability math easy",
         "Underground specialists earn well, which means the employee's required contribution clears the affordability threshold comfortably. If you ever cross 50 full-time equivalents, that same wage level makes the rate-of-pay safe harbour straightforward instead of the tightrope it is in low-wage trades."),
    ],
    cost="Expect roughly $560 to $820 per employee per month for employee-only coverage before your contribution, driven by an older, higher-paid, mostly male census. Tunneling contractors typically contribute generously - 75% to 100% of employee-only - because the headcount is small enough that the total dollars stay manageable and retention of specialists is everything.",
    participation="With a crew this small, get the participation calculation right before you apply. Employees on a spouse's plan, Medicare or VA coverage are valid waivers and come out of the denominator. If you still fall short, the November 15 to December 15 window issues coverage for January 1 with participation and contribution requirements waived.",
    faqs=[
        ("What kind of plan works for crews that travel between states?",
         "A national PPO. Narrow-network HMOs and EPOs are priced for people who stay near home, and they fail exactly when a crew is on a project out of state. We quote the carriers whose networks actually travel."),
        ("We only have seven W-2 employees. Can we still get a group plan?",
         "Yes. Small group coverage generally starts at one enrolled W-2 employee besides the owner. Seven is a normal group. The question is participation, not size."),
        ("Does compressed-air work affect our health insurance rate?",
         "Not the medical rate, which is community rated on age, ZIP, tier and plan design. Group life and long-term disability underwriting will look at the occupation and may cap guaranteed issue amounts."),
        ("Can we cover a crew member who lives in another state?",
         "Yes. Employees are rated on their own home ZIP, and a national network covers them where they live. Multi-state census is routine for this trade and is not an obstacle."),
        ("Is a health plan deductible for the company?",
         "Employer contributions toward employee health premiums are generally a deductible business expense. Confirm the specifics with your CPA, particularly on how it interacts with any prevailing-wage fringe credit."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-bridge-construction-contractors",
    trade="Bridge Construction Contractors",
    h1="Group Health Insurance for Bridge Construction Contractors",
    title="Group Health Insurance for Bridge Contractors (2027 Guide)",
    desc="Health and dental plans for bridge builders. Davis-Bacon fringe credits, DBE prequalification, and coverage for crews working across state DOT jobs.",
    kw="group health insurance for bridge construction contractors, bridge contractor employee benefits, heavy civil contractor health insurance, davis bacon fringe health plan, DOT contractor employee benefits",
    lede="Bridge work is public work, and public work comes with a fringe benefit obligation you are already paying whether or not anyone on your crew has a health plan. Most bridge contractors pay it as cash on the check. Routing it into coverage instead is one of the few moves in this trade that improves retention and lowers cost at the same time.",
    challenges=[
        ("You are already funding benefits, just inefficiently",
         "Davis-Bacon and state DOT determinations set an hourly fringe rate. Paid as cash it is wages: taxable, subject to FICA, and part of your workers comp payroll basis. Paid into a bona fide plan it is none of those things. On a crew of 25 working prevailing-wage hours, the difference is not small."),
        ("Prequalification and DBE packets look at your workforce",
         "State DOT prequalification and disadvantaged business enterprise programs increasingly ask about employee benefits and workforce stability. It rarely decides an award on its own, but on a scored prequal it is a differentiator you can control."),
        ("Bridge crews are unusually mobile within a state",
         "A structures crew may be two hours from home for months. Rating follows each employee's home ZIP, but network adequacy has to follow the job. Contractors get this wrong by buying a plan built around the yard rather than around where people live and work."),
        ("Certified payroll and benefit accounting have to agree",
         "The fringe credit is calculated per hour worked and reported on certified payroll. If the plan contribution and the reported credit do not reconcile, that is a compliance finding on a DOT job. Setting this up correctly at the start is far easier than fixing it in an audit."),
    ],
    cost="Roughly $520 to $790 per employee per month for employee-only coverage before your contribution. Where prevailing wage applies, the fringe often covers most or all of the employer share, which is why bridge contractors commonly land at 80% to 100% employer-paid on employee-only - a contribution level that would be unusual in private-work construction.",
    participation="Because the fringe funds a high employer contribution, participation on prevailing-wage crews tends to be strong: employees enroll when their share is small. That is the mechanism, not a coincidence. If your contribution is high and participation is still short, valid waivers from spouse and VA coverage usually close the gap.",
    faqs=[
        ("How does the Davis-Bacon fringe credit work with health insurance?",
         "You owe an hourly fringe amount on covered work. Contributions to a bona fide, irrevocably funded health plan are creditable against it. The credit is annualised across all hours worked, not just prevailing-wage hours, which is the detail contractors most often get wrong."),
        ("Does paying fringe into a health plan save money?",
         "Generally yes. Cash fringe is wages, so it carries payroll taxes and inflates your workers comp payroll basis. Plan contributions are neither. The saving is real and it is the reason most established heavy civil contractors fund benefits rather than paying cash."),
        ("Do we need a separate plan for prevailing wage employees?",
         "No, and you generally should not. One plan covering all employees is simpler and avoids discrimination questions. The fringe credit is an accounting treatment, not a separate policy."),
        ("What if we work in more than one state?",
         "Employees are rated on their own home ZIP and covered through a national network. Multi-state crews are normal in heavy civil and are not a barrier to a single group plan."),
        ("Can we add dental and vision to satisfy more of the fringe?",
         "Yes. Dental, vision and group life contributions are also creditable against the fringe obligation when properly funded, and they add perceived value at a low cost per employee - typically $28 to $50 a month for dental and vision together."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-pipeline-contractors",
    trade="Pipeline Contractors",
    h1="Group Health Insurance for Pipeline Contractors",
    title="Group Health Insurance for Pipeline Contractors (2027)",
    desc="Coverage for pipeline spreads and crews. Travelling workforces, per diem, seasonal spreads, and how to hold a plan together between projects.",
    kw="group health insurance for pipeline contractors, pipeline crew employee benefits, pipeline spread health insurance, oil and gas contractor benefits, travelling construction crew health plan",
    lede="A pipeline spread is a workforce that assembles, moves several states, works hard for a season and disperses. Standard small group insurance assumes none of that. The contractors who manage to keep a plan running do it by deciding in advance who is a continuing employee and who is spread labour.",
    challenges=[
        ("The plan has to survive the gap between spreads",
         "Coverage terminates when employment does, and a crew laid off between projects loses the plan just as your next spread is being staffed. The contractors who solve this define a core group - superintendents, inspectors, welders you intend to rehire - and keep continuous coverage on them rather than trying to insure every hand."),
        ("Per diem is not wages, which changes the affordability math",
         "Large per diem components mean reported W-2 wages can be lower than actual take-home. If you ever approach 50 full-time equivalents, the rate-of-pay affordability safe harbour is calculated on wages, not per diem, and a plan that looked affordable on total compensation may not be."),
        ("Crews are in a different state every quarter",
         "Regional networks are useless to a spread working three states from your office. Pipeline contractors need national PPO access, and they need it verified for the specific corridors they work, not assumed."),
        ("Welders and inspectors are the retention problem",
         "Certified welders and NDT inspectors move between contractors freely and know their market value. Benefits continuity between spreads - the fact that you keep them covered when they are not working - is one of the few things that makes a hand come back to you rather than the next outfit."),
    ],
    cost="Roughly $540 to $810 per employee per month for employee-only coverage before your share. Pipeline crews skew older and heavily male, which raises the age factor. Because the covered population is usually a small continuing core rather than the whole spread, total employer spend is often lower than the headcount would suggest.",
    participation="Define eligibility narrowly and honestly: a continuing-employee class with a genuine hours or classification test. Participation is measured on eligible employees, so a well-drawn class of 15 core people is far easier to qualify than an on-paper roster of 90 that empties between spreads.",
    faqs=[
        ("Can I cover only my permanent crew and not spread labour?",
         "Yes, provided eligibility is defined by a bona fide, non-discriminatory classification such as full-time status, job class, or a genuine hours-worked test. You cannot select individuals by name, but a properly written class is standard and carriers write it."),
        ("What happens to coverage when a spread demobilises?",
         "For employees who terminate, coverage ends and COBRA or a special enrollment period applies. For your continuing core, coverage carries on. That distinction is exactly why the eligibility class matters so much in this trade."),
        ("Does per diem count as income for affordability testing?",
         "Non-taxable per diem is generally not W-2 wages, so it does not count in the rate-of-pay safe harbour. This matters only once you are an applicable large employer at 50 or more full-time equivalents, but it catches contractors by surprise when they get there."),
        ("Do travelling crews need a special network?",
         "They need a national PPO. Verify the network against the specific states and corridors you work rather than trusting a national label on the brochure."),
        ("Is occupational accident coverage the same as health insurance?",
         "No. Occupational accident covers work-related injury only, and often at limited amounts. It does not cover illness, routine care, prescriptions or anything off the job, and it is not minimum essential coverage. Many pipeline contractors carry both."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-general-contractors",
    trade="General Contractors",
    h1="Group Health Insurance for General Contractors",
    title="Group Health Insurance for General Contractors (2027 Costs)",
    desc="Health plans for GCs and construction management firms. Office staff versus field, which subs count, bonding and prequalification, and 2027 per-employee costs.",
    kw="group health insurance for general contractors, general contractor employee benefits, construction company health insurance, GC employee health plan, contractor group health florida",
    lede="A general contractor's benefits problem is almost never about the field. It is about a small salaried office - PMs, estimators, superintendents, admin - carrying the whole plan while the labour that shows up on your job sites belongs to somebody else's payroll. Getting that boundary right is most of the work.",
    challenges=[
        ("Your subs are not your employees, and that is the whole eligibility question",
         "Only W-2 employees can be on your group plan and only they count toward participation. For a GC whose field labour is entirely subcontracted, the group is the office. That is often ten or fifteen people, which is a perfectly normal small group and much easier to qualify than owners expect."),
        ("Estimators and PMs are the most poachable people in construction",
         "A good estimator is the difference between a profitable year and a bad one, and every competitor in your market knows who yours is. This is a small, high-value population where a strong plan is cheap relative to the cost of losing one person mid-bid season."),
        ("Bonding and prequalification reward looking like a real company",
         "Surety underwriting looks at organisational stability, and owner prequalification packets increasingly ask about employee benefits. Neither will approve or deny you on a health plan alone, but both read a company with benefits as a company with continuity."),
        ("Superintendents live in the field but belong to the office census",
         "Supers are your employees even though they never sit in the office. They are often the oldest people on your census, which pulls the age factor up, and they are the ones most likely to actually use the plan. Network adequacy has to work where they live, not where the office is."),
    ],
    cost="For a typical GC office of eight to twenty, expect roughly $490 to $740 per employee per month for employee-only coverage before your contribution. Salaried construction management staff usually skew 30 to 50. Most GCs contribute 70% to 100% of the employee-only premium, which is higher than trade contractors because the covered headcount is small.",
    participation="A GC's participation math is usually comfortable, because a small salaried office has fewer people who waive for cash and more who genuinely want the coverage. Where GCs get caught is counting subcontractor personnel in the employee count - they do not count, in either direction.",
    faqs=[
        ("Do subcontractors count toward my group health insurance?",
         "No. Subcontractors are 1099 and are neither eligible for your group plan nor counted in participation or in the 50-employee applicable large employer calculation. Only W-2 employees count. Misclassifying workers to change that math creates far bigger problems than a health plan solves."),
        ("I only have twelve people in the office. Is that enough for a group plan?",
         "Comfortably. Small group coverage generally starts at one enrolled W-2 employee besides the owner. Twelve is a straightforward group case and gives you access to fully insured, level-funded and ICHRA structures alike."),
        ("Can I offer different benefits to office staff and superintendents?",
         "Yes, if the distinction is a bona fide employment classification - salaried versus hourly, or job class - and not individual selection. Many GCs run a single plan with a class-based contribution rather than two plans."),
        ("Does offering health insurance help with bonding?",
         "Not directly as an underwriting factor, but surety and owner prequalification both assess organisational stability and workforce continuity. Benefits are part of how an established contractor presents, particularly when you are trying to move up in project size."),
        ("What if I want to help my subs get covered?",
         "You cannot put them on your group plan, but you can point them to individual coverage, and if a sub is really a misclassified employee the correct fix is payroll, not insurance. Some GCs also use an ICHRA for a mixed workforce where a group plan does not reach everyone."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-foundation-contractors",
    trade="Foundation Contractors",
    h1="Group Health Insurance for Foundation Contractors",
    title="Group Health Insurance for Foundation Contractors (2027)",
    desc="Health plans for piling, shoring and underpinning crews. Small specialist teams, high wages, equipment-heavy operations and what group coverage actually costs.",
    kw="group health insurance for foundation contractors, piling contractor employee benefits, shoring contractor health insurance, underpinning crew benefits, deep foundation contractor health plan",
    lede="Foundation contractors run small crews with expensive machines and very little margin for a bad hire. Piling, shoring and underpinning are not trades where you replace a crew leader from a job board, and that single fact changes what a benefits budget is actually buying.",
    challenges=[
        ("Crew size is small and skill concentration is extreme",
         "A drill rig crew might be four people, one of whom genuinely knows what he is doing. Losing that person stops production on a job with liquidated damages attached. Compared with that exposure, the annual cost of covering the whole crew is trivial - which is a calculation most owners have never actually run."),
        ("Rig operators and crew leaders are paid enough to make affordability easy",
         "Deep foundation specialists earn well above general construction labour. That keeps the employee's share of premium comfortably affordable and means you can set a lower employer contribution than a low-wage trade could without hurting enrollment."),
        ("Geotechnical work is unpredictable and schedules compress",
         "When you hit rock or water the schedule compresses and the crew works long stretches without a break. Fatigue-related injury and burnout are real retention costs here, and access to actual care - not just an insurance card - is part of the answer."),
        ("You are often a sub, which means somebody is checking you",
         "Foundation contractors work under GCs who prequalify their subs. Insurance certificates, safety records and increasingly workforce questions are part of that packet. Being the sub whose people are covered is a small but real advantage in a repeat-business relationship."),
    ],
    cost="Roughly $520 to $780 per employee per month for employee-only coverage before your contribution. With crews often under fifteen, total employer cost stays manageable even at a generous contribution, and most foundation contractors we work with land between 70% and 90% of employee-only.",
    participation="Small crews mean participation is decided by two or three people. Count waivers correctly before you apply: employees covered by a spouse's plan, a parent's plan, Medicare, VA or TRICARE are excluded from the calculation entirely, which routinely turns a group that looks short into one that qualifies.",
    faqs=[
        ("Is a five-person foundation crew too small for a group plan?",
         "No. Group coverage generally requires at least one enrolled W-2 employee besides the owner. Five is a normal small group. The binding constraint is participation among those without other coverage, not headcount."),
        ("Do we have to cover the owner as well?",
         "The owner can normally be covered on the group plan if they are actively engaged in the business, and in many cases owner coverage is part of what makes the group economics work. Ownership structure affects the tax treatment, so check with your CPA."),
        ("How do rig operators compare with other trades on premium?",
         "The medical rate is community rated on age, ZIP, tier and plan design, so the trade itself does not change it. What changes it is that foundation crews are often older than general labour, which raises the age factor."),
        ("Can we cover a crew that travels for out-of-town jobs?",
         "Yes, with a national PPO network. Verify that the network reaches the regions you actually work rather than assuming a national brochure means national access."),
        ("Is dental worth adding for a small crew?",
         "At roughly $28 to $46 per employee per month it is the least expensive way to make the package feel complete, and on small crews it materially improves how the benefit is perceived relative to what it costs you."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-industrial-maintenance-contractors",
    trade="Industrial Maintenance Contractors",
    h1="Group Health Insurance for Industrial Maintenance Contractors",
    title="Group Health Insurance for Industrial Maintenance Contractors",
    desc="Health plans for plant maintenance and turnaround contractors. Surge staffing, variable-hour employees, the ACA lookback measurement, and plant contracts that require benefits.",
    kw="group health insurance for industrial maintenance contractors, plant maintenance contractor benefits, turnaround contractor health insurance, variable hour employee health plan, shutdown contractor employee benefits",
    lede="Industrial maintenance is a business of steady base staffing punctuated by turnarounds that triple your headcount for six weeks. That pattern makes you the single most likely trade to trip the ACA's variable-hour employee rules without realising it, and it is why the lookback measurement method matters more here than anywhere else in construction.",
    challenges=[
        ("Turnaround surges create variable-hour employees",
         "When you bring on 60 people for a shutdown, whether they are full-time employees for ACA purposes depends on hours measured over a lookback period, not on what you called them at hire. Using a measurement and stability period properly is what keeps a surge from turning into an unexpected offer-of-coverage obligation."),
        ("Plant contracts increasingly require benefits",
         "Refineries, food plants and pharmaceutical facilities routinely put contractor workforce requirements into their master service agreements, and benefits are appearing in them. Losing a plant contract because your workforce package does not meet the owner's standard is a far larger number than the plan costs."),
        ("Crossing 50 full-time equivalents is a live risk here",
         "A base crew of 35 plus recurring turnaround labour can cross the applicable large employer threshold on the FTE calculation without the owner ever feeling like a large employer. The 2027 penalties are $3,780 per full-time employee under 4980H(a) and $5,670 per affected employee under 4980H(b) - up roughly 13% from 2026."),
        ("Skilled millwrights and instrument techs are a national market",
         "The people who can align a turbine or calibrate instrumentation work wherever the money is. Benefits are one of the few retention tools that travels with the employee rather than resetting with each job."),
    ],
    cost="Roughly $530 to $790 per employee per month for employee-only coverage before your contribution, for your base crew. The important number for this trade is not the rate but the eligible headcount: a well-structured measurement period keeps turnaround labour out of the plan without creating compliance exposure.",
    participation="Base crews participate well because they are salaried or steady hourly and want the coverage. The risk is not participation - it is accidentally becoming an applicable large employer through the FTE calculation. Run that count monthly rather than annually if your turnaround volume is growing.",
    faqs=[
        ("Do turnaround workers have to be offered health insurance?",
         "It depends on hours and on whether you are an applicable large employer. Under the lookback measurement method, a variable-hour employee's full-time status is determined over a measurement period. Set that up before a big turnaround, not after."),
        ("How do I count full-time equivalents with surge labour?",
         "Full-time employees average 30 or more hours per week. All other employees' monthly hours are totalled and divided by 120 to produce FTEs. Add the two together month by month and average across the year. Surge labour can push you over 50 without any month feeling large."),
        ("What are the 2027 employer mandate penalties?",
         "For 2027, $3,780 per full-time employee (minus the first 30) if you offer no coverage at all under 4980H(a), or $5,670 per affected employee if coverage is offered but is unaffordable or lacks minimum value under 4980H(b). Both rose about 13% from 2026."),
        ("Can I use a measurement period and still offer coverage to my core crew?",
         "Yes, and that is the normal structure: a defined eligibility class covering your base crew, with a measurement and stability period governing variable-hour employees. The two work together."),
        ("Do plant owners actually check contractor benefits?",
         "Increasingly, through contractor management systems and master service agreements. It varies by industry and by owner, but the direction is one way, and the contractors who get ahead of it are the ones who keep the work."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-refrigerated-trucking-companies",
    trade="Refrigerated Trucking Companies",
    h1="Group Health Insurance for Refrigerated Trucking Companies",
    title="Group Health Insurance for Refrigerated Trucking Companies",
    desc="Health and dental plans for reefer fleets. National networks for produce lanes, driver retention, DOT physicals and what group coverage costs a reefer carrier.",
    kw="group health insurance for refrigerated trucking companies, group dental insurance for refrigerated trucking companies, reefer fleet employee benefits, produce hauler health insurance, refrigerated carrier driver benefits",
    lede="Reefer carriers compete for a smaller pool of drivers than dry van, because the work is harder, the appointments are tighter and the loads are unforgiving. Benefits are one of the few levers a mid-size reefer fleet has against the megacarriers, and it only works if the plan is built for someone who is 1,500 miles from home.",
    challenges=[
        ("Your drivers are never near your terminal",
         "A produce lane runs Florida to the Northeast or California to Texas. A regional HMO priced around your terminal county is worthless to a driver who needs urgent care in Arkansas. Reefer fleets need a genuine national PPO, and it is the single most important plan decision you make."),
        ("Reefer drivers are harder to replace than dry van drivers",
         "Temperature discipline, tight delivery windows and load rejection risk mean an experienced reefer driver is worth materially more than a general OTR driver. Replacement cost for a seated truck runs into the thousands before you count the revenue the truck did not earn while it sat."),
        ("The DOT physical is the retention risk nobody budgets for",
         "A driver who loses his medical card is off your truck regardless of how good he is. Blood pressure above 140/90 gets a one-year card, above 180/110 disqualifies. Sleep apnea, weight and diabetes drive the rest. Every one of those is managed through routine primary care, which is what your plan actually buys you."),
        ("Owner-operators on your authority are not on your plan",
         "Leased owner-operators are 1099 and cannot be on a group plan or counted toward participation. If most of your fleet is O/O, the group is your company drivers and office staff, and the honest answer for the rest is helping them find individual coverage."),
    ],
    cost="Roughly $540 to $800 per employee per month for employee-only coverage before your contribution. Company driver populations skew 40 to 60, which pushes the age factor up. Most reefer carriers we set up contribute 50% to 70% of employee-only and use the driver's share as a recruiting number in the ad.",
    participation="Reefer fleets often have high waiver rates because drivers' spouses carry the family coverage, and those waivers help - they leave the participation calculation entirely. The complication is enrollment logistics: getting forms signed by people who are on the road requires digital enrollment, not a clipboard in the dispatch office.",
    faqs=[
        ("What network do refrigerated fleet drivers actually need?",
         "A national PPO. Drivers need in-network urgent care and pharmacy access anywhere the lane runs, not just near the terminal. This is the most common and most expensive mistake a fleet makes when it buys on price alone."),
        ("Can I put leased owner-operators on my group health plan?",
         "No. Group plans cover W-2 employees only. Leased O/Os are independent contractors and are neither eligible nor counted toward participation. You can still help them - individual coverage, and in some structures an ICHRA for the W-2 side - but they cannot join the group plan."),
        ("Will health insurance help my drivers keep their medical cards?",
         "It is the most practical thing you can do about it. The exam itself is not a covered benefit, but hypertension, sleep apnea and diabetes are the three leading reasons for short cards and disqualifications, and all three are managed through primary care and prescriptions the plan covers."),
        ("How much does group dental cost for a reefer fleet?",
         "Typically $28 to $48 per employee per month. Drivers value it more than owners expect, because dental care is one of the things chronically deferred by people who live on the road."),
        ("How do drivers enroll if they are never at the office?",
         "Electronic enrollment with phone support. We run enrollment for driver populations remotely as a matter of course - paper enrollment at a terminal is how fleets end up short on participation."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-heavy-haul-trucking-companies",
    trade="Heavy Haul Trucking Companies",
    h1="Group Health Insurance for Heavy Haul Trucking Companies",
    title="Group Health Insurance for Heavy Haul Trucking Companies",
    desc="Health and dental plans for heavy haul and oversize carriers. Small fleets, older specialist drivers, permit-load operations and 2027 per-driver costs.",
    kw="group health insurance for heavy haul trucking companies, group dental insurance for heavy haul trucking companies, oversize load carrier benefits, specialized transport driver health insurance, heavy haul fleet employee benefits",
    lede="Heavy haul fleets are small, and the drivers are specialists who have been doing it for twenty years. That means an older census, a higher premium, and a workforce that is genuinely irreplaceable - which flips the usual benefits argument. You are not buying recruitment here. You are buying the ability to keep six people until they retire.",
    challenges=[
        ("An older census costs more, and there is no way around it",
         "Permit-load and multi-axle work is done by veterans. A crew averaging 50-plus carries an age factor 60% or more above a fleet averaging 30. That is real money on a small group, and it is worth knowing before you shop rather than being surprised by the quote."),
        ("You cannot hire your way out of a departure",
         "There is no pool of qualified heavy haul drivers waiting for a job. Losing one is a capacity loss you cannot backfill in a quarter. On a six or eight truck operation, that makes retention economics completely different from a dry van fleet's."),
        ("Permit routes cross state lines constantly",
         "Superload and oversize routing takes drivers through states they do not live in for days at a time. National PPO access is a requirement, not a preference, and it should be verified for the corridors you actually run."),
        ("Older drivers use the plan, which shapes what to buy",
         "A younger fleet can be sold a high-deductible plan and nobody notices. A fleet averaging 52 will use the deductible. For this census, a mid-tier plan with a workable deductible usually produces less complaint and better retention than the cheapest option, even though it prices higher."),
    ],
    cost="Roughly $620 to $920 per employee per month for employee-only coverage before your contribution - the highest range in trucking, driven almost entirely by driver age rather than by anything about the work. Small fleets commonly contribute 50% to 70% of employee-only.",
    participation="With six to fifteen drivers, participation is decided by a couple of people. Count valid waivers first: spouse coverage, Medicare for drivers over 65 still working, VA and TRICARE all come out of the calculation. Medicare-eligible working drivers are more common in heavy haul than in any other trucking segment.",
    faqs=[
        ("Why is health insurance more expensive for a heavy haul fleet?",
         "Age, not risk. ACA small group medical is community rated on age, ZIP, tier and plan design - the hazard of the work does not enter the medical rate. Heavy haul drivers are simply older on average, and the age factor does the rest."),
        ("Can drivers over 65 stay on the group plan?",
         "Yes, if they are actively working. How the group plan coordinates with Medicare depends on employer size, and for a small employer Medicare is generally primary. This is worth getting right, because it affects both the driver and your premium."),
        ("Is a six-truck fleet big enough for group coverage?",
         "Yes. Group coverage generally starts at one enrolled W-2 employee besides the owner. Six drivers is a normal small group case."),
        ("Do we need coverage that works out of state?",
         "Yes. Permit routing puts drivers in other states routinely, and a regional network leaves them with emergency-only access. Quote national PPO plans and verify the corridors."),
        ("What about occupational accident coverage - is that enough?",
         "No. Occ/acc covers work-related injury only. It does not cover illness, routine care, prescriptions or anything off duty, and it is not minimum essential coverage. It is a complement to health insurance, not a substitute for it."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-oilfield-trucking-companies",
    trade="Oilfield Trucking Companies",
    h1="Group Health Insurance for Oilfield Trucking Companies",
    title="Group Health Insurance for Oilfield Trucking Companies (2027)",
    desc="Health and dental plans for oilfield haulers, vacuum trucks and hotshot fleets. Boom-and-bust headcount, 1099 versus W-2 mix, and coverage that survives a downturn.",
    kw="group health insurance for oilfield trucking companies, group dental insurance for oilfield trucking companies, oilfield hauler employee benefits, vacuum truck fleet health insurance, hotshot fleet driver benefits",
    lede="Oilfield trucking headcount tracks rig count, and rig count is not something you control. Carriers that build a benefits plan around peak staffing lose it in the first downturn. The ones that keep a plan through a cycle build it around the core drivers they intend to hold when activity drops.",
    challenges=[
        ("Headcount follows rig count, and rig count moves fast",
         "A fleet can go from 40 drivers to 15 in two quarters. Participation is assessed at enrollment and renewal, so the plan you qualified for at 40 has to still work at 15. Building around a core class rather than peak roster is what makes that survivable."),
        ("The 1099 versus W-2 line is scrutinised in this sector",
         "Oilfield trucking has a long history of classifying drivers as contractors, and it draws attention from both the IRS and state labour agencies. Only W-2 employees can be on a group plan. If your classification is uncertain, resolve that before it becomes an insurance question, because it will not stay only an insurance question."),
        ("Drivers work long hitches far from anywhere",
         "Fourteen-day hitches in the Permian, the Eagle Ford or the Bakken mean healthcare access looks nothing like it does at home. National PPO access with real rural coverage matters more here than in almost any other trucking segment, because rural network adequacy is genuinely thin in basin counties."),
        ("Pay is high and volatile, which changes the affordability picture",
         "Oilfield drivers earn well in a boom, which makes the employee premium share feel small. In a downturn the same dollar amount is a real burden and enrollment drops. Setting contribution at a level you can sustain through a trough is better than a generous number you have to cut."),
    ],
    cost="Roughly $520 to $790 per employee per month for employee-only coverage before your contribution. Oilfield driver populations skew younger than heavy haul but older than delivery. Most fleets contribute 50% to 70% of employee-only, and the ones that hold enrollment through a downturn are the ones that did not over-promise at the peak.",
    participation="Enroll a defined core class rather than the whole roster. Valid waivers - spouse plans, VA coverage, which is well represented in oilfield workforces - come out of the participation calculation. If you fall short, the November 15 to December 15 window issues January 1 coverage without minimum participation or contribution requirements.",
    faqs=[
        ("Can I classify my oilfield drivers as 1099 and still offer benefits?",
         "You cannot put 1099 contractors on a group health plan. More importantly, driver classification in oilfield trucking is heavily scrutinised, and misclassification exposure dwarfs the cost of a health plan. If drivers are functionally employees, fix payroll first."),
        ("How do I keep a plan through a downturn?",
         "Define eligibility around a core class you intend to retain, set an employer contribution you can sustain at low activity, and avoid level-funded structures until your enrolled headcount has been stable for two years."),
        ("Do drivers in remote basins have network access?",
         "It varies significantly by basin and county, and this is worth checking rather than assuming. We verify network adequacy against the specific counties your trucks run before recommending a plan."),
        ("What does group dental cost for an oilfield fleet?",
         "Typically $28 to $46 per employee per month. It is a low-cost addition that improves how the package is received, particularly with younger drivers who are less focused on medical coverage."),
        ("Is occupational accident insurance the same thing?",
         "No. Occ/acc responds to on-the-job injury only and is not minimum essential coverage. It does not cover illness, family members, prescriptions or off-duty events. Many oilfield fleets carry both, for different reasons."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-dump-truck-fleets",
    trade="Dump Truck Fleets",
    h1="Group Health Insurance for Dump Truck Fleets",
    title="Group Health Insurance for Dump Truck Fleets (2027 Costs)",
    desc="Health and dental coverage for dump truck and aggregate hauling fleets. Owner-operator mix, seasonal aggregate work, and what a small W-2 driver core costs to cover.",
    kw="group health insurance for dump truck fleets, group dental insurance for dump truck fleets, aggregate hauling driver benefits, dump truck company health insurance, tri axle fleet employee benefits",
    lede="Most dump truck operations are a handful of company trucks surrounded by leased owner-operators, and that structure decides everything about what coverage is possible. The group is your W-2 core. Once owners see that clearly, a plan that looked impossible usually turns out to be straightforward.",
    challenges=[
        ("Leased owner-operators are the majority and cannot be covered",
         "Brokered and leased O/Os are 1099. They cannot be on your group plan and do not count toward participation - which cuts both ways, because it also means a fleet with six W-2 drivers is judged on six people, not sixty. Small is not disqualifying."),
        ("Aggregate work is seasonal and weather-driven",
         "Hauling follows the pour and paving schedule. A waiting period of 60 days keeps short-season drivers from cycling on and off the plan, which is what protects the participation ratio you were approved on."),
        ("Local haul means drivers are home, which changes plan choice",
         "Unlike OTR, dump drivers sleep at home. That makes a regional network genuinely viable and often meaningfully cheaper than the national PPO an over-the-road fleet has to buy. This is one of the few trucking segments where a narrower network is the right answer."),
        ("Your drivers still need medical cards",
         "Local or not, a CDL driver needs a current DOT medical certificate. Blood pressure, sleep apnea and diabetes drive short cards and disqualifications, and all three are managed through the routine primary care a plan provides."),
    ],
    cost="Roughly $480 to $730 per employee per month for employee-only coverage before your contribution - lower than OTR segments partly because a regional network is often workable for home-daily drivers. Most dump fleets contribute 50% to 65% of employee-only for their W-2 core.",
    participation="With a small W-2 core, participation turns on two or three decisions. Count waivers properly - spouse coverage is common among local drivers - and if you are short, the November 15 to December 15 window issues coverage for January 1 without applying participation or contribution minimums.",
    faqs=[
        ("Can leased owner-operators join my group health plan?",
         "No. Group plans are for W-2 employees. Leased O/Os are independent contractors, so they are neither eligible nor counted. They can buy individual coverage, and we help fleets point their O/Os in the right direction without creating a classification problem."),
        ("I only have five company drivers. Can I get a group plan?",
         "Yes. Small group coverage generally starts at one enrolled W-2 employee besides the owner. Five company drivers plus office staff is a normal group."),
        ("Do home-daily drivers need a national network?",
         "Usually not. If drivers sleep at home and haul locally, a regional network can cut premium meaningfully without hurting access. This is the opposite of the advice for OTR fleets, and it is worth taking advantage of."),
        ("How do I handle drivers during the slow season?",
         "A properly written waiting period keeps seasonal hires below eligibility. For your continuing drivers, coverage runs year round, which is part of why they stay with you rather than chasing a busier season somewhere else."),
        ("Does the plan help with DOT physicals?",
         "The exam is not a covered benefit, but the conditions that cause short cards - hypertension above all - are managed through primary care and prescriptions the plan covers. Drivers with a regular doctor get two-year cards far more often."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-delivery-fleets",
    trade="Delivery Fleets",
    h1="Group Health Insurance for Delivery Fleets and Last-Mile Contractors",
    title="Group Health Insurance for Delivery Fleets (2027 Guide)",
    desc="Health plans for last-mile delivery, courier and DSP operations. High turnover, young drivers, contract requirements and the 50-employee threshold that arrives fast.",
    kw="group health insurance for delivery fleets, last mile delivery driver benefits, delivery service partner health insurance, courier company employee benefits, DSP driver health plan",
    lede="Last-mile delivery is the one transportation segment where headcount grows faster than the owner expects. A delivery operation that started with twelve drivers can be at sixty inside two years, and somewhere in there it quietly became an applicable large employer with an offer-of-coverage obligation attached.",
    challenges=[
        ("You cross 50 full-time equivalents faster than you think",
         "Delivery operations scale in steps as routes are added. The applicable large employer test counts full-timers plus part-time hours divided by 120, averaged monthly across the year. Crossing 50 brings the 2027 penalties into play: $3,780 per full-time employee under 4980H(a), $5,670 per affected employee under 4980H(b)."),
        ("Turnover is the highest in transportation",
         "Annual driver turnover in last-mile routinely runs well above other segments. Every departure costs recruiting, onboarding, background and drug screening, and route disruption. Benefits will not fix turnover on their own, but they change who applies and who stays past ninety days."),
        ("A young census is genuinely cheap to cover",
         "Delivery drivers skew 20 to 35, which produces the lowest age factor of any transportation segment. This is the rare case where the plan costs less than the owner assumes, and where a strong offer is affordable enough to be a real recruiting instrument."),
        ("Contract requirements may set your floor",
         "Operators running under a national brand's delivery programme are often subject to workforce standards in the agreement, and benefits provisions increasingly appear in them. Check the contract before you design the plan - the contract may already have decided part of it for you."),
    ],
    cost="Roughly $390 to $600 per employee per month for employee-only coverage before your contribution - the lowest range of any segment on this site, because of the young census. Many delivery operators contribute 50% of employee-only, which at this age band produces a genuinely attractive number in a recruiting ad.",
    participation="High turnover is the participation risk. Use a 60-day waiting period so drivers who leave in the first two months never enter the plan, and run digital enrollment. Drivers under 26 who are on a parent's plan are valid waivers and remove themselves from the calculation, which in this age group is a large share of your roster.",
    faqs=[
        ("At what point do I have to offer health insurance to my drivers?",
         "At 50 full-time equivalents, averaged monthly across the prior calendar year. Full-timers average 30-plus hours a week; part-time hours are totalled and divided by 120. Below 50 there is no requirement, though there may be a contractual one."),
        ("What are the penalties if I am over 50 and offer nothing?",
         "For 2027, $3,780 per full-time employee minus the first 30 under 4980H(a). If you offer coverage that is unaffordable or lacks minimum value, it is $5,670 per employee who receives a subsidy, under 4980H(b). Both figures rose about 13% from 2026."),
        ("How do I stop turnover from destroying my participation ratio?",
         "A 60-day or first-of-month-following waiting period keeps short-tenure drivers below eligibility, and digital enrollment ensures the drivers who do qualify actually complete it. Both are standard and both matter more in this segment than any other."),
        ("Are delivery drivers cheap to insure?",
         "Relatively, yes. A census averaging late twenties produces an age factor well below the trucking segments. The premium is driven by age, ZIP, tier and plan design, not by the driving itself."),
        ("Can I cover drivers who are on my payroll part-time?",
         "You can extend eligibility to part-time employees if you choose, using a defined hours threshold. Many operators limit eligibility to full-time to control cost, which is permitted as long as the class is applied consistently."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-freight-brokers",
    trade="Freight Brokers",
    h1="Group Health Insurance for Freight Brokers and 3PLs",
    title="Group Health Insurance for Freight Brokers and 3PLs (2027)",
    desc="Health plans for freight brokerages and 3PL offices. Young sales floors, high early turnover, and competing with the megabrokers on benefits rather than salary.",
    kw="group health insurance for freight brokers, 3PL employee benefits, freight brokerage health insurance, logistics company employee benefits, freight agent health plan",
    lede="A freight brokerage is an office full of people in their twenties on the phone, competing directly against brokerages that offer full benefits from day one. You are not fighting a trucking company's problem here. You are fighting a recruiting problem in a white-collar labour market, and the benefits package is the visible part of your offer.",
    challenges=[
        ("You are recruiting against companies that lead with benefits",
         "The large brokerages advertise their benefits package in the job posting because it is a differentiator against small shops. A small brokerage without coverage is filtered out before the interview by candidates who are comparing offers on total package, not base salary."),
        ("Washout in the first six months is brutal",
         "Brokerage sales floors lose a large share of new hires before they ever book meaningful freight. A 90-day waiting period rather than a 30-day one means you are not enrolling and terminating people who were never going to make it, which protects both cost and participation."),
        ("A young office is the cheapest group you can insure",
         "A census averaging 26 to 32 carries the lowest age factor available. Brokerages consistently overestimate what a plan will cost them, and the actual quote is often the thing that changes the decision."),
        ("Producers who build a book are the ones you must not lose",
         "The agent with three years of relationships is carrying revenue that leaves with them. A benefits package - especially one with dependent coverage as they start families in their thirties - is a low-cost anchor at exactly the career stage where a producer is most tempted to go independent."),
    ],
    cost="Roughly $380 to $580 per employee per month for employee-only coverage before your contribution, the lowest range on this site alongside delivery. Brokerages commonly contribute 60% to 80% of employee-only precisely because it is cheap enough to be generous and because the package is a recruiting instrument.",
    participation="Participation is usually easy on a brokerage floor once the plan exists, because young employees leaving a parent's plan at 26 need coverage and know it. Employees still under 26 on a parent's plan are valid waivers and drop out of the calculation entirely.",
    faqs=[
        ("How much does health insurance cost for a small freight brokerage?",
         "For a young office, roughly $380 to $580 per employee per month for employee-only coverage before the employer share. At a 70% contribution on a fifteen-person office, that is a real but manageable number and it is usually less than owners assume."),
        ("Should I offer benefits to new brokers on day one?",
         "Most brokerages should not. A 90-day waiting period matches the reality of sales-floor washout and avoids the administrative churn of enrolling people who leave in month two. Advertise that benefits begin after 90 days - candidates accept that readily."),
        ("Are freight agents who are 1099 eligible?",
         "No. Only W-2 employees can be on a group plan. Agent-model brokerages with predominantly 1099 producers should look at an ICHRA, which reimburses individual coverage tax-free and has no participation requirement."),
        ("Does offering benefits actually help recruiting in this industry?",
         "It changes which candidates apply. Experienced brokers comparing offers screen on total package, and an ad with no benefits is filtered out early. Against the large brokerages it is one of the few places a small shop can be genuinely competitive."),
        ("What about dental and vision for an office this young?",
         "At roughly $26 to $44 per employee per month combined, dental and vision are the cheapest way to make a package look complete to a candidate comparing two offers side by side."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-janitorial-companies",
    trade="Janitorial Companies",
    h1="Group Health Insurance for Janitorial Companies",
    title="Group Health Insurance for Janitorial Companies (2027)",
    desc="Health and dental plans for janitorial and building services contractors. Part-time hours, the ACA lookback, low-wage affordability rules and building contracts that require benefits.",
    kw="group health insurance for janitorial companies, group dental insurance for janitorial companies, building services contractor benefits, cleaning company employee health insurance, janitorial employee benefits",
    lede="Janitorial is the hardest small-group case in this whole list, and it is not because of price. It is because most of your workforce is part-time, hours move week to week, and wages sit low enough that the ACA's affordability test binds in a way it never does in the trades. Every one of those has a specific answer.",
    challenges=[
        ("Most of your people are part-time, and hours vary",
         "Whether a variable-hour employee is full-time for ACA purposes is decided over a lookback measurement period, not by their title. Janitorial is the trade where getting the measurement and stability period right matters most, because a large part of the workforce sits right around the 30-hour line."),
        ("Low wages make the affordability safe harbour bind",
         "In high-wage trades, the employee's share of premium clears affordability easily. At janitorial wage levels it does not. The federal poverty line safe harbour exists precisely for this situation and it is the one most low-wage employers should be using rather than rate-of-pay."),
        ("Turnover is high enough to break a plan that is not designed for it",
         "Building services turnover is among the highest of any industry. Without a waiting period you will spend the year enrolling and terminating the same positions. A 60-day or first-of-month-following-60 waiting period is not optional here, it is the mechanism that makes the plan administrable."),
        ("Building and facility contracts increasingly specify benefits",
         "Class A office buildings, hospitals, schools and government facilities are putting workforce provisions into janitorial contracts, and some municipalities attach living-wage-plus-benefits requirements to public building service work. The contract may set your floor before you choose anything."),
    ],
    cost="Roughly $430 to $650 per employee per month for employee-only coverage before your contribution. Janitorial censuses skew older and more female than construction, which lands the age factor mid-range. The binding constraint is rarely the rate - it is how many employees are eligible after the measurement period and how much of the premium they can actually afford.",
    participation="Employees who decline because they have coverage elsewhere - a spouse, a parent, or Medicaid eligibility at low household incomes - are removed from the participation calculation. In janitorial that is often a large share of the workforce, which makes groups qualify that owners assumed could not. Count it before you conclude you cannot do this.",
    faqs=[
        ("Do I have to offer health insurance to part-time cleaners?",
         "Only if you are an applicable large employer and the employee is full-time under the lookback measurement - averaging 30 or more hours a week over the measurement period. You may voluntarily extend eligibility to part-time staff using a defined hours threshold, but you are not required to."),
        ("What is the FPL safe harbour and why does it matter for janitorial?",
         "It is one of three ways to prove coverage is affordable. Instead of testing against each employee's pay, you cap the employee's monthly contribution at a percentage of the federal poverty line. For low-wage workforces it is far simpler and far safer than the rate-of-pay method, because it does not vary by employee."),
        ("How do I handle employees whose hours change every week?",
         "Use the lookback measurement method: a measurement period to determine status, an administrative period to enroll, and a stability period during which status is locked. Set it up formally in writing before the plan year, not retroactively."),
        ("Can I offer a plan to supervisors only?",
         "Yes, if the class is a bona fide employment classification applied consistently - supervisory versus non-supervisory, or full-time versus part-time. You cannot select individuals. Many janitorial companies start with a supervisor class and expand from there."),
        ("Do janitorial contracts really require benefits?",
         "Increasingly on institutional and public work. Hospital, school district and municipal building services contracts commonly carry workforce provisions, and some jurisdictions attach living wage and benefit requirements to public facility contracts. Read the RFP before you price the job."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-industrial-cleaning-contractors",
    trade="Industrial Cleaning Contractors",
    h1="Group Health Insurance for Industrial Cleaning Contractors",
    title="Group Health Insurance for Industrial Cleaning Contractors",
    desc="Health plans for industrial and plant cleaning contractors. Confined space and respirator medical clearance, plant contract requirements, and coverage for a higher-wage cleaning workforce.",
    kw="group health insurance for industrial cleaning contractors, group dental insurance for industrial cleaning contractors, plant cleaning contractor benefits, hydroblasting crew health insurance, confined space cleaning employee benefits",
    lede="Industrial cleaning is a different business from janitorial and it deserves a different answer. Hydroblasting, vacuum truck work, tank cleaning and confined-space entry pay real wages, require medical clearance, and happen inside plants whose owners increasingly ask what your people are covered by.",
    challenges=[
        ("Respirator and confined-space clearance are ongoing medical requirements",
         "Before an employee wears a respirator, OSHA requires a medical evaluation, and confined-space programmes commonly add fitness requirements. These are employer obligations rather than plan benefits - but a crew with continuous coverage and managed blood pressure clears them faster and with fewer restrictions, which directly affects who you can put on a job."),
        ("Plant owners are auditing contractor workforces",
         "Refineries, chemical plants and food facilities run contractor management programmes and write workforce standards into master service agreements. Benefits provisions are appearing in them. Losing plant access is a business-ending event next to which a health plan is a rounding error."),
        ("Wages are high enough that affordability is not the problem",
         "Unlike janitorial, industrial cleaning pays well. The employee's share of premium clears affordability comfortably and enrollment is driven by whether the plan is good, not by whether it is cheap. That lets you buy a better plan rather than the minimum."),
        ("Turnaround work surges the same way maintenance does",
         "Shutdown and turnaround cleaning triples headcount for weeks. Variable-hour rules and the lookback measurement apply here exactly as they do to maintenance contractors, and the FTE count can cross 50 without any single month feeling large."),
    ],
    cost="Roughly $510 to $760 per employee per month for employee-only coverage before your contribution. The census sits between janitorial and the heavy trades on age. Because wages support it, industrial cleaning contractors commonly contribute 65% to 80% of employee-only and see strong enrollment as a result.",
    participation="Participation is generally healthy in this trade because wages make the employee share manageable and the workforce is more stable than in building services. Where it gets complicated is turnaround surges, which should be handled through a measurement period rather than by enrolling temporary labour.",
    faqs=[
        ("Does health insurance cover the OSHA respirator medical evaluation?",
         "Usually not as a plan benefit - it is an employment-required exam and OSHA puts the cost on the employer. But employees with a regular doctor and controlled chronic conditions clear the evaluation more often and with fewer work restrictions, which is a direct operational benefit to you."),
        ("Do plant contracts require contractors to provide benefits?",
         "It is becoming more common in master service agreements and contractor management programmes, particularly at refineries, chemical plants and food facilities. Requirements vary by owner, so read the MSA - it may set a floor you have to meet regardless of what you would otherwise choose."),
        ("How is this different from a janitorial group?",
         "Wages, mainly. Higher pay means the affordability test is easy, enrollment is stronger, and you can offer a better plan. The workforce is also more stable, so turnover-driven plan design matters less than it does in building services."),
        ("What happens during a turnaround when we double headcount?",
         "Use the lookback measurement method for variable-hour employees rather than enrolling temporary labour. Set the measurement and stability periods in writing before the plan year so a surge does not create an unplanned coverage obligation."),
        ("Does the hazard of the work raise our medical premium?",
         "No. ACA small group medical is community rated on age, ZIP, tier and plan design. Group life and disability underwriting does look at occupation and may limit guaranteed issue amounts for confined-space and hydroblasting classifications."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-multi-location-retailers",
    trade="Multi-Location Retailers",
    h1="Group Health Insurance for Multi-Location Retailers",
    title="Group Health Insurance for Multi-Location Retailers (2027)",
    desc="Health plans for retail groups with several stores. Rating across ZIP codes, part-time and seasonal staff, the ACA lookback and the 50-employee aggregation rule.",
    kw="group health insurance for multi location retailers, retail chain employee benefits, multi store health insurance, retail group health plan, seasonal retail employee health coverage",
    lede="One store is a simple group. Six stores across three counties is a different animal, because every employee is rated on their own home ZIP, part-time hours have to be measured rather than assumed, and commonly owned entities are added together for the 50-employee test whether or not you think of them as one company.",
    challenges=[
        ("Every location is rated separately, on employee home ZIPs",
         "Small group premiums follow each employee's residence, not your corporate address. A group spread across Miami-Dade, Broward and Palm Beach is being rated in three areas on one census. That is normal and manageable, but it means a quote built off your headquarters ZIP is wrong."),
        ("Part-time and seasonal staff have to be measured, not assumed",
         "Retail runs on part-timers whose hours move with the season. Full-time status for ACA purposes is determined by a lookback measurement period. A fourth-quarter holiday ramp is exactly the scenario the measurement and stability period structure exists to handle."),
        ("Common ownership aggregates for the 50-employee test",
         "If you own several store entities, the controlled group rules generally add them together for the applicable large employer calculation. Owners regularly discover they are an ALE across five LLCs none of which individually looks like one. The 2027 penalties are $3,780 and $5,670 per employee respectively."),
        ("Store managers are the retention population that matters",
         "Hourly sales staff turn over and always will. A store manager who knows your inventory, your vendors and your customers is expensive to replace and takes a quarter to become productive. That is the group a class-based benefit is genuinely designed for."),
    ],
    cost="Roughly $440 to $680 per employee per month for employee-only coverage before your contribution, varying by which rating areas your stores sit in. Retail censuses are typically younger than the trades. Many retail groups start with a manager and full-time class at a 60% to 75% contribution rather than covering all hourly staff.",
    participation="Retail participation is helped enormously by valid waivers: part-time employees under 26 on a parent's plan, second-job employees covered elsewhere, and spouses' plans all come out of the calculation. Measure eligible employees after those exclusions before concluding the numbers do not work.",
    faqs=[
        ("How does health insurance work across multiple store locations?",
         "One group plan covers all locations. Each employee is rated on their home ZIP code, so a multi-county group carries a blended rate. You do not need a separate plan per store, and having one is almost always worse."),
        ("Do all my LLCs count together for the 50-employee threshold?",
         "Generally yes, under the controlled group and affiliated service group rules. Commonly owned entities are aggregated for the applicable large employer determination. This surprises multi-store owners constantly and is worth confirming with your CPA before you assume you are under the line."),
        ("Can I cover managers but not hourly sales staff?",
         "Yes, using a bona fide classification such as salaried versus hourly or full-time versus part-time, applied consistently. You cannot select individuals. A manager-and-full-time class is a common starting structure for retail groups."),
        ("What do I do about seasonal holiday hires?",
         "A waiting period keeps them below eligibility, and the lookback measurement method determines full-time status for anyone whose hours vary. There is also a seasonal worker exception in the FTE calculation for workforces that exceed 50 for 120 days or fewer in a year."),
        ("How much does dental and vision add for a retail group?",
         "Roughly $26 to $46 per employee per month for both. In retail, where you are competing for staff against every other store in the plaza, an inexpensive complete-looking package does more recruiting work than the medical plan alone."),
    ],
))

T.append(dict(
    slug="group-health-insurance-for-shipyard-and-marine-contractors",
    trade="Shipyard and Marine Contractors",
    h1="Group Health Insurance for Shipyard and Marine Contractors",
    title="Group Health Insurance for Shipyard and Marine Contractors",
    desc="Health plans for shipyard, marine repair and waterfront contractors. How Longshore Act coverage differs from health insurance, and what group coverage costs a marine trade.",
    kw="health insurance for shipyard workers, health insurance for shipyard contractors, marine contractor employee benefits, boatyard employee health insurance, waterfront contractor group health",
    lede="Shipyard and marine repair employers carry a liability structure nobody else on this list has to think about. Longshore and Harbor Workers coverage handles work injury on the waterfront, and because it is expensive and comprehensive, owners routinely assume it does more than it does. It does not touch health insurance.",
    challenges=[
        ("Longshore coverage is not health insurance and does not replace it",
         "The Longshore and Harbor Workers' Compensation Act covers work-related injury and illness for eligible maritime employment. It does nothing for a cold, a child's asthma, a spouse's surgery or anything off the clock. It is also not minimum essential coverage. Employers conflate the two and their workers find out the hard way."),
        ("Marine trades are a genuinely mixed workforce",
         "A yard runs welders, painters, riggers, mechanics, electricians and yard labour, plus an office. That spread of ages and wages on one census produces a blended rate, and it means a single plan design rarely suits everyone - which is the argument for offering two tiers."),
        ("Blasting and coating work carries respiratory surveillance",
         "Abrasive blasting and marine coatings bring respirator requirements and, in older vessel work, lead and asbestos exposure. The OSHA-required evaluations sit with the employer, but ongoing care for what they reveal sits with the health plan."),
        ("South Florida yards compete with cruise and commercial operators for the same trades",
         "In Miami, Fort Lauderdale and along the river, a good marine welder or systems tech has options with much larger employers who offer full benefits. A small yard without coverage is recruiting against that with one hand tied."),
    ],
    cost="Roughly $520 to $780 per employee per month for employee-only coverage before your contribution. Marine trade censuses tend to skew 35 to 55 across the skilled positions. Most yards we work with contribute 55% to 75% of employee-only and add dental, which is well received in a trade with heavy physical demands.",
    participation="Yards frequently have workers covered through a spouse or through prior military service, and VA and TRICARE coverage are valid waivers that leave the participation calculation. Marine trades carry more veteran coverage than most industries, which usually works in the employer's favour on participation.",
    faqs=[
        ("Does Longshore Act coverage mean I do not need health insurance?",
         "No. Longshore covers work-related injury and illness for eligible maritime employment only. It does not cover ordinary illness, family members, prescriptions unrelated to a work injury, or anything off duty, and it does not count as minimum essential coverage. They are entirely separate."),
        ("Does the hazard of shipyard work raise health premiums?",
         "Not the medical rate. ACA small group medical is community rated on age, ZIP, tier and plan design. Group life and disability underwriting does consider occupation and marine classifications can affect those rates or guaranteed issue limits."),
        ("Can a small boatyard with eight employees get a group plan?",
         "Yes. Coverage generally starts at one enrolled W-2 employee besides the owner. Eight employees is a normal small group case."),
        ("What about workers who are on the water or travelling to vessels?",
         "A national PPO handles crews who travel to vessels or yards out of the area. For a yard whose people are on site daily, a regional network is usually adequate and less expensive."),
        ("Do we need to cover subcontracted trades working in our yard?",
         "No. Subcontractors are not your employees, are not eligible for your plan, and do not count toward participation or toward the 50-employee applicable large employer calculation."),
    ],
))

print("Trades defined: %d" % len(T))


# ============================================================ TRADE PAGE BODY
# Shared scaffolding is deliberately minimal - a CTA and a related-links strip.
# Everything above them is written for the individual trade.
TRADE_BODY = """
<main>
  <section class="section" style="background:linear-gradient(160deg,var(--blue-900),var(--blue-700) 60%,var(--blue-600));color:#fff;padding:56px 0 48px">
    <div class="container" style="max-width:860px">
      <span class="eyebrow" style="background:rgba(255,255,255,.15);color:#fff">Group coverage by trade</span>
      <h1 style="color:#fff">{h1}</h1>
      <p style="color:rgba(255,255,255,.93);font-size:1.06rem">{lede}</p>
      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:22px">
        <a class="btn btn-primary" href="/quote?type=business" style="background:#fff;color:var(--blue-700)">Get group quotes</a>
        <a class="btn" href="/group-health-eligibility-checker" style="border:2px solid rgba(255,255,255,.55);color:#fff">Check if you qualify</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:860px">
      <h2>What actually decides this for {trade_lower}</h2>
      {challenges}
    </div>
  </section>

  <section class="section bg-soft">
    <div class="container" style="max-width:860px">
      <h2>What it costs</h2>
      <p>{cost}</p>
      <h2 style="margin-top:34px">Getting approved: the participation question</h2>
      <p>{participation}</p>
      <div style="background:#fff;border:1px solid var(--line);border-left:3px solid var(--teal);border-radius:10px;padding:16px 18px;margin-top:16px">
        <p style="margin:0;font-size:.93rem">Not sure where you land? The <a href="/group-health-eligibility-checker">group eligibility checker</a> works out your real participation number in about a minute, and the <a href="/employer-health-insurance-cost-calculator">cost calculator</a> shows your monthly share and the payroll tax you get back.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:860px">
      <h2>Which structure fits</h2>
      <p>Four routes are open to a business of this size, and the right one depends on your headcount, your W-2 versus contractor mix, and how much you want to spend per head.</p>
      <ul style="line-height:1.85">
        <li><b>Fully insured small group</b> &mdash; community rated, predictable, and the usual starting point from two enrolled employees up.</li>
        <li><b>Level funded</b> &mdash; often 10&ndash;20% below fully insured for a healthy group, with unused claims dollars refundable. Generally worth quoting from about ten enrolled employees.</li>
        <li><b>ICHRA</b> &mdash; reimburse individual coverage tax-free. No participation requirement, no contribution cap, and it reaches a workforce a group plan cannot.</li>
        <li><b>QSEHRA</b> &mdash; for employers under 50, a fixed tax-free monthly allowance, capped at $6,450 single and $13,100 family for 2026.</li>
      </ul>
    </div>
  </section>

  <section class="section bg-soft">
    <div class="container" style="max-width:860px">
      <h2>{trade} &mdash; common questions</h2>
      {faqhtml}
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:860px">
      <div class="cta-strip">
        <h2>Get real numbers for your crew</h2>
        <p>Send us your census and a licensed VS Health Benefits advisor comes back with actual carrier pricing. Carriers pay our commission, so comparing costs you nothing.</p>
        <a class="btn" href="/quote?type=business" style="background:#fff;color:var(--blue-700)">Get group quotes</a>
      </div>
      <p style="margin-top:26px;font-size:.87rem;color:var(--muted);text-align:center">{related}</p>
    </div>
  </section>
</main>
"""


def challenge_html(items):
    return "\n".join(
        '      <h3 style="margin-top:26px">%s</h3>\n      <p>%s</p>' % (esc(h), esc(p))
        for h, p in items)


def faq_html(faqs):
    return "\n".join(
        '      <details class="fi"><summary>%s</summary><p>%s</p></details>'
        % (esc(q), esc(a)) for q, a in faqs)


def related_for(t, allslugs):
    """Point each trade at its three nearest siblings plus the hub and a tool."""
    fam = {
        "steel": ["concrete", "foundation", "general"], "concrete": ["foundation", "steel", "excavation"],
        "foundation": ["concrete", "excavation", "steel"], "demolition": ["excavation", "concrete", "industrial-maintenance"],
        "excavation": ["foundation", "concrete", "dump-truck"], "tunneling": ["excavation", "pipeline", "foundation"],
        "bridge": ["steel", "general", "concrete"], "pipeline": ["tunneling", "oilfield", "excavation"],
        "general": ["bridge", "steel", "concrete"], "industrial-maintenance": ["industrial-cleaning", "demolition", "pipeline"],
        "refrigerated": ["heavy-haul", "dump-truck", "delivery"], "heavy-haul": ["refrigerated", "oilfield", "dump-truck"],
        "oilfield": ["heavy-haul", "pipeline", "dump-truck"], "dump-truck": ["excavation", "refrigerated", "delivery"],
        "delivery": ["freight-brokers", "refrigerated", "multi-location"], "freight-brokers": ["delivery", "multi-location", "refrigerated"],
        "janitorial": ["industrial-cleaning", "multi-location", "general"], "industrial-cleaning": ["janitorial", "industrial-maintenance", "demolition"],
        "multi-location": ["janitorial", "delivery", "freight-brokers"], "shipyard": ["industrial-cleaning", "steel", "general"],
    }
    key = None
    for k in fam:
        if k.replace("-", "") in t["slug"].replace("-", ""):
            key = k
            break
    sibs = []
    for want in fam.get(key, []):
        for s, name in allslugs:
            if want.replace("-", "") in s.replace("-", "") and s != t["slug"]:
                sibs.append((s, name))
                break
    links = ['<a href="/%s">%s</a>' % (s, n) for s, n in sibs[:3]]
    links.append('<a href="/group-health-insurance-by-industry">All industries</a>')
    links.append('<a href="/employer-health-insurance-cost-calculator">Cost calculator</a>')
    return "Related: " + " &middot; ".join(links)


def build_trade(t, head, header, tail, allslugs):
    url = BASE + "/" + t["slug"]
    h = rehead(head, t["title"], t["desc"], url, t["kw"])
    h += "\n" + schema_blocks(t["title"], t["desc"], url, t["faqs"],
                              t["trade"], ("Group Health Insurance by Industry",
                                           "/group-health-insurance-by-industry"))
    body = TRADE_BODY.format(
        h1=esc(t["h1"]), lede=esc(t["lede"]), trade=esc(t["trade"]),
        trade_lower=esc(t["trade"].lower()),
        challenges=challenge_html(t["challenges"]),
        cost=esc(t["cost"]), participation=esc(t["participation"]),
        faqhtml=faq_html(t["faqs"]), related=related_for(t, allslugs))
    return h + "\n</head>\n<body>\n" + header + "\n" + body + "\n" + tail, body


# ============================================================ TRUCKING CITY PAGES
# The Raleigh page holds positions 3.7-14.4 across an entire city's driver
# searches off one URL. These four replicate it in freight hubs inside states
# where the site already has a state page.
C = []

C.append(dict(
    slug="truck-driver-health-insurance-atlanta-ga",
    city="Atlanta", state="Georgia", st="GA",
    title="Health Insurance for Truck Drivers in Atlanta, GA (2027)",
    desc="Coverage for Atlanta-area truck drivers and small fleets. Network reach for Southeast lanes, Georgia enrollment dates, DOT physicals and 2027 costs.",
    kw="truck driver health insurance atlanta, health insurance for truckers atlanta, atlanta owner operator health insurance, georgia truck driver health insurance, medical insurance for truck drivers atlanta",
    lede="Atlanta is where the Southeast's freight converges. I-75, I-85 and I-20 meet inside I-285, the rail yards move containers all night, and Hartsfield-Jackson keeps a whole ecosystem of air freight and drayage running. If you drive out of Atlanta, you are rarely in Georgia for long &mdash; and that is the single fact that should decide your health plan.",
    local=[
        ("Your lanes leave the state before lunch",
         "Chattanooga is under two hours. Birmingham, Greenville and Jacksonville are a day's work. An Atlanta driver spends more time in Tennessee, Alabama, the Carolinas and Florida than at home, and a Georgia HMO built around metro Atlanta hospitals does not follow you there. Drivers running out of Atlanta need a national PPO, and it is worth paying for."),
        ("Metro Atlanta and rural Georgia are different rating areas",
         "Georgia's rating areas mean a driver living in Fulton or Gwinnett pays a different rate from one in Bartow or Coweta, on identical coverage. If you have moved out from the perimeter to somewhere cheaper, your premium likely changed too, and it is worth re-shopping rather than renewing on autopilot."),
        ("Drayage and intermodal work is home-daily, which changes the answer",
         "Container drayage around the rail yards and the airport gets drivers home most nights. If that is your work, a regional network is genuinely viable and can cut your premium meaningfully compared with the national plan an over-the-road driver needs. This is one of the few places where buying less network is the right call."),
        ("The DOT physical is what actually ends careers here",
         "Georgia drivers lose cards for the same reasons everyone does: blood pressure, sleep apnea, and diabetes that nobody has been managing. All three are handled through routine primary care. A plan you never use because you feel fine is still the thing that keeps your medical certificate at two years instead of one."),
    ],
    cost="For a single Atlanta driver in his forties, a mid-range individual plan commonly runs somewhere in the mid hundreds per month before any subsidy, with metro rating areas priced above rural Georgia. For a small fleet putting company drivers on a group plan, budget roughly $520 to $790 per employee per month for employee-only coverage before the employer contribution.",
    fleet="A small Atlanta fleet can set up group coverage with as few as one enrolled W-2 driver besides the owner. Leased owner-operators are 1099 and cannot be on the group plan or counted toward participation - which also means a fleet with five company drivers is judged on five people, not on the forty trucks under its authority.",
    faqs=[
        ("What health insurance works best for Atlanta truck drivers?",
         "A national PPO for anyone running the Southeast corridors, because Atlanta lanes leave Georgia constantly and a metro-Atlanta network is emergency-only once you cross a state line. For home-daily drayage and intermodal drivers, a regional Georgia network is usually adequate and cheaper."),
        ("When can I enroll in coverage in Georgia?",
         "Georgia follows the federal marketplace schedule, with open enrollment running November 1 through January 15 for the 2027 plan year. Outside that window you need a qualifying life event - losing coverage, marriage, a birth, or a permanent move."),
        ("Does insurance cover my DOT physical in Atlanta?",
         "Generally no, because it is an employment-required exam rather than treatment. What your plan does cover is the primary care and prescriptions that keep blood pressure and sleep apnea controlled, which is what determines whether you get a two-year card or a one-year card."),
        ("Can a small Atlanta fleet offer drivers health insurance?",
         "Yes, generally from one enrolled W-2 driver besides the owner. The practical question is participation among drivers without other coverage, and there is a window each November 15 to December 15 when carriers must issue January 1 coverage without applying participation minimums."),
        ("I am an owner-operator, not an employee. What are my options?",
         "Individual coverage through the marketplace or off-exchange, with subsidy eligibility based on your net income after business deductions rather than gross revenue. That distinction matters enormously for owner-operators and is the single most common thing drivers get wrong."),
    ],
))

C.append(dict(
    slug="truck-driver-health-insurance-dallas-tx",
    city="Dallas-Fort Worth", state="Texas", st="TX",
    title="Health Insurance for Truck Drivers in Dallas-Fort Worth (2027)",
    desc="Coverage for DFW truck drivers, owner-operators and small fleets. Texas enrollment dates, network reach for I-35 and I-20 lanes, DOT physicals and costs.",
    kw="truck driver health insurance dallas, health insurance for truckers dallas fort worth, texas owner operator health insurance, dfw truck driver medical insurance, health insurance for truck drivers texas",
    lede="Dallas-Fort Worth sits on the intersection of I-35, I-20, I-30 and I-45, with Alliance and the inland port moving freight north and south all year. It is also one of the largest concentrations of owner-operators in the country, which means most drivers here are buying their own coverage rather than being handed a plan.",
    local=[
        ("Most DFW drivers are buying individual coverage, not group",
         "The owner-operator density around Fort Worth and south Dallas means the relevant question for most drivers is not what their carrier offers but what they can buy for themselves. Subsidy eligibility is based on net income after business deductions - fuel, maintenance, depreciation, the per-diem allowance - not on gross settlement revenue."),
        ("I-35 runs to Laredo, and your network should too",
         "Freight moving between DFW and the border is a huge share of Texas trucking. A driver running the I-35 corridor to Laredo or the Valley needs a network that works in South Texas, and rural network adequacy in parts of that corridor is genuinely thin. Verify it rather than assuming."),
        ("Texas has not expanded Medicaid, which changes the low-income picture",
         "In states that did not expand, adults below the poverty line can fall into a coverage gap - earning too little for marketplace subsidies and too much for Medicaid. For an owner-operator having a bad year, that is a real scenario and it is worth understanding before you underestimate your income on an application."),
        ("Heat is an occupational health issue here in a way it is not up north",
         "Texas summers put drivers, and especially flatbed and oilfield haulers, under genuine cardiovascular load. Blood pressure and hydration-related conditions show up in DOT physicals, and a driver with managed hypertension keeps a two-year card while one without loses road time."),
    ],
    cost="A single DFW driver in his forties commonly sees a mid-range individual plan somewhere in the mid hundreds per month before subsidy, with Dallas and Tarrant county rating areas differing from rural North Texas. Small fleets covering company drivers should budget roughly $500 to $780 per employee per month for employee-only coverage before the employer share.",
    fleet="Texas fleets can set up small group coverage from one enrolled W-2 driver besides the owner. The 1099 line matters more in Texas than almost anywhere, given how much of the DFW fleet base runs on leased owner-operators - they cannot be on the group plan, and they do not count toward participation in either direction.",
    faqs=[
        ("How do owner-operators in Dallas qualify for subsidies?",
         "Subsidies are based on modified adjusted gross income - your net business income after deductible expenses, not gross settlements. Owner-operators routinely overestimate their income on applications by reporting revenue, and end up either overpaying all year or skipping coverage entirely when they would have qualified for help."),
        ("When is open enrollment in Texas?",
         "Texas uses the federal marketplace, so open enrollment runs November 1 through January 15 for the 2027 plan year. Outside that, you need a qualifying life event such as losing coverage, moving, marriage or a birth."),
        ("What network do I need for I-35 and border runs?",
         "A national PPO, verified against South Texas and border counties specifically. National branding on a plan does not always mean strong rural network adequacy along that corridor, and it is worth checking before you buy rather than at an urgent care in Laredo."),
        ("Does my health plan pay for a DOT physical in Texas?",
         "Typically not - it is an employment-required exam. But the conditions that cost drivers their cards, principally hypertension and sleep apnea, are managed through covered primary care and prescriptions."),
        ("Can I get coverage if I had a bad year and my income is low?",
         "It depends. Because Texas did not expand Medicaid, very low incomes can fall into a coverage gap between Medicaid eligibility and subsidy eligibility. Talk it through before you file an application with a guessed income figure - the number you report has real consequences either way."),
    ],
))

C.append(dict(
    slug="truck-driver-health-insurance-memphis-tn",
    city="Memphis", state="Tennessee", st="TN",
    title="Health Insurance for Truck Drivers in Memphis, TN (2027)",
    desc="Coverage for Memphis truck drivers and small fleets. Night-shift freight, I-40 and I-55 lanes, Tennessee enrollment dates, DOT physicals and 2027 costs.",
    kw="truck driver health insurance memphis, health insurance for truckers memphis, tennessee truck driver health insurance, memphis owner operator insurance, medical insurance truck drivers tennessee",
    lede="Memphis runs on freight at night. The air hub sorts while the city sleeps, I-40 and I-55 cross here, and the rail yards and drayage operations around them work shifts that do not resemble anyone else's. That schedule is not a detail &mdash; it changes what kind of health plan is actually usable.",
    local=[
        ("Night shift makes access, not price, the deciding factor",
         "A plan is worthless if every in-network provider closes before your shift ends and opens after it starts. Memphis drivers working the sort or night drayage need a network with real urgent care and telehealth access, and telehealth in particular is the single most valuable plan feature for someone whose day starts at 10pm."),
        ("Short-haul drayage and long-haul I-40 need different plans",
         "Yard and drayage drivers are home daily and can use a regional Tennessee network at a meaningfully lower premium. A driver running I-40 to Oklahoma City or Nashville and beyond needs national PPO access. Buying the wrong one of those two is the most common and most expensive mistake made here."),
        ("Tennessee did not expand Medicaid",
         "TennCare eligibility is narrower than in expansion states, which means lower-income drivers and their families can fall into a gap between Medicaid and marketplace subsidy eligibility. It is worth understanding where you actually sit before assuming you do not qualify for help."),
        ("Sleep apnea is the condition that costs Memphis drivers their cards",
         "Irregular shifts, night work and disrupted sleep make sleep apnea more likely to be both present and undiagnosed. It is one of the leading causes of DOT certification problems, and the sleep study and CPAP that address it are covered under a real health plan and not under an occupational accident policy."),
    ],
    cost="A single Memphis driver in his forties typically sees a mid-range individual plan in the mid hundreds per month before any subsidy. Small fleets covering company drivers should budget roughly $500 to $760 per employee per month for employee-only coverage before the employer contribution, with Shelby County rating differing from surrounding rural counties.",
    fleet="A Memphis fleet can start group coverage with one enrolled W-2 driver besides the owner. For drayage operations built on leased owner-operators, the group is the company drivers and office staff only - which is often a much smaller and much more achievable number than the owner assumes.",
    faqs=[
        ("What is the best health plan for a night-shift Memphis driver?",
         "One with strong telehealth and 24-hour urgent care access in network. For someone whose shift runs overnight, a plan with excellent hospital coverage but no after-hours primary care access is functionally hard to use."),
        ("When can I enroll in Tennessee?",
         "Tennessee uses the federal marketplace, with open enrollment November 1 through January 15 for the 2027 plan year. A qualifying life event - losing coverage, moving, marriage, a birth - opens a special enrollment period outside that window."),
        ("Does health insurance cover a sleep study for DOT certification?",
         "A medically necessary sleep study and CPAP therapy are generally covered benefits under a real health plan. The DOT examination itself is not. This is one of the clearest cases where health insurance directly protects a driver's ability to keep working."),
        ("Is occupational accident coverage enough for a Memphis driver?",
         "No. Occ/acc pays for work-related injury only. It does not cover illness, sleep apnea, blood pressure medication, family members or anything off duty, and it is not minimum essential coverage."),
        ("Can a small drayage company offer benefits?",
         "Yes, from one enrolled W-2 driver besides the owner. Leased owner-operators are not eligible and do not count toward participation, so the group is smaller and easier to qualify than most owners expect."),
    ],
))

C.append(dict(
    slug="truck-driver-health-insurance-indianapolis-in",
    city="Indianapolis", state="Indiana", st="IN",
    title="Health Insurance for Truck Drivers in Indianapolis, IN (2027)",
    desc="Coverage for Indianapolis truck drivers and small fleets. Crossroads of America lanes, Indiana enrollment dates, winter driving health, DOT physicals and 2027 costs.",
    kw="truck driver health insurance indianapolis, health insurance for truckers indiana, indiana owner operator health insurance, indianapolis trucking company benefits, medical insurance truck drivers indiana",
    lede="Indianapolis calls itself the Crossroads of America and the freight numbers back it up: I-70, I-65, I-69 and I-74 all pass through, and a large share of the US population is inside a day's drive. That geography makes Indianapolis a regional-run town, which is unusual, and it changes the coverage calculation in the driver's favour.",
    local=[
        ("Regional runs mean you are home more than most drivers",
         "A one-day radius covering a big share of the country means Indianapolis supports far more regional and dedicated work than long OTR. Drivers who are home several nights a week can use a network built around where they live rather than paying for national reach they will not use. That is a real premium saving."),
        ("Winter changes the health risks of the job",
         "Ice, chain-up, longer pre-trips in the cold and the cardiovascular load of physical work in winter conditions are all real. Slips and falls getting in and out of the cab in January are one of the more common injury patterns, and those are health plan events when they happen off the clock."),
        ("Indiana expanded Medicaid, which widens the low-income options",
         "Indiana operates an expanded Medicaid programme, so lower-income drivers and families have a route that does not exist in non-expansion states like Texas or Tennessee. If you have had a lean year, that is worth checking before you assume coverage is unaffordable."),
        ("LTL and dedicated fleets here often already offer benefits",
         "The strong LTL and dedicated presence around Indianapolis means many drivers can compare a company plan with buying their own. Company coverage is usually the better deal when the employer contributes meaningfully, but it is worth comparing rather than assuming - particularly if your spouse also has an offer."),
    ],
    cost="A single Indianapolis driver in his forties typically sees a mid-range individual plan in the mid hundreds per month before subsidy, and Indiana premiums generally compare favourably with the Southeast. Small fleets should budget roughly $490 to $750 per employee per month for employee-only coverage before the employer share.",
    fleet="Indiana fleets can put a group plan in place from one enrolled W-2 driver besides the owner. With the number of regional carriers competing for drivers around Indianapolis, a small fleet without benefits is recruiting against LTL and dedicated operations that have them, which is a hard fight to win on pay alone.",
    faqs=[
        ("Do Indianapolis drivers need a national network?",
         "Less often than drivers in most freight hubs, because so much Indianapolis work is regional and dedicated. If you are home several nights a week, a regional network can save real money without costing you access. Long OTR drivers still need national PPO reach."),
        ("When is open enrollment in Indiana?",
         "Indiana uses the federal marketplace, so open enrollment runs November 1 through January 15 for the 2027 plan year, with special enrollment periods available after a qualifying life event."),
        ("Can I get Medicaid in Indiana as an owner-operator?",
         "Indiana operates an expanded Medicaid programme, so eligibility reaches further up the income scale than in non-expansion states. For an owner-operator whose net income after business deductions is low, it is worth checking rather than assuming you earn too much."),
        ("Does my plan cover a DOT physical in Indiana?",
         "Generally no, since it is an employment-required exam. The primary care and prescriptions that keep blood pressure and sleep apnea under control are covered, and those are what determine whether you keep a two-year card."),
        ("Should I take my company's plan or buy my own?",
         "If your employer contributes meaningfully to the premium, the company plan is almost always the better value, and taking it also means you are not eligible for marketplace subsidies on an affordable offer. Compare them properly rather than assuming either way."),
    ],
))


CITY_BODY = """
<main>
  <section class="section" style="background:linear-gradient(160deg,var(--blue-900),var(--blue-700) 60%,var(--blue-600));color:#fff;padding:56px 0 48px">
    <div class="container" style="max-width:860px">
      <span class="eyebrow" style="background:rgba(255,255,255,.15);color:#fff">{city}, {st}</span>
      <h1 style="color:#fff">Health Insurance for Truck Drivers in {city}, {st}</h1>
      <p style="color:rgba(255,255,255,.93);font-size:1.06rem">{lede}</p>
      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:22px">
        <a class="btn btn-primary" href="/quote" style="background:#fff;color:var(--blue-700)">Get my quote</a>
        <a class="btn" href="/dot-physical-requirements" style="border:2px solid rgba(255,255,255,.55);color:#fff">DOT physical guide</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:860px">
      <h2>What {city} drivers should know first</h2>
      {local}
    </div>
  </section>

  <section class="section bg-soft">
    <div class="container" style="max-width:860px">
      <h2>What it costs in {state}</h2>
      <p>{cost}</p>
      <h2 style="margin-top:34px">Coverage for small {st} fleets</h2>
      <p>{fleet}</p>
      <div style="background:#fff;border:1px solid var(--line);border-left:3px solid var(--teal);border-radius:10px;padding:16px 18px;margin-top:16px">
        <p style="margin:0;font-size:.93rem">Running a fleet? The <a href="/group-health-eligibility-checker">eligibility checker</a> tells you whether your driver count qualifies, and the <a href="/employer-health-insurance-cost-calculator">cost calculator</a> shows your monthly share per driver.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:860px">
      <h2>{city} driver questions</h2>
      {faqhtml}
    </div>
  </section>

  <section class="section bg-soft">
    <div class="container" style="max-width:860px">
      <div class="cta-strip">
        <h2>Get {state} coverage sorted</h2>
        <p>A licensed VS Health Benefits advisor will compare what is actually available where you live and where you run. Free, and we handle the paperwork.</p>
        <a class="btn" href="/quote" style="background:#fff;color:var(--blue-700)">Start my quote</a>
      </div>
      <p style="margin-top:26px;font-size:.87rem;color:var(--muted);text-align:center">More for drivers: <a href="/dot-physical-requirements">DOT physical requirements</a> &middot; <a href="/truck-driver-health-insurance">Truck driver health insurance</a> &middot; <a href="/best-health-insurance-owner-operators">Best plans for owner-operators</a> &middot; <a href="/occupational-accident-vs-health-insurance">Occ/acc vs health insurance</a></p>
    </div>
  </section>
</main>
"""


def build_city(c, head, header, tail):
    url = BASE + "/" + c["slug"]
    h = rehead(head, c["title"], c["desc"], url, c["kw"])
    h += "\n" + schema_blocks(c["title"], c["desc"], url, c["faqs"],
                              "%s, %s" % (c["city"], c["st"]),
                              ("Truck Driver Health Insurance", "/truck-driver-health-insurance"))
    body = CITY_BODY.format(
        city=esc(c["city"]), state=esc(c["state"]), st=esc(c["st"]),
        lede=c["lede"], local=challenge_html(c["local"]),
        cost=esc(c["cost"]), fleet=esc(c["fleet"]), faqhtml=faq_html(c["faqs"]))
    return h + "\n</head>\n<body>\n" + header + "\n" + body + "\n" + tail, body


# ============================================================ DOT PHYSICAL HUB
# Targets the "will I pass / keep my card" cluster: blood pressure requirements
# for dot physical, dot hypertension guidelines, sleep apnea and cdl licence,
# truck driver blood pressure requirements. The existing
# /does-health-insurance-cover-dot-physical page answers the COST question and is
# linked from here rather than duplicated.
DOT = dict(
    slug="dot-physical-requirements",
    title="DOT Physical Requirements 2027: Blood Pressure, Sleep Apnea, Vision",
    desc="What the DOT physical actually checks and why drivers fail. Blood pressure limits and certification lengths, sleep apnea and CPAP, diabetes, vision and hearing standards.",
    kw="dot physical requirements, blood pressure requirements for dot physical, dot hypertension guidelines, sleep apnea and cdl license, truck driver blood pressure requirements, dot medical card requirements, cdl physical requirements",
)

DOT_BODY = """
<main>
  <section class="section" style="background:linear-gradient(160deg,var(--blue-900),var(--blue-700) 60%,var(--blue-600));color:#fff;padding:56px 0 48px">
    <div class="container" style="max-width:880px">
      <span class="eyebrow" style="background:rgba(255,255,255,.15);color:#fff">Driver medical certification</span>
      <h1 style="color:#fff">DOT physical requirements: what they check and why drivers fail</h1>
      <p style="color:rgba(255,255,255,.93);font-size:1.06rem">Almost nobody loses a CDL to a dramatic diagnosis. Cards get shortened or pulled over blood pressure, undiagnosed sleep apnea and uncontrolled blood sugar &mdash; three things that are entirely manageable with a doctor, and entirely unmanaged when a driver has no coverage.</p>
      <div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:22px">
        <a class="btn btn-primary" href="/quote" style="background:#fff;color:var(--blue-700)">Get covered</a>
        <a class="btn" href="/does-health-insurance-cover-dot-physical" style="border:2px solid rgba(255,255,255,.55);color:#fff">What the exam costs</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:880px">
      <h2>Blood pressure is the number that decides your certification length</h2>
      <p>This is the single most consequential part of the exam, and most drivers do not realise that blood pressure does not simply pass or fail &mdash; it sets how long your card lasts. The FMCSA guidance a certified medical examiner works from breaks it into stages:</p>
      <div class="rlist" style="border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:18px 0">
        <div style="display:flex;justify-content:space-between;gap:12px;padding:13px 16px;border-bottom:1px solid var(--line);background:var(--bg-soft)"><span><b>Under 140 / 90</b></span><b>Up to 24-month certificate</b></div>
        <div style="display:flex;justify-content:space-between;gap:12px;padding:13px 16px;border-bottom:1px solid var(--line)"><span><b>140&ndash;159 / 90&ndash;99</b> (stage 1)</span><b>One-time 12-month certificate</b></div>
        <div style="display:flex;justify-content:space-between;gap:12px;padding:13px 16px;border-bottom:1px solid var(--line);background:var(--bg-soft)"><span><b>160&ndash;179 / 100&ndash;109</b> (stage 2)</span><b>One-time 3-month certificate</b></div>
        <div style="display:flex;justify-content:space-between;gap:12px;padding:13px 16px"><span><b>180 / 110 or higher</b> (stage 3)</span><b>Disqualified until reduced</b></div>
      </div>
      <p>The practical consequence is that a driver at 152/94 who could have been at 132/84 on a $12 generic prescription just traded a two-year card for a one-year card, and will be back in the examiner's office in twelve months with the same problem. Once reduced below 140/90, a stage 3 driver can generally be certified again but on a six-month cycle rather than two years.</p>
      <p>Blood pressure is also the most improvable item on this entire page. It responds to medication that costs very little, and the barrier is almost never the drug &mdash; it is having a doctor to prescribe and monitor it, which is what a health plan actually buys you.</p>

      <h2 style="margin-top:38px">Sleep apnea: not a regulation, but it ends careers anyway</h2>
      <p>There is no separate federal rule dedicated to obstructive sleep apnea. What exists is the examiner's obligation to certify only drivers who can operate safely, and untreated OSA with excessive daytime sleepiness does not meet that bar. Examiners screen using the factors in front of them: body mass index, neck circumference, reported snoring and witnessed apnea, high blood pressure, and airway assessment.</p>
      <p>If you are referred for a sleep study, that is not the end of your career &mdash; it is a detour. Drivers diagnosed with OSA are routinely certified once they are on treatment and can document adherence, commonly understood as using CPAP at least four hours a night on 70% of nights. The machine reports the data automatically.</p>
      <p>The important part for coverage: a medically necessary sleep study and CPAP equipment are generally covered health plan benefits. They are not covered by occupational accident policies, which respond only to work-related injury. A driver relying on occ/acc alone is paying for a sleep study out of pocket at a moment when he is already off the road.</p>

      <h2 style="margin-top:38px">Diabetes and blood sugar</h2>
      <p>Insulin-treated diabetes stopped being an automatic disqualification. Under the current pathway, a treating clinician completes the insulin-treated diabetes assessment form, and the certified medical examiner can certify the driver for up to twelve months if blood sugar is stable and well managed. What still disqualifies is instability &mdash; severe hypoglycaemic episodes, or a driver with no recent clinical management at all.</p>
      <p>Urinalysis at the exam checks for protein, blood and sugar. A driver who has never been diagnosed and shows sugar in the urine at the exam is in a much worse position than one whose condition is documented, treated and stable, because the examiner has nothing to certify against.</p>

      <h2 style="margin-top:38px">Vision and hearing</h2>
      <p>Vision requires at least 20/40 acuity in each eye and both together, with or without correction, plus at least 70 degrees of peripheral vision in the horizontal meridian in each eye, and the ability to recognise the colours of traffic signals. Glasses and contacts are fine. Drivers who cannot meet the standard in one eye have a federal vision exemption pathway rather than an automatic end to the career.</p>
      <p>Hearing is tested by the forced whisper test at five feet in at least one ear, or by audiometry if that is inconclusive. Hearing aids are permitted, and a driver who passes with aids must wear them while driving.</p>

      <h2 style="margin-top:38px">What the exam covers, and what your health plan covers</h2>
      <p>The DOT physical itself is an employment-required examination, not treatment, so health plans generally do not pay for it &mdash; we cover that in detail in <a href="/does-health-insurance-cover-dot-physical">does health insurance cover DOT physicals</a>. What a plan does pay for is everything that determines the outcome: the primary care visit, the blood pressure medication, the sleep study, the CPAP, the diabetes management, the eye exam.</p>
      <p>That is the honest case for coverage in this trade. Not that insurance pays for your physical. That being uninsured for two years between physicals is how a driver arrives at the exam with a problem nobody has been treating.</p>
      <div style="background:var(--bg-soft);border-left:3px solid var(--teal);border-radius:10px;padding:16px 18px;margin-top:20px">
        <p style="margin:0;font-size:.93rem"><b>If you are an owner-operator:</b> subsidy eligibility is based on net income after business deductions, not gross settlements &mdash; which is why many drivers who assume they earn too much actually qualify for help. See <a href="/best-health-insurance-owner-operators">plans for owner-operators</a>.</p>
      </div>

      <p style="margin-top:26px;font-size:.85rem;color:var(--muted)">This page describes the standards a certified medical examiner works from and is general information, not medical advice. Your examiner makes the certification decision, and guidance is updated from time to time &mdash; confirm current requirements with your examiner or on the FMCSA National Registry.</p>
    </div>
  </section>

  <section class="section bg-soft">
    <div class="container" style="max-width:880px">
      <h2>DOT physical questions</h2>
      {faqhtml}
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:880px">
      <div class="cta-strip">
        <h2>Keep your card. Get covered.</h2>
        <p>A licensed VS Health Benefits advisor will find a plan that gives you a real doctor and affordable prescriptions &mdash; the two things that keep a two-year card. Free, and we work with drivers every day.</p>
        <a class="btn" href="/quote" style="background:#fff;color:var(--blue-700)">Get my quote</a>
      </div>
      <p style="margin-top:26px;font-size:.87rem;color:var(--muted);text-align:center">More for drivers: <a href="/does-health-insurance-cover-dot-physical">Does insurance cover DOT physicals</a> &middot; <a href="/truck-driver-health-insurance">Truck driver health insurance</a> &middot; <a href="/occupational-accident-vs-health-insurance">Occ/acc vs health insurance</a> &middot; <a href="/cdl-driver-health-insurance">CDL driver coverage</a></p>
    </div>
  </section>
</main>
"""

DOT_FAQS = [
    ("What blood pressure do you need to pass a DOT physical?",
     "Under 140/90 gets you the full certification, up to 24 months. Between 140/90 and 159/99 you can receive a one-time 12-month certificate. From 160/100 to 179/109 it is a one-time three-month certificate. At 180/110 or above you are disqualified until it comes down, and can then generally be certified on a six-month cycle."),
    ("Can you get a CDL medical card with sleep apnea?",
     "Yes. There is no rule barring drivers with obstructive sleep apnea. What disqualifies is untreated apnea with daytime sleepiness. Drivers on CPAP who can document adherence - commonly at least four hours a night on 70% of nights, which the machine records automatically - are routinely certified."),
    ("Will my health insurance pay for a sleep study?",
     "A medically necessary sleep study and CPAP equipment are generally covered health plan benefits, subject to your deductible and plan rules. They are not covered by occupational accident policies, which respond only to work-related injury."),
    ("Can I drive a truck if I take insulin?",
     "Yes, under the current pathway. Your treating clinician completes the insulin-treated diabetes assessment, and a certified medical examiner can certify you for up to twelve months when blood sugar is stable and well managed. Severe hypoglycaemic episodes are what cause problems, not insulin itself."),
    ("What are the vision requirements for a DOT physical?",
     "At least 20/40 in each eye and both together, with or without correction, at least 70 degrees of peripheral vision horizontally in each eye, and the ability to recognise traffic signal colours. Glasses and contacts are permitted. A federal vision exemption programme exists for drivers who cannot meet the standard in one eye."),
    ("How long is a DOT medical card valid?",
     "Up to 24 months at maximum. Shorter certifications - twelve months, six months or three months - are issued when a condition needs monitoring, most commonly elevated blood pressure or diabetes."),
    ("Does health insurance pay for the DOT physical itself?",
     "Generally no, because it is an employment-required examination rather than treatment. What your plan covers is everything that determines whether you pass: the primary care visits, the blood pressure medication, the sleep study, the CPAP and the diabetes management."),
]


def build_dot(head, header, tail):
    url = BASE + "/" + DOT["slug"]
    h = rehead(head, DOT["title"], DOT["desc"], url, DOT["kw"])
    h += "\n" + schema_blocks(DOT["title"], DOT["desc"], url, DOT_FAQS,
                              "DOT Physical Requirements",
                              ("Truck Driver Health Insurance", "/truck-driver-health-insurance"))
    body = DOT_BODY.format(faqhtml=faq_html(DOT_FAQS))
    return h + "\n</head>\n<body>\n" + header + "\n" + body + "\n" + tail, body


def main():
    t_head, t_header, t_tail = shell(TRADE_SRC)
    c_head, c_header, c_tail = shell(CITY_SRC)

    allslugs = [(x["slug"], x["trade"]) for x in T]
    bodies = {}
    n = 0

    for t in T:
        html, body = build_trade(t, t_head, t_header, t_tail, allslugs)
        write(t["slug"] + ".html", html)
        bodies[t["slug"]] = body
        n += 1
    for c in C:
        html, body = build_city(c, c_head, c_header, c_tail)
        write(c["slug"] + ".html", html)
        bodies[c["slug"]] = body
        n += 1
    html, body = build_dot(c_head, c_header, c_tail)
    write(DOT["slug"] + ".html", html)
    bodies[DOT["slug"]] = body
    n += 1

    print("  Emitted %d pages (%d trades, %d cities, 1 DOT hub)" % (n, len(T), len(C)))
    verify_uniqueness(bodies)
    for slug in sorted(bodies):
        words = len(re.sub(r"<[^>]+>", " ", bodies[slug]).split())
        print("    %-58s %4d words" % (slug, words))


if __name__ == "__main__":
    main()

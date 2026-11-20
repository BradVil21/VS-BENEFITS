# -*- coding: utf-8 -*-
"""Six job pages (2026-11-17): plumbers, electricians, landscapers (group + owner),
barbers, nail techs, DoorDash/Instacart drivers (individual, self-employed).
Figures match llms.txt and pages already live. Photos: set IMG[slug] when the
owner sends them; pages render without a photo until then."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_lib as P
SITE = "https://www.vshealthbenefits.com"
TODAY = "2026-11-17"

# slug -> (base image name in /compressed, alt). Swap in owner photos here.
IMG = {
 "health-insurance-for-electricians": ("electrician-lineman-utility-pole", "Electrician working on a utility pole"),
 "health-insurance-for-hvac-technicians": ("hvac-rooftop-technician", "HVAC technician servicing a rooftop unit"),
}

def fig(slug):
    if slug not in IMG: return ""
    b, alt = IMG[slug]
    has900 = os.path.exists("compressed/%s-900.jpg" % b)
    src = "/compressed/%s%s.jpg" % (b, "-900" if has900 else "")
    webp = os.path.exists("compressed/%s-640.webp" % b)
    pic = ('<picture>%s<img src="%s" alt="%s" width="1200" height="675" decoding="async" fetchpriority="high" '
           'style="width:100%%;height:auto;max-height:420px;object-fit:cover;border-radius:16px;display:block"></picture>') % (
        ('<source type="image/webp" srcset="/compressed/%s-640.webp 640w, /compressed/%s.webp 1200w" sizes="(max-width:900px) 100vw, 900px">' % (b, b)) if webp else "",
        src, alt)
    return '<div class="container" style="max-width:900px;margin-top:-12px;margin-bottom:8px">%s</div>' % pic

def section(inner, soft=False, width="820px"):
    return ('\n<section class="section%s">\n  <div class="container" style="max-width:%s">\n%s\n  </div>\n</section>'
            % (" bg-soft" if soft else "", width, inner))

def hero(eyebrow, h1_plain, h1_span, sub, q, calc):
    return """
<section class="hero">
  <div class="container">
    <div style="max-width:780px">
      <span class="eyebrow">%s</span>
      <h1>%s <span>%s</span></h1>
      <p class="hero-sub">%s</p>
      <div class="hero-ctas"><a class="btn btn-primary" href="%s">Get my free quote</a><a class="btn btn-secondary" href="%s">%s</a></div>
      <div class="hero-meta">
        <span><span class="dot"></span>Licensed independent brokerage</span>
        <span><span class="dot"></span>40+ states</span>
        <span><span class="dot"></span>Free, carriers pay our commission</span>
      </div>
    </div>
  </div>
</section>""" % (eyebrow, h1_plain, h1_span, sub, q, calc[0], calc[1])

def cta(h, p, href, label="Get my free quote"):
    return ('<div class="cta-strip"><h2>%s</h2><p>%s</p>'
            '<a class="btn" href="%s" style="background:#fff;color:var(--blue-700)">%s</a></div>' % (h, p, href, label))

def answer(t):
    return ('<div class="highlight-box" style="margin-top:0"><h4>The short answer</h4><p>%s</p></div>' % t)

# ----------------------------------------------------------------- shared text
GROUP_COST = """
    <h2>What group health insurance costs a %(trade)s business</h2>
    <p>Small group coverage for a trade business generally runs about <strong>$350 to $650 per employee per month</strong> for employee-only coverage, before you decide how much the company pays. Most owners cover 50%% to 100%% of the employee&rsquo;s own premium and let employees add family members at their own cost.</p>
    <p>Three things move your rate more than the carrier you pick:</p>
    <ul>
      <li><strong>The ages on your census.</strong> A crew averaging 28 prices very differently from one averaging 48. This is the biggest factor in a small group rate.</li>
      <li><strong>Plan design.</strong> A higher deductible lowers the premium and shifts cost to whoever uses care. It often fits a young crew and rarely fits an older one.</li>
      <li><strong>Funding type.</strong> Fully insured is simple and predictable. <a href="/level-funded-health-insurance-florida">Level-funded</a> asks health questions and can come in lower for a healthy crew.</li>
    </ul>
    <p><a href="/small-business-health-insurance-calculator">Estimate your cost with your real headcount</a>, or send us a census and we price every carrier for you.</p>"""

GROUP_STRUCT = """
    <h2>Plan options that fit a %(trade)s business</h2>
    <div class="vs-tw"><table class="vs-t">
      <thead><tr><th>Option</th><th>Fits when</th><th>Watch for</th></tr></thead>
      <tbody>
        <tr><td>Fully insured small group</td><td>You want predictable rates and no medical questions</td><td>Carriers usually require a share of eligible employees to enroll</td></tr>
        <tr><td><a href="/level-funded-health-insurance-florida">Level-funded</a></td><td>Your crew is young and mostly healthy</td><td>Medical underwriting; renewals move with claims</td></tr>
        <tr><td><a href="/ichra-florida-small-business">ICHRA</a></td><td>You want a fixed monthly cost per employee or class</td><td>Employees buy their own individual plans</td></tr>
        <tr><td>QSEHRA</td><td>Under 50 employees and you want to reimburse premiums</td><td>2026 limits: $6,450 self-only, $13,100 family</td></tr>
        <tr><td>Owner-only coverage</td><td>It&rsquo;s just you, or you and your spouse</td><td>You need an individual plan, not a group plan (see below)</td></tr>
      </tbody>
    </table></div>
    <p style="font-size:.88rem;color:var(--muted)">General product behavior. Carrier rules and your plan documents govern.</p>
    <p>Carriers must accept small groups regardless of participation each year from <strong>November 15 to December 15</strong>, which is the easiest window to start a first plan.</p>"""

OWNER_ONLY = """
    <h2>Just you, or you and a helper?</h2>
    <p>A one-person %(trade)s business, or a husband-and-wife shop with no other employees, generally cannot buy a small group plan. You buy an <strong>individual plan</strong> instead, and that is often the better deal: Marketplace tax credits are based on your <strong>net</strong> business income after expenses, so a %(trade)s owner with a good year on paper may still qualify for help. If your income is too high for a credit, private PPO plans compete on equal terms.</p>
    <p>Either way, self-employed owners can usually deduct health insurance premiums. <a href="/self-employed-health-insurance">How self-employed coverage works</a> &middot; <a href="/aca-subsidy-calculator">Check your 2027 subsidy</a></p>"""

PENALTY = """
    <div class="highlight-box">
      <h4>The number that decides what you owe</h4>
      <p><strong>50 full-time equivalent employees.</strong> Under it, offering coverage is your choice and there is no federal penalty. At or over it, the 2027 penalty for offering nothing is <strong>$3,780 per full-time employee</strong> (minus the first 30).</p>
    </div>"""

def group_faq(trade, extra):
    return [
     ("How much does health insurance cost for a %s company?" % trade,
      "Small group coverage generally runs about $350 to $650 per employee per month for employee-only coverage before the employer contribution. Your rate depends mostly on employee ages, ZIP code, plan design and funding type. A free quote prices every carrier for your census."),
     ("Does a %s business have to offer health insurance?" % trade,
      "Not until you have 50 full-time equivalent employees. Under that line there is no federal requirement or penalty. At 50 or more, the 2027 penalty for offering no coverage is $3,780 per full-time employee, minus the first 30."),
     ("Can I get health insurance if I'm a one-person %s business?" % trade,
      "Yes, through an individual plan rather than a group plan. Marketplace tax credits are based on your net business income, and self-employed owners can usually deduct their premiums."),
     ("Do 1099 subcontractors count toward 50 employees?",
      "A genuine independent contractor does not count and cannot join your group plan. If you control their hours, tools and methods, they may be employees in practice, which changes the count."),
     ("Is workers' comp enough for my crew?",
      "No. Workers' compensation only pays for injuries from the work. It does not pay for an illness, a heart attack at home or ongoing prescriptions. Health insurance covers everything else."),
    ] + extra

# ----------------------------------------------------------------- GROUP PAGES
def group_page(slug, trade, trade_plural, eyebrow, h1span, sub, intro_h, intro, answer_t, special_h, special, extra_faq, title, desc, kw):
    q = "/quote?type=business&from=" + slug
    faq = group_faq(trade, extra_faq)
    main = "<main>" + "".join([
      hero(eyebrow, "Health insurance for", h1span, sub, q, ("/small-business-health-insurance-calculator", "Estimate my cost")),
      fig(slug),
      section(answer(answer_t) + "\n<h2>%s</h2>\n%s" % (intro_h, intro) + PENALTY),
      section(GROUP_COST % {"trade": trade}, soft=True),
      section(cta("Want the real number for your crew?", "Send us headcount, ages and ZIP codes. We price every carrier that writes %s groups and show them side by side. Free." % trade, q)),
      section("<h2>%s</h2>\n%s" % (special_h, special)),
      section(GROUP_STRUCT % {"trade": trade}, soft=True),
      section(OWNER_ONLY % {"trade": trade}),
      section('<h2>%s health insurance: common questions</h2>\n' % trade.capitalize() + P.faq_html(faq), soft=True),
      section(cta("Get a quote, not a guess", "Tell us your headcount and ZIP. A licensed advisor comes back with every option for your %s, free and with no obligation." % ("business" if trade_plural else "crew"), q)),
    ]) + "</main>"
    return dict(slug=slug, title=title, desc=desc, keywords=kw, main=main, faq=faq, crumb="Group Health Insurance by Industry",
                crumb_url="/group-health-insurance-by-industry", service="Health insurance for %s" % trade_plural)

PLUMB = group_page("health-insurance-for-plumbers", "plumbing", "plumbers and plumbing companies",
  "Plumbing contractors", "plumbers and plumbing companies",
  "Licensed plumbers are hard to hire and harder to keep. Here is what coverage costs a plumbing business in 2027, what the rules require, and the plans that help you keep your best techs.",
  "Why benefits matter more in plumbing than most trades",
  "<p>The licensed plumber shortage means your best journeymen get calls from competitors and union shops every month. Pay matters, but so does the question every tech with a family asks: <em>does the job come with health insurance?</em> A small plumbing shop that offers even a basic plan competes with the big outfits on more than wages.</p><p>Plumbing also carries real health exposure that workers&rsquo; comp does not touch: back and knee wear from years under sinks and in crawl spaces, and the everyday doctor visits, prescriptions and family care that a comp policy never pays for.</p>",
  "Plumbers get health insurance three ways: a <strong>group plan</strong> through a plumbing company (about $350 to $650 per employee per month), an <strong>individual Marketplace plan</strong> priced on net income for self-employed plumbers, or a <strong>private PPO</strong> when income is too high for a tax credit. Shops under 50 employees are not required to offer coverage, but most use it to keep licensed techs.",
  "Apprentices, journeymen and part-time helpers",
  "<p>You can offer coverage to some classes of employees and not others, as long as the classes are based on the job, not on health: full-time versus part-time, field versus office, or after a waiting period of up to 90 days. Many plumbing shops cover licensed plumbers and full-time apprentices from day one and add helpers after the waiting period.</p><p>Part-time hours count toward the 50-employee line as full-time equivalents. <a href='/blog/seasonal-part-time-crew-health-insurance'>Here is how that math works</a>.</p>",
  [("Do plumbing companies usually offer health insurance?", "Larger shops usually do, and many small shops now do to compete for licensed plumbers. Under 50 employees it is optional, so owners often start with employee-only coverage and let staff add family members.")],
  "Health Insurance for Plumbers & Plumbing Companies (2027)",
  "Health insurance for plumbers in 2027: group plans from $350 to $650 per employee, options for self-employed plumbers, and the 50-employee rule.",
  "health insurance for plumbers, plumbing company health insurance, group health insurance for plumbing contractors, self employed plumber health insurance, plumber benefits")

ELEC = group_page("health-insurance-for-electricians", "electrical", "electricians and electrical contractors",
  "Electrical contractors", "electricians and electrical contractors",
  "From two-van shops to crews of 40, here is what health coverage costs an electrical contractor in 2027, how to cover apprentices, and the plan that fits a self-employed electrician.",
  "What electrical contractors are really deciding",
  "<p>Electrical work is high-skill and high-risk, and your licensed people know what they are worth. Union shops offer full benefits, so a non-union contractor without a health plan starts every hiring conversation at a disadvantage.</p><p>Workers&rsquo; comp handles a shock or a fall on the job. It does not pay for a child&rsquo;s ER visit, a diabetes prescription or a cancer screening. That gap is what health insurance fills, and it is what your electricians&rsquo; spouses ask about.</p>",
  "Electricians get health insurance through an <strong>electrical contractor&rsquo;s group plan</strong> (about $350 to $650 per employee per month), an <strong>individual Marketplace plan</strong> priced on net income if self-employed, or a <strong>private PPO</strong> when income is too high for a tax credit. Contractors under 50 employees are not required to offer it, but it is one of the strongest tools for hiring licensed electricians.",
  "Competing with union benefits",
  "<p>You do not need to match a union package dollar for dollar. Most non-union contractors who win hires offer a clear employee-only plan the company pays most of, plus dental and vision, and they say so in the job post. An <a href='/ichra-florida-small-business'>ICHRA</a> lets you set a fixed monthly amount per class (for example, licensed electricians versus apprentices) so cost stays predictable as the crew grows.</p>",
  [("Do non-union electricians get health insurance?", "Only if their employer offers it or they buy their own. Many non-union contractors now offer a group plan or an ICHRA to compete with union shops for licensed electricians.")],
  "Health Insurance for Electricians & Electrical Contractors 2027",
  "Health insurance for electricians in 2027: group plan costs, covering apprentices, competing with union benefits, and plans for self-employed electricians.",
  "health insurance for electricians, electrical contractor health insurance, group health insurance electrical contractors, self employed electrician health insurance, electrician benefits")

LAND = group_page("health-insurance-for-landscaping-companies", "landscaping", "landscaping and lawn care companies",
  "Landscaping and lawn care", "landscaping and lawn care companies",
  "Seasonal crews, H-2B workers and thin margins. Here is what health coverage costs a landscaping company in 2027 and how seasonal workers affect what you owe.",
  "Why landscaping is different",
  "<p>Landscaping payrolls swing with the season. A company with 20 people in January can have 60 in June, and that swing is exactly where owners get confused about the 50-employee rule. The good news: there is a specific <strong>seasonal worker exception</strong> built for businesses like yours.</p><p>Crews work outside in the heat with mowers, trimmers and chemicals. Workers&rsquo; comp covers an injury on the job. It does not cover heat-related illness that shows up at home, ongoing blood pressure medication, or a family member&rsquo;s care.</p>",
  "Landscaping companies are <strong>not required to offer health insurance under 50 full-time equivalent employees</strong>, and a seasonal exception can keep you under that line even if summer headcount goes higher. When you do offer it, group coverage runs about <strong>$350 to $650 per employee per month</strong>. Owners and solo lawn care operators buy individual plans priced on net income.",
  "Seasonal crews and the 50-employee line",
  "<p>If you only go over 50 full-time equivalents for <strong>120 days or fewer</strong> in a year, and only because of seasonal workers, you are generally not treated as a large employer. Many landscaping companies cover their year-round core crew (foremen, crew leads, office) and do not offer coverage to seasonal workers who are not expected to work 30+ hours a week for a full measurement period.</p><p><a href='/blog/seasonal-part-time-crew-health-insurance'>The full guide to counting seasonal and part-time workers</a>.</p>",
  [("Do I have to offer health insurance to seasonal landscaping workers?", "Usually not. Seasonal workers often fall outside the employees you must offer coverage to, and the seasonal worker exception can keep a company under the 50-employee line. The details depend on hours and how long they work.")],
  "Health Insurance for Landscaping & Lawn Care Companies (2027)",
  "Health insurance for landscaping and lawn care companies in 2027: group plan costs, seasonal crews and the 50-employee rule, and plans for solo lawn care owners.",
  "health insurance for landscaping companies, lawn care business health insurance, landscaper health insurance, group health insurance landscaping, seasonal employee health insurance")

# ------------------------------------------------------------ INDIVIDUAL PAGES
SE_COST = """
    <h2>What %(who)s actually pay</h2>
    <p>Most %(who)s are self-employed, so you buy an individual plan. What you pay depends on whether you qualify for a Marketplace tax credit, and that depends on your <strong>net</strong> income after business expenses, not what you take in.</p>
    <div class="vs-tw"><table class="vs-t" style="min-width:0">
      <thead><tr><th>Your situation</th><th>Typical monthly cost</th></tr></thead>
      <tbody>
        <tr><td>Single, net income qualifies for a tax credit</td><td style="white-space:nowrap">Often $0 to $100</td></tr>
        <tr><td>Benchmark silver plan, age 40, before any credit</td><td style="white-space:nowrap">About $704</td></tr>
        <tr><td>Net income above 400%% of poverty (about $63,840 single)</td><td style="white-space:nowrap">Full price; private PPOs compete</td></tr>
      </tbody>
    </table></div>
    <p>Your premiums are usually <strong>tax-deductible</strong> as a self-employed person, which lowers the real cost again. <a href="/aca-subsidy-calculator">See your 2027 price in 60 seconds</a>.</p>"""

SE_INCOME = """
    <h2>The mistake that costs %(who)s the most</h2>
    <p>The Marketplace asks for your expected income. Many %(who)s enter what they take in. The number that counts is <strong>net self-employment income</strong>: what is left after %(expenses)s. Using the gross number can cost you hundreds of dollars a month in lost tax credits.</p>
    <p>If your income changes during the year, update it. If you estimate too low, you may pay some of the credit back at tax time. <a href="/blog/what-income-counts-for-aca-subsidies">Exactly what income counts</a>.</p>"""

def se_faq(who, extra):
    return extra + [
     ("How much is health insurance for %s?" % who,
      "It depends on your net income, age and ZIP code. Many self-employed %s with moderate net income qualify for Marketplace tax credits that bring premiums to $0 to $100 a month. A benchmark silver plan for a 40-year-old costs about $704 a month before any credit." % who),
     ("Can I deduct health insurance as a self-employed %s?" % who.rstrip("s"),
      "Usually yes. Self-employed people can generally deduct health insurance premiums for themselves, a spouse and dependents, as long as they are not eligible for an employer plan through a spouse. Check with your tax preparer."),
     ("When can I sign up?",
      "During Open Enrollment, November 1 to January 15 in most states. Enroll by December 15 for coverage starting January 1. Outside that window you need a qualifying life event, such as losing other coverage."),
    ]

def se_page(slug, who, eyebrow, h1span, sub, answer_t, intro_h, intro, expenses, special_h, special, extra_faq, title, desc, kw, crumb, crumb_url, related):
    q = "/quote?type=individual&from=" + slug
    faq = se_faq(who, extra_faq)
    main = "<main>" + "".join([
      hero(eyebrow, "Health insurance for", h1span, sub, q, ("/aca-subsidy-calculator", "Check my subsidy")),
      fig(slug),
      section(answer(answer_t) + "\n<h2>%s</h2>\n%s" % (intro_h, intro)),
      section(SE_COST % {"who": who}, soft=True),
      section(cta("See your real price", "A licensed advisor checks every plan and tax credit for your ZIP and income. Free, and English y Espa&ntilde;ol.", q)),
      section(SE_INCOME % {"who": who, "expenses": expenses}),
      section("<h2>%s</h2>\n%s" % (special_h, special), soft=True),
      section("<h2>Related guides</h2><ul>%s</ul>" % "".join('<li><a href="%s">%s</a></li>' % (u, t) for t, u in related)),
      section('<h2>Common questions</h2>\n' + P.faq_html(faq), soft=True),
      section(cta("Stop guessing what coverage costs", "Get your free quote in about 2 minutes. No obligation.", q)),
    ]) + "</main>"
    return dict(slug=slug, title=title, desc=desc, keywords=kw, main=main, faq=faq, crumb=crumb, crumb_url=crumb_url,
                service="Health insurance for %s" % who)

BARB = se_page("health-insurance-for-barbers", "barbers", "Barbers and barbershop owners", "barbers",
  "Booth renter, commission barber or shop owner, you are probably buying your own coverage. Here is what barbers pay in 2027 and how to pay less.",
  "Most barbers are self-employed booth renters or 1099 commission barbers, so they <strong>buy an individual health plan</strong>. Marketplace tax credits are based on <strong>net income after expenses</strong> like booth rent and supplies, so many barbers pay <strong>$0 to $100 a month</strong>. Shop owners with employees can also offer a small group plan or an ICHRA.",
  "Booth renter, commission or owner: it changes your options",
  "<ul><li><strong>Booth renters</strong> run their own business. You buy an individual plan and can usually deduct the premium.</li><li><strong>Commission barbers paid on a 1099</strong> are in the same position as booth renters for health insurance.</li><li><strong>W-2 barbers</strong> get whatever the shop offers. If it offers nothing, you buy individually like everyone else.</li><li><strong>Shop owners</strong> with W-2 employees can offer a group plan or an <a href='/ichra-florida-small-business'>ICHRA</a>. With only booth renters, there is no group to cover.</li></ul>",
  "booth rent, clippers, products, licensing and other business costs",
  "Hand, back and standing health",
  "<p>Barbers stand 8 to 10 hours a day and work with their hands and shoulders. Look for a plan that covers physical therapy, specialists and the doctors you already see, not just the lowest premium. We check networks and prescriptions before you choose. If you also want dental and vision, it can be added for a small monthly cost.</p><p>Own the shop? See <a href='/health-insurance-for-salons-and-spas'>group health insurance for salons and barbershops</a>.</p>",
  [("Does a barbershop have to provide health insurance?", "Not unless it has 50 or more full-time equivalent employees, which very few shops do. Booth renters are not the shop's employees, so they buy their own coverage.")],
  "Health Insurance for Barbers (2027): Booth Renters & Shop Owners",
  "Health insurance for barbers in 2027: what booth renters and 1099 barbers pay, how net income lowers your premium, and options for barbershop owners.",
  "health insurance for barbers, barber health insurance, booth renter health insurance, self employed barber health insurance, barbershop health insurance",
  "Self-Employed Health Insurance", "/self-employed-health-insurance",
  [("Self-employed health insurance", "/self-employed-health-insurance"), ("1099 health insurance", "/1099-health-insurance"), ("Group health insurance for salons and barbershops", "/health-insurance-for-salons-and-spas"), ("2027 ACA subsidy calculator", "/aca-subsidy-calculator")])

NAIL = se_page("health-insurance-for-nail-technicians", "nail technicians", "Nail techs and nail salon owners", "nail technicians",
  "Booth renter, commission tech or salon owner, here is what nail technicians pay for health insurance in 2027, and how to pay less.",
  "Most nail technicians are booth renters or 1099 commission techs, so they <strong>buy an individual health plan</strong>. Tax credits are based on <strong>net income after expenses</strong> like booth rent, polish, tools and licensing, so many nail techs pay <strong>$0 to $100 a month</strong>. Salon owners with W-2 staff can offer a group plan or an ICHRA.",
  "How nail techs get covered",
  "<ul><li><strong>Booth renters and 1099 techs</strong> buy individual coverage and can usually deduct the premium.</li><li><strong>W-2 techs</strong> get the salon&rsquo;s plan if it offers one; if not, they buy individually.</li><li><strong>Salon owners</strong> with employees can offer a group plan or an <a href='/ichra-florida-small-business'>ICHRA</a>.</li><li><strong>Couples who run a salon together</strong> with no other employees usually need individual plans, not a group plan.</li></ul>",
  "booth rent, polish and supplies, tools, licensing and other business costs",
  "Coverage that fits nail work",
  "<p>Nail techs spend long hours close to dust and chemical fumes and repeat the same hand and wrist motions all day. A plan with good access to primary care, specialists and prescriptions matters more than the lowest premium. Many techs also add dental and vision.</p><p>Plans and help are available in English y Espa&ntilde;ol. Own the salon? See <a href='/health-insurance-for-salons-and-spas'>group health insurance for salons</a>.</p>",
  [("Do nail salons offer health insurance?", "Some larger salons do. Most nail techs are booth renters or 1099 workers and buy their own plans. Salons with fewer than 50 full-time equivalent employees are not required to offer coverage.")],
  "Health Insurance for Nail Technicians (2027): Costs & Options",
  "Health insurance for nail technicians in 2027: what booth renters and 1099 nail techs pay, how net income lowers premiums, and options for nail salon owners.",
  "health insurance for nail technicians, nail tech health insurance, nail salon health insurance, self employed nail technician insurance, booth renter health insurance",
  "Self-Employed Health Insurance", "/self-employed-health-insurance",
  [("Self-employed health insurance", "/self-employed-health-insurance"), ("1099 health insurance", "/1099-health-insurance"), ("Group health insurance for salons", "/health-insurance-for-salons-and-spas"), ("2027 ACA subsidy calculator", "/aca-subsidy-calculator")])

DASH = se_page("health-insurance-for-doordash-drivers", "delivery drivers", "DoorDash, Instacart and delivery drivers", "DoorDash and Instacart drivers",
  "Does DoorDash or Instacart offer health insurance? No, outside a few state programs. Here is how delivery drivers get covered in 2027, and why most pay far less than they expect.",
  "<strong>No, DoorDash and Instacart do not offer health insurance</strong> to drivers and shoppers, because they are independent contractors. California drivers can get a quarterly healthcare stipend under Prop 22 if they meet hours rules and already have a qualifying plan. Everywhere else, delivery drivers buy an individual plan, and because tax credits use <strong>net income after mileage</strong>, many pay <strong>$0 to $100 a month</strong>.",
  "Does DoorDash or Instacart give you health insurance?",
  "<p>Dashers and full-service Instacart shoppers are independent contractors, not employees, so neither company provides a health plan. A few exceptions are worth knowing:</p><ul><li><strong>California (Prop 22):</strong> drivers who average 15 or more active hours a week in a quarter and already have a qualifying health plan can apply for a quarterly stipend. It helps pay for a plan; it is not a plan itself.</li><li><strong>Portable benefits pilots</strong> in a few states give drivers a small fund they can use toward health costs.</li></ul><p>In Florida and most other states, there is no stipend. You buy your own plan, and that is usually cheaper than people expect.</p>",
  "mileage, phone, insulated bags and other business costs. Mileage alone often cuts a driver&rsquo;s income on paper by thousands of dollars a year",
  "Driving for more than one app",
  "<p>Most drivers run DoorDash, Instacart, Uber Eats and Amazon Flex together. For health insurance, add the net income from all of them. You only need one plan, and it stays with you no matter which apps you drive for or if you stop.</p><p>Drive rideshare too? See <a href='/health-insurance-uber-drivers'>health insurance for Uber and Lyft drivers</a>.</p>",
  [("Does DoorDash offer health insurance?", "No. Dashers are independent contractors and DoorDash does not provide a health plan. In California, eligible Dashers can get a quarterly healthcare stipend under Prop 22 if they average 15 or more active hours a week and already have a qualifying plan."),
   ("Does Instacart offer health insurance to shoppers?", "No. Full-service shoppers are independent contractors and Instacart does not provide health insurance. California shoppers may qualify for a healthcare subsidy under Prop 22.")],
  "Does DoorDash Offer Health Insurance? Delivery Drivers 2027",
  "Does DoorDash or Instacart offer health insurance? No, outside California's Prop 22 stipend. How delivery drivers get covered in 2027, often for $0 to $100/month.",
  "does doordash offer health insurance, doordash health insurance, instacart health insurance, health insurance for delivery drivers, gig worker health insurance, dasher health insurance",
  "Self-Employed Health Insurance", "/self-employed-health-insurance",
  [("Health insurance for Uber and Lyft drivers", "/health-insurance-uber-drivers"), ("1099 health insurance", "/1099-health-insurance"), ("What income counts for ACA subsidies", "/blog/what-income-counts-for-aca-subsidies"), ("2027 ACA subsidy calculator", "/aca-subsidy-calculator")])

HVACT = se_page("health-insurance-for-hvac-technicians", "HVAC technicians", "HVAC techs and self-employed HVAC contractors", "HVAC technicians",
  "Your shop doesn't offer coverage, or you work for yourself? Here is how HVAC techs get health insurance in 2027, what it costs, and how to pay less.",
  "If your HVAC company offers a group plan, that is usually your best deal. If it doesn&rsquo;t, or you&rsquo;re a <strong>self-employed HVAC contractor</strong>, you <strong>buy an individual plan</strong>. Marketplace tax credits are based on your <strong>net income</strong> after truck, tools and other business costs, so many techs pay <strong>$0 to $100 a month</strong>. If your income is above the subsidy cliff, private PPO plans can cost less than full Marketplace price.",
  "Where HVAC techs get health insurance",
  "<ul><li><strong>Your HVAC company&rsquo;s group plan</strong>, if it offers one. Ask what the company pays toward your premium and what adding family costs.</li><li><strong>A spouse&rsquo;s plan</strong> through their job.</li><li><strong>An individual Marketplace (ACA) plan</strong>, with tax credits based on household income. Most HVAC techs who buy their own coverage start here.</li><li><strong>A private PPO</strong>, which can beat Marketplace prices for healthy techs earning too much for a tax credit.</li></ul><p>HVAC techs earn a median of about $61,010 a year (U.S. Bureau of Labor Statistics), and many households at that income qualify for meaningful tax credits.</p>",
  "your truck and fuel, tools and gauges, EPA and state licensing, business insurance and other job costs",
  "Coverage that fits HVAC work",
  "<p>Attics in July, ladders, rooftops and refrigerant. Workers&rsquo; comp covers an injury on the job. It doesn&rsquo;t cover a heat-related illness at home, a kid&rsquo;s ER visit, or your blood pressure medication. Look for a plan with good urgent care, physical therapy and specialist coverage, and check that your doctors are in network.</p><p><strong>Company plan too expensive?</strong> If your share of employee-only coverage costs more than <strong>10.22% of household income</strong> in 2027, you may qualify for Marketplace tax credits instead. Even if it&rsquo;s affordable for you, your spouse and kids may qualify under the family glitch fix.</p><p>Own the shop? See <a href='/health-insurance-for-hvac-companies'>group health insurance for HVAC companies</a> and <a href='/blog/hvac-employee-benefits'>HVAC employee benefits</a>.</p>",
  [("Do HVAC companies offer health insurance?", "Many do, especially larger shops competing for licensed techs. Companies with fewer than 50 full-time equivalent employees aren't required to, so smaller shops may not. If yours doesn't, you can buy an individual plan with tax credits based on income."),
   ("Can I get a tax credit if my HVAC company offers health insurance?", "Usually not, unless the company's coverage is unaffordable (your employee-only premium costs more than 10.22% of household income in 2027) or doesn't meet minimum value. Your spouse and children may still qualify under the family glitch fix.")],
  "Health Insurance for HVAC Technicians (2027): Costs & Options",
  "Health insurance for HVAC techs in 2027: options when your shop offers nothing, costs for self-employed HVAC contractors, and tax credits on net income.",
  "health insurance for hvac technicians, hvac tech health insurance, self employed hvac health insurance, hvac contractor health insurance, health insurance for hvac workers",
  "Self-Employed Health Insurance", "/self-employed-health-insurance",
  [("Group health insurance for HVAC companies", "/health-insurance-for-hvac-companies"), ("HVAC employee benefits", "/blog/hvac-employee-benefits"), ("Self-employed health insurance", "/self-employed-health-insurance"), ("2027 ACA subsidy calculator", "/aca-subsidy-calculator")])

PAGES = [PLUMB, ELEC, LAND, BARB, NAIL, DASH, HVACT]

RELATED = """
<section class="vs-related-guides" data-block="vs-job-pages">
  <div class="vs-rg-inner">
    <h2>Health insurance by job</h2>
    <p class="vs-rg-sub">Find the page for your line of work. Ready for numbers? <a href="/quote" style="color:#16447f;font-weight:700">Get my quote &rarr;</a></p>
    <div class="vs-rg-grid">
      <a class="vs-rg-card" href="/health-insurance-for-plumbers"><strong>Plumbers</strong><span>Plumbing companies and self-employed plumbers.</span><em>See the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/health-insurance-for-electricians"><strong>Electricians</strong><span>Electrical contractors and apprentices.</span><em>See the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/health-insurance-for-landscaping-companies"><strong>Landscapers</strong><span>Lawn care crews and seasonal workers.</span><em>See the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/health-insurance-for-barbers"><strong>Barbers</strong><span>Booth renters and shop owners.</span><em>See the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/health-insurance-for-nail-technicians"><strong>Nail techs</strong><span>Booth renters and salon owners.</span><em>See the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/health-insurance-for-doordash-drivers"><strong>Delivery drivers</strong><span>DoorDash, Instacart and gig work.</span><em>See the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/health-insurance-for-hvac-technicians"><strong>HVAC techs</strong><span>HVAC technicians and self-employed contractors.</span><em>See the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/group-health-insurance-by-industry"><strong>Every industry</strong><span>Costs and plan options by trade.</span><em>Browse all &rarr;</em></a>
    </div>
  </div>
</section>"""

def service_schema(slug, name):
    return {"@context": "https://schema.org", "@type": "Service", "serviceType": name, "name": name, "url": SITE + "/" + slug,
            "provider": {"@type": "InsuranceAgency", "name": "VS Health Benefits", "url": SITE + "/", "telephone": "+1-954-825-1009",
                         "email": "info@vshealthbenefits.com", "address": {"@type": "PostalAddress", "addressLocality": "Miami", "addressRegion": "FL", "addressCountry": "US"}},
            "areaServed": {"@type": "Country", "name": "United States"}}

import re as _re
C = P.Chrome()
for p in PAGES:
    plainq = lambda t: _re.sub(r"<[^>]+>", "", t)
    schemas = [P.breadcrumbs([("Home", "/"), (p["crumb"], p["crumb_url"]), (p["service"].replace("Health insurance for ", "").capitalize(), "/" + p["slug"])]),
               service_schema(p["slug"], p["service"]),
               P.faq_schema([(q, plainq(a)) for q, a in p["faq"]]),
               P.article_schema(p["slug"], p["title"], p["desc"], TODAY)]
    og = "/compressed/%s.jpg" % IMG[p["slug"]][0] if p["slug"] in IMG else "/compressed/hvac-rooftop-technician.jpg"
    html = C.page(p["slug"], p["title"], p["desc"], p["keywords"], p["main"], schemas, og_image=og, related_block=RELATED, sticky_call=True)
    qt = "business" if p["crumb"].startswith("Group") else "individual"
    html = html.replace("from=group-health-insurance-for-dump-truck-fleets&amp;type=business&amp;niche=trucking", "from=%s&amp;type=%s" % (p["slug"], qt))
    html = html.replace("from=group-health-insurance-for-dump-truck-fleets", "from=" + p["slug"])
    assert "dump-truck" not in html.replace("/group-health-insurance-for-dump-truck-fleets\"", ""), p["slug"]
    html = html.replace('href="/quote" data-vs-cta="sticky-quote"', 'href="/quote?from=%s" data-vs-cta="sticky-quote"' % p["slug"])
    print(P.write(p["slug"], html), len(p["title"]), len(p["desc"]))

# -*- coding: utf-8 -*-
"""Two trade pages the industry hub was missing: roofing and childcare.

Roofing: the hub covers general, concrete, excavation, demolition and steel, but
not the trade most likely to be asked about workers' comp and health insurance in
the same sentence. Childcare: high part-time headcount, thin margins, and no page
on the site aimed at it.

House rules carried over: figures come from what the site already publishes, and
regulatory numbers match llms.txt (2027 ALE penalties, affordability, FL statute).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_lib as P

TODAY = "2026-09-16"

def section(inner, soft=False, width="820px"):
    return ('\n<section class="section%s">\n  <div class="container" style="max-width:%s">\n%s\n  </div>\n</section>'
            % (" bg-soft" if soft else "", width, inner))

def hero(eyebrow, h1_plain, h1_span, sub):
    return """
<section class="hero">
  <div class="container">
    <div style="max-width:780px">
      <span class="eyebrow">%s</span>
      <h1>%s <span>%s</span></h1>
      <p class="hero-sub">%s</p>
      <div class="hero-ctas"><a class="btn btn-primary" href="/quote?type=business">Get my group quote</a><a class="btn btn-secondary" href="/small-business-health-insurance-calculator">Estimate the cost</a></div>
      <div class="hero-meta">
        <span><span class="dot"></span>Licensed independent brokerage</span>
        <span><span class="dot"></span>40+ states</span>
        <span><span class="dot"></span>Carriers pay our commission</span>
      </div>
    </div>
  </div>
</section>""" % (eyebrow, h1_plain, h1_span, sub)

def cta(h, p, label="Get my group quote", href="/quote?type=business"):
    return ('<div class="cta-strip"><h2>%s</h2><p>%s</p>'
            '<a class="btn" href="%s" style="background:#fff;color:var(--blue-700)">%s</a></div>' % (h, p, href, label))

RELATED = """
<section class="vs-related-guides" data-block="vs-smallbiz-trades">
  <div class="vs-rg-inner">
    <h2>Before you price a plan</h2>
    <p class="vs-rg-sub">The four things owners ask us first. Ready for numbers? <a href="/quote?type=business" style="color:#16447f;font-weight:700">Get my quote &rarr;</a></p>
    <div class="vs-rg-grid">
      <a class="vs-rg-card" href="/blog/skilled-trades-health-insurance"><strong>What the Trades Actually Pay</strong><span>Per-employee ranges for 2027 and the three things that move your rate.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/blog/seasonal-part-time-crew-health-insurance"><strong>Part-Time and Seasonal Crews</strong><span>Who counts toward the 50-employee line, and who has to be offered coverage.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/blog/workers-comp-vs-health-insurance"><strong>Workers' Comp Is Not Health Insurance</strong><span>What each one pays for, and the gap that sends crews to collections.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-rg-card" href="/group-health-insurance-by-industry"><strong>Every Trade We Cover</strong><span>Costs and plan structures by industry, from concrete to childcare.</span><em>Browse trades &rarr;</em></a>
    </div>
  </div>
</section>"""

# =========================================================================== #
# 1. Roofing
# =========================================================================== #
ROOF_FAQ = [
 ("How much does health insurance cost a roofing company?",
  "For a small roofing crew, group coverage generally runs in the same band as the rest of the trades, roughly $350 to $650 per employee per month for the employee's own coverage, before the employer decides how much of that to pay. Your actual rate is set by the ages of your crew, your ZIP code, the plan design you pick and, on a level-funded plan, the answers on the medical questionnaire. Roofing does not carry a separate 'high risk' health insurance rate the way it does in workers' compensation."),
 ("Does a roofing company have to offer health insurance?",
  "Not until you have 50 full-time equivalent employees. Below that line there is no federal requirement and no penalty, and Florida has no state mandate of its own. At 50 or more full-time equivalents you become an Applicable Large Employer and must offer affordable, minimum-value coverage to at least 95% of full-time employees or face penalties of $3,780 per full-time employee for 2027 if you offer nothing and an employee gets a subsidised marketplace plan."),
 ("Do 1099 subcontractors count toward the 50-employee threshold?",
  "Only if they are misclassified. A genuine independent contractor is not your employee for this purpose and cannot be covered on your group plan. The risk is that a lot of construction 'subs' would not survive scrutiny: if you set their hours, supply the tools and direct the work, a state or federal agency may treat them as employees, which changes your headcount, your workers' compensation exposure and your ACA obligations at the same time."),
 ("Can I cover the crew but not the office?",
  "You can offer different coverage to different classes of employees as long as the classes are defined by bona fide job-based criteria rather than by health status &mdash; hourly versus salaried, field versus office, full-time versus part-time. What you cannot do is pick and choose individuals. An ICHRA makes class-based design cleaner, because you set a different monthly allowance per class."),
 ("What about seasonal crews?",
  "Two separate questions. For counting toward 50 full-time equivalents, there is a seasonal worker exception: if your workforce only exceeds 50 for 120 days or fewer in a year because of seasonal workers, you are generally not an Applicable Large Employer. For who gets offered coverage, the test is hours &mdash; 30 or more hours a week, or 130 hours a month, measured over a period you choose in advance."),
 ("Is workers' compensation enough?",
  "No, and in roofing this gets expensive. Workers' compensation responds to injuries arising out of the work. It does not pay for a heart attack at home, a cancer diagnosis, a kidney stone, or the blood pressure medication your foreman takes. In Florida the construction industry must carry workers' compensation at one or more employees, so roofers usually have it &mdash; and often assume it covers more than it does."),
]

ROOF_MAIN = "<main>" + "".join([
 hero("Roofing contractors",
      "Group health insurance for", "roofing companies",
      "Your crew is on a roof in July and your margins are set at bid. Here is what coverage actually costs a roofing business, what the 50-employee line means for you, and where owners lose money on the wrong plan design."),
 section("""
    <h2>What roofing owners are actually deciding</h2>
    <p>Roofing has two features that make the benefits conversation different from an office business: a workforce that moves between jobs and companies, and a workers' compensation bill that already takes a visible bite out of every dollar of payroll. Owners see health insurance as the next line item in the same column.</p>
    <p>It is not the same line item. Workers' compensation is required by Florida law for construction employers at one employee, and it pays only for work injuries. Health insurance is optional until you hit 50 full-time equivalents, and it pays for everything else &mdash; which is most of what actually happens to people.</p>
    <div class="highlight-box">
      <h4>The number that decides your obligations</h4>
      <p><strong>50 full-time equivalent employees.</strong> Under it, you offer coverage because you want to keep crews. At or over it, you offer coverage because the federal penalty for not offering is $3,780 per full-time employee for 2027.</p>
    </div>
    """),
 section("""
    <h2>What it costs</h2>
    <p>Group coverage for a small trade business generally runs about <strong>$350 to $650 per employee per month</strong> for employee-only coverage, before you decide how much of that the company pays. Family tiers cost more and are usually funded partly by the employee.</p>
    <p>Three things move your number more than the carrier you pick:</p>
    <ul>
      <li><strong>The ages on your census.</strong> A crew averaging 28 prices very differently from one averaging 48. This is the single biggest factor in a small group rate.</li>
      <li><strong>Plan design.</strong> A higher deductible lowers the premium and shifts cost to the person using care. For a young crew that rarely goes to the doctor, that trade often makes sense; for an older crew it usually does not.</li>
      <li><strong>Funding type.</strong> Fully insured is simple and predictable. <a href="/level-funded-health-insurance-florida">Level-funded</a> asks health questions and can come in materially lower for a healthy crew, with a surplus refund if claims run low.</li>
    </ul>
    <p><a href="/small-business-health-insurance-calculator">Run your own numbers</a> with your real headcount before you talk to anyone.</p>
    """, soft=True),
 section(cta("Want the number for your crew?",
   "Send us a census with ages and ZIP codes. We come back with every carrier that will write a roofing group, side by side. Free, and carriers pay our commission.")),
 section("""
    <h2>The 1099 question, honestly</h2>
    <p>Roofing runs on subcontracted labour more than almost any other trade, and the benefits conversation often ends there: &ldquo;my guys are 1099, so this does not apply to me.&rdquo;</p>
    <p>Sometimes that is right. A true independent contractor is not your employee, does not count toward your 50, and cannot be on your group plan. But the classification is decided by how the work actually happens, not by what the paperwork says. If you set the schedule, supply the materials, direct the sequence of work and the person works only for you, an auditor may reach a different conclusion than your invoices do &mdash; and that same conclusion applies to workers' compensation, payroll taxes and your ACA headcount at once.</p>
    <p>Two practical notes. First, if you want to help genuine subcontractors get covered without putting them on a group plan, point them at individual coverage; <a href="/blog/1099-crew-vs-w2-health-insurance">the trade-offs are here</a>. Second, if a large share of your crew would fail a classification test, get that looked at by someone who does it for a living before you build a benefits plan on top of it.</p>
    """),
 section("""
    <h2>Plan structures that fit a roofing business</h2>
    <div class="vs-tw">
    <table class="vs-t">
      <thead><tr><th>Structure</th><th>Fits when</th><th>Watch for</th></tr></thead>
      <tbody>
        <tr><td>Fully insured small group</td><td>You want predictable rates and no medical questions</td><td>Carrier participation rules &mdash; usually a share of eligible employees must enroll</td></tr>
        <tr><td>Level-funded</td><td>Crew is young and generally healthy</td><td>Medical underwriting; rates can move at renewal if claims run high</td></tr>
        <tr><td><a href="/ichra-florida-small-business">ICHRA</a></td><td>Crew sizes swing, or you want a fixed monthly cost per class</td><td>90-day notice, and employees buy their own individual plans</td></tr>
        <tr><td>QSEHRA</td><td>Under 50 employees and you want to reimburse rather than sponsor</td><td>2026 limits are $6,450 self-only and $13,100 family</td></tr>
      </tbody>
    </table>
    </div>
    <p style="font-size:.88rem;color:var(--muted)">General product behaviour. Your carrier's rules and your plan documents govern.</p>
    <p>Participation is where most small roofing groups stall. Florida law sets no participation percentage &mdash; that is a carrier underwriting rule &mdash; and there is a window each year, <strong>15 November to 15 December</strong>, when carriers must accept a group that cannot meet it. <a href="/blog/group-health-insurance-minimum-participation">How that window works.</a></p>
    """, soft=True),
 section('<h2>Roofing health insurance: common questions</h2>\n' + P.faq_html(ROOF_FAQ)),
 section(cta("Get a real quote, not a range",
   "Tell us your headcount, ages and ZIP. We price every carrier that writes roofing groups in your state and show you what each one costs you and your crew.")),
]) + "</main>"

# =========================================================================== #
# 2. Daycare / childcare
# =========================================================================== #
DAY_FAQ = [
 ("Do daycare centers have to provide health insurance?",
  "Not until the center has 50 full-time equivalent employees, which most single-location centers never reach. Below that threshold there is no federal requirement and Florida has no state mandate. Many centers offer coverage anyway, because staff turnover is the most expensive problem in childcare and benefits are one of the few levers that move it."),
 ("How do part-time teachers and aides affect the count?",
  "They count fractionally. Full-time equivalents are calculated by adding all part-time hours in a month, capping each person at 120 hours, dividing by 120, and adding the result to your count of full-time employees. That is how a center with 20 full-time teachers and 30 part-time aides can be closer to the 50-employee line than the owner expects. Only employees working 30 or more hours a week have to be offered coverage."),
 ("What does health insurance cost a childcare center?",
  "Small group coverage generally runs about $350 to $650 per employee per month for employee-only coverage before the employer contribution. Childcare payrolls are tight, which is why many centers use a defined-contribution approach &mdash; the center pays a fixed amount per employee per month and staff choose the plan &mdash; rather than sponsoring a rich plan they cannot sustain."),
 ("Can we contribute a set dollar amount instead of a percentage?",
  "Yes, and for childcare it is often the better structure. An ICHRA lets you set a fixed monthly allowance, which can differ by employee class such as full-time teachers versus part-time aides, and employees buy individual plans with it. There is no minimum company size, no participation requirement, and you control the cost line exactly. A 90-day notice is required before the plan year."),
 ("Is there a tax credit for a small center?",
  "There may be. The small business health care tax credit is worth up to 50% of what the employer pays toward premiums for employers with fewer than 25 full-time equivalents, average wages below an annually adjusted threshold, an employer contribution of at least 50%, and coverage bought through the SHOP marketplace. It runs for two consecutive years. Childcare centers are among the businesses most likely to qualify on the wage test and least likely to know it exists."),
 ("Most of our staff are young. Will they even enroll?",
  "Often not at the rate a carrier wants, which is the practical problem. Many carriers require a share of eligible employees to enroll before they will issue a small group plan, and a young, lower-wage workforce frequently declines. Two ways through it: waivers count for employees with other coverage, such as a spouse's plan, and there is a window each year from 15 November to 15 December when carriers must accept a group that cannot meet participation."),
]

DAY_MAIN = "<main>" + "".join([
 hero("Childcare and daycare",
      "Group health insurance for", "daycare and childcare centers",
      "Tight margins, part-time staff and turnover that eats your year. Here is what coverage costs a childcare center, how part-time hours are counted, and the structures that fit a payroll that cannot absorb surprises."),
 section("""
    <h2>Why this is harder for childcare than for most businesses</h2>
    <p>Three things about a childcare payroll make the standard small-group advice fit badly. A large share of your people are part-time. Wages are low relative to premiums, so the employee's share matters more than the employer's. And turnover is high enough that a plan year rarely ends with the same roster it started with.</p>
    <p>None of that makes coverage impossible. It changes which structure works, and it raises the value of getting the counting right before you talk to a carrier.</p>
    <div class="highlight-box">
      <h4>Two different counts, often confused</h4>
      <p><strong>Who counts toward 50</strong> uses full-time equivalents, which include part-time hours. <strong>Who must be offered coverage</strong> is only employees at 30 or more hours a week. A center can be over the line for the first test and still owe an offer to relatively few people.</p>
    </div>
    """),
 section("""
    <h2>How part-time hours are counted</h2>
    <p>The arithmetic is specific, and it is worth doing once on paper:</p>
    <ol>
      <li>Count employees who average <strong>30 or more hours a week</strong>, or 130 hours a month. Those are your full-time employees.</li>
      <li>Add up all hours worked by everyone else in the month, counting <strong>no more than 120 hours per person</strong>.</li>
      <li>Divide that total by 120. That is your full-time equivalent count from part-time staff.</li>
      <li>Add the two numbers. Fifty or more, averaged across the year, makes you an Applicable Large Employer for the following year.</li>
    </ol>
    <p>For 2027, an Applicable Large Employer that offers nothing and has an employee take a subsidised marketplace plan faces a penalty of <strong>$3,780 per full-time employee</strong> minus the first 30. Coverage that is offered but unaffordable carries <strong>$5,670 per affected employee</strong>. Affordability for 2027 is measured at <strong>10.22%</strong> of household income for the employee's own coverage.</p>
    <p><a href="/blog/seasonal-part-time-crew-health-insurance">The full counting guide, with examples</a>.</p>
    """, soft=True),
 section(cta("Not sure which side of 50 you are on?",
   "Send us a roster with hours. We will do the full-time equivalent math with you and tell you plainly whether anything is required.")),
 section("""
    <h2>Structures that fit a childcare payroll</h2>
    <div class="vs-tw">
    <table class="vs-t">
      <thead><tr><th>Structure</th><th>Why centers pick it</th><th>The catch</th></tr></thead>
      <tbody>
        <tr><td><a href="/ichra-florida-small-business">ICHRA</a></td><td>Fixed monthly cost per employee, can differ for full-time teachers and part-time aides</td><td>Employees buy individual plans; 90-day notice before the plan year</td></tr>
        <tr><td>QSEHRA</td><td>Reimburse premiums without sponsoring a plan; under 50 employees only</td><td>2026 caps: $6,450 self-only, $13,100 family</td></tr>
        <tr><td>Fully insured small group</td><td>Familiar, no medical questions, one plan for everyone</td><td>Carrier participation minimums, which a young staff often misses</td></tr>
        <tr><td>Dental and vision only</td><td>Real benefit at a fraction of medical cost; often the first step</td><td>Not medical coverage, and should not be described as such</td></tr>
      </tbody>
    </table>
    </div>
    <p style="font-size:.88rem;color:var(--muted)">General product behaviour. Your carrier's rules and your plan documents govern.</p>
    <p>For a center that has never offered anything, the honest sequence is usually: dental and vision first, then a defined contribution toward individual coverage, then a sponsored medical plan when margins and headcount support it.</p>
    """),
 section("""
    <h2>The turnover math nobody runs</h2>
    <p>Replacing a qualified lead teacher is not a line item most centers track, but it is real: advertising, background screening, onboarding, the ratio pressure while the role is open, and the parents who notice. Against that, a few hundred dollars a month per employee stops looking like an expense and starts looking like the cheaper side of a trade.</p>
    <p>We are not going to pretend benefits fix turnover on their own. What they do is remove one of the two reasons good teachers leave for a school district job, and the other one is pay.</p>
    """, soft=True),
 section('<h2>Childcare health insurance: common questions</h2>\n' + P.faq_html(DAY_FAQ)),
 section(cta("Price it before you decide",
   "A quote costs nothing and takes a roster. We will show you the sponsored-plan number and the defined-contribution number side by side.")),
]) + "</main>"

PAGES = [
 dict(slug="health-insurance-for-roofing-companies",
      title="Group Health Insurance for Roofing Companies 2027",
      desc="What health coverage costs a roofing crew in 2027, how the 50-employee rule works, the 1099 classification trap, and which plan structures fit the trade.",
      keywords="health insurance for roofing companies, group health insurance roofing contractors, roofing employee benefits, roofer health insurance, construction group health",
      main=ROOF_MAIN, faq=ROOF_FAQ,
      img="/compressed/construction-site-safety-briefing.jpg",
      alt="Roofing and construction crew in a site safety briefing",
      service="Group health insurance for roofing companies"),
 dict(slug="health-insurance-for-daycare-centers",
      title="Group Health Insurance for Daycare & Childcare Centers",
      desc="What coverage costs a childcare center, how part-time teacher hours count toward the 50-employee rule, and the structures that fit a tight payroll.",
      keywords="health insurance for daycare centers, childcare employee benefits, daycare group health insurance, child care center health plans, part time employee health insurance",
      main=DAY_MAIN, faq=DAY_FAQ,
      img="/compressed/kidsplaying.jpg",
      alt="Children playing at a childcare center",
      service="Group health insurance for daycare and childcare centers"),
]

SITE = "https://www.vshealthbenefits.com"

def service_schema(slug, name):
    return {"@context": "https://schema.org", "@type": "Service", "serviceType": name, "name": name,
            "url": SITE + "/" + slug,
            "provider": {"@type": "InsuranceAgency", "name": "VS Health Benefits", "url": SITE + "/",
                         "telephone": "+1-954-866-6872", "email": "info@vshealthbenefits.com",
                         "address": {"@type": "PostalAddress", "addressLocality": "Miami",
                                     "addressRegion": "FL", "addressCountry": "US"}},
            "areaServed": {"@type": "Country", "name": "United States"}}

C = P.Chrome()
for p in PAGES:
    schemas = [
        P.breadcrumbs([("Home", "/"), ("Group Health Insurance by Industry", "/group-health-insurance-by-industry"),
                       (p["title"].split(" 2027")[0].replace("Group Health Insurance for ", ""), "/" + p["slug"])]),
        service_schema(p["slug"], p["service"]),
        P.faq_schema(p["faq"]),
    ]
    html = C.page(p["slug"], p["title"], p["desc"], p["keywords"], p["main"], schemas,
                  og_image=p["img"], related_block=RELATED, sticky_call=True)
    P.write(p["slug"], html)

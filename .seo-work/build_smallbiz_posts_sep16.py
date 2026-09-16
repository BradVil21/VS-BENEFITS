# -*- coding: utf-8 -*-
"""Four small-business posts aimed at the trades and service businesses.

Each targets a query family with demand and no page behind it:
  skilled trades health insurance        64 impressions, position 23, no page
  part-time / seasonal counting          asked on every trade call, nothing written
  1099 crew vs W-2                       "1099 contractor health insurance", pos 75
  workers' comp vs health insurance      the most expensive confusion in the trades

Regulatory figures match llms.txt and the rest of the site: 50 FTE threshold,
2027 penalties of $3,780 / $5,670, affordability 10.22%, QSEHRA 2026 caps,
Florida's construction workers' compensation threshold of one employee.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

TODAY = "2026-09-16"

def faq_html(pairs):
    out = ['<h2 id="faq">Frequently asked</h2>']
    for q, a in pairs:
        out.append('<h3>%s</h3>\n      <p>%s</p>' % (q, a))
    return '\n      '.join(out)

# =========================================================================== #
# 1. Skilled trades
# =========================================================================== #
TRADES_FAQ = [
 ("How much is health insurance for a small trade business?",
  "Employee-only group coverage generally runs about $350 to $650 per employee per month before the employer decides its share. Family tiers cost more. The spread inside that range is driven mostly by the ages on your census and the plan design you choose, not by which carrier's name is on the card."),
 ("Do I have to pay the whole premium?",
  "No. Most small employers pay a percentage of the employee-only premium and little or nothing toward dependents. Carriers typically require a minimum employer contribution, commonly around half of the employee-only cost, and Florida law sets no percentage of its own &mdash; that is a carrier underwriting rule rather than a statute."),
 ("What if half my crew says they do not want it?",
  "That is the participation problem, and it stops more small-group applications than price does. Employees with other coverage, such as a spouse's plan or Medicare, usually count as waivers rather than refusals. There is also a window each year from 15 November to 15 December when carriers must accept a group that cannot meet participation."),
 ("Is a health plan really worth it if my competitors do not offer one?",
  "That is exactly the argument for offering one. In trades where every shop pays within a dollar or two an hour of every other shop, benefits are the difference that is hard to match quickly. The honest caveat is that benefits do not fix a pay problem; they win the hire when pay is close."),
 ("Can I offer coverage to my licensed techs but not to helpers?",
  "Yes, provided the classes are based on genuine job criteria rather than on anybody's health. Full-time versus part-time, salaried versus hourly, field versus office are all defensible. Picking individuals is not. An ICHRA makes class-based design cleanest, because you set a different monthly allowance per class."),
 ("What is the cheapest way to offer something?",
  "Usually a defined contribution rather than a sponsored plan: a QSEHRA if you are under 50 employees, or an ICHRA at any size, where you set a fixed monthly amount and employees buy their own coverage. Dental and vision is the other low-cost starting point, though it is not medical coverage and should never be presented as such."),
]
TRADES_TOC = [("cost","What It Costs"),("drivers","What Moves Your Rate"),
              ("structures","Four Ways to Do It"),("participation","The Participation Wall"),
              ("retention","The Retention Math"),("faq","FAQ")]
TRADES_BODY = '''<h2 id="cost">What the trades actually pay</h2>
      <p>Owners ask for a number and get a shrug. Here is the honest version: for a small trade business, employee-only group coverage generally runs <strong>$350 to $650 per employee per month</strong> before you decide how much of that the company pays.</p>
      <p>That range holds fairly steadily across roofing, HVAC, electrical, plumbing, concrete and the rest. Health insurance rates are not set by how dangerous your trade is &mdash; that is workers' compensation. They are set by age, location, plan design and, on some plans, the health of the group.</p>
      <div class="highlight-box">
        <h4>The two numbers that matter</h4>
        <p><strong>Your share</strong> is what the company pays per employee per month. <strong>Their share</strong> is what comes out of the crew's checks. A plan that looks affordable to you and unaffordable to them will fail on participation, which is where most small-group applications die.</p>
      </div>

      <h2 id="drivers">What actually moves your rate</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>Factor</th><th>Effect</th><th>What you can do about it</th></tr></thead>
        <tbody>
          <tr><td>Average age of the crew</td><td>The single biggest factor in a small group rate</td><td>Nothing directly &mdash; but it argues for different plan designs at different crew ages</td></tr>
          <tr><td>Plan design</td><td>A higher deductible lowers premium, raises what a sick employee pays</td><td>Match the design to how your crew actually uses care</td></tr>
          <tr><td>Funding type</td><td>Level-funded can price below fully insured for a healthy group</td><td>Answer the medical questions honestly and compare both</td></tr>
          <tr><td>ZIP code</td><td>Rates and networks vary by county, sometimes sharply</td><td>Check that the hospitals your crew would actually use are in network</td></tr>
          <tr><td>Who enrolls</td><td>Participation rules can block the whole application</td><td>Count waivers properly before you apply</td></tr>
        </tbody>
      </table>
      </div>
      <p style="font-size:.88rem;color:var(--muted)">General product behaviour. Your carrier's rules and plan documents govern.</p>

      <h2 id="structures">Four ways to do it</h2>
      <p><strong>Fully insured small group.</strong> The familiar one. No medical questions, predictable rate for the year, one plan for everyone. In Florida a small employer is 1 to 50 eligible employees and coverage is guaranteed issue, so a small shop cannot be turned away for the health of its people.</p>
      <p><strong>Level-funded.</strong> You pay a fixed monthly amount that covers expected claims, stop-loss and administration, and a surplus comes back if claims run low. It is medically underwritten, so a young healthy crew often prices below fully insured. <a href="/level-funded-health-insurance-florida">How level-funded works in Florida</a>.</p>
      <p><strong>ICHRA.</strong> You set a fixed monthly allowance, employees buy individual plans and get reimbursed tax-free. No minimum company size, no participation requirement, and the cost line is exactly what you decide it is. 90-day notice is required. <a href="/ichra-florida-small-business">The ICHRA guide</a>.</p>
      <p><strong>QSEHRA.</strong> Same idea for employers under 50 employees, with annual caps &mdash; $6,450 self-only and $13,100 family for 2026.</p>

      <h2 id="participation">The participation wall</h2>
      <p>Here is the failure nobody warns small employers about. Most carriers require a share of eligible employees to actually enroll before they will issue a group plan. Trades crews are often young, often already covered on a spouse's plan, and often unwilling to give up $120 a check.</p>
      <p>Two things get you through it. First, waivers usually do not count against you when the employee has other coverage &mdash; a spouse's plan, a parent's plan under 26, Medicare, TRICARE. Count those correctly before you conclude you cannot qualify. Second, there is a window every year, <strong>15 November to 15 December</strong>, when carriers must accept a small group that cannot meet participation or contribution requirements. <a href="/blog/group-health-insurance-minimum-participation">The window, explained</a>.</p>

      <h2 id="retention">The retention math</h2>
      <p>Benefits are not a moral question, they are a cost comparison. What does it cost you when a licensed tech leaves &mdash; the recruiting, the weeks at reduced capacity, the mistakes a new hire makes on somebody's house, the customer who asks why a different person showed up?</p>
      <p>Against that, a few hundred a month per employee is usually the cheaper side of the trade. It is also the thing a competitor down the road cannot match by bumping pay fifty cents an hour.</p>
      <p>Where benefits do not help: if your pay is genuinely below market, a health plan will not keep anyone. Fix pay first, then benefits win the close ones.</p>'''

# =========================================================================== #
# 2. Part-time and seasonal
# =========================================================================== #
SEAS_FAQ = [
 ("Do part-time employees count toward the 50-employee rule?",
  "Yes, fractionally. Add every part-time employee's hours for the month, counting no more than 120 hours per person, divide the total by 120, and add that to your count of full-time employees. The result is your full-time equivalent count. Averaged over the year, 50 or more makes you an Applicable Large Employer for the following year."),
 ("Do I have to offer coverage to part-timers?",
  "No. The offer obligation applies to full-time employees, defined as 30 or more hours a week or 130 hours a month. Part-time employees count toward whether you are a large employer, but they do not have to be offered coverage. Many employers offer it anyway to keep the workforce stable."),
 ("How do seasonal workers change the count?",
  "There is a specific exception. If your workforce exceeds 50 full-time equivalents for 120 days or fewer during the year, and the people pushing you over the line are seasonal workers, you are generally not treated as an Applicable Large Employer. A roofing company that doubles for a busy season may stay under the requirement even though its peak headcount is 70."),
 ("How do I handle employees whose hours swing week to week?",
  "Measure them over a period instead of week by week. The look-back method lets you pick a measurement period of 3 to 12 months, average an employee's hours across it, and then treat that person as full-time or not for a matching stability period regardless of how their hours move in the meantime. You choose the periods in advance and apply them consistently."),
 ("What happens if I get the count wrong?",
  "If you were an Applicable Large Employer and offered nothing, and at least one full-time employee received a premium tax credit on the marketplace, the 2027 penalty is $3,780 per full-time employee minus the first 30. If you offered coverage that was unaffordable or lacked minimum value, it is $5,670 per affected employee. Both are assessed monthly at one twelfth."),
 ("What counts as affordable for 2027?",
  "For 2027 the affordability percentage is 10.22% of household income for the employee's own coverage, up from 9.96% for 2026. Employers generally use one of the IRS safe harbours &mdash; W-2 wages, rate of pay, or the federal poverty line &mdash; rather than trying to know an employee's household income."),
]
SEAS_TOC = [("two","Two Different Questions"),("math","The Full-Time Equivalent Math"),
            ("seasonal","The Seasonal Exception"),("swing","Crews Whose Hours Swing"),
            ("cost","What It Costs to Be Wrong"),("faq","FAQ")]
SEAS_BODY = '''<h2 id="two">Two different questions, constantly confused</h2>
      <p>Every owner with a mixed workforce asks the same thing: do my part-timers count? The answer depends on which question you are actually asking, because there are two, and they have different answers.</p>
      <div class="highlight-box">
        <h4>Keep these separate</h4>
        <p><strong>1. Am I a large employer?</strong> Part-time hours count, fractionally.<br>
        <strong>2. Who must I offer coverage to?</strong> Only employees at 30+ hours a week.</p>
      </div>
      <p>A landscaping company with 30 full-timers and 40 part-timers may be an Applicable Large Employer and still owe an offer of coverage to only those 30 people.</p>

      <h2 id="math">The full-time equivalent math</h2>
      <ol>
        <li>Count everyone averaging <strong>30 or more hours a week</strong>, or 130 hours a month. Those are full-time employees.</li>
        <li>Total the hours of everyone else for the month, counting <strong>no more than 120 hours per person</strong>.</li>
        <li>Divide by 120. That is your full-time equivalent count from part-time staff.</li>
        <li>Add the two. Average the monthly results across the year.</li>
      </ol>
      <p>A worked example. A childcare center has 18 teachers at 35 hours a week and 26 aides averaging 90 hours a month.</p>
      <div class="vs-tw">
      <table class="vs-t">
        <tbody>
          <tr><td>Full-time employees</td><td>18</td></tr>
          <tr><td>Part-time hours (26 &times; 90)</td><td>2,340</td></tr>
          <tr><td>Divided by 120</td><td>19.5 full-time equivalents</td></tr>
          <tr><td><strong>Total</strong></td><td><strong>37.5</strong> &mdash; under the line</td></tr>
        </tbody>
      </table>
      </div>
      <p>Under 50, nothing is required. The same center with 40 aides instead of 26 lands at 48, and one busy season away from the obligation.</p>

      <h2 id="seasonal">The seasonal exception</h2>
      <p>This is the part roofing, landscaping, pool and holiday-retail businesses need to know. If your workforce goes over 50 full-time equivalents for <strong>120 days or fewer</strong> in the year, and the excess is made up of seasonal workers, you are generally not an Applicable Large Employer for that year.</p>
      <p>Two cautions. The 120 days do not have to be consecutive, and they are counted across the whole year. And &ldquo;seasonal&rdquo; means work that is genuinely tied to a season, not simply a busy stretch you have every month.</p>

      <h2 id="swing">Crews whose hours swing</h2>
      <p>Construction and service trades rarely produce a clean 40-hour week. Rather than reclassifying someone every payroll, the rules let you measure.</p>
      <p>Pick a <strong>measurement period</strong> of 3 to 12 months. Average each variable-hour employee's hours across it. Whoever averages 30 or more is treated as full-time for a matching <strong>stability period</strong>, regardless of what their hours do in the meantime. Whoever does not is treated as part-time for that period. You choose the lengths in advance and apply them the same way to everyone in a category.</p>
      <p>The practical benefit: a framer who runs 55 hours in March and 12 in August has one status for the year instead of six.</p>

      <h2 id="cost">What it costs to be wrong</h2>
      <p>For 2027, an Applicable Large Employer that offers nothing, where at least one full-time employee gets a subsidised marketplace plan, faces <strong>$3,780 per full-time employee</strong> minus the first 30. Offering coverage that is unaffordable or lacks minimum value costs <strong>$5,670 per affected employee</strong>. Affordability for 2027 is <strong>10.22%</strong> of household income for employee-only coverage, and most employers use a safe harbour based on W-2 wages or rate of pay rather than guessing at household income.</p>
      <p>The trigger matters as much as the amount: no employee claims a subsidy, no penalty. That is why the counting is worth doing before a marketplace notice arrives rather than after.</p>'''

# =========================================================================== #
# 3. 1099 vs W-2
# =========================================================================== #
C1099_FAQ = [
 ("Can I put 1099 contractors on my group health plan?",
  "No. Group health insurance covers employees. A genuine independent contractor is not an employee, is not eligible for the group plan, and does not count toward your 50 full-time equivalents. If a carrier discovers contractors enrolled on a group plan, it can rescind coverage, which is a far worse outcome than never having offered it."),
 ("How do I help my subs get coverage without putting them on the plan?",
  "Point them at individual coverage and make the introduction. Self-employed people can buy an ACA marketplace plan with premium tax credits based on net profit, or a privately underwritten plan if they are healthy and earn above the subsidy cutoff. They can also deduct premiums above the line. You can make a broker available to them at no cost; what you cannot do is pay their premiums directly without creating tax and classification questions."),
 ("Does paying someone on a 1099 make them a contractor?",
  "No. The form follows the relationship; it does not create it. Classification turns on control &mdash; who sets the hours, who supplies tools and materials, who directs how the work is done, whether the person is free to work for others, and whether the work is a core part of your business. A crew that works only for you, on your schedule, with your equipment, looks like employees to an auditor no matter what form you file."),
 ("What happens if my contractors are reclassified?",
  "Several things at once, which is what makes it expensive: back payroll taxes with penalties and interest, workers' compensation exposure for the period, potential wage-and-hour claims, and a recalculated full-time equivalent count that can pull you over the 50-employee line retroactively. The health insurance consequence is usually the smallest piece of the bill."),
 ("Is there a legitimate way to have a mixed crew?",
  "Yes, and plenty of businesses do. The test is whether each relationship genuinely fits its label. Specialty subs who bring their own crews, carry their own insurance, work for multiple general contractors and bid jobs are contractors. The helper who shows up at your yard every morning at seven in your shirt is not, whatever the paperwork says."),
 ("Can I offer a stipend instead?",
  "Careful here. Cash paid to an employee to buy insurance is taxable wages and does not satisfy an employer mandate. The compliant version of the same idea is an ICHRA or QSEHRA, which reimburses individual premiums tax-free under specific rules. For contractors, neither applies &mdash; they are not employees."),
]
C1099_TOC = [("line","Where the Line Is"),("cost","What Misclassification Costs"),
             ("options","What Each Group Can Actually Get"),("mixed","Running a Mixed Crew"),
             ("do","What To Do This Week"),("faq","FAQ")]
C1099_BODY = '''<h2 id="line">Where the line actually is</h2>
      <p>&ldquo;My guys are all 1099&rdquo; ends a lot of benefits conversations in the trades. Sometimes it is accurate. Often it is a filing choice that has never been tested, and the health insurance question is the least of what rides on it.</p>
      <p>Classification is decided by the relationship, not the form. The questions an auditor asks are about control: who sets the schedule, who supplies the tools and materials, who decides the sequence of the work, whether the person can work for your competitor next week, and whether what they do is the core of your business or a specialty service bought in.</p>
      <div class="highlight-box">
        <h4>The short version</h4>
        <p>A specialty sub who bids the job, brings a crew, carries insurance and works for four other GCs is a contractor. A helper who reports to your yard at 7am, in your shirt, using your tools, on your schedule, is an employee with a 1099.</p>
      </div>

      <h2 id="cost">What getting it wrong costs</h2>
      <p>The health plan is not the expensive part. A reclassification lands several bills at once:</p>
      <ul>
        <li><strong>Payroll taxes</strong> for the period, with penalties and interest.</li>
        <li><strong>Workers' compensation.</strong> In Florida, construction employers must carry coverage at one or more employees, so a reclassified crew means an uninsured period in the eyes of the state.</li>
        <li><strong>Wage and hour exposure</strong>, including overtime that was never paid.</li>
        <li><strong>A recalculated headcount.</strong> Workers who were never counted may push you over 50 full-time equivalents, with the 2027 employer penalties of $3,780 or $5,670 per employee attached.</li>
      </ul>

      <h2 id="options">What each group can actually get</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th></th><th>W-2 employees</th><th>True 1099 contractors</th></tr></thead>
        <tbody>
          <tr><td>Your group health plan</td><td>Eligible</td><td>Not eligible</td></tr>
          <tr><td>Count toward your 50 FTEs</td><td>Yes</td><td>No</td></tr>
          <tr><td>ICHRA or QSEHRA from you</td><td>Yes</td><td>No</td></tr>
          <tr><td>Marketplace subsidy</td><td>Only if your offer is unaffordable</td><td>Yes, based on net profit</td></tr>
          <tr><td>Deduct their own premiums</td><td>No (pre-tax through payroll instead)</td><td>Yes, above the line</td></tr>
        </tbody>
      </table>
      </div>
      <p>That last row is the one worth telling your subs about. A self-employed tradesman generally deducts health premiums above the line, and his subsidy is calculated on <em>net</em> profit after expenses, not on what you paid him. Most of them report the gross and lose the credit. <a href="/blog/what-income-counts-for-aca-subsidies">What counts as income</a>.</p>

      <h2 id="mixed">Running a mixed crew without creating a problem</h2>
      <p>Mixed crews are normal and legal. The discipline is making each relationship match its label, and documenting it: signed subcontractor agreements, certificates of insurance on file, subs who invoice you rather than collecting a check every Friday for hours worked.</p>
      <p>On the benefits side, keep the line clean. Your group plan covers employees. For your subs, the helpful move is an introduction to someone who can quote them individually &mdash; at no cost to you or to them, since carriers pay the commission. It is a genuine benefit to hand a sub, and it creates none of the exposure that paying their premium directly would.</p>

      <h2 id="do">What to do this week</h2>
      <ol>
        <li><strong>List every person who worked for you last month</strong> and mark each one W-2 or 1099.</li>
        <li><strong>For each 1099, answer three questions:</strong> do I set their hours, do I supply the tools, could they work for a competitor tomorrow?</li>
        <li><strong>Anyone where the answers are yes, yes, no</strong> goes on a list to review with your CPA or an employment attorney. Not with your insurance broker &mdash; this is their call, not ours.</li>
        <li><strong>Build the benefits plan on what is left</strong>, once the headcount is real.</li>
      </ol>
      <p>Nothing in this post is legal or tax advice, and classification is genuinely fact-specific. What we can tell you is what it does to your coverage options, which is what the table above is for.</p>'''

# =========================================================================== #
# 4. Workers' comp vs health insurance
# =========================================================================== #
WC_FAQ = [
 ("Is workers' compensation the same as health insurance?",
  "No. Workers' compensation pays for injuries and illnesses arising out of the job, and it is required of most employers by state law. Health insurance pays for illness and injury regardless of how they happened, and it is optional for employers under 50 full-time equivalents. An employee with workers' compensation and no health plan is uncovered for nearly everything that actually happens to people."),
 ("Does workers' comp cover a heart attack at work?",
  "Usually not, and this surprises people. Compensability turns on whether the condition arose out of the employment, not on where the person was standing when it happened. A heart attack on a job site is generally treated as a personal medical event unless unusual work exertion caused it. That claim lands on the employee's health plan, or on the employee."),
 ("Do I have to carry workers' compensation in Florida?",
  "In the construction industry, yes, at one or more employees. Outside construction, the threshold is generally four or more employees, and agriculture has its own rules. Coverage requirements and exemptions are set out in Florida Statutes chapter 440, and contractors are also responsible for verifying that their subcontractors carry it."),
 ("If I have workers' comp, do my employees still need health insurance?",
  "Yes. Workers' compensation is not minimum essential coverage and never has been. It covers a narrow category of events and nothing else &mdash; not a spouse, not a child, not an illness, not a condition diagnosed on a Saturday."),
 ("What about occupational accident coverage?",
  "That is a different product again, most common where workers are not employees, such as owner-operator trucking. It responds to on-duty accidents, excludes illness, and is not health insurance. If someone is selling it as a substitute for medical coverage, ask for the certificate and read what it pays for an inpatient stay."),
 ("Does offering health insurance lower my workers' comp premium?",
  "Not directly. Your workers' compensation rate is driven by classification codes, payroll and your experience modifier. What a health plan can change over time is what happens after an injury: employees with a primary care relationship and treated chronic conditions tend to recover and return to work faster, and that does eventually show up in your experience rating."),
]
WC_TOC = [("difference","The Difference in One Table"),("gap","The Gap Where People Get Hurt"),
          ("florida","What Florida Requires"),("owners","Owners and Exemptions"),
          ("both","Why You Need Both"),("faq","FAQ")]
WC_BODY = '''<h2 id="difference">The difference, in one table</h2>
      <p>Ask a contractor whether the crew is covered and the answer is often &ldquo;yes, we carry comp.&rdquo; Those are different products solving different problems, and the gap between them is where families end up in collections.</p>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>What happens</th><th>Workers' compensation</th><th>Health insurance</th></tr></thead>
        <tbody>
          <tr><td>Falls off a ladder on the job</td><td>Generally responds</td><td>Generally responds</td></tr>
          <tr><td>Heart attack at home Saturday</td><td>No</td><td>Responds</td></tr>
          <tr><td>Cancer diagnosis</td><td>No</td><td>Responds</td></tr>
          <tr><td>Blood pressure medication</td><td>No</td><td>Responds</td></tr>
          <tr><td>Wife's pregnancy</td><td>No</td><td>Responds if she is on the plan</td></tr>
          <tr><td>Child's broken arm</td><td>No</td><td>Responds if the child is on the plan</td></tr>
          <tr><td>Back surgery from an old non-work injury</td><td>No</td><td>Responds</td></tr>
        </tbody>
      </table>
      </div>
      <p style="font-size:.88rem;color:var(--muted)">General product-category behaviour, not a description of any particular policy. Your policy documents govern.</p>

      <h2 id="gap">The gap where people actually get hurt</h2>
      <p>Look at rows two through seven. That is most of what happens to a working adult over a decade, and workers' compensation answers none of it.</p>
      <p>The version we see most often: a foreman in his late forties with no health plan skips the doctor for two years because a visit is cash out of pocket. The blood pressure that would have cost $12 a month to control becomes an emergency. Comp does not pay, because it did not arise out of the work. He has a five-figure bill and your best crew lead is off the schedule for two months.</p>

      <h2 id="florida">What Florida actually requires</h2>
      <p>Workers' compensation rules are set by state. In Florida:</p>
      <ul>
        <li><strong>Construction industry:</strong> coverage required at <strong>one or more employees</strong>.</li>
        <li><strong>Non-construction:</strong> generally required at <strong>four or more employees</strong>.</li>
        <li><strong>Contractors</strong> are responsible for making sure their subcontractors carry it; if a sub is uninsured, the contractor can end up responsible for that sub's employees.</li>
      </ul>
      <p>Requirements, exemptions and penalties live in Florida Statutes chapter 440. Health insurance, by contrast, has no Florida employer mandate at all &mdash; the federal obligation starts at 50 full-time equivalents. <a href="/florida-small-business-health-insurance-requirements">Where that line sits for your business</a>.</p>

      <h2 id="owners">Owners, officers and the exemption trap</h2>
      <p>Construction corporate officers in Florida can file for an exemption from workers' compensation coverage for themselves, within limits. Plenty of owners do it to cut the premium.</p>
      <p>The trap is what it leaves. An exempt owner with no health insurance has nothing at all: not comp, because he exempted himself, and not medical, because he never bought it. He is the person on the roof with the most to lose and the least behind him. If that describes you, price an individual plan before your next renewal &mdash; as a self-employed person you can generally deduct the premiums above the line.</p>

      <h2 id="both">Why the crews you want have both</h2>
      <p>Experienced tradespeople know the difference between these two products, because someone they worked with has been through the gap. Offering a health plan is the single clearest signal that a shop is run properly, and in trades where pay is within a dollar of the shop down the road, it is the thing that makes the difference.</p>
      <p>It also changes what happens after an injury that <em>is</em> covered. Someone with a regular doctor, controlled blood pressure and no untreated conditions recovers faster and returns to work sooner. That shows up in your experience modifier eventually, though nobody should sell you a health plan on that basis alone.</p>'''

POSTS = [
 dict(slug="skilled-trades-health-insurance",
      title="Health Insurance for the Skilled Trades: 2027 Costs",
      h1="Health Insurance for the Skilled Trades: What It Really Costs",
      desc="What group coverage costs a roofing, HVAC, electrical or plumbing business in 2027, what actually moves your rate, and the participation rule that blocks most applications.",
      lede="Owners ask for a number and get a shrug. Here is the range, what moves it, and the four ways to structure coverage for a crew.",
      read_min=9, eyebrow="Small business", img="/compressed/electrician-lineman-utility-pole.jpg",
      alt="Electrician working on a utility pole", toc=TRADES_TOC, body=TRADES_BODY, faq=TRADES_FAQ,
      cta_head="What would it cost your crew?", cta_copy="Send a census with ages and ZIP codes. We price every carrier that will write your trade and show you both numbers: yours and theirs."),
 dict(slug="seasonal-part-time-crew-health-insurance",
      title="Do Part-Time and Seasonal Crews Count for Health Insurance?",
      h1="Do Part-Time and Seasonal Crews Count for Health Insurance?",
      desc="Part-time hours count toward the 50-employee rule but do not have to be offered coverage. The full-time equivalent math, the 120-day seasonal exception, and 2027 penalties.",
      lede="Two questions get confused constantly, and they have different answers. Here is the arithmetic, with the seasonal exception the trades need.",
      read_min=8, eyebrow="Small business", img="/compressed/construction-crew-rebar-column.jpg",
      alt="Construction crew working on a rebar column", toc=SEAS_TOC, body=SEAS_BODY, faq=SEAS_FAQ,
      cta_head="Not sure which side of 50 you are on?", cta_copy="Send a roster with hours. We will run the full-time equivalent math with you and tell you plainly whether anything is required."),
 dict(slug="1099-crew-vs-w2-health-insurance",
      title="1099 Crew or W-2? What It Does to Your Health Plan",
      h1="1099 Crew or W-2 Employees? What It Does to Your Health Plan",
      desc="Contractors cannot go on your group plan and do not count toward 50 employees. Where the classification line sits, what getting it wrong costs, and what each group can actually buy.",
      lede="“My guys are all 1099” ends a lot of benefits conversations. Sometimes it is accurate. Here is what rides on whether it is.",
      read_min=8, eyebrow="Small business", img="/compressed/10-99working.jpg",
      alt="Tradesman reviewing paperwork on a job site", toc=C1099_TOC, body=C1099_BODY, faq=C1099_FAQ,
      cta_head="Mixed crew, and not sure what you can offer?", cta_copy="We will map who is eligible for what, price the group side, and quote your subs individually at no cost to anyone."),
 dict(slug="workers-comp-vs-health-insurance",
      title="Workers' Comp Is Not Health Insurance. Here Is the Gap.",
      h1="Workers' Comp Is Not Health Insurance &mdash; Here Is the Gap",
      desc="Workers' compensation covers injuries arising out of the job and nothing else. The seven-row table every contractor should see, what Florida requires, and the owner exemption trap.",
      lede="“We carry comp” is the most expensive sentence in the trades, because of everything it does not cover.",
      read_min=7, eyebrow="Small business", img="/compressed/construction-site-safety-briefing.jpg",
      alt="Construction crew in a site safety briefing", toc=WC_TOC, body=WC_BODY, faq=WC_FAQ,
      cta_head="Close the gap for your crew", cta_copy="We price group medical alongside what you already carry, and show you what the employee share looks like before you commit."),
]

for p in POSTS:
    build(p["slug"], p["title"], p["h1"], p["desc"], p["lede"], TODAY, p["read_min"],
          p["eyebrow"], p["img"], p["alt"], p["toc"],
          p["body"] + "\n\n      " + faq_html(p["faq"]), p["faq"],
          p["cta_head"], p["cta_copy"], cta_href="/quote?type=business")

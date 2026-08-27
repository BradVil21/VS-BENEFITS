# -*- coding: utf-8 -*-
"""How many employees do you need for group health insurance - FL / TX / MD / KY.
The answer genuinely differs by state and almost every national page gets it wrong."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

FAQ = [
 ("How many employees do you need for group health insurance?",
  "It depends on the state. The federal default at 45 CFR 155.20 is one employee, and Florida and Maryland follow it. Texas and Kentucky both wrote a two-employee floor into state law, so a one-person business in those states cannot buy small group coverage at all. The ceiling is 50 in all four states."),
 ("Does the business owner count toward the employee minimum?",
  "Generally no, and this is where most owners get caught. Maryland Health Connection requires at least one common-law employee on payroll, not including a business owner, sole proprietor or spouse. Federal SHOP rules say the same. Texas is the exception worth knowing: TDI has told carriers they must issue to a Texas small employer with two or more employees even where those two employees are married to one another."),
 ("Can a sole proprietor with no employees get a group plan?",
  "In Florida and Maryland, no, because there is no second person to enrol even where the statute says one. In Texas there is one narrow route - a health group cooperative may admit an eligible single-employee business under Texas Insurance Code section 1501.0581, and small-employer rules then apply to it. Otherwise the realistic options everywhere are individual coverage or an ICHRA funded by a related entity."),
 ("Do part-time employees count toward the 50-employee ceiling?",
  "They count as fractions. Maryland's definition at Insurance Article section 31-101 counts full-time employees, meaning those averaging at least 30 hours a week, plus full-time equivalents calculated monthly by dividing the aggregate hours of everyone else by 120. Seasonal employees are excluded. Counting rules vary in the detail from state to state, which is why a business hovering near 50 should have someone run the arithmetic rather than eyeball it."),
 ("Do 1099 contractors count?",
  "No, in any of the four states. Group health plans cover W-2 employees. Contractors cannot be enrolled whatever they are called internally, and misclassifying them is the single most common reason a group application comes back. If a meaningful share of your workforce is 1099, an ICHRA reaches them where a group plan cannot."),
]

TOC = [("short-answer", "The Short Answer"), ("why", "Why It Differs"),
       ("florida", "Florida"), ("texas", "Texas"), ("maryland", "Maryland"),
       ("kentucky", "Kentucky"), ("counting", "Who Counts"),
       ("group-of-one", "If You're a Group of One"), ("faq", "FAQ")]

BODY = '''<h2 id="short-answer">The short answer, by state</h2>
      <p>Almost every national page on this subject says a small group is &ldquo;1 to 50 employees.&rdquo; That is the federal default, and in half the states we work in it is wrong. Here is what the four states actually require:</p>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>State</th><th>Minimum</th><th>Maximum</th><th>The catch</th></tr></thead>
        <tbody>
          <tr><td><strong>Florida</strong></td><td>1</td><td>50</td><td>Follows the federal default. Carriers still generally want a second enrolled person.</td></tr>
          <tr><td><strong>Texas</strong></td><td><strong>2</strong></td><td>50</td><td>Two separate tests: an average of two last year <em>and</em> two on day one of the plan year.</td></tr>
          <tr><td><strong>Maryland</strong></td><td>1</td><td>50</td><td>Must be one common-law employee who is not the owner, sole proprietor or spouse.</td></tr>
          <tr><td><strong>Kentucky</strong></td><td><strong>2</strong></td><td>50</td><td>Same two-part test as Texas, written into KRS 304.17A-005(44).</td></tr>
        </tbody>
      </table>
      </div>
      <p>If you are a two-person business in Florida you have options. If you are a one-person business in Texas or Kentucky, small group coverage is closed to you and the sooner you know that, the less time you waste.</p>

      <h2 id="why">Why the answer differs at all</h2>
      <p>The Affordable Care Act set a federal floor at 45 CFR 155.20: a small employer is one that &ldquo;employed an average of at least one but not more than 50 employees.&rdquo; But the statute at 42 U.S.C. 300gg-91(e)(1)(B) lets a state elect to regulate coverage sold to very small groups as small group coverage &mdash; and, by extension, lets a state set its own floor. Texas and Kentucky both kept the two-employee definition they had before the ACA. Florida and Maryland did not.</p>
      <p>All four states also declined the option the PACE Act of 2015 handed them to raise the ceiling to 100 employees. So 50 is the top everywhere, and a 51-employee company in any of them is in the large group market with different rules and different pricing.</p>

      <h2 id="florida">Florida: 1 to 50</h2>
      <p>Florida follows the federal definition, so a Florida employer with one W-2 employee besides the owner can set up a group plan. In practice carriers want at least two enrolled people, and they want the employer contributing at least half the employee-only premium. There is no Florida employer mandate below 50 full-time equivalents, so this is a choice rather than an obligation.</p>
      <p>More detail: <a href="/florida-small-business-health-insurance">group health insurance for Florida small business</a> and <a href="/blog/how-many-employees-group-health-insurance-florida">how many employees you need in Florida</a>.</p>

      <h2 id="texas">Texas: two employees, and a spouse rule nobody expects</h2>
      <p>Texas Insurance Code section 1501.002(14) defines a small employer as one that &ldquo;employed an average of at least two employees but not more than 50 employees on business days during the preceding calendar year and who employs at least two employees on the first day of the plan year.&rdquo; Both tests, not either.</p>
      <div class="highlight-box">
        <h4>Two spouses count as a group in Texas</h4>
        <p>Federal guidance does not treat a husband-and-wife business as a group health plan unless there is a common-law employee who is neither spouse. The Texas Department of Insurance has told carriers they may not refuse a Texas group on that basis, because Texas considers a group of two eligible employees a small group regardless of marital status and coverage must be issued. Note this is a Texas-law point &mdash; the SHOP marketplace's own stated eligibility rules still require an employee other than owners, spouses and family members.</p>
      </div>
      <p>One more Texas wrinkle: since a 2013 amendment the count is of <em>all</em> employees, not only the eligible ones. A business with two part-timers who will never enrol still counts them toward the definition.</p>
      <p>More detail: <a href="/texas-small-business-health-insurance">group health insurance for Texas small business</a>.</p>

      <h2 id="maryland">Maryland: up to 50, with one real employee</h2>
      <p>Maryland Insurance Article section 31-101 defines a small employer as one that averaged &ldquo;not more than 50 employees&rdquo; in the preceding calendar year. There is no stated floor in the definition itself. The floor comes from the exchange: Maryland Health Connection for Small Business requires the employer to &ldquo;have at least one common-law employee on payroll, not including a business owner, sole proprietor or spouse.&rdquo;</p>
      <p>Maryland's counting method is spelled out more precisely than most states': full-time employees, meaning those averaging at least 30 hours a week, plus full-time equivalents calculated monthly by dividing the aggregate hours of non-full-time employees by 120. Seasonal employees are excluded.</p>
      <p>More detail: <a href="/maryland-small-business-health-insurance">group health insurance for Maryland small business</a>.</p>

      <h2 id="kentucky">Kentucky: two employees, and no marketplace to check against</h2>
      <p>KRS 304.17A-005(44) uses the same two-part structure as Texas: an average of at least two but not more than 50 employees during the preceding calendar year, and at least two on the first day of the plan year.</p>
      <p>Kentucky has a second complication now. kynect's SHOP marketplace closed to new enrolment after Anthem, its sole issuer, withdrew, so there is no state portal that will tell you whether you qualify. You find out from a carrier or a broker. Confusingly, kynect's own older SHOP training material said &ldquo;1&ndash;50 FTE employees,&rdquo; borrowing the federal phrasing &mdash; but the operative rule for a Kentucky employer buying today is the two-employee statutory definition as the carrier applies it.</p>
      <p>More detail: <a href="/kentucky-small-business-health-insurance">group health insurance for Kentucky small business</a>.</p>

      <h2 id="counting">Who counts, and who quietly does not</h2>
      <p>Two different counts get confused constantly, so it is worth separating them.</p>
      <h3>Counting toward the small employer <em>definition</em></h3>
      <p>This is a headcount of employees over the previous calendar year, generally including part-timers as fractions. It decides which market you are in.</p>
      <h3>Counting toward <em>minimum participation</em></h3>
      <p>This is entirely separate and much more forgiving. Owners, an owner's spouse, COBRA enrollees and retirees come out of the calculation. So does any employee who declines because they already have qualifying coverage from a spouse's plan, a second job, Medicare, Medicaid, TRICARE or the VA &mdash; those are treated as waivers, not refusals. A twelve-person company where five people are on a spouse's plan is measured against seven.</p>
      <p>We wrote that up separately: <a href="/blog/group-health-insurance-minimum-participation">minimum participation and the November window</a>.</p>
      <p>What never counts, in any state: 1099 contractors. They cannot be enrolled on a group plan whatever the internal job title says, and misclassification is the most common reason an application comes back.</p>

      <h2 id="group-of-one">If you are genuinely a group of one</h2>
      <p>You have three routes, in rough order of how often they work:</p>
      <ol>
        <li><strong>Individual coverage.</strong> On the Florida and Texas federal marketplace, on Maryland Health Connection, or on kynect in Kentucky. Straightforward, and if your income qualifies there may be a premium tax credit &mdash; though the enhanced subsidies expired at the end of 2025 and the 400 percent income cliff is back.</li>
        <li><strong>An ICHRA from a related entity.</strong> If you have a business that can reimburse individual premiums tax-free, this gets you a business deduction without needing a second employee. <a href="/ichra-florida-small-business">How ICHRA works &rarr;</a></li>
        <li><strong>A health group cooperative, in Texas only.</strong> Texas statute creates an &ldquo;eligible single-employee business&rdquo; category at section 1501.051(3-a), and section 1501.0581 lets a cooperative admit one, after which small-employer guaranteed-issue, rating and mandated-benefit rules apply. Narrow, but real, and unique to Texas.</li>
      </ol>
      <div class="cta-block">
        <h3>Not sure which side of the line you are on?</h3>
        <p>Send us your headcount and state. We will tell you which market you are in and what it prices at &mdash; free, and with no obligation to buy anything.</p>
        <a class="btn btn-teal" href="/quote?type=business" style="background:#fff;color:var(--blue-700)">Get group quotes &rarr;</a>
      </div>

      <h2 id="faq">Frequently asked</h2>
      <h3>Does the business owner count toward the minimum?</h3>
      <p>Generally no. Maryland and federal SHOP rules both exclude owners, sole proprietors and spouses from the common-law employee requirement. Texas is the exception: two spouses on payroll are a small group under Texas law.</p>
      <h3>What happens if I drop below the minimum mid-year?</h3>
      <p>Guaranteed renewability generally protects the plan through the policy year, but the carrier will look at your census at renewal. If you have dropped below the state's floor, expect the conversation to be about individual coverage or an ICHRA rather than a renewal.</p>
      <h3>Do I have to offer coverage at all?</h3>
      <p>Only at 50 or more full-time equivalent employees, where the federal employer mandate applies. None of Florida, Texas, Maryland or Kentucky has a state employer mandate below that. Below 50 this is a hiring and retention decision, not a compliance one.</p>
      <p class="vs-src">Sources: <a href="https://www.ecfr.gov/current/title-45/section-155.20" rel="nofollow noopener" target="_blank">45 CFR 155.20</a> &middot; <a href="https://statutes.capitol.texas.gov/Docs/IN/htm/IN.1501.htm" rel="nofollow noopener" target="_blank">Tex. Ins. Code ch. 1501</a> &middot; <a href="https://www.tdi.texas.gov/health/faq.html" rel="nofollow noopener" target="_blank">Texas Department of Insurance carrier FAQ</a> &middot; <a href="https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gin&amp;section=31-101&amp;enactments=false" rel="nofollow noopener" target="_blank">Md. Ins. Art. 31-101</a> &middot; <a href="https://www.marylandhealthconnection.gov/smallbusiness-health-coverage-options/" rel="nofollow noopener" target="_blank">MHC for Small Business</a> &middot; <a href="https://apps.legislature.ky.gov/law/statutes/chapter.aspx?id=38715" rel="nofollow noopener" target="_blank">KRS ch. 304 subtitle 17A</a></p>'''

build(slug='how-many-employees-do-you-need-for-group-health-insurance',
      title='How Many Employees for Group Health Insurance?',
      h1='How Many Employees Do You Need for Group Health Insurance? Florida, Texas, Maryland and Kentucky',
      desc='The federal answer is one employee. Texas and Kentucky require two. Here is what each state actually demands, and who counts.',
      lede='Every national page says a small group is 1 to 50 employees. In Texas and Kentucky that is wrong, and finding out after you have picked a plan is expensive. Here is the real answer in four states.',
      published='2026-08-24', read_min=7, eyebrow='Small Business',
      img='/compressed/microgroup.jpg',
      alt='Small business owner counting employees to check group health insurance eligibility',
      toc=TOC, body=BODY, faq=FAQ,
      cta_head='Which market are you in?',
      cta_copy='Send your headcount and state. We will tell you free.')

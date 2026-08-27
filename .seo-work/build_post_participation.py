# -*- coding: utf-8 -*-
"""Minimum participation and the Nov 15 - Dec 15 waiver window.
High-intent: the employer already wants coverage and has hit a wall."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

FAQ = [
 ("What is minimum participation for group health insurance?",
  "The share of eligible employees who have to enrol before a carrier will issue the plan. The usual federal SHOP figure is 70 percent, but it varies: Texas Insurance Code section 1501.154 sets 75 percent, Maryland Health Connection for Small Business requires 60 percent while Maryland statute caps any carrier's demand at 75 percent, and kynect applied 50 percent in Kentucky before its small business marketplace closed."),
 ("Which employees are excluded from the participation calculation?",
  "More than most employers realise. Owners, an owner's spouse, COBRA enrollees and retirees come out entirely. So does any employee who declines because they already have qualifying coverage - a spouse's plan, a second job, Medicare, Medicaid, TRICARE or VA coverage. Those are treated as waivers rather than refusals, so they leave the denominator instead of counting against you."),
 ("What is the November 15 to December 15 window?",
  "A federal rule at 45 CFR 147.104(b)(1) lets a small group carrier confine an employer who cannot meet a participation or contribution requirement to one annual enrolment window running November 15 through December 15. Inside that window the requirement does not apply and guaranteed issue still does. It is the single most useful thing to know if your participation is short."),
 ("Does the November window waive the employer contribution requirement too?",
  "The federal rule covers an employer 'unable to comply with a material plan provision relating to employer contribution or group participation', so both are in scope of the window. Maryland is narrower: its statute at Insurance Article section 15-1206 waives minimum participation only, and there is no Maryland authority waiving a carrier's contribution requirement. Confirm with the specific carrier rather than assuming."),
 ("Can a carrier just refuse my group for low participation?",
  "No. Guaranteed issue means the carrier has to let the group enrol; what it may do is limit that enrolment to the November 15 to December 15 window. The Texas Department of Insurance states this directly in its carrier FAQ: carriers may not refuse to extend coverage to groups that fail to meet minimum participation requirements."),
 ("How do I raise participation without spending more?",
  "Two levers. First, audit the waivers - every person on a spouse's plan or Medicare who is properly documented as having other coverage leaves the denominator, and employers routinely fail to collect those waiver forms. Second, raise the employer contribution on employee-only coverage, which is usually cheaper than it sounds and moves participation more than any amount of persuading."),
]

TOC = [("what", "What It Is"), ("numbers", "The Numbers by State"),
       ("denominator", "Who Comes Out of the Count"), ("window", "The November Window"),
       ("contribution", "Contribution Is Separate"), ("fix", "How to Fix It"), ("faq", "FAQ")]

BODY = '''<h2 id="what">What minimum participation actually is</h2>
      <p>You have decided to offer coverage, you have picked a plan, and the carrier comes back and says not enough of your people enrolled. That is minimum participation, and it stops more small group applications than price does.</p>
      <p>The logic is straightforward. A group plan is priced on the assumption that healthy people enrol alongside sick ones. If only the people with high claims sign up, the pool is worse than the rate assumed. So carriers set a floor on the share of eligible employees who have to be on the plan.</p>
      <p>What almost nobody explains is that the floor is measured against a much smaller denominator than your headcount, and that there is a two-week window every year when it does not apply at all.</p>

      <h2 id="numbers">The numbers, state by state</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>State</th><th>Participation floor</th><th>Where it comes from</th></tr></thead>
        <tbody>
          <tr><td><strong>Texas</strong></td><td><strong>75%</strong></td><td>Tex. Ins. Code 1501.154. Texas is one of the few states healthcare.gov names as above the usual 70 percent.</td></tr>
          <tr><td><strong>Maryland</strong></td><td><strong>60%</strong> on exchange</td><td>MHC for Small Business, uniform across carriers since 1 Nov 2024. Md. Ins. Art. 15-1206 separately caps any carrier at 75 percent.</td></tr>
          <tr><td><strong>Kentucky</strong></td><td><strong>50%</strong> historically</td><td>kynect's SHOP rule. With SHOP now closed to new groups, it is carrier by carrier.</td></tr>
          <tr><td><strong>Florida</strong></td><td>Carrier-set</td><td>Typically in the 70&ndash;75 percent range; check the specific carrier rather than assuming a single Florida number.</td></tr>
          <tr><td>Federal SHOP default</td><td>70%</td><td>Applies where a state has not set its own.</td></tr>
        </tbody>
      </table>
      </div>
      <p>Two things follow. A Texas employer has the hardest threshold of the four and should plan for it from the start. A Maryland employer buying on the exchange has the easiest, and it is uniform &mdash; every participating Maryland carrier applies the same 60 percent, so shopping carriers will not change the answer.</p>

      <h2 id="denominator">Who comes out of the count</h2>
      <p>This is the part that rescues most groups, and it is the part employers most often get wrong &mdash; usually by measuring against total headcount and concluding they cannot qualify.</p>
      <div class="highlight-box">
        <h4>Not counted at all</h4>
        <p>Owners. An owner's spouse. COBRA enrollees. Retirees. None of these belong in the participation calculation in the first place.</p>
      </div>
      <div class="highlight-box">
        <h4>Counted as waivers, not refusals</h4>
        <p>Any employee who declines because they already have qualifying coverage: a spouse's or partner's plan, another job, Medicare, Medicaid, TRICARE or VA coverage. Maryland spells this out in statute &mdash; section 15-1206 excludes employees with spousal group coverage including Medicare, Medicaid and CHAMPUS, and employees under 26 on a parent's plan. Federal SHOP guidance treats them the same way.</p>
      </div>
      <p>Work an example. A twelve-person Texas company. The owner and the owner's spouse are both on payroll, so they come out &mdash; ten left. Four employees are on a spouse's plan and one is on Medicare, all properly documented, so they come out too &mdash; five eligible. At 75 percent, four of those five need to enrol. That is a completely different problem from getting nine of twelve.</p>
      <p>The catch is documentation. Those waivers only count if you have collected them. A signed waiver form recording <em>why</em> each person declined is the difference between qualifying and not, and it is the single most common piece of missing paperwork on a small group application.</p>

      <h2 id="window">The November 15 to December 15 window</h2>
      <p>If the maths still does not work, there is a federal rule almost no employer has heard of.</p>
      <div class="highlight-box">
        <h4>45 CFR 147.104(b)(1)</h4>
        <p>A small group carrier may limit the availability of coverage to an annual enrolment period running <strong>November 15 through December 15</strong> for any plan sponsor unable to comply with a material plan provision relating to employer contribution or group participation. Inside that window, the requirement does not apply.</p>
      </div>
      <p>Two things make it stronger than it sounds. First, guaranteed issue still applies &mdash; the carrier is not permitted to refuse the group, only to confine when it may enrol. The Texas Department of Insurance says so directly in its carrier FAQ: asked whether small employer plans may refuse to extend coverage to groups that fail to meet minimum participation requirements, TDI's answer is a flat &ldquo;No.&rdquo;</p>
      <p>Second, Maryland went further and put it in state law rather than relying on the federal rule. Insurance Article section 15-1206 provides that a carrier &ldquo;may not impose a minimum participation requirement for a small employer group if the small employer group applies for coverage during the period that begins on November 15 and extends through December 15 of any year.&rdquo; Maryland Health Connection confirms the same waiver period applies to renewing groups.</p>
      <p><strong>Do not confuse it with individual open enrollment.</strong> Individual ACA coverage runs November 1 to January 15. The participation waiver is a different, shorter window with a different purpose. Missing it by two weeks means waiting a year.</p>

      <h2 id="contribution">Contribution is a separate rule, and it is not the same 50 percent</h2>
      <p>Employers routinely merge two requirements that have nothing to do with each other.</p>
      <ul>
        <li><strong>What the carrier wants.</strong> Usually at least 50 percent of the employee-only premium. This is a carrier underwriting rule, not law. Texas says so explicitly &mdash; section 1501.153 states the chapter does not require a small employer to contribute, but lets carriers require it in line with their usual practice. Maryland has no statutory minimum either, and its own employer guide is careful to say the 50 percent figure is a tax-credit condition.</li>
        <li><strong>What the tax credit wants.</strong> Paying a uniform percentage of at least 50 percent of employee-only coverage is one of the four conditions of the federal Small Business Health Care Tax Credit. Different rule, same number, which is why they get conflated. <a href="/blog/small-business-health-care-tax-credit-2026">More on the credit &rarr;</a></li>
      </ul>
      <p>Worth noting: Maryland's statutory November window waives participation only. Nothing in section 15-1206 waives a carrier's contribution requirement, so if contribution is your problem in Maryland, the window may not solve it.</p>

      <h2 id="fix">Three ways to fix short participation</h2>
      <ol>
        <li><strong>Audit your waivers first.</strong> Before anything else, collect a signed waiver from every employee who is declining and record why. Other coverage removes them from the denominator; &ldquo;too expensive&rdquo; does not. Employers routinely fail this on paperwork rather than on substance.</li>
        <li><strong>Raise the employee-only contribution.</strong> Going from 50 to 65 or 75 percent of employee-only coverage moves participation more reliably than any amount of internal persuasion, and because employee-only is the cheapest tier the incremental cost is smaller than owners expect. Model it before dismissing it.</li>
        <li><strong>Time the application into the window.</strong> If you are short and it is September, waiting until November 15 may be the whole answer. Your renewal date then anchors to a December or January start, which most small employers find convenient anyway.</li>
      </ol>
      <p>And if none of those work, an ICHRA has no participation requirement at all. You reimburse individual premiums tax-free, and whether one employee or all of them take it up does not affect whether the arrangement is viable. <a href="/ichra-florida-small-business">How ICHRA works &rarr;</a></p>

      <div class="cta-block">
        <h3>Short on participation? Send us the census.</h3>
        <p>We will run the real denominator, tell you whether you already qualify, and if not, what the cheapest route to yes looks like. Free, and carriers pay our commission either way.</p>
        <a class="btn btn-teal" href="/quote?type=business" style="background:#fff;color:var(--blue-700)">Get group quotes &rarr;</a>
      </div>

      <h2 id="faq">Frequently asked</h2>
      <h3>Does a part-time employee count?</h3>
      <p>Participation is measured against <em>eligible</em> employees, and eligibility is defined by your own plan's hours threshold, usually 30 hours a week. Employees below the threshold are not eligible and so are not in the calculation at all.</p>
      <h3>What if someone leaves and we drop below mid-year?</h3>
      <p>Guaranteed renewability generally protects the plan through the policy year. Participation is tested at issue and at renewal, not continuously.</p>
      <h3>Does this apply to level-funded plans?</h3>
      <p>Level-funded arrangements sit under a self-funded structure with a stop-loss policy, so the ACA small group participation rules do not apply in the same way &mdash; but the stop-loss carrier will have its own underwriting requirements, which are often stricter. Do not assume level-funded is the way around a participation problem without checking.</p>
      <p class="vs-src">Sources: <a href="https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-B/part-147/section-147.104" rel="nofollow noopener" target="_blank">45 CFR 147.104</a> &middot; <a href="https://www.tdi.texas.gov/health/faq.html" rel="nofollow noopener" target="_blank">Texas Department of Insurance carrier FAQ</a> &middot; <a href="https://statutes.capitol.texas.gov/Docs/IN/htm/IN.1501.htm" rel="nofollow noopener" target="_blank">Tex. Ins. Code ch. 1501</a> &middot; <a href="https://law.justia.com/codes/maryland/insurance/title-15/subtitle-12/section-15-1206/" rel="nofollow noopener" target="_blank">Md. Ins. Art. 15-1206</a> &middot; <a href="https://www.healthcare.gov/small-businesses/choose-and-enroll/qualify-for-shop-marketplace/" rel="nofollow noopener" target="_blank">healthcare.gov SHOP eligibility</a></p>'''

build(slug='group-health-insurance-minimum-participation',
      title='Minimum Participation for Group Health Insurance',
      h1='Can&rsquo;t Hit Minimum Participation? The Two-Week Window That Suspends It',
      desc='Minimum participation stops more small group applications than price does. Who actually counts, and the November 15 to December 15 rule.',
      lede='Not enough of your people enrolled, so the carrier will not issue the plan. Before you give up: the count is smaller than you think, and there is a federal window every year when the requirement does not apply.',
      published='2026-08-25', read_min=8, eyebrow='Small Business',
      img='/compressed/business-team-meeting.jpg',
      alt='Small business team reviewing group health insurance enrollment and participation requirements',
      toc=TOC, body=BODY, faq=FAQ,
      cta_head='Short on participation?',
      cta_copy='Send the census. We will run the real number for free.')

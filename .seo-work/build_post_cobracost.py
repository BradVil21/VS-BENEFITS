# -*- coding: utf-8 -*-
"""Why is COBRA so expensive. Cost-shock query with no government competition
on the SERP at all - it is entirely broker and content sites."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

FAQ = [
 ("Why is COBRA so much more expensive than what I paid as an employee?",
  "Because your payroll deduction was never the price of the insurance. Your employer was paying most of the premium and you were paying the remainder. COBRA lets the plan charge up to 102 percent of the full cost - the employer's share, your share, and a 2 percent administrative fee. Nothing has been marked up. You have been handed the invoice that used to be split."),
 ("What is the 2 percent COBRA fee for?",
  "Administration. Federal law caps the COBRA charge at 102 percent of the applicable premium, and the extra 2 percent covers the cost of running the continuation coverage - billing, eligibility tracking, notices. Plans are not required to charge it, but almost all do."),
 ("How much does COBRA actually cost per month?",
  "It is the full cost of your specific plan, so it varies. Using the 2025 KFF employer survey averages as a benchmark, single coverage averaged $9,325 a year and family coverage $26,993, which at 102 percent works out to roughly $793 and $2,294 a month. Your own number is on the election notice and it is the real figure, not an estimate."),
 ("Can COBRA cost more than 102 percent?",
  "Yes, in one situation. If you qualified for the 11-month disability extension, the plan may charge up to 150 percent of the full cost for months 19 through 29. Federal COBRA also only applies to employers with 20 or more employees; below that, state continuation rules apply and the pricing rules differ by state."),
 ("Is COBRA ever cheaper than a marketplace plan?",
  "It can be, and it is worth checking rather than assuming. Premium tax credits now phase out completely above 400 percent of the federal poverty level, because the enhanced subsidies expired at the end of 2025. A household above that line pays full price on the marketplace too, and if you have already met your deductible for the year, staying put can come out ahead. Below that line, a subsidised marketplace plan usually wins by a wide margin."),
 ("Can I pay COBRA premiums with an HSA?",
  "Yes. Insurance premiums are normally not a qualified HSA expense, but the tax code carves out continuation coverage specifically, and also coverage during a period when you are receiving unemployment compensation. If you have a funded HSA from your old plan, that balance is available tax-free against COBRA."),
]

TOC = [("split", "The Split You Never Saw"), ("numbers", "What It Works Out To"),
       ("two-percent", "The 2 Percent"), ("higher", "When It Is Even Higher"),
       ("cheaper", "What Costs Less"), ("hsa", "Paying With an HSA"), ("faq", "FAQ")]

BODY = '''<h2 id="split">Your payroll deduction was never the price</h2>
      <p>Almost everyone opens a COBRA election notice and assumes there has been a mistake, or that they are being punished for leaving. Neither is true, and the real explanation is more annoying than either.</p>
      <p>Employer health insurance is a split bill. Your employer paid most of it, you paid the rest through payroll, and the only number you ever saw was your part. COBRA does not raise the price of your coverage. It moves the whole bill to you.</p>
      <div class="highlight-box">
        <h4>What federal law actually allows</h4>
        <p>A plan may charge a COBRA enrollee up to <strong>102 percent of the applicable premium</strong> — the full cost of the coverage for similarly situated people, plus a 2 percent administrative charge. That is the cap, written into ERISA. There is no markup beyond it and no negotiating it down.</p>
      </div>

      <h2 id="numbers">What that works out to</h2>
      <p>The KFF Employer Health Benefits Survey is the standard benchmark for what employer coverage costs. Its 2025 figures, and what 102 percent of them looks like:</p>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th></th><th>Total annual premium</th><th>Average worker share</th><th>COBRA at 102%</th></tr></thead>
        <tbody>
          <tr><td><strong>Single</strong></td><td>$9,325</td><td>$1,440 — about $120/month</td><td><strong>about $793/month</strong></td></tr>
          <tr><td><strong>Family</strong></td><td>$26,993</td><td>$6,850 — about $571/month</td><td><strong>about $2,294/month</strong></td></tr>
        </tbody>
      </table>
      </div>
      <p class="vs-src">Premium and worker-contribution figures: <a href="https://www.kff.org/health-costs/2025-employer-health-benefits-survey/" rel="nofollow noopener" target="_blank">KFF 2025 Employer Health Benefits Survey</a>. The COBRA column is 102% of the total, computed here for illustration — it is not a KFF figure, and your own plan will differ.</p>
      <p>So the single person goes from about $120 to about $793, and the family from about $571 to about $2,294. Roughly six times and four times. Those multiples are why COBRA feels punitive when it is really just arithmetic.</p>
      <p>Your own number is on the notice, and unlike almost every other health insurance figure you will be quoted, it is exact. It is what your specific plan costs.</p>

      <h2 id="two-percent">What the 2 percent is for</h2>
      <p>Administration — billing you, tracking your eligibility, sending notices, remitting to the carrier. Plans are not obliged to charge it, but nearly all do, and on a family premium it is roughly $45 a month.</p>
      <p>It is worth knowing about mainly because it explains the odd number. People see "102 percent" and assume it is a typo for 100, or suspect a hidden fee. It is neither.</p>

      <h2 id="higher">Three situations where it is higher still</h2>
      <ul>
        <li><strong>The disability extension.</strong> If the Social Security Administration determined you disabled during the first 60 days of COBRA, you can extend from 18 months to 29 — but the plan may charge up to <strong>150 percent</strong> of the full cost for months 19 through 29. The extension is usually worth having anyway; just do not be surprised by the invoice.</li>
        <li><strong>Your employer was subsidising more than you realised.</strong> Generous employers pay 85 or 90 percent of family premiums rather than the 74 percent average. The more generous the benefit was, the harder COBRA lands.</li>
        <li><strong>A mid-year rate increase.</strong> COBRA premiums track the plan's actual cost, so when the group renews at a higher rate, yours goes up with it.</li>
      </ul>
      <p>One thing that will not raise it: your health. COBRA is a continuation of the same group coverage at the group's cost. Nobody is rating you individually.</p>
      <p>And a limit worth knowing — <strong>federal COBRA only applies to employers with 20 or more employees.</strong> If your employer was smaller, what you have been offered is state continuation coverage, which most states require and which runs on different rules. Kentucky, for instance, gives 18 months to employees of employers under 20. <a href="/kentucky-small-business-health-insurance">More on that here &rarr;</a></p>

      <h2 id="cheaper">What costs less</h2>
      <p>The short version, in the order worth checking:</p>
      <ol>
        <li><strong>A spouse's or partner's employer plan.</strong> Your loss of coverage opens a special enrollment period on their plan, and their employer is subsidising it. Frequently the cheapest thing available and frequently forgotten.</li>
        <li><strong>A marketplace plan with a premium tax credit.</strong> Subsidies key off your <em>projected</em> income for the year, not last year's W-2, so a mid-year layoff often qualifies you for far more than your old salary suggests.</li>
        <li><strong>Medicaid</strong>, if your income has dropped far enough. No enrollment window — you can apply any day.</li>
        <li><strong>A parent's plan</strong>, if you are under 26.</li>
      </ol>
      <p>The one caveat on the marketplace route, and it is new: the enhanced premium tax credits expired at the end of 2025, so credits now phase out entirely above 400 percent of the federal poverty level. Above that line you pay full price on the marketplace too, and the comparison gets much closer — particularly if you have already met your deductible this year. Below it, a subsidised plan usually wins by a lot.</p>
      <div class="highlight-box">
        <h4>Do not cancel first and shop second</h4>
        <p>Voluntarily dropping COBRA mid-year does not open a special enrollment period. If you cancel in April without a replacement lined up, you are uninsured until January. Get the new policy's effective date confirmed in writing, then stop the old coverage. <a href="/blog/can-i-drop-cobra-for-marketplace">The full rule, and the three windows where switching does work &rarr;</a></p>
      </div>
      <p>Full comparison of the options: <a href="/cobra-alternatives">COBRA alternatives &rarr;</a></p>

      <h2 id="hsa">One thing nobody tells you: your HSA can pay for it</h2>
      <p>Health insurance premiums are normally <em>not</em> a qualified HSA expense. Continuation coverage is one of a very short list of exceptions written into the tax code, alongside long-term care insurance and coverage while you are receiving unemployment compensation.</p>
      <p>So if you have a funded HSA sitting from your old high-deductible plan, that balance can go against your COBRA premiums tax-free. For a lot of recently laid-off people that is several months of coverage they did not know they had already paid for. It applies to premiums while you are collecting unemployment too, which covers most of the same people twice over.</p>

      <div class="cta-block">
        <h3>Send us your COBRA number</h3>
        <p>Your monthly quote, ZIP code, ages and roughly what you expect to earn this year. We come back with what the same household pays on the marketplace after any subsidy, and whether your doctors are in it. Free — carriers pay our commission either way.</p>
        <a class="btn btn-teal" href="/quote?type=individual" style="background:#fff;color:var(--blue-700)">Compare against my COBRA quote &rarr;</a>
      </div>

      <h2 id="faq">Frequently asked</h2>
      <h3>Can I negotiate my COBRA premium?</h3>
      <p>No. It is set by the plan's actual cost and capped by statute. There is no discretion at the administrator's end, so there is nobody to ask.</p>
      <h3>Does COBRA get cheaper over time?</h3>
      <p>No — it tracks the group's premium, so if anything it rises at the group's renewal. The one exception runs the other way: the disability extension makes months 19 to 29 more expensive, not less.</p>
      <h3>Is COBRA tax deductible?</h3>
      <p>Premiums may count toward the medical expense itemised deduction, which only helps above a threshold of adjusted gross income and only if you itemise. If you are self-employed, the self-employed health insurance deduction is usually the better route. Worth a conversation with your accountant rather than an assumption.</p>
      <p class="vs-src">Sources: <a href="https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/an-employees-guide-health-benefits-under-cobra-2022.pdf" rel="nofollow noopener" target="_blank">DOL, An Employee&rsquo;s Guide to Health Benefits Under COBRA</a> &middot; <a href="https://www.law.cornell.edu/uscode/text/29/1162" rel="nofollow noopener" target="_blank">29 U.S.C. 1162</a> &middot; <a href="https://www.kff.org/health-costs/2025-employer-health-benefits-survey/" rel="nofollow noopener" target="_blank">KFF 2025 Employer Health Benefits Survey</a> &middot; <a href="https://www.irs.gov/publications/p969" rel="nofollow noopener" target="_blank">IRS Publication 969</a></p>'''

build(slug='why-is-cobra-so-expensive',
      title='Why Is COBRA So Expensive? The Real Reason',
      h1='Why Is COBRA So Expensive? Because You Were Only Ever Seeing Half the Bill',
      desc='COBRA is capped at 102% of your plan&rsquo;s full cost. Here is where the number comes from, what the 2% is, and what costs less.',
      lede='Nothing has been marked up and you are not being penalised. Your employer was paying most of the premium, and COBRA simply moves the whole bill to you. Here is the arithmetic, and what to do about it.',
      published='2026-08-27', read_min=7, eyebrow='COBRA',
      img='/compressed/health-insurance-cost-2026-woman.jpg',
      alt='Person reviewing a COBRA election notice and comparing the premium against marketplace options',
      toc=TOC, body=BODY, faq=FAQ,
      cta_head='Beat your COBRA quote',
      cta_copy='Send the number. We will tell you what else you can get.',
      cta_href='/quote?type=individual')

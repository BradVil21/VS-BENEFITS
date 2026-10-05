# -*- coding: utf-8 -*-
"""Open Enrollment 2027 savings cluster, 4 October 2026.

Five posts aimed at the people searching right now because their renewal
letter just arrived, their premium went up, or their coverage is ending:

  /blog/how-to-lower-health-insurance-premiums-2027     "how to lower health insurance premium", "cheaper health insurance"
  /blog/health-insurance-renewal-notice-2027             "health insurance renewal letter", "marketplace auto renewal 2027"
  /blog/losing-health-insurance-2027                     "cigna leaving marketplace 2027", "losing health insurance 2027"
  /blog/cheapest-health-insurance-2027                   "cheapest health insurance 2027", "catastrophic plan 2027", "bronze hsa"
  /blog/owner-operator-health-insurance-increase-2027    trucking: "owner operator health insurance cost 2027"

House rules kept: no carrier benefit claims, no invented premium tables, every
regulatory figure matches the rest of the site or was verified 4 Oct 2026:
  KFF 2027 rate filings: median proposed +15% (276 insurers, -1% to +54%), Aug 3 2026
  Florida 2027 requests: 12 insurers, +3.87% to +39.14%, OIR not final (WLRN, Sep 11 2026)
  2026 benchmark premium +26% (KFF)
  Enhanced credits expired 12/31/2025; House passed extension 1/8/2026, Senate has not acted
  OE Nov 1 2026 - Jan 15 2027, Dec 15 for Jan 1 (City of Columbus v. Kennedy, June 12 2026)
  2027 HSA $4,500 / $9,000, +$1,000 at 55; HDHP min deductible $1,750 / $3,500 (Rev. Proc. 2026-24)
  Bronze + catastrophic plans HSA-compatible from 2026 (OBBBA, IRS Notice 2026-5)
  Catastrophic hardship exemption: ineligible for APTC or CSR due to income (<100% / >250% FPL),
    permanent and nationwide in the 2027 NBPP; multi-year catastrophic plans allowed from 2027
  2027 ACA out-of-pocket max $12,000 / $24,000
  Cigna exits all 11 marketplace states for 2027 incl. Florida (KFF tracker, Sep 15 2026)
  Medicaid work requirements from Jan 1 2027 (expansion adults 19-64, 80 hrs/month); 6-month renewals
  Immigrant PTC eligibility narrows Jan 1 2027; 150% FPL monthly SEP ends after plan year 2026
  Full repayment of excess APTC from tax year 2026
  Pre-enrollment verification for auto re-enrollment: 2028, not 2027
  2026 Solo 401(k) deferral $24,500 (+$8,000 at 50, +$11,250 at 60-63); SEP/DC max $72,000
  FPL (2026 guidelines, used for 2027 coverage): $15,960 + $5,680/person
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

TODAY = "2026-10-04"


def faq_html(pairs):
    out = ['<h2 id="faq">Frequently asked</h2>']
    for q, a in pairs:
        out.append('<h3>%s</h3>\n      <p>%s</p>' % (q, a))
    return '\n      '.join(out)


def cta(head, copy, href="/quote?type=individual", btn="Get my free 2027 quote &rarr;"):
    return ('<div class="cta-block">\n        <h3>%s</h3>\n        <p>%s</p>\n'
            '        <a class="btn btn-teal" href="%s">%s</a>\n      </div>' % (head, copy, href, btn))


SOURCES_COMMON = ('<p class="vs-src">Sources: KFF analysis of 2027 ACA rate filings (Aug 2026); Florida Office of Insurance '
                  'Regulation filings as reported by WLRN (Sep 2026); KFF insurer participation tracker for 2027 (Sep 2026); '
                  'CMS 2027 Notice of Benefit and Payment Parameters; IRS Rev. Proc. 2026-24 and Notice 2026-5; 2026 HHS poverty '
                  'guidelines. Figures checked 4 October 2026. Rates are proposals until each state finalizes them.</p>')

# =========================================================================== #
# 1. How to lower your premium
# =========================================================================== #
TOC_LOWER = [("why", "Why 2027 Costs More"), ("moves", "11 Moves That Lower It"),
             ("table", "Which Moves Fit You"), ("deadline", "The Deadline"), ("faq", "FAQ")]

FAQ_LOWER = [
 ("Why is my health insurance going up so much in 2027?",
  "Two things are stacking. Insurers asked for a median 15% rate increase for 2027 nationally, on top of a 26% average "
  "benchmark increase in 2026. And the enhanced premium tax credits that capped what most people paid expired at the end of "
  "2025, so the subsidy that used to absorb those increases is smaller, and above 400% of the poverty level it is gone."),
 ("What is the fastest way to lower my health insurance premium?",
  "Shop instead of letting your plan auto-renew, and update your income estimate before you do. Your subsidy is tied to "
  "the second-lowest-cost silver plan in your area, and that benchmark changes every year. A plan that was a good deal "
  "in 2026 can be one of the more expensive options in 2027 even if its sticker price barely moved."),
 ("Can I lower my income to get a bigger ACA subsidy?",
  "You can lower your modified adjusted gross income legally. Pre-tax contributions to a traditional 401(k), a deductible "
  "IRA, a SEP or Solo 401(k) if you are self-employed, and an HSA all reduce it, and so does the self-employed health "
  "insurance deduction. Near the 400% line, a few thousand dollars of contributions can be worth more in subsidy than "
  "they cost. You cannot simply under-report income: since tax year 2026 any excess credit is repaid in full."),
 ("Is a bronze plan a good way to save money?",
  "It lowers the premium, and since 2026 every bronze plan is HSA-compatible, which adds a tax break. It is a good fit if "
  "you rarely use care and could cover a high deductible in a bad year. If your income is under 250% of the poverty level, "
  "compare it against silver first: cost-sharing reductions only apply to silver plans and can make silver the cheaper "
  "plan over a full year."),
 ("When is the deadline to change plans for 2027?",
  "Open Enrollment runs November 1, 2026 to January 15, 2027 on HealthCare.gov. Pick a plan by December 15 for coverage "
  "that starts January 1. Plans picked from December 16 to January 15 start February 1. Some state-run exchanges have "
  "different end dates."),
 ("Does using a broker cost more?",
  "No. Plan prices are set by the insurer and filed with the state, so the premium is the same whether you enroll on your "
  "own, on HealthCare.gov or through a licensed broker. The carrier pays the broker's commission."),
]

BODY_LOWER = '''<h2 id="why">Why your 2027 premium is going up</h2>
      <p>If your renewal letter made you wince, you are not imagining it. Insurers asked for a <strong>median 15% rate increase</strong> for 2027 across 276 insurers nationwide, with individual requests running from a small decrease to more than 50%. That lands on top of a 26% average benchmark increase in 2026. In Florida, the 12 insurers that filed asked for increases from about 4% to about 39%, and the state has not finalized them yet.</p>
      <p>The bigger change is the subsidy. The enhanced premium tax credits expired on December 31, 2025. The House passed a three-year extension in January 2026, but the Senate has not acted, so for 2027 the original rules apply: the share of income you are expected to pay is higher, and above <strong>400% of the federal poverty level</strong> (about $63,840 for a single person or $132,000 for a family of four) there is no credit at all.</p>
      <div class="highlight-box">
        <h4>The one thing to remember</h4>
        <p>Your premium is not a fixed price you either accept or cancel. It moves with your income estimate, the plan you choose and how your local benchmark plan moved this year. Most of the savings below come from those three levers, and none of them requires giving up real coverage.</p>
      </div>
      <p>Want to see how big your increase actually is? Our <a href="/health-insurance-premium-increase-calculator">2027 premium increase calculator</a> compares your renewal number to what a benchmark plan should cost at your income.</p>

      <h2 id="moves">11 moves that lower a 2027 premium</h2>

      <h3>1. Do not let your plan auto-renew</h3>
      <p>If you do nothing, the Marketplace re-enrolls you in the same plan, or the closest match if yours is discontinued. That is convenient and often expensive. Your subsidy is pegged to the second-lowest-cost silver plan in your area, and the benchmark resets every year. When the benchmark gets cheaper relative to your plan, your net premium rises even if your plan's sticker price barely moved. <a href="/blog/health-insurance-renewal-notice-2027">Here is how to read your renewal notice</a>.</p>

      <h3>2. Update your income estimate before you shop</h3>
      <p>Your subsidy is calculated on the income you expect for 2027, not what you made last year. If your hours dropped, you changed jobs or your business had a slow year, a lower estimate can mean a much larger credit. Be accurate rather than hopeful: starting with tax year 2026, any excess credit has to be paid back in full at tax time. <a href="/blog/what-income-counts-for-aca-subsidies">What counts as income for the subsidy</a>.</p>

      <h3>3. Lower your MAGI on purpose if you are near the 400% line</h3>
      <p>The subsidy uses modified adjusted gross income, and you can reduce it legally. Pre-tax contributions to a traditional 401(k) or 403(b), a deductible IRA, a SEP or Solo 401(k) if you are self-employed, and an HSA all count. So does the self-employed health insurance deduction. At $1,000 over the cliff, a $1,500 retirement contribution can restore a credit worth thousands. <a href="/blog/aca-income-limits-2027">See the 2027 income limits by household size</a>.</p>

      <h3>4. Pick the metal tier by total cost, not premium</h3>
      <p>Compare premium plus what you are likely to spend on care. If your income is under 250% of the poverty level (about $39,900 for one person), silver plans come with cost-sharing reductions that lower the deductible and copays. Those discounts only exist on silver, which is why a silver plan can cost less over the year than a bronze plan with a lower premium. <a href="/bronze-vs-silver-vs-gold-vs-platinum">Bronze vs silver vs gold vs platinum</a>.</p>

      <h3>5. Pair a bronze plan with an HSA</h3>
      <p>Since 2026, every bronze and catastrophic plan counts as HSA-compatible. For 2027 you can put in up to <strong>$4,500</strong> for yourself or <strong>$9,000</strong> for a family, plus $1,000 if you are 55 or older. Contributions lower your taxable income and your MAGI, the money rolls over every year, and it pays for qualified care tax-free. For healthy people who can handle a high deductible, this is the cleanest way to cut the total bill.</p>

      <h3>6. Check whether you qualify for a catastrophic plan</h3>
      <p>Catastrophic plans have the lowest premiums on the Marketplace. They used to be limited to people under 30. Now anyone whose income makes them ineligible for premium tax credits or cost-sharing reductions, generally income below 100% or above 250% of the poverty level, can request a hardship exemption to buy one. The 2027 rules made that permanent and nationwide. Credits cannot be applied to catastrophic plans, so they make most sense for people who do not get a credit anyway. <a href="/blog/cheapest-health-insurance-2027">How catastrophic, bronze and HSA plans compare</a>.</p>

      <h3>7. Match the network to how you actually use care</h3>
      <p>PPOs cost more because they cover out-of-network care. If your doctors are local and you rarely travel, an HMO or EPO with your doctors in network is often the same care for less. If you travel for work or split time between states, the PPO premium may be worth it. <a href="/hmo-vs-ppo">HMO vs PPO, explained</a>.</p>

      <h3>8. Price the household together and split</h3>
      <p>Nobody in a household has to be on the same policy. If one person needs a broad network and the rest need local care, two plans can cost less than one plan that tries to do both. Your subsidy is still based on total household income, so splitting does not hide anything; it just lets each person buy the right plan.</p>

      <h3>9. Re-check the job-based options in your household</h3>
      <p>If a spouse's employer offers coverage, compare it again for 2027. Since the family glitch fix, family members are judged against the cost of <em>family</em> coverage, so if the family premium is unaffordable they may qualify for Marketplace credits while the employee stays on the work plan. Small business owners can look at <a href="/ichra-vs-group-health-calculator">ICHRA or a group plan</a>, which can cover the owner's family for less than individual coverage.</p>

      <h3>10. Buy dental and vision only if the math works</h3>
      <p>Adult dental and vision are not part of a medical plan. A standalone plan is worth it if you will actually use it; otherwise it is premium you do not need. <a href="/blog/is-dental-and-vision-insurance-worth-it">Here is the break-even math</a>.</p>

      <h3>11. Be careful with plans that only look cheaper</h3>
      <p>Short-term plans, fixed indemnity plans and health care sharing ministries are cheaper because they cover less. Most can turn down pre-existing conditions, cap what they pay, or are not insurance at all, and none of them qualifies for a premium tax credit. They have a place as a bridge, but they are not a cheaper version of the same thing. <a href="/blog/how-to-shop-for-health-insurance">How the four ways to buy compare</a>.</p>

      ''' + cta("See your real 2027 number", "We compare every plan in your ZIP at your real income and show what a bad year would cost on each. Same prices as HealthCare.gov, free to you.") + '''

      <h2 id="table">Which moves fit your situation</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>If this is you</th><th>Start with</th><th>Why</th></tr></thead>
        <tbody>
          <tr><td>Income under 250% of the poverty level</td><td>Moves 1, 2, 4</td><td>Silver with cost-sharing reductions often beats bronze over a full year</td></tr>
          <tr><td>Income just over 400% of the poverty level</td><td>Moves 3, 5</td><td>A retirement or HSA contribution can bring the credit back</td></tr>
          <tr><td>Well above 400%, healthy</td><td>Moves 5, 6, 7</td><td>No credit to protect, so the lowest premium with a tax break wins</td></tr>
          <tr><td>Self-employed or 1099</td><td>Moves 2, 3</td><td>Net profit, not gross, sets the subsidy</td></tr>
          <tr><td>Family with mixed needs</td><td>Moves 8, 9</td><td>Splitting plans or using a spouse's employer can cut the total</td></tr>
          <tr><td>Insurer leaving your state</td><td>Move 1</td><td>You will be moved to another plan unless you choose one yourself</td></tr>
        </tbody>
      </table>
      </div>

      <h2 id="deadline">The deadline that matters</h2>
      <p>Open Enrollment for 2027 coverage runs <strong>November 1, 2026 to January 15, 2027</strong>. Choose a plan by <strong>December 15</strong> for coverage that starts January 1. Choose after that and your new plan starts February 1. The full calendar, including state exchanges, is in our <a href="/blog/aca-open-enrollment-2027-guide">Open Enrollment 2027 guide</a>.</p>
      <p>If your coverage is ending because your insurer is leaving or you lost Medicaid or job coverage, you may not have to wait for Open Enrollment. <a href="/blog/losing-health-insurance-2027">Here is what to do if you are losing coverage in 2027</a>.</p>
      ''' + SOURCES_COMMON

# =========================================================================== #
# 2. Renewal notice
# =========================================================================== #
TOC_RENEW = [("notice", "What the Notice Tells You"), ("wrong", "Why the Number Can Be Wrong"),
             ("auto", "What Happens If You Do Nothing"), ("checks", "6 Things to Check"),
             ("business", "Employer Plan Renewals"), ("faq", "FAQ")]

FAQ_RENEW = [
 ("What happens if I ignore my health insurance renewal notice?",
  "If you are on a Marketplace plan and do nothing, you are usually re-enrolled automatically for January 1 in the same "
  "plan, or in a similar plan if yours is discontinued, with your subsidy recalculated from the information the "
  "Marketplace already has. You stay covered, but you may pay more than you need to."),
 ("Why did my premium go up when my plan did not change?",
  "Your net premium is the plan's price minus your premium tax credit, and the credit is based on the second-lowest-cost "
  "silver plan in your area. If that benchmark plan got cheaper or a cheaper insurer entered, your credit shrinks and "
  "your net premium rises, even if your own plan's price barely changed. That is why the cheapest plan last year is not "
  "always the cheapest plan this year."),
 ("Is my insurer leaving the Marketplace in 2027?",
  "Nine insurers are leaving at least one state for 2027. The largest is Cigna, which is exiting the Marketplace in all "
  "11 of its states, including Florida. Others include CareSource in Indiana, Ohio and West Virginia, Baylor Scott & White "
  "in Texas, PacificSource in Idaho, Montana and Oregon, and ConnectiCare in Connecticut. If your insurer is leaving you "
  "should get a discontinuance notice; you can pick a new plan yourself instead of being moved into one."),
 ("Can I change plans after I am auto-renewed?",
  "Yes, as long as Open Enrollment is still open. On HealthCare.gov you can change plans through January 15, 2027. The "
  "last plan you choose is the one that takes effect, with a January 1 start if you choose by December 15."),
 ("Does the Marketplace check my income when it renews me?",
  "It uses the most recent data it has, which may be your 2025 tax return. If your 2027 income will be different, update "
  "your application. Starting in 2028, new verification rules will make passive re-enrollment with a subsidy harder, so "
  "building the habit of updating every fall pays off."),
]

BODY_RENEW = '''<h2 id="notice">What your renewal notice is telling you</h2>
      <p>Between October and early November, everyone on a Marketplace plan gets a notice from their insurer and usually one from the Marketplace. It shows your plan for next year, its new monthly price, any changes to the deductible or copays, and an estimate of your premium after the tax credit.</p>
      <p>That last number is the one most people look at, and it is the one most likely to be off.</p>

      <h2 id="wrong">Why the number on the notice can be wrong</h2>
      <p>The estimate is built from information that is a year old and a benchmark that just changed.</p>
      <ul>
        <li><strong>Your income is last year's.</strong> The Marketplace uses whatever it has on file, often your previous tax return. If your 2027 income will be lower, your real credit is likely bigger. If it will be higher, the notice is understating what you will owe, and since tax year 2026 any excess credit is repaid in full.</li>
        <li><strong>The benchmark moved.</strong> Your credit equals the price of the second-lowest-cost silver plan in your area minus the amount you are expected to pay. With insurers asking for a median 15% increase for 2027, and some insurers leaving, the benchmark plan in many areas is now a different plan at a different price.</li>
        <li><strong>The cliff is back.</strong> Above 400% of the poverty level there is no credit in 2027. If a raise pushed you just over the line, your notice may show the full price.</li>
      </ul>
      <div class="highlight-box">
        <h4>Check your number in a minute</h4>
        <p>Enter your current premium, your renewal premium and your expected income in the <a href="/health-insurance-premium-increase-calculator">premium increase calculator</a>. It shows your increase and roughly what a benchmark silver plan should cost at your income.</p>
      </div>

      <h2 id="auto">What happens if you do nothing</h2>
      <p>If you stay silent, you are usually re-enrolled for January 1 automatically:</p>
      <ul>
        <li><strong>Your plan is still offered:</strong> you are renewed in the same plan, at the new price.</li>
        <li><strong>Your plan is discontinued:</strong> you are moved into a similar plan, often from the same insurer. If the insurer is leaving entirely, you may be placed with a different insurer, and your doctors may not be in that network.</li>
        <li><strong>Your subsidy:</strong> recalculated using the data on file, not your 2027 income.</li>
      </ul>
      <p>For 2027, the biggest exit is <strong>Cigna, which is leaving the Marketplace in all 11 of its states, including Florida</strong>. If you are on a Cigna Marketplace plan, choose your next plan yourself rather than accepting whatever you are moved into. <a href="/blog/losing-health-insurance-2027">More on insurers leaving in 2027</a>.</p>

      <h2 id="checks">Six things to check before you renew</h2>
      <ol>
        <li><strong>Your premium after the credit</strong>, compared with at least two other plans at the same metal level. If your plan is no longer near the benchmark, there is usually a cheaper plan with a similar network.</li>
        <li><strong>The deductible and out-of-pocket maximum.</strong> The legal cap on out-of-pocket costs rises to $12,000 for one person and $24,000 for a family in 2027, and many plans are moving their limits up with it.</li>
        <li><strong>Your doctors, by name</strong>, in next year's directory. Networks change every January.</li>
        <li><strong>Your prescriptions</strong> in next year's drug list, including the tier. A drug moving from tier 2 to tier 3 can cost more than the premium change.</li>
        <li><strong>Your 2027 income estimate</strong>, updated before you compare plans. <a href="/blog/what-income-counts-for-aca-subsidies">What counts as income</a>.</li>
        <li><strong>Whether your insurer is staying</strong> in your state for 2027.</li>
      </ol>
      ''' + cta("Send us your renewal letter", "We will check it against every plan in your ZIP and tell you whether to keep it or switch. Free, and the premium is the same as buying direct.") + '''

      <h3>The dates</h3>
      <div class="vs-tw">
      <table class="vs-t" style="min-width:0">
        <thead><tr><th>Date</th><th>What happens</th></tr></thead>
        <tbody>
          <tr><td>October to early November</td><td>Renewal and discontinuance notices arrive</td></tr>
          <tr><td>November 1, 2026</td><td>Open Enrollment opens; window-shop and change plans</td></tr>
          <tr><td>December 15, 2026</td><td>Last day to choose a plan for a January 1 start</td></tr>
          <tr><td>January 1, 2027</td><td>Auto-renewed and new plans begin</td></tr>
          <tr><td>January 15, 2027</td><td>Open Enrollment ends on HealthCare.gov; plans chosen after Dec 15 start February 1</td></tr>
        </tbody>
      </table>
      </div>

      <h2 id="business">If the renewal is for your company's group plan</h2>
      <p>Small group plans renew on the anniversary of the plan, not on January 1, and the renewal usually arrives 60 to 90 days ahead. The same rule applies: never accept the first renewal without a market check. Options include a different carrier, a different plan mix, a level-funded plan, or an ICHRA. <a href="/business-open-enrollment-faq">Our employer open enrollment FAQ</a> walks through it, and we can re-market a group at no cost.</p>
      ''' + SOURCES_COMMON

# =========================================================================== #
# 3. Losing coverage in 2027
# =========================================================================== #
TOC_LOSE = [("who", "Who Is Losing Coverage"), ("insurer", "Your Insurer Is Leaving"),
            ("cliff", "Priced Out by the Cliff"), ("medicaid", "Medicaid Changes"),
            ("immigrant", "Immigrant Eligibility"), ("sep", "Low-Income Enrollment Window"),
            ("plan", "What to Do Next"), ("faq", "FAQ")]

FAQ_LOSE = [
 ("Is Cigna leaving the ACA Marketplace in 2027?",
  "Yes. Cigna is exiting the ACA Marketplace in all 11 states where it sold individual plans, including Florida, for "
  "2027. Members should receive a discontinuance notice. You can choose a new plan from another insurer during Open "
  "Enrollment, November 1, 2026 to January 15, 2027; choose by December 15 to have coverage start January 1."),
 ("What do I do if my health insurance company leaves the Marketplace?",
  "Pick a new plan yourself during Open Enrollment rather than waiting to be reassigned, and check that your doctors and "
  "prescriptions are covered on the new plan. Losing a plan because it was discontinued also counts as a loss of "
  "coverage for a Special Enrollment Period, so if you miss Open Enrollment you generally have 60 days from the date the "
  "coverage ends to enroll."),
 ("When do Medicaid work requirements start?",
  "Federal law requires them starting January 1, 2027, although states can start sooner and some can get extensions. "
  "They apply to adults aged 19 to 64 covered through Medicaid expansion, who need 80 hours a month of work, job "
  "training, school or community service unless they qualify for an exemption. Florida did not expand Medicaid, so most "
  "Floridians on Medicaid are not in the group these rules target."),
 ("I lost Medicaid. Can I get a Marketplace plan?",
  "Yes. Losing Medicaid is a qualifying event, and you generally have 60 days to enroll in a Marketplace plan, with a "
  "premium tax credit if your income is in range. In states that did not expand Medicaid, including Florida, adults "
  "below 100% of the poverty level usually do not qualify for a credit, but may qualify for a low-cost catastrophic plan "
  "through a hardship exemption."),
 ("Can I still enroll any month if my income is low?",
  "Not after 2026. The monthly Special Enrollment Period for people at or below 150% of the poverty level ends after plan "
  "year 2026, and people who enroll through an income-based Special Enrollment Period no longer receive a premium tax "
  "credit. For 2027, Open Enrollment is the window to use."),
 ("Which immigrants can still get ACA subsidies in 2027?",
  "From January 1, 2027, premium tax credits are limited to lawful permanent residents, Cuban and Haitian entrants, and "
  "people living in the U.S. under a Compact of Free Association. Other lawfully present immigrants can still buy a "
  "Marketplace plan, but at full price."),
]

BODY_LOSE = '''<h2 id="who">Who is losing coverage going into 2027</h2>
      <p>Most people losing coverage this fall fit one of five situations. Each has a different deadline and a different fix, so find yours first.</p>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>What happened</th><th>When</th><th>Your window</th></tr></thead>
        <tbody>
          <tr><td>Your insurer is leaving your state's Marketplace</td><td>Plan ends Dec 31, 2026</td><td>Open Enrollment, or 60 days after coverage ends</td></tr>
          <tr><td>Your income is over 400% of the poverty level, so no credit</td><td>Since Jan 1, 2026</td><td>Open Enrollment</td></tr>
          <tr><td>You are a Medicaid expansion adult facing work requirements or 6-month checks</td><td>From Jan 1, 2027 (some states earlier)</td><td>60 days after Medicaid ends</td></tr>
          <tr><td>You are lawfully present but not in an eligible immigration category</td><td>From Jan 1, 2027</td><td>Open Enrollment (at full price)</td></tr>
          <tr><td>You relied on the year-round low-income enrollment window</td><td>Ends after 2026</td><td>Open Enrollment only</td></tr>
        </tbody>
      </table>
      </div>

      <h2 id="insurer">Your insurer is leaving the Marketplace</h2>
      <p>Nine insurers are pulling out of at least one state for 2027. The largest is <strong>Cigna, which is exiting the Marketplace in all 11 of its states, including Florida</strong>, where it covered about 97,000 people. Others include CareSource (Indiana, Ohio, West Virginia), Baylor Scott &amp; White (Texas), PacificSource (Idaho, Montana, Oregon) and ConnectiCare (Connecticut).</p>
      <p>If your insurer is leaving, you will get a discontinuance notice. If you do nothing, the Marketplace may place you in a plan from another insurer, chosen on price and plan type, not on your doctors. Choose your own plan during Open Enrollment instead, and check your doctors and prescriptions on it before you enroll.</p>
      <div class="highlight-box">
        <h4>Missed the deadline?</h4>
        <p>A plan ending because it was discontinued counts as a loss of coverage, which opens a 60-day Special Enrollment Period. Do not count on it, though: enrolling by December 15 is the only way to guarantee no gap on January 1.</p>
      </div>

      <h2 id="cliff">Priced out by the subsidy cliff</h2>
      <p>With the enhanced credits gone, a single person earning more than about <strong>$63,840</strong>, a couple above about $86,560 or a family of four above about <strong>$132,000</strong> gets no credit in 2027. Florida saw roughly 443,000 people leave the Marketplace between 2025 and 2026, much of it from that change.</p>
      <p>Dropping coverage is the expensive way out. A single hospital stay can cost more than several years of premiums. Before you let a plan lapse:</p>
      <ul>
        <li>Check whether pre-tax retirement or HSA contributions bring your income back under the line. <a href="/blog/aca-income-limits-2027">See the 2027 income limits</a>.</li>
        <li>Price a bronze plan with an HSA, or a catastrophic plan, which anyone above 250% of the poverty level can request through a hardship exemption.</li>
        <li>If you are self-employed, use your net profit, not gross revenue. <a href="/blog/owner-operator-health-insurance-no-subsidy">Over the cliff as a self-employed person</a>.</li>
      </ul>
      <p>Our <a href="/blog/how-to-lower-health-insurance-premiums-2027">guide to lowering a 2027 premium</a> has all eleven options.</p>

      <h2 id="medicaid">Medicaid work requirements and 6-month renewals</h2>
      <p>Under the 2025 budget law, states must start <strong>work and community engagement requirements on January 1, 2027</strong> (some can start sooner or get an extension). They apply to adults aged 19 to 64 covered through Medicaid expansion, who must show 80 hours a month of work, job training, school or community service unless exempt. Expansion adults also move to eligibility checks every six months, starting with renewals due on or after December 31, 2026.</p>
      <p>Florida did not expand Medicaid, so most Floridians on Medicaid are not in the expansion group. If you live in an expansion state and lose Medicaid, you generally have 60 days to enroll in a Marketplace plan, often with a sizable credit.</p>

      <h2 id="immigrant">Immigrant eligibility changes on January 1, 2027</h2>
      <p>From January 1, 2027, premium tax credits are limited to lawful permanent residents (green card holders), Cuban and Haitian entrants, and people here under a Compact of Free Association. Other lawfully present immigrants, such as many people with work visas, TPS or pending asylum cases, can still buy a Marketplace plan but without a credit. If that is you, compare Marketplace plans at full price with job-based coverage and catastrophic options. <a href="/blog/inscripcion-abierta-2027">Gu&iacute;a en espa&ntilde;ol</a>.</p>

      <h2 id="sep">The year-round low-income window is closing</h2>
      <p>Since 2022, people at or below 150% of the poverty level could enroll any month. That window ends after plan year 2026, and people who enroll through an income-based special enrollment period no longer get a credit. For 2027, if your income is low, Open Enrollment is the time to enroll.</p>

      <h2 id="plan">What to do next, in order</h2>
      <ol>
        <li><strong>Read every letter from your insurer, the Marketplace or Medicaid.</strong> Note the date your coverage ends.</li>
        <li><strong>Estimate your 2027 income honestly.</strong> Since tax year 2026, any excess credit is repaid in full.</li>
        <li><strong>Compare plans by your doctors and drugs</strong>, not just premium. <a href="/blog/health-insurance-renewal-notice-2027">Six things to check on any 2027 plan</a>.</li>
        <li><strong>Enroll by December 15</strong> for January 1 coverage. Open Enrollment closes January 15, 2027.</li>
        <li><strong>If you miss it, act within 60 days</strong> of losing coverage. <a href="/special-enrollment-period-checker">Check whether you qualify for a Special Enrollment Period</a>.</li>
      </ol>
      ''' + cta("Losing your plan? We will find the next one", "Tell us your ZIP, income and doctors. We line up the replacement before your coverage ends, at no cost to you.") + '''
      ''' + SOURCES_COMMON

# =========================================================================== #
# 4. Cheapest health insurance 2027
# =========================================================================== #
TOC_CHEAP = [("short", "The Short Answer"), ("subsidy", "If You Get a Credit"),
             ("bronze", "Bronze Plus an HSA"), ("catastrophic", "Catastrophic Plans"),
             ("network", "Narrow Networks"), ("nonaca", "Plans That Only Look Cheaper"),
             ("compare", "Side by Side"), ("faq", "FAQ")]

FAQ_CHEAP = [
 ("What is the cheapest health insurance in 2027?",
  "For most people it is a Marketplace plan with the premium tax credit applied, because the credit is money no other "
  "option can match. Many people under about 150% of the poverty level can still find a $0 or near-$0 bronze plan. If "
  "you do not qualify for a credit, the lowest premiums are usually catastrophic plans and HMO or EPO bronze plans."),
 ("Who can buy a catastrophic health plan in 2027?",
  "People under 30, and anyone who qualifies for a hardship exemption. Since 2026, that includes people whose income "
  "makes them ineligible for premium tax credits or cost-sharing reductions, generally income below 100% or above 250% "
  "of the poverty level. The 2027 rules made this permanent in every state."),
 ("Can I open an HSA with a bronze plan?",
  "Yes. Since January 1, 2026, all bronze and catastrophic plans are treated as HSA-compatible, whether bought on or off "
  "the Marketplace. For 2027 you can contribute up to $4,500 for self-only coverage or $9,000 for family coverage, plus "
  "$1,000 if you are 55 or older."),
 ("Is short-term health insurance cheaper?",
  "It usually has a lower premium because it covers less. Short-term plans can decline people with pre-existing "
  "conditions, exclude whole categories of care, cap what they pay and do not qualify for premium tax credits. They "
  "can work as a short bridge between plans, but they are not a lower-priced version of a Marketplace plan."),
 ("What is the most I can pay out of pocket in 2027?",
  "The 2027 legal limit for an ACA plan is $12,000 for one person and $24,000 for a family, not counting premiums. Some "
  "bronze plans may go above it as long as the insurer also offers a bronze plan within the limit. Check the "
  "out-of-pocket maximum on any low-premium plan, because that is what a bad year costs."),
 ("Are health care sharing ministries insurance?",
  "No. Sharing ministries are not insurance, are not regulated as insurance and do not guarantee payment of claims. "
  "Members share costs under the ministry's own rules, which often exclude pre-existing conditions. They do not qualify "
  "for premium tax credits."),
]

BODY_CHEAP = '''<h2 id="short">The short answer</h2>
      <p>The cheapest real health insurance in 2027 depends on one number: your household income compared with the federal poverty level. Below 400% of it (about $63,840 for one person or $132,000 for a family of four), the cheapest coverage is almost always a Marketplace plan with the premium tax credit. Above it, you are choosing among bronze, catastrophic and narrow-network plans at full price.</p>
      <p>Either way, the plan with the lowest premium is not always the one that costs least over a year. That depends on how much care you use.</p>

      <h2 id="subsidy">If you qualify for a premium tax credit</h2>
      <p>Your credit is set so that the second-lowest-cost silver plan costs you a fixed share of income, up to 10.22% in 2027. You can apply that credit to any metal level:</p>
      <ul>
        <li><strong>Bronze with the credit applied</strong> often lands at $0 or close to it for lower incomes, because the credit is sized to a more expensive silver plan.</li>
        <li><strong>Silver with cost-sharing reductions</strong> is usually the best deal under 250% of the poverty level (about $39,900 for one person). The deductible and copays drop sharply, and those reductions only exist on silver.</li>
      </ul>
      <p>Use the <a href="/aca-subsidy-calculator">ACA subsidy calculator</a> to see your credit, or the <a href="/blog/aca-income-limits-2027">2027 income limits chart</a> to see where you land.</p>

      <h2 id="bronze">Bronze plus an HSA</h2>
      <p>Since 2026, every bronze and catastrophic plan counts as HSA-compatible. For 2027 you can put in up to <strong>$4,500</strong> for self-only coverage or <strong>$9,000</strong> for a family, plus $1,000 at 55 or older. Contributions are tax-deductible, grow tax-free and pay for qualified care tax-free. They also lower your MAGI, which can increase your credit.</p>
      <p>The trade-off is the deductible. Bronze plans pay less until you hit it, and the out-of-pocket limit for 2027 can be as high as $12,000 for one person. If you can keep that amount in your HSA or savings, bronze is often the cheapest plan over a full year for people who rarely need care.</p>

      <h2 id="catastrophic">Catastrophic plans: no longer just for under 30</h2>
      <p>Catastrophic plans have the lowest premiums on the Marketplace. They cover three primary care visits and preventive care before the deductible, then very little until the out-of-pocket limit.</p>
      <ul>
        <li><strong>Who qualifies:</strong> anyone under 30, plus anyone with a hardship exemption. That now includes people whose income makes them ineligible for premium tax credits or cost-sharing reductions, generally below 100% or above 250% of the poverty level. The 2027 rules made this permanent in every state.</li>
        <li><strong>The catch:</strong> tax credits cannot be applied to catastrophic plans. If you qualify for a credit, a subsidized bronze plan is usually cheaper.</li>
        <li><strong>New for 2027:</strong> insurers may offer multi-year catastrophic plans with terms of up to 10 years. Few are expected in the first year, so ask before you count on one.</li>
      </ul>
      <p>In Florida and other states that did not expand Medicaid, adults under 100% of the poverty level usually get neither Medicaid nor a credit. A catastrophic plan through the hardship exemption is often the most affordable real coverage for them.</p>

      <h2 id="network">Narrow networks cost less</h2>
      <p>Within the same metal level, HMO and EPO plans usually cost less than PPOs because they only cover in-network care (except emergencies). If your doctors are in the network and you stay mostly local, that is a real saving. If you travel for work, the gap can cost more than the premium difference. <a href="/hmo-vs-ppo">HMO vs PPO</a>.</p>

      <h2 id="nonaca">Plans that only look cheaper</h2>
      <p>These products show up near the top of most searches for cheap health insurance. They cost less because they cover less, and none of them qualifies for a premium tax credit.</p>
      <ul>
        <li><strong>Short-term plans</strong> can decline you for pre-existing conditions, exclude whole categories of care and cap benefits.</li>
        <li><strong>Fixed indemnity plans</strong> pay a set dollar amount per day or per service, not your actual bill.</li>
        <li><strong>Health care sharing ministries</strong> are not insurance and do not guarantee payment.</li>
      </ul>
      <p>They can make sense as a short bridge for healthy people. They are not a cheaper version of a Marketplace plan. <a href="/private-health-insurance">How private and ACA plans compare</a>.</p>

      ''' + cta("Want the cheapest plan that still covers you?", "We price every plan in your ZIP, with your credit applied, and show you what a bad year would cost on each. Free.") + '''

      <h2 id="compare">Side by side</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>Option</th><th>Premium</th><th>Who it fits</th><th>Watch out for</th></tr></thead>
        <tbody>
          <tr><td>Bronze with credit</td><td>Lowest for many subsidized buyers, often $0</td><td>Lower incomes, light users of care</td><td>High deductible</td></tr>
          <tr><td>Silver with cost-sharing reductions</td><td>Low with credit</td><td>Income under 250% of poverty level</td><td>Only on silver; check the network</td></tr>
          <tr><td>Bronze + HSA</td><td>Low, plus tax savings</td><td>Healthy people who can save for the deductible</td><td>Out-of-pocket limit up to $12,000</td></tr>
          <tr><td>Catastrophic</td><td>Lowest full-price premium</td><td>Under 30, or no credit due to income</td><td>No tax credit; little coverage before the limit</td></tr>
          <tr><td>HMO / EPO</td><td>Lower than PPO at the same tier</td><td>People whose care is local</td><td>No routine out-of-network care</td></tr>
          <tr><td>Short-term / indemnity / sharing</td><td>Low</td><td>A brief bridge, if healthy</td><td>Not ACA coverage; pre-existing conditions</td></tr>
        </tbody>
      </table>
      </div>
      <p>Open Enrollment for 2027 runs November 1, 2026 to January 15, 2027. Choose by December 15 for January 1 coverage. Already on a plan? <a href="/blog/health-insurance-renewal-notice-2027">Check your renewal notice first</a>.</p>
      ''' + SOURCES_COMMON

# =========================================================================== #
# 5. Trucking: owner-operator premiums 2027
# =========================================================================== #
TOC_OO = [("changed", "What Changed for Drivers"), ("fixes", "8 Ways to Cut the Cost"),
          ("example", "A Worked Example"), ("company", "Company Drivers"),
          ("road", "Enrolling From the Road"), ("faq", "FAQ")]

FAQ_OO = [
 ("How much will owner-operator health insurance go up in 2027?",
  "Insurers asked for a median 15% increase nationally for 2027, and in Florida the requests ranged from about 4% to "
  "about 39%. What you actually pay depends more on your subsidy than on the rate increase. A driver whose household "
  "income lands just over 400% of the poverty level can see the full price after paying a fraction of it, which is a far "
  "bigger jump than any rate filing."),
 ("Does an owner-operator qualify for an ACA subsidy on gross or net income?",
  "Net. The subsidy is based on modified adjusted gross income, which for an owner-operator starts from Schedule C net "
  "profit after fuel, maintenance, insurance, truck payments and other business expenses, then subtracts half of your "
  "self-employment tax and other above-the-line deductions. Using gross settlements is the most expensive mistake drivers "
  "make on the application."),
 ("Can a Solo 401(k) or SEP-IRA get me back under the subsidy cliff?",
  "Often, yes. Contributions to a Solo 401(k) or SEP-IRA reduce your MAGI. For 2026, the Solo 401(k) employee deferral "
  "limit is $24,500, plus catch-up contributions from age 50, and total contributions can reach $72,000. SEP-IRA "
  "contributions can be made up to your tax filing deadline, so you can fine-tune once you know your real profit. The "
  "IRS publishes 2027 limits late in the year."),
 ("Is my health insurance tax deductible as an owner-operator?",
  "Generally yes. The self-employed health insurance deduction covers premiums for you, your spouse and dependents, "
  "reduces adjusted gross income whether or not you itemize, and is limited to your net self-employment profit. Because "
  "it also lowers the income used for your subsidy, the IRS provides a method for calculating both together."),
 ("My Marketplace plan is with Cigna. What happens in 2027?",
  "Cigna is leaving the ACA Marketplace in all 11 of its states, including Florida, for 2027. You will need a new plan. "
  "Choose one yourself during Open Enrollment, by December 15 for a January 1 start, and check how it handles care "
  "outside your home state before you enroll."),
 ("Can I use an HSA for my DOT physical?",
  "A DOT medical exam is generally a qualified medical expense if your health plan or employer does not reimburse it, "
  "so it can be paid from an HSA. Since 2026 every bronze plan is HSA-compatible, which makes an HSA available to many "
  "more drivers. Keep the receipt with your tax records."),
]

BODY_OO = '''<h2 id="changed">What changed for drivers in 2027</h2>
      <p>Three things hit owner-operators at once this year:</p>
      <ul>
        <li><strong>Rates are up again.</strong> Insurers asked for a median 15% increase for 2027, after a 26% benchmark jump in 2026. Florida filings ranged from about 4% to about 39%.</li>
        <li><strong>The subsidy cliff is back.</strong> Above 400% of the poverty level there is no premium tax credit: about $63,840 for a single driver, $86,560 for a couple and $132,000 for a family of four. A good year can cost you thousands in lost credit.</li>
        <li><strong>An insurer is leaving.</strong> Cigna is exiting the Marketplace in all 11 of its states, including Florida, so a lot of drivers need a new plan whether they wanted one or not.</li>
      </ul>
      <div class="highlight-box">
        <h4>Where you stand in one minute</h4>
        <p>Plug your net profit into the <a href="/owner-operator-subsidy-cliff-calculator">owner-operator subsidy cliff calculator</a>. It shows how close you are to the 400% line and how much a Solo 401(k), SEP or HSA contribution would need to be to get you under it.</p>
      </div>

      <h2 id="fixes">8 ways owner-operators cut the 2027 cost</h2>

      <h3>1. Report net profit, not settlements</h3>
      <p>Your subsidy is based on MAGI, which starts from Schedule C net profit, after fuel, maintenance, insurance, the truck payment, per diem and everything else. A driver grossing $220,000 can easily net $65,000. Putting the gross number on the application can cost the whole credit. <a href="/truck-driver-health-insurance-cost-calculator">Our driver cost calculator</a> starts from settlements and expenses for that reason.</p>

      <h3>2. Use a Solo 401(k) or SEP-IRA to get under the line</h3>
      <p>Retirement contributions lower MAGI. For 2026, a Solo 401(k) allows a $24,500 employee deferral (plus $8,000 at 50 or $11,250 at ages 60 to 63), and total contributions can reach $72,000. A SEP-IRA can be funded up to your tax filing deadline, which lets you set the amount once you know what the year really netted. The IRS announces the 2027 limits late in the year.</p>

      <h3>3. Take the self-employed health insurance deduction</h3>
      <p>Premiums for you, your spouse and your kids are deductible above the line, and that deduction lowers the same income figure your subsidy uses. Tax software and the IRS worksheet handle the back-and-forth between the two.</p>

      <h3>4. Pair a bronze plan with an HSA</h3>
      <p>Since 2026 every bronze plan is HSA-compatible. For 2027 you can contribute up to $4,500 single or $9,000 family, plus $1,000 at 55. That lowers MAGI too, rolls over every year, and can pay for things like your DOT physical and prescriptions tax-free.</p>

      <h3>5. Check the network before you check the price</h3>
      <p>The cheapest plan in your ZIP is usually an HMO or EPO built around your home town. That works for your family. It does not work for you in a clinic three states away, where only emergencies are covered. Compare the PPO premium against what routine out-of-state care would cost you. <a href="/nationwide-ppo-health-insurance-truck-drivers">Nationwide PPO options for drivers</a>.</p>

      <h3>6. Split the household if it is cheaper</h3>
      <p>Your spouse and kids do not have to be on your plan. A PPO for you and a local plan for them can cost less than one PPO for everyone. Subsidy eligibility is still based on household income, so the split is about buying the right plan for each person, not hiding income. <a href="/blog/truck-driver-family-health-insurance-guide">Family coverage for drivers</a>.</p>

      <h3>7. Price a catastrophic plan if you are well over the cliff</h3>
      <p>If your income is above 250% of the poverty level, you can request a hardship exemption to buy a catastrophic plan, whatever your age. It has the lowest full-price premium on the Marketplace. Credits do not apply to it, so it mainly makes sense for drivers who get no credit anyway.</p>

      <h3>8. Do not let it auto-renew from the road</h3>
      <p>If you are not home when the renewal letter arrives, the Marketplace renews you automatically, using old income data and a benchmark that may have moved. If your insurer is leaving, you get placed in whatever is closest. Set a reminder to shop between November 1 and December 15. <a href="/truck-driver-open-enrollment-2027">Open Enrollment 2027 for drivers</a>.</p>

      ''' + cta("Over the cliff, or close to it?", "We run your subsidy from net profit, show you exactly how much a retirement contribution has to be, and price PPOs that travel. Call or text from the cab.") + '''

      <h2 id="example">A worked example</h2>
      <p>A single owner-operator in Florida nets <strong>$70,000</strong> on Schedule C for 2027.</p>
      <div class="vs-tw">
      <table class="vs-t" style="min-width:0">
        <thead><tr><th>Step</th><th>Amount</th></tr></thead>
        <tbody>
          <tr><td>Schedule C net profit</td><td>$70,000</td></tr>
          <tr><td>Less half of self-employment tax (about)</td><td>&minus;$4,945</td></tr>
          <tr><td>MAGI before any planning</td><td>about $65,055</td></tr>
          <tr><td>400% line for a household of one (2027 coverage)</td><td>$63,840</td></tr>
          <tr><td>Over the cliff by</td><td>about $1,215</td></tr>
          <tr><td>Solo 401(k) or SEP contribution needed</td><td>about $1,300 or more</td></tr>
        </tbody>
      </table>
      </div>
      <p>Without the contribution, this driver gets no credit and pays full price. With it, the benchmark silver plan is capped at 10.22% of income and the credit covers the rest. The credit grows with age and with how expensive plans are in your ZIP: for a driver in their 50s it is often worth several thousand dollars a year, and the contribution is not a cost at all, since it stays in the driver's own retirement account. Run your own numbers in the <a href="/owner-operator-subsidy-cliff-calculator">subsidy cliff calculator</a> before you decide.</p>

      <h2 id="company">If you are a company driver</h2>
      <p>Your carrier's plan renewal is coming too. Do not assume it wins. If the family premium is unaffordable under the IRS test, your spouse and kids may qualify for a Marketplace credit even while you stay on the company plan. <a href="/best-trucking-company-health-benefits">How to judge a fleet's benefits</a>.</p>

      <h2 id="road">Enrolling from the road</h2>
      <p>You can do all of it by phone. Have your last Schedule C or a year-to-date profit figure, your household's birth dates and your current doctors and prescriptions ready. Open Enrollment runs November 1, 2026 to January 15, 2027; choose by December 15 for a January 1 start.</p>
      <p><a href="/blog/how-to-lower-health-insurance-premiums-2027">More ways anyone can lower a 2027 premium</a> &middot; <a href="/blog/losing-health-insurance-2027">If your plan is ending</a></p>
      ''' + SOURCES_COMMON.replace('2026 HHS poverty guidelines.', '2026 HHS poverty guidelines; IRS Notice 2025-67 (2026 retirement limits).')

POSTS = [
 dict(slug="how-to-lower-health-insurance-premiums-2027",
      title="How to Lower Your Health Insurance Premium in 2027",
      h1="How to Lower Your Health Insurance Premium in 2027: 11 Moves That Work",
      desc="Premiums are up a median 15% for 2027 and the subsidy cliff is back. 11 legal ways to pay less during Open Enrollment, from income planning to HSA bronze plans.",
      lede="Rates are up again and the subsidy that used to absorb increases is smaller. You still have more control over your 2027 price than your renewal letter suggests.",
      read_min=9, eyebrow="Open Enrollment 2027",
      img="/compressed/health-insurance-cost-2026-woman.jpg",
      alt="Woman reviewing her 2027 health insurance premium",
      toc=TOC_LOWER, body=BODY_LOWER, faq=FAQ_LOWER,
      cta_head="Premium going up?",
      cta_copy="We compare every plan in your ZIP at your real 2027 income. Same price as buying direct, free help."),
 dict(slug="health-insurance-renewal-notice-2027",
      title="Health Insurance Renewal Notice 2027: Don't Auto-Renew",
      h1="Got Your 2027 Health Insurance Renewal Notice? Check These 6 Things First",
      desc="Your renewal notice uses last year's income and a benchmark that just moved. What happens if you do nothing, and the 6 checks to make before Dec 15.",
      lede="The number on your renewal letter is an estimate built on old data. Here is how to read it, and when switching saves money.",
      read_min=7, eyebrow="Open Enrollment 2027",
      img="/compressed/insurance-advisor-woman.jpg",
      alt="Advisor reviewing a health insurance renewal notice",
      toc=TOC_RENEW, body=BODY_RENEW, faq=FAQ_RENEW,
      cta_head="Got your renewal letter?",
      cta_copy="Send it to us. We check it against every plan in your ZIP and tell you whether to keep it or switch."),
 dict(slug="losing-health-insurance-2027",
      title="Losing Health Insurance in 2027? What to Do Next",
      h1="Losing Your Health Insurance in 2027? Who Is Affected and What to Do",
      desc="Cigna is leaving the Marketplace, the subsidy cliff is back and Medicaid work rules start in 2027. Who is losing coverage, your deadlines and how to avoid a gap.",
      lede="Insurer exits, the subsidy cliff, Medicaid changes and new immigrant rules are all ending coverage for people this fall. Here is what applies to you and what to do before January 1.",
      read_min=8, eyebrow="Open Enrollment 2027",
      img="/compressed/family-picture.jpg",
      alt="Family reviewing health coverage options for 2027",
      toc=TOC_LOSE, body=BODY_LOSE, faq=FAQ_LOSE,
      cta_head="Is your plan ending?",
      cta_copy="We line up the replacement before your coverage ends, at no cost to you."),
 dict(slug="cheapest-health-insurance-2027",
      title="Cheapest Health Insurance in 2027: What Costs Less",
      h1="The Cheapest Health Insurance in 2027: Bronze, HSA and Catastrophic Plans Compared",
      desc="The lowest-cost real coverage for 2027 by income: subsidized bronze, silver with extra savings, bronze plus HSA, and catastrophic plans, now open to more people.",
      lede="The cheapest plan depends on your income and how much care you use. Here is what actually costs less in 2027, and what only looks cheaper.",
      read_min=8, eyebrow="Open Enrollment 2027",
      img="/compressed/ACAphoto.jpg",
      alt="Comparing the cheapest health insurance options for 2027",
      toc=TOC_CHEAP, body=BODY_CHEAP, faq=FAQ_CHEAP,
      cta_head="Looking for the lowest price?",
      cta_copy="We price every plan in your ZIP with your credit applied and show what a bad year would cost on each."),
 dict(slug="owner-operator-health-insurance-increase-2027",
      title="Owner-Operator Health Insurance Going Up in 2027?",
      h1="Owner-Operator Health Insurance Going Up in 2027? 8 Ways to Cut the Cost",
      desc="Rates are up, the 400% subsidy cliff is back and Cigna is leaving the Marketplace. 8 ways owner-operators and truck drivers cut their 2027 health insurance cost.",
      lede="A good year on the road can cost a driver the whole subsidy. Here is how owner-operators keep the credit and pay less for 2027.",
      read_min=8, eyebrow="Trucking",
      img="/compressed/truck-driver-hands-on-wheel-sunrise.jpg",
      alt="Owner-operator truck driver at sunrise",
      toc=TOC_OO, body=BODY_OO, faq=FAQ_OO,
      cta_head="Owner-operator?",
      cta_copy="We run your subsidy from net profit and show exactly what a Solo 401(k) or SEP would save you."),
]

for p in POSTS:
    build(p["slug"], p["title"], p["h1"], p["desc"], p["lede"], TODAY, p["read_min"],
          p["eyebrow"], p["img"], p["alt"], p["toc"], p["body"] + "\n\n      " + faq_html(p["faq"]), p["faq"],
          p["cta_head"], p["cta_copy"], cta_href="/quote?type=individual")

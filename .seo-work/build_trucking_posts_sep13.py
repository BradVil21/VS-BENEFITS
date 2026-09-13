# -*- coding: utf-8 -*-
"""Three educational trucking posts, 13 September 2026.

Each targets a query family with impressions and no page pointed at it:
  family coverage for drivers      "health insurance for truck drivers and their family" (44 imp, pos 52)
  affordable coverage for drivers  "affordable health insurance for truck drivers" (40 imp, pos 56)
  company driver -> owner-operator no page, and it is the moment coverage breaks

House rule from the earlier passes: no carrier-specific benefit claims, no
invented premium tables, and every regulatory figure matches what the rest of
the site already publishes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

TODAY = "2026-09-13"

# =========================================================================== #
# 1. Family coverage
# =========================================================================== #
FAQ_FAM = [
 ("Can a truck driver put their family on a health insurance plan?",
  "Yes. Individual and Marketplace plans are sold as family coverage, and your spouse and children can be on the same "
  "plan as you. Children can stay on a parent's plan until they turn 26, whether or not they live at home or are "
  "financially dependent. What changes for a driver is not eligibility, it is network design: the plan is built around "
  "your home address, so your family sees in-network doctors at home while you may be 1,000 miles away."),
 ("Whose address does the plan use if I am on the road?",
  "The address where you live and file taxes, not where you happen to be parked. Plan availability, pricing and the "
  "provider network all key off your home ZIP code. That is why a driver whose family stays in one place usually wants "
  "a plan whose network is strong at home for the family, and broad enough nationally to cover the driver."),
 ("Does my family need a PPO too, or just me?",
  "You are on one plan together, so whatever network the plan has applies to everyone on it. A PPO costs more than a "
  "comparable HMO, and the reason to pay for it is you: your spouse and kids can use a local network fine, while you "
  "need care in states nobody planned for. If the household budget cannot stretch to a PPO, the fallback is an HMO or "
  "EPO plus a clear understanding of how emergency care works away from home."),
 ("What happens if I get sick or hurt out of state on an HMO?",
  "Emergency care is covered at the in-network level regardless of where you are, under the federal emergency services "
  "rules that apply to ACA-compliant plans. What is not covered on a narrow-network plan is routine or follow-up care "
  "out of state, which is exactly what a driver needs after the emergency room visit. That gap is the practical case "
  "for a national PPO network."),
 ("Is it cheaper to cover my family separately from me?",
  "Sometimes, and it is allowed. Household members do not all have to be on the same policy. Subsidy eligibility is "
  "still calculated on your whole household income and family size, so splitting does not hide income, but a driver "
  "who needs a national PPO and a family who only needs local care can occasionally land on two plans for less than "
  "one plan that tries to do both. It is worth pricing both ways before you enroll."),
 ("If my trucking company offers a plan, can my family get a subsidy instead?",
  "Possibly. Since 2023, a family member's subsidy eligibility is measured against the cost of the employer's family "
  "coverage rather than the employee-only cost, which is the fix to what was known as the family glitch. If your "
  "company's family premium is unaffordable by the IRS standard, your spouse and children may qualify for premium tax "
  "credits on a Marketplace plan even though your own employee-only coverage is affordable."),
 ("Does a family plan cover my kids' dental?",
  "Children's dental is one of the ten essential health benefits, so pediatric dental is either built into an "
  "ACA-compliant plan or offered alongside it. Adult dental is not included, which is why most families add a "
  "standalone dental and vision plan. Ours are compared on our dental and vision page."),
]

TOC_FAM = [("who", "Who You Are Covering"), ("network", "The Network Problem"),
           ("cost", "What Family Coverage Costs"), ("employer", "If Your Company Offers a Plan"),
           ("split", "Two Plans, One Household"), ("checklist", "Before You Enroll"), ("faq", "FAQ")]

BODY_FAM = '''<h2 id="who">You are insuring two different lives at once</h2>
      <p>This is the part that generic health insurance advice gets wrong for drivers. A family plan normally covers people who live in the same place, see doctors in the same town and use the same hospital. Your household does not work that way. Your spouse and kids use care within a few miles of home. You use care wherever the load put you.</p>
      <p>One policy has to do both jobs. Everything below is about how to make that choice deliberately instead of discovering the gap at a clinic in another state.</p>
      <div class="highlight-box">
        <h4>The one-sentence version</h4>
        <p>Your plan is built around your home address, so the network decision is really about you, not your family &mdash; they are covered at home either way.</p>
      </div>

      <h2 id="network">The network problem, in plain terms</h2>
      <p>Health plans come in a few network shapes, and the differences matter more to a driver than the premium does.</p>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>Plan type</th><th>Your family at home</th><th>You, three states away</th></tr></thead>
        <tbody>
          <tr><td>HMO</td><td>Works well, usually the cheapest</td><td>Emergencies only; routine care generally not covered</td></tr>
          <tr><td>EPO</td><td>Works well</td><td>Emergencies covered; out-of-network care generally not</td></tr>
          <tr><td>PPO</td><td>Works well</td><td>In-network and out-of-network care both covered, at different rates</td></tr>
        </tbody>
      </table>
      </div>
      <p>Emergency care is the exception that confuses people. Under federal rules, an ACA-compliant plan has to cover emergency services at the in-network level no matter where you are. So an HMO will not leave you stranded after a heart attack in Nebraska. What it will not do is pay for the follow-up visit, the imaging a week later or the specialist the ER told you to see, when none of them are in your home network.</p>
      <p>That is the real trade. <a href="/nationwide-ppo-health-insurance-truck-drivers">Our nationwide PPO guide for drivers</a> covers which states actually have PPO options on the exchange, because in several states they are scarce.</p>

      <h2 id="cost">What family coverage actually costs</h2>
      <p>Family premiums scale with the number of people and their ages, with children priced lower than adults, and only the three oldest children under 21 counting toward the family premium. Beyond that, two things move the number more than anything else:</p>
      <ul>
        <li><strong>Your household income estimate.</strong> Premium tax credits are calculated on household income and family size, so a family of four qualifies at a much higher income than a single driver. For 2027 the cutoff sits at 400% of the federal poverty level, roughly $130,000 for a family of four, with no credit at all above it now that the enhanced subsidies have expired.</li>
        <li><strong>Whose income counts.</strong> For an owner-operator it is net Schedule C profit, not gross settlements. This is the single most common mistake we see, and it usually costs the family thousands. <a href="/truck-driver-health-insurance-cost-calculator">Our driver cost calculator</a> works from settlements and expenses for that reason.</li>
      </ul>
      <p>We do not publish premium tables because a real quote depends on your ZIP, ages, plan and income. What we can say is that the gap between a guessed income and an accurate one is routinely larger than the gap between two carriers' prices.</p>

      <h2 id="employer">If your trucking company offers a plan</h2>
      <p>Company drivers with a plan on offer have a second decision, and a rule change in 2023 made it a better one for families.</p>
      <p>Before that change, a family's subsidy eligibility was measured against the cost of <em>employee-only</em> coverage. If your own coverage was affordable, your family was locked out of tax credits even when the family premium was out of reach. That was known as the family glitch. Since the IRS fix took effect, family members are measured against the cost of <em>family</em> coverage instead.</p>
      <p>In practice: if your employer's family premium is unaffordable under the IRS standard, your spouse and children may qualify for premium tax credits on a Marketplace plan while you stay on the company plan. That is a legitimate, common split, and it is worth running the numbers on every year at open enrollment.</p>

      <h2 id="split">Two plans, one household</h2>
      <p>Nothing requires everyone in a household to be on the same policy. A driver who needs a national PPO and a family who only ever uses the pediatrician eight minutes from the house are buying two different products.</p>
      <p>Subsidy math does not change when you split &mdash; household income and household size still drive eligibility for everyone &mdash; but the plan design can. We price both configurations for drivers regularly, and roughly speaking, splitting tends to win when the PPO premium difference is large and the family's care is genuinely local.</p>
      <p>It tends to lose when splitting creates two deductibles that both have to be met in a bad year. Ask for both numbers before you decide.</p>

      <h2 id="checklist">Before you enroll, check these five things</h2>
      <ol>
        <li><strong>Your family's actual doctors</strong>, by name, in the plan's network directory. Not the hospital system, the individual pediatrician and OB.</li>
        <li><strong>How the plan handles you out of state</strong>, for routine care, not just emergencies.</li>
        <li><strong>The family out-of-pocket maximum</strong>, which is what a genuinely bad year costs you, not the deductible.</li>
        <li><strong>Whether your income estimate is net</strong>, if you are an owner-operator. Gross settlements will cost you the credit.</li>
        <li><strong>Pediatric dental</strong>, and whether you need a <a href="/dental-vision-insurance">standalone dental and vision plan</a> for the adults.</li>
      </ol>
      <p>Open enrollment for 2027 coverage runs 1 November 2026 to 15 January 2027. Enroll by 15 December for coverage that starts 1 January; enroll after that and your start date moves to 1 February. <a href="/truck-driver-open-enrollment-2027">The driver open enrollment guide</a> has the full calendar.</p>'''

# =========================================================================== #
# 2. Affordable coverage
# =========================================================================== #
FAQ_AFF = [
 ("What is the cheapest health insurance for a truck driver?",
  "The cheapest real coverage for most drivers is a Marketplace plan with a premium tax credit applied, because the "
  "credit is money nobody else can match. Cheaper-looking products exist, such as short-term plans, fixed indemnity "
  "and accident-only coverage, but they are not comprehensive major medical and several of them do not cover a "
  "pre-existing condition at all. Cheap and covered are different questions, and the second one is the one that "
  "matters when something happens."),
 ("How much is health insurance for a truck driver per month?",
  "Unsubsidized individual plans commonly run a few hundred to roughly $900 a month for a single driver depending on "
  "age, state and plan level. With premium tax credits applied, many owner-operators pay far less than that. Because "
  "the subsidy is calculated on your net income rather than your gross settlements, two drivers hauling the same "
  "freight can pay very different premiums."),
 ("Does a lower premium mean I pay less overall?",
  "Not necessarily. A bronze plan has the lowest premium and the highest deductible; a silver plan costs more monthly "
  "and pays sooner. If your income qualifies you for cost-sharing reductions, those apply only to silver plans, which "
  "can make silver cheaper in total than bronze even though the monthly number is higher. The right comparison is "
  "premium plus expected out-of-pocket costs over a year, not premium alone."),
 ("Can I deduct my health insurance premiums as an owner-operator?",
  "Generally yes. The self-employed health insurance deduction is taken above the line, so it reduces your adjusted "
  "gross income whether or not you itemize. It applies to premiums for you, your spouse and your dependents, subject "
  "to the usual limits, and it interacts with your subsidy because both are driven by the same income figure."),
 ("Is an HSA worth it for a driver?",
  "For a healthy driver on a qualifying high-deductible plan, it is one of the few genuinely free wins available. "
  "Contributions reduce taxable income, the money rolls over year to year rather than expiring, and it can be spent "
  "on qualified expenses tax-free, including the DOT physical. The catch is that it only works with an HSA-eligible "
  "high-deductible plan, so it has to be part of the plan choice rather than an afterthought."),
 ("What is the cheapest option if I missed open enrollment?",
  "It depends on why you missed it. A qualifying life event in the last 60 days, such as losing job-based coverage, "
  "reopens the Marketplace. Without one, the honest options are a privately underwritten plan, which is medically "
  "underwritten and can decline you, or waiting for the next open enrollment. Anything advertised as guaranteed, "
  "instant and cheap outside those windows deserves a close read of what it actually pays."),
]

TOC_AFF = [("meaning", "What Affordable Means"), ("lever1", "Lever 1: Your Income Figure"),
           ("lever2", "Lever 2: Metal Tier"), ("lever3", "Lever 3: Network"),
           ("lever4", "Lever 4: Tax Treatment"), ("cheap", "When Cheap Is Not Coverage"),
           ("faq", "FAQ")]

BODY_AFF = '''<h2 id="meaning">"Affordable" is four decisions, not one number</h2>
      <p>Drivers search for affordable health insurance and get sold a premium. The premium is one of four levers, and for most owner-operators it is not even the biggest one.</p>
      <p>Here is what actually moves what you pay in a year, in order of how much money is usually on the table.</p>

      <h2 id="lever1">Lever 1: the income figure you report</h2>
      <p>This is the big one, and it is the one most drivers get wrong.</p>
      <p>Premium tax credits are calculated on modified adjusted gross income. For an owner-operator that starts from <strong>net</strong> Schedule C profit, after fuel, maintenance, insurance, permits, depreciation and the rest &mdash; not from gross settlements. A driver who reports $180,000 in settlements when the business nets $62,000 is telling the Marketplace he earns nearly three times what he does, and the credit disappears.</p>
      <p>With the enhanced subsidies expired, 2027 has a hard cutoff at 400% of the federal poverty level, roughly $63,000 for a single adult and about $130,000 for a family of four. Above that line there is no credit at all, which makes an accurate estimate worth more than shopping carriers. <a href="/truck-driver-health-insurance-cost-calculator">The driver calculator</a> works from settlements minus expenses for exactly this reason.</p>
      <div class="highlight-box">
        <h4>The other half of the same rule</h4>
        <p>Estimating too low is not a strategy either. Subsidies are reconciled on your tax return, so an underestimate comes back as a repayment. An honest estimate that turns out wrong is normal; a deliberately low one is a false statement on a federal application.</p>
      </div>

      <h2 id="lever2">Lever 2: which metal tier you buy</h2>
      <p>Bronze has the lowest premium and the highest deductible. Gold is the reverse. Silver sits in the middle and carries something the others do not: <strong>cost-sharing reductions</strong>, which lower your deductible and out-of-pocket maximum if your income qualifies. Those apply only to silver plans.</p>
      <p>That is why "cheapest premium" and "cheapest year" often point at different plans. A driver who qualifies for cost-sharing reductions and buys bronze to save $60 a month can spend that difference back in one urgent care visit and a prescription.</p>
      <p>The question to ask is not which premium is lowest, but what a bad year costs you. That number is the out-of-pocket maximum, and it is the one worth comparing.</p>

      <h2 id="lever3">Lever 3: the network you are paying for</h2>
      <p>A narrow-network plan is cheaper because the insurer negotiated with fewer providers. For someone who lives and works in one county, that is often a fine trade. For a driver, it is the trade that turns a $40 savings into a $2,000 bill.</p>
      <p>Emergency care is covered at in-network rates wherever you are. Routine and follow-up care is not, unless the plan travels. Before you take the cheaper premium, decide honestly how often you need care in a state you do not live in.</p>

      <h2 id="lever4">Lever 4: what the tax code gives back</h2>
      <p>Two things quietly reduce the real cost of coverage for a self-employed driver:</p>
      <ul>
        <li><strong>The self-employed health insurance deduction.</strong> Taken above the line, so you get it whether or not you itemize. <a href="/blog/can-owner-operators-deduct-health-insurance">How it works for owner-operators</a>.</li>
        <li><strong>An HSA, if your plan qualifies.</strong> Contributions reduce taxable income, the balance rolls over, and qualified spending comes out tax-free &mdash; including the DOT physical, which health plans themselves <a href="/does-health-insurance-cover-dot-physical">almost never cover</a>.</li>
      </ul>
      <p>Neither shows up on the premium quote, and together they change the arithmetic more than switching carriers usually does.</p>

      <h2 id="cheap">When cheap is not coverage</h2>
      <p>Everything above is about buying comprehensive major medical for less. There is a separate category of products that look cheaper because they cover less, and drivers get pitched them constantly at truck stops and in load board ads.</p>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>Product</th><th>What it does</th><th>What to check first</th></tr></thead>
        <tbody>
          <tr><td>Occupational accident</td><td>Responds to injuries arising out of your work</td><td>It excludes illness. It is not health insurance.</td></tr>
          <tr><td>Fixed indemnity</td><td>Pays a set amount per service or per day</td><td>Whether there is any out-of-pocket maximum at all</td></tr>
          <tr><td>Short-term medical</td><td>Temporary coverage, medically underwritten</td><td>Pre-existing condition exclusions and the term limit in your state</td></tr>
          <tr><td>Association or membership plans</td><td>Varies enormously</td><td>Ask for the certificate of coverage, then read what it pays for an inpatient stay</td></tr>
        </tbody>
      </table>
      </div>
      <p style="font-size:.88rem;color:var(--muted)">General product-category behavior, not a description of any particular policy. Your policy documents govern.</p>
      <p>None of these are frauds, and a couple of them have a legitimate place alongside major medical. The mistake is buying one <em>instead</em> of major medical because the monthly number was smaller. <a href="/ooida-health-insurance-vs-aca">We compare association products against Marketplace coverage here.</a></p>'''

# =========================================================================== #
# 3. Company driver to owner-operator
# =========================================================================== #
FAQ_OO = [
 ("What happens to my health insurance when I become an owner-operator?",
  "Your employer coverage ends, usually on your last day or at the end of that month, and you become responsible for "
  "buying your own. Losing job-based coverage is a qualifying life event, which opens a 60-day special enrollment "
  "period on the Marketplace. That window is the most important date in the transition, because missing it can leave "
  "you without a way to buy comprehensive coverage until the next open enrollment."),
 ("How long do I have to get coverage after leaving a company job?",
  "Sixty days from the date your job-based coverage ends, and the window also opens up to 60 days before a known end "
  "date. Lining the new plan up in advance is the cleanest version: you pick a start date that begins the day after "
  "the old coverage stops, and there is no gap at all."),
 ("Should I take COBRA when I go independent?",
  "Sometimes, briefly. COBRA keeps the exact plan and network you already have, which matters if you are mid-treatment "
  "or have met most of your deductible for the year. It is expensive, because you pay the full premium plus an "
  "administrative fee with no employer contribution. The trap to avoid is cancelling COBRA mid-year on your own, which "
  "does not open a special enrollment period; running out the full term does."),
 ("How do I estimate my income for a subsidy in my first year on my own authority?",
  "Make a good-faith projection of net profit, not gross revenue: expected settlements minus fuel, maintenance, "
  "insurance, permits, tires, tolls and depreciation. First-year owner-operators frequently net far less than the "
  "revenue number suggests, especially with a truck payment. Update the Marketplace within 30 days when reality "
  "shifts, and your credit adjusts going forward instead of becoming a tax-time correction."),
 ("Can I keep my company plan after I leave?",
  "Not as an active employee plan. Your options are COBRA continuation for a limited term, a spouse's employer plan if "
  "one is available, a Marketplace plan, or a privately underwritten plan. A spouse's plan is worth checking first, "
  "because your loss of coverage also opens a special enrollment period on their plan."),
 ("Is health insurance deductible once I am an owner-operator?",
  "Generally yes, through the self-employed health insurance deduction, which is taken above the line and so applies "
  "whether or not you itemize. This is one of the real financial differences between being a company driver and being "
  "self-employed, and it is worth factoring into the rate you need to run profitably."),
]

TOC_OO = [("clock", "The 60-Day Clock"), ("options", "Your Four Options"),
          ("cobra", "When COBRA Makes Sense"), ("income", "Estimating Year-One Income"),
          ("timeline", "A Clean Timeline"), ("faq", "FAQ")]

BODY_OO = '''<h2 id="clock">The clock starts the day your company coverage ends</h2>
      <p>Going from a company driver to your own authority changes your taxes, your insurance, your maintenance bill and your risk. The piece that breaks quietly is health coverage, because nothing arrives in the mail to tell you it is about to.</p>
      <p>Losing job-based coverage is a qualifying life event. It opens a <strong>60-day special enrollment period</strong> on the Marketplace, and the window also opens up to 60 days <em>before</em> a known end date. Inside it you can buy comprehensive coverage with no health questions and with premium tax credits if your income qualifies. Outside it, without another life event, you are generally waiting for open enrollment.</p>
      <div class="highlight-box">
        <h4>The mistake that costs the most</h4>
        <p>Letting the 60 days run out while you are busy getting the truck plated and the authority active. Coverage is the one decision in this transition with a hard deadline attached.</p>
      </div>

      <h2 id="options">Your four real options</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>Option</th><th>Best when</th><th>Watch out for</th></tr></thead>
        <tbody>
          <tr><td>Marketplace plan with a subsidy</td><td>Your projected net income qualifies for a premium tax credit</td><td>Estimating from gross settlements instead of net profit</td></tr>
          <tr><td>Spouse's employer plan</td><td>One is available and the family premium is reasonable</td><td>Their plan has its own 30 or 60 day window from your loss of coverage</td></tr>
          <tr><td>COBRA continuation</td><td>Mid-treatment, or most of the deductible already met this year</td><td>Full cost with no employer share; cancelling early opens nothing</td></tr>
          <tr><td><a href="/private-health-insurance">Private, underwritten plan</a></td><td>Healthy, income above the subsidy cutoff, or outside any window</td><td>Health questions; the carrier can exclude a condition or decline</td></tr>
        </tbody>
      </table>
      </div>
      <p>For most drivers making this move, the answer is the first one, because first-year net profit is usually lower than people expect and the credit is correspondingly larger.</p>

      <h2 id="cobra">When COBRA is genuinely the right call</h2>
      <p>COBRA is expensive because you are now paying the whole premium, including the part your employer used to cover, plus an administrative fee. That said, there are two situations where it wins clearly:</p>
      <ul>
        <li><strong>You are mid-treatment.</strong> Keeping the same plan means keeping the same network, the same prior authorizations and the same specialists.</li>
        <li><strong>You have already met most of your deductible.</strong> Starting a new plan resets that to zero. Late in a plan year, that reset can cost more than COBRA does.</li>
      </ul>
      <p>One rule to know either way: dropping COBRA voluntarily partway through does <em>not</em> open a special enrollment period, while exhausting the full term does. <a href="/blog/can-i-drop-cobra-for-marketplace">The full explanation is here</a>, and it is the single most common way drivers end up uninsured by accident.</p>

      <h2 id="income">Estimating your first-year income without wrecking your subsidy</h2>
      <p>The Marketplace asks what you expect to earn this year. As a new owner-operator you genuinely do not know, and that is fine &mdash; the standard is a good-faith estimate, not a guarantee.</p>
      <p>Build it from net profit: expected settlements minus fuel, maintenance, tires, insurance, permits, tolls, parking, the truck payment's interest and depreciation, and any per-diem treatment your accountant uses. First-year operators with a truck note frequently net a fraction of their revenue.</p>
      <p>Then keep it current. Update the Marketplace within 30 days when your income moves materially. Your credit adjusts going forward, which is far better than discovering the difference at tax time on Form 8962. <a href="/blog/what-income-counts-for-aca-subsidies">What counts as income is here</a>, and <a href="/truck-driver-health-insurance-cost-calculator">the driver calculator</a> turns settlements into the figure the Marketplace is actually asking for.</p>

      <h2 id="timeline">A clean timeline, start to finish</h2>
      <ol>
        <li><strong>60 to 30 days out.</strong> Confirm the exact date your company coverage ends. It is often the last day of the month, not your last day driving.</li>
        <li><strong>30 days out.</strong> Project net profit for the rest of the year. Price a Marketplace plan against a private plan and, if relevant, a spouse's plan.</li>
        <li><strong>Two weeks out.</strong> Check that the doctors and prescriptions you actually use are in the new plan's network and formulary.</li>
        <li><strong>Before the end date.</strong> Enroll with a start date of the day after your old coverage ends. Do not cancel anything until the new policy is issued.</li>
        <li><strong>After you are running.</strong> Keep receipts for premiums; they are deductible above the line. Report income changes within 30 days.</li>
      </ol>
      <p>If you want a second set of eyes on the timing, that is what we do, and carriers pay our commission, so it costs you nothing. <a href="/best-health-insurance-owner-operators">Our owner-operator guide</a> compares the four options in more depth.</p>'''



def faq_html(pairs):
    out = ['<h2 id="faq">Frequently asked</h2>']
    for q, a in pairs:
        out.append('<h3>%s</h3>\n      <p>%s</p>' % (q, a))
    return '\n      '.join(out)

POSTS = [
 dict(slug="truck-driver-family-health-insurance-guide",
      title="Health Insurance for Truck Drivers and Their Family",
      h1="Health Insurance for Truck Drivers and Their Family",
      desc="Your family uses doctors at home while you are three states away. How network type, subsidies and the family glitch fix decide what one plan has to do.",
      lede="One policy has to cover a household that lives in one place and a driver who does not. Here is how to choose it deliberately.",
      read_min=7, eyebrow="Trucking",
      img="/compressed/trucking-family-child-at-truck.jpg",
      alt="Truck driver with child beside the truck",
      toc=TOC_FAM, body=BODY_FAM, faq=FAQ_FAM,
      cta_head="Covering the whole household?",
      cta_copy="We price the family together and split, and show you both numbers side by side. Free."),
 dict(slug="affordable-health-insurance-truck-drivers",
      title="Affordable Health Insurance for Truck Drivers, Honestly",
      h1="Affordable Health Insurance for Truck Drivers",
      desc="Four levers set what a driver pays in a year, and the premium is not the biggest one. Income reporting, metal tier, network and tax treatment, explained.",
      lede="Drivers search for affordable coverage and get sold a premium. The premium is one of four levers, and usually not the one holding the money.",
      read_min=8, eyebrow="Trucking",
      img="/compressed/truck-driver-hands-on-wheel-sunrise.jpg",
      alt="Truck driver hands on the wheel at sunrise",
      toc=TOC_AFF, body=BODY_AFF, faq=FAQ_AFF,
      cta_head="Want your real number?",
      cta_copy="We run your subsidy from net profit, not gross settlements, and show you what a bad year would cost on each plan."),
 dict(slug="company-driver-to-owner-operator-health-insurance",
      title="Company Driver to Owner-Operator: Your Health Insurance",
      h1="Company Driver to Owner-Operator: What Happens to Your Health Insurance",
      desc="Leaving a company plan opens a 60-day window. Your four options, when COBRA is worth it, and how to estimate first-year net profit for a subsidy.",
      lede="Going out on your own authority changes your taxes, your risk and your coverage. Coverage is the one with a hard deadline attached.",
      read_min=8, eyebrow="Trucking",
      img="/compressed/truck-driver-highway-view-state-line.jpg",
      alt="Highway view from a truck cab at a state line",
      toc=TOC_OO, body=BODY_OO, faq=FAQ_OO,
      cta_head="Making the jump?",
      cta_copy="We time the switch so there is no gap, and price all four options before you cancel anything."),
]

for p in POSTS:
    build(p["slug"], p["title"], p["h1"], p["desc"], p["lede"], TODAY, p["read_min"],
          p["eyebrow"], p["img"], p["alt"], p["toc"], p["body"] + "\n\n      " + faq_html(p["faq"]), p["faq"],
          p["cta_head"], p["cta_copy"], cta_href="/quote?type=individual")

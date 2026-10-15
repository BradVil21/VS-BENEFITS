# -*- coding: utf-8 -*-
"""Three trucker posts, 15 October 2026. Each covers an intent no existing page owns:
  carrier switch / benefits waiting period, insulin-treated diabetes and the CDL,
  health sharing vs insurance. All link up to /truck-driver-health-insurance.
Facts: 29 CFR 2590.715-2708 (90-day waiting period cap), CMS 'Losing job-based coverage',
49 CFR 391.46 (ITDM), current IRS treatment of sharing-ministry payments (H.R. 2062 not law).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build
TODAY = "2026-10-15"

def faq_html(pairs):
    out = ['<h2 id="faq">Frequently asked</h2>']
    for q, a in pairs:
        out.append('<h3>%s</h3>\n      <p>%s</p>' % (q, a))
    return '\n      '.join(out)

HUB = '<p class="vs-series" style="font-size:.92rem;color:var(--muted)">Part of our complete guide to <a href="/truck-driver-health-insurance">health insurance for truck drivers</a>.</p>\n\n      '

# ---------------------------------------------------------------- 1. waiting period
TOC_W = [("gap","Where the Gap Comes From"),("rules","The 90-Day Rule"),("options","Four Ways to Bridge It"),
         ("compare","Side by Side"),("ask","Ask the Recruiter"),("no-plan","If You Had No Plan Before"),("faq","FAQ")]
BODY_W = HUB + '''<h2 id="gap">Where the gap comes from</h2>
      <p>Drivers change carriers for better miles, better home time or a better truck. Health insurance rarely makes the list until the first week at the new outfit, when orientation mentions that benefits start "after 60 days" or "the first of the month after 90 days."</p>
      <p>Meanwhile the old plan usually ends on your last day or at the end of that month. Put the two dates side by side and most drivers find a gap of one to three months with nothing in it. That gap is exactly when a breakdown, a back injury loading freight or a kid's ER visit tends to happen.</p>
      <div class="highlight-box">
        <h4>The short version</h4>
        <p>Leaving a job that gave you health insurance opens a 60-day window to get a Marketplace plan, and you can get tax credits for the months you are waiting on the new carrier's plan. You do not have to go uninsured.</p>
      </div>

      <h2 id="rules">The 90-day rule, and what it does not promise</h2>
      <p>Federal rules cap a group plan's waiting period at 90 days once you are otherwise eligible. A carrier can also use a reasonable orientation period of up to one month before that clock starts, which is how some drivers end up waiting closer to four months.</p>
      <p>The rule limits how long you wait. It does not require the new plan to be good, affordable or national. A regional carrier's plan may be an HMO built around its terminal city, which matters if you run OTR. Ask before you sign, not after.</p>

      <h2 id="options">Four ways to bridge the wait</h2>
      <h3>1. A Marketplace plan for the gap months</h3>
      <p>Losing job-based coverage is a qualifying life event. You have 60 days after the old coverage ends to pick a plan, and you can pick it up to 60 days before, so it starts the day after the old one stops. Because you are not yet eligible for the new carrier's plan during the waiting period, you can receive premium tax credits for those months if your household income qualifies.</p>
      <p>When the group plan starts, you report the new coverage and end the Marketplace plan. Two things to know: your deductible restarts on the new plan, and your tax credit is reconciled on your tax return, so estimate your full-year household income, both jobs included, as honestly as you can.</p>
      <h3>2. COBRA from the old carrier</h3>
      <p>If your old carrier had 20 or more employees, you can usually keep the same plan through COBRA for up to 18 months, whether you quit or were let go (gross misconduct is the exception). Many states, Florida among them, have similar continuation rules for smaller employers. The catch is cost: you pay the full premium plus up to 2%, with no employer share. You also have 60 days to elect it, and coverage is retroactive when you elect and pay, which is why some drivers wait and only elect if something happens. Our post on <a href="/blog/cobra-60-day-loophole">the COBRA 60-day window</a> explains the risks of that strategy.</p>
      <p>One trap: you cannot get Marketplace tax credits while you are enrolled in COBRA, and dropping COBRA early on purpose does not open a new enrollment window outside open enrollment. Decide between COBRA and the Marketplace at the start of the gap, not halfway through it. More in <a href="/blog/can-i-drop-cobra-for-marketplace">can I drop COBRA for a Marketplace plan</a>.</p>
      <h3>3. A spouse's plan</h3>
      <p>Your loss of coverage is also a qualifying event for a spouse's employer plan, usually with a 30-day window to add you. If your spouse's plan has a decent network where you run, this is often the cheapest bridge.</p>
      <h3>4. Short-term coverage</h3>
      <p>Short-term plans are cheaper because they are not ACA coverage. They can exclude pre-existing conditions, cap benefits and decline to cover you at all, and some states restrict or ban them. For a healthy driver with a short, fixed gap they can work; for anyone with a condition the DOT is already watching, they usually do not. See our <a href="/short-term-health-insurance">short-term health insurance guide</a> before buying one.</p>

      <h2 id="compare">The four options side by side</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>Option</th><th>Tax credits?</th><th>Pre-existing conditions</th><th>Best when</th></tr></thead>
        <tbody>
          <tr><td>Marketplace plan</td><td>Yes, if income qualifies</td><td>Covered</td><td>The gap is a month or more and your income qualifies for help</td></tr>
          <tr><td>COBRA</td><td>No</td><td>Covered</td><td>You are mid-treatment, or already met this year's deductible on that plan</td></tr>
          <tr><td>Spouse's plan</td><td>No (employer plan)</td><td>Covered</td><td>Your spouse has family coverage with a usable network</td></tr>
          <tr><td>Short-term plan</td><td>No</td><td>Often excluded</td><td>Short, fixed gap and no ongoing health conditions</td></tr>
        </tbody>
      </table>
      </div>

      <h2 id="ask">Five questions to ask the recruiter before you switch</h2>
      <ol>
        <li><strong>How long is the waiting period, and when does coverage actually start?</strong> "60 days" and "first of the month after 60 days" can be a month apart.</li>
        <li><strong>Is it a national PPO or a regional network?</strong> Ask for the network name and check your doctors.</li>
        <li><strong>What does the driver pay per week, and what does family coverage cost?</strong> If family coverage is unaffordable, your family may qualify for Marketplace credits even if you take the company plan.</li>
        <li><strong>Is there a deductible credit for the partial year?</strong> Some plans offer one, most do not.</li>
        <li><strong>Are lease or 1099 drivers eligible at all?</strong> Usually not. If you are signing on as a lease operator, plan to buy your own coverage; see <a href="/best-health-insurance-owner-operators">owner-operator health insurance</a>.</li>
      </ol>

      <h2 id="no-plan">If you had no plan at the old carrier</h2>
      <p>Starting a new job is not by itself a qualifying event. If you had no coverage to lose, you generally wait for the new carrier's plan or for open enrollment. Open enrollment for 2027 coverage runs November 1, 2026 to January 15, 2027; enroll by December 15 for coverage that starts January 1. <a href="/truck-driver-open-enrollment-2027">Our driver open enrollment guide</a> has the full calendar.</p>
      <p>Switching carriers this month? Tell us your last day at the old carrier and the new carrier's start date, and we will price the Marketplace and COBRA options side by side. Carriers pay our commission, so it costs you nothing.</p>'''
FAQ_W = [
 ("How long can a trucking company make me wait for health insurance?",
  "Federal rules cap a group health plan's waiting period at 90 days once you are otherwise eligible, and an employer may add a reasonable orientation period of up to one month before the 90 days start. Many carriers use 30, 60 or 90 days."),
 ("Can I get a Marketplace plan while I wait for my new job's insurance?",
  "Yes, if you are losing coverage from your old job. Loss of job-based coverage gives you 60 days to enroll, and because you are not yet eligible for the new employer's plan during the waiting period, you can receive premium tax credits for those months if your income qualifies."),
 ("Is COBRA or a Marketplace plan cheaper for a short gap?",
  "Usually the Marketplace plan, because COBRA has no employer contribution and no tax credits. COBRA can still win if you are in the middle of treatment with the same doctors or have already met most of this year's deductible on that plan."),
 ("Do I get COBRA if I quit my trucking job?",
  "Generally yes. COBRA applies whether you quit or were terminated, except for gross misconduct, as long as the employer had 20 or more employees. Florida and many other states have similar continuation rules for smaller employers."),
 ("What if my old carrier gave me no insurance?",
  "Then there is no coverage to lose, and starting a new job is not a qualifying event on its own. You would wait for the new plan or enroll during open enrollment, which for 2027 coverage runs November 1, 2026 to January 15, 2027."),
]

# ---------------------------------------------------------------- 2. diabetes
TOC_D = [("rule","The Insulin Rule"),("records","The Paperwork"),("insurance","What Your Plan Must Do"),
         ("pick","Picking a Plan"),("road","Insulin on the Road"),("avoid","Coverage to Avoid"),("faq","FAQ")]
BODY_D = HUB + '''<h2 id="rule">Insulin no longer ends a trucking career</h2>
      <p>Until 2018, a driver who needed insulin had to apply for a federal exemption to keep a medical card. FMCSA's insulin-treated diabetes rule replaced that. Today a driver using insulin can be certified by a medical examiner like any other driver, as long as the treating clinician signs off first.</p>
      <p>That makes health insurance part of keeping your CDL. The visits, the meter, the insulin and the eye exams that the rule depends on all run through your plan.</p>
      <div class="highlight-box">
        <h4>The short version</h4>
        <p>Insulin-treated drivers can hold a medical card for up to 12 months at a time. To get it, you need a treating clinician's signed form and 3 months of glucose records, and your insurance has to cover the care that produces both.</p>
      </div>

      <h2 id="rule-details">How the insulin rule works</h2>
      <ul>
        <li><strong>The form.</strong> Your treating clinician, the doctor or nurse practitioner who manages your diabetes, completes the Insulin-Treated Diabetes Mellitus Assessment Form (MCSA-5870).</li>
        <li><strong>The timing.</strong> Your DOT exam has to happen within 45 days after the clinician signs that form.</li>
        <li><strong>The card length.</strong> Up to 12 months, so this is an every-year cycle, not every two years.</li>
        <li><strong>Hypoglycemia.</strong> After a severe low (one that needs someone else's help or causes loss of consciousness, a seizure or coma), you cannot drive until your clinician clears you and completes a new form.</li>
        <li><strong>Eyes.</strong> Severe non-proliferative or proliferative diabetic retinopathy is permanently disqualifying, which is why the annual dilated eye exam matters.</li>
      </ul>
      <p>Drivers whose diabetes is managed without insulin are not covered by this rule; the medical examiner decides card length based on overall control. For blood pressure thresholds that often travel with diabetes, see <a href="/blog/cdl-blood-pressure-health-insurance">blood pressure and your medical card</a>.</p>

      <h2 id="records">The paperwork that keeps you certified</h2>
      <p>The clinician needs at least the preceding 3 months of blood glucose readings while you were on insulin, from an electronic meter that stores the date and time of every reading and can be downloaded. If you are newly started on insulin, expect to build those 3 months of records before you can get a full 12-month card; with missing records the examiner can only certify you for up to 3 months at a time.</p>
      <p>Bring the meter, not a notebook. Handwritten logs do not meet the rule.</p>

      <h2 id="insurance">What an ACA-compliant plan has to do for you</h2>
      <ul>
        <li><strong>It cannot turn you down or charge you more</strong> because you have diabetes. Pre-existing conditions are covered from day one on Marketplace and other ACA-compliant individual plans.</li>
        <li><strong>Preventive care is covered without a copay</strong> when you see an in-network provider, including diabetes screening for adults at risk. Treatment visits, the A1C tests and specialist care fall under your plan's normal cost sharing.</li>
        <li><strong>Prescriptions are an essential health benefit.</strong> Every compliant plan covers prescription drugs, though which insulins and which tier they sit on varies by plan. Many states also cap what state-regulated plans can charge for a month of insulin; ask us what applies in your state.</li>
      </ul>

      <h2 id="pick">Picking a plan when you manage diabetes</h2>
      <ol>
        <li><strong>Check the formulary for your exact insulin</strong> and your test strips or CGM supplies, not just "insulin." Brand and tier change what you pay.</li>
        <li><strong>Look at the out-of-pocket maximum before the premium.</strong> A driver with diabetes will use the plan every month; the cap is what a year really costs.</li>
        <li><strong>Consider silver if your income qualifies for cost-sharing reductions.</strong> Those extra savings apply only to silver plans and can cut deductibles sharply for steady users of care.</li>
        <li><strong>Keep your treating clinician in network.</strong> The MCSA-5870 comes from that person every year; losing them to a network change can cost you your card timeline.</li>
        <li><strong>Think about the road.</strong> Emergencies are covered anywhere, but refills and follow-up visits out of state depend on your network. Our <a href="/nationwide-ppo-health-insurance-truck-drivers">nationwide PPO guide</a> covers when a national network is worth the price.</li>
      </ol>

      <h2 id="road">Insulin on the road</h2>
      <p>Most plans let you fill at national pharmacy chains in any state, and many offer 90-day mail order, which helps if you are out for weeks. Keep insulin in a temperature-controlled cooler in the cab, carry the prescription label, and carry fast sugar for lows. Our <a href="/blog/truck-driver-prescriptions-on-the-road">guide to filling prescriptions on the road</a> covers refills away from home.</p>

      <h2 id="avoid">Coverage to be careful with</h2>
      <p><strong>Short-term plans</strong> can exclude pre-existing conditions, so diabetes care may not be covered at all. <strong>Health sharing programs</strong> are not insurance and commonly limit sharing for pre-existing conditions. <strong>Accident-only and occupational accident policies</strong> do not cover illness. For a driver whose card depends on steady diabetes care, an ACA-compliant plan is the safe floor. More in <a href="/blog/health-sharing-plans-truck-drivers">health sharing vs health insurance for truck drivers</a>.</p>
      <p>Want help matching a plan to your insulin and your clinician? Send us the drug names and your doctor, and we will check every plan for your ZIP. It costs you nothing.</p>'''
BODY_D = BODY_D.replace('<h2 id="rule">','<h2 id="rule">',1).replace('<h2 id="rule-details">','<h2 id="details">')
FAQ_D = [
 ("Can a truck driver with insulin-treated diabetes get a medical card?",
  "Yes. Since FMCSA's 2018 rule, drivers on insulin can be certified without an exemption. The treating clinician completes form MCSA-5870, the DOT exam must happen within 45 days after the clinician signs it, and the card lasts up to 12 months."),
 ("How many months of glucose records do I need for my DOT physical?",
  "At least the preceding 3 months of electronic blood glucose records while on insulin, from a meter that stores the date and time of each reading. Without them, the examiner can certify you for no more than 3 months at a time."),
 ("Can health insurance deny me because I have diabetes?",
  "Not an ACA-compliant plan. Marketplace and other ACA-compliant individual plans cannot deny you or charge you more for a pre-existing condition. Short-term plans and health sharing programs can exclude or limit it."),
 ("Does health insurance cover insulin?",
  "Every ACA-compliant plan covers prescription drugs, but which insulin brands are covered and at what tier differs by plan. Many states also cap monthly insulin costs for state-regulated plans. Check the formulary for your exact insulin before you enroll."),
 ("Does diabetes disqualify me from driving a truck?",
  "Diabetes alone does not. Insulin-treated drivers can be certified annually, and non-insulin diabetes is judged by the medical examiner. A severe hypoglycemic episode pauses driving until your clinician clears you, and severe diabetic retinopathy is permanently disqualifying."),
]

# ---------------------------------------------------------------- 3. health sharing
TOC_H = [("what","What Health Sharing Is"),("compare","Sharing vs Insurance"),("drivers","Why Drivers Get Pitched"),
         ("money","The Money Math"),("when","When It Might Fit"),("check","Before You Join"),("faq","FAQ")]
BODY_H = HUB + '''<h2 id="what">What a health sharing plan actually is</h2>
      <p>Health care sharing programs are groups of members, usually organized around shared religious beliefs, who pay a monthly amount that goes toward other members' medical bills. They are often marketed to truckers as a cheaper alternative to health insurance, and the monthly price usually is lower.</p>
      <p>The reason is in the paperwork: a health sharing program is not insurance. It does not have to follow the ACA's rules, and it does not legally promise to pay your bills.</p>
      <div class="highlight-box">
        <h4>The short version</h4>
        <p>Health sharing is cheaper because it guarantees less. No promise to pay, pre-existing conditions often limited, no tax credits, and no federal tax deduction under current law.</p>
      </div>

      <h2 id="compare">Health sharing vs health insurance, side by side</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th></th><th>ACA-compliant insurance</th><th>Health sharing program</th></tr></thead>
        <tbody>
          <tr><td>Legally required to pay covered claims</td><td>Yes</td><td>No</td></tr>
          <tr><td>Pre-existing conditions</td><td>Covered from day one</td><td>Often excluded or limited, especially early in membership</td></tr>
          <tr><td>Premium tax credits</td><td>Yes, on Marketplace plans if income qualifies</td><td>No</td></tr>
          <tr><td>Out-of-pocket maximum</td><td>Yes, capped by law</td><td>No legal cap; limits set by the program's guidelines</td></tr>
          <tr><td>Preventive care and prescriptions</td><td>Essential benefits</td><td>Varies; often limited</td></tr>
          <tr><td>Self-employed health insurance deduction</td><td>Yes, for eligible owner-operators</td><td>No, under current law</td></tr>
          <tr><td>Can be denied for lifestyle or faith requirements</td><td>No</td><td>Yes; many require a faith statement or lifestyle pledge</td></tr>
        </tbody>
      </table>
      </div>

      <h2 id="drivers">Why drivers get pitched health sharing so often</h2>
      <p>Owner-operators buy their own coverage, often see sticker prices without their tax credits applied, and are easy to reach through trucking groups and load boards. A program that shows a low monthly number looks like the obvious move. The comparison that matters is not that number against a full-price premium. It is that number against your premium <em>after</em> tax credits, which for many drivers is calculated on net Schedule C profit and comes out far lower than they expect. Run your own number with our <a href="/truck-driver-health-insurance-cost-calculator">truck driver cost calculator</a>.</p>

      <h2 id="money">The money math drivers miss</h2>
      <ul>
        <li><strong>No tax credits.</strong> Sharing programs are not Marketplace coverage, so any credit you qualify for is left on the table.</li>
        <li><strong>No deduction.</strong> Under current IRS treatment, sharing payments are not deductible as health insurance premiums or medical expenses and cannot be paid from an HSA. A bill in Congress would change that, but it is not law. Insurance premiums, by contrast, can qualify for the <a href="/blog/can-owner-operators-deduct-health-insurance">self-employed health insurance deduction</a>.</li>
        <li><strong>No cap.</strong> One large claim the program declines to share can cost more than years of premium savings.</li>
      </ul>

      <h2 id="when">When health sharing might fit</h2>
      <p>It can make sense for a driver who is healthy, earns above the subsidy limit, shares the program's beliefs, understands that payment is not guaranteed, and can absorb a large bill if a claim is not shared. It rarely makes sense for a driver with diabetes, high blood pressure, sleep apnea or anything else the DOT physical is already watching, because those are exactly the conditions sharing programs tend to limit. See <a href="/blog/truck-driver-diabetes-health-insurance">diabetes and your CDL</a> for one example.</p>
      <p>A few states require residents to have qualifying coverage or pay a state penalty, and how sharing membership counts varies by state. Check yours before you rely on it.</p>

      <h2 id="check">Before you join, check these five things</h2>
      <ol>
        <li>The written guidelines, especially the pre-existing condition limits and waiting periods.</li>
        <li>The annual and per-incident caps on what can be shared.</li>
        <li>How prescriptions and preventive care are handled, if at all.</li>
        <li>What happens to bills the program decides not to share, in writing.</li>
        <li>Your Marketplace price with tax credits applied, from a licensed agent, for comparison.</li>
      </ol>
      <p>We are licensed insurance agents, so we do not sell health sharing, but we will gladly price real coverage next to the quote you were given so you can compare honestly. It costs you nothing.</p>'''
FAQ_H = [
 ("Is health sharing the same as health insurance?",
  "No. Health care sharing programs are not insurance, are not regulated as insurance, and do not legally guarantee payment of medical bills. They also do not have to cover pre-existing conditions or cap your out-of-pocket costs."),
 ("Can truck drivers use tax credits with a health sharing plan?",
  "No. Premium tax credits apply only to Marketplace health insurance plans. Owner-operators whose subsidy is figured on net income often find a subsidized Marketplace plan costs less than they expected."),
 ("Are health sharing payments tax deductible for owner-operators?",
  "Not under current law. They are not treated as health insurance premiums for the self-employed health insurance deduction or as qualified medical expenses, and they cannot be paid from an HSA. A pending bill would change this, but it has not passed."),
 ("Do health sharing plans cover pre-existing conditions?",
  "Often only partly. Many programs exclude or limit sharing for pre-existing conditions, especially during the first years of membership. Read the program's written guidelines before joining."),
 ("Is health sharing cheaper for truck drivers?",
  "The monthly cost is usually lower than an unsubsidized premium, but the right comparison is against your Marketplace price after tax credits, plus what you would owe if a large bill is not shared. For many drivers the subsidized plan is close in price and far safer."),
]

POSTS = [
 dict(slug="switching-trucking-companies-health-insurance",
      title="Switching Trucking Companies? Cover the Benefits Wait",
      h1="Switching Trucking Companies: How to Cover the 60- to 90-Day Benefits Wait",
      desc="New carrier's plan starts in 60 to 90 days? How drivers bridge the gap with a Marketplace plan, COBRA or a spouse's plan, and what to ask the recruiter.",
      lede="Your old plan ends when you leave. The new carrier's plan starts months later. Here is how to keep coverage in between without overpaying.",
      read_min=7, img="/compressed/truck-driver-walking-city-street.jpg", alt="Truck driver walking to a new job",
      toc=TOC_W, body=BODY_W, faq=FAQ_W, cta_head="Changing carriers?",
      cta_copy="Give us your last day and new start date. We price the gap both ways, free."),
 dict(slug="truck-driver-diabetes-health-insurance",
      title="Diabetes and Your CDL: Insulin, DOT Rules & Insurance",
      h1="Diabetes and Your CDL: Health Insurance That Keeps You Driving",
      desc="Insulin-treated drivers can hold a 12-month medical card. The FMCSA rules, the paperwork, and how to pick a plan that covers your insulin and clinician.",
      lede="Insulin no longer ends a trucking career, but it ties your medical card to your health plan every single year. Here is how to keep both working.",
      read_min=7, img="/compressed/truck-cab-driving-fog-rain.jpg", alt="View from a truck cab on the highway",
      toc=[("rule","Insulin Is Allowed"),("details","How the Rule Works"),("records","The Paperwork"),("insurance","What Your Plan Must Do"),("pick","Picking a Plan"),("road","Insulin on the Road"),("avoid","Coverage to Avoid"),("faq","FAQ")],
      body=BODY_D, faq=FAQ_D, cta_head="Managing diabetes on the road?",
      cta_copy="Send us your insulin and your doctor. We check every plan in your ZIP, free."),
 dict(slug="health-sharing-plans-truck-drivers",
      title="Health Sharing Plans for Truck Drivers: Worth It?",
      h1="Health Sharing Plans vs Health Insurance for Truck Drivers",
      desc="Health sharing looks cheaper, but it is not insurance: no promise to pay, no tax credits, no deduction. What owner-operators should compare before joining.",
      lede="Health sharing programs are pitched hard to owner-operators. The monthly price is lower for a reason. Here is what you give up, side by side.",
      read_min=6, img="/compressed/truck-driver-cb-radio.jpg", alt="Owner-operator talking on the CB radio in the cab",
      toc=TOC_H, body=BODY_H, faq=FAQ_H, cta_head="Got a sharing quote?",
      cta_copy="We will price real coverage with your tax credits next to it, so you can compare honestly."),
]
for p in POSTS:
    build(p["slug"], p["title"], p["h1"], p["desc"], p["lede"], TODAY, p["read_min"], "Trucking",
          p["img"], p["alt"], p["toc"], p["body"] + "\n\n      " + faq_html(p["faq"]), p["faq"],
          p["cta_head"], p["cta_copy"], cta_href="/truckers/quote?from=" + p["slug"])

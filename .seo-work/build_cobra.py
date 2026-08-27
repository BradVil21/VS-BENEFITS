# -*- coding: utf-8 -*-
"""Build /cobra-alternatives.

Cost-shock + alternatives pillar for people holding a COBRA election notice.
Every competitor page that ranks for "alternatives to COBRA" is either stale on
2026 policy or wrong on the cancellation rule. This one is neither.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from state_lib import BASE, build

URL = BASE + '/cobra-alternatives'

TITLE = "COBRA Alternatives: Cheaper Coverage Options"
DESC = ("Your COBRA quote is the full premium your employer used to split with you. Six cheaper "
        "options, the 60-day clock, and the one mistake that locks you out.")

FAQ = [
 ("Why is my COBRA premium so much higher than what I paid at work?",
  "Because you were only ever seeing part of it. Your employer was paying most of the premium and your payroll deduction was the remainder. COBRA lets the plan charge up to 102 percent of the full cost - the whole premium plus a 2 percent administrative fee - so the number on your election notice is the real price of the coverage you already had. Using the 2025 KFF employer survey averages, a worker paying about $120 a month for single coverage sees roughly $793, and a family paying about $571 sees roughly $2,294."),
 ("What are the cheaper alternatives to COBRA?",
  "In rough order of how often they win: a marketplace plan with a premium tax credit, joining a spouse's or partner's employer plan, Medicaid if your income has dropped far enough, staying on a parent's plan if you are under 26, an ICHRA if you are going self-employed and have a business that can fund one, and a short-term plan as a last resort. Losing job-based coverage opens a 60-day special enrollment period for the first four of those."),
 ("How long do I have to decide on COBRA?",
  "At least 60 days, running from the later of the date your election notice was provided or the date you would otherwise lose coverage. Your employer has 30 days to notify the plan and the plan has 14 days to send the notice, so if the employer is also the plan administrator the combined deadline is 44 days from the qualifying event. After you elect, you get at least 45 more days to make the first payment."),
 ("If I elect COBRA, can I still switch to a marketplace plan?",
  "Only in specific windows, and this is where people get hurt. You can switch while you are still inside the original 60 days from losing your job-based coverage. You can switch during annual open enrollment for any reason. And you can switch when COBRA runs out at the end of its full term, which opens a fresh 60-day special enrollment period. What does not work is simply cancelling COBRA in, say, April - voluntarily dropping it is not a qualifying event, and you would be uninsured until January."),
 ("Is COBRA coverage retroactive if I wait to decide?",
  "If you have simply not responded yet and then elect on day 55, coverage is backdated to the date you lost it and you pay premiums back to that date. That is what people mean by the 60-day loophole. But if you signed and returned a waiver and then changed your mind, the plan is not required to backdate - coverage may start only from the date you revoked the waiver, leaving a real gap for anything you were treated for in between. Do not sign a waiver to buy time."),
 ("Can I pay COBRA premiums from my HSA?",
  "Yes. Health insurance premiums are normally not a qualified HSA expense, but continuation coverage is one of the narrow exceptions written into the tax code, and so is coverage while you are receiving unemployment compensation. If you have a funded HSA sitting from your old plan, that is tax-free money you can put against COBRA or against premiums while you are out of work."),
 ("Does a broker cost me anything?",
  "No. Carriers build the commission into the premium whether you use a broker or enroll yourself, so the rate is identical either way. What you get for free is somebody who checks your subsidy against your projected income rather than last year's, checks your doctors are actually in the network, and makes sure the replacement policy is active before anything gets cancelled."),
]

SCHEMA = [
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
  {"@type": "ListItem", "position": 2, "name": "COBRA Alternatives"}]},
 {"@context": "https://schema.org", "@type": "Service",
  "serviceType": "Health insurance alternatives to COBRA continuation coverage",
  "name": "COBRA Alternatives and Replacement Coverage", "url": URL,
  "provider": {"@type": "InsuranceAgency", "name": "VS Health Benefits", "url": BASE + "/",
               "telephone": "+1-954-825-1009", "email": "info@vshealthbenefits.com",
               "address": {"@type": "PostalAddress", "addressLocality": "Miami",
                           "addressRegion": "FL", "addressCountry": "US"}},
  "areaServed": {"@type": "Country", "name": "United States"},
  "audience": {"@type": "Audience",
               "name": "People who have lost job-based coverage and received a COBRA election notice"},
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
             "description": "Free comparison of COBRA against subsidized marketplace and other coverage; carriers pay the broker commission."},
  "availableChannel": {"@type": "ServiceChannel", "serviceUrl": BASE + "/quote?type=individual",
                       "servicePhone": {"@type": "ContactPoint", "telephone": "+1-954-825-1009"}}},
]

BODY = '''<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">COBRA Alternatives</span>
        <h1>Your COBRA quote is <span>the whole premium</span></h1>
        <p class="hero-sub">Not a mistake, and not a penalty. Your employer was paying most of it and you were seeing the rest. Here is what the same coverage costs elsewhere, the clock you are actually on, and the one move that locks you out until January.</p>
        <p><a class="vs-ih-cta" href="/quote?type=individual">See what you would pay instead &rarr;</a></p>
      </div>
      <div>
        <div class="vs-ih-panel">
          <h2 style="font-size:1.05rem;margin:0 0 14px">What you are working with</h2>
          <dl class="vs-ih-dl">
            <div><dt>COBRA price cap</dt><dd>102% of the full premium</dd></div>
            <div><dt>Time to decide</dt><dd>At least 60 days</dd></div>
            <div><dt>Time to pay after electing</dt><dd>At least 45 more days</dd></div>
            <div><dt>Marketplace window</dt><dd>60 days from losing coverage</dd></div>
            <div><dt>How long COBRA lasts</dt><dd>18 months, or 36 for some events</dd></div>
            <div><dt>Our fee</dt><dd>$0 &mdash; carriers pay the commission</dd></div>
          </dl>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Why the number is four to six times what you were paying</h2>
    <div class="vs-ih-key">
      <strong>You never saw the real price of your health insurance. Your payroll deduction was a share of it.</strong>
      <p>Federal law lets a plan charge a COBRA enrollee up to <strong>102 percent</strong> of the full cost of coverage &mdash; everything the employer was paying, plus everything you were paying, plus a 2 percent administrative fee. Nothing has been marked up. You have simply been handed the invoice that used to be split.</p>
    </div>
    <p class="lede">Put the 2025 KFF employer survey averages against it and the jump is stark:</p>
    <div class="vs-ih-scroll">
    <table class="vs-ih-tbl">
      <thead><tr><th>Coverage</th><th>Average total premium</th><th>What you were paying</th><th>COBRA at 102%</th></tr></thead>
      <tbody>
        <tr><td>Single</td><td>$9,325 / yr</td><td>$1,440 / yr &mdash; about $120 a month</td><td><strong>about $793 a month</strong></td></tr>
        <tr><td>Family</td><td>$26,993 / yr</td><td>$6,850 / yr &mdash; about $571 a month</td><td><strong>about $2,294 a month</strong></td></tr>
      </tbody>
    </table>
    </div>
    <p class="vs-ih-src">Premium and worker-contribution averages from the <a href="https://www.kff.org/health-costs/2025-employer-health-benefits-survey/" rel="nofollow noopener" target="_blank">KFF 2025 Employer Health Benefits Survey</a>. The COBRA column is 102% of the total, calculated for illustration &mdash; your actual plan cost will differ. There is one more sting: if you are in month 19 or later of a disability extension, the cap rises to 150 percent.</p>
    <p class="lede">Which is why almost nobody looks at a COBRA notice and thinks it is reasonable. The useful question is not whether it is expensive. It is what the same person can buy somewhere else this week.</p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Six ways to pay less than COBRA</h2>
    <p class="lede">Roughly in the order they tend to win. Losing job-based coverage opens a 60-day special enrollment period, which is what makes the first four possible outside of open enrollment.</p>
    <div class="vs-ih-grid">
      <div class="vs-ih-card">
        <strong>1. A marketplace plan with a premium tax credit</strong>
        <span>The usual answer, and usually the biggest saving. Subsidies are calculated on your <em>projected</em> income for this year, not last year's W-2 &mdash; so a mid-year job loss often qualifies you for far more help than your old salary suggests. Worth modelling properly, because a high year-to-date income can push the projection above the cutoff.</span>
      </div>
      <div class="vs-ih-card">
        <strong>2. A spouse&rsquo;s or partner&rsquo;s employer plan</strong>
        <span>Your loss of coverage opens a special enrollment period on their plan too, and it is frequently the cheapest option on the table because their employer is subsidising it. The window is short and their HR department will not chase you. Check this first, before anything else.</span>
      </div>
      <div class="vs-ih-card">
        <strong>3. Medicaid, if your income dropped far enough</strong>
        <span>Medicaid has no enrollment window &mdash; you can apply any day of the year, and eligibility is assessed on current monthly income, which after a layoff may be very different from your annual figure. If you qualify, this is usually free or close to it.</span>
      </div>
      <div class="vs-ih-card">
        <strong>4. A parent&rsquo;s plan, if you are under 26</strong>
        <span>Losing your own coverage is a qualifying event for joining a parent's plan. Straightforward, often the cheapest thing available, and routinely forgotten by people in their early twenties who assume they aged out when they started working.</span>
      </div>
      <div class="vs-ih-card">
        <strong>5. An ICHRA, if you are going self-employed</strong>
        <span>If the next chapter is a business rather than a job, an ICHRA lets that business reimburse your individual premiums tax-free. It turns a personal expense into a business one. <a href="/ichra-florida-small-business">How ICHRA works &rarr;</a></span>
      </div>
      <div class="vs-ih-card">
        <strong>6. A short-term plan &mdash; last resort, and read this first</strong>
        <span>Cheap because of what it leaves out. Short-term plans are not required to cover pre-existing conditions or essential health benefits, and they can decline you. Reasonable for a genuinely healthy person bridging a few weeks to a known start date. A bad idea for anyone with a condition, a prescription or a pregnancy.</span>
      </div>
    </div>
    <p class="lede" style="margin-top:22px">There is a seventh that is not an alternative but is free money: <strong>you can pay COBRA premiums out of an HSA</strong>. Insurance premiums are normally not a qualified HSA expense, but continuation coverage is one of the written exceptions, and so is coverage while you are collecting unemployment. If you have a funded HSA from the old plan, that balance is available tax-free either way.</p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>The clock, and why it is longer than it looks</h2>
    <p class="lede">The election notice reads like a demand. It is closer to an option you hold.</p>
    <div class="vs-ih-scroll">
    <table class="vs-ih-tbl">
      <thead><tr><th>Step</th><th>Deadline</th><th>What it means for you</th></tr></thead>
      <tbody>
        <tr><td>Employer notifies the plan</td><td>30 days from the qualifying event</td><td rowspan="2">If your employer is also the plan administrator, the notice can legally take up to <strong>44 days</strong> to reach you. It is not lost.</td></tr>
        <tr><td>Plan sends your election notice</td><td>14 days after that</td></tr>
        <tr><td><strong>You elect</strong></td><td><strong>At least 60 days</strong>, from the later of the notice date or the date coverage ended</td><td>This is your decision window, and it is yours to use.</td></tr>
        <tr><td>You make the first payment</td><td>At least 45 days after electing</td><td>Electing and paying are separate acts. In practice the two windows stack.</td></tr>
        <tr><td>Later payments</td><td>30-day grace period each</td><td>Missing one ends the coverage.</td></tr>
      </tbody>
    </table>
    </div>
    <div class="vs-ih-key">
      <strong>If you have not responded yet, COBRA is retroactive &mdash; and that is the part worth understanding.</strong>
      <p>Elect on day 55 and coverage is backdated to the day you lost it. You pay the back premiums, but nothing that happened in between falls into a gap. In effect you can shop for the full 60 days holding COBRA in reserve, and only pay for it if you need it.</p>
      <p><strong>One condition.</strong> That works if you have simply not replied. If you sign and return a waiver and then change your mind, the plan is not required to backdate at all &mdash; coverage can start from the day you revoked the waiver, leaving anything treated in between uninsured. So do not sign a waiver to tidy up your paperwork. Just do not reply until you have decided.</p>
    </div>
    <p class="lede">And your marketplace special enrollment period runs alongside it. Losing job-based coverage gives you 60 days, and it opens up to 60 days <em>before</em> the loss &mdash; so if you have a termination date on the calendar, you can line up a replacement policy before your last day rather than after it.</p>
  </div>
</section>

<section class="vs-ih" style="background:#fff6f4;border-top:1px solid #f4d9d2">
  <div class="vs-ih-inner">
    <h2>Before you cancel anything, read this</h2>
    <div class="vs-ih-key" style="background:#fff;border-color:#f0cfc6;border-left-color:#c0442a">
      <strong>Voluntarily cancelling COBRA mid-year does not open a special enrollment period. It leaves you uninsured until January.</strong>
      <p>This is the single most expensive mistake in this whole subject, and most of the pages ranking above us either bury it or leave it out. Federal rule 45 CFR 155.420(e)(1) excludes stopping COBRA payments from what counts as a loss of coverage. HealthCare.gov puts it plainly: &ldquo;Voluntarily dropping COBRA doesn&rsquo;t count.&rdquo;</p>
      <p><strong>What does work, three ways:</strong></p>
      <p>&bull; You are still inside the original <strong>60 days</strong> from losing your job-based coverage. Switch now and there is no problem at all.<br>
      &bull; It is <strong>annual open enrollment</strong>. You may drop COBRA for a marketplace plan for any reason, no justification needed.<br>
      &bull; Your COBRA has <strong>run out</strong> at the end of its full 18 or 36 months. Exhaustion is a qualifying event and opens a fresh 60-day window. Running out is not the same as quitting.</p>
      <p>There is one narrow extra: if your former employer stops contributing to your COBRA premium, or a government COBRA subsidy ends, that does count as a qualifying event.</p>
    </div>
    <p class="lede">The practical rule is simply this: <strong>never cancel anything until the replacement policy is confirmed active.</strong> Get the new effective date in writing, then stop the old coverage. That order costs nothing and it is the whole ballgame.</p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Four things to check before you switch</h2>
    <p class="lede">Not reasons to keep COBRA &mdash; reasons to do the arithmetic properly first, so you are not switching into something worse.</p>
    <div class="vs-ih-grid">
      <div class="vs-ih-card">
        <strong>Have you already met your deductible?</strong>
        <span>A new plan restarts it at zero. If it is September and you have satisfied a $3,000 deductible, switching can cost more in out-of-pocket exposure than it saves in premium. Average marketplace deductibles rose to $3,786 for 2026, so this matters more than it used to.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Are you mid-treatment, or is anyone pregnant?</strong>
        <span>Surgery scheduled, a course of treatment underway, an active specialist relationship. Check your doctors and hospital by name in the new plan's own directory, not the carrier's marketing page. Continuity is sometimes worth paying for.</span>
      </div>
      <div class="vs-ih-card">
        <strong>What is your projected income for the year?</strong>
        <span>Subsidies are calculated on projected annual income, and premium tax credits now phase out entirely above 400 percent of the federal poverty level &mdash; the enhanced subsidies expired at the end of 2025. A high year-to-date salary before a mid-year layoff can put you above it. Worth checking before you assume a subsidy is coming.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Are you at or near 65?</strong>
        <span>The real trap. COBRA does not count as active employer coverage for Medicare, so your 8-month Part B window runs from when your <em>employment</em> ended, not when COBRA ends. Take 18 months of COBRA and you have missed it by ten &mdash; and the Part B late penalty is permanent.</span>
      </div>
    </div>
    <p class="lede" style="margin-top:22px">All four take one conversation to settle. That is the conversation we have for free.</p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Run your own numbers</h2>
    <div class="vs-ih-grid">
      <a class="vs-ih-card" href="/cobra-vs-marketplace-calculator">
        <strong>COBRA vs marketplace calculator</strong>
        <span>Put your COBRA premium next to a subsidised marketplace plan and see the monthly gap, the yearly gap, and how many days you have left to decide.</span>
        <em>Open the calculator &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/aca-subsidy-calculator">
        <strong>Subsidy calculator</strong>
        <span>Estimate your premium tax credit from household size and projected income. This is the number that decides whether the marketplace beats COBRA for you.</span>
        <em>Check your subsidy &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/special-enrollment-period-checker">
        <strong>Special enrollment period checker</strong>
        <span>Confirm you qualify to enroll outside open enrollment and how many days are left on the clock.</span>
        <em>Check your window &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/health-insurance-between-jobs">
        <strong>Coverage between jobs</strong>
        <span>The wider picture when there is a gap to bridge, including what to do if the next job's benefits do not start on day one.</span>
        <em>Read the guide &rarr;</em>
      </a>
    </div>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Frequently asked</h2>__FAQ__
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Related reading</h2>
    <div class="vs-ih-grid">
      <a class="vs-ih-card" href="/blog/why-is-cobra-so-expensive"><strong>Why is COBRA so expensive?</strong><span>Where the number comes from, what the 2 percent is, and the four cases where the price is even higher than you were quoted.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-ih-card" href="/blog/cobra-60-day-loophole"><strong>The COBRA 60-day loophole</strong><span>Why not replying is a strategy, how retroactive coverage actually works, and the waiver that quietly destroys it.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-ih-card" href="/blog/can-i-drop-cobra-for-marketplace"><strong>Can I drop COBRA and switch?</strong><span>The three windows where you can, the rest of the year when you cannot, and what the regulation actually says.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-ih-card" href="/blog/lost-health-insurance-job-loss-options"><strong>Just lost your coverage?</strong><span>The full set of options after a job loss, in the order to work through them.</span><em>Read the guide &rarr;</em></a>
    </div>
  </div>
</section>

<section class="vs-ih-band">
  <div class="vs-ih-inner">
    <h2>Send us your COBRA number and we will beat it or tell you we can&rsquo;t</h2>
    <p>Your monthly COBRA quote, your ZIP code, ages, and roughly what you expect to earn this year. We come back with what the same household actually pays on the marketplace after any subsidy, whether your doctors are in it, and how many days you have left. If COBRA is genuinely the better deal for you, we will say so &mdash; you are not our only call today. Free either way, because carriers pay our commission.</p>
    <p style="margin:0"><a class="vs-ih-cta" href="/quote?type=individual" style="background:#fff;color:#0b2346">Compare against my COBRA quote &rarr;</a></p>
  </div>
</section>

'''

build('cobra-alternatives.html', URL, TITLE, DESC, 'US-FL', 'Miami', BODY, FAQ, SCHEMA)

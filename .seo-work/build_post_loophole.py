# -*- coding: utf-8 -*-
"""The COBRA 60-day loophole. Strong existing hook in the SERP (WHIA owns it with
a 5,200-word page) but their guide never warns that cancelling COBRA mid-year
strands you. This one does, and adds the waiver trap they omit."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

FAQ = [
 ("What is the COBRA 60-day loophole?",
  "It is not really a loophole, it is how the election period is designed. You have at least 60 days to elect COBRA, and if you elect, coverage is backdated to the day you lost it. So you can wait, shop, and only elect if something happens that you need covered. In effect the 60 days are free optional coverage - you hold the right to buy it retroactively, and you only pay if you use it."),
 ("Is COBRA really retroactive?",
  "Yes, if you have simply not responded. Treasury regulation 26 CFR 54.4980B-6 says that where an election is made during the election period, coverage must be provided from the date coverage would otherwise have been lost. You pay the back premiums for those months, but nothing falls into a gap."),
 ("Does the loophole still work if I already sent back a waiver?",
  "Not fully, and this is what most guides leave out. You may revoke a waiver any time before the election period ends, but the same regulation says that where a waiver is later revoked, coverage need not be provided retroactively - it can start from the date you revoked. So anything treated between the waiver and the reversal may not be covered. The rule is simple: do not sign a waiver to tidy up your paperwork. Just do not reply until you have decided."),
 ("How long do I actually have?",
  "At least 60 days from the later of the date your election notice was provided or the date you would otherwise lose coverage. Before that clock even starts, your employer has 30 days to notify the plan and the plan has 14 days to send the notice - so if your employer is also the plan administrator, the notice can legally take 44 days to arrive. After you elect, you get at least 45 more days to make the first payment."),
 ("Can I use the 60 days and then take a marketplace plan instead?",
  "Yes, and that is the best use of the window. Losing job-based coverage opens a 60-day marketplace special enrollment period that runs alongside your COBRA election period, and it can start up to 60 days before the loss. So you can shop the marketplace with COBRA held in reserve, and elect COBRA retroactively only if you need care before the new plan starts."),
 ("What happens if I miss the 60-day deadline?",
  "COBRA is gone, and it does not come back. Your marketplace special enrollment period is running on a similar clock, so if both lapse you are waiting for open enrollment. Medicaid is the exception - it has no enrollment window and can be applied for any day of the year, and eligibility is assessed on current monthly income, which after a job loss may look very different from your annual figure."),
]

TOC = [("what", "What the Loophole Is"), ("how", "How Retroactive Works"),
       ("clock", "The Real Clock"), ("waiver", "The Waiver Trap"),
       ("use", "How to Use It"), ("after", "After the 60 Days"), ("faq", "FAQ")]

BODY = '''<h2 id="what">The 60-day window is an option, not a deadline</h2>
      <p>A COBRA election notice reads like a bill with a due date. It is closer to a call option: you hold the right to buy the coverage, backdated, for 60 days, and you only pay if you exercise it.</p>
      <p>That is what people mean by the "60-day loophole." It is not a trick and nobody is being outsmarted — it is simply how the election period is built, and most people never realise it because the notice does not explain it.</p>
      <div class="highlight-box">
        <h4>The mechanic in one sentence</h4>
        <p>You have at least <strong>60 days to elect</strong>, and if you elect, coverage is <strong>backdated to the day you lost it</strong> — so you can spend the whole window shopping, uninsured on paper but covered in practice, and only pay COBRA's back premiums if something happens that you need covered.</p>
      </div>
      <p>For a healthy person bridging a gap to a new job, that is genuinely valuable. Break your wrist on day 40 and you elect COBRA, pay two months of back premiums, and the emergency room visit is covered. Nothing happens and you never elect, and it cost you nothing at all.</p>

      <h2 id="how">How the retroactivity actually works</h2>
      <p>The authority is Treasury regulation 26 CFR 54.4980B-6. Where an election is made during the election period, coverage "must be provided from the date that coverage would otherwise have been lost." Not from the date you elected — from the date you lost it.</p>
      <p>You do pay for those months. Electing on day 55 means writing a cheque covering the period back to your last day of coverage. But there is no gap in the record, no pre-existing condition question, and no uninsured window.</p>
      <p>And the payment clock is separate from the election clock. After you elect, the plan must give you <strong>at least 45 more days</strong> to make that first payment. In practice the two windows stack, which is why people talk about having "over three months."</p>

      <h2 id="clock">The real clock, start to finish</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>Stage</th><th>Legal deadline</th><th>What it means</th></tr></thead>
        <tbody>
          <tr><td>Employer notifies the plan</td><td>30 days from the qualifying event</td><td rowspan="2">Where the employer <em>is</em> the plan administrator, the notice can take <strong>44 days</strong> to reach you. It is not lost — the clock has not started.</td></tr>
          <tr><td>Plan sends the election notice</td><td>14 days after being notified</td></tr>
          <tr><td><strong>Your election period</strong></td><td><strong>At least 60 days</strong> from the later of the notice date or the coverage-loss date</td><td>The window. It runs from the <em>later</em> of the two dates, which usually helps you.</td></tr>
          <tr><td>First premium payment</td><td>At least 45 days after you elect</td><td>Separate clock. Electing does not mean paying that week.</td></tr>
          <tr><td>Every payment after</td><td>30-day grace period</td><td>Miss one and the coverage ends.</td></tr>
        </tbody>
      </table>
      </div>
      <p>Two exceptions to know. If the qualifying event was a <strong>divorce, legal separation, or a child ageing off the plan</strong>, the employer does not notify anyone — <em>you</em> have to, within 60 days, or there is no COBRA to elect. And federal COBRA only applies to employers with <strong>20 or more employees</strong>; below that, state continuation rules apply and the timelines differ.</p>

      <h2 id="waiver">The waiver trap that breaks the whole thing</h2>
      <p>This is the part the long guides ranking for this phrase leave out, and it is the one that actually costs people money.</p>
      <div class="highlight-box">
        <h4>Do not sign the waiver</h4>
        <p>You may revoke a waiver any time before the election period ends — the Department of Labor is explicit about that. But 26 CFR 54.4980B-6 also says that where "a waiver of COBRA continuation coverage is later revoked, coverage need not be provided retroactively." It can start from the date you revoked, and not a day earlier.</p>
        <p>So signing and returning the waiver, then changing your mind on day 50, can leave you with an uninsured gap covering everything that happened in between. The retroactivity you were counting on is gone.</p>
      </div>
      <p>The fix costs nothing: <strong>just do not reply.</strong> Not replying preserves the full retroactive election. Replying with a declination does not. People sign the waiver because the packet came with a form and returning forms feels responsible, and it is the single most avoidable mistake in this whole process.</p>

      <h2 id="use">How to actually use the window</h2>
      <ol>
        <li><strong>Put two dates in your calendar the day the notice arrives.</strong> Day 60 of your COBRA election period, and day 60 of your marketplace special enrollment period. They are different clocks and they do not necessarily end together.</li>
        <li><strong>Do not sign anything.</strong> File the packet. Do not return the waiver.</li>
        <li><strong>Shop the marketplace immediately.</strong> Your special enrollment period from losing job-based coverage runs alongside, and it opens up to <strong>60 days before</strong> the loss — so if you know your termination date, you can have a replacement policy effective the day the old one ends.</li>
        <li><strong>Check a spouse's plan in the same week.</strong> Your loss of coverage opens a window on their employer's plan too, and it is often the cheapest option on the table.</li>
        <li><strong>If something medical happens before the new plan starts, elect COBRA.</strong> That is what the option was for. Elect, pay the back premiums, get the care covered.</li>
        <li><strong>Never cancel one thing before the other is confirmed active.</strong> Get the new effective date in writing first.</li>
      </ol>
      <p>Worth knowing while you are in the window: if you have a funded HSA from the old plan, COBRA premiums are one of the few insurance premiums you can pay from it tax-free. So can premiums during a period when you are collecting unemployment.</p>

      <div class="cta-block">
        <h3>Use the 60 days properly</h3>
        <p>Send us your COBRA quote, ZIP code, ages and rough expected income for the year. We will tell you what the marketplace costs you after any subsidy, whether your doctors are in it, and exactly how many days are left on both clocks. Free — carriers pay our commission either way.</p>
        <a class="btn btn-teal" href="/quote?type=individual" style="background:#fff;color:var(--blue-700)">Compare my options &rarr;</a>
      </div>

      <h2 id="after">What happens when the 60 days close</h2>
      <p>The option expires and does not return. If you let both the COBRA election period and the marketplace special enrollment period lapse, you are generally waiting for annual open enrollment.</p>
      <p>Two things still work after that. <strong>Medicaid has no enrollment window</strong> — you can apply any day, and eligibility is assessed on current monthly income, which after a layoff often looks nothing like your annual number. And <strong>a new job's coverage</strong> is its own qualifying event.</p>
      <p>The other thing to understand before you elect: once you are <em>on</em> COBRA, the flexibility ends. Voluntarily cancelling it mid-year is not a qualifying event and does not open a special enrollment period. You can switch during open enrollment, or when COBRA exhausts at the end of its full term, and otherwise you are on it until January. <a href="/blog/can-i-drop-cobra-for-marketplace">The full rule &rarr;</a></p>
      <p>Which is the real argument for using the 60 days to shop properly rather than electing on day two and sorting it out later. Electing is easy. Leaving is not.</p>

      <h2 id="faq">Frequently asked</h2>
      <h3>Do I have to pay for the 60 days if I never elect?</h3>
      <p>No. If you do not elect, you owe nothing. That is the whole point of the window.</p>
      <h3>Can my spouse or child elect COBRA if I do not?</h3>
      <p>Yes. Each qualified beneficiary has an independent right to elect. A family can put one person on COBRA — the one mid-treatment, say — and everyone else on a cheaper marketplace plan. This is under-used and can save a great deal.</p>
      <h3>Does electing COBRA burn my marketplace special enrollment period?</h3>
      <p>No. HealthCare.gov lists "it&rsquo;s still within 60 days of when you lost your job-based coverage" as a circumstance in which you may switch from COBRA to a marketplace plan. Electing does not spend the window; running out the clock does.</p>
      <p class="vs-src">Sources: <a href="https://www.ecfr.gov/current/title-26/chapter-I/subchapter-D/part-54/section-54.4980B-6" rel="nofollow noopener" target="_blank">26 CFR 54.4980B-6</a> &middot; <a href="https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/an-employees-guide-health-benefits-under-cobra-2022.pdf" rel="nofollow noopener" target="_blank">DOL, An Employee&rsquo;s Guide to Health Benefits Under COBRA</a> &middot; <a href="https://www.healthcare.gov/unemployed/cobra-coverage/" rel="nofollow noopener" target="_blank">HealthCare.gov, COBRA coverage when unemployed</a> &middot; <a href="https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-B/part-155/subpart-E/section-155.420" rel="nofollow noopener" target="_blank">45 CFR 155.420</a></p>'''

build(slug='cobra-60-day-loophole',
      title='The COBRA 60-Day Loophole, Explained',
      h1='The COBRA 60-Day Loophole: Why Not Replying Is a Strategy',
      desc='You have 60 days to elect COBRA and it backdates to the day you lost coverage. Free optional insurance &mdash; unless you sign the waiver.',
      lede='A COBRA notice reads like a bill with a due date. It is closer to an option you hold for 60 days, exercisable retroactively. Here is how it works, and the one form that destroys it.',
      published='2026-08-27', read_min=8, eyebrow='COBRA',
      img='/compressed/business-seminar.jpg',
      alt='Person holding a COBRA election notice and reviewing the 60-day election period deadline',
      toc=TOC, body=BODY, faq=FAQ,
      cta_head='Use the 60 days properly',
      cta_copy='We will tell you what is left on both clocks. Free.',
      cta_href='/quote?type=individual')

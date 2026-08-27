# -*- coding: utf-8 -*-
"""Can I drop COBRA and switch to a marketplace plan.
KFF and healthinsurance.org own the accurate answers here and commercial supply
is thin and often wrong. Of ten ranking pages checked, not one states both
branches of the rule as a decision, up front."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

FAQ = [
 ("Can I drop COBRA and switch to a marketplace plan?",
  "Only inside one of three windows. While you are still within 60 days of losing your job-based coverage. During annual open enrollment, for any reason. Or when COBRA runs out at the end of its full 18 or 36 month term, which opens a fresh 60-day special enrollment period. Outside those, voluntarily cancelling COBRA does not qualify you for anything and you would be uninsured until January."),
 ("Why doesn't cancelling COBRA count as losing coverage?",
  "Because the regulation says so explicitly. 45 CFR 155.420(e)(1) excludes from the definition of loss of coverage a failure to pay premiums on a timely basis, including COBRA premiums, before COBRA expires. HealthCare.gov states it plainly: voluntarily dropping COBRA does not count, and choosing to stop paying COBRA premiums on your own does not qualify. The logic is that you chose to end it, so it is not a loss."),
 ("What is the difference between exhausting COBRA and cancelling it?",
  "Exhausting means running out the full term - your 18 or 36 months came to an end. That is a qualifying event and opens a 60-day special enrollment period. Cancelling means you stopped it early, by choice or by not paying. That is not a qualifying event and opens nothing. Same outcome for your coverage, completely different consequence for your options."),
 ("Can I switch from COBRA during open enrollment?",
  "Yes, for any reason and with no justification needed. HealthCare.gov is explicit that during open enrollment you can enroll in a marketplace plan regardless of why you are ending COBRA coverage. Time the marketplace plan's effective date to line up with when you stop paying COBRA so there is no gap."),
 ("Does electing COBRA use up my special enrollment period?",
  "No. The 60 days run from when you lost your job-based coverage, not from any decision you make about COBRA. HealthCare.gov lists being within 60 days of losing job-based coverage as a circumstance in which you can switch from COBRA to a marketplace plan. So electing COBRA and then switching a few weeks later, inside that original window, is entirely allowed."),
 ("Are there any exceptions where dropping COBRA does qualify?",
  "Two narrow ones. If your former employer completely stops contributing toward your COBRA premium, or if a government subsidy of COBRA coverage completely ceases, that is treated as a loss of coverage and opens a special enrollment period. Both are carved out in 45 CFR 155.420. Neither covers the ordinary case of deciding it costs too much."),
]

TOC = [("answer", "The Short Answer"), ("three", "The Three Windows"),
       ("trap", "Why Cancelling Fails"), ("exhaust", "Exhausting vs Cancelling"),
       ("exceptions", "Two Exceptions"), ("order", "The Safe Order"), ("faq", "FAQ")]

BODY = '''<h2 id="answer">The short answer</h2>
      <p>Sometimes yes, mostly no, and the difference is worth about a year of your life if you get it wrong.</p>
      <p>You can move from COBRA to a marketplace plan in exactly three situations. Outside them, cancelling COBRA does not open any door — it just leaves you uninsured until January. That distinction is poorly covered even by pages that rank well for this question, and it is the reason people call us in June with no coverage and no options.</p>
      <div class="highlight-box">
        <h4>The rule, both halves</h4>
        <p><strong>Voluntarily dropping COBRA mid-year does not create a special enrollment period.</strong> But <strong>running out of COBRA at the end of its term does.</strong> Quitting and finishing are treated completely differently, even though your coverage ends the same way.</p>
      </div>

      <h2 id="three">The three windows where switching works</h2>
      <h3>1. You are still within 60 days of losing your job-based coverage</h3>
      <p>This is the clean one. Losing job-based coverage opens a 60-day marketplace special enrollment period, and electing COBRA does not spend it. HealthCare.gov lists, among the circumstances in which you may switch from COBRA to the marketplace, that "it's still within 60 days of when you lost your job-based coverage."</p>
      <p>So if you elected COBRA three weeks ago and have since seen a better marketplace number, you can switch. Under 45 CFR 155.420(c)(2) the window actually opens up to <strong>60 days before</strong> the loss as well, so someone with a known termination date can line the replacement up in advance.</p>
      <h3>2. It is annual open enrollment</h3>
      <p>No justification required. HealthCare.gov: during open enrollment "you can enroll in a Marketplace plan, regardless of why you're ending COBRA coverage." Enrol, get the effective date, then stop paying COBRA so the two line up without a gap. For most people stuck on expensive COBRA in, say, March, this is the answer — wait for open enrollment in the autumn.</p>
      <h3>3. Your COBRA has run out</h3>
      <p>Exhausting the full 18 or 36 months is a qualifying event and opens a fresh 60-day window. HealthCare.gov draws the line explicitly: a special enrollment period applies "when your COBRA coverage expires or is no longer available, not if you voluntarily cancel it before it ends."</p>
      <p>If you are within a couple of months of exhaustion, that is worth planning around rather than cancelling early and losing the right.</p>

      <h2 id="trap">Why cancelling fails</h2>
      <p>It is written into the regulation. 45 CFR 155.420(e)(1) says that for special enrollment purposes, loss of coverage does <em>not</em> include "failure to pay premiums on a timely basis, including COBRA continuation coverage premiums prior to expiration of COBRA continuation coverage."</p>
      <p>HealthCare.gov translates it without hedging: "Voluntarily dropping COBRA doesn't count. Choosing to stop paying COBRA premiums on your own doesn't qualify." And: "If you choose to end COBRA coverage early, you'll have to wait until next Open Enrollment to get Marketplace coverage (unless you experience another life event)."</p>
      <p>The reasoning is that a special enrollment period exists for things that happen <em>to</em> you. Deciding a premium is too expensive is a choice, however reasonable — so the door does not open.</p>
      <p>What that means in practice: cancel COBRA in April with nothing lined up, and you are uninsured for eight or nine months. Not on a worse plan. Uninsured.</p>

      <h2 id="exhaust">Exhausting versus cancelling, side by side</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>What happened</th><th>Special enrollment period?</th><th>What you can do</th></tr></thead>
        <tbody>
          <tr><td>You are within 60 days of losing job-based coverage</td><td><strong>Yes</strong></td><td>Switch to a marketplace plan now</td></tr>
          <tr><td>COBRA ran out at the end of its 18 or 36 months</td><td><strong>Yes</strong> — 60 days</td><td>Switch to a marketplace plan</td></tr>
          <tr><td>Your employer stopped contributing to your COBRA premium</td><td><strong>Yes</strong></td><td>Switch to a marketplace plan</td></tr>
          <tr><td>It is annual open enrollment</td><td>Not needed</td><td>Switch for any reason at all</td></tr>
          <tr><td>You cancelled COBRA because it was too expensive</td><td><strong>No</strong></td><td>Wait for open enrollment</td></tr>
          <tr><td>You stopped paying and it lapsed</td><td><strong>No</strong></td><td>Wait for open enrollment</td></tr>
        </tbody>
      </table>
      </div>
      <p>Rows two and five end with the same thing — no COBRA — and are treated as opposites. That is the entire point.</p>

      <h2 id="exceptions">Two exceptions worth knowing</h2>
      <p>45 CFR 155.420 carves out two situations where losing COBRA <em>does</em> qualify even though you did not exhaust it:</p>
      <ul>
        <li><strong>Your former employer completely stops contributing</strong> toward the COBRA premium. Some employers subsidise COBRA as part of a severance package for a few months; when that ends, the resulting loss is a qualifying event.</li>
        <li><strong>A government subsidy of COBRA coverage completely ceases.</strong> This was the mechanism used when federal COBRA subsidies ended in 2021.</li>
      </ul>
      <p>If either applies to you, say so when you apply — it is easy to be assessed as an ordinary voluntary cancellation when you are not one.</p>

      <h2 id="order">The safe order of operations</h2>
      <p>Whatever your situation, the sequence is the same and it costs nothing to follow:</p>
      <ol>
        <li><strong>Work out which window you are in</strong> before you do anything. Within 60 days of the original loss? Approaching exhaustion? Coming up to open enrollment? Or none of the above?</li>
        <li><strong>Apply for the replacement first.</strong> Do not cancel, then shop.</li>
        <li><strong>Get the effective date in writing.</strong> An application is not coverage.</li>
        <li><strong>Only then stop paying COBRA</strong>, timed so the new plan starts as the old one ends.</li>
      </ol>
      <p>If you are in none of the three windows and COBRA is genuinely unaffordable, two things still work regardless of the calendar. <strong>Medicaid has no enrollment window</strong> — you can apply any day and eligibility is assessed on current monthly income, which after a job loss often looks very different from your annual figure. And <strong>a spouse's employer plan</strong> may have its own window open.</p>
      <p>Also worth knowing before you decide it is unaffordable: <strong>COBRA premiums can be paid tax-free from an HSA</strong>. Insurance premiums usually cannot be, but continuation coverage is a written exception, as is coverage while you are receiving unemployment.</p>

      <div class="cta-block">
        <h3>Not sure which window you are in?</h3>
        <p>Tell us the date you lost coverage, whether you elected COBRA, and what it costs. We will tell you exactly which options are open to you today, what the marketplace would cost after any subsidy, and how many days are left. Free — carriers pay our commission either way.</p>
        <a class="btn btn-teal" href="/quote?type=individual" style="background:#fff;color:var(--blue-700)">Check my options &rarr;</a>
      </div>

      <h2 id="faq">Frequently asked</h2>
      <h3>Can I drop COBRA for just one family member?</h3>
      <p>Yes. Each qualified beneficiary has an independent right to elect and to end COBRA. A family can keep one person on COBRA — the one mid-treatment — and move everyone else to a cheaper plan, provided the movers are in a valid enrollment window.</p>
      <h3>What if I get a new job with benefits?</h3>
      <p>That is its own qualifying event and you can drop COBRA for the new employer's plan. Watch the start date: if the new coverage begins the first of the month after 30 days, you may need COBRA for those weeks. Elect and pay only for the months you need.</p>
      <h3>Will I owe anything if I switch mid-month?</h3>
      <p>COBRA is generally billed monthly and is not usually prorated, so you will typically pay for the whole final month. Time the switch to a month boundary where you can.</p>
      <h3>Does this apply to state continuation coverage too?</h3>
      <p>The federal special enrollment rules key off loss of minimum essential coverage, and state continuation counts. But state mini-COBRA terms vary — different durations and different rules for employers under 20 employees — so confirm your own state's before planning around a date.</p>
      <p class="vs-src">Sources: <a href="https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-B/part-155/subpart-E/section-155.420" rel="nofollow noopener" target="_blank">45 CFR 155.420</a> &middot; <a href="https://www.healthcare.gov/unemployed/cobra-coverage/" rel="nofollow noopener" target="_blank">HealthCare.gov, COBRA coverage when unemployed</a> &middot; <a href="https://www.healthcare.gov/coverage-outside-open-enrollment/special-enrollment-period/" rel="nofollow noopener" target="_blank">HealthCare.gov, special enrollment periods</a> &middot; <a href="https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/an-employees-guide-health-benefits-under-cobra-2022.pdf" rel="nofollow noopener" target="_blank">DOL, An Employee&rsquo;s Guide to Health Benefits Under COBRA</a></p>'''

build(slug='can-i-drop-cobra-for-marketplace',
      title='Can I Drop COBRA and Switch to a Marketplace Plan?',
      h1='Can I Drop COBRA and Switch to a Marketplace Plan? Three Windows, and the Rest of the Year',
      desc='Cancelling COBRA mid-year does not open a special enrollment period. Running out of it does. Here is exactly when you can switch.',
      lede='Cancelling COBRA because it is too expensive leaves you uninsured until January. Letting it run out does not. Same ending, opposite consequences &mdash; here is the rule and the three windows where switching works.',
      published='2026-08-27', read_min=8, eyebrow='COBRA',
      img='/compressed/servicesmeeting.jpg',
      alt='Person comparing COBRA continuation coverage against a marketplace plan before switching',
      toc=TOC, body=BODY, faq=FAQ,
      cta_head='Which window are you in?',
      cta_copy='Tell us the date you lost coverage. We will tell you free.',
      cta_href='/quote?type=individual')

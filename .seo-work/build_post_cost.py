# -*- coding: utf-8 -*-
"""What small business health insurance actually costs - and why every
'average by state' figure you will find is close to meaningless."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

FAQ = [
 ("What is the average cost of small business health insurance?",
  "The only trustworthy national benchmark comes from AHRQ's Medical Expenditure Panel Survey. For 2024, at private firms with fewer than 50 employees, the average annual premium was $8,215 for single coverage and $23,170 for family coverage. Employees contributed an average of $1,755 single and $7,984 family, leaving the employer paying roughly $6,460 and $15,186 respectively. Those are national figures, not state figures."),
 ("Why can't you tell me the average premium in my state?",
  "Because there is no reliable published figure, and the ones circulating online are mostly invented. Premiums are set by geographic rating area within a state, not by the state, and the spread inside a single state can be very wide. Texas has 27 rating areas, Kentucky 8, Maryland 4, and Florida rates by county. A state average blends all of them into a number that describes no actual employer."),
 ("What actually determines what I pay?",
  "Five things, and only five. Whether the coverage is individual or family, your geographic rating area, the ages of your employees within a 3 to 1 band, tobacco use within a 1.5 to 1 band, and the plan you select. Federal rule 45 CFR 147.102 says rates must not vary by any other factor. Your industry, your claims history and your employees' health are not permitted rating factors for a group of 50 or fewer."),
 ("How much did small group rates go up for 2026 and 2027?",
  "It varies enormously by state. Maryland approved an average small group increase of 4.9 percent for 2026, below the 5.5 percent carriers requested. Kentucky's small group filings averaged roughly 14 percent for 2026, with about 10.7 percent requested for 2027. The individual market moved far more sharply than small group in both years."),
 ("How much of the premium does an employer have to pay?",
  "There is no state minimum in Texas or Maryland, and carriers generally set their own requirement at around 50 percent of the employee-only premium. Paying at least 50 percent of employee-only coverage is separately a condition of the federal small business tax credit. Nationally, employers at firms under 50 employees covered about 79 percent of single premiums and 66 percent of family premiums in 2024."),
]

TOC = [("benchmark", "The Only Honest Benchmark"), ("state-average", "Why State Averages Lie"),
       ("rating-areas", "Rating Areas by State"), ("trend", "What's Moving in 2026-27"),
       ("drivers", "What Drives Your Number"), ("offer", "The Hiring Argument"), ("faq", "FAQ")]

BODY = '''<h2 id="benchmark">The only benchmark worth quoting</h2>
      <p>Search for what small business health insurance costs and you will find dozens of confident per-employee figures. Almost none of them cite a source, because there is only one credible one: the federal Medical Expenditure Panel Survey Insurance Component, run by AHRQ. Here is what it says for 2024, at private firms with fewer than 50 employees:</p>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>Annual premium, firms under 50 employees</th><th>Single</th><th>Family</th></tr></thead>
        <tbody>
          <tr><td>Total premium</td><td><strong>$8,215</strong></td><td><strong>$23,170</strong></td></tr>
          <tr><td>Average employee contribution</td><td>$1,755</td><td>$7,984</td></tr>
          <tr><td>Implied employer share</td><td>$6,460 (79%)</td><td>$15,186 (66%)</td></tr>
        </tbody>
      </table>
      </div>
      <p class="vs-src">Source: <a href="https://meps.ahrq.gov/data_files/publications/rf54/rf54.shtml" rel="nofollow noopener" target="_blank">AHRQ MEPS-IC Research Findings #54</a>, national figures for 2024. Not state-specific.</p>
      <p>Per employee per month that is roughly $685 single and $1,930 family in total premium, with the employer carrying about $538 and $1,266 of it. Use those as a sanity check on any quote you are given, not as a prediction of your own number.</p>

      <h2 id="state-average">Why an &ldquo;average premium in Texas&rdquo; is close to meaningless</h2>
      <p>Because premiums are not set by state. They are set by <strong>geographic rating area</strong> inside a state, and the areas can differ from one another by a great deal.</p>
      <p>We will not publish a state average because we cannot source one, and inventing one would be the same thing every competitor page does. What we can tell you is how fragmented each state is, which is the actual reason a state number would not help you:</p>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>State</th><th>Rating areas</th><th>What that means</th></tr></thead>
        <tbody>
          <tr><td><strong>Texas</strong></td><td><strong>27</strong></td><td>Among the most fragmented in the country. Dallas and Fort Worth are two separate areas; McAllen and Brownsville are two more. Since 2023 there is no separate rural area &mdash; rural counties were folded into adjacent metro areas.</td></tr>
          <tr><td><strong>Kentucky</strong></td><td>8</td><td>By county. Northern Kentucky is its own six-county area; Bowling Green sits inside a twenty-county Southern Kentucky area.</td></tr>
          <tr><td><strong>Maryland</strong></td><td>4</td><td>Least fragmented of the four. Frederick and Carroll are in Western Maryland, not the DC-suburb area &mdash; a common and expensive assumption.</td></tr>
          <tr><td><strong>Florida</strong></td><td>County-based</td><td>The spread between the cheapest and most expensive Florida county runs wide for comparable coverage. Miami-Dade sits at the high end; Hillsborough is mid-range.</td></tr>
        </tbody>
      </table>
      </div>
      <p>A single employer with two offices can therefore be quoted two different per-employee costs for identical coverage. That is not a broker mistake; it is how the rating works.</p>

      <h2 id="rating-areas">The five things that are allowed to move your price</h2>
      <p>Federal rule 45 CFR 147.102 permits small group premiums to vary by exactly four factors, plus the plan you choose:</p>
      <ol>
        <li>Whether the coverage is for an individual or a family</li>
        <li>Geographic rating area</li>
        <li>Age, within a 3 to 1 band for adults, using the federal standard age curve unless a state sets its own</li>
        <li>Tobacco use, within a 1.5 to 1 band &mdash; though Kentucky caps it at 1.4 to 1, no Maryland carrier applies one at all, and Texas forbids charging it to an individual employee</li>
        <li>The metal level and plan design you select</li>
      </ol>
      <p>And then the rule closes the list: premiums &ldquo;must not vary with respect to the particular plan or coverage involved by any other factor.&rdquo;</p>
      <div class="highlight-box">
        <h4>Your industry does not raise your health premium</h4>
        <p>Industry classification, injury rate and prior claims experience are not permitted rating factors for a group of 50 or fewer. Owners in construction, trucking, manufacturing and oilfield services routinely assume group health is priced the way workers' compensation is &mdash; class code, experience mod, loss history &mdash; and never ask for a quote. It is not, and that assumption costs real money. <a href="/group-health-insurance-by-industry">Group health by trade &rarr;</a></p>
      </div>

      <h2 id="trend">What is actually moving in 2026 and 2027</h2>
      <p>Small group and individual coverage have moved very differently since the enhanced federal premium subsidies expired at the end of 2025, and conflating them is the biggest single error in most cost content right now.</p>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>Market</th><th>2026</th><th>2027</th></tr></thead>
        <tbody>
          <tr><td>Maryland small group</td><td><strong>+4.9%</strong> approved, market average (5.5% requested)</td><td>&mdash;</td></tr>
          <tr><td>Kentucky small group</td><td>~14% average across filings</td><td>~10.7% requested</td></tr>
          <tr><td>ACA individual market, national</td><td>~20% finalised</td><td>~15% median proposed across 276 insurers</td></tr>
        </tbody>
      </table>
      </div>
      <p>The individual market took the harder hit because the enhanced premium tax credits lapsed. KFF found the average marketplace deductible rose 37 percent for 2026, from $2,759 to $3,786, and the average net premium actually paid rose 58 percent from $113 to $178 a month.</p>
      <p>The practical consequence for an employer: the &ldquo;just send everyone to the exchange&rdquo; argument that worked in 2021 through 2025 is much weaker now. <a href="/blog/ichra-vs-group-health-subsidy-cliff">We wrote that up in full &rarr;</a></p>

      <h2 id="drivers">What will actually determine your number</h2>
      <p>In rough order of how much they move it:</p>
      <ul>
        <li><strong>The ages of your team.</strong> The 3 to 1 age band is the largest single lever. A firm averaging 28 and a firm averaging 52 in the same office building pay very different rates for the same plan.</li>
        <li><strong>Family mix.</strong> Family premiums run close to three times single. A group where most people enrol dependents costs far more per head than one where most take employee-only, and per-member rating counts no more than the three oldest children under 21.</li>
        <li><strong>Your rating area.</strong> See above.</li>
        <li><strong>Metal level and deductible.</strong> The one thing entirely within your control.</li>
        <li><strong>Your contribution.</strong> Not a rating factor, but it decides how the total splits and it drives participation, which decides whether the plan is issuable at all.</li>
      </ul>
      <p>Five inputs get you a real quote: employee count, dates of birth, ZIP codes, who is enrolling dependents, and how much you intend to contribute. That is a fifteen-minute exercise, and it beats any average.</p>

      <h2 id="offer">The number that makes the case for offering at all</h2>
      <p>Nationally, only <strong>50.5 percent</strong> of employees at firms with fewer than 50 people work somewhere that offers health insurance, against <strong>97.4 percent</strong> at firms of 50 or more. Of those who are offered it, about 80 percent are eligible and two thirds of the eligible take it up.</p>
      <p>In other words, roughly half the small-employer jobs a candidate might take have no health benefit at all. In Texas the gap is starker still: 16.8 percent of Texans had no coverage in 2024 against 8.2 percent nationally, the highest uninsured rate of any state.</p>
      <p>That is the retention argument, and it is more concrete than most of what gets written about benefits and culture. If you offer, you are in the half of the market that does.</p>

      <div class="cta-block">
        <h3>Stop guessing at averages. Get your actual number.</h3>
        <p>Employee count, dates of birth and ZIP codes is enough. We come back with real quotes from every carrier writing in your rating area &mdash; not a range, your range. Free, and carriers pay our commission either way.</p>
        <a class="btn btn-teal" href="/quote?type=business" style="background:#fff;color:var(--blue-700)">Get group quotes &rarr;</a>
      </div>

      <h2 id="faq">Frequently asked</h2>
      <h3>Is level-funded cheaper?</h3>
      <p>Often, for a younger and healthier group, with a refund of unused claims at year end. But it is not universally cheaper and it is more tightly regulated in some states &mdash; Maryland sets minimum stop-loss attachment points of $22,500 specific and 120 percent aggregate for small employers, which rules out the aggressive designs marketed elsewhere. <a href="/level-funded-health-insurance-florida">Compare level-funded &rarr;</a></p>
      <h3>Does the plan have to start in January?</h3>
      <p>No. Group coverage is not tied to the ACA open enrollment calendar. A small business can start a plan in any month, and the effective date becomes its annual renewal point.</p>
      <h3>Will a broker cost me more?</h3>
      <p>No. Carrier commission is built into the premium whether you use a broker or go direct, so the rate is identical either way. Going direct saves you nothing and costs you the comparison.</p>
      <p class="vs-src">Sources: <a href="https://meps.ahrq.gov/data_files/publications/rf54/rf54.shtml" rel="nofollow noopener" target="_blank">AHRQ MEPS-IC Research Findings #54</a> &middot; <a href="https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-B/part-147/section-147.102" rel="nofollow noopener" target="_blank">45 CFR 147.102</a> &middot; <a href="https://insurance.maryland.gov/Documents/newscenter/newsreleases/2026-ACA-Press-Release-Approved-Rates-with-exhibits.pdf" rel="nofollow noopener" target="_blank">Maryland Insurance Administration, approved 2026 rates</a> &middot; <a href="https://www.healthsystemtracker.org/brief/how-much-and-why-aca-marketplace-premiums-are-going-up-in-2027/" rel="nofollow noopener" target="_blank">Peterson-KFF Health System Tracker</a> &middot; <a href="https://www.kff.org/uninsured/state-indicator/nonelderly-uninsured-rate-by-age/" rel="nofollow noopener" target="_blank">KFF State Health Facts</a></p>'''

build(slug='small-business-health-insurance-cost-2027',
      title='What Small Business Health Insurance Costs in 2027',
      h1='What Small Business Health Insurance Actually Costs &mdash; and Why Every State Average You Read Is Wrong',
      desc='The one national benchmark worth quoting, why per-state averages mislead, and the five things that actually set your premium.',
      lede='Most cost pages quote a per-employee figure with no source behind it. Here is the one national benchmark that holds up, and the reason a &ldquo;state average&rdquo; describes no real employer.',
      published='2026-08-26', read_min=9, eyebrow='Small Business',
      img='/compressed/health-insurance-cost-2026-woman.jpg',
      alt='Small business owner comparing group health insurance premium costs for 2027',
      toc=TOC, body=BODY, faq=FAQ,
      cta_head='Get your actual number',
      cta_copy='Headcount, dates of birth, ZIP codes. Real quotes, free.')

# -*- coding: utf-8 -*-
"""ICHRA vs group health now that the 400% FPL subsidy cliff is back.
The single most consequential change to the small-employer decision in years."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

FAQ = [
 ("Did the enhanced ACA subsidies expire?",
  "Yes. The enhanced premium tax credits expanded under the American Rescue Plan and extended by the Inflation Reduction Act lapsed at the end of 2025, and subsidies reverted to pre-ARPA levels on 1 January 2026. The clearest proof is in the IRS applicable percentage tables: Revenue Procedure 2025-25 for 2026 and Revenue Procedure 2026-26 for 2027 both use the pre-ARPA structure and both cut off entirely above 400 percent of the federal poverty level."),
 ("What is the 400 percent subsidy cliff?",
  "Under the pre-2021 rules, which are back in force, a household earning more than 400 percent of the federal poverty level receives no premium tax credit at all. Not a reduced one - none. Between 2021 and 2025 that cliff was replaced by a smooth cap at 8.5 percent of income, so higher earners still got help. That cap is gone."),
 ("Does the subsidy expiry make ICHRA a worse idea?",
  "For some employees, yes. The old argument that an employee is better off with a subsidised exchange plan than on your group plan now fails for anyone above 400 percent of the federal poverty level, because there is no subsidy for them to receive. For employees below the cliff, the calculus is largely unchanged. The honest answer is that ICHRA became more census-dependent rather than universally better or worse."),
 ("What is the employer affordability percentage for 2026 and 2027?",
  "9.96 percent of household income for plan years beginning in 2026, per IRS Revenue Procedure 2025-25, and 10.22 percent for 2027, per Revenue Procedure 2026-26. The figure rises each year, which means a given ICHRA contribution goes slightly further toward being considered affordable with each passing plan year."),
 ("Can an employee take both an ICHRA and a premium tax credit?",
  "No. If the ICHRA offer is affordable under the applicable percentage test, the employee is barred from the premium tax credit whether or not they accept the ICHRA. If the offer is unaffordable, the employee may opt out of the ICHRA and claim the credit instead. That choice is what the whole design turns on."),
 ("Does an ICHRA qualify for the small business health care tax credit?",
  "No. The credit requires a qualified health plan purchased through a SHOP marketplace, and an ICHRA reimburses individual coverage instead. If the credit is worth real money to your business, that is a genuine point in favour of a group plan."),
]

TOC = [("changed", "What Changed on 1 January"), ("proof", "The Proof, in Two IRS Tables"),
       ("math", "How It Broke the ICHRA Argument"), ("affordability", "The Affordability Test"),
       ("wins", "Where ICHRA Still Wins"), ("group-wins", "Where Group Wins Now"), ("faq", "FAQ")]

BODY = '''<h2 id="changed">What changed on 1 January 2026</h2>
      <p>The enhanced premium tax credits &mdash; expanded under the American Rescue Plan in 2021 and extended by the Inflation Reduction Act &mdash; expired at the end of 2025. Congress did not replace them. A three-year extension passed the House in January 2026 by 230 to 196 and was not enacted; an earlier Senate bill failed to reach 60 votes in December 2025.</p>
      <p>So on 1 January 2026, ACA subsidies reverted to the pre-2021 structure, and the piece that matters most to employers came back with them: <strong>the 400 percent subsidy cliff</strong>.</p>
      <div class="highlight-box">
        <h4>What the cliff means</h4>
        <p>A household above 400 percent of the federal poverty level now receives <strong>no</strong> premium tax credit. Not a smaller one &mdash; none at all. Between 2021 and 2025 that cliff had been replaced by a smooth cap at 8.5 percent of household income, so a higher-earning employee still received meaningful help. That cap is gone.</p>
      </div>
      <p>The market effects showed up immediately. KFF found the average marketplace deductible rose 37 percent for 2026, from $2,759 to $3,786 per person, and the average net premium actually paid rose 58 percent, from $113 to $178 a month. Enrolment was projected to fall from 22.3 million to around 17.5 million, and bronze plans went from 30 to 40 percent of selections as people traded coverage down.</p>

      <h2 id="proof">The proof, in two IRS tables</h2>
      <p>You do not have to take anyone's word for it. The IRS publishes the section 36B applicable percentage table each year, and both the 2026 and 2027 tables use the pre-ARPA structure with a hard stop at 400 percent:</p>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>Household income (% FPL)</th><th>2026 initial &rarr; final</th><th>2027 initial &rarr; final</th></tr></thead>
        <tbody>
          <tr><td>Less than 133%</td><td>2.10% &rarr; 2.10%</td><td>2.15% &rarr; 2.15%</td></tr>
          <tr><td>133% &ndash; under 150%</td><td>3.14% &rarr; 4.19%</td><td>3.23% &rarr; 4.30%</td></tr>
          <tr><td>150% &ndash; under 200%</td><td>4.19% &rarr; 6.60%</td><td>4.30% &rarr; 6.78%</td></tr>
          <tr><td>200% &ndash; under 250%</td><td>6.60% &rarr; 8.44%</td><td>6.78% &rarr; 8.66%</td></tr>
          <tr><td>250% &ndash; under 300%</td><td>8.44% &rarr; 9.96%</td><td>8.66% &rarr; 10.22%</td></tr>
          <tr><td>300% &ndash; 400%</td><td>9.96% &rarr; 9.96%</td><td>10.22% &rarr; 10.22%</td></tr>
          <tr><td><strong>Above 400%</strong></td><td><strong>No credit</strong></td><td><strong>No credit</strong></td></tr>
        </tbody>
      </table>
      </div>
      <p class="vs-src">Sources: <a href="https://www.irs.gov/pub/irs-drop/rp-25-25.pdf" rel="nofollow noopener" target="_blank">IRS Rev. Proc. 2025-25</a> (2026) and <a href="https://www.irs.gov/pub/irs-drop/rp-26-26.pdf" rel="nofollow noopener" target="_blank">Rev. Proc. 2026-26</a> (2027).</p>

      <h2 id="math">How this broke the standard ICHRA argument</h2>
      <p>For five years the pitch for an Individual Coverage HRA ran roughly like this: instead of buying a group plan, give employees a fixed tax-free allowance, send them to the exchange, and many of them will do better than they would on your plan because the subsidy picks up part of the cost. Your cost is capped and predictable. Everybody wins.</p>
      <p>That argument depended on the subsidy existing. For a meaningful share of a typical small-business census, it no longer does.</p>
      <p>Consider a fifteen-person company where five people are married with working spouses and household incomes above 400 percent of FPL. Under the 2021&ndash;2025 rules those five still received help capped at 8.5 percent of income. In 2026 and 2027 they receive nothing, and your ICHRA allowance is the <em>only</em> offset against a full-price individual premium &mdash; on a plan whose average deductible just rose by around a thousand dollars.</p>
      <p>Meanwhile the ten employees below the cliff are broadly where they were. The subsidy structure below 400 percent is essentially the pre-ARPA one, slightly less generous than 2021&ndash;2025 but intact.</p>
      <div class="highlight-box">
        <h4>The honest summary</h4>
        <p>ICHRA did not become a bad idea. It became <strong>much more census-dependent</strong>. Whether it beats a group plan for your business now turns on how many of your people sit above 400 percent of FPL &mdash; a question nobody was asking in 2023 and everybody should be asking now.</p>
      </div>

      <h2 id="affordability">The affordability test, and why it moves in your favour</h2>
      <p>The second half of the ICHRA design is the affordability test. If your ICHRA offer is affordable, the employee is barred from the premium tax credit whether or not they take the ICHRA. If it is unaffordable, they may opt out and claim the credit instead.</p>
      <p>Affordability is measured against the applicable percentage, which is <strong>9.96 percent for plan years beginning in 2026</strong> and <strong>10.22 percent for 2027</strong>. That figure has been rising, and the direction matters: a given ICHRA contribution counts as affordable at a higher share of income each year, so the same allowance goes slightly further toward triggering the bar.</p>
      <p>Combine the two and the picture is clear enough. Above 400 percent of FPL there is no credit to lose, so the affordability question is academic for those employees &mdash; the ICHRA allowance is simply money toward their premium. Below the cliff, the affordability calculation is the whole design decision, and it needs running against your actual census rather than a rule of thumb.</p>

      <h2 id="wins">Where ICHRA still clearly wins</h2>
      <ul>
        <li><strong>A mixed W-2 and 1099 workforce.</strong> Contractors cannot go on a group plan in any state. An ICHRA structure can reach them where a group plan structurally cannot &mdash; which is why it comes up so often in trucking, construction, real estate and delivery.</li>
        <li><strong>A group of one in Texas or Kentucky.</strong> Both states set a two-employee statutory floor for small group coverage, so a one-person business simply cannot buy a group plan there. An ICHRA from a related entity is the realistic route. <a href="/blog/how-many-employees-do-you-need-for-group-health-insurance">The employee minimums by state &rarr;</a></li>
        <li><strong>Teams spread across rating areas or states.</strong> A group plan prices off one rating area and one network. If you have people in Miami, Dallas, Baltimore and Louisville, an ICHRA lets each of them buy locally instead of being priced and networked off the head office.</li>
        <li><strong>A hard budget ceiling.</strong> Your cost is the allowance. There is no renewal increase to absorb, because the exposure is fixed by definition.</li>
        <li><strong>No participation requirement.</strong> If minimum participation is what stopped your group application, an ICHRA has none. <a href="/blog/group-health-insurance-minimum-participation">More on participation &rarr;</a></li>
      </ul>

      <h2 id="group-wins">Where a group plan now wins more often than it did</h2>
      <ul>
        <li><strong>A census concentrated above 400 percent of FPL.</strong> Professional services, engineering, medical and financial firms. There is no subsidy for these employees to collect, so pooled group pricing and an employer contribution beat a full-price individual premium in most modelling.</li>
        <li><strong>Where the small business tax credit is real money.</strong> An ICHRA cannot qualify &mdash; the credit requires a qualified health plan bought through SHOP. For a genuinely low-wage employer under ten FTEs, that is worth up to 50 percent of premiums for two years. <a href="/blog/small-business-health-care-tax-credit-2026">What the credit is worth &rarr;</a></li>
        <li><strong>Where individual-market deductibles are the problem.</strong> A group plan's cost sharing is chosen by you. An individual bronze plan's is not, and after a 37 percent average deductible rise the difference in what employees actually experience has widened.</li>
        <li><strong>Where employees want it decided for them.</strong> An ICHRA hands each employee a shopping task. Plenty of workforces experience that as a benefit cut regardless of the arithmetic.</li>
      </ul>

      <div class="cta-block">
        <h3>Have us model both against your actual census</h3>
        <p>Employee count, dates of birth, ZIP codes and rough household income bands is enough. We will show you the group quote and the ICHRA arithmetic side by side, including how many of your people now sit above the cliff. Free, and we have no incentive either way.</p>
        <a class="btn btn-teal" href="/quote?type=business" style="background:#fff;color:var(--blue-700)">Compare both &rarr;</a>
      </div>

      <h2 id="faq">Frequently asked</h2>
      <h3>Could the enhanced subsidies come back?</h3>
      <p>Possibly. Extension bills have moved through Congress without being enacted, and insurers filing 2027 rates are assuming continued expiration. Build your plan on the rules as they stand and treat any restoration as upside &mdash; not the other way round.</p>
      <h3>Can I offer an ICHRA to some employees and a group plan to others?</h3>
      <p>Yes, within limits. The rules allow different treatment across defined classes of employees &mdash; full-time versus part-time, salaried versus hourly, by worksite location &mdash; but you cannot offer the same class a choice between the two. The class rules are specific and worth getting right the first time.</p>
      <h3>Does an ICHRA satisfy the employer mandate?</h3>
      <p>It can, if the allowance is large enough to make coverage affordable under the applicable percentage. Below 50 full-time equivalents the mandate does not apply at all, which is most of the businesses we work with.</p>
      <p class="vs-src">Sources: <a href="https://www.irs.gov/pub/irs-drop/rp-25-25.pdf" rel="nofollow noopener" target="_blank">IRS Rev. Proc. 2025-25</a> &middot; <a href="https://www.irs.gov/pub/irs-drop/rp-26-26.pdf" rel="nofollow noopener" target="_blank">IRS Rev. Proc. 2026-26</a> &middot; <a href="https://www.kff.org/affordable-care-act/the-average-marketplace-deductible-grew-by-about-1000-per-person-in-2026-with-more-enrollees-shifting-to-higher-deductible-plans-as-enhanced-tax-credits-expired/" rel="nofollow noopener" target="_blank">KFF on 2026 deductibles and net premiums</a> &middot; <a href="https://www.healthsystemtracker.org/brief/how-much-and-why-aca-marketplace-premiums-are-going-up-in-2027/" rel="nofollow noopener" target="_blank">Peterson-KFF Health System Tracker, 2027 premiums</a></p>'''

build(slug='ichra-vs-group-health-subsidy-cliff',
      title='ICHRA vs Group Health After the Subsidy Cliff',
      h1='ICHRA vs Group Health Now That the 400% Subsidy Cliff Is Back',
      desc='The enhanced ACA subsidies expired at the end of 2025 and the 400% cliff returned. Here is exactly how that changes the ICHRA decision.',
      lede='For five years the ICHRA pitch rested on employees collecting an exchange subsidy. Above 400 percent of the federal poverty level, there is no longer a subsidy to collect. That changes the arithmetic, and not evenly.',
      published='2026-08-27', read_min=9, eyebrow='Small Business',
      img='/compressed/servicesmeeting.jpg',
      alt='Employer comparing ICHRA and group health insurance options after the ACA subsidy cliff returned',
      toc=TOC, body=BODY, faq=FAQ,
      cta_head='Model both against your census',
      cta_copy='Group quote and ICHRA arithmetic, side by side. Free.')

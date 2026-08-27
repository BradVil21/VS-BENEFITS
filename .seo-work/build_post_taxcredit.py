# -*- coding: utf-8 -*-
"""The Small Business Health Care Tax Credit in 2026 - and the SHOP problem
that now makes it unreachable in some states."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blog_lib import build

FAQ = [
 ("How much is the small business health care tax credit worth?",
  "Up to 50 percent of what the employer paid in premiums for a for-profit employer, or 35 percent for a tax-exempt one. It is available for two consecutive taxable years and no more. The full amount goes to the smallest, lowest-wage employers; it phases down as the business gets larger or better paid."),
 ("What are the eligibility rules?",
  "Four conditions, all of which must be met: fewer than 25 full-time equivalent employees; average annual wages below an inflation-indexed threshold; the employer pays at least 50 percent of the cost of employee-only coverage, at a uniform percentage; and the plan is a qualified health plan bought through a SHOP marketplace, or the employer qualifies for a limited exception."),
 ("What is the average wage threshold for 2026?",
  "IRS Revenue Procedure 2025-32 sets the dollar amount in effect under section 45R(d)(3)(B) at $34,100 for taxable years beginning in 2026. The credit begins phasing out above that and phases out entirely at roughly twice it. healthcare.gov's plain-English version of the ceiling is 'about $65,000 per year or less' in average salary."),
 ("Can I claim the credit in Kentucky now that kynect's SHOP is closed?",
  "Probably not as a new purchaser. The credit generally requires a plan bought through SHOP, and Kentucky no longer has one open to new business. IRS Notice 2018-27 provides relief for an employer that first claimed the credit for 2016 or a later year and is partway through its two-year period when SHOP plans are unavailable in its county. The Kentucky exchange itself notes credits may be available for businesses that had SHOP coverage in tax year 2025 or 2026."),
 ("Does an ICHRA qualify for the credit?",
  "No. An ICHRA reimburses employees for individual coverage rather than the employer buying a qualified health plan through SHOP, so it does not meet the credit's requirements. If the credit is worth real money to you, that is a genuine argument for a group plan over an ICHRA. For most employers it is not the deciding factor."),
 ("How do I actually claim it?",
  "IRS Form 8941, Credit for Small Employer Health Insurance Premiums, filed with your return. A tax-exempt employer claims it as a refundable credit. Keep the SHOP enrolment documentation, your premium records and the wage and FTE calculations - the FTE and average wage arithmetic is where returns get questioned."),
]

TOC = [("worth", "What It Is Worth"), ("rules", "The Four Conditions"),
       ("wages", "The Wage Threshold"), ("shop", "The SHOP Problem"),
       ("states", "State by State"), ("verdict", "Is It Worth Chasing?"), ("faq", "FAQ")]

BODY = '''<h2 id="worth">What the credit is actually worth</h2>
      <p>The Small Business Health Care Tax Credit under Internal Revenue Code section 45R pays a for-profit employer up to <strong>50 percent of the premiums it paid</strong>, and a tax-exempt employer up to 35 percent. That sounds enormous until you read the next sentence in the IRS guidance: the credit is available for <strong>two consecutive taxable years</strong>, and no more.</p>
      <p>So it is a two-year subsidy on the front end of offering coverage, not an ongoing reduction in your benefits cost. That framing matters, because plenty of small employers pick a plan structure around the credit and then discover in year three that the arithmetic they built the budget on has expired.</p>
      <p>The maximum goes to the smallest and lowest-paid employers &mdash; healthcare.gov notes the largest credit goes to employers with 10 or fewer full-time equivalent employees and average wages of $28,000 or less. Above that it tapers on both axes at once.</p>

      <h2 id="rules">The four conditions</h2>
      <p>All four have to be true. The IRS states them as:</p>
      <ol>
        <li><strong>Fewer than 25 full-time equivalent employees.</strong> FTEs, not headcount &mdash; part-time hours aggregate. Owners and certain family members are excluded from the count, which usually helps.</li>
        <li><strong>Average annual wages below an inflation-indexed threshold.</strong> See below; this is where most employers fall out.</li>
        <li><strong>The employer pays at least 50 percent of the cost of employee-only coverage</strong> &mdash; not family or dependent coverage &mdash; at a uniform percentage for each employee.</li>
        <li><strong>The plan is a qualified health plan bought through a SHOP marketplace</strong>, or the employer qualifies for a limited exception.</li>
      </ol>
      <p>Condition three is the one that gets confused with carrier participation rules, which often also land on 50 percent. Different requirement, same number. <a href="/blog/group-health-insurance-minimum-participation">More on participation and contribution &rarr;</a></p>

      <h2 id="wages">The wage threshold for 2026</h2>
      <div class="highlight-box">
        <h4>$34,100</h4>
        <p>IRS Revenue Procedure 2025-32 sets the dollar amount in effect under section 45R(d)(3)(B) at <strong>$34,100 for taxable years beginning in 2026</strong>. The credit begins phasing out above that figure and phases out entirely at roughly twice it. healthcare.gov states the practical upper ceiling in rounder terms: average employee salary of &ldquo;about $65,000 per year or less.&rdquo;</p>
      </div>
      <p>Two numbers, one credit, and they get quoted interchangeably by people who should know better. Maryland's own materials illustrate the problem &mdash; the state's 2025&ndash;2026 employer guide says &ldquo;under $65,000 (adjusted annually)&rdquo; while a Maryland Business Express fact sheet says &ldquo;less than $58,000.&rdquo; Both are versions of the same indexed IRS figure at different vintages. The one to work from is the current Revenue Procedure.</p>
      <p>Practically: a business paying an average of $34,100 or less gets the full credit rate. Between there and roughly $68,000 it tapers. Above that there is nothing, regardless of how few employees you have.</p>

      <h2 id="shop">The SHOP problem, and why it is getting worse</h2>
      <p>Condition four is the one that has quietly broken. Enrolling through SHOP is, in healthcare.gov's words, &ldquo;generally the only way for a small business or non-profit to claim the Small Business Health Care Tax Credit.&rdquo; But SHOP has been dismantled almost everywhere.</p>
      <p>On the federal marketplace there is no online SHOP enrolment any more. CMS gives employers two routes: through an insurance company directly, or with the assistance of a SHOP-registered agent or broker. SHOP still exists as a certification on a plan &mdash; CMS publishes a plan year 2026 SHOP dataset and a November 2025 employer guide &mdash; but the shopping portal is gone.</p>
      <p>And in at least one state it has gone entirely.</p>

      <h2 id="states">Where you can still get it: four states</h2>
      <div class="vs-tw">
      <table class="vs-t">
        <thead><tr><th>State</th><th>SHOP status</th><th>Credit realistically available?</th></tr></thead>
        <tbody>
          <tr><td><strong>Maryland</strong></td><td>State exchange, fully operating. Employer portal, three carriers, current employer guide.</td><td><strong>Yes.</strong> The cleanest route of the four.</td></tr>
          <tr><td><strong>Florida</strong></td><td>Federal SHOP: certification only, no portal. Buy through a carrier or a SHOP-registered broker.</td><td>Yes, if the plan is SHOP-certified and you have a broker who handles the filing.</td></tr>
          <tr><td><strong>Texas</strong></td><td>Federal SHOP, same as Florida.</td><td>Yes, with the same caveat.</td></tr>
          <tr><td><strong>Kentucky</strong></td><td><strong>Closed.</strong> Anthem, the sole issuer, withdrew and KHBE states employers can no longer apply and enrol in SHOP coverage.</td><td>Not for a new purchaser. See the relief below.</td></tr>
        </tbody>
      </table>
      </div>
      <h3>The Kentucky relief</h3>
      <p>IRS Notice 2018-27 covers exactly this situation: an employer that first claimed the credit for 2016 or a later year &ldquo;may still claim the credit for all or part of the remainder of the two-year credit period, even if the employer has a principal business address in a county where QHPs are not available through the SHOP Marketplace.&rdquo; The Kentucky exchange's own notice echoes it, saying tax credits may be available for businesses that had SHOP coverage in tax year 2025 or 2026.</p>
      <p>If you are starting fresh in Kentucky, build your budget without the credit and treat it as upside if your accountant finds a route. <a href="/kentucky-small-business-health-insurance">More on buying group coverage in Kentucky &rarr;</a></p>

      <h2 id="verdict">Should the credit drive your decision?</h2>
      <p>Usually not, and it is worth being blunt about that.</p>
      <p>Run the arithmetic on a real case. Eight employees, average wage $40,000, employer paying 50 percent of employee-only premiums. The wage figure is above $34,100, so the credit is already tapering. It lasts two years. And claiming it requires you to buy a SHOP-certified plan, which may not be the best plan available to you off-exchange.</p>
      <p>That last point is the real cost. If the SHOP-certified plan is $60 a month per employee worse than the off-exchange alternative, an eight-person group gives up $5,760 a year to chase a credit that may be worth less than that and expires after twenty-four months.</p>
      <div class="highlight-box">
        <h4>Where the credit genuinely does change the answer</h4>
        <p>Very small, genuinely low-wage employers &mdash; under ten FTEs with average wages near or below $34,100 &mdash; in a state where the SHOP route is easy. A Maryland non-profit with eight staff on modest salaries is the textbook case, and there the credit is real money and worth structuring around.</p>
      </div>
      <p>One structural consequence: an ICHRA cannot qualify. You are reimbursing employees for individual coverage rather than buying a qualified health plan through SHOP. If the credit is worth serious money to you, that is a genuine argument for a group plan over an ICHRA. For most employers it is not the deciding factor. <a href="/blog/ichra-vs-group-health-subsidy-cliff">How the ICHRA comparison changed in 2026 &rarr;</a></p>

      <div class="cta-block">
        <h3>Want to know if the credit is worth chasing for your business?</h3>
        <p>Send us your headcount, average wage and state. We will tell you what the credit is realistically worth, what the SHOP-certified plan costs against the off-exchange alternative, and whether the trade is worth making. Free.</p>
        <a class="btn btn-teal" href="/quote?type=business" style="background:#fff;color:var(--blue-700)">Get group quotes &rarr;</a>
      </div>

      <h2 id="faq">Frequently asked</h2>
      <h3>Do owners count toward the 25 FTE limit?</h3>
      <p>Sole proprietors, partners, 2-percent S-corporation shareholders and certain family members are excluded from both the FTE count and the average wage calculation. That exclusion usually works in your favour on both tests.</p>
      <h3>Can I claim it for a year I already filed?</h3>
      <p>Amended returns are possible within the normal statute of limitations. Talk to your accountant &mdash; and note that using a year burns one of your two consecutive credit years.</p>
      <h3>Is the credit refundable?</h3>
      <p>For a tax-exempt employer, yes, limited to certain payroll taxes withheld and paid. For a for-profit employer it is a general business credit, so it offsets tax liability rather than generating a refund on its own, with carryback and carryforward rules.</p>
      <p class="vs-src">Sources: <a href="https://www.irs.gov/affordable-care-act/employers/small-business-health-care-tax-credit-and-the-shop-marketplace" rel="nofollow noopener" target="_blank">IRS, Small Business Health Care Tax Credit</a> &middot; <a href="https://www.irs.gov/pub/irs-drop/rp-25-32.pdf" rel="nofollow noopener" target="_blank">IRS Rev. Proc. 2025-32</a> &middot; <a href="https://www.healthcare.gov/small-businesses/provide-shop-coverage/" rel="nofollow noopener" target="_blank">healthcare.gov, SHOP and the tax credit</a> &middot; <a href="https://www.cms.gov/marketplace/employers-sponsors/small-business-health-options-program-shop" rel="nofollow noopener" target="_blank">CMS SHOP</a> &middot; <a href="https://khbe.ky.gov/Enrollment/Pages/SHOP.aspx" rel="nofollow noopener" target="_blank">Kentucky Health Benefit Exchange, SHOP</a> &middot; <a href="https://www.marylandhealthconnection.gov/smallbusiness-health-coverage-options/" rel="nofollow noopener" target="_blank">MHC for Small Business</a></p>'''

build(slug='small-business-health-care-tax-credit-2026',
      title='Small Business Health Care Tax Credit in 2026',
      h1='The Small Business Health Care Tax Credit in 2026: Who Can Still Claim It',
      desc='Up to 50% of premiums for two years, gated behind a SHOP requirement that has quietly stopped working in some states. What it is worth and where.',
      lede='The credit pays up to half your premiums &mdash; for exactly two years, if you clear four conditions, one of which has quietly become unreachable in Kentucky. Here is the honest arithmetic.',
      published='2026-08-26', read_min=8, eyebrow='Small Business',
      img='/compressed/business-seminar.jpg',
      alt='Small business owner reviewing the federal small business health care tax credit with an advisor',
      toc=TOC, body=BODY, faq=FAQ,
      cta_head='Is the credit worth it for you?',
      cta_copy='Headcount, average wage and state is all we need.')

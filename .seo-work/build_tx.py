# -*- coding: utf-8 -*-
"""Build /texas-small-business-health-insurance.

Angle nobody else leads with: Texas is a TWO-employee small group state
(Tex. Ins. Code 1501.002(14)), not the 1-50 every national page claims, and TDI
bars a tobacco load from being charged to an individual employee. Written fresh.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from state_lib import BASE, build

URL = BASE + '/texas-small-business-health-insurance'

TITLE = "Group Health Insurance Texas | Small Business Plans"
DESC = ("Group health insurance for Texas small businesses. Texas requires two employees, not one, "
        "and has 27 rating areas. Every carrier compared, free.")

FAQ = [
 ("How many employees do you need for group health insurance in Texas?",
  "Two. Texas is one of the states that did not adopt the federal one-employee floor. Under Texas Insurance Code section 1501.002(14) a small employer is one that averaged at least two but not more than 50 employees during the preceding calendar year and employs at least two on the first day of the plan year. A true sole proprietor with no employees is an individual-market buyer in Texas, not a small group buyer."),
 ("Can a husband-and-wife business get a group plan in Texas?",
  "Yes, and this is a Texas-specific advantage. Federal law generally does not treat a business made up only of two spouses as a group health plan. The Texas Department of Insurance has told carriers they must still issue coverage to a small employer with two or more employees even if those employees are married to one another, because Texas elects to regulate very small groups as small group coverage. Note the same is not true of the SHOP marketplace, whose stated rules require an employee other than owners, spouses and family."),
 ("What is the minimum participation requirement in Texas?",
  "Texas Insurance Code section 1501.154 sets it at 75 percent of eligible employees, and Texas is one of only a handful of states with a SHOP participation rate above the usual 70 percent. Employees who waive because they have other qualifying coverage - a spouse's plan, another job, Medicare, Medicaid, TRICARE or VA coverage - are taken out of the calculation rather than counted against you."),
 ("What if we cannot hit 75 percent participation?",
  "Apply between November 15 and December 15. Federal market rules at 45 CFR 147.104(b)(1) let a small group carrier limit coverage to that annual window for an employer who cannot meet a participation or contribution requirement, and TDI states plainly that carriers may not refuse a group outright on participation grounds. Inside that window the requirement does not apply. Do not confuse it with individual open enrollment, which runs November 1 to January 15."),
 ("Does my industry change what I pay for group health in Texas?",
  "No. For a group of 50 or fewer, federal rule 45 CFR 147.102 permits premiums to vary only by individual-versus-family coverage, rating area, age within a 3 to 1 band, and tobacco use within a 1.5 to 1 band, and says rates must not vary by any other factor. Industry classification, injury rate and prior claims experience are not permitted rating factors. This is the opposite of how workers' compensation is priced, which is why so many owners in high-hazard trades assume group health will be expensive and never ask."),
 ("Can a Texas carrier charge one smoker on my team more?",
  "No. Federal law allows a 1.5 to 1 tobacco variation, but TDI has told carriers that in Texas tobacco use is treated as a health status factor, and section 1501.206 prohibits adjusting an individual small group enrollee's rate on health status. A tobacco load may be reflected in the rate charged to the employer, but it has to be applied uniformly across every member of the group rather than assessed against the person who smokes."),
 ("How much does a broker cost a Texas small business?",
  "Nothing. Carrier commission is built into the premium whether you use a broker or go direct, so the rate is the same either way. You may as well have someone shop all 27 rating areas, run the participation math and handle the filings."),
]

SCHEMA = [
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
  {"@type": "ListItem", "position": 2, "name": "Small Business Health Insurance",
   "item": BASE + "/small-business-health-insurance"},
  {"@type": "ListItem", "position": 3, "name": "Texas"}]},
 {"@context": "https://schema.org", "@type": "Service",
  "serviceType": "Group health insurance for Texas small business",
  "name": "Group Health Insurance for Texas Small Business", "url": URL,
  "provider": {"@type": "InsuranceAgency", "name": "VS Health Benefits", "url": BASE + "/",
               "telephone": "+1-954-825-1009", "email": "info@vshealthbenefits.com",
               "address": {"@type": "PostalAddress", "addressLocality": "Miami",
                           "addressRegion": "FL", "addressCountry": "US"}},
  "areaServed": [{"@type": "City", "name": c, "addressRegion": "TX"} for c in
                 ["Houston", "Dallas", "Fort Worth", "Austin", "San Antonio", "El Paso",
                  "Arlington", "Corpus Christi", "Plano", "Laredo", "McAllen", "Lubbock"]]
                + [{"@type": "State", "name": "Texas"}],
  "audience": {"@type": "BusinessAudience",
               "name": "Texas small businesses with 2 to 50 employees",
               "numberOfEmployees": {"@type": "QuantitativeValue", "minValue": 2, "maxValue": 50}},
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
             "description": "Free group health comparison and setup; carriers pay the broker commission."},
  "availableChannel": {"@type": "ServiceChannel", "serviceUrl": BASE + "/quote?type=business",
                       "servicePhone": {"@type": "ContactPoint", "telephone": "+1-954-825-1009"}}},
]

BODY = '''<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Group Health Insurance &middot; Texas</span>
        <h1>Group health insurance for <span>Texas small business</span></h1>
        <p class="hero-sub">Plans for teams of 2 to 50 anywhere in Texas &mdash; Houston, DFW, Austin, San Antonio, El Paso and the Valley. We compare every carrier writing in your rating area, run the participation math, and it costs you nothing. Carriers pay our commission either way.</p>
        <p><a class="vs-ih-cta" href="/quote?type=business">Get group quotes for your team &rarr;</a></p>
      </div>
      <div>
        <div class="vs-ih-panel">
          <h2 style="font-size:1.05rem;margin:0 0 14px">Texas group coverage at a glance</h2>
          <dl class="vs-ih-dl">
            <div><dt>Group size</dt><dd>2 to 50 employees</dd></div>
            <div><dt>Rating areas</dt><dd>27 &mdash; your county sets the rate</dd></div>
            <div><dt>Participation</dt><dd>75% of eligible employees</dd></div>
            <div><dt>Participation waiver</dt><dd>Nov 15 &ndash; Dec 15 each year</dd></div>
            <div><dt>Employer share</dt><dd>No state minimum; carriers typically 50%</dd></div>
            <div><dt>Our fee</dt><dd>$0 &mdash; carriers pay the commission</dd></div>
          </dl>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Texas needs two employees, not one</h2>
    <div class="vs-ih-key">
      <strong>Almost every national page you will read says a small group starts at one employee. In Texas that is wrong.</strong>
      <p>Texas Insurance Code section 1501.002(14) defines a small employer as one that &ldquo;employed an average of at least two employees but not more than 50 employees on business days during the preceding calendar year and who employs at least two employees on the first day of the plan year.&rdquo; Two separate tests, both of which have to be met. The federal default at 45 CFR 155.20 is one; Texas chose two and kept it.</p>
      <p>The practical effect is that a genuine one-person business in Texas cannot buy small group coverage, however it is structured on paper. Owners find this out after they have already picked a plan.</p>
    </div>
    <p class="lede">Two things soften it, and both are Texas-only.</p>
    <h3 class="sub">Two spouses count as a group in Texas</h3>
    <p class="lede">Federal guidance does not treat a husband-and-wife business as a group health plan unless there is a common-law employee who is neither spouse. TDI has told carriers they may not refuse a Texas group on that basis: under Texas law a group of two eligible employees is a small group regardless of marital status, and coverage must be issued. If you and your spouse are both on payroll, you are a group in Texas.</p>
    <h3 class="sub">A sole proprietor has one route in &mdash; a health group cooperative</h3>
    <p class="lede">Texas statute creates an &ldquo;eligible single-employee business&rdquo; category at section 1501.051(3-a) &mdash; owned and operated by a sole proprietor, averaging fewer than two employees. Section 1501.0581 lets a health group cooperative admit those businesses, and when it does, the small-employer guaranteed-issue, rating and mandated-benefit rules apply to them. It is a narrow door, but it exists, and it is the only one. If you are a true group of one, the realistic comparison is that route against individual coverage or an ICHRA from a related entity.</p>
    <p class="vs-ih-src">Sources: <a href="https://statutes.capitol.texas.gov/Docs/IN/htm/IN.1501.htm" rel="nofollow noopener" target="_blank">Tex. Ins. Code ch. 1501</a> &middot; <a href="https://www.tdi.texas.gov/health/faq.html" rel="nofollow noopener" target="_blank">TDI health carrier FAQ</a></p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>27 rating areas, and DFW is split down the middle</h2>
    <p class="lede">Texas prices small group by the employer&rsquo;s geographic rating area, and it has 27 of them &mdash; more granular than almost any state. Before 2023 there were 26, with a single catch-all area covering all 177 rural counties. Texas dissolved that area and folded those counties into adjacent urban ones, so a rural Texas employer is now pooled with a nearby metro rather than with the rest of rural Texas.</p>
    <div class="vs-ih-scroll">
    <table class="vs-ih-tbl">
      <thead><tr><th>Metro</th><th>Rating area</th><th>What that means for you</th></tr></thead>
      <tbody>
        <tr><td>Houston</td><td>Area 10 &mdash; Harris, Galveston</td><td>One area covers the core; surrounding counties rate separately</td></tr>
        <tr><td>Dallas</td><td>Area 8 &mdash; Collin, Dallas, Ellis, Hunt, Kaufman, Navarro, Rockwall</td><td rowspan="2">DFW is <strong>two</strong> rating areas. A team split across Dallas and Tarrant counties is not one price</td></tr>
        <tr><td>Fort Worth</td><td>Area 25 &mdash; Tarrant, Denton, Parker, Johnson, Hood and others</td></tr>
        <tr><td>Austin</td><td>Area 3 &mdash; Travis, Williamson, Hays, Bastrop and others</td><td>Wide area; suburban growth counties are included</td></tr>
        <tr><td>San Antonio</td><td>Area 18 &mdash; Bexar, Comal, Guadalupe, Kendall and 17 more</td><td>Largest area by county count, reaching to the border</td></tr>
        <tr><td>El Paso</td><td>Area 9 &mdash; El Paso, Hudspeth, Culberson, Brewster and others</td><td>Far West Texas rates as its own pool</td></tr>
        <tr><td>Rio Grande Valley</td><td>Area 15 (Hidalgo, Starr, Brooks) and Area 5 (Cameron, Willacy, Kenedy)</td><td>McAllen and Brownsville are <strong>separate</strong> rating areas</td></tr>
      </tbody>
    </table>
    </div>
    <p class="lede">If you have people in more than one of these, model it before you sign. Two offices ninety minutes apart can carry meaningfully different per-employee costs for identical coverage, and the quote you were given for the headquarters address is not the quote for the whole company.</p>
    <p class="vs-ih-src">County assignments: <a href="https://www.cms.gov/CCIIO/Programs-and-Initiatives/Health-Insurance-Market-Reforms/tx-gra" rel="nofollow noopener" target="_blank">CMS Texas geographic rating areas</a></p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>The 75 percent rule, and the two-week window that suspends it</h2>
    <p class="lede">Texas Insurance Code section 1501.154 makes coverage available to a small employer when at least 75 percent of eligible employees elect to participate &mdash; higher than the 70 percent most states use, and Texas is named explicitly on healthcare.gov as one of the few states above the standard. Carriers may offer a lower threshold, but they have to offer the same lower threshold to every Texas small employer, so in practice 75 percent is what you plan against.</p>
    <div class="vs-ih-key">
      <strong>Who actually counts is where most employers go wrong.</strong>
      <p>Owners, an owner&rsquo;s spouse, COBRA enrollees and retirees come out of the calculation entirely. So does any employee who declines because they already have qualifying coverage &mdash; a spouse&rsquo;s plan, a second job, Medicare, Medicaid, TRICARE or VA. Those are waivers, not refusals. A ten-person company where four are on a spouse&rsquo;s plan is measured against six, not ten.</p>
      <p>And if you still cannot get there: apply between <strong>November 15 and December 15</strong>. Federal market rules at 45 CFR 147.104(b)(1) let carriers confine a non-compliant group to that annual window, and TDI has told carriers they may not refuse the group outright &mdash; guaranteed issue still applies. Inside those thirty days the participation and contribution requirements do not.</p>
    </div>
    <h3 class="sub">Employer contribution</h3>
    <p class="lede">Texas imposes no minimum. Section 1501.153 says outright that the chapter does not require a small employer to contribute, though it lets carriers set their own requirement in line with their usual practice &mdash; which in Texas is generally at least half of the employee-only premium. Separately, paying at least 50 percent of employee-only coverage is a condition of the federal Small Business Health Care Tax Credit, so the two numbers get conflated. They are not the same rule.</p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>A Texas tobacco surcharge cannot land on one employee</h2>
    <div class="vs-ih-key">
      <strong>Federal law permits a 1.5 to 1 tobacco load. Texas does not let a carrier charge it to the person who smokes.</strong>
      <p>TDI has told carriers that in Texas tobacco use has always been treated as a health status related factor under section 1501.002(7), and section 1501.206 prohibits adjusting an individual small group enrollee&rsquo;s premium on health status. The department states it will not change that interpretation. A carrier may reflect a tobacco load in the rate charged to the employer, but &ldquo;the surcharge must be applied uniformly to the rates charged for all members of the small employer.&rdquo;</p>
      <p>If a Texas quote shows a per-person smoker surcharge on a named employee, that is worth a question before you sign.</p>
    </div>
    <p class="lede">The wider point is that a small group of 2 to 50 in Texas can be rated on five things and nothing else: whether the coverage is individual or family, the rating area, employee age within a 3 to 1 band, tobacco use within a 1.5 to 1 band, and the plan you pick. Industry, injury rate and last year&rsquo;s claims are not on the list. Owners in construction, oilfield services, trucking and manufacturing routinely assume group health is priced the way workers&rsquo; comp is &mdash; class code, experience mod, loss history &mdash; and never get a quote. It is not, and the assumption is expensive.</p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>What Texas employers actually run into</h2>
    <div class="vs-ih-grid">
      <div class="vs-ih-card">
        <strong>Energy and oilfield services</strong>
        <span>Headcount swings with rig count, and crews rotate across rating areas. Waiting periods and a variable-hour measurement period are what stop you enrolling and terminating the same people every quarter.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Construction and the trades</strong>
        <span>Mixed W-2 and 1099 crews and seasonal headcount. Your trade does not raise your health premium. On federally funded work, bona fide health contributions can count toward the prevailing-wage fringe obligation instead of being paid as cash.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Restaurants and hospitality</strong>
        <span>Tipped wages, turnover and part-time staff. Employees averaging under 30 hours generally do not have to be offered coverage, and the ACA lookback lets you measure over a period rather than guess month to month.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Trucking and logistics</strong>
        <span>Drivers domiciled across several rating areas, owner-operators who cannot go on a group plan at all, and DOT physical questions. An ICHRA often reaches the 1099 side a group plan cannot.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Healthcare and clinical practices</strong>
        <span>Small, stable, mostly full-time teams competing against hospital systems for staff. Usually the most straightforward group case and often a strong level-funded candidate.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Teams split across metros</strong>
        <span>Houston, DFW and Austin rate separately, and DFW itself is two areas. Participation is measured across the whole company rather than per location, which usually works in your favour.</span>
      </div>
    </div>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Benefits are a bigger hiring lever in Texas than anywhere else</h2>
    <p class="lede">Texas has the highest uninsured rate in the country. In 2024, 16.8 percent of Texans had no health coverage against a national figure of 8.2 percent, and 19.2 percent of Texans under 65 were uninsured. Nationally, only about half of employees at firms with fewer than 50 people work somewhere that offers health insurance at all, against 97 percent at firms of 50 or more.</p>
    <p class="lede">Put those together and a Texas small employer that offers coverage is competing for staff against a field where most of the comparable jobs do not. That is the argument for offering, and it is stronger here than in any other state.</p>
    <p class="vs-ih-src">Sources: <a href="https://www.kff.org/uninsured/state-indicator/nonelderly-uninsured-rate-by-age/" rel="nofollow noopener" target="_blank">KFF State Health Facts, 2024 ACS</a> &middot; <a href="https://meps.ahrq.gov/data_files/publications/rf54/rf54.shtml" rel="nofollow noopener" target="_blank">AHRQ MEPS-IC Research Findings #54</a>. National figures where noted; there is no reliable Texas-only small-group premium average, and we will not invent one &mdash; ask us for real quotes instead.</p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Three ways to cover a Texas team</h2>
    <div class="vs-ih-grid">
      <a class="vs-ih-card" href="/small-business-health-insurance">
        <strong>Traditional group plan</strong>
        <span>Fully insured, simplest to run, predictable renewal. Carriers want 75 percent participation in Texas and usually at least half the employee-only premium from you.</span>
        <em>How group plans work &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/level-funded-health-insurance-florida">
        <strong>Level-funded</strong>
        <span>Often below fully insured for a healthier group, with a refund of unused claims at year end. Texas regulates the stop-loss policy underneath these as direct insurance, so the terms matter more here.</span>
        <em>Compare level-funded &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/ichra-florida-small-business">
        <strong>ICHRA</strong>
        <span>Reimburse individual premiums tax-free instead of running a group plan. Caps your cost, hands employees the choice, and reaches contractors a group plan cannot.</span>
        <em>How ICHRA works &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/small-business-health-insurance-calculator">
        <strong>Not sure yet? Run the numbers</strong>
        <span>Estimate your monthly cost by employee count, ages and how much you contribute. Instant, no email required.</span>
        <em>Open the calculator &rarr;</em>
      </a>
    </div>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Setting up a Texas group plan</h2>
    <p class="lede">Most owners arrive with one question &mdash; what does it cost &mdash; and leave with four decisions, in this order:</p>
    <h3 class="sub">1. Confirm you have two employees</h3>
    <p class="lede">Average of at least two in the prior calendar year and at least two on day one of the plan year. W-2 only; 1099 contractors cannot go on a group plan whatever you call them internally. In Texas the count is of all employees, not only the eligible ones &mdash; the legislature changed that wording in 2013.</p>
    <h3 class="sub">2. Decide your contribution</h3>
    <p class="lede">No Texas minimum, but carriers generally want half of employee-only, and 50 percent is also the tax-credit condition. Going above it lifts participation, which is what keeps you clear of the 75 percent threshold.</p>
    <h3 class="sub">3. Check the network by name</h3>
    <p class="lede">Look your people&rsquo;s actual doctors up in the plan&rsquo;s own directory, not the carrier&rsquo;s marketing page. Texas plan names oversell network breadth, and a narrow network discovered in February is an expensive surprise.</p>
    <h3 class="sub">4. Pick a start date</h3>
    <p class="lede">Group coverage is not tied to the ACA open enrollment calendar &mdash; a Texas small business can start a plan in any month, and the effective date becomes your annual renewal point. The one date that matters is November 15 to December 15, if participation is tight. <a href="/business-open-enrollment-faq">More on employer timing &rarr;</a></p>
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
      <a class="vs-ih-card" href="/blog/how-many-employees-do-you-need-for-group-health-insurance"><strong>How many employees do you need?</strong><span>Florida, Texas, Maryland and Kentucky all answer this differently. Two of them are not 1&ndash;50.</span><em>Read the comparison &rarr;</em></a>
      <a class="vs-ih-card" href="/blog/group-health-insurance-minimum-participation"><strong>Can&rsquo;t hit minimum participation?</strong><span>What counts as a waiver, and the November 15 to December 15 window that suspends the requirement.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-ih-card" href="/blog/small-business-health-care-tax-credit-2026"><strong>The tax credit in 2026</strong><span>Who can still claim it, the $34,100 wage figure, and why the SHOP requirement now breaks in some states.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-ih-card" href="/group-health-insurance-by-industry"><strong>Group health by industry</strong><span>Ten trades, what each runs into, and the rating rules that apply to all of them.</span><em>Browse by trade &rarr;</em></a>
    </div>
  </div>
</section>

<section class="vs-ih-band">
  <div class="vs-ih-inner">
    <h2>Send us your headcount and we will price it</h2>
    <p>Employee count, ages and ZIP codes is enough to start. We come back with real numbers from every carrier writing in your Texas rating area &mdash; not a range, your range. Licensed in Texas and 40+ states, bilingual, and free either way.</p>
    <p style="margin:0"><a class="vs-ih-cta" href="/quote?type=business" style="background:#fff;color:#0b2346">Get Texas group quotes &rarr;</a></p>
  </div>
</section>

'''

build('texas-small-business-health-insurance.html', URL, TITLE, DESC,
      'US-TX', 'Texas', BODY, FAQ, SCHEMA)

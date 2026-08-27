# -*- coding: utf-8 -*-
"""Build /maryland-small-business-health-insurance.

Angles nobody else leads with: Maryland is one of the last states with a working
small-business exchange (and it is the only route to the federal tax credit), and
no Maryland carrier applies a tobacco surcharge because the exchange platform
cannot process one. Written fresh.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from state_lib import BASE, build

URL = BASE + '/maryland-small-business-health-insurance'

TITLE = "Group Health Insurance Maryland | Small Business"
DESC = ("Group health insurance for Maryland small businesses. Maryland still runs a real small "
        "business exchange, and no carrier here charges a tobacco load.")

FAQ = [
 ("How many employees do you need for group health insurance in Maryland?",
  "Up to 50, with a practical floor of one common-law employee who is not the owner. Maryland Insurance Article section 31-101 defines a small employer as one that averaged not more than 50 employees in the preceding calendar year, counting full-time employees plus full-time equivalents. Maryland Health Connection for Small Business states the employer must have at least one common-law employee on payroll, not including a business owner, sole proprietor or spouse. A true group of one buys individual coverage in Maryland, not small group."),
 ("Does Maryland still have a SHOP marketplace?",
  "Yes, and it is one of the few states that does. Maryland Health Connection for Small Business is a live state-run small business exchange with a current employer guide, an online employer portal and three participating carriers for 2025-2026: CareFirst, UnitedHealthcare and Kaiser Permanente. You can enrol through the portal or through a broker, and using a broker costs nothing."),
 ("Do Maryland small group plans charge a tobacco surcharge?",
  "In practice, no. Maryland law permits a tobacco variation of up to 1.5 to 1, but Maryland Health Connection's own carrier reference manual states that the exchange cannot accommodate tobacco rating, and because ACA rating rules apply market-wide rather than only on the exchange, no Maryland carrier has filed a tobacco rating factor. For a Maryland group with smokers on it, that is a real difference against neighbouring states where the load does apply."),
 ("What is the minimum participation requirement in Maryland?",
  "On Maryland Health Connection for Small Business it is 60 percent, applied uniformly across every participating carrier and both purchasing models since 1 November 2024. Off the exchange, Maryland Insurance Article section 15-1206 caps what any carrier may demand at 75 percent. Employees covered under a spouse's plan, another employer's arrangement, Medicare, Medicaid or CHAMPUS, and employees under 26 on a parent's plan, are excluded from the calculation."),
 ("What if we cannot meet the participation requirement?",
  "Apply between November 15 and December 15. Maryland is unusual in putting this in statute rather than leaving it to federal market rules: section 15-1206 says a carrier may not impose a minimum participation requirement on a small employer group that applies during the period beginning November 15 and extending through December 15 of any year. Note it waives participation only. There is no authority waiving a carrier's contribution requirement in that window."),
 ("How many rating areas does Maryland have, and which one am I in?",
  "Four. Area 1 is the Baltimore metro - Baltimore City and County, Anne Arundel, Harford and Howard. Area 2 is Eastern and Southern Maryland. Area 3 is the DC suburbs, and it is only Montgomery and Prince George's. Area 4 is Western Maryland, and it includes Frederick and Carroll, which catches people out because they are often assumed to be in the DC-suburb area."),
 ("Is level-funded coverage available to a small Maryland employer?",
  "It is, but Maryland regulates it more tightly than most states. Insurance Article section 15-129 sets minimum stop-loss attachment points for small employers: a specific attachment point of not less than $22,500 and an aggregate attachment point of not less than 120 percent of expected claims, for policies issued on or after 1 June 2015. Deep-attachment level-funded designs that work in unregulated states cannot be structured the same way here, so the comparison against a fully insured plan is genuinely closer in Maryland."),
]

SCHEMA = [
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
  {"@type": "ListItem", "position": 2, "name": "Small Business Health Insurance",
   "item": BASE + "/small-business-health-insurance"},
  {"@type": "ListItem", "position": 3, "name": "Maryland"}]},
 {"@context": "https://schema.org", "@type": "Service",
  "serviceType": "Group health insurance for Maryland small business",
  "name": "Group Health Insurance for Maryland Small Business", "url": URL,
  "provider": {"@type": "InsuranceAgency", "name": "VS Health Benefits", "url": BASE + "/",
               "telephone": "+1-954-825-1009", "email": "info@vshealthbenefits.com",
               "address": {"@type": "PostalAddress", "addressLocality": "Miami",
                           "addressRegion": "FL", "addressCountry": "US"}},
  "areaServed": [{"@type": "City", "name": c, "addressRegion": "MD"} for c in
                 ["Baltimore", "Columbia", "Silver Spring", "Rockville", "Bethesda", "Frederick",
                  "Annapolis", "Gaithersburg", "Bowie", "Towson", "Salisbury", "Hagerstown"]]
                + [{"@type": "AdministrativeArea", "name": "Montgomery County"},
                   {"@type": "AdministrativeArea", "name": "Prince George's County"},
                   {"@type": "AdministrativeArea", "name": "Baltimore County"},
                   {"@type": "AdministrativeArea", "name": "Anne Arundel County"},
                   {"@type": "State", "name": "Maryland"}],
  "audience": {"@type": "BusinessAudience",
               "name": "Maryland small businesses with 1 to 50 employees",
               "numberOfEmployees": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 50}},
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
             "description": "Free group health comparison and setup; carriers pay the broker commission."},
  "availableChannel": {"@type": "ServiceChannel", "serviceUrl": BASE + "/quote?type=business",
                       "servicePhone": {"@type": "ContactPoint", "telephone": "+1-954-825-1009"}}},
]

BODY = '''<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Group Health Insurance &middot; Maryland</span>
        <h1>Group health insurance for <span>Maryland small business</span></h1>
        <p class="hero-sub">Plans for teams of up to 50 across all four Maryland rating areas &mdash; Baltimore, the DC suburbs, the Eastern Shore and Western Maryland. We compare every carrier, handle the exchange filing, and it costs you nothing. Carriers pay our commission either way.</p>
        <p><a class="vs-ih-cta" href="/quote?type=business">Get group quotes for your team &rarr;</a></p>
      </div>
      <div>
        <div class="vs-ih-panel">
          <h2 style="font-size:1.05rem;margin:0 0 14px">Maryland group coverage at a glance</h2>
          <dl class="vs-ih-dl">
            <div><dt>Group size</dt><dd>Up to 50 employees</dd></div>
            <div><dt>Rating areas</dt><dd>4</dd></div>
            <div><dt>Participation</dt><dd>60% on exchange, 75% cap off it</dd></div>
            <div><dt>Participation waiver</dt><dd>Nov 15 &ndash; Dec 15, in statute</dd></div>
            <div><dt>Tobacco surcharge</dt><dd>Not applied by Maryland carriers</dd></div>
            <div><dt>2026 approved increase</dt><dd>4.9% average, small group</dd></div>
          </dl>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Maryland is one of the last states with a small business exchange that works</h2>
    <div class="vs-ih-key">
      <strong>Almost everywhere else, SHOP is a certification stamp on a plan you buy from a carrier. In Maryland it is a real marketplace with a portal, a plan menu and three carriers.</strong>
      <p>Maryland Health Connection for Small Business publishes a current employer guide, runs an employer portal, and had CareFirst, UnitedHealthcare and Kaiser Permanente participating for 2025&ndash;2026. Texas and Florida employers have no equivalent &mdash; the federal SHOP dropped online enrolment years ago. Kentucky&rsquo;s closed to new business entirely when its sole issuer withdrew.</p>
      <p>That matters for one concrete reason: <strong>buying through the exchange is generally the only way to claim the federal Small Business Health Care Tax Credit</strong>. Maryland is one of the few states where that route is still straightforwardly open.</p>
    </div>
    <p class="lede">Maryland also gives you a choice of purchasing model that most states cannot. Under <strong>Employer Choice</strong> you pick one carrier and a reference plan, and employees choose any plan from that carrier. Under <strong>Employee Choice</strong> you pick up to two consecutive metal levels and a reference plan, and employees choose across every carrier at those levels. Employee Choice is how a small Maryland employer gets something closer to a large-company benefits menu without running two plans.</p>
    <p class="lede">Rates are guaranteed for twelve months from the initial effective date, and effective dates are always the first of a month.</p>
    <p class="vs-ih-src">Sources: <a href="https://www.marylandhealthconnection.gov/smallbusiness-health-coverage-options/" rel="nofollow noopener" target="_blank">MHC for Small Business</a> &middot; <a href="https://www.healthcare.gov/small-businesses/provide-shop-coverage/" rel="nofollow noopener" target="_blank">healthcare.gov on the tax credit and SHOP</a></p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Nobody in Maryland pays a tobacco surcharge</h2>
    <div class="vs-ih-key">
      <strong>Not because Maryland bans it &mdash; because the exchange cannot process it, so no carrier ever filed one.</strong>
      <p>Maryland Insurance Article section 15-1205 permits small group rates to vary by tobacco use up to 1.5 to 1, exactly like the federal rule. But Maryland Health Connection&rsquo;s carrier reference manual says plainly: &ldquo;At this time, Maryland Health Connection cannot accommodate tobacco rating.&rdquo; The platform Maryland adopted in 2015 has no tobacco factor. Because ACA rating rules apply at the market level rather than only on-exchange, carriers have not filed tobacco rating factors at all &mdash; the then-Insurance Commissioner confirmed as much publicly.</p>
      <p>So: Maryland law allows it, Maryland carriers do not do it. For a group where two or three people smoke, that is a real difference against Virginia, Delaware or Pennsylvania, where a 1.5 to 1 load is live.</p>
    </div>
    <p class="lede">What Maryland small group rates can vary on, then, comes down to four things: whether the coverage is individual or family, the rating area, employee age within a 3 to 1 band, and the plan selected. Section 15-1205 closes the list explicitly &mdash; &ldquo;a rate may not vary by any factor that is not specified.&rdquo; Your industry, your claims history and your employees&rsquo; health are not rating factors, whatever a competitor&rsquo;s quote implies.</p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Four rating areas, and Frederick is not where people think</h2>
    <div class="vs-ih-scroll">
    <table class="vs-ih-tbl">
      <thead><tr><th>Area</th><th>Name</th><th>Jurisdictions</th></tr></thead>
      <tbody>
        <tr><td><strong>1</strong></td><td>Baltimore Metropolitan</td><td>Baltimore City, Baltimore County, Anne Arundel, Harford, Howard</td></tr>
        <tr><td><strong>2</strong></td><td>Eastern &amp; Southern Maryland</td><td>Cecil, Kent, Queen Anne&rsquo;s, Talbot, Caroline, Dorchester, Wicomico, Somerset, Worcester, St. Mary&rsquo;s, Charles, Calvert</td></tr>
        <tr><td><strong>3</strong></td><td>Washington DC Metropolitan</td><td>Montgomery and Prince George&rsquo;s <em>only</em></td></tr>
        <tr><td><strong>4</strong></td><td>Western Maryland</td><td>Garrett, Allegany, Washington, <strong>Frederick, Carroll</strong></td></tr>
      </tbody>
    </table>
    </div>
    <p class="lede">Frederick and Carroll sit in the Western Maryland rating area, not the DC-suburb one. Employers with an office in Frederick and staff commuting down to Montgomery County regularly assume they are being rated as a DC-metro group and are not. With only four areas Maryland is far less fragmented than Texas, which has 27 &mdash; but the DC line is the one that catches people.</p>
    <p class="vs-ih-src">County assignments: <a href="https://www.cms.gov/CCIIO/Programs-and-Initiatives/Health-Insurance-Market-Reforms/md-gra" rel="nofollow noopener" target="_blank">CMS Maryland geographic rating areas</a></p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Participation: 60 percent, and a window written into Maryland law</h2>
    <p class="lede">Maryland Health Connection for Small Business has required a minimum participation rate of 60 percent since 1 November 2024, applied uniformly across every participating carrier and both purchasing models. Off the exchange, Insurance Article section 15-1206 caps what any carrier may demand at 75 percent &mdash; a ceiling on the carrier, not a floor on you.</p>
    <div class="vs-ih-key">
      <strong>Employees with other coverage come out of the denominator.</strong>
      <p>Section 15-1206 excludes employees covered under a spousal group plan, public or private, including Medicare, Medicaid and CHAMPUS, and employees under 26 covered on a parent&rsquo;s plan. A twelve-person Maryland company where five are on a spouse&rsquo;s plan is measured against seven.</p>
      <p>And Maryland does something almost no other state does: it puts the participation escape hatch in <strong>statute</strong>. Section 15-1206 says a carrier &ldquo;may not impose a minimum participation requirement for a small employer group if the small employer group applies for coverage during the period that begins on November 15 and extends through December 15 of any year.&rdquo; Elsewhere that window exists only as a federal market rule carriers apply. In Maryland it is state law.</p>
    </div>
    <h3 class="sub">Employer contribution</h3>
    <p class="lede">There is no Maryland legal minimum. The 50 percent figure you will see quoted is a condition of the <em>federal tax credit</em>, not a Maryland requirement, and Maryland&rsquo;s own employer guide is careful to say so. Carriers may set their own contribution rules contractually. Also worth knowing: the November window waives participation only &mdash; nothing in section 15-1206 waives a carrier&rsquo;s contribution requirement.</p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Level-funded is harder to build in Maryland, and you should know why</h2>
    <p class="lede">Level-funded plans work by pairing a self-funded arrangement with a stop-loss policy that attaches at a low point. Maryland regulates that stop-loss policy directly. Insurance Article section 15-129 sets minimums for small employers, for policies issued on or after 1 June 2015:</p>
    <div class="vs-ih-scroll">
    <table class="vs-ih-tbl">
      <thead><tr><th>Attachment point</th><th>Maryland minimum for a small employer</th></tr></thead>
      <tbody>
        <tr><td>Specific (per person)</td><td>Not less than <strong>$22,500</strong></td></tr>
        <tr><td>Aggregate (whole group)</td><td>Not less than <strong>120% of expected claims</strong></td></tr>
      </tbody>
    </table>
    </div>
    <p class="lede">Section 15-129 also bars a stop-loss carrier from charging higher cost sharing for one individual within the group, or excluding an employee or dependent on a health status related factor. Policies written before June 2015 at the old $10,000 and 115 percent thresholds can still be renewed.</p>
    <p class="lede">None of that makes level-funded a bad idea in Maryland. It does mean the very aggressive designs marketed in unregulated states are not available here, and the honest comparison against a fully insured plan is closer than a national broker&rsquo;s pitch will suggest. If someone is quoting you a Maryland level-funded plan with a specific attachment point under $22,500, ask when the policy was issued.</p>
    <p class="lede">One more Maryland-specific consequence: state continuation, mandated benefits and the rating rules above apply to <em>insurance</em>. A self-funded or level-funded arrangement sits under ERISA and outside a good deal of that. That is sometimes an advantage and sometimes a trap, and it is worth walking through before you switch.</p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Maryland mandates that show up in your premium</h2>
    <p class="lede">Maryland requires benefits that many states do not, and they are part of why Maryland plans price the way they do. Among the less common ones reaching small group coverage:</p>
    <div class="vs-ih-grid">
      <div class="vs-ih-card"><strong>In vitro fertilisation and fertility preservation</strong><span>Maryland is one of a minority of states mandating IVF coverage, and separately mandates fertility preservation ahead of medically induced infertility. A meaningful benefit for a young workforce, and one competitors in neighbouring states cannot match.</span></div>
      <div class="vs-ih-card"><strong>Hearing aids, adults and children</strong><span>Maryland mandates hearing aid coverage for both. Most states mandate neither, or children only.</span></div>
      <div class="vs-ih-card"><strong>Habilitative services for children</strong><span>Occupational, physical and speech therapy through age 18. Maryland was an early adopter, ahead of the federal essential health benefit category.</span></div>
      <div class="vs-ih-card"><strong>Bariatric surgery for morbid obesity</strong><span>An express Maryland mandate rather than a carrier option.</span></div>
    </div>
    <p class="lede">Maryland&rsquo;s essential health benefits benchmark is built on a CareFirst BlueChoice HMO plan, and the Insurance Administration confirmed for 2026 that the benefits remain substantially as they have been since 2017. Approved 2026 small group rates rose 4.9 percent on average across the market, below the 5.5 percent carriers requested, with roughly 203,000 Marylanders enrolled in small group plans and more than 225 small group plans available.</p>
    <p class="vs-ih-src">Sources: <a href="https://insurance.maryland.gov/Documents/newscenter/newsreleases/2026-ACA-Press-Release-Approved-Rates-with-exhibits.pdf" rel="nofollow noopener" target="_blank">Maryland Insurance Administration, approved 2026 rates</a> &middot; <a href="https://www.cms.gov/files/document/md-state-required-benefitspdf" rel="nofollow noopener" target="_blank">CMS Maryland state-required benefits</a></p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Three ways to cover a Maryland team</h2>
    <div class="vs-ih-grid">
      <a class="vs-ih-card" href="/small-business-health-insurance">
        <strong>Traditional group plan</strong>
        <span>Fully insured, on or off the exchange. On-exchange is what keeps the federal tax credit available to you, and Employee Choice is only available there.</span>
        <em>How group plans work &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/level-funded-health-insurance-florida">
        <strong>Level-funded</strong>
        <span>Available, but bounded by Maryland&rsquo;s $22,500 specific and 120 percent aggregate stop-loss floors. Worth modelling honestly against fully insured rather than assuming it wins.</span>
        <em>Compare level-funded &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/ichra-florida-small-business">
        <strong>ICHRA</strong>
        <span>Reimburse individual premiums tax-free instead of running a group plan. Caps your cost and reaches people a group plan cannot &mdash; though it forfeits the small business tax credit.</span>
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
    <h2>Frequently asked</h2>__FAQ__
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Related reading</h2>
    <div class="vs-ih-grid">
      <a class="vs-ih-card" href="/blog/small-business-health-care-tax-credit-2026"><strong>The tax credit in 2026</strong><span>Maryland is one of the few states where the SHOP route still works. Here is what it is worth and who qualifies.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-ih-card" href="/blog/how-many-employees-do-you-need-for-group-health-insurance"><strong>How many employees do you need?</strong><span>Florida, Texas, Maryland and Kentucky all answer this differently. Two of them are not 1&ndash;50.</span><em>Read the comparison &rarr;</em></a>
      <a class="vs-ih-card" href="/blog/group-health-insurance-minimum-participation"><strong>Can&rsquo;t hit minimum participation?</strong><span>What counts as a waiver, and the November window Maryland wrote into its own statute.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-ih-card" href="/group-health-insurance-by-industry"><strong>Group health by industry</strong><span>Ten trades, what each runs into, and the rating rules that apply to all of them.</span><em>Browse by trade &rarr;</em></a>
    </div>
  </div>
</section>

<section class="vs-ih-band">
  <div class="vs-ih-inner">
    <h2>Send us your headcount and we will price it</h2>
    <p>Employee count, ages and ZIP codes is enough to start. We come back with real numbers from every carrier writing in your Maryland rating area, on and off the exchange, and tell you whether the tax credit is worth chasing. Licensed in Maryland and 40+ states, and free either way.</p>
    <p style="margin:0"><a class="vs-ih-cta" href="/quote?type=business" style="background:#fff;color:#0b2346">Get Maryland group quotes &rarr;</a></p>
  </div>
</section>

'''

build('maryland-small-business-health-insurance.html', URL, TITLE, DESC,
      'US-MD', 'Baltimore', BODY, FAQ, SCHEMA)

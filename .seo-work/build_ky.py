# -*- coding: utf-8 -*-
"""Build /kentucky-small-business-health-insurance.

Lead angle nobody else has: kynect's SHOP is CLOSED to new enrolment after Anthem,
the sole issuer, withdrew - so a Kentucky small employer has no marketplace portal
and the federal tax credit route is effectively shut for new purchasers. Plus the
two-employee floor, the 1.4:1 tobacco ceiling, any-willing-provider, and mini-COBRA.
Written fresh.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from state_lib import BASE, build

URL = BASE + '/kentucky-small-business-health-insurance'

TITLE = "Group Health Insurance Kentucky | Small Business"
DESC = ("Group health insurance for Kentucky small businesses. kynect's SHOP is closed to new groups, "
        "so it runs through a carrier or broker. Two-employee minimum.")

FAQ = [
 ("Can I still buy small business health insurance through kynect?",
  "No. The Kentucky Health Benefit Exchange states that Anthem, the current issuer, will no longer offer SHOP health or dental plans through the marketplace, and that effective immediately employers can no longer apply and enrol in SHOP coverage in Kentucky. Existing enrollees were told they would see no disruption. New groups now go directly to a carrier or work through a licensed agent or broker. This does not affect individual coverage on kynect, which is unchanged."),
 ("How many employees do you need for group health insurance in Kentucky?",
  "Two. KRS 304.17A-005(44) defines a small employer as one that employed an average of at least two but not more than 50 employees during the preceding calendar year and employs at least two on the first day of the plan year. Both tests have to be met. A sole proprietor with no other employees does not qualify for the Kentucky small group market and is an individual-market buyer. Kentucky also did not take the option to raise the small group ceiling to 100 employees, so 50 remains the cap."),
 ("Can a Kentucky small business still claim the federal health care tax credit?",
  "It is difficult now. The Small Business Health Care Tax Credit generally requires the plan to be bought through a SHOP marketplace, and Kentucky no longer has one open to new business. IRS Notice 2018-27 provides relief for an employer that first claimed the credit for 2016 or a later year and is partway through its two-year credit period when SHOP plans are not available in its county. KHBE itself notes tax credits may be available for businesses that had SHOP coverage in tax year 2025 or 2026. If you are starting fresh in Kentucky, plan on the credit not being part of the arithmetic and treat it as upside if it turns out to be available."),
 ("What is Kentucky's maximum tobacco surcharge?",
  "1.4 to 1, below the federal ceiling of 1.5 to 1. Both CMS's market rating reforms table and the Kentucky Department of Insurance's own PPACA pre-emption chart publish Kentucky's tobacco maximum as 1.4 to 1 in the individual and small group markets. Kentucky uses the federal default 3 to 1 age ratio and the federal standard age curve."),
 ("Why do narrow-network plans save less in Kentucky?",
  "Because of the any willing provider law. KRS 304.17A-270 says a health insurer shall not discriminate against any provider located within the plan's geographic coverage area who is willing to meet the insurer's terms and conditions for participation. Kentucky networks therefore tend to be broader and harder to narrow than in other states, which is generally good for your employees and means the aggressive narrow-network discounts pitched by national brokers usually do not materialise here."),
 ("Do I have to offer COBRA if I have fewer than 20 employees in Kentucky?",
  "Federal COBRA does not apply below 20 employees, but Kentucky's own continuation law does. KRS 304.18-110 requires employers with fewer than 20 employees offering fully insured coverage to let employees and dependents extend group health coverage for 18 months after it would otherwise have ended. This is the single most commonly missed compliance obligation for a Kentucky group of two to nineteen. Note it applies to insurance, so a self-funded or level-funded arrangement is outside it."),
 ("How many rating areas does Kentucky have?",
  "Eight, defined by county rather than ZIP code. Louisville and Jefferson County are Area 3. Lexington and Fayette County are Area 5. Northern Kentucky - Boone, Kenton, Campbell, Gallatin, Grant and Pendleton - is Area 6, the smallest in the state. Bowling Green does not get its own area; Warren County sits inside the twenty-county Southern Kentucky Area 4. Eastern and Appalachian Kentucky is Area 8."),
]

SCHEMA = [
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
  {"@type": "ListItem", "position": 2, "name": "Small Business Health Insurance",
   "item": BASE + "/small-business-health-insurance"},
  {"@type": "ListItem", "position": 3, "name": "Kentucky"}]},
 {"@context": "https://schema.org", "@type": "Service",
  "serviceType": "Group health insurance for Kentucky small business",
  "name": "Group Health Insurance for Kentucky Small Business", "url": URL,
  "provider": {"@type": "InsuranceAgency", "name": "VS Health Benefits", "url": BASE + "/",
               "telephone": "+1-954-825-1009", "email": "info@vshealthbenefits.com",
               "address": {"@type": "PostalAddress", "addressLocality": "Miami",
                           "addressRegion": "FL", "addressCountry": "US"}},
  "areaServed": [{"@type": "City", "name": c, "addressRegion": "KY"} for c in
                 ["Louisville", "Lexington", "Bowling Green", "Owensboro", "Covington",
                  "Florence", "Georgetown", "Richmond", "Elizabethtown", "Paducah",
                  "Nicholasville", "Ashland"]]
                + [{"@type": "AdministrativeArea", "name": "Jefferson County"},
                   {"@type": "AdministrativeArea", "name": "Fayette County"},
                   {"@type": "AdministrativeArea", "name": "Boone County"},
                   {"@type": "AdministrativeArea", "name": "Kenton County"},
                   {"@type": "State", "name": "Kentucky"}],
  "audience": {"@type": "BusinessAudience",
               "name": "Kentucky small businesses with 2 to 50 employees",
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
        <span class="eyebrow">Group Health Insurance &middot; Kentucky</span>
        <h1>Group health insurance for <span>Kentucky small business</span></h1>
        <p class="hero-sub">Plans for teams of 2 to 50 across all eight Kentucky rating areas &mdash; Louisville, Lexington, Northern Kentucky, Bowling Green, Owensboro and eastern Kentucky. kynect&rsquo;s small business marketplace is closed, so this now runs through a carrier or a broker. We do it for nothing; carriers pay our commission either way.</p>
        <p><a class="vs-ih-cta" href="/quote?type=business">Get group quotes for your team &rarr;</a></p>
      </div>
      <div>
        <div class="vs-ih-panel">
          <h2 style="font-size:1.05rem;margin:0 0 14px">Kentucky group coverage at a glance</h2>
          <dl class="vs-ih-dl">
            <div><dt>Group size</dt><dd>2 to 50 employees</dd></div>
            <div><dt>Rating areas</dt><dd>8, by county</dd></div>
            <div><dt>kynect SHOP</dt><dd>Closed to new enrollment</dd></div>
            <div><dt>Tobacco ceiling</dt><dd>1.4:1 &mdash; below the federal 1.5:1</dd></div>
            <div><dt>State continuation</dt><dd>18 months, employers under 20</dd></div>
            <div><dt>Our fee</dt><dd>$0 &mdash; carriers pay the commission</dd></div>
          </dl>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>kynect&rsquo;s small business marketplace is closed</h2>
    <div class="vs-ih-key">
      <strong>This is the fact that changes how you buy in Kentucky, and most pages still on the web have not caught up with it.</strong>
      <p>The Kentucky Health Benefit Exchange states it directly: Anthem, the current issuer, will no longer offer SHOP health or dental plans through the marketplace, and &ldquo;effective immediately, employers will no longer be able to enrol in new plans through SHOP.&rdquo; KHBE tells small businesses to work directly with Anthem, or with a licensed agent or broker, to find alternative group coverage. Existing enrollees were told they would see no disruption.</p>
      <p>Individual coverage on kynect is unaffected. Kentucky came back to a fully state-based exchange for the 2022 plan year and it is still running &mdash; open enrolment for 2027 coverage runs 1 November 2026 to 15 January 2027. It is the <em>small business</em> side that closed.</p>
    </div>
    <p class="lede">Two practical consequences follow.</p>
    <h3 class="sub">There is no portal to shop</h3>
    <p class="lede">Where a Maryland employer can log into a state exchange and compare three carriers side by side, a Kentucky employer has to approach carriers individually or have a broker do it. That is not a disaster &mdash; it is how Texas and Florida employers have always bought &mdash; but it does mean nobody is assembling the comparison for you by default.</p>
    <h3 class="sub">The federal tax credit route is largely shut</h3>
    <p class="lede">The Small Business Health Care Tax Credit generally requires a qualified health plan bought through a SHOP marketplace. With no SHOP open to new business in Kentucky, that condition cannot be met by a new purchaser. IRS Notice 2018-27 offers relief to an employer that first claimed the credit for 2016 or later and is midway through its two consecutive credit years when QHPs are not available through SHOP in its county, and KHBE notes credits may be available for businesses that had SHOP coverage in tax year 2025 or 2026. If you are starting from scratch in Kentucky, build your budget without the credit and treat it as upside.</p>
    <p class="vs-ih-src">Source: <a href="https://khbe.ky.gov/Enrollment/Pages/SHOP.aspx" rel="nofollow noopener" target="_blank">Kentucky Health Benefit Exchange, SHOP</a> &middot; <a href="https://www.irs.gov/newsroom/small-business-health-care-tax-credit-questions-and-answers-who-gets-the-tax-credit" rel="nofollow noopener" target="_blank">IRS credit Q&amp;A</a></p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Kentucky needs two employees, not one</h2>
    <p class="lede">KRS 304.17A-005(44) defines a small employer as one that &ldquo;employed an average of at least two (2) but not more than fifty (50) employees on business days during the preceding calendar year and who employs at least two (2) employees on the first day of the plan year.&rdquo; Two independent tests. The federal default is one employee; Kentucky, like Texas, chose two.</p>
    <p class="lede">So a genuine one-person Kentucky business cannot buy small group coverage. The realistic options are individual coverage on kynect, or an ICHRA funded by a related entity. It is worth knowing before you shop, not after.</p>
    <p class="lede">Kentucky also declined the option to raise the small group ceiling to 100 employees, so the market runs 2 to 50 and a 51-employee Kentucky company is in the large group market with different rules and different pricing.</p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Kentucky&rsquo;s tobacco ceiling is lower than the federal one</h2>
    <div class="vs-ih-key">
      <strong>1.4 to 1, not 1.5 to 1.</strong>
      <p>Both CMS&rsquo;s market rating reforms table and the Kentucky Department of Insurance&rsquo;s own PPACA pre-emption chart publish Kentucky&rsquo;s maximum tobacco rating ratio as 1.4 to 1 in the individual and small group markets, against the federal maximum of 1.5 to 1. Kentucky is one of a short list of states below the federal ceiling. On age Kentucky uses the federal default: a 3 to 1 band and the federal standard age curve.</p>
    </div>
    <p class="lede">Beyond that, the permitted rating factors are the federal four and nothing else &mdash; individual versus family coverage, rating area, age, and tobacco use. Your industry, your injury rate and last year&rsquo;s claims are not permitted rating factors for a Kentucky group of 2 to 50. Owners in construction, manufacturing, trucking and agriculture routinely assume group health is priced the way workers&rsquo; comp is and never ask for a quote. It is not.</p>
    <p class="lede">One quirk worth knowing: Kentucky&rsquo;s guaranteed-issue right actually comes from federal law, not Kentucky law. KY DOI&rsquo;s own pre-emption chart says Kentucky is pre-empted on guaranteed availability &ldquo;because there is no statute regarding guaranteed availability.&rdquo; The old KRS 304.17A-200 minimum participation and contribution provisions are pre-empted too. That is why the federal November 15 to December 15 window is the operative escape hatch if your participation is tight.</p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Any willing provider: why narrow-network savings underdeliver here</h2>
    <p class="lede">KRS 304.17A-270 provides that a health insurer &ldquo;shall not discriminate against any provider who is located within the geographic coverage area of the health benefit plan and who is willing to meet the terms and conditions for participation established by the health insurer.&rdquo; Kentucky is one of a small number of states with a broad any-willing-provider law.</p>
    <p class="lede">For your employees, that is good news: Kentucky networks tend to be wider and harder to cut down than in neighbouring states, and the odds that a given doctor is in-network are better. For your budget, it means the deep discounts a national broker attaches to a narrow-network product usually do not appear in Kentucky, because the network cannot be narrowed the same way. If a Kentucky quote is priced off a network-restriction saving, ask what specifically is being excluded.</p>
    <p class="vs-ih-src">Source: <a href="https://apps.legislature.ky.gov/law/statutes/chapter.aspx?id=38715" rel="nofollow noopener" target="_blank">KRS chapter 304 subtitle 17A</a></p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Kentucky mini-COBRA: the obligation small employers miss</h2>
    <div class="vs-ih-key">
      <strong>Federal COBRA starts at 20 employees. Kentucky fills the gap below it, and a lot of two-to-nineteen employee groups do not know.</strong>
      <p>KRS 304.18-110 requires employers with fewer than 20 employees offering fully insured coverage to allow employees and dependents to extend group health coverage for <strong>18 months</strong> after the date it would otherwise have ended. KRS 304.18-114 separately provides conversion coverage. The Department of Insurance describes state continuation as providing protections similar to COBRA without duplicating it.</p>
      <p>It applies to insurance. A self-funded or level-funded arrangement is not insurance for this purpose and sits outside the requirement &mdash; which is a real consideration if you are weighing level-funded against fully insured in Kentucky.</p>
    </div>
    <h3 class="sub">Mandates that are unusual for a Kentucky plan</h3>
    <p class="lede">Kentucky caps cost sharing for covered prescription insulin at <strong>$30 per 30-day supply</strong> under KRS 304.17A-148, which is at the stricter end nationally, alongside broad diabetes equipment, supplies and self-management training. KRS 304.17A-129 mandates speech therapy for stuttering with no annual visit limit, no benefit cap and no prior authorisation, in person or by telehealth &mdash; a combination very few states require. Cochlear implants and hearing aids are separate express mandates. If you have a diabetic employee or a child in speech therapy, those are worth knowing about.</p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>Eight rating areas, and two metros that cross a state line</h2>
    <div class="vs-ih-scroll">
    <table class="vs-ih-tbl">
      <thead><tr><th>Area</th><th>Covers</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td><strong>3</strong> &mdash; Louisville</td><td>Jefferson, Bullitt, Oldham, Shelby, Hardin, Nelson and 10 more</td><td>Stops at the Indiana line; Clark and Floyd counties rate under Indiana</td></tr>
        <tr><td><strong>5</strong> &mdash; Lexington</td><td>Fayette, Scott, Jessamine, Madison, Woodford, Franklin and 15 more</td><td>Wide 21-county area covering the Bluegrass</td></tr>
        <tr><td><strong>6</strong> &mdash; Northern Kentucky</td><td>Boone, Kenton, Campbell, Gallatin, Grant, Pendleton</td><td>Smallest area in the state; the Ohio side of the Cincinnati metro rates under Ohio</td></tr>
        <tr><td><strong>4</strong> &mdash; Southern Kentucky</td><td>Warren, Barren, Pulaski, Logan, Hart and 15 more</td><td>Bowling Green does <em>not</em> get its own area</td></tr>
        <tr><td><strong>8</strong> &mdash; Southeastern Kentucky</td><td>Pike, Perry, Harlan, Letcher, Floyd, Knox, Whitley, Bell and 11 more</td><td>Appalachian Kentucky</td></tr>
        <tr><td><strong>1, 2, 7</strong></td><td>Western Kentucky, Owensboro, Northeastern Kentucky</td><td>Paducah, Owensboro and Henderson, Ashland and the Huntington side</td></tr>
      </tbody>
    </table>
    </div>
    <p class="lede">Rates follow the employer&rsquo;s rating area, which is why the two state-line metros need care. A Covington employer and a Cincinnati employer four miles apart face different rating areas, different mandated benefits and different continuation rules. Same for Louisville and southern Indiana. If your team is split across the river, the placement question is a real one and it is settled by carrier underwriting rather than by any Kentucky statute.</p>
    <p class="vs-ih-src">County assignments: <a href="https://www.cms.gov/cciio/programs-and-initiatives/health-insurance-market-reforms/ky-gra" rel="nofollow noopener" target="_blank">CMS Kentucky geographic rating areas</a></p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Three ways to cover a Kentucky team</h2>
    <div class="vs-ih-grid">
      <a class="vs-ih-card" href="/small-business-health-insurance">
        <strong>Traditional group plan</strong>
        <span>Fully insured, direct with a carrier or through a broker now that SHOP is closed. Simplest to run and the only route that carries Kentucky&rsquo;s state continuation protection.</span>
        <em>How group plans work &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/level-funded-health-insurance-florida">
        <strong>Level-funded</strong>
        <span>Often below fully insured for a healthier group, with a refund of unused claims at year end. Sits outside Kentucky&rsquo;s state continuation and mandated benefit rules, which cuts both ways.</span>
        <em>Compare level-funded &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/ichra-florida-small-business">
        <strong>ICHRA</strong>
        <span>Reimburse individual kynect premiums tax-free instead of running a group plan. The realistic route for a Kentucky business that cannot reach two employees.</span>
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
      <a class="vs-ih-card" href="/blog/how-many-employees-do-you-need-for-group-health-insurance"><strong>How many employees do you need?</strong><span>Florida, Texas, Maryland and Kentucky all answer this differently. Two of them are not 1&ndash;50.</span><em>Read the comparison &rarr;</em></a>
      <a class="vs-ih-card" href="/blog/small-business-health-care-tax-credit-2026"><strong>The tax credit in 2026</strong><span>Why the SHOP requirement now breaks in Kentucky, and what relief exists if you were already claiming it.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-ih-card" href="/blog/group-health-insurance-minimum-participation"><strong>Can&rsquo;t hit minimum participation?</strong><span>What counts as a waiver, and the November 15 to December 15 window that suspends the requirement.</span><em>Read the guide &rarr;</em></a>
      <a class="vs-ih-card" href="/group-health-insurance-by-industry"><strong>Group health by industry</strong><span>Ten trades, what each runs into, and the rating rules that apply to all of them.</span><em>Browse by trade &rarr;</em></a>
    </div>
  </div>
</section>

<section class="vs-ih-band">
  <div class="vs-ih-inner">
    <h2>Send us your headcount and we will price it</h2>
    <p>Employee count, ages and county is enough to start. With kynect&rsquo;s SHOP closed, somebody has to assemble the carrier comparison by hand &mdash; that is the job. Licensed in Kentucky and 40+ states, and free either way.</p>
    <p style="margin:0"><a class="vs-ih-cta" href="/quote?type=business" style="background:#fff;color:#0b2346">Get Kentucky group quotes &rarr;</a></p>
  </div>
</section>

'''

build('kentucky-small-business-health-insurance.html', URL, TITLE, DESC,
      'US-KY', 'Louisville', BODY, FAQ, SCHEMA)

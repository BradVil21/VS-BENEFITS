# -*- coding: utf-8 -*-
"""Build /tampa-small-business-health-insurance.
GSC: 'business health insurance tampa' pos 36.8 (40 impr), 'small business health
insurance tampa' 52.5 (25), 'small business benefits planning in tampa fl' 25.7 (10),
'st petersburg small business health insurance' 70.5 (8). No Tampa page exists today.

Written fresh rather than find/replaced off the Miami page - a templated sibling is
what got the dental-vision cluster 301'd."""
import re, json

SRC='health-insurance-for-hvac-companies.html'
OUT='tampa-small-business-health-insurance.html'
BASE='https://www.vshealthbenefits.com'
URL=BASE+'/tampa-small-business-health-insurance'
s=open(SRC,encoding='utf-8').read()
head_end=s.index('</head>'); hdr=s[s.index('<header'):s.index('</header>')+9]; tail=s[s.rindex('<footer'):]
h=s[:head_end]

TITLE="Group Health Insurance Tampa, FL | Small Business"
DESC=("Group health insurance for Tampa small businesses with 2 to 50 employees. Hillsborough County rates run "
      "below Miami-Dade for the same plan. Every major carrier compared free.")

h=re.sub(r'<title>.*?</title>','<title>%s</title>'%TITLE,h,flags=re.S)
h=re.sub(r'(<meta name="description" content=")(.*?)(")',lambda m:m.group(1)+DESC+m.group(3),h,count=1,flags=re.S)
h=re.sub(r'(<link rel="canonical" href=")(.*?)(")',lambda m:m.group(1)+URL+m.group(3),h,count=1)
for p,v in [('og:title',TITLE),('og:description',DESC),('og:url',URL)]:
    h=re.sub(r'(<meta property="%s" content=")(.*?)(")'%re.escape(p),lambda m,v=v:m.group(1)+v+m.group(3),h,count=1,flags=re.S)
for n,v in [('twitter:title',TITLE),('twitter:description',DESC)]:
    h=re.sub(r'(<meta name="%s" content=")(.*?)(")'%re.escape(n),lambda m,v=v:m.group(1)+v+m.group(3),h,count=1,flags=re.S)
h=re.sub(r'<meta name="geo.placename" content="[^"]*"','<meta name="geo.placename" content="Tampa"',h)
# drop the source page's page-level schema
spans=[]
for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',h,re.S):
    try: d=json.loads(m.group(1))
    except Exception: continue
    if d.get('@type') in ('FAQPage','Article','Service','BreadcrumbList','WebPage'): spans.append((m.start(),m.end()))
for a,b in reversed(spans): h=h[:a]+h[b:]

FAQ=[
 ("How much does small business health insurance cost in Tampa?",
  "Budget roughly $350 to $650 per employee per month for an employee-only group plan in 2027, usually split between employer and employee. Hillsborough County sits in the middle of Florida's range rather than the top, so the same plan generally prices below what a Miami-Dade employer pays for it."),
 ("Why is group health cheaper in Tampa than in Miami?",
  "Premiums are set by geographic rating area, and Florida's areas are county-based. Across Florida the spread from the cheapest county to the most expensive runs roughly 40 to 60 percent for comparable coverage. Miami-Dade sits at the high end of that range and Hillsborough is mid-range, so a Tampa employer typically pays less than a Miami employer for the same plan and the same employee ages."),
 ("How many employees do I need for a group plan in Tampa?",
  "Florida's small-group market covers employers with 1 to 50 employees, so you can set up a group plan with as few as one W-2 employee besides the owner. Carriers generally require a minimum share of eligible employees to participate and that the employer contribute at least half of the employee-only premium."),
 ("Do you cover St. Petersburg, Clearwater and the rest of Tampa Bay?",
  "Yes. We write group coverage across Hillsborough, Pinellas, Pasco and Hernando counties, which covers Tampa, St. Petersburg, Clearwater, Brandon, Riverview and the surrounding area. Note that Pinellas and Hillsborough can price differently, so a team split across the bay is worth modelling before you commit."),
 ("Am I required to offer health insurance to my Tampa employees?",
  "Only if you average 50 or more full-time equivalent employees. Below that threshold there is no federal mandate and Florida has no state employer mandate. Most Tampa small employers offer coverage for hiring and retention reasons, not because they have to."),
 ("Does my industry change what I pay?",
  "No. For a group of 1 to 50, the ACA allows premiums to vary only by employee age, geographic rating area, family size, tobacco use and the plan selected. Industry, injury rate and prior claims are not permitted rating factors. That is the opposite of workers' compensation."),
 ("What does it cost to work with a broker?",
  "Nothing. Carriers pay our commission, and it is built into the premium whether you use a broker or not. You pay the same rate going direct, so you may as well have someone shop the market and handle the paperwork."),
]
faq_html=''.join('\n        <div class="vs-ih-faq"><h3>%s</h3><p>%s</p></div>'%(q,a) for q,a in FAQ)

STYLE='''<style id="vs-tpa-style">
.vs-ih{padding:52px 0}
.vs-ih .vs-ih-inner{width:100%;max-width:1160px;margin:0 auto;padding:0 18px}
.vs-ih h2{font-family:'Poppins','Inter',system-ui,sans-serif;color:#0b2346;font-size:1.55rem;margin:0 0 10px;line-height:1.25}
.vs-ih h3.sub{font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1.08rem;margin:26px 0 8px}
.vs-ih p.lede{color:#3d4c5f;font-size:1.02rem;line-height:1.7;max-width:800px;margin:0 0 22px}
.vs-ih-key{background:#f2f7fd;border:1px solid #d6e6f7;border-left:4px solid #16447f;border-radius:12px;padding:20px 22px;margin:0 0 28px;max-width:880px}
.vs-ih-key strong{display:block;color:#0b2346;font-size:1.04rem;margin-bottom:6px}
.vs-ih-key p{margin:0;color:#3d4c5f;font-size:.97rem;line-height:1.68}
.vs-ih-grid{display:grid;grid-template-columns:1fr;gap:14px}
.vs-ih-card{display:block;background:#fff;border:1px solid #e4e9f2;border-radius:14px;padding:19px 21px;text-decoration:none}
.vs-ih-card strong{display:block;font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1.02rem;margin-bottom:6px}
.vs-ih-card span{display:block;color:#5a6b80;font-size:.91rem;line-height:1.6}
a.vs-ih-card:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(13,27,42,.09);text-decoration:none}
.vs-ih-card em{display:inline-block;margin-top:9px;color:#16447f;font-weight:700;font-size:.85rem;font-style:normal}
.vs-ih-faq{border-bottom:1px solid #eceff4;padding:16px 0}
.vs-ih-faq:last-child{border-bottom:0}
.vs-ih-faq h3{font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1.02rem;margin:0 0 6px}
.vs-ih-faq p{margin:0;color:#4a5a6e;font-size:.95rem;line-height:1.68}
.vs-ih-cta{display:inline-block;background:#16447f;color:#fff;font-weight:700;font-size:1rem;padding:15px 32px;border-radius:999px;text-decoration:none}
.vs-ih-cta:hover{background:#0e3266;color:#fff;text-decoration:none}
.vs-ih-band{background:#0b2346;color:#fff;padding:44px 0}
.vs-ih-band h2{color:#fff}.vs-ih-band p{color:#c9d4e2;max-width:660px;margin:0 0 20px;line-height:1.65}
.vs-ih-panel{background:#fff;border:1px solid #e4e9f2;border-radius:16px;padding:24px 26px;box-shadow:0 10px 30px rgba(13,27,42,.07)}
.vs-ih-dl>div{display:flex;justify-content:space-between;gap:16px;padding:9px 0;border-bottom:1px solid #f0f2f6}
.vs-ih-dl>div:last-child{border-bottom:0}
.vs-ih-dl dt{color:#7a8798;font-size:.83rem;font-weight:600;margin:0;flex:0 0 40%}
.vs-ih-dl dd{color:#0b2346;font-size:.88rem;font-weight:600;margin:0;text-align:right;line-height:1.4}
@media(min-width:760px){.vs-ih-grid{grid-template-columns:1fr 1fr}}
</style>'''

CITIES=['Tampa','St. Petersburg','Clearwater','Brandon','Riverview','Wesley Chapel','Plant City','Largo']
SCHEMA=[
 {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},
  {"@type":"ListItem","position":2,"name":"Florida Small Business Health Insurance","item":BASE+"/florida-small-business-health-insurance"},
  {"@type":"ListItem","position":3,"name":"Tampa"}]},
 {"@context":"https://schema.org","@type":"Service",
  "serviceType":"Group health insurance for Tampa small business",
  "name":"Group Health Insurance for Tampa Small Business","url":URL,
  "provider":{"@type":"InsuranceAgency","name":"VS Health Benefits","url":BASE+"/",
    "telephone":"+1-954-825-1009","email":"info@vshealthbenefits.com",
    "address":{"@type":"PostalAddress","addressLocality":"Miami","addressRegion":"FL","addressCountry":"US"}},
  "areaServed":[{"@type":"City","name":c,"addressRegion":"FL"} for c in CITIES]
    +[{"@type":"AdministrativeArea","name":"Hillsborough County"},
      {"@type":"AdministrativeArea","name":"Pinellas County"},
      {"@type":"AdministrativeArea","name":"Pasco County"},
      {"@type":"State","name":"Florida"}],
  "audience":{"@type":"BusinessAudience","name":"Tampa Bay small businesses with 1-50 employees",
    "numberOfEmployees":{"@type":"QuantitativeValue","minValue":1,"maxValue":50}},
  "offers":{"@type":"Offer","price":"0","priceCurrency":"USD",
    "description":"Free group health comparison and setup; carriers pay the broker commission."},
  "availableChannel":{"@type":"ServiceChannel","serviceUrl":BASE+"/quote?type=business",
    "servicePhone":{"@type":"ContactPoint","telephone":"+1-954-825-1009"}}},
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
]
schema_html=''.join('<script type="application/ld+json">\n%s\n</script>\n'%json.dumps(x,indent=2) for x in SCHEMA)

BODY='''<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Group Health Insurance &middot; Tampa, FL</span>
        <h1>Group health insurance for <span>Tampa small business</span></h1>
        <p class="hero-sub">Plans for teams of 2 to 50 across Hillsborough, Pinellas and Pasco. We compare every carrier writing in Tampa Bay, handle the setup, and it costs you nothing &mdash; carriers pay our commission either way.</p>
        <p><a class="vs-ih-cta" href="/quote?type=business">Get group quotes for your team &rarr;</a></p>
      </div>
      <div>
        <div class="vs-ih-panel">
          <h2 style="font-size:1.05rem;margin:0 0 14px">Tampa group coverage at a glance</h2>
          <dl class="vs-ih-dl">
            <div><dt>Group size</dt><dd>1 to 50 employees</dd></div>
            <div><dt>Typical cost</dt><dd>$350&ndash;$650 per employee / month</dd></div>
            <div><dt>County rating</dt><dd>Hillsborough is mid-range for Florida</dd></div>
            <div><dt>Employer share</dt><dd>Usually 50%+ of employee-only</dd></div>
            <div><dt>Counties served</dt><dd>Hillsborough, Pinellas, Pasco, Hernando</dd></div>
            <div><dt>Our fee</dt><dd>$0 &mdash; carriers pay the commission</dd></div>
          </dl>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Tampa employers pay less than Miami employers for the same plan</h2>
    <div class="vs-ih-key">
      <strong>Where your business sits changes the price more than what your business does.</strong>
      <p>Health premiums are set by geographic rating area, and Florida&rsquo;s are county-based. Across the state the gap between the cheapest county and the most expensive runs roughly 40 to 60 percent for comparable coverage. Miami-Dade sits at the high end of that range; Hillsborough is mid-range. Same carrier, same plan, same employee ages &mdash; a Tampa group generally prices below a Miami one. If you have been quoted using South Florida numbers, or you moved a team up from Miami, your real Tampa number is probably lower than you have been told.</p>
    </div>
    <p class="lede">The flip side is that a team split across the bay is not one price. Hillsborough and Pinellas are rated separately, so a company with an office in Tampa and a second in St. Petersburg can see different per-employee costs for identical coverage. It is worth modelling before you sign, not after.</p>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>What Tampa Bay employers actually run into</h2>
    <p class="lede">The industries here create specific problems, and they are not the same ones South Florida has.</p>
    <div class="vs-ih-grid">
      <div class="vs-ih-card">
        <strong>Healthcare and clinical employers</strong>
        <span>A dense provider market is good news: network breadth is rarely the constraint in Hillsborough the way it is in parts of Miami-Dade. The harder question is usually covering clinical staff competitively when large hospital systems are hiring against you.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Port, logistics and distribution</strong>
        <span>Warehouse and drayage operations run variable hours and seasonal peaks. Waiting periods and a measurement period for variable-hour staff are what keep you from enrolling and terminating people every month.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Hospitality and food service</strong>
        <span>Tipped wages, high turnover and part-time staff. Employees averaging under 30 hours generally do not have to be offered coverage, and the ACA lookback lets you measure over a period instead of guessing.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Construction and the trades</strong>
        <span>Mixed W-2 and 1099 crews, seasonal headcount, and public work with prevailing-wage fringe obligations. Your trade does not raise your health premium &mdash; that is workers&rsquo; comp, not health.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Professional services and finance</strong>
        <span>Small, stable, mostly full-time teams. Usually the most straightforward group case, and often a strong candidate for a level-funded plan that refunds unused claims.</span>
      </div>
      <div class="vs-ih-card">
        <strong>Teams split across the bay</strong>
        <span>Hillsborough, Pinellas and Pasco price separately. Participation is measured across the whole group rather than per location, which usually works in your favour.</span>
      </div>
    </div>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Three ways to cover a Tampa team</h2>
    <div class="vs-ih-grid">
      <a class="vs-ih-card" href="/small-business-health-insurance">
        <strong>Traditional group plan</strong>
        <span>Fully insured, simplest to run, predictable renewal. Carriers want minimum participation and at least half the employee-only premium from you.</span>
        <em>How group plans work &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/level-funded-health-insurance-florida">
        <strong>Level-funded</strong>
        <span>Often 10 to 30 percent under fully insured for a healthier group, with a refund of unused claims at the end of the year. Suits stable, younger teams.</span>
        <em>Compare level-funded &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/ichra-florida-small-business">
        <strong>ICHRA</strong>
        <span>Reimburse individual premiums tax-free instead of running a group plan. Caps your cost, hands employees the choice, and reaches 1099 people a group plan cannot.</span>
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
    <h2>Benefits planning for a Tampa small business</h2>
    <p class="lede">Most owners come to this with one question &mdash; what will it cost &mdash; and leave with four decisions. Here is the order they actually come in:</p>
    <h3 class="sub">1. Who is eligible</h3>
    <p class="lede">W-2 employees only, and only those meeting your hours threshold. 1099 contractors cannot go on a group plan, whatever you call them internally. Getting this wrong is the most common reason an application comes back.</p>
    <h3 class="sub">2. How much you contribute</h3>
    <p class="lede">Carriers typically require at least 50 percent of the employee-only premium. Going above that improves participation, which in turn keeps the plan viable and can widen the plan options available to you.</p>
    <h3 class="sub">3. Which network</h3>
    <p class="lede">Check your people&rsquo;s actual doctors by name in the plan&rsquo;s own directory. Tampa Bay has good provider density, but plan names still oversell network breadth, and a narrow network discovered in February is an expensive surprise.</p>
    <h3 class="sub">4. When you start</h3>
    <p class="lede">Group coverage is not tied to the ACA open enrollment calendar &mdash; a small business can start a plan in any month. Your renewal date then becomes your annual decision point. <a href="/business-open-enrollment-faq">More on employer timing &rarr;</a></p>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Frequently asked</h2>__FAQ__
  </div>
</section>

<section class="vs-ih-band">
  <div class="vs-ih-inner">
    <h2>Send us your headcount and we will price it</h2>
    <p>Employee count and ages is enough to start. We come back with real numbers from every carrier writing in Hillsborough and Pinellas &mdash; not a range, your range. Licensed in Florida and 40+ states, bilingual, and free either way.</p>
    <p style="margin:0"><a class="vs-ih-cta" href="/quote?type=business" style="background:#fff;color:#0b2346">Get Tampa group quotes &rarr;</a></p>
  </div>
</section>

'''.replace('__FAQ__', faq_html)

out=h+STYLE+'\n'+schema_html+'</head>\n<body>\n'+hdr+'\n'+BODY+tail
open(OUT,'w',encoding='utf-8').write(out)
print('wrote %s (%d bytes)'%(OUT,len(out)))

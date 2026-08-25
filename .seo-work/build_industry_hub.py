# -*- coding: utf-8 -*-
"""Build /group-health-insurance-by-industry: the vertical hub for the
"group health insurance for [trade]" cluster (~420 impressions, positions 19-41,
zero clicks, no matching page today). Reuses the site shell from an existing page."""
import re, json

SRC='health-insurance-for-hvac-companies.html'
OUT='group-health-insurance-by-industry.html'
BASE='https://www.vshealthbenefits.com'
URL=BASE+'/group-health-insurance-by-industry'
s=open(SRC,encoding='utf-8').read()

head_end = s.index('</head>')
hdr_start= s.index('<header')
hdr_end  = s.index('</header>')+len('</header>')
foot_start=s.rindex('<footer')

HEAD_RAW = s[:head_end]
HEADER   = s[hdr_start:hdr_end]
TAIL     = s[foot_start:]

TITLE="Group Health Insurance by Industry | Small Business"
DESC=("Group health insurance for contractors, janitorial, retail, restaurants, trucking, HVAC, dental and salons. "
      "What changes by trade, what does not, and real 2027 per-employee costs.")

# --- rebuild <head>: strip source-specific tags, keep the shared assets ---
h = HEAD_RAW
h = re.sub(r'<title>.*?</title>', '<title>%s</title>'%TITLE, h, flags=re.S)
h = re.sub(r'(<meta name="description" content=")(.*?)(")', lambda m: m.group(1)+DESC+m.group(3), h, count=1, flags=re.S)
h = re.sub(r'(<link rel="canonical" href=")(.*?)(")', lambda m: m.group(1)+URL+m.group(3), h, count=1)
for prop,val in [('og:title',TITLE),('og:description',DESC),('og:url',URL)]:
    h = re.sub(r'(<meta property="%s" content=")(.*?)(")'%re.escape(prop), lambda m,v=val: m.group(1)+v+m.group(3), h, count=1, flags=re.S)
for nm,val in [('twitter:title',TITLE),('twitter:description',DESC)]:
    h = re.sub(r'(<meta name="%s" content=")(.*?)(")'%re.escape(nm), lambda m,v=val: m.group(1)+v+m.group(3), h, count=1, flags=re.S)
# drop the source page's FAQPage / Article / Service schema; keep org + styles
def drop_schema(html):
    out=[]; pos=0
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try: d=json.loads(m.group(1))
        except Exception: continue
        t=d.get('@type')
        if t in ('FAQPage','Article','Service','BreadcrumbList','WebPage'):
            out.append((m.start(),m.end()))
    for a,b in reversed(out): html = html[:a]+html[b:]
    return html
h = drop_schema(h)

TRADES=[
 ('/health-insurance-for-construction-companies','Construction contractors',
  'General, excavation, bridge and tunneling. Mixed W-2 and 1099 crews, seasonal headcount, and the Davis-Bacon fringe credit on public work.'),
 ('/health-insurance-for-cleaning-companies','Janitorial and cleaning',
  'High turnover and variable hours are the real problem, not price. Waiting periods and the ACA lookback are what make these groups workable.'),
 ('/health-insurance-for-trucking-companies','Trucking companies and fleets',
  'Reefer, flatbed, dump, oilfield and drayage. For long-haul the network matters more than the premium.'),
 ('/health-insurance-for-retail-businesses','Retail stores and chains',
  'Single store or twelve. Rating areas follow each employee ZIP, and participation is measured across the whole group.'),
 ('/health-insurance-for-restaurants','Restaurants and food service',
  'Tipped wages, part-time rules and the ACA lookback, plus what turnover really does to your renewal.'),
 ('/health-insurance-for-hvac-companies','HVAC companies',
  'Roughly $350 to $650 per employee per month. Certified techs are the hardest hires in the trades to keep.'),
 ('/health-insurance-for-auto-repair-shops','Auto repair shops',
  'A physical trade with a small W-2 crew. Usually a straightforward group case once eligibility is set.'),
 ('/health-insurance-for-dental-offices','Dental offices and practices',
  'Small teams, owner-dentist options, and how to cover an associate without blowing the budget.'),
 ('/health-insurance-for-salons-and-spas','Salons, spas and barbershops',
  'Booth renters, commission stylists and W-2 staff each need a different answer. Often not a group plan at all.'),
 ('/health-insurance-for-real-estate-agents','Real estate brokerages',
  'Agents are 1099, so a group plan usually is not the answer. Subsidies on net commission income often are.'),
]

cards=''.join(
 '\n        <a class="vs-ih-card" href="%s">\n          <strong>%s</strong>\n          <span>%s</span>\n'
 '          <em>See plans and costs &rarr;</em>\n        </a>'%(u,t,b) for u,t,b in TRADES)

FAQ=[
 ("Does my industry affect my group health insurance premium?",
  "No. For a group of 1 to 50 employees, the ACA allows premiums to vary only by employee age, geographic rating area, family size, tobacco use and the plan selected. Industry, injury rate and prior claims are not permitted rating factors. This is the opposite of workers' compensation, which is priced on your class code and claims history."),
 ("How much does group health insurance cost per employee?",
  "In 2027 a typical employee-only group plan runs roughly $350 to $650 per month, usually split between employer and employee. Level-funded plans often come in 10 to 30 percent below that for a healthier group. Your actual number depends on the ages of your team, your county and the plan you choose."),
 ("How many employees do I need to offer a group plan?",
  "In Florida the small-group market covers employers with 1 to 50 employees, so you can set up a group plan with as few as one W-2 employee besides the owner. Carriers generally require that a minimum share of eligible employees participate and that the employer contribute at least half of the employee-only premium."),
 ("Can I cover 1099 subcontractors on my group plan?",
  "No. Group plans cover W-2 employees. 1099 subcontractors buy individual coverage, though they can deduct premiums against net self-employment income. Some employers use an ICHRA to reimburse individual premiums tax-free instead, which reaches people a group plan cannot."),
 ("Do health insurance contributions count toward Davis-Bacon fringe requirements?",
  "Yes. Bona fide health insurance contributions count toward the fringe obligation on federally funded work rather than being paid out as cash. Credit is subject to annualization, meaning it is based on the effective annual rate of contributions across all hours worked, both Davis-Bacon and non-Davis-Bacon."),
 ("Am I required to offer health insurance to my employees?",
  "Only if you average 50 or more full-time equivalent employees. Below that threshold there is no federal mandate and no Florida state mandate. Most small employers offer coverage because of hiring and retention, not because they have to."),
]
faq_html=''.join('\n        <div class="vs-ih-faq"><h3>%s</h3><p>%s</p></div>'%(q,a) for q,a in FAQ)

STYLE='''<style id="vs-ih-style">
.vs-ih{padding:52px 0}
.vs-ih .vs-ih-inner{width:100%;max-width:1160px;margin:0 auto;padding:0 18px}
.vs-ih h2{font-family:'Poppins','Inter',system-ui,sans-serif;color:#0b2346;font-size:1.55rem;margin:0 0 10px;line-height:1.25}
.vs-ih p.lede{color:#3d4c5f;font-size:1.02rem;line-height:1.7;max-width:780px;margin:0 0 26px}
.vs-ih-key{background:#f2f7fd;border:1px solid #d6e6f7;border-left:4px solid #16447f;border-radius:12px;padding:20px 22px;margin:0 0 30px;max-width:860px}
.vs-ih-key strong{display:block;color:#0b2346;font-size:1.04rem;margin-bottom:6px}
.vs-ih-key p{margin:0;color:#3d4c5f;font-size:.97rem;line-height:1.68}
.vs-ih-grid{display:grid;grid-template-columns:1fr;gap:14px}
.vs-ih-card{display:block;background:#fff;border:1px solid #e4e9f2;border-radius:14px;padding:19px 21px;text-decoration:none;transition:transform .2s,box-shadow .2s}
.vs-ih-card:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(13,27,42,.09);text-decoration:none}
.vs-ih-card strong{display:block;font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1.04rem;margin-bottom:6px}
.vs-ih-card span{display:block;color:#5a6b80;font-size:.9rem;line-height:1.58}
.vs-ih-card em{display:inline-block;margin-top:9px;color:#16447f;font-weight:700;font-size:.85rem;font-style:normal}
.vs-ih-faq{border-bottom:1px solid #eceff4;padding:16px 0}
.vs-ih-faq:last-child{border-bottom:0}
.vs-ih-faq h3{font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1.02rem;margin:0 0 6px}
.vs-ih-faq p{margin:0;color:#4a5a6e;font-size:.95rem;line-height:1.68}
.vs-ih-cta{display:inline-block;background:#16447f;color:#fff;font-weight:700;font-size:1rem;padding:15px 32px;border-radius:999px;text-decoration:none}
.vs-ih-cta:hover{background:#0e3266;color:#fff;text-decoration:none}
.vs-ih-band{background:#0b2346;color:#fff;padding:42px 0;margin-top:8px}
.vs-ih-band h2{color:#fff}
.vs-ih-band p{color:#c9d4e2;max-width:640px;margin:0 0 20px;line-height:1.65}
@media(min-width:760px){.vs-ih-grid{grid-template-columns:1fr 1fr}}
</style>'''

SCHEMA=[
 {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
   {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},
   {"@type":"ListItem","position":2,"name":"Small Business Health Insurance","item":BASE+"/small-business-health-insurance"},
   {"@type":"ListItem","position":3,"name":"Group Health Insurance by Industry"}]},
 {"@context":"https://schema.org","@type":"Service","serviceType":"Group health insurance brokerage",
  "name":"Group Health Insurance by Industry","url":URL,
  "provider":{"@type":"InsuranceAgency","name":"VS Health Benefits","url":BASE+"/",
              "telephone":"+1-954-825-1009","areaServed":[{"@type":"State","name":"Florida"},{"@type":"Country","name":"United States"}]},
  "audience":{"@type":"BusinessAudience","name":"Small businesses with 1-50 employees"},
  "offers":{"@type":"Offer","price":"0","priceCurrency":"USD",
            "description":"Free group health insurance comparison and setup; carriers pay the broker commission."}},
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
   {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
]
schema_html=''.join('<script type="application/ld+json">\n%s\n</script>\n'%json.dumps(x,indent=2) for x in SCHEMA)

BODY = '''<section class="hero">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow">Group Health Insurance by Industry</span>
        <h1>Group health insurance, <span>by what you actually do</span></h1>
        <p class="hero-sub">Contractors, janitorial crews, fleets, restaurants, retail floors and clinics all buy the same product and run into completely different problems doing it. Pick your trade below, or start with the thing most owners get wrong.</p>
        <p><a class="vs-ih-cta" href="/quote?type=business">Get group quotes for your team &rarr;</a></p>
      </div>
    </div>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>The thing most owners get wrong</h2>
    <div class="vs-ih-key">
      <strong>Your trade does not raise your health premium.</strong>
      <p>Owners in high-hazard trades routinely assume group health is priced out of reach for them, because that is exactly how workers&rsquo; compensation works &mdash; class code, claims history, experience mod. Small-group health insurance does not work that way. Under the ACA, a plan for a group of 1 to 50 in Florida can be priced on five things only: employee age, geographic rating area, family size, tobacco use, and the plan selected. Industry, injury rate and prior claims are not permitted rating factors. An excavation crew and an accounting office of the same ages in the same county pay the same rate for the same plan.</p>
    </div>
    <p class="lede">What genuinely does change by trade is <strong>eligibility</strong> &mdash; who counts, when they count, and how you handle people who are not W-2. That is where the money and the compliance risk actually sit, and it is what each page below covers.</p>

    <h2>Find your trade</h2>
    <div class="vs-ih-grid">%s
    </div>
  </div>
</section>

<section class="vs-ih" style="background:#f7faff;border-top:1px solid #e4e9f2">
  <div class="vs-ih-inner">
    <h2>What changes by trade, and what does not</h2>
    <p class="lede">Four questions decide almost every small-group design, whatever the industry:</p>
    <div class="vs-ih-grid">
      <a class="vs-ih-card" href="/small-business-health-insurance-calculator">
        <strong>1. What will it cost per employee?</strong>
        <span>Roughly $350 to $650 a month for employee-only in 2027, usually split with the employee. Level-funded often lands 10 to 30 percent under that for a healthier group. Run your own numbers first.</span>
        <em>Open the calculator &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/florida-small-business-health-insurance-requirements">
        <strong>2. Am I required to offer anything?</strong>
        <span>Only at 50 or more full-time equivalents. Below that there is no federal mandate and no Florida mandate &mdash; but common ownership across entities can push you over the line without you noticing.</span>
        <em>Check the threshold &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/ichra-florida-small-business">
        <strong>3. What about my 1099 people?</strong>
        <span>Group plans cover W-2 employees only. An ICHRA reimburses individual premiums tax-free instead, which reaches subs, leased operators and booth renters a group plan cannot.</span>
        <em>How ICHRA works &rarr;</em>
      </a>
      <a class="vs-ih-card" href="/level-funded-health-insurance-florida">
        <strong>4. Group, level-funded or ICHRA?</strong>
        <span>Fully insured is simplest. Level-funded can refund unused claims if your group runs healthy. ICHRA hands the choice to employees and caps your cost. They suit different teams.</span>
        <em>Compare the three &rarr;</em>
      </a>
    </div>
  </div>
</section>

<section class="vs-ih">
  <div class="vs-ih-inner">
    <h2>Frequently asked</h2>%s
  </div>
</section>

<section class="vs-ih-band">
  <div class="vs-ih-inner">
    <h2>Tell us your headcount and we will price it</h2>
    <p>Send your employee count and ages and we come back with real numbers from every major carrier &mdash; not a range, your range. Carriers pay our commission, so this costs you nothing either way. Licensed in 40+ states, based in Miami, bilingual.</p>
    <p style="margin:0"><a class="vs-ih-cta" href="/quote?type=business" style="background:#fff;color:#0b2346">Get group quotes &rarr;</a></p>
  </div>
</section>

''' % (cards, faq_html)

out = h + STYLE + '\n' + schema_html + '</head>\n<body>\n' + HEADER + '\n' + BODY + TAIL
# body tag may already exist in the source head slice; make sure only one
out = re.sub(r'(<body[^>]*>)(?=.*<body)', '', out, count=1, flags=re.S)
open(OUT,'w',encoding='utf-8').write(out)
print('wrote %s (%d bytes)'%(OUT,len(out)))

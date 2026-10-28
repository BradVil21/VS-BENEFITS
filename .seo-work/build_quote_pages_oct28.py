"""2026-10-28: SEO for the two quote landing pages. Keeps hero/form untouched; adds content below reviews.
Usage: python3 .seo-work/build_quote_pages_oct28.py [--apply]"""
import re,os,sys,json,html
APPLY='--apply' in sys.argv
os.chdir(os.path.expanduser('~/mnt/VS-BENEFITS'))
CSS = """
/* quote-page info (2026-10-28) */
.lp-info{padding:46px 0 10px}
.lp-info .wrap{max-width:820px}
.lp-info h2{text-align:center;font-size:clamp(1.45rem,3.4vw,2rem);font-weight:700;margin:0 0 18px}
.lp-info h3{font-size:1.08rem;margin:0 0 4px}
.lp-info p,.lp-info li{color:#33404d;font-size:1.02rem}
.lp-info a{color:var(--blue-d);font-weight:600}
.lp-steps{list-style:none;padding:0;margin:0 0 34px;display:grid;gap:14px;counter-reset:s}
.lp-steps li{counter-increment:s;position:relative;padding:16px 18px 16px 62px;border:1px solid var(--line);border-radius:16px;background:#fff}
.lp-steps li::before{content:counter(s);position:absolute;left:18px;top:16px;width:30px;height:30px;border-radius:50%;background:var(--navy);color:#fff;font-weight:700;display:grid;place-items:center;font-family:'Poppins',sans-serif}
.lp-steps p{margin:0}
.lp-list{padding-left:20px;margin:0 0 34px}
.lp-list li{margin:0 0 8px}
.lp-who{display:grid;gap:14px;margin:0 0 34px}
@media(min-width:760px){.lp-who{grid-template-columns:repeat(3,1fr)}}
.lp-who div{background:var(--soft);border-radius:16px;padding:18px}
.lp-who p{margin:0;font-size:.97rem}
.lp-faq{margin:0 0 30px}
.lp-faq details{border-bottom:1px solid var(--line);padding:14px 2px}
.lp-faq summary{cursor:pointer;font-weight:700;color:var(--navy);font-size:1.03rem;list-style:none;display:flex;justify-content:space-between;gap:12px}
.lp-faq summary::-webkit-details-marker{display:none}
.lp-faq summary::after{content:"+";font-size:1.3rem;line-height:1;color:var(--blue-d)}
.lp-faq details[open] summary::after{content:"\\2212"}
.lp-faq details p{margin:10px 0 0}
"""
ORG={"@type":"InsuranceAgency","name":"VS Health Benefits","legalName":"VS BENEFITS LLC","url":"https://www.vshealthbenefits.com/","telephone":"+1-954-825-1009"}

def faq_html(faqs):
    return '<div class="lp-faq">'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs)+'</div>'
def strip(s): return html.unescape(re.sub(r'<[^>]+>','',s))
def schema(url,name,desc,service_type,crumbs,faqs):
    g=[{"@type":"Service","@id":url+"#service","name":name,"description":desc,"serviceType":service_type,"provider":ORG,
        "areaServed":{"@type":"Country","name":"United States"},"url":url,
        "offers":{"@type":"Offer","price":"0","priceCurrency":"USD","description":"Free quote, no obligation"}},
       {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":"https://www.vshealthbenefits.com"+p} for i,(n,p) in enumerate(crumbs)]},
       {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":strip(q),"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in faqs]}]
    return '<script type="application/ld+json">\n'+json.dumps({"@context":"https://schema.org","@graph":g},indent=1,ensure_ascii=False)+'\n</script>\n'

PAGES={
'trucking-health-quote.html':dict(
 url="https://www.vshealthbenefits.com/trucking-health-quote",
 title="Health Insurance Quotes for Truck Drivers (Free, 2027)",
 desc="Free health insurance quotes for truck drivers, owner-operators and trucking companies. A licensed advisor checks plans that work on the road.",
 h1_old="Health Insurance for Truckers", h1="Health Insurance Quotes for Truck Drivers",
 service="Health insurance quotes for truck drivers", stype="Health insurance brokerage",
 crumbs=[("Home","/"),("Truck driver health insurance","/truck-driver-health-insurance"),("Quotes","/trucking-health-quote")],
 body="""
  <h2>How truck driver health insurance quotes work</h2>
  <ol class="lp-steps">
    <li><h3>Enter your home ZIP</h3><p>Health plans are priced by where you live, not where you park the truck. Your home ZIP decides which plans and prices you can get.</p></li>
    <li><h3>Answer a few quick questions</h3><p>Who needs coverage and their ages, whether anyone uses tobacco, and your estimated household income. For owner-operators that is net profit after truck expenses, not gross revenue.</p></li>
    <li><h3>A licensed advisor checks your quote</h3><p>We compare plans side by side, check that your doctors and prescriptions are covered, and look for networks that work across state lines. We reach out within 1 business day, often within hours.</p></li>
  </ol>
  <h2>What sets the price of your quote</h2>
  <ul class="lp-list">
    <li><strong>Home ZIP and age.</strong> Under ACA rules these two drive most of the price. Your health history does not.</li>
    <li><strong>Income.</strong> Marketplace tax credits are based on household income. Above 400% of the poverty level (about $63,840 for a single driver on 2027 coverage) most people lose the credit, so a good mileage year can change your price. Try the <a href="/owner-operator-subsidy-cliff-calculator">owner-operator subsidy cliff calculator</a>.</li>
    <li><strong>Network.</strong> A <a href="/nationwide-ppo-health-insurance-truck-drivers">nationwide PPO</a> usually costs more than a local HMO, but it lets you see doctors in other states.</li>
    <li><strong>Plan level and tobacco.</strong> Bronze, silver and gold trade a lower premium for a higher deductible, and tobacco use can add a surcharge.</li>
  </ul>
  <p style="margin-top:-18px;margin-bottom:34px">See typical prices in our guide to <a href="/truck-driver-health-insurance-cost">truck driver health insurance cost</a>.</p>
  <h2>Quotes for every kind of driver</h2>
  <div class="lp-who">
    <div><h3>Owner-operators and 1099 drivers</h3><p>Individual and family plans, with ACA tax credits if you qualify. Premiums are often deductible for self-employed drivers. <a href="/best-health-insurance-owner-operators">Owner-operator plans</a></p></div>
    <div><h3>Company drivers</h3><p>Compare your carrier's plan with Marketplace options, or cover the waiting period when you switch carriers. <a href="/blog/switching-trucking-companies-health-insurance">Switching carriers</a></p></div>
    <div><h3>Trucking companies</h3><p>Group health plans for fleets from 2 employees, with coverage that can start on the 1st of any month. <a href="/health-insurance-for-trucking-companies">Fleet group plans</a></p></div>
  </div>
  <h2>Truck driver quote FAQ</h2>
""",
 faqs=[
  ("How long does a truck driver health insurance quote take?","The online form takes about a minute. A licensed advisor follows up within 1 business day, often within hours, by call or text, whichever works from the road."),
  ("Does a quote cost anything or commit me to a plan?","No. Quotes are free and there is no obligation. Insurance companies pay us, and you pay the same premium you would pay buying the plan yourself."),
  ("Can I get a quote outside open enrollment?","Yes. For 2027 coverage, open enrollment runs November 1 to January 15 in most states, and you need to enroll by December 15 for coverage that starts January 1. Outside that window you need a qualifying life event, such as losing coverage when you leave a carrier. See the <a href=\"/truck-driver-open-enrollment-2027\">2027 open enrollment guide for drivers</a>."),
  ("Will my plan work when I'm on the road in another state?","Emergency care is covered at in-network cost sharing anywhere in the U.S. under ACA rules. Routine care depends on the network, so we look for plans with national PPO networks when you run out of state. More in <a href=\"/blog/using-health-insurance-out-of-state-truck-drivers\">using your plan out of state</a>."),
  ("Does health insurance cover my DOT physical?","Usually not, because a DOT physical is a work requirement rather than preventive care. There are ways to pay less. See <a href=\"/does-health-insurance-cover-dot-physical\">does insurance cover a DOT physical</a>."),
 ]),
'small-business-health-quote.html':dict(
 url="https://www.vshealthbenefits.com/small-business-health-quote",
 title="Small Business Health Insurance Quotes: Free Group Quotes (2027)",
 desc="Free small business health insurance quotes. Compare group plans from top carriers for teams of 2 to 100+. Most quotes back within 1 business day.",
 h1_old="Get Small Business Health Insurance", h1="Small Business Health Insurance Quotes",
 service="Small business health insurance quotes", stype="Group health insurance brokerage",
 crumbs=[("Home","/"),("Small business health insurance","/small-business-health-insurance"),("Quotes","/small-business-health-quote")],
 body="""
  <h2>How small business health insurance quotes work</h2>
  <ol class="lp-steps">
    <li><h3>Tell us your ZIP and team size</h3><p>Group plans and prices depend on where your business is located and how many employees are eligible.</p></li>
    <li><h3>Share a simple employee list</h3><p>For each employee we need a date of birth, home ZIP and coverage level (employee only, with spouse, with children, or family). No Social Security numbers and no health questions.</p></li>
    <li><h3>Compare carriers side by side</h3><p>A licensed advisor shops group plans from multiple carriers and walks you through the options. We reach out within 1 business day, often within hours.</p></li>
  </ol>
  <h2>What affects your group health insurance quote</h2>
  <ul class="lp-list">
    <li><strong>Employee ages and location.</strong> Small group plans (up to 50 employees in most states) are priced under ACA rules by age, location and, in some states, tobacco use. Employee health history is not used.</li>
    <li><strong>Plan design.</strong> Deductibles, copays and network type (PPO or HMO) change the premium. Many employers offer two plans so employees can choose.</li>
    <li><strong>How much you contribute.</strong> You set the employer share. Many carriers require at least 50% of the employee-only premium.</li>
  </ul>
  <p style="margin-top:-18px;margin-bottom:34px">Want a ballpark first? Try the <a href="/small-business-health-insurance-calculator">small business health insurance cost calculator</a>.</p>
  <h2>What you need to qualify for a group plan</h2>
  <div class="lp-who">
    <div><h3>At least one employee</h3><p>Most carriers need at least one W-2 employee who is not the owner or the owner's spouse. <a href="/blog/how-many-employees-do-you-need-for-group-health-insurance">How many employees you need</a></p></div>
    <div><h3>Enough enrollment</h3><p>Most carriers want about 70% of eligible employees to enroll. Employees covered elsewhere often don't count against you. <a href="/blog/group-health-insurance-minimum-participation">The 70% rule</a></p></div>
    <div><h3>Other ways to offer benefits</h3><p>If a group plan doesn't fit, an ICHRA reimburses employees for individual plans instead. <a href="/ichra-vs-group-health-calculator">ICHRA vs. group calculator</a></p></div>
  </div>
  <h2>Small business quote FAQ</h2>
""",
 faqs=[
  ("How fast can I get a small business health insurance quote?","Most quotes are back within 1 business day, often within hours, once we have your employee list."),
  ("Is the quote free?","Yes. Quotes are free with no obligation. Insurance companies pay us, so your premium is the same as buying from the carrier directly."),
  ("When can group coverage start?","Small group coverage can start on the 1st of any month. There is no open enrollment period for employers, so plan on a few weeks between choosing a plan and the start date."),
  ("Do employees have to answer health questions?","No. Small group plans follow ACA rules, so employees are not asked about their health and nobody can be turned down for a pre-existing condition."),
  ("Our renewal went up. Can you quote against it?","Yes. Send us your renewal and we will compare it with other carriers. Start with a <a href=\"/small-business-renewal-review\">free renewal review</a>."),
 ]),
}
for f,c in PAGES.items():
    s=open(f).read(); o=s
    t=html.escape(c['title'],quote=False); d=html.escape(c['desc'])
    s=re.sub(r'<title>[^<]*</title>',f'<title>{t}</title>',s,1)
    s=re.sub(r'<meta name="description" content="[^"]*"',f'<meta name="description" content="{d}"',s,1)
    s=re.sub(r'<meta property="og:title" content="[^"]*"',f'<meta property="og:title" content="{html.escape(c["title"])}"',s,1)
    s=re.sub(r'<meta property="og:description" content="[^"]*"',f'<meta property="og:description" content="{d}"',s,1)
    if 'og:url' not in s: s=s.replace('<meta property="og:title"',f'<meta property="og:url" content="{c["url"]}" />\n<meta property="og:type" content="website" />\n<meta property="og:title"',1)
    assert s.count(f'<h1 id="lp-h1">{c["h1_old"]}</h1>')==1,f
    s=s.replace(f'<h1 id="lp-h1">{c["h1_old"]}</h1>',f'<h1 id="lp-h1">{c["h1"]}</h1>')
    if 'quote-page info (2026-10-28)' not in s: s=s.replace('</style>',CSS+'</style>',1)
    if 'class="lp-info"' not in s:
        block=f'<section class="lp-info" aria-label="How quotes work"><div class="wrap">{c["body"]}  {faq_html(c["faqs"])}\n</div></section>\n\n'
        assert s.count('<section class="lp-cta">')==1
        s=s.replace('<section class="lp-cta">',block+'<section class="lp-cta">')
    if '#service' not in s:
        s=s.replace('</head>',schema(c['url'],c['service'],c['desc'],c['stype'],c['crumbs'],c['faqs'])+'</head>',1)
    print(f, 'title',len(c['title']),'desc',len(c['desc']))
    if APPLY: open(f,'w').write(s)

# descriptive links from the main pages
LINKS=[('truck-driver-health-insurance.html','/trucking-health-quote','health insurance quotes for truck drivers'),
       ('health-insurance-for-trucking-companies.html','/trucking-health-quote','health insurance quotes for trucking companies'),
       ('best-health-insurance-owner-operators.html','/trucking-health-quote','free health insurance quotes for owner-operators'),
       ('small-business-health-insurance.html','/small-business-health-quote','small business health insurance quotes'),
       ('health-insurance-for-small-business-owners.html','/small-business-health-quote','small business health insurance quotes')]
for f,href,anchor in LINKS:
    s=open(f).read()
    if f'>{anchor}</a>' in s: print('link exists',f); continue
    lede=re.search(r'(<h1[^>]*>.*?</h1>)(.*?)(</p>)',s,re.S)
    if not lede: print('!! no h1/p',f); continue
    ins=f' <a href="{href}">Get {anchor}</a>.' if False else ''
    para=f'\n<p class="vs-quote-link" style="font-size:.98rem;margin:10px 0 0">Ready for real numbers? Get free <a href="{href}">{anchor}</a> from a licensed advisor.</p>'
    s2=s[:lede.end()]+para+s[lede.end():]
    print('link ->',f,'after:',re.sub(r'<[^>]+>','',lede.group(2))[-90:].strip())
    if APPLY: open(f,'w').write(s2)
print('APPLIED' if APPLY else 'dry run')

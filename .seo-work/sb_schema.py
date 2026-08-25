# -*- coding: utf-8 -*-
"""Add Service schema with areaServed + BusinessAudience to the industry/trade pages.
They carry FAQPage already but nothing that says 'this is a group-health service for
employers in these places'."""
import re, json, glob

BASE='https://www.vshealthbenefits.com'
FL_METRO=['Miami','Fort Lauderdale','Coral Gables','Doral','Hialeah','Hollywood','Miramar',
          'Pembroke Pines','Plantation','Sunrise','Coral Springs']

PAGES={
 'health-insurance-for-construction-companies.html':'Group health insurance for construction contractors',
 'health-insurance-for-cleaning-companies.html':'Group health insurance for janitorial and cleaning contractors',
 'health-insurance-for-retail-businesses.html':'Group health insurance for retail stores and chains',
 'health-insurance-for-trucking-companies.html':'Group health insurance for trucking companies and fleets',
 'health-insurance-for-restaurants.html':'Group health insurance for restaurants and food service',
 'health-insurance-for-hvac-companies.html':'Group health insurance for HVAC companies',
 'health-insurance-for-auto-repair-shops.html':'Group health insurance for auto repair shops',
 'health-insurance-for-dental-offices.html':'Group health insurance for dental offices and practices',
 'health-insurance-for-salons-and-spas.html':'Group health insurance for salons, spas and barbershops',
 'small-business-health-insurance.html':'Small business group health insurance',
 'small-business-health-insurance-cost.html':'Small business group health insurance pricing',
 'florida-small-business-health-insurance.html':'Group health insurance for Florida small business',
 'ichra-florida-small-business.html':'ICHRA setup for Florida small business',
 'level-funded-health-insurance-florida.html':'Level-funded health plan setup for Florida employers',
}

n=0
for f,svc in PAGES.items():
    s=open(f,encoding='utf-8').read()
    if 'vs-service-schema' in s: continue
    url=BASE+'/'+f[:-5]
    schema={
      "@context":"https://schema.org","@type":"Service",
      "serviceType":svc,"name":svc,"url":url,
      "provider":{"@type":"InsuranceAgency","name":"VS Health Benefits","url":BASE+"/",
        "telephone":"+1-954-825-1009","email":"info@vshealthbenefits.com",
        "address":{"@type":"PostalAddress","addressLocality":"Miami","addressRegion":"FL","addressCountry":"US"}},
      "areaServed":[{"@type":"City","name":c,"addressRegion":"FL"} for c in FL_METRO]
                  +[{"@type":"State","name":"Florida"},{"@type":"Country","name":"United States"}],
      "audience":{"@type":"BusinessAudience","name":"Small businesses with 1-50 employees",
                  "numberOfEmployees":{"@type":"QuantitativeValue","minValue":1,"maxValue":50}},
      "offers":{"@type":"Offer","price":"0","priceCurrency":"USD",
                "description":"Free comparison and setup of group health coverage; carriers pay the broker commission."},
      "availableChannel":{"@type":"ServiceChannel","serviceUrl":BASE+"/quote?type=business",
                          "servicePhone":{"@type":"ContactPoint","telephone":"+1-954-825-1009"}}
    }
    block='<script type="application/ld+json" id="vs-service-schema">\n%s\n</script>\n'%json.dumps(schema,indent=2)
    s=s.replace('</head>', block+'</head>',1)
    open(f,'w',encoding='utf-8').write(s); n+=1
print('Service schema added to',n,'pages')

# validate all
bad=0
for f in sorted(glob.glob('*.html'))+sorted(glob.glob('blog/*.html')):
    s=open(f,encoding='utf-8').read()
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',s,re.S):
        try: json.loads(m.group(1))
        except Exception as e: print(' BAD',f,str(e)[:50]); bad+=1
print('invalid JSON-LD:',bad)

# -*- coding: utf-8 -*-
"""HVAC companies page rework (2026-11-21): simple hero, problem/solution,
Jack quote, no level-funded, every CTA to the business quote."""
import re, sys, json
sys.path.insert(0, ".seo-work")
import trade_hero as TH

P = "health-insurance-for-hvac-companies.html"
SLUG = "health-insurance-for-hvac-companies"
Q = "/quote?type=business&amp;from=" + SLUG
s = open(P, encoding="utf-8").read()

def ed(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:90])
    s = s.replace(a, b)

# --- meta / SEO
TITLE = "Health Insurance for HVAC Companies: Recruit &amp; Keep Techs (2027)"
DESC = "Health insurance for HVAC companies, compared across top carriers. Group plans for 2 to 100+ techs from about $350 per employee. 1,000+ companies helped. Free quotes."
s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % TITLE, s, 1)
s = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + TITLE, s, 1)
s = re.sub(r'(<meta name="description" content=")[^"]*', r"\g<1>" + DESC, s, 1)
s = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\g<1>" + DESC, s, 1)
s = re.sub(r'(<meta name="keywords" content=")[^"]*', r"\g<1>health insurance for hvac companies, hvac company health insurance, group health insurance for hvac technicians, hvac employee benefits, how to recruit hvac technicians, hvac technician retention, health insurance for hvac contractors, air conditioning company health insurance", s, 1)
s = s.replace('content="https://www.vshealthbenefits.com/compressed/hvac-rooftop-technician.jpg"', 'content="https://www.vshealthbenefits.com/compressed/hvac-techs-checking-ac-unit.jpg"')

# --- hero
hero = TH.hero(SLUG, "Health Insurance for", "HVAC Companies &amp; Their Techs",
               "Hire and keep good HVAC techs with health benefits that fit your budget. We compare every major carrier for shops of 2 to 100+, free.",
               "hvac-techs-checking-ac-unit", "Two HVAC technicians checking an outdoor AC condenser unit at a home")
s, n = re.subn(r'<section class="hero">.*?</section>', hero, s, count=1, flags=re.S)
assert n == 1

CSS = TH.CSS + """
<style id="vs-hv-css">
.hv-ps{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:8px}
.hv-ps>div{background:#fff;border:1px solid #e4e9f2;border-radius:18px;padding:28px 28px 24px;box-shadow:0 14px 34px -26px rgba(11,35,70,.4)}
.hv-ps .hv-prob{border-top:5px solid #e0533d}
.hv-ps .hv-sol{border-top:5px solid #0db5a6}
.hv-tag{display:inline-block;font-size:.74rem;font-weight:800;letter-spacing:.09em;text-transform:uppercase;padding:5px 11px;border-radius:999px;margin-bottom:12px}
.hv-prob .hv-tag{background:#fdecea;color:#b42318}.hv-sol .hv-tag{background:#e3f7f4;color:#0b766c}
.hv-ps h3{font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1.3rem;line-height:1.3;margin:0 0 14px}
.hv-ps ul{margin:0;padding-left:20px;display:grid;gap:10px;color:#334155;line-height:1.55}
.hv-band{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:26px auto 0;background:linear-gradient(90deg,#0b2346,#16447f);color:#fff;border-radius:18px;padding:22px 28px;text-align:left}
.hv-band b{font-family:'Poppins','Inter',sans-serif;font-size:2.4rem;line-height:1;color:#5eead4}
.hv-band p{margin:0;max-width:440px;color:rgba(255,255,255,.92)}
.hv-band .btn{background:#fff;color:#0b2346;border-color:#fff}
.hv-jack{display:grid;grid-template-columns:220px 1fr;gap:34px;align-items:center;max-width:900px;margin:0 auto}
.hv-jack img{width:220px;height:220px;border-radius:50%;object-fit:cover;object-position:50% 22%;box-shadow:0 18px 40px -20px rgba(11,35,70,.55);border:5px solid #fff}
.hv-jack blockquote{margin:0;font-family:'Poppins','Inter',sans-serif;font-size:clamp(1.15rem,2.2vw,1.45rem);line-height:1.5;color:#0b2346;font-weight:600}
.hv-jack blockquote::before{content:"\\201C";display:block;font-size:3.4rem;line-height:.6;color:#0db5a6;margin-bottom:6px}
.hv-jack figcaption{margin-top:14px;color:#475569;font-size:.98rem}.hv-jack figcaption strong{color:#0b2346}
@media(max-width:820px){.hv-ps{grid-template-columns:1fr}.hv-jack{grid-template-columns:1fr;text-align:center;justify-items:center}.hv-jack img{width:170px;height:170px}.hv-band{text-align:center}}
</style>"""
ed("</head>", CSS + "\n</head>")

# --- trust bar
ed("Affordable Level Funded Plans</span>", "1,000+ Companies Assisted</span>")

# --- problem / solution + Jack, right after the carrier strip
PS = """<section class="section" id="recruiting">
  <div class="container">
    <div class="center" style="margin-bottom:26px"><span class="eyebrow">Recruiting &amp; Retention</span><h2>Why HVAC Companies Struggle to Hire and Keep Techs</h2><p style="max-width:720px;margin:0 auto">Most HVAC owners we talk to have more calls than crew. Here is what is going on, and how benefits fix it.</p></div>
    <div class="hv-ps">
      <div class="hv-prob"><span class="hv-tag">The problem</span><h3>Good HVAC techs are hard to find and harder to keep</h3><ul>
        <li>Experienced techs get recruiting calls every week, and they compare total compensation, not just the hourly rate.</li>
        <li>Union, utility and large competitors lead with full benefits. A shop without health insurance starts every interview behind.</li>
        <li>Every tech who leaves costs you recruiting, overtime for the rest of the crew, missed service calls and callbacks, usually in peak season.</li>
        <li>Demand keeps climbing. The <a href="https://www.bls.gov/ooh/installation-maintenance-and-repair/heating-air-conditioning-and-refrigeration-mechanics-and-installers.htm" rel="noopener" target="_blank">Bureau of Labor Statistics</a> projects HVAC jobs to grow 11%% from 2025 to 2035.</li>
      </ul></div>
      <div class="hv-sol"><span class="hv-tag">The solution</span><h3>A benefits package that wins the hire and keeps your crew</h3><ul>
        <li>We compare group health plans across every major carrier for HVAC shops of 2 to 100+ employees.</li>
        <li>You set the budget. We build options with a contribution you can carry through the shoulder season.</li>
        <li>ICHRA options when your headcount swings with the season or you want a fixed cost per tech.</li>
        <li>We run enrollment around your schedule and handle tech questions, adds, drops and renewals.</li>
      </ul></div>
    </div>
    <div class="hv-band"><b>1,000+</b><p>companies assisted with employee health benefits. Tell us about your crew and we&rsquo;ll show you real numbers.</p><a class="btn" href="%s">Get a Group Quote</a></div>
  </div>
</section><section class="section bg-soft" id="jack">
  <div class="container">
    <figure class="hv-jack">
      <picture><source type="image/webp" srcset="/compressed/jack-schnell-480.webp"><img src="/compressed/jack-schnell-480.jpg" width="480" height="478" alt="Jack Schnell, Co-Founder of VS Health Benefits" loading="lazy" decoding="async" /></picture>
      <div><blockquote>HVAC owners rarely lose a good tech over a dollar an hour. They lose them to the shop down the road that offers health insurance. Our job is to make you that shop, at a price that still works in the slow months.</blockquote>
      <figcaption><strong>Jack Schnell</strong>, Co-Founder, VS Health Benefits</figcaption></div>
    </figure>
  </div>
</section>""" % Q
i = s.index('<div class="carriers">'); j = s.index("<section", i)
s = s[:j] + PS + s[j:]

# --- level funded out
ed("<p>We lean on level funded and ICHRA options that keep costs predictable, work for shops of two to fifty or more, and give you clear guidance on who you are required to cover.</p>",
   "<p>We compare fully insured group plans and ICHRA options that keep costs predictable, work for shops of two to a hundred or more, and give you clear guidance on who you are required to cover.</p>")
ed("<li>Affordable level funded plans for healthy teams</li>", "<li>Plans and contributions that fit your budget</li>")
s, n = re.subn(r'\s*<div class="card">\s*<div class="card-img"><img[^>]*microgroup[^>]*></div>\s*<div class="card-body"><div class="ic">L</div><h3>Level Funded</h3>.*?</div>\s*</div>', "", s, count=1, flags=re.S)
assert n == 1
ed("        <tr><td><strong>Level funded group</strong></td><td>Often 10 to 30 percent less</td><td>Possible refund if claims stay low</td></tr>\n", "")
ed("HVAC companies with as few as two employees can qualify for group or level funded coverage. Level funded is often the most affordable route for a young, healthy crew.",
   "HVAC companies with as few as two employees can qualify for group coverage. Shops with seasonal headcount often start with an ICHRA, which reimburses a set monthly amount toward each tech's own plan.", 2)
ed("Single coverage commonly runs about 350 to 700 dollars per month and is usually split with the employee. Level funded options can lower that for a healthy team. We show exact numbers free.",
   "Single coverage commonly runs about 350 to 650 dollars per employee per month and is usually split with the employee. Rates depend on ages, ZIP code and plan design. We show exact numbers free.", 2)
ed("<span>Group, level-funded and ICHRA compared for a team of 2 to 50, with real per-employee ranges.</span>",
   "<span>Group plans and ICHRA compared for a team of 2 to 50, with real per-employee ranges.</span>")

# --- FAQ: add recruiting question (HTML + schema)
FQ = ("How does health insurance help an HVAC company recruit and keep techs?",
      "Experienced HVAC techs compare total compensation, and health insurance is the benefit they ask about most. Offering a group plan, or an ICHRA with a set monthly amount, lets you compete with union and larger shops and cuts turnover, which saves recruiting costs, overtime and missed service calls.")
ed('<div class="faq"><details class="faq-item">', '<div class="faq"><details class="faq-item"><summary>%s</summary><p>%s</p></details><details class="faq-item">' % FQ)
m = re.search(r'<script type="application/ld\+json">\s*(\{"@context": "https://schema.org", "@type": "FAQPage".*?)\s*</script>', s, re.S)
d = json.loads(m.group(1)); d["mainEntity"].insert(0, {"@type": "Question", "name": FQ[0], "acceptedAnswer": {"@type": "Answer", "text": FQ[1]}})
s = s.replace(m.group(1), json.dumps(d))

# --- stats
ed('<div class="stat"><div class="stat-num">2-100+</div><div class="stat-label">Employees covered</div></div>',
   '<div class="stat"><div class="stat-num">1,000+</div><div class="stat-label">Companies assisted</div></div>')

# --- every quote link to the business quote
s = s.replace('href="/small-business-health-quote?type=business"', 'href="%s"' % Q)
s = s.replace('>Get a Quote</a>', '>Get Quotes</a>')
assert "level funded" not in s.lower() and "level-funded" not in s.lower(), re.findall(r".{60}level.funded.{40}", s, re.I)
assert "small-business-health-quote?type" not in s
open(P, "w", encoding="utf-8").write(s)
print("ok", len(s))

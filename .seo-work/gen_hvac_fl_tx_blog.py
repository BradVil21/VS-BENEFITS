#!/usr/bin/env python3
"""Build blog/hvac-health-insurance-florida-texas.html (2026-11-25). Run from site root."""
import json, re, html

TPL = "blog/team-truck-drivers-health-insurance.html"
OLD_SLUG = "team-truck-drivers-health-insurance"
SITE = "https://www.vshealthbenefits.com"
DATE_ISO, DATE_LONG = "2026-11-25", "November 25, 2026"
SLUG = "hvac-health-insurance-florida-texas"

tpl = open(TPL, encoding="utf-8").read()
META_DIV = re.search(r'<div class="article-meta">.*?</div>', tpl, re.S).group(0).replace("September 27, 2026", DATE_LONG)
ALERT_ICON = re.search(r'<div class="alert-box"><div class="icon">(.*?)</div>', tpl, re.S).group(1)
rr = open("premium-increase-review.html", encoding="utf-8").read()
Q = "/quote?from=blog/" + SLUG + "&type=business"

def cta(h, p, href=Q, btn="Get a Group Quote &rarr;"):
    return '<div class="cta-block"><h3>%s</h3><p>%s</p><a class="btn btn-teal" href="%s">%s</a></div>' % (h, p, href.replace("&", "&amp;"), btn)

def tbl(head, rows, note=""):
    h = '<div class="vs-tw"><table class="vs-t" style="min-width:0"><thead><tr>' + "".join("<th>%s</th>" % x for x in head) + "</tr></thead><tbody>"
    h += "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows) + "</tbody></table></div>"
    return h + ('<p class="vs-src">%s</p>' % note if note else "")


H1 = "Health Insurance for HVAC Companies and Contractors in Florida and Texas (2027)"

def fig(img, alt, cap, w=1200, h=900):
    return ('<figure style="margin:22px 0"><picture><source type="image/webp" srcset="/compressed/%s-900.webp 900w, /compressed/%s.webp %dw" sizes="(max-width: 800px) 100vw, 760px">'
            '<img src="/compressed/%s-900.jpg" srcset="/compressed/%s-900.jpg 900w, /compressed/%s.jpg %dw" sizes="(max-width: 800px) 100vw, 760px" width="%d" height="%d" alt="%s" loading="lazy" decoding="async" style="width:100%%;height:auto;border-radius:14px;display:block"></picture>'
            '<figcaption style="font-size:.85rem;color:var(--muted);margin-top:8px">%s</figcaption></figure>') % (img, img, w, img, img, img, w, w, h, alt, cap)

COMPARE = tbl(["", "Florida", "Texas"], [
  ["Who counts as a small employer", "1 to 50 employees, including the self-employed", "2 to 50 employees"],
  ["Employer must offer coverage under 50 FTEs?", "No", "No"],
  ["Where individuals buy Marketplace plans", "HealthCare.gov", "HealthCare.gov"],
  ["2027 individual rate change", "About 10.4% approved average (15.3% requested)", "About 14.1% requested average"],
  ["Uninsured rate (2024)", "10.9%", "16.7%, the highest in the U.S."],
  ["HVAC techs employed (May 2023)", "37,370, the most of any state", "31,910"],
], "Small employer definitions from Fla. Stat. 627.6699 and Texas Insurance Code 1501.002. Rate changes are statewide averages for individual plans; group renewals are priced separately.")

OPTIONS = tbl(["Option", "Best for an HVAC shop that...", "Watch for"], [
  ["Small group plan", "Wants one company plan for W-2 techs and office staff", "Carriers usually want about 70% of eligible employees enrolled and about 50% of employee-only premium paid by you"],
  ["<a href=\"/ichra-florida-small-business\">ICHRA</a>", "Has headcount that swings with the season, or wants a fixed cost per tech", "Techs pick individual plans; an affordable ICHRA can end their Marketplace tax credit"],
  ["QSEHRA", "Has under 50 employees and wants to reimburse part of each tech's premium", "2026 limits: $6,450 self-only, $13,100 family"],
  ["Dental and vision", "Wants a low-cost first step", "Not a substitute for health coverage"],
])

SLUG_URL = "/blog/hvac-health-insurance-florida-texas"
A = dict(
    title="HVAC Company Health Insurance in Florida & Texas: 2027 Costs",
    h1=H1,
    desc="Health insurance for HVAC companies and contractors in Florida and Texas: 2027 costs from $350 per employee, each state's small-group rules, ICHRA and 1099 tech options.",
    keywords=["hvac company health insurance florida", "hvac health insurance texas", "health insurance for hvac companies florida", "health insurance for hvac companies texas", "air conditioning company health insurance florida", "hvac contractor benefits texas", "minimum employees for group health insurance florida", "minimum employees for group health insurance texas", "hvac company health insurance texas", "health insurance for hvac contractors florida", "health insurance for hvac contractors texas",
              "small business health insurance florida hvac", "texas small employer health insurance", "group health insurance hvac", "health insurance for 1099 hvac techs"],
    alt="Three HVAC technicians in safety glasses working on an outdoor AC unit with gauges",
    mins=8,
    lede="Florida and Texas run on air conditioning, and both states are short on the techs who keep it running. If you own an HVAC company or work as an HVAC contractor in either state, health insurance is one of the strongest tools you have to hire and keep good people. Here is how the rules work in each state, what coverage costs in 2027, and the options that fit an HVAC crew.",
    short="HVAC companies in Florida and Texas can offer a <strong>small group plan</strong> (about <strong>$350 to $650 per employee per month</strong> for employee-only coverage), an <strong>ICHRA</strong>, or help techs buy their own plans. The key difference: <strong>Florida</strong> treats businesses with <strong>1 to 50 employees</strong>, including the self-employed, as small employers, while <strong>Texas</strong> starts at <strong>2 employees</strong>. Neither state requires a company under 50 full-time equivalents to offer coverage. <a href=\"" + Q.replace("&", "&amp;") + "\">Get group quotes for your crew</a>.",
    sections=[
        ("why", "Why benefits matter more for HVAC in Florida and Texas",
         "<p>No state employs more HVAC mechanics and installers than Florida: the Bureau of Labor Statistics counted <strong>37,370</strong> in May 2023. Texas had <strong>31,910</strong>, third in the country. Cooling demand runs most of the year in both states, so every shop is competing for the same licensed techs.</p>"
         "<p>Both states also have a lot of people without health insurance. In 2024, <strong>16.7%</strong> of Texans were uninsured, the highest rate in the country, and Florida stood at <strong>10.9%</strong>, compared with <strong>8.2%</strong> nationally. Many of the techs you interview have never had employer coverage. A shop that offers it stands out right away.</p>"),
        ("compare", "Florida vs. Texas: the rules side by side", COMPARE),
        ("florida", "Health insurance for HVAC companies in Florida",
         "<p>Florida law defines a small employer as a business with <strong>at least 1 and no more than 50</strong> employees, and it expressly includes self-employed individuals. That means even a very small HVAC company can shop small group coverage in Florida. Carriers still set their own participation and contribution rules, so it pays to compare more than one.</p>"
         "<p>Florida employers are not required to offer coverage until they reach 50 full-time equivalent employees. For techs buying their own plans, Florida insurers asked for an average increase of about 15.3% for 2027, and regulators approved a lower weighted average of about 10.4%, after a 31.5% average increase in 2026. See <a href=\"/blog/health-insurance-rate-increases-2027-by-state\">2027 rate increases by state</a>.</p>"
         "<p>More detail: <a href=\"/florida-small-business-health-insurance\">Florida small business health insurance</a> and <a href=\"/florida-small-business-health-insurance-requirements\">Florida employer requirements</a>.</p>"),
        ("texas", "Health insurance for HVAC companies in Texas",
         "<p>The Texas Insurance Code defines a small employer as one that employed an average of <strong>at least 2 and no more than 50</strong> employees during the prior year and has at least 2 employees on the first day of the plan year. A one-person HVAC business in Texas generally can&rsquo;t buy small group coverage, so the owner buys an individual plan until the first hire.</p>"
         "<p>The Texas Department of Insurance notes that state law doesn&rsquo;t require you to pay your employees&rsquo; premiums, but your insurance company may require you to pay at least 50%. Texas individual-market insurers asked for an average increase of about 14.1% for 2027, after a 34.7% average increase in 2026.</p>"
         "<p>More detail: <a href=\"/texas-small-business-health-insurance\">Texas small business health insurance</a>.</p>"),
        ("options", "Coverage options that fit an HVAC crew",
         OPTIONS + "<p>Under federal rules, carriers waive their participation and contribution requirements for small groups that start coverage during the <strong>November 15 to December 15</strong> window each year, which makes it the easiest time to set up a first plan.</p>"),
        ("contractors", "1099 subs and self-employed HVAC contractors",
         fig("contractor-roof-window-work", "Contractor working on the second-story roof of a house", "Independent contractors buy their own coverage. Tax credits are based on net income after business expenses.")
         + "<p>A genuine 1099 subcontractor can&rsquo;t join your group plan. Self-employed HVAC contractors in either state buy individual coverage, and Marketplace tax credits are based on <strong>net</strong> income after the truck, tools and other business costs. A single person qualifies up to about $63,840 for 2027 coverage. See <a href=\"/health-insurance-for-hvac-technicians\">health insurance for HVAC technicians</a>.</p>"
         "<p>If you control a sub&rsquo;s hours, tools and methods, they may be an employee in practice, which changes both your headcount and your obligations. <a href=\"/blog/1099-crew-vs-w2-health-insurance\">1099 crews vs. W-2 employees</a>.</p>"),
        ("cities", "Florida and Texas cities we quote HVAC groups in",
         "<p>Carriers, networks and prices change by county, so the plan that fits a shop in Miami may not be the best one in Jacksonville. We quote HVAC companies across both states, including:</p>"
         "<ul><li><strong>Florida:</strong> <a href=\"/miami-small-business-health-insurance\">Miami</a>, <a href=\"/fort-lauderdale-small-business-health-insurance\">Fort Lauderdale</a>, <a href=\"/tampa-small-business-health-insurance\">Tampa</a>, Orlando, Jacksonville, West Palm Beach and Fort Myers.</li>"
         "<li><strong>Texas:</strong> Houston, Dallas&ndash;Fort Worth, San Antonio, Austin, El Paso and the Rio Grande Valley.</li></ul>"
         "<p>Before you enroll, we check that the hospitals and doctors your techs actually use are in network in your area.</p>"),
        ("steps", "How to get your crew covered",
         "<ol><li>List each W-2 employee&rsquo;s age, ZIP code and average weekly hours.</li><li>Decide who&rsquo;s eligible, for example everyone at 30+ hours, after a waiting period of up to 90 days.</li>"
         "<li>Pick a monthly amount you can carry through the slower months.</li><li><a href=\"" + Q.replace("&", "&amp;") + "\">Get quotes</a> from every carrier that writes HVAC groups in your county, plus ICHRA options.</li>"
         "<li>Enroll before December 15 for January 1 coverage, or start any month after that.</li></ol>"),
    ],
    faq=[
        ("Do HVAC companies in Florida or Texas have to offer health insurance?", "Not until they have 50 or more full-time equivalent employees. Neither state adds its own employer mandate. At 50 or more, the 2027 federal penalty for offering no coverage is $3,780 per full-time employee, minus the first 30."),
        ("How much does group health insurance cost for an HVAC company in Florida or Texas?", "Small group coverage usually runs about $350 to $650 per employee per month for employee-only coverage, before the employer's share. Rates depend mostly on employee ages, ZIP code and plan design."),
        ("Can a one-person HVAC business get group health insurance?", "In Florida, state law counts businesses with 1 to 50 employees, including the self-employed, as small employers, so it may be possible depending on the carrier. In Texas, a small employer needs at least 2 employees, so a one-person business buys an individual plan."),
        ("What is the minimum number of employees for group health insurance in Florida?", "Florida law counts businesses with 1 to 50 employees, including the self-employed, as small employers. In practice, many carriers want at least one W-2 employee besides the owner, so options for a one-person business are limited. A licensed broker can check which carriers will write your group."),
        ("What is the minimum number of employees for group health insurance in Texas?", "Two. Texas law defines a small employer as one with an average of at least 2 and no more than 50 employees, with at least 2 employees on the first day of the plan year."),
        ("Is health insurance tax deductible for an HVAC company?", "Premiums a business pays for its employees' health coverage are generally a deductible business expense, and very small employers with lower average wages may qualify for the small business health care tax credit. Self-employed HVAC contractors can usually deduct their own premiums. Check with your tax preparer."),
        ("Can I cover my W-2 techs and not my 1099 subcontractors?", "Yes. Genuine 1099 subcontractors can't join a group plan. They buy individual coverage, often with Marketplace tax credits based on their net income."),
        ("What if my HVAC crew grows every summer?", "Seasonal workers who aren't expected to work 30+ hours for a full measurement period usually don't have to be offered coverage. An ICHRA can also give you a fixed cost per tech as headcount changes."),
    ],
    sources=[
        ("U.S. Bureau of Labor Statistics: Occupational Employment and Wages, HVAC mechanics and installers, May 2023", "https://www.bls.gov/oes/2023/may/oes499021.htm"),
        ("Texas Department of Insurance: Small employer health insurance guide", "https://tdi.texas.gov/pubs/consumer/cb040.html"),
        ("Texas Insurance Code Chapter 1501", "https://statutes.capitol.texas.gov/Docs/IN/htm/IN.1501.htm"),
        ("America's Health Rankings: Uninsured by state (U.S. Census Bureau ACS, 2024)", "https://www.americashealthrankings.org/explore/annual/measure/HealthInsurance/state/ALL"),
    ],
    related=[("Free quote", "Get a Group Quote for Your HVAC Company", Q.replace("&", "&amp;")),
             ("Guide", "Group Health Insurance for HVAC Companies", "/health-insurance-for-hvac-companies"),
             ("Benefits", "HVAC Employee Benefits: What to Offer Techs", "/blog/hvac-employee-benefits")],
)

def related(items):
    cards = "".join(
        '<a href="%s" style="background:var(--bg-soft);border:1px solid var(--line);border-radius:12px;padding:16px;text-decoration:none;display:block">'
        '<div style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">%s</div>'
        '<div style="font-weight:700;color:var(--blue-900);font-size:.95rem;line-height:1.4">%s</div></a>' % (href, k, t) for k, t, href in items)
    return ('<div style="margin-top:36px"><h3 style="margin-top:0">Related Pages</h3>'
            '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">%s</div></div>') % cards

IMG = "hvac-techs-training-ac-unit"
hero = ('<div class="hero-img"><img src="/compressed/%s-900.jpg" srcset="/compressed/%s-900.jpg 900w, /compressed/%s.jpg 1600w" sizes="(max-width: 800px) 100vw, 760px" alt="%s" width="1600" height="1200" fetchpriority="high" decoding="async" itemprop="image" /></div>'
        % (IMG, IMG, IMG, html.escape(A["alt"], quote=True)))

url = "%s/blog/%s" % (SITE, SLUG)
img_full = "%s/compressed/%s.jpg" % (SITE, IMG)
s = tpl
esc_desc, esc_title = html.escape(A["desc"], quote=True), html.escape(A["title"], quote=True)
s = re.sub(r"<title>.*?</title>", "<title>%s</title>" % html.escape(A["title"]), s, count=1, flags=re.S)
for pat, val in [(r'<meta name="description" content="[^"]*"', '<meta name="description" content="%s"' % esc_desc),
                 (r'<link rel="canonical" href="[^"]*"', '<link rel="canonical" href="%s"' % url),
                 (r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="%s"' % esc_title),
                 (r'<meta property="og:description" content="[^"]*"', '<meta property="og:description" content="%s"' % esc_desc),
                 (r'<meta property="og:url" content="[^"]*"', '<meta property="og:url" content="%s"' % url),
                 (r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="%s"' % img_full),
                 (r'<meta property="article:published_time" content="[^"]*"', '<meta property="article:published_time" content="%sT08:00:00-05:00"' % DATE_ISO),
                 (r'<meta name="twitter:title" content="[^"]*"', '<meta name="twitter:title" content="%s"' % esc_title),
                 (r'<meta name="twitter:description" content="[^"]*"', '<meta name="twitter:description" content="%s"' % esc_desc),
                 (r'<meta name="twitter:image" content="[^"]*"', '<meta name="twitter:image" content="%s"' % img_full)]:
    s = re.sub(pat, val, s, count=1)
s = re.sub(r'<link rel="preload" as="image"[^>]*>', '<link rel="preload" as="image" href="/compressed/%s-900.jpg" fetchpriority="high" />' % IMG, s, count=1)
plain_h1 = html.unescape(H1)
blog_ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": plain_h1, "description": A["desc"], "image": img_full,
           "author": {"@type": "Person", "name": "Bradley Vilsaint", "url": SITE + "/bradley-vilsaint"},
           "publisher": {"@type": "Organization", "name": "VS Health Benefits", "logo": {"@type": "ImageObject", "url": SITE + "/favicon.png"}},
           "datePublished": DATE_ISO, "dateModified": DATE_ISO, "mainEntityOfPage": {"@type": "WebPage", "@id": url},
           "keywords": A["keywords"], "articleSection": "Health Insurance Costs"}
crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
    {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog"},
    {"@type": "ListItem", "position": 3, "name": plain_h1}]}
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in A["faq"]]}
lds = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, re.S))
for m, payload in reversed(list(zip(lds[:3], [blog_ld, crumb_ld, faq_ld]))):
    s = s[:m.start()] + '<script type="application/ld+json">\n' + json.dumps(payload, ensure_ascii=False) + "\n</script>" + s[m.end():]

toc = "".join('<li><a href="#%s">%s</a></li>' % (sid, h2) for sid, h2, _ in A["sections"]) + '<li><a href="#faq">FAQ</a></li>'
secs = []
for k, (sid, h2, body) in enumerate(A["sections"]):
    secs.append('<h2 id="%s">%s</h2>\n%s' % (sid if sid != "review" else "rate-review", h2, body))
    if sid == "why":
        secs.append(cta("Pricing coverage for your HVAC crew?", "Tell us your headcount and ZIP. We compare every carrier that writes HVAC groups in Florida and Texas, plus ICHRA options. Free."))
toc = toc.replace('href="#review"', 'href="#rate-review"')
faq_html = "".join("<h3>%s</h3>\n<p>%s</p>\n" % (q, a) for q, a in A["faq"])
src_html = ('<h2 id="sources">Sources</h2><ul class="vs-src">' +
            "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, html.escape(t)) for t, u in A["sources"]) + "</ul>")
article = (
    '<nav class="breadcrumb" aria-label="Breadcrumb">\n    <a href="/">Home</a><span class="sep">&rsaquo;</span>\n'
    '    <a href="/blog">Blog</a><span class="sep">&rsaquo;</span>\n    <span>HVAC Health Insurance in Florida &amp; Texas</span>\n  </nav>\n'
    '</div><main class="container">\n  <div class="article-wrap">\n\n'
    '    <article class="article-body" itemscope itemtype="https://schema.org/Article">\n'
    '<meta itemprop="datePublished" content="%s" />\n<meta itemprop="dateModified" content="%s" />\n'
    '<span class="eyebrow">HVAC &amp; Trades | Florida &amp; Texas | %d min read</span>\n%s\n'
    '<h1 itemprop="headline">%s</h1>\n<p class="lede">%s</p>\n%s\n\n'
    '<div class="alert-box"><div class="icon">%s</div><div><strong style="color:var(--ink)">The short answer</strong><br>'
    '<span style="color:var(--ink-2);font-size:.93rem">%s</span></div></div>\n\n'
    '%s\n\n<h2 id="faq">Frequently Asked Questions</h2>\n%s\n%s\n%s\n%s\n</article>\n\n'
    '    <aside class="article-sidebar">\n<a href="/blog" class="back-link">&larr; Back to Blog</a>\n'
    '<div class="sidebar-card"><h4>In This Article</h4><ul class="toc-list">%s</ul></div>\n'
    '<div class="sidebar-card" style="background:linear-gradient(135deg,var(--blue-700),var(--teal));border:none"><h4 style="color:#fff">Florida or Texas HVAC shop?</h4>'
    '<p style="color:rgba(255,255,255,.9);font-size:.88rem;margin-bottom:14px">We compare every carrier that writes HVAC groups in your county, side by side. Free.</p>'
    '<a class="btn" href="/quote?from=blog/health-insurance-premiums-rising-2027" style="background:#fff;color:var(--blue-700);width:100%%;justify-content:center;font-weight:700">Get My Free Quote</a></div>\n'
    '<div class="sidebar-card"><h4>Prefer to talk?</h4><p style="font-size:.88rem;color:var(--muted);margin-bottom:10px">Call or text a licensed advisor. English y Espa&ntilde;ol.</p>'
    '<a href="tel:+19548666872" style="font-size:1.1rem;font-weight:700;color:var(--blue-700)">(954) 866-6872</a></div>\n'
    '</aside>\n  </div>\n</main>'
) % (DATE_ISO, DATE_ISO, A["mins"], META_DIV, H1, A["lede"], hero, ALERT_ICON, A["short"].replace('href=\\"#review\\"', 'href="#rate-review"').replace('href="#review"', 'href="#rate-review"'),
     "\n\n".join(secs), faq_html,
     cta("Don&rsquo;t auto-renew a price increase", "See if you can pay less for 2027 before December 15. Free, no obligation."),
     src_html, related(A["related"]), toc)
b = s.index('<nav class="breadcrumb"'); e = s.index("</main>", b) + len("</main>")
s = s[:b] + article + s[e:]
s = s.replace(OLD_SLUG, SLUG).replace("&amp;niche=trucking", "").replace("&niche=trucking", "")
if 'id="vs-post-tbl"' not in s:
    s = s.replace("</head>", re.search(r'<style id="vs-post-tbl">.*?</style>', rr, re.S).group(0) + "\n</head>", 1)
s = re.sub(r'<section class="section vs-guide-sec".*?</section>', '', s, count=1, flags=re.S)
s = s.replace('<script src="/vs-guide.js" defer></script>', '')
assert "Team Truck Drivers" not in s, "template text leaked"
s = s.replace("/quote?from=blog/health-insurance-premiums-rising-2027", Q.replace("&", "&amp;")).replace("from=blog-%s&amp;type=individual" % SLUG, "from=blog-%s&amp;type=business" % SLUG)
open("blog/%s.html" % SLUG, "w", encoding="utf-8").write(s)
print("wrote blog/%s.html" % SLUG, len(s))

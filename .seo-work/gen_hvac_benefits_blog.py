#!/usr/bin/env python3
"""Build blog/hvac-employee-benefits.html (2026-11-20). Run from site root."""
import json, re, html

TPL = "blog/team-truck-drivers-health-insurance.html"
OLD_SLUG = "team-truck-drivers-health-insurance"
SITE = "https://www.vshealthbenefits.com"
DATE_ISO, DATE_LONG = "2026-11-20", "November 20, 2026"
SLUG = "hvac-employee-benefits"

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

BENEFITS = tbl(["Benefit", "Typical cost to you", "What it does for hiring"], [
  ["<strong>Health insurance</strong> (group plan or ICHRA)", "About $350&ndash;$650 per employee per month for employee-only coverage", "The #1 question techs with families ask"],
  ["<strong>Dental and vision</strong>", "Often $25&ndash;$60 per employee per month", "Cheap, visible, and easy to start with"],
  ["<strong>Paid time off and paid holidays</strong>", "Paid hours, planned around peak season", "Reduces burnout after summer and winter rushes"],
  ["<strong>Retirement plan</strong> (SIMPLE IRA or 401(k))", "Your match, often 2&ndash;4% of pay", "Keeps experienced techs for the long haul"],
  ["<strong>Tools, truck and phone</strong>", "Varies", "Big quality-of-life benefit techs compare between shops"],
  ["<strong>Training and certifications</strong> (EPA 608, NATE)", "Course and exam fees", "Builds your bench and shows a career path"],
], "Cost ranges are general estimates. Your rates depend on employee ages, ZIP code, plan design and carrier.")

PLANS = tbl(["Option", "Fits an HVAC company when", "Watch for"], [
  ["Fully insured small group", "You want one plan, predictable rates and no health questions", "Carriers usually need a share of eligible employees to enroll"],
  ["<a href=\"/level-funded-health-insurance-florida\">Level-funded</a>", "Your crew is young and mostly healthy", "Health questions; renewals move with claims"],
  ["<a href=\"/ichra-florida-small-business\">ICHRA</a>", "Headcount swings with the season, or you want a fixed cost per tech", "Employees pick their own individual plans"],
  ["QSEHRA", "Under 50 employees and you want to reimburse premiums", "2026 limits: $6,450 self-only, $13,100 family"],
])

PACKAGES = tbl(["Company size", "A realistic starting package"], [
  ["1&ndash;5 techs", "ICHRA or QSEHRA at a set monthly amount, plus dental and vision"],
  ["6&ndash;20 techs", "Small group PPO or level-funded plan, company pays 50&ndash;100% of employee-only, plus dental, vision and PTO"],
  ["21&ndash;49 techs", "Two plan choices (a lower-deductible PPO and an HSA plan), dental, vision, retirement match"],
  ["50+ full-time equivalents", "Affordable, minimum-value coverage is required, or you face the 2027 penalty of $3,780 per full-time employee"],
])

H1 = "HVAC Employee Benefits: What to Offer Techs in 2027 (and What It Costs)"
A = dict(
    title="HVAC Employee Benefits: What to Offer Techs in 2027",
    h1=H1,
    desc="HVAC employee benefits that help you hire and keep techs in 2027: health insurance costs, dental, vision, PTO, retirement, ICHRA options, and sample packages by company size.",
    keywords=["hvac employee benefits", "hvac technician benefits", "health insurance for hvac employees", "hvac company benefits package",
              "how to attract hvac technicians", "hvac employee health insurance", "benefits for hvac techs", "hvac recruiting and retention"],
    alt="Two HVAC technicians checking an outdoor AC condenser unit at a home",
    mins=8,
    lede="Good HVAC techs get recruiting calls every week, and pay alone isn't keeping them. The question most techs ask, especially those with families, is simple: <em>does the job come with health insurance?</em> Here is what a competitive HVAC benefits package looks like in 2027, what each piece costs, and how small shops can offer real coverage without blowing the budget.",
    short="The benefits HVAC techs care about most are <strong>health insurance</strong>, <strong>dental and vision</strong>, <strong>paid time off</strong>, a <strong>retirement match</strong>, and the <strong>tools, truck and training</strong> that come with the job. Group health coverage for a small trade business usually runs about <strong>$350 to $650 per employee per month</strong> for employee-only coverage. Shops under 50 employees aren&rsquo;t required to offer it, but it is the benefit that most often decides where a tech goes. <a href=\"" + Q.replace("&", "&amp;") + "\">See what it would cost your crew</a>.",
    sections=[
        ("why", "Why benefits decide who you can hire",
         "<p>HVAC is one of the fastest-growing trades. The Bureau of Labor Statistics counts about <strong>440,900</strong> HVAC mechanics and installers in the U.S., projects <strong>11% growth</strong> from 2025 to 2035, and reports a median pay of <strong>$61,010</strong> a year. With that much demand, techs can be picky, and they compare total compensation, not just the hourly rate.</p>"
         "<p>Pay gets a tech&rsquo;s attention. Benefits are what keep him from leaving for the shop down the road, or for a union or utility job with a full benefits package. Health insurance matters most, because it is the expense a tech can&rsquo;t easily cover on his own, especially with a spouse and kids.</p>"),
        ("package", "The HVAC benefits package, piece by piece", BENEFITS),
        ("health", "Health insurance options for HVAC companies",
         "<p>You don&rsquo;t have to offer one rich plan to everyone. These are the structures that fit HVAC shops best:</p>" + PLANS +
         "<p>Two timing notes. Carriers must accept small groups regardless of participation every year from <strong>November 15 to December 15</strong>, the easiest window to start a first plan. And seasonal hiring affects the 50-employee count: see <a href=\"/blog/seasonal-part-time-crew-health-insurance\">how part-time and seasonal crews are counted</a>.</p>"
         "<p>Full plan and cost details: <a href=\"/health-insurance-for-hvac-companies\">group health insurance for HVAC companies</a>.</p>"),
        ("sizes", "Sample benefits packages by company size", PACKAGES +
         "<p>Start with what you can sustain. A modest plan you keep for years does more for retention than a rich plan you have to cut after one bad renewal.</p>"),
        ("cost", "What benefits really cost vs. losing a tech",
         "<p>For a 10-tech shop paying an average of $450 per employee per month for employee-only coverage, health insurance runs about <strong>$54,000 a year</strong>. Premiums you pay for employees are generally a deductible business expense, and very small employers with lower average wages may qualify for the small business health care tax credit.</p>"
         "<p>Compare that with losing one experienced tech in July: recruiting, lost service calls, overtime for the rest of the crew, and callbacks while a new hire gets up to speed. Most owners who run that math find that benefits pay for themselves after one or two techs stay instead of leaving.</p>"),
        ("techs", "1099 techs and techs whose shop offers nothing",
         "<p>A genuine 1099 subcontractor can&rsquo;t join your group plan. If you control their hours, tools and methods, they may be employees in practice, which changes both your count and your obligations. See <a href=\"/blog/1099-crew-vs-w2-health-insurance\">1099 crews vs. W-2 employees</a>.</p>"
         "<p>HVAC techs who buy their own coverage, including self-employed contractors, often qualify for Marketplace tax credits based on net income. Send them to <a href=\"/health-insurance-for-hvac-technicians\">health insurance for HVAC technicians</a>.</p>"),
        ("jobpost", "Put your benefits in the job post",
         "<p>If you offer benefits, say so in the first lines of every job listing: &ldquo;Company-paid health insurance, dental and vision, paid holidays, EPA and NATE training paid.&rdquo; Techs scroll past listings that hide benefits, and shops that lead with them get more and better applicants.</p>"),
    ],
    faq=[
        ("What benefits do HVAC technicians want most?", "Health insurance comes first, followed by dental and vision, paid time off, a retirement match, a company truck, tools and phone, and paid training and certifications."),
        ("How much does health insurance cost for an HVAC company?", "Group coverage for a small trade business usually runs about $350 to $650 per employee per month for employee-only coverage, before the employer's contribution. Rates depend mostly on employee ages, ZIP code and plan design."),
        ("Does a small HVAC company have to offer health insurance?", "Not until it has 50 or more full-time equivalent employees. Under that, offering coverage is optional and there is no federal penalty. At 50 or more, the 2027 penalty for not offering coverage is $3,780 per full-time employee, minus the first 30."),
        ("What is the cheapest way for a small HVAC shop to offer health benefits?", "Many small shops start with an ICHRA or QSEHRA, which reimburse a set monthly amount toward each tech's own plan, or with a level-funded group plan for a young, healthy crew. Dental and vision are a low-cost first step."),
        ("Can I offer benefits to full-time techs and not part-time helpers?", "Yes. You can offer coverage to classes of employees based on the job, such as full-time versus part-time, as long as the classes aren't based on health."),
    ],
    sources=[
        ("U.S. Bureau of Labor Statistics: HVAC mechanics and installers, Occupational Outlook Handbook", "https://www.bls.gov/ooh/installation-maintenance-and-repair/heating-air-conditioning-and-refrigeration-mechanics-and-installers.htm"),
    ],
    related=[("Free quote", "Get a Group Quote for Your HVAC Company", Q.replace("&", "&amp;")),
             ("Guide", "Group Health Insurance for HVAC Companies", "/health-insurance-for-hvac-companies"),
             ("Techs", "Health Insurance for HVAC Technicians", "/health-insurance-for-hvac-technicians")],
)
def related(items):
    cards = "".join(
        '<a href="%s" style="background:var(--bg-soft);border:1px solid var(--line);border-radius:12px;padding:16px;text-decoration:none;display:block">'
        '<div style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">%s</div>'
        '<div style="font-weight:700;color:var(--blue-900);font-size:.95rem;line-height:1.4">%s</div></a>' % (href, k, t) for k, t, href in items)
    return ('<div style="margin-top:36px"><h3 style="margin-top:0">Related Pages</h3>'
            '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">%s</div></div>') % cards

IMG = "hvac-techs-checking-ac-unit"
hero = ('<div class="hero-img"><img src="/compressed/%s-900.jpg" srcset="/compressed/%s-900.jpg 900w, /compressed/%s.jpg 1600w" sizes="(max-width: 800px) 100vw, 760px" alt="%s" width="1600" height="900" fetchpriority="high" decoding="async" itemprop="image" /></div>'
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
        secs.append(cta("Think you&rsquo;re paying too much?", "A licensed advisor checks every plan and tax credit for your ZIP. Free, and you are never obligated to switch."))
toc = toc.replace('href="#review"', 'href="#rate-review"')
faq_html = "".join("<h3>%s</h3>\n<p>%s</p>\n" % (q, a) for q, a in A["faq"])
src_html = ('<h2 id="sources">Sources</h2><ul class="vs-src">' +
            "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, html.escape(t)) for t, u in A["sources"]) + "</ul>")
article = (
    '<nav class="breadcrumb" aria-label="Breadcrumb">\n    <a href="/">Home</a><span class="sep">&rsaquo;</span>\n'
    '    <a href="/blog">Blog</a><span class="sep">&rsaquo;</span>\n    <span>HVAC Employee Benefits</span>\n  </nav>\n'
    '</div><main class="container">\n  <div class="article-wrap">\n\n'
    '    <article class="article-body" itemscope itemtype="https://schema.org/Article">\n'
    '<meta itemprop="datePublished" content="%s" />\n<meta itemprop="dateModified" content="%s" />\n'
    '<span class="eyebrow">HVAC &amp; Trades | %d min read</span>\n%s\n'
    '<h1 itemprop="headline">%s</h1>\n<p class="lede">%s</p>\n%s\n\n'
    '<div class="alert-box"><div class="icon">%s</div><div><strong style="color:var(--ink)">The short answer</strong><br>'
    '<span style="color:var(--ink-2);font-size:.93rem">%s</span></div></div>\n\n'
    '%s\n\n<h2 id="faq">Frequently Asked Questions</h2>\n%s\n%s\n%s\n%s\n</article>\n\n'
    '    <aside class="article-sidebar">\n<a href="/blog" class="back-link">&larr; Back to Blog</a>\n'
    '<div class="sidebar-card"><h4>In This Article</h4><ul class="toc-list">%s</ul></div>\n'
    '<div class="sidebar-card" style="background:linear-gradient(135deg,var(--blue-700),var(--teal));border:none"><h4 style="color:#fff">Pricing benefits for your crew?</h4>'
    '<p style="color:rgba(255,255,255,.9);font-size:.88rem;margin-bottom:14px">We compare every carrier that writes HVAC groups, side by side. Free.</p>'
    '<a class="btn" href="/quote?from=blog/health-insurance-premiums-rising-2027" style="background:#fff;color:var(--blue-700);width:100%%;justify-content:center;font-weight:700">Get My Free Quote</a></div>\n'
    '<div class="sidebar-card"><h4>Prefer to talk?</h4><p style="font-size:.88rem;color:var(--muted);margin-bottom:10px">Call or text a licensed advisor. English y Espa&ntilde;ol.</p>'
    '<a href="tel:+19548251009" style="font-size:1.1rem;font-weight:700;color:var(--blue-700)">(954) 825-1009</a></div>\n'
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
s = s.replace("/quote?from=blog/health-insurance-premiums-rising-2027", Q.replace("&", "&amp;")).replace("from=blog-hvac-employee-benefits&amp;type=individual", "from=blog-hvac-employee-benefits&amp;type=business")
open("blog/%s.html" % SLUG, "w", encoding="utf-8").write(s)
print("wrote blog/%s.html" % SLUG, len(s))

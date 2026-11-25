#!/usr/bin/env python3
"""Build blog/other-ways-to-get-health-insurance.html (2026-11-18). Run from site root."""
import json, re, html

TPL = "blog/team-truck-drivers-health-insurance.html"
OLD_SLUG = "team-truck-drivers-health-insurance"
SITE = "https://www.vshealthbenefits.com"
DATE_ISO, DATE_LONG = "2026-11-18", "November 18, 2026"
SLUG = "other-ways-to-get-health-insurance"

tpl = open(TPL, encoding="utf-8").read()
META_DIV = re.search(r'<div class="article-meta">.*?</div>', tpl, re.S).group(0).replace("September 27, 2026", DATE_LONG)
ALERT_ICON = re.search(r'<div class="alert-box"><div class="icon">(.*?)</div>', tpl, re.S).group(1)
rr = open("premium-increase-review.html", encoding="utf-8").read()   # for the shared table style
QUAD = open(".seo-work/quad_snippet.html", encoding="utf-8").read()
Q = "/quote?from=blog/" + SLUG

def cta(h, p, href=Q, btn="Get Quotes &rarr;"):
    return '<div class="cta-block"><h3>%s</h3><p>%s</p><a class="btn btn-teal" href="%s">%s</a></div>' % (h, p, href, btn)

TABLE = ('<div class="vs-tw"><table class="vs-t" style="min-width:560px"><thead><tr><th>Option</th><th>Can you be turned down?</th><th>When you can enroll</th><th>Income-based tax credits</th><th>Best for</th></tr></thead><tbody>'
 '<tr><td><strong>ACA (Marketplace) plans</strong></td><td>No</td><td>Nov 1 &ndash; Jan 15, or after a life event</td><td>Yes</td><td>Pre-existing conditions; income that qualifies for help</td></tr>'
 '<tr><td><strong>Employer (group) plans</strong></td><td>No, if you&rsquo;re eligible</td><td>When hired or at the plan&rsquo;s open enrollment</td><td>No (the employer pays part)</td><td>Employees and business owners with staff</td></tr>'
 '<tr><td><strong>Medically underwritten plans</strong></td><td>Yes, based on health questions</td><td>Any time of year</td><td>No</td><td>Healthy people, often over the subsidy cliff</td></tr>'
 '<tr><td><strong>Short-term, discount &amp; MEC</strong></td><td>Short-term: yes</td><td>Usually any time</td><td>No</td><td>A short bridge, not long-term coverage</td></tr>'
 '</tbody></table></div><p class="vs-src">General rules. What&rsquo;s available, and the details, vary by state and carrier.</p>')

H1 = "Other Ways to Get Health Insurance Besides the Marketplace"
A = dict(
    title="Other Ways to Get Health Insurance Besides Obamacare (2027)",
    h1=H1,
    desc="The ACA Marketplace isn't your only option. The 4 ways to get health insurance in 2027, private plans you can buy year-round, and how to pick the right one.",
    keywords=["other ways to get health insurance", "alternatives to obamacare", "health insurance outside the marketplace", "types of health insurance plans",
              "ways to get health insurance", "health insurance options", "private health insurance vs obamacare", "health insurance outside open enrollment",
              "medically underwritten health insurance", "where to buy health insurance"],
    alt="Licensed insurance advisor helping a client compare health insurance options",
    mins=7,
    lede="Most people think health insurance comes from two places: a job or HealthCare.gov. There are actually four kinds of plans, and two of them are sold outside the Marketplace, some of them any time of year. If Marketplace prices are too high, you missed Open Enrollment, or you just want to see what else is out there, here is every option side by side.",
    short="There are <strong>four ways to get health insurance</strong>: <strong>ACA Marketplace plans</strong> and <strong>employer plans</strong> (you can&rsquo;t be turned down), and two private-market options: <strong>medically underwritten plans</strong>, which ask health questions but can cost less for healthy people and can be bought year-round, and <strong>short-term, discount or MEC plans</strong>, which are cheaper but limited. <a href=\"" + Q + "\">A licensed broker can quote all four</a>.",
    sections=[
        ("four-types", "The 4 types of health insurance plans",
         "<p>Every plan falls into one of four groups. The left side is the <strong>private market</strong>, where insurers can look at your health. The right side is <strong>guaranteed issue</strong>: you can&rsquo;t be turned down or charged more for a health condition.</p>"
         + QUAD +
         '<p style="font-size:.9rem"><a href="/guides/types-of-health-insurance-plans.pdf" target="_blank" rel="noopener">Download this as a one-page PDF</a></p>'),
        ("aca", "1. ACA Marketplace plans (Obamacare)",
         "<p>These are the plans on HealthCare.gov and state exchanges. Every one covers the essential health benefits, and insurers <strong>can&rsquo;t deny you or charge more for a pre-existing condition</strong>.</p>"
         "<ul><li><strong>Tax credits</strong> lower the premium based on your income. Check yours with our <a href=\"/aca-subsidy-calculator\">2027 subsidy calculator</a>.</li>"
         "<li><strong>When to enroll:</strong> Open Enrollment runs November 1 to January 15 in most states, or within 60 days of a qualifying life event.</li>"
         "<li><strong>The catch:</strong> if your income is above the subsidy cliff, you pay full price, and full price went up again for 2027.</li></ul>"),
        ("employer", "2. Employer (group) plans",
         "<p>Coverage through a job, or through your own business if you have employees. Eligible employees can&rsquo;t be turned down for health reasons, and the employer pays part of the premium.</p>"
         "<ul><li>If your employer offers affordable coverage, you usually can&rsquo;t get Marketplace tax credits instead.</li>"
         "<li>Own a business? Options include small group plans, level-funded plans and an <a href=\"/ichra-florida-small-business\">ICHRA</a>. See <a href=\"/small-business-health-insurance\">small business health insurance</a>.</li>"
         "<li>A one-person business, or a husband-and-wife business with no other employees, usually needs individual coverage instead.</li></ul>"),
        ("underwritten", "3. Medically underwritten private plans",
         "<p>This is the option most people have never heard of. These are private plans, often PPOs with national networks, sold <strong>outside the Marketplace</strong>. You answer health questions, and the insurer decides whether to offer coverage and at what price.</p>"
         "<ul><li><strong>Who it fits:</strong> healthy people, especially those earning too much for a tax credit, who would otherwise pay full Marketplace price.</li>"
         "<li><strong>You can apply any time of year</strong>, not just during Open Enrollment.</li>"
         "<li><strong>The catch:</strong> you can be declined, and some conditions can be limited or excluded. Read exactly what is covered before you switch.</li></ul>"
         "<p>More: <a href=\"/private-health-insurance\">private health insurance</a> &middot; <a href=\"/blog/benefits-of-private-health-insurance\">benefits of private health insurance</a></p>"),
        ("limited", "4. Short-term, discount and MEC plans",
         "<p>These are the lowest-cost options, and the most limited. They are not ACA coverage.</p>"
         "<ul><li><strong>Short-term plans</strong> cover some unexpected medical costs for a limited time and can exclude pre-existing conditions. How long one can last depends on your state, and the federal rules on their length are changing.</li>"
         "<li><strong>Discount plans</strong> are not insurance. They give you lower prices at participating providers, and you still pay the bill.</li>"
         "<li><strong>MEC (minimum essential coverage) plans</strong> mostly cover preventive care, such as checkups and screenings.</li></ul>"
         "<p>They can work as a <strong>bridge</strong> between jobs or until your next enrollment window. They are risky as your only coverage. See <a href=\"/short-term-health-insurance\">short-term health insurance</a> and <a href=\"/cobra-alternatives\">COBRA alternatives</a>.</p>"),
        ("compare", "All four options, side by side", TABLE),
        ("which", "Which option is right for you?",
         "<ul><li><strong>You have a health condition or take ongoing prescriptions:</strong> start with ACA or employer coverage, where you can&rsquo;t be turned down.</li>"
         "<li><strong>You&rsquo;re healthy and earn too much for a tax credit:</strong> compare a medically underwritten plan against full Marketplace price. The difference can be large.</li>"
         "<li><strong>You missed Open Enrollment:</strong> look at medically underwritten plans, which you can apply for year-round, or a short-term plan as a bridge.</li>"
         "<li><strong>You just lost a job:</strong> you have a special enrollment period for ACA plans. Compare it with COBRA before you pay COBRA&rsquo;s price.</li>"
         "<li><strong>You own a business with employees:</strong> compare group plans, level-funded plans and an ICHRA.</li></ul>"
         "<p>Still deciding? Our general guide covers <a href=\"/blog/how-to-shop-for-health-insurance\">how to shop for health insurance</a> step by step.</p>"),
    ],
    faq=[
        ("What are the other ways to get health insurance besides the Marketplace?", "Besides ACA Marketplace plans, you can get coverage through an employer (group) plan, a medically underwritten private plan sold outside the Marketplace, or a limited plan such as a short-term, discount or MEC plan."),
        ("Can I buy health insurance outside of Open Enrollment?", "Yes. Medically underwritten private plans and short-term plans can usually be bought any time of year. ACA Marketplace plans require Open Enrollment or a qualifying life event, such as losing other coverage."),
        ("Is private health insurance cheaper than Obamacare?", "It can be for healthy people who don't qualify for a Marketplace tax credit. If you qualify for a tax credit or have health conditions, an ACA plan is often the better deal. Compare both before you choose."),
        ("Can a private health plan deny me?", "Medically underwritten plans can decline coverage or limit some conditions based on your health answers. ACA and employer plans can't deny you for a health condition."),
        ("Are short-term health plans real insurance?", "They are insurance, but limited. They don't have to cover pre-existing conditions or all essential health benefits, and they only last for a limited time. Discount plans are not insurance at all."),
        ("Does it cost more to use a broker?", "No. Licensed brokers are paid by the insurance companies, so there is no charge to you, and a broker can compare options across all four types."),
    ],
    sources=[
        ("HealthCare.gov: Getting health coverage outside Open Enrollment", "https://www.healthcare.gov/coverage-outside-open-enrollment/special-enrollment-period/"),
        ("HealthCare.gov: Private plans outside the Marketplace", "https://www.healthcare.gov/private-plan-exceptions-outside-open-enrollment/"),
        ("NAIC: Short-term limited-duration health plans", "https://content.naic.org/insurance-topics/short-term-limited-duration-health-plans"),
    ],
    related=[("Free quote", "Get Health Insurance Quotes", Q),
             ("Guide", "How to Shop for Health Insurance: 4 Ways Compared", "/blog/how-to-shop-for-health-insurance"),
             ("Private plans", "Private Health Insurance", "/private-health-insurance")],
)
def related(items):
    cards = "".join(
        '<a href="%s" style="background:var(--bg-soft);border:1px solid var(--line);border-radius:12px;padding:16px;text-decoration:none;display:block">'
        '<div style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">%s</div>'
        '<div style="font-weight:700;color:var(--blue-900);font-size:.95rem;line-height:1.4">%s</div></a>' % (href, k, t) for k, t, href in items)
    return ('<div style="margin-top:36px"><h3 style="margin-top:0">Related Pages</h3>'
            '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">%s</div></div>') % cards

IMG = "insurance-advisor-woman"
hero = ('<div class="hero-img"><img src="/compressed/%s-900.jpg" srcset="/compressed/%s-900.jpg 900w, /compressed/%s.jpg 1200w" sizes="(max-width: 800px) 100vw, 760px" alt="%s" width="1200" height="800" fetchpriority="high" decoding="async" itemprop="image" /></div>'
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
    '    <a href="/blog">Blog</a><span class="sep">&rsaquo;</span>\n    <span>Other Ways to Get Health Insurance</span>\n  </nav>\n'
    '</div><main class="container">\n  <div class="article-wrap">\n\n'
    '    <article class="article-body" itemscope itemtype="https://schema.org/Article">\n'
    '<meta itemprop="datePublished" content="%s" />\n<meta itemprop="dateModified" content="%s" />\n'
    '<span class="eyebrow">Health Insurance Options | %d min read</span>\n%s\n'
    '<h1 itemprop="headline">%s</h1>\n<p class="lede">%s</p>\n%s\n\n'
    '<div class="alert-box"><div class="icon">%s</div><div><strong style="color:var(--ink)">The short answer</strong><br>'
    '<span style="color:var(--ink-2);font-size:.93rem">%s</span></div></div>\n\n'
    '%s\n\n<h2 id="faq">Frequently Asked Questions</h2>\n%s\n%s\n%s\n%s\n</article>\n\n'
    '    <aside class="article-sidebar">\n<a href="/blog" class="back-link">&larr; Back to Blog</a>\n'
    '<div class="sidebar-card"><h4>In This Article</h4><ul class="toc-list">%s</ul></div>\n'
    '<div class="sidebar-card" style="background:linear-gradient(135deg,var(--blue-700),var(--teal));border:none"><h4 style="color:#fff">Not sure which fits?</h4>'
    '<p style="color:rgba(255,255,255,.9);font-size:.88rem;margin-bottom:14px">A licensed advisor compares all four options for you, free.</p>'
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
open("blog/%s.html" % SLUG, "w", encoding="utf-8").write(s)
print("wrote blog/%s.html" % SLUG, len(s))

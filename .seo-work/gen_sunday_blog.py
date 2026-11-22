#!/usr/bin/env python3
"""Build blog/why-we-are-closed-on-sundays.html (2026-11-22). Run from site root."""
import json, re, html

TPL = "blog/team-truck-drivers-health-insurance.html"
OLD_SLUG = "team-truck-drivers-health-insurance"
SITE = "https://www.vshealthbenefits.com"
DATE_ISO, DATE_LONG = "2026-11-22", "November 22, 2026"
SLUG = "why-we-are-closed-on-sundays"

tpl = open(TPL, encoding="utf-8").read()
META_DIV = re.search(r'<div class="article-meta">.*?</div>', tpl, re.S).group(0).replace("September 27, 2026", DATE_LONG)
ALERT_ICON = re.search(r'<div class="alert-box"><div class="icon">(.*?)</div>', tpl, re.S).group(1)
rr = open("premium-increase-review.html", encoding="utf-8").read()
Q = "/quote?from=blog/" + SLUG

def cta(h, p, href=Q, btn="Get Quotes &rarr;"):
    return '<div class="cta-block"><h3>%s</h3><p>%s</p><a class="btn btn-teal" href="%s">%s</a></div>' % (h, p, href, btn)

HOURS = ('<div class="vs-tw"><table class="vs-t" style="min-width:0"><thead><tr><th>Day</th><th>Hours (Eastern)</th></tr></thead><tbody>'
         '<tr><td>Monday &ndash; Friday</td><td>8:00am &ndash; 8:00pm</td></tr>'
         '<tr><td>Saturday</td><td>10:00am &ndash; 5:00pm</td></tr>'
         '<tr><td>Sunday</td><td><strong>Closed</strong></td></tr></tbody></table></div>')

H1 = "Why VS Health Benefits Is Closed on Sundays"
A = dict(
    title="Is VS Health Benefits Open on Sunday? Hours & Why We’re Closed",
    h1=H1,
    desc="VS Health Benefits hours: Mon–Fri 8am–8pm and Sat 10am–5pm ET, closed Sundays for rest, family and worship. Call or text (954) 825-1009, or request a quote any day.",
    keywords=["vs health benefits hours", "is vs health benefits open on sunday", "vs health benefits open saturday", "vs health benefits phone number", "vs health benefits closed sunday", "health insurance agent open on weekends", "health insurance broker hours", "vs health benefits miami"],
    alt="Family walking together on the beach at sunset",
    mins=2,
    lede="If you&rsquo;ve tried to reach us on a Sunday, you may have noticed we&rsquo;re closed. That&rsquo;s on purpose, and here&rsquo;s why.",
    short="We&rsquo;re open <strong>Monday through Friday, 8am to 8pm</strong>, and <strong>Saturday, 10am to 5pm</strong> Eastern. Sundays are our day to rest, be with family and friends, and worship. You can still <a href=\"" + Q + "\">request a quote</a> any day, and we&rsquo;ll get back to you first thing Monday.",
    sections=[
        ("rest", "A day to rest",
         "<p>Open enrollment is our busiest time of year. We spend six days a week comparing plans, answering questions and helping families and business owners find coverage that fits. Taking Sunday off lets us recharge, so when we pick up the phone on Monday, you get our best.</p>"),
        ("family", "Time with family and friends",
         "<p>We help people protect the ones they love, and we want to make time for the ones we love, too. Sundays are for family dinners, time with friends, and simply enjoying ourselves.</p>"),
        ("faith", "Time to worship and give thanks",
         "<p>Sunday is also a day for us to worship and give thanks. We&rsquo;re grateful for every client who trusts us with something as important as their health coverage, and for the chance to do this work.</p>"),
        ("hours", "VS Health Benefits hours and how to reach us on a Sunday",
         HOURS + "<p>You don&rsquo;t have to wait to get started. Any day of the week, you can:</p><ul>"
         "<li><a href=\"" + Q + "\">Fill out a quote request</a>, and a licensed advisor will reach out during business hours.</li>"
         "<li>Try our <a href=\"/aca-subsidy-calculator\">2027 subsidy calculator</a> to estimate your price.</li>"
         "<li>Leave a voicemail or text us at <a href=\"tel:+19548251009\">(954) 825-1009</a>, and we&rsquo;ll get back to you Monday.</li></ul>"),
    ],
    faq=[
        ("Is VS Health Benefits open on Sundays?", "No. We are closed on Sundays so our team can rest, spend time with family and friends, and worship. We're open Monday through Friday from 8am to 8pm and Saturday from 10am to 5pm Eastern."),
        ("Can I request a quote on a Sunday?", "Yes. Our quote form is available any day. A licensed advisor will contact you during business hours, usually first thing Monday."),
        ("What are VS Health Benefits' hours?", "Monday through Friday from 8am to 8pm, and Saturday from 10am to 5pm, Eastern Time. We are closed on Sundays."),
        ("Is VS Health Benefits open on Saturday?", "Yes. We're open Saturday from 10am to 5pm Eastern, so you can talk to a licensed advisor on the weekend."),
        ("What is VS Health Benefits' phone number?", "Call or text (954) 825-1009. We help in English and Spanish. If you reach us after hours or on a Sunday, leave a message and we'll call you back the next business day."),
        ("Can I still sign up for health insurance on a Sunday?", "You can start any time by requesting a quote online, and we'll help you finish enrolling during business hours. For 2027 open enrollment, sign up by Tuesday, December 15, 2026 for coverage that starts January 1. Open enrollment ends Friday, January 15, 2027, so don't wait until the last weekend."),
        ("Where is VS Health Benefits located?", "We're a licensed independent health insurance brokerage based in Miami, Florida, and we help clients by phone and online in more than 40 states."),
    ],
    sources=[],
    related=[("Free quote", "Get a Free Health Insurance Quote", Q),
             ("Our team", "Meet the Team", "/meet-the-team"),
             ("Calculator", "2027 ACA Subsidy Calculator", "/aca-subsidy-calculator")],
)
def related(items):
    cards = "".join(
        '<a href="%s" style="background:var(--bg-soft);border:1px solid var(--line);border-radius:12px;padding:16px;text-decoration:none;display:block">'
        '<div style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">%s</div>'
        '<div style="font-weight:700;color:var(--blue-900);font-size:.95rem;line-height:1.4">%s</div></a>' % (href, k, t) for k, t, href in items)
    return ('<div style="margin-top:36px"><h3 style="margin-top:0">Related Pages</h3>'
            '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">%s</div></div>') % cards

IMG = "family-walking-beach-sunset"
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
src_html = "" if not A["sources"] else ('<h2 id="sources">Sources</h2><ul class="vs-src">' +
            "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, html.escape(t)) for t, u in A["sources"]) + "</ul>")
article = (
    '<nav class="breadcrumb" aria-label="Breadcrumb">\n    <a href="/">Home</a><span class="sep">&rsaquo;</span>\n'
    '    <a href="/blog">Blog</a><span class="sep">&rsaquo;</span>\n    <span>Why We&rsquo;re Closed on Sundays</span>\n  </nav>\n'
    '</div><main class="container">\n  <div class="article-wrap">\n\n'
    '    <article class="article-body" itemscope itemtype="https://schema.org/Article">\n'
    '<meta itemprop="datePublished" content="%s" />\n<meta itemprop="dateModified" content="%s" />\n'
    '<span class="eyebrow">From Our Team | %d min read</span>\n%s\n'
    '<h1 itemprop="headline">%s</h1>\n<p class="lede">%s</p>\n%s\n\n'
    '<div class="alert-box"><div class="icon">%s</div><div><strong style="color:var(--ink)">The short answer</strong><br>'
    '<span style="color:var(--ink-2);font-size:.93rem">%s</span></div></div>\n\n'
    '%s\n\n<h2 id="faq">Frequently Asked Questions</h2>\n%s\n%s\n%s\n%s\n</article>\n\n'
    '    <aside class="article-sidebar">\n<a href="/blog" class="back-link">&larr; Back to Blog</a>\n'
    '<div class="sidebar-card"><h4>In This Article</h4><ul class="toc-list">%s</ul></div>\n'
    '<div class="sidebar-card" style="background:linear-gradient(135deg,var(--blue-700),var(--teal));border:none"><h4 style="color:#fff">Need a quote?</h4>'
    '<p style="color:rgba(255,255,255,.9);font-size:.88rem;margin-bottom:14px">Send us your info any day of the week. We&rsquo;ll get back to you during business hours.</p>'
    '<a class="btn" href="/quote?from=blog/why-we-are-closed-on-sundays" style="background:#fff;color:var(--blue-700);width:100%%;justify-content:center;font-weight:700">Get My Free Quote</a></div>\n'
    '<div class="sidebar-card"><h4>Prefer to talk?</h4><p style="font-size:.88rem;color:var(--muted);margin-bottom:10px">Call or text a licensed advisor. English y Espa&ntilde;ol.</p>'
    '<a href="tel:+19548251009" style="font-size:1.1rem;font-weight:700;color:var(--blue-700)">(954) 825-1009</a><p style="font-size:.82rem;color:var(--muted);margin:8px 0 0">Mon&ndash;Fri 8am&ndash;8pm, Sat 10am&ndash;5pm ET. Closed Sundays.</p></div>\n'
    '</aside>\n  </div>\n</main>'
) % (DATE_ISO, DATE_ISO, A["mins"], META_DIV, H1, A["lede"], hero, ALERT_ICON, A["short"].replace('href=\\"#review\\"', 'href="#rate-review"').replace('href="#review"', 'href="#rate-review"'),
     "\n\n".join(secs), faq_html,
     cta("Ready when you are", "Fill out a quote any day, even Sunday. A licensed advisor will reach out during business hours. Free, no obligation."),
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

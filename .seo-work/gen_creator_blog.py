#!/usr/bin/env python3
"""Build blog/vs-health-benefits-creator-program-launch.html from the blog template.
Run from the site root:  python3 .seo-work/gen_creator_blog.py   (2026-11-15)
"""
import json, re, html

TPL = "blog/team-truck-drivers-health-insurance.html"
OLD_SLUG = "team-truck-drivers-health-insurance"
SITE = "https://www.vshealthbenefits.com"
DATE_ISO = "2026-11-15"
DATE_LONG = "November 15, 2026"
SLUG = "vs-health-benefits-creator-program-launch"
IMG = "creator-program-launch"

tpl = open(TPL, encoding="utf-8").read()
META_DIV = re.search(r'<div class="article-meta">.*?</div>', tpl, re.S).group(0).replace("September 27, 2026", DATE_LONG)
ALERT_ICON = re.search(r'<div class="alert-box"><div class="icon">(.*?)</div>', tpl, re.S).group(1)

STATES = ["Alabama", "Arkansas", "Colorado", "Delaware", "Florida", "Georgia", "Illinois", "Indiana", "Iowa", "Kansas",
          "Kentucky", "Louisiana", "Maryland", "Michigan", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
          "North Carolina", "Ohio", "Oklahoma", "Pennsylvania", "South Carolina", "South Dakota", "Tennessee", "Texas",
          "Utah", "Virginia", "West Virginia", "Wisconsin", "Wyoming"]

A = dict(
    title="VS Health Benefits Launches Creator & Affiliate Program (2026)",
    h1="VS Health Benefits Launches Its Creator and Affiliate Program",
    desc="VS Health Benefits launched a creator and affiliate program. Share your link and earn a flat reward for every referral who completes a free consultation.",
    keywords=["health insurance affiliate program", "health insurance referral program", "insurance affiliate program for creators",
              "health insurance creator program", "influencer affiliate program", "VS Health Benefits creator program",
              "earn money referring health insurance"],
    alt="VS Health Benefits Creator Program: share your link and earn a flat reward for every qualified referral",
    w=1600, h=700, mins=5,
    lede="We just launched the VS Health Benefits Creator Program. If you have an audience of self-employed people, truck drivers, families or small business owners, you can now share your own personal link and earn a flat reward for every person who completes a free consultation with our team.",
    short="The <strong>VS Health Benefits Creator Program</strong> is free to join. Approved creators get a personal link, a live dashboard and a <strong>flat reward for every referral who completes a free consultation</strong> with a licensed advisor, whether or not they buy. You never sell or explain insurance; our advisors handle that. <a href=\"/affiliate-program\">Apply here</a>.",
    sections=[
        ("what", "What the Creator Program is",
         "<p>Most of our best clients found us the same way: someone they trust told them, <em>\"Call VS Health Benefits. They'll actually help you.\"</em> The Creator Program is how we thank the people who already do that.</p>"
         "<p>It is a <strong>health insurance referral program for creators</strong>: content creators, podcasters, community leaders, trucking pages and anyone whose audience needs honest help with health coverage. You share your link. We do everything else.</p>"),
        ("how", "How it works, step by step",
         "<ol>"
         "<li><strong>Apply.</strong> Fill out the short application on our <a href=\"/affiliate-program\">Creator Program page</a>. It takes about two minutes.</li>"
         "<li><strong>Get approved.</strong> We review every application within 2 business days and text and email you the decision.</li>"
         "<li><strong>Set up your login.</strong> Your approval message includes a personal setup link, good for 48 hours, that takes you straight into your creator dashboard to pick a username and password.</li>"
         "<li><strong>Share your link.</strong> You get one personal link, like <em>vshealthbenefits.com/yourname</em>. Anyone who opens it is credited to you for 90 days on every page of our site, including the quote form.</li>"
         "<li><strong>We help your audience.</strong> A licensed advisor compares plans for them for free, with no pressure.</li>"
         "<li><strong>You earn your reward.</strong> When someone you referred completes a free consultation, it counts as a qualified referral. We text and email you at each step.</li>"
         "</ol>"),
        ("who", "Who the program is for",
         "<p>The program is a fit if your audience includes people who often struggle to find good coverage:</p>"
         "<ul>"
         "<li><strong>Self-employed and 1099 workers</strong>, freelancers and gig workers</li>"
         "<li><strong>Truck drivers and owner-operators</strong>, including <a href=\"/truck-driver-health-insurance\">drivers who need coverage that works on the road</a></li>"
         "<li><strong>Families</strong> facing higher premiums in 2027</li>"
         "<li><strong>Small business owners</strong> thinking about <a href=\"/small-business-health-insurance\">group health benefits</a> for their team</li>"
         "</ul>"
         "<p>You do not need an insurance license, and you never quote prices or explain plans. That is our job.</p>"),
        ("rewards", "How rewards work",
         "<p>You earn a <strong>flat reward for every qualified referral</strong>, meaning a person who used your link and completed a free consultation with one of our licensed advisors. Your reward does not depend on whether they buy a plan. That keeps it simple for you and fair for the people you refer.</p>"
         "<p>Creators also move up <strong>tiers</strong> as their qualified referrals grow: <strong>Beginner</strong> (0 to 4), <strong>Rising</strong> (5 to 14), <strong>Pro</strong> (15 to 29) and <strong>Elite</strong> (30 and up). Your current tier and your progress to the next one are always on your dashboard.</p>"
         "<p style=\"font-size:.9rem;color:var(--muted)\">Rewards are a flat amount per qualified referral and are never tied to whether anyone buys insurance (s. 626.112(8), Florida Statutes). Where state law does not allow referral rewards, we cannot pay one.</p>"),
        ("dashboard", "Your creator dashboard",
         "<p>Every approved creator gets a private dashboard at <a href=\"/creator\">vshealthbenefits.com/creator</a>. Sign in with your username and password, or with a one-time email link. It shows:</p>"
         "<ul>"
         "<li>Your personal link, ready to copy or share</li>"
         "<li>Link visits over the last 30 days and all time</li>"
         "<li>Quote requests and qualified referrals</li>"
         "<li>What you have earned, what is on the way and what has been paid</li>"
         "<li>Your tier and how close you are to the next one</li>"
         "</ul>"
         "<p>For their privacy, we never share who your referrals are or anything about their coverage. You see a date and a status for each one, nothing more.</p>"),
        ("rules", "A few simple rules",
         "<ul>"
         "<li><strong>Share your own experience in your own words.</strong></li>"
         "<li><strong>Label sponsored posts</strong> with #ad or #partner.</li>"
         "<li><strong>Do not quote prices, plans or coverage details.</strong> Our licensed advisors handle every insurance question.</li>"
         "</ul>"),
        ("states", "States we can help",
         "<p>Our licensed advisors can help people in these %d states, so these are the best places to focus your sharing:</p><p>%s.</p>"
         "<p>If someone outside these states uses your link, we may not be able to help them yet.</p>" % (len(STATES), ", ".join(STATES))),
        ("why", "Why we built it",
         "<p>\"Health insurance is confusing, and the people who need help the most usually hear about it from someone they follow, not from an ad,\" said <a href=\"/bradley-vilsaint\">Bradley Vilsaint</a>, Founder and CEO of VS Health Benefits. \"The Creator Program lets us reward the people who point their audience toward honest help, without ever asking them to sell insurance.\"</p>"),
    ],
    faq=[
        ("Is the VS Health Benefits Creator Program free to join?", "Yes. There is no cost to apply or to participate. Apply on our <a href=\"/affiliate-program\">Creator Program page</a>."),
        ("Do I need an insurance license to be a creator?", "No. Creators only share their personal link. Our licensed advisors handle every conversation about plans, prices and coverage."),
        ("Do my referrals have to buy insurance for me to earn a reward?", "No. You earn a flat reward when someone you referred completes a free consultation with our team, whether or not they buy."),
        ("How long is a visitor credited to my link?", "90 days. Anyone who opens your link is credited to you on every page of our site for 90 days, even if they leave and come back later."),
        ("How do I log in to my creator dashboard?", "Go to <a href=\"/creator\">vshealthbenefits.com/creator</a> and sign in with your username and password, or ask for a one-time email sign-in link. New creators set up their login from the personal link in their approval message."),
        ("How long does approval take?", "We review every application within 2 business days and text and email you our decision."),
    ],
    related=[("Program", "Apply to the Creator Program", "/affiliate-program"),
             ("Dashboard", "Creator Login", "/creator"),
             ("Company", "Meet Our Founder, Bradley Vilsaint", "/bradley-vilsaint")],
)


def cta(h, p, href="/affiliate-program", btn="Apply to the Creator Program"):
    return '<div class="cta-block"><h3>%s</h3><p>%s</p><a class="btn btn-teal" href="%s">%s</a></div>' % (h, p, href, btn)


def related(items):
    cards = "".join(
        '<a href="%s" style="background:var(--bg-soft);border:1px solid var(--line);border-radius:12px;padding:16px;text-decoration:none;display:block">'
        '<div style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px">%s</div>'
        '<div style="font-weight:700;color:var(--blue-900);font-size:.95rem;line-height:1.4">%s</div></a>' % (href, kind, title)
        for kind, title, href in items)
    return ('<div style="margin-top:36px"><h3 style="margin-top:0">Related Pages</h3>'
            '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">%s</div></div>') % cards


def hero():
    i, w, h = IMG, A["w"], A["h"]
    return ('<div class="hero-img"><picture><source type="image/webp" srcset="/compressed/{i}-640.webp 640w, /compressed/{i}-900.webp 900w, /compressed/{i}.webp {w}w" '
            'sizes="(max-width: 800px) 100vw, 760px"><img src="/compressed/{i}-900.jpg" srcset="/compressed/{i}-640.webp 640w, /compressed/{i}.webp {w}w" '
            'sizes="(max-width: 760px) 100vw, 760px" alt="{a}" width="{w}" height="{h}" fetchpriority="high" decoding="async" itemprop="image" /></picture></div>'
            ).format(i=i, a=html.escape(A["alt"], quote=True), w=w, h=h)


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
s = re.sub(r'<link rel="preload" as="image"[^>]*>',
           '<link rel="preload" as="image" type="image/webp" href="/compressed/{i}.webp" imagesrcset="/compressed/{i}-640.webp 640w, /compressed/{i}-900.webp 900w, /compressed/{i}.webp 1600w" imagesizes="(max-width: 800px) 100vw, 760px" fetchpriority="high" />'.format(i=IMG),
           s, count=1)

blog_ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": A["h1"], "description": A["desc"], "image": img_full,
           "author": {"@type": "Person", "name": "Bradley Vilsaint", "url": SITE + "/bradley-vilsaint"},
           "publisher": {"@type": "Organization", "name": "VS Health Benefits", "logo": {"@type": "ImageObject", "url": SITE + "/favicon.png"}},
           "datePublished": DATE_ISO, "dateModified": DATE_ISO, "mainEntityOfPage": {"@type": "WebPage", "@id": url},
           "keywords": A["keywords"], "articleSection": "Company News",
           "about": {"@type": "Thing", "name": "VS Health Benefits Creator Program", "url": SITE + "/affiliate-program"}}
crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
    {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog"},
    {"@type": "ListItem", "position": 3, "name": A["h1"]}]}
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in A["faq"]]}
lds = list(re.finditer(r'<script type="application/ld\+json">.*?</script>', s, re.S))
for m, payload in reversed(list(zip(lds[:3], [blog_ld, crumb_ld, faq_ld]))):
    s = s[:m.start()] + '<script type="application/ld+json">\n' + json.dumps(payload, ensure_ascii=False) + "\n</script>" + s[m.end():]

toc = "".join('<li><a href="#%s">%s</a></li>' % (sid, h2) for sid, h2, _ in A["sections"]) + '<li><a href="#faq">FAQ</a></li>'
secs = []
for i, (sid, h2, body) in enumerate(A["sections"]):
    secs.append('<h2 id="%s">%s</h2>\n%s' % (sid, h2, body))
    if i == 1:
        secs.append(cta("Ready to share your link?", "Apply in about two minutes. We review every application within 2 business days."))
faq_html = "".join("<h3>%s</h3>\n<p>%s</p>\n" % (q, a) for q, a in A["faq"])
article = (
    '<nav class="breadcrumb" aria-label="Breadcrumb">\n    <a href="/">Home</a><span class="sep">&rsaquo;</span>\n'
    '    <a href="/blog">Blog</a><span class="sep">&rsaquo;</span>\n    <span>%s</span>\n  </nav>\n'
    '</div><main class="container">\n  <div class="article-wrap">\n\n'
    '    <article class="article-body" itemscope itemtype="https://schema.org/Article">\n'
    '<meta itemprop="datePublished" content="%s" />\n<meta itemprop="dateModified" content="%s" />\n'
    '<span class="eyebrow">Company News | %d min read</span>\n%s\n'
    '<h1 itemprop="headline">%s</h1>\n<p class="lede">%s</p>\n%s\n\n'
    '<div class="alert-box"><div class="icon">%s</div><div><strong style="color:var(--ink)">The short answer</strong><br>'
    '<span style="color:var(--ink-2);font-size:.93rem">%s</span></div></div>\n\n'
    '%s\n\n<h2 id="faq">Frequently Asked Questions</h2>\n%s\n%s\n%s\n</article>\n\n'
    '    <aside class="article-sidebar">\n<a href="/blog" class="back-link">&larr; Back to Blog</a>\n'
    '<div class="sidebar-card"><h4>In This Article</h4><ul class="toc-list">%s</ul></div>\n'
    '<div class="sidebar-card" style="background:linear-gradient(135deg,var(--blue-700),var(--teal));border:none"><h4 style="color:#fff">Become a Creator</h4>'
    '<p style="color:rgba(255,255,255,.9);font-size:.88rem;margin-bottom:14px">Get your own link and earn a flat reward for every referral who completes a free consultation.</p>'
    '<a class="btn" href="/affiliate-program" style="background:#fff;color:var(--blue-700);width:100%%;justify-content:center;font-weight:700">Apply Now</a></div>\n'
    '<div class="sidebar-card"><h4>Already a Creator?</h4><p style="font-size:.88rem;color:var(--muted);margin-bottom:10px">See your visits, referrals and rewards.</p>'
    '<a href="/creator" style="font-size:1rem;font-weight:700;color:var(--blue-700)">Creator Login &rarr;</a></div>\n'
    '<div class="sidebar-card"><h4>Questions?</h4><p style="font-size:.88rem;color:var(--muted);margin-bottom:10px">Email info@vshealthbenefits.com or text us. Include your name and the word "Affiliate."</p>'
    '<a href="tel:+19548251009" style="font-size:1.1rem;font-weight:700;color:var(--blue-700)">(954) 825-1009</a></div>\n'
    '</aside>\n  </div>\n</main>'
) % (A["h1"], DATE_ISO, DATE_ISO, A["mins"], META_DIV, A["h1"], A["lede"], hero(), ALERT_ICON, A["short"],
     "\n\n".join(secs), faq_html,
     cta("Join the VS Health Benefits Creator Program", "Free to join. No license needed. Share your link and we handle the rest."),
     related(A["related"]), toc)
b = s.index('<nav class="breadcrumb"')
e = s.index("</main>", b) + len("</main>")
s = s[:b] + article + s[e:]
s = s.replace(OLD_SLUG, SLUG).replace("&amp;niche=trucking", "").replace("&niche=trucking", "")
assert "Team Truck Drivers" not in s, "template text leaked"
open("blog/%s.html" % SLUG, "w", encoding="utf-8").write(s)
print("wrote blog/%s.html" % SLUG)

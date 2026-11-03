import re, json, sys, os, html
ROOT = os.path.expanduser("~/mnt/VS-BENEFITS")
sys.path.insert(0, os.path.join(ROOT, "_build"))
from content_posts import POSTS, DATE, DATE_H
SITE = "https://www.vshealthbenefits.com"

def one(s, old, new, n=1):
    c = s.count(old)
    if c != n: raise SystemExit("expected %d of %r, found %d" % (n, old[:80], c))
    return s.replace(old, new)

def sub1(s, pat, new, flags=re.S):
    out, k = re.subn(pat, lambda m: new, s, count=1, flags=flags)
    if k != 1: raise SystemExit("pattern not found: " + pat[:80])
    return out

GENERAL_BAR = '<div id="oe-annc-bar" style="background:linear-gradient(135deg,#16447f,#0db5a6);color:#fff;text-align:center;padding:9px 16px;font-family:Inter,system-ui,-apple-system,sans-serif;font-size:.9rem;font-weight:600;line-height:1.35"><span style="display:inline-flex;gap:10px;align-items:center;justify-content:center;flex-wrap:wrap"><span><a href="/blog/aca-open-enrollment-2027-guide" style="color:#fff;text-decoration:underline;text-underline-offset:3px">Open Enrollment for 2027 coverage runs Nov 1 &ndash; Jan 15. Enroll by Dec 15 for a January 1 start.</a></span><a href="/quote?from=oe-bar-general" style="background:#fff;color:#16447f;border-radius:999px;padding:3px 12px;font-weight:800;white-space:nowrap;text-decoration:none">Get a Free Quote &rarr;</a></span></div>'

ICON_CAL = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:1em;height:1em;display:inline-block;vertical-align:-.14em" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>'
ICON_PEN = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:1em;height:1em;display:inline-block;vertical-align:-.14em" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>'
ICON_PIN = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:1em;height:1em;display:inline-block;vertical-align:-.14em" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>'

def build_post(p):
    T = open(os.path.join(ROOT, "blog/owner-operator-health-insurance-increase-2027.html"), encoding="utf-8").read()
    OS = "owner-operator-health-insurance-increase-2027"
    OH1 = "Owner-Operator Health Insurance Going Up in 2027? 8 Ways to Cut the Cost"
    OT = "Owner-Operator Health Insurance Going Up in 2027?"
    OD = "Rates are up, the 400% subsidy cliff is back and Cigna is leaving the Marketplace. 8 ways owner-operators and truck drivers cut their 2027 health insurance cost."
    slug, e = p["slug"], html.escape
    s = T
    # page-level text
    s = one(s, OH1, e(p["h1"]), 3)              # json-ld headline, breadcrumb json-ld, h1
    s = one(s, "<title>" + OT + "</title>", "<title>" + e(p["title"]) + "</title>")
    s = one(s, 'content="' + OT + '"', 'content="' + e(p["title"]) + '"', 2)
    s = one(s, "<span>" + OT + "</span>", "<span>" + e(p["title"]) + "</span>")
    s = one(s, OD, e(p["desc"]), 4)
    s = s.replace("/compressed/woman-reading-insurance-notice.jpg", "/compressed/" + p["img"])
    s = one(s, "2026-10-04T08:00:00-05:00", DATE + "T08:00:00-04:00")
    s = s.replace('"datePublished": "2026-10-04"', '"datePublished": "%s"' % DATE).replace('"dateModified": "2026-10-04"', '"dateModified": "%s"' % DATE)
    # FAQ schema
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}
    s = sub1(s, r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>',
             '<script type="application/ld+json">\n' + json.dumps(faq, indent=2, ensure_ascii=False) + '\n</script>')
    # article
    if p["audience"] == "trucker":
        pillar = '<p class="vs-pillar-link" style="font-size:.95rem;color:#334155">New to this? Start with our guide to <a href="/truck-driver-health-insurance">health insurance for truck drivers</a>, including where drivers in each state enroll.</p>'
        qb = ('<aside class="vs-bq" aria-label="Get a truck driver quote">\n<strong class="t">Get your driver quote in about 60 seconds</strong>\n'
              '<p>A licensed advisor checks every plan and tax credit for your home ZIP code, including PPO options that work on the road. Free, no obligation.</p>\n'
              '<form action="/trucking-health-quote" method="get"><input type="hidden" name="from" value="blog-%s"><input name="zip" inputmode="numeric" pattern="[0-9]{5}" maxlength="5" placeholder="Home ZIP code" aria-label="Home ZIP code" required autocomplete="postal-code"><button type="submit">See my plans &rarr;</button></form>\n'
              '<span class="alt">Driving right now? <a href="tel:+19548251009">Speak to an advisor</a> when you\'re parked.</span>\n</aside>') % slug
    else:
        pillar = '<p class="vs-pillar-link" style="font-size:.95rem;color:#334155">Open Enrollment for 2027 runs November 1 to January 15. Dates and deadlines: <a href="/blog/aca-open-enrollment-2027-guide">Open Enrollment 2027 guide</a>.</p>'
        qb = p["quote_box"]
    faq_html = "\n".join("<h3>%s</h3>\n<p>%s</p>" % (e(q), e(a)) for q, a in p["faq"])
    art = ('<article class="article-body" itemscope itemtype="https://schema.org/Article">\n'
           '      <meta itemprop="datePublished" content="%s" />\n      <meta itemprop="dateModified" content="%s" />\n'
           '      <span class="eyebrow">%s</span>\n      <div class="article-meta">\n'
           '        <span>%s %s</span>\n        <span>%s VS Health Benefits Team</span>\n        <span>%s Miami, FL</span>\n      </div>\n'
           '      <h1 itemprop="headline">%s</h1>\n      <p class="lede">%s</p>\n'
           '      <div class="hero-img">\n        <img src="/compressed/%s" alt="%s" width="1200" height="525" itemprop="image" />\n      </div>\n\n'
           '      %s\n%s\n%s\n%s\n    </article>') % (DATE, DATE, e(p["eyebrow"]), ICON_CAL, DATE_H, ICON_PEN, ICON_PIN,
            e(p["h1"]), e(p["lede"]), p["img"], e(p["img_alt"]), pillar, qb, p["body"].strip(), faq_html)
    s = sub1(s, r'<article class="article-body".*?</article>', art)
    toc = "".join('<li><a href="#%s">%s</a></li>' % (a, e(b)) for a, b in p["toc"])
    side = ('<aside class="article-sidebar">\n      <a href="/blog" class="back-link">← Back to Blog</a>\n      <div class="sidebar-card">\n        <h4>In This Article</h4>\n'
            '        <ul class="toc-list">%s</ul>\n      </div>\n'
            '      <div class="sidebar-card" style="background:linear-gradient(135deg,var(--blue-700),var(--teal));border:none">\n        <h4 style="color:#fff">%s</h4>\n'
            '        <p style="color:rgba(255,255,255,.9);font-size:.88rem;margin-bottom:14px">%s</p>\n'
            '        <a class="btn btn-teal" href="%s" style="background:#fff;color:var(--blue-700);width:100%%;justify-content:center">Get Started →</a>\n      </div>\n'
            '      <div class="sidebar-card">\n        <h4>Prefer to talk?</h4>\n        <p style="font-size:.88rem;color:var(--muted);margin-bottom:10px">Mon–Fri 8am–6pm · Sat–Sun 8am–1pm ET</p>\n'
            '        <a href="tel:+19548251009" style="font-size:1.1rem;font-weight:700;color:var(--blue-700)">(954) 825-1009</a>\n      </div>\n    </aside>') % (toc, e(p["side_h"]), e(p["side_p"]), p["side_href"])
    s = sub1(s, r'<aside class="article-sidebar">.*?</aside>', side)
    cards = "".join('\n        <a class="vs-rg-card" href="%s">\n          <strong>%s</strong>\n          <span>%s</span>\n          <em>Read the guide &rarr;</em>\n        </a>' % (h, e(t), e(d)) for h, t, d in p["related"])
    rel = ('<section class="vs-related-guides" data-block="%s">\n  <div class="vs-rg-inner">\n    <h2>%s</h2>\n    <p class="vs-rg-sub">%s</p>\n    <div class="vs-rg-grid">%s\n    </div>\n  </div>\n</section>') % (slug, e(p["related_h"]), p["related_sub"], cards)
    s = sub1(s, r'<section class="vs-related-guides".*?</section>', rel)
    if p["audience"] != "trucker":
        s = sub1(s, r'<div id="oe-annc-bar".*?</div>', GENERAL_BAR)
        s = s.replace("/trucking-health-quote?from=blog-" + OS, p["quote_path"] + "?from=blog-" + slug)
    s = s.replace(OS, slug)
    for bad in [OS, "Owner-Operator Health Insurance Going Up", "8 Ways to Cut"]:
        if bad in s: raise SystemExit("leftover %r in %s" % (bad, slug))
    out = os.path.join(ROOT, "blog", slug + ".html")
    if os.path.exists(out) and "--force" not in sys.argv: raise SystemExit("exists: " + out)
    open(out, "w", encoding="utf-8").write(s)
    print("wrote", out, len(s))

if __name__ == "__main__":
    for p in POSTS: build_post(p)

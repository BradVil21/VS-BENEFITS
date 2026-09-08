# -*- coding: utf-8 -*-
"""Build new VS Health Benefits pages that reuse the live site chrome.

Everything structural (CSS, header, footer, login modal, tail scripts, org
schema) is lifted verbatim from a donor page so new pages cannot drift from
the rest of the site. Only the meta block, the page schema and <main> are new.
"""
import re, os, json

DONOR = "group-health-insurance-for-dump-truck-fleets.html"
SITE  = "https://www.vshealthbenefits.com"

def _read(p):
    return open(p, encoding="utf-8").read()

def _grab(pat, s, name, flags=re.S):
    m = re.search(pat, s, flags)
    if not m:
        raise SystemExit("page_lib: could not find %s in donor" % name)
    return m.group(0)

class Chrome:
    def __init__(self, donor=DONOR):
        d = _read(donor)
        self.gtag = _grab(r'<script async src="https://www\.googletagmanager\.com.*?</script>\s*<script>.*?</script>', d, "gtag")
        self.style_main = _grab(r'<style>\s*:root\{--blue-900.*?</style>', d, "main style")
        self.style_rg = _grab(r'<style id="vs-rg-style">.*?</style>', d, "vs-rg-style")
        self.style_carrier = _grab(r'<style id="carrier-logo-css">.*?</style>', d, "carrier css")
        self.org_schema = _grab(r'<script type="application/ld\+json">\s*\{"@context":"https://schema\.org","@type":"InsuranceAgency".*?</script>', d, "org schema")
        self.fonts = _grab(r'<link rel="icon".*?rel="stylesheet" />', d, "fonts")
        self.header = _grab(r'<header class="site-header">.*?</header>', d, "header")
        self.footer = _grab(r'<footer>.*?</footer>', d, "footer")
        self.tail = _grab(r'<div class="modal-backdrop" id="login-modal".*?</body>', d, "tail")
        # The donor is itself a trucking page, so a previous wiring pass may have
        # injected the sticky call bar into it. Strip anything this library adds
        # back, or every page built afterwards inherits a duplicate.
        self.tail = re.sub(r'<div id="vs-callbar".*?</script>\s*', '', self.tail, flags=re.S)
        self.tail = re.sub(r'<section class="vs-related-guides" data-block="vs-trucking-tools">.*?</section>\s*',
                           '', self.tail, flags=re.S)
        for attr in ("header", "footer", "style_main"):
            v = re.sub(r'<div id="vs-callbar".*?</script>\s*', '', getattr(self, attr), flags=re.S)
            setattr(self, attr, v)

    def page(self, slug, title, description, keywords, main, schemas,
             og_image="/compressed/hvac-rooftop-technician.jpg",
             related_block="", lang="en", hreflang=None, sticky_call=True,
             body_extra=""):
        url = SITE + "/" + slug.lstrip("/")
        esc = lambda t: t.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
        parts = []
        parts.append("<!DOCTYPE html>")
        parts.append('<html lang="%s">' % lang)
        parts.append("<head>")
        parts.append(self.gtag)
        parts.append('<meta charset="utf-8" />')
        parts.append('<meta name="viewport" content="width=device-width, initial-scale=1" />')
        parts.append("<title>%s</title>" % esc(title))
        parts.append('<meta name="description" content="%s" />' % esc(description))
        parts.append('<meta name="keywords" content="%s" />' % esc(keywords))
        parts.append('<link rel="canonical" href="%s" />' % url)
        parts.append('<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1" />')
        for hl in (hreflang or []):
            parts.append('<link rel="alternate" hreflang="%s" href="%s%s" />' % (hl[0], SITE, hl[1]))
        parts.append('<meta property="og:type" content="website" />')
        parts.append('<meta property="og:title" content="%s" />' % esc(title))
        parts.append('<meta property="og:description" content="%s" />' % esc(description))
        parts.append('<meta property="og:url" content="%s" />' % url)
        parts.append('<meta property="og:site_name" content="VS Health Benefits" />')
        parts.append('<meta property="og:image" content="%s%s" />' % (SITE, og_image))
        parts.append('<meta name="twitter:card" content="summary_large_image" />')
        parts.append(self.fonts)
        parts.append(self.style_main)
        parts.append(self.style_rg)
        parts.append(self.style_carrier)
        if sticky_call:
            parts.append(STICKY_CSS)
        parts.append(self.org_schema)
        for s in schemas:
            parts.append('<script type="application/ld+json">\n%s\n</script>'
                         % json.dumps(s, ensure_ascii=False, separators=(",", ":")))
        parts.append("</head>")
        parts.append("<body>")
        parts.append('<div id="vs-scroll-bar"></div>')
        parts.append(self.header)
        parts.append(main)
        if related_block:
            parts.append(related_block)
        parts.append(self.footer)
        if sticky_call:
            parts.append(STICKY_HTML)
        parts.append(body_extra)
        parts.append(self.tail)
        parts.append("</html>")
        return "\n".join(p for p in parts if p)

# --- sticky mobile click-to-call -------------------------------------------
# Truck drivers search from the cab. On a phone the call button is the
# conversion; the form is not. Hidden >=760px so desktop is untouched.
STICKY_CSS = """<style id="vs-sticky-call">
#vs-callbar{position:fixed;left:0;right:0;bottom:0;z-index:120;display:flex;gap:8px;padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.97);backdrop-filter:saturate(160%) blur(8px);border-top:1px solid var(--line);box-shadow:0 -6px 18px rgba(13,27,42,.10)}
#vs-callbar a{flex:1;display:flex;align-items:center;justify-content:center;gap:7px;min-height:48px;border-radius:999px;font-weight:700;font-size:.95rem;text-decoration:none;line-height:1.1}
#vs-callbar .vs-call{background:var(--teal-dark);color:#fff}
#vs-callbar .vs-quote{background:var(--blue-700);color:#fff}
#vs-callbar a:hover{text-decoration:none;color:#fff}
body{padding-bottom:0}
@media(max-width:759px){body{padding-bottom:76px}#back-to-top{bottom:88px}}
@media(min-width:760px){#vs-callbar{display:none}}
</style>"""

STICKY_HTML = """<div id="vs-callbar" role="region" aria-label="Contact a licensed advisor">
  <a class="vs-call" href="tel:+19548251009" data-vs-cta="sticky-call"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.3 2.2z"/></svg>Call an advisor</a>
  <a class="vs-quote" href="/quote" data-vs-cta="sticky-quote">Get my quote</a>
</div>
<script>(function(){var b=document.getElementById("vs-callbar");if(!b)return;b.addEventListener("click",function(e){var a=e.target.closest("a[data-vs-cta]");if(!a)return;try{if(window.vsTrack)window.vsTrack(a.getAttribute("data-vs-cta")==="sticky-call"?"contact_call":"quote_start",{lead_type:"sticky_bar"});}catch(_){}});})();</script>"""

# --- shared builders --------------------------------------------------------
def faq_schema(pairs):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in pairs]}

def breadcrumbs(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":SITE+u} for i,(n,u) in enumerate(items)]}

def article_schema(slug, headline, description, published, modified=None):
    return {"@context":"https://schema.org","@type":"Article","headline":headline,
            "description":description,"datePublished":published,
            "dateModified":modified or published,
            "mainEntityOfPage":{"@type":"WebPage","@id":SITE+"/"+slug.lstrip("/")},
            "author":{"@type":"Person","name":"Bradley Vilsaint",
                      "url":SITE+"/bradley-vilsaint",
                      "jobTitle":"Licensed Health Insurance Advisor"},
            "publisher":{"@type":"Organization","name":"VS Health Benefits",
                         "url":SITE+"/","logo":{"@type":"ImageObject","url":SITE+"/favicon.png"}}}

def faq_html(pairs):
    out = ['<div class="faq">']
    for q, a in pairs:
        out.append('<details class="faq-item"><summary>%s</summary><p>%s</p></details>' % (q, a))
    out.append("</div>")
    return "\n".join(out)

def write(slug, html):
    path = slug.lstrip("/") + ".html"
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    open(path, "w", encoding="utf-8").write(html)
    return path

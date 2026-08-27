# -*- coding: utf-8 -*-
"""Shared shell for the TX / MD / KY small-business state hubs.

Reuses the site chrome (head, header, footer) from an existing page and the
proven .vs-ih component styles from build_tampa.py. Each state's copy is written
fresh in its own build_*.py - no find/replace siblings.
"""
import re, json

BASE = 'https://www.vshealthbenefits.com'
SRC  = 'tampa-small-business-health-insurance.html'

STYLE = '''<style id="vs-st-style">
.vs-ih{padding:52px 0}
.vs-ih .vs-ih-inner{width:100%;max-width:1160px;margin:0 auto;padding:0 18px}
.vs-ih h2{font-family:'Poppins','Inter',system-ui,sans-serif;color:#0b2346;font-size:1.55rem;margin:0 0 10px;line-height:1.25}
.vs-ih h3.sub{font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1.08rem;margin:26px 0 8px}
.vs-ih p.lede{color:#3d4c5f;font-size:1.02rem;line-height:1.7;max-width:800px;margin:0 0 22px}
.vs-ih-key{background:#f2f7fd;border:1px solid #d6e6f7;border-left:4px solid #16447f;border-radius:12px;padding:20px 22px;margin:0 0 28px;max-width:880px}
.vs-ih-key>strong{display:block;color:#0b2346;font-size:1.04rem;margin-bottom:6px}
.vs-ih-key p strong,.vs-ih-key li strong{display:inline;color:#0b2346;font-weight:700;font-size:inherit;margin:0}
.vs-ih-key p{margin:0 0 12px;color:#3d4c5f;font-size:.97rem;line-height:1.68}
.vs-ih-key p:last-child{margin-bottom:0}
.vs-ih-grid{display:grid;grid-template-columns:1fr;gap:14px}
.vs-ih-card{display:block;background:#fff;border:1px solid #e4e9f2;border-radius:14px;padding:19px 21px;text-decoration:none}
.vs-ih-card strong{display:block;font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1.02rem;margin-bottom:6px}
.vs-ih-card span{display:block;color:#5a6b80;font-size:.91rem;line-height:1.6}
a.vs-ih-card:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(13,27,42,.09);text-decoration:none}
.vs-ih-card em{display:inline-block;margin-top:9px;color:#16447f;font-weight:700;font-size:.85rem;font-style:normal}
.vs-ih-faq{border-bottom:1px solid #eceff4;padding:16px 0}
.vs-ih-faq:last-child{border-bottom:0}
.vs-ih-faq h3{font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1.02rem;margin:0 0 6px}
.vs-ih-faq p{margin:0;color:#4a5a6e;font-size:.95rem;line-height:1.68}
.vs-ih-cta{display:inline-block;background:#16447f;color:#fff;font-weight:700;font-size:1rem;padding:15px 32px;border-radius:999px;text-decoration:none}
.vs-ih-cta:hover{background:#0e3266;color:#fff;text-decoration:none}
.vs-ih-band{background:#0b2346;color:#fff;padding:44px 0}
.vs-ih-band h2{color:#fff}.vs-ih-band p{color:#c9d4e2;max-width:680px;margin:0 0 20px;line-height:1.65}
.vs-ih-panel{background:#fff;border:1px solid #e4e9f2;border-radius:16px;padding:24px 26px;box-shadow:0 10px 30px rgba(13,27,42,.07)}
.vs-ih-dl>div{display:flex;justify-content:space-between;gap:16px;padding:9px 0;border-bottom:1px solid #f0f2f6}
.vs-ih-dl>div:last-child{border-bottom:0}
.vs-ih-dl dt{color:#7a8798;font-size:.83rem;font-weight:600;margin:0;flex:0 0 42%}
.vs-ih-dl dd{color:#0b2346;font-size:.88rem;font-weight:600;margin:0;text-align:right;line-height:1.4}
.vs-ih-tbl{width:100%;border-collapse:collapse;margin:0 0 22px;font-size:.93rem}
.vs-ih-tbl th{text-align:left;background:#f2f7fd;color:#0b2346;font-weight:700;padding:11px 13px;border-bottom:2px solid #d6e6f7;font-size:.86rem}
.vs-ih-tbl td{padding:11px 13px;border-bottom:1px solid #eceff4;color:#3d4c5f;line-height:1.55;vertical-align:top}
.vs-ih-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.vs-ih-src{font-size:.82rem;color:#7a8798;line-height:1.6;margin:0 0 6px}
.vs-ih-src a{color:#16447f}
@media(min-width:760px){.vs-ih-grid{grid-template-columns:1fr 1fr}}
</style>'''


def build(out, url, title, desc, region, placename, body, faq, schema_extra):
    """Assemble a state hub page from the site chrome + fresh body copy."""
    s = open(SRC, encoding='utf-8').read()
    head_end = s.index('</head>')
    hdr = s[s.index('<header'):s.index('</header>') + 9]
    tail = s[s.rindex('<footer'):]
    h = s[:head_end]

    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, h, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")(.*?)(")',
               lambda m: m.group(1) + desc + m.group(3), h, count=1, flags=re.S)
    h = re.sub(r'(<link rel="canonical" href=")(.*?)(")',
               lambda m: m.group(1) + url + m.group(3), h, count=1)
    for p, v in [('og:title', title), ('og:description', desc), ('og:url', url)]:
        h = re.sub(r'(<meta property="%s" content=")(.*?)(")' % re.escape(p),
                   lambda m, v=v: m.group(1) + v + m.group(3), h, count=1, flags=re.S)
    for n, v in [('twitter:title', title), ('twitter:description', desc)]:
        h = re.sub(r'(<meta name="%s" content=")(.*?)(")' % re.escape(n),
                   lambda m, v=v: m.group(1) + v + m.group(3), h, count=1, flags=re.S)
    h = re.sub(r'<meta name="geo.region" content="[^"]*"',
               '<meta name="geo.region" content="%s"' % region, h)
    h = re.sub(r'<meta name="geo.placename" content="[^"]*"',
               '<meta name="geo.placename" content="%s"' % placename, h)

    # strip the source page's page-level schema
    spans = []
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        if d.get('@type') in ('FAQPage', 'Article', 'Service', 'BreadcrumbList', 'WebPage'):
            spans.append((m.start(), m.end()))
    for a, b in reversed(spans):
        h = h[:a] + h[b:]

    schema = list(schema_extra) + [{
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    schema_html = ''.join('<script type="application/ld+json">\n%s\n</script>\n'
                          % json.dumps(x, indent=2) for x in schema)

    faq_html = ''.join('\n        <div class="vs-ih-faq"><h3>%s</h3><p>%s</p></div>'
                       % (q, a) for q, a in faq)
    body = body.replace('__FAQ__', faq_html)

    BAR = ('<div id="oe-annc-bar" style="background:linear-gradient(135deg,#16447f,#0db5a6);color:#fff;'
           'text-align:center;padding:9px 16px;font-family:Inter,system-ui,-apple-system,sans-serif;'
           'font-size:.9rem;font-weight:600;line-height:1.35"><a href="/quote" style="color:#fff;'
           'text-decoration:none;display:inline-flex;gap:10px;align-items:center;justify-content:center;'
           'flex-wrap:wrap"><span>Open Enrollment for 2027 coverage runs Nov 1 &ndash; Jan 15. '
           'Get ahead of the deadline.</span><span style="background:#fff;color:#16447f;border-radius:999px;'
           'padding:3px 12px;font-weight:800;white-space:nowrap">Get a Free Quote &rarr;</span></a></div>')
    out_html = (h + STYLE + '\n' + schema_html + '</head>\n<body>\n' + BAR
                + '\n\n<div id="vs-scroll-bar"></div>\n\n' + hdr + '\n' + body + tail)
    open(out, 'w', encoding='utf-8').write(out_html)
    print('wrote %s (%d bytes, ~%d words)'
          % (out, len(out_html), len(re.sub(r'<[^>]*>', ' ', body).split())))


def provider(city, state_code):
    return {"@type": "InsuranceAgency", "name": "VS Health Benefits", "url": BASE + "/",
            "telephone": "+1-954-825-1009", "email": "info@vshealthbenefits.com",
            "address": {"@type": "PostalAddress", "addressLocality": "Miami",
                        "addressRegion": "FL", "addressCountry": "US"}}

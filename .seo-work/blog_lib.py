# -*- coding: utf-8 -*-
"""Shared shell for the FL/TX/MD/KY small-business blog cluster.

Reuses the blog article chrome from an existing post; each post's copy is written
fresh in its own build_post_*.py.
"""
import re, json

BASE = 'https://www.vshealthbenefits.com'
SRC = 'blog/how-to-set-up-small-business-health-insurance-florida.html'


def build(slug, title, h1, desc, lede, published, read_min, eyebrow,
          img, alt, toc, body, faq, cta_head, cta_copy):
    url = BASE + '/blog/' + slug
    s = open(SRC, encoding='utf-8').read()
    head_end = s.index('</head>')
    h = s[:head_end]
    rest = s[head_end:]

    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, h, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")(.*?)(")',
               lambda m: m.group(1) + desc + m.group(3), h, count=1, flags=re.S)
    h = re.sub(r'(<link rel="canonical" href=")(.*?)(")',
               lambda m: m.group(1) + url + m.group(3), h, count=1)
    for p, v in [('og:title', title), ('og:description', desc), ('og:url', url),
                 ('og:image', BASE + img), ('article:published_time', published + 'T08:00:00-05:00')]:
        h = re.sub(r'(<meta property="%s" content=")(.*?)(")' % re.escape(p),
                   lambda m, v=v: m.group(1) + v + m.group(3), h, count=1, flags=re.S)
    for n, v in [('twitter:title', title), ('twitter:description', desc),
                 ('twitter:image', BASE + img)]:
        h = re.sub(r'(<meta name="%s" content=")(.*?)(")' % re.escape(n),
                   lambda m, v=v: m.group(1) + v + m.group(3), h, count=1, flags=re.S)
    # multi-state posts: drop the FL-only geo hints
    h = re.sub(r'\s*<meta name="geo.region" content="[^"]*"\s*/?>', '', h)
    h = re.sub(r'\s*<meta name="geo.placename" content="[^"]*"\s*/?>', '', h)

    spans = []
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        if d.get('@type') in ('FAQPage', 'Article', 'Service', 'BreadcrumbList', 'WebPage', 'BlogPosting'):
            spans.append((m.start(), m.end()))
    for a, b in reversed(spans):
        h = h[:a] + h[b:]

    org = {"@type": "Organization", "name": "VS Health Benefits", "url": BASE,
           "logo": {"@type": "ImageObject", "url": BASE + "/favicon.png"}}
    schema = [
        {"@context": "https://schema.org", "@type": "Article", "headline": h1,
         "description": desc, "image": BASE + img, "author": org, "publisher": org,
         "datePublished": published, "dateModified": published,
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "/blog"},
            {"@type": "ListItem", "position": 3, "name": h1}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]
    schema_html = ''.join('<script type="application/ld+json">\n%s\n</script>\n'
                          % json.dumps(x, indent=2) for x in schema)

    TBL = ("<style id=\"vs-post-tbl\">.article-body .vs-tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:22px 0}"
           ".article-body table.vs-t{width:100%;border-collapse:collapse;font-size:.93rem;min-width:520px}"
           ".article-body table.vs-t th{text-align:left;background:var(--blue-50);color:var(--blue-700);font-weight:700;"
           "padding:11px 13px;border-bottom:2px solid var(--blue-100);font-size:.86rem}"
           ".article-body table.vs-t td{padding:11px 13px;border-bottom:1px solid #eceff4;line-height:1.55;vertical-align:top}"
           ".article-body .vs-src{font-size:.82rem;color:var(--muted);line-height:1.6;margin:14px 0 22px}</style>")
    h = h + TBL + '\n'
    out = h + schema_html + rest

    # breadcrumb trail label
    out = re.sub(r'(<a href="/blog">Blog</a><span class="sep">›</span>\s*<span>)(.*?)(</span>)',
                 lambda m: m.group(1) + title + m.group(3), out, count=1, flags=re.S)

    # article body: everything between the hero image div and </article>
    a = out.index('<div class="hero-img">')
    b = out.index('</article>')
    head_block = (
        '<div class="hero-img">\n'
        '        <img src="%s" alt="%s" width="1200" height="525" itemprop="image" />\n'
        '      </div>\n\n      %s\n    ' % (img, alt, body))
    out = out[:a] + head_block + out[b:]

    # meta line above H1
    out = re.sub(r'<meta itemprop="datePublished" content="[^"]*"',
                 '<meta itemprop="datePublished" content="%s"' % published, out, count=1)
    out = re.sub(r'<meta itemprop="dateModified" content="[^"]*"',
                 '<meta itemprop="dateModified" content="%s"' % published, out, count=1)
    out = re.sub(r'<span class="eyebrow">.*?</span>',
                 '<span class="eyebrow">%s | %d min read</span>' % (eyebrow, read_min),
                 out, count=1, flags=re.S)
    import datetime
    d = datetime.date.fromisoformat(published)
    nice = '%s %d, %d' % (d.strftime('%B'), d.day, d.year)
    out = re.sub(r'(</svg>\s*)[A-Z][a-z]+ \d{1,2}, \d{4}', lambda m: m.group(1) + nice, out, count=1)
    out = re.sub(r'(</svg>\s*)Miami, FL', lambda m: m.group(1) + 'Miami, FL', out, count=1)
    out = re.sub(r'<h1 itemprop="headline">.*?</h1>',
                 '<h1 itemprop="headline">%s</h1>' % h1, out, count=1, flags=re.S)
    out = re.sub(r'<p class="lede">.*?</p>',
                 '<p class="lede">%s</p>' % lede, out, count=1, flags=re.S)

    # sidebar
    toc_html = ''.join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in toc)
    out = re.sub(r'<ul class="toc-list">.*?</ul>',
                 '<ul class="toc-list">%s</ul>' % toc_html, out, count=1, flags=re.S)
    out = re.sub(r'<h4 style="color:#fff">.*?</h4>',
                 '<h4 style="color:#fff">%s</h4>' % cta_head, out, count=1, flags=re.S)
    out = re.sub(r'(<p style="color:rgba\(255,255,255,\.9\);font-size:\.88rem;margin-bottom:14px">)(.*?)(</p>)',
                 lambda m: m.group(1) + cta_copy + m.group(3), out, count=1, flags=re.S)
    out = out.replace('href="/quote" style="background:#fff;color:var(--blue-700);width:100%',
                      'href="/quote?type=business" style="background:#fff;color:var(--blue-700);width:100%')

    path = 'blog/' + slug + '.html'
    open(path, 'w', encoding='utf-8').write(out)
    words = len(re.sub(r'<[^>]*>', ' ', body).split())
    print('wrote %s (%d bytes, ~%d words)' % (path, len(out), words))

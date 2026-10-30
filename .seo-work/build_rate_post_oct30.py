# -*- coding: utf-8 -*-
"""2026-10-30: /blog/health-insurance-rate-increases-2027-by-state, built from the why-did-my-health-insurance-go-up-2027 template."""
import json, re, html
m = json.load(open('.seo-work/rate_post_meta.json', encoding='utf-8'))
body = open('.seo-work/rate_post_body.html', encoding='utf-8').read()
OLD = 'why-did-my-health-insurance-go-up-2027'
s = open('blog/%s.html' % OLD, encoding='utf-8').read()
olddesc = 'Florida Marketplace rates rose about 10% for 2027 and some insurers left. The 7 reasons your premium went up, and how to lower it before Dec 15.'
esc = lambda x: html.escape(x, quote=True)
# article body + FAQ schema first (they contain the old slug / text)
a = s.index('<p class="vs-pillar-link"'); b = s.index('    </article>')
s = s[:a] + body + '\n' + s[b:]
faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in m['faq']]}
s = re.sub(r'(<script type="application/ld\+json">\s*)\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>',
           lambda _: '<script type="application/ld+json">\n' + json.dumps(faq, indent=2, ensure_ascii=False) + '\n</script>', s, count=1, flags=re.S)
# sidebar TOC
s = re.sub(r'<ul class="toc-list">.*?</ul>', '<ul class="toc-list"><li><a href="#short">The Short Answer</a></li><li><a href="#chart">Increases by State</a></li><li><a href="#table">Full Table</a></li><li><a href="#florida">Florida</a></li><li><a href="#dollars">What It Means in Dollars</a></li><li><a href="#do">What to Do</a></li><li><a href="#faq">FAQ</a></li></ul>', s, count=1, flags=re.S)
# head/meta/hero
s = s.replace('Why Did My Health Insurance Go Up in 2027? 7 Reasons and What to Do', m['h1'])
s = s.replace('Why Did My Health Insurance Go Up in 2027? 7 Reasons', m['title'])
s = s.replace(olddesc, esc(m['desc']))
s = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">%s</p>' % m['lede'], s, count=1, flags=re.S)
s = s.replace('woman-reading-insurance-notice', '2027-rate-increases-by-state')
s = s.replace('alt="Woman reading a 2027 health insurance premium increase letter at home" width="1200" height="525"',
              'alt="2027 health insurance rate increases by state: 16% average, Arizona highest at 29%" width="1200" height="630"')
s = s.replace('2026-10-27', '2026-10-30').replace('October 27, 2026', 'October 30, 2026').replace('Open Enrollment 2027 | 8 min read', 'Open Enrollment 2027 | ' + m['read'])
# related cards: swap the renewal-notice card for the why-did post
s = re.sub(r'<a class="vs-rg-card" href="/blog/health-insurance-renewal-notice-2027">.*?</a>',
           '<a class="vs-rg-card" href="/blog/why-did-my-health-insurance-go-up-2027">\n          <strong>Why Did My Premium Go Up?</strong>\n          <span>The 7 reasons 2027 premiums rose, and which ones you can fix before December 15.</span>\n          <em>Read the guide &rarr;</em>\n        </a>', s, count=1, flags=re.S)
s = s.replace('<h2>Paying more in 2027? Start here</h2>', '<h2>Rates going up? Start here</h2>')
s = s.replace(OLD + '"', m['slug'] + '"').replace(OLD + '&', m['slug'] + '&').replace('blog-' + OLD, m['FROM']).replace('blog/' + OLD + '"', 'blog/' + m['slug'] + '"')
s = s.replace('/blog/' + m['slug'] + '">\n          <strong>Why Did', '/blog/' + OLD + '">\n          <strong>Why Did')  # keep the card pointing at the old post
# chart styles
css = ('.article-body .vs-rchart{margin:18px 0 26px;padding:16px 14px 10px;border:1px solid var(--line);border-radius:14px;background:#fff}'
       '.article-body .vs-rchart figcaption{display:flex;flex-wrap:wrap;gap:16px;font-size:.85rem;color:var(--muted);margin-top:8px;padding-left:6px}'
       '.article-body .vs-rchart i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:-1px}')
s = s.replace('<style id="vs-post-tbl">', '<style id="vs-post-tbl">' + css, 1)
open('blog/%s.html' % m['slug'], 'w', encoding='utf-8').write(s)
left = [l for l in s.split('\n') if OLD in l]
print('written; lines still mentioning old slug:', len(left))
for l in left: print('  ', l.strip()[:160])

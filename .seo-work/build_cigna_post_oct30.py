# -*- coding: utf-8 -*-
"""2026-10-30: /blog/cigna-leaving-aca-marketplace-2027 from the why-did template."""
import json, re, html
m = json.load(open('.seo-work/cigna_post_meta.json', encoding='utf-8'))
body = open('.seo-work/cigna_post_body.html', encoding='utf-8').read()
OLD = 'why-did-my-health-insurance-go-up-2027'; S = m['slug']; IMG = m['img']
s = open('blog/%s.html' % OLD, encoding='utf-8').read()
olddesc = 'Florida Marketplace rates rose about 10% for 2027 and some insurers left. The 7 reasons your premium went up, and how to lower it before Dec 15.'
a = s.index('<p class="vs-pillar-link"'); b = s.index('    </article>')
s = s[:a] + body + '\n' + s[b:]
faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(t)}} for q, t in m['faq']]}
s = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>',
           lambda _: '<script type="application/ld+json">\n' + json.dumps(faq, indent=2, ensure_ascii=False) + '\n</script>', s, count=1, flags=re.S)
toc = ''.join('<li><a href="#%s">%s</a></li>' % tuple(t) for t in m['toc'])
s = re.sub(r'<ul class="toc-list">.*?</ul>', '<ul class="toc-list">%s</ul>' % toc, s, count=1, flags=re.S)
s = s.replace('Why Did My Health Insurance Go Up in 2027? 7 Reasons and What to Do', m['h1'])
s = s.replace('Why Did My Health Insurance Go Up in 2027? 7 Reasons', m['title'])
s = s.replace(olddesc, html.escape(m['desc'], quote=True))
s = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">%s</p>' % m['lede'], s, count=1, flags=re.S)
s = s.replace('woman-reading-insurance-notice', IMG)
s = re.sub(r'(<div class="hero-img">.*?</div>)', lambda mm: mm.group(1).replace(IMG + '-900.jpg', IMG + '-hero-900.jpg').replace(IMG + '.jpg', IMG + '-hero.jpg'), s, count=1, flags=re.S)
s = s.replace('alt="Woman reading a 2027 health insurance premium increase letter at home" width="1200" height="525"', 'alt="%s" width="1200" height="525"' % m['alt'])
s = s.replace('2026-10-27', '2026-10-30').replace('October 27, 2026', 'October 30, 2026').replace('Open Enrollment 2027 | 8 min read', 'Open Enrollment 2027 | ' + m['read'])
s = re.sub(r'<a class="vs-rg-card" href="/blog/health-insurance-renewal-notice-2027">.*?</a>',
           '<a class="vs-rg-card" href="/blog/health-insurance-rate-increases-2027-by-state">\n          <strong>2027 Rate Increases by State</strong>\n          <span>Average 2027 increases in 32 states, and what they mean for your monthly bill.</span>\n          <em>Read the guide &rarr;</em>\n        </a>', s, count=1, flags=re.S)
s = s.replace('<h2>Paying more in 2027? Start here</h2>', '<h2>Losing your Cigna plan? Start here</h2>')
s = s.replace('<h4 style="color:#fff">Premium went up?</h4>', '<h4 style="color:#fff">Have a Cigna plan?</h4>')
s = s.replace('Tell us your 2026 and 2027 premium. We check every plan and credit for your ZIP, free.', 'We compare every 2027 plan in your ZIP and check your doctors, free.')
s = s.replace(OLD + '"', S + '"').replace(OLD + '&', S + '&').replace('blog-' + OLD, m['FROM'])
open('blog/%s.html' % S, 'w', encoding='utf-8').write(s)
print('written; old slug lines:', [l.strip()[:120] for l in s.split('\n') if OLD in l])

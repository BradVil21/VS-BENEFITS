# -*- coding: utf-8 -*-
"""Wire /private-health-insurance into the site: service card on the three hub
pages, footer link everywhere, redirects for the natural alternates."""
import re, glob, json, io

CARD = '''      <div class="card">
        <div class="card-image"><img src="/compressed/independent.jpg" alt="Private market health insurance plans" loading="lazy" /></div>
        <div class="card-body">
          <div class="ic">P</div>
          <h3>Private Market</h3>
          <p>Medically underwritten plans outside the Marketplace, for healthy applicants above the subsidy cutoff. Open year-round.</p>
          <a href="/private-health-insurance" style="font-weight:700;color:var(--blue-700);font-size:.9rem">Private health insurance &rarr;</a>
        </div>
      </div>
'''

FOOTER_LI = '          <li><a href="/private-health-insurance">Private Market Plans</a></li>\n'

def add_card(f):
    s = open(f, encoding='utf-8').read()
    if '/private-health-insurance' in s and 'Private Market</h3>' in s:
        return 'already'
    m = re.search(r'<h3>ACA ?/ ?Individual[^<]*</h3>', s)
    if not m:
        return 'no ACA card'
    nxt = s.find('<div class="card">', m.end())
    if nxt == -1:
        return 'no following card'
    line_start = s.rfind('\n', 0, nxt) + 1
    s = s[:line_start] + CARD + s[line_start:]
    open(f, 'w', encoding='utf-8').write(s)
    return 'card added'

for f in ['index.html', 'services.html', 'health-insurance.html']:
    print(f, '->', add_card(f))

# footer link on every page that carries the Solutions column
n = 0
for f in sorted(glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('quote/*.html')):
    s = open(f, encoding='utf-8').read()
    if 'href="/private-health-insurance">Private Market Plans' in s:
        continue
    m = re.search(r'[ \t]*<li><a href="/ppo-health-insurance">PPO Plans</a></li>\n', s)
    if not m:
        continue
    s = s[:m.end()] + FOOTER_LI + s[m.end():]
    open(f, 'w', encoding='utf-8').write(s)
    n += 1
print('footer link added to', n, 'pages')

# redirects
v = json.load(open('vercel.json', encoding='utf-8'))
have = {r['source'] for r in v['redirects']}
add = [('/private-health-insurance.html', '/private-health-insurance'),
       ('/private-market-health-insurance', '/private-health-insurance'),
       ('/non-marketplace-health-insurance', '/private-health-insurance'),
       ('/private-ppo-health-insurance', '/private-health-insurance'),
       ('/private-health-insurance-plans', '/private-health-insurance')]
added = 0
for src, dst in add:
    if src in have:
        continue
    v['redirects'].append({'source': src, 'destination': dst, 'permanent': True})
    added += 1
if added:
    open('vercel.json', 'w', encoding='utf-8').write(json.dumps(v, indent=2, ensure_ascii=False) + '\n')
print('redirects added:', added, 'total:', len(v['redirects']))

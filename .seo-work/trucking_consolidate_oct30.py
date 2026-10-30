# -*- coding: utf-8 -*-
"""2026-10-30: fold 6 thin fleet pages + 4 thin city pages into their parent pages.
301s in vercel.json, internal links removed or repointed, so no link hits a redirect."""
import re, glob, json, sys
DRY = '--dry' in sys.argv
B = 'https://www.vshealthbenefits.com'
TC = '/health-insurance-for-trucking-companies'
FLEET = {s: TC for s in [
 '/group-health-insurance-for-refrigerated-trucking-companies',
 '/group-health-insurance-for-heavy-haul-trucking-companies',
 '/group-health-insurance-for-oilfield-trucking-companies',
 '/group-health-insurance-for-dump-truck-fleets',
 '/group-health-insurance-for-delivery-fleets',
 '/group-health-insurance-for-freight-brokers']}
CITY_REDIRECT = {
 '/truck-driver-health-insurance-atlanta-ga': '/truck-driver-health-insurance?state=GA',
 '/truck-driver-health-insurance-memphis-tn': '/truck-driver-health-insurance?state=TN',
 '/truck-driver-health-insurance-indianapolis-in': '/truck-driver-health-insurance?state=IN',
 '/truck-driver-health-insurance-dallas-tx': '/truck-driver-health-insurance-texas'}
CITY_LINK = {k: ('/truck-driver-health-insurance-texas' if 'dallas' in k else '/truck-driver-health-insurance#by-state')
             for k in CITY_REDIRECT}
OLD = {**FLEET, **CITY_LINK}
OLDFILES = {s.lstrip('/') + '.html' for s in OLD}

def hre(slug):  # href="slug" or absolute, optional query/hash
    return r'href="(?:%s)?%s(?:[?#][^"]*)?"' % (re.escape(B), re.escape(slug))

CARD = r'<a class="(?:vs-rg-card|vs-ih-card|hub-card|rel-card|rc)"[^>]*?%s[^>]*>.*?</a>'
TC_CARD = ('<a class="vs-rg-card" href="%s">\n          <strong>Group Health for Trucking Companies</strong>\n'
           '          <span>Reefer, flatbed and heavy haul, dump, oilfield and drayage: what each fleet needs from a group plan, and what it costs per driver.</span>\n'
           '          <em>Read the guide &rarr;</em>\n        </a>') % TC

files = [f for f in glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('guides/*.html') + glob.glob('truckers/*.html') + glob.glob('quote/*.html')
         if f not in OLDFILES]
stats = {}
def bump(k, n=1): stats[k] = stats.get(k, 0) + n
changed = []
for f in files:
    s0 = s = open(f, encoding='utf-8').read()
    is_tc = f == TC.lstrip('/') + '.html'
    # a) cards. Fleet: first fleet card in each related-guides block becomes one trucking-companies card.
    def fix_block(m):
        blk = m.group(0)
        put = (not is_tc) and (('href="%s"' % TC) not in blk)
        for slug in OLD:
            def card(mm):
                nonlocal put
                bump('card removed')
                if slug in FLEET and put and 'vs-rg-card' in mm.group(0):
                    put = False; bump('tc card added'); return TC_CARD
                return ''
            blk = re.sub(CARD % hre(slug), card, blk, flags=re.S)
        return blk
    s = re.sub(r'<section[^>]*>.*?</section>', fix_block, s, flags=re.S)
    for slug, tgt in OLD.items():
        h = hre(slug)
        n0 = len(re.findall(h, s))
        if not n0: continue
        s = re.sub(CARD % h, '', s, flags=re.S)                                      # stray cards
        s = re.sub(r'<li>\s*<a [^>]*?%s[^>]*>.*?</a>\s*</li>' % h, '', s, flags=re.S)  # list items
        s = re.sub(r'\s*&middot;\s*<a [^>]*?%s[^>]*>[^<]*</a>' % h, '', s)            # " · link"
        s = re.sub(r'<a [^>]*?%s[^>]*>[^<]*</a>\s*&middot;\s*' % h, '', s)            # "link · "
        s = re.sub(r'<a [^>]*?%s[^>]*>[^<]*&rarr;</a>' % h, '', s)                    # "Memphis ... →" CTAs
        # remaining prose links: repoint (or unlink if the page would link to itself)
        if is_tc and tgt == TC:
            s, n = re.subn(r'<a [^>]*?%s[^>]*>(.*?)</a>' % h, r'\1', s, flags=re.S); bump('self-link unwrapped', n)
        else:
            s, n = re.subn(h, 'href="%s"' % tgt, s); bump('prose link repointed', n)
    if s != s0:
        changed.append(f)
        if not DRY: open(f, 'w', encoding='utf-8').write(s)

# hub: Texas replaces the city list
hub = 'truck-driver-health-insurance.html'
s = open(hub, encoding='utf-8').read()
if 'href="/truck-driver-health-insurance-texas">Texas Drivers' not in s:
    s2 = s.replace('<li><a href="/truck-driver-health-insurance-florida">Florida Drivers</a></li>',
                   '<li><a href="/truck-driver-health-insurance-florida">Florida Drivers</a></li><li><a href="/truck-driver-health-insurance-texas">Texas Drivers</a></li>', 1)
    if s2 != s:
        bump('hub texas li'); 
        if not DRY: open(hub, 'w', encoding='utf-8').write(s2)

# trucking companies page: delivery + broker section
f = TC.lstrip('/') + '.html'; s = open(f, encoding='utf-8').read()
if 'id="delivery-brokers"' not in s:
    add = ('<h3 id="delivery-brokers">Delivery fleets, freight brokers and 3PLs</h3>\n'
           '<p>Last-mile delivery and DSP operations hire young drivers and turn over fast, so waiting periods, contract requirements and the 50-employee threshold drive the plan design more than network reach does. '
           'Freight brokerages and 3PL offices have the same young, high-turnover profile on the sales floor, and they compete with the megabrokers for people on benefits as much as on base pay. '
           'In both cases a level-funded or ICHRA structure often fits better than a traditional fully insured plan.</p>\n\n')
    s2 = s.replace('<h2 id="fleet-faq">', add + '<h2 id="fleet-faq">', 1)
    if s2 != s:
        bump('tc delivery/broker section')
        if not DRY: open(f, 'w', encoding='utf-8').write(s2)

# vercel.json 301s (clean + .html), and repoint any existing redirect that lands on an old URL
v = json.load(open('vercel.json', encoding='utf-8'))
srcs = {r['source'] for r in v['redirects']}
for r in v['redirects']:
    d = r['destination'].split('?')[0]
    if d in FLEET: r['destination'] = FLEET[d]; bump('chain fixed')
    elif d in CITY_REDIRECT: r['destination'] = CITY_REDIRECT[d]; bump('chain fixed')
for src, dst in {**FLEET, **CITY_REDIRECT}.items():
    for s_ in (src, src + '.html'):
        if s_ not in srcs:
            v['redirects'].append({'source': s_, 'destination': dst, 'permanent': True}); bump('redirect added')
if not DRY: open('vercel.json', 'w', encoding='utf-8').write(json.dumps(v, indent=2, ensure_ascii=False) + '\n')

# llms.txt
l = open('llms.txt', encoding='utf-8').read()
l2 = '\n'.join(x for x in l.split('\n') if not any((B + slug + ')') in x for slug in OLD))
bump('llms lines removed', l.count('\n') - l2.count('\n'))
if not DRY: open('llms.txt', 'w', encoding='utf-8').write(l2)

print('DRY' if DRY else 'APPLIED', stats); print(len(changed), 'files changed')

# -*- coding: utf-8 -*-
"""Verification pass over everything this change touched."""
import re, json, glob, os, html.parser, subprocess

NEW = ['texas-small-business-health-insurance.html',
       'maryland-small-business-health-insurance.html',
       'kentucky-small-business-health-insurance.html',
       'blog/how-many-employees-do-you-need-for-group-health-insurance.html',
       'blog/group-health-insurance-minimum-participation.html',
       'blog/small-business-health-care-tax-credit-2026.html',
       'blog/small-business-health-insurance-cost-2027.html',
       'blog/ichra-vs-group-health-subsidy-cliff.html']

changed = subprocess.run(['git','status','--porcelain'],capture_output=True,text=True).stdout.split('\n')
changed = [l[3:].strip() for l in changed if l.strip().endswith('.html')]

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class P(html.parser.HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.stack=[]; s.err=[]
    def handle_starttag(s,t,a):
        if t not in VOID: s.stack.append(t)
    def handle_endtag(s,t):
        if t in VOID: return
        if t in s.stack:
            while s.stack and s.stack.pop()!=t: pass
        else: s.err.append('stray </%s>'%t)

red = {r['source'] for r in json.load(open('vercel.json'))['redirects']}
pages = {'/'+f[:-5] for f in glob.glob('*.html')+glob.glob('blog/*.html')+glob.glob('guides/*.html')}
pages.add('/'); pages.discard('/index')

problems = 0
print('=== structure + schema on %d changed html files ===' % len(changed))
for f in sorted(changed):
    if not os.path.exists(f): continue
    s = open(f, encoding='utf-8').read()
    p = P(); p.feed(s)
    msgs = []
    if p.stack: msgs.append('unclosed %s' % p.stack[-3:])
    if p.err:   msgs.append('%s' % p.err[:2])
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
        try: json.loads(m.group(1))
        except Exception as e: msgs.append('bad JSON-LD: %s' % str(e)[:50])
    for tag, pat in [('title', r'<title>.*?</title>'),
                     ('canonical', r'rel="canonical" href="'),
                     ('h1', r'<h1[\s>]')]:
        c = len(re.findall(pat, s, re.S))
        if c != 1: msgs.append('%s x%d' % (tag, c))
    if msgs:
        problems += 1
        print('  ! %-70s %s' % (f, ' | '.join(msgs)))
print('  structural problems: %d' % problems)

print('\n=== internal links on the 8 new pages ===')
bad = 0
for f in NEW:
    s = open(f, encoding='utf-8').read()
    for href in set(re.findall(r'href="(/[^"#?]*)(?:\?[^"]*)?"', s)):
        if href.startswith(('/compressed','/images','/favicon','/api')): continue
        if href in ('/','/quote'): continue
        if href in red:
            print('  ! %s -> %s (redirect source)' % (f, href)); bad += 1
        elif href not in pages:
            print('  ! %s -> %s (no such page)' % (f, href)); bad += 1
print('  broken / redirect-source internal links: %d' % bad)

print('\n=== new pages: word counts + CTA wiring ===')
for f in NEW:
    s = open(f, encoding='utf-8').read()
    a = s.find('<main') if '<main' in s else s.find('<body')
    body = s[a:s.rfind('<footer')]
    words = len(re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]*>', ' ', body, flags=re.S).split())
    print('  %-70s %4d words  %d group CTAs' % (f, words, s.count('/quote?type=business')))

print('\n=== sitemap ===')
sm = open('sitemap.xml', encoding='utf-8').read()
print('  urls: %d  parses: %s' % (sm.count('<loc>'), 'yes' if sm.strip().endswith('</urlset>') else 'NO'))
for f in NEW:
    slug = '/' + f[:-5]
    print('  %-70s %s' % (slug, 'IN' if slug+'<' in sm else 'MISSING'))

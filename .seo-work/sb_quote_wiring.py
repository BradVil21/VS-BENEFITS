# -*- coding: utf-8 -*-
"""Point in-content CTAs on small-business pages at /quote?type=business so the
visitor lands on the group form, not the type chooser. Nav/header/footer links
stay generic /quote - those serve every visitor, not just employers."""
import re, glob, json

red={r['source'] for r in json.load(open('vercel.json'))['redirects']}
SB=[f for f in sorted(glob.glob('*.html')) if re.search(
    r'small-business|business-open-enrollment|group-health|restaurant-health|'
    r'health-insurance-for-(auto-repair|cleaning|construction|dental-offices|hvac|restaurants|retail|salons|trucking-companies)|'
    r'ichra-florida|level-funded|florida-small-business', f)]

changed=0; total=0
for f in SB:
    if '/'+f[:-5] in red:      # redirect source, skip
        continue
    s=open(f,encoding='utf-8').read(); o=s
    # region boundaries: keep header + footer untouched
    h_end = s.find('</header>')
    h_end = h_end+9 if h_end>0 else 0
    f_start = s.rfind('<footer')
    if f_start < 0: f_start = len(s)
    head, body, foot = s[:h_end], s[h_end:f_start], s[f_start:]
    body, n = re.subn(r'href="/quote"', 'href="/quote?type=business"', body)
    s = head + body + foot
    if s!=o:
        open(f,'w',encoding='utf-8').write(s); changed+=1; total+=n
print('pages wired: %d | in-content CTAs repointed: %d'%(changed,total))

# sanity: nav/footer still generic, no double params
bad=0
for f in SB:
    s=open(f,encoding='utf-8').read()
    if 'type=business&' in s or '?type=business?' in s: print(' malformed',f); bad+=1
print('malformed URLs:',bad)

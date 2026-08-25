# -*- coding: utf-8 -*-
"""Reverse two redirects that point a page-1 ranking into a page-20 page.

GSC 24 May - 23 Aug 2026:
  /blog/how-much-does-health-insurance-cost-2026   541 impr, avg position   7.7
  /how-much-does-health-insurance-cost           3,134 impr, avg position 196.0
The current redirect sends the strong URL into the weak one. Reverse it.
"""
import json, collections

P='vercel.json'
d=json.load(open(P,encoding='utf-8'))
R=d['redirects']
before=len(R)

STRONG='/blog/how-much-does-health-insurance-cost-2026'
WEAK  ='/how-much-does-health-insurance-cost'

# 1. drop the backwards redirect(s)
R=[r for r in R if not (r['source']==STRONG and r['destination']==WEAK)]

# 2. point the weak national page (and its FAQ satellite) at the ranking post
def upsert(src,dst):
    for r in R:
        if r['source']==src:
            r['destination']=dst; r['permanent']=True; return 'updated'
    R.append({'source':src,'destination':dst,'permanent':True}); return 'added'

print('weak->strong :', upsert(WEAK, STRONG))
print('cost-faq     :', upsert('/health-insurance-cost-faq', STRONG))
print('cost-faq.html:', upsert('/health-insurance-cost-faq.html', STRONG))
print('weak .html   :', upsert(WEAK+'.html', STRONG))

# 3. sanity: no redirect chains, no self-redirects, no loops
m={r['source']:r['destination'] for r in R}
issues=0
for s,dst in m.items():
    if s==dst: print('SELF-REDIRECT:',s); issues+=1
    seen={s}; cur=dst; hops=0
    while cur in m and hops<10:
        if cur in seen: print('LOOP:',s,'->',cur); issues+=1; break
        seen.add(cur); cur=m[cur]; hops+=1
    else:
        if hops: print('CHAIN(%d): %s -> ... -> %s'%(hops,s,cur)); issues+=1

dupes=[k for k,v in collections.Counter(r['source'] for r in R).items() if v>1]
if dupes: print('DUPLICATE SOURCES:',dupes); issues+=1

d['redirects']=R
json.dump(d,open(P,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
open(P,'a').write('\n')
print('\nredirects %d -> %d | issues: %d'%(before,len(R),issues))

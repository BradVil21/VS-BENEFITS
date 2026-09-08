import json,glob,re,os,sys
root='.'
vj=json.load(open('vercel.json'))
redir={}
for r in vj.get('redirects',[]):
    s=r['source']
    if '*' in s or ':' in s: continue
    redir[s]=r['destination']
files=sorted(glob.glob('*.html')+glob.glob('blog/*.html'))
def slug(f): return '/'+f[:-5]
content={f:open(f,encoding='utf-8',errors='ignore').read() for f in files}
sm=open('sitemap.xml',encoding='utf-8').read()
sm_urls=set(re.findall(r'<loc>\s*([^<]+?)\s*</loc>',sm))
sm_paths={u.replace('https://www.vshealthbenefits.com','').rstrip('/') or '/' for u in sm_urls}

live=[];dead=[];noidx=[]
for f in files:
    s=slug(f)
    if s=='/index': s='/'
    c=content[f]
    if s in redir or (s+'.html') in redir and redir.get(s): pass
    if s in redir: dead.append((s,redir[s])); continue
    if re.search(r'<meta name="robots" content="[^"]*noindex',c): noidx.append(s); continue
    live.append(s)

print("files=%d  live=%d  redirected=%d  noindex=%d"%(len(files),len(live),len(dead),len(noidx)))
print("\n### LIVE PAGES MISSING FROM SITEMAP ###")
miss=[s for s in live if s not in sm_paths]
for s in miss: print("  ",s)
print("  total:",len(miss))

print("\n### SITEMAP ENTRIES THAT ARE REDIRECTED OR DEAD ###")
deadset={d[0] for d in dead}
bad=[p for p in sorted(sm_paths) if p in deadset]
for p in bad: print("  ",p,"->",redir[p])
print("  total:",len(bad))
smfile=[p for p in sorted(sm_paths) if p not in ('/',) and p not in deadset and not os.path.exists(p.lstrip('/')+'.html')]
print("\n### SITEMAP ENTRIES WITH NO FILE ###")
for p in smfile: print("  ",p)

# internal links
linkre=re.compile(r'href="(/[^"#?]*)"')
inlinks={s:0 for s in live}
to_redirected={}
for f,c in content.items():
    for h in set(linkre.findall(c)):
        h2=h[:-5] if h.endswith('.html') else h
        h2=h2.rstrip('/') or '/'
        if h2 in inlinks and slug(f)!=h2: inlinks[h2]+=1
        if h in redir or h2 in redir:
            to_redirected.setdefault(h,set()).add(f)
print("\n### LIVE PAGES WITH ZERO INTERNAL LINKS (true orphans) ###")
orph=[s for s in live if inlinks[s]==0 and s!='/']
for s in orph: print("  ",s)
print("  total:",len(orph))
print("\n### INTERNAL LINKS POINTING AT REDIRECTED URLS (equity leak) ###")
for h,fs in sorted(to_redirected.items(), key=lambda x:-len(x[1]))[:40]:
    print(f"  {len(fs):4d} files -> {h}  => {redir.get(h) or redir.get(h[:-5])}")
print("  distinct bad targets:",len(to_redirected))

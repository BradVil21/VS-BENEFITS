# -*- coding: utf-8 -*-
"""Full verification pass for the September 2026 trucking work."""
import glob, re, json, os, sys, collections

BASE="https://www.vshealthbenefits.com"
NEW=["truck-driver-health-insurance-cost-calculator","truck-driver-open-enrollment-2027",
     "ooida-health-insurance-vs-aca","blue-cross-blue-shield-truck-drivers",
     "best-trucking-company-health-benefits"]

vj=json.load(open("vercel.json"))
redir={r["source"]:r["destination"] for r in vj["redirects"] if "*" not in r["source"] and ":" not in r["source"]}
files=sorted(glob.glob("*.html")+glob.glob("blog/*.html"))
C={f:open(f,encoding="utf-8").read() for f in files}
sm=open("sitemap.xml",encoding="utf-8").read()
sm_paths={u.replace(BASE,"").rstrip("/") or "/" for u in re.findall(r"<loc>([^<]+)</loc>",sm)}

problems=collections.OrderedDict()
def bad(cat,msg): problems.setdefault(cat,[]).append(msg)

def slug(f):
    s="/"+f[:-5]
    return "/" if s=="/index" else s

live=[f for f in files if slug(f) not in redir and
      not re.search(r'<meta name="robots" content="[^"]*noindex',C[f])]

# --- 1. one of each critical head tag ---------------------------------------
PRIVATE={"admin.html","census.html","client.html"}
for f in files:
    if f in PRIVATE: continue
    c=C[f]
    for tag,pat in (("title",r"<title>.*?</title>"),
                    ("description",r'<meta name="description"'),
                    ("canonical",r'<link rel="canonical"')):
        n=len(re.findall(pat,c,re.S))
        if n!=1 and slug(f) not in redir:
            bad("head tags","%s: %d x %s"%(f,n,tag))
    n=len(re.findall(r"<h1[\s>]",c))
    if n!=1 and slug(f) not in redir:
        bad("h1 count","%s: %d h1"%(f,n))

# --- 2. title length --------------------------------------------------------
for f in live:
    m=re.search(r"<title>(.*?)</title>",C[f],re.S)
    if m and len(m.group(1))>60:
        bad("title >60 chars","%s (%d): %s"%(f,len(m.group(1)),m.group(1)[:70]))

# --- 3. JSON-LD parses ------------------------------------------------------
for f in files:
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',C[f],re.S):
        try: json.loads(m.group(1))
        except Exception as e: bad("invalid JSON-LD","%s: %s"%(f,str(e)[:90]))

# --- 4. internal links resolve, and none point at a redirect source ---------
def exists(p):
    p=p.rstrip("/") or "/"
    if p=="/": return True
    if os.path.exists(p.lstrip("/")+".html"): return True
    if os.path.isdir(p.lstrip("/")) and os.path.exists(os.path.join(p.lstrip("/"),"index.html")): return True
    return False
for f in files:
    for h in set(re.findall(r'href="(/[^"#?]*)"',C[f])):
        clean=h[:-5] if h.endswith(".html") else h
        clean=clean.rstrip("/") or "/"
        if h in redir or clean in redir:
            bad("link to redirect source","%s -> %s"%(f,h))
        elif not exists(clean) and not h.startswith(("/api/","/assets/","/compressed/")) and not re.search(r"\.(js|css|png|jpg|jpeg|svg|webp|xml|txt|pdf|ico|xlsx|xls|csv|docx|zip|webmanifest)$",h):
            bad("broken internal link","%s -> %s"%(f,h))

# --- 5. sitemap coverage ----------------------------------------------------
for f in live:
    if slug(f) not in sm_paths and slug(f) not in ("/admin","/census","/client","/book"):
        bad("live page missing from sitemap",slug(f))
for p in sm_paths:
    if p in redir: bad("sitemap lists a redirect source",p)

# --- 6. the new pages specifically ------------------------------------------
for s in NEW:
    f=s+".html"
    if not os.path.exists(f): bad("new page missing",f); continue
    c=C[f]
    if "/"+s not in sm_paths: bad("new page not in sitemap",s)
    inl=sum(1 for g in files if g!=f and ('"/%s"'%s) in C[g])
    if inl<10: bad("new page under-linked","%s has only %d internal links"%(s,inl))
    if 'id="vs-callbar"' not in c: bad("new page missing sticky call bar",s)
    for need in ("/quote","canonical"):
        if need not in c: bad("new page missing %s"%need,s)

# --- 7. countdown integrity -------------------------------------------------
for f in files:
    c=C[f]
    if "now<=DEC15" in c and not re.search(r"\bDEC15\s*=\s*new Date",c):
        bad("countdown broken","%s uses DEC15 without defining it"%f)
    if re.search(r'END\s*=\s*new Date\("2026-12-15',c):
        bad("countdown still ends Dec 15",f)

# --- 8. sticky bar did not double up ----------------------------------------
for f in files:
    if C[f].count('id="vs-callbar"')>1: bad("duplicate call bar",f)
    if C[f].count('data-block="vs-trucking-tools"')>1: bad("duplicate tools block",f)

print("files scanned: %d   live: %d   sitemap: %d\n"%(len(files),len(live),len(sm_paths)))
if not problems:
    print("NO PROBLEMS FOUND")
else:
    tot=0
    for cat,items in problems.items():
        print("### %s (%d)"%(cat,len(items)))
        for i in items[:12]: print("   ",i)
        if len(items)>12: print("    ... and %d more"%(len(items)-12))
        tot+=len(items); print()
    print("TOTAL PROBLEMS:",tot)
    sys.exit(1)

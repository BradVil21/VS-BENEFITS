"""2026-10-28 site speed pass. Usage: python3 .seo-work/speed_pass_oct28.py [--apply]
 - <img> of a large photo without srcset: add a 900px version + srcset/sizes
 - decoding="async" on every <img>; loading="lazy" on images after the first two in <body>
 - defer on the GoHighLevel chat-widget loader and tracking script"""
import re,glob,os,sys
from PIL import Image, ImageOps
APPLY='--apply' in sys.argv
os.chdir(os.path.expanduser('~/mnt/VS-BENEFITS'))
pages=[f for f in glob.glob('**/*.html',recursive=True) if not f.startswith(('_to_delete','node_modules','_build','.seo-work','admin','client','census'))]
W={}
def width(p):
    if p not in W:
        try: W[p]=Image.open(p).width
        except Exception: W[p]=0
    return W[p]
made=set(); stats=dict(srcset=0,dec=0,lazy=0,defer=0,files=0,variants=0)
def variant(path):
    base,ext=path.rsplit('.',1); v=f'{base}-900.{ext}'
    if not os.path.exists(v) and v not in made:
        made.add(v); stats['variants']+=1
        if APPLY:
            im=ImageOps.exif_transpose(Image.open(path)); im=im.resize((900,round(im.height*900/im.width)),Image.LANCZOS)
            if ext.lower() in('jpg','jpeg'): im.convert('RGB').save(v,'JPEG',quality=76,optimize=True,progressive=True)
            elif ext.lower()=='webp': im.save(v,'WEBP',quality=72,method=6)
            else: im.save(v,'PNG',optimize=True)
    return '/'+v
for f in pages:
    s=open(f,encoding='utf-8',errors='ignore').read(); o=s
    head,sep,body=s.partition('<body')
    if not sep: continue
    n=[0]
    def fix(m):
        t=m.group(0); n[0]+=1
        # inside <picture> with a <source>? leave srcset alone
        pre=body[max(0,m.start()-400):m.start()]
        in_pic=pre.rfind('<picture')>pre.rfind('</picture>') and '<source' in pre[pre.rfind('<picture'):]
        sm=re.search(r'\ssrc="(/(?:compressed|images)/[^"?#]+\.(?:jpe?g|png|webp))"',t,re.I)
        if sm and 'srcset=' not in t and not in_pic and not re.search(r'-(900|640)\.\w+$',sm.group(1)):
            p=sm.group(1).lstrip('/')
            if os.path.isfile(p) and width(p)>=1200 and 'carriers/' not in p and 'partners/' not in p:
                v=variant(p)
                t=t.replace('<img ',f'<img srcset="{v} 900w, {sm.group(1)} {width(p)}w" sizes="(max-width: 900px) 100vw, 1200px" ',1); stats['srcset']+=1
        if 'decoding=' not in t: t=t.replace('<img ','<img decoding="async" ',1); stats['dec']+=1
        if 'loading=' not in t and n[0]>2 and 'fetchpriority' not in t: t=t.replace('<img ','<img loading="lazy" ',1); stats['lazy']+=1
        return t
    body2=re.sub(r'<img\b[^>]*>',fix,body)
    def dfr(m):
        t=m.group(0)
        if re.search(r'\b(defer|async)\b',t): return t
        stats['defer']+=1; return t.replace('<script ','<script defer ',1)
    body2=re.sub(r'<script\b[^>]*src="https://(?:widgets\.leadconnectorhq\.com/loader\.js|link\.msgsndr\.com/js/external-tracking\.js)"[^>]*>',dfr,body2)
    s=head+sep+body2
    if s!=o:
        stats['files']+=1
        if APPLY: open(f,'w',encoding='utf-8').write(s)
print(stats,'APPLIED' if APPLY else 'dry run')

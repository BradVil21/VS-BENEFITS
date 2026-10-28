"""2026-10-28: image speed. (1) /blog cards -> 640px WebP thumbnails. (2) new photos -> <picture> with WebP srcset.
Usage: python3 .seo-work/speed_images_oct28.py [--apply]"""
import re,os,sys
from PIL import Image, ImageOps
APPLY='--apply' in sys.argv
os.chdir(os.path.expanduser('~/mnt/VS-BENEFITS'))
def src_for(base):
    for c in (f'compressed/{base}.jpg',f'compressed/{base}.webp',f'compressed/{base}-900.jpg',f'images/{base}.jpg'):
        if os.path.exists(c): return c
def make(base,W,suf,fmts):
    outs=[f'compressed/{base}{suf}.{f}' for f in fmts]
    if all(os.path.exists(o) for o in outs): return
    im=ImageOps.exif_transpose(Image.open(src_for(base))).convert('RGB')
    w=min(W,im.width); r=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    for o in outs:
        if os.path.exists(o): continue
        if APPLY: r.save(o,'JPEG',quality=80,optimize=True,progressive=True) if o.endswith('jpg') else r.save(o,'WEBP',quality=76,method=6)
        print('  make',o)
def basename(p): return re.sub(r'(-900|-640)?\.(jpg|jpeg|webp|png)$','',os.path.basename(p))
changes={}
# (1) blog cards
s=open('blog.html').read(); before=0; after=0
def card(m):
    global before,after
    blk=m.group(0); im=re.search(r'<img src="/((?:compressed|images)/[^"]+)"',blk)
    if not im or 'partners/' in im.group(1): return blk
    b=basename(im.group(1)); before+=os.path.getsize(im.group(1))
    make(b,640,'-640',('webp',))
    new=f'compressed/{b}-640.webp'
    after+=os.path.getsize(new) if os.path.exists(new) else 30000
    tag=re.search(r'<img [^>]*>',blk[im.start():]).group(0)
    nt=tag.replace(f'src="/{im.group(1)}"',f'src="/{new}"')
    if 'decoding=' not in nt: nt=nt.replace('<img ','<img decoding="async" ',1)
    if 'width=' not in nt: nt=nt.replace('<img ','<img width="640" height="360" ',1)
    return blk.replace(tag,nt,1)
s2=re.sub(r'<a class="post-card" href="[^"]+">.*?</a>',card,s,flags=re.S)
changes['blog.html']=s2
print(f'blog cards: {before//1024} KB -> ~{after//1024} KB')
# (2) <picture> for the new photos wherever they appear in page bodies
NEW=['construction-workers-hard-hats-clipboard','carpenter-cutting-wood-workbench','construction-site-supervisors-rebar','factory-workers-sanding-wood','mail-truck-side-mirror','semi-truck-highway-rain-autumn','trucker-red-semi-cab','kids-playing-park-circle','kids-parachute-game-field','grandmother-family-farm-eggs','family-farm-garden-portrait','family-walking-dairy-farm-road','truck1','truckdriver2']
for b in NEW:
    make(b,1600,'',('webp',)); make(b,900,'-900',('jpg','webp')); make(b,640,'-640',('webp',))
FILES={'index.html':'(max-width: 700px) 100vw, 400px','health-insurance-for-contractors.html':'(max-width: 700px) 100vw, 400px',
 'group-health-insurance-for-delivery-fleets.html':'(max-width: 900px) 100vw, 880px','health-insurance-for-daycare-centers.html':'(max-width: 900px) 100vw, 880px',
 'family-health-insurance.html':'(max-width: 900px) 100vw, 880px','health-insurance-for-self-employed-truck-drivers.html':'(max-width: 900px) 100vw, 880px',
 '1099-truck-driver-health-insurance.html':'(max-width: 900px) 100vw, 880px'}
for slug in ['hsa-for-truck-drivers','team-truck-drivers-health-insurance','health-sharing-plans-truck-drivers','company-driver-to-owner-operator-health-insurance','truck-driver-diabetes-health-insurance','switching-trucking-companies-health-insurance','company-truck-driver-health-insurance','cobra-60-day-loophole','health-insurance-for-construction-companies','how-many-employees-do-you-need-for-group-health-insurance','why-do-we-get-health-insurance','health-insurance-when-you-go-independent']:
    FILES[f'blog/{slug}.html']='(max-width: 800px) 100vw, 760px'
alt='|'.join(map(re.escape,NEW))
pat=re.compile(r'(<picture>\s*(?:<source[^>]*>\s*)*)?(<img\b[^>]*?src="/compressed/('+alt+r')(?:-900|-640)?\.(?:jpg|webp)"[^>]*>)(\s*</picture>)?')
for f,sizes in FILES.items():
    s=changes.get(f) or open(f).read(); n=0
    def rep(m):
        global n
        if bool(m.group(1))!=bool(m.group(4)): return m.group(0)  # unusual nesting: leave
        b=m.group(3); tag=m.group(2)
        tag=re.sub(r'src="[^"]+"',f'src="/compressed/{b}-900.jpg"',tag,count=1)
        hero='itemprop="image"' in tag or 'loading="eager"' in tag
        if hero and 'fetchpriority' not in tag: tag=tag.replace('<img ','<img fetchpriority="high" ',1)
        if not hero and 'loading=' not in tag: tag=tag.replace('<img ','<img loading="lazy" ',1)
        if 'decoding=' not in tag: tag=tag.replace('<img ','<img decoding="async" ',1)
        n+=1
        return (f'<picture><source type="image/webp" srcset="/compressed/{b}-640.webp 640w, /compressed/{b}-900.webp 900w, /compressed/{b}.webp 1600w" sizes="{sizes}">{tag}</picture>')
    s2=pat.sub(rep,s); print(f'{f}: {n} img'); changes[f]=s2
if APPLY:
    for f,s in changes.items(): open(f,'w').write(s)
print('APPLIED' if APPLY else 'dry run')

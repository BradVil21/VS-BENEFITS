"""2026-10-28: add 12 new photos; make every blog index card image unique.
Usage: python3 .seo-work/swap_photos_oct28.py [--apply]"""
import re,glob,os,sys
APPLY='--apply' in sys.argv
os.chdir(os.path.expanduser('~/mnt/VS-BENEFITS'))
C='compressed'
def variant(base,suf,ext):
    p=f'{base}{suf}.{ext}'
    if os.path.exists(f'{C}/{p}'): return p
    if os.path.exists(f'{C}/{base}.{ext}'): return f'{base}.{ext}'
    return f'{base}.jpg'
def swap_paths(txt,old,new):
    for o in old.split('|'): txt=_swap1(txt,o,new)
    return txt
def has(txt,old): return any('/compressed/'+o in txt for o in old.split('|'))
def _swap1(txt,old,new):
    return re.sub(r'/compressed/'+re.escape(old)+r'(-900|-640)?\.(jpg|webp)',
                  lambda m:'/compressed/'+variant(new,m.group(1) or '',m.group(2)),txt)
def set_alt(tag,alt):
    a=alt.replace('"','&quot;')
    return re.sub(r'alt="[^"]*"',f'alt="{a}"',tag) if 'alt="' in tag else tag.replace('<img ',f'<img alt="{a}" ',1)
def swap_block(block,old,new,alt):
    b=swap_paths(block,old,new)
    return re.sub(r'<img [^>]*>',lambda m:set_alt(m.group(0),alt) if '/compressed/'+new in m.group(0) else m.group(0),b)

POSTS={ # slug: (old, new, alt)
 'hsa-for-truck-drivers':('truck-driver-hands-on-wheel-sunrise','family-farm-garden-portrait','Family standing together in their backyard garden at home'),
 'team-truck-drivers-health-insurance':('truck-driver-cb-radio','semi-truck-highway-rain-autumn','Semi truck running down a wet highway on a rainy fall day'),
 'health-sharing-plans-truck-drivers':('truck-driver-cb-radio','grandmother-family-farm-eggs','Grandmother sharing a carton of farm eggs with her family'),
 'company-driver-to-owner-operator-health-insurance':('truck-driver-highway-view-state-line','trucker-red-semi-cab','Owner-operator crouching in front of his red semi truck'),
 'truck-driver-diabetes-health-insurance':('truck-cab-driving-fog-rain','family-walking-dairy-farm-road','Family walking down a gravel road past a dairy farm'),
 'switching-trucking-companies-health-insurance':('truck-driver-walking-city-street|truck1','truckdriver2','Truck driver sitting on the hood of his truck at night'),
 'company-truck-driver-health-insurance':('HMOimage2','truck1','View of the open road from a truck cab'),
 'cobra-60-day-loophole':('kids-playing-together','kids-playing-park-circle','Kids holding hands and playing in a circle at the park'),
 'health-insurance-for-construction-companies':('10-99working|construction-crew-rebar-column','construction-workers-hard-hats-clipboard','Two construction workers in hard hats reviewing a clipboard on site'),
 'how-many-employees-do-you-need-for-group-health-insurance':('microgroup','factory-workers-sanding-wood','Small manufacturing crew sanding wood panels in a workshop'),
 'why-do-we-get-health-insurance':('familyhappy','kids-parachute-game-field','Kids lifting a rainbow parachute together in a sunny field'),
 'health-insurance-when-you-go-independent':('independent','carpenter-cutting-wood-workbench','Independent carpenter cutting a board at his workbench'),
}
# site pages: (file, line-match substring, old, new, alt)
PAGES=[
 ('index.html','alt="Group health insurance for small employers"','10-99working','construction-workers-hard-hats-clipboard','Construction crew in hard hats reviewing plans on a job site'),
 ('index.html','alt="Micro-group health insurance"','microgroup','factory-workers-sanding-wood','Small workshop team sanding wood panels'),
 ('health-insurance-for-contractors.html','alt="Fully insured group health plan"','10-99working','construction-site-supervisors-rebar','Contractors walking a job site with rebar and steel columns'),
 ('group-health-insurance-for-delivery-fleets.html','alt="Delivery fleet truck"','truck2','mail-truck-side-mirror','Delivery truck seen in a car side mirror on a city street'),
 ('health-insurance-for-daycare-centers.html','kids-playing-together-900','kids-playing-together','kids-parachute-game-field','Children playing a parachute game outdoors'),
 ('family-health-insurance.html','/compressed/family-picture.jpg','family-picture','family-farm-garden-portrait','Family standing together in their garden at home'),
 ('health-insurance-for-self-employed-truck-drivers.html','/compressed/Truckermore.jpg" alt="Self-employed','Truckermore','trucker-red-semi-cab','Self-employed truck driver crouching in front of his red semi'),
 ('1099-truck-driver-health-insurance.html','alt="Independent truck driver reviewing 1099','10-99working','semi-truck-highway-rain-autumn','Independent truck driver hauling a load on a rainy highway'),
]
changes={}
def put(f,new,old):
    if new!=old: changes[f]=new
# 1) the post files: meta/schema lines + hero-img block
for slug,(old,new,alt) in POSTS.items():
    f=f'blog/{slug}.html'; s=changes.get(f) or open(f).read(); o=s
    s=re.sub(r'(?m)^.*(og:image|twitter:image|"image"|"thumbnailUrl").*$',lambda m:swap_paths(m.group(0),old,new),s)
    s,n=re.subn(r'<div class="hero-img">.*?</div>',lambda m:swap_block(m.group(0),old,new,alt),s,count=1,flags=re.S)
    if '/compressed/'+new not in s: print('!! hero not swapped',f)
    put(f,s,o)
# 2) every card on the site that links to one of those posts
for f in glob.glob('*.html')+glob.glob('blog/*.html')+glob.glob('truckers/*.html'):
    s=changes.get(f) or open(f).read(); o=s
    for slug,(old,new,alt) in POSTS.items():
        pat=r'<a\b[^>]*href="(?:https://www\.vshealthbenefits\.com)?/blog/'+re.escape(slug)+r'(?:\.html)?/?"[^>]*>(?:(?!</a>).)*?</a>'
        s=re.sub(pat,lambda m:swap_block(m.group(0),old,new,alt) if has(m.group(0),old) else m.group(0),s,flags=re.S)
    put(f,s,o)
# 3) site pages
for f,key,old,new,alt in PAGES:
    s=changes.get(f) or open(f).read(); o=s
    lines=s.split('\n'); hit=0
    for i,l in enumerate(lines):
        if key in l and '/compressed/'+old in l and 'og:image' not in l:
            lines[i]=swap_block(l,old,new,alt); hit+=1; break
    if not hit: print('!! no match',f,key)
    put(f,'\n'.join(lines),o)
for f,s in sorted(changes.items()):
    o=open(f).read()
    ol,nl=o.split('\n'),s.split('\n')
    d=[i for i in range(min(len(ol),len(nl))) if ol[i]!=nl[i]]
    print(f'{f}: {len(d)} lines')
    if APPLY: open(f,'w').write(s)
print('APPLIED' if APPLY else 'dry run', len(changes),'files')

"""2026-10-28: remove the Individual/Business picker card (qf-card / quote-card) and keep only the quote button."""
import re,glob,os,sys
APPLY='--apply' in sys.argv
os.chdir(os.path.expanduser('~/mnt/VS-BENEFITS'))
BTN_STYLE='display:inline-block;background:#1565d8;color:#fff;font-weight:700;font-size:1.08rem;padding:16px 40px;border-radius:10px;text-decoration:none;box-shadow:0 8px 20px rgba(21,101,216,.28)'
n=0
for f in sorted(glob.glob('*.html')):
    s=open(f).read(); o=s
    for cls in ('qf-card','quote-card'):
        while True:
            m=re.search(r'class="'+cls+r'\b',s)
            if not m: break
            st=s.rfind('<section',0,m.start()); open_tag=re.match(r'<section[^>]*>',s[st:]).group(0)
            depth=0
            for mm in re.finditer(r'<(/?)section\b',s[st:]):
                depth+=-1 if mm.group(1) else 1
                if depth==0: end=s.find('>',st+mm.start())+1; break
            blk=s[st:end]
            cta=re.search(r'<div class="qf-cta".*?</div>',blk,re.S)
            if cta: inner=cta.group(0)
            else:
                slug=f[:-5]
                inner=(f'<div class="qf-cta" style="text-align:center;padding:10px 24px 0"><a href="/quote?from={slug}" class="qf-cta-btn" style="{BTN_STYLE}">Get My Free Quote &rarr;</a>'
                       '<p style="font-size:.85rem;color:#5a6b80;margin:12px 0 0">Free, no obligation.</p></div>')
            new_open=re.sub(r'\s*style="[^"]*"','',open_tag)[:-1]+' style="padding:36px 0">'
            s=s[:st]+new_open+'\n  '+inner+'\n</section>'+s[end:]
            n+=1; print(f, cls, '->', re.search(r'href="([^"]+)"',inner).group(1))
    if APPLY and s!=o: open(f,'w').write(s)
print(n,'sections','APPLIED' if APPLY else 'dry run')

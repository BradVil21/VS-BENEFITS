"""2026-10-28: remove sticky bottom call/quote bars (#vs-callbar, #vs-sticky) site-wide."""
import re,glob,os,sys
APPLY='--apply' in sys.argv
os.chdir(os.path.expanduser('~/mnt/VS-BENEFITS'))
def cut_div(s,idattr):
    i=s.find(idattr)
    if i<0: return s,False
    st=s.rfind('<div',0,i); depth=0
    for m in re.finditer(r'<(/?)div\b',s[st:]):
        depth+=-1 if m.group(1) else 1
        if depth==0: end=s.find('>',st+m.start())+1; break
    # also drop the bar's own <script> right after it
    m=re.match(r'\s*<script>\s*\(function\(\)\{\s*var (?:b|bar)\s*=\s*document\.getElementById\(["\']'+idattr.split('"')[1]+r'["\']\).*?</script>',s[end:],re.S)
    if m: end+=m.end()
    pre=s[:st].rstrip(' \t')
    return pre+s[end:],True
counts={'callbar':0,'sticky':0,'style':0}; files=0
for f in glob.glob('**/*.html',recursive=True):
    if f.startswith(('_to_delete','node_modules')): continue
    s=open(f).read(); o=s
    s,ok=cut_div(s,'id="vs-callbar"'); counts['callbar']+=ok
    s,ok=cut_div(s,'id="vs-sticky"'); counts['sticky']+=ok
    s,n=re.subn(r'\n?<style id="vs-sticky-call">.*?</style>','',s,flags=re.S); counts['style']+=n
    if s!=o:
        files+=1
        if APPLY: open(f,'w').write(s)
print(files,'files',counts)
# stop the script from adding the bar
js='vs-conversions.js'; t=open(js).read()
a='      if (SKIP.test(location.pathname)) return;\n      if (document.getElementById("vs-callbar")'
if a in t and 'STICKY BAR REMOVED' not in t:
    t=t.replace(a,'      return; // STICKY BAR REMOVED 2026-10-28 (owner request). Delete this line to bring it back.\n'+a,1)
    print('vs-conversions.js: auto bar disabled')
    if APPLY: open(js,'w').write(t)
print('APPLIED' if APPLY else 'dry run')

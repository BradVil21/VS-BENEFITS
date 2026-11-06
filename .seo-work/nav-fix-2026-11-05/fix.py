import os, re, glob, shutil, sys
root = sys.argv[1]; os.chdir(root)
bk = '.seo-work/nav-fix-2026-11-05/backup'
CORE = {'florida':'Florida','georgia':'Georgia','illinois':'Illinois','kentucky':'Kentucky','maryland':'Maryland','missouri':'Missouri','ohio':'Ohio','texas':'Texas'}
STATES = "alabama arizona arkansas colorado florida georgia illinois indiana iowa kansas kentucky louisiana michigan minnesota mississippi missouri montana nebraska nevada north-carolina north-dakota ohio oklahoma south-carolina south-dakota tennessee texas utah virginia west-virginia wisconsin wyoming".split()
def dest(st):
    if st in CORE: return '/lp/self-employed/' + st
    return '/' + st + '-small-business-health-insurance'
for st in STATES: assert os.path.exists(dest(st).lstrip('/') + '.html'), st
def backup(f):
    t = os.path.join(bk, f); os.makedirs(os.path.dirname(t), exist_ok=True)
    if not os.path.exists(t): shutil.copy(f, t)
# 1. nav menu
files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith(('node_modules', '.seo-work', '_to_delete', 'Claude outputs', 'contractor-outreach', 'restaurant-list', 'ghl'))]
changed = 0; links = 0
for f in files:
    s = open(f, encoding='utf-8').read(); o = s
    for st in STATES:
        a = 'href="/health-insurance-%s" role="menuitem"' % st
        if a in s:
            n = s.count(a); s = s.replace(a, 'href="%s" role="menuitem"' % dest(st)); links += n
    if s != o: backup(f); open(f, 'w', encoding='utf-8').write(s); changed += 1
print('nav: %d files, %d links fixed' % (changed, links))
# 2. state link rows on hub pages
def row(title, items, note=''):
    a = ' &middot; '.join('<a href="%s">%s</a>' % (h, t) for h, t in items)
    return '<p class="vs-state-links" style="margin:14px 0 4px;font-size:.95rem;line-height:1.7"><strong>%s</strong> %s%s</p>' % (title, a, note)
trk = [('/truck-driver-health-insurance-florida' if s=='florida' else '/truck-driver-health-insurance-texas' if s=='texas' else '/lp/truckers/'+s, n) for s, n in CORE.items()]
es_names = dict(CORE); es_names['missouri'] = 'Misuri'
cam = [('/seguro-medico-camioneros-florida' if s=='florida' else '/lp/es/camioneros/'+s, es_names[s]) for s in CORE]
ind = [('/lp/es/independientes/'+s, es_names[s]) for s in CORE]
se = [('/lp/self-employed/'+s, n) for s, n in CORE.items()]
edits = [
 ('truck-driver-health-insurance.html',
  '<p>We\'re licensed in the 33 states below. Pick yours to see how coverage works there.',
  'before', row('Driver pages by state:', trk)),
 ('seguro-medico-camioneros.html', '<h2 class="center">Guías de Seguro Médico para Camioneros</h2>', 'after',
  row('Seguro médico para camioneros por estado:', cam) + row('Trabajadores independientes y 1099:', ind)),
 ('self-employed-health-insurance.html', '<h2>More Guides for the Self-Employed</h2></div>', 'after',
  row('Self-employed health insurance by state:', se)),
]
for f, anchor, where, html in edits:
    s = open(f, encoding='utf-8').read()
    if 'vs-state-links' in s: print('skip (already done):', f); continue
    assert s.count(anchor) == 1, (f, s.count(anchor))
    backup(f)
    s = s.replace(anchor, (html + '\n' + anchor) if where == 'before' else (anchor + '\n' + html), 1)
    open(f, 'w', encoding='utf-8').write(s); print('links added:', f)

"""Trucker SEO quick wins (2026-11-03): mid-page call/quote box + FAQs for the exact
searches, mirrored in FAQPage data. Safe to re-run (skips pages already done)."""
import json, re, sys, html

def box(h, p, frm):
    return ('<div class="vs-qw-cta" style="margin:28px 0;padding:20px 22px;border-radius:16px;background:linear-gradient(135deg,#0b2346,#16447f);color:#fff;'
            'display:flex;flex-wrap:wrap;gap:14px 18px;align-items:center;justify-content:space-between">'
            '<div style="flex:1 1 280px"><strong style="display:block;font-size:1.12rem;color:#fff;margin-bottom:4px">' + h + '</strong>'
            '<span style="color:rgba(255,255,255,.86);font-size:.95rem;line-height:1.5">' + p + '</span></div>'
            '<div style="display:flex;gap:10px;flex-wrap:wrap">'
            '<a href="tel:+19548251009" style="display:inline-flex;align-items:center;gap:8px;background:#0db5a6;color:#fff;font-weight:700;padding:12px 18px;border-radius:999px;text-decoration:none">'
            '&#9742; Call (954) 825-1009</a>'
            '<a href="/trucking-health-quote?from=' + frm + '-midcta" style="display:inline-flex;align-items:center;background:#fff;color:#0b2346;font-weight:700;padding:12px 18px;border-radius:999px;text-decoration:none">Get a free quote &rarr;</a>'
            '</div></div>\n')

PAGES = {
 'does-health-insurance-cover-dot-physical.html': dict(
   before_h2='Three ways to reduce what you pay', style='h3',
   cta=('DOT physical coming up?', 'Your plan will not pay for the exam, but it covers the care that keeps you passing it. Talk to a licensed advisor about plans that work on the road.'),
   faq=[('Where can I get a DOT physical?', 'Only a medical examiner listed on the FMCSA National Registry of Certified Medical Examiners can do a DOT physical. Many urgent care and occupational health clinics are on the registry, and you can search it by ZIP code on the FMCSA website.'),
        ('How long is a DOT medical card good for?', 'Up to 24 months. The examiner can issue a shorter card, often one year, when a condition such as high blood pressure needs to be checked again sooner.'),
        ('Can my health plan help me pass my DOT physical?', 'It cannot pay for the exam itself, but it pays for the doctor visits, blood pressure and diabetes medication, and sleep apnea testing and treatment that keep a condition under control before your exam. Coverage details depend on the plan, so ask your advisor to check.')]),
 'truck-driver-health-insurance-cost.html': dict(
   before_h2='The Five Things That Set Your Price', style='details',
   title='Truck Driver &amp; Owner-Operator Health Insurance Cost 2027',
   cta=('Want your exact price, not a range?', 'A licensed advisor prices private PPO plans from top A-rated carriers for your age, ZIP and family. Free, usually the same day.'),
   faq=[('How do I find out exactly what I would pay?', 'Give a licensed advisor your age, ZIP code, who needs coverage and the doctors you want to keep. You get real prices from several carriers, usually the same day, at no cost.'),
        ('Is a PPO worth the higher premium for a truck driver?', 'Often, yes. A PPO usually costs more per month than an HMO, but a driver who needs care in another state can avoid large out-of-network bills with a national PPO network.')]),
 'best-health-insurance-owner-operators.html': dict(
   before_h2='Your Four Real Options', style='details',
   cta=('Price your owner-operator plan in minutes', 'Compare private PPO plans with nationwide networks from top A-rated carriers. A licensed advisor does the shopping for you, free.'),
   faq=[('How fast can an owner-operator get covered?', 'Private PPO plans accept applications year-round, and if you are approved, coverage can often start on the first of the next month.'),
        ('How do I get an owner-operator health insurance quote?', 'Call (954) 825-1009 or fill in the short quote form. A licensed advisor asks your age, ZIP code, household and doctors, then compares plans from several carriers for you.')]),
}

def plain(t): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', t))).strip()

for f, cfg in PAGES.items():
    s = open(f, encoding='utf-8').read()
    if 'vs-qw-cta' in s:
        print(f, 'already done'); continue
    # 1. mid-page CTA before the chosen h2
    m = re.search(r'<h2[^>]*>\s*' + re.escape(cfg['before_h2']), s)
    assert m, (f, 'h2 not found')
    s = s[:m.start()] + box(cfg['cta'][0], cfg['cta'][1], f[:-5]) + s[m.start():]
    # 2. visible FAQs appended to the end of the existing FAQ block
    fi = re.search(r'<h2[^>]*>[^<]*(Frequently Asked Questions|FAQ)\s*</h2>', s)
    assert fi, (f, 'faq heading')
    nxt = s.find('<h2', fi.end())
    seg = s[fi.end():nxt]
    if cfg['style'] == 'details':
        last = seg.rfind('</details>'); assert last > 0
        cls = re.search(r'<details class="([^"]+)"', seg).group(1)
        acls = re.search(r'<div class="(faq-a[^"]*)"', seg).group(1)
        new = ''.join('\n<details class="%s"><summary>%s</summary><div class="%s"><p>%s</p></div></details>' % (cls, html.escape(q), acls, html.escape(a)) for q, a in cfg['faq'])
        pos = fi.end() + last + len('</details>')
    else:
        lastp = seg.rfind('</p>'); assert lastp > 0
        new = ''.join('\n<h3>%s</h3><p>%s</p>' % (html.escape(q), html.escape(a)) for q, a in cfg['faq'])
        pos = fi.end() + lastp + len('</p>')
    s = s[:pos] + new + s[pos:]
    # 3. same questions in the FAQPage data
    done = False
    for jm in list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)):
        try: d = json.loads(jm.group(2))
        except Exception: continue
        holder = None
        if isinstance(d, dict) and d.get('@type') == 'FAQPage': holder = d
        elif isinstance(d, dict):
            for it in d.get('@graph', []):
                if isinstance(it, dict) and it.get('@type') == 'FAQPage': holder = it
        if not holder: continue
        have = {plain(q.get('name', '')) for q in holder['mainEntity']}
        for q, a in cfg['faq']:
            if q not in have:
                holder['mainEntity'].append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
        s = s[:jm.start(2)] + '\n' + json.dumps(d, ensure_ascii=False) + '\n' + s[jm.end(2):]
        done = True; break
    assert done, (f, 'no FAQPage data')
    # 4. title (cost page only) - title, og and twitter
    if cfg.get('title'):
        old = re.search(r'<title>(.*?)</title>', s).group(1)
        s = s.replace('<title>' + old + '</title>', '<title>' + cfg['title'] + '</title>', 1)
        s = s.replace('content="' + old + '"', 'content="' + cfg['title'] + '"')
        print('  title:', plain(old), '->', plain(cfg['title']))
    open(f, 'w', encoding='utf-8').write(s)
    print(f, 'ok: CTA +', len(cfg['faq']), 'FAQs')

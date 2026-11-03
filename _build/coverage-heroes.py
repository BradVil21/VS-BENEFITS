"""Coverage page heroes (2026-11-03): dental & vision, private market, short-term get the same
light hero as the home and small business pages (cutout photo, ribbon, ZIP box, rating).
Re-runnable: replaces the first <section class="hero"> (or an earlier cvh hero) on each page."""
import re, html

SB = open('small-business-health-insurance.html', encoding='utf-8').read()
m = re.search(r'/\* Small business page refresh.*?\n(.*?)/\* industry photo tiles \*/', SB, re.S)
BASE_CSS = m.group(1)
CSS = ('<style id="cvh-css">\n/* Coverage hero, same look as the small business hero (2026-11-03) */\n' + BASE_CSS +
       '.cvh .sb-img img{aspect-ratio:auto!important;object-fit:contain}\n'
       '@media(min-width:900px){.cvh .sb-img{width:min(460px,100%)}}\n'
       '@media(max-width:899px){.cvh .sb-hero .sb-img,.cvh.sb-hero .sb-img{width:min(320px,84%)}}\n'
       '</style>\n')

STARS = SB[SB.find('<a class="sb-rating"'):SB.find('</a>', SB.find('<a class="sb-rating"')) + 4]
RIB = re.search(r'<svg class="sb-ribbon".*?</svg>', SB, re.S).group(0)

ICON = {
 'smile': '<path d="M8 14s1.5 2 4 2 4-2 4-2"/><circle cx="12" cy="12" r="9"/><path d="M9 9h.01M15 9h.01"/>',
 'shield': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'eye': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
}
def chip(cls, ic, big, small):
    return ('<div class="sb-chip ' + cls + '"><i><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON[ic] + '</svg></i><span><b>' + big + '</b>' + small + '</span></div>')

PAGES = {
 'dental-vision-insurance.html': dict(
   eyebrow='Dental &amp; Vision Insurance',
   h1='Dental and Vision Coverage <span>Without the Guesswork</span>',
   sub='Cleanings, fillings, glasses and contacts. Compare plans from top carriers and keep your dentist and eye doctor in network.',
   label='Enter your ZIP code', img='dental-vision-cutout', w=668, h=636, alt='Woman laughing with a bright, healthy smile',
   chips=[chip('c1', 'smile', 'Dentist', 'in network'), chip('c2', 'eye', 'Glasses', '&amp; contacts')],
   quote='type=individual&amp;niche=dental-vision'),
 'private-health-insurance.html': dict(
   eyebrow='Private Market Plans',
   h1='Private Health Insurance <span>with PPO Networks</span>',
   sub='Privately underwritten PPO plans from top A-rated carriers, compared side by side by a licensed advisor, free.',
   label='Enter your ZIP code', img='private-market-cutout', w=673, h=692, alt='Smiling family of three hugging outdoors',
   chips=[chip('c1', 'shield', 'PPO', 'networks'), chip('c2', 'smile', '$0', 'to compare')],
   quote='type=individual&amp;niche=private'),
 'short-term-health-insurance.html': dict(
   eyebrow='Short-Term Coverage',
   h1='Short-Term Health Insurance <span>for the Gap Between Plans</span>',
   sub='Between jobs or waiting on new coverage? A short-term plan can start within days and cover unexpected illness and injury.',
   label='Enter your ZIP code', img='short-term-cutout', w=810, h=642, alt='Smiling father carrying his baby on his shoulders',
   chips=[chip('c1', 'clock', 'Starts', 'in days'), chip('c2', 'shield', 'Licensed', 'advisor')],
   quote='type=individual&amp;niche=short-term'),
}

for f, c in PAGES.items():
    s = open(f, encoding='utf-8').read()
    slug = f[:-5]
    hero = ('<section class="hero sb-hero cvh" aria-labelledby="cvh-h1">\n  <div class="container">\n    <div class="hero-grid">\n      <div>\n'
      '        <span class="eyebrow">' + c['eyebrow'] + '</span>\n'
      '        <h1 id="cvh-h1">' + c['h1'] + '</h1>\n'
      '        <p class="sb-sub">' + c['sub'] + '</p>\n'
      '        <form class="sbz" action="/quote" method="get" novalidate onsubmit="var z=this.zip.value.replace(/\\D/g,\'\');var e=this.querySelector(\'.sbz-err\');if(z.length!==5){e.hidden=false;this.zip.focus();return false}e.hidden=true;this.zip.value=z;">\n'
      '          ' + ''.join('<input type="hidden" name="%s" value="%s" />' % tuple(kv.split('=')) for kv in c['quote'].split('&amp;')) +
      '<input type="hidden" name="from" value="' + slug + '_zip" />\n'
      '          <label for="cvh-zip">' + c['label'] + '</label>\n'
      '          <div class="sbz-row"><input id="cvh-zip" name="zip" type="text" inputmode="numeric" pattern="[0-9]{5}" maxlength="5" placeholder="ZIP code" autocomplete="postal-code" required /><button type="submit">Find Affordable Plans</button></div>\n'
      '          <p class="sbz-err" role="alert" hidden>Please enter a valid 5-digit ZIP code.</p>\n'
      '        </form>\n        ' + STARS + '\n      </div>\n'
      '      <div class="sb-img">\n        ' + RIB.replace('sbg1', 'cvg1') + '\n'
      '        <img decoding="async" fetchpriority="high" srcset="/compressed/' + c['img'] + '-480.webp 480w, /compressed/' + c['img'] + '.webp ' + str(c['w']) + 'w" sizes="(max-width: 900px) 320px, 460px" '
      'src="/compressed/' + c['img'] + '.webp" width="' + str(c['w']) + '" height="' + str(c['h']) + '" alt="' + c['alt'] + '" loading="eager" />\n'
      '        ' + '\n        '.join(c['chips']) + '\n      </div>\n    </div>\n  </div>\n</section>')
    m = re.search(r'<section class="hero(?: sb-hero cvh)?"[^>]*>', s)
    i = m.start(); j = s.find('</section>', i) + len('</section>')
    old = s[i:j]
    s = s[:i] + hero + s[j:]
    s = re.sub(r'<style id="cvh-css">.*?</style>\n', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(s)
    print(f, 'hero replaced (old hero %d chars)' % len(old))

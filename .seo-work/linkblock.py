# -*- coding: utf-8 -*-
"""Reusable: inject a 'related guides' cross-link section before </footer>-adjacent point."""
import re

STYLE_ID = 'vs-rg-style'
STYLE = '''<style id="vs-rg-style">
.vs-related-guides{background:#f7faff;border-top:1px solid #e4e9f2;padding:44px 0}
.vs-related-guides .vs-rg-inner{width:100%;max-width:1160px;margin:0 auto;padding:0 18px}
.vs-related-guides h2{font-family:'Poppins','Inter',system-ui,sans-serif;color:#0b2346;font-size:1.35rem;margin:0 0 6px;line-height:1.25}
.vs-related-guides .vs-rg-sub{color:#5a6b80;font-size:.94rem;margin:0 0 22px}
.vs-rg-grid{display:grid;grid-template-columns:1fr;gap:14px}
.vs-rg-card{display:block;background:#fff;border:1px solid #e4e9f2;border-radius:14px;padding:18px 20px;text-decoration:none;transition:transform .2s,box-shadow .2s}
.vs-rg-card:hover{transform:translateY(-2px);box-shadow:0 8px 22px rgba(13,27,42,.09);text-decoration:none}
.vs-rg-card strong{display:block;font-family:'Poppins','Inter',sans-serif;color:#0b2346;font-size:1rem;line-height:1.35;margin-bottom:6px}
.vs-rg-card span{display:block;color:#5a6b80;font-size:.88rem;line-height:1.55}
.vs-rg-card em{display:inline-block;margin-top:9px;color:#16447f;font-weight:700;font-size:.85rem;font-style:normal}
@media(min-width:760px){.vs-rg-grid{grid-template-columns:1fr 1fr}}
</style>'''

def inject(path, marker, heading, sub, cards, cta='/quote', cta_text='Get a free quote'):
    """cards: list of (href, title, blurb). marker: unique id so we can update idempotently."""
    s = open(path, encoding='utf-8').read(); orig = s

    # remove a previously injected block with the same marker
    s = re.sub(r'<section class="vs-related-guides" data-block="%s">.*?</section>\s*' % re.escape(marker),
               '', s, flags=re.S)

    if STYLE_ID not in s and '.vs-related-guides{' not in s:
        s = s.replace('</head>', STYLE + '\n</head>', 1)

    cardhtml = ''.join(
        '\n        <a class="vs-rg-card" href="%s">\n          <strong>%s</strong>\n'
        '          <span>%s</span>\n          <em>Read the guide &rarr;</em>\n        </a>' % c
        for c in cards)
    section = ('<section class="vs-related-guides" data-block="%s">\n'
               '  <div class="vs-rg-inner">\n    <h2>%s</h2>\n'
               '    <p class="vs-rg-sub">%s Ready for numbers instead? '
               '<a href="%s" style="color:#16447f;font-weight:700">%s &rarr;</a></p>\n'
               '    <div class="vs-rg-grid">%s\n    </div>\n  </div>\n</section>\n\n'
               % (marker, heading, sub, cta, cta_text, cardhtml))

    i = s.rfind('<footer')
    if i < 0:
        i = s.rfind('</body>')
    s = s[:i] + section + s[i:]
    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
    return s != orig

# -*- coding: utf-8 -*-
"""VS does not place Medicaid. Strip Medicaid from everything that presents it
as a service we offer: the service card, the footer link, the /services block,
the about-page service list and the chatbot's service list. Informational
mentions inside guides (eligibility lines, enrollment-window facts) are handled
separately - they are content, not offers."""
import re, glob

CARD = re.compile(
    r'\s*<div class="card">\s*<div class="card-image">\s*<img[^>]*?/compressed/m\.jpg[^>]*>\s*</div>\s*'
    r'<div class="card-body">\s*<div class="ic">[^<]*</div>\s*<h3>Medicaid Guidance</h3>.*?</div>\s*</div>',
    re.S)
FOOTER_LI = re.compile(r'\s*<li><a href="/services#medicaid">Medicaid Guidance</a></li>')
BLOCK = re.compile(r'\s*<div id="medicaid" class="service-block">.*?</div>\s*</div>(?=\s*<div id=)', re.S)

cards = lis = blocks = 0
for f in sorted(glob.glob('*.html') + glob.glob('blog/*.html') + glob.glob('quote/*.html')):
    s = open(f, encoding='utf-8').read()
    o = s
    s, n1 = CARD.subn('', s); cards += n1
    s, n2 = FOOTER_LI.subn('', s); lis += n2
    s, n3 = BLOCK.subn('', s); blocks += n3
    if s != o:
        open(f, 'w', encoding='utf-8').write(s)
print('service cards removed:', cards)
print('footer links removed :', lis)
print('service blocks removed:', blocks)

# about.html service sentence
s = open('about.html', encoding='utf-8').read()
o = s
s = s.replace('Group, individual, family, ACA, Medicaid guidance, dental',
              'Group, individual, family, ACA, private market, dental')
s = s.replace('Group, individual, family, ACA, Medicaid, dental',
              'Group, individual, family, ACA, private market, dental')
if s != o:
    open('about.html', 'w', encoding='utf-8').write(s); print('about.html service list updated')

# chatbot service list
p = 'vs-benefits-chatbot-embed.js'
s = open(p, encoding='utf-8').read()
o = s
s = s.replace('ACA/Individual, Family, Dental & Vision, Medicaid',
              'ACA/Individual, Family, Dental & Vision, Private Market')
if s != o:
    open(p, 'w', encoding='utf-8').write(s); print('chatbot service list updated')

left = [f for f in glob.glob('*.html') + glob.glob('blog/*.html')
        if 'Medicaid Guidance' in open(f, errors='ignore').read()]
print('files still containing "Medicaid Guidance":', len(left), left[:6])

"""Small business state pages (2026-11-03).

Builds /<state>-small-business-health-insurance for every Service Areas state from the
main /small-business-health-insurance page, so every state page looks exactly like it.
Also adds a "Find your state" grid to the main page.

Run from the site root after editing small-business-health-insurance.html:
    python3 _build/build-sb-states.py
Safe to re-run. The first run saves the old FL/TX/KY/MD pages in .seo-work/sb-old/.
"""
import json, os, re, shutil, html

SITE = 'https://www.vshealthbenefits.com'
SRC = 'small-business-health-insurance.html'
ST = {
 'AL': ('Alabama', ['Birmingham', 'Montgomery', 'Huntsville', 'Mobile']),
 'AZ': ('Arizona', ['Phoenix', 'Tucson', 'Mesa', 'Scottsdale']),
 'AR': ('Arkansas', ['Little Rock', 'Fayetteville', 'Fort Smith', 'Jonesboro']),
 'CO': ('Colorado', ['Denver', 'Colorado Springs', 'Aurora', 'Fort Collins']),
 'FL': ('Florida', ['Miami', 'Tampa', 'Orlando', 'Jacksonville']),
 'GA': ('Georgia', ['Atlanta', 'Savannah', 'Augusta', 'Columbus']),
 'IL': ('Illinois', ['Chicago', 'Aurora', 'Naperville', 'Springfield']),
 'IN': ('Indiana', ['Indianapolis', 'Fort Wayne', 'Evansville', 'South Bend']),
 'IA': ('Iowa', ['Des Moines', 'Cedar Rapids', 'Davenport', 'Iowa City']),
 'KS': ('Kansas', ['Wichita', 'Overland Park', 'Kansas City', 'Topeka']),
 'KY': ('Kentucky', ['Louisville', 'Lexington', 'Bowling Green', 'Owensboro']),
 'LA': ('Louisiana', ['New Orleans', 'Baton Rouge', 'Shreveport', 'Lafayette']),
 'MD': ('Maryland', ['Baltimore', 'Columbia', 'Frederick', 'Annapolis']),
 'MI': ('Michigan', ['Detroit', 'Grand Rapids', 'Lansing', 'Ann Arbor']),
 'MN': ('Minnesota', ['Minneapolis', 'Saint Paul', 'Rochester', 'Duluth']),
 'MS': ('Mississippi', ['Jackson', 'Gulfport', 'Southaven', 'Hattiesburg']),
 'MO': ('Missouri', ['Kansas City', 'St. Louis', 'Springfield', 'Columbia']),
 'MT': ('Montana', ['Billings', 'Missoula', 'Great Falls', 'Bozeman']),
 'NE': ('Nebraska', ['Omaha', 'Lincoln', 'Bellevue', 'Grand Island']),
 'NV': ('Nevada', ['Las Vegas', 'Henderson', 'Reno', 'North Las Vegas']),
 'NC': ('North Carolina', ['Charlotte', 'Raleigh', 'Greensboro', 'Durham']),
 'ND': ('North Dakota', ['Fargo', 'Bismarck', 'Grand Forks', 'Minot']),
 'OH': ('Ohio', ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo']),
 'OK': ('Oklahoma', ['Oklahoma City', 'Tulsa', 'Norman', 'Broken Arrow']),
 'SC': ('South Carolina', ['Charleston', 'Columbia', 'Greenville', 'Myrtle Beach']),
 'SD': ('South Dakota', ['Sioux Falls', 'Rapid City', 'Aberdeen', 'Brookings']),
 'TN': ('Tennessee', ['Nashville', 'Memphis', 'Knoxville', 'Chattanooga']),
 'TX': ('Texas', ['Houston', 'Dallas', 'San Antonio', 'Austin']),
 'UT': ('Utah', ['Salt Lake City', 'Provo', 'West Valley City', 'St. George']),
 'VA': ('Virginia', ['Virginia Beach', 'Richmond', 'Norfolk', 'Arlington']),
 'WV': ('West Virginia', ['Charleston', 'Huntington', 'Morgantown', 'Parkersburg']),
 'WI': ('Wisconsin', ['Milwaukee', 'Madison', 'Green Bay', 'Kenosha']),
 'WY': ('Wyoming', ['Cheyenne', 'Casper', 'Laramie', 'Gillette']),
}
# Pages that already rank: keep their Google titles.
KEEP_TITLE = {
 'FL': 'Group Health Insurance for Florida Small Business 2027',
 'TX': 'Group Health Insurance Texas | Small Business Plans',
 'KY': 'Group Health Insurance Kentucky | Small Business',
 'MD': 'Group Health Insurance Maryland | Small Business',
}

def slug(n): return n.lower().replace(' ', '-')
def url(c): return '/' + slug(ST[c][0]) + '-small-business-health-insurance'

def rep(s, a, b, n=1):
    assert s.count(a) == n, (s.count(a), a[:80])
    return s.replace(a, b)

GRID_CSS = ('<style id="sbst-css">.sbst{padding:56px 0}.sbst h2{margin-bottom:10px}.sbst-lede{max-width:760px;color:#334155;font-size:1.05rem;line-height:1.6}'
  '.sbst-cities{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 6px;padding:0;list-style:none}.sbst-cities li{background:#fff;border:1px solid #dbe7f7;border-radius:999px;padding:7px 14px;font-weight:600;font-size:.9rem;color:#0b2346}'
  '.sbst-links{display:flex;flex-wrap:wrap;gap:10px 18px;margin-top:18px;font-weight:700}.sbst-links a{color:#16447f}'
  '.sbst-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:8px;margin-top:18px}.sbst-grid a{display:block;background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:10px 12px;color:#0b2346;font-weight:600;font-size:.92rem;text-decoration:none}'
  '.sbst-grid a:hover{border-color:#0db5a6;background:#f3fbfa}.sbst-grid a[aria-current]{background:#0b2346;color:#fff;border-color:#0b2346}</style>')

def grid(cur=None):
    return '<div class="sbst-grid">' + ''.join(
        '<a href="%s"%s>%s</a>' % (url(c), ' aria-current="page"' if c == cur else '', ST[c][0])
        for c in sorted(ST, key=lambda c: ST[c][0])) + '</div>'

def state_section(c):
    n, cities = ST[c]
    cl = ', '.join(cities[:-1]) + ' or ' + cities[-1]
    return (GRID_CSS + '\n<section class="section sbst" id="state-coverage"><div class="container">'
      '<span class="eyebrow">' + n + '</span>'
      '<h2>Small Business Health Insurance in ' + n + '</h2>'
      '<p class="sbst-lede">We help ' + n + ' employers with 2 to 50 employees compare group, level-funded and ICHRA options from the carriers that sell in their county. '
      'Whether your business is in ' + cl + ', one licensed advisor builds your quotes, enrolls your team and handles every renewal, free.</p>'
      '<ul class="sbst-cities" aria-label="' + n + ' cities we serve">' + ''.join('<li>' + x + '</li>' for x in cities) + '<li>All of ' + n + '</li></ul>'
      '<div class="sbst-links"><a href="/health-insurance-' + slug(n) + '">Individual &amp; family plans in ' + n + ' &rarr;</a>'
      '<a href="/small-business-health-insurance">Small business health insurance overview &rarr;</a></div>'
      '<h3 style="margin-top:34px;font-size:1.1rem">Other states we serve</h3>' + grid(c) +
      '</div></section>\n')

def main_section():
    return (GRID_CSS + '\n<section class="section sbst" id="by-state"><div class="container">'
      '<span class="eyebrow">Service Areas</span><h2>Small Business Health Insurance by State</h2>'
      '<p class="sbst-lede">Pick your state to see group plan options for your business.</p>' + grid() + '</div></section>\n')

src = open(SRC, encoding='utf-8').read()
# ---- main page: state grid + forward old ?state=XX links to the state page ----
if 'id="by-state"' not in src:
    i = src.find('Who We Serve'); j = src.rfind('<section', 0, i)
    src = src[:j] + main_section() + src[j:]
fwd = ('<script id="sbst-fwd">(function(){try{var m={%s},c=(new URLSearchParams(location.search).get("state")||"").toUpperCase();'
       'if(m[c])location.replace(m[c]+location.search.replace(/([?&])state=[^&]*&?/,"$1").replace(/[?&]$/,"")+location.hash);}catch(e){}})();</script>') % ','.join('%s:"%s"' % (c, url(c)) for c in ST)
src = re.sub(r'<script id="sbst-fwd">.*?</script>', '', src)
src = src.replace('</head>', fwd + '\n</head>', 1)
open(SRC, 'w', encoding='utf-8').write(src)

base = re.sub(r'<script id="sbst-fwd">.*?</script>\n?', '', src)
i = base.find('id="by-state"'); a = base.rfind('<style id="sbst-css">', 0, i); b = base.find('</section>', i) + len('</section>\n')
base = base[:a] + base[b:]

os.makedirs('.seo-work/sb-old', exist_ok=True)
built = []
for c, (n, cities) in ST.items():
    out = url(c)[1:] + '.html'
    if os.path.exists(out) and not os.path.exists('.seo-work/sb-old/' + out) and 'id="state-coverage"' not in open(out, encoding='utf-8').read():
        shutil.copy(out, '.seo-work/sb-old/' + out)
    s = base
    title = KEEP_TITLE.get(c, n + ' Small Business Health Insurance | 2027 Group Plans')
    desc = n + ' small business health insurance for teams of 2 to 50: group, level-funded and ICHRA plans compared side by side by a licensed independent broker. Free quote in minutes.'
    old_t = 'Small Business Health Insurance: 2027 Group Plans, 2-50 Staff'
    s = rep(s, '<title>' + old_t, '<title>' + title)
    s = s.replace('content="' + old_t + '"', 'content="' + title + '"')
    s = s.replace('Small business health insurance for teams of 2 to 50: group, level-funded and ICHRA compared side by side by a licensed independent broker. Free quote in minutes.', desc)
    s = s.replace(SITE + '/small-business-health-insurance"', SITE + url(c) + '"')
    s = rep(s, 'Group Health Insurance &middot; 40+ States', 'Group Health Insurance &middot; ' + n)
    s = rep(s, 'Small Business Health Insurance for <span>', n + ' Small Business Health Insurance for <span>')
    s = rep(s, 'Group plans from top A-rated carriers, compared and set up for you, free.', 'Group plans from top A-rated carriers in ' + n + ', compared and set up for you, free.')
    s = rep(s, 'name="from" value="small-business-health-insurance_zip" />', 'name="from" value="' + url(c)[1:] + '_zip" /><input type="hidden" name="state" value="' + c + '" />')
    s = rep(s, 'Enter your business ZIP code', 'Enter your ' + n + ' business ZIP code')
    s = rep(s, 'small employers in 40+ states', 'small employers across ' + n + ' and 40+ states')
    s = s.replace('"areaServed":"US"', '"areaServed":{"@type":"State","name":"' + n + '"}')
    s = rep(s, '"name": "Small Business Group Health Insurance 2027"}', '"name": "Small Business Health Insurance", "item": "' + SITE + '/small-business-health-insurance"}, {"@type": "ListItem", "position": 3, "name": "' + n + '"}')
    # FAQ: one state question, on the page and in the FAQ data
    q = 'Can a small business in ' + n + ' get group health insurance with only 2 employees?'
    ans = ('Yes. Small group plans in ' + n + ' are guaranteed issue for employers with 1 to 50 employees, so no one can be turned down for health reasons. '
           'Most carriers want at least one W-2 employee besides the owner and roughly 70% of eligible employees enrolled. A licensed advisor checks which carriers sell in your county, free.')
    m = re.search(r'(<script type="application/ld\+json">)(\s*\{"@context": "https://schema.org", "@type": "FAQPage".*?)(</script>)', s, re.S)
    d = json.loads(m.group(2)); d['mainEntity'].insert(0, {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ans}})
    s = s[:m.start(2)] + json.dumps(d, ensure_ascii=False) + s[m.end(2):]
    fq = re.search(r'<details[^>]*>\s*<summary[^>]*>\s*How many employees do I need for group health insurance\?', s)
    if fq:
        seg_end = s.find('</details>', fq.start()) + len('</details>')
        first = s[fq.start():seg_end]
        summ = re.search(r'(<summary[^>]*>)(.*?)(</summary>)', first, re.S)
        body = re.sub(r'(<summary[^>]*>).*?(</summary>)', lambda x: x.group(1) + html.escape(q) + (summ.group(2)[summ.group(2).find('<'):] if '<' in summ.group(2) else '') + x.group(2), first, count=1, flags=re.S)
        body = re.sub(r'(</summary>\s*<div[^>]*>\s*(?:<p>)?).*?((?:</p>)?\s*</div>\s*</details>)', lambda x: x.group(1) + html.escape(ans) + x.group(2), body, count=1, flags=re.S)
        s = s[:fq.start()] + body + '\n' + s[fq.start():]
    # state section before "Who We Serve"
    i = s.find('Who We Serve'); j = s.rfind('<section', 0, i)
    s = s[:j] + state_section(c) + s[j:]
    open(out, 'w', encoding='utf-8').write(s)
    built.append(out)
print('main page updated; built', len(built), 'state pages')

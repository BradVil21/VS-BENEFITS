import re, json, sys, os, shutil
root = sys.argv[1]
work = os.path.join(root, '.seo-work', 'phi')
p = os.path.join(root, 'private-health-insurance.html')
src = open(p, encoding='utf-8').read()
os.makedirs(os.path.join(root, '.seo-work'), exist_ok=True)
bak = os.path.join(root, '.seo-work', 'private-health-insurance.before-2026-11-04-rebuild.html')
if not os.path.exists(bak):
    shutil.copy(p, bak)
    print('backup', bak)
else:
    src = open(bak, encoding='utf-8').read()  # always patch from the original

def one(pat, s, flags=re.S):
    m = re.findall(pat, s, flags)
    assert len(m) >= 1, pat
    return m[0]

rating = one(r'(<a class="sb-rating".*?</a>)', src)
heroimg = one(r'<div class="sb-img">\s*(.*?)\s*</div>\s*</div>\s*</div>\s*</section>', src)
assert 'private-market-cutout' in heroimg and 'sb-chip c2' in heroimg

TITLE = 'Private Health Insurance for Self-Employed &amp; High Earners'
DESC = 'Make too much for ACA subsidies? Compare private PPO plans with nationwide networks, priced on age and health, not income. Free licensed comparison.'
KW = 'private health insurance, private health insurance for self-employed, health insurance for high earners, too much income for health insurance subsidy, private ppo plans, nationwide ppo health insurance, non-marketplace health insurance, health insurance without subsidy'

faq = [
 ("Can I switch to a private plan mid-year?",
  "Generally, yes. Medically underwritten private plans are not tied to open enrollment, so you can apply in any month. If you are approved, you choose a start date, and you cancel your current plan only after the new policy is issued in writing. Two things to know first: money you have already paid toward this year's deductible usually does not carry over to a new plan, and if you have been getting an advance premium tax credit on a Marketplace plan, end that plan properly so your tax reconciliation is clean."),
 ("Do private plans cover pre-existing conditions?",
  "Not the way ACA plans do. Marketplace plans must cover pre-existing conditions. Underwritten private plans ask health questions, and the carrier can accept you at the quoted rate, charge more, exclude a specific condition, or decline the application. If you have an ongoing condition, are pregnant, or take a maintenance medication, a Marketplace plan is often the safer choice, and we will tell you that up front. Always get any exclusion language in writing before you drop the coverage you have."),
 ("Do I need to wait for a special enrollment period?",
  "Not for an underwritten private plan. Open enrollment and special enrollment periods are rules for ACA Marketplace plans; private underwritten plans accept applications year-round, subject to approval. If you want a Marketplace plan instead, open enrollment for 2027 coverage runs November 1, 2026 to January 15, 2027 in most states, and outside that window you need a qualifying life event."),
 ("Is private health insurance cheaper than a Marketplace plan?",
  "It depends on whether you qualify for a premium tax credit. If you do, the credit only works on Marketplace plans, and a private plan rarely beats a subsidized premium. If your income is above the cutoff, you pay the full Marketplace price, and that is where a privately underwritten plan for a healthy applicant often comes in lower. We check your subsidy number before quoting either one."),
 ("Can I be turned down for a private plan?",
  "Yes. That is the trade for the lower price and the wider network. Based on your answers and, in some cases, a prescription history check, a carrier can accept you, charge more than the quoted rate, exclude a condition, or decline you. Applying does not obligate you to anything, and a decline does not affect your right to enroll in a Marketplace plan during an enrollment window."),
 ("Do subsidies work with private plans?",
  "No. Premium tax credits exist only on Marketplace plans, so with a private plan you pay the full premium. Self-employed people can generally still deduct their premiums under the self-employed health insurance deduction, which applies to both types of plan. Ask your tax professional how it applies to you."),
 ("What is private health insurance?",
  "Here it means major medical coverage bought directly from an insurance company or through a broker, rather than through HealthCare.gov or a state exchange. The key difference is underwriting: a private plan asks health questions and decides whether to cover you, while a Marketplace plan must accept everyone who applies during an enrollment window."),
]
from html import escape
faq_html = '\n'.join('<details class="faq-item"><summary>%s</summary><p>%s</p></details>' % (escape(q), escape(a)) for q, a in faq)
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
video_ld = {"@context": "https://schema.org", "@type": "VideoObject",
    "name": "Full-price Marketplace premiums: a family quote on Nevada Health Link",
    "description": "Screen recording of a full-price family health insurance quote on Nevada Health Link with no subsidy applied: Bronze and Silver HMO plans from about $1,288 to $1,925 a month with deductibles from $11,000 to $21,200.",
    "thumbnailUrl": ["https://www.vshealthbenefits.com/compressed/marketplace-full-price-premiums-poster.jpg"],
    "uploadDate": "2026-11-04T12:00:00-05:00", "duration": "PT45S",
    "contentUrl": "https://www.vshealthbenefits.com/videos/marketplace-full-price-premiums.mp4",
    "embedUrl": "https://www.vshealthbenefits.com/private-health-insurance#full-price-video",
    "publisher": {"@id": "https://vshealthbenefits.com/#org"}}

out = src
out = re.sub(r'<title>.*?</title>', '<title>%s</title>' % TITLE, out, count=1)
out = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="%s"' % DESC, out, count=1)
out = re.sub(r'<meta name="keywords" content="[^"]*"', '<meta name="keywords" content="%s"' % KW, out, count=1)
out = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="Paying Full Price for Health Insurance? Compare Private PPO Plans"', out, count=1)
out = re.sub(r'<meta property="og:description" content="[^"]*"', '<meta property="og:description" content="%s"' % DESC, out, count=1)
out = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="https://www.vshealthbenefits.com/compressed/marketplace-full-price-premiums-poster.jpg"', out, count=1)
out = out.replace('<meta name="twitter:card" content="summary_large_image" />',
    '<meta name="twitter:card" content="summary_large_image" />\n<meta name="twitter:title" content="Paying Full Price for Health Insurance? Compare Private PPO Plans" />\n<meta name="twitter:description" content="%s" />' % DESC, 1)
n0 = len(out)
out, k = re.subn(r'<script type="application/ld\+json">\s*\{"@context":"https://schema.org","@type":"FAQPage".*?</script>',
    lambda m: '<script type="application/ld+json">\n' + json.dumps(faq_ld, ensure_ascii=False) + '\n</script>\n<script type="application/ld+json">\n' + json.dumps(video_ld, ensure_ascii=False) + '\n</script>', out, count=1, flags=re.S)
assert k == 1, 'faq schema'
def fix_article(m):
    s = m.group(0)
    s = re.sub(r'"headline":"[^"]*"', '"headline":"Private Health Insurance for Self-Employed & High Earners"', s)
    s = re.sub(r'"description":"[^"]*"', '"description":"Why people who earn too much for ACA subsidies compare private PPO plans: nationwide networks, doctor choice and pricing based on health and age, with the trade-offs explained."', s, count=1)
    s = re.sub(r'"dateModified":"[^"]*"', '"dateModified":"2026-11-04"', s)
    return s
out, k = re.subn(r'<script type="application/ld\+json">\s*\{"@context":"https://schema.org","@type":"Article".*?</script>', fix_article, out, count=1, flags=re.S)
assert k == 1, 'article'
css = open(os.path.join(work, 'phi.css'), encoding='utf-8').read()
out = out.replace('</head>', css + '</head>', 1)
main = open(os.path.join(work, 'phi-main.html'), encoding='utf-8').read().strip()
main = main.replace('%%RATING%%', rating).replace('%%HEROIMG%%', heroimg).replace('%%FAQ%%', faq_html)
out, k = re.subn(r'<main>.*?</main>', lambda m: main, out, count=1, flags=re.S)
assert k == 1, 'main'
# related guides: point the CTA at the private quote
out = out.replace('Ready for numbers? <a href="/quote"', 'Ready for numbers? <a href="/quote?type=individual&amp;niche=private&amp;from=private-health-insurance_related"', 1)
open(p, 'w', encoding='utf-8').write(out)
# sitemap lastmod
sm = os.path.join(root, 'sitemap.xml')
s = open(sm, encoding='utf-8').read()
s2 = re.sub(r'(<loc>https://www.vshealthbenefits.com/private-health-insurance</loc><lastmod>)[^<]*', r'\g<1>2026-11-04', s)
open(sm, 'w', encoding='utf-8').write(s2)
print('ok', len(src), '->', len(out), 'sitemap changed:', s != s2)

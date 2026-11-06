import re, json, html
src = open('blog/cigna-leaving-aca-marketplace-2027.html', encoding='utf-8').read()
SLUG = 'state-farm-agents-losing-health-insurance'
URL = 'https://www.vshealthbenefits.com/blog/' + SLUG
TITLE = 'State Farm Agents Losing Health Insurance: What to Do Now'
DESC = "State Farm is ending health coverage for its 19,000 agents and their spouses. Your 2027 options, subsidy and tax rules, and how to replace it with no gap."
IMG = 'https://www.vshealthbenefits.com/compressed/business-owner-office.jpg'
FROM = 'blog-' + SLUG
QUOTE = '/quote?type=individual&amp;from=' + FROM

faq = [
 ("Is State Farm ending health insurance for its agents?",
  "Yes. Reporting since May 2026 says State Farm will no longer offer health insurance to its roughly 19,000 exclusive agents and their spouses as part of a new agent contract. When State Farm reversed part of its deferred compensation change in June 2026, it did not reverse the end of agent health and life insurance support."),
 ("When does State Farm agent health insurance end?",
  "Reports differ on the exact date. Local coverage in Bloomington, Illinois said support for agent health and life insurance ends at the end of 2026, while other reports tie the changes to the new contract that agents must sign by 2028. Check the notice State Farm sent you, and plan replacement coverage before that date so there is no gap."),
 ("Can State Farm agents get an ACA subsidy?",
  "Possibly. As self-employed independent contractors, agents qualify based on their household's projected 2027 modified adjusted gross income, which for most agents starts with net business profit, not gross commissions. With the enhanced credits expired, there is no credit above 400% of the federal poverty level, roughly $63,000 for a single person and about $130,000 for a family of four. Lower or less predictable commissions can move some agents under that line."),
 ("Can I deduct health insurance premiums as a State Farm agent?",
  "Self-employed people can generally deduct health insurance premiums for themselves, a spouse and dependents under the self-employed health insurance deduction, as long as they are not eligible for an employer plan through a spouse's job and the deduction does not exceed business net profit. Confirm with your tax professional."),
 ("Can my agency set up a group health plan for me and my team?",
  "Usually, if you have at least one W-2 employee who is not you or your spouse. A small group plan, an ICHRA or a QSEHRA can then cover your team, and a group plan can cover you as the owner too. An agency with only the owner and a spouse generally cannot buy a small group plan and uses individual coverage instead."),
 ("What happens to retired State Farm agents' Medicare supplement support?",
  "Reports say the Medicare supplement support for retired agents, about $2,400 a year per person ($4,800 with a spouse), ends at the end of 2026. That support ending does not by itself cancel your Medicare or Medigap policy; it means you pay more of the premium yourself."),
]

body = '''
      <meta itemprop="datePublished" content="2026-11-05" />
      <meta itemprop="dateModified" content="2026-11-05" />
      <span class="eyebrow">Insurance Agency Owners | 7 min read</span>
      %%META%%
      <h1 itemprop="headline">State Farm Agents Are Losing Their Health Insurance: What to Do Now</h1>
      <p class="lede">State Farm is ending health coverage for its roughly 19,000 agents and their spouses. Here is what is changing, what your 2027 options are as a self-employed agency owner, and how to replace your plan without a gap.</p>
      <div class="hero-img">
        <img decoding="async" src="/compressed/business-owner-office.jpg" alt="Insurance agency owner standing in his office" width="739" height="323" itemprop="image" style="object-position:70% 30%" />
      </div>

      <p class="vs-pillar-link" style="font-size:.95rem;color:#334155">Open Enrollment for 2027 runs November 1 to January 15. Choose a plan by December 15 for coverage that starts January 1. <a href="/blog/aca-open-enrollment-2027-guide">Open Enrollment 2027 guide</a>.</p>
<aside class="vs-bq" aria-label="Get help replacing your State Farm agent health plan">
<strong class="t">State Farm agent? Let us replace your plan</strong>
<p>A licensed, independent advisor compares Marketplace and private PPO plans for you and your spouse, checks your doctors, and can set up group coverage for your agency team. Free, no obligation.</p>
<form action="/quote" method="get"><input type="hidden" name="type" value="individual"><input type="hidden" name="from" value="%%FROM%%"><input name="zip" inputmode="numeric" pattern="[0-9]{5}" maxlength="5" placeholder="Your ZIP code" aria-label="Your ZIP code" required autocomplete="postal-code"><button type="submit">Compare my options &rarr;</button></form>
<span class="alt">Prefer to talk? <a href="tel:+19548251009">(954) 825-1009</a></span>
</aside>

<h2 id="short">The short answer</h2>
<p>State Farm is moving its exclusive agents to a new contract, and health insurance for agents and their spouses is not part of it. In June 2026 State Farm walked back part of its deferred compensation change, but it did not reverse the end of agent health and life insurance support. If your health plan comes through State Farm, you need your own coverage before it ends.</p>
<div class="vs-tw"><table class="vs-t" style="min-width:0">
<thead><tr><th>Key fact</th><th>What it means</th></tr></thead>
<tbody>
<tr><td><strong>~19,000 agents</strong></td><td>Exclusive State Farm agents affected by the new contract, plus their spouses.</td></tr>
<tr><td><strong>~$585 a month</strong></td><td>What agents reportedly paid per person for the State Farm plan. Replacement coverage may cost more or less depending on age, income and health.</td></tr>
<tr><td><strong>End of 2026</strong></td><td>When local reporting says agent health and life insurance support ends. Other reports tie it to the new contract due by 2028. Check your notice.</td></tr>
<tr><td><strong>$2,400 a year</strong></td><td>Medicare supplement support per retired agent ($4,800 with a spouse), reported to end at the end of 2026.</td></tr>
<tr><td><strong>Dec 15</strong></td><td>Pick a Marketplace plan by this date in HealthCare.gov states for a January 1 start.</td></tr>
</tbody></table></div>

<h2 id="what-changed">What State Farm changed</h2>
<p>In May 2026 State Farm told agents it was replacing its several agent contract types with one new agreement built around digital sales and new-business incentives. Along with lower base compensation and the end of the Annual Investment Payment Program (AIPP), agents learned that State Farm would no longer offer health insurance to agents and their spouses. Agents also reported that dental and vision coverage was ending. A May 19 letter to retired agents said their non-contractual group benefits and Medicare supplement support end at the end of 2026.</p>
<p>After strong pushback, State Farm restored AIPP payments for 2026 through 2028 in a June 12 message to agents. The health insurance change stayed. Agents who do not sign the new agreement can apply for a transition program instead.</p>
<p>Whatever you decide about the contract, the health insurance question is the same: you are a self-employed business owner who now buys your own coverage.</p>

<h2 id="who">Who is affected</h2>
<ul>
<li><strong>Agents and spouses</strong> covered through State Farm's agent health plan. If your children are on the plan, confirm in your notice how their coverage ends.</li>
<li><strong>Retired agents</strong> who received Medicare supplement support. See <a href="#retired">retired agents</a> below.</li>
<li><strong>Your agency team, indirectly.</strong> Your team members are your employees, not State Farm's. If you were planning to rely on State Farm benefits for your own family, this is a good moment to decide whether a group plan for the whole agency makes more sense.</li>
</ul>

<h2 id="options">Your 2027 health insurance options</h2>
<p>State Farm agents are independent contractors, so the options are the same as for any self-employed business owner. Which one wins depends mostly on your household income, your health and whether you have employees.</p>
<div class="vs-tw"><table class="vs-t">
<thead><tr><th>Option</th><th>Best for</th><th>Watch out for</th></tr></thead>
<tbody>
<tr><td><strong>ACA Marketplace plan</strong></td><td>Agents whose household income is under the subsidy limit, or anyone with a health condition. Guaranteed acceptance, pre-existing conditions covered.</td><td>Many plans are HMO or EPO networks. Above the 400% line you pay full price.</td></tr>
<tr><td><strong>Private PPO plan</strong></td><td>Healthy agents earning too much for a subsidy who want a national PPO network.</td><td>Medically underwritten: health questions, possible exclusions or decline.</td></tr>
<tr><td><strong>Group plan for your agency</strong></td><td>Agencies with at least one W-2 employee besides you and your spouse. Covers you and your team.</td><td>Carrier participation and contribution rules; you pay part of employee premiums.</td></tr>
<tr><td><strong>ICHRA or QSEHRA</strong></td><td>Agencies that want a fixed monthly budget and let each person pick an individual plan.</td><td>An ICHRA can cost your employees their premium tax credit. Owners generally can't use it for themselves unless set up as an employee.</td></tr>
<tr><td><strong>Spouse's employer plan</strong></td><td>Agents whose spouse has job-based coverage.</td><td>Compare the family premium with buying your own.</td></tr>
</tbody></table></div>
<p>Comparing private plans? Read <a href="/private-health-insurance">private health insurance for self-employed people and high earners</a>. Setting up coverage for your team? See <a href="/small-business-health-insurance">small business health insurance</a> and <a href="/ichra-florida-small-business">how ICHRA works</a>.</p>

<div class="cta-block">
<h3>Get both numbers side by side</h3>
<p>We show you the Marketplace price after any subsidy next to private PPO options for you and your spouse, and a group option if you have employees. Free, licensed, independent.</p>
<a class="btn btn-teal" href="%%QUOTE%%">Compare my options &rarr;</a>
</div>

<h2 id="subsidy">Will you qualify for a subsidy?</h2>
<p>Premium tax credits are based on your household's projected 2027 modified adjusted gross income. For an agent, that starts with net profit from the agency after business expenses, not gross commissions. With the enhanced credits expired, there is no credit above 400% of the federal poverty level: roughly $63,000 for a single person and about $130,000 for a family of four.</p>
<p>Two things make this worth a careful estimate this year. Lower base compensation and the shift to new-business incentives can make 2027 income harder to predict. And retirement contributions such as a SEP IRA or Solo 401(k), plus HSA contributions, can lower the income that counts. See <a href="/blog/what-income-counts-for-aca-subsidies">what income counts for ACA subsidies</a> and the <a href="/aca-subsidy-calculator">subsidy calculator</a>.</p>

<h2 id="timing">Timing: how to avoid a gap</h2>
<ol>
<li><strong>Find your end date.</strong> Read the notice from State Farm and note the last day of coverage for you, your spouse and any children.</li>
<li><strong>Use Open Enrollment if your plan ends December 31.</strong> Open Enrollment runs November 1, 2026 to January 15, 2027. Enroll by December 15 for a January 1 start.</li>
<li><strong>If it ends at another time,</strong> losing qualifying health coverage generally opens a 60-day special enrollment period. You can usually apply up to 60 days before the coverage ends, so the new plan starts the day after.</li>
<li><strong>Private plans don't wait for a window.</strong> Underwritten private plans accept applications year-round. Apply early so approval comes before your old plan ends, and keep your current coverage until the new policy is issued.</li>
<li><strong>List your doctors and prescriptions</strong> and check them against every plan before you enroll.</li>
</ol>

<h2 id="taxes">The tax side</h2>
<p>As self-employed business owners, agents can generally deduct health insurance premiums for themselves, a spouse and dependents under the self-employed health insurance deduction, as long as they are not eligible for an employer plan through a spouse's job and the deduction does not exceed the agency's net profit. If you also get a premium tax credit, the two interact, so plan with your tax professional. More: <a href="/blog/truck-driver-health-insurance-tax-write-off">how the self-employed health insurance deduction works</a>.</p>

<h2 id="team">Covering your agency team</h2>
<p>If you have W-2 team members, you have more choices than an individual agent. A small group plan can cover you, your spouse if employed, and your staff, often with a broader network than individual plans. An ICHRA or QSEHRA lets you give each person a monthly allowance toward their own plan. If it is only you and your spouse, you generally cannot buy a small group plan; see <a href="/blog/husband-and-wife-business-health-insurance">health insurance for a husband-and-wife business</a>.</p>

<h2 id="retired">If you are a retired agent</h2>
<p>Reports say the Medicare supplement support for retired agents, about $2,400 a year per person or $4,800 with a spouse, ends at the end of 2026. Losing that support does not cancel your Medicare or Medigap policy by itself; it means more of the premium comes out of your pocket. If you are not yet 65 and lose retiree coverage, see <a href="/health-insurance-before-medicare">health insurance before Medicare</a>.</p>

<h2 id="how-we-help">How VS Health Benefits can help</h2>
<p>We are a licensed, independent health insurance brokerage. We work with insurance professionals the same way we work with any small business owner, and we know you'll read the fine print. We will:</p>
<ul>
<li>Run your 2027 subsidy estimate from your agency's projected net profit.</li>
<li>Compare Marketplace plans and private PPO plans for you and your spouse, side by side.</li>
<li>Quote a group plan, ICHRA or QSEHRA if you have team members.</li>
<li>Check your doctors and prescriptions before you apply, and line up the start date so there is no gap.</li>
</ul>
<p>There is no fee. Carriers pay our commission, and the price is the same as buying direct. We serve 40+ states in English and Spanish.</p>

<p class="vs-src">Sources: <a href="https://www.wvik.org/illinois/2026-05-27/state-farm-reduces-compensation-for-19-000-agents" target="_blank" rel="noopener">WGLT/WVIK, State Farm reduces compensation for 19,000 agents (May 27, 2026)</a>; <a href="https://www.nprillinois.org/illinois/2026-06-02/boiling-mad-and-fearing-an-uncertain-future-state-farm-agents-react-to-contract-changes" target="_blank" rel="noopener">NPR Illinois, agents react to contract changes (Jun 2, 2026)</a>; <a href="https://www.insurancebusinessmag.com/us/news/breaking-news/state-farm-blinked--that-doesnt-mean-their-agents-won-579449.aspx" target="_blank" rel="noopener">Insurance Business, State Farm blinked (Jun 18, 2026)</a>; <a href="https://www.wglt.org/local-news/2026-06-26/state-farm-slows-changes-for-agent-contracts" target="_blank" rel="noopener">WGLT, State Farm slows changes for agent contracts (Jun 26, 2026)</a>; <a href="https://hrexecutive.com/state-farm-agents-accuse-company-of-false-promises-after-benefits-overhaul/" target="_blank" rel="noopener">HR Executive (Jun 22, 2026)</a>. VS Health Benefits is not affiliated with State Farm. Details of your coverage are in the notices State Farm sent you.</p>

<h2 id="faq">Frequently asked</h2>
%%FAQ%%
'''
faq_html = ''.join('<h3>%s</h3><p>%s</p>' % (html.escape(q), html.escape(a)) for q, a in faq)
s = src
# head
s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % html.escape(TITLE), s, 1)
for k in ['description', 'twitter:description']:
    s = re.sub(r'(<meta name="%s" content=")[^"]*' % re.escape(k), lambda m: m.group(1) + html.escape(DESC), s)
for k in ['og:description']:
    s = re.sub(r'(<meta property="%s" content=")[^"]*' % re.escape(k), lambda m: m.group(1) + html.escape(DESC), s)
s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(TITLE), s)
s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + html.escape(TITLE), s)
s = re.sub(r'(<meta (?:property|name)="(?:og|twitter):image" content=")[^"]*', lambda m: m.group(1) + IMG, s)
s = s.replace('content="2026-10-30T08:00:00-04:00"', 'content="2026-11-05T10:00:00-05:00"')
s = s.replace('https://www.vshealthbenefits.com/blog/cigna-leaving-aca-marketplace-2027', URL)
# Article + breadcrumb schema
s = s.replace('"headline": "Cigna Is Leaving the ACA Marketplace in 2027: What to Do"', '"headline": %s' % json.dumps(TITLE))
s = re.sub(r'("@type": "Article",\s*"headline": [^\n]+\n\s*"description": )"[^"]*"', lambda m: m.group(1) + json.dumps(DESC), s)
s = s.replace('"image": "https://www.vshealthbenefits.com/compressed/cigna-exit-og.jpg"', '"image": "%s"' % IMG)
s = s.replace('"datePublished": "2026-10-30"', '"datePublished": "2026-11-05"').replace('"dateModified": "2026-10-30"', '"dateModified": "2026-11-05"')
s = s.replace('"name": "Cigna Is Leaving the ACA Marketplace in 2027: What to Do"', '"name": %s' % json.dumps(TITLE))
# FAQ schema
fs = '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, indent=2, ensure_ascii=False) + '\n</script>'
s, k = re.subn(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>', lambda m: fs, s, count=1, flags=re.S)
assert k == 1, 'faq schema'
# article body
a = s.index('<article class="article-body"'); a = s.index('>', a) + 1
b = s.index('    </article>')
meta = re.search(r'<div class="article-meta">.*?</div>', s[a:b], re.S).group(0).replace('October 30, 2026', 'November 5, 2026')
s = s[:a] + body.replace('%%META%%', meta).replace('%%FROM%%', FROM).replace('%%QUOTE%%', QUOTE).replace('%%FAQ%%', faq_html) + s[b:]
# sidebar
s = re.sub(r'<ul class="toc-list">.*?</ul>', '<ul class="toc-list"><li><a href="#short">The Short Answer</a></li><li><a href="#what-changed">What Changed</a></li><li><a href="#options">Your Options</a></li><li><a href="#subsidy">Subsidies</a></li><li><a href="#timing">Avoid a Gap</a></li><li><a href="#team">Your Agency Team</a></li><li><a href="#retired">Retired Agents</a></li><li><a href="#faq">FAQ</a></li></ul>', s, 1, flags=re.S)
s = s.replace('<h4 style="color:#fff">Have a Cigna plan?</h4>', '<h4 style="color:#fff">State Farm agent?</h4>')
s = s.replace('We compare every 2027 plan in your ZIP and check your doctors, free.', 'We compare Marketplace and private PPO plans for you and your spouse, free.')
s = s.replace('/premium-increase-review?from=blog-cigna-leaving-aca-marketplace-2027', QUOTE)
s = s.replace('blog-cigna-leaving-aca-marketplace-2027', FROM).replace('blog/cigna-leaving-aca-marketplace-2027', 'blog/' + SLUG).replace('/blog/cigna-leaving-aca-marketplace-2027', '/blog/' + SLUG)
# related guides
rg = '''<section class="vs-related-guides" data-block="%s">
  <div class="vs-rg-inner">
    <h2>Replacing your State Farm agent coverage? Start here</h2>
    <p class="vs-rg-sub">Want an advisor to compare it for you? <a href="%s" style="color:#16447f;font-weight:700">Compare my options &rarr;</a></p>
    <div class="vs-rg-grid">
        <a class="vs-rg-card" href="/private-health-insurance"><strong>Private PPO Plans for High Earners</strong><span>Over the subsidy limit? Nationwide PPO options priced on age and health.</span><em>Read the guide &rarr;</em></a>
        <a class="vs-rg-card" href="/self-employed-health-insurance"><strong>Self-Employed Health Insurance</strong><span>How net income sets your price, and the plans that fit business owners.</span><em>Read the guide &rarr;</em></a>
        <a class="vs-rg-card" href="/small-business-health-insurance"><strong>Group Coverage for Your Agency</strong><span>Small group plans, ICHRA and QSEHRA for agencies with W-2 team members.</span><em>Read the guide &rarr;</em></a>
    </div>
  </div>
</section>''' % (SLUG, QUOTE)
s, k = re.subn(r'<section class="vs-related-guides".*?</section>', lambda m: rg, s, count=1, flags=re.S)
assert k == 1
leftover = [w for w in ['Cigna', 'cigna'] if w in s]
open('blog/' + SLUG + '.html', 'w', encoding='utf-8').write(s)
print('written', len(s), 'leftover cigna mentions:', s.count('Cigna') + s.count('cigna'))
for m in re.finditer(r'.{60}[Cc]igna.{60}', s): print('  ', m.group(0).replace('\n', ' '))

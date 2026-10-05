# -*- coding: utf-8 -*-
"""Two Open Enrollment 2027 tools, 4 October 2026.

  /health-insurance-premium-increase-calculator   renewal letter vs what a benchmark plan should cost
  /owner-operator-subsidy-cliff-calculator        net profit -> MAGI -> 400% line -> contribution needed

Shell (GA head, styles, nav, footer, chat + conversion scripts) comes from the
same donor the other tools use, via build_tools_2026.shell(). Math matches the
site's other calculators: FPL 15,960 + 5,680 (2026 guidelines for 2027
coverage), Rev. Proc. 2026-26 contribution scale, BASE21 = 375 benchmark
estimate with the federal age curve.
"""
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_tools_2026 import shell, WIZ_CSS, SITE

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EXTRA_CSS = """
.tool-hero .center{text-align:center}
.calc-grid{display:grid;grid-template-columns:1fr;gap:0 14px}
@media(min-width:560px){.calc-grid{grid-template-columns:1fr 1fr}}
.calc-go{width:100%;background:var(--blue-700);color:#fff;border:0;border-radius:999px;font-family:inherit;font-weight:700;font-size:1rem;padding:15px 22px;cursor:pointer;min-height:52px;margin-top:6px}
.calc-go:hover{background:var(--blue-600)}
#result{margin-top:24px;display:none}
#result.show{display:block;animation:wfade .28s ease}
.res-cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.res-cta a{flex:1 1 200px;text-align:center;border-radius:999px;padding:14px 18px;font-weight:700;text-decoration:none;min-height:var(--tap)}
.res-cta .p{background:var(--teal);color:#fff}
.res-cta .s{background:#fff;color:var(--blue-700);border:1.5px solid var(--blue-700)}
.guide{max-width:820px;margin:0 auto}
.guide h2{margin:30px 0 10px}
.guide p,.guide li{color:var(--ink-2);line-height:1.7}
.guide ul{padding-left:20px;margin:0 0 14px}
.guide a{color:var(--blue-700);font-weight:600}
"""

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
%(head_open)s<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>%(title)s</title>
<meta name="description" content="%(desc)s" />
<meta name="keywords" content="%(kw)s" />
<link rel="canonical" href="%(site)s/%(slug)s" />
<meta name="robots" content="index,follow" />
<meta property="og:type" content="website" />
<meta property="og:title" content="%(title)s" />
<meta property="og:description" content="%(desc)s" />
<meta property="og:url" content="%(site)s/%(slug)s" />
<meta property="og:site_name" content="VS Health Benefits" />
<meta property="og:image" content="%(site)s/images/og-default.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="%(title)s" />
<meta name="twitter:description" content="%(desc)s" />
<meta name="twitter:image" content="%(site)s/images/og-default.jpg" />
<link rel="icon" type="image/png" href="/favicon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet" />
<script type="application/ld+json">
%(appjson)s
</script>
<script type="application/ld+json">
%(faqjson)s
</script>
<script type="application/ld+json">
%(crumbjson)s
</script>
<style>
%(style)s
%(wizcss)s
%(extracss)s
</style>
</head>
<body>
<div id="sb"></div>
%(header)s
<main>
  <section class="tool-hero">
    <div class="container center">
      <span class="eyebrow" style="background:rgba(255,255,255,.15);color:#fff">%(eyebrow)s</span>
      <h1>%(h1)s</h1>
      <p class="lede">%(lede)s</p>
      <div class="trust">%(trust)s</div>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="container">
      <div class="wiz">
%(form)s
        <button type="button" class="calc-go" id="go">%(gobtn)s</button>
        <p class="wfine">Estimates only, for 2027 coverage. Benchmark prices are a national average by age; your ZIP code changes them. Uses 2026 HHS poverty guidelines and the IRS 2027 contribution scale. Not tax advice.</p>
        <div id="result" aria-live="polite"></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container guide">
%(guide)s
    </div>
  </section>

  <section class="section bg-soft">
    <div class="container" style="max-width:820px">
      <h2 class="center" style="margin-bottom:24px">%(faqh)s</h2>
%(faqhtml)s
    </div>
  </section>

  <section class="section">
    <div class="container" style="max-width:820px">
      <div class="cta-strip">
        <h2>%(ctah)s</h2>
        <p>%(ctap)s</p>
        <a class="btn btn-white" href="/quote?type=individual" style="background:#fff;color:var(--blue-700)">Get my free 2027 quote</a>
      </div>
      <p class="center" style="margin-top:26px;font-size:.86rem;color:var(--muted)">%(related)s</p>
    </div>
  </section>
</main>
%(footer)s

<script>
(function(){
  "use strict";
  var FPL_BASE=15960,FPL_ADD=5680; // 2026 HHS guidelines, used for 2027 coverage
  function fpl(n){return FPL_BASE+(n-1)*FPL_ADD;}
  function lerp(x,x0,x1,y0,y1){return y0+(y1-y0)*(x-x0)/(x1-x0);}
  // 2027 required-contribution scale (IRS Rev. Proc. 2026-26). null above 400%% FPL = no credit.
  function applicablePct(p){if(p<133)return 2.15;if(p<150)return lerp(p,133,150,3.23,4.30);if(p<200)return lerp(p,150,200,4.30,6.78);if(p<250)return lerp(p,200,250,6.78,8.66);if(p<300)return lerp(p,250,300,8.66,10.22);if(p<=400)return 10.22;return null;}
  function ageFactor(a){if(a<21)return 0.765;if(a>=64)return 3.0;var p=[[21,1.0],[25,1.004],[30,1.135],[35,1.222],[40,1.278],[45,1.444],[50,1.786],[55,2.230],[60,2.714],[64,3.0]];for(var i=0;i<p.length-1;i++){if(a>=p[i][0]&&a<p[i+1][0])return lerp(a,p[i][0],p[i+1][0],p[i][1],p[i+1][1]);}return 1.0;}
  var BASE21=375;
  function prem(a){return BASE21*ageFactor(a);}
  function bench(a1,a2,kids){return prem(a1)+((a2>=18)?prem(Math.min(a2,64)):0)+Math.min(kids,3)*BASE21*0.765;}
  function num(id){var el=document.getElementById(id);if(!el)return 0;var v=parseFloat(String(el.value||"").replace(/[^0-9.]/g,""));return isFinite(v)?v:0;}
  function money(n){return (n<0?"-$":"$")+Math.round(Math.abs(n)).toLocaleString();}
  function row(k,v,hl){return '<div'+(hl?' class="hl"':'')+'><span>'+k+'</span><b>'+v+'</b></div>';}
  function track(name){try{if(window.gtag)gtag("event",name,{tool:%(toollabel)s});}catch(e){}}
  var CTA='<div class="res-cta"><a class="p" href="/quote?type=individual">Get my real 2027 quote</a><a class="s" href="tel:+19548251009">Call (954) 825-1009</a></div>';
%(logic)s
  document.getElementById("go").addEventListener("click",function(){
    var html=run(); var r=document.getElementById("result");
    r.innerHTML=html+CTA; r.className="show"; track("tool_result");
    try{r.scrollIntoView({behavior:"smooth",block:"start"});}catch(e){}
  });
})();
</script>
%(tail)s
"""


def jstr(s):
    return json.dumps(s, ensure_ascii=False)


def field(id_, label, ph="", hint="", kind="text", opts=None, val=""):
    if opts:
        o = "".join('<option value="%s"%s>%s</option>' % (v, ' selected' if v == val else '', t) for v, t in opts)
        inp = '<select id="%s">%s</select>' % (id_, o)
    else:
        inp = ('<input type="text" inputmode="decimal" id="%s" placeholder="%s" value="%s" autocomplete="off" />'
               % (id_, ph, val))
    h = '<div class="hint">%s</div>' % hint if hint else ''
    return '<div class="wf"><label for="%s">%s</label>%s%s</div>' % (id_, label, inp, h)


HH = [(str(i), str(i) + (" person" if i == 1 else " people")) for i in range(1, 9)]
KIDS = [("0", "None"), ("1", "1"), ("2", "2"), ("3", "3 or more")]


def build(cfg):
    head_open, style, header, footer, tail = shell()
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": cfg["appname"],
           "url": SITE + "/" + cfg["slug"], "applicationCategory": "FinanceApplication", "operatingSystem": "All",
           "browserRequirements": "Requires JavaScript",
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "description": cfg["desc"],
           "provider": {"@type": "InsuranceAgency", "name": "VS Health Benefits", "url": "https://vshealthbenefits.com/"}}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in cfg["faq"]]}
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": cfg["crumb2"][0], "item": SITE + cfg["crumb2"][1]},
        {"@type": "ListItem", "position": 3, "name": cfg["appname"], "item": SITE + "/" + cfg["slug"]}]}
    faqhtml = "\n".join('      <details class="fi"><summary>%s</summary><p>%s</p></details>' % (q, a)
                        for q, a in cfg["faq"])
    html = PAGE % dict(
        head_open=head_open, style=style, wizcss=WIZ_CSS, extracss=EXTRA_CSS, header=header, footer=footer,
        tail=tail, site=SITE, title=cfg["title"], desc=cfg["desc"], kw=cfg["kw"], slug=cfg["slug"],
        appjson=json.dumps(app, ensure_ascii=False), faqjson=json.dumps(faq, ensure_ascii=False, indent=1),
        crumbjson=json.dumps(crumb, ensure_ascii=False), eyebrow=cfg["eyebrow"], h1=cfg["h1"], lede=cfg["lede"],
        trust=cfg["trust"], form=cfg["form"], gobtn=cfg["gobtn"], guide=cfg["guide"], faqh=cfg["faqh"],
        faqhtml=faqhtml, ctah=cfg["ctah"], ctap=cfg["ctap"], related=cfg["related"],
        toollabel=jstr(cfg["toollabel"]), logic=cfg["logic"])
    io.open(cfg["slug"] + ".html", "w", encoding="utf-8").write(html)
    print("wrote %s.html (%d bytes)" % (cfg["slug"], len(html.encode("utf-8"))))


TRUST = ('<span>Free, no email</span><span>2027 subsidy rules</span><span>Licensed advisors</span>')

# =========================================================================== #
# 1. Premium increase calculator
# =========================================================================== #
PI_FORM = '''        <div class="wiz-steplabel">Your renewal letter</div>
        <div class="calc-grid">
          %s
          %s
        </div>
        <div class="wiz-steplabel" style="margin-top:8px">Your household for 2027</div>
        <div class="calc-grid">
          %s
          %s
          %s
          %s
          %s
        </div>''' % (
    field("cur", "What you pay now (per month)", "e.g. 310", "After your tax credit, from your 2026 bill"),
    field("ren", "What your 2027 notice says (per month)", "e.g. 455", "After the estimated credit on your renewal letter"),
    field("inc", "Expected 2027 household income", "e.g. 58,000", "Net profit if self-employed. <a href=\\\"/blog/what-income-counts-for-aca-subsidies\\\">What counts</a>"),
    field("hh", "Household size (tax household)", opts=HH, val="1"),
    field("a1", "Age of oldest adult", "e.g. 45"),
    field("a2", "Age of spouse or partner (if covered)", "leave blank if none"),
    field("kids", "Children under 21 on the plan", opts=KIDS, val="0"))

PI_LOGIC = r'''
  function run(){
    var cur=num("cur"),ren=num("ren"),inc=num("inc"),hh=parseInt(document.getElementById("hh").value,10)||1;
    var a1=num("a1")||40,a2=num("a2"),kids=parseInt(document.getElementById("kids").value,10)||0;
    if(!ren||!inc){return '<div class="vcard warn"><span class="vtag">Need two numbers</span><h3>Add your 2027 renewal premium and your expected income.</h3><p>Both are on your renewal letter and your tax return. A rough income estimate is fine.</p></div>';}
    var line=fpl(hh), p=inc/line*100, b=bench(a1,a2,kids);
    var diff=ren-cur, pct=cur>0?diff/cur*100:null;
    var out='<div class="bigres"><small>Your 2027 increase</small><b>'+(diff>=0?"+":"")+money(diff)+'/mo</b><span>'+(pct!==null?(pct>=0?"+":"")+pct.toFixed(0)+'% &middot; ':'')+(diff>=0?"+":"")+money(diff*12)+' a year</span></div>';
    var rows=row("Your income as % of the poverty level",Math.round(p)+"%")+row("400% line for your household",money(4*line))+row("Estimated full price, benchmark silver",money(b)+"/mo");
    var ap=applicablePct(p), verdict="";
    if(p<100){
      verdict='<div class="vcard warn"><span class="vtag">Below 100% of the poverty level</span><h3>You may qualify for Medicaid, or for a low-cost catastrophic plan.</h3><p>In states that expanded Medicaid, adults under 138% usually qualify. In Florida and other non-expansion states, adults under 100% usually get neither Medicaid nor a credit, but can request a hardship exemption to buy a catastrophic plan. Double-check your income estimate too: if it will be over 100%, you may get a large credit.</p></div>';
    } else if(ap===null){
      var over=inc-4*line, capLine=0.1022*4*line/12, worth=Math.max(0,b-capLine);
      verdict='<div class="vcard no"><span class="vtag">Over the 400% subsidy cliff</span><h3>You are about '+money(over)+' over the line, so no credit applies in 2027.</h3>'+
        (worth>0?'<p>If you got just under it, a benchmark silver plan would cost you about <b>'+money(capLine)+'/mo</b> instead of about '+money(b)+'. That is roughly <b>'+money(worth*12)+' a year</b> in credit.</p>':'<p>At your ages, the credit just under the line would be small, so focus on the lowest-cost plan that fits.</p>')+
        '<p>Pre-tax 401(k), IRA, SEP or HSA contributions lower the income the subsidy uses. Over 250% of the poverty level you can also request a catastrophic plan. <a href="/blog/how-to-lower-health-insurance-premiums-2027">11 ways to lower it</a>.</p></div>';
      rows+=row("Over the cliff by",money(over),true);
    } else {
      var cap=ap/100*inc/12, credit=Math.max(0,b-cap), net=Math.min(b,cap);
      rows+=row("Your expected share for benchmark silver",ap.toFixed(2)+"% of income")+row("Benchmark silver after credit (est.)",money(net)+"/mo",true)+row("Estimated tax credit",money(credit)+"/mo");
      if(ren>net*1.1+15){
        verdict='<div class="vcard warn"><span class="vtag">Worth shopping</span><h3>Your renewal is about '+money(ren-net)+'/mo above a benchmark silver plan at your income.</h3><p>That is about <b>'+money((ren-net)*12)+' a year</b>. Your plan may simply be richer than silver, but often it means the benchmark moved and a similar plan now costs less. Compare before December 15.</p>'+(p<250?'<p>At your income, silver plans also come with extra savings that lower the deductible.</p>':'')+'</div>';
      } else {
        verdict='<div class="vcard good"><span class="vtag">In line</span><h3>Your renewal is close to what a benchmark plan should cost at your income.</h3><p>Still worth a look: bronze plans with your credit are often cheaper, and networks and drug lists change every January.'+(p<250?' At your income, silver plans come with extra savings that lower the deductible.':'')+'</p></div>';
      }
      if(4*line-inc<6000){rows+=row("Room before the 400% cliff",money(4*line-inc),true);}
    }
    return verdict+'<div class="rlist">'+rows+'</div><div class="wnote"><b>Why the number moves:</b> your credit is tied to the second-lowest-cost silver plan in your ZIP, and that plan changes every year. A real quote uses your ZIP, exact ages and every plan available.</div>';
  }
'''

PI_GUIDE = '''<h2>Why your 2027 renewal went up</h2>
      <p>Insurers asked for a median 15% rate increase for 2027 nationally, after a 26% benchmark jump in 2026, and the enhanced premium tax credits expired at the end of 2025. Your net premium is the plan's price minus your credit, and the credit is pegged to the second-lowest-cost silver plan in your area. If that benchmark got cheaper relative to your plan, you pay more even if your plan's price barely moved.</p>
      <h2>How to use your result</h2>
      <ul>
        <li><b>Worth shopping:</b> your renewal is well above what a benchmark plan should cost at your income. Compare plans before December 15. <a href="/blog/health-insurance-renewal-notice-2027">The six things to check</a>.</li>
        <li><b>Over the cliff:</b> you are above 400% of the poverty level. See how retirement and HSA contributions can bring the credit back in <a href="/blog/aca-income-limits-2027">the 2027 income limits</a>.</li>
        <li><b>In line:</b> your plan is priced about right, but a bronze plan with an HSA may still cost less in total. <a href="/blog/cheapest-health-insurance-2027">Cheapest options for 2027</a>.</li>
      </ul>
      <p>Open Enrollment runs November 1, 2026 to January 15, 2027. Choose by December 15 for January 1 coverage.</p>'''

PI_FAQ = [
 ("How much are health insurance premiums going up in 2027?",
  "Insurers proposed a median increase of 15% for 2027 across 276 insurers nationwide, with requests ranging from a "
  "small decrease to more than 50%. In Florida, filed requests ranged from about 4% to about 39%. What you pay also "
  "depends on your premium tax credit, which changes with your income and your area's benchmark plan."),
 ("Why did my Marketplace premium go up more than the rate increase?",
  "Because your net premium depends on your credit as well as the price. The credit is based on the second-lowest-cost "
  "silver plan in your area. If that plan's price rose less than yours, or a cheaper plan became the benchmark, your "
  "credit covers less of your plan. Losing the enhanced credits that expired in 2025 raised net premiums for most people "
  "too."),
 ("Is this calculator accurate for my ZIP code?",
  "It is an estimate. Benchmark prices here are a national average adjusted for age; actual prices vary a lot by ZIP "
  "code and state. Use it to see whether your renewal looks high, then get a quote with your exact ZIP and ages."),
 ("What should I do if my renewal is too high?",
  "Update your 2027 income estimate, then compare plans at the same metal level and one level down before December 15. "
  "If you are near the 400% cliff, pre-tax retirement or HSA contributions can bring your credit back. A licensed broker "
  "can do this comparison for free."),
]

PI = dict(
    slug="health-insurance-premium-increase-calculator",
    title="2027 Health Insurance Premium Increase Calculator",
    desc="Enter your 2026 premium and your 2027 renewal. See your increase, what a benchmark plan should cost at your income, and whether you are overpaying. Free.",
    kw="health insurance premium increase 2027, health insurance renewal calculator, marketplace premium increase calculator, why did my health insurance go up 2027, aca premium 2027, obamacare renewal 2027",
    appname="2027 Premium Increase Calculator", crumb2=("Open Enrollment", "/open-enrollment"),
    eyebrow="Open Enrollment 2027 tool", h1="Did Your Health Insurance Go Up? 2027 Premium Increase Calculator",
    lede="Put in your current premium and the number on your renewal letter. See how big the jump is and whether you are paying more than you should at your income.",
    trust=TRUST, form=PI_FORM, gobtn="Check my renewal", guide=PI_GUIDE, faqh="Premium increase questions",
    faq=PI_FAQ, ctah="Want a real comparison?",
    ctap="Send us your renewal letter. We check it against every plan in your ZIP, free, and the premium is the same as buying direct.",
    related='Also useful: <a href="/aca-subsidy-calculator">ACA subsidy calculator</a> &middot; <a href="/blog/how-to-lower-health-insurance-premiums-2027">How to lower your premium</a> &middot; <a href="/blog/losing-health-insurance-2027">Losing coverage in 2027</a>',
    toollabel="premium_increase_2027", logic=PI_LOGIC)

# =========================================================================== #
# 2. Owner-operator subsidy cliff calculator
# =========================================================================== #
OO_FORM = '''        <div class="wiz-steplabel">Your trucking business</div>
        <div class="calc-grid">
          %s
          %s
        </div>
        <div class="wiz-steplabel" style="margin-top:8px">Your household for 2027</div>
        <div class="calc-grid">
          %s
          %s
          %s
          %s
          %s
        </div>''' % (
    field("profit", "Expected 2027 net profit (Schedule C)", "e.g. 72,000", "After fuel, maintenance, truck payment, insurance and per diem, not gross settlements"),
    field("planned", "Retirement contributions already planned", "0", "Solo 401(k), SEP-IRA or HSA, if any"),
    field("other", "Other household income", "0", "Spouse's wages, other jobs, interest"),
    field("hh", "Household size (tax household)", opts=HH, val="1"),
    field("a1", "Your age", "e.g. 48"),
    field("a2", "Spouse's age (if on the plan)", "leave blank if none"),
    field("kids", "Children under 21 on the plan", opts=KIDS, val="0"))

OO_LOGIC = r'''
  var SS_BASE=184500; // 2026 Social Security wage base
  function halfSE(profit){var ne=Math.max(0,profit)*0.9235;return (Math.min(ne,SS_BASE)*0.124+ne*0.029)/2;}
  function run(){
    var profit=num("profit"),planned=num("planned"),other=num("other"),hh=parseInt(document.getElementById("hh").value,10)||1;
    var a1=num("a1")||45,a2=num("a2"),kids=parseInt(document.getElementById("kids").value,10)||0;
    if(!profit){return '<div class="vcard warn"><span class="vtag">Need your net profit</span><h3>Add your expected 2027 net profit.</h3><p>Use your last Schedule C line 31, or settlements minus expenses so far this year. Not gross.</p></div>';}
    var hse=halfSE(profit), magi=Math.max(0,profit-hse+other-planned), line=4*fpl(hh), p=magi/fpl(hh)*100, b=bench(a1,a2,kids);
    var rows=row("Net profit",money(profit))+row("Less half of self-employment tax","&minus;"+money(hse))+(other?row("Plus other household income",money(other)):"")+(planned?row("Less planned contributions","&minus;"+money(planned)):"")+row("Your MAGI for the subsidy",money(magi),true)+row("400% line for a household of "+hh,money(line));
    var capLine=0.1022*line/12, worthAtLine=Math.max(0,b-capLine)*12;
    var catch1=(a1>=60&&a1<=63)?11250:(a1>=50?8000:0);
    var earned=Math.max(0,profit-hse);
    var soloEmp=Math.min(24500+catch1,earned), soloEr=Math.min(0.2*earned,72000-24500), solo=Math.min(soloEmp+soloEr,72000+catch1,earned);
    var sep=Math.min(0.2*earned,72000), hsa=((a2>=18||kids>0)?9000:4500)+(a1>=55?1000:0);
    var verdict;
    if(p<100){
      verdict='<div class="vcard warn"><span class="vtag">Under 100% of the poverty level</span><h3>Your MAGI is below the range where a credit applies.</h3><p>In states that expanded Medicaid you may qualify for Medicaid. In Florida and other non-expansion states, you can request a hardship exemption for a low-cost catastrophic plan. If your profit will be higher than this, re-run it: a realistic estimate over 100% usually gets a large credit.</p></div>';
    } else if(magi<=line){
      var ap=applicablePct(p), cap=ap/100*magi/12, credit=Math.max(0,b-cap), room=line-magi;
      rows+=row("Estimated tax credit",money(credit)+"/mo",true)+row("Benchmark silver after credit (est.)",money(Math.min(b,cap))+"/mo");
      verdict='<div class="vcard good"><span class="vtag">Under the cliff</span><h3>You qualify for a credit of about '+money(credit*12)+' a year.</h3><p>You have about <b>'+money(room)+'</b> of MAGI room before the 400% line, which is roughly <b>'+money(room/0.9294)+'</b> more net profit. '+(room<8000?'That is tight. If 2027 runs better than expected, a SEP-IRA contribution made before your tax deadline can pull you back under.':'Keep your estimate honest: since 2026 any excess credit is repaid in full.')+'</p></div>';
    } else {
      var gap=magi-line+100, reach=solo+hsa;
      rows+=row("Over the cliff by",money(magi-line),true)+row("Contribution needed to get under",money(gap),true);
      verdict='<div class="vcard no"><span class="vtag">Over the 400% cliff</span><h3>You need about '+money(gap)+' in pre-tax contributions to get your credit back.</h3>'+
        (worthAtLine>0?'<p>Just under the line, a benchmark silver plan would cost you about <b>'+money(capLine)+'/mo</b> instead of about '+money(b)+'. That credit is worth roughly <b>'+money(worthAtLine)+' a year</b>, and the contribution stays in your own account.</p>':'<p>At your ages the credit right under the line would be small, so the cheapest plan that fits may matter more than the cliff.</p>')+
        (gap<=reach?'<p><b>This looks reachable.</b> Your rough maximums: Solo 401(k) about '+money(solo)+', SEP-IRA about '+money(sep)+', HSA '+money(hsa)+' (with a bronze or HSA-eligible plan).</p>':'<p>The gap is larger than typical contribution limits (Solo 401(k) about '+money(solo)+' plus HSA '+money(hsa)+'). Compare bronze, catastrophic and PPO plans at full price instead.</p>')+'</div>';
    }
    return verdict+'<div class="rlist">'+rows+'</div><div class="wnote"><b>Notes:</b> Retirement limits shown are 2026 figures (the IRS announces 2027 limits late in the year). Solo 401(k) deferrals must be elected by December 31; SEP-IRA contributions can be made up to your filing deadline. The self-employed health insurance deduction lowers MAGI further and is not included here, so your real number is likely a little lower. Have your tax preparer confirm before contributing.</div>';
  }
'''

OO_GUIDE = '''<h2>Why the cliff matters so much for owner-operators</h2>
      <p>For 2027 coverage there is no premium tax credit once household income passes 400% of the federal poverty level: about $63,840 for a single driver, $86,560 for a couple and $132,000 for a family of four. Owner-operator income swings with rates and miles, so a good year can push a driver a few hundred dollars over the line and cost thousands in credit.</p>
      <p>The subsidy uses modified adjusted gross income, not gross settlements. For a sole proprietor, that starts with Schedule C net profit, minus half of self-employment tax, the self-employed health insurance deduction and pre-tax retirement and HSA contributions.</p>
      <h2>Three ways drivers get back under the line</h2>
      <ul>
        <li><b>Solo 401(k):</b> up to $24,500 as an employee deferral for 2026, plus catch-up from age 50, plus an employer contribution. Best for drivers with no employees.</li>
        <li><b>SEP-IRA:</b> roughly 20% of net self-employment earnings, and it can be funded up to your tax deadline, after you know what the year actually netted.</li>
        <li><b>HSA with a bronze plan:</b> since 2026 every bronze plan is HSA-compatible. For 2027, $4,500 single or $9,000 family, plus $1,000 at 55.</li>
      </ul>
      <p>More detail: <a href="/blog/owner-operator-health-insurance-increase-2027">8 ways owner-operators cut the 2027 cost</a> &middot; <a href="/blog/owner-operator-health-insurance-no-subsidy">over the cliff with no subsidy</a> &middot; <a href="/can-truckers-deduct-health-insurance">deducting your premiums</a>.</p>'''

OO_FAQ = [
 ("What is the subsidy cliff for truck drivers in 2027?",
  "For 2027 coverage, premium tax credits stop at 400% of the federal poverty level: about $63,840 of MAGI for a "
  "household of one, $86,560 for two and $132,000 for four. Above that line there is no credit at all, so an "
  "owner-operator a few hundred dollars over can pay the full premium."),
 ("Does the subsidy use my gross settlements?",
  "No. It uses modified adjusted gross income. For an owner-operator filing Schedule C, that starts with net profit after "
  "business expenses, then subtracts half of self-employment tax and other above-the-line deductions such as retirement "
  "contributions and the self-employed health insurance deduction."),
 ("How much do I need to put in a Solo 401(k) to get under the cliff?",
  "Enough to bring your MAGI below the 400% line for your household size. The calculator estimates that amount from your "
  "net profit. For 2026, the Solo 401(k) employee deferral limit is $24,500, plus catch-up from age 50, and total "
  "contributions can reach $72,000. The IRS publishes 2027 limits late in the year."),
 ("Can I wait until tax time to fix it?",
  "Partly. SEP-IRA contributions can be made up to your tax filing deadline, including extensions, and count for the "
  "prior year. Solo 401(k) employee deferrals have to be elected by December 31. HSA contributions for a year can be made "
  "until the tax deadline too."),
 ("Is this calculator tax advice?",
  "No. It is an estimate to show where you stand. Self-employment tax, deductions and contribution limits depend on your "
  "full return, so confirm with your tax preparer before contributing."),
]

OO = dict(
    slug="owner-operator-subsidy-cliff-calculator",
    title="Owner-Operator Subsidy Cliff Calculator (2027)",
    desc="Truck drivers: enter your net profit and see if you are over the 2027 ACA subsidy cliff, and how much a Solo 401(k), SEP or HSA contribution gets your credit back.",
    kw="owner operator subsidy cliff calculator, truck driver aca subsidy calculator, owner operator health insurance subsidy 2027, solo 401k aca subsidy, self employed aca subsidy cliff, 400% fpl 2027 calculator",
    appname="Owner-Operator Subsidy Cliff Calculator", crumb2=("Truck Driver Health Insurance", "/truck-driver-health-insurance"),
    eyebrow="Truck driver tool", h1="Owner-Operator Subsidy Cliff Calculator for 2027",
    lede="A good year can cost a driver the whole health insurance credit. Enter your net profit to see how close you are to the 400% line, and what it takes to get back under it.",
    trust='<span>Free, no email</span><span>Built for owner-operators</span><span>2027 subsidy rules</span>',
    form=OO_FORM, gobtn="Check my cliff", guide=OO_GUIDE, faqh="Subsidy cliff questions for drivers", faq=OO_FAQ,
    ctah="Close to the line?",
    ctap="We run your subsidy from net profit, price PPOs that work on the road, and enroll you by phone from the cab. Free.",
    related='Also for drivers: <a href="/truck-driver-health-insurance-cost-calculator">Driver cost calculator</a> &middot; <a href="/truck-driver-open-enrollment-2027">Open Enrollment 2027 for drivers</a> &middot; <a href="/owner-operator-plan-finder">Plan finder</a>',
    toollabel="oo_subsidy_cliff", logic=OO_LOGIC)

if __name__ == "__main__":
    build(PI)
    build(OO)

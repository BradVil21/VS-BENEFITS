import re, json, os, sys, html
ROOT = os.path.expanduser("~/mnt/VS-BENEFITS")
sys.path.insert(0, os.path.join(ROOT, "_build"))
from build_pages import one, sub1, GENERAL_BAR

T = open(os.path.join(ROOT, "small-business-renewal-review.html"), encoding="utf-8").read()
SLUG = "premium-increase-review"
URL = "https://www.vshealthbenefits.com/" + SLUG
TITLE = "2027 Health Insurance Went Up? Free Premium Review"
DESC = "Florida Marketplace rates rose about 10% for 2027. Send us your old and new premium and a licensed advisor checks every plan and tax credit for your ZIP. Free."
OT = "2027 Group Health Renewal Went Up? Free Renewal Review"
OD = "Small group health renewals are coming in 8% to 15%+ higher for 2027. Send us your renewal and a licensed advisor will shop it against other carriers, level-funded and ICHRA options before you sign. Free."

FAQ = [
("Why did my health insurance go up for 2027?", "Insurers raised prices again, about 10.4% on average in Florida and a 15% median request nationally, driven by hospital and drug costs and a sicker risk pool after the enhanced tax credits expired. Your own increase also depends on how much your tax credit changed, your age, your income estimate and whether your plan was discontinued."),
("Is the premium on my renewal letter final?", "No. During Open Enrollment, November 1, 2026 to January 15, 2027, you can switch to any plan in your area and update your income. Choose by December 15 for a January 1 start. If you do nothing, you are auto-renewed at the new price."),
("What do you need from me for the review?", "Your ZIP code, who needs coverage, what you paid each month in 2026 and what the 2027 renewal says. A photo of the renewal letter helps but is not required. An advisor will also ask about your expected 2027 income, your doctors and your prescriptions."),
("My insurer is leaving. Can you help?", "Yes. For 2027 in Florida, Cigna is leaving the Marketplace and Sunshine State Health Plan's Marketplace products end, with members who do not choose a plan moved to Ambetter. We compare replacement plans and check your doctors before you are placed in one automatically."),
("Does the review cost anything?", "No. Insurance carriers pay licensed brokers, and Marketplace prices are the same whether you enroll yourself or with us. If your current plan is still your best option, we will tell you."),
]

head_ld = [
 {"@context":"https://schema.org","@type":"WebPage","name":TITLE,"url":URL,"description":DESC,"dateModified":"2026-10-27","inLanguage":"en-US",
  "author":{"@type":"Person","name":"Bradley Vilsaint","jobTitle":"Licensed Health Insurance Advisor","url":"https://www.vshealthbenefits.com/bradley-vilsaint"}},
 {"@context":"https://schema.org","@type":"Service","name":"Individual and family health insurance premium increase review","serviceType":"Health insurance renewal review","areaServed":"US",
  "provider":{"@type":"InsuranceAgency","name":"VS Health Benefits","telephone":"+1-954-825-1009"},
  "offers":{"@type":"Offer","price":"0","priceCurrency":"USD","description":"Free review of a 2027 individual or family health insurance premium increase"}},
 {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Home","item":"https://www.vshealthbenefits.com/"},
  {"@type":"ListItem","position":2,"name":"Open Enrollment 2027","item":"https://www.vshealthbenefits.com/open-enrollment"},
  {"@type":"ListItem","position":3,"name":"Premium Increase Review","item":URL}]},
 {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]},
]

e = html.escape
opt = lambda vals: '<option value="">Select</option>' + "".join('<option value="%s">%s</option>' % (e(v), e(v)) for v in vals)
MAIN = r'''<main class="container" id="main">
  <section class="rr-hero">
    <div>
      <span class="rr-eyebrow">2027 renewal letters are arriving now</span>
      <h1>Your health insurance went up for 2027. Get a free second look before you auto-renew.</h1>
      <p class="rr-lede">Florida Marketplace rates rose about 10% on average for 2027, and some plans rose far more. Tell us what you paid this year and what the renewal says. A licensed advisor checks every plan and tax credit for your ZIP code and shows you what it would cost to switch, before the December 15 deadline.</p>
      <ul class="rr-checks">
        <li><strong>Free, no obligation.</strong> Carriers pay us, not you. If your renewal is still your best deal, we'll say so.</li>
        <li><strong>Marketplace, private and off-exchange plans</strong>, including PPOs for people over the subsidy cliff.</li>
        <li><strong>We check your doctors and prescriptions</strong> before recommending any change.</li>
        <li><strong>For individuals, families, self-employed and truck drivers.</strong> English y Español.</li>
      </ul>
      <a class="rr-jump" href="#review">Start my free review &darr;</a>
      <p class="rr-by">Reviewed by <a href="/bradley-vilsaint">Bradley Vilsaint</a>, licensed health insurance advisor (NPN 22116298). Updated October 27, 2026. Prefer to talk? <a href="tel:+19548251009">(954) 825-1009</a></p>
    </div>

    <div class="rr-card" id="review">
      <form id="rr-form" novalidate>
        <h2>Request a free premium review</h2>
        <p class="rr-sub">About 60 seconds. Your renewal letter helps but isn't required.</p>
        <div class="rr-row">
          <div class="rr-f"><label for="rr-first">First name</label><input id="rr-first" autocomplete="given-name" required></div>
          <div class="rr-f"><label for="rr-last">Last name</label><input id="rr-last" autocomplete="family-name" required></div>
        </div>
        <div class="rr-row">
          <div class="rr-f"><label for="rr-zip">ZIP code</label><input id="rr-zip" inputmode="numeric" maxlength="5" autocomplete="postal-code" required></div>
          <div class="rr-f"><label for="rr-who">Who needs coverage</label><select id="rr-who" required>__WHO__</select></div>
        </div>
        <div class="rr-row">
          <div class="rr-f"><label for="rr-cur">2026 premium ($/mo)</label><input id="rr-cur" inputmode="decimal" placeholder="e.g. 410" required></div>
          <div class="rr-f"><label for="rr-new">2027 renewal ($/mo)</label><input id="rr-new" inputmode="decimal" placeholder="Blank if not yet"></div>
        </div>
        <div class="rr-f"><label for="rr-cov">Current coverage</label><select id="rr-cov" required>__COV__</select></div>
        <div class="rr-f"><label for="rr-phone">Mobile phone</label><input id="rr-phone" type="tel" inputmode="tel" autocomplete="tel" required></div>
        <div class="rr-f"><label for="rr-email">Email <span style="font-weight:400;color:#5a6b80">(optional)</span></label><input id="rr-email" type="email" autocomplete="email"></div>
        <label class="rr-consent"><input type="checkbox" id="rr-consent"><span>I agree to receive calls and SMS text messages from <strong>VS BENEFITS LLC</strong> (d/b/a VS Health Benefits) at the number provided about my quote, including by automated technology. Message &amp; data rates may apply. Message frequency varies. Reply <strong>STOP</strong> to opt out or <strong>HELP</strong> for help. Consent is not a condition of purchase. <a href="/privacy#sms" target="_blank" rel="noopener">Privacy Policy</a>.</span></label>
        <button class="rr-btn" type="submit" id="rr-submit">Review my increase &rarr;</button>
        <p class="rr-msg" id="rr-msg" role="alert"></p>
        <p class="rr-fine">Estimates and comparisons are not a guarantee of price or eligibility.</p>
      </form>
      <div class="rr-ok" id="rr-ok" aria-live="polite">
        <svg width="54" height="54" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/></svg>
        <h3>Got it. Your review is started.</h3>
        <p>An advisor will reach out today during business hours. To speed things up, email a photo of your 2027 renewal letter to <a href="mailto:info@vshealthbenefits.com?subject=Premium%20increase%20review">info@vshealthbenefits.com</a> or text it to <a href="sms:+19548251009">(954) 825-1009</a>.</p>
        <p>While you wait, see what a benchmark plan should cost at your income.</p>
        <a class="rr-btn" href="/health-insurance-premium-increase-calculator">Open the 2027 calculator &rarr;</a>
      </div>
    </div>
  </section>

  <section class="rr-stats" aria-label="2027 premium numbers">
    <div class="rr-stat"><b>10.4%</b><span>Average approved 2027 rate increase for Florida Marketplace plans, before subsidies (final rates, October 2026).</span></div>
    <div class="rr-stat"><b>15%</b><span>Median increase insurers requested nationally for 2027, the second double-digit year in a row (KFF).</span></div>
    <div class="rr-stat"><b>$12,000</b><span>2027 out-of-pocket maximum for one person on a Marketplace plan, up from $10,600 in 2026.</span></div>
  </section>

  <section class="rr-sec">
    <h2>How the premium review works</h2>
    <div class="rr-steps">
      <div class="rr-step"><h3>Tell us your numbers</h3><p>What you paid in 2026, what the 2027 letter says, your ZIP and who is covered. A photo of the letter is a bonus.</p></div>
      <div class="rr-step"><h3>We shop it</h3><p>We price every Marketplace and off-exchange plan for your ZIP, recalculate your tax credit on your real 2027 income, and check your doctors and prescriptions.</p></div>
      <div class="rr-step"><h3>You decide by December 15</h3><p>Keep your plan, switch, or adjust. We enroll you by phone and confirm your January 1 start.</p></div>
    </div>
  </section>

  <section class="rr-sec">
    <h2>Seven ways people cut a 2027 increase</h2>
    <p>These are the levers we check against your renewal. Most people only need one or two of them.</p>
    <div class="rr-levers">
      <div class="rr-lever"><h3>1. Update your income</h3><p>Your credit is based on the income you expect in 2027. An old or overstated figure can cost you hundreds a month. <a href="/blog/what-income-counts-for-aca-subsidies">What income counts</a>.</p></div>
      <div class="rr-lever"><h3>2. Re-shop against the new benchmark</h3><p>The second-cheapest silver plan sets your credit. When it changes insurers, the cheapest plan for you often changes too.</p></div>
      <div class="rr-lever"><h3>3. Pair a bronze plan with an HSA</h3><p>Every bronze plan is HSA-eligible now. Contributions lower your taxes and the income your credit is based on.</p></div>
      <div class="rr-lever"><h3>4. Check if your plan was replaced</h3><p>Cigna is leaving Florida's Marketplace and Sunshine State Health Plan products end in 2026. Replacement plans are rarely the best price.</p></div>
      <div class="rr-lever"><h3>5. Over the subsidy cliff? Go off-exchange</h3><p>Above 400% of poverty ($63,840 single) there is no credit, so private and off-exchange PPOs compete on equal terms. <a href="/private-health-insurance">Private options</a>.</p></div>
      <div class="rr-lever"><h3>6. Split the household</h3><p>Kids may qualify for Florida KidCare, and spouses sometimes do better on different plans.</p></div>
      <div class="rr-lever"><h3>7. Don't trade your doctors for $50</h3><p>We check networks and drug lists first, so a lower premium doesn't turn into a surprise bill.</p></div>
    </div>
  </section>

  <section class="rr-sec">
    <h2>Key dates for 2027 coverage</h2>
    <div class="rr-tw"><table class="rr-t">
      <thead><tr><th>When</th><th>What happens</th><th>What to do</th></tr></thead>
      <tbody>
        <tr><td>October</td><td>Renewal letters with 2027 prices arrive.</td><td>Send us the numbers as soon as yours arrives.</td></tr>
        <tr><td>November 1, 2026</td><td>Open Enrollment opens on HealthCare.gov.</td><td>Plans can be compared and changed.</td></tr>
        <tr><td>December 15, 2026</td><td>Last day to choose a plan that starts January 1.</td><td>Have your decision made.</td></tr>
        <tr><td>January 15, 2027</td><td>Open Enrollment closes. Plans chosen after Dec 15 start February 1.</td><td>Last chance without a qualifying event.</td></tr>
      </tbody>
    </table></div>
  </section>

  <section class="rr-sec">
    <h2>Premium reviews for</h2>
    <div class="rr-ind">
      <a href="/truck-driver-health-insurance">Truck drivers</a>
      <a href="/best-health-insurance-owner-operators">Owner-operators</a>
      <a href="/1099-health-insurance">Self-employed &amp; 1099</a>
      <a href="/family-health-insurance">Families</a>
      <a href="/health-insurance-before-medicare">Early retirees (50-64)</a>
      <a href="/health-insurance-uber-drivers">Rideshare drivers</a>
      <a href="/seguro-de-salud-miami">En español</a>
      <a href="/small-business-renewal-review">Small business group plans</a>
    </div>
  </section>

  <section class="rr-sec rr-faq">
    <h2>Premium increase questions</h2>
    __FAQ__
  </section>

  <section class="rr-cta">
    <h2>Don't auto-renew a price increase.</h2>
    <p>A review is free and usually takes one phone call.</p>
    <a href="#review">Start my premium review</a>
    <a href="tel:+19548251009">Call (954) 825-1009</a>
  </section>

  <p class="rr-src">Sources: <a href="https://acasignups.net/rate_changes/2027/fl" rel="noopener" target="_blank">ACASignups, Florida 2027 final approved rates (updated Oct 19, 2026)</a>; <a href="https://www.healthsystemtracker.org/brief/how-much-and-why-aca-marketplace-premiums-are-going-up-in-2027/" rel="noopener" target="_blank">Peterson-KFF Health System Tracker, 2027 rate filings (Aug 3, 2026)</a>; <a href="https://www.healthinsurance.org/aca-marketplace/florida/" rel="noopener" target="_blank">healthinsurance.org, Florida 2027 Marketplace (Sep 17, 2026)</a>; CMS 2027 Notice of Benefit and Payment Parameters; 2026 HHS poverty guidelines. Your own rate depends on your plan, age, ZIP code and income.</p>
</main>'''
MAIN = (MAIN.replace("__WHO__", opt(["Just me", "Me and my spouse/partner", "Me and my kids", "My whole family", "Someone else"]))
            .replace("__COV__", opt(["Marketplace / Obamacare plan", "Private or off-exchange plan", "COBRA", "Employer plan (too expensive)", "No coverage right now", "Not sure"]))
            .replace("__FAQ__", "".join("<details><summary>%s</summary><p>%s</p></details>" % (e(q), e(a)) for q, a in FAQ)))

JS = r'''<script id="rr-js">
(function(){
  var f=document.getElementById('rr-form'); if(!f) return;
  var $=function(id){return document.getElementById(id);};
  var started=false;
  f.addEventListener('focusin',function(){ if(started) return; started=true;
    try{ window.vsTrack && window.vsTrack('quote_start',{type:'individual',form:'premium-increase-review'}); }catch(e){} });
  try{ var q=new URLSearchParams(location.search);
    if(/^\d{5}$/.test(q.get('zip')||'')) $('rr-zip').value=q.get('zip');
    if(q.get('cur')) $('rr-cur').value=String(q.get('cur')).replace(/[^\d.]/g,'');
    if(q.get('new')) $('rr-new').value=String(q.get('new')).replace(/[^\d.]/g,'');
  }catch(e){}
  function bad(id,on){ var el=$(id); if(el&&el.parentNode) el.parentNode.classList.toggle('err',!!on); }
  function money(x){ var n=parseFloat(String(x).replace(/[^\d.]/g,'')); return isFinite(n)&&n>0?n:null; }
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var v=function(id){return ($(id).value||'').trim();};
    var phone=v('rr-phone').replace(/\D/g,''); if(phone.length===11&&phone[0]==='1') phone=phone.slice(1);
    var email=v('rr-email'), zip=v('rr-zip'), cur=money(v('rr-cur')), nw=money(v('rr-new'));
    var checks=[['rr-first',v('rr-first')],['rr-last',v('rr-last')],['rr-zip',/^\d{5}$/.test(zip)],['rr-who',v('rr-who')],
      ['rr-cur',cur!==null],['rr-cov',v('rr-cov')],['rr-phone',phone.length===10],['rr-email',!email||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)]];
    var ok=true; checks.forEach(function(c){ bad(c[0],!c[1]); if(!c[1]) ok=false; });
    var msg=$('rr-msg');
    if(!ok){ msg.textContent='Please fill in the highlighted fields.'; return; }
    if(!$('rr-consent').checked){ msg.textContent='Please check the box so we can contact you about your review.'; return; }
    msg.textContent='';
    var btn=$('rr-submit'); btn.disabled=true; btn.textContent='Sending...';
    var inc = (cur&&nw) ? Math.round((nw-cur)/cur*100) : null;
    var notes='Premium increase review. Covered: '+v('rr-who')+'. Current coverage: '+v('rr-cov')+'. 2026 premium $'+cur+'/mo'+
      (nw? ', 2027 renewal $'+nw+'/mo ('+(inc>=0?'+':'')+inc+'%)' : ', 2027 renewal not received yet')+'. ZIP '+zip+'. Page '+location.pathname+location.search+'.';
    var payload={firstName:v('rr-first'),lastName:v('rr-last'),phone:phone,email:email,zip:zip,state:'',
      source:'premium-increase-review',pipeline:'individual',
      tags:['premium-increase-review','website-lead','individual-family'],notes:notes,
      smsConsent:true,consentText:'Premium increase review form TCPA consent v2026-10-27'};
    fetch('/api/lead-sync',{method:'POST',headers:{'Content-Type':'application/json'},keepalive:true,body:JSON.stringify(payload)})
      .then(function(r){ if(!r.ok) throw new Error('status '+r.status); return r.json().catch(function(){return {};}); })
      .then(function(){
        try{ window.vsTrack && window.vsTrack('generate_lead',{currency:'USD',value:0,lead_type:'premium_increase_review',increase_pct:inc}); }catch(e){}
        f.style.display='none'; $('rr-ok').style.display='block';
        $('review').scrollIntoView({behavior:'smooth',block:'start'});
      })
      .catch(function(){ btn.disabled=false; btn.textContent='Review my increase →';
        msg.innerHTML='Something went wrong. Please call <a href="tel:+19548251009">(954) 825-1009</a> or try again.'; });
  });
})();
</script>'''

s = T
s = one(s, OT, TITLE, 4)
s = one(s, OD, DESC, 4)
s = s.replace("https://www.vshealthbenefits.com/small-business-renewal-review", URL)
s = s.replace("/compressed/health-insurance-cost-2026-woman.jpg", "/compressed/woman-reading-insurance-notice.jpg")
lines = s.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith('<script type="application/ld+json">{"@context": "https://schema.org", "@type": "') and any(t in l for t in ('"WebPage"', '"Service"', '"BreadcrumbList"', '"FAQPage"'))]
assert len(idx) == 4, idx
for k, i in enumerate(idx):
    lines[i] = '<script type="application/ld+json">' + json.dumps(head_ld[k], ensure_ascii=False) + '</script>'
s = "\n".join(lines)
s = sub1(s, r'<nav class="breadcrumb" aria-label="Breadcrumb">.*?</nav>', '<nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span class="sep">›</span><a href="/open-enrollment">Open Enrollment 2027</a><span class="sep">›</span><span>Premium Increase Review</span></nav>')
s = sub1(s, r'<main class="container" id="main">.*?</main>', MAIN)
s = sub1(s, r'<script id="rr-js">.*?</script>', JS)
s = re.sub(r'<div id="oe-annc-bar".*?</div>\n?', '', s, count=1, flags=re.S)  # OE banner retired 2026-11-03
for bad in ["small-business-renewal-review\"", "Group Health Renewal Went Up", "business-quote", "ICHRA options before you sign"]:
    if bad in s and bad != "small-business-renewal-review\"": raise SystemExit("leftover " + bad)
out = os.path.join(ROOT, SLUG + ".html")
if os.path.exists(out) and "--force" not in sys.argv: raise SystemExit("exists " + out)
open(out, "w", encoding="utf-8").write(s); print("wrote", out, len(s))
print("remaining business refs:", [m for m in re.findall(r'[^\s"]*(?:small-business|business-quote)[^\s"<]*', s)][:20])

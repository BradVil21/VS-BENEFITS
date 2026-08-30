# -*- coding: utf-8 -*-
"""
Build the two small-business tools:
  /group-health-eligibility-checker
  /employer-health-insurance-cost-calculator

Both reuse the shell (head boilerplate, styles, header nav, footer, tail
scripts) from small-business-health-insurance-calculator.html so the nav,
footer, chat widget, attribution and conversion scripts stay identical.

Lead capture matches the /quote funnel:
  - Step 1 collects business name + phone + employee count. Pressing Continue
    posts to /api/lead-draft, which upserts the GHL contact AND pushes a card
    onto the admin portal board. The visitor is a New Lead before they answer
    a single tool question.
  - Field IDs reuse the biz-* names the /quote funnel uses, so
    vs-lead-system.js picks them up for its own exit-beacon capture too.
  - The final step collects first name, last name and email and posts the
    complete lead to /api/lead-sync, tagged business-lead. The server dedupes
    on phone, so the finished lead updates the SAME card the draft opened.
"""
import io, re, os

DONOR = "small-business-health-insurance-calculator.html"
SITE  = "https://www.vshealthbenefits.com"


def read(p):
    return io.open(p, encoding="utf-8").read()


def write(p, s):
    io.open(p, "w", encoding="utf-8").write(s)
    print("wrote %s (%d bytes)" % (p, len(s.encode("utf-8"))))


def shell():
    s = read(DONOR)
    head_open = s[: s.index("<meta charset")]          # GA + gtag block
    style = re.search(r"<style>([\s\S]*?)</style>", s).group(1)
    header = re.search(r"<header[\s\S]*?</header>", s).group(0)
    footer = re.search(r"<footer[\s\S]*?</footer>", s).group(0)
    # everything after the page's own <script> block: org schema, chat widget,
    # attribution + conversion scripts, GHL tracking.
    tail = s[s.rindex('<script type="application/ld+json">'):]
    return head_open, style, header, footer, tail


# ---------------------------------------------------------------- wizard CSS
WIZ_CSS = """
/* ===== TOOL WIZARD ===== */
.tool-hero{background:linear-gradient(160deg,var(--blue-900),var(--blue-700) 60%,var(--blue-600));color:#fff;padding:54px 0 46px}
.tool-hero h1{color:#fff;margin-bottom:14px}
.tool-hero .lede{color:rgba(255,255,255,.92);font-size:1.05rem;max-width:640px;margin:0 auto 18px}
.tool-hero .trust{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.tool-hero .trust span{background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:7px 14px;font-size:.79rem;font-weight:600}
.wiz{max-width:660px;margin:-34px auto 0;background:#fff;border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);padding:26px 20px 28px;position:relative;z-index:2}
@media(min-width:640px){.wiz{padding:32px 34px 34px}}
.wiz-progress{height:6px;background:var(--blue-100);border-radius:999px;overflow:hidden;margin-bottom:10px}
.wiz-bar{height:100%;width:20%;background:linear-gradient(90deg,var(--blue-600),var(--teal));border-radius:999px;transition:width .35s ease}
.wiz-steplabel{font-size:.74rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--blue-600);margin-bottom:18px}
.wstep{display:none}
.wstep.active{display:block;animation:wfade .28s ease}
@keyframes wfade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.wstep h2{font-size:clamp(1.25rem,4vw,1.6rem);margin-bottom:6px}
.wstep .wsub{color:var(--muted);font-size:.93rem;margin-bottom:20px}
.wf{margin-bottom:16px}
.wf label{display:block;font-size:.8rem;font-weight:700;color:var(--ink);margin-bottom:6px;letter-spacing:.02em}
.wf input[type=text],.wf input[type=tel],.wf input[type=email],.wf input[type=number],.wf select{
  width:100%;padding:13px 15px;border:1.5px solid var(--line);border-radius:10px;font-size:16px;
  font-family:inherit;color:var(--ink);background:#fff;min-height:var(--tap);transition:border-color .2s,box-shadow .2s}
.wf input:focus,.wf select:focus{outline:none;border-color:var(--blue-600);box-shadow:0 0 0 4px rgba(22,68,127,.10)}
.wf .hint{font-size:.76rem;color:var(--muted);margin-top:5px}
.wf .msg{display:none;font-size:.76rem;color:#b23a1d;font-weight:600;margin-top:5px}
.wf.err input,.wf.err select{border-color:#b23a1d;box-shadow:0 0 0 3px rgba(178,58,29,.08)}
.wf.err .msg{display:block}
.wrow{display:grid;grid-template-columns:1fr;gap:14px}
@media(min-width:560px){.wrow.two{grid-template-columns:1fr 1fr}}
.wseg{display:flex;flex-wrap:wrap;gap:8px}
.wseg button{flex:1 1 auto;min-width:84px;min-height:var(--tap);padding:11px 12px;border:1.5px solid var(--line);
  background:#fff;border-radius:10px;font-family:inherit;font-size:.88rem;font-weight:600;color:var(--ink-2);cursor:pointer;transition:all .18s}
.wseg button:hover{border-color:var(--blue-400,#60a5fa)}
.wseg button.on{background:var(--blue-700);border-color:var(--blue-700);color:#fff}
.wpick{display:grid;gap:9px}
.wpick button{display:flex;align-items:flex-start;gap:11px;text-align:left;width:100%;padding:14px 15px;border:1.5px solid var(--line);
  background:var(--bg-soft);border-radius:12px;font-family:inherit;font-size:.93rem;color:var(--ink);cursor:pointer;transition:all .18s;min-height:var(--tap)}
.wpick button:hover{border-color:var(--blue-500);background:#fff}
.wpick button.on{border-color:var(--blue-700);background:#fff;box-shadow:0 0 0 3px rgba(22,68,127,.09)}
.wpick b{display:block;font-weight:700;margin-bottom:2px}
.wpick small{color:var(--muted);font-size:.79rem;line-height:1.45;display:block}
.wnav{display:flex;gap:10px;margin-top:22px;align-items:center}
.wnav .wback{background:none;border:0;color:var(--muted);font-family:inherit;font-weight:600;font-size:.9rem;cursor:pointer;padding:10px 4px;min-height:var(--tap)}
.wnav .wnext{flex:1;background:var(--blue-700);color:#fff;border:0;border-radius:999px;font-family:inherit;font-weight:700;
  font-size:1rem;padding:15px 22px;cursor:pointer;min-height:52px;transition:background .2s,transform .15s}
.wnav .wnext:hover{background:var(--blue-600);transform:translateY(-1px)}
.wnav .wnext:disabled{opacity:.65;cursor:not-allowed;transform:none}
.wfine{font-size:.75rem;color:var(--muted);margin-top:12px;line-height:1.5}
.wfine a{color:var(--blue-700);font-weight:600}
/* verdict + results */
.vcard{border-radius:16px;padding:22px 20px;margin-bottom:16px;border:2px solid}
.vcard.good{background:#f0fdf9;border-color:var(--teal)}
.vcard.warn{background:#fffbeb;border-color:#e0a800}
.vcard.no{background:#fef4f1;border-color:#d97757}
.vcard .vtag{font-size:.72rem;font-weight:800;letter-spacing:.11em;text-transform:uppercase;margin-bottom:8px;display:block}
.vcard.good .vtag{color:var(--teal-dark)}.vcard.warn .vtag{color:#8a6100}.vcard.no .vtag{color:#a34a2a}
.vcard h3{font-size:clamp(1.15rem,3.6vw,1.45rem);margin-bottom:8px}
.vcard p{margin:0 0 8px;font-size:.94rem}
.vcard p:last-child{margin-bottom:0}
.vstat{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:16px 0}
.vstat div{background:var(--bg-soft);border:1px solid var(--line);border-radius:12px;padding:13px 14px}
.vstat b{display:block;font-family:'Poppins',sans-serif;font-size:1.3rem;color:var(--blue-900);line-height:1.15}
.vstat small{font-size:.73rem;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.06em}
.bigres{background:linear-gradient(135deg,var(--blue-700),var(--blue-500));color:#fff;border-radius:16px;padding:24px 20px;text-align:center;margin-bottom:14px}
.bigres small{display:block;font-size:.74rem;letter-spacing:.1em;text-transform:uppercase;opacity:.85;margin-bottom:6px}
.bigres b{font-family:'Poppins',sans-serif;font-size:clamp(2rem,8vw,2.8rem);line-height:1;display:block}
.bigres span{font-size:.9rem;opacity:.9;display:block;margin-top:6px}
.rlist{border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-bottom:16px}
.rlist div{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 15px;font-size:.92rem;border-bottom:1px solid var(--line)}
.rlist div:last-child{border-bottom:0}
.rlist div:nth-child(odd){background:var(--bg-soft)}
.rlist span{color:var(--ink-2)}
.rlist b{font-weight:700;color:var(--blue-900);white-space:nowrap}
.rlist div.hl{background:var(--blue-50)}
.rlist div.hl b{color:var(--teal-dark)}
.wnote{background:var(--bg-soft);border-left:3px solid var(--teal);border-radius:8px;padding:13px 15px;font-size:.85rem;color:var(--ink-2);margin-bottom:16px;line-height:1.55}
.wnote b{color:var(--blue-900)}
.wok{text-align:center;padding:14px 0}
.wok .tick{width:62px;height:62px;border-radius:50%;background:var(--teal);display:flex;align-items:center;justify-content:center;margin:0 auto 16px}
"""


# ---------------------------------------------------------------- shared JS
SHARED_JS = r"""
  /* ---------- validation: same rules as /quote ---------- */
  function isValidPhone(v){
    var d=String(v||'').replace(/\D/g,'');
    if(d.length===11 && d.charAt(0)==='1') d=d.slice(1);
    if(d.length!==10) return false;
    var a=d.slice(0,3), x=d.slice(3,6);
    if(a.charAt(0)==='0'||a.charAt(0)==='1') return false;
    if(x.charAt(0)==='0'||x.charAt(0)==='1') return false;
    if(/^(\d)\1{9}$/.test(d)) return false;
    if(d==='1234567890'||d==='0123456789') return false;
    if(a==='555'||x==='555') return false;
    return true;
  }
  function isValidEmail(v){
    v=String(v||'').trim(); var m=/^([^\s@]+)@([^\s@]+)$/.exec(v); if(!m) return false;
    var local=m[1], domain=m[2].toLowerCase();
    if(local.length>64) return false;
    if(/^\.|\.$|\.\./.test(local)) return false;
    if(domain.indexOf('.')===-1) return false;
    if(/^[.-]|[.-]$|\.\./.test(domain)) return false;
    var labels=domain.split('.'), tld=labels[labels.length-1];
    if(!/^[a-z]{2,}$/.test(tld)) return false;
    for(var i=0;i<labels.length;i++){ if(!/^[a-z0-9-]+$/.test(labels[i])) return false; }
    var junk=['example.com','test.com','test.test','asdf.com','aaa.com','abc.com','none.com','na.com','fake.com','no.com'];
    return junk.indexOf(domain)===-1;
  }
  var DFIX={'gmial.com':'gmail.com','gmai.com':'gmail.com','gmail.con':'gmail.com','gmail.co':'gmail.com','hotnail.com':'hotmail.com','hotmial.com':'hotmail.com','yahoo.con':'yahoo.com','yaho.com':'yahoo.com','outlok.com':'outlook.com','comcast.com':'comcast.net'};
  var TFIX={'con':'com','cmo':'com','ocm':'com','vom':'com','xom':'com','comm':'com','coom':'com','cpm':'com'};
  function suggestEmail(v){ v=String(v||'').trim().toLowerCase(); var at=v.lastIndexOf('@'); if(at<1) return null;
    var l=v.slice(0,at), d=v.slice(at+1); if(!d) return null;
    if(DFIX[d]) return l+'@'+DFIX[d];
    var p=d.split('.'), t=p[p.length-1]; if(TFIX[t]){p[p.length-1]=TFIX[t]; return l+'@'+p.join('.');} return null; }
  function err(id,on,msg){ var el=document.getElementById(id); if(!el) return;
    el.classList[on?'add':'remove']('err'); if(msg){ var m=el.querySelector('.msg'); if(m) m.textContent=msg; } }
  function val(id){ var e=document.getElementById(id); return e? String(e.value||'').trim() : ''; }
  function num(id){ var n=parseInt(val(id).replace(/\D/g,''),10); return isNaN(n)?0:n; }
  function money(n){ return '$'+Math.round(n).toLocaleString('en-US'); }
  function txt(id){ var e=document.getElementById(id); return e? e.textContent.replace(/\s+/g,' ').trim() : ''; }

  /* ---------- step engine ---------- */
  var STEP=1, MAXSTEP=TOTAL_STEPS;
  function show(n){
    STEP=n;
    for(var i=1;i<=MAXSTEP+1;i++){ var el=document.getElementById('s'+i); if(el) el.classList.remove('active'); }
    var t=document.getElementById('s'+n); if(t) t.classList.add('active');
    var bar=document.getElementById('wbar'); if(bar) bar.style.width=Math.min(100,Math.round(n/MAXSTEP*100))+'%';
    var lab=document.getElementById('wstep');
    if(lab) lab.textContent = n>MAXSTEP ? 'Done' : ('Step '+n+' of '+MAXSTEP);
    var w=document.getElementById('wiz'); if(w){ var y=w.getBoundingClientRect().top+window.pageYOffset-90; window.scrollTo({top:y,behavior:'smooth'}); }
  }
  window.wBack=function(n){ show(n); };
  window.wShow=function(n){ show(n); };

  /* ---------- PARTIAL LEAD CAPTURE ----------
     Fires the moment step 1 is cleared. /api/lead-draft upserts the GoHighLevel
     contact and pushes a card onto the admin portal board, so the business is a
     New Lead with a callable number before it answers a single tool question.
     The server dedupes on phone, so the completed submission below updates the
     SAME card instead of opening a second one. */
  var _draftSent='';
  function captureDraft(step, extraNotes){
    try{
      var phone=val('biz-contact-phone');
      if(!isValidPhone(phone)) return;
      var payload={
        consent:true, capture:'auto', optIn:false, type:'business',
        step:'Step '+step,
        phone:phone, email:'',
        firstName:val('biz-firstname'), lastName:val('biz-lastname'),
        company:val('biz-name'), state:val('biz-state'), zip:val('biz-zip'),
        source:LEAD_SOURCE+' (in progress)',
        notes:(TOOL_LABEL+'. Employees: '+(val('biz-employees')||'not given')+'.'+(extraNotes?' '+extraNotes:''))
      };
      var key=JSON.stringify(payload);
      if(key===_draftSent) return;
      _draftSent=key;
      fetch('/api/lead-draft',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify(payload),keepalive:true}).catch(function(){});
      /* if /vs-lead-system.js is ever added to these pages, this tells it the
         funnel is a business one so its own exit capture routes the same way */
      if(window.vsCaptureDraft){ try{ window.vsCaptureDraft('business', step); }catch(e){} }
    }catch(e){}
  }

  /* ---------- FULL SUBMIT ---------- */
  var fired=false;
  function fireConv(){ if(fired) return; fired=true;
    try{ if(typeof gtag==='function') gtag('event','generate_lead',{currency:'USD',value:0,lead_type:'business'}); }catch(e){} }
  function sendLead(notes){
    try{
      fetch('/api/lead-sync',{method:'POST',headers:{'Content-Type':'application/json'},keepalive:true,
        body:JSON.stringify({
          firstName:val('biz-firstname'), lastName:val('biz-lastname'),
          email:val('biz-email'), phone:val('biz-contact-phone'),
          company:val('biz-name'), zip:val('biz-zip'), state:val('biz-state'),
          type:'business', employees:val('biz-employees'),
          source:LEAD_SOURCE,
          tags:['business-lead','website-lead',LEAD_TAG],
          notes:notes
        })}).catch(function(){});
    }catch(e){}
    fireConv();
  }

  /* Exit capture: fetch(keepalive) survives the page going away, so somebody who
     answers step 1 and then abandons still lands on the board with their number. */
  function wBeacon(){ try{ captureDraft(STEP, 'Left the tool at step '+STEP+'.'); }catch(e){} }
  window.addEventListener('pagehide', wBeacon);
  document.addEventListener('visibilitychange', function(){ if(document.visibilityState==='hidden') wBeacon(); });

  /* ---------- step 1 is identical on both tools ---------- */
  window.wStep1=function(){
    var ok=true;
    var biz=val('biz-name'), ph=val('biz-contact-phone'), emp=num('biz-employees');
    err('f-bizname', !biz, 'Please enter your business name.'); if(!biz) ok=false;
    err('f-bizphone', !isValidPhone(ph), 'Please enter a valid phone number.'); if(!isValidPhone(ph)) ok=false;
    err('f-bizemp', !(emp>=1 && emp<=500), 'Enter a number between 1 and 500.'); if(!(emp>=1&&emp<=500)) ok=false;
    if(!ok) return;
    captureDraft(1);
    show(2);
  };

  /* ---------- final identity step ---------- */
  window.wFinish=function(){
    var ok=true;
    var f=val('biz-firstname'), l=val('biz-lastname'), e=val('biz-email');
    err('f-first', !f, 'Please enter your first name.'); if(!f) ok=false;
    err('f-last', !l, 'Please enter your last name.'); if(!l) ok=false;
    if(!isValidEmail(e)){ err('f-email',true,'Please enter a valid email address.'); ok=false; }
    else { var sg=suggestEmail(e); if(sg){ err('f-email',true,'Did you mean '+sg+'?'); ok=false; } else err('f-email',false); }
    if(!ok) return;
    var btn=document.getElementById('w-finish'); if(btn){ btn.disabled=true; btn.textContent='Sending...'; }
    sendLead(buildNotes());
    show(MAXSTEP+1);
  };

  /* ---------- nav + scrollbar ---------- */
  var mt=document.querySelector('.menu-toggle');
  if(mt) mt.addEventListener('click', function(){ var n=document.getElementById('nav-links'); var open=n.classList.toggle('open'); this.setAttribute('aria-expanded', open); });
  var sb=document.getElementById('sb');
  if(sb) window.addEventListener('scroll', function(){ var h=document.documentElement; var p=h.scrollTop/(h.scrollHeight-h.clientHeight)*100; sb.style.width=p+'%'; });
"""


# ---------------------------------------------------------------- step 1 markup
STEP1 = """
      <div class="wstep active" id="s1">
        <h2>%(h)s</h2>
        <p class="wsub">%(sub)s</p>
        <div class="wf" id="f-bizname">
          <label for="biz-name">Business name</label>
          <input type="text" id="biz-name" placeholder="Acme Restaurant Group LLC" autocomplete="organization" />
          <div class="msg">Please enter your business name.</div>
        </div>
        <div class="wrow two">
          <div class="wf" id="f-bizphone">
            <label for="biz-contact-phone">Best phone number</label>
            <input type="tel" id="biz-contact-phone" placeholder="(305) 555-0100" autocomplete="tel" inputmode="tel" />
            <div class="msg">Please enter a valid phone number.</div>
          </div>
          <div class="wf" id="f-bizemp">
            <label for="biz-employees">W-2 employees (not counting the owner)</label>
            <input type="number" id="biz-employees" min="1" max="500" placeholder="8" inputmode="numeric" />
            <div class="msg">Enter a number between 1 and 500.</div>
          </div>
        </div>
        <div class="wf" id="f-bizstate">
          <label for="biz-state">Business state</label>
          <select id="biz-state">
            <option value="FL" selected>Florida</option>
            <option value="TX">Texas</option><option value="GA">Georgia</option>
            <option value="NC">North Carolina</option><option value="SC">South Carolina</option>
            <option value="TN">Tennessee</option><option value="KY">Kentucky</option>
            <option value="MD">Maryland</option><option value="VA">Virginia</option>
            <option value="AL">Alabama</option><option value="OTHER">Another state</option>
          </select>
        </div>
        <div class="wnav">
          <button class="wnext" type="button" onclick="wStep1()">%(cta)s &rarr;</button>
        </div>
        <p class="wfine">No cost, no obligation. We use your number only to send your results and to have a licensed advisor follow up. See our <a href="/privacy">Privacy Policy</a>.</p>
      </div>
"""

FINAL_STEP = """
      <div class="wstep" id="s%(n)d">
        <h2>Where should we send it?</h2>
        <p class="wsub">%(sub)s</p>
        <div class="wrow two">
          <div class="wf" id="f-first"><label for="biz-firstname">First name</label>
            <input type="text" id="biz-firstname" placeholder="Jane" autocomplete="given-name" />
            <div class="msg">Please enter your first name.</div></div>
          <div class="wf" id="f-last"><label for="biz-lastname">Last name</label>
            <input type="text" id="biz-lastname" placeholder="Owner" autocomplete="family-name" />
            <div class="msg">Please enter your last name.</div></div>
        </div>
        <div class="wf" id="f-email"><label for="biz-email">Work email</label>
          <input type="email" id="biz-email" placeholder="jane@company.com" autocomplete="email" />
          <div class="msg">Please enter a valid email address.</div></div>
        <div class="wnav">
          <button class="wback" type="button" onclick="wBack(%(back)d)">&larr; Back</button>
          <button class="wnext" id="w-finish" type="button" onclick="wFinish()">%(cta)s</button>
        </div>
        <p class="wfine">By submitting you agree to our <a href="/privacy">Privacy Policy</a> and consent to be contacted by a licensed VS Health Benefits advisor. We never sell your information.</p>
      </div>

      <div class="wstep" id="s%(done)d">
        <div class="wok">
          <div class="tick"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg></div>
          <h2>You're all set</h2>
          <p class="wsub" style="margin-bottom:18px">%(donetext)s</p>
          <a class="btn btn-primary" href="/quote">Start a full group quote</a>
        </div>
      </div>
"""


# ================================================================= PAGE TEMPLATE
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
<meta name="geo.region" content="US-FL" />
<meta name="geo.placename" content="Miami" />
<meta property="og:type" content="website" />
<meta property="og:title" content="%(title)s" />
<meta property="og:description" content="%(desc)s" />
<meta property="og:url" content="%(site)s/%(slug)s" />
<meta property="og:site_name" content="VS Health Benefits" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="%(title)s" />
<meta name="twitter:description" content="%(desc)s" />
<link rel="icon" type="image/png" href="/favicon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet" />
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"%(appname)s","url":"%(site)s/%(slug)s","applicationCategory":"BusinessApplication","operatingSystem":"All","browserRequirements":"Requires JavaScript","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"description":"%(desc)s","provider":{"@type":"InsuranceAgency","name":"VS Health Benefits","url":"https://vshealthbenefits.com/"}}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%(faqjson)s]}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
{"@type":"ListItem","position":1,"name":"Home","item":"%(site)s/"},
{"@type":"ListItem","position":2,"name":"Small Business Health Insurance","item":"%(site)s/small-business-health-insurance"},
{"@type":"ListItem","position":3,"name":"%(appname)s","item":"%(site)s/%(slug)s"}]}
</script>
<style>
%(style)s
%(wizcss)s
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
      <div class="wiz" id="wiz">
        <div class="wiz-progress"><div class="wiz-bar" id="wbar"></div></div>
        <div class="wiz-steplabel" id="wstep">Step 1 of %(total)d</div>
%(steps)s
      </div>
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
        <a class="btn btn-white" href="/quote" style="background:#fff;color:var(--blue-700)">Get a group quote</a>
      </div>
      <p class="center" style="margin-top:26px;font-size:.86rem;color:var(--muted)">%(related)s</p>
    </div>
  </section>
</main>
%(footer)s

<script>
(function(){
  "use strict";
  var TOTAL_STEPS=%(total)d;
  var LEAD_SOURCE=%(leadsource)s;
  var LEAD_TAG=%(leadtag)s;
  var TOOL_LABEL=%(toollabel)s;
%(shared)s
%(logic)s
})();
</script>
%(tail)s
"""


def build(cfg, head_open, style, header, footer, tail):
    faqjson = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (jstr(q), jstr(a)) for q, a in cfg["faq"]
    )
    faqhtml = "\n".join(
        '      <details class="fi"><summary>%s</summary><p>%s</p></details>' % (q, a)
        for q, a in cfg["faq"]
    )
    html = PAGE % dict(
        head_open=head_open, style=style, wizcss=WIZ_CSS,
        header=header, footer=footer, tail=tail,
        shared=SHARED_JS, site=SITE,
        title=cfg["title"], desc=cfg["desc"], kw=cfg["kw"], slug=cfg["slug"],
        appname=cfg["appname"], eyebrow=cfg["eyebrow"], h1=cfg["h1"],
        lede=cfg["lede"], trust=cfg["trust"], total=cfg["total"],
        steps=cfg["steps"], faqjson=faqjson, faqhtml=faqhtml, faqh=cfg["faqh"],
        ctah=cfg["ctah"], ctap=cfg["ctap"], related=cfg["related"],
        leadsource=jstr(cfg["leadsource"]), leadtag=jstr(cfg["leadtag"]),
        toollabel=jstr(cfg["toollabel"]), logic=cfg["logic"],
    )
    write(cfg["slug"] + ".html", html)


def jstr(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# ================================================================= TOOL 1
ELIG_STEPS = STEP1 % dict(
    h="Let's check your group in 60 seconds",
    sub="Answer three quick questions and we'll tell you whether you can put a group health plan in place, and which route fits your headcount.",
    cta="Check my eligibility",
) + """
      <div class="wstep" id="s2">
        <h2>Who is on your payroll?</h2>
        <p class="wsub">Carriers count W-2 employees. This is the question that decides whether a group plan is even on the table.</p>
        <div class="wf">
          <label>Besides the owner, who is on W-2 payroll?</label>
          <div class="wpick" id="p-struct">
            <button type="button" data-v="employee"><span><b>At least one non-family W-2 employee</b><small>A real employee on payroll who is not the owner or the owner's spouse.</small></span></button>
            <button type="button" data-v="spouse"><span><b>Only the owner's spouse</b><small>The owner and their spouse are the only people on payroll.</small></span></button>
            <button type="button" data-v="none"><span><b>Just the owner &mdash; nobody else on W-2</b><small>You may pay contractors, but nobody receives a W-2.</small></span></button>
          </div>
          <div class="msg" style="display:none">Please choose one.</div>
        </div>
        <div class="wf" id="f-1099">
          <label for="cnt-1099">How many 1099 contractors do you pay? (optional)</label>
          <input type="number" id="cnt-1099" min="0" max="500" placeholder="0" inputmode="numeric" />
          <div class="hint">Contractors don't count toward group eligibility, but they can often be covered a different way.</div>
        </div>
        <div class="wnav">
          <button class="wback" type="button" onclick="wBack(1)">&larr; Back</button>
          <button class="wnext" type="button" onclick="wStep2()">Continue &rarr;</button>
        </div>
      </div>

      <div class="wstep" id="s3">
        <h2>How many would actually enroll?</h2>
        <p class="wsub">This is the number that trips up most small employers. Carriers require a minimum percentage to take the plan &mdash; but employees with other coverage don't count against you.</p>
        <div class="wrow two">
          <div class="wf" id="f-enroll">
            <label for="cnt-enroll">How many would sign up?</label>
            <input type="number" id="cnt-enroll" min="0" max="500" placeholder="4" inputmode="numeric" />
            <div class="msg">Enter how many employees would enroll.</div>
          </div>
          <div class="wf" id="f-waive">
            <label for="cnt-waive">How many have coverage elsewhere?</label>
            <input type="number" id="cnt-waive" min="0" max="500" placeholder="2" inputmode="numeric" />
            <div class="hint">Spouse's plan, a parent's plan, Medicare, VA or TRICARE. These are valid waivers.</div>
          </div>
        </div>
        <div class="wnote"><b>Why this matters:</b> participation is calculated on employees <em>without</em> other coverage &mdash; not on your total headcount. Employers are told "you don't have enough people" all the time when they actually do.</div>
        <div class="wnav">
          <button class="wback" type="button" onclick="wBack(2)">&larr; Back</button>
          <button class="wnext" type="button" onclick="wStep3()">See my result &rarr;</button>
        </div>
      </div>

      <div class="wstep" id="s4">
        <div id="verdict"></div>
        <div class="vstat">
          <div><b id="v-part">&mdash;</b><small>Your participation</small></div>
          <div><b id="v-need">&mdash;</b><small>Typical carrier minimum</small></div>
        </div>
        <div id="v-routes"></div>
        <div class="wnav">
          <button class="wback" type="button" onclick="wBack(3)">&larr; Back</button>
          <button class="wnext" type="button" onclick="wShow(5)">Email me this result &rarr;</button>
        </div>
        <p class="wfine">This is an estimate based on the participation and contribution rules carriers most commonly apply to small groups. Final eligibility is determined by the carrier at underwriting. VS Health Benefits sets up group coverage at no cost to the employer.</p>
      </div>
""" + FINAL_STEP % dict(
    n=5, back=4,
    sub="We'll send your eligibility summary and a licensed advisor will confirm it against the specific carriers in your state.",
    cta="Send my result",
    done=6,
    donetext="Your eligibility summary is on its way. A licensed VS Health Benefits advisor will call to confirm which carriers will write your group and what it would cost.",
)

ELIG_LOGIC = r"""
  var STRUCT='', PART=0, VERDICT='';
  document.getElementById('p-struct').addEventListener('click', function(e){
    var b=e.target.closest('button'); if(!b) return;
    this.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});
    b.classList.add('on'); STRUCT=b.getAttribute('data-v');
  });

  window.wStep2=function(){
    if(!STRUCT){ var m=document.querySelector('#s2 .wf .msg'); if(m) m.style.display='block'; return; }
    captureDraft(2, 'Payroll: '+STRUCT+'.');
    show(3);
  };

  window.wStep3=function(){
    var emp=num('biz-employees');
    var enroll=num('cnt-enroll'), waive=num('cnt-waive');
    var enrEl=document.getElementById('cnt-enroll');
    if(!enrEl || enrEl.value===''){ err('f-enroll',true,'Enter how many employees would enroll.'); return; }
    err('f-enroll',false);
    if(waive>emp) waive=emp;
    var eligible=Math.max(0, emp-waive);
    PART = eligible>0 ? (enroll/eligible) : 0;
    var pct=Math.round(PART*100);
    document.getElementById('v-part').textContent = eligible>0 ? pct+'%' : 'n/a';
    document.getElementById('v-need').textContent = '70%';

    var v=document.getElementById('verdict'), r=document.getElementById('v-routes'), html='', routes='';

    if(STRUCT==='none'){
      VERDICT='Not group-eligible (owner only)';
      html='<div class="vcard no"><span class="vtag">Not yet</span><h3>A group plan needs at least one W-2 employee besides the owner</h3>'
        +'<p>With nobody else on payroll, carriers treat you as a sole proprietor rather than a group &mdash; so small group coverage is not available. That is not the end of the road.</p></div>';
      routes='<div class="wnote"><b>What works instead:</b> an individual plan for the owner, or an ICHRA once you do have employees. If you are paying contractors, there are ways to help them get covered that do not require a group plan.</div>';
    } else if(STRUCT==='spouse'){
      VERDICT='Spouse-only group — carrier dependent';
      html='<div class="vcard warn"><span class="vtag">Depends on the carrier</span><h3>Owner + spouse groups are written by some carriers and declined by others</h3>'
        +'<p>When the only other person on payroll is the owner\'s spouse, some carriers treat the business as a group of one and decline it. Others will write it if the spouse is a bona fide W-2 employee with payroll records.</p>'
        +'<p>This is worth a five-minute call &mdash; it comes down to which carriers are writing spouse-only groups in your state this year.</p></div>';
      routes='<div class="wnote"><b>Your realistic options:</b> a small group plan with a carrier that accepts spouse-only groups, or an ICHRA, which has no participation requirement at all.</div>';
    } else if(enroll < 1){
      VERDICT='No enrollees';
      html='<div class="vcard warn"><span class="vtag">Almost</span><h3>You are structurally eligible, but nobody is enrolling</h3>'
        +'<p>You have the payroll to qualify for a group plan. With zero employees signing up there is no group to write &mdash; usually a cost problem, not an eligibility one.</p></div>';
      routes='<div class="wnote"><b>Worth knowing:</b> raising your contribution a little often flips several employees from waiving to enrolling, and an ICHRA lets you set a flat monthly dollar amount instead.</div>';
    } else if(PART >= 0.70){
      VERDICT='Eligible now';
      html='<div class="vcard good"><span class="vtag">Good news</span><h3>Yes &mdash; you can put a group plan in place</h3>'
        +'<p>At <b>'+pct+'%</b> participation you clear the minimum most carriers apply to small groups, which is typically around 70% of employees who don\'t have other coverage.</p>'
        +'<p>With '+emp+' W-2 '+(emp===1?'employee':'employees')+' and '+enroll+' enrolling, you can be quoted for coverage effective the first of next month.</p></div>';
      routes='<div class="wnote"><b>Which route fits:</b> a fully insured small group plan is the usual starting point. '
        +(emp>=10?'At your size, a level-funded plan often comes in 10&ndash;20% lower if your team is relatively healthy. ':'')
        +(emp<50?'You could also use a QSEHRA, which lets you reimburse employees tax-free up to $6,450 for single coverage in 2026 without buying a group plan at all.':'An ICHRA is the other route, with no participation requirement and no contribution cap.')
        +'</div>';
    } else {
      VERDICT='Below participation — Nov 15-Dec 15 window applies';
      html='<div class="vcard warn"><span class="vtag">Yes, but timing matters</span><h3>You are under the usual participation minimum &mdash; and there is a window that ignores it</h3>'
        +'<p>At <b>'+pct+'%</b> participation you would normally be declined, because carriers typically want about 70% of employees without other coverage to enroll.</p>'
        +'<p><b>Between November 15 and December 15</b>, carriers must offer small group coverage effective January 1 without applying minimum participation or employer contribution requirements. It is a federal guaranteed-availability rule, it runs once a year, and most small employers have never heard of it.</p></div>';
      routes='<div class="wnote"><b>What this means for you:</b> if you apply inside that window for a January 1 start date, your participation number stops being the obstacle. Outside it, an ICHRA is the route that has no participation requirement at any time of year. '
        +'<a href="/blog/group-health-insurance-minimum-participation">How minimum participation actually works &rarr;</a></div>';
    }
    v.innerHTML=html; r.innerHTML=routes;
    captureDraft(3, 'Verdict: '+VERDICT+'. Participation '+pct+'% ('+enroll+' enrolling of '+eligible+' without other coverage). Payroll: '+STRUCT+'.');
    show(4);
  };

  window.buildNotes=function(){
    var emp=num('biz-employees');
    return 'Group Eligibility Checker. '+emp+' W-2 employees. Payroll structure: '+(STRUCT||'not given')
      +'. Enrolling: '+num('cnt-enroll')+'. Other coverage: '+num('cnt-waive')
      +'. 1099 contractors: '+num('cnt-1099')
      +'. Participation: '+Math.round(PART*100)+'%. Result: '+VERDICT+'.';
  };
"""

ELIG = dict(
    slug="group-health-eligibility-checker",
    title="Do You Have Enough Employees for Group Health Insurance? Free Check (2027)",
    desc="Find out in 60 seconds whether your business can get a group health plan. Checks W-2 headcount, participation and the Nov 15-Dec 15 window most employers miss.",
    kw="how many employees do you need for group health insurance, group health insurance eligibility, minimum participation group health insurance, small business health insurance requirements, can i get group health insurance with 2 employees, group health insurance florida requirements",
    appname="Group Health Insurance Eligibility Checker",
    eyebrow="Free eligibility check",
    h1="Do you have enough employees for group health insurance?",
    lede="Most small employers are told no by one carrier and assume the answer is no everywhere. Answer three questions and find out where you actually stand &mdash; including the one window each year when participation rules don't apply.",
    trust='<span>60 seconds</span><span>No cost, no obligation</span><span>Licensed in 40+ states</span>',
    total=5,
    steps=ELIG_STEPS,
    logic=ELIG_LOGIC,
    leadsource="Group Eligibility Checker",
    leadtag="eligibility-checker",
    toollabel="Group Eligibility Checker",
    faqh="Group health eligibility questions",
    faq=[
        ("How many employees do you need for group health insurance?",
         "In most states, including Florida, you can set up small group coverage with as few as one enrolled W-2 employee besides the owner - two people total. The owner alone is not enough, because carriers treat a business with nobody else on payroll as an individual rather than a group. Businesses with up to 50 employees are considered a small group."),
        ("What is minimum participation for group health insurance?",
         "Carriers typically require about 70% of eligible employees to enroll. The important detail is that employees who waive because they have other coverage - a spouse's plan, a parent's plan, Medicare, VA or TRICARE - are removed from the calculation entirely. A business with 10 employees where 4 have coverage elsewhere only needs about 4 of the remaining 6 to enroll."),
        ("Is there a way around minimum participation requirements?",
         "Yes. Under federal guaranteed-availability rules, carriers must offer small group coverage between November 15 and December 15 each year for a January 1 effective date without applying minimum participation or employer contribution requirements. An ICHRA is the other route, because it has no participation requirement at any time of year."),
        ("Do 1099 contractors count toward group health insurance eligibility?",
         "No. Only W-2 employees count toward group eligibility and participation. Contractors cannot be enrolled on a group plan, though there are other ways to help them get covered, including reimbursement arrangements and individual coverage."),
        ("Can the owner and their spouse get a group plan?",
         "It depends on the carrier. Some carriers treat an owner-plus-spouse business as a group of one and decline it; others will write it if the spouse is a legitimate W-2 employee with payroll records. It is worth checking, because the answer varies by carrier and by state."),
        ("Does the employer have to pay for the plan?",
         "Carriers normally require the employer to contribute at least 50% of the employee-only premium. During the November 15 to December 15 window that contribution requirement is waived along with the participation requirement."),
    ],
    ctah="Not sure which route fits your business?",
    ctap="A licensed VS Health Benefits advisor will look at your headcount and tell you what will actually get written - at no cost to you.",
    related='Related: <a href="/employer-health-insurance-cost-calculator">Employer cost calculator</a> &middot; <a href="/blog/group-health-insurance-minimum-participation">Minimum participation explained</a> &middot; <a href="/small-business-health-insurance">Small business health insurance</a> &middot; <a href="/ichra-vs-group-health-calculator">ICHRA vs group health</a>',
)


# ================================================================= TOOL 2
COST_STEPS = STEP1 % dict(
    h="Let's price your group",
    sub="Four quick questions and you'll see what a plan costs you per employee, what comes out of their paycheck, and what you get back in payroll tax.",
    cta="Start my estimate",
) + """
      <div class="wstep" id="s2">
        <h2>Tell us about your team</h2>
        <p class="wsub">Premiums move with the average age of your group and how many people add dependents. These two inputs do most of the work.</p>
        <div class="wf">
          <label>Average age of your team</label>
          <div class="wseg" id="age-seg">
            <button type="button" data-age="0.80">Under 30</button>
            <button type="button" data-age="1.00" class="on">30&ndash;39</button>
            <button type="button" data-age="1.28">40&ndash;49</button>
            <button type="button" data-age="1.65">50+</button>
          </div>
        </div>
        <div class="wf" id="f-fam">
          <label for="cnt-family">How many would add a spouse or children?</label>
          <input type="number" id="cnt-family" min="0" max="500" placeholder="2" inputmode="numeric" />
          <div class="hint">Family coverage runs roughly 2.7&times; the employee-only rate. You choose separately how much of that you cover.</div>
        </div>
        <div class="wnav">
          <button class="wback" type="button" onclick="wBack(1)">&larr; Back</button>
          <button class="wnext" type="button" onclick="wStep2()">Continue &rarr;</button>
        </div>
      </div>

      <div class="wstep" id="s3">
        <h2>How much do you want to contribute?</h2>
        <p class="wsub">Carriers normally require at least 50% of the employee-only premium. Everything above that is your call.</p>
        <div class="wf">
          <label>Your share of the employee-only premium</label>
          <div class="wseg" id="contrib-seg">
            <button type="button" data-c="0.50" class="on">50%</button>
            <button type="button" data-c="0.60">60%</button>
            <button type="button" data-c="0.75">75%</button>
            <button type="button" data-c="1.00">100%</button>
          </div>
        </div>
        <div class="wf">
          <label>Your share of dependent coverage</label>
          <div class="wseg" id="dep-seg">
            <button type="button" data-d="0" class="on">0%</button>
            <button type="button" data-d="0.25">25%</button>
            <button type="button" data-d="0.50">50%</button>
            <button type="button" data-d="1.00">100%</button>
          </div>
          <div class="hint">Most small employers cover the employee and let the employee pay for dependents. That is completely normal.</div>
        </div>
        <div class="wnav">
          <button class="wback" type="button" onclick="wBack(2)">&larr; Back</button>
          <button class="wnext" type="button" onclick="wStep3()">See my numbers &rarr;</button>
        </div>
      </div>

      <div class="wstep" id="s4">
        <div class="bigres">
          <small>Your cost per month</small>
          <b id="r-employer">&mdash;</b>
          <span id="r-per">&mdash;</span>
        </div>
        <div class="rlist">
          <div><span>Total group premium</span><b id="r-total">&mdash;</b></div>
          <div><span>Employee-only premium, per person</span><b id="r-single">&mdash;</b></div>
          <div><span>Employee payroll deductions</span><b id="r-ee">&mdash;</b></div>
          <div><span>Your annual cost</span><b id="r-annual">&mdash;</b></div>
          <div class="hl"><span>Payroll tax you save (Section 125)</span><b id="r-fica">&mdash;</b></div>
          <div class="hl"><span>Net annual cost after tax savings</span><b id="r-net">&mdash;</b></div>
        </div>
        <div class="wnote"><b>The savings most owners miss:</b> when employee premiums are run pre-tax through a Section 125 plan, you don't pay the 7.65% employer FICA on that money. On a group this size that is <b id="r-fica2">&mdash;</b> a year back in your pocket, and it is not counted in the sticker price a carrier quotes you.</div>
        <div class="wnav">
          <button class="wback" type="button" onclick="wBack(3)">&larr; Back</button>
          <button class="wnext" type="button" onclick="wShow(5)">Email me these numbers &rarr;</button>
        </div>
        <p class="wfine">Estimate only, based on a mid-range plan at 2026&ndash;2027 small group rates for Florida and nearby states. Bronze runs lower and Gold higher; your advisor will price all three. Real premiums depend on your ZIP code, exact employee ages, carrier and plan design. VS Health Benefits quotes and sets up group coverage at no cost to the employer.</p>
      </div>
""" + FINAL_STEP % dict(
    n=5, back=4,
    sub="We'll send this estimate and a licensed advisor will follow up with real quotes from the carriers writing groups in your area.",
    cta="Send my estimate",
    done=6,
    donetext="Your estimate is on its way. A licensed VS Health Benefits advisor will follow up with actual carrier pricing for your group.",
)

COST_LOGIC = r"""
  var AGE=1.00, CEE=0.50, CDEP=0;
  var BASE=605;   /* mid-range (Silver-level) small group rate */
  var FAMFACTOR=2.7, FICA=0.0765;

  function seg(id, cb){
    var w=document.getElementById(id); if(!w) return;
    w.addEventListener('click', function(e){
      var b=e.target.closest('button'); if(!b) return;
      w.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});
      b.classList.add('on'); cb(b); calc();
    });
  }
  seg('age-seg',     function(b){ AGE=parseFloat(b.getAttribute('data-age')); });
  seg('contrib-seg', function(b){ CEE=parseFloat(b.getAttribute('data-c')); });
  seg('dep-seg',     function(b){ CDEP=parseFloat(b.getAttribute('data-d')); });

  var LAST={};
  function calc(){
    var emp=Math.max(1, Math.min(500, num('biz-employees')||1));
    var fam=Math.min(emp, num('cnt-family'));
    var single=AGE*BASE;
    var dep=single*(FAMFACTOR-1);
    var total=emp*single + fam*dep;
    var employer=emp*single*CEE + fam*dep*CDEP;
    var employee=total-employer;
    var per=employer/emp;
    var fica=employee*FICA;
    var net=(employer-fica)*12;
    LAST={emp:emp,fam:fam,total:total,employer:employer,employee:employee,per:per,fica:fica*12,net:net};
    function set(id,v){ var e=document.getElementById(id); if(e) e.textContent=v; }
    set('r-employer', money(employer)+'/mo');
    set('r-per', money(per)+' per employee, per month');
    set('r-total', money(total)+'/mo');
    set('r-single', money(single)+'/mo');
    set('r-ee', money(employee)+'/mo');
    set('r-annual', money(employer*12));
    set('r-fica', money(fica*12)+'/yr');
    set('r-fica2', money(fica*12));
    set('r-net', money(net)+'/yr');
  }
  var famEl=document.getElementById('cnt-family'); if(famEl) famEl.addEventListener('input', calc);
  var empEl=document.getElementById('biz-employees'); if(empEl) empEl.addEventListener('input', calc);

  window.wStep2=function(){ calc(); captureDraft(2, 'Age factor '+AGE+', '+num('cnt-family')+' taking family coverage.'); show(3); };
  window.wStep3=function(){
    calc();
    captureDraft(3, 'Estimate: employer '+money(LAST.employer)+'/mo, total premium '+money(LAST.total)+'/mo, annual employer cost '+money(LAST.employer*12)+'.');
    show(4);
  };

  window.buildNotes=function(){
    return 'Employer Cost Calculator. '+LAST.emp+' employees, '+LAST.fam+' taking family coverage. '
      +'Employer share '+Math.round(CEE*100)+'% of employee-only, '+Math.round(CDEP*100)+'% of dependents. '
      +'Estimate: total premium '+money(LAST.total)+'/mo, employer '+money(LAST.employer)+'/mo ('+money(LAST.per)+' per employee), '
      +'employee deductions '+money(LAST.employee)+'/mo, annual employer cost '+money(LAST.employer*12)+', '
      +'Section 125 payroll tax saving '+money(LAST.fica)+'/yr.';
  };
  calc();
"""

COST = dict(
    slug="employer-health-insurance-cost-calculator",
    title="Employer Health Insurance Cost Calculator: What Will It Cost Per Employee? (2027)",
    desc="See what group health insurance costs your business per employee per month, what employees pay, and the payroll tax you get back. Free instant estimate.",
    kw="employer health insurance cost calculator, how much does it cost to offer health insurance to employees, group health insurance cost per employee, small business health insurance cost calculator, employer contribution health insurance calculator, cost of employee benefits calculator",
    appname="Employer Health Insurance Cost Calculator",
    eyebrow="Free instant estimate",
    h1="What will health insurance actually cost me per employee?",
    lede="Carriers quote you a premium. They don't show you your share, your employees' share, or the payroll tax you get back. This does all three.",
    trust='<span>Instant estimate</span><span>No cost, no obligation</span><span>Licensed in 40+ states</span>',
    total=5,
    steps=COST_STEPS,
    logic=COST_LOGIC,
    leadsource="Employer Cost Calculator",
    leadtag="cost-calculator",
    toollabel="Employer Cost Calculator",
    faqh="Employer cost questions",
    faq=[
        ("How much does it cost an employer to offer health insurance?",
         "For 2026-2027, small group coverage commonly runs about $470 to $740 per employee per month for employee-only coverage, before the employer's share is applied. Most small employers contribute 50% to 75% of that, which puts real employer cost somewhere around $250 to $500 per employee per month depending on plan level and the average age of the team."),
        ("How much does an employer have to contribute to health insurance?",
         "Carriers generally require the employer to contribute at least 50% of the employee-only premium. There is normally no requirement to contribute anything toward dependent coverage, which is why most small employers cover the employee and let employees pay for spouses and children."),
        ("Do employers save money on payroll taxes by offering health insurance?",
         "Yes. When employee premium contributions are taken pre-tax through a Section 125 cafeteria plan, that money is not subject to FICA, so the employer avoids the 7.65% payroll tax on it. On a group of ten employees this commonly returns several thousand dollars a year, and it is never included in the premium a carrier quotes."),
        ("Is health insurance for employees tax deductible?",
         "Employer contributions toward employee health premiums are generally a deductible business expense. Businesses with fewer than 25 full-time equivalent employees and low average wages may also qualify for the Small Business Health Care Tax Credit. Check your specific situation with your tax advisor."),
        ("How much cheaper is a level-funded plan?",
         "Level-funded plans often come in 10% to 20% below a fully insured plan for groups with a relatively healthy team, and can return unused claims dollars at the end of the year. They typically make sense from about ten enrolled employees upward."),
        ("Can I offer money toward insurance instead of buying a group plan?",
         "Yes. A QSEHRA lets employers with fewer than 50 employees reimburse employees tax-free for individual coverage, capped at $6,450 for single and $13,100 for family in 2026. An ICHRA works similarly with no contribution cap and no company size limit."),
    ],
    ctah="Want real carrier pricing instead of an estimate?",
    ctap="Send us your employee census and a licensed VS Health Benefits advisor will come back with actual quotes - at no cost to your business.",
    related='Related: <a href="/group-health-eligibility-checker">Group eligibility checker</a> &middot; <a href="/small-business-health-insurance-cost">Small business health insurance cost</a> &middot; <a href="/level-funded-health-insurance-florida">Level-funded plans</a> &middot; <a href="/ichra-vs-group-health-calculator">ICHRA vs group health</a>',
)


def main():
    ho, st, hd, ft, tl = shell()
    for cfg in (ELIG, COST):
        build(cfg, ho, st, hd, ft, tl)


if __name__ == "__main__":
    main()

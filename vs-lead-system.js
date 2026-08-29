/* =====================================================================
   VS LEAD SYSTEM  (vs-lead-system.js)
   Cookie consent + abandoned-draft recovery for the /quote funnel.

   Privacy-first design:
   - No analytics/marketing cookies load until the visitor consents
     (GDPR "prior consent" / CCPA-CPRA opt-out friendly).
   - Form progress is NOT kept in this browser. There is no "resume / start over"
     banner: a returning visitor gets a clean form, and the recovery happens on
     Bradley's side from the captured lead, not on the visitor's screen.
   - In-progress leads are auto-captured to our own /api/lead-draft (server-side
     validated) once a valid PHONE or email is present, even if the visitor never
     submits. The /quote funnel asks for ZIP and phone before name and email, so an
     abandoned quote still lands in the CRM with a number to call and an area to quote.
   - Clears the local draft the moment the form is successfully submitted.

   Safe by design: everything is wrapped in try/catch and degrades to a
   normal working form if anything is unavailable.
   ===================================================================== */
(function(){
  "use strict";
  var CONSENT_KEY='vs_consent';
  var GA_ID='G-Z6EVXL76GG', ADS_ID='AW-17950389267';

  function $(id){return document.getElementById(id);}
  function store(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
  function load(k){try{return JSON.parse(localStorage.getItem(k)||'null');}catch(e){return null;}}
  function del(k){try{localStorage.removeItem(k);}catch(e){}}
  function ready(fn){ if(document.readyState!=='loading'){fn();} else {document.addEventListener('DOMContentLoaded',fn);} }
  function inject(src,attrs){var s=document.createElement('script');s.src=src;s.async=true;if(attrs)Object.keys(attrs).forEach(function(k){s.setAttribute(k,attrs[k]);});document.head.appendChild(s);return s;}

  /* ---------------- STYLES ---------------- */
  var CSS=""
   +"#vs-consent-banner{position:fixed;left:0;right:0;bottom:0;z-index:10000;background:#fff;border-top:3px solid #0db5a6;box-shadow:0 -8px 30px rgba(13,27,42,.16);padding:18px 16px;display:none;font-family:'Inter',system-ui,sans-serif}"
   +"#vs-consent-banner.show{display:block}"
   +".vs-cc-wrap{max-width:1080px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:14px 20px}"
   +".vs-cc-text{flex:1;min-width:260px;font-size:.86rem;color:#334155;line-height:1.55}"
   +".vs-cc-text strong{color:#0b2346}.vs-cc-text a{color:#16447f;font-weight:600;text-decoration:underline}"
   +".vs-cc-btns{display:flex;flex-wrap:wrap;gap:8px}"
   +".vs-cc-btn{border:2px solid #16447f;background:#fff;color:#16447f;font-weight:700;font-size:.85rem;padding:10px 18px;border-radius:999px;cursor:pointer;font-family:inherit;min-height:42px}"
   +".vs-cc-btn.primary{background:#16447f;color:#fff}.vs-cc-btn.teal{background:#0db5a6;border-color:#0db5a6;color:#fff}.vs-cc-btn:hover{opacity:.92}"
   +".vs-cc-prefs{width:100%;margin-top:6px;padding-top:12px;border-top:1px solid #e4e9f2;display:none;gap:18px;flex-wrap:wrap}"
   +".vs-cc-prefs.show{display:flex}"
   +".vs-cc-pref{display:flex;align-items:flex-start;gap:9px;font-size:.82rem;color:#334155;max-width:320px}"
   +".vs-cc-pref input{margin-top:3px;width:17px;height:17px;accent-color:#0db5a6}"
   +".vs-cc-pref b{color:#0b2346;display:block;font-size:.85rem}.vs-cc-pref.locked{opacity:.7}"
   +""
   +".vs-recover-row{display:flex;align-items:flex-start;gap:9px;margin:14px 0 2px;padding:11px 13px;background:#f7faff;border:1px solid #e4e9f2;border-radius:10px;font-size:.8rem;color:#475569;line-height:1.5;cursor:pointer}"
   +".vs-recover-row input[type=checkbox]{-webkit-appearance:checkbox!important;appearance:checkbox!important;box-sizing:border-box!important;width:18px!important;height:18px!important;min-width:18px!important;max-width:18px!important;min-height:18px!important;padding:0!important;margin:1px 8px 0 0!important;border:0!important;border-radius:0!important;box-shadow:none!important;background:none!important;flex:0 0 auto!important;accent-color:#0db5a6!important;vertical-align:top}"
   +".vs-recover-row a{color:#16447f;font-weight:600;text-decoration:underline}"
   +".vs-ck-link{background:none;border:0;color:inherit;text-decoration:underline;cursor:pointer;font:inherit;padding:0}";
  function addStyles(){ if($('vs-consent-styles'))return; var st=document.createElement('style'); st.id='vs-consent-styles'; st.textContent=CSS; (document.head||document.documentElement).appendChild(st); }
  addStyles();

  /* ---------------- CONSENT MANAGER ---------------- */
  window.dataLayer=window.dataLayer||[];
  window.gtag=window.gtag||function(){window.dataLayer.push(arguments);};
  var consent=load(CONSENT_KEY);
  var _aOn=false,_mOn=false;
  function loadAnalytics(){ if(_aOn)return; _aOn=true;
    inject('https://www.googletagmanager.com/gtag/js?id='+GA_ID);
    gtag('js',new Date()); gtag('config',GA_ID,{anonymize_ip:true});
  }
  function loadMarketing(){ if(_mOn)return; _mOn=true;
    inject('https://www.googletagmanager.com/gtag/js?id='+ADS_ID);
    gtag('config',ADS_ID);
  }
  function killCookies(names){
    var domains=['','.'+location.hostname,location.hostname,'.vshealthbenefits.com'];
    document.cookie.split(';').forEach(function(ck){
      var n=ck.split('=')[0].trim();
      for(var i=0;i<names.length;i++){
        if(n===names[i]||n.indexOf(names[i])===0){
          domains.forEach(function(dm){document.cookie=n+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'+(dm?';domain='+dm:'');});
        }
      }
    });
  }
  function applyConsent(c){
    if(!c)return;
    if(c.analytics) loadAnalytics(); else killCookies(['_ga','_gid','_gat']);
    if(c.marketing) loadMarketing(); else killCookies(['_gcl_au']);
  }
  function saveConsent(a,m){
    consent={analytics:!!a,marketing:!!m,ts:Date.now(),v:1};
    store(CONSENT_KEY,consent); applyConsent(consent); hideBanner();
  }

  /* ---------------- CONSENT BANNER UI ---------------- */
  function buildBanner(){
    if($('vs-consent-banner'))return;
    var b=document.createElement('div'); b.id='vs-consent-banner';
    b.innerHTML=''
      +'<div class="vs-cc-wrap">'
      +'  <div class="vs-cc-text"><strong>We value your privacy.</strong> We use essential cookies to run this site. With your permission we also use analytics and marketing cookies to improve the site and measure our ads. See our <a href="/privacy" target="_blank" rel="noopener">Privacy Policy</a>.</div>'
      +'  <div class="vs-cc-btns">'
      +'    <button type="button" class="vs-cc-btn" id="vs-cc-customize">Customize</button>'
      +'    <button type="button" class="vs-cc-btn" id="vs-cc-decline">Decline</button>'
      +'    <button type="button" class="vs-cc-btn teal" id="vs-cc-accept">Accept all</button>'
      +'  </div>'
      +'  <div class="vs-cc-prefs" id="vs-cc-prefs">'
      +'    <label class="vs-cc-pref locked"><input type="checkbox" checked disabled><span><b>Essential</b>Required for the site and forms to work. Always on.</span></label>'
      +'    <label class="vs-cc-pref"><input type="checkbox" id="vs-cc-analytics"><span><b>Analytics</b>Helps us understand how visitors use the site (Google Analytics).</span></label>'
      +'    <label class="vs-cc-pref"><input type="checkbox" id="vs-cc-marketing"><span><b>Marketing</b>Measures ad performance and enables follow-up (Google Ads).</span></label>'
      +'    <button type="button" class="vs-cc-btn primary" id="vs-cc-save" style="align-self:center">Save my choices</button>'
      +'  </div>'
      +'</div>';
    document.body.appendChild(b);
    $('vs-cc-accept').onclick=function(){saveConsent(true,true);};
    $('vs-cc-decline').onclick=function(){saveConsent(false,false);};
    $('vs-cc-customize').onclick=function(){$('vs-cc-prefs').classList.toggle('show');};
    $('vs-cc-save').onclick=function(){saveConsent($('vs-cc-analytics').checked,$('vs-cc-marketing').checked);};
  }
  function showBanner(openPrefs){
    buildBanner();
    if(consent){ var a=$('vs-cc-analytics'),m=$('vs-cc-marketing'); if(a)a.checked=!!consent.analytics; if(m)m.checked=!!consent.marketing; }
    $('vs-consent-banner').classList.add('show');
    if(openPrefs)$('vs-cc-prefs').classList.add('show');
  }
  function hideBanner(){ var b=$('vs-consent-banner'); if(b)b.classList.remove('show'); }
  window.vsOpenCookieSettings=function(){ showBanner(true); return false; };

  if(consent && typeof consent.analytics!=='undefined'){ applyConsent(consent); }
  else { ready(function(){ showBanner(false); }); }

  ready(function(){
    var f=document.querySelector('footer .foot-bottom')||document.querySelector('footer');
    if(f){ var lk=document.createElement('a'); lk.href='#'; lk.className='vs-ck-link'; lk.style.cssText='margin-left:10px;color:inherit;text-decoration:underline;font-size:.8rem';
      lk.textContent='Cookie settings'; lk.onclick=function(e){e.preventDefault();window.vsOpenCookieSettings();}; f.appendChild(lk); }
  });

  /* ---------------- DRAFT AUTOSAVE + RESUME ---------------- */
  var IND=['ind-firstname','ind-lastname','ind-dob','ind-address','ind-zip','ind-state','ind-phone','ind-email'];
  var BIZ=['biz-firstname','biz-lastname','biz-contact-phone','biz-email','biz-name','biz-employees','biz-coverage','biz-insured','biz-start','biz-address','biz-zip','biz-state','biz-phone'];
  var _vsType=null,_vsStep=1,_vsIncome=null,_submitted=false,_t=null;

  function snapshot(){
    var d={fields:{},sits:{ind:[],biz:[]},income:_vsIncome,type:_vsType,step:_vsStep,ts:Date.now(),v:1};
    IND.concat(BIZ).forEach(function(id){var el=$(id);if(el&&el.value)d.fields[id]=el.value;});
    document.querySelectorAll('#ind-situations input:checked').forEach(function(cb){d.sits.ind.push(cb.value);});
    document.querySelectorAll('#biz-situations input:checked').forEach(function(cb){d.sits.biz.push(cb.value);});
    if(!d.income){var s=document.querySelector('#ind-income .income-item.selected'); if(s)d.income=s.textContent.trim();}
    return d;
  }
  function meaningful(d){ if(!d)return false; var f=d.fields||{}; return !!(f['ind-phone']||f['ind-zip']||f['ind-firstname']||f['ind-email']||f['biz-contact-phone']||f['biz-email']||f['biz-name']||f['biz-firstname']); }
  function scheduleSave(){ if(_submitted)return; clearTimeout(_t); _t=setTimeout(doSave,800); }
  function doSave(){ var d=snapshot(); if(meaningful(d)) maybeBackend(d); }

  /* Backend draft save — fires as soon as we have a reachable contact point.
     A valid phone is enough: the funnel collects ZIP + phone before name + email,
     so this is what turns an abandoned quote into a followable lead. The server
     dedupes on phone (then email), so the completed submission later updates the
     SAME contact instead of creating a second one. */
  var _lastBE=0,_lastHash='';
  function validEmail(v){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(String(v||'').trim()); }
  function validPhone(v){
    var d=String(v||'').replace(/\D/g,'');
    if(d.length===11&&d.charAt(0)==='1')d=d.slice(1);
    if(d.length!==10)return false;
    if(/^(\d)\1{9}$/.test(d))return false;
    if(d.slice(0,3)==='555'||d.slice(3,6)==='555')return false;
    return true;
  }
  function draftPayload(d){
    var f=d.fields||{};
    // Situation and income are not <input> values, so they never reach the card
    // through `fields`. Fold them into the note instead - a lead that says "lost
    // job coverage, $35-50k" is worth more on the phone than a bare number.
    var extras=[];
    var sits=((d.sits&&d.sits.ind)||[]).concat((d.sits&&d.sits.biz)||[]);
    if(sits.length) extras.push('Situation: '+sits.join(', '));
    if(d.income) extras.push('Household income: '+d.income);
    if(f['ind-dob']) extras.push('DOB: '+f['ind-dob']);
    if(f['biz-employees']) extras.push('Employees: '+f['biz-employees']);
    if(f['biz-coverage']) extras.push('Requested coverage: '+f['biz-coverage']);
    return {consent:true,capture:'auto',optIn:false,type:d.type||_vsType||'individual',step:'Step '+(d.step||_vsStep||1),
      email:cleanEmail(f['ind-email']||f['biz-email']||''),
      phone:(f['ind-phone']||f['biz-contact-phone']||f['biz-phone']||'').trim(),
      firstName:f['ind-firstname']||f['biz-firstname']||'',
      lastName:f['ind-lastname']||f['biz-lastname']||'',
      address:f['ind-address']||f['biz-address']||'',
      zip:f['ind-zip']||f['biz-zip']||'',state:f['ind-state']||f['biz-state']||'',
      company:f['biz-name']||'',
      notes:extras.join('; ')};
  }
  /* Only pass an email the funnel itself is happy with: a half-typed or mistyped
     address (jane@gmial.com) would otherwise land on the CRM record. */
  function cleanEmail(v){
    v=String(v||'').trim(); if(!validEmail(v))return '';
    try{ if(window.vsSuggestEmail && window.vsSuggestEmail(v)) return ''; }catch(e){}
    return v;
  }
  function reachable(p){ return validEmail(p.email)||validPhone(p.phone); }
  /* Dedupe key: everything the card would show, minus the step label. Moving
     from step 3 to step 4 without answering anything is not worth a write. */
  function payloadKey(p){ var c={}; Object.keys(p).forEach(function(k){ if(k!=='step') c[k]=p[k]; }); return JSON.stringify(c); }

  /* Typing is noisy: every 800ms pause would otherwise be a CRM write and a
     board read-modify-write. Rate-limited to one post per 8s while typing; the
     step advance below and the exit beacon are not rate-limited, so the last
     state a visitor typed always gets out. */
  function maybeBackend(d){
    if(_submitted)return;
    var payload=draftPayload(d); if(!reachable(payload))return;
    var key=payloadKey(payload), now=Date.now();
    if(key===_lastHash) return;
    if(now-_lastBE<8000) return;
    _lastBE=now; _lastHash=key;
    try{fetch('/api/lead-draft',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),keepalive:true}).catch(function(){});}catch(e){}
  }

  /* Called by the funnel the moment a step with a phone number is cleared, so the
     lead is captured on the spot rather than on the next debounce tick. */
  window.vsCaptureDraft=function(type,step){
    if(_submitted)return;
    if(type)_vsType=type; if(step)_vsStep=step;
    var d=snapshot();
    var payload=draftPayload(d); if(!reachable(payload))return;
    var key=payloadKey(payload);
    if(key===_lastHash) return;                        // nothing new since the last post
    _lastBE=Date.now(); _lastHash=key;
    try{fetch('/api/lead-draft',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),keepalive:true}).catch(function(){});}catch(e){}
  };

  /* Send the latest partial lead on exit (mobile-safe) so nothing is lost even if the
     debounced autosave has not fired yet. */
  function beaconSend(){
    if(_submitted)return; var d=snapshot(); if(!meaningful(d))return;
    var payload=draftPayload(d); if(!reachable(payload))return;
    try{ var body=JSON.stringify(payload), key=payloadKey(payload);
      if(key===_lastHash) return;                      // already sent this exact state
      _lastBE=Date.now(); _lastHash=key;
      if(navigator.sendBeacon){ navigator.sendBeacon('/api/lead-draft', new Blob([body],{type:'application/json'})); }
      else { fetch('/api/lead-draft',{method:'POST',headers:{'Content-Type':'application/json'},body:body,keepalive:true}).catch(function(){}); }
    }catch(e){}
  }

  /* Wrap the funnel's global navigation so we always know type/step and can autosave. */
  function wrap(name,before){ var orig=window[name]; if(typeof orig!=='function')return; window[name]=function(){ try{before.apply(null,arguments);}catch(e){} return orig.apply(this,arguments); }; }
  wrap('selectType',function(t){_vsType=t;_vsStep=1;});
  wrap('indNav',function(s){
    var fwd = s > _vsStep; _vsType='individual'; _vsStep=s;
    if(fwd && window.vsCaptureDraft) window.vsCaptureDraft('individual', s); else scheduleSave();
  });
  wrap('bizNav',function(s){
    var fwd = s > _vsStep; _vsType='business'; _vsStep=s;
    if(fwd && window.vsCaptureDraft) window.vsCaptureDraft('business', s); else scheduleSave();
  });
  wrap('selectIncome',function(el,val){_vsIncome=val;scheduleSave();});
  wrap('backTo',function(s){if(s===0){_vsStep=0;}});

  function clearDraft(){ _submitted=true; }

  /* (Removed) resume banner + local draft restore. A half-finished quote is
     recovered by calling the person, not by offering them their old answers
     back on the next visit - the banner told a visitor we had been keeping
     their data and handed them a "Start over" button that threw the lead away.
     The capture below is what makes that unnecessary. */

  /* (Removed) opt-in "save my progress" checkbox — /quote now auto-captures
     in-progress leads without an opt-in box. */

  ready(function(){
    // Typing is rate-limited; leaving a field is not. Blur is the moment a
    // value is actually finished, and on the last step - name and email - it is
    // the only chance to capture them before the visitor goes.
    function saveNow(){ try{ if(window.vsCaptureDraft) window.vsCaptureDraft(_vsType,_vsStep); }catch(e){} }
    var IDENTITY=['ind-firstname','ind-lastname','ind-email','ind-phone',
                  'biz-firstname','biz-lastname','biz-email','biz-contact-phone'];
    IND.concat(BIZ).forEach(function(id){
      var el=$(id); if(!el) return;
      el.addEventListener('input',scheduleSave);
      if(IDENTITY.indexOf(id)>=0){ el.addEventListener('change',saveNow); el.addEventListener('blur',saveNow); }
      else { el.addEventListener('change',scheduleSave); }
    });
    document.querySelectorAll('#ind-situations input,#biz-situations input').forEach(function(cb){cb.addEventListener('change',scheduleSave);});
    document.querySelectorAll('#ind-income .income-item').forEach(function(it){it.addEventListener('click',function(){setTimeout(scheduleSave,20);});});
    var sp=$('panel-success');
    if(sp && window.MutationObserver){ new MutationObserver(function(){ if(sp.classList.contains('active')) clearDraft(); }).observe(sp,{attributes:true,attributeFilter:['class']}); }
    try{ del('vs_quote_draft'); }catch(e){}   // clear drafts left by the old banner
    window.addEventListener('beforeunload',beaconSend);
    window.addEventListener('pagehide',beaconSend);
    document.addEventListener('visibilitychange',function(){ if(document.visibilityState==='hidden') beaconSend(); });
  });
})();

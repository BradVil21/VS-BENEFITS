/* =====================================================================
   VS LEAD SYSTEM  (vs-lead-system.js)
   Cookie consent + abandoned-draft recovery for the /quote funnel.

   Privacy-first design:
   - No analytics/marketing cookies load until the visitor consents
     (GDPR "prior consent" / CCPA-CPRA opt-out friendly).
   - Form progress autosaves to THIS browser only (localStorage).
   - Backend draft save happens ONLY if the visitor ticks the opt-in box,
     and only posts to our own /api/lead-draft (server-side validated).
   - Clears the local draft the moment the form is successfully submitted.

   Safe by design: everything is wrapped in try/catch and degrades to a
   normal working form if anything is unavailable.
   ===================================================================== */
(function(){
  "use strict";
  var CONSENT_KEY='vs_consent', DRAFT_KEY='vs_quote_draft', DRAFT_TTL=7*24*3600*1000;
  var GA_ID='G-Z6EVXL76GG', ADS_ID='AW-17950389267', HS_ID='246725050';

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
   +"#vs-resume-banner{display:none;max-width:680px;margin:0 auto 18px;background:linear-gradient(135deg,#f4f8fe,#eef5ff);border:1px solid #cfe0f7;border-left:4px solid #0db5a6;border-radius:12px;padding:15px 18px}"
   +"#vs-resume-banner.show{display:block}"
   +".vs-rb-row{display:flex;flex-wrap:wrap;align-items:center;gap:12px;justify-content:space-between}"
   +".vs-rb-txt{font-size:.9rem;color:#0b2346;font-weight:600}.vs-rb-txt span{display:block;font-weight:400;color:#5a6b80;font-size:.8rem;margin-top:2px}"
   +".vs-rb-btns{display:flex;gap:8px}"
   +".vs-rb-btn{border:0;border-radius:999px;padding:9px 16px;font-weight:700;font-size:.82rem;cursor:pointer;font-family:inherit;min-height:40px}"
   +".vs-rb-btn.go{background:#16447f;color:#fff}.vs-rb-btn.clear{background:#fff;border:1px solid #cbd5e1;color:#5a6b80}"
   +".vs-recover-row{display:flex;align-items:flex-start;gap:9px;margin:14px 0 2px;padding:11px 13px;background:#f7faff;border:1px solid #e4e9f2;border-radius:10px;font-size:.8rem;color:#475569;line-height:1.5;cursor:pointer}"
   +".vs-recover-row input{margin-top:2px;width:17px;height:17px;flex-shrink:0;accent-color:#0db5a6}"
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
    inject('https://js-na2.hs-scripts.com/'+HS_ID+'.js',{id:'hs-script-loader',defer:'defer'});
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
    if(c.marketing) loadMarketing(); else killCookies(['hubspotutk','__hstc','__hssrc','__hssc','_gcl_au']);
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
      +'    <label class="vs-cc-pref"><input type="checkbox" id="vs-cc-marketing"><span><b>Marketing</b>Measures ad performance and enables follow-up (Google Ads, HubSpot).</span></label>'
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
  function meaningful(d){ if(!d)return false; var f=d.fields||{}; return !!(f['ind-firstname']||f['ind-email']||f['ind-phone']||f['biz-email']||f['biz-name']||f['biz-firstname']); }
  function scheduleSave(){ if(_submitted)return; clearTimeout(_t); _t=setTimeout(doSave,800); }
  function doSave(){ var d=snapshot(); if(meaningful(d)){ store(DRAFT_KEY,d); maybeBackend(d); } }

  /* Backend draft save — ONLY when the visitor opted in AND we have a valid email. */
  var _lastBE=0,_lastHash='';
  function validEmail(v){ return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(String(v||'').trim()); }
  function maybeBackend(d){
    if(_submitted)return;
    var opt=document.querySelector('.vs-recover-consent:checked'); if(!opt)return;
    var email=(d.fields['ind-email']||d.fields['biz-email']||'').trim(); if(!validEmail(email))return;
    var hash=JSON.stringify(d.fields), now=Date.now();
    if(now-_lastBE<15000 && hash===_lastHash)return;
    _lastBE=now; _lastHash=hash;
    var payload={consent:true,type:d.type||_vsType||'individual',step:'Step '+(d.step||_vsStep||1),email:email,
      firstName:d.fields['ind-firstname']||d.fields['biz-firstname']||'',
      lastName:d.fields['ind-lastname']||d.fields['biz-lastname']||'',
      phone:d.fields['ind-phone']||d.fields['biz-contact-phone']||d.fields['biz-phone']||'',
      zip:d.fields['ind-zip']||d.fields['biz-zip']||'',state:d.fields['ind-state']||d.fields['biz-state']||'',
      company:d.fields['biz-name']||''};
    try{fetch('/api/lead-draft',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).catch(function(){});}catch(e){}
  }

  /* Wrap the funnel's global navigation so we always know type/step and can autosave. */
  function wrap(name,before){ var orig=window[name]; if(typeof orig!=='function')return; window[name]=function(){ try{before.apply(null,arguments);}catch(e){} return orig.apply(this,arguments); }; }
  wrap('selectType',function(t){_vsType=t;_vsStep=1;});
  wrap('indNav',function(s){_vsType='individual';_vsStep=s;scheduleSave();});
  wrap('bizNav',function(s){_vsType='business';_vsStep=s;scheduleSave();});
  wrap('selectIncome',function(el,val){_vsIncome=val;scheduleSave();});
  wrap('backTo',function(s){if(s===0){_vsStep=0;}});

  function clearDraft(){ _submitted=true; del(DRAFT_KEY); hideResume(); }

  /* Restore a saved draft into the funnel. */
  function restore(d){
    var type=d.type||((d.fields['biz-email']||d.fields['biz-name']||d.fields['biz-firstname'])?'business':'individual');
    if(window.selectType) window.selectType(type);
    setTimeout(function(){
      Object.keys(d.fields||{}).forEach(function(id){var el=$(id);if(el){el.value=d.fields[id];}});
      restoreSits('#ind-situations',(d.sits&&d.sits.ind)||[]);
      restoreSits('#biz-situations',(d.sits&&d.sits.biz)||[]);
      if(d.income){document.querySelectorAll('#ind-income .income-item').forEach(function(it){ if(it.textContent.trim()===d.income && window.selectIncome){window.selectIncome(it,d.income);} });}
      var step=d.step||1;
      setTimeout(function(){
        if(type==='individual'&&window.indNav){window.indNav(Math.min(step||1,5));}
        else if(type==='business'&&window.bizNav){window.bizNav(Math.min(step||1,4));}
      },260);
    },320);
    hideResume();
  }
  function restoreSits(sel,vals){
    document.querySelectorAll(sel+' input[type=checkbox]').forEach(function(cb){
      if(vals.indexOf(cb.value)!==-1){ cb.checked=true; var lb=cb.closest('label'); if(lb)lb.classList.add('checked'); }
    });
  }

  /* Resume banner */
  function buildResume(d){
    if($('vs-resume-banner'))return;
    var panel0=$('panel-0'); if(!panel0)return;
    var host=panel0.parentNode; if(!host)return;
    var r=document.createElement('div'); r.id='vs-resume-banner';
    var when=''; try{ var mins=Math.round((Date.now()-(d.ts||Date.now()))/60000); when=mins<60?(Math.max(mins,1)+' min ago'):(Math.round(mins/60)+' hr ago'); }catch(e){}
    r.innerHTML='<div class="vs-rb-row"><div class="vs-rb-txt">Welcome back &mdash; want to pick up where you left off?<span>We saved your progress on this device'+(when?(' ('+when+')'):'')+'. Nothing was submitted.</span></div>'
      +'<div class="vs-rb-btns"><button type="button" class="vs-rb-btn go" id="vs-rb-go">Resume</button><button type="button" class="vs-rb-btn clear" id="vs-rb-clear">Start over</button></div></div>';
    host.insertBefore(r,panel0);
    $('vs-rb-go').onclick=function(){ restore(d); };
    $('vs-rb-clear').onclick=function(){ del(DRAFT_KEY); hideResume(); };
  }
  function showResume(d){ buildResume(d); var r=$('vs-resume-banner'); if(r)r.classList.add('show'); }
  function hideResume(){ var r=$('vs-resume-banner'); if(r)r.classList.remove('show'); }

  /* Inject the opt-in consent checkbox into the individual + business contact steps. */
  function injectRecoverRow(emailId){
    var el=$(emailId); if(!el)return; var host=el.parentNode; if(!host)return;
    if(host.querySelector('.vs-recover-row'))return;
    var row=document.createElement('label'); row.className='vs-recover-row';
    row.innerHTML='<input type="checkbox" class="vs-recover-consent"><span>Save my progress so a licensed VS Health Benefits advisor can help me finish if I get interrupted. Optional. Your info is handled per our <a href="/privacy" target="_blank" rel="noopener">Privacy Policy</a>.</span>';
    host.appendChild(row);
    row.querySelector('input').addEventListener('change',function(){ if(this.checked){ doSave(); } });
  }

  ready(function(){
    IND.concat(BIZ).forEach(function(id){var el=$(id); if(el){el.addEventListener('input',scheduleSave);el.addEventListener('change',scheduleSave);}});
    document.querySelectorAll('#ind-situations input,#biz-situations input').forEach(function(cb){cb.addEventListener('change',scheduleSave);});
    document.querySelectorAll('#ind-income .income-item').forEach(function(it){it.addEventListener('click',function(){setTimeout(scheduleSave,20);});});
    injectRecoverRow('ind-email'); injectRecoverRow('biz-email');
    var sp=$('panel-success');
    if(sp && window.MutationObserver){ new MutationObserver(function(){ if(sp.classList.contains('active')) clearDraft(); }).observe(sp,{attributes:true,attributeFilter:['class']}); }
    var saved=load(DRAFT_KEY);
    if(saved && meaningful(saved) && (Date.now()-(saved.ts||0))<DRAFT_TTL){ showResume(saved); }
    else if(saved){ del(DRAFT_KEY); }
    window.addEventListener('beforeunload',function(){ if(!_submitted){ var d=snapshot(); if(meaningful(d)) store(DRAFT_KEY,d); } });
  });
})();

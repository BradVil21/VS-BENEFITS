/* VS Health Benefits: free Owner-Operator Health Insurance Guide (lead magnet).
   Drop <div data-vs-guide></div> on a page and include this script. The visitor
   leaves a first name + mobile number, the lead goes to GoHighLevel through
   /api/lead-sync (tags: trucker, owner-operator-guide), and the PDF opens.
   Also remembers a trucking partner's ?ref= code so partner-sent drivers are
   credited (see /trucking-partners). */
(function(){
  var PDF='/guides/owner-operator-health-insurance-guide.pdf', KEY='vs_guide_ok', PKEY='vs_partner';
  function ls(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}
  // partner attribution: ?ref=acme-logistics is kept 90 days
  try{var ref=(new URLSearchParams(location.search).get('ref')||'').toLowerCase().replace(/[^a-z0-9-]/g,'').slice(0,40);
    if(ref)ls(PKEY,JSON.stringify({ref:ref,t:Date.now()}));}catch(e){}
  window.vsPartnerRef=function(){try{var p=JSON.parse(ls(PKEY)||'null');if(p&&Date.now()-p.t<90*864e5)return p.ref;}catch(e){}return '';};

  var CSS='.vg{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:1fr;gap:22px;align-items:center;background:linear-gradient(135deg,#0b2346,#16447f 60%,#0b6f79);border-radius:22px;padding:28px 22px;color:#fff;box-shadow:0 20px 50px rgba(13,27,42,.18)}'
   +'@media(min-width:880px){.vg{grid-template-columns:1.05fr .95fr;padding:38px 40px;gap:36px}}'
   +'.vg-tag{display:inline-block;font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#8ff0e4;margin-bottom:8px}'
   +'.vg h2{color:#fff!important;font-size:clamp(1.35rem,3.4vw,1.85rem);line-height:1.2;margin:0 0 10px}'
   +'.vg p.vg-sub{color:rgba(255,255,255,.88);margin:0 0 14px;font-size:.98rem}'
   +'.vg ul{list-style:none;margin:0;padding:0;display:grid;gap:8px}'
   +'.vg li{display:flex;gap:9px;align-items:flex-start;color:rgba(255,255,255,.92);font-size:.92rem;line-height:1.4}'
   +'.vg li:before{content:"";flex:none;width:18px;height:18px;margin-top:1px;border-radius:50%;background:#0db5a6 url("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 24 24%27 fill=%27none%27 stroke=%27white%27 stroke-width=%273.2%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27%3E%3Cpath d=%27M20 6 9 17l-5-5%27/%3E%3C/svg%3E") center/11px no-repeat}'
   +'.vg-card{background:#fff;color:#0d1b2a;border-radius:16px;padding:20px 18px}'
   +'.vg-card h3{margin:0 0 4px;font-size:1.05rem;color:#0b2346}.vg-card .vg-note{font-size:.84rem;color:#5a6b80;margin:0 0 12px}'
   +'.vg-row{display:grid;grid-template-columns:1fr;gap:10px}@media(min-width:480px){.vg-row{grid-template-columns:1fr 1fr}}'
   +'.vg-in{width:100%;box-sizing:border-box;font:inherit;font-size:1rem;padding:12px 13px;border:1.5px solid #d6dde8;border-radius:10px;color:#0d1b2a;background:#fff;margin:0}'
   +'.vg-in:focus{outline:none;border-color:#0db5a6;box-shadow:0 0 0 3px rgba(13,181,166,.18)}'
   +'.vg-btn{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;margin-top:12px;font:inherit;font-weight:700;font-size:1rem;color:#fff;background:#16447f;border:0;border-radius:10px;min-height:50px;cursor:pointer;text-decoration:none!important}'
   +'.vg-btn:hover{background:#1e5ab0}.vg-btn[disabled]{opacity:.7;cursor:wait}'
   +'.vg-cons{display:flex;gap:9px;align-items:flex-start;margin-top:10px}.vg-cons input{width:18px;height:18px;margin-top:2px;flex:none}'
   +'.vg-cons label{font-size:.72rem;line-height:1.45;color:#5a6b80;font-weight:400}.vg-cons a{color:#16447f}'
   +'.vg-err{color:#c0392b;font-size:.84rem;font-weight:600;margin:8px 0 0}'
   +'.vg-done{text-align:center}.vg-done p{color:#334155;font-size:.92rem;margin:6px 0 0}';
  var CONSENT='I agree to receive SMS text messages and/or phone calls from <strong>VS BENEFITS LLC</strong> (d/b/a VS Health Benefits) at the number provided, including quote information, appointment confirmations and reminders, and policy service updates. Message &amp; data rates may apply. Message frequency varies. Reply <strong>STOP</strong> to opt out at any time or <strong>HELP</strong> for help. Consent is not a condition of purchase. <a href="/privacy#sms" target="_blank" rel="noopener">Privacy Policy</a> &amp; <a href="/terms#sms-terms" target="_blank" rel="noopener">Terms</a>.';
  function done(card,first){
    card.innerHTML='<div class="vg-done"><h3>Your guide is ready'+(first?', '+first.replace(/[<>&"]/g,''):'')+'</h3>'
      +'<a class="vg-btn" href="'+PDF+'" target="_blank" rel="noopener" data-vs-cta="guide-download">Download the free guide (PDF)</a>'
      +'<p>Want real numbers for your ZIP? <a href="/truckers/quote?from=guide" style="font-weight:700;color:#16447f">Get a 60-second driver quote &rarr;</a></p></div>';
  }
  function mount(el){
    if(el._vg)return;el._vg=1;
    var src=el.getAttribute('data-vs-guide')||location.pathname;
    el.innerHTML='<div class="vg"><div><span class="vg-tag">Free guide &middot; 7 pages</span>'
      +'<h2>The Owner-Operator Health Insurance Guide</h2>'
      +'<p class="vg-sub">Not ready for a quote? Read this first. Written for independent drivers, not office workers.</p>'
      +'<ul><li>The 4 ways to buy coverage, and which one wins if you\'re healthy</li><li>The self-employed tax deduction most drivers miss</li><li>How to make sure your plan works on every route</li><li>Real 2026 cost ranges, 5 costly mistakes, and an enrollment checklist</li></ul></div>'
      +'<form class="vg-card" novalidate><h3>Send me the free guide</h3><p class="vg-note">Instant download. No cost, no obligation.</p>'
      +'<div class="vg-row"><input class="vg-in" name="first" autocomplete="given-name" placeholder="First name" aria-label="First name"><input class="vg-in" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="Mobile number" aria-label="Mobile number"></div>'
      +'<input class="vg-in" name="email" type="email" autocomplete="email" placeholder="Email (optional)" aria-label="Email (optional)" style="margin-top:10px">'
      +'<div class="vg-cons"><input type="checkbox" name="sms" id="vg-sms-'+Math.random().toString(36).slice(2,7)+'"><label>'+CONSENT+'</label></div>'
      +'<p class="vg-err" hidden></p><button class="vg-btn" type="submit">Get the free guide</button></form></div>';
    var cons=el.querySelector('.vg-cons');cons.querySelector('label').setAttribute('for',cons.querySelector('input').id);
    var f=el.querySelector('form'),err=el.querySelector('.vg-err');
    if(ls(KEY)){done(f,'');return;}
    f.addEventListener('submit',function(e){e.preventDefault();
      var first=f.first.value.trim(),email=f.email.value.trim(),d=f.phone.value.replace(/\D/g,'');if(d.length===11&&d[0]==='1')d=d.slice(1);
      function bad(m){err.textContent=m;err.hidden=false;}
      if(!first)return bad('Please enter your first name.');
      if(d.length!==10)return bad('Please enter a 10-digit mobile number.');
      if(email&&!/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(email))return bad('That email looks off. Fix it or leave it blank.');
      err.hidden=true;var b=f.querySelector('.vg-btn');b.disabled=true;b.textContent='One moment...';
      var sms=f.sms.checked,partner=window.vsPartnerRef();
      var tags=['trucker','owner-operator-guide'];if(sms)tags.push('sms-opt-in');if(partner)tags.push('partner-'+partner);
      var notes='Downloaded the Owner-Operator Health Insurance Guide\nPage: '+src+'\nSMS opt-in: '+(sms?'yes':'no')+(partner?'\nReferred by partner: '+partner:'');
      try{if(window.vsTrack)window.vsTrack('generate_lead',{currency:'USD',value:0,lead_type:'guide'});}catch(x){}
      fetch('/api/lead-sync',{method:'POST',headers:{'Content-Type':'application/json'},keepalive:true,
        body:JSON.stringify({firstName:first,phone:d,email:email,source:'Owner-Operator Guide',notes:notes,tags:tags,sms_opt_in:sms?'yes':'no'})})
      .then(function(){ls(KEY,'1');done(f,first);try{window.open(PDF,'_blank','noopener');}catch(x){}},
            function(){b.disabled=false;b.textContent='Get the free guide';bad('Something went wrong. Please try again or speak to an advisor at (954) 825-1009.');});
    });
  }
  function init(){
    if(!document.getElementById('vg-css')){var s=document.createElement('style');s.id='vg-css';s.textContent=CSS;document.head.appendChild(s);}
    [].forEach.call(document.querySelectorAll('[data-vs-guide]'),mount);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();

(function(){
  if(document.getElementById('vsb-root'))return;

  // ── STYLES ──
  var style=document.createElement('style');
  style.textContent=[
    '#vsb-root *{box-sizing:border-box;margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}',
    '#vsb-launcher{position:fixed!important;bottom:24px!important;left:24px!important;z-index:2147483647!important;width:60px!important;height:60px!important;border-radius:50%!important;border:none!important;cursor:pointer!important;background:linear-gradient(135deg,#0b2346,#0db5a6)!important;display:flex!important;align-items:center!important;justify-content:center!important;box-shadow:0 6px 24px rgba(11,35,70,.45)!important;transition:transform .2s!important;outline:none!important}',
    '#vsb-launcher:hover{transform:scale(1.1)!important}',
    '#vsb-badge{position:absolute;top:-3px;right:-3px;width:20px;height:20px;border-radius:50%;background:#f5b301;border:2.5px solid #fff;font-size:11px;font-weight:700;color:#0b2346;display:flex;align-items:center;justify-content:center;pointer-events:none}',
    '#vsb-pulse{position:absolute;inset:0;border-radius:50%;background:rgba(13,181,166,.3);animation:vsbPulse 2s ease-out infinite;pointer-events:none}',
    '@keyframes vsbPulse{0%{transform:scale(1);opacity:.8}100%{transform:scale(1.8);opacity:0}}',
    '#vsb-window{position:fixed!important;bottom:96px!important;left:24px!important;z-index:2147483646!important;width:360px!important;max-width:calc(100vw - 32px)!important;height:560px!important;max-height:calc(100vh - 110px)!important;background:#fff!important;border-radius:20px!important;box-shadow:0 20px 60px rgba(11,35,70,.25),0 4px 16px rgba(11,35,70,.12)!important;border:1px solid rgba(11,35,70,.12)!important;display:none!important;flex-direction:column!important;overflow:hidden!important}',
    '#vsb-window.vsb-open{display:flex!important}',
    '.vsb-head{background:linear-gradient(135deg,#0b2346 0%,#16447f 55%,#0db5a6 100%);padding:14px 16px;display:flex;align-items:center;gap:12px;flex-shrink:0}',
    '.vsb-ava{width:44px;height:44px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,#0db5a6,#f5b301);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;color:#fff;box-shadow:0 2px 8px rgba(0,0,0,.2);position:relative}',
    '.vsb-ava-dot{position:absolute;bottom:1px;right:1px;width:12px;height:12px;border-radius:50%;background:#2dbd79;border:2.5px solid #fff}',
    '.vsb-hname{font-weight:700;font-size:14px;color:#fff;line-height:1.2}',
    '.vsb-hsub{font-size:11px;color:rgba(255,255,255,.7);margin-top:3px;display:flex;align-items:center;gap:5px}',
    '.vsb-hsub::before{content:"";width:6px;height:6px;border-radius:50%;background:#2dbd79;flex-shrink:0}',
    '.vsb-xbtn{margin-left:auto;background:rgba(255,255,255,.18);border:none;cursor:pointer;width:32px;height:32px;border-radius:50%;color:#fff;font-size:20px;display:flex;align-items:center;justify-content:center;flex-shrink:0;line-height:1;transition:background .15s}',
    '.vsb-xbtn:hover{background:rgba(255,255,255,.3)}',
    '.vsb-msgs{flex:1;overflow-y:auto;padding:13px 12px 6px;display:flex;flex-direction:column;gap:9px;background:#f5f7fb;scrollbar-width:thin;scrollbar-color:rgba(11,35,70,.1) transparent}',
    '.vsb-msgs::-webkit-scrollbar{width:4px}',
    '.vsb-msgs::-webkit-scrollbar-thumb{background:rgba(11,35,70,.12);border-radius:2px}',
    '.vsb-row{display:flex;gap:7px;align-items:flex-end}',
    '.vsb-row-u{flex-direction:row-reverse}',
    '.vsb-mav{width:27px;height:27px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,#0b2346,#0db5a6);display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:800;color:#fff}',
    '.vsb-bub{max-width:82%;padding:9px 12px;font-size:13.5px;line-height:1.5;word-break:break-word}',
    '.vsb-bot{background:#fff;border:1px solid rgba(11,35,70,.08);border-radius:4px 15px 15px 15px;color:#0e1726}',
    '.vsb-usr{background:linear-gradient(135deg,#0b2346,#16447f);color:#fff;border-radius:15px 15px 4px 15px}',
    '.vsb-t{display:block;font-size:10px;margin-top:3px;color:#9aabb8}',
    '.vsb-usr .vsb-t{color:rgba(255,255,255,.45)}',
    '.vsb-typing{display:flex;gap:4px;padding:10px 13px;background:#fff;border:1px solid rgba(11,35,70,.08);border-radius:4px 15px 15px 15px;width:fit-content}',
    '.vsb-d{width:7px;height:7px;border-radius:50%;background:#0db5a6;animation:vsbB .75s ease-in-out infinite}',
    '.vsb-d:nth-child(2){animation-delay:.15s}.vsb-d:nth-child(3){animation-delay:.3s}',
    '@keyframes vsbB{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}',
    '.vsb-qr{display:flex;flex-wrap:wrap;gap:6px;padding:4px 0 2px}',
    '.vsb-qb{background:#fff;border:1.5px solid #0db5a6;color:#0b2346;font-size:12.5px;font-weight:600;padding:6px 12px;border-radius:999px;cursor:pointer;transition:all .15s;font-family:inherit}',
    '.vsb-qb:hover{background:#0db5a6;color:#fff}',
    '.vsb-bot-wrap{padding:10px 12px 11px;border-top:1px solid rgba(11,35,70,.07);background:#fff;flex-shrink:0}',
    '.vsb-inrow{display:flex;gap:8px;align-items:flex-end}',
    '.vsb-inp{flex:1;border:1.5px solid rgba(11,35,70,.16);border-radius:11px;padding:9px 12px;font-size:13.5px;color:#0e1726;resize:none;outline:none;background:#fafbfd;min-height:40px;max-height:88px;line-height:1.4;font-family:inherit;transition:border-color .15s}',
    '.vsb-inp:focus{border-color:#0db5a6;background:#fff}',
    '.vsb-inp::placeholder{color:#b0baca}',
    '.vsb-inp:disabled{opacity:.5;cursor:not-allowed}',
    '.vsb-snd{width:40px;height:40px;border-radius:10px;flex-shrink:0;background:linear-gradient(135deg,#0b2346,#0db5a6);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform .15s,opacity .15s}',
    '.vsb-snd:hover{transform:scale(1.06)}.vsb-snd:disabled{opacity:.35;cursor:not-allowed;transform:none}',
    '.vsb-foot{text-align:center;font-size:10px;color:#b0baca;padding:4px 0 3px;flex-shrink:0;background:#fff}',
    '.vsb-ok{background:linear-gradient(135deg,#e8f7ef,#f0fdf6);border:1.5px solid #9fdabc;border-radius:13px;padding:15px;text-align:center;max-width:94%}',
    '.vsb-ok-ic{font-size:30px;margin-bottom:7px}',
    '.vsb-ok h3{font-size:14px;font-weight:700;color:#065f46;margin:0 0 5px}',
    '.vsb-ok p{font-size:12px;color:#064e3b;line-height:1.6;margin:0}',
    '.vsb-ok a{color:#0a8754;font-weight:700}'
  ].join('');
  document.head.appendChild(style);

  // ── HTML ──
  var root=document.createElement('div');
  root.id='vsb-root';
  root.innerHTML=
    '<button id="vsb-launcher" aria-label="Chat with VS Health Benefits">'+
      '<div id="vsb-pulse"></div>'+
      '<div id="vsb-badge">1</div>'+
      '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" style="pointer-events:none;flex-shrink:0">'+
        '<path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" fill="rgba(255,255,255,.92)"/>'+
        '<path d="M8 10h8M8 14h5" stroke="#0b2346" stroke-width="1.8" stroke-linecap="round"/>'+
      '</svg>'+
    '</button>'+
    '<div id="vsb-window">'+
      '<div class="vsb-head">'+
        '<div class="vsb-ava">VS<div class="vsb-ava-dot"></div></div>'+
        '<div style="flex:1;min-width:0">'+
          '<div class="vsb-hname">Ava &middot; VS Health Benefits</div>'+
          '<div class="vsb-hsub">Online &middot; Health Insurance Specialist</div>'+
        '</div>'+
        '<button class="vsb-xbtn" id="vsb-close">&times;</button>'+
      '</div>'+
      '<div class="vsb-msgs" id="vsb-msgs"></div>'+
      '<div class="vsb-bot-wrap">'+
        '<div class="vsb-inrow">'+
          '<textarea class="vsb-inp" id="vsb-inp" rows="1" placeholder="Type a message\u2026"></textarea>'+
          '<button class="vsb-snd" id="vsb-snd" disabled>'+
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="pointer-events:none">'+
              '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>'+
            '</svg>'+
          '</button>'+
        '</div>'+
      '</div>'+
      '<div class="vsb-foot">Powered by <strong style="color:#0db5a6">VS Health Benefits</strong> AI &middot; Licensed Advisors</div>'+
    '</div>';
  document.body.appendChild(root);

  // ── FIREBASE ──
  function loadScript(src,cb){var s=document.createElement('script');s.src=src;s.onload=cb;document.head.appendChild(s);}
  var dbReady=false,db=null;
  function initFB(){
    var cfg={apiKey:"AIzaSyCbZ7Otrz6yPlxJuLlDPEoMzssgsWkjo5U",authDomain:"vs-benefits-c1da9.firebaseapp.com",projectId:"vs-benefits-c1da9",storageBucket:"vs-benefits-c1da9.firebasestorage.app",messagingSenderId:"487471388882",appId:"1:487471388882:web:63e98e6699d5a823e3f50b"};
    var app=firebase.apps&&firebase.apps.length?firebase.apps[0]:firebase.initializeApp(cfg);
    db=firebase.firestore(app);
    firebase.auth(app).signInAnonymously().then(function(){dbReady=true;}).catch(function(e){console.warn('VSB FB:',e);});
  }
  function genId(){return'chat_'+Math.random().toString(36).slice(2,8)+Date.now().toString(36);}
  function saveLead(lead){
    if(!dbReady||!db)return;
    db.collection('vs_state').doc('leads').get().then(function(snap){
      var items=snap.exists?(snap.data().items||[]):[];
      items.unshift({
        id:genId(),
        firstName:lead.firstName||'',lastName:lead.lastName||'',
        name:((lead.firstName||'')+' '+(lead.lastName||'')).trim(),
        email:lead.email||'',phone:lead.phone||'',dob:lead.dob||'',
        zipcode:lead.zip||'',state:lead.state||'',coverage:lead.coverageType||'',
        status:'new',
        notes:'Chat lead | Coverage:'+(lead.coverageType||'N/A')+' | Employees:'+(lead.employees||'N/A')+' | ZIP:'+(lead.zip||'N/A')+(lead.extraNotes?' | '+lead.extraNotes:''),
        created:Date.now(),updated:Date.now(),_source:'chatbot'
      });
      return db.collection('vs_state').doc('leads').set({items:items,ts:Date.now()});
    }).catch(function(e){console.warn('VSB save:',e);});
  }

  // ── STATE ──
  var isOpen=false,isBusy=false,isSubmitted=false,history=[],lead={};
  var launcher=document.getElementById('vsb-launcher');
  var win=document.getElementById('vsb-window');
  var msgs=document.getElementById('vsb-msgs');
  var inp=document.getElementById('vsb-inp');
  var snd=document.getElementById('vsb-snd');
  var badge=document.getElementById('vsb-badge');
  var pulse=document.getElementById('vsb-pulse');

  launcher.addEventListener('click',function(){isOpen?closeChat():openChat();});
  document.getElementById('vsb-close').addEventListener('click',closeChat);

  function openChat(){
    isOpen=true;win.classList.add('vsb-open');
    badge.style.display='none';pulse.style.animation='none';
    if(!history.length)setTimeout(start,350);
    inp.focus();
  }
  function closeChat(){
    isOpen=false;win.classList.remove('vsb-open');
    history=[];lead={};isSubmitted=false;isBusy=false;
    msgs.innerHTML='';inp.value='';inp.disabled=false;
    inp.placeholder='Type a message\u2026';snd.disabled=true;
    badge.style.display='flex';pulse.style.animation='vsbPulse 2s ease-out infinite';
  }

  inp.addEventListener('input',function(){
    inp.style.height='auto';inp.style.height=Math.min(inp.scrollHeight,88)+'px';
    snd.disabled=!inp.value.trim()||isBusy||isSubmitted;
  });
  inp.addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}});
  snd.addEventListener('click',send);

  function send(){
    var t=(inp.value||'').trim();if(!t||isBusy||isSubmitted)return;
    inp.value='';inp.style.height='auto';snd.disabled=true;
    addU(t);turn(t);
  }

  function ts(){var d=new Date();return d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});}
  function esc(s){return String(s||'').replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
  function scroll(){msgs.scrollTop=msgs.scrollHeight;}

  function addU(t){
    removeQR();
    var r=document.createElement('div');r.className='vsb-row vsb-row-u';
    var b=document.createElement('div');b.className='vsb-bub vsb-usr';
    b.innerHTML=esc(t)+'<span class="vsb-t">'+ts()+'</span>';
    r.appendChild(b);msgs.appendChild(r);scroll();
    history.push({role:'user',content:t});
  }
  function addB(t){
    var r=document.createElement('div');r.className='vsb-row';
    var av=document.createElement('div');av.className='vsb-mav';av.textContent='VS';
    var b=document.createElement('div');b.className='vsb-bub vsb-bot';
    b.innerHTML=esc(t).replace(/\n/g,'<br>')+'<span class="vsb-t">'+ts()+'</span>';
    r.appendChild(av);r.appendChild(b);msgs.appendChild(r);scroll();
  }
  function showTyp(){
    var r=document.createElement('div');r.className='vsb-row';r.id='vsb-typ';
    var av=document.createElement('div');av.className='vsb-mav';av.textContent='VS';
    var t=document.createElement('div');t.className='vsb-typing';
    t.innerHTML='<div class="vsb-d"></div><div class="vsb-d"></div><div class="vsb-d"></div>';
    r.appendChild(av);r.appendChild(t);msgs.appendChild(r);scroll();
  }
  function hideTyp(){var t=document.getElementById('vsb-typ');if(t)t.remove();}
  function addQR(opts){
    removeQR();
    var qr=document.createElement('div');qr.className='vsb-qr';qr.id='vsb-qr';
    opts.forEach(function(o){
      var b=document.createElement('button');b.className='vsb-qb';b.textContent=o;
      b.addEventListener('click',function(){removeQR();addU(o);turn(o);});
      qr.appendChild(b);
    });
    msgs.appendChild(qr);scroll();
  }
  function removeQR(){var q=document.getElementById('vsb-qr');if(q)q.remove();}

  function showOK(){
    saveLead(lead);
    var r=document.createElement('div');r.className='vsb-row';
    var av=document.createElement('div');av.className='vsb-mav';av.textContent='VS';
    var box=document.createElement('div');box.className='vsb-ok';
    box.innerHTML='<div class="vsb-ok-ic">\uD83C\uDF89</div>'+
      '<h3>You\'re all set, '+esc(lead.firstName||'there')+'!</h3>'+
      '<p>A licensed VS Health Benefits advisor will reach out within <strong>1 business day</strong> with your personalized plan options.</p>'+
      '<p style="margin-top:8px">Need help sooner?<br><a href="tel:+19548666872">(954) 866-6872</a></p>';
    r.appendChild(av);r.appendChild(box);msgs.appendChild(r);scroll();
    inp.disabled=true;inp.placeholder='Chat complete \u00B7 Call (954) 866-6872';snd.disabled=true;
  }

  var SYS='You are Ava, a warm health insurance specialist for VS Health Benefits (Miami FL, licensed in 40+ states).\n\nMISSION: Qualify visitors through friendly conversation. Collect their info so an advisor can call with a personalized quote.\n\nSTYLE: Warm, short (2-3 sentences), conversational. Use first name once known.\n\nCOLLECT naturally in order:\n1. First name\n2. Coverage type (individual/family, small business, dental/vision)\n3. ZIP or state\n4. Number of people/employees\n5. Age or DOB\n6. Email ("so I can send plan options")\n7. Phone ("so our advisor can call with your quote")\n\nRULES:\n- Never promise instant quote — team will call/email with options\n- Pricing questions: rates vary, advisor covers exact numbers\n- VS Health Benefits questions: answer then redirect to info collection or (954) 866-6872\n- Urgent issues: give (954) 866-6872 immediately\n- Services: Group 10-99, Micro 2-9, ACA/Individual, Family, Dental & Vision, Medicaid\n- Hours: Mon-Fri 8am-6pm ET, Sat-Sun 8am-1pm ET\n\nWHEN you have name + email + phone + coverage type:\nWarmly confirm all collected info and say the team will be in touch within 1 business day.\nThen append at the very end (never shown to user):\n<LEAD_DATA>{"firstName":"","lastName":"","email":"","phone":"","zip":"","state":"","dob":"","coverageType":"","employees":"","extraNotes":""}</LEAD_DATA>';

  function callAI(m){
    return fetch('https://api.anthropic.com/v1/messages',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({model:'claude-sonnet-4-20250514',max_tokens:500,system:SYS,messages:m})
    }).then(function(r){if(!r.ok)throw new Error(r.status);return r.json();})
    .then(function(d){return((d.content||[]).map(function(b){return b.text||'';}).join('')).trim();});
  }

  function start(){
    isBusy=true;showTyp();
    var seed=[{role:'user',content:'Hi, I\'m on the VS Health Benefits website and I\'m interested in health insurance.'}];
    callAI(seed).then(function(r){
      hideTyp();
      history=seed.concat([{role:'assistant',content:r}]);
      addB(r.replace(/<LEAD_DATA>[\s\S]*?<\/LEAD_DATA>/g,'').trim()||'Hi! I\'m Ava from VS Health Benefits. What type of coverage are you looking for?');
      setTimeout(function(){addQR(['Individual / Family','Small Business','Dental & Vision','I have a question']);},200);
    }).catch(function(){
      hideTyp();
      addB('Hi! I\'m Ava from VS Health Benefits \uD83D\uDC4B What type of health coverage are you looking for today?');
      setTimeout(function(){addQR(['Individual / Family','Small Business','Dental & Vision','I have a question']);},200);
    }).finally(function(){isBusy=false;snd.disabled=!inp.value.trim();});
  }

  function turn(userText){
    if(isBusy)return;
    isBusy=true;snd.disabled=true;showTyp();
    callAI(history).then(function(r){
      hideTyp();
      var match=r.match(/<LEAD_DATA>([\s\S]*?)<\/LEAD_DATA>/);
      var disp=r.replace(/<LEAD_DATA>[\s\S]*?<\/LEAD_DATA>/g,'').trim();
      if(match){try{Object.assign(lead,JSON.parse(match[1]));}catch(e){}}
      history.push({role:'assistant',content:r});
      if(match&&!isSubmitted&&lead.email&&lead.phone){
        isSubmitted=true;if(disp)addB(disp);setTimeout(showOK,400);
      }else{
        addB(disp||'I\'m here to help! Could you tell me more about what you\'re looking for?');
      }
    }).catch(function(){
      hideTyp();
      addB('Sorry about that! Please call us at (954) 866-6872 and we\'ll help right away.');
      history.push({role:'assistant',content:'Please call (954) 866-6872.'});
    }).finally(function(){isBusy=false;snd.disabled=!inp.value.trim()||isSubmitted;});
  }

  // Load Firebase then init
  loadScript('https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js',function(){
    loadScript('https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js',function(){
      loadScript('https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore-compat.js',function(){
        initFB();
      });
    });
  });

})();

/* Live Google rating on every page.
   Pages ship with a typed-in fallback ("5.0 from 47 Google reviews"). This script
   asks /api/google-rating for the current numbers and swaps them in. If the
   request fails, the fallback stays, so the badge never goes blank. */
(function(){
  var KEY='vs_gr_v1', TTL=30*60*1000;
  var RX_EN=/(\b)(\d{1,5})(\s+Google reviews)/g, RX_ES=/(\b)(\d{1,5})(\s+rese(?:&ntilde;|ñ)as)/g;
  function apply(d){
    if(!d||!d.count||!d.rating)return;
    var n=String(d.count), r=(Math.round(d.rating*10)/10).toFixed(1);
    var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null), t, hits=[];
    while((t=w.nextNode())){ if(/\d\s+(Google reviews|reseñas)/.test(t.nodeValue))hits.push(t); }
    hits.forEach(function(node){
      node.nodeValue=node.nodeValue.replace(RX_EN,'$1'+n+'$3').replace(RX_ES,'$1'+n+'$3');
      // the bold "5.0" sits right next to the count, inside the same badge
      var box=node.parentNode&&node.parentNode.parentNode;
      if(box)[].forEach.call(box.querySelectorAll('strong'),function(s){if(/^\d\.\d$/.test(s.textContent.trim()))s.textContent=r;});
    });
    [].forEach.call(document.querySelectorAll('[aria-label*="Google reviews"],[aria-label*="reseñas"]'),function(el){
      var a=el.getAttribute('aria-label');
      a=a.replace(RX_EN,'$1'+n+'$3').replace(RX_ES,'$1'+n+'$3').replace(/\b\d\.\d(?= (out of|de) 5)/,r);
      el.setAttribute('aria-label',a);
    });
  }
  function cached(){try{var c=JSON.parse(sessionStorage.getItem(KEY)||'null');if(c&&Date.now()-c.t<TTL)return c.d;}catch(e){}return null;}
  function run(){
    var c=cached(); if(c){apply(c);return;}
    if(!window.fetch)return;
    fetch('/api/google-rating',{headers:{'Accept':'application/json'}}).then(function(r){return r.ok?r.json():null;}).then(function(d){
      if(!d||!d.count)return;
      try{sessionStorage.setItem(KEY,JSON.stringify({t:Date.now(),d:d}));}catch(e){}
      apply(d);
    }).catch(function(){});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
})();

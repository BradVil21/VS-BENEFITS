# -*- coding: utf-8 -*-
"""Let /quote deep-link straight into the small-business path via ?type=business.
Every small-business page can then send traffic to /quote?type=business and land
the visitor on the group form instead of the type chooser."""
F='quote/index.html'
s=open(F,encoding='utf-8').read()
if 'vs-quote-deeplink' in s:
    print('already installed'); raise SystemExit

SNIP = '''
  <script id="vs-quote-deeplink">
  /* Deep-link support: /quote?type=business (aliases: group, employer, smallbusiness)
     lands the visitor directly on the group form. Falls back silently. */
  (function(){
    function go(){
      try{
        var p = new URLSearchParams(window.location.search);
        var t = (p.get('type') || p.get('for') || '').toLowerCase().replace(/[^a-z]/g,'');
        if(!t) return;
        var biz = ['business','group','employer','smallbusiness','company'];
        var ind = ['individual','family','personal','self'];
        var pick = biz.indexOf(t) > -1 ? 'business' : (ind.indexOf(t) > -1 ? 'individual' : null);
        if(!pick || typeof window.selectType !== 'function') return;
        window.selectType(pick);
        var el = document.getElementById('progressWrap') ||
                 document.getElementById(pick === 'business' ? 'typeBusiness' : 'typeIndividual');
        if(el && el.scrollIntoView) setTimeout(function(){
          el.scrollIntoView({behavior:'smooth', block:'start'});
        }, 420);
      }catch(e){}
    }
    if(document.readyState === 'loading'){
      document.addEventListener('DOMContentLoaded', go);
    } else { go(); }
  })();
  </script>
'''
s = s.replace('</body>', SNIP + '</body>', 1)
open(F,'w',encoding='utf-8').write(s)
print('installed deep-link handler on /quote')

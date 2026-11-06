import re,sys
def sy(y): return round(30+(y-30)*1.2)
ST={"FL":(760,400),"GA":(700,330),"AL":(650,335),"MS":(603,345),"LA":(560,378),"TN":(608,272),"KY":(672,238),"IN":(645,196),"IL":(583,208),
    "IA":(520,172),"NE":(430,182),"CO":(348,226),"UT":(245,192),"NV":(160,182),"CA":(92,228),"AZ":(212,304),"NM":(320,312),"TX":(442,372)}
NAMES_EN={"FL":"Florida","GA":"Georgia","AL":"Alabama","MS":"Mississippi","LA":"Louisiana","TN":"Tennessee","KY":"Kentucky","IN":"Indiana","IL":"Illinois","IA":"Iowa","NE":"Nebraska","CO":"Colorado","UT":"Utah","NV":"Nevada","CA":"California","AZ":"Arizona","NM":"New Mexico","TX":"Texas"}
NAMES_ES=dict(NAMES_EN,MS="Misisipi",LA="Luisiana",NM="Nuevo México")
labels=''.join(f'<text data-st="{k}" x="{x}" y="{sy(y)}">{k}</text>' for k,(x,y) in ST.items())
CSS='''
.trm-map{position:relative}
.trm-states text{fill:#4b5263;font:800 17px Inter,system-ui,sans-serif;text-anchor:middle;letter-spacing:.04em;transition:fill .35s}
.trm-states text.on{fill:#fbbf24}
.trm-states text.done{fill:#8a6a1a}
.trm-badge{position:absolute;left:4px;top:4px;background:rgba(17,17,17,.92);border:1px solid #2a2f3a;border-radius:12px;padding:8px 12px;color:#fff;font:600 12px Inter,system-ui,sans-serif;line-height:1.35;pointer-events:none;min-width:150px}
.trm-badge small{display:block;color:#9ca3af;font-size:10px;letter-spacing:.12em;text-transform:uppercase}
.trm-badge b{display:block;font:800 17px Poppins,Inter,sans-serif;color:#fbbf24}
.trm-badge i{font-style:normal;color:#5eead4}
@media(max-width:860px){.trm-states text{font-size:24px}.trm-badge{font-size:11px;padding:6px 10px;min-width:0}.trm-badge b{font-size:15px}}
'''
def JS(names,lang):
    t=dict(en=("Now driving through","states crossed","In network ✓"),es=("Ahora pasando por","estados cruzados","Dentro de la red ✓"))[lang]
    import json
    return '''<script>(function(){var N=%s,T=%s;
var SEG=[["FL","GA"],["GA","TN"],["TN","KY","IN","IL"],["IL","IA","NE","CO"],["CO","UT","NV","CA"],["CA","AZ"],["AZ","NM","TX"],["TX","LA","MS","AL","GA"],["GA","FL"]];
var CITY=[[790,528],[690,354],[640,306],[620,186],[330,234],[105,336],[210,390],[470,402],[690,354],[790,528]];
function init(map){var svg=map.querySelector("svg"),path=svg&&svg.querySelector(".trm-route"),mv=svg&&svg.querySelector(".trm-mover");if(!path||!mv)return;
 var L=path.getTotalLength(),b=document.createElement("div");b.className="trm-badge";b.setAttribute("aria-hidden","true");map.appendChild(b);
 var marks=[0],from=0;for(var c=1;c<CITY.length;c++){if(c===CITY.length-1){marks.push(L);break;}var best=1e9,bl=from;for(var s=from;s<=L;s+=2){var p=path.getPointAtLength(s),d=(p.x-CITY[c][0])*(p.x-CITY[c][0])+(p.y-CITY[c][1])*(p.y-CITY[c][1]);if(d<best){best=d;bl=s;}if(d>best+40000&&best<400)break;}marks.push(bl);from=bl+5;}
 var labels={};svg.querySelectorAll(".trm-states text").forEach(function(e){labels[e.getAttribute("data-st")]=e;});
 var DUR=24000,last="",seen={},t0=null,reduce=false;try{reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;}catch(e){}
 function stateAt(len){for(var i=0;i<SEG.length;i++){if(len<=marks[i+1]){var f=(len-marks[i])/Math.max(1,marks[i+1]-marks[i]),seg=SEG[i];return seg[Math.min(seg.length-1,Math.floor(f*seg.length))];}}return "FL";}
 function draw(len){var p=path.getPointAtLength(len),q=path.getPointAtLength(Math.min(L,len+3));if(len>L-3)q=path.getPointAtLength(L),p=path.getPointAtLength(L-3);
  var a=Math.atan2(q.y-p.y,q.x-p.x)*180/Math.PI;mv.setAttribute("transform","translate("+p.x.toFixed(1)+" "+p.y.toFixed(1)+") rotate("+a.toFixed(1)+")");
  var st=stateAt(len);if(st!==last){if(last&&labels[last]){labels[last].classList.remove("on");labels[last].classList.add("done");}if(labels[st]){labels[st].classList.add("on");labels[st].classList.remove("done");}seen[st]=1;last=st;
   b.innerHTML="<small>"+T[0]+"</small><b>"+N[st]+"</b>"+Object.keys(seen).length+" "+T[1]+" · <i>"+T[2]+"</i>";}}
 if(reduce){draw(marks[3]);return;}
 function loop(ts){if(t0===null)t0=ts;var f=((ts-t0)%%DUR)/DUR;if(f<0.004&&Object.keys(seen).length>2){seen={};Object.keys(labels).forEach(function(k){labels[k].classList.remove("done");});}draw(f*L);requestAnimationFrame(loop);}
 requestAnimationFrame(loop);}
function go(){document.querySelectorAll(".trm-map").forEach(init);}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",go);else go();})();</script>''' % (json.dumps(names,ensure_ascii=False),json.dumps(t,ensure_ascii=False))
for f,lang in [('truck-driver-health-insurance.html','en'),('trucking-health-quote.html','en'),('seguro-medico-camioneros.html','es')]:
    s=open(f).read()
    if 'trm-mover' in s: print(f,'already'); continue
    s,n1=re.subn(r'<g><ellipse (rx="34"[^>]*/>)(<g id="trm-truck".*?</g>)<animateMotion[^>]*/></g>',r'<g class="trm-mover" transform="translate(790 528)"><ellipse \1\2</g>',s,flags=re.S)
    s,n2=re.subn(r'(<g class="trm-pin">)',lambda m:'<g class="trm-states">'+labels+'</g>'+m.group(1),s,count=1)
    s,n3=re.subn(r'(<style id="trm-css">)',r'\1'+CSS.replace('\\','\\\\'),s,count=1)
    s=s.replace('</body>',JS(NAMES_ES if lang=='es' else NAMES_EN,lang)+'\n</body>',1)
    open(f,'w').write(s); print(f,n1,n2,n3)

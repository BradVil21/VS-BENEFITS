/* ============================ GOOGLE ADS PERFORMANCE ============================
   Fed by the Google Ads Script (google-ads/vs-ads-sync-script.js) -> /api/ads-sync
   -> Firestore vs_state/ads_perf -> onSnapshot in initCloud. Re-renders live. */
var ADS_RANGE_KEY="vs_ads_range";
function adsSnap(){
  if(window.__vsAdsPerf)return window.__vsAdsPerf;
  try{var s=JSON.parse(localStorage.getItem("vs_ads_perf")||"null");return s;}catch(e){return null;}
}
function adsMoney(n){n=+n||0;return "$"+(n>=1000?Math.round(n).toLocaleString():n.toFixed(2));}
function adsPct(n){return isFinite(n)?(Math.round(n*1000)/10)+"%":"–";}
function adsDiv(a,b){return b?a/b:NaN;}
function adsIsGoogle(x){
  var a=(x&&x.attribution)||{};var s=((x&&x.source)||"")+" "+(a.source||"")+" "+(a.lastSource||"");
  return /google ads/i.test(s)||!!a.gclid||(a.utm_source==="google"&&a.utm_medium==="cpc");
}
function adsDayMs(d){var p=String(d||"").split("-");return new Date(+p[0],(+p[1]||1)-1,+p[2]||1).getTime();}
function renderAdsPerf(){
  var mount=$("ads-mount");if(!mount)return;
  var S=adsSnap();
  mount.innerHTML="";
  if(!S||!S.daily){
    mount.appendChild(el("div",{class:"an-section"},[
      el("h4",{text:"Connect Google Ads"}),
      el("p",{class:"sub",html:"No Google Ads data has arrived yet. Setup takes about 5 minutes and then this page refreshes itself every hour:"}),
      el("ol",{class:"ads-steps",html:"<li>In Vercel &rarr; Project &rarr; Settings &rarr; Environment Variables, add <code>ADS_SYNC_SECRET</code> (any long random value) and redeploy.</li><li>In Google Ads &rarr; Tools &rarr; Bulk actions &rarr; Scripts, create a new script and paste <code>google-ads/vs-ads-sync-script.js</code>. Put the same secret in <code>SECRET</code>.</li><li>Authorize, click <strong>Preview</strong> (the log should say <em>Sync 200</em>), then set Frequency to <strong>Hourly</strong>.</li>"})
    ]));
    return;
  }
  var range=30;try{range=+localStorage.getItem(ADS_RANGE_KEY)||30;}catch(e){}
  var endMs=adsDayMs(S.range&&S.range.end)||Date.now(), startMs=endMs-(range-1)*864e5;
  var prevStart=startMs-range*864e5;
  var inR=function(d){var t=adsDayMs(d);return t>=startMs&&t<=endMs;};
  var inP=function(d){var t=adsDayMs(d);return t>=prevStart&&t<startMs;};
  function sum(rows){var o={imp:0,clk:0,cost:0,conv:0};rows.forEach(function(r){o.imp+=+r.imp||0;o.clk+=+r.clk||0;o.cost+=+r.cost||0;o.conv+=+r.conv||0;});return o;}
  var cur=sum(S.daily.filter(function(r){return inR(r.d);})), prev=sum(S.daily.filter(function(r){return inP(r.d);}));

  // Portal side: the leads Google Ads actually produced, and what became of them.
  var leads=(typeof getLeads==="function"?getLeads():[]).filter(adsIsGoogle).map(function(l){return {t:l.created||0,q:/quoted|sold|enrolled|appointment/.test(l.status||""),s:/sold|enrolled/.test(l.status||""),biz:false,camp:(l.attribution||{}).utm_campaign||""};});
  var biz=(typeof getBizLeads==="function"?getBizLeads():[]).filter(adsIsGoogle).map(function(b){return {t:b.created||0,q:/meeting|proposal|won/.test(b.stage||""),s:b.stage==="won",biz:true,camp:(b.attribution||{}).utm_campaign||""};});
  var all=leads.concat(biz), endOfDay=endMs+864e5;
  var pl=all.filter(function(x){return x.t>=startMs&&x.t<endOfDay;});
  var plQ=pl.filter(function(x){return x.q;}).length, plS=pl.filter(function(x){return x.s;}).length;

  // Header: freshness + range picker
  var age=Date.now()-(S.syncedAt||0), stale=age>3*36e5;
  var head=el("div",{class:"ads-head"});
  head.appendChild(el("div",{class:"ads-sync"+(stale?" stale":""),html:(stale?"&#9888; ":"&#9679; ")+"Synced "+(age<36e5?Math.max(1,Math.round(age/6e4))+" min ago":Math.round(age/36e5)+" h ago")+" &middot; "+(S.account&&S.account.name||"Google Ads")+" ("+(S.account&&S.account.id||"")+")"}));
  var pick=el("div",{class:"ads-range"});
  [7,14,30,60].forEach(function(n){var b=el("button",{type:"button",class:n===range?"on":"",text:n+"d"});b.addEventListener("click",function(){try{localStorage.setItem(ADS_RANGE_KEY,n);}catch(e){}renderAdsPerf();});pick.appendChild(b);});
  head.appendChild(pick);mount.appendChild(head);

  // KPIs
  function delta(a,b,lowerIsBetter){if(!b||!isFinite(a)||!isFinite(b))return "";var d=(a-b)/b;var good=lowerIsBetter?d<0:d>0;return '<span class="ads-d '+(Math.abs(d)<.02?"":good?"up":"down")+'">'+(d>=0?"&#9650; ":"&#9660; ")+Math.abs(Math.round(d*100))+"%</span>";}
  var cpl=adsDiv(cur.cost,cur.conv), pcpl=adsDiv(prev.cost,prev.conv), realCpl=adsDiv(cur.cost,pl.length), cps=adsDiv(cur.cost,plS);
  var kp=el("div",{class:"an-kpis ads-kpis"});
  [["Spend",adsMoney(cur.cost),delta(cur.cost,prev.cost)],
   ["Clicks",String(cur.clk),delta(cur.clk,prev.clk)],
   ["CTR",adsPct(adsDiv(cur.clk,cur.imp)),delta(adsDiv(cur.clk,cur.imp),adsDiv(prev.clk,prev.imp))],
   ["Avg CPC",isFinite(adsDiv(cur.cost,cur.clk))?adsMoney(cur.cost/cur.clk):"–",delta(adsDiv(cur.cost,cur.clk),adsDiv(prev.cost,prev.clk),true)],
   ["Ads conversions",String(Math.round(cur.conv*10)/10),delta(cur.conv,prev.conv)],
   ["Cost / conversion",isFinite(cpl)?adsMoney(cpl):"–",delta(cpl,pcpl,true)],
   ["Leads in portal",String(pl.length),""],
   ["Cost / real lead",isFinite(realCpl)?adsMoney(realCpl):"–",""],
   ["Quoted",String(plQ),""],
   ["Sold",String(plS)+(isFinite(cps)?" &middot; "+adsMoney(cps)+" each":""),""]
  ].forEach(function(k){kp.appendChild(el("div",{class:"an-kpi"},[el("div",{class:"n",html:k[1]}),el("div",{class:"l",html:k[0]+" "+k[2]})]));});
  mount.appendChild(kp);
  mount.appendChild(el("p",{class:"ads-fine",text:"Change vs the previous "+range+" days. \u201cLeads in portal\u201d counts Pipeline and Business Leads cards whose source is Google Ads, so it shows what the ad spend actually produced, including quotes and sales Google can't see."}));

  // Insights
  var tips=[];
  if(stale)tips.push(["warn","No sync in "+Math.round(age/36e5)+" hours. Check Google Ads \u2192 Tools \u2192 Scripts for errors."]);
  if(S.policy&&(S.policy.disapproved||S.policy.limited))tips.push(["bad",(S.policy.disapproved||0)+" disapproved and "+(S.policy.limited||0)+" limited ads. Open Policy manager in Google Ads (health insurance certification may be needed)."]);
  (S.campaigns||[]).forEach(function(c){if(c.status==="ENABLED"&&/LIMITED|NOT_ELIGIBLE/.test(c.primary||""))tips.push(["warn","Campaign \u201c"+c.name+"\u201d is "+String(c.primary).toLowerCase().replace(/_/g," ")+(c.reasons?" ("+String(c.reasons).toLowerCase().replace(/_/g," ")+")":"")+"."]);});
  var avgCpc=adsDiv(cur.cost,cur.clk)||5;
  var waste=(S.terms||[]).filter(function(t){return !(+t.conv)&&(+t.cost)>=Math.max(10,2*avgCpc);}).sort(function(a,b){return b.cost-a.cost;});
  if(waste.length){var w=waste.reduce(function(s,t){return s+(+t.cost);},0);tips.push(["bad",adsMoney(w)+" spent in 30 days on "+waste.length+" search term"+(waste.length>1?"s":"")+" with no conversions. Review them below and add the irrelevant ones as negatives."]);}
  var ag=(S.adGroups||[]).filter(function(g){return g.conv>=1;}).map(function(g){g.cpa=g.cost/g.conv;return g;}).sort(function(a,b){return a.cpa-b.cpa;});
  if(ag.length>=2&&ag[ag.length-1].cpa>ag[0].cpa*1.5)tips.push(["good","\u201c"+ag[0].g+"\u201d converts at "+adsMoney(ag[0].cpa)+" vs "+adsMoney(ag[ag.length-1].cpa)+" for \u201c"+ag[ag.length-1].g+"\u201d. Shift budget toward the cheaper ad group."]);
  if(cur.conv>=3&&pl.length<cur.conv*0.5)tips.push(["warn","Google counts "+Math.round(cur.conv)+" conversions but only "+pl.length+" Google Ads leads reached the portal. Calls are counted by Google but not as portal leads; if this gap is mostly forms, check the lead tracking."]);
  var lowQs=(S.keywords||[]).filter(function(k){return k.qs&&k.qs<=4&&k.cost>0;});
  if(lowQs.length)tips.push(["warn",lowQs.length+" keyword"+(lowQs.length>1?"s have":" has")+" a Quality Score of 4 or less: "+lowQs.slice(0,3).map(function(k){return "\u201c"+k.kw+"\u201d";}).join(", ")+". Tighten the ad text and landing page for these, or pause them."]);
  var hrs=(S.hours||[]).slice().sort(function(a,b){return b.conv-a.conv;});
  var hTot=hrs.reduce(function(s,h){return s+(+h.conv||0);},0);
  if(hTot>=10){var fmt=function(h){h=+h;return (h%12||12)+(h<12?"am":"pm");};tips.push(["good","Most conversions come at "+hrs.slice(0,3).map(function(h){return fmt(h.h);}).join(", ")+". Consider a bid increase for those hours."]);}
  if(!tips.length)tips.push(["good","Nothing needs attention right now."]);
  var ins=el("div",{class:"an-section"});ins.appendChild(el("h4",{text:"What to do next"}));
  tips.forEach(function(t){ins.appendChild(el("div",{class:"ads-tip "+t[0],html:'<span class="ads-ico">'+(t[0]==="good"?"&#10003;":t[0]==="bad"?"&#10005;":"!")+"</span><span>"+t[1].replace(/</g,"&lt;")+"</span>"}));});
  mount.appendChild(ins);

  // Daily charts (single series each, one scale each; never dual-axis)
  var days=[];for(var t=startMs;t<=endMs;t+=864e5){var dd=new Date(t);days.push({k:dd.getFullYear()+"-"+String(dd.getMonth()+1).padStart(2,"0")+"-"+String(dd.getDate()).padStart(2,"0"),lab:(dd.getMonth()+1)+"/"+dd.getDate(),cost:0,clk:0,conv:0,leads:0});}
  var idx={};days.forEach(function(d,i){idx[d.k]=i;});
  S.daily.forEach(function(r){var i=idx[r.d];if(i!=null){days[i].cost+=+r.cost||0;days[i].clk+=+r.clk||0;days[i].conv+=+r.conv||0;}});
  pl.forEach(function(x){var dd=new Date(x.t);var k=dd.getFullYear()+"-"+String(dd.getMonth()+1).padStart(2,"0")+"-"+String(dd.getDate()).padStart(2,"0");if(idx[k]!=null)days[idx[k]].leads++;});
  function chart(title,sub,key,fmt){
    var sec=el("div",{class:"an-section"});sec.appendChild(el("h4",{text:title}));sec.appendChild(el("p",{class:"sub",text:sub}));
    var max=Math.max.apply(null,days.map(function(d){return d[key];}))||1;
    var wrap=el("div",{class:"ads-bars"});
    var tip=el("div",{class:"ads-tt"});
    days.forEach(function(d,i){
      var col=el("div",{class:"ads-bcol"});
      var bar=el("div",{class:"ads-bar"});bar.style.height=(d[key]?Math.max(3,Math.round(d[key]/max*120)):0)+"px";
      col.appendChild(bar);
      if(days.length<=14||i%Math.ceil(days.length/10)===0)col.appendChild(el("div",{class:"ads-bl",text:d.lab}));
      col.addEventListener("mouseenter",function(){tip.innerHTML="<b>"+d.lab+"</b><br>Spend "+adsMoney(d.cost)+"<br>Clicks "+d.clk+"<br>Ads conversions "+(Math.round(d.conv*10)/10)+"<br>Portal leads "+d.leads;tip.style.display="block";tip.style.left=Math.min(col.offsetLeft,wrap.clientWidth-170)+"px";});
      col.addEventListener("mouseleave",function(){tip.style.display="none";});
      wrap.appendChild(col);
    });
    var holder=el("div",{class:"ads-chart"});holder.appendChild(el("div",{class:"ads-max",text:fmt(max)}));holder.appendChild(wrap);holder.appendChild(tip);
    sec.appendChild(holder);return sec;
  }
  var two=el("div",{class:"ads-two"});
  two.appendChild(chart("Daily spend","Hover a day for clicks, conversions and portal leads.","cost",adsMoney));
  two.appendChild(chart("Daily conversions (Google Ads)","Form leads and calls Google Ads counted.","conv",function(n){return String(Math.round(n*10)/10);}));
  mount.appendChild(two);

  // Tables
  function table(title,sub,cols,rows,empty){
    var sec=el("div",{class:"an-section"});sec.appendChild(el("h4",{text:title}));if(sub)sec.appendChild(el("p",{class:"sub",html:sub}));
    if(!rows.length){sec.appendChild(el("div",{class:"an-empty",text:empty||"No data yet."}));return sec;}
    var h="<div class='an-tablewrap'><table class='ads-t'><thead><tr>"+cols.map(function(c){return "<th"+(c[2]?" class='r'":"")+">"+c[0]+"</th>";}).join("")+"</tr></thead><tbody>";
    rows.forEach(function(r){h+="<tr"+(r.__cls?" class='"+r.__cls+"'":"")+">"+cols.map(function(c){var v=c[1](r);return "<td"+(c[2]?" class='r'":"")+">"+(v==null?"":String(v).replace(/</g,"&lt;"))+"</td>";}).join("")+"</tr>";});
    sec.appendChild(el("div",{html:h+"</tbody></table></div>"}));return sec;
  }
  var M=[["Clicks",function(r){return r.clk;},1],["CTR",function(r){return adsPct(adsDiv(r.clk,r.imp));},1],["Spend",function(r){return adsMoney(r.cost);},1],["Conv.",function(r){return Math.round(r.conv*10)/10;},1],["Cost / conv.",function(r){return r.conv?adsMoney(r.cost/r.conv):"–";},1]];
  // Campaign table follows the selected range (built from daily rows)
  var cm={};S.daily.filter(function(r){return inR(r.d);}).forEach(function(r){var o=cm[r.c]||(cm[r.c]={name:r.c,imp:0,clk:0,cost:0,conv:0});o.imp+=+r.imp||0;o.clk+=+r.clk||0;o.cost+=+r.cost||0;o.conv+=+r.conv||0;});
  var meta={};(S.campaigns||[]).forEach(function(c){meta[c.name]=c;});
  var camps=Object.keys(cm).map(function(k){return cm[k];}).sort(function(a,b){return b.cost-a.cost;});
  mount.appendChild(table("Campaigns","Last "+range+" days.",[["Campaign",function(r){return r.name;}],["Status",function(r){var m=meta[r.name]||{};return String(m.primary||m.status||"").toLowerCase().replace(/_/g," ");}],["Budget/day",function(r){var m=meta[r.name];return m&&m.budget?adsMoney(m.budget):"";},1]].concat(M),camps,"No campaign spend in this range."));
  mount.appendChild(table("Ad groups","Last 30 days.",[["Ad group",function(r){return r.g;}],["Campaign",function(r){return r.c;}]].concat(M),(S.adGroups||[]).filter(function(r){return r.imp>0;}).sort(function(a,b){return b.cost-a.cost;})));
  var termRows=(S.terms||[]).slice(0,40).map(function(t){var o=Object.assign({},t);if(!(+t.conv)&&(+t.cost)>=Math.max(10,2*avgCpc))o.__cls="waste";else if(+t.conv)o.__cls="win";return o;});
  var termSec=table("Search terms","Last 30 days, by spend. <span class='ads-key waste'>Red</span> = spend with no conversions (negative keyword candidate). <span class='ads-key win'>Green</span> = converting (add as exact match).",[["Search term",function(r){return r.term;}],["Ad group",function(r){return r.g;}]].concat(M),termRows,"No search terms yet.");
  if(waste.length){var cp=el("button",{type:"button",class:"btn btn-sm ads-copy",text:"Copy "+waste.length+" red terms as a negative list"});cp.addEventListener("click",function(){var txt=waste.map(function(t){return "\""+t.term+"\"";}).join("\n");try{navigator.clipboard.writeText(txt);cp.textContent="Copied. Paste into Google Ads \u2192 Negative keywords";}catch(e){cp.textContent="Copy failed";}});termSec.insertBefore(cp,termSec.children[2]||null);}
  mount.appendChild(termSec);
  mount.appendChild(table("Keywords","Last 30 days, top by spend.",[["Keyword",function(r){return r.kw;}],["Match",function(r){return String(r.mt||"").toLowerCase();}],["QS",function(r){return r.qs||"–";},1]].concat(M),(S.keywords||[]).slice(0,30)));
  var byCamp={};pl.forEach(function(x){var k=x.camp||"(no utm_campaign)";var o=byCamp[k]||(byCamp[k]={k:k,n:0,q:0,s:0,biz:0});o.n++;if(x.q)o.q++;if(x.s)o.s++;if(x.biz)o.biz++;});
  mount.appendChild(table("Portal leads from Google Ads","Last "+range+" days, by the campaign tag on the ad's URL.",[["Campaign tag",function(r){return r.k;}],["Leads",function(r){return r.n;},1],["Business",function(r){return r.biz;},1],["Quoted",function(r){return r.q;},1],["Sold",function(r){return r.s;},1]],Object.keys(byCamp).map(function(k){return byCamp[k];}).sort(function(a,b){return b.n-a.n;}),"No Google Ads leads in this range yet."));
  var dv=(S.devices||[]).slice().sort(function(a,b){return b.cost-a.cost;});
  mount.appendChild(table("Devices","Last 30 days.",[["Device",function(r){return String(r.dev||"").toLowerCase().replace(/_/g," ");}]].concat(M),dv));
}

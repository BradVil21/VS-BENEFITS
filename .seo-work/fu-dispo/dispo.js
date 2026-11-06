/* ── Follow-ups: click a name -> quick disposition pop-up (Nov 2026) ──
   Pick what happened, optionally move the lead to a pipeline stage, set the next
   follow-up, add a note, Save. "Open full profile" still opens the contact editor. */
var FUD_OUT=[
  {k:"noanswer",l:"No answer",ico:"☎",days:2},
  {k:"voicemail",l:"Left voicemail",ico:"✉",days:2},
  {k:"talked",l:"Talked, follow up later",ico:"✔",days:7},
  {k:"appt",l:"Appointment set",ico:"📅",stage:"appointment_scheduled",days:0},
  {k:"quoted",l:"Sent a quote",ico:"$",stage:"quoted",days:3},
  {k:"sold",l:"Sold",ico:"★",stage:"sold"},
  {k:"notint",l:"Not interested",ico:"✕",stage:"no_longer_interested"},
  {k:"bad",l:"Wrong number / bad lead",ico:"⚠",stage:"disqualified"},
  {k:"done",l:"Done, no more follow-up",ico:"✓",days:-1}
];
function czFudClose(){var m=document.getElementById("fud-modal");if(m)m.remove();document.removeEventListener("keydown",czFudKey);}
function czFudKey(e){if(e.key==="Escape")czFudClose();}
function czFudOpen(id){
  var c=getLeads().filter(function(x){return x.id===id;})[0];if(!c)return;
  czFudClose();
  var tel=c.phone?String(c.phone).replace(/[^0-9+]/g,""):"";
  var fu=czFU(c);
  var stOpts='<option value="">Keep in '+escapeHtml(czMETA[c.stage]?czMETA[c.stage].label:"current stage")+'</option>'
    +czSTAGES.filter(function(s){return s.id!==c.stage;}).map(function(s){return '<option value="'+s.id+'">'+escapeHtml(s.label)+'</option>';}).join("");
  var m=document.createElement("div");m.id="fud-modal";m.className="fud-back";
  m.innerHTML='<div class="fud" role="dialog" aria-modal="true" aria-labelledby="fud-t">'
    +'<div class="fud-h"><div><div class="fud-t" id="fud-t">'+escapeHtml(czName(c))+'</div>'
    +'<div class="fud-meta"><span class="cz-chip" style="'+czChipStyle(c.stage)+'">'+escapeHtml(czMETA[c.stage]?czMETA[c.stage].label:"")+'</span>'
    +(tel?'<a href="tel:'+escapeHtml(tel)+'" class="fud-ph">'+escapeHtml(c.phone)+'</a>':'<span class="fud-faint">no phone</span>')
    +'<span class="fud-faint">Last contact: '+(c.lastContact?czPretty(c.lastContact):"never")+'</span>'
    +(fu.label?'<span class="cz-pill" style="'+czFUSTYLE[fu.key]+'">'+fu.label+'</span>':'')+'</div></div>'
    +'<button type="button" class="fud-x" data-fud="close" aria-label="Close">✕</button></div>'
    +'<div class="fud-l">What happened?</div><div class="fud-outs">'
    +FUD_OUT.map(function(o){return '<button type="button" class="fud-o" data-fud-out="'+o.k+'"><span>'+o.ico+'</span>'+o.l+'</button>';}).join("")+'</div>'
    +'<div class="fud-row"><label class="fud-f"><span class="fud-l">Move to pipeline stage</span><select id="fud-stage">'+stOpts+'</select></label>'
    +'<div class="fud-f" id="fud-nextwrap"><span class="fud-l">Next follow-up</span><div class="fud-days">'
    +[["2","2 days"],["7","1 week"],["14","2 weeks"],["30","30 days"],["90","90 days"]].map(function(d){return '<button type="button" class="fud-d" data-fud-days="'+d[0]+'">'+d[1]+'</button>';}).join("")
    +'</div><input type="date" id="fud-date" class="fud-date" value="'+escapeHtml(c.followUpDue||"")+'"/></div></div>'
    +'<div class="fud-f" id="fud-apptwrap" hidden><span class="fud-l">Appointment date &amp; time</span><input type="datetime-local" id="fud-appt" class="fud-date"/></div>'
    +'<label class="fud-f"><span class="fud-l">Note (optional)</span><textarea id="fud-note" rows="2" placeholder="e.g. wants a PPO, call back after 5pm"></textarea></label>'
    +'<div class="fud-foot"><button type="button" class="fud-prof" data-fud="profile">Open full profile</button>'
    +'<span class="fud-err" id="fud-err"></span><button type="button" class="fud-save" data-fud="save">Save</button></div></div>';
  document.body.appendChild(m);
  document.addEventListener("keydown",czFudKey);
  var sel=null;
  var $q=function(s){return m.querySelector(s);};
  function setDays(n){
    m.querySelectorAll(".fud-d").forEach(function(b){b.classList.toggle("on",String(n)===b.getAttribute("data-fud-days"));});
    $q("#fud-date").value=n>0?czAddDays(todayStr(),n):"";
  }
  function syncStage(){
    var st=$q("#fud-stage").value||c.stage;
    var closed=czCLOSED.indexOf(st)>=0||(sel&&sel.k==="done");
    $q("#fud-nextwrap").style.opacity=closed?".4":"";
    $q("#fud-nextwrap").style.pointerEvents=closed?"none":"";
    $q("#fud-apptwrap").hidden=st!=="appointment_scheduled";
  }
  m.addEventListener("click",function(e){if(e.target===m)czFudClose();});
  m.querySelectorAll("[data-fud-out]").forEach(function(b){b.addEventListener("click",function(){
    sel=FUD_OUT.filter(function(o){return o.k===b.getAttribute("data-fud-out");})[0];
    m.querySelectorAll(".fud-o").forEach(function(x){x.classList.toggle("on",x===b);});
    $q("#fud-stage").value=(sel.stage&&sel.stage!==c.stage)?sel.stage:"";
    if(sel.days>0)setDays(sel.days);else setDays(0);
    $q("#fud-err").textContent="";syncStage();
  });});
  m.querySelectorAll("[data-fud-days]").forEach(function(b){b.addEventListener("click",function(){setDays(parseInt(b.getAttribute("data-fud-days"),10));});});
  $q("#fud-date").addEventListener("change",function(){m.querySelectorAll(".fud-d").forEach(function(b){b.classList.remove("on");});});
  $q("#fud-stage").addEventListener("change",syncStage);
  $q("[data-fud=close]").addEventListener("click",czFudClose);
  $q("[data-fud=profile]").addEventListener("click",function(){czFudClose();var cc=getLeads().filter(function(x){return x.id===id;})[0];if(cc)czOpenModal(cc);});
  $q("[data-fud=save]").addEventListener("click",function(){
    var newStage=$q("#fud-stage").value,note=$q("#fud-note").value.trim(),next=$q("#fud-date").value,appt=$q("#fud-appt").value;
    if(!sel&&!newStage&&!note){$q("#fud-err").textContent="Pick what happened (or a stage).";return;}
    var stage=newStage||c.stage,closed=czCLOSED.indexOf(stage)>=0||(sel&&sel.k==="done");
    if(stage==="appointment_scheduled"&&newStage&&!appt&&sel&&sel.k==="appt"){$q("#fud-err").textContent="Add the appointment date and time.";return;}
    var arr=getLeads();var r=arr.filter(function(x){return x.id===id;})[0];if(!r){czFudClose();return;}
    var t=todayStr();
    r.lastContact=t;r.updated=Date.now();
    if(closed){r.followUpDue="";r.fuCleared=true;}
    else if(next){r.followUpDue=next;r.fuCleared=false;}
    var line=(sel?sel.l:"Updated")+(newStage?" → "+(czMETA[newStage]?czMETA[newStage].label:newStage):"")
      +(!closed&&next?" · next follow-up "+czPretty(next):"")+(note?" — "+note:"");
    czStampNote(r,line);
    saveLeads(arr);
    if(typeof addLeadActivity==="function")addLeadActivity(id,"followup",line);
    if(newStage&&newStage!==c.stage)czSetStage(id,newStage);
    if(appt&&stage==="appointment_scheduled"&&typeof czSetApptDate==="function")czSetApptDate(id,appt);
    czFudClose();czCurrentRender();if(typeof renderTasks==="function")renderTasks();
    if(typeof toast==="function")try{toast("Saved: "+czName(r));}catch(e){}
  });
}
function czFudBind(box){
  box.querySelectorAll("[data-fud-open]").forEach(function(n){n.addEventListener("click",function(e){
    if(e.target.closest("a,button,select,input,textarea,.fuq-disp"))return;
    e.stopPropagation();czFudOpen(n.getAttribute("data-fud-open"));
  });});
}
(function(){try{var st=document.createElement("style");st.setAttribute("data-fud","1");st.textContent=[
".fud-back{position:fixed;inset:0;background:rgba(13,27,42,.5);z-index:9000;display:flex;align-items:flex-start;justify-content:center;padding:6vh 16px;overflow:auto}",
".fud{background:#fff;border-radius:18px;width:100%;max-width:600px;padding:20px 22px;box-shadow:0 24px 60px rgba(13,27,42,.3);font-size:14px;color:#0f172a}",
".fud-h{display:flex;justify-content:space-between;gap:12px;margin-bottom:14px}",
".fud-t{font-size:20px;font-weight:800;color:#0b2346}",
".fud-meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:6px;font-size:13px}",
".fud-ph{font-weight:700;color:#0a7a4f;text-decoration:none}.fud-faint{color:#94a3b8}",
".fud-x{border:0;background:none;font-size:18px;color:#94a3b8;cursor:pointer;padding:4px 8px;border-radius:8px;height:fit-content}.fud-x:hover{background:#f1f5f9;color:#334155}",
".fud-l{display:block;font-size:11.5px;font-weight:800;text-transform:uppercase;letter-spacing:.05em;color:#64748b;margin:0 0 6px}",
".fud-outs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-bottom:16px}",
".fud-o{display:flex;align-items:center;gap:8px;text-align:left;font:inherit;font-size:13px;font-weight:700;padding:10px 12px;border:1px solid #dbe3ef;border-radius:12px;background:#fff;color:#1e293b;cursor:pointer;min-height:44px}",
".fud-o span{width:22px;flex:none;text-align:center;color:#16447f}",
".fud-o:hover{border-color:#9dbbe8;background:#f6f9fe}.fud-o.on{border-color:#16447f;background:#eaf2fd;box-shadow:0 0 0 1px #16447f inset}",
".fud-row{display:grid;grid-template-columns:1fr 1.3fr;gap:14px;margin-bottom:14px}",
".fud-f{display:block;margin-bottom:12px}",".fud-f[hidden]{display:none!important}",
".fud select,.fud textarea,.fud-date{width:100%;font:inherit;font-size:14px;border:1px solid #d8e0ee;border-radius:10px;padding:9px 11px;background:#fff;color:#0f172a;box-sizing:border-box}",
".fud-days{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}",
".fud-d{font:inherit;font-size:12.5px;font-weight:700;border:1px solid #d8e0ee;border-radius:999px;padding:5px 10px;background:#fff;color:#334155;cursor:pointer}.fud-d.on{background:#16447f;border-color:#16447f;color:#fff}",
".fud-foot{display:flex;align-items:center;gap:10px;margin-top:6px}",
".fud-prof{border:0;background:none;color:#16447f;font:inherit;font-weight:700;cursor:pointer;padding:8px 0}",
".fud-err{flex:1;text-align:right;color:#e11d48;font-size:13px;font-weight:600}",
".fud-save{font:inherit;font-weight:800;border:0;border-radius:999px;background:#0a7a4f;color:#fff;padding:11px 26px;cursor:pointer}.fud-save:hover{background:#086640}",
"html.dark .fud{background:#111d2b;color:#e6edf6}html.dark .fud-t{color:#f0f4fa}",
"html.dark .fud-o,html.dark .fud select,html.dark .fud textarea,html.dark .fud-date,html.dark .fud-d{background:#0f1a27;border-color:#253a54;color:#e6edf6}",
"html.dark .fud-o.on{background:#16263a;border-color:#5b8fd8}",
"@media(max-width:620px){.fud-outs{grid-template-columns:1fr 1fr}.fud-row{grid-template-columns:1fr}.fud{padding:16px}}"
].join("");document.head.appendChild(st);}catch(e){}})();

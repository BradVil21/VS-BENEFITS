/* VS Health Benefits: site search + "Call an Advisor" in the header (2026-11-03).
   Loaded on every page with <script src="/vs-search.js" defer></script>.
   The index is /search-index.json, rebuilt by _build/build-search-index.py. */
(function () {
  if (window.__vsSearch) return; window.__vsSearch = 1;
  var PHONE = 'tel:+19548251009', PHONE_TXT = '(954) 825-1009';
  var wrap = document.querySelector('.site-header .nav-wrap');
  if (!wrap) return;

  var ICON_S = '<svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>';
  var ICON_P = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>';

  var css = ''
  + '.vss-d{display:none}.vss-m{display:flex;align-items:center;gap:8px;margin-left:auto;margin-right:10px}'
  + '.vss-ib{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:999px;border:1.5px solid #d7dfeb;background:#fff;color:#0b2346;cursor:pointer;padding:0;flex-shrink:0}'
  + '.vss-ib:hover{border-color:#16447f;color:#16447f}'
  + '.vss-call{display:inline-flex;align-items:center;gap:7px;border:1.5px solid #0b2346!important;color:#0b2346!important;border-radius:999px!important;font-weight:700!important;text-decoration:none!important;white-space:nowrap}'
  + '.vss-call:hover{background:#0b2346!important;color:#fff!important}'
  + '.vss-m .vss-call{height:40px;padding:0 14px;font-size:.9rem}'
  + '@media(max-width:959px){.site-header .nav-wrap{gap:0}.site-header .brand{white-space:nowrap;min-width:0;flex-shrink:1;gap:8px}.site-header .brand span:last-child{font-size:1rem}'
  +   '.vss-m{margin-right:8px}.vss-mpill{display:inline-flex;align-items:center;gap:6px;height:38px;padding:0 14px 0 11px;border:1.5px solid #d7dfeb;border-radius:999px;background:#f6f8fb;color:#64748b;font:inherit;font-size:.9rem;font-weight:500;cursor:pointer;white-space:nowrap}.vss-mpill svg{color:#16447f;flex-shrink:0}'
  +   '.nav-links .vss-mrow{display:flex!important;align-items:center;gap:10px}'
  +   '.nav-links .vss-d{display:none!important}'
  +   '.nav-links button.vss-mrow{width:100%;background:none;border:0;border-bottom:1px solid var(--line,#e4e9f2);padding:14px 20px;font:inherit;font-weight:600;font-size:1rem;color:var(--ink,#0b2346);cursor:pointer;text-align:left;min-height:48px}'
  +   '.nav-links a.vss-mcall{justify-content:center;margin:10px 16px 0!important;width:calc(100% - 32px)!important;align-self:center;border:1.5px solid #0b2346!important;border-radius:10px!important;color:#0b2346!important;font-weight:700!important;padding:13px 16px!important}}'
  + '@media(max-width:389px){.vss-mpill span{display:none}.vss-mpill{width:38px;padding:0;justify-content:center}}'
  + '@media(max-width:350px){.site-header .brand span:last-child{font-size:.9rem}}'
  + '.vss-mrow{display:none!important}'
  + '@media(min-width:960px){.vss-m{display:none}.vss-d{display:inline-flex!important}'
  +   '.site-header .brand{flex-shrink:0;white-space:nowrap}.nav-links>a[href="/"]{display:none!important}'
  +   'html body header nav.nav-links>a.nav-cta{display:none!important}'
  +   'html body header nav.nav-links>.vss-bar{margin-left:auto!important;margin-right:0!important}'
  +   '.nav-links button.vss-bar{display:inline-flex!important;align-items:center;gap:8px;width:230px;height:40px;margin:0 0 0 10px!important;padding:0 10px 0 14px!important;border:1.5px solid #d7dfeb!important;border-radius:999px!important;background:#f6f8fb!important;color:#64748b!important;font:inherit;font-size:.9rem!important;font-weight:500!important;cursor:text;text-align:left;white-space:nowrap;transition:border-color .15s,background .15s,box-shadow .15s}'
  +   '.nav-links button.vss-bar:hover{border-color:#16447f!important;background:#fff!important;box-shadow:0 4px 14px -6px rgba(11,35,70,.25)}'
  +   '.nav-links button.vss-bar svg{color:#16447f;flex-shrink:0}'
  +   '.vss-bar .vss-ph{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}'
  +   '.vss-bar kbd{font:inherit;font-size:.72rem;font-weight:700;color:#64748b;border:1px solid #d7dfeb;background:#fff;border-radius:6px;padding:1px 7px;line-height:1.5}}'
  + '@media(min-width:1280px){.site-header .nav-wrap{max-width:1360px}}'
  + '@media(min-width:960px) and (max-width:1279px){.nav-links button.vss-bar{width:170px}.vss-bar kbd{display:none}}'
  + '@media(min-width:960px) and (max-width:1099px){.nav-links button.vss-bar{width:136px;margin-left:8px!important}}'

  + '.vss-ov{position:fixed;inset:0;z-index:10000;background:rgba(11,35,70,.45);backdrop-filter:blur(3px);display:none;align-items:flex-start;justify-content:center;padding:9vh 14px 14px}'
  + '.vss-ov.open{display:flex}.vss-body{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}.vss-res{overflow:visible!important}'
  + '.vss-pn{width:100%;max-width:680px;max-height:80vh;display:flex;flex-direction:column;background:#fff;border-radius:18px;box-shadow:0 30px 80px -20px rgba(11,35,70,.5);overflow:hidden;font-family:Inter,system-ui,-apple-system,sans-serif}'
  + '.vss-top{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid #e8edf4;color:#16447f}'
  + '.vss-top input{flex:1;min-width:0;border:0;outline:0;font:inherit;font-size:1.1rem;color:#0b2346;background:transparent;padding:6px 0;-webkit-appearance:none;appearance:none}.vss-top input::-webkit-search-cancel-button{display:none}'
  + '.vss-x{border:0;background:#f1f5f9;color:#475569;border-radius:8px;padding:6px 10px;font:inherit;font-size:.78rem;font-weight:700;cursor:pointer}.vss-x .vss-xm{display:none}'
  + '@media(max-width:639px){.vss-ov{padding:0;background:#fff;backdrop-filter:none}.vss-pn{max-width:none;height:100%;max-height:none;border-radius:0;box-shadow:none}'
  +   '.vss-top{padding:10px 12px 10px 16px;min-height:60px}.vss-x{background:none;color:#16447f;font-size:1rem;padding:10px 6px}.vss-x .vss-xd{display:none}.vss-x .vss-xm{display:inline}'
  +   '.vss-res{padding:4px 6px}.vss-res a{padding:14px 12px}.vss-chips button{padding:10px 15px;font-size:.92rem}.vss-ft{padding:12px 16px calc(12px + env(safe-area-inset-bottom))}}'
  + '.vss-res{overflow-y:auto;padding:8px;margin:0;list-style:none}'
  + '.vss-res a{display:block;padding:12px 14px;border-radius:12px;text-decoration:none;color:#0b2346}'
  + '.vss-res a:hover,.vss-res a.on{background:#f1f6fd}'
  + '.vss-t{display:block;font-weight:700;font-size:.98rem;line-height:1.35}'
  + '.vss-u{display:block;font-size:.74rem;color:#0b7f74;font-weight:600;margin:2px 0 3px;text-transform:uppercase;letter-spacing:.04em}'
  + '.vss-s{display:block;font-size:.86rem;color:#475569;line-height:1.45;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}'
  + '.vss-res mark{background:#d9f5f1;color:inherit;border-radius:3px;padding:0 1px}'
  + '.vss-msg{padding:18px 16px;color:#475569;font-size:.92rem}'
  + '.vss-chips{display:flex;flex-wrap:wrap;gap:8px;padding:4px 16px 16px}'
  + '.vss-chips button{border:1.5px solid #d7dfeb;background:#fff;border-radius:999px;padding:7px 13px;font:inherit;font-size:.85rem;font-weight:600;color:#16447f;cursor:pointer}'
  + '.vss-chips button:hover{border-color:#0db5a6}'
  + '.vss-ft{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;padding:12px 16px;border-top:1px solid #e8edf4;background:#fafbfd;font-size:.85rem;color:#475569}'
  + '.vss-ft a{color:#16447f;font-weight:700;text-decoration:none;display:inline-flex;align-items:center;gap:6px}'
  + 'body.vss-lock{overflow:hidden}';
  var st = document.createElement('style'); st.id = 'vss-css'; st.textContent = css; document.head.appendChild(st);

  /* ---- header buttons ---- */
  var nav = wrap.querySelector('.nav-links');
  var cta = nav && nav.querySelector('a.nav-cta');
  if (nav) {
    var sb = document.createElement('button');
    sb.type = 'button'; sb.className = 'vss-d vss-bar vss-sbtn'; sb.setAttribute('aria-label', 'Search the site'); sb.innerHTML = ICON_S + '<span class="vss-ph">Search</span><kbd>/</kbd>';
    if (cta) { nav.insertBefore(sb, cta); cta.classList.add('vss-has'); }
    else { nav.appendChild(sb); }
  }
  var m = document.createElement('div'); m.className = 'vss-m';
  m.innerHTML = '<button type="button" class="vss-mpill vss-sbtn" aria-label="Search the site">' + ICON_S + '<span>Search</span></button>';
  var tog = wrap.querySelector('.menu-toggle');
  if (tog) wrap.insertBefore(m, tog); else wrap.appendChild(m);

  /* ---- search overlay ---- */
  var ov = document.createElement('div');
  ov.className = 'vss-ov'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', 'Search VS Health Benefits');
  ov.innerHTML = '<div class="vss-pn">'
    + '<div class="vss-top">' + ICON_S + '<input type="search" placeholder="Search the site" aria-label="Search" autocomplete="off" enterkeyhint="search"><button type="button" class="vss-x"><span class="vss-xd">Esc</span><span class="vss-xm">Cancel</span></button></div>'
    + '<div class="vss-body"></div>'
    + '<div class="vss-ft"><span>Can\'t find it? Talk to a licensed advisor.</span><a href="' + PHONE + '">' + ICON_P + PHONE_TXT + '</a></div>'
    + '</div>';
  document.body.appendChild(ov);
  var inp = ov.querySelector('input'), body = ov.querySelector('.vss-body');
  var SUGG = ['Truck drivers', 'Small business', 'Self-employed', 'PPO plans', 'Dental and vision', 'Family plans', 'DOT physical', 'COBRA'];

  var idx = null, loading = null, sel = -1, lastFocus = null;
  function load() {
    if (idx || loading) return loading;
    loading = fetch('/search-index.json', { cache: 'force-cache' }).then(function (r) { return r.json(); }).then(function (j) {
      idx = j.map(function (p) {
        return { p: p, t: norm(p.t), h: norm(p.h || ''), d: norm(p.d || ''), b: norm(p.b || ''), u: norm(p.u.replace(/[\/-]/g, ' ')) };
      });
      return idx;
    }).catch(function () { idx = []; });
    return loading;
  }
  function norm(s) { return (' ' + s + ' ').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9$]+/g, ' '); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var SYN = { trucker: 'truck', truckers: 'truck', trucking: 'truck', driver: 'driver', otr: 'truck', cdl: 'cdl', dentist: 'dental', eye: 'vision', glasses: 'vision', kids: 'family', children: 'family', employees: 'small business', employer: 'small business', business: 'business', freelancer: 'self employed', contractor: 'contractor', '1099': '1099', cost: 'cost', price: 'cost', cheap: 'affordable' };
  function terms(q) {
    var out = [];
    norm(q).trim().split(' ').forEach(function (w) {
      if (!w || (w.length < 2 && !/\d/.test(w))) return;
      var v = SYN[w] && SYN[w].indexOf(' ') < 0 ? SYN[w] : w;
      if (v.length > 4 && /s$/.test(v) && !/ss$/.test(v)) v = v.slice(0, -1);
      out.push(v);
    });
    return out;
  }
  function score(e, ts, all) {
    var s = 0, hit = 0;
    for (var i = 0; i < ts.length; i++) {
      var w = ' ' + ts[i], f = 0;
      if (e.t.indexOf(w) >= 0) { s += 12; f = 1; }
      if (e.u.indexOf(w) >= 0) { s += 6; f = 1; }
      if (e.h.indexOf(w) >= 0) { s += 5; f = 1; }
      if (e.d.indexOf(w) >= 0) { s += 3; f = 1; }
      if (e.b.indexOf(w) >= 0) { s += 1; f = 1; }
      if (f) hit++; else if (all) return 0;
    }
    if (!hit) return 0;
    var phrase = ' ' + ts.join(' ');
    if (ts.length > 1 && e.t.indexOf(phrase) >= 0) s += 15;
    if (e.p.k === 'Blog') s -= 1;
    return s + hit * 4;
  }
  function hl(text, ts) {
    var h = esc(text);
    ts.forEach(function (t) { if (t.length < 2) return; h = h.replace(new RegExp('(^|[^a-z0-9])(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '[a-z0-9]*)', 'gi'), '$1<mark>$2</mark>'); });
    return h;
  }
  function empty() {
    sel = -1;
    body.innerHTML = '<div class="vss-msg">Popular searches</div><div class="vss-chips">' + SUGG.map(function (s) { return '<button type="button">' + esc(s) + '</button>'; }).join('') + '</div>';
    [].forEach.call(body.querySelectorAll('.vss-chips button'), function (b) { b.onclick = function () { inp.value = b.textContent; run(); inp.focus(); }; });
  }
  function run() {
    var q = inp.value.trim();
    if (!q) return empty();
    if (!idx) { body.innerHTML = '<div class="vss-msg">Loading&hellip;</div>'; load().then(run); return; }
    var ts = terms(q); if (!ts.length) return empty();
    var r = [];
    idx.forEach(function (e) { var s = score(e, ts, true); if (s) r.push([s, e]); });
    if (!r.length) idx.forEach(function (e) { var s = score(e, ts, false); if (s) r.push([s, e]); });
    r.sort(function (a, b) { return b[0] - a[0]; });
    r = r.slice(0, 12);
    sel = -1;
    if (!r.length) { body.innerHTML = '<div class="vss-msg">No pages found for &ldquo;' + esc(q) + '&rdquo;. Try another word, or call us and we\'ll answer it directly.</div>'; return; }
    body.innerHTML = '<ul class="vss-res" role="listbox">' + r.map(function (x) {
      var p = x[1].p;
      return '<li><a href="' + esc(p.u) + '"><span class="vss-u">' + esc(p.k || 'Page') + '</span><span class="vss-t">' + hl(p.t, ts) + '</span>' + (p.d ? '<span class="vss-s">' + hl(p.d, ts) + '</span>' : '') + '</a></li>';
    }).join('') + '</ul>';
  }
  function move(d) {
    var as = body.querySelectorAll('.vss-res a'); if (!as.length) return;
    if (as[sel]) as[sel].classList.remove('on');
    sel = (sel + d + as.length) % as.length;
    as[sel].classList.add('on'); as[sel].scrollIntoView({ block: 'nearest' });
  }
  var timer;
  inp.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(run, 90); });
  inp.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter') {
      var a = body.querySelectorAll('.vss-res a'); var t = a[sel >= 0 ? sel : 0];
      if (t) { e.preventDefault(); location.href = t.getAttribute('href'); }
    }
  });
  function open() {
    lastFocus = document.activeElement;
    ov.classList.add('open'); document.body.classList.add('vss-lock');
    load(); if (!inp.value) empty(); else run();
    setTimeout(function () { inp.focus(); }, 30);
    var nl = document.getElementById('nav-links'); if (nl && nl.classList.contains('open') && tog) tog.click();
    try { if (window.gtag) gtag('event', 'search_open'); } catch (e) {}
  }
  function close() {
    ov.classList.remove('open'); document.body.classList.remove('vss-lock');
    if (inp.value.trim()) { try { if (window.gtag) gtag('event', 'search', { search_term: inp.value.trim() }); } catch (e) {} }
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  [].forEach.call(document.querySelectorAll('.vss-sbtn'), function (b) { b.addEventListener('click', open); });
  ov.querySelector('.vss-x').addEventListener('click', close);
  ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && ov.classList.contains('open')) { close(); return; }
    var tag = (e.target.tagName || '').toLowerCase();
    if (((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') || (e.key === '/' && !/input|textarea|select/.test(tag) && !e.target.isContentEditable)) {
      if (!ov.classList.contains('open')) { e.preventDefault(); open(); }
    }
  });
  window.vsOpenSearch = open;
})();

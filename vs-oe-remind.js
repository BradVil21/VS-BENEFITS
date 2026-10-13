/* =====================================================================
   OPEN ENROLLMENT REMINDER  (vs-oe-remind.js)

   Most drivers who read the trucker pages in October are not ready to buy
   until open enrollment opens on November 1. This box keeps them: one phone
   number, an explicit SMS opt-in, and the lead lands in GoHighLevel + the
   admin board through /api/lead-draft, tagged "oe-reminder" so a workflow
   can text them on Nov 1 and again before the Dec 15 deadline.

   Markup on the page:  <div class="vs-oer" data-from="page-slug" data-lang="en|es"></div>
   It switches itself off on November 1, 2026 (open enrollment is then live,
   and the normal quote form is the right ask).
   ===================================================================== */
(function () {
  "use strict";
  var OPENS = new Date(2026, 10, 1); // Nov 1, 2026 (local time)
  if (new Date() >= OPENS) return;

  var TXT = {
    en: {
      eyebrow: "Open enrollment starts November 1",
      h: "Not ready yet? Get a text when 2027 plans open.",
      p: "Leave your number and we'll text you the day open enrollment opens, plus one reminder before the December 15 deadline for January 1 coverage.",
      name: "First name (optional)", phone: "Mobile number", btn: "Text me when it opens",
      consent: 'I agree to receive SMS text messages from <strong>VS BENEFITS LLC</strong> (d/b/a VS Health Benefits) at this number about open enrollment and my health insurance quote. Message &amp; data rates may apply. Message frequency varies. Reply <strong>STOP</strong> to opt out or <strong>HELP</strong> for help. Consent is not a condition of purchase. <a href="/privacy#sms" target="_blank" rel="noopener">Privacy Policy</a> &amp; <a href="/terms#sms-terms" target="_blank" rel="noopener">Terms</a>.',
      errPhone: "Please enter a valid 10-digit mobile number.", errConsent: "Please check the box so we're allowed to text you.",
      sending: "Saving...", okH: "You're on the list.", okP: "We'll text you on November 1 when 2027 plans open. Want your numbers sooner?",
      okLink: "Get a quote now &rarr;", quote: "/truckers/quote"
    },
    es: {
      eyebrow: "La inscripci&oacute;n abierta empieza el 1 de noviembre",
      h: "&iquest;Todav&iacute;a no? Reciba un texto cuando abran los planes 2027.",
      p: "Deje su n&uacute;mero y le enviaremos un texto el d&iacute;a que abra la inscripci&oacute;n, y un recordatorio antes del 15 de diciembre para tener cobertura desde el 1 de enero.",
      name: "Nombre (opcional)", phone: "N&uacute;mero de celular", btn: "Av&iacute;senme por texto",
      consent: 'Acepto recibir mensajes de texto SMS de <strong>VS BENEFITS LLC</strong> (d/b/a VS Health Benefits) a este n&uacute;mero sobre la inscripci&oacute;n abierta y mi cotizaci&oacute;n de seguro m&eacute;dico. Pueden aplicarse tarifas de mensajes y datos. La frecuencia de los mensajes var&iacute;a. Responda <strong>STOP</strong> para cancelar o <strong>HELP</strong> para recibir ayuda. El consentimiento no es una condici&oacute;n de compra. <a href="/privacy#sms" target="_blank" rel="noopener">Pol&iacute;tica de privacidad</a> y <a href="/terms#sms-terms" target="_blank" rel="noopener">T&eacute;rminos</a>.',
      errPhone: "Escriba un número de celular válido de 10 dígitos.", errConsent: "Marque la casilla para que podamos enviarle textos.",
      sending: "Guardando...", okH: "&iexcl;Listo, ya est&aacute; en la lista!", okP: "Le enviaremos un texto el 1 de noviembre cuando abran los planes 2027. &iquest;Quiere sus n&uacute;meros antes?",
      okLink: "Cotizar ahora &rarr;", quote: "/truckers/cotizar"
    }
  };

  var CSS =
    ".vs-oer-box{max-width:880px;margin:28px auto;border-radius:18px;background:linear-gradient(135deg,#0b2346,#16447f);color:#fff;padding:26px 26px 22px;box-shadow:0 16px 40px rgba(13,27,42,.18);font-family:Inter,system-ui,-apple-system,sans-serif}" +
    ".vs-oer-box *{box-sizing:border-box}" +
    ".vs-oer-eb{display:inline-block;background:rgba(13,181,166,.22);color:#9ff0e6;border-radius:999px;padding:5px 12px;font-size:.74rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:10px}" +
    ".vs-oer-box h3{font-family:Poppins,Inter,sans-serif;color:#fff;font-size:clamp(1.2rem,2.6vw,1.5rem);line-height:1.25;margin:0 0 8px}" +
    ".vs-oer-box>p,.vs-oer-ok p{color:#d7e3f4;margin:0 0 16px;line-height:1.55;font-size:.95rem}" +
    ".vs-oer-row{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1fr) auto;gap:10px}" +
    ".vs-oer-row input{width:100%;min-height:50px;border:0;border-radius:12px;padding:0 14px;font:inherit;font-size:1rem;color:#0d1b2a;background:#fff}" +
    ".vs-oer-btn{min-height:50px;border:0;border-radius:12px;padding:0 20px;font:inherit;font-weight:700;font-size:.98rem;color:#fff;background:#0db5a6;cursor:pointer;white-space:nowrap}" +
    ".vs-oer-btn:disabled{opacity:.7;cursor:default}" +
    ".vs-oer-c{display:flex;gap:10px;align-items:flex-start;margin-top:12px;font-size:.74rem;line-height:1.5;color:#b9c9de}" +
    ".vs-oer-c input{margin-top:3px;width:16px;height:16px;flex:none}" +
    ".vs-oer-c a{color:#9ff0e6}" +
    ".vs-oer-err{color:#ffd2c9;font-size:.86rem;font-weight:600;margin:10px 0 0}" +
    ".vs-oer-ok h3{margin-bottom:6px}.vs-oer-ok a{color:#9ff0e6;font-weight:700}" +
    "@media(max-width:700px){.vs-oer-box{margin:22px 0;padding:20px 18px}.vs-oer-row{grid-template-columns:minmax(0,1fr)}}";

  function d10(v) { var d = String(v || "").replace(/\D/g, ""); if (d.length === 11 && d[0] === "1") d = d.slice(1); return d; }
  function phoneOk(v) {
    var d = d10(v); if (d.length !== 10) return false; var a = d.slice(0, 3), x = d.slice(3, 6);
    if (/[01]/.test(a[0]) || /[01]/.test(x[0])) return false; if (/^(\d)\1{9}$/.test(d) || d === "1234567890") return false;
    if (a === "555" || x === "555") return false; return true;
  }
  function attr() { try { return window.vsAttribution ? window.vsAttribution() : null; } catch (e) { return null; } }
  function slug(s) { return String(s || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 30); }

  function build(el, i) {
    if (el._oer) return; el._oer = 1;
    var lang = (el.getAttribute("data-lang") || document.documentElement.lang || "en").slice(0, 2) === "es" ? "es" : "en";
    var T = TXT[lang], from = el.getAttribute("data-from") || location.pathname.replace(/^\/+/, "");
    var id = "vs-oer-" + i;
    el.innerHTML =
      '<div class="vs-oer-box" role="region" aria-labelledby="' + id + '-h">' +
      '<span class="vs-oer-eb">' + T.eyebrow + '</span>' +
      '<h3 id="' + id + '-h">' + T.h + '</h3><p>' + T.p + '</p>' +
      '<form novalidate><div class="vs-oer-row">' +
      '<input type="text" name="first" autocomplete="given-name" placeholder="' + T.name + '" aria-label="' + T.name + '">' +
      '<input type="tel" name="phone" inputmode="tel" autocomplete="tel" placeholder="' + T.phone + '" aria-label="' + T.phone + '" required>' +
      '<button type="submit" class="vs-oer-btn">' + T.btn + '</button></div>' +
      '<label class="vs-oer-c"><input type="checkbox" name="sms"><span>' + T.consent + '</span></label>' +
      '<p class="vs-oer-err" role="alert" hidden></p></form></div>';
    var f = el.querySelector("form"), ph = f.phone, er = f.querySelector(".vs-oer-err"), btn = f.querySelector("button");
    ph.addEventListener("input", function () {
      var v = ph.value.replace(/\D/g, ""); if (v.length >= 10) { if (v.length === 11 && v[0] === "1") v = v.slice(1); ph.value = "(" + v.slice(0, 3) + ") " + v.slice(3, 6) + "-" + v.slice(6, 10); }
    });
    function fail(m) { er.innerHTML = m; er.hidden = false; }
    f.addEventListener("submit", function (e) {
      e.preventDefault(); er.hidden = true;
      if (!phoneOk(ph.value)) return fail(T.errPhone);
      if (!f.sms.checked) return fail(T.errConsent);
      btn.disabled = true; btn.innerHTML = T.sending;
      var a = attr() || {}, ch = a.source || "Direct";
      var tags = ["trucker", "oe-reminder", "sms-opt-in", "src-" + slug(ch)];
      if (lang === "es") tags.push("spanish");
      var notes = ["Wants a text when 2027 open enrollment opens (Nov 1) and a reminder before Dec 15",
        "SMS consent: yes (checkbox)", "Language: " + (lang === "es" ? "Spanish" : "English"),
        "Came from page: /" + from, "Channel: " + ch];
      if (a.landing) notes.push("First landing page: " + a.landing);
      if (a.utm_campaign) notes.push("Campaign: " + a.utm_campaign);
      var body = JSON.stringify({
        type: "individual", product: "Trucker", phone: f.phone.value.trim(), firstName: f.first.value.trim(),
        consent: true, optIn: true, sms_opt_in: "yes", capture: "oe-reminder", step: "OE reminder signup",
        source: "Open enrollment reminder (trucker" + (lang === "es" ? ", Spanish" : "") + ")",
        requestedCoverage: "Health (truck driver)", tags: tags, notes: notes.join("; "), attribution: a,
        meta: { device: navigator.userAgent || "", referrer: document.referrer || "", page: location.pathname + location.search }
      });
      var finished = false;
      function done() {
        if (finished) return; finished = true;
        try { if (window.vsTrack) window.vsTrack("oe_reminder_signup", { lead_type: "trucker", lang: lang }); } catch (x) {}
        el.querySelector(".vs-oer-box").innerHTML = '<div class="vs-oer-ok"><h3>' + T.okH + '</h3><p>' + T.okP +
          ' <a href="' + T.quote + '?from=' + encodeURIComponent(from + "-oe-reminder") + '">' + T.okLink + '</a></p></div>';
      }
      try { fetch("/api/lead-draft", { method: "POST", headers: { "Content-Type": "application/json" }, body: body, keepalive: true }).then(done, done); }
      catch (x) { done(); }
      setTimeout(done, 2500);
    });
  }

  function init() {
    var els = document.querySelectorAll(".vs-oer"); if (!els.length) return;
    if (!document.getElementById("vs-oer-css")) { var s = document.createElement("style"); s.id = "vs-oer-css"; s.textContent = CSS; document.head.appendChild(s); }
    for (var i = 0; i < els.length; i++) build(els[i], i);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();

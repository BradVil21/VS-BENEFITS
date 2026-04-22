/* VS Benefits - vshealthbenefits.com
   Interactive behaviors: mobile nav, countdown, coverage-picker,
   form submission via Make.com webhook (with mailto fallback). */

// !! REPLACE the placeholder below with your actual Make.com webhook URL.
// Example: "https://hook.us1.make.com/abc123xyz..."
window.MAKE_WEBHOOK_URL = window.MAKE_WEBHOOK_URL || "REPLACE_WITH_YOUR_MAKE_WEBHOOK_URL";

document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  /* ---------- Mobile hamburger nav ---------- */
  var toggle = document.querySelector(".menu-toggle");
  var links  = document.querySelector(".nav-links");

  function closeMenu() {
    if (!links) return;
    links.classList.remove("open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  }
  function toggleMenu(e) {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    if (!links) return;
    var open = links.classList.toggle("open");
    if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  if (toggle && links) {
    toggle.addEventListener("click", toggleMenu);
    toggle.addEventListener("touchend", function (e) { toggleMenu(e); }, { passive: false });
    // close menu after tapping a nav link
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeMenu);
    });
    // close menu when clicking/tapping outside
    document.addEventListener("click", function (e) {
      if (!links.classList.contains("open")) return;
      if (toggle.contains(e.target) || links.contains(e.target)) return;
      closeMenu();
    });
    // close menu on Escape
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });
  }

  /* ---------- ACA Open Enrollment countdown ---------- */
  // 2026-27 Open Enrollment Period (federal marketplace): Nov 1, 2026 - Jan 15, 2027.
  // Update these anchors annually.
  var START = new Date("2026-11-01T00:00:00-05:00").getTime();
  var END   = new Date("2027-01-15T23:59:59-05:00").getTime();

  var elDays = document.getElementById("cd-days");
  var elHrs  = document.getElementById("cd-hrs");
  var elMin  = document.getElementById("cd-min");
  var elSec  = document.getElementById("cd-sec");
  var elTitle = document.getElementById("cd-title");
  var elSub   = document.getElementById("cd-sub");
  var elWrap  = document.getElementById("cd-wrap");

  function pad(n){ return String(Math.max(0, n)).padStart(2, "0"); }

  function paint(target, titleText, subText) {
    var now = Date.now();
    var delta = Math.max(0, target - now);
    var d = Math.floor(delta / 86400000);
    var h = Math.floor((delta % 86400000) / 3600000);
    var m = Math.floor((delta % 3600000) / 60000);
    var s = Math.floor((delta % 60000) / 1000);
    if (elDays) elDays.textContent = pad(d);
    if (elHrs)  elHrs.textContent  = pad(h);
    if (elMin)  elMin.textContent  = pad(m);
    if (elSec)  elSec.textContent  = pad(s);
    if (elTitle && titleText) elTitle.textContent = titleText;
    if (elSub   && subText)   elSub.textContent   = subText;
  }
  function tick() {
    var now = Date.now();
    if (now < START) {
      paint(START,
            "ACA Open Enrollment 2027 starts in",
            "Nov 1, 2026 is your next chance to lock in individual or family ACA coverage. Get your documents ready.");
      if (elWrap) elWrap.classList.remove("closed");
    } else if (now <= END) {
      paint(END,
            "Time left to enroll in 2027 ACA coverage",
            "Open Enrollment closes Jan 15, 2027. After that you will need a Special Enrollment event to switch plans.");
      if (elWrap) elWrap.classList.add("closed");
    } else {
      paint(Date.now(),
            "Open Enrollment is closed for 2027",
            "You may still qualify for a Special Enrollment Period (job change, marriage, move, etc). Ask us.");
      if (elWrap) elWrap.classList.add("closed");
    }
  }
  if (elDays || elHrs || elMin || elSec) {
    tick();
    setInterval(tick, 1000);
  }

  /* ---------- Coverage picker / stepped form ---------- */
  // Every form wrapped in <form class="stepped-form"> will have a picker step
  // followed by the data-collection step. On choice click, step 2 appears and
  // carries a hidden input "coverage_type" with the user's selection.
  document.querySelectorAll("form.stepped-form").forEach(function (form) {
    var step1 = form.querySelector(".coverage-step");
    var step2 = form.querySelector(".form-step");
    var dots  = form.querySelectorAll(".step-indicator .dot");
    var back  = form.querySelector(".back-to-picker");
    var badge = form.querySelector(".picked-badge-value");
    var hidden = form.querySelector('input[name="coverage_type"]');

    if (!step1 || !step2) return; // not a stepped form

    function setStep(n) {
      if (n === 1) {
        step1.hidden = false; step2.hidden = true;
      } else {
        step1.hidden = true;  step2.hidden = false;
      }
      if (dots.length >= 2) {
        dots[0].classList.toggle("active", n === 1);
        dots[1].classList.toggle("active", n === 2);
      }
    }
    setStep(1);

    form.querySelectorAll(".coverage-picker .choice").forEach(function (btn) {
      btn.addEventListener("click", function () {
        form.querySelectorAll(".coverage-picker .choice").forEach(function (b){ b.classList.remove("selected"); });
        btn.classList.add("selected");
        var val = btn.getAttribute("data-value") || btn.textContent.trim();
        if (hidden) hidden.value = val;
        if (badge) badge.textContent = val;
        setStep(2);
        // scroll form into view on mobile
        setTimeout(function(){ form.scrollIntoView({behavior:"smooth", block:"start"}); }, 50);
      });
    });
    if (back) {
      back.addEventListener("click", function (e) {
        e.preventDefault();
        setStep(1);
      });
    }
  });

  /* ---------- Form submission: Make.com webhook with mailto fallback ---------- */
  document.querySelectorAll("form[data-webhook], form.stepped-form, form[data-mailto]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      data._source = "vshealthbenefits.com";
      data._page   = window.location.pathname;
      data._ts     = new Date().toISOString();

      var webhook = form.getAttribute("data-webhook") || window.MAKE_WEBHOOK_URL;
      var mailto  = form.getAttribute("data-mailto")  || "bvilsainthealth@gmail.com";
      var submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
      var originalLabel = submitBtn ? submitBtn.textContent : "";
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "Sending..."; }

      function showSuccess() {
        var note = form.querySelector(".form-success");
        if (!note) {
          note = document.createElement("div");
          note.className = "form-success";
          note.style.cssText = "margin-top:14px;padding:14px 16px;border-radius:10px;background:#e8f7ee;border:1px solid #b7e0c5;color:#165c2e;font-weight:600";
          form.appendChild(note);
        }
        note.textContent = "Thanks - your request is in. I will personally reach out within one business day.";
        form.reset();
        var step1 = form.querySelector(".coverage-step");
        var step2 = form.querySelector(".form-step");
        if (step1 && step2) { step1.hidden = false; step2.hidden = true; }
      }
      function fallbackMailto() {
        var subj = "VS Benefits website inquiry - " + (data.coverage_type || "general");
        var body = Object.keys(data).filter(function(k){return k[0]!=="_"}).map(function(k){
          return k.replace(/_/g," ").toUpperCase() + ": " + data[k];
        }).join("\n");
        var href = "mailto:" + encodeURIComponent(mailto) +
                   "?subject=" + encodeURIComponent(subj) +
                   "&body=" + encodeURIComponent(body);
        window.location.href = href;
      }

      var useWebhook = webhook && webhook.indexOf("http") === 0 && webhook.indexOf("REPLACE_WITH_") === -1;

      if (useWebhook) {
        fetch(webhook, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        }).then(function (r) {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = originalLabel; }
          if (r.ok) { showSuccess(); }
          else { fallbackMailto(); }
        }).catch(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = originalLabel; }
          fallbackMailto();
        });
      } else {
        if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = originalLabel; }
        fallbackMailto();
      }
    });
  });

  /* ---------- Footer year ---------- */
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
});

/* =====================================================================
   VETERANS DAY POP-UP  (vs-veterans-day.js)

   Loaded site-wide by a small block at the end of vs-search.js, which only
   pulls this file in on November 11 (visitor's local date).
   - Shows once per visitor per year: closing it (X, tap outside, or Esc)
     saves the year in localStorage, so it stays hidden until next Nov 11.
   - Test on any day by adding ?vetday-preview=1 to any page URL.
   - Image: /images/veterans-day-2026.jpg
   ===================================================================== */
(function () {
  "use strict";
  var IMAGE_URL = "/images/veterans-day-2026.jpg";
  var PHONE = "+19548251009";
  var PHONE_LABEL = "(954) 825-1009";
  var STORAGE_KEY = "vsHealthVetDayClosed";

  var now = new Date();
  var preview = /[?&]vetday-preview=1/.test(location.search);
  if (!preview && !(now.getMonth() === 10 && now.getDate() === 11)) return;

  var year = String(now.getFullYear());
  function getClosed() { try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; } }
  function setClosed() { try { localStorage.setItem(STORAGE_KEY, year); } catch (e) {} }
  if (!preview && getClosed() === year) return;
  if (document.getElementById("vsvd-overlay")) return;

  var css =
    "#vsvd-overlay{position:fixed;inset:0;z-index:2147483000;display:none;align-items:center;justify-content:center;padding:16px;background:rgba(5,12,35,.72);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);opacity:0;transition:opacity .3s ease}" +
    "#vsvd-overlay.vsvd-show{opacity:1}" +
    "#vsvd-box{position:relative;width:100%;max-width:560px;max-height:calc(100vh - 32px);overflow:auto;background:#fff;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.45);transform:translateY(16px) scale(.97);transition:transform .3s ease;font-family:'Poppins','Inter',system-ui,-apple-system,sans-serif;text-align:center}" +
    "#vsvd-overlay.vsvd-show #vsvd-box{transform:none}" +
    "#vsvd-img{display:block;width:100%;height:auto;border-radius:16px 16px 0 0}" +
    "#vsvd-body{padding:18px 22px 22px;border-top:5px solid #b22234}" +
    "#vsvd-body h2{margin:0 0 6px;font-size:22px;line-height:1.25;color:#002171;font-weight:800}" +
    "#vsvd-body p{margin:0;font-size:15px;line-height:1.5;color:#3a4256}" +
    "#vsvd-cta{display:inline-block;margin-top:16px;padding:12px 26px;border-radius:999px;background:#002171;color:#fff!important;text-decoration:none;font-weight:700;font-size:15px}" +
    "#vsvd-cta:hover{background:#0a2f8f}" +
    "#vsvd-close{position:absolute;top:10px;right:10px;width:40px;height:40px;border:0;border-radius:50%;background:rgba(0,0,0,.6);color:#fff;font-size:24px;line-height:40px;text-align:center;cursor:pointer;padding:0;font-family:Arial,sans-serif}" +
    "#vsvd-close:hover,#vsvd-close:focus-visible{background:#b22234;outline:none}" +
    "@media (max-width:480px){#vsvd-body{padding:14px 16px 18px}#vsvd-body h2{font-size:19px}#vsvd-body p{font-size:14px}#vsvd-close{width:36px;height:36px;line-height:36px;font-size:22px;top:8px;right:8px}}" +
    "@media (prefers-reduced-motion:reduce){#vsvd-overlay,#vsvd-box{transition:none}}";

  function build() {
    var style = document.createElement("style");
    style.textContent = css;
    document.head.appendChild(style);

    var overlay = document.createElement("div");
    overlay.id = "vsvd-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-labelledby", "vsvd-title");
    overlay.innerHTML =
      '<div id="vsvd-box">' +
        '<button id="vsvd-close" type="button" aria-label="Close">&times;</button>' +
        '<img id="vsvd-img" src="' + IMAGE_URL + '" width="1200" height="900" alt="VS Health Benefits - Happy Veterans Day. Honoring those who served.">' +
        '<div id="vsvd-body">' +
          '<h2 id="vsvd-title">Happy Veterans Day &#127482;&#127480;</h2>' +
          '<p>Thank you to every veteran and their family for your service and sacrifice. From all of us at VS Health Benefits.</p>' +
          '<a id="vsvd-cta" href="tel:' + PHONE + '">Call us: ' + PHONE_LABEL + '</a>' +
        '</div>' +
      '</div>';
    document.body.appendChild(overlay);

    var closeBtn = document.getElementById("vsvd-close");
    var lastFocus = document.activeElement;

    function close() {
      setClosed();
      overlay.classList.remove("vsvd-show");
      document.documentElement.style.overflow = "";
      setTimeout(function () { overlay.style.display = "none"; }, 300);
      document.removeEventListener("keydown", onKey);
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    function onKey(e) { if (e.key === "Escape") close(); }

    closeBtn.addEventListener("click", close);
    overlay.addEventListener("click", function (e) { if (e.target === overlay) close(); });
    document.addEventListener("keydown", onKey);

    overlay.style.display = "flex";
    document.documentElement.style.overflow = "hidden";
    requestAnimationFrame(function () { overlay.classList.add("vsvd-show"); });
    closeBtn.focus();
  }

  function start() { setTimeout(build, 1200); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();

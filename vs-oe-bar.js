/* OE BAR (vs-oe-bar.js) - retired 2026-11-03.
   The open enrollment announcement bar was removed from every page. This stub
   stays only so cached pages that still reference it remove any leftover bar. */
(function () {
  function go() { var b = document.getElementById("oe-annc-bar"); if (b && b.parentNode) b.parentNode.removeChild(b); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", go); else go();
})();

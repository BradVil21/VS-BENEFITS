/* VS Health Benefits - lightweight background video loader
 * Usage: <video data-vs-video="name" muted loop playsinline preload="none" ...></video>
 * Loads /videos/name-sm.mp4 (phones) or /videos/name-lg.mp4 only AFTER the page
 * finishes loading, only when the video is on screen, and pauses it when off screen.
 * Skipped entirely for Data Saver, 2G, and prefers-reduced-motion visitors
 * (they keep the photo underneath). */
(function () {
  var vids = [].slice.call(document.querySelectorAll('video[data-vs-video]'));
  if (!vids.length) return;
  var c = navigator.connection || {};
  if (c.saveData || /(^|-)2g$/.test(c.effectiveType || '')) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var small = window.matchMedia ? matchMedia('(max-width: 700px)').matches : false;

  function play(v) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  function load(v) {
    if (v.getAttribute('data-loaded')) return;
    v.setAttribute('data-loaded', '1');
    v.muted = true;
    v.addEventListener('playing', function () { v.style.opacity = '1'; }, { once: true });
    v.src = '/videos/' + v.getAttribute('data-vs-video') + (small ? '-sm' : '-lg') + '.mp4';
    play(v);
  }
  function start() {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          var v = e.target;
          if (e.isIntersecting) { v.getAttribute('data-loaded') ? play(v) : load(v); }
          else if (v.getAttribute('data-loaded')) { v.pause(); }
        });
      }, { rootMargin: '200px 0px' });
      vids.forEach(function (v) { io.observe(v); });
    } else {
      vids.forEach(load);
    }
  }
  function idle() { (window.requestIdleCallback || function (f) { setTimeout(f, 300); })(start, { timeout: 2500 }); }
  if (document.readyState === 'complete') idle(); else window.addEventListener('load', idle);
})();

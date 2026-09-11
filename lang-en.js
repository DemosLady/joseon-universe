/* joseon-universe · /en/ side
   Records that this visitor is reading in English, and records a switch back to
   Korean when they use the language switcher, so the redirect never fights them. */
(function () {
  var KEY = 'ju_lang';
  var BOTS = /bot|crawler|spider|crawling|yeti|daum|slurp|bingpreview|facebookexternalhit|embedly|lighthouse|headlesschrome/i;
  if (BOTS.test(navigator.userAgent)) return;

  function remember(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }

  remember('en');

  function wire() {
    var links = document.querySelectorAll('.langswitch a[hreflang="ko"]');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function () {
        remember('ko');
        if (typeof gtag === 'function') gtag('event', 'lang_switch', { to: 'ko' });
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wire);
  } else {
    wire();
  }
})();

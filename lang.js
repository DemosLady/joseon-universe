/* joseon-universe · language routing
   Sends a non-Korean browser to /en/ once, remembers the choice, and shows a
   banner for anyone the redirect did not catch. Crawlers are never redirected. */
(function () {
  var KEY = 'ju_lang';

  // --- never touch a crawler: Google and Naver must index both trees ---
  var BOTS = /bot|crawler|spider|crawling|yeti|daum|slurp|bingpreview|facebookexternalhit|embedly|quora|pinterest|whatsapp|telegram|lighthouse|headlesschrome/i;
  if (BOTS.test(navigator.userAgent)) return;

  // --- work out where the English twin of this page lives ---
  function twin() {
    var p = location.pathname;
    if (p.indexOf('/en/') === 0) return null;            // already there
    if (p === '/' || p === '' || /\/index\.html$/.test(p)) return '/en/';
    var file = p.replace(/^\//, '');
    // the story chapters are named differently on the two sides
    var m = file.match(/^tistory_ch(\d)_[a-z_]+\.html$/);
    if (m) return '/en/ch' + m[1] + '.html';
    // these exist in both trees under the same name
    if (/^(story|characters|timeline|ledger|search|songs|book|references|contact)\.html$/.test(file))
      return '/en/' + file;
    if (/^chapter[789]\.html$/.test(file)) return '/en/' + file;
    if (/^songs\/ch\d+-\d+\.html$/.test(file)) return '/en/' + file;
    // lyrics pages are Korean only, so offer the English index instead
    return '/en/';
  }

  var target = twin();
  if (!target) return;

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function remember(v) {
    try { localStorage.setItem(KEY, v); } catch (e) {}
  }

  // an explicit choice always wins, in both directions
  var choice = stored();
  if (choice === 'ko') return;

  var langs = (navigator.languages && navigator.languages.length)
    ? navigator.languages : [navigator.language || ''];
  var korean = langs.some(function (l) { return /^ko\b/i.test(l); });

  // --- first visit, non-Korean browser: go across once ---
  if (!korean && choice !== 'en-seen') {
    remember('en-seen');
    if (typeof gtag === 'function') gtag('event', 'lang_redirect', { to: 'en' });
    location.replace(target + location.search + location.hash);
    return;
  }

  // --- anyone the redirect did not catch gets a banner ---
  if (korean) return;

  function banner() {
    var bar = document.createElement('div');
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Language');
    bar.style.cssText =
      'position:relative;z-index:40;display:flex;align-items:center;justify-content:center;' +
      'gap:14px;padding:11px 18px;background:#e9e2d2;color:#2a2622;' +
      'font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:14px;' +
      'letter-spacing:.01em;line-height:1.5;box-shadow:0 1px 0 rgba(0,0,0,.25);';

    var text = document.createElement('span');
    text.textContent = 'This page is in Korean.';

    var go = document.createElement('a');
    go.href = target;
    go.textContent = 'Read in English →';
    go.style.cssText = 'color:#1a1a1a;font-weight:600;text-decoration:none;' +
      'border-bottom:1px solid rgba(26,26,26,.45);padding-bottom:1px;';
    go.addEventListener('click', function () {
      remember('en');
      if (typeof gtag === 'function') gtag('event', 'lang_banner', { to: 'en' });
    });

    var no = document.createElement('button');
    no.type = 'button';
    no.textContent = 'Stay';
    no.setAttribute('aria-label', 'Stay on the Korean page');
    no.style.cssText = 'background:none;border:0;color:#7a7060;font:inherit;' +
      'font-size:13px;cursor:pointer;padding:2px 6px;';
    no.addEventListener('click', function () {
      remember('ko');
      bar.parentNode && bar.parentNode.removeChild(bar);
    });

    bar.appendChild(text);
    bar.appendChild(go);
    bar.appendChild(no);
    document.body.insertBefore(bar, document.body.firstChild);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', banner);
  } else {
    banner();
  }
})();

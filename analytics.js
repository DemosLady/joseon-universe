'use strict';
(()=>{
  // The review Site never loads Google Analytics or sends production events.
  const active=SITE_CONFIG.mode==='public'&&location.origin===SITE_CONFIG.publicOrigin&&SITE_CONFIG.analyticsId==='G-J060GTVPQ1';
  if(!active)return;
  window.dataLayer=window.dataLayer||[];
  window.gtag=window.gtag||function(){window.dataLayer.push(arguments)};
  window.gtag('js',new Date());
  window.gtag('config',SITE_CONFIG.analyticsId,{allow_google_signals:false,allow_ad_personalization_signals:false});
  const script=document.createElement('script');script.async=true;script.src='https://www.googletagmanager.com/gtag/js?id='+SITE_CONFIG.analyticsId;document.head.appendChild(script);
  // GA4 Enhanced Measurement owns page_view; do not also emit manual page_view events.
  // Enable Page changes based on browser history events when checking the public property.
  let previousView='';
  function recordView(){const key=location.pathname;if(previousView===key)return;previousView=key;window.gtag('event','explorer_view',{page_path:key,page_title:document.title,content_language:document.documentElement.lang})}
  window.addEventListener('joseon:navigate',recordView);recordView();
  document.addEventListener('click',event=>{const link=event.target.closest('a[download]');if(link){const name=link.getAttribute('href').split('/').pop();window.gtag('event','book_download',{file_name:name,file_extension:'pdf',content_language:name.includes('-kr')?'ko':'en'})}const player=event.target.closest('[data-play]');if(player)window.gtag('event','listen_click',{track_id:player.dataset.play,content_language:document.documentElement.lang})});
})();

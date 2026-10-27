/* Alu-on measurement v1: GA4 + Consent Mode + click tracking */
(function () {
  var GA_ID = 'G-90R9DD9LW7';
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  window.gtag = gtag;

  // Consent: read the existing banner choice (app.js initPrivacyConsentSystem)
  var c = null;
  try { c = localStorage.getItem('aluon_privacy_consent'); } catch (e) {}
  var analyticsOk = (c === 'all' || c === 'custom_analytics');
  var adsOk = (c === 'all');
  gtag('consent', 'default', {
    analytics_storage: analyticsOk ? 'granted' : 'denied',
    ad_storage: adsOk ? 'granted' : 'denied',
    ad_user_data: adsOk ? 'granted' : 'denied',
    ad_personalization: adsOk ? 'granted' : 'denied',
    wait_for_update: 500
  });
  gtag('js', new Date());
  gtag('config', GA_ID);

  // Called from app.js when the user clicks the banner
  window.aluonConsentUpdate = function (type) {
    var a = (type === 'all' || type === 'custom_analytics');
    var ad = (type === 'all');
    gtag('consent', 'update', {
      analytics_storage: a ? 'granted' : 'denied',
      ad_storage: ad ? 'granted' : 'denied',
      ad_user_data: ad ? 'granted' : 'denied',
      ad_personalization: ad ? 'granted' : 'denied'
    });
  };

  function digits(s){ return (s || '').replace(/\D/g, ''); }
  function prettyPhone(d){
    if (d.indexOf('972') === 0) d = '0' + d.slice(3);
    return d.length === 10 ? d.slice(0,3) + '-' + d.slice(3) : d;
  }
  function locationOf(a){
    if (a.id === 'calcWhatsappLink') return 'calculator';
    if (a.closest('footer')) return 'footer';
    if (a.classList.contains('social-icon-btn')) return 'top_icons';
    if (a.closest('header')) return 'header';
    if (a.closest('#mobileMenu')) return 'mobile_menu';
    return 'content';
  }
  window.aluonTrack = function (name, params) {
    params = params || {};
    params.page_path = location.pathname;
    gtag('event', name, params);
  };

  // One delegated listener for every tel: and WhatsApp link, including future ones
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    var where = locationOf(a);
    if (href.indexOf('tel:') === 0) {
      var tel = prettyPhone(digits(href));
      aluonTrack('phone_click', { phone_label: 'call', phone_number: tel, link_location: where });
      aluonTrack('generate_lead', { lead_source: 'phone', phone_label: 'call', phone_number: tel, link_location: where });
    } else if (/wa\.me\/|api\.whatsapp\.com|whatsapp:\/\//.test(href)) {
      var m = href.match(/wa\.me\/(\d+)/) || href.match(/phone=(\d+)/);
      var wa = m ? prettyPhone(m[1]) : '';
      aluonTrack('whatsapp_click', { phone_label: 'whatsapp', phone_number: wa, link_location: where });
      aluonTrack('generate_lead', { lead_source: 'whatsapp', phone_label: 'whatsapp', phone_number: wa, link_location: where });
    }
  }, true);
})();

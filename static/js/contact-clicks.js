document.addEventListener('DOMContentLoaded', function () {
  if (typeof gtag !== 'function') return;

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a');
    if (!link || !link.href) return;

    if (link.href.indexOf('wa.me') !== -1) {
      gtag('event', 'whatsapp_click');
    } else if (link.href.indexOf('tel:') === 0) {
      gtag('event', 'phone_click');
    }
  });
});

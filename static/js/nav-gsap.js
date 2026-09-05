// Smooth GSAP-driven underline animation on nav link hover.
// Requires GSAP loaded first (see base.html CDN include).
document.addEventListener('DOMContentLoaded', function () {
  if (typeof gsap === 'undefined') return;

  document.querySelectorAll('.nav-links li').forEach(function (li) {
    var link = li.querySelector('a');
    if (!link) return;

    var underline = document.createElement('span');
    underline.className = 'nav-underline';
    li.appendChild(underline);

    li.addEventListener('mouseenter', function () {
      gsap.to(underline, { width: '100%', duration: 0.25, ease: 'power2.out' });
    });
    li.addEventListener('mouseleave', function () {
      // Keep the underline filled if this is the active page link
      if (link.classList.contains('is-active')) return;
      gsap.to(underline, { width: '0%', duration: 0.2, ease: 'power2.in' });
    });

    // Active page link starts with the underline already shown
    if (link.classList.contains('is-active')) {
      gsap.set(underline, { width: '100%' });
    }
  });

  // Subtle logo hover lift
  var logo = document.querySelector('.logo');
  if (logo) {
    logo.addEventListener('mouseenter', function () {
      gsap.to(logo, { scale: 1.03, duration: 0.2, ease: 'power2.out' });
    });
    logo.addEventListener('mouseleave', function () {
      gsap.to(logo, { scale: 1, duration: 0.2, ease: 'power2.in' });
    });
  }
});

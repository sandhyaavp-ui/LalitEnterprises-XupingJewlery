// Animates any element with data-countup="<target number>" from 0 to the
// target as it scrolls into view, appending data-suffix (if present) once
// finished. Static text (like "Since 2002") is untouched — just don't add
// data-countup to it.
document.addEventListener('DOMContentLoaded', function () {
  var targets = document.querySelectorAll('[data-countup]');
  if (targets.length === 0) return;

  function animateCount(el) {
    var target = parseInt(el.getAttribute('data-countup'), 10);
    var suffix = el.getAttribute('data-suffix') || '';
    var duration = 1200;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var current = Math.floor(progress * target);
      el.textContent = current + suffix;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target + suffix;
      }
    }
    requestAnimationFrame(step);
  }

  if (!('IntersectionObserver' in window)) {
    targets.forEach(function (el) {
      el.textContent = el.getAttribute('data-countup') + (el.getAttribute('data-suffix') || '');
    });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        animateCount(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });

  targets.forEach(function (el) { observer.observe(el); });
});

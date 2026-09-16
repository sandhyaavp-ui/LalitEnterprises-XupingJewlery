document.addEventListener('DOMContentLoaded', function () {
  var root = document.getElementById('circular-testimonials');
  if (!root) return;

  var dataEl = document.getElementById('ct-data');
  var items = dataEl ? JSON.parse(dataEl.textContent || '[]') : [];
  if (!items.length) return;

  var imagesEl = document.getElementById('ct-images');
  var nameEl = document.getElementById('ct-name');
  var designationEl = document.getElementById('ct-designation');
  var starsEl = document.getElementById('ct-stars');
  var quoteEl = document.getElementById('ct-quote');
  var prevBtn = document.getElementById('ct-prev');
  var nextBtn = document.getElementById('ct-next');

  var SILHOUETTE_ICON = '<svg viewBox="0 0 24 24"><path d="M12 12c2.7 0 4.9-2.2 4.9-4.9S14.7 2.2 12 2.2 7.1 4.4 7.1 7.1 9.3 12 12 12zm0 2.4c-3.3 0-9.8 1.6-9.8 4.9v2.5h19.6v-2.5c0-3.3-6.5-4.9-9.8-4.9z"/></svg>';

  var len = items.length;
  var activeIndex = 0;
  var autoplayTimer = null;

  items.forEach(function (item, i) {
    var el = document.createElement('div');
    el.className = 'ct-avatar';
    el.innerHTML = '<span class="ct-glow"></span>' + SILHOUETTE_ICON;
    el.dataset.index = i;
    imagesEl.appendChild(el);
  });
  var avatarEls = imagesEl.querySelectorAll('.ct-avatar');

  function gap() {
    var w = imagesEl.offsetWidth || 300;
    return Math.max(40, Math.min(70, w * 0.28));
  }

  function render() {
    var g = gap();
    var base = 'translate(-50%, -50%) ';

    avatarEls.forEach(function (el, i) {
      var isActive = i === activeIndex;
      var isRight = (activeIndex + 1) % len === i;
      var isLeft = (activeIndex - 1 + len) % len === i;

      if (isActive) {
        el.style.zIndex = 3;
        el.style.opacity = 1;
        el.style.transform = base + 'scale(1) rotateY(0deg)';
      } else if (len === 2 && isRight) {
        el.style.zIndex = 2;
        el.style.opacity = 1;
        el.style.transform = base + 'translateX(' + g + 'px) scale(0.8) rotateY(-20deg)';
      } else if (len > 2 && isLeft) {
        el.style.zIndex = 2;
        el.style.opacity = 1;
        el.style.transform = base + 'translateX(-' + g + 'px) scale(0.8) rotateY(20deg)';
      } else if (len > 2 && isRight) {
        el.style.zIndex = 2;
        el.style.opacity = 1;
        el.style.transform = base + 'translateX(' + g + 'px) scale(0.8) rotateY(-20deg)';
      } else {
        el.style.zIndex = 1;
        el.style.opacity = 0;
      }
    });

    var t = items[activeIndex];
    nameEl.textContent = t.name;
    designationEl.textContent = t.designation;
    starsEl.textContent = '★'.repeat(t.rating) + '☆'.repeat(5 - t.rating);
    quoteEl.innerHTML = '';
    t.quote.split(' ').forEach(function (word, i) {
      var span = document.createElement('span');
      span.className = 'ct-word';
      span.style.animationDelay = (i * 0.03) + 's';
      span.textContent = word + ' ';
      quoteEl.appendChild(span);
    });
  }

  function goTo(i) {
    activeIndex = (i + len) % len;
    render();
    resetAutoplay();
  }

  function next() { goTo(activeIndex + 1); }
  function prev() { goTo(activeIndex - 1); }

  function resetAutoplay() {
    if (autoplayTimer) clearInterval(autoplayTimer);
    if (len < 2) return;
    autoplayTimer = setInterval(function () {
      activeIndex = (activeIndex + 1) % len;
      render();
    }, 5000);
  }

  if (len > 1) {
    prevBtn.addEventListener('click', prev);
    nextBtn.addEventListener('click', next);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') prev();
      if (e.key === 'ArrowRight') next();
    });
  } else {
    prevBtn.style.display = 'none';
    nextBtn.style.display = 'none';
  }

  window.addEventListener('resize', render);

  render();
  resetAutoplay();
});

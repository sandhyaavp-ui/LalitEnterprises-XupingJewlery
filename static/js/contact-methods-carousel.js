document.addEventListener('DOMContentLoaded', function () {
  var grid = document.getElementById('contact-methods-grid');
  var dotsEl = document.getElementById('cm-dots');
  var prevBtn = document.getElementById('cm-prev');
  var nextBtn = document.getElementById('cm-next');
  if (!grid || !dotsEl || !prevBtn || !nextBtn) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('.card'));
  if (cards.length < 2) return;

  var activeIndex = 0;

  cards.forEach(function (_, i) {
    var dot = document.createElement('button');
    dot.type = 'button';
    dot.setAttribute('aria-label', 'Go to contact method ' + (i + 1));
    dot.addEventListener('click', function () { goTo(i); });
    dotsEl.appendChild(dot);
  });
  var dots = Array.prototype.slice.call(dotsEl.children);

  function render() {
    cards.forEach(function (card, i) {
      card.classList.toggle('is-active', i === activeIndex);
    });
    dots.forEach(function (dot, i) {
      dot.classList.toggle('is-active', i === activeIndex);
    });
  }

  function goTo(i) {
    activeIndex = (i + cards.length) % cards.length;
    render();
  }

  prevBtn.addEventListener('click', function () { goTo(activeIndex - 1); });
  nextBtn.addEventListener('click', function () { goTo(activeIndex + 1); });

  render();
});

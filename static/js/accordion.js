// Toggles .faq-item open/closed. Expected markup per item:
// <div class="faq-item">
//   <button class="faq-question">Question text <span class="faq-icon">+</span></button>
//   <div class="faq-answer"><p>Answer text</p></div>
// </div>
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.faq-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq-item');
      var alreadyOpen = item.classList.contains('is-open');
      // Close any other open item (accordion behavior: one open at a time)
      item.parentElement.querySelectorAll('.faq-item.is-open').forEach(function (open) {
        if (open !== item) open.classList.remove('is-open');
      });
      item.classList.toggle('is-open', !alreadyOpen);
    });
  });
});

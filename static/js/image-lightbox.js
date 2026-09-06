(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var overlay = document.getElementById('image-lightbox');
    var lightboxImg = document.getElementById('image-lightbox-img');
    var closeBtn = overlay ? overlay.querySelector('.image-lightbox-close') : null;
    var zoomBtn = document.querySelector('.image-zoom-btn');
    if (!overlay || !lightboxImg || !zoomBtn) return;

    function openLightbox() {
      lightboxImg.src = zoomBtn.getAttribute('data-full-src');
      lightboxImg.alt = zoomBtn.getAttribute('data-full-alt') || '';
      overlay.hidden = false;
      document.body.style.overflow = 'hidden';
      closeBtn.focus();
    }

    function closeLightbox() {
      overlay.hidden = true;
      document.body.style.overflow = '';
      lightboxImg.src = '';
    }

    zoomBtn.addEventListener('click', openLightbox);
    closeBtn.addEventListener('click', closeLightbox);

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeLightbox();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !overlay.hidden) closeLightbox();
    });
  });
})();

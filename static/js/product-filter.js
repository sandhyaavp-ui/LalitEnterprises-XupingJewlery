document.addEventListener('DOMContentLoaded', function () {
  var searchInput = document.getElementById('product-search');
  var pills = document.querySelectorAll('.filter-pill');
  var cards = document.querySelectorAll('#all-products-grid .card');
  if (!searchInput || cards.length === 0) return;

  var activeFilter = 'all';

  function applyFilters() {
    var query = searchInput.value.trim().toLowerCase();
    cards.forEach(function (card) {
      var matchesFilter = activeFilter === 'all' || card.dataset.collection === activeFilter;
      var matchesSearch = !query ||
        card.dataset.name.indexOf(query) !== -1 ||
        card.dataset.collection.indexOf(query) !== -1;
      card.style.display = (matchesFilter && matchesSearch) ? '' : 'none';
    });
  }

  pills.forEach(function (pill) {
    pill.addEventListener('click', function () {
      pills.forEach(function (p) { p.classList.remove('is-active'); });
      pill.classList.add('is-active');
      activeFilter = pill.dataset.filter;
      applyFilters();
    });
  });

  searchInput.addEventListener('input', applyFilters);
});

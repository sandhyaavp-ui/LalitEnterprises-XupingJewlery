document.addEventListener('DOMContentLoaded', function () {
  var $ = django.jQuery;
  var moqDefaults = window.COLLECTION_MOQ_MAP || {};

  $('#id_collection').on('change', function () {
    var selected = $(this).val();
    var currentMoq = $('#id_moq').val();
    if (moqDefaults[selected] !== undefined && (currentMoq === '' || currentMoq === '6')) {
      // Only auto-fill if MOQ is still at the generic default —
      // won't override a value staff already typed in.
      $('#id_moq').val(moqDefaults[selected]);
    }
  });
});

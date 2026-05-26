(function () {
  function updatePreview(select, preview) {
    preview.innerHTML = '';
    if (!select.value) {
      return;
    }
    var icon = document.createElement('i');
    icon.className = 'bi ' + select.value;
    preview.appendChild(icon);
  }

  function initIconSelect(select) {
    if (select.dataset.iconSelectInit === '1') {
      return;
    }
    select.dataset.iconSelectInit = '1';

    var wrap = document.createElement('div');
    wrap.className = 'bootstrap-icon-select-wrap';
    select.parentNode.insertBefore(wrap, select);
    wrap.appendChild(select);

    var preview = document.createElement('span');
    preview.className = 'bootstrap-icon-select__preview';
    preview.setAttribute('aria-hidden', 'true');
    wrap.appendChild(preview);

    select.addEventListener('change', function () {
      updatePreview(select, preview);
    });
    updatePreview(select, preview);
  }

  function initIconSelects(root) {
    var scope = root || document;
    scope.querySelectorAll('select.bootstrap-icon-select').forEach(initIconSelect);
  }

  document.addEventListener('DOMContentLoaded', function () {
    initIconSelects(document);
  });

  if (typeof django !== 'undefined' && django.jQuery) {
    django.jQuery(document).on('formset:added', function (_event, row) {
      initIconSelects(row && row.length ? row[0] : document);
    });
  }
})();

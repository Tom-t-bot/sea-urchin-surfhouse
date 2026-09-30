document.addEventListener('DOMContentLoaded', function () {
  // Squarespace ships more than one copy of the desktop language-picker
  // markup on some pages (one in the visible header, one nested inside the
  // mobile header's own markup) — wire up every instance, not just the
  // first, since they can share the same id.
  var pickers = document.querySelectorAll('.language-picker.language-picker-desktop');

  pickers.forEach(function (picker) {
    var btn = picker.querySelector('.current-language');
    var menu = picker.querySelector('.language-picker-content');
    if (!btn || !menu) return;

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var willOpen = menu.hidden;
      menu.hidden = !willOpen;
      btn.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    });

    document.addEventListener('click', function (e) {
      if (!picker.contains(e.target)) {
        menu.hidden = true;
        btn.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        menu.hidden = true;
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  var picker = document.getElementById('multilingual-language-picker-desktop');
  if (!picker) return;
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

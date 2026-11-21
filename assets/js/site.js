/* 安徽华森氢能源科技 — 站点交互（零依赖） */
(function () {
  "use strict";
  var btn = document.querySelector('.menu-btn');
  var nav = document.querySelector('.main-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') nav.classList.remove('open');
    });
  }

  /* 复制电话/邮箱 */
  document.querySelectorAll('[data-copy]').forEach(function (el) {
    el.addEventListener('click', function () {
      var text = el.getAttribute('data-copy');
      var done = function () {
        var old = el.getAttribute('data-label') || el.textContent;
        el.setAttribute('data-label', old);
        el.textContent = '已复制';
        setTimeout(function () { el.textContent = old; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, done);
      } else {
        var ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta); done();
      }
    });
  });

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();

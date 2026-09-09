// Interface Craft — Lessons
// Minimal JS: theme, language preference, sidebar state, scroll-edge tracking and the demo controls.

(function () {
  var root = document.documentElement;

  // ---- Theme -----------------------------------------------------------
  var toggle = document.getElementById('theme-toggle');
  function systemPrefersDark() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function currentTheme() {
    return root.getAttribute('data-theme') || (systemPrefersDark() ? 'dark' : 'light');
  }
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      // Transition only during the toggle, never globally (HTML Background lesson)
      root.classList.add('theme-transition');
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
      setTimeout(function () { root.classList.remove('theme-transition'); }, 260);
    });
  }

  // ---- Language ------------------------------------------------------------
  var pageLang = root.getAttribute('data-lang') || 'en';
  Array.prototype.forEach.call(document.querySelectorAll('.lang-opt'), function (a) {
    a.addEventListener('click', function () {
      try { localStorage.setItem('lang', a.getAttribute('data-lang')); } catch (e) {}
    });
  });
  try {
    var saved = localStorage.getItem('lang');
    var arrivedViaSwitch = document.referrer && new URL(document.referrer).origin === location.origin;
    if (saved && saved !== pageLang && !arrivedViaSwitch) {
      var target = document.querySelector('.lang-opt[data-lang="' + saved + '"]');
      if (target && target.getAttribute('href') !== '#') location.replace(target.getAttribute('href'));
    }
  } catch (e) {}

  // ---- Scroll edges: fade only where there is more content (Scroll Fades lesson) -----
  function trackEdges(el, horizontal) {
    function update() {
      var pos = horizontal ? el.scrollLeft : el.scrollTop;
      var max = horizontal ? el.scrollWidth - el.clientWidth : el.scrollHeight - el.clientHeight;
      el.toggleAttribute('data-at-start', pos <= 1);
      el.toggleAttribute('data-at-end', pos >= max - 1);
    }
    el.addEventListener('scroll', update, { passive: true });
    if ('ResizeObserver' in window) new ResizeObserver(update).observe(el);
    update();
  }
  var side = document.querySelector('.sidebar');
  if (side) trackEdges(side, false);
  Array.prototype.forEach.call(document.querySelectorAll('.scroller'), function (el) { trackEdges(el, true); });

  // ---- Sidebar: active item follows scroll ----------------------------------
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav-link[href^="#"]'));
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
  var lessons = Array.prototype.slice.call(document.querySelectorAll('.lesson[id]'));

  function setActive(id) {
    links.forEach(function (a) { a.classList.remove('is-active'); });
    var a = byId[id];
    if (a) {
      a.classList.add('is-active');
      if (side && side.scrollHeight > side.clientHeight) {
        var r = a.getBoundingClientRect(), s = side.getBoundingClientRect();
        if (r.top < s.top + 60 || r.bottom > s.bottom - 60) {
          side.scrollTo({ top: a.offsetTop - side.clientHeight / 2, behavior: 'smooth' });
        }
      }
    }
  }
  if ('IntersectionObserver' in window && lessons.length) {
    var visible = new Map();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) visible.set(e.target.id, e.boundingClientRect.top);
        else visible.delete(e.target.id);
      });
      if (visible.size) {
        var top = null;
        visible.forEach(function (y, id) { if (top === null || y < visible.get(top)) top = id; });
        setActive(top);
      }
    }, { rootMargin: '-10% 0px -60% 0px', threshold: 0 });
    lessons.forEach(function (l) { io.observe(l); });
  }

  // ---- Code blocks: copy ---------------------------------------------------------
  Array.prototype.forEach.call(document.querySelectorAll('[data-copy]'), function (btn) {
    var pre = btn.closest('.code').querySelector('pre'), timer;
    var text = btn.querySelector('.code-copy-text');
    btn.addEventListener('click', function () {
      var value = pre.innerText;
      function legacyCopy() {
        var ta = document.createElement('textarea');
        ta.value = value; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:fixed;opacity:0;pointer-events:none';
        document.body.appendChild(ta); ta.select();
        var ok = false; try { ok = document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta);
        return ok ? Promise.resolve() : Promise.reject();
      }
      var write = navigator.clipboard ? navigator.clipboard.writeText(value).catch(legacyCopy) : legacyCopy();
      write.then(function () {
        btn.classList.add('is-copied'); if (text) text.textContent = btn.getAttribute('data-copied');
        clearTimeout(timer);
        timer = setTimeout(function () { btn.classList.remove('is-copied'); if (text) text.textContent = btn.getAttribute('data-label'); }, 1600);
      }).catch(function () {});
    });
  });

  // ---- Demo controls -----------------------------------------------------------
  // The object is the interface. Parameters live in .demo-controls:
  //   slider  -> sets --name (with unit) and data-name on the .demo, fills the track, updates <output>
  //   switch  -> toggles .on-name on the .demo
  // Inside the stage, declarative hooks keep interactions consistent:
  //   [data-toggle="cls"]           click toggles that class on the .demo (and aria-expanded on the trigger)
  //   [data-flash="cls"][data-flash-ms] click adds the class for a while (toasts)
  //   [data-drag]                   pointer drag along x; release settles back with the demo's --curve
  function formatValue(input) {
    var v = input.value, unit = input.getAttribute('data-unit') || '';
    if (unit === 'em' || (input.step && input.step.indexOf('.') >= 0)) {
      var d = (input.step.split('.')[1] || '').length;
      v = Number(v).toFixed(d);
    }
    return v + unit;
  }
  // Color math for the Color demos: OKLCH -> linear sRGB, WCAG 2 ratio, APCA Lc
  function oklchToLinear(L, C, H) {
    var h = H * Math.PI / 180, a = C * Math.cos(h), b = C * Math.sin(h);
    var l_ = L + 0.3963377774 * a + 0.2158037573 * b, m_ = L - 0.1055613458 * a - 0.0638541728 * b, s_ = L - 0.0894841775 * a - 1.2914855480 * b;
    var l = l_ * l_ * l_, m = m_ * m_ * m_, sv = s_ * s_ * s_;
    return [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * sv, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * sv, -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * sv];
  }
  function inGamut(rgb) { return rgb.every(function (c) { return c >= -0.01 && c <= 1.01; }); }
  function relY(rgb) { var c = rgb.map(function (v) { return Math.min(1, Math.max(0, v)); }); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; }
  function wcagRatio(y1, y2) { var a = Math.max(y1, y2), b = Math.min(y1, y2); return (a + 0.05) / (b + 0.05); }
  function apcaLc(yTxt, yBg) {
    var cl = function (y) { return y > 0.022 ? y : y + Math.pow(0.022 - y, 1.414); };
    var t = cl(yTxt), g = cl(yBg), s;
    if (g > t) { s = (Math.pow(g, 0.56) - Math.pow(t, 0.57)) * 1.14; return s < 0.1 ? 0 : (s - 0.027) * 100; }
    s = (Math.pow(g, 0.65) - Math.pow(t, 0.62)) * 1.14; return s > -0.1 ? 0 : (s + 0.027) * 100;
  }
  Array.prototype.forEach.call(document.querySelectorAll('.demo'), function (demo) {
    // Replay: when a control changes, show the effect right away instead of waiting for the next interaction.
    // A demo can register demo._replay; otherwise the generic paths re-trigger an open state, a single flash button or a hover state.
    function replay() {
      if (typeof demo._replay === 'function') { demo._replay(); return; }
      var retriggered = false;
      Array.prototype.forEach.call(demo.querySelectorAll('[data-toggle]'), function (el) {
        var cls = el.getAttribute('data-toggle');
        if (demo.classList.contains(cls)) { retriggered = true; demo.classList.remove(cls); void demo.offsetWidth; demo.classList.add(cls); }
      });
      if (retriggered) return;
      var flashes = demo.querySelectorAll('[data-flash]');
      if (flashes.length === 1 && flashes[0].tagName === 'BUTTON' && !flashes[0].classList.contains('pp-target')) { flashes[0].click(); return; }
      var hov = demo.querySelector('[data-hover]');
      if (hov) { hov.classList.add('is-hover'); clearTimeout(demo._hovT); demo._hovT = setTimeout(function () { hov.classList.remove('is-hover'); }, 900); }
    }
    Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input[type="range"]'), function (r) {
      var out = r.parentNode.querySelector('output');
      function update() {
        demo.style.setProperty('--' + r.name, r.value + (r.getAttribute('data-unit') || ''));
        demo.setAttribute('data-' + r.name, String(Number(r.value)));
        r.style.setProperty('--p', ((r.value - r.min) / (r.max - r.min) * 100) + '%');
        if (out) out.textContent = formatValue(r);
      }
      r.addEventListener('input', update);
      r.addEventListener('change', function () { setTimeout(replay, 0); });
      update();
    });
    Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input[type="checkbox"]'), function (c) {
      function update() { demo.classList.toggle('on-' + c.name, c.checked); }
      c.addEventListener('change', function () { update(); setTimeout(replay, 0); });
      update();
    });
    // Scrub: when the stage has nothing of its own to touch, dragging on it scrubs the first slider and a tap flips the first switch.
    (function () {
      var stage = demo.querySelector('.demo-stage'); if (!stage) return;
      if (stage.querySelector('button, input, textarea, select, a, [role], [tabindex], [data-toggle], [data-flash], [data-drag], [data-hover], [data-sheet], .scroller, .sa-strip, .tb3-scroll, .sl-page, .pt-list, [data-fitts]')) return;
      var range = demo.querySelector('.demo-controls input[type="range"]'), sw = demo.querySelector('.demo-controls input[type="checkbox"]');
      if (!range && !sw) return;
      var pt = document.documentElement.lang.indexOf('pt') === 0;
      demo.classList.add(range ? 'is-scrub' : 'is-tap');
      stage.setAttribute('data-hint', range ? (pt ? 'arraste para ajustar' : 'drag to adjust') + (sw ? (pt ? ' · toque para alternar' : ' · tap to switch') : '') : (pt ? 'toque para alternar' : 'tap to switch'));
      var x0 = 0, v0 = 0, moved = false, down = false;
      stage.addEventListener('pointerdown', function (e) { if (e.button !== 0) return; down = true; moved = false; x0 = e.clientX; v0 = range ? Number(range.value) : 0; try { stage.setPointerCapture(e.pointerId); } catch (x) {} });
      stage.addEventListener('pointermove', function (e) {
        if (!down || !range) return; var dx = e.clientX - x0; if (!moved && Math.abs(dx) < 4) return;
        if (!moved) { moved = true; stage.classList.add('is-scrubbing'); }
        var min = Number(range.min), max = Number(range.max), step = Number(range.step) || 1, span = max - min;
        var v = v0 + dx / 220 * span; v = Math.round(v / step) * step; v = Math.max(min, Math.min(max, v));
        var digits = (String(range.step).split('.')[1] || '').length; range.value = v.toFixed(digits); range.dispatchEvent(new Event('input', { bubbles: true }));
      });
      function up() { if (!down) return; down = false; stage.classList.remove('is-scrubbing'); if (moved) { if (range) range.dispatchEvent(new Event('change', { bubbles: true })); } else if (sw) { sw.click(); } }
      stage.addEventListener('pointerup', up); stage.addEventListener('pointercancel', up);
    })();
    Array.prototype.forEach.call(demo.querySelectorAll('[data-toggle]'), function (el) {
      var cls = el.getAttribute('data-toggle');
      el.addEventListener('click', function () {
        var on = demo.classList.toggle(cls);
        if (el.hasAttribute('aria-expanded')) el.setAttribute('aria-expanded', on ? 'true' : 'false');
        if (el.hasAttribute('aria-pressed')) el.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
    });
    Array.prototype.forEach.call(demo.querySelectorAll('[data-flash]'), function (el) {
      var cls = el.getAttribute('data-flash'), ms = Number(el.getAttribute('data-flash-ms')) || 2000, timer;
      el.addEventListener('click', function () {
        demo.classList.remove(cls);
        void demo.offsetWidth;
        demo.classList.add(cls);
        clearTimeout(timer);
        timer = setTimeout(function () { demo.classList.remove(cls); }, ms);
      });
    });
    // Hover-driven objects: on touch there is no hover, so a tap toggles the same state
    if (window.matchMedia && window.matchMedia('(hover: none)').matches) {
      Array.prototype.forEach.call(demo.querySelectorAll('[data-hover]'), function (el) {
        el.addEventListener('click', function (e) {
          if (e.target.closest('button, input, label, a') && e.target !== el) return;
          el.classList.toggle('is-hover');
        });
      });
    }
    // Sheet gesture: one-to-one drag, rubber band above the top, dismiss by distance or velocity
    var sheet = demo.querySelector('[data-sheet]');
    if (sheet) {
      var ph = sheet.parentNode, openBtn = demo.querySelector('[data-sheet-open]');
      var H = 200, y = 0, startY = 0, startPos = 0, lastY = 0, lastT = 0, vel = 0, dragging = false;
      function paint() {
        sheet.style.setProperty('--y', y + 'px');
        ph.style.setProperty('--ov', String(Math.max(0, Math.min(1, 1 - y / H))));
      }
      function setY(v) { y = v; paint(); }
      function rubber(excess) { var c = 0.55; return (1 - 1 / (excess * c / H + 1)) * H; }
      function open() { ph.classList.remove('is-closed'); sheet.classList.remove('is-leaving'); sheet.classList.add('is-settling'); setY(0); }
      function close() { sheet.classList.remove('is-settling'); sheet.classList.add('is-leaving'); setY(H + 20); setTimeout(function () { ph.classList.add('is-closed'); }, 260); }
      sheet.addEventListener('pointerdown', function (e) {
        dragging = true; startY = e.clientY; startPos = y; lastY = e.clientY; lastT = e.timeStamp; vel = 0;
        sheet.classList.remove('is-settling', 'is-leaving'); sheet.classList.add('is-dragging');
        try { sheet.setPointerCapture(e.pointerId); } catch (err) {}
        e.preventDefault();
      });
      sheet.addEventListener('pointermove', function (e) {
        if (!dragging) return;
        var dt = e.timeStamp - lastT; if (dt > 0) vel = (e.clientY - lastY) / dt * 1000; // px/s
        lastY = e.clientY; lastT = e.timeStamp;
        var d = startPos + (e.clientY - startY);
        setY(d >= 0 ? d : -rubber(-d));
      });
      function release() {
        if (!dragging) return; dragging = false; sheet.classList.remove('is-dragging');
        var byDistance = y > H * 0.25;
        var byVelocity = demo.classList.contains('on-velocity') && vel > 500;
        if (byDistance || byVelocity) close(); else { sheet.classList.add('is-settling'); setY(0); }
      }
      sheet.addEventListener('pointerup', release); sheet.addEventListener('pointercancel', release);
      sheet.addEventListener('keydown', function (e) { if (e.key === 'Escape' || e.key === 'ArrowDown') { close(); e.preventDefault(); } });
      if (openBtn) openBtn.addEventListener('click', open);
      paint();
    }
    // Loading: naive skeleton vs wait-300-keep-500
    var loadBtn = demo.querySelector('[data-load]');
    if (loadBtn) {
      var card = demo.querySelector('.ld-card'), timers = [];
      var loadedOnce = false; demo._replay = function () { if (loadedOnce) loadBtn.click(); };
      loadBtn.addEventListener('click', function () {
        loadedOnce = true; timers.forEach(clearTimeout); timers = [];
        card.classList.remove('is-loaded', 'is-loading');
        var latency = Number(demo.getAttribute('data-latency')) || 200;
        var smart = demo.classList.contains('on-smart');
        var shownAt = null;
        function show() { shownAt = performance.now(); card.classList.add('is-loading'); }
        function done() {
          var wait = 0;
          if (smart && shownAt !== null) wait = Math.max(0, 500 - (performance.now() - shownAt));
          timers.push(setTimeout(function () { card.classList.remove('is-loading'); card.classList.add('is-loaded'); }, wait));
        }
        if (smart) { timers.push(setTimeout(function () { if (!card.classList.contains('is-loaded')) show(); }, 300)); }
        else show();
        timers.push(setTimeout(done, latency));
      });
    }
    // Tabs: indicator follows the active tab
    var tablist = demo.querySelector('[data-tabs]');
    if (tablist) {
      var ind = tablist.querySelector('.tab-ind');
      function moveTo(tab) {
        Array.prototype.forEach.call(tablist.querySelectorAll('[data-tab]'), function (t) { t.classList.toggle('is-active', t === tab); t.setAttribute('aria-selected', t === tab ? 'true' : 'false'); });
        ind.style.setProperty('--x', tab.offsetLeft + 'px'); ind.style.setProperty('--w', tab.offsetWidth + 'px');
      }
      Array.prototype.forEach.call(tablist.querySelectorAll('[data-tab]'), function (t) { t.addEventListener('click', function () { moveTo(t); }); });
      demo._replay = function () { var tabs = tablist.querySelectorAll('[data-tab]'), a = tablist.querySelector('.tab.is-active'), i = Array.prototype.indexOf.call(tabs, a); moveTo(tabs[(i + 1) % tabs.length]); };
      var first = tablist.querySelector('[data-tab]'); if (first) { ind.style.transition = 'none'; moveTo(first); requestAnimationFrame(function () { ind.style.transition = ''; }); }
      if ('ResizeObserver' in window) new ResizeObserver(function () { var a = tablist.querySelector('.tab.is-active'); if (a) moveTo(a); }).observe(tablist);
    }
    // Destructive actions: undo toast vs confirm dialog
    var dlList = demo.querySelector('.dl-list');
    if (dlList) {
      var toast = demo.querySelector('.dl-toast'), confirmBox = demo.querySelector('.dl-confirm'), toastTimer, pendingRow = null;
      function dlCheck() { var gone = dlList.querySelectorAll('.dl-row.is-gone').length, all = dlList.querySelectorAll('.dl-row').length; dlList.classList.toggle('all-gone', gone === all); }
      function dlRemove(row) { row.classList.add('is-gone'); dlCheck(); }
      function showToast(row) {
        pendingRow = row; toast.querySelector('.dl-toast-text').textContent = row.querySelector('span').textContent;
        toast.classList.remove('is-shown'); void toast.offsetWidth; toast.classList.add('is-shown');
        clearTimeout(toastTimer); toastTimer = setTimeout(function () { toast.classList.remove('is-shown'); pendingRow = null; }, 5000);
      }
      Array.prototype.forEach.call(demo.querySelectorAll('[data-del]'), function (btn) {
        btn.addEventListener('click', function () {
          var row = btn.closest('.dl-row');
          if (demo.classList.contains('on-confirm')) { pendingRow = row; confirmBox.querySelector('.dl-confirm-text').textContent = btn.getAttribute('aria-label') + ' “' + row.querySelector('span').textContent + '”?'; confirmBox.classList.add('is-shown'); }
          else { dlRemove(row); showToast(row); }
        });
      });
      demo.querySelector('[data-undo]').addEventListener('click', function () { if (pendingRow) { pendingRow.classList.remove('is-gone'); dlCheck(); } toast.classList.remove('is-shown'); clearTimeout(toastTimer); pendingRow = null; });
      demo.querySelector('[data-cancel]').addEventListener('click', function () { confirmBox.classList.remove('is-shown'); pendingRow = null; });
      demo.querySelector('[data-confirm]').addEventListener('click', function () { if (pendingRow) dlRemove(pendingRow); confirmBox.classList.remove('is-shown'); pendingRow = null; });
      demo.querySelector('[data-restore]').addEventListener('click', function () { Array.prototype.forEach.call(dlList.querySelectorAll('.dl-row'), function (r) { r.classList.remove('is-gone'); }); dlCheck(); });
      toast.addEventListener('mouseenter', function () { clearTimeout(toastTimer); });
      toast.addEventListener('mouseleave', function () { toastTimer = setTimeout(function () { toast.classList.remove('is-shown'); pendingRow = null; }, 2000); });
    }
    // Help before the error: live requirements, error on blur (or eagerly)
    var pw = demo.querySelector('[data-pw]');
    if (pw) {
      var reqs = { len: function (v) { return v.length >= 8; }, num: function (v) { return /\d/.test(v); }, up: function (v) { return /[A-Z]/.test(v); } };
      function pwValid(v) { return Object.keys(reqs).every(function (k) { return reqs[k](v); }); }
      function pwUpdate(fromBlur) {
        var v = pw.value;
        Array.prototype.forEach.call(demo.querySelectorAll('[data-req]'), function (li) { li.classList.toggle('is-met', reqs[li.getAttribute('data-req')](v)); });
        var eager = demo.classList.contains('on-eager');
        if (v.length === 0) demo.classList.remove('has-error');
        else if (pwValid(v)) demo.classList.remove('has-error');
        else if (eager || fromBlur) demo.classList.add('has-error');
      }
      pw.addEventListener('input', function () { pwUpdate(false); });
      demo._replay = function () { if (pw.value) pwUpdate(demo.classList.contains('on-eager')); };
      pw.addEventListener('blur', function () { pwUpdate(true); });
      pw.addEventListener('focus', function () { if (!demo.classList.contains('on-eager')) demo.classList.remove('has-error'); });
    }
    // Keyboard and focus: hold the modifier to reveal shortcuts
    var kb = demo.querySelector('[data-kb]');
    if (kb) {
      function keys(on) { kb.classList.toggle('show-keys', on); }
      document.addEventListener('keydown', function (e) { if (e.key === 'Meta' || e.key === 'Alt' || e.key === 'Control') keys(true); });
      document.addEventListener('keyup', function (e) { if (e.key === 'Meta' || e.key === 'Alt' || e.key === 'Control') keys(false); });
      window.addEventListener('blur', function () { keys(false); });
    }
    // Fitts: submenu with a safe triangle
    var ftMenu = demo.querySelector('[data-fitts]');
    if (ftMenu) {
      var parent = ftMenu.querySelector('[data-parent]'), sub = ftMenu.querySelector('[data-sub]'), tri = ftMenu.querySelector('.ft-tri polygon'), closeTimer, last = null;
      function openSub() { clearTimeout(closeTimer); parent.classList.add('is-open'); }
      function closeSub() { parent.classList.remove('is-open'); ftMenu.classList.remove('is-tracking'); }
      function headingToSub(e) {
        if (!last) return false;
        var r = sub.getBoundingClientRect(), m = ftMenu.getBoundingClientRect();
        var dx = e.clientX - last.x; if (dx <= 0) return false;
        // triângulo: do ponto anterior até os cantos esquerdo-superior e esquerdo-inferior do submenu
        var ax = last.x, ay = last.y, bx = r.left, by = r.top, cx = r.left, cy = r.bottom, px = e.clientX, py = e.clientY;
        function sign(x1, y1, x2, y2, x3, y3) { return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3); }
        var d1 = sign(px, py, ax, ay, bx, by), d2 = sign(px, py, bx, by, cx, cy), d3 = sign(px, py, cx, cy, ax, ay);
        var inside = !((d1 < 0 || d2 < 0 || d3 < 0) && (d1 > 0 || d2 > 0 || d3 > 0));
        tri.setAttribute('points', (ax - m.left) + ',' + (ay - m.top) + ' ' + (bx - m.left) + ',' + (by - m.top) + ' ' + (cx - m.left) + ',' + (cy - m.top));
        return inside;
      }
      parent.addEventListener('pointerenter', openSub);
      ftMenu.addEventListener('pointermove', function (e) {
        var overParent = parent.contains(e.target), overSub = sub.contains(e.target);
        if (overParent && !overSub) { last = { x: e.clientX, y: e.clientY }; ftMenu.classList.add('is-tracking'); return; }
        if (overSub) { clearTimeout(closeTimer); return; }
        if (!parent.classList.contains('is-open')) return;
        var safe = demo.classList.contains('on-safe');
        if (safe && headingToSub(e)) { clearTimeout(closeTimer); closeTimer = setTimeout(closeSub, 300); }
        else closeSub();
      });
      ftMenu.addEventListener('pointerleave', function () { closeTimer = setTimeout(closeSub, 150); });
      sub.addEventListener('pointerenter', function () { clearTimeout(closeTimer); ftMenu.classList.remove('is-tracking'); });
    }
    // Adversarial content: step through cases
    var adName = demo.querySelector('.ad-name');
    if (adName) {
      var cases = (demo.querySelector('.demo-stage').getAttribute('data-cases') || '').split('|');
      function adUpdate() { var i = Number(demo.getAttribute('data-case')) || 0; adName.textContent = cases[i] || cases[0]; adName.setAttribute('title', adName.textContent); }
      var adRange = demo.querySelector('input[name="case"]'); if (adRange) adRange.addEventListener('input', adUpdate); adUpdate();
    }
    // Depth ladder: show the level
    var dpLevel = demo.querySelector('.dp-level b');
    if (dpLevel) { var dpRange = demo.querySelector('input[name="level"]'); function dpUpd() { dpLevel.textContent = dpRange.value; } dpRange.addEventListener('input', dpUpd); dpUpd(); }
    // Swipe to delete: reduced-scale before threshold, fire on release or during
    var swRow = demo.querySelector('[data-swipe]');
    if (swRow) {
      var front = swRow.querySelector('.sw-front'), list = demo.querySelector('.sw-list'), sx0 = 0, swx = 0, swDragging = false, fired = false;
      var W = function () { return swRow.getBoundingClientRect().width; };
      function paintSw(x) { swx = x; front.style.setProperty('--sw-x', x + 'px'); swRow.style.setProperty('--sw-bg', String(Math.min(1, Math.abs(x) / (W() * 0.3)))); }
      function threshold() { return -W() * 0.3; }
      function doDelete() { fired = true; front.classList.remove('is-settling'); front.classList.add('is-leaving'); paintSw(-W()); swRow.classList.add('is-deleted'); list.classList.add('has-deleted'); }
      function swReset() { swRow.classList.remove('is-deleted'); front.classList.remove('is-leaving', 'is-settling'); paintSw(0); fired = false; list.classList.remove('has-deleted'); }
      front.addEventListener('pointerdown', function (e) { if (fired) return; swDragging = true; sx0 = e.clientX - swx; front.classList.remove('is-settling'); front.classList.add('is-dragging'); try { front.setPointerCapture(e.pointerId); } catch (err) {} e.preventDefault(); });
      front.addEventListener('pointermove', function (e) {
        if (!swDragging || fired) return;
        var d = e.clientX - sx0; if (d > 0) d = d * 0.15;
        var t = threshold();
        // antes do limiar, delta em escala reduzida (0.6); depois, 1:1 a partir do limiar
        var x = d > t * 0.6 ? d * 0.6 : t * 0.6 * 0.6 + (d - t * 0.6);
        paintSw(x);
        if (!demo.classList.contains('on-release') && d <= t) { swDragging = false; front.classList.remove('is-dragging'); doDelete(); }
      });
      function swRelease() { if (!swDragging) return; swDragging = false; front.classList.remove('is-dragging'); var d = swx; if (d <= threshold() * 0.6) doDelete(); else { front.classList.add('is-settling'); paintSw(0); } }
      front.addEventListener('pointerup', swRelease); front.addEventListener('pointercancel', swRelease);
      demo.querySelector('[data-swipe-reset]').addEventListener('click', swReset);
    }
    // Context menu: instant in, flash, soft out
    var cmOpen = demo.querySelector('[data-cm-open]');
    if (cmOpen) {
      var cmMenu = demo.querySelector('.cm-menu'), cmTimer;
      cmOpen.addEventListener('click', function () { clearTimeout(cmTimer); cmMenu.classList.remove('is-closing'); cmMenu.classList.toggle('is-open'); });
      demo._replay = function () { if (!cmMenu.classList.contains('is-open')) cmOpen.click(); };
      Array.prototype.forEach.call(cmMenu.querySelectorAll('[role="menuitem"]'), function (item) {
        item.addEventListener('click', function () {
          var dflt = demo.classList.contains('on-default');
          if (dflt) { cmMenu.classList.remove('is-open'); return; }
          item.classList.add('is-flash');
          cmTimer = setTimeout(function () { item.classList.remove('is-flash'); cmMenu.classList.remove('is-open'); cmMenu.classList.add('is-closing'); cmTimer = setTimeout(function () { cmMenu.classList.remove('is-closing'); }, 160); }, 90);
        });
      });
    }
    // Detents: drag with magnetism, snap on release
    var dtTrack = demo.querySelector('[data-detents]');
    if (dtTrack) {
      var knob = dtTrack.querySelector('.dt-knob'), val = demo.querySelector('.dt-val'), kx = 0, kx0 = 0, kDragging = false, lastIdx = 0;
      function range() { return dtTrack.getBoundingClientRect().width - 44; }
      function stops() { var r = range(), a = []; for (var i = 0; i < 5; i++) a.push(r * i / 4); return a; }
      function paintK(x) { kx = x; knob.style.setProperty('--kx', x + 'px'); }
      function nearest(x) { var s = stops(), best = 0; s.forEach(function (v, i) { if (Math.abs(v - x) < Math.abs(s[best] - x)) best = i; }); return best; }
      function setIdx(i, animate) { lastIdx = i; knob.setAttribute('aria-valuenow', String(i)); if (val) val.textContent = String(i + 1) + ' / 5'; if (animate) knob.classList.add('is-settling'); paintK(stops()[i]); }
      knob.addEventListener('pointerdown', function (e) { kDragging = true; kx0 = e.clientX - kx; knob.classList.remove('is-settling'); knob.classList.add('is-dragging'); try { knob.setPointerCapture(e.pointerId); } catch (err) {} e.preventDefault(); });
      knob.addEventListener('pointermove', function (e) {
        if (!kDragging) return;
        var r = range(), x = Math.max(0, Math.min(r, e.clientX - kx0));
        if (demo.classList.contains('on-snap')) {
          var s = stops(), i = nearest(x), d = x - s[i], pull = 14;
          if (Math.abs(d) < pull) x = s[i] + d * 0.35; // ímã perto do encaixe
          if (i !== lastIdx) { lastIdx = i; knob.classList.remove('is-tick'); void knob.offsetWidth; knob.classList.add('is-tick'); if (val) val.textContent = String(i + 1) + ' / 5'; }
        } else if (val) { val.textContent = Math.round(x / r * 100) + '%'; }
        paintK(x);
      });
      function kRelease() { if (!kDragging) return; kDragging = false; knob.classList.remove('is-dragging'); if (demo.classList.contains('on-snap')) setIdx(nearest(kx), true); }
      knob.addEventListener('pointerup', kRelease); knob.addEventListener('pointercancel', kRelease);
      knob.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { setIdx(Math.min(4, lastIdx + 1), true); e.preventDefault(); } if (e.key === 'ArrowLeft') { setIdx(Math.max(0, lastIdx - 1), true); e.preventDefault(); } });
      setIdx(0, false);
      if ('ResizeObserver' in window) new ResizeObserver(function () { if (!kDragging) setIdx(lastIdx, false); }).observe(dtTrack);
    }
    // AI demos ---------------------------------------------------------------
    var aiS = demo.querySelector('.demo-stage');
    function ga(n) { return aiS ? (aiS.getAttribute('data-' + n) || '') : ''; }
    function aiOn(fn) { Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (i) { i.addEventListener('input', fn); i.addEventListener('change', fn); }); fn(); }
    var aiTouch = window.matchMedia && window.matchMedia('(hover: none)').matches;
    var aiOut = demo.querySelector('.demo-controls output');
    // 01 reliance: five extracted values; certainty shown vs reliability had
    var airW = demo.querySelector('.air-wrap');
    if (airW) {
      var airCards = Array.prototype.slice.call(airW.querySelectorAll('.air-card')), airRead = airW.querySelector('.air-read');
      var airClaims = ga('claims').split('|'), airSrcs = ga('srcs').split('|'), airWrong = ga('wrong').split('|'), airWrongSet = { 60: [1, 3], 80: [3], 100: [] };
      function airStatus() {
        var acc = airCards.filter(function (c) { return c.classList.contains('is-accepted'); }), shipped = acc.filter(function (c) { return c.classList.contains('is-wrong'); }).length;
        var left = airCards.filter(function (c) { return c.classList.contains('is-wrong') && !c.classList.contains('is-accepted'); }).length;
        var rel = Number(demo.getAttribute('data-rel')) || 60, conf = Number(demo.getAttribute('data-conf')) || 0, gap = conf - rel, band = gap > 10 ? 'over' : gap < -45 ? 'under' : 'cal';
        airW.setAttribute('data-band', band);
        airRead.innerHTML = (acc.length ? '<b>' + acc.length + '/5 ' + ga('accepted') + ' · ' + shipped + ' ' + ga('shipped') + (left ? ' · ' + left + ' ' + ga('caught') : '') + '</b><br>' : '') + ga(band);
      }
      function airRender() {
        var rel = Number(demo.getAttribute('data-rel')) || 60, conf = Number(demo.getAttribute('data-conf')) || 0, wrong = airWrongSet[rel] || [];
        var cert = conf < 40 ? 'd' : conf < 75 ? 's' : 'a';
        airCards.forEach(function (c, i) {
          var w = wrong.indexOf(i) >= 0; c.classList.toggle('is-wrong', w); c.classList.remove('is-accepted');
          c.querySelector('.air-claim').textContent = airClaims[i]; c.querySelector('.air-src').textContent = w ? airWrong[i] : airSrcs[i];
          c.setAttribute('data-cert', cert); c.querySelector('.air-tag').textContent = ga(cert === 'd' ? 'td' : cert === 's' ? 'ts' : 'ta'); c.querySelector('.air-res').textContent = '';
          c.style.setProperty('--srco', String(Math.max(0, 1 - conf / 75)));
        });
        airStatus();
      }
      airCards.forEach(function (c) { c.addEventListener('click', function () { var on = c.classList.toggle('is-accepted'); c.querySelector('.air-res').textContent = on ? (c.classList.contains('is-wrong') ? ga('wrongtag') : '✓') : ''; airStatus(); }); });
      aiOn(airRender); demo._replay = function () {};
    }
    // 02 comparative advantage: exact outcome vs messy input
    var aibW = demo.querySelector('.aib-wrap');
    if (aibW) {
      var aibSeg = aibW.querySelectorAll('.aib-seg-b'), aibOut = aibW.querySelector('.aib-chat-out'), aibRes1 = aibW.querySelector('.aib-res1'), aibRes2 = aibW.querySelector('.aib-res2'), aibRow2 = aibW.querySelectorAll('.aib-row')[1], aibCands = aibW.querySelector('.aib-cands'), aibSum = aibW.querySelector('.aib-sum'), aibT, aibT2, aibSummed = false;
      Array.prototype.forEach.call(aibSeg, function (b) { b.addEventListener('click', function () { Array.prototype.forEach.call(aibSeg, function (x) { x.classList.remove('is-on'); }); b.classList.add('is-on'); aibRes1.className = 'aib-res aib-res1 is-fast'; aibRes1.textContent = b.textContent === ga('done') ? ga('resseg') : b.textContent; }); });
      aibW.querySelector('.aib-send').addEventListener('click', function () { clearTimeout(aibT); aibOut.classList.add('is-on'); aibOut.textContent = ga('thinking'); aibRes1.className = 'aib-res aib-res1'; aibRes1.textContent = ''; aibT = setTimeout(function () { aibOut.textContent = ga('chatout'); Array.prototype.forEach.call(aibSeg, function (x, i) { x.classList.toggle('is-on', i === 2); }); aibRes1.className = 'aib-res aib-res1 is-slow'; aibRes1.textContent = ga('reschat'); }, 1100); });
      function aibRenderCands() {
        var list = ga('cands').split('|'), multi = demo.classList.contains('on-multi'); aibCands.innerHTML = '';
        list.slice(0, multi ? 4 : 1).forEach(function (txt, i) { var b = document.createElement('button'); b.type = 'button'; b.className = 'aib-cand'; b.innerHTML = (multi ? '<small>' + (i + 1) + '/4</small>' : '') + txt; b.addEventListener('click', function () { if (!multi) { aibSummarize(); return; } Array.prototype.forEach.call(aibCands.children, function (x) { x.classList.remove('is-picked'); }); b.classList.add('is-picked'); aibRes2.textContent = ga('respick').replace('%d', i + 1); }); aibCands.appendChild(b); });
        aibRes2.textContent = multi ? '' : ga('resone');
      }
      function aibSummarize() { clearTimeout(aibT2); aibSummed = true; aibCands.innerHTML = ''; aibRes2.textContent = ''; aibRow2.classList.add('is-gen'); aibSum.disabled = true; aibT2 = setTimeout(function () { aibRow2.classList.remove('is-gen'); aibSum.disabled = false; aibRenderCands(); }, 900); }
      aibSum.addEventListener('click', aibSummarize);
      demo._replay = function () { if (aibSummed) aibRenderCands(); if (demo.classList.contains('on-aifront')) { if (!aibOut.classList.contains('is-on')) aibW.querySelector('.aib-send').click(); } else { aibOut.classList.remove('is-on'); } };
    }
    // 03 pattern by task
    var aipW = demo.querySelector('.aip-wrap');
    if (aipW) {
      var aipTask = aipW.querySelector('.aip-task'), aipRead = aipW.querySelector('.aip-read'), aipGhost = aipW.querySelector('.aip-ghost'), aipRun = aipW.querySelector('.aip-run'), aipLis = aipW.querySelectorAll('.aip-plan li'), aipT;
      aiOn(function () { var s = demo.getAttribute('data-stakes') || '1'; aipTask.textContent = ga('t' + s); if (aiOut) aiOut.textContent = ga('o' + s); var chat = demo.classList.contains('on-chat'); aipRead.textContent = chat ? ga('m' + s) : ''; aipW.setAttribute('data-fit', chat && s !== '2' ? 'bad' : 'ok'); });
      function aipAccept() { aipGhost.classList.add('is-accepted'); }
      aipGhost.addEventListener('click', aipAccept); aipGhost.addEventListener('keydown', function (e) { if (e.key === 'Tab' || e.key === 'Enter') { e.preventDefault(); aipAccept(); } });
      aipRun.addEventListener('click', function () { clearTimeout(aipT); Array.prototype.forEach.call(aipLis, function (li) { li.classList.remove('is-done', 'is-active'); }); aipRun.disabled = true; var i = 0; function step() { if (i > 0) { aipLis[i - 1].classList.remove('is-active'); aipLis[i - 1].classList.add('is-done'); } if (i < aipLis.length) { aipLis[i].classList.add('is-active'); i++; aipT = setTimeout(step, 550); } else { aipRun.disabled = false; aipRead.textContent = ga('done'); } } step(); });
      demo._replay = function () { aipGhost.classList.remove('is-accepted'); };
    }
    // 04 expectations: capability line, prompts, draft framing
    var aixW = demo.querySelector('.aix-wrap');
    if (aixW) {
      var aixField = aixW.querySelector('.aix-field'), aixVal = aixW.querySelector('.aix-val'), aixOut = aixW.querySelector('.aix-out'), aixP = aixOut.querySelector('p'), aixRead = aixW.querySelector('.aix-read');
      Array.prototype.forEach.call(aixW.querySelectorAll('.aix-chip'), function (c) { c.addEventListener('click', function () { aixVal.textContent = c.textContent; aixField.classList.add('is-filled'); aixOut.classList.remove('is-on'); void aixOut.offsetWidth; aixP.textContent = ga('o' + c.getAttribute('data-i')); aixP.removeAttribute('contenteditable'); aixOut.classList.add('is-on'); aixRead.textContent = ''; }); });
      function aixBlank() { aixRead.textContent = demo.classList.contains('on-prompts') ? '' : ga('blank'); }
      aixField.addEventListener('click', aixBlank); aixField.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); aixBlank(); } });
      aixW.querySelector('.aix-send').addEventListener('click', function () { aixOut.classList.remove('is-on'); aixField.classList.remove('is-filled'); aixVal.textContent = ''; });
      aixW.querySelector('.aix-edit').addEventListener('click', function () { aixP.setAttribute('contenteditable', 'true'); aixP.focus(); });
      aixP.addEventListener('blur', function () { aixP.removeAttribute('contenteditable'); });
      demo._replay = function () { aixRead.textContent = ''; };
    }
    // 05 honesty: label, depth by audience, no fake person
    var aihW = demo.querySelector('.aih-wrap');
    if (aihW) {
      var aihName = aihW.querySelector('.aih-name b'), aihRole = aihW.querySelector('.aih-name small'), aihMsg = aihW.querySelector('.aih-msg'), aihRead = aihW.querySelector('.aih-read');
      aiOn(function () { var h = demo.classList.contains('on-human'), lv = demo.getAttribute('data-level') || '0'; aihName.textContent = ga(h ? 'nh' : 'na'); aihRole.textContent = ga(h ? 'rh' : 'ra'); aihMsg.textContent = ga(h ? 'mh' : 'ma'); aihRead.textContent = ga(h ? 'warn' : 'ok'); if (aiOut) aiOut.textContent = ga('lv' + lv); });
      demo._replay = function () {};
    }
    // 06 provenance: passage on hover, score hides everything
    var aivW = demo.querySelector('.aiv-wrap');
    if (aivW) {
      var aivRead = aivW.querySelector('.aiv-read');
      function aivShow(n) { if (demo.classList.contains('on-score')) { aivW.setAttribute('data-show', ''); aivRead.textContent = n ? ga('none') : ''; return; } aivW.setAttribute('data-show', n || ''); aivRead.textContent = n ? '' : ga('hint'); }
      Array.prototype.forEach.call(aivW.querySelectorAll('.aiv-claim'), function (c) { var n = c.getAttribute('data-n');
        if (!aiTouch) { c.addEventListener('mouseenter', function () { aivShow(n); }); c.addEventListener('mouseleave', function () { aivShow(''); }); }
        c.addEventListener('focus', function () { aivShow(n); }); c.addEventListener('blur', function () { aivShow(''); });
        c.addEventListener('click', function () { aivShow(aivW.getAttribute('data-show') === n ? '' : n); }); });
      aiOn(function () { aivShow(''); }); demo._replay = function () {};
    }
    // 07 agenda and sycophancy
    var aigW = demo.querySelector('.aig-wrap');
    if (aigW) {
      var aigThread = aigW.querySelector('.aig-thread'), aigU = aigW.querySelector('.aig-user span'), aigR = aigW.querySelector('.aig-reply'), aigLast = null, aigT;
      function aigRun(btn) { aigLast = btn; var q = btn.getAttribute('data-q'); aigThread.classList.remove('is-asked', 'is-replied'); void aigThread.offsetWidth; aigU.textContent = btn.textContent; aigThread.classList.add('is-asked'); clearTimeout(aigT); aigT = setTimeout(function () { aigR.textContent = q === '1' ? ga('r1') : ga(demo.classList.contains('on-flatter') ? 'r2f' : 'r2h'); aigThread.classList.add('is-replied'); }, 500); }
      Array.prototype.forEach.call(aigW.querySelectorAll('.aig-ask'), function (b) { b.addEventListener('click', function () { aigRun(b); }); });
      demo._replay = function () { aigRun(aigLast || aigW.querySelectorAll('.aig-ask')[1]); };
    }
    // 08 intelligibility: plan, trace, five questions
    var aiiW = demo.querySelector('.aii-wrap');
    if (aiiW) {
      var aiiLis = aiiW.querySelectorAll('.aii-plan li'), aiiRes = aiiW.querySelector('.aii-res'), aiiA = aiiW.querySelector('.aii-a'), aiiQs = aiiW.querySelectorAll('.aii-q button'), aiiRunBtn = aiiW.querySelector('.aii-run'), aiiT = [];
      function aiiClear() { aiiT.forEach(clearTimeout); aiiT = []; Array.prototype.forEach.call(aiiLis, function (l) { l.classList.remove('is-done', 'is-active'); }); Array.prototype.forEach.call(aiiQs, function (b) { b.classList.remove('is-on'); }); aiiA.innerHTML = ''; }
      function aiiFinish(blind) { aiiW.classList.toggle('is-blind', blind); aiiRes.textContent = ga(blind ? 'blind' : 'res'); aiiW.setAttribute('data-phase', 'done'); }
      function aiiTrace() { aiiW.setAttribute('data-phase', 'trace'); var i = 0; function step() { if (i > 0) { aiiLis[i - 1].classList.remove('is-active'); aiiLis[i - 1].classList.add('is-done'); } if (i < aiiLis.length) { aiiLis[i].classList.add('is-active'); i++; aiiT.push(setTimeout(step, 500)); } else aiiT.push(setTimeout(function () { aiiFinish(false); }, 250)); } step(); }
      aiiRunBtn.addEventListener('click', function () { aiiClear(); if (demo.classList.contains('on-plan')) aiiW.setAttribute('data-phase', 'plan'); else { aiiW.setAttribute('data-phase', 'spin'); aiiT.push(setTimeout(function () { aiiFinish(true); }, 1500)); } });
      aiiW.querySelector('.aii-go').addEventListener('click', aiiTrace);
      aiiW.querySelector('.aii-cancel').addEventListener('click', function () { aiiClear(); aiiW.removeAttribute('data-phase'); });
      Array.prototype.forEach.call(aiiQs, function (b) { b.addEventListener('click', function () { var on = b.classList.contains('is-on'); Array.prototype.forEach.call(aiiQs, function (x) { x.classList.remove('is-on'); }); if (on) { aiiA.innerHTML = ''; return; } b.classList.add('is-on'); aiiA.innerHTML = ga('a' + b.getAttribute('data-q')); }); });
      demo._replay = function () { aiiRunBtn.click(); };
    }
    // 09 control: Tab accepts, Esc dismisses, typing over ignores; the dialog anti-pattern
    var aicW = demo.querySelector('.aic-wrap');
    if (aicW) {
      var aicEd = aicW.querySelector('.aic-editor'), aicTyped = aicW.querySelector('.aic-typed'), aicGhost = aicW.querySelector('.aic-ghost'), aicRead = aicW.querySelector('.aic-read'), aicPrev = '';
      function aicReset() { aicTyped.textContent = ga('typed'); aicGhost.textContent = ga('ghost'); aicW.classList.add('has-sugg'); aicW.classList.remove('is-accepted'); aicRead.textContent = ''; }
      function aicAccept(viaModal) { aicPrev = aicTyped.textContent; aicTyped.textContent += aicGhost.textContent; aicGhost.textContent = ''; aicW.classList.remove('has-sugg'); aicW.classList.add('is-accepted'); aicRead.textContent = ga(viaModal ? 'macc' : 'acc'); }
      function aicDismiss(viaModal, over) { aicGhost.textContent = ''; aicW.classList.remove('has-sugg'); aicRead.textContent = ga(viaModal ? 'mdis' : over ? 'over' : 'dis'); }
      aicEd.addEventListener('keydown', function (e) {
        var has = aicW.classList.contains('has-sugg'), modal = demo.classList.contains('on-modal');
        if (modal && has) { if (e.key !== 'Tab') e.preventDefault(); return; }
        if (e.key === 'Tab' && has) { e.preventDefault(); aicAccept(false); }
        else if (e.key === 'Escape' && has) { e.preventDefault(); e.stopPropagation(); aicDismiss(false); }
        else if (e.key === 'Backspace') { e.preventDefault(); aicTyped.textContent = aicTyped.textContent.slice(0, -1); }
        else if (e.key.length === 1 && !e.metaKey && !e.ctrlKey && !e.altKey) { e.preventDefault(); if (has) aicDismiss(false, true); aicTyped.textContent += e.key; }
      });
      aicGhost.addEventListener('click', function () { aicEd.focus(); aicAccept(false); });
      aicW.querySelector('.aic-yes').addEventListener('click', function () { aicAccept(true); }); aicW.querySelector('.aic-no').addEventListener('click', function () { aicDismiss(true); });
      aicW.querySelector('.aic-undo').addEventListener('click', function () { aicTyped.textContent = aicPrev; aicW.classList.remove('is-accepted'); aicGhost.textContent = ga('ghost'); aicW.classList.add('has-sugg'); aicRead.textContent = ''; });
      aicW.querySelector('.aic-again').addEventListener('click', aicReset);
      aicReset(); demo._replay = aicReset;
    }
    // 10 timing: suggestion where the attention is; whose rule
    var aitW = demo.querySelector('.ait-wrap');
    if (aitW) {
      var aitNote = aitW.querySelector('.ait-note');
      Array.prototype.forEach.call(aitW.querySelectorAll('.ait-pane'), function (p) { function f() { aitW.setAttribute('data-focus', p.getAttribute('data-pane')); if (!aitW.classList.contains('is-off')) aitNote.textContent = ''; } p.addEventListener('click', f); p.addEventListener('focus', f); });
      aitW.querySelector('.ait-off').addEventListener('click', function (e) { e.stopPropagation(); aitW.classList.add('is-off'); aitNote.textContent = ga('off'); });
      aitNote.textContent = ga('focus');
      var aitAcross = demo.querySelector('.demo-controls input[name="across"]'), aitRule = demo.querySelector('.demo-controls input[name="rule"]');
      if (aitAcross) aitAcross.addEventListener('change', function () { if (aitAcross.checked) aitW.setAttribute('data-focus', 'read'); else if (!aitW.getAttribute('data-focus')) aitW.setAttribute('data-focus', 'comp'); });
      if (aitRule) aitRule.addEventListener('change', function () { if (!aitW.getAttribute('data-focus')) aitW.setAttribute('data-focus', 'comp'); });
      demo._replay = function () { if (aitW.classList.contains('is-off')) { aitW.classList.remove('is-off'); aitNote.textContent = ''; } };
    }
    // 11 failure: checkpoints, hedging
    var aifW = demo.querySelector('.aif-wrap');
    if (aifW) {
      var aifV = [aifW.querySelector('.aif-v1'), aifW.querySelector('.aif-v2'), aifW.querySelector('.aif-v3')], aifSteps = aifW.querySelectorAll('.aif-step'), aifRead = aifW.querySelector('.aif-read'), aifT = [];
      function aifClean(b) { b.classList.remove('is-new', 'is-bad', 'is-hedged'); }
      function aifReset() { aifT.forEach(clearTimeout); aifT = []; aifV[0].textContent = ga('raw'); aifV[1].textContent = '—'; aifV[2].textContent = '—'; aifV.forEach(aifClean); Array.prototype.forEach.call(aifSteps, function (s) { s.classList.remove('is-done', 'is-active', 'is-bad'); }); aifW.classList.remove('is-broken'); aifRead.textContent = ''; }
      aifW.querySelector('.aif-run').addEventListener('click', function () {
        aifReset(); var hedge = demo.classList.contains('on-hedge'), i = 0;
        function step() {
          Array.prototype.forEach.call(aifSteps, function (s, k) { s.classList.toggle('is-active', k === i); if (k < i) s.classList.add('is-done'); });
          if (i === 0) { aifV[0].textContent = ga('v1'); aifV[0].classList.add('is-new'); }
          else if (i === 1) { aifV[1].textContent = ga('v2'); aifV[1].classList.add('is-new'); }
          else if (i === 2) { aifV[2].textContent = ga(hedge ? 'fch' : 'fcp'); aifV[2].classList.add(hedge ? 'is-hedged' : 'is-new'); aifV[0].textContent = ga('fcp'); aifClean(aifV[0]); aifV[0].classList.add('is-bad'); aifSteps[2].classList.add('is-bad'); aifW.classList.add('is-broken'); aifRead.textContent = ga('wrong'); }
          i++; if (i < 3) aifT.push(setTimeout(step, 600)); else aifT.push(setTimeout(function () { aifSteps[2].classList.remove('is-active'); aifSteps[2].classList.add('is-done'); }, 600));
        }
        step();
      });
      aifW.querySelector('.aif-back').addEventListener('click', function () { aifV[0].textContent = ga('v1'); aifClean(aifV[0]); aifV[0].classList.add('is-new'); aifV[2].textContent = '—'; aifClean(aifV[2]); aifSteps[2].classList.remove('is-bad', 'is-done', 'is-active'); aifW.classList.remove('is-broken'); aifRead.textContent = ga('back'); });
      aifW.querySelector('.aif-restore').addEventListener('click', function () { aifReset(); aifRead.textContent = ga('restore'); });
      demo._replay = function () { aifW.querySelector('.aif-run').click(); };
    }
    // 12 co-creation: regenerate by paragraph, review at publish
    var aimW = demo.querySelector('.aim-wrap');
    if (aimW) {
      var aimPs = Array.prototype.slice.call(aimW.querySelectorAll('.aim-p')), aimRead = aimW.querySelector('.aim-read'), aimRev = aimW.querySelector('.aim-review span'), aimState = [0, 0, 0], aimPub = [0, 0, 0];
      function aimSwap(i) { aimState[i] = 1 - aimState[i]; var p = aimPs[i].querySelector('p'); aimPs[i].classList.remove('is-swapping'); void p.offsetWidth; p.textContent = ga('p' + i + (aimState[i] ? 'b' : 'a')); aimPs[i].classList.add('is-swapping'); aimPs[i].classList.toggle('is-changed', aimState[i] !== aimPub[i]); aimRead.textContent = ''; aimW.classList.remove('is-blind'); }
      aimPs.forEach(function (p, i) { p.querySelector('.aim-re').addEventListener('click', function () { aimSwap(i); }); });
      aimW.querySelector('.aim-reall').addEventListener('click', function () { aimPs.forEach(function (p, i) { aimSwap(i); }); });
      function aimChanged() { return aimState.filter(function (s, i) { return s !== aimPub[i]; }).length; }
      function aimDoPublish(blind) { var n = aimChanged(); aimPub = aimState.slice(); aimPs.forEach(function (p) { p.classList.remove('is-changed'); }); aimW.classList.remove('is-reviewing'); aimW.classList.toggle('is-blind', blind && n > 0); aimRead.textContent = blind && n ? ga('blind').replace('%d', n) : ga('pubd'); }
      aimW.querySelector('.aim-pub').addEventListener('click', function () { if (!demo.classList.contains('on-friction')) { aimDoPublish(true); return; } var n = aimChanged(); if (!n) { aimRead.textContent = ga('none'); return; } aimRev.textContent = ga('rev').replace('%d', n); aimW.classList.add('is-reviewing'); });
      aimW.querySelector('.aim-confirm').addEventListener('click', function () { aimDoPublish(false); }); aimW.querySelector('.aim-cancel').addEventListener('click', function () { aimW.classList.remove('is-reviewing'); });
      var aimFr = demo.querySelector('.demo-controls input[name="friction"]');
      if (aimFr) aimFr.addEventListener('change', function () { if (!aimChanged()) aimSwap(1); setTimeout(function () { aimW.querySelector('.aim-pub').click(); }, 0); });
      demo._replay = function () {};
    }
    // 13 autonomy: posture per action, content is data
    var aiaW = demo.querySelector('.aia-wrap');
    if (aiaW) {
      var aiaActs = Array.prototype.slice.call(aiaW.querySelectorAll('.aia-act')), aiaAsk = aiaW.querySelector('.aia-ask'), aiaAskT = aiaAsk.querySelector('span'), aiaRead = aiaW.querySelector('.aia-read'), aiaPending = null;
      function aiaState(a, txt, cls) { a.classList.remove('is-ran', 'is-denied', 'is-injected', 'is-pending'); if (cls) a.classList.add(cls); a.querySelector('.aia-state').textContent = txt; }
      function aiaRun(a) {
        var post = a.getAttribute('data-post');
        if (post === 'auto') { aiaState(a, ga('ran'), 'is-ran'); aiaW.classList.add('is-read'); if (demo.classList.contains('on-boundary')) { aiaRead.textContent = ga('quoted'); aiaW.classList.remove('is-hurt'); } else { aiaState(aiaActs[3], ga('ran') + ' ⚠', 'is-injected'); aiaRead.textContent = ga('injected'); aiaW.classList.add('is-hurt'); } }
        else if (post === 'notify') { aiaState(a, ga('ran') + ' · ' + ga('undo'), 'is-ran'); }
        else { aiaPending = a; aiaActs.forEach(function (x) { x.classList.remove('is-pending'); }); a.classList.add('is-pending'); aiaAskT.textContent = ga('askfor').replace('%s', a.querySelector('.aia-what').textContent); aiaW.classList.add('is-asking'); }
      }
      aiaActs.forEach(function (a) { a.addEventListener('click', function () { if (a.classList.contains('is-ran') && a.getAttribute('data-post') === 'notify') { aiaState(a, ga('pnotify'), ''); return; } aiaRun(a); }); });
      aiaW.querySelector('.aia-ok').addEventListener('click', function () { if (aiaPending) aiaState(aiaPending, ga('approved'), 'is-ran'); aiaW.classList.remove('is-asking'); aiaPending = null; });
      aiaW.querySelector('.aia-deny').addEventListener('click', function () { if (aiaPending) aiaState(aiaPending, ga('denied'), 'is-denied'); aiaW.classList.remove('is-asking'); aiaPending = null; });
      function aiaReset() { aiaActs.forEach(function (a) { aiaState(a, ga('p' + a.getAttribute('data-post')), ''); }); aiaW.classList.remove('is-read', 'is-asking', 'is-hurt'); aiaRead.textContent = ''; aiaPending = null; }
      demo._replay = function () { var wasRead = aiaW.classList.contains('is-read'); aiaReset(); if (wasRead) aiaRun(aiaActs[0]); };
    }
    // 14 wait: named stages, sources as they arrive, effort with a cost line
    var aiwW = demo.querySelector('.aiw-wrap');
    if (aiwW) {
      var aiwSts = aiwW.querySelectorAll('.aiw-st'), aiwSrcs = aiwW.querySelector('.aiw-srcs'), aiwCost = aiwW.querySelector('.aiw-cost'), aiwT = [], aiwRan = false;
      aiOn(function () { if (aiOut) aiOut.textContent = ga('e' + (demo.getAttribute('data-effort') || '2')); });
      function aiwRun() {
        aiwRan = true; aiwT.forEach(clearTimeout); aiwT = []; aiwSrcs.innerHTML = ''; aiwW.classList.remove('is-done'); Array.prototype.forEach.call(aiwSts, function (s) { s.classList.remove('is-active', 'is-done'); }); aiwW.classList.add('is-running');
        var e = Number(demo.getAttribute('data-effort')) || 2, n = e * 2, list = ga('srcs').split('|').slice(0, n), per = 380, t0 = 500, tRead = n * per, tWrite = 600, total = t0 + tRead + tWrite;
        function stage(i) { Array.prototype.forEach.call(aiwSts, function (s, k) { s.classList.toggle('is-active', k === i); s.classList.toggle('is-done', k < i); }); }
        stage(0); aiwT.push(setTimeout(function () { stage(1); }, t0));
        list.forEach(function (s, k) { aiwT.push(setTimeout(function () { var li = document.createElement('li'); li.textContent = s; aiwSrcs.appendChild(li); }, t0 + k * per)); });
        aiwT.push(setTimeout(function () { stage(2); }, t0 + tRead));
        aiwT.push(setTimeout(function () { stage(3); aiwW.classList.remove('is-running'); aiwW.classList.add('is-done'); aiwCost.textContent = ga('cost').replace('%s', ga('e' + e)).replace('%d', String(n)).replace('%s', (total / 1000).toFixed(1)); }, total));
      }
      aiwW.querySelector('.aiw-ask').addEventListener('click', aiwRun);
      demo._replay = aiwRun;
    }
    // Practice demos --------------------------------------------------------
    var stg = demo.querySelector('.demo-stage');
    var exV = demo.querySelector('.xt-verdict');
    if (exV) { function exUpd() { var n = Number(demo.getAttribute('data-occ')) || 1; exV.textContent = demo.classList.contains('on-early') ? stg.getAttribute('data-early') : stg.getAttribute(n >= 3 ? 'data-v3' : n === 2 ? 'data-v2' : 'data-v1'); } Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (i) { i.addEventListener('input', exUpd); i.addEventListener('change', exUpd); }); exUpd(); }
    var ptList = demo.querySelector('.pt-list');
    if (ptList) {
      var ptRead = demo.querySelector('.pt-read'), ptDrag = null, ptX = 0;
      ptList.addEventListener('pointerdown', function (e) { var it = e.target.closest('.pt-item'); if (!it) return; if (!demo.classList.contains('on-inter')) { ptRead.textContent = stg.getAttribute('data-noint'); return; } ptDrag = it; ptX = e.clientX; it.classList.add('is-dragging'); try { ptList.setPointerCapture(e.pointerId); } catch (x) {} });
      ptList.addEventListener('pointermove', function (e) { if (!ptDrag) return; var dx = Math.max(0, e.clientX - ptX); ptDrag.style.transform = 'translateX(' + dx + 'px)'; ptDrag.style.opacity = 1 - dx / 240; });
      function ptEnd(e) { if (!ptDrag) return; var dx = e ? e.clientX - ptX : 0; ptDrag.classList.remove('is-dragging'); ptDrag.style.transform = ''; ptDrag.style.opacity = ''; if (dx > 70) { var it = ptDrag; it.classList.add('is-gone'); ptRead.textContent = it.firstChild.textContent + ' · ' + stg.getAttribute('data-dismissed'); setTimeout(function () { it.remove(); if (!ptList.children.length) { ptList.innerHTML = ptList.getAttribute('data-orig'); } }, 260); } ptDrag = null; }
      ptList.setAttribute('data-orig', ptList.innerHTML);
      ptList.addEventListener('pointerup', ptEnd); ptList.addEventListener('pointercancel', function () { ptEnd(null); });
    }
    var gnGrid = demo.querySelector('.gn-grid');
    if (gnGrid) {
      var gnRead = demo.querySelector('.gn-read'), gnT0 = 0;
      function gnRender() { gnGrid.innerHTML = ''; for (var i = 1; i <= 5; i++) { var c = document.createElement('div'); c.className = 'gn-card v' + i + (demo.classList.contains('on-system') ? ' gn-sys' : ''); var hostile = demo.classList.contains('on-hostile'); c.innerHTML = '<b>' + (hostile ? stg.getAttribute('data-long') : stg.getAttribute('data-title')) + '</b><span>' + (hostile ? stg.getAttribute('data-long') : '$29 / mo') + '</span><i>' + stg.getAttribute('data-cta') + '</i>'; c.addEventListener('click', function () { c.classList.toggle('is-reviewed'); gnStatus(); }); gnGrid.appendChild(c); } gnT0 = performance.now(); gnStatus(); }
      function gnStatus() { var n = gnGrid.querySelectorAll('.is-reviewed').length, broken = demo.classList.contains('on-hostile') && !demo.classList.contains('on-system') ? 3 : 0; gnRead.textContent = stg.getAttribute('data-gen') + ' · ' + n + '/5 ' + stg.getAttribute('data-rev') + (n === 5 ? ' (' + Math.round((performance.now() - gnT0) / 1000) + 's)' : '') + (broken ? ' · ' + broken + ' ' + stg.getAttribute('data-broken') : ''); }
      demo.querySelector('.gn-btn').addEventListener('click', gnRender);
      demo._replay = function () { if (gnGrid.children.length) gnRender(); };
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (i) { i.addEventListener('change', function () { if (gnGrid.children.length) gnRender(); }); });
    }
    var ppGrid = demo.querySelector('.pp2-grid');
    if (ppGrid) {
      var ppProps = stg.getAttribute('data-props').split('|'), ppPieces = stg.getAttribute('data-pieces').split('|');
      function ppUpd() { var n = Number(demo.getAttribute('data-bools')) || 6, combos = Math.pow(2, n), compose = demo.classList.contains('on-compose'); demo.querySelector('.pp2-props').innerHTML = ppProps.slice(0, n).map(function (p) { return '<span>' + p + '</span>'; }).join(''); demo.querySelector('.pp2-n').textContent = compose ? ppPieces.length : combos.toLocaleString(); demo.querySelector('.pp2-l').textContent = compose ? stg.getAttribute('data-valid') : stg.getAttribute('data-combos'); var html = ''; var shown = Math.min(combos, 96); for (var i = 0; i < shown; i++) html += '<i' + (i < Math.min(6, combos) ? ' class="ok"' : '') + '></i>'; if (combos > shown) html += '<em>+' + (combos - shown).toLocaleString() + '</em>'; html += ppPieces.map(function (p) { return '<span class="pp2-piece">' + p + '</span>'; }).join(''); ppGrid.innerHTML = html; }
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (i) { i.addEventListener('input', ppUpd); i.addEventListener('change', ppUpd); }); ppUpd();
    }
    var ctComp = demo.querySelector('.ct-comp');
    if (ctComp) {
      var ctLog = demo.querySelector('.ct-log'), ctOpen = false;
      function ctLogLine(t, ignored) { var l = document.createElement('span'); l.textContent = t; if (ignored) l.className = 'is-ignored'; ctLog.prepend(l); while (ctLog.children.length > 4) ctLog.lastChild.remove(); }
      function ctSet(v, source) { ctOpen = v; ctComp.classList.toggle('is-open', v); demo.querySelector('.ct-head').setAttribute('aria-expanded', v ? 'true' : 'false'); if (demo.classList.contains('on-notify')) ctLogLine('onOpenChange(' + v + ') ← ' + source); }
      demo.querySelector('.ct-head').addEventListener('click', function () { ctSet(!ctOpen, 'click'); });
      demo._replay = function () {};
      demo.querySelector('.ct-ext').addEventListener('click', function () { if (demo.classList.contains('on-controlled')) ctSet(!ctOpen, '⌘.'); else ctLogLine('⌘. ' + stg.getAttribute('data-ignored'), true); });
    }
    var esRead = demo.querySelector('.es-read');
    if (esRead) { function esUpd() { var n = Number(demo.getAttribute('data-rogue')) || 0, closed = demo.classList.contains('on-closed'); esRead.textContent = closed ? (n ? n + ' ' + stg.getAttribute('data-work') : '—') : (n + ' ' + stg.getAttribute('data-usage') + (n >= 3 ? ' · ' + stg.getAttribute('data-promote') : '')); } Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (i) { i.addEventListener('input', esUpd); i.addEventListener('change', esUpd); }); esUpd(); }
    var tmRead = demo.querySelector('.tm-read');
    if (tmRead) { var tmNames = stg.getAttribute('data-names').split('|'), tmRisks = stg.getAttribute('data-risks').split('|'); function tmUpd() { var m = Number(demo.getAttribute('data-model')) || 0; demo.querySelector('.tm-name').textContent = tmNames[m]; demo.querySelector('.tm-risk').textContent = tmRisks[m]; demo.querySelector('.tm-health').textContent = demo.classList.contains('on-rituals') ? stg.getAttribute('data-ok') : stg.getAttribute('data-bad'); } Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (i) { i.addEventListener('input', tmUpd); i.addEventListener('change', tmUpd); }); tmUpd(); }
    var gvV = demo.querySelector('.gv-verdict');
    if (gvV) { function gvUpd() { var n = Number(demo.getAttribute('data-teams')) || 1, third = demo.classList.contains('on-third'), layer; if (n >= 2 || third) { gvV.textContent = stg.getAttribute('data-component'); layer = 1; } else { gvV.textContent = stg.getAttribute(n === 1 ? 'data-local' : 'data-pattern'); layer = 3; } if (n === 1 && !third) { gvV.textContent = stg.getAttribute('data-local'); layer = 3; } Array.prototype.forEach.call(demo.querySelectorAll('.gv-layer'), function (l, i) { l.classList.toggle('is-hit', i === layer); }); } Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (i) { i.addEventListener('input', gvUpd); i.addEventListener('change', gvUpd); }); gvUpd(); }
    var quList = demo.querySelector('.qu-list');
    if (quList) {
      var quReqs = stg.getAttribute('data-reqs').split('|'), quTiers = stg.getAttribute('data-tiers').split('|'), quI = 0, quRead = demo.querySelector('.qu-read');
      function quCount() { var w = quList.querySelectorAll('.qu-status:not(.ok):not(.no)').length; quRead.textContent = w ? w + ' ' + stg.getAttribute('data-unanswered') : ''; }
      demo.querySelector('.qu-btn').addEventListener('click', function () { var t = quReqs[quI % quReqs.length], tier = quTiers[quI % 3]; quI++; var it = document.createElement('div'); it.className = 'qu-item'; it.innerHTML = '<span>' + t + '</span><span class="qu-tier">' + tier + '</span><span class="qu-status">' + stg.getAttribute('data-waiting') + '</span>'; quList.prepend(it); while (quList.children.length > 4) quList.lastChild.remove(); quCount(); var st = it.querySelector('.qu-status'); var tick = function () { if (!it.isConnected) return; if (demo.classList.contains('on-triage')) { var ok = quI % 3 !== 0; st.textContent = stg.getAttribute(ok ? 'data-accepted' : 'data-declined'); st.className = 'qu-status ' + (ok ? 'ok' : 'no'); quCount(); } else setTimeout(tick, 800); }; setTimeout(tick, 1200); });
    }
    var mxGrid = demo.querySelector('.mx-grid');
    if (mxGrid) {
      var mxStates = stg.getAttribute('data-states').split('|');
      function mxUpd() { var cells = Array.prototype.slice.call(mxGrid.querySelectorAll('.mx-cell')), applicable = cells.filter(function (c) { return c.getAttribute('data-s') !== '3'; }), done = applicable.filter(function (c) { return c.getAttribute('data-s') === '2'; }).length, empty = applicable.filter(function (c) { return c.getAttribute('data-s') === '0'; }).length; demo.querySelector('.mx-read').textContent = Math.round(done / applicable.length * 100) + '% ' + stg.getAttribute('data-ready') + ' · ' + empty + ' ' + stg.getAttribute('data-empty'); var badge = demo.querySelector('.mx-badge'), gaps = Array.prototype.slice.call(mxGrid.querySelectorAll('.mx-row')).filter(function (r) { return Array.prototype.some.call(r.querySelectorAll('.mx-cell'), function (c) { return c.getAttribute('data-s') === '0' || c.getAttribute('data-s') === '1'; }); }).map(function (r) { return r.querySelector('.mx-dim').textContent.toLowerCase(); }); var partial = gaps.length > 0 && demo.classList.contains('on-label'); badge.textContent = partial ? stg.getAttribute('data-partial') + ' · ' + gaps.slice(0, 2).join(', ') : stg.getAttribute('data-published'); badge.classList.toggle('is-partial', partial); cells.forEach(function (c) { c.title = mxStates[Number(c.getAttribute('data-s'))]; }); }
      Array.prototype.forEach.call(mxGrid.querySelectorAll('.mx-cell'), function (c) { c.addEventListener('click', function () { c.setAttribute('data-s', (Number(c.getAttribute('data-s')) + 1) % 4); mxUpd(); }); });
      var mxSw = demo.querySelector('input[name="label"]'); if (mxSw) mxSw.addEventListener('change', mxUpd); mxUpd();
    }
    var mgGrid = demo.querySelector('.mg-grid');
    if (mgGrid) {
      var mgRead = demo.querySelector('.mg-read');
      function mgUpd() { var all = mgGrid.querySelectorAll('.mg-chip').length, n = mgGrid.querySelectorAll('.is-migrated').length; mgRead.textContent = n + '/' + all + ' ' + stg.getAttribute('data-migrated') + (demo.classList.contains('on-forced') && n < all ? ' · ' + stg.getAttribute('data-blocked') : '') + (demo.classList.contains('on-codemod') ? ' · ' + stg.getAttribute('data-auto') : ''); }
      Array.prototype.forEach.call(mgGrid.querySelectorAll('.mg-chip'), function (c) { c.addEventListener('click', function () { c.classList.toggle('is-migrated'); mgUpd(); }); });
      var mgSw = demo.querySelector('input[name="codemod"]'); if (mgSw) mgSw.addEventListener('change', function () { Array.prototype.forEach.call(mgGrid.querySelectorAll('.mg-mech'), function (c) { c.classList.toggle('is-migrated', mgSw.checked); }); mgUpd(); });
      var mgF = demo.querySelector('input[name="forced"]'); if (mgF) mgF.addEventListener('change', mgUpd); mgUpd();
    }
    var dcBtn = demo.querySelector('.dc-demo-btn');
    if (dcBtn) dcBtn.addEventListener('click', function () { var t = demo.querySelector('.dc-toast'); t.classList.add('is-shown'); clearTimeout(t._t); t._t = setTimeout(function () { t.classList.remove('is-shown'); }, 1500); });
    var pyRead = demo.querySelector('.py-read');
    if (pyRead) {
      function pyUpd() { var e = Number(demo.getAttribute('data-e2e')) || 0; pyRead.textContent = stg.getAttribute('data-min') + ': ' + Math.round(2 + e * 0.55) + ' min · ' + stg.getAttribute('data-flaky') + ': ' + Math.round(e * 0.35) + '%'; }
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input[type="range"]'), function (r) { r.addEventListener('input', pyUpd); }); pyUpd();
      var pyRes = demo.querySelector('.py-result');
      demo.querySelector('.py-refactor').addEventListener('click', function () { var role = demo.classList.contains('on-role'); pyRes.textContent = role ? '✓ ' + stg.getAttribute('data-pass') : '✕ ' + stg.getAttribute('data-fail'); pyRes.className = 'py-result ' + (role ? 'ok' : 'bad'); });
      var pySw = demo.querySelector('input[name="role"]'); if (pySw) pySw.addEventListener('change', function () { pyRes.textContent = ''; pyRes.className = 'py-result'; });
    }
    var snRun = demo.querySelector('.sn-run');
    if (snRun) {
      var snRead = demo.querySelector('.sn-read'), snCur = demo.querySelector('.sn-cur');
      demo.querySelector('.sn-base .sn-lbl').textContent = stg.getAttribute('data-base'); demo.querySelector('.sn-cur .sn-lbl').textContent = stg.getAttribute('data-cur');
      demo._replay = function () { if (snRun._ran) snRun.click(); };
      snRun.addEventListener('click', function () { snRun._ran = true; var dot = snCur.querySelector('.sn-dot'), time = snCur.querySelector('.sn-time'), diffs = 0; var anim = !demo.classList.contains('on-noanim'), tick = !demo.classList.contains('on-freeze'); dot.style.setProperty('--dx', anim ? '-14px' : '0'); dot.style.setProperty('--ds', anim ? '1.6' : '1'); dot.classList.toggle('is-diff', anim); if (anim) diffs++; time.textContent = tick ? stg.getAttribute('data-time2') : demo.querySelector('.sn-base .sn-time').textContent; time.classList.toggle('is-diff', tick); if (tick) diffs++; snRead.textContent = diffs ? diffs + ' ' + stg.getAttribute('data-diff') : '✓ ' + stg.getAttribute('data-clean'); snRead.className = 'sn-read ' + (diffs ? 'bad' : 'ok'); });
    }
    var itRun = demo.querySelector('.it-run');
    if (itRun) {
      var itDlg = demo.querySelector('.it-dialog'), itOpen = demo.querySelector('.it-open'), itClose = demo.querySelector('.it-close');
      function itShow() { itDlg.classList.add('is-open'); itClose.focus(); }
      function itHide() { itDlg.classList.remove('is-open'); if (demo.classList.contains('on-restore')) itOpen.focus(); else itClose.blur(); }
      itOpen.addEventListener('click', itShow); itClose.addEventListener('click', itHide); itDlg.addEventListener('keydown', function (e) { if (e.key === 'Escape') { e.stopPropagation(); itHide(); } });
      demo._replay = function () { if (itRun._ran) itRun.click(); };
      itRun.addEventListener('click', function () { itRun._ran = true; var res = {}; itShow(); res.focusin = itDlg.contains(document.activeElement) || itDlg.classList.contains('is-open'); itHide(); res.restore = document.activeElement === itOpen || demo.classList.contains('on-restore'); res.contrast = demo.classList.contains('on-contrast'); Array.prototype.forEach.call(demo.querySelectorAll('.it-results li'), function (li) { var ok = res[li.getAttribute('data-t')]; li.className = ok ? 'ok' : 'bad'; }); itRun.focus(); });
    }
    // Primitives demos ------------------------------------------------------
    var stageEl = demo.querySelector('.demo-stage');
    // 01 dimensions
    var dmChecks = demo.querySelector('.dm-checks');
    if (dmChecks) {
      function dmMark(k, v) { var li = dmChecks.querySelector('[data-check="' + k + '"]'); if (li) li.classList.toggle('is-ok', v); }
      function dmReset() { Array.prototype.forEach.call(dmChecks.children, function (li) { li.classList.remove('is-ok'); }); dmMark('role', demo.classList.contains('on-native')); }
      Array.prototype.forEach.call(demo.querySelectorAll('[data-el]'), function (el) {
        el.addEventListener('focus', function () { dmMark('reach', true); dmMark('ring', true); });
        el.addEventListener('keydown', function (e) { dmMark('reach', true); dmMark('ring', true); if (e.key === 'Enter' || e.key === ' ') { dmMark('activate', true); e.preventDefault(); } });
        el.addEventListener('click', function () { dmMark('activate', true); });
      });
      var dmSw = demo.querySelector('input[name="native"]'); if (dmSw) dmSw.addEventListener('change', dmReset); dmReset();
    }
    // 02 hit areas
    var htRow = demo.querySelector('.ht-row');
    if (htRow) {
      var hits = 0, miss = 0, htRead = demo.querySelector('.ht-read'), htLabel = stageEl.getAttribute('data-hits');
      function htUpdate() { htRead.textContent = hits + ' ' + htLabel + ' · ' + miss + ' miss'; }
      Array.prototype.forEach.call(htRow.querySelectorAll('.ht-btn'), function (b) { b.addEventListener('click', function (e) { e.stopPropagation(); hits++; b.classList.add('is-hit'); setTimeout(function () { b.classList.remove('is-hit'); }, 500); htUpdate(); }); });
      stageEl.addEventListener('click', function (e) { if (!e.target.closest('.ht-btn')) { miss++; htUpdate(); } });
      htUpdate();
    }
    // 03 press vs release
    var pmTrigger = demo.querySelector('.pm-trigger');
    if (pmTrigger) {
      var pmMenu = demo.querySelector('.pm-menu'), pmRead = demo.querySelector('.pm-read'), pmLabel = pmRead.textContent.replace(' —', ''), pmActive = null, pmPressOpened = false;
      function pmOpen() { pmMenu.classList.add('is-open'); } function pmClose() { pmMenu.classList.remove('is-open'); pmSet(null); }
      function pmSet(it) { if (pmActive) pmActive.classList.remove('is-active'); pmActive = it; if (it) it.classList.add('is-active'); }
      function pmSelect(it) { pmRead.textContent = pmLabel + ' ' + it.getAttribute('data-v'); pmClose(); }
      pmTrigger.addEventListener('pointerdown', function (e) { if (!demo.classList.contains('on-onpress')) return; e.preventDefault(); pmPressOpened = true; pmOpen(); try { pmTrigger.setPointerCapture(e.pointerId); } catch (x) {} });
      pmTrigger.addEventListener('pointermove', function (e) { if (!pmPressOpened) return; var hit = null; Array.prototype.forEach.call(pmMenu.querySelectorAll('.pm-item'), function (it) { var r = it.getBoundingClientRect(); if (e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom) hit = it; }); pmSet(hit); });
      pmTrigger.addEventListener('pointerup', function (e) { if (!pmPressOpened) return; pmPressOpened = false; try { pmTrigger.releasePointerCapture(e.pointerId); } catch (x) {} if (pmActive) pmSelect(pmActive); });
      pmTrigger.addEventListener('click', function (e) { if (demo.classList.contains('on-onpress') && e.detail !== 0) return; pmMenu.classList.contains('is-open') ? pmClose() : pmOpen(); });
      Array.prototype.forEach.call(pmMenu.querySelectorAll('.pm-item'), function (it) { it.addEventListener('pointerenter', function () { pmSet(it); }); it.addEventListener('click', function () { pmSelect(it); }); });
      document.addEventListener('pointerdown', function (e) { if (!demo.contains(e.target) && pmMenu.classList.contains('is-open')) pmClose(); });
    }
    // 04 focus
    var fcList = demo.querySelector('.fc-list');
    if (fcList) {
      var fcRead = demo.querySelector('.fc-read'), fcTabs = 0, fcL = { focus: stageEl.getAttribute('data-focus'), body: stageEl.getAttribute('data-body'), tabs: stageEl.getAttribute('data-tabs') };
      function fcItems() { return Array.prototype.slice.call(fcList.querySelectorAll('.fc-item')); }
      function fcApply() { var rov = demo.classList.contains('on-roving'); fcItems().forEach(function (it, i) { it.tabIndex = rov ? (i === 0 ? 0 : -1) : 0; }); }
      function fcReport() { var a = document.activeElement, t; if (a && a.classList && a.classList.contains('fc-item')) t = fcL.focus + ': ' + a.firstChild.textContent.trim(); else if (a === demo.querySelector('.fc-after')) t = fcL.focus + ': ' + a.textContent; else if (a === demo.querySelector('.fc-before')) t = fcL.focus + ': ' + a.textContent; else t = fcL.focus + ': ' + fcL.body; fcRead.textContent = t + ' · ' + fcL.tabs + ': ' + fcTabs; }
      demo.querySelector('.fc-before').addEventListener('focus', function () { fcTabs = 0; fcReport(); });
      demo.querySelector('.fc-after').addEventListener('focus', fcReport);
      fcList.addEventListener('keydown', function (e) {
        var items = fcItems(), i = items.indexOf(document.activeElement); if (i < 0) return;
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); var n = items[Math.max(0, Math.min(items.length - 1, i + (e.key === 'ArrowDown' ? 1 : -1)))]; if (demo.classList.contains('on-roving')) { items.forEach(function (x) { x.tabIndex = -1; }); n.tabIndex = 0; } n.focus(); }
        if (e.key === 'Backspace' || e.key === 'Delete') { e.preventDefault(); var cur = items[i]; var next = items[i + 1] || items[i - 1]; cur.remove(); if (demo.classList.contains('on-restore') && next) { next.tabIndex = 0; next.focus(); } else { cur.blur(); document.activeElement && document.activeElement.blur && document.activeElement.blur(); } fcApply(); setTimeout(fcReport, 0); }
      });
      fcList.addEventListener('keydown', function (e) { if (e.key === 'Tab') fcTabs++; }, true);
      demo.addEventListener('focusin', fcReport); demo.addEventListener('focusout', function () { setTimeout(fcReport, 0); });
      var fcSw = demo.querySelector('input[name="roving"]'); if (fcSw) fcSw.addEventListener('change', fcApply); fcApply(); fcReport();
    }
    // 05 escape stack
    var stWrap = demo.querySelector('.st-wrap');
    if (stWrap) {
      var stDialog = demo.querySelector('.st-dialog'), stMenu = demo.querySelector('.st-menu'), stRead = demo.querySelector('.st-read'), stL = { layers: stageEl.getAttribute('data-layers'), dialog: stageEl.getAttribute('data-dialog'), menu: stageEl.getAttribute('data-menu') };
      function stReport() { var l = []; if (stDialog.classList.contains('is-open')) l.push(stL.dialog); if (stMenu.classList.contains('is-open')) l.push(stL.menu); stRead.textContent = stL.layers + ': ' + (l.length ? l.join(' › ') : '—'); }
      demo.querySelector('.st-open').addEventListener('click', function () { stDialog.classList.add('is-open'); demo.querySelector('.st-menubtn').focus(); stReport(); });
      demo.querySelector('.st-menubtn').addEventListener('click', function () { stMenu.classList.toggle('is-open'); stReport(); });
      Array.prototype.forEach.call(stMenu.querySelectorAll('.st-mi'), function (mi) { mi.addEventListener('click', function () { stMenu.classList.remove('is-open'); stReport(); }); });
      stWrap.addEventListener('keydown', function (e) {
        if (e.key !== 'Escape') return; e.preventDefault(); e.stopPropagation();
        if (demo.classList.contains('on-stackesc')) { if (stMenu.classList.contains('is-open')) stMenu.classList.remove('is-open'); else if (stDialog.classList.contains('is-open')) { stDialog.classList.remove('is-open'); demo.querySelector('.st-open').focus(); } }
        else { stMenu.classList.remove('is-open'); stDialog.classList.remove('is-open'); demo.querySelector('.st-open').focus(); }
        stReport();
      });
    }
    // 07 state
    var seBtn = demo.querySelector('.st2-btn');
    if (seBtn) { seBtn.addEventListener('click', function () { demo.classList.add('is-explain'); clearTimeout(seBtn._t); seBtn._t = setTimeout(function () { demo.classList.remove('is-explain'); }, 1800); }); var seField = demo.querySelector('.st2-field'); function seApply() { seField.disabled = demo.classList.contains('on-asdisabled'); seField.readOnly = !seField.disabled; } var seSw = demo.querySelector('input[name="asdisabled"]'); if (seSw) seSw.addEventListener('change', seApply); seApply(); }
    // 08 aria
    var arToggle = demo.querySelector('.ar-toggle');
    if (arToggle) {
      var arDisc = demo.querySelector('.ar-disc'), arPanel = demo.querySelector('.ar-panel'), arRead = demo.querySelector('.ar-read');
      var arL = { role: stageEl.getAttribute('data-role'), pressed: stageEl.getAttribute('data-pressed'), expanded: stageEl.getAttribute('data-expanded'), collapsed: stageEl.getAttribute('data-collapsed'), none: stageEl.getAttribute('data-none') };
      function arSay(el, state) { var decl = demo.classList.contains('on-declare'), name = Array.prototype.filter.call(el.childNodes, function (n) { return n.nodeType === 3; }).map(function (n) { return n.textContent; }).join('').trim() || el.textContent.trim(); arRead.textContent = name + ', ' + arL.role + (decl ? ', ' + state : ''); }
      function arSync() { var decl = demo.classList.contains('on-declare'); if (decl) { arToggle.setAttribute('aria-pressed', arToggle.classList.contains('is-on') ? 'true' : 'false'); arDisc.setAttribute('aria-expanded', arPanel.classList.contains('is-open') ? 'true' : 'false'); } else { arToggle.removeAttribute('aria-pressed'); arDisc.removeAttribute('aria-expanded'); } }
      arToggle.addEventListener('click', function () { arToggle.classList.toggle('is-on'); arSync(); arSay(arToggle, arToggle.classList.contains('is-on') ? arL.pressed : arL.none); });
      arDisc.addEventListener('click', function () { arPanel.classList.toggle('is-open'); arSync(); arSay(arDisc, arPanel.classList.contains('is-open') ? arL.expanded : arL.collapsed); });
      var arSw = demo.querySelector('input[name="declare"]'); if (arSw) arSw.addEventListener('change', arSync); arSync();
    }
    // 09 button
    var btBtn = demo.querySelector('.bt-btn');
    if (btBtn) { var btLabel = btBtn.querySelector('.bt-label'); btBtn.addEventListener('click', function () { if (btBtn.classList.contains('is-loading')) return; btBtn.classList.add('is-loading'); btLabel.textContent = stageEl.getAttribute('data-saving'); setTimeout(function () { btLabel.textContent = stageEl.getAttribute('data-saved'); setTimeout(function () { btLabel.textContent = stageEl.getAttribute('data-save'); btBtn.classList.remove('is-loading'); }, 900); }, 1100); }); }
    // 10 field
    var fdInput = demo.querySelector('.fd-input');
    if (fdInput) {
      var fdWrap = demo.querySelector('.fd-wrap'), fdTouched = false;
      function fdValid() { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(fdInput.value); }
      function fdCheck(force) { fdWrap.classList.toggle('has-value', !!fdInput.value); var bad = fdInput.value && !fdValid(); if (force || !demo.classList.contains('on-onblur') || fdTouched) { fdWrap.classList.toggle('is-invalid', !!bad); fdInput.setAttribute('aria-invalid', bad ? 'true' : 'false'); } }
      fdInput.addEventListener('input', function () { fdCheck(false); });
      fdInput.addEventListener('blur', function () { if (fdInput.value) fdTouched = true; fdCheck(true); });
    }
    // 11 checkbox tri-state
    var ckParent = demo.querySelector('.ck2-parent');
    if (ckParent) {
      var ckKids = Array.prototype.slice.call(demo.querySelectorAll('.ck2-child'));
      function ckSync() { var n = ckKids.filter(function (k) { return k.checked; }).length; ckParent.checked = n === ckKids.length; ckParent.indeterminate = demo.classList.contains('on-mixed') && n > 0 && n < ckKids.length; }
      ckKids.forEach(function (k) { k.addEventListener('change', ckSync); });
      ckParent.addEventListener('change', function () { var v = ckParent.checked; ckKids.forEach(function (k) { k.checked = v; }); ckParent.indeterminate = false; });
      var ckSw = demo.querySelector('input[name="mixed"]'); if (ckSw) ckSw.addEventListener('change', ckSync); ckSync();
    }
    // 12 select
    var sxTrigger = demo.querySelector('.sx-trigger');
    if (sxTrigger) {
      var sxList = demo.querySelector('.sx-list'), sxRead = demo.querySelector('.sx-read'), sxOpts = Array.prototype.slice.call(sxList.querySelectorAll('.sx-opt')), sxActive = -1, sxBuf = '', sxBufT = null;
      function sxSetActive(i, scroll) { sxOpts.forEach(function (o) { o.classList.remove('is-active'); }); sxActive = i; if (i >= 0) { sxOpts[i].classList.add('is-active'); if (scroll) sxOpts[i].scrollIntoView({ block: 'nearest' }); } }
      function sxOpen() { sxList.classList.add('is-open'); var sel = sxOpts.findIndex(function (o) { return o.getAttribute('aria-selected') === 'true'; }); if (demo.classList.contains('on-openat') && sel >= 0) { sxSetActive(sel, false); sxOpts[sel].scrollIntoView({ block: 'center' }); } else { sxList.scrollTop = 0; sxSetActive(0, false); } sxList.focus(); }
      function sxClose() { sxList.classList.remove('is-open'); sxTrigger.focus(); }
      function sxSelect(i) { sxOpts.forEach(function (o) { o.removeAttribute('aria-selected'); }); sxOpts[i].setAttribute('aria-selected', 'true'); demo.querySelector('.sx-value').textContent = sxOpts[i].getAttribute('data-v'); sxClose(); }
      sxTrigger.addEventListener('click', function () { sxList.classList.contains('is-open') ? sxClose() : sxOpen(); });
      sxOpts.forEach(function (o, i) { o.addEventListener('pointerenter', function () { sxSetActive(i, false); }); o.addEventListener('click', function () { sxSelect(i); }); });
      sxList.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); sxSetActive(Math.max(0, Math.min(sxOpts.length - 1, sxActive + (e.key === 'ArrowDown' ? 1 : -1))), true); }
        else if (e.key === 'Home') { e.preventDefault(); sxSetActive(0, true); } else if (e.key === 'End') { e.preventDefault(); sxSetActive(sxOpts.length - 1, true); }
        else if (e.key === 'Enter') { e.preventDefault(); if (sxActive >= 0) sxSelect(sxActive); } else if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); sxClose(); } else if (e.key === 'Tab') { sxList.classList.remove('is-open'); }
        else if (e.key.length === 1 && /\S/.test(e.key)) {
          e.preventDefault(); var buffer = demo.classList.contains('on-typeahead'); sxBuf = (buffer ? sxBuf : '') + e.key.toLowerCase(); clearTimeout(sxBufT); sxBufT = setTimeout(function () { sxBuf = ''; }, 700);
          var norm = function (t) { return t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); };
          var start = buffer ? 0 : (sxActive + 1) % sxOpts.length, hit = -1;
          for (var k = 0; k < sxOpts.length; k++) { var idx = (start + k) % sxOpts.length; if (norm(sxOpts[idx].getAttribute('data-v')).indexOf(sxBuf) === 0) { hit = idx; break; } }
          if (hit >= 0) sxSetActive(hit, true);
          sxRead.textContent = stageEl.getAttribute('data-typed') + ': “' + sxBuf + '”';
        }
      });
      document.addEventListener('pointerdown', function (e) { if (!demo.contains(e.target) && sxList.classList.contains('is-open')) sxList.classList.remove('is-open'); });
    }
    // 13 slider
    var sdTrack = demo.querySelector('.sd-track');
    if (sdTrack) {
      var sdVal = 40, sdThumb = demo.querySelector('.sd-thumb'), sdBubble = demo.querySelector('.sd-bubble'), sdDrag = false;
      function sdSet(v) { sdVal = Math.max(0, Math.min(100, Math.round(v))); sdTrack.style.setProperty('--v', sdVal + '%'); sdTrack.setAttribute('aria-valuenow', sdVal); sdBubble.textContent = sdVal; }
      function sdFromX(x) { var r = sdTrack.getBoundingClientRect(); return (x - r.left) / r.width * 100; }
      sdThumb.addEventListener('pointerdown', function (e) { e.preventDefault(); e.stopPropagation(); sdDrag = true; sdTrack.classList.add('is-dragging'); if (demo.classList.contains('on-capture')) { try { sdThumb.setPointerCapture(e.pointerId); } catch (x) {} } });
      sdThumb.addEventListener('pointermove', function (e) { if (sdDrag) sdSet(sdFromX(e.clientX)); });
      sdThumb.addEventListener('pointerleave', function () { if (sdDrag && !demo.classList.contains('on-capture')) { sdDrag = false; sdTrack.classList.remove('is-dragging'); } });
      sdThumb.addEventListener('pointerup', function () { sdDrag = false; sdTrack.classList.remove('is-dragging'); });
      sdThumb.addEventListener('pointercancel', function () { sdDrag = false; sdTrack.classList.remove('is-dragging'); });
      sdTrack.addEventListener('pointerdown', function (e) { if (demo.classList.contains('on-jump')) sdSet(sdFromX(e.clientX)); });
      sdTrack.addEventListener('keydown', function (e) { var big = e.shiftKey ? 10 : 1; var m = { ArrowRight: big, ArrowUp: big, ArrowLeft: -big, ArrowDown: -big, PageUp: 10, PageDown: -10 }; if (m[e.key] !== undefined) { e.preventDefault(); sdSet(sdVal + m[e.key]); } else if (e.key === 'Home') { e.preventDefault(); sdSet(0); } else if (e.key === 'End') { e.preventDefault(); sdSet(100); } });
      sdSet(40);
    }
    // 14 tooltip
    var tpBar = demo.querySelector('.tp-bar');
    if (tpBar) {
      var tpTip = demo.querySelector('.tp-tip'), tpTimer = null, tpWarm = null, tpShown = false;
      function tpShow(b) { var r = b.getBoundingClientRect(), w = demo.querySelector('.tp-wrap').getBoundingClientRect(); tpTip.textContent = b.getAttribute('data-tip'); tpTip.style.setProperty('--x', (r.left - w.left + r.width / 2) + 'px'); tpTip.classList.add('is-shown'); tpShown = true; }
      function tpHide() { clearTimeout(tpTimer); tpTip.classList.remove('is-shown'); if (tpShown) { tpShown = false; clearTimeout(tpWarm); tpWarm = setTimeout(function () { tpWarm = null; }, 300); } }
      function tpIntent(b, viaFocus) { clearTimeout(tpTimer); var immediate = viaFocus || (demo.classList.contains('on-group') && tpWarm !== null) ; if (tpShown || immediate) tpShow(b); else tpTimer = setTimeout(function () { tpShow(b); }, 500); }
      Array.prototype.forEach.call(tpBar.querySelectorAll('.tp-btn'), function (b) {
        b.addEventListener('pointerenter', function () { tpIntent(b, false); });
        b.addEventListener('pointerleave', tpHide);
        b.addEventListener('focus', function () { if (demo.classList.contains('on-focus') && b.matches(':focus-visible')) tpIntent(b, true); });
        b.addEventListener('blur', tpHide);
        b.addEventListener('click', tpHide);
        b.addEventListener('keydown', function (e) { if (e.key === 'Escape') tpHide(); });
      });
    }
    // 15 menu with submenu
    var mnTrigger = demo.querySelector('.mn-trigger');
    if (mnTrigger) {
      var mnMenu = demo.querySelector('.mn-menu'), mnParent = demo.querySelector('.mn-parent'), mnCloseT = null;
      mnTrigger.addEventListener('pointerdown', function (e) { e.preventDefault(); mnMenu.classList.toggle('is-open'); mnParent.classList.remove('is-sub-open'); });
      mnTrigger.addEventListener('click', function (e) { if (e.detail === 0) { mnMenu.classList.toggle('is-open'); mnParent.classList.remove('is-sub-open'); } });
      mnParent.addEventListener('pointerenter', function () { clearTimeout(mnCloseT); mnParent.classList.add('is-sub-open'); mnParent.classList.add('is-active'); });
      Array.prototype.forEach.call(mnMenu.querySelectorAll(':scope > .mn-item'), function (it) {
        it.addEventListener('pointerenter', function (e) {
          if (it === mnParent) return;
          Array.prototype.forEach.call(mnMenu.querySelectorAll(':scope > .mn-item'), function (x) { x.classList.remove('is-active'); }); it.classList.add('is-active');
          if (mnParent.classList.contains('is-sub-open')) {
            var pr = mnParent.getBoundingClientRect(), towardSub = e.clientX > pr.left + pr.width * 0.5;
            if (demo.classList.contains('on-safe') && towardSub) { clearTimeout(mnCloseT); mnCloseT = setTimeout(function () { mnParent.classList.remove('is-sub-open'); }, 300); }
            else mnParent.classList.remove('is-sub-open');
          }
        });
        it.addEventListener('pointerleave', function () { it.classList.remove('is-active'); });
        it.addEventListener('click', function (e) { if (it === mnParent) return; mnMenu.classList.remove('is-open'); });
      });
      Array.prototype.forEach.call(mnParent.querySelectorAll('.mn-sub .mn-item'), function (si) { si.addEventListener('pointerenter', function () { clearTimeout(mnCloseT); Array.prototype.forEach.call(mnParent.querySelectorAll('.mn-sub .mn-item'), function (x) { x.classList.remove('is-active'); }); si.classList.add('is-active'); }); si.addEventListener('click', function (e) { e.stopPropagation(); mnMenu.classList.remove('is-open'); mnParent.classList.remove('is-sub-open'); }); });
      mnMenu.addEventListener('pointerleave', function () { clearTimeout(mnCloseT); mnParent.classList.remove('is-sub-open'); });
      document.addEventListener('pointerdown', function (e) { if (!demo.contains(e.target)) mnMenu.classList.remove('is-open'); });
      demo.addEventListener('keydown', function (e) { if (e.key === 'Escape') { mnMenu.classList.remove('is-open'); mnTrigger.focus(); } });
    }
    // 16 command menu
    var cmPanel = demo.querySelector('.cmd-panel');
    if (cmPanel) {
      var cmInput = demo.querySelector('.cmd-input'), cmList = demo.querySelector('.cmd-list'), cmTrigger = demo.querySelector('.cmd-trigger'), cmCmds = stageEl.getAttribute('data-cmds').split('|'), cmRecent = [cmCmds[3], cmCmds[0]], cmActive = 0, cmItems = [];
      function cmFuzzy(q, t) { var ql = q.toLowerCase(), tl = t.toLowerCase(), j = 0, out = ''; for (var i = 0; i < t.length && j < ql.length; i++) { if (tl[i] === ql[j]) { out += '<b>' + t[i] + '</b>'; j++; } else out += t[i]; } if (j < ql.length) return null; return out + t.slice(t.length); }
      function cmRender() {
        var q = cmInput.value.trim(), fuzzy = demo.classList.contains('on-fuzzy'), rows = [];
        if (!q) rows = cmRecent.map(function (c) { return { t: c, h: c }; });
        else cmCmds.forEach(function (c) { if (fuzzy) { var h = cmFuzzy(q, c); if (h !== null) rows.push({ t: c, h: h }); } else { var i = c.toLowerCase().indexOf(q.toLowerCase()); if (i >= 0) rows.push({ t: c, h: c.slice(0, i) + '<b>' + c.slice(i, i + q.length) + '</b>' + c.slice(i + q.length) }); } });
        cmList.innerHTML = (!q ? '<div class="cmd-group">' + stageEl.getAttribute('data-recent') + '</div>' : '') + (rows.length ? rows.map(function (r, i) { return '<div class="cmd-item' + (i === 0 ? ' is-active' : '') + '" role="option" data-t="' + r.t + '"><span>' + r.h + '</span></div>'; }).join('') : '<div class="cmd-empty">' + stageEl.getAttribute('data-empty') + '</div>');
        cmItems = Array.prototype.slice.call(cmList.querySelectorAll('.cmd-item')); cmActive = 0;
        cmItems.forEach(function (it, i) { it.addEventListener('pointerenter', function () { cmSetActive(i); }); it.addEventListener('click', function () { cmRun(it); }); });
      }
      function cmSetActive(i) { cmItems.forEach(function (x) { x.classList.remove('is-active'); }); cmActive = Math.max(0, Math.min(cmItems.length - 1, i)); if (cmItems[cmActive]) { cmItems[cmActive].classList.add('is-active'); cmItems[cmActive].scrollIntoView({ block: 'nearest' }); } }
      function cmRun(it) { var t = it.getAttribute('data-t'); cmRecent = [t].concat(cmRecent.filter(function (x) { return x !== t; })).slice(0, 3); cmClose(); cmTrigger.querySelector('span') && (cmTrigger.firstChild.textContent = t + ' ✓ '); setTimeout(function () { cmTrigger.firstChild.textContent = cmTrigger.getAttribute('data-orig'); }, 1400); }
      function cmOpen() { cmPanel.classList.add('is-open'); cmInput.value = ''; cmRender(); cmInput.focus(); }
      function cmClose() { cmPanel.classList.remove('is-open'); cmTrigger.focus(); }
      cmTrigger.setAttribute('data-orig', cmTrigger.firstChild.textContent);
      cmTrigger.addEventListener('click', cmOpen);
      demo._replay = function () { if (cmPanel.classList.contains('is-open')) { cmPanel.classList.remove('is-open'); void cmPanel.offsetWidth; cmPanel.classList.add('is-open'); cmRender(); cmInput.focus(); } };
      cmInput.addEventListener('input', cmRender);
      cmInput.addEventListener('keydown', function (e) { if (e.key === 'ArrowDown') { e.preventDefault(); cmSetActive(cmActive + 1); } else if (e.key === 'ArrowUp') { e.preventDefault(); cmSetActive(cmActive - 1); } else if (e.key === 'Enter') { e.preventDefault(); if (cmItems[cmActive]) cmRun(cmItems[cmActive]); } else if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); cmClose(); } });
      demo.addEventListener('keydown', function (e) { if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); cmPanel.classList.contains('is-open') ? cmClose() : cmOpen(); } });
      document.addEventListener('pointerdown', function (e) { if (!demo.contains(e.target) && cmPanel.classList.contains('is-open')) cmPanel.classList.remove('is-open'); });
    }
    // 17 dialog
    var dgDialog = demo.querySelector('.dg-dialog');
    if (dgDialog) {
      var dgWrap = demo.querySelector('.dg-wrap'), dgRead = demo.querySelector('.dg-read'), dgField = demo.querySelector('.dg-field'), dgOpenBtn = demo.querySelector('.dg-open');
      function dgOpen() { dgDialog.show(); dgWrap.classList.add('is-open'); var f = demo.classList.contains('on-safefocus') ? demo.querySelector('.dg-cancel') : demo.querySelector('.dg-delete'); f.focus(); dgRead.textContent = stageEl.getAttribute('data-focused') + ': ' + f.textContent; }
      function dgClose(msg) { dgDialog.close(); dgWrap.classList.remove('is-open'); dgOpenBtn.focus(); dgRead.textContent = msg; dgField.value = ''; }
      dgOpenBtn.addEventListener('click', dgOpen);
      demo._replay = function () { if (dgDialog.open) dgOpen(); };
      demo.querySelector('.dg-cancel').addEventListener('click', function () { dgClose(stageEl.getAttribute('data-closed')); });
      demo.querySelector('.dg-delete').addEventListener('click', function () { dgClose(stageEl.getAttribute('data-closed')); });
      dgDialog.addEventListener('keydown', function (e) { if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); dgClose(stageEl.getAttribute('data-closed')); } if (e.key === 'Tab') { var f = dgDialog.querySelectorAll('input, button'); var first = f[0], last = f[f.length - 1]; if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); } else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); } } });
      dgDialog.addEventListener('cancel', function (e) { e.preventDefault(); });
      dgWrap.addEventListener('pointerdown', function (e) { if (!dgDialog.open || dgDialog.contains(e.target) || e.target === dgOpenBtn) return; if (demo.classList.contains('on-outside')) { var n = dgField.value.length; dgClose(stageEl.getAttribute('data-lost') + ' ' + n + ' chars'); } });
    }
    // 18 drawer with gesture transfer
    var dwSheet = demo.querySelector('.dw2-sheet');
    if (dwSheet) {
      var dwWrap = demo.querySelector('.dw2-wrap'), dwList = demo.querySelector('.dw2-list'), dwRead = demo.querySelector('.dw2-read'), dwY = 1, dwStartY = 0, dwStartVal = 0, dwMode = null, dwLastY = 0, dwLastT = 0, dwVel = 0;
      function dwSetY(v) { dwY = Math.max(0, Math.min(1, v)); dwWrap.style.setProperty('--y', dwY); }
      demo.querySelector('.dw2-open').addEventListener('click', function () { dwSetY(0); });
      dwSheet.addEventListener('pointerdown', function (e) {
        var onList = dwList.contains(e.target), transfer = demo.classList.contains('on-transfer');
        dwStartY = e.clientY; dwStartVal = dwY; dwLastY = e.clientY; dwLastT = e.timeStamp; dwVel = 0;
        dwMode = (onList && transfer && dwY === 0) ? 'undecided' : 'sheet';
        try { dwSheet.setPointerCapture(e.pointerId); } catch (x) {} dwSheet.classList.add('is-dragging'); e.preventDefault();
      });
      dwSheet.addEventListener('pointermove', function (e) {
        if (!dwMode) return; var dy = e.clientY - dwStartY, h = dwSheet.offsetHeight;
        dwVel = (e.clientY - dwLastY) / Math.max(1, e.timeStamp - dwLastT); dwLastY = e.clientY; dwLastT = e.timeStamp;
        if (dwMode === 'undecided') { if (Math.abs(dy) < 6) return; dwMode = (dy > 0 && dwList.scrollTop <= 0) ? 'sheet' : 'scroll'; dwStartY = e.clientY; dy = 0; }
        if (dwMode === 'scroll') { dwList.scrollTop -= (e.clientY - (dwLastY)) ; dwList.scrollTop = dwList.scrollTop - 0; dwList.scrollBy(0, -(e.movementY || 0)); dwRead.textContent = stageEl.getAttribute('data-content'); if (dwList.scrollTop <= 0 && dy > 0) { dwMode = 'sheet'; dwStartY = e.clientY; } return; }
        dwSetY(dwStartVal + dy / h); dwRead.textContent = stageEl.getAttribute('data-sheet');
      });
      function dwEnd() { if (!dwMode) return; dwSheet.classList.remove('is-dragging'); if (dwMode === 'sheet') { var projected = dwY + dwVel * 0.2; dwSetY(projected > 0.25 || dwVel > 0.5 ? 1 : 0); } dwMode = null; setTimeout(function () { dwRead.textContent = ''; }, 900); }
      dwSheet.addEventListener('pointerup', dwEnd); dwSheet.addEventListener('pointercancel', dwEnd);
      demo.querySelector('.dw2-overlay').addEventListener('click', function () { dwSetY(1); });
      dwWrap.style.setProperty('--y', 1);
    }
    // 19 toast
    var tsStack = demo.querySelector('.ts-stack');
    if (tsStack) {
      var tsBtnEl = demo.querySelector('.ts-btn');
      function tsLayout() { var list = Array.prototype.slice.call(tsStack.querySelectorAll('.ts-toast:not(.is-leaving)')).reverse(); list.forEach(function (t, i) { t.style.setProperty('--i', i); t.style.opacity = i > 2 ? 0 : 1; }); }
      function tsRemove(t) { t.classList.add('is-leaving'); setTimeout(function () { t.remove(); tsLayout(); }, 220); }
      tsBtnEl.addEventListener('click', function () {
        var t = document.createElement('div'); t.className = 'ts-toast'; t.innerHTML = '<span>' + stageEl.getAttribute('data-msg') + '</span><button type="button">' + stageEl.getAttribute('data-undo') + '</button><span class="ts-bar"></span>';
        tsStack.appendChild(t); tsLayout();
        var total = 4000, left = total, last = performance.now(), paused = false, bar = t.querySelector('.ts-bar');
        function tick(now) { if (!t.isConnected) return; if (!paused) { left -= now - last; bar.style.setProperty('--p', Math.max(0, left / total * 100) + '%'); } last = now; if (left <= 0) { tsRemove(t); return; } requestAnimationFrame(tick); }
        requestAnimationFrame(tick);
        t.addEventListener('pointerenter', function () { if (demo.classList.contains('on-pause')) paused = true; }); t.addEventListener('pointerleave', function () { paused = false; });
        t.querySelector('button').addEventListener('click', function () { tsRemove(t); });
      });
    }
    // 20 tabs
    var tbList = demo.querySelector('.tb-list');
    if (tbList) {
      var tbTabs = Array.prototype.slice.call(tbList.querySelectorAll('.tb-tab')), tbInd = demo.querySelector('.tb-ind'), tbName = demo.querySelector('.tb-panel-name'), tbLoads = demo.querySelector('.tb-loads b'), tbCount = 0;
      function tbActivate(i, focus) { tbTabs.forEach(function (t, k) { t.setAttribute('aria-selected', k === i ? 'true' : 'false'); t.tabIndex = k === i ? 0 : -1; }); var r = tbTabs[i].getBoundingClientRect(), lr = tbList.getBoundingClientRect(); tbInd.style.setProperty('--x', (r.left - lr.left) + 'px'); tbInd.style.setProperty('--w', r.width + 'px'); tbName.textContent = tbTabs[i].textContent; tbCount++; tbLoads.textContent = tbCount; if (focus) tbTabs[i].focus(); }
      tbTabs.forEach(function (t, i) { t.addEventListener('click', function () { tbActivate(i, true); }); });
      tbList.addEventListener('keydown', function (e) {
        var cur = tbTabs.indexOf(document.activeElement); if (cur < 0) return;
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft' || e.key === 'Home' || e.key === 'End') {
          e.preventDefault(); var n = e.key === 'Home' ? 0 : e.key === 'End' ? tbTabs.length - 1 : (cur + (e.key === 'ArrowRight' ? 1 : -1) + tbTabs.length) % tbTabs.length;
          if (demo.classList.contains('on-manual')) { tbTabs.forEach(function (t) { t.tabIndex = -1; }); tbTabs[n].tabIndex = 0; tbTabs[n].focus(); } else tbActivate(n, true);
        } else if ((e.key === 'Enter' || e.key === ' ') && demo.classList.contains('on-manual')) { e.preventDefault(); tbActivate(cur, true); }
      });
      tbActivate(0, false); tbCount = 0; tbLoads.textContent = 0;
    }
    // 21 accordion
    var acList = demo.querySelector('.ac-list');
    if (acList) {
      var acItems = Array.prototype.slice.call(acList.querySelectorAll('.ac-item'));
      function acSet(item, open) { var head = item.querySelector('.ac-head'), body = item.querySelector('.ac-body'); head.setAttribute('aria-expanded', open ? 'true' : 'false'); if (!demo.classList.contains('on-measure')) { body.style.transition = 'none'; body.style.height = open ? 'auto' : '0px'; return; } body.style.transition = ''; var target = open ? body.querySelector('.ac-inner').offsetHeight : 0; body.style.height = body.offsetHeight + 'px'; requestAnimationFrame(function () { body.style.height = target + 'px'; }); }
      acItems.forEach(function (item) { var head = item.querySelector('.ac-head'); head.addEventListener('click', function () {
        var isOpen = head.getAttribute('aria-expanded') === 'true'; var others = acItems.filter(function (o) { return o !== item && o.querySelector('.ac-head').getAttribute('aria-expanded') === 'true'; });
        if (isOpen) { acSet(item, false); return; }
        if (demo.classList.contains('on-together')) { others.forEach(function (o) { acSet(o, false); }); acSet(item, true); }
        else { others.forEach(function (o) { acSet(o, false); }); setTimeout(function () { acSet(item, true); }, others.length ? 280 : 0); }
      }); });
      acItems.forEach(function (item, i) { var body = item.querySelector('.ac-body'); body.style.height = i === 0 ? body.querySelector('.ac-inner').offsetHeight + 'px' : '0px'; });
    }
    // 22 table
    var tb3 = demo.querySelector('.tb3-scroll');
    if (tb3) tb3.addEventListener('scroll', function () { tb3.classList.toggle('is-scrolled', tb3.scrollTop > 2); }, { passive: true });
    // 23 scroll area
    var saStrip = demo.querySelector('.sa-strip');
    if (saStrip) { var saWrap = demo.querySelector('.sa-wrap'); function saUpdate() { var max = saStrip.scrollWidth - saStrip.clientWidth; saWrap.style.setProperty('--fl', saStrip.scrollLeft > 4 ? 1 : 0); saWrap.style.setProperty('--fr', saStrip.scrollLeft < max - 4 ? 1 : 0); } saStrip.addEventListener('scroll', saUpdate, { passive: true }); saUpdate(); }
    // 24 reorder
    var roList = demo.querySelector('.ro-list');
    if (roList) {
      var roLine = demo.querySelector('.ro-line'), roLive = demo.querySelector('.ro-live'), roDrag = null, roStartY = 0, roStarted = false, roTarget = -1, roGrabbed = null, roOrigIndex = -1;
      function roItems() { return Array.prototype.slice.call(roList.querySelectorAll('.ro-item')); }
      function roAnnounce(item) { var items = roItems(); roLive.textContent = item.lastChild.textContent + ' ' + stageEl.getAttribute('data-moved') + ' ' + (items.indexOf(item) + 1) + ' ' + stageEl.getAttribute('data-of') + ' ' + items.length; }
      function roIndexAt(y) { var items = roItems().filter(function (i) { return i !== roDrag; }); for (var k = 0; k < items.length; k++) { var r = items[k].getBoundingClientRect(); if (y < r.top + r.height / 2) return k; } return items.length; }
      function roShowTarget(idx) { var items = roItems().filter(function (i) { return i !== roDrag; }); items.forEach(function (i) { i.classList.remove('is-gap'); }); var lr = roList.getBoundingClientRect(), y; if (idx < items.length) { y = items[idx].getBoundingClientRect().top - lr.top - 2; items[idx].classList.add('is-gap'); } else { var last = items[items.length - 1]; y = last.getBoundingClientRect().bottom - lr.top; } roLine.style.setProperty('--y', y + 'px'); roTarget = idx; }
      roList.addEventListener('pointerdown', function (e) { var h = e.target.closest('.ro-handle'); if (!h) return; roDrag = h.closest('.ro-item'); roStartY = e.clientY; roStarted = false; try { roList.setPointerCapture(e.pointerId); } catch (x) {} e.preventDefault(); });
      roList.addEventListener('pointermove', function (e) { if (!roDrag) return; var dy = e.clientY - roStartY; if (!roStarted) { if (Math.abs(dy) < 10) return; roStarted = true; roDrag.classList.add('is-dragging'); roList.classList.add('is-dragging'); } roDrag.style.transform = 'translateY(' + dy + 'px) scale(1.02)'; roShowTarget(roIndexAt(e.clientY)); });
      function roEnd(cancel) { if (!roDrag) return; var items = roItems().filter(function (i) { return i !== roDrag; }); roDrag.style.transform = ''; roDrag.classList.remove('is-dragging'); roList.classList.remove('is-dragging'); items.forEach(function (i) { i.classList.remove('is-gap'); }); if (roStarted && !cancel && roTarget >= 0) { if (roTarget < items.length) roList.insertBefore(roDrag, items[roTarget]); else roList.insertBefore(roDrag, roLine); roAnnounce(roDrag); } roDrag = null; roStarted = false; roTarget = -1; }
      roList.addEventListener('pointerup', function () { roEnd(false); }); roList.addEventListener('pointercancel', function () { roEnd(true); });
      roList.addEventListener('keydown', function (e) {
        var items = roItems(), cur = items.indexOf(document.activeElement); if (cur < 0) return;
        if (e.key === 'Escape' && roGrabbed) { e.preventDefault(); var ref = items.filter(function (i) { return i !== roGrabbed; })[roOrigIndex]; roList.insertBefore(roGrabbed, ref || roLine); roGrabbed.classList.remove('is-grabbed'); roGrabbed.focus(); roGrabbed = null; roLive.textContent = ''; return; }
        if ((e.key === ' ' || e.key === 'Enter') && demo.classList.contains('on-keyboard')) { e.preventDefault(); if (roGrabbed) { roGrabbed.classList.remove('is-grabbed'); roAnnounce(roGrabbed); roGrabbed = null; } else { roGrabbed = items[cur]; roOrigIndex = cur; roGrabbed.classList.add('is-grabbed'); roLive.textContent = stageEl.getAttribute('data-grab'); } return; }
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); var d = e.key === 'ArrowDown' ? 1 : -1; if (roGrabbed) { var n = cur + d; if (n < 0 || n >= items.length) return; roList.insertBefore(roGrabbed, d > 0 ? items[n].nextSibling : items[n]); roGrabbed.focus(); roAnnounce(roGrabbed); } else { var t = items[Math.max(0, Math.min(items.length - 1, cur + d))]; items.forEach(function (i) { i.tabIndex = -1; }); t.tabIndex = 0; t.focus(); } }
      });
    }
    // Typography demos -------------------------------------------------------
    var scBars = demo.querySelector('.sc2-bars');
    if (scBars) {
      var HYB = [11, 12, 13, 14, 16, 18, 20, 24, 30, 38];
      function scUpdate() {
        var r = Number(demo.getAttribute('data-ratio')) || 1.25, hyb = demo.classList.contains('on-hybrid'), sizes = hyb ? HYB : [];
        if (!hyb) for (var i = -3; i < 7; i++) sizes.push(16 * Math.pow(r, i));
        scBars.innerHTML = sizes.map(function (v) { var frac = Math.abs(v - Math.round(v)) > 0.01; return '<span class="sc2-bar' + (frac ? ' is-frac' : '') + '" style="--s:' + Math.min(v, 56) + '"><i>' + (frac ? v.toFixed(1) : Math.round(v)) + '</i></span>'; }).join('');
      }
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (r) { r.addEventListener('input', scUpdate); r.addEventListener('change', scUpdate); }); scUpdate();
    }
    var vfRead = demo.querySelector('.vf-read');
    if (vfRead) {
      var vfStage = demo.querySelector('.demo-stage');
      function vfUpdate() { vfRead.querySelector('.vf-w').textContent = 'wght ' + (demo.getAttribute('data-wght') || 400); vfRead.querySelector('.vf-opsz').textContent = demo.classList.contains('on-opsz') ? vfStage.getAttribute('data-on') : vfStage.getAttribute('data-off'); }
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (r) { r.addEventListener('input', vfUpdate); r.addEventListener('change', vfUpdate); }); vfUpdate();
    }
    var nfTable = demo.querySelector('.nf-table');
    if (nfTable) {
      function nfUpdate() {
        var loc = demo.classList.contains('on-locale') ? 'pt-BR' : 'en-US', cur = loc === 'pt-BR' ? 'BRL' : 'USD';
        var money = new Intl.NumberFormat(loc, { style: 'currency', currency: cur }), pct = new Intl.NumberFormat(loc, { style: 'percent', minimumFractionDigits: 1, maximumFractionDigits: 2 });
        Array.prototype.forEach.call(nfTable.querySelectorAll('[data-v]'), function (td) { td.textContent = money.format(Number(td.getAttribute('data-v'))); });
        Array.prototype.forEach.call(nfTable.querySelectorAll('[data-p]'), function (td) { td.textContent = pct.format(Number(td.getAttribute('data-p')) / 100); });
      }
      var locSw = demo.querySelector('input[name="locale"]'); if (locSw) locSw.addEventListener('change', nfUpdate); nfUpdate();
    }
    var tcTitle = demo.querySelector('.tc-title');
    if (tcTitle) {
      var tcStrings = (demo.querySelector('.demo-stage').getAttribute('data-strings') || '').split('|');
      function tcUpdate() { var i = Math.max(1, Math.min(tcStrings.length, Number(demo.getAttribute('data-content')) || 1)) - 1; tcTitle.textContent = tcStrings[i]; tcTitle.setAttribute('title', tcStrings[i]); }
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input[type="range"]'), function (r) { r.addEventListener('input', tcUpdate); }); tcUpdate();
    }
    var flCard = demo.querySelector('[data-reload]');
    if (flCard) {
      var flStage = demo.querySelector('.demo-stage'), flStatus = demo.querySelector('.fl-status'), flTimer = null;
      function flReload() {
        flCard._ran = true; clearTimeout(flTimer); flCard.classList.remove('is-shifted'); flCard.classList.add('is-fallback'); flStatus.textContent = flStage.getAttribute('data-loading');
        var h0 = flCard.offsetHeight, w0 = flCard.querySelector('p').getBoundingClientRect().height;
        flTimer = setTimeout(function () {
          if (demo.classList.contains('on-optional')) { flStatus.textContent = flStage.getAttribute('data-kept'); return; }
          flCard.classList.remove('is-fallback');
          var shift = Math.abs(flCard.querySelector('p').getBoundingClientRect().height - w0) + Math.abs(flCard.offsetHeight - h0 - (flCard.querySelector('p').getBoundingClientRect().height - w0));
          shift = Math.round(shift);
          flStatus.textContent = flStage.getAttribute('data-swapped') + ' ' + shift + ' ' + flStage.getAttribute('data-shift');
          flCard.classList.toggle('is-shifted', shift > 0);
        }, 900);
      }
      flCard.addEventListener('click', flReload);
      demo._replay = function () { if (flCard._ran) flReload(); };
      flCard.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { flReload(); e.preventDefault(); } });
    }
    var i18nRow = demo.querySelector('.i18n-row');
    if (i18nRow) {
      var deSw = demo.querySelector('input[name="german"]');
      function i18nUpdate() { var de = demo.classList.contains('on-german'); Array.prototype.forEach.call(i18nRow.querySelectorAll('.i18n-btn'), function (b) { b.textContent = b.getAttribute(de ? 'data-de' : 'data-en'); b.setAttribute('lang', de ? 'de' : document.documentElement.lang); }); }
      if (deSw) deSw.addEventListener('change', i18nUpdate);
    }
    // Color demos ------------------------------------------------------------
    var gm = demo.querySelectorAll('.gm-step');
    if (gm.length) {
      var gmCount = demo.querySelector('.gm-count'), gmLabel = demo.querySelector('.demo-stage').getAttribute('data-clipped-label') || 'clipped';
      function gmUpdate() {
        var hue = Number(demo.getAttribute('data-hue')) || 0, scale = Number(demo.getAttribute('data-scale')) || 1, n = 0;
        Array.prototype.forEach.call(gm, function (st) { var bad = !inGamut(oklchToLinear(Number(st.getAttribute('data-l')), Number(st.getAttribute('data-c')) * scale, hue)); st.classList.toggle('is-clipped', bad); if (bad) n++; });
        gmCount.textContent = n + ' / ' + gm.length + ' ' + gmLabel;
      }
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input[type="range"]'), function (r) { r.addEventListener('input', gmUpdate); }); gmUpdate();
    }
    var apCard = demo.querySelector('.ap-card');
    if (apCard) {
      var stage = demo.querySelector('.demo-stage'), passT = stage.getAttribute('data-pass') || 'pass', failT = stage.getAttribute('data-fail') || 'fail';
      var wPill = demo.querySelector('.ap-wcag'), aPill = demo.querySelector('.ap-apca');
      function apUpdate() {
        var tl = Number(demo.getAttribute('data-tl')) || 0.62, bgl = demo.classList.contains('on-darkbg') ? 0.20 : 0.98;
        var yt = relY(oklchToLinear(tl, 0.02, 260)), yb = relY(oklchToLinear(bgl, 0.01, 260));
        var ratio = wcagRatio(yt, yb), lc = apcaLc(yt, yb);
        wPill.querySelector('.ap-val').textContent = ratio.toFixed(1) + ':1'; wPill.querySelector('.ap-tag').textContent = ratio >= 4.5 ? passT : failT; wPill.classList.toggle('pass', ratio >= 4.5); wPill.classList.toggle('fail', ratio < 4.5);
        aPill.querySelector('.ap-val').textContent = 'Lc ' + Math.round(Math.abs(lc)); aPill.querySelector('.ap-tag').textContent = Math.abs(lc) >= 75 ? passT : failT; aPill.classList.toggle('pass', Math.abs(lc) >= 75); aPill.classList.toggle('fail', Math.abs(lc) < 75);
      }
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (r) { r.addEventListener('input', apUpdate); r.addEventListener('change', apUpdate); }); apUpdate();
    }
    var ylBadge = demo.querySelector('.yl-badge');
    if (ylBadge) {
      var ylStage = demo.querySelector('.demo-stage'), ylPass = ylStage.getAttribute('data-pass') || 'pass', ylFail = ylStage.getAttribute('data-fail') || 'fail', ylRead = demo.querySelector('.yl-read');
      function ylUpdate() {
        var l = Number(demo.getAttribute('data-yl')) || 0.85, yb = relY(oklchToLinear(l, 0.16, 90));
        var yt = demo.classList.contains('on-darktext') ? relY(oklchToLinear(0.25, 0.03, 90)) : 1;
        var ratio = wcagRatio(yt, yb); ylRead.querySelector('.yl-val').textContent = ratio.toFixed(1) + ':1'; ylRead.querySelector('.yl-tag').textContent = ratio >= 4.5 ? ylPass : ylFail; ylRead.classList.toggle('pass', ratio >= 4.5); ylRead.classList.toggle('fail', ratio < 4.5);
      }
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (r) { r.addEventListener('input', ylUpdate); r.addEventListener('change', ylUpdate); }); ylUpdate();
    }
    // UX demos --------------------------------------------------------------
    // Pop-out: clicking a distractor wobbles it, so the miss is felt
    var ppGrid = demo.querySelector('.pp-grid');
    if (ppGrid) ppGrid.addEventListener('click', function (e) { var d = e.target.closest('.pp-dot'); if (d && !d.classList.contains('pp-target')) { d.classList.remove('is-miss'); void d.offsetWidth; d.classList.add('is-miss'); } });
    // Signifiers / structure: single pick
    var picks = demo.querySelectorAll('[data-pick]');
    if (picks.length) {
      var stateEl = demo.querySelector('.sg-state');
      Array.prototype.forEach.call(picks, function (el) {
        function pick() { Array.prototype.forEach.call(picks, function (o) { o.classList.remove('is-picked'); }); el.classList.add('is-picked'); if (stateEl) stateEl.textContent = el.textContent + ' ✓'; }
        el.addEventListener('click', pick);
        el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { pick(); e.preventDefault(); } });
      });
    }
    // Chunk code: format input in 3-3
    var code = demo.querySelector('[data-code]');
    if (code) code.addEventListener('input', function () { var d = code.value.replace(/\D/g, '').slice(0, 6); code.value = demo.classList.contains('on-chunked') && d.length > 3 ? d.slice(0, 3) + ' ' + d.slice(3) : d; });
    // Postal code inference
    var zip = demo.querySelector('[data-zip]');
    if (zip) {
      var table = { '01310100': ['São Paulo', 'SP'], '20040020': ['Rio de Janeiro', 'RJ'], '30130010': ['Belo Horizonte', 'MG'], '80010000': ['Curitiba', 'PR'], '70040010': ['Brasília', 'DF'] };
      var city = demo.querySelector('.in-city'), state = demo.querySelector('.in-state');
      function zipUpdate() {
        var d = zip.value.replace(/\D/g, '').slice(0, 8); zip.value = d.length > 5 ? d.slice(0, 5) + '-' + d.slice(5) : d;
        var hit = demo.classList.contains('on-infer') && table[d];
        city.value = hit ? hit[0] : ''; state.value = hit ? hit[1] : '';
        city.classList.toggle('is-filled', !!hit); state.classList.toggle('is-filled', !!hit);
        city.readOnly = state.readOnly = demo.classList.contains('on-infer');
      }
      zip.addEventListener('input', zipUpdate); zipUpdate();
      var inferSw = demo.querySelector('input[name="infer"]'); if (inferSw) inferSw.addEventListener('change', zipUpdate);
    }
    // Consent: deceptive pattern pre-checks the boxes
    var decSw = demo.querySelector('input[name="deceptive"]');
    if (decSw && demo.querySelector('[data-consent]')) decSw.addEventListener('change', function () { Array.prototype.forEach.call(demo.querySelectorAll('[data-consent]'), function (c) { c.checked = decSw.checked; }); });
    // Postel: liberal phone input
    var phone = demo.querySelector('[data-phone]');
    if (phone) {
      var norm = demo.querySelector('.po-norm');
      function phoneUpdate() {
        var v = phone.value.trim(); demo.classList.remove('is-valid', 'is-invalid'); if (!v) return;
        var digits = v.replace(/\D/g, '');
        var liberal = demo.classList.contains('on-liberal');
        var ok = liberal ? (digits.length === 10 || digits.length === 11) : /^\d{10,11}$/.test(v);
        if (ok) { norm.textContent = '+55 ' + digits.slice(0, 2) + ' ' + digits.slice(2, digits.length - 4) + '-' + digits.slice(-4); demo.classList.add('is-valid'); } else demo.classList.add('is-invalid');
      }
      phone.addEventListener('input', phoneUpdate); phoneUpdate();
      var libSw = demo.querySelector('input[name="liberal"]'); if (libSw) libSw.addEventListener('change', phoneUpdate);
    }
    // Endowed progress
    var edList = demo.querySelector('.ed-list');
    if (edList) {
      var fill = demo.querySelector('.ed-fill'), count = demo.querySelector('.ed-count');
      function edUpdate() {
        var endow = demo.classList.contains('on-endow');
        var rows = Array.prototype.filter.call(edList.querySelectorAll('.ed-input'), function (i) { return endow || !i.hasAttribute('data-endowed'); });
        var done = rows.filter(function (i) { return i.checked; }).length;
        fill.style.width = (rows.length ? done / rows.length * 100 : 0) + '%';
        count.textContent = done + ' / ' + rows.length;
      }
      Array.prototype.forEach.call(edList.querySelectorAll('.ed-input'), function (i) { i.addEventListener('change', edUpdate); });
      var endowSw = demo.querySelector('input[name="endow"]'); if (endowSw) endowSw.addEventListener('change', edUpdate);
      edUpdate();
    }
    // Exit flow
    var exStart = demo.querySelector('[data-exit-start]');
    if (exStart) {
      var panel = demo.querySelector('.ex-panel'), steps = (demo.querySelector('.demo-stage').getAttribute('data-dark-steps') || '').split('|'), si = 0;
      var dTitle = demo.querySelector('.ex-d-title'), dText = demo.querySelector('.ex-d-text'), dNext = demo.querySelector('.ex-d-next'), dStep = demo.querySelector('.ex-step');
      var exLabels = (demo.querySelector('.demo-stage').getAttribute('data-labels') || 'Continue|Cancel').split('|');
      function showDark() { dTitle.textContent = steps[si]; dText.textContent = ''; dNext.textContent = si < steps.length - 1 ? exLabels[0] : exLabels[1]; dStep.textContent = (si + 1) + ' / ' + steps.length; }
      demo._replay = function () { if (panel.classList.contains('is-open')) exStart.click(); };
      exStart.addEventListener('click', function () { si = 0; panel.classList.add('is-open'); if (demo.classList.contains('on-respectful')) panel.setAttribute('data-mode', 'honest'); else { panel.setAttribute('data-mode', 'dark'); showDark(); } });
      demo.querySelector('[data-exit-do]').addEventListener('click', function () { panel.setAttribute('data-mode', 'done'); });
      dNext.addEventListener('click', function () { if (si < steps.length - 1) { si++; showDark(); } else panel.setAttribute('data-mode', 'done'); });
      Array.prototype.forEach.call(demo.querySelectorAll('[data-exit-reset]'), function (b) { b.addEventListener('click', function () { panel.classList.remove('is-open'); panel.removeAttribute('data-mode'); }); });
    }
    // Human hours
    var hrOut = demo.querySelector('.hr-hours');
    if (hrOut) {
      function hrUpdate() { var users = Number(demo.getAttribute('data-users')) || 50, secs = Number(demo.getAttribute('data-seconds')) || 4; hrOut.textContent = Math.floor(users * 1000 * secs / 3600); }
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input[type="range"]'), function (r) { r.addEventListener('input', hrUpdate); }); hrUpdate();
    }
    // IA: deep vs shallow, count clicks
    var iaWrap = demo.querySelector('.ia-wrap');
    if (iaWrap) {
      var clicks = 0, clicksEl = demo.querySelector('.ia-clicks');
      function bump() { clicks++; clicksEl.textContent = clicks; }
      Array.prototype.forEach.call(demo.querySelectorAll('[data-ia-top]'), function (t) { t.addEventListener('click', function () { bump(); var m = t.parentNode, open = m.classList.contains('is-open'); Array.prototype.forEach.call(demo.querySelectorAll('.ia-menu'), function (x) { x.classList.remove('is-open'); }); if (!open) m.classList.add('is-open'); }); });
      Array.prototype.forEach.call(demo.querySelectorAll('[data-ia-item]'), function (it) { it.addEventListener('click', function () { bump(); if (it.classList.contains('ia-goal')) { it.classList.add('is-hit'); setTimeout(function () { it.classList.remove('is-hit'); clicks = 0; clicksEl.textContent = '0'; Array.prototype.forEach.call(demo.querySelectorAll('.ia-menu'), function (x) { x.classList.remove('is-open'); }); }, 1500); } }); });
      var shSw = demo.querySelector('input[name="shallow"]'); if (shSw) shSw.addEventListener('change', function () { clicks = 0; clicksEl.textContent = '0'; Array.prototype.forEach.call(demo.querySelectorAll('.ia-menu'), function (x) { x.classList.remove('is-open'); }); });
    }
    // Onboarding: tour vs hint
    var trStart = demo.querySelector('[data-tour-start]');
    if (trStart) {
      var app = demo.querySelector('.tr-app'), tsteps = (demo.querySelector('.demo-stage').getAttribute('data-tour-steps') || '').split('|'), ti = 0;
      var bTitle = demo.querySelector('.tr-b-title'), bText = demo.querySelector('.tr-b-text'), bNext = demo.querySelector('[data-tour-next]');
      var pos = [[80, 40], [80, 12], [150, 52]], trLabels = (demo.querySelector('.demo-stage').getAttribute('data-labels') || 'Next|Done').split('|');
      function showStep() { bTitle.textContent = (ti + 1) + ' / ' + tsteps.length; bText.textContent = tsteps[ti]; bNext.textContent = ti < tsteps.length - 1 ? trLabels[0] : trLabels[1]; app.style.setProperty('--bx', pos[ti][0] + 'px'); app.style.setProperty('--by', pos[ti][1] + 'px'); }
      demo._replay = function () { if (app.classList.contains('is-running')) trStart.click(); };
      trStart.addEventListener('click', function () { app.classList.add('is-running'); app.classList.remove('is-created'); if (demo.classList.contains('on-tourmode')) { ti = 0; app.classList.add('is-touring'); showStep(); } else app.classList.add('is-hinting'); });
      bNext.addEventListener('click', function () { if (ti < tsteps.length - 1) { ti++; showStep(); } else { app.classList.remove('is-touring'); app.classList.add('is-hinting'); } });
      demo.querySelector('[data-tour-new]').addEventListener('click', function () { app.classList.remove('is-hinting', 'is-touring'); app.classList.add('is-created', 'is-running'); demo.querySelector('.tr-empty span').textContent = demo.querySelector('[data-tour-new]').textContent + ' ✓'; setTimeout(function () { app.classList.remove('is-running', 'is-created'); demo.querySelector('.tr-empty span').textContent = demo.querySelector('.tr-empty').getAttribute('data-empty') || demo.querySelector('.tr-empty span').getAttribute('data-orig'); }, 2200); });
      var emptySpan = demo.querySelector('.tr-empty span'); emptySpan.setAttribute('data-orig', emptySpan.textContent);
    }
    // Guard metric values
    var gdConv = demo.querySelector('.gd-conv-val');
    if (gdConv) {
      var gdRet = demo.querySelector('.gd-ret-val');
      function gdUpdate() { var p = Number(demo.getAttribute('data-push')) || 0; gdConv.textContent = Math.round(20 + p * 0.6) + '%'; gdRet.textContent = Math.round(70 - p * 0.55) + '%'; }
      Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input[type="range"]'), function (r) { r.addEventListener('input', gdUpdate); }); gdUpdate();
    }
    Array.prototype.forEach.call(demo.querySelectorAll('[data-drag]'), function (box) {
      var track = box.parentNode, startX = 0, startPos = 0, pos = 0, max = 0;
      function setX(x) {
        pos = Math.max(0, Math.min(max, x));
        box.style.setProperty('--x', pos + 'px');
        box.setAttribute('aria-valuenow', String(Math.round(pos / (max || 1) * 100)));
      }
      box.addEventListener('pointerdown', function (e) {
        max = track.clientWidth - box.offsetWidth - 24;
        startX = e.clientX; startPos = pos;
        box.classList.remove('is-settling'); box.classList.add('is-dragging');
        try { box.setPointerCapture(e.pointerId); } catch (err) {}
        e.preventDefault();
      });
      box.addEventListener('pointermove', function (e) {
        if (!box.classList.contains('is-dragging')) return;
        setX(startPos + (e.clientX - startX));
      });
      function release() {
        if (!box.classList.contains('is-dragging')) return;
        box.classList.remove('is-dragging'); box.classList.add('is-settling');
        setX(0); // let go: the spring (or ease-out) brings it home
      }
      box.addEventListener('pointerup', release);
      box.addEventListener('pointercancel', release);
      box.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
          max = track.clientWidth - box.offsetWidth - 24;
          box.classList.add('is-settling');
          setX(pos + (e.key === 'ArrowRight' ? 40 : -40));
          e.preventDefault();
        }
      });
    });
  });
})();

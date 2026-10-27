    // Development demos --------------------------------------------------------
    var dvS = demo.querySelector('.demo-stage');
    function gd(n) { return dvS ? (dvS.getAttribute('data-' + n) || '') : ''; }
    function dvOn(fn) { Array.prototype.forEach.call(demo.querySelectorAll('.demo-controls input'), function (i) { i.addEventListener('input', fn); i.addEventListener('change', fn); }); fn(); }
    function dvSeg(wrap, cls, onChange) { var bs = wrap ? wrap.querySelectorAll('.' + cls + ' .dv-seg-b') : []; Array.prototype.forEach.call(bs, function (b) { b.addEventListener('click', function () { Array.prototype.forEach.call(bs, function (x) { x.classList.remove('is-on'); }); b.classList.add('is-on'); onChange(Number(b.getAttribute('data-v')), b); }); }); return function () { var on = wrap.querySelector('.' + cls + ' .dv-seg-b.is-on'); return on ? Number(on.getAttribute('data-v')) : -1; }; }
    function dvRead(el, txt, cls) { if (!el) return; el.textContent = txt; el.classList.remove('dv-bad', 'dv-good'); if (cls) el.classList.add(cls); }
    var dvOut = demo.querySelector('.demo-controls output');
    // 01 HTTP
    var dv01 = demo.querySelector('.dv01-wrap');
    if (dv01) {
      var dv01res = dv01.querySelector('.dv01-res'), dv01st = dv01.querySelector('.dv01-status'), dv01rd = dv01.querySelector('.dv01-read'), dv01m = -1;
      var dv01get = dvSeg(dv01, 'dv01-m', function (v) { dv01m = v; dv01show(); });
      function dv01show() { if (dv01m < 0) { dv01st.textContent = ''; dv01rd.textContent = gd('first'); dv01res.className = 'dv01-res'; return; } var anon = demo.classList.contains('on-anon'), other = demo.classList.contains('on-other'), code; if (anon) code = 's401'; else if (other) code = dv01m === 0 ? 's404' : 's403'; else code = ['s200', 's201', 's200', 's204'][dv01m]; var txt = gd(code), i = txt.indexOf(' · '); dv01st.textContent = txt.slice(0, i); dv01rd.textContent = txt.slice(i + 3); dv01res.className = 'dv01-res ' + (code === 's401' || code === 's403' || code === 's404' ? 'is-no' : 'is-ok'); }
      dvOn(dv01show); demo._replay = function () {};
    }
    // 02 TLS
    var dv02 = demo.querySelector('.dv02-wrap');
    if (dv02) {
      var dv02rd = dv02.querySelector('.dv02-read');
      Array.prototype.forEach.call(dv02.querySelectorAll('.dv02-row'), function (r) { var plain = r.querySelector('.dv02-plain').textContent; r.querySelector('.dv02-enc').textContent = plain.split(':')[0] + ': ••••••••••••'; });
      function dv02upd() { dvRead(dv02rd, demo.classList.contains('on-stolen') ? gd('rest') : '', demo.classList.contains('on-stolen') ? 'dv-bad' : ''); }
      dv02.querySelector('.dv02-sniff').addEventListener('click', function () { var h = demo.classList.contains('on-https'); dvRead(dv02rd, gd(h ? 'h' : 'p'), h ? 'dv-good' : 'dv-bad'); });
      dvOn(dv02upd); demo._replay = function () { if (!demo.classList.contains('on-stolen')) dv02.querySelector('.dv02-sniff').click(); };
    }
    // 03 storage
    var dv03 = demo.querySelector('.dv03-wrap');
    if (dv03) {
      var dv03b = dv03.querySelectorAll('.dv03-box'), dv03rd = dv03.querySelector('.dv03-read');
      function dv03clear() { Array.prototype.forEach.call(dv03b, function (b) { b.classList.remove('is-read', 'is-sent'); }); }
      dvOn(function () { dv03b[0].classList.toggle('is-locked', demo.classList.contains('on-httponly')); dv03clear(); dv03rd.textContent = ''; });
      dv03.querySelector('.dv03-run').addEventListener('click', function () { dv03clear(); if (!demo.classList.contains('on-xss')) { dvRead(dv03rd, gd('noxss')); return; } var ho = demo.classList.contains('on-httponly'); dv03b[1].classList.add('is-read'); if (!ho) dv03b[0].classList.add('is-read'); dvRead(dv03rd, gd('read') + ' ' + gd(ho ? 'got2' : 'got'), 'dv-bad'); });
      dv03.querySelector('.dv03-req').addEventListener('click', function () { dv03clear(); dv03b[0].classList.add('is-sent'); dvRead(dv03rd, gd('sent')); });
      demo._replay = function () { if (demo.classList.contains('on-xss')) dv03.querySelector('.dv03-run').click(); };
    }
    // 04 CORS
    var dv04 = demo.querySelector('.dv04-wrap');
    if (dv04) {
      var dv04rd = dv04.querySelector('.dv04-read'), dv04from = dv04.querySelector('.dv04-from'), dv04acao = dv04.querySelector('.dv04-acao'), dv04src = dv04.querySelector('.dv04-src b');
      dvOn(function () { var c = demo.classList.contains('on-curl'); dv04from.textContent = gd(c ? 'fromc' : 'fromb'); dv04src.textContent = c ? 'curl' : 'evil.example'; dv04acao.textContent = demo.classList.contains('on-allow') ? 'https://app.example' : '*'; dv04.classList.remove('is-blocked', 'is-leak'); dv04rd.textContent = ''; });
      dv04.querySelector('.dv04-send').addEventListener('click', function () { dv04.classList.remove('is-blocked', 'is-leak'); if (demo.classList.contains('on-curl')) { dvRead(dv04rd, gd('curlr'), 'dv-bad'); dv04.classList.add('is-leak'); } else if (demo.classList.contains('on-allow')) { dvRead(dv04rd, gd('blocked'), 'dv-good'); dv04.classList.add('is-blocked'); } else { dvRead(dv04rd, gd('read'), 'dv-bad'); dv04.classList.add('is-leak'); } });
      demo._replay = function () { dv04.querySelector('.dv04-send').click(); };
    }
    // 05 AuthN vs AuthZ
    var dv05 = demo.querySelector('.dv05-wrap');
    if (dv05) {
      var dv05rd = dv05.querySelector('.dv05-read'), dv05acts = dv05.querySelectorAll('.dv05-act'), dv05role = 1;
      var dv05get = dvSeg(dv05, 'dv05-role', function (v) { dv05role = v; dv05upd(); });
      function dv05upd() { Array.prototype.forEach.call(dv05acts, function (a) { a.classList.toggle('is-hidden', dv05role !== 1); var r = a.querySelector('.dv05-res'); r.textContent = ''; r.className = 'dv05-res'; }); dv05rd.textContent = gd('first'); }
      Array.prototype.forEach.call(dv05acts, function (a) {
        var r = a.querySelector('.dv05-res');
        a.querySelector('.dv05-btn').addEventListener('click', function () { var ok = dv05role === 1; dvRead(r, ok ? gd('ok') : gd('no'), ok ? 'dv-good' : 'dv-bad'); });
        a.querySelector('.dv05-api').addEventListener('click', function () { var ok = dv05role === 1; if (ok) { dvRead(r, gd('ok'), 'dv-good'); } else { dvRead(r, gd('leak'), 'dv-bad'); } });
      });
      dvOn(dv05upd); demo._replay = function () {};
    }
    // 06 auth flows
    var dv06 = demo.querySelector('.dv06-wrap');
    if (dv06) {
      var dv06st = dv06.querySelector('.dv06-state'), dv06rec = dv06.querySelector('.dv06-rec'), dv06rd = dv06.querySelector('.dv06-read'), dv06up = false;
      dv06.querySelector('.dv06-signup').addEventListener('click', function () { dv06up = true; dvRead(dv06st, gd('created'), 'dv-good'); dv06rd.textContent = ''; });
      dv06.querySelector('.dv06-signin').addEventListener('click', function () { if (!dv06up) { dvRead(dv06st, gd(demo.classList.contains('on-neutral') ? 'rneutral' : 'rleak').replace(/recovery link|link de recuperação/, 'link'), ''); dv06rd.textContent = gd('first'); return; } if (demo.classList.contains('on-verify')) dvRead(dv06st, gd('blocked'), 'dv-good'); else dvRead(dv06st, gd('unverified'), 'dv-bad'); });
      dv06.querySelector('.dv06-recover').addEventListener('click', function () { var n = demo.classList.contains('on-neutral'); dvRead(dv06rec, gd(n ? 'rneutral' : 'rleak'), n ? 'dv-good' : 'dv-bad'); });
      dv06rd.textContent = gd('first'); demo._replay = function () { if (dv06rec.textContent) dv06.querySelector('.dv06-recover').click(); if (dv06up) dv06.querySelector('.dv06-signin').click(); };
    }
    // 07 tokens
    var dv07 = demo.querySelector('.dv07-wrap');
    if (dv07) {
      var dv07t = 0, dv07issued = 0, dv07n = 1, dv07T = dv07.querySelector('.dv07-t'), dv07a = dv07.querySelector('.dv07-a'), dv07r = dv07.querySelector('.dv07-r'), dv07bar = dv07.querySelector('.dv07-bar b'), dv07as = dv07.querySelector('.dv07-as'), dv07rs = dv07.querySelector('.dv07-rs'), dv07rd = dv07.querySelector('.dv07-read'), dv07dead = false;
      function dv07ttl() { return Number(demo.getAttribute('data-ttl')) || 30; }
      function dv07paint(note) { var age = dv07t - dv07issued, left = Math.max(0, dv07ttl() - age); dv07T.textContent = dv07t; dv07bar.style.width = (left / dv07ttl() * 100) + '%'; dv07a.classList.toggle('is-expired', left === 0); dv07as.textContent = left ? left + ' min · ' + gd('valid') : gd('expired'); dv07rs.textContent = '#' + dv07n; if (note !== undefined) dv07rd.textContent = note; }
      dv07.querySelector('.dv07-use').addEventListener('click', function () { if (dv07dead) return; dv07t += 20; if (dv07t - dv07issued >= dv07ttl()) { dv07issued = dv07t; if (demo.classList.contains('on-rotate')) dv07n++; dv07paint(gd('expired')); } else dv07paint(''); });
      dv07.querySelector('.dv07-steal').addEventListener('click', function () { dv07a.classList.remove('is-revoked', 'is-hijacked'); dv07r.classList.remove('is-revoked', 'is-hijacked'); if (demo.classList.contains('on-rotate')) { dv07dead = true; dv07r.classList.add('is-revoked'); dv07a.classList.add('is-revoked'); dvRead(dv07rd, gd('rev'), 'dv-good'); } else { dv07r.classList.add('is-hijacked'); dvRead(dv07rd, gd('hij'), 'dv-bad'); } });
      dvOn(function () { dv07paint(); }); dv07rd.textContent = gd('first');
      demo._replay = function () { dv07t = 0; dv07issued = 0; dv07n = 1; dv07dead = false; dv07a.classList.remove('is-revoked', 'is-hijacked'); dv07r.classList.remove('is-revoked', 'is-hijacked'); dv07paint(gd('first')); };
    }
    // 08 abuse
    var dv08 = demo.querySelector('.dv08-wrap');
    if (dv08) {
      var dv08n = 0, dv08login = dv08.querySelector('.dv08-login'), dv08out = dv08.querySelector('.dv08-out'), dv08c = dv08.querySelector('.dv08-count b'), dv08rd = dv08.querySelector('.dv08-read'), dv08T;
      dv08.querySelector('.dv08-try').addEventListener('click', function () { dv08n++; dv08c.textContent = dv08n; if (demo.classList.contains('on-limit') && dv08n >= 5) { dvRead(dv08out, gd('wait'), 'dv-bad'); dv08login.classList.add('is-locked'); clearTimeout(dv08T); dv08T = setTimeout(function () { dv08login.classList.remove('is-locked'); dv08n = 0; dv08c.textContent = '0'; dv08out.textContent = ''; }, 2500); } else dvRead(dv08out, gd('wrong'), ''); dv08rd.textContent = ''; });
      dv08.querySelector('.dv08-right').addEventListener('click', function () { if (dv08login.classList.contains('is-locked')) { dvRead(dv08out, gd('wait'), 'dv-bad'); return; } dvRead(dv08out, gd(demo.classList.contains('on-mfa') ? 'code' : 'sin'), 'dv-good'); dv08rd.textContent = ''; });
      dv08rd.textContent = gd('first'); demo._replay = function () {};
    }
    // 09 data model
    var dv09 = demo.querySelector('.dv09-wrap');
    if (dv09) {
      var dv09rows = dv09.querySelectorAll('.dv09-row'), dv09rd = dv09.querySelector('.dv09-read'), dv09deleted = false;
      function dv09reset() { Array.prototype.forEach.call(dv09rows, function (r) { r.classList.remove('is-lit', 'is-gone', 'is-orphan'); }); dv09deleted = false; dv09rd.textContent = gd('hint'); }
      Array.prototype.forEach.call(dv09.querySelectorAll('.dv09-table[data-t="0"] .dv09-row'), function (p) { p.addEventListener('click', function () { if (dv09deleted) return; var o = p.getAttribute('data-owner'); Array.prototype.forEach.call(dv09rows, function (r) { r.classList.toggle('is-lit', r.getAttribute('data-owner') === o); }); }); });
      dv09.querySelector('.dv09-del').addEventListener('click', function () { dv09deleted = true; var c = demo.classList.contains('on-cascade'); Array.prototype.forEach.call(dv09rows, function (r) { r.classList.remove('is-lit'); if (r.getAttribute('data-owner') !== 'ana') return; var isProfile = r.parentNode.getAttribute('data-t') === '0'; if (c || isProfile) r.classList.add('is-gone'); else r.classList.add('is-orphan'); }); dvRead(dv09rd, gd(c ? 'gone' : 'orphan'), c ? 'dv-good' : 'dv-bad'); });
      dv09reset(); demo._replay = function () { var was = dv09deleted; dv09reset(); if (was) dv09.querySelector('.dv09-del').click(); };
    }
    // 10 RLS
    var dv10 = demo.querySelector('.dv10-wrap');
    if (dv10) {
      var dv10rows = dv10.querySelectorAll('.dv10-row'), dv10rd = dv10.querySelector('.dv10-read'), dv10cnt = dv10.querySelector('.dv10-count'), dv10who = 0, dv10ran = false, dv10names = ['', 'ana', 'rui'];
      dvSeg(dv10, 'dv10-as', function (v) { dv10who = v; if (dv10ran) dv10run(); });
      function dv10run() { dv10ran = true; var rls = demo.classList.contains('on-rls'), left = demo.classList.contains('on-leftover'), n = 0, leak = 0; Array.prototype.forEach.call(dv10rows, function (r) { var allowed = r.getAttribute('data-vis') === 'public' || r.getAttribute('data-owner') === dv10names[dv10who]; var vis = !rls || left || allowed; r.classList.toggle('is-vis', vis && allowed); r.classList.toggle('is-leak', vis && !allowed); if (vis) n++; if (vis && !allowed) leak++; }); dv10cnt.textContent = n + ' ' + gd('r'); dvRead(dv10rd, !rls ? gd('norls') : left ? gd('leftover') : '', leak ? 'dv-bad' : 'dv-good'); }
      dv10.querySelector('.dv10-run').addEventListener('click', dv10run); dv10rd.textContent = gd('first'); dvOn(function () { if (dv10ran) dv10run(); }); demo._replay = function () {};
    }
    // 11 visibility
    var dv11 = demo.querySelector('.dv11-wrap');
    if (dv11) {
      var dv11vis = 2, dv11label = dv11.querySelector('.dv11-label'), dv11rd = dv11.querySelector('.dv11-read'), dv11viewers = dv11.querySelectorAll('.dv11-viewer'), dv11labels = gd('labels').split('|'), dv11names = gd('vis').split('|');
      dvSeg(dv11, 'dv11-vis', function (v) { dv11vis = v; dv11upd(); });
      function dv11upd() { dv11label.textContent = dv11labels[dv11vis]; Array.prototype.forEach.call(dv11viewers, function (b) { b.classList.remove('is-yes', 'is-no', 'is-leak'); }); dv11rd.textContent = gd('first'); }
      Array.prototype.forEach.call(dv11viewers, function (b) { b.addEventListener('click', function () { var v = Number(b.getAttribute('data-v')), can = v === 2 || (v === 1 && dv11vis <= 1) || (v === 0 && dv11vis === 0), leak = !can && demo.classList.contains('on-uionly') && v === 1; Array.prototype.forEach.call(dv11viewers, function (x) { x.classList.remove('is-yes', 'is-no', 'is-leak'); }); b.classList.add(leak ? 'is-leak' : can ? 'is-yes' : 'is-no'); dvRead(dv11rd, b.textContent + ' ' + (leak ? gd('leak') : can ? gd('yes') : gd('no')), leak ? 'dv-bad' : can ? 'dv-good' : ''); }); });
      dv11.querySelector('.dv11-new').addEventListener('click', function () { var p = demo.classList.contains('on-defpriv'); dvRead(dv11rd, gd('newmsg').replace('%s', dv11names[p ? 2 : 0].toLowerCase()), p ? 'dv-good' : 'dv-bad'); });
      dvOn(dv11upd); demo._replay = function () {};
    }
    // 12 IDOR
    var dv12 = demo.querySelector('.dv12-wrap');
    if (dv12) {
      var dv12id = dv12.querySelector('.dv12-id'), dv12res = dv12.querySelector('.dv12-res'), dv12rd = dv12.querySelector('.dv12-read'), dv12last = 'mine';
      function dv12show(which) { dv12last = which; var u = demo.classList.contains('on-uuid'), rls = demo.classList.contains('on-rls'); dv12res.className = 'dv12-res'; dv12rd.textContent = ''; if (which === 'mine') { dv12id.textContent = u ? '8c1f…42a0' : '42'; dv12res.textContent = gd('ok'); dv12res.classList.add('is-ok'); } else if (which === 'next') { dv12id.textContent = u ? '????…????' : '43'; if (u) { dv12res.textContent = gd('guess'); } else if (rls) { dv12res.textContent = gd('empty'); dv12res.classList.add('is-ok'); } else { dv12res.textContent = gd('leak'); dv12res.classList.add('is-leak'); } } else { dv12id.textContent = u ? '3e7b…91cd' : '43'; if (rls) { dv12res.textContent = gd('empty'); dv12res.classList.add('is-ok'); } else { dv12res.textContent = gd('leak'); dv12res.classList.add('is-leak'); } } }
      dv12.querySelector('.dv12-mine').addEventListener('click', function () { dv12show('mine'); }); dv12.querySelector('.dv12-next').addEventListener('click', function () { dv12show('next'); }); dv12.querySelector('.dv12-leaked').addEventListener('click', function () { dv12show('leaked'); });
      dv12show('mine'); dv12rd.textContent = gd('first'); demo._replay = function () { dv12show(dv12last); };
    }
    // 13 XSS
    var dv13 = demo.querySelector('.dv13-wrap');
    if (dv13) {
      var dv13out = dv13.querySelector('.dv13-out'), dv13rd = dv13.querySelector('.dv13-read'), dv13i = -1, dv13pays = dv13.querySelectorAll('.dv13-pay');
      function dv13show() { Array.prototype.forEach.call(dv13pays, function (b, i) { b.classList.toggle('is-on', i === dv13i); }); if (dv13i < 0) { dv13out.textContent = ''; dv13rd.textContent = gd('first'); return; } var p = gd('p' + dv13i), html = demo.classList.contains('on-html'), csp = demo.classList.contains('on-csp'); dv13out.className = 'dv13-out'; if (!html || dv13i === 0) { dv13out.textContent = p; if (html && dv13i === 0) dv13out.className = 'dv13-out'; else dv13out.classList.add('is-code'); dvRead(dv13rd, gd('text'), 'dv-good'); return; } if (csp) { dv13out.innerHTML = '<span class="dv13-blk">steal()</span>'; dvRead(dv13rd, gd('blocked'), 'dv-good'); } else { dv13out.innerHTML = '<span class="dv13-alert">steal() → session sent to evil.example</span>'; dvRead(dv13rd, gd('ran'), 'dv-bad'); } }
      Array.prototype.forEach.call(dv13pays, function (b, i) { b.addEventListener('click', function () { dv13i = i; dv13show(); }); });
      dvOn(dv13show); demo._replay = function () {};
    }
    // 14 SQLi
    var dv14 = demo.querySelector('.dv14-wrap');
    if (dv14) {
      var dv14q = dv14.querySelector('.dv14-q'), dv14rows = dv14.querySelectorAll('.dv14-row'), dv14rd = dv14.querySelector('.dv14-read'), dv14i = -1, dv14ins = dv14.querySelectorAll('.dv14-in');
      function dv14show() { Array.prototype.forEach.call(dv14ins, function (b, i) { b.classList.toggle('is-on', i === dv14i); }); Array.prototype.forEach.call(dv14rows, function (r) { r.classList.remove('is-hit', 'is-leak'); }); if (dv14i < 0) { dv14q.textContent = ''; dv14rd.textContent = gd('first'); return; } var v = gd('i' + dv14i), param = demo.classList.contains('on-param'); if (param) { dv14q.innerHTML = "SELECT * FROM items WHERE title = <span class=\"dv14-p\">$1</span>  — $1 = '" + v.replace(/</g, '&lt;') + "'"; if (dv14i === 0) dv14rows[0].classList.add('is-hit'); dvRead(dv14rd, gd('safe'), 'dv-good'); } else { if (dv14i === 0) { dv14q.textContent = "SELECT * FROM items WHERE title = '" + v + "'"; dv14rows[0].classList.add('is-hit'); dvRead(dv14rd, '', ''); } else { dv14q.innerHTML = "SELECT * FROM items WHERE title = '<span class=\"dv14-inj\">' OR 1=1 --</span>'"; Array.prototype.forEach.call(dv14rows, function (r, k) { r.classList.add(k === 0 ? 'is-hit' : 'is-leak'); }); dvRead(dv14rd, gd('inj'), 'dv-bad'); } } }
      Array.prototype.forEach.call(dv14ins, function (b, i) { b.addEventListener('click', function () { dv14i = i; dv14show(); }); });
      dvOn(dv14show); demo._replay = function () {};
    }
    // 15 CSRF
    var dv15 = demo.querySelector('.dv15-wrap');
    if (dv15) {
      var dv15req = dv15.querySelector('.dv15-req'), dv15cred = dv15.querySelector('.dv15-cred'), dv15rd = dv15.querySelector('.dv15-read'), dv15ran = false;
      function dv15go() { dv15ran = true; var c = demo.classList.contains('on-cookie'), ss = demo.classList.contains('on-samesite'); dv15req.classList.remove('is-forged'); if (!c) { dv15cred.textContent = gd('chdr'); dvRead(dv15rd, gd('rej'), 'dv-good'); } else if (ss) { dv15cred.textContent = gd('css'); dvRead(dv15rd, gd('rej'), 'dv-good'); } else { dv15cred.textContent = gd('cyes'); dv15req.classList.add('is-forged'); dvRead(dv15rd, gd('ok'), 'dv-bad'); } }
      dv15.querySelector('.dv15-submit').addEventListener('click', dv15go); demo._replay = function () { if (dv15ran) dv15go(); };
    }
    // 16 keys
    var dv16 = demo.querySelector('.dv16-wrap');
    if (dv16) {
      var dv16rd = dv16.querySelector('.dv16-read');
      dvOn(function () { var s = demo.classList.contains('on-srv'); dvRead(dv16rd, gd(s ? 'bad' : 'good'), s ? 'dv-bad' : 'dv-good'); });
      dv16.querySelector('.dv16-scan').addEventListener('click', function () { var ig = demo.classList.contains('on-ignore'); dvRead(dv16rd, gd(ig ? 'clean' : 'found'), ig ? 'dv-good' : 'dv-bad'); });
      demo._replay = function () {};
    }
    // 17 storage
    var dv17 = demo.querySelector('.dv17-wrap');
    if (dv17) {
      var dv17url = dv17.querySelector('.dv17-url'), dv17rd = dv17.querySelector('.dv17-read'), dv17b = dv17.querySelector('.dv17-bucket'), dv17copied = false;
      dvOn(function () { dv17b.textContent = demo.classList.contains('on-private') ? 'private/lists/42/' : 'public/lists/42/'; dv17url.textContent = ''; dv17url.classList.remove('is-expired'); dv17copied = false; dv17rd.textContent = gd('first'); });
      dv17.querySelector('.dv17-copy').addEventListener('click', function () { dv17copied = true; dv17url.classList.remove('is-expired'); if (demo.classList.contains('on-private')) { var e = Number(demo.getAttribute('data-exp')) || 15; dv17url.textContent = 'https://…/object/sign/private/lists/42/camera.jpg?token=eyJ…&exp=' + (e * 60); dvRead(dv17rd, gd('signed').replace('%d', e), ''); } else { dv17url.textContent = 'https://…/object/public/lists/42/camera.jpg'; dvRead(dv17rd, gd('pub'), 'dv-bad'); } });
      dv17.querySelector('.dv17-open').addEventListener('click', function () { if (!dv17copied) { dv17rd.textContent = gd('first'); return; } if (!demo.classList.contains('on-private')) { dvRead(dv17rd, gd('pub'), 'dv-bad'); return; } var e = Number(demo.getAttribute('data-exp')) || 15; if (e > 30) { dvRead(dv17rd, gd('ok'), ''); } else { dv17url.classList.add('is-expired'); dvRead(dv17rd, gd('expired'), 'dv-good'); } });
      demo._replay = function () {};
    }
    // 18 CSP
    var dv18 = demo.querySelector('.dv18-wrap');
    if (dv18) {
      var dv18out = dv18.querySelector('.dv18-out'), dv18rd = dv18.querySelector('.dv18-read');
      dv18.querySelector('.dv18-inject').addEventListener('click', function () { var csp = demo.classList.contains('on-csp'); dv18out.innerHTML = csp ? '<span class="dv13-blk">&lt;script&gt;steal()&lt;/script&gt;</span>' : '<span class="dv13-alert">steal() ran</span>'; dvRead(dv18rd, gd(csp ? 'blk' : 'ran'), csp ? 'dv-good' : 'dv-bad'); });
      dv18.querySelector('.dv18-embed').addEventListener('click', function () { var f = demo.classList.contains('on-frame'); dv18.classList.toggle('is-framed', !f); dvRead(dv18rd, gd(f ? 'noframe' : 'framed'), f ? 'dv-good' : 'dv-bad'); });
      dv18rd.textContent = gd('first'); dvOn(function () {}); demo._replay = function () { if (dv18out.innerHTML) dv18.querySelector('.dv18-inject').click(); if (dv18.classList.contains('is-framed') || dv18rd.textContent === gd('noframe')) dv18.querySelector('.dv18-embed').click(); };
    }
    // 19 deps
    var dv19 = demo.querySelector('.dv19-wrap');
    if (dv19) {
      var dv19deps = dv19.querySelectorAll('.dv19-dep'), dv19known = dv19.querySelector('.dv19-known'), dv19rd = dv19.querySelector('.dv19-read'), dv19ran = false;
      function dv19state() { var m = Number(demo.getAttribute('data-months')) || 0, bot = demo.classList.contains('on-bot'), raw = Math.min(5, Math.floor(m / 4)), n = bot ? (m >= 4 ? 1 : 0) : raw; var order = [2, 4, 1, 3, 0]; Array.prototype.forEach.call(dv19deps, function (d) { d.classList.remove('is-vuln', 'is-fixed'); d.querySelector('.dv19-v').textContent = ''; }); for (var i = 0; i < raw; i++) { var d = dv19deps[order[i]]; if (bot && i >= n) { d.classList.add('is-fixed'); d.querySelector('.dv19-v').textContent = '↑ ' + (i < 2 ? 'high' : 'moderate') + ' · PR merged'; } else { d.classList.add('is-vuln'); d.querySelector('.dv19-v').textContent = (i < 2 ? 'high' : 'moderate'); } } dv19known.textContent = n + ' ' + gd('known'); return { n: n, raw: raw, bot: bot }; }
      dv19.querySelector('.dv19-audit').addEventListener('click', function () { dv19ran = true; var s = dv19state(); dvRead(dv19rd, gd('rep').replace('%d', s.n).replace('%d', Math.min(2, s.n)).replace('%s', gd(s.bot ? 'patched' : 'open')), s.n ? 'dv-bad' : 'dv-good'); });
      dvOn(function () { dv19state(); if (!dv19ran) dv19rd.textContent = gd('first'); }); demo._replay = function () { if (dv19ran) dv19.querySelector('.dv19-audit').click(); };
    }
    // 20 backups
    var dv20 = demo.querySelector('.dv20-wrap');
    if (dv20) {
      var dv20tbl = dv20.querySelector('.dv20-table'), dv20rows = dv20.querySelector('.dv20-rows'), dv20rd = dv20.querySelector('.dv20-read');
      dv20.querySelector('.dv20-oops').addEventListener('click', function () { dv20tbl.classList.add('is-gone'); dv20tbl.classList.remove('is-back'); dv20.classList.add('is-gone'); dvRead(dv20rd, gd('lost'), 'dv-bad'); });
      dv20.querySelector('.dv20-restore').addEventListener('click', function () { var b = demo.classList.contains('on-backup'), t = demo.classList.contains('on-tested'); if (!b) { dvRead(dv20rd, gd('nobackup'), 'dv-bad'); return; } if (!t) { dvRead(dv20rd, gd('untested'), 'dv-bad'); return; } dv20tbl.classList.remove('is-gone'); dv20tbl.classList.add('is-back'); dv20.classList.remove('is-gone'); dvRead(dv20rd, gd('ok'), 'dv-good'); });
      dv20rd.textContent = gd('first'); demo._replay = function () { if (dv20.classList.contains('is-gone')) dv20.querySelector('.dv20-restore').click(); };
    }
    // 21 personal data
    var dv21 = demo.querySelector('.dv21-wrap');
    if (dv21) {
      var dv21f = dv21.querySelectorAll('.dv21-f'), dv21rd = dv21.querySelector('.dv21-read'), dv21ans = gd('ans').split('|').map(Number), dv21notes = gd('notes').split('|'), dv21pick = [];
      Array.prototype.forEach.call(dv21f, function (f, i) { dv21pick[i] = -1; f.querySelector('.dv21-note').textContent = dv21notes[i]; var bs = f.querySelectorAll('.dv-seg-b'); Array.prototype.forEach.call(bs, function (b, k) { b.classList.toggle('is-ans', k === dv21ans[i]); b.addEventListener('click', function () { Array.prototype.forEach.call(bs, function (x) { x.classList.remove('is-on'); }); b.classList.add('is-on'); dv21pick[i] = k; dv21score(); }); }); });
      function dv21score() { var right = 0, done = 0; Array.prototype.forEach.call(dv21f, function (f, i) { if (dv21pick[i] >= 0) done++; var ok = dv21pick[i] === dv21ans[i]; if (ok) right++; f.classList.toggle('is-right', dv21pick[i] >= 0 && ok); f.classList.toggle('is-wrong', dv21pick[i] >= 0 && !ok); }); dvRead(dv21rd, demo.classList.contains('on-reveal') ? gd('score').replace('%d', right) : done ? done + ' / 7' : gd('first'), ''); }
      dvOn(dv21score); demo._replay = function () {};
    }
    // 22 legal bases
    var dv22 = demo.querySelector('.dv22-wrap');
    if (dv22) {
      var dv22rows = dv22.querySelectorAll('.dv22-row'), dv22rd = dv22.querySelector('.dv22-read'), dv22base = [1, 2, 0];
      Array.prototype.forEach.call(dv22rows, function (r, i) { dvSeg(r, 'dv22-b', function (v) { dv22base[i] = v; r.classList.remove('is-bad'); dv22rd.textContent = ''; }); });
      dv22.querySelector('.dv22-withdraw').addEventListener('click', function () { Array.prototype.forEach.call(dv22rows, function (r) { r.classList.remove('is-bad'); }); if (dv22base[0] === 0) { dv22rows[0].classList.add('is-bad'); dvRead(dv22rd, gd('wbad'), 'dv-bad'); } else { dvRead(dv22rd, gd('wok'), 'dv-good'); } });
      dv22.querySelector('.dv22-export').addEventListener('click', function () { var r = demo.classList.contains('on-rights'); dvRead(dv22rd, gd(r ? 'expok' : 'expman'), r ? 'dv-good' : 'dv-bad'); });
      dv22.querySelector('.dv22-delete').addEventListener('click', function () { var r = demo.classList.contains('on-rights'); dvRead(dv22rd, gd(r ? 'delok' : 'delman'), r ? 'dv-good' : 'dv-bad'); });
      dv22rd.textContent = gd('first'); demo._replay = function () {};
    }
    // 23 privacy by design
    var dv23 = demo.querySelector('.dv23-wrap');
    if (dv23) {
      var dv23banner = dv23.querySelector('.dv23-banner'), dv23list = dv23.querySelector('.dv23-list'), dv23rd = dv23.querySelector('.dv23-read');
      var dv23txt = document.documentElement.lang.indexOf('pt') === 0 ? ['Listas novas nascem %s.', 'Guardamos e-mail, listas e itens para operar sua conta (execução de contrato).', 'Analytics %s.', 'Você pode exportar e excluir seus dados a qualquer momento; backups expurgam em 30 dias.', 'privadas', 'públicas', 'só roda se você aceitar (consentimento)', 'roda por padrão'] : ['New lists are born %s.', 'We keep email, lists and items to run your account (contract).', 'Analytics %s.', 'You can export and delete your data at any time; backups purge within 30 days.', 'private', 'public', 'runs only if you accept (consent)', 'runs by default'];
      dvOn(function () { var p = demo.classList.contains('on-defpriv'), a = demo.classList.contains('on-analytics'); dvRead(dv23banner, gd(a ? 'bbad' : 'bok'), ''); dv23list.innerHTML = ''; [[dv23txt[0].replace('%s', dv23txt[p ? 4 : 5]), !p], [dv23txt[1], false], [dv23txt[2].replace('%s', dv23txt[a ? 7 : 6]), a], [dv23txt[3], false]].forEach(function (x) { var li = document.createElement('li'); li.textContent = x[0]; if (x[1]) li.classList.add('is-bad'); dv23list.appendChild(li); }); });
      dv23.querySelector('.dv23-new').addEventListener('click', function () { var p = demo.classList.contains('on-defpriv'); dvRead(dv23rd, gd('new').replace('%s', gd(p ? 'priv' : 'pub')), p ? 'dv-good' : 'dv-bad'); });
      dv23.querySelector('.dv23-del').addEventListener('click', function () { dvRead(dv23rd, gd('deleted'), 'dv-good'); });
      demo._replay = function () {};
    }
    // 24 matrix
    var dv24 = demo.querySelector('.dv24-wrap');
    if (dv24) {
      var dv24cells = dv24.querySelectorAll('.dv24-cell'), dv24rd = dv24.querySelector('.dv24-read');
      function dv24test(c) { var exp = c.getAttribute('data-exp') === '1', r = Number(c.getAttribute('data-r')), o = Number(c.getAttribute('data-o')), rls = demo.classList.contains('on-rls'); var actual = rls ? exp : (o === 1 && r !== 1 ? true : exp); var pass = actual === exp; c.classList.remove('is-pass', 'is-fail'); c.classList.add(pass ? 'is-pass' : 'is-fail'); c.textContent = pass ? '✓' : '✗'; return pass; }
      function dv24sum() { var tested = 0, pass = 0; Array.prototype.forEach.call(dv24cells, function (c) { if (c.classList.contains('is-pass') || c.classList.contains('is-fail')) { tested++; if (c.classList.contains('is-pass')) pass++; } }); if (!tested) { dv24rd.textContent = gd('first'); return; } var fail = tested - pass; dvRead(dv24rd, fail ? gd('fail').replace('%d', fail) : gd('pass').replace('%d', pass), fail ? 'dv-bad' : 'dv-good'); }
      Array.prototype.forEach.call(dv24cells, function (c) { c.addEventListener('click', function () { dv24test(c); dv24sum(); }); });
      dv24.querySelector('.dv24-run').addEventListener('click', function () { Array.prototype.forEach.call(dv24cells, dv24test); dv24sum(); });
      dv24rd.textContent = gd('first'); dvOn(function () { var any = dv24.querySelector('.is-pass, .is-fail'); if (any) { Array.prototype.forEach.call(dv24cells, function (c) { if (c.classList.contains('is-pass') || c.classList.contains('is-fail')) dv24test(c); }); dv24sum(); } }); demo._replay = function () {};
    }

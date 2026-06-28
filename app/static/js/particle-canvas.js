(function () {
  'use strict';

  // ── Shared particle engine ─────────────────────────────────────────────────
  function ParticleNetwork(canvas, opts) {
    var o = Object.assign({
      count: 60,
      color: 'rgba(99,102,241,0.9)',
      lineColor: 'rgba(99,102,241,',
      bg: '#0a1628',
      speed: 0.45,
      lineDistance: 130,
      mouseRadius: 130,
      mouseForce: 0.055,
      minR: 1.2,
      maxR: 2.8
    }, opts);

    var ctx = canvas.getContext('2d');
    var W, H, pts, raf;
    var mx = -9999, my = -9999;

    function resize() {
      var dpr = window.devicePixelRatio || 1;
      var rect = canvas.getBoundingClientRect();
      W = rect.width;
      H = rect.height;
      canvas.width  = W * dpr;
      canvas.height = H * dpr;
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr, dpr);
    }

    function mkPt() {
      return {
        x:  Math.random() * W,
        y:  Math.random() * H,
        vx: (Math.random() - 0.5) * o.speed,
        vy: (Math.random() - 0.5) * o.speed,
        r:  o.minR + Math.random() * (o.maxR - o.minR),
        a:  0.4 + Math.random() * 0.6
      };
    }

    function init() {
      resize();
      pts = Array.from({ length: o.count }, mkPt);
    }

    function tick() {
      ctx.clearRect(0, 0, W, H);

      ctx.fillStyle = o.bg;
      ctx.fillRect(0, 0, W, H);

      for (var i = 0; i < pts.length; i++) {
        var p = pts[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < p.r)     { p.x = p.r;     p.vx *= -1; }
        if (p.x > W - p.r) { p.x = W - p.r; p.vx *= -1; }
        if (p.y < p.r)     { p.y = p.r;     p.vy *= -1; }
        if (p.y > H - p.r) { p.y = H - p.r; p.vy *= -1; }

        var ddx = p.x - mx, ddy = p.y - my;
        var dd  = ddx * ddx + ddy * ddy;
        if (dd < o.mouseRadius * o.mouseRadius) {
          var dist  = Math.sqrt(dd);
          var force = (1 - dist / o.mouseRadius) * o.mouseForce;
          p.x += ddx * force;
          p.y += ddy * force;
        }

        ctx.globalAlpha = p.a;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, 6.2832);
        ctx.fillStyle = o.color;
        ctx.fill();
      }

      ctx.globalAlpha = 1;

      for (var i = 0; i < pts.length; i++) {
        for (var j = i + 1; j < pts.length; j++) {
          var dx = pts[i].x - pts[j].x;
          var dy = pts[i].y - pts[j].y;
          var d  = Math.sqrt(dx * dx + dy * dy);
          if (d < o.lineDistance) {
            ctx.beginPath();
            ctx.moveTo(pts[i].x, pts[i].y);
            ctx.lineTo(pts[j].x, pts[j].y);
            ctx.strokeStyle = o.lineColor + (0.55 * (1 - d / o.lineDistance)) + ')';
            ctx.lineWidth   = 0.8;
            ctx.stroke();
          }
        }
      }

      raf = requestAnimationFrame(tick);
    }

    function onMove(e) {
      var r = canvas.getBoundingClientRect();
      mx = e.clientX - r.left;
      my = e.clientY - r.top;
    }
    function onTouch(e) {
      if (e.touches.length) {
        var r = canvas.getBoundingClientRect();
        mx = e.touches[0].clientX - r.left;
        my = e.touches[0].clientY - r.top;
      }
    }
    function onLeave() { mx = -9999; my = -9999; }

    init();
    tick();

    canvas.addEventListener('mousemove',  onMove);
    canvas.addEventListener('mouseleave', onLeave);
    canvas.addEventListener('touchmove',  onTouch, { passive: true });
    window.addEventListener('resize',     init);

    return { destroy: function () { cancelAnimationFrame(raf); } };
  }

  // ── Hero canvas ────────────────────────────────────────────────────────────
  var heroEl = document.getElementById('hero-canvas');
  if (heroEl) {
    new ParticleNetwork(heroEl, {
      count: 72,
      color: 'rgba(99,102,241,0.92)',
      lineColor: 'rgba(99,102,241,',
      bg: '#080f1e',
      speed: 0.42,
      lineDistance: 135,
      mouseRadius: 140,
      mouseForce: 0.06,
      minR: 1.4,
      maxR: 3.0
    });
  }

  // ── CTA canvas ────────────────────────────────────────────────────────────
  var ctaEl = document.getElementById('cta-canvas');
  if (ctaEl) {
    new ParticleNetwork(ctaEl, {
      count: 44,
      color: 'rgba(6,182,212,0.88)',
      lineColor: 'rgba(6,182,212,',
      bg: '#04111e',
      speed: 0.28,
      lineDistance: 115,
      mouseRadius: 110,
      mouseForce: 0.05,
      minR: 1.0,
      maxR: 2.4
    });
  }

  // ── 3D tilt on feature cards ───────────────────────────────────────────────
  var MAX_ROT = 10;

  document.querySelectorAll('.modern-feature-card').forEach(function (card) {
    var bound = null;

    function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }

    card.addEventListener('mouseenter', function () {
      bound = card.getBoundingClientRect();
      card.style.transition = 'transform 0.08s ease, box-shadow 0.08s ease';
    });

    card.addEventListener('mousemove', function (e) {
      if (!bound) bound = card.getBoundingClientRect();
      var px  = (e.clientX - bound.left)  / bound.width  - 0.5;
      var py  = (e.clientY - bound.top)   / bound.height - 0.5;
      var rX  = clamp(-py * MAX_ROT * 2, -MAX_ROT, MAX_ROT);
      var rY  = clamp( px * MAX_ROT * 2, -MAX_ROT, MAX_ROT);
      card.style.transform =
        'perspective(700px) rotateX(' + rX + 'deg) rotateY(' + rY + 'deg) scale3d(1.04,1.04,1.04)';
      card.style.boxShadow =
        '0 ' + (8 + Math.abs(rX)) + 'px ' + (24 + Math.abs(rY) * 2) + 'px rgba(99,102,241,0.22)';
    });

    card.addEventListener('mouseleave', function () {
      card.style.transition = 'transform 0.45s ease, box-shadow 0.45s ease';
      card.style.transform  = 'perspective(700px) rotateX(0deg) rotateY(0deg) scale3d(1,1,1)';
      card.style.boxShadow  = '';
      bound = null;
    });
  });

})();

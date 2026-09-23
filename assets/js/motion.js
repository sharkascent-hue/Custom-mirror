/* Cut to Size Mirrors & Glass — motion and interaction.
   Pointer tilt, glints, spotlights, magnetic buttons, ripples, number tweens,
   scroll progress. Does nothing when the visitor prefers reduced motion. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var raf = window.requestAnimationFrame.bind(window);

  /* ---------- number tween, shared with the price calculators ---------- */
  window.CTSMTween = function (el, to, format) {
    if (reduce || !el) { el.textContent = format(to); return; }
    var from = el._tweenVal != null ? el._tweenVal : 0;
    el._tweenVal = to;
    if (from === to) { el.textContent = format(to); return; }
    var start = performance.now(), dur = 550;
    cancelAnimationFrame(el._tweenRaf);
    (function step(now) {
      var t = Math.min(1, (now - start) / dur), e = 1 - Math.pow(1 - t, 3);
      el.textContent = format(from + (to - from) * e);
      if (t < 1) el._tweenRaf = raf(step);
    })(start);
    el.classList.remove("bump"); void el.offsetWidth; el.classList.add("bump");
  };
  window.CTSMTweenReset = function (el) { if (el) el._tweenVal = null; };

  /* ---------- scroll progress ---------- */
  var bar = document.querySelector(".scroll-progress");
  if (bar) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) return; ticking = true;
      raf(function () {
        var max = document.documentElement.scrollHeight - innerHeight;
        bar.style.setProperty("--p", max > 0 ? (scrollY / max).toFixed(4) : 0);
        ticking = false;
      });
    };
    addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  /* ---------- stagger siblings in scroll reveals ---------- */
  var groups = new Map();
  document.querySelectorAll(".reveal").forEach(function (el) {
    var i = groups.get(el.parentNode) || 0;
    el.style.setProperty("--stagger", (i % 6) * 80 + "ms");
    groups.set(el.parentNode, i + 1);
  });

  /* ---------- one-off "in view" triggers: steps line, counters, stars ---------- */
  var once = document.querySelectorAll(".steps, [data-count], .tp-score");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target; io.unobserve(el);
        el.classList.add("is-in");
        if (el.dataset.count) {
          var d = +el.dataset.decimals || 0;
          el._tweenVal = 0;
          window.CTSMTween(el, +el.dataset.count, function (n) { return n.toFixed(d); });
        }
      });
    }, { threshold: .35 });
    once.forEach(function (el) { io.observe(el); });
  } else { once.forEach(function (el) { el.classList.add("is-in"); }); }

  /* ---------- button ripple (touch and mouse) ---------- */
  document.addEventListener("pointerdown", function (e) {
    var b = e.target.closest(".btn");
    if (!b || b.disabled || reduce) return;
    var r = b.getBoundingClientRect(), size = Math.max(r.width, r.height) * 2.2;
    var s = document.createElement("span");
    s.className = "ripple";
    s.style.cssText = "width:" + size + "px;height:" + size + "px;left:" + (e.clientX - r.left - size / 2) + "px;top:" + (e.clientY - r.top - size / 2) + "px";
    b.appendChild(s);
    setTimeout(function () { s.remove(); }, 650);
  });

  if (reduce || !fine) return; // everything below follows a mouse

  /* ---------- helper: pointer position inside an element, -0.5 … 0.5 ---------- */
  function rel(e, el) {
    var r = el.getBoundingClientRect();
    return { x: (e.clientX - r.left) / r.width - .5, y: (e.clientY - r.top) / r.height - .5, px: e.clientX - r.left, py: e.clientY - r.top };
  }

  /* ---------- hero: card tilts, mirror drifts the other way, glint follows ---------- */
  var hero = document.querySelector(".hero");
  var stage = document.querySelector("[data-tilt-stage]");
  if (hero && stage) {
    var card = stage.querySelector(".card-glass"), mirror = stage.querySelector(".quote-stage__mirror");
    hero.addEventListener("pointermove", function (e) {
      var p = rel(e, hero);
      card.style.setProperty("--rx", (-p.y * 5).toFixed(2) + "deg");
      card.style.setProperty("--ry", (p.x * 7).toFixed(2) + "deg");
      mirror.style.setProperty("--px", (p.x * -26).toFixed(1) + "px");
      mirror.style.setProperty("--py", (p.y * -18).toFixed(1) + "px");
      var m = rel(e, mirror);
      mirror.style.setProperty("--gx", m.px + "px");
      mirror.style.setProperty("--gy", m.py + "px");
    });
    hero.addEventListener("pointerleave", function () {
      ["--rx", "--ry"].forEach(function (v) { card.style.setProperty(v, "0deg"); });
      ["--px", "--py"].forEach(function (v) { mirror.style.setProperty(v, "0px"); });
    });
  }

  /* ---------- spotlight on cards ---------- */
  document.addEventListener("pointermove", function (e) {
    var el = e.target.closest(".pcard, .pillar, .review, .tp-score, .panel, .ccard, .measure-step");
    if (!el) return;
    var r = el.getBoundingClientRect();
    el.style.setProperty("--mx", e.clientX - r.left + "px");
    el.style.setProperty("--my", e.clientY - r.top + "px");
  }, { passive: true });

  /* ---------- product cards: 3D tilt ---------- */
  document.querySelectorAll(".pcard").forEach(function (c) {
    c.addEventListener("pointermove", function (e) {
      var p = rel(e, c);
      c.classList.add("is-tilting");
      c.style.setProperty("--rx", (-p.y * 8).toFixed(2) + "deg");
      c.style.setProperty("--ry", (p.x * 10).toFixed(2) + "deg");
    });
    c.addEventListener("pointerleave", function () {
      c.classList.remove("is-tilting");
      c.style.setProperty("--rx", "0deg"); c.style.setProperty("--ry", "0deg");
    });
  });

  /* ---------- use-case tiles: background parallax ---------- */
  document.querySelectorAll(".use").forEach(function (t) {
    t.addEventListener("pointermove", function (e) {
      var p = rel(e, t);
      t.style.setProperty("--px", (p.x * -14).toFixed(1) + "px");
      t.style.setProperty("--py", (p.y * -14).toFixed(1) + "px");
    });
    t.addEventListener("pointerleave", function () { t.style.setProperty("--px", "0px"); t.style.setProperty("--py", "0px"); });
  });

  /* ---------- magnetic primary buttons ---------- */
  document.querySelectorAll(".magnetic, .header .btn--cta, .cta-dark .btn--light").forEach(function (b) {
    b.classList.add("magnetic");
    b.addEventListener("pointermove", function (e) {
      var p = rel(e, b);
      b.style.setProperty("--bx", (p.x * 10).toFixed(1) + "px");
      b.style.setProperty("--by", (p.y * 8).toFixed(1) + "px");
    });
    b.addEventListener("pointerleave", function () { b.style.setProperty("--bx", "0px"); b.style.setProperty("--by", "0px"); });
  });

  /* ---------- configurator preview: tilt + glint ---------- */
  var preview = document.querySelector(".preview"), piece = document.querySelector("[data-piece]");
  if (preview && piece) {
    var glint = piece.querySelector(".glint");
    preview.addEventListener("pointermove", function (e) {
      var p = rel(e, preview);
      piece.style.setProperty("--rx", (-p.y * 14).toFixed(2) + "deg");
      piece.style.setProperty("--ry", (p.x * 18).toFixed(2) + "deg");
      if (glint) { var g = rel(e, piece); glint.style.setProperty("--gx", g.px + "px"); glint.style.setProperty("--gy", g.py + "px"); }
    });
    preview.addEventListener("pointerleave", function () { piece.style.setProperty("--rx", "0deg"); piece.style.setProperty("--ry", "0deg"); });
  }
})();

/* Cut to Size Mirrors & Glass — shared behaviour: header, drawer, basket, forms, reveal. */
(function () {
  "use strict";
  var C = window.CTSM;
  document.documentElement.classList.remove("no-js");

  /* ---------- money + basket helpers (shared with configurator.js) ---------- */
  var gbp = new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" });
  var KEY = "ctsm-basket-v1";

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; }
  }
  function write(items) {
    try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) { /* private mode */ }
    updateCount();
  }
  function count() { return read().reduce(function (n, i) { return n + i.qty; }, 0); }
  function updateCount() {
    var n = count();
    document.querySelectorAll("[data-basket-count]").forEach(function (b) {
      b.textContent = n; b.hidden = n === 0;
    });
  }

  window.CTSMBasket = {
    read: read,
    write: write,
    add: function (item) { var items = read(); items.push(item); write(items); },
    gbp: function (n) { return gbp.format(n); },
    incVat: function (n) { return Math.round(n * (1 + C.vatRate) * 100) / 100; }
  };

  /* ---------- header shadow ---------- */
  var header = document.querySelector(".header");
  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  /* ---------- mobile drawer ---------- */
  var drawer = document.getElementById("drawer");
  var opener = document.querySelector("[data-open-drawer]");
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle("is-open", open);
    drawer.setAttribute("aria-hidden", String(!open));
    drawer.inert = !open;
    document.body.classList.toggle("no-scroll", open);
    if (opener) opener.setAttribute("aria-expanded", String(open));
    if (open) drawer.querySelector("button, a").focus(); else if (opener) opener.focus();
  }
  if (drawer) {
    drawer.inert = true;
    if (opener) opener.addEventListener("click", function () { setDrawer(true); });
    drawer.querySelectorAll("[data-close-drawer]").forEach(function (el) { el.addEventListener("click", function () { setDrawer(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && drawer.classList.contains("is-open")) setDrawer(false); });
  }

  /* ---------- reveal on scroll ---------- */
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add("is-in"); }); }

  /* ---------- year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- fitting area chips from config ---------- */
  document.querySelectorAll("[data-fitting-areas]").forEach(function (ul) {
    ul.textContent = "";
    C.fittingAreas.forEach(function (a) { var li = document.createElement("li"); li.textContent = a; ul.appendChild(li); });
  });

  /* ---------- forms (quote / contact / order) ---------- */
  function formToText(form) {
    var lines = [];
    new FormData(form).forEach(function (v, k) {
      if (typeof v === "string" && v.trim() && k !== "_subject") lines.push(k + ": " + v.trim());
    });
    return lines.join("\n");
  }
  window.CTSMSubmit = function (form, extraText) {
    var status = form.querySelector(".form-status");
    var subject = (form.querySelector("[name=_subject]") || {}).value || "Website enquiry";
    var body = formToText(form) + (extraText ? "\n\n" + extraText : "");
    function show(ok, msg) { if (!status) return; status.hidden = false; status.className = "form-status " + (ok ? "ok" : "err"); status.textContent = msg; }

    if (C.formEndpoint) {
      var fd = new FormData(form);
      if (extraText) fd.append("details", extraText);
      return fetch(C.formEndpoint, { method: "POST", body: fd, headers: { Accept: "application/json" } })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          show(true, "Thanks — we've got it and will be in touch within one working day.");
          form.reset();
          return true;
        })
        .catch(function () { show(false, "Sorry, that didn't send. Please call us on " + C.business.phone + " or email " + C.business.email + "."); return false; });
    }
    window.location.href = "mailto:" + C.business.email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    show(true, "Your email app should now open with your details filled in — just press send. If nothing happens, email " + C.business.email + " or call " + C.business.phone + ".");
    return Promise.resolve(true);
  };
  document.querySelectorAll("form[data-enquiry]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      window.CTSMSubmit(form);
    });
  });

  /* ---------- home quick price ---------- */
  var qp = document.querySelector("[data-quick-price]");
  if (qp) {
    var P = C.products, kind = "mirror", lastPrice = 0;
    var w = qp.querySelector("[name=qw]"), h = qp.querySelector("[name=qh]");
    var out = qp.querySelector("[data-qp-out]"), go = qp.querySelector("[data-qp-go]");
    var links = { mirror: go.dataset.mirror, glass: go.dataset.glass, splashback: go.dataset.splashback };
    var fromRate = { mirror: P.mirror.types.silver.perM2 + P.mirror.edging.polished.perM2, glass: P.glass.thickness["6"].perM2, splashback: P.splashback.perM2 };
    var label = { mirror: "6mm silver, polished edge", glass: "6mm toughened, polished edge", splashback: "6mm toughened, any colour" };

    function render() {
      var W = parseFloat(w.value), H = parseFloat(h.value);
      var href = links[kind];
      out.textContent = "";
      if (W > 0 && H > 0) {
        href += "?w=" + W + "&h=" + H;
        var area = (W * H) / 1e6;
        var left = document.createElement("div");
        var right = document.createElement("div"); right.className = "qp__meta";
        if (fromRate[kind]) {
          var price = window.CTSMBasket.incVat(Math.max(area, C.minChargeArea) * fromRate[kind]);
          left.innerHTML = '<div class="qp__price"><span></span><small>inc VAT</small></div>';
          var num = left.firstChild.firstChild;
          if (window.CTSMTween) { num._tweenVal = lastPrice; window.CTSMTween(num, price, window.CTSMBasket.gbp); }
          else num.textContent = window.CTSMBasket.gbp(price);
          lastPrice = price;
        } else {
          lastPrice = 0;
          left.innerHTML = '<div class="qp__hint"><strong>Priced to your colour</strong><br>Get a quote in one working day</div>';
        }
        right.textContent = area.toFixed(2) + " m²";
        right.appendChild(document.createElement("br"));
        right.appendChild(document.createTextNode(label[kind]));
        out.appendChild(left); out.appendChild(right);
      } else {
        lastPrice = 0;
        out.innerHTML = '<span class="qp__hint">Enter your size to see your price</span>';
      }
      go.href = href;
    }
    qp.querySelectorAll("[role=tab]").forEach(function (t) {
      t.addEventListener("click", function () {
        qp.querySelectorAll("[role=tab]").forEach(function (x) { x.setAttribute("aria-selected", "false"); x.tabIndex = -1; });
        t.setAttribute("aria-selected", "true"); t.tabIndex = 0; kind = t.dataset.kind; render();
      });
    });
    [w, h].forEach(function (i) { i.addEventListener("input", render); });
    render();
  }

  updateCount();
})();

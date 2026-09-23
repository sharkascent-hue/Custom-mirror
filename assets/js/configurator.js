/* Cut to Size Mirrors & Glass — product configurator (mirror / glass / splashback).
   Builds the option cards from config.js, keeps a live price and preview. */
(function () {
  "use strict";
  var form = document.querySelector("[data-config]");
  if (!form) return;

  var C = window.CTSM, B = window.CTSMBasket;
  var kind = form.dataset.config;
  var P = C.products[kind];
  var UNIT = { mm: 1, cm: 10, in: 25.4 };

  var state = {
    unit: "mm", w: 0, h: 0, qty: 1,
    type: "silver", thickness: P.defaultThickness || "6", edging: "polished", backing: "none", fixings: "none",
    colour: "", colourHex: "#3f8a74"
  };

  var $ = function (s) { return form.querySelector(s); };
  var wIn = $("[name=width]"), hIn = $("[name=height]");
  var priceEl = document.querySelectorAll("[data-price]"), vatEl = $("[data-vat]"), areaEl = $("[data-area]");
  var linesEl = $("[data-lines]"), sizeMsg = $("[data-size-msg]"), fixMsg = $("[data-fix-msg]");
  var addBtns = document.querySelectorAll("[data-add]"), addedEl = $("[data-added]");
  var piece = document.querySelector("[data-piece]"), dimW = document.querySelector("[data-dim-w]"), dimH = document.querySelector("[data-dim-h]");
  var capArea = document.querySelector("[data-cap-area]"), capDesc = document.querySelector("[data-cap-desc]");
  var barPrice = document.querySelector("[data-bar-price]"), barSub = document.querySelector("[data-bar-sub]");
  var quoteOnly = kind === "splashback" && !P.perM2;

  /* ---------- build option cards ---------- */
  function optionCards(group, entries, extra) {
    var wrap = form.querySelector('[data-opts="' + group + '"]');
    if (!wrap) return;
    wrap.textContent = "";
    Object.keys(entries).forEach(function (key) {
      var o = entries[key], id = group + "-" + key;
      var div = document.createElement("div"); div.className = "opt";
      var input = document.createElement("input");
      input.type = "radio"; input.name = group; input.value = key; input.id = id;
      input.checked = state[group] === key;
      var label = document.createElement("label"); label.htmlFor = id;
      if (extra) extra(label, key, o);
      var name = document.createElement("span"); name.className = "opt__name"; name.textContent = o.label; label.appendChild(name);
      if (o.sub) { var sub = document.createElement("span"); sub.className = "opt__sub"; sub.textContent = o.sub; label.appendChild(sub); }
      var price = priceTag(o);
      if (price) { var pr = document.createElement("span"); pr.className = "opt__price"; pr.textContent = price; label.appendChild(pr); }
      div.appendChild(input); div.appendChild(label); wrap.appendChild(div);
    });
  }
  function priceTag(o) {
    if (o.perM2) return (P.edging && (o === P.edging.polished || o === P.edging.bevel) ? "+" : "") + B.gbp(o.perM2) + " /m²";
    if (o.each) return "+" + B.gbp(o.each);
    return "";
  }

  if (kind === "mirror") {
    optionCards("type", P.types, function (label, key, o) {
      var s = document.createElement("span"); s.className = "opt__swatch"; s.style.background = o.swatch; label.prepend(s);
    });
    optionCards("thickness", P.thickness);
    optionCards("edging", P.edging, function (label, key) {
      var s = document.createElement("span"); s.className = "opt__edge opt__edge--" + key; label.prepend(s);
    });
    optionCards("backing", P.backing);
    optionCards("fixings", P.fixings);
  } else if (kind === "glass") {
    optionCards("thickness", P.thickness);
  }

  /* ---------- prefill from ?w=&h= (mm) ---------- */
  var qs = new URLSearchParams(location.search);
  if (+qs.get("w") > 0) { state.w = +qs.get("w"); wIn.value = state.w; }
  if (+qs.get("h") > 0) { state.h = +qs.get("h"); hIn.value = state.h; }

  /* ---------- events ---------- */
  var cutTimer;
  form.addEventListener("input", function (e) {
    var t = e.target;
    if (t === wIn || t === hIn) {
      var v = parseFloat(t.value);
      state[t === wIn ? "w" : "h"] = v > 0 ? v * UNIT[state.unit] : 0;
      clearTimeout(cutTimer);
      cutTimer = setTimeout(function () { piece.classList.remove("is-cutting"); void piece.offsetWidth; piece.classList.add("is-cutting"); }, 350);
    } else if (t.name === "unit") {
      state.unit = t.value;
      form.querySelectorAll("[data-unit-label]").forEach(function (s) { s.textContent = t.value; });
      wIn.value = state.w ? round(state.w / UNIT[state.unit]) : "";
      hIn.value = state.h ? round(state.h / UNIT[state.unit]) : "";
      wIn.step = hIn.step = state.unit === "mm" ? "1" : "0.1";
    } else if (t.name === "qty") {
      state.qty = Math.max(1, Math.min(99, parseInt(t.value, 10) || 1));
    } else if (t.name === "colour") {
      state.colour = t.value;
    } else if (t.name === "colourPick") {
      state.colourHex = t.value;
    } else if (t.type === "radio" && t.name in state) {
      state[t.name] = t.value;
    }
    update();
  });
  form.querySelectorAll("[data-qty]").forEach(function (b) {
    b.addEventListener("click", function () {
      state.qty = Math.max(1, Math.min(99, state.qty + (+b.dataset.qty)));
      $("[name=qty]").value = state.qty; update();
    });
  });
  form.querySelectorAll(".swatch").forEach(function (s) {
    s.addEventListener("click", function () {
      form.querySelectorAll(".swatch").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
      s.setAttribute("aria-pressed", "true");
      state.colour = s.dataset.name; state.colourHex = s.dataset.hex;
      $("[name=colour]").value = s.dataset.name; $("[name=colourPick]").value = s.dataset.hex;
      update();
    });
  });
  var tubeBtn = $("[data-use-tubes]");
  if (tubeBtn) tubeBtn.addEventListener("click", function () {
    var r = form.querySelector('[name=fixings][value="' + tubeBtn.dataset.value + '"]');
    if (r) { r.checked = true; state.fixings = r.value; update(); }
  });

  function round(n) { return Math.round(n * 10) / 10; }
  function mm(n) { return Math.round(n) + "mm"; }

  /* ---------- constraints ---------- */
  function applyConstraints() {
    if (kind !== "mirror") return;
    var t = P.types[state.type];
    form.querySelectorAll("[name=thickness]").forEach(function (r) {
      r.disabled = t.thickness.indexOf(r.value) < 0;
      if (r.disabled && r.checked) { r.checked = false; }
    });
    if (t.thickness.indexOf(state.thickness) < 0) {
      state.thickness = t.thickness[t.thickness.length - 1];
      form.querySelector('[name=thickness][value="' + state.thickness + '"]').checked = true;
    }
    form.querySelectorAll("[name=edging]").forEach(function (r) { r.disabled = t.edging.indexOf(r.value) < 0; });
    if (t.edging.indexOf(state.edging) < 0) {
      state.edging = t.edging[0];
      form.querySelector('[name=edging][value="' + state.edging + '"]').checked = true;
    }
    var note = $("[data-type-note]");
    if (note) note.hidden = state.type === "silver";
  }

  function limits() {
    if (kind === "mirror") return P.thickness[state.thickness];
    return P;
  }

  /* ---------- main update ---------- */
  function update() {
    applyConstraints();
    var W = state.w, H = state.h, has = W > 0 && H > 0;
    var area = has ? (W * H) / 1e6 : 0;
    var charge = Math.max(area, C.minChargeArea);
    var lim = limits(), long = Math.max(W, H), short = Math.min(W, H);
    var err = "";

    if (has && short < P.minMM) err = "The smallest we cut is " + P.minMM + "mm on each side.";
    else if (has && (long > lim.maxLong || short > lim.maxShort)) {
      err = "That's bigger than one sheet (max " + lim.maxLong + " × " + lim.maxShort + "mm). Call us on " + C.business.phone + " — we can join panels for a seamed option.";
    }
    sizeMsg.hidden = !err; sizeMsg.className = "size-msg err"; sizeMsg.textContent = err;
    [wIn, hIn].forEach(function (i) { i.setAttribute("aria-invalid", String(!!err)); });

    /* price */
    var lines = [], ex = 0, desc = [];
    if (kind === "mirror") {
      var t = P.types[state.type], e = P.edging[state.edging], b = P.backing[state.backing], f = P.fixings[state.fixings];
      ex = charge * (t.perM2 + e.perM2) + b.each + f.each;
      lines.push([t.label + " mirror, " + P.thickness[state.thickness].label, charge * t.perM2]);
      lines.push([e.label, charge * e.perM2]);
      if (b.each) lines.push([b.label, b.each]);
      if (f.each) lines.push([f.label, f.each]);
      desc = [P.thickness[state.thickness].label + " " + t.label.toLowerCase(), e.label.toLowerCase()];
      piece.style.setProperty("--piece", t.swatch);
      piece.classList.toggle("is-bevel", state.edging === "bevel");

      /* fixings advice */
      var tubes = Math.max(1, Math.ceil(area));
      var helper = $("[data-tube-helper]");
      if (helper) {
        helper.hidden = !has;
        var suggest = tubes > 4 ? 4 : tubes;
        $("[data-tube-text]").textContent = has ? (tubes > 4
          ? "At " + area.toFixed(2) + " m² you'll need about " + tubes + " tubes — choose 4 and call us for extra."
          : "We suggest " + tubes + " tube" + (tubes > 1 ? "s" : "") + " of adhesive for " + area.toFixed(2) + " m².") : "";
        tubeBtn.dataset.value = "glue" + suggest;
        tubeBtn.textContent = "Use " + suggest + " tube" + (suggest > 1 ? "s" : "");
        tubeBtn.hidden = state.fixings === "glue" + suggest;
      }
      var fm = "";
      if (state.fixings === "screws" && area > 1) fm = "We don't recommend holes & screws on mirrors over 1 m² — adhesive is safer and stronger for this size." + (state.thickness === "4" ? " If you do need screws, choose 6mm." : "");
      fixMsg.hidden = !fm; fixMsg.textContent = fm;
    } else if (kind === "glass") {
      var th = P.thickness[state.thickness];
      ex = charge * th.perM2;
      lines.push([th.label + " toughened glass, polished edges", ex]);
      desc = [th.label + " toughened", "polished edges"];
    } else {
      piece.style.setProperty("--piece", "linear-gradient(135deg, " + state.colourHex + ", " + state.colourHex + ")");
      desc = ["6mm toughened", state.colour ? state.colour : "your colour"];
      if (P.perM2) { ex = charge * P.perM2; lines.push(["6mm coloured toughened glass", ex]); }
    }
    ex = ex * state.qty;
    if (state.qty > 1) lines.push(["Quantity", "× " + state.qty]);

    var priced = has && !err && !quoteOnly;
    var inc = B.incVat(ex);
    priceEl.forEach(function (p) {
      p.classList.toggle("is-empty", !priced);
      if (priced && window.CTSMTween) { window.CTSMTween(p, inc, B.gbp); return; }
      if (window.CTSMTweenReset) window.CTSMTweenReset(p);
      p.textContent = priced ? B.gbp(inc) : quoteOnly ? (has && !err ? "Quote in 1 working day" : "Enter your size & colour") : "Enter your size to see your price";
    });
    vatEl.textContent = priced ? B.gbp(ex) + " ex VAT · delivery added at checkout" : quoteOnly ? "Every colour is mixed to order, so we price it for you." : "Prices include VAT. Delivery is added at checkout.";
    areaEl.textContent = has ? area.toFixed(2) + " m²" : "—";

    linesEl.textContent = "";
    if (priced) lines.forEach(function (l) {
      var li = document.createElement("li");
      var a = document.createElement("span"); a.textContent = l[0];
      var b2 = document.createElement("span"); b2.textContent = typeof l[1] === "number" ? B.gbp(l[1]) : l[1];
      li.appendChild(a); li.appendChild(b2); linesEl.appendChild(li);
    });

    /* preview */
    if (has) {
      var max = Math.max(W, H);
      piece.style.width = (W / max) * 100 + "%";
      piece.style.height = (H / max) * 100 + "%";
    } else { piece.style.width = "60%"; piece.style.height = "75%"; }
    piece.classList.toggle("is-empty", !has);
    dimW.textContent = has ? mm(W) : "width"; dimH.textContent = has ? mm(H) : "height";
    capArea.textContent = has ? area.toFixed(2) + " m²" : "—";
    capDesc.textContent = desc.join(" · ");

    /* mobile bar */
    if (barPrice) {
      barPrice.textContent = priced ? B.gbp(inc) : quoteOnly && has && !err ? "Free quote" : "Enter your size";
      barSub.textContent = priced ? "inc VAT · " + area.toFixed(2) + " m²" : quoteOnly ? "Priced to your colour" : "Live price as you type";
    }

    var ready = has && !err && (kind !== "splashback" || state.colour.trim());
    addBtns.forEach(function (b) { b.disabled = !ready; });
    state._ex = ex; state._area = area; state._desc = desc;
  }

  /* ---------- add to basket / request quote ---------- */
  function specs() {
    var s = ["Size: " + mm(state.w) + " × " + mm(state.h) + " (" + state._area.toFixed(2) + " m²)"];
    if (kind === "mirror") {
      s.push("Type: " + P.types[state.type].label + ", " + P.thickness[state.thickness].label);
      s.push("Edge: " + P.edging[state.edging].label);
      s.push("Backing: " + P.backing[state.backing].label);
      s.push("Fixings: " + P.fixings[state.fixings].label);
    } else if (kind === "glass") {
      s.push("Glass: " + P.thickness[state.thickness].label + " toughened, polished edges");
    } else {
      s.push("Colour: " + state.colour.trim());
    }
    return s;
  }

  function add() {
    update();
    if (addBtns[0].disabled) { wIn.focus(); return; }
    if (quoteOnly) {
      var q = $("[data-quote-fields]");
      var missing = Array.prototype.find.call(q.querySelectorAll("input[required]"), function (i) { return !i.checkValidity(); });
      if (missing) { missing.reportValidity(); return; }
      window.CTSMSubmit(form, P.title + "\n" + specs().join("\n") + "\nQuantity: " + state.qty);
      return;
    }
    B.add({
      id: Date.now().toString(36), kind: kind, title: P.title,
      specs: specs(), unitEx: Math.round((state._ex / state.qty) * 100) / 100, qty: state.qty,
      swatch: kind === "mirror" ? P.types[state.type].swatch : kind === "glass" ? "linear-gradient(135deg,#e6f4f6,#b8dde2 40%,#eaf7f9 60%,#a6d0d6)" : state.colourHex
    });
    addedEl.hidden = false;
    addedEl.querySelector("[data-added-text]").textContent = "Added to your basket (" + state.qty + ").";
    addedEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }
  addBtns.forEach(function (b) { b.addEventListener("click", add); });
  form.addEventListener("submit", function (e) { e.preventDefault(); }); // Enter in a field shouldn't add to basket

  if (quoteOnly) {
    var q = $("[data-quote-fields]"); if (q) q.hidden = false;
    addBtns.forEach(function (b) { b.querySelector("[data-add-label]").textContent = "Request my quote"; });
  }

  document.body.classList.add("has-price-bar");
  update();
})();

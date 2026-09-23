/* Cut to Size Mirrors & Glass — basket page + order request. */
(function () {
  "use strict";
  var root = document.querySelector("[data-basket]");
  if (!root) return;
  var B = window.CTSMBasket;
  var list = root.querySelector("[data-items]"), totals = root.querySelector("[data-totals]");
  var empty = root.querySelector("[data-empty]"), full = root.querySelectorAll("[data-full]");
  var form = root.querySelector("form");

  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

  function render() {
    var items = B.read();
    empty.hidden = items.length > 0;
    full.forEach(function (f) { f.hidden = items.length === 0; });
    list.textContent = "";
    var ex = 0;
    items.forEach(function (it, idx) {
      ex += it.unitEx * it.qty;
      var row = el("article", "bitem");
      var th = el("div", "bitem__thumb"); th.style.background = it.swatch; row.appendChild(th);
      var mid = el("div"); mid.appendChild(el("h3", null, it.title));
      var ul = el("ul"); it.specs.forEach(function (s) { ul.appendChild(el("li", null, s)); }); mid.appendChild(ul);
      row.appendChild(mid);
      var right = el("div", "bitem__right");
      right.appendChild(el("div", "bitem__price", B.gbp(B.incVat(it.unitEx * it.qty))));
      var q = el("div", "qty");
      var minus = el("button", null, "−"); minus.type = "button"; minus.setAttribute("aria-label", "One fewer");
      var val = el("input"); val.value = it.qty; val.readOnly = true; val.setAttribute("aria-label", "Quantity");
      var plus = el("button", null, "+"); plus.type = "button"; plus.setAttribute("aria-label", "One more");
      minus.onclick = function () { change(idx, -1); }; plus.onclick = function () { change(idx, 1); };
      q.appendChild(minus); q.appendChild(val); q.appendChild(plus); right.appendChild(q);
      var rm = el("button", "linkbtn", "Remove"); rm.type = "button"; rm.onclick = function () { remove(idx); };
      right.appendChild(rm);
      row.appendChild(right);
      list.appendChild(row);
    });
    var inc = B.incVat(ex);
    totals.textContent = "";
    [["Subtotal (ex VAT)", B.gbp(ex)], ["VAT (20%)", B.gbp(inc - ex)], ["Delivery", "Confirmed with your order"], ["Total inc VAT", B.gbp(inc)]].forEach(function (r, i, a) {
      var li = el("li", i === a.length - 1 ? "grand" : null);
      li.appendChild(el("span", null, r[0])); li.appendChild(el("span", null, r[1])); totals.appendChild(li);
    });
  }
  function change(i, d) {
    var items = B.read(); items[i].qty = Math.max(1, Math.min(99, items[i].qty + d)); B.write(items); render();
  }
  function remove(i) { var items = B.read(); items.splice(i, 1); B.write(items); render(); }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var items = B.read(), ex = 0;
    var text = items.map(function (it, n) {
      ex += it.unitEx * it.qty;
      return (n + 1) + ". " + it.title + " × " + it.qty + " — " + B.gbp(B.incVat(it.unitEx * it.qty)) + " inc VAT\n   " + it.specs.join("\n   ");
    }).join("\n\n");
    text = "ORDER\n\n" + text + "\n\nTotal: " + B.gbp(B.incVat(ex)) + " inc VAT (" + B.gbp(ex) + " ex VAT) + delivery";
    window.CTSMSubmit(form, text).then(function (ok) { if (ok && window.CTSM.formEndpoint) { B.write([]); render(); } });
  });

  render();
})();

/* Minimal interactions: reveal on scroll, active nav link, reading progress. */
(function () {
  document.documentElement.classList.add("js");

  // ---- reveal on scroll ----
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && items.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("is-in");
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("is-in"); });
  }

  // ---- active nav link ----
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav__links a"));
  var targets = links.map(function (a) {
    var id = a.getAttribute("href");
    return id && id.charAt(0) === "#" ? document.querySelector(id) : null;
  }).filter(Boolean);

  function syncActive() {
    var pos = window.scrollY + window.innerHeight * 0.3;
    var current = -1;
    targets.forEach(function (el, i) { if (el.offsetTop <= pos) current = i; });
    links.forEach(function (a, i) { a.classList.toggle("is-active", i === current); });
  }

  // ---- reading progress ----
  var bar = document.createElement("div");
  bar.style.cssText = "position:fixed;left:0;top:0;height:2px;width:0;z-index:99;" +
    "background:linear-gradient(90deg,#123a70,#3f7ed4);transition:width .1s linear";
  document.body.appendChild(bar);

  function onScroll() {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + "%";
    syncActive();
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();

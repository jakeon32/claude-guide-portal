/* Claude 연동 가이드 포탈 — 공통 스크립트 */
(function () {
  "use strict";

  // ---- 테마 (기본 라이트) ----
  var KEY = "portal-theme";
  var root = document.documentElement;
  function applyTheme(t) {
    root.setAttribute("data-theme", t === "dark" ? "dark" : "light");
  }
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  applyTheme(saved || "light"); // 저장값 없으면 라이트

  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-theme-toggle]");
    if (!btn) return;
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    applyTheme(next);
    try { localStorage.setItem(KEY, next); } catch (e2) {}
  });

  // ---- 코드 복사 ----
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".code .copy");
    if (!b) return;
    var pre = b.parentElement.querySelector("pre");
    if (!pre) return;
    var txt = pre.innerText;
    navigator.clipboard && navigator.clipboard.writeText(txt).then(function () {
      var old = b.textContent; b.textContent = "복사됨"; b.style.color = "var(--ok)";
      setTimeout(function () { b.textContent = old; b.style.color = ""; }, 1400);
    });
  });

  // ---- 스크롤 진행바 ----
  var bar = document.getElementById("scrollbar");
  if (bar) {
    var onScroll = function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    };
    document.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // ---- TOC 활성 (가이드 페이지) ----
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a[href^='#']"));
  if (tocLinks.length) {
    var targets = tocLinks.map(function (a) {
      return document.getElementById(a.getAttribute("href").slice(1));
    }).filter(Boolean);
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        tocLinks.forEach(function (a) {
          a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id);
        });
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    targets.forEach(function (t) { io.observe(t); });
  }
})();

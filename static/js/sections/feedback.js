(function () {
  "use strict";

  document.querySelectorAll(".fb-slider").forEach(initSlider);

  function initSlider(slider) {
    const track = slider.querySelector(".fb-track");
    const cards = Array.from(track.children);
    const prev = slider.querySelector(".fb-prev");
    const next = slider.querySelector(".fb-next");
    const dotsBox = slider.querySelector(".fb-dots");
    const autoplay = slider.dataset.autoplay === "true";
    const delay = Math.max(1, parseInt(slider.dataset.speed, 10) || 5) * 1000;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let timer = null;
    let dots = [];
    let paused = false;

    const perView = () => parseInt(getComputedStyle(track).getPropertyValue("--per-view"), 10) || 1;
    const step = () => {
      const a = cards[0].getBoundingClientRect();
      const b = cards[1] ? cards[1].getBoundingClientRect() : null;
      return b ? b.left - a.left : a.width;
    };
    const pages = () => Math.max(1, cards.length - perView() + 1);
    const maxScroll = () => track.scrollWidth - track.clientWidth;
    const index = () => Math.min(pages() - 1, Math.round(track.scrollLeft / step()));

    function buildDots() {
      if (!dotsBox) return;
      dotsBox.innerHTML = "";
      dots = [];
      const n = pages();
      if (n < 2) return;
      for (let i = 0; i < n; i++) {
        const d = document.createElement("button");
        d.type = "button";
        d.className = "fb-dot";
        d.setAttribute("role", "tab");
        d.setAttribute("aria-label", "Go to feedback " + (i + 1));
        d.addEventListener("click", () => { goTo(i); restart(); });
        dotsBox.appendChild(d);
        dots.push(d);
      }
      update();
    }

    function update() {
      const i = track.scrollLeft >= maxScroll() - 2 ? pages() - 1 : index();
      dots.forEach((d, k) => {
        d.classList.toggle("active", k === i);
        d.setAttribute("aria-selected", k === i ? "true" : "false");
      });
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= maxScroll() - 2;
      const hide = cards.length <= perView();
      [prev, next].forEach((b) => b && b.parentElement && (b.parentElement.hidden = hide));
    }

    function goTo(i) {
      const n = pages();
      i = (i + n) % n;
      track.scrollTo({ left: i * step(), behavior: reduce ? "auto" : "smooth" });
    }

    function move(dir) {
      const at = track.scrollLeft >= maxScroll() - 2 ? pages() - 1 : index();
      if (dir > 0 && at >= pages() - 1) return goTo(0);
      goTo(Math.max(0, at + dir));
    }

    function start() {
      if (!autoplay || reduce || timer || cards.length <= perView()) return;
      timer = setInterval(() => { if (!paused && !document.hidden) move(1); }, delay);
    }
    function stop() { clearInterval(timer); timer = null; }
    function restart() { stop(); start(); }

    if (prev) prev.addEventListener("click", () => { move(-1); restart(); });
    if (next) next.addEventListener("click", () => { move(1); restart(); });

    let ticking = false;
    track.addEventListener("scroll", () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => { update(); ticking = false; });
    }, { passive: true });

    ["mouseenter", "focusin", "touchstart"].forEach((e) => slider.addEventListener(e, () => (paused = true), { passive: true }));
    ["mouseleave", "focusout"].forEach((e) => slider.addEventListener(e, () => (paused = false)));
    slider.addEventListener("touchend", () => setTimeout(() => (paused = false), 2500), { passive: true });

    track.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") { e.preventDefault(); move(1); restart(); }
      if (e.key === "ArrowLeft") { e.preventDefault(); move(-1); restart(); }
    });

    let lastPer = perView();
    window.addEventListener("resize", () => {
      const p = perView();
      if (p !== lastPer) { lastPer = p; buildDots(); }
      update();
    });

    if ("IntersectionObserver" in window) {
      new IntersectionObserver((es) => es.forEach((en) => (en.isIntersecting ? start() : stop())), { threshold: 0.25 }).observe(slider);
    } else {
      start();
    }

    buildDots();
    update();
  }
})();
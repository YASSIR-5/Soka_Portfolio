/* Soukaina Ait Ali — interactions (progressive enhancement, no dependencies) */
(function () {
  "use strict";
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const doc = document.documentElement;

  /* ---------- header state ---------- */
  const head = document.querySelector(".site-head");
  if (head) {
    const onScroll = () => head.classList.toggle("solid", window.scrollY > 40);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- mobile nav ---------- */
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      doc.classList.toggle("nav-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    });
    nav.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        nav.classList.remove("open");
        doc.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      })
    );
  }

  /* ---------- scroll reveals ---------- */
  const revealables = document.querySelectorAll(".reveal, .clip-wipe, .line-mask");
  if (reduce || !("IntersectionObserver" in window)) {
    revealables.forEach((el) => el.classList.add("in"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            io.unobserve(e.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    revealables.forEach((el) => io.observe(el));
  }

  /* ---------- gentle image expansion when in view ---------- */
  if (!reduce) {
    const figs = document.querySelectorAll("[data-expand] img");
    if (figs.length && "IntersectionObserver" in window) {
      const io2 = new IntersectionObserver(
        (entries) => {
          entries.forEach((e) => {
            e.target.style.setProperty("--zoom", e.isIntersecting ? "1.06" : "1");
          });
        },
        { threshold: 0.25 }
      );
      figs.forEach((f) => io2.observe(f));
    }

    /* ---------- work media scroll-linked scale (--p) ---------- */
    const medias = Array.from(document.querySelectorAll(".work-media[data-drift]"));
    if (medias.length) {
      let ticking = false;
      const update = () => {
        const vh = window.innerHeight;
        medias.forEach((m) => {
          const r = m.getBoundingClientRect();
          // progress 0→1 as the media block travels through the viewport
          const p = Math.min(1, Math.max(0, (vh - r.top) / (vh + r.height)));
          m.style.setProperty("--p", p.toFixed(3));
        });
        ticking = false;
      };
      window.addEventListener(
        "scroll",
        () => {
          if (!ticking) {
            ticking = true;
            requestAnimationFrame(update);
          }
        },
        { passive: true }
      );
      update();
    }
  }

  /* ---------- lightbox for technical drawings ---------- */
  const lb = document.getElementById("lightbox");
  if (lb) {
    const img = lb.querySelector("img");
    const cap = lb.querySelector(".lb-cap");
    let lastFocus = null;
    const close = () => {
      lb.classList.remove("open");
      img.removeAttribute("src");
      if (lastFocus) lastFocus.focus();
      doc.style.overflow = "";
    };
    document.querySelectorAll("[data-zoom]").forEach((el) => {
      el.addEventListener("click", () => {
        lastFocus = el;
        const src = el.getAttribute("data-full") || el.querySelector("img")?.src;
        const alt = el.getAttribute("data-alt") || el.querySelector("img")?.alt || "";
        const c = el.getAttribute("data-caption") || "";
        if (!src) return;
        img.src = src;
        img.alt = alt;
        cap.textContent = c;
        lb.classList.add("open");
        doc.style.overflow = "hidden";
        lb.querySelector(".close").focus();
      });
    });
    lb.querySelector(".close").addEventListener("click", close);
    lb.addEventListener("click", (e) => { if (e.target === lb) close(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && lb.classList.contains("open")) close(); });
  }

  /* ---------- active nav link by pathname ---------- */
  const here = location.pathname.replace(/index\.html$/, "");
  document.querySelectorAll(".nav a").forEach((a) => {
    const p = a.getAttribute("href").replace(/^\./, "").replace(/index\.html$/, "");
    if (p !== "/" && p !== "" && here.endsWith(p)) a.setAttribute("aria-current", "page");
  });
})();

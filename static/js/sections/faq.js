(function () {
  "use strict";

  const list = document.querySelector(".faq-list");
  if (!list) return;

  const items = Array.from(list.querySelectorAll(".faq-item"));
  const single = list.dataset.single === "true";

  function toggle(item, open) {
    item.classList.toggle("open", open);
    item
      .querySelector(".faq-q")
      .setAttribute("aria-expanded", open ? "true" : "false");
  }

  items.forEach((item) => {
    item.querySelector(".faq-q").addEventListener("click", () => {
      const opening = !item.classList.contains("open");
      if (opening && single) {
        items.forEach((other) => {
          if (other !== item) toggle(other, false);
        });
      }
      toggle(item, opening);
    });
  });
})();

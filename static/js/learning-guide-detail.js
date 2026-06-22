(function () {
  "use strict";

  document.addEventListener("click", function (event) {
    var printButton = event.target.closest("[data-print-guide]");
    if (printButton) {
      window.print();
      return;
    }

    var button = event.target.closest("[data-reveal-target]");
    if (!button) return;
    var target = document.getElementById(button.getAttribute("data-reveal-target"));
    if (!target) return;
    var shouldShow = target.hidden || target.style.display === "none";
    target.hidden = !shouldShow;
    target.style.display = shouldShow ? "block" : "none";
    button.textContent = shouldShow
      ? "Ocultar"
      : button.getAttribute("data-label-show") || "Ver";
  });
})();

/*
 * Interacciones de la vista de recurso (CSP-safe, archivo externo):
 *  - Pestañas accesibles del bloque "Practica y evalúa tu aprendizaje"
 *    (patrón ARIA tabs: aria-selected, roving tabindex, flechas/Home/End).
 *  - Expansión de la descripción (Ver más / Ver menos), solo si hay desborde.
 *
 * Se reengancha tras swaps de HTMX (el bloque se refresca vía quiz_status).
 */
(function () {
  "use strict";

  /* ---------- Pestañas ---------- */
  function initTabs(block) {
    if (!block || block.dataset.tabsReady === "1") return;
    block.dataset.tabsReady = "1";

    var tabs = Array.prototype.slice.call(block.querySelectorAll("[data-quiz-tab]"));
    if (!tabs.length) return;

    function panelFor(tab) {
      return block.querySelector('[data-quiz-panel="' + tab.getAttribute("data-quiz-tab") + '"]');
    }

    function select(tab, focus) {
      tabs.forEach(function (t) {
        var selected = t === tab;
        t.setAttribute("aria-selected", selected ? "true" : "false");
        t.setAttribute("tabindex", selected ? "0" : "-1");
        t.classList.toggle("quiz-tab--active", selected);
        var panel = panelFor(t);
        if (panel) {
          panel.hidden = !selected;
          panel.classList.toggle("quiz-panel--active", selected);
        }
      });
      if (focus) tab.focus();
    }

    block.addEventListener("click", function (e) {
      var tab = e.target.closest("[data-quiz-tab]");
      if (tab && block.contains(tab)) select(tab, false);
    });

    block.addEventListener("keydown", function (e) {
      var current = e.target.closest("[data-quiz-tab]");
      if (!current) return;
      var i = tabs.indexOf(current);
      var next = null;
      if (e.key === "ArrowRight" || e.key === "ArrowDown") next = tabs[(i + 1) % tabs.length];
      else if (e.key === "ArrowLeft" || e.key === "ArrowUp") next = tabs[(i - 1 + tabs.length) % tabs.length];
      else if (e.key === "Home") next = tabs[0];
      else if (e.key === "End") next = tabs[tabs.length - 1];
      if (next) {
        e.preventDefault();
        select(next, true);
      }
    });
  }

  /* ---------- Descripción Ver más / Ver menos ---------- */
  function initDesc(wrap) {
    if (!wrap || wrap.dataset.descReady === "1") return;
    var text = wrap.querySelector("[data-resource-desc-text]");
    var toggle = wrap.querySelector("[data-resource-desc-toggle]");
    if (!text || !toggle) return;
    wrap.dataset.descReady = "1";

    // Solo mostrar el botón si el texto realmente se recorta.
    if (text.scrollHeight - text.clientHeight > 2) {
      toggle.hidden = false;
    }

    toggle.addEventListener("click", function () {
      var expanded = wrap.classList.toggle("resource-view__desc--open");
      toggle.setAttribute("aria-expanded", expanded ? "true" : "false");
      toggle.textContent = expanded ? "Ver menos" : "Ver más";
    });
  }

  function initAll(root) {
    (root || document).querySelectorAll("[data-quiz-block]").forEach(initTabs);
    (root || document).querySelectorAll("[data-resource-desc]").forEach(initDesc);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { initAll(document); });
  } else {
    initAll(document);
  }

  // Reenganchar tras swaps de HTMX (p. ej. al refrescar el bloque de niveles).
  document.addEventListener("htmx:afterSwap", function (e) {
    if (e.target && e.target.querySelectorAll) initAll(e.target);
    if (e.target && e.target.id === "quiz-section") initTabs(e.target);
  });
})();

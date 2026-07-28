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

  /* ---------- Bloques pedagógicos de la guía ---------- */
  function normalizedHeading(value) {
    return (value || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .trim();
  }

  function blockKind(heading) {
    var value = normalizedHeading(heading);
    if (value.indexOf("resumen") === 0) return "summary";
    if (value.indexOf("explicacion formal") === 0) return "formal";
    if (value.indexOf("explicacion en palabras simples") === 0) return "plain";
    if (value.indexOf("definiciones") === 0) return "definitions";
    if (value.indexOf("propiedades") === 0) return "properties";
    if (value.indexOf("ejemplo") === 0) return "example";
    if (value.indexOf("procedimiento") === 0) return "procedure";
    if (value.indexOf("errores") === 0) return "errors";
    if (value.indexOf("al terminar") === 0) return "closing";
    return "default";
  }

  function renderInsertedMath(element) {
    if (!element || typeof window.renderMathInElement !== "function") return;
    window.renderMathInElement(element, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "\\[", right: "\\]", display: true },
        { left: "\\(", right: "\\)", display: false },
        { left: "$", right: "$", display: false },
      ],
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
      throwOnError: false,
    });
  }

  function checkpointCard(checkpoint, index) {
    var card = document.createElement("section");
    card.className = "resource-reading-checkpoint";
    card.setAttribute("aria-labelledby", "reading-checkpoint-title-" + index);

    var kicker = document.createElement("p");
    kicker.className = "resource-reading-checkpoint__kicker";
    kicker.textContent = "Comprueba tu avance";

    var title = document.createElement("h3");
    title.className = "resource-reading-checkpoint__question";
    title.id = "reading-checkpoint-title-" + index;
    title.textContent = checkpoint.question;

    var choices = document.createElement("div");
    choices.className = "resource-reading-checkpoint__choices";
    choices.setAttribute("role", "group");
    choices.setAttribute("aria-label", "Alternativas");

    var feedback = document.createElement("div");
    feedback.className = "resource-reading-checkpoint__feedback";
    feedback.setAttribute("aria-live", "polite");
    feedback.hidden = true;

    var feedbackTitle = document.createElement("strong");
    var feedbackText = document.createElement("p");
    var reinforcement = document.createElement("p");
    reinforcement.className = "resource-reading-checkpoint__reinforcement";

    var retry = document.createElement("button");
    retry.type = "button";
    retry.className = "resource-reading-checkpoint__retry";
    retry.textContent = "Intentar nuevamente";
    retry.hidden = true;

    var buttons = checkpoint.choices.map(function (choice, choiceIndex) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "resource-reading-checkpoint__choice";
      button.dataset.correct = choice.is_correct ? "1" : "0";
      button.textContent = String.fromCharCode(65 + choiceIndex) + ". " + choice.text;
      choices.appendChild(button);
      return button;
    });

    function answer(selected) {
      var isCorrect = selected.dataset.correct === "1";
      buttons.forEach(function (button) {
        button.disabled = true;
        if (button.dataset.correct === "1") {
          button.classList.add("resource-reading-checkpoint__choice--correct");
        }
      });
      if (!isCorrect) {
        selected.classList.add("resource-reading-checkpoint__choice--incorrect");
      }
      feedbackTitle.textContent = isCorrect ? "Correcto." : "Revisa tu razonamiento.";
      feedbackText.textContent = checkpoint.explanation;
      reinforcement.textContent = "Refuerzo recomendado: " + checkpoint.reinforcement_section + ".";
      feedback.hidden = false;
      retry.hidden = false;
      renderInsertedMath(feedback);
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () { answer(button); });
    });
    retry.addEventListener("click", function () {
      buttons.forEach(function (button) {
        button.disabled = false;
        button.classList.remove(
          "resource-reading-checkpoint__choice--correct",
          "resource-reading-checkpoint__choice--incorrect",
        );
      });
      feedback.hidden = true;
      retry.hidden = true;
      buttons[0].focus();
    });

    feedback.appendChild(feedbackTitle);
    feedback.appendChild(feedbackText);
    feedback.appendChild(reinforcement);
    card.appendChild(kicker);
    card.appendChild(title);
    card.appendChild(choices);
    card.appendChild(feedback);
    card.appendChild(retry);
    renderInsertedMath(card);
    return card;
  }

  function insertReadingCheckpoints(content, conceptFigure, sections) {
    var data = document.getElementById("resource-reading-checkpoints");
    if (!data) return;
    var checkpoints;
    try {
      checkpoints = JSON.parse(data.textContent || "[]");
    } catch (_error) {
      return;
    }
    if (!Array.isArray(checkpoints) || checkpoints.length !== 3) return;

    function sectionByKind(kind) {
      return content.querySelector(".resource-content-block--" + kind);
    }

    var targets = {
      after_concept_image: conceptFigure || sectionByKind("formal"),
      after_guided_example: sectionByKind("example"),
      after_errors: sectionByKind("errors"),
    };
    checkpoints.forEach(function (checkpoint, index) {
      var target = targets[checkpoint.placement];
      if (!target) return;
      var card = checkpointCard(checkpoint, index + 1);
      target.insertAdjacentElement("afterend", card);
      targets[checkpoint.placement] = card;
      sections.push(card);
    });
  }

  function initContentBlocks(content) {
    if (!content || content.dataset.blocksReady === "1") return;
    var children = Array.prototype.slice.call(content.children);
    var headings = children.filter(function (child) { return child.tagName === "H2"; });
    if (!headings.length) return;
    content.dataset.blocksReady = "1";
    content.classList.add("resource-view__content--enhanced");

    var conceptImage = content.querySelector('img[src*="asset=concept"]');
    var conceptFigure = conceptImage ? conceptImage.parentElement : null;
    if (conceptFigure) {
      conceptFigure.classList.add(
        "resource-editorial-figure",
        "resource-concept-figure",
      );
    }
    var infographicImage = content.querySelector('img[src*="asset=infographic"]');
    var infographicFigure = infographicImage ? infographicImage.parentElement : null;
    if (infographicFigure) {
      infographicFigure.classList.add(
        "resource-editorial-figure",
        "resource-infographic-figure",
      );
    }

    var sections = [];
    headings.forEach(function (heading) {
      var section = document.createElement("section");
      var kind = blockKind(heading.textContent);
      section.className = "resource-content-block resource-content-block--" + kind;
      content.insertBefore(section, heading);
      section.appendChild(heading);
      while (
        section.nextSibling
        && section.nextSibling.tagName !== "H2"
        && !(
          section.nextSibling.nodeType === 1
          && section.nextSibling.classList.contains("resource-editorial-figure")
        )
      ) {
        section.appendChild(section.nextSibling);
      }
      sections.push(section);
    });
    if (conceptFigure) sections.push(conceptFigure);
    if (infographicFigure) sections.push(infographicFigure);
    insertReadingCheckpoints(content, conceptFigure, sections);

    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduceMotion || !("IntersectionObserver" in window)) {
      sections.forEach(function (section) { section.classList.add("is-visible"); });
      return;
    }

    content.classList.add("resource-view__content--motion");
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -8% 0px" });
    sections.forEach(function (section) { observer.observe(section); });
  }

  function initAll(root) {
    (root || document).querySelectorAll("[data-quiz-block]").forEach(initTabs);
    (root || document).querySelectorAll("[data-resource-desc]").forEach(initDesc);
    (root || document).querySelectorAll("[data-resource-content]").forEach(initContentBlocks);
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

/*
 * Reproductor de preguntas a pantalla completa.
 *
 * Las vistas HTMX (quiz_form, quiz_results, quiz_empty, quiz_blocked,
 * quiz_recover_result, topic_exam_form/results) se cargan dentro de
 * #quiz-player-root. Este controlador maneja: apertura/cierre del overlay,
 * navegacion una-pregunta-a-la-vez, progreso, pantalla de revision, foco
 * atrapado, Escape, confirmacion al cerrar y bloqueo de scroll.
 *
 * Todo es CSP-safe (archivo externo, sin eval ni handlers inline).
 */
(function () {
  "use strict";

  var root = document.getElementById("quiz-player-root");
  if (!root) return;

  var lastTrigger = null;
  var statusUrl = null;
  var refreshTargetSelector = "#quiz-section";
  var refreshSwapMode = "outerHTML";

  var FOCUSABLE =
    'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex="0"]';

  function isOpen() {
    return root.classList.contains("quiz-player-root--open");
  }

  function getPlayer() {
    return root.querySelector("[data-quiz-player]");
  }

  function getSlides(player) {
    return Array.prototype.slice.call(player.querySelectorAll("[data-quiz-slide]"));
  }

  function answerIsPresent(input) {
    if (input.type === "radio" || input.type === "checkbox") {
      return input.checked;
    }
    return input.value.trim() !== "";
  }

  function slideIsAnswered(slide) {
    return Array.prototype.slice
      .call(slide.querySelectorAll("[data-quiz-answer]"))
      .some(answerIsPresent);
  }

  function hasAnswers() {
    return Array.prototype.slice
      .call(root.querySelectorAll("[data-quiz-answer]"))
      .some(answerIsPresent);
  }

  /* ---- Apertura / cierre ---- */

  function openPlayer() {
    if (!isOpen()) {
      root.hidden = false;
      root.classList.add("quiz-player-root--open");
      document.body.classList.add("quiz-open");
    }
  }

  function closePlayer() {
    var refreshTarget = statusUrl && document.querySelector(refreshTargetSelector);
    if (refreshTarget && window.htmx) {
      window.htmx.ajax("GET", statusUrl, { target: refreshTargetSelector, swap: refreshSwapMode });
    }
    root.classList.remove("quiz-player-root--open");
    root.hidden = true;
    root.innerHTML = "";
    document.body.classList.remove("quiz-open");
    statusUrl = null;
    if (lastTrigger && document.contains(lastTrigger) && typeof lastTrigger.focus === "function") {
      lastTrigger.focus();
    }
    lastTrigger = null;
  }

  function requestClose() {
    if (getPlayer() && hasAnswers()) {
      if (!window.confirm("¿Salir del cuestionario? Se perderán las respuestas seleccionadas.")) {
        return;
      }
    }
    closePlayer();
  }

  /* ---- Navegacion del reproductor ---- */

  function currentIndex(player) {
    return parseInt(player.getAttribute("data-quiz-index") || "0", 10);
  }

  function render(player) {
    var slides = getSlides(player);
    var review = player.querySelector("[data-quiz-review]");
    var total = slides.length;
    var index = currentIndex(player);
    if (index < 0) index = 0;
    var max = review ? total : total - 1;
    if (index > max) index = max;
    player.setAttribute("data-quiz-index", String(index));

    var onReview = review && index === total;

    slides.forEach(function (slide, i) {
      slide.hidden = i !== index;
    });
    if (review) review.hidden = !onReview;

    // Progreso
    var progress = player.querySelector("[data-quiz-progress]");
    if (progress) {
      progress.textContent = onReview ? "Revisión" : "Pregunta " + (index + 1) + " de " + total;
    }

    // Botones anterior / siguiente
    var prev = player.querySelector("[data-quiz-prev]");
    var next = player.querySelector("[data-quiz-next]");
    if (prev) prev.disabled = index === 0;
    if (next) {
      // En la pantalla de revisión ya no hay "siguiente"
      next.hidden = !!onReview;
    }

    if (onReview) buildReview(player, slides);

    // Foco al inicio del contenido visible
    var active = onReview ? review : slides[index];
    if (active) {
      var heading = active.querySelector("[data-quiz-focus], legend, h3, h2");
      if (heading) {
        if (!heading.hasAttribute("tabindex")) heading.setAttribute("tabindex", "-1");
        heading.focus({ preventScroll: true });
      }
    }
    var stage = player.querySelector("[data-quiz-stage]");
    if (stage) stage.scrollTop = 0;
  }

  function navTo(player, i) {
    player.setAttribute("data-quiz-index", String(i));
    render(player);
  }

  function buildReview(player, slides) {
    var list = player.querySelector("[data-quiz-review-list]");
    if (!list) return;
    list.innerHTML = "";
    var pending = 0;
    slides.forEach(function (slide, i) {
      var answered = slideIsAnswered(slide);
      if (!answered) pending += 1;
      var li = document.createElement("li");
      li.className = "quiz-review__item" + (answered ? " quiz-review__item--done" : " quiz-review__item--pending");
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "quiz-review__jump";
      btn.setAttribute("data-quiz-jump", String(i));
      btn.innerHTML =
        '<span class="quiz-review__num">' + (i + 1) + "</span>" +
        '<span class="quiz-review__state">' + (answered ? "Respondida" : "Pendiente") + "</span>";
      li.appendChild(btn);
      list.appendChild(li);
    });
    var summary = player.querySelector("[data-quiz-review-summary]");
    if (summary) {
      summary.textContent = pending === 0
        ? "Respondiste todas las preguntas."
        : "Te quedan " + pending + " pregunta" + (pending === 1 ? "" : "s") + " sin responder.";
    }
  }

  /* ---- Inicializacion tras cada swap dentro del root ---- */

  function initContent() {
    var holder = root.querySelector("[data-quiz-status-url]");
    statusUrl = holder ? holder.getAttribute("data-quiz-status-url") : statusUrl;
    refreshTargetSelector = (holder && holder.getAttribute("data-quiz-refresh-target")) || "#quiz-section";
    refreshSwapMode = (holder && holder.getAttribute("data-quiz-refresh-swap")) || "outerHTML";

    var player = getPlayer();
    if (player && getSlides(player).length) {
      player.setAttribute("data-quiz-index", "0");
      render(player);
    } else {
      // Resultados / vacío / bloqueado: solo enfocar el cierre
      root.scrollTop = 0;
      var focusable = root.querySelector(FOCUSABLE);
      if (focusable) focusable.focus({ preventScroll: true });
    }
  }

  /* ---- Listeners ---- */

  // Recordar el botón que abrió el reproductor (para restaurar foco)
  document.addEventListener(
    "click",
    function (e) {
      var trigger = e.target.closest('[hx-target="#quiz-player-root"]');
      if (trigger) lastTrigger = trigger;
    },
    true
  );

  // Clicks dentro del overlay: cerrar / navegar / saltar
  root.addEventListener("click", function (e) {
    if (e.target.closest("[data-quiz-close]")) {
      e.preventDefault();
      requestClose();
      return;
    }
    var player = getPlayer();
    if (!player) return;
    if (e.target.closest("[data-quiz-prev]")) {
      e.preventDefault();
      navTo(player, currentIndex(player) - 1);
    } else if (e.target.closest("[data-quiz-next]")) {
      e.preventDefault();
      navTo(player, currentIndex(player) + 1);
    } else {
      var jump = e.target.closest("[data-quiz-jump]");
      if (jump) {
        e.preventDefault();
        navTo(player, parseInt(jump.getAttribute("data-quiz-jump"), 10));
      }
    }
  });

  // Al recalcular respondida/pendiente en vivo, refrescar revisión si está visible
  function refreshReviewForAnswer(e) {
    if (e.target.matches("[data-quiz-answer]")) {
      var player = getPlayer();
      if (player && player.querySelector("[data-quiz-review]") &&
          currentIndex(player) === getSlides(player).length) {
        buildReview(player, getSlides(player));
      }
    }
  }

  root.addEventListener("change", refreshReviewForAnswer);
  root.addEventListener("input", refreshReviewForAnswer);

  // HTMX: cada vez que se inyecta contenido en el root
  document.addEventListener("htmx:afterSwap", function (e) {
    if (e.target !== root) return;
    if (root.children.length === 0) {
      closePlayer();
      return;
    }
    openPlayer();
    initContent();
  });

  // Teclado: Escape cierra, Tab atrapado dentro del overlay
  document.addEventListener("keydown", function (e) {
    if (!isOpen()) return;
    if (e.key === "Escape") {
      e.preventDefault();
      requestClose();
      return;
    }
    if (e.key === "Tab") {
      var focusables = Array.prototype.slice
        .call(root.querySelectorAll(FOCUSABLE))
        .filter(function (el) {
          return el.offsetWidth > 0 || el.offsetHeight > 0 || el.getClientRects().length > 0;
        });
      if (!focusables.length) return;
      var first = focusables[0];
      var last = focusables[focusables.length - 1];
      var active = document.activeElement;
      if (e.shiftKey) {
        if (active === first || !root.contains(active)) {
          last.focus();
          e.preventDefault();
        }
      } else if (active === last || !root.contains(active)) {
        first.focus();
        e.preventDefault();
      }
    }
  });
})();

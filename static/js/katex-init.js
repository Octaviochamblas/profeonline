/*
 * Render de fórmulas matemáticas con KaTeX (auto-render).
 *
 * Escanea el contenido buscando delimitadores LaTeX y los convierte en
 * notación matemática real (superíndices, fracciones, raíces, matrices,
 * integrales, derivadas, etc.). Cubre toda la página y el contenido que
 * HTMX inyecta dinámicamente (incluido el reproductor de preguntas).
 *
 * Delimitadores soportados al redactar contenido/preguntas:
 *   - En línea:  $...$   o  \(...\)        ej.  $x^2$  →  x²
 *   - En bloque: $$...$$ o  \[...\]        ej.  $$\frac{a}{b}$$
 * OJO con el signo $ literal (precios): \$ evita que KaTeX lo confunda con
 * una fórmula, pero NO borra la barra invertida — se ve "\$5", no "$5".
 * Para precios, mejor evitar el símbolo $ y escribir el monto en palabras
 * (ej. "5 pesos") o usar otra unidad.
 *
 * CSP-safe: archivo externo cargado con nonce, sin eval.
 */
(function () {
  "use strict";

  var OPTIONS = {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "\\[", right: "\\]", display: true },
      { left: "\\(", right: "\\)", display: false },
      { left: "$", right: "$", display: false },
    ],
    // No tocar bloques de código ni controles de formulario.
    ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
    // No romper la página entera si una fórmula está mal escrita.
    throwOnError: false,
    macros: {
      "\\wideparen": "\\overset{\\frown}{#1}",
      "\\overarc": "\\overset{\\frown}{#1}",
      "\\overgroup": "\\overset{\\frown}{#1}",
    },
  };

  // KaTeX agrega "struts" internos para alinear sub/superíndices que
  // desbordan 1-2px incluso en fórmulas cortas; eso no debe activar scroll.
  // Solo marcamos como desbordada una fórmula que realmente no cabe.
  var OVERFLOW_THRESHOLD_PX = 6;

  function markOverflowingFormulas(root) {
    if (!root || root.nodeType !== 1) return;
    var nodes = root.querySelectorAll(".katex-display, :not(.katex-display) > .katex");
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var overflows = el.scrollWidth - el.clientWidth > OVERFLOW_THRESHOLD_PX;
      el.classList.toggle("katex-scroll", overflows);
    }
  }

  function renderMath(el) {
    if (el && el.nodeType === 1 && typeof window.renderMathInElement === "function") {
      try {
        window.renderMathInElement(el, OPTIONS);
        markOverflowingFormulas(el);
      } catch (e) {
        /* nunca bloquear el render del resto de la página */
      }
    }
  }

  // Primer render: todo el documento.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      renderMath(document.body);
    });
  } else {
    renderMath(document.body);
  }

  // Contenido inyectado por HTMX (reproductor de preguntas, swaps parciales).
  document.addEventListener("htmx:afterSwap", function (e) {
    renderMath(e.target);
  });
})();

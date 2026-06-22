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
 * Para un signo $ literal (precios), escribir \$.
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
  };

  function renderMath(el) {
    if (el && el.nodeType === 1 && typeof window.renderMathInElement === "function") {
      try {
        window.renderMathInElement(el, OPTIONS);
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

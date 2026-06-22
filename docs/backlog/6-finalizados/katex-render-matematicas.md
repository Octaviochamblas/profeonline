# KaTeX — render de fórmulas matemáticas (LaTeX)

> ⏸️ **CONDICIONAL — pendiente decisión del 🧑 Usuario:** ¿el contenido llevará fórmulas en notación?
> **No** → diferir/descartar. **Sí** → construir. Mitiga el riesgo **A4** de `../../gobernanza/matriz-riesgos.md`.

- **Estado:** ✅ CERRADO 🟢 (2026-06-21) — el 🧑 aprobó: KaTeX en **todo el sitio**.
- **Creado:** 2026-06-03
- **Área:** Contenido / Pedagogía · **Prioridad:** 🟠 P1 (A4)
- **Dueño sugerido:** 🧑 decide → 🏛️ Claude (handoff) → 🔨 Antigravity → 🧩 Codex → 🏛️ Claude

## Diagnóstico (ya hecho, 2026-06-03)
- **No** hay KaTeX ni MathJax instalados (solo se mencionan en docs).
- El contenido de recursos se renderiza como **Markdown** (`apps/core/templatetags/markdown_tags.py`,
  usado en `templates/pages/resource_detail.html`).
- Hoy **no hay fórmulas en notación**: la matemática está descrita en prosa ("fracciones",
  "ecuaciones diferenciales"). Por eso no es un bug que arreglar, sino un **habilitador**.

## Objetivo (una frase)
Permitir escribir fórmulas (`$...$` / `$$...$$`) que se rendericen bien en recursos y en las
explicaciones de `Question`, para un sitio STEM.

## Alcance (lo que SÍ entra, si se aprueba)
- Integrar KaTeX en el render Markdown (extensión server-side **o** auto-render en cliente).
- Cargar assets de KaTeX **self-host** (no CDN) con nonce CSP.
- Aplicar también a las explicaciones de `Question` si corresponde.

## Fuera de alcance
- Editor visual de fórmulas. Migrar el contenido existente.

## Criterios de aceptación
- [ ] `$...$` y `$$...$$` renderizan en recurso y en `Question`.
- [ ] Sin violar la CSP (assets self-host); el `$` literal de texto/precios no se rompe (escape).
- [ ] Barrera verde + `check --deploy`.

## Riesgos / rollback
- Falsos positivos con `$` de texto → manejar escape/delimitadores. Rollback: quitar el include.

## Qué se hizo
**Integración self-host de KaTeX 0.16.11 en toda la página** (rama `feat/katex-render-matematicas`,
🏛️ Claude + 🧑, 2026-06-21).

- **Assets self-host** en `static/vendor/katex/` (`katex.min.css`, `katex.min.js`,
  `contrib/auto-render.min.js` + 60 fuentes en `fonts/`). **Sin CDN** → no rompe la CSP
  (`script-src 'self'`, `font-src 'self'`, `style-src` ya tenía `'unsafe-inline'` para los
  estilos inline de KaTeX).
- **`static/js/katex-init.js`** (CSP-safe, con nonce): `renderMathInElement` sobre
  `document.body` al cargar y sobre `e.target` en cada `htmx:afterSwap` → cubre toda la web
  y el contenido inyectado por HTMX, **incluido el reproductor de preguntas a pantalla
  completa** (`#quiz-player-root`).
- **`templates/base.html`**: `<link>` al CSS en el `<head>` y los tres JS al final del
  `<body>` con `defer` + nonce.
- **Delimitadores:** en línea `$...$` o `\(...\)`; en bloque `$$...$$` o `\[...\]`.
  `throwOnError:false` (una fórmula mal escrita no rompe la página). `ignoredTags` para
  no tocar `code/pre/textarea/option`. Para un `$` literal (precios) escribir `\$`
  (hoy no hay precios con `$` en plantillas → riesgo nulo).
- **Generación IA conectada a KaTeX** (`apps/content/services/ai_generation_service.py::_build_prompt`):
  el prompt compartido (generación inline **y** pipeline de publicación) ahora ordena a la
  IA escribir TODA expresión matemática en LaTeX (`$...$` / `$$...$$`), con ejemplos por tipo
  (potencias, fracciones, raíces, sumatorias, integrales, derivadas, límites, matrices) y la
  regla de escapar `\\` en el JSON. El ejemplo de salida JSON se actualizó para mostrar LaTeX.
  Los bloques con LaTeX se definen como *raw strings* para no chocar con el f-string del prompt.
- **Niveles pedagógicos reestructurados** (mismo prompt): N1 *Comprensión conceptual y funcional*,
  N2 *Dominio procedimental y resolución técnica*, N3 *Transferencia y aplicación en contextos
  reales*, cada uno con su alcance y guía de distractores por nivel.
- **Pipeline reforzado** (`publication_pipeline_service.py`): los otros dos prompts de Gemini
  también saben de LaTeX → el **documento canónico** se redacta en LaTeX y el **auditor** no
  penaliza el LaTeX (y marca como problema la matemática en texto plano). Así ninguna etapa
  del pipeline degrada la notación.
- **Tests:** `apps/core/tests.py::KatexWiringTests` (cableado self-host, sin CDN) +
  `apps/content/tests/test_ai_generation.py` (notación LaTeX + tres niveles) +
  `apps/content/tests/test_publication_pipeline.py::...test_pipeline_prompts_request_latex_notation`
  (documento canónico y auditor piden/aceptan LaTeX). **Suite completa: 403 tests OK.**
- **QA visual:** verificado en navegador que renderizan potencia (`$x^2$`→x²), fracción,
  raíz, integral en bloque y matriz; sin errores de consola ni 404 de fuentes.

### Cómo redactar contenido con fórmulas (para el 🧑 / generación IA)
Escribir LaTeX entre delimitadores en enunciados, alternativas, explicaciones y recursos:
`$x^2$`, `$\frac{a}{b}$`, `$\sqrt{x}$`, `$$\int_0^1 x\,dx$$`, `$\frac{d}{dx}f(x)$`,
`$\begin{pmatrix}1&2\\3&4\end{pmatrix}$`. El contenido viejo en prosa sigue intacto
(KaTeX solo renderiza lo que esté entre delimitadores). La **generación IA nueva ya produce
LaTeX** automáticamente.

**Pendiente aparte (fuera de alcance):** regenerar/migrar el banco existente (~1.500
preguntas en prosa) para que use notación LaTeX. Conviene también, tras la primera
generación real, **verificar que el parser JSON aguanta el escape de `\\`** de la IA y,
si hace falta, endurecerlo.

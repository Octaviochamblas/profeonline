# Guías interactivas — Fase 6: exportación PDF

- **Estado:** 🟢 Auditada y CERRADA por 🏛️ Claude (2026-06-23) — sin errores, merge de PR #84 a `main`
- **Creado:** 2026-06-22 · **Epic padre:** `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`
- **Prioridad:** P2 · **Cartera:** educativa · **Tipo:** producto
- **Dueño:** 🧩 Codex (preflight) → 🔨 Antigravity (construye, rama `feat/guias-fase6-pdf`) → 🧩 Codex (audita) → 🏛️ Claude (cierre)

> **Alcance: descarga PDF de la guía ProfeOnline pública (Fase 3).** La web sigue siendo la versión
> canónica/accesible; el PDF es visual. **No se almacenan PDFs** en el filesystem efímero de Railway.

## Objetivo (una frase)
Permitir descargar una versión PDF de la guía ProfeOnline (con portada y solucionario) generada en el
cliente **después** de que KaTeX haya renderizado las fórmulas, sin almacenar archivos en el servidor.

## Fuentes a leer
- Página de la guía de Fase 3 (`learning_guide_detail`) y `static/js/katex-init.js` (evento de
  render KaTeX, `htmx:afterSwap`).
- `templates/base.html` (carga de JS con nonce + cache-buster; patrón self-host).
- [html2pdf.js](https://github.com/ekoopmans/html2pdf) — **autoalojado** en `static/vendor/`.
  (WeasyPrint server-side descartado por FS efímero.)

## Alcance de construcción
1. **html2pdf.js self-host** en `static/vendor/html2pdf/` (sin CDN, CSP con nonce intacta).
2. **Botón "Descargar PDF"** en la página de la guía: dispara la generación **tras** confirmar que
   KaTeX terminó de renderizar (escuchar el flujo de `katex-init.js`).
3. **Portada ProfeOnline** + contenido + **solucionario** al final; saltos de página razonables (CSS
   print / page-break).
4. JS en archivo externo con nonce + `?v=N`; nada inline. **No** persistir el PDF (descarga directa).

## Criterios de aceptación
- [x] Barrera verde. Sin migraciones (es front).
- [x] El PDF se genera con fórmulas YA renderizadas (no LaTeX crudo), con portada y solucionario.
- [x] Saltos de página correctos; sin almacenamiento server-side.
- [x] CSP intacta; sin JS nuevo y cache-buster actualizado. QA en escritorio y móvil.

## No-objetivos
- Generación server-side de PDF; almacenamiento/caché de PDFs.
- Migración legacy + gate + piloto (Fase 7).

## Riesgos
- Tamaño/tiempo de render con muchas fórmulas (probar con una guía real grande).
- Asegurar que el botón espere el render de KaTeX (si no, salen fórmulas sin renderizar).

## Preflight — 🏛️ Claude (2026-06-23)

Contrastado contra el código real (`learning_guide_detail.html`, `_guide_content_box.html`,
`learning-guide-print.css`, `learning-guide-detail.js`, `katex-init.js`, `base.html`).

### Decisión del usuario: **print nativo** (NO html2pdf.js)
Ya existe un camino impresión→PDF funcionando: el botón `data-print-guide` llama `window.print()`
([learning-guide-detail.js](../../../static/js/learning-guide-detail.js)) y hay un
`@media print` en `learning-guide-print.css`. Se descarta html2pdf.js por: riesgo de exigir
`'unsafe-eval'` (CSP estricta con nonce), rasterización del **tema oscuro** (html2canvas ignora
`@media print`), ~1 MB de JS vendorizado y PDF no seleccionable. El print nativo reutiliza
`@media print`, da texto seleccionable, KaTeX ya renderizado y **cero JS nuevo / cero riesgo CSP**.

### Realidad encontrada (esto es el trabajo real de la fase)
El `learning-guide-print.css` actual está **mayormente obsoleto**: apunta a clases que ya no existen
en el markup (`.guide-section`, `.formula-list`, `.solved-example`, `.choices-list`, `.choice-option`,
`.exercise-item-block`). El markup real usa utilidades Bootstrap + estilos inline. Bugs concretos:

1. **No hay portada:** `@media print { header { display:none } }` **oculta el `<header>`** que contiene
   el logo + badge "Guía Oficial" + el `<h1>` con el título. Hoy el PDF sale **sin título ni logo**.
   → Crear un bloque **portada solo-print** (`.print-cover`: logo + título de la guía + asignatura +
   fecha) con `page-break-after: always`. No reutilizar el header interactivo (lleno de botones).
2. **Texto invisible en papel:** el contenido usa `.text-light` (blanco), `.text-secondary` (gris),
   `.text-teal`, y colores inline (`style="color:#e2e8f0"`). El `body{color:#000!important}` **no**
   gana contra un `color` declarado directamente en el elemento. → Reglas `@media print` que fuercen
   `.text-light,.text-secondary,.text-teal,.text-muted,.badge { color:#000 !important }` y que cubran
   los elementos con color inline (selectores a `.question-card p`, `.question-card li`, etc.).
3. **Fondos oscuros:** `.bg-dark`, `.bg-glass` y fondos inline (`rgba(15,23,42,...)`) → forzar
   `background:transparent !important` / blanco en print.
4. **KaTeX:** las fórmulas (`{{ f.latex }}`, `$...$`) renderizan sincrónicamente al cargar (no hay
   evento async que esperar). Solo asegurar que hereden `color:#000` en print (ver punto 2). El
   `katex.min.css` se carga sin `media`, así que aplica también a print.
5. **Doble solucionario:** existen DOS. (a) el del `_guide_content_box.html` (tabla
   `guide.structured_content.answer_key`, el solucionario propio de la guía); (b) el
   `print-solution-block` de `learning_guide_detail.html` (respuestas del banco visible, grid 3-col,
   `page-break-before: always`). → **Decidir y dejar uno claro**: recomendado conservar el del banco
   (`print-solution-block`) como solucionario imprimible y que el `answer_key` de la guía también
   imprima dentro del cuerpo; o consolidar. No deben verse duplicados/confusos.
6. **Saltos de página:** agregar `page-break-inside: avoid` a `.item-block` (contenedor por ítem del
   detalle) — hoy solo lo tiene `.question-card`.

### Alcance de construcción (afinado)
1. **Reescribir `learning-guide-print.css`** contra el markup real: ocultar `.no-print`/controles,
   forzar tema claro (texto negro venciendo clases Bootstrap + inline), fondos transparentes, bordes
   legibles, `page-break-inside: avoid` en `.item-block`/`.question-card`/cajas del content-box.
2. **Portada solo-print** (`.print-cover`) con logo + título + asignatura + fecha; `page-break-after`.
3. **Relabelar el botón** a "Descargar PDF" (sigue siendo `data-print-guide` → `window.print()`, sin JS
   nuevo) + microcopy "Elige 'Guardar como PDF' en el diálogo".
4. **Resolver el doble solucionario** (punto 5).
5. **Cache-buster:** subir `?v=` del CSS modificado (hoy `?v=2`).

### Criterios de aceptación
- [x] Barrera verde. **Sin migraciones** (solo front: CSS + template + label).
- [x] El PDF (vía print) sale con **portada** (logo+título), cuerpo legible en **tema claro**, fórmulas
  KaTeX **en negro** y **un** solucionario claro.
- [x] Todo `.no-print`/controles/evaluaciones ocultos; saltos de página razonables; sin texto gris/blanco
  invisible.
- [x] **CSP intacta** (no se agrega JS ni inline; solo CSS). Cache-buster actualizado.
- [x] QA en print-preview de **escritorio y móvil** (320/360/390) con una guía real con varias fórmulas.

### No-objetivos / Riesgos
- Sin html2pdf, sin generación/almacenamiento server-side de PDF (descartados).
- Riesgo: estilos inline con alta especificidad → usar `!important` en selectores a los elementos
  reales, no solo en `body`. Probar con una guía grande (muchas fórmulas) por tiempos/paginación.

**Veredicto: Listo para construir** en `feat/guias-fase6-pdf` (🔨 Antigravity → 🧩 Codex audita →
🏛️ Claude cierra). Tarjeta movida a `backlog/3-construccion/`.

## Construcción — 🧩 Codex (2026-06-23)

- Reescrito `learning-guide-print.css` contra las clases y estilos inline reales. En impresión se
  resetean contenedores globales, fondos oscuros, sombras y colores Bootstrap; KaTeX hereda negro.
- Agregada portada solo-print con logo, título, asignatura, tema y fecha; A4 con márgenes definidos.
- Botón relabelado a **Descargar PDF** con microcopy de “Guardar como PDF”; conserva
  `data-print-guide` y `window.print()`. No se agregó JS, vendor, CDN ni persistencia server-side.
- **Decisión del solucionario:** el `answer_key` sigue visible en pantalla, pero se oculta en print.
  Al final del PDF hay un único bloque “Solucionario”, con secciones “Ejercicios de la guía” y
  “Banco práctico”; así no se duplica ni se confunden sus fuentes.
- Agregados saltos/guards para portada, ítems, preguntas y soluciones. Se ocultan navegación,
  evaluaciones, formularios, CTA, footer, overlay y WhatsApp flotante.
- Cache-buster del CSS actualizado de `?v=2` a `?v=3`; regresión de template añadida.

### Evidencia

- QA con guía local realista: 3 fórmulas principales y 90 nodos KaTeX renderizados.
- Chrome print nativo/headless → PDF **A4 de 7 páginas**, portada y solucionario completos, texto
  seleccionable, sin página final vacía, CTA, WhatsApp ni controles.
- Responsive 320/360/390 px: `scrollWidth == viewport`, sin overflow; botón/microcopy apilados.
- `manage.py test` → **511 OK, 1 skip** en 836,877 s.
- `check --deploy` exit 0 con 7 warnings locales conocidos.
- `makemigrations --check --dry-run` → `No changes detected`.
- `pre-commit run --all-files` y `git diff --check` verdes.

**Estado:** construcción terminada; pasa a auditoría independiente. No mergear desde esta etapa.

## Auditoría independiente y cierre — 🏛️ Claude (2026-06-23)

Auditor distinto al builder (🧩 Codex). Fase solo-front (CSS + template + label).
**Verdicto: sin errores que corregir.** La implementación cubre cada punto del preflight.

### Verificado contra el markup real ✅
- **Decisión respetada:** print nativo (`window.print()`); **sin JS nuevo** ni dependencias; CSP intacta.
  El test fija la decisión con `assertNotContains("html2pdf")`.
- **Bug de texto invisible resuelto correctamente:** `.guide-container * { color:#000 !important }` —
  un `!important` de hoja de estilos vence al `color` inline sin `!important` (era el riesgo clave del
  preflight). Fondos cubiertos por `[class*="bg-"]`/`[style*="background"]`.
- **Portada solo-print** (`.print-cover`, A4, `page-break-after`) con logo+título+asignatura+fecha;
  `aria-hidden="true"` + `alt=""` (a11y correcta: el título real sigue en el header para pantalla/SR).
  El header interactivo se oculta en print.
- **Doble solucionario consolidado:** `.screen-answer-key` oculto en print; el `print-solution-block`
  muestra "Ejercicios de la guía" (`answer_key`) + "Banco práctico" una sola vez.
- **Saltos de página** (`page-break-inside: avoid`) en `.item-block`/`.question-card`/cajas del
  content-box; KaTeX forzado a negro; cache-buster `?v=2 → ?v=3`.
- Test `test_learning_guide_print` significativo (verifica portada, label, hint, solucionario, `?v=3`,
  ausencia de html2pdf).

### Barrera (independiente)
- **CI Linux `test (3.12)` verde (511 OK, 1 skip)** — barrera real del repo.
- **Sin migraciones** (front-only); pre-commit verde. QA del builder: PDF A4 real de 7 páginas +
  móviles 320/360/390 sin overflow.
- Squash-merge de PR **#84** a `main` (`22d3d7d`); `audit:aprobado` aplicado. Tarjeta a
  `backlog/6-finalizados/`. **Siguiente: Fase 7 (migración legacy + gate de activación + piloto).**

### Observación menor (no bloqueante)
- `@media print { form { display:none } }` es amplio, pero inocuo: todas las forms del detalle son
  interactivas y ya están en secciones `.no-print`.

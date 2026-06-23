# Guías interactivas — Fase 6: exportación PDF

- **Estado:** 🟢 Preflight resuelto por 🏛️ Claude (2026-06-23) — Ready para construir (🔨 Antigravity)
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
- [ ] Barrera verde. Sin migraciones (es front).
- [ ] El PDF se genera con fórmulas YA renderizadas (no LaTeX crudo), con portada y solucionario.
- [ ] Saltos de página correctos; sin almacenamiento server-side.
- [ ] CSP intacta (vendor self-host + nonce); cache-buster en assets nuevos. QA en escritorio y móvil.

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
- [ ] Barrera verde. **Sin migraciones** (solo front: CSS + template + label).
- [ ] El PDF (vía print) sale con **portada** (logo+título), cuerpo legible en **tema claro**, fórmulas
  KaTeX **en negro** y **un** solucionario claro.
- [ ] Todo `.no-print`/controles/evaluaciones ocultos; saltos de página razonables; sin texto gris/blanco
  invisible.
- [ ] **CSP intacta** (no se agrega JS ni inline; solo CSS). Cache-buster actualizado.
- [ ] QA en print-preview de **escritorio y móvil** (320/360/390) con una guía real con varias fórmulas.

### No-objetivos / Riesgos
- Sin html2pdf, sin generación/almacenamiento server-side de PDF (descartados).
- Riesgo: estilos inline con alta especificidad → usar `!important` en selectores a los elementos
  reales, no solo en `body`. Probar con una guía grande (muchas fórmulas) por tiempos/paginación.

**Veredicto: Listo para construir** en `feat/guias-fase6-pdf` (🔨 Antigravity → 🧩 Codex audita →
🏛️ Claude cierra). Tarjeta movida a `backlog/3-construccion/`.

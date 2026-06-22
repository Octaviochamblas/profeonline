# Guías interactivas — Fase 6: exportación PDF

- **Estado:** 🟡 Handoff de arquitectura (afinar en preflight)
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

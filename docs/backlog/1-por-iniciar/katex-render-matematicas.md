# KaTeX — render de fórmulas matemáticas (LaTeX)

> ⏸️ **CONDICIONAL — pendiente decisión del 🧑 Usuario:** ¿el contenido llevará fórmulas en notación?
> **No** → diferir/descartar. **Sí** → construir. Mitiga el riesgo **A4** de `../../gobernanza/matriz-riesgos.md`.

- **Estado:** Por iniciar (bloqueado por decisión de contenido)
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
_(Completar al finalizar.)_

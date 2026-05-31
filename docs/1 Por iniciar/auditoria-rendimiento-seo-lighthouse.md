# Auditoría real de rendimiento y SEO (Lighthouse / PageSpeed)

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Auditoría
- **Prioridad:** 🔴 Alta (da la línea base objetiva antes de tocar diseño)

## Problema / Objetivo

La auditoría de Core Web Vitals de 2026-05 quedó como **documento teórico, sin medición real**
(ver `docs/3 Finalizados/Auditorías-2026-05-30/auditoria-rendimiento-core-web-vitals.md`,
hallazgos PEND-008). No tenemos una línea base de LCP/CLS/INP ni un puntaje Lighthouse.
Sin números reales no podemos priorizar ni demostrar mejoras.

Objetivo: **medir el estado real** de rendimiento y SEO técnico en las páginas clave y dejar
un registro reproducible que sirva de punto de partida para el resto del trabajo.

## Diagnóstico inicial (sospechas a confirmar con datos)

Basado en la revisión del código actual:

1. **Google Fonts externo (render-blocking).** En `templates/base.html` se carga `Outfit`
   con 6 pesos (300–800) desde `fonts.googleapis.com`. Hay `preconnect`, pero traer 6 pesos
   es caro. Probable mejora: self-host + `font-display: swap`, o reducir a 3 pesos
   (400/600/700).
2. **CSS monolítico.** `static/css/estilos.css` tiene ~2.187 líneas en un solo archivo,
   versionado a mano con `?v=6`. Se carga completo en todas las páginas. Evaluar critical CSS
   o, al menos, confirmar que se sirve comprimido y cacheado.
3. **JS global innecesario.** `enhanced-select.js` se carga con `defer` en **todas** las
   páginas (PEND también lo señalaba), aunque solo hace falta donde hay `<select>`.
4. **Imagen OG en SVG.** `static/img/og-default.svg`: **muchas redes sociales no renderizan
   SVG** en `og:image` (WhatsApp, Facebook, X piden PNG/JPG ≥1200×630). Esto degrada cómo se
   ve el sitio al compartirlo — relevante para un negocio que se difunde por WhatsApp.
5. **Video YouTube.** Ya está con `loading="lazy"` y `youtube-nocookie` (resuelto antes).
   Confirmar que no genera CLS (tiene `aspect-ratio` vía `.video-container`).
6. **Consultas N+1.** Revisar que los listados (`home`, `resource_list`, `subject_detail`)
   usen `select_related`/`prefetch_related` para subject/levels/area.

## Ruta de trabajo

### Fase 1 — Preparar el entorno de medición
- Levantar el sitio con `collectstatic` aplicado (para medir estáticos como en producción).
- Cargar datos semilla representativos (`seed_math_resources`) para que los listados tengan
  volumen real.
- Definir la lista de URLs a auditar: `home`, `/recursos/` (con y sin filtro),
  `resource_detail` (con video + adjunto), `subject_detail`, `level_detail`, login, registro.

### Fase 2 — Medición
- Correr **Lighthouse** (Chrome DevTools o CLI) en mobile y desktop para cada URL.
- Registrar las 4 categorías: Performance, Accessibility, Best Practices, SEO.
- Anotar métricas crudas: LCP, CLS, INP/TBT, TTFB, peso CSS/JS, nº de requests.
- Cuando exista dominio público, repetir con **PageSpeed Insights** (datos de campo CrUX).

### Fase 3 — Análisis y priorización
- Volcar hallazgos en la tabla de abajo (ID, página, métrica, problema, fix, esfuerzo).
- Separar "quick wins" (fuentes, OG en PNG, defer condicional de JS) de cambios mayores.

### Fase 4 — Aplicar quick wins y re-medir
- Implementar las mejoras de bajo esfuerzo / alto impacto.
- Re-correr Lighthouse y comparar contra la línea base.

## Checklist de hallazgos

| ID | Página | Métrica | Problema | Recomendación | Esfuerzo | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| PERF-A | (todas) | LCP/peso | 6 pesos de Google Fonts externos | Self-host o reducir a 3 pesos + `font-display: swap` | M | Pendiente |
| PERF-B | (todas) | Best Practices/SEO | `og:image` en SVG no renderiza en redes | Generar PNG 1200×630 | S | Pendiente |
| PERF-C | (todas) | TBT | `enhanced-select.js` global | Cargar solo en páginas con `<select>` | S | Pendiente |
| PERF-D | (todas) | LCP | CSS monolítico de ~2.2k líneas | Confirmar gzip/brotli + cache; evaluar critical CSS | M | Pendiente |

## Criterios de aceptación

- Existe un registro con puntajes Lighthouse mobile+desktop de todas las páginas clave.
- LCP, CLS e INP están medidos y documentados (línea base).
- Los quick wins identificados están aplicados y re-medidos.
- Estáticos confirmados como comprimidos y cacheables en producción (WhiteNoise).

## Notas / Consideraciones

- No reescribir el documento viejo de CWV; este lo **reemplaza con datos reales**.
- Coordinar con el documento de accesibilidad (`auditoria-accesibilidad-axe.md`): Lighthouse
  da un puntaje a11y superficial, pero axe es la herramienta seria.

---

## Qué se hizo
_(Completar al finalizar, antes de mover a "3 Finalizados".)_

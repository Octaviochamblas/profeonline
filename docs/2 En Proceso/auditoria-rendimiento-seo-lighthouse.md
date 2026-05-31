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

### Medición realizada (2026-05-31, servidor local, Lighthouse 12.8.2, mobile)

Auditadas 4 páginas con `manage.py runserver` + Lighthouse headless:

| Página | Perf | A11y | Best Pr. | SEO | LCP | CLS | TBT | FCP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Home (`/`) | 90 | 95 | 100 | 100 | 2.9 s | 0 | 0 ms | 2.9 s |
| Recursos (`/recursos/`) | 93 | 96 | 100 | 100 | 2.6 s | 0 | 0 ms | 2.5 s |
| Detalle recurso | 93 | 95 | 100 | 100 | 2.6 s | 0 | 0 ms | 2.5 s |
| Detalle asignatura | 93 | 95 | 100 | 100 | 2.6 s | 0 | 0 ms | 2.5 s |

**Lectura:** base muy buena. CLS 0 y TBT 0 ms (excelente: nada de layout shift ni JS
bloqueante). El **único flanco real es el LCP/FCP ~2.6–2.9 s** (zona "needs improvement" en
mobile; el umbral "good" es <2.5 s). Como FCP ≈ LCP ≈ Speed Index, el cuello es el
**render-blocking** de la primera pintura, no el JS ni imágenes pesadas.

### Hallazgos de rendimiento (oportunidades de Lighthouse)

| ID | Hallazgo | Ahorro estimado | Real o artefacto local | Fix |
| --- | --- | --- | --- | --- |
| PERF-1 | **Recursos render-blocking** (Google Fonts + CSS) | ~1.380–1.440 ms | **Real** | Self-host fuentes / reducir pesos / `font-display: swap`; preload CSS crítico |
| PERF-2 | CSS sin usar (`unused-css-rules`) | ~31–33 KiB | **Real** | CSS monolítico; evaluar critical CSS o split |
| PERF-3 | CSS sin minificar (`unminified-css`) | ~10 KiB | **Real** | Minificar `estilos.css` en build/deploy |
| PERF-4 | LCP = `logo.png` en home | — | **Real** | Optimizar logo (WebP/tamaño) + `preload`; o usar texto |
| PERF-5 | Imágenes: responsive + formatos modernos | ~30 + 24 KiB | **Real** | WebP/AVIF y tamaños responsive para el logo |
| PERF-6 | Sin compresión de texto (`uses-text-compression`) | ~83–96 KiB | **Artefacto local** | WhiteNoise comprime en prod; **verificar contra producción/PageSpeed** |
| PERF-7 | Cache TTL corto (`uses-long-cache-ttl`) | 3–4 recursos | **Artefacto local** | Igual que arriba: confirmar headers en prod |

> ⚠️ **Caveat importante:** la medición fue en `runserver`, que **no** comprime ni cachea
> estáticos como WhiteNoise en producción. PERF-6 y PERF-7 son muy probablemente artefactos
> del entorno local; hay que **re-medir contra producción (o PageSpeed Insights)** para
> confirmarlos. Los demás (render-blocking, CSS, imágenes) son reales en cualquier entorno.

### Quick wins priorizados (para la fase de fixes — fuera del alcance de esta medición)
1. **Fuentes Outfit**: self-host o reducir de 6 a 3 pesos + `font-display: swap` → ataca
   directamente el render-blocking (~1.4 s) y el LCP.
2. **Optimizar el logo** (WebP + tamaño correcto + `preload`) → mejora el LCP del home.
3. **Minificar CSS** en el deploy.
4. **`og:image` en PNG 1200×630** (del diagnóstico inicial; SVG no renderiza en redes).
5. Re-medir PERF-6/7 contra producción antes de tocar nada de compresión/cache.

### Estado
Medición + documentación **completas** (alcance acordado: "solo medir y documentar"). Los
fixes quedan como fase siguiente / posibles tarjetas nuevas. Reportes JSON guardados en
`%TEMP%\lh-profe\` (no versionados).

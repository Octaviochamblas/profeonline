# Auditoria de Rendimiento y Core Web Vitals

Fecha de creacion: 2026-05-24
Estado: pendiente de ejecucion
Objetivo: mejorar velocidad percibida, estabilidad visual, carga de recursos y preparacion para SEO tecnico en produccion.

## Alcance recomendado

- Home.
- `/recursos/` con y sin filtros.
- Detalle de recurso con video, Markdown y archivo adjunto.
- `/asignaturas/` y detalle de asignatura.
- `/niveles/` y detalle de nivel.
- Login y registro.
- Static files generados con `collectstatic`.

## Metricas a revisar

- LCP: Largest Contentful Paint.
- CLS: Cumulative Layout Shift.
- INP: Interaction to Next Paint.
- TTFB: Time to First Byte.
- Peso total de CSS/JS.
- Numero de requests.
- Cache de estaticos.
- Tiempo de render inicial en mobile.

## Pasos de auditoria

1. Ejecutar medicion local.
   - Levantar servidor local.
   - Probar paginas clave con Lighthouse.
   - Capturar resultados mobile y desktop.

2. Revisar estaticos.
   - Confirmar que `collectstatic` genera archivos correctamente.
   - Confirmar WhiteNoise y storage comprimido en produccion.
   - Revisar peso de `static/css/estilos.css`.
   - Revisar peso de `static/js/htmx.min.js` y `static/js/enhanced-select.js`.

3. Revisar fuentes.
   - Validar impacto de Google Fonts.
   - Considerar self-host o fallback si hay penalizacion fuerte.
   - Confirmar `font-display` segun estrategia.

4. Revisar imagenes y favicon/OG.
   - Confirmar dimensiones estables.
   - Evitar layout shift.
   - Evaluar si `og-default.svg` es suficiente para compartir.

5. Revisar videos.
   - Confirmar que el iframe de YouTube no bloquea render innecesariamente.
   - Evaluar lazy loading del iframe.
   - Agregar dimensiones/aspect-ratio por CSS.

6. Revisar consultas.
   - Listados con `select_related`/`prefetch_related`.
   - Sitemap con entidades publicas.
   - Recursos relacionados en detalle.
   - Busqueda y filtros.

7. Revisar cache.
   - Cache HTTP para estaticos.
   - Cache de sitemap si hace falta.
   - Cache del rate limit del webhook.

## Herramientas sugeridas

- Lighthouse.
- PageSpeed Insights cuando exista dominio publico.
- Playwright con trazas.
- Django Debug Toolbar en local si se decide instalar solo para desarrollo.
- DevTools Network y Performance.

## Checklist de hallazgos

| ID | Pagina/recurso | Metrica afectada | Problema | Recomendacion | Estado | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| PERF-001 |  |  |  |  | Pendiente |  |

## Recomendaciones iniciales probables

- Agregar `loading="lazy"` y `title` al iframe de YouTube.
- Revisar si Google Fonts debe quedar local para produccion.
- Medir si `enhanced-select.js` debe cargarse solo en paginas con selects.
- Verificar que tablas y cards no provoquen CLS.
- Mantener imagenes con dimensiones o `aspect-ratio`.

## Criterios de aceptacion

- Lighthouse mobile sin problemas criticos de rendimiento.
- No hay layout shift visible en home, recursos y detalle.
- Estaticos se sirven comprimidos y cacheables en produccion.
- Videos no bloquean innecesariamente la primera carga.
- Las consultas principales no crecen de forma explosiva con datos semilla.

## Registro de cambios aplicados

| Fecha | Cambio | Archivo(s) | Validacion | Commit |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

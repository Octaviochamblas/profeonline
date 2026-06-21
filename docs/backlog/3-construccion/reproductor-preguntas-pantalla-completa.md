# Reproductor de preguntas a pantalla completa

- **Estado:** Por iniciar
- **Creado:** 2026-06-21
- **Prioridad:** P1  ·  **Cartera:** producto / educativa
- **Tipo:** producto
- **Dueño sugerido:** 🏛️ Claude

> Una tarjeta está **Ready** (lista para construir) solo si todos los campos de abajo están
> completos. Ver `docs/gobernanza/proceso-multiagente.md` §3.

## Objetivo (una frase)
Reemplazar los cuestionarios verticales (que en móvil se ven apretados y se mezclan con el
contenido de fondo) por un **panel interno a pantalla completa** que muestre una pregunta a la vez
con navegación `Anterior`/`Siguiente`, mejorando la experiencia de responder tanto en celular
como en PC.

## Fuentes a leer (rutas concretas)
- `templates/pages/resource_detail.html` — barra de acciones + `{% include "includes/quiz_section.html" %}`.
- `templates/includes/quiz_section.html` — botones HTMX `Practicar`/`Evaluación` (`hx-get` a `quiz_start`),
  contenedor de destino `#quiz-area-{{ level }}`.
- `templates/includes/quiz_form.html` — formulario actual (todas las preguntas en un solo `<form>`,
  `hx-post` a `quiz_submit`).
- `templates/includes/quiz_results.html` — pantalla de resultados (botones HTMX que apuntan a
  `#quiz-area-{{ level }}` y `#quiz-section`).
- `templates/includes/quiz_empty.html`, `quiz_blocked.html` — estados vacío/bloqueado.
- `templates/includes/topic_exam_section.html`, `topic_exam_form.html`, `topic_exam_empty.html` —
  evaluación final del tema (mismo patrón, también debe entrar al reproductor).
- `apps/content/views/evaluation_views.py` — `quiz_start` / `quiz_submit` / `quiz_status`
  (sesión `quiz_{pk}_{level}_{mode}`, orden aleatorio guardado, reglas de puntuación).
- `templates/base.html` — handlers inline de `data-quiz-cancel` / `data-quiz-report-toggle`,
  botón flotante `.whatsapp-float`, bloque `{% block extra_js %}`.
- `static/css/estilos.css` (zona `.quiz-*`, ~líneas 2555+) + tokens (`--primary #0f766e`, radios, etc.);
  recordar cache-buster `?v=N` (actual `?v=29`).

## Propuesta
- **Contenedor global `#quiz-player-root`** fuera de la columna estrecha del contenido (p. ej. en
  `base.html`), que actúe como overlay `position: fixed; inset: 0` a pantalla completa en móvil y PC.
- Las vistas HTMX existentes (`quiz_form`, `quiz_results`, `quiz_empty`, `quiz_blocked`,
  `topic_exam_form`) se **cargan dentro de ese contenedor**, manteniendo URLs, modelos, sesiones y
  reglas de puntuación actuales. **Sin nuevos endpoints, migraciones ni dependencias.**
- **Todas las preguntas en el mismo `<form>`**, ocultando las inactivas por CSS/JS; así las
  respuestas persisten al avanzar/retroceder sin autosave ni intento incompleto en servidor.
- **JS externo CSP-safe** (`static/js/quiz-player.js`, incluido vía `{% block extra_js %}`) que
  controle: navegación anterior/siguiente, salto desde la revisión, progreso, pantalla de revisión,
  foco atrapado, cierre (botón/Escape/confirmación), restauración de foco y bloqueo de scroll del body.
- Ocultar `.whatsapp-float` mientras el reproductor esté abierto.
- Al cerrar, usar el endpoint de estado existente (`quiz_status`) para refrescar niveles/estrellas.

### Experiencia
- Cabecera fija: cerrar (✕), modo/nivel y progreso “Pregunta 2 de 5”.
- Área central con ancho cómodo en PC y ancho completo en móvil; una pregunta + alternativas por pantalla.
- Pie fijo con `Anterior` y `Siguiente`. Se puede avanzar sin responder y volver a cualquier pregunta.
- Tras la última pregunta, **pantalla de revisión** con indicadores respondida/pendiente; el **envío
  ocurre solo desde ahí**.
- Preparación y Evaluación muestran la corrección **solo al finalizar**.
- Los resultados abren con nota/estado y permiten revisar cada respuesta; conservan el **mismo orden
  aleatorio** en que se presentaron las preguntas.
- Cerrar con respuestas seleccionadas pide confirmación; al cerrar se **restaura el foco** al botón origen.

## No-objetivos (qué queda FUERA)
- Corrección inmediata pregunta a pregunta en Preparación (la corrección sigue siendo al final).
- Guardar intentos incompletos en el servidor (no hay autosave).
- Nuevos endpoints públicos, migraciones o dependencias.
- Rediseño de la lógica/puntuación de evaluación (se conserva intacta).

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check` · `makemigrations --check --dry-run`
- [ ] El reproductor ocupa el viewport completo en móvil (360–390 px) y PC, sin cabecera del sitio,
      sin WhatsApp flotante ni contenido de fondo visible.
- [ ] Una pregunta por pantalla; `Anterior`/`Siguiente` navegan y las respuestas **persisten** al
      avanzar/retroceder.
- [ ] La pantalla de revisión marca respondida/pendiente y es el **único** punto de envío.
- [ ] Enviar con preguntas sin responder funciona; esas cuentan como incorrectas.
- [ ] Los resultados conservan el orden de presentación (mismo orden aleatorio).
- [ ] Aplica a Preparación, Evaluación por nivel y **Evaluación final del tema**; estados
      bloqueado/vacío también se ven dentro del reproductor.
- [ ] Foco atrapado, cierre con Escape, confirmación al cerrar con respuestas, restauración del foco.
- [ ] CSS con cache-buster `?v=N` subido.

## Plan de pruebas
- Navegación anterior/siguiente y salto desde la revisión.
- Respuestas conservadas al retroceder.
- Envío con preguntas pendientes y corrección adecuada.
- Orden de resultados idéntico al orden presentado.
- Flujos de Preparación, Evaluación, bloqueo, reintento y evaluación final del tema.
- Foco atrapado, cierre con Escape, restauración del foco y navegación por teclado.
- QA en móvil de 360–390 px y escritorio, incluyendo preguntas y alternativas largas.
- Tests focalizados, `check`, `makemigrations --check --dry-run` y suite completa antes de entregar.

## Riesgos / rollback
- **Riesgo CSP:** todo el JS debe ir en archivo externo con `nonce`; nada inline nuevo. Verificar
  que no rompa la política existente (`apps/core/middleware.py`).
- **Riesgo de scroll/foco** atrapado en móvil (teclado virtual, body lock). Mitigar con pruebas en
  360–390 px.
- **Rollback:** el cambio es de presentación (templates + CSS + JS, sin migraciones). Revertir el
  commit restaura los cuestionarios verticales actuales.

## Supuestos
- No hay corrección inmediata en Preparación.
- No se guarda intento incompleto en el servidor.
- El alumno puede enviar preguntas sin responder; cuentan como incorrectas.

---

## Qué se hizo
**Implementado en la rama `feat/reproductor-preguntas-fullscreen` (🏛️ Claude).**

- **Overlay global** `#quiz-player-root` en `templates/base.html` (fixed, `inset:0`, fuera del
  contenido) + inclusión de `static/js/quiz-player.js?v=1` y cache-buster CSS `?v=30`.
- **`static/js/quiz-player.js`** (CSP-safe, externo): apertura/cierre del overlay vía
  `htmx:afterSwap`, navegación una-pregunta-a-la-vez (`Anterior`/`Siguiente`), progreso
  "Pregunta N de M", pantalla de **revisión** con chips respondida/pendiente y salto a cualquier
  pregunta, foco atrapado + restauración al disparador, cierre con Escape, **confirmación al cerrar
  con respuestas seleccionadas**, bloqueo de scroll del body y refresco de niveles vía
  `quiz_status` al cerrar.
- **Reproductor en formularios:** `templates/includes/quiz_form.html` y `topic_exam_form.html`
  reescritos como reproductor (todas las preguntas en el mismo `<form>`, ocultas salvo la activa →
  las respuestas persisten sin autosave). Reporte de error pasó a `data-quiz-report-toggle`
  (sin `onclick` inline).
- **Paneles dentro del reproductor:** `quiz_results.html`, `quiz_blocked.html`,
  `quiz_recover_result.html`, `quiz_empty.html`, `quiz_error.html`, `topic_exam_results.html`,
  `topic_exam_empty.html` envueltos en cabecera fija + cuerpo scrollable; "Volver a niveles"/
  "Cerrar" pasaron a `data-quiz-close`.
- **Disparadores** (`quiz_section.html`, `topic_exam_section.html` y botones de resultados/bloqueo/
  recuperación) re-apuntados a `hx-target="#quiz-player-root"`.
- **Backend:** `quiz_submit` (`apps/content/views/evaluation_views.py`) ahora ordena los resultados
  por el **orden de presentación** (IDs de la sesión), no por `question.order`. (La evaluación final
  del tema ya preservaba el orden.) **Sin migraciones ni endpoints nuevos.**
- **CSS** nuevo en `static/css/estilos.css` para el reproductor (cabecera/cuerpo/pie, revisión,
  resultados, ocultar WhatsApp con `body.quiz-open`, `env(safe-area-inset-*)`).

### Verificación
- Tests focalizados de evaluación verdes (60) + nuevo test
  `test_quiz_results_preserve_presentation_order`. `check` sin errores; `makemigrations --check
  --dry-run` sin cambios.
- **QA visual** (runserver) en escritorio y móvil 360px: abrir, navegar, persistencia al
  retroceder, salto desde revisión, envío, resultados a pantalla completa con corrección, cierre con
  restauración de scroll/WhatsApp y refresco de niveles. **Sin errores de consola.**

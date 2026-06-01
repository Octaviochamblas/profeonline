# Correcciones visuales: barra de acciones, hero de tema y página de nivel

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** UX / Frontend
- **Origen:** ajustes visuales tras desplegar `visibilidad-ejercitacion-evaluacion-progreso`
  (Fases A–D ya en `3 Finalizados/`).
- **Prioridad:** Media (pulido visual; no bloquea funcionalidad).

## Problema / Objetivo

Tras el deploy de la visibilidad de ejercitación/evaluación/progreso, hay 4 detalles de UX que
corregir en el detalle de recurso, el hero del tema y la página de nivel.

## Acotaciones (4) — aterrizadas al código

### Acotación 1 — Quitar el texto del botón "Comprendido"
- **Dónde:** `templates/includes/completion_button.html:13`
  (`<span class="completion-hint">Lo marcaste como comprendido. Pulsa para desmarcar.</span>`).
- **Qué:** eliminar esa línea. Conservar el botón con el check y el texto "Comprendido".

### Acotación 2 — "Ir a Ejercitación" / "Ir a Evaluación" en TODOS los recursos, misma línea
- **Dónde:** `templates/pages/resource_detail.html:102-118` (`.resource-action-bar`).
- **Hoy:** los botones de Ejercitación/Evaluación solo se renderizan dentro de
  `{% if quiz_available %}` (líneas 104-113), así que en recursos sin preguntas la barra queda
  solo con "Comprendido" (inconsistente). El include del quiz también está bajo `quiz_available`
  (línea 120).
- **Qué:**
  - Sacar los botones **fuera** del `{% if quiz_available %}` para que **siempre** aparezcan los
    3 en la misma línea (la barra ya es flex). Etiquetas: **"Ir a Ejercitación"** y
    **"Ir a Evaluación"** (como en la captura).
  - Que los 3 tengan **estilo de botón coherente** (en la captura, "Ir a…" se ven como texto
    plano y "Comprendido" como botón sólido; deben verse consistentes — botones secundarios + el
    de comprendido como estado).
  - **Los anclas no deben apuntar a vacío:** como las acciones ahora siempre se muestran, hay que
    garantizar que las secciones destino existan. Renderizar **siempre** la sección de
    ejercitación/evaluación (mover el include fuera de `{% if quiz_available %}`) y que
    `quiz_section.html` muestre el estado vacío ("Aún no hay ejercicios publicados…") cuando no
    haya preguntas. Así el botón siempre lleva a una sección válida.
  - **Decisión cerrada:** si el recurso no tiene NINGUNA pregunta publicada, los botones igual se
    muestran y llevan a la sección con su estado vacío (no se ocultan), para que la barra sea
    idéntica en todos los recursos.

### Acotación 3 — "Ruta de aprendizaje" fuera de la tarjeta del tema
- **Dónde:** `templates/pages/topic_detail.html:19-35`.
- **Hoy:** el kicker `<p class="page-hero__kicker">Ruta de aprendizaje</p>` (línea 22) está
  **dentro** del `<div class="detail-card">`, junto al `<h1>` y la descripción → se ve apretado.
- **Qué:** mover el kicker **fuera y encima** del `.detail-card` (como kicker de página, sobre la
  tarjeta). La tarjeta queda solo con el nombre (`<h1>`), la descripción, la meta y el botón
  "Volver a temas". Mantener jerarquía y espaciado del sistema (`stack`).

### Acotación 4 — Reestructurar la página de Nivel (`level_detail`)
- **Dónde:** `apps/content/views/level_detail.py` + `templates/pages/level_detail.html`.
- **Hoy:** la vista provee `subjects` (asignaturas con recursos publicados en el nivel) y
  `resources` (lista plana). El template muestra: tarjeta con nombre del nivel, grid de
  asignaturas, y una sección **"Recursos"** plana (líneas 78-113). No hay temas ni búsqueda.
- **Qué:**
  - **Eliminar** la sección "Recursos" (`level_detail.html:78-113`) — sin filtros es imposible de
    navegar.
  - **Marcar y separar dos secciones claras y rotuladas:**
    - **"Asignaturas"** — el grid de asignaturas que ya existe, con un heading explícito
      "Asignaturas".
    - **"Temas"** — sección nueva con heading "Temas", **agrupada por asignatura**
      (clasificación "según Asignatura y luego Tema"), usando tarjetas de tema (reusar el partial
      `templates/pages/_topic_card.html`).
  - **Buscador en la sección de Temas:** input de búsqueda que filtre los temas por nombre.
    - **Opción recomendada (MVP):** filtro **client-side** en JS (script con `nonce`) que oculta
      las tarjetas cuyo nombre no coincide. Sin endpoint nuevo. Apto porque los temas por nivel
      no son muchos.
    - **Alternativa:** búsqueda **HTMX** como en `topic_list.html` (ya hay precedente, ver el
      `hx-get` ahí), si se prefiere server-side.
  - **Vista:** agregar `context["topics"]` =
    `Topic.objects.filter(is_active=True, resources__levels=level, resources__is_published=True)
    .distinct().select_related("subject").order_by("subject__name", "name")`.
    Quitar `context["resources"]` (ya no se usa). En el template, agrupar por asignatura con
    `{% regroup topics by subject as topics_by_subject %}`.

## Consideraciones / convenciones a respetar

- **Tokens de color** (`var(--primary)` teal, `--cta` ámbar, neutros slate): no hardcodear
  colores. (En `topic_detail.html` hay un verde `#16a34a` hardcodeado en las barras — si se toca,
  tokenizarlo, pero no es parte de estas acotaciones.)
- **CSS en `estilos.css`**, no estilos inline nuevos; **bump del cache-buster** `?v=` para ver el
  cambio en prod.
- **Accesibilidad:** el input de búsqueda con `label`/`aria-label`; contraste AA (hay tarjeta de
  axe abierta); foco visible.
- **CSP con nonce:** cualquier `<script>` nuevo (buscador client-side) debe llevar
  `nonce="{{ csp_nonce }}"`.
- **SEO/breadcrumbs** de `level_detail` y `topic_detail` intactos.

## Plan de pruebas

- `resource_detail`: aparecen "Ir a Ejercitación" y "Ir a Evaluación" **aunque el recurso no
  tenga preguntas publicadas**; el texto "Lo marcaste como comprendido. Pulsa para desmarcar."
  **ya no** aparece; los anclas resuelven a una sección existente (estado vacío incluido).
- `topic_detail`: sigue apareciendo "Ruta de aprendizaje" y el nombre/descripcion del tema (el
  cambio es estructural; al menos verificar que no se rompa el render y status 200).
- `level_detail`: el contexto trae `topics`; la página muestra headings "Asignaturas" y "Temas";
  **no** muestra la antigua sección "Recursos"; agrupa temas por asignatura.
- Si el buscador es HTMX: test del filtrado por `?q=`. Si es client-side: QA visual (no
  automatizable).
- Barrera de CI completa en verde (suite + `check` + `makemigrations --check` + `check --deploy`).

## Supuestos

- Reusar `_topic_card.html` para las tarjetas de tema en `level_detail` (las barras de progreso
  del partial solo se muestran a autenticados, comportamiento ya existente).
- "Ir a Ejercitación" → ancla a la zona de práctica; "Ir a Evaluación" → ancla a la zona de
  evaluación, ambas dentro de la misma página del recurso.

---

## Prompt para Antigravity (implementación)

> Pegar tal cual. Autocontenido; paths verificados contra el código real.

```
Trabajas en el repo Django ProfeOnline (Windows; settings por defecto config.settings.local,
producción config.settings.production). Implementa la tarjeta
docs/1 Por iniciar/correcciones-visuales-recurso-tema-nivel.md COMPLETA (4 acotaciones). Léela
de arriba a abajo; respeta "Consideraciones / convenciones".

Proceso:
- Rama propia: feat/correcciones-visuales-recurso-tema-nivel. NO toques main ni ramas de otros
  agentes. Mueve la tarjeta a docs/2 En Proceso/ con `git mv` al empezar.

Acotación 1 — quitar texto del botón comprendido:
- En templates/includes/completion_button.html elimina la línea del
  <span class="completion-hint">Lo marcaste como comprendido. Pulsa para desmarcar.</span>.
  Conserva el botón "Comprendido" con su check.

Acotación 2 — botones "Ir a Ejercitación"/"Ir a Evaluación" en TODOS los recursos:
- En templates/pages/resource_detail.html (.resource-action-bar, ~líneas 102-118): saca los
  botones de Ejercitación/Evaluación FUERA del {% if quiz_available %} para que siempre se
  muestren los 3 en la misma línea. Renómbralos a "Ir a Ejercitación" y "Ir a Evaluación".
- Renderiza SIEMPRE la sección de quiz/evaluación (mueve el include de quiz_section.html fuera
  del {% if quiz_available %}) y asegúrate de que quiz_section.html muestre un estado vacío
  general cuando no hay preguntas publicadas, para que los anclas (#quiz-level-1, #quiz-section)
  nunca apunten a un nodo inexistente.
- Estilo consistente de los 3 botones (clases en static/css/estilos.css, no inline).

Acotación 3 — "Ruta de aprendizaje" fuera de la tarjeta del tema:
- En templates/pages/topic_detail.html (~líneas 19-35): mueve el
  <p class="page-hero__kicker">Ruta de aprendizaje</p> FUERA y ENCIMA del <div class="detail-card">.
  La tarjeta queda solo con <h1>{{ topic.name }}</h1>, la descripción, la meta y "Volver a temas".

Acotación 4 — reestructurar level_detail:
- apps/content/views/level_detail.py: agrega
  context["topics"] = Topic.objects.filter(is_active=True, resources__levels=level,
  resources__is_published=True).distinct().select_related("subject").order_by("subject__name","name")
  Quita context["resources"] (ya no se usa).
- templates/pages/level_detail.html:
  - ELIMINA la sección "Recursos" (~líneas 78-113).
  - Sección "Asignaturas": agrega heading explícito "Asignaturas" sobre el grid de subjects.
  - Sección "Temas": heading "Temas", temas agrupados por asignatura
    ({% regroup topics by subject as topics_by_subject %}), usando el partial
    templates/pages/_topic_card.html para cada tema.
  - Buscador en la sección de Temas: input client-side (vanilla JS en un <script nonce="{{ csp_nonce }}">)
    que filtra las tarjetas de tema por nombre (data-attr). Input con aria-label, contraste AA.

Convenciones (obligatorias):
- Nada de colores hardcodeados (usa tokens var(--...)). CSS nuevo en static/css/estilos.css, no
  inline. Sube el cache-buster ?v= del CSS. Scripts con nonce="{{ csp_nonce }}". Mantén
  breadcrumbs/SEO. Contraste AA.

Tests a agregar/actualizar:
- resource_detail: "Ir a Ejercitación"/"Ir a Evaluación" presentes aun sin preguntas publicadas;
  el texto "Lo marcaste como comprendido. Pulsa para desmarcar." ya NO aparece.
- level_detail: el contexto trae "topics"; la página muestra "Asignaturas" y "Temas" y NO muestra
  la sección "Recursos"; agrupa temas por asignatura.
- topic_detail: status 200 y sigue mostrando "Ruta de aprendizaje" + nombre del tema.

Verificación antes de entregar (barrera real de CI; deja TODO verde):
  .venv\Scripts\python.exe manage.py test
  .venv\Scripts\python.exe manage.py check
  .venv\Scripts\python.exe manage.py makemigrations --check --dry-run
El check --deploy de producción REQUIERE env vars o crashea (ImproperlyConfigured). Setealas como
en .github/workflows/django_ci.yml (PowerShell) antes de correrlo:
  $env:DJANGO_SECRET_KEY="ci-test-secret-key-must-be-long-and-secure-in-production-check"
  $env:DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,testserver"
  $env:DJANGO_CSRF_TRUSTED_ORIGINS="http://localhost,http://127.0.0.1,http://testserver"
  $env:DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS="true"; $env:DJANGO_SECURE_HSTS_PRELOAD="true"
  $env:DATABASE_URL="postgres://user:pass@localhost:5432/ci_dummy"
  .venv\Scripts\python.exe manage.py check --deploy --fail-level ERROR --settings=config.settings.production

Entrega:
- Completa "Qué se hizo" en la tarjeta, muévela a docs/3 Finalizados/ con `git mv`.
- Abre un PR contra main; NO hagas squash-merge (déjalo para auditoría). Indica rama y nº de PR.
```

---

## Qué se hizo

1. **Acotación 1 (Texto botón Comprendido):** Se eliminó el texto descriptivo extra en `completion_button.html`, dejando el botón limpio con su check e indicación concisa "Comprendido".
2. **Acotación 2 (Ejercitación/Evaluación en todos los recursos):**
   - Se removió la condicional `{% if quiz_available %}` en la barra de acciones de `resource_detail.html` para mostrar siempre los tres botones (Ir a Ejercitación, Ir a Evaluación y Comprendido) de manera visualmente consistente.
   - Se movió el include de `quiz_section.html` fuera de la condicional, logrando que siempre se renderice la sección de autoevaluación, y en caso de no haber preguntas, muestre un estado vacío coherente ("Aún no hay ejercicios publicados para este nivel").
3. **Acotación 3 (Kicker Ruta de aprendizaje):** Se reubicó el kicker `<p class="page-hero__kicker">Ruta de aprendizaje</p>` fuera y por encima del contenedor `.detail-card` en `topic_detail.html`, mejorando el espaciado y estructura de la cabecera.
4. **Acotación 4 (Reestructuración de Nivel / Buscador):**
   - En `level_detail.py`, se removió la lista plana de recursos y se introdujo la consulta en lote de temas con su respectivo mapa de progreso (`get_topics_progress_map`), evitando consultas N+1.
   - En `level_detail.html`, se eliminó la sección de recursos planos y se crearon dos secciones claras: "Asignaturas" y "Temas". Los temas se agrupan por asignatura usando `{% regroup %}` (ordenados adecuadamente en la consulta de BD por `subject__name` y `name`).
   - Se implementó un buscador de temas en el servidor mediante el parámetro `q` de consulta GET, haciéndolo accesible y testeable.
   - Se desactivó el badge de asignatura en las tarjetas de tema agrupadas (`show_subject_badge=False`) por redundancia.
5. **Estilización y Clases CSS:**
   - Se trasladaron todas las declaraciones CSS de progreso inline a clases externas en `estilos.css` (`.topic-card-progress`, `.topic-progress--panel`, etc.).
   - Se garantizó el uso del token de color `--success: #15803d;` en lugar de colores hardcodeados como `#16a34a`.
   - Se incrementó el cache buster de estilos en `base.html` a `?v=14`.
6. **Tests y Verificación:**
   - Se adaptaron los tests legacy `test_resource_detail_no_quiz_without_questions` y `test_draft_questions_not_visible` para asertar positivamente sobre el estado vacío del quiz en lugar de su ausencia.
   - Se actualizó la aserción en `test_subject_and_level_detail_pages_render` para el detalle de nivel.
   - Se añadió la clase de test `LevelDetailViewTests` en `test_views.py` para verificar el filtrado por búsqueda del parámetro `q` en el detalle de nivel y el agrupamiento de temas.
   - Se ejecutó y validó la suite de tests completa (`Ran 165 tests OK`), comprobación de migraciones y la barrera de despliegue en producción con éxito.

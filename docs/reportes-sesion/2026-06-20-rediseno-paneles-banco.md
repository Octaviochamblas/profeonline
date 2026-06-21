# Reporte de sesión — 2026-06-20 (rediseño de paneles del banco)

> Sesión 🏛️ Claude + 🧑 Octavio. Rama `feat/rediseno-resumen-banco`. Trabajo de UI/UX
> sobre dos paneles del banco de preguntas; sin migraciones ni cambios en producción.

## 1. Resumen del banco (`/publicar/preguntas/resumen/`) — acordeón Área → Asignatura → Tema → Recurso

Se reemplazó la tabla ancha (que mezclaba todo al mismo peso visual) por un **acordeón
jerárquico** navegable:

- Cada nodo (Área, Asignatura, Tema) muestra el nº de recursos y las **5 categorías
  editoriales como fracción `auditados/total`** (Transcripción, Título web, Descripción web,
  Título YouTube, Descripción YouTube), con color verde/ámbar/rojo según cuántos recursos
  estén auditados.
- Al expandir un nodo aparece el siguiente nivel; el tema despliega sus **recursos**.
- Cada recurso (hoja) muestra: **preguntas publicadas por nivel** (N1/N2/N3 destacadas), las
  5 marcas editoriales ✓/✗ compactas (solo icono, con tooltip), y enlaza a su página de
  edición.
- **Semáforo de cobertura** (reemplaza las barras de nivel): verde = completo, amarillo =
  faltan preguntas, rojo = menos del 20% de lo requerido (`CRITICAL_COVERAGE_RATIO = 0.2`).
  El estado se agrega hacia arriba (tema/asignatura/área).

Archivos: [bank_analytics.py](../../apps/content/views/bank_analytics.py) (`_build_coverage_tree`,
`_coverage_status`, `_audit_fractions`, `_aggregate_node`, conteo por nivel y `coverage_status`
por recurso), [bank_coverage.html](../../templates/pages/bank_coverage.html),
[bank_audit_fractions.html](../../templates/includes/bank_audit_fractions.html) (include de
fracciones reutilizado en los 3 niveles), [bank_analytics.css](../../static/css/bank_analytics.css),
[bank_analytics.js](../../static/js/bank_analytics.js) (se quitó el filtro client-side, ya no
necesario con el acordeón).

## 2. Panel de generación por recurso (`question_review`) — rediseño completo

A pedido del 🧑, se reorganizó la página de gestión de un recurso:

- **Configuración de Evaluación arriba, ancho completo:** intentos, umbral, regla de
  recuperación, nivel educativo (IA), "permitir repetir / autopublicar" y la **Muestra**
  (cuántas preguntas ve el alumno) por nivel y modo —valores estándar por defecto, editables
  por recurso—. Se **quitó el campo "Pool"** del formulario: se conserva su valor existente
  (meta del banco que usa el resumen) detrás de escena.
- **Generación con IA, ancho completo:** una tarjeta por nivel donde se **habilita el nivel**,
  se habilita **Práctica y/o Evaluación con su cantidad**, y una **descripción/enfoque por
  nivel** que se pasa a la IA. Botón único "Generar lo habilitado" que recorre lo activado
  generando en tandas de 5 (tope por timeout de gunicorn) con log de progreso en vivo;
  las preguntas se anexan al acordeón.
- Se **deshabilitó "Generar copiando documento"**; queda solo "desde el video"
  (transcripción).

### Backend de generación
- La generación sigue siendo **solo por API (Gemini 2.5 Flash; OpenAI como fallback)**.
- Ahora **se le pasan a la IA las preguntas ya existentes del recurso** y se le instruye a no
  repetirlas ni hacer variantes triviales (`_existing_question_texts` + bloque en el prompt).
- `generate_questions_inline` acepta una `description` (instrucción por nivel).
- `save_resource_quiz_config` conserva el `pool` existente y solo actualiza `shown` + params.

Archivos: [ai_generation_service.py](../../apps/content/services/ai_generation_service.py),
[question_review.py](../../apps/content/views/question_review.py),
[question_review.html](../../templates/pages/question_review.html),
[question_review.js](../../static/js/question_review.js) (`initGenx` orquestador),
[question_studio.css](../../static/css/question_studio.css).

## Validación
- **Tests focalizados verdes:** `test_bank_analytics` (17), `test_ai_generation` (9),
  `test_ai_api_resilience` (3), `test_generate_inline` + `test_quiz_config` (24). Se agregaron
  casos: agregación de fracciones por nodo, estado crítico <20%, y que el prompt incluya las
  preguntas existentes (anti-repetición).
- `manage.py check` sin issues; `makemigrations --check` → sin cambios (no hay migraciones).
- Render de `question_review` confirmado por el GET 200 de `test_quiz_config`.

## Pendientes / notas
- **Verificación visual en navegador** (solo-admin): el flujo de clics del orquestador de
  generación (habilitar niveles, tandas, log) conviene probarlo logueado; se validó a nivel
  de endpoints/tests.
- **Pool vs cobertura:** el 🧑 quería "pool = lo generado", pero el pool es la meta que usa el
  semáforo del resumen. Se dejó el pool conservándose como meta estándar; si se quiere
  eliminar de verdad, hay que rediseñar también el semáforo de cobertura (paso aparte).
- La suite completa + `check --deploy` siguen siendo la barrera real en CI antes de pushear.

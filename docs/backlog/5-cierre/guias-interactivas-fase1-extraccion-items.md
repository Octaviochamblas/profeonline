# Guías interactivas — Fase 1: extracción y aprobación de ítems

- **Estado:** 🟢 CERRADA (2026-06-22) — todos los P1/P2 corregidos, barrera completa verde, mergeada a `main`.
- **Creado:** 2026-06-22 · **Epic padre:** `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`
- **Prioridad:** P1 · **Cartera:** educativa · **Tipo:** producto · pedagogía
- **Dueño:** 🧩 Codex (preflight) → 🔨 Antigravity (construye, rama `feat/guias-fase1-extraccion-items`) → 🧩 Codex (audita) → 🏛️ Claude (cierre)

> **Alcance de esta fase: SOLO extracción IA de ítems + panel de aprobación.** A partir de una
> guía privada ya subida, la IA propone ítems de aprendizaje y un panel admin propio permite
> editar / fusionar / rechazar / aprobar. **Sin** generar guía nueva, **sin** banco visible, **sin**
> parser de respuesta, **sin** evaluaciones. Eso entra en las fases 2–7.

## Objetivo (una frase)
A partir de una guía privada (`QuizGuide.content_text`), la IA **propone ítems de aprendizaje**
(objetivo, nivel, dificultad, recomendación, errores frecuentes, recursos sugeridos, cantidad de
ejercicios detectada) y un **panel admin propio** permite editarlos, fusionarlos, rechazarlos o
aprobarlos — dejando ítems `aprobado` listos para que las fases siguientes generen guía y banco.

## Antes de empezar
- `git pull` (la rama parte de `origin/main`; Fase 0 / #81 y el parser tolerante #80 ya están).
- Todo va **detrás del flag por tema**: el panel opera sobre temas pero **no** cambia el
  comportamiento de temas con `structured_bank_enabled=False`. **No tocar el banco legacy.**

## Fuentes a leer (rutas concretas)
- `apps/content/models/exercise_item.py` — `ExerciseItem` (ya existe: `topic`, `title`, `level`,
  `difficulty`, `objective`, `recommendation`, `common_errors`, `order`, `status`
  propuesto/aprobado/archivado, `learning_guide`) y `ResourceExerciseItem` (cuotas + constraint
  `unique_item_resource`).
- `apps/content/models/quiz_guide.py` — fuente privada: el texto a analizar está en `content_text`;
  vínculos M2M a `resources`/`topics`/`subjects` e `is_active`.
- `apps/content/models/question.py` — usar `Question.LEVEL_CHOICES` y `Question.DIFFICULTY_CHOICES`
  para validar lo que devuelve la IA.
- `apps/content/services/ai_generation_service.py` — reusar `_call_gemini_api` / `_call_openai_api`
  (ambos con `responseMimeType: application/json`), **`_loads_ai_json`** (parser tolerante del #80),
  el patrón de selección de llave (`GEMINI_API_KEY` → `OPENAI_API_KEY`), `_sanitize_key` y
  `_post_json_with_retry` (backoff 429). Mirar `_generate_mock_questions` como referencia de mock.
  **No reinventar llamadas HTTP ni parseo.**
- `apps/content/views/question_review.py` y `apps/content/views/bank_analytics.py` — patrón de panel
  staff: `@user_passes_test(is_admin)` (de `apps.content.views.permissions`), render a
  `templates/pages/…`, edición inline vía HTMX.
- `apps/content/urls/publish_urls.py` — todas las rutas staff cuelgan de `publicar/…`.
- `templates/pages/quiz_guides.html` y `templates/pages/bank_coverage.html` — estilo de los paneles
  propios (config-driven, no Django admin).

## Decisiones de diseño ya tomadas (del epic)
- **Nada se publica automáticamente** (solo el sistema nuevo); la aprobación de ítems es manual.
- Administración con **paneles propios in-app** (no Django admin), config-driven.
- La **fuente privada** reutiliza `QuizGuide`; los ítems aprobados se enlazan a la `LearningGuide`
  de origen vía el FK `learning_guide` (la guía generada llega en Fase 2; en Fase 1 puede ir nulo o
  enlazarse a una `LearningGuide` borrador placeholder — preferir **nulo** hasta Fase 2).
- **Costo IA:** generar a cuentagotas — un disparo por guía, sin reintentos masivos automáticos.

## Alcance de construcción

### 1) Servicio nuevo: `apps/content/services/item_extraction_service.py`
- `propose_items_from_guide(quiz_guide, topic, api_key=None) -> list[dict]`:
  - Helper `_build_item_prompt` (LaTeX en *raw strings*, como `_build_prompt`) que recibe
    `quiz_guide.content_text` + el tema **+ el nivel educativo** (ver abajo) y **pide JSON** con, por
    ítem: `title`, `level` (1/2/3), `difficulty` (de `DIFFICULTY_CHOICES`), `objective`,
    `recommendation`, `common_errors`, `suggested_resource_ids` (de los recursos del tema) y
    `detected_exercise_count`.
  - **Calibrar la dificultad al nivel educativo:** pasar al prompt el nivel educativo del tema/recurso
    (`Resource.get_education_level()` para los recursos del tema; si difieren o no hay recurso, usar el
    del tema vía su asignatura — `Subject.education_level`, migración 0031). La instrucción debe pedir
    que `difficulty` se reparta según ese nivel (p. ej. un tema Escolar tiende a `básica`/`intermedia`;
    Medio/Preuniversitario a `intermedia`/`avanzada`; Universitario a `avanzada`/`desafío`), **no** que
    todo salga `intermedia`. El nivel educativo es el ancla de calibración, no un valor fijo.
  - Llama vía los helpers existentes y parsea con **`_loads_ai_json`** (no `json.loads` directo).
  - Toda fórmula en LaTeX `$...$`/`$$...$$` (consistente con el resto del pipeline + KaTeX).
  - **Modo test/sin llave:** mock determinista (estilo `_generate_mock_questions`) para que la suite
    no llame a la red.
  - **No persiste**: devuelve los dicts; la persistencia la decide el profesor en el panel.

### 2) Panel admin propio (HTMX, `is_admin`) — `apps/content/views/item_review.py`
- `item_extraction(request)` (GET) — selector de **tema** + **guía privada** (las `QuizGuide`
  vinculadas a ese tema o a sus asignaturas) → botón "Proponer ítems con IA".
- `propose_items(request)` (POST/HTMX) — corre el servicio, guarda los ítems con `status="propuesto"`
  enlazados al tema (y a la guía de origen cuando exista), y renderiza la lista editable.
  Un disparo por guía (a cuentagotas).
- Edición / fusión / rechazo / aprobación (HTMX inline, espejo de `question_review`):
  - `edit_item_inline(item_id)` — editar campos.
  - `set_item_status(item_id)` — `aprobado` / `archivado`.
  - `merge_items(request)` — fusiona ≥2 ítems en uno (concatena objetivo/errores, reasigna
    `resource_links` sin duplicar, archiva los origen).
  - `link_item_resource(item_id)` / `unlink_item_resource(...)` — crea/borra `ResourceExerciseItem`
    (cuotas en 0 por ahora; se afinan en las fases de evaluación).
- **Nada se borra**: rechazar = `status="archivado"`, nunca `.delete()`.

### 3) URLs (`apps/content/urls/publish_urls.py`)
```
publicar/items/                         → item_extraction        (name="item_extraction")
publicar/items/proponer/                → propose_items          (name="propose_items")
publicar/items/editar/<int:item_id>/    → edit_item_inline       (name="edit_item_inline")
publicar/items/estado/<int:item_id>/    → set_item_status        (name="set_item_status")
publicar/items/fusionar/                → merge_items            (name="merge_items")
publicar/items/vincular/<int:item_id>/  → link_item_resource     (name="link_item_resource")
```
Agregar el enlace al panel desde el menú staff existente (junto a "Guías" / "Resumen").

### 4) Plantillas
`templates/pages/item_extraction.html` + parciales HTMX (`partials/_item_row.html`, etc.), reusando
el estilo de los paneles staff. KaTeX ya se renderiza solo en `htmx:afterSwap` — no agregar JS de render.

## Contrato JSON de la IA
```json
[
  {
    "title": "…",
    "level": 1,
    "difficulty": "básica",
    "objective": "…",
    "recommendation": "…",
    "common_errors": "…",
    "suggested_resource_ids": [12, 15],
    "detected_exercise_count": 8
  },
  {
    "title": "…",
    "level": 3,
    "difficulty": "avanzada",
    "objective": "…",
    "recommendation": "…",
    "common_errors": "…",
    "suggested_resource_ids": [15],
    "detected_exercise_count": 5
  }
]
```
`difficulty` ∈ `DIFFICULTY_CHOICES` (`básica/intermedia/avanzada/desafío`) y se **calibra al nivel
educativo** del tema/recurso (ver el servicio), no es un valor fijo. Toda fórmula en LaTeX `$...$`.
El parseo tolera cercas markdown / prosa (lo cubre `_loads_ai_json`).

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `python manage.py test` · `check --deploy` · `makemigrations --check --dry-run`
  (esta fase **no debería** requerir migraciones; si las requiere, **aditivas** y justificadas).
- [ ] El panel solo es accesible para `is_admin` (test de acceso anónimo / no-staff → redirect/403).
- [ ] `propose_items_from_guide` parsea con `_loads_ai_json`; con mock (sin llave) devuelve ítems
  válidos sin tocar la red.
- [ ] Aprobar/archivar/fusionar cambia `status` (nunca borra filas); fusionar reasigna
  `resource_links` sin duplicar (respeta `unique_item_resource`).
- [ ] Temas con `structured_bank_enabled=False` y el **banco legacy quedan intactos** (regresión).
- [ ] Si se toca CSS → cache-buster `?v=N`.

## Plan de pruebas (mínimo)
- Extracción con mock → N ítems `propuesto` enlazados al tema/guía.
- Parseo tolerante (LaTeX escapado + cerca markdown) vía el servicio nuevo.
- Aprobar / archivar / fusionar (incluida la no-duplicación de `ResourceExerciseItem`).
- Control de acceso (`is_admin`).
- Regresión: generación legacy de preguntas sigue funcionando.
- QA móvil del panel (320/360/390 px).

## No-objetivos (qué queda FUERA de la Fase 1)
- Generar la guía ProfeOnline original ni validación de originalidad (Fase 2).
- Banco visible / experiencia de estudio (Fase 3).
- Parser de respuesta directa (Fase 4); evaluaciones/timers/dominio (Fase 5); PDF (Fase 6);
  migración legacy + gate de activación + piloto (Fase 7).
- Publicar nada automáticamente.

## Riesgos / rollback
- **Costo IA:** a cuentagotas; un disparo por guía, sin reintentos masivos automáticos.
- **Llave en logs:** usar `_sanitize_key` en cualquier error (patrón existente).
- **Rollback:** todo es aditivo y solo staff; basta no usar el panel. Ningún tema cambia de
  comportamiento (el flag sigue gobernando las fases visibles al alumno).

## Auditoría 🧩 Codex — 2026-06-22

**Gate:** rechazado; vuelve a construcción por hallazgos P1.

### P1 — bloqueantes

1. **El flag por tema no gobierna el panel ni las mutaciones.**
   `item_extraction`, `propose_items`, edición, estados, fusión y vínculos aceptan temas con
   `structured_bank_enabled=False`; incluso el selector lista todos los temas activos
   (`apps/content/views/item_review.py:31-56,81-82,165,227,265,329,364`). Esto contradice la
   restricción dura de aislamiento. Filtrar/validar el flag server-side en todas las entradas y
   agregar regresión que demuestre que un tema desactivado no puede crear ni modificar ítems.
2. **La fusión permite mezclar ítems de temas distintos y corromper asociaciones.**
   Se cargan IDs globales, se toma el tema del primer ítem y se trasladan todos los recursos antes
   de archivar todos los orígenes (`apps/content/views/item_review.py:265-312`). Exigir que todos
   pertenezcan al mismo tema habilitado —idealmente filtrando por `topic_id` validado— y rechazar
   cualquier conjunto mixto; agregar test de regresión.
3. **La UI de fusión queda bloqueada por la CSP vigente.**
   Se añadió un `<script>` sin nonce y un `onclick` inline
   (`templates/pages/item_extraction.html:64-66,83-139`). La política solo permite scripts con nonce,
   y los event handlers inline tampoco quedan autorizados. Mover la lógica a un archivo JS externo
   autoalojado, cargarlo con nonce/cache-buster y enlazar eventos con `addEventListener`.
4. **Se descarta un dato central del contrato IA.**
   `detected_exercise_count` se pide y llega en el JSON, pero `propose_items` nunca lo valida,
   persiste ni muestra (`apps/content/views/item_review.py:100-148`). El profesor no puede revisar
   la cantidad detectada prometida por la Fase 1. Incorporar almacenamiento/presentación editable
   —con migración aditiva si hace falta— y sus pruebas.
5. **El POST acepta cualquier guía por ID, aunque esté inactiva o no pertenezca al tema/asignatura.**
   El selector filtra, pero el servidor hace `get_object_or_404(QuizGuide, id=guide_id)` sin repetir
   la autorización de asociación (`apps/content/views/item_review.py:81-86`). Validar `is_active`
   y la relación con el tema o su asignatura antes de enviar contenido privado a la IA.

### P2 — importantes

1. **N+1 en servicio y panel.** `get_topic_education_level` carga recursos sin
   `select_related` y llama dos veces a `get_education_level()` por recurso
   (`apps/content/services/item_extraction_service.py:25-35`); el listado renderiza
   `resource_links`, cada `link.resource` y `get_unlinked_resources` por ítem sin prefetch
   (`apps/content/views/item_review.py:46,150,314` y
   `templates/partials/_item_row.html:69-103`). Usar `select_related("subject")`,
   `prefetch_related("resource_links__resource")` y una colección de recursos del tema compartida.
2. **IDs repetidos de recursos pueden abortar toda la transacción.**
   La persistencia usa `create()` por cada ID sugerido (`item_review.py:132-145`); una lista IA con
   duplicados viola `unique_item_resource`. Deduplicar o usar `get_or_create`/`bulk_create`
   controlado y cubrirlo con test.
3. **Edición acepta `level` y `difficulty` fuera de choices.**
   Se convierten/guardan sin comprobar las listas válidas (`item_review.py:181-197`). Reutilizar
   `Question.LEVEL_CHOICES` y `DIFFICULTY_CHOICES`, devolviendo 400 o re-render con error.
4. **Errores IA se vuelcan sin saneamiento/escape.**
   El servicio no importa ni aplica `_sanitize_key` y la vista interpola `str(e)` directamente en
   HTML (`item_extraction_service.py:75-82`; `item_review.py:84-90`). Sanear antes de log/respuesta
   y renderizar una plantilla o escapar el texto; no exponer detalles del proveedor al navegador.
5. **Pruebas insuficientes para los riesgos anteriores.**
   No existe test explícito de cero red mediante `patch` de ambos proveedores, flag apagado,
   guía ajena/inactiva, fusión entre temas, CSP del nuevo template, duplicados IA ni conteo de
   consultas. El test legacy confirma generación antigua, pero no impide mutaciones nuevas con el
   flag apagado.

### Barrera ejecutada

- `.venv\Scripts\python.exe manage.py test` → **425 tests, OK** en 267.357 s.
- `.venv\Scripts\python.exe manage.py check --deploy` → **exit 0**, 7 warnings de settings locales
  (`security.W004/W008/W009/W012/W016/W018/W020`), sin errores.
- `.venv\Scripts\python.exe manage.py makemigrations --check --dry-run` →
  **No changes detected**.
- `.venv\Scripts\pre-commit.exe run --all-files` → **todos los hooks Passed**.
- `git diff --check main...feat/guias-fase1-extraccion-items` → sin errores.

Nota de entorno: los tres primeros comandos con `python` global fallaron inicialmente porque ese
intérprete no tiene Django; se repitieron con el `.venv` canónico configurado por el proyecto.

## Respuesta de 🏛️ Claude a la auditoría — 2026-06-22 (cierre)

🔨 Antigravity no subió correcciones tras el rechazo (la rama seguía en el commit `2a4efa6`
auditado). Por decisión del 🧑, 🏛️ Claude tomó excepcionalmente el rol de builder y corrigió
**todos los P1 y P2**:

### P1 (bloqueantes) — corregidos
1. **Flag por tema gobierna todo.** Helpers `_get_enabled_topic` / `_get_enabled_item` (404 si el
   tema no está activo y con `structured_bank_enabled=True`). El selector inicial y `load_guides`/
   `list_items` solo aceptan temas habilitados; todas las mutaciones (propose/edit/status/merge/
   link/unlink) validan el flag. Regresión: `test_flag_disabled_blocks_panel_and_mutations`.
2. **Fusión solo dentro del mismo tema habilitado.** `merge_items` rechaza conjuntos con
   `topic_id` mixto (400) y exige que el tema tenga el flag. Test `test_merge_cross_topic_rejected`.
3. **CSP.** Se eliminó el `<script>` inline y el `onclick`; la lógica vive en
   `static/js/item-extraction.js` (cargado con `nonce` + `?v=1`), con `addEventListener` y
   `data-merge-url`. Test `test_template_has_no_inline_script_or_onclick`.
4. **`detected_exercise_count`.** Campo nuevo en `ExerciseItem` (migración aditiva **0034**),
   persistido en `propose_items`, mostrado en `_item_row.html` y editable en `_item_edit_row.html`;
   en la fusión se suma. Test `test_propose_items_dedupes_resources_and_stores_count`.
5. **Validación de guía.** `propose_items` exige guía `is_active` y asociada al tema o a su
   asignatura (mismo filtro que el selector) antes de mandar contenido a la IA.
   Test `test_foreign_or_inactive_guide_rejected`.

### P2 (importantes) — corregidos
1. **N+1.** `get_topic_education_level` usa `select_related("subject","topic__subject")` y calcula
   el nivel una sola vez por recurso; el listado usa `prefetch_related("resource_links__resource")`
   y calcula `unlinked_resources_list` en memoria (recursos del tema cargados una vez).
2. **Duplicados IA.** `propose_items` deduplica `suggested_resource_ids` y filtra IDs ajenos al tema
   antes de crear `ResourceExerciseItem` (no se aborta la transacción). Cubierto por test.
3. **Choices en edición.** `edit_item_inline` valida `level`/`difficulty` contra
   `Question.LEVEL_CHOICES`/`DIFFICULTY_CHOICES` → re-render con error y **400**.
   Test `test_edit_rejects_invalid_choices`.
4. **Saneamiento de llave.** El servicio importa y aplica `_sanitize_key` (y `raise … from None`);
   la vista ya no interpola `str(e)` en HTML: registra el detalle y muestra un mensaje genérico.
5. **Pruebas.** +7 tests (flag apagado, guía ajena/inactiva, fusión cruzada, CSP, cero-red con
   `patch` de ambos proveedores, duplicados IA + conteo, choices inválidos).

## Qué se hizo (cierre 🏛️ Claude — 2026-06-22)

Panel solo-admin (`/publicar/items/`) que, desde una guía privada (`QuizGuide`), propone ítems de
aprendizaje con IA (calibrando dificultad al nivel educativo del tema/recurso) y permite
editar / fusionar / aprobar / archivar, todo **detrás del flag `Topic.structured_bank_enabled`** y
sin tocar el banco legacy. Construyó 🔨 Antigravity; 🧩 Codex auditó y rechazó por 5 P1 + 5 P2;
🏛️ Claude (por decisión del 🧑, ante la falta de correcciones del builder) corrigió **todos** los
hallazgos y cerró.

- **Archivos:** `apps/content/models/exercise_item.py` (campo `detected_exercise_count` + métodos
  prefetch-friendly), migración aditiva `0034`, `apps/content/services/item_extraction_service.py`,
  `apps/content/views/item_review.py`, `apps/content/urls/publish_urls.py`,
  `apps/content/tests/test_item_extraction.py` (+7 tests), `static/js/item-extraction.js` (nuevo),
  `templates/pages/item_extraction.html`, `templates/partials/_item_row.html`,
  `templates/partials/_item_edit_row.html`, `templates/base.html`.
- **Barrera final (`.venv`):** `manage.py test` → **432 tests OK** (605 s) · `check --deploy` →
  exit 0 (7 warnings de settings locales) · `makemigrations --check --dry-run` → **No changes** ·
  `pre-commit run --all-files` → **todo Passed** · `git diff --check` → sin errores.
- **Sin tocar CSP/HTMX/KaTeX** (JS externo con nonce). **Sin borrar datos**; migración aditiva.

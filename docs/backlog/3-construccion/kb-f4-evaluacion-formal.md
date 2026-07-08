# F4 — Evaluación formal por recurso (espejo del motor de `Resource`, generada por IA)

- **Estado:** Handoff Ready — rediseñado y verificado contra código real (2026-07-08)
- **Creado:** 2026-06-26 · **Rediseñado:** 2026-07-08 (decisión del 🧑, ver abajo)
- **Prioridad:** P1 · **Cartera:** educativa · producto
- **Tipo:** infraestructura · producto
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción)
- **Requiere:** F2 completo (páginas del nodo, ✅), F3 completo (banco de ejercicios, ✅)

## Decisión del 🧑 (2026-07-08) — reemplaza el diseño anterior

El diseño original (`AssessmentExercise` balanceado por `exercise_type`, cargado a mano desde
admin) queda **descartado**. Nuevo alcance, cerrado explícitamente:

1. **Escala de 3 niveles nueva**, igual a la de `Resource`/`Question` (Definición · Ejercicios
   simples · Problemas de aplicación) — **independiente** de los 6 `ItemGroup` del banco de
   práctica (`comprender→evaluar`). No se tocan ni se mezclan.
2. **Solo modo evaluación** (no hay modo "preparación" separado para este banco). El banco de
   práctica visible (`NodeExercise`, ya publicado) sigue existiendo tal cual, **sin cambios**, en
   su propia sección de la página del recurso. La evaluación formal es una sección aparte.
3. **7 preguntas por nivel** (21 por recurso), generadas por IA a partir del contenido propio del
   nodo (no cargadas a mano).
4. Es un **espejo funcional** del sistema que ya corre en `/recursos/<slug>/` (`Question` +
   `Choice` + `QuizAttempt`, ver `apps/content/services/evaluation_service.py` y
   `apps/content/views/evaluation_views.py`), re-anclado a `KnowledgeNode` en vez de `Resource`.

## Objetivo

Cada recurso (nodo hoja) de `/aprender/` tiene, además de su banco de práctica visible, una
sección de **evaluación formal** con 3 niveles. Cada nivel se aprueba o no según un umbral de
aciertos sobre sus 7 preguntas (ocultas hasta enviar, generadas por IA). El resultado se traduce
en un indicador de dominio (estrellas 0-3) visible en la página del recurso.

## Fuentes a leer

- `apps/content/models/evaluation.py` — `QuizAttempt`, `QuizAttemptAnswer` (la forma a espejar)
- `apps/content/models/question.py` — `Question`, `Choice` (la forma a espejar)
- `apps/content/services/evaluation_service.py` — **el algoritmo a espejar**: `get_questions_for_quiz`,
  `get_next_attempt_number`, `get_attempts_info`, `submit_quiz`, `get_resource_mastery`
- `apps/content/views/evaluation_views.py` — vistas HTMX (`quiz_start`, `quiz_submit`, `quiz_status`)
- `apps/content/services/ai_generation_service.py` — `generate_questions_for_resource` y `_build_prompt`
  (la forma a adaptar para leer `NodeContent` en vez de campos de `Resource`)
- `apps/content/management/commands/generate_pending_questions.py` — comando a espejar
- `apps/content/models/knowledge.py` — `KnowledgeNode`, `NodeContent` (objetivo/introduccion/
  explicacion/procedimiento/ejemplos/resumen — insumo del prompt IA)
- `apps/content/models/node_bank.py` — `ItemGroup`, `NodeExercise` (el banco de práctica — **no
  tocar**, solo referenciar desde el mensaje de "repasa la práctica" al reprobar)
- `apps/learn/views.py`, `templates/learn/node_detail.html` — punto de integración de la nueva sección

## Por qué NO se comparte la tabla con `Question`/`QuizAttempt`

Se evaluó explícitamente reusar las mismas tablas (`Question`/`Choice`/`QuizAttempt`) para ambos
sistemas. Se descarta: `Question.resource` es FK duro a `Resource`; migrar a `GenericForeignKey`
tocaría tablas de producción en uso activo sin necesidad real (ambos "recursos" — `Resource` legacy
y `KnowledgeNode` nuevo — son conceptos distintos en el modelo de datos, aunque el algoritmo de
evaluación sea idéntico). Se opta por **espejar la forma y el algoritmo, no la tabla**: modelos
nuevos con la misma estructura que `Question`/`Choice`/`QuizAttempt`, y un servicio nuevo que replica
la lógica ya probada de `evaluation_service.py` en vez de generalizarla prematuramente (los dos
sistemas divergen en si existe o no modo "preparación"/recuperación — forzar una capa común
agregaría una abstracción que ninguno de los dos necesita hoy).

## Propuesta

### 1. Modelos nuevos en `apps/content/models/knowledge.py`

**`NodeAssessmentQuestion`** — espejo de `Question`, anclado a `KnowledgeNode`:

| Campo | Tipo | Notas |
|---|---|---|
| `node` | `FK(KnowledgeNode, related_name='assessment_questions')` | Solo `node_type='recurso'` |
| `level` | `PositiveSmallIntegerField(choices=[(1,'Definición'),(2,'Ejercicios simples'),(3,'Problemas de aplicación')])` | |
| `text` | `TextField` | Enunciado, puede contener KaTeX |
| `explanation` | `TextField(blank=True)` | Se muestra tras responder |
| `status` | `CharField(choices: borrador\|publicada\|archivada, default='borrador')` | Solo `publicada` entra al pool |
| `generation_key` | `CharField(max_length=64, blank=True)` | Idempotencia: evita duplicar en regeneración IA |
| `order` | `PositiveIntegerField(default=0)` | |
| `created_at` / `updated_at` | `DateTimeField` | |

**`NodeAssessmentChoice`** — espejo de `Choice`:

| Campo | Tipo | Notas |
|---|---|---|
| `question` | `FK(NodeAssessmentQuestion, related_name='choices')` | |
| `text` | `CharField(max_length=500)` | |
| `is_correct` | `BooleanField(default=False)` | |
| `order` | `PositiveIntegerField(default=0)` | |

**`NodeAssessmentAttempt`** — espejo de `QuizAttempt` (sin campo `mode`: siempre evaluación):

| Campo | Tipo | Notas |
|---|---|---|
| `user` | `FK(settings.AUTH_USER_MODEL, related_name='node_assessment_attempts')` | |
| `node` | `FK(KnowledgeNode, related_name='assessment_attempts')` | |
| `level` | `PositiveSmallIntegerField` | 1/2/3 |
| `score` | `PositiveSmallIntegerField` | Aciertos |
| `total` | `PositiveSmallIntegerField` | Siempre 7 (o menos si no hay pool suficiente) |
| `passed` | `BooleanField` | `score/total >= pass_threshold` (default 0.8, igual que `Resource`) |
| `attempt_number` | `PositiveSmallIntegerField` | Autoincremental por `(user, node, level)` |
| `created_at` | `DateTimeField(auto_now_add=True)` | |

Meta: `UniqueConstraint(['user','node','level','attempt_number'])`, `ordering=['-created_at']`

**`NodeAssessmentAnswer`** — espejo de `QuizAttemptAnswer`:

| Campo | Tipo | Notas |
|---|---|---|
| `attempt` | `FK(NodeAssessmentAttempt, related_name='answers')` | |
| `question` | `FK(NodeAssessmentQuestion, related_name='attempt_answers')` | |
| `selected_choice` | `FK(NodeAssessmentChoice, null=True, blank=True, on_delete=SET_NULL)` | |
| `is_correct` | `BooleanField` | |

Registrar los cuatro en `apps/content/models/__init__.py` y en `admin.py` (solo lectura de intentos;
CRUD normal de preguntas/alternativas para revisión editorial).

**Máximo de intentos / umbral:** reusar las constantes de `evaluation_service.py` como defaults
globales (`MAX_EVAL_ATTEMPTS = 3`, `pass_threshold = 0.8`) — **sin mecanismo de recuperación por
práctica en esta iteración** (no hay modo "preparación" que sirva de señal de recuperación; queda
como nota de Fase 2 más abajo, no bloquea este handoff).

### 2. Generación IA — comando nuevo

**`apps/content/management/commands/generate_node_assessment_questions.py`**, espejo de
`generate_pending_questions.py`:

- Input: un nodo hoja (o `--all` para recorrer todos los publicados sin banco de evaluación aún)
- Por cada nivel (1/2/3) sin 7 preguntas `publicada`: genera las que falten
- Prompt construido desde `NodeContent` del nodo (`objetivo`, `introduccion`, `explicacion`,
  `procedimiento`, `ejemplos`, `resumen`) + nombre del nodo + cadena de ancestros (asignatura/eje/
  bloque/tema), en vez de `resource.description`/`resource.content`/transcript como hace
  `_build_prompt` hoy — mismo patrón, distinta fuente de contexto
- Reusa el cliente Gemini y el manejo de `GEMINI_API_KEY`/mock-en-DEBUG ya existente en
  `ai_generation_service.py` (extraer la llamada HTTP + parseo JSON a un helper compartido si es
  directo; si no, duplicar el bloque de llamada — no vale la pena abstraer el resto del servicio)
- Preguntas nuevas quedan en `status='borrador'`; publicación es manual (mismo flujo editorial que
  el resto del banco de contenido) o vía un flag `--publish` explícito para el piloto
- Idempotente: `generation_key` evita duplicar si se re-corre

### 3. Vistas nuevas en `apps/learn/`

Mismo patrón HTMX que `evaluation_views.py`, sin modo "preparación":

- **`GET /aprender/…/<slug>/evaluar/<nivel>/`** (`login_required`) — arma el intento: si
  `max_reached` sin poder recuperar, bloquea (mensaje simple, sin recuperación en esta fase);
  si no, selecciona las preguntas `publicada` del nivel (máx. 7), guarda IDs en sesión
  (anti-tampering, igual que `quiz_start`), renderiza formulario con respuestas ocultas
- **`POST /aprender/…/<slug>/evaluar/<nivel>/`** — valida contra los IDs de sesión, califica,
  crea `NodeAssessmentAttempt` + `NodeAssessmentAnswer`, limpia sesión, muestra resultados con
  alternativa correcta y `explanation`
- **`GET /aprender/…/<slug>/evaluar/`** (o incluido directo en `node_detail.html`) — panel de
  estado de los 3 niveles + mastery (estrellas), igual a `quiz_status`/`_quiz_section_context`
- Reprobado → mensaje "Repasa la sección de práctica" con anchor a la sección `NodeExercise` ya
  existente en la misma página (no genera un link a otra URL)

### 4. Integración en `node_detail.html`

Nueva sección **separada** de la sección de práctica existente (no la reemplaza ni la reordena):
banco de práctica visible primero (como hoy), evaluación formal después, con su propio título
("Evaluación de dominio") y los 3 niveles como chips/tarjetas (bloqueado/disponible/aprobado),
mismo lenguaje visual que el panel `quiz_section.html` de `Resource` en lo posible.

## No-objetivos (esta iteración)

- No recuperación de intentos vía práctica (no hay modo preparación equivalente) — **Fase 2** si se
  decide más adelante ligarlo a completar el banco `NodeExercise`
- No examen final por bloque/tema (equivalente a `TopicEvaluationAttempt`) — fuera de alcance
- No actualizar ningún estado agregado de alumno más allá de `NodeAssessmentAttempt` (no hay F5 aún)
- No formatos `numerica`/`algebraica` en V1 — solo alternativa (igual que lo que realmente corre
  hoy en producción para `Resource`; los campos de `Question` para numérica/algebraica existen pero
  `submit_quiz` no los evalúa)
- No tocar `NodeExercise`/`ItemGroup` (banco de práctica) de ninguna forma

## Criterios de aceptación

- [ ] Barrera verde: `python manage.py test` · `check` · `makemigrations --check --dry-run`
- [ ] `generate_node_assessment_questions --node <semantic_id>` genera 7 preguntas por nivel (21
      total) en `status='borrador'`, idempotente (re-correr no duplica)
- [ ] `GET /aprender/…/evaluar/<nivel>/` → 302 a login si no está autenticado
- [ ] Con login y preguntas publicadas: formulario muestra hasta 7 preguntas del nivel, sin revelar
      la alternativa correcta
- [ ] `POST` califica correctamente, crea `NodeAssessmentAttempt` con `score`/`total`/`passed`
      correctos y `attempt_number` incremental por `(user, node, level)`
- [ ] Tercer intento fallido bloquea un cuarto (sin recuperación) con mensaje claro
- [ ] Mastery (estrellas) refleja niveles aprobados, visible en `node_detail.html`
- [ ] La sección de práctica (`NodeExercise`) no cambia en absoluto

## Plan de pruebas

- Unit: cálculo de `score`/`passed`, autoincremento de `attempt_number`, bloqueo al 4º intento
- Unit: comando de generación — idempotencia (`generation_key`), no genera de más si ya hay 7
- Integration: flujo completo GET → POST → resultado, con login requerido
- Smoke: piloto en un nodo real de Números Enteros con preguntas generadas por IA en local

## Riesgos / rollback

- Calidad de preguntas generadas por IA: requiere revisión editorial antes de publicar (`status`
  arranca en `borrador`, igual que el resto del pipeline de contenido)
- Si no hay 7 preguntas publicadas en un nivel, el intento corre con las disponibles (no falla)
- Costo/cuota de la API de generación (Gemini) — mismo límite que el resto del pipeline existente
- Rollback: revertir migraciones (tablas nuevas, sin FK a tablas críticas existentes)

## Qué se hizo

_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_

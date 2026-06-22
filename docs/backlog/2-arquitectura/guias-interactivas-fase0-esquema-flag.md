# Guías interactivas — Fase 0: esquema y flag por tema

- **Estado:** 🟢 Ready para construir (handoff de arquitectura)
- **Creado:** 2026-06-22 · **Epic padre:** `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`
- **Prioridad:** P1 · **Cartera:** educativa · **Tipo:** producto · infraestructura
- **Dueño:** 🧩 Codex (preflight) → 🔨 Antigravity (construye, rama `feat/guias-fase0-esquema`) → 🧩 Codex (audita) → 🏛️ Claude (cierre)

> **Alcance de esta fase: SOLO esquema + flag.** Modelos, migraciones aditivas, config por tema y
> exportaciones. **Sin UI, sin pipeline IA, sin lógica de evaluación, sin corrección.** Eso entra en
> las fases 1–7. El objetivo es dejar la base de datos lista y 100% retrocompatible.

## Objetivo (una frase)
Crear los modelos del sistema de banco estandarizado por ítems y el flag por tema, de forma
**aditiva** (ninguna pregunta histórica se altera; todos los temas siguen con el sistema actual
hasta activar el flag), para habilitar las fases siguientes.

## Fuentes a leer (rutas concretas)
- `apps/content/models/question.py` (Question + Choice — se amplía Question).
- `apps/content/models/evaluation.py` (QuizAttempt, QuizAttemptAnswer, TopicEvaluationAttempt — se amplía QuizAttemptAnswer).
- `apps/content/models/topic.py` (se amplía Topic con el flag).
- `apps/content/models/quiz_guide.py` (QuizGuide = fuente privada reutilizable; se vincula como fuente).
- `apps/content/models/__init__.py` (exportar los modelos nuevos).
- `apps/content/models/resource.py` (FK de cuotas y sesiones).

## Decisiones de diseño ya tomadas (del epic)
- Publicación manual **solo en el sistema nuevo**; el banco actual sigue publicando directo.
- Administración con **paneles propios in-app** (se construyen en fases ≥1, no aquí).
- La **fuente privada original** reutiliza `QuizGuide` (ya guarda `content_text`, `source_filename`,
  vínculos a tema/recursos e `is_active`). `LearningGuide` es la guía ProfeOnline **generada** (nueva).

## Propuesta — modelos (todos aditivos)

### 1. Flag + config por tema
- **`Topic.structured_bank_enabled`** — `BooleanField(default=False)`. Mientras sea `False`, el tema
  usa exactamente el sistema actual. (Migración aditiva con default → no toca filas existentes.)
- **`TopicBankConfig`** (OneToOne con Topic, `related_name="bank_config"`):
  - `level_eval_minutes` PositiveSmallInteger default **10**
  - `level_eval_attempts` PositiveSmallInteger default **3**
  - `final_minutes` PositiveSmallInteger default **45**
  - `final_attempts` PositiveSmallInteger default **2**
  - `final_distribution` JSONField default `{"conceptual": 20, "mecanico": 50, "aplicacion": 30}`
  - `network_tolerance_seconds` PositiveSmallInteger default **15**
  - `duration_tolerance_pct` PositiveSmallInteger default **10**
  - `created_at` / `updated_at`
  - (Se crea on-demand; no es obligatorio que todos los temas tengan una.)

### 2. `ExerciseItem` (ítem de aprendizaje)
- `topic` FK Topic `related_name="exercise_items"`
- `title` CharField(200)
- `level` PositiveSmallInteger choices `Question.LEVEL_CHOICES` (1/2/3)
- `difficulty` CharField choices `DIFFICULTY_CHOICES` (ver §5), blank default `""`
- `objective` TextField (objetivo)
- `recommendation` TextField blank (recomendación)
- `common_errors` TextField blank (errores frecuentes)
- `order` PositiveInteger default 0
- `status` CharField choices `propuesto/aprobado/archivado` default `propuesto`
- `learning_guide` FK LearningGuide null blank `related_name="items"` (guía generada de origen)
- `created_at` / `updated_at`
- Meta: `ordering = ["topic", "level", "order"]`

### 3. `ResourceExerciseItem` (ítem ↔ recurso, con cuotas)
- `exercise_item` FK ExerciseItem `related_name="resource_links"`
- `resource` FK Resource `related_name="exercise_item_links"`
- `practice_quota` PositiveSmallInteger default 0 (cuota de práctica)
- `evaluation_quota` PositiveSmallInteger default 0 (cuota de evaluación)
- `order` PositiveInteger default 0
- Meta: `UniqueConstraint(["exercise_item", "resource"])`

### 4. `LearningGuide` (guía ProfeOnline generada)
- `topic` FK Topic `related_name="learning_guides"`
- `title` CharField(200) · `slug` SlugField(unique, blank/null, auto como Topic.save)
- `structured_content` JSONField default dict (intro, resumen, fórmulas, ejemplos resueltos,
  ejercicios por ítem/dificultad, desafíos, solucionario — el render lo consume en fases ≥3)
- `resources` M2M Resource blank `related_name="learning_guides"`
- `private_sources` M2M QuizGuide blank `related_name="derived_guides"` (fuentes privadas utilizadas)
- `visibility` CharField choices `interna/publica` default `interna`
- `status` CharField choices `borrador/publicada` default `borrador`
- `created_at` / `updated_at`

### 5. Ampliar `Question` (campos nullable/con default → aditivo)
Nuevas `choices` compartidas:
- `QUESTION_TYPE_CHOICES = alternativa / numerica / algebraica`
- `DIFFICULTY_CHOICES = basica / intermedia / avanzada / desafio`
- `SCOPE_CHOICES = banco_visible / evaluacion_nivel / prueba_final`

Campos a agregar a `Question`:
- `exercise_item` FK ExerciseItem null blank `related_name="questions"`
- `question_type` CharField choices QUESTION_TYPE_CHOICES default `alternativa`
- `difficulty` CharField choices DIFFICULTY_CHOICES blank default `""`
- `canonical_answer` TextField blank (respuesta canónica para numérica/algebraica)
- `answer_tolerance` FloatField null blank (tolerancia numérica configurable)
- `hint` TextField blank (pista)
- `points` PositiveSmallInteger default 1 (puntaje)
- `estimated_minutes` PositiveSmallInteger default 0 (minutos estimados)
- `scope` CharField choices SCOPE_CHOICES **blank default `""`** ⚠️ (cadena vacía = **sin clasificar**;
  así el gate de Fase 7 detecta "cero publicadas sin clasificar" y el legacy NO entra solo)
- `learning_guide` FK LearningGuide null blank `related_name="bank_questions"`

> **Compatibilidad clave:** todos los campos nuevos tienen default o son nullable. Las ~2.500
> preguntas existentes quedan con `scope=""` (sin clasificar), `question_type="alternativa"`,
> sin ítem y sin guía → **no entran al sistema nuevo** (que requiere flag de tema + clasificación).

### 6. Ampliar `QuizAttemptAnswer`
- `text_answer` TextField blank (texto ingresado por el alumno en numéricas/algebraicas).
  (Aditivo; las respuestas existentes quedan con `""`.)

### 7. Sesiones de evaluación (solo tablas; la lógica es Fase 5)
- **`EvaluationSession`**:
  - `user` FK AUTH_USER_MODEL `related_name="evaluation_sessions"`
  - `topic` FK Topic `related_name="evaluation_sessions"`
  - `resource` FK Resource null blank (para evaluaciones por nivel)
  - `kind` CharField choices `evaluacion_nivel / prueba_final`
  - `level` PositiveSmallInteger null blank (para evaluación por nivel)
  - `attempt_number` PositiveSmallInteger
  - `started_at` DateTimeField · `expires_at` DateTimeField
  - `status` CharField choices `en_curso / enviada / vencida` default `en_curso`
  - `questions` M2M Question through **`EvaluationSessionQuestion`** (con `order`) — preguntas seleccionadas
  - `created_at`
  - Meta: `UniqueConstraint(["user","topic","kind","level","attempt_number"])`
- **`EvaluationSessionQuestion`** (through): `session` FK, `question` FK, `order` PositiveInteger.
- **`EvaluationSessionAnswer`** (respuestas detalladas, sirve nivel y final):
  - `session` FK EvaluationSession `related_name="answers"`
  - `question` FK Question
  - `selected_choice` FK Choice null blank (alternativa)
  - `text_answer` TextField blank (numérica/algebraica)
  - `is_correct` BooleanField default False
  - `points_awarded` FloatField default 0
  - Meta: `UniqueConstraint(["session","question"])`

### 8. Exportaciones
Registrar todos los modelos nuevos en `apps/content/models/__init__.py`.

## No-objetivos (FUERA de Fase 0)
- Cualquier UI/plantilla/panel admin. Cualquier endpoint o vista.
- Pipeline IA (extracción de ítems, generación de guía, validación de originalidad).
- Lógica de selección por cuotas, no-repetición, timers, corrección, dominio, PDF.
- Migrar/clasificar preguntas legacy (eso es Fase 7).
- Cambiar el comportamiento de cualquier tema con `structured_bank_enabled=False`.

## Criterios de aceptación (verificables)
- [ ] Barrera verde: `test` · `check` · `makemigrations --check --dry-run` (migración incluida).
- [ ] **Una sola migración aditiva**; `makemigrations --check` no pide más cambios.
- [ ] Ninguna pregunta histórica modificada: tras migrar, todas conservan datos y quedan
      `scope=""`, `question_type="alternativa"`, `exercise_item=NULL`.
- [ ] Con `structured_bank_enabled=False` (todos los temas tras migrar), el sitio se comporta
      idéntico (smoke: home, lista de recursos, detalle de recurso, quiz actual, evaluación de tema).
- [ ] `Topic.bank_config` accesible (OneToOne) con los defaults 10/3/45/2 y distribución 20/50/30.
- [ ] Modelos exportados en `__init__.py` e importables.
- [ ] `str()` razonable en cada modelo nuevo.

## Plan de pruebas
- **Modelos:** test de creación de cada modelo nuevo + constraints únicos (ResourceExerciseItem,
  EvaluationSession, EvaluationSessionAnswer) y defaults de `TopicBankConfig`.
- **Aditividad/legacy:** crear preguntas "estilo legacy" antes de aplicar (fixture), aplicar la
  migración en test y verificar `scope==""`, sin ítem, intactas.
- **Flag:** test de que `structured_bank_enabled` default False y que togglearlo no rompe selectores
  actuales (smoke de `get_ordered_resources` y del flujo de quiz existente).
- **Migración:** `makemigrations --check --dry-run` limpio en CI.

## Riesgos / rollback
- **Riesgo:** migración no aditiva o default faltante rompe filas existentes → mitigar con defaults
  explícitos y revisión del SQL (`sqlmigrate`).
- **Riesgo:** `scope` con default no-vacío clasificaría legacy por error → **debe** ser `default=""`.
- **Rollback:** los modelos son nuevos y los campos nullable; revertir = migración inversa
  (`migrate content <anterior>`). Sin pérdida de datos legacy.

---

## Qué se hizo
_(Completar al cerrar Fase 0.)_

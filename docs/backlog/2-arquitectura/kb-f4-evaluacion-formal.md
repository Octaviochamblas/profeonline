# F4 — Evaluación formal de dominio (piloto: 02.01 Números Enteros)

- **Estado:** Handoff — listo para preflight
- **Creado:** 2026-06-26
- **Prioridad:** P1 · **Cartera:** educativa · producto
- **Tipo:** infraestructura · producto
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción)
- **Requiere:** F2 completo (páginas del nodo), F3 completo (banco de ejercicios)

## Objetivo

Implementar la evaluación formal de dominio: banco de `AssessmentExercise` (respuesta oculta hasta
enviar), `NodeAssessmentRule` que define "dominio" como dato editable, flujo de evaluación UI con
login, y `AssessmentAttempt` que registra puntaje y qué tipos de ejercicio se fallaron.

## Fuentes a leer

- `docs/backlog/2-arquitectura/arquitectura-plataforma-conocimiento.md` §3 Capa 4
- `apps/content/models/evaluation.py` — `QuizAttempt`, `QuizAttemptAnswer` (base reutilizable)
- `apps/content/models/__init__.py` — `Question`, `Choice` (base para `AssessmentExercise`)
- `apps/content/models/knowledge.py` — `KnowledgeNode`, `NodePrerequisite` (de F1)
- `apps/learn/` — vistas y templates del nodo (de F2) — punto de integración

## Propuesta

### 1. Modelos nuevos en `apps/content/models/knowledge.py`

**`AssessmentExercise`** — ejercicios de evaluación formal. **Respuesta oculta hasta enviar.**
Son un pool distinto del banco (`BookExercise`): el alumno no los ha visto al practicar.

| Campo | Tipo | Notas |
|---|---|---|
| `node` | `FK(KnowledgeNode, related_name='assessment_exercises')` | Solo hojas |
| `exercise_type` | `CharField(max_length=60)` | Mismo vocabulario que `BookExercise` |
| `format` | `CharField(choices: alternativa\|numerica\|algebraica)` | |
| `enunciado` | `TextField` | Puede contener KaTeX |
| `choices` | `JSONField(default=list)` | `[{"texto":"...","es_correcta":bool}]` — solo si `format=alternativa` |
| `respuesta_canonica` | `CharField(max_length=200, blank=True)` | Solo si `format=numerica/algebraica` |
| `tolerancia` | `FloatField(default=0.0)` | Margen de error para respuestas numéricas |
| `solucion` | `TextField` | Mostrar SOLO después de enviar |
| `dificultad` | `CharField(choices: basica\|media\|avanzada)` | |
| `estado` | `CharField(choices: borrador\|publicado, default='borrador')` | |

**`NodeAssessmentRule`** — define "dominio" como dato, por nodo hoja:

| Campo | Tipo | Notas |
|---|---|---|
| `node` | `OneToOneField(KnowledgeNode, related_name='assessment_rule')` | |
| `min_score` | `FloatField(default=0.75)` | Porcentaje mínimo para aprobar (0.0–1.0) |
| `require_type_coverage` | `BooleanField(default=True)` | Debe cubrir todos los `exercise_type` |
| `num_questions` | `PositiveSmallIntegerField(default=10)` | Preguntas por evaluación |
| `attempt_cooldown_minutes` | `PositiveSmallIntegerField(default=0)` | Tiempo entre reintentos |

**`AssessmentAttempt`** — historial de evaluaciones formales:

| Campo | Tipo | Notas |
|---|---|---|
| `user` | `FK(settings.AUTH_USER_MODEL)` | |
| `node` | `FK(KnowledgeNode, related_name='assessment_attempts')` | |
| `score` | `FloatField` | Porcentaje de acierto (0.0–1.0) |
| `passed` | `BooleanField` | `score >= NodeAssessmentRule.min_score` |
| `failed_exercise_types` | `JSONField(default=list)` | Tipos que falló en este intento |
| `attempt_number` | `PositiveSmallIntegerField` | Autoincremental por `(user, node)` |
| `created_at` | `DateTimeField(auto_now_add=True)` | |

Meta: `UniqueConstraint(['user','node','attempt_number'])`, `ordering=['-created_at']`

Registrar los tres en `apps/content/models/__init__.py`.

### 2. Flujo de evaluación (vistas nuevas en `apps/learn/`)

**`GET /aprender/…/<slug>/evaluar/`** — formulario de evaluación (requiere login → redirect a login si no)

Lógica de selección de preguntas:
1. Obtener `NodeAssessmentRule` del nodo (si no existe: usar defaults)
2. Seleccionar `num_questions` `AssessmentExercise` publicados, balanceados por `exercise_type`
3. Si `require_type_coverage=True`: incluir al menos 1 pregunta por tipo disponible
4. Barajar el orden

El formulario muestra las preguntas sin revelar la respuesta.

**`POST /aprender/…/<slug>/evaluar/`** — procesa las respuestas:

1. Comparar cada respuesta con `respuesta_canonica` / `es_correcta`
2. Calcular `score = aciertos / total`
3. Calcular `failed_exercise_types` = tipos donde `aciertos_del_tipo / total_del_tipo < min_score`
4. Calcular `attempt_number` = `AssessmentAttempt.objects.filter(user=user,node=node).count() + 1`
5. Crear `AssessmentAttempt`
6. Redirect a pantalla de resultado
7. **No** actualiza `StudentNodeState` — eso es F5

**`GET /aprender/…/<slug>/evaluar/resultado/<attempt_id>/`** — pantalla de resultado:

- Puntaje alcanzado y umbral necesario
- "✓ Aprobado" o "✗ Reprobado"
- Solución de cada ejercicio (revelar ahora)
- Si reprobado: lista de `failed_exercise_types` con mensaje:
  _"Para mejorar en [nombre del tipo], repasa los ejercicios del banco"_ (enlace a sección banco)
- Botón "Intentar de nuevo" (respeta `attempt_cooldown_minutes`)

### 3. Admin

Registrar `AssessmentExercise`, `NodeAssessmentRule`, `AssessmentAttempt` en admin.

## No-objetivos

- No actualizar `StudentNodeState` (F5 — aquí solo se crea `AssessmentAttempt`)
- No emitir eventos de dominio (F5)
- No UI de prerrequisitos (F6)
- No evaluar nodos que no sean hojas (`node_type != 'recurso'`)
- No adaptar el generador IA de preguntas en este sprint (los ejercicios se cargan manualmente desde admin)

## Criterios de aceptación

- [ ] Barrera verde: `python manage.py test` · `check` · `makemigrations --check --dry-run`
- [ ] `GET /aprender/…/evaluar/` → 302 a login si no está autenticado
- [ ] Con login: formulario muestra N preguntas balanceadas por tipo, respuestas ocultas
- [ ] `POST` correcto crea `AssessmentAttempt` con `score` y `failed_exercise_types` correctos
- [ ] Pantalla de resultado muestra: puntaje, aprobó/reprobó, tipos a repasar, soluciones
- [ ] Segundo intento crea nuevo `AssessmentAttempt` con `attempt_number` incremental
- [ ] Si no hay `NodeAssessmentRule`, usa los defaults (no lanza 500)
- [ ] Tests: cálculo de `score`, cálculo de `failed_exercise_types`, autoincremento de `attempt_number`

## Plan de pruebas

- Unit: lógica de score, lógica de `failed_exercise_types`, selección balanceada de preguntas
- Integration: flujo completo GET → POST → resultado
- Smoke: evaluar el piloto en local con ejercicios reales cargados en admin

## Riesgos / rollback

- Si no hay suficientes `AssessmentExercise` para cubrir todos los tipos: la evaluación corre con los disponibles (no falla)
- Respuestas numéricas: la comparación con `tolerancia` debe manejar strings y floats cuidadosamente
- Rollback: revertir migraciones (tablas nuevas, sin FK a tablas existentes críticas)

---

## Qué se hizo

_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_

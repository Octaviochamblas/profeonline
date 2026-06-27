# F5 — Estado del alumno: StudentNodeState + mastery_service

- **Estado:** Handoff Ready — verificado contra código real (2026-06-26)
- **Creado:** 2026-06-26
- **Prioridad:** P1 · **Cartera:** producto · retención
- **Tipo:** infraestructura · producto
- **Dueño sugerido:** 🧩 Codex (preflight) → 🔨 Antigravity (construcción)
- **Requiere:** F4 completo (`AssessmentAttempt` en DB)

## Objetivo

Crear `StudentNodeState` (estado de dominio del alumno por nodo, basado exclusivamente en resultados
de evaluación formal), el `mastery_service` que lo actualiza tras cada intento, y la señal
`node_mastered` que la gamificación futura escuchará. El estado se refleja en la página del nodo.

## Fuentes a leer

- `docs/backlog/2-arquitectura/arquitectura-plataforma-conocimiento.md` §3 Capa 5 + §4 (contrato de desacople)
- `apps/content/models/knowledge.py` — `KnowledgeNode`, `AssessmentAttempt`, `NodeAssessmentRule`
- `apps/content/services/` (si existe) — convención de servicios del proyecto
- `apps/learn/views.py` — POST de evaluación (F4) — punto de integración con `mastery_service`
- `apps/content/models/gamification.py` — `XPEvent`/`UserSkill` (a NO tocar, solo entender para no colisionar)

## Propuesta

### 1. Modelo `StudentNodeState` (en `apps/content/models/knowledge.py`)

| Campo | Tipo | Notas |
|---|---|---|
| `user` | `FK(settings.AUTH_USER_MODEL, related_name='node_states')` | |
| `node` | `FK(KnowledgeNode, related_name='student_states')` | |
| `status` | `CharField(choices: no_iniciado\|en_progreso\|dominado, default='no_iniciado')` | |
| `mastery_score` | `FloatField(null=True)` | Mejor score alcanzado en evaluación formal |
| `passed` | `BooleanField(default=False)` | Aprobó según `NodeAssessmentRule.min_score` |
| `failed_exercise_types` | `JSONField(default=list)` | Tipos que falló en el último intento |
| `attempts` | `PositiveSmallIntegerField(default=0)` | Número de evaluaciones formales realizadas |
| `last_attempt_at` | `DateTimeField(null=True)` | |

Meta: `UniqueConstraint(['user', 'node'])`, `ordering = ['-last_attempt_at']`

Registrar en `apps/content/models/__init__.py`.

### 2. Señal `node_mastered` (en `apps/content/signals.py`)

```python
from django.dispatch import Signal

node_mastered = Signal()
# Kwargs al emitir: sender=KnowledgeNode, user=User, node=KnowledgeNode, score=float
```

Sin suscriptores en este sprint. La gamificación (F8) se conectará aquí. El dominio
**nunca importa** el módulo de gamificación — la conexión es unidireccional.

### 3. Servicio `apps/content/services/mastery_service.py`

```python
from django.db import transaction
from apps.content.models import StudentNodeState, AssessmentAttempt, KnowledgeNode
from apps.content.signals import node_mastered


def update_after_attempt(user, node: KnowledgeNode, attempt: AssessmentAttempt) -> StudentNodeState:
    with transaction.atomic():
        state, _ = StudentNodeState.objects.select_for_update().get_or_create(
            user=user, node=node
        )
        state.attempts += 1
        state.last_attempt_at = attempt.created_at
        state.failed_exercise_types = attempt.failed_exercise_types

        if attempt.score > (state.mastery_score or 0.0):
            state.mastery_score = attempt.score

        if attempt.passed:
            state.passed = True
            state.status = 'dominado'
        elif state.status == 'no_iniciado':
            state.status = 'en_progreso'

        state.save()

    if attempt.passed:
        node_mastered.send(
            sender=KnowledgeNode,
            user=user,
            node=node,
            score=attempt.score,
        )

    return state
```

> `select_for_update()` evita condición de carrera si el alumno envía dos evaluaciones simultáneas.
> La señal se emite **fuera** del bloque `atomic()` para que los suscriptores no queden dentro de
> la transacción del dominio.

### 4. Integración con F4

En la vista POST de evaluación (`apps/learn/views.py`), después de crear `AssessmentAttempt`:

```python
from apps.content.services import mastery_service

# ...después de crear attempt:
mastery_service.update_after_attempt(user=request.user, node=node, attempt=attempt)
```

### 5. Indicador de estado en la página del nodo (modificar template de F2)

Agregar para usuarios logueados, arriba del contenido o en un sidebar:

| `status` | Lo que ve el alumno |
|---|---|
| `no_iniciado` | (sin indicador, o invisible) |
| `en_progreso` | "Tu mejor puntaje: 60% — Tipos a repasar: [lista]" |
| `dominado` | "✓ Dominado (85%)" |

Sin login: no muestra indicador de estado (el contenido se ve igual).

## No-objetivos

- No implementar listeners de `node_mastered` (gamificación va en F8)
- No prerrequisitos UI (F6)
- No tracking de "vio el contenido" ni "practicó en el banco"
- No tocar `XPEvent`, `UserSkill`, `UserStreak` existentes

## Criterios de aceptación

- [ ] Barrera verde: `python manage.py test` · `check` · `makemigrations --check --dry-run`
- [ ] Evaluación aprobada → `StudentNodeState.status='dominado'`, `passed=True`
- [ ] Evaluación reprobada → `StudentNodeState.status='en_progreso'`, `failed_exercise_types` actualizado
- [ ] Mejor puntaje nunca baja (si pasa de 60% a 50%, `mastery_score` sigue en 60%)
- [ ] Página del nodo muestra indicador correcto para usuario logueado
- [ ] Sin login: sin indicador de estado (no rompe la página)
- [ ] Señal `node_mastered` se emite al aprobar (verificar con test de señal)
- [ ] `select_for_update`: dos intentos simultáneos no crean dos filas `StudentNodeState`
- [ ] Tests: `update_after_attempt` con aprobado, reprobado, múltiples intentos, mejor score se conserva

## Plan de pruebas

- Unit: `mastery_service.update_after_attempt` con distintos escenarios (aprobado, reprobado, mejora de score, no regresión)
- Signal test: receptor temporal que verifica que `node_mastered` se emite con los kwargs correctos
- Integration: flujo evaluación → `mastery_service` → indicador en página del nodo

## Riesgos / rollback

- La señal emitida fuera de la transacción: si el suscriptor futuro falla, no revierte el `StudentNodeState` (comportamiento correcto — el dominio no depende de la gamificación)
- Rollback: revertir migración (`StudentNodeState` tabla nueva); eliminar `signals.py` y la importación en el POST de evaluación

---

## Reutilización verificada (código real, 2026-06-26)

- **Análogo directo: `apps/content/services/structured_progress_service.py`.** Ya calcula el "dominio"
  de un alumno a partir de `EvaluationSession`, **aislado del legacy `QuizAttempt`** (mismo principio que
  buscamos). F5 **espeja este patrón** pero para `KnowledgeNode` + `AssessmentAttempt` → `StudentNodeState`.
- `apps/content/services/progress_service.py` (legacy, basado en `QuizAttempt`) queda como referencia,
  no se toca.
- **Señal `node_mastered`:** `django.dispatch.Signal` en un `apps/content/signals.py` nuevo. El
  `apps/content/services/gamification_service.py` **ya existe** y se conectará como **suscriptor** a futuro
  (capa 6) — el núcleo (capas 1–5) **nunca** importa gamificación.
- **Patrón de servicio:** seguir el estilo de los servicios existentes en `apps/content/services/`
  (funciones puras + `transaction.atomic`).

## Qué se hizo

_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_

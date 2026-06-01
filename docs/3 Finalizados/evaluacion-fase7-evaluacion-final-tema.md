# Evaluación gamificada · Fase 7 — Evaluación final por tema

- **Estado:** Finalizado (2026-05-31)
- **Creado:** 2026-05-31
- **Área:** Producto pedagógico / Gamificación
- **Origen:** Fase 7 de la épica `sistema-evaluacion-gamificada` (MVP Fases 1–6 ya entregado y
  en `3 Finalizados/`).
- **Prioridad:** Media-alta (es el siguiente escalón natural sobre el MVP de evaluación por
  recurso).

## Problema / Objetivo

El MVP evalúa **por recurso y nivel** (1/2/3, 5/5 para aprobar). Falta la capa de cierre por
**tema**: una evaluación final que compile el dominio del alumno sobre todos los recursos del
`Topic`, registre nota e intentos, y traduzca la aprobación en señal visual y recompensa.

## Propuesta

- Crear evaluación final asociada a `Topic` (modelo nuevo o reutilizar `Question` con un modo
  `evaluacion_tema`, ya previsto en el MVP).
- Tomar preguntas de los recursos del tema o preguntas específicas de tema.
- Guardar por intento: nota/porcentaje, número de intento, mejor nota, aprobado/no aprobado,
  fecha.
- Umbral de aprobación recomendado: **80%**.
- Al aprobar:
  - marcar el tema como aprobado y aplicar color verde en `topic_detail` / listados;
  - aumentar el brillo/resplandor del tema según la nota (sin volver la UI ruidosa);
  - desbloquear la **skill** del tema (engancha con Fase 8);
  - otorgar XP (engancha con Fase 8).
- UI en `topic_detail`: bloque de "Evaluación final del tema" con estado, mejor nota e intentos.

## Notas / Consideraciones

- El modo `evaluacion_tema` ya está contemplado en el modelado del MVP — revisar
  `apps/content/models/question.py` y `evaluation.py` antes de añadir modelos nuevos.
- Depende parcialmente de Fase 8 para XP/skills; se puede entregar primero la mecánica de
  nota/intentos/estado verde y conectar XP/skill cuando exista la Fase 8.
- Mantener accesibilidad: estado del tema no solo por color (texto + icono).
- Tests: nota/intentos persistidos, umbral 80%, transición de tema a aprobado, idempotencia de
  recompensas (no duplicar skill/XP al reaprobar).

---

## Qué se hizo

Implementado en la rama `feat/evaluacion-fase7-tema` (2026-05-31).

- **Modelo** `TopicEvaluationAttempt` (`apps/content/models/evaluation.py`): user, topic,
  score, total, percentage, passed, attempt_number, created_at. Migración
  `0018_topicevaluationattempt`.
- **Servicio** (`apps/content/services/evaluation_service.py`):
  - `get_topic_exam_questions` / `get_topic_exam_question_count`: compilan preguntas
    **publicadas** en modo `evaluacion`/`ambas` de los **recursos publicados** del tema, al azar,
    tope `TOPIC_EXAM_QUESTION_COUNT = 10`.
  - `submit_topic_exam`: califica, calcula porcentaje y aprueba con **≥80%**
    (`TOPIC_PASS_THRESHOLD`). Rechaza alternativas inyectadas de otra pregunta (misma defensa
    que el MVP). Devuelve `(attempt, results)` con feedback por pregunta.
  - `get_topic_exam_info`: mejor nota, intentos usados, aprobado y **brillo** (0-3) según la
    mejor nota (80-89 → 1, 90-99 → 2, 100 → 3).
- **Vistas HTMX** (`evaluation_views.py`): `topic_exam_start` y `topic_exam_submit`; URLs
  `temas/<slug>/evaluacion-final/` y `.../enviar/`.
- **UI** en `topic_detail`: sección "Evaluación final del tema" (intro, estado, botón
  rendir/reintentar/repetir, área HTMX), badge **"Tema dominado · N%"** en el hero y clases de
  brillo progresivo. Templates `topic_exam_section/form/results/empty.html`. CSS `.topic-exam*`
  + cache buster `?v=12`.
- **Admin**: `TopicEvaluationAttempt` read-only (no add/change), filtrable por aprobado/asignatura.
- **Tests** (`test_evaluation.py`, +17): compilación de preguntas, exclusión de
  borradores/preparación/otros temas, aprobado en umbral, fallo bajo umbral, rechazo de
  alternativa cruzada, mejor nota/brillo, incremento de intento, vistas (login, form, vacío,
  submit/aprueba, sin sesión activa, sección en detalle, badge dominado).

### Verificación

- `apps.content.tests.test_evaluation`: 54/54 OK.
- Suite completa: **141/141 OK**.
- `manage.py check`: sin issues · `makemigrations --check`: sin cambios.

### Pendiente / fuera de alcance

- **XP/skill al aprobar el tema** → Fase 8 (`evaluacion-fase8-xp-skills-rangos.md`): aquí quedó
  la mecánica de nota/intentos/estado verde; el enganche de XP y desbloqueo de skill se hará al
  implementar la Fase 8.
- El estado verde del hero se refleja al **recargar** tras aprobar por HTMX (los resultados ya
  muestran el aprobado en el momento).
- QA visual manual en navegador (flujo completo del examen de tema).

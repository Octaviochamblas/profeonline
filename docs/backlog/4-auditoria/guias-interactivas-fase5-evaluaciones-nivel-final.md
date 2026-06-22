# Guías interactivas — Fase 5: evaluaciones por nivel + prueba final

- **Estado:** 🟢 Preflight resuelto por 🏛️ Claude (2026-06-22) — Ready para construir (🔨 Antigravity)
- **Creado:** 2026-06-22 · **Epic padre:** `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`
- **Prioridad:** P1 · **Cartera:** educativa · **Tipo:** producto · pedagogía · **seguridad** (timers server-side)
- **Dueño:** 🧩 Codex (preflight) → 🔨 Antigravity (construye, rama `feat/guias-fase5-evaluaciones`) → 🧩 Codex (audita) → 🏛️ Claude (cierre)

> **Alcance: pools ocultos, ensamblado de evaluaciones, timers server-side y dominio académico.**
> Depende de Fase 4 (corrección de respuesta) y Fase 3 (banco). Es la fase con más reglas; **el
> preflight de Codex debe afinar cuotas, distribución y bordes antes de construir.**

## Objetivo (una frase)
Evaluaciones por nivel y una prueba final que usan **pools ocultos** con cuotas fijas por ítem, sin
repetir variantes hasta agotar el pool, con **temporizadores controlados por el servidor** y un
**dominio académico ponderado** que determina si el tema queda dominado.

## Fuentes a leer
- `apps/content/models/evaluation_session.py` — YA EXISTE: `EvaluationSession` (`user`, `topic`,
  `resource`, `kind`, `level`, `attempt_number`, `started_at`, `expires_at`, `status`, `questions`
  M2M vía `EvaluationSessionQuestion`) y `EvaluationSessionAnswer` (`selected_choice`, `text_answer`,
  `is_correct`, `points_awarded`).
- `apps/content/models/topic_bank_config.py` — YA EXISTE: `level_eval_minutes` (10), `level_eval_attempts`
  (3), `final_minutes` (45), `final_attempts` (2), `final_distribution` (JSON 20/50/30),
  `network_tolerance_seconds` (15), `duration_tolerance_pct` (±10).
- `apps/content/models/question.py` — `scope` (banco visible vs evaluación de nivel vs prueba final),
  `points`, `estimated_minutes`, `exercise_item`.
- `answer_grading_service` (Fase 4) y `progress_service` (dominio actual).

## Alcance de construcción (a afinar en preflight)
1. **Ensamblador** (`evaluation_assembly_service`): selecciona del pool oculto según `scope`,
   respetando cuotas por ítem (`ResourceExerciseItem.evaluation_quota`), **sin repetir** variante al
   mismo alumno hasta agotar el pool; **pool reservado distinto** para la final; distribución
   20/50/30 por puntaje en la final; duración estimada 45 min ±10% (suma de `estimated_minutes`).
2. **Sesiones + timers server-side:** crear `EvaluationSession` consume intento; `expires_at` server;
   al vencer, pendientes = incorrectas, con `network_tolerance_seconds` de gracia. Nada de confiar en
   el reloj del cliente.
3. **Corrección:** alternativas + respuesta directa (Fase 4); guarda `points_awarded`/`is_correct`.
4. **Dominio académico:** nivel = 60%, final = 40%; requeridas no rendidas = 0; **tema dominado solo
   si** promedio ponderado ≥ 80% **y** final ≥ 80%. Integrar con `progress_service`.

## Criterios de aceptación
- [ ] Barrera verde. Migraciones, si hay, aditivas.
- [ ] Cuotas por ítem + no-repetición hasta agotar pool + pool de la final separado.
- [ ] Distribución final 20/50/30 y duración 45±10% respetadas por el ensamblador.
- [ ] Timers **server-side**: intento consumido al iniciar, vencimiento marca pendientes incorrectas,
  15 s de tolerancia. Tests de expiración e intentos.
- [ ] Dominio 60/40 y condición de aprobación (≥80% y final ≥80%) verificados con tests.
- [ ] Banco visible (Fase 3) y legacy intactos; flag por tema gobierna todo.

## No-objetivos
- Exportación PDF (Fase 6); migración legacy + gate de activación + piloto (Fase 7).

## Riesgos / decisiones abiertas (resolver en preflight)
- Bordes de cuotas vs. tamaño real del pool (qué pasa si no alcanza para 3 evaluaciones → relación con
  el gate de Fase 7). Estrategia de no-repetición y reseteo de pool. Concurrencia de sesiones
  (`select_for_update`). Definir exactamente la fórmula de duración y el redondeo de la distribución.

## Preflight — 🏛️ Claude (2026-06-22)

Contrastado contra el código real (`evaluation_session.py`, `topic_bank_config.py`, `question.py`,
`exercise_item.py`, `visible_bank_service.py`, `progress_service.py`).

### Hueco de alcance resuelto (decisión 🧑: incluir en Fase 5)
- `visible_bank_service` **hardcodea `scope="banco_visible"`**; no existe generación para
  `evaluacion_nivel`/`prueba_final`. **Fase 5 incluye** generar ambos pools: generalizar
  `generate_visible_bank_questions` con `scope` parametrizable (o servicio hermano
  `evaluation_bank_service`) reutilizando `generate_question_candidates`, persistiendo en borrador con
  el `scope` destino, y **panel editorial por `evaluation_quota`** (paralelo al de práctica de Fase 3).
  Publicación manual con la validación por tipo de Fase 4 (`validate_direct_answer_config`).

### Contradicciones del handoff resueltas
1. **`final_distribution` → `level`.** `{conceptual,mecanico,aplicacion}` no es un campo; mapear
   `conceptual→N1`, `mecanico→N2`, `aplicacion→N3`. La distribución 20/50/30 es proporción del
   **puntaje total** de la final por nivel; redondeo por **mayor-resto**; si el pool de un nivel no
   alcanza, completar desde otros niveles y registrar el desvío (relación con gate de Fase 7).
2. **Timer ≠ duración estimada.**
   - **Autoridad:** `expires_at = started_at + config.{level_eval_minutes|final_minutes}` (cronómetro
     y corte duro, 100% server-side).
   - **Cota de ensamblado:** `sum(estimated_minutes)` dentro de `final_minutes ± duration_tolerance_pct`.
   - **Exigir `estimated_minutes > 0`** al publicar preguntas de pool (default 0 rompería la cota).
3. **Intento + concurrencia.** `attempt_number = max(previos)+1` en `transaction.atomic` +
   `select_for_update`; unique `(user,topic,kind,level,attempt_number)` como backstop (capturar
   `IntegrityError` y reintentar). **Una sola sesión `en_curso`** por `(user,topic,kind,level)`: si hay
   una vencida, finalizarla *lazy* antes de un intento nuevo; validar tope `*_attempts` antes de crear.

### Decisiones fijadas
- **No-repetición:** excluir IDs ya usados en sesiones previas del mismo `(user,topic,kind[,level])`;
  si los no-vistos no alcanzan → **resetear** (repetir pool completo), no fallar. Conecta con el gate
  de suficiencia de pool de Fase 7.
- **`finalize_session` idempotente** (`update_or_create` sobre `unique_session_answer`): corrige lo
  respondido (alternativa por `is_correct`; numérica/algebraica vía `answer_grading_service.grade_answer`,
  `points_awarded = points` si correcta), marca **toda** pregunta no respondida como incorrecta (0 pts),
  fija `status` = `enviada` (en tiempo) o `vencida` (pasado `expires_at + network_tolerance_seconds`).
  Se invoca al enviar **y** lazy al abrir una `en_curso` ya vencida. Gracia = `network_tolerance_seconds`.
- **Aislamiento:** el ensamblador filtra `scope ∈ {evaluacion_nivel|prueba_final}`, excluye
  `""`/`banco_visible`; todo gobernado por `structured_bank_enabled`. Legacy/banco visible intactos.
- **Dominio académico (decisión 🧑: ÚLTIMO intento):** función **nueva y separada** (no tocar el
  `progress_service` legacy de `QuizAttempt`), solo para temas con el flag.
  - score de nivel = promedio de los recursos de ese nivel usando su **último** intento de evaluación
    de nivel (recurso sin evaluación rendida = 0);
  - ponderado = 60% (promedio de niveles) + 40% (último intento de la final);
  - **dominado ⟺ ponderado ≥ 80% Y final ≥ 80%**; requeridas no rendidas = 0.

### Migraciones
- **Ninguna esperada** (esquema completo desde Fase 0). La validación `estimated_minutes>0` es de
  aplicación, no de modelo. Si surge algún campo, **aditivo**.

### Criterios de aceptación añadidos
- [ ] Generación + edición + publicación de pools `evaluacion_nivel` y `prueba_final` por
  `evaluation_quota`, con validación por tipo (Fase 4) y `estimated_minutes>0`.
- [ ] Una sola sesión `en_curso` por `(user,topic,kind,level)`; intento consumido en transacción.
- [ ] `finalize_session` idempotente y lazy; tests de envío, expiración+gracia y reintentos.
- [ ] Dominio por último intento (60/40, ≥80% y final ≥80%) con tests, sin tocar progreso legacy.

**Veredicto: Listo para construir** en `feat/guias-fase5-evaluaciones` (🔨 Antigravity → 🧩 Codex
audita → 🏛️ Claude cierra). Tarjeta movida a `backlog/3-construccion/`.

## Construcción — 🧩 Codex (2026-06-22)

- Generación editorial de pools `evaluacion_nivel` y `prueba_final`, reutilizando el servicio IA
  existente, cuotas de evaluación, borradores y publicación manual validada.
- Ensamblado por cuotas, scopes estrictos, no-repetición hasta agotar el pool, distribución final
  20/50/30 por puntos y control de duración estimada.
- Sesiones transaccionales con intento consumido al iniciar, una sesión activa por clave, timer
  server-side, tolerancia de red y finalización idempotente de alternativas/respuesta directa.
- Dominio estructurado separado del progreso legacy: últimos intentos, faltantes en cero, ponderación
  60/40 y gate simultáneo de 80% ponderado + 80% final.
- UI editorial y del alumno mediante HTMX, reproductor reutilizado y contador externo compatible
  con CSP.
- Barrera: `manage.py test` **502 OK (1 skip)**; `check --deploy` exit 0 con 7 warnings locales
  conocidos; `makemigrations --check --dry-run` sin cambios; pre-commit y diff-check verdes.

**Estado:** construcción terminada; pasa a auditoría independiente. No mergear desde esta etapa.

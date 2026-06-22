# Guías interactivas — Fase 5: evaluaciones por nivel + prueba final

- **Estado:** 🟡 Handoff de arquitectura (afinar en preflight de Codex antes de construir)
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

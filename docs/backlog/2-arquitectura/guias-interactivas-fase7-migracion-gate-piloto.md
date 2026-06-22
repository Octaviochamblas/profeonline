# Guías interactivas — Fase 7: migración legacy + gate de activación + piloto

- **Estado:** 🟡 Handoff de arquitectura (afinar en preflight; depende de Fases 2–5)
- **Creado:** 2026-06-22 · **Epic padre:** `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`
- **Prioridad:** P1 · **Cartera:** educativa · **Tipo:** producto · datos
- **Dueño:** 🧩 Codex (preflight) → 🔨 Antigravity (construye, rama `feat/guias-fase7-gate-piloto`) → 🧩 Codex (audita) → 🏛️ Claude (cierre)

> **Alcance: clasificar las preguntas antiguas, un gate de activación verificable y encender el piloto
> en UN tema.** Es la fase que finalmente **activa** el flag en producción para un tema, una vez que
> todo lo anterior está completo. **Nunca borra datos** (archiva).

## Objetivo (una frase)
Clasificar manualmente las ~2.500 preguntas antiguas por ítem y ámbito, y exigir que un **gate de
activación** verifique cobertura completa antes de encender `Topic.structured_bank_enabled` en el
tema piloto.

## Fuentes a leer
- `apps/content/models/question.py` — `scope` (vacío = legacy sin clasificar), `exercise_item`,
  `difficulty`; el modo `ambas` legacy NO entra automáticamente.
- `apps/content/models/exercise_item.py` / `ResourceExerciseItem` (cuotas), `topic_bank_config.py`
  (distribución/duración), `learning_guide.py`.
- Panel de ítems (Fase 1) y de evaluaciones (Fase 5) para reusar selectores/validaciones.

## Alcance de construcción
1. **Clasificación legacy (panel admin):** asignar cada pregunta antigua a un ítem y un `scope`
   (banco visible / nivel / final); **duplicar** si sirve a varios ámbitos o **archivar** (nunca
   `.delete()`). Las de modo `ambas` requieren clasificación explícita (no entran solas).
2. **Gate de activación** (`activation_gate_service` + vista): verifica para el tema —
   - todos los ítems **aprobados**;
   - ejercicios visibles completos por ítem;
   - **reserva suficiente para 3 evaluaciones** sin repetir;
   - cuotas válidas; distribución final 20/50/30 factible; duración estimada dentro de rango;
   - **cero preguntas publicadas sin clasificar** (`scope=""`).
   Devuelve checklist con lo que falta; **solo si todo pasa** permite activar el flag.
3. **Encender el piloto** en **un** tema (activar `structured_bank_enabled` vía el gate, no a mano).

## Criterios de aceptación
- [ ] Barrera verde. Migraciones, si hay, aditivas; **ninguna pregunta histórica borrada** (archivar).
- [ ] Clasificación no destructiva; `ambas` no entra sin clasificar.
- [ ] El gate bloquea la activación si falta cualquier verificación; la habilita solo con todo completo.
- [ ] Tras activar el piloto: el alumno ve banco/guía/evaluaciones del tema; los demás temas intactos.
- [ ] Tests del gate (cada condición que falla bloquea) y de la clasificación (duplicar/archivar).

## No-objetivos
- Activar más de un tema en esta fase; tocar temas fuera del piloto.

## Riesgos / rollback
- **Datos:** trabajar sobre copias/archivado; respaldo antes de clasificar en prod.
- **Rollback:** apagar el flag del tema restaura el sistema actual (todo siguió detrás del flag).
- Volumen (~2.500 preguntas): clasificar a cuentagotas; medir N+1 en el panel.

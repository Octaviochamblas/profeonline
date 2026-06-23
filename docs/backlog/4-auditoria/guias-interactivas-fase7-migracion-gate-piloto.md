# Guías interactivas — Fase 7: migración legacy + gate de activación + piloto

- **Estado:** 🟡 Preflight + construcción por 🏛️ Claude (2026-06-23) → ESPERANDO AUDITOR DISTINTO (🧩 Codex) · ⚠️ `seguridad:requiere-claude`
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

## Preflight + construcción — 🏛️ Claude (2026-06-23)

Contrastado contra el código real. **Decisión del 🧑: modelo de COEXISTENCIA** — el gate verifica
que el contenido estructurado (F1–F5) esté completo; **no** exige retirar el banco legacy (`scope=""`)
ni clasificar/archivar las ~2.500 preguntas. Las capas ya están aisladas por `scope`. Activación
100% reversible.

### Decisión técnica resuelta: staging (huevo-y-gallina)
Los paneles editoriales usaban `_get_enabled_topic`, que exige el flag YA encendido. Para preparar el
tema **antes** de exponerlo se agregó **`Topic.structured_bank_staging`** (migración aditiva `0036`) y
la propiedad **`Topic.structured_bank_editable` = `enabled OR staging`**. Los guards **admin** pasaron a
`editable`; las vistas de **alumno** siguen exigiendo `enabled` (el staging no expone nada).

### Qué se construyó (rama `feat/guias-fase7-gate-piloto`)
- **Modelo:** `structured_bank_staging` (BooleanField, default False) + propiedad `structured_bank_editable`.
  Migración **0036** aditiva.
- **Guards admin → `editable`** (sin tocar lo de alumno): `item_review` (`_get_enabled_topic/item`,
  lista de temas, `edit_evaluation_quota`), `question_review._visible_bank_mutation_error` + panel +
  acciones en lote, `visible_bank_service` (generación; `select_visible_practice_questions` queda en
  `enabled` por ser de alumno), `evaluation_assembly_service._base_pool`, `learning_guide_review`
  (lista + 5 guards).
- **Gate (`activation_gate_service.evaluate_topic_gate`)**, solo-lectura, reusa los ensambladores
  reales (dry-run). Checklist: configuración presente · todos los ítems aprobados (ninguno
  "propuesto") · guía pública · banco visible completo por ítem · cuotas de evaluación · reserva de
  nivel y final ≥ `intentos × cuota` (sin repetir) · prueba final y evaluaciones de nivel **armables**
  (distribución/duración factibles).
- **Activación (`structured_activation.py` + URLs)** admin-only, CSP-safe (HTMX, sin JS inline):
  `set_staging` (marcar/quitar preparación), `activate_structured_bank` (corre el gate; **solo si
  `ok` enciende el flag**, si no devuelve 400 con el checklist), `deactivate_structured_bank`
  (rollback: apaga el flag y vuelve a staging), `activation_panel` (render del checklist).
- **UI:** sección "Activación del banco (piloto)" en `item_extraction.html` + partial
  `_activation_gate.html` (se carga con el `topicChanged` existente).
- **Tests (`test_activation_gate.py`, 9):** gate pasa con tema completo; bloquea por ítem no aprobado,
  sin guía, banco visible incompleto y reserva insuficiente; activar enciende el flag; activar con
  gate fallido → 400 sin encender; rollback; staging habilita el panel admin pero **oculta al alumno**
  (guía 404).

### Barrera
- `manage.py test` → en verificación (ver reporte). `check --deploy` exit 0 (7 warnings locales).
- `makemigrations --check --dry-run` → `No changes detected` (la `0036` coincide). Migración **aditiva**.
- **Ninguna pregunta histórica tocada** (coexistencia).

### Pendiente
- **Auditoría de una IA distinta al builder (🧩 Codex)** — yo (🏛️ Claude) hice preflight + build.
  Toca el flag de producción → `seguridad:requiere-claude`, auto-merge deshabilitado. El cierre lo
  hace una IA distinta.
- **Operativo del 🧑:** elegir el tema piloto, prepararlo (staging), poblar banco/evaluaciones a
  cuentagotas y activar vía el gate.

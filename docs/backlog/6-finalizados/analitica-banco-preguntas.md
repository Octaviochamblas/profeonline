# Analítica del banco: cobertura, efectividad y resultados por alumno

- **Estado:** ✅ Auditado y cerrado por 🏛️ Claude (2026-06-18) — mergeado en PR #69
- **Creado:** 2026-06-17 · **Construido:** 2026-06-18 (🧩 Codex) · **Auditado/cerrado:** 2026-06-18 (🏛️ Claude)
- **Prioridad:** P2 · **Cartera:** educativa / producto
- **Dueño:** 🧩 Codex construye → 🏛️ Claude audita y cierra

## Objetivo

Exponer, sin modelos ni migraciones nuevas, tres vistas de solo lectura sobre los datos existentes:

1. Resumen de cobertura por Área → Asignatura → Tema → Recurso.
2. Efectividad de cada pregunta dentro de la revisión del banco.
3. Resultados e intentos agrupables por alumno o recurso/tema.
4. Efectividad ponderada filtrable por alumno individual o grupo ad hoc seleccionado.

## Preflight Codex

- Related names confirmados: `quiz_attempts`, `topic_eval_attempts`, `answers`,
  `attempt_answers`, `topics`, `resources` y `choices`.
- Permiso elegido: `is_admin` (superusuario), coherente con el resto del banco.
- Las preguntas legacy `mode="ambas"` cuentan en práctica y evaluación, como el runtime real.
- Las rutas estáticas `resumen/` y `resultados/` deben ir antes de `<slug:slug>/`.
- Anti-N+1: cobertura en una consulta anotada; item analysis en dos consultas fijas
  (preguntas + alternativas anotadas).

## Criterios de aceptación

- [x] Barrera verde: suite completa · `check --deploy` · sin migraciones.
- [x] Las páginas nuevas rechazan usuarios que no sean superusuarios.
- [x] Cobertura muestra fuentes, publicadas/borradores, pools, mostradas, faltantes y estado.
- [x] Filtros client-side por área/asignatura/tema/título actualizan métricas sin violar CSP.
- [x] Resultados combina `QuizAttempt` y `TopicEvaluationAttempt`, con filtros y agregados.
- [x] Revisión muestra respuestas, acierto, distribución y alertas por pregunta.
- [x] Tests de consultas acotan A a 1 query y C a 2 queries, independientemente del volumen.
- [x] Efectividad global permite seleccionar uno o varios alumnos y agrega
      Tema → Recurso → Pregunta, comparando contra el promedio global.
- [x] La jerarquía completa de efectividad usa 4 consultas constantes.
- [x] CSS/JS externos con cache-buster.

## Qué se hizo

- **Pieza A:** nueva ruta `/publicar/preguntas/resumen/`, tabla jerárquica, fuentes disponibles,
  objetivos efectivos desde `get_quiz_config`, métricas y filtros en cascada.
- **Pieza C:** anotaciones de respuestas/aciertos y prefetch anotado de alternativas en
  `question_review`; alertas por baja/alta efectividad y distractor dominante.
- **Pieza B:** nueva ruta `/publicar/preguntas/resultados/`, detalle unificado de intentos,
  filtros y resumen por alumno o por contenido.
- **Ampliación de efectividad:** nueva ruta `/publicar/preguntas/efectividad/`; selector con
  búsqueda y checkboxes para alumno individual o grupo ad hoc; tasa ponderada, respuestas,
  alumnos únicos, tamaño de muestra y comparación contra el global por tema/recurso/pregunta.
- **Navegación:** enlaces staff “Resumen del Banco”, “Resultados” y “Efectividad”.
- **Pruebas:** 10 tests de analítica; regresión `test_quiz_config` y suite completa verdes.
- **QA visual:** cobertura, filtros, resultados e item analysis revisados localmente; sin errores
  de consola ni overflow horizontal. Selector individual verificado con comparación global.

## Auditoría final (🏛️ Claude, 2026-06-18)

Revisión completa del diff (17 archivos, +2097/−16) contra `main` y los criterios de la tarjeta.

**Verificado OK:**
- **Matemática:** tasa de acierto (`correct/answers`), ponderada global (38,6% = 32/83 en QA),
  delta grupo-vs-global (Ada 50% vs global 25% → +25 pp), promedios y % aprobación de resultados.
  Grupo seleccionado vs "todos": **no mezclan denominadores** (el grupo filtra por `attempt__user`,
  el global usa el mismo *base* sin filtro de usuario). Sin alumnos → grupo = global → delta 0.
- **N+1 / consultas:** confirmados los límites — cobertura **1** (`assertNumQueries(1)` con 2 recursos,
  vía `select_related("quiz_config")` + anotaciones), item analysis **2**, efectividad jerárquica **4**.
- **Permisos/PII/CSP/HTML/a11y:** todas las vistas `@user_passes_test(is_admin)` (test rechaza staff
  no-superusuario); sin PII extra; JS externo con `nonce` + cache-buster, sin handlers inline; partial
  con `aria-label`; sin overflow horizontal ni errores de consola en las 4 páginas.
- **Casos nulos:** recurso sin tema/asignatura (fallback a `topic.subject`/`None`), preguntas sin
  respuestas (`accuracy=None` → "Sin datos"), `transcript` `TextField(default="")` (sin `.strip()` sobre None).
- **Orden de rutas:** `resumen/`, `resultados/`, `efectividad/` antes de `<slug:slug>/` ✓.
- **Evaluación final de tema:** fuera de la efectividad por pregunta (no genera `QuizAttemptAnswer`);
  cubierto con test de regresión.

**Hallazgo corregido (🏛️ Claude):**
- **Parámetros GET inválidos** (`?area=abc`, `?user=foo`, `?resource=xyz`) provocaban un **500**
  (`ValueError` al castear a `_id`) en `bank_results` y `bank_effectiveness`. **Fix:** helper
  `_clean_id()` que normaliza cada filtro a string numérico o `""` (se ignora), conservando el tipo
  para los `<select>`. **+3 tests de regresión** (resultados, efectividad, exclusión de eval de tema).

**QA visual** (4 superficies, logueado como superusuario): cobertura (filtros en cascada + totales en
vivo), resultados (tablas + filtros, GET inválido → 200), efectividad (selector de grupo + comparación
global, GET inválido → 200), item analysis (distribución + banderas de baja/alta efectividad y
distractor dominante). Sin errores.

## Evidencia de barrera

- `python manage.py test` → **317 tests OK** (tras integrar PR #68).
- `python manage.py makemigrations --check --dry-run` → **No changes detected**.
- `python manage.py check --deploy --fail-level ERROR --settings=config.settings.production`
  → **sin errores**; advertencias conocidas de Redis/HSTS usando variables locales ficticias.

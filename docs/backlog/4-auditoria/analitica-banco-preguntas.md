# Analítica del banco: cobertura, efectividad y resultados por alumno

- **Estado:** Construcción terminada — pendiente auditoría/cierre 🏛️ Claude
- **Creado:** 2026-06-17 · **Construido:** 2026-06-18
- **Prioridad:** P2 · **Cartera:** educativa / producto
- **Dueño:** 🧩 Codex construye → 🏛️ Claude audita y cierra

## Objetivo

Exponer, sin modelos ni migraciones nuevas, tres vistas de solo lectura sobre los datos existentes:

1. Resumen de cobertura por Área → Asignatura → Tema → Recurso.
2. Efectividad de cada pregunta dentro de la revisión del banco.
3. Resultados e intentos agrupables por alumno o recurso/tema.

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
- [x] CSS/JS externos con cache-buster.

## Qué se hizo

- **Pieza A:** nueva ruta `/publicar/preguntas/resumen/`, tabla jerárquica, fuentes disponibles,
  objetivos efectivos desde `get_quiz_config`, métricas y filtros en cascada.
- **Pieza C:** anotaciones de respuestas/aciertos y prefetch anotado de alternativas en
  `question_review`; alertas por baja/alta efectividad y distractor dominante.
- **Pieza B:** nueva ruta `/publicar/preguntas/resultados/`, detalle unificado de intentos,
  filtros y resumen por alumno o por contenido.
- **Navegación:** enlaces staff “Resumen del Banco” y “Resultados”.
- **Pruebas:** 7 tests nuevos; regresión `test_quiz_config` (19) y suite completa (301) verdes.
- **QA visual:** cobertura, filtros, resultados e item analysis revisados localmente; sin errores
  de consola ni overflow horizontal.

## Evidencia de barrera

- `python manage.py test` → **301 tests OK**.
- `python manage.py makemigrations --check --dry-run` → **No changes detected**.
- `python manage.py check --deploy --fail-level ERROR --settings=config.settings.production`
  → **sin errores**; advertencias conocidas de Redis/HSTS usando variables locales ficticias.

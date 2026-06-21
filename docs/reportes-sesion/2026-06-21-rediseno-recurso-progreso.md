# Reporte de sesión — 2026-06-21 · Rediseño de recurso y progreso académico

## Avances desde el último reporte

- **Reproductor de preguntas a pantalla completa** cerrado y desplegado (ver
  `2026-06-21-reproductor-preguntas.md`).
- **Rediseño de la vista de recurso + progreso académico** construido en la rama
  `feat/recurso-progreso-academico` (tarjeta creada y movida por el pipeline).

## Qué se hizo

Rediseño de la vista de recurso (más legible, menos "cajas dentro de cajas") y reemplazo de la
acción manual "Comprendido" por un **progreso calculado desde los intentos reales**.

- **Motor de progreso** (`progress_service.py`): promedio de los últimos 3 intentos por modo,
  ponderado **30/70** por nivel, progreso de recurso sobre niveles trabajados, estados
  **Preparado** (práctica ≥80%) y **Aprobado** (histórico, persiste si el promedio baja).
- **Selectores sin N+1**: `get_available_levels_map`, `get_recent_attempts_by_resource` (1 query).
  Los agregados de tema (`get_topics_progress_map`) usan progreso ponderado, ya no
  `ResourceCompletion`.
- **Vista de recurso**: enlace discreto al tema, título primero, metadatos compactos, descripción
  con `Ver más/menos`, columna legible; **sin barra "Comprendido"**.
- **Bloque único "Practica y evalúa tu aprendizaje"** con pestañas por nivel
  (Conceptos/Ejercicios/Problemas), acciones Practicar/Evaluarme con promedio reciente y estados,
  progreso del nivel; reusa el reproductor a pantalla completa.
- **Perfil ampliado**: panel por tema/recurso (ponderado, niveles trabajados, promedios recientes,
  últimos 3 por modo, estados; "Comprendido anteriormente" solo aquí).
- **JS** `resource-detail.js` CSP-safe (pestañas ARIA con teclado + Ver más/menos).
- 🧩 **Auditoría Codex:** se corrigieron tres hallazgos antes del cierre:
  - disponibilidad independiente por modo para no ofrecer cuestionarios vacíos;
  - cobertura del perfil contra todos los recursos publicados del tema;
  - pestañas móviles en cuadrícula de tres columnas, sin scroll horizontal.

## Decisiones importantes

- El significado de la barra de progreso del **tema** cambia: de "% comprendido" (manual) a
  **progreso ponderado** promediado sobre los recursos trabajados, con cobertura "X de N trabajados".
- "Comprendido" se conserva como **historial** (endpoint + `ResourceCompletion`), pero se retira de
  la UI salvo en el panel histórico del perfil.
- Sin migraciones, sin endpoints nuevos; reglas de aprobación, límites de intentos y reproductor
  intactos.

## Estado del proyecto / notas

- Barrera: **96 tests focalizados OK**, **391 tests completos OK**, `check` OK,
  `check --deploy` sin errores (warnings esperados de desarrollo),
  `makemigrations --check --dry-run` sin cambios y `git diff --check` OK.
- QA visual a **320, 360 y 390 px**: pestañas completas, sin overflow; acción por modo correcta.
- Reproductor verificado a pantalla completa: raíz y panel ocupan todo el viewport.

## Pendientes / Próximos pasos

- PR **#75** abierto hacia `main`; auditoría final y squash-merge por 🏛️ Claude.
- Opcional: QA con teclado/lector de pantalla de pestañas y "Ver más".

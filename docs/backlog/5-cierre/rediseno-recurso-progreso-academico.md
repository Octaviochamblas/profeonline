# Rediseño móvil del recurso y progreso académico

- **Estado:** Auditoría Codex aprobada — listo para cierre
- **Creado:** 2026-06-21
- **Prioridad:** P1  ·  **Cartera:** producto / educativa
- **Tipo:** producto
- **Dueño sugerido:** 🏛️ Claude
- **PR:** #75 — `feat/recurso-progreso-academico` → `main`

## Objetivo (una frase)
Rediseñar la vista de recurso (más legible y sin "cajas dentro de cajas", título protagonista,
descripción resumida, bloque único de práctica/evaluación con pestañas) y reemplazar la acción
manual "Comprendido" por un **progreso académico calculado desde los intentos reales** de práctica y
evaluación, visible en el recurso y en el perfil.

## Fuentes a leer (rutas concretas)
- `templates/pages/resource_detail.html` · `templates/includes/quiz_section.html`.
- `apps/content/views/resource_detail.py` · `apps/content/views/topic_detail.py`.
- `apps/content/services/evaluation_service.py` (`get_resource_mastery`, `get_attempts_info`).
- `apps/content/selectors/evaluation_selectors.py` (`get_resource_progress_map`,
  `get_topics_progress_map`, `get_topic_evaluation_summary`).
- `apps/content/models/evaluation.py` (`QuizAttempt`: score/total/level/mode/passed/created_at).
- `apps/content/models/completion.py` (`ResourceCompletion`, `ResourceView`).
- `apps/content/views/resource_completion.py` + `templates/includes/completion_button.html`.
- `templates/includes/resume_card.html` · `apps/content/selectors/resource_selectors.py`
  (`get_resume_resource`).
- `accounts/views.py` (`profile_view`) · `templates/accounts/profile.html`.
- Plantillas que muestran % / Comprendido: `topic_detail.html`, `topic_list`, `subject_detail`,
  `level_detail`, `home`, `resource_list`.
- `static/css/estilos.css` (cache-buster, actual `?v=30`).

## Propuesta
### Experiencia (vista de recurso)
- Breadcrumb a una línea secundaria, omitiendo el recurso actual; "Volver a recursos" → enlace
  discreto al tema.
- Título primero (mayor tamaño/contraste); asignatura/tema/nivel como metadatos compactos debajo.
- Descripción limitada a 3 líneas con `Ver más/Ver menos`.
- Eliminar la barra `Ir a ejercitación / Ir a evaluación / Comprendido`.
- En móvil, quitar bordes/paddings anidados; columna legible, mayor interlineado.

### Práctica y evaluación (bloque único)
- Título `Practica y evalúa tu aprendizaje`; pestañas `1 Conceptos`, `2 Ejercicios`, `3 Problemas`.
- Al elegir nivel → acciones `Practicar` y `Evaluarme`, cada una con su promedio reciente y estado.
- Selección inicial: primer nivel disponible no aprobado; si todos aprobados, el disponible más alto.
- Mantener el **reproductor de preguntas a pantalla completa** existente.
- Niveles sin preguntas no se muestran ni penalizan.

### Cálculo del progreso
- `promedio = media de los % de los últimos 3 intentos` (con 1–2 intentos, los disponibles).
- `progreso_nivel = práctica × 30% + evaluación × 70%` (modo sin intentos aporta 0).
- `progreso_recurso = promedio de los niveles con algún intento`.
- Niveles no trabajados se excluyen del %, pero se muestra cobertura `X de N niveles trabajados`.
- Estados históricos separados: `Preparado` (práctica ≥80%) y `Aprobado` (algún intento aprobó,
  persiste aunque el promedio reciente baje).

### Progreso personal e historial
- En el recurso: resumen compacto del nivel seleccionado + progreso general.
- En `Mi perfil`: panel por tema y recurso (progreso ponderado, niveles trabajados, promedios
  recientes práctica/evaluación, últimos 3 intentos por modo, estados Preparado/Aprobado).
- Conservar `ResourceCompletion` y su historial; "Comprendido anteriormente" solo en el panel
  histórico del perfil. Retirar "Comprendido" de recursos, tarjetas, barras de tema y reanudación.
- Agregados de tema dejan de depender de `ResourceCompletion` → usan el nuevo progreso ponderado.

### Implementación técnica
- Selectores agregados para los últimos 3 intentos por usuario/recurso/nivel/modo **sin N+1**.
- Extender el contrato de progreso con `practice_average`, `evaluation_average`,
  `weighted_progress`, `practice_ready`, `passed`, `worked_levels`, `available_levels`.
- Reutilizar `QuizAttempt`; **sin migraciones**. Mantener endpoints, reglas de aprobación, límites
  de intentos y reproductor actuales.
- JS externo CSP-safe para pestañas y expansión de descripción (teclado + ARIA).
- Mantener el endpoint de "Comprendido" por compatibilidad, sin exponerlo en la UI.

## No-objetivos (qué queda FUERA)
- Cambiar reglas de aprobación, límites de intentos o el reproductor.
- Migraciones o nuevos modelos.
- Eliminar `ResourceCompletion` o su endpoint.

## Criterios de aceptación (verificables)
- [x] Barrera verde: `test` · `check` · `makemigrations --check --dry-run`.
- [x] Vista de recurso rediseñada (título primero, metadatos compactos, descripción con Ver más/menos,
      bloque único con pestañas) y sin barra "Comprendido".
- [x] Progreso ponderado 30/70 correcto; niveles no trabajados excluidos + cobertura `X de N`.
- [x] Promedios = media de los últimos 3 intentos (0/1/2/3/+ intentos).
- [x] `Aprobado` histórico persiste aunque el promedio reciente baje.
- [x] Niveles sin preguntas no se muestran ni penalizan.
- [x] "Comprendido" retirado de la UI (recurso/tarjetas/tema/reanudación); endpoint+modelo intactos;
      "Comprendido anteriormente" solo en perfil.
- [x] Agregados de tema usan progreso ponderado.
- [x] Selectores en lote con control de consultas (sin N+1).
- [x] Pestañas y descripción accesibles (teclado + ARIA), JS CSP-safe.
- [x] CSS con cache-buster `?v=N` subido.

## Plan de pruebas
- Promedios con 0/1/2/3/+ intentos; selección exacta de los 3 más recientes.
- Ponderación 30/70 y exclusión de niveles no trabajados.
- Promedio reciente descendente sin perder `Aprobado`.
- Recursos con niveles sin preguntas.
- Selectores en lote con `assertNumQueries`.
- Navegación por teclado y ARIA de pestañas/descripción.
- QA móvil 360–390 px (título, video, contenido, selector sin columnas estrechas).
- Regresión: reproductor, bloqueo de evaluaciones, perfil, tema y listado de recursos.

## Riesgos / rollback
- Riesgo de cambiar el significado de las barras de progreso de tema (de "comprendido" a ponderado):
  documentar en el reporte. Sin migraciones → rollback = revertir commits.
- CSP: JS de pestañas/descripción debe ir externo con `nonce`.

---

## Qué se hizo
**Implementado en la rama `feat/recurso-progreso-academico` (🏛️ Claude).**

- **Motor de progreso** (`apps/content/services/progress_service.py`): promedios de los últimos 3
  intentos por modo, ponderado 30/70 por nivel, progreso de recurso sobre niveles trabajados,
  estados `practice_ready` (Preparado) y `passed` (Aprobado histórico), `select_initial_level`,
  `get_resources_progress`/`get_resource_progress` y `get_profile_progress` (perfil).
- **Selectores sin N+1** (`evaluation_selectors.py`): `get_available_levels_map`,
  `get_recent_attempts_by_resource` (1 query). `get_topics_progress_map` ahora usa progreso
  ponderado (ya no `ResourceCompletion`); expone `weighted_progress`/`worked`.
- **Vista de recurso** (`resource_detail.html` + view): enlace discreto al tema, título primero,
  metadatos compactos, descripción con `Ver más/menos`, columna legible; **sin barra "Comprendido"**.
  Fix de overflow horizontal en móvil (`grid-template-columns: minmax(0,1fr)`).
- **Bloque único** (`quiz_section.html`): "Practica y evalúa tu aprendizaje" con pestañas por nivel,
  acciones Practicar/Evaluarme con promedio reciente + estados, progreso del nivel; reusa el
  reproductor a pantalla completa. `_quiz_section_context` inyecta el progreso (refresco al cerrar).
- **JS** `static/js/resource-detail.js` (CSP-safe): pestañas ARIA con teclado + `Ver más/menos`
  (solo si hay desborde); se reengancha tras swaps de HTMX.
- **Perfil** (`accounts/views.py` + `includes/profile_progress.html`): panel por tema/recurso con
  progreso ponderado, niveles trabajados, promedios recientes y últimos 3 por modo, estados
  Preparado/Aprobado y "Comprendido anteriormente".
- **"Comprendido" retirado de la UI** (recurso, tarjetas/barras de tema, reanudación); el endpoint
  `resource_toggle_completion` y `ResourceCompletion` se conservan (historial). Agregados de tema
  usan progreso ponderado.
- **CSS** nuevo (cache-buster final `?v=33`).

### Correcciones de auditoría Codex
- **P1 — disponibilidad por modo:** el contrato distingue `practice_available` y
  `evaluation_available`; la UI oculta la acción inexistente y muestra un estado informativo.
- **P2 — cobertura del perfil:** `X de N` usa ahora todos los recursos publicados del tema como
  denominador, aunque el detalle siga limitado a recursos con actividad/historial.
- **P3 — pestañas móviles:** cuadrícula de tres columnas sin scroll horizontal, con objetivos
  táctiles de 44 px. Cache-buster actualizado a `?v=33`.

### Verificación
- Tests focalizados: **96 OK** (`test_progress`, `test_evaluation`, `test_completion`,
  `test_visibilidad`). Suite completa: **391 OK**.
- `check` OK · `check --deploy` sin errores (7 warnings esperados de settings locales) ·
  `makemigrations --check --dry-run` sin cambios · `git diff --check` OK.
- **QA visual real** con runserver a 320, 360 y 390 px: tres pestañas visibles sin overflow;
  modo inexistente sin botón; reproductor abierto a pantalla completa (viewport completo).

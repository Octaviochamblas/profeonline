# Rediseño móvil del recurso y progreso académico

- **Estado:** Por iniciar
- **Creado:** 2026-06-21
- **Prioridad:** P1  ·  **Cartera:** producto / educativa
- **Tipo:** producto
- **Dueño sugerido:** 🏛️ Claude

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
- [ ] Barrera verde: `test` · `check` · `makemigrations --check --dry-run`.
- [ ] Vista de recurso rediseñada (título primero, metadatos compactos, descripción con Ver más/menos,
      bloque único con pestañas) y sin barra "Comprendido".
- [ ] Progreso ponderado 30/70 correcto; niveles no trabajados excluidos + cobertura `X de N`.
- [ ] Promedios = media de los últimos 3 intentos (0/1/2/3/+ intentos).
- [ ] `Aprobado` histórico persiste aunque el promedio reciente baje.
- [ ] Niveles sin preguntas no se muestran ni penalizan.
- [ ] "Comprendido" retirado de la UI (recurso/tarjetas/tema/reanudación); endpoint+modelo intactos;
      "Comprendido anteriormente" solo en perfil.
- [ ] Agregados de tema usan progreso ponderado.
- [ ] Selectores en lote con control de consultas (sin N+1).
- [ ] Pestañas y descripción accesibles (teclado + ARIA), JS CSP-safe.
- [ ] CSS con cache-buster `?v=N` subido.

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
_(Completar al cerrar, antes de mover a `backlog/6-finalizados/`.)_

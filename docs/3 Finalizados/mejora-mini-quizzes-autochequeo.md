# Mini-quizzes de autochequeo al final de cada recurso

- **Estado:** Finalizado (entregado por la épica de evaluación gamificada, no como tarjeta propia)
- **Creado:** 2026-05-31
- **Área:** Producto (pedagógico)
- **Prioridad:** 🟡 Media-alta (gran diferenciador de aprendizaje)
- **Depende de:** `sistema-evaluacion-gamificada.md`

## Problema / Objetivo

Hoy un recurso es "consumir y marcar como completado" (`ResourceCompletion`). No hay forma de
que el estudiante **compruebe si entendió**. Esta tarjeta queda como el **MVP inicial** de la
épica `sistema-evaluacion-gamificada.md`: empezar por evaluación de recurso con selección
múltiple y feedback, antes de implementar todo el sistema de XP, skills, preparación y
evaluación final de tema.

Objetivo: añadir preguntas de autochequeo/evaluación al final de un recurso, con feedback
inmediato, persistencia de intentos y estado visual de dominio.

## Diagnóstico / contexto técnico

- Ya existe `apps/content/models/completion.py` (`ResourceCompletion`) y `ResourceView` —
  base para enganchar "quiz aprobado → sugerir marcar completado".
- HTMX ya está integrado (`static/js/htmx.min.js`), ideal para validar respuestas sin
  recargar y mostrar feedback inline (igual que el botón de completado).
- El detalle vive en `templates/pages/resource_detail.html` y
  `apps/content/views/resource_detail.py`.

## Decisiones de diseño tomadas desde la épica

- **Sí se guarda el resultado.** Los intentos alimentan progreso, estrellas y bloqueo.
- **Tipo de pregunta inicial:** selección múltiple con 1 correcta.
- **Aprobación:** 5/5 correctas.
- **Intentos:** 3 intentos por nivel; si falla, debe practicar con 80% para recuperar 1 intento.
- **Reportes:** cada pregunta debe permitir reportar error; se guarda en admin y se envía email.
- **Autoría:** staff desde admin; preguntas generadas por IA quedan como borrador.

## Ruta de trabajo

### Fase 1 — Modelado de datos mínimo
- Modelo de pregunta/alternativa para recurso, con nivel 1/2/3, modo y estado.
- Modelo de intento con usuario, recurso, nivel, puntaje, aprobado, número de intento y fecha.
- Modelo de reporte de error por pregunta.
- Mantener compatibilidad con `ResourceView` y `ResourceCompletion`.

### Fase 2 — Autoría (staff)
- Inline en el admin para crear preguntas/opciones por recurso.
- (Opcional) integración en el formulario de recurso existente.

### Fase 3 — Render y validación (estudiante)
- Sección "Demuestra lo aprendido" al final de `resource_detail.html`.
- Envío de respuestas vía HTMX → vista que valida y responde con feedback inline
  (correcto/incorrecto + explicación), reusando patrón del botón de completado.
- Estilos coherentes con los tokens del sitio (verde acierto, rojo error, ya existen).

### Fase 4 — Integración con progreso
- Al aprobar nivel 1/2/3, actualizar estrellas y estado visual del recurso.
- Mostrar badge amarillo "Visto" si solo existe `ResourceView`.
- Mostrar verde + estrellas si existe evaluación aprobada.
- Bloquear evaluación tras 3 intentos fallidos.
- Conectar recuperación de intento a práctica con 80% correcto.

### Fase 5 — Tests
- Tests de modelos, validación de respuestas y vista HTMX (siguiendo `apps/content/tests/`).

## Criterios de aceptación

- El staff puede crear preguntas de opción múltiple por recurso desde el admin.
- El estudiante responde y recibe feedback inmediato sin recargar (HTMX).
- Aprobar el quiz se refleja en el estado visual del recurso.
- La evaluación exige 5/5 para aprobar.
- Tras 3 fallos, la evaluación se bloquea hasta practicar con 80%.
- Cada pregunta permite reportar errores.
- Suite de tests cubre creación, validación y casos límite; todo verde.

## Notas / Consideraciones

- Mantener el MVP simple: opción múltiple + feedback + persistencia de intentos.
- La épica completa vive en `sistema-evaluacion-gamificada.md`.
- Accesibilidad: las preguntas deben ser navegables por teclado y anunciadas por lector
  (coordinar con `auditoria-accesibilidad-axe.md`).

---

## Qué se hizo

Esta tarjeta era el **MVP inicial** de la épica `sistema-evaluacion-gamificada.md`, y quedó
**100% cubierta por la implementación de esa épica** (no se ejecutó como tarjeta independiente).
Todos sus criterios de aceptación están entregados y en producción:

- Staff crea preguntas de opción múltiple por recurso desde el admin (`QuestionAdmin`,
  `ChoiceInline`).
- El estudiante responde con feedback inmediato por HTMX (`quiz_section.html`, `submit_quiz`).
- Aprobar se refleja en el estado visual del recurso (badges Visto/Comprendido/Aprobado +
  estrellas).
- Umbral 5/5 para aprobar; 3 intentos por nivel; recuperación con práctica ≥80%.
- Reporte de errores por pregunta (`QuestionErrorReport`) hacia admin + email.
- Preguntas IA nacen como `borrador` (Fase 9), nunca auto-publicadas.
- Cobertura de tests: `test_evaluation.py`, `test_completion.py`, `test_visibilidad.py` (verdes).

**Referencias:** `3 Finalizados/sistema-evaluacion-gamificada.md` (MVP Fases 1–6),
`evaluacion-fase7/8/9-*.md` y `visibilidad-ejercitacion-evaluacion-progreso.md`. Se cierra y
archiva por trazabilidad; **no requiere trabajo adicional**.

# Mini-quizzes de autochequeo al final de cada recurso

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Producto (pedagógico)
- **Prioridad:** 🟡 Media-alta (gran diferenciador de aprendizaje)

## Problema / Objetivo

Hoy un recurso es "consumir y marcar como completado" (`ResourceCompletion`). No hay forma de
que el estudiante **compruebe si entendió**. Un mini-quiz de autochequeo al final de cada
recurso convierte la plataforma de "lista de videos/guías" en una herramienta de aprendizaje
activo (modelo Khan Academy, en línea con el trabajo previo de recursos completados).

Objetivo: añadir preguntas de autochequeo (opción múltiple) al final de un recurso, con
feedback inmediato, sin necesariamente calificar ni guardar nota.

## Diagnóstico / contexto técnico

- Ya existe `apps/content/models/completion.py` (`ResourceCompletion`) y `ResourceView` —
  base para enganchar "quiz aprobado → sugerir marcar completado".
- HTMX ya está integrado (`static/js/htmx.min.js`), ideal para validar respuestas sin
  recargar y mostrar feedback inline (igual que el botón de completado).
- El detalle vive en `templates/pages/resource_detail.html` y
  `apps/content/views/resource_detail.py`.

## Decisiones de diseño abiertas

- **¿Se guarda el resultado?** Mínimo viable: autochequeo efímero (no persiste). Evolución:
  guardar intento/acierto para alimentar el progreso.
- **Tipos de pregunta:** empezar solo con **opción múltiple** (1 correcta). Más adelante:
  verdadero/falso, múltiples correctas, respuesta numérica.
- **Quién crea las preguntas:** el staff, desde el admin o el formulario de recurso.

## Ruta de trabajo

### Fase 1 — Modelado de datos
- Modelo `QuizQuestion` (FK a `Resource`, enunciado, orden, explicación opcional).
- Modelo `QuizChoice` (FK a `QuizQuestion`, texto, `is_correct`).
- (Opcional) `QuizAttempt` si se decide persistir resultados.
- Migraciones + registro en admin con inlines (pregunta → opciones).

### Fase 2 — Autoría (staff)
- Inline en el admin para crear preguntas/opciones por recurso.
- (Opcional) integración en el formulario de recurso existente.

### Fase 3 — Render y validación (estudiante)
- Sección "Pon a prueba lo aprendido" al final de `resource_detail.html`.
- Envío de respuestas vía HTMX → vista que valida y responde con feedback inline
  (correcto/incorrecto + explicación), reusando patrón del botón de completado.
- Estilos coherentes con los tokens del sitio (verde acierto, rojo error, ya existen).

### Fase 4 — Integración con progreso
- Al aprobar el quiz, sugerir/auto-marcar `ResourceCompletion`.
- Mostrar estado del quiz en la tarjeta de recurso si aplica.

### Fase 5 — Tests
- Tests de modelos, validación de respuestas y vista HTMX (siguiendo `apps/content/tests/`).

## Criterios de aceptación

- El staff puede crear preguntas de opción múltiple por recurso desde el admin.
- El estudiante responde y recibe feedback inmediato sin recargar (HTMX).
- Aprobar el quiz se refleja en el progreso del tema.
- Suite de tests cubre creación, validación y casos límite; todo verde.

## Notas / Consideraciones

- Mantener el MVP simple: opción múltiple + feedback. No construir un motor de exámenes.
- Accesibilidad: las preguntas deben ser navegables por teclado y anunciadas por lector
  (coordinar con `auditoria-accesibilidad-axe.md`).

---

## Qué se hizo
_(Completar al finalizar, antes de mover a "3 Finalizados".)_

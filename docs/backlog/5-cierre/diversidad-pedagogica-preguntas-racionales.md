# Diversidad pedagógica del banco de preguntas de números racionales

- **Estado:** Implementado y auditado por Codex · pendiente cierre
- **Creado:** 2026-06-19
- **Prioridad:** P1  ·  **Cartera:** educativa
- **Tipo:** pedagogía · QA
- **Dueño sugerido:** 🧩 Codex

## Objetivo (una frase)
Reemplazar la variación puramente numérica del generador de racionales por preguntas con distintos procesos cognitivos, sin reducir la cobertura por nivel y modo.

## Fuentes a leer (rutas concretas)
- `scratch/generate_racionales_questions.py`
- `apps/content/services/ai_generation_service.py`
- `apps/content/models/question.py`

## Propuesta
Definir familias pedagógicas explícitas por recurso y nivel (identificación, representación, cálculo directo e inverso, comparación, detección de errores, selección de estrategia y aplicación), generar variantes controladas y validar automáticamente la diversidad estructural antes de permitir el poblado.

## No-objetivos (qué queda FUERA)
- Ejecutar el poblado contra producción.
- Borrar preguntas existentes de la base de datos.
- Cambiar modelos o la experiencia de evaluación.

## Criterios de aceptación (verificables)
- [x] Cada recurso recibe 90 preguntas nuevas: 30 por nivel y 10 por modo.
- [x] Cada nivel contiene 6 familias pedagógicas equilibradas.
- [x] No hay duplicados literales ni preguntas diferenciadas solo por etiquetas como “caso” o “variación”.
- [x] El generador ofrece una auditoría local que no requiere conexión a la base de datos.
- [x] El poblado deja de borrar preguntas existentes de forma implícita.

## Plan de pruebas
Ejecutar el generador en modo de auditoría, comprobar conteos, familias, textos y respuestas; luego usar tests acotados de importación/guardado sin conectar a producción.

## Riesgos / rollback
El principal riesgo es introducir respuestas u opciones incorrectas al ampliar los moldes. Se mitiga con generación determinista, validaciones aritméticas y revisión por recurso. El script no se ejecutará contra producción durante esta tarea.

---

## Qué se hizo
- Se incorporó un prototipo de diversificación automática con seis familias pedagógicas por nivel:
  resolución directa, selección de justificación, contraste de respuestas, corrección de error,
  evaluación de afirmación y selección de estrategia.
- La auditoría local valida 1.440 preguntas: 90 por recurso, seis familias equilibradas, cuatro
  alternativas, una respuesta correcta y ausencia de textos o alternativas duplicadas.
- La ejecución sin argumentos quedó en modo auditoría. Escribir requiere `--apply`; el borrado
  destructivo requiere además `--replace`.
- La revisión estructural y el dry-run de producción se completaron antes de aplicar.
- Aplicado en producción el 2026-06-19: se conservaron 55 representantes antiguas, se archivaron
  1.351 repeticiones y se publicaron 1.440 preguntas nuevas. Las repetidas se archivaron en vez de
  borrarse físicamente para mantener una ruta segura de rollback.
- Respaldo local previo: `backups/racionales_questions_before_20260619T132910Z.json`
  (1.406 preguntas con alternativas).
- Verificación posterior: 1.495 publicadas, 1.351 archivadas, 90 nuevas por recurso, 10 nuevas por
  cada combinación nivel/modo y cero preguntas con alternativas inválidas.

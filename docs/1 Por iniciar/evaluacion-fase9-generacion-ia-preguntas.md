# Evaluación gamificada · Fase 9 — Generación asistida de preguntas por IA

- **Estado:** Por iniciar
- **Creado:** 2026-05-31
- **Área:** Producto pedagógico / Contenido / IA
- **Origen:** Fase 9 de la épica `sistema-evaluacion-gamificada` (MVP Fases 1–6 ya entregado y
  en `3 Finalizados/`).
- **Prioridad:** Media (acelera el llenado del banco de preguntas, pero el staff ya puede
  crearlas a mano desde el admin con el MVP).

## Problema / Objetivo

El banco de preguntas se carga **a mano** desde el admin. Para escalar la cobertura por recurso
y nivel conviene una **generación asistida por IA** que proponga preguntas, alternativas,
respuesta correcta y explicación breve, **siempre con revisión humana antes de publicar**.

## Propuesta

- A partir de: título del recurso, contenido escrito, transcripción del video (si existe), nivel
  educativo y objetivo de aprendizaje, generar borradores de `Question` + `Choice`.
- Las preguntas generadas quedan en estado **`borrador`** (ya soportado por el modelo del MVP);
  **nunca** se publican automáticamente.
- Flujo de revisión en el admin: el staff edita/aprueba y recién ahí pasa a `publicada`.
- Posible comando de management o acción de admin que dispare la generación por recurso/nivel.

## Notas / Consideraciones

- El modelo ya tiene estados `borrador/publicada/archivada` — esta fase solo añade el productor
  de borradores, no cambia el esquema.
- Definir proveedor/modelo y manejo de credenciales (alinear con la economía de tokens del
  proyecto y settings de prod).
- Riesgo pedagógico: validar que la IA no fije respuestas incorrectas; la revisión humana es
  obligatoria (la épica lo exige).
- Tests: las preguntas generadas entran como `borrador`; no aparecen en evaluaciones hasta
  publicarse.

---

## Qué se hizo
_(Completar al finalizar, antes de mover a "3 Finalizados".)_

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

- **Configuración de credenciales**: Se agregaron las variables de entorno `GEMINI_API_KEY` y `OPENAI_API_KEY` en `config/settings/base.py`.
- **Servicio de generación de IA (`ai_generation_service.py`)**:
  - Implementación de la función `generate_questions_for_resource` que genera borradores de preguntas (`Question` + `Choice`) para un recurso y un nivel pedagógico seleccionados.
  - Soporte integrado para las APIs de Gemini (Gemini 1.5 Flash) y OpenAI (GPT-4o-mini).
  - Mecanismo de **fallback a preguntas simuladas (mock)** si no hay llaves configuradas y se ejecuta en modo de desarrollo (`DEBUG = True` o entorno de pruebas/tests). Esto permite que el sistema funcione out-of-the-box localmente y en la integración continua (CI) sin costes.
- **Comando de management (`generate_ai_questions`)**: Permite la ejecución de la generación asistida a través de la terminal indicando el recurso, nivel, modo y cantidad.
- **Acción e interfaz en Django Admin**:
  - Se agregó una acción personalizada "Generar preguntas con IA" en la vista de lista de `Resource` de Django Admin.
  - Implementación de un **formulario intermedio** premium e integrado en el diseño del admin para configurar el nivel, modo y cantidad de preguntas antes de disparar la generación por IA.
- **Tests unitarios e integración (`test_ai_generation.py`)**:
  - Cobertura de tests para la generación simulada/mock (matemáticas y ciencias).
  - Pruebas del servicio con llamadas HTTP mockeadas a Gemini y OpenAI.
  - Validación del comando de management y de la acción con formulario intermedio de Django Admin.

# Pipeline único de publicación educativa basado en transcripción

- **Estado:** Cerrada 🟢 — backend **mergeado** (PR #72, 2026-06-19) · agente de subida (flujo de dos
  fases) a integrar en el uploader Node `profeonline-uploader`
- **Creado:** 2026-06-19
- **Prioridad:** P1 · **Cartera:** educativa / ingeniería
- **Tipo:** producto · pedagogía · infraestructura
- **Dueño sugerido:** 🧩 Codex (arquitectura + construcción por delegación explícita) → 🏛️ Claude (cierre)

## Objetivo (una frase)
Procesar cada video de un lote de forma idempotente, usando su transcripción real como fuente
principal para generar un documento pedagógico canónico, metadatos coherentes, guía y preguntas
auditadas, y publicar el conjunto solo cuando todas las etapas estén validadas.

## Fuentes a leer (rutas concretas)
- `apps/content/views/publish_studio.py`
- `apps/content/views/api_video.py`
- `apps/content/services/resource_copy.py`
- `apps/content/services/transcript_service.py`
- `apps/content/models/resource.py`
- `apps/content/models/quiz_guide.py`
- `apps/content/services/guide_service.py`
- `apps/content/services/ai_generation_service.py`
- `apps/content/management/commands/generate_pending_questions.py`
- `apps/content/management/commands/import_questions_json.py`
- `apps/content/models/resource_quiz_config.py`
- `apps/content/views/question_studio.py`
- `apps/content/views/question_review.py`
- `docs/gobernanza/inventario-operacional.md`

## Propuesta
1. Extender `profeonline.upload-batch/v1` con identificador de lote y política de publicación,
   manteniendo compatibilidad con órdenes existentes.
2. Persistir un ítem de pipeline por `batch_id + source_filename`, con estados
   `uploaded → transcript_pending → context_ready → metadata_ready → questions_ready → published`
   y estado de fallo reintentable.
3. Extender el webhook para hacer *upsert* del recurso y del ítem por ID de YouTube, siempre en
   borrador hasta el cierre.
4. Crear un documento pedagógico canónico en una `QuizGuide` vinculada directamente al recurso.
5. Generar desde ese documento los títulos y descripciones del recurso/YouTube y el contenido
   introductorio.
6. Generar candidatos de preguntas en borrador, auditarlos en una segunda etapa y regenerar los
   cupos rechazados con un máximo explícito de intentos.
7. Publicar atómicamente recurso y preguntas solo si transcripción, contexto, metadatos, guía,
   cobertura y auditoría están completas.
8. Incorporar un agente local versionado que consuma el lote y suba videos como no listados antes
   de invocar el webhook/pipeline. No realizar llamadas reales en tests ni en esta sesión.

## No-objetivos (qué queda FUERA)
- Ejecutar el flujo contra producción o publicar videos reales sin autorización explícita.
- Eliminar, reemplazar o mutar preguntas que tengan respuestas históricas.
- OCR de videos o PDFs escaneados.
- Una cola distribuida/worker en esta primera entrega; la orquestación será reintentable por comando.
- Curación destructiva de recursos o preguntas preexistentes.

## Criterios de aceptación (verificables)
- [x] Barrera verde: `test` · `check --deploy` · `makemigrations --check --dry-run`
- [x] El lote conserva compatibilidad con `profeonline.upload-batch/v1` y obtiene un `batch_id` estable.
- [x] Reintentar un ítem no duplica `Resource`, `QuizGuide`, configuración ni preguntas del pipeline.
- [x] Un transcript vacío o insuficiente detiene el ítem sin generar contenido inventado.
- [x] El documento canónico se basa principalmente en la transcripción y alimenta todos los metadatos.
- [x] Las preguntas se guardan primero en borrador y una segunda etapa valida fidelidad, unicidad,
      alternativas, explicación, dificultad, diversidad y ausencia de contenido fuera de guía.
- [x] Los cupos rechazados se regeneran hasta cubrir la matriz o agotar el máximo de intentos.
- [x] Solo el cierre exitoso publica recurso y preguntas dentro de una transacción.
- [x] Ninguna ruta del pipeline elimina preguntas con `QuizAttemptAnswer` o reportes históricos.
- [x] El uploader local usa privacidad `unlisted` y no se ejecuta contra YouTube durante tests.

## Plan de pruebas
- Unitarios de transiciones, transcript mínimo, documento canónico, metadatos y auditoría.
- Integración del webhook: creación, reintento por otra URL del mismo YouTube ID y no publicación parcial.
- Integración del orquestador: éxito completo, fallo por transcript, regeneración y rollback transaccional.
- Contrato del lote y agente local con cliente YouTube/webhook mockeados.
- Regresión focalizada: publicación, transcript, guías, generación, importador y estudio de preguntas.
- Suite completa y `check --deploy` al final, antes del handoff.

## Riesgos / rollback
- **Costo/cuota de IA:** lotes pequeños, máximo de regeneraciones y pruebas con mocks.
- **Bloqueo de transcript por YouTube:** el ítem queda en `transcript_pending`; nunca inventa contexto.
- **Migración aditiva:** modelos/campos nuevos y relaciones opcionales; rollback de código sin borrar datos.
- **Publicación parcial:** recursos y preguntas permanecen en borrador hasta la transacción final.
- **Historial estudiantil:** no se borra contenido histórico; cualquier reemplazo futuro deberá archivar.
- **Uploader/OAuth:** credenciales solo locales y fuera del repositorio; rollback = no ejecutar el agente.

---

## Qué se hizo
- Se añadió `PublicationItem` como estado durable e idempotente por lote/archivo, con migración
  aditiva y trazabilidad del recurso, video, guía, metadatos, cobertura, errores y reintentos.
- `QuizGuide` admite una relación canónica directa con `Resource`; las preguntas del pipeline
  registran origen, clave estable y evidencia de auditoría.
- El webhook crea/actualiza recurso e ítem dentro de una transacción y fuerza borrador.
- Se creó el servicio de orquestación: valida transcript mínimo, genera documento canónico y
  metadatos, crea/actualiza guía y `ResourceQuizConfig`, genera candidatos, ejecuta auditoría
  independiente, regenera rechazos y deja todo en borrador hasta cubrir la matriz.
- Se creó `process_publication_pipeline`, reintentable por ítem/lote y sin operaciones destructivas.
- Se añadió el agente local `scripts/process_upload_batch.py`: valida el contrato, sube no listado,
  maneja playlist, obtiene transcript, registra el ítem, espera `questions_ready`, actualiza
  metadatos de YouTube y confirma el cierre.
- Se añadieron endpoints autenticados de estado/confirmación y protección explícita para no borrar
  preguntas o alternativas con respuestas históricas.
- Pruebas focalizadas cubren idempotencia, transcript insuficiente, publicación atómica, webhook,
  privacidad de metadatos y preservación de historial.

## Auditoría final y correcciones (🏛️ Claude, 2026-06-19)

- Auditoría rigurosa read-only del backend (modelos, migración, webhook, servicio, comando,
  endpoints) y del agente. Veredicto: **aprobable con correcciones**.
- **Corregido (alto):** el agente de subida revierte el video a `unlisted` si la confirmación
  server-side falla (`publish_and_confirm`), preservando el invariante "un fallo mantiene YouTube no
  listado". *(Vive en el agente; viaja con la integración al uploader Node.)*
- **Corregido (medio):** `QuizGuide.canonical_resource` pasa de `CASCADE` a `SET_NULL` (modelo +
  migración 0029) para no borrar guías al eliminar un recurso.
- **Tests añadidos (medio):** regeneración por rechazo, agotamiento de rondas y auth negativa de los
  endpoints. **Suite completa 348 OK**; focalizada 17 OK; `check` y `makemigrations --check` verdes.
- **Diferido (medio):** bloqueo por concurrencia (`select_for_update`); sostener el lock durante las
  llamadas de IA rompería la durabilidad por checkpoints → tarjeta aparte.
- **Decisión de arquitectura:** el **agente Python** `scripts/process_upload_batch.py` **no se
  mergea** — duplica el uploader Node `profeonline-uploader` (subida, miniaturas, playlists). Este PR
  trae solo el **backend** (motor). El flujo de subida de dos fases se integrará en el uploader Node,
  reutilizando su OAuth/miniaturas/playlists; el script Python queda como referencia local.

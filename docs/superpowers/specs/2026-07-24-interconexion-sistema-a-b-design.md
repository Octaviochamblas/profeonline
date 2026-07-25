# Diseño: enlace cruzado entre Sistema A (Resource) y Sistema B (KnowledgeNode)

- **Fecha:** 2026-07-24 · **Redactado por:** 🏛️ Claude (brainstorming con el 🧑)
- **Origen:** auditoría de arquitectura del 2026-07-24 (`docs/auditorias/2026-07-24-auditoria-arquitectura-plataforma-aprendizaje.md`)
  confirmó que el Sistema A (legacy: `Area > Subject > Level > Module > Topic > Resource`, videos
  de YouTube) y el Sistema B (`KnowledgeNode`, `/aprender/...`) no comparten ninguna lógica de
  negocio — 0 aristas de imports en común. El 🧑 pidió explorar cómo complementarlos sin fusionarlos.

## 1. Objetivo

Cuando se sube o revisa un video del Sistema A, sugerir a qué nodo(s) del árbol de conocimiento
(Sistema B) corresponde, y mostrar un enlace cruzado "Ver también" en ambas páginas — **sin fusionar
los datos de los dos sistemas**. Es un puente de navegación, no una migración.

## 2. No-objetivos (explícitamente fuera de alcance)

- **No** se incrusta el video como `NodeMedia` dentro del nodo — solo un link cruzado entre las
  dos páginas existentes (`resource_detail.html` ↔ `node_detail.html`).
- **No** se corre sobre el catálogo ya publicado (181 recursos existentes) en esta primera versión —
  solo videos nuevos desde que se activa la funcionalidad. Un lote retroactivo queda para después,
  si esta primera versión funciona bien.
- **No** se toca `apps/content/services/publication_pipeline_service.py` ni la máquina de estados de
  `PublicationItem` — la funcionalidad es 100% aditiva y desacoplada del pipeline de subida.
- **No** se fusionan los modelos `NodeExercise`/`NodeAssessmentQuestion` ni ningún otro cambio de la
  hoja de ruta de la auditoría — esto es una pieza aislada, independiente del resto del roadmap.

## 3. Hallazgos de contexto que informan el diseño

- `NodeMedia` (Sistema B) ya soporta asociar un video de YouTube a un nodo — el "enchufe" de destino
  ya existe si en el futuro se decide incrustar. No se usa en esta versión (ver no-objetivos).
- El pipeline de subida (`PublicationItem`) ya genera una transcripción completa del video y guarda
  `taxonomy` (`subject_slug`, `topic_slug`, `education_level`) indicado por quien sube el video.
- No existe infraestructura de búsqueda semántica/embeddings en el proyecto (sin pgvector, sin
  sentence-transformers) — el matching debe apoyarse en lo que ya hay: texto y una llamada de IA
  puntual, no en una nueva pieza de infraestructura pesada.
- Los `Topic` del Sistema A (30 en la base local, ej. "Límites y Continuidad", "Campo eléctrico y
  potencial", "Números Racionales") son razonablemente atómicos y no se solapan entre sí — mapearlos
  al bloque/tema correspondiente del árbol de `KnowledgeNode` puede resolverse por comparación de
  nombre/slug, sin IA. Ya incluyen contenido universitario (Cálculo, Física), no solo PAES escolar.
- Un `Topic` es más grueso que un `recurso` (nodo hoja): un mismo tema de Sistema A agrupa varios
  videos, y cada video probablemente cubre un concepto atómico distinto de los 5-20 nodos hoja que
  existen dentro del bloque equivalente en Sistema B. El matching fino ocurre a ese nivel, no al
  nivel de bloque.
- Ya existe el patrón de endpoint "options" para autocompletado (`subject_options`, `module_options`
  en `apps/content/views/subject_options.py` / `module_options`) — se reutiliza para el buscador
  manual de nodos.
- Ya existe el patrón de comando de un solo uso con llamada a IA (`generate_pending_questions.py`,
  `apps/content/services/ai_generation_service.py` con `call_gemini_api`/`call_openai_api`) — se
  reutiliza para la llamada de corroboración.

## 4. Arquitectura

### 4.1 Modelo nuevo: `ResourceNodeSuggestion`

Tabla puente, aditiva, sin tocar `Resource`, `NodeMedia` ni ningún modelo existente.

| Campo | Tipo | Notas |
|---|---|---|
| `resource` | FK a `content.Resource` | |
| `node` | FK a `KnowledgeNode` | nulo si `status='sin_bloque'` (paso 1 no encontró bloque) |
| `status` | Char | `sugerido` \| `confirmado` \| `descartado` \| `sin_bloque` |
| `origen` | Char | `ia` \| `manual` — de dónde vino el nodo finalmente confirmado |
| `ai_rationale` | Text, blank | razón breve que da la IA en el paso de corroboración |
| `ai_corrigio` | Bool, default False | si la IA cambió el candidato del paso 2 (señal de confianza para quien revisa) |
| `created_at` / `confirmed_at` | DateTime | |

Constraint: unique together (`resource`, `node`) para no duplicar la misma sugerencia si el comando
se corre de nuevo. Un `Resource` con una fila `confirmado` o `descartado` se excluye de futuras
corridas del comando (idempotencia).

### 4.2 Pipeline de matching (comando de un solo uso, `suggest_resource_node_links`)

No se engancha al pipeline de subida — es un comando independiente que se corre manualmente o por
barrido periódico sobre recursos publicados sin sugerencia/confirmación previa.

**Paso 1 — Bloque/tema (determinístico, sin IA):**
Compara `Resource.topic.name`/slug contra el nombre/código de los nodos `bloque`/`tema` del árbol
`KnowledgeNode` (mismo `subject_abbr` cuando se pueda inferir de `taxonomy.subject_slug`). Si no hay
match razonable, se crea `ResourceNodeSuggestion(status='sin_bloque')` — sin candidato, disponible
para resolución manual en la vista de revisión.

**Paso 2 — Candidato atómico (búsqueda de texto, sin IA):**
Dentro del bloque identificado en el paso 1, hay un puñado de nodos hoja (`recurso`, ~5-20). Se
compara el título del video (y opcionalmente los primeros ~200 palabras de la transcripción, solo si
el título es ambiguo) contra `nombre`/`objetivo` de cada nodo hoja usando búsqueda de texto nativa de
Postgres (`SearchVector`/trigram — sin dependencia nueva). Devuelve 1 candidato principal + hasta 2
alternativas cercanas.

**Paso 3 — Corroboración con IA (prompt acotado):**
Un llamado chico, reusando el patrón de `ai_generation_service.py`. El prompt incluye **solo**:
título del video (+ extracto corto de transcripción si hizo falta en el paso 2), el candidato
principal (nombre + objetivo, no el contenido completo del nodo), y las 1-2 alternativas cercanas
(mismo formato compacto). Se le pide confirmar o corregir, con una razón breve. Nunca se le manda el
listado completo de nodos de un bloque ni el contenido completo (`explicacion`) de ningún nodo —
mantiene el prompt chico independiente de cuántos recursos se procesen.

Resultado: `ResourceNodeSuggestion(status='sugerido', node=<candidato final>, ai_rationale=<razón>,
ai_corrigio=<bool>)`.

**Control de costo:** modelo económico/rápido para esta tarea (es clasificación, no generación
creativa); tope duro de candidatos en el paso 2 (máx. 20) independiente de qué tan bien haya
funcionado el paso 1; transcripción nunca completa en el prompt, solo extracto corto si hace falta.

### 4.3 Vista de revisión (nueva, staff-only)

Ruta nueva bajo el mismo namespace que el resto del "estudio de publicación", ej.
`publicar/sugerencias-nodos/` (`apps/content/urls/publish_urls.py`), con su vista en un archivo nuevo
`apps/content/views/node_suggestions.py` (sigue la convención de un archivo por vista de esa carpeta).

Por cada `Resource` pendiente (con sugerencia `sugerido` o `sin_bloque`), la vista muestra:

- La sugerencia automática si existe: nodo candidato, razón de la IA, y si `ai_corrigio=True` (señal
  visual de "la IA no confirmó el primer candidato, revisar con más cuidado").
- Un campo de búsqueda con autocompletado sobre `KnowledgeNode` (por nombre o código), reusando el
  patrón de `subject_options`/`module_options` — nuevo endpoint `node_options` que devuelve JSON
  filtrado por texto.
- Botones: **Confirmar sugerencia automática** / **Confirmar nodo buscado manualmente** / **Descartar**.

Al confirmar (automático o manual), se actualiza `status='confirmado'` y `origen` correspondiente.

### 4.4 Render del enlace cruzado

En `templates/pages/resource_detail.html` y `templates/learn/node_detail.html`, un bloque nuevo
"Ver también" que consulta si existe una `ResourceNodeSuggestion` con `status='confirmado'` para el
objeto actual, y si existe, muestra el link a la página del otro lado (recurso → nodo, o nodo →
recurso). Sin sugerencia confirmada, el bloque no se renderiza (no ensucia la página).

## 5. Flujo de datos (resumen)

```
Resource publicado (sin sugerencia previa)
        │
        ▼
[Paso 1] Topic → bloque KnowledgeNode  (texto, gratis)
        │
        ├─ sin match → status='sin_bloque' (espera resolución manual)
        │
        ▼ (bloque encontrado)
[Paso 2] título/extracto vs. nodos hoja del bloque (texto, gratis)
        │
        ▼
[Paso 3] corroboración IA (prompt chico: 1 video + 1-3 candidatos compactos)
        │
        ▼
ResourceNodeSuggestion(status='sugerido', node=X, ai_rationale=..., ai_corrigio=...)
        │
        ▼
Vista de revisión (staff) — confirma / busca manual / descarta
        │
        ▼ (confirmado)
"Ver también" visible en resource_detail.html y node_detail.html
```

## 6. Manejo de errores

- Fallo de red/IA en un recurso individual del comando → se salta ese recurso, se loguea, sigue con
  el resto del lote (mismo patrón que `generate_pending_questions.py`).
- Paso 1 sin match → no es un error, es `status='sin_bloque'`, disponible para resolución manual.
- Paso 3 con respuesta de IA inválida/no parseable → se guarda igual el candidato del paso 2 como
  `status='sugerido'` con `ai_rationale=''` y `ai_corrigio=False` (degrada a solo texto, no bloquea).
- Confirmar/descartar es idempotente — una vez resuelto, el recurso no vuelve a aparecer en corridas
  futuras del comando ni en la cola de revisión.

## 7. Testing

- Comando `suggest_resource_node_links`: mock de la llamada IA; verificar paso 1 (match de topic→bloque
  determinístico, incluyendo el caso sin match); verificar que el paso 2 nunca manda más de 20
  candidatos; verificar que no se duplican sugerencias en recursos ya `confirmado`/`descartado`.
- Vista de revisión: permisos (solo staff); confirmar automático vs. manual actualiza `origen`
  correctamente; descartar no deja el recurso disponible para nueva sugerencia automática.
- Endpoint `node_options`: filtra correctamente por texto, formato JSON esperado por el autocompletado.
- Templates: bloque "Ver también" se renderiza con sugerencia confirmada y no se renderiza sin ella,
  en ambos lados (`resource_detail.html`, `node_detail.html`).

## 8. Trabajo futuro (fuera de este spec)

- Lote retroactivo sobre los 181 recursos ya publicados, si esta primera versión valida bien.
- Reconsiderar si conviene además incrustar como `NodeMedia` (no solo link cruzado) una vez que haya
  señal de que las conexiones sugeridas son confiables.
- Limpiar los dos `Topic` basura sin recursos ("dds", "ds") encontrados durante la exploración —
  no bloquea este spec, es limpieza aparte.

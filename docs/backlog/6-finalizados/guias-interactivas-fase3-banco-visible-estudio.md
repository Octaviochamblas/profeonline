# Guías interactivas — Fase 3: banco visible + experiencia de estudio

- **Estado:** 🟢 CERRADA (2026-06-22) — gate técnico de Codex + cierre de Claude; barrera completa verde; mergeada a `main`.
- **Creado:** 2026-06-22 · **Epic padre:** `1-por-iniciar/guias-interactivas-banco-estandarizado-items.md`
- **Prioridad:** P1 · **Cartera:** educativa · **Tipo:** producto · pedagogía
- **Dueño:** 🧩 Codex (preflight) → 🔨 Antigravity (construye, rama `feat/guias-fase3-banco-visible`) → 🧩 Codex (audita) → 🏛️ Claude (cierre)

> **Alcance: página de la guía propia + banco visible agrupado + práctica.** Sin corrección de
> respuesta directa (Fase 4) ni evaluaciones por nivel/final (Fase 5). Las prácticas de esta fase no
> tienen peso académico.

## Objetivo (una frase)
Que el alumno vea, en tema y recurso, **solo las guías ProfeOnline públicas**, con su página propia
(logo, KaTeX, imprimible) y un **banco visible** agrupado por ítem y dificultad, donde pueda estudiar
todo, practicar un ítem concreto o hacer una práctica mixta equilibrada — con "Ver pista" / "Ver
solución" que **no** afectan el dominio académico.

## Antes de empezar
- Detrás del flag `Topic.structured_bank_enabled`. Temas apagados → experiencia actual intacta.
- Solo entran preguntas con `scope="banco_visible"` (valor real del modelo) e ítem aprobado; el banco legacy
  (`scope=""`) **no** aparece aquí.
- Antes de publicar preguntas del banco visible, aislar explícitamente el sistema legacy con
  `scope=""` en sus selectores de disponibilidad, quiz y evaluación final. Hoy esos selectores
  aceptan toda pregunta publicada y mezclarían ambos sistemas.

## Fuentes a leer
- `apps/content/models/question.py` — campos Fase 0: `exercise_item` (FK), `question_type`,
  `difficulty`, `hint`, `canonical_answer`, `scope`, `learning_guide`. Valores reales:
  `scope="banco_visible"` y dificultades `basica/intermedia/avanzada/desafio`.
- `apps/content/models/exercise_item.py` / `ResourceExerciseItem` (cuotas `practice_quota`).
- `apps/content/models/learning_guide.py` — `structured_content`, `visibility="publica"`.
- `apps/content/services/ai_generation_service.py` — reutilizar
  `generate_question_candidates`, `_call_gemini_api`/`_call_openai_api`, `_loads_ai_json`,
  `_sanitize_key`; **no** duplicar HTTP, backoff ni parseo. `_save_questions` legacy no sirve tal
  cual para persistir los campos del banco estructurado.
- `apps/content/selectors/evaluation_selectors.py` y
  `apps/content/services/evaluation_service.py` — agregar aislamiento `scope=""` al sistema actual.
- `static/js/quiz-player.js` + plantillas de quiz (reproductor fullscreen) y
  `apps/content/services/progress_service.py` (NO darle peso a estas prácticas).
- Vistas de recurso/tema del alumno (dónde insertar el listado de guías públicas).

## Alcance de construcción

### 1) Generación editorial del banco visible

Crear `apps/content/services/visible_bank_service.py` con:

```python
def generate_visible_bank_questions(
    *,
    exercise_item,
    resource,
    learning_guide,
    count=None,
    api_key=None,
    status="borrador",
) -> list[Question]:
    ...
```

- Exigir tema activo con `structured_bank_enabled=True`, ítem `status="aprobado"`, recurso publicado
  del mismo tema y vínculo `ResourceExerciseItem(exercise_item, resource)`.
- Exigir `LearningGuide` del mismo tema, `status="publicada"` y `visibility="publica"`.
- Cantidad por defecto:

```python
count = resource_link.practice_quota or exercise_item.detected_exercise_count
```

  `practice_quota` es el objetivo editable por vínculo. Si el ítem tiene varios recursos, el
  profesor elige el recurso por tanda: **no** multiplicar automáticamente la cantidad detectada.
- Reusar `generate_question_candidates(...)` y sus helpers IA existentes. Añadir instrucciones
  específicas mediante `custom_instructions` para pedir `difficulty`, `hint`, explicación y una
  alternativa correcta. No duplicar llamadas HTTP ni `json.loads`.
- Crear un persistidor propio transaccional; no ensanchar `_save_questions` con parámetros opcionales
  del sistema nuevo.
- Cada fila creada debe llevar obligatoriamente:

```python
resource=resource
level=exercise_item.level
mode="preparacion"          # compatibilidad del modelo; no implica progreso académico
status="borrador"           # revisión/publicación manual
exercise_item=exercise_item
scope="banco_visible"
question_type="alternativa"
difficulty=<Question.DIFFICULTY_CHOICES>
hint=<texto>
canonical_answer=<texto de la alternativa correcta>
learning_guide=learning_guide
```

- Crear exactamente cuatro `Choice`, una sola correcta. Validar el contrato completo antes de
  persistir y usar `transaction.atomic()`.
- Mantener flujo editorial: generar borradores → revisar/editar → publicar manualmente. Nada se
  publica solo.

### 2) Panel editorial

Extender el panel de ítems de Fase 1 con una sección **Banco visible**, sin crear otro estudio
desconectado:

- por ítem aprobado, listar sus `ResourceExerciseItem`;
- mostrar recurso, `practice_quota`, preguntas borrador/publicadas y déficit;
- permitir editar `practice_quota`;
- acción “Generar borradores” por recurso;
- enlace al panel de revisión de preguntas filtrado por ítem/scope.

Las mutaciones son solo-admin y replican `_get_enabled_topic` / `_get_enabled_item`.

### 3) Aislamiento del sistema legacy

Agregar `scope=""` en:

- `get_question_availability_map`;
- `get_questions_for_quiz`;
- validación/lectura defensiva de preguntas en `submit_quiz`;
- queryset de la evaluación final actual (`_topic_exam_question_qs`) y su submit.

Así las preguntas `banco_visible` no habilitan niveles legacy, no entran en Preparación/Evaluación
actual ni en la prueba final existente. Agregar regresiones explícitas.

### 4) Página pública de la guía

- Nueva vista `learning_guide_detail(slug)` y URL pública.
- Query obligatoria:

```python
LearningGuide.objects.get(
    slug=slug,
    status="publicada",
    visibility="publica",
    topic__is_active=True,
    topic__structured_bank_enabled=True,
)
```

- Requiere usuario autenticado, coherente con el contenido completo de recursos.
- Render de `structured_content` con logo ProfeOnline, KaTeX y `@media print`. “Imprimible” significa
  impresión del navegador; **no** `html2pdf.js` ni generación/almacenamiento PDF.
- Nunca exponer `private_sources`, `originality_report` ni guías internas/borradores/archivadas.

### 5) Listados en tema y recurso

- `TopicDetailView`: cargar la guía pública del tema solo cuando el flag esté activo.
- `ResourceDetailView`: mostrar la guía únicamente si el recurso está asociado a ella.
- Sincronizar `LearningGuide.resources` a partir de los recursos vinculados mediante
  `ResourceExerciseItem` a los ítems incluidos en la guía/banco. No asumir que Fase 2 dejó ese M2M
  poblado.
- Temas con flag apagado conservan exactamente las plantillas y queries actuales.

### 6) Banco visible y queries

Query base:

```python
Question.objects.filter(
    status="publicada",
    scope="banco_visible",
    resource__is_published=True,
    resource__topic=topic,
    exercise_item__topic=topic,
    exercise_item__status="aprobado",
    learning_guide=guide,
    learning_guide__status="publicada",
    learning_guide__visibility="publica",
).select_related(
    "resource",
    "exercise_item",
    "learning_guide",
).prefetch_related(
    "choices",
).order_by(
    "exercise_item__order",
    "difficulty",
    "order",
    "id",
)
```

- Ejecutar una sola query y agrupar en memoria por ítem/dificultad.
- `difficulty="desafio"` se muestra como desafío; `basica/intermedia/avanzada` son normales.
- Paginar o limitar la carga inicial si el banco crece; no iterar `item.questions` por ítem.
- “Ver pista” (`hint`) y “Ver solución” (`canonical_answer`/alternativa correcta) son controles de
  presentación sin escrituras ni eventos académicos.

### 7) Práctica no académica

Crear selector independiente:

```python
def select_visible_practice_questions(
    *,
    topic,
    item_id=None,
    resource_id=None,
    count=10,
    seed=None,
) -> list[Question]:
    ...
```

- Base obligatoria: `status="publicada"`, `scope="banco_visible"`, ítem aprobado, tema con flag,
  recurso publicado y guía pública.
- Si se solicita `item_id`/`resource_id`, validarlos dentro del mismo tema.
- La práctica mixta usa round-robin entre ítems y dificultades, con límite de cantidad; no incorpora
  cuotas, no-repetición ni pools ocultos de Fase 5.
- Crear endpoints/parciales propios de inicio y envío. **No usar `quiz_submit` ni
  `submit_quiz`**, porque crean `QuizAttempt` y afectan el progreso.
- El submit calcula resultados y recomendaciones solo para la respuesta actual, sin persistir
  `QuizAttempt`, `TopicEvaluationAttempt`, puntaje académico ni dominio.
- Las recomendaciones de menor rendimiento son efímeras, derivadas de los errores de esa práctica.

### 8) Reproductor fullscreen

- Reusar `quiz-player.js` y su contrato DOM: `#quiz-player-root`, `data-quiz-player`,
  `data-quiz-slide`, `data-quiz-prev/next` y radios.
- Crear formulario/resultados propios; no reutilizar literalmente `quiz_form.html`, porque apunta al
  submit académico y rotula solo Preparación/Evaluación.
- Omitir `data-quiz-status-url` para no refrescar la sección de progreso legacy al cerrar.

### 9) CSP, KaTeX e impresión

- JS nuevo solo externo, autoalojado, con nonce y cache-buster `?v=N`; sin handlers inline.
- KaTeX ya renderiza `document.body` y cada `htmx:afterSwap`: no agregar otro renderizador.
- CSS `@media print` para ocultar navegación/controles y conservar logo, contenido y solucionario.
- Si se toca CSS global, subir el cache-buster de `estilos.css`.

## Criterios de aceptación
- [ ] Barrera verde (`test`/`check`/`makemigrations --check`). Migraciones, si hay, aditivas.
- [ ] Generación crea solo preguntas `borrador` con todos los campos estructurados y sin red en tests.
- [ ] El alumno solo ve guías `status="publicada"` + `visibility="publica"` de temas con flag.
- [ ] El banco visible usa exclusivamente `scope="banco_visible"`; el banco legacy no aparece aquí.
- [ ] Los selectores legacy filtran `scope=""`; preguntas visibles no alteran disponibilidad,
  quiz actual ni evaluación final.
- [ ] Filtros por ítem/dificultad y separación normales/desafíos correctos.
- [ ] “Ver solución”/“Ver pista” no escriben en BD ni alteran dominio.
- [ ] Práctica visible no crea `QuizAttempt`; `progress_service` entrega exactamente el mismo
  resultado antes y después.
- [ ] Práctica por ítem/recurso respeta filtros; mixta equilibra ítems y dificultades.
- [ ] Sin N+1 al agrupar banco ni listar guías en tema/recurso.
- [ ] CSS nuevo → cache-buster `?v=N`; CSP/KaTeX intactos; QA móvil 320/360/390.

## No-objetivos
- Corrección de respuesta directa numérica/algebraica (Fase 4).
- Evaluaciones por nivel / prueba final / timers / dominio ponderado (Fase 5).
- No-repetición, cuotas de evaluación ni pools ocultos (Fase 5).
- Exportación/descarga PDF y `html2pdf.js` (Fase 6); solo CSS print.
- Migración del banco legacy, gate de activación y piloto (Fase 7).

## Riesgos
- No mezclar el banco visible con el pool oculto de evaluaciones (Fase 5 usa `scope` distinto).
- Rendimiento: paginar/prefetch para no caer en N+1 al agrupar por ítem.

## Plan mínimo de pruebas

- Generación mock/offline: campos completos, cuatro alternativas, una correcta y estado borrador.
- Rechazo de tema apagado, ítem no aprobado, recurso ajeno/no vinculado y guía no pública.
- Cantidad por `practice_quota` y fallback a `detected_exercise_count`.
- Publicación manual; ninguna pregunta estructurada se publica automáticamente.
- Regresión legacy: `scope="banco_visible"` no aparece en disponibilidad, quiz ni evaluación final.
- Guía interna/borrador/archivada → 404 para alumno; pública + flag activo → 200.
- Recurso solo lista guías asociadas; tema lista únicamente su guía pública.
- Query count acotado al agrupar múltiples ítems/dificultades/recursos.
- Selector por ítem, por recurso y mixto equilibrado.
- Submit de práctica no crea `QuizAttempt` ni cambia `get_resource_progress`.
- Pista/solución sin escrituras.
- Contrato DOM compatible con `quiz-player.js`; KaTeX tras swap; CSP sin inline.
- CSS print y QA 320/360/390 px.

## Preflight 🧩 Codex — 2026-06-22

**Resultado:** listo para construir con este handoff refinado.

- Los modelos contienen todos los campos necesarios; no se anticipa migración.
- `generate_questions_for_resource`/`_save_questions` no se reutilizan tal cual: se reutiliza la
  generación de candidatos y se persiste mediante un servicio específico.
- El aislamiento `scope=""` del flujo legacy es obligatorio antes de publicar el banco visible.
- La práctica usa endpoints propios y no crea intentos académicos.
- La UI pública se integra en `TopicDetailView`/`ResourceDetailView` y reutiliza el reproductor
  fullscreen, CSP y KaTeX existentes.

## Auditoría y correcciones 🧩 Codex — 2026-06-22

**Veredicto:** aprobada técnicamente; sin P0/P1 abiertos.

Correcciones principales aplicadas:

- Publicación exclusivamente manual: generación siempre en borrador y validación completa de
  enunciado, explicación, dificultad, pista, cuatro alternativas únicas, una correcta y respuesta
  canónica antes de publicar.
- Las preguntas del banco visible nunca se borran físicamente; archivar reemplaza toda acción de
  eliminación. Editar una pregunta/alternativa publicada la devuelve a borrador.
- El submit de práctica revalida en caliente scope, estado, tema, recurso, ítem y guía; también se
  valida el vínculo ítem↔recurso cuando ambos filtros están presentes.
- Generación limitada y protegida contra sobrellenado concurrente mediante bloqueo del vínculo y
  recálculo del déficit dentro de la transacción.
- Panel de ítems completado con cuota, conteos, déficit, generación y enlace de revisión; refrescos
  de fila con `prefetch_related("resource_links__resource")`.
- Página pública corregida para renderizar el esquema JSON real de Fase 2; logo, JS externo CSP-safe,
  cache-buster del CSS de impresión y reutilización del render KaTeX global.
- Tests ampliados de 10 a 13, incluyendo ausencia de red, publicación incompleta, archivo lógico y
  revalidación posterior al inicio de práctica.

Barrera real:

- `python manage.py test`: **469 tests OK** en **324,059 s**.
- `python manage.py check --deploy`: exit 0; 7 warnings conocidos de settings locales.
- `python manage.py makemigrations --check --dry-run`: **No changes detected**.
- `pre-commit run --all-files`: todos los hooks pasaron.
- Regresiones focalizadas de ítems, guías y evaluación: **104 tests OK**.

P3 no bloqueante para cierre: repetir QA visual manual en 320/360/390 px antes del despliegue si
Claude dispone de navegador; la estructura responsive y el CSS fueron revisados, pero Codex no
registró una sesión visual manual en esta auditoría.

## Cierre 🏛️ Claude — 2026-06-22

Verificado en corrida limpia (lock libre, sin colisión de working tree):
- **Aislamiento legacy:** los selectores/servicios actuales filtran `scope=""` (mapa de
  disponibilidad, preguntas de quiz, validación de submit y prueba final), de modo que el banco
  `banco_visible` NO entra en Preparación/Evaluación/Final legacy ni habilita niveles.
- **Vista de alumno** (`learning_guide_student.py`): `@login_required`, guía solo si
  `status="publicada"` + `visibility="publica"` + tema con flag; banco solo `scope="banco_visible"` +
  ítem aprobado + guía pública; guardas anti-manipulación en el submit.
- **Sin peso académico:** la práctica no crea `QuizAttempt` ni escribe progreso; pista/solución no
  tocan BD.
- **Generación editorial** (`visible_bank_service.py`): borradores manuales, reusa
  `generate_question_candidates` (sin duplicar HTTP), cap por tanda de 50, mock determinista en tests.
- **CSP:** JS externo con nonce; **sin migraciones** (esquema de Fase 0 ya cubría los campos).

**Barrera reverificada por Claude (`.venv`, corrida limpia):** `manage.py test` → **469 tests OK**
(304 s) · `check --deploy` exit 0 (7 warnings locales) · `makemigrations --check` sin cambios ·
`pre-commit` Passed · `git diff --check` sin errores.

**Pendiente P3 (no bloqueante):** QA visual manual en 320/360/390 px.

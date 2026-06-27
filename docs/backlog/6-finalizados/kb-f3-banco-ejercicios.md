# F3 — Estructura pedagógica por ítems: `ItemGroup` + banco `NodeExercise` + pipeline JSONL

- **Estado:** Handoff Ready — reescrito tras decisiones D2/D3/D4 (🧑, 2026-06-27)
- **Creado:** 2026-06-26 · **Reescrito:** 2026-06-27
- **Prioridad:** P1 · **Cartera:** educativa
- **Tipo:** infraestructura · producto
- **Requiere:** F2 completo (páginas del nodo en pie)

> **Cambio de alcance vs versión anterior:** ya no son "ejercicios de libros" (`BookExercise`) sueltos.
> Ahora es la **estructura pedagógica** del recurso: un **banco único** (`NodeExercise`) organizado en
> **grupos pedagógicos** (`ItemGroup`), poblado por el pipeline **NotebookLM → Claude → JSONL → DB**.
> Las decisiones que fijan esto están en `arquitectura-plataforma-conocimiento.md` §8 (D2, D3, D4).

## Objetivo

Que cada recurso (nodo hoja) tenga una estructura de práctica concreta: bloques pedagógicos que van de
*comprender* a *evaluar*, con ejercicios anclados al nodo y al grupo. Respuestas **visibles** (práctica
libre, sin login, sin scoring). La **medición del alumno se difiere** (capas 4–5): este sprint construye
solo la estructura y su pipeline de carga.

## Decisiones que aplican (ya ratificadas, §8)

- **D2** — tablas **nuevas** ancladas a `KnowledgeNode`; Sistema A (`Question`/`Resource`) **intacto**.
- **D3** — **banco único** por `ItemGroup`; ítems "no vistos" para evaluación futura saldrán de
  `kind=template` (generadores). No se construye el runtime de generadores ahora.
- **D4** — sin `AssessmentRule`/`AssessmentAttempt`/`StudentNodeState` en este sprint (entran después,
  aditivos). Versionado por **snapshot en el intento** + timestamps, no por tablas de versión.

## Reencuadre pedagógico (importante)

Los "errores frecuentes" **no** se muestran como tales. Se transforman en **preguntas conceptuales**
("chequeo de comprensión", enfoque positivo: *"Veamos si tienes clara esta idea"*). Internamente se
etiquetan con `conceptual_checks` (p. ej. `comprende_denominador_comun`). Evitar lenguaje visible de
"errores/fallas".

## Propuesta

### 1. Modelos (nuevo archivo `apps/content/models/node_bank.py`)

**`ItemGroup`** — bloque pedagógico de preguntas dentro de un recurso.

| Campo | Tipo | Notas |
|---|---|---|
| `node` | FK `KnowledgeNode` (`related_name='item_groups'`) | hoja |
| `code` | Char(40) | `conceptuales`, `reconocimiento`, … |
| `title` | Char(120) | visible |
| `purpose` | Text | para qué sirve el grupo |
| `level` | Char(choices) | `comprender`/`reconocer`/`resolver`/`variar`/`aplicar`/`evaluar` |
| `order` | PosSmallInt | |
| `required_for_mastery` | Bool=False | para evaluación futura |
| `is_published` | Bool=True | |
| `created_at`/`updated_at` | DateTime | |
| | unique(`node`,`code`) | |

Constante `STANDARD_ITEM_GROUPS` (7 grupos, §4.4 del handoff) + helper idempotente
`ensure_standard_item_groups(node)`.

**`NodeExercise`** — ejercicio del banco (único).

| Campo | Tipo | Notas |
|---|---|---|
| `stable_id` | Char, unique si ≠'' | llave idempotente de reimport |
| `node` | FK `KnowledgeNode` (`related_name='exercises'`) | hoja |
| `item_group` | FK `ItemGroup` (`related_name='exercises'`) | |
| `kind` | Char | `item` \| `template` (patrón generador) |
| `format` | Char | `multiple_choice`/`open_answer`/`true_false`/`matching`/`completion`/`development` |
| `difficulty` | Char | `basica`/`media`/`avanzada` |
| `competencia` | Char | `M1`/`M2`/`U` (reusa choices de `KnowledgeNode`) |
| `prompt` | Text | enunciado (KaTeX) |
| `choices` | JSON | alternativas |
| `correct_answer` | Text | |
| `solution_steps` | Text | |
| `explanation` | Text | |
| `conceptual_checks` | JSON | etiquetas de idea evaluada |
| `prerequisites` | JSON | semantic_ids detectados |
| `pattern` | JSON | variables/restricciones si `kind=template` |
| `paes_style` | Bool=False | |
| `source_title`/`source_location`/`source_reference` | | procedencia (auditable) |
| `source_kind` | Char | `notebooklm_extraction`/`manual`/`generated`/`rewritten` |
| `status` | Char | `draft`/`ready`/`review_required`/`published`/`archived` |
| `legal_review`/`rewrite_required`/`duplicate_candidate` | Bool | banderas de control |
| `notes` | Text | |
| `order` | PosSmallInt | |
| `created_at`/`updated_at` | DateTime | |

Registrar ambos en `models/__init__.py` y en admin (`ItemGroupAdmin` con inline de `NodeExercise`;
`NodeExerciseAdmin` con filtros por `status`/`format`/`difficulty`/`legal_review`).

### 2. Importador JSONL (`load_exercise_bank`)

Comando que lee un `.jsonl` (una línea por ejercicio, formato §12 del handoff) y:

1. Valida que `semantic_id` exista en `KnowledgeNode`.
2. Resuelve/crea el `ItemGroup` por `code` (si falta, lo crea desde plantilla estándar).
3. **Upsert idempotente** por `stable_id` (o crea si viene vacío).
4. **Nunca publica automáticamente** si: `legal_review=true` · `rewrite_required=true` ·
   `status=review_required` · falta `prompt` · falta `correct_answer`. En esos casos entra como
   `review_required`/`draft`.
5. Informa: `Creados / Actualizados / semantic_id no encontrado / marcados para revisión`.

### 3. Sección de banco en la página del nodo (`templates/learn/node_detail.html`)

Después de "Ejemplos": **"Practica por ítems"** (solo si hay `NodeExercise` publicados):
- Agrupado por `ItemGroup` (en orden de progresión), cada grupo en `<details>` con su `title`/`purpose`.
- Cada ejercicio: `prompt` (KaTeX), alternativas si las hay, botón **"Ver solución"** (toggle JS vanilla,
  nonce CSP) que despliega `solution_steps`/`explanation` + `correct_answer`.
- Conceptuales = primer grupo, encuadre positivo.
- Sin ejercicios → sección no aparece. Sin login → igual.

### 4. Prompts del pipeline (documentación)

`docs/conocimiento/pipeline/` — los prompts de NotebookLM (extracción general, pasada por recurso,
patrones) y el de Claude normalizador (salida JSONL), del handoff §11.

## No-objetivos (este sprint)

- Sin `AssessmentRule`/evaluación formal/intentos/scoring (capa 4, futuro).
- Sin `StudentNodeState`/estrellas/XP (capa 5, futuro).
- Sin runtime de generadores (solo se guarda `kind=template` + `pattern`).
- Sin tocar el Sistema A (`Question`/`Resource`/banco viejo).
- Poblar solo el piloto (ruta enteros→fracciones, §20).

## Criterios de aceptación

- [ ] Barrera verde: `python manage.py test` · `check --deploy` · `makemigrations --check`.
- [ ] Migración aditiva (solo tablas nuevas; cero `ALTER` sobre tablas vivas).
- [ ] `ItemGroup` unique(`node`,`code`); `ensure_standard_item_groups` idempotente (7 grupos).
- [ ] `NodeExercise.stable_id` único cuando no vacío; vacío permite múltiples.
- [ ] `load_exercise_bank` idempotente; respeta el "no autopublicar".
- [ ] Página del nodo muestra "Practica por ítems" agrupado, con toggle de solución y KaTeX.
- [ ] Admin operativo (CRUD + filtros + inline).

## Reutilización verificada (código real)

- `originality_service` → apoya el chequeo de `duplicate_candidate`/`legal_review`.
- `answer_grading_service` / `evaluation_assembly_service` / `evaluation_bank_service` → se reutilizan
  **cuando llegue la evaluación formal** (capa 4); este sprint no los toca.
- `ExerciseItem`/`visible_bank_service` (Sistema A) → **no** se reutilizan (anclaje viejo a `Topic`).
- KaTeX y toggle JS vanilla con nonce → patrón de F2/sitio; no re-cablear.

## Riesgos / rollback

- Muchos ejercicios por nodo (>50): paginar/lazy-load dentro del acordeón.
- Rollback: revertir la migración (tablas nuevas con FK a tablas nuevas → sin impacto en lo existente).

## Qué se hizo (2026-06-27, 🏛️ Claude + 🧑)

Construido en `feat/grafo-conocimiento-f1`, todo **aditivo** (Sistema A intacto):

- **Modelos** `apps/content/models/node_bank.py`: `ItemGroup` (unique `node`+`code`, 6 niveles de
  progresión) y `NodeExercise` (banco único, `kind=item|template`, `pattern` para generadores futuros,
  procedencia + banderas legal/rewrite/duplicate, `status` de 5 estados, `stable_id` único). Constante
  `STANDARD_ITEM_GROUPS` (7 grupos) + helper idempotente `ensure_standard_item_groups`. Migración
  `0039`. Exportados + admin (inline + filtros).
- **Importador** `load_exercise_bank` (JSONL): valida `semantic_id`, resuelve/crea `ItemGroup` desde
  plantilla, upsert idempotente por `stable_id`, **nunca autopublica** (legal/rewrite/sin-respuesta →
  `review_required`; `published` entrante → `ready`) y **no degrada** publicaciones manuales.
- **Página**: sección "Practica por ítems" en `node_detail.html` (acordeón por grupo, toggle
  "Ver solución" JS vanilla con nonce + atributo `hidden`, KaTeX), `_build_practice_bank` sin N+1.
- **Pipeline**: prompts NotebookLM + normalizador Claude + esquema JSONL en
  `docs/conocimiento/pipeline/pipeline-notebooklm.md`. Piloto JSONL del nodo Naturales (4 ejercicios),
  verificado en navegador.
- **Tests**: 20 nuevos (17 `test_node_bank` + 3 banco en `apps/learn`). `makemigrations --check` limpio.

**Fuera de alcance (por D4, a futuro):** `AssessmentRule`/evaluación formal/intentos/`StudentNodeState`/
estrellas/runtime de generadores. Pendiente operativo: poblar el banco a cuentagotas.

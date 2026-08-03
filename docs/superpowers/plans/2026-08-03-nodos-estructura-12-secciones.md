# Nodos — estructura editorial de 12 secciones (infraestructura) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Agregar a `NodeContent` los campos necesarios para la nueva estructura de 12 secciones +
2 checkpoints ("Comprueba tu avance"), y reordenar `node_detail.html` para mostrarlos — sin romper
ninguno de los ~2200 nodos ya publicados que todavía no tienen los campos nuevos rellenos.

**Architecture:** Migración aditiva en `apps/content/models/knowledge.py` (`NodeContent`), nuevo
servicio `apps/content/services/node_checkpoint_service.py` (calco de `reading_checkpoint_service.py`
con 2 placements en vez de 3), cálculo de contexto de checkpoints en `apps/learn/views.py`
(`_recurso_view`), y `templates/learn/node_detail.html` reordenado con fallback a los campos viejos
mientras no haya backfill.

**Tech Stack:** Django 6.0, sqlite/Postgres vía `config.settings.local`, `python manage.py test`.

## Global Constraints

- Spec de origen: `docs/backlog/2-arquitectura/nodos-estructura-editorial-12-secciones.md` — toda tarea
  implementa una fila de sus tablas de campos.
- Migración **aditiva únicamente** en esta fase: no se borran `objetivo`, `introduccion`, `resumen`,
  `explicacion` todavía (eso es un paso posterior, después del backfill de contenido real).
- `ejemplos`, `errores_frecuentes`, `procedimiento`, `estado`, `fuente` **no cambian de esquema**.
- Durante el desarrollo correr solo el módulo afectado (`python manage.py test apps.content` /
  `python manage.py test apps.learn`), nunca la suite completa por cada paso — regla del proyecto
  (`CLAUDE.md`). La suite completa se corre una sola vez al final, antes de considerar la fase cerrada.
- `--parallel` no funciona en Windows local — no usarlo.
- Todo texto de UI/tests en español, consistente con el resto del proyecto.

---

### Task 1: Campos nuevos en `NodeContent` + migración

**Files:**
- Modify: `apps/content/models/knowledge.py:167-224` (clase `NodeContent`)
- Create: `apps/content/migrations/0050_nodecontent_estructura_12_secciones.py`
- Test: `apps/content/tests/test_node_content_fields.py` (nuevo)

**Interfaces:**
- Produces: `NodeContent.resumen_inicial` (str), `.explicacion_simple` (str), `.explicacion_formal`
  (str), `.definiciones_clave` (str), `.propiedades_relaciones` (str), `.ejemplo_guiado` (dict, forma
  `{"enunciado": str, "pasos": [str, ...]}`), `.errores_correccion` (str), `.al_terminar_debes_poder`
  (str), `.checkpoints` (list de dicts, forma validada por Task 2).

- [ ] **Step 1: Escribir el test que falla**

Crear `apps/content/tests/test_node_content_fields.py`:

```python
from django.test import TestCase

from apps.content.models import KnowledgeNode, NodeContent


class NodeContentNewFieldsTests(TestCase):
    def setUp(self):
        self.node = KnowledgeNode.objects.create(
            semantic_id="MAT.TEST.NODO",
            code="99.99.99.99",
            node_type=KnowledgeNode.NODE_RECURSO,
            subject_abbr="MAT",
            name="Nodo de prueba",
            is_published=True,
        )

    def test_new_fields_default_to_empty(self):
        content = NodeContent.objects.create(node=self.node)

        self.assertEqual(content.resumen_inicial, "")
        self.assertEqual(content.explicacion_simple, "")
        self.assertEqual(content.explicacion_formal, "")
        self.assertEqual(content.definiciones_clave, "")
        self.assertEqual(content.propiedades_relaciones, "")
        self.assertEqual(content.ejemplo_guiado, {})
        self.assertEqual(content.errores_correccion, "")
        self.assertEqual(content.al_terminar_debes_poder, "")
        self.assertEqual(content.checkpoints, [])

    def test_new_fields_persist_after_save(self):
        content = NodeContent.objects.create(
            node=self.node,
            resumen_inicial="Resumen de apertura.",
            explicacion_simple="En palabras simples.",
            explicacion_formal="Definición formal.",
            definiciones_clave="Término: definición.",
            propiedades_relaciones="Propiedad: enunciado.",
            ejemplo_guiado={"enunciado": "Calcula X.", "pasos": ["Paso 1", "Paso 2"]},
            errores_correccion="Error común: por qué está mal y cómo corregirlo.",
            al_terminar_debes_poder="Resolver el procedimiento completo.",
            checkpoints=[
                {
                    "placement": "after_explicacion_formal",
                    "question": "¿Pregunta?",
                    "choices": [
                        {"text": "A", "is_correct": True},
                        {"text": "B", "is_correct": False},
                        {"text": "C", "is_correct": False},
                        {"text": "D", "is_correct": False},
                    ],
                    "explanation": "La correcta es A porque...",
                    "reinforcement_section": "Explicación formal",
                },
            ],
        )
        content.refresh_from_db()

        self.assertEqual(content.resumen_inicial, "Resumen de apertura.")
        self.assertEqual(content.ejemplo_guiado["pasos"], ["Paso 1", "Paso 2"])
        self.assertEqual(len(content.checkpoints), 1)
        self.assertEqual(content.checkpoints[0]["placement"], "after_explicacion_formal")
```

- [ ] **Step 2: Confirmar que falla**

Run: `python manage.py test apps.content.tests.test_node_content_fields -v 2`
Expected: `FieldError` / `AttributeError` — los campos no existen todavía.

- [ ] **Step 3: Agregar los campos al modelo**

En `apps/content/models/knowledge.py`, dentro de `class NodeContent(models.Model):`, después de la
línea `errores_frecuentes = models.JSONField(...)` (línea 195) y antes de `estado = models.CharField(...)`
(línea 196), insertar:

```python
    resumen_inicial = models.TextField(
        blank=True, verbose_name="resumen inicial"
    )
    explicacion_simple = models.TextField(
        blank=True, verbose_name="explicación en palabras simples"
    )
    explicacion_formal = models.TextField(
        blank=True, verbose_name="explicación formal"
    )
    definiciones_clave = models.TextField(
        blank=True, verbose_name="definiciones clave"
    )
    propiedades_relaciones = models.TextField(
        blank=True, verbose_name="propiedades y relaciones importantes"
    )
    ejemplo_guiado = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="ejemplo guiado",
        help_text='Forma: {"enunciado": str, "pasos": [str, ...]}',
    )
    errores_correccion = models.TextField(
        blank=True,
        verbose_name="errores frecuentes y cómo corregirlos",
        help_text="Texto explicativo; no reemplaza errores_frecuentes (fuente del V/F).",
    )
    al_terminar_debes_poder = models.TextField(
        blank=True, verbose_name="al terminar debes poder"
    )
    checkpoints = models.JSONField(
        default=list,
        blank=True,
        verbose_name="comprobaciones intermedias",
        help_text=(
            "Exactamente 2 checkpoints ('Comprueba tu avance'), validados por "
            "node_checkpoint_service."
        ),
    )
```

- [ ] **Step 4: Generar y revisar la migración**

Run: `python manage.py makemigrations content`
Expected: crea `apps/content/migrations/0050_nodecontent_estructura_12_secciones.py` (el número real
puede variar según el estado local; usar el que Django asigne) con 9 `AddField` sobre `nodecontent`,
todos con `blank=True` y sin `null=True` (coherente con el resto del modelo, que usa `""`/`[]`/`{}`
como vacío, no `NULL`).

- [ ] **Step 5: Aplicar la migración y correr los tests**

Run: `python manage.py migrate content`
Run: `python manage.py test apps.content.tests.test_node_content_fields -v 2`
Expected: PASS (2 tests)

- [ ] **Step 6: Commit**

```bash
git add apps/content/models/knowledge.py apps/content/migrations/ apps/content/tests/test_node_content_fields.py
git commit -m "feat: agrega campos de la nueva estructura editorial a NodeContent"
```

---

### Task 2: `node_checkpoint_service.py` — validación de checkpoints de nodo

**Files:**
- Create: `apps/content/services/node_checkpoint_service.py`
- Test: `apps/content/tests/test_node_checkpoint_service.py`

**Interfaces:**
- Consumes: nada (módulo autocontenido, sin imports de otros servicios).
- Produces: `CHECKPOINT_PLACEMENTS = ("after_explicacion_formal", "after_ejemplo_guiado")`,
  `normalize_node_checkpoints(value: list) -> list[dict]` (misma forma de retorno que
  `reading_checkpoint_service.normalize_reading_checkpoints`, con exactamente 2 elementos),
  `correct_choice_text(checkpoint: dict) -> str` (helper nuevo, usado por Task 3 para precomputar
  el contexto de la plantilla).

- [ ] **Step 1: Escribir el test que falla**

Crear `apps/content/tests/test_node_checkpoint_service.py`:

```python
from django.test import SimpleTestCase

from apps.content.services.node_checkpoint_service import (
    CHECKPOINT_PLACEMENTS,
    correct_choice_text,
    normalize_node_checkpoints,
)


def _checkpoints():
    return [
        {
            "placement": "after_explicacion_formal",
            "question": "¿Cuál es el opuesto de $-5$?",
            "choices": [
                {"text": "$5$", "is_correct": True},
                {"text": "$-5$", "is_correct": False},
                {"text": "$0$", "is_correct": False},
                {"text": "$1/5$", "is_correct": False},
            ],
            "explanation": "La alternativa correcta es $5$, el opuesto cambia el signo.",
            "reinforcement_section": "Explicación formal",
        },
        {
            "placement": "after_ejemplo_guiado",
            "question": "En el ejemplo guiado, ¿qué paso va primero?",
            "choices": [
                {"text": "Identificar los signos", "is_correct": True},
                {"text": "Sumar los valores absolutos", "is_correct": False},
                {"text": "Escribir el resultado", "is_correct": False},
                {"text": "Comprobar con la recta numérica", "is_correct": False},
            ],
            "explanation": "La alternativa correcta es identificar los signos, es el primer paso del ejemplo.",
            "reinforcement_section": "Ejemplo guiado",
        },
    ]


class NormalizeNodeCheckpointsTests(SimpleTestCase):
    def test_accepts_two_canonical_checkpoints(self):
        normalized = normalize_node_checkpoints(_checkpoints())

        self.assertEqual(len(normalized), 2)
        self.assertEqual(
            [item["placement"] for item in normalized], list(CHECKPOINT_PLACEMENTS)
        )

    def test_rejects_wrong_count(self):
        with self.assertRaisesRegex(ValueError, "exactamente dos"):
            normalize_node_checkpoints(_checkpoints()[:1])

    def test_rejects_duplicate_placement(self):
        checkpoints = _checkpoints()
        checkpoints[1]["placement"] = "after_explicacion_formal"

        with self.assertRaisesRegex(ValueError, "ubicación inválida o repetida"):
            normalize_node_checkpoints(checkpoints)

    def test_rejects_placement_outside_node_set(self):
        checkpoints = _checkpoints()
        checkpoints[0]["placement"] = "after_concept_image"

        with self.assertRaisesRegex(ValueError, "ubicación inválida o repetida"):
            normalize_node_checkpoints(checkpoints)

    def test_rejects_multiple_correct_choices(self):
        checkpoints = _checkpoints()
        checkpoints[0]["choices"][1]["is_correct"] = True

        with self.assertRaisesRegex(ValueError, "exactamente una alternativa correcta"):
            normalize_node_checkpoints(checkpoints)

    def test_rejects_explanation_that_does_not_mention_correct_choice(self):
        checkpoints = _checkpoints()
        checkpoints[0]["explanation"] = "Esta explicación no menciona la respuesta."

        with self.assertRaisesRegex(ValueError, "debe mencionar la alternativa correcta"):
            normalize_node_checkpoints(checkpoints)


class CorrectChoiceTextTests(SimpleTestCase):
    def test_returns_text_of_correct_choice(self):
        checkpoint = _checkpoints()[0]

        self.assertEqual(correct_choice_text(checkpoint), "$5$")
```

- [ ] **Step 2: Confirmar que falla**

Run: `python manage.py test apps.content.tests.test_node_checkpoint_service -v 2`
Expected: `ModuleNotFoundError: No module named 'apps.content.services.node_checkpoint_service'`

- [ ] **Step 3: Implementar el servicio**

Crear `apps/content/services/node_checkpoint_service.py`:

```python
"""Validation for the two formative checkpoints embedded in node guides.

Same contract as apps.content.services.reading_checkpoint_service (used by
Resource), but with 2 canonical placements instead of 3 — see
docs/backlog/2-arquitectura/nodos-estructura-editorial-12-secciones.md.
"""

from __future__ import annotations

CHECKPOINT_PLACEMENTS = (
    "after_explicacion_formal",
    "after_ejemplo_guiado",
)


def _text(value) -> str:
    return " ".join(str(value or "").split())


def normalize_node_checkpoints(value) -> list[dict]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("El nodo debe incluir exactamente dos comprobaciones intermedias.")

    normalized = []
    seen_questions = set()
    seen_placements = set()
    for index, checkpoint in enumerate(value, start=1):
        if not isinstance(checkpoint, dict):
            raise ValueError(f"Comprobación {index}: estructura inválida.")
        placement = _text(checkpoint.get("placement"))
        question = _text(checkpoint.get("question"))
        explanation = _text(checkpoint.get("explanation"))
        reinforcement_section = _text(checkpoint.get("reinforcement_section"))
        choices = checkpoint.get("choices")

        if placement not in CHECKPOINT_PLACEMENTS or placement in seen_placements:
            raise ValueError(f"Comprobación {index}: ubicación inválida o repetida.")
        if not question or question.casefold() in seen_questions:
            raise ValueError(f"Comprobación {index}: enunciado vacío o duplicado.")
        if not explanation or not reinforcement_section:
            raise ValueError(f"Comprobación {index}: faltan explicación o ruta de refuerzo.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError(f"Comprobación {index}: debe tener exactamente cuatro alternativas.")

        normalized_choices = []
        seen_choices = set()
        correct_count = 0
        correct_text = ""
        for choice_index, choice in enumerate(choices, start=1):
            if not isinstance(choice, dict):
                raise ValueError(f"Comprobación {index}, alternativa {choice_index}: estructura inválida.")
            choice_text = _text(choice.get("text"))
            choice_key = choice_text.casefold()
            is_correct = choice.get("is_correct") is True
            if not choice_text or choice_key in seen_choices:
                raise ValueError(f"Comprobación {index}: alternativas vacías o repetidas.")
            seen_choices.add(choice_key)
            correct_count += int(is_correct)
            if is_correct:
                correct_text = choice_text
            normalized_choices.append({"text": choice_text, "is_correct": is_correct})

        if correct_count != 1:
            raise ValueError(f"Comprobación {index}: debe tener exactamente una alternativa correcta.")
        if correct_text.casefold() not in explanation.casefold():
            raise ValueError(
                f"Comprobación {index}: la explicación debe mencionar la alternativa correcta."
            )

        seen_questions.add(question.casefold())
        seen_placements.add(placement)
        normalized.append(
            {
                "placement": placement,
                "question": question,
                "choices": normalized_choices,
                "explanation": explanation,
                "reinforcement_section": reinforcement_section,
            }
        )

    if seen_placements != set(CHECKPOINT_PLACEMENTS):
        raise ValueError("Las comprobaciones no cubren las dos ubicaciones canónicas.")
    return normalized


def correct_choice_text(checkpoint: dict) -> str:
    for choice in checkpoint.get("choices", []):
        if choice.get("is_correct"):
            return choice.get("text", "")
    return ""
```

- [ ] **Step 4: Correr los tests**

Run: `python manage.py test apps.content.tests.test_node_checkpoint_service -v 2`
Expected: PASS (7 tests)

- [ ] **Step 5: Commit**

```bash
git add apps/content/services/node_checkpoint_service.py apps/content/tests/test_node_checkpoint_service.py
git commit -m "feat: agrega node_checkpoint_service para validar Comprueba tu avance"
```

---

### Task 3: Contexto de checkpoints en la vista de recurso

**Files:**
- Modify: `apps/learn/views.py:170-221` (función `_recurso_view`)
- Test: `apps/learn/tests.py` (agregar clase nueva al final del archivo)

**Interfaces:**
- Consumes: `node_checkpoint_service.correct_choice_text` (Task 2), `NodeContent.checkpoints` (Task 1).
- Produces: contexto de plantilla `checkpoint_after_formal` (dict con `question`, `choices`,
  `explanation`, `correct_answer`, o `None`) y `checkpoint_after_ejemplo` (misma forma o `None`),
  usados por Task 4.

- [ ] **Step 1: Escribir el test que falla**

Agregar al final de `apps/learn/tests.py`:

```python
class NodeCheckpointRenderTests(TestCase):
    def setUp(self):
        self.asig, self.eje, self.bloque, self.tema, self.recurso = _build_tree()
        self.url = (
            f"/aprender/{self.asig.slug}/{self.eje.slug}/"
            f"{self.bloque.slug}/{self.tema.slug}/{self.recurso.slug}/"
        )

    def test_no_checkpoints_no_section(self):
        NodeContent.objects.create(node=self.recurso, estado=NodeContent.ESTADO_PUBLICADO)
        response = self.client.get(self.url)
        self.assertNotContains(response, "Comprueba tu avance")

    def test_checkpoint_after_formal_explanation_renders_with_choices(self):
        NodeContent.objects.create(
            node=self.recurso,
            estado=NodeContent.ESTADO_PUBLICADO,
            checkpoints=[
                {
                    "placement": "after_explicacion_formal",
                    "question": "¿Cuál es el opuesto de -5?",
                    "choices": [
                        {"text": "5", "is_correct": True},
                        {"text": "-5", "is_correct": False},
                        {"text": "0", "is_correct": False},
                        {"text": "10", "is_correct": False},
                    ],
                    "explanation": "La correcta es 5.",
                    "reinforcement_section": "Explicación formal",
                },
            ],
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Comprueba tu avance")
        self.assertContains(response, "¿Cuál es el opuesto de -5?")
        self.assertContains(response, 'data-answer="5"')
```

- [ ] **Step 2: Confirmar que falla**

Run: `python manage.py test apps.learn.tests.NodeCheckpointRenderTests -v 2`
Expected: FAIL — `assertNotContains`/`assertContains` fallan porque la vista no pasa nada de esto
todavía y la plantilla no tiene el bloque (fallará también más adelante hasta Task 4; en este paso
el fallo esperado es que "Comprueba tu avance" no aparece incluso cuando debería).

- [ ] **Step 3: Calcular el contexto en la vista**

En `apps/learn/views.py`, agregar el import al inicio del archivo (junto a los demás imports de
`apps.content`):

```python
from apps.content.services.node_checkpoint_service import correct_choice_text
```

Agregar una función auxiliar antes de `_recurso_view` (después de `_build_practice_bank`, línea 168):

```python
def _checkpoint_context(content, placement):
    if content is None:
        return None
    for checkpoint in content.checkpoints:
        if checkpoint.get("placement") == placement:
            return {
                "question": checkpoint["question"],
                "choices": [choice["text"] for choice in checkpoint["choices"]],
                "explanation": checkpoint["explanation"],
                "correct_answer": correct_choice_text(checkpoint),
            }
    return None
```

Dentro de `_recurso_view`, después de la línea `content = getattr(node, "content", None)` (línea 173),
agregar:

```python
    checkpoint_after_formal = _checkpoint_context(content, "after_explicacion_formal")
    checkpoint_after_ejemplo = _checkpoint_context(content, "after_ejemplo_guiado")
```

Y en el `return render(...)` (líneas 204-221), agregar dos claves al diccionario de contexto, junto
a `"mastery": ...`:

```python
            "checkpoint_after_formal": checkpoint_after_formal,
            "checkpoint_after_ejemplo": checkpoint_after_ejemplo,
```

- [ ] **Step 4: Correr el test (debe seguir fallando, falta Task 4)**

Run: `python manage.py test apps.learn.tests.NodeCheckpointRenderTests -v 2`
Expected: FAIL todavía — el contexto ya llega a la plantilla pero la plantilla no lo renderiza. Esto
es esperado en este paso; Task 4 lo hace pasar.

- [ ] **Step 5: Commit**

```bash
git add apps/learn/views.py apps/learn/tests.py
git commit -m "feat: calcula contexto de checkpoints de nodo en la vista de recurso"
```

---

### Task 4: Reordenar `node_detail.html` con las 12 secciones + checkpoints

**Files:**
- Modify: `templates/learn/node_detail.html:319-460` (bloque `{% else %}` del contenido)
- Create: `templates/learn/includes/_node_checkpoint.html` (partial reutilizable)

**Interfaces:**
- Consumes: `checkpoint_after_formal`, `checkpoint_after_ejemplo` (Task 3); campos nuevos de
  `content` (Task 1).

- [ ] **Step 1: Crear el partial de checkpoint**

Crear `templates/learn/includes/_node_checkpoint.html`:

```html
{% if checkpoint %}
<div class="learn-ejemplo-card learn-exercise" data-format="multiple_choice" data-answer="{{ checkpoint.correct_answer }}">
    <div class="learn-ejemplo-card__header">
        <span class="learn-ejemplo-card__num">Comprueba tu avance</span>
        <span class="learn-ejemplo-card__titulo">{{ checkpoint.question }}</span>
    </div>
    <div class="learn-ejemplo-card__body">
        <ul class="learn-exercise__mc">
            {% for ch in checkpoint.choices %}
            <li><button type="button" class="ex-choice" data-value="{{ ch }}">{{ ch }}</button></li>
            {% endfor %}
        </ul>
        <div class="learn-exercise__feedback" hidden>
            <div class="learn-exercise__verdict"></div>
            <div class="learn-exercise__explanation">{{ checkpoint.explanation|markdown }}</div>
        </div>
    </div>
</div>
{% endif %}
```

- [ ] **Step 2: Reordenar el bloque de contenido en `node_detail.html`**

Reemplazar todo el rango desde `{% if content.objetivo %}` (línea 321) hasta el cierre de la sección
"Ejemplos Verdadero/Falso" (línea 460 inclusive) por:

```html
    {% if content.resumen_inicial %}
    <section class="learn-section">
        <h2 class="learn-section__title">Resumen inicial</h2>
        <div class="resource-view__content">{{ content.resumen_inicial|markdown }}</div>
    </section>
    {% elif content.objetivo or content.introduccion %}
    {% if content.objetivo %}
    <div class="learn-objetivo-card">
        <span class="learn-objetivo-card__label">Objetivo</span>
        <p>{{ content.objetivo }}</p>
    </div>
    {% endif %}
    {% if content.introduccion %}
    <section class="learn-section learn-intro">
        <div class="learn-intro__body">{{ content.introduccion|markdown }}</div>
    </section>
    {% endif %}
    {% endif %}

    {% if content.explicacion_simple %}
    <section class="learn-section">
        <h2 class="learn-section__title">Explicación en palabras simples</h2>
        <div class="resource-view__content">{{ content.explicacion_simple|markdown }}</div>
    </section>
    {% endif %}

    {% if content.explicacion_formal %}
    <section class="learn-section">
        <h2 class="learn-section__title">Explicación formal</h2>
        <div class="resource-view__content">{{ content.explicacion_formal|markdown }}</div>
    </section>
    {% elif not content.explicacion_simple and content.explicacion %}
    <section class="learn-section">
        <h2 class="learn-section__title">Explicación</h2>
        <div class="resource-view__content">{{ content.explicacion|markdown }}</div>
    </section>
    {% endif %}

    {% include "learn/includes/_node_checkpoint.html" with checkpoint=checkpoint_after_formal %}

    {% if content.definiciones_clave %}
    <section class="learn-section">
        <h2 class="learn-section__title">Definiciones clave</h2>
        <div class="resource-view__content">{{ content.definiciones_clave|markdown }}</div>
    </section>
    {% endif %}

    {% if content.propiedades_relaciones %}
    <section class="learn-section">
        <h2 class="learn-section__title">Propiedades y relaciones importantes</h2>
        <div class="resource-view__content">{{ content.propiedades_relaciones|markdown }}</div>
    </section>
    {% endif %}

    {% if content.ejemplo_guiado.enunciado %}
    <section class="learn-section">
        <h2 class="learn-section__title">Ejemplo guiado</h2>
        <p class="resource-view__content">{{ content.ejemplo_guiado.enunciado|markdown }}</p>
        <ul class="learn-procedure">
            {% for paso in content.ejemplo_guiado.pasos %}
            <li class="learn-procedure__step">{{ paso|bold_step }}</li>
            {% endfor %}
        </ul>
    </section>
    {% endif %}

    {% include "learn/includes/_node_checkpoint.html" with checkpoint=checkpoint_after_ejemplo %}

    {% if content.procedimiento %}
    <section class="learn-section">
        <h2 class="learn-section__title">Procedimiento</h2>
        <ul class="learn-procedure">
            {% for paso in content.procedimiento %}
            <li class="learn-procedure__step">{{ paso|bold_step }}</li>
            {% endfor %}
        </ul>
    </section>
    {% endif %}

    {% if content.errores_correccion %}
    <section class="learn-section">
        <h2 class="learn-section__title">Errores frecuentes y cómo corregirlos</h2>
        <div class="resource-view__content">{{ content.errores_correccion|markdown }}</div>
    </section>
    {% endif %}

    {% if content.ejemplos %}
    <section class="learn-section">
        <h2 class="learn-section__title">Ejemplos</h2>
        <p class="learn-section__hint">Responde los siguientes ejercicios para poner a prueba lo que acabas de aprender.</p>
        <div class="learn-ejemplos-list">
            {% for ej in content.ejemplos %}
            {% if ej.respuesta == "Sí" or ej.respuesta == "No" %}
            <div class="learn-ejemplo-card learn-exercise"
                 data-format="true_false"
                 data-answer="{{ ej.respuesta }}">
                <div class="learn-ejemplo-card__header">
                    <span class="learn-ejemplo-card__num">{{ forloop.counter }}</span>
                    <span class="learn-ejemplo-card__titulo">{{ ej.enunciado|default:ej.titulo }}</span>
                </div>
                <div class="learn-ejemplo-card__body">
                    <div class="learn-exercise__tf">
                        <button type="button" class="ex-choice" data-value="Sí">Sí</button>
                        <button type="button" class="ex-choice" data-value="No">No</button>
                    </div>
                    <div class="learn-exercise__feedback" hidden>
                        <div class="learn-exercise__verdict"></div>
                        {% if ej.solucion_pasos %}
                        <ol class="learn-procedure" style="margin-top:.5rem">
                            {% for paso in ej.solucion_pasos %}<li class="learn-procedure__step">{{ paso }}</li>{% endfor %}
                        </ol>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% elif ej.respuesta == "Verdadero" or ej.respuesta == "Falso" %}
            <div class="learn-ejemplo-card learn-exercise"
                 data-format="true_false"
                 data-answer="{{ ej.respuesta }}">
                <div class="learn-ejemplo-card__header">
                    <span class="learn-ejemplo-card__num">{{ forloop.counter }}</span>
                    <span class="learn-ejemplo-card__titulo">{{ ej.enunciado|default:ej.titulo }}</span>
                </div>
                <div class="learn-ejemplo-card__body">
                    <div class="learn-exercise__tf">
                        <button type="button" class="ex-choice" data-value="Verdadero">Verdadero</button>
                        <button type="button" class="ex-choice" data-value="Falso">Falso</button>
                    </div>
                    <div class="learn-exercise__feedback" hidden>
                        <div class="learn-exercise__verdict"></div>
                        {% if ej.solucion_pasos %}
                        <ol class="learn-procedure" style="margin-top:.5rem">
                            {% for paso in ej.solucion_pasos %}<li class="learn-procedure__step">{{ paso }}</li>{% endfor %}
                        </ol>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% else %}
            <div class="learn-ejemplo-card learn-exercise"
                 data-format="open_answer"
                 data-answer="">
                <div class="learn-ejemplo-card__header">
                    <span class="learn-ejemplo-card__num">{{ forloop.counter }}</span>
                    <span class="learn-ejemplo-card__titulo">{{ ej.enunciado|default:ej.titulo }}</span>
                </div>
                <div class="learn-ejemplo-card__body">
                    <button type="button" class="ex-submit">Ver solución</button>
                    <div class="learn-exercise__feedback" hidden>
                        <div class="learn-exercise__verdict"></div>
                        {% if ej.solucion_pasos %}
                        <ol class="learn-procedure" style="margin-top:.5rem">
                            {% for paso in ej.solucion_pasos %}<li class="learn-procedure__step">{{ paso }}</li>{% endfor %}
                        </ol>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endif %}
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if content.errores_frecuentes %}
    <section class="learn-section conceptual-section">
        <h2 class="learn-section__title">Ejemplos Verdadero/Falso</h2>
        <p class="learn-section__hint">Decide si cada afirmación es verdadera o falsa antes de ver la explicación.</p>
        <div class="conceptual-list">
            {% for error in content.errores_frecuentes %}
            <div class="conceptual-item learn-exercise"
                data-format="true_false"
                data-answer="Falso">
                <div class="conceptual-item__claim"><span>"{{ error }}"</span></div>
                <div class="conceptual-item__body">
                    <div class="learn-exercise__tf">
                        <button type="button" class="ex-choice" data-value="Verdadero">Verdadero</button>
                        <button type="button" class="ex-choice" data-value="Falso">Falso</button>
                    </div>
                    <div class="learn-exercise__feedback" hidden>
                        <div class="learn-exercise__verdict"></div>
                        <p style="margin-top:.4rem;font-size:.9rem;color:#374151;">
                            Esta afirmación describe un error frecuente: es <strong>incorrecta</strong>.
                        </p>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
    {% endif %}

    {% if content.al_terminar_debes_poder %}
    <section class="learn-section">
        <h2 class="learn-section__title">Al terminar debes poder</h2>
        <div class="resource-view__content">{{ content.al_terminar_debes_poder|markdown }}</div>
    </section>
    {% endif %}
```

No tocar las secciones que siguen ("Material adicional", "Fuente", tarjeta `resumen` legacy) — quedan
exactamente donde están hoy, después de este bloque. La tarjeta `resumen` legacy (líneas 489-494 del
archivo original) sigue con su guardia `{% if content and content.resumen %}` intacta: mientras
`resumen_inicial` esté vacío en un nodo, esa tarjeta legacy sigue mostrando el resumen viejo al final;
en cuanto el nodo se reescriba con `resumen_inicial`, dejará de aparecer duplicada porque el campo
`resumen` viejo se vacía en el mismo backfill.

- [ ] **Step 3: Correr los tests de Task 3 (ahora deben pasar) y los de regresión de la vista**

Run: `python manage.py test apps.learn -v 2`
Expected: PASS — todos los tests de `apps/learn/tests.py`, incluidos los nuevos de
`NodeCheckpointRenderTests` y los existentes (`NodeDetailViewTests` etc., que siguen viendo el
contenido legacy en `test_recurso_with_content_shows_sections`, porque ese test solo usa `objetivo`/
`explicacion`, que ahora caen en las ramas `{% elif %}`).

- [ ] **Step 4: Commit**

```bash
git add templates/learn/node_detail.html templates/learn/includes/_node_checkpoint.html
git commit -m "feat: reordena node_detail.html a la estructura de 12 secciones con fallback legacy"
```

---

### Task 5: Verificación manual en navegador + barrera completa

**Files:** ninguno nuevo — solo verificación.

- [ ] **Step 1: Levantar el servidor de desarrollo y revisar un nodo existente sin backfill**

Usar el preview del proyecto (`python manage.py runserver` vía la herramienta de browser del
harness, no Bash) y abrir un recurso real, por ejemplo
`/aprender/matematicas/numeros/enteros/el-conjunto-de-los-numeros-enteros-y-orden/identificacion-de-los-numeros-naturales-n/`
(ajustar slug real si difiere). Confirmar que se ve exactamente igual que antes de este cambio
(fallback legacy activo, sin secciones nuevas vacías, sin errores 500).

- [ ] **Step 2: Crear un `NodeContent` de prueba con las 12 secciones + 2 checkpoints completos**
      (vía shell o admin) sobre un nodo cualquiera de prueba, y verificar en el navegador:
      orden correcto, los dos checkpoints responden igual que los ejercicios existentes (click →
      feedback correcto/incorrecto con KaTeX si aplica), sin scroll horizontal falso (regresión
      KaTeX ya cerrada, no reintroducirla).

- [ ] **Step 3: Barrera completa antes de cerrar la fase**

Run: `python manage.py test`
Run: `python manage.py check --deploy`
Run: `python manage.py makemigrations --check --dry-run`
Expected: los tres verdes / sin cambios pendientes.

- [ ] **Step 4: Commit final de la fase (si quedó algo suelto) y mover la tarjeta**

```bash
git mv docs/backlog/2-arquitectura/nodos-estructura-editorial-12-secciones.md docs/backlog/6-finalizados/
```

Completar la sección "Qué se hizo" del handoff antes de moverlo, y avisar al usuario que la
infraestructura está lista para empezar el backfill de contenido del bloque `enteros`
(`MAT.NUM` `02.01`, 36 recursos: `ENTEROS_CONJUNTO` 15 + `ENTEROS_OPERATORIA` 21) como proyecto de
contenido aparte, según lo dejado explícito en "No-objetivos" del handoff.

from copy import deepcopy

from django.test import SimpleTestCase

from apps.content.services.editorial_guide_service import THEORETICAL_RESOURCE_PROFILE
from apps.content.services.publication_pipeline_service import (
    PipelineError,
    has_malformed_math,
    validate_editorial_content,
)


def _checkpoint(placement, number):
    correct = f"Criterio correcto {number}"
    return {
        "placement": placement,
        "question": f"¿Qué opción aplica correctamente el criterio {number}?",
        "choices": [
            {"text": correct, "is_correct": True},
            {"text": f"Distractor A {number}", "is_correct": False},
            {"text": f"Distractor B {number}", "is_correct": False},
            {"text": f"Distractor C {number}", "is_correct": False},
        ],
        "explanation": f"La alternativa correcta es {correct}, porque respeta la condición indicada.",
        "reinforcement_section": "Explicación formal",
    }


def _content():
    return """
## Resumen inicial

### Pregunta de activación

¿Qué criterio permite reconocer el fenómeno antes de comenzar el procedimiento?

### Propósito

Comprender el concepto, justificar su formulación y aplicarlo de manera verificable.

### Antes de comenzar

Debes distinguir las magnitudes principales y reconocer la notación utilizada.

### Recorrido

Partiremos con una lectura sencilla, la formalizaremos y resolveremos un caso.

## Explicación en palabras simples

La idea puede entenderse como una relación estable entre aquello que observamos y
una regla que permite decidir. Primero identificamos qué cambia, qué permanece y
qué información resulta relevante. Esa lectura cotidiana orienta el razonamiento
antes de introducir símbolos o ejecutar operaciones.

## Explicación formal

Formalmente, el concepto se define mediante un criterio que relaciona las variables
relevantes. La regla establece las condiciones en que puede utilizarse, mientras
que la notación representa el vínculo sin ambigüedad. Toda aplicación debe respetar
esas condiciones y conservar el significado de cada variable.

## Definiciones clave

- **Concepto:** definición operativa.
- **Criterio:** condición que permite decidir.

## Propiedades y relaciones importantes

- La relación conserva sus condiciones de validez.
- El resultado debe ser coherente con la definición.

## Ejemplo guiado

Se analiza una situación concreta con información suficiente.

### 1. Qué se hace

Se identifican los datos y se selecciona la relación pertinente.

### 2. Por qué se hace así

La relación conecta exactamente las magnitudes presentes.

### 3. Qué regla lo permite

La definición formal autoriza la operación bajo esas condiciones.

### 4. Cómo se comprueba

Se contrasta el resultado con el contexto y las condiciones iniciales.

## Procedimiento

### Método general

1. Identifica los datos.
2. Selecciona la regla.
3. Aplica y comprueba.

### Variaciones que debes reconocer

- Caso directo.
- Caso con información equivalente.
- Caso que exige descartar información.

## Errores frecuentes y cómo corregirlos

### No confundir

- No confundas el concepto con una magnitud relacionada.

### Errores frecuentes

- **Error:** aplicar la regla fuera de sus condiciones. **Corrección:** verifica primero el dominio.

## Al terminar debes poder

Debes poder reconocer las variables del concepto, explicar la regla formal que las
conecta, seleccionar el procedimiento pertinente y comprobar la solución
contrastando las condiciones de uso, las unidades o relaciones involucradas y el
sentido del resultado obtenido en la situación planteada.
""".strip()


def _package():
    return {
        "metadata": {
            "resource_title": "Recurso teórico",
            "youtube_title": "Recurso teórico explicado",
            "resource_description": "Descripción completa del recurso teórico.",
            "youtube_description": "Descripción completa para YouTube.",
            "introduction": "Introducción al contenido del recurso.",
            "guide_title": "Guía teórica interactiva",
            "pedagogical_document": "Documento pedagógico del recurso.",
        },
        "guide": {
            "profile": THEORETICAL_RESOURCE_PROFILE,
            "content": _content(),
            "checkpoints": [
                _checkpoint("after_concept_image", 1),
                _checkpoint("after_guided_example", 2),
                _checkpoint("after_errors", 3),
            ],
        },
        "concept_image": {
            "formal_summary": "Representa la definición formal, sus variables y todas las condiciones exactas de aplicación.",
            "plain_language_summary": "Muestra la misma relación mediante una situación sencilla para interpretar claramente cada elemento.",
        },
        "infographic": {
            "coverage": [
                "resumen",
                "definiciones",
                "formulas_relaciones",
                "ejemplo",
                "procedimiento",
                "errores",
                "sintesis_final",
            ]
        },
    }


class TheoreticalResourceProfileTests(SimpleTestCase):
    def test_display_math_does_not_shift_following_inline_delimiters(self):
        content = (
            r"Definición: $$\frac{a}{b},\qquad a,b\in\mathbb Z,\quad b\neq0.$$ "
            r"En $\frac{a}{b}$, $a$ es el numerador y $b$ es el denominador."
        )

        self.assertFalse(has_malformed_math(content))

    def test_accepts_complete_theoretical_profile(self):
        normalized = validate_editorial_content(_package())

        self.assertEqual(normalized["guide"]["profile"], THEORETICAL_RESOURCE_PROFILE)
        self.assertEqual(len(normalized["guide"]["checkpoints"]), 3)

    def test_rejects_theoretical_profile_without_checkpoints(self):
        package = _package()
        del package["guide"]["checkpoints"]

        with self.assertRaisesRegex(PipelineError, "tres comprobaciones"):
            validate_editorial_content(package)

    def test_rejects_theoretical_profile_without_visual_briefs(self):
        package = _package()
        del package["concept_image"]

        with self.assertRaisesRegex(PipelineError, "briefs completos"):
            validate_editorial_content(package)

    def test_legacy_content_without_profile_remains_supported(self):
        package = deepcopy(_package())
        del package["guide"]["profile"]
        del package["guide"]["checkpoints"]
        del package["concept_image"]
        del package["infographic"]

        normalized = validate_editorial_content(package)

        self.assertNotIn("profile", normalized["guide"])

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

    def test_accepts_answer_mentioned_with_different_katex_delimiters(self):
        checkpoints = _checkpoints()
        checkpoints[0]["choices"][0]["text"] = "$-7^\\circ\\text{C}$"
        checkpoints[0]["choices"][1]["text"] = "$7^\\circ\\text{C}$"
        checkpoints[0]["explanation"] = (
            "$\\Delta T = T_f - T_i = 18 - 25 = -7^\\circ\\text{C}$."
        )

        normalize_node_checkpoints(checkpoints)  # no raise

    def test_accepts_answer_with_trailing_parenthetical_gloss(self):
        checkpoints = _checkpoints()
        checkpoints[0]["choices"][0]["text"] = (
            "$k = \\frac{T}{\\sum c_i}$ (Total dividido por la suma de los índices)"
        )
        checkpoints[0]["choices"][1]["text"] = "$k = T \\cdot \\sum c_i$"
        checkpoints[0]["explanation"] = (
            "La alternativa correcta es '$k = \\frac{T}{\\sum c_i}$'."
        )

        normalize_node_checkpoints(checkpoints)  # no raise

    def test_accepts_coordinate_pair_answer_without_math_delimiters(self):
        checkpoints = _checkpoints()
        checkpoints[0]["choices"][0]["text"] = "(0, 7)"
        checkpoints[0]["choices"][1]["text"] = "(7, 0)"
        checkpoints[0]["explanation"] = (
            "La alternativa correcta es '(0, 7)'. Toda función $f(x) = c$ corta al eje Y en $(0, c)$."
        )

        normalize_node_checkpoints(checkpoints)  # no raise

    def test_accepts_prose_choice_whose_math_span_is_in_the_explanation(self):
        checkpoints = _checkpoints()
        checkpoints[0]["choices"][0]["text"] = "Dividir el valor final por $1,15$"
        checkpoints[0]["choices"][1]["text"] = "Multiplicar el valor final por $1,15$"
        checkpoints[0]["explanation"] = (
            "El cálculo inverso exige dividir por el factor: $V_i = \\frac{V_f}{1,15}$."
        )

        normalize_node_checkpoints(checkpoints)  # no raise


class CorrectChoiceTextTests(SimpleTestCase):
    def test_returns_text_of_correct_choice(self):
        checkpoint = _checkpoints()[0]

        self.assertEqual(correct_choice_text(checkpoint), "$5$")

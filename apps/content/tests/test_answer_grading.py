import os
import signal
import tempfile
import time
from types import SimpleNamespace
from unittest import skipUnless
from unittest.mock import patch

from django.test import SimpleTestCase

from apps.content.services.answer_grading_service import (
    MAX_ALGEBRA_LENGTH,
    grade_answer,
    validate_direct_answer_config,
)


def question(question_type, canonical_answer, tolerance=None):
    return SimpleNamespace(
        question_type=question_type,
        canonical_answer=canonical_answer,
        answer_tolerance=tolerance,
    )


class NumericAnswerGradingTests(SimpleTestCase):
    def test_accepts_equivalent_integer_decimal_comma_and_fraction(self):
        numeric = question("numerica", "1/2")
        for answer in ("0.5", "0,5", "1/2"):
            with self.subTest(answer=answer):
                result = grade_answer(numeric, answer)
                self.assertTrue(result["correct"])
                self.assertEqual(result["reason"], "correct")

    def test_uses_absolute_tolerance(self):
        numeric = question("numerica", "10", 0.1)
        self.assertTrue(grade_answer(numeric, "10.1")["correct"])
        self.assertFalse(grade_answer(numeric, "10.1001")["correct"])

    def test_exact_comparison_when_tolerance_is_empty_or_zero(self):
        self.assertFalse(
            grade_answer(question("numerica", "1", None), "1.0001")["correct"]
        )
        self.assertFalse(
            grade_answer(question("numerica", "1", 0), "1.0001")["correct"]
        )

    def test_rejects_invalid_numeric_formats(self):
        numeric = question("numerica", "1")
        for answer in (
            "",
            "1/0",
            "1e3",
            "NaN",
            "Infinity",
            "1,000.5",
            "1 + 1",
            "50%",
        ):
            with self.subTest(answer=answer):
                result = grade_answer(numeric, answer)
                self.assertFalse(result["correct"])
                self.assertIn(
                    result["reason"],
                    {"empty", "invalid_format"},
                )

    def test_rejects_numeric_limits_and_invalid_canonical_config(self):
        too_many_digits = "1" * 31
        self.assertEqual(
            grade_answer(question("numerica", "1"), too_many_digits)["reason"],
            "limits_exceeded",
        )
        self.assertEqual(
            grade_answer(question("numerica", "not-a-number"), "1")["reason"],
            "invalid_canonical",
        )
        self.assertEqual(
            grade_answer(question("numerica", "1", float("inf")), "1")["reason"],
            "invalid_canonical",
        )
        self.assertEqual(
            grade_answer(question("numerica", "1", -0.1), "1")["reason"],
            "invalid_canonical",
        )


class AlgebraicAnswerGradingTests(SimpleTestCase):
    def test_accepts_expansion_implicit_multiplication_and_power_alias(self):
        algebraic = question("algebraica", "2*x + 2")
        for answer in ("2(x+1)", "2x+2"):
            with self.subTest(answer=answer):
                self.assertTrue(grade_answer(algebraic, answer)["correct"])

        power = question("algebraica", "x**2 - 1")
        self.assertTrue(grade_answer(power, "x^2-1")["correct"])

    def test_accepts_formally_equivalent_rational_expressions(self):
        algebraic = question("algebraica", "x + 1")
        result = grade_answer(algebraic, "(x^2-1)/(x-1)")
        self.assertTrue(result["correct"])

    def test_rejects_non_equivalent_and_extra_variables(self):
        algebraic = question("algebraica", "x + 1")
        self.assertFalse(grade_answer(algebraic, "x+2")["correct"])
        self.assertEqual(
            grade_answer(algebraic, "x+y")["reason"],
            "invalid_format",
        )

    def test_rejects_calls_attributes_code_and_unsupported_syntax(self):
        algebraic = question("algebraica", "x + 1")
        payloads = (
            "__import__('os').system('echo unsafe')",
            "open('file')",
            "x.__class__",
            "x[0]",
            "[x for x in (1,2)]",
            "lambda: 1",
            "x = 1",
            "sqrt(x)",
            "Symbol('x')",
            "x;1",
            "x\n+1",
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                result = grade_answer(algebraic, payload)
                self.assertFalse(result["correct"])
                self.assertEqual(result["reason"], "invalid_format")

    def test_malicious_input_is_never_executed(self):
        handle, marker = tempfile.mkstemp()
        os.close(handle)
        os.unlink(marker)
        try:
            payload = (
                f"__import__('pathlib').Path({marker!r}).write_text('owned')"
            )
            result = grade_answer(question("algebraica", "x"), payload)
            self.assertEqual(result["reason"], "invalid_format")
            self.assertFalse(os.path.exists(marker))
        finally:
            if os.path.exists(marker):
                os.unlink(marker)

    def test_enforces_length_variables_exponents_and_operator_limits(self):
        algebraic = question("algebraica", "x")
        self.assertEqual(
            grade_answer(algebraic, "x" * (MAX_ALGEBRA_LENGTH + 1))["reason"],
            "limits_exceeded",
        )
        self.assertEqual(
            grade_answer(question("algebraica", "w+x+y+z"), "w+x+y+z")[
                "reason"
            ],
            "invalid_canonical",
        )
        self.assertEqual(
            grade_answer(algebraic, "x**9")["reason"],
            "limits_exceeded",
        )
        self.assertEqual(
            grade_answer(algebraic, "+".join(["x"] * 32))["reason"],
            "limits_exceeded",
        )
        deeply_nested = "(" * 13 + "x" + ")" * 13
        self.assertEqual(
            grade_answer(algebraic, deeply_nested)["reason"],
            "limits_exceeded",
        )

    def test_rejects_stacked_exponent_degree_blowup(self):
        # El apilamiento de potencias `(...**n)**m` evade el tope por-exponente
        # (cada `**` es <=8) pero el grado efectivo crece geométricamente y, al
        # expandirse en `cancel`, explota en memoria/CPU. El tope de grado total
        # debe cortarlo antes de ese paso caro.
        algebraic = question("algebraica", "x")
        for payload in (
            "((x+y+z)**8)**8",
            "(((x+1)**4)**4)**4",
            "((((x+y+z)**8)**8)**8)**8",
        ):
            with self.subTest(payload=payload):
                self.assertEqual(
                    grade_answer(algebraic, payload)["reason"],
                    "limits_exceeded",
                )
        # Un grado total dentro del tope sigue evaluándose normalmente.
        self.assertEqual(
            grade_answer(question("algebraica", "x**4"), "(x**2)**2")["reason"],
            "correct",
        )

    def test_rejects_invalid_canonical_and_algebraic_tolerance(self):
        self.assertEqual(
            grade_answer(question("algebraica", "sqrt(x)"), "x")["reason"],
            "invalid_canonical",
        )
        self.assertEqual(
            grade_answer(question("algebraica", "x", 0.1), "x")["reason"],
            "invalid_canonical",
        )
        self.assertEqual(
            grade_answer(question("algebraica", "x/(x-x)"), "1")["reason"],
            "invalid_canonical",
        )

    def test_validate_direct_answer_config(self):
        self.assertIsNone(
            validate_direct_answer_config(question("numerica", "3/4"))
        )
        self.assertIsNone(
            validate_direct_answer_config(question("algebraica", "2x+1"))
        )
        self.assertEqual(
            validate_direct_answer_config(question("algebraica", "sqrt(x)")),
            "invalid_canonical",
        )

    @skipUnless(
        hasattr(signal, "SIGALRM") and hasattr(signal, "setitimer"),
        "Wall-clock grading timeout requires SIGALRM.",
    )
    def test_symbolic_work_has_wall_clock_timeout(self):
        algebraic = question("algebraica", "x + 1")

        def slow_together(expression):
            time.sleep(1)
            return expression

        with patch(
            "apps.content.services.answer_grading_service.sympy.together",
            side_effect=slow_together,
        ):
            result = grade_answer(algebraic, "x+1")
        self.assertEqual(result["reason"], "grading_timeout")

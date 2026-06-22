"""Safe, deterministic grading for numeric and algebraic direct answers.

Untrusted strings are parsed with a strict tokenizer and Python's AST parser.
They are never passed to SymPy string parsers or dynamic code execution APIs.
"""

import ast
import re
import signal
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from fractions import Fraction

import sympy

MAX_NUMERIC_LENGTH = 100
MAX_NUMERIC_DIGITS = 30
MAX_ALGEBRA_LENGTH = 200
MAX_AST_NODES = 80
MAX_OPERATORS = 30
MAX_VARIABLES = 3
MAX_EXPONENT_ABS = 8
MAX_INTEGER_DIGITS = 12
MAX_NESTING = 12
MAX_RESULT_OPS = 120
MAX_TOTAL_DEGREE = 32
GRADING_TIMEOUT_SECONDS = 0.5

_INTEGER_RE = re.compile(r"[+-]?\d+\Z")
_DECIMAL_RE = re.compile(r"[+-]?\d+[.,]\d+\Z")
_FRACTION_RE = re.compile(r"([+-]?\d+)/(\d+)\Z")
_TOKEN_RE = re.compile(
    r"(?P<SPACE>[ \t]+)"
    r"|(?P<NUMBER>\d+(?:[.,]\d+)?)"
    r"|(?P<NAME>[a-z])"
    r"|(?P<POWER>\*\*|\^)"
    r"|(?P<OP>[+\-*/()])"
)


class _InvalidFormat(ValueError):
    pass


class _LimitsExceeded(ValueError):
    pass


class _GradingTimeout(TimeoutError):
    pass


@dataclass(frozen=True)
class _AlgebraicValue:
    expression: sympy.Expr
    normalized: str
    variables: frozenset[str]


def _result(correct=False, normalized="", reason="incorrect"):
    return {
        "correct": bool(correct),
        "normalized": normalized,
        "reason": reason,
    }


def _parse_numeric(raw_text):
    text = str(raw_text).strip()
    if not text:
        raise _InvalidFormat
    if len(text) > MAX_NUMERIC_LENGTH:
        raise _LimitsExceeded
    if sum(char.isdigit() for char in text) > MAX_NUMERIC_DIGITS:
        raise _LimitsExceeded

    fraction_match = _FRACTION_RE.fullmatch(text)
    try:
        if fraction_match:
            numerator = int(fraction_match.group(1))
            denominator = int(fraction_match.group(2))
            if denominator == 0:
                raise _InvalidFormat
            value = Fraction(numerator, denominator)
            normalized = str(value)
        elif _INTEGER_RE.fullmatch(text):
            value = Fraction(int(text), 1)
            normalized = str(value.numerator)
        elif _DECIMAL_RE.fullmatch(text):
            normalized = text.replace(",", ".")
            value = Fraction(Decimal(normalized))
        else:
            raise _InvalidFormat
    except (InvalidOperation, OverflowError, ValueError) as exc:
        raise _InvalidFormat from exc
    return value, normalized


def _parse_tolerance(raw_tolerance):
    if raw_tolerance in (None, ""):
        return Fraction(0, 1)
    try:
        tolerance_decimal = Decimal(str(raw_tolerance))
    except (InvalidOperation, ValueError) as exc:
        raise _InvalidFormat from exc
    if not tolerance_decimal.is_finite() or tolerance_decimal < 0:
        raise _InvalidFormat
    return Fraction(tolerance_decimal)


def _tokenize_algebraic(raw_text):
    text = str(raw_text).strip()
    if not text:
        raise _InvalidFormat
    if len(text) > MAX_ALGEBRA_LENGTH:
        raise _LimitsExceeded
    if re.search(r"[a-z]{2,}[ \t]*\(", text):
        raise _InvalidFormat

    tokens = []
    position = 0
    parenthesis_depth = 0
    while position < len(text):
        match = _TOKEN_RE.match(text, position)
        if not match:
            raise _InvalidFormat
        position = match.end()
        kind = match.lastgroup
        value = match.group()
        if kind == "SPACE":
            continue
        if kind == "NUMBER":
            if sum(char.isdigit() for char in value) > MAX_INTEGER_DIGITS:
                raise _LimitsExceeded
            value = value.replace(",", ".")
        elif kind == "POWER":
            value = "**"
            kind = "OP"
        if value == "(":
            parenthesis_depth += 1
            if parenthesis_depth > MAX_NESTING:
                raise _LimitsExceeded
        elif value == ")":
            parenthesis_depth -= 1
            if parenthesis_depth < 0:
                raise _InvalidFormat
        tokens.append((kind, value))

    if not tokens:
        raise _InvalidFormat
    if parenthesis_depth != 0:
        raise _InvalidFormat

    normalized = []
    previous = None
    for current in tokens:
        if previous and _needs_implicit_multiplication(previous, current):
            normalized.append("*")
        elif previous and previous[0] == "NUMBER" and current[0] == "NUMBER":
            raise _InvalidFormat
        normalized.append(current[1])
        previous = current
    return "".join(normalized)


def _needs_implicit_multiplication(previous, current):
    previous_ends_atom = (
        previous[0] in {"NUMBER", "NAME"} or previous[1] == ")"
    )
    current_starts_atom = (
        current[0] in {"NUMBER", "NAME"} or current[1] == "("
    )
    if not (previous_ends_atom and current_starts_atom):
        return False
    return not (previous[0] == "NUMBER" and current[0] == "NUMBER")


def _tree_depth(node):
    children = list(ast.iter_child_nodes(node))
    if not children:
        return 1
    return 1 + max(_tree_depth(child) for child in children)


def _degree_upper_bound(node):
    """Cota superior del grado polinomial total del AST (ya validado por el builder).

    Se calcula sobre el AST sin construir objetos SymPy: las potencias `evaluate=False`
    no se aplanan, así que `(x**3)**3` parece grado bajo en `count_ops` pero al expandirse
    en `cancel` cuesta como grado 9. Aquí se multiplica el grado de la base por el exponente
    literal, de modo que el apilamiento de potencias se acota antes del paso caro.
    """
    if isinstance(node, ast.Expression):
        return _degree_upper_bound(node.body)
    if isinstance(node, ast.Name):
        return 1
    if isinstance(node, ast.UnaryOp):
        return _degree_upper_bound(node.operand)
    if isinstance(node, ast.BinOp):
        left = _degree_upper_bound(node.left)
        if isinstance(node.op, ast.Pow):
            exponent_node = node.right
            if isinstance(exponent_node, ast.UnaryOp):
                exponent_node = exponent_node.operand
            # El builder ya garantizó que el exponente es un entero literal acotado.
            return left * abs(exponent_node.value)
        right = _degree_upper_bound(node.right)
        if isinstance(node.op, (ast.Mult, ast.Div)):
            return left + right
        return max(left, right)
    return 0


class _SafeExpressionBuilder:
    _BINARY_OPERATORS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)
    _UNARY_OPERATORS = (ast.UAdd, ast.USub)

    def __init__(self, source):
        self.source = source
        self.symbols = {}

    def build(self, node):
        if isinstance(node, ast.Expression):
            return self.build(node.body)
        if isinstance(node, ast.Constant):
            return self._constant(node)
        if isinstance(node, ast.Name):
            if not re.fullmatch(r"[a-z]", node.id):
                raise _InvalidFormat
            return self.symbols.setdefault(node.id, sympy.Symbol(node.id))
        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, self._UNARY_OPERATORS
        ):
            operand = self.build(node.operand)
            return operand if isinstance(node.op, ast.UAdd) else -operand
        if isinstance(node, ast.BinOp) and isinstance(
            node.op, self._BINARY_OPERATORS
        ):
            if isinstance(node.op, ast.Pow):
                exponent = self._literal_exponent(node.right)
                base = self.build(node.left)
                return sympy.Pow(base, exponent, evaluate=False)
            left = self.build(node.left)
            right = self.build(node.right)
            if isinstance(node.op, ast.Add):
                return sympy.Add(left, right, evaluate=False)
            if isinstance(node.op, ast.Sub):
                return sympy.Add(left, -right, evaluate=False)
            if isinstance(node.op, ast.Mult):
                return sympy.Mul(left, right, evaluate=False)
            if right == 0:
                raise _InvalidFormat
            return sympy.Mul(
                left,
                sympy.Pow(right, -1, evaluate=False),
                evaluate=False,
            )
        raise _InvalidFormat

    def _constant(self, node):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise _InvalidFormat
        source_value = ast.get_source_segment(self.source, node)
        if source_value is None:
            raise _InvalidFormat
        if "." in source_value:
            try:
                decimal_value = Decimal(source_value)
            except InvalidOperation as exc:
                raise _InvalidFormat from exc
            if not decimal_value.is_finite():
                raise _InvalidFormat
            return sympy.Rational(
                int(decimal_value.as_integer_ratio()[0]),
                int(decimal_value.as_integer_ratio()[1]),
            )
        if not source_value.isdigit():
            raise _InvalidFormat
        if len(source_value) > MAX_INTEGER_DIGITS:
            raise _LimitsExceeded
        return sympy.Integer(source_value)

    def _literal_exponent(self, node):
        sign = 1
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            sign = -1
            node = node.operand
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            node = node.operand
        if (
            not isinstance(node, ast.Constant)
            or isinstance(node.value, bool)
            or not isinstance(node.value, int)
        ):
            raise _InvalidFormat
        exponent = sign * node.value
        if abs(exponent) > MAX_EXPONENT_ABS:
            raise _LimitsExceeded
        return exponent


def _parse_algebraic(raw_text):
    normalized = _tokenize_algebraic(raw_text)
    try:
        tree = ast.parse(normalized, mode="eval")
    except (SyntaxError, ValueError) as exc:
        raise _InvalidFormat from exc

    nodes = list(ast.walk(tree))
    if len(nodes) > MAX_AST_NODES or _tree_depth(tree) > MAX_NESTING:
        raise _LimitsExceeded
    operator_count = sum(
        isinstance(node, (ast.BinOp, ast.UnaryOp)) for node in nodes
    )
    if operator_count > MAX_OPERATORS:
        raise _LimitsExceeded

    builder = _SafeExpressionBuilder(normalized)
    expression = builder.build(tree)
    # Acotar el grado total ANTES del paso caro (`cancel`/`together`): las potencias
    # anidadas evaden el tope por-exponente y, expandidas, explotan en memoria/CPU.
    if _degree_upper_bound(tree) > MAX_TOTAL_DEGREE:
        raise _LimitsExceeded
    variables = frozenset(str(symbol) for symbol in expression.free_symbols)
    if len(variables) > MAX_VARIABLES:
        raise _LimitsExceeded
    if sympy.count_ops(expression) > MAX_RESULT_OPS:
        raise _LimitsExceeded
    if expression.has(sympy.zoo, sympy.nan, sympy.oo, -sympy.oo):
        raise _InvalidFormat
    symbols = sorted(expression.free_symbols, key=lambda symbol: symbol.name)
    if expression.is_rational_function(*symbols) is not True:
        raise _InvalidFormat
    checked_expression = sympy.together(expression)
    if sympy.count_ops(checked_expression) > MAX_RESULT_OPS:
        raise _LimitsExceeded
    if checked_expression.has(sympy.zoo, sympy.nan, sympy.oo, -sympy.oo):
        raise _InvalidFormat
    return _AlgebraicValue(expression, normalized, variables)


@contextmanager
def _grading_timeout():
    can_use_alarm = (
        hasattr(signal, "SIGALRM")
        and hasattr(signal, "setitimer")
        and threading.current_thread() is threading.main_thread()
    )
    if not can_use_alarm:
        yield
        return

    def handle_timeout(signum, frame):
        raise _GradingTimeout

    previous_handler = signal.getsignal(signal.SIGALRM)
    previous_timer = signal.getitimer(signal.ITIMER_REAL)
    signal.signal(signal.SIGALRM, handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, GRADING_TIMEOUT_SECONDS)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
        if previous_timer[0] > 0:
            signal.setitimer(signal.ITIMER_REAL, *previous_timer)


def _grade_numeric(question, raw_text):
    try:
        canonical, _ = _parse_numeric(question.canonical_answer)
        tolerance = _parse_tolerance(question.answer_tolerance)
    except (_InvalidFormat, _LimitsExceeded):
        return _result(reason="invalid_canonical")
    try:
        student, normalized = _parse_numeric(raw_text)
    except _LimitsExceeded:
        return _result(reason="limits_exceeded")
    except _InvalidFormat:
        return _result(reason="invalid_format")
    correct = abs(student - canonical) <= tolerance
    return _result(
        correct=correct,
        normalized=normalized,
        reason="correct" if correct else "incorrect",
    )


def _grade_algebraic(question, raw_text):
    try:
        with _grading_timeout():
            canonical = _parse_algebraic(question.canonical_answer)
    except (_InvalidFormat, _LimitsExceeded, ArithmeticError, TypeError, ValueError):
        return _result(reason="invalid_canonical")
    except _GradingTimeout:
        return _result(reason="grading_timeout")

    try:
        with _grading_timeout():
            student = _parse_algebraic(raw_text)
            if not student.variables.issubset(canonical.variables):
                return _result(
                    normalized=student.normalized,
                    reason="invalid_format",
                )
            difference = sympy.cancel(
                sympy.together(student.expression - canonical.expression)
            )
            if sympy.count_ops(difference) > MAX_RESULT_OPS:
                return _result(
                    normalized=student.normalized,
                    reason="limits_exceeded",
                )
            correct = difference == 0 or difference.is_zero is True
    except _GradingTimeout:
        return _result(reason="grading_timeout")
    except _LimitsExceeded:
        return _result(reason="limits_exceeded")
    except _InvalidFormat:
        return _result(reason="invalid_format")
    except (ArithmeticError, TypeError, ValueError):
        return _result(reason="invalid_format")
    return _result(
        correct=correct,
        normalized=student.normalized,
        reason="correct" if correct else "incorrect",
    )


def grade_answer(question, raw_text):
    """Grade an untrusted direct answer using the question's stored type."""
    if raw_text is None or not str(raw_text).strip():
        return _result(reason="empty")
    if question.question_type == "numerica":
        return _grade_numeric(question, raw_text)
    if question.question_type == "algebraica":
        if question.answer_tolerance not in (None, 0, 0.0):
            return _result(reason="invalid_canonical")
        return _grade_algebraic(question, raw_text)
    return _result(reason="unsupported_type")


def validate_direct_answer_config(question):
    """Return None when a direct-answer question is publishable, else a reason."""
    if question.question_type not in {"numerica", "algebraica"}:
        return "unsupported_type"
    result = grade_answer(question, question.canonical_answer)
    return None if result["correct"] else result["reason"]

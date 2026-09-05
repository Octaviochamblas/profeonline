"""Shared check: does a checkpoint explanation actually reference its answer?

The old test (`correct_text in explanation`) was a literal substring match and
too strict for math content:

* choice ``$1,25$`` vs explanation ending ``... = 1,25$.``
* choice ``Dividir el valor final por $1,15$`` vs explanation ``$V_i = V_f/1,15$``
* choice ``(0, 7)`` (a coordinate pair, not a gloss)

Strategy: if the choice carries math spans (``$...$``), every span must appear in
the explanation once both sides are stripped of KaTeX noise. Otherwise fall back
to comparing the whole normalised strings.
"""

from __future__ import annotations

import re

_MATH_SPAN = re.compile(r"\$(.+?)\$")
_TRAILING_PAREN = re.compile(r"\s*\([^()]*\)\s*$")
_LATEX_NOISE = re.compile(r"[\s${}\\]+")


def _normalize(value: str) -> str:
    value = (value or "").strip()
    # Drop a trailing "(gloss)" on the choice — unless the parenthetical IS the
    # whole answer (e.g. a coordinate pair like "(0, 7)").
    without_gloss = _TRAILING_PAREN.sub("", value)
    if without_gloss:
        value = without_gloss
    return _LATEX_NOISE.sub("", value).casefold()


def explanation_mentions_answer(correct_text: str, explanation: str) -> bool:
    exp = _LATEX_NOISE.sub("", (explanation or "")).casefold()
    # ``\$`` is an escaped literal dollar (e.g. a peso amount inside a KaTeX
    # span); drop it before pairing ``$...$`` delimiters.
    choice = (correct_text or "").replace("\\$", "")
    spans = [s for s in (_normalize(m) for m in _MATH_SPAN.findall(choice)) if s]
    if spans:
        return all(span in exp for span in spans)
    core = _normalize(correct_text)
    return bool(core) and core in exp

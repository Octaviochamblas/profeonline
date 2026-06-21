"""Construye un paquete revisable de preguntas v2 sin tocar la base de datos.

Produce un índice y un Markdown por recurso con 90 preguntas, alternativas,
respuesta correcta y explicación. Reutiliza los generadores matemáticos
deterministas del banco v1, pero elimina las preguntas conceptuales genéricas.
"""

from __future__ import annotations

import copy
import hashlib
import html
import json
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "scratch" / "review_lenguaje_algebraico_v2"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

import django

django.setup()

from apps.content.models import Resource
from scratch import populate_lenguaje_algebraico_questions as v1


MODE_LABELS = {
    "preparacion": "Preparación",
    "evaluacion": "Evaluación",
    "ambas": "Ambas",
}

GENERIC_LEADS = (
    "selecciona la afirmación correcta",
    "analiza el método explicado",
    "evalúa cuidadosamente el procedimiento",
)

FORBIDDEN_CHOICES = {
    "No se puede concluir sin alterar la expresión.",
    "La operación no está definida para ningún valor.",
    "La expresión permanece exactamente igual.",
    "Se obtiene el opuesto del resultado correcto.",
}

RULE_DISTRACTORS = {
    "terms": [
        "Dos términos son semejantes si tienen el mismo coeficiente.",
        "El grado de un término siempre coincide con su coeficiente.",
        "Las letras pueden cambiar mientras se conserve el signo.",
    ],
    "like": [
        "Se suman todas las variables y se conservan los números.",
        "Se multiplican los coeficientes de términos semejantes.",
        "Se pueden combinar términos con exponentes diferentes.",
    ],
    "paren": [
        "Todo paréntesis cambia automáticamente los signos.",
        "El signo exterior afecta solamente al primer término.",
        "Los paréntesis se eliminan sin revisar el signo anterior.",
    ],
    "mono_mono": [
        "Se suman los coeficientes y se multiplican los exponentes.",
        "Los exponentes se conservan siempre sin cambios.",
        "Se suman exponentes aunque las bases sean diferentes.",
    ],
    "mono_poly": [
        "El monomio multiplica únicamente al primer término.",
        "Se suman los coeficientes antes de distribuir.",
        "La propiedad distributiva cambia todos los signos a positivo.",
    ],
    "poly_poly": [
        "Solo se multiplican los términos de la misma posición.",
        "Los productos cruzados pueden omitirse.",
        "Primero se suman ambos polinomios y luego se eleva al cuadrado.",
    ],
    "square": [
        "El cuadrado de un binomio es solo la suma de los cuadrados.",
        "El término central es el producto simple de ambos términos.",
        "El signo del término central siempre es positivo.",
    ],
    "conjugates": [
        "El resultado conserva el término cruzado.",
        "Se obtiene una suma de cuadrados.",
        "Se eleva al cuadrado solo el primer término.",
    ],
    "common_binomials": [
        "El coeficiente lineal es el producto de los términos no comunes.",
        "El término independiente es la suma de los términos no comunes.",
        "El término común desaparece del resultado.",
    ],
    "factor_mono": [
        "Se extrae el mayor exponente aunque no esté en todos los términos.",
        "Se extraen factores presentes solo en el primer término.",
        "Factorizar significa dividir cada término por valores distintos.",
    ],
    "factor_binomial": [
        "Se extrae solo una letra del binomio repetido.",
        "El bloque común puede cambiar de signo en cada término.",
        "No es posible extraer expresiones de más de un término.",
    ],
    "grouping": [
        "Los grupos pueden formarse sin obtener un factor común igual.",
        "Solo se factoriza el primer par de términos.",
        "Después de agrupar no es necesario volver a factorizar.",
    ],
    "fraction_simple": [
        "Se cancelan términos separados por suma o resta.",
        "Las restricciones desaparecen después de simplificar.",
        "Numerador y denominador se reducen restando sus términos.",
    ],
    "fraction_complex": [
        "Se cancelan expresiones antes de factorizar.",
        "Los valores excluidos se recuperan después de simplificar.",
        "Solo es necesario factorizar el denominador.",
    ],
    "fraction_division": [
        "Se invierte la primera fracción.",
        "Se dividen numeradores y se suman denominadores.",
        "La segunda fracción se conserva sin calcular su recíproco.",
    ],
    "lcm": [
        "Se eligen únicamente los factores comunes con menor exponente.",
        "Se multiplican todos los coeficientes aunque compartan factores.",
        "Se descartan las letras que no aparecen en todas las expresiones.",
    ],
    "gcd": [
        "Se incluyen factores presentes solo en una expresión.",
        "Se eligen los exponentes mayores.",
        "Se usa el mínimo común múltiplo de los coeficientes.",
    ],
}

RULE_STATEMENTS = {
    "terms": (
        "El coeficiente es el factor numérico; la parte literal contiene las "
        "variables y el grado depende de sus exponentes."
    ),
    "like": (
        "Solo pueden reducirse términos con la misma parte literal; se operan "
        "sus coeficientes y se conserva esa parte literal."
    ),
    "paren": (
        "Un signo menos delante del paréntesis cambia cada signo interior; "
        "un signo más los conserva."
    ),
    "mono_mono": (
        "Se multiplican los coeficientes y se suman exponentes únicamente "
        "cuando las potencias tienen la misma base."
    ),
    "mono_poly": (
        "La propiedad distributiva obliga a multiplicar el monomio por cada "
        "término del polinomio."
    ),
    "poly_poly": (
        "Cada término del primer polinomio multiplica a cada término del "
        "segundo y luego se reducen términos semejantes."
    ),
    "square": (
        "El cuadrado de un binomio es el cuadrado del primero, más o menos "
        "el doble producto, más el cuadrado del segundo."
    ),
    "conjugates": (
        "El producto de binomios conjugados es una diferencia de cuadrados "
        "porque sus términos cruzados se anulan."
    ),
    "common_binomials": (
        "En (x+a)(x+b), el coeficiente lineal es a+b y el término "
        "independiente es ab."
    ),
    "factor_mono": (
        "El máximo factor común usa el MCD de los coeficientes y la menor "
        "potencia presente en todos los términos."
    ),
    "factor_binomial": (
        "Una expresión binomial completa puede extraerse cuando aparece como "
        "factor en todos los términos."
    ),
    "grouping": (
        "Los términos se agrupan de manera que cada grupo produzca el mismo "
        "factor compuesto, que luego se extrae."
    ),
    "fraction_simple": (
        "En una fracción algebraica se cancelan factores completos después "
        "de factorizar, nunca términos separados por suma o resta."
    ),
    "fraction_complex": (
        "Numerador y denominador deben factorizarse completamente antes de "
        "cancelar factores, conservando las restricciones originales."
    ),
    "fraction_division": (
        "Dividir por una fracción algebraica equivale a multiplicar por su "
        "recíproco y después factorizar y simplificar."
    ),
    "lcm": (
        "El MCM algebraico usa el MCM de los coeficientes y la mayor potencia "
        "necesaria de cada factor."
    ),
    "gcd": (
        "El MCD algebraico conserva solo factores comunes, usando el MCD de "
        "coeficientes y los menores exponentes compartidos."
    ),
}

FINAL_CHECKS = {
    "fraction_simple": (
        "Confirmar la equivalencia y mantener los valores excluidos por el "
        "denominador original."
    ),
    "fraction_complex": (
        "Confirmar la equivalencia y mantener los valores excluidos por los "
        "denominadores originales."
    ),
    "fraction_division": (
        "Confirmar la equivalencia y revisar restricciones, incluido que la "
        "fracción divisora no sea cero."
    ),
    "lcm": "Verificar que cada expresión original divida al múltiplo obtenido.",
    "gcd": "Verificar que el resultado divida a todas las expresiones originales.",
}


def answer_data(item):
    correct = next(
        choice["text"] for choice in item["choices"] if choice["is_correct"]
    )
    wrong = [
        choice["text"] for choice in item["choices"] if not choice["is_correct"]
    ]
    return correct, wrong


def sanitize_choices(item):
    """Elimina distractores de relleno y exige cuatro opciones plausibles."""
    item = copy.deepcopy(item)
    correct = next(
        choice["text"] for choice in item["choices"] if choice["is_correct"]
    )

    def wrong_variants(value):
        text = str(value)
        candidates = []
        if re.fullmatch(r"-?\d+", text):
            number = int(text)
            candidates.extend((str(number + 1), str(number - 1), str(-number)))
        if " + " in text:
            candidates.append(text.replace(" + ", " - ", 1))
        if " - " in text:
            candidates.append(text.replace(" - ", " + ", 1))
        exponent_match = re.search(r"\^(\d+)", text)
        if exponent_match:
            exponent = int(exponent_match.group(1))
            candidates.append(
                text[: exponent_match.start(1)]
                + str(exponent + 1)
                + text[exponent_match.end(1):]
            )
        if "²" in text:
            candidates.append(text.replace("²", "", 1))
        candidates.extend((f"-({text})", f"{text} + 1", f"{text} - 1"))
        return list(dict.fromkeys(candidates))

    replacements = wrong_variants(correct)
    used = {
        choice["text"]
        for choice in item["choices"]
        if choice["text"] not in FORBIDDEN_CHOICES
    }
    fallback_index = 0
    for choice in item["choices"]:
        if choice["text"] not in FORBIDDEN_CHOICES:
            continue
        if choice["is_correct"]:
            raise ValueError("Una respuesta correcta no puede ser un texto de relleno.")
        while replacements[fallback_index] in used:
            fallback_index += 1
        choice["text"] = replacements[fallback_index]
        used.add(choice["text"])
    return item


def clone_question(text, correct, distractors, explanation, cognitive_type):
    return sanitize_choices(
        v1.question(
            text=text,
            correct=correct,
            distractors=distractors,
            explanation=explanation,
            cognitive_type=cognitive_type,
        )
    )


def vary_symbol(item, index):
    """Cambia la variable principal sin alterar la estructura matemática."""
    symbol = ("x", "y", "a", "m", "p", "t", "z", "u", "v", "n")[index % 10]
    if symbol == "x":
        return item
    item = copy.deepcopy(item)

    def replace(value):
        return re.sub(r"(?<![A-Za-z])x(?![A-Za-z])", symbol, str(value))

    item["text"] = replace(item["text"])
    item["explanation"] = replace(item["explanation"])
    for choice in item["choices"]:
        choice["text"] = replace(choice["text"])
    return item


def concrete_base(kind, index):
    """Genera el ejercicio matemático base evitando distractores de relleno."""
    if kind != "terms":
        return sanitize_choices(v1.calculation(kind, index))
    variable = ("x", "y", "a", "m", "p", "t", "z", "u", "v", "n")[index % 10]
    coefficient = index + 2
    if index % 2 == 0:
        coefficient *= -1
    exponent = 1 + index % 4
    family = index % 3
    if family == 0:
        distractors = [
            abs(coefficient),
            exponent,
            -exponent if -exponent != coefficient else exponent + 1,
        ]
        return clone_question(
            f"En el término {v1.term(coefficient, variable, exponent)}, "
            "¿cuál es el coeficiente?",
            coefficient,
            distractors,
            "El coeficiente es el factor numérico que multiplica la parte literal.",
            "aplicacion",
        )
    if family == 1:
        return clone_question(
            f"¿Cuál es el grado del término {v1.term(coefficient, variable, exponent)}?",
            exponent,
            [abs(coefficient), exponent + 1, abs(coefficient) + exponent],
            "En un monomio de una variable, el grado corresponde a su exponente.",
            "aplicacion",
        )
    other = coefficient + 3
    return clone_question(
        f"¿Cuál término es semejante a {v1.term(coefficient, variable, exponent)}?",
        v1.term(other, variable, exponent),
        [
            v1.term(other, variable, exponent + 1),
            v1.term(other, "w", exponent),
            v1.term(other, variable, exponent + 2),
        ],
        "Los términos semejantes tienen exactamente las mismas variables "
        "elevadas a los mismos exponentes.",
        "analisis",
    )


def concrete_level_one(spec, index):
    kind, action, _rule, first_step, common_error = spec
    rule = RULE_STATEMENTS[kind]
    rule_sentence = rule.rstrip(".")
    base = vary_symbol(concrete_base(kind, index), index)
    correct, wrong = answer_data(base)
    family = index % 6
    variant = index // 6
    expression = base["text"]

    if family == 0:
        base["text"] = (
            f"Observa el caso concreto y responde sin omitir su estructura: {expression}"
        )
        base["cognitive_type"] = "comprension"
        return base

    if family == 1:
        return clone_question(
            f"En el ejercicio «{expression}», ¿qué regla justifica principalmente el procedimiento?",
            rule,
            RULE_DISTRACTORS[kind],
            f"Este caso se resuelve porque {rule_sentence.lower()}.",
            "comprension",
        )

    if family == 2:
        return clone_question(
            f"Para comenzar correctamente «{expression}», ¿qué acción debe realizarse primero?",
            first_step,
            [
                common_error,
                "Sustituir todas las variables por cero.",
                "Escoger la alternativa con más términos.",
            ],
            f"El primer paso pertinente es {first_step}.",
            "aplicacion",
        )

    if family == 3:
        return clone_question(
            f"Un estudiante obtiene {wrong[0]} al resolver «{expression}». "
            "¿Cuál observación permite detectar el error?",
            f"Es incorrecto; al aplicar la regla correspondiente se obtiene {correct}.",
            [
                "El resultado es válido porque contiene las mismas variables.",
                "Solo falta cambiar el orden de los términos.",
                "Cualquier expresión de igual grado es equivalente.",
            ],
            f"La comprobación correcta conduce a {correct}. {base['explanation']}",
            "analisis",
        )

    if family == 4:
        claim = correct if variant % 2 == 0 else wrong[0]
        correct_evaluation = (
            f"Es correcta: el resultado es {correct}."
            if claim == correct
            else f"Es incorrecta: el resultado correcto es {correct}."
        )
        return clone_question(
            f"Se afirma que «{expression}» conduce a {claim}. ¿Cómo debe evaluarse?",
            correct_evaluation,
            [
                "Es correcta porque conserva al menos una variable.",
                "No puede evaluarse sin asignar un valor numérico a todas las letras.",
                "Es correcta si se ignoran signos y exponentes.",
            ],
            base["explanation"],
            "analisis",
        )

    return clone_question(
        f"¿Qué revisión permite confirmar el resultado {correct} en «{expression}»?",
        first_step.capitalize() + ".",
        [
            "Revisar únicamente que la respuesta sea más corta.",
            "Comprobar que todos los coeficientes sean positivos.",
            "Cambiar las variables por otras letras y aceptar el resultado.",
        ],
        f"La equivalencia se confirma al reproducir el procedimiento. {base['explanation']}",
        "analisis",
    )


def concrete_level_two(spec, index):
    kind = spec[0]
    base = vary_symbol(concrete_base(kind, index + 40), index)
    correct, wrong = answer_data(base)
    family = index % 6
    variant = index // 6
    expression = base["text"]

    if family == 0:
        base["text"] = f"Resuelve paso a paso: {expression}"
        return base

    if family == 1:
        return clone_question(
            f"En «{expression}», ¿cuál de estas transformaciones conserva la equivalencia?",
            correct,
            wrong,
            base["explanation"],
            "aplicacion",
        )

    if family == 2:
        return clone_question(
            f"Dos estudiantes resuelven «{expression}». Elena obtiene {correct} y Diego obtiene "
            f"{wrong[0]}. ¿Quién aplicó correctamente las reglas?",
            "Elena",
            ["Diego", "Ambos", "Ninguno"],
            base["explanation"],
            "analisis",
        )

    if family == 3:
        return clone_question(
            f"Una pauta entrega {wrong[0]} como respuesta de «{expression}». "
            "¿Qué corrección debe incorporarse?",
            f"Reemplazarla por {correct}.",
            [
                "Mantenerla y cambiar solo el orden de los términos.",
                "Eliminar las variables para obtener un número.",
                "Cambiar únicamente el signo de la expresión.",
            ],
            base["explanation"],
            "analisis",
        )

    if family == 4:
        return clone_question(
            f"Al resolver «{expression}», ¿qué error produciría específicamente la respuesta {wrong[0]}?",
            spec[4],
            [
                "Comprobar el resultado mediante una operación inversa.",
                "Conservar las restricciones de la expresión original.",
                "Reducir términos solo cuando son realmente semejantes.",
            ],
            f"La respuesta correcta es {correct}. {base['explanation']}",
            "analisis",
        )

    return clone_question(
        f"En «{expression}», ¿qué resultado debe obtenerse antes de dar el ejercicio por terminado?",
        correct,
        wrong,
        base["explanation"],
        "aplicacion",
    )


def concrete_level_three(spec, index):
    kind = spec[0]
    base = vary_symbol(concrete_base(kind, index + 80), index)
    correct, wrong = answer_data(base)
    family = index % 6
    context = (
        "una pauta de corrección",
        "un programa de álgebra",
        "una tutoría",
        "una evaluación",
        "una revisión entre pares",
    )[index // 6]
    expression = base["text"]

    if family == 0:
        return clone_question(
            f"En {context} se debe resolver «{expression}». ¿Qué respuesta debe aceptarse?",
            correct,
            wrong,
            base["explanation"],
            "aplicacion",
        )

    if family == 1:
        return clone_question(
            f"En {context}, una solución propone {wrong[0]} para «{expression}». "
            "¿Cuál es el diagnóstico correcto?",
            f"La solución es incorrecta; debe obtenerse {correct}.",
            [
                "La solución es correcta porque mantiene el grado.",
                "La solución es correcta si se omite el último paso.",
                "No es posible decidir usando reglas algebraicas.",
            ],
            base["explanation"],
            "analisis",
        )

    if family == 2:
        return clone_question(
            f"Para validar automáticamente «{expression}», ¿qué salida debe producir el sistema?",
            correct,
            wrong,
            base["explanation"],
            "aplicacion",
        )

    if family == 3:
        return clone_question(
            f"Una respuesta a «{expression}» entrega {correct}. "
            "¿Qué argumento demuestra que la conclusión es válida?",
            base["explanation"],
            [
                "La respuesta tiene menos símbolos que el enunciado.",
                "La expresión final contiene al menos una variable.",
                "Los coeficientes pueden elegirse sin efectuar el procedimiento.",
            ],
            base["explanation"],
            "analisis",
        )

    if family == 4:
        return clone_question(
            f"En {context}, ¿cuál de estas respuestas revela el error «{spec[4]}» "
            f"al trabajar con «{expression}»?",
            wrong[0],
            [correct, wrong[1], wrong[2]],
            f"{wrong[0]} representa el error indicado; la respuesta válida es {correct}.",
            "analisis",
        )

    return clone_question(
        f"Después de obtener {correct} en «{expression}», ¿qué revisión final es pertinente?",
        FINAL_CHECKS.get(
            kind,
            "Desarrollar la forma obtenida o sustituir un valor para confirmar "
            "que es equivalente a la expresión original.",
        ),
        [
            "Aceptar el resultado solo porque tiene menos términos.",
            "Cambiar los signos para obtener una expresión positiva.",
            "Sustituir las letras por nombres distintos sin volver a comprobar.",
        ],
        base["explanation"],
        "analisis",
    )


def build_resource_questions(slug):
    spec = v1.SPECS[slug]
    random.seed(f"profeonline:lenguaje-algebraico:v2:{slug}:2026-06-21")
    result = []
    for level, builder in (
        (1, concrete_level_one),
        (2, concrete_level_two),
        (3, concrete_level_three),
    ):
        for index in range(30):
            item = builder(spec, index)
            item["level"] = level
            item["mode"] = v1.MODES[index // 10]
            result.append(item)
    return result


def reference_questions(resource):
    """Recupera preguntas editoriales manuales para usarlas como patrón/contenido."""
    references = []
    queryset = resource.questions.filter(status="publicada").prefetch_related(
        "choices"
    ).order_by("id")
    for question_object in queryset:
        if (question_object.audit_data or {}).get("generator"):
            continue
        choices = list(question_object.choices.all())
        if len(choices) != 4 or sum(choice.is_correct for choice in choices) != 1:
            continue
        text = question_object.text.replace(
            "mínimo común denominador (MCD)",
            "mínimo común denominador",
        )
        explanation = question_object.explanation.replace(
            "mínimo común denominador (MCD)",
            "mínimo común denominador",
        )
        references.append(
            {
                "text": text,
                "explanation": explanation,
                "cognitive_type": "comprension",
                "level": question_object.level,
                "mode": question_object.mode,
                "choices": [
                    {
                        "text": choice.text,
                        "is_correct": choice.is_correct,
                    }
                    for choice in choices
                ],
                "_reference_id": question_object.id,
            }
        )
    return references


def merge_references(questions, references):
    """Sustituye propuestas del mismo nivel/modo sin alterar la matriz 90/90."""
    merged = list(questions)
    for reference in references:
        replace_index = next(
            index
            for index, item in enumerate(merged)
            if item["level"] == reference["level"]
            and item["mode"] == reference["mode"]
            and not item.get("_reference_id")
        )
        merged[replace_index] = reference
    return merged


def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def audit(slug, questions):
    v1.audit_bank(slug, questions)
    texts = [normalize(item["text"]) for item in questions]
    for lead in GENERIC_LEADS:
        if any(lead in text for text in texts):
            raise ValueError(f"{slug}: conserva el inicio genérico «{lead}»")
    forbidden = [
        choice["text"]
        for item in questions
        for choice in item["choices"]
        if choice["text"] in FORBIDDEN_CHOICES
    ]
    if forbidden:
        raise ValueError(f"{slug}: conserva {len(forbidden)} distractores de relleno")
    exact_leads = Counter(text.split(":", 1)[0] for text in texts)
    if exact_leads and max(exact_leads.values()) > 10:
        raise ValueError(f"{slug}: demasiadas preguntas con el mismo inicio")
    concrete = sum(
        bool(re.search(r"[0-9]|[xyzabmp]\^|[()+*/²≠]", item["text"].lower()))
        for item in questions
    )
    if concrete < 60:
        raise ValueError(f"{slug}: solo {concrete}/90 preguntas concretas")
    return {
        "concrete": concrete,
        "unique": len(set(texts)),
        "generic_leads": 0,
    }


def render_question(number, item):
    correct = next(
        choice["text"] for choice in item["choices"] if choice["is_correct"]
    )
    letters = "ABCD"
    lines = [
        f"### {number}. {item['text']}",
        "",
    ]
    for letter, choice in zip(letters, item["choices"]):
        lines.append(f"- {letter}. {choice['text']}")
    lines.extend(
        [
            "",
            f"**Respuesta:** {correct}",
            "",
            f"**Explicación:** {item['explanation']}",
            "",
        ]
    )
    return lines


def render_resource(resource, questions, audit_result):
    transcript_hash = hashlib.sha256(
        resource.transcript.encode("utf-8")
    ).hexdigest()
    lines = [
        f"# {resource.title}",
        "",
        f"- Recurso: `{resource.slug}`",
        f"- Transcripción: {len(resource.transcript.split())} palabras",
        f"- SHA-256: `{transcript_hash}`",
        "- Estado: propuesta v2 para revisión; no publicada",
        f"- Preguntas concretas detectadas: {audit_result['concrete']}/90",
        f"- Preguntas editoriales conservadas como referencia: {audit_result['references']}",
        "",
    ]
    number = 0
    for level in (1, 2, 3):
        lines.extend([f"## Nivel {level}", ""])
        for mode in v1.MODES:
            lines.extend([f"### Banco {MODE_LABELS[mode]}", ""])
            for item in questions:
                if item["level"] == level and item["mode"] == mode:
                    number += 1
                    lines.extend(render_question(number, item))
    return "\n".join(lines).rstrip() + "\n"


def render_html(resources_payload):
    navigation = []
    sections = []
    for item in resources_payload:
        resource = item["resource"]
        questions = item["questions"]
        navigation.append(
            f'<a href="#r-{resource.id}">{html.escape(resource.title)}</a>'
        )
        groups = []
        for level in (1, 2, 3):
            modes = []
            for mode in v1.MODES:
                cards = []
                selected = [
                    question
                    for question in questions
                    if question["level"] == level and question["mode"] == mode
                ]
                for number, question in enumerate(selected, 1):
                    choices = "".join(
                        (
                            '<li class="correct">'
                            if choice["is_correct"]
                            else "<li>"
                        )
                        + html.escape(choice["text"])
                        + "</li>"
                        for choice in question["choices"]
                    )
                    cards.append(
                        "<article class=\"question\">"
                        f"<h5>{number}. {html.escape(question['text'])}</h5>"
                        f"<ol type=\"A\">{choices}</ol>"
                        f"<p><strong>Respuesta:</strong> "
                        f"{html.escape(next(choice['text'] for choice in question['choices'] if choice['is_correct']))}</p>"
                        f"<p><strong>Explicación:</strong> "
                        f"{html.escape(question['explanation'])}</p>"
                        "</article>"
                    )
                modes.append(
                    "<details>"
                    f"<summary>{MODE_LABELS[mode]} ({len(selected)})</summary>"
                    + "".join(cards)
                    + "</details>"
                )
            groups.append(
                f"<section class=\"level\"><h3>Nivel {level}</h3>"
                + "".join(modes)
                + "</section>"
            )
        sections.append(
            f'<details class="resource" id="r-{resource.id}">'
            f"<summary>{html.escape(resource.title)}</summary>"
            f"<p class=\"meta\">90 preguntas · propuesta v2 no publicada</p>"
            + "".join(groups)
            + "</details>"
        )
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Revisión v2 — Lenguaje Algebraico</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:1200px;margin:auto;padding:24px;color:#17202a;background:#f5f7f8}}
h1{{color:#0f766e}} nav{{display:grid;gap:6px;margin:20px 0;padding:16px;background:white;border-radius:12px}}
nav a{{color:#0f766e;text-decoration:none}} details{{margin:10px 0}} summary{{cursor:pointer;font-weight:700}}
.resource{{background:white;border:1px solid #dbe5e3;border-radius:12px;padding:14px}}
.resource>summary{{font-size:1.05rem}} .meta{{color:#64748b}} .level{{margin-left:12px}}
.level>details{{border-left:3px solid #14b8a6;padding-left:12px}}
.question{{margin:14px 0;padding:14px;background:#f8fafc;border-radius:9px}}
.question h5{{font-size:.95rem;margin:0 0 10px}} .question p{{margin:8px 0}}
.correct{{color:#166534;font-weight:700}} ol{{padding-left:28px}}
</style>
</head>
<body>
<h1>Revisión de preguntas v2 — Lenguaje Algebraico</h1>
<p>17 recursos · 1.530 preguntas · esta propuesta todavía no está publicada.</p>
<nav>{"".join(navigation)}</nav>
{"".join(sections)}
</body>
</html>
"""


def main():
    resources = {
        resource.slug: resource
        for resource in Resource.objects.filter(
            topic__slug=v1.TOPIC_SLUG
        ).order_by("order", "id")
    }
    if set(resources) != set(v1.SPECS):
        raise RuntimeError("El inventario de recursos no coincide con el generador.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    index_lines = [
        "# Revisión de preguntas v2 — Lenguaje Algebraico",
        "",
        "Este paquete no modifica producción. Contiene 90 preguntas propuestas por recurso.",
        "",
        "| Recurso | Preguntas concretas | Documento |",
        "| --- | ---: | --- |",
    ]
    package = {
        "schema": "profeonline.question-review/v2",
        "topic": v1.TOPIC_SLUG,
        "status": "review_pending",
        "resources": {},
    }
    html_payload = []
    total = 0
    for slug, resource in resources.items():
        references = reference_questions(resource)
        questions = merge_references(
            build_resource_questions(slug),
            references,
        )
        result = audit(slug, questions)
        result["references"] = len(references)
        filename = f"{resource.order:05d}-{slug}.md"
        (OUTPUT_DIR / filename).write_text(
            render_resource(resource, questions, result),
            encoding="utf-8",
        )
        package["resources"][slug] = {
            "resource_id": resource.id,
            "title": resource.title,
            "transcript_sha256": hashlib.sha256(
                resource.transcript.encode("utf-8")
            ).hexdigest(),
            "questions": questions,
            "audit": result,
        }
        html_payload.append(
            {
                "resource": resource,
                "questions": questions,
            }
        )
        index_lines.append(
            f"| {resource.title} | {result['concrete']}/90 | [{filename}]({filename}) |"
        )
        total += len(questions)
        print(f"[OK] {slug}: {len(questions)} preguntas")

    package["question_count"] = total
    (OUTPUT_DIR / "INDEX.md").write_text(
        "\n".join(index_lines) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "package.json").write_text(
        json.dumps(package, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "REVIEW.html").write_text(
        render_html(html_payload),
        encoding="utf-8",
    )
    print(f"REVIEW_PACKAGE_OK resources={len(resources)} questions={total}")
    print(f"INDEX={OUTPUT_DIR / 'INDEX.md'}")


if __name__ == "__main__":
    main()

"""Genera y publica el banco estándar del tema Lenguaje Algebraico.

Dry-run por defecto. Para escribir exige ``--apply`` y una frase de confirmación.
No usa APIs externas, no reemplaza preguntas existentes y deja respaldo previo.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import django


BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.conf import settings
from django.db import transaction
from django.db.models import Count

from apps.content.models import Choice, Question, Resource, ResourceQuizConfig


TOPIC_SLUG = "lenguaje-algebraico"
CONFIRMATION = "POBLAR_LENGUAJE_ALGEBRAICO_1530"
MODES = ("preparacion", "evaluacion", "ambas")
COUNTS = {
    str(level): {
        "practice": {"pool": 20, "shown": 5},
        "eval": {"pool": 20, "shown": 5 if level < 3 else 3},
    }
    for level in (1, 2, 3)
}


SPECS = {
    "lenguaje-algebraico-101-termino-algebraico-y-terminos-semejantes-reduccion-paso-a-paso": (
        "terms",
        "reconocer las partes de un término y decidir cuándo dos términos son semejantes",
        "coeficiente, parte literal y grado",
        "comparar variables y exponentes antes de operar coeficientes",
        "sumar términos con partes literales distintas",
    ),
    "lenguaje-algebraico-102-ejercicios-agrupacion-de-terminos-semejantes": (
        "like",
        "agrupar y reducir términos semejantes, incluso con coeficientes fraccionarios",
        "suma de coeficientes de una misma parte literal",
        "identificar primero el mínimo común denominador cuando corresponde",
        "sumar numeradores sin igualar denominadores",
    ),
    "lenguaje-algebraico-103-ejercicios-reduccion-de-expresiones-algebraicas-con-parentesis": (
        "paren",
        "eliminar paréntesis respetando el signo exterior y reducir",
        "cambio de signos ante un signo menos",
        "distribuir el signo exterior antes de agrupar términos",
        "quitar un paréntesis negativo sin cambiar sus signos",
    ),
    "lenguaje-algebraica-104-ejercicios-multiplicacion-algebraica-monomios-por-monomios": (
        "mono_mono",
        "multiplicar monomios",
        "producto de coeficientes y suma de exponentes de igual base",
        "resolver signos y coeficientes antes de combinar potencias",
        "multiplicar exponentes de bases iguales",
    ),
    "lenguaje-algebraica-105-ejercicios-multiplicacion-algebraica-monomio-por-polinomio-paso-a-paso": (
        "mono_poly",
        "aplicar la propiedad distributiva de un monomio sobre un polinomio",
        "distribución término a término",
        "multiplicar el monomio por cada término del paréntesis",
        "multiplicar únicamente el primer término",
    ),
    "lenguaje-algebraico-106-ejercicios-multiplicacion-algebraica-de-polinomios-por-polinomios": (
        "poly_poly",
        "multiplicar polinomios y reducir términos semejantes",
        "distribución completa entre todos los términos",
        "obtener los productos parciales y luego reducir",
        "omitir los productos cruzados",
    ),
    "lenguaje-algebraico-201-cuadrado-de-binomio-formula-y-ejercicios-resueltos": (
        "square",
        "desarrollar el cuadrado de un binomio",
        "a² ± 2ab + b²",
        "identificar ambos términos y el signo del término central",
        "olvidar el doble producto",
    ),
    "lenguaje-algebraico-202-suma-por-su-diferencia-formula-y-ejercicios-resueltos-paso-a-paso": (
        "conjugates",
        "reconocer y desarrollar una suma por su diferencia",
        "(a+b)(a-b)=a²-b²",
        "verificar que los binomios sean conjugados",
        "conservar términos cruzados que se anulan",
    ),
    "lenguaje-algebraico-203-multiplicacion-de-binomios-con-termino-comun-formula-y-ejercicios": (
        "common_binomials",
        "multiplicar binomios con término común",
        "(x+a)(x+b)=x²+(a+b)x+ab",
        "sumar los términos no comunes y calcular su producto",
        "usar a+b como término independiente",
    ),
    "lenguaje-algebraico-301-factorizacion-por-factor-comun-monomio-paso-a-paso": (
        "factor_mono",
        "extraer el máximo factor común monomio",
        "MCD de coeficientes y menor exponente común",
        "buscar factores presentes en todos los términos",
        "extraer un exponente mayor que el disponible",
    ),
    "lenguaje-algebraico-302-factorizacion-por-binomio-factor-comun-binomio-por-pasos": (
        "factor_binomial",
        "extraer un binomio común",
        "A·B+C·B=B(A+C)",
        "identificar el bloque binomial repetido",
        "factorizar solo una parte del binomio común",
    ),
    "lenguaje-algebraico303-factorizacion-por-agrupacion-facil-y-explicado": (
        "grouping",
        "factorizar por agrupación",
        "crear un factor binomial común en dos grupos",
        "agrupar términos de modo que aparezca el mismo factor",
        "agrupar sin comprobar el factor común resultante",
    ),
    "lenguaje-algebraico-401-fracciones-algebraicas-factorizar-y-simplificar": (
        "fraction_simple",
        "factorizar y simplificar fracciones algebraicas",
        "cancelación de factores, no de términos sumados",
        "factorizar numerador y denominador antes de cancelar",
        "cancelar términos dentro de una suma",
    ),
    "lenguaje-algebraico-401a-ejercicios-de-fracciones-algebraicas": (
        "fraction_complex",
        "resolver simplificaciones de fracciones algebraicas compuestas",
        "factorización completa y restricciones del denominador",
        "buscar factores comunes después de factorizar",
        "ignorar los valores que anulan el denominador original",
    ),
    "lenguaje-algebraico-402-division-de-fracciones-algebraicas": (
        "fraction_division",
        "dividir fracciones algebraicas",
        "multiplicación por el recíproco de la segunda fracción",
        "factorizar y transformar la división en producto",
        "invertir la primera fracción",
    ),
    "lenguaje-algebraico-403-minimo-comun-multiplo-algebraico": (
        "lcm",
        "calcular el mínimo común múltiplo algebraico",
        "MCM de coeficientes y mayor exponente de cada factor",
        "descomponer y elegir todos los factores necesarios",
        "elegir los exponentes menores",
    ),
    "lenguaje-algebraico-404-maximo-comun-divisor-algebraico": (
        "gcd",
        "calcular el máximo común divisor algebraico",
        "MCD de coeficientes y menor exponente común",
        "conservar solo factores presentes en todas las expresiones",
        "incluir factores que no aparecen en todos los monomios",
    ),
}


def gcd_many(*values):
    result = 0
    for value in values:
        result = math.gcd(result, abs(value))
    return result


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def signed(value):
    return f"+ {value}" if value >= 0 else f"- {abs(value)}"


def term(coefficient, variable="x", exponent=1):
    if coefficient == 0:
        return "0"
    sign = "-" if coefficient < 0 else ""
    absolute = abs(coefficient)
    coefficient_text = "" if absolute == 1 and variable else str(absolute)
    power = "" if exponent == 1 else f"^{exponent}"
    return f"{sign}{coefficient_text}{variable}{power}"


def polynomial(terms):
    parts = []
    for coefficient, variable, exponent in terms:
        if coefficient == 0:
            continue
        value = term(coefficient, variable, exponent)
        if not parts:
            parts.append(value)
        elif value.startswith("-"):
            parts.append(f"- {value[1:]}")
        else:
            parts.append(f"+ {value}")
    return " ".join(parts) or "0"


def question(text, correct, distractors, explanation, cognitive_type):
    choices = [str(correct), *map(str, distractors)]
    unique = []
    for choice in choices:
        if choice not in unique:
            unique.append(choice)
    fallbacks = (
        "No se puede concluir sin alterar la expresión.",
        "La operación no está definida para ningún valor.",
        "La expresión permanece exactamente igual.",
        "Se obtiene el opuesto del resultado correcto.",
    )
    for fallback in fallbacks:
        if len(unique) == 4:
            break
        if fallback not in unique:
            unique.append(fallback)
    unique = unique[:4]
    random.shuffle(unique)
    return {
        "text": text,
        "explanation": explanation,
        "cognitive_type": cognitive_type,
        "choices": [
            {"text": choice, "is_correct": choice == str(correct)}
            for choice in unique
        ],
    }


def conceptual_item(spec, index):
    _kind, action, rule, first_step, common_error = spec
    family = index % 10
    cycle = index // 10
    prompts = (
        (
            f"¿Qué regla fundamenta el procedimiento para {action}?",
            rule,
            [common_error, first_step, "Operar sin reconocer la estructura algebraica."],
            f"La regla central es {rule}.",
        ),
        (
            f"¿Cuál es el primer paso recomendable al {action}?",
            first_step,
            [common_error, rule, "Reemplazar las variables por cero."],
            f"Conviene comenzar por {first_step}.",
        ),
        (
            f"¿Cuál es un error frecuente al {action}?",
            common_error,
            [first_step, rule, "Comprobar el resultado mediante la operación inversa."],
            f"El error consiste en {common_error}.",
        ),
        (
            f"¿Qué objetivo tiene {action}?",
            "Obtener una expresión equivalente mediante reglas algebraicas válidas.",
            ["Cambiar el valor de la expresión.", "Eliminar todas las variables.", common_error],
            "El procedimiento transforma la forma, pero conserva la equivalencia.",
        ),
        (
            f"¿Cómo puede verificarse un resultado al {action}?",
            "Desarrollando, sustituyendo valores permitidos o aplicando la operación inversa.",
            ["Mirando solo el signo final.", common_error, "Eligiendo la forma más corta sin revisar."],
            "Una verificación independiente permite confirmar la equivalencia.",
        ),
        (
            f"¿Qué información debe conservarse durante el proceso de {action}?",
            "Signos, coeficientes, variables, exponentes y restricciones pertinentes.",
            ["Solo los coeficientes positivos.", "Únicamente las variables.", common_error],
            "Cada componente aporta información a la expresión.",
        ),
        (
            f"Una estudiante propone {common_error}. ¿Cómo se evalúa esa estrategia?",
            "Es incorrecta porque no respeta la estructura ni las reglas del procedimiento.",
            ["Es siempre correcta.", "Es correcta solo si hay variables.", first_step],
            f"La estrategia correcta requiere {first_step}.",
        ),
        (
            f"¿Qué distingue una transformación válida al {action}?",
            "Mantiene la equivalencia para todos los valores permitidos.",
            ["Solo funciona para x=1.", "Aumenta siempre el grado.", common_error],
            "Una identidad válida conserva el valor en todo el dominio permitido.",
        ),
        (
            f"¿Qué papel cumple la estructura «{rule}» al {action}?",
            "Resume la relación algebraica que guía los pasos.",
            ["Es una aproximación numérica.", "Elimina la necesidad de verificar.", common_error],
            "La estructura identifica qué operaciones están justificadas.",
        ),
        (
            f"Antes de terminar un ejercicio de {action}, ¿qué conviene revisar?",
            "Que no queden operaciones posibles y que las restricciones se mantengan.",
            ["Que todos los signos sean positivos.", "Que desaparezcan las variables.", common_error],
            "La revisión final detecta simplificaciones pendientes y errores de dominio.",
        ),
    )
    text, correct, distractors, explanation = prompts[family]
    leads = (
        "Selecciona la afirmación correcta.",
        "Analiza el método explicado en la clase.",
        "Evalúa cuidadosamente el procedimiento.",
    )
    return question(
        f"{leads[cycle]} {text}",
        correct,
        distractors,
        explanation,
        "comprension" if cycle == 0 else "analisis",
    )


def calculation(kind, index):
    a = 2 + index % 7 + index // 14
    b = 1 + (index * 2) % 9 + index // 18
    c = 2 + (index * 3) % 7 + index // 21
    p = 1 + index % 4
    q = 1 + (index * 2) % 4
    sign = -1 if index % 3 == 0 else 1

    if kind == "terms":
        variable = ("x", "y", "a", "m", "z")[(index // 3) % 5]
        cases = (
            question(
                f"En el término {term(sign*a, variable, p)}, ¿cuál es el coeficiente?",
                sign * a, [a, p, sign * p],
                "El coeficiente es el factor numérico que multiplica la parte literal.",
                "aplicacion",
            ),
            question(
                f"¿Cuál es el grado del término {term(a, variable, p)}?",
                p, [a, p + 1, a + p],
                "En un monomio de una variable, el grado es el exponente de la variable.",
                "aplicacion",
            ),
            question(
                f"¿Cuál término es semejante a {term(a, variable, p)}?",
                term(-b, variable, p),
                [term(b, variable, p + 1), term(b, "w", p), term(b, variable, max(1, p - 1))],
                "Los términos semejantes tienen exactamente la misma parte literal.",
                "analisis",
            ),
        )
        return cases[index % 3]

    if kind == "like":
        result = sign * a + b
        expression = f"{term(sign*a)} {signed(b)}x"
        return question(
            f"Reduce la expresión {expression}.",
            term(result), [term(sign*a*b), term(sign*a-b), f"{result}x²"],
            f"Se suman los coeficientes: {sign*a}+{b}={result}; la parte literal x se conserva.",
            "aplicacion",
        )

    if kind == "paren":
        outer = -1 if index % 2 else 1
        inner_b = sign * b
        result = a + outer * c
        constant = b + outer * inner_b
        operator = "+" if outer == 1 else "-"
        expression = f"{a}x + {b} {operator} ({c}x {signed(inner_b)})"
        answer = polynomial([(result, "x", 1), (constant, "", 1)])
        wrong1 = polynomial([(a + c, "x", 1), (b + inner_b, "", 1)])
        return question(
            f"Simplifica {expression}.",
            answer, [wrong1, f"{result}x", polynomial([(a-c, "x", 1), (b-inner_b, "", 1)])],
            "Se distribuye el signo exterior y luego se agrupan términos semejantes.",
            "aplicacion",
        )

    if kind == "mono_mono":
        coefficient = sign * a * b
        answer = term(coefficient, "x", p + q)
        return question(
            f"Calcula ({term(sign*a, 'x', p)})({term(b, 'x', q)}).",
            answer,
            [term(coefficient, "x", p*q), term(sign*(a+b), "x", p+q), term(abs(coefficient), "x", p+q)],
            "Se multiplican coeficientes y se suman exponentes de la misma base.",
            "aplicacion",
        )

    if kind == "mono_poly":
        first = sign * a * b
        second = sign * a * c
        answer = polynomial([(first, "x", p + 1), (second, "x", p)])
        return question(
            f"Desarrolla {term(sign*a, 'x', p)}({b}x + {c}).",
            answer,
            [polynomial([(first, "x", p+1), (c, "x", 1)]), term(first+second, "x", p+1), polynomial([(first, "x", p), (second, "x", p)])],
            "El monomio multiplica a cada término del binomio.",
            "aplicacion",
        )

    if kind == "poly_poly":
        middle = sign * a * c + b
        constant = b * c
        answer = polynomial([(sign*a, "x", 2), (middle, "x", 1), (constant, "", 1)])
        return question(
            f"Desarrolla ({term(sign*a)} + {b})(x + {c}).",
            answer,
            [polynomial([(sign*a, "x", 2), (b+c, "x", 1), (constant, "", 1)]), polynomial([(sign*a, "x", 2), (middle, "x", 1)]), polynomial([(sign*a, "x", 2), (sign*a*c-b, "x", 1), (constant, "", 1)])],
            "Se realizan los cuatro productos y se reducen los términos en x.",
            "aplicacion",
        )

    if kind == "square":
        middle = 2 * sign * a * b
        answer = polynomial([(a*a, "x", 2), (middle, "x", 1), (b*b, "", 1)])
        op = "+" if sign == 1 else "-"
        return question(
            f"Desarrolla ({a}x {op} {b})².",
            answer,
            [polynomial([(a*a, "x", 2), (sign*a*b, "x", 1), (b*b, "", 1)]), polynomial([(a*a, "x", 2), (b*b, "", 1)]), polynomial([(a*a, "x", 2), (-middle, "x", 1), (b*b, "", 1)])],
            "Se aplica primero², más o menos el doble producto, más segundo².",
            "aplicacion",
        )

    if kind == "conjugates":
        answer = polynomial([(a*a, "x", 2), (-b*b, "", 1)])
        return question(
            f"Calcula ({a}x + {b})({a}x - {b}).",
            answer,
            [polynomial([(a*a, "x", 2), (b*b, "", 1)]), polynomial([(a*a, "x", 2), (-2*a*b, "x", 1), (-b*b, "", 1)]), polynomial([(a, "x", 2), (-b, "", 1)])],
            "Los términos cruzados se anulan y queda una diferencia de cuadrados.",
            "aplicacion",
        )

    if kind == "common_binomials":
        left = sign * a
        middle = left + b
        constant = left * b
        answer = polynomial([(1, "x", 2), (middle, "x", 1), (constant, "", 1)])
        return question(
            f"Desarrolla (x {signed(left)})(x + {b}).",
            answer,
            [polynomial([(1, "x", 2), (constant, "x", 1), (middle, "", 1)]), polynomial([(1, "x", 2), (middle, "x", 1)]), polynomial([(1, "x", 2), (left-b, "x", 1), (constant, "", 1)])],
            "El coeficiente lineal es la suma de los términos no comunes y el independiente es su producto.",
            "aplicacion",
        )

    if kind == "factor_mono":
        common = gcd_many(a*b, a*c)
        minimum = min(p + 1, p)
        original = polynomial([(a*b, "x", p+1), (sign*a*c, "x", p)])
        inside = polynomial([
            (a*b // common, "x", 1),
            (sign*a*c // common, "", 1),
        ])
        answer = f"{term(common, 'x', minimum)}({inside})"
        return question(
            f"Factoriza {original} extrayendo el máximo factor común.",
            answer,
            [f"{a}({original})", f"{term(common, 'x', p+1)}({inside})", inside],
            "Se extraen el MCD de los coeficientes y la menor potencia común de x.",
            "aplicacion",
        )

    if kind == "factor_binomial":
        common = f"(x + {b})"
        answer = f"{common}({a}x {signed(sign*c)})"
        return question(
            f"Factoriza {a}x{common} {signed(sign*c)}{common}.",
            answer,
            [f"{common}({a+c}x)", f"(x + {a})({b}x {signed(sign*c)})", f"{a+c}{common}"],
            "El binomio completo es el factor común de ambos términos.",
            "aplicacion",
        )

    if kind == "grouping":
        answer = f"({a}x {signed(sign*b)})(y + {c})"
        original = polynomial([(a, "xy", 1), (a*c, "x", 1), (sign*b, "y", 1), (sign*b*c, "", 1)])
        return question(
            f"Factoriza por agrupación {original}.",
            answer,
            [f"({a}x + {c})(y {signed(sign*b)})", f"({a+b}x)(y + {c})", f"({a}x {signed(sign*b)})(y - {c})"],
            f"Los dos grupos producen el factor común (y+{c}).",
            "aplicacion",
        )

    if kind == "fraction_simple":
        answer = f"x + {a}"
        return question(
            f"Simplifica (x² - {a*a})/(x - {a}), con x ≠ {a}.",
            answer, [f"x - {a}", "x", f"x² + {a}"],
            f"x²-{a*a}=(x-{a})(x+{a}); se cancela el factor x-{a}, manteniendo la restricción.",
            "aplicacion",
        )

    if kind == "fraction_complex":
        answer = f"{c}(x + {b})"
        numerator = polynomial([(c, "x", 2), (c*(a+b), "x", 1), (c*a*b, "", 1)])
        return question(
            f"Simplifica ({numerator})/(x + {a}), con x ≠ {-a}.",
            answer, [f"{c}(x + {a})", f"x + {b}", f"{c}x + {a+b}"],
            f"El numerador factoriza como {c}(x+{a})(x+{b}); se cancela x+{a}.",
            "aplicacion",
        )

    if kind == "fraction_division":
        return question(
            f"Calcula [(x² - {a*a})/(x - {b})] ÷ [(x + {a})/(x - {b})], respetando las restricciones.",
            f"x - {a}", [f"x + {a}", "1", f"(x - {a})/(x + {a})"],
            "Se multiplica por el recíproco, se factoriza la diferencia de cuadrados y se cancelan factores.",
            "aplicacion",
        )

    if kind in {"lcm", "gcd"}:
        n1, n2, n3 = 2*a, 3*b, 2*c
        exponents = ((p, q), (q+1, p), (p+2, q+1))
        if kind == "lcm":
            coefficient = lcm(lcm(n1, n2), n3)
            ex = max(item[0] for item in exponents)
            ey = max(item[1] for item in exponents)
            label = "MCM"
        else:
            coefficient = gcd_many(n1, n2, n3)
            ex = min(item[0] for item in exponents)
            ey = min(item[1] for item in exponents)
            label = "MCD"
        answer = f"{coefficient}x^{ex}y^{ey}"
        expressions = ", ".join(
            f"{number}x^{powers[0]}y^{powers[1]}"
            for number, powers in zip((n1, n2, n3), exponents)
        )
        return question(
            f"Determina el {label} de {expressions}.",
            answer,
            [f"{coefficient}x^{max(1, ex-1)}y^{ey}", f"{coefficient}x^{ex}y^{ey+1}", f"{n1*n2*n3}x^{ex}y^{ey}"],
            f"Se calcula el {label} numérico y se eligen los exponentes {'mayores' if kind == 'lcm' else 'menores comunes'}.",
            "aplicacion",
        )

    raise ValueError(f"Generador no implementado: {kind}")


def procedural_item(spec, index):
    base = calculation(spec[0], index)
    correct = next(
        choice["text"] for choice in base["choices"] if choice["is_correct"]
    )
    wrong = [
        choice["text"] for choice in base["choices"] if not choice["is_correct"]
    ]
    family = index % 6
    context = (
        "cuidando signos y coeficientes",
        "respetando variables y exponentes",
        "sin omitir transformaciones intermedias",
        "comprobando la equivalencia final",
        "siguiendo el método explicado en la clase",
    )[index // 6]
    if family == 0:
        base["text"] = f"Resuelve {context}: {base['text']}"
        return base
    if family == 1:
        return question(
            f"Para resolver «{base['text']}» {context}, ¿qué justificación conduce a {correct}?",
            base["explanation"],
            [
                "Se elige la expresión de mayor grado sin efectuar operaciones.",
                "Se eliminan signos y exponentes antes de comparar.",
                "Se conserva únicamente el primer término de la expresión.",
            ],
            base["explanation"],
            "analisis",
        )
    if family == 2:
        return question(
            f"Al resolver «{base['text']}», Elisa obtiene {correct} y Martín obtiene {wrong[0]}. "
            "¿Quién aplicó correctamente el procedimiento?",
            "Elisa",
            ["Martín", "Ambos", "Ninguno"],
            base["explanation"],
            "analisis",
        )
    if family == 3:
        return question(
            f"Una pauta propone {wrong[0]} para «{base['text']}». ¿Cómo debe corregirse?",
            f"Debe reemplazarse por {correct}.",
            [
                "Debe mantenerse porque cualquier simplificación es válida.",
                "Solo debe cambiarse el signo.",
                "Deben eliminarse las variables.",
            ],
            base["explanation"],
            "analisis",
        )
    if family == 4:
        claim = correct if (index // 6) % 2 == 0 else wrong[0]
        evaluation = (
            "La afirmación es correcta."
            if claim == correct
            else f"La afirmación es incorrecta; corresponde {correct}."
        )
        return question(
            f"Se afirma que la respuesta de «{base['text']}» es {claim}. ¿Cómo se evalúa?",
            evaluation,
            [
                "Es correcta porque conserva algunos términos.",
                "No puede evaluarse con información algebraica.",
                "Es correcta si se ignoran los signos.",
            ],
            base["explanation"],
            "analisis",
        )
    first_step = base["explanation"].split(".", 1)[0]
    return question(
        f"¿Qué estrategia permite iniciar correctamente «{base['text']}» {context}?",
        first_step,
        [
            "Operar todos los números sin considerar la estructura.",
            "Eliminar paréntesis, factores o denominadores sin aplicar reglas.",
            "Escoger una alternativa y ajustar después el procedimiento.",
        ],
        base["explanation"],
        "aplicacion",
    )


def application_item(spec, index):
    base = calculation(spec[0], index + 30)
    correct = next(choice["text"] for choice in base["choices"] if choice["is_correct"])
    wrong = next(choice["text"] for choice in base["choices"] if not choice["is_correct"])
    family = index % 3
    contexts = (
        "control de calidad de una solución",
        "diseño de una pauta de corrección",
        "validación de un procedimiento automático",
        "comparación de dos métodos",
        "detección de un error frecuente",
        "revisión de una equivalencia algebraica",
        "preparación de una explicación tutorial",
        "análisis de una respuesta de evaluación",
        "comprobación mediante un método alternativo",
        "selección de una estrategia eficiente",
    )
    context = contexts[index // 3]
    if family == 0:
        return question(
            f"En una situación de {context} se plantea: «{base['text']}». "
            f"Camila obtiene {correct} y Tomás obtiene {wrong}. ¿Qué conclusión es válida?",
            f"Camila tiene razón: {base['explanation']}",
            [
                "Tomás tiene razón porque su respuesta es más breve.",
                "Ambos tienen razón para todos los valores.",
                "Ninguno puede verificar el resultado.",
            ],
            base["explanation"],
            "analisis",
        )
    if family == 1:
        return question(
            f"Durante una situación de {context}, un sistema debe resolver «{base['text']}». "
            "¿Qué resultado debe almacenar?",
            correct,
            [choice["text"] for choice in base["choices"] if not choice["is_correct"]],
            base["explanation"],
            "aplicacion",
        )
    return question(
        f"En una situación de {context}, un estudiante propone {wrong} para «{base['text']}». "
        "¿Cuál corrección corresponde?",
        f"Reemplazarlo por {correct}.",
        [
            "Mantenerlo porque toda simplificación es equivalente.",
            "Eliminar las variables de la respuesta.",
            "Cambiar únicamente el signo sin revisar el procedimiento.",
        ],
        base["explanation"],
        "analisis",
    )


def build_questions(slug):
    spec = SPECS[slug]
    random.seed(f"profeonline:lenguaje-algebraico:{slug}:2026-06-21")
    questions = []
    for level, builder in (
        (1, conceptual_item),
        (2, procedural_item),
        (3, application_item),
    ):
        for index in range(30):
            mode = MODES[index // 10]
            item = builder(spec, index)
            item["level"] = level
            item["mode"] = mode
            questions.append(item)
    return questions


def normalize(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def audit_bank(slug, questions):
    errors = []
    if len(questions) != 90:
        errors.append(f"total={len(questions)}")
    texts = [normalize(item["text"]) for item in questions]
    if len(texts) != len(set(texts)):
        errors.append("enunciados duplicados")
    matrix = {}
    for level in (1, 2, 3):
        for mode in MODES:
            count = sum(
                item["level"] == level and item["mode"] == mode
                for item in questions
            )
            matrix[f"N{level}_{mode}"] = count
            if count != 10:
                errors.append(f"N{level}/{mode}={count}")
    for index, item in enumerate(questions, 1):
        choices = item["choices"]
        choice_texts = [normalize(choice["text"]) for choice in choices]
        if len(choices) != 4 or len(choice_texts) != len(set(choice_texts)):
            errors.append(f"P{index}: alternativas inválidas")
        if sum(choice["is_correct"] for choice in choices) != 1:
            errors.append(f"P{index}: respuesta correcta inválida")
        if not item["explanation"].strip():
            errors.append(f"P{index}: explicación vacía")
    if errors:
        raise ValueError(f"{slug}: {'; '.join(errors)}")
    return matrix


def build_all():
    generated = {}
    for slug in SPECS:
        questions = build_questions(slug)
        matrix = audit_bank(slug, questions)
        generated[slug] = questions
        print(f"[OK] {slug}: {len(questions)} preguntas | {matrix}")
    return generated


def backup_resources(resources):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = BASE_DIR / "backups" / f"lenguaje_algebraico_before_{timestamp}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "resources": [
            {
                "id": resource.id,
                "slug": resource.slug,
                "questions": list(
                    resource.questions.values(
                        "id", "level", "mode", "status", "text", "audit_data"
                    )
                ),
            }
            for resource in resources
        ],
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def apply(generated):
    if settings.DEBUG:
        raise RuntimeError("Se rechaza la escritura con DEBUG=True")
    resources = list(
        Resource.objects.filter(topic__slug=TOPIC_SLUG)
        .select_related("topic")
        .order_by("id")
    )
    expected = set(SPECS)
    actual = {resource.slug for resource in resources}
    if actual != expected:
        raise RuntimeError(
            f"Inventario inesperado. Faltan={expected-actual}; sobran={actual-expected}"
        )
    existing = {
        resource.slug: resource.questions.count()
        for resource in resources
        if resource.questions.exists()
    }
    if existing:
        raise RuntimeError(f"Hay preguntas preexistentes; no se reemplaza: {existing}")
    backup = backup_resources(resources)

    with transaction.atomic():
        locked = {
            resource.slug: resource
            for resource in Resource.objects.select_for_update().filter(
                id__in=[resource.id for resource in resources]
            )
        }
        question_objects = []
        choice_payloads = []
        for slug, questions in generated.items():
            resource = locked[slug]
            transcript_hash = hashlib.sha256(
                resource.transcript.encode("utf-8")
            ).hexdigest()
            level_orders = {1: 0, 2: 0, 3: 0}
            for level in (1, 2, 3):
                for mode in MODES:
                    batch = [
                        item
                        for item in questions
                        if item["level"] == level and item["mode"] == mode
                    ]
                    for item in batch:
                        level_orders[level] += 1
                        question_object = Question(
                            resource=resource,
                            level=level,
                            mode=mode,
                            text=item["text"],
                            explanation=item["explanation"],
                            status="publicada",
                            order=level_orders[level],
                            audit_data={
                            "editorial_source": "codex_transcript",
                            "transcript_sha256": transcript_hash,
                            "topic": TOPIC_SLUG,
                            "generator": "lenguaje_algebraico_v1",
                            "cognitive_type": item["cognitive_type"],
                            },
                        )
                        question_objects.append(question_object)
                        choice_payloads.append((question_object, item["choices"]))
            ResourceQuizConfig.objects.update_or_create(
                resource=resource,
                defaults={"counts": COUNTS},
            )

        Question.objects.bulk_create(question_objects, batch_size=500)
        choices = [
            Choice(
                question=question_object,
                text=choice["text"],
                is_correct=choice["is_correct"],
                order=index,
            )
            for question_object, question_choices in choice_payloads
            for index, choice in enumerate(question_choices, 1)
        ]
        Choice.objects.bulk_create(choices, batch_size=1000)

        matrix = {
            (row["resource_id"], row["level"], row["mode"]): row["count"]
            for row in (
                Question.objects.filter(
                    resource_id__in=[resource.id for resource in resources],
                    status="publicada",
                )
                .values("resource_id", "level", "mode")
                .annotate(count=Count("id"))
            )
        }
        for resource in locked.values():
            for level in (1, 2, 3):
                for mode in MODES:
                    if matrix.get((resource.id, level, mode)) != 10:
                        raise RuntimeError(
                            f"{resource.slug}: matriz inválida N{level}/{mode}"
                        )
    return backup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm")
    args = parser.parse_args()
    generated = build_all()
    print(
        f"AUDIT_OK resources={len(generated)} "
        f"questions={sum(map(len, generated.values()))}"
    )
    if not args.apply:
        print("DRY_RUN_OK")
        return
    if args.confirm != CONFIRMATION:
        raise RuntimeError(f"Use --confirm {CONFIRMATION}")
    backup = apply(generated)
    print(f"APPLY_OK backup={backup}")


if __name__ == "__main__":
    main()

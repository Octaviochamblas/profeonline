"""Renueva de forma segura los recursos del tema Números Enteros.

El modo predeterminado es dry-run. La escritura en producción exige --apply y
una frase de confirmación. Antes de reemplazar preguntas o metadatos se crea un
respaldo JSON completo. Las preguntas se construyen localmente, sin Gemini.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import django


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_UPLOADER_DIR = BASE_DIR.parent.parent / "profeonline-uploader"
UPLOADER_DIR = Path(
    os.environ.get("PROFEONLINE_UPLOADER_DIR", DEFAULT_UPLOADER_DIR)
).expanduser().resolve()
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.conf import settings
from django.db import transaction

from apps.content.models import Choice, Question, Resource, ResourceQuizConfig
from apps.content.services.ai_generation_service import _save_questions
from apps.content.services.transcript_service import fetch_transcript


CONFIRMATION = "REEMPLAZAR_BANCO_NUMEROS_ENTEROS"
MODES = ("preparacion", "evaluacion", "ambas")
QUIZ_COUNTS = {
    str(level): {
        "practice": {"pool": 20, "shown": 5},
        "eval": {"pool": 20, "shown": 5 if level < 3 else 3},
    }
    for level in (1, 2, 3)
}

RESOURCE_DATA = {
    "11-que-son-los-numeros": {
        "video_id": "rFwyRipjDOY",
        "focus": "qué son los números y para qué sirven",
        "summary": (
            "Comprende los números como ideas que permiten contar, ordenar, medir y "
            "representar cantidades, diferenciando el concepto numérico del símbolo escrito."
        ),
        "outcomes": [
            "Distinguir un número de la cifra o símbolo que lo representa.",
            "Reconocer usos de los números para contar, ordenar, medir e identificar.",
            "Interpretar información numérica en situaciones cotidianas.",
        ],
    },
    "12-conjuntos-numericos": {
        "video_id": "yfUsZZrL7PA",
        "focus": "conjuntos numéricos y relaciones de inclusión",
        "summary": (
            "Revisa números naturales, enteros, racionales, irracionales y reales, con "
            "ejemplos que ayudan a clasificar valores y entender cómo se relacionan los conjuntos."
        ),
        "outcomes": [
            "Clasificar números en los conjuntos que les corresponden.",
            "Reconocer inclusiones entre naturales, enteros, racionales y reales.",
            "Justificar por qué un número pertenece o no a un conjunto.",
        ],
    },
    "13-numeros-enteros-relaciones-de-orden-mayor-menor-e-igual": {
        "video_id": "khau52eLlCQ",
        "focus": "orden y comparación de números enteros",
        "summary": (
            "Aprende a comparar números enteros con la recta numérica y a usar correctamente "
            "los signos mayor que, menor que e igual, incluyendo números negativos."
        ),
        "outcomes": [
            "Ubicar y comparar enteros en la recta numérica.",
            "Usar correctamente <, > e =.",
            "Ordenar datos positivos y negativos en contextos reales.",
        ],
    },
    "14-valor-absoluto-relaciones-de-orden": {
        "video_id": "EkcPbQAz1I4",
        "focus": "valor absoluto como distancia al cero",
        "summary": (
            "Estudia el valor absoluto como distancia al cero, su relación con números opuestos "
            "y su uso para comparar distancias sin confundirlas con el orden de los enteros."
        ),
        "outcomes": [
            "Interpretar |a| como distancia al cero.",
            "Calcular valores absolutos y resolver igualdades sencillas.",
            "Aplicar distancias numéricas en temperaturas, alturas y desplazamientos.",
        ],
    },
    "15-regla-de-signos-para-sumasrestas": {
        "video_id": "RVj8kW9QjSI",
        "focus": "reglas de signos en sumas y restas de enteros",
        "summary": (
            "Explica cómo sumar enteros de igual y distinto signo y cómo transformar una resta "
            "en suma del opuesto para decidir correctamente el signo del resultado."
        ),
        "outcomes": [
            "Aplicar la regla de signos en sumas de enteros.",
            "Transformar restas en sumas del opuesto.",
            "Explicar el signo del resultado usando valores absolutos.",
        ],
    },
    "15a-ejercicios-de-sumas-y-restas-aplicacion-de-regla-de-los-signos": {
        "video_id": "vHWVe72pVc0",
        "focus": "ejercicios de sumas y restas con números enteros",
        "summary": (
            "Resuelve ejercicios guiados de suma y resta de enteros, con énfasis en organizar "
            "signos, detectar errores y comprobar cada resultado."
        ),
        "outcomes": [
            "Resolver cadenas de sumas y restas con signos.",
            "Detectar y corregir errores frecuentes de procedimiento.",
            "Comprobar resultados mediante operaciones inversas o estimación.",
        ],
    },
    "16-regla-de-los-signos-en-multiplicaciondivision-ejemplos": {
        "video_id": "GGc-UZRUD90",
        "focus": "regla de signos en multiplicación y división",
        "summary": (
            "Trabaja la ley de signos en productos y cocientes de enteros, separando el cálculo "
            "del valor absoluto de la determinación del signo."
        ),
        "outcomes": [
            "Predecir el signo de productos y cocientes.",
            "Multiplicar y dividir enteros correctamente.",
            "Resolver factores o dividendos desconocidos.",
        ],
    },
    "17-prioridad-de-operaciones-sumarestamultiplicaciondivision-combinadas": {
        "video_id": "j1EyI6Or4vQ",
        "focus": "prioridad de operaciones combinadas",
        "summary": (
            "Aplica la prioridad de paréntesis, multiplicaciones, divisiones, sumas y restas "
            "para resolver expresiones combinadas sin alterar su significado."
        ),
        "outcomes": [
            "Identificar la operación que debe resolverse primero.",
            "Resolver expresiones combinadas paso a paso.",
            "Analizar errores causados por ignorar la prioridad.",
        ],
    },
    "18-numeros-primos-multiplos-y-divisores": {
        "video_id": "UzkH1lrlJ6w",
        "focus": "números primos, múltiplos y divisores",
        "summary": (
            "Introduce números primos y compuestos, múltiplos y divisores, junto con criterios "
            "para reconocer relaciones de divisibilidad y descomponer números."
        ),
        "outcomes": [
            "Distinguir números primos de compuestos.",
            "Encontrar múltiplos, divisores y factores primos.",
            "Usar divisibilidad para organizar cantidades exactas.",
        ],
    },
    "19-minimo-comun-multiplo-maximo-comun-divisor": {
        "video_id": "2Kk55AKkvyw",
        "focus": "mínimo común múltiplo y máximo común divisor",
        "summary": (
            "Diferencia el mínimo común múltiplo del máximo común divisor y explica cómo "
            "calcularlos mediante múltiplos, divisores o factorización prima."
        ),
        "outcomes": [
            "Decidir cuándo corresponde usar MCM o MCD.",
            "Calcular MCM y MCD con distintos métodos.",
            "Interpretar resultados en coincidencias y repartos exactos.",
        ],
    },
    "19a-ejercicios-minimo-comun-multiplo": {
        "video_id": "zb1m0mWyJCE",
        "focus": "ejercicios de mínimo común múltiplo",
        "summary": (
            "Desarrolla ejercicios de MCM con dos y tres números, usando descomposición prima, "
            "verificación por múltiplos y problemas de coincidencia periódica."
        ),
        "outcomes": [
            "Calcular el MCM de dos o tres números.",
            "Revisar exponentes en la factorización prima.",
            "Modelar situaciones periódicas con el MCM.",
        ],
    },
}


def choice(text, correct=False):
    return {"text": str(text), "is_correct": correct}


def question(text, correct, wrongs, explanation):
    alternatives = [str(correct), *(str(item) for item in wrongs)]
    unique = []
    for item in alternatives:
        if item not in unique:
            unique.append(item)
    fallbacks = [
        "No se puede determinar con la información entregada.",
        "El valor opuesto al resultado correcto.",
        "Cero, porque interviene un número negativo.",
        "La suma de todos los datos sin considerar la operación.",
    ]
    for fallback in fallbacks:
        if len(unique) >= 4:
            break
        if fallback not in unique:
            unique.append(fallback)
    return {
        "text": text,
        "explanation": explanation,
        "choices": [choice(unique[0], True)] + [choice(item) for item in unique[1:4]],
    }


def nq(text, answer, explanation, wrongs=None, unit=""):
    answer_text = f"{answer}{unit}"
    if wrongs is None:
        if isinstance(answer, int):
            candidates = [-answer, answer + 1, answer - 1, 0, abs(answer)]
        else:
            candidates = ["0", "1", "No existe"]
        wrongs = [f"{value}{unit}" for value in candidates if f"{value}{unit}" != answer_text][:3]
    return question(text, answer_text, wrongs, explanation)


def expand_seed(seed, mode):
    correct = next(item["text"] for item in seed["choices"] if item["is_correct"])
    wrong = next(item["text"] for item in seed["choices"] if not item["is_correct"])
    explanation = seed["explanation"].strip()
    if mode == "preparacion":
        return seed
    if mode == "evaluacion":
        return question(
            f"Un estudiante respondió «{wrong}» ante esta tarea: {seed['text']} "
            "¿Cuál es el diagnóstico correcto?",
            f"La respuesta es «{correct}»; la propuesta del estudiante es incorrecta.",
            [
                "La propuesta es correcta porque conserva los datos del enunciado.",
                "Ambas respuestas son equivalentes.",
                "No es posible decidir sin cambiar el ejercicio.",
            ],
            f"La propuesta es incorrecta. {explanation}",
        )
    return question(
        f"Para resolver con fundamento la tarea «{seed['text']}», ¿qué argumento es válido?",
        explanation,
        [
            "Basta escoger la alternativa con el número de mayor valor absoluto.",
            "Se pueden ignorar los signos porque solo cambian la escritura.",
            "Conviene sumar todos los números visibles antes de interpretar la pregunta.",
        ],
        explanation,
    )


def concept_seeds(slug):
    if slug == "11-que-son-los-numeros":
        return [
            question("¿Qué es un número?", "Una idea matemática que representa cantidad, orden o medida.", ["Solo el dibujo de una cifra.", "Una palabra usada únicamente para contar.", "Un objeto físico."], "Un número es un concepto; las cifras son símbolos usados para escribirlo."),
            question("¿Qué diferencia hay entre el número cinco y la cifra 5?", "El número es la idea de cantidad y la cifra es su representación escrita.", ["No existe diferencia.", "La cifra es la cantidad y el número es el dibujo.", "El número solo puede escribirse con palabras."], "La cantidad cinco puede representarse con 5, V, cinco u otros sistemas."),
            question("¿Cuál es un uso cardinal de los números?", "Indicar cuántos elementos hay.", ["Indicar la posición en una fila.", "Nombrar una camiseta.", "Marcar un código postal."], "El uso cardinal responde a la pregunta cuántos."),
            question("¿Cuál es un uso ordinal de los números?", "Indicar el lugar que ocupa un elemento.", ["Medir una longitud.", "Contar monedas.", "Identificar un teléfono."], "El uso ordinal expresa primero, segundo, tercero y otras posiciones."),
            question("¿Qué uso numérico aparece al decir que una mesa mide 120 cm?", "Medición.", ["Orden.", "Identificación.", "Conteo de objetos."], "La medida compara una magnitud con una unidad."),
            question("En el número de una camiseta, ¿qué función puede cumplir el número?", "Identificar a un jugador.", ["Expresar necesariamente una cantidad.", "Indicar siempre su edad.", "Medir su estatura."], "Un número también puede funcionar como etiqueta o identificador."),
            question("¿Por qué distintos símbolos pueden representar el mismo número?", "Porque el concepto numérico no depende del sistema de escritura.", ["Porque toda cifra vale lo mismo.", "Porque los números no representan cantidades.", "Porque solo existe un sistema numérico."], "La misma cantidad puede escribirse de distintas maneras según el sistema."),
            question("¿Qué permite hacer un sistema de numeración?", "Representar números mediante símbolos y reglas.", ["Crear cantidades físicas.", "Eliminar la necesidad de contar.", "Convertir todo número en una palabra."], "Los sistemas de numeración establecen símbolos y reglas de combinación."),
            question("¿Cuál afirmación describe mejor al cero?", "Es un número que puede representar ausencia de cantidad y servir como referencia.", ["No es un número.", "Siempre significa deuda.", "Solo se usa como cifra final."], "El cero tiene significado numérico y cumple funciones importantes en la escritura posicional."),
            question("¿Qué información aporta el contexto al interpretar un número?", "Permite saber si expresa cantidad, orden, medida o identificación.", ["Cambia automáticamente su valor.", "Elimina su representación escrita.", "Hace que todos los números sean positivos."], "El mismo número puede cumplir funciones distintas según la situación."),
        ]
    if slug == "12-conjuntos-numericos":
        return [
            question("¿Qué números forman el conjunto de los enteros?", "Los negativos, el cero y los positivos sin parte fraccionaria.", ["Solo los positivos.", "Todas las fracciones.", "Solo los negativos."], "Los enteros amplían a los naturales incorporando cero y negativos."),
            question("¿Cuál inclusión es correcta?", "Todo número natural es entero.", ["Todo entero es natural.", "Todo real es entero.", "Ningún natural es racional."], "Los naturales están contenidos en los enteros."),
            question("¿Por qué -7 no es un número natural?", "Porque es negativo.", ["Porque no es real.", "Porque tiene infinitos decimales.", "Porque es una fracción."], "Los naturales se usan para contar y no incluyen enteros negativos."),
            question("¿Qué caracteriza a un número racional?", "Puede escribirse como cociente de dos enteros con denominador distinto de cero.", ["Tiene que ser positivo.", "No puede tener decimales.", "Su decimal nunca se repite."], "Los racionales incluyen enteros, fracciones y decimales finitos o periódicos."),
            question("¿Cuál número es irracional?", "√2", ["3/4", "-5", "0,25"], "√2 no puede expresarse como fracción de enteros y su decimal no es periódico."),
            question("¿A qué conjunto pertenecen racionales e irracionales?", "A los números reales.", ["Solo a los naturales.", "Solo a los enteros.", "A conjuntos sin relación."], "Los reales reúnen racionales e irracionales."),
            question("¿Por qué todo entero es racional?", "Porque puede escribirse con denominador 1.", ["Porque todo entero tiene decimales infinitos.", "Porque los enteros son siempre positivos.", "Porque racional significa real."], "Por ejemplo, -4 = -4/1."),
            question("¿Qué representa un diagrama de conjuntos numéricos anidados?", "Las relaciones de inclusión entre conjuntos.", ["El orden de menor a mayor.", "La frecuencia con que se usa cada número.", "La cantidad de cifras de cada número."], "La inclusión muestra que todo elemento del conjunto interior pertenece al exterior."),
            question("¿Cuál afirmación sobre el cero es correcta?", "Es entero, racional y real.", ["Es irracional.", "Solo es natural.", "No pertenece a ningún conjunto."], "0 es entero y puede escribirse 0/1, por lo que también es racional y real."),
            question("¿Qué basta para refutar que todo real es racional?", "Exhibir un real irracional, como π.", ["Mostrar un entero positivo.", "Escribir una fracción.", "Usar el número cero."], "Un contraejemplo irracional demuestra que la inclusión inversa es falsa."),
        ]
    if slug == "13-numeros-enteros-relaciones-de-orden-mayor-menor-e-igual":
        return [
            question("En la recta numérica, ¿qué entero es mayor?", "El que está más a la derecha.", ["El más alejado de cero.", "El que tiene signo negativo.", "El que posee más cifras."], "La posición horizontal determina el orden: derecha significa mayor."),
            question("¿Qué expresa el símbolo < ?", "Que el valor de la izquierda es menor.", ["Que ambos valores son iguales.", "Que el valor izquierdo es mayor.", "Que se suman los valores."], "La abertura del símbolo mira hacia el número mayor."),
            question("¿Qué expresa el símbolo > ?", "Que el valor de la izquierda es mayor.", ["Que el valor izquierdo es menor.", "Que ambos son opuestos.", "Que se resta el segundo."], "El vértice apunta hacia el número menor."),
            question("¿Cómo se comparan un entero positivo y uno negativo?", "El positivo siempre es mayor.", ["El negativo siempre es mayor.", "Son iguales si tienen el mismo valor absoluto.", "Depende de cuántas cifras tengan."], "Todo positivo está a la derecha de todo negativo."),
            question("Entre dos enteros negativos, ¿cuál es mayor?", "El que está más cerca de cero.", ["El de mayor valor absoluto.", "El que tiene más cifras.", "Siempre son iguales."], "Entre negativos, acercarse a cero significa desplazarse a la derecha."),
            question("¿Qué relación tienen -6 y 6?", "Son opuestos, pero 6 es mayor.", ["Son iguales.", "-6 es mayor.", "No se pueden comparar."], "Están a igual distancia de cero, aunque ocupan posiciones distintas."),
            question("¿Qué significa a = b?", "Que ambos símbolos representan el mismo valor.", ["Que a está a la derecha de b.", "Que a tiene mayor valor absoluto.", "Que uno es positivo y otro negativo."], "La igualdad indica coincidencia de valor."),
            question("¿Qué es ordenar enteros de menor a mayor?", "Escribirlos desde el más ubicado a la izquierda hasta el más ubicado a la derecha.", ["Ordenarlos por valor absoluto.", "Poner primero los positivos.", "Eliminar los negativos."], "El orden creciente sigue la recta numérica de izquierda a derecha."),
            question("¿Cuál es el sucesor de un entero?", "El entero que está una unidad a su derecha.", ["Su opuesto.", "El doble del entero.", "El número más cercano a cero."], "El sucesor de n es n + 1."),
            question("¿Cuál es el predecesor de un entero?", "El entero que está una unidad a su izquierda.", ["Su valor absoluto.", "El número n + 1.", "El entero positivo asociado."], "El predecesor de n es n - 1."),
        ]
    if slug == "14-valor-absoluto-relaciones-de-orden":
        return [
            question("¿Qué representa |a|?", "La distancia de a al cero.", ["El opuesto de a en todos los casos.", "La distancia entre a y 1.", "El signo de a."], "El valor absoluto mide distancia y por eso nunca es negativo."),
            question("¿Por qué |-8| = 8?", "Porque -8 está a ocho unidades del cero.", ["Porque se elimina cualquier cifra negativa.", "Porque -8 es mayor que 8.", "Porque se suman -8 y 8."], "La distancia al cero es 8, independientemente del sentido."),
            question("¿Cuál es el valor absoluto de cero?", "0", ["1", "-1", "No está definido"], "El cero está a distancia cero de sí mismo."),
            question("¿Puede un valor absoluto ser negativo?", "No, porque representa una distancia.", ["Sí, cuando el número original es negativo.", "Sí, si está a la izquierda.", "Solo cuando vale cero."], "Toda distancia es mayor o igual que cero."),
            question("¿Qué relación existe entre |7| y |-7|?", "Son iguales.", ["El primero es mayor.", "El segundo es mayor.", "Son opuestos."], "7 y -7 están a la misma distancia del cero."),
            question("Si |x| = 5, ¿qué valores puede tomar x?", "5 y -5", ["Solo 5", "Solo -5", "0 y 5"], "Hay dos puntos a distancia cinco del cero."),
            question("¿Qué indica que |a| < |b|?", "Que a está más cerca de cero que b.", ["Que a siempre es menor que b.", "Que a es positivo.", "Que b es negativo."], "La comparación de valores absolutos compara distancias, no necesariamente orden."),
            question("¿Cuál es la diferencia entre opuesto y valor absoluto?", "El opuesto cambia el signo; el valor absoluto entrega la distancia al cero.", ["Son siempre la misma operación.", "El valor absoluto cambia el signo y el opuesto mide.", "Ninguna de las dos usa el cero."], "Por ejemplo, el opuesto de 4 es -4, pero |4| = 4."),
            question("¿Cómo se interpreta |a-b|?", "Como la distancia entre a y b.", ["Como la suma de sus distancias.", "Como el menor de los dos.", "Como el opuesto de a."], "La diferencia absoluta mide separación en la recta numérica."),
            question("¿Qué error hay en afirmar |-3| = -3?", "Una distancia no puede ser negativa.", ["Ninguno.", "El resultado debería ser cero.", "Solo faltó cambiar 3 por 6."], "|-3| vale 3."),
        ]
    if slug in {
        "15-regla-de-signos-para-sumasrestas",
        "15a-ejercicios-de-sumas-y-restas-aplicacion-de-regla-de-los-signos",
    }:
        exercise = slug.startswith("15a")
        return [
            question("Al sumar enteros del mismo signo, ¿qué se hace?", "Se suman los valores absolutos y se conserva el signo.", ["Se restan los valores absolutos.", "Siempre se obtiene cero.", "Se conserva el signo positivo."], "La suma acumula cantidades en el mismo sentido."),
            question("Al sumar enteros de distinto signo, ¿qué se hace?", "Se restan los valores absolutos y se conserva el signo del mayor valor absoluto.", ["Se suman y se deja signo negativo.", "Se multiplican los signos.", "Siempre se conserva el primer signo."], "Los sentidos opuestos se compensan."),
            question("¿A qué equivale restar un entero?", "A sumar su opuesto.", ["A sumar su valor absoluto.", "A cambiar el signo del primer número.", "A dividir por -1."], "a - b = a + (-b)."),
            question("¿Qué ocurre al restar un número negativo?", "Se transforma en una suma del positivo correspondiente.", ["El resultado siempre es negativo.", "Se eliminan ambos números.", "Se conserva la resta sin cambios."], "a - (-b) = a + b."),
            question("¿Cuál es el inverso aditivo de -9?", "9", ["-9", "0", "1/9"], "Un número y su inverso aditivo suman cero."),
            question("¿Cuándo una suma de dos enteros da cero?", "Cuando los sumandos son opuestos.", ["Cuando ambos son negativos.", "Cuando tienen distinto signo cualquiera.", "Cuando uno es mayor que el otro."], "a + (-a) = 0."),
            question("¿Cómo ayuda la recta numérica a sumar +4?", "Desplazándose cuatro unidades a la derecha.", ["Moviéndose cuatro unidades a la izquierda.", "Cambiando el signo del punto inicial.", "Volviendo siempre al cero."], "Los positivos representan desplazamientos hacia la derecha."),
            question("¿Cómo se representa sumar -6 en la recta numérica?", "Desplazándose seis unidades a la izquierda.", ["Moviéndose seis a la derecha.", "Saltando al opuesto.", "Multiplicando la posición por seis."], "Los negativos representan desplazamientos hacia la izquierda."),
            question("¿Qué conviene hacer primero en una cadena de sumas y restas?", "Transformar las restas en sumas del opuesto y organizar los signos.", ["Borrar los paréntesis sin revisar.", "Sumar solo los valores positivos.", "Cambiar todos los signos a positivo."], "Una escritura uniforme reduce errores de signo."),
            question(
                "¿Qué habilidad distingue a una revisión correcta de ejercicios?" if exercise else "¿Cómo se justifica el signo final de una suma con signos distintos?",
                "Comprobar la operación y explicar qué valor absoluto domina." if exercise else "Comparando los valores absolutos de los sumandos.",
                ["Elegir el signo del primer número.", "Contar la cantidad de cifras.", "Usar siempre signo positivo."],
                "El signo se determina por la magnitud dominante y puede verificarse con una operación inversa.",
            ),
        ]
    if slug == "16-regla-de-los-signos-en-multiplicaciondivision-ejemplos":
        return [
            question("¿Qué signo tiene el producto de dos enteros con igual signo?", "Positivo.", ["Negativo.", "Cero.", "Depende del valor absoluto."], "Signos iguales producen resultado positivo."),
            question("¿Qué signo tiene el producto de enteros con distinto signo?", "Negativo.", ["Positivo.", "Cero.", "No está definido."], "Signos diferentes producen resultado negativo."),
            question("¿Qué signo tiene el cociente de dos negativos?", "Positivo.", ["Negativo.", "Cero.", "Irracional."], "La división sigue la misma ley de signos que la multiplicación."),
            question("¿Qué signo tiene un cociente entre positivo y negativo?", "Negativo.", ["Positivo.", "Cero.", "Depende del divisor."], "Los signos son diferentes."),
            question("¿Qué resultado da cualquier entero multiplicado por cero?", "Cero.", ["El mismo entero.", "Su opuesto.", "Uno."], "El cero es elemento absorbente de la multiplicación."),
            question("¿Está definida la división de un entero por cero?", "No.", ["Sí, y da cero.", "Sí, y da el mismo entero.", "Solo si el entero es negativo."], "No existe un número que multiplicado por cero recupere un dividendo no nulo."),
            question("¿Cómo se determina el signo de un producto de varios factores?", "Contando cuántos factores negativos hay.", ["Mirando solo el primer factor.", "Sumando los signos.", "Eligiendo el mayor valor absoluto."], "Una cantidad par de negativos da positivo; una impar da negativo."),
            question("¿Qué conviene separar al multiplicar enteros?", "El cálculo de los valores absolutos y la determinación del signo.", ["Los factores positivos de los negativos y no reunirlos.", "El signo del resultado del valor cero.", "La multiplicación de la operación original."], "Separar magnitud y signo ordena el procedimiento."),
            question("¿Por qué (-a)(-b) es positivo si a y b son positivos?", "Porque intervienen dos cambios de sentido.", ["Porque todo producto es positivo.", "Porque se eliminan las letras.", "Porque a y b son iguales."], "Dos signos negativos en un producto se combinan en positivo."),
            question("Si ab es negativo y a es positivo, ¿qué signo tiene b?", "Negativo.", ["Positivo.", "Cero.", "No se puede saber."], "Para obtener producto negativo los factores deben tener signos distintos."),
        ]
    if slug == "17-prioridad-de-operaciones-sumarestamultiplicaciondivision-combinadas":
        return [
            question("Sin paréntesis, ¿qué se resuelve antes: suma o multiplicación?", "La multiplicación.", ["La suma.", "La operación de la izquierda siempre.", "Ambas al mismo tiempo."], "Multiplicación y división tienen prioridad sobre suma y resta."),
            question("¿Qué se resuelve primero cuando hay paréntesis?", "Las operaciones dentro de los paréntesis.", ["La suma exterior.", "La última operación.", "Los números negativos."], "Los agrupadores modifican el orden natural."),
            question("Entre multiplicación y división, ¿cómo se decide el orden?", "De izquierda a derecha.", ["Siempre división primero.", "Siempre multiplicación primero.", "Por el valor más grande."], "Tienen la misma prioridad."),
            question("Entre suma y resta, ¿cómo se decide el orden?", "De izquierda a derecha.", ["Siempre suma primero.", "Siempre resta primero.", "Se elige la más fácil."], "Tienen la misma prioridad."),
            question("¿Por qué 2 + 3·4 no es igual a (2+3)·4?", "Porque los paréntesis cambian la prioridad.", ["Porque la multiplicación no admite paréntesis.", "Porque 2 deja de ser entero.", "Porque ambas expresiones sí son iguales."], "La primera vale 14 y la segunda 20."),
            question("¿Qué riesgo tiene resolver siempre de izquierda a derecha?", "Ignorar la prioridad de multiplicaciones y divisiones.", ["Obtener siempre números negativos.", "Eliminar los paréntesis correctamente.", "Convertir enteros en fracciones."], "La lectura lineal solo sirve entre operaciones de igual prioridad."),
            question("¿Qué debe conservarse al escribir cada paso?", "Las operaciones que todavía no se han resuelto.", ["Solo el último número.", "Los signos positivos.", "La respuesta esperada."], "Mantener la expresión evita perder términos o signos."),
            question("¿Qué función cumplen los paréntesis anidados?", "Indicar que se resuelve primero el grupo más interno.", ["Cancelar signos negativos.", "Transformar productos en sumas.", "Separar números pares."], "Se avanza desde el agrupador interior hacia el exterior."),
            question("¿Cómo se detecta un error de prioridad?", "Comparando cada paso con la jerarquía de operaciones.", ["Revisando solo el signo final.", "Contando la cantidad de números.", "Cambiando el resultado por su opuesto."], "El procedimiento debe respetar agrupadores y niveles de prioridad."),
            question("¿Qué significa resolver una expresión paso a paso?", "Aplicar una operación válida por vez y conservar el resto.", ["Separar todos los números.", "Sumar primero los positivos.", "Eliminar signos y paréntesis."], "Cada igualdad debe ser equivalente a la expresión anterior."),
        ]
    if slug == "18-numeros-primos-multiplos-y-divisores":
        return [
            question("¿Qué es un número primo?", "Un entero mayor que 1 con exactamente dos divisores positivos.", ["Cualquier número impar.", "Un entero con más de dos divisores.", "Todo múltiplo de 2."], "Los divisores positivos de un primo son 1 y él mismo."),
            question("¿Qué es un número compuesto?", "Un entero mayor que 1 con más de dos divisores positivos.", ["Un número negativo.", "Un número con exactamente un divisor.", "Cualquier número par, incluido 2."], "Los compuestos pueden escribirse como producto no trivial de enteros."),
            question("¿Por qué 1 no es primo?", "Porque tiene un solo divisor positivo.", ["Porque es impar.", "Porque no es entero.", "Porque es múltiplo de todos."], "La definición de primo exige exactamente dos divisores."),
            question("¿Cuál es el único primo par?", "2", ["0", "4", "6"], "Todo par mayor que 2 es divisible por 1, 2 y por sí mismo."),
            question("¿Qué es un múltiplo de n?", "Un número obtenido al multiplicar n por un entero.", ["Un número que divide a n.", "El resto de dividir n.", "Solo el doble de n."], "Los múltiplos de n tienen la forma n·k."),
            question("¿Qué significa que d sea divisor de n?", "Que n/d es entero y la división es exacta.", ["Que d es mayor que n.", "Que n y d son primos.", "Que la división deja resto 1."], "Un divisor reparte exactamente la cantidad."),
            question("¿Qué relación conecta múltiplos y divisores?", "Si n es múltiplo de d, entonces d es divisor de n.", ["Son conceptos sin relación.", "Todo múltiplo es menor que su divisor.", "Solo se relacionan números primos."], "Ambas expresiones describen la misma divisibilidad desde perspectivas opuestas."),
            question("¿Qué es una factorización prima?", "Escribir un número como producto de números primos.", ["Listar todos sus múltiplos.", "Sumar sus cifras.", "Dividirlo siempre por 10."], "La descomposición prima revela la estructura multiplicativa."),
            question("¿Qué criterio permite saber si un número es divisible por 2?", "Que su última cifra sea par.", ["Que termine en 5.", "Que la suma de cifras sea 2.", "Que sea primo."], "Las terminaciones 0, 2, 4, 6 y 8 indican divisibilidad por 2."),
            question("¿Qué criterio permite saber si un número es divisible por 3?", "Que la suma de sus cifras sea múltiplo de 3.", ["Que termine en 3.", "Que sea impar.", "Que tenga tres cifras."], "La suma de cifras conserva el resto módulo 3."),
        ]
    return [
        question("¿Qué representa el MCM?", "El menor múltiplo positivo común.", ["El mayor divisor común.", "La suma de los números.", "El menor divisor."], "El MCM busca la primera coincidencia positiva entre secuencias de múltiplos."),
        question("¿Qué representa el MCD?", "El mayor divisor positivo común.", ["El menor múltiplo común.", "El producto de los números.", "El mayor número del grupo."], "El MCD es el mayor tamaño que divide exactamente a todos."),
        question("¿Cuándo suele usarse el MCM?", "Cuando se busca una coincidencia de ciclos o denominadores.", ["Cuando se reparte en grupos máximos.", "Cuando se resta una cantidad.", "Cuando no hay periodicidad."], "El MCM encuentra una primera coincidencia común."),
        question("¿Cuándo suele usarse el MCD?", "Cuando se busca repartir o agrupar en el mayor tamaño exacto.", ["Cuando se sincronizan ciclos.", "Cuando se suman intervalos.", "Cuando se busca un múltiplo mayor."], "El MCD maximiza un tamaño que divide sin resto."),
        question("Si dos números son coprimos, ¿cuál es su MCD?", "1", ["0", "Su producto", "El menor de ellos"], "Los coprimos solo comparten el divisor 1."),
        question("Si a divide exactamente a b, ¿cuál es MCM(a,b)?", "b", ["a", "1", "a+b"], "Cuando b ya es múltiplo de a, la primera coincidencia es b."),
        question("Si a divide exactamente a b, ¿cuál es MCD(a,b)?", "a", ["b", "1", "a·b"], "El mayor divisor común es el propio a."),
        question("¿Qué relación cumplen dos enteros positivos a y b?", "MCM(a,b)·MCD(a,b)=a·b", ["MCM+MCD=a+b", "MCM=MCD siempre", "MCM·MCD=a+b"], "La identidad conecta ambos valores para dos enteros positivos."),
        question("En factorización prima, ¿cómo se forma el MCM?", "Tomando cada primo con el mayor exponente presente.", ["Tomando solo factores comunes.", "Usando los menores exponentes.", "Sumando los primos."], "El MCM debe contener suficientes factores para ser múltiplo de todos."),
        question("En factorización prima, ¿cómo se forma el MCD?", "Tomando los primos comunes con el menor exponente.", ["Tomando todos con mayor exponente.", "Multiplicando los números originales.", "Restando exponentes."], "El MCD solo conserva lo compartido por todos."),
    ]


def procedure_seeds(slug):
    if slug == "11-que-son-los-numeros":
        return [
            question("¿Qué función cumple el 18 en «18 estudiantes»?", "Cantidad.", ["Orden.", "Identificación.", "Medida de longitud."], "Responde cuántos estudiantes hay."),
            question("¿Qué función cumple el 3 en «tercer lugar»?", "Orden.", ["Cantidad.", "Código.", "Temperatura."], "Indica una posición."),
            question("¿Qué función cumple 24 en «24 °C»?", "Medida.", ["Identificación.", "Orden.", "Cantidad de termómetros."], "La cifra acompaña una unidad o escala de temperatura."),
            question("¿Qué función cumple 7 en «bus 7»?", "Identificación.", ["Cantidad de buses.", "Séptimo lugar necesariamente.", "Longitud."], "El número distingue una línea o recorrido."),
            question("¿Qué representación equivale a una decena y cuatro unidades?", "14", ["104", "41", "10"], "El sistema decimal posiciona una decena y cuatro unidades como 14."),
            question("¿Cuántas unidades representa el dígito 5 en 52?", "50", ["5", "2", "500"], "El 5 ocupa la posición de las decenas."),
            question("¿Cuál descomposición corresponde a 306?", "300 + 6", ["30 + 6", "300 + 60", "3 + 6"], "El cero indica ausencia de decenas."),
            question("¿Qué número está representado por «dos centenas, una decena y nueve unidades»?", "219", ["291", "209", "129"], "Se combinan 200 + 10 + 9."),
            question("¿Qué cambia al mover el dígito 4 de unidades a centenas?", "Su valor pasa de 4 a 400.", ["Su valor no cambia.", "Pasa a valer 40.", "Se vuelve negativo."], "El valor posicional depende de la ubicación."),
            question("¿Cuál escritura usa cifras para representar «mil veinticinco»?", "1025", ["125", "10025", "1520"], "Una unidad de mil, cero centenas, dos decenas y cinco unidades forman 1025."),
        ]
    if slug == "12-conjuntos-numericos":
        values = [
            ("-12", "Entero, racional y real.", ["Natural solamente.", "Irracional.", "No real."], "-12=-12/1."),
            ("0,75", "Racional y real.", ["Entero.", "Irracional.", "Natural."], "0,75=3/4."),
            ("√9", "Natural, entero, racional y real.", ["Irracional.", "Solo real.", "Entero negativo."], "√9=3."),
            ("π", "Irracional y real.", ["Racional.", "Entero.", "Natural."], "π no es cociente de enteros."),
            ("-3/2", "Racional y real.", ["Entero.", "Natural.", "Irracional."], "Es una fracción de enteros."),
            ("0", "Entero, racional y real.", ["Irracional.", "Solo natural.", "No pertenece a los reales."], "0=0/1."),
            ("2,333… periódico", "Racional y real.", ["Irracional.", "Entero.", "Natural."], "Todo decimal periódico representa una fracción."),
            ("√5", "Irracional y real.", ["Racional.", "Entero.", "Natural."], "√5 no es raíz exacta ni fracción."),
            ("14/7", "Natural, entero, racional y real.", ["Solo racional.", "Irracional.", "Entero negativo."], "14/7=2."),
            ("-√16", "Entero, racional y real.", ["Natural.", "Irracional.", "No real."], "-√16=-4."),
        ]
        return [question(f"Clasifica {value}.", correct, wrongs, explanation) for value, correct, wrongs, explanation in values]
    if slug == "13-numeros-enteros-relaciones-de-orden-mayor-menor-e-igual":
        return [
            question("Completa: -8 __ -3.", "-8 < -3", ["-8 > -3", "-8 = -3", "|-8| < |-3|"], "-8 está más a la izquierda."),
            question("Completa: 0 __ -11.", "0 > -11", ["0 < -11", "0 = -11", "No se comparan"], "Cero está a la derecha de todo negativo."),
            question("Ordena de menor a mayor: 4, -6, 0, -1.", "-6, -1, 0, 4", ["4, 0, -1, -6", "-1, -6, 0, 4", "-6, 0, -1, 4"], "Se sigue la recta de izquierda a derecha."),
            question("Ordena de mayor a menor: -2, 5, -9, 1.", "5, 1, -2, -9", ["-9, -2, 1, 5", "5, -2, 1, -9", "1, 5, -2, -9"], "Los positivos preceden a los negativos en orden decreciente."),
            nq("¿Cuál es el sucesor de -14?", -13, "El sucesor se obtiene sumando uno."),
            nq("¿Cuál es el predecesor de 0?", -1, "El predecesor se obtiene restando uno."),
            question("¿Qué entero está entre -5 y -3?", "-4", ["-6", "3", "4"], "-4 está una unidad a la derecha de -5."),
            question("¿Cuál es el mayor de {-12, -7, -20, -9}?", "-7", ["-20", "-12", "-9"], "Entre negativos, el más cercano a cero es mayor."),
            question("Escribe una desigualdad verdadera con -4 y 6.", "-4 < 6", ["-4 > 6", "-4 = 6", "4 < -6"], "Todo negativo es menor que todo positivo."),
            question("Si a < b y b < 3, ¿qué relación necesariamente vale?", "a < 3", ["a > 3", "a = 3", "a > b"], "La relación de orden es transitiva."),
        ]
    if slug == "14-valor-absoluto-relaciones-de-orden":
        return [
            nq("Calcula |-17|.", 17, "La distancia entre -17 y cero es 17."),
            nq("Calcula |23|.", 23, "La distancia entre 23 y cero es 23."),
            nq("Calcula -|-9|.", -9, "Primero |-9|=9 y luego se aplica el signo exterior."),
            question("Resuelve |x|=8.", "x=8 o x=-8", ["x=8 solamente", "x=-8 solamente", "x=0"], "Hay dos puntos a distancia ocho del cero."),
            question("¿Cuál es mayor: |-12| o |7|?", "|-12|", ["|7|", "Son iguales", "No se comparan"], "12 es mayor que 7."),
            nq("Calcula la distancia entre -6 y 5: |-6-5|.", 11, "La diferencia es -11 y su valor absoluto es 11."),
            nq("Calcula ||-4|-9|.", 5, "Primero |-4|=4; luego |4-9|=|-5|=5."),
            question("Resuelve |x|<3 en enteros.", "x∈{-2,-1,0,1,2}", ["x∈{-3,3}", "x>3", "x<-3"], "Son los enteros cuya distancia a cero es menor que tres."),
            question("Resuelve |x|=0.", "x=0", ["x=1", "x=-1", "No hay solución"], "Solo cero está a distancia cero de cero."),
            nq("Si |a|=6 y a es negativo, ¿cuál es a?", -6, "La condición de signo selecciona la solución negativa."),
        ]
    if slug in {"15-regla-de-signos-para-sumasrestas", "15a-ejercicios-de-sumas-y-restas-aplicacion-de-regla-de-los-signos"}:
        advanced = slug.startswith("15a")
        if not advanced:
            specs = [
                ("-8+(-5)", -13), ("14+(-9)", 5), ("-17+23", 6), ("-6-11", -17),
                ("9-(-7)", 16), ("-12-(-4)", -8), ("18+(-18)", 0), ("-25+8", -17),
                ("7-15+4", -4), ("-3+12-(-5)", 14),
            ]
        else:
            specs = [
                ("-18+7-12", -23), ("25-(-9)+(-14)", 20), ("-6-15+28-9", -2),
                ("42+(-17)-(-8)", 33), ("-30-(-12)-19", -37), ("8-23-(-11)+5", 1),
                ("-14+(-16)-(-25)", -5), ("50-18+(-27)-9", -4),
                ("-5-(-7)-(-9)+(-12)", -1), ("31+(-44)-(-6)+10", 3),
            ]
        return [
            nq(f"Resuelve {expr}.", ans, f"Al transformar restas y agrupar signos se obtiene {ans}.")
            for expr, ans in specs
        ]
    if slug == "16-regla-de-los-signos-en-multiplicaciondivision-ejemplos":
        return [
            nq("Calcula (-7)·6.", -42, "Signos distintos dan negativo y 7·6=42."),
            nq("Calcula (-8)·(-5).", 40, "Signos iguales dan positivo."),
            nq("Calcula 63÷(-9).", -7, "El cociente tiene signo negativo."),
            nq("Calcula (-72)÷(-8).", 9, "Dos negativos producen cociente positivo."),
            nq("Calcula (-3)·4·(-2).", 24, "Hay dos factores negativos, por lo que el producto es positivo."),
            nq("Calcula (-2)·(-3)·(-5).", -30, "Tres factores negativos producen signo negativo."),
            nq("Encuentra x: (-6)x=42.", -7, "x=42÷(-6)=-7."),
            nq("Encuentra x: x÷(-4)=9.", -36, "Multiplicando ambos lados por -4 se obtiene -36."),
            nq("Calcula 0·(-125).", 0, "Todo número multiplicado por cero da cero."),
            question("Determina solo el signo de (-2)(-3)(4)(-5)(-1).", "Positivo", ["Negativo", "Cero", "Indeterminado"], "Hay cuatro factores negativos, una cantidad par."),
        ]
    if slug == "17-prioridad-de-operaciones-sumarestamultiplicaciondivision-combinadas":
        specs = [
            ("8+3·(-4)", -4, "Primero 3·(-4)=-12; luego 8-12=-4."),
            ("18÷(-3)+7", 1, "Primero 18÷(-3)=-6; luego -6+7=1."),
            ("5-2·(3-7)", 13, "Primero 3-7=-4, luego 2·(-4)=-8 y 5-(-8)=13."),
            ("(-6+10)·3", 12, "Primero el paréntesis vale 4."),
            ("24÷(2·(-3))", -4, "El denominador agrupado vale -6."),
            ("7+18÷3-5", 8, "La división se resuelve antes que suma y resta."),
            ("(-2)·5+16÷4", -6, "Producto y división primero: -10+4=-6."),
            ("30-[4·(6-9)]", 42, "6-9=-3; 4·(-3)=-12; 30-(-12)=42."),
            ("48÷(-6)·2+3", -13, "División y multiplicación de izquierda a derecha: -8·2+3."),
            ("12-3·2+8÷4", 8, "Productos y cocientes primero: 12-6+2=8."),
        ]
        return [nq(f"Calcula {expr}.", ans, explanation) for expr, ans, explanation in specs]
    if slug == "18-numeros-primos-multiplos-y-divisores":
        return [
            question("Clasifica 29.", "Primo", ["Compuesto", "Ni primo ni compuesto", "Múltiplo de 4"], "Sus únicos divisores positivos son 1 y 29."),
            question("Clasifica 51.", "Compuesto", ["Primo", "Ni primo ni compuesto", "Potencia de 2"], "51=3·17."),
            question("¿Cuál lista contiene todos los divisores de 18?", "1, 2, 3, 6, 9, 18", ["1, 2, 9, 18", "2, 3, 6, 9", "1, 3, 9, 18"], "Cada valor divide 18 sin resto."),
            question("¿Cuál es el quinto múltiplo positivo de 7?", "35", ["28", "42", "49"], "7·5=35."),
            question("Descompón 60 en factores primos.", "2²·3·5", ["2·3·10", "3²·5", "2³·5"], "60=2·2·3·5."),
            question("¿Cuántos divisores positivos tiene 12?", "6", ["4", "5", "12"], "Son 1,2,3,4,6 y 12."),
            question("¿Es 132 divisible por 3?", "Sí, porque 1+3+2=6.", ["No, porque termina en 2.", "Sí, porque es par.", "No, porque 6 es compuesto."], "La suma de cifras es múltiplo de 3."),
            question("¿Cuál número es divisor de 84?", "12", ["5", "16", "25"], "84÷12=7."),
            question("¿Cuál número es múltiplo común de 6 y 8?", "24", ["12", "18", "30"], "24=6·4=8·3."),
            question("¿Cuál factor falta en 2³·3·__ = 120?", "5", ["2", "3", "10"], "120÷24=5."),
        ]
    if slug == "19a-ejercicios-minimo-comun-multiplo":
        sets = [(6, 8), (9, 12), (10, 15), (14, 21), (8, 12, 18), (4, 6, 10), (15, 20, 30), (16, 24), (18, 27), (12, 25)]
        return [
            nq(
                f"Calcula MCM({','.join(map(str, values))}).",
                math.lcm(*values),
                f"Tomando los factores primos con mayor exponente se obtiene {math.lcm(*values)}.",
            )
            for values in sets
        ]
    pairs = [(12, 18, "MCD"), (8, 20, "MCM"), (24, 36, "MCD"), (15, 25, "MCM"), (14, 21, "MCD"), (9, 12, "MCM"), (16, 24, "MCM"), (30, 45, "MCD"), (18, 30, "MCM"), (28, 42, "MCD")]
    result = []
    for a, b, kind in pairs:
        ans = math.gcd(a, b) if kind == "MCD" else math.lcm(a, b)
        result.append(nq(f"Calcula {kind}({a},{b}).", ans, f"El {kind} de {a} y {b} es {ans}."))
    return result


def application_seeds(slug):
    if slug == "11-que-son-los-numeros":
        return [
            question("Una receta indica 4 huevos. ¿Qué uso tiene el 4?", "Cantidad.", ["Orden.", "Identificación.", "Código."], "Indica cuántos huevos se necesitan."),
            question("Una atleta llega segunda. ¿Qué uso tiene el número 2?", "Orden.", ["Medida.", "Cantidad de pistas.", "Identificación telefónica."], "Describe su posición en la llegada."),
            question("Una carretera marca kilómetro 85. ¿Qué uso predomina?", "Medición de distancia.", ["Conteo de autos.", "Orden de conductores.", "Código sin magnitud."], "El kilometraje ubica una distancia desde un origen."),
            question("El departamento 304 está en un edificio. ¿Qué función cumple 304?", "Identificación.", ["Cantidad de habitantes.", "Temperatura.", "Precio."], "Distingue una unidad dentro del edificio."),
            question("Un envase contiene 750 mL. ¿Qué expresa 750?", "Una medida de volumen.", ["Una posición.", "Un número de serie necesariamente.", "Cantidad de envases."], "El número acompaña la unidad mililitro."),
            question("El dorsal 10 pertenece a una jugadora. ¿Significa que hay diez jugadoras?", "No necesariamente; funciona como identificador.", ["Sí, siempre.", "Indica su edad.", "Indica diez goles."], "Los dorsales etiquetan participantes."),
            question("Una sala tiene aforo 40. ¿Qué decisión permite ese número?", "Controlar la cantidad máxima de personas.", ["Ordenar las sillas por color.", "Medir la temperatura.", "Identificar el edificio."], "El valor cuantifica un límite."),
            question("Un ascensor muestra piso -2. ¿Qué información comunica?", "Una posición bajo el nivel de referencia.", ["Dos personas.", "Una medida de tiempo.", "Un código sin orden."], "El entero negativo localiza un piso subterráneo."),
            question("Un producto cuesta $12.990. ¿Qué representa el número?", "Una medida monetaria del precio.", ["Orden del producto.", "Cantidad de tiendas.", "Número telefónico."], "El contexto y el símbolo monetario fijan su significado."),
            question("Una app muestra 3 de 5 tareas completadas. ¿Qué aportan ambos números?", "Relacionan una cantidad lograda con un total.", ["Solo identifican tareas.", "Indican una temperatura.", "Expresan una posición geográfica."], "Los números permiten comparar avance y meta."),
        ]
    if slug == "12-conjuntos-numericos":
        return [
            question("Un saldo bancario es -$18.000. ¿Qué conjunto mínimo permite representarlo?", "Enteros.", ["Naturales.", "Irracionales.", "Solo positivos."], "Las deudas requieren números negativos."),
            question("Una longitud es 2,5 m. ¿Qué tipo de número la representa?", "Racional.", ["Entero.", "Natural.", "Irracional necesariamente."], "2,5=5/2."),
            question("La diagonal de un cuadrado de lado 1 mide √2. ¿Qué conjunto describe esa medida?", "Irracionales.", ["Enteros.", "Naturales.", "Racionales."], "√2 es un real irracional."),
            question("Un ascensor está en el piso 0. ¿A qué conjuntos pertenece el dato?", "Entero, racional y real.", ["Solo natural.", "Irracional.", "Ninguno."], "0 es entero y 0/1 es racional."),
            question("Un descuento es 1/4 del precio. ¿Qué conjunto mínimo lo contiene?", "Racionales.", ["Enteros.", "Naturales.", "Irracionales."], "Es un cociente de enteros."),
            question("Una calculadora muestra 3,141592… para π. ¿Qué precaución corresponde?", "El decimal mostrado es aproximado; π es irracional.", ["π es racional por tener cifras.", "π es entero.", "El decimal termina realmente."], "La pantalla trunca una expansión infinita no periódica."),
            question("Una temperatura de -3,5 °C, ¿es entera?", "No; es racional y real.", ["Sí, porque es negativa.", "Sí, porque es temperatura.", "No es real."], "-3,5=-7/2."),
            question("Se cuentan 28 entradas vendidas. ¿Qué conjunto mínimo basta?", "Naturales.", ["Irracionales.", "Negativos.", "Complejos no reales."], "El conteo usa un entero positivo."),
            question("Una probabilidad vale 0, ¿puede representarse como racional?", "Sí, como 0/1.", ["No, porque no es positivo.", "Solo como irracional.", "No pertenece a los reales."], "Cero es racional."),
            question("Un modelo usa √25 personas como resultado. ¿Cómo debe interpretarse?", "√25=5, un número natural.", ["Es irracional.", "No puede contar personas.", "Es negativo."], "La raíz es exacta."),
        ]
    if slug == "13-numeros-enteros-relaciones-de-orden-mayor-menor-e-igual":
        return [
            question("Santiago registra -2 °C y otra ciudad 5 °C. ¿Cuál está más fría?", "La de -2 °C.", ["La de 5 °C.", "Ambas igual.", "No se pueden comparar."], "-2<5."),
            question("Un buzo está a -18 m y otro a -11 m. ¿Quién está más profundo?", "El que está a -18 m.", ["El de -11 m.", "Ambos.", "El que está más cerca de cero."], "-18 es menor y representa mayor profundidad."),
            question("Una cuenta tiene saldo -$7.000 y otra -$12.000. ¿Cuál saldo es mayor?", "-$7.000", ["-$12.000", "Son iguales", "$12.000"], "-7000 está más cerca de cero."),
            question("Un ascensor pasa de piso -3 a piso 2. ¿La posición final es mayor?", "Sí, 2>-3.", ["No, -3>2.", "Son iguales.", "Solo se comparan valores absolutos."], "El piso 2 está sobre el nivel de referencia."),
            question("Una temperatura baja de 1 °C a -4 °C. ¿Cuál desigualdad describe el cambio?", "-4<1", ["-4>1", "-4=1", "4<1"], "La temperatura final es menor."),
            question("Tres deudas son -$5.000, -$20.000 y -$8.000. ¿Cuál es la menor?", "-$20.000", ["-$5.000", "-$8.000", "$20.000"], "En orden numérico, -20000 es el menor."),
            question("Un submarino A está a -90 m y B a -90 m. ¿Qué relación hay?", "A y B están a igual profundidad.", ["A está más profundo.", "B está más profundo.", "Son opuestos."], "Los enteros son iguales."),
            question("Una ruta tiene puntos -4, 0 y 7 respecto del origen. ¿Cuál está más a la derecha?", "7", ["-4", "0", "Todos igual"], "7 es el mayor."),
            question("La variación de dos acciones es -3 y -9. ¿Cuál tuvo mejor variación?", "-3", ["-9", "Ambas", "La de mayor valor absoluto"], "-3 es mayor que -9."),
            question("Una cámara está en piso -1 y debe bajar al -5. ¿Su número de piso aumenta o disminuye?", "Disminuye.", ["Aumenta.", "No cambia.", "Se vuelve positivo."], "Se mueve hacia enteros menores."),
        ]
    if slug == "14-valor-absoluto-relaciones-de-orden":
        return [
            nq("Un buzo está a -24 m. ¿A qué distancia está del nivel del mar?", 24, "La distancia es |-24|.", unit=" m"),
            nq("Una ciudad está a -6 °C y otra a 4 °C. ¿Qué diferencia de temperatura hay?", 10, "La distancia entre -6 y 4 es |-6-4|=10.", unit=" °C"),
            question("Dos ascensores están en pisos -5 y 5. ¿Cuál está más lejos del piso 0?", "Están a la misma distancia.", ["El de -5.", "El de 5.", "No se puede saber."], "Ambos tienen valor absoluto 5."),
            nq("Una cuenta varía de -$8.000 a $3.000. ¿Cuál es la distancia entre saldos?", 11000, "La distancia es |-8000-3000|.", unit=" pesos"),
            question("Un sensor acepta errores con |e|≤2. ¿Cuál error es aceptable?", "-2", ["3", "-4", "2,5"], "|-2|=2 cumple el límite."),
            nq("Un vehículo está 13 km al oeste del origen, representado por -13. ¿Qué distancia recorrió desde el origen?", 13, "La distancia es el valor absoluto.", unit=" km"),
            question("Dos temperaturas tienen valores absolutos 7 y 10. ¿Cuál está más alejada de 0 °C?", "La de valor absoluto 10.", ["La de 7.", "Ambas.", "Depende del signo."], "El valor absoluto compara distancias."),
            nq("Una persona camina desde -3 hasta 8 en una recta. ¿Cuántas unidades recorre?", 11, "La distancia es |8-(-3)|.", unit=" unidades"),
            question("Una tolerancia exige |x-20|<3. ¿Qué valor entero cumple?", "22", ["23", "16", "24"], "|22-20|=2<3."),
            nq("La altitud cambia de 12 m a -4 m. ¿Cuál es la magnitud del cambio?", 16, "La magnitud es |-4-12|.", unit=" m"),
        ]
    if slug in {"15-regla-de-signos-para-sumasrestas", "15a-ejercicios-de-sumas-y-restas-aplicacion-de-regla-de-los-signos"}:
        advanced = slug.startswith("15a")
        base = [
            ("Una cuenta parte con -$12.000 y recibe un depósito de $20.000. ¿Cuál es el saldo?", 8000, " pesos"),
            ("La temperatura es 4 °C y baja 11 °C. ¿Cuál queda?", -7, " °C"),
            ("Un buzo está a -18 m y asciende 7 m. ¿Cuál es su nueva posición?", -11, " m"),
            ("Un ascensor está en -2 y sube 6 pisos. ¿A qué piso llega?", 4, ""),
            ("Una acción cambia -5 puntos y luego +13. ¿Cuál es la variación acumulada?", 8, " puntos"),
            ("Un jugador gana 9 puntos y recibe una penalización de 14. ¿Cuál es su cambio neto?", -5, " puntos"),
            ("La temperatura pasa de -3 °C a 8 °C. ¿Cuánto aumentó?", 11, " °C"),
            ("Una deuda de $25.000 se reduce en $9.000. ¿Qué saldo entero representa la deuda restante?", -16000, " pesos"),
            ("Un submarino está a -40 m, baja 12 m y sube 20 m. ¿Dónde termina?", -32, " m"),
            ("Un marcador parte en 6, pierde 15 y gana 4. ¿Cuál es el valor final?", -5, ""),
        ]
        if advanced:
            base[0] = ("Una cuenta parte en -$35.000, recibe $18.000, paga $9.000 y recibe $14.000. ¿Cuál es el saldo?", -12000, " pesos")
            base[4] = ("Una acción cambia -8, +15, -11 y +6 puntos. ¿Cuál es la variación acumulada?", 2, " puntos")
        return [nq(text, ans, f"Se modelan aumentos como positivos y disminuciones como negativas; el resultado es {ans}{unit}.", unit=unit) for text, ans, unit in base]
    if slug == "16-regla-de-los-signos-en-multiplicaciondivision-ejemplos":
        return [
            nq("Un submarino desciende 6 m por minuto durante 7 minutos. ¿Cuál es la variación de altura?", -42, "Un descenso se representa con -6; (-6)·7=-42.", unit=" m"),
            nq("Una deuda aumenta $4.000 por día durante 5 días. ¿Qué variación representa?", -20000, "La deuda se representa como variación negativa.", unit=" pesos"),
            nq("Una temperatura baja 3 °C por hora durante 8 horas. ¿Cuál es la variación?", -24, "(-3)·8=-24.", unit=" °C"),
            nq("Un puntaje total de -36 se reparte en 6 penalizaciones iguales. ¿Cuánto vale cada una?", -6, "-36÷6=-6.", unit=" puntos"),
            nq("Un ascensor cambia -28 pisos en 7 recorridos iguales. ¿Qué cambio tiene cada recorrido?", -4, "-28÷7=-4.", unit=" pisos"),
            nq("Cuatro ajustes iguales generan una variación total de 52. ¿Cuánto vale cada ajuste?", 13, "52÷4=13.", unit=" unidades"),
            question("Tres factores negativos modelan tres inversiones de dirección. ¿Qué signo tiene el efecto total?", "Negativo", ["Positivo", "Cero", "No definido"], "Una cantidad impar de factores negativos produce signo negativo."),
            nq("Una pérdida de $2.500 se repite 12 veces. ¿Cuál es el cambio acumulado?", -30000, "(-2500)·12=-30000.", unit=" pesos"),
            nq("Un cambio total de -63 m ocurre a razón de -9 m por minuto. ¿Cuántos minutos dura?", 7, "-63÷(-9)=7.", unit=" minutos"),
            nq("Un juego aplica una penalización de -6 puntos a 5 jugadores. ¿Cuál es la variación total del equipo?", -30, "(-6)·5=-30.", unit=" puntos"),
        ]
    if slug == "17-prioridad-de-operaciones-sumarestamultiplicaciondivision-combinadas":
        return [
            nq("Una tienda tiene 20 cajas con 6 artículos y vende 17 artículos. ¿Cuántos quedan?", 103, "La expresión es 20·6-17.", unit=" artículos"),
            nq("Un juego entrega 8 bonos de 5 puntos y resta una penalización de 13. ¿Qué puntaje neto resulta?", 27, "8·5-13=27.", unit=" puntos"),
            nq("Tres grupos aportan 12 unidades cada uno y se reparten en 4 equipos. ¿Cuánto recibe cada equipo?", 9, "(3·12)÷4=9.", unit=" unidades"),
            nq("Una cuenta parte en $50.000, paga 4 cuotas de $8.000 y recibe $5.000. ¿Cuál es el saldo?", 23000, "50000-4·8000+5000=23000.", unit=" pesos"),
            nq("Se empacan 72 objetos en grupos de 6 y luego se agregan 3 grupos. ¿Cuántos grupos hay?", 15, "72÷6+3=15.", unit=" grupos"),
            nq("Un ascensor parte en -2, realiza 3 subidas de 4 pisos y baja 5. ¿Dónde termina?", 5, "-2+3·4-5=5.", unit=""),
            nq("Un depósito contiene 90 L, pierde 5 recipientes de 7 L y recibe 12 L. ¿Cuánto queda?", 67, "90-5·7+12=67.", unit=" L"),
            nq("Un torneo entrega 6 puntos por victoria en 5 partidos y descuenta 2 sanciones de 4. ¿Puntaje final?", 22, "5·6-2·4=22.", unit=" puntos"),
            nq("Cuatro personas pagan $3.000 cada una y dividen el total entre 2 compras. ¿Valor por compra?", 6000, "(4·3000)÷2=6000.", unit=" pesos"),
            nq("Una ruta tiene 3 tramos de 15 km y un desvío que resta 8 km al recorrido planificado. ¿Distancia?", 37, "3·15-8=37.", unit=" km"),
        ]
    if slug == "18-numeros-primos-multiplos-y-divisores":
        return [
            question("Hay 24 estudiantes y se quieren filas iguales. ¿Cuál tamaño de fila es posible?", "6 estudiantes", ["5 estudiantes", "7 estudiantes", "10 estudiantes"], "6 divide exactamente a 24."),
            question("Una alarma suena cada 8 minutos. ¿Cuál tiempo es un múltiplo de su intervalo?", "40 minutos", ["18 minutos", "34 minutos", "42 minutos"], "40=8·5."),
            question("Se empaquetan 37 objetos en grupos iguales mayores que uno. ¿Qué ocurre?", "Solo puede hacerse un grupo de 37; 37 es primo.", ["Se forman grupos de 4.", "Se forman grupos de 6.", "37 es divisible por 5."], "37 solo tiene divisores 1 y 37."),
            question("Un código exige un número primo entre 20 y 25. ¿Cuál sirve?", "23", ["21", "22", "24"], "23 solo es divisible por 1 y 23."),
            question("Se tienen 36 flores. ¿Cuál número de floreros permite reparto exacto?", "9", ["5", "7", "10"], "36÷9=4."),
            question("Una rueda completa ciclos de 12 pasos. ¿Cuál conteo corresponde a ciclos completos?", "60 pasos", ["50 pasos", "62 pasos", "70 pasos"], "60 es múltiplo de 12."),
            question("Un profesor quiere detectar rápido si 246 se reparte entre 3 grupos. ¿Qué concluye?", "Sí, porque 2+4+6=12 es múltiplo de 3.", ["No, porque termina en 6.", "Sí, porque tiene tres cifras.", "No, porque 246 es par."], "Se aplica el criterio de divisibilidad por 3."),
            question("Un tablero tiene 49 casillas y se organiza como cuadrado. ¿Qué factorización lo explica?", "7·7", ["5·9", "6·8", "2·24"], "49=7²."),
            question("Se desea formar equipos iguales con 31 personas. ¿Qué propiedad complica el reparto?", "31 es primo.", ["31 es par.", "31 es múltiplo de 6.", "31 tiene diez divisores."], "Solo admite grupos de 1 o 31."),
            question("Una caja contiene 90 piezas. ¿Qué factor primo aparece en su descomposición?", "5", ["7", "11", "13"], "90=2·3²·5."),
        ]
    if slug == "19a-ejercicios-minimo-comun-multiplo":
        scenarios = [
            ("Dos luces parpadean cada 6 y 8 segundos. ¿Cuándo coinciden?", (6, 8), " segundos"),
            ("Dos buses pasan cada 9 y 12 minutos. ¿Cuándo vuelven a coincidir?", (9, 12), " minutos"),
            ("Tres alarmas suenan cada 4, 6 y 10 minutos. ¿Primera coincidencia?", (4, 6, 10), " minutos"),
            ("Dos ruedas completan giros cada 14 y 21 segundos. ¿Cuándo se sincronizan?", (14, 21), " segundos"),
            ("Tres turnos se repiten cada 8, 12 y 18 días. ¿Cuándo coinciden?", (8, 12, 18), " días"),
            ("Dos medicamentos se toman cada 10 y 15 horas. ¿Cuándo vuelven a coincidir?", (10, 15), " horas"),
            ("Tres máquinas se revisan cada 15, 20 y 30 días. ¿Primera revisión conjunta?", (15, 20, 30), " días"),
            ("Dos señales se emiten cada 16 y 24 segundos. ¿Cuándo coinciden?", (16, 24), " segundos"),
            ("Dos atletas completan vueltas cada 18 y 27 minutos. ¿Cuándo pasan juntos por la meta?", (18, 27), " minutos"),
            ("Dos eventos ocurren cada 12 y 25 días. ¿Primera coincidencia?", (12, 25), " días"),
        ]
        return [nq(text, math.lcm(*values), f"Se calcula el MCM de {values}: {math.lcm(*values)}.", unit=unit) for text, values, unit in scenarios]
    return [
        nq("Dos campanas suenan cada 6 y 10 minutos. ¿Cuándo coinciden?", 30, "Se usa MCM(6,10)=30.", unit=" minutos"),
        nq("Se reparten 24 lápices y 36 cuadernos en el máximo número de kits iguales. ¿Cuántos kits?", 12, "Se usa MCD(24,36)=12.", unit=" kits"),
        nq("Dos buses pasan cada 8 y 12 minutos. ¿Cuándo vuelven a coincidir?", 24, "Se usa MCM(8,12)=24.", unit=" minutos"),
        nq("Cintas de 30 y 45 cm se cortan en trozos iguales lo más largos posible. ¿Longitud?", 15, "Se usa MCD(30,45)=15.", unit=" cm"),
        nq("Tres alarmas suenan cada 4, 6 y 9 minutos. ¿Primera coincidencia?", 36, "Se usa MCM(4,6,9)=36.", unit=" minutos"),
        nq("Se distribuyen 42 rojas y 56 azules en grupos idénticos máximos. ¿Número de grupos?", 14, "Se usa MCD(42,56)=14.", unit=" grupos"),
        nq("Dos ciclos de 15 y 20 días parten juntos. ¿Cuándo se repiten juntos?", 60, "Se usa MCM(15,20)=60.", unit=" días"),
        nq("Tablas de 48 y 60 cm se cortan sin sobrantes en piezas máximas. ¿Longitud?", 12, "Se usa MCD(48,60)=12.", unit=" cm"),
        question("Un problema pregunta por la primera coincidencia de periodos. ¿Qué herramienta corresponde?", "MCM", ["MCD", "Suma", "Resta"], "La primera coincidencia es un múltiplo común mínimo."),
        question("Un problema pregunta por el mayor tamaño de grupos iguales sin sobrantes. ¿Qué herramienta corresponde?", "MCD", ["MCM", "Producto", "Promedio"], "El tamaño debe dividir exactamente todas las cantidades."),
    ]


def build_questions(slug):
    levels = {
        1: concept_seeds(slug),
        2: procedure_seeds(slug),
        3: application_seeds(slug),
    }
    built = []
    for level, seeds in levels.items():
        if len(seeds) != 10:
            raise ValueError(f"{slug}: nivel {level} tiene {len(seeds)} semillas, se esperaban 10")
        for mode in MODES:
            for order, seed in enumerate(seeds, 1):
                item = expand_seed(seed, mode)
                item.update({"level": level, "mode": mode, "order": order})
                built.append(item)
    return built


def normalize(text):
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"\d+(?:[.,]\d+)?", "<n>", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def audit_bank(bank):
    errors = []
    exact_global = Counter()
    for slug, questions in bank.items():
        if len(questions) != 90:
            errors.append(f"{slug}: {len(questions)} preguntas")
        exact = Counter(" ".join(item["text"].lower().split()) for item in questions)
        repeated = [text for text, count in exact.items() if count > 1]
        if repeated:
            errors.append(f"{slug}: {len(repeated)} textos duplicados")
        for level in (1, 2, 3):
            for mode in MODES:
                count = sum(item["level"] == level and item["mode"] == mode for item in questions)
                if count != 10:
                    errors.append(f"{slug}: N{level}/{mode}={count}")
        for index, item in enumerate(questions, 1):
            choices = item["choices"]
            texts = [option["text"].strip() for option in choices]
            if len(choices) != 4 or len(set(texts)) != 4:
                errors.append(f"{slug}: pregunta {index} no tiene 4 alternativas únicas")
            if sum(bool(option["is_correct"]) for option in choices) != 1:
                errors.append(f"{slug}: pregunta {index} no tiene una correcta")
            if not item["explanation"].strip():
                errors.append(f"{slug}: pregunta {index} sin explicación")
            exact_global[" ".join(item["text"].lower().split())] += 1
    global_duplicates = [text for text, count in exact_global.items() if count > 1]
    if global_duplicates:
        errors.append(f"Banco global: {len(global_duplicates)} enunciados duplicados")
    if errors:
        raise RuntimeError("Auditoría fallida: " + "; ".join(errors[:20]))


def disambiguate_cross_resource_questions(bank):
    """Da contexto explícito solo a enunciados válidos compartidos por dos clases.

    Algunas definiciones base (por ejemplo, sumar enteros del mismo signo) son
    legítimamente comunes entre una clase teórica y una clase de ejercicios.
    La referencia al foco de la clase evita publicar copias textuales y aclara
    qué lectura o procedimiento se está evaluando en cada recurso.
    """
    occurrences = defaultdict(list)
    for slug, questions in bank.items():
        for item in questions:
            key = " ".join(item["text"].lower().split())
            occurrences[key].append((slug, item))
    for matches in occurrences.values():
        if len(matches) < 2:
            continue
        for slug, item in matches:
            focus = RESOURCE_DATA[slug]["focus"]
            item["text"] = f"En la clase centrada en {focus}, {item['text'][0].lower()}{item['text'][1:]}"


def youtube_description(resource, data):
    outcomes = "\n".join(f"• {item}" for item in data["outcomes"])
    description = (
        f"{data['summary']}\n\n"
        f"En esta clase aprenderás a:\n{outcomes}\n\n"
        "Este video forma parte de la ruta de Matemática de ProfeOnline y sirve para "
        "reforzamiento escolar, preparación de evaluaciones y estudio autónomo. Si buscas "
        "clases particulares online o acompañamiento con un profesor online, en "
        "https://www.profeonline.cl encontrarás recursos y práctica guiada.\n\n"
        f"Recurso y preguntas: https://www.profeonline.cl/recursos/{resource.slug}/\n\n"
        "#Matemática #NúmerosEnteros #ClasesOnline #ProfesorOnline"
    )
    return description.replace("<", "menor que").replace(">", "mayor que")


def web_metadata(resource, data):
    description = (
        f"{data['summary']} Incluye práctica en tres niveles para comprender, calcular y "
        "aplicar el contenido. Útil como apoyo de Matemática, clases particulares online "
        "y estudio con profesor online."
    )
    outcomes = "\n".join(f"- {item}" for item in data["outcomes"])
    content = (
        f"## Qué aprenderás\n\n{outcomes}\n\n"
        "## Cómo trabajar esta clase\n\n"
        "Mira el video completo, anota los procedimientos y luego responde las preguntas "
        "por nivel. La preparación permite reconocer ideas y practicar; la evaluación exige "
        "justificar decisiones y aplicar el contenido sin copiar mecánicamente un ejemplo.\n\n"
        "## Apoyo para tu estudio\n\n"
        "Este recurso puede usarse para reforzamiento de Matemática, preparación de pruebas "
        "y clases particulares online. En ProfeOnline puedes avanzar con práctica guiada y "
        "acompañamiento de un profesor online según tus necesidades."
    )
    return description, content


def fetch_transcripts(resources):
    transcripts = {}
    for resource in resources:
        text = fetch_transcript(resource.video_url or RESOURCE_DATA[resource.slug]["video_id"])
        if not text or len(text.split()) < 80:
            raise RuntimeError(f"No se obtuvo una transcripción suficiente para {resource.slug}")
        transcripts[resource.slug] = text
    return transcripts


def serialize_question(question_obj):
    return {
        "id": question_obj.id,
        "resource_slug": question_obj.resource.slug,
        "level": question_obj.level,
        "mode": question_obj.mode,
        "text": question_obj.text,
        "explanation": question_obj.explanation,
        "status": question_obj.status,
        "order": question_obj.order,
        "choices": [
            {
                "id": item.id,
                "text": item.text,
                "is_correct": item.is_correct,
                "order": item.order,
            }
            for item in question_obj.choices.all()
        ],
    }


def dependency_counts(queryset):
    return {
        "questions_with_answers": queryset.filter(attempt_answers__isnull=False).distinct().count(),
        "answer_rows": sum(item.attempt_answers.count() for item in queryset.prefetch_related("attempt_answers")),
        "questions_with_reports": queryset.filter(error_reports__isnull=False).distinct().count(),
        "report_rows": sum(item.error_reports.count() for item in queryset.prefetch_related("error_reports")),
    }


def write_backup(resources, transcripts, bank):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = BASE_DIR / "backups" / f"enteros_before_refresh_{timestamp}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    old_questions = (
        Question.objects.filter(resource__in=resources)
        .select_related("resource")
        .prefetch_related("choices")
        .order_by("resource_id", "level", "mode", "order", "id")
    )
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "database_name": settings.DATABASES["default"].get("NAME"),
        "resources": [
            {
                "id": resource.id,
                "slug": resource.slug,
                "title": resource.title,
                "description": resource.description,
                "content": resource.content,
                "transcript": resource.transcript,
                "video_url": resource.video_url,
            }
            for resource in resources
        ],
        "questions": [serialize_question(item) for item in old_questions],
        "new_transcript_lengths": {slug: len(text) for slug, text in transcripts.items()},
        "new_question_counts": {slug: len(items) for slug, items in bank.items()},
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    check = json.loads(path.read_text(encoding="utf-8"))
    if len(check["questions"]) != old_questions.count():
        raise RuntimeError("El respaldo no contiene todas las preguntas antiguas")
    return path


def write_youtube_payload(resources):
    path = UPLOADER_DIR / "editorial-packages" / "numeros-enteros-youtube.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = []
    for resource in resources:
        data = RESOURCE_DATA[resource.slug]
        payload.append(
            {
                "videoId": data["video_id"],
                "resourceSlug": resource.slug,
                "description": youtube_description(resource, data),
            }
        )
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def apply_changes(resources, transcripts, bank):
    resource_ids = [item.id for item in resources]
    old_questions = Question.objects.filter(resource_id__in=resource_ids)
    dependencies = dependency_counts(old_questions)
    if any(dependencies.values()):
        raise RuntimeError(f"Las preguntas antiguas adquirieron dependencias: {dependencies}")

    with transaction.atomic():
        locked_resources = list(
            Resource.objects.select_for_update().filter(id__in=resource_ids).order_by("id")
        )
        locked_questions = Question.objects.select_for_update().filter(resource_id__in=resource_ids)
        locked_dependencies = dependency_counts(locked_questions)
        if any(locked_dependencies.values()):
            raise RuntimeError(f"Aparecieron dependencias durante la operación: {locked_dependencies}")
        locked_questions.delete()

        for resource in locked_resources:
            data = RESOURCE_DATA[resource.slug]
            description, content = web_metadata(resource, data)
            resource.description = description
            resource.content = content
            resource.transcript = transcripts[resource.slug]
            resource.save(update_fields=["description", "content", "transcript"])

            for level in (1, 2, 3):
                for mode in MODES:
                    batch = [
                        item for item in bank[resource.slug]
                        if item["level"] == level and item["mode"] == mode
                    ]
                    _save_questions(resource, level, mode, batch, status="publicada")

            config, _ = ResourceQuizConfig.objects.get_or_create(resource=resource)
            config.counts = QUIZ_COUNTS
            config.autopublish = True
            config.save(update_fields=["counts", "autopublish"])


def verify(resources):
    failures = []
    for resource in resources:
        published = resource.questions.filter(status="publicada")
        if published.count() != 90:
            failures.append(f"{resource.slug}: publicadas={published.count()}")
        if len((resource.transcript or "").split()) < 80:
            failures.append(f"{resource.slug}: transcript insuficiente")
        for level in (1, 2, 3):
            for mode in MODES:
                count = published.filter(level=level, mode=mode).count()
                if count != 10:
                    failures.append(f"{resource.slug}: N{level}/{mode}={count}")
        for item in published.prefetch_related("choices"):
            options = list(item.choices.all())
            if len(options) != 4 or sum(option.is_correct for option in options) != 1:
                failures.append(f"{resource.slug}: pregunta {item.id} inválida")
    if Choice.objects.filter(question__isnull=True).exists():
        failures.append("Hay alternativas huérfanas")
    if failures:
        raise RuntimeError("Verificación fallida: " + "; ".join(failures[:20]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm")
    parser.add_argument("--transcripts-json")
    args = parser.parse_args()

    resources = list(Resource.objects.filter(slug__in=RESOURCE_DATA).order_by("id"))
    if len(resources) != len(RESOURCE_DATA):
        found = {item.slug for item in resources}
        raise RuntimeError(f"Faltan recursos: {sorted(set(RESOURCE_DATA)-found)}")

    bank = {slug: build_questions(slug) for slug in RESOURCE_DATA}
    disambiguate_cross_resource_questions(bank)
    audit_bank(bank)
    if args.transcripts_json:
        transcripts = json.loads(Path(args.transcripts_json).read_text(encoding="utf-8"))
    else:
        transcripts = fetch_transcripts(resources)

    current_questions = Question.objects.filter(resource__in=resources)
    dependencies = dependency_counts(current_questions)
    print(f"RECURSOS={len(resources)}")
    print(f"PREGUNTAS_ANTES={current_questions.count()}")
    print(f"PREGUNTAS_NUEVAS={sum(map(len, bank.values()))}")
    print(f"TRANSCRIPTS_OK={len(transcripts)}")
    print(f"DEPENDENCIAS={dependencies}")
    print("AUDITORIA_BANCO=OK")

    if not args.apply:
        print("DRY_RUN_OK: no se modificó producción.")
        return
    if settings.DEBUG:
        raise RuntimeError("Se rechaza la operación con DEBUG=True")
    if args.confirm != CONFIRMATION:
        raise RuntimeError(f"Use --confirm {CONFIRMATION}")
    if any(dependencies.values()):
        raise RuntimeError(f"No es seguro borrar el banco anterior: {dependencies}")

    backup = write_backup(resources, transcripts, bank)
    apply_changes(resources, transcripts, bank)
    resources = list(Resource.objects.filter(slug__in=RESOURCE_DATA).order_by("id"))
    verify(resources)
    youtube_payload = write_youtube_payload(resources)
    print(f"BACKUP={backup}")
    print(f"YOUTUBE_PAYLOAD={youtube_payload}")
    print("APPLY_OK")


if __name__ == "__main__":
    main()

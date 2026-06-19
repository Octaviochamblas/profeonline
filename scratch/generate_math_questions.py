import os
import sys
import django
import random
import math

# Asegurar codificación UTF-8
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.db import transaction

from apps.content.models import Question, Resource
from apps.content.services.ai_generation_service import _save_questions

# Definir generadores dinámicos para cada recurso (35 preguntas cada uno)

def gen_conjuntos_numericos():
    questions = []
    # N1 - 10 conceptuales
    questions.append({
        "text": "¿Cuál de las siguientes afirmaciones describe mejor al conjunto de los números enteros (ℤ)?",
        "explanation": "El conjunto de los números enteros (ℤ) incluye los números naturales (enteros positivos), el cero y los enteros negativos. Por lo tanto, incluye positivos, negativos y el cero.",
        "choices": [
            {"text": "Está formado por los enteros positivos, los enteros negativos y el cero.", "is_correct": True},
            {"text": "Solo contiene los números positivos que sirven para contar y el cero.", "is_correct": False},
            {"text": "Incluye a todas las fracciones y números decimales infinitos.", "is_correct": False},
            {"text": "Está compuesto únicamente por números impares menores a 100.", "is_correct": False}
        ]
    })
    questions.append({
        "text": "¿Cuál es la principal diferencia entre el conjunto de los números naturales (ℕ) y los números enteros (ℤ)?",
        "explanation": "Los números naturales (ℕ) solo contemplan cantidades positivas (y a veces el cero), mientras que los enteros (ℤ) amplían este conjunto agregando los números negativos para representar deudas, temperaturas bajo cero, etc.",
        "choices": [
            {"text": "Los enteros contienen números negativos, a diferencia de los naturales.", "is_correct": True},
            {"text": "Los naturales contienen números negativos y los enteros no.", "is_correct": False},
            {"text": "Los naturales incluyen fracciones y los enteros solo números con coma.", "is_correct": False},
            {"text": "No hay ninguna diferencia; son exactamente el mismo conjunto.", "is_correct": False}
        ]
    })
    for i in range(8):
        num = random.randint(10, 100)
        questions.append({
            "text": f"¿Cómo se clasifica el número natural positivo {num} en el conjunto de los enteros?",
            "explanation": f"Todo número natural ({num}) es también un número entero positivo. Por ende, pertenece a ambos conjuntos.",
            "choices": [
                {"text": "Pertenece tanto a los naturales (ℕ) como a los enteros (ℤ).", "is_correct": True},
                {"text": "Solo pertenece a los naturales (ℕ).", "is_correct": False},
                {"text": "Solo pertenece a los enteros (ℤ).", "is_correct": False},
                {"text": "Es un entero negativo.", "is_correct": False}
            ]
        })
    # N2 - 15 clasificación mecánica
    for i in range(15):
        num = random.randint(-100, -1)
        questions.append({
            "text": f"¿A qué conjuntos numéricos pertenece el número {num}?",
            "explanation": f"El número {num} es un número entero negativo. Por lo tanto, pertenece al conjunto de los números enteros (ℤ), pero NO pertenece al conjunto de los números naturales (ℕ) que solo tiene positivos.",
            "choices": [
                {"text": f"Pertenece a los enteros (ℤ) pero no a los naturales (ℕ).", "is_correct": True},
                {"text": f"Pertenece a los naturales (ℕ) pero no a los enteros (ℤ).", "is_correct": False},
                {"text": "Pertenece a ambos conjuntos (ℕ y ℤ).", "is_correct": False},
                {"text": "No pertenece a ninguno de los dos conjuntos.", "is_correct": False}
            ]
        })
    # N3 - 10 problemas
    contexts = [
        ("un termómetro marca una temperatura de 4 grados bajo cero", -4),
        ("un submarino navega a una profundidad de 150 metros bajo el nivel del mar", -150),
        ("un cliente de un banco tiene una deuda de $12.000 en su cuenta", -12000),
        ("un ascensor se encuentra en el tercer piso del subterráneo (-3)", -3),
        ("la temperatura en la Antártica es de 25 grados bajo cero", -25),
        ("un buzo desciende a una profundidad de 40 metros bajo el mar", -40),
        ("una persona debe 5.000 pesos en la tienda de la esquina", -5000),
        ("un estacionamiento subterráneo está a 2 pisos de profundidad (-2)", -2),
        ("un pozo de agua tiene una profundidad de 15 metros bajo tierra", -15),
        ("una cuenta corriente registra un saldo en contra de $8.500", -8500)
    ]
    for desc, val in contexts:
        questions.append({
            "text": f"Si representamos la siguiente situación con un número entero: '{desc}', ¿cuál es el número entero correspondiente?",
            "explanation": f"Las situaciones que indican 'bajo cero', 'bajo el nivel del mar', 'subterráneo' o 'deuda/saldo en contra' se representan matemáticamente con números enteros negativos. En este caso corresponde a {val}.",
            "choices": [
                {"text": f"{val}", "is_correct": True},
                {"text": f"{abs(val)}", "is_correct": False},
                {"text": "0", "is_correct": False},
                {"text": f"{val * 2}", "is_correct": False}
            ]
        })
    return questions

def gen_relaciones_orden():
    questions = []
    # N1 - 10 conceptuales
    questions.append({
        "text": "En la recta numérica, ¿cómo se determina si un número entero es mayor que otro?",
        "explanation": "En la recta numérica, el número que se ubica más a la derecha siempre es el mayor, y el que está más a la izquierda es el menor.",
        "choices": [
            {"text": "El número que está más a la derecha siempre es el mayor.", "is_correct": True},
            {"text": "El número que tiene más cifras siempre es el menor.", "is_correct": False},
            {"text": "El número que está más cerca del cero siempre es el mayor.", "is_correct": False},
            {"text": "Los números negativos siempre son mayores que los positivos.", "is_correct": False}
        ]
    })
    for i in range(9):
        questions.append({
            "text": "Si comparamos un número entero positivo cualquiera con un número entero negativo cualquiera, ¿cuál es siempre el mayor?",
            "explanation": "Cualquier número positivo es siempre mayor que cualquier número negativo, ya que los positivos están ubicados a la derecha del cero y los negativos a la izquierda.",
            "choices": [
                {"text": "El número positivo siempre es mayor.", "is_correct": True},
                {"text": "El número negativo siempre es mayor.", "is_correct": False},
                {"text": "El número que esté más lejos del cero siempre es mayor.", "is_correct": False},
                {"text": "Son de igual valor.", "is_correct": False}
            ]
        })
    # N2 - 15 comparaciones
    for i in range(15):
        n1 = random.randint(-100, -2)
        n2 = random.randint(n1 + 1, 30)
        questions.append({
            "text": f"¿Cuál de las siguientes relaciones de comparación es correcta para los números {n1} y {n2}?",
            "explanation": f"En la recta numérica, {n2} está a la derecha de {n1}. Por tanto, {n2} > {n1} (o {n1} < {n2}).",
            "choices": [
                {"text": f"{n1} < {n2}", "is_correct": True},
                {"text": f"{n1} > {n2}", "is_correct": False},
                {"text": f"{n1} = {n2}", "is_correct": False},
                {"text": "Ninguna relación es correcta", "is_correct": False}
            ]
        })
    # N3 - 10 problemas
    for i in range(10):
        temp1 = random.randint(-25, -2)
        temp2 = random.randint(temp1 + 1, 15)
        questions.append({
            "text": f"Una ciudad A registra una temperatura de {temp1}°C y una ciudad B registra {temp2}°C. ¿Cuál ciudad tiene la temperatura más fría y por qué?",
            "explanation": f"La temperatura más fría corresponde al número menor en la escala. Como {temp1} es menor que {temp2} ({temp1} < {temp2}), la ciudad A es la más fría.",
            "choices": [
                {"text": f"La ciudad A es la más fría, porque {temp1} es menor que {temp2}.", "is_correct": True},
                {"text": f"La ciudad B es la más fría, porque {temp2} es menor que {temp1}.", "is_correct": False},
                {"text": "Ambas ciudades tienen el mismo nivel de frío.", "is_correct": False},
                {"text": "La ciudad A es la más cálida, por estar más lejos del cero.", "is_correct": False}
            ]
        })
    return questions

def gen_valor_absoluto():
    questions = []
    # N1 - 10 conceptuales
    questions.append({
        "text": "¿Qué representa el valor absoluto de un número entero?",
        "explanation": "El valor absoluto de un número representa su distancia al cero en la recta numérica. Dado que las distancias siempre son positivas o cero, el valor absoluto nunca puede ser negativo.",
        "choices": [
            {"text": "La distancia del número al cero en la recta numérica.", "is_correct": True},
            {"text": "El número con el signo contrario.", "is_correct": False},
            {"text": "La suma del número consigo mismo.", "is_correct": False},
            {"text": "La distancia entre el número y su opuesto.", "is_correct": False}
        ]
    })
    questions.append({
        "text": "¿Cuál es el valor absoluto de un número negativo?",
        "explanation": "El valor absoluto de cualquier número distinto de cero es siempre positivo, ya que representa una distancia.",
        "choices": [
            {"text": "Es el mismo número pero con signo positivo.", "is_correct": True},
            {"text": "Es el mismo número pero con signo negativo.", "is_correct": False},
            {"text": "Siempre es cero.", "is_correct": False},
            {"text": "Es la mitad del número original.", "is_correct": False}
        ]
    })
    for i in range(8):
        questions.append({
            "text": "¿Cuál es el valor absoluto del número cero |0|?",
            "explanation": "La distancia del número cero al cero en la recta numérica es exactamente cero unidades. Por lo tanto, |0| = 0.",
            "choices": [
                {"text": "0", "is_correct": True},
                {"text": "1", "is_correct": False},
                {"text": "-0", "is_correct": False},
                {"text": "No está definido", "is_correct": False}
            ]
        })
    # N2 - 15 ejercicios
    for i in range(15):
        val = random.randint(-150, -5)
        questions.append({
            "text": f"¿Cuál es el valor de |{val}|?",
            "explanation": f"El valor absoluto de {val}, escrito como |{val}|, es la distancia de {val} al cero en la recta numérica, lo cual es {abs(val)} unidades.",
            "choices": [
                {"text": f"{abs(val)}", "is_correct": True},
                {"text": f"{val}", "is_correct": False},
                {"text": "0", "is_correct": False},
                {"text": f"{-val - 10}", "is_correct": False}
            ]
        })
    # N3 - 10 problemas
    questions.append({
        "text": "Un buzo está a -15 metros bajo el nivel del mar y un ave vuela a 15 metros de altura sobre el nivel del mar. ¿Quién está a mayor distancia del nivel del mar (cero)?",
        "explanation": "El buzo está a |-15| = 15 metros del nivel del mar. El ave está a |15| = 15 metros del nivel del mar. Por lo tanto, ambos están exactamente a la misma distancia (15 metros) del cero.",
        "choices": [
            {"text": "Ambos están a la misma distancia del nivel del mar.", "is_correct": True},
            {"text": "El buzo está más lejos porque -15 es menor que 15.", "is_correct": False},
            {"text": "El ave está más lejos porque 15 es un número positivo.", "is_correct": False},
            {"text": "El buzo está más cerca porque está bajo el agua.", "is_correct": False}
        ]
    })
    depths = [
        (-25, 5), (-35, 10), (-18, 3), (-40, 8), (-15, 4), (-30, 6), (-50, 12), (-22, 5), (-14, 2)
    ]
    for d1, d2 in depths:
        questions.append({
            "text": f"Un pez se encuentra a {d1} metros de profundidad y un cangrejo a {d1 + d2} metros de profundidad. ¿Cuál de los dos está más cerca del nivel del mar (cero) y por qué?",
            "explanation": f"El pez está a |{d1}| = {abs(d1)} metros del cero. El cangrejo está a |{d1 + d2}| = {abs(d1 + d2)} metros del cero. Como {abs(d1 + d2)} es menor que {abs(d1)}, el cangrejo está más cerca del nivel del mar.",
            "choices": [
                {"text": f"El cangrejo, porque su valor absoluto ({abs(d1 + d2)}) es menor que el del pez ({abs(d1)}).", "is_correct": True},
                {"text": f"El pez, porque su valor absoluto ({abs(d1)}) es mayor que el del cangrejo ({abs(d1 + d2)}).", "is_correct": False},
                {"text": "Ambos están a la misma distancia.", "is_correct": False},
                {"text": f"El pez, porque está a mayor profundidad.", "is_correct": False}
            ]
        })
    return questions

def gen_sumas_restas():
    questions = []
    # N1 - 10 conceptuales
    questions.append({
        "text": "Al sumar dos números enteros con el mismo signo, ¿cuál es la regla a seguir?",
        "explanation": "La regla para sumar números de igual signo es: se suman sus valores absolutos y se conserva el signo común.",
        "choices": [
            {"text": "Se suman sus valores absolutos y se mantiene el signo común.", "is_correct": True},
            {"text": "Se restan sus valores absolutos y se pone el signo del mayor.", "is_correct": False},
            {"text": "El resultado siempre es un número positivo.", "is_correct": False},
            {"text": "El resultado siempre es cero.", "is_correct": False}
        ]
    })
    questions.append({
        "text": "Al sumar dos números enteros con signos diferentes (uno positivo y uno negativo), ¿cuál es la regla?",
        "explanation": "La regla para sumar enteros de distinto signo es: se restan sus valores absolutos (el mayor menos el menor) y se conserva el signo del número con mayor valor absoluto.",
        "choices": [
            {"text": "Se restan sus valores absolutos y se conserva el signo del que tiene mayor valor absoluto.", "is_correct": True},
            {"text": "Se suman sus valores absolutos y se coloca signo positivo.", "is_correct": False},
            {"text": "Se restan sus valores absolutos y el signo del resultado siempre es negativo.", "is_correct": False},
            {"text": "Se multiplican sus signos y se suman los números.", "is_correct": False}
        ]
    })
    for i in range(8):
        questions.append({
            "text": "Si restas un número entero negativo a otro número entero, ¿qué transformación equivale a esta resta?",
            "explanation": "Restar un número negativo equivale a sumar su valor opuesto positivo (ej. a - (-b) = a + b). Por lo tanto, equivale a sumarlo.",
            "choices": [
                {"text": "Equivale a sumar el valor positivo de dicho número.", "is_correct": True},
                {"text": "Equivale a restarlo dos veces.", "is_correct": False},
                {"text": "Equivale a multiplicar el número por cero.", "is_correct": False},
                {"text": "Equivale a dividir el número por -1.", "is_correct": False}
            ]
        })
    # N2 - 15 ejercicios
    for i in range(15):
        n1 = random.randint(-50, 10)
        n2 = random.randint(-40, 40)
        ans = n1 + n2
        questions.append({
            "text": f"Resuelve la siguiente operación: {n1} + ({n2})",
            "explanation": f"Para resolver {n1} + ({n2}): si tienen igual signo se suman y conserva el signo; si tienen distinto signo se restan y conserva el signo del mayor absoluto. El resultado es {ans}.",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{ans + 3}", "is_correct": False},
                {"text": f"{ans - 5}", "is_correct": False},
                {"text": f"{ans + 8}", "is_correct": False}
            ]
        })
    # N3 - 10 problemas
    for i in range(10):
        saldo = random.randint(-30, -2) * 1000
        deposito = random.randint(10, 45) * 1000
        ans = saldo + deposito
        questions.append({
            "text": f"Una cuenta bancaria tiene un saldo de {saldo} pesos (en contra). Si el dueño realiza un depósito de {deposito} pesos, ¿cuál es el nuevo saldo de la cuenta?",
            "explanation": f"El saldo inicial es de {saldo} (negativo). Al depositar {deposito} (positivo), calculamos la suma: {saldo} + {deposito} = {ans} pesos.",
            "choices": [
                {"text": f"{ans} pesos", "is_correct": True},
                {"text": f"{saldo - deposito} pesos", "is_correct": False},
                {"text": f"{deposito} pesos", "is_correct": False},
                {"text": f"{ans - 2000} pesos", "is_correct": False}
            ]
        })
    return questions

def gen_mult_div():
    questions = []
    # N1 - 10 conceptuales
    questions.append({
        "text": "¿Cuál es el signo del resultado al multiplicar dos números enteros con signos diferentes (un positivo por un negativo)?",
        "explanation": "La ley de signos para la multiplicación establece que más por menos es menos (+ · - = -). Por lo tanto, el resultado es siempre negativo.",
        "choices": [
            {"text": "Negativo", "is_correct": True},
            {"text": "Positivo", "is_correct": False},
            {"text": "Depende de cuál número sea mayor en valor absoluto.", "is_correct": False},
            {"text": "Siempre es cero.", "is_correct": False}
        ]
    })
    questions.append({
        "text": "¿Cuál es el signo del resultado al dividir dos números enteros negativos?",
        "explanation": "La ley de signos para la división establece que menos dividido por menos es más (- / - = +). Por lo tanto, el resultado es siempre positivo.",
        "choices": [
            {"text": "Positivo", "is_correct": True},
            {"text": "Negativo", "is_correct": False},
            {"text": "Depende de la distancia al cero.", "is_correct": False},
            {"text": "Es indeterminado.", "is_correct": False}
        ]
    })
    for i in range(8):
        questions.append({
            "text": "¿Qué resultado se obtiene al multiplicar cualquier número entero por cero (0)?",
            "explanation": "El número cero es el elemento absorbente de la multiplicación. Cualquier número entero multiplicado por cero da como resultado cero.",
            "choices": [
                {"text": "Cero (0)", "is_correct": True},
                {"text": "El mismo número entero.", "is_correct": False},
                {"text": "El opuesto del número entero.", "is_correct": False},
                {"text": "Uno (1)", "is_correct": False}
            ]
        })
    # N2 - 15 ejercicios
    for i in range(15):
        n1 = random.choice([-15, -12, -9, -8, -6, -5, 4, 7, 10])
        n2 = random.choice([-8, -6, -4, -3, 2, 5, 8, 11])
        ans = n1 * n2
        questions.append({
            "text": f"Resuelve la siguiente multiplicación: {n1} · ({n2})",
            "explanation": f"Multiplicamos los valores absolutos: {abs(n1)} · {abs(n2)} = {abs(ans)}. Luego aplicamos la ley de signos: si los signos son iguales el resultado es positivo; si son diferentes es negativo. Por tanto, el resultado es {ans}.",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{-ans}", "is_correct": False},
                {"text": f"{ans + n1}", "is_correct": False},
                {"text": f"{abs(ans) + 2}", "is_correct": False}
            ]
        })
    # N3 - 10 problemas
    for i in range(10):
        desc = random.randint(2, 10)
        tiempo = random.randint(3, 12)
        total = -desc * tiempo
        questions.append({
            "text": f"Un globo aerostático desciende {desc} metros por cada minuto que transcurre. Si mantiene este ritmo constante durante {tiempo} minutos, ¿cuál es la variación total en su altura?",
            "explanation": f"El descenso se representa como un número negativo: -{desc} metros por minuto. Multiplicado por los {tiempo} minutos de trayecto: -{desc} · {tiempo} = {total} metros de variación (es decir, descendió {abs(total)} metros en total).",
            "choices": [
                {"text": f"{total} metros", "is_correct": True},
                {"text": f"{abs(total)} metros", "is_correct": False},
                {"text": f"-{desc + tiempo} metros", "is_correct": False},
                {"text": "0 metros", "is_correct": False}
            ]
        })
    return questions

def gen_prioridad():
    questions = []
    # N1 - 10 conceptuales
    questions.append({
        "text": "Al resolver operaciones combinadas sin paréntesis, ¿cuál es el orden correcto de prioridad?",
        "explanation": "El orden estándar de prioridad de operaciones (conocido en Chile como PAPOMUDAS) dicta que primero se resuelven Paréntesis, luego Potencias, después Multiplicaciones y Divisiones de izquierda a derecha, y finalmente Sumas y Restas de izquierda a derecha.",
        "choices": [
            {"text": "Primero multiplicaciones y divisiones, luego sumas y restas.", "is_correct": True},
            {"text": "Primero sumas y restas, luego multiplicaciones y divisiones.", "is_correct": False},
            {"text": "Siempre de izquierda a derecha sin importar el tipo de operación.", "is_correct": False},
            {"text": "Primero las sumas y divisiones, luego restas y multiplicaciones.", "is_correct": False}
        ]
    })
    for i in range(9):
        questions.append({
            "text": "En la prioridad de operaciones combinadas, ¿qué símbolo tiene la mayor prioridad absoluta de resolución?",
            "explanation": "Los paréntesis son los elementos que rompen la prioridad natural y deben resolverse siempre primero, desde los más internos hacia los externos.",
            "choices": [
                {"text": "Los Paréntesis", "is_correct": True},
                {"text": "La Multiplicación", "is_correct": False},
                {"text": "La Suma", "is_correct": False},
                {"text": "La División", "is_correct": False}
            ]
        })
    # N2 - 15 ejercicios
    for i in range(15):
        n1 = random.randint(5, 20)
        n2 = random.randint(2, 9)
        n3 = random.randint(-8, -2)
        ans = n1 + n2 * n3
        questions.append({
            "text": f"Calcula el resultado de la siguiente expresión: {n1} + {n2} · ({n3})",
            "explanation": f"Primero resolvemos la multiplicación por prioridad: {n2} · ({n3}) = {n2 * n3}. Luego sumamos el resultado: {n1} + ({n2 * n3}) = {ans}.",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{(n1 + n2) * n3}", "is_correct": False},
                {"text": f"{ans + 5}", "is_correct": False},
                {"text": f"{ans - 5}", "is_correct": False}
            ]
        })
    # N3 - 10 problemas
    for i in range(10):
        base = random.randint(10, 50)
        cajas = random.randint(3, 8)
        cant = random.randint(4, 12)
        perdidas = random.randint(2, 8)
        ans = base + cajas * cant - perdidas
        questions.append({
            "text": f"Un almacén tiene {base} manzanas. Recibe {cajas} cajas con {cant} manzanas cada una. Si al final del día se botan {perdidas} manzanas que estaban en mal estado, ¿cuántas manzanas quedan?",
            "explanation": f"Escribimos la expresión matemática: {base} + {cajas} · {cant} - {perdidas}. Resolvemos la multiplicación primero: {cajas} · {cant} = {cajas * cant}. Luego sumamos y restamos: {base} + {cajas * cant} - {perdidas} = {ans} manzanas.",
            "choices": [
                {"text": f"{ans} manzanas", "is_correct": True},
                {"text": f"{ans + 10} manzanas", "is_correct": False},
                {"text": f"{ans - 10} manzanas", "is_correct": False},
                {"text": f"{ans + 20} manzanas", "is_correct": False}
            ]
        })
    return questions

def gen_primos():
    questions = []
    # N1 - 10 conceptuales
    questions.append({
        "text": "¿Qué define a un número primo?",
        "explanation": "Un número primo es un número entero mayor que 1 que tiene exactamente dos divisores distintos: el 1 y él mismo.",
        "choices": [
            {"text": "Es un número mayor que 1 que solo se puede dividir por 1 y por sí mismo.", "is_correct": True},
            {"text": "Es cualquier número impar.", "is_correct": False},
            {"text": "Es un número que termina en 1, 3, 7 o 9.", "is_correct": False},
            {"text": "Es cualquier número que tenga más de dos divisores.", "is_correct": False}
        ]
    })
    questions.append({
        "text": "¿Cuál es el único número par que también es un número primo?",
        "explanation": "El número 2 es el único número primo par, ya que sus únicos divisores son el 1 y el 2. Todos los demás números pares mayores son compuestos (divisibles por 2).",
        "choices": [
            {"text": "El número 2", "is_correct": True},
            {"text": "El número 4", "is_correct": False},
            {"text": "El número 0", "is_correct": False},
            {"text": "No existen números primos pares.", "is_correct": False}
        ]
    })
    for i in range(8):
        questions.append({
            "text": "¿Qué es un número compuesto?",
            "explanation": "Un número compuesto es un número entero mayor que 1 que tiene más de dos divisores distintos (es decir, no es primo).",
            "choices": [
                {"text": "Un número entero mayor que 1 que tiene más de dos divisores.", "is_correct": True},
                {"text": "Un número que se compone por la suma de dos primos.", "is_correct": False},
                {"text": "Cualquier número terminado en cero.", "is_correct": False},
                {"text": "Un número negativo con decimales.", "is_correct": False}
            ]
        })
    # N2 - 15 ejercicios
    nums = [9, 12, 15, 18, 20, 21, 24, 25, 27, 28, 30, 32, 35, 36, 40]
    for num in nums:
        divs = [d for d in range(1, num + 1) if num % d == 0]
        questions.append({
            "text": f"¿Cuáles son todos los divisores del número {num}?",
            "explanation": f"Los divisores de {num} son los números enteros que lo dividen de forma exacta. Para {num}, estos son: {', '.join(map(str, divs))}.",
            "choices": [
                {"text": f"{', '.join(map(str, divs))}", "is_correct": True},
                {"text": f"1, {num}", "is_correct": False},
                {"text": f"{', '.join(map(str, divs[:-1]))}", "is_correct": False},
                {"text": "Ninguna de las anteriores", "is_correct": False}
            ]
        })
    # N3 - 10 problemas
    for i in range(10):
        alumnos = random.choice([12, 18, 24, 30, 36, 40, 48])
        options = [d for d in range(2, alumnos) if alumnos % d == 0]
        opt = random.choice(options)
        questions.append({
            "text": f"Un profesor quiere organizar a sus {alumnos} alumnos en grupos de igual tamaño. ¿Cuál de los siguientes tamaños de grupo es posible sin que sobre ningún alumno?",
            "explanation": f"Para organizar a los {alumnos} alumnos de forma exacta, el tamaño del grupo debe ser un divisor de {alumnos}. Entre las opciones, {opt} es divisor de {alumnos}.",
            "choices": [
                {"text": f"Grupos de {opt} alumnos.", "is_correct": True},
                {"text": f"Grupos de {opt + 1} alumnos.", "is_correct": False},
                {"text": f"Grupos de {alumnos - 1} alumnos.", "is_correct": False},
                {"text": "No es posible organizarlos en grupos iguales.", "is_correct": False}
            ]
        })
    return questions

def gen_mcm_mcd():
    questions = []
    # N1 - 10 conceptuales
    questions.append({
        "text": "¿Qué representa el Mínimo Común Múltiplo (MCM) de dos números?",
        "explanation": "El Mínimo Común Múltiplo (MCM) de dos o más números es el número más pequeño (distinto de cero) que es múltiplo común de todos ellos.",
        "choices": [
            {"text": "El múltiplo más pequeño que tienen en común ambos números.", "is_correct": True},
            {"text": "El divisor más grande que tienen en común ambos números.", "is_correct": False},
            {"text": "La suma de los múltiplos de ambos números.", "is_correct": False},
            {"text": "El producto de ambos números dividido por dos.", "is_correct": False}
        ]
    })
    questions.append({
        "text": "¿Qué representa el Máximo Común Divisor (MCD) de dos números?",
        "explanation": "El Máximo Común Divisor (MCD) es el número entero más grande que divide de forma exacta a todos los números del grupo.",
        "choices": [
            {"text": "El divisor más grande que tienen en común ambos números.", "is_correct": True},
            {"text": "El múltiplo más pequeño que tienen en común ambos números.", "is_correct": False},
            {"text": "El número primo más pequeño de los divisores comunes.", "is_correct": False},
            {"text": "La diferencia entre los divisores comunes.", "is_correct": False}
        ]
    })
    for i in range(8):
        questions.append({
            "text": "Si dos números son primos entre sí (no tienen divisores comunes excepto el 1), ¿cuál es su Máximo Común Divisor (MCD)?",
            "explanation": "Por definición, si dos números son primos entre sí, el único divisor que comparten es el número 1. Por ende, su MCD es 1.",
            "choices": [
                {"text": "El número 1", "is_correct": True},
                {"text": "El producto de ambos números.", "is_correct": False},
                {"text": "El número cero (0).", "is_correct": False},
                {"text": "No existe divisor común.", "is_correct": False}
            ]
        })
    # N2 - 15 ejercicios
    pairs = [
        (4, 3, 12), (6, 5, 30), (8, 6, 24), (10, 4, 20), (6, 9, 18), (8, 5, 40), (12, 8, 24),
        (3, 7, 21), (5, 9, 45), (10, 15, 30), (6, 8, 24), (12, 15, 60), (4, 10, 20), (9, 12, 36), (8, 12, 24)
    ]
    for a, b, mcm in pairs:
        mcd = math.gcd(a, b)
        questions.append({
            "text": f"Calcula el Mínimo Común Múltiplo (MCM) de los números {a} y {b}.",
            "explanation": f"Los múltiplos de {a} son: {a}, {a*2}, {a*3}... y los de {b} son: {b}, {b*2}, {b*3}... El primer múltiplo común más pequeño que encontramos es {mcm}.",
            "choices": [
                {"text": f"{mcm}", "is_correct": True},
                {"text": f"{mcd}", "is_correct": False},
                {"text": f"{mcm + a + b}", "is_correct": False},
                {"text": f"{mcm + a}", "is_correct": False}
            ]
        })
    # N3 - 10 problemas
    bus_problems = [
        (4, 3, 12), (6, 5, 30), (8, 3, 24), (5, 4, 20), (6, 4, 12), (8, 5, 40),
        (10, 15, 30), (12, 8, 24), (9, 6, 18), (12, 10, 60)
    ]
    for t1, t2, mcm in bus_problems:
        mcd = math.gcd(t1, t2)
        questions.append({
            "text": f"Dos buses salen al mismo tiempo del terminal. El bus A pasa por un paradero cada {t1} minutos y el bus B pasa por el mismo paradero cada {t2} minutos. ¿En cuántos minutos volverán a coincidir en el paradero?",
            "explanation": f"Este problema se resuelve calculando el Mínimo Común Múltiplo (MCM) de los intervalos de tiempo {t1} y {t2}. El MCM({t1}, {t2}) es {mcm} minutos.",
            "choices": [
                {"text": f"En {mcm} minutos.", "is_correct": True},
                {"text": f"En {t1 + t2} minutos.", "is_correct": False},
                {"text": f"En {t1 * t2 * 2} minutos.", "is_correct": False},
                {"text": f"En {mcd} minutos.", "is_correct": False}
            ]
        })
    return questions

# Mapeo de slugs a sus generadores
GENERATORS = {
    '12-conjuntos-numericos': gen_conjuntos_numericos,
    '13-numeros-enteros-relaciones-de-orden-mayor-menor-e-igual': gen_relaciones_orden,
    '14-valor-absoluto-relaciones-de-orden': gen_valor_absoluto,
    '15-regla-de-signos-para-sumasrestas': gen_sumas_restas,
    '15a-ejercicios-de-sumas-y-restas-aplicacion-de-regla-de-los-signos': gen_sumas_restas,
    '16-regla-de-los-signos-en-multiplicaciondivision-ejemplos': gen_mult_div,
    '17-prioridad-de-operaciones-sumarestamultiplicaciondivision-combinadas': gen_prioridad,
    '18-numeros-primos-multiplos-y-divisores': gen_primos,
    '19-minimo-comun-multiplo-maximo-comun-divisor': gen_mcm_mcd,
    '19a-ejercicios-minimo-comun-multiplo': gen_mcm_mcd
}

def populate():
    slugs = list(GENERATORS)
    print(
        f"Iniciando poblado local sin API para {len(slugs)} recursos del tema "
        "'Números enteros' (hasta 35 preguntas nuevas por recurso)..."
    )
    total_pobladas = 0

    for idx, slug in enumerate(slugs, 1):
        print(f"\n[{idx}/{len(slugs)}] Generando preguntas para recurso: {slug}...")
        try:
            resource = Resource.objects.get(slug=slug)
        except Resource.DoesNotExist:
            print(f"  [Error] No existe el recurso con slug '{slug}'. Saltando.")
            continue

        # Generación reproducible por recurso. Nunca se borran preguntas existentes.
        random.seed(f"profeonline:{slug}:2026-06-19")
        questions_data = GENERATORS[slug]()

        existing_texts = set(
            Question.objects.filter(resource=resource).values_list("text", flat=True)
        )
        new_by_level = {1: [], 2: [], 3: []}
        for level, items in (
            (1, questions_data[0:10]),
            (2, questions_data[10:25]),
            (3, questions_data[25:35]),
        ):
            for item in items:
                text = item.get("text")
                if not text or text in existing_texts:
                    continue
                existing_texts.add(text)
                new_by_level[level].append(item)

        if not any(new_by_level.values()):
            print("  [Omitido] Todas las preguntas generadas ya existen.")
            continue

        try:
            with transaction.atomic():
                created = []
                for level in (1, 2, 3):
                    created.extend(
                        _save_questions(
                            resource=resource,
                            level=level,
                            mode="ambas",
                            questions_data=new_by_level[level],
                            status="publicada",
                        )
                    )

            sum_created = len(created)
            total_pobladas += sum_created
            print(
                f"  [Éxito] Agregadas {sum_created} preguntas nuevas para "
                f"'{resource.title}'; las existentes se conservaron."
            )
        except (TypeError, ValueError) as exc:
            print(f"  [Error] Al guardar preguntas para '{slug}': {exc}")

    print(f"\n¡Proceso local finalizado! Se agregaron {total_pobladas} preguntas nuevas.")


if __name__ == "__main__":
    populate()

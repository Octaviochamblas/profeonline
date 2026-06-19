import os
import sys
import django
import random

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

from apps.content.models import Resource
from apps.content.services.ai_generation_service import _save_questions

# Definir generadores dinámicos para cada recurso

def gen_conjuntos_numericos(resource):
    # Genera 15 preguntas
    questions = []

    # N1 Práctica & Evaluación (Conceptuales)
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

    # N2 Práctica & Evaluación (Clasificación mecánica)
    for i in range(5):
        num = random.randint(-50, -1)
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

    # N3 Práctica & Evaluación (Aplicación contextual)
    contexts = [
        {"desc": "un termómetro marca una temperatura de 4 grados bajo cero", "val": -4, "unit": "grados"},
        {"desc": "un submarino navega a una profundidad de 150 metros bajo el nivel del mar", "val": -150, "unit": "metros"},
        {"desc": "un cliente de un banco tiene una deuda de $12.000 en su cuenta", "val": -12000, "unit": "pesos"},
        {"desc": "un ascensor se encuentra en el tercer piso del subterráneo (-3)", "val": -3, "unit": "piso"}
    ]
    for ctx in contexts:
        questions.append({
            "text": f"Si representamos la siguiente situación con un número entero: '{ctx['desc']}', ¿cuál es el número entero correspondiente?",
            "explanation": f"Las situaciones que indican 'bajo cero', 'bajo el nivel del mar', 'subterráneo' o 'deuda/saldo en contra' se representan matemáticamente con números enteros negativos. En este caso corresponde a {ctx['val']}.",
            "choices": [
                {"text": f"{ctx['val']}", "is_correct": True},
                {"text": f"{abs(ctx['val'])}", "is_correct": False},
                {"text": "0", "is_correct": False},
                {"text": f"{ctx['val'] * 2}", "is_correct": False}
            ]
        })

    # Completar con más preguntas para llegar a 15
    while len(questions) < 15:
        num = random.randint(1, 100)
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

    return questions

def gen_relaciones_orden(resource):
    questions = []

    # N1 Conceptuales
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

    # N2 Comparaciones mecánicas
    for _ in range(7):
        n1 = random.randint(-30, -2)
        n2 = random.randint(n1 + 1, 10)

        # n2 > n1 siempre
        questions.append({
            "text": f"¿Cuál de las siguientes relaciones de comparación es correcta para los números {n1} y {n2}?",
            "explanation": f"En la recta numérica, {n2} está a la derecha de {n1} (cualquier positivo es mayor que un negativo, o un negativo más cercano a cero es mayor que uno más lejano). Por tanto, {n2} > {n1} (o {n1} < {n2}).",
            "choices": [
                {"text": f"{n1} < {n2}", "is_correct": True},
                {"text": f"{n1} > {n2}", "is_correct": False},
                {"text": f"{n1} = {n2}", "is_correct": False},
                {"text": "Ninguna relación es correcta", "is_correct": False}
            ]
        })

    # N3 Aplicación (Temperaturas)
    for _ in range(7):
        temp1 = random.randint(-15, -2)
        temp2 = random.randint(temp1 + 1, 5)
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

    return questions[:15]

def gen_valor_absoluto(resource):
    questions = []

    # N1 Conceptuales
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
            {"text": "Es el número multiplicado por -1.", "is_correct": False}
        ]
    })

    # N2 Operaciones mecánicas
    for _ in range(7):
        val = random.randint(-50, -5)
        questions.append({
            "text": f"¿Cuál es el valor de |{val}|?",
            "explanation": f"El valor absoluto de {val}, escrito como |{val}|, es la distancia de {val} al cero en la recta numérica, lo cual es {abs(val)} unidades.",
            "choices": [
                {"text": f"{abs(val)}", "is_correct": True},
                {"text": f"{val}", "is_correct": False},
                {"text": "0", "is_correct": False},
                {"text": f"{-val}", "is_correct": False} # repetido pero se maneja
            ]
        })
    # Asegurar opciones únicas
    for q in questions[2:]:
        if q["choices"][0]["text"] == q["choices"][3]["text"]:
            q["choices"][3]["text"] = "No se puede determinar"

    # N3 Problemas
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

    for _ in range(5):
        d1 = random.randint(-40, -10)
        d2 = random.randint(5, 9)
        # d1 absoluto es mayor que d2
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

    return questions[:15]

def gen_sumas_restas(resource):
    questions = []

    # N1 Conceptuales
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

    # N2 Ejercicios mecánicos
    for _ in range(7):
        n1 = random.randint(-25, -5)
        n2 = random.randint(-20, 20)
        ans = n1 + n2
        questions.append({
            "text": f"Resuelve la siguiente operación: {n1} + ({n2})",
            "explanation": f"Para resolver {n1} + ({n2}): si tienen igual signo se suman y conserva el signo; si tienen distinto signo se restan y conserva el signo del mayor absoluto. El resultado es {ans}.",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{ans + 5}", "is_correct": False},
                {"text": f"{ans - 10}", "is_correct": False},
                {"text": f"{n1 - n2}", "is_correct": False}
            ]
        })
    # Eliminar duplicados en alternativas si n2 es 0 o similar
    for q in questions[2:]:
        texts = [c["text"] for c in q["choices"]]
        if len(set(texts)) < 4:
            q["choices"][1]["text"] = f"{int(q['choices'][0]['text']) + 2}"
            q["choices"][2]["text"] = f"{int(q['choices'][0]['text']) - 2}"
            q["choices"][3]["text"] = f"{int(q['choices'][0]['text']) + 10}"

    # N3 Problemas aplicados
    for _ in range(6):
        saldo = random.randint(-15, -2) * 1000
        deposito = random.randint(5, 20) * 1000
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

    return questions[:15]

def gen_mult_div(resource):
    questions = []

    # N1 Conceptuales
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

    # N2 Ejercicios
    for _ in range(7):
        n1 = random.choice([-8, -6, -5, -4, 3, 5, 8])
        n2 = random.choice([-7, -6, -3, 2, 4, 9])
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

    # N3 Problemas
    for _ in range(6):
        desc = random.randint(2, 6)
        tiempo = random.randint(3, 8)
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

    return questions[:15]

def gen_prioridad(resource):
    questions = []

    # N1 Conceptuales
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

    # N2 Ejercicios combinados
    for _ in range(7):
        n1 = random.randint(2, 10)
        n2 = random.randint(2, 6)
        n3 = random.randint(-5, -2)
        ans = n1 + n2 * n3 # prioridad: n2 * n3 primero, luego + n1
        questions.append({
            "text": f"Calcula el resultado de la siguiente expresión: {n1} + {n2} · ({n3})",
            "explanation": f"Primero resolvemos la multiplicación por prioridad: {n2} · ({n3}) = {n2 * n3}. Luego sumamos el resultado: {n1} + ({n2 * n3}) = {ans}.",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{(n1 + n2) * n3}", "is_correct": False}, # error común de izquierda a derecha
                {"text": f"{ans + 5}", "is_correct": False},
                {"text": f"{ans - 5}", "is_correct": False}
            ]
        })

    # N3 Problemas
    for _ in range(7):
        base = random.randint(10, 30)
        cajas = random.randint(3, 6)
        cant = random.randint(4, 8)
        perdidas = random.randint(2, 5)
        ans = base + cajas * cant - perdidas
        questions.append({
            "text": f"Un almacén tiene {base} manzanas. Recibe {cajas} cajas con {cant} manzanas cada una. Si al final del día se botan {perdidas} manzanas que estaban en mal estado, ¿cuántas manzanas quedan?",
            "explanation": f"Escribimos la expresión matemática: {base} + {cajas} · {cant} - {perdidas}. Resolvemos la multiplicación primero: {cajas} · {cant} = {cajas * cant}. Luego sumamos y restamos: {base} + {cajas * cant} - {perdidas} = {ans} manzanas.",
            "choices": [
                {"text": f"{ans} manzanas", "is_correct": True},
                {"text": f"{(base + cajas) * cant - perdidas} manzanas", "is_correct": False},
                {"text": f"{base + cajas * (cant - perdidas)} manzanas", "is_correct": False},
                {"text": f"{ans - 10} manzanas", "is_correct": False}
            ]
        })

    return questions[:15]

def gen_primos(resource):
    questions = []

    # N1 Conceptuales
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

    # N2 Ejercicios mecánicos
    for _ in range(7):
        num = random.choice([9, 12, 15, 18, 20, 21, 25])
        divs = [d for d in range(1, num + 1) if num % d == 0]
        questions.append({
            "text": f"¿Cuáles son todos los divisores del número {num}?",
            "explanation": f"Los divisores de {num} son los números enteros que lo dividen de forma exacta (con residuo cero). Para {num}, estos son: {', '.join(map(str, divs))}.",
            "choices": [
                {"text": f"{', '.join(map(str, divs))}", "is_correct": True},
                {"text": f"1, {num}", "is_correct": False},
                {"text": f"{', '.join(map(str, divs[:-1]))}", "is_correct": False},
                {"text": f"1, 2, {num}", "is_correct": False}
            ]
        })
    # Asegurar que no se repitan por casualidad las falsas
    for q in questions[2:]:
        texts = [c["text"] for c in q["choices"]]
        if len(set(texts)) < 4:
            q["choices"][3]["text"] = "Ninguna de las anteriores"

    # N3 Problemas
    for _ in range(6):
        alumnos = random.choice([12, 18, 24, 30])
        # buscar opciones de distribución
        options = [d for d in range(2, alumnos) if alumnos % d == 0]
        opt = random.choice(options)
        questions.append({
            "text": f"Un profesor quiere organizar a sus {alumnos} alumnos en grupos de igual tamaño. ¿Cuál de los siguientes tamaños de grupo es posible sin que sobre ningún alumno?",
            "explanation": f"Para organizar a los {alumnos} alumnos de forma exacta, el tamaño del grupo debe ser un divisor de {alumnos}. Entre las opciones, {opt} es divisor de {alumnos}.",
            "choices": [
                {"text": f"Grupos de {opt} alumnos.", "is_correct": True},
                {"text": f"Grupos de {opt + 1 if (opt + 1) not in options else opt - 1} alumnos.", "is_correct": False},
                {"text": f"Grupos de {alumnos - 1 if (alumnos - 1) not in options else alumnos - 2} alumnos.", "is_correct": False},
                {"text": "No es posible organizarlos en grupos iguales.", "is_correct": False}
            ]
        })

    return questions[:15]

def gen_mcm_mcd(resource):
    questions = []

    # N1 Conceptuales
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

    # N2 Ejercicios mecánicos
    import math
    for _ in range(7):
        a = random.choice([4, 6, 8, 10])
        b = random.choice([3, 5, 6, 9])
        if a == b:
            b += 1
        mcd = math.gcd(a, b)
        mcm = (a * b) // mcd
        questions.append({
            "text": f"Calcula el Mínimo Común Múltiplo (MCM) de los números {a} y {b}.",
            "explanation": f"Los múltiplos de {a} son: {a}, {a*2}, {a*3}... y los de {b} son: {b}, {b*2}, {b*3}... El primer múltiplo común más pequeño que encontramos es {mcm}.",
            "choices": [
                {"text": f"{mcm}", "is_correct": True},
                {"text": f"{mcd}", "is_correct": False},
                {"text": f"{a * b}", "is_correct": False},
                {"text": f"{mcm + a}", "is_correct": False}
            ]
        })
    # Asegurar alternativas únicas
    for q in questions[2:]:
        texts = [c["text"] for c in q["choices"]]
        if len(set(texts)) < 4:
            q["choices"][2]["text"] = f"{int(q['choices'][0]['text']) + 12}"
            q["choices"][3]["text"] = f"{int(q['choices'][0]['text']) + 6}"

    # N3 Problemas
    for _ in range(6):
        t1 = random.choice([4, 6, 8])
        t2 = random.choice([3, 5, 7])
        mcd = math.gcd(t1, t2)
        mcm = (t1 * t2) // mcd
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

    return questions[:15]

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

slugs = list(GENERATORS.keys())

print(f"Iniciando poblado masivo local sin API para {len(slugs)} recursos del tema 'Números enteros'...")
total_pobladas = 0

for idx, slug in enumerate(slugs, 1):
    print(f"\n[{idx}/{len(slugs)}] Generando preguntas para recurso: {slug}...")
    try:
        resource = Resource.objects.get(slug=slug)
    except Resource.DoesNotExist:
        print(f"  [Error] No existe el recurso con slug '{slug}'. Saltando.")
        continue

    generator_fn = GENERATORS[slug]
    # Generamos 15 preguntas (que se guardarán para Práctica y Evaluación)
    questions_data = generator_fn(resource)

    # Las dividimos y guardamos según las directrices:
    # Las primeras 5 son para Nivel 1 (Definición) en modo "ambas"
    # Las siguientes 5 son para Nivel 2 (Ejercicios simples) en modo "ambas"
    # Las últimas 5 son para Nivel 3 (Problemas de aplicación) en modo "ambas"

    try:
        # Nivel 1
        n1_created = _save_questions(
            resource=resource,
            level=1,
            mode="ambas",
            questions_data=questions_data[0:5],
            status="publicada"
        )
        # Nivel 2
        n2_created = _save_questions(
            resource=resource,
            level=2,
            mode="ambas",
            questions_data=questions_data[5:10],
            status="publicada"
        )
        # Nivel 3
        n3_created = _save_questions(
            resource=resource,
            level=3,
            mode="ambas",
            questions_data=questions_data[10:15],
            status="publicada"
        )

        sum_created = len(n1_created) + len(n2_created) + len(n3_created)
        total_pobladas += sum_created
        print(f"  [Éxito] Generadas e insertadas {sum_created} preguntas para '{resource.title}'.")
    except Exception as e:
        print(f"  [Error] Al guardar preguntas para '{slug}': {e}")

print(f"\n¡Proceso finalizado con éxito! Se poblaron {total_pobladas} preguntas en total.")

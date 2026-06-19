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

# --- HELPERS GENERALES PARA VARIABILIDAD ---
NOMBRES = ["Juan", "María", "Carlos", "Ana", "Luis", "Sofía", "Diego", "Elena", "Andrés", "Patricia", "Javier", "Lucía", "Esteban", "Clara", "Gabriel", "Valentina", "Javier", "Camila", "Manuel", "Isabel", "Ricardo", "Florencia", "Tomás", "Antonia", "Martín", "Daniela", "Nicolás", "Catalina", "Pedro", "Paula"]
OBJETOS = ["manzanas", "pizzas", "tortas", "chocolates", "queques", "panes", "galletas", "frascos de mermelada", "bebidas", "quesos"]

def get_unique_pairs(count, range1, range2, condition=None):
    pairs = set()
    attempts = 0
    while len(pairs) < count and attempts < 1000:
        attempts += 1
        a = random.randint(*range1)
        b = random.randint(*range2)
        if condition is None or condition(a, b):
            pairs.add((a, b))
    return list(pairs)

def get_unique_triplets(count, range1, range2, range3, condition=None):
    triplets = set()
    attempts = 0
    while len(triplets) < count and attempts < 1000:
        attempts += 1
        a = random.randint(*range1)
        b = random.randint(*range2)
        c = random.randint(*range3)
        if condition is None or condition(a, b, c):
            triplets.add((a, b, c))
    return list(triplets)

# --- GENERADORES ESPECÍFICOS POR RECURSO ---

# 2.0 Fracciones propias, impropias y números mixtos
def gen_racionales_20():
    questions = []
    # LEVEL 1: Identificación propia/impropia (30 preguntas)
    pairs = get_unique_pairs(30, (2, 40), (2, 40), lambda n, d: n != d)
    for n, d in pairs:
        is_propia = n < d
        tipo = "propia" if is_propia else "impropia"
        correct = f"Fracción {tipo}"
        incorrect = f"Fracción {'impropia' if is_propia else 'propia'}"
        questions.append({
            "text": f"¿Cómo se clasifica la fracción {n}/{d}?",
            "explanation": f"La fracción {n}/{d} tiene un numerador ({n}) que es {'menor' if is_propia else 'mayor'} que el denominador ({d}), por lo que es una fracción {tipo}.",
            "choices": [
                {"text": correct, "is_correct": True},
                {"text": incorrect, "is_correct": False},
                {"text": "Fracción nula", "is_correct": False},
                {"text": "Número entero puro", "is_correct": False}
            ]
        })

    # LEVEL 2: Conversión a mixto y viceversa (30 preguntas)
    triplets = get_unique_triplets(30, (1, 10), (1, 11), (2, 12), lambda c, d, b: d < b)
    for i, (c, d, b) in enumerate(triplets):
        impropia_num = c * b + d
        if i % 2 == 0:
            questions.append({
                "text": f"Convierte la fracción impropia {impropia_num}/{b} a un número mixto.",
                "explanation": f"Dividimos {impropia_num} entre {b}: cabe {c} veces y sobran {d}. Por lo tanto, equivale a {c} enteros y {d}/{b}.",
                "choices": [
                    {"text": f"{c} {d}/{b}", "is_correct": True},
                    {"text": f"{c} {d+1}/{b}", "is_correct": False},
                    {"text": f"{c+1} {d}/{b}", "is_correct": False},
                    {"text": f"{d} {c}/{b}", "is_correct": False}
                ]
            })
        else:
            questions.append({
                "text": f"Convierte el número mixto {c} {d}/{b} a una fracción impropia.",
                "explanation": f"Multiplicamos la parte entera por el denominador y sumamos el numerador: ({c} · {b}) + {d} = {impropia_num}. Conservamos el denominador, resultando {impropia_num}/{b}.",
                "choices": [
                    {"text": f"{impropia_num}/{b}", "is_correct": True},
                    {"text": f"{impropia_num + b}/{b}", "is_correct": False},
                    {"text": f"{impropia_num - 1}/{b}", "is_correct": False},
                    {"text": f"{c * b}/{b}", "is_correct": False}
                ]
            })

    # LEVEL 3: Problemas de reparto (30 preguntas)
    triplets_p = get_unique_triplets(30, (2, 8), (2, 6), (2, 6), lambda t, p, e: t > p)
    for i, (t, p, e) in enumerate(triplets_p):
        nombre = NOMBRES[i % len(NOMBRES)]
        obj = OBJETOS[i % len(OBJETOS)]
        frac_num = t
        frac_den = p
        enteros = frac_num // frac_den
        sobrante = frac_num % frac_den
        questions.append({
            "text": f"{nombre} tiene {frac_num} porciones de {obj}, donde cada {obj[:-1] if obj.endswith('s') else obj} entera se divide en {frac_den} porciones iguales. ¿Cómo se expresa esta cantidad en número mixto?",
            "explanation": f"Al dividir {frac_num} porciones de tamaño 1/{frac_den}, obtenemos {enteros} {obj} completas y sobran {sobrante} porciones, es decir, {enteros} {sobrante}/{frac_den}.",
            "choices": [
                {"text": f"{enteros} {sobrante}/{frac_den}", "is_correct": True},
                {"text": f"{enteros + 1} {sobrante}/{frac_den}", "is_correct": False},
                {"text": f"{sobrante} {enteros}/{frac_den}", "is_correct": False},
                {"text": f"{frac_num}/{frac_den + 1}", "is_correct": False}
            ]
        })
    return questions

# 2.01 Conversión de decimales finitos, periódicos y semi-periódicos a Fracción
def gen_racionales_201():
    questions = []
    # LEVEL 1: Clasificación de decimales (30 preguntas)
    for i in range(30):
        tipo = i % 3
        val = random.randint(11, 99)
        if tipo == 0:
            questions.append({
                "text": f"¿Qué tipo de número decimal es 0.{val} (caso {i+1})?",
                "explanation": f"El número 0.{val} tiene una cantidad finita de cifras decimales, por lo que es un decimal finito.",
                "choices": [
                    {"text": "Decimal finito", "is_correct": True},
                    {"text": "Decimal periódico puro", "is_correct": False},
                    {"text": "Decimal semiperiódico", "is_correct": False},
                    {"text": "Número entero", "is_correct": False}
                ]
            })
        elif tipo == 1:
            questions.append({
                "text": f"¿Qué tipo de número decimal es 0.{val}{val}... (donde {val} se repite infinitamente) (caso {i+1})?",
                "explanation": f"La parte decimal entera se repite de manera infinita inmediatamente después de la coma, por lo que es un decimal periódico puro.",
                "choices": [
                    {"text": "Decimal periódico puro", "is_correct": True},
                    {"text": "Decimal finito", "is_correct": False},
                    {"text": "Decimal semiperiódico", "is_correct": False},
                    {"text": "Decimal irracional", "is_correct": False}
                ]
            })
        else:
            questions.append({
                "text": f"¿Qué tipo de número decimal es 0.3{val}{val}... (donde solo {val} se repite infinitamente) (caso {i+1})?",
                "explanation": f"Tiene una cifra que no se repite (el 3, anteperíodo) y luego un grupo que se repite infinitamente ({val}, período), por lo que es un decimal semiperiódico.",
                "choices": [
                    {"text": "Decimal semiperiódico", "is_correct": True},
                    {"text": "Decimal finito", "is_correct": False},
                    {"text": "Decimal periódico puro", "is_correct": False},
                    {"text": "Número entero", "is_correct": False}
                ]
            })

    # LEVEL 2: Conversión decimal finito a fracción (30 preguntas)
    pairs = get_unique_pairs(30, (1, 95), (2, 2), lambda a, b: a % 10 != 0)
    for val, _ in pairs:
        num = val
        den = 10 if val < 10 else 100
        g = math.gcd(num, den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"Convierte el número decimal finito {val/10 if val < 10 else val/100} a fracción simplificada.",
            "explanation": f"Escribimos el número sin coma en el numerador ({num}) y un 1 seguido de tantos ceros como decimales tenga en el denominador ({den}). Simplificando por {g} obtenemos {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{num}/{den + 10}", "is_correct": False},
                {"text": f"{correct_num + 1}/{correct_den}", "is_correct": False},
                {"text": f"{num + 1}/{den}", "is_correct": False}
            ]
        })

    # LEVEL 3: Conversión de periódicos complejos (30 preguntas)
    pairs_per = get_unique_pairs(30, (1, 9), (1, 9), lambda a, b: a != b)
    for i, (p1, p2) in enumerate(pairs_per):
        dec_str = f"0.{p1}{p2}{p1}{p2}..."
        num = p1 * 10 + p2
        den = 99
        g = math.gcd(num, den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"Convierte el decimal periódico {dec_str} a su fracción irreductible correspondiente.",
            "explanation": f"Para un decimal periódico de dos cifras periódicas, el numerador es el período ({num}) y el denominador contiene dos nueves ({den}). Simplificando por {g} queda {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{num}/100", "is_correct": False},
                {"text": f"{correct_num}/{correct_den + 1}", "is_correct": False},
                {"text": f"{num}/90", "is_correct": False}
            ]
        })
    return questions

# 2.01a Ejercicios: Conversión de decimales finitos, periódicos y semi-periódicos a Fracción
def gen_racionales_201a():
    questions = []
    # LEVEL 1: Preguntas sobre período y anteperíodo (30 preguntas)
    for i in range(30):
        val = random.randint(2, 9)
        ant = random.randint(1, 8)
        if i % 2 == 0:
            questions.append({
                "text": f"En el número decimal semiperiódico 0.1{val}{val}... ¿cuál es el período?",
                "explanation": f"El período es la cifra o grupo de cifras que se repite infinitamente. En este caso, {val} es el período.",
                "choices": [
                    {"text": f"{val}", "is_correct": True},
                    {"text": "1", "is_correct": False},
                    {"text": f"1{val}", "is_correct": False},
                    {"text": "No tiene período", "is_correct": False}
                ]
            })
        else:
            questions.append({
                "text": f"En el número decimal semiperiódico 0.{ant}{val}{val}... ¿cuál es el anteperíodo?",
                "explanation": f"El anteperíodo es la cifra o grupo de cifras que está entre la coma y el período, y que no se repite. En este caso, es {ant}.",
                "choices": [
                    {"text": f"{ant}", "is_correct": True},
                    {"text": f"{val}", "is_correct": False},
                    {"text": f"{ant}{val}", "is_correct": False},
                    {"text": "0", "is_correct": False}
                ]
            })

    # LEVEL 2: Decimales periódicos puros (30 preguntas)
    vals = random.sample(range(1, 99), 30)
    for val in vals:
        if val < 10:
            dec_str = f"0.{val}{val}..."
            num = val
            den = 9
        else:
            dec_str = f"0.{val}{val}..."
            num = val
            den = 99
        g = math.gcd(num, den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"Escribe el decimal periódico puro {dec_str} como fracción simplificada.",
            "explanation": f"Colocamos el período ({num}) en el numerador y tantos nueves como cifras tenga el período ({den}) en el denominador. Simplificado: {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{num}/{den + 1}", "is_correct": False},
                {"text": f"{num}/10" if val < 10 else f"{num}/100", "is_correct": False},
                {"text": f"{correct_num + 1}/{correct_den}", "is_correct": False}
            ]
        })

    # LEVEL 3: Decimales semiperiódicos de varios dígitos (30 preguntas)
    triplets = get_unique_triplets(30, (1, 8), (1, 9), (1, 9), lambda a, p1, p2: p1 != p2)
    for ant, p1, p2 in triplets:
        dec_str = f"0.{ant}{p1}{p2}{p1}{p2}..."
        total_num = ant * 100 + p1 * 10 + p2
        num = total_num - ant
        den = 990
        g = math.gcd(num, den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"Convierte el decimal semiperiódico {dec_str} a su fracción generatriz irreductible.",
            "explanation": f"Numerador: número completo ({total_num}) menos la parte no periódica ({ant}) = {num}. Denominador: dos nueves por las dos cifras del período y un cero por la cifra del anteperíodo = {den}. Simplificado: {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{num}/999", "is_correct": False},
                {"text": f"{total_num}/{den}", "is_correct": False},
                {"text": f"{num}/1000", "is_correct": False}
            ]
        })
    return questions

# 2.02 Sumas y restas de números decimales
def gen_racionales_202():
    questions = []
    # LEVEL 1: Conceptos de alineación (30 preguntas)
    for i in range(30):
        questions.append({
            "text": f"Al realizar una suma o resta de números decimales de forma manual (variación {i+1}), ¿qué elemento es crucial alinear verticalmente?",
            "explanation": "Para sumar o restar decimales de forma vertical, es indispensable alinear la coma decimal de todos los números para sumar correctamente las décimas con décimas, centésimas con centésimas, etc.",
            "choices": [
                {"text": "La coma decimal.", "is_correct": True},
                {"text": "La última cifra de la derecha.", "is_correct": False},
                {"text": "La primera cifra de la izquierda.", "is_correct": False},
                {"text": "No se requiere ninguna alineación.", "is_correct": False}
            ]
        })

    # LEVEL 2: Suma/resta con signos mixtos (30 preguntas)
    pairs = get_unique_pairs(30, (5, 95), (5, 95), lambda a, b: a != b)
    for val1, val2 in pairs:
        v1 = val1 / 10
        v2 = -val2 / 10
        ans = round(v1 + v2, 1)
        questions.append({
            "text": f"Resuelve la siguiente operación con decimales: {v1} + ({v2})",
            "explanation": f"Restamos los valores absolutos: {v1} - {abs(v2)} = {ans} (conservando el signo del número con mayor valor absoluto).",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{round(v1 - v2, 1)}", "is_correct": False},
                {"text": f"{round(-v1 + v2, 1)}", "is_correct": False},
                {"text": "0.0", "is_correct": False}
            ]
        })

    # LEVEL 3: Problemas cotidianos (compras, temperatura) (30 preguntas)
    pairs_p = get_unique_pairs(30, (10, 80), (1, 9), lambda a, b: a > 10)
    for i, (ent, dec) in enumerate(pairs_p):
        nombre = NOMBRES[i % len(NOMBRES)]
        precio1 = ent + dec/10
        precio2 = round(precio1 * 0.6, 2)
        total = round(precio1 + precio2, 2)
        questions.append({
            "text": f"{nombre} compra un cuaderno por ${precio1} y un lápiz por ${precio2}. ¿Cuánto dinero gasta en total?",
            "explanation": f"Sumamos los dos precios alinear la coma decimal: {precio1} + {precio2} = {total}.",
            "choices": [
                {"text": f"${total}", "is_correct": True},
                {"text": f"${round(precio1 - precio2, 2)}", "is_correct": False},
                {"text": f"${round(precio1 * 2, 2)}", "is_correct": False},
                {"text": f"${round(total + 10, 2)}", "is_correct": False}
            ]
        })
    return questions

# 2.02a Ejercicios: Números Racionales - Sumas y Restas de números decimales
def gen_racionales_202a():
    questions = []
    # LEVEL 1: Estimación (30 preguntas)
    for i in range(30):
        val1 = random.randint(11, 49) / 10
        val2 = random.randint(51, 89) / 10
        est = round(val1 + val2)
        questions.append({
            "text": f"Estima el resultado entero más cercano de la suma: {val1} + {val2} (caso {i+1})",
            "explanation": f"Sumando exactamente {val1} + {val2} obtenemos {round(val1 + val2, 2)}, cuyo entero más cercano es {est}.",
            "choices": [
                {"text": f"{est}", "is_correct": True},
                {"text": f"{est + 5}", "is_correct": False},
                {"text": f"{est - 3}", "is_correct": False},
                {"text": "0", "is_correct": False}
            ]
        })

    # LEVEL 2: Desarrollo directo complejo (30 preguntas)
    triplets = get_unique_triplets(30, (10, 50), (10, 50), (10, 50))
    for a, b, c in triplets:
        da, db, dc = a/100, b/100, c/100
        ans = round(da - db + dc, 2)
        questions.append({
            "text": f"Resuelve la operación combinada de decimales: {da} - {db} + {dc}",
            "explanation": f"Realizamos primero la resta {da} - {db} = {round(da-db, 2)}, y luego sumamos {dc} para obtener {ans}.",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{round(da + db + dc, 2)}", "is_correct": False},
                {"text": f"{round(da - db - dc, 2)}", "is_correct": False},
                {"text": f"{round(da + db - dc, 2)}", "is_correct": False}
            ]
        })

    # LEVEL 3: Problemas financieros (30 preguntas)
    pairs = get_unique_pairs(30, (100, 500), (10, 90))
    for i, (saldo, gasto) in enumerate(pairs):
        nombre = NOMBRES[i % len(NOMBRES)]
        s = saldo + 0.50
        g = gasto + 0.25
        ans = round(s - g, 2)
        questions.append({
            "text": f"{nombre} tiene un saldo de ${s} en su cuenta bancaria. Si realiza un pago de ${g}, ¿cuál es su nuevo saldo?",
            "explanation": f"Al saldo inicial le restamos el cobro realizado: {s} - {g} = {ans}.",
            "choices": [
                {"text": f"${ans}", "is_correct": True},
                {"text": f"${round(s + g, 2)}", "is_correct": False},
                {"text": f"${round(ans + 10, 2)}", "is_correct": False},
                {"text": f"${saldo}", "is_correct": False}
            ]
        })
    return questions

# 2.03 Números Racionales: Multiplicacion de números decimales
def gen_racionales_203():
    questions = []
    # LEVEL 1: Ubicación de la coma (30 preguntas)
    for i in range(30):
        dec1 = random.choice([1, 2, 3])
        dec2 = random.choice([1, 2])
        tot = dec1 + dec2
        questions.append({
            "text": f"Si multiplicamos un número decimal con {dec1} cifras decimales por otro con {dec2} cifras decimales, ¿cuántas cifras decimales tendrá el resultado final antes de simplificar? (caso {i+1})",
            "explanation": f"Al multiplicar decimales, la cantidad de cifras decimales del producto es la suma de las cifras decimales de los factores: {dec1} + {dec2} = {tot}.",
            "choices": [
                {"text": f"{tot} cifras decimales", "is_correct": True},
                {"text": f"{abs(dec1 - dec2)} cifras decimales", "is_correct": False},
                {"text": f"{dec1 * dec2} cifras decimales", "is_correct": False},
                {"text": "Ninguna, el resultado es entero", "is_correct": False}
            ]
        })

    # LEVEL 2: Multiplicación directa (30 preguntas)
    pairs = get_unique_pairs(30, (-12, 12), (2, 15), lambda a, b: a != 0)
    for n1, n2 in pairs:
        v1 = n1 / 10
        v2 = n2 / 10
        ans = round(v1 * v2, 2)
        questions.append({
            "text": f"Resuelve la siguiente multiplicación: {v1} · {v2}",
            "explanation": f"Multiplicamos {v1} por {v2} como si fueran enteros (y luego ubicamos la coma decimal retrocediendo dos posiciones desde la derecha, resultando {ans}).",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{round(v1 + v2, 2)}", "is_correct": False},
                {"text": f"{-ans}", "is_correct": False},
                {"text": f"{round(ans * 10, 2)}", "is_correct": False}
            ]
        })

    # LEVEL 3: Cálculo de áreas decimales (30 preguntas)
    pairs_a = get_unique_pairs(30, (15, 60), (12, 35))
    for i, (ancho_dm, largo_dm) in enumerate(pairs_a):
        nombre = NOMBRES[i % len(NOMBRES)]
        ancho = ancho_dm / 10
        largo = largo_dm / 10
        area = round(ancho * largo, 2)
        questions.append({
            "text": f"{nombre} quiere alfombrar una habitación rectangular que mide {ancho} metros de ancho y {largo} metros de largo. ¿Cuántos metros cuadrados de alfombra necesita?",
            "explanation": f"El área de un rectángulo se calcula multiplicando ancho por largo: {ancho} · {largo} = {area} metros cuadrados.",
            "choices": [
                {"text": f"{area} metros cuadrados", "is_correct": True},
                {"text": f"{round(ancho + largo, 2)} metros cuadrados", "is_correct": False},
                {"text": f"{round(area * 2, 2)} metros cuadrados", "is_correct": False},
                {"text": f"{round(area - 1, 2)} metros cuadrados", "is_correct": False}
            ]
        })
    return questions

# 2.03a Ejercicios: Nodos Racionales: Multiplicación de Decimales
def gen_racionales_203a():
    questions = []
    # LEVEL 1: Multiplicación por potencias de 10 (30 preguntas)
    for i in range(30):
        val = random.randint(105, 995) / 100
        factor = random.choice([10, 100, 1000])
        ans = round(val * factor, 3)
        questions.append({
            "text": f"Resuelve la multiplicación desplazando la coma decimal: {val} · {factor} (variación {i+1})",
            "explanation": f"Al multiplicar por una potencia de 10 ({factor}), movemos la coma hacia la derecha tantas posiciones como ceros tenga el factor, resultando {ans}.",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{val}", "is_correct": False},
                {"text": f"{round(val / factor, 5)}", "is_correct": False},
                {"text": f"{ans * 10}", "is_correct": False}
            ]
        })

    # LEVEL 2: Ejercicios mecánicos directos (30 preguntas)
    pairs = get_unique_pairs(30, (11, 49), (3, 9))
    for v1, v2 in pairs:
        val1 = v1 / 10
        val2 = v2 / 10
        ans = round(val1 * val2, 2)
        questions.append({
            "text": f"Resuelve el ejercicio: {val1} · {val2}",
            "explanation": f"Multiplicamos {v1} · {v2} = {v1 * v2}. Como ambos tienen un decimal, el producto lleva dos cifras decimales: {ans}.",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{-ans}", "is_correct": False},
                {"text": f"{round(val1 / val2, 2)}", "is_correct": False},
                {"text": f"{round(ans + 1, 2)}", "is_correct": False}
            ]
        })

    # LEVEL 3: Escala de planos (30 preguntas)
    pairs_e = get_unique_pairs(30, (5, 35), (2, 8))
    for i, (medida, escala_int) in enumerate(pairs_e):
        nombre = NOMBRES[i % len(NOMBRES)]
        m = medida / 10
        escala = escala_int + 0.5
        real = round(m * escala, 2)
        questions.append({
            "text": f"En el plano de {nombre}, una pared mide {m} cm. Si la escala del dibujo indica que cada centímetro equivale a {escala} metros reales, ¿cuánto mide la pared en la realidad?",
            "explanation": f"Multiplicamos la longitud en el plano por la equivalencia de la escala: {m} · {escala} = {real} metros.",
            "choices": [
                {"text": f"{real} metros", "is_correct": True},
                {"text": f"{round(m / escala, 2)} metros", "is_correct": False},
                {"text": f"{round(real * 10, 2)} metros", "is_correct": False},
                {"text": f"{round(real - 0.5, 2)} metros", "is_correct": False}
            ]
        })
    return questions

# 2.04 Nodos Racionales: División de números Decimales
def gen_racionales_204():
    questions = []
    # LEVEL 1: Quitar la coma del divisor (30 preguntas)
    for i in range(30):
        decimales = random.choice([1, 2, 3])
        factor = 10 ** decimales
        questions.append({
            "text": f"Para resolver la división manual de un número decimal por otro que tiene {decimales} cifras decimales, ¿por qué número debemos multiplicar a ambos para eliminar la coma del divisor? (caso {i+1})",
            "explanation": f"Para quitar {decimales} decimales del divisor y convertirlo en entero, multiplicamos dividendo y divisor por 10 elevado a {decimales}, lo cual es {factor}.",
            "choices": [
                {"text": f"{factor}", "is_correct": True},
                {"text": f"{decimales * 10}", "is_correct": False},
                {"text": "1", "is_correct": False},
                {"text": f"{factor * 10}", "is_correct": False}
            ]
        })

    # LEVEL 2: Divisiones de entero por decimal y decimal por decimal (30 preguntas)
    pairs = get_unique_pairs(30, (5, 50), (2, 9), lambda a, b: (a * 10) % b == 0)
    for a, b in pairs:
        dividendo = a
        divisor = b / 10
        ans = round(dividendo / divisor, 2)
        questions.append({
            "text": f"Resuelve la siguiente división: {dividendo} : {divisor}",
            "explanation": f"Multiplicamos ambos números por 10 para quitar la coma: {dividendo * 10} : {b} = {ans}.",
            "choices": [
                {"text": f"{ans}", "is_correct": True},
                {"text": f"{round(dividendo * divisor, 2)}", "is_correct": False},
                {"text": f"{round(ans / 10, 2)}", "is_correct": False},
                {"text": f"{round(ans + 2, 2)}", "is_correct": False}
            ]
        })

    # LEVEL 3: Distribución de pesos y líquidos (30 preguntas)
    pairs_d = get_unique_pairs(30, (30, 250), (2, 8), lambda a, b: (a * 10) % (b * 5) == 0)
    for i, (total, porcion) in enumerate(pairs_d):
        nombre = NOMBRES[i % len(NOMBRES)]
        t = total / 10
        p = porcion / 10
        ans = int(t / p)
        questions.append({
            "text": f"{nombre} tiene un bidón con {t} litros de jugo. Si desea envasarlo en botellas de {p} litros de capacidad cada una, ¿cuántas botellas completas logrará llenar?",
            "explanation": f"Dividimos el total de jugo por la capacidad de cada botella: {t} : {p} = {ans} botellas.",
            "choices": [
                {"text": f"{ans} botellas", "is_correct": True},
                {"text": f"{ans + 1} botellas", "is_correct": False},
                {"text": f"{ans - 2} botellas", "is_correct": False},
                {"text": f"{int(t * p)} botellas", "is_correct": False}
            ]
        })
    return questions

# 2.04a Ejercicios: Números Racionales - División de decimales
def gen_racionales_204a():
    questions = []
    # LEVEL 1: Signos en la división (30 preguntas)
    for i in range(30):
        tipo = i % 2
        val1 = random.randint(5, 50) / 10
        val2 = random.randint(2, 9) / 10
        if tipo == 0:
            questions.append({
                "text": f"Si dividimos un número decimal negativo (-{val1}) entre uno positivo ({val2}), ¿cuál será el signo del resultado? (variación {i+1})",
                "explanation": "La ley de signos para la división establece que un número negativo dividido por uno positivo da como resultado un número negativo.",
                "choices": [
                    {"text": "Negativo", "is_correct": True},
                    {"text": "Positivo", "is_correct": False},
                    {"text": "Depende de cuál número sea mayor en valor absoluto.", "is_correct": False},
                    {"text": "Cero", "is_correct": False}
                ]
            })
        else:
            questions.append({
                "text": f"Si dividimos un número decimal negativo (-{val1}) entre otro negativo (-{val2}), ¿cuál será el signo del resultado? (variación {i+1})",
                "explanation": "La ley de signos para la división establece que un número negativo dividido por otro negativo da como resultado un número positivo.",
                "choices": [
                    {"text": "Positivo", "is_correct": True},
                    {"text": "Negativo", "is_correct": False},
                    {"text": "Depende del residuo de la división.", "is_correct": False},
                    {"text": "Indeterminado", "is_correct": False}
                ]
            })

    # LEVEL 2: Divisiones con conversión a fracción (30 preguntas)
    pairs = get_unique_pairs(30, (3, 18), (3, 9), lambda a, b: a != b)
    for num, den in pairs:
        dec_val = round(num / 9, 3)
        divisor = den / 10
        ans_num = num * 10
        ans_den = 9 * den
        g = math.gcd(ans_num, ans_den)
        correct_num = ans_num // g
        correct_den = ans_den // g
        questions.append({
            "text": f"Calcula la división de un decimal periódico por uno finito: 0.{num}{num}... : {divisor}",
            "explanation": f"Convertimos el periódico a fracción: 0.{num}{num}... = {num}/9. El finito es {den}/10. Dividimos: ({num}/9) : ({den}/10) = ({num}/9) · (10/{den}) = {ans_num}/{ans_den} = {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{ans_num}/{ans_den + 2}", "is_correct": False},
                {"text": f"{num}/{den}", "is_correct": False},
                {"text": f"{correct_num + 1}/{correct_den}", "is_correct": False}
            ]
        })

    # LEVEL 3: Dosificación médica (30 preguntas)
    pairs_m = get_unique_pairs(30, (5, 30), (2, 8), lambda a, b: (a * 10) % b == 0)
    for i, (dosis_total, dosis_toma) in enumerate(pairs_m):
        nombre = NOMBRES[i % len(NOMBRES)]
        dt = dosis_total / 10
        dp = dosis_toma / 10
        ans = int(dt / dp)
        questions.append({
            "text": f"Un médico receta a {nombre} un frasco de jarabe que contiene {dt} ml. Si cada dosis diaria debe ser de exactamente {dp} ml, ¿para cuántos días de tratamiento alcanzará el frasco?",
            "explanation": f"Dividimos la dosis total del frasco por la dosis diaria: {dt} : {dp} = {ans} días.",
            "choices": [
                {"text": f"{ans} días", "is_correct": True},
                {"text": f"{ans + 1} días", "is_correct": False},
                {"text": f"{ans - 1} días", "is_correct": False},
                {"text": f"{int(dt * dp)} días", "is_correct": False}
            ]
        })
    return questions

# 2.05 Simplificación de fracciones y fracciones equivalentes
def gen_racionales_205():
    questions = []
    # LEVEL 1: Fracciones equivalentes (30 preguntas)
    pairs = get_unique_pairs(30, (2, 10), (3, 12), lambda a, b: a < b and math.gcd(a, b) == 1)
    for i, (a, b) in enumerate(pairs):
        f = random.choice([2, 3, 4, 5])
        correct_num = a * f
        correct_den = b * f
        questions.append({
            "text": f"¿Cuál de las siguientes fracciones es equivalente a {a}/{b}? (variación {i+1})",
            "explanation": f"Al amplificar la fracción {a}/{b} por {f} (multiplicando numerador y denominador por {f}), obtenemos {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{correct_num + 1}/{correct_den}", "is_correct": False},
                {"text": f"{correct_num}/{correct_den + 1}", "is_correct": False},
                {"text": f"{a + f}/{b + f}", "is_correct": False}
            ]
        })

    # LEVEL 2: Simplificación de fracciones grandes (30 preguntas)
    triplets = get_unique_triplets(30, (2, 8), (3, 10), (6, 15), lambda a, b, f: a < b and math.gcd(a, b) == 1)
    for a, b, f in triplets:
        num = a * f
        den = b * f
        questions.append({
            "text": f"Simplifica la fracción {num}/{den} a su forma irreductible.",
            "explanation": f"Dividimos el numerador y el denominador por su máximo común divisor, que es {f}: {num}:{f} = {a} y {den}:{f} = {b}. Obtenemos {a}/{b}.",
            "choices": [
                {"text": f"{a}/{b}", "is_correct": True},
                {"text": f"{a*2}/{b*2}", "is_correct": False},
                {"text": f"{a}/{b + 1}", "is_correct": False},
                {"text": f"{a + 1}/{b}", "is_correct": False}
            ]
        })

    # LEVEL 3: Problemas de razones (30 preguntas)
    triplets_p = get_unique_triplets(30, (5, 20), (5, 20), (2, 5))
    for i, (hombres_base, mujeres_base, f) in enumerate(triplets_p):
        nombre = NOMBRES[i % len(NOMBRES)]
        h = hombres_base * f
        m = mujeres_base * f
        total = h + m
        g = math.gcd(h, total)
        ans_num = h // g
        ans_den = total // g
        questions.append({
            "text": f"En el grupo de {nombre} hay {h} hombres y {m} mujeres. ¿Qué fracción del total del grupo representan los hombres, expresada de forma simplificada?",
            "explanation": f"La fracción de hombres es {h} sobre el total de {total} personas. Simplificando {h}/{total} por su MCD ({g}) obtenemos {ans_num}/{ans_den}.",
            "choices": [
                {"text": f"{ans_num}/{ans_den}", "is_correct": True},
                {"text": f"{h}/{total + 2}", "is_correct": False},
                {"text": f"{ans_num}/{ans_den + 1}", "is_correct": False},
                {"text": f"{m}/{total}", "is_correct": False}
            ]
        })
    return questions

# 2.05a Ejercicios: Números Racionales - Operaciones Combinadas
def gen_racionales_205a():
    questions = []
    # LEVEL 1: Prioridad de operaciones conceptual (30 preguntas)
    for i in range(30):
        questions.append({
            "text": f"En operaciones combinadas con fracciones (caso {i+1}), ¿qué operación debe resolverse antes que las sumas y restas si no hay paréntesis?",
            "explanation": "De acuerdo a la prioridad matemática, las multiplicaciones y divisiones se deben resolver siempre antes que las sumas y restas.",
            "choices": [
                {"text": "La multiplicación y la división.", "is_correct": True},
                {"text": "La suma y la resta.", "is_correct": False},
                {"text": "Cualquiera, de izquierda a derecha.", "is_correct": False},
                {"text": "Las operaciones que tengan denominadores menores.", "is_correct": False}
            ]
        })

    # LEVEL 2: Ejercicios directos de operaciones combinadas (30 preguntas)
    triplets = get_unique_triplets(30, (1, 5), (1, 4), (2, 5))
    for a, b, c in triplets:
        num = a + b
        den = c * 2
        g = math.gcd(num, den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"Resuelve la siguiente operación combinada: ({a}/{c} + {b}/{c}) · 1/2",
            "explanation": f"Primero resolvemos el paréntesis: {a}/{c} + {b}/{c} = {a+b}/{c}. Luego multiplicamos por 1/2: ({a+b}/{c}) · (1/2) = {num}/{den}. Simplificado: {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{num}/{den + 1}", "is_correct": False},
                {"text": f"{a+b}/{c}", "is_correct": False},
                {"text": "1/2", "is_correct": False}
            ]
        })

    # LEVEL 3: Operaciones con paréntesis anidados (30 preguntas)
    triplets_p = get_unique_triplets(30, (1, 4), (1, 3), (2, 5))
    for a, b, c in triplets_p:
        num = (c - a) * b
        den = c
        g = math.gcd(num, den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"Resuelve la operación: [ 1 - ({a}/{c}) ] · {b}",
            "explanation": f"Resolvemos la resta interna: 1 - {a}/{c} = {c}/{c} - {a}/{c} = {c-a}/{c}. Luego multiplicamos por {b}: ({c-a}/{c}) · {b} = {num}/{den}. Simplificado: {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{(c-a)*b}/{c+1}", "is_correct": False},
                {"text": f"{c-a}/{c}", "is_correct": False},
                {"text": f"{correct_num + 1}/{correct_den}", "is_correct": False}
            ]
        })
    return questions

# 2.06 Números Racionales: Multiplicación y División de Fracciones
def gen_racionales_206():
    questions = []
    # LEVEL 1: Conceptos de multiplicación/división (30 preguntas)
    for i in range(30):
        tipo = i % 2
        if tipo == 0:
            questions.append({
                "text": f"Para multiplicar dos fracciones (caso {i+1}), ¿cuál es el procedimiento correcto?",
                "explanation": "La multiplicación de fracciones se realiza de forma directa: multiplicando numerador con numerador y denominador con denominador.",
                "choices": [
                    {"text": "Multiplicar numerador con numerador y denominador con denominador.", "is_correct": True},
                    {"text": "Multiplicar cruzado (numerador por denominador contrario).", "is_correct": False},
                    {"text": "Mantener el denominador común y multiplicar solo numeradores.", "is_correct": False},
                    {"text": "Invertir la primera fracción y luego sumarlas.", "is_correct": False}
                ]
            })
        else:
            questions.append({
                "text": f"Para dividir dos fracciones (caso {i+1}), ¿cuál es el procedimiento estándar?",
                "explanation": "Para dividir dos fracciones, se multiplica la primera fracción por el recíproco (inverso multiplicativo) de la segunda fracción.",
                "choices": [
                    {"text": "Multiplicar la primera fracción por el inverso de la segunda.", "is_correct": True},
                    {"text": "Multiplicar de forma directa numerador con numerador.", "is_correct": False},
                    {"text": "Sumar los numeradores y restar los denominadores.", "is_correct": False},
                    {"text": "Dividir cruzado sumando el resultado.", "is_correct": False}
                ]
            })

    # LEVEL 2: Operaciones directas con fracciones (30 preguntas)
    triplets = get_unique_triplets(30, (2, 7), (2, 8), (3, 10), lambda a, b, c: a != b and b != c)
    for a, b, c in triplets:
        g = math.gcd(a, c)
        correct_num = a // g
        correct_den = c // g
        questions.append({
            "text": f"Resuelve el producto de fracciones: {a}/{b} · {b}/{c}",
            "explanation": f"Multiplicamos directamente: ({a} · {b}) / ({b} · {c}) = {a*b}/{b*c}. Simplificando por {b} (simplificación cruzada), nos queda {a}/{c}. Simplificado al máximo: {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{a}/{b*c}", "is_correct": False},
                {"text": f"{correct_num + 1}/{correct_den}", "is_correct": False},
                {"text": f"{a+b}/{b+c}", "is_correct": False}
            ]
        })

    # LEVEL 3: Partes de partes (30 preguntas)
    triplets_p = get_unique_triplets(30, (1, 4), (2, 5), (3, 8), lambda n1, d1, d2: n1 < d1)
    for i, (n1, d1, d2) in enumerate(triplets_p):
        nombre = NOMBRES[i % len(NOMBRES)]
        num = n1
        den = d1 * d2
        g = math.gcd(num, den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"{nombre} tiene una barra de chocolate. Si regala 1/{d2} de la barra, y luego consume {n1}/{d1} de la parte que regaló, ¿qué fracción de la barra original consumió?",
            "explanation": f"Calculamos la fracción de una fracción multiplicándolas: {n1}/{d1} · 1/{d2} = {num}/{den}. Simplificado queda {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{n1}/{d1 + d2}", "is_correct": False},
                {"text": f"{correct_num}/{correct_den + 2}", "is_correct": False},
                {"text": "1/2", "is_correct": False}
            ]
        })
    return questions

# 2.06a Ejercicios: Números Racionales: Multiplicación con simplificación
def gen_racionales_206a():
    questions = []
    # LEVEL 1: Simplificación cruzada conceptual (30 preguntas)
    for i in range(30):
        questions.append({
            "text": f"En el producto de fracciones a/b · c/d (caso {i+1}), ¿qué cifras se pueden simplificar mutuamente antes de realizar la multiplicación?",
            "explanation": "En la multiplicación de fracciones, se puede realizar simplificación cruzada: cualquier numerador con cualquier denominador (el numerador 'a' con 'd', o el numerador 'c' con 'b').",
            "choices": [
                {"text": "Cualquier numerador con cualquier denominador.", "is_correct": True},
                {"text": "Solo numeradores entre sí.", "is_correct": False},
                {"text": "Solo denominadores entre sí.", "is_correct": False},
                {"text": "Únicamente denominadores que sean iguales.", "is_correct": False}
            ]
        })

    # LEVEL 2: Ejercicios de simplificación cruzada (30 preguntas)
    triplets = get_unique_triplets(30, (2, 9), (2, 9), (2, 5))
    for a, b, f in triplets:
        num = 1
        den = f * f
        questions.append({
            "text": f"Resuelve utilizando la simplificación cruzada antes de multiplicar: {a}/{b * f} · {b}/{a * f}",
            "explanation": f"Simplificamos cruzado: el {a} con el {a*f} (queda 1 y {f}), y el {b} con el {b*f} (queda 1 y {f}). Multiplicando los remanentes: 1/{f} · 1/{f} = 1/{den}.",
            "choices": [
                {"text": f"1/{den}", "is_correct": True},
                {"text": f"1/{f}", "is_correct": False},
                {"text": f"{a*b}/{a*b*f*f}", "is_correct": False},
                {"text": f"2/{den}", "is_correct": False}
            ]
        })

    # LEVEL 3: Problemas de escala e ingeniería (30 preguntas)
    triplets_p = get_unique_triplets(30, (2, 10), (3, 12), (5, 20), lambda f1, f2, m: f1 < f2)
    for i, (f1, f2, m) in enumerate(triplets_p):
        nombre = NOMBRES[i % len(NOMBRES)]
        num = m * f1
        den = f2
        g = math.gcd(num, den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"{nombre} diseña una maqueta donde cada metro real se representa con {f1}/{f2} metros de maqueta. Si una estructura real mide {m} metros de altura, ¿cuántos metros de altura tendrá en la maqueta?",
            "explanation": f"Multiplicamos la altura real por la escala de la maqueta: {m} · {f1}/{f2} = {num}/{den}. Simplificando por {g} obtenemos {correct_num}/{correct_den} metros.",
            "choices": [
                {"text": f"{correct_num}/{correct_den} metros", "is_correct": True},
                {"text": f"{m}/{f2} metros", "is_correct": False},
                {"text": f"{correct_num + 1}/{correct_den} metros", "is_correct": False},
                {"text": f"{f1}/{f2} metros", "is_correct": False}
            ]
        })
    return questions

# 2-07 Números Racionales Suma y Resta de Fracciones
def gen_racionales_2_07():
    questions = []
    # LEVEL 1: MCM conceptual (30 preguntas)
    pairs = get_unique_pairs(30, (2, 12), (2, 12), lambda a, b: a != b)
    for i, (a, b) in enumerate(pairs):
        mcm = math.lcm(a, b)
        questions.append({
            "text": f"Para sumar dos fracciones cuyos denominadores son {a} y {b}, ¿cuál es el mínimo común denominador que debemos utilizar? (caso {i+1})",
            "explanation": f"El mínimo común denominador es el mínimo común múltiplo (MCM) de los denominadores. Para {a} y {b}, el MCM es {mcm}.",
            "choices": [
                {"text": f"{mcm}", "is_correct": True},
                {"text": f"{a * b}", "is_correct": False},
                {"text": f"{math.gcd(a, b)}", "is_correct": False},
                {"text": f"{mcm + 1}", "is_correct": False}
            ]
        })

    # LEVEL 2: Suma/resta con distinto denominador (30 preguntas)
    triplets = get_unique_triplets(30, (1, 5), (1, 5), (2, 6), lambda a, b, c: a != b)
    for a, b, c in triplets:
        d1 = c
        d2 = c + 1
        num = a * d2 - b * d1
        den = d1 * d2
        g = math.gcd(abs(num), den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"Resuelve la resta de fracciones: {a}/{d1} - {b}/{d2}",
            "explanation": f"El mínimo común denominador es {den}. Multiplicamos cruzado: ({a} · {d2}) - ({b} · {d1}) = {a*d2} - {b*d1} = {num}. Queda {num}/{den}. Simplificado: {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{a - b}/{d1 - d2}", "is_correct": False},
                {"text": f"{num}/{den + 2}", "is_correct": False},
                {"text": f"{correct_num + 1}/{correct_den}", "is_correct": False}
            ]
        })

    # LEVEL 3: Estanque de agua (30 preguntas)
    triplets_p = get_unique_triplets(30, (1, 3), (1, 3), (4, 8))
    for i, (n1, n2, den_base) in enumerate(triplets_p):
        nombre = NOMBRES[i % len(NOMBRES)]
        d1 = den_base
        d2 = den_base - 1
        num = n1 * d2 + n2 * d1
        den = d1 * d2
        g = math.gcd(num, den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"Un estanque contiene agua hasta las {n1}/{d1} partes de su capacidad. Si {nombre} vierte agua equivalente a {n2}/{d2} partes del estanque, ¿qué fracción de la capacidad total del estanque contiene agua ahora?",
            "explanation": f"Sumamos ambas fracciones buscando el denominador común ({den}): {n1}/{d1} + {n2}/{d2} = ({n1*d2} + {n2*d1})/{den} = {num}/{den}. Simplificado: {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{n1+n2}/{d1+d2}", "is_correct": False},
                {"text": f"{correct_num}/{correct_den + 1}", "is_correct": False},
                {"text": f"{num + 1}/{den}", "is_correct": False}
            ]
        })
    return questions

# 2-07a Ejercicios: Suma y Resta de FRACCIONES
def gen_racionales_2_07a():
    questions = []
    # LEVEL 1: Igual denominador (30 preguntas)
    triplets = get_unique_triplets(30, (1, 10), (1, 10), (11, 25))
    for a, b, c in triplets:
        tot = a + b
        g = math.gcd(tot, c)
        correct_num = tot // g
        correct_den = c // g
        questions.append({
            "text": f"Resuelve la suma de fracciones con igual denominador: {a}/{c} + {b}/{c}",
            "explanation": f"Como los denominadores son iguales ({c}), simplemente sumamos los numeradores: {a} + {b} = {tot}. La fracción es {tot}/{c}. Simplificado: {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{tot}/{c * 2}", "is_correct": False},
                {"text": f"{correct_num + 1}/{correct_den}", "is_correct": False},
                {"text": f"{a*b}/{c}", "is_correct": False}
            ]
        })

    # LEVEL 2: Más de tres fracciones (30 preguntas)
    for i in range(30):
        a = random.choice([2, 3])
        b = random.choice([4, 5])
        c = random.choice([6, 7])
        mcm = math.lcm(math.lcm(a, b), c)
        num = (mcm // a) + (mcm // b) - (mcm // c)
        g = math.gcd(num, mcm)
        correct_num = num // g
        correct_den = mcm // g
        questions.append({
            "text": f"Resuelve la siguiente expresión combinada de tres fracciones: 1/{a} + 1/{b} - 1/{c} (variación {i+1})",
            "explanation": f"El MCM de {a}, {b} y {c} es {mcm}. Llevamos las fracciones a este denominador: {mcm//a}/{mcm} + {mcm//b}/{mcm} - {mcm//c}/{mcm} = {num}/{mcm}. Simplificado: {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{1 + 1 - 1}/{a + b - c}", "is_correct": False},
                {"text": f"{num}/{mcm + 2}", "is_correct": False},
                {"text": f"{correct_num + 1}/{correct_den}", "is_correct": False}
            ]
        })

    # LEVEL 3: Problemas de herencia y reparto (30 preguntas)
    pairs_p = get_unique_pairs(30, (2, 4), (5, 10))
    for i, (d1, d2) in enumerate(pairs_p):
        nombre = NOMBRES[i % len(NOMBRES)]
        den = d1 * d2
        num = den - d2 - d1
        g = math.gcd(num, den)
        correct_num = num // g
        correct_den = den // g
        questions.append({
            "text": f"{nombre} reparte un terreno. Regala 1/{d1} a su hermano y 1/{d2} a su hijo, y se queda con el resto. ¿Qué fracción del terreno se queda {nombre}?",
            "explanation": f"Restamos del total (1) la suma de las partes regaladas: 1 - (1/{d1} + 1/{d2}) = 1 - ({d1+d2}/{den}) = {num}/{den}. Simplificado: {correct_num}/{correct_den}.",
            "choices": [
                {"text": f"{correct_num}/{correct_den}", "is_correct": True},
                {"text": f"{d1+d2}/{den}", "is_correct": False},
                {"text": f"{correct_num}/{correct_den + 1}", "is_correct": False},
                {"text": "0", "is_correct": False}
            ]
        })
    return questions

# 2.08 Prioridad de operaciones con racionales mezclados
def gen_racionales_208():
    questions = []
    # LEVEL 1: Reglas de prioridad mezclada (30 preguntas)
    for i in range(30):
        questions.append({
            "text": f"Si en un ejercicio combinamos fracciones, decimales, sumas y multiplicaciones (caso {i+1}), ¿qué operación debe resolverse en primer lugar según las reglas de prioridad?",
            "explanation": "Las reglas de prioridad de operaciones exigen resolver siempre primero los paréntesis, luego potencias, después multiplicaciones y divisiones, y al final sumas y restas.",
            "choices": [
                {"text": "Los Paréntesis (si existen) o las multiplicaciones/divisiones.", "is_correct": True},
                {"text": "Las sumas y restas siempre.", "is_correct": False},
                {"text": "Los decimales antes que las fracciones.", "is_correct": False},
                {"text": "De izquierda a derecha sin importar el tipo de operación.", "is_correct": False}
            ]
        })

    # LEVEL 2: Ejercicios directos mezclados (30 preguntas)
    triplets = get_unique_triplets(30, (1, 4), (1, 5), (2, 8))
    for a, b, c in triplets:
        val = (a + 1) * c
        correct = f"{val/2}" if val % 2 != 0 else f"{val//2}"
        questions.append({
            "text": f"Resuelve el siguiente ejercicio mixto de prioridad: ( {a}/2 + 0.5 ) · {c}",
            "explanation": f"Convertimos 0.5 a fracción (1/2). Sumamos dentro del paréntesis: {a}/2 + 1/2 = {a+1}/2. Luego multiplicamos por {c}: ({a+1}/2) · {c} = {val}/2 = {correct}.",
            "choices": [
                {"text": correct, "is_correct": True},
                {"text": f"{val/2 + 1}", "is_correct": False},
                {"text": f"{val/2 - 0.5}", "is_correct": False},
                {"text": f"{a+c}", "is_correct": False}
            ]
        })

    # LEVEL 3: Problemas de modelado algebraico combinados (30 preguntas)
    triplets_p = get_unique_triplets(30, (5, 25), (2, 6), (10, 40))
    for i, (total, porcion, extra) in enumerate(triplets_p):
        nombre = NOMBRES[i % len(NOMBRES)]
        total_float = float(total)
        gastado = porcion * 1.5
        ext = extra / 10
        ans = round(total_float - gastado + ext, 2)
        questions.append({
            "text": f"{nombre} tiene ${total_float}. Si gasta el equivalente a {porcion} bolsas de dulces a ${1.5} cada una, y luego recibe un reembolso de ${ext}, ¿cuál es su saldo total final?",
            "explanation": f"Primero resolvemos la multiplicación del gasto: {porcion} · 1.5 = {gastado}. Luego restamos del total: {total_float} - {gastado} = {total_float - gastado}. Finalmente sumamos el reembolso: {total_float - gastado} + {ext} = {ans}.",
            "choices": [
                {"text": f"${ans}", "is_correct": True},
                {"text": f"${round(total_float + gastado + ext, 2)}", "is_correct": False},
                {"text": f"${round(total_float - gastado, 2)}", "is_correct": False},
                {"text": f"${round(ans + 5, 2)}", "is_correct": False}
            ]
        })
    return questions

# Mapeo de slugs a sus generadores
GENERATORS = {
    '20-numeros-racionales-fraciones-propias-impropias-y-numeros-mixtos': gen_racionales_20,
    '201-numeros-racionales-conversion-de-decimales-finitos-periodicos-y-semi-periodicos-a-fraccion': gen_racionales_201,
    '201a-ejercicios-conversion-de-decimales-finitos-periodicos-y-semi-periodicos-a-fraccion': gen_racionales_201a,
    '202-numeros-racionales-sumas-y-restas-de-numeros-decimales': gen_racionales_202,
    '202a-ejercicios-numeros-racionales-sumas-y-restas-de-numeros-decimales': gen_racionales_202a,
    '203-numeros-racionales-multiplicacion-de-numeros-decimales': gen_racionales_203,
    '203a-ejercicios-nodos-racionales-multiplicacion-de-decimales': gen_racionales_203a,
    '204-nodos-racionales-division-de-numeros-decimales': gen_racionales_204,
    '204a-ejercicios-numeros-racionales-division-de-decimales': gen_racionales_204a,
    '205-numeros-racionales-que-son-las-fracciones-simplificacion-fracciones': gen_racionales_205,
    '205a-ejercicios-numeros-racionales-operaciones-combinadas-profeonlinecl': gen_racionales_205a,
    '206-numeros-racionales-multiplicacion-y-division-de-fracciones': gen_racionales_206,
    '206a-ejercicios-numeros-racionales-multiplicacion-con-simplificacion-profeonlinecl': gen_racionales_206a,
    '2-07-numeros-racionales-suma-y-resta-de-fracciones': gen_racionales_2_07,
    '2-07a-ejercicios-suma-y-resta-de-fracciones-profeonlinecl': gen_racionales_2_07a,
    '208-numeros-racionales-prioridad-en-las-operaciones': gen_racionales_208
}

def populate():
    slugs = list(GENERATORS)
    print(
        f"Iniciando poblado local sin API para {len(slugs)} recursos del tema "
        "'Números racionales' (90 preguntas por recurso: 10 de práctica, 10 de evaluación y 10 en común por nivel)..."
    )
    total_pobladas = 0

    for idx, slug in enumerate(slugs, 1):
        print(f"\n[{idx}/{len(slugs)}] Generando preguntas para recurso: {slug}...")
        try:
            resource = Resource.objects.get(slug=slug)
        except Resource.DoesNotExist:
            print(f"  [Error] No existe el recurso con slug '{slug}'. Saltando.")
            continue

        # Generación reproducible por recurso. Saneamiento limpio por recurso.
        random.seed(f"profeonline_racionales:{slug}:2026-06-19")
        questions_data = GENERATORS[slug]()

        # Agrupar preguntas por nivel y por modo
        new_questions_by_level_and_mode = {
            1: {"preparacion": [], "evaluacion": [], "ambas": []},
            2: {"preparacion": [], "evaluacion": [], "ambas": []},
            3: {"preparacion": [], "evaluacion": [], "ambas": []},
        }

        # Level 1 (indices 0 a 29)
        local_texts = set()
        for sub_idx, item in enumerate(questions_data[0:30]):
            text = item.get("text")
            if text and text not in local_texts:
                local_texts.add(text)
                mode = "preparacion" if sub_idx < 10 else ("evaluacion" if sub_idx < 20 else "ambas")
                new_questions_by_level_and_mode[1][mode].append(item)

        # Level 2 (indices 30 a 59)
        for sub_idx, item in enumerate(questions_data[30:60]):
            text = item.get("text")
            if text and text not in local_texts:
                local_texts.add(text)
                mode = "preparacion" if sub_idx < 10 else ("evaluacion" if sub_idx < 20 else "ambas")
                new_questions_by_level_and_mode[2][mode].append(item)

        # Level 3 (indices 60 a 89)
        for sub_idx, item in enumerate(questions_data[60:90]):
            text = item.get("text")
            if text and text not in local_texts:
                local_texts.add(text)
                mode = "preparacion" if sub_idx < 10 else ("evaluacion" if sub_idx < 20 else "ambas")
                new_questions_by_level_and_mode[3][mode].append(item)

        try:
            with transaction.atomic():
                # Saneamiento de preguntas viejas de este recurso
                Question.objects.filter(resource=resource).delete()

                created_count = 0
                for lvl in (1, 2, 3):
                    for mode in ("preparacion", "evaluacion", "ambas"):
                        batch = new_questions_by_level_and_mode[lvl][mode]
                        if batch:
                            created = _save_questions(
                                resource=resource,
                                level=lvl,
                                mode=mode,
                                questions_data=batch,
                                status="publicada",
                            )
                            created_count += len(created)

            total_pobladas += created_count
            print(
                f"  [Éxito] Pobladas exactamente {created_count} preguntas para "
                f"'{resource.title}' (10 práctica, 10 evaluación y 10 comunes por nivel)."
            )
        except (TypeError, ValueError) as exc:
            print(f"  [Error] Al guardar preguntas para '{slug}': {exc}")

    print(f"\n¡Proceso de racionales finalizado! Se agregaron {total_pobladas} preguntas nuevas.")


if __name__ == "__main__":
    populate()

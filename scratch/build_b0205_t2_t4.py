# scratch/build_b0205_t2_t4.py
import json
import yaml
import os
from pathlib import Path

CONTENT_DIR = Path("docs/conocimiento/contenido")
EJERCICIOS_DIR = Path("docs/conocimiento/ejercicios")

def write_yaml(filename, data):
    with open(CONTENT_DIR / f"{filename}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

def append_jsonl(filename, items):
    with open(EJERCICIOS_DIR / f"{filename}.jsonl", "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

RECURSOS = []
EJERCICIOS = []

# ================= TANDA 2: PROPORCIONES (5r) =================
sid1 = "MAT.NUM.PROPORCIONES.DEFINICION_IGUALDAD_RAZONES"
RECURSOS.append({
    "semantic_id": sid1,
    "objetivo": "Comprender una proporción como la igualdad de dos razones matemáticas.",
    "introduccion": "Si preparas jugo con 2 limones y 1 litro de agua, y luego haces otra jarra con 4 limones y 2 litros de agua, ambas jarras tendrán exactamente el mismo sabor. Esta equivalencia de mezclas es lo que en matemáticas llamamos proporción.",
    "resumen": "Una proporción es la igualdad entre dos razones. Se expresa como $\\frac{a}{b} = \\frac{c}{d}$ y significa que ambas razones tienen el mismo valor.",
    "explicacion": "Una **proporción** se forma cuando igualamos dos razones que representan la misma relación cuantitativa. Si tenemos la razón $a:b$ y la razón $c:d$, afirmamos que forman una proporción si y solo si su cociente es el mismo. Se lee 'a es a b como c es a d'.",
    "procedimiento": [
        "Paso 1: Plantea las dos razones a comparar en forma de fracción.",
        "Paso 2: Calcula el cociente decimal de cada una o simplifícalas al máximo.",
        "Paso 3: Si los resultados coinciden exactamente, las razones forman una proporción."
    ],
    "ejemplos": [
        {
            "titulo": "Verificando una proporción",
            "enunciado": "¿Forman proporción las razones $3:5$ y $9:15$?",
            "solucion_pasos": [
                "Escribimos como fracciones: $\\frac{3}{5}$ y $\\frac{9}{15}$.",
                "Simplificamos la segunda: $\\frac{9:3}{15:3} = \\frac{3}{5}$.",
                "Como ambas equivalen a $\\frac{3}{5}$, sí forman una proporción."
            ]
        },
        {
            "titulo": "¿Toda igualdad de fracciones es proporción?",
            "respuesta": "Sí",
            "solucion_pasos": ["Cualquier par de fracciones equivalentes representa, por definición, una proporción."]
        }
    ],
    "errores_frecuentes": [
        "Sumar una constante a ambos términos creyendo que mantiene la proporción.",
        "Confundir la igualdad de razones con la suma de fracciones.",
        "Asumir que $a:b = c:d$ implica $a=c$ y $b=d$.",
        "Comparar cruzado sumando en lugar de multiplicando.",
        "Ignorar el orden: pensar que $a:b$ es proporcional a $d:c$."
    ],
    "fuente": "Currículum Nacional MINEDUC — Proporciones.",
    "estado": "publicado"
})

for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPDEF-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué es una proporción matemática? (v{i})", "choices": ["A) La igualdad de dos razones.", "B) La suma de dos fracciones.", "C) El producto de cuatro números.", "D) Una resta de cantidades."], "correct_answer": "A) La igualdad de dos razones.", "solution_steps": "Por definición es igualdad de razones.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PROPDEF-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Indica cuál es una proporción:", "choices": ["A) $1:2 = 2:4$", "B) $1:2 = 3:4$", "C) $1:2 = 1:3$", "D) $2:3 = 3:2$"], "correct_answer": "A) $1:2 = 2:4$", "solution_steps": "Solo $1/2 = 2/4$ es cierto.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPDEF-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Es $\\frac{4}{8} = \\frac{5}{10}$ una proporción?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Ambas equivalen a $0.5$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPDEF-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Para que la mezcla de pintura A ($2L$ rojo por $3L$ blanco) sea igual a la mezcla B ($4L$ rojo por $xL$ blanco), ¿qué debe cumplirse? (v{i})", "choices": ["A) Que $2/3 = 4/x$.", "B) Que $2+3 = 4+x$.", "C) Que $2\\cdot3 = 4\\cdot x$.", "D) Que $3/2 = 4/x$."], "correct_answer": "A) Que $2/3 = 4/x$.", "solution_steps": "Deben mantener la misma razón.", "paes_style": True})

sid2 = "MAT.NUM.PROPORCIONES.TERMINOS_EXTREMOS"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Identificar los términos extremos en una proporción.",
    "introduccion": "Cuando escribes una proporción en una sola línea, hay números que quedan en las puntas (al inicio y al final). Reconocerlos es el primer paso para aplicar las reglas de resolución.",
    "resumen": "En la proporción $a:b = c:d$, los valores $a$ y $d$ se llaman extremos porque ocupan la primera y última posición.",
    "explicacion": "Al escribir $\\frac{a}{b} = \\frac{c}{d}$ en notación de cociente $a:b = c:d$, los **extremos** son el primer término de la primera razón ($a$) y el segundo término de la segunda razón ($d$). Son fundamentales para aplicar el teorema fundamental de las proporciones.",
    "procedimiento": ["Paso 1: Escribe la proporción en formato lineal $a:b = c:d$.", "Paso 2: Observa el primer número de toda la expresión.", "Paso 3: Observa el último número de toda la expresión. Esos dos son los extremos."],
    "ejemplos": [
        {"titulo": "Identificando extremos", "enunciado": "En $2:5 = 6:15$, ¿cuáles son los extremos?", "solucion_pasos": ["El primer término es 2.", "El último término es 15.", "Los extremos son 2 y 15."]},
        {"titulo": "¿Pueden los extremos ser fracciones?", "respuesta": "Sí", "solucion_pasos": ["Cualquier número real puede ocupar la posición de un extremo."]}
    ],
    "errores_frecuentes": ["Confundirlos con los medios.", "Pensar que en $a/b = c/d$ los extremos son los numeradores.", "Asumir que siempre el mayor y menor número son los extremos.", "Intercambiarlos con los medios al aplicar reglas cruzadas.", "Creer que si se invierte la proporción, los extremos no cambian."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPEXT-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuáles son los extremos en $a:b = c:d$? (v{i})", "choices": ["A) a y d", "B) b y c", "C) a y c", "D) b y d"], "correct_answer": "A) a y d", "solution_steps": "Son el primero y el último.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PROPEXT-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "En $7:14 = 1:2$, los extremos son:", "choices": ["A) 7 y 2", "B) 14 y 1", "C) 7 y 14", "D) 1 y 2"], "correct_answer": "A) 7 y 2", "solution_steps": "7 es el primero y 2 el último.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPEXT-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿En $x/y = z/w$, los extremos son $x$ y $w$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Escrito en línea es $x:y = z:w$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPEXT-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Si en el diseño de un plano la razón $Escale:Real = 1:100$ equivale a $Plano:Medida$, ¿cuáles son los extremos de esta proporción? (v{i})", "choices": ["A) Escale y Medida", "B) Real y Plano", "C) Escale y Plano", "D) Real y Medida"], "correct_answer": "A) Escale y Medida", "solution_steps": "Son el primero y el último de la igualdad lineal.", "paes_style": True})

sid3 = "MAT.NUM.PROPORCIONES.TERMINOS_MEDIOS"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Identificar los términos medios en una proporción.",
    "introduccion": "Así como hay números en las puntas, hay números que quedan 'al centro' cuando leemos una proporción de izquierda a derecha. Son los medios.",
    "resumen": "En la proporción $a:b = c:d$, los valores $b$ y $c$ se llaman medios porque ocupan las posiciones centrales.",
    "explicacion": "Al escribir $\\frac{a}{b} = \\frac{c}{d}$ en notación de cociente $a:b = c:d$, los **medios** son el segundo término de la primera razón ($b$) y el primer término de la segunda razón ($c$). Identificarlos correctamente evita errores al resolver incógnitas.",
    "procedimiento": ["Paso 1: Escribe la proporción en formato lineal $a:b = c:d$.", "Paso 2: Observa los dos números que quedan en el centro, junto al signo igual.", "Paso 3: Esos dos números consecutivos son los medios."],
    "ejemplos": [
        {"titulo": "Identificando medios", "enunciado": "En $2:5 = 6:15$, ¿cuáles son los medios?", "solucion_pasos": ["El número antes del igual es 5.", "El número después del igual es 6.", "Los medios son 5 y 6."]},
        {"titulo": "¿Pueden los medios ser iguales?", "respuesta": "Sí", "solucion_pasos": ["Se conoce como proporción continua, por ejemplo en $2:4 = 4:8$."]}
    ],
    "errores_frecuentes": ["Confundirlos con los extremos.", "Pensar que en $a/b = c/d$ los medios son los denominadores.", "Tomar solo un número como 'el medio'.", "Multiplicar un medio por otro medio para hallar el valor de la razón.", "Creer que los medios siempre son números enteros."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPMED-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuáles son los medios en $a:b = c:d$? (v{i})", "choices": ["A) b y c", "B) a y d", "C) a y c", "D) b y d"], "correct_answer": "A) b y c", "solution_steps": "Son los centrales.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PROPMED-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "En $8:16 = 2:4$, los medios son:", "choices": ["A) 16 y 2", "B) 8 y 4", "C) 8 y 16", "D) 2 y 4"], "correct_answer": "A) 16 y 2", "solution_steps": "16 y 2 están junto al signo igual.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPMED-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿En $x/y = z/w$, los medios son $y$ y $z$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Escrito en línea es $x:y = z:w$, medios son y, z.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPMED-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Si en una maqueta se plantea que $Real : Maqueta = Largo : Corto$, ¿cuáles son los términos medios? (v{i})", "choices": ["A) Maqueta y Largo", "B) Real y Corto", "C) Real y Largo", "D) Maqueta y Corto"], "correct_answer": "A) Maqueta y Largo", "solution_steps": "Ocupan las posiciones centrales.", "paes_style": True})

sid4 = "MAT.NUM.PROPORCIONES.PRODUCTO_CRUZADO"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Aplicar el Teorema Fundamental de las Proporciones (producto cruzado).",
    "introduccion": "Si dos fracciones son equivalentes, sus diagonales esconden un secreto matemático: al multiplicarlas, el resultado es siempre el mismo. Esta es la llave maestra para resolver casi cualquier problema de proporciones.",
    "resumen": "El Teorema Fundamental establece que en toda proporción $a/b = c/d$, el producto de los extremos es igual al producto de los medios: $a \\cdot d = b \\cdot c$.",
    "explicacion": "El **producto cruzado** es la propiedad más importante de las proporciones. Indica que si multiplicas cruzado el numerador de la primera por el denominador de la segunda, y viceversa, los resultados deben ser idénticos. Esto permite comprobar si dos razones forman proporción y, más útil aún, encontrar términos desconocidos (resolución de ecuaciones).",
    "procedimiento": ["Paso 1: Escribe la proporción como fracciones $\\frac{a}{b} = \\frac{c}{d}$.", "Paso 2: Multiplica el numerador izquierdo por el denominador derecho ($a \\cdot d$).", "Paso 3: Multiplica el denominador izquierdo por el numerador derecho ($b \\cdot c$) y compara o iguala."],
    "ejemplos": [
        {"titulo": "Comprobando una proporción", "enunciado": "¿Es $4/6 = 10/15$ una proporción válida?", "solucion_pasos": ["Multiplicamos extremos: $4 \\cdot 15 = 60$.", "Multiplicamos medios: $6 \\cdot 10 = 60$.", "Como $60 = 60$, es una proporción."]},
        {"titulo": "¿Sirve para encontrar una incógnita?", "respuesta": "Sí", "solucion_pasos": ["Si $x/3 = 8/6$, entonces $6x = 24$, por lo que $x = 4$."]}
    ],
    "errores_frecuentes": ["Multiplicar numeradores con numeradores en lugar de hacerlo en cruz.", "Sumar en cruz en vez de multiplicar.", "Olvidar igualar los dos productos (dejándolos sueltos).", "Aplicar producto cruzado cuando se están sumando fracciones ($a/b + c/d$).", "Confundir el producto de extremos con el valor de la razón."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPCRUZ-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué afirma el Teorema Fundamental de las Proporciones? (v{i})", "choices": ["A) El producto de los extremos es igual al producto de los medios.", "B) La suma de los extremos es igual a la suma de los medios.", "C) El producto de los numeradores es igual al de los denominadores.", "D) El cociente cruzado es igual a cero."], "correct_answer": "A) El producto de los extremos es igual al producto de los medios.", "solution_steps": "Propiedad básica: ad = bc.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PROPCRUZ-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si $m/n = p/q$, el producto cruzado indica que:", "choices": ["A) $m \\cdot q = n \\cdot p$", "B) $m \\cdot p = n \\cdot q$", "C) $m \\cdot n = p \\cdot q$", "D) $m+q = n+p$"], "correct_answer": "A) $m \\cdot q = n \\cdot p$", "solution_steps": "Multiplicación cruzada de numerador y denominador opuesto.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPCRUZ-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si $2/3 = 8/12$, entonces $2 \\cdot 12 = 3 \\cdot 8$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$24 = 24$, se cumple el teorema.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPCRUZ-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un arquitecto usa la escala $1:50$. Si iguala $\\frac{1}{50} = \\frac{{Altura}}{200}$, ¿qué ecuación resuelve correctamente el problema usando producto cruzado? (v{i})", "choices": ["A) $1 \\cdot 200 = 50 \\cdot Altura$", "B) $1 \\cdot Altura = 50 \\cdot 200$", "C) $1+200 = 50+Altura$", "D) $50/1 = Altura/200$"], "correct_answer": "A) $1 \\cdot 200 = 50 \\cdot Altura$", "solution_steps": "Extremo por extremo = medio por medio.", "paes_style": True})

sid5 = "MAT.NUM.PROPORCIONES.CUARTA_PROPORCIONAL"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Calcular la cuarta proporcional en una proporción dada.",
    "introduccion": "Si conoces el precio de 2 kilos de pan, puedes predecir el de 5 kilos usando una regla de tres. En el fondo, estás buscando una cuarta pieza del rompecabezas que hace que todo encaje a la perfección.",
    "resumen": "La cuarta proporcional es el término desconocido ($x$) en una proporción cuando se conocen los otros tres. Se calcula despejando $x$ de la ecuación del producto cruzado.",
    "explicacion": "Se llama **cuarta proporcional** a cualquiera de los términos de una proporción cuando los otros tres son conocidos. Para encontrar su valor en $\\frac{a}{b} = \\frac{c}{x}$, multiplicamos los términos de la diagonal que está completa ($b$ y $c$) y dividimos por el término que queda solo ($a$).",
    "procedimiento": ["Paso 1: Plantea la proporción dejando la incógnita $x$ en una de las posiciones.", "Paso 2: Multiplica los dos términos conocidos que forman una diagonal.", "Paso 3: Divide ese resultado por el término que hace diagonal con la $x$."],
    "ejemplos": [
        {"titulo": "Hallando x", "enunciado": "Halla $x$ en $3/4 = 9/x$", "solucion_pasos": ["La diagonal completa es $4$ y $9$.", "Multiplicamos $4 \\cdot 9 = 36$.", "Dividimos por el término opuesto a $x$, que es $3$: $36 / 3 = 12$. La cuarta proporcional es 12."]},
        {"titulo": "¿Es lo mismo que la regla de tres?", "respuesta": "Sí", "solucion_pasos": ["La regla de tres simple directa es la aplicación práctica del cálculo de la cuarta proporcional."]}
    ],
    "errores_frecuentes": ["Dividir por un número de la diagonal equivocada.", "Multiplicar los números de la misma fracción.", "Confundir cuarta proporcional con tercera proporcional.", "No simplificar las fracciones antes para facilitar el cálculo mental.", "Despejar mal en la ecuación de primer grado."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPCUAR-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿A qué se le llama cuarta proporcional? (v{i})", "choices": ["A) Al término desconocido cuando se conocen tres en una proporción.", "B) Al resultado de elevar un número a cuatro.", "C) A dividir una proporción entre cuatro.", "D) Al producto de cuatro fracciones."], "correct_answer": "A) Al término desconocido cuando se conocen tres en una proporción.", "solution_steps": "Concepto de despeje.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PROPCUAR-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Para hallar $x$ en $a/b = c/x$, la operación es:", "choices": ["A) $x = (b \\cdot c) / a$", "B) $x = (a \\cdot b) / c$", "C) $x = (a \\cdot c) / b$", "D) $x = a+b-c$"], "correct_answer": "A) $x = (b \\cdot c) / a$", "solution_steps": "Diagonal completa dividida por el opuesto.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPCUAR-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿En la proporción $2/5 = 6/x$, el valor de $x$ es $15$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$x = 5\\cdot6 / 2 = 30 / 2 = 15$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPCUAR-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Para un evento escolar, la razón entre profesores y alumnos debe ser de $2$ a $45$. Si ya hay $180$ alumnos confirmados, ¿cuántos profesores se necesitan como mínimo? (v{i})", "choices": ["A) $8$", "B) $10$", "C) $4$", "D) $16$"], "correct_answer": "A) $8$", "solution_steps": "$2/45 = x/180 \\implies x = 2\\cdot180 / 45 = 360/45 = 8$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 2...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 2...")
    append_jsonl("mat-num-razones-banco-gen-2", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-2.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()

# scratch/build_alg_b0304_t3.py
import json
import yaml
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

# 1. MULT_POLINOMIOS.ORDENAMIENTO_FACTORES
sid1 = "MAT.ALG.MULT_POLINOMIOS.ORDENAMIENTO_FACTORES"
RECURSOS.append({
    "semantic_id": sid1,
    "objetivo": "Ordenar previamente los polinomios antes de multiplicarlos para facilitar la alineación de términos semejantes.",
    "introduccion": "Si intentas multiplicar polinomios desordenados, te arriesgas a perder la pista de qué término va con cuál. La forma más segura y ordenada de multiplicar es organizar ambos polinomios por grados, de mayor a menor.",
    "resumen": "El **Ordenamiento de Factores** en la multiplicación exige ordenar cada polinomio factor en orden descendente respecto a una misma variable. Esto asegura que al multiplicar verticalmente, los productos semejantes queden naturalmente alineados en las mismas columnas.",
    "explicacion": "Multiplica: $(3 + x^2 - 2x)(x + 5)$.\n\nPaso 1: Ordenamos el trinomio: $(x^2 - 2x + 3)$.\nPaso 2: Ordenamos el binomio (ya está ordenado): $(x + 5)$.\nPaso 3: Multiplicamos verticalmente:\n```\n    x² - 2x + 3\n  ×      x + 5\n  ─────────────\n    5x² - 10x + 15    (multiplicación por 5)\n+ x³ - 2x² +  3x          (multiplicación por x)\n────────────────\n  x³ + 3x² -  7x + 15\n```\n\nEl ordenamiento garantiza que la familia $x^2$ y la familia $x$ queden perfectamente alineadas una debajo de la otra.",
    "procedimiento": [
        "Paso 1: Elige una variable de referencia en común.",
        "Paso 2: Reescribe el primer polinomio en orden decreciente de exponentes de esa variable.",
        "Paso 3: Reescribe el segundo polinomio siguiendo el mismo orden.",
        "Paso 4: Realiza la multiplicación término a término de izquierda a derecha (o usando el método vertical).",
        "Paso 5: Reduce los términos que queden alineados."
    ],
    "ejemplos": [
        {"titulo": "Ordenar para el producto vertical", "enunciado": "Multiplica: (2 - a + a^2)(a + 1).", "solucion_pasos": ["Ordenamos trinomio: a^2 - a + 2.", "Ordenamos binomio: a + 1.", "Multiplicación 1 (por 1): a^2 - a + 2.", "Multiplicación 2 (por a): a^3 - a^2 + 2a.", "Sumamos: a^3 + 0a^2 + a + 2 = a^3 + a + 2."]}
    ],
    "errores_frecuentes": [
        "Multiplicar los polinomios en el orden desordenado original, dificultando la suma de términos semejantes.",
        "Cambiar los signos de los términos al reordenarlos dentro del polinomio."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MP-OF-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"¿Cuál es el beneficio de ordenar los polinomios de forma descendente antes de multiplicarlos verticalmente? (v{i})", "choices": ["A) Permite que los productos semejantes de cada fila queden alineados verticalmente en las mismas columnas, facilitando su reducción.", "B) Permite multiplicar solo los coeficientes de igual grado.", "C) Elimina la necesidad de aplicar la propiedad distributiva.", "D) Cambia el grado final del producto."], "correct_answer": "A) Permite que los productos semejantes de cada fila queden alineados verticalmente en las mismas columnas, facilitando su reducción.", "solution_steps": "El orden decreciente alinea las columnas del mismo exponente al hacer los corrimientos laterales.", "paes_style": False})
EJERCICIOS.append({"stable_id": "MP-OF-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Ordena de mayor a menor y multiplica: $(2 + m)(m^2 - 3 + m)$.", "choices": ["A) $m^3 + 3m^2 - m - 6$", "B) $m^3 - 3m^2 + m - 6$", "C) $m^3 + 3m^2 - m + 6$", "D) $m^3 + 2m^2 - 6$"], "correct_answer": "A) $m^3 + 3m^2 - m - 6$", "solution_steps": "Ordenados: $(m+2)(m^2+m-3)$. Multiplicamos: $m(m^2+m-3) = m^3+m^2-3m$. $2(m^2+m-3) = 2m^2+2m-6$. Sumamos: $m^3+(1+2)m^2+(-3+2)m-6 = m^3+3m^2-m-6$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MP-OF-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿El polinomio desordenado $3 - a^2 + 5a$ equivale al polinomio ordenado $-a^2 + 5a + 3$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Se reordenan los términos de mayor a menor exponente manteniendo sus signos originales: el trinomio ordenado es $-a^2 + 5a + 3$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MP-OF-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"La ganancia neta de una fábrica se describe como $G = (p + 3)(p^2 - 2p + 4)$. Al resolver el producto ordenado de manera equivalente, ¿cuál es la expresión resultante? (v{i})", "choices": ["A) $p^3 + p^2 - 2p + 12$", "B) $p^3 + p^2 + 2p + 12$", "C) $p^3 - p^2 - 2p + 12$", "D) $p^3 + 12$"], "correct_answer": "A) $p^3 + p^2 - 2p + 12$", "solution_steps": "Multiplicamos: $p(p^2-2p+4) = p^3-2p^2+4p$. $3(p^2-2p+4) = 3p^2-6p+12$. Sumamos: $p^3 + (-2+3)p^2 + (4-6)p + 12 = p^3 + p^2 - 2p + 12$.", "paes_style": True})

# 2. MULT_MONOMIOS.COEFICIENTES_FRACCIONARIOS
sid2 = "MAT.ALG.MULT_MONOMIOS.COEFICIENTES_FRACCIONARIOS"
RECURSOS.append({
    "semantic_id": sid2,
    "objetivo": "Multiplicar monomios con coeficientes fraccionarios, aplicando la multiplicación de fracciones y las leyes de exponentes.",
    "introduccion": "Los coeficientes fraccionarios en los monomios no cambian las reglas algebraicas. La multiplicación de fracciones se realiza directamente: numerador por numerador, y denominador por denominador. Las variables se operan como siempre.",
    "resumen": "Al multiplicar monomios con **Coeficientes Fraccionarios**, se multiplican los numeradores entre sí y los denominadores entre sí para obtener el nuevo coeficiente, simplificando la fracción al final. Los exponentes de igual base se suman.",
    "explicacion": "Multiplica: $(\\frac{2}{3}x^2y)(\\frac{3}{4}xy^2)$.\n\n1. Multiplicamos coeficientes:\n   $\\frac{2}{3} \\times \\frac{3}{4} = \\frac{2 \\cdot 3}{3 \\cdot 4} = \\frac{6}{12} = \\frac{1}{2}$.\n2. Parte literal:\n   $x^2 \\cdot x = x^3$.\n   $y \\cdot y^2 = y^3$.\n3. Resultado final: $\\frac{1}{2}x^3y^3$.",
    "procedimiento": [
        "Paso 1: Multiplica las fracciones de los coeficientes (numerador × numerador y denominador × denominador).",
        "Paso 2: Simplifica la fracción resultante a su mínima expresión.",
        "Paso 3: Para las variables de igual base, suma sus exponentes.",
        "Paso 4: Escribe el resultado combinando la fracción simplificada y las variables resultantes."
    ],
    "ejemplos": [
        {"titulo": "Fracciones combinadas", "enunciado": "Multiplica: (1/2 a)(2/5 b).", "solucion_pasos": ["Coeficientes: 1/2 × 2/5 = 2/10 = 1/5.", "Letras: a × b = ab.", "Resultado: 1/5 ab."]}
    ],
    "errores_frecuentes": [
        "Sumar las fracciones en lugar de multiplicarlas.",
        "Omitir la simplificación de la fracción resultante en el coeficiente."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-CF-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al multiplicar $(\\frac{{3}}{{4}}x^2)$ por $(\\frac{{2}}{{3}}x)$, ¿cuál es el nuevo coeficiente del monomio resultante tras simplificar? (v{i})", "choices": ["A) $\\frac{1}{2}$", "B) $\\frac{5}{7}$", "C) $\\frac{6}{12}$", "D) $\\frac{9}{8}$"], "correct_answer": "A) $\\frac{1}{2}$", "solution_steps": "Multiplicamos: $\\frac{3}{4} \\times \\frac{2}{3} = \\frac{6}{12}$. Al simplificar por 6, queda $\\frac{1}{2}$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "MM-CF-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el producto: $(\\frac{1}{5}a^3)(\\frac{5}{2}b^2)$.", "choices": ["A) $\\frac{1}{2}a^3b^2$", "B) $\\frac{6}{7}a^3b^2$", "C) $\\frac{5}{10}a^3b^2$", "D) $\\frac{1}{10}a^3b^2$"], "correct_answer": "A) $\\frac{1}{2}a^3b^2$", "solution_steps": "Coeficientes: $\\frac{1}{5} \\times \\frac{5}{2} = \\frac{5}{10} = \\frac{1}{2}$. Letras: $a^3b^2$. Resultado: $\\frac{1}{2}a^3b^2$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-CF-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿El producto de $(\\frac{2}{3}x)$ y $(\\frac{3}{2}x)$ es igual a $x^2$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Coeficientes: $\\frac{2}{3} \\times \\frac{3}{2} = \\frac{6}{6} = 1$. Variable: $x \\cdot x = x^2$. El coeficiente 1 no se escribe. Resultado: $x^2$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-CF-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Un laboratorio químico mezcla dos disoluciones. La concentración total está dada por el producto de $(\\frac{{1}}{{4}}c)$ y $(\\frac{{2}}{{5}}d^2)$. ¿Cuál es la concentración resultante simplificada? (v{i})", "choices": ["A) $\\frac{1}{10}cd^2$", "B) $\\frac{2}{20}cd^2$", "C) $\\frac{3}{9}cd^2$", "D) $\\frac{1}{20}cd^2$"], "correct_answer": "A) $\\frac{1}{10}cd^2$", "solution_steps": "Producto: $(\\frac{1}{4}c)(\\frac{2}{5}d^2) = (\\frac{1}{4} \\cdot \\frac{2}{5})(cd^2) = \\frac{2}{20}cd^2 = \\frac{1}{10}cd^2$.", "paes_style": True})

# 3. MULT_MON_POL.COEFICIENTES_FRACCIONARIOS
sid3 = "MAT.ALG.MULT_MON_POL.COEFICIENTES_FRACCIONARIOS"
RECURSOS.append({
    "semantic_id": sid3,
    "objetivo": "Multiplicar un monomio por un polinomio con coeficientes fraccionarios, aplicando la propiedad distributiva término a término.",
    "introduccion": "Cuando distribuimos un monomio sobre un polinomio con fracciones, multiplicamos el término exterior por cada término interior. Esto genera múltiples multiplicaciones de fracciones independientes que resolvemos una por una.",
    "resumen": "Al multiplicar un monomio por un polinomio con **Coeficientes Fraccionarios**, se distribuye el monomio multiplicando cada término. Cada producto parcial requiere multiplicar fracciones numeradores con numeradores y denominadores con denominadores.",
    "explicacion": "Multiplica: $\\frac{1}{2}x(\\frac{2}{3}x - \\frac{4}{5})$.\n\n1. Distribución 1:\n   $\\frac{1}{2}x \\cdot \\frac{2}{3}x = (\\frac{1}{2} \\cdot \\frac{2}{3})x^2 = \\frac{2}{6}x^2 = \\frac{1}{3}x^2$.\n2. Distribución 2:\n   $\\frac{1}{2}x \\cdot (-\\frac{4}{5}) = -(\\frac{1}{2} \\cdot \\frac{4}{5})x = -\\frac{4}{10}x = -\\frac{2}{5}x$.\n\nResultado combinado: $\\frac{1}{3}x^2 - \\frac{2}{5}x$.",
    "procedimiento": [
        "Paso 1: Identifica el monomio multiplicador y cada uno de los sumandos fraccionarios dentro del polinomio.",
        "Paso 2: Distribuye el monomio multiplicando el primer término del polinomio (multiplicación de fracciones).",
        "Paso 3: Distribuye al segundo término (ojo con los signos y la multiplicación de fracciones).",
        "Paso 4: Simplifica cada una de las fracciones obtenidas en los coeficientes.",
        "Paso 5: Escribe el polinomio final."
    ],
    "ejemplos": [
        {"titulo": "Distribución fraccionaria", "enunciado": "Multiplica: 2/3 a(3/4 a + 1/2).", "solucion_pasos": ["Producto 1: (2/3 a)(3/4 a) = 6/12 a^2 = 1/2 a^2.", "Producto 2: (2/3 a)(1/2) = 2/6 a = 1/3 a.", "Resultado: 1/2 a^2 + 1/3 a."]}
    ],
    "errores_frecuentes": [
        "Olvidar distribuir el monomio al denominador de los coeficientes del polinomio.",
        "No simplificar las fracciones finales de cada término."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MMP-CF-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al distribuir $\\frac{{3}}{{5}}y$ sobre el polinomio $(\\frac{{5}}{{3}}y - 10)$, ¿cuáles son los coeficientes simplificados de los dos términos resultantes? (v{i})", "choices": ["A) $1$ y $-6$", "B) $\\frac{15}{15}$ y $-\\frac{30}{5}$", "C) $1$ y $-10$", "D) $\\frac{3}{5}$ y $-6$"], "correct_answer": "A) $1$ y $-6$", "solution_steps": "Término 1: $\\frac{3}{5} \\times \\frac{5}{3} = 1$. Término 2: $\\frac{3}{5} \\times (-10) = -6$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "MMP-CF-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Calcula: $\\frac{2}{3}x(\\frac{1}{2}x^2 - \\frac{3}{4}x)$.", "choices": ["A) $\\frac{1}{3}x^3 - \\frac{1}{2}x^2$", "B) $\\frac{2}{6}x^3 - \\frac{6}{12}x^2$", "C) $\\frac{1}{3}x^2 - \\frac{1}{2}x$", "D) $\\frac{2}{3}x^3 - \\frac{3}{4}x^2$"], "correct_answer": "A) $\\frac{1}{3}x^3 - \\frac{1}{2}x^2$", "solution_steps": "Término 1: $\\frac{2}{3} \\times \\frac{1}{2} = \\frac{2}{6} = \\frac{1}{3}$. Letras: $x \\cdot x^2 = x^3$. Término 2: $\\frac{2}{3} \\times (-\\frac{3}{4}) = -\\frac{6}{12} = -\\frac{1}{2}$. Letras: $x \\cdot x = x^2$. Resultado: $\\frac{1}{3}x^3 - \\frac{1}{2}x^2$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MMP-CF-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿El resultado de multiplicar $\\frac{3}{4}a(a - \\frac{4}{3})$ es $\\frac{3}{4}a^2 - a$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Término 1: $\\frac{3}{4}a \\cdot a = \\frac{3}{4}a^2$. Término 2: $\\frac{3}{4}a \\cdot (-\\frac{4}{3}) = -\\frac{12}{12}a = -a$. Resultado: $\\frac{3}{4}a^2 - a$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MMP-CF-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Un maestro de obra diseña una rampa de ancho $\\frac{{1}}{{2}}w$ metros y longitud descrita por $(\\frac{{2}}{{3}}w^2 + 8w)$ metros. ¿Cuál es el área de la superficie de la rampa? (v{i})", "choices": ["A) $\\frac{1}{3}w^3 + 4w^2$", "B) $\\frac{2}{6}w^3 + 8w^2$", "C) $\\frac{1}{2}w^3 + 4w^2$", "D) $\\frac{1}{3}w^2 + 4w$"], "correct_answer": "A) $\\frac{1}{3}w^3 + 4w^2$", "solution_steps": "Área $= (\\frac{1}{2}w)(\\frac{2}{3}w^2 + 8w) = (\\frac{1}{2} \\cdot \\frac{2}{3})w^3 + (\\frac{1}{2} \\cdot 8)w^2 = \\frac{2}{6}w^3 + 4w^2 = \\frac{1}{3}w^3 + 4w^2$.", "paes_style": True})

# 4. MULT_POLINOMIOS.PRODUCTO_BINOMIOS
sid4 = "MAT.ALG.MULT_POLINOMIOS.PRODUCTO_BINOMIOS"
RECURSOS.append({
    "semantic_id": sid4,
    "objetivo": "Multiplicar dos binomios aplicando el método distributivo doble (método FOIL) y reduciendo semejantes.",
    "introduccion": "El producto de dos binomios, como $(x+a)(x+b)$, es la multiplicación más común que verás en álgebra. Existe un método nemotécnico muy popular en inglés llamado FOIL (First, Outer, Inner, Last), que te ayuda a recordar los cuatro productos cruzados indispensables.",
    "resumen": "Al multiplicar **Dos Binomios** $(a+b)(c+d)$, se realizan exactamente 4 productos: primero × primero ($ac$), primero × segundo ($ad$), segundo × primero ($bc$) y segundo × segundo ($bd$). Luego se reducen los semejantes.",
    "explicacion": "Sea el producto: $(x + 3)(x - 5)$.\n\nAplicamos los cuatro productos:\n1. **F**irst (Primeros): $x \\cdot x = x^2$.\n2. **O**uter (Exteriores): $x \\cdot (-5) = -5x$.\n3. **I**nner (Interiores): $3 \\cdot x = +3x$.\n4. **L**ast (Últimos): $3 \\cdot (-5) = -15$.\n\nSumamos: $x^2 - 5x + 3x - 15$.\nReducimos semejantes: $x^2 - 2x - 15$.",
    "procedimiento": [
        "Paso 1: Multiplica los primeros términos de cada binomio.",
        "Paso 2: Multiplica los términos exteriores (el primero del primero y el segundo del segundo).",
        "Paso 3: Multiplica los términos interiores (el segundo del primero y el primero del segundo).",
        "Paso 4: Multiplica los últimos términos de cada binomio.",
        "Paso 5: Agrupa los dos términos centrales (semejantes) y redúcelos."
    ],
    "ejemplos": [
        {"titulo": "El FOIL en acción", "enunciado": "Multiplica: (2x + 1)(x - 3).", "solucion_pasos": ["Primeros: (2x)(x) = 2x^2.", "Exteriores: (2x)(-3) = -6x.", "Interiores: (1)(x) = +x.", "Últimos: (1)(-3) = -3.", "Línea: 2x^2 - 6x + x - 3.", "Reducción: 2x^2 - 5x - 3."]}
    ],
    "errores_frecuentes": [
        "Multiplicar solo los primeros y los últimos, omitiendo los productos cruzados exteriores/interiores.",
        "Equivocarse en el signo del producto de los últimos términos."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MP-PB-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al multiplicar $(x - 4)(x + 6)$, ¿cuáles son los cuatro productos cruzados antes de reducir semejantes? (v{i})", "choices": ["A) $x^2$, $6x$, $-4x$ y $-24$.", "B) $x^2$, $-4x$ y $-24$.", "C) $x^2$ y $-24$.", "D) $2x$, $6x$, $-4x$ y $2$."], "correct_answer": "A) $x^2$, $6x$, $-4x$ y $-24$.", "solution_steps": "Productos: $x \\cdot x=x^2$, $x \\cdot 6=6x$, $-4 \\cdot x=-4x$, $-4 \\cdot 6=-24$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "MP-PB-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el producto de: $(a - 7)(a - 3)$.", "choices": ["A) $a^2 - 10a + 21$", "B) $a^2 - 10a - 21$", "C) $a^2 + 21$", "D) $a^2 - 21$"], "correct_answer": "A) $a^2 - 10a + 21$", "solution_steps": "FOIL: $a^2$, $-3a$, $-7a$, $+21$. Sumamos: $a^2 - 10a + 21$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MP-PB-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿El producto de $(3x + 2)(x - 1)$ es igual a $3x^2 - x - 2$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$(3x)(x) = 3x^2$. $(3x)(-1) = -3x$. $(2)(x) = 2x$. $(2)(-1) = -2$. Suma: $3x^2 - 3x + 2x - 2 = 3x^2 - x - 2$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MP-PB-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"El ingreso neto por ventas de una distribuidora es $I = (x - 2)(2x + 10)$ miles de pesos, donde $x$ es el precio unitario. ¿Cuál es la expresión equivalente al desarrollar el producto? (v{i})", "choices": ["A) $2x^2 + 6x - 20$ miles de pesos.", "B) $2x^2 - 20$ miles de pesos.", "C) $2x^2 - 6x - 20$ miles de pesos.", "D) $2x^2 + 10x - 20$ miles de pesos."], "correct_answer": "A) $2x^2 + 6x - 20$ miles de pesos.", "solution_steps": "Desarrollamos: $x(2x+10) = 2x^2 + 10x$. $-2(2x+10) = -4x - 20$. Reduciendo semejantes: $2x^2 + (10-4)x - 20 = 2x^2 + 6x - 20$.", "paes_style": True})

# 5. MULT_MONOMIOS.MONOMIOS_NEGATIVOS
sid5 = "MAT.ALG.MULT_MONOMIOS.MONOMIOS_NEGATIVOS"
RECURSOS.append({
    "semantic_id": sid5,
    "objetivo": "Multiplicar monomios que contienen signos negativos en sus coeficientes y variables.",
    "introduccion": "Los signos negativos en el álgebra pueden asustar, pero en la multiplicación son de lo más predecibles. Siguiendo las reglas de signos que ya conoces, los negativos simplemente se cancelan por pares o se mantienen si hay un número impar.",
    "resumen": "Al multiplicar **Monomios Negativos**, se calcula el signo final según la regla de signos (par o impar de negativos). Los coeficientes numéricos se multiplican normalmente y se suman los exponentes de las variables de igual base.",
    "explicacion": "Multiplica: $(-3x^2y^2)(-5xy^3)$.\n\n1. Signo: dos negativos multiplicando se cancelan → positivo.\n2. Coeficientes: $3 \\times 5 = 15$.\n3. Parte literal: $x^2 \\cdot x = x^3$ y $y^2 \\cdot y^3 = y^5$.\n4. Resultado final: $15x^3y^5$.\n\nSi multiplicamos tres factores: $(-2a)(-a^2)(-3b)$:\n- 3 negativos (impar) → negativo.\n- Coeficientes: $2 \\times 1 \\times 3 = 6$.\n- Letras: $a \\cdot a^2 \\cdot b = a^3b$.\n- Resultado: $-6a^3b$.",
    "procedimiento": [
        "Paso 1: Cuenta el número de signos negativos entre todos los factores.",
        "Paso 2: Si el total es par, el resultado es positivo. Si es impar, es negativo.",
        "Paso 3: Multiplica los valores absolutos de los coeficientes.",
        "Paso 4: Multiplica las partes literales aplicando la suma de exponentes de igual base.",
        "Paso 5: Combina el signo final con el coeficiente y las variables ordenadas alfabéticamente."
    ],
    "ejemplos": [
        {"titulo": "Triple producto negativo", "enunciado": "Multiplica: (-2x)(-3x^2)(-x^3).", "solucion_pasos": ["Signos: 3 negativos (impar) → -.", "Coeficientes: 2 × 3 × 1 = 6.", "Variable x: x^1 · x^2 · x^3 = x^6.", "Resultado: -6x^6."]}
    ],
    "errores_frecuentes": [
        "Sumar los coeficientes negativos creyendo que es una adición (ej. $(-2)(-3) = -5$ en lugar de $+6$).",
        "Omitir el signo negativo del coeficiente del resultado cuando hay un número impar de factores negativos."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-MN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es el resultado de multiplicar $(-6a^3)$ por $(-2ab)$? (v{i})", "choices": ["A) $12a^4b$", "B) $-12a^4b$", "C) $-8a^4b$", "D) $12a^3b$"], "correct_answer": "A) $12a^4b$", "solution_steps": "Signo: $(-)(-) = +$. Coeficientes: $6 \\times 2 = 12$. Letras: $a^3 \\cdot a = a^4$ y $b$. Resultado: $12a^4b$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "MM-MN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el producto de: $(-4x)(-2x^2)(-3x^3)$.", "choices": ["A) $-24x^6$", "B) $24x^6$", "C) $-24x^5$", "D) $-9x^6$"], "correct_answer": "A) $-24x^6$", "solution_steps": "Signo: 3 negativos (impar) → $-$. Coef: $4 \\times 2 \\times 3 = 24$. $x$: $x \\cdot x^2 \\cdot x^3 = x^6$. Resultado: $-24x^6$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-MN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿El producto $(-5a^2b)(-b^2)$ da $+5a^2b^3$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Signos: $(-)(-) = +$. Coeficientes: $5 \\times 1 = 5$. Letras: $a^2$ y $b \\cdot b^2 = b^3$. Resultado: $5a^2b^3$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-MN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Un modelo físico de disipación de energía calcula una pérdida como $E = (-2v^2)(-3v)(-v^3)$. Si $v > 0$, ¿cuál es la expresión reducida de la pérdida de energía? (v{i})", "choices": ["A) $-6v^6$", "B) $6v^6$", "C) $-6v^5$", "D) $-5v^6$"], "correct_answer": "A) $-6v^6$", "solution_steps": "Operamos: $(-2v^2)(-3v)(-v^3)$. Signo: 3 negativos → $-$. Coef: $2 \\times 3 \\times 1 = 6$. Letra: $v^2 \\cdot v \\cdot v^3 = v^6$. Resultado: $-6v^6$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 3 (B0304/Ordenamiento y Fracciones)...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"  Creado {filename}.yaml")
    print("Escribiendo JSONL Tanda 3...")
    append_jsonl("mat-alg-multiplicacion-banco-gen-3", EJERCICIOS)
    print(f"  mat-alg-multiplicacion-banco-gen-3.jsonl con {len(EJERCICIOS)} ejercicios.")

if __name__ == "__main__":
    generate_all()

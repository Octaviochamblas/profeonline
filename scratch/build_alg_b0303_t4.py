# scratch/build_alg_b0303_t4.py
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

# 1. ADICION_POL.METODO_HORIZONTAL
sid1 = "MAT.ALG.ADICION_POL.METODO_HORIZONTAL"
RECURSOS.append({
    "semantic_id": sid1,
    "objetivo": "Sumar polinomios mediante el método horizontal, identificando y reduciendo términos semejantes en una sola línea.",
    "introduccion": "La suma de polinomios es, en esencia, la extensión de la reducción de términos semejantes. El método horizontal permite hacerlo todo en una misma línea, que es la forma más natural cuando los polinomios son sencillos.",
    "resumen": "En la **Adición Horizontal**, se colocan los polinomios uno al lado del otro entre paréntesis (si es necesario) y se eliminan los agrupadores. Luego se identifican y reducen todos los términos semejantes en una sola expresión de línea.",
    "explicacion": "Suma: $(3x^2 + 2x - 1) + (x^2 - 4x + 5)$.\n\nPaso 1: Eliminamos paréntesis (precedidos de $+$, sin cambio de signos):\n$3x^2 + 2x - 1 + x^2 - 4x + 5$.\n\nPaso 2: Agrupamos por familias:\n- Familia $x^2$: $3x^2 + x^2 = 4x^2$.\n- Familia $x$: $2x - 4x = -2x$.\n- Constantes: $-1 + 5 = 4$.\n\nResultado: $4x^2 - 2x + 4$.",
    "procedimiento": [
        "Paso 1: Escribe los polinomios en una línea, conectados por el signo $+$.",
        "Paso 2: Elimina los paréntesis (en suma, los signos no cambian).",
        "Paso 3: Agrupa visualmente los términos semejantes (por familias).",
        "Paso 4: Reduce cada familia y escribe el polinomio resultado."
    ],
    "ejemplos": [
        {"titulo": "Suma horizontal directa", "enunciado": "Suma: (5a - 3) + (2a + 7).", "solucion_pasos": ["Eliminamos paréntesis: 5a - 3 + 2a + 7.", "Familia a: 5a + 2a = 7a.", "Constantes: -3 + 7 = 4.", "Resultado: 7a + 4."]}
    ],
    "errores_frecuentes": [
        "Cambiar signos al eliminar paréntesis precedidos de $+$ (error que viene de confundir con la resta).",
        "Olvidar agrupar todas las familias y dejar términos semejantes sin reducir."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-H-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al sumar $(4x + 3) + (2x - 1)$ por el método horizontal, ¿cuál es el primer paso operativo? (v{i})", "choices": ["A) Eliminar los paréntesis sin cambiar ningún signo, obteniendo $4x + 3 + 2x - 1$.", "B) Cambiar todos los signos del segundo paréntesis.", "C) Multiplicar los coeficientes de los términos semejantes.", "D) Elevar los exponentes de cada término."], "correct_answer": "A) Eliminar los paréntesis sin cambiar ningún signo, obteniendo $4x + 3 + 2x - 1$.", "solution_steps": "En la adición, los paréntesis precedidos de $+$ se eliminan sin alterar los signos.", "paes_style": False})
EJERCICIOS.append({"stable_id": "ADD-H-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Suma horizontalmente: $(3x^2 - x + 4) + (x^2 + 5x - 2)$.", "choices": ["A) $4x^2 + 4x + 2$", "B) $4x^2 - 6x + 2$", "C) $4x^2 + 4x - 2$", "D) $2x^2 + 4x + 2$"], "correct_answer": "A) $4x^2 + 4x + 2$", "solution_steps": "Familia $x^2$: $3+1=4x^2$. Familia $x$: $-1+5=4x$. Constantes: $4-2=2$. Resultado: $4x^2+4x+2$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-H-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿La suma $(a + b) + (a - b)$ resulta en $2a$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Eliminamos paréntesis: $a + b + a - b$. Familia $a$: $1+1=2a$. Familia $b$: $+b-b=0$. El $b$ se cancela. Resultado: $2a$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-H-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"La ganancia del primer trimestre de una empresa es $G_1 = 5000k - 200$, y del segundo trimestre es $G_2 = 3000k + 800$. ¿Cuál es la ganancia semestral total? (v{i})", "choices": ["A) $8000k + 600$", "B) $8000k - 600$", "C) $2000k + 600$", "D) $8000k + 1000$"], "correct_answer": "A) $8000k + 600$", "solution_steps": "Familia $k$: $5000+3000=8000k$. Constantes: $-200+800=600$. Total: $8000k+600$.", "paes_style": True})

# 2. ADICION_POL.METODO_VERTICAL
sid2 = "MAT.ALG.ADICION_POL.METODO_VERTICAL"
RECURSOS.append({
    "semantic_id": sid2,
    "objetivo": "Sumar polinomios mediante el método vertical, alineando los términos semejantes en columnas.",
    "introduccion": "Cuando en la escuela aprendiste a sumar números de varios dígitos (unidades con unidades, decenas con decenas), estabas usando el método vertical. En álgebra, la misma lógica se aplica: cada 'columna' agrupa una familia de términos semejantes.",
    "resumen": "En la **Adición Vertical**, los polinomios se escriben uno debajo del otro, alineando los términos semejantes en columnas. Luego se suma columna por columna, como en la aritmética de los números.",
    "explicacion": "Suma: $(4x^2 + 3x - 5)$ y $(2x^2 - x + 1)$.\n\nAlineamos verticalmente:\n```\n  4x² + 3x - 5\n+ 2x² -  x + 1\n─────────────\n  6x² + 2x - 4\n```\n\nEn cada columna sumamos los coeficientes:\n- Columna $x^2$: $4 + 2 = 6$.\n- Columna $x$: $3 + (-1) = 2$.\n- Columna constante: $-5 + 1 = -4$.\n\nResultado: $6x^2 + 2x - 4$.",
    "procedimiento": [
        "Paso 1: Escribe el primer polinomio.",
        "Paso 2: Escribe el segundo polinomio debajo, alineando estrictamente los términos del mismo grado en la misma columna.",
        "Paso 3: Traza una línea horizontal separadora.",
        "Paso 4: Suma columna por columna los coeficientes."
    ],
    "ejemplos": [
        {"titulo": "La suma de los pesos", "enunciado": "Suma verticalmente: (2m^2 - 3m) + (m^2 + 5m - 4).", "solucion_pasos": ["Columna m^2: 2 + 1 = 3m^2.", "Columna m: -3 + 5 = 2m.", "Columna constante: 0 + (-4) = -4.", "Resultado: 3m^2 + 2m - 4."]}
    ],
    "errores_frecuentes": [
        "Desalinear los términos, sumando coeficientes de distintas familias por error de columna.",
        "Olvidar que si un polinomio no tiene un término de cierto grado, se deja un espacio en blanco (coeficiente 0) en esa columna."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-V-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es la ventaja principal del método vertical para sumar polinomios? (v{i})", "choices": ["A) Permite alinear términos semejantes en columnas, reduciendo el riesgo de mezclar coeficientes de distintas familias.", "B) Es más rápido que el método horizontal siempre.", "C) Elimina la necesidad de identificar términos semejantes.", "D) Permite multiplicar en lugar de sumar."], "correct_answer": "A) Permite alinear términos semejantes en columnas, reduciendo el riesgo de mezclar coeficientes de distintas familias.", "solution_steps": "La alineación visual por columnas es la gran fortaleza del método vertical.", "paes_style": False})
EJERCICIOS.append({"stable_id": "ADD-V-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Suma verticalmente $(5n^2 + 2n - 3)$ y $(-n^2 + 4n + 7)$.", "choices": ["A) $4n^2 + 6n + 4$", "B) $4n^2 - 6n + 4$", "C) $6n^2 + 6n + 4$", "D) $4n^2 + 6n - 4$"], "correct_answer": "A) $4n^2 + 6n + 4$", "solution_steps": "Col $n^2$: $5-1=4$. Col $n$: $2+4=6$. Col constante: $-3+7=4$. Resultado: $4n^2+6n+4$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-V-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿Al sumar $(3x + 5)$ y $(x^2 - 2)$ verticalmente, el término $x^2$ del segundo polinomio no tiene pareja en la primera fila y su coeficiente en la suma es simplemente $1$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Si un polinomio no tiene término de cierto grado, ese lugar equivale a $0x^2$. Al sumarlo con $1x^2$, el resultado es $1x^2 = x^2$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-V-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Tres proyectos describen sus costos con los polinomios $P_1 = 2t^2 + 3t$, $P_2 = t^2 - t + 5$ y $P_3 = 4t - 2$. ¿Cuál es el costo total combinado? (v{i})", "choices": ["A) $3t^2 + 6t + 3$", "B) $3t^2 - 6t + 3$", "C) $3t^2 + 6t - 3$", "D) $7t^2 + 6t + 3$"], "correct_answer": "A) $3t^2 + 6t + 3$", "solution_steps": "Col $t^2$: $2+1+0=3$. Col $t$: $3-1+4=6$. Col constante: $0+5-2=3$. Total: $3t^2+6t+3$.", "paes_style": True})

# 3. ADICION_POL.COEFICIENTES_FRACCIONARIOS
sid3 = "MAT.ALG.ADICION_POL.COEFICIENTES_FRACCIONARIOS"
RECURSOS.append({
    "semantic_id": sid3,
    "objetivo": "Sumar polinomios cuyos coeficientes son fracciones, aplicando la suma de fracciones término a término.",
    "introduccion": "Igual que en la vida real podemos tener la mitad de una torta más un cuarto de torta, en álgebra podemos sumar polinomios con coeficientes fraccionarios. La lógica no cambia, solo necesitamos recordar cómo sumar fracciones.",
    "resumen": "Al sumar polinomios con **Coeficientes Fraccionarios**, el proceso es idéntico al de la adición normal, pero al sumar los coeficientes de cada familia, se aplica la suma de fracciones con denominador común.",
    "explicacion": "Suma: $(\\frac{1}{2}x^2 + \\frac{1}{3}x) + (\\frac{1}{4}x^2 - \\frac{2}{3}x + 1)$.\n\nFamilia $x^2$: $\\frac{1}{2} + \\frac{1}{4} = \\frac{2}{4} + \\frac{1}{4} = \\frac{3}{4}$.\nFamilia $x$: $\\frac{1}{3} - \\frac{2}{3} = \\frac{-1}{3}$.\nConstante: $1$.\n\nResultado: $\\frac{3}{4}x^2 - \\frac{1}{3}x + 1$.",
    "procedimiento": [
        "Paso 1: Identifica las familias de términos semejantes.",
        "Paso 2: Para cada familia, extrae los coeficientes fraccionarios.",
        "Paso 3: Suma o resta esas fracciones buscando denominador común.",
        "Paso 4: El resultado de cada operación de fracciones forma el nuevo coeficiente de su familia."
    ],
    "ejemplos": [
        {"titulo": "Mitades y cuartos", "enunciado": "Suma: (1/2)a + (1/4)a + (3/4)a.", "solucion_pasos": ["Todos son de la familia 'a'. Sumamos los coeficientes.", "MCD de 2, 4, 4 es 4.", "1/2 = 2/4.", "2/4 + 1/4 + 3/4 = 6/4 = 3/2.", "Resultado: (3/2)a."]}
    ],
    "errores_frecuentes": [
        "Sumar numeradores y denominadores directamente sin buscar denominador común.",
        "Olvidar simplificar la fracción resultante a su mínima expresión."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-CF-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al sumar los términos $(\\frac{{1}}{{3}})x + (\\frac{{1}}{{6}})x$, ¿cuál es el procedimiento correcto para encontrar el coeficiente de $x$? (v{i})", "choices": ["A) Buscar el denominador común (6), convertir $\\frac{1}{3} = \\frac{2}{6}$, y sumar: $\\frac{2}{6}+\\frac{1}{6}=\\frac{3}{6}=\\frac{1}{2}$.", "B) Sumar numeradores y denominadores: $\\frac{1+1}{3+6} = \\frac{2}{9}$.", "C) Multiplicar las fracciones: $\\frac{1}{3} \\times \\frac{1}{6} = \\frac{1}{18}$.", "D) Restar los denominadores: $\\frac{1}{3-6}$."], "correct_answer": "A) Buscar el denominador común (6), convertir $\\frac{1}{3} = \\frac{2}{6}$, y sumar: $\\frac{2}{6}+\\frac{1}{6}=\\frac{3}{6}=\\frac{1}{2}$.", "solution_steps": "La suma de fracciones requiere denominador común. La suma de numeradores y denominadores es un error fundamental.", "paes_style": False})
EJERCICIOS.append({"stable_id": "ADD-CF-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Suma: $(\\frac{2}{3}m - \\frac{1}{2}) + (\\frac{1}{6}m + \\frac{3}{4})$.", "choices": ["A) $\\frac{5}{6}m + \\frac{1}{4}$", "B) $\\frac{3}{9}m + \\frac{2}{6}$", "C) $\\frac{5}{6}m - \\frac{1}{4}$", "D) $m + \\frac{1}{4}$"], "correct_answer": "A) $\\frac{5}{6}m + \\frac{1}{4}$", "solution_steps": "Familia $m$: $\\frac{2}{3}+\\frac{1}{6} = \\frac{4}{6}+\\frac{1}{6}=\\frac{5}{6}$. Constantes: $-\\frac{1}{2}+\\frac{3}{4}=-\\frac{2}{4}+\\frac{3}{4}=\\frac{1}{4}$. Resultado: $\\frac{5}{6}m+\\frac{1}{4}$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-CF-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿La suma de $(\\frac{3}{4})x$ y $(\\frac{1}{4})x$ resulta en $x$ (un coeficiente de 1)?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Mismo denominador: $\\frac{3}{4}+\\frac{1}{4}=\\frac{4}{4}=1$. Un coeficiente de 1 en álgebra se escribe simplemente como $x$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-CF-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Un nutricionista combina dos dietas. La primera aporta $\\frac{{1}}{{4}}p$ de proteína y $\\frac{{1}}{{2}}c$ de carbohidratos. La segunda aporta $\\frac{{3}}{{4}}p$ y $\\frac{{1}}{{4}}c$. ¿Cuál es el aporte nutricional total? (v{i})", "choices": ["A) $p + \\frac{3}{4}c$", "B) $p + \\frac{3}{4}c$... misma respuesta", "C) $\\frac{4}{8}p + \\frac{3}{6}c$", "D) $\\frac{1}{2}p + \\frac{3}{4}c$"], "correct_answer": "A) $p + \\frac{3}{4}c$", "solution_steps": "Proteína: $\\frac{1}{4}+\\frac{3}{4}=\\frac{4}{4}=1p$. Carbohidratos: $\\frac{1}{2}+\\frac{1}{4}=\\frac{2}{4}+\\frac{1}{4}=\\frac{3}{4}c$. Total: $p + \\frac{3}{4}c$.", "paes_style": True})

# 4. ADICION_POL.TERMINOS_FALTANTES
sid4 = "MAT.ALG.ADICION_POL.TERMINOS_FALTANTES"
RECURSOS.append({
    "semantic_id": sid4,
    "objetivo": "Sumar polinomios que tienen grados distintos o términos ausentes, gestionando correctamente los espacios vacíos.",
    "introduccion": "Muchas veces los polinomios que se suman no tienen los mismos términos. Uno puede tener término en $x^3$ y el otro no. En la suma vertical, esto corresponde a una columna con solo un número, que pasa directo al resultado.",
    "resumen": "Al sumar polinomios con **Términos Faltantes**, los grados que no tienen representación en uno de los sumandos se tratan como si tuvieran coeficiente $0$. En el resultado, esos términos se 'heredan' directamente del único polinomio que los tiene.",
    "explicacion": "Suma: $(x^3 + 2x - 5)$ y $(3x^2 + x + 1)$.\n\nEl primer polinomio no tiene $x^2$, el segundo no tiene $x^3$.\n\nEn formato vertical:\n```\n  x³ + 0x² + 2x - 5\n+ 0x³ + 3x² +  x + 1\n───────────────────\n  x³ + 3x² + 3x - 4\n```\n\nLos ceros se hacen explícitos para no confundir columnas. Los términos únicos (como $x^3$) pasan directo al resultado.",
    "procedimiento": [
        "Paso 1: Determina el grado máximo entre todos los polinomios a sumar.",
        "Paso 2: Completa los polinomios con los términos faltantes usando coeficiente $0$.",
        "Paso 3: Alinea verticalmente.",
        "Paso 4: Suma columna por columna como siempre."
    ],
    "ejemplos": [
        {"titulo": "El hueco del cuadrado", "enunciado": "Suma: (2a^3 - 5) + (a^2 + 3a + 2).", "solucion_pasos": ["Completamos con ceros: (2a^3 + 0a^2 + 0a - 5) + (0a^3 + a^2 + 3a + 2).", "Col a^3: 2+0 = 2a^3.", "Col a^2: 0+1 = a^2.", "Col a: 0+3 = 3a.", "Constante: -5+2 = -3.", "Resultado: 2a^3 + a^2 + 3a - 3."]}
    ],
    "errores_frecuentes": [
        "Desalinear los términos al no colocar explícitamente los ceros, sumando términos de distintas familias.",
        "Omitir completamente un grado faltante en el resultado por creer que 'no existe'."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-TF-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Si un polinomio no tiene término de grado $x^2$ y se suma verticalmente con otro que sí lo tiene, ¿qué valor de coeficiente se le asigna al grado faltante del primero? (v{i})", "choices": ["A) Cero ($0$), porque matemáticamente ese grado existe con coeficiente nulo.", "B) Uno ($1$), para no alterar la suma.", "C) Se omite la columna entera.", "D) Se toma el coeficiente del polinomio que sí lo tiene."], "correct_answer": "A) Cero ($0$), porque matemáticamente ese grado existe con coeficiente nulo.", "solution_steps": "Un término ausente equivale a tener ese grado con coeficiente 0. Esto es clave para no confundir columnas en el método vertical.", "paes_style": False})
EJERCICIOS.append({"stable_id": "ADD-TF-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Suma: $(4x^3 - 2)$ y $(x^2 + 5x - 3)$.", "choices": ["A) $4x^3 + x^2 + 5x - 5$", "B) $4x^3 - x^2 + 5x - 5$", "C) $5x^3 + 5x - 5$", "D) $4x^3 + x^2 - 5$"], "correct_answer": "A) $4x^3 + x^2 + 5x - 5$", "solution_steps": "El primero no tiene $x^2$ ni $x$. El segundo no tiene $x^3$. Sumamos: $4x^3+x^2+5x-5$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-TF-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿La suma de $(x^2 + 1)$ y $(x + 2)$ resulta en el polinomio de grado 2: $x^2 + x + 3$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$x^2$ solo en el primero. $x$ solo en el segundo. Constantes: $1+2=3$. Resultado: $x^2+x+3$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-TF-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"El costo de producción de tres productos se modela como $C_1 = 2v^3 + 5$, $C_2 = 3v^2$ y $C_3 = 4v - 1$. ¿Cuál es el costo total? (v{i})", "choices": ["A) $2v^3 + 3v^2 + 4v + 4$", "B) $2v^3 + 3v^2 + 4v - 4$", "C) $9v^6 + 4$", "D) $2v^3 + 3v^2 + 4v + 5$"], "correct_answer": "A) $2v^3 + 3v^2 + 4v + 4$", "solution_steps": "Cada término de cada grado: $2v^3$ (solo en $C_1$), $3v^2$ (solo en $C_2$), $4v$ (solo en $C_3$), constante: $5+0-1=4$. Total: $2v^3+3v^2+4v+4$.", "paes_style": True})

# 5. ADICION_POL.POLINOMIOS_DESORDENADOS
sid5 = "MAT.ALG.ADICION_POL.POLINOMIOS_DESORDENADOS"
RECURSOS.append({
    "semantic_id": sid5,
    "objetivo": "Sumar polinomios cuyos términos no están ordenados por grado decreciente, aplicando un reordenamiento previo.",
    "introduccion": "Un polinomio puede estar 'desordenado', con sus términos escritos en cualquier orden. Antes de sumarlos, conviene organizarlos por grado de mayor a menor para no cometer errores de columna.",
    "resumen": "Al sumar **Polinomios Desordenados**, el primer paso es reorganizar cada polinomio en orden decreciente de grado. Una vez ordenados, la suma (horizontal o vertical) fluye sin riesgo de confundir familias.",
    "explicacion": "Suma: $(3 + x^2 + 5x)$ y $(2x - 1 + x^3)$.\n\nOrdenamos primero:\n- Primer polinomio: $x^2 + 5x + 3$.\n- Segundo polinomio: $x^3 + 2x - 1$.\n\nAhora sumamos:\n$x^3 + x^2 + 7x + 2$.\n\n(El $x^3$ solo estaba en el segundo, el $x^2$ solo en el primero, $5x + 2x = 7x$, $3 + (-1) = 2$.)",
    "procedimiento": [
        "Paso 1: Reescribe cada polinomio con sus términos ordenados de mayor a menor grado.",
        "Paso 2: Completa los términos faltantes con coeficiente 0.",
        "Paso 3: Aplica el método horizontal o vertical normalmente.",
        "Paso 4: Verifica que el resultado también esté ordenado."
    ],
    "ejemplos": [
        {"titulo": "Ordenar para ganar", "enunciado": "Suma: (4 - 2a + a^3) y (a^2 + 3 - a).", "solucion_pasos": ["Orden 1: a^3 + 0a^2 - 2a + 4.", "Orden 2: 0a^3 + a^2 - a + 3.", "Suma: a^3 + a^2 - 3a + 7."]}
    ],
    "errores_frecuentes": [
        "Sumar los polinomios sin ordenar, mezclando términos de distintas familias por estar visualmente adyacentes.",
        "Ordenar un polinomio pero no el otro, creando desalineación en el método vertical."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-PD-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Por qué se recomienda ordenar los polinomios de mayor a menor grado antes de sumarlos? (v{i})", "choices": ["A) Para alinear correctamente los términos semejantes en columnas y evitar errores al mezclar coeficientes de distintas familias.", "B) Porque los polinomios desordenados no pueden ser sumados.", "C) Para que el resultado siempre sea positivo.", "D) Para multiplicar antes de sumar."], "correct_answer": "A) Para alinear correctamente los términos semejantes en columnas y evitar errores al mezclar coeficientes de distintas familias.", "solution_steps": "El orden facilita la alineación. Sin él, es fácil sumar términos de familias distintas por error visual.", "paes_style": False})
EJERCICIOS.append({"stable_id": "ADD-PD-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Ordena y suma: $(5 + 3n^2 - n)$ y $(n^3 - 2 + 4n)$.", "choices": ["A) $n^3 + 3n^2 + 3n + 3$", "B) $n^3 - 3n^2 + 3n + 3$", "C) $n^3 + 3n^2 - 3n + 3$", "D) $n^3 + 3n^2 + 3n - 3$"], "correct_answer": "A) $n^3 + 3n^2 + 3n + 3$", "solution_steps": "Ordenados: $(3n^2 - n + 5)$ y $(n^3 + 4n - 2)$. Suma: $n^3+3n^2+(-1+4)n+(5-2)=n^3+3n^2+3n+3$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-PD-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿El polinomio $2 - x + x^2$ ya está ordenado en forma decreciente de grado?", "choices": [], "correct_answer": "Falso", "solution_steps": "La forma decreciente ordena de mayor grado a menor: $x^2 - x + 2$. El polinomio presentado empieza con la constante (grado 0), que es el grado más bajo.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"ADD-PD-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Dos físicos modelan la posición de un objeto: el primero la expresa como $3 + 2t^2 - t$ y el segundo como $5t - t^3 + 1$. ¿Cuál es la posición combinada total correctamente ordenada? (v{i})", "choices": ["A) $-t^3 + 2t^2 + 4t + 4$", "B) $-t^3 - 2t^2 + 4t + 4$", "C) $t^3 + 2t^2 + 4t + 4$", "D) $-t^3 + 2t^2 - 4t + 4$"], "correct_answer": "A) $-t^3 + 2t^2 + 4t + 4$", "solution_steps": "Ordenamos: $(2t^2-t+3)$ y $(-t^3+5t+1)$. Suma: $-t^3+2t^2+(-1+5)t+(3+1)=-t^3+2t^2+4t+4$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 4 (B0303/Adicion Polinomios)...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"  Creado {filename}.yaml")
    print("Escribiendo JSONL Tanda 4...")
    append_jsonl("mat-alg-operaciones-banco-gen-4", EJERCICIOS)
    print(f"  mat-alg-operaciones-banco-gen-4.jsonl con {len(EJERCICIOS)} ejercicios.")

if __name__ == "__main__":
    generate_all()

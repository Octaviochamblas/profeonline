# scratch/build_alg_b0304_t2.py
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

# 1. MULT_MONOMIOS.DOS_MONOMIOS
sid1 = "MAT.ALG.MULT_MONOMIOS.DOS_MONOMIOS"
RECURSOS.append({
    "semantic_id": sid1,
    "objetivo": "Multiplicar dos monomios aplicando la regla de signos, el producto de coeficientes y la suma de exponentes de bases iguales.",
    "introduccion": "Multiplicar dos monomios es el bloque básico de toda la multiplicación algebraica. Consiste simplemente en fusionar dos términos simples en uno solo siguiendo tres reglas ordenadas.",
    "resumen": "Para multiplicar **Dos Monomios**, se multiplican sus coeficientes numéricos (aplicando la regla de signos) y se suman los exponentes de las letras que tengan la misma base.",
    "explicacion": "Multiplica: $(5x^2y)(−3xy^3)$.\n\nPaso 1: Signos. $(+)(-) = -$.\nPaso 2: Coeficientes. $5 \\times 3 = 15$.\nPaso 3: Variable $x$. $x^2 \\cdot x^1 = x^{2+1} = x^3$.\nPaso 4: Variable $y$. $y^1 \\cdot y^3 = y^{1+3} = y^4$.\n\nResultado combinado: $-15x^3y^4$.",
    "procedimiento": [
        "Paso 1: Determina el signo del producto usando la regla de signos.",
        "Paso 2: Multiplica los valores numéricos de los coeficientes.",
        "Paso 3: Identifica las variables repetidas en ambos monomios y suma sus exponentes.",
        "Paso 4: Conserva intactas las variables que aparezcan en solo uno de los monomios.",
        "Paso 5: Escribe el término final combinando signo, coeficiente y variables ordenadas alfabéticamente."
    ],
    "ejemplos": [
        {"titulo": "Variables no compartidas", "enunciado": "Multiplica: (2a^2b)(-5bc).", "solucion_pasos": ["Signo: (+)(-) = -.", "Coeficientes: 2 × 5 = 10.", "Variable a: a^2 (no se repite, queda igual).", "Variable b: b^1 · b^1 = b^2.", "Variable c: c (no se repite, queda igual).", "Resultado: -10a^2b^2c."]}
    ],
    "errores_frecuentes": [
        "Sumar los coeficientes en lugar de multiplicarlos (ej. $2x \\cdot 3x = 5x^2$).",
        "Olvidar sumar los exponentes implícitos que tienen valor 1 (ej. $x^2 \\cdot x = x^2$ en lugar de $x^3$)."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-D-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es el resultado correcto al multiplicar los monomios $(-4ab^2)$ y $(3a^2c)$? (v{i})", "choices": ["A) $-12a^3b^2c$", "B) $-12ab^2c$", "C) $-1a^3b^2c$", "D) $-12a^2b^2c$"], "correct_answer": "A) $-12a^3b^2c$", "solution_steps": "Signo: $(-)(+)=-$. Coeficientes: $4 \\times 3 = 12$. Variable $a$: $a^1 \\cdot a^2 = a^3$. Variable $b$: $b^2$. Variable $c$: $c$. Resultado: $-12a^3b^2c$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "MM-D-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Calcula el producto: $(7x^3y^2)(-2xy^4)$.", "choices": ["A) $-14x^4y^6$", "B) $-14x^3y^8$", "C) $14x^4y^6$", "D) $-9x^4y^6$"], "correct_answer": "A) $-14x^4y^6$", "solution_steps": "Signo: $(-)(+)=-$. Coeficientes: $7 \\times 2 = 14$. Variable $x$: $x^3 \\cdot x = x^4$. Variable $y$: $y^2 \\cdot y^4 = y^6$. Resultado: $-14x^4y^6$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-D-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿El producto de $(3m^2)$ y $(-2n^3)$ es $-6m^2n^3$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Signo: $(+)(-) = -$. Coeficientes: $3 \\times 2 = 6$. Como no comparten letras, se escriben juntas: $m^2n^3$. Resultado: $-6m^2n^3$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-D-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un terreno rectangular tiene de largo $6a^2b$ metros y de ancho $2ab^3$ metros. ¿Cuál es su área en metros cuadrados? (v{i})", "choices": ["A) $12a^3b^4$", "B) $12a^2b^3$", "C) $8a^3b^4$", "D) $12ab$"], "correct_answer": "A) $12a^3b^4$", "solution_steps": "Área = largo × ancho $= (6a^2b)(2ab^3) = (6 \\cdot 2)(a^{2+1})(b^{1+3}) = 12a^3b^4$.", "paes_style": True})

# 2. MULT_MON_POL.DISTRIBUCION_TERMINOS
sid2 = "MAT.ALG.MULT_MON_POL.DISTRIBUCION_TERMINOS"
RECURSOS.append({
    "semantic_id": sid2,
    "objetivo": "Aplicar la propiedad distributiva al multiplicar un monomio por un polinomio.",
    "introduccion": "Imagina que eres un cartero y tienes que entregar una carta en cada casa de una cuadra. El monomio es el cartero, y cada término del polinomio es una casa. ¡El monomio debe visitar (multiplicar) a absolutamente todos los términos de la cuadra!",
    "resumen": "La multiplicación de un monomio por un polinomio se basa en la **Propiedad Distributiva**: el monomio exterior se multiplica por cada uno de los términos del polinomio interior por separado, sumando los resultados obtenidos.",
    "explicacion": "Operación: $3x(2x^2 - 5x + 4)$.\n\nAplicamos la distribución término a término:\n1. Primer término: $(3x)(2x^2) = 6x^3$.\n2. Segundo término: $(3x)(-5x) = -15x^2$.\n3. Tercer término: $(3x)(+4) = +12x$.\n\nSumamos o conectamos los resultados: $6x^3 - 15x^2 + 12x$.",
    "procedimiento": [
        "Paso 1: Identifica el monomio exterior y todos los términos del polinomio interior.",
        "Paso 2: Multiplica el monomio por el primer término del polinomio.",
        "Paso 3: Multiplica el monomio por el segundo término del polinomio (respetando signos).",
        "Paso 4: Repite el proceso para todos los términos restantes.",
        "Paso 5: Escribe la expresión final conectando todos los productos parciales con sus respectivos signos."
    ],
    "ejemplos": [
        {"titulo": "El cartero algebraico", "enunciado": "Multiplica: 2a(3a - 5b).", "solucion_pasos": ["Multiplicación 1: (2a)(3a) = 6a^2.", "Multiplicación 2: (2a)(-5b) = -10ab.", "Combinación: 6a^2 - 10ab."]}
    ],
    "errores_frecuentes": [
        "Multiplicar el monomio únicamente por el primer término del polinomio y dejar los demás intactos (ej. $2(x+3) = 2x+3$).",
        "Cometer errores de signos al multiplicar el monomio por los términos negativos del polinomio."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MMP-DT-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué propiedad matemática justifica que la operación $3a(b + c)$ se resuelva como $3ab + 3ac$? (v{i})", "choices": ["A) Propiedad distributiva de la multiplicación respecto de la suma.", "B) Propiedad conmutativa.", "C) Propiedad asociativa.", "D) Elemento neutro multiplicativo."], "correct_answer": "A) Propiedad distributiva de la multiplicación respecto de la suma.", "solution_steps": "La distributividad permite repartir el producto exterior a cada sumando interior.", "paes_style": False})
EJERCICIOS.append({"stable_id": "MMP-DT-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el producto: $4x^2(2x - 3)$.", "choices": ["A) $8x^3 - 12x^2$", "B) $8x^2 - 12x^2$", "C) $8x^3 - 3$", "D) $8x^3 + 12x^2$"], "correct_answer": "A) $8x^3 - 12x^2$", "solution_steps": "$4x^2(2x) = 8x^3$. $4x^2(-3) = -12x^2$. Resultado: $8x^3 - 12x^2$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MMP-DT-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿El resultado de multiplicar $2(x^2 - 5x + 3)$ es $2x^2 - 10x + 6$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Multiplicamos 2 por cada término: $2(x^2) = 2x^2$, $2(-5x) = -10x$, $2(3) = 6$. Combinado da $2x^2 - 10x + 6$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MMP-DT-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"El ingreso de un cine se calcula como $I = p(100 - 2p)$ donde $p$ es el precio de la entrada. ¿Cuál es la expresión equivalente para el ingreso al distribuir el precio? (v{i})", "choices": ["A) $100p - 2p^2$", "B) $100 - 2p^2$", "C) $100p - 2p$", "D) $98p^2$"], "correct_answer": "A) $100p - 2p^2$", "solution_steps": "Distribuimos $p$: $p \\cdot 100 = 100p$. $p \\cdot (-2p) = -2p^2$. Resultado: $100p - 2p^2$.", "paes_style": True})

# 3. MULT_POLINOMIOS.REGLA_GENERAL
sid3 = "MAT.ALG.MULT_POLINOMIOS.REGLA_GENERAL"
RECURSOS.append({
    "semantic_id": sid3,
    "objetivo": "Multiplicar dos polinomios multiplicando cada término del primero por todos los términos del segundo y reduciendo los semejantes.",
    "introduccion": "Si la multiplicación de monomio por polinomio era un cartero entregando cartas en una cuadra, la multiplicación de polinomios es como si todos los carteros de una oficina entregaran cartas en todas las casas de la cuadra. Absolutamente todos se multiplican con todos.",
    "resumen": "La **Multiplicación de Polinomios** consiste en multiplicar cada término del primer polinomio por cada uno de los términos del segundo polinomio. Luego se reducen todos los términos semejantes que resulten.",
    "explicacion": "Multiplica: $(2x + 3)(x - 4)$.\n\nAplicamos la distribución extendida:\n1. $(2x)(x) = 2x^2$.\n2. $(2x)(-4) = -8x$.\n3. $(3)(x) = +3x$.\n4. $(3)(-4) = -12$.\n\nUnimos los términos: $2x^2 - 8x + 3x - 12$.\nReducimos semejantes (familia $x$): $-8x + 3x = -5x$.\nResultado final: $2x^2 - 5x - 12$.",
    "procedimiento": [
        "Paso 1: Toma el primer término del primer polinomio y multiplícalo por todos los términos del segundo.",
        "Paso 2: Toma el segundo término del primer polinomio y haz lo mismo.",
        "Paso 3: Repite el proceso para cada término del primer polinomio.",
        "Paso 4: Escribe todos los productos obtenidos en una sola línea.",
        "Paso 5: Identifica y reduce los términos semejantes para obtener el polinomio simplificado."
    ],
    "ejemplos": [
        {"titulo": "El producto cruzado", "enunciado": "Multiplica: (a + b)(a - b).", "solucion_pasos": ["(a)(a) = a^2.", "(a)(-b) = -ab.", "(b)(a) = +ab (ordenado).", "(b)(-b) = -b^2.", "Línea completa: a^2 - ab + ab - b^2.", "Reducción: -ab + ab = 0.", "Resultado: a^2 - b^2."]}
    ],
    "errores_frecuentes": [
        "Multiplicar solo términos en la misma posición (ej. creer que $(x+1)(x+2) = x^2 + 2$).",
        "Olvidar la regla de signos en algunos de los productos cruzados."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MP-RG-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al multiplicar un binomio de 2 términos por un trinomio de 3 términos, ¿cuántas multiplicaciones de monomios individuales se deben realizar antes de reducir semejantes? (v{i})", "choices": ["A) $6$ multiplicaciones.", "B) $5$ multiplicaciones.", "C) $4$ multiplicaciones.", "D) $2$ multiplicaciones."], "correct_answer": "A) $6$ multiplicaciones.", "solution_steps": "Por regla general, si el primero tiene $m$ términos y el segundo $n$ términos, se realizan $m \\times n$ productos. En este caso: $2 \\times 3 = 6$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "MP-RG-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Multiplica y simplifica: $(x + 5)(x + 2)$.", "choices": ["A) $x^2 + 7x + 10$", "B) $x^2 + 10$", "C) $x^2 + 7x + 7$", "D) $x^2 + 3x + 10$"], "correct_answer": "A) $x^2 + 7x + 10$", "solution_steps": "$(x)(x)=x^2$. $(x)(2)=2x$. $(5)(x)=5x$. $(5)(2)=10$. Sumamos: $x^2 + 2x + 5x + 10 = x^2 + 7x + 10$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MP-RG-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿El producto $(2a + 1)(a - 3)$ es igual a $2a^2 - 5a - 3$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$(2a)(a) = 2a^2$, $(2a)(-3) = -6a$, $(1)(a) = a$, $(1)(-3) = -3$. Juntos: $2a^2 - 6a + a - 3 = 2a^2 - 5a - 3$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MP-RG-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un parque rectangular tiene largo $(x + 8)$ metros y ancho $(x - 3)$ metros. ¿Qué expresión algebraica describe el área total del parque? (v{i})", "choices": ["A) $x^2 + 5x - 24$ metros cuadrados.", "B) $x^2 - 24$ metros cuadrados.", "C) $x^2 + 5x + 24$ metros cuadrados.", "D) $2x + 5$ metros cuadrados."], "correct_answer": "A) $x^2 + 5x - 24$ metros cuadrados.", "solution_steps": "Área = largo × ancho $= (x+8)(x-3) = x^2 - 3x + 8x - 24 = x^2 + 5x - 24$.", "paes_style": True})

# 4. MULT_MONOMIOS.MULTIPLES_MONOMIOS
sid4 = "MAT.ALG.MULT_MONOMIOS.MULTIPLES_MONOMIOS"
RECURSOS.append({
    "semantic_id": sid4,
    "objetivo": "Multiplicar tres o más monomios en una sola operación aplicando las propiedades asociativa y conmutativa.",
    "introduccion": "Cuando multiplicas tres o más números, como $2 \\times 3 \\times 5$, multiplicas dos de ellos y luego el resultado por el tercero. Al multiplicar tres o más monomios, hacemos exactamente lo mismo combinando todos los números y todas las letras juntas.",
    "resumen": "Al multiplicar **Múltiples Monomios**, el signo final se determina contando los factores negativos. Luego se multiplican todos los coeficientes numéricos y se suman los exponentes de las letras que tengan la misma base.",
    "explicacion": "Calcula: $(-2x^2)(3y)(-5x^3y^2)$.\n\nPaso 1: Signo. 2 negativos (par) → $+$.\nPaso 2: Coeficientes. $2 \\times 3 \\times 5 = 30$.\nPaso 3: Variable $x$. $x^2 \\cdot x^3 = x^5$.\nPaso 4: Variable $y$. $y^1 \\cdot y^2 = y^3$.\n\nResultado combinado: $30x^5y^3$.",
    "procedimiento": [
        "Paso 1: Determina el signo final contando cuántos términos negativos hay (par → +, impar → -).",
        "Paso 2: Multiplica todos los coeficientes numéricos entre sí.",
        "Paso 3: Agrupa las variables de igual base y suma sus exponentes.",
        "Paso 4: Escribe las variables sin repetir en orden alfabético.",
        "Paso 5: Ensambla el signo, el coeficiente y la parte literal en un solo término."
    ],
    "ejemplos": [
        {"titulo": "Tres factores combinados", "enunciado": "Multiplica: (a^2b)(-3ab^2)(-2c).", "solucion_pasos": ["Signo: 2 negativos → +.", "Coeficientes: 1 × 3 × 2 = 6.", "Variable a: a^2 · a = a^3.", "Variable b: b · b^2 = b^3.", "Variable c: c (se mantiene).", "Resultado: 6a^3b^3c."]}
    ],
    "errores_frecuentes": [
        "Multiplicar los exponentes de la misma base en lugar de sumarlos.",
        "Olvidar el exponente 1 de variables que no muestran número arriba (ej. $y \\cdot y^2 = y^2$ en lugar de $y^3$)."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-M-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al multiplicar los tres monomios $(-3a^2b)(2ab^3)(-a^2)$, ¿cómo se calcula el signo y la potencia de la variable $a$? (v{i})", "choices": ["A) Hay 2 factores negativos (signo $+$) y los exponentes de la variable $a$ se suman ($2+1+2=5$), dando $a^5$.", "B) Hay 3 factores negativos (signo $-$) y los exponentes de $a$ se multiplican ($2 \\cdot 1 \\cdot 2 = 4$).", "C) Signo $-$ y exponente de $a$ es $4$.", "D) Signo $+$ y exponente de $a$ es $4$."], "correct_answer": "A) Hay 2 factores negativos (signo $+$) y los exponentes de la variable $a$ se suman ($2+1+2=5$), dando $a^5$.", "solution_steps": "Signos: $(-)(+)(-)=+$. Exponentes de $a$: $2+1+2=5$. Coeficientes: $3 \\times 2 \\times 1 = 6$. Resultado completo: $6a^5b^4$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "MM-M-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el producto de: $(2x)(-3y)(4x^2)(y^2)$.", "choices": ["A) $-24x^3y^3$", "B) $24x^3y^3$", "C) $-24x^2y^2$", "D) $-12x^3y^3$"], "correct_answer": "A) $-24x^3y^3$", "solution_steps": "Signo: 1 negativo (impar) → $-$. Coeficientes: $2 \\times 3 \\times 4 \\times 1 = 24$. Variable $x$: $x \\cdot x^2 = x^3$. Variable $y$: $y \\cdot y^2 = y^3$. Resultado: $-24x^3y^3$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-M-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿El producto de $(-a)(-b)(-c)$ resulta en $-abc$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Signos: 3 negativos (impar) → $-$. Coeficientes: $1 \\times 1 \\times 1 = 1$. Letras: $a \\cdot b \\cdot c = abc$. Resultado: $-abc$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MM-M-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"El volumen de una caja rectangular con tres dimensiones es largo × ancho × alto. Si el largo es $2t^2$, el ancho es $3t$ y el alto es $5t^3$, ¿cuál es la fórmula simplificada para el volumen? (v{i})", "choices": ["A) $30t^6$", "B) $10t^6$", "C) $30t^5$", "D) $30t^7$"], "correct_answer": "A) $30t^6$", "solution_steps": "Volumen $= (2t^2)(3t)(5t^3) = (2 \\cdot 3 \\cdot 5)(t^{2+1+3}) = 30t^6$.", "paes_style": True})

# 5. MULT_MON_POL.REGLA_OPERATIVA
sid5 = "MAT.ALG.MULT_MON_POL.REGLA_OPERATIVA"
RECURSOS.append({
    "semantic_id": sid5,
    "objetivo": "Multiplicar un monomio por un polinomio siguiendo la regla operativa formal del álgebra.",
    "introduccion": "La regla operativa para multiplicar un monomio por un polinomio establece un orden estricto para realizar cada multiplicación individual. Seguir este protocolo de forma metódica garantiza que no haya descuidos de signo o de variables.",
    "resumen": "La **Regla Operativa** para multiplicar un monomio por un polinomio exige escribir el monomio, abrir paréntesis para el polinomio, y multiplicar el monomio por cada uno de los términos del polinomio de izquierda a derecha, respetando las leyes de multiplicación.",
    "explicacion": "Sea la operación: $-4a^2(2a^2 - 3ab + 5b^2)$.\n\nAplicamos la regla operativa distribuyendo $-4a^2$ de izquierda a derecha:\n1. $(-4a^2)(2a^2) = -8a^4$.\n2. $(-4a^2)(-3ab) = +12a^3b$ (ojo con el signo: negativo × negativo = positivo).\n3. $(-4a^2)(+5b^2) = -20a^2b^2$.\n\nResultado completo: $-8a^4 + 12a^3b - 20a^2b^2$.",
    "procedimiento": [
        "Paso 1: Escribe el monomio multiplicador delante del polinomio encerrado en paréntesis.",
        "Paso 2: Multiplica el monomio por el primer término del polinomio (signo, número, letras).",
        "Paso 3: Multiplica el monomio por el segundo término del polinomio (signo, número, letras).",
        "Paso 4: Continúa término a término hasta finalizar el polinomio.",
        "Paso 5: Escribe el polinomio resultante con sus términos ordenados."
    ],
    "ejemplos": [
        {"titulo": "Monomio negativo distribuidor", "enunciado": "Multiplica: -3x(2x^2 - x + 4).", "solucion_pasos": ["Multiplicación 1: (-3x)(2x^2) = -6x^3.", "Multiplicación 2: (-3x)(-x) = +3x^2.", "Multiplicación 3: (-3x)(+4) = -12x.", "Resultado combinado: -6x^3 + 3x^2 - 12x."]}
    ],
    "errores_frecuentes": [
        "Olvidar cambiar el signo de los términos interiores cuando el monomio multiplicador es negativo.",
        "Multiplicar el monomio por el primer término y sumar el resto del polinomio sin multiplicar."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MMP-RO-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al multiplicar el monomio negativo $-5x$ por el binomio $(2x - 3)$, ¿cuál es el resultado correcto al aplicar la regla operativa? (v{i})", "choices": ["A) $-10x^2 + 15x$", "B) $-10x^2 - 15x$", "C) $-10x^2 - 3$", "D) $-10x + 15$"], "correct_answer": "A) $-10x^2 + 15x$", "solution_steps": "Multiplicamos: $(-5x)(2x) = -10x^2$. $(-5x)(-3) = +15x$. Resultado: $-10x^2 + 15x$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "MMP-RO-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el producto: $-2a(3a^2 - 4a + 1)$.", "choices": ["A) $-6a^3 + 8a^2 - 2a$", "B) $-6a^3 - 8a^2 + 2a$", "C) $-6a^3 + 8a^2 + 2a$", "D) $-6a^2 + 8a - 2$"], "correct_answer": "A) $-6a^3 + 8a^2 - 2a$", "solution_steps": "Multiplicamos $-2a$ por cada término: $-2a(3a^2) = -6a^3$, $-2a(-4a) = +8a^2$, $-2a(1) = -2a$. Resultado: $-6a^3 + 8a^2 - 2a$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MMP-RO-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿El resultado de multiplicar $-x^2(x - 5)$ es $-x^3 + 5x^2$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Multiplicamos: $(-x^2)(x) = -x^3$. $(-x^2)(-5) = +5x^2$. Resultado: $-x^3 + 5x^2$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"MMP-RO-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"La producción de un insumo se modela como $P = -3k^2(2k - 5)$. Para fines de presupuesto, ¿cuál es la expresión equivalente al distribuir la producción? (v{i})", "choices": ["A) $-6k^3 + 15k^2$", "B) $-6k^3 - 15k^2$", "C) $-6k^2 + 15k$", "D) $-6k^3 + 5$"], "correct_answer": "A) $-6k^3 + 15k^2$", "solution_steps": "Distribuimos el monomio: $-3k^2 \\cdot 2k = -6k^3$. $-3k^2 \\cdot (-5) = +15k^2$. Resultado: $-6k^3 + 15k^2$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 2 (B0304/Mult Monomios y Polinomios)...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"  Creado {filename}.yaml")
    print("Escribiendo JSONL Tanda 2...")
    append_jsonl("mat-alg-multiplicacion-banco-gen-2", EJERCICIOS)
    print(f"  mat-alg-multiplicacion-banco-gen-2.jsonl con {len(EJERCICIOS)} ejercicios.")

if __name__ == "__main__":
    generate_all()

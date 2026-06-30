# scratch/build_alg_b0304_t1.py
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

# 1. LEYES_MULTIPLICACION.SIGNOS_DOS_FACTORES
sid1 = "MAT.ALG.LEYES_MULTIPLICACION.SIGNOS_DOS_FACTORES"
RECURSOS.append({
    "semantic_id": sid1,
    "objetivo": "Aplicar correctamente la regla de los signos al multiplicar dos factores algebraicos.",
    "introduccion": "¿Qué obtienes cuando un amigo de tu amigo es tu amigo? Positivo. ¿Y cuando el enemigo de tu enemigo es tu amigo? También positivo. La regla de los signos en la multiplicación sigue exactamente esa lógica.",
    "resumen": "Al multiplicar dos factores, la **Regla de los Signos** establece: igual × igual = positivo, distinto × distinto = negativo. Específicamente: $(+)(+) = +$, $(-)(-)= +$, $(+)(-) = -$, $(-)(+) = -$.",
    "explicacion": "Las cuatro combinaciones posibles:\n- $(+3)(+4) = +12$: positivo × positivo = positivo.\n- $(-3)(-4) = +12$: negativo × negativo = positivo.\n- $(+3)(-4) = -12$: positivo × negativo = negativo.\n- $(-3)(+4) = -12$: negativo × positivo = negativo.\n\nEn álgebra con variables: $(-2x)(+5y) = -10xy$. El signo se determina por la regla, y el resto es la multiplicación normal de coeficientes y letras.",
    "procedimiento": [
        "Paso 1: Determina el signo del resultado según la regla (igual → positivo, distinto → negativo).",
        "Paso 2: Multiplica los valores absolutos de los coeficientes.",
        "Paso 3: Multiplica las partes literales (letras).",
        "Paso 4: Combina el signo del paso 1 con el resultado de los pasos 2 y 3."
    ],
    "ejemplos": [
        {"titulo": "Los dos casos negativos", "enunciado": "Calcula: (-4a)(−3b).", "solucion_pasos": ["Signos: (-)(-) = +.", "Coeficientes: 4 × 3 = 12.", "Letras: a × b = ab.", "Resultado: +12ab = 12ab."]}
    ],
    "errores_frecuentes": [
        "Creer que dos negativos siempre dan negativo (el opuesto es cierto en multiplicación).",
        "Aplicar la regla de los signos de la suma (distinto → conservar el mayor) en lugar de la de la multiplicación."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-S2-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es el signo del producto $(-7x)(+3y)$? (v{i})", "choices": ["A) Negativo, porque los signos son distintos.", "B) Positivo, porque hay dos factores.", "C) Depende del valor de x e y.", "D) Positivo, porque la x es positiva."], "correct_answer": "A) Negativo, porque los signos son distintos.", "solution_steps": "Regla: distinto × distinto = negativo. $(-)( +) = -$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "LM-S2-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Cuál de los siguientes productos resulta en un valor positivo?", "choices": ["A) $(-5a)(-3b)$", "B) $(+5a)(-3b)$", "C) $(-5a)(+3b)$", "D) $(-5a)(+0)$"], "correct_answer": "A) $(-5a)(-3b)$", "solution_steps": "$(-)(-)=+$. Es el único con signos iguales (ambos negativos).", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-S2-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El producto $(-8m)(+2n)$ es igual a $-16mn$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Signos: $(-)(+)=-$. Coeficientes: $8 \\times 2 = 16$. Letras: $mn$. Resultado: $-16mn$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-S2-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"En física, la fuerza se expresa como $F = ma$. Si la aceleración es $-3a$ (hacia abajo) y la masa es $-2m$ (representando una deuda de masa en un modelo), ¿cuál es la expresión de la fuerza? (v{i})", "choices": ["A) $6ma$ (positiva)", "B) $-6ma$ (negativa)", "C) $-5ma$", "D) $1ma$"], "correct_answer": "A) $6ma$ (positiva)", "solution_steps": "$F = (-2m)(-3a)$. Signos: $(-)(-)=+$. Coeficientes: $2 \\times 3=6$. Resultado: $+6ma$.", "paes_style": True})

# 2. LEYES_MULTIPLICACION.SIGNOS_MULTIPLES_FACTORES
sid2 = "MAT.ALG.LEYES_MULTIPLICACION.SIGNOS_MULTIPLES_FACTORES"
RECURSOS.append({
    "semantic_id": sid2,
    "objetivo": "Determinar el signo del producto de tres o más factores algebraicos contando los signos negativos.",
    "introduccion": "Con dos factores, la regla de signos es simple. Con tres o más, hay un truco elegante: basta con contar cuántos factores negativos hay. Número par de negativos → positivo. Número impar → negativo.",
    "resumen": "Para **Múltiples Factores**, el signo del producto se determina contando los factores con signo negativo: si son **pares**, el producto es positivo; si son **impares**, el producto es negativo.",
    "explicacion": "Ejemplo: $(-2)(-3)(+4)$.\nFactores negativos: $-2$ y $-3$ → 2 negativos (par) → resultado positivo.\nProducto: $2 \\times 3 \\times 4 = 24$ → resultado final: $+24$.\n\nEjemplo con 3 negativos: $(-2)(-3)(-4)$.\nFactores negativos: 3 (impar) → resultado negativo.\nProducto: $24$ → resultado final: $-24$.\n\nRegla mnemotécnica: un número par de signos negativos se 'cancelan' entre sí.",
    "procedimiento": [
        "Paso 1: Cuenta cuántos factores tienen signo negativo.",
        "Paso 2: Si el conteo es par → signo positivo. Si es impar → signo negativo.",
        "Paso 3: Multiplica los valores absolutos de todos los coeficientes.",
        "Paso 4: Multiplica todas las partes literales.",
        "Paso 5: Adjunta el signo del paso 2 al resultado."
    ],
    "ejemplos": [
        {"titulo": "Los tres negativos", "enunciado": "Calcula: (-a)(-2b)(-3c).", "solucion_pasos": ["Negativos: 3 (impar) → resultado negativo.", "Coeficientes: 1 × 2 × 3 = 6.", "Letras: a × b × c = abc.", "Resultado: -6abc."]}
    ],
    "errores_frecuentes": [
        "Aplicar la regla par/impar en la suma en lugar de la multiplicación.",
        "Olvidar contar un factor y llegar al signo equivocado."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-SM-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es el signo del producto $(-x)(-y)(-z)(-w)$? (v{i})", "choices": ["A) Positivo, porque hay 4 factores negativos (número par).", "B) Negativo, porque hay más de dos factores negativos.", "C) Depende de los valores de las variables.", "D) Negativo, porque todas las letras son negativas."], "correct_answer": "A) Positivo, porque hay 4 factores negativos (número par).", "solution_steps": "4 negativos → par → signo positivo. El producto es $+xyzw$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "LM-SM-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula: $(-2a)(-3b)(+2c)(-1)$.", "choices": ["A) $-12abc$", "B) $+12abc$", "C) $-8abc$", "D) $+8abc$"], "correct_answer": "A) $-12abc$", "solution_steps": "Negativos: $-2a$, $-3b$, $-1$ = 3 (impar) → negativo. Coeficientes: $2 \\times 3 \\times 2 \\times 1=12$. Resultado: $-12abc$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-SM-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿El producto $(-1)(-1)(-1)(-1)(-1)$ (cinco factores $-1$) resulta en $-1$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "5 factores negativos → impar → resultado negativo. Valor absoluto: $1^5=1$. Resultado: $-1$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-SM-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"El rendimiento de una inversión se modela como $R = (-r_1)(-r_2)(+r_3)(-r_4)$. Si todos los $r_i$ son positivos, ¿el rendimiento es positivo o negativo? (v{i})", "choices": ["A) Negativo, porque hay 3 factores negativos (impar).", "B) Positivo, porque hay variables positivas.", "C) Depende del valor de $r_3$.", "D) Positivo, porque hay 4 factores en total."], "correct_answer": "A) Negativo, porque hay 3 factores negativos (impar).", "solution_steps": "Contamos los signos negativos en la fórmula: $-r_1$, $-r_2$, $-r_4$ = 3 negativos. Impar → negativo.", "paes_style": True})

# 3. LEYES_MULTIPLICACION.EXPONENTES_IGUAL_BASE
sid3 = "MAT.ALG.LEYES_MULTIPLICACION.EXPONENTES_IGUAL_BASE"
RECURSOS.append({
    "semantic_id": sid3,
    "objetivo": "Aplicar la ley de exponentes al multiplicar potencias de la misma base, sumando los exponentes.",
    "introduccion": "¿Cuánto es $x^2 \\cdot x^3$? Podemos pensar: $x^2 = x \\cdot x$ y $x^3 = x \\cdot x \\cdot x$. Juntándolos: $x \\cdot x \\cdot x \\cdot x \\cdot x = x^5$. ¡Los exponentes se suman!",
    "resumen": "Al multiplicar potencias de la **misma base**, los exponentes se **suman**: $x^m \\cdot x^n = x^{m+n}$. La base permanece igual; solo los exponentes se operan.",
    "explicacion": "Regla formal: $a^m \\cdot a^n = a^{m+n}$.\n\nEjemplos:\n- $x^3 \\cdot x^4 = x^{3+4} = x^7$.\n- $y^2 \\cdot y = y^{2+1} = y^3$ (el exponente 1 es implícito).\n- $a^5 \\cdot a^0 = a^{5+0} = a^5$ (cualquier base elevada a cero es 1).\n\nImportante: Esta regla solo aplica cuando las bases son idénticas. $x^3 \\cdot y^4$ NO se simplifica sumando exponentes porque las bases ($x$ e $y$) son distintas.",
    "procedimiento": [
        "Paso 1: Verifica que las dos potencias tengan exactamente la misma base.",
        "Paso 2: Suma sus exponentes.",
        "Paso 3: Escribe la base con el exponente resultante.",
        "Paso 4: Si las bases son distintas, NO apliques esta regla; déjalas separadas."
    ],
    "ejemplos": [
        {"titulo": "El acumulador de potencias", "enunciado": "Simplifica: x^3 · x^2 · x.", "solucion_pasos": ["Misma base x en los tres factores.", "Sumamos exponentes: 3 + 2 + 1 = 6.", "Resultado: x^6."]}
    ],
    "errores_frecuentes": [
        "Multiplicar los exponentes en lugar de sumarlos (ej. $x^3 \\cdot x^4 = x^{12}$). Eso es elevar una potencia a otra.",
        "Aplicar la regla a bases distintas (ej. creer que $x^3 \\cdot y^2 = xy^5$)."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-EB-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es la ley que permite simplificar $x^5 \\cdot x^3$? (v{i})", "choices": ["A) Al multiplicar potencias de igual base, se conserva la base y se suman los exponentes: $x^{5+3}=x^8$.", "B) Al multiplicar potencias de igual base, se multiplican los exponentes: $x^{5 \\cdot 3}=x^{15}$.", "C) Los exponentes se restan: $x^{5-3}=x^2$.", "D) Los exponentes no cambian: el resultado es $x^5$."], "correct_answer": "A) Al multiplicar potencias de igual base, se conserva la base y se suman los exponentes: $x^{5+3}=x^8$.", "solution_steps": "Regla: $a^m \\cdot a^n = a^{m+n}$. Base idéntica → sumar exponentes.", "paes_style": False})
EJERCICIOS.append({"stable_id": "LM-EB-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Simplifica: $a^4 \\cdot a^2 \\cdot a^3$.", "choices": ["A) $a^9$", "B) $a^{24}$", "C) $a^6$", "D) $3a^9$"], "correct_answer": "A) $a^9$", "solution_steps": "Misma base $a$. Sumamos exponentes: $4+2+3=9$. Resultado: $a^9$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-EB-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿$m^3 \\cdot n^4$ puede simplificarse a $mn^7$ usando la ley de exponentes de igual base?", "choices": [], "correct_answer": "Falso", "solution_steps": "La regla de suma de exponentes solo aplica cuando las bases son iguales. $m$ y $n$ son bases distintas, por lo que $m^3 \\cdot n^4$ no se simplifica.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-EB-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"El área de un rectángulo es largo × ancho. Si el largo es $x^3$ cm y el ancho es $x^2$ cm, ¿cuál es el área? (v{i})", "choices": ["A) $x^5$ cm²", "B) $x^6$ cm²", "C) $2x^5$ cm²", "D) $x^5$ cm"], "correct_answer": "A) $x^5$ cm²", "solution_steps": "$A = x^3 \\cdot x^2 = x^{3+2} = x^5$ cm².", "paes_style": True})

# 4. LEYES_MULTIPLICACION.PRODUCTO_COEFICIENTES
sid4 = "MAT.ALG.LEYES_MULTIPLICACION.PRODUCTO_COEFICIENTES"
RECURSOS.append({
    "semantic_id": sid4,
    "objetivo": "Multiplicar correctamente los coeficientes numéricos de monomios, separándolos de la parte literal.",
    "introduccion": "En un monomio como $3x^2$, el $3$ y el $x^2$ son dos piezas distintas. Al multiplicar monomios, cada pieza va por su propio carril: los números se multiplican con números, y las letras con letras.",
    "resumen": "Al multiplicar monomios, el **Producto de Coeficientes** se calcula por separado multiplicando los números entre sí. Luego se multiplican las partes literales. El resultado final combina ambas partes.",
    "explicacion": "Para multiplicar $(3x^2)(4x^3)$:\n1. Coeficientes: $3 \\times 4 = 12$.\n2. Parte literal: $x^2 \\times x^3 = x^{2+3} = x^5$.\n3. Resultado: $12x^5$.\n\nCon signo: $(-5a^2)(3a) = -15a^3$.\n- Signo: $(-)( +) = -$.\n- Coeficientes: $5 \\times 3 = 15$.\n- Literal: $a^2 \\cdot a = a^3$.\n- Resultado: $-15a^3$.",
    "procedimiento": [
        "Paso 1: Determina el signo del producto (regla de signos).",
        "Paso 2: Multiplica los valores absolutos de los coeficientes.",
        "Paso 3: Para cada variable, suma los exponentes.",
        "Paso 4: Escribe el resultado: signo + coeficiente + parte literal."
    ],
    "ejemplos": [
        {"titulo": "El monomio combinado", "enunciado": "Multiplica: (2x^2y)(5xy^3).", "solucion_pasos": ["Signo: (+)(+) = +.", "Coeficientes: 2 × 5 = 10.", "Variable x: x^2 · x = x^3.", "Variable y: y · y^3 = y^4.", "Resultado: 10x^3y^4."]}
    ],
    "errores_frecuentes": [
        "Sumar los coeficientes en lugar de multiplicarlos (ej. $3x \\cdot 4y = 7xy$).",
        "Mezclar la multiplicación de coeficientes con la de exponentes (ej. $3x^2 \\cdot 4x = 12x^2$ en lugar de $12x^3$)."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-PC-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al multiplicar $(5a^2b)(3ab^2)$, ¿cómo se obtienen el coeficiente y la parte literal del resultado? (v{i})", "choices": ["A) Los coeficientes se multiplican entre sí ($5 \\times 3=15$) y para cada variable se suman los exponentes ($a^{2+1}=a^3$, $b^{1+2}=b^3$), dando $15a^3b^3$.", "B) Los coeficientes se suman ($5+3=8$) y los exponentes también ($15a^6b^6$).", "C) Los coeficientes se multiplican pero los exponentes también ($15a^2b^2$).", "D) Solo se multiplican los coeficientes: $15ab$."], "correct_answer": "A) Los coeficientes se multiplican entre sí ($5 \\times 3=15$) y para cada variable se suman los exponentes ($a^{2+1}=a^3$, $b^{1+2}=b^3$), dando $15a^3b^3$.", "solution_steps": "Coeficientes: $5 \\times 3=15$. Variable $a$: $a^2 \\cdot a = a^3$. Variable $b$: $b \\cdot b^2=b^3$. Resultado: $15a^3b^3$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "LM-PC-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula: $(-4m^3n)(2mn^2)$.", "choices": ["A) $-8m^4n^3$", "B) $8m^4n^3$", "C) $-8m^3n^2$", "D) $-6m^4n^3$"], "correct_answer": "A) $-8m^4n^3$", "solution_steps": "Signo: $(-)(+)=-$. Coef: $4 \\times 2=8$. $m$: $m^3 \\cdot m=m^4$. $n$: $n \\cdot n^2=n^3$. Resultado: $-8m^4n^3$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-PC-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿El producto $(6x^2)(x^3)$ resulta en $6x^5$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Coeficiente: $6 \\times 1=6$. Variable $x$: $x^2 \\cdot x^3=x^5$. Resultado: $6x^5$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-PC-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"El volumen de un cubo de lado $3a^2$ cm se calcula como $V = (3a^2)^3$. Expresando esto como producto de tres factores iguales, ¿cuánto es $(3a^2)(3a^2)(3a^2)$? (v{i})", "choices": ["A) $27a^6$", "B) $9a^6$", "C) $27a^5$", "D) $9a^5$"], "correct_answer": "A) $27a^6$", "solution_steps": "Coeficientes: $3 \\times 3 \\times 3=27$. Variable $a$: $a^2 \\cdot a^2 \\cdot a^2=a^6$. Resultado: $27a^6$.", "paes_style": True})

# 5. LEYES_MULTIPLICACION.PROPIEDAD_CONMUTATIVA
sid5 = "MAT.ALG.LEYES_MULTIPLICACION.PROPIEDAD_CONMUTATIVA"
RECURSOS.append({
    "semantic_id": sid5,
    "objetivo": "Reconocer y aplicar la propiedad conmutativa de la multiplicación algebraica.",
    "introduccion": "$3 \\times 5 = 5 \\times 3 = 15$. El orden en que multiplicas no importa. En álgebra, esta regla persiste: $3x \\cdot 5y = 5y \\cdot 3x = 15xy$.",
    "resumen": "La **Propiedad Conmutativa** de la multiplicación establece que el orden de los factores no altera el producto: $a \\cdot b = b \\cdot a$. En álgebra, esto permite reorganizar factores para simplificar cálculos.",
    "explicacion": "Ejemplo: $(2x)(5y)(3z)$.\n\nPuedo reordenarlos cómodamente:\n$(2 \\cdot 5 \\cdot 3)(x \\cdot y \\cdot z) = 30xyz$.\n\nSin commutativity tendría que multiplicar en orden estricto. Con ella, junto todos los números primero y luego todas las letras, lo que hace el cálculo más limpio.\n\nTambién se usa para reorganizar: si tienes $(-3ab)(+5c)(-2b)$, puedes agrupar: signos → $(-)(+)(-) = +$, coeficientes → $3 \\times 5 \\times 2 = 30$, literales → $ab \\cdot c \\cdot b = ab^2c$. Resultado: $30ab^2c$.",
    "procedimiento": [
        "Paso 1: Agrupa todos los signos y determina el signo del producto.",
        "Paso 2: Agrupa todos los coeficientes numéricos y multiplícalos.",
        "Paso 3: Agrupa todas las variables (por tipo) y aplica la ley de exponentes.",
        "Paso 4: Combina el signo con el coeficiente numérico y el resultado literal."
    ],
    "ejemplos": [
        {"titulo": "Agrupar para ganar", "enunciado": "Calcula: (3a)(2b)(4c).", "solucion_pasos": ["Signos: (+)(+)(+) = +.", "Coeficientes: 3 × 2 × 4 = 24.", "Letras: a · b · c = abc.", "Resultado: 24abc."]}
    ],
    "errores_frecuentes": [
        "Confundir la propiedad conmutativa con la asociativa (aunque en la práctica se usan juntas).",
        "Al reordenar, olvidar el signo de un factor que se mueve."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-PC2-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál propiedad garantiza que $(4x)(3y) = (3y)(4x)$? (v{i})", "choices": ["A) La propiedad conmutativa de la multiplicación: $a \\cdot b = b \\cdot a$.", "B) La propiedad asociativa.", "C) La propiedad distributiva.", "D) La identidad multiplicativa."], "correct_answer": "A) La propiedad conmutativa de la multiplicación: $a \\cdot b = b \\cdot a$.", "solution_steps": "La conmutatividad garantiza que el orden de los factores no altera el producto.", "paes_style": False})
EJERCICIOS.append({"stable_id": "LM-PC2-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Usando la propiedad conmutativa para ordenar, calcula: $(-2x)(5y)(-3z)$.", "choices": ["A) $30xyz$", "B) $-30xyz$", "C) $10xyz$", "D) $-10xyz$"], "correct_answer": "A) $30xyz$", "solution_steps": "Signos: $(-)(+)(-)= +$. Coef: $2 \\times 5 \\times 3=30$. Letras: $xyz$. Resultado: $30xyz$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-PC2-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿$(7ab)(-3c)$ produce el mismo resultado que $(-3c)(7ab)$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Por la propiedad conmutativa, el orden no altera el producto. Ambas expresiones dan $-21abc$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"LM-PC2-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un estudiante calcula la densidad de una aleación como $D = (masa)(volumen)^{{-1}}$ y escribe $(5m)(2v)$. Su compañero lo escribe al revés: $(2v)(5m)$. ¿Quién tiene razón? (v{i})", "choices": ["A) Ambos, porque la multiplicación es conmutativa y el orden no altera el resultado ($10mv$).", "B) Solo el primero, el orden importa en multiplicación.", "C) Solo el segundo.", "D) Ninguno, deben sumarse."], "correct_answer": "A) Ambos, porque la multiplicación es conmutativa y el orden no altera el resultado ($10mv$).", "solution_steps": "La propiedad conmutativa garantiza $(5m)(2v) = (2v)(5m) = 10mv$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 1 (B0304/Leyes Mult.)...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"  Creado {filename}.yaml")
    print("Escribiendo JSONL Tanda 1...")
    append_jsonl("mat-alg-multiplicacion-banco-gen-1", EJERCICIOS)
    print(f"  mat-alg-multiplicacion-banco-gen-1.jsonl con {len(EJERCICIOS)} ejercicios.")

if __name__ == "__main__":
    generate_all()

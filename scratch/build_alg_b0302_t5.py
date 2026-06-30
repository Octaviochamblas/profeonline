# scratch/build_alg_b0302_t5.py
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

# 21. CUBO_NUMERO
sid21 = "MAT.ALG.LENGUAJE_RELACIONES.CUBO_NUMERO"
RECURSOS.append({
    "semantic_id": sid21, "objetivo": "Traducir correctamente la operación de elevar al cubo en contraposición a multiplicar por tres.",
    "introduccion": "Si el cuadrado era el área de una figura plana, el cubo nos da el volumen, la tercera dimensión. Es un crecimiento exponencial aún más acelerado.",
    "resumen": "El **Cubo de un Número** se traduce elevando la variable a la potencia de tres ($x^3$). Representa el volumen de un cubo de arista $x$, o el producto del número por sí mismo tres veces ($x \\cdot x \\cdot x$).",
    "explicacion": "Al igual que con el cuadrado, no debemos confundir el múltiplo con la potencia:\n- 'El triple de un número' $\\rightarrow$ $3x$ (multiplicación).\n- 'El cubo de un número' $\\rightarrow$ $x^3$ (potenciación).\n\nY la regla de los paréntesis sigue siendo sagrada:\n- 'El cubo de la diferencia' $\\rightarrow$ $(x - y)^3$.\n- 'La diferencia de los cubos' $\\rightarrow$ $x^3 - y^3$.",
    "procedimiento": ["Paso 1: Identifica a qué entidad se le está aplicando el 'cubo'.", "Paso 2: Si es a una variable simple, agrégale el exponente 3 ($a^3$).", "Paso 3: Si es a un polinomio o a un resultado de una operación (ej. la suma de dos números), agrupa primero la operación entre paréntesis y pon el exponente 3 fuera del grupo ($(a+b)^3$)."],
    "ejemplos": [
        {"titulo": "Volumen algebraico", "enunciado": "Traduce algebraicamente: 'El cubo de la suma entre un número y dos'.", "solucion_pasos": ["La base que será elevada es la suma de un número y dos: (x + 2).", "Se nos pide 'el cubo' de toda esa suma.", "Traducción correcta: (x + 2)^3."]}
    ],
    "errores_frecuentes": ["Confundir el triple ($3x$) con el cubo ($x^3$).", "Escribir mal el orden de operaciones por falta de paréntesis. (Ej: 'el cubo del doble de x' escrito como $2x^3$ en lugar de $(2x)^3$)."],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CUBO-CONC-{i}", "semantic_id": sid21, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al modelar un crecimiento acelerado, ¿cuál es la distinción formal entre la traducción de 'el triple de una variable' y 'el cubo de una variable'? (v{i})", "choices": ["A) El 'triple' representa una multiplicación lineal por $3$ ($3x$), mientras que el 'cubo' representa elevar la variable a la potencia de $3$ ($x^3$).", "B) Ambas expresiones significan lo mismo en álgebra básica.", "C) El cubo representa una raíz cúbica, mientras que el triple es una multiplicación.", "D) El cubo requiere multiplicar la variable por un número impar."], "correct_answer": "A) El 'triple' representa una multiplicación lineal por $3$ ($3x$), mientras que el 'cubo' representa elevar la variable a la potencia de $3$ ($x^3$).", "solution_steps": "El triple aumenta el valor de forma progresiva. El cubo ($x \\cdot x \\cdot x$) lo hace de forma volumétrica o exponencial.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"CUBO-REC-1", "semantic_id": sid21, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Indica cuál de las siguientes expresiones traduce: 'La suma de los cubos de tres cantidades'.", "choices": ["A) $a^3 + b^3 + c^3$", "B) $(a + b + c)^3$", "C) $3a + 3b + 3c$", "D) $a^3 b^3 c^3$"], "correct_answer": "A) $a^3 + b^3 + c^3$", "solution_steps": "Se piden 'los cubos' (individuales) de tres cantidades, que luego se suman. El resultado es $a^3 + b^3 + c^3$. La opción B sería 'el cubo de la suma'.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CUBO-PROC-{i}", "semantic_id": sid21, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿Si se enuncia 'el cubo del cuádruple de $x$', la expresión $(4x)^3$ es la única forma matemáticamente correcta de traducirlo sin desarrollar la potencia?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Primero construimos el cuádruple ($4x$). Luego aplicamos el cubo a todo ese bloque usando paréntesis: $(4x)^3$. Si escribimos $4x^3$, el 4 quedaría sin elevarse al cubo.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CUBO-PAES-{i}", "semantic_id": sid21, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"El algoritmo de un software financiero penaliza el riesgo ($R$) según la siguiente política textual: 'La penalidad es igual al cubo de la diferencia entre el riesgo actual y el riesgo base ($B$)'. Si un programador escribió la fórmula de penalidad como $P = R^3 - B^3$, ¿qué ocurrirá con el cálculo? (v{i})", "choices": ["A) El cálculo será erróneo porque el programador modeló 'la diferencia de los cubos'. La traducción correcta para 'el cubo de la diferencia' requería paréntesis: $P = (R - B)^3$.", "B) El cálculo será correcto porque $(R - B)^3$ es idéntico a $R^3 - B^3$.", "C) El cálculo fallará porque la penalidad nunca puede ser negativa.", "D) El cálculo será erróneo porque debió multiplicar por 3."], "correct_answer": "A) El cálculo será erróneo porque el programador modeló 'la diferencia de los cubos'. La traducción correcta para 'el cubo de la diferencia' requería paréntesis: $P = (R - B)^3$.", "solution_steps": "La frase 'el cubo de...' exige que el cubo sea la operación principal (exterior). Lo de adentro es 'la diferencia'. Queda $(R - B)^3$. El error del programador es clásico en álgebra.", "paes_style": True})

# 22. EXCESO_NUMERO
sid22 = "MAT.ALG.LENGUAJE_RELACIONES.EXCESO_NUMERO"
RECURSOS.append({
    "semantic_id": sid22, "objetivo": "Comprender y traducir el concepto de 'exceso', que equivale matemáticamente a una diferencia o resta.",
    "introduccion": "Cuando decimos que un camión 'excede' el límite de peso por 500 kilos, estamos hablando de lo que le sobra. Y la única forma matemática de calcular cuánto le sobra a algo, es mediante la resta.",
    "resumen": "El **Exceso de un número sobre otro** se traduce planteando una **resta** donde la primera cantidad (el que excede) es el minuendo, y la segunda (el que es excedido) es el sustraendo: **$x - y$**.",
    "explicacion": "Palabras clave:\n- El exceso de A sobre B: $A - B$\n- A excede a B en C: $A - B = C$\n- Lo que B es excedido por A: $A - B$\n\nFrecuentemente, el concepto de exceso asusta por su redacción rebuscada. Sin embargo, 'el exceso de 10 sobre 7' es simplemente preguntar '¿cuánto le sobra al 10 para igualar al 7?'. La respuesta es la resta: $10 - 7 = 3$.\nEn álgebra, 'El exceso del doble de un número sobre 5 es 11' se traduce como: $2x - 5 = 11$.",
    "procedimiento": ["Paso 1: Identifica a la entidad mayor (la que excede). Escríbela primero.", "Paso 2: Escribe el signo de resta (-).", "Paso 3: Identifica a la entidad menor (la que es superada). Escríbela después del signo menos.", "Paso 4: Si te dan el valor exacto del exceso, iguálalo a la resta (Ej. ... = 10)."],
    "ejemplos": [
        {"titulo": "Lo que sobra", "enunciado": "Traduce algebraicamente: 'El exceso de tu salario sobre tus gastos es de mil dólares'.", "solucion_pasos": ["El que excede (el mayor): Salario (S).", "El superado (el menor): Gastos (G).", "La resta del exceso: S - G.", "El valor del exceso es mil: S - G = 1000."]}
    ],
    "errores_frecuentes": ["Confundir el 'exceso' con un 'aumento', y sumar las variables ($A+B$) en lugar de restarlas.", "Invertir el orden de la resta (escribir $B - A$ en lugar de $A - B$)."],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"EXCE-CONC-{i}", "semantic_id": sid22, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"¿Qué operación aritmética fundamental es requerida para calcular algebraicamente 'el exceso' de una cantidad $A$ sobre una cantidad $B$? (v{i})", "choices": ["A) Una sustracción, estableciendo a la cantidad $A$ como el minuendo y a la $B$ como el sustraendo ($A - B$).", "B) Una adición, sumando el exceso a la cantidad menor.", "C) Una división entre $A$ y $B$.", "D) Un cálculo de porcentaje sobre $A$."], "correct_answer": "A) Una sustracción, estableciendo a la cantidad $A$ como el minuendo y a la $B$ como el sustraendo ($A - B$).", "solution_steps": "El exceso mide cuánto más grande es A en comparación con B. Eso es, por definición, la distancia entre ellos en la recta numérica, lo que se calcula restando $A - B$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"EXCE-REC-1", "semantic_id": sid22, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Selecciona la ecuación correcta que traduce el enunciado: 'El exceso del triple de un número sobre diez es igual a veinte'.", "choices": ["A) $3x - 10 = 20$", "B) $3x + 10 = 20$", "C) $10 - 3x = 20$", "D) $3(x - 10) = 20$"], "correct_answer": "A) $3x - 10 = 20$", "solution_steps": "El mayor es el triple del número ($3x$). El menor es el diez ($10$). El exceso es la resta ($3x - 10$). Como es igual a veinte: $3x - 10 = 20$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"EXCE-PROC-{i}", "semantic_id": sid22, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿La afirmación 'la edad de Juan excede a la de Pedro en $5$ años' puede ser traducida válidamente tanto con la ecuación de diferencia ($J - P = 5$) como con una ecuación de igualación compensada ($J = P + 5$)?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Ambas formas son 100% equivalentes y correctas. $J - P = 5$ es la definición de exceso. Si despejamos J, obtenemos $J = P + 5$, que representa la lógica de 'Pedro más 5 años iguala a Juan'.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"EXCE-PAES-{i}", "semantic_id": sid22, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Un contrato de alquiler estipula: 'La multa a pagar será equivalente al cuadrado del exceso de los días de retraso ($d$) sobre los días de gracia permitidos ($g$)'. ¿Cuál es la fórmula matemática que define la multa ($M$)? (v{i})", "choices": ["A) $M = (d - g)^2$", "B) $M = d^2 - g^2$", "C) $M = d + g^2$", "D) $M = (g - d)^2$"], "correct_answer": "A) $M = (d - g)^2$", "solution_steps": "Primero determinamos el exceso de retraso sobre gracia: $d - g$. Luego se nos pide el cuadrado de esa cantidad entera (del exceso). Entonces encerramos en paréntesis y elevamos: $(d - g)^2$.", "paes_style": True})

# 23. MAYOR_QUE
sid23 = "MAT.ALG.LENGUAJE_RELACIONES.MAYOR_QUE"
RECURSOS.append({
    "semantic_id": sid23, "objetivo": "Traducir relaciones de desigualdad donde una cantidad es superior a otra.",
    "introduccion": "Hasta ahora hemos sido los reyes de la igualdad. Todo era perfecto y estaba en equilibrio. Pero en la vida real, las cosas rara vez son iguales. Bienvenido al mundo de las inecuaciones.",
    "resumen": "La relación **'Mayor que'** se traduce utilizando el símbolo de desigualdad estricta **$>$**. La punta abierta o 'boca' del símbolo siempre apunta hacia la cantidad más grande.",
    "explicacion": "Palabras clave:\n- A es mayor que B: $A > B$\n- Es superior a\n- Supera a\n- Más que\n\nEjemplos:\n- 'El salario de un gerente es mayor que el de un analista': $G > A$\n- 'El doble de un número es superior a cien': $2x > 100$\n\n¿Por qué es importante el sentido? Porque, a diferencia de la igualdad, si inviertes los lados tienes que invertir el símbolo. Si $A > B$, entonces obligatoriamente $B < A$.",
    "procedimiento": ["Paso 1: Identifica qué entidad es la más grande en la comparación.", "Paso 2: Escribe esa entidad en el lado izquierdo.", "Paso 3: Dibuja el símbolo > (la boca abierta mirando a la entidad grande).", "Paso 4: Escribe la entidad más pequeña en el lado derecho."],
    "ejemplos": [
        {"titulo": "Rompiendo barreras", "enunciado": "Traduce: 'La suma de las ventas de hoy y ayer superan los cinco mil dólares'.", "solucion_pasos": ["Suma de ventas de hoy y ayer: H + A.", "Es superior a (>) cinco mil (5000).", "Traducción: H + A > 5000."]}
    ],
    "errores_frecuentes": ["Confundir los símbolos $>$ (mayor) con $<$ (menor). (Regla nemotécnica: el pez grande se come al chico, la boca abierta va hacia el mayor).", "Asumir que 'mayor que' implica una suma."],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"MAYQ-CONC-{i}", "semantic_id": sid23, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En la sintaxis de las inecuaciones matemáticas, ¿qué indica direccionalmente la abertura ('boca') del símbolo '$>$'? (v{i})", "choices": ["A) Siempre apunta (se abre) hacia la cantidad que tiene el valor absoluto o real más alto en la relación de desigualdad.", "B) Siempre apunta hacia la incógnita, sin importar si es mayor o menor.", "C) Siempre apunta hacia la derecha, por convención de lectura.", "D) Indica que el lado hacia donde se abre es un número negativo."], "correct_answer": "A) Siempre apunta (se abre) hacia la cantidad que tiene el valor absoluto o real más alto en la relación de desigualdad.", "solution_steps": "La regla visual del símbolo es que la parte más ancha (la abertura) enfrenta a la expresión más grande, mientras el vértice (la punta) apunta al menor.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"MAYQ-REC-1", "semantic_id": sid23, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Identifica la traducción correcta para el enunciado: 'El volumen del cilindro ($V$) es superior a 400 litros'.", "choices": ["A) $V > 400$", "B) $V < 400$", "C) $V = 400$", "D) $V \\ge 400$"], "correct_answer": "A) $V > 400$", "solution_steps": "La palabra 'superior a' indica estricta mayoridad. El símbolo adecuado es $>$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"MAYQ-PROC-{i}", "semantic_id": sid23, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿La afirmación '$A > B$' es matemáticamente idéntica y produce los mismos resultados que la afirmación '$B < A$' en cualquier contexto algebraico?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Decir que A es mayor que B implica, por lógica inversa obligatoria, que B es menor que A. Son dos formas de escribir exactamente la misma inecuación.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"MAYQ-PAES-{i}", "semantic_id": sid23, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una aerolínea dicta en sus políticas: 'El peso del equipaje ($P$) más el peso del pasajero ($M$) no debe ser igual a la capacidad máxima ($C$), de hecho, debe ser siempre un valor que la sobrepase para justificar el uso de aviones grandes'. ¿Cuál es la inecuación que modela esta extraña política? (v{i})", "choices": ["A) $P + M > C$", "B) $P + M < C$", "C) $P + M \\ge C$", "D) $P > M + C$"], "correct_answer": "A) $P + M > C$", "solution_steps": "La suma de ambos pesos ($P+M$) debe 'sobrepasar' (ser estrictamente mayor que) la capacidad ($C$). Esto se traduce sin ambigüedades como $P + M > C$.", "paes_style": True})

# 24. MENOR_QUE
sid24 = "MAT.ALG.LENGUAJE_RELACIONES.MENOR_QUE"
RECURSOS.append({
    "semantic_id": sid24, "objetivo": "Traducir relaciones de desigualdad donde una cantidad es inferior a otra.",
    "introduccion": "Los límites de velocidad en las carreteras son un ejemplo clásico. Nadie te prohíbe ir más lento, la regla es ser inferior al límite. El álgebra modela los 'techos' con el símbolo menor que.",
    "resumen": "La relación **'Menor que'** se traduce utilizando el símbolo de desigualdad estricta **$<$**. La punta cerrada o 'vértice' del símbolo siempre apunta hacia la cantidad más pequeña.",
    "explicacion": "Palabras clave:\n- A es menor que B: $A < B$\n- Es inferior a\n- No alcanza a\n- Está por debajo de\n\nEjemplos:\n- 'La edad de María es menor que la de Juan': $M < J$\n- 'El costo de producción no alcanzó los mil dólares': $C < 1000$\n\nNuevamente, hablamos de desigualdad **estricta**. Si una velocidad límite es de 100 km/h y te dicen que vayas a una velocidad 'menor que' 100, ir a 100 exactos está prohibido. Debe ser 99.9 o menos.",
    "procedimiento": ["Paso 1: Identifica la entidad más pequeña. Escríbela en el lado izquierdo.", "Paso 2: Dibuja el símbolo < (la punta afilada mirando a la entidad pequeña).", "Paso 3: Escribe el 'techo' o entidad mayor en el lado derecho."],
    "ejemplos": [
        {"titulo": "Por debajo del radar", "enunciado": "Traduce algebraicamente: 'El doble del peso es inferior a sesenta kilos'.", "solucion_pasos": ["El doble del peso: 2P.", "Es inferior a: <.", "El límite superior: 60.", "Traducción completa: 2P < 60."]}
    ],
    "errores_frecuentes": ["Confundir 'menor que' con 'menor o igual a'.", "Invertir los lados de la inecuación al plantearla mentalmente de atrás hacia adelante."],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"MENQ-CONC-{i}", "semantic_id": sid24, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En el planteamiento de inecuaciones estrictas, ¿qué característica diferencial define a una relación 'menor que' ($<$) frente a una relación de igualdad ($=$)? (v{i})", "choices": ["A) La relación 'menor que' prohíbe explícitamente que la primera cantidad alcance el valor exacto de la segunda cantidad, marcándola como un límite inalcanzable.", "B) Ninguna, ambas permiten que las cantidades sean exactamente iguales.", "C) La relación 'menor que' significa que el resultado siempre será un número decimal.", "D) La relación 'menor que' solo aplica para comparar cantidades negativas."], "correct_answer": "A) La relación 'menor que' prohíbe explícitamente que la primera cantidad alcance el valor exacto de la segunda cantidad, marcándola como un límite inalcanzable.", "solution_steps": "El símbolo $<$ es estricto. Si $x < 10$, $x$ jamás podrá ser 10.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"MENQ-REC-1", "semantic_id": sid24, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Selecciona la expresión que traduce adecuadamente: 'El ingreso familiar ($I$) mensual está por debajo del salario mínimo ($M$)'.", "choices": ["A) $I < M$", "B) $I > M$", "C) $I \\le M$", "D) $I = M$"], "correct_answer": "A) $I < M$", "solution_steps": "La frase 'por debajo de' implica inferioridad estricta. El símbolo adecuado es el menor que ($<$).", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"MENQ-PROC-{i}", "semantic_id": sid24, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿Si un texto indica 'la tercera parte de la edad de Ana no alcanza a igualar los $15$ años', la traducción algebraica correcta es $\\frac{A}{3} < 15$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "La frase 'no alcanza a igualar' significa que se queda corta, es decir, es estrictamente menor. La tercera parte se modela como $\\frac{A}{3}$. La inecuación $\\frac{A}{3} < 15$ es perfecta.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"MENQ-PAES-{i}", "semantic_id": sid24, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Las especificaciones de un ascensor detallan: 'Para que el sistema de poleas no sufra daño estructural, la suma de las masas de los ocupantes ($M$) y la masa de la cabina ($C$) debe ser inferior al límite de resistencia del cable ($R$)'. ¿Qué modelo algebraico debe implementar el sensor de seguridad? (v{i})", "choices": ["A) $M + C < R$", "B) $M + C > R$", "C) $M + C \\le R$", "D) $M - C < R$"], "correct_answer": "A) $M + C < R$", "solution_steps": "La suma de ambas masas es $M + C$. El texto exige que esta suma sea 'inferior a' (estrictamente menor que) el límite de resistencia R. El sensor debe verificar que $M + C < R$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 5 (MAT.ALG.B0302)...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 5 (MAT.ALG.B0302)...")
    append_jsonl("mat-alg-lenguaje-banco-gen-5", EJERCICIOS)
    print("Creado mat-alg-lenguaje-banco-gen-5.jsonl con 40 ejercicios.")

if __name__ == "__main__":
    generate_all()

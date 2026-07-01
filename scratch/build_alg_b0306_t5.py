import os
import json

def to_yaml_list(items):
    return "\n  - '" + "'\n  - '".join(i.replace("'", "''") for i in items) + "'"

def format_multiline(text):
    return "\n  " + "\n  ".join(text.strip().split("\n"))

def build_node(sid, title, obj, intro, res, expl, proc, ex_a, ex_b, errs):
    filename = f"docs/conocimiento/contenido/{sid.lower().replace('.', '-').replace('_', '-')}.yaml"
    proc_yaml = to_yaml_list(proc)
    errs_yaml = to_yaml_list(errs)

    yaml_content = f"""semantic_id: '{sid}'
titulo: '{title.replace("'", "''")}'
objetivo: '{obj.replace("'", "''")}'
introduccion: |{format_multiline(intro)}
resumen: |{format_multiline(res)}
explicacion: |{format_multiline(expl)}
procedimiento:{proc_yaml}
ejemplos:"""

    for t, e, sp in ex_a:
        yaml_content += f"""
  - titulo: '{t.replace("'", "''")}'
    enunciado: '{e.replace("'", "''")}'
    solucion_pasos:{to_yaml_list(sp)}"""

    for t, r, sp in ex_b:
        yaml_content += f"""
  - titulo: '{t.replace("'", "''")}'
    respuesta: '{r}'
    solucion_pasos:{to_yaml_list(sp)}"""

    yaml_content += f"""
errores_frecuentes:{errs_yaml}
estado: publicado
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    print(f"Generado {filename}")

def append_exercises(sid, prefix, ex_list):
    filename = "docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-5.jsonl"
    with open(filename, 'a', encoding='utf-8') as f:
        for i, ex in enumerate(ex_list):
            group = ex['group']
            difficulty = ex['diff']
            prompt = ex['prompt']
            sol = ex['sol']
            if group == 'procedimiento_basico':
                doc = {
                    "stable_id": f"{prefix}-GEN-PROC-{i+1}",
                    "semantic_id": sid,
                    "item_group": group,
                    "format": "true_false",
                    "difficulty": difficulty,
                    "prompt": prompt,
                    "correct_answer": ex['ans'],
                    "solution_steps": sol,
                    "status": "ready",
                    "source_kind": "manual"
                }
            else:
                doc = {
                    "stable_id": f"{prefix}-GEN-{group[:4].upper()}-{i+1}",
                    "semantic_id": sid,
                    "item_group": group,
                    "format": "multiple_choice",
                    "difficulty": difficulty,
                    "prompt": prompt,
                    "choices": ex['choices'],
                    "correct_answer": ex['ans'],
                    "solution_steps": sol,
                    "status": "ready",
                    "source_kind": "manual",
                    "competencia": "M1" if not ex.get('paes') else "M2",
                    "paes_style": ex.get('paes', False)
                }
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

nodes = []

# 1. RECONOCIMIENTO_SUMA_CUBOS
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUBOS.RECONOCIMIENTO_SUMA_CUBOS",
    "title": "Reconocimiento de la Suma de Cubos",
    "obj": "Identificar visual y matemáticamente cuándo un binomio corresponde a una suma de dos cubos perfectos.",
    "intro": "Si la suma de cuadrados era un espejismo que no se podía factorizar, la Suma de Cubos es una grata sorpresa. En la tercera dimensión, las reglas de los signos cambian y permiten que $a^3 + b^3$ se pueda romper en piezas más pequeñas.",
    "res": "Una suma de cubos perfectos consta de dos términos positivos sumados, donde a cada término se le puede extraer raíz cúbica exacta (ej. $x^3, 8, 27y^6, 125$).",
    "expl": "Para reconocer una suma de cubos $A^3 + B^3$, debes hacer un simple 'control de calidad':\n1. Son exactamente dos términos.\n2. Hay un signo 'más' $(+)$ entre ellos.\n3. Ambos términos tienen raíz cúbica exacta.\n\nEjemplo: $8x^3 + 27$.\n- ¿Son dos términos sumados? Sí.\n- La raíz cúbica de $8x^3$ se calcula sacando raíz cúbica a 8 (que es 2, pues $2 \\times 2 \\times 2 = 8$) y raíz cúbica a $x^3$ (que es $x$). Por tanto, es $2x$.\n- La raíz cúbica de $27$ es 3 (pues $3 \\times 3 \\times 3 = 27$).\n\nComo ambos pasaron la prueba, estamos ante una Suma de Cubos y podemos prepararnos para aplicar su fórmula de factorización.",
    "proc": [
        "Paso 1: Cuenta los términos. Deben ser dos.",
        "Paso 2: Revisa el signo, debe ser positivo (+).",
        "Paso 3: Verifica si los coeficientes numéricos pertenecen a la lista de cubos perfectos (1, 8, 27, 64, 125, 216...).",
        "Paso 4: Verifica que los exponentes de las letras sean múltiplos de 3 (ej. $x^3, y^6, z^9$)."
    ],
    "ex_a": [
        ("Ejemplo 1", "Determina si $64m^6 + 1$ es una suma de cubos.", ["Tiene dos términos con signo más.", "Raíz cúbica de 64 es 4. Raíz cúbica de $m^6$ es $m^2$.", "Raíz cúbica de 1 es 1.", "Cumple todos los requisitos. Es suma de cubos."])
    ],
    "ex_b": [
        ("¿Es $x^3 + 9$ una suma de cubos en los números enteros?", "No", ["El número 9 no tiene raíz cúbica entera (la raíz cúbica de 9 es ~2.08, su cuadrado perfecto es 9, pero no cubo)."])
    ],
    "errs": [
        "Confundir un cuadrado perfecto (como 9 o 25) con un cubo perfecto.",
        "Creer que un exponente par (como $x^2$) no puede ser parte de un cubo. ¡Sí puede! Si es $x^6$, su raíz cúbica es $x^2$."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Cuál es la característica principal de los exponentes de las variables en un cubo perfecto?", "choices": ["A) Son números pares.", "B) Son múltiplos de 3.", "C) Siempre valen 3.", "D) Son números primos."], "ans": "B) Son múltiplos de 3.", "sol": "Al sacar raíz cúbica, el exponente se divide entre 3. Por ende, debe ser múltiplo de 3 para que sea exacto."},
        {"group": "conceptuales", "diff": "media", "prompt": "De los siguientes números, ¿cuál es simultáneamente un cuadrado perfecto y un cubo perfecto?", "choices": ["A) 16", "B) 27", "C) 64", "D) 125"], "ans": "C) 64", "sol": "64 es 8^2 y también es 4^3."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Cuál de las siguientes expresiones es una suma de cubos?", "choices": ["A) $x^2 + 8$", "B) $x^3 + 16$", "C) $x^3 + 125$", "D) $x^3 - 27$"], "ans": "C) $x^3 + 125$", "sol": "125 es el cubo de 5, y el signo es +. La alternativa D es diferencia de cubos."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Qué término le falta a $8a^9 + \\text{___}$ para ser una suma de cubos perfectos?", "choices": ["A) $16b^3$", "B) $27b^2$", "C) $64b^6$", "D) $9b^3$"], "ans": "C) $64b^6$", "sol": "64 es 4^3, y b^6 tiene exponente múltiplo de 3. 27b^2 falla porque 2 no es múltiplo de 3."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si el binomio es $1 + y^3$, cuenta como suma de cubos aunque el 1 esté primero?", "ans": "Verdadero", "sol": "El orden de los sumandos no altera la suma, y 1 es el cubo de 1."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿La expresión $x^3 + y^3 + z^3$ es una suma de cubos y se puede factorizar con la fórmula estándar de dos términos?", "ans": "Falso", "sol": "La fórmula clásica solo aplica a binomios (dos términos). Para 3 cubos hay fórmulas avanzadas (identidad de Gauss)."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿La raíz cúbica de $x^{12}$ es $x^4$?", "ans": "Verdadero", "sol": "12 dividido en 3 es 4. $(x^4)^3 = x^{12}$."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "En la expresión de un volumen $V(x) = (x+1)^3 + 8$, el profesor te pide identificar sus raíces cúbicas. ¿Cuáles son?", "choices": ["A) $x+1$ y $2$", "B) $(x+1)^3$ y $2$", "C) $x+1$ y $8$", "D) No es una suma de cubos."], "ans": "A) $x+1$ y $2$", "sol": "El primer bloque es un cubo perfecto cuya raíz es el paréntesis (x+1). La raíz de 8 es 2."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Dada la expresión $M = 1000 - (-y^3)$, ¿cómo se clasifica y cuáles son sus bases cúbicas?", "choices": ["A) Diferencia de cubos, bases 10 y $y$.", "B) Suma de cubos, bases 10 y $-y$.", "C) Suma de cubos, bases 10 y $y$.", "D) Diferencia de cuadrados."], "ans": "C) Suma de cubos, bases 10 y $y$.", "sol": "Al simplificar los signos menos por menos da más: 1000 + y^3. Las raíces son 10 y 'y'."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "¿Cuál de estas representaciones algebraicas de la vida real NO es una suma de cubos factorizable?", "choices": ["A) Volumen de un dado más volumen de un cubo mágico: $L^3 + 216$.", "B) Suma de esferas (omitiendo $4/3\\pi$): $R^3 + r^3$.", "C) Área de un cuadrado más volumen de un cubo: $L^2 + L^3$.", "D) Aumento de capital en el tiempo: $8t^3 + 1000$."], "ans": "C) Área de un cuadrado más volumen de un cubo: $L^2 + L^3$.", "sol": "L^2 no es un cubo perfecto, por lo que no es una suma de cubos."}
    ]
})

# 2. FACTORIZACION_SUMA_CUBOS
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUBOS.FACTORIZACION_SUMA_CUBOS",
    "title": "Factorización de la Suma de Cubos",
    "obj": "Aplicar la fórmula $a^3 + b^3 = (a+b)(a^2 - ab + b^2)$ para factorizar polinomios.",
    "intro": "Una vez que identificamos los dos cubos, el proceso de desarmarlos sigue una plantilla estricta. ¡Es como una coreografía matemática! Produce un binomio pequeño y un trinomio más grande.",
    "res": "La suma de cubos se factoriza en dos paréntesis: un binomio con la suma de las raíces cúbicas $(a+b)$, multiplicado por un trinomio que contiene el cuadrado de la primera raíz, menos el producto de ambas raíces, más el cuadrado de la segunda: $(a^2 - ab + b^2)$.",
    "expl": "Fórmula Maestra: $a^3 + b^3 = (a+b)(a^2 - ab + b^2)$.\n\nApliquémoslo a $x^3 + 8$:\n1. Raíces cúbicas: La de $x^3$ es $x$ (nuestra '$a$'). La de $8$ es $2$ (nuestra '$b$').\n2. Primer paréntesis (el binomio): Simplemente cópialas con el signo original. Nos queda $(x + 2)$.\n3. Segundo paréntesis (el trinomio):\n   - El primero al cuadrado: $(x)^2 = x^2$.\n   - MENOS la multiplicación de ambos: $-(x \\cdot 2) = -2x$. (¡Ojo! No es el doble, es solo la multiplicación).\n   - MÁS el segundo al cuadrado: $(2)^2 = 4$.\n\nUnimos las piezas: $(x + 2)(x^2 - 2x + 4)$.\nDato curioso: El trinomio resultante $(x^2 - 2x + 4)$ JAMÁS se puede seguir factorizando en los Reales.",
    "proc": [
        "Paso 1: Extrae la raíz cúbica del 1er término ($a$) y del 2do término ($b$).",
        "Paso 2: Abre un paréntesis pequeño para el binomio: $(a + b)$.",
        "Paso 3: Abre un paréntesis grande para el trinomio.",
        "Paso 4: El primer elemento es el cuadrado de la primera raíz: $a^2$.",
        "Paso 5: El segundo elemento es el negativo del producto de las raíces: $-ab$.",
        "Paso 6: El tercer elemento es el cuadrado de la segunda raíz: $+b^2$."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $27y^3 + 1$.", ["Raíces: $3y$ y $1$.", "Binomio: $(3y + 1)$.", "Trinomio: $(3y)^2 - (3y)(1) + (1)^2 = 9y^2 - 3y + 1$.", "Resultado: $(3y + 1)(9y^2 - 3y + 1)$."])
    ],
    "ex_b": [
        ("Factoriza $8x^3 + 125y^6$.", "$(2x + 5y^2)(4x^2 - 10xy^2 + 25y^4)$", ["Raíces: 2x y 5y^2. Trinomio: cuadrado de 2x es 4x^2, producto invertido es -10xy^2, cuadrado de 5y^2 es 25y^4."])
    ],
    "errs": [
        "En el trinomio, poner el doble del producto (escribir $-2ab$ en vez de $-ab$), confundiéndolo con un TCP.",
        "Olvidar cambiar el signo del término central del trinomio a negativo.",
        "Intentar factorizar el trinomio resultante. (¡Pérdida de tiempo, su discriminante siempre es negativo!)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "En la factorización de la suma de cubos, ¿qué signos lleva el trinomio largo?", "choices": ["A) $+ + +$", "B) $+ - +$", "C) $- - +$", "D) $- - -$"], "ans": "B) $+ - +$", "sol": "El término central del trinomio SIEMPRE lleva el signo opuesto al binomio inicial, que en este caso era positivo."},
        {"group": "conceptuales", "diff": "media", "prompt": "¿Por qué el término central del trinomio largo NO lleva un '2' como coeficiente, a diferencia del TCP?", "choices": ["A) Porque así lo dicta la regla mnemotécnica (SOAP).", "B) Porque si llevara un 2, al multiplicar el binomio por el trinomio no se cancelarían los términos intermedios para dejar solo $a^3 + b^3$.", "C) Porque los cubos no tienen dobles.", "D) Es opcional."], "ans": "B) Porque si llevara un 2, al multiplicar el binomio por el trinomio no se cancelarían los términos intermedios para dejar solo $a^3 + b^3$.", "sol": "Al expandir, el -ab del trinomio es exactamente lo necesario para cancelar las multiplicaciones cruzadas con a^2 y b^2."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Factoriza $m^3 + 64$.", "choices": ["A) $(m+4)(m^2 + 4m + 16)$", "B) $(m-4)(m^2 + 4m + 16)$", "C) $(m+4)(m^2 - 4m + 16)$", "D) $(m+4)(m^2 - 8m + 16)$"], "ans": "C) $(m+4)(m^2 - 4m + 16)$", "sol": "Raíces m y 4. Trinomio lleva el signo cambiado al centro: -4m. Y no lleva el doble."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al factorizar $8p^3 + 27q^3$, ¿cuál es el trinomio que acompaña a $(2p + 3q)$?", "choices": ["A) $4p^2 - 6pq + 9q^2$", "B) $4p^2 + 6pq + 9q^2$", "C) $4p^2 - 12pq + 9q^2$", "D) $2p^2 - 6pq + 3q^2$"], "ans": "A) $4p^2 - 6pq + 9q^2$", "sol": "Cuadrado del primero: (2p)^2 = 4p^2. Producto negativo: -(2p)(3q) = -6pq. Cuadrado segundo: 9q^2."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Se puede seguir factorizando en los reales el trinomio $a^2 - ab + b^2$ obtenido?", "ans": "Falso", "sol": "El discriminante de ese trinomio siempre da negativo (-3b^2). Es una regla universal que es irreducible."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si factorizo $1 + x^6$, el binomio pequeño será $(1+x^2)$?", "ans": "Verdadero", "sol": "La raíz cúbica de 1 es 1, la de $x^6$ es $x^2$. Correcto."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿En $(3x+2y^2)(9x^2 - 6xy^2 + 4y^4)$, el término central del trinomio es incorrecto porque debería ser $-12xy^2$?", "ans": "Falso", "sol": "Está correcto. El producto de las raíces es $3x \\times 2y^2 = 6xy^2$. El doble (-12) sería un error común que el estudiante en la afirmación cree correcto."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Para simplificar el cálculo de una resistencia en paralelo, un físico factoriza $R^3 + 1000$ y divide por $R+10$. ¿Qué expresión queda al final?", "choices": ["A) $R^2 + 10R + 100$", "B) $R^2 - 20R + 100$", "C) $R^2 - 10R + 100$", "D) $R^2 - 10R - 100$"], "ans": "C) $R^2 - 10R + 100$", "sol": "R^3 + 10^3 = (R+10)(R^2 - 10R + 100). Al dividir por R+10, queda el trinomio."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Se tiene la expresión $8x^3 + (x-1)^3$. Al aplicar suma de cubos, el primer factor (el binomio pequeño) simplificado es:", "choices": ["A) $3x - 1$", "B) $2x - 1$", "C) $3x + 1$", "D) $2x^3 + (x-1)$"], "ans": "A) $3x - 1$", "sol": "Las raíces son 2x y (x-1). Su suma es 2x + (x-1) = 3x - 1."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "El volumen de una caja defectuosa difiere del modelo ideal por la expresión $\\frac{x^6 + 64}{x^2 + 4}$. Al simplificarla, ¿cuál es el coeficiente numérico del término central de la expresión resultante?", "choices": ["A) $+4$", "B) $-4$", "C) $-8$", "D) $+8$"], "ans": "B) $-4$", "sol": "x^6 + 64 factoriza como (x^2+4)(x^4 - 4x^2 + 16). El término central del trinomio es -4x^2. Coeficiente: -4."}
    ]
})

# 3. RECONOCIMIENTO_DIFERENCIA_CUBOS
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUBOS.RECONOCIMIENTO_DIFERENCIA_CUBOS",
    "title": "Reconocimiento de la Diferencia de Cubos",
    "obj": "Identificar binomios que corresponden a la resta de dos cubos perfectos.",
    "intro": "¡No discrimines a la resta! Así como vimos la Suma de Cubos, su hermana, la Diferencia de Cubos, es igual de predecible y elegante. De hecho, los requisitos para encontrarla son exactamente los mismos, solo cambia el signo central.",
    "res": "Una diferencia de cubos se presenta como $A^3 - B^3$. Son dos términos con signo negativo entre ellos, donde a ambos se les puede extraer raíz cúbica exacta.",
    "expl": "Para reconocerla, pasamos el control de calidad:\n1. Son dos términos.\n2. Están separados por un signo menos (resta).\n3. Tienen raíz cúbica exacta.\n\nEjemplo: $125 - 64y^9$.\n- ¿Dos términos separados por resta? Sí.\n- La raíz cúbica de 125 es 5.\n- La raíz cúbica de $64y^9$ se halla sacando raíz a 64 (que es 4) y dividiendo el exponente 9 entre 3 (que da 3). Queda $4y^3$.\n\nAl tener ambas raíces exactas ($5$ y $4y^3$), confirmamos que estamos ante una Diferencia de Cubos lista para ser factorizada.\n\nRecuerda los cubos clave: $1, 8, 27, 64, 125, 216, 343, 512, 729, 1000$.",
    "proc": [
        "Paso 1: Observa que la expresión tiene 2 términos restándose.",
        "Paso 2: Comprueba que el coeficiente numérico del primer y segundo término sean cubos perfectos.",
        "Paso 3: Comprueba que los exponentes de todas las letras involucradas sean divisibles por 3."
    ],
    "ex_a": [
        ("Ejemplo 1", "Determina si $x^3 y^6 - 27$ es diferencia de cubos.", ["Dos términos, signo resta.", "Raíz del primero: $\\sqrt[3]{x^3 y^6} = x y^2$.", "Raíz del segundo: $\\sqrt[3]{27} = 3$.", "Ambas raíces existen. Es Diferencia de Cubos."])
    ],
    "ex_b": [
        ("¿Es $16x^3 - 8$ diferencia de cubos?", "No", ["El número 8 es cubo de 2, pero el 16 no tiene raíz cúbica entera (no hay entero que multiplicado tres veces dé 16)."])
    ],
    "errs": [
        "Confundirla con la Diferencia de Cuadrados (ej. $x^6 - 64$ es AMBAS cosas, pero generalmente es mejor sacarla como Diferencia de Cuadrados primero por facilidad).",
        "Asumir que 9 es un cubo perfecto (¡es el cuadrado de 3, no su cubo!)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué signo debe separar a los dos términos para que sea una Diferencia de Cubos?", "choices": ["A) Positivo (+)", "B) Negativo (-)", "C) Multiplicación", "D) División"], "ans": "B) Negativo (-)", "sol": "Diferencia es sinónimo de resta en matemáticas."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si tienes $x^6 - 64$, que es tanto diferencia de cuadrados como diferencia de cubos, ¿qué método suele recomendarse aplicar primero para una factorización más completa y sencilla?", "choices": ["A) Diferencia de Cubos.", "B) Diferencia de Cuadrados.", "C) Trinomio Cuadrado Perfecto.", "D) Da exactamente lo mismo paso a paso."], "ans": "B) Diferencia de Cuadrados.", "sol": "Sacar la diferencia de cuadrados primero produce (x^3-8)(x^3+8), lo cual desglosa en suma y diferencia de cubos y es menos propenso a errores que el trinomio de grado 4 que produce sacarlo por cubos primero."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Cuál de las siguientes es una diferencia de cubos perfectos?", "choices": ["A) $27x^3 + 8$", "B) $8x^3 - 9$", "C) $x^3 - 125$", "D) $x^2 - 27$"], "ans": "C) $x^3 - 125$", "sol": "125 es 5^3 y hay una resta."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Las raíces cúbicas de $343m^{12} - n^3$ son:", "choices": ["A) $7m^4$ y $n$", "B) $49m^4$ y $n$", "C) $7m^3$ y $n$", "D) $343m^4$ y $n$"], "ans": "A) $7m^4$ y $n$", "sol": "La raíz cúbica de 343 es 7 (7*7*7 = 343). El exponente 12 dividido 3 es 4."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El número 1 se considera un cubo perfecto válido para la diferencia de cubos, como en $y^3 - 1$?", "ans": "Verdadero", "sol": "El 1 es mágico: es cuadrado, cubo, cuarta potencia... $1^3 = 1$."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si el polinomio es $-x^3 + 8$, no se puede considerar una diferencia de cubos?", "ans": "Falso", "sol": "Puedes reordenarlo a $8 - x^3$ y ahí tienes tu diferencia de cubos clara y cristalina."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿La expresión $2x^3 - 54$ es una diferencia de cubos?", "ans": "Verdadero", "sol": "Escondida, sí. Primero sacas factor común 2: $2(x^3 - 27)$. Y el interior es una diferencia de cubos."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "En un análisis de fluidos, la diferencia de presiones genera la ecuación $P^3 - 216 = 0$. ¿Cuáles son las raíces cúbicas de los términos?", "choices": ["A) $P$ y $16$", "B) $P$ y $6$", "C) $P$ y $36$", "D) $P$ y $-6$"], "ans": "B) $P$ y $6$", "sol": "La raíz cúbica de 216 es 6."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Si el volumen sobrante en una fundición es $V = (2x-1)^3 - 8y^3$, ¿cuáles son los términos o bases $A$ y $B$ para aplicar la fórmula de diferencia de cubos?", "choices": ["A) $A = 2x-1$, $B = 8y$", "B) $A = (2x-1)^2$, $B = 2y$", "C) $A = 2x-1$, $B = 2y$", "D) No es una diferencia de cubos."], "ans": "C) $A = 2x-1$, $B = 2y$", "sol": "El primer bloque entero es un cubo cuya raíz es (2x-1). El segundo tiene raíz 2y."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Una estudiante duda si $0.001 - m^3$ es diferencia de cubos. ¿Qué le dirías?", "choices": ["A) No, los decimales nunca son cubos.", "B) Sí, 0.001 es el cubo de 0.1, así que es diferencia de cubos.", "C) Sí, pero 0.001 es el cuadrado de 0.01.", "D) No, porque empieza con número y no con letra."], "ans": "B) Sí, 0.001 es el cubo de 0.1, así que es diferencia de cubos.", "sol": "(0.1) * (0.1) * (0.1) = 0.001."}
    ]
})

# 4. FACTORIZACION_DIFERENCIA_CUBOS
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUBOS.FACTORIZACION_DIFERENCIA_CUBOS",
    "title": "Factorización de Diferencia de Cubos",
    "obj": "Aplicar la fórmula $a^3 - b^3 = (a-b)(a^2 + ab + b^2)$ de manera sistemática.",
    "intro": "¡Hora de desarmar la resta! La fórmula para factorizar la Diferencia de Cubos es casi un espejo de la suma, pero los signos se cambian de asiento. Si aprendes la mnemotecnia correcta (SOAP), jamás los confundirás.",
    "res": "La diferencia de cubos se factoriza como: $(a-b)(a^2 + ab + b^2)$. El binomio mantiene el signo de resta, y el trinomio tiene todos sus signos positivos.",
    "expl": "Fórmula: $A^3 - B^3 = (A - B)(A^2 + A \\cdot B + B^2)$.\n\n¿Cómo recordar los signos? Usa el acrónimo en inglés **SOAP** (Same, Opposite, Always Positive):\n- **S**ame (Mismo signo): El binomio inicial lleva el MISMO signo que el problema ($-$).\n- **O**pposite (Signo opuesto): El primer signo del trinomio lleva el OPUESTO ($+$).\n- **AP** (Siempre Positivo): El último signo del trinomio es SIEMPRE POSITIVO ($+$).\n\nFactoricemos $27x^3 - 64$:\n1. Raíces: $A = 3x$, $B = 4$.\n2. Binomio (Same): $(3x - 4)$.\n3. Trinomio (Opposite, AP): \n   - Cuadrado de A: $(3x)^2 = 9x^2$\n   - Producto (Opposite sign): $+(3x)(4) = +12x$\n   - Cuadrado de B (Always Positive): $+(4)^2 = +16$\n\nResultado: $(3x - 4)(9x^2 + 12x + 16)$.",
    "proc": [
        "Paso 1: Extrae la raíz cúbica de ambos términos ($a$ y $b$).",
        "Paso 2: Escribe el binomio con la resta: $(a - b)$.",
        "Paso 3: Escribe el trinomio abriendo paréntesis.",
        "Paso 4: Eleva la primera raíz al cuadrado: $a^2$.",
        "Paso 5: Multiplica ambas raíces y ponle signo positivo: $+ab$.",
        "Paso 6: Eleva la segunda raíz al cuadrado y ponle signo positivo: $+b^2$."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $y^3 - 1000$.", ["Raíces: $y$ y $10$.", "Binomio: $(y - 10)$.", "Trinomio: $y^2 + 10y + 100$.", "Respuesta final: $(y - 10)(y^2 + 10y + 100)$."])
    ],
    "ex_b": [
        ("Factoriza $8m^6 - 1$.", "$(2m^2 - 1)(4m^4 + 2m^2 + 1)$", ["Raíces: 2m^2 y 1. Binomio (2m^2-1). Trinomio: (2m^2)^2 = 4m^4. Producto = +2m^2. (1)^2 = +1."])
    ],
    "errs": [
        "Poner un signo negativo en el término central del trinomio.",
        "Elevar incorrectamente la primera raíz al cuadrado si tiene coeficientes numéricos (Ej: raíz $3x$, poner $3x^2$ en vez de $9x^2$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Según la regla SOAP, ¿qué signo lleva el término del medio en el trinomio largo de la Diferencia de Cubos?", "choices": ["A) Negativo.", "B) Positivo.", "C) El mismo del problema original.", "D) Depende de las variables."], "ans": "B) Positivo.", "sol": "Opposite (Opuesto). Como el problema es una resta (-), el opuesto es positivo (+)."},
        {"group": "conceptuales", "diff": "media", "prompt": "¿El trinomio largo resultante en una diferencia de cubos es un Trinomio Cuadrado Perfecto?", "choices": ["A) Sí, siempre.", "B) No, le falta el '2' en el término central.", "C) Sí, pero con signos cambiados.", "D) Depende de los números."], "ans": "B) No, le falta el '2' en el término central.", "sol": "El TCP tiene la forma a^2 + 2ab + b^2. Este trinomio es a^2 + ab + b^2, por lo que es irreducible en los Reales."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Factoriza $w^3 - 8$.", "choices": ["A) $(w-2)(w^2 - 2w + 4)$", "B) $(w+2)(w^2 - 2w + 4)$", "C) $(w-2)(w^2 + 2w + 4)$", "D) $(w-2)(w^2 + 4w + 4)$"], "ans": "C) $(w-2)(w^2 + 2w + 4)$", "sol": "Binomio con el mismo signo (-). Trinomio con signos (+, +) y el producto es 2w, no 4w."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Qué resulta al factorizar $64x^3 - 27y^3$?", "choices": ["A) $(4x - 3y)(16x^2 + 12xy + 9y^2)$", "B) $(4x - 3y)(16x^2 - 12xy + 9y^2)$", "C) $(8x - 3y)(64x^2 + 24xy + 9y^2)$", "D) $(4x + 3y)(16x^2 - 12xy + 9y^2)$"], "ans": "A) $(4x - 3y)(16x^2 + 12xy + 9y^2)$", "sol": "Raíces 4x y 3y. Trinomio es suma: (4x)^2 + (4x)(3y) + (3y)^2."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Es correcto afirmar que el último término del trinomio largo SIEMPRE es positivo, sin importar si es suma o diferencia de cubos?", "ans": "Verdadero", "sol": "La 'AP' de SOAP (Always Positive) aplica a ambas fórmulas: el $b^2$ siempre va con más."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si factorizo $x^3 - 64$, el binomio obtenido es $(x-8)$?", "ans": "Falso", "sol": "La raíz cúbica de 64 es 4, no 8. El 8 es su raíz cuadrada. El binomio correcto es $(x-4)$."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿Si tengo una expresión como $x^3 - (y+1)^3$, puedo aplicar esta fórmula tratando a $(y+1)$ como mi '$b$'?", "ans": "Verdadero", "sol": "Sí. Quedaría: $[x - (y+1)] [x^2 + x(y+1) + (y+1)^2]$. El método es universal."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Una viga soporta un estrés de $1000m^3 - n^6$. Para encontrar sus puntos críticos se debe factorizar. ¿Cuál es la expresión factorizada?", "choices": ["A) $(10m - n^2)(100m^2 + 10mn^2 + n^4)$", "B) $(10m - n^2)(100m^2 - 10mn^2 + n^4)$", "C) $(100m - n^3)(10m^2 + 10mn^2 + n^4)$", "D) $(10m - n^3)(100m^2 + 10mn^3 + n^6)$"], "ans": "A) $(10m - n^2)(100m^2 + 10mn^2 + n^4)$", "sol": "Raíces 10m y n^2. Trinomio: (10m)^2 = 100m^2. Producto: 10mn^2. (n^2)^2 = n^4. Todos positivos en trinomio."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Al simplificar la fracción $\\frac{a^3 - 125}{a^2 + 5a + 25}$, ¿qué resultado arroja?", "choices": ["A) $a + 5$", "B) $a - 5$", "C) $a^2 - 25$", "D) $\\frac{1}{a-5}$"], "ans": "B) $a - 5$", "sol": "El numerador es (a-5)(a^2+5a+25). El trinomio gigante se cancela entero con el denominador. Sobrevive a-5."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un alumno factoriza $1 - 216x^3$. Su respuesta es $(1 - 6x)(1 + 6x + 36x^2)$. ¿El profesor la marcará como correcta?", "choices": ["A) Sí, está perfectamente factorizada.", "B) No, el 1 en el trinomio debería ser $-1$.", "C) No, el producto cruzado debería ser $12x$.", "D) No, $216$ no es el cubo de $6$."], "ans": "A) Sí, está perfectamente factorizada.", "sol": "Raíz de 1 es 1, de 216x^3 es 6x. Cuadrado de 1 es 1. Producto es 6x. Cuadrado de 6x es 36x^2. Perfecto."}
    ]
})

# 5. SUMA_POTENCIAS_IMPARES
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUBOS.SUMA_POTENCIAS_IMPARES",
    "title": "Suma de Potencias Impares Iguales",
    "obj": "Conocer la generalización de la suma de cubos para cualquier potencia impar (quinta, séptima, etc.).",
    "intro": "¡Los cubos no son los únicos privilegiados! La regla que permite factorizar $x^3 + y^3$ es solo la punta del iceberg de una ley matemática más grande. Toda suma de potencias impares iguales puede descomponerse siguiendo un elegante patrón rítmico.",
    "res": "La expresión $a^n + b^n$ (donde $n$ es impar: 5, 7, 9...) siempre es divisible por $(a+b)$. El polinomio resultante tendrá signos alternados $(+ - + - ...)$ y los exponentes de '$a$' irán bajando mientras los de '$b$' van subiendo.",
    "expl": "Pensemos en $x^5 + y^5$ (Suma de quintas potencias).\nComo 5 es impar, SABEMOS que uno de los factores será $(x + y)$.\n\n¿Cómo construimos el paréntesis grande?\n1. Empezamos con la primera letra elevada a un grado menos: $x^4$.\n2. Los signos deben ALTERNARSE: si empezamos positivo, el siguiente es negativo.\n3. En cada término que avanza, la 'x' baja un grado y la 'y' sube un grado (apareciendo desde la nada como $y^1$).\n\nVeamos la danza:\n$+x^4$ \n$-x^3 y^1$\n$+x^2 y^2$\n$-x^1 y^3$\n$+y^4$\n\n¡Unimos todo! $x^5 + y^5 = (x + y)(x^4 - x^3 y + x^2 y^2 - x y^3 + y^4)$.\nEste patrón de exponentes en escalera (uno baja, el otro sube) aplica para el grado 7, 9, 11... ¡para el infinito impar!",
    "proc": [
        "Paso 1: Confirma que sea una suma y que ambas potencias sean iguales e IMPARES.",
        "Paso 2: Escribe el factor corto (binomio) como la suma de las bases: $(a + b)$.",
        "Paso 3: Para el polinomio largo, empieza con la primera base elevada a $n-1$.",
        "Paso 4: Alterna los signos: $+ - + - +$ terminando siempre en positivo.",
        "Paso 5: En cada término subsiguiente, réstale 1 al exponente de $a$, y súmale 1 al exponente de $b$ hasta llegar a $b^{n-1}$."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $m^7 + 1$.", ["Factor corto: $(m + 1)$.", "Grado menos 1 es $m^6$.", "Polinomio: $m^6 - m^5(1) + m^4(1)^2 - m^3(1)^3 + m^2(1)^4 - m(1)^5 + (1)^6$.", "Resultado: $(m + 1)(m^6 - m^5 + m^4 - m^3 + m^2 - m + 1)$."])
    ],
    "ex_b": [
        ("¿Cuál es el binomio corto al factorizar $x^5 + 32$?", "$(x + 2)$", ["Como 32 es $2^5$, la expresión es $x^5 + 2^5$. Las bases son $x$ y $2$, por ende el binomio es $(x+2)$."])
    ],
    "errs": [
        "Intentar aplicar esta regla a sumas de potencias PARES (ej. $x^4 + y^4$), lo cual es matemáticamente imposible en los reales.",
        "Olvidar alternar los signos y ponerlos todos positivos."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué patrón de signos debe tener el polinomio largo al factorizar una suma de potencias impares?", "choices": ["A) Todos positivos.", "B) Todos negativos.", "C) Alternados, comenzando con positivo (+ - + -).", "D) Alternados, comenzando con negativo (- + - +)."], "ans": "C) Alternados, comenzando con positivo (+ - + -).", "sol": "La alternancia asegura que todos los términos cruzados se cancelen mutuamente en la multiplicación."},
        {"group": "conceptuales", "diff": "media", "prompt": "¿Por qué no se puede factorizar $x^4 + y^4$ usando esta regla general?", "choices": ["A) Porque 4 no es un número suficientemente grande.", "B) Porque la regla solo aplica estrictamente a potencias impares.", "C) Porque los exponentes pares requieren que el factor pequeño sea $(x-y)$.", "D) Porque daría demasiados términos."], "ans": "B) Porque la regla solo aplica estrictamente a potencias impares.", "sol": "La suma de potencias pares es irreducible con métodos elementales sin números complejos (a menos que pueda formarse como suma de cubos si el exponente es múltiplo de 3)."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al desarrollar $a^5 + b^5$, ¿cuál es el término central del polinomio largo?", "choices": ["A) No tiene término central, son 5 términos, por lo que el central es el tercero: $+a^2b^2$", "B) $-a^3b^2$", "C) $-a^2b^3$", "D) $+a^3b^3$"], "ans": "A) No tiene término central, son 5 términos, por lo que el central es el tercero: $+a^2b^2$", "sol": "Los términos son: a^4, -a^3b, +a^2b^2, -ab^3, +b^4. El tercero es +a^2b^2."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Factoriza $x^5 + 243$.", "choices": ["A) $(x-3)(x^4 + 3x^3 + 9x^2 + 27x + 81)$", "B) $(x+3)(x^4 - 3x^3 + 9x^2 - 27x + 81)$", "C) $(x+3)(x^4 - 3x^3 - 9x^2 - 27x - 81)$", "D) $(x+3)(x^5 - 3x^4 + 9x^3 - 27x^2 + 81x)$"], "ans": "B) $(x+3)(x^4 - 3x^3 + 9x^2 - 27x + 81)$", "sol": "243 es 3^5. El binomio es (x+3). El polinomio arranca con x^4, y los exponentes de x bajan mientras multiplicamos por las potencias crecientes de 3, alternando signos."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El factor binomio (el pequeño) SIEMPRE conserva el mismo signo de la expresión original (suma = signo +)?", "ans": "Verdadero", "sol": "Esa regla nunca cambia. $a^n + b^n$ siempre es divisible por $(a+b)$."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿El número de términos en el polinomio largo es igual al exponente $n$ de la potencia original?", "ans": "Verdadero", "sol": "Sí. Para $x^3$ son 3 términos (trinomio). Para $x^5$ son 5 términos. Para $x^7$ son 7 términos."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿La suma de coeficientes del polinomio largo en $x^n + 1$ es igual a 1 (si evaluamos en x=1)?", "ans": "Verdadero", "sol": "Al evaluar x=1 en la expresión de signos alternados de longitud n impar (ej: 1 - 1 + 1 - 1 + 1), todos los pares se cancelan y siempre sobra un +1. Matemáticamente fascinante."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Un algoritmo de cifrado se basa en la simplificación de $\\frac{y^7 + 128}{y+2}$. ¿Cuál será el primer y el último término del polinomio resultante?", "choices": ["A) Primer: $y^6$. Último: $+64$.", "B) Primer: $y^7$. Último: $-128$.", "C) Primer: $y^6$. Último: $-64$.", "D) Primer: $y^6$. Último: $+128$."], "ans": "A) Primer: $y^6$. Último: $+64$.", "sol": "128 es 2^7. El polinomio arranca en y^6. El último término será +(2^6) = +64. Recuerda que los signos terminan siempre en positivo."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Una estudiante debe demostrar que $3^5 + 2^5$ es múltiplo de 5. ¿Cómo le ayuda esta factorización a demostrarlo sin calcular la suma grande?", "choices": ["A) Porque el binomio factor es $(3-2) = 1$.", "B) Porque el binomio factor es $(3+2) = 5$, lo que indica que toda la expresión es 5 multiplicado por un número entero.", "C) Porque los exponentes son 5.", "D) No sirve para números puros."], "ans": "B) Porque el binomio factor es $(3+2) = 5$, lo que indica que toda la expresión es 5 multiplicado por un número entero.", "sol": "Al igual que con el álgebra, a^n + b^n es divisible por a+b. 3+2 = 5, por tanto es múltiplo de 5 directo sin calcular 243+32=275."}
    ]
})

# 6. DIFERENCIA_POTENCIAS_IMPARES
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUBOS.DIFERENCIA_POTENCIAS_IMPARES",
    "title": "Diferencia de Potencias Impares Iguales",
    "obj": "Conocer la generalización para factorizar restas de potencias impares iguales.",
    "intro": "Para cerrar el círculo cósmico de los exponentes, abordaremos la Diferencia de Potencias Impares. A diferencia de las sumas (que alternan signos), las diferencias nos regalan el polinomio largo más amigable y relajado de todos: ¡todo es positivo!",
    "res": "La expresión $a^n - b^n$ (con $n$ impar) siempre es divisible por $(a-b)$. El polinomio resultante tendrá TODOS sus signos positivos $(+ + + ...)$ manteniendo el mismo patrón de escalera de exponentes.",
    "expl": "Pensemos en $x^5 - y^5$.\nSabemos que el factor corto mantendrá el signo negativo: $(x - y)$.\n\nEl factor largo seguirá la regla de la escalera que ya conoces:\n- La 'x' empieza en $x^4$ y va bajando.\n- La 'y' va subiendo.\n\nLa gran ventaja es que NO hay que alternar signos. Como el binomio ya lleva el signo negativo, el polinomio largo compensa siendo pura positividad.\n\n$x^5 - y^5 = (x - y)(x^4 + x^3 y + x^2 y^2 + x y^3 + y^4)$.\n\nEste patrón (binomio negativo, todo el resto positivo) es la generalización de la regla de Diferencia de Cubos que vimos antes (donde el trinomio tenía signos $+ + +$).",
    "proc": [
        "Paso 1: Confirma que sea una diferencia (resta) de potencias iguales impares.",
        "Paso 2: Escribe el factor corto como $(a - b)$.",
        "Paso 3: Escribe el polinomio largo empezando con $a^{n-1}$.",
        "Paso 4: Usa SÓLO signos positivos (+).",
        "Paso 5: Sigue bajando el exponente de '$a$' y subiendo el de '$b$' en cada término."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $p^7 - q^7$.", ["Factor corto: $(p - q)$.", "El largo empieza en $p^6$ y son 7 términos, todos positivos.", "Respuesta: $(p - q)(p^6 + p^5 q + p^4 q^2 + p^3 q^3 + p^2 q^4 + p q^5 + q^6)$."])
    ],
    "ex_b": [
        ("Factoriza $x^5 - 1$.", "$(x - 1)(x^4 + x^3 + x^2 + x + 1)$", ["El 1 a cualquier potencia es 1. El binomio es (x-1). El factor largo es la escalera decreciente de x hasta 1, todo con signo positivo."])
    ],
    "errs": [
        "Alternar los signos en el polinomio largo (confundiéndolo con la regla de la suma de potencias).",
        "Poner un signo $+$ en el factor corto (binomio)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "En la factorización de la diferencia de potencias impares ($a^n - b^n$), ¿qué signos lleva el polinomio largo?", "choices": ["A) Alternados.", "B) Todos negativos.", "C) Todos positivos.", "D) Solo el primero y el último son positivos."], "ans": "C) Todos positivos.", "sol": "A diferencia de la suma, la diferencia genera un polinomio complementario 100% positivo."},
        {"group": "conceptuales", "diff": "media", "prompt": "¿El binomio factor corto siempre es $(a-b)$ cuando factorizas una diferencia de potencias?", "choices": ["A) Sí, esa es la regla universal.", "B) No, a veces es $(a+b)$.", "C) Depende si el exponente es mayor a 5.", "D) Sí, pero el polinomio largo no existe."], "ans": "A) Sí, esa es la regla universal.", "sol": "Todo polinomio de la forma a^n - b^n es divisible por (a-b) sin importar si n es par o impar."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Cuál es la factorización correcta de $m^5 - 32$?", "choices": ["A) $(m-2)(m^4 + 2m^3 + 4m^2 + 8m + 16)$", "B) $(m-2)(m^4 - 2m^3 + 4m^2 - 8m + 16)$", "C) $(m+2)(m^4 + 2m^3 + 4m^2 + 8m + 16)$", "D) $(m-2)(m^5 + 2m^4 + 4m^3 + 8m^2 + 16m)$"], "ans": "A) $(m-2)(m^4 + 2m^3 + 4m^2 + 8m + 16)$", "sol": "32 es 2^5. Binomio es (m-2). El largo arranca en m^4 y es todo positivo: m^4, m^3(2), m^2(4), m(8), 16."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al desarrollar el polinomio largo para $x^7 - y^7$, ¿cuál de los siguientes términos está INCORRECTO si lo encuentras en el desarrollo de un alumno?", "choices": ["A) $+x^5 y$", "B) $+x^3 y^3$", "C) $-x^2 y^4$", "D) $+x y^5$"], "ans": "C) $-x^2 y^4$", "sol": "Todos los términos deben tener signo positivo (+). El signo negativo delata el error."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿La suma de los exponentes de las letras en CADA término del polinomio largo siempre es igual a $n-1$?", "ans": "Verdadero", "sol": "Por ejemplo, en $x^5 - y^5$, el grado es 5. Los términos como $x^3 y^1$ suman 3+1 = 4 ($n-1$). ¡Siempre ocurre!"},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Esta regla de \"todos positivos\" aplica también a diferencias de potencias PARES como $x^6 - y^6$ (vista como diferencia de sextas potencias)?", "ans": "Verdadero", "sol": "Absolutamente. Toda diferencia $a^n - b^n$ al dividirse por $(a-b)$ genera un cociente de términos exclusivamente positivos, sea 'n' par o impar."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿Si calculas $10^5 - 1$ con esta regla, el polinomio largo evalúa a $11111$?", "ans": "Verdadero", "sol": "El polinomio es $10^4 + 10^3 + 10^2 + 10^1 + 1 = 10000 + 1000 + 100 + 10 + 1 = 11111$. (Y el binomio es 9, por lo que $100000-1 = 99999 = 9 \\times 11111$). ¡Correcto y fascinante!"},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Para calcular límites en series geométricas, se usa frecuentemente $1 - r^5$. Su forma factorizada es $(1-r)(1+r+r^2+r^3+r^4)$. ¿Esto es matemáticamente válido según nuestras reglas?", "choices": ["A) No, el 1 no puede usarse como base variable.", "B) Sí, es una simple diferencia de quintas potencias aplicadas en orden inverso.", "C) No, los signos deberían alternarse.", "D) Sí, pero falta un $r^5$."], "ans": "B) Sí, es una simple diferencia de quintas potencias aplicadas en orden inverso.", "sol": "1^5 - r^5 cumple a la perfección el modelo. (1-r) multiplicado por todas las potencias de 'r' decreciendo el 1 y aumentando la 'r'."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Simplifica la fracción $\\frac{t^5 - 243}{t - 3}$ y encuentra la evaluación final si $t = 3$.", "choices": ["A) La expresión queda $t^4 + 3t^3 + 9t^2 + 27t + 81$. Al evaluar en $t=3$, da $405$.", "B) La expresión queda $t^4$. Evalúa en 81.", "C) La expresión no se puede simplificar.", "D) Da 0."], "ans": "A) La expresión queda $t^4 + 3t^3 + 9t^2 + 27t + 81$. Al evaluar en $t=3$, da $405$.", "sol": "La división elimina el (t-3). Queda el polinomio de 5 términos. Evaluado en 3: 81+81+81+81+81 = 405."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-5.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

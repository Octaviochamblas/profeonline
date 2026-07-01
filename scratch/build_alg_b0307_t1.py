import os
import json

def to_yaml_list(items, indent=4):
    spaces = " " * indent
    if not items:
        return ""
    return "\n" + spaces + "- '" + f"'\n{spaces}- '".join(i.replace("'", "''") for i in items) + "'"

def format_multiline(text):
    return "\n  " + "\n  ".join(text.strip().split("\n"))

def build_node(sid, title, obj, intro, res, expl, proc, ex_a, ex_b, errs):
    filename = f"docs/conocimiento/contenido/{sid.lower().replace('.', '-').replace('_', '-')}.yaml"
    proc_yaml = to_yaml_list(proc, indent=2)
    errs_yaml = to_yaml_list(errs, indent=2)

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
    solucion_pasos:{to_yaml_list(sp, indent=4)}"""

    for t, r, sp in ex_b:
        yaml_content += f"""
  - titulo: '{t.replace("'", "''")}'
    respuesta: '{r}'
    solucion_pasos:{to_yaml_list(sp, indent=4)}"""

    yaml_content += f"""
errores_frecuentes:{errs_yaml}
estado: publicado
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    print(f"Generado {filename}")

def append_exercises(sid, prefix, ex_list):
    filename = "docs/conocimiento/ejercicios/mat-alg-fracciones-banco-gen-1.jsonl"
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

# 1. CONCEPTO_MCD
nodes.append({
    "sid": "MAT.ALG.MCD_ALGEBRAICO.CONCEPTO_MCD",
    "title": "Concepto de MCD Algebraico",
    "obj": "Comprender la definición del Máximo Común Divisor (MCD) aplicado a expresiones algebraicas.",
    "intro": "Así como en la aritmética el Máximo Común Divisor (MCD) es el número más grande que divide exactamente a varios números, en álgebra el MCD es la expresión algebraica 'más grande' (de mayor grado y coeficiente) que divide exactamente a dos o más polinomios o monomios.",
    "res": "El Máximo Común Divisor (MCD) de dos o más expresiones algebraicas es la expresión de mayor grado posible que es factor de todas ellas simultáneamente.",
    "expl": "El concepto de MCD algebraico es una extensión directa del MCD numérico.\nPor ejemplo, el MCD numérico entre 12 y 18 es 6, porque 6 es el número más grande que divide a ambos sin dejar resto.\n\nEn álgebra, buscamos lo mismo pero con letras y exponentes.\nSi tenemos $x^3$ y $x^2$, buscamos la mayor potencia de 'x' que divida a ambos.\n- $x$ divide a ambos.\n- $x^2$ divide a $x^2$ (da 1) y a $x^3$ (da $x$).\n- $x^3$ divide a $x^3$, pero no divide exactamente a $x^2$ (daría $x^{-1}$, que no es polinomio).\n\nPor tanto, el MCD entre $x^3$ y $x^2$ es $x^2$. La regla conceptual es que el MCD está formado por los factores comunes elevados a su **menor exponente**. Es el bloque de construcción compartido más grande que tienen las expresiones.",
    "proc": [
        "Paso 1: Entiende que el MCD debe ser un divisor EXACTO de todas las expresiones dadas.",
        "Paso 2: Recuerda que 'máximo' en álgebra significa incluir todos los factores comunes posibles con el mayor exponente que no supere a ninguno (es decir, el menor exponente presente).",
        "Paso 3: El MCD de expresiones sin factores comunes (excepto el 1) es simplemente 1."
    ],
    "ex_a": [
        ("Ejemplo 1", "Conceptualmente, ¿cuál es el MCD de $(x-1)^2$ y $(x-1)(x+2)$?", ["Ambas expresiones comparten el bloque factor $(x-1)$.", "En la primera está elevado a 2, en la segunda a 1.", "El MCD es el factor común al menor exponente: $(x-1)$."])
    ],
    "ex_b": [
        ("¿Cuál es el MCD conceptual de $x$ e $y$?", "1", ["Como $x$ e $y$ son variables distintas y no comparten factores, el único divisor que tienen en común es el número 1."])
    ],
    "errs": [
        "Confundir MCD con MCM (elegir el mayor exponente en lugar del menor).",
        "Creer que si no hay factores comunes, el MCD es 0. (¡El MCD es siempre al menos 1!)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "En álgebra, ¿qué representa el MCD de dos polinomios?", "choices": ["A) El polinomio de menor grado que es múltiplo de ambos.", "B) El polinomio de mayor grado que divide exactamente a ambos.", "C) La suma de los polinomios.", "D) El producto de los polinomios."], "ans": "B) El polinomio de mayor grado que divide exactamente a ambos.", "sol": "MCD significa Máximo Común Divisor, el mayor factor compartido."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Si dos polinomios son primos entre sí, ¿cuál es su MCD?", "choices": ["A) 0", "B) 1", "C) La variable $x$", "D) El producto de ambos"], "ans": "B) 1", "sol": "Polinomios primos entre sí (o coprimos) no comparten factores, por lo que su único divisor común es 1."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El MCD de varias expresiones contiene SOLO los factores que están presentes en TODAS las expresiones?", "ans": "Verdadero", "sol": "Exacto. Si un factor falta en al menos una expresión, no es \"común\" y no entra en el MCD."}
    ]
})

# 2. COEFICIENTE_MONOMIOS (MCD)
nodes.append({
    "sid": "MAT.ALG.MCD_ALGEBRAICO.COEFICIENTE_MONOMIOS",
    "title": "MCD de los Coeficientes Numéricos",
    "obj": "Calcular el Máximo Común Divisor de los coeficientes numéricos en un conjunto de monomios.",
    "intro": "Antes de lidiar con las letras, debemos limpiar el terreno de los números. Todo monomio tiene un coeficiente (el número que va adelante). Extraer el MCD algebraico siempre empieza por encontrar el MCD tradicional de estos coeficientes.",
    "res": "El coeficiente numérico del MCD algebraico es simplemente el MCD aritmético de los coeficientes de las expresiones dadas (tomando sus valores absolutos).",
    "expl": "Si tenemos los monomios $12x^2 y$ y $18x y^3$.\nIgnoramos las letras por un momento y nos enfocamos en los números: 12 y 18.\n\n¿Cuál es el mayor número que divide exactamente a 12 y a 18?\n- Divisores de 12: 1, 2, 3, 4, 6, 12.\n- Divisores de 18: 1, 2, 3, 6, 9, 18.\n\nEl mayor número que aparece en ambas listas es el **6**.\nPor lo tanto, la parte numérica del MCD de nuestros monomios será 6.\n\nNota: Si los coeficientes son negativos (ej. $-15$ y $25$), el MCD algebraico siempre se toma como un valor positivo (en este caso 5), a menos que todas las expresiones sean negativas y por convención se decida extraer el signo negativo.",
    "proc": [
        "Paso 1: Identifica los coeficientes numéricos de todos los monomios (sus valores absolutos).",
        "Paso 2: Descompón cada número en factores primos, o lista mentalmente sus divisores.",
        "Paso 3: Identifica el mayor divisor que tengan en común (MCD aritmético).",
        "Paso 4: Este número será el coeficiente del MCD algebraico final."
    ],
    "ex_a": [
        ("Ejemplo 1", "Halla el coeficiente del MCD de $24a^2b$ y $36a^3$.", ["Coeficientes: 24 y 36.", "Descomposición: $24 = 2^3 \\times 3$. $36 = 2^2 \\times 3^2$.", "MCD aritmético: tomamos factores comunes al menor exponente: $2^2 \\times 3 = 4 \\times 3 = 12$.", "El coeficiente del MCD es 12."])
    ],
    "ex_b": [
        ("¿Cuál es la parte numérica del MCD entre $7x$ y $15y$?", "1", ["Los números 7 y 15 no tienen divisores comunes además del 1 (son coprimos). Por tanto, es 1."])
    ],
    "errs": [
        "Calcular el MCM de los números en lugar del MCD (ej. para 4 y 6, responder 12 en vez de 2).",
        "Creer que si uno de los números es primo, el MCD es ese número. (Ej. para 5 y 10 sí es 5, pero para 5 y 12 es 1)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Cómo se determina el coeficiente del MCD de varios monomios?", "choices": ["A) Multiplicando todos los coeficientes.", "B) Buscando el MCM aritmético.", "C) Buscando el MCD aritmético de sus valores absolutos.", "D) Sumando los coeficientes."], "ans": "C) Buscando el MCD aritmético de sus valores absolutos.", "sol": "El MCD algebraico utiliza el MCD aritmético estándar para su parte numérica."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Halla el coeficiente del MCD de $30m^2$, $45m^3$ y $60m^4$.", "choices": ["A) 5", "B) 10", "C) 15", "D) 30"], "ans": "C) 15", "sol": "El mayor número que divide a 30, 45 y 60 es 15. (15*2, 15*3, 15*4)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si los coeficientes son $-8$ y $-12$, el coeficiente del MCD es estrictamente $-4$?", "ans": "Falso", "sol": "En álgebra, el MCD se define típicamente como positivo. Se extrae el factor común 4. Aunque extraer el signo negativo como factor (-4) es matemáticamente válido, no es obligatorio ni la respuesta estándar de un 'coeficiente de MCD'."}
    ]
})

# 3. PARTE_LITERAL_MONOMIOS (MCD)
nodes.append({
    "sid": "MAT.ALG.MCD_ALGEBRAICO.PARTE_LITERAL_MONOMIOS",
    "title": "MCD de la Parte Literal (Letras)",
    "obj": "Aprender la regla para extraer el MCD de las variables y sus exponentes.",
    "intro": "¿Qué pasa con las letras? Las variables en álgebra siguen una regla implacable para el MCD: solo sobreviven las letras que están en TODOS los términos, y siempre se escogen en su versión más 'débil' (el menor exponente).",
    "res": "Para obtener la parte literal del MCD, se deben escribir únicamente las bases (letras) que sean comunes a TODOS los monomios, y elevar cada una a su menor exponente presente.",
    "expl": "Pensemos en tres estudiantes que quieren aportar dinero a un fondo común, pero la regla es que todos deben aportar exactamente la misma cantidad.\n- Ana tiene $x^5$ monedas.\n- Beto tiene $x^3$ monedas.\n- Carlos tiene $x^4$ monedas.\n\nSi todos deben aportar lo mismo, lo máximo que pueden dar sin que nadie quede debiendo es $x^3$. Beto da todo lo que tiene, Ana y Carlos dan $x^3$ y les sobra.\n\nEsa es la regla del MCD literal: **Las letras comunes, con el menor exponente**.\n\nSi Carlos tuviera billetes 'y' pero Ana y Beto no, entonces el fondo común no puede incluir billetes 'y'. La variable 'y' se ignora por completo en el MCD porque no es COMÚN a todos.",
    "proc": [
        "Paso 1: Observa todas las letras en los monomios dados.",
        "Paso 2: Selecciona SÓLO aquellas letras que aparecen en todos y cada uno de los monomios.",
        "Paso 3: Para cada letra seleccionada, busca en los monomios cuál es su exponente más pequeño.",
        "Paso 4: Eleva la letra a ese menor exponente. Ese es el resultado."
    ],
    "ex_a": [
        ("Ejemplo 1", "Halla el MCD literal de $a^4 b^2 c$, $a^3 b^5$ y $a^6 b^3 c^2$.", ["Letras en los 3 monomios: 'a' y 'b'. (La 'c' no está en el segundo, se descarta).", "Menor exponente para 'a': está $a^4, a^3, a^6$. El menor es 3 $\\rightarrow a^3$.", "Menor exponente para 'b': está $b^2, b^5, b^3$. El menor es 2 $\\rightarrow b^2$.", "El MCD literal es $a^3 b^2$."])
    ],
    "ex_b": [
        ("MCD literal de $x^2 y$ y $w^3 z$.", "1", ["No hay ninguna letra en común entre ambos monomios. El MCD no tiene parte literal (es 1)."])
    ],
    "errs": [
        "Incluir letras que no están en todos los términos.",
        "Elegir el exponente más alto (confusión clásica con el MCM)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "La regla de oro para el MCD literal indica que se escogen:", "choices": ["A) Las letras comunes con el mayor exponente.", "B) Las letras comunes y no comunes con el menor exponente.", "C) Las letras comunes con el menor exponente.", "D) Todas las letras que aparezcan, sin importar el exponente."], "ans": "C) Las letras comunes con el menor exponente.", "sol": "Solo lo que todos comparten, restringido al nivel del que menos tiene."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Halla la parte literal del MCD de: $x^5 y^4 z^2$, $x^3 y^6 z^5$, $x^4 y^5$.", "choices": ["A) $x^3 y^4 z^2$", "B) $x^3 y^4$", "C) $x^5 y^6 z^5$", "D) $x^3 y^4 z$"], "ans": "B) $x^3 y^4$", "sol": "La 'z' no está en el tercer término, así que se elimina. Para x, el menor es 3. Para y, el menor es 4."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si una letra no tiene exponente escrito, se asume que su exponente es 1 al buscar el menor exponente?", "ans": "Verdadero", "sol": "Por ejemplo, entre x^2 y x, el menor exponente es el 1 invisible de la x."}
    ]
})

# 4. MCD_MONOMIOS
nodes.append({
    "sid": "MAT.ALG.MCD_ALGEBRAICO.MCD_MONOMIOS",
    "title": "Cálculo del MCD de Monomios Completos",
    "obj": "Integrar el coeficiente numérico y la parte literal para hallar el MCD completo de varios monomios.",
    "intro": "Ya dominas los números y las letras por separado. Ahora es el momento de juntarlos para ensamblar el Máximo Común Divisor definitivo de cualquier grupo de monomios.",
    "res": "El MCD de dos o más monomios es un nuevo monomio compuesto por el MCD aritmético de sus coeficientes, multiplicado por las variables comunes elevadas a su menor exponente.",
    "expl": "Vamos a calcular el MCD completo de $20x^4 y^2 z$ y $30x^2 y^5$.\n\n1. **Parte numérica (coeficientes):**\n   MCD aritmético de 20 y 30. El mayor divisor de ambos es el 10.\n\n2. **Parte literal (letras):**\n   - ¿Letras comunes? Solo 'x' e 'y' (la 'z' se descarta porque falta en el segundo).\n   - Menor exponente de 'x': entre $x^4$ y $x^2$, elegimos $x^2$.\n   - Menor exponente de 'y': entre $y^2$ y $y^5$, elegimos $y^2$.\n   - Parte literal: $x^2 y^2$.\n\n3. **Ensamblaje:**\n   Juntamos ambas partes: $10x^2 y^2$.\n   Este es el monomio más grande posible que puede dividir de forma exacta tanto a $20x^4 y^2 z$ como a $30x^2 y^5$.",
    "proc": [
        "Paso 1: Calcula el MCD aritmético de los coeficientes numéricos.",
        "Paso 2: Identifica las letras que aparecen en todos los monomios.",
        "Paso 3: Asigna a cada letra común el exponente más pequeño que posea en el grupo.",
        "Paso 4: Une el número y las letras para formar el monomio MCD."
    ],
    "ex_a": [
        ("Ejemplo 1", "Halla el MCD de $15a^3 b^2$, $25a^2 b^4$ y $35a^4 b^3$.", ["MCD numérico de 15, 25 y 35: Es 5.", "Letras comunes: 'a' y 'b'.", "Menores exponentes: 'a' es 2, 'b' es 2.", "Resultado final: $5a^2 b^2$."])
    ],
    "ex_b": [
        ("MCD de $12x^3 y$ y $8x^2 y z$.", "$4x^2 y$", ["Números: MCD de 12 y 8 es 4. Letras comunes: x, y. Menor de x es 2. Menor de y es 1. z no va."])
    ],
    "errs": [
        "Sacar el MCD de los coeficientes y el MCM de las letras (combinar reglas opuestas).",
        "Olvidarse de que este procedimiento de 'MCD de monomios' es la base exacta del método de 'Factor Común'."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "El MCD que calculamos para un conjunto de monomios es matemáticamente equivalente a:", "choices": ["A) El Mínimo Común Múltiplo.", "B) El Factor Común más grande que se extrae al factorizar la suma de esos monomios.", "C) El producto de los monomios.", "D) El residuo de su división."], "ans": "B) El Factor Común más grande que se extrae al factorizar la suma de esos monomios.", "sol": "Hallar el MCD de monomios es exactamente el paso 1 de la factorización por factor común."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Calcula el MCD de $14m^4 n^3$ y $21m^3 n^5$.", "choices": ["A) $7m^4 n^5$", "B) $7m^3 n^3$", "C) $42m^3 n^3$", "D) $21m^4 n^5$"], "ans": "B) $7m^3 n^3$", "sol": "MCD(14,21)=7. Menor de m=3. Menor de n=3. -> 7m^3 n^3."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "En un análisis de redes, se necesitan subdividir tres cables cuyas capacidades están dadas por $16x^5 y^3$, $24x^3 y^4$ y $32x^4 y^2$. ¿Cuál es la mayor capacidad estándar que divide a los tres exactamente?", "choices": ["A) $8x^3 y^2$", "B) $8x^5 y^4$", "C) $4x^3 y^2$", "D) $16x^3 y^2$"], "ans": "A) $8x^3 y^2$", "sol": "MCD de 16, 24, 32 es 8. Menor exponente de x es 3. Menor de y es 2."}
    ]
})

# 5. FACTORIZACION_POLINOMIOS (MCD)
nodes.append({
    "sid": "MAT.ALG.MCD_ALGEBRAICO.FACTORIZACION_POLINOMIOS",
    "title": "MCD de Polinomios Factorizados",
    "obj": "Encontrar el Máximo Común Divisor entre polinomios (binomios, trinomios) usando sus formas factorizadas.",
    "intro": "Para hallar el MCD de expresiones más grandes que un monomio, primero debemos 'desarmarlas'. Así como descomponemos un número en primos, debemos factorizar los polinomios. Una vez factorizados, la regla es exactamente la misma que vimos antes.",
    "res": "Para hallar el MCD de varios polinomios, primero se factorizan por completo. Luego, el MCD se forma tomando EXCLUSIVAMENTE los paréntesis (factores) comunes a todos los polinomios, elevados a su menor exponente.",
    "expl": "Queremos el MCD entre $P(x) = x^2 - 4$ y $Q(x) = x^2 - 4x + 4$.\n\n1. **Factorizamos todo:**\n   - $P(x) = x^2 - 4$ es una diferencia de cuadrados: $(x+2)(x-2)$.\n   - $Q(x) = x^2 - 4x + 4$ es un trinomio cuadrado perfecto: $(x-2)^2$.\n\n2. **Buscamos factores comunes:**\n   - ¿Qué paréntesis comparten ambas expresiones? Solo el paréntesis $(x-2)$.\n   - El $(x+2)$ solo está en P(x), así que queda fuera.\n\n3. **Aplicamos el menor exponente:**\n   - En P(x) el $(x-2)$ tiene exponente 1.\n   - En Q(x) el $(x-2)$ tiene exponente 2.\n   - Escogemos el menor: exponente 1.\n\nPor tanto, el MCD es $(x-2)$.",
    "proc": [
        "Paso 1: Factoriza completamente cada uno de los polinomios dados (usa factor común, TCP, etc.).",
        "Paso 2: Trata cada paréntesis (binomio o trinomio irreducible) como si fuera una sola 'letra'.",
        "Paso 3: Identifica los paréntesis que estén presentes en TODAS las factorizaciones.",
        "Paso 4: Escribe el MCD con los paréntesis comunes elevados al menor exponente en que aparecen."
    ],
    "ex_a": [
        ("Ejemplo 1", "Halla el MCD de $A = (x-1)^3(x+5)$ y $B = (x-1)^2(x+5)^2(x-3)$.", ["Ambos ya están factorizados.", "Factores comunes: $(x-1)$ y $(x+5)$.", "Menor exp de $(x-1)$: 2. Menor exp de $(x+5)$: 1.", "MCD: $(x-1)^2(x+5)$."])
    ],
    "ex_b": [
        ("MCD entre $x^2+x$ y $x^2-1$.", "$x+1$", ["x^2+x = x(x+1). x^2-1 = (x+1)(x-1). El único factor común es (x+1)."])
    ],
    "errs": [
        "Intentar sacar el MCD mirando el polinomio sin factorizar (ej. tratar de buscar la letra 'x' con el menor exponente en una suma, lo cual es matemáticamente falso).",
        "Creer que $(x+2)$ y $(x-2)$ son el mismo factor y combinarlos."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "Para poder calcular el MCD de dos polinomios, el paso previo absolutamente necesario es:", "choices": ["A) Multiplicarlos.", "B) Sumarlos.", "C) Factorizarlos en sus bloques irreducibles.", "D) Dividirlos sintéticamente."], "ans": "C) Factorizarlos en sus bloques irreducibles.", "sol": "El MCD requiere conocer los factores base de cada expresión, lo cual exige factorización."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Dados $P = (a+b)^4 (a-b)$ y $Q = (a+b)^2 (a-b)^3 (a^2+b^2)$, ¿cuál es su MCD?", "choices": ["A) $(a+b)^4 (a-b)^3$", "B) $(a+b)^2 (a-b)$", "C) $(a+b)^4 (a-b)^3 (a^2+b^2)$", "D) $(a+b)^2 (a-b) (a^2+b^2)$"], "ans": "B) $(a+b)^2 (a-b)$", "sol": "Factores comunes son (a+b) y (a-b). Menor exp de (a+b) es 2. Menor exp de (a-b) es 1. El tercer factor no es común."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Si el lado de un cuadrado es el MCD entre el área $A = x^2 + 5x + 6$ y el perímetro modificado $P = x^2 + 4x + 4$, ¿cuánto mide el lado?", "choices": ["A) $x+2$", "B) $x+3$", "C) $(x+2)^2$", "D) No tienen MCD."], "ans": "A) $x+2$", "sol": "A = (x+3)(x+2). P = (x+2)^2. El factor común es (x+2) al menor exponente, que es 1."}
    ]
})

# 6. ALGORITMO_EUCLIDES (MCD)
nodes.append({
    "sid": "MAT.ALG.MCD_ALGEBRAICO.ALGORITMO_EUCLIDES",
    "title": "Algoritmo de Euclides para Polinomios",
    "obj": "Conocer el algoritmo de divisiones sucesivas para encontrar el MCD sin necesidad de factorizar.",
    "intro": "¿Qué pasa si te topas con dos polinomios gigantescos que no sabes cómo factorizar? Euclides, hace miles de años, inventó un truco brillante para números, que resulta que también funciona con polinomios: las divisiones sucesivas.",
    "res": "El Algoritmo de Euclides halla el MCD de dos polinomios dividiendo el de mayor grado entre el de menor grado. Si hay resto, se divide el divisor anterior por el nuevo resto, repitiendo hasta que el resto sea cero. El último divisor no nulo es el MCD.",
    "expl": "El proceso del Algoritmo de Euclides:\nSean $P(x)$ y $Q(x)$.\n1. Divide $P(x)$ entre $Q(x)$. Obtienes un resto $R_1(x)$.\n   - Si $R_1 = 0$, el MCD es $Q(x)$. ¡Terminaste!\n   - Si $R_1 \\neq 0$, avanzamos al paso 2.\n2. Divide el divisor antiguo $Q(x)$ entre el nuevo resto $R_1(x)$. Obtienes un resto $R_2(x)$.\n3. Continúa dividiendo el divisor de la etapa anterior por el resto de esa misma etapa.\n4. Cuando finalmente una división dé resto EXACTAMENTE 0, el polinomio por el que dividiste en esa última etapa (tu último divisor) es el MCD.\n\nEste método es muy poderoso para ordenadores y algoritmos computacionales, ya que evita por completo tener que factorizar. (Se recomienda simplificar coeficientes numéricos en los restos intermedios para facilitar el cálculo).",
    "proc": [
        "Paso 1: Identifica el polinomio de mayor grado como Dividendo y el menor como Divisor.",
        "Paso 2: Realiza la división larga polinomial.",
        "Paso 3: Si el residuo es 0, el divisor actual es el MCD.",
        "Paso 4: Si el residuo no es 0, toma tu divisor actual y divídelo entre el residuo que acabas de encontrar.",
        "Paso 5: Repite hasta obtener residuo 0."
    ],
    "ex_a": [
        ("Ejemplo 1", "Concepto en números: MCD de 1071 y 462.", ["1071 / 462 = 2, resto 147.", "462 / 147 = 3, resto 21.", "147 / 21 = 7, resto 0.", "El último divisor fue 21. El MCD es 21. El álgebra polinomial usa la misma lógica exacta."])
    ],
    "ex_b": [
        ("¿Qué se hace cuando el resto de la primera división de P(x) / Q(x) no es cero?", "Dividir Q(x) entre el resto.", ["La regla es empujar los términos: el divisor se convierte en dividendo, y el resto en divisor."])
    ],
    "errs": [
        "Confundir quién se divide por quién en las iteraciones siguientes (siempre es el divisor viejo entre el resto nuevo).",
        "Olvidar que los coeficientes pueden multiplicarse o simplificarse por constantes durante el proceso sin alterar el MCD algebraico esencial."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Cuál es la principal ventaja del Algoritmo de Euclides para polinomios?", "choices": ["A) Es más corto que factorizar.", "B) Permite hallar el MCD de polinomios de grado alto sin tener que encontrar sus raíces ni factorizarlos.", "C) Siempre da como resultado 1.", "D) Funciona para el MCM."], "ans": "B) Permite hallar el MCD de polinomios de grado alto sin tener que encontrar sus raíces ni factorizarlos.", "sol": "Factorizar polinomios de grado 5 o superior puede ser analíticamente imposible. Euclides siempre funciona porque usa división matemática básica."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El Algoritmo de Euclides termina cuando el cociente de la división es 0?", "ans": "Falso", "sol": "El algoritmo termina cuando el RESTO de la división es 0. El divisor de esa etapa es la respuesta."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Es válido dividir o multiplicar un residuo intermedio por un número constante (ej: dividir todo entre 2) para facilitar los cálculos del Algoritmo de Euclides?", "ans": "Verdadero", "sol": "En álgebra polinomial, las constantes multiplicativas no afectan los factores estructurales del MCD, por lo que simplificar constantes intermedias es un truco estándar."}
    ]
})

# 7. CONCEPTO_MCM
nodes.append({
    "sid": "MAT.ALG.MCM_ALGEBRAICO.CONCEPTO_MCM",
    "title": "Concepto de MCM Algebraico",
    "obj": "Comprender la definición del Mínimo Común Múltiplo (MCM) aplicado a expresiones algebraicas.",
    "intro": "Si el MCD era el divisor más grande, el Mínimo Común Múltiplo (MCM) es el contenedor más pequeño. El MCM busca la expresión algebraica de menor grado posible que pueda ser dividida EXACTAMENTE por todas las expresiones originales.",
    "res": "El Mínimo Común Múltiplo (MCM) de varias expresiones algebraicas es la expresión de menor grado y coeficiente que las contiene a todas como factores.",
    "expl": "El MCM numérico de 4 y 6 es 12, porque 12 es el número más pequeño que contiene a ambos (12/4=3, 12/6=2).\n\nEn álgebra, el MCM entre $x^3$ y $x^5$ es el término más pequeño que puede albergar a ambos.\n- $x^3$ no sirve porque no puede albergar a $x^5$ (faltan 2 grados).\n- $x^5$ sirve perfecto: puede contener a $x^5$ y tiene espacio de sobra para albergar a $x^3$.\n\nLa regla conceptual para el MCM es tomar **todos los factores** (comunes y no comunes) y elevarlos a su **mayor exponente**. Al tomar todo lo de todos en su máxima cantidad, nos aseguramos de que cualquier expresión original quepa perfectamente en el MCM.",
    "proc": [
        "Paso 1: El MCM debe actuar como un contenedor que incluye la totalidad de las expresiones dadas.",
        "Paso 2: La regla fundamental es juntar TODO tipo de letra o factor que aparezca en cualquier lugar.",
        "Paso 3: Si un factor se repite, se debe elegir aquel que tenga el MAYOR exponente."
    ],
    "ex_a": [
        ("Ejemplo 1", "Conceptualmente, ¿cuál es el MCM de $(x+1)$ y $(x-2)$?", ["Son dos bloques distintos, sin nada en común.", "El MCM debe contenerlos a ambos.", "Por lo tanto, se multiplican: el MCM es $(x+1)(x-2)$."])
    ],
    "ex_b": [
        ("¿Cuál es el MCM de $x$ y $x^2$?", "$x^2$", ["Buscamos el mayor exponente de la variable en común, para asegurarnos de que la otra quepa dentro. $x^2$ alberga a $x$ y a $x^2$."])
    ],
    "errs": [
        "Confundir MCM con MCD (elegir solo lo común, o el exponente menor).",
        "Olvidarse de incluir letras o paréntesis que no son comunes. ¡El MCM no perdona exclusiones, debe llevarlo todo!"
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "En álgebra, ¿qué representa el MCM de dos polinomios?", "choices": ["A) El polinomio de menor grado que contiene a ambos como factores.", "B) El divisor más grande.", "C) La resta de los polinomios.", "D) El mayor polinomio posible."], "ans": "A) El polinomio de menor grado que contiene a ambos como factores.", "sol": "Debe ser múltiplo de ambos (contenerlos), y buscamos el más pequeño de esos múltiplos (mínimo)."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Si dos polinomios son primos entre sí, ¿cuál es su MCM?", "choices": ["A) 1", "B) 0", "C) El producto de ambos", "D) No existe MCM"], "ans": "C) El producto de ambos", "sol": "Al no compartir nada, el contenedor más pequeño es multiplicar uno por el otro (igual que MCM de 3 y 5 es 15)."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El MCM debe incluir letras o factores que solo aparezcan en UNO de los polinomios originales?", "ans": "Verdadero", "sol": "Sí (factores \"no comunes\"). El MCM es inclusivo, necesita todo para poder ser divisible por todos."}
    ]
})

# 8. COEFICIENTE_MONOMIOS (MCM)
nodes.append({
    "sid": "MAT.ALG.MCM_ALGEBRAICO.COEFICIENTE_MONOMIOS",
    "title": "MCM de los Coeficientes Numéricos",
    "obj": "Calcular el Mínimo Común Múltiplo de los coeficientes numéricos en un conjunto de monomios.",
    "intro": "Para construir el MCM de monomios, empezamos por la fundación numérica. Necesitamos encontrar el Mínimo Común Múltiplo tradicional de los números que van por delante.",
    "res": "El coeficiente numérico del MCM algebraico es el MCM aritmético de los coeficientes de las expresiones (el menor número positivo que sea múltiplo de todos ellos).",
    "expl": "Tenemos los monomios $4x$ y $6y$.\nIgnoramos las letras y miramos el 4 y el 6.\n\nBuscamos el MCM de 4 y 6:\n- Múltiplos de 4: 4, 8, 12, 16, 20...\n- Múltiplos de 6: 6, 12, 18, 24...\n\nEl primer número que coincide en ambas listas es el **12**.\nPor lo tanto, la parte numérica del MCM de nuestros monomios será 12.\n\nEste 12 garantiza que cuando hagamos divisiones (ej. $12/4$ o $12/6$), siempre obtendremos resultados enteros exactos.",
    "proc": [
        "Paso 1: Extrae los coeficientes numéricos de los monomios, tomando sus valores positivos.",
        "Paso 2: Descompón cada número en sus factores primos.",
        "Paso 3: Multiplica todos los factores primos diferentes, eligiendo el de mayor exponente si se repiten.",
        "Paso 4: El número resultante es el coeficiente del MCM algebraico."
    ],
    "ex_a": [
        ("Ejemplo 1", "Halla el coeficiente del MCM de $15a$ y $10b$.", ["Coeficientes: 15 y 10.", "Factores: $15 = 3 \\times 5$. $10 = 2 \\times 5$.", "MCM: Tomamos todos los primos al mayor exponente: $2^1 \\times 3^1 \\times 5^1 = 30$.", "El coeficiente del MCM es 30."])
    ],
    "ex_b": [
        ("MCM numérico entre $2x$ y $3y$.", "6", ["2 y 3 son primos relativos, así que su MCM es su multiplicación: 6."])
    ],
    "errs": [
        "Calcular el MCD en lugar del MCM (ej. decir que el MCM de 12 y 18 es 6, en vez de 36).",
        "Multiplicar ciegamente todos los números. (Ej. para 6 y 8, decir que el MCM es 48. Funciona matemáticamente, pero no es el MÍNIMO, que sería 24)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué método aritmético se usa para la parte numérica del MCM algebraico?", "choices": ["A) El Mínimo Común Múltiplo tradicional.", "B) El Máximo Común Divisor.", "C) Se suman los números.", "D) Se deja en 1."], "ans": "A) El Mínimo Común Múltiplo tradicional.", "sol": "El comportamiento numérico es idéntico a la aritmética escolar."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Calcula el coeficiente del MCM de $12x^2$, $18x^3$ y $24x^4$.", "choices": ["A) 6", "B) 36", "C) 72", "D) 144"], "ans": "C) 72", "sol": "El MCM de 12, 18 y 24 es 72. (72/12=6, 72/18=4, 72/24=3)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si multiplicas todos los coeficientes numéricos siempre obtienes el MCM?", "ans": "Falso", "sol": "Multiplicarlos te da un múltiplo común, pero rara vez es el \"mínimo\". Por ejemplo, 4 y 6 multiplicados dan 24, pero el MCM es 12."}
    ]
})

# 9. PARTE_LITERAL_MONOMIOS (MCM)
nodes.append({
    "sid": "MAT.ALG.MCM_ALGEBRAICO.PARTE_LITERAL_MONOMIOS",
    "title": "MCM de la Parte Literal (Letras)",
    "obj": "Aprender la regla para crear el contenedor literal perfecto usando factores comunes y no comunes.",
    "intro": "¿Y qué hay de las letras en el MCM? Aquí reina la inclusión absoluta. Si una letra aparece, sin importar si está sola o en todos lados, debe estar en el MCM. Y si hay competencia de exponentes, ¡gana siempre el más fuerte!",
    "res": "Para obtener la parte literal del MCM, escribe TODAS las bases (letras) diferentes que aparezcan en los monomios, y eleva cada una a su MAYOR exponente presente.",
    "expl": "Retomemos a Ana, Beto y Carlos, pero ahora armando un super-kit de herramientas para el taller.\n- Ana trae: llave 5, llave 8.\n- Beto trae: llave 8, martillo.\n- Carlos trae: martillo, destornillador.\n\nEl super-kit (MCM) debe contener TODO lo necesario para replicar la caja de cualquiera de los tres. Necesitamos: llave 5, llave 8, martillo, destornillador.\n\nEn álgebra, es lo mismo con los exponentes:\nSi tenemos $x^2 y$, $x^4$, y $y^3 z$.\n- Listamos todas las letras presentes: x, y, z.\n- Para 'x', compiten $x^2$ y $x^4$. El ganador (mayor) es $x^4$.\n- Para 'y', compiten $y^1$ y $y^3$. El mayor es $y^3$.\n- Para 'z', solo hay $z^1$, así que gana $z^1$.\n\nParte literal del MCM: $x^4 y^3 z$. Cualquier monomio original cabe perfectamente aquí dentro.",
    "proc": [
        "Paso 1: Haz una lista con TODAS las letras distintas que aparezcan, sin excluir ninguna.",
        "Paso 2: Revisa los exponentes que tiene cada letra en los distintos monomios.",
        "Paso 3: Asígnale a cada letra de tu lista el exponente MÁS GRANDE que hayas encontrado.",
        "Paso 4: Multiplica todas las letras resultantes."
    ],
    "ex_a": [
        ("Ejemplo 1", "Halla el MCM literal de $m^3 n^2$, $m^5 p$ y $n^4 p^2$.", ["Letras totales: m, n, p.", "Mayor exp de m: 5 ($m^5$).", "Mayor exp de n: 4 ($n^4$).", "Mayor exp de p: 2 ($p^2$).", "El MCM literal es $m^5 n^4 p^2$."])
    ],
    "ex_b": [
        ("MCM literal de $a^2$ y $b^3$.", "$a^2 b^3$", ["Se incluyen ambas variables sin alterar sus exponentes porque no hay competencia: $a^2 b^3$."])
    ],
    "errs": [
        "Descartar letras que no son comunes a todos los términos (es el error fatal más común, contamina el MCM con lógica de MCD).",
        "Elegir el exponente más pequeño."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "La regla de oro para el MCM literal indica que se escogen:", "choices": ["A) Solo las letras comunes al mayor exponente.", "B) Las letras comunes y no comunes al mayor exponente.", "C) Las letras comunes y no comunes al menor exponente.", "D) Las letras multiplicadas entre sí."], "ans": "B) Las letras comunes y no comunes al mayor exponente.", "sol": "Es la definición técnica de inclusión máxima (MCM)."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Halla la parte literal del MCM de $x^3 y^2$, $x^5 z$, $y^4 w^2$.", "choices": ["A) $x^3 y^2$", "B) $x^5 y^4 z w^2$", "C) $x^8 y^6 z w^2$", "D) $x^5 y^4$"], "ans": "B) $x^5 y^4 z w^2$", "sol": "Todas las letras (x,y,z,w) a su mayor exponente (x5, y4, z1, w2)."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si una letra (como la 'a') aparece con exponente 3 en un monomio y con exponente 5 en otro, en el MCM debemos sumar ambos exponentes para formar $a^8$?", "ans": "Falso", "sol": "No se suman los exponentes, se SELECCIONA el mayor. La respuesta correcta es a^5."}
    ]
})

# 10. MCM_MONOMIOS
nodes.append({
    "sid": "MAT.ALG.MCM_ALGEBRAICO.MCM_MONOMIOS",
    "title": "Cálculo del MCM de Monomios Completos",
    "obj": "Integrar el coeficiente numérico y la parte literal para hallar el MCM completo de varios monomios.",
    "intro": "Uniendo las dos mitades que hemos aprendido (números y letras), puedes ensamblar el MCM completo. Este monomio gigante será vital más adelante cuando queramos sumar o restar fracciones algebraicas.",
    "res": "El MCM completo de dos o más monomios se obtiene multiplicando el MCM de sus coeficientes por las letras comunes y no comunes elevadas a su mayor exponente.",
    "expl": "Vamos a encontrar el MCM de $6a^2 b^3$ y $8a^4 c$.\n\n1. **Parte numérica (coeficientes):**\n   MCM de 6 y 8. Múltiplos de 6: 6, 12, 18, 24... Múltiplos de 8: 8, 16, 24...\n   El MCM es 24.\n\n2. **Parte literal (letras):**\n   - Letras presentes: 'a', 'b', 'c'.\n   - Mayor exp de 'a': entre $a^2$ y $a^4$ gana $a^4$.\n   - Mayor exp de 'b': $b^3$.\n   - Mayor exp de 'c': $c^1$.\n   - Parte literal es $a^4 b^3 c$.\n\n3. **Ensamblaje:**\n   Juntamos todo: $24a^4 b^3 c$. ¡Ese es el MCM perfecto!",
    "proc": [
        "Paso 1: Calcula el MCM aritmético de los coeficientes numéricos.",
        "Paso 2: Extrae todas las letras diferentes que encuentres.",
        "Paso 3: Colócale a cada letra el exponente mayor con el que aparezca en el grupo.",
        "Paso 4: Multiplica la parte numérica y la parte literal."
    ],
    "ex_a": [
        ("Ejemplo 1", "Halla el MCM de $10x^3 y$, $15x y^2$ y $5y^3 z$.", ["Números: MCM de 10, 15 y 5. El mayor múltiplo mínimo común es 30.", "Letras presentes: x, y, z.", "Exp. mayores: $x^3$, $y^3$, $z^1$.", "Resultado final: $30x^3 y^3 z$."])
    ],
    "ex_b": [
        ("Calcula el MCM de $3p$ y $4q$.", "$12pq$", ["MCM de 3 y 4 es 12. Letras p y q. Todo junto: 12pq."])
    ],
    "errs": [
        "Intercambiar la regla numérica con la literal (sacar MCM de letras pero MCD de números).",
        "Olvidar escribir una variable solitaria que estaba escondida en un rincón del último monomio."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "Al dividir el MCM algebraico recién calculado entre cualquiera de los monomios originales, el resultado será:", "choices": ["A) Siempre 0.", "B) Un monomio exacto (sin fracciones ni exponentes negativos).", "C) Una fracción algebraica.", "D) El MCD."], "ans": "B) Un monomio exacto (sin fracciones ni exponentes negativos).", "sol": "Ese es todo el punto del MCM: al contenerlos a todos de forma perfecta, las divisiones son siempre exactas."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Halla el MCM de $4x^2 y^3$ y $6x^5$.", "choices": ["A) $2x^2$", "B) $12x^5 y^3$", "C) $24x^7 y^3$", "D) $12x^2 y^3$"], "ans": "B) $12x^5 y^3$", "sol": "MCM de 4 y 6 es 12. Mayor x es 5. Mayor y es 3."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un algoritmo de compresión debe asignar un bloque de memoria mínimo que pueda almacenar paquetes de tamaño $9A^3 B$, $12A^2 C$ y $18B^2 C^2$. ¿Cuál debe ser el tamaño del bloque asignado?", "choices": ["A) $3A^2 B$", "B) $36A^3 B^2 C^2$", "C) $72A^5 B^3 C^3$", "D) $36A^3 B C$"], "ans": "B) $36A^3 B^2 C^2$", "sol": "MCM(9,12,18) = 36. Letras al mayor exponente: A^3, B^2, C^2."}
    ]
})

# 11. FACTORIZACION_POLINOMIOS (MCM)
nodes.append({
    "sid": "MAT.ALG.MCM_ALGEBRAICO.FACTORIZACION_POLINOMIOS",
    "title": "MCM de Polinomios Factorizados",
    "obj": "Encontrar el Mínimo Común Múltiplo entre polinomios (binomios, trinomios) usando sus formas factorizadas.",
    "intro": "¿Recuerdas que desarmamos polinomios para hallar el MCD? Para el MCM haremos exactamente lo mismo. Factorizaremos primero, y luego aplicaremos la regla de \"todo el mundo adentro al mayor exponente\".",
    "res": "Para hallar el MCM de varios polinomios, primero se factorizan completamente. Luego, el MCM se forma tomando TODOS los paréntesis diferentes (comunes y no comunes) y elevándolos a su mayor exponente.",
    "expl": "Vamos a hallar el MCM entre $P(x) = x^2 - 9$ y $Q(x) = x^2 + 6x + 9$.\n\n1. **Factorizamos:**\n   - $P(x) = x^2 - 9 \\rightarrow (x-3)(x+3)$\n   - $Q(x) = x^2 + 6x + 9 \\rightarrow (x+3)^2$\n\n2. **Construimos el MCM:**\n   - Hacemos la lista de TODOS los paréntesis que existen en el problema: $(x-3)$ y $(x+3)$.\n   - Buscamos el mayor exponente para $(x-3)$: solo aparece elevado a 1, así que queda $(x-3)^1$.\n   - Buscamos el mayor exponente para $(x+3)$: en $P(x)$ está a la 1, pero en $Q(x)$ está a la 2. Gana el 2, así que queda $(x+3)^2$.\n\n3. **MCM Final:** $(x-3)(x+3)^2$.\n\nNota: No expandas este resultado (no lo multipliques para hacerlo gigante). En álgebra, mantenerlo factorizado es la forma correcta y más útil de presentar el MCM.",
    "proc": [
        "Paso 1: Factoriza completamente cada uno de los polinomios.",
        "Paso 2: Haz una lista mental (o escrita) de todos los factores (paréntesis) distintos que veas.",
        "Paso 3: Asígnale a cada paréntesis el exponente más alto que tenga en el grupo.",
        "Paso 4: Multiplica todos estos paréntesis. Deja el resultado expresado (factorizado)."
    ],
    "ex_a": [
        ("Ejemplo 1", "Halla el MCM de $2x+4$ y $x^2-4$.", ["Factorizamos: $2x+4 = 2(x+2)$.", "Factorizamos: $x^2-4 = (x+2)(x-2)$.", "Lista de factores distintos: el número '2', el paréntesis $(x+2)$ y el paréntesis $(x-2)$.", "Mayor exponente de cada uno es 1.", "MCM: $2(x+2)(x-2)$."])
    ],
    "ex_b": [
        ("MCM entre $(x-1)^3$ y $(x-1)(x+5)$.", "$(x-1)^3(x+5)$", ["Factores: (x-1) y (x+5). Mayor de (x-1) es 3. Mayor de (x+5) es 1."])
    ],
    "errs": [
        "Confundir la regla del MCD y tomar solo los factores comunes (lo que arruina el MCM).",
        "Si hay factores numéricos externos (ej. un 3 y un 6), olvidarse de sacar el MCM numérico de esos números (que sería 6)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Al buscar el MCM de polinomios factorizados, ¿qué factores se deben incluir?", "choices": ["A) Solo los factores comunes al menor exponente.", "B) Todos los factores (comunes y no comunes) al mayor exponente.", "C) Solo los factores no comunes.", "D) Las raíces sin repetir."], "ans": "B) Todos los factores (comunes y no comunes) al mayor exponente.", "sol": "Es la regla universal de construcción del Mínimo Común Múltiplo."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Encuentra el MCM de los polinomios factorizados $A = (x-2)^2 (x+1)$ y $B = (x-2) (x+3)^2$.", "choices": ["A) $(x-2)$", "B) $(x-2)(x+1)(x+3)$", "C) $(x-2)^2 (x+1) (x+3)^2$", "D) $(x-2)^3 (x+1) (x+3)^2$"], "ans": "C) $(x-2)^2 (x+1) (x+3)^2$", "sol": "Factores: (x-2), (x+1), (x+3). Mayor exp de (x-2) es 2, mayor de (x+3) es 2."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Es mejor dejar la respuesta final del MCM multiplicada en un solo polinomio gigante o mantenerla con sus paréntesis individuales?", "ans": "Falso", "sol": "Mantenerla factorizada (con paréntesis) es mucho mejor y estándar en álgebra para el siguiente paso (trabajar con denominadores comunes). (Falso a la primera opción, Verdadero a la segunda). Ok, digamos Falso a multiplicarla."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Un fabricante de baldosas tiene dos modelos de áreas $A_1 = x^2 - x - 6$ y $A_2 = x^2 - 9$. Necesita una caja cuyo fondo (área) pueda albergar exactamente cualquiera de las dos baldosas sin desperdicio asimétrico (es decir, el MCM). ¿Cuál es la expresión factorizada de la caja?", "choices": ["A) $(x-3)(x+2)(x+3)$", "B) $(x-3)(x+3)$", "C) $(x-3)$", "D) $(x-3)^2 (x+2) (x+3)$"], "ans": "A) $(x-3)(x+2)(x+3)$", "sol": "A1 = (x-3)(x+2). A2 = (x-3)(x+3). Factores: (x-3), (x+2), (x+3). Todos al exponente 1."}
    ]
})

# 12. DENOMINADOR_COMUN (MCM)
nodes.append({
    "sid": "MAT.ALG.MCM_ALGEBRAICO.DENOMINADOR_COMUN",
    "title": "El MCM como Denominador Común",
    "obj": "Comprender la utilidad directa del MCM algebraico en la suma y resta de fracciones algebraicas.",
    "intro": "¿Para qué sirve exactamente el MCM en álgebra? Su hábitat natural y propósito en la vida matemática es actuar como el \"Mínimo Común Denominador\" cuando quieres sumar o restar fracciones complejas.",
    "res": "Al sumar o restar fracciones algebraicas con denominadores distintos, el MCM de esos denominadores se convierte en el nuevo denominador común, garantizando la expresión más simplificada posible.",
    "expl": "Imagínate que debes sumar $\\frac{1}{x^2 - 4} + \\frac{1}{x^2 + 4x + 4}$.\nSumarlas directamente es imposible porque los denominadores no coinciden.\n\nEl truco universal es reemplazar los denominadores de abajo por un único \"súper-denominador\" en el que ambos quepan perfectamente. ¡Ese es el MCM!\nComo vimos antes, el MCM de esos dos denominadores factorizados es $(x-2)(x+2)^2$.\n\nUna vez que estableces que tu denominador común es $(x-2)(x+2)^2$, aplicas la lógica aritmética de la enseñanza básica: amplificas los numeradores según lo que le falta a su denominador original para convertirse en el MCM. Esto lo dominaremos en el bloque de sumas de fracciones, pero saber calcular el MCM es el $80\\%$ del trabajo pesado.",
    "proc": [
        "Paso 1: Si tienes una suma/resta de fracciones, toma solo la parte inferior (los denominadores).",
        "Paso 2: Factorízalos completamente (cada uno por separado).",
        "Paso 3: Extrae el MCM de esos denominadores factorizados.",
        "Paso 4: Dibuja una línea de fracción larga y escribe tu MCM en la parte inferior. ¡Estás listo para amplificar!"
    ],
    "ex_a": [
        ("Ejemplo 1", "Determina el denominador común para $\\frac{5}{3x} + \\frac{2}{x^2}$.", ["Los denominadores son $3x$ y $x^2$.", "MCM numérico de 3 y 1 es 3.", "MCM de las letras es $x^2$ (mayor exponente).", "El denominador común será $3x^2$."])
    ],
    "ex_b": [
        ("Halla el denominador común para $\\frac{1}{a} - \\frac{1}{a+b}$.", "$a(a+b)$", ["Los denominadores son 'a' y '(a+b)'. Son factores distintos, por lo que el MCM es su producto: $a(a+b)$."])
    ],
    "errs": [
        "Creer que el denominador común SIEMPRE es la simple multiplicación de todos los denominadores juntos. (Multiplicarlos funciona matemáticamente, pero a menudo no es el MÍNIMO y resultará en un monstruo gigante imposible de reducir después)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Por qué es crucial calcular el Mínimo Común Múltiplo al sumar fracciones algebraicas?", "choices": ["A) Porque permite multiplicar las fracciones más rápido.", "B) Porque se usa como el denominador común más pequeño posible.", "C) Para simplificar la fracción final a cero.", "D) Es un paso opcional sin importancia."], "ans": "B) Porque se usa como el denominador común más pequeño posible.", "sol": "Garantiza sumar eficientemente sin inflar los grados de los polinomios innecesariamente."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál es el mínimo denominador común para $\\frac{3}{m-n} - \\frac{2}{(m-n)^2}$?", "choices": ["A) $m-n$", "B) $(m-n)^3$", "C) $(m-n)^2$", "D) $(m-n)^2 - (m-n)$"], "ans": "C) $(m-n)^2$", "sol": "El MCM entre (m-n)^1 y (m-n)^2 es (m-n)^2 (se toma el mayor exponente)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "En un circuito, la impedancia total requiere sumar inversas: $\\frac{1}{x^2-1} + \\frac{1}{x^2+x}$. Para resolver esto analíticamente, el ingeniero busca el denominador común MÍNIMO. ¿Cuál es?", "choices": ["A) $(x-1)(x+1)x$", "B) $(x^2-1)(x^2+x)$", "C) $x(x-1)^2(x+1)$", "D) $(x+1)^2$"], "ans": "A) $(x-1)(x+1)x$", "sol": "D1 = (x-1)(x+1). D2 = x(x+1). MCM: factores x, (x-1), (x+1). Todos a exp 1. -> x(x-1)(x+1). La opción B es multiplicar a lo bruto."}
    ]
})


with open("docs/conocimiento/ejercicios/mat-alg-fracciones-banco-gen-1.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

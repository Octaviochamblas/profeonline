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
    filename = "docs/conocimiento/ejercicios/mat-alg-fracciones-banco-gen-2.jsonl"
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

# 1. DEFINICION_FRACCION
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_BASE.DEFINICION_FRACCION",
    "title": "Definición de Fracción Algebraica",
    "obj": "Comprender qué es una fracción algebraica y sus partes constituyentes.",
    "intro": "Las fracciones no son solo para números enteros. En álgebra, dividimos polinomios enteros entre otros polinomios, creando fracciones algebraicas. Funcionan casi igual que las numéricas, pero con letras.",
    "res": "Una fracción algebraica es el cociente de dos expresiones algebraicas (generalmente polinomios), donde el denominador debe ser distinto de cero.",
    "expl": "Una fracción algebraica tiene la forma $\\frac{P(x)}{Q(x)}$.\n- El polinomio superior, $P(x)$, se llama **numerador**.\n- El polinomio inferior, $Q(x)$, se llama **denominador**.\n\nEs idéntico a una fracción aritmética como $\\frac{3}{4}$, solo que ahora podemos tener cosas como $\\frac{x^2 - 1}{x + 3}$. La principal diferencia es que al contener variables, su valor cambia dependiendo del número que reemplacemos en las letras.",
    "proc": [
        "Paso 1: Identifica la expresión que se encuentra sobre la línea divisoria como el numerador.",
        "Paso 2: Identifica la expresión debajo de la línea como el denominador.",
        "Paso 3: Recuerda que la línea central representa la operación de división."
    ],
    "ex_a": [
        ("Ejemplo 1", "Conceptualmente, identifica numerador y denominador de $\\frac{2a+b}{3a^2}$.", ["Numerador (parte de arriba): $2a+b$.", "Denominador (parte de abajo): $3a^2$.", "Es el cociente de un binomio dividido por un monomio."])
    ],
    "ex_b": [
        ("¿Es $\\frac{x}{5}$ una fracción algebraica?", "Sí", ["Cualquier cociente de expresiones algebraicas es una fracción algebraica, incluso si el denominador es solo un número."])
    ],
    "errs": [
        "Confundir numerador con denominador.",
        "Creer que una fracción sin variables en el denominador (como $x/2$) no es algebraica. Sí lo es, pero también se puede escribir como un polinomio regular (1/2)*x."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué representa la línea horizontal en una fracción algebraica?", "choices": ["A) Una suma oculta.", "B) Una resta entre los polinomios.", "C) Una operación de división.", "D) El límite de la ecuación."], "ans": "C) Una operación de división.", "sol": "Toda fracción es, por definición, una división del numerador entre el denominador."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "En la fracción $\\frac{m^2 - n}{m+n}$, el numerador es:", "choices": ["A) $m+n$", "B) $m^2 - n$", "C) $m^2$", "D) $n$"], "ans": "B) $m^2 - n$", "sol": "El numerador es toda la expresión que está en la parte superior."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Un polinomio normal como $x^2 + 5$ puede considerarse una fracción algebraica con denominador 1?", "ans": "Verdadero", "sol": "Correcto, toda expresión puede escribirse sobre 1 matemáticamente."}
    ]
})

# 2. DENOMINADOR_NO_NULO
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_BASE.DENOMINADOR_NO_NULO",
    "title": "La Regla de Oro: Denominador Distinto de Cero",
    "obj": "Entender la restricción fundamental de que la división por cero no está definida en matemáticas.",
    "intro": "En álgebra hay una regla que nunca, bajo ninguna circunstancia, se puede romper: la división por cero no existe. Esta prohibición matemática pura es la base de todas las restricciones en fracciones algebraicas.",
    "res": "En cualquier fracción matemática o algebraica, el valor del denominador NUNCA puede ser cero, porque la división por cero no está definida.",
    "expl": "Si tienes 10 dulces y los divides entre 2 niños, a cada uno le tocan 5. (10/2 = 5).\nSi tienes 10 dulces y los divides entre 0 niños... ¿cuántos le tocan a cada uno? La pregunta no tiene sentido.\nMatemáticamente, $\\frac{P(x)}{0}$ es una aberración que 'rompe' la lógica aritmética. Por esto, siempre que veas una fracción algebraica $\\frac{P(x)}{Q(x)}$, debes declarar de inmediato la ley marcial: $Q(x) \\neq 0$.",
    "proc": [
        "Paso 1: Siempre que veas una fracción, mira su denominador.",
        "Paso 2: Recuerda la regla: ese denominador jamás puede tomar el valor cero.",
        "Paso 3: Esta regla prevalece incluso antes de intentar simplificar o resolver cualquier cosa."
    ],
    "ex_a": [
        ("Ejemplo 1", "Concepto: Si tenemos $\\frac{5}{x-3}$, ¿qué pasa si la variable 'x' vale 3?", ["Si $x = 3$, el denominador sería $3 - 3 = 0$.", "La fracción se convertiría en $\\frac{5}{0}$.", "Esto es matemáticamente imposible (indefinido)."])
    ],
    "ex_b": [
        ("Si el denominador es 'a', ¿qué valor está prohibido para 'a'?", "El cero", ["'a' no puede ser 0, porque dividiríamos por 0."])
    ],
    "errs": [
        "Creer que dividir por cero da cero.",
        "Creer que dividir por cero da infinito en álgebra básica (en cálculo diferencial se analiza el límite, pero en álgebra estática está simplemente indefinido)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "En matemáticas, la división por cero:", "choices": ["A) Es siempre cero.", "B) Da como resultado 1.", "C) Es igual al numerador.", "D) No está definida."], "ans": "D) No está definida.", "sol": "No existe ningún número que multiplicado por cero dé un número distinto de cero."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si el numerador de una fracción es cero, la fracción entera no está definida?", "ans": "Falso", "sol": "Si el numerador es 0 (y el denominador no lo es), la fracción vale 0. Lo que está prohibido es que el DENOMINADOR sea 0."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Dada la expresión $\\frac{0}{x+5}$, si $x=2$, ¿cuál es su valor?", "choices": ["A) Indefinido", "B) 0", "C) 7", "D) 1"], "ans": "B) 0", "sol": "Numerador es 0, denominador es 2+5=7. 0/7 = 0. Completamente legal."}
    ]
})

# 3. RESTRICCIONES_DOMINIO
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_BASE.RESTRICCIONES_DOMINIO",
    "title": "Restricciones y Dominio de una Fracción",
    "obj": "Calcular los valores numéricos que la variable no puede tomar para evitar que el denominador sea cero.",
    "intro": "Debido a la regla de oro (no dividirás por cero), cada vez que te entreguen una fracción algebraica debes ponerle una etiqueta de advertencia indicando qué valores son 'tóxicos' para ella. A esto le llamamos restricciones.",
    "res": "Para encontrar las restricciones de una fracción, se toma el denominador, se iguala a cero, y se resuelve la ecuación resultante. Los valores obtenidos son los que la variable NO puede tomar.",
    "expl": "Encuentra las restricciones de $\\frac{x+4}{x^2 - 25}$.\n\n1. **Aisla el denominador:** Ignora el numerador. Solo nos importa el fondo: $x^2 - 25$.\n2. **Iguala a cero:** Queremos saber cuándo esta bomba explota. $x^2 - 25 = 0$.\n3. **Resuelve:**\n   - Factorizamos: $(x-5)(x+5) = 0$.\n   - Soluciones: $x = 5$ y $x = -5$.\n\nEsto significa que si 'x' toma el valor 5 o el valor -5, el denominador se hace cero.\nPor lo tanto, las restricciones son: $x \\neq 5$ y $x \\neq -5$.\nEl \"Dominio\" es el conjunto de todos los números reales excepto esos valores prohibidos.",
    "proc": [
        "Paso 1: Ignora completamente el numerador.",
        "Paso 2: Toma la expresión del denominador y plantéala igual a cero ($Denominador = 0$).",
        "Paso 3: Resuelve la ecuación (generalmente requerirá factorizar si es cuadrática).",
        "Paso 4: Los números resultantes son las restricciones ($variable \\neq número$)."
    ],
    "ex_a": [
        ("Ejemplo 1", "Determina las restricciones de $\\frac{x+1}{2x - 8}$.", ["Tomamos el denominador: $2x - 8$.", "Lo igualamos a cero: $2x - 8 = 0$.", "Resolvemos: $2x = 8 \\rightarrow x = 4$.", "La restricción es $x \\neq 4$."])
    ],
    "ex_b": [
        ("¿Qué valores no puede tomar 'y' en $\\frac{3}{y(y-2)}$?", "0 y 2", ["Igualamos el denominador a cero: y(y-2) = 0. Esto se cumple si y=0 o si y=2."])
    ],
    "errs": [
        "Calcular las restricciones usando el numerador en lugar del denominador.",
        "Si el denominador es una letra sola ($x$), pensar que no hay restricciones (la restricción es $x \\neq 0$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Qué representa el 'dominio' en el contexto de una fracción algebraica?", "choices": ["A) Los valores que hacen que el numerador sea cero.", "B) Todos los números reales permitidos, excluyendo aquellos que hacen cero al denominador.", "C) El grado máximo del polinomio.", "D) Los valores que dan como resultado una fracción negativa."], "ans": "B) Todos los números reales permitidos, excluyendo aquellos que hacen cero al denominador.", "sol": "El dominio es el conjunto de valores \"seguros\" o permitidos para la variable."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Encuentra las restricciones para la fracción $\\frac{5a}{a^2 + 9}$.", "choices": ["A) $a \\neq 3, a \\neq -3$", "B) $a \\neq 0$", "C) $a \\neq -9$", "D) No tiene restricciones en los números reales."], "ans": "D) No tiene restricciones en los números reales.", "sol": "a^2 + 9 nunca puede ser cero con números reales (un cuadrado siempre es positivo o cero, más 9 es siempre positivo)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Para modelar la transferencia de calor, se usa la expresión $H(t) = \\frac{t^2 - 1}{t^2 - 7t + 10}$. ¿Para qué valores de tiempo $t$ el modelo matemático deja de estar definido?", "choices": ["A) $t=1$ y $t=-1$", "B) $t=2$ y $t=5$", "C) $t=-2$ y $t=-5$", "D) Solo para $t=0$"], "ans": "B) $t=2$ y $t=5$", "sol": "Denominador: t^2 - 7t + 10 = 0 -> (t-2)(t-5) = 0 -> t=2, t=5. (Los valores del numerador no importan)."}
    ]
})

# 4. SIGNO_FRACCION
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_BASE.SIGNO_FRACCION",
    "title": "El Signo de la Fracción (Global)",
    "obj": "Comprender la regla de los signos aplicada a la estructura general de una fracción.",
    "intro": "Una fracción tiene tres lugares donde puede llevar un signo negativo: arriba (numerador), abajo (denominador) o justo al frente (el signo de la fracción). ¿Cómo interactúan entre ellos? Con la vieja y confiable regla de los signos de la multiplicación.",
    "res": "Toda fracción tiene tres signos (numerador, denominador y el de la fracción misma). Cambiar exactamente DOS de estos signos al mismo tiempo NO altera el valor de la fracción.",
    "expl": "Piensa en el número $-\\frac{6}{2}$. Esto es igual a -3.\n¿Dónde más puedo poner ese negativo?\n- $\\frac{-6}{2} = -3$.\n- $\\frac{6}{-2} = -3$.\n\nLas tres formas son idénticas: $-\\frac{a}{b} = \\frac{-a}{b} = \\frac{a}{-b}$.\n\n¿Qué pasa si cambio DOS signos simultáneamente?\nSi tengo $\\frac{a}{b}$, y le cambio el signo al numerador y al denominador:\n$\\frac{-a}{-b}$. Por regla de signos, negativo dividido por negativo es positivo. Vuelve a ser $\\frac{a}{b}$.\nCambiar dos signos se anula a sí mismo. Cambiar uno solo invierte el valor de toda la fracción.",
    "proc": [
        "Paso 1: Identifica el signo global de la fracción (frente a la línea fraccionaria).",
        "Paso 2: Identifica el signo del numerador y el del denominador.",
        "Paso 3: Para que la fracción siga valiendo lo mismo, solo puedes multiplicar por -1 (cambiar el signo) a DOS de esos tres elementos simultáneamente."
    ],
    "ex_a": [
        ("Ejemplo 1", "Muestra dos formas alternativas de escribir $-\\frac{x}{y}$.", ["Cambiamos el global y el de arriba: $\\frac{-x}{y}$.", "Cambiamos el global y el de abajo: $\\frac{x}{-y}$.", "Ambas son completamente válidas."])
    ],
    "ex_b": [
        ("¿Es $-\\frac{-a}{-b}$ igual a $\\frac{a}{b}$ o a $-\\frac{a}{b}$?", "$-\\frac{a}{b}$", ["Tres signos negativos: dos de ellos se cancelan (- / - = +), pero queda el tercero flotando al frente, así que es negativo."])
    ],
    "errs": [
        "Creer que $-\\frac{x}{y}$ es lo mismo que $\\frac{-x}{-y}$ (en el primero hay un solo negativo, en el segundo hay dos que se vuelven positivo).",
        "Poner el signo negativo al numerador y además dejarlo al frente de la fracción doblemente."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Si en la fracción $\\frac{x}{y}$ cambiamos el signo del numerador y del denominador simultáneamente, obtenemos:", "choices": ["A) $-\\frac{x}{y}$", "B) $\\frac{-x}{-y}$ que equivale a $\\frac{x}{y}$", "C) $\\frac{y}{x}$", "D) 1"], "ans": "B) $\\frac{-x}{-y}$ que equivale a $\\frac{x}{y}$", "sol": "Menos entre menos da más, por lo que el valor global no se altera."},
        {"group": "reconocimiento", "diff": "media", "prompt": "De las siguientes expresiones, ¿cuál NO es equivalente a $-\\frac{m}{n}$?", "choices": ["A) $\\frac{-m}{n}$", "B) $\\frac{m}{-n}$", "C) $\\frac{-m}{-n}$", "D) $-(\\frac{m}{n})$"], "ans": "C) $\\frac{-m}{-n}$", "sol": "La opción C equivale a + m/n, lo cual es distinto al valor original negativo."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El signo que se coloca exactamente a la misma altura de la línea de la fracción afecta a todo el resultado de la fracción?", "ans": "Verdadero", "sol": "Sí, el signo global al frente invierte el valor de todo el cociente."}
    ]
})

# 5. SIGNO_NUMERADOR
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_BASE.SIGNO_NUMERADOR",
    "title": "Cambio de Signos en el Numerador",
    "obj": "Saber cómo aplicar un signo negativo externo a un polinomio que está en el numerador.",
    "intro": "Cuando mueves el signo negativo desde el frente de la fracción hacia el numerador (la parte superior), debes tener mucho cuidado si arriba hay un polinomio. Ese signo es un multiplicador silencioso para TODO el techo de la casa.",
    "res": "Si introduces un signo negativo al numerador, o lo pasas del frente al numerador, debes cambiarle el signo a TODOS y CADA UNO de los términos del polinomio superior.",
    "expl": "Mira esta fracción: $-\\frac{x - 5}{x + 2}$.\nQueremos meter ese signo negativo al numerador. Piensa que el numerador tiene un paréntesis invisible: $-(x - 5)$.\n\nAl aplicar el negativo adentro, se distribuye:\n- El 'x' positivo se vuelve '-x'.\n- El '-5' negativo se vuelve '+5'.\n\nPor lo tanto: $-\\frac{x - 5}{x + 2} = \\frac{-x + 5}{x + 2} = \\frac{5 - x}{x + 2}$.\n\nEl error garrafal que muchos cometen es cambiarle el signo solo a la primera letra y olvidarse del resto (ej. escribir $\\frac{-x - 5}{x+2}$), lo cual es incorrecto.",
    "proc": [
        "Paso 1: Imagina que todo el polinomio del numerador está entre paréntesis.",
        "Paso 2: Si le vas a aplicar un cambio de signo, distribuye el signo menos en el paréntesis.",
        "Paso 3: Cambia el signo de TODOS los términos del numerador sin excepción."
    ],
    "ex_a": [
        ("Ejemplo 1", "Convierte $-\\frac{2a - b + c}{5}$ moviendo el signo al numerador.", ["El negativo afecta a todo el techo: $-(2a - b + c)$.", "Distribuimos: $-2a + b - c$.", "El resultado es $\\frac{-2a + b - c}{5}$."])
    ],
    "ex_b": [
        ("¿A qué es equivalente $-\\frac{x+y}{z}$?", "$\\frac{-x-y}{z}$", ["El negativo afecta a la 'x' y a la 'y' a la vez."])
    ],
    "errs": [
        "Cambiar el signo solo al primer término del polinomio superior (el famoso error del francotirador miope).",
        "Distribuir el signo negativo tanto al numerador COMO al denominador simultáneamente (eso altera el valor de la fracción)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Al pasar el signo negativo global hacia el numerador, este signo debe:", "choices": ["A) Afectar solo a la primera variable.", "B) Afectar a todos los términos del numerador por propiedad distributiva.", "C) Eliminar el denominador.", "D) Quedar flotando."], "ans": "B) Afectar a todos los términos del numerador por propiedad distributiva.", "sol": "El numerador completo está agrupado, el signo global lo afecta todo."},
        {"group": "reconocimiento", "diff": "media", "prompt": "La expresión $-\\frac{a - b}{c}$ es estrictamente igual a:", "choices": ["A) $\\frac{-a - b}{c}$", "B) $\\frac{a + b}{c}$", "C) $\\frac{b - a}{c}$", "D) $\\frac{a - b}{-c}$"], "ans": "C) $\\frac{b - a}{c}$", "sol": "-(a - b) = -a + b, que reordenado es b - a."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si meto el signo negativo de la fracción hacia adentro, debo cambiar el signo tanto de los términos de arriba como de los de abajo?", "ans": "Falso", "sol": "Si cambias ambos a la vez, no estás metiendo el negativo global, estás multiplicando por (-1)/(-1)=+1, lo que destruye el negativo global que intentabas meter."}
    ]
})

# 6. SIGNO_DENOMINADOR
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_BASE.SIGNO_DENOMINADOR",
    "title": "Cambio de Signos en el Denominador",
    "obj": "Saber cómo aplicar un signo negativo externo a un polinomio que está en el denominador.",
    "intro": "Al igual que con el piso de arriba, podemos inyectar un signo negativo en el subsuelo (el denominador). El mecanismo es exactamente el mismo, y es un truco fantástico para arreglar denominadores 'al revés'.",
    "res": "Si aplicas un cambio de signo al denominador (por ejemplo, pasando el signo global hacia abajo), debes cambiarle el signo a TODOS los términos del polinomio del denominador.",
    "expl": "Tenemos $-\\frac{10}{3 - x}$.\nEl numerador nos gusta así (positivo 10), pero el denominador está un poco incómodo ('3 - x').\nUsemos el signo global para arreglar el denominador:\nMetemos el signo negativo abajo: $-(3 - x)$.\n\nDistribuimos el negativo a todos los miembros de abajo:\nEl '3' positivo se vuelve '-3'.\nEl '-x' negativo se vuelve '+x'.\n\nEl denominador quedó: $-3 + x$, que se ve más bonito ordenado como $x - 3$.\nNuestra fracción final es $\\frac{10}{x - 3}$.\n¡Hemos usado el signo negativo para 'darle la vuelta' a una resta en el denominador!",
    "proc": [
        "Paso 1: Para mover el signo al denominador, agrupa el denominador entre paréntesis.",
        "Paso 2: Multiplica todo el paréntesis por el signo negativo.",
        "Paso 3: Cambia de signo a TODOS los términos. Las restas invertidas ($b-a$) se volverán rectas ($a-b$)."
    ],
    "ex_a": [
        ("Ejemplo 1", "Mueve el negativo global de $-\\frac{x^2}{4 - y}$ hacia el denominador.", ["El signo va hacia abajo: $-(4 - y)$.", "Distribuimos: $-4 + y$.", "Reordenamos: $y - 4$.", "Resultado: $\\frac{x^2}{y - 4}$."])
    ],
    "ex_b": [
        ("¿Cómo escribir $\\frac{5}{-(x+2)}$ sin el paréntesis?", "$\\frac{5}{-x-2}$", ["El negativo afecta a la x y al 2."])
    ],
    "errs": [
        "Cambiar el signo solo al primer término del denominador.",
        "Creer que al darle vuelta a un polinomio sumado ($x+3$ a $3+x$) se necesita un negativo. (La suma es conmutativa, la resta no)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Si distribuimos un signo negativo hacia el polinomio del denominador:", "choices": ["A) Solo el término mayor cambia.", "B) Todos los términos del denominador cambian su signo.", "C) Se invierte la fracción.", "D) El numerador también cambia."], "ans": "B) Todos los términos del denominador cambian su signo.", "sol": "El signo afecta a toda la expresión como bloque."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál de las siguientes es equivalente a $\\frac{5}{- (a - b)}$?", "choices": ["A) $\\frac{5}{a - b}$", "B) $\\frac{5}{-a - b}$", "C) $\\frac{5}{b - a}$", "D) $-\\frac{5}{b - a}$"], "ans": "C) $\\frac{5}{b - a}$", "sol": "-(a - b) = -a + b = b - a. Así que el denominador es (b - a)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Podemos cambiar libremente $-\\frac{x}{a-b}$ a $\\frac{x}{b-a}$?", "ans": "Verdadero", "sol": "Sí, exactamente. Metimos el signo negativo al denominador, lo que invirtió los signos de 'a' y '-b'."}
    ]
})

# 7. FACTORES_OPUESTOS
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_BASE.FACTORES_OPUESTOS",
    "title": "Simplificación de Binomios Opuestos (x-y) / (y-x)",
    "obj": "Reconocer y simplificar la estructura clásica de la división de polinomios opuestos que resulta en -1.",
    "intro": "¿Qué pasa si intentas simplificar dos expresiones que son idénticas, pero donde alguien las escribió exactamente al revés? En las restas algebraicas esto sucede todo el tiempo.",
    "res": "Cualquier binomio dividido por su exacto opuesto invertido matemáticamente, de la forma $\\frac{a-b}{b-a}$, siempre da como resultado $-1$ (siempre que $a \\neq b$).",
    "expl": "Queremos simplificar $\\frac{x-5}{5-x}$.\nA primera vista, no son iguales. Arriba la 'x' es positiva, abajo es negativa. Arriba el 5 es negativo, abajo es positivo.\n¡Tienen los signos exactamente opuestos!\n\n¿Cómo lo resolvemos usando las reglas que aprendimos?\nSaquemos un 'factor común' de -1 en el numerador:\n$x - 5 = -1(-x + 5) = -(5 - x)$.\n\nSi reemplazamos esto en nuestra fracción:\n$\\frac{-(5 - x)}{5 - x}$.\nAhora el paréntesis $(5 - x)$ es idéntico arriba y abajo. Lo cancelamos.\n¿Qué sobrevivió? El signo negativo del frente (el -1).\n\nConclusión directa: Cuando veas una resta dividida por la misma resta al revés, bórralas de inmediato y escribe un `-1` gigante.",
    "proc": [
        "Paso 1: Revisa si el polinomio de arriba tiene EXACTAMENTE los mismos términos que el de abajo, pero con todos los signos invertidos.",
        "Paso 2: Esta situación es muy común en restas invertidas como $(a-b)$ y $(b-a)$.",
        "Paso 3: Cancela todo el bloque de arriba con todo el de abajo y reemplázalos por un $-1$."
    ],
    "ex_a": [
        ("Ejemplo 1", "Simplifica $\\frac{3m - 2n}{2n - 3m}$.", ["La 'm' arriba es $+3$, abajo es $-3$.", "La 'n' arriba es $-2$, abajo es $+2$.", "Son opuestos perfectos.", "Cancelamos y el resultado es $-1$."])
    ],
    "ex_b": [
        ("Simplifica $\\frac{x+y}{y+x}$.", "1", ["¡Cuidado! Son sumas, y la suma es conmutativa. $x+y$ es exactamente igual a $y+x$, no son opuestos. El resultado es 1."])
    ],
    "errs": [
        "Creer que $\\frac{a-b}{b-a} = 1$ (ignorar los signos).",
        "Confundir la suma con la resta (creer que $\\frac{a+b}{b+a} = -1$).",
        "Tachar un $(a-b)$ con un $(a+b)$ que no son opuestos, sino diferentes."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Cuál es la justificación matemática de que $\\frac{x-y}{y-x} = -1$?", "choices": ["A) Porque las variables se anulan a cero y queda un uno.", "B) Porque al factorizar un -1 en el numerador o denominador, los binomios se vuelven idénticos.", "C) Es un axioma indemostrable.", "D) Porque los exponentes se restan."], "ans": "B) Porque al factorizar un -1 en el numerador o denominador, los binomios se vuelven idénticos.", "sol": "(x-y) = -(-x+y) = -(y-x). Al dividir por (y-x), queda el -1."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Simplifica la fracción $\\frac{p^2 - q}{q - p^2}$.", "choices": ["A) $1$", "B) $-1$", "C) $0$", "D) No se puede simplificar"], "ans": "B) $-1$", "sol": "Son exactamente opuestos en signos término a término."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Una expresión de eficiencia devuelve la relación $\\frac{3x - 12}{4 - x}$. Si simplificas esto a su mínima expresión entera (asumiendo $x \\neq 4$), ¿qué obtienes?", "choices": ["A) $3$", "B) $-3$", "C) $-\\frac{3}{4}$", "D) $12$"], "ans": "B) $-3$", "sol": "Factor común 3 arriba: 3(x-4) / (4-x). El (x-4)/(4-x) da -1. Por lo tanto 3 * -1 = -3."}
    ]
})

# 8. SIMPLIFICACION_MONOMIOS
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_BASE.SIMPLIFICACION_MONOMIOS",
    "title": "Simplificación de Fracciones de Monomios",
    "obj": "Aplicar las leyes de los exponentes y simplificación de fracciones numéricas a un monomio dividido por otro.",
    "intro": "La simplificación es el arte de hacer las cosas más pequeñas y elegantes. Si tienes una fracción donde arriba y abajo hay un único bloque multiplicado (un monomio), todo es fiesta: solo divides números con números y restas letras con letras.",
    "res": "Para simplificar la fracción de dos monomios, simplifica los coeficientes numéricos como una fracción normal, y para las letras usa la regla de los exponentes (resta el exponente de abajo al de arriba).",
    "expl": "Queremos simplificar $\\frac{15x^5 y^2}{20x^2 y^6}$.\n\n1. **Parte numérica:**\n   $\\frac{15}{20}$. Ambos son divisibles por 5.\n   Queda $\\frac{3}{4}$.\n\n2. **Las letras 'x':**\n   Tenemos $\\frac{x^5}{x^2}$. Restamos exponentes (arriba manda): $5 - 2 = 3$.\n   Queda $x^3$ arriba.\n\n3. **Las letras 'y':**\n   Tenemos $\\frac{y^2}{y^6}$. Restamos exponentes: $2 - 6 = -4$.\n   $y^{-4}$ significa que la 'y' quedó abajo con exponente positivo 4. (O de forma más simple: había 2 y griegas arriba y 6 abajo. Se cancelan 2 de cada lado y quedan 4 vivas abajo).\n   Queda $y^4$ abajo.\n\n4. **Ensamblaje final:**\n   Juntamos todo: $\\frac{3x^3}{4y^4}$.\n\n¡Eso es todo! Todo lo que sea puramente multiplicativo se puede desarmar y cancelar.",
    "proc": [
        "Paso 1: Trata la parte de los números grandes (coeficientes) como una fracción de escuela primaria y redúcela al máximo.",
        "Paso 2: Por cada letra repetida arriba y abajo, cancela exponentes.",
        "Paso 3: El sobrante de letras queda en el lado (numerador o denominador) donde había un exponente mayor.",
        "Paso 4: Vuelve a armar la fracción final."
    ],
    "ex_a": [
        ("Ejemplo 1", "Simplifica $\\frac{12a^4 b}{8a b^3}$.", ["Números: $\\frac{12}{8} \\rightarrow \\frac{3}{2}$.", "Letra 'a': $\\frac{a^4}{a} \\rightarrow a^3$ arriba.", "Letra 'b': $\\frac{b}{b^3} \\rightarrow b^2$ abajo.", "Resultado: $\\frac{3a^3}{2b^2}$."])
    ],
    "ex_b": [
        ("Simplifica $\\frac{-5x y}{15x y}$.", "$-\\frac{1}{3}$", ["Números: -5/15 = -1/3. Las variables x e y se cancelan por completo porque son idénticas en cantidad."])
    ],
    "errs": [
        "Intentar aplicar esta regla cuando hay SUMAS o RESTAS en el numerador o denominador.",
        "Equivocarse al restar y poner el resultado en el numerador aunque el exponente mayor estaba abajo (ej. $\\frac{x^2}{x^5} \\rightarrow x^3$ arriba, fatal, es abajo)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué propiedad matemática permite cancelar directamente exponentes al simplificar fracciones de monomios?", "choices": ["A) La división de potencias de igual base.", "B) La distributividad de la multiplicación.", "C) La factorización de trinomios.", "D) El teorema de Pitágoras."], "ans": "A) La división de potencias de igual base.", "sol": "x^A / x^B = x^(A-B). Es la base del manejo de exponentes."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Simplifica $\\frac{24 m^2 n^5}{18 m^4 n^2}$.", "choices": ["A) $\\frac{4n^3}{3m^2}$", "B) $\\frac{4m^2}{3n^3}$", "C) $\\frac{6n^3}{m^2}$", "D) $\\frac{4n^7}{3m^6}$"], "ans": "A) $\\frac{4n^3}{3m^2}$", "sol": "24/18 = 4/3. n^5/n^2 = n^3 (arriba). m^2/m^4 = m^2 (abajo)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si simplifico $\\frac{x^3}{x^3}$, el resultado es 0 y la variable desaparece de la ecuación?", "ans": "Falso", "sol": "El resultado es 1, no 0. Las letras se cancelan, pero dejan un 1 matemático detrás."}
    ]
})

# 9. SIMPLIFICACION_FACTORIZACION
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_BASE.SIMPLIFICACION_FACTORIZACION",
    "title": "Simplificación con Polinomios (Factorizar primero)",
    "obj": "Aprender a simplificar fracciones que contienen sumas o restas mediante la factorización previa.",
    "intro": "Aquí es donde los estudiantes novatos caen como moscas. Tachan cosas que no deberían tachar. Existe una regla inquebrantable en las fracciones algebraicas: NUNCA puedes tachar términos que se estén sumando o restando.",
    "res": "Para simplificar una fracción con polinomios, primero DEBES FACTORIZAR completamente tanto el numerador como el denominador. Solo se pueden simplificar (tachar) factores completos (paréntesis multiplicativos) que sean idénticos.",
    "expl": "El peor error del álgebra es ver esto: $\\frac{x^2 + 5x}{x^2}$ y decir '¡Tacho la x cuadrada arriba y abajo!'. ¡ERROR GIGANTE!\nLa 'x' arriba se está sumando, no está sola.\n\n¿Cómo se hace bien?\n$\\frac{x^2 + 5x}{x^2}$\n\n1. **FACTORIZAR TODO:**\n   - Arriba (Factor común 'x'): $x(x + 5)$.\n   - Abajo (Ya es monomio): $x \\cdot x$.\n\nNuestra fracción ahora es: $\\frac{x(x + 5)}{x \\cdot x}$.\n\n2. **SIMPLIFICAR FACTORES:**\n   - Ahora sí tenemos puras multiplicaciones conectando los grandes bloques.\n   - Hay una 'x' multiplicando sola arriba, y dos 'x' solas abajo.\n   - Tachamos una 'x' de arriba con una 'x' de abajo.\n\n3. **Resultado:**\n   $\\frac{x + 5}{x}$.\n   \n(Y no, no puedes tachar la 'x' final que quedó).",
    "proc": [
        "Paso 1: Ignora tu instinto de tachar letras sueltas a simple vista.",
        "Paso 2: Factoriza el numerador lo máximo que puedas.",
        "Paso 3: Factoriza el denominador lo máximo que puedas.",
        "Paso 4: Busca paréntesis (o monomios sueltos) enteros que sean idénticos arriba y abajo, y cancélelos."
    ],
    "ex_a": [
        ("Ejemplo 1", "Simplifica $\\frac{a^2 - b^2}{a+b}$.", ["1. No puedes tachar 'a' con 'a'.", "2. Factoriza arriba (Diferencia de cuadrados): $(a+b)(a-b)$.", "3. Abajo ya es irreducible: $(a+b)$.", "4. Fracción: $\\frac{(a+b)(a-b)}{(a+b)}$.", "5. Cancela el bloque entero $(a+b)$. Resultado: $a-b$."])
    ],
    "ex_b": [
        ("Simplifica $\\frac{x^2-3x}{x-3}$.", "$x$", ["Arriba factor común: x(x-3). Abajo: (x-3). Se cancela (x-3) completo."])
    ],
    "errs": [
        "Tachar un sumando (ej. en $(x+4)/4$, tachar los cuatros).",
        "Tachar partes internas de un paréntesis."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Por qué es matemáticamente incorrecto simplificar los números '4' en la expresión $\\frac{x+4}{4}$?", "choices": ["A) Porque el 4 de arriba no es múltiplo de x.", "B) Porque en una fracción solo se pueden cancelar factores que estén multiplicando a TODO el numerador y denominador.", "C) Porque da x, y debería dar x+1.", "D) Porque no tienen exponentes."], "ans": "B) Porque en una fracción solo se pueden cancelar factores que estén multiplicando a TODO el numerador y denominador.", "sol": "El 4 en el numerador es un sumando, no un factor. (Como probar (2+4)/4 -> 6/4 = 1.5, pero si tacharas daría 2)."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Simplifica la fracción $\\frac{y^2 + 5y + 6}{y^2 - 4}$.", "choices": ["A) $\\frac{y+3}{y-2}$", "B) $\\frac{5y+6}{-4}$", "C) $\\frac{y+2}{y-2}$", "D) $\\frac{y+3}{y+2}$"], "ans": "A) $\\frac{y+3}{y-2}$", "sol": "Numerador: (y+3)(y+2). Denominador: (y-2)(y+2). Se cancela el factor (y+2)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "El área de un rectángulo está dada por $x^2 - x - 12$ y su base es $x - 4$. Al calcular su altura (área dividida por base) y simplificar, ¿qué expresión obtenemos para la altura?", "choices": ["A) $x+3$", "B) $x-3$", "C) $x+4$", "D) No se puede simplificar"], "ans": "A) $x+3$", "sol": "(x^2-x-12)/(x-4). Arriba se factoriza como (x-4)(x+3). Se cancela (x-4)."}
    ]
})

# 10. ERROR_RESTRICCIONES
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_BASE.ERROR_RESTRICCIONES",
    "title": "Las Restricciones Sobreviven a la Simplificación",
    "obj": "Comprender que las restricciones de dominio de una fracción deben calcularse ANTES de simplificarla.",
    "intro": "Un error muy común es simplificar una fracción algebraicamente y olvidarse de dónde venía. Cuando cancelas un factor del denominador, parece que el \"peligro\" ha desaparecido, ¡pero no es así para la función original!",
    "res": "Las restricciones del dominio (donde el denominador se hace cero) deben determinarse a partir de la expresión ORIGINAL, antes de cualquier simplificación o tachado de factores.",
    "expl": "Considera la fracción $\\frac{x^2 - 4}{x - 2}$.\nSi te pido las restricciones al principio, tomas el denominador original $x - 2 = 0$. La restricción es **$x \\neq 2$**.\n\nAhora la simplificamos:\n$\\frac{(x-2)(x+2)}{x-2}$.\nTachamos el bloque $(x-2)$ y nos queda simplemente la expresión plana: $x + 2$.\n\nSi miras solo \"$x + 2$\", dirías \"ah, no tiene denominador, no hay restricciones\".\n¡Grave error matemático! La expresión $x+2$ vino de la fracción original. La fracción original no sabe calcular el valor en $x=2$ (haría 0/0). Por tanto, aunque la versión simplificada luzca inofensiva, acarrea el \"fantasma\" de la restricción originaria.\n\nLa respuesta matemáticamente correcta es: La fracción se simplifica a $x+2$, pero sigue con la restricción $x \\neq 2$.",
    "proc": [
        "Paso 1: Toma la fracción exactamente como te la dieron en el problema inicial.",
        "Paso 2: Iguala el denominador inicial a cero y calcula sus raíces. ESAS son las restricciones eternas.",
        "Paso 3: Ahora sí, factoriza y simplifica.",
        "Paso 4: Presenta tu respuesta simplificada, pero anexando las restricciones que descubriste en el Paso 2."
    ],
    "ex_a": [
        ("Ejemplo 1", "Simplifica y da las restricciones de $\\frac{3x - 15}{x^2 - 5x}$.", ["1. Restricciones iniciales: Denom $x^2 - 5x = x(x-5) = 0$. Las restricciones son $x \\neq 0$ y $x \\neq 5$.", "2. Simplificamos: Arriba $3(x-5)$, abajo $x(x-5)$.", "3. Cancelamos $(x-5)$. Queda $\\frac{3}{x}$.", "4. Resultado final: $\\frac{3}{x}$, con restricciones $x \\neq 0$ y $x \\neq 5$."])
    ],
    "ex_b": [
        ("Simplifica $\\frac{x^2+x}{x+1}$", "$x$, para $x \\neq -1$", ["El factor (x+1) se cancela, pero la restricción de que x no puede ser -1 se mantiene viva."])
    ],
    "errs": [
        "Simplificar primero y luego buscar las restricciones en la fracción resultante (perdiendo restricciones en el camino).",
        "Considerar que $0/0$ da 1."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Por qué es obligatorio calcular las restricciones antes de simplificar una fracción algebraica?", "choices": ["A) Porque la simplificación hace que las fracciones desaparezcan.", "B) Porque cancelar un factor $(x-a)$ enmascara el hecho de que la función original no estaba definida para $x=a$.", "C) Para evitar sumar polinomios equivocados.", "D) Es solo una regla mnemotécnica sin base lógica."], "ans": "B) Porque cancelar un factor $(x-a)$ enmascara el hecho de que la función original no estaba definida para $x=a$.", "sol": "Es lo que en funciones se llama una 'discontinuidad evitable' o 'agujero', el punto sigue sin existir."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Simplifica la expresión $\\frac{a^3 - 4a}{a^2 + 2a}$ y determina TODAS sus restricciones reales.", "choices": ["A) Simplifica a $a-2$; restricción: $a \\neq -2$", "B) Simplifica a $a-2$; restricciones: $a \\neq 0, a \\neq -2$", "C) Simplifica a $a+2$; restricciones: $a \\neq 0, a \\neq -2$", "D) Simplifica a $a(a-2)$; restricciones: $a \\neq -2$"], "ans": "B) Simplifica a $a-2$; restricciones: $a \\neq 0, a \\neq -2$", "sol": "Denominador original: a(a+2). Restricciones: a=0, a=-2. Arriba: a(a-2)(a+2). Se cancelan a y (a+2), quedando (a-2)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si un problema te pide simplificar una fracción, puedes ignorar totalmente el denominador original y entregar solo la versión corta final?", "ans": "Falso", "sol": "Técnicamente, en rigor matemático, toda simplificación debe indicar su dominio de validez heredado."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-fracciones-banco-gen-2.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

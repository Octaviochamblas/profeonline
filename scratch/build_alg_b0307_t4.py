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
    filename = "docs/conocimiento/ejercicios/mat-alg-fracciones-banco-gen-4.jsonl"
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

# 1. SUMA IGUAL DENOMINADOR
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_SUMA.IGUAL_DENOMINADOR",
    "title": "Suma de Fracciones con Igual Denominador",
    "obj": "Sumar fracciones algebraicas que comparten el mismo denominador.",
    "intro": "El caso ideal al sumar fracciones es que los denominadores sean idénticos. Cuando esto pasa, el trabajo pesado ya está hecho.",
    "res": "Para sumar fracciones con igual denominador, mantén el denominador y suma los numeradores.",
    "expl": "Piensa en el denominador como el 'tipo' de objeto. Si sumas 3 manzanas y 2 manzanas, tienes 5 manzanas.\nSi sumas $\\frac{3}{x+1} + \\frac{2x}{x+1}$, el 'tipo' es el denominador $x+1$.\nSolo unes los numeradores en una misma fracción: $\\frac{3 + 2x}{x+1}$.",
    "proc": [
        "Paso 1: Confirma que los denominadores son exactamente iguales.",
        "Paso 2: Escribe una sola fracción usando ese denominador común.",
        "Paso 3: Coloca la suma de los numeradores en la parte superior."
    ],
    "ex_a": [
        ("Ejemplo 1", "Suma $\\frac{5a}{3b} + \\frac{2a}{3b}$.", ["El denominador es $3b$ para ambos.", "Sumamos numeradores: $5a + 2a = 7a$.", "Resultado: $\\frac{7a}{3b}$."])
    ],
    "ex_b": [
        ("Suma $\\frac{x^2}{x-2} + \\frac{4}{x-2}$.", "$\\frac{x^2+4}{x-2}$", ["Al tener el mismo denominador, solo se juntan los términos del numerador."])
    ],
    "errs": [
        "Sumar los denominadores (ej. decir que el nuevo denominador es el doble)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué pasa con los denominadores cuando se suman dos fracciones que ya tienen el mismo denominador?", "choices": ["A) Se suman entre sí.", "B) Se multiplican.", "C) Se mantiene el mismo denominador en el resultado.", "D) Se cancelan, dejando solo los numeradores."], "ans": "C) Se mantiene el mismo denominador en el resultado.", "sol": "El denominador indica en cuántas partes se divide el entero, no cambia al sumar más partes."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Calcula $\\frac{4m}{m^2+1} + \\frac{m}{m^2+1}$.", "choices": ["A) $\\frac{5m}{2m^2+2}$", "B) $\\frac{4m^2}{m^2+1}$", "C) $\\frac{5m}{m^2+1}$", "D) $5m$"], "ans": "C) $\\frac{5m}{m^2+1}$", "sol": "Denominador se mantiene. 4m + m = 5m."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si sumo $\\frac{x}{2} + \\frac{x}{2}$ el resultado es $\\frac{2x}{4}$?", "ans": "Falso", "sol": "El denominador se mantiene (2), por lo que es 2x/2, que luego se simplifica a x."}
    ]
})

# 2. SUMA DISTINTO DENOMINADOR
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_SUMA.DISTINTO_DENOMINADOR",
    "title": "Suma de Fracciones con Distinto Denominador",
    "obj": "Comprender la necesidad de unificar denominadores antes de sumar.",
    "intro": "Si intentas sumar peras con manzanas sin transformarlas a 'frutas' primero, tendrás un problema. Con fracciones de distinto denominador, no puedes sumar los techos hasta que no unifiques los pisos.",
    "res": "Nunca se pueden sumar fracciones con distintos denominadores directamente. Primero deben amplificarse para que compartan un denominador común.",
    "expl": "La suma $\\frac{2}{x} + \\frac{3}{y}$ no es $\\frac{5}{x+y}$ (este es el error más común y doloroso del álgebra).\nPara sumarlas, debemos encontrar un piso común (el MCM) y multiplicar arriba y abajo por lo que falte.",
    "proc": [
        "Paso 1: Identifica que los denominadores son diferentes.",
        "Paso 2: Encuentra un denominador común (idealmente el mínimo).",
        "Paso 3: Amplifica cada fracción para que tenga ese denominador común.",
        "Paso 4: Realiza la suma de los nuevos numeradores."
    ],
    "ex_a": [
        ("Ejemplo 1", "Concepto de $\\frac{a}{b} + \\frac{c}{d}$.", ["No se pueden sumar tal cual.", "Denominador común es $bd$.", "Amplificamos la primera por $d$: $\\frac{ad}{bd}$.", "Amplificamos la segunda por $b$: $\\frac{bc}{bd}$.", "Suma: $\\frac{ad+bc}{bd}$."])
    ],
    "ex_b": [
        ("¿Es correcto decir que $\\frac{1}{2} + \\frac{1}{x} = \\frac{2}{2+x}$?", "No", ["Sumar denominadores es un error conceptual grave."])
    ],
    "errs": [
        "Sumar los numeradores por un lado y los denominadores por otro lado."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Por qué es incorrecto sumar directamente los numeradores si los denominadores son diferentes?", "choices": ["A) Porque el numerador siempre debe ser mayor al denominador.", "B) Porque representan partes de tamaños diferentes que no se pueden contar juntas directamente.", "C) Es matemáticamente correcto pero no se acostumbra.", "D) Porque los signos pueden ser diferentes."], "ans": "B) Porque representan partes de tamaños diferentes que no se pueden contar juntas directamente.", "sol": "1/2 y 1/3 son pedazos de distinto tamaño. Necesitan un molde común (1/6)."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Calcula algebraicamente $\\frac{1}{x} + \\frac{1}{y}$.", "choices": ["A) $\\frac{2}{x+y}$", "B) $\\frac{x+y}{xy}$", "C) $\\frac{xy}{x+y}$", "D) $\\frac{2}{xy}$"], "ans": "B) $\\frac{x+y}{xy}$", "sol": "MCM es xy. La primera se amplifica por y (queda y/xy), la segunda por x (queda x/xy). Suma: (y+x)/xy."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Al buscar el denominador común entre dos fracciones que no tienen factores comunes, basta con multiplicar sus denominadores originales.", "ans": "Verdadero", "sol": "Sí, si no comparten factores (son primos entre sí), su mínimo común múltiplo es su producto directo."}
    ]
})

# 3. SUMA USO MCM
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_SUMA.USO_MCM",
    "title": "Uso del MCM en Sumas Algebraicas",
    "obj": "Utilizar el Mínimo Común Múltiplo para sumar fracciones de forma eficiente sin crear polinomios gigantes.",
    "intro": "Para igualar denominadores puedes simplemente multiplicar todos los denominadores viejos entre sí. ¡Pero eso puede crear un monstruo! El MCM te asegura usar el denominador común más pequeño posible.",
    "res": "El denominador común óptimo es el MCM de todos los denominadores originales, obtenido factorizándolos y tomando los factores únicos con su mayor exponente.",
    "expl": "Suma: $\\frac{1}{x^2} + \\frac{1}{x^3}$.\nSi multiplicas los denominadores (método de aspas), obtienes $x^5$.\nLa fracción quedaría $\\frac{x^3 + x^2}{x^5}$. (Gigante y requiere simplificar después).\n\nUsando el MCM:\nLos denominadores son $x^2$ y $x^3$. El factor común es $x$, el mayor exponente es $3$.\nMCM = $x^3$.\nAmplificamos solo la primera por $x$: $\\frac{x}{x^3}$. La segunda ya tiene el $x^3$.\nSuma: $\\frac{x+1}{x^3}$.\nEs más directo y el resultado ya está casi simplificado.",
    "proc": [
        "Paso 1: Factoriza los denominadores.",
        "Paso 2: Construye el MCM.",
        "Paso 3: Para cada fracción, multiplica su numerador por los factores del MCM que NO están en su denominador original.",
        "Paso 4: Pon la suma de esos nuevos numeradores sobre el MCM."
    ],
    "ex_a": [
        ("Ejemplo 1", "Suma $\\frac{2}{ab} + \\frac{3}{b^2}$.", ["MCM entre $ab$ y $b^2$ es $ab^2$.", "A la 1ra le falta 'b': numerador $2b$.", "A la 2da le falta 'a': numerador $3a$.", "Suma: $\\frac{2b + 3a}{ab^2}$."])
    ],
    "ex_b": [
        ("Suma $\\frac{1}{2x} + \\frac{1}{4x}$.", "$\\frac{3}{4x}$", ["MCM es 4x. A la primera le falta 2. 2/4x + 1/4x = 3/4x."])
    ],
    "errs": [
        "Usar el producto de todos los denominadores sin sacar MCM, resultando en polinomios difíciles de manejar.",
        "Multiplicar el numerador por todo el MCM en lugar de solo por el factor faltante."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Cuál es la principal ventaja de usar el MCM al sumar fracciones algebraicas?", "choices": ["A) Evita tener que amplificar las fracciones.", "B) Garantiza que no aparezcan signos negativos.", "C) Mantiene los polinomios del numerador final en su grado más bajo posible, facilitando el trabajo.", "D) Hace que la respuesta sea siempre 1."], "ans": "C) Mantiene los polinomios del numerador final en su grado más bajo posible, facilitando el trabajo.", "sol": "Evita crear fracciones gigantes 'infladas' que tendrías que simplificar laboriosamente al final."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Calcula usando MCM: $\\frac{1}{x(x-1)} + \\frac{1}{(x-1)(x+1)}$.", "choices": ["A) $\\frac{2}{x(x-1)(x+1)}$", "B) $\\frac{2x+1}{x(x-1)(x+1)}$", "C) $\\frac{x+1}{x(x-1)(x+1)}$", "D) $\\frac{2x+1}{x(x-1)^2(x+1)}$"], "ans": "B) $\\frac{2x+1}{x(x-1)(x+1)}$", "sol": "MCM: x(x-1)(x+1). A la primera le falta (x+1). A la segunda le falta 'x'. Numerador final: (x+1) + x = 2x+1."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "Para la suma $\\frac{1}{x^2} + \\frac{1}{xy}$, ¿el MCM de los denominadores es $x^3y$?", "ans": "Falso", "sol": "El MCM es x^2y. Tomamos cada factor (x e y) con su mayor exponente visible (2 para x, 1 para y)."}
    ]
})

# 4. REDUCCION NUMERADOR
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_SUMA.REDUCCION_NUMERADOR",
    "title": "Reducción de Términos en la Suma",
    "obj": "Agrupar y reducir los términos semejantes que aparecen en el numerador final tras la suma.",
    "intro": "Una vez que construyes ese gran numerador uniendo todo, a menudo parece un desorden. Tu deber es ordenarlo, agrupar las x con las x, los números con los números, y limpiar la casa.",
    "res": "Después de sumar los numeradores amplificados, siempre debes reducir términos semejantes (sumar y restar coeficientes de las mismas variables).",
    "expl": "Imagina que llegas a esto tras sumar:\n$\\frac{(3x - 5) + (2x + 1)}{x+1}$\n\nNo lo dejes así. Busca los semejantes en el numerador:\n- Las equis: $3x + 2x = 5x$.\n- Los números: $-5 + 1 = -4$.\n\nEl numerador limpio es $5x - 4$.\nEl resultado ordenado y final es $\\frac{5x - 4}{x+1}$.",
    "proc": [
        "Paso 1: Observa el numerador resultante gigante.",
        "Paso 2: Identifica los términos que tienen las mismas variables con los mismos exponentes (términos semejantes).",
        "Paso 3: Suma o resta sus coeficientes numéricos.",
        "Paso 4: Escribe el polinomio final reducido y ordenado."
    ],
    "ex_a": [
        ("Ejemplo 1", "Reduce el numerador de $\\frac{4x^2 + 3x - 1 + x^2 - 3x + 5}{x}$.", ["Términos con $x^2$: $4x^2 + x^2 = 5x^2$.", "Términos con $x$: $3x - 3x = 0$ (se anulan).", "Números: $-1 + 5 = 4$.", "Resultado final: $\\frac{5x^2 + 4}{x}$."])
    ],
    "ex_b": [
        ("Limpia $\\frac{a + 2b - a + b}{c}$.", "$\\frac{3b}{c}$", ["Las 'a' se cancelan (a - a = 0). Las 'b' se suman (2b + b = 3b)."])
    ],
    "errs": [
        "Sumar términos que no son semejantes (ej. $2x + 3 = 5x$).",
        "Olvidarse de incluir términos que no tienen pareja al transcribir el resultado."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Reducir términos semejantes en el numerador de una fracción significa:", "choices": ["A) Dividir todos los términos por un factor común.", "B) Agrupar y sumar los coeficientes de los términos que tienen exactamente las mismas variables y exponentes.", "C) Tachar términos que sean iguales al denominador.", "D) Ordenar de menor a mayor grado."], "ans": "B) Agrupar y sumar los coeficientes de los términos que tienen exactamente las mismas variables y exponentes.", "sol": "Es el proceso estándar de limpieza algebraica de sumas."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Después de amplificar y sumar, un estudiante obtiene la fracción $\\frac{2x^2 + 5x - 3x^2 + 4}{x-1}$. ¿Cuál es la forma reducida correcta?", "choices": ["A) $\\frac{5x^2 + 5x + 4}{x-1}$", "B) $\\frac{x^2 + 5x + 4}{x-1}$", "C) $\\frac{-x^2 + 5x + 4}{x-1}$", "D) $\\frac{4x^3 + 4}{x-1}$"], "ans": "C) $\\frac{-x^2 + 5x + 4}{x-1}$", "sol": "2x^2 - 3x^2 = -x^2. Los demás términos bajan igual."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si en el numerador tengo $3a + 4b$, puedo reducirlos a $7ab$?", "ans": "Falso", "sol": "No son semejantes. Uno es 'a' y otro es 'b', no se pueden fusionar mediante suma."}
    ]
})

# 5. SIMPLIFICACION FINAL SUMA
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_SUMA.SIMPLIFICACION_FINAL",
    "title": "Simplificación Final Tras Sumar",
    "obj": "Verificar si la fracción obtenida tras la suma se puede simplificar mediante factorización.",
    "intro": "¡No cantes victoria al sumar! A veces, el nuevo numerador que formaste tiene una sorpresa: se puede factorizar y cancelar mágicamente con el denominador.",
    "res": "Después de sumar y reducir el numerador, intenta factorizarlo. Si encuentras un factor idéntico al denominador, puedes simplificar la fracción final.",
    "expl": "Mira esta suma: $\\frac{x^2}{x-2} + \\frac{-4}{x-2}$.\n1. Igual denominador, unimos: $\\frac{x^2 - 4}{x-2}$.\n¿Terminamos? ¡Casi!\n\n2. Factoriza el numerador: El numerador $x^2 - 4$ es una diferencia de cuadrados, se factoriza como $(x-2)(x+2)$.\nLa fracción ahora es: $\\frac{(x-2)(x+2)}{x-2}$.\n\n3. ¡Tacha el $(x-2)$!\nResultado glorioso final: $x+2$.",
    "proc": [
        "Paso 1: Asegúrate de que el numerador final esté completamente reducido.",
        "Paso 2: Busca algún método para factorizar ese numerador (factor común, diferencia de cuadrados, trinomio).",
        "Paso 3: Si uno de los factores coincide con parte o la totalidad del denominador, cancélalos."
    ],
    "ex_a": [
        ("Ejemplo 1", "Suma y simplifica $\\frac{2x}{x+3} + \\frac{6}{x+3}$.", ["Suma: $\\frac{2x + 6}{x+3}$.", "Factoriza el numerador sacando factor común 2: $\\frac{2(x+3)}{x+3}$.", "Cancela el factor $(x+3)$ de arriba y abajo.", "Resultado final: $2$."])
    ],
    "ex_b": [
        ("Suma $\\frac{m^2}{m+1} + \\frac{m}{m+1}$.", "$m$", ["Suma m^2+m en el numerador. Factor común m: m(m+1). Se cancela el m+1 del denominador."])
    ],
    "errs": [
        "Terminar el ejercicio sin revisar si se podía factorizar el numerador.",
        "Tachar sumandos en lugar de factorizar (ej. en $\\frac{x^2+2}{2}$, tachar los 2)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "Para poder simplificar una fracción después de haber sumado sus partes, el paso intermedio absolutamente obligatorio es:", "choices": ["A) Multiplicar por -1.", "B) Voltear la fracción.", "C) Factorizar el polinomio resultante en el numerador.", "D) Restar los exponentes."], "ans": "C) Factorizar el polinomio resultante en el numerador.", "sol": "Sin factorizar, tendrás sumandos en el numerador que son ilegales de tachar directamente."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Calcula la suma $\\frac{x^2}{x-5} - \\frac{25}{x-5}$ y exprésala en su forma más simple (asumiendo $x \\neq 5$).", "choices": ["A) $x - 5$", "B) $x + 5$", "C) $x^2 - 5$", "D) $\\frac{x^2 - 25}{x-5}$"], "ans": "B) $x + 5$", "sol": "Numerador: x^2 - 25. Se factoriza a (x-5)(x+5). Denominador: (x-5). Se cancelan y queda x+5."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "Si tras sumar obtengo $\\frac{3x+5}{x}$, ¿puedo simplificar la 'x' del $3x$ con la 'x' de abajo?", "ans": "Falso", "sol": "No se puede. El 3x es un sumando (está atado al +5). Solo podrías si pudieras sacar 'x' como factor común de todo el numerador, lo cual aquí es imposible."}
    ]
})

# 6. RESTA IGUAL DENOMINADOR
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_RESTA.IGUAL_DENOMINADOR",
    "title": "Resta de Fracciones con Igual Denominador",
    "obj": "Restar fracciones algebraicas que comparten el mismo denominador.",
    "intro": "La resta es igual de sencilla que la suma cuando los pisos son idénticos. Pero la resta tiene veneno: el signo negativo.",
    "res": "Para restar fracciones con igual denominador, mantén el denominador y resta los numeradores. ¡Cuidado con el signo negativo que afecta al segundo numerador!",
    "expl": "Con igual denominador, agrupas rápido:\n$\\frac{5x}{2a} - \\frac{3x}{2a} = \\frac{5x - 3x}{2a} = \\frac{2x}{2a} = \\frac{x}{a}$.\n\nEl cuidado es cuando el numerador que restas tiene varios términos. El signo negativo actúa como un francotirador contra TODOS ellos.",
    "proc": [
        "Paso 1: Confirma denominadores iguales.",
        "Paso 2: Escribe la única fracción.",
        "Paso 3: Coloca el primer numerador, luego un signo MENOS, y luego el segundo numerador (¡preferiblemente entre paréntesis!)."
    ],
    "ex_a": [
        ("Ejemplo 1", "Resta $\\frac{9m}{4} - \\frac{2m}{4}$.", ["Denominador común: 4.", "Numeradores: $9m - 2m = 7m$.", "Resultado: $\\frac{7m}{4}$."])
    ],
    "ex_b": [
        ("Calcula $\\frac{y^2}{y-1} - \\frac{1}{y-1}$.", "$y+1$", ["Numerador es y^2-1. Se factoriza a (y-1)(y+1). Se cancela (y-1)."])
    ],
    "errs": [
        "Confundir las reglas y tratar de voltear alguna fracción (eso es para división)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Al restar dos fracciones algebraicas con el mismo denominador:", "choices": ["A) Los denominadores se restan y dan 0.", "B) El denominador se conserva intacto y los numeradores se restan.", "C) Se invierte la segunda fracción.", "D) Se multiplican los numeradores cruzados."], "ans": "B) El denominador se conserva intacto y los numeradores se restan.", "sol": "Es el mismo principio que la suma, el denominador es inmutable en este paso."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Calcula $\\frac{7a}{2} - \\frac{5a}{2}$.", "choices": ["A) $\\frac{2a}{0}$", "B) $a$", "C) $2a$", "D) $\\frac{12a}{2}$"], "ans": "B) $a$", "sol": "(7a - 5a)/2 = 2a/2 = a."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿La resta $\\frac{A}{C} - \\frac{B}{C}$ es equivalente a $\\frac{A-B}{C}$?", "ans": "Verdadero", "sol": "Sí, es la definición exacta de suma/resta homogénea."}
    ]
})

# 7. PARENTESIS_NUMERADOR
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_RESTA.PARENTESIS_NUMERADOR",
    "title": "El Peligro del Signo Menos (Paréntesis Vital)",
    "obj": "Distribuir correctamente el signo negativo al restar un polinomio completo.",
    "intro": "Aquí es donde mueren el 90% de los ejercicios de resta algebraica. El signo de resta que separa las fracciones NO ataca solo a la primera letra del numerador que le sigue, ¡ataca a TODA la casa!",
    "res": "Al restar una fracción cuyo numerador es un polinomio, debes colocar todo ese polinomio entre paréntesis precedido por el signo menos, lo cual cambiará el signo de TODOS sus términos.",
    "expl": "Considera: $\\frac{5x}{x+1} - \\frac{2x - 3}{x+1}$.\n\n**Forma Incorrecta (Muerte instantánea):**\n$\\frac{5x - 2x - 3}{x+1}$. (¡El -3 se quedó como negativo!).\n\n**Forma Correcta (Ninja):**\nUsa paréntesis para el segundo techo:\n$\\frac{5x - (2x - 3)}{x+1}$\nDistribuye el negativo. Entra matando:\n- El $2x$ positivo se vuelve $-2x$.\n- El $-3$ negativo se vuelve $+3$.\nQueda: $\\frac{5x - 2x + 3}{x+1}$.\nResultado: $\\frac{3x + 3}{x+1}$.",
    "proc": [
        "Paso 1: Escribe el denominador común.",
        "Paso 2: Escribe el primer numerador.",
        "Paso 3: Pon un signo menos y ABRE PARÉNTESIS.",
        "Paso 4: Escribe el segundo numerador dentro del paréntesis.",
        "Paso 5: En el siguiente renglón, quita el paréntesis cambiando TODOS los signos interiores."
    ],
    "ex_a": [
        ("Ejemplo 1", "Resta $\\frac{a + 4}{2} - \\frac{a - 2}{2}$.", ["Escribimos: $\\frac{a + 4 - (a - 2)}{2}$.", "Distribuimos el menos: $\\frac{a + 4 - a + 2}{2}$.", "Reducimos: las 'a' se van, $4+2=6$.", "Queda $\\frac{6}{2} = 3$."])
    ],
    "ex_b": [
        ("Calcula $\\frac{3x}{5} - \\frac{x+1}{5}$.", "$\\frac{2x-1}{5}$", ["El negativo afecta a la 'x' y al '1'. Queda 3x - x - 1 = 2x - 1."])
    ],
    "errs": [
        "El 'error del francotirador miope': restarle solo al primer término del segundo numerador y copiar el resto igual."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Por qué es crucial usar un paréntesis en el numerador al restar fracciones algebraicas polinómicas?", "choices": ["A) Por estética matemática.", "B) Porque el signo negativo de la resta debe distribuirse a TODOS los términos del segundo numerador.", "C) Para multiplicar los numeradores.", "D) Para evitar que se cancelen las variables."], "ans": "B) Porque el signo negativo de la resta debe distribuirse a TODOS los términos del segundo numerador.", "sol": "El signo de resta es para toda la fracción, lo que equivale a multiplicar el numerador entero por -1."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Calcula el resultado de $\\frac{4m-5}{m} - \\frac{m-5}{m}$.", "choices": ["A) $\\frac{3m-10}{m}$", "B) $\\frac{3m}{m}$ o $3$", "C) $\\frac{5m}{m}$", "D) $\\frac{3m-5}{m}$"], "ans": "B) $\\frac{3m}{m}$ o $3$", "sol": "(4m-5) - (m-5) = 4m - 5 - m + 5 = 3m. Al dividir por m, da 3."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "Si resto $\\frac{x}{3} - \\frac{-x+2}{3}$, el numerador final sin reducir se escribe como $x - (-x+2)$.", "ans": "Verdadero", "sol": "Correcto, y luego se distribuye el negativo quedando x + x - 2 = 2x - 2."}
    ]
})

# 8. RESTA DISTINTO DENOMINADOR
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_RESTA.DISTINTO_DENOMINADOR",
    "title": "Resta con Diferentes Denominadores",
    "obj": "Preparar y restar fracciones algebraicas que no comparten denominador.",
    "intro": "Al igual que con la suma, si los pisos son distintos, tienes prohibido restar. Debes nivelar el terreno amplificando las fracciones primero.",
    "res": "Para restar fracciones de distinto denominador, halla el común denominador, amplifica los numeradores (multiplicando por lo que faltaba al denominador original), y procede con la resta usando paréntesis.",
    "expl": "Problema: $\\frac{x}{y} - \\frac{2}{x}$.\n1. Los denominadores son $y$ y $x$. MCM es $xy$.\n2. Amplificamos:\n   - A $\\frac{x}{y}$ le falta la 'x' abajo. Multiplicamos por 'x' arriba: $x \\cdot x = x^2$.\n   - A $\\frac{2}{x}$ le falta la 'y' abajo. Multiplicamos por 'y' arriba: $2 \\cdot y = 2y$.\n3. Unimos con la resta en medio:\n   $\\frac{x^2 - 2y}{xy}$.\n¡Hecho!",
    "proc": [
        "Paso 1: Encuentra el denominador común.",
        "Paso 2: Amplifica el primer numerador.",
        "Paso 3: Amplifica el segundo numerador.",
        "Paso 4: Pon el signo menos entre ellos (si el segundo numerador tiene varios términos, ponlo entre paréntesis).",
        "Paso 5: Reduce y simplifica si es posible."
    ],
    "ex_a": [
        ("Ejemplo 1", "Resta $\\frac{3}{a} - \\frac{5}{b}$.", ["Común denominador: $ab$.", "Primer num: $3 \\cdot b = 3b$.", "Segundo num: $5 \\cdot a = 5a$.", "Resultado: $\\frac{3b - 5a}{ab}$."])
    ],
    "ex_b": [
        ("Calcula $1 - \\frac{1}{x}$.", "$\\frac{x-1}{x}$", ["El 1 es 1/1. MCM es x. Queda x/x - 1/x = (x-1)/x."])
    ],
    "errs": [
        "Restar los denominadores entre sí."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "El primer paso indispensable para restar $\\frac{A}{B} - \\frac{C}{D}$ cuando B y D son distintos es:", "choices": ["A) Restar A - C.", "B) Restar B - D.", "C) Encontrar un denominador común.", "D) Invertir C/D."], "ans": "C) Encontrar un denominador común.", "sol": "Sin común denominador, no se puede hacer la operación de resta."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Resuelve la resta $\\frac{4}{a} - \\frac{3}{a^2}$.", "choices": ["A) $\\frac{1}{a-a^2}$", "B) $\\frac{4a-3}{a^2}$", "C) $\\frac{4a^2-3a}{a^3}$", "D) $\\frac{1}{a^2}$"], "ans": "B) $\\frac{4a-3}{a^2}$", "sol": "MCM es a^2. A la primera le falta 'a', queda 4a. A la segunda no le falta nada, queda 3. (4a-3)/a^2."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Calcula algebraicamente la diferencia: $\\frac{x}{x-2} - \\frac{2}{x}$.", "choices": ["A) $\\frac{x^2 - 2x + 4}{x(x-2)}$", "B) $\\frac{x^2 - 2x - 4}{x(x-2)}$", "C) $\\frac{x-2}{x-2}$", "D) $\\frac{x^2 - 4}{x(x-2)}$"], "ans": "A) $\\frac{x^2 - 2x + 4}{x(x-2)}$", "sol": "MCM: x(x-2). Num1 amplificado: x * x = x^2. Num2 amplificado: 2 * (x-2) = 2x - 4. Resta: x^2 - (2x - 4) = x^2 - 2x + 4."}
    ]
})

# 9. RESTA USO MCM
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_RESTA.USO_MCM",
    "title": "Uso del MCM en Restas Algebraicas",
    "obj": "Aplicar el Mínimo Común Múltiplo para optimizar restas complejas.",
    "intro": "Al igual que en la suma, usar el MCM para el común denominador en las restas evita que los polinomios se hinchen innecesariamente.",
    "res": "El denominador común para la resta debe ser el MCM de los denominadores. Así la amplificación será mínima y se evitarán polinomios gigantes a reducir.",
    "expl": "Resta: $\\frac{1}{x^2-1} - \\frac{1}{x-1}$.\n\n1. **Denominadores factorizados:** $(x-1)(x+1)$ y $(x-1)$.\n2. **MCM:** Tomamos todo, sin repetir exponentes. Es $(x-1)(x+1)$.\n3. **Amplificación:**\n   - A la primera fracción no le falta nada. Su numerador sigue siendo 1.\n   - A la segunda fracción (con piso $x-1$) le falta el $(x+1)$. Su numerador se multiplica por eso: $1 \\cdot (x+1) = x+1$.\n4. **Restamos con cuidado (paréntesis!):**\n   $1 - (x+1) = 1 - x - 1 = -x$.\n5. **Resultado final:** $\\frac{-x}{(x-1)(x+1)}$.",
    "proc": [
        "Paso 1: Factoriza ambos denominadores para ver sus entrañas.",
        "Paso 2: Arma el súper denominador MCM (todos los factores distintos, exponente mayor).",
        "Paso 3: Amplifica los numeradores por los factores que les faltaban.",
        "Paso 4: Pon un menos y un gran paréntesis para el segundo bloque amplificado, y resuelve."
    ],
    "ex_a": [
        ("Ejemplo 1", "Resta $\\frac{3}{x(x-2)} - \\frac{2}{x^2(x-2)}$.", ["MCM: La x mayor es $x^2$. Incluimos $(x-2)$. MCM=$x^2(x-2)$.", "A la 1ra le falta una 'x'. Num = 3x.", "A la 2da no le falta nada. Num = 2.", "Resta: $\\frac{3x - 2}{x^2(x-2)}$."])
    ],
    "ex_b": [
        ("Halla el MCM de denominadores de $\\frac{5}{m^3 n} - \\frac{2}{m n^4}$.", "$m^3 n^4$", ["Mayores exponentes: m al cubo y n a la cuarta."])
    ],
    "errs": [
        "Tomar un denominador común simplemente multiplicando todo (por ejemplo, $(x-1)(x+1)(x-1)$), lo que complica enormemente la expresión."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "Al usar el MCM para restar fracciones, el objetivo de factorizar primero los denominadores es:", "choices": ["A) Simplificarlos con los numeradores.", "B) Identificar factores repetidos para no incluirlos múltiples veces en el denominador común.", "C) Eliminar el signo negativo.", "D) Invertir las fracciones."], "ans": "B) Identificar factores repetidos para no incluirlos múltiples veces en el denominador común.", "sol": "Esto mantiene el MCM lo más 'pequeño' posible."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Aplica MCM para resolver: $\\frac{5}{x^2} - \\frac{2}{x^3}$.", "choices": ["A) $\\frac{3}{x^3}$", "B) $\\frac{5x-2}{x^3}$", "C) $\\frac{5x^3-2x^2}{x^5}$", "D) $\\frac{3}{x^{-1}}$"], "ans": "B) $\\frac{5x-2}{x^3}$", "sol": "MCM es x^3. A la primera le falta x, queda 5x. A la segunda nada, queda 2. Resta: (5x-2)/x^3."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si los denominadores son $a(a+1)$ y $a^2$, el MCM será $a^2(a+1)$?", "ans": "Verdadero", "sol": "Tomamos 'a' con el mayor exponente (2) y el bloque factor (a+1)."}
    ]
})

# 10. CAMBIO SIGNOS NUMERADOR
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_RESTA.CAMBIO_SIGNOS_NUMERADOR",
    "title": "Cambio de Signos tras la Resta",
    "obj": "Ejecutar la eliminación de paréntesis tras una resta para simplificar el numerador.",
    "intro": "¡El trabajo no termina al plantear la resta con su paréntesis protector! Hay que abrir las puertas y dejar que el signo negativo haga su trabajo destructivo/constructivo.",
    "res": "Al quitar el paréntesis del segundo numerador en una resta, todos y cada uno de los términos dentro del paréntesis deben invertir su signo matemático.",
    "expl": "Pusiste el paréntesis: $\\frac{A - (B - C + D)}{E}$.\nAl limpiar, queda: $\\frac{A - B + C - D}{E}$.\n\nSi te enfrentas a una resta donde ya factorizaste, cuidado. El signo afecta a los coeficientes sueltos cuando multiplicas.\nEjemplo:\n$\\frac{3x - 2(x - 5)}{x^2}$.\nEse $-2$ se distribuye:\n$-2 \\cdot x = -2x$.\n$-2 \\cdot -5 = +10$.\nQueda: $\\frac{3x - 2x + 10}{x^2} = \\frac{x + 10}{x^2}$.",
    "proc": [
        "Paso 1: Observa el polinomio que está precedido por el signo menos (o por un número negativo).",
        "Paso 2: Reescribe el polinomio completo, cambiando los + por - y los - por +.",
        "Paso 3: Si había un número multiplicando (ej. $-4(x+2)$), distribuye el número con todo y su signo negativo."
    ],
    "ex_a": [
        ("Ejemplo 1", "Limpia el numerador: $5x - (3x^2 - 4x + 1)$.", ["El $3x^2$ sale como $-3x^2$.", "El $-4x$ sale como $+4x$.", "El $+1$ sale como $-1$.", "Resultado: $5x - 3x^2 + 4x - 1 = -3x^2 + 9x - 1$."])
    ],
    "ex_b": [
        ("Distribuye el menos en $- ( -2a - 3b )$.", "$2a + 3b$", ["Menos por menos da más en ambos casos."])
    ],
    "errs": [
        "Invertir el signo solo del primer término y copiar el resto igual (el error clásico)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Cuando tienes un signo de resta delante de un polinomio entre paréntesis, matemáticamente estás:", "choices": ["A) Restando solo el primer término.", "B) Multiplicando cada término del polinomio por -1.", "C) Dividiendo el polinomio entre 1.", "D) Elevando todo a -1."], "ans": "B) Multiplicando cada término del polinomio por -1.", "sol": "Es la definición de la distribución de un signo negativo."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Reduce el siguiente numerador: $2x^2 + 3 - (x^2 - 5x - 3)$.", "choices": ["A) $x^2 - 5x$", "B) $x^2 + 5x + 6$", "C) $3x^2 - 5x$", "D) $x^2 - 5x - 6$"], "ans": "B) $x^2 + 5x + 6$", "sol": "2x^2 + 3 - x^2 + 5x + 3. 2x^2 - x^2 = x^2. Las x son 5x. Los números son 3+3=6."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Al evaluar $7x - 3(x - 2)$, la distribución correcta da como resultado $7x - 3x - 6$.", "ans": "Falso", "sol": "Da 7x - 3x + 6. El (-3)*(-2) da positivo 6."}
    ]
})

# 11. ERROR PARENTESIS
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_RESTA.ERROR_PARENTESIS",
    "title": "Errores de Opresión (Falta de Paréntesis)",
    "obj": "Reconocer ejercicios que han sido desarrollados erróneamente por falta de paréntesis y corregirlos.",
    "intro": "Aprender del error ajeno es inteligencia. Revisaremos el error más destructivo de las fracciones algebraicas: cómo la omisión de un par de garabatos curvos () arruina todo el trabajo.",
    "res": "Omitir los paréntesis al colocar el segundo numerador detrás del signo de resta resultará inevitablemente en signos erróneos para todos los términos (excepto el primero) de ese polinomio.",
    "expl": "Un ejercicio resuelto por un estudiante desatento:\n$\\frac{4x}{x-1} - \\frac{x - 5}{x-1}$\nPaso del estudiante: $=\\frac{4x - x - 5}{x-1}$\nResultado del estudiante: $=\\frac{3x - 5}{x-1}$\n\n**¡TERRIBLE ERROR!**\nEl estudiante aplicó el menos de la resta SÓLO a la 'x'. El $-5$ bajó impunemente como $-5$.\n\nResolución correcta:\n$=\\frac{4x - (x - 5)}{x-1}$\n$=\\frac{4x - x + 5}{x-1}$ (¡El -5 se volvió +5!)\n$=\\frac{3x + 5}{x-1}$.\nUn simple + o - determina si apruebas o no.",
    "proc": [
        "Paso 1: Siempre asume que los numeradores con más de un término vienen empacados en un paréntesis invisible.",
        "Paso 2: Al pasarlos después de un signo menos, haz que el paréntesis sea visible.",
        "Paso 3: Recuerda la regla: 'El menos ataca a todos'."
    ],
    "ex_a": [
        ("Ejemplo 1", "Corrige el error: $\\frac{a}{2} - \\frac{a+b}{2} = \\frac{a - a + b}{2} = \\frac{b}{2}$.", ["Error: El signo no afectó a la 'b'.", "Correcto: $\\frac{a - (a+b)}{2} = \\frac{a - a - b}{2} = \\frac{-b}{2}$."])
    ],
    "ex_b": [
        ("Si un alumno dice que $\\frac{5}{x} - \\frac{y-2}{x} = \\frac{5-y-2}{x}$, ¿qué signo se equivocó?", "El -2 debería ser +2.", ["No distribuyó el negativo hacia el -2 original."])
    ],
    "errs": [
        "Confiar excesivamente en la memoria y hacer la distribución mentalmente fallando en los signos posteriores."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Por qué un polinomio en el numerador de una fracción que está restando se comporta como si tuviera un paréntesis invisible?", "choices": ["A) Porque la línea de la fracción actúa como un símbolo de agrupación para todo el numerador.", "B) Porque todos los polinomios llevan paréntesis en álgebra.", "C) Es una regla de formato.", "D) Porque los signos se cancelan."], "ans": "A) Porque la línea de la fracción actúa como un símbolo de agrupación para todo el numerador.", "sol": "La línea divisoria agrupa firmemente todo lo que está arriba. Al colocarlo en una línea con otros, ese bloque agrupado debe protegerse con paréntesis reales."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Identifica la expansión correcta de $\\frac{7x+2}{4} - \\frac{3x-8}{4}$.", "choices": ["A) $\\frac{7x+2 - 3x - 8}{4}$", "B) $\\frac{7x+2 - 3x + 8}{4}$", "C) $\\frac{7x+2 + 3x - 8}{4}$", "D) $\\frac{4x - 10}{4}$"], "ans": "B) $\\frac{7x+2 - 3x + 8}{4}$", "sol": "Al distribuir el menos en el segundo numerador (3x-8), queda -3x + 8."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "El \"error del francotirador miope\" consiste en cambiarle el signo solo al primer término del polinomio que se está restando.", "ans": "Verdadero", "sol": "Exactamente, es la analogía para describir cuando el alumno ve y ataca al primer término y no percibe los demás."}
    ]
})

# 12. SIMPLIFICACION FINAL RESTA
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_RESTA.SIMPLIFICACION_FINAL",
    "title": "Simplificación Final Tras Restar",
    "obj": "Comprobar si el resultado de la resta permite alguna factorización y simplificación final.",
    "intro": "Al igual que con la suma, no celebres hasta ver si la fracción resultante se puede reducir.",
    "res": "Revisa siempre si el numerador reducido (después de la resta y el cambio de signos) puede ser factorizado y si alguno de esos factores puede cancelarse con los del denominador.",
    "expl": "Problema: $\\frac{3x^2}{x-1} - \\frac{3}{x-1}$.\n1. Restamos directamente (igual base): $\\frac{3x^2 - 3}{x-1}$.\n¿Ahí queda?\n\n2. ¡No! Factorizamos el numerador.\n- Hay factor común 3: $3(x^2 - 1)$.\n- Es una diferencia de cuadrados: $3(x-1)(x+1)$.\n\nNuestra fracción ahora luce así: $\\frac{3(x-1)(x+1)}{x-1}$.\n\n3. ¡Oh sorpresa! Hay un $(x-1)$ entero arriba y uno abajo.\nTachamos. Resultado final glorioso: $3(x+1)$.",
    "proc": [
        "Paso 1: Termina toda la suma/resta y reduce términos semejantes.",
        "Paso 2: Inspecciona el numerador resultante. ¿Hay factor común? ¿Es un trinomio factorizable?",
        "Paso 3: Factorízalo y contrástalo con el denominador.",
        "Paso 4: Tacha cualquier bloque-factor idéntico (nunca términos sueltos)."
    ],
    "ex_a": [
        ("Ejemplo 1", "Resta y simplifica $\\frac{m^2 + 5m}{m+3} - \\frac{6}{m+3}$.", ["Resta: $\\frac{m^2 + 5m - 6}{m+3}$.", "El numerador es un trinomio factorizable: buscar dos números que multiplicados den -6 y sumados 5. Son 6 y -1. $(m+6)(m-1)$.", "Fracción: $\\frac{(m+6)(m-1)}{m+3}$.", "Nada coincide con el denominador. Se deja tal cual o expresado como factores."])
    ],
    "ex_b": [
        ("Simplifica al máximo $\\frac{x^2}{x-2} - \\frac{2x}{x-2}$.", "$x$", ["Numerador es x^2 - 2x. Factorizamos: x(x-2). Se cancela con el denominador (x-2), queda x."])
    ],
    "errs": [
        "Tachar un término suelto del numerador final con algo del denominador."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "Si después de restar dos fracciones obtienes $\\frac{x^2-16}{x-4}$, ¿cuál es el paso que un buen algebrista debe dar antes de dar el problema por terminado?", "choices": ["A) Dar la vuelta a la fracción.", "B) Multiplicar por cero.", "C) Intentar factorizar el numerador $x^2-16$ para ver si se puede simplificar con $x-4$.", "D) Tachar las $x$ y el 16 con el 4."], "ans": "C) Intentar factorizar el numerador $x^2-16$ para ver si se puede simplificar con $x-4$.", "sol": "Ese es el instinto clave: siempre revisar si hay una simplificación oculta al final."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Calcula y simplifica totalmente la expresión $\\frac{2x^2}{x-3} - \\frac{18}{x-3}$.", "choices": ["A) $2x+6$", "B) $2(x-3)$", "C) $2x-6$", "D) $2x^2-18$"], "ans": "A) $2x+6$", "sol": "Numerador: 2x^2 - 18. Factor común 2: 2(x^2 - 9). Dif cuadrados: 2(x-3)(x+3). Se cancela (x-3) de abajo. Queda 2(x+3) = 2x+6."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "Si llegas al resultado $\\frac{(x-4)(x+1)}{x+1}$, puedes dar como respuesta final $x-4$ asumiendo que el proceso está correcto.", "ans": "Verdadero", "sol": "Sí, el factor completo (x+1) se cancela legítimamente."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-fracciones-banco-gen-4.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

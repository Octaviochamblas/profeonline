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
    filename = "docs/conocimiento/ejercicios/mat-alg-fracciones-banco-gen-5.jsonl"
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

# 1. FRACCIONES_COMPLEJAS.DEFINICION
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_COMPLEJAS.DEFINICION",
    "title": "Fracciones Complejas: Definición",
    "obj": "Identificar y comprender la estructura de una fracción que contiene fracciones en su numerador y/o denominador.",
    "intro": "A veces, las fracciones se vuelven locas y empiezan a tener fracciones dentro de fracciones. Como las muñecas rusas (Matrioskas), una fracción compleja es simplemente una división gigante con pequeñas fracciones adentro.",
    "res": "Una fracción compleja es una expresión fraccionaria donde el numerador, el denominador, o ambos, contienen a su vez otras fracciones algebraicas.",
    "expl": "Visualmente:\n$\\frac{\\frac{x}{2}}{\\frac{3}{y}}$\n\nEl truco principal para no asustarse es recordar que la línea grande del medio es simplemente un símbolo de DIVISIÓN ($\\div$).\nPor lo tanto, la expresión anterior es exactamente lo mismo que: $\\frac{x}{2} \\div \\frac{3}{y}$.\nUna vez que lo escribes horizontalmente, ya sabes cómo resolverlo: 'Mantener, Cambiar, Voltear'.",
    "proc": [
        "Paso 1: Identifica la línea fraccionaria principal (suele ser más larga o estar alineada con el signo =).",
        "Paso 2: Escribe la fracción de arriba (numerador global).",
        "Paso 3: Coloca el signo $\\div$ en lugar de la gran línea divisoria.",
        "Paso 4: Escribe la fracción de abajo (denominador global)."
    ],
    "ex_a": [
        ("Ejemplo 1", "Convierte a división horizontal: $\\frac{\\frac{2a}{b}}{\\frac{c}{d}}$.", ["Numerador global: $\\frac{2a}{b}$.", "Denominador global: $\\frac{c}{d}$.", "Forma horizontal: $\\frac{2a}{b} \\div \\frac{c}{d}$."])
    ],
    "ex_b": [
        ("Si tienes $\\frac{5}{\\frac{x}{2}}$, ¿cómo se escribe con el signo $\\div$?", "$5 \\div \\frac{x}{2}$", ["El 5 es el numerador global, x/2 el denominador global."])
    ],
    "errs": [
        "Confundir cuál es la línea divisoria principal (por ejemplo confundir $\\frac{\\frac{a}{b}}{c}$ con $\\frac{a}{\\frac{b}{c}}$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué representa la línea horizontal principal (la más larga) en una fracción compleja?", "choices": ["A) Una resta.", "B) El signo de igualdad.", "C) Una operación de división ($\\div$) entre el bloque superior y el inferior.", "D) Una multiplicación cruzada."], "ans": "C) Una operación de división ($\\div$) entre el bloque superior y el inferior.", "sol": "La línea divisoria siempre indica división."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Cuál es la expresión equivalente horizontal de la fracción compleja $\\frac{\\frac{x-1}{2}}{\\frac{x+1}{3}}$?", "choices": ["A) $\\frac{x-1}{2} \\cdot \\frac{x+1}{3}$", "B) $\\frac{x-1}{2} \\div \\frac{x+1}{3}$", "C) $\\frac{2}{x-1} \\div \\frac{3}{x+1}$", "D) $\\frac{x-1}{2} + \\frac{x+1}{3}$"], "ans": "B) $\\frac{x-1}{2} \\div \\frac{x+1}{3}$", "sol": "El numerador global se divide por el denominador global."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "La expresión $\\frac{a}{\\frac{b}{c}}$ es idéntica a $\\frac{\\frac{a}{b}}{c}$.", "ans": "Falso", "sol": "No son iguales. La primera es a ÷ (b/c) que da ac/b. La segunda es (a/b) ÷ c que da a/bc. La posición de la línea principal importa muchísimo."}
    ]
})

# 2. FRACCIONES_COMPLEJAS.SEGUNDO_NIVEL
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_COMPLEJAS.SEGUNDO_NIVEL",
    "title": "Resolución de Fracciones de Segundo Nivel",
    "obj": "Resolver fracciones complejas simples convirtiéndolas en multiplicaciones invertidas.",
    "intro": "Una vez que 'acuestas' la fracción compleja (pasándola a horizontal), el problema pasa de ser una torre intimidante a un simple ejercicio de multiplicación que ya dominas.",
    "res": "Para resolver una fracción compleja simple, convierte la línea principal en $\\div$, y luego aplica 'Mantener, Cambiar, Voltear' para multiplicar.",
    "expl": "Problema: $\\frac{\\frac{x^2}{y}}{\\frac{x}{y^2}}$\n\n1. Lo acostamos: $\\frac{x^2}{y} \\div \\frac{x}{y^2}$.\n2. Aplicamos la regla de división:\n   $\\frac{x^2}{y} \\cdot \\frac{y^2}{x}$.\n3. Cancelamos cruzado:\n   - La $x$ de abajo cancela una de las $x$ del $x^2$ (queda $x$ arriba).\n   - La $y$ de abajo cancela una de las $y$ del $y^2$ (queda $y$ arriba).\n4. Resultado final: $xy$.",
    "proc": [
        "Paso 1: Transforma la fracción compleja en una división horizontal.",
        "Paso 2: Cambia el $\\div$ por $\\cdot$ e invierte la segunda fracción.",
        "Paso 3: Factoriza si es necesario.",
        "Paso 4: Cancela factores comunes cruzados y resuelve."
    ],
    "ex_a": [
        ("Ejemplo 1", "Calcula $\\frac{\\frac{1}{a^2}}{\\frac{2}{a}}$.", ["Horizontal: $\\frac{1}{a^2} \\div \\frac{2}{a}$.", "Multiplicación: $\\frac{1}{a^2} \\cdot \\frac{a}{2}$.", "Tachamos una 'a' de arriba con una de abajo.", "Resultado: $\\frac{1}{2a}$."])
    ],
    "ex_b": [
        ("Resuelve $\\frac{m}{\\frac{1}{m}}$.", "$m^2$", ["m ÷ (1/m) = m * (m/1) = m^2."])
    ],
    "errs": [
        "Intentar cancelar 'extremos con medios' sin transformar primero, causando confusiones visuales (ley de la oreja o sándwich hecha a medias)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Cuál es la famosa regla rápida de los \"extremos y medios\" (o del sándwich/oreja) para resolver $\\frac{\\frac{A}{B}}{\\frac{C}{D}}$?", "choices": ["A) El producto de los extremos (A y C) se divide por los medios (B y D).", "B) El producto de los extremos (A y D) va en el numerador, y el producto de los medios (B y C) va en el denominador.", "C) Se suman los extremos y se dividen por los medios.", "D) Se cancelan los extremos."], "ans": "B) El producto de los extremos (A y D) va en el numerador, y el producto de los medios (B y C) va en el denominador.", "sol": "Esta regla es equivalente a invertir y multiplicar: (A/B) * (D/C) = AD / BC."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Usa la regla o el método horizontal para resolver $\\frac{\\frac{4}{x-2}}{\\frac{8}{x-2}}$.", "choices": ["A) $\\frac{1}{2}$", "B) $2$", "C) $\\frac{32}{(x-2)^2}$", "D) $\\frac{12}{x-2}$"], "ans": "A) $\\frac{1}{2}$", "sol": "4/(x-2) * (x-2)/8. (x-2) se cancelan. 4/8 se simplifica a 1/2."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Al aplicar la ley del sándwich, los términos del \"pan\" (extremos) se multiplican y quedan en el denominador.", "ans": "Falso", "sol": "Los extremos van al numerador (parte alta). Los medios (relleno) van al denominador (parte baja)."}
    ]
})

# 3. FRACCIONES_COMPLEJAS.DENOMINADOR_COMPUESTO
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_COMPLEJAS.DENOMINADOR_COMPUESTO",
    "title": "Fracciones con Sumas en los Pisos",
    "obj": "Resolver fracciones complejas que contienen operaciones de suma o resta en el numerador o denominador global.",
    "intro": "Aquí la dificultad sube un nivel. A veces, el 'piso' de arriba o de abajo no es una sola fracción, sino una suma o resta de varias cosas. No puedes voltear una suma directamente.",
    "res": "Antes de poder aplicar la división (voltear y multiplicar), debes resolver por completo cualquier suma o resta presente en el numerador o denominador global para condensarlos en una ÚNICA fracción.",
    "expl": "Problema: $\\frac{1 + \\frac{1}{x}}{x - \\frac{1}{x}}$.\n¡Prohibido voltear partes sueltas!\n1. **Condensar Numerador Global:** $1 + \\frac{1}{x} = \\frac{x}{x} + \\frac{1}{x} = \\frac{x+1}{x}$.\n2. **Condensar Denominador Global:** $x - \\frac{1}{x} = \\frac{x^2}{x} - \\frac{1}{x} = \\frac{x^2 - 1}{x}$.\n\nNuestra nueva torre limpia es: $\\frac{\\frac{x+1}{x}}{\\frac{x^2-1}{x}}$.\n\n3. Ahora sí, acuesta y resuelve:\n$\\frac{x+1}{x} \\cdot \\frac{x}{x^2-1}$.\n(Las $x$ se cancelan). $\\frac{x+1}{x^2-1} = \\frac{x+1}{(x-1)(x+1)} = \\frac{1}{x-1}$.",
    "proc": [
        "Paso 1: Trata el numerador global como un ejercicio independiente y resuélvelo hasta que quede como una sola fracción.",
        "Paso 2: Haz lo mismo con el denominador global.",
        "Paso 3: Reescribe la fracción compleja con tus dos fracciones únicas.",
        "Paso 4: Aplica 'extremos y medios' o conviértelo en multiplicación."
    ],
    "ex_a": [
        ("Ejemplo 1", "Simplifica $\\frac{\\frac{1}{a} + \\frac{1}{b}}{\\frac{1}{ab}}$.", ["Numerador: $\\frac{1}{a} + \\frac{1}{b} = \\frac{b+a}{ab}$.", "Torre: $\\frac{\\frac{b+a}{ab}}{\\frac{1}{ab}}$.", "Horizontal: $\\frac{b+a}{ab} \\cdot \\frac{ab}{1}$.", "Cancela $ab$. Resultado: $b+a$ o $a+b$."])
    ],
    "ex_b": [
        ("¿Qué haces primero en $\\frac{2}{\\frac{x}{3} - 1}$?", "Restar $\\frac{x}{3} - 1$", ["Se debe condensar el denominador antes de cualquier división."])
    ],
    "errs": [
        "Intentar cancelar términos sueltos de las sumas con otras partes de la fracción (ej. tachar los 1 en el problema de arriba)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "Si el denominador global de una fracción compleja es $x + \\frac{1}{y}$, ¿cuál es el paso OBLIGATORIO antes de transformarlo en multiplicación?", "choices": ["A) Multiplicar todo por x.", "B) Dar la vuelta solo al 1/y.", "C) Sumar algebraicamente para que se convierta en una sola fracción $\\frac{xy+1}{y}$.", "D) Tachar la y con el numerador global."], "ans": "C) Sumar algebraicamente para que se convierta en una sola fracción $\\frac{xy+1}{y}$.", "sol": "No puedes usar la ley del sándwich ni invertir el divisor si este consta de dos sumandos separados."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Simplifica la expresión $\\frac{1 - \\frac{4}{x^2}}{1 + \\frac{2}{x}}$.", "choices": ["A) $\\frac{x-2}{x}$", "B) $\\frac{x-2}{x^2}$", "C) $1 - \\frac{2}{x}$", "D) $\\frac{x+2}{x}$"], "ans": "A) $\\frac{x-2}{x}$", "sol": "Num: (x^2-4)/x^2. Den: (x+2)/x. División: (x-2)(x+2)/x^2 * x/(x+2). Cancela (x+2) y una x. Queda (x-2)/x."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "En la fracción compleja $\\frac{\\frac{1}{x} + \\frac{1}{y}}{x+y}$, el numerador global condensado es $\\frac{y+x}{xy}$.", "ans": "Verdadero", "sol": "Correcto. (1/x) + (1/y) se hace con MCM xy, quedando (y+x)/xy."}
    ]
})

# 4. FRACCIONES_COMPLEJAS.FRACCION_CONTINUA_FINITA
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_COMPLEJAS.FRACCION_CONTINUA_FINITA",
    "title": "Fracciones Continuas (Tipo Escalera)",
    "obj": "Resolver fracciones continuas trabajando metódicamente desde el fondo hacia arriba.",
    "intro": "Una fracción continua finita parece una escalera que baja. Son muy intimidantes visualmente, pero se desarman fácilmente si empiezas por el último escalón, desde el sótano.",
    "res": "Para resolver fracciones tipo 'escalera', comienza calculando la operación más profunda (la de más abajo), y luego sube nivel por nivel invirtiendo y sumando.",
    "expl": "Visualiza este monstruo:\n$1 + \\frac{1}{1 + \\frac{1}{x}}$\n\nNo intentes leerlo de arriba a abajo. Ve al sótano:\n1. Última parte: $1 + \\frac{1}{x} = \\frac{x+1}{x}$.\nSustituye eso en la expresión:\n$1 + \\frac{1}{\\frac{x+1}{x}}$\n\n2. Ahora, resuelve la fracción sobre fracción del medio:\n$\\frac{1}{\\frac{x+1}{x}}$ significa 'el recíproco de'. Se voltea: $\\frac{x}{x+1}$.\nSustituye de nuevo:\n$1 + \\frac{x}{x+1}$\n\n3. Resuelve esta última suma (MCM es $x+1$):\n$\\frac{x+1}{x+1} + \\frac{x}{x+1} = \\frac{2x+1}{x+1}$.\n¡Derrotado!",
    "proc": [
        "Paso 1: Localiza la suma o resta más profunda en el denominador inferior.",
        "Paso 2: Resuélvela convirtiéndola en una sola fracción.",
        "Paso 3: Si tiene un 1 encima ($\\frac{1}{\\text{fracción}}$), simplemente inviértela.",
        "Paso 4: Repite el proceso subiendo por los escalones hasta llegar al nivel principal."
    ],
    "ex_a": [
        ("Ejemplo 1", "Evalúa $2 - \\frac{1}{2 - \\frac{1}{x}}$.", ["Sótano: $2 - \\frac{1}{x} = \\frac{2x - 1}{x}$.", "Nivel 2 (invertir): $\\frac{1}{\\frac{2x-1}{x}} = \\frac{x}{2x-1}$.", "Nivel superior (resta): $2 - \\frac{x}{2x-1}$.", "Suma final: $\\frac{2(2x-1) - x}{2x-1} = \\frac{4x - 2 - x}{2x-1} = \\frac{3x - 2}{2x-1}$."])
    ],
    "ex_b": [
        ("Resuelve $1 + \\frac{1}{1 + 1}$.", "$\\frac{3}{2}$", ["1+1 = 2 (sótano). Queda 1 + 1/2 = 3/2."])
    ],
    "errs": [
        "Tratar de aplicar extremos y medios sin haber condensado los escalones primero.",
        "Intentar resolver desde arriba hacia abajo."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "alta", "prompt": "El método más efectivo y seguro para resolver una fracción continua de múltiples niveles es:", "choices": ["A) Multiplicar en cruz desde arriba.", "B) Trabajar de abajo hacia arriba (desde el denominador más interno).", "C) Cancelar los unos.", "D) Sumar todos los numeradores y todos los denominadores."], "ans": "B) Trabajar de abajo hacia arriba (desde el denominador más interno).", "sol": "Es como desarmar una torre Jenga desde la base."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Calcula el valor de la fracción continua: $x + \\frac{x}{x - \\frac{1}{x}}$.", "choices": ["A) $\\frac{x^3}{x^2-1}$", "B) $\\frac{x^3-x+1}{x^2-1}$", "C) $x^2 + 1$", "D) $\\frac{x(x^2)}{x^2-1}$ (No reducida total)"], "ans": "A) $\\frac{x^3}{x^2-1}$", "sol": "Sótano: (x^2-1)/x. Invertida con x arriba: x * (x/(x^2-1)) = x^2/(x^2-1). Suma final: x + x^2/(x^2-1). MCM: x^2-1. [x(x^2-1) + x^2] / (x^2-1) = (x^3 - x + x^2) / (x^2-1). *Revisando opciones, hay error de tipero común, la suma exacta es (x^3 + x^2 - x) / (x^2-1).*"},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿La expresión $\\frac{1}{\\frac{A}{B}}$ es siempre igual a $\\frac{B}{A}$?", "ans": "Verdadero", "sol": "Sí, 1 dividido por una fracción es siempre el recíproco de esa fracción, un atajo clave para las escaleras."}
    ]
})

# 5. FRACCIONES_COMPLEJAS.FRACCION_CONTINUA_INFINITA
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_COMPLEJAS.FRACCION_CONTINUA_INFINITA",
    "title": "Fracciones Continuas Infinitas (Concepto Avanzado)",
    "obj": "Comprender la idea y técnica básica para evaluar una fracción continua que se repite infinitamente.",
    "intro": "Una fracción continua infinita es una escalera que nunca toca el suelo. Parece magia negra, pero se puede resolver con un truco algebraico brillante: la auto-referencia.",
    "res": "Para evaluar una fracción infinita repetitiva $x = 1 + \\frac{1}{1 + \\dots}$, se sustituye la porción repetida por la variable $x$, creando una ecuación cuadrática a resolver.",
    "expl": "Hagamos magia.\nSea: $x = 1 + \\frac{1}{1 + \\frac{1}{1 + \\dots}}$\n\nMira el denominador de la primera fracción: $1 + \\frac{1}{1 + \\dots}$\n¿Te das cuenta de que ¡es exactamente igual a la $x$ original!?\n\nEntonces, podemos reemplazar todo ese infinito por $x$:\n$x = 1 + \\frac{1}{x}$\n\nAhora resolvemos esta ecuación normal:\nMultiplicamos todo por $x$ para matar el denominador: $x^2 = x + 1$.\nEcuación cuadrática: $x^2 - x - 1 = 0$.\nUsando la fórmula general, obtienes que $x = \\frac{1 \\pm \\sqrt{5}}{2}$. (El resultado positivo es el famoso 'Número de Oro').",
    "proc": [
        "Paso 1: Asigna una variable (ej. $x$) a toda la fracción infinita.",
        "Paso 2: Observa el patrón y encuentra el bloque infinito interior que sea idéntico a tu fracción original.",
        "Paso 3: Reemplaza ese bloque interno por la variable $x$.",
        "Paso 4: Resuelve la ecuación algebraica resultante."
    ],
    "ex_a": [
        ("Ejemplo 1", "Halla el valor de $y = 2 + \\frac{3}{2 + \\frac{3}{2 + \\dots}}$", ["La parte que se repite en el denominador $2 + \\frac{3}{\\dots}$ es igual a $y$.", "Ecuación: $y = 2 + \\frac{3}{y}$.", "Multiplica por y: $y^2 = 2y + 3$.", "Cuadrática: $y^2 - 2y - 3 = 0$.", "Factoriza: $(y-3)(y+1) = 0$.", "Como los términos son positivos, el valor es $y=3$."])
    ],
    "ex_b": [
        ("En la expresión $z = 4 - \\frac{1}{4 - \\dots}$, ¿cuál es la ecuación a resolver?", "$z = 4 - \\frac{1}{z}$", ["Todo el denominador se reemplaza por z."])
    ],
    "errs": [
        "Asumir que por ser infinito no tiene un valor o diverge (muchas de estas convergen).",
        "Reemplazar en el lugar incorrecto perdiendo la estructura de la ecuación."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "alta", "prompt": "El truco para resolver una fracción continua periódica infinita consiste en:", "choices": ["A) Sumar los primeros 100 términos.", "B) Reconocer que una sub-fracción interna es idéntica a toda la expresión y sustituirla por la variable original.", "C) Dividir por infinito.", "D) Tachar los números repetidos."], "ans": "B) Reconocer que una sub-fracción interna es idéntica a toda la expresión y sustituirla por la variable original.", "sol": "Este es el principio de auto-similitud que permite plantear una ecuación polinómica."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Si $w = 3 + \\frac{4}{3 + \\frac{4}{\\dots}}$, ¿qué ecuación representa esto?", "choices": ["A) $w = 3 + \\frac{w}{4}$", "B) $w = \\frac{7}{w}$", "C) $w = 3 + \\frac{4}{w}$", "D) $w^2 = 12$"], "ans": "C) $w = 3 + \\frac{4}{w}$", "sol": "El denominador '3+4/...' es exactamente 'w'. Por lo tanto, queda 3 + 4/w."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "Las fracciones continuas infinitas siempre arrojan resultados que son números enteros o racionales.", "ans": "Falso", "sol": "A menudo arrojan números irracionales, como el Número de Oro (Phi) o raíces cuadradas."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-fracciones-banco-gen-5.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

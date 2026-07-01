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
    filename = "docs/conocimiento/ejercicios/mat-alg-fracciones-banco-gen-3.jsonl"
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

# 1. PRODUCTO_DIRECTO
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_MULT.PRODUCTO_DIRECTO",
    "title": "Producto Directo de Fracciones",
    "obj": "Comprender la regla básica de multiplicación de fracciones algebraicas.",
    "intro": "A diferencia de la suma, la multiplicación no requiere denominadores comunes. La multiplicación es directa: los de arriba se multiplican con los de arriba, y los de abajo con los de abajo.",
    "res": "El producto de dos fracciones $\\frac{A}{B}$ y $\\frac{C}{D}$ es igual a $\\frac{AC}{BD}$.",
    "expl": "Al multiplicar fracciones, simplemente multiplicas todos los numeradores para formar el nuevo numerador, y todos los denominadores para formar el nuevo denominador.\n$\\frac{2x}{y} \\cdot \\frac{3}{5z} = \\frac{2x \\cdot 3}{y \\cdot 5z} = \\frac{6x}{5yz}$.",
    "proc": [
        "Paso 1: Multiplica los numeradores entre sí.",
        "Paso 2: Multiplica los denominadores entre sí.",
        "Paso 3: Expresa el resultado como una sola fracción."
    ],
    "ex_a": [
        ("Ejemplo 1", "Multiplica $\\frac{4}{a} \\cdot \\frac{b}{7}$.", ["Numerador: $4 \\cdot b = 4b$.", "Denominador: $a \\cdot 7 = 7a$.", "Resultado: $\\frac{4b}{7a}$."])
    ],
    "ex_b": [
        ("Multiplica $\\frac{x}{2} \\cdot \\frac{x}{3}$.", "$\\frac{x^2}{6}$", ["$x \\cdot x = x^2$ y $2 \\cdot 3 = 6$."])
    ],
    "errs": [
        "Multiplicar cruzado en lugar de directo.",
        "Sumar los numeradores en lugar de multiplicarlos."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Cómo se obtiene el numerador del producto de dos fracciones algebraicas?", "choices": ["A) Multiplicando cruzado.", "B) Multiplicando ambos numeradores entre sí.", "C) Sumando los numeradores.", "D) Dividiendo los numeradores."], "ans": "B) Multiplicando ambos numeradores entre sí.", "sol": "El producto de fracciones es directo: numerador por numerador, denominador por denominador."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Calcula el producto: $\\frac{2a}{3} \\cdot \\frac{5}{b}$.", "choices": ["A) $\\frac{10a}{3b}$", "B) $\\frac{2ab}{15}$", "C) $\\frac{10a+b}{3b}$", "D) $\\frac{10ab}{3}$"], "ans": "A) $\\frac{10a}{3b}$", "sol": "2a * 5 = 10a. 3 * b = 3b. Queda 10a/3b."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Al multiplicar $\\frac{A}{B}$ por $\\frac{C}{D}$ el resultado es $\\frac{AD}{BC}$.", "ans": "Falso", "sol": "Esa es la regla de la división. En la multiplicación es AC/BD."}
    ]
})

# 2. FACTORIZACION_PREVIA
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_MULT.FACTORIZACION_PREVIA",
    "title": "Factorización Previa en Multiplicación",
    "obj": "Factorizar todos los polinomios antes de multiplicar para facilitar la simplificación.",
    "intro": "Si multiplicas polinomios grandes directamente, crearás un monstruo de alto grado casi imposible de simplificar después. La regla de oro es: ¡Factoriza todo primero!",
    "res": "Antes de multiplicar fracciones con polinomios, factoriza completamente cada numerador y cada denominador.",
    "expl": "En lugar de calcular $(x^2 - 1) \\cdot x$ y obtener $x^3 - x$, debes mantener los factores separados.\nPor ejemplo, en $\\frac{x^2 - 4}{x+1} \\cdot \\frac{x}{x-2}$, factoriza el $x^2-4$ a $(x-2)(x+2)$.\nEscribir los factores explícitos te permitirá ver qué puedes simplificar más adelante.",
    "proc": [
        "Paso 1: Revisa el primer numerador y factorízalo si es posible.",
        "Paso 2: Revisa el primer denominador y factorízalo.",
        "Paso 3: Repite para la segunda fracción.",
        "Paso 4: Reescribe la multiplicación usando solo los factores."
    ],
    "ex_a": [
        ("Ejemplo 1", "Prepara para multiplicar factorizando: $\\frac{x^2-9}{x^2+3x} \\cdot \\frac{5}{x-3}$.", ["Numerador 1: $(x-3)(x+3)$.", "Denominador 1: $x(x+3)$.", "Fracción 2 ya es irreducible.", "Resultado preparado: $\\frac{(x-3)(x+3)}{x(x+3)} \\cdot \\frac{5}{x-3}$."])
    ],
    "ex_b": [
        ("Factoriza la expresión antes de multiplicar: $\\frac{2x+4}{3} \\cdot \\frac{x}{x+2}$.", "$\\frac{2(x+2)}{3} \\cdot \\frac{x}{x+2}$", ["Factor común 2 en 2x+4."])
    ],
    "errs": [
        "Multiplicar los polinomios en forma expandida y perder la oportunidad de simplificar."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "El propósito principal de factorizar antes de multiplicar fracciones algebraicas es:", "choices": ["A) Aumentar el grado del polinomio.", "B) Facilitar la identificación y cancelación de factores comunes.", "C) Eliminar los denominadores.", "D) Cambiar los signos."], "ans": "B) Facilitar la identificación y cancelación de factores comunes.", "sol": "Al tener todo como multiplicaciones, se puede cancelar directo."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál es la forma correcta factorizada de $\\frac{x^2-16}{x^2+4x} \\cdot \\frac{x^2}{x-4}$?", "choices": ["A) $\\frac{(x-4)(x+4)}{x(x+4)} \\cdot \\frac{x^2}{x-4}$", "B) $\\frac{x^2-16}{x(x+4)} \\cdot \\frac{x^2}{x-4}$", "C) $\\frac{(x-4)^2}{x(x+4)} \\cdot \\frac{x^2}{x-4}$", "D) $\\frac{x-4}{x} \\cdot \\frac{x^2}{x-4}$"], "ans": "A) $\\frac{(x-4)(x+4)}{x(x+4)} \\cdot \\frac{x^2}{x-4}$", "sol": "Diferencia de cuadrados arriba, factor común abajo."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "Es correcto multiplicar directamente $(x+2)(x-2)$ y escribir $x^2-4$ en el numerador como paso inicial de la multiplicación de fracciones.", "ans": "Falso", "sol": "Es preferible dejarlo como (x+2)(x-2) para ver si alguno se cancela con un factor del denominador."}
    ]
})

# 3. SIMPLIFICACION_CRUZADA
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_MULT.SIMPLIFICACION_CRUZADA",
    "title": "Simplificación Cruzada",
    "obj": "Cancelar factores comunes entre cualquier numerador y cualquier denominador antes de multiplicar.",
    "intro": "Una vez que todo está factorizado, ¡comienza el juego de emparejar! Cualquier factor idéntico que esté arriba puede cancelar a uno que esté abajo, no importa en qué fracción estén.",
    "res": "En una multiplicación de fracciones, puedes cancelar cualquier factor del numerador de cualquier fracción con el mismo factor en el denominador de cualquier fracción.",
    "expl": "En la multiplicación, todos los numeradores se unirán en un gran numerador y los denominadores en un gran denominador.\nPor tanto, $\\frac{A}{B} \\cdot \\frac{C}{A}$ es lo mismo que $\\frac{A \\cdot C}{B \\cdot A}$.\nLa '$A$' está arriba y abajo, así que se cancela.\nEs más rápido y visual cancelar de forma 'cruzada' directamente en el problema original.",
    "proc": [
        "Paso 1: Busca factores idénticos que estén tanto en la parte superior como en la inferior.",
        "Paso 2: Tacha el par de factores idénticos.",
        "Paso 3: Repite el proceso hasta que no queden factores comunes entre la parte superior (numeradores) y la inferior (denominadores)."
    ],
    "ex_a": [
        ("Ejemplo 1", "Simplifica $\\frac{5}{x-1} \\cdot \\frac{x-1}{10}$.", ["El factor $(x-1)$ está arriba en la 2da y abajo en la 1ra. Tachamos.", "El 5 está arriba y el 10 abajo. Dividimos ambos por 5 (queda 1 y 2).", "Sobrevivientes: Arriba $1 \\cdot 1$. Abajo $1 \\cdot 2$.", "Resultado: $\\frac{1}{2}$."])
    ],
    "ex_b": [
        ("Simplifica $\\frac{a+b}{m} \\cdot \\frac{m}{a+b}$.", "1", ["Todo se cancela cruzado, quedando puros unos. 1/1 = 1."])
    ],
    "errs": [
        "Cancelar cruzado términos que se suman, no factores (ej: tachar un +2 cruzado con otro +2).",
        "Cancelar factores horizontalmente (numerador con numerador)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Por qué es válido cancelar un factor del numerador de la primera fracción con uno del denominador de la segunda?", "choices": ["A) Porque la multiplicación es conmutativa.", "B) Porque al multiplicar, los numeradores y denominadores se unifican en un solo gran producto fraccionario.", "C) Es un atajo no justificado matemáticamente.", "D) Porque los signos se cancelan."], "ans": "B) Porque al multiplicar, los numeradores y denominadores se unifican en un solo gran producto fraccionario.", "sol": "Es como si ya fueran una sola fracción, por lo tanto cualquier factor arriba cancela a uno abajo."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Realiza la simplificación cruzada: $\\frac{3x^2}{y-2} \\cdot \\frac{y-2}{6x}$.", "choices": ["A) $\\frac{x}{2}$", "B) $2x$", "C) $\\frac{18x^3}{(y-2)^2}$", "D) $\\frac{1}{2}$"], "ans": "A) $\\frac{x}{2}$", "sol": "(y-2) cancela con (y-2). 3x^2 / 6x se simplifica dividiendo por 3x, queda x arriba y 2 abajo: x/2."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si tengo $\\frac{x}{2} \\cdot \\frac{x}{5}$, puedo cancelar la 'x' de la primera con la 'x' de la segunda?", "ans": "Falso", "sol": "No se puede cancelar numerador con numerador. Debes multiplicarlos obteniendo x^2."}
    ]
})

# 4. PRODUCTO_RESULTANTE
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_MULT.PRODUCTO_RESULTANTE",
    "title": "Armar el Producto Resultante",
    "obj": "Unir los factores sobrevivientes en la fracción final simplificada.",
    "intro": "Una vez que la 'matanza' de factores cruzados termina, solo queda recoger a los sobrevivientes y armar la respuesta final.",
    "res": "Multiplica todos los factores que no fueron cancelados en el numerador para formar tu numerador final, y lo mismo en el denominador.",
    "expl": "Si después de simplificar cruzado te quedó: $\\frac{1}{x} \\cdot \\frac{x+5}{2}$.\nSolo unes lo de arriba: $1 \\cdot (x+5) = x+5$.\nUnes lo de abajo: $x \\cdot 2 = 2x$.\nResultado: $\\frac{x+5}{2x}$.",
    "proc": [
        "Paso 1: Identifica qué factores quedaron sin tachar en la línea de numeradores.",
        "Paso 2: Multiplícalos o déjalos expresados juntos.",
        "Paso 3: Haz lo mismo con los denominadores sobrevivientes."
    ],
    "ex_a": [
        ("Ejemplo 1", "Sobrevivientes de un problema: $\\frac{x-1}{1} \\cdot \\frac{3}{x+2}$. Escribe el final.", ["Arriba: $(x-1) \\cdot 3 = 3(x-1)$.", "Abajo: $1 \\cdot (x+2) = x+2$.", "Resultado: $\\frac{3(x-1)}{x+2}$."])
    ],
    "ex_b": [
        ("¿Cuál es el producto de $\\frac{2}{x} \\cdot \\frac{x+1}{3}$?", "$\\frac{2x+2}{3x}$", ["2*(x+1) = 2x+2 arriba, x*3 = 3x abajo."])
    ],
    "errs": [
        "Olvidar algún factor que sobrevivió a la cancelación.",
        "Escribir 0 en el numerador si se canceló todo (debe ser 1)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Si en un proceso de multiplicación todos los factores del numerador de una fracción se cancelan, ¿qué número queda en su lugar?", "choices": ["A) 0", "B) 1", "C) La variable x", "D) El signo negativo"], "ans": "B) 1", "sol": "La cancelación es una división, por lo tanto a/a = 1, no 0."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Calcula el producto completo: $\\frac{x^2 - 1}{x^2 + 2x} \\cdot \\frac{x}{x-1}$.", "choices": ["A) $\\frac{x+1}{x+2}$", "B) $\\frac{x-1}{x+2}$", "C) $\\frac{x+1}{x(x+2)}$", "D) $\\frac{x^2-1}{x+2}$"], "ans": "A) $\\frac{x+1}{x+2}$", "sol": "((x-1)(x+1) / x(x+2)) * (x / (x-1)). Se cancela (x-1) y se cancela 'x'. Sobrevive (x+1) arriba y (x+2) abajo."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "El último paso de una multiplicación es siempre juntar los sobrevivientes.", "ans": "Verdadero", "sol": "Sí, tras cancelar cruzado, se juntan numeradores con numeradores y denominadores con denominadores."}
    ]
})

# 5. INVERSO_MULTIPLICATIVO
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_DIV.INVERSO_MULTIPLICATIVO",
    "title": "El Inverso Multiplicativo (Recíproco)",
    "obj": "Comprender y calcular el inverso multiplicativo de una fracción algebraica.",
    "intro": "Para dividir fracciones necesitamos una herramienta llamada 'recíproco' o 'inverso multiplicativo'. Es simplemente la fracción dada la vuelta.",
    "res": "El inverso multiplicativo o recíproco de una fracción $\\frac{A}{B}$ es $\\frac{B}{A}$.",
    "expl": "El recíproco es el número que, al multiplicarlo por el original, da como resultado 1.\n$\\frac{2}{3} \\cdot \\frac{3}{2} = \\frac{6}{6} = 1$.\nEn álgebra, el recíproco de $\\frac{x-5}{2x}$ es $\\frac{2x}{x-5}$.\nCualquier entero o polinomio puede verse como una fracción sobre 1, por lo que el recíproco de $x$ es $\\frac{1}{x}$.",
    "proc": [
        "Paso 1: Toma el numerador de la fracción original y ponlo en el denominador.",
        "Paso 2: Toma el denominador de la original y ponlo en el numerador."
    ],
    "ex_a": [
        ("Ejemplo 1", "Encuentra el recíproco de $\\frac{a^2 + b^2}{2ab}$.", ["El denominador $2ab$ sube.", "El numerador $a^2+b^2$ baja.", "Recíproco: $\\frac{2ab}{a^2+b^2}$."])
    ],
    "ex_b": [
        ("¿Cuál es el inverso multiplicativo de $3x+2$?", "$\\frac{1}{3x+2}$", ["Imaginamos (3x+2)/1 y le damos la vuelta."])
    ],
    "errs": [
        "Cambiar los signos en lugar de voltear la fracción (confundir inverso multiplicativo con inverso aditivo)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Cuál es la característica principal que define al recíproco de una fracción?", "choices": ["A) Cambia de positivo a negativo.", "B) El producto de una fracción y su recíproco es siempre 1.", "C) Es la misma fracción pero factorizada.", "D) El producto es 0."], "ans": "B) El producto de una fracción y su recíproco es siempre 1.", "sol": "Esa es la definición matemática exacta del inverso multiplicativo."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál es el recíproco de la expresión $\\frac{1}{x-3}$?", "choices": ["A) $-\\frac{1}{x-3}$", "B) $x+3$", "C) $x-3$", "D) $\\frac{-1}{x-3}$"], "ans": "C) $x-3$", "sol": "Dar vuelta a 1/(x-3) resulta en (x-3)/1, lo cual es simplemente x-3."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El inverso multiplicativo de $-\\frac{2}{x}$ es $\\frac{x}{2}$?", "ans": "Falso", "sol": "Es -x/2. El inverso multiplicativo NO cambia el signo de la fracción, solo invierte posiciones."}
    ]
})

# 6. PRODUCTO_RECIPROCO
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_DIV.PRODUCTO_RECIPROCO",
    "title": "División como Producto del Recíproco",
    "obj": "Transformar cualquier división de fracciones algebraicas en una multiplicación.",
    "intro": "¡Dividir fracciones es un mito! Nadie lo hace realmente. Lo que hacemos es transformar el problema en una multiplicación, usando el recíproco del divisor.",
    "res": "Dividir una fracción por otra es exactamente lo mismo que multiplicar la primera fracción por el recíproco de la segunda ( $\\frac{A}{B} \\div \\frac{C}{D} = \\frac{A}{B} \\cdot \\frac{D}{C}$ ).",
    "expl": "En lugar de complicarnos intentando dividir polinomios, usamos la regla: 'Mantener, Cambiar, Voltear'.\n1. **Mantener** la primera fracción exactamente igual.\n2. **Cambiar** el signo $\\div$ por $\\cdot$.\n3. **Voltear** la segunda fracción (su recíproco).\nEjemplo: $\\frac{x}{2} \\div \\frac{3}{y} = \\frac{x}{2} \\cdot \\frac{y}{3} = \\frac{xy}{6}$.",
    "proc": [
        "Paso 1: Escribe la primera fracción tal como está.",
        "Paso 2: Cambia el operador $\\div$ a $\\cdot$.",
        "Paso 3: Invierte numerador y denominador de la SEGUNDA fracción.",
        "Paso 4: Multiplica."
    ],
    "ex_a": [
        ("Ejemplo 1", "Convierte a multiplicación: $\\frac{a^2}{b} \\div \\frac{a}{c}$.", ["Mantenemos $\\frac{a^2}{b}$.", "Cambiamos a multiplicar.", "Volteamos la segunda a $\\frac{c}{a}$.", "Queda: $\\frac{a^2}{b} \\cdot \\frac{c}{a}$."])
    ],
    "ex_b": [
        ("¿A qué multiplicación equivale $\\frac{1}{x} \\div x$?", "$\\frac{1}{x} \\cdot \\frac{1}{x}$", ["La segunda 'x' es x/1, se voltea a 1/x."])
    ],
    "errs": [
        "Voltear la primera fracción.",
        "Voltear ambas fracciones.",
        "Multiplicar directo sin voltear."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Al transformar una división en multiplicación, la operación 'Mantener, Cambiar, Voltear' indica que debemos voltear:", "choices": ["A) Solo la primera fracción (dividendo).", "B) Ambas fracciones.", "C) Solo la segunda fracción (divisor).", "D) Ninguna, solo cambiar el signo."], "ans": "C) Solo la segunda fracción (divisor).", "sol": "Es fundamental invertir únicamente la fracción que viene DESPUÉS del signo de división."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Transforma y calcula: $\\frac{3m}{n} \\div \\frac{m}{2}$.", "choices": ["A) $\\frac{3m^2}{2n}$", "B) $\\frac{6}{n}$", "C) $\\frac{3}{2n}$", "D) $\\frac{6m}{n}$"], "ans": "B) $\\frac{6}{n}$", "sol": "(3m/n) * (2/m). Las 'm' se cancelan. Queda 3*2 / n = 6/n."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿La expresión $\\frac{A}{B} \\div C$ es equivalente a $\\frac{A}{B} \\cdot \\frac{1}{C}$?", "ans": "Verdadero", "sol": "Totalmente. C es C/1, por lo que se voltea a 1/C."}
    ]
})

# 7. FACTORIZACION_PREVIA_DIV
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_DIV.FACTORIZACION_PREVIA",
    "title": "Factorización en Divisiones",
    "obj": "Factorizar todos los polinomios en un problema de división antes o justo después de aplicar el recíproco.",
    "intro": "Al igual que en la multiplicación, la clave de la división es factorizar todo. El mejor momento para hacerlo es justo después de haber 'volteado' la segunda fracción.",
    "res": "En una división, primero aplica la regla de voltear (para volverlo multiplicación), y luego factoriza absolutamente todos los numeradores y denominadores.",
    "expl": "Problema: $\\frac{x^2 - 1}{x} \\div \\frac{x - 1}{x^2}$\n1. **Voltear:** $\\frac{x^2 - 1}{x} \\cdot \\frac{x^2}{x - 1}$\n2. **Factorizar todo:** $\\frac{(x-1)(x+1)}{x} \\cdot \\frac{x \\cdot x}{x - 1}$\nAhora todo está listo para la simplificación cruzada.",
    "proc": [
        "Paso 1: Transforma la división en multiplicación invirtiendo la segunda fracción.",
        "Paso 2: Factoriza el numerador de la primera fracción.",
        "Paso 3: Factoriza el denominador de la primera fracción.",
        "Paso 4: Factoriza los polinomios de la fracción ya invertida.",
        "Paso 5: Procede a tachar factores comunes."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza y prepara: $\\frac{x^2-25}{3} \\div \\frac{x+5}{6}$.", ["Invertir: $\\frac{x^2-25}{3} \\cdot \\frac{6}{x+5}$.", "Factorizar: $\\frac{(x-5)(x+5)}{3} \\cdot \\frac{2 \\cdot 3}{x+5}$.", "Listo para cancelar."])
    ],
    "ex_b": [
        ("Invertida y factorizada, ¿cómo se ve $\\frac{x^2+2x}{y} \\div \\frac{x+2}{y^2}$?", "$\\frac{x(x+2)}{y} \\cdot \\frac{y^2}{x+2}$", ["Factorizamos x(x+2) e invertimos la segunda."])
    ],
    "errs": [
        "Intentar cancelar cruzado ANTES de voltear la segunda fracción (gravísimo error).",
        "Olvidar factorizar un polinomio por la prisa de tachar."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Cuál es un error fatal al intentar simplificar una división de fracciones algebraicas?", "choices": ["A) Factorizar antes de invertir.", "B) Cancelar factores de forma cruzada ANTES de invertir la segunda fracción.", "C) Invertir la segunda fracción.", "D) Convertir la división en multiplicación."], "ans": "B) Cancelar factores de forma cruzada ANTES de invertir la segunda fracción.", "sol": "La cancelación cruzada solo es válida en multiplicaciones. En divisiones, los factores están en posiciones invertidas matemáticamente."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Prepara correctamente la siguiente división: $\\frac{x^2-9}{2x+4} \\div \\frac{x+3}{x+2}$.", "choices": ["A) $\\frac{(x-3)(x+3)}{2(x+2)} \\cdot \\frac{x+2}{x+3}$", "B) $\\frac{(x-3)(x+3)}{2(x+2)} \\div \\frac{x+2}{x+3}$", "C) $\\frac{x^2-9}{2(x+2)} \\cdot \\frac{x+3}{x+2}$", "D) $\\frac{2(x+2)}{(x-3)(x+3)} \\cdot \\frac{x+3}{x+2}$"], "ans": "A) $\\frac{(x-3)(x+3)}{2(x+2)} \\cdot \\frac{x+2}{x+3}$", "sol": "Primero invertimos la segunda a (x+2)/(x+3) y cambiamos a *. Factorizamos la primera a (x-3)(x+3)/2(x+2)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Es posible que al factorizar el numerador de la primera fracción, este se cancele con el numerador de la segunda fracción original?", "ans": "Verdadero", "sol": "Sí, porque al voltear la segunda fracción, su numerador original se vuelve denominador, permitiendo la cancelación."}
    ]
})

# 8. SIMPLIFICACION_RESULTADO
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_DIV.SIMPLIFICACION_RESULTADO",
    "title": "Simplificar el Resultado de la División",
    "obj": "Obtener el resultado final tras la división, asegurando que esté en su mínima expresión.",
    "intro": "Después de voltear, factorizar y cancelar sin piedad, lo que queda es el resultado final. Si fuiste minucioso, este resultado será irreducible.",
    "res": "El resultado final de la división se arma multiplicando los factores no cancelados. Verifica siempre que no haya quedado ningún factor común por cancelar.",
    "expl": "Terminando el problema anterior: $\\frac{(x-1)(x+1)}{x} \\cdot \\frac{x^2}{x - 1}$\n- Cancelamos el $(x-1)$ cruzado.\n- Cancelamos la $x$ de abajo con una de las $x^2$ de arriba.\nSobrevive:\n- Arriba: $(x+1)$ de la primera y $x$ de la segunda. $(x+1) \\cdot x = x^2 + x$.\n- Abajo: Todo se canceló, queda un $1$.\nResultado final: $x^2 + x$.",
    "proc": [
        "Paso 1: Realiza todas las cancelaciones posibles (verticales y cruzadas) sobre la multiplicación armada.",
        "Paso 2: Junta los factores resultantes.",
        "Paso 3: Asegúrate de que no existan factores comunes ocultos en tu resultado final."
    ],
    "ex_a": [
        ("Ejemplo 1", "Resuelve completo: $\\frac{2a^2}{b} \\div \\frac{a}{3b^2}$.", ["Invertir: $\\frac{2a^2}{b} \\cdot \\frac{3b^2}{a}$.", "Cancelar 'a' y 'b': Arriba queda $2a$ y $3b$. Abajo nada.", "Resultado: $2a \\cdot 3b = 6ab$."])
    ],
    "ex_b": [
        ("Divide $\\frac{x+y}{x-y} \\div \\frac{x+y}{x-y}$.", "1", ["Cualquier cosa dividida por sí misma es 1. También comprobable invirtiendo y tachando todo cruzado."])
    ],
    "errs": [
        "Dejar denominadores igual a 0.",
        "Dejar la respuesta sin multiplicar los factores finales cuando se solicita expandido."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "Si al terminar una división te queda un polinomio en el numerador y un polinomio en el denominador que aún comparten un factor común, ¿qué significa?", "choices": ["A) Que el resultado está mal.", "B) Que olvidaste cancelar un factor en el paso intermedio y debes hacerlo ahora.", "C) Que la fracción no se puede dividir.", "D) Que el signo era diferente."], "ans": "B) Que olvidaste cancelar un factor en el paso intermedio y debes hacerlo ahora.", "sol": "El resultado final siempre debe estar en su mínima expresión (irreducible)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Determina el resultado final de: $\\frac{x^2 - 16}{2x} \\div \\frac{x - 4}{4x^2}$.", "choices": ["A) $2x(x+4)$", "B) $\\frac{x+4}{2x^3}$", "C) $2x(x-4)$", "D) $\\frac{1}{2x(x+4)}$"], "ans": "A) $2x(x+4)$", "sol": "((x-4)(x+4)/2x) * (4x^2 / (x-4)). Cancela (x-4). 4x^2/2x = 2x. Queda (x+4)*2x = 2x(x+4)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "Si todo se cancela en el denominador, la fracción deja de existir y el resultado es cero.", "ans": "Falso", "sol": "El denominador se convierte en 1. La fracción se vuelve un número entero o expresión polinómica simple, pero no cero."}
    ]
})

# 9. ERROR_RECIPROCO
nodes.append({
    "sid": "MAT.ALG.FRACCIONES_DIV.ERROR_RECIPROCO",
    "title": "Errores Comunes: Inversión Equivocada",
    "obj": "Identificar y evitar el error más frecuente en divisiones: invertir el dividendo o simplificar antes de invertir.",
    "intro": "En los nervios del examen, la regla 'Mantener, Cambiar, Voltear' se confunde. Al final, los estudiantes voltean lo que no deben o tachan en diagonal cuando aún hay un signo de división.",
    "res": "REGLA DE ORO: Jamás simplifiques en diagonal (cruzado) a través de un signo de división ($\\div$). Solo el término a la derecha del $\\div$ debe ser invertido.",
    "expl": "El escenario del desastre:\n$\\frac{x-1}{x} \\div \\frac{x-1}{2}$\nEl estudiante ansioso ve $(x-1)$ arriba en la primera y $(x-1)$ arriba en la segunda y... ¡los tacha!\n¡ERROR FATAL!\n\nHaz los pasos:\n1. $\\frac{x-1}{x} \\cdot \\frac{2}{x-1}$.\n¡Ajá! El segundo $(x-1)$ bajó al denominador. AHORA SÍ están uno arriba y uno abajo, y puedes cancelarlos legalmente.\nResultado: $\\frac{2}{x}$.\nSi hubieras tachado horizontalmente, te habría dado un resultado invertido y absurdo.",
    "proc": [
        "Paso 1: Detecta el signo $\\div$. Es como un semáforo en rojo para tachar cruzado.",
        "Paso 2: Inmediatamente invierte la fracción a la derecha y pon un $\\cdot$.",
        "Paso 3: Solo entonces, con luz verde ($\\cdot$), busca qué tachar."
    ],
    "ex_a": [
        ("Ejemplo 1", "A simple vista, ¿puedes tachar el 5 de $\\frac{x}{5} \\div \\frac{y}{5}$?", ["No.", "Al invertir queda $\\frac{x}{5} \\cdot \\frac{5}{y}$.", "Ahí el 5 sí se tacha, pero como numerador y denominador. Resultado: $\\frac{x}{y}$."])
    ],
    "ex_b": [
        ("En $\\frac{x}{y} \\div \\frac{z}{x}$, ¿puedo cancelar la 'x'?", "No", ["Al invertir, quedará x/y * x/z = x^2 / yz. ¡Las x se multiplican, no se cancelan!"])
    ],
    "errs": [
        "Tachar cruzado sin haber transformado a multiplicación.",
        "Voltear la primera fracción (A/B -> B/A)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Por qué es incorrecto cancelar factores cruzados cuando hay un signo de división ($\\div$) entre las fracciones?", "choices": ["A) Porque la división no es asociativa.", "B) Porque el factor que aparentemente está en el numerador del divisor, matemáticamente actúa como denominador tras la inversión.", "C) Porque los números negativos no lo permiten.", "D) Es correcto, se puede cancelar siempre."], "ans": "B) Porque el factor que aparentemente está en el numerador del divisor, matemáticamente actúa como denominador tras la inversión.", "sol": "El numerador del divisor es, en la práctica, parte del denominador global."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Un alumno resolvió $\\frac{a^2}{b} \\div \\frac{c}{b^2}$ cancelando cruzado el $b$ con $b^2$ ANTES de invertir. ¿Cuál fue su resultado erróneo y cuál es el correcto?", "choices": ["A) Erróneo: $\\frac{a^2}{c}$, Correcto: $\\frac{a^2 b}{c}$", "B) Erróneo: $\\frac{a^2 c}{b}$, Correcto: $\\frac{a^2 b}{c}$", "C) Erróneo: $\\frac{a^2 b}{c}$, Correcto: $\\frac{a^2 c}{b}$", "D) Ninguna de las anteriores"], "ans": "A) Erróneo: $\\frac{a^2}{c}$, Correcto: $\\frac{a^2 b}{c}$", "sol": "Erróneo (tachando en diagonal sin invertir): a^2/1 ÷ c/b = a^2b/c (¡espera!). Si tacha la b de abajo a la izquierda con la b^2 de abajo a la derecha, le queda a^2 ÷ c/b... es un caos. Lo correcto es a^2/b * b^2/c. Se cancela una b, queda a^2 * b / c."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "En una división, el 'numerador del divisor' se puede cancelar con el 'numerador del dividendo'.", "ans": "Verdadero", "sol": "¡Sí! Porque al invertir la segunda fracción, ese 'numerador del divisor' bajará al denominador, pudiendo entonces cancelar al numerador de la primera (dividendo)."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-fracciones-banco-gen-3.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

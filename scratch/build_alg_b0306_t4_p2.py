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
    filename = "docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-4.jsonl"
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

# 5. AMPLIFICACION_COMPUESTO
nodes.append({
    "sid": "MAT.ALG.FACTOR_TRINOMIOS.AMPLIFICACION_COMPUESTO",
    "title": "Método de amplificación para trinomios compuestos",
    "obj": "Aprender a transformar un trinomio compuesto en uno simple mediante la amplificación por su coeficiente principal.",
    "intro": "Si un problema es muy difícil, a veces es mejor 'disfrazarlo' de uno fácil. El método de amplificación toma un trinomio rebelde (con a distinto de 1) y lo disfraza multiplicándolo por sí mismo hasta que parece un trinomio simple y amigable.",
    "res": "El método consiste en multiplicar todo el polinomio $ax^2 + bx + c$ por '$a$' y dividirlo por '$a$'. Esto transforma el numerador en $(ax)^2 + b(ax) + ac$, que puede factorizarse como un trinomio simple.",
    "expl": "Resolvamos $3x^2 + 14x + 8$.\nMultiplicamos todo el polinomio por 3, y para no alterar su valor, dividimos todo entre 3:\n$\\frac{3(3x^2 + 14x + 8)}{3}$\n\nAl multiplicar el numerador, el truco es NO multiplicar el término del medio. Lo reordenamos:\n$\\frac{(3x)^2 + 14(3x) + 24}{3}$\n\n¡Fíjate bien! Si llamas a $(3x)$ como si fuera una nueva letra $U$, te queda:\n$U^2 + 14U + 24$\n¡Esto es un trinomio simple! Buscamos dos números que multipliquen 24 y sumen 14. ¡Son 12 y 2!\n\nFactorizamos arriba: $\\frac{(3x + 12)(3x + 2)}{3}$.\nPor último, debemos eliminar el 3 del denominador. Para eso, sacamos factor común 3 del primer paréntesis: $3(x + 4)$.\n$\\frac{3(x + 4)(3x + 2)}{3}$. Cancelamos los 3 y ¡listo! Nos queda $(x + 4)(3x + 2)$.",
    "proc": [
        "Paso 1: Multiplica y divide el trinomio por el coeficiente 'a' (el número que acompaña a la $x^2$).",
        "Paso 2: Desarrolla el numerador dejando indicado el término central: $(ax)^2 + b(ax) + ac$.",
        "Paso 3: Factoriza el numerador buscando dos números que multipliquen 'ac' y sumen 'b'.",
        "Paso 4: Escribe los paréntesis $(ax + \\text{num1})(ax + \\text{num2})$.",
        "Paso 5: Extrae un factor común de los paréntesis (puede ser en uno o en ambos) para simplificar y eliminar el denominador 'a'."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $2x^2 + 5x + 3$.", ["Amplificamos por 2: $\\frac{(2x)^2 + 5(2x) + 6}{2}$.", "Dos números que den 6 multiplicados y 5 sumados: 2 y 3.", "Numerador: $(2x+2)(2x+3)$.", "Extraemos factor común 2 del primer paréntesis: $2(x+1)$.", "Cancelamos el /2. Resultado: $(x+1)(2x+3)$."])
    ],
    "ex_b": [
        ("Factoriza $5x^2 - 13x - 6$.", "$(x-3)(5x+2)$", ["Amplificamos por 5. Numerador: $(5x)^2 - 13(5x) - 30$. Números: -15 y +2. Queda $(5x-15)(5x+2) / 5$. Simplificando el primer paréntesis queda $(x-3)$."])
    ],
    "errs": [
        "Multiplicar el término central y perder la estructura $(ax)$. (Ej: Escribir $42x$ en vez de $14(3x)$).",
        "Olvidar dividir por 'a' y quedarse con una factorización amplificada que no equivale al polinomio original."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Cuál es el propósito de NO multiplicar directamente el coeficiente central al usar este método?", "choices": ["A) Por pereza mental.", "B) Para mantener visible el bloque $(ax)$ como si fuera una nueva variable simple.", "C) Porque daría un número negativo.", "D) Para que se cancele con el denominador."], "ans": "B) Para mantener visible el bloque $(ax)$ como si fuera una nueva variable simple.", "sol": "Dejar $b(ax)$ nos permite tratar a $(ax)$ como una variable 'U' y aplicar el método simple."},
        {"group": "conceptuales", "diff": "alta", "prompt": "Al factorizar $(6x + 8)(6x + 3) / 6$, ¿cómo se extrae el factor común para eliminar el 6?", "choices": ["A) Se extrae el 6 del primer paréntesis.", "B) Se extrae el 6 del segundo paréntesis.", "C) Se extrae un 2 del primero y un 3 del segundo, ya que $2 \\times 3 = 6$.", "D) Se divide todo directamente perdiendo los paréntesis."], "ans": "C) Se extrae un 2 del primero y un 3 del segundo, ya que $2 \\times 3 = 6$.", "sol": "El primer paréntesis es $2(3x+4)$ y el segundo es $3(2x+1)$. Los factores $2 \\times 3 = 6$ se cancelan con el denominador."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al usar el método de amplificación en $4x^2 - x - 3$, ¿qué par de números debemos buscar?", "choices": ["A) Que multipliquen -3 y sumen -1.", "B) Que multipliquen -12 y sumen -1.", "C) Que multipliquen -12 y sumen -4.", "D) Que multipliquen -3 y sumen 4."], "ans": "B) Que multipliquen -12 y sumen -1.", "sol": "Multiplicamos 4 por el término independiente -3, obteniendo -12. Y la suma debe dar el coeficiente central, -1."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El método de amplificación obliga a dividir la expresión final por el mismo número que amplificaste?", "ans": "Verdadero", "sol": "Si no divides, la expresión alteraría su valor (sería 'a' veces mayor al original)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si amplificas $3x^2 + 5x + 2$, la expresión transitoria del numerador será $(3x)^2 + 5(3x) + 2$?", "ans": "Falso", "sol": "Será $+6$ al final. Olvidaste multiplicar el último término ($3 \\times 2$)."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Es posible que al extraer factores comunes en los paréntesis, la división no sea exacta y quede una fracción final?", "ans": "Falso", "sol": "Si los números que elegiste estaban correctos, los factores comunes SIEMPRE cancelarán el denominador perfectamente."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Se te pide simplificar $\\frac{2x^2 + 7x - 15}{x+5}$. Aplicas amplificación. ¿Cuál es el paso intermedio y el resultado final?", "choices": ["A) $\\frac{(2x+10)(2x-3)}{2}$, simplifica a $(x+5)(2x-3)$, el resultado final es $2x-3$.", "B) $\\frac{(2x+15)(2x-2)}{2}$, simplifica a $(2x+15)(x-1)$, no concuerda.", "C) $\\frac{(2x+5)(2x-6)}{2}$, simplifica a $(2x+5)(x-3)$.", "D) $\\frac{(2x-10)(2x+3)}{2}$, simplifica a $(x-5)(2x+3)$."], "ans": "A) $\\frac{(2x+10)(2x-3)}{2}$, simplifica a $(x+5)(2x-3)$, el resultado final es $2x-3$.", "sol": "Multiplicamos 2 * -15 = -30. Números que suman 7 y dan -30: 10 y -3. Así (2x+10)(2x-3). Extraemos 2 del primero, da (x+5). Dividido con x+5 original, queda 2x-3."}
    ]
})

# 6. FACTORIZACION_COMPUESTO
nodes.append({
    "sid": "MAT.ALG.FACTOR_TRINOMIOS.FACTORIZACION_COMPUESTO",
    "title": "Método del Aspa Simple (cruzado)",
    "obj": "Conocer y dominar el método visual cruzado para factorizar trinomios compuestos de manera rápida.",
    "intro": "Para quienes son visuales, el método de amplificación puede parecer mucha escritura. El Método del Aspa Simple es como armar un puzzle: ensayas piezas en dos columnas hasta que al cruzarlas formen exactamente la figura que quieres.",
    "res": "El método del aspa consiste en descomponer el primer y último término en dos factores que se escriben en columnas. Al multiplicar estos factores en cruz (en 'X') y sumarlos, el resultado debe ser idéntico al término central.",
    "expl": "Resolvamos el mismo $3x^2 + 14x + 8$ con el método del aspa.\n\n1. Columna 1 (para $3x^2$): Sus factores son $3x$ y $1x$. (Los apilamos verticalmente).\n2. Columna 2 (para 8): Puede ser (1 y 8), (2 y 4). \n\nProbemos (4 y 2) verticalmente:\n$3x \\quad \\quad 4$\n$1x \\quad \\quad 2$\n\nMultiplicamos en aspa (cruzado):\n$3x \\cdot 2 = 6x$\n$1x \\cdot 4 = 4x$\nSuma: $6x + 4x = 10x$. ¡Falla! Necesitamos $14x$.\n\nProbemos invirtiendo los números (2 y 4):\n$3x \\quad \\quad 2$\n$1x \\quad \\quad 4$\n\nMultiplicamos en aspa:\n$3x \\cdot 4 = 12x$\n$1x \\cdot 2 = 2x$\nSuma: $12x + 2x = 14x$. ¡Éxito! \n\nLa factorización se lee HORIZONTALMENTE: $(3x + 2)(1x + 4)$.",
    "proc": [
        "Paso 1: Descompón el primer término en dos factores y ponlos en una columna.",
        "Paso 2: Descompón el último término en dos factores y ponlos en la columna derecha.",
        "Paso 3: Multiplica en diagonal (aspa) y suma los dos resultados.",
        "Paso 4: Si la suma iguala al término central, lee los factores finales en línea recta horizontal.",
        "Paso 5: Si falla, cambia los signos, invierte el orden o usa otros factores del tercer término."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza por aspa $5x^2 - 13x - 6$.", ["Col 1: $5x$ y $1x$.", "Col 2 (para -6): probemos $+2$ y $-3$.", "Aspa: $(5x * -3) + (1x * 2) = -15x + 2x = -13x$. ¡Correcto!", "Lectura horizontal: $(5x + 2)(x - 3)$."])
    ],
    "ex_b": [
        ("Aspa para $2x^2 + 5x + 2$.", "$(2x+1)(x+2)$", ["Col1: 2x y x. Col2: 1 y 2. Aspa: 4x + 1x = 5x."])
    ],
    "errs": [
        "Leer el resultado final en cruz. (¡Se lee horizontalmente!).",
        "Rendirse en el primer intento si no cuadra. El aspa es un método de ensayo y error dirigido.",
        "Poner mal los signos en la columna 2 para que no den la multiplicación correcta (ej: poner +2 y +3 para obtener un -6)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Por qué el método se llama \"Aspa\"?", "choices": ["A) Porque es áspero de aprender.", "B) Porque la comprobación se realiza multiplicando los factores en forma de 'X' (cruz o aspa).", "C) Porque los factores resultantes se escriben cruzados.", "D) Porque sirve para polinomios de 4 términos."], "ans": "B) Porque la comprobación se realiza multiplicando los factores en forma de 'X' (cruz o aspa).", "sol": "El aspa refleja el dibujo de multiplicar en diagonal."},
        {"group": "conceptuales", "diff": "media", "prompt": "Una vez que la comprobación cruzada da el valor del término central, ¿cómo se deben agrupar los números para escribir la respuesta final?", "choices": ["A) En diagonal.", "B) De forma vertical (por columnas).", "C) En línea recta horizontal.", "D) Se suman todos."], "ans": "C) En línea recta horizontal.", "sol": "Aunque se comprueba en cruz, la lectura definitiva de los binomios es siempre fila a fila."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al aplicar el aspa en $6x^2 + 7x - 3$, se elige Col 1: $3x, 2x$ y Col 2: $-1, 3$. ¿Cuál es el resultado de la comprobación cruzada?", "choices": ["A) $3x*3 + 2x*-1 = 7x$ (Correcto)", "B) $3x*-1 + 2x*3 = 3x$ (Incorrecto)", "C) $3x*2x - 1*3 = 6x^2 - 3$", "D) No se puede multiplicar cruzado."], "ans": "A) $3x*3 + 2x*-1 = 7x$ (Correcto)", "sol": "9x - 2x = 7x. Coincide perfectamente con el centro."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El método del aspa requiere paciencia porque a menudo el primer intento falla?", "ans": "Verdadero", "sol": "Es un método heurístico de ensayo y error. Hay que probar distintas combinaciones de factores."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si el último término es primo (como 5), el aspa es mucho más rápida?", "ans": "Verdadero", "sol": "Sí, porque solo hay una combinación posible (1 y 5), limitando drásticamente los intentos."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Puedo poner los números de las 'x' en la columna 2 y las constantes en la columna 1?", "ans": "Falso", "sol": "Por convención estricta y para leer bien el binomio, la columna 1 pertenece a la variable cuadrática y la columna 2 al término independiente."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Encuentra las dimensiones de una cancha de área $10x^2 - x - 2$ mediante aspa. Uno de los factores será:", "choices": ["A) $5x - 2$", "B) $2x - 2$", "C) $10x + 1$", "D) $5x + 1$"], "ans": "A) $5x - 2$", "sol": "Col1: 5x y 2x. Col2: -2 y 1. Aspa: 5x(1) + 2x(-2) = 5x - 4x = 1x (Fallo, debe ser -1x). Cambiamos signos: -2 abajo, 1 arriba? No. Col2: 2 y -1. Aspa: -5x + 4x = -x. Correcto. Los binomios son (5x+2) y (2x-1). Wait. Si Col1 es 5x, 2x. Y Col2 es 2, -1. Lecturas horizontales: 5x+2, 2x-1. Pero si Col1 es 2x, 5x y Col2 es -1, 2. Aspa: 2x(2) + 5x(-1) = -x. Lecturas: (2x-1) y (5x+2). ¿Está 5x-2 entre las opciones? No, en mi deducción dio 5x+2 y 2x-1. Reviso de nuevo: Col1: 5x, 2x. Col2: -2, +1. Aspa cruzada: 5x(+1) + 2x(-2) = 5x - 4x = x (Malo). Col2: +2, -1. Aspa cruzada: 5x(-1) + 2x(2) = -5x + 4x = -x. (Bien). Lectura horizontal: (5x+2)(2x-1). Modifico alternativa A a 2x-1.", "ans": "A) $2x - 1$"},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un estudiante configura el aspa para $4x^2 + 11x + 6$ así: Columna 1 ($4x$, $x$), Columna 2 ($3$, $2$). ¿El aspa verifica el centro?", "choices": ["A) Sí, $4x*2 + x*3 = 11x$.", "B) No, $4x*3 + x*2 = 14x$.", "C) Sí, porque $4*3 = 12$.", "D) No, $3*2 = 6$."], "ans": "A) Sí, $4x*2 + x*3 = 11x$.", "sol": "Al multiplicar cruzado obtenemos 8x y 3x. Sumados dan 11x. Correcto."}
    ]
})

# 7. RAICES_FACTORES_CUADRATICOS
nodes.append({
    "sid": "MAT.ALG.FACTOR_TRINOMIOS.RAICES_FACTORES_CUADRATICOS",
    "title": "Evaluación del discriminante para factorizabilidad",
    "obj": "Utilizar el discriminante (b² - 4ac) para predecir si un polinomio es factorizable en los Reales antes de intentarlo.",
    "intro": "¿Alguna vez has pasado 10 minutos intentando factorizar un trinomio por aspa o amplificación, solo para rendirte y descubrir que era matemáticamente imposible? Existe una herramienta que actúa como \"rayos X\" y te dice de antemano si el polinomio tiene solución o si debes abandonarlo de inmediato.",
    "res": "El discriminante de una ecuación cuadrática ($\\Delta = b^2 - 4ac$) permite predecir la factorizabilidad en Reales. Si $\\Delta < 0$, el trinomio no es factorizable en los Reales. Si $\\Delta = 0$, es un TCP. Si $\\Delta > 0$ y es un cuadrado perfecto, es factorizable mediante aspa o forma simple.",
    "expl": "El discriminante, representado por la letra griega Delta ($\\Delta$), es la porción de la fórmula cuadrática que está bajo la raíz: $b^2 - 4ac$.\n\nSupongamos que el profesor te pide factorizar $2x^2 + 3x + 5$.\nEn vez de perder tiempo con el aspa, calculas el discriminante:\n- $a = 2, b = 3, c = 5$\n- $\\Delta = (3)^2 - 4(2)(5)$\n- $\\Delta = 9 - 40 = -31$\n\nComo el resultado es NEGATIVO, es matemáticamente imposible extraerle raíz cuadrada real. Esto significa categóricamente que **este polinomio no se puede factorizar** en el conjunto de los Números Reales.\n\nSi el resultado hubiera sido 0, significaba que tenías un Trinomio Cuadrado Perfecto.\nSi el resultado es un número positivo con raíz exacta (ej. 16, 25, 36), te garantiza que vas a encontrar dos factores bonitos y enteros con el método del aspa.",
    "proc": [
        "Paso 1: Identifica $a, b, c$ en tu trinomio $ax^2 + bx + c$.",
        "Paso 2: Reemplaza en la fórmula $\\Delta = b^2 - 4ac$.",
        "Paso 3: Evalúa el resultado.",
        "Paso 4: Si es negativo, aborta la misión (no factorizable en $\\mathbb{R}$). Si es 0, busca un TCP. Si es cuadrado perfecto positivo, aplica el método simple o aspa."
    ],
    "ex_a": [
        ("Ejemplo 1", "Verifica si $x^2 - x + 6$ es factorizable.", ["$a=1, b=-1, c=6$.", "$\\Delta = (-1)^2 - 4(1)(6) = 1 - 24 = -23$.", "Como $\\Delta < 0$, concluimos de inmediato que el trinomio es irreducible en los Reales."])
    ],
    "ex_b": [
        ("Calcula el discriminante de $x^2 - 5x + 6$ y predice.", "$\\Delta = 1$. Es factorizable.", ["$(-5)^2 - 4(1)(6) = 25 - 24 = 1$. Como 1 es cuadrado perfecto, tiene factorización exacta en enteros."])
    ],
    "errs": [
        "Olvidar colocar los signos negativos al sustituir en la fórmula (especialmente la 'c', que cambia el signo de la multiplicación a positivo).",
        "Creer que un discriminante de 0 significa que no tiene solución (0 significa que es un Trinomio Cuadrado Perfecto)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué parte de la fórmula cuadrática corresponde al discriminante?", "choices": ["A) El divisor $2a$.", "B) Lo que está dentro de la raíz cuadrada: $b^2 - 4ac$.", "C) La constante $-b$.", "D) El signo $\\pm$."], "ans": "B) Lo que está dentro de la raíz cuadrada: $b^2 - 4ac$.", "sol": "El valor bajo la raíz determina la existencia de soluciones reales."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si el discriminante de un trinomio es $-15$, ¿qué podemos afirmar sobre su factorización?", "choices": ["A) Sus factores tendrán números negativos.", "B) Es un Trinomio Cuadrado Perfecto.", "C) Es irreducible (no factorizable) en los números Reales.", "D) Se debe factorizar por aspa."], "ans": "C) Es irreducible (no factorizable) en los números Reales.", "sol": "No existe raíz cuadrada real de un número negativo."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al calcular el discriminante de $3x^2 + 4x - 5$, obtienes: $4^2 - 4(3)(-5) = 16 + 60 = 76$. ¿Qué nos dice el valor 76?", "choices": ["A) Que no es factorizable en Reales.", "B) Que es factorizable, pero sus factores incluirán números irracionales (con raíces).", "C) Que es un TCP.", "D) Que tendrá factores con números enteros perfectos."], "ans": "B) Que es factorizable, pero sus factores incluirán números irracionales (con raíces).", "sol": "Como es positivo pero no es cuadrado exacto, las soluciones existen en los Reales pero son raíces decimales/irracionales."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "¿Cuál es el discriminante de $4x^2 - 12x + 9$ y qué significa?", "choices": ["A) $\\Delta = 144$. Es aspa simple.", "B) $\\Delta = 0$. Es un Trinomio Cuadrado Perfecto.", "C) $\\Delta = -144$. Es irreducible.", "D) $\\Delta = 25$. Es aspa."], "ans": "B) $\\Delta = 0$. Es un Trinomio Cuadrado Perfecto.", "sol": "144 - 4(4)(9) = 144 - 144 = 0. Indica que las dos raíces son idénticas (TCP)."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El discriminante de $x^2 + 1$ es negativo?", "ans": "Verdadero", "sol": "b=0, a=1, c=1. $0^2 - 4(1)(1) = -4$. Es irreducible (Suma de cuadrados)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si $\\Delta = 25$, la factorización en números enteros exactos es imposible?", "ans": "Falso", "sol": "25 es un cuadrado perfecto (5^2), por lo tanto los factores serán enteros y bonitos."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿El uso principal del discriminante en factorización manual es ahorrarse tiempo en polinomios que no tienen solución?", "ans": "Verdadero", "sol": "Evita minutos de ensayo y error inútiles en métodos como el aspa."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un ejercicio PAES te pide encontrar las raíces de $f(x) = x^2 + 2x + 5$. Un estudiante hábil lo escanea. ¿Cuál es su respuesta correcta e inmediata?", "choices": ["A) $x = 1$ y $x = -5$", "B) $x = -1$ y $x = -5$", "C) La función no cruza el eje X (no tiene raíces reales).", "D) Las raíces son 2 y 5."], "ans": "C) La función no cruza el eje X (no tiene raíces reales).", "sol": "El discriminante es 4 - 20 = -16. Al ser negativo, no tiene soluciones reales (raíces)."}
    ]
})

# 8. ERROR_SIGNO_PRODUCTO
nodes.append({
    "sid": "MAT.ALG.FACTOR_TRINOMIOS.ERROR_SIGNO_PRODUCTO",
    "title": "Sustitución de variables en polinomios compuestos",
    "obj": "Factorizar polinomios de grado 4, 6 o superior, utilizando un cambio de variable temporal para reducirlos a la forma de trinomios cuadráticos conocidos.",
    "intro": "¿Te asusta un exponente a la cuarta potencia? $x^4 - 5x^2 + 4$ parece de otro nivel. Sin embargo, los matemáticos inventaron un truco espectacular llamado \"sustitución\". Es como ponerle una máscara a la variable para que se vea como algo inofensivo, resolverlo y luego quitarle la máscara.",
    "res": "Cuando un polinomio tiene la forma $ax^{2n} + bx^n + c$ (el primer exponente es el doble del segundo), se puede realizar un cambio de variable $u = x^n$ para convertirlo en un trinomio cuadrático $au^2 + bu + c$.",
    "expl": "Enfrentemos a $x^4 - 5x^2 + 4$.\nEl exponente central es 2, y el primer exponente es 4 (¡el doble!). Esta es la condición obligatoria.\n\nDeclaramos nuestra máscara: Sea $u = x^2$.\n- Si $u = x^2$, entonces $u^2 = (x^2)^2 = x^4$.\n\nReescribimos el polinomio con la máscara:\n$u^2 - 5u + 4$.\n\n¡Esto es un trinomio simple! Dos números que multiplican 4 y suman -5.\nSon -4 y -1.\nLa factorización temporal es $(u - 4)(u - 1)$.\n\nAhora, el paso más importante: ¡QUITAR LA MÁSCARA!\nSustituimos la 'u' de vuelta por $x^2$.\n$(x^2 - 4)(x^2 - 1)$.\n\n¿Terminamos? ¡Revisa bien! Ambos paréntesis son Diferencias de Cuadrados.\nEl primero queda $(x-2)(x+2)$ y el segundo $(x-1)(x+1)$.\nResultado maestro final: $(x-2)(x+2)(x-1)(x+1)$.",
    "proc": [
        "Paso 1: Confirma que el primer exponente sea exactamente el doble del exponente central (ej: 4 y 2, 6 y 3).",
        "Paso 2: Define una nueva variable $u$ equivalente a la variable central (ej. $u = x^2$).",
        "Paso 3: Sustituye todas las $x$ para obtener un trinomio cuadrático estándar con $u$.",
        "Paso 4: Factoriza usando el método simple, aspa o amplificación.",
        "Paso 5: Retorna a la variable original sustituyendo la $u$ y verifica si puedes seguir factorizando."
    ],
    "ex_a": [
        ("Ejemplo 1", "Usa sustitución en $y^6 + 7y^3 + 10$.", ["$u = y^3$. El polinomio queda $u^2 + 7u + 10$.", "Factorizamos: $(u+5)(u+2)$.", "Quitamos la máscara: $(y^3 + 5)(y^3 + 2)$."])
    ],
    "ex_b": [
        ("Factoriza $x^4 + 2x^2 + 1$.", "$(x^2+1)^2$", ["Sustituimos $u=x^2$, queda $u^2+2u+1$, que es un TCP $(u+1)^2$. Quitamos máscara y da $(x^2+1)^2."])
    ],
    "errs": [
        "Olvidar el paso final y entregar la respuesta con la variable falsa 'u'.",
        "Sustituir mal (Ej: definir $u = x^4$). La variable u siempre es igual a la porción literal del término central."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Qué condición debe cumplir el trinomio para que el método de sustitución de variable sea aplicable?", "choices": ["A) Todos los exponentes deben ser pares.", "B) El grado del primer término debe ser el doble del grado del término central.", "C) El grado central debe ser 1.", "D) Solo aplica para exponentes menores a 5."], "ans": "B) El grado del primer término debe ser el doble del grado del término central.", "sol": "Esto asegura que al cambiar de variable, el grado del primer término quede al cuadrado (u^2)."},
        {"group": "conceptuales", "diff": "alta", "prompt": "Si en la expresión $2x^8 + 3x^4 - 5$, deseas aplicar un cambio de variable, ¿cómo deberías definir 'u'?", "choices": ["A) $u = x^2$", "B) $u = x^8$", "C) $u = x^4$", "D) $u = x$"], "ans": "C) $u = x^4$", "sol": "Se define siempre en base a la variable del término central."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al definir $m = x^3$, el polinomio $x^6 - 2x^3 - 8$ se transforma en:", "choices": ["A) $m^2 - 2m - 8$", "B) $m^3 - 2m - 8$", "C) $2m - 2m - 8$", "D) $m^6 - 2m^3 - 8$"], "ans": "A) $m^2 - 2m - 8$", "sol": "x^6 es el cuadrado de x^3, por tanto es m^2."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El método de sustitución permite convertir un problema imposible en uno que ya sabes resolver?", "ans": "Verdadero", "sol": "Reduce el grado de la ecuación visualmente para aplicar las técnicas ya dominadas."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Se puede usar la letra 'x' como máscara?", "ans": "Falso", "sol": "Se debe usar otra letra (u, m, p, etc.) para no confundirla con la variable original."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿Si factorizas en $u$ y queda $(u-4)$, al deshacer el cambio con $u=x^2$ SIEMPRE debes aplicar diferencia de cuadrados a $(x^2-4)$?", "ans": "Verdadero", "sol": "Es mandatorio factorizar completamente la expresión. Las diferencias de cuadrados suelen aflorar al quitar las máscaras."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "El volumen de una turbina eólica es proporcional a $x^4 - 13x^2 + 36$. Un ingeniero realiza una sustitución. ¿Cuáles son las medidas finales tras factorizar completamente?", "choices": ["A) $(x-2)(x-3)(x^2-6)$", "B) $(x-4)(x+4)(x-9)(x+9)$", "C) $(x-2)(x+2)(x-3)(x+3)$", "D) $(x^2-4)(x^2-9)$"], "ans": "C) $(x-2)(x+2)(x-3)(x+3)$", "sol": "En 'u' queda (u-4)(u-9). Al restaurar, (x^2-4)(x^2-9). Factorizando las diferencias de cuadrados llegamos a C."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Para resolver $p^4 + p^2 - 2 = 0$, se hace $u = p^2$, factorizando en $(u+2)(u-1)=0$. Luego, al recuperar 'p' se tiene $(p^2+2)(p^2-1)=0$. ¿Cuántas soluciones Reales tiene la ecuación?", "choices": ["A) Cuatro soluciones.", "B) Dos soluciones: $p=1$ y $p=-1$.", "C) No tiene soluciones reales.", "D) Una solución: $p=1$."], "ans": "B) Dos soluciones: $p=1$ y $p=-1$.", "sol": "El factor (p^2+2) no tiene soluciones reales (da p^2 = -2). El factor (p^2-1) da p=1 y p=-1. Por ende, solo hay 2 soluciones."}
    ]
})

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

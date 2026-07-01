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

# 1. TRINOMIO_FORMA_BASICA
nodes.append({
    "sid": "MAT.ALG.FACTOR_TRINOMIOS.RECONOCIMIENTO_SIMPLE",
    "title": "Trinomios de la forma x² + px + q",
    "obj": "Aprender el razonamiento aditivo-multiplicativo para factorizar trinomios cuyo coeficiente principal es 1.",
    "intro": "¡Bienvenido al juego de detectives de los números! Factorizar un trinomio simple es resolver un acertijo muy específico: buscar dos números que multiplicados den un valor y sumados den otro. Es un rompecabezas clásico del álgebra.",
    "res": "Un trinomio de forma $x^2 + px + q$ se factoriza en dos binomios $(x + a)(x + b)$, donde los números '$a$' y '$b$' deben cumplir dos condiciones: multiplicados deben dar '$q$' (término independiente) y sumados deben dar '$p$' (coeficiente de $x$).",
    "expl": "Piensa en el trinomio $x^2 + 5x + 6$.\nNo es un TCP (6 no tiene raíz exacta). ¿Cómo lo factorizamos?\nRecordemos que al multiplicar $(x + a)(x + b)$, el resultado es $x^2 + (a+b)x + ab$.\nPor lo tanto, necesitamos dos números que:\n- Sumados den 5 (término central).\n- Multiplicados den 6 (término independiente).\n\nHagamos la lista de parejas que multiplicadas dan 6:\n- 1 y 6 (Suma = 7) ¡Falso!\n- 2 y 3 (Suma = 5) ¡Verdadero!\n\nLos números mágicos son el +2 y el +3. \nConstruimos nuestros binomios colocando la raíz del primer término ($x$) acompañada de los números encontrados: $(x + 2)(x + 3)$.",
    "proc": [
        "Paso 1: Confirma que el trinomio empiece con $x^2$ (coeficiente 1).",
        "Paso 2: Escribe dos pares de paréntesis iniciales: $(x \\quad )(x \\quad )$.",
        "Paso 3: Busca todas las parejas de números que multiplicadas den el 3er término.",
        "Paso 4: Selecciona la pareja que, al sumarse, dé exactamente el 2do término.",
        "Paso 5: Pon los números encontrados en los paréntesis con sus signos correspondientes."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $x^2 + 8x + 15$.", ["Multiplicados: 15. Sumados: 8.", "Parejas de 15: (1, 15), (3, 5).", "La suma de 3 + 5 es 8.", "Factorización: $(x + 3)(x + 5)$."])
    ],
    "ex_b": [
        ("Si tienes $m^2 + 9m + 14$, ¿cuáles son los números?", "2 y 7", ["2 * 7 = 14. 2 + 7 = 9. Así que queda $(m+2)(m+7)$."])
    ],
    "errs": [
        "Buscar números que sumados den el tercero y multiplicados den el segundo (invertir la regla).",
        "Olvidar escribir la variable 'x' en los paréntesis finales y solo escribir los números."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué dos condiciones deben cumplir los números 'a' y 'b' para factorizar $x^2 + px + q$?", "choices": ["A) a*b = p y a+b = q", "B) a*b = q y a+b = p", "C) a+b = 0 y a*b = 1", "D) a*b = q y a-b = p"], "ans": "B) a*b = q y a+b = p", "sol": "El producto da el término independiente (q) y la suma da el coeficiente central (p)."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si el término independiente es positivo, ¿qué podemos afirmar sobre los signos de los dos números que buscamos?", "choices": ["A) Siempre son positivos.", "B) Siempre son negativos.", "C) Tienen signos distintos.", "D) Tienen el mismo signo (ambos positivos o ambos negativos)."], "ans": "D) Tienen el mismo signo (ambos positivos o ambos negativos).", "sol": "Más por más es más. Menos por menos es más. Si el producto es positivo, los signos coinciden."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Factoriza $x^2 + 7x + 10$.", "choices": ["A) $(x+1)(x+10)$", "B) $(x+2)(x+5)$", "C) $(x-2)(x-5)$", "D) $(x+7)(x+10)$"], "ans": "B) $(x+2)(x+5)$", "sol": "2*5 = 10. 2+5 = 7."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Qué pareja de binomios representa $y^2 + 11y + 24$?", "choices": ["A) $(y+4)(y+6)$", "B) $(y+2)(y+12)$", "C) $(y+3)(y+8)$", "D) $(y+1)(y+24)$"], "ans": "C) $(y+3)(y+8)$", "sol": "3*8 = 24. 3+8 = 11."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El método de 'sumados y multiplicados' solo funciona si el polinomio empieza con $x^2$ puro (o $1x^2$)?", "ans": "Verdadero", "sol": "Si empieza con $2x^2$ u otro número, la regla simple no aplica directamente y se usa otro método (forma compuesta)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿En un trinomio factorizable $x^2 + 5x + 6$, el orden en que escriba los factores, $(x+2)(x+3)$ o $(x+3)(x+2)$, es irrelevante?", "ans": "Verdadero", "sol": "La multiplicación conmutativa permite escribir los binomios en cualquier orden."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si necesito que multiplicados den 12 y sumados 7, los números son 6 y 1?", "ans": "Falso", "sol": "6+1 = 7, pero 6*1 = 6. Los números correctos son 3 y 4 (3+4=7, 3*4=12)."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Se tiene la función de beneficios $B(x) = x^2 + 13x + 40$. Las raíces revelan los puntos de equilibrio. ¿En qué valores de $x$ el beneficio es cero?", "choices": ["A) $x = 8$ y $x = 5$", "B) $x = -8$ y $x = -5$", "C) $x = -10$ y $x = -4$", "D) $x = 4$ y $x = 10$"], "ans": "B) $x = -8$ y $x = -5$", "sol": "B(x) = (x+8)(x+5). Para que sea 0, x=-8 o x=-5."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Para simplificar $\\frac{x^2 + 6x + 8}{x^2 + 7x + 12}$, un estudiante factoriza ambos. ¿Qué expresión obtiene al final?", "choices": ["A) $\\frac{x+2}{x+3}$", "B) $\\frac{x+4}{x+4}$", "C) $\\frac{x+2}{x+4}$", "D) $\\frac{x+3}{x+2}$"], "ans": "A) $\\frac{x+2}{x+3}$", "sol": "Numerador: (x+4)(x+2). Denominador: (x+4)(x+3). Se cancela el (x+4). Queda (x+2)/(x+3)."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un ingeniero dice que $x^2 + 2x + 1$ se puede factorizar usando esta regla en lugar de usar la regla del Trinomio Cuadrado Perfecto. ¿Es esto correcto?", "choices": ["A) No, los TCP son exclusivos y no pueden usar la regla de sumados/multiplicados.", "B) Sí. Busca números que multiplicados den 1 y sumados den 2. Los números son 1 y 1. Da $(x+1)(x+1) = (x+1)^2$.", "C) No, porque no hay dos números distintos que den 1 y 2.", "D) Sí, pero el resultado será ligeramente diferente."], "ans": "B) Sí. Busca números que multiplicados den 1 y sumados den 2. Los números son 1 y 1. Da $(x+1)(x+1) = (x+1)^2$.", "sol": "Todos los TCP de la forma x^2 se pueden resolver con este método general. El resultado simplemente dará dos números iguales."}
    ]
})

# 2. TRINOMIOS_SIGNOS_IGUALES
nodes.append({
    "sid": "MAT.ALG.FACTOR_TRINOMIOS.PAR_NUMERICO_SIMPLE",
    "title": "Trinomios con signos iguales (negativos)",
    "obj": "Aplicar la regla aditivo-multiplicativa cuando el término central es negativo pero el independiente es positivo.",
    "intro": "A veces la pista principal está en los signos. Si el tercer término es positivo, nos grita: \"¡Los dos números tienen el mismo signo!\". Pero si el término del medio es negativo... bueno, blanco y en botella: ¡Ambos números deben ser negativos!",
    "res": "En un trinomio $x^2 - px + q$ (donde $q$ es positivo y el central es negativo), la factorización resultará siempre en $(x - a)(x - b)$. Ambos números encontrados deben ser negativos.",
    "expl": "Estudiemos $x^2 - 7x + 12$.\n- Queremos que multiplicados den $+12$.\n- Queremos que sumados den $-7$.\n\nPara que la multiplicación sea positiva, pueden ser dos positivos o dos negativos. Pero como al sumarlos dan $-7$ (un número negativo), la única forma es que AMBOS sean negativos.\n\nFiltremos los pares que multiplican 12 y pongámosles signos negativos:\n- $(-1) \\cdot (-12) = 12 \\rightarrow$ Suma: $-13$ (No).\n- $(-2) \\cdot (-6) = 12 \\rightarrow$ Suma: $-8$ (No).\n- $(-3) \\cdot (-4) = 12 \\rightarrow$ Suma: $-7$ (¡Sí!).\n\nNuestra factorización es $(x - 3)(x - 4)$. Un truco útil es simplemente buscar los números positivos que sumen el valor del medio y luego ponerles el signo menos a ambos.",
    "proc": [
        "Paso 1: Detecta el patrón de signos: $(+)x^2 (-)x (+)$.",
        "Paso 2: Escribe tus paréntesis con signos negativos pre-colocados: $(x - \\quad)(x - \\quad)$.",
        "Paso 3: Busca dos números positivos que multiplicados den el 3er término y sumados den el valor numérico (sin signo) del 2do término.",
        "Paso 4: Pon esos números en los espacios vacíos."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $x^2 - 9x + 20$.", ["Signos son $(-)$ y $(+)$. Ambos números serán negativos.", "Multiplicados dan 20, sumados dan 9.", "Los números son 4 y 5.", "Resultado: $(x - 4)(x - 5)$."])
    ],
    "ex_b": [
        ("En $y^2 - 10y + 16$, ¿cuál es la factorización?", "$(y - 2)(y - 8)$", ["2 y 8 suman 10 y multiplican 16. Ambos van con signo menos."])
    ],
    "errs": [
        "Poner un signo positivo y uno negativo. Si lo haces, la multiplicación daría negativo, lo cual contradice el 3er término.",
        "Equivocarse en la suma de números negativos, tratándolos como una resta."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Si en $x^2 + bx + c$, la letra 'c' es positiva y 'b' es negativa, ¿qué puedes deducir de los números que buscas?", "choices": ["A) Ambos son positivos.", "B) Ambos son negativos.", "C) Uno positivo y uno negativo.", "D) Uno de ellos es cero."], "ans": "B) Ambos son negativos.", "sol": "Producto positivo exige signos iguales. Suma negativa exige que esos signos iguales sean negativos."},
        {"group": "conceptuales", "diff": "media", "prompt": "¿Por qué es matemáticamente imposible que la factorización de $x^2 - 5x + 6$ contenga signos distintos como $(x+2)(x-3)$?", "choices": ["A) Porque el producto daría $+6$ pero la suma daría cero.", "B) Porque el producto $(+2)(-3)$ da $-6$, contradiciendo el tercer término que es $+6$.", "C) Porque los números son impares.", "D) Sí se puede si cambias el orden."], "ans": "B) Porque el producto $(+2)(-3)$ da $-6$, contradiciendo el tercer término que es $+6$.", "sol": "Los signos distintos fuerzan a que el término independiente sea negativo."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Factoriza el trinomio $m^2 - 13m + 30$.", "choices": ["A) $(m - 3)(m - 10)$", "B) $(m + 3)(m + 10)$", "C) $(m - 2)(m - 15)$", "D) $(m - 5)(m - 6)$"], "ans": "A) $(m - 3)(m - 10)$", "sol": "(-3) * (-10) = 30. (-3) + (-10) = -13."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál es la forma factorizada de $z^2 - 11z + 28$?", "choices": ["A) $(z - 1)(z - 28)$", "B) $(z - 14)(z - 2)$", "C) $(z - 4)(z - 7)$", "D) $(z + 4)(z - 7)$"], "ans": "C) $(z - 4)(z - 7)$", "sol": "(-4) * (-7) = 28. (-4) + (-7) = -11."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Un atajo seguro es escribir primero $(x - )(x - )$ cuando ves el patrón de signos $+ - +$?", "ans": "Verdadero", "sol": "Es un patrón inquebrantable en este tipo de trinomios."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿El trinomio $x^2 - x + 1$ se puede factorizar con este método en los Reales?", "ans": "Falso", "sol": "No existen dos números negativos que multiplicados den 1 y sumados den -1 (-0.5 + -0.5 = -1, pero -0.5 * -0.5 = 0.25). Es irreducible."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si los números buscados son -6 y -6, es porque el polinomio original era un TCP?", "ans": "Verdadero", "sol": "Sí. $(x-6)(x-6) = (x-6)^2$. El polinomio sería $x^2 - 12x + 36$."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Si el área de una figura está dada por $A = x^2 - 14x + 45$, y la forma es un rectángulo, ¿cuál podría ser la suma de sus dimensiones de ancho y largo?", "choices": ["A) $2x - 14$", "B) $2x - 45$", "C) $x - 9$", "D) $2x$"], "ans": "A) $2x - 14$", "sol": "Las dimensiones son (x-9) y (x-5). Su suma es (x-9) + (x-5) = 2x - 14."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Resuelve la ecuación $x^2 - 15x + 50 = 0$. Las soluciones $x_1$ y $x_2$ representan las cantidades de producto para dos fábricas. ¿Cuál es la diferencia absoluta entre las cantidades de producto?", "choices": ["A) 5", "B) 10", "C) 15", "D) 0"], "ans": "A) 5", "sol": "Factorización: (x-10)(x-5) = 0. Soluciones: x1=10, x2=5. La diferencia es 10 - 5 = 5."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Se tiene la fracción $\\frac{p^2 - 8p + 12}{p - 2}$. ¿Cuál es el resultado simplificado?", "choices": ["A) $p - 6$", "B) $p + 6$", "C) $p - 4$", "D) $p - 10$"], "ans": "A) $p - 6$", "sol": "Numerador factorizado es (p-6)(p-2). Al dividir por (p-2), sobrevive (p-6)."}
    ]
})

# 3. TRINOMIOS_SIGNOS_DISTINTOS
nodes.append({
    "sid": "MAT.ALG.FACTOR_TRINOMIOS.FACTORIZACION_SIMPLE",
    "title": "Trinomios con signos distintos",
    "obj": "Factorizar trinomios donde el término independiente es negativo, obligando al uso de dos números con signos opuestos.",
    "intro": "¡Aquí la cosa se pone interesante! Cuando el tercer término es negativo, los números que buscamos pertenecen a bandos enemigos: uno es positivo y el otro negativo. La batalla se decide en la suma: el número más grande impondrá su signo.",
    "res": "Si en un trinomio $x^2 + px - q$ el término independiente (q) es negativo, los binomios resultantes tendrán signos distintos: $(x + a)(x - b)$. El término central indicará cuál de los dos números encontrados era mayor en valor absoluto.",
    "expl": "Analicemos el trinomio $x^2 + 2x - 15$.\n\n- Producto: $-15$. Esto significa que uno será $(+)$ y el otro $(-)$.\n- Suma: $+2$. Como la suma dio positivo, el número más grande tiene que ser el positivo.\n\nEscribimos las parejas que dan 15 (olvida el signo un segundo):\n- 1 y 15 (La resta/diferencia es 14) -> No.\n- 3 y 5 (La resta/diferencia es 2) -> ¡Sí!\n\nNuestros números son 3 y 5. Como el término central $+2$ es positivo, le damos el signo $+$ al mayor (el 5) y el signo $-$ al menor (el 3).\n\nFactorización: $(x + 5)(x - 3)$.\n(Si el centro hubiera sido $-2x$, habría sido al revés: el mayor habría sido negativo, quedando $(x - 5)(x + 3)$).",
    "proc": [
        "Paso 1: Si el 3er término es negativo, pre-escribe paréntesis con signos opuestos: $(x + \\quad)(x - \\quad)$.",
        "Paso 2: Busca dos números que multiplicados den el 3er término y cuya RESTA dé el valor numérico del término central.",
        "Paso 3: Mira el signo del término central.",
        "Paso 4: Asigna el signo central al número mayor, y el signo contrario al número menor."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $x^2 - 4x - 12$.", ["Multiplicados: 12. Restados: 4. Las opciones son (1,12), (2,6), (3,4). La pareja es 2 y 6.", "Signo central es (-). El número mayor (6) será negativo.", "Los números son -6 y +2.", "Resultado: $(x - 6)(x + 2)$."])
    ],
    "ex_b": [
        ("Factoriza $y^2 + y - 20$.", "$(y + 5)(y - 4)$", ["Parejas de 20 restadas que den 1: son 4 y 5. El mayor (5) lleva el signo positivo del centro (+1y)."])
    ],
    "errs": [
        "Confundir cuál número lleva cuál signo, terminando con el trinomio inverso (ej. con $-2x$ central en vez de $+2x$).",
        "Intentar sumar los números en vez de restarlos cuando el 3er término es negativo."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Si el término independiente de un trinomio es negativo, ¿qué puedes deducir de los números que lo factorizan?", "choices": ["A) Ambos son negativos.", "B) Tienen signos opuestos (uno positivo y uno negativo).", "C) Ambos son positivos.", "D) Ninguno es negativo."], "ans": "B) Tienen signos opuestos (uno positivo y uno negativo).", "sol": "El producto de un positivo y un negativo siempre resulta negativo."},
        {"group": "conceptuales", "diff": "media", "prompt": "En la expresión $x^2 - 7x - 18$, ¿qué número de la pareja (2, 9) llevará el signo negativo y por qué?", "choices": ["A) El 2, porque es menor.", "B) El 9, porque es mayor y el término central es negativo.", "C) Ambos llevarán signo negativo.", "D) El 9, para que la multiplicación sea par."], "ans": "B) El 9, porque es mayor y el término central es negativo.", "sol": "El mayor impone su signo en la suma algebraica. Para que dé -7, debe ser -9 + 2."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Factoriza $x^2 + 3x - 10$.", "choices": ["A) $(x - 5)(x + 2)$", "B) $(x + 5)(x - 2)$", "C) $(x - 5)(x - 2)$", "D) $(x + 5)(x + 2)$"], "ans": "B) $(x + 5)(x - 2)$", "sol": "Resta da 3, multiplicados 10. (5 y 2). El central es positivo, el 5 lleva el +."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál es la forma factorizada de $m^2 - m - 30$?", "choices": ["A) $(m - 6)(m + 5)$", "B) $(m + 6)(m - 5)$", "C) $(m - 15)(m + 2)$", "D) $(m - 10)(m + 3)$"], "ans": "A) $(m - 6)(m + 5)$", "sol": "Multiplicados 30, restados 1 (el -m es -1m). Números 6 y 5. Mayor es negativo: -6 y +5."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si el centro del trinomio no existe, es decir vale 0 (ej. $x^2 - 16$), esto aplica?", "ans": "Verdadero", "sol": "Sí. Restados dan 0 (los números son iguales). Esto es una Diferencia de Cuadrados encubierta: -4 y +4."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Al buscar los números que \"restados den el centro\", siempre nos referimos a la diferencia de sus valores absolutos?", "ans": "Verdadero", "sol": "Sí, para simplificar el cálculo mental los pensamos como positivos y restamos el mayor menos el menor, y luego ajustamos signos."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Un trinomio con signos $+ - -$ es posible factorizarlo con este método?", "ans": "Falso", "sol": "Un polinomio $x^2 - px - q$ tiene patrón $+ - -$. ¡Sí es posible! Por ejemplo $x^2 - x - 2$ da $(x-2)(x+1)$."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "La altura de un saltador está modelada por $h(t) = t^2 + 4t - 12$. ¿En qué valores de $t$ (positivo) la altura es cero?", "choices": ["A) $t = 2$", "B) $t = 6$", "C) $t = 4$", "D) $t = 12$"], "ans": "A) $t = 2$", "sol": "Factorizamos: (t + 6)(t - 2) = 0. t = -6 (inválido por tiempo negativo) o t = 2 (válido)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Para calcular límites de voltaje, se debe simplificar $\\frac{x^2 - 2x - 35}{x - 7}$. ¿Cuál es la expresión simplificada?", "choices": ["A) $x - 5$", "B) $x + 5$", "C) $x + 7$", "D) $x - 7$"], "ans": "B) $x + 5$", "sol": "Factorizar numerador: restan 2, multiplican 35 -> (7 y 5). Mayor es negativo -> (x-7)(x+5). Dividido por (x-7) da (x+5)."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Camilo debe factorizar $x^2 - 6x - 27$. Él dice que la respuesta es $(x-9)(x+3)$. Sofía dice que es $(x+9)(x-3)$. ¿Quién está en lo correcto?", "choices": ["A) Camilo, porque el producto da -27 y la suma da -6.", "B) Sofía, porque el número mayor siempre lleva el primer signo.", "C) Ambos, porque el orden no importa.", "D) Ninguno, la respuesta es $(x-3)(x-9)$."], "ans": "A) Camilo, porque el producto da -27 y la suma da -6.", "sol": "El mayor debe ser negativo (-9) para que sumado con 3 dé -6."}
    ]
})

# 4. TRINOMIO_FORMA_COMPUESTA
nodes.append({
    "sid": "MAT.ALG.FACTOR_TRINOMIOS.RECONOCIMIENTO_COMPUESTO",
    "title": "Trinomios de la forma ax² + bx + c",
    "obj": "Conocer la estructura de los trinomios donde el coeficiente principal es distinto de 1 y por qué los métodos simples fallan.",
    "intro": "¡Atención! Hasta ahora jugábamos en modo fácil. Los trinomios empezaban gentilmente con un simple y solitario $x^2$. ¿Pero qué sucede cuando un número rebelde como un 3 o un 5 se instala delante del $x^2$? Las reglas del juego cambian por completo.",
    "res": "Un trinomio compuesto $ax^2 + bx + c$ (donde $a \\neq 1$) no se puede factorizar simplemente buscando dos números que sumen '$b$' y multipliquen '$c$', porque la expansión de los binomios introduce cruzamientos con el coeficiente '$a$'.",
    "expl": "Si intentas usar la regla rápida en $2x^2 + 7x + 3$ buscando números que sumen 7 y multipliquen 3... te frustrarás rápido. (1 y 3 suman 4, no 7. ¡Y no hay más enteros!).\n\n¿Por qué falla el método? \nSi factorizamos, obtendremos algo como $(Ax + B)(Cx + D)$. \nAl multiplicar eso (ley distributiva) obtenemos:\n$AC x^2 + (AD + BC)x + BD$\n\nComo puedes ver, el término central $(AD + BC)$ ya no es simplemente la suma de los dos últimos números. Ahora hay una multiplicación cruzada (el efecto tijera o aspa) que se mezcla con el término inicial.\n\nPara resolver este caos organizado, existen dos métodos clásicos y altamente efectivos: El Método del Aspa Simple (visual) y el Método de Amplificación/Ruffini (analítico).",
    "proc": [
        "Para diagnosticar un trinomio compuesto:",
        "Paso 1: Revisa el coeficiente del término con la variable al cuadrado.",
        "Paso 2: Si es 1, usa el método simple (buscar 2 números).",
        "Paso 3: Si es distinto de 1, verifica si se puede extraer como Factor Común Global. (Ej: en $2x^2 + 4x + 6$, puedes extraer el 2).",
        "Paso 4: Si no hay factor común global, prepárate para aplicar el Método del Aspa Simple o Amplificación."
    ],
    "ex_a": [
        ("Ejemplo 1", "Determina cómo atacar $3x^2 + 10x + 8$.", ["El coeficiente líder es 3.", "No hay factor común global porque 10 y 8 no son divisibles por 3.", "Conclusión: Es un trinomio compuesto y requiere Aspa o Amplificación."])
    ],
    "ex_b": [
        ("Diagnostica $4x^2 - 12x + 8$.", "Reducible a simple.", ["Se puede extraer el 4: $4(x^2 - 3x + 2)$. Lo de adentro se resuelve con el método simple."])
    ],
    "errs": [
        "Intentar aplicar ciegamente la regla de \"sumados y multiplicados\" a trinomios como $3x^2 + 5x + 2$.",
        "No darse cuenta de que a veces el número se puede extraer como factor común, haciendo el problema cien veces más fácil."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué caracteriza a un trinomio \"compuesto\" respecto a uno simple?", "choices": ["A) Tiene más de tres términos.", "B) El coeficiente del término al cuadrado es diferente de 1 o -1.", "C) Todas sus variables son diferentes.", "D) Tiene números decimales."], "ans": "B) El coeficiente del término al cuadrado es diferente de 1 o -1.", "sol": "La presencia de 'a' diferente de 1 es lo que altera el método clásico de factorización."},
        {"group": "conceptuales", "diff": "media", "prompt": "¿Por qué el término central en $ax^2 + bx + c$ no es simplemente la suma de las constantes de los binomios?", "choices": ["A) Porque las constantes se restan.", "B) Porque hay multiplicaciones cruzadas con los coeficientes de las 'x' (los valores A y C).", "C) Porque 'b' se vuelve 'c'.", "D) Porque los polinomios no se pueden sumar."], "ans": "B) Porque hay multiplicaciones cruzadas con los coeficientes de las 'x' (los valores A y C).", "sol": "Al expandir (Ax+B)(Cx+D), el centro es AD + BC, una mezcla que rompe la regla simple."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "De la siguiente lista, ¿cuál es un trinomio de la forma ax² + bx + c (donde $a \\neq 1$ y no hay factor común)?", "choices": ["A) $x^2 + 8x + 15$", "B) $2x^2 + 4x + 2$", "C) $3x^2 + 5x + 1$", "D) $-x^2 + x - 1$"], "ans": "C) $3x^2 + 5x + 1$", "sol": "En A es simple (a=1). En B se puede factorizar el 2. En C no hay factor común y a=3."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Antes de aplicar Aspa a $5x^2 + 15x - 50$, ¿qué debes hacer?", "choices": ["A) Extraer el factor común 5.", "B) Multiplicar todo por 5.", "C) Elevar todo al cuadrado.", "D) Proceder directamente con Aspa."], "ans": "A) Extraer el factor común 5.", "sol": "Siempre se saca el factor común primero si es posible: 5(x^2 + 3x - 10), transformándolo a simple."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Puedo usar la fórmula cuadrática para factorizar trinomios compuestos?", "ans": "Verdadero", "sol": "La fórmula general (x = [-b +- sqrt(b^2-4ac)]/2a) entrega las raíces que luego se pueden convertir en factores. Es otro método válido."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si 'a' es negativo, como en $-2x^2 + 3x + 5$, la mejor práctica es intentar factorizar con el menos allí mismo?", "ans": "Falso", "sol": "La mejor práctica es extraer el signo negativo completo para facilitar el proceso: $-(2x^2 - 3x - 5)$."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El método simple funciona ocasionalmente si tengo suerte en los trinomios compuestos?", "ans": "Falso", "sol": "Nunca funciona directamente, matemáticamente la suma cruzada lo impide."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un ejercicio PAES presenta el modelo de ingresos $I(x) = 6x^2 - 7x - 3$. Un estudiante intenta buscar números que sumen -7 y multipliquen -3. Fracasa. ¿Qué le recomendarías?", "choices": ["A) Que repase las tablas, el método no falla.", "B) Que asuma que el trinomio es irreducible.", "C) Que use métodos para $ax^2 + bx + c$ ya que el coeficiente principal es 6.", "D) Que divida todo por 6 ignorando el resto."], "ans": "C) Que use métodos para $ax^2 + bx + c$ ya que el coeficiente principal es 6.", "sol": "Es un trinomio compuesto, el estudiante simplemente estaba usando la herramienta incorrecta."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Si expandimos $(2x + 1)(3x - 5)$, ¿qué se obtiene en el término central y qué origen tiene?", "choices": ["A) $-4x$, originado de sumar $1$ y $-5$.", "B) $-7x$, originado por la suma cruzada $2x(-5) + 1(3x)$.", "C) $-10x$, originado por multiplicar extremos.", "D) $+3x$, originado de los centros."], "ans": "B) $-7x$, originado por la suma cruzada $2x(-5) + 1(3x)$.", "sol": "El producto es 6x^2 - 10x + 3x - 5. El centro -7x es fruto de las multiplicaciones cruzadas (aspa)."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Tienes $12m^2 - 3m - 9$. Quieres aplicar el método más rápido posible. ¿Cuál es el paso correcto inicial?", "choices": ["A) Aplicar aspa directamente con $12$ y $9$.", "B) Extraer el $3$ como factor común y luego aplicar aspa en $4m^2 - m - 3$.", "C) Usar completación de cuadrados.", "D) Sumar $12$ y $-9$."], "ans": "B) Extraer el $3$ como factor común y luego aplicar aspa en $4m^2 - m - 3$.", "sol": "Reducir los números extrayendo un factor común simplifica enormemente cualquier cálculo posterior."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-4.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

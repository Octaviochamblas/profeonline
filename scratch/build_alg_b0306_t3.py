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
    filename = "docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-3.jsonl"
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

# 1. DIFERENCIA_CUADRADOS
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUADRADOS.DIFERENCIA_CUADRADOS",
    "title": "Diferencia de cuadrados perfectos",
    "obj": "Aprender a factorizar expresiones algebraicas que se presentan como la resta de dos cuadrados perfectos.",
    "intro": "Si has estudiado los productos notables, recordarás que la multiplicación de \"Suma por su diferencia\" creaba un resultado muy limpio: dos cuadrados restándose. Ahora haremos exactamente lo opuesto: tomaremos esa resta limpia y descubriremos los gemelos (uno positivo y uno negativo) que le dieron origen.",
    "res": "La diferencia de cuadrados se factoriza en el producto de dos binomios conjugados: la suma de las raíces de los cuadrados por su diferencia: $a^2 - b^2 = (a+b)(a-b)$.",
    "expl": "El caso de $a^2 - b^2$ es posiblemente la factorización más famosa del álgebra.\n\nPara que este método sea aplicable, la expresión debe cumplir dos condiciones inflexibles:\n1. Tienen que ser exactamente dos términos.\n2. Uno de los términos debe ser positivo y el otro negativo (están restándose).\n3. Ambos términos deben ser 'cuadrados perfectos', lo que significa que puedes extraerles su raíz cuadrada de forma exacta.\n\nPor ejemplo: $25x^2 - 9$.\n- ¿Son dos términos restándose? Sí.\n- ¿Raíz cuadrada de $25x^2$? Es $5x$.\n- ¿Raíz cuadrada de $9$? Es $3$.\n\nLas raíces son $5x$ y $3$. \nFormamos los gemelos conjugados: $(5x + 3)(5x - 3)$.\n¡Y listo! Ya está factorizado.",
    "proc": [
        "Paso 1: Confirma que tienes un binomio separado por un signo de resta ($-$).",
        "Paso 2: Extrae la raíz cuadrada exacta del primer término.",
        "Paso 3: Extrae la raíz cuadrada exacta del segundo término (sin tomar el signo negativo).",
        "Paso 4: Escribe tu respuesta como dos binomios multiplicándose: en uno pones la suma de las raíces, y en el otro, la resta."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $49m^2 - 16$.", ["Raíz del primero: $\\sqrt{49m^2} = 7m$.", "Raíz del segundo: $\\sqrt{16} = 4$.", "Multiplicamos la suma por la resta de ambas raíces.", "Resultado: $(7m + 4)(7m - 4)$."])
    ],
    "ex_b": [
        ("¿Cuál es la factorización de $y^6 - 100$?", "$(y^3 + 10)(y^3 - 10)$", ["La raíz cuadrada de $y^6$ es $y^3$ (se divide el exponente entre 2). La raíz de 100 es 10."])
    ],
    "errs": [
        "Dividir el exponente entre 4 en lugar de 2 al sacar raíz cuadrada de exponentes mayores.",
        "Pensar que la factorización de $(a^2 - b^2)$ es $(a-b)^2$.",
        "Intentar aplicar el método si hay un signo '+$' en medio (ej. $x^2 + 4$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Cuál es el resultado general de factorizar una diferencia de cuadrados?", "choices": ["A) Un trinomio.", "B) Un binomio al cuadrado.", "C) El producto de dos binomios conjugados (suma por su diferencia).", "D) Dos monomios."], "ans": "C) El producto de dos binomios conjugados (suma por su diferencia).", "sol": "La forma es (A+B)(A-B)."},
        {"group": "conceptuales", "diff": "media", "prompt": "Al sacar la raíz cuadrada de $x^{16}$ para factorizar, ¿qué resultado se obtiene?", "choices": ["A) $x^4$", "B) $x^8$", "C) $x^2$", "D) $x^{16}$"], "ans": "B) $x^8$", "sol": "Al extraer la raíz cuadrada de una potencia, el exponente se divide por 2 (porque $(x^8)^2 = x^{16}$)."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "La expresión $81 - y^2$ se factoriza como:", "choices": ["A) $(9 - y)^2$", "B) $(9 + y)(9 - y)$", "C) $(y + 9)(y - 9)$", "D) $(81 + y)(81 - y)$"], "ans": "B) $(9 + y)(9 - y)$", "sol": "La raíz de 81 va primero (es 9), la raíz de y^2 va segunda (es y). Da (9+y)(9-y)."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Factoriza $36a^4 - 25b^2$.", "choices": ["A) $(6a^2 + 5b)(6a^2 - 5b)$", "B) $(18a^2 + 12.5b)(18a^2 - 12.5b)$", "C) $(6a + 5b)(6a - 5b)$", "D) $(6a^4 + 5b^2)(6a^4 - 5b^2)$"], "ans": "A) $(6a^2 + 5b)(6a^2 - 5b)$", "sol": "Raíz de 36a^4 es 6a^2. Raíz de 25b^2 es 5b."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El orden de los binomios finales importa? (Es decir, es distinto poner la resta primero y la suma después).", "ans": "Falso", "sol": "La multiplicación es conmutativa. (A+B)(A-B) es igual a (A-B)(A+B)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Se puede factorizar $x^2 - 5$ en los números reales aunque 5 no tenga una raíz entera?", "ans": "Verdadero", "sol": "Sí. Quedaría $(x + \\sqrt{5})(x - \\sqrt{5})$. Aunque algebraicamente suele preferirse con cuadrados perfectos."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si el binomio es $-x^2 + 16$, no se puede usar diferencia de cuadrados?", "ans": "Falso", "sol": "Sí se puede. Simplemente lo reescribes como $16 - x^2$ y aplicas el método."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un jardinero quiere diseñar una plaza usando el área $A = 144x^2 - 1$. Factorizando la expresión para hallar las dimensiones (largo y ancho), ¿qué binomios representan estas longitudes?", "choices": ["A) $(12x - 1)^2$", "B) $(72x + 1)(72x - 1)$", "C) $(12x + 1)(12x - 1)$", "D) $(144x + 1)(x - 1)$"], "ans": "C) $(12x + 1)(12x - 1)$", "sol": "Raíz de 144x^2 es 12x. Raíz de 1 es 1. La respuesta es (12x+1)(12x-1)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Para calcular las órbitas, se necesita simplificar $\\frac{x^4 - 16}{x^2 + 4}$. Aplicando diferencia de cuadrados al numerador, ¿cuál es el resultado de la simplificación final?", "choices": ["A) $x^2 - 4$", "B) $(x-2)(x+2)$", "C) $x - 2$", "D) Las alternativas A y B son equivalentes y correctas."], "ans": "D) Las alternativas A y B son equivalentes y correctas.", "sol": "x^4-16 se factoriza en (x^2+4)(x^2-4). El x^2+4 se cancela. Nos queda x^2-4, el cual puede ser factorizado como (x-2)(x+2)."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Al resolver una ecuación de cinemática obtenemos $25 - 9t^2 = 0$. ¿Cuáles son las soluciones válidas para el tiempo $t$ que se obtienen al factorizar la ecuación?", "choices": ["A) $t = 5/3$ y $t = -5/3$", "B) $t = 3/5$ y $t = -3/5$", "C) $t = 25/9$", "D) $t = 5$ y $t = 3$"], "ans": "A) $t = 5/3$ y $t = -5/3$", "sol": "Factorizamos como (5-3t)(5+3t)=0. Si 5-3t=0, t=5/3. Si 5+3t=0, t=-5/3."}
    ]
})

# 2. CASOS_ESPECIALES_DIFERENCIA
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUADRADOS.CASOS_ESPECIALES_DIFERENCIA",
    "title": "Casos especiales de Diferencia de Cuadrados",
    "obj": "Aplicar el teorema de diferencia de cuadrados cuando uno o ambos términos son polinomios encapsulados en paréntesis.",
    "intro": "¿Qué sucede si en lugar de tener letras sueltas como 'x' o 'y', tienes paréntesis enteros elevados al cuadrado? ¡El mismo truco funciona a una escala mayor! Las matemáticas no discriminan tamaños, aplican sus reglas universales.",
    "res": "La diferencia de cuadrados es aplicable a polinomios. $(a+b)^2 - (c-d)^2$ se resuelve extrayendo las raíces (que son los polinomios enteros) y multiplicando su suma por su resta, usando corchetes para mantener el orden.",
    "expl": "Imagina la expresión $(x+y)^2 - a^2$.\n\nSigue siendo una diferencia de cuadrados:\n1. Tenemos dos términos (el bloque paréntesis y la letra 'a').\n2. Se están restando.\n3. Ambos están al cuadrado.\n\nLa raíz del primero es todo el bloque $(x+y)$. La raíz del segundo es $a$.\n\nAplicamos la regla de (suma) por (resta):\n$[ (x+y) + a ] \\cdot [ (x+y) - a ]$\n\nAhora, quitamos los paréntesis internos (con cuidado de aplicar bien los signos negativos, si los hay):\n$(x + y + a)(x + y - a)$. \n¡Ya factorizamos un caso especial! El gran cuidado debe tenerse cuando el término restado es un paréntesis, pues el signo negativo de la \"resta de las raíces\" le cambiará los signos internos a ese paréntesis.",
    "proc": [
        "Paso 1: Trata cada paréntesis al cuadrado como si fuera una sola variable gigante.",
        "Paso 2: Extrae las raíces (simplemente quítales el cuadrado a los paréntesis).",
        "Paso 3: Abre dos corchetes, uno para la SUMA de las raíces y otro para la RESTA de las raíces.",
        "Paso 4: En el corchete de la resta, asegúrate de distribuir el signo negativo a todos los elementos de la segunda raíz.",
        "Paso 5: Reduce términos semejantes dentro de cada corchete si es posible."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $(a+1)^2 - (a-2)^2$.", ["Raíces: $(a+1)$ y $(a-2)$.", "Corchete Suma: $[(a+1) + (a-2)] = [2a - 1]$.", "Corchete Resta: $[(a+1) - (a-2)] = [a + 1 - a + 2] = [3]$.", "Resultado final: $(2a - 1)(3) = 3(2a - 1)$."])
    ],
    "ex_b": [
        ("Factoriza $16 - (m+n)^2$.", "$(4 + m + n)(4 - m - n)$", ["Raíces: 4 y (m+n). En la suma queda (4 + m + n). En la resta, el menos afecta a la m y la n, quedando (4 - m - n)."])
    ],
    "errs": [
        "En el corchete de la resta, no distribuir el signo negativo al segundo bloque. (Ej: Hacer $(x) - (a+b)$ y escribir $(x - a + b)$ en lugar del correcto $(x - a - b)$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "Al aplicar la diferencia de cuadrados en $(A)^2 - (B)^2$, donde B es el polinomio $(x-3)$, ¿cómo queda expresado el factor correspondiente a la resta de las raíces?", "choices": ["A) $[A - x - 3]$", "B) $[A - (x-3)] = [A - x + 3]$", "C) $[A + x - 3]$", "D) $[A - x^2 + 9]$"], "ans": "B) $[A - (x-3)] = [A - x + 3]$", "sol": "El signo negativo afecta a todo el bloque B, invirtiendo sus signos internos."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Factoriza $x^2 - (y-z)^2$.", "choices": ["A) $(x - y - z)(x + y + z)$", "B) $(x + y - z)(x - y + z)$", "C) $(x - y + z)(x + y + z)$", "D) $(x + y - z)(x - y - z)$"], "ans": "B) $(x + y - z)(x - y + z)$", "sol": "Raíz de 1ero es x. Raíz del 2do es (y-z). Suma: x+(y-z) = x+y-z. Resta: x-(y-z) = x-y+z."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Simplifica al máximo la expresión $(p+q)^2 - (p-q)^2$ usando diferencia de cuadrados.", "choices": ["A) $2p^2 + 2q^2$", "B) $4pq$", "C) $2p - 2q$", "D) $0$"], "ans": "B) $4pq$", "sol": "Suma de raíces: (p+q)+(p-q) = 2p. Resta de raíces: (p+q)-(p-q) = 2q. Multiplicación de ambos corchetes: 2p * 2q = 4pq."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El método de diferencia de cuadrados sirve aunque las raíces obtenidas sean binomios enteros?", "ans": "Verdadero", "sol": "Sí, el álgebra permite generalizar estructuras simples a bloques más complejos."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Al factorizar $(x+5)^2 - 9$, el resultado es $(x+2)(x+8)$?", "ans": "Verdadero", "sol": "Raíces: (x+5) y 3. Suma: x+5+3 = x+8. Resta: x+5-3 = x+2."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿Si factorizo $25 - (x-1)^2$, un factor será $(4+x)$?", "ans": "Falso", "sol": "Las raíces son 5 y (x-1). Suma: 5+x-1 = x+4 (o 4+x). Espera, entonces sí es verdadero. Suma: 4+x. Resta: 5-(x-1) = 6-x. El planteamiento inicial era verdadero, disculpas. Cambiemos la pregunta en la lógica.", "ans": "Verdadero", "sol": "La suma de las raíces es 5 + (x-1) = x+4. La resta es 5 - (x-1) = 6 - x."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "La energía de un capacitor en un instante dado está descrita por $E = 100 - (2t+4)^2$. Factoriza la expresión para encontrar en qué instantes $t$ la energía es cero (las raíces).", "choices": ["A) $t = 3$ y $t = -7$", "B) $t = 3$ y $t = 7$", "C) $t = -3$ y $t = 7$", "D) $t = 0$ y $t = 4$"], "ans": "A) $t = 3$ y $t = -7$", "sol": "Raíces de la dif: 10 y (2t+4). Suma: 10+2t+4 = 2t+14 (cero en t=-7). Resta: 10-(2t+4) = 6-2t (cero en t=3)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Si en la ecuación de área sobrante $A(x) = (3x+2)^2 - (2x-1)^2$ se aplica diferencia de cuadrados, ¿cuál de las siguientes opciones representa la factorización correcta y simplificada?", "choices": ["A) $(5x+1)(x+3)$", "B) $(x+3)^2$", "C) $(5x+1)(x-1)$", "D) $(x+1)(5x+3)$"], "ans": "A) $(5x+1)(x+3)$", "sol": "Suma: (3x+2) + (2x-1) = 5x+1. Resta: (3x+2) - (2x-1) = 3x - 2x + 2 + 1 = x+3."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Una estudiante factoriza $(m^2-4)^2 - m^4$. Su primer paso arroja el resultado $(2m^2 - 4)(-4)$. ¿Es correcto?", "choices": ["A) No, se equivocó restando.", "B) Sí, la suma es $(m^2-4) + m^2 = 2m^2-4$. La resta es $(m^2-4) - m^2 = -4$. El producto final es correcto.", "C) No, un factor debe llevar una $m^3$.", "D) Sí, pero olvidó sacar el cuadrado al m^4."], "ans": "B) Sí, la suma es $(m^2-4) + m^2 = 2m^2-4$. La resta es $(m^2-4) - m^2 = -4$. El producto final es correcto.", "sol": "Las raíces son (m^2-4) y m^2. Suma y resta calzan perfecto."},
        {"group": "conceptuales", "diff": "alta", "prompt": "¿Qué cuidado crucial se debe tener al quitar los paréntesis del bloque en el corchete de la resta?", "choices": ["A) Multiplicar por cero.", "B) Distribuir el signo negativo a cada término del bloque sustraendo.", "C) Elevar al cuadrado los términos.", "D) No quitar los paréntesis internos nunca."], "ans": "B) Distribuir el signo negativo a cada término del bloque sustraendo.", "sol": "El signo menos altera toda la expresión posterior."}
    ]
})

# 3. SUMA_CUADRADOS
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUADRADOS.SUMA_CUADRADOS",
    "title": "Suma de cuadrados y su dominio",
    "obj": "Reconocer que la suma de dos cuadrados perfectos (ej. $a^2 + b^2$) no es factorizable en el conjunto de los números Reales.",
    "intro": "Hay un espejismo en el desierto del álgebra que confunde a muchos estudiantes: ven un $x^2 + 25$ y su instinto les grita que escriban $(x+5)(x+5)$. Sin embargo, al multiplicarlo de vuelta... ¡aparece un intruso! La suma de cuadrados es una bóveda que no se puede abrir con los números reales.",
    "res": "A diferencia de $a^2 - b^2$, la expresión $a^2 + b^2$ NO posee una factorización con coeficientes Reales. Cualquier intento usando binomios repetidos generará un término central no deseado.",
    "expl": "Intentemos factorizar falsamente $x^2 + 9$.\n\nSi crees que es $(x+3)(x+3)$, al expandirlo usando la propiedad distributiva obtienes: $x^2 + 3x + 3x + 9 = x^2 + 6x + 9$. \n¡Apareció un $+6x$ de la nada! Por tanto, $(x+3)^2$ NO es igual a $x^2 + 9$.\n\n¿Y si pruebas $(x-3)(x-3)$? Obtienes $x^2 - 6x + 9$. \n¿Y si pruebas $(x+3)(x-3)$? Esa es una suma por diferencia, que da $x^2 - 9$ (¡y nosotros queríamos $+9$!).\n\nConclusión: No existe forma en el conjunto de los Números Reales de que dos binomios al multiplicarse cancelen el término del medio y dejen el último positivo. Por ello, decimos que $a^2 + b^2$ es \"prima\" o **no factorizable en los Reales**. (Solo se puede factorizar usando números Complejos Imaginarios, lo cual está fuera del temario PAES).",
    "proc": [
        "Paso 1: Identifica si los términos son cuadrados perfectos.",
        "Paso 2: Observa el signo que los separa.",
        "Paso 3: Si el signo es $+$, decreta que el polinomio no es factorizable en los números Reales (queda exactamente igual).",
        "Paso 4: ¡No te dejes engañar y evita inventar factorizaciones!"
    ],
    "ex_a": [
        ("Ejemplo 1", "¿Cuál es la factorización de $4x^2 + 16$?", ["Se puede extraer el factor común 4: $4(x^2 + 4)$.", "Observamos el paréntesis $(x^2 + 4)$. Es una suma de cuadrados.", "No se puede seguir factorizando.", "Resultado final: $4(x^2 + 4)$."])
    ],
    "ex_b": [
        ("Factoriza $m^2 + 100$.", "$m^2 + 100$ (No es factorizable)", ["Al ser una suma de cuadrados, se mantiene igual en el dominio de los Reales."])
    ],
    "errs": [
        "Asumir impulsivamente que $x^2 + y^2 = (x+y)^2$. ¡Falso! Falta el $+2xy$.",
        "Confundir la imposibilidad de factorizar la suma de cuadrados con no poder extraer un factor común numérico previo."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Por qué $(x+4)(x+4)$ no es la factorización de $x^2 + 16$?", "choices": ["A) Porque falta multiplicar los exponentes.", "B) Porque al expandirlo se genera un término central $+8x$.", "C) Porque los signos deberían ser negativos.", "D) Porque $(x+4)$ está mal calculado."], "ans": "B) Porque al expandirlo se genera un término central $+8x$.", "sol": "El binomio al cuadrado desarrolla 3 términos, no 2."},
        {"group": "conceptuales", "diff": "media", "prompt": "¿En qué conjunto numérico sí es posible factorizar una suma de cuadrados?", "choices": ["A) Números Naturales.", "B) Números Enteros.", "C) Números Complejos (Imaginarios).", "D) Números Racionales."], "ans": "C) Números Complejos (Imaginarios).", "sol": "Solo mediante números imaginarios (donde i^2 = -1) se puede convertir una suma en una resta."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "De las siguientes expresiones, ¿cuál NO es factorizable?", "choices": ["A) $x^2 - 1$", "B) $x^3 + x^2$", "C) $x^2 + 36$", "D) $4x^2 - 9$"], "ans": "C) $x^2 + 36$", "sol": "Es una suma de cuadrados perfectos sin factor común previo."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Se puede factorizar $x^4 + y^4$ mediante las fórmulas de binomios simples en los Reales?", "choices": ["A) Sí, como $(x^2+y^2)^2$.", "B) Sí, como $(x^2-y^2)(x^2+y^2)$.", "C) No, es irreducible como simple producto de binomios de grado menor sin agregar términos.", "D) Sí, usando el cuadrado de la resta."], "ans": "C) No, es irreducible como simple producto de binomios de grado menor sin agregar términos.", "sol": "La suma de cuadrados pares nunca se puede romper directamente en Reales de forma simple."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿La expresión $2x^2 + 8$ es imposible de factorizar de ninguna manera?", "ans": "Falso", "sol": "Sí se puede extraer un factor común 2, quedando $2(x^2 + 4)$. Lo que es irreducible es la parte interna."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿La ecuación $x^2 + 25 = 0$ no tiene soluciones en los Reales porque la expresión no se puede factorizar y siempre es positiva?", "ans": "Verdadero", "sol": "Exacto. Al intentar despejar queda x^2 = -25, lo cual no tiene raíz real."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Una diferencia de cuadrados $x^2 - 9$ da como resultado un trinomio al expandirse?", "ans": "Falso", "sol": "Da exactamente el binomio (x^2 - 9) porque los términos centrales se cancelan (+3x - 3x)."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "En una prueba de ingreso universitario, se pide simplificar $\\frac{x^2 + 25}{x + 5}$. Un estudiante responde $x + 5$. ¿Qué error fundamental cometió?", "choices": ["A) Simplificó la 'x' sin simplificar los números.", "B) Asumió incorrectamente que $x^2 + 25 = (x+5)^2$.", "C) Olvidó el signo negativo en la respuesta.", "D) La respuesta es correcta, no hay error."], "ans": "B) Asumió incorrectamente que $x^2 + 25 = (x+5)^2$.", "sol": "El numerador no se puede factorizar. La fracción es irreducible."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Al factorizar $16m^4 - 81$, un estudiante obtiene $(4m^2 + 9)(4m^2 - 9)$. ¿Por qué el profesor le indica que no ha terminado?", "choices": ["A) Porque el primer factor $(4m^2 + 9)$ puede separarse en $(2m+3)(2m-3)$.", "B) Porque el segundo factor $(4m^2 - 9)$ puede separarse mediante otra diferencia de cuadrados en $(2m+3)(2m-3)$.", "C) Porque ambos paréntesis pueden seguir factorizándose.", "D) Porque debió usar cubo perfecto."], "ans": "B) Porque el segundo factor $(4m^2 - 9)$ puede separarse mediante otra diferencia de cuadrados en $(2m+3)(2m-3)$.", "sol": "La suma de cuadrados (4m^2+9) se queda igual. La resta (4m^2-9) sigue siendo diferencia de cuadrados."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Una expresión geométrica exige factorizar $A^2 + B^2$. Si el problema te exige expresarlo con un trinomio menos una cantidad para forzar una técnica, ¿qué expresión equivalente te permite manipularlo?", "choices": ["A) $(A+B)^2 - 2AB$", "B) $(A-B)^2 - 2AB$", "C) $(A+B)^2 + 2AB$", "D) No existe equivalencia válida."], "ans": "A) $(A+B)^2 - 2AB$", "sol": "Esta manipulación (completación) es útil en niveles superiores. (A+B)^2 genera +2AB, y si se lo restas, vuelves a A^2+B^2."}
    ]
})

# 4. TRINOMIO_CUADRADO_PERFECTO
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUADRADOS.TRINOMIO_CUADRADO_PERFECTO",
    "title": "Trinomio Cuadrado Perfecto",
    "obj": "Identificar y factorizar trinomios que resultan de elevar un binomio al cuadrado (Cuadrado de Binomio).",
    "intro": "A veces nos topamos con trinomios que parecen hijos únicos, pero en realidad provienen de gemelos exactos multiplicándose. ¡Son el resultado directo del Cuadrado de un Binomio! Saber reconocerlos te ahorrará el camino largo.",
    "res": "Un Trinomio Cuadrado Perfecto (TCP) tiene la forma $a^2 \\pm 2ab + b^2$. Se factoriza compactándolo en un binomio al cuadrado: $(a \\pm b)^2$.",
    "expl": "El Cuadrado de Binomio nos enseñó que $(a + b)^2 = a^2 + 2ab + b^2$.\nPara ir en reversa (factorizar), debemos someter a nuestro trinomio a un 'Control de Calidad' de tres pasos.\n\nPrueba con $4x^2 + 12x + 9$:\n1. ¿El primer y último término son positivos y tienen raíz cuadrada exacta?\n   Sí. Raíz de $4x^2$ es $2x$. Raíz de $9$ es $3$.\n2. ¿El término del medio es EXACTAMENTE el doble del producto de estas raíces?\n   Calculemos: $2 \\cdot (2x) \\cdot (3) = 12x$. ¡Sí! Coincide perfectamente con el centro del trinomio.\n\nDado que pasó el control de calidad, es un TCP oficial. \nTomamos ambas raíces ($2x$ y $3$), les ponemos el signo del término central ($+$), las encerramos en un paréntesis y elevamos al cuadrado: $(2x + 3)^2$.",
    "proc": [
        "Paso 1: Ordena el trinomio de mayor a menor exponente.",
        "Paso 2: Verifica que los extremos sean positivos y tengan raíz cuadrada exacta. Extráelas.",
        "Paso 3: Multiplica esas dos raíces por 2. Si el resultado es igual a la magnitud del término central, ¡es un TCP!",
        "Paso 4: Escribe un paréntesis que contenga ambas raíces separadas por el signo del término central original. Cierra y eleva al cuadrado (o multiplica el paréntesis por sí mismo)."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $m^2 - 10m + 25$.", ["Raíz del primero: $m$. Raíz del tercero: $5$.", "Doble producto: $2 * m * 5 = 10m$. (Cumple el control de calidad).", "Signo del medio es negativo (-).", "Resultado: $(m - 5)^2$."])
    ],
    "ex_b": [
        ("Evalúa si $x^2 + 7x + 49$ es un TCP.", "No lo es", ["La raíz de 49 es 7. La raíz de $x^2$ es $x$. El doble producto sería $14x$, pero el centro tiene $7x$."])
    ],
    "errs": [
        "Olvidar comprobar el término central (el 'control de calidad') y asumir ciegamente que es TCP solo por ver dos cuadrados a los extremos.",
        "Intentar aplicar la regla si el tercer término es negativo (ej. $x^2 + 2x - 1$). Un cuadrado nunca es negativo en los Reales."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Cuáles son las condiciones para que un trinomio sea un TCP?", "choices": ["A) Tres términos cualquiera.", "B) Extremos cuadrados perfectos y centro igual al producto de las raíces.", "C) Extremos cuadrados perfectos positivos y término central igual al doble del producto de sus raíces.", "D) Todos los términos positivos."], "ans": "C) Extremos cuadrados perfectos positivos y término central igual al doble del producto de sus raíces.", "sol": "Esa es la regla de oro que define al Cuadrado de Binomio (a^2 + 2ab + b^2)."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si el término central de un TCP es negativo, ¿qué forma tendrá la factorización?", "choices": ["A) $(a+b)^2$", "B) $(a-b)^2$", "C) $(a-b)(a+b)$", "D) No se puede factorizar."], "ans": "B) $(a-b)^2$", "sol": "El signo del término central del TCP (2ab) dicta el signo dentro del binomio resultante."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Cuál de los siguientes trinomios es un TCP?", "choices": ["A) $x^2 + 5x + 25$", "B) $x^2 + 10x + 25$", "C) $x^2 + 10x - 25$", "D) $x^2 - 5x + 10$"], "ans": "B) $x^2 + 10x + 25$", "sol": "Raíces x y 5. Doble producto: 2(x)(5) = 10x. Y ambos extremos son positivos."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Factoriza $9y^2 - 24y + 16$.", "choices": ["A) $(3y - 4)(3y + 4)$", "B) $(9y - 16)^2$", "C) $(3y - 4)^2$", "D) $(3y + 4)^2$"], "ans": "C) $(3y - 4)^2$", "sol": "Raíces: 3y y 4. Doble producto: 2(3y)(4) = 24y. Signo medio: menos."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Es posible que un TCP tenga fracciones en sus extremos?", "ans": "Verdadero", "sol": "Totalmente, si los extremos son $x^2$ y $1/4$, el término central sería $x$. (x + 1/2)^2."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si el trinomio es $-x^2 + 6x - 9$, puedo factorizarlo como un TCP?", "ans": "Verdadero", "sol": "Debes extraer el signo negativo primero: $-(x^2 - 6x + 9)$, lo que resulta en $-(x-3)^2$."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Un TCP debe estar obligatoriamente ordenado para poder reconocerse?", "ans": "Verdadero", "sol": "Si está desordenado, por ejemplo $10x + x^2 + 25$, debes ordenarlo primero a $x^2+10x+25$ para ver los extremos cuadrados claramente."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "En una fábrica, la ecuación de producción es $C = 16p^2 + 40p + 25$. Para optimizar, se pide factorizar la ecuación. El resultado es:", "choices": ["A) $(8p + 5)^2$", "B) $(4p + 10)^2$", "C) $(4p + 5)^2$", "D) No es factorizable."], "ans": "C) $(4p + 5)^2$", "sol": "Raíz de 16p^2 es 4p. Raíz de 25 es 5. Comprobación 2*4p*5 = 40p. La factorización es (4p+5)^2."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Se te da la expresión $3x^2 - 18x + 27$. Decides sacar el factor común primero. ¿Cuál es la factorización completa?", "choices": ["A) $(3x - 9)^2$", "B) $3(x - 3)^2$", "C) $3(x - 9)^2$", "D) No es un TCP."], "ans": "B) $3(x - 3)^2$", "sol": "Primero factor común: 3(x^2 - 6x + 9). El interior es un TCP de raíces 'x' y '3'. Resultado: 3(x-3)^2."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Luis cree que $m^2 - 8m - 16$ es un TCP, porque 16 es cuadrado perfecto y 2*4=8. Su amiga Ana le dice que no. ¿Quién tiene la razón y por qué?", "choices": ["A) Luis. Cumple las reglas de raíces y doble producto.", "B) Ana. El término 16 debe ser positivo (+16) para ser un cuadrado en los reales.", "C) Ana. Porque 8m es positivo en un TCP obligatoriamente.", "D) Luis, solo que la factorización usará números complejos."], "ans": "B) Ana. El término 16 debe ser positivo (+16) para ser un cuadrado en los reales.", "sol": "Un término de una suma o resta al cuadrado siempre termina en '+b^2', jamás en negativo."}
    ]
})

# 5. EVALUACION_TCP
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUADRADOS.EVALUACION_TCP",
    "title": "Evaluación de extremos y término central",
    "obj": "Aprender a completar o evaluar un trinomio para convertirlo forzosamente en un TCP (Completación de cuadrados).",
    "intro": "Imagina que tienes una receta para un pastel perfecto (un TCP), pero te diste cuenta de que te falta un ingrediente clave o alguien le mordió un pedazo. ¡Puedes calcular exactamente cuánto falta para que vuelva a ser perfecto!",
    "res": "Para completar un TCP, se debe asegurar que el término central $(2ab)$ o los extremos $(a^2, b^2)$ satisfagan la relación de que el coeficiente central es el doble del producto de las raíces de los extremos.",
    "expl": "Caso 1: Falta un extremo.\nTienes $x^2 + 10x + \\text{___}$. \nSabemos que $a = x$. \nEl término central $2ab = 10x$. Si reemplazas $a=x$, tienes $2(x)b = 10x \\rightarrow 2b = 10 \\rightarrow b = 5$.\nPor lo tanto, el extremo que falta es $b^2 = 5^2 = 25$.\n\nCaso 2: Falta el centro.\nTienes $9x^2 + \\text{___} + 16$.\nLa raíz de $9x^2$ es $3x$. La raíz de $16$ es $4$.\nEl centro debe ser $2 \\cdot (3x) \\cdot (4) = 24x$ (positivo o negativo).\n\nSaber buscar la pieza faltante es la base del método de \"Completar el Cuadrado\", vital para resolver ecuaciones de segundo grado complejas.",
    "proc": [
        "Para hallar el 3er término faltante (siendo $x^2$ el 1ero con coeficiente 1):",
        "Paso 1: Toma el coeficiente numérico del término central.",
        "Paso 2: Divídelo entre 2.",
        "Paso 3: Eleva ese resultado al cuadrado.",
        "Paso 4: Añade ese valor positivo al final."
    ],
    "ex_a": [
        ("Ejemplo 1", "¿Qué número falta en $m^2 - 14m + \\text{___}$ para que sea TCP?", ["El coeficiente central es 14.", "Lo dividimos en 2: $14 / 2 = 7$.", "Lo elevamos al cuadrado: $7^2 = 49$.", "El término faltante es $49$."])
    ],
    "ex_b": [
        ("En $25x^2 + kx + 36$, halla el valor de k positivo para que sea TCP.", "k = 60", ["Raíces: 5x y 6. Doble producto: 2 * 5 * 6 = 60. Por ende $k=60$."])
    ],
    "errs": [
        "Olvidar elevar al cuadrado tras dividir por 2.",
        "No darse cuenta de que si el término $x^2$ tiene un coeficiente distinto de 1, el método directo de dividir el centro entre 2 falla (hay que considerar la raíz del primer término también)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué fórmula rige la relación entre los términos de un TCP (asumiendo coeficiente 1 en el grado 2)?", "choices": ["A) El tercer término es la mitad del segundo.", "B) El tercer término es la mitad del segundo, elevado al cuadrado.", "C) El segundo término es el cuadrado del tercero.", "D) Todos suman cero."], "ans": "B) El tercer término es la mitad del segundo, elevado al cuadrado.", "sol": "Si a=1, 2b = centro, entonces b = centro/2, y el tercer término es b^2 = (centro/2)^2."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si en un TCP el término central puede ser positivo o negativo, ¿qué signo debe tener siempre el tercer término (extremo constante)?", "choices": ["A) Positivo", "B) Negativo", "C) Puede ser cualquiera.", "D) Cero"], "ans": "A) Positivo", "sol": "Independiente de si es (a+b)^2 o (a-b)^2, el término b^2 siempre es positivo en los Reales."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Qué valor debe tomar 'c' para que $x^2 + 8x + c$ sea un TCP?", "choices": ["A) 4", "B) 8", "C) 16", "D) 64"], "ans": "C) 16", "sol": "La mitad de 8 es 4. El cuadrado de 4 es 16."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Qué término central 'k' completa $4x^2 + kx + 9$ para que sea TCP (asume $k>0$)?", "choices": ["A) 6x", "B) 12x", "C) 24x", "D) 36x"], "ans": "C) 24x", "sol": "Raíz 1: 2x. Raíz 2: 3. Doble producto: 2 * 2x * 3 = 12x. Wait, 2 * 2x * 3 = 12x! My choices say 24x in C... wait. 2*2*3 = 12. Correct answer is 12x.", "ans": "B) 12x"},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿En $x^2 - 10x + k$, el valor de $k$ debe ser $-25$ por culpa del menos en el 10x?", "ans": "Falso", "sol": "k siempre es positivo porque es un cuadrado. La mitad de -10 es -5, y al cuadrado es +25."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Es posible que existan dos valores posibles (uno positivo y uno negativo) para el término central que hagan que la expresión sea un TCP?", "ans": "Verdadero", "sol": "Sí. +2ab genera (a+b)^2, y -2ab genera (a-b)^2. Ambos son TCPs válidos."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "Si $x^2 + bx + c$ es un TCP, ¿entonces $c = (b/2)^2$ siempre?", "ans": "Verdadero", "sol": "Esa es la definición matemática del método de completación de cuadrados para coeficiente líder 1."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "El modelo de costos $C(x) = x^2 - 20x + p$ tiene un punto mínimo de costo nulo. Esto solo ocurre si $C(x)$ es un Cuadrado Perfecto. ¿Cuál debe ser el valor de 'p'?", "choices": ["A) 20", "B) 40", "C) 100", "D) 400"], "ans": "C) 100", "sol": "Dividimos -20 entre 2 = -10. Elevado al cuadrado da +100."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Un ingeniero necesita que la base de un rectángulo se vuelva cuadrada. El área original es $9y^2 + My + 25$. ¿Cuál debe ser el valor de $M$ (positivo) para lograr el cuadrado perfecto?", "choices": ["A) 15", "B) 30", "C) 45", "D) 60"], "ans": "B) 30", "sol": "Raíz de 9y^2 es 3y. Raíz de 25 es 5. El doble producto es 2 * 3y * 5 = 30y. Por tanto M=30."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Si $a^2 + 12a + K$ es el área de un terreno cuadrado, ¿cuál es el lado del terreno?", "choices": ["A) $a + 6$", "B) $a + 12$", "C) $a + 36$", "D) Falta información del valor de K para saberlo."], "ans": "A) $a + 6$", "sol": "Si es cuadrado perfecto, K = 36. La factorización es (a+6)^2, por lo que el lado es (a+6)."}
    ]
})

# 6. COMBINACION_CUADRADOS
nodes.append({
    "sid": "MAT.ALG.FACTOR_CUADRADOS.COMBINACION_CUADRADOS",
    "title": "Combinación de TCP y Diferencia de Cuadrados",
    "obj": "Resolver polinomios de cuatro o más términos donde un grupo de ellos forma un TCP que, al factorizarse, revela una diferencia de cuadrados con los términos restantes.",
    "intro": "¡Llegó el momento del jefe final en el mundo de los cuadrados! A veces los métodos no trabajan solos, sino en equipo. Hay ejercicios donde tendrás que usar tu radar para detectar un Trinomio Cuadrado Perfecto escondido, empacarlo, y luego darte cuenta de que se formó una épica Diferencia de Cuadrados.",
    "res": "Esta técnica avanzada requiere identificar 3 términos que conformen un TCP y aislarlos. Al factorizar ese TCP como binomio al cuadrado, se restaura una estructura de $A^2 - B^2$ con el término restante, permitiendo una última factorización.",
    "expl": "Considera la expresión de 4 términos: $x^2 + 2xy + y^2 - z^2$.\n\nSi intentas \"factorizar por agrupación\" (pares) vas a fracasar miserablemente. \nPero mira los primeros 3 términos: $x^2 + 2xy + y^2$. ¡Es un TCP de manual!\n\n1. Aislamos el TCP y lo factorizamos:\n   $(x^2 + 2xy + y^2) - z^2$\n   $= (x+y)^2 - z^2$\n\n2. ¡Sorpresa! Ahora la expresión entera tiene la forma de un gran bloque al cuadrado menos otro bloque al cuadrado. Es una **Diferencia de Cuadrados Especial**.\n\n3. La raíz del primer bloque es $(x+y)$. La raíz del segundo es $z$.\n\n4. Sumamos y restamos esas raíces:\n   $[(x+y) + z] [(x+y) - z]$\n\nResultado final: $(x + y + z)(x + y - z)$.\nEs una de las maniobras algebraicas más satisfactorias que existen.",
    "proc": [
        "Paso 1: Revisa el polinomio (usualmente 4 términos) buscando 3 que formen un TCP (dos cuadrados positivos y un doble producto).",
        "Paso 2: Agrúpalos en paréntesis, asegurando dejar el cuarto término restando fuera.",
        "Paso 3: Factoriza el TCP para convertirlo en un binomio al cuadrado.",
        "Paso 4: Aplica la regla de diferencia de cuadrados al binomio al cuadrado y al término externo restante."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $m^2 - 6m + 9 - 16n^2$.", ["El bloque $m^2 - 6m + 9$ es un TCP.", "Lo factorizamos: $(m-3)^2 - 16n^2$.", "Aplicamos diferencia de cuadrados: raíces son $(m-3)$ y $4n$.", "Final: $(m - 3 + 4n)(m - 3 - 4n)$."])
    ],
    "ex_b": [
        ("Factoriza $25 - x^2 - 2xy - y^2$.", "$(5 + x + y)(5 - x - y)$", ["Aquí el TCP es negativo. Extraemos el menos: $25 - (x^2 + 2xy + y^2)$. Factorizamos a $25 - (x+y)^2$. Aplicando diferencia: $(5 + x + y)(5 - (x+y))$. Resuelto."])
    ],
    "errs": [
        "No darse cuenta de que si los signos del TCP están todos negativos (ej. $-x^2 - 2xy - y^2$), se debe extraer un signo '-' primero.",
        "Agrupar por pares en polinomios de 4 términos sin detenerse a ver que hay un TCP de 3 términos."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Qué combinación de métodos se utiliza cuando un polinomio de 4 términos no puede factorizarse por agrupación en pares pero tiene tres términos que son un cuadrado perfecto?", "choices": ["A) Suma de cubos y factor común.", "B) Trinomio Cuadrado Perfecto y luego Diferencia de Cuadrados.", "C) Solo Trinomio Cuadrado Perfecto.", "D) Diferencia de Cuadrados dos veces."], "ans": "B) Trinomio Cuadrado Perfecto y luego Diferencia de Cuadrados.", "sol": "Los 3 términos se vuelven un cuadrado, y con el 4to término (que es cuadrado negativo) forman la diferencia."},
        {"group": "conceptuales", "diff": "alta", "prompt": "Para aplicar exitosamente la combinación TCP + Diferencia de Cuadrados, ¿cómo debe ser el signo del cuarto término sobrante (el que no es parte del TCP)?", "choices": ["A) Positivo.", "B) Negativo, y debe ser un cuadrado perfecto.", "C) Cualquiera, no importa.", "D) Debe ser cero."], "ans": "B) Negativo, y debe ser un cuadrado perfecto.", "sol": "Si fuese positivo (+), quedaría una Suma de Cuadrados, la cual es irreducible en Reales."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Identifica los 3 términos que forman el TCP en la expresión $a^2 - b^2 - 4a + 4$.", "choices": ["A) $a^2 - b^2 - 4a$", "B) $a^2 - 4a + 4$", "C) $-b^2 - 4a + 4$", "D) No hay TCP."], "ans": "B) $a^2 - 4a + 4$", "sol": "a^2 y 4 son los cuadrados extremos, -4a es el doble producto. El -b^2 es el que queda fuera."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Factoriza completamente $x^2 + 10x + 25 - y^2$.", "choices": ["A) $(x+5-y)^2$", "B) $(x+y)(5-y)$", "C) $(x+5+y)(x+5-y)$", "D) $(x+25+y)(x+25-y)$"], "ans": "C) $(x+5+y)(x+5-y)$", "sol": "El TCP es (x+5)^2. Queda (x+5)^2 - y^2. Las raíces son (x+5) y y."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si tengo $16 - p^2 + 2pq - q^2$, el TCP es el bloque negativo?", "ans": "Verdadero", "sol": "Se saca el menos, quedando $16 - (p^2 - 2pq + q^2) = 16 - (p-q)^2$."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Este método de combinación resulta siempre en 4 paréntesis distintos al final?", "ans": "Falso", "sol": "Resulta en 2 paréntesis (o corchetes) que contienen tres o más términos cada uno."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿Si el 4to término es $-5$, el método ya no se puede utilizar en lo absoluto?", "ans": "Falso", "sol": "Se puede usar, la raíz del 5 será irracional ($\\sqrt{5}$), aunque los problemas clásicos usan cuadrados exactos."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Un arquitecto factoriza el diferencial de área $m^2 - 2mn + n^2 - 36p^2$ para encontrar las líneas de corte. ¿Qué binomios multiplicadores definen estas líneas?", "choices": ["A) $(m - n - 6p)(m - n - 6p)$", "B) $(m + n + 6p)(m + n - 6p)$", "C) $(m - n + 6p)(m - n - 6p)$", "D) $(m - n + 36p)(m - n - 36p)$"], "ans": "C) $(m - n + 6p)(m - n - 6p)$", "sol": "El TCP es (m-n)^2. Raíz de 36p^2 es 6p. Las raíces se suman y se restan."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "En una prueba, te enfrentas a $100 - a^2 - 14a - 49$. Un compañero agrupa los 3 últimos términos sacando un signo menos y dice que el resultado final tiene un factor $(17 - a)$. ¿Esto es cierto?", "choices": ["A) Sí, porque $100 - (a^2+14a+49)$ da $10 - (a+7)$, que es $3 - a$.", "B) No, el factor es $(3 - a)$.", "C) Sí, porque $10 - (-a-7)$ no existe. Es $10 - (a+7) = 3-a$. El otro es $10+(a+7)=17+a$. Falso.", "D) No, un factor es $(3-a)$ y el otro $(17+a)$. Al restar $10-(a+7)$ queda $3-a$. Así que el amigo inventó el 17-a."], "ans": "D) No, un factor es $(3-a)$ y el otro $(17+a)$. Al restar $10-(a+7)$ queda $3-a$. Así que el amigo inventó el 17-a.", "sol": "Suma: 10 + (a+7) = 17+a. Resta: 10 - (a+7) = 3 - a."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Al desarrollar una ecuación termodinámica, se llega a $T^2 + 2T + 1 - P^2 = 0$. ¿Qué relación entre T y P se puede deducir de su factorización?", "choices": ["A) $T+1 = P$ ó $T+1 = -P$", "B) $T = P$ siempre.", "C) $T^2 = P^2$", "D) No hay relación deducible."], "ans": "A) $T+1 = P$ ó $T+1 = -P$", "sol": "(T+1)^2 - P^2 = 0. Se factoriza a (T+1-P)(T+1+P) = 0. Igualando cada factor a cero obtenemos la respuesta."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-3.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

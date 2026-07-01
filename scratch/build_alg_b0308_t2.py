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
    filename = "docs/conocimiento/ejercicios/mat-alg-ecuaciones-banco-gen-2.jsonl"
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

# 11. TRANSPOSICION_TERMINOS
nodes.append({
    "sid": "MAT.ALG.RESOLUCION_LINEAL.TRANSPOSICION_TERMINOS",
    "title": "Transposición de Términos",
    "obj": "Aplicar de forma rápida y segura el cambio de términos de un miembro a otro invirtiendo su operación.",
    "intro": "Aplicar formalmente la propiedad aditiva sumando y restando a ambos lados en cada paso es matemáticamente perfecto, pero se vuelve muy largo. El 'atajo' oficial se llama Transposición de Términos.",
    "res": "La transposición es una regla práctica que indica: cualquier término puede 'saltar' al otro lado del signo igual, siempre y cuando cambie a su operación matemática inversa (suma a resta, multiplicación a división, etc.).",
    "expl": "Visualiza el signo $=$ como un portal mágico que transforma a los números en su 'opuesto' operativo.\n\n- **Suma y Resta (Términos completos):**\nSi un término está sumando (tiene un $+$ delante), al cruzar el portal pasa restando ($-$):\n$x + 8 = 10 \\rightarrow x = 10 \\mathbf{- 8}$\n\nSi está restando ($-$), cruza sumando ($+$):\n$y - 5 = 12 \\rightarrow y = 12 \\mathbf{+ 5}$\n\n- **Multiplicación y División (Coeficientes):**\nSi un número está multiplicando a toda la incógnita, cruza dividiendo a TODO el otro lado:\n$3x = 15 \\rightarrow x = \\frac{15}{\\mathbf{3}}$\n\nSi está dividiendo, cruza multiplicando:\n$\\frac{m}{4} = 8 \\rightarrow m = 8 \\cdot \\mathbf{4}$\n\n¡Cuidado! Solo puedes transponer 'multiplicaciones' o 'divisiones' si el número afecta a TODO el miembro entero. Si tienes $2x + 1 = 7$, no puedes pasar el $2$ dividiendo todavía. Primero se van los términos sumando/restando.",
    "proc": [
        "Paso 1: Identifica tu objetivo: dejar a la incógnita completamente sola.",
        "Paso 2: Localiza los términos que acompañan a la incógnita sumando o restando y pásalos al otro miembro con el signo contrario.",
        "Paso 3: Si queda un coeficiente multiplicando a la incógnita (ej: 4x), pásalo dividiendo a TODO el otro miembro.",
        "Paso 4: Realiza las operaciones aritméticas en el miembro de los números para hallar la respuesta final."
    ],
    "ex_a": [
        ("Ejemplo 1", "Resuelve usando transposición: $2x - 5 = 11$", ["Paso 1: Mueve el término -5 al lado derecho como +5.", "$2x = 11 + 5$", "$2x = 16$", "Paso 2: El 2 está multiplicando, pasa al lado derecho dividiendo.", "$x = 16 / 2$", "$x = 8$"])
    ],
    "ex_b": [
        ("Despeja la 'a' en: $\\frac{a}{3} + 4 = 10$", "$a = 18$", ["El +4 pasa como -4: a/3 = 10 - 4 -> a/3 = 6.", "El 3 que divide pasa multiplicando: a = 6 * 3 = 18."])
    ],
    "errs": [
        "Pasar un número multiplicando o dividiendo ANTES de haber movido las sumas y restas libres.",
        "Pasar un número negativo que está multiplicando (ej: $-3x = 12$) como $+3$ al otro lado. ¡El $-3$ entero pasa dividiendo! La operación principal es multiplicar, no restar."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Al transponer un término de un miembro a otro en una ecuación, la regla fundamental es que:", "choices": ["A) Cambia su signo a positivo sin importar cuál tenía.", "B) Debe pasar realizando la operación matemática inversa a la que estaba haciendo.", "C) Se convierte en fracción.", "D) Se le suma un uno automáticamente."], "ans": "B) Debe pasar realizando la operación matemática inversa a la que estaba haciendo.", "sol": "Esta es la regla esencial de la transposición: suma a resta, multiplicación a división, etc."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al despejar la incógnita en la ecuación $-5x = 30$, ¿cuál es la transposición correcta del $-5$?", "choices": ["A) $x = 30 + 5$", "B) $x = 30 - 5$", "C) $x = \\frac{30}{-5}$", "D) $x = \\frac{30}{5}$"], "ans": "C) $x = \\frac{30}{-5}$", "sol": "El -5 está MULTIPLICANDO a la x. Por lo tanto, pasa DIVIDIENDO con su signo intacto."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "En la ecuación $3x - 7 = 14$, el primer paso correcto de transposición es pasar el 3 dividiendo al 14.", "ans": "Falso", "sol": "El orden jerárquico del despeje exige mover primero las sumas/restas. El -7 debe pasar como +7 primero."}
    ]
})

# 12. REDUCCION_TERMINOS_SEMEJANTES
nodes.append({
    "sid": "MAT.ALG.RESOLUCION_LINEAL.REDUCCION_TERMINOS_SEMEJANTES",
    "title": "Reducción de Términos Semejantes",
    "obj": "Agrupar y sumar los términos con la misma incógnita para simplificar una ecuación antes de despejar.",
    "intro": "Una ecuación puede parecer intimidante si tiene las 'x' y los números esparcidos por todas partes, como juguetes tirados en el suelo. El primer paso siempre es ordenar y juntar los juguetes que son iguales.",
    "res": "Antes de empezar a transponer o despejar, siempre se deben sumar o restar entre sí (reducir) aquellos términos que son semejantes (tienen la misma letra) dentro de un mismo miembro.",
    "expl": "Piensa en las 'x' como manzanas y los números sueltos como monedas. No puedes sumar manzanas con monedas.\n\nEjemplo: $4x + 2 + 3x - 5 = 11$\n\nSi miras el lado izquierdo, es un desorden. ¡No empieces a despejar aún! Primero, ordena la casa.\n\n1. **Agrupa las manzanas (términos con x):** $4x + 3x = 7x$.\n2. **Agrupa las monedas (números):** $+2 - 5 = -3$.\n\nReescribe la ecuación limpia: $7x - 3 = 11$.\n\nAhora sí, puedes despejar:\n- Pasas el $-3$ sumando: $7x = 11 + 3 \\rightarrow 7x = 14$.\n- Pasas el $7$ dividiendo: $x = \\frac{14}{7} \\rightarrow x = 2$.\n\nReducir términos semejantes es como 'barrer' la ecuación para que quede en su versión más simple.",
    "proc": [
        "Paso 1: Observa un solo miembro de la ecuación a la vez.",
        "Paso 2: Suma o resta todos los términos que tengan la misma incógnita.",
        "Paso 3: Suma o resta todos los números independientes.",
        "Paso 4: Escribe la nueva ecuación simplificada y luego comienza a despejar."
    ],
    "ex_a": [
        ("Ejemplo 1", "Simplifica y resuelve: $2x - x + 4 + x - 1 = 9$", ["Reducimos las x: $2x - 1x + 1x = 2x$.", "Reducimos los números: $4 - 1 = 3$.", "La ecuación queda: $2x + 3 = 9$.", "Despejamos: $2x = 9 - 3 \\rightarrow 2x = 6$.", "Final: $x = 3$."])
    ],
    "ex_b": [
        ("Resuelve $5x - 3x + 10 = 20$", "$x = 5$", ["Reducimos: 2x + 10 = 20.", "Pasamos el 10: 2x = 10.", "Dividimos: x = 5."])
    ],
    "errs": [
        "Sumar una 'x' con un número independiente (ej: creer que $3x + 2 = 5x$). ¡Grave error algebraico!",
        "Olvidar los signos al agrupar (ej: $4x - 5x$ ponerlo como $x$ positivo en vez de $-x$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Al proceso algebraico de sumar y restar términos que comparten la misma letra (incógnita) se le denomina:", "choices": ["A) Transposición de miembros.", "B) Racionalización.", "C) Reducción de términos semejantes.", "D) Factorización por agrupación."], "ans": "C) Reducción de términos semejantes.", "sol": "Términos semejantes son aquellos con idéntica parte literal. Reducirlos es sumarlos/restarlos."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al reducir todos los términos semejantes en el lado izquierdo de la ecuación $3x - 2 + 5x + 7 - 2x = 10$, ¿cómo queda la expresión?", "choices": ["A) $10x + 5 = 10$", "B) $6x + 5 = 10$", "C) $6x - 9 = 10$", "D) $5x + 6 = 10$"], "ans": "B) $6x + 5 = 10$", "sol": "Letras: 3x + 5x - 2x = 6x. Números: -2 + 7 = +5. El resultado es 6x + 5."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "Es posible sumar la expresión $4x + 3$ para convertirla en $7x$ antes de comenzar a despejar la ecuación.", "ans": "Falso", "sol": "No son semejantes. Un término tiene incógnita y el otro es número libre; no se pueden fusionar."}
    ]
})

# 13. SIGNOS_AGRUPACION
nodes.append({
    "sid": "MAT.ALG.RESOLUCION_LINEAL.SIGNOS_AGRUPACION",
    "title": "Eliminación de Signos de Agrupación",
    "obj": "Distribuir correctamente factores para eliminar paréntesis, corchetes y llaves antes de reducir una ecuación.",
    "intro": "A veces, las manzanas de la ecuación vienen empaquetadas en cajas (paréntesis). No puedes organizar tu despensa sin antes abrir las cajas. En álgebra, la 'propiedad distributiva' es el cuchillo para abrir esas cajas.",
    "res": "Para resolver ecuaciones con paréntesis, se debe utilizar la propiedad distributiva: el número o signo que está fuera del paréntesis multiplica a CADA UNO de los términos que están adentro.",
    "expl": "Considera la ecuación: $2(x - 3) = 14$\n\nNo puedes 'pasar' el $-3$ al otro lado todavía, porque está atrapado dentro de la fortaleza del paréntesis, y el $2$ es el guardia en la puerta.\n\nPara liberar a los términos, el guardia ($2$) multiplica a todos:\n$2 \\cdot (x) - 2 \\cdot (3) = 14$\n$2x - 6 = 14$\n\n¡Listo! El paréntesis desapareció. Ahora es una ecuación normal y corriente.\n- Pasa el $-6$ como $+6$: $2x = 20$\n- Pasa el $2$ dividiendo: $x = 10$\n\nSi hubiera múltiples signos de agrupación (ej. llaves y corchetes), se destruyen de adentro hacia afuera.",
    "proc": [
        "Paso 1: Localiza el número y signo que están inmediatamente a la izquierda del paréntesis.",
        "Paso 2: Multiplica ese número por el primer término de adentro.",
        "Paso 3: Multiplica ese número por el segundo término (respeta la ley de los signos).",
        "Paso 4: Escribe la nueva ecuación sin paréntesis y procede a reducir términos semejantes."
    ],
    "ex_a": [
        ("Ejemplo 1", "Resuelve: $3(2x + 1) = 21$", ["Distribuimos el 3: $3(2x) + 3(1) = 21$.", "$6x + 3 = 21$.", "Pasamos el 3 restando: $6x = 18$.", "Dividimos por 6: $x = 3$."])
    ],
    "ex_b": [
        ("Resuelve la ecuación $4(x - 2) = x + 7$", "$x = 5$", ["Distribuye: 4x - 8 = x + 7.", "Trae las x a un lado: 4x - x = 7 + 8.", "Reduce: 3x = 15.", "Despeja: x = 5."])
    ],
    "errs": [
        "Distribuir el número solo al primer término del paréntesis y olvidar el segundo (ej: $2(x+3)$ -> $2x+3$). ¡Error súper común!",
        "Pasar un término que está dentro del paréntesis sumando al otro lado de la ecuación antes de eliminar el paréntesis."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué propiedad matemática permite 'eliminar' los paréntesis multiplicando el factor externo por cada término interno?", "choices": ["A) Propiedad Asociativa.", "B) Propiedad Conmutativa.", "C) Propiedad Distributiva.", "D) Propiedad Cancelativa."], "ans": "C) Propiedad Distributiva.", "sol": "El factor se 'distribuye' a cada uno de los sumandos del interior."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al aplicar la propiedad distributiva correctamente para eliminar los paréntesis en $5(3x - 4) = 10$, la ecuación queda como:", "choices": ["A) $15x - 4 = 10$", "B) $15x - 20 = 10$", "C) $8x - 9 = 10$", "D) $15x + 20 = 10$"], "ans": "B) $15x - 20 = 10$", "sol": "El 5 multiplica al 3x (da 15x) y también multiplica al -4 (da -20)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "En la ecuación $2(x - 5) = 12$, es válido pasar el 5 sumando al lado derecho en el primer paso para obtener $2x = 17$.", "ans": "Falso", "sol": "El -5 está encerrado en el paréntesis, afectado por la multiplicación. Tienes que distribuir el 2 primero (da 2x - 10), o pasar el 2 dividiendo."}
    ]
})

# 14. PARENTESIS_NEGATIVO
nodes.append({
    "sid": "MAT.ALG.RESOLUCION_LINEAL.PARENTESIS_NEGATIVO",
    "title": "El Peligro del Paréntesis Precedido por un Signo Menos",
    "obj": "Cambiar correctamente los signos de todos los términos dentro de un paréntesis que está precedido por una resta.",
    "intro": "Si hay un 'asesino silencioso' en los exámenes de álgebra, es el signo menos antes de un paréntesis. Ha arruinado más notas perfectas que cualquier otro error matemático.",
    "res": "Cuando un paréntesis está precedido por un signo menos ($-$), al eliminar el paréntesis se DEBEN CAMBIAR LOS SIGNOS de TODOS los términos de su interior.",
    "expl": "Fíjate en esto: $10 - (2x + 4) = 0$\n\nEse signo $-$ no solo afecta al $2x$. Ese signo menos es en realidad un $-1$ disfrazado que está multiplicando a todo el paréntesis.\nSi aplicas la propiedad distributiva con $-1$:\n- El $2x$ positivo se vuelve negativo: $-2x$\n- El $+4$ se vuelve negativo: $-4$\n\nLa ecuación liberada queda: $10 - 2x - 4 = 0$.\n\nSi el interior tuviera un negativo, por ejemplo $-(x - 5)$, la regla de los signos (menos por menos da más) lo transforma en $-x + 5$.\n\nLa regla de oro: Un 'menos' afuera invierte TODOS los signos de adentro. Un 'más' afuera deja todos los signos exactamente igual.",
    "proc": [
        "Paso 1: Detecta el signo $-$ antes del paréntesis.",
        "Paso 2: Borra el signo menos y los paréntesis.",
        "Paso 3: Escribe cada término del interior pero con su signo opuesto (+ cambia a -, y - cambia a +).",
        "Paso 4: Continúa reduciendo términos como de costumbre."
    ],
    "ex_a": [
        ("Ejemplo 1", "Elimina el paréntesis y resuelve: $8 - (x - 2) = 12$", ["El signo menos afecta a la 'x' y al '-2'.", "Queda: $8 - x + 2 = 12$.", "Reducimos: $10 - x = 12$.", "Despejamos: $-x = 12 - 10 \\rightarrow -x = 2$.", "Cambiamos signo a todo: $x = -2$."])
    ],
    "ex_b": [
        ("Resuelve $5x - (2x + 9) = 6$", "$x = 5$", ["5x - 2x - 9 = 6", "3x - 9 = 6", "3x = 15", "x = 5"])
    ],
    "errs": [
        "El error más clásico: Cambiar el signo solo del primer término y copiar el segundo igual. Ej: $-(x+5)$ -> $-x+5$ (Incorrecto, es $-x-5$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "Al remover los paréntesis de la expresión algebraica $-(3x - 7)$, el resultado correcto aplicando las leyes de los signos es:", "choices": ["A) $-3x - 7$", "B) $3x + 7$", "C) $-3x + 7$", "D) $3x - 7$"], "ans": "C) $-3x + 7$", "sol": "El menos de afuera invierte el signo del 3x positivo (queda -3x) y el del -7 (queda +7)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "¿Cuál es la ecuación equivalente correcta a $2x - (x - 1) = 5$ luego de destruir los signos de agrupación?", "choices": ["A) $2x - x - 1 = 5$", "B) $2x - x + 1 = 5$", "C) $x - 1 = 5$", "D) $3x - 1 = 5$"], "ans": "B) $2x - x + 1 = 5$", "sol": "El - afecta a x dejándolo como -x, y afecta a -1 convirtiéndolo en +1 por la regla de signos (menos por menos)."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Si un paréntesis tiene un signo '+' antes de él, ej: $+(2x - 5)$, basta con borrar los paréntesis sin modificar ningún signo interior.", "ans": "Verdadero", "sol": "El signo '+' actúa como un +1 multiplicando. Multiplicar por 1 positivo no altera ningún signo ni valor."}
    ]
})

# 15. INCOGNITA_AMBOS_MIEMBROS
nodes.append({
    "sid": "MAT.ALG.RESOLUCION_LINEAL.INCOGNITA_AMBOS_MIEMBROS",
    "title": "Incógnitas en Ambos Miembros",
    "obj": "Agrupar todas las incógnitas en un lado de la ecuación y los números en el otro.",
    "intro": "A veces, las manzanas están repartidas en ambos platillos de la balanza. Para saber cuánto pesa una, primero debemos juntarlas todas en un solo platillo.",
    "res": "Cuando una ecuación tiene la incógnita (la misma letra) en el primer y en el segundo miembro, se deben transponer los términos para que todas las letras queden de un lado (usualmente a la izquierda) y los números del otro (a la derecha).",
    "expl": "Observa: $5x - 4 = 2x + 11$\n\nHay 'x' a la izquierda y a la derecha. ¿Qué hacemos? Organizar.\n1. Decidimos un lado para las 'x'. Generalmente se elige el izquierdo.\n2. Traemos el $2x$ del lado derecho hacia el izquierdo. Como el $2x$ es positivo, cruza el portal restando ($-2x$).\n3. Llevamos el $-4$ del lado izquierdo hacia el derecho de los números. Cruzará sumando ($+4$).\n\nNuestra ecuación se convierte en:\n$5x - 2x = 11 + 4$\n\nAhora, el problema es súper fácil. Reducimos:\n$3x = 15$\n$x = \\frac{15}{3} = 5$.\n\n*Tip pro:* Siempre conviene pasar la incógnita menor hacia el lado donde está la incógnita mayor. Así evitas trabajar con números negativos, ¡y menos signos negativos significan menos probabilidad de error!",
    "proc": [
        "Paso 1: Identifica los términos que tienen letra en ambos miembros.",
        "Paso 2: Transpón el término con letra de menor coeficiente hacia el otro miembro (cambiando su signo).",
        "Paso 3: Transpón los términos independientes (números) hacia el miembro opuesto.",
        "Paso 4: Reduce términos semejantes en ambos miembros.",
        "Paso 5: Despeja dividiendo."
    ],
    "ex_a": [
        ("Ejemplo 1", "Resuelve: $8x + 2 = 5x + 14$", ["El 5x es menor, lo movemos a la izquierda restando.", "$8x - 5x + 2 = 14$", "El +2 lo movemos a la derecha restando.", "$8x - 5x = 14 - 2$", "Reducimos: $3x = 12$", "Dividimos: $x = 4$."])
    ],
    "ex_b": [
        ("Resuelve $x - 7 = 3x - 19$", "$x = 6$", ["Movemos la x: -7 = 2x - 19", "Movemos -19: 12 = 2x", "x = 6"])
    ],
    "errs": [
        "Sumar las 'x' de ambos lados como si estuvieran en el mismo miembro (ej. en $3x = 2x + 5$, sumar $3x+2x = 5x$). Deben cruzarse cambiando el signo primero."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Si en la ecuación $6x + 5 = 2x + 17$ decides agrupar las incógnitas en el lado izquierdo, el término $2x$ del lado derecho debe moverse como:", "choices": ["A) $+2x$", "B) $-2x$", "C) Dividiendo por $2$", "D) Multiplicando por $2$"], "ans": "B) $-2x$", "sol": "El 2x es positivo y está sumando en su miembro. Al transponerlo al miembro izquierdo, debe cruzar restando."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Para evitar trabajar con coeficientes negativos en la ecuación $2x + 10 = 7x - 5$, el paso más astuto sería mover:", "choices": ["A) El $7x$ hacia la izquierda.", "B) El $2x$ hacia la derecha.", "C) El $10$ hacia la derecha y el $-5$ a la izquierda.", "D) Dividir todo por 2."], "ans": "B) El $2x$ hacia la derecha.", "sol": "Si mueves el 2x a la derecha quedará 7x - 2x = 5x positivo. Si mueves el 7x a la izquierda, quedará 2x - 7x = -5x negativo."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "En una ecuación, es estrictamente obligatorio agrupar las incógnitas siempre en el lado izquierdo.", "ans": "Falso", "sol": "La igualdad es simétrica. Puedes agrupar las letras en el lado derecho si resulta más conveniente. Decir x=5 es idéntico a decir 5=x."}
    ]
})

# 16. COEFICIENTE_NEGATIVO
nodes.append({
    "sid": "MAT.ALG.RESOLUCION_LINEAL.COEFICIENTE_NEGATIVO",
    "title": "Manejo del Coeficiente Negativo",
    "obj": "Aprender el truco matemático de multiplicar la ecuación completa por -1 cuando la incógnita queda negativa.",
    "intro": "Has hecho todo bien, pero al final del problema te topas con que tu 'x' quedó con un molesto signo negativo (ej: $-x = 8$). No hemos terminado. La respuesta debe ser de 'x', no de 'anti-x'.",
    "res": "Si al final del despeje el término con la incógnita queda negativo, se debe multiplicar (o dividir) TODA la ecuación por $-1$ para cambiar el signo de todos los términos y hacer positiva a la incógnita.",
    "expl": "Imagínate que al resolver una ecuación llegas a este punto:\n$-3x = 15$\n\nTienes dos formas legítimas de proceder:\n\n**Método 1 (El paso natural):**\nRecuerda que el $-3$ está multiplicando. Simplemente pásalo dividiendo con todo y su signo:\n$x = \\frac{15}{-3}$\n$x = -5$\n\n**Método 2 (El truco del -1):**\nA muchos no les gusta mover el negativo. Entonces, multiplicas la ecuación completa por $(-1)$.\n$(-1) \\cdot (-3x) = (-1) \\cdot (15)$\n$3x = -15$\nAhora el $3$ pasa dividiendo positivo:\n$x = \\frac{-15}{3} \\rightarrow x = -5$.\n\nSi llegas a $-x = 7$, el Método 2 es perfecto. Multiplicas todo por $-1$ y queda directamente $x = -7$.",
    "proc": [
        "Paso 1: Si tienes $-x = [número]$, simplemente invierte el signo de ambos lados de la igualdad.",
        "Paso 2: Si tienes un número negativo (como $-4x$), puedes dividir el otro lado directamente por ese número negativo (ej. $12 / -4$).",
        "Paso 3: Verifica que en el resultado final, la 'x' esté positiva y solitaria."
    ],
    "ex_a": [
        ("Ejemplo 1", "Despeja: $10 - x = 14$", ["Pasamos el 10 restando: $-x = 14 - 10$.", "Queda: $-x = 4$.", "Multiplicamos la ecuación por (-1): $x = -4$."])
    ],
    "ex_b": [
        ("¿Cuál es el valor de 'x' si $-2x = -18$?", "$x = 9$", ["Se puede dividir -18 entre -2. Menos por menos da más. x = 9."])
    ],
    "errs": [
        "Llegar a $-x = 5$ y dejar eso como respuesta final, pensando que ya se resolvió.",
        "Pasar el coeficiente negativo sumando (ej: $-3x = 12 \\rightarrow x = 12 + 3$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Si al final del desarrollo de una ecuación obtienes $-x = 10$, ¿cuál es el paso matemático formal para obtener el valor de $x$?", "choices": ["A) Multiplicar ambos miembros por $-1$ (o dividir por $-1$).", "B) Mover el signo menos al otro lado como suma.", "C) Elevar al cuadrado para matar el signo.", "D) Dejarlo así, ya está resuelto."], "ans": "A) Multiplicar ambos miembros por $-1$ (o dividir por $-1$).", "sol": "Multiplicar todo por -1 es la operación válida que invierte los signos y vuelve positiva la incógnita."},
        {"group": "reconocimiento", "diff": "media", "prompt": "En el paso final de una ecuación tenemos $-5x = 20$. ¿Cuál es el valor correcto de x?", "choices": ["A) $x = 25$", "B) $x = 4$", "C) $x = -4$", "D) $x = -25$"], "ans": "C) $x = -4$", "sol": "El -5 pasa dividiendo. 20 dividido entre -5 da -4 por la regla de los signos."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Multiplicar una ecuación completa por $(-1)$ es ilegal porque rompe el equilibrio de la igualdad.", "ans": "Falso", "sol": "La propiedad multiplicativa permite multiplicar por CUALQUIER número, incluido el -1. Como se hace a ambos lados, el equilibrio matemático se conserva perfectamente."}
    ]
})

# 17. VERIFICACION_SOLUCION
nodes.append({
    "sid": "MAT.ALG.RESOLUCION_LINEAL.VERIFICACION_SOLUCION",
    "title": "Verificación (Comprobación) de una Ecuación",
    "obj": "Comprobar la certeza de un resultado matemático sustituyéndolo de regreso en la ecuación original.",
    "intro": "Las ecuaciones tienen algo maravilloso que casi ningún otro tema de matemáticas tiene: te permiten 'revisar tu propio examen' antes de entregarlo. Si haces la comprobación, sabrás con 100% de certeza si tu nota es un 7.",
    "res": "La verificación consiste en sustituir el valor obtenido como respuesta en el lugar de la incógnita en la ecuación ORIGINAL. Si se obtiene una igualdad numérica verdadera (ej: $10 = 10$), la solución es correcta.",
    "expl": "Paso 1: Resuelves la ecuación.\nSupón que resolviste $3x - 2 = x + 6$ y concluiste que $x = 4$.\n\nPaso 2: La prueba de fuego.\nTomas tu $4$ y lo metes en la ecuación inicial. ¡Nunca en los pasos intermedios, siempre en la original por si arrastraste un error!\n\nLado Izquierdo: $3(4) - 2 = 12 - 2 = 10$.\nLado Derecho: $(4) + 6 = 10$.\n\nPaso 3: Compara.\n¿Es $10 = 10$? ¡Sí! Tu respuesta es correcta y absoluta.\n¿Qué pasa si hubiera dado $8 = 10$? Significaría que te equivocaste despejando, algún signo falló y debes revisar tu procedimiento.",
    "proc": [
        "Paso 1: Termina de resolver la ecuación y obtén tu posible solución.",
        "Paso 2: Copia la ecuación ORIGINAL.",
        "Paso 3: Sustituye la incógnita en todos los lados por tu número, usando paréntesis.",
        "Paso 4: Calcula el valor de cada lado de manera independiente (no cruces números de un lado a otro).",
        "Paso 5: Si los dos números finales son iguales, has verificado exitosamente."
    ],
    "ex_a": [
        ("Ejemplo 1", "Verifica si $x = -2$ es solución de $5x + 3 = -7$.", ["Sustituimos -2 en la ecuación: $5(-2) + 3$.", "Calculamos lado izquierdo: $-10 + 3 = -7$.", "Comparamos con el lado derecho: $-7$.", "$-7 = -7$. La solución es correcta."])
    ],
    "ex_b": [
        ("Si al verificar $x=1$ en una ecuación obtengo $5 = 6$, ¿qué concluyo?", "Que $x=1$ no es la solución correcta.", ["La balanza está desequilibrada. Hay un error en el despeje."])
    ],
    "errs": [
        "Verificar el resultado en el segundo o tercer paso de la resolución (si te equivocaste en el primer paso, ¡la verificación dirá que está bien siendo un resultado malo!). Siempre usar la primera línea."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Por qué es crucial realizar la verificación sustituyendo en la ecuación ORIGINAL del problema y no en un paso intermedio del despeje?", "choices": ["A) Porque es la única que tiene letras.", "B) Porque si cometiste un error algebraico en el primer paso, la verificación intermedia no lo detectará.", "C) Para practicar más la multiplicación.", "D) Porque los pasos intermedios siempre son incorrectos."], "ans": "B) Porque si cometiste un error algebraico en el primer paso, la verificación intermedia no lo detectará.", "sol": "Un error temprano corrompe la ecuación. Comprobar en una ecuación corrompida te dará un falso positivo."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un estudiante resuelve $2(x - 3) = 4x - 10$ y obtiene $x = 2$. Al realizar la comprobación, evalúa el lado izquierdo y el lado derecho. ¿Qué par de valores numéricos obtiene y qué concluye?", "choices": ["A) Obtiene $-2 = -2$, por lo que concluye que su respuesta es correcta.", "B) Obtiene $-2 = 2$, por lo que concluye que hay un error.", "C) Obtiene $1 = 1$, por lo que es correcta.", "D) Obtiene $-2 = -8$, por lo que hay un error."], "ans": "A) Obtiene $-2 = -2$, por lo que concluye que su respuesta es correcta.", "sol": "Si reemplaza x=2: Izquierda -> 2(2-3) = 2(-1) = -2. Derecha -> 4(2)-10 = 8-10 = -2. Ambos lados dan -2, la respuesta estaba correcta."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Durante la fase de verificación, está prohibido transponer o despejar términos; solo debes realizar operaciones aritméticas puras (sumar, multiplicar, etc.) en cada lado por separado.", "ans": "Verdadero", "sol": "Así es. Se evalúa el valor numérico del miembro izquierdo por sí solo, y el derecho por sí solo, para ver si son idénticos."}
    ]
})

# 18. DETECCION_ERROR_TRANSPOSICION
nodes.append({
    "sid": "MAT.ALG.RESOLUCION_LINEAL.DETECCION_ERROR_TRANSPOSICION",
    "title": "Detección de Errores Comunes en Transposición",
    "obj": "Identificar y corregir los errores clásicos de transposición de términos y operaciones inversas.",
    "intro": "Para ser un maestro del álgebra, no solo debes saber cómo hacerlo bien, sino también saber exactamente cómo y por qué se equivocan los demás. Analizar errores ajenos es el mejor entrenamiento.",
    "res": "Los errores más críticos ocurren al: 1) olvidar cambiar el signo al mover un sumando, 2) alterar el signo de un coeficiente cuando pasa dividiendo, 3) no respetar la jerarquía (separar productos antes que sumas).",
    "expl": "Vamos a ser auditores matemáticos. Revisa este 'desarrollo' erróneo paso a paso:\n\n**Ecuación:** $2x - 5 = 7$\n- *Paso 1 del estudiante:* $2x = 7 - 5$ (¡ERROR 1!)\n  *Corrección:* El $-5$ estaba restando, debió pasar sumando como $+5$.\n- *Paso 2 del estudiante (asumiendo que $2x = 2$):* $x = \\frac{2}{-2}$ (¡ERROR 2!)\n  *Corrección:* El $2$ multiplicaba positivo. Pasa dividiendo como $2$ positivo, ¡no cambia de signo, cambia de operación!\n\nOtro clásico:\n**Ecuación:** $\\frac{x - 1}{3} = 4$\n- *Paso 1 del estudiante:* $\\frac{x}{3} = 4 + 1$ (¡ERROR 3!)\n  *Corrección:* El $-1$ no está libre, está atrapado arriba en la fracción (dividido por 3). Primero hay que pasar el $3$ multiplicando al otro lado.\n\nAprender a auditar estos pasos te evitará cometerlos en tus pruebas de estrés (como la PAES).",
    "proc": [
        "Paso 1: Revisa el movimiento de términos sumando/restando. ¿Cambiaron a su signo opuesto al saltar el '='?",
        "Paso 2: Revisa el movimiento de coeficientes multiplicando/dividiendo. ¿Conservaron su signo original pero cambiaron su operación matemática?",
        "Paso 3: Revisa la jerarquía. ¿El término movido estaba 'libre' para moverse, o estaba atrapado por una división o multiplicación mayor?"
    ],
    "ex_a": [
        ("Ejemplo 1", "Audita el siguiente paso: $4 - x = 10 \\rightarrow x = 10 - 4$. ¿Hay un error?", ["Sí, hay error de arrastre de signo.", "El 4 positivo pasó restando (-4), eso está bien.", "Pero el estudiante ignoró que la 'x' tenía un signo menos, dejándola como 'x' positiva.", "Lo correcto era: $-x = 10 - 4$."])
    ],
    "ex_b": [
        ("Identifica el error en $3(x + 2) = 15 \\rightarrow x + 2 = 15 - 3$", "Pasó el 3 restando.", ["El 3 estaba multiplicando al paréntesis. Debió pasar DIVIDIENDO al 15."])
    ],
    "errs": [
        "Inventar 'super-reglas', como 'cuando pasa al otro lado SIEMPRE cambia de signo' (lo cual arruina las divisiones, donde el signo se conserva)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "Al transponer un factor que está multiplicando hacia el otro miembro para dividir, ¿qué ocurre con su signo (positivo o negativo)?", "choices": ["A) Siempre se convierte en positivo.", "B) Debe invertirse: si era positivo queda negativo y viceversa.", "C) Se conserva exactamente igual, porque la operación que cambia es la multiplicación a división, no el signo.", "D) Se cancela."], "ans": "C) Se conserva exactamente igual, porque la operación que cambia es la multiplicación a división, no el signo.", "sol": "Esta es la corrección al error más extendido. Un número como -5 que multiplica, pasa como el número -5 dividiendo."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Un alumno desarrolla la ecuación $5 - 2x = 11$ de la siguiente manera:\nPaso 1: $-2x = 11 + 5$\nPaso 2: $-2x = 16$\nPaso 3: $x = \\frac{16}{2}$\nPaso 4: $x = 8$\n\n¿En qué paso cometió el primer error algebraico?", "choices": ["A) En el Paso 1", "B) En el Paso 2", "C) En el Paso 3", "D) En el Paso 4"], "ans": "A) En el Paso 1", "sol": "En el Paso 1 transpuso el 5 positivo como +5. Debió haber sido 11 - 5."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "En la ecuación $\\frac{x + 2}{5} = 4$, el movimiento correcto inicial es pasar el $+2$ restando hacia el lado derecho.", "ans": "Falso", "sol": "La fracción completa obliga primero a eliminar el denominador. Primero el 5 pasa multiplicando, dejando x + 2 = 20."}
    ]
})


with open("docs/conocimiento/ejercicios/mat-alg-ecuaciones-banco-gen-2.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

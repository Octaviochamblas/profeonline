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
    filename = "docs/conocimiento/ejercicios/mat-alg-ecuaciones-banco-gen-1.jsonl"
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

# 1. DEFINICION_IGUALDAD
nodes.append({
    "sid": "MAT.ALG.ECUACION_BASE.DEFINICION_IGUALDAD",
    "title": "Concepto de Igualdad Matemática",
    "obj": "Comprender la igualdad matemática como una balanza en perfecto equilibrio.",
    "intro": "Antes de correr, hay que caminar. Y antes de resolver ecuaciones, hay que entender qué significa el signo más famoso de las matemáticas: el igual ($=$). No es una orden para 'calcular el resultado', es una declaración de equilibrio.",
    "res": "Una igualdad matemática es una afirmación que establece que dos expresiones tienen exactamente el mismo valor numérico o algebraico.",
    "expl": "¿Qué significa realmente escribir $A = B$?\nSignifica que, aunque se vean distintos, lo que está a la izquierda pesa exactamente lo mismo que lo que está a la derecha.\n\nPiensa en una balanza antigua de dos platillos. Si tienes 5 kilos de plomo a la izquierda y 5 kilos de plumas a la derecha, la balanza no se mueve. Visualmente son diferentes, pero en 'valor' son idénticos.\n\nExisten dos tipos de igualdades básicas:\n1. **Igualdades Numéricas:** Tienen solo números. Ej: $3 + 2 = 5$. Esto es siempre verdadero.\n2. **Igualdades Algebraicas:** Tienen letras (variables). Ej: $x + 2 = 5$. Esta igualdad depende del valor que tome la $x$ para ser verdadera o falsa.\n\nEl signo $=$ actúa como el pivote central de esta balanza. Todo lo que hagas a un lado, deberás hacerlo al otro para mantener ese delicado equilibrio.",
    "proc": [
        "Paso 1: Identifica el signo $=$ como el centro de la expresión.",
        "Paso 2: Reconoce todo lo que está a la izquierda como la 'expresión izquierda' (peso izquierdo).",
        "Paso 3: Reconoce todo lo que está a la derecha como la 'expresión derecha' (peso derecho).",
        "Paso 4: Entiende que ambas expresiones representan la misma cantidad total."
    ],
    "ex_a": [
        ("Ejemplo 1", "¿La expresión $4 \\cdot 2 = 10 - 2$ es una igualdad verdadera?", ["Lado izquierdo: $4 \\cdot 2 = 8$.", "Lado derecho: $10 - 2 = 8$.", "Ambos lados valen 8. Por lo tanto, $8 = 8$, la igualdad es verdadera y está en equilibrio."])
    ],
    "ex_b": [
        ("¿Es la expresión $x + y$ una igualdad?", "No", ["Falta el signo igual y otra expresión al otro lado. Solo es una expresión algebraica suelta, no una igualdad."])
    ],
    "errs": [
        "Creer que el signo = significa 'aquí va la respuesta'.",
        "Confundir una expresión algebraica simple (ej. $2x+3$) con una igualdad (ej. $2x+3=0$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "En matemáticas, el signo de igualdad ($=$) indica que:", "choices": ["A) Se debe calcular la operación de la izquierda para poner el resultado a la derecha.", "B) Las expresiones de ambos lados tienen exactamente el mismo valor.", "C) El lado izquierdo es mayor que el derecho.", "D) Las expresiones son idénticas en su forma escrita."], "ans": "B) Las expresiones de ambos lados tienen exactamente el mismo valor.", "sol": "El signo = declara que ambas cantidades, aunque estén escritas de forma distinta, representan la misma magnitud o valor."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Cuál de las siguientes opciones representa una igualdad matemática verdadera?", "choices": ["A) $3 + 4 = 8$", "B) $x + 2$", "C) $5 \\cdot 3 = 10 + 5$", "D) $2 > 1$"], "ans": "C) $5 \\cdot 3 = 10 + 5$", "sol": "15 a la izquierda y 15 a la derecha. Ambas pesan lo mismo. B no es igualdad, D es desigualdad, A es falsa."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Toda expresión matemática que contenga números y letras es automáticamente una igualdad.", "ans": "Falso", "sol": "Si no tiene el signo '=', es solo una expresión (un polinomio o monomio), no una igualdad."}
    ]
})

# 2. DEFINICION_ECUACION
nodes.append({
    "sid": "MAT.ALG.ECUACION_BASE.DEFINICION_ECUACION",
    "title": "Definición de Ecuación",
    "obj": "Diferenciar una ecuación de otras igualdades, comprendiendo que su veracidad depende de incógnitas específicas.",
    "intro": "No todas las igualdades son ecuaciones. Una ecuación es como un candado con clave: es una igualdad que solo 'se abre' o es cierta si usas el número secreto correcto.",
    "res": "Una ecuación es una igualdad algebraica que contiene letras (incógnitas) y que solo es verdadera para valores muy específicos de dichas letras.",
    "expl": "Vamos a diseccionar esto:\n- Si escribo $2 + 2 = 4$, es una **igualdad numérica**. Siempre es verdad, no hay misterio.\n- Si escribo $x + 2 = 5$, ¡ahí hay un misterio! La letra $x$ es una incógnita. Esta expresión se llama **ecuación**.\n\n¿Por qué es especial?\nPorque su equilibrio es 'condicional'. Imagina que la balanza está tapada. ¿Es cierto que el lado izquierdo pesa igual que el derecho?\n- Si adivinas que $x = 1$, tendrías $1 + 2 = 5$. Esto es falso. La balanza se inclina.\n- Si adivinas que $x = 3$, tendrías $3 + 2 = 5$. Esto es cierto. ¡Equilibrio perfecto!\n\nEntonces, una ecuación es una pregunta matemática disfrazada de afirmación: '¿Qué valor debe tener la $x$ para que este lado sea idéntico al otro?'",
    "proc": [
        "Paso 1: Busca el signo $=$ para confirmar que es una igualdad.",
        "Paso 2: Busca letras (variables o incógnitas).",
        "Paso 3: Pregúntate: '¿Esta igualdad depende de la letra para ser cierta?'. Si la respuesta es sí, es una ecuación."
    ],
    "ex_a": [
        ("Ejemplo 1", "Clasifica: $3x - 1 = 8$", ["Tiene signo '=': Es igualdad.", "Tiene incógnita 'x': Es algebraica.", "Solo es cierta si $x=3$ (pues $3(3)-1=8$).", "Conclusión: Es una ecuación."])
    ],
    "ex_b": [
        ("¿La expresión $x + x = 2x$ es una ecuación?", "No, es una identidad", ["Aunque tiene letras, es cierta para CUALQUIER valor de x (si x=1, 2=2; si x=5, 10=10). Las ecuaciones suelen ser ciertas solo para valores específicos."])
    ],
    "errs": [
        "Llamar 'ecuación' a cualquier cosa que tenga una 'x', incluso si no tiene signo igual."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Una ecuación se define formalmente como:", "choices": ["A) Una expresión algebraica sin signo igual.", "B) Una igualdad numérica siempre verdadera.", "C) Una igualdad que contiene una o más incógnitas y se cumple solo para ciertos valores de estas.", "D) Una multiplicación de polinomios."], "ans": "C) Una igualdad que contiene una o más incógnitas y se cumple solo para ciertos valores de estas.", "sol": "Esa es la diferencia clave: depende del valor de la incógnita para ser verdad."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál de las siguientes expresiones clasifica estrictamente como una ecuación (que requiere resolución para hallar su incógnita)?", "choices": ["A) $2x + 5$", "B) $4 + 5 = 9$", "C) $x^2 + 1 = 10$", "D) $a + b = b + a$"], "ans": "C) $x^2 + 1 = 10$", "sol": "A no es igualdad. B es identidad numérica. D es una propiedad (identidad) que se cumple para todo a y b. C solo se cumple si x=3 o x=-3, es una ecuación."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Una ecuación plantea una condición que las incógnitas deben cumplir para que la balanza se mantenga equilibrada.", "ans": "Verdadero", "sol": "Esa es la mejor manera de interpretar una ecuación: como una condición de equilibrio."}
    ]
})

# 3. DIFERENCIA_IDENTIDAD
nodes.append({
    "sid": "MAT.ALG.ECUACION_BASE.DIFERENCIA_IDENTIDAD",
    "title": "Ecuación vs Identidad",
    "obj": "Distinguir entre una ecuación (condicional) y una identidad (absoluta).",
    "intro": "Hay dos tipos de frases algebraicas que usan el signo igual. Una es un misterio que hay que resolver (la ecuación). La otra es un hecho irrefutable que siempre es verdad (la identidad).",
    "res": "Una ecuación se cumple solo para algunos valores de la incógnita. Una identidad se cumple para ABSOLUTAMENTE TODOS los valores de la incógnita.",
    "expl": "Piénsalo así:\n- **Ecuación (Condicional):** $x + 2 = 5$.\n  Pregunta: ¿Cuándo es verdad esto? Solo cuando $x=3$. Si $x$ es otro número, es mentira.\n\n- **Identidad (Absoluta):** $x + x = 2x$.\n  Pregunta: ¿Cuándo es verdad esto?\n  - Si $x = 1$, $1+1 = 2(1) \\rightarrow 2=2$. Verdad.\n  - Si $x = 10$, $10+10 = 2(10) \\rightarrow 20=20$. Verdad.\n  - Si $x = -5$, $-5-5 = 2(-5) \\rightarrow -10=-10$. Verdad.\n  ¡Es verdad para siempre y para cualquier número! Eso es una identidad.\n\nLos Productos Notables (ej. $(a+b)^2 = a^2 + 2ab + b^2$) son identidades. No se 'resuelven', se 'aplican', porque son una verdad universal sin importar cuánto valgan 'a' y 'b'.",
    "proc": [
        "Paso 1: Observa la igualdad algebraica.",
        "Paso 2: Intenta resolverla o simplificarla al máximo.",
        "Paso 3: Si al simplificar ambos lados te queda algo como $x = 3$, es una ecuación.",
        "Paso 4: Si al simplificar llegas a algo como $x = x$ o $0 = 0$, significa que es una identidad."
    ],
    "ex_a": [
        ("Ejemplo 1", "Determina si $2(x + 1) = 2x + 2$ es ecuación o identidad.", ["Desarrolla el lado izquierdo multiplicando: $2x + 2$.", "Compara con el derecho: $2x + 2 = 2x + 2$.", "Son exactamente iguales en estructura. Cualquier valor de x funcionará.", "Es una Identidad."])
    ],
    "ex_b": [
        ("Clasifica: $3x = 15$.", "Ecuación", ["Solo se cumple si x=5. No es universal."])
    ],
    "errs": [
        "Tratar de resolver una identidad y frustrarse al llegar a $0 = 0$, pensando que se cometió un error."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Qué sucede invariablemente si intentas resolver algebraicamente una identidad?", "choices": ["A) Llegas a un resultado fraccionario.", "B) Las incógnitas se cancelan y llegas a una afirmación verdadera como $0 = 0$ o $5 = 5$.", "C) Llegas a una contradicción como $0 = 1$.", "D) Llegas a que $x = 0$."], "ans": "B) Las incógnitas se cancelan y llegas a una afirmación verdadera como $0 = 0$ o $5 = 5$.", "sol": "Como es verdad para toda x, la x 'desaparece' del cálculo, dejándote con una verdad absoluta."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál de las siguientes es una identidad algebraica?", "choices": ["A) $2x - 1 = 7$", "B) $x^2 = 16$", "C) $x(x - 2) = x^2 - 2x$", "D) $\\frac{x}{2} = 4$"], "ans": "C) $x(x - 2) = x^2 - 2x$", "sol": "Al distribuir la x de la izquierda se obtiene x^2 - 2x, que es idéntico a la derecha. Cierto para cualquier x."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Una expresión como $(x+y)(x-y) = x^2 - y^2$ es considerada una ecuación que debemos despejar.", "ans": "Falso", "sol": "Es un producto notable, lo que la clasifica matemáticamente como una Identidad. No se despeja, es una regla universal."}
    ]
})

# 4. MIEMBROS_ECUACION
nodes.append({
    "sid": "MAT.ALG.ECUACION_BASE.MIEMBROS_ECUACION",
    "title": "Miembros de una Ecuación",
    "obj": "Identificar y nombrar correctamente las dos mitades principales de una ecuación.",
    "intro": "Para hablar el lenguaje del álgebra fluido, necesitas saber cómo llamar a las partes de una ecuación. Cuando hablemos de 'pasar de un lado a otro', debemos usar los nombres oficiales.",
    "res": "Toda ecuación está dividida por el signo igual ($=$) en dos bloques principales: el Primer Miembro (a la izquierda) y el Segundo Miembro (a la derecha).",
    "expl": "Dada la ecuación: $3x + 4 = 2x - 1$\n\n- **El Signo Igual ($=$)** es la frontera, el muro que divide los dos países.\n- **Primer Miembro (Miembro Izquierdo):** Es TODO lo que está a la izquierda del $=$. En este caso, $3x + 4$.\n- **Segundo Miembro (Miembro Derecho):** Es TODO lo que está a la derecha del $=$. En este caso, $2x - 1$.\n\nEs fundamental ver estos miembros como 'paquetes' completos. Si multiplicas la ecuación por 2, debes multiplicar TODO el primer miembro y TODO el segundo miembro. No puedes multiplicar partes sueltas.",
    "proc": [
        "Paso 1: Localiza el signo $=$.",
        "Paso 2: Todo el bloque a su izquierda es el Primer Miembro.",
        "Paso 3: Todo el bloque a su derecha es el Segundo Miembro."
    ],
    "ex_a": [
        ("Ejemplo 1", "Identifica los miembros en $5 - x = 12 + 3x$.", ["Frontera: el signo $=$.", "Primer Miembro (izquierdo): $5 - x$.", "Segundo Miembro (derecho): $12 + 3x$."])
    ],
    "ex_b": [
        ("En la ecuación $x^2 = 25$, ¿cuál es el segundo miembro?", "25", ["Es lo que está a la derecha del igual."])
    ],
    "errs": [
        "Confundir 'miembro' con 'término'. (Un miembro contiene varios términos)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "En una ecuación, la expresión matemática completa que se encuentra a la izquierda del signo igual se denomina:", "choices": ["A) Primer término.", "B) Coeficiente principal.", "C) Primer Miembro.", "D) Incógnita izquierda."], "ans": "C) Primer Miembro.", "sol": "Es el nombre formal en álgebra para todo el bloque izquierdo."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "En la ecuación $\\frac{x}{2} + 5 = 10 - x$, ¿cuál es exactamente el Segundo Miembro?", "choices": ["A) $10$", "B) $10 - x$", "C) $-x$", "D) $\\frac{x}{2} + 5$"], "ans": "B) $10 - x$", "sol": "El segundo miembro comprende TODO lo que está a la derecha de la igualdad."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Una ecuación siempre debe tener incógnitas en ambos miembros.", "ans": "Falso", "sol": "Puede tener la incógnita en un solo miembro, como en x + 2 = 5, y sigue siendo una ecuación válida."}
    ]
})

# 5. TERMINOS_ECUACION
nodes.append({
    "sid": "MAT.ALG.ECUACION_BASE.TERMINOS_ECUACION",
    "title": "Términos de una Ecuación",
    "obj": "Descomponer los miembros de una ecuación en sus componentes individuales (términos).",
    "intro": "Si el Miembro es el 'país' dentro de la ecuación, los 'Términos' son las ciudades individuales. Son las piezas de LEGO con las que está construida la igualdad.",
    "res": "Los términos son las partes individuales de una ecuación o expresión que están separadas entre sí por los signos de suma ($+$) o resta ($-$).",
    "expl": "Veamos la ecuación: $3x - 5 = x + 7$\n\nEsta ecuación tiene dos Miembros, pero ¿cuántos Términos tiene?\nCortamos la ecuación donde haya un $+$ o un $-$ que no esté dentro de un paréntesis.\n- En el primer miembro ($3x - 5$), hay dos términos: el $3x$ y el $-5$.\n- En el segundo miembro ($x + 7$), hay dos términos: la $x$ y el $+7$.\n\nEn total, esta ecuación tiene 4 términos. Cada término viaja con su signo a la izquierda. El signo es el 'apellido' del término; no se lo puedes quitar.\n\nTipos de términos:\n- **Término con incógnita:** Tiene letras (ej. $3x$).\n- **Término independiente:** Es un número puro sin letras (ej. $-5$ o $7$).",
    "proc": [
        "Paso 1: Observa toda la ecuación.",
        "Paso 2: Haz una marca imaginaria justo antes de cada signo $+$ o $-$.",
        "Paso 3: Cada bloque que queda es un término.",
        "Paso 4: Recuerda que el primer término de un miembro, si es positivo, tiene un $+$ invisible."
    ],
    "ex_a": [
        ("Ejemplo 1", "Analiza los términos de $-2x + 8 - y = 14$.", ["Cortes antes de +, -, =.", "Término 1: $-2x$", "Término 2: $+8$", "Término 3: $-y$", "Término 4 (en el otro miembro): $14$ (o $+14$).", "Total: 4 términos."])
    ],
    "ex_b": [
        ("¿Cuántos términos hay en la ecuación $5x = 20$?", "Dos", ["El '5x' es un solo término porque la multiplicación los une. El '20' es el otro."])
    ],
    "errs": [
        "Separar términos por multiplicaciones (ej. decir que $3x$ son dos términos, el 3 y la x. ¡Falso, la multiplicación los pega!).",
        "Olvidar incluir el signo negativo al identificar el término."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué símbolos matemáticos se encargan de separar los distintos términos dentro de una ecuación?", "choices": ["A) Los signos de multiplicación ($\\cdot$) y división ($\\div$).", "B) Únicamente el signo de igualdad ($=$).", "C) Los signos de suma ($+$) y resta ($-$).", "D) Los paréntesis y corchetes."], "ans": "C) Los signos de suma ($+$) y resta ($-$).", "sol": "Los sumandos y restandos conforman los términos algebraicos individuales."},
        {"group": "reconocimiento", "diff": "media", "prompt": "En la ecuación $4x - 7 = 3x + 2$, ¿cuáles son los 'términos independientes' (sin incógnita)?", "choices": ["A) $4x$ y $3x$", "B) $7$ y $2$", "C) $-7$ y $+2$", "D) $-7$ y $3x$"], "ans": "C) $-7$ y $+2$", "sol": "Son los números puros, y OJO: el signo que los precede les pertenece (-7, y +2)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "La expresión $5(x + 2)$ está compuesta inicialmente por un solo gran término factorizado.", "ans": "Verdadero", "sol": "El número 5 multiplica al bloque entero. Hasta que no rompas el paréntesis distribuyendo, se considera un solo gran término."}
    ]
})

# 6. CONCEPTO_SOLUCION
nodes.append({
    "sid": "MAT.ALG.ECUACION_BASE.CONCEPTO_SOLUCION",
    "title": "Concepto de Solución de una Ecuación",
    "obj": "Entender qué significa que un número sea la solución de una ecuación.",
    "intro": "El objetivo final de cualquier ecuación es 'resolverla'. Pero ¿qué es exactamente lo que estamos buscando? Buscamos el peso mágico que equilibra la balanza.",
    "res": "La solución (o raíz) de una ecuación es el valor específico que, al sustituirse en lugar de la incógnita, hace que la igualdad sea numéricamente verdadera.",
    "expl": "Resolver una ecuación es un trabajo detectivesco.\nSi te dan la ecuación $2x - 1 = 7$, te están diciendo: 'El doble de un número secreto, menos uno, es igual a siete. ¿Quién es el número?'.\n\nSi alguien te dice '¡Creo que la solución es 5!' ¿Cómo lo compruebas?\nReemplazas la 'x' por el 5:\nLado izquierdo: $2(5) - 1 = 10 - 1 = 9$.\nLado derecho: $7$.\n¿Es $9 = 7$? No. Entonces 5 **no es la solución**.\n\nSi alguien te dice '¡Es 4!':\nReemplazas: $2(4) - 1 = 8 - 1 = 7$.\nLado derecho: $7$.\n¿Es $7 = 7$? ¡Sí! Perfecto equilibrio.\nEntonces decimos que **$x = 4$ es la solución**.",
    "proc": [
        "Paso 1: Toma el valor candidato que crees que es la solución.",
        "Paso 2: Sustituye todas las apariciones de la incógnita en la ecuación por ese número (usa paréntesis).",
        "Paso 3: Calcula el valor numérico del Primer Miembro.",
        "Paso 4: Calcula el valor numérico del Segundo Miembro.",
        "Paso 5: Si ambos valores son idénticos, es la solución."
    ],
    "ex_a": [
        ("Ejemplo 1", "Comprueba si $x = 3$ es solución de $x^2 - 2 = 7$.", ["Reemplazamos $x$ por 3: $(3)^2 - 2 = 7$.", "Calculamos: $9 - 2 = 7$.", "$7 = 7$.", "Sí, es solución verdadera."])
    ],
    "ex_b": [
        ("¿Es $y = -2$ solución de $y + 5 = 3$?", "Sí", ["Reemplazamos: (-2) + 5 = 3. 3 = 3. Correcto."])
    ],
    "errs": [
        "Creer que la 'solución' son los pasos intermedios.",
        "Equivocarse en los signos al verificar la solución (ej. al reemplazar un número negativo)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "La forma definitiva y más confiable de saber si has encontrado la solución correcta de una ecuación es:", "choices": ["A) Preguntarle al profesor.", "B) Sustituir tu resultado en la ecuación original y verificar si ambos miembros dan el mismo número.", "C) Repasar los pasos de álgebra para ver si no hay errores.", "D) Usar otra letra diferente."], "ans": "B) Sustituir tu resultado en la ecuación original y verificar si ambos miembros dan el mismo número.", "sol": "La verificación empírica sustituyendo el valor es infalible y te asegura el puntaje."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál de los siguientes números es la solución de la ecuación $3x + 2 = 14$?", "choices": ["A) $2$", "B) $3$", "C) $4$", "D) $5$"], "ans": "C) $4$", "sol": "Si reemplazamos x=4, queda 3(4) + 2 = 12 + 2 = 14. ¡Coincide con el lado derecho!"},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "Si al reemplazar un valor candidato en la ecuación obtengo $0 = 0$, significa que el valor está equivocado.", "ans": "Falso", "sol": "El 0 es un número. Si llegas a 0=0, la balanza está equilibrada, y el valor que reemplazaste SÍ es la solución correcta."}
    ]
})

# 7. CONCEPTO_RAIZ
nodes.append({
    "sid": "MAT.ALG.ECUACION_BASE.CONCEPTO_RAIZ",
    "title": "La 'Raíz' de una Ecuación",
    "obj": "Conocer la terminología 'raíz' como sinónimo de solución y entender su uso, especialmente en grados superiores.",
    "intro": "En álgebra, las palabras importan. Si un ejercicio de examen te pide 'Encuentra las raíces de la ecuación', no te lances a calcular raíces cuadradas. Te están pidiendo otra cosa.",
    "res": "En el contexto de ecuaciones, la palabra 'raíz' es un sinónimo directo de 'solución'. Es el valor que satisface la ecuación.",
    "expl": "Históricamente, los matemáticos se referían al número de origen que generaba el equilibrio de la ecuación como la 'raíz' del problema (de ahí crecía el árbol de la ecuación).\n\n- Ecuación de primer grado (lineal): Ej. $2x - 6 = 0$. Tiene **una sola raíz** ($x=3$).\n- Ecuación de segundo grado (cuadrática): Ej. $x^2 - 9 = 0$. Puede tener **dos raíces** (soluciones). En este caso, $x=3$ y $x=-3$.\n- Ecuación de tercer grado (cúbica): Puede tener hasta **tres raíces**.\n\nPor lo tanto, la cantidad máxima de 'raíces' o soluciones que tiene un polinomio depende de su grado mayor (Teorema Fundamental del Álgebra). Cuando te pidan raíces, solo despeja la 'x'.",
    "proc": [
        "Paso 1: Cuando leas 'Encuentra la raíz', tradúcelo en tu mente a 'Encuentra la solución'.",
        "Paso 2: Resuelve la ecuación despejando la incógnita.",
        "Paso 3: El valor numérico final obtenido es la raíz."
    ],
    "ex_a": [
        ("Ejemplo 1", "Pregunta de examen: ¿Cuál es la raíz de $4x = 20$?", ["Traducimos: ¿Cuál es la solución de $4x = 20$?", "Despejamos: El 4 pasa dividiendo, $x = 20/4$.", "$x = 5$.", "La raíz es 5."])
    ],
    "ex_b": [
        ("¿Cuántas raíces máximo puede tener una ecuación de grado 1 (lineal)?", "Una", ["Las ecuaciones lineales (x elevada a 1) solo tienen una solución o raíz."])
    ],
    "errs": [
        "Extraer raíz cuadrada a los términos de la ecuación pensando que a eso se refiere la instrucción 'halla la raíz'."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "En la instrucción matemática 'Halle la raíz de la ecuación', el término 'raíz' hace referencia a:", "choices": ["A) El exponente de la incógnita.", "B) El valor numérico (solución) que hace verdadera la igualdad.", "C) La operación de raíz cuadrada.", "D) El coeficiente que acompaña a la 'x'."], "ans": "B) El valor numérico (solución) que hace verdadera la igualdad.", "sol": "Raíz y solución son sinónimos en este contexto."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Encuentra la raíz de la ecuación $x + 8 = 15$.", "choices": ["A) $7$", "B) $23$", "C) $\\sqrt{7}$", "D) $8$"], "ans": "A) $7$", "sol": "El número que sumado con 8 da 15 es 7. No hay que calcular raíces cuadradas."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "Toda ecuación polinómica tiene tantas raíces máximas posibles como el grado más alto de su incógnita.", "ans": "Verdadero", "sol": "Es el Teorema Fundamental del Álgebra. Grado 1 (lineal) tiene 1 raíz, grado 2 tiene 2 raíces, etc."}
    ]
})

# 8. CONJUNTO_SOLUCION
nodes.append({
    "sid": "MAT.ALG.ECUACION_BASE.CONJUNTO_SOLUCION",
    "title": "Conjunto Solución",
    "obj": "Escribir la respuesta de una ecuación en formato de teoría de conjuntos.",
    "intro": "Una vez que atrapas al culpable (la solución), debes encerrarlo en una celda. En matemáticas formales, esa celda se llama 'Conjunto Solución'.",
    "res": "El Conjunto Solución, denotado usualmente con una $S$, es el grupo de todos los valores que hacen verdadera la ecuación, encerrados entre llaves $\\{ \\}$.",
    "expl": "Aunque decir '$x = 5$' es correcto, la notación formal universitaria (y usada en pruebas estandarizadas como PAES) es colocar ese 5 en un conjunto.\n\n- Si la ecuación es lineal y su respuesta es 5, escribimos: $S = \\{5\\}$.\n- Si la ecuación es cuadrática y tiene dos respuestas, ej. 3 y -3, escribimos: $S = \\{-3, 3\\}$.\n- Si una ecuación absurda (ej. $x = x + 1$) resulta NO tener solución, decimos que su conjunto solución es el Conjunto Vacío. Se escribe $S = \\emptyset$ o $S = \\{\\}$.\n\nLas llaves $\\{ \\}$ indican que estamos enumerando elementos específicos, a diferencia de los corchetes $[ ]$ que indican un intervalo completo.",
    "proc": [
        "Paso 1: Resuelve la ecuación para obtener la(s) solución(es).",
        "Paso 2: Escribe la letra mayúscula $S$ y un signo igual.",
        "Paso 3: Abre llaves $\\{$.",
        "Paso 4: Escribe tus respuestas dentro, separadas por comas (si hay más de una).",
        "Paso 5: Cierra llaves $\\}$."
    ],
    "ex_a": [
        ("Ejemplo 1", "Expresa la solución de $2x - 4 = 0$ como conjunto solución.", ["Resolvemos: $2x = 4 \\rightarrow x = 2$.", "Formateamos como conjunto: $S = \\{2\\}$."])
    ],
    "ex_b": [
        ("Si una ecuación no tiene solución, ¿cómo se escribe su conjunto solución?", "$S = \\emptyset$", ["O también S = {}. Simboliza que el conjunto está vacío de respuestas."])
    ],
    "errs": [
        "Usar paréntesis redondos () o corchetes [] en lugar de llaves {}. En matemáticas esto significa 'intervalo' y es un grave error conceptual en ecuaciones.",
        "Escribir $\\{ \\emptyset \\}$ (esto es un conjunto que contiene al conjunto vacío, no está vacío)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿Qué indican las llaves $\\{ \\}$ al escribir un Conjunto Solución como $S = \\{4\\}$?", "choices": ["A) Que la solución está entre 0 y 4.", "B) Que 4 es un elemento discreto (aislado) que pertenece al grupo de soluciones correctas.", "C) Que es un intervalo abierto.", "D) Que el número 4 es negativo."], "ans": "B) Que 4 es un elemento discreto (aislado) que pertenece al grupo de soluciones correctas.", "sol": "Las llaves en teoría de conjuntos sirven para listar elementos discretos y exactos."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Si se determina que una ecuación de la forma $ax + b = cx + d$ genera una contradicción como $5 = 8$, ¿cuál es su conjunto solución?", "choices": ["A) $S = \\{0\\}$", "B) $S = \\emptyset$", "C) $S = \\mathbb{R}$", "D) $S = \\{5, 8\\}$"], "ans": "B) $S = \\emptyset$", "sol": "Una contradicción significa que no existe ningún número que satisfaga la ecuación. Por tanto, el conjunto de soluciones está vacío."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Escribir $S = [3]$ es exactamente lo mismo y es igual de válido que escribir $S = \\{3\\}$ para la respuesta de una ecuación lineal.", "ans": "Falso", "sol": "En matemáticas rigurosas, los corchetes [] indican un intervalo (desde un punto a otro). Para un número aislado DEBEN usarse las llaves {}."}
    ]
})

# 9. PROPIEDAD_ADITIVA
nodes.append({
    "sid": "MAT.ALG.ECUACION_BASE.PROPIEDAD_ADITIVA",
    "title": "La Regla de Oro: Propiedad Aditiva",
    "obj": "Comprender y aplicar la propiedad fundamental de añadir o restar la misma cantidad en ambos miembros de una ecuación.",
    "intro": "Llegamos a la magia negra que nos permite resolver problemas algebraicos. El 'despeje' no es un truco místico de 'pasar al otro lado cambiando de signo'. Es simplemente la aplicación de la regla de oro de la balanza.",
    "res": "Si sumas o restas exactamente la misma cantidad en el Primer Miembro y en el Segundo Miembro de una ecuación, la igualdad se mantiene (la balanza no pierde su equilibrio).",
    "expl": "Visualiza una balanza en equilibrio:\n$x - 3 = 5$\n\nQueremos descubrir el valor de la $x$. Nos estorba el $-3$. ¿Cómo lo eliminamos?\n¡Agregándole $+3$!\nPero, regla de oro: si pones $+3$ a la izquierda, debes poner $+3$ a la derecha para no romper la balanza.\n\nMatemáticamente:\n$x - 3 \\mathbf{+ 3} = 5 \\mathbf{+ 3}$\nEl $-3$ y el $+3$ se anulan (dan $0$).\n$x = 8$.\n\nEsto es lo que tu profesor te enseñó como 'pasar al otro lado cambiando el signo'. Es un atajo genial, pero la verdad absoluta debajo de ese atajo es la **Propiedad Aditiva de la Igualdad**.",
    "proc": [
        "Paso 1: Identifica qué término está sumando o restando a la incógnita y te estorba.",
        "Paso 2: Aplica la operación inversa (si hay un $+5$, debes restar $5$) en AMBOS miembros de la ecuación simultáneamente.",
        "Paso 3: Simplifica los cálculos de ambos lados. En un lado, el término estorboso desaparecerá."
    ],
    "ex_a": [
        ("Ejemplo 1", "Resuelve usando la propiedad aditiva: $y + 7 = 12$.", ["Estorba el +7. Debemos restar 7.", "Restamos 7 a ambos lados: $y + 7 - 7 = 12 - 7$.", "Simplificamos: $y + 0 = 5$.", "$y = 5$."])
    ],
    "ex_b": [
        ("Si tengo $x - 10 = 0$, ¿qué operación debo hacer en ambos lados para despejar x?", "Sumar 10", ["Para eliminar el -10, sumamos 10 a la izquierda y a la derecha."])
    ],
    "errs": [
        "Sumar una cantidad a un lado y restar esa misma cantidad al otro lado (rompe la balanza)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "El famoso atajo de 'pasar un término sumando al otro lado restando' es en realidad una aplicación rápida de:", "choices": ["A) La propiedad distributiva.", "B) La propiedad aditiva de la igualdad (restar lo mismo a ambos lados).", "C) La cancelación de inversos.", "D) La transposición mágica de Euler."], "ans": "B) La propiedad aditiva de la igualdad (restar lo mismo a ambos lados).", "sol": "El atajo oculta el hecho de que en realidad estás aplicando la misma operación a la balanza completa."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Si aplicas correctamente la propiedad aditiva para deshacerte del $-4$ en la ecuación $x - 4 = 15$, el paso matemático intermedio correcto se verá así:", "choices": ["A) $x - 4 + 4 = 15 - 4$", "B) $x = 15 + 4$", "C) $x - 4 + 4 = 15 + 4$", "D) $x - 4 - 4 = 15 - 4$"], "ans": "C) $x - 4 + 4 = 15 + 4$", "sol": "Se debe SUMAR 4 positivo a AMBOS miembros (izquierdo y derecho) simultáneamente."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Para mantener una ecuación balanceada, puedo sumar $2$ al lado izquierdo y sumar $3$ al lado derecho si son números pequeños.", "ans": "Falso", "sol": "La regla exige sumar o restar EXACTAMENTE la misma cantidad. Si no, destruyes el equilibrio de la ecuación."}
    ]
})

# 10. PROPIEDAD_MULTIPLICATIVA
nodes.append({
    "sid": "MAT.ALG.ECUACION_BASE.PROPIEDAD_MULTIPLICATIVA",
    "title": "La Regla de Plata: Propiedad Multiplicativa",
    "obj": "Entender y aplicar la regla de multiplicar o dividir ambos lados de una ecuación por la misma cantidad.",
    "intro": "Si podemos añadir pesas a la balanza, también podemos duplicar todo su peso o reducirlo a la mitad, siempre y cuando lo hagamos parejo. Esta es la segunda gran regla de las ecuaciones.",
    "res": "Si multiplicas o divides TODO el Primer Miembro y TODO el Segundo Miembro de una ecuación por la misma cantidad (distinta de cero), la igualdad se mantiene.",
    "expl": "Situación común: $3x = 12$.\nSignifica 'El triple de mi incógnita pesa 12'.\n¿Cómo descubro el peso de una sola $x$? Dividiendo ambas partes entre 3.\n$\\frac{3x}{3} = \\frac{12}{3}$\nLos tres de la izquierda se simplifican (dan $1x$, que es $x$).\n$x = 4$.\n\nEsto es lo que conoces como 'si está multiplicando, pasa dividiendo'.\n\n**OJO (Advertencia Letal):** Cuando divides o multiplicas, afecta a TODO EL MIEMBRO.\nSi la ecuación fuera $3x + 1 = 12$, y decides dividir por 3, debes dividir todo: $\\frac{3x + 1}{3} = \\frac{12}{3}$. ¡Por eso siempre se recomienda hacer sumas/restas PRIMERO, y dejar esta regla de multiplicar/dividir para el final, cuando la $x$ esté sola con su coeficiente!",
    "proc": [
        "Paso 1: Asegúrate de que el término que tiene la incógnita esté aislado (ya aplicaste sumas y restas).",
        "Paso 2: Identifica el coeficiente (el número que multiplica a la incógnita).",
        "Paso 3: Divide a ambos lados de la ecuación por ese mismo coeficiente.",
        "Paso 4: Simplifica las fracciones para obtener tu 'x' desnuda."
    ],
    "ex_a": [
        ("Ejemplo 1", "Despeja aplicando la propiedad: $5y = 35$.", ["El 5 está multiplicando a la 'y'.", "Dividimos ambos lados entre 5: $\\frac{5y}{5} = \\frac{35}{5}$.", "Simplificamos: $1y = 7$.", "Respuesta: $y = 7$."])
    ],
    "ex_b": [
        ("Si tengo $\\frac{x}{2} = 8$, ¿qué operación aplico?", "Multiplicar por 2 ambos lados.", ["Multiplicar por 2 elimina la división por 2 del lado izquierdo."])
    ],
    "errs": [
        "Dividir por 0 (matemáticamente imposible y explota el universo).",
        "En un lado dividir por 3 y en el otro por -3 (arruina el signo final)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "El atajo 'si está dividiendo, pasa multiplicando al otro lado' funciona gracias a la propiedad multiplicativa. ¿Qué hiciste realmente?", "choices": ["A) Moviste físicamente el número por arte de magia.", "B) Multiplicaste ambos miembros completos de la ecuación por ese mismo número.", "C) Sumaste ese número repetidas veces.", "D) Cambiaste el signo de la división."], "ans": "B) Multiplicaste ambos miembros completos de la ecuación por ese mismo número.", "sol": "Al multiplicar ambos lados, el número de la división en la izquierda se cancela, y aparece multiplicando en la derecha."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Para despejar la incógnita en la ecuación $-4x = 24$, ¿por qué número EXACTO debes dividir a ambos lados?", "choices": ["A) Por $4$", "B) Por $24$", "C) Por $-4$", "D) Por $-24$"], "ans": "C) Por $-4$", "sol": "Debes dividir exactamente por el coeficiente con su signo para que quede '1x' positivo. -4 / -4 = 1."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "Si en la ecuación $x + 2 = 10$ decido multiplicar todo por 2, la igualdad verdadera resultante sería $2x + 4 = 20$.", "ans": "Verdadero", "sol": "Sí. Al multiplicar TODOS los términos de AMBOS miembros por 2, la igualdad matemática se conserva intacta."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-ecuaciones-banco-gen-1.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

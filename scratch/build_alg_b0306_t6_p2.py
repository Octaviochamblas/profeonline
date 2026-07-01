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
    filename = "docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-6.jsonl"
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

# 5. METODO_RUFFINI
nodes.append({
    "sid": "MAT.ALG.TEOREMA_FACTOR.METODO_RUFFINI",
    "title": "Factorización mediante Ruffini",
    "obj": "Aprender a buscar raíces racionales y aplicar la regla de Ruffini en cadena para factorizar polinomios de grado mayor a 2.",
    "intro": "Factorizar un polinomio de grado 3 o 4 usando solo agrupación es como intentar desarmar un reloj con un martillo: a veces funciona, pero usualmente terminas frustrado. El método de Ruffini es tu destornillador de precisión. Te permite adivinar una pieza, sacarla limpiamente, y ver qué queda.",
    "res": "El Método de Ruffini para factorizar consiste en: 1) Adivinar una raíz '$c$' probando divisores del término independiente. 2) Aplicar división sintética con esa raíz para obtener un resto $0$. 3) Escribir el polinomio como $(x-c) \\cdot \\text{Cociente}$.",
    "expl": "Queremos factorizar $x^3 - 4x^2 + x + 6$.\n\n1. **Adivinar la raíz:** Probamos divisores del número final (6). Son: $\\pm1, \\pm2, \\pm3, \\pm6$.\n- Probemos $x = -1$. Evaluamos: $(-1)^3 - 4(-1)^2 + (-1) + 6 = -1 - 4 - 1 + 6 = 0$. ¡Es raíz!\n\n2. **Extraer el factor:** Sabemos que $(x - (-1)) = (x+1)$ es factor.\n\n3. **Aplicar Ruffini** para encontrar el otro paréntesis:\nMultiplicador: $-1$.\nCoeficientes: `1  -4   1   6`\nRuffini nos dará una fila final: `1  -5   6  | 0`.\n\n4. **Armar el rompecabezas:** El polinomio original ahora es $(x + 1)(x^2 - 5x + 6)$.\n\n5. **Seguir factorizando:** El trinomio $(x^2 - 5x + 6)$ lo podemos factorizar con el método simple de buscar dos números que multipliquen 6 y sumen -5. Son -2 y -3. Nos queda $(x-2)(x-3)$.\n\n**Factorización final:** $(x + 1)(x - 2)(x - 3)$. ¡Hemos destrozado un polinomio de tercer grado en sus tres piezas lineales fundamentales!",
    "proc": [
        "Paso 1: Lista los posibles divisores enteros del término independiente (el número solo).",
        "Paso 2: Evalúa el polinomio con esos números hasta encontrar uno que dé como resultado 0 (esa es tu raíz).",
        "Paso 3: Realiza la división sintética (Ruffini) usando esa raíz como multiplicador.",
        "Paso 4: Comprueba que el resto sea 0. Si no es 0, te equivocaste en la suma o no era raíz.",
        "Paso 5: Escribe la respuesta parcial como $(x - \\text{raíz}) \\cdot (\\text{polinomio cociente})$.",
        "Paso 6: Repite el proceso con el polinomio cociente si su grado es mayor a 2, o aplica métodos clásicos si es cuadrático."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $x^3 - 7x + 6$. (Ojo: falta $x^2$).", ["Divisores de 6: $\\pm1, \\pm2, \\pm3, \\pm6$. Probamos 1: $1^3 - 7(1) + 6 = 0$. Raíz: 1.", "Ruffini con raíz 1. Coeficientes: `1, 0, -7, 6`.", "Fila final: `1  1  -6 | 0`. Cociente: $x^2 + x - 6$.", "Factorizamos el trinomio: $(x+3)(x-2)$.", "Resultado: $(x-1)(x+3)(x-2)$."])
    ],
    "ex_b": [
        ("Si al hacer Ruffini en un grado 4 te da resto 0, ¿qué grado tiene el cociente?", "Grado 3", ["Al extraer un factor lineal de un grado 4, el polinomio se reduce a un grado 3, al cual le puedes volver a aplicar Ruffini."])
    ],
    "errs": [
        "Adivinar un número que no es divisor del término independiente (ej. intentar probar el 5 si el término independiente es 6, lo cual es pérdida de tiempo en raíces enteras).",
        "Olvidar poner el factor lineal extraído en la respuesta final y entregar solo la factorización del cociente."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "media", "prompt": "¿De dónde provienen las \"candidatas\" a raíces enteras que debemos probar al usar Ruffini?", "choices": ["A) De los múltiplos del coeficiente principal.", "B) Son los divisores exactos del término independiente.", "C) Siempre probamos solo 1 y -1.", "D) De los números primos."], "ans": "B) Son los divisores exactos del término independiente.", "sol": "Según el Teorema de las Raíces Racionales, cualquier raíz entera forzosamente debe dividir al término constante (independiente)."},
        {"group": "conceptuales", "diff": "alta", "prompt": "Si encuentras que $x=2$ es raíz y aplicas Ruffini, y el cociente resultante vuelve a ser divisible por $x=2$ (es decir, al aplicar Ruffini de nuevo a la nueva fila vuelve a dar resto 0). ¿Qué significa esto?", "choices": ["A) Que cometiste un error en la suma.", "B) Que la raíz $x=2$ tiene \"multiplicidad 2\" o superior (es una raíz repetida).", "C) Que el polinomio es infinito.", "D) Que debes cambiar el signo."], "ans": "B) Que la raíz $x=2$ tiene \"multiplicidad 2\" o superior (es una raíz repetida).", "sol": "Las raíces pueden repetirse. Significa que el factor (x-2) está elevado al cuadrado o más (ej: (x-2)^2)."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Para factorizar $x^3 - x^2 - 14x + 24$, la lista de posibles raíces a probar incluye:", "choices": ["A) $\\pm1, \\pm2, \\pm3, \\pm4, \\pm6, \\pm8, \\pm12, \\pm24$", "B) $\\pm1, \\pm14$", "C) Solo números positivos.", "D) 0, 1, 2, 3, 4"], "ans": "A) $\\pm1, \\pm2, \\pm3, \\pm4, \\pm6, \\pm8, \\pm12, \\pm24$", "sol": "Son todos los divisores enteros del número 24."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Es posible que un polinomio no tenga ninguna raíz entera y no pueda ser factorizado por Ruffini de forma sencilla?", "ans": "Verdadero", "sol": "Si las raíces son irracionales (como $\\sqrt{2}$) o complejas, probar divisores enteros será inútil."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si al hacer Ruffini el resto NO es 0, significa que el número que probaste no era una raíz?", "ans": "Verdadero", "sol": "El resto es igual al valor de evaluación. Si no es 0, no es raíz."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿Se puede usar Ruffini sucesivamente en forma de 'cascada' (aplicarlo sobre los cocientes obtenidos repetidamente) para factorizar un grado 5?", "ans": "Verdadero", "sol": "Es la técnica estándar. Sacas un grado y bajas a 4. Sacas otro y bajas a 3. Sucesivamente hasta llegar a un grado 2 (trinomio)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Un alumno factoriza $x^3 - 3x^2 - x + 3$. Sus pasos son: prueba el 1, da resto 0. Su fila de cociente da $x^2 - 2x - 3$. Factoriza eso en $(x-3)(x+1)$. Escribe como respuesta final $(x-3)(x+1)$. ¿Qué error fatal cometió?", "choices": ["A) Factorizó mal el trinomio.", "B) Olvidó agregar el factor inicial $(x-1)$ que usó para el primer Ruffini.", "C) Ruffini no se puede aplicar a polinomios con signos mixtos.", "D) Debió probar el 3 primero."], "ans": "B) Olvidó agregar el factor inicial $(x-1)$ que usó para el primer Ruffini.", "sol": "Un polinomio de grado 3 factorizado en binomios lineales debe tener 3 paréntesis: (x-1)(x-3)(x+1). Le faltó el primero que extrajo."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Para el volumen de una piscina $V(x) = x^3 + 4x^2 + x - 6$, sabes que la profundidad es $(x-1)$. ¿Cuáles son las expresiones para el ancho y el largo?", "choices": ["A) $(x+3)$ y $(x+2)$", "B) $(x-3)$ y $(x-2)$", "C) $(x+6)$ y $(x-1)$", "D) No se puede saber."], "ans": "A) $(x+3)$ y $(x+2)$", "sol": "Si (x-1) es factor, la raíz es 1. Ruffini con 1 da cociente x^2+5x+6. Esto se factoriza como (x+3)(x+2). Esas son las otras dos dimensiones."}
    ]
})

# 6. FACTORIZACION_POR_RAICES
nodes.append({
    "sid": "MAT.ALG.TEOREMA_FACTOR.FACTORIZACION_POR_RAICES",
    "title": "Factorización Completa por Raíces",
    "obj": "Consolidar el uso de raíces dadas o calculadas para construir la expresión factorizada total de un polinomio, incluyendo coeficientes líderes.",
    "intro": "A veces el problema te da la solución en bandeja: \"Construye un polinomio sabiendo que sus raíces son estas\". Esta es la ingeniería inversa definitiva del Teorema del Factor. Pasarás de tener puntos dispersos en un plano a construir la ecuación maestra que los rige.",
    "res": "Si un polinomio tiene raíces $r_1, r_2, \\dots, r_n$, su factorización completa se expresa como $P(x) = a(x - r_1)(x - r_2)\\dots(x - r_n)$, donde '$a$' es un coeficiente líder (constante de ajuste de escala).",
    "expl": "Imagínate que alguien te dice: \"Tengo un polinomio de tercer grado. Sus raíces son $5$, $-2$ y $0$.\n¿Puedes reconstruirlo?\n\n¡Por supuesto!\n- Si la raíz es $5$, su factor es $(x - 5)$.\n- Si la raíz es $-2$, su factor es $(x - (-2)) = (x + 2)$.\n- Si la raíz es $0$, su factor es $(x - 0) = x$.\n\nMultiplicamos las piezas maestras:\n$P(x) = x \\cdot (x - 5) \\cdot (x + 2)$.\n\nSi te pidieran la forma expandida, simplemente multiplicas todo:\n$x \\cdot (x^2 - 3x - 10) = x^3 - 3x^2 - 10x$.\n\nLa única trampa es el \"coeficiente $a$\". Si el problema te dice que el polinomio cruza el eje Y en 20, tendrás que añadir una letra '$a$' multiplicando al frente: $P(x) = a(x)(x-5)(x+2)$ y resolver para '$a$' evaluando en un punto dado.",
    "proc": [
        "Paso 1: Transforma cada raíz $r$ dada en un factor $(x - r)$.",
        "Paso 2: Multiplica todos los factores entre sí.",
        "Paso 3: Si te dan el coeficiente líder de $x^n$, colócalo multiplicando al frente de todo.",
        "Paso 4: Si te piden la forma general, aplica distributiva múltiple para expandir los paréntesis."
    ],
    "ex_a": [
        ("Ejemplo 1", "Construye un polinomio factorizado con raíces $1, 2$ y $3$.", ["Factores: $(x-1)$, $(x-2)$, $(x-3)$.", "Ensamblaje: $P(x) = (x-1)(x-2)(x-3)$."])
    ],
    "ex_b": [
        ("Crea un polinomio cuadrático con raíz doble en -4.", "$P(x) = (x+4)^2$", ["Una raíz doble significa que el factor aparece dos veces. El factor es (x - (-4)) = (x+4). Al repetirlo, es (x+4)^2."])
    ],
    "errs": [
        "Olvidar cambiar el signo al meter la raíz en el paréntesis. (Ej: con raíz $3$, poner $(x+3)$ en lugar de $(x-3)$).",
        "Si te dan una raíz fraccionaria como $1/2$, escribir $(x - 1/2)$ está bien, pero es más elegante (y algebraicamente preferido) escribirlo como $(2x - 1)$ para evitar fracciones."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "Si las raíces de un polinomio de grado 2 son $6$ y $-1$, ¿cuál es su forma factorizada más simple?", "choices": ["A) $(x+6)(x-1)$", "B) $(x-6)(x+1)$", "C) $(x-6)(x-1)$", "D) $(x+6)(x+1)$"], "ans": "B) $(x-6)(x+1)$", "sol": "Se invierten los signos: (x - 6) y (x - (-1))."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si el problema indica que el coeficiente de la variable de mayor grado (coeficiente principal o líder) es 3, ¿dónde se ubica en la factorización?", "choices": ["A) Se suma al final.", "B) Se multiplica al principio de todos los factores: $3(x-a)(x-b)$.", "C) Se eleva al cuadrado.", "D) Se ignora, no afecta las raíces."], "ans": "B) Se multiplica al principio de todos los factores: $3(x-a)(x-b)$.", "sol": "El coeficiente líder ajusta la \"altura\" de la curva, y multiplica a toda la expresión."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Qué polinomio tiene como únicas raíces a $0$ y $5$?", "choices": ["A) $x^2 + 5x$", "B) $x^2 - 5x$", "C) $x^2 - 25$", "D) $5x^2$"], "ans": "B) $x^2 - 5x$", "sol": "Factores: (x-0) y (x-5). Multiplicados: x(x-5) = x^2 - 5x."},
        {"group": "reconocimiento", "diff": "alta", "prompt": "Construye un polinomio cúbico con raíces $1, -1$ y $2$, y luego expándelo.", "choices": ["A) $x^3 - 2x^2 - x + 2$", "B) $x^3 + 2x^2 - x - 2$", "C) $x^3 - 2x^2 + x - 2$", "D) $x^3 - x^2 - 2x + 1$"], "ans": "A) $x^3 - 2x^2 - x + 2$", "sol": "Factores: (x-1)(x+1)(x-2). Primero multiplicamos (x-1)(x+1) = x^2-1. Luego (x^2-1)(x-2) = x^3 - 2x^2 - x + 2."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si una raíz es la fracción $3/4$, el factor correspondiente puede escribirse sin fracciones como $(4x-3)$?", "ans": "Verdadero", "sol": "Sí. Despejando $x = 3/4 \\rightarrow 4x = 3 \\rightarrow 4x - 3 = 0$. Es el mismo factor escalado por 4."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Un polinomio con raíces 2, 4 y 6 será forzosamente de grado 3 (como mínimo)?", "ans": "Verdadero", "sol": "Cada raíz distinta requiere un factor lineal 'x'. Multiplicar tres 'x' genera un $x^3$."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿Si me dicen que el polinomio tiene raíz doble en 3, la factorización es $(x-3)(x-3)$ o $(x-3)^2$?", "ans": "Verdadero", "sol": "Una raíz con \"multiplicidad\" (repetida) significa que el paréntesis se eleva a esa potencia."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Un modelo de rentabilidad corta el eje del tiempo (X) en los años 2 y 5. Sabiendo que es una función cuadrática y que el año 3 generó 4 millones en pérdidas (es decir $P(3) = -4$), encuentra la expresión exacta del modelo factorizado.", "choices": ["A) $P(t) = 2(t-2)(t-5)$", "B) $P(t) = (t-2)(t-5)$", "C) $P(t) = -2(t-2)(t-5)$", "D) $P(t) = 4(t-2)(t-5)$"], "ans": "A) $P(t) = 2(t-2)(t-5)$", "sol": "El esqueleto es P(t) = a(t-2)(t-5). Evaluamos t=3: a(3-2)(3-5) = -4 -> a(1)(-2) = -4 -> -2a = -4 -> a=2. Respuesta es 2(t-2)(t-5)."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "En una prueba te entregan el gráfico de un polinomio que cruza el eje X exactamente en los valores -3, 0 y 4. Te preguntan por un posible divisor exacto de este polinomio. ¿Cuál sirve?", "choices": ["A) $x^2 + 3x$", "B) $x^2 - 4x$", "C) $x^2 - x - 12$", "D) Todas las anteriores son posibles divisores (factores cuadráticos armados con las raíces)."], "ans": "D) Todas las anteriores son posibles divisores (factores cuadráticos armados con las raíces).", "sol": "Las raíces son (x+3), x y (x-4). Si multiplicas x(x+3) da x^2+3x. Si multiplicas x(x-4) da x^2-4x. Si multiplicas (x+3)(x-4) da x^2-x-12. Todos son divisores correctos."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-6.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

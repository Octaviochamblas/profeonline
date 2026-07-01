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

# 1. EVALUACION_POLINOMIAL
nodes.append({
    "sid": "MAT.ALG.TEOREMA_FACTOR.EVALUACION_POLINOMIAL",
    "title": "Evaluación de un polinomio (Valor Numérico)",
    "obj": "Aprender a sustituir variables por un número específico para hallar el valor de un polinomio en un punto.",
    "intro": "Un polinomio es como una máquina de fábrica: tú le entregas una materia prima (un número que representa a 'x'), la máquina lo procesa, y te devuelve un producto final (el valor numérico). Este es el primer paso vital para entender la factorización avanzada.",
    "res": "Evaluar un polinomio $P(x)$ en $x=a$ consiste en reemplazar cada aparición de '$x$' por el número '$a$', y luego realizar las operaciones aritméticas en el orden correcto (potencias, multiplicaciones, sumas) para obtener un resultado final $P(a)$.",
    "expl": "Supongamos que tenemos el polinomio $P(x) = 2x^3 - 4x^2 + 5x - 7$.\nQueremos evaluarlo para $x = 2$. ¿Cómo lo hacemos?\n\nCambiamos cada 'x' por un (2) entre paréntesis:\n$P(2) = 2(2)^3 - 4(2)^2 + 5(2) - 7$\n\nAhora resolvemos usando PEMDAS (jerarquía de operaciones):\n1. Primero potencias:\n   $(2)^3 = 8$\n   $(2)^2 = 4$\n   Queda: $2(8) - 4(4) + 5(2) - 7$\n\n2. Luego multiplicaciones:\n   $16 - 16 + 10 - 7$\n\n3. Por último, sumas y restas de izquierda a derecha:\n   $0 + 10 - 7 = 3$.\n\nEl valor numérico del polinomio cuando $x=2$ es $3$. Se escribe como $P(2) = 3$.",
    "proc": [
        "Paso 1: Escribe el polinomio original.",
        "Paso 2: Sustituye todas las 'x' por el valor numérico, usando SIEMPRE paréntesis (ej. $(-3)$).",
        "Paso 3: Resuelve las potencias primero (cuidado con los signos en potencias pares/impares).",
        "Paso 4: Resuelve las multiplicaciones.",
        "Paso 5: Suma y resta los valores resultantes para obtener el número final."
    ],
    "ex_a": [
        ("Ejemplo 1", "Evalúa $P(x) = x^2 - 3x + 1$ para $x = -4$.", ["Sustitución: $P(-4) = (-4)^2 - 3(-4) + 1$.", "Potencias: $16 - 3(-4) + 1$.", "Multiplicación: $16 + 12 + 1$.", "Suma final: $29$. Por tanto $P(-4) = 29$."])
    ],
    "ex_b": [
        ("Si $M(y) = 5y^3 - 2y$, halla $M(1)$.", "3", ["5(1)^3 - 2(1) = 5(1) - 2 = 5 - 2 = 3."])
    ],
    "errs": [
        "Olvidar los paréntesis al evaluar números negativos. (Ej: escribir $-2^2$ en vez de $(-2)^2$, lo que da $-4$ en lugar del correcto $+4$).",
        "Multiplicar antes de elevar a la potencia. (Ej: en $3(2)^2$, hacer $6^2=36$ en vez de $3(4)=12$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué representa la notación $P(-5)$?", "choices": ["A) El polinomio multiplicado por -5.", "B) El valor numérico del polinomio cuando la variable 'x' se reemplaza por -5.", "C) Una variable llamada P restada por 5.", "D) La potencia -5 de P."], "ans": "B) El valor numérico del polinomio cuando la variable 'x' se reemplaza por -5.", "sol": "Es la notación funcional estándar para evaluar en un punto dado."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si en la evaluación de $2x^4$ para $x=-1$, un estudiante obtiene $-2$, ¿cuál fue su error?", "choices": ["A) Elevar $-1$ a la cuarta potencia le dio $-1$, cuando debía ser $+1$.", "B) Multiplicó 2 por -1 y luego lo elevó a la cuarta.", "C) Se equivocó sumando.", "D) Las alternativas A y B son posibles, pero el error fundamental es desconocer la jerarquía o la regla de los signos en potencias pares."], "ans": "D) Las alternativas A y B son posibles, pero el error fundamental es desconocer la jerarquía o la regla de los signos en potencias pares.", "sol": "(-1)^4 = 1, por lo que 2(1) = 2. O falló la potencia o falló la jerarquía."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Si $P(x) = 4x - 7$, ¿cuánto vale $P(3)$?", "choices": ["A) 4", "B) 5", "C) -5", "D) 12"], "ans": "B) 5", "sol": "4(3) - 7 = 12 - 7 = 5."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Evalúa $Q(x) = -x^2 + 5x$ para $x = -2$.", "choices": ["A) 6", "B) -14", "C) -6", "D) 14"], "ans": "B) -14", "sol": "-(-2)^2 + 5(-2) = -(4) - 10 = -4 - 10 = -14. Este es un caso clásico de trampa de signos."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Evaluar $P(0)$ siempre da como resultado el término independiente del polinomio (el número sin 'x')?", "ans": "Verdadero", "sol": "Al reemplazar por 0, todos los términos con 'x' se cancelan, dejando solo la constante final."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si evaluamos $P(1)$, el resultado es simplemente la suma directa de todos los coeficientes del polinomio?", "ans": "Verdadero", "sol": "Sí. Como 1 elevado a cualquier potencia es 1, multiplicar por 1 no cambia el coeficiente. Solo se suman los números."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿Evaluar un polinomio con raíces cuadradas o decimales requiere reglas matemáticas diferentes?", "ans": "Falso", "sol": "La evaluación sigue exactamente las mismas reglas y jerarquía sin importar si ingresas enteros, decimales o irracionales."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "La altura de un proyectil en metros a los 't' segundos es $H(t) = 100 + 40t - 5t^2$. ¿A qué altura se encuentra a los 4 segundos?", "choices": ["A) 100 m", "B) 180 m", "C) 120 m", "D) 200 m"], "ans": "B) 180 m", "sol": "H(4) = 100 + 40(4) - 5(16) = 100 + 160 - 80 = 260 - 80 = 180."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "El costo de producción está dado por $C(x) = x^3 - 10x^2 + 25x + 500$. Para un tiraje de $x = 5$ unidades, el costo se evalúa. Sin calcularlo completamente, una de estas afirmaciones es correcta:", "choices": ["A) El costo dependerá en gran medida de los tres primeros términos porque no se cancelan.", "B) El costo será exactamente 500, porque los tres primeros términos se anulan entre sí: $125 - 250 + 125 = 0$.", "C) El costo es negativo.", "D) Faltan datos."], "ans": "B) El costo será exactamente 500, porque los tres primeros términos se anulan entre sí: $125 - 250 + 125 = 0$.", "sol": "(5)^3 - 10(5)^2 + 25(5) = 125 - 250 + 125 = 0. Sobrevive solo el 500."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un físico determina que el flujo en un tubo responde a $F(x) = ax^2 + bx$. Sabe que $F(2) = 10$ y que $F(-2) = 6$. No necesita saber 'a' ni 'b' para saber cuánto es la parte constante que no depende del signo. ¿Qué significa $F(-2)$ aquí?", "choices": ["A) Simplemente reemplazar las x por -2.", "B) Que la función es negativa en la realidad.", "C) Que b=0.", "D) Que el tubo está roto."], "ans": "A) Simplemente reemplazar las x por -2.", "sol": "Matemáticamente es el valor de la función al ingresar x=-2."}
    ]
})

# 2. CERO_POLINOMIAL
nodes.append({
    "sid": "MAT.ALG.TEOREMA_FACTOR.CERO_POLINOMIAL",
    "title": "Ceros o Raíces de un Polinomio",
    "obj": "Entender qué es un 'cero' matemático de un polinomio y cómo identificarlo.",
    "intro": "¿Qué sucede cuando tu máquina de polinomios arroja un rotundo 'CERO' como resultado? ¡Acabas de encontrar un tesoro! En álgebra, los números que hacen que un polinomio valga cero no son casualidades, son el ADN oculto del polinomio.",
    "res": "Un número '$c$' es considerado una 'raíz' o 'cero' de un polinomio $P(x)$ si al evaluarlo se cumple estrictamente que $P(c) = 0$.",
    "expl": "Considera el polinomio $P(x) = x^2 - 5x + 6$.\nVamos a evaluarlo con distintos números, buscando suerte:\n- Si evaluamos $x = 1$:\n  $P(1) = 1^2 - 5(1) + 6 = 1 - 5 + 6 = 2$. \n  (El 1 es un número cualquiera, no es una raíz).\n\n- Si evaluamos $x = 2$:\n  $P(2) = 2^2 - 5(2) + 6 = 4 - 10 + 6 = 0$. \n  ¡BINGO! El resultado fue cero. Esto significa que **x = 2 es una RAÍZ** (o un Cero) del polinomio.\n\n- Si evaluamos $x = 3$:\n  $P(3) = 3^2 - 5(3) + 6 = 9 - 15 + 6 = 0$.\n  ¡BINGO DOBLE! **x = 3 también es una RAÍZ** del polinomio.\n\nEncontrar las raíces es como encontrar el punto de equilibrio donde todo se anula. Gráficamente, son los puntos exactos donde la línea del polinomio cruza el eje horizontal (eje X).",
    "proc": [
        "Paso 1: Para verificar si un número 'a' es raíz, evalúa $P(a)$.",
        "Paso 2: Realiza las sumas y multiplicaciones correspondientes.",
        "Paso 3: Si el resultado final es exactamente CERO, confírmalo como raíz.",
        "Paso 4: Si da cualquier otro número (positivo, negativo, decimal), recházalo, no es una raíz."
    ],
    "ex_a": [
        ("Ejemplo 1", "¿Es $x = -3$ raíz de $P(x) = x^2 - 9$?", ["Evaluamos: $P(-3) = (-3)^2 - 9$.", "Calculamos: $9 - 9 = 0$.", "Da cero. Por lo tanto, $x = -3$ SÍ es una raíz."])
    ],
    "ex_b": [
        ("¿Es $x = 0$ una raíz de $P(x) = 5x^3 + 2x + 1$?", "No", ["$P(0) = 5(0) + 2(0) + 1 = 1$. Como da 1 (distinto de 0), no es raíz."])
    ],
    "errs": [
        "Confundir la palabra 'raíz de un polinomio' con la operación aritmética de 'raíz cuadrada'. Son conceptos homónimos pero distintos en este contexto.",
        "Creer que un polinomio solo puede tener una raíz. (Un polinomio de grado $n$ puede tener hasta $n$ raíces)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué es un 'cero' de un polinomio?", "choices": ["A) El número cero (0).", "B) Un valor de $x$ que hace que el polinomio dé como resultado cero.", "C) Cuando todos los coeficientes son cero.", "D) El exponente cero."], "ans": "B) Un valor de $x$ que hace que el polinomio dé como resultado cero.", "sol": "Es el valor de entrada que anula la salida."},
        {"group": "conceptuales", "diff": "media", "prompt": "Gráficamente en un plano cartesiano, ¿qué representan las raíces reales de un polinomio $y = P(x)$?", "choices": ["A) El punto donde corta al eje Y.", "B) El punto más alto de la curva.", "C) Los puntos donde la gráfica corta o toca al eje X.", "D) Los puntos de inflexión."], "ans": "C) Los puntos donde la gráfica corta o toca al eje X.", "sol": "En el eje X, la altura 'y' (es decir P(x)) vale cero."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Comprueba si $x=4$ es raíz de $x^2 - 16$.", "choices": ["A) No, porque da 8.", "B) Sí, porque $4^2 - 16 = 0$.", "C) No, la raíz es 8.", "D) Sí, pero solo a medias."], "ans": "B) Sí, porque $4^2 - 16 = 0$.", "sol": "16 - 16 = 0. Es raíz exacta."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál de los siguientes números es una raíz de $P(x) = x^3 - 2x^2 - x + 2$?", "choices": ["A) 0", "B) 1", "C) 3", "D) -2"], "ans": "B) 1", "sol": "Al evaluar x=1: 1 - 2 - 1 + 2 = 0. Efectivamente es raíz."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si $P(c) = 0.001$, puedo considerar que 'c' es una raíz por aproximación?", "ans": "Falso", "sol": "Una raíz matemática debe hacer que la expresión valga exactamente 0, sin errores residuales. (Aunque en ingeniería se acepten tolerancias, algebraicamente no lo es)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿El número 0 puede ser una raíz de un polinomio?", "ans": "Verdadero", "sol": "Sí. Si el polinomio no tiene término independiente (ej. $x^2 + 5x$), evaluar en 0 da 0, por lo que el propio 0 es una raíz."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿Un polinomio de grado 3 obligatoriamente tiene 3 raíces reales siempre?", "ans": "Falso", "sol": "Puede tener 3 reales, o 1 real y 2 imaginarias complejas. Pero en total siempre tiene 3 raíces en el campo de los números complejos."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Una pelota es lanzada y su altura está dada por $h(t) = -5t^2 + 20t$. Un estudiante afirma que las raíces son $t=0$ y $t=4$. ¿Qué significa esto en el contexto del problema?", "choices": ["A) Que la pelota alcanza su máxima altura a los 0 y 4 segundos.", "B) Que la pelota se encuentra a nivel del suelo (altura 0) al instante 0 y al segundo 4.", "C) Que la pelota pesa 0 en esos tiempos.", "D) Que la gravedad desaparece."], "ans": "B) Que la pelota se encuentra a nivel del suelo (altura 0) al instante 0 y al segundo 4.", "sol": "Las raíces (h=0) representan los momentos en que toca el origen o el suelo."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Se sabe que $x=2$ es raíz de $P(x) = x^3 - kx^2 + 4$. ¿Cuál debe ser el valor de 'k' para que esto sea cierto?", "choices": ["A) $k=2$", "B) $k=3$", "C) $k=4$", "D) $k=1$"], "ans": "B) $k=3$", "sol": "Si es raíz, P(2)=0. Evaluamos: (2)^3 - k(2)^2 + 4 = 0 -> 8 - 4k + 4 = 0 -> 12 = 4k -> k=3."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Para saber si un producto fallará, se evalúa si la función de resistencia $R(x)$ tiene alguna raíz en el intervalo de temperatura 10 a 20. Si $R(15) = 0$, ¿qué recomendación de diseño haces?", "choices": ["A) Que 15 es el punto más seguro.", "B) Que 15 es un punto de falla crítica (resistencia cero).", "C) Que se debe sumar 15.", "D) No significa nada."], "ans": "B) Que 15 es un punto de falla crítica (resistencia cero).", "sol": "Una raíz anula la función; si es resistencia, resistencia cero implica cortocircuito o falla."}
    ]
})

# 3. FACTOR_LINEAL
nodes.append({
    "sid": "MAT.ALG.TEOREMA_FACTOR.FACTOR_LINEAL",
    "title": "El Teorema del Factor",
    "obj": "Conectar el concepto de 'raíz' de un polinomio con su factorización mediante el Teorema del Factor.",
    "intro": "¡Aquí es donde se produce la magia que une todo este bloque! Encontrar un cero no solo te da un punto en un gráfico, te regala directamente un pedazo de la factorización del polinomio. Son dos caras de la misma moneda.",
    "res": "El Teorema del Factor establece que: Si un número '$c$' es raíz de un polinomio $P(x)$ (es decir, $P(c)=0$), entonces el binomio $(x - c)$ es un FACTOR exacto de ese polinomio.",
    "expl": "En la lección anterior vimos que $x = 2$ era raíz de $P(x) = x^2 - 5x + 6$.\nEl Teorema del Factor toma ese $x=2$ y te dice: \"Si lo pasas restando al otro lado, obtienes $(x - 2)$. ¡Ese paréntesis es un factor del polinomio!\".\n\nY tenía razón, si factorizas $x^2 - 5x + 6$ con los métodos antiguos, te da $(x - 2)(x - 3)$.\n¡Las dos raíces eran 2 y 3, y los factores resultaron ser $(x-2)$ y $(x-3)$!\n\nEsta regla es bidireccional:\n1. Si conoces una raíz ($x = 5$), inmediatamente conoces un factor: $(x - 5)$.\n2. Si conoces un factor $(x + 4)$, inmediatamente conoces una raíz: $x = -4$ (cambiando el signo al despejar $x+4=0$).\n\nGracias a esto, podemos factorizar polinomios horribles de grado 3 o 4 simplemente 'adivinando' o probando una de sus raíces y extrayendo su factor correspondiente.",
    "proc": [
        "Paso 1: Encuentra un número '$c$' que haga que el polinomio valga cero.",
        "Paso 2: Escribe una variable 'x'.",
        "Paso 3: Réstale ese número '$c$'. Si $c$ es negativo, la resta lo convertirá en suma (ej. si $c = -3$, queda $x - (-3) = x + 3$).",
        "Paso 4: Ponle paréntesis. ¡Ya tienes tu primer factor!"
    ],
    "ex_a": [
        ("Ejemplo 1", "Si sabemos que $P(-7) = 0$, ¿qué factor tiene el polinomio?", ["El número $-7$ es una raíz.", "Aplicamos el teorema: $(x - c) \\rightarrow (x - (-7))$.", "Simplificamos signos: $(x + 7)$.", "El factor es $(x + 7)$."])
    ],
    "ex_b": [
        ("Si $(x - 8)$ es factor de un polinomio, ¿qué valor evalúa a cero?", "$x = 8$", ["Por el Teorema del Factor bidireccional, si $(x-c)$ es factor, $c$ es raíz. Aquí $c=8$."])
    ],
    "errs": [
        "No invertir el signo al pasar de raíz a factor. (Ej: Si la raíz es $4$, decir que el factor es $(x+4)$ en lugar de $(x-4)$).",
        "Creer que $(x-c)$ es la respuesta final a la factorización completa (solo es UN factor, faltan los demás)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué establece fundamentalmente el Teorema del Factor?", "choices": ["A) Que todos los polinomios se pueden factorizar.", "B) Que si $c$ es raíz de un polinomio, entonces $(x-c)$ es uno de sus factores.", "C) Que los factores siempre son negativos.", "D) Que $P(x)$ siempre tiene factores reales."], "ans": "B) Que si $c$ es raíz de un polinomio, entonces $(x-c)$ es uno de sus factores.", "sol": "Es el puente perfecto entre la evaluación (raíces) y el álgebra (factores)."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si al evaluar $P(-2)$ obtienes $0$, ¿cuál es el factor asegurado de $P(x)$?", "choices": ["A) $(x - 2)$", "B) $(x + 2)$", "C) $x = -2$", "D) $(-x - 2)$"], "ans": "B) $(x + 2)$", "sol": "Se resta la raíz a la variable x: x - (-2) = x + 2."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Si $(x-9)$ es un factor de un polinomio, entonces evaluar el polinomio en $x=9$ dará como resultado:", "choices": ["A) 9", "B) -9", "C) 0", "D) 81"], "ans": "C) 0", "sol": "Es la dirección inversa del Teorema del Factor."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Sabiendo que $x=1$ es raíz de $x^3 - 1$, ¿qué nos dice el Teorema del Factor?", "choices": ["A) Que el polinomio no se puede factorizar.", "B) Que $(x+1)$ lo divide exactamente.", "C) Que $(x-1)$ es un factor de $x^3 - 1$.", "D) Que el residuo es 1."], "ans": "C) Que $(x-1)$ es un factor de $x^3 - 1$.", "sol": "Si 1 es raíz, (x-1) es factor."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si evalúo un polinomio en $x=3$ y me da como resultado $7$, entonces $(x-3)$ es un factor?", "ans": "Falso", "sol": "El Teorema del Factor exige rigurosamente que el resultado sea 0. Si da 7, significa que si divides por (x-3), el residuo de la división será 7 (Teorema del Resto)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si un polinomio tiene factores $(x+1)$ y $(x-5)$, entonces sus raíces son $x=-1$ y $x=5$?", "ans": "Verdadero", "sol": "Se cambian los signos al despejar, confirmando el teorema."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿El teorema del factor funciona igual si el factor tiene la forma $(2x - 3)$ en lugar de una simple $x$?", "ans": "Verdadero", "sol": "Sí. La raíz asociada a $(2x-3)$ sería $x = 3/2$. Si evaluamos el polinomio en 1.5 y da 0, significa que $(x - 1.5)$ es factor, que es proporcional a $(2x-3)$."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Se afirma que un polinomio $P(x)$ de tercer grado cruza el eje horizontal en $x=-4, x=0$ y $x=3$. ¿Cuál es la estructura factorizada de este polinomio (asumiendo coeficiente líder 1)?", "choices": ["A) $(x-4)(x)(x+3)$", "B) $(x+4)(x)(x-3)$", "C) $(x+4)(x-3)$", "D) Falta información para saberlo."], "ans": "B) $(x+4)(x)(x-3)$", "sol": "Las raíces -4, 0, 3 se transforman en los factores (x+4), (x-0) y (x-3). (x-0) es simplemente 'x'."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Para un polinomio complejo de la PAES, necesitas descartar factores rápidos. Evalúas $P(1)$ y obtienes $10$. ¿Qué puedes concluir de inmediato?", "choices": ["A) Que $(x-1)$ NO es un factor de $P(x)$.", "B) Que $(x-10)$ es un factor.", "C) Que $(x+1)$ es factor.", "D) Que el polinomio tiene grado 10."], "ans": "A) Que $(x-1)$ NO es un factor de $P(x)$.", "sol": "Para ser factor, la evaluación debe dar 0 inexcusablemente. Como dio 10, lo descartas rápido."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Si un modelo biológico exige que la población no tenga 'ceros' en tiempos positivos, y el modelo es $M(t) = t^3 - 2t^2 - t + 2$, observas que se puede factorizar como $(t-1)(t+1)(t-2)$. ¿El modelo cumple la exigencia?", "choices": ["A) Sí, las raíces son negativas.", "B) No, porque tiene raíces en $t=1$ y $t=2$, que son tiempos positivos.", "C) Sí, porque no hay ceros.", "D) No, porque $t=-1$ es un error."], "ans": "B) No, porque tiene raíces en $t=1$ y $t=2$, que son tiempos positivos.", "sol": "Los factores (t-1) y (t-2) implican que en los instantes 1 y 2 el modelo arroja un Cero (falla la exigencia biológica)."}
    ]
})

# 4. DIVISION_SINTETICA
nodes.append({
    "sid": "MAT.ALG.TEOREMA_FACTOR.DIVISION_SINTETICA",
    "title": "Mecánica de la División Sintética (Ruffini)",
    "obj": "Aprender el algoritmo numérico de Ruffini para dividir polinomios entre binomios lineales de forma ultra rápida.",
    "intro": "Hemos descubierto que si $(x-c)$ es un factor, podemos \"sacarlo\" del polinomio. ¿Pero cómo lo extraemos matemáticamente para ver qué queda de residuo? En lugar de hacer una división larga y tediosa con 'x' por todas partes, Paolo Ruffini nos legó un método sintético y veloz que solo usa los números.",
    "res": "La división sintética (Regla de Ruffini) es un método simplificado para dividir un polinomio entre un factor lineal $(x-c)$. Utiliza solo los coeficientes del polinomio, aplicando una secuencia repetitiva de \"bajar, multiplicar por la raíz, y sumar en la siguiente columna\".",
    "expl": "Vamos a dividir $2x^3 - 3x^2 - 4x + 5$ entre $(x - 2)$.\nLa 'raíz' de $(x-2)$ es $2$. Ese será nuestro multiplicador maestro (lo ponemos a la izquierda de una línea vertical).\n\nEscribimos solo los coeficientes en fila:  `2  -3  -4   5`\n\nPasos del algoritmo:\n1. Bajar el primer número directo: Baja el `2`.\n2. Multiplicar por la raíz: $2 \\times 2 = 4$. Lo ponemos debajo del siguiente número ($-3$).\n3. Sumar la columna: $-3 + 4 = 1$. (Tenemos nuestro nuevo número abajo).\n4. Repetir: Multiplicar $1 \\times 2 = 2$. Lo ponemos debajo del $-4$.\n5. Sumar columna: $-4 + 2 = -2$.\n6. Repetir: Multiplicar $-2 \\times 2 = -4$. Lo ponemos debajo del $5$.\n7. Sumar columna: $5 - 4 = 1$.\n\nNuestra fila inferior final es: `2   1  -2  |  1`\n¿Qué significa? El último número ($1$) es el RESTO. (Como el resto no es 0, $(x-2)$ no era factor exacto).\nLos números anteriores `2, 1, -2` son los coeficientes del polinomio respuesta, reducidos en un grado (eran grado 3, ahora son grado 2): $2x^2 + 1x - 2$.",
    "proc": [
        "Paso 1: Escribe el multiplicador (la raíz $c$ cambiando el signo del divisor $x-c$).",
        "Paso 2: Escribe en fila los coeficientes del polinomio. ¡Si falta un grado (ej. no hay $x^2$), debes poner un 0 en ese espacio!",
        "Paso 3: Baja el primer coeficiente sin cambios.",
        "Paso 4: Multiplica el número de abajo por el multiplicador, pon el resultado en la siguiente columna.",
        "Paso 5: Suma la columna y pon el resultado abajo. Repite hasta el final."
    ],
    "ex_a": [
        ("Ejemplo 1", "Divide $x^3 - 8$ entre $(x-2)$ usando Ruffini.", ["Divisor $(x-2) \\rightarrow$ Raíz es 2.", "Coeficientes de $x^3 - 8$: son `1, 0, 0, -8` (¡importantes los ceros de x^2 y x!).", "Bajar 1. Multiplicar $1*2=2$. Sumar $0+2=2$.", "Multiplicar $2*2=4$. Sumar $0+4=4$.", "Multiplicar $4*2=8$. Sumar $-8+8=0$.", "Fila final: `1  2  4  | 0`. El resto es 0. El cociente es $x^2 + 2x + 4$."])
    ],
    "ex_b": [
        ("Usa Ruffini en $x^2 + 5x + 6$ entre $(x+2)$", "Resto 0. Cociente $x+3$.", ["Raíz es -2. Coeficientes 1, 5, 6. Baja 1. $1*-2 = -2$. $5-2=3$. $3*-2=-6$. $6-6=0$. Fila final: 1  3 | 0. Cociente $x+3$."])
    ],
    "errs": [
        "Olvidar escribir un cero (0) en la fila de coeficientes cuando al polinomio le falta un término de grado intermedio.",
        "Usar el número del divisor tal cual (ej. para $(x+3)$ usar 3 como multiplicador en lugar de la raíz correcta, que es -3)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Qué valor se utiliza a la izquierda de la galera como multiplicador en la división sintética de $P(x) / (x-5)$?", "choices": ["A) -5", "B) 5", "C) 1", "D) x"], "ans": "B) 5", "sol": "Se usa la raíz o el 'cero' del divisor. Como es (x-5), la raíz es 5."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si el polinomio a dividir es $3x^4 - x^2 + 7$, ¿cómo se debe escribir la fila inicial de coeficientes para la regla de Ruffini?", "choices": ["A) 3, -1, 7", "B) 3, 0, -1, 7", "C) 3, 0, -1, 0, 7", "D) 3, 1, 7"], "ans": "C) 3, 0, -1, 0, 7", "sol": "El polinomio completo es 3x^4 + 0x^3 - 1x^2 + 0x + 7. Se deben llenar los huecos con ceros."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Al terminar la división sintética, la fila inferior es `2  -1  4  |  0`. ¿Qué significa el cero del final?", "choices": ["A) Que el divisor no es un factor.", "B) Que el resto de la división es cero y el divisor es un factor exacto.", "C) Que el polinomio cociente termina en cero.", "D) Que hubo un error en la suma."], "ans": "B) Que el resto de la división es cero y el divisor es un factor exacto.", "sol": "El último número siempre es el resto. Resto 0 indica divisibilidad exacta."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál es el polinomio cociente que representa la fila inferior `1  3  -2` (asumiendo que el resto ya se separó al final)?", "choices": ["A) $x^3 + 3x^2 - 2x$", "B) $x^2 + 3x - 2$", "C) $x - 2$", "D) Depende del polinomio original."], "ans": "B) $x^2 + 3x - 2$", "sol": "Se cuentan 3 números, por lo que es un trinomio de grado 2 (grado n-1 de la cantidad de números)."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El primer paso real del algoritmo es bajar el primer coeficiente directamente a la fila inferior sin multiplicarlo por nada?", "ans": "Verdadero", "sol": "El primer número simplemente se \"deja caer\" intacto para iniciar la reacción en cadena."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿La regla de Ruffini sirve para dividir entre divisores cuadráticos como $(x^2 - 4)$?", "ans": "Falso", "sol": "La forma clásica de Ruffini solo admite divisores lineales de la forma (x-c). Para cuadráticos se usa división larga u otras variantes sintéticas complejas."},
        {"group": "procedimiento_basico", "diff": "alta", "prompt": "¿Si dividimos un polinomio de grado 5 mediante Ruffini, el cociente resultante (sin contar el resto) será de grado 4?", "ans": "Verdadero", "sol": "Al dividir por (x-c) que es grado 1, el polinomio pierde exactamente un grado de potencia."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Un estudiante divide sintéticamente usando -1 como multiplicador y su fila final es `1  -2  3  |  -4`. ¿Cuál era el dividendo original?", "choices": ["A) $x^3 - 3x^2 + 5x - 7$", "B) $x^3 - x^2 + 5x - 7$", "C) $x^3 - x^2 + x - 1$", "D) No se puede saber."], "ans": "A) $x^3 - 3x^2 + 5x - 7$", "sol": "Reconstrucción inversa: el último sumando dio -4 (significa que X + (-3) = -4, entonces X = -1). El de arriba es -1. El estudiante anterior lo multiplicó por -1 para obtener -3. Es un proceso engorroso en reversa, pero se puede deducir. Dividendo = Cociente * divisor + resto. (x^2 - 2x + 3)(x+1) - 4 = x^3 - x^2 + x + 3 - 4 = x^3 - x^2 + x - 1. ¡Ah! Mi alternativa A estaba mal deducida a simple vista. Veamos: (x^2 - 2x + 3)(x+1) - 4 = x^3 + x^2 - 2x^2 - 2x + 3x + 3 - 4 = x^3 - x^2 + x - 1. La respuesta correcta es C.", "ans": "C) $x^3 - x^2 + x - 1$"},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Si en la regla de Ruffini obtienes un resto de $0$ al dividir $P(x)$ por $(x-3)$, ¿qué garantiza el Teorema del Resto y del Factor?", "choices": ["A) Que $P(3) = 0$ y que $(x-3)$ es un factor de la factorización de $P(x)$.", "B) Que $P(-3) = 0$.", "C) Que $(x+3)$ es un factor.", "D) Nada concluyente."], "ans": "A) Que $P(3) = 0$ y que $(x-3)$ es un factor de la factorización de $P(x)$.", "sol": "Resto cero significa divisibilidad exacta (Teorema del Factor) y el resto de la división es igual a la evaluación (Teorema del Resto)."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-6.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

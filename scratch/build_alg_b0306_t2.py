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
    filename = "docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-2.jsonl"
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

# 1. AGRUPACION_TERMINOS
nodes.append({
    "sid": "MAT.ALG.FACTOR_AGRUPACION.AGRUPACION_TERMINOS",
    "title": "Agrupación estratégica de términos",
    "obj": "Aprender a dividir un polinomio extenso en grupos más pequeños para facilitar la extracción de factores comunes parciales.",
    "intro": "¿Alguna vez has intentado mover un mueble demasiado grande por una puerta pequeña? A veces la solución es desarmarlo en dos partes y pasarlas por separado. En álgebra, cuando un polinomio es muy largo y no tiene un factor común general, lo dividimos en \"equipos\".",
    "res": "La agrupación de términos consiste en asociar los términos de un polinomio en grupos (normalmente pares) que compartan un factor común parcial, como paso preparatorio para una factorización mayor.",
    "expl": "A veces, al enfrentarnos a un polinomio como $ax + bx + ay + by$, nos damos cuenta de que no existe ninguna letra o número que esté presente en los CUATRO términos a la vez.\n\nSin embargo, si miramos más de cerca, podemos dividirlo en dos grupos estratégicos:\n- Grupo 1: $(ax + bx)$ -> Aquí ambos comparten la 'x'.\n- Grupo 2: $(ay + by)$ -> Aquí ambos comparten la 'y'.\n\nAl agruparlos utilizando paréntesis, estamos preparando el terreno. Lo escribimos así: $(ax + bx) + (ay + by)$. \n\nEs fundamental agrupar con un signo '$+$' entre los paréntesis para no alterar los signos originales. Si necesitas agrupar términos negativos, deja el signo menos dentro del paréntesis: $(... - ...) + (-... + ...)$.",
    "proc": [
        "Paso 1: Verifica que el polinomio no tenga un factor común global.",
        "Paso 2: Cuenta la cantidad de términos. (Generalmente debe ser un número par como 4 o 6).",
        "Paso 3: Agrupa los términos en pares (o tríos) asegurándote de que cada grupo comparta algo en común.",
        "Paso 4: Escríbelos encerrados en paréntesis, unidos siempre por un signo de suma (+)."
    ],
    "ex_a": [
        ("Ejemplo 1", "Agrupa los términos del polinomio $2x^2 - 4x + xy - 2y$ en dos pares.", ["El primer y segundo término comparten números pares y la 'x'.", "El tercer y cuarto término comparten la 'y'.", "Agrupamos: $(2x^2 - 4x) + (xy - 2y)$."])
    ],
    "ex_b": [
        ("¿Cómo agruparías $ab + ac - b - c$ asegurando no alterar signos?", "$(ab + ac) + (-b - c)$", ["Al usar un + en medio, el - de la 'b' se mantiene intacto dentro del segundo paréntesis."])
    ],
    "errs": [
        "Poner un signo negativo entre los grupos sin cambiar los signos del segundo paréntesis. Ej: $(ax) - (by+...)$ incorrectamente.",
        "Agrupar términos que no tienen absolutamente nada en común."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Cuál es el propósito principal de agrupar términos en un polinomio largo?", "choices": ["A) Sumar los términos semejantes.", "B) Facilitar la extracción de factores comunes parciales.", "C) Eliminar variables.", "D) Convertir el polinomio en un monomio."], "ans": "B) Facilitar la extracción de factores comunes parciales.", "sol": "Agrupar nos permite extraer un factor en un grupo, y otro factor en otro grupo."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si tenemos un polinomio de 4 términos sin factor común global, ¿de qué tamaño deben ser los grupos?", "choices": ["A) Un grupo de 3 y uno de 1.", "B) Dos grupos de 2 términos.", "C) Cuatro grupos de 1 término.", "D) Es imposible factorizar."], "ans": "B) Dos grupos de 2 términos.", "sol": "La agrupación más estándar y equilibrada para 4 términos es en dos pares."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Cuál es la forma correcta de agrupar $am - bm + an - bn$ sin alterar su valor?", "choices": ["A) $(am - bm) + (an - bn)$", "B) $(am) - (bm + an - bn)$", "C) $(am + an) - (bm - bn)$", "D) $(am - bn) * (an - bm)$"], "ans": "A) $(am - bm) + (an - bn)$", "sol": "Usar un + entre los paréntesis garantiza que ningún signo original se modifique."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Dada la expresión $3x^3 - x^2 - 6x + 2$, ¿qué agrupación tiene sentido para buscar factores parciales?", "choices": ["A) $(3x^3 - x^2) + (-6x + 2)$", "B) $(3x^3 + 2) + (-x^2 - 6x)$", "C) $(3x^3) + (-x^2 - 6x + 2)$", "D) $(3x^3 - 6x - x^2) + 2$"], "ans": "A) $(3x^3 - x^2) + (-6x + 2)$", "sol": "El primer grupo comparte x^2. El segundo comparte el número 2."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Agrupar términos cambia el valor matemático del polinomio original?", "ans": "Falso", "sol": "Solo reorganiza la estructura. Por propiedad asociativa, el valor se mantiene."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si pongo un signo menos entre dos grupos, debo invertir los signos de los términos del segundo grupo?", "ans": "Verdadero", "sol": "Sí, porque el menos exterior se distribuiría y afectaría los signos internos. Por eso es más seguro usar un '+'."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Todo polinomio de 4 términos puede ser agrupado para encontrar una factorización perfecta final?", "ans": "Falso", "sol": "No todos los polinomios son factorizables por agrupación; los coeficientes deben ser proporcionales."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Una viga de acero tiene una distribución de tensión descrita por $15T^2 - 10T + 3T - 2$. Un arquitecto quiere agrupar los términos para simplificarla. ¿Cuál es la agrupación más útil?", "choices": ["A) $(15T^2 - 10T) + (3T - 2)$", "B) $(15T^2 - 2) + (-10T + 3T)$", "C) $(15T^2 + 3T) - (10T - 2)$", "D) Las agrupaciones A y C son igualmente útiles."], "ans": "D) Las agrupaciones A y C son igualmente útiles.", "sol": "Ambas formas permiten sacar factores comunes en cada grupo (en A, sacas 5T y 1; en C, sacas 3T y -2)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Al agrupar la fórmula de decaimiento $P = a^2b - a^2c - ab + ac$, un estudiante escribe $(a^2b - ab) - (a^2c + ac)$. ¿Qué error cometió?", "choices": ["A) Agrupó mal las letras.", "B) El signo '+ac' se transformó en negativo al expandir el menos exterior.", "C) No sacó el factor común de inmediato.", "D) El polinomio original tenía '+ac', y al agrupar con un '-' afuera, el estudiante escribió '+ac' adentro, lo que daría '-ac' al expandirse."], "ans": "D) El polinomio original tenía '+ac', y al agrupar con un '-' afuera, el estudiante escribió '+ac' adentro, lo que daría '-ac' al expandirse.", "sol": "El estudiante olvidó que al poner un '-' afuera, los signos internos deben invertirse (-a^2c - ac) para que vuelva a dar el original."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "En la expresión $x^3 + 2x^2 + 5x + 10$, al realizar la agrupación $(x^3 + 2x^2) + (5x + 10)$, ¿qué se busca lograr en el siguiente paso lógico?", "choices": ["A) Sumar los cuatro términos.", "B) Extraer el factor común $x^2$ en el primer grupo y el factor $5$ en el segundo.", "C) Extraer un $x^3$ de toda la expresión.", "D) Cancelar los términos independientes."], "ans": "B) Extraer el factor común $x^2$ en el primer grupo y el factor $5$ en el segundo.", "sol": "Esa es la razón exacta por la cual los agrupamos así."}
    ]
})

# 2. FACTOR_COMUN_POR_GRUPO
nodes.append({
    "sid": "MAT.ALG.FACTOR_AGRUPACION.FACTOR_COMUN_POR_GRUPO",
    "title": "Extracción del factor común por grupo",
    "obj": "Aplicar la regla del factor común monomio de forma independiente a cada uno de los grupos formados previamente.",
    "intro": "Una vez que tenemos a nuestro polinomio gigante dividido en dos equipos, es hora de poner a dieta a cada equipo por separado. Le quitaremos a cada grupo lo que le sobra, aplicando la técnica de factor común monomio que ya conocemos.",
    "res": "Consiste en factorizar cada uno de los paréntesis agrupados extrayendo su respectivo factor común monomio. El objetivo crítico de este paso es lograr que los polinomios resultantes dentro de los nuevos paréntesis sean **idénticos**.",
    "expl": "Continuando con nuestro polinomio agrupado: $(ax + bx) + (ay + by)$.\n\nTrabajamos en el primer grupo: $(ax + bx)$. Ambos términos tienen la letra 'x'. Si factorizamos extrayendo la 'x', nos queda $x(a + b)$.\n\nTrabajamos en el segundo grupo: $(ay + by)$. Ambos tienen la letra 'y'. Extraemos la 'y' y nos queda $y(a + b)$.\n\nJuntando los dos resultados en nuestra expresión general, tenemos ahora: \n$x(a + b) + y(a + b)$.\n\n¡Fíjate en la magia que acaba de ocurrir! Al factorizar cada grupo por separado, hemos creado artificialmente un nuevo bloque repetido: el paréntesis $(a + b)$. Si los paréntesis no hubiesen quedado iguales, significaría que la agrupación fue incorrecta o que debimos extraer un signo negativo.",
    "proc": [
        "Paso 1: Toma el primer grupo y extrae su mayor factor común monomio.",
        "Paso 2: Toma el segundo grupo y haz lo mismo.",
        "Paso 3: Si los interiores de los paréntesis quedaron con los signos al revés (ej. $(x-y)$ y $(y-x)$), extrae un -1 en el segundo grupo para igualarlos.",
        "Paso 4: Escribe la nueva expresión mostrando los monomios multiplicando a sus respectivos paréntesis."
    ],
    "ex_a": [
        ("Ejemplo 1", "Extrae los factores por grupo en $(2x^2 + 4x) + (3xy + 6y)$.", ["Primer grupo: Factor común es 2x. Queda $2x(x + 2)$.", "Segundo grupo: Factor común es 3y. Queda $3y(x + 2)$.", "Expresión resultante: $2x(x + 2) + 3y(x + 2)$."])
    ],
    "ex_b": [
        ("¿Qué obtienes al extraer factores en $(m^3 - m^2) + (-2m + 2)$?", "$m^2(m - 1) - 2(m - 1)$", ["En el segundo grupo sacamos el factor negativo (-2) para que el interior cambie a (m-1) y sea idéntico al primero."])
    ],
    "errs": [
        "Olvidar escribir el signo '+' (o '-') entre los dos grupos una vez extraídos los factores.",
        "Extraer factores pero dejar paréntesis que no son idénticos, y tratar de continuar con el siguiente paso.",
        "Extraer un número positivo cuando se necesitaba uno negativo para igualar signos internos."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Cuál es el objetivo principal al extraer factores de cada grupo?", "choices": ["A) Eliminar todos los paréntesis.", "B) Que los paréntesis resultantes queden idénticos.", "C) Que los factores externos sean iguales.", "D) Reducir la expresión a cero."], "ans": "B) Que los paréntesis resultantes queden idénticos.", "sol": "Crear un paréntesis idéntico en ambos lados es vital para el paso final."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si en un grupo obtienes $(a-b)$ y en el otro $(b-a)$, ¿qué debes hacer?", "choices": ["A) Sumarlos.", "B) Extraer un factor -1 de uno de los grupos.", "C) Cancelarlos.", "D) Asumir que el ejercicio no tiene solución."], "ans": "B) Extraer un factor -1 de uno de los grupos.", "sol": "El -1 invertirá los signos de (b-a) convirtiéndolo en -(a-b)."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Cuál es la expresión correcta tras factorizar por grupos el polinomio $(x^3 + 2x^2) + (5x + 10)$?", "choices": ["A) $x^2(x + 2) + 5(x + 2)$", "B) $x^2(x + 2) + 5(x + 10)$", "C) $x(x^2 + 2x) + 5(x + 2)$", "D) $x^2(x+2) * 5(x+2)$"], "ans": "A) $x^2(x + 2) + 5(x + 2)$", "sol": "En el primero sale x^2, en el segundo sale 5."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Al procesar $(6ab - 4b) + (15a - 10)$, extraemos factores. ¿Qué obtenemos?", "choices": ["A) $2b(3a - 2) + 5(3a - 2)$", "B) $2b(3a - 4) + 5(3a - 10)$", "C) $2a(3b - 2) + 5(3a - 2)$", "D) $b(6a - 4) + 5(3a - 2)$"], "ans": "A) $2b(3a - 2) + 5(3a - 2)$", "sol": "2b es el factor común del 1ero. 5 es del 2do."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Si los paréntesis no quedan iguales, puedo forzarlos a ser iguales copiando el primero?", "ans": "Falso", "sol": "La matemática debe cuadrar. Si no quedan iguales de forma lícita, hay que revisar la agrupación."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Es posible que un grupo ya esté factorizado o no tenga factor común y simplemente se le asigne un '1' afuera?", "ans": "Verdadero", "sol": "Sí. Por ejemplo, en x^2(x+1) + (x+1), el segundo grupo se factoriza como 1(x+1)."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿El signo que une a las dos partes extraídas siempre será un más (+)?", "ans": "Falso", "sol": "Si en el segundo grupo extrajiste un factor negativo, el conector será un menos (-)."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "En el desarrollo de un puente, la curva de carga se agrupa como $(10k^3 - 15k^2) - (4k - 6)$. Un técnico extrae factores. ¿Cuál es la forma correcta?", "choices": ["A) $5k^2(2k - 3) - 2(2k - 3)$", "B) $5k^2(2k - 3) + 2(2k - 3)$", "C) $5k^2(2k - 3) - 2(2k + 3)$", "D) $5k^2(2k - 3) - 1(4k - 6)$"], "ans": "A) $5k^2(2k - 3) - 2(2k - 3)$", "sol": "Extraemos 5k^2 en el 1ero. En el 2do, sacamos 2 (respetando el menos que ya estaba afuera) y queda (2k-3)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Para factorizar $mx - nx - m + n$, Javiera agrupa $(mx - nx) + (-m + n)$. Extrae 'x' del primero, dando $x(m - n)$. ¿Qué debe extraer del segundo grupo para que el interior quede idéntico?", "choices": ["A) $1$", "B) $-1$", "C) $n$", "D) $0$"], "ans": "B) $-1$", "sol": "Extraer -1 de (-m+n) invierte los signos, dando -1(m-n), igualando así los paréntesis."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un error común al extraer factores es 'soltar' un término. Si un estudiante tiene $(x^3 + x^2)$ y extrae $x^2$, anota $x^2(x)$. ¿Qué debió anotar?", "choices": ["A) $x^2(x + x)$", "B) $x^2(x + 1)$", "C) $x^3(1 + x)$", "D) $x^2(x - 1)$"], "ans": "B) $x^2(x + 1)$", "sol": "El x^2 dividido por x^2 es 1. Olvidar este '1' es fatal para la factorización final."}
    ]
})

# 3. FACTOR_COMUN_RESULTANTE
nodes.append({
    "sid": "MAT.ALG.FACTOR_AGRUPACION.FACTOR_COMUN_RESULTANTE",
    "title": "Extracción del factor común polinomial resultante",
    "obj": "Concluir el método de agrupación extrayendo el bloque polinomial que se ha revelado como común en toda la expresión.",
    "intro": "¡Es el gran final del truco de magia! Lo que empezó como un polinomio desordenado, se agrupó, se limpió, y ahora nos muestra un patrón idéntico en ambos bandos. Ahora solo falta recoger el premio.",
    "res": "El paso final de la factorización por agrupación es identificar el factor polinomio (el paréntesis) que se repite y extraerlo como un factor común global, creando un producto de dos polinomios.",
    "expl": "Nuestra expresión procesada en el paso anterior era: $x(a + b) + y(a + b)$.\n\nSi observas, esto no es más que una \"Extracción de factor común polinomio\", un concepto que vimos en el bloque de Factor Común. El bloque $(a+b)$ se comporta como si fuera una sola letra gigante que se repite en ambos lados.\n\nProcedemos a extraerlo escribiéndolo una sola vez: $(a + b)$.\nLuego, abrimos un segundo paréntesis donde introducimos todo lo que estaba multiplicando por fuera a esos bloques: la '$x$' y el '$+y$'.\n\nEl resultado definitivo y completamente factorizado es: $(a + b)(x + y)$.\n¡Hemos convertido una suma de 4 términos en una simple multiplicación de 2 binomios!",
    "proc": [
        "Paso 1: Confirma visualmente que los paréntesis de tu expresión son matemáticamente idénticos.",
        "Paso 2: Escribe ese paréntesis común una sola vez al inicio de tu respuesta.",
        "Paso 3: Abre un nuevo par de paréntesis justo al lado (para indicar multiplicación).",
        "Paso 4: Ingresa los factores externos (coeficientes o monomios) en este nuevo paréntesis, conservando sus signos."
    ],
    "ex_a": [
        ("Ejemplo 1", "Completa la factorización para $3x(m-n) - 5y(m-n)$.", ["El factor polinomio repetido es $(m-n)$.", "Los factores exteriores son $3x$ y $-5y$.", "Juntamos: $(m-n)(3x - 5y)$."])
    ],
    "ex_b": [
        ("¿Cuál es el final de $x^2(a+1) + (a+1)$?", "$(a+1)(x^2 + 1)$", ["El segundo $(a+1)$ tiene un 1 imaginario multiplicando afuera. Lo recolectamos como $+1$."])
    ],
    "errs": [
        "Sumar los factores internos del paréntesis. (Ej: pensar que el resultado es $(2a+2b)$ en lugar de sacarlo como factor).",
        "Olvidar colocar el '1' cuando un paréntesis no tiene un número afuera visible.",
        "Dejar un signo '+' entre los dos paréntesis finales, arruinando la factorización (Ej: $(a+b) + (x+y)$)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Cuál es la forma final de un polinomio factorizado por agrupación?", "choices": ["A) Un polinomio muy largo.", "B) Una suma de dos paréntesis.", "C) Una multiplicación de factores (generalmente dos binomios).", "D) Un monomio simple."], "ans": "C) Una multiplicación de factores (generalmente dos binomios).", "sol": "Toda factorización exitosa termina siendo una cadena de multiplicaciones."},
        {"group": "conceptuales", "diff": "media", "prompt": "En la expresión $A(x) + B(x)$, donde $(x)$ es el paréntesis común, ¿cuál es el resultado de extraer $(x)$?", "choices": ["A) $x(A + B)$", "B) $A(x)B(x)$", "C) $x^2(A + B)$", "D) $AB(x)$"], "ans": "A) $x(A + B)$", "sol": "El factor común (x) se extrae y multiplica a la suma de los exteriores (A+B)."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "Si llegaste al paso $5m(x-3) + 2n(x-3)$, ¿cuál es el resultado final?", "choices": ["A) $(x-3)(5m * 2n)$", "B) $(x-3)(5m + 2n)$", "C) $(5m - 3)(2n - 3)$", "D) $(x-3) + (5m + 2n)$"], "ans": "B) $(x-3)(5m + 2n)$", "sol": "Recogemos los externos (5m y +2n) en un segundo paréntesis multiplicador."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Qué resulta de finalizar la factorización en $y^2(x+y) - (x+y)$?", "choices": ["A) $(x+y)(y^2 - 1)$", "B) $(x+y)(y^2 - 0)$", "C) $(x+y)(y^2)$", "D) $y^2(x+y)^2$"], "ans": "A) $(x+y)(y^2 - 1)$", "sol": "El segundo paréntesis tiene un coeficiente implícito de -1."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Los factores resultantes $(A)(B)$ pueden cambiar su orden a $(B)(A)$ sin afectar la respuesta?", "ans": "Verdadero", "sol": "Sí, el orden de los factores no altera el producto (conmutatividad de la multiplicación)."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si los paréntesis en el penúltimo paso no son idénticos, puedo de todas formas juntarlos sumando sus partes?", "ans": "Falso", "sol": "Si no son idénticos, no puedes aplicar la extracción de factor común. El método falló o hubo un error."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Es posible que después de sacar el binomio resultante, alguno de los factores aún se pueda seguir factorizando?", "ans": "Verdadero", "sol": "Sí. A veces el paréntesis de los externos queda como una diferencia de cuadrados, por ejemplo."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un programa computacional simplifica una ecuación de renderizado a $T^2(R-5) + 4(R-5) = 0$. ¿Qué factorización final debe aplicar el software para hallar las raíces?", "choices": ["A) $(R-5)(T^2 + 4) = 0$", "B) $(R-5)(T^2 - 4) = 0$", "C) $(R-5) + (T^2 + 4) = 0$", "D) $(R-5)T^2 + 4 = 0$"], "ans": "A) $(R-5)(T^2 + 4) = 0$", "sol": "Extrae el bloque común (R-5) y junta los factores externos en (T^2 + 4)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "El volumen de una bóveda se factoriza agrupando. El penúltimo paso es $x^2(x-3) - 9(x-3)$. Un estudiante da como respuesta final $(x-3)(x^2-9)$. Su profesor le dice que la tarea está incompleta. ¿Por qué?", "choices": ["A) Porque debió multiplicarlo de vuelta para comprobar.", "B) Porque el factor $(x^2-9)$ aún puede ser factorizado como $(x-3)(x+3)$.", "C) Porque olvidó un signo negativo.", "D) El profesor se equivocó, la factorización está completa."], "ans": "B) Porque el factor $(x^2-9)$ aún puede ser factorizado como $(x-3)(x+3)$.", "sol": "La factorización no está completa hasta que todos los factores sean irreducibles (factores primos)."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Dada la expresión $a(c-d) - c + d$, al agrupar los dos últimos términos y finalizar, ¿qué factorización resulta?", "choices": ["A) $(c-d)(a+1)$", "B) $(c-d)(a-1)$", "C) $(c+d)(a-1)$", "D) $(c-d)(a-c+d)$"], "ans": "B) $(c-d)(a-1)$", "sol": "Agrupamos -c+d como -(c-d). Nos queda a(c-d) - 1(c-d), que finalmente es (c-d)(a-1)."}
    ]
})

# 4. REAGRUPACION_ALTERNATIVA
nodes.append({
    "sid": "MAT.ALG.FACTOR_AGRUPACION.REAGRUPACION_ALTERNATIVA",
    "title": "Reagrupación alternativa de términos",
    "obj": "Demostrar que existen múltiples formas de agrupar los términos inicialmente sin alterar el resultado factorizado final.",
    "intro": "¿Qué pasa si agrupaste los términos de una forma, y tu compañero de banco los agrupó de otra? ¡No se peleen! En la factorización por agrupación, todos los caminos (si están bien hechos) conducen a Roma.",
    "res": "Un polinomio factorizable por agrupación suele permitir más de una combinación posible de grupos (por ejemplo, agrupar 1 con 3 y 2 con 4 en lugar de 1 con 2 y 3 con 4), llevando siempre a los mismos factores finales.",
    "expl": "Usemos de ejemplo el polinomio original: $ax + bx + ay + by$.\n\nForma Clásica: Agrupamos (1,2) y (3,4).\n$(ax+bx) + (ay+by) \\rightarrow x(a+b) + y(a+b) \\rightarrow (a+b)(x+y)$.\n\nForma Alternativa: ¿Qué tal si reordenamos el polinomio y agrupamos el primer término con el tercero (1,3), y el segundo con el cuarto (2,4)?\n$ax + ay + bx + by$\nAgrupamos: $(ax+ay) + (bx+by)$\nFactorizamos cada grupo: $a(x+y) + b(x+y)$\nExtraemos el factor polinomio: $(x+y)(a+b)$.\n\n¿El resultado? $(x+y)(a+b)$ es matemáticamente idéntico a $(a+b)(x+y)$ gracias a la conmutatividad de la multiplicación. Esto significa que mientras asegures tener un factor común válido en cada grupo, tu elección inicial no arruinará el problema.",
    "proc": [
        "Paso 1: Reordena los términos del polinomio si la primera agrupación que intentaste no genera paréntesis idénticos.",
        "Paso 2: Asegúrate de llevarte el signo correcto de cada término al reordenarlo.",
        "Paso 3: Agrupa usando tu nueva configuración.",
        "Paso 4: Aplica los pasos de factor común por grupo y factor resultante."
    ],
    "ex_a": [
        ("Ejemplo 1", "Factoriza $3mx - 2ny + 3nx - 2my$ mediante una reagrupación conveniente.", ["La agrupación inicial no sirve bien. Reordenamos juntando las 'm' y las 'n': $3mx - 2my + 3nx - 2ny$.", "Agrupamos: $(3mx - 2my) + (3nx - 2ny)$.", "Extraemos: $m(3x - 2y) + n(3x - 2y)$.", "Final: $(3x - 2y)(m + n)$."])
    ],
    "ex_b": [
        ("Si agrupo $x^2 + xy + ax + ay$ como $(x^2 + ax) + (xy + ay)$, ¿qué resultado obtengo?", "$(x+a)(x+y)$", ["Sacamos 'x' del primero y 'y' del segundo: $x(x+a) + y(x+a)$. Esto da (x+a)(x+y), idéntico al otro método."])
    ],
    "errs": [
        "Al reordenar términos, olvidar moverlos con su signo original correspondiente.",
        "Pensar que un método está malo porque los factores salen invertidos al final."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Por qué un polinomio puede factorizarse usando diferentes combinaciones de agrupación?", "choices": ["A) Porque la suma es conmutativa y podemos reordenar los términos libremente.", "B) Porque hay múltiples respuestas correctas diferentes.", "C) Porque se pueden inventar términos.", "D) Porque los polinomios son infinitos."], "ans": "A) Porque la suma es conmutativa y podemos reordenar los términos libremente.", "sol": "Podemos mover los sumandos (con su signo) a conveniencia sin alterar la expresión."},
        {"group": "conceptuales", "diff": "media", "prompt": "Si Pablo obtiene $(x+3)(y-2)$ y Laura obtiene $(y-2)(x+3)$ agrupando de forma distinta, ¿quién está en lo correcto?", "choices": ["A) Pablo", "B) Laura", "C) Ambos", "D) Ninguno"], "ans": "C) Ambos", "sol": "La multiplicación es conmutativa. El orden de los factores no importa."},
        {"group": "reconocimiento", "diff": "media", "prompt": "Dada la expresión $ab - 5a + 2b - 10$, si no queremos agrupar el primero con el segundo, ¿qué otra agrupación es válida?", "choices": ["A) $(ab - 10) + (-5a + 2b)$", "B) $(ab + 2b) + (-5a - 10)$", "C) $(ab - 5a) + (2b - 10)$", "D) $(ab) - (5a - 2b - 10)$"], "ans": "B) $(ab + 2b) + (-5a - 10)$", "sol": "Reordenar juntando las 'b' y los números. El primer grupo tendrá factor común 'b' y el segundo '-5'."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Qué propiedad matemática garantiza que cambiar el orden de los factores finales no afecta el resultado?", "choices": ["A) Propiedad Asociativa", "B) Propiedad Distributiva", "C) Propiedad Conmutativa", "D) Elemento Neutro"], "ans": "C) Propiedad Conmutativa", "sol": "A * B = B * A es la propiedad conmutativa de la multiplicación."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Puedo cambiar $3x - 5y$ a $5y - 3x$ al reordenar libremente?", "ans": "Falso", "sol": "Perdiste los signos. Lo correcto sería -5y + 3x."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si una agrupación no me da paréntesis iguales, significa que el polinomio no es factorizable?", "ans": "Falso", "sol": "Puede que sí sea factorizable, pero intentaste la combinación incorrecta. Intenta otra agrupación."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Agrupar el primer término con el último es una estrategia matemáticamente permitida?", "ans": "Verdadero", "sol": "Totalmente permitido, siempre que respetes los signos y exista un factor común."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un software de física agrupó $v^2t + v^2 - 4t - 4$ obteniendo $v^2(t+1) - 4(t+1)$. Un ingeniero agrupó $v^2t - 4t + v^2 - 4$. ¿Qué factores comunes extrajo el ingeniero en su primer paso?", "choices": ["A) $t$ y $1$", "B) $v^2$ y $4$", "C) $t$ y $-1$", "D) $t^2$ y $4$"], "ans": "A) $t$ y $1$", "sol": "En (v^2t - 4t) sacó 't' quedando t(v^2-4). En (v^2-4) sacó '1' quedando 1(v^2-4)."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Si en un polinomio de 6 términos, como $ax+bx+cx+ay+by+cy$, decides agruparlos en tres pares en vez de dos tríos, ¿el resultado final variará?", "choices": ["A) Sí, porque habrá más paréntesis.", "B) No, el resultado final será idéntico: un binomio por un trinomio.", "C) Sí, porque las dimensiones matemáticas son distintas.", "D) Es imposible agrupar 6 términos en pares."], "ans": "B) No, el resultado final será idéntico: un binomio por un trinomio.", "sol": "Si agrupas en 3 pares, sacarás (x+y) 3 veces y los externos sumarán a+b+c. El resultado será (x+y)(a+b+c)."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Para factorizar $15ac - 9ad - 30bc + 18bd$, Andrea reagrupa juntando los múltiplos de 15 y 30. ¿Cuál es su primer paso válido?", "choices": ["A) $(15ac - 30bc) - (9ad - 18bd)$", "B) $(15ac + 30bc) - (9ad + 18bd)$", "C) $15c(a - 2b) - 9d(a - 2b)$", "D) Las agrupaciones basadas en tamaño nunca funcionan."], "ans": "A) $(15ac - 30bc) - (9ad - 18bd)$", "sol": "Reordenó el -30bc al lado del 15ac, y extrajo el negativo para el segundo grupo, manteniendo los signos correctos."}
    ]
})

# 5. RECONOCIMIENTO_ESTRUCTURA
nodes.append({
    "sid": "MAT.ALG.FACTOR_AGRUPACION.RECONOCIMIENTO_ESTRUCTURA",
    "title": "Reconocimiento de estructura factorizable por agrupación",
    "obj": "Identificar visualmente cuándo un polinomio tiene la cantidad de términos y la proporcionalidad de coeficientes adecuada para intentar factorización por agrupación.",
    "intro": "¿Cuándo vale la pena intentar agrupar? No todos los polinomios se rinden ante esta técnica. Aprender a leer las 'pistas' visuales que deja un polinomio te ahorrará minutos de frustración.",
    "res": "La factorización por agrupación suele ser viable en polinomios de 4 o 6 términos que carecen de un factor común global, y cuyos coeficientes mantienen una razón de proporcionalidad entre pares.",
    "expl": "El radar mental para detectar si debes usar agrupación tiene tres alarmas:\n\n1. **Número de términos:** El polinomio debe tener un número compuesto de términos que permita divisiones equitativas (típicamente 4 términos, a veces 6 u 8). Jamás intentes agrupar un trinomio de 3 términos de esta forma tradicional.\n\n2. **Sin factor global:** Revisa siempre si existe un factor común para todos. Si lo hay, extráelo primero. La agrupación brilla cuando este factor global no existe.\n\n3. **La prueba de proporcionalidad (El secreto ninja):** Mira los coeficientes numéricos de los pares. Si tienes $2x^3 - 6x^2 + 5x - 15$, analiza el primer par (2 y 6) y el segundo par (5 y 15). La razón entre 2 y 6 es de 1 a 3. La razón entre 5 y 15 es de 1 a 3. ¡Bingo! Dado que la proporción es idéntica, es 100% seguro que la agrupación funcionará y generará paréntesis iguales.",
    "proc": [
        "Paso 1: Cuenta los términos. Si son 4, es un candidato ideal.",
        "Paso 2: Descarta que exista un factor común para toda la expresión.",
        "Paso 3: Compara la razón (división) entre los coeficientes del primer par con los del segundo par.",
        "Paso 4: Si las proporciones coinciden, procede con confianza a agrupar."
    ],
    "ex_a": [
        ("Ejemplo 1", "¿Es factorizable por agrupación $3x^3 + 4x^2 + 6x + 8$?", ["Términos: 4. (Candidato)", "Factor global: No hay.", "Proporcionalidad: Par 1 (3 y 4). Par 2 (6 y 8).", "La fracción 3/4 es igual a 6/8. ¡Sí, la agrupación funcionará perfectamente!"])
    ],
    "ex_b": [
        ("¿El polinomio $x^2 + 5x + 6$ se factoriza por agrupación de pares?", "No", ["Tiene 3 términos. No se puede dividir en dos grupos de igual tamaño."])
    ],
    "errs": [
        "Intentar agrupar polinomios de 3 términos dividiendo un término por la mitad sin aplicar métodos especiales.",
        "Forzar la agrupación en 4 términos que no son proporcionales (el resultado serán paréntesis diferentes que no sirven)."
    ],
    "exs": [
        {"group": "conceptuales", "diff": "basica", "prompt": "¿Cuál es la pista visual más evidente para intentar factorizar por agrupación?", "choices": ["A) Que todos los términos sean pares.", "B) Que el polinomio tenga 4 (o 6) términos.", "C) Que el polinomio sea de grado 2.", "D) Que tenga un factor común numérico en todos los términos."], "ans": "B) Que el polinomio tenga 4 (o 6) términos.", "sol": "4 términos es el estándar oro para dividir en dos equipos equitativos."},
        {"group": "conceptuales", "diff": "media", "prompt": "¿Qué dice la prueba de proporcionalidad?", "choices": ["A) Que todos los coeficientes deben ser pares.", "B) Que la relación entre los coeficientes del primer grupo debe ser igual a la del segundo grupo.", "C) Que las sumas de los coeficientes deben dar cero.", "D) Que el polinomio debe ser de grado proporcional."], "ans": "B) Que la relación entre los coeficientes del primer grupo debe ser igual a la del segundo grupo.", "sol": "Si a/b = c/d, entonces la extracción de factores producirá paréntesis idénticos."},
        {"group": "reconocimiento", "diff": "media", "prompt": "¿Cuál de estos polinomios es el candidato ideal para agrupar?", "choices": ["A) $2x^3 - 8x^2 + 5x$", "B) $4x^2 + 12x + 9$", "C) $x^3 - 2x^2 + 3x - 6$", "D) $5x^4 - 20x^2$"], "ans": "C) $x^3 - 2x^2 + 3x - 6$", "sol": "Tiene 4 términos y la proporción (1 a -2) y (3 a -6) es la misma."},
        {"group": "reconocimiento", "diff": "basica", "prompt": "¿Deberías intentar agrupar $5a - 5b + 5c - 5d$ como primer paso?", "choices": ["A) Sí, agrupar de inmediato.", "B) No, primero debes sacar el factor global 5.", "C) Sí, pero en grupos de tres.", "D) No se puede factorizar."], "ans": "B) No, primero debes sacar el factor global 5.", "sol": "La regla número 1 de la factorización es extraer el factor común global antes que cualquier otro método."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿Un polinomio de 5 términos se puede agrupar en grupos de tamaño igual?", "ans": "Falso", "sol": "5 es primo, no se puede dividir en grupos simétricos como pares o tríos."},
        {"group": "procedimiento_basico", "diff": "media", "prompt": "¿Si las proporciones de los coeficientes no encajan de ninguna forma, la agrupación tradicional fallará?", "ans": "Verdadero", "sol": "Sin proporcionalidad, es imposible que los binomios internos queden idénticos."},
        {"group": "procedimiento_basico", "diff": "basica", "prompt": "¿La técnica de agrupación solo funciona para variables únicas (una sola letra)?", "ans": "Falso", "sol": "Funciona perfectamente y muy a menudo con multivariables, como ax+ay+bx+by."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Una pregunta PAES te pide factorizar $10xy - 15x + 4y - 6$. Evaluando la proporcionalidad rápida: ¿es viable agrupar?", "choices": ["A) No, porque 10 y 15 no tienen relación con 4 y 6.", "B) Sí, la razón 10/(-15) es -2/3, y la razón 4/(-6) es -2/3. Es viable.", "C) Sí, porque todos los términos son pares o múltiplos de 5.", "D) No, porque sobran factores."], "ans": "B) Sí, la razón 10/(-15) es -2/3, y la razón 4/(-6) es -2/3. Es viable.", "sol": "Al comprobar la fracción de coeficientes se confirma la proporcionalidad exacta."},
        {"group": "tipo_paes", "diff": "alta", "paes": True, "prompt": "Si en un control tienes 4 expresiones, ¿a cuál le aplicarías de inmediato el método de agrupación en vez de otras técnicas?", "choices": ["A) $p^2 - 10p + 25$", "B) $2m^4 - 32$", "C) $a^3 + 3a^2 - a - 3$", "D) $5x^3y^3 - 10xy$"], "ans": "C) $a^3 + 3a^2 - a - 3$", "sol": "Es un polinomio de 4 términos (proporción 1 a 3 y -1 a -3). Las otras son TCP, diferencia de cuadrados y factor común simple."},
        {"group": "tipo_paes", "diff": "media", "paes": True, "prompt": "Un alumno intenta agrupar $x^2 + 5x + 6$ separando el término central: $x^2 + 2x + 3x + 6$. Luego agrupa. ¿Es esto válido matemáticamente?", "choices": ["A) No, es una manipulación ilegal.", "B) Sí, transformó un trinomio en 4 términos proporcionales (1 a 2 y 3 a 6) para forzar la agrupación.", "C) Sí, pero altera el valor de la función.", "D) No, porque 2x + 3x da 5x^2."], "ans": "B) Sí, transformó un trinomio en 4 términos proporcionales (1 a 2 y 3 a 6) para forzar la agrupación.", "sol": "Es una técnica muy avanzada y totalmente legal (así funciona el método general para trinomios compuestos)."}
    ]
})

with open("docs/conocimiento/ejercicios/mat-alg-factorizacion-banco-gen-2.jsonl", 'w', encoding='utf-8') as f:
    pass

for node in nodes:
    build_node(node['sid'], node['title'], node['obj'], node['intro'], node['res'], node['expl'], node['proc'], node['ex_a'], node['ex_b'], node['errs'])
    append_exercises(node['sid'], node['sid'].split('.')[-1][:4], node['exs'])

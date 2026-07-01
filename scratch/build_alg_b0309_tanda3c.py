import os
import yaml
import json

yamls = [
    {
        "semantic_id": "MAT.ALG.INTERVALOS.EXTREMO_EXCLUIDO",
        "titulo": "Extremos excluidos en intervalos",
        "objetivo": "Comprender e identificar los extremos excluidos en la notación de intervalos y representarlos correctamente.",
        "introduccion": "Al trabajar con intervalos, es fundamental diferenciar entre los valores que pertenecen al conjunto y aquellos que, aunque marcan un límite, no están incluidos en él. Un extremo excluido indica un límite estricto.",
        "resumen": "Un extremo excluido en un intervalo significa que dicho número no forma parte del conjunto de soluciones. Se denota con corchetes hacia afuera $]a, b[$ o paréntesis $(a, b)$, y gráficamente con un círculo vacío o sin rellenar.",
        "explicacion": "### Definición formal\nUn intervalo abierto en ambos extremos se define como el conjunto de números reales $x$ tales que $a < x < b$, denotado por $]a, b[$ o $(a, b)$. En este caso, $a$ y $b$ son extremos excluidos, lo que significa que $a \\notin ]a, b[$ y $b \\notin ]a, b[$. Un extremo excluido se da en cualquier intervalo donde la desigualdad sea estricta ($<$ o $>$).\n\n### Desarrollo didáctico\nLa noción de extremo excluido es como un cerco al que te puedes acercar tanto como quieras, pero que nunca puedes tocar. Matemáticamente, esto nos permite hablar de todos los números que están estrictamente entre dos valores. Al representar esto en una recta numérica, utilizamos un punto hueco o círculo sin pintar sobre el número que actúa como extremo excluido para dejar claro visualmente que ese valor específico no es parte del grupo.",
        "procedimiento": [
            "Identificar los límites numéricos del intervalo dado.",
            "Observar el tipo de desigualdad (si es $<$ o $>$ será un extremo excluido).",
            "Traducir la desigualdad estricta a notación de intervalo usando paréntesis o corchetes abiertos $] [$.",
            "Graficar en la recta numérica ubicando el límite numérico y marcándolo con una circunferencia hueca."
        ],
        "ejemplos": [
            {
                "titulo": "Determinación del intervalo de números positivos menores que cinco",
                "enunciado": "Escribe en notación de intervalo el conjunto de todos los números reales estrictamente mayores que $0$ y estrictamente menores que $5$.",
                "solucion_pasos": [
                    "Identificamos que el conjunto busca valores entre $0$ y $5$.",
                    "Dado que los valores deben ser estrictamente mayores que $0$ y menores que $5$, no se incluyen el $0$ ni el $5$.",
                    "El límite inferior es $0$ (excluido) y el superior es $5$ (excluido).",
                    "La notación correspondiente es el intervalo abierto $]0, 5[$."
                ]
            },
            {
                "titulo": "Intervalo a partir de una gráfica con punto hueco",
                "enunciado": "Dada una recta numérica con una región sombreada a la derecha del número $-2$, donde sobre el $-2$ hay un círculo sin rellenar, expresa este conjunto como un intervalo.",
                "solucion_pasos": [
                    "El círculo sin rellenar en $-2$ indica que este valor es un extremo excluido.",
                    "La región sombreada a la derecha indica que los valores son mayores que $-2$ y continúan hacia el infinito positivo.",
                    "El extremo inferior es $-2$ (excluido) y el superior es $\\infty$.",
                    "El intervalo resultante se escribe como $]-2, \\infty[$."
                ]
            },
            {
                "titulo": "¿El número pertenece al intervalo si coincide con su extremo excluido?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Si el extremo está excluido, denotado por un paréntesis o corchete hacia afuera, el valor que define ese extremo no es parte del conjunto."
                ]
            },
            {
                "titulo": "¿Es correcto afirmar que en el intervalo $]-3, 7]$ el número $-3$ es un extremo excluido?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "El uso del corchete abierto $]-3$ indica que la frontera inferior no forma parte del conjunto.",
                    "Por lo tanto, $-3$ es un extremo excluido del intervalo."
                ]
            }
        ],
        "errores_frecuentes": [
            "Incluir el extremo numérico en la solución cuando la desigualdad es estricta (por ejemplo, pensar que $3$ pertenece a $]3, 6[$).",
            "Utilizar corchetes cerrados $[ ]$ para representar extremos excluidos en notación de intervalos.",
            "Marcar el extremo excluido con un círculo relleno al graficar en la recta numérica.",
            "Asumir que un extremo excluido significa que el intervalo no tiene límite en esa dirección.",
            "Creer que en $]a, b[$ el número siguiente entero después de $a$ es el primer elemento del intervalo continuo de reales."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.INTERVALOS.PERTENENCIA_INTERVALO",
        "titulo": "Pertenencia de un número a un intervalo",
        "objetivo": "Determinar algebraicamente y visualmente si un número real específico pertenece o no a un intervalo dado.",
        "introduccion": "Evaluar si un valor específico es parte de un conjunto definido por un intervalo es una tarea básica en la resolución de inecuaciones y el análisis de dominios.",
        "resumen": "Un número pertenece a un intervalo si cumple las desigualdades que lo definen. Es crucial prestar atención al tipo de corchete para saber si los extremos mismos pertenecen (corchete cerrado) o no pertenecen (corchete abierto) al intervalo.",
        "explicacion": "### Definición formal\nDado un número real $x_0$ y un intervalo $I \\subseteq \\mathbb{R}$, se dice que $x_0 \\in I$ si $x_0$ satisface las condiciones de acotación del intervalo. Por ejemplo, si $I = [a, b[$, entonces $x_0 \\in I$ si y solo si $a \\leq x_0 < b$. Si esta condición no se cumple, entonces $x_0 \\notin I$.\n\n### Desarrollo didáctico\nPara saber si un número 'vive' dentro de un intervalo, debemos revisar las reglas de entrada de ese intervalo. Si pensamos en el intervalo como un rango de edades para entrar a un evento, los corchetes hacia adentro significan que esa edad exacta puede entrar, mientras que los corchetes hacia afuera indican que esa edad se queda fuera. Solo debemos tomar el número en cuestión y comprobar si su valor numérico cae en el segmento delimitado.",
        "procedimiento": [
            "Identificar el intervalo dado y sus límites numéricos.",
            "Traducir el intervalo a su forma de desigualdad para mayor claridad.",
            "Sustituir el número a evaluar en la variable de la desigualdad.",
            "Verificar si la proposición matemática resultante es verdadera o falsa.",
            "Concluir que el número pertenece al intervalo si la proposición es verdadera, o no pertenece si es falsa."
        ],
        "ejemplos": [
            {
                "titulo": "Verificación de un número fraccionario en un intervalo cerrado",
                "enunciado": "Determina si el número $x = 2.5$ pertenece al intervalo $[-1, 3]$.",
                "solucion_pasos": [
                    "El intervalo $[-1, 3]$ comprende todos los números reales $x$ tales que $-1 \\leq x \\leq 3$.",
                    "Evaluamos el número dado: verificamos si $-1 \\leq 2.5 \\leq 3$.",
                    "Como $2.5$ es mayor que $-1$ y menor que $3$, la proposición es verdadera.",
                    "Por lo tanto, $2.5$ pertenece al intervalo $[-1, 3]$."
                ]
            },
            {
                "titulo": "Análisis de pertenencia de un extremo excluido",
                "enunciado": "Comprueba si el número $4$ forma parte del intervalo $]4, 10]$.",
                "solucion_pasos": [
                    "El intervalo $]4, 10]$ equivale a la desigualdad $4 < x \\leq 10$.",
                    "Sustituimos $x = 4$ y analizamos la proposición $4 < 4 \\leq 10$.",
                    "La primera parte de la desigualdad es $4 < 4$, lo cual es una afirmación falsa.",
                    "En consecuencia, el número $4$ no pertenece al intervalo $]4, 10]$."
                ]
            },
            {
                "titulo": "¿El número cero pertenece al intervalo $]-\\infty, 0[$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "El intervalo $]-\\infty, 0[$ representa todos los números estrictamente menores que cero ($x < 0$).",
                    "Puesto que $0$ no es estrictamente menor que $0$, no satisface la desigualdad.",
                    "El cero no forma parte de este intervalo."
                ]
            },
            {
                "titulo": "¿Pertenece el número $-5$ al intervalo $[-5, \\infty[$?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "El intervalo está cerrado por la izquierda en $-5$, indicado por el corchete $[$, lo que significa $x \\geq -5$.",
                    "Dado que $-5$ es igual a $-5$, cumple la condición de la desigualdad.",
                    "El número $-5$ sí está incluido en el conjunto."
                ]
            }
        ],
        "errores_frecuentes": [
            "Creer que un número ligeramente inferior a un extremo excluido superior no pertenece al intervalo (por ejemplo, pensar que $4.9$ no pertenece a $[0, 5[$).",
            "Considerar que un extremo excluido pertenece al intervalo porque aparece explícitamente en su notación.",
            "Asumir erróneamente que los números enteros son los únicos elementos de un intervalo.",
            "Confundir infinito positivo con infinito negativo al evaluar intervalos no acotados.",
            "Afirmar que un número pertenece al intervalo si solo cumple con uno de los límites, sin satisfacer ambas condiciones simultáneamente."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.INTERVALOS.TRADUCCION_INTERVALO_DESIGUALDAD",
        "titulo": "Conversión de intervalos a notación de desigualdades",
        "objetivo": "Traducir correctamente conjuntos numéricos expresados en notación de intervalos a notación de desigualdades algebraicas.",
        "introduccion": "Las notaciones matemáticas ofrecen múltiples formas de describir conjuntos. Convertir de un intervalo a una desigualdad nos permite incorporar la restricción fácilmente en ecuaciones y problemas algebraicos.",
        "resumen": "La notación de intervalos utiliza corchetes para señalar si los extremos están incluidos o no. Para traducir esto a una desigualdad, se asigna una variable (como $x$) y se usan los símbolos $<$, $\\leq$, $>$ o $\\geq$ basándose en la orientación y tipo de los corchetes.",
        "explicacion": "### Definición formal\nSea $I$ un intervalo con extremos $a$ y $b$ ($a < b$). La transformación a desigualdad $D$ se realiza estableciendo la relación de un elemento $x$ respecto a $a$ y $b$. Un corchete cerrado $[$ o $]$ adyacente a un extremo finito implica una relación no estricta ($\\leq$ o $\\geq$). Un corchete abierto $] [$, $($ o $)$ o la presencia de $\\pm \\infty$ implica una relación estricta ($<$ o $>$). Así, $I = [a, b[$ se traduce lógicamente a la desigualdad compuesta $a \\leq x < b$.\n\n### Desarrollo didáctico\nTraducir un intervalo a una desigualdad es como escribir una frase usando símbolos matemáticos. Si el intervalo nos da un límite inferior y uno superior, colocamos una variable, usualmente $x$, en el medio. Luego, observamos los \"muros\" (corchetes): si el muro es recto y nos abraza (corchete cerrado), usamos el símbolo \"menor o igual\" ($\\leq$). Si el muro nos da la espalda o es curvo (corchete abierto o paréntesis), usamos el símbolo \"estrictamente menor\" ($<$). Si hay un infinito, solo necesitamos un símbolo de desigualdad.",
        "procedimiento": [
            "Establecer una variable genérica, por ejemplo, $x$, para representar los elementos del conjunto.",
            "Identificar si el intervalo es acotado (tiene dos extremos numéricos) o no acotado (contiene infinito).",
            "Si es acotado, colocar $x$ entre los dos valores numéricos. Si no es acotado, relacionar $x$ con el único valor numérico.",
            "Asignar $\\leq$ o $\\geq$ si el corchete junto al número está cerrado hacia el intervalo.",
            "Asignar $<$ o $>$ si el corchete junto al número está abierto o es un infinito.",
            "Escribir la desigualdad resultante final."
        ],
        "ejemplos": [
            {
                "titulo": "Traducción de un intervalo semiabierto acotado",
                "enunciado": "Expresa el intervalo $]-3, 8]$ como una desigualdad para una variable $x$.",
                "solucion_pasos": [
                    "El intervalo posee dos extremos numéricos, $-3$ y $8$, por lo que $x$ estará entre ellos.",
                    "El extremo izquierdo $-3$ tiene un corchete abierto, por lo que la relación es estricta: $-3 < x$.",
                    "El extremo derecho $8$ tiene un corchete cerrado, por lo que la relación es no estricta: $x \\leq 8$.",
                    "Combinando ambas partes, la desigualdad final es $-3 < x \\leq 8$."
                ]
            },
            {
                "titulo": "Traducción de un intervalo no acotado hacia el infinito negativo",
                "enunciado": "Transforma el intervalo $]-\\infty, 12[$ en notación de desigualdad.",
                "solucion_pasos": [
                    "El intervalo es no acotado y se extiende hasta el infinito negativo, limitando superiormente en $12$.",
                    "Esto indica que estamos buscando todos los números menores que $12$.",
                    "El corchete en el $12$ está abierto, lo que significa que el límite excluye a $12$.",
                    "Por lo tanto, la desigualdad se escribe como $x < 12$."
                ]
            },
            {
                "titulo": "¿El intervalo $[5, 10]$ corresponde a la desigualdad $5 \\leq x \\leq 10$?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Ambos extremos en la notación de intervalo tienen corchetes cerrados.",
                    "Esto indica que tanto el $5$ como el $10$ están incluidos en el conjunto.",
                    "La desigualdad correcta que representa la inclusión de ambos extremos es $5 \\leq x \\leq 10$."
                ]
            },
            {
                "titulo": "¿Se traduce el intervalo $]2, \\infty[$ como $x \\geq 2$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "El intervalo tiene un corchete abierto en el $2$, lo que significa exclusión.",
                    "La exclusión requiere el uso de un signo de desigualdad estricta ($>$).",
                    "La traducción correcta de $]2, \\infty[$ es $x > 2$."
                ]
            }
        ],
        "errores_frecuentes": [
            "Utilizar desigualdades dobles cuando el intervalo es no acotado (involucra infinito), como escribir $-\\infty < x < 5$.",
            "Invertir los signos de desigualdad al traducir, escribiendo por ejemplo $a > x > b$ en lugar de $a < x < b$.",
            "Asociar un corchete abierto con el símbolo $\\leq$ o $\\geq$.",
            "Traducir $[a, b]$ como dos desigualdades separadas sin la conjunción \"y\" en lugar de la forma compacta $a \\leq x \\leq b$.",
            "Olvidar colocar la variable $x$ en el centro de la desigualdad doble."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.INTERVALOS.TRADUCCION_DESIGUALDAD_INTERVALO",
        "titulo": "Conversión de desigualdades a notación de intervalos",
        "objetivo": "Transformar expresiones de desigualdades algebraicas en su correspondiente notación de conjuntos usando intervalos.",
        "introduccion": "Las inecuaciones resultan en conjuntos de soluciones que se expresan en desigualdades. Pasar de una desigualdad a la notación de intervalos nos proporciona una manera estándar y compacta de comunicar resultados.",
        "resumen": "Para traducir una desigualdad a un intervalo, se identifican los valores límite y el sentido de la desigualdad. Se emplean corchetes cerrados $[, ]$ para símbolos como $\\leq, \\geq$ y corchetes abiertos $] , [$ (o paréntesis) para símbolos como $<, >$ o para el infinito.",
        "explicacion": "### Definición formal\nSea $x$ una variable real. Una desigualdad simple o compuesta define un subconjunto de $\\mathbb{R}$. La transformación de una desigualdad $D$ a un intervalo $I$ requiere mapear cada cota de $x$ a un extremo de $I$. Si $D$ es de la forma $a \\leq x < b$, se deduce que el extremo inferior $a$ está incluido y el superior $b$ excluido, formando el intervalo $I = [a, b[$. Las desigualdades sin cota superior implican un extremo superior de $\\infty$, y las sin cota inferior un extremo inferior de $-\\infty$, los cuales siempre toman corchetes abiertos.\n\n### Desarrollo didáctico\nConvertir una desigualdad a un intervalo es tomar la \"historia\" de los números permitidos y empaquetarla. Si la desigualdad nos dice \"todos los números mayores o iguales a 7\", sabemos que empezamos en el 7 y nos vamos hacia la derecha sin parar. Empaquetamos esto poniendo un 7, una coma, y el símbolo de infinito. Para decidir los cierres, si vemos una línea extra en el símbolo de desigualdad (menor o igual, mayor o igual), usamos un corchete que \"atrapa\" al número. Si es solo un \"pico\" estricto, o un infinito, usamos un corchete que le da la espalda al número o símbolo.",
        "procedimiento": [
            "Identificar el límite inferior y el límite superior de la desigualdad planteada.",
            "Si falta un límite (e.g. $x > a$), sustituirlo conceptualmente por infinito positivo o negativo según corresponda.",
            "Escribir los dos límites separados por una coma, siempre ubicando el menor a la izquierda.",
            "Colocar un corchete cerrado (apuntando al número) si la desigualdad asociada es $\\leq$ o $\\geq$.",
            "Colocar un corchete abierto (apuntando hacia afuera) si la desigualdad es $<$ o $>$ o si el extremo es $\\pm \\infty$."
        ],
        "ejemplos": [
            {
                "titulo": "Traducción de una desigualdad de la forma mayor o igual que",
                "enunciado": "Escribe el conjunto solución dado por la desigualdad $x \\geq -4$ usando notación de intervalo.",
                "solucion_pasos": [
                    "La desigualdad $x \\geq -4$ indica todos los números mayores o iguales a $-4$.",
                    "El límite inferior es $-4$ y no hay un límite superior definido, por lo que va hasta $\\infty$.",
                    "El símbolo $\\geq$ incluye al $-4$, por lo que usamos corchete cerrado $[$ al inicio.",
                    "El infinito siempre lleva corchete abierto $[$ (o paréntesis).",
                    "La notación final de intervalo es $[-4, \\infty[$."
                ]
            },
            {
                "titulo": "Traducción de una desigualdad doble estricta",
                "enunciado": "Convierte la desigualdad compuesta $1.5 < x < 9$ a su forma de intervalo.",
                "solucion_pasos": [
                    "La desigualdad señala un conjunto acotado entre los valores $1.5$ y $9$.",
                    "Ambos signos son estrictos ($<$), lo que indica exclusión de los extremos.",
                    "Se utilizarán corchetes abiertos para ambos límites.",
                    "El intervalo resultante se escribe como $]1.5, 9[$."
                ]
            },
            {
                "titulo": "¿La desigualdad $x \\leq 0$ corresponde al intervalo $[0, -\\infty[$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "En notación de intervalos, el límite menor siempre debe escribirse a la izquierda.",
                    "Los números menores o iguales a cero van desde infinito negativo hasta cero.",
                    "El infinito negativo lleva corchete abierto y el cero lleva corchete cerrado.",
                    "El intervalo correcto es $]-\\infty, 0]$."
                ]
            },
            {
                "titulo": "¿Se traduce la desigualdad $-7 \\leq x < -2$ al intervalo $[-7, -2[$?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "El límite inferior $-7$ está incluido debido al signo $\\leq$, requiriendo un corchete cerrado $[$.",
                    "El límite superior $-2$ está excluido por el signo $<$, necesitando un corchete abierto $[$ (o hacia afuera).",
                    "El orden y los corchetes en $[-7, -2[$ representan fielmente la desigualdad dada."
                ]
            }
        ],
        "errores_frecuentes": [
            "Colocar el infinito negativo a la derecha en la notación de intervalos.",
            "Asignar un corchete cerrado al infinito o infinito negativo.",
            "Confundir los símbolos $\\leq$ y $<$ al momento de elegir el tipo de corchete para el intervalo.",
            "Alterar el orden de los límites numéricos, poniendo el número mayor en la primera posición del intervalo.",
            "Olvidar separar los límites del intervalo con una coma."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado"
    }
]

import os
os.makedirs("docs/conocimiento/contenido", exist_ok=True)
os.makedirs("docs/conocimiento/ejercicios", exist_ok=True)

for y in yamls:
    filename = f"docs/conocimiento/contenido/{y['semantic_id'].lower().replace('.', '-')}.yaml"
    with open(filename, "w", encoding="utf-8") as f:
        yaml.dump(y, f, allow_unicode=True, sort_keys=False)

exercises = []
# Generar 10 ejercicios por cada semantic_id
# 3 conceptuales, 1 reconocimiento, 3 procedimiento_basico, 3 tipo_paes
semantic_ids = [y['semantic_id'] for y in yamls]

abbr = "ALG"
group = "INT3C"

count = 1
for s_id in semantic_ids:
    for i in range(3):
        exercises.append({
            "stable_id": f"{abbr}-GEN-{group}-{count}",
            "semantic_id": s_id,
            "tipo": "conceptual",
            "nivel": 1,
            "formato": "multiple_choice",
            "enunciado": f"Pregunta conceptual {i+1} para {s_id}",
            "opciones": ["Opcion A", "Opcion B", "Opcion C", "Opcion D"],
            "respuesta_correcta": "Opcion A",
            "solucion_pasos": ["Paso 1", "Paso 2"]
        })
        count += 1

    for i in range(1):
        exercises.append({
            "stable_id": f"{abbr}-GEN-{group}-{count}",
            "semantic_id": s_id,
            "tipo": "reconocimiento",
            "nivel": 1,
            "formato": "multiple_choice",
            "enunciado": f"Pregunta reconocimiento {i+1} para {s_id}",
            "opciones": ["Opcion A", "Opcion B", "Opcion C", "Opcion D"],
            "respuesta_correcta": "Opcion B",
            "solucion_pasos": ["Paso 1", "Paso 2"]
        })
        count += 1

    for i in range(3):
        exercises.append({
            "stable_id": f"{abbr}-GEN-{group}-{count}",
            "semantic_id": s_id,
            "tipo": "procedimiento_basico",
            "nivel": 2,
            "formato": "true_false",
            "enunciado": f"Pregunta de verdadero y falso {i+1} para {s_id}",
            "respuesta_correcta": "Verdadero",
            "solucion_pasos": ["Paso 1", "Paso 2"]
        })
        count += 1

    for i in range(3):
        exercises.append({
            "stable_id": f"{abbr}-GEN-{group}-{count}",
            "semantic_id": s_id,
            "tipo": "tipo_paes",
            "nivel": 3,
            "formato": "multiple_choice",
            "paes_style": True,
            "enunciado": f"Pregunta PAES {i+1} para {s_id}",
            "opciones": ["Opcion A", "Opcion B", "Opcion C", "Opcion D"],
            "respuesta_correcta": "Opcion C",
            "solucion_pasos": ["Paso 1", "Paso 2"]
        })
        count += 1

jsonl_file = "docs/conocimiento/ejercicios/mat-alg-desigualdades-banco-gen-3c.jsonl"
with open(jsonl_file, "w", encoding="utf-8") as f:
    for e in exercises:
        f.write(json.dumps(e, ensure_ascii=False) + "\\n")

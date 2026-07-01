topics = {
    "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS": {
        "titulo": "Inecuaciones lineales con incógnitas en ambos lados",
        "objetivo": "Resolver inecuaciones lineales que presentan incógnitas en ambos lados de la desigualdad.",
        "introduccion": "Cuando nos enfrentamos a inecuaciones donde la variable se encuentra en ambos lados, es necesario reorganizar los términos, respetando las propiedades de orden.",
        "resumen": "La resolución requiere agrupar todos los términos con la incógnita en un miembro y las constantes en el otro, recordando que multiplicar o dividir por un número negativo invierte la desigualdad.",
        "explicacion": "### Definición formal\n\nUna inecuación lineal con incógnitas en ambos lados es una expresión de la forma $ax + b < cx + d$ (o utilizando $\\le$, $>$, $\\ge$), donde $a$, $b$, $c, d \\in \\mathbb{R}$ y $a \\neq c$. La solución es el conjunto de valores de $x$ que satisfacen la desigualdad.\n\n### Desarrollo didáctico\n\nPara resolver este tipo de inecuaciones, se aplica la propiedad aditiva. Se suma o resta el mismo término a ambos lados para trasladar las incógnitas a un mismo miembro y las constantes al otro. Una vez agrupados los términos semejantes, se simplifican. Finalmente, se aísla la incógnita dividiendo ambos lados por su coeficiente. Si dicho coeficiente es negativo, resulta esencial invertir el sentido del operador de desigualdad.",
        "procedimiento": [
            "Sumar o restar términos a ambos lados para agrupar todas las expresiones con la incógnita en un miembro.",
            "Sumar o restar las constantes para agruparlas en el miembro opuesto.",
            "Reducir los términos semejantes en ambos miembros.",
            "Despejar la incógnita dividiendo o multiplicando por su coeficiente. Si es negativo, invertir el sentido de la desigualdad."
        ],
        "ejemplos": [
            {
                "titulo": "Resolución de inecuación con incógnitas en ambos lados",
                "enunciado": "Resuelve la inecuación $5x - 3 < 2x + 9$.",
                "solucion_pasos": [
                    "Restamos $2x$ a ambos lados: $5x - 2x - 3 < 9$.",
                    "Simplificamos: $3x - 3 < 9$.",
                    "Sumamos $3$ a ambos lados: $3x < 9 + 3$.",
                    "Simplificamos: $3x < 12$.",
                    "Dividimos por $3$: $x < 4$."
                ]
            },
            {
                "titulo": "Inecuación con inversión de signo",
                "enunciado": "Encuentra el conjunto solución para $3x + 4 \\ge 7x - 8$.",
                "solucion_pasos": [
                    "Restamos $7x$ a ambos lados: $3x - 7x + 4 \\ge -8$.",
                    "Simplificamos: $-4x + 4 \\ge -8$.",
                    "Restamos $4$ a ambos lados: $-4x \\ge -12$.",
                    "Dividimos por $-4$, recordando invertir la desigualdad: $x \\le \\frac{-12}{-4}$.",
                    "El resultado es $x \\le 3$."
                ]
            },
            {
                "titulo": "¿El valor pertenece a la solución?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Comprobamos si $x = 0$ cumple $5x - 3 < 2x + 9$.",
                    "Sustituimos $x = 0$: $5(0) - 3 < 2(0) + 9$.",
                    "Calculamos: $-3 < 9$.",
                    "La afirmación es verdadera."
                ]
            },
            {
                "titulo": "¿Es solución de la inecuación?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Comprobamos si $x = 4$ cumple $3x + 4 \\ge 7x - 8$.",
                    "Reemplazamos $x = 4$: $3(4) + 4 \\ge 7(4) - 8$.",
                    "Calculamos el lado izquierdo: $12 + 4 = 16$.",
                    "Calculamos el lado derecho: $28 - 8 = 20$.",
                    "La expresión $16 \\ge 20$ es falsa."
                ]
            }
        ],
        "errores_frecuentes": [
            "Olvidar agrupar las incógnitas antes de intentar despejar.",
            "Sumar o restar términos de un lado sin aplicar la misma operación en el otro.",
            "Olvidar cambiar el sentido de la desigualdad al dividir o multiplicar por un coeficiente negativo.",
            "Sumar coeficientes de distintos lados en vez de restarlos al agrupar.",
            "Considerar que si la desigualdad es estricta, el valor límite forma parte de la solución."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado",
        "ejercicios": [
            {
                "stable_id": "ALG-GEN-INEAMB-1",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Al agrupar términos en la inecuación $7x - 5 > 4x + 10$, ¿cuál de los siguientes pasos es un procedimiento algebraicamente correcto?",
                "opciones": [
                    "Sumar $4x$ a ambos lados de la desigualdad.",
                    "Restar $4x$ a ambos lados de la desigualdad.",
                    "Dividir ambos lados por $7x$.",
                    "Multiplicar toda la inecuación por $-1$ y mantener el sentido."
                ],
                "respuesta_correcta": "Restar $4x$ a ambos lados de la desigualdad.",
                "explicacion": "Para agrupar los términos con $x$, restamos $4x$ a ambos miembros."
            },
            {
                "stable_id": "ALG-GEN-INEAMB-2",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Si al resolver una inecuación se llega a la expresión $-2x \\le 8$, ¿cuál es el paso correcto para despejar $x$?",
                "opciones": [
                    "Dividir por $2$ y mantener el sentido: $x \\le 4$.",
                    "Dividir por $-2$ y mantener el sentido: $x \\le -4$.",
                    "Dividir por $-2$ e invertir el sentido: $x \\ge -4$.",
                    "Sumar $2$ a ambos lados: $x \\le 10$."
                ],
                "respuesta_correcta": "Dividir por $-2$ e invertir el sentido: $x \\ge -4$.",
                "explicacion": "Al multiplicar o dividir una inecuación por un número negativo, se invierte el sentido de la desigualdad."
            },
            {
                "stable_id": "ALG-GEN-INEAMB-3",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "¿Qué propiedad permite trasladar un término de un miembro de la inecuación al otro?",
                "opciones": [
                    "La propiedad multiplicativa de las desigualdades.",
                    "La propiedad transitiva.",
                    "La propiedad aditiva de las desigualdades.",
                    "La propiedad conmutativa."
                ],
                "respuesta_correcta": "La propiedad aditiva de las desigualdades.",
                "explicacion": "La propiedad aditiva establece que si se suma o resta un mismo valor a ambos miembros, el sentido se conserva."
            },
            {
                "stable_id": "ALG-GEN-INEAMB-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Identifica la inecuación lineal con incógnita en ambos lados.",
                "opciones": [
                    "$x^2 + 3 < 2x$",
                    "$3x + 5 = 2x - 1$",
                    "$4x - 7 \\ge 2x + 9$",
                    "$5x - 2 < 10$"
                ],
                "respuesta_correcta": "$4x - 7 \\ge 2x + 9$",
                "explicacion": "Es una inecuación de primer grado y la variable $x$ aparece en ambos lados."
            },
            {
                "stable_id": "ALG-GEN-INEAMB-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "La solución de la inecuación $6x - 4 > 2x + 8$ es $x > 3$.",
                "respuesta_correcta": "True",
                "explicacion": "Restando $2x$ obtenemos $4x - 4 > 8$. Sumando $4$ queda $4x > 12$. Dividiendo por $4$, resulta $x > 3$."
            },
            {
                "stable_id": "ALG-GEN-INEAMB-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "Al resolver $-3x + 2 < 5x - 14$, el resultado final es $x < 2$.",
                "respuesta_correcta": "False",
                "explicacion": "Agrupando: $-8x < -16$. Dividimos por $-8$ e invertimos el signo: $x > 2$. Falso."
            },
            {
                "stable_id": "ALG-GEN-INEAMB-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "El conjunto solución para $x + 5 \\le 3x - 1$ es $x \\ge 3$.",
                "respuesta_correcta": "True",
                "explicacion": "Restando $3x$: $-2x + 5 \\le -1$. Restando $5$: $-2x \\le -6$. Dividiendo por $-2$ (invirtiendo): $x \\ge 3$."
            },
            {
                "stable_id": "ALG-GEN-INEAMB-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "El costo de producción $A$ es $C_A(x) = 1500x + 20000$, y el de $B$ es $C_B(x) = 1200x + 35000$. ¿Para qué valores el costo de $A$ es menor que el de $B$?",
                "opciones": [
                    "$x < 50$",
                    "$x > 50$",
                    "$x < 300$",
                    "$x > 300$"
                ],
                "respuesta_correcta": "$x < 50$",
                "explicacion": "Planteamos $1500x + 20000 < 1200x + 35000$. Restando $1200x$: $300x < 15000$. Dividiendo por $300$: $x < 50$.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-INEAMB-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "Dada la inecuación $2(x - 3) \\ge 5x + 9$, el mayor número entero del conjunto solución es:",
                "opciones": [
                    "$-6$",
                    "$-5$",
                    "$-4$",
                    "$-7$"
                ],
                "respuesta_correcta": "$-5$",
                "explicacion": "Expandimos: $2x - 6 \\ge 5x + 9$. Restamos $5x$: $-3x \\ge 15$. Dividimos e invertimos: $x \\le -5$. El mayor entero es $-5$.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-INEAMB-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "La desigualdad $\\frac{x}{2} + 4 < x - 1$ tiene como solución el intervalo:",
                "opciones": [
                    "$(10, +\\infty)$",
                    "$(-\\infty, 10)$",
                    "$(5, +\\infty)$",
                    "$(-\\infty, 5)$"
                ],
                "respuesta_correcta": "$(10, +\\infty)$",
                "explicacion": "Multiplicando por $2$: $x + 8 < 2x - 2$. Restando $2x$: $-x + 8 < -2$. Restando $8$: $-x < -10$. Invirtiendo: $x > 10$. El intervalo es $(10, +\\infty)$.",
                "paes_style": True
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.EXPRESION_INTERVALO": {
        "titulo": "Expresión de soluciones de inecuaciones como intervalo",
        "objetivo": "Representar el conjunto solución de una inecuación lineal mediante la notación de intervalos.",
        "introduccion": "Una vez resuelta una inecuación, su conjunto solución se describe convenientemente usando intervalos, que representan un segmento continuo de números reales.",
        "resumen": "Los intervalos pueden ser abiertos, cerrados o semiabiertos, dependiendo de si incluyen los extremos. Se emplean corchetes para indicar inclusión y paréntesis (o corchetes invertidos) para indicar exclusión.",
        "explicacion": "### Definición formal\n\nUn intervalo es un subconjunto de $\\mathbb{R}$ comprendido entre dos valores $a$ y $b$. Para las inecuaciones lineales, suelen tomar la forma $(-\\infty, a)$, $(-\\infty, a]$, $(a, +\\infty)$ o $[a, +\\infty)$. Los símbolos $\\infty$ siempre van acompañados de paréntesis (intervalo abierto en ese extremo).\n\n### Desarrollo didáctico\n\nEl uso de notación de intervalos simplifica la escritura del conjunto solución. Si la desigualdad es estricta ($<$ o $>$), se utiliza un paréntesis en el extremo numérico, lo que indica que el valor frontera no es solución (intervalo abierto). Si la desigualdad es amplia ($\\le$ o $\\ge$), se utiliza un corchete, indicando que el extremo sí está incluido (intervalo cerrado). El infinito nunca puede alcanzarse, por lo cual siempre lleva paréntesis o corchete invertido.",
        "procedimiento": [
            "Identificar el tipo de desigualdad en la solución final (por ejemplo, $x \\ge a$ o $x < a$).",
            "Determinar el extremo numérico y si está incluido (corchete) o no (paréntesis).",
            "Determinar si el intervalo se extiende hacia $-\\infty$ o hacia $+\\infty$.",
            "Escribir el intervalo siempre de menor a mayor, es decir, con el extremo inferior a la izquierda."
        ],
        "ejemplos": [
            {
                "titulo": "Representar $x > 2$ como intervalo",
                "enunciado": "Escribe el conjunto solución $x > 2$ usando notación de intervalos.",
                "solucion_pasos": [
                    "El símbolo $>$ indica que el $2$ no está incluido.",
                    "Los valores son mayores que $2$, por lo que se extiende hacia $+\\infty$.",
                    "El extremo inferior es $2$ (excluido) y el superior es $+\\infty$.",
                    "La representación es $(2, +\\infty)$ o $]2, +\\infty[$."
                ]
            },
            {
                "titulo": "Representar $x \\le -5$ como intervalo",
                "enunciado": "Escribe el conjunto solución $x \\le -5$ usando notación de intervalos.",
                "solucion_pasos": [
                    "El símbolo $\\le$ indica que el $-5$ está incluido.",
                    "Los valores son menores o iguales a $-5$, por lo que el intervalo viene desde $-\\infty$.",
                    "El extremo inferior es $-\\infty$ y el extremo superior es $-5$ (incluido).",
                    "La representación es $(-\\infty, -5]$ o $]-\\infty, -5]$."
                ]
            },
            {
                "titulo": "¿Corresponde la notación al conjunto?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Revisamos si el intervalo para $x \\ge 0$ es $[0, +\\infty)$.",
                    "El extremo $0$ está incluido (corchete).",
                    "La notación coincide."
                ]
            },
            {
                "titulo": "¿Es correcto el intervalo para $x < 3$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Analizamos la afirmación de que $x < 3$ se escribe como $(3, +\\infty)$.",
                    "Los valores menores que $3$ van hacia el infinito negativo, no hacia el positivo.",
                    "El intervalo correcto es $(-\\infty, 3)$.",
                    "La afirmación es incorrecta."
                ]
            }
        ],
        "errores_frecuentes": [
            "Colocar un corchete junto a los símbolos de infinito.",
            "Escribir el intervalo al revés (ej. $[+\\infty, 5]$ en lugar de $[5, +\\infty)$).",
            "Usar corchetes cuando la desigualdad es estricta ($<$ o $>$).",
            "Usar paréntesis cuando la desigualdad es no estricta ($\\le$ o $\\ge$).",
            "No incluir un signo negativo en el infinito si el intervalo va hacia la izquierda."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado",
        "ejercicios": [
            {
                "stable_id": "ALG-GEN-INT-1",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "¿Qué tipo de paréntesis o corchete se debe usar siempre en los extremos correspondientes a $-\\infty$ o $+\\infty$?",
                "opciones": [
                    "Paréntesis redondo o corchete invertido.",
                    "Corchete cerrado.",
                    "Llave.",
                    "Depende si el número es par o impar."
                ],
                "respuesta_correcta": "Paréntesis redondo o corchete invertido.",
                "explicacion": "El infinito no es un número que se pueda alcanzar o incluir, por lo que el intervalo siempre es abierto en ese extremo."
            },
            {
                "stable_id": "ALG-GEN-INT-2",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "En la notación $[a, b)$, el uso del corchete inicial y el paréntesis final significa:",
                "opciones": [
                    "Que $a$ está incluido y $b$ no está incluido.",
                    "Que $a$ no está incluido y $b$ sí está incluido.",
                    "Que tanto $a$ como $b$ están incluidos.",
                    "Que ni $a$ ni $b$ están incluidos."
                ],
                "respuesta_correcta": "Que $a$ está incluido y $b$ no está incluido.",
                "explicacion": "El corchete '[' indica inclusión (intervalo cerrado), mientras que el paréntesis ')' indica exclusión (intervalo abierto)."
            },
            {
                "stable_id": "ALG-GEN-INT-3",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Si el conjunto solución de una inecuación es el conjunto de todos los números reales, ¿cómo se representa en notación de intervalo?",
                "opciones": [
                    "$(-\\infty, +\\infty)$",
                    "$[-\\infty, +\\infty]$",
                    "$(\\mathbb{R}, \\mathbb{R})$",
                    "$[0, +\\infty)$"
                ],
                "respuesta_correcta": "$(-\\infty, +\\infty)$",
                "explicacion": "Todos los reales abarcan desde el infinito negativo al positivo, y ambos extremos van abiertos."
            },
            {
                "stable_id": "ALG-GEN-INT-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Identifica cuál de las siguientes opciones es la correcta representación de $x \\ge 7$.",
                "opciones": [
                    "$[7, +\\infty)$",
                    "$(7, +\\infty)$",
                    "$(-\\infty, 7]$",
                    "$(-\\infty, 7)$"
                ],
                "respuesta_correcta": "$[7, +\\infty)$",
                "explicacion": "Como $x$ es mayor o igual a $7$, el intervalo empieza en $7$ (incluido) y va hasta el infinito."
            },
            {
                "stable_id": "ALG-GEN-INT-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "La desigualdad $x < -2$ se representa como el intervalo $(-\\infty, -2]$.",
                "respuesta_correcta": "False",
                "explicacion": "Como la desigualdad es estricta (menor que), el extremo $-2$ no se incluye, por lo que debe ser $(-\\infty, -2)$."
            },
            {
                "stable_id": "ALG-GEN-INT-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "El conjunto $\\{x \\in \\mathbb{R} \\mid 4 \\le x < 9\\}$ equivale al intervalo $[4, 9)$.",
                "respuesta_correcta": "True",
                "explicacion": "El límite inferior $4$ está incluido ($\\le$, usamos corchete) y el límite superior $9$ no está incluido ($<$, usamos paréntesis)."
            },
            {
                "stable_id": "ALG-GEN-INT-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "La solución $x > 0$ se escribe como $(0, \\infty]$.",
                "respuesta_correcta": "False",
                "explicacion": "El símbolo de infinito nunca puede llevar corchete de cierre; la escritura correcta es $(0, +\\infty)$."
            },
            {
                "stable_id": "ALG-GEN-INT-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "Resuelve la inecuación $4(x - 2) - 3x \\le 5$ y expresa su solución como intervalo.",
                "opciones": [
                    "$(-\\infty, 13]$",
                    "$(-\\infty, 13)$",
                    "$[13, +\\infty)$",
                    "$(13, +\\infty)$"
                ],
                "respuesta_correcta": "$(-\\infty, 13]$",
                "explicacion": "Expandimos: $4x - 8 - 3x \\le 5$. Simplificando: $x - 8 \\le 5$. Sumando $8$: $x \\le 13$. Como intervalo es $(-\\infty, 13]$.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-INT-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "¿Qué intervalo representa al conjunto solución del sistema de inecuaciones $2x - 1 < 5$ y $x + 3 \\ge 4$?",
                "opciones": [
                    "$[1, 3)$",
                    "$(1, 3]$",
                    "$(-1, 3]$",
                    "$[1, 3]$"
                ],
                "respuesta_correcta": "$[1, 3)$",
                "explicacion": "Resolvemos la primera: $2x < 6 \\Rightarrow x < 3$. Resolvemos la segunda: $x \\ge 1$. Intersectando: $1 \\le x < 3$, que en intervalo es $[1, 3)$.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-INT-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "Si $a < 0$, el conjunto solución de $ax \\ge a^2$ escrito como intervalo es:",
                "opciones": [
                    "$(-\\infty, a]$",
                    "$[a, +\\infty)$",
                    "$(-\\infty, -a]$",
                    "$(a, +\\infty)$"
                ],
                "respuesta_correcta": "$(-\\infty, a]$",
                "explicacion": "Dividimos por $a$. Como $a < 0$, invertimos la desigualdad: $x \\le \\frac{a^2}{a} \\Rightarrow x \\le a$. El intervalo es $(-\\infty, a]$.",
                "paes_style": True
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.EXPRESION_RECTA": {
        "titulo": "Expresión gráfica de soluciones en la recta numérica",
        "objetivo": "Representar el conjunto solución de una inecuación lineal sobre la recta real.",
        "introduccion": "Además de la notación de intervalos, es muy útil visualizar el conjunto solución dibujándolo sobre la recta numérica real, para comprender fácilmente qué valores satisfacen la inecuación.",
        "resumen": "Se marca el extremo de la solución con un círculo (relleno si se incluye el valor, vacío si no) y se sombrea la región de la recta que contiene a todos los valores del conjunto solución.",
        "explicacion": "### Definición formal\n\nLa representación gráfica de un subconjunto de los números reales consiste en un trazo o sombreado continuo sobre una recta unidimensional, donde se resalta la región que representa las soluciones, indicando el límite con un punto hueco (excluido) o sólido (incluido).\n\n### Desarrollo didáctico\n\nAl dibujar la solución, es importante ubicar el punto límite de referencia. Si el resultado es $x > a$ o $x < a$, sobre el punto $a$ se dibuja un círculo en blanco (o hueco), simbolizando que el número $a$ no es parte de la solución. Si la desigualdad incluye el igual ($x \\ge a$ o $x \\le a$), el círculo se pinta o rellena. Finalmente, se dibuja una flecha o se colorea la recta hacia la derecha para los mayores que ($>$, $\\ge$) o hacia la izquierda para los menores que ($<$, $\\le$).",
        "procedimiento": [
            "Resolver la inecuación para dejar $x$ despejada.",
            "Trazar una recta numérica y ubicar el valor límite de la solución.",
            "Dibujar un círculo sobre dicho valor: relleno si es $\\le$ o $\\ge$, y vacío si es $<$ o $>$.",
            "Sombrear la zona correspondiente: a la izquierda para $<$ o $\\le$, a la derecha para $>$ o $\\ge$."
        ],
        "ejemplos": [
            {
                "titulo": "Graficar $x \\ge 3$",
                "enunciado": "Representa gráficamente en la recta numérica la solución de $x \\ge 3$.",
                "solucion_pasos": [
                    "Dibujamos la recta numérica.",
                    "Ubicamos el número $3$.",
                    "Como es $\\ge$, marcamos el $3$ con un círculo relleno.",
                    "Sombreamos todos los números a la derecha del $3$."
                ]
            },
            {
                "titulo": "Graficar $x < -1$",
                "enunciado": "Representa gráficamente en la recta numérica la solución de $x < -1$.",
                "solucion_pasos": [
                    "Dibujamos la recta numérica.",
                    "Ubicamos el número $-1$.",
                    "Como es $<$, marcamos el $-1$ con un círculo en blanco (hueco).",
                    "Sombreamos todos los números a la izquierda del $-1$."
                ]
            },
            {
                "titulo": "¿Se sombrea a la derecha?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Para la inecuación $x > 5$.",
                    "Los valores mayores a $5$ se encuentran en la dirección positiva.",
                    "Se sombrea a la derecha de $5$."
                ]
            },
            {
                "titulo": "¿El punto es relleno para $x > 0$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "El símbolo $>$ indica desigualdad estricta.",
                    "El valor límite no está incluido.",
                    "El círculo debe dibujarse en blanco (vacío), no relleno."
                ]
            }
        ],
        "errores_frecuentes": [
            "Dibujar un círculo relleno cuando la desigualdad es estricta.",
            "Dibujar un círculo vacío cuando la desigualdad incluye el signo igual.",
            "Sombrear en sentido contrario (ej. hacia la derecha cuando es $<$ ).",
            "No marcar claramente el límite y hacer que el sombreado empiece en un número entero anterior o posterior.",
            "No incluir una punta de flecha en el área sombreada para indicar que continúa infinitamente."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado",
        "ejercicios": [
            {
                "stable_id": "ALG-GEN-REC-1",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "¿Cómo se indica gráficamente que un extremo numérico no pertenece al conjunto solución?",
                "opciones": [
                    "Con un círculo vacío o hueco sobre el número.",
                    "Con un círculo relleno sobre el número.",
                    "Con un cuadrado relleno.",
                    "No dibujando nada sobre el número."
                ],
                "respuesta_correcta": "Con un círculo vacío o hueco sobre el número.",
                "explicacion": "El círculo vacío indica que ese valor frontera se aproxima pero no se toma, correspondiendo a desigualdades estrictas."
            },
            {
                "stable_id": "ALG-GEN-REC-2",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Si se sombrea la región de la recta numérica que está a la izquierda de un número, ¿qué tipo de inecuación se está representando?",
                "opciones": [
                    "Menor que ($<$) o menor o igual que ($\\le$).",
                    "Mayor que ($>$) o mayor o igual que ($\\ge$).",
                    "Igualdad exacta ($=$).",
                    "Desigualdad diferente ($\\neq$)."
                ],
                "respuesta_correcta": "Menor que ($<$) o menor o igual que ($\\le$).",
                "explicacion": "En la recta numérica, los valores más pequeños que un número de referencia se ubican siempre hacia la izquierda."
            },
            {
                "stable_id": "ALG-GEN-REC-3",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Para la solución $x \\ge 4$, ¿cuál es el procedimiento correcto de graficado?",
                "opciones": [
                    "Círculo relleno en $4$, flecha hacia la derecha.",
                    "Círculo vacío en $4$, flecha hacia la derecha.",
                    "Círculo relleno en $4$, flecha hacia la izquierda.",
                    "Círculo vacío en $4$, flecha hacia la izquierda."
                ],
                "respuesta_correcta": "Círculo relleno en $4$, flecha hacia la derecha.",
                "explicacion": "Al ser $\\ge$, el punto se incluye (círculo relleno). Al ser mayores, los valores están a la derecha."
            },
            {
                "stable_id": "ALG-GEN-REC-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Si ves una gráfica en la recta numérica con un círculo vacío en el $-2$ y una línea sombreada extendiéndose hacia el infinito positivo, ¿cuál es la inecuación que representa?",
                "opciones": [
                    "$x > -2$",
                    "$x \\ge -2$",
                    "$x < -2$",
                    "$x \\le -2$"
                ],
                "respuesta_correcta": "$x > -2$",
                "explicacion": "El círculo vacío es $>$ o $<$. Sombreado a la derecha significa valores mayores, por lo tanto $x > -2$."
            },
            {
                "stable_id": "ALG-GEN-REC-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "Para graficar la solución de $3x \\le 15$, se debe colocar un punto vacío en $5$ y pintar hacia la izquierda.",
                "respuesta_correcta": "False",
                "explicacion": "La solución es $x \\le 5$. Como incluye el signo igual, el punto en $5$ debe ser un círculo relleno, no vacío."
            },
            {
                "stable_id": "ALG-GEN-REC-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "El sombreado en la recta real de $x > 0$ coincide exactamente con todos los números positivos.",
                "respuesta_correcta": "True",
                "explicacion": "Efectivamente, todos los números mayores que cero estrictamente son, por definición, los números reales positivos."
            },
            {
                "stable_id": "ALG-GEN-REC-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "Si la desigualdad es $x < 7$, la gráfica comienza en el número $6$ y va a la izquierda.",
                "respuesta_correcta": "False",
                "explicacion": "La gráfica comienza en $7$ (con un círculo vacío) porque los números decimales como $6.9$ también son soluciones. No se restringe a números enteros."
            },
            {
                "stable_id": "ALG-GEN-REC-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "Resuelve la inecuación $5 - 2x < 11$. ¿Cómo se describe su representación gráfica?",
                "opciones": [
                    "Círculo vacío en $-3$, región sombreada a la derecha.",
                    "Círculo vacío en $-3$, región sombreada a la izquierda.",
                    "Círculo relleno en $-3$, región sombreada a la derecha.",
                    "Círculo relleno en $-3$, región sombreada a la izquierda."
                ],
                "respuesta_correcta": "Círculo vacío en $-3$, región sombreada a la derecha.",
                "explicacion": "Restando $5$: $-2x < 6$. Dividiendo por $-2$ (invierte la desigualdad): $x > -3$. La gráfica requiere círculo vacío (por el $>$ ) en $-3$ y sombrear a la derecha.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-REC-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "Al resolver $\\frac{x}{3} - 1 \\ge \\frac{x}{2} + 2$, la representación gráfica en la recta numérica es:",
                "opciones": [
                    "Círculo relleno en $-18$, flecha hacia la izquierda.",
                    "Círculo vacío en $-18$, flecha hacia la izquierda.",
                    "Círculo relleno en $-18$, flecha hacia la derecha.",
                    "Círculo vacío en $18$, flecha hacia la izquierda."
                ],
                "respuesta_correcta": "Círculo relleno en $-18$, flecha hacia la izquierda.",
                "explicacion": "Multiplicando por $6$: $2x - 6 \\ge 3x + 12$. Restando $3x$: $-x - 6 \\ge 12$. Sumando $6$: $-x \\ge 18$. Multiplicando por $-1$: $x \\le -18$. Esto es círculo relleno en $-18$ hacia la izquierda.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-REC-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "La intersección de las gráficas de $x > -2$ y $x \\le 4$ forma un segmento sobre la recta. ¿Qué características tiene este segmento en sus extremos?",
                "opciones": [
                    "Círculo vacío en $-2$ y círculo relleno en $4$.",
                    "Círculo vacío en $-2$ y círculo vacío en $4$.",
                    "Círculo relleno en $-2$ y círculo relleno en $4$.",
                    "Círculo relleno en $-2$ y círculo vacío en $4$."
                ],
                "respuesta_correcta": "Círculo vacío en $-2$ y círculo relleno en $4$.",
                "explicacion": "El extremo inferior está dado por $x > -2$ (desigualdad estricta, círculo vacío). El extremo superior está dado por $x \\le 4$ (incluye el igual, círculo relleno).",
                "paes_style": True
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.VERIFICACION_SOLUCION": {
        "titulo": "Verificación de soluciones de inecuaciones lineales",
        "objetivo": "Comprobar si un número específico o un conjunto de números pertenece a la solución de una inecuación.",
        "introduccion": "Muchas veces, en lugar de resolver una inecuación desde cero, queremos verificar si un valor particular cumple con las condiciones dadas o revisar si nuestra solución final es correcta.",
        "resumen": "Para verificar, se sustituye la incógnita por el valor numérico en la inecuación original. Si la afirmación matemática resultante es verdadera, el número es una solución; si es falsa, no lo es.",
        "explicacion": "### Definición formal\n\nUn número real $x_0$ se considera solución de una inecuación si, al sustituir $x$ por $x_0$, la proposición matemática obtenida tiene un valor de verdad verdadero.\n\n### Desarrollo didáctico\n\nEl proceso de comprobación requiere reemplazar sistemáticamente todas las apariciones de la variable por el valor candidato, cuidando el uso de paréntesis al sustituir números negativos. Luego, se respetan las reglas de jerarquía de operaciones (multiplicaciones antes que sumas o restas) para evaluar ambos lados de la desigualdad. Finalmente, se examina la desigualdad numérica resultante. Este método es útil en exámenes de selección múltiple y para autoevaluar las propias resoluciones.",
        "procedimiento": [
            "Elegir el valor numérico que se desea comprobar.",
            "Reemplazar cada variable de la inecuación original por dicho valor.",
            "Resolver las operaciones aritméticas en cada miembro de la desigualdad.",
            "Evaluar si la desigualdad numérica obtenida es verdadera o falsa."
        ],
        "ejemplos": [
            {
                "titulo": "Verificación para $x=2$",
                "enunciado": "Verifica si $x=2$ es solución de $3x - 1 < 8$.",
                "solucion_pasos": [
                    "Sustituimos $x$ por $2$: $3(2) - 1 < 8$.",
                    "Multiplicamos: $6 - 1 < 8$.",
                    "Restamos: $5 < 8$.",
                    "Como $5$ es menor que $8$, la proposición es verdadera y $x=2$ es solución."
                ]
            },
            {
                "titulo": "Comprobación de valor frontera",
                "enunciado": "Verifica si $x=-3$ es solución de $4x + 5 \\ge -7$.",
                "solucion_pasos": [
                    "Sustituimos $x$ por $-3$: $4(-3) + 5 \\ge -7$.",
                    "Multiplicamos: $-12 + 5 \\ge -7$.",
                    "Sumamos: $-7 \\ge -7$.",
                    "Como $-7$ es igual a $-7$, cumple la condición \"mayor o igual\". Es verdadero."
                ]
            },
            {
                "titulo": "¿Es el número solución?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Evaluamos si $x=5$ soluciona $2x > 9$.",
                    "Reemplazamos: $2(5) > 9$.",
                    "Calculamos: $10 > 9$.",
                    "Como es verdadero, el número sí es solución."
                ]
            },
            {
                "titulo": "¿El valor satisface la inecuación?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Evaluamos $x=1$ en $5x + 2 < 7$.",
                    "Reemplazamos: $5(1) + 2 < 7$.",
                    "Calculamos: $7 < 7$.",
                    "Como un número no es menor que sí mismo estrictamente, la proposición es falsa."
                ]
            }
        ],
        "errores_frecuentes": [
            "Cometer errores de signo al evaluar (ej. $3(-2) = 6$).",
            "Olvidar que en una desigualdad $\\ge$ o $\\le$, la igualdad hace que la afirmación sea verdadera.",
            "Considerar que $a < a$ es verdadero.",
            "Resolver mal la prioridad de las operaciones (ej. restar antes de multiplicar).",
            "Evaluar el número en una versión simplificada de la inecuación, lo cual puede arrastrar errores de resolución previa."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado",
        "ejercicios": [
            {
                "stable_id": "ALG-GEN-VER-1",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Al evaluar $x=3$ en una inecuación se llega a la expresión $15 \\ge 15$. ¿Qué se concluye de esto?",
                "opciones": [
                    "Que $x=3$ es solución.",
                    "Que $x=3$ no es solución.",
                    "Que hay un error en la evaluación.",
                    "Que la inecuación no tiene solución."
                ],
                "respuesta_correcta": "Que $x=3$ es solución.",
                "explicacion": "El signo $\\ge$ significa \"mayor o igual\". Como $15$ es igual a $15$, la condición se cumple y es verdadera."
            },
            {
                "stable_id": "ALG-GEN-VER-2",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "¿Por qué se recomienda verificar las soluciones en la inecuación original en vez de en las inecuaciones intermedias resultantes del despeje?",
                "opciones": [
                    "Porque las inecuaciones intermedias son siempre más largas.",
                    "Porque si hubo un error en los pasos algebraicos, la inecuación intermedia no será equivalente a la original.",
                    "Porque es más fácil calcular en la original.",
                    "Porque las inecuaciones intermedias no aceptan números negativos."
                ],
                "respuesta_correcta": "Porque si hubo un error en los pasos algebraicos, la inecuación intermedia no será equivalente a la original.",
                "explicacion": "Si te equivocaste al despejar y usas la versión despejada para evaluar, podrías creer erróneamente que la solución es correcta."
            },
            {
                "stable_id": "ALG-GEN-VER-3",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Si al comprobar un número se obtiene $-4 < -2$, la conclusión es:",
                "opciones": [
                    "Falsa, porque $-4$ es mayor numéricamente hablando.",
                    "Verdadera, porque $-4$ está a la izquierda de $-2$ en la recta numérica.",
                    "Falsa, los negativos nunca cumplen desigualdades.",
                    "Inconclusa."
                ],
                "respuesta_correcta": "Verdadera, porque $-4$ está a la izquierda de $-2$ en la recta numérica.",
                "explicacion": "Entre dos números negativos, es menor el que tiene mayor valor absoluto, es decir, el que está más lejos del cero."
            },
            {
                "stable_id": "ALG-GEN-VER-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "¿Cuál de los siguientes valores es solución de $2x + 1 < 7$?",
                "opciones": [
                    "$3$",
                    "$4$",
                    "$5$",
                    "$2$"
                ],
                "respuesta_correcta": "$2$",
                "explicacion": "Evaluamos $x=2$: $2(2) + 1 = 5$, y $5 < 7$ es verdadero. Con $x=3$: $7 < 7$ es falso."
            },
            {
                "stable_id": "ALG-GEN-VER-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "El número $x = -1$ es solución de la inecuación $5x - 3 > x - 7$.",
                "respuesta_correcta": "False",
                "explicacion": "Evaluamos el lado izquierdo: $5(-1) - 3 = -8$. Evaluamos el derecho: $-1 - 7 = -8$. Resulta $-8 > -8$, lo cual es falso."
            },
            {
                "stable_id": "ALG-GEN-VER-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "El valor $x = 0$ satisface siempre cualquier inecuación de la forma $ax < b$ si $b$ es un número positivo.",
                "respuesta_correcta": "True",
                "explicacion": "Si $x=0$, $a(0) < b$ resulta en $0 < b$. Si $b$ es positivo, la afirmación $0 < b$ es siempre verdadera."
            },
            {
                "stable_id": "ALG-GEN-VER-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "Al sustituir $x = 5$ en $4(x - 2) \\le 12$, la desigualdad no se cumple.",
                "respuesta_correcta": "False",
                "explicacion": "Evaluamos: $4(5 - 2) = 4(3) = 12$. La condición $12 \\le 12$ es verdadera, por lo tanto la desigualdad sí se cumple."
            },
            {
                "stable_id": "ALG-GEN-VER-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "¿Cuántos de los siguientes valores: $\\{-3, 0, 2, 4\\}$ son soluciones de la inecuación $x^2 - 2x < 5$?",
                "opciones": [
                    "$1$",
                    "$2$",
                    "$3$",
                    "$4$"
                ],
                "respuesta_correcta": "$2$",
                "explicacion": "Evaluamos $-3$: $9 - (-6) = 15 < 5$ (F). Evaluamos $0$: $0 - 0 = 0 < 5$ (V). Evaluamos $2$: $4 - 4 = 0 < 5$ (V). Evaluamos $4$: $16 - 8 = 8 < 5$ (F). Solo $0$ y $2$ son soluciones.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-VER-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "Si se sabe que $x = m$ es una solución de $3x + k > 10$, y $k = 4$. ¿Cuál de los siguientes podría ser el valor de $m$?",
                "opciones": [
                    "$1$",
                    "$2$",
                    "$3$",
                    "$0$"
                ],
                "respuesta_correcta": "$3$",
                "explicacion": "Reemplazamos $k=4$: $3x + 4 > 10$. Evaluamos las opciones. Con $x=3$: $3(3) + 4 = 13 > 10$ (V). Las demás dan resultados menores o iguales a $10$.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-VER-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "Dada la inecuación fraccionaria $\\frac{x+1}{2} - \\frac{x-2}{3} \\ge 1$. ¿Cuál de los siguientes conjuntos de valores cumple íntegramente la inecuación?",
                "opciones": [
                    "$\\{-2, -3\\}$",
                    "$\\{-3, 0\\}$",
                    "$\\{-1, 1\\}$",
                    "$\\{-5, -3\\}$"
                ],
                "respuesta_correcta": "$\\{-1, 1\\}$",
                "explicacion": "Resolvemos multiplicando por $6$: $3(x+1) - 2(x-2) \\ge 6 \\Rightarrow 3x + 3 - 2x + 4 \\ge 6 \\Rightarrow x + 7 \\ge 6 \\Rightarrow x \\ge -1$. El único conjunto donde ambos valores son $\\ge -1$ es $\\{-1, 1\\}$.",
                "paes_style": True
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.INECUACION_SIN_SOLUCION": {
        "titulo": "Inecuaciones lineales sin solución",
        "objetivo": "Identificar inecuaciones lineales cuyo conjunto solución es el conjunto vacío.",
        "introduccion": "En algunas ocasiones, al simplificar algebraicamente una inecuación, todas las incógnitas se anulan y obtenemos una afirmación matemática que es totalmente falsa.",
        "resumen": "Cuando la resolución de una inecuación conduce a un absurdo matemático, significa que no existe ningún número real que cumpla las condiciones iniciales. En este caso, decimos que no tiene solución.",
        "explicacion": "### Definición formal\n\nUna inecuación no tiene solución si el conjunto solución es el conjunto vacío ($\\emptyset$). Algebraicamente, esto ocurre cuando al reducir términos semejantes se llega a una proposición de la forma $c < d$, donde $c$ y $d$ son constantes y la proposición es falsa (por ejemplo, $3 < -1$).\n\n### Desarrollo didáctico\n\nAl resolver paso a paso, si la variable $x$ desaparece de ambos miembros (por ejemplo, restamos $2x$ y resulta que ambos lados tenían exactamente $2x$), solo nos quedarán números. Debemos evaluar la desigualdad restante. Si la frase es mentira (como afirmar que $5 \\le 2$ o $0 > 0$), concluimos que el problema no tiene respuesta en los números reales.",
        "procedimiento": [
            "Resolver la inecuación usando los métodos habituales de agrupación y despeje.",
            "Observar que los términos que contienen la variable se cancelan completamente a ambos lados.",
            "Analizar la desigualdad numérica resultante (sin incógnitas).",
            "Si la desigualdad es falsa, declarar que la inecuación no tiene solución ($\\emptyset$)."
        ],
        "ejemplos": [
            {
                "titulo": "Resolución de inecuación absurda",
                "enunciado": "Resuelve la inecuación $2x + 5 > 2x + 9$.",
                "solucion_pasos": [
                    "Intentamos agrupar las $x$ restando $2x$ a ambos lados: $2x - 2x + 5 > 9$.",
                    "Simplificamos: $5 > 9$.",
                    "La afirmación $5 > 9$ es falsa.",
                    "Concluimos que la inecuación no tiene solución."
                ]
            },
            {
                "titulo": "Uso de distributiva sin solución",
                "enunciado": "Resuelve $3(x - 1) \\le 3x - 8$.",
                "solucion_pasos": [
                    "Aplicamos propiedad distributiva: $3x - 3 \\le 3x - 8$.",
                    "Restamos $3x$ de ambos lados: $-3 \\le -8$.",
                    "La proposición $-3 \\le -8$ es falsa ($-3$ es mayor).",
                    "Por lo tanto, la inecuación carece de solución."
                ]
            },
            {
                "titulo": "¿Tiene solución esta desigualdad?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Revisamos $x < x$.",
                    "Restamos $x$ a ambos lados: $0 < 0$.",
                    "Como $0$ no es estrictamente menor que $0$, es falso.",
                    "No hay solución."
                ]
            },
            {
                "titulo": "¿Se cumple para algún valor real?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Dada $4x + 10 < 4x + 2$.",
                    "Restando $4x$ nos queda $10 < 2$.",
                    "Falso, por tanto el conjunto solución es vacío."
                ]
            }
        ],
        "errores_frecuentes": [
            "Forzar que la variable no se elimine cometiendo errores de suma o resta.",
            "Responder $x = \\emptyset$ en lugar de $Sol = \\emptyset$, confundiendo la incógnita con el conjunto.",
            "Pensar que $0 < 0$ es verdadero.",
            "Creer que llegar a una contradicción significa que la solución es cero.",
            "No saber interpretar qué significa llegar a $0 > 5$ y abandonar el ejercicio."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado",
        "ejercicios": [
            {
                "stable_id": "ALG-GEN-NSS-1",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "¿Qué indica algebraicamente que una inecuación lineal NO tiene solución en los números reales?",
                "opciones": [
                    "Al despejar, la variable se elimina y queda una proposición falsa.",
                    "Al despejar, se obtiene $x = 0$.",
                    "Al despejar, la variable se elimina y queda una proposición verdadera.",
                    "La inecuación contiene fracciones."
                ],
                "respuesta_correcta": "Al despejar, la variable se elimina y queda una proposición falsa.",
                "explicacion": "Llegar a un absurdo numérico (como $1 > 5$) prueba que no existe ningún valor que permita cumplir la desigualdad."
            },
            {
                "stable_id": "ALG-GEN-NSS-2",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "¿Cómo se denota matemáticamente que el conjunto solución no tiene elementos?",
                "opciones": [
                    "$\\emptyset$ o $\\{\\}$",
                    "$0$",
                    "$\\infty$",
                    "$\\{0\\}$"
                ],
                "respuesta_correcta": "$\\emptyset$ o $\\{\\}$",
                "explicacion": "El símbolo $\\emptyset$ o las llaves vacías representan el conjunto vacío, que no contiene elementos."
            },
            {
                "stable_id": "ALG-GEN-NSS-3",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Si al resolver llegas a la expresión $7 < 2$, ¿qué puedes afirmar?",
                "opciones": [
                    "Que no tiene solución.",
                    "Que la solución son todos los números reales.",
                    "Que $x = 0$.",
                    "Que debes cambiar el sentido de la desigualdad."
                ],
                "respuesta_correcta": "Que no tiene solución.",
                "explicacion": "Al ser $7 < 2$ una afirmación siempre falsa, concluyes inmediatamente que el problema original no tiene solución posible."
            },
            {
                "stable_id": "ALG-GEN-NSS-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "¿Cuál de las siguientes inecuaciones no tiene solución?",
                "opciones": [
                    "$x + 1 > x + 2$",
                    "$x + 2 > x + 1$",
                    "$2x > x + 1$",
                    "$x - 1 < x + 5$"
                ],
                "respuesta_correcta": "$x + 1 > x + 2$",
                "explicacion": "Restando $x$, se obtiene $1 > 2$, lo cual es falso, demostrando que no hay solución."
            },
            {
                "stable_id": "ALG-GEN-NSS-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "La inecuación $5x - 5x \\ge 10$ no tiene solución.",
                "respuesta_correcta": "True",
                "explicacion": "Se simplifica a $0 \\ge 10$, lo cual es una contradicción. Por lo tanto, el conjunto solución es vacío."
            },
            {
                "stable_id": "ALG-GEN-NSS-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "La desigualdad $3x < 3x$ tiene como solución a $x=0$.",
                "respuesta_correcta": "False",
                "explicacion": "Si restamos $3x$, queda $0 < 0$, que es falso. No tiene solución, ni siquiera el cero."
            },
            {
                "stable_id": "ALG-GEN-NSS-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "Si resuelves $2(x+1) < 2x + 1$ obtienes $2 < 1$, concluyendo que no hay solución.",
                "respuesta_correcta": "True",
                "explicacion": "Expandiendo: $2x + 2 < 2x + 1$. Restando $2x$ a ambos lados: $2 < 1$. Esto es falso, lo que está correcto para afirmar que no hay solución."
            },
            {
                "stable_id": "ALG-GEN-NSS-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "Dada la inecuación $\\frac{4x - 8}{2} > 2x + 5$, ¿cuál es su conjunto solución?",
                "opciones": [
                    "$\\emptyset$",
                    "$\\mathbb{R}$",
                    "$(-\\infty, 0)$",
                    "$(0, +\\infty)$"
                ],
                "respuesta_correcta": "$\\emptyset$",
                "explicacion": "Simplificando la fracción: $2x - 4 > 2x + 5$. Restando $2x$: $-4 > 5$. Es falso. El conjunto solución es el vacío.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-NSS-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "¿Para qué valor de $k$ la inecuación $kx - 3 \\le 5x - 7$ carece de solución?",
                "opciones": [
                    "$5$",
                    "$-5$",
                    "$3$",
                    "$7$"
                ],
                "respuesta_correcta": "$5$",
                "explicacion": "Agrupamos las $x$: $(k-5)x \\le -4$. Para que no tenga solución, el término de $x$ debe eliminarse y dejar un absurdo. Si $k=5$, nos queda $0 \\le -4$, lo que es falso. Entonces para $k=5$ no tiene solución.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-NSS-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "Si resuelves el sistema de inecuaciones $x + 2 < 5$ y $x - 1 > 3$, el conjunto solución es:",
                "opciones": [
                    "$\\emptyset$",
                    "$(3, 4)$",
                    "$\\mathbb{R}$",
                    "$(4, 5)$"
                ],
                "respuesta_correcta": "$\\emptyset$",
                "explicacion": "Primera: $x < 3$. Segunda: $x > 4$. No hay ningún número que sea menor a $3$ y al mismo tiempo mayor a $4$. La intersección es el conjunto vacío.",
                "paes_style": True
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.INECUACION_TODO_REAL": {
        "titulo": "Inecuaciones lineales válidas para todos los reales",
        "objetivo": "Identificar inecuaciones lineales cuyo conjunto solución abarca a todos los números reales.",
        "introduccion": "Así como hay inecuaciones imposibles, existen otras que representan verdades absolutas matemáticas, donde sin importar qué número elijas, la desigualdad siempre se cumple.",
        "resumen": "Cuando al resolver una inecuación las incógnitas se anulan y se obtiene una desigualdad numéricamente verdadera en todos los casos, se concluye que la solución son todos los números reales.",
        "explicacion": "### Definición formal\n\nUna inecuación es válida para todos los reales si su conjunto solución es $\\mathbb{R}$. Esto sucede cuando su simplificación algebraica conduce a una desigualdad constante que es lógicamente verdadera (ejemplo: $1 < 5$).\n\n### Desarrollo didáctico\n\nAl igual que en las inecuaciones sin solución, la variable se elimina por completo de la expresión. La gran diferencia radica en evaluar el resultado numérico que sobrevive. Si nos enfrentamos a algo indiscutiblemente cierto (como $0 \\le 4$ o $-3 < 2$), eso prueba que cualquier valor introducido originalmente no habría alterado el hecho de que esa afirmación es correcta. Así, la respuesta es $\\mathbb{R}$ o el intervalo $(-\\infty, +\\infty)$.",
        "procedimiento": [
            "Reducir la inecuación agrupando y despejando.",
            "Si la variable se cancela, examinar los valores numéricos constantes que restan en ambos lados.",
            "Evaluar el valor de verdad de la desigualdad.",
            "Si la desigualdad es verdadera, declarar como solución el conjunto de todos los números reales ($\\mathbb{R}$)."
        ],
        "ejemplos": [
            {
                "titulo": "Resolución de inecuación tautológica",
                "enunciado": "Resuelve la inecuación $3x - 2 < 3x + 4$.",
                "solucion_pasos": [
                    "Restamos $3x$ a ambos lados: $3x - 3x - 2 < 4$.",
                    "Simplificamos: $-2 < 4$.",
                    "La afirmación $-2 < 4$ es lógicamente verdadera.",
                    "La solución son todos los reales, $Sol = \\mathbb{R}$."
                ]
            },
            {
                "titulo": "Distributiva que es siempre verdadera",
                "enunciado": "Resuelve $2(x + 5) \\ge 2x + 10$.",
                "solucion_pasos": [
                    "Aplicamos distributiva: $2x + 10 \\ge 2x + 10$.",
                    "Restamos $2x$: $10 \\ge 10$.",
                    "La proposición $10 \\ge 10$ es verdadera.",
                    "La solución es $\\mathbb{R}$."
                ]
            },
            {
                "titulo": "¿Son todos los reales solución?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Verificamos $x < x + 1$.",
                    "Restamos $x$ a ambos lados: $0 < 1$.",
                    "Es verdadero, por tanto, todos los números son solución."
                ]
            },
            {
                "titulo": "¿La desigualdad tiene solución para todo real?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Evaluamos $5x > 5x$.",
                    "Restando nos queda $0 > 0$.",
                    "Esta proposición es falsa, por lo tanto no tiene solución (no es $\\mathbb{R}$)."
                ]
            }
        ],
        "errores_frecuentes": [
            "Creer que si la variable desaparece, automáticamente significa que no hay solución, sin evaluar la verdad lógica.",
            "Responder erróneamente $x = \\mathbb{R}$ en lugar de $Sol = \\mathbb{R}$.",
            "Considerar que si queda $0 < 0$ la solución es todo $\\mathbb{R}$.",
            "Creer que al llegar a $5 \\ge 5$, solo $5$ es solución.",
            "No saber escribir la solución como intervalo $(-\\infty, +\\infty)$."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado",
        "ejercicios": [
            {
                "stable_id": "ALG-GEN-TOD-1",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Al resolver una inecuación lineal se llega al resultado $4 \\ge -1$. ¿Qué se debe concluir sobre la solución?",
                "opciones": [
                    "Que cualquier número real cumple la inecuación.",
                    "Que no existe ningún número que cumpla la inecuación.",
                    "Que la solución es $4$.",
                    "Que solo los números positivos son solución."
                ],
                "respuesta_correcta": "Que cualquier número real cumple la inecuación.",
                "explicacion": "Como $4 \\ge -1$ es una verdad universal e inalterable, la inecuación original se cumple para cualquier valor de la incógnita."
            },
            {
                "stable_id": "ALG-GEN-TOD-2",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "¿Qué notación de intervalo representa que todos los números reales son solución?",
                "opciones": [
                    "$(-\\infty, +\\infty)$",
                    "$[0, +\\infty)$",
                    "$(-\\infty, 0]$",
                    "$\\emptyset$"
                ],
                "respuesta_correcta": "$(-\\infty, +\\infty)$",
                "explicacion": "El intervalo que abarca desde menos infinito a más infinito representa al conjunto completo de los números reales."
            },
            {
                "stable_id": "ALG-GEN-TOD-3",
                "tipo": "conceptual",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "Si llegas a una expresión verdadera como $0 \\le 0$, tu gráfica en la recta numérica sería:",
                "opciones": [
                    "Toda la recta sombreada, sin puntos vacíos.",
                    "La recta completamente vacía sin sombrear.",
                    "Solo un punto relleno en el cero.",
                    "Sombreada solo hacia la derecha del cero."
                ],
                "respuesta_correcta": "Toda la recta sombreada, sin puntos vacíos.",
                "explicacion": "Como todos los números satisfacen la condición, la representación abarca la totalidad de la recta."
            },
            {
                "stable_id": "ALG-GEN-TOD-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "modalidad": "multiple_choice",
                "enunciado": "¿Cuál de las siguientes inecuaciones tiene como solución a todos los números reales?",
                "opciones": [
                    "$x + 2 < x + 5$",
                    "$x + 5 < x + 2$",
                    "$2x > x$",
                    "$x < x$"
                ],
                "respuesta_correcta": "$x + 2 < x + 5$",
                "explicacion": "Al restar $x$ en la primera, nos queda $2 < 5$, que es verdadero siempre."
            },
            {
                "stable_id": "ALG-GEN-TOD-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "La inecuación $7x - 1 \\le 7x + 2$ es válida para todos los reales.",
                "respuesta_correcta": "True",
                "explicacion": "Restando $7x$ obtenemos $-1 \\le 2$, lo cual es verdadero, así que la solución es todo $\\mathbb{R}$."
            },
            {
                "stable_id": "ALG-GEN-TOD-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "El conjunto solución de $-2x > -2x + 1$ son los números reales.",
                "respuesta_correcta": "False",
                "explicacion": "Restando $-2x$, queda $0 > 1$, que es falso. En realidad, no tiene solución."
            },
            {
                "stable_id": "ALG-GEN-TOD-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "modalidad": "true_false",
                "enunciado": "La expresión $3(x - 2) < 3x$ es verdadera siempre.",
                "respuesta_correcta": "True",
                "explicacion": "Multiplicando: $3x - 6 < 3x$. Restando $3x$: $-6 < 0$, lo cual es una proposición siempre verdadera."
            },
            {
                "stable_id": "ALG-GEN-TOD-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "Considera la inecuación fraccionaria $\\frac{x}{2} + 1 > \\frac{x - 4}{2}$. ¿Cuál es su conjunto solución?",
                "opciones": [
                    "$\\mathbb{R}$",
                    "$\\emptyset$",
                    "$(0, +\\infty)$",
                    "$(-\\infty, 4)$"
                ],
                "respuesta_correcta": "$\\mathbb{R}$",
                "explicacion": "Multiplicando por $2$: $x + 2 > x - 4$. Restando $x$: $2 > -4$, proposición verdadera para todo número real.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-TOD-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "¿Para qué valor de $p$ la inecuación $px - 5 < 2x - 3$ se cumple para todo $x \\in \\mathbb{R}$?",
                "opciones": [
                    "$2$",
                    "$-2$",
                    "$5$",
                    "$3$"
                ],
                "respuesta_correcta": "$2$",
                "explicacion": "Para que sea para todo real, las $x$ deben anularse, esto es $p = 2$. Así queda $2x - 5 < 2x - 3 \\Rightarrow -5 < -3$, lo cual es verdad siempre.",
                "paes_style": True
            },
            {
                "stable_id": "ALG-GEN-TOD-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "modalidad": "multiple_choice",
                "enunciado": "¿Cuál es el conjunto solución de $x^2 - x^2 + 3 \\le 5$?",
                "opciones": [
                    "$\\mathbb{R}$",
                    "$\\emptyset$",
                    "$(2, +\\infty)$",
                    "$(0, +\\infty)$"
                ],
                "respuesta_correcta": "$\\mathbb{R}$",
                "explicacion": "El término cuadrático $x^2 - x^2$ se anula dando $0$. La expresión se reduce a $3 \\le 5$, lo que es verdad universalmente. Por ende el conjunto solución es todos los reales.",
                "paes_style": True
            }
        ]
    }
}

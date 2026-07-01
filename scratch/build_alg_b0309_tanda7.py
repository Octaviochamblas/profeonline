topics = {
    "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO": {
        "titulo": "Inecuaciones con valor absoluto: Conceptos generales",
        "objetivo": "Comprender la estructura y los fundamentos matemáticos de las inecuaciones que involucran valor absoluto, reconociendo la distancia entre elementos en la recta real.",
        "introduccion": "El valor absoluto de una expresión matemática representa su distancia al origen en la recta real. Al trabajar con inecuaciones que contienen valor absoluto, se modelan conjuntos de números cuyas distancias cumplen ciertas condiciones de orden, lo que permite resolver problemas donde las variaciones o márgenes de error son limitados.",
        "resumen": "Una inecuación con valor absoluto es una desigualdad de la forma $|A(x)| < b$, $|A(x)| > b$, $|A(x)| \\leq b$ o $|A(x)| \\geq b$, donde $A(x)$ es una expresión algebraica y $b$ es un número real.",
        "explicacion": "### Definición formal\nUna inecuación con valor absoluto en la variable $x$ es una desigualdad que contiene el valor absoluto de una expresión algebraica en $x$. Se clasifica según el signo de desigualdad y el valor de la constante con la cual se compara. Sus conjuntos solución se determinan aplicando las propiedades de orden del valor absoluto.\n\n### Desarrollo didáctico\nPara comprender estas inecuaciones, es esencial recordar que el valor absoluto $|x|$ indica la distancia desde $x$ hasta el cero. Por ende, la inecuación $|x| < a$ (con $a > 0$) busca todos los puntos cuya distancia al cero es estrictamente menor que $a$, formando el intervalo abierto $(-a, a)$. Análogamente, $|x| > a$ busca los puntos cuya distancia al cero es estrictamente mayor que $a$, lo que corresponde a la unión de intervalos $(-\\infty, -a) \\cup (a, \\infty)$. Las expresiones más complejas, como $|A(x)|$, se analizan con los mismos principios.",
        "procedimiento": [
            "Identificar el tipo de desigualdad involucrada ($<$, $>$, $\\leq$, $\\geq$).",
            "Aislar la expresión con valor absoluto en un lado de la inecuación, si es necesario.",
            "Analizar el signo de la constante con la cual se compara el valor absoluto.",
            "Aplicar la propiedad correspondiente al tipo de desigualdad para reescribir la inecuación como un sistema de inecuaciones lineales o cuadráticas sin valor absoluto.",
            "Resolver las inecuaciones resultantes y combinar las soluciones mediante intersección o unión, según corresponda."
        ],
        "ejemplos": [
            {
                "titulo": "Distancia a una referencia",
                "enunciado": "La temperatura en un reactor debe mantenerse a $50^\\circ$C con un margen de tolerancia estrictamente menor a $3^\\circ$C. Si $T$ representa la temperatura en grados Celsius, exprese esta condición mediante una inecuación y determine el conjunto solución.",
                "solucion_pasos": [
                    "La diferencia entre la temperatura $T$ y la referencia $50$ es $T - 50$.",
                    "El margen de tolerancia implica que el valor absoluto de esta diferencia debe ser menor que $3$: $|T - 50| < 3$.",
                    "Por la propiedad del valor absoluto, esto es equivalente a $-3 < T - 50 < 3$.",
                    "Sumando $50$ a cada término: $-3 + 50 < T < 3 + 50$.",
                    "El conjunto solución es $47 < T < 53$."
                ]
            },
            {
                "titulo": "Intervalos de exclusión",
                "enunciado": "Un sistema de seguridad activa su alarma si la presión $P$ en bares de una caldera difiere de $100$ bares en $5$ bares o más. Determine el conjunto de valores de $P$ que activan la alarma.",
                "solucion_pasos": [
                    "La diferencia de la presión respecto al valor nominal es $P - 100$.",
                    "La condición de activación es que la magnitud de esta diferencia sea igual o superior a $5$: $|P - 100| \\geq 5$.",
                    "Esto se descompone en dos inecuaciones: $P - 100 \\leq -5$ o $P - 100 \\geq 5$.",
                    "Resolviendo cada una: $P \\leq 95$ o $P \\geq 105$.",
                    "El conjunto de valores es $P \\in (-\\infty, 95] \\cup [105, \\infty)$."
                ]
            },
            {
                "titulo": "¿Es $|x+2| < 5$ equivalente a $-3 < x < 3$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Se aplica la propiedad del valor absoluto: $-5 < x + 2 < 5$.",
                    "Se resta $2$ a toda la expresión: $-5 - 2 < x < 5 - 2$.",
                    "El resultado correcto es $-7 < x < 3$."
                ]
            },
            {
                "titulo": "¿El conjunto solución de $|x| \\geq -2$ es $\\mathbb{R}$?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "El valor absoluto de cualquier número real siempre es mayor o igual a cero, es decir, $|x| \\geq 0$.",
                    "Como $0 > -2$, se deduce por transitividad que $|x| \\geq -2$ para todo $x$ en los números reales.",
                    "Por lo tanto, la inecuación es válida para cualquier número real."
                ]
            }
        ],
        "errores_frecuentes": [
            "Asumir que $|x-a| < b$ es equivalente a $x-a < b$ e ignorar el caso negativo.",
            "Creer que una inecuación como $|x| > -5$ no tiene solución.",
            "Resolver $|x| > a$ como $-a < x < a$.",
            "Considerar que $|x+y| < a$ implica $|x| + |y| < a$ como paso de resolución.",
            "Tratar a $|x| \\leq 0$ como una inecuación sin solución en lugar de la ecuación $x = 0$."
        ],
        "ejercicios": [
            {
                "stable_id": "ALG-GEN-INEVA-1",
                "nivel": 1,
                "tipo_ejercicio": "multiple_choice",
                "subtipo": "conceptual",
                "enunciado": "Geométricamente, ¿qué representa la inecuación $|x - a| \\leq b$ (con $b > 0$) en la recta real?",
                "opciones": [
                    "El conjunto de puntos cuya distancia al origen es menor o igual a $b$.",
                    "El conjunto de puntos cuya distancia a $a$ es exactamente $b$.",
                    "El conjunto de puntos cuya distancia a $a$ es menor o igual a $b$.",
                    "El conjunto de puntos cuya distancia a $b$ es menor o igual a $a$."
                ],
                "respuesta_correcta": "El conjunto de puntos cuya distancia a $a$ es menor o igual a $b$.",
                "explicacion": "La expresión $|x - a|$ representa la distancia entre $x$ y $a$ en la recta real. Que sea menor o igual a $b$ significa que la distancia máxima permitida entre los puntos y el centro $a$ es $b$."
            },
            {
                "stable_id": "ALG-GEN-INEVA-2",
                "nivel": 1,
                "tipo_ejercicio": "multiple_choice",
                "subtipo": "conceptual",
                "enunciado": "Si $c < 0$, ¿cuál es el conjunto solución de la inecuación $|x| < c$?",
                "opciones": [
                    "Los números reales negativos.",
                    "El conjunto vacío.",
                    "Todos los números reales.",
                    "El intervalo $(-c, c)$."
                ],
                "respuesta_correcta": "El conjunto vacío.",
                "explicacion": "El valor absoluto de cualquier número real es mayor o igual a cero. Un número no negativo no puede ser estrictamente menor que un número negativo $c$, por lo que no existen soluciones."
            },
            {
                "stable_id": "ALG-GEN-INEVA-3",
                "nivel": 1,
                "tipo_ejercicio": "multiple_choice",
                "subtipo": "conceptual",
                "enunciado": "Para la inecuación $|x - 3| > 4$, ¿cuál de las siguientes afirmaciones es correcta?",
                "opciones": [
                    "El conjunto solución es un único intervalo continuo.",
                    "El conjunto solución consiste en dos intervalos disjuntos.",
                    "El punto $x = 3$ es parte de la solución.",
                    "El conjunto solución está acotado superiormente."
                ],
                "respuesta_correcta": "El conjunto solución consiste en dos intervalos disjuntos.",
                "explicacion": "La inecuación se divide en $x - 3 > 4$ o $x - 3 < -4$, lo que da como resultado $x > 7$ o $x < -1$. Esto corresponde a los intervalos $(-\\infty, -1)$ y $(7, \\infty)$, que son disjuntos."
            },
            {
                "stable_id": "ALG-GEN-INEVA-4",
                "nivel": 1,
                "tipo_ejercicio": "multiple_choice",
                "subtipo": "reconocimiento",
                "enunciado": "¿Qué inecuación se representa por la unión de intervalos $(-\\infty, -5] \\cup [5, \\infty)$?",
                "opciones": [
                    "$|x| \\leq 5$",
                    "$|x| \\geq 5$",
                    "$|x| < 5$",
                    "$|x| > 5$"
                ],
                "respuesta_correcta": "$|x| \\geq 5$",
                "explicacion": "El conjunto indica valores menores o iguales a $-5$ y mayores o iguales a $5$. Esto corresponde a que la distancia de $x$ al origen sea mayor o igual a $5$, es decir, $|x| \\geq 5$."
            },
            {
                "stable_id": "ALG-GEN-INEVA-5",
                "nivel": 2,
                "tipo_ejercicio": "true_false",
                "subtipo": "procedimiento_basico",
                "enunciado": "La inecuación $|2x| \\leq 0$ tiene por único conjunto solución a $x = 0$.",
                "respuesta_correcta": "True",
                "explicacion": "Como el valor absoluto no puede ser negativo, la única forma de que $|2x| \\leq 0$ sea verdadero es que $|2x| = 0$, lo que implica $2x = 0$, resultando en $x = 0$."
            },
            {
                "stable_id": "ALG-GEN-INEVA-6",
                "nivel": 2,
                "tipo_ejercicio": "true_false",
                "subtipo": "procedimiento_basico",
                "enunciado": "Al resolver $|x - 1| > 2$, se obtiene como solución $-1 < x < 3$.",
                "respuesta_correcta": "False",
                "explicacion": "La inecuación se separa en $x - 1 < -2 \\cup x - 1 > 2$, lo que resulta en $x < -1 \\cup x > 3$. El intervalo planteado corresponde a $|x - 1| < 2$."
            },
            {
                "stable_id": "ALG-GEN-INEVA-7",
                "nivel": 2,
                "tipo_ejercicio": "true_false",
                "subtipo": "procedimiento_basico",
                "enunciado": "La desigualdad $|-x| < 4$ es equivalente a la desigualdad $|x| < 4$.",
                "respuesta_correcta": "True",
                "explicacion": "Por propiedad del valor absoluto, se cumple que $|-x| = |x|$ para todo $x$ real, por lo tanto, ambas inecuaciones son idénticas y tienen la misma solución."
            },
            {
                "stable_id": "ALG-GEN-INEVA-8",
                "nivel": 3,
                "tipo_ejercicio": "multiple_choice",
                "subtipo": "tipo_paes",
                "enunciado": "Se requiere diseñar una pieza metálica de longitud $L$ cm, la cual debe cumplir que su diferencia con la medida estándar de $12$ cm no exceda los $0.2$ cm en valor absoluto. ¿Cuál es la inecuación que modela esta situación y el rango de medidas aceptables?",
                "opciones": [
                    "$|L - 12| \\leq 0.2$ ; $11.8 \\leq L \\leq 12.2$",
                    "$|L - 12| < 0.2$ ; $11.8 < L < 12.2$",
                    "$|L - 0.2| \\leq 12$ ; $-11.8 \\leq L \\leq 12.2$",
                    "$|L - 12| \\geq 0.2$ ; $L \\leq 11.8$ o $L \\geq 12.2$"
                ],
                "respuesta_correcta": "$|L - 12| \\leq 0.2$ ; $11.8 \\leq L \\leq 12.2$",
                "explicacion": "Que la diferencia no exceda implica que es menor o igual ($\\leq$). Así, $|L - 12| \\leq 0.2$. Al resolver, se tiene $-0.2 \\leq L - 12 \\leq 0.2$, lo que resulta en $11.8 \\leq L \\leq 12.2$."
            },
            {
                "stable_id": "ALG-GEN-INEVA-9",
                "nivel": 3,
                "tipo_ejercicio": "multiple_choice",
                "subtipo": "tipo_paes",
                "enunciado": "El conjunto de los números reales cuya distancia al número $4$ es estrictamente mayor que $7$ se puede representar mediante la inecuación $|x - 4| > 7$. ¿Cuál de los siguientes gráficos en la recta numérica describe este conjunto?",
                "opciones": [
                    "Los intervalos $(-\\infty, -3)$ y $(11, \\infty)$ sin incluir los extremos.",
                    "El segmento $(-3, 11)$ sin incluir los extremos.",
                    "Los intervalos $(-\\infty, -3]$ y $[11, \\infty)$ incluyendo los extremos.",
                    "Los intervalos $(-\\infty, 3)$ y $(11, \\infty)$ sin incluir los extremos."
                ],
                "respuesta_correcta": "Los intervalos $(-\\infty, -3)$ y $(11, \\infty)$ sin incluir los extremos.",
                "explicacion": "La inecuación se traduce a $x - 4 < -7$ o $x - 4 > 7$, que es $x < -3$ o $x > 11$. Esto corresponde a la unión de los intervalos abiertos $(-\\infty, -3) \\cup (11, \\infty)$."
            },
            {
                "stable_id": "ALG-GEN-INEVA-10",
                "nivel": 3,
                "tipo_ejercicio": "multiple_choice",
                "subtipo": "tipo_paes",
                "enunciado": "Si $a$ y $b$ son números reales, se sabe que la solución de la inecuación $|x - a| \\leq b$ es el intervalo $[-2, 8]$. ¿Cuáles son los valores de $a$ y $b$?",
                "opciones": [
                    "$a = 3$, $b = 5$",
                    "$a = 5$, $b = 3$",
                    "$a = 3$, $b = 8$",
                    "$a = -2$, $b = 5$"
                ],
                "respuesta_correcta": "$a = 3$, $b = 5$",
                "explicacion": "El intervalo $[-2, 8]$ tiene como centro o punto medio a $a = (-2 + 8)/2 = 3$. La distancia desde el centro a cualquiera de los extremos es $b = 8 - 3 = 5$. Por tanto, la inecuación es $|x - 3| \\leq 5$."
            }
        ]
    }
}

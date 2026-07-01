import os
import yaml
import json

topics = {
    "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.INTERPRETACION_INTERVALO": {
        "yaml": {
            "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.INTERPRETACION_INTERVALO",
            "titulo": "Interpretación del Valor Absoluto como Intervalo",
            "objetivo": "Interpretar la distancia entre números en la recta numérica usando inecuaciones con valor absoluto y expresarlo como un intervalo.",
            "introduccion": "El valor absoluto nos permite medir distancias sin preocuparnos por la dirección. Cuando establecemos una inecuación con valor absoluto, estamos determinando un conjunto de números que cumplen cierta condición de proximidad o lejanía respecto a un punto central específico.",
            "resumen": "La inecuación $|x - a| \\le b$ (con $b > 0$) representa todos los números $x$ cuya distancia a $a$ es menor o igual a $b$, lo que equivale al intervalo cerrado $[a - b, a + b]$. Análogamente, si es de tipo 'mayor que', representa los intervalos exteriores.",
            "explicacion": "### Definición formal\nPara cualquier número real $x$, y constantes $a, b \\in \\mathbb{R}$ con $b > 0$, la inecuación $|x - a| \\le b$ es equivalente a $-b \\le x - a \\le b$, cuyo conjunto solución en notación de intervalos es $x \\in [a - b, a + b]$. La inecuación $|x - a| \\ge b$ es equivalente a $x - a \\ge b \\lor x - a \\le -b$, y su solución se representa como la unión de intervalos $x \\in (-\\infty, a - b] \\cup [a + b, \\infty)$.\n\n### Desarrollo didáctico\nPodemos visualizar el valor absoluto $|x - a|$ como la distancia geométrica entre $x$ y $a$ en la recta numérica. Así, $|x - 3| < 2$ nos dice \"la distancia entre $x$ y $3$ es estrictamente menor que $2$\". Si nos paramos en el $3$, podemos caminar hasta casi $2$ pasos a la derecha (llegando al $5$) y casi $2$ pasos a la izquierda (llegando al $1$). Por lo tanto, cualquier número entre $1$ y $5$ cumple la condición. Esto se expresa directamente con el intervalo abierto $(1, 5)$.",
            "procedimiento": [
                "Identificar la inecuación y llevarla a la forma $|x - a| < b$, $|x - a| \\le b$, $|x - a| > b$, o $|x - a| \\ge b$.",
                "Plantear la doble desigualdad equivalente según sea el caso (intersección para menores, unión para mayores).",
                "Despejar la variable $x$ resolviendo las inecuaciones lineales resultantes.",
                "Escribir el conjunto solución empleando la notación formal de intervalos."
            ],
            "ejemplos": [
                {
                    "tipo": "A",
                    "titulo": "Distancia máxima en control de calidad",
                    "enunciado": "El grosor $x$ de una lámina metálica, medido en milímetros, debe cumplir con la inecuación $|x - 5| \\le 0.5$ para ser aceptada. Expresa el rango de grosores aceptables como un intervalo.",
                    "solucion_pasos": [
                        "La inecuación indica que la distancia de $x$ a $5$ debe ser menor o igual a $0.5$.",
                        "Planteamos la desigualdad doble: $-0.5 \\le x - 5 \\le 0.5$.",
                        "Sumamos $5$ en todas las partes: $5 - 0.5 \\le x \\le 5 + 0.5$.",
                        "Obtenemos $4.5 \\le x \\le 5.5$.",
                        "En notación de intervalo, el rango aceptable es $[4.5, 5.5]$ milímetros."
                    ]
                },
                {
                    "tipo": "A",
                    "titulo": "Rango de temperatura exterior",
                    "enunciado": "Se requiere que una maquinaria opere a temperaturas $T$ (en grados Celsius) que cumplan con la condición $|T - 20| > 15$. ¿En qué intervalos de temperatura debe operar la maquinaria?",
                    "solucion_pasos": [
                        "La inecuación indica que la distancia entre $T$ y $20$ es mayor a $15$.",
                        "Esto se divide en dos casos: $T - 20 > 15$ o $T - 20 < -15$.",
                        "Para el primer caso: $T > 35$. Para el segundo caso: $T < 5$.",
                        "La solución son los números menores a $5$ o mayores a $35$.",
                        "El intervalo correspondiente es $(-\\infty, 5) \\cup (35, \\infty)$."
                    ]
                },
                {
                    "tipo": "B",
                    "titulo": "¿El número $4$ pertenece al intervalo solución de $|x - 1| \\le 2$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "Evaluamos la distancia de $4$ al $1$: $|4 - 1| = |3| = 3$.",
                        "Comparamos con el límite: $3$ no es menor o igual a $2$.",
                        "Alternativamente, el intervalo es $[1 - 2, 1 + 2] = [-1, 3]$. El $4$ no pertenece a $[-1, 3]$."
                    ]
                },
                {
                    "tipo": "B",
                    "titulo": "¿El intervalo solución de la inecuación $|x| < 7$ es $(-7, 7)$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "La inecuación señala que la distancia desde $x$ al origen ($0$) es menor que $7$.",
                        "Esto se traduce en la desigualdad doble $-7 < x < 7$.",
                        "En notación de intervalos, los límites no se incluyen, por lo que resulta efectivamente en $(-7, 7)$."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Afirmar que $|x - a| < b$ significa que la distancia de $x$ a $b$ es menor que $a$.",
                "Concluir equivocadamente que el conjunto solución de una inecuación de la forma $|x - a| > b$ siempre puede escribirse como un solo intervalo continuo.",
                "Interpretar la inecuación $|x| < -5$ como un intervalo simétrico válido alrededor del cero, cuando en realidad no tiene solución real.",
                "Asumir que el centro del intervalo correspondiente a la desigualdad $|x + c| < d$ es $c$ positivo, ignorando que la forma estándar es restando el centro.",
                "Afirmar que los corchetes siempre se utilizan junto a los símbolos de infinito al escribir los intervalos."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "MAT.ALG.IVA.II-GEN-CONCEPT-1",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Geométricamente, ¿qué representa el conjunto solución de la inecuación $|x - 8| \\le 3$ en la recta numérica?",
                "opciones": [
                    "Todos los números cuya distancia a $8$ es menor o igual a $3$.",
                    "Todos los números cuya distancia a $3$ es menor o igual a $8$.",
                    "Todos los números negativos mayores que $3$.",
                    "Todos los números que están exactamente a una distancia de $3$ u $8$ desde el origen."
                ],
                "respuesta_correcta": "Todos los números cuya distancia a $8$ es menor o igual a $3$.",
                "explicacion": "La expresión $|x - 8|$ mide la distancia entre $x$ y $8$. Que sea menor o igual a $3$ significa que la distancia máxima a $8$ es $3$."
            },
            {
                "stable_id": "MAT.ALG.IVA.II-GEN-CONCEPT-2",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Si el conjunto solución de una inecuación es el intervalo $(-4, 4)$, ¿cuál inecuación con valor absoluto le corresponde?",
                "opciones": [
                    "$|x| < 4$",
                    "$|x| \\le 4$",
                    "$|x - 4| < 0$",
                    "$|x + 4| < 4$"
                ],
                "respuesta_correcta": "$|x| < 4$",
                "explicacion": "El intervalo $(-4, 4)$ contiene los números cuya distancia al cero es estrictamente menor a $4$, lo cual se escribe como $|x| < 4$."
            },
            {
                "stable_id": "MAT.ALG.IVA.II-GEN-CONCEPT-3",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Cuando se resuelve $|x - c| > d$ con $d > 0$, el conjunto solución siempre está compuesto por:",
                "opciones": [
                    "La unión de dos intervalos disjuntos.",
                    "Un único intervalo cerrado.",
                    "Un único intervalo abierto.",
                    "La intersección de dos rayos opuestos."
                ],
                "respuesta_correcta": "La unión de dos intervalos disjuntos.",
                "explicacion": "Las inecuaciones 'mayor que' indican números que se alejan del centro, formando dos zonas separadas representadas por dos intervalos."
            },
            {
                "stable_id": "MAT.ALG.IVA.II-GEN-RECON-1",
                "tipo": "reconocimiento",
                "nivel": 1,
                "enunciado": "Identifica la representación en intervalo para la inecuación $-5 \\le x - 2 \\le 5$.",
                "opciones": [
                    "$[-3, 7]$",
                    "$(-3, 7)$",
                    "$(-5, 5)$",
                    "$[-5, 5]$"
                ],
                "respuesta_correcta": "$[-3, 7]$",
                "explicacion": "Sumando $2$ a todas las partes de $-5 \\le x - 2 \\le 5$ obtenemos $-3 \\le x \\le 7$, que corresponde al intervalo $[-3, 7]$."
            },
            {
                "stable_id": "MAT.ALG.IVA.II-GEN-PROC-1",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El conjunto solución de $|x - 5| < 2$ es el intervalo $(3, 7)$.",
                "opciones": ["Verdadero", "Falso"],
                "respuesta_correcta": "Verdadero",
                "explicacion": "Despejando: $-2 < x - 5 < 2$. Sumando $5$: $3 < x < 7$, que se expresa como $(3, 7)$."
            },
            {
                "stable_id": "MAT.ALG.IVA.II-GEN-PROC-2",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El conjunto solución de $|x + 1| \\ge 4$ se puede escribir como el intervalo $[-5, 3]$.",
                "opciones": ["Verdadero", "Falso"],
                "respuesta_correcta": "Falso",
                "explicacion": "Es 'mayor o igual', por lo tanto son los exteriores: $x + 1 \\le -4 \\lor x + 1 \\ge 4$, dando $(-\\infty, -5] \\cup [3, \\infty)$."
            },
            {
                "stable_id": "MAT.ALG.IVA.II-GEN-PROC-3",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El conjunto solución de $|x| \\le 0$ está formado por un único número.",
                "opciones": ["Verdadero", "Falso"],
                "respuesta_correcta": "Verdadero",
                "explicacion": "El valor absoluto nunca es negativo, así que la única manera de cumplir $|x| \\le 0$ es que $x = 0$."
            },
            {
                "stable_id": "MAT.ALG.IVA.II-GEN-PAES-1",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Un fabricante de termómetros especifica que el error máximo de lectura permitido es de $0.2^{\\circ}\\text{C}$. Si un termómetro mide la temperatura real $T$ de un líquido que se sabe está a $100^{\\circ}\\text{C}$, ¿cuál es el intervalo de lecturas $L$ aceptables para este termómetro según el fabricante?",
                "opciones": [
                    "$[99.8, 100.2]$",
                    "$(99.8, 100.2)$",
                    "$[0, 0.2]$",
                    "$[-0.2, 0.2]$"
                ],
                "respuesta_correcta": "$[99.8, 100.2]$",
                "explicacion": "La condición indica que $|L - 100| \\le 0.2$. Al resolver, $-0.2 \\le L - 100 \\le 0.2$, lo que resulta en $99.8 \\le L \\le 100.2$, es decir, el intervalo $[99.8, 100.2]$."
            },
            {
                "stable_id": "MAT.ALG.IVA.II-GEN-PAES-2",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Se requiere que el valor de un componente $p$ cumpla la condición $|2p - 6| < 8$. ¿A qué intervalo debe pertenecer el valor de $p$ para ser admisible?",
                "opciones": [
                    "$(-1, 7)$",
                    "$(1, 7)$",
                    "$(-4, 4)$",
                    "$(-\\infty, -1) \\cup (7, \\infty)$"
                ],
                "respuesta_correcta": "$(-1, 7)$",
                "explicacion": "Resolviendo la inecuación: $-8 < 2p - 6 < 8$. Sumamos $6$: $-2 < 2p < 14$. Dividimos por $2$: $-1 < p < 7$, lo que corresponde a $(-1, 7)$."
            },
            {
                "stable_id": "MAT.ALG.IVA.II-GEN-PAES-3",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Para estimar el precio $P$ de un producto, un estudio de mercado define la banda de precios razonables usando la expresión $|P - 1500| \\le 300$. ¿Cuál de los siguientes precios queda FUERA de la banda razonable?",
                "opciones": [
                    "$1150$",
                    "$1200$",
                    "$1500$",
                    "$1750$"
                ],
                "respuesta_correcta": "$1150$",
                "explicacion": "La banda razonable es $1500 - 300 \\le P \\le 1500 + 300$, que equivale a $[1200, 1800]$. El precio $1150$ no pertenece a dicho intervalo."
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.EXPRESION_INTERVALO": {
        "yaml": {
            "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.EXPRESION_INTERVALO",
            "titulo": "Expresión de Inecuaciones Lineales como Intervalo",
            "objetivo": "Relacionar los conjuntos solución de inecuaciones lineales con su notación y representación en intervalos reales.",
            "introduccion": "Una vez que resolvemos una inecuación lineal, el resultado nos indica un conjunto infinito de números que satisfacen la condición inicial. Aprender a expresar este rango como un intervalo es fundamental para comunicar la respuesta de forma estandarizada y compacta.",
            "resumen": "Resolver una inecuación lineal de una variable arroja una desigualdad simple de la forma $x < a$, $x \\le a$, $x > a$ o $x \\ge a$. Cada una se asocia de forma directa con un intervalo: $(-\\infty, a)$, $(-\\infty, a]$, $(a, \\infty)$ o $[a, \\infty)$, respectivamente.",
            "explicacion": "### Definición formal\nUna inecuación lineal es una expresión de la forma $mx + n \\ge 0$, donde $m, n \\in \\mathbb{R}$ y $m \\neq 0$ (o utilizando otros símbolos de orden). Su solución es un conjunto $S \\subseteq \\mathbb{R}$. Dependiendo de la desigualdad resultante tras despejar $x$, el conjunto solución se denota mediante un intervalo que se extiende hasta el infinito positivo o negativo. Los símbolos de orden estricto ($<$ o $>$) generan intervalos abiertos denotados con paréntesis redondos, y los de orden no estricto ($\\le$ o $\\ge$) incluyen al extremo con un corchete recto cerrado.\n\n### Desarrollo didáctico\nDespejar una inecuación lineal es muy similar a resolver una ecuación, con la salvedad de que multiplicar o dividir por un número negativo invierte el signo de la desigualdad. Por ejemplo, al llegar a la conclusión $x \\ge 4$, leemos \"todos los números mayores o iguales a $4$\". Si representamos esto en la recta numérica, dibujaríamos un punto relleno en el $4$ y sombrearíamos todo hacia la derecha. La notación de intervalo resume ese dibujo como $[4, \\infty)$. Si el resultado fuera $x < 4$, sería un círculo sin rellenar en el $4$ sombreado hacia la izquierda, denotado como $(-\\infty, 4)$.",
            "procedimiento": [
                "Simplificar y agrupar los términos semejantes de la inecuación lineal a ambos lados.",
                "Despejar la variable $x$, recordando invertir la desigualdad si multiplicas o divides por un coeficiente negativo.",
                "Interpretar la expresión final (por ejemplo $x > a$) ubicando mentalmente o en papel los valores en la recta numérica real.",
                "Traducir dicha región gráfica en la notación de intervalo correspondiente, cuidando el uso de corchetes según si el extremo está incluido o no."
            ],
            "ejemplos": [
                {
                    "tipo": "A",
                    "titulo": "Presupuesto de compras",
                    "enunciado": "Tienes un presupuesto de $50000$ pesos y quieres comprar libros que cuestan $12000$ pesos cada uno, además de pagar $2000$ por envío. ¿Cuántos libros $x$ puedes comprar? Expresa el conjunto de valores que puede tomar $x$ como intervalo continuo.",
                    "solucion_pasos": [
                        "Modelamos el gasto total: $12000x + 2000 \\le 50000$.",
                        "Restamos $2000$: $12000x \\le 48000$.",
                        "Dividimos por $12000$: $x \\le 4$.",
                        "El intervalo de números reales que cumplen esta condición es $(-\\infty, 4]$. (En la vida real se restringiría a enteros no negativos)."
                    ]
                },
                {
                    "tipo": "A",
                    "titulo": "Resolución con coeficiente negativo",
                    "enunciado": "Resuelve la inecuación $-3x + 7 > 22$ y expresa su conjunto solución usando notación de intervalos.",
                    "solucion_pasos": [
                        "Restamos $7$ a ambos lados: $-3x > 15$.",
                        "Dividimos por $-3$. Como es negativo, invertimos el sentido de la desigualdad: $x < -5$.",
                        "En palabras, son todos los números menores que $-5$.",
                        "En notación de intervalo, esto se escribe como $(-\\infty, -5)$."
                    ]
                },
                {
                    "tipo": "B",
                    "titulo": "¿El conjunto solución de $2x \\ge 10$ se representa con el intervalo $(5, \\infty)$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "Despejando $x$, dividimos por $2$ (positivo), quedando $x \\ge 5$.",
                        "Como la desigualdad incluye el igual (es no estricta), el $5$ debe estar incluido.",
                        "La notación correcta emplea corchete: $[5, \\infty)$."
                    ]
                },
                {
                    "tipo": "B",
                    "titulo": "¿El infinito siempre va acompañado de un paréntesis redondo en los intervalos?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "El infinito no es un número real específico que pueda ser 'incluido'.",
                        "Por convención matemática universal, en la notación de intervalos siempre se usan paréntesis o corchetes abiertos en los extremos infinitos, es decir, $(-\\infty$ y $\\infty)$."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Afirmar que el corchete se usa en los extremos numéricos de un intervalo de forma obligatoria e independiente del tipo de desigualdad.",
                "Omitir la inversión del símbolo de desigualdad al dividir o multiplicar por un coeficiente negativo.",
                "Concluir que el símbolo de infinito $(+\\infty)$ o $(-\\infty)$ puede ir acompañado de un corchete cerrado.",
                "Escribir el intervalo al revés, colocando el número mayor a la izquierda y el menor a la derecha.",
                "Interpretar una desigualdad estricta (como $x < 8$) empleando un corchete cerrado para el número límite en el intervalo."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "MAT.ALG.IL.EI-GEN-CONCEPT-1",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Si el resultado de despejar una inecuación lineal es $x > -2$, ¿qué intervalo representa correctamente este conjunto solución?",
                "opciones": [
                    "$(-2, \\infty)$",
                    "$[-2, \\infty)$",
                    "$(-\\infty, -2)$",
                    "$(-\\infty, -2]$"
                ],
                "respuesta_correcta": "$(-2, \\infty)$",
                "explicacion": "La condición $x > -2$ implica todos los números mayores que $-2$, extendiéndose hasta el infinito positivo, sin incluir el $-2$. Esto es $(-2, \\infty)$."
            },
            {
                "stable_id": "MAT.ALG.IL.EI-GEN-CONCEPT-2",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "¿Qué diferencia gráfica y notacional existe entre $x < 3$ y $x \\le 3$?",
                "opciones": [
                    "La primera no incluye el $3$ (paréntesis), la segunda sí (corchete).",
                    "La primera va a infinito positivo, la segunda a infinito negativo.",
                    "La primera incluye el $3$ (corchete), la segunda no (paréntesis).",
                    "No existe ninguna diferencia."
                ],
                "respuesta_correcta": "La primera no incluye el $3$ (paréntesis), la segunda sí (corchete).",
                "explicacion": "El símbolo $<$ es estricto (no incluye el extremo, se usa paréntesis), mientras que $\\le$ incluye la igualdad (se usa corchete cerrado)."
            },
            {
                "stable_id": "MAT.ALG.IL.EI-GEN-CONCEPT-3",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Al multiplicar ambos lados de una inecuación lineal por $-1$, ¿qué ocurre geométricamente con el conjunto solución en la recta?",
                "opciones": [
                    "Se refleja respecto al cero (cambian los signos y se invierte la dirección de la desigualdad).",
                    "Se mantiene exactamente en la misma posición y dirección.",
                    "Se desplaza hacia la izquierda en una unidad.",
                    "Se transforma en un intervalo cerrado sin importar cómo era antes."
                ],
                "respuesta_correcta": "Se refleja respecto al cero (cambian los signos y se invierte la dirección de la desigualdad).",
                "explicacion": "Multiplicar por $-1$ cambia el signo de los números (reflexión en cero) y obliga a invertir el símbolo de la desigualdad para mantener la verdad de la proposición."
            },
            {
                "stable_id": "MAT.ALG.IL.EI-GEN-RECON-1",
                "tipo": "reconocimiento",
                "nivel": 1,
                "enunciado": "La inecuación lineal $-x < 4$ es equivalente a:",
                "opciones": [
                    "$x > -4$",
                    "$x < -4$",
                    "$x > 4$",
                    "$x < 4$"
                ],
                "respuesta_correcta": "$x > -4$",
                "explicacion": "Al multiplicar o dividir por $-1$ ambos lados, debemos invertir la desigualdad, obteniendo $x > -4$."
            },
            {
                "stable_id": "MAT.ALG.IL.EI-GEN-PROC-1",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El conjunto solución de la inecuación $3x - 5 \\le 10$ es el intervalo $(-\\infty, 5]$.",
                "opciones": ["Verdadero", "Falso"],
                "respuesta_correcta": "Verdadero",
                "explicacion": "Sumando $5$: $3x \\le 15$. Dividiendo por $3$: $x \\le 5$. El intervalo de números menores o iguales a $5$ es $(-\\infty, 5]$."
            },
            {
                "stable_id": "MAT.ALG.IL.EI-GEN-PROC-2",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El conjunto solución de $-2x + 4 < 0$ es $(-\\infty, 2)$.",
                "opciones": ["Verdadero", "Falso"],
                "respuesta_correcta": "Falso",
                "explicacion": "Restando $4$: $-2x < -4$. Al dividir por $-2$, invertimos la desigualdad: $x > 2$. El intervalo correcto es $(2, \\infty)$."
            },
            {
                "stable_id": "MAT.ALG.IL.EI-GEN-PROC-3",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "La solución de $\\frac{x}{2} + 1 \\ge 4$ se puede expresar mediante el intervalo $[6, \\infty)$.",
                "opciones": ["Verdadero", "Falso"],
                "respuesta_correcta": "Verdadero",
                "explicacion": "Restando $1$: $\\frac{x}{2} \\ge 3$. Multiplicando por $2$: $x \\ge 6$. Esto en intervalo es $[6, \\infty)$."
            },
            {
                "stable_id": "MAT.ALG.IL.EI-GEN-PAES-1",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "En un plan de telefonía celular, el costo mensual $C$ en pesos se calcula como un cargo fijo de $\\$5000$ más $\\$50$ por cada minuto extra $x$ consumido, es decir, $C = 5000 + 50x$. Si un usuario desea que su factura no supere los $\\$12000$, ¿cuál de los siguientes intervalos representa los valores posibles para los minutos extra $x$ consumidos?",
                "opciones": [
                    "$(-\\infty, 140]$",
                    "$[140, \\infty)$",
                    "$(-\\infty, 140)$",
                    "$(140, \\infty)$"
                ],
                "respuesta_correcta": "$(-\\infty, 140]$",
                "explicacion": "La condición es $5000 + 50x \\le 12000$. Restando $5000$: $50x \\le 7000$. Dividiendo por $50$: $x \\le 140$. Como intervalo numérico completo es $(-\\infty, 140]$. (El dominio real sería desde $0$)."
            },
            {
                "stable_id": "MAT.ALG.IL.EI-GEN-PAES-2",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Al resolver la inecuación $\\frac{2x - 3}{3} < \\frac{x + 1}{2}$, ¿qué intervalo representa el conjunto solución?",
                "opciones": [
                    "$(-\\infty, 9)$",
                    "$(9, \\infty)$",
                    "$(-\\infty, 9]$",
                    "$(-\\infty, 3)$"
                ],
                "respuesta_correcta": "$(-\\infty, 9)$",
                "explicacion": "Multiplicamos la inecuación por el mcm $6$: $2(2x - 3) < 3(x + 1)$. Desarrollando: $4x - 6 < 3x + 3$. Restando $3x$ y sumando $6$: $x < 9$. Su intervalo es $(-\\infty, 9)$."
            },
            {
                "stable_id": "MAT.ALG.IL.EI-GEN-PAES-3",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Sea el conjunto $P$ la solución de $1 - 4x \\ge 13$. ¿A cuál de los siguientes intervalos pertenece el conjunto $P$?",
                "opciones": [
                    "$(-\\infty, -3]$",
                    "$[-3, \\infty)$",
                    "$(-\\infty, 3]$",
                    "$(3, \\infty)$"
                ],
                "respuesta_correcta": "$(-\\infty, -3]$",
                "explicacion": "Restando $1$: $-4x \\ge 12$. Dividiendo por $-4$ (e invirtiendo la desigualdad): $x \\le -3$. Por tanto, el conjunto $P$ es $(-\\infty, -3]$."
            }
        ]
    }
}

def main():
    os.makedirs('scratch/out_yaml', exist_ok=True)
    os.makedirs('scratch/out_jsonl', exist_ok=True)

    for semantic_id, content in topics.items():
        yaml_data = content["yaml"]
        jsonl_data = content["jsonl"]

        # Save yaml
        yaml_path = f"scratch/out_yaml/{semantic_id}.yaml"
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

        # Save jsonl
        jsonl_path = f"scratch/out_jsonl/{semantic_id}.jsonl"
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            for item in jsonl_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\\n")

    print(f"Archivos generados exitosamente en scratch/out_yaml/ y scratch/out_jsonl/.")

if __name__ == '__main__':
    main()

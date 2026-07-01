topics = {
    "MAT.ALG.INECUACIONES_LINEALES": {
        "yaml": {
            "titulo": "Inecuaciones Lineales",
            "objetivo": "Comprender y resolver inecuaciones lineales identificando el conjunto solución correspondiente.",
            "introduccion": "Las inecuaciones lineales establecen una relación de desigualdad entre dos expresiones algebraicas de primer grado.",
            "resumen": "Una inecuación lineal tiene la forma general $ax + b < c$, $ax + b \\le c$, $ax + b > c$ o $ax + b \\ge c$, donde $a, b, c \\in \\mathbb{R}$ y $a \\neq 0$.",
            "explicacion": "### Definición formal\nSea una inecuación lineal una desigualdad de la forma $ax+b < c$ (o $>$, $\\le$, $\\ge$), donde $x$ es la incógnita y $a, b, c$ son números reales con $a \\neq 0$.\n\n### Desarrollo didáctico\nAl igual que en una ecuación, el objetivo es aislar la incógnita $x$ utilizando operaciones aritméticas, manteniendo siempre la desigualdad. Es fundamental recordar que si multiplicamos o dividimos ambos lados de la inecuación por un número negativo, el sentido de la desigualdad se invierte.",
            "procedimiento": [
                "Agrupar los términos con la incógnita $x$ en un lado de la desigualdad y los términos independientes en el otro lado.",
                "Reducir los términos semejantes en ambos lados de la inecuación.",
                "Despejar la incógnita dividiendo ambos lados por su coeficiente. Si dicho coeficiente es negativo, invertir el sentido de la desigualdad."
            ],
            "ejemplos": [
                {
                    "titulo": "Resolución de inecuación básica",
                    "enunciado": "Resolver la inecuación $2x - 3 < 5$.",
                    "solucion_pasos": [
                        "Sumamos $3$ a ambos lados: $2x < 5 + 3$.",
                        "Simplificamos: $2x < 8$.",
                        "Dividimos por $2$: $x < 4$."
                    ]
                },
                {
                    "titulo": "Resolución con términos en ambos lados",
                    "enunciado": "Resolver $4x + 2 \\ge x - 7$.",
                    "solucion_pasos": [
                        "Restamos $x$ a ambos lados: $3x + 2 \\ge -7$.",
                        "Restamos $2$ a ambos lados: $3x \\ge -9$.",
                        "Dividimos por $3$: $x \\ge -3$."
                    ]
                },
                {
                    "titulo": "¿El número $0$ pertenece al conjunto solución de $x + 5 < 2$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "Sustituimos $x = 0$ en la inecuación: $0 + 5 < 2$.",
                        "Obtenemos la proposición $5 < 2$.",
                        "Como $5$ no es menor que $2$, el $0$ no es parte del conjunto solución."
                    ]
                },
                {
                    "titulo": "¿El valor $x=3$ satisface la inecuación $-2x + 1 \\le -3$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "Reemplazamos $x = 3$: $-2(3) + 1 \\le -3$.",
                        "Calculamos: $-6 + 1 \\le -3$, es decir $-5 \\le -3$.",
                        "Como la desigualdad es verdadera, $x=3$ es solución."
                    ]
                }
            ],
            "errores_frecuentes": [
                "El conjunto solución de una inecuación lineal es siempre un único número.",
                "Al dividir ambos lados por un número negativo, el símbolo de desigualdad se mantiene igual.",
                "Las inecuaciones lineales no se pueden representar gráficamente en la recta numérica.",
                "Resolver una inecuación lineal es exactamente lo mismo que resolver una ecuación cuadrática.",
                "Una inecuación de la forma $0x < 5$ tiene como solución a todo el conjunto de los números reales negativos."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "ALG-GEN-INECLI-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECLI-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECLI-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECLI-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECLI-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECLI-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECLI-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECLI-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECLI-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECLI-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.DEFINICION": {
        "yaml": {
            "titulo": "Definición de Inecuaciones Lineales",
            "objetivo": "Identificar los componentes y la estructura que definen a una inecuación lineal.",
            "introduccion": "Una inecuación se diferencia de una ecuación en que relaciona expresiones matemáticas mediante un símbolo de desigualdad en lugar de uno de igualdad.",
            "resumen": "Se define a través de los signos $<, >, \\le, \\ge$ y contiene variables cuyo mayor exponente es $1$.",
            "explicacion": "### Definición formal\nUna inecuación lineal es una proposición matemática que relaciona dos expresiones algebraicas lineales mediante desigualdades, por ejemplo $P(x) < Q(x)$, con grado $1$.\n\n### Desarrollo didáctico\nAplicamos el concepto de desigualdad para comparar cantidades. Esencialmente establece que un lado puede ser estrictamente mayor, estrictamente menor, o igual al otro lado, formando un rango continuo de valores.",
            "procedimiento": [
                "Identificar la variable presente en la inecuación.",
                "Asegurarse de que el máximo exponente de la variable sea $1$.",
                "Reconocer el símbolo de desigualdad utilizado ($<, >, \\le, \\ge$)."
            ],
            "ejemplos": [
                {
                    "titulo": "Reconocimiento de inecuación lineal",
                    "enunciado": "Determinar si $3x + 1 > 4$ es una inecuación lineal.",
                    "solucion_pasos": [
                        "Identificamos la variable $x$.",
                        "Observamos que el exponente de $x$ es $1$.",
                        "Concluimos que sí es una inecuación lineal."
                    ]
                },
                {
                    "titulo": "Diferenciación con ecuaciones",
                    "enunciado": "Distinguir $2x = 5$ de $2x < 5$.",
                    "solucion_pasos": [
                        "La primera tiene el signo $=$, es una ecuación.",
                        "La segunda tiene el signo $<$, es una inecuación lineal."
                    ]
                },
                {
                    "titulo": "¿La expresión $x^2 + 1 > 0$ corresponde a una inecuación lineal?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "Verificamos la variable $x$.",
                        "Su exponente es $2$.",
                        "Al no ser de grado $1$, no es lineal."
                    ]
                },
                {
                    "titulo": "¿Es $5 - x \\ge 2$ una inecuación lineal?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "Identificamos la variable $x$.",
                        "Observamos que es de primer grado.",
                        "Contiene el signo $\\ge$, por ende cumple la definición."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Pensar que una expresión como $x^3 < 8$ es una inecuación lineal.",
                "Creer que una inecuación lineal solo puede tener el signo $>$.",
                "Confundir el signo de desigualdad con una ecuación de igualdad.",
                "Considerar que $x + y = 3$ es una inecuación lineal en una variable.",
                "Afirmar que $1/x > 2$ es una inecuación lineal."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "ALG-GEN-INEDEFI-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDEFI-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDEFI-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDEFI-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDEFI-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INEDEFI-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INEDEFI-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INEDEFI-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDEFI-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDEFI-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.RESOLUCION_DESPEJE": {
        "yaml": {
            "titulo": "Resolución de Inecuaciones por Despeje",
            "objetivo": "Aislar la variable en una inecuación lineal mediante operaciones inversas para hallar su conjunto solución.",
            "introduccion": "El despeje en inecuaciones sigue reglas muy similares al de las ecuaciones, cuidando especialmente el manejo del signo de la desigualdad.",
            "resumen": "Consiste en sumar, restar, multiplicar o dividir constantes a ambos lados de la inecuación para dejar la incógnita sola.",
            "explicacion": "### Definición formal\nEl proceso de despeje se basa en las propiedades de monotonicidad de la suma y el producto sobre desigualdades para transformar $ax+b<c$ en $x < k$ (o similar).\n\n### Desarrollo didáctico\nSe realizan operaciones equivalentes en ambos miembros de la desigualdad. Se debe proceder sumando o restando términos primero, y finalmente dividiendo o multiplicando por el coeficiente de la variable.",
            "procedimiento": [
                "Sumar o restar los términos necesarios para dejar los términos con la variable de un solo lado.",
                "Simplificar ambos lados de la desigualdad.",
                "Dividir ambos lados por el coeficiente de la variable (si es positivo, la desigualdad se mantiene)."
            ],
            "ejemplos": [
                {
                    "titulo": "Despeje con suma",
                    "enunciado": "Resolver $x - 8 > 12$.",
                    "solucion_pasos": [
                        "Sumamos $8$ a ambos lados de la inecuación.",
                        "Obtenemos $x > 12 + 8$.",
                        "El resultado final es $x > 20$."
                    ]
                },
                {
                    "titulo": "Despeje con resta y división",
                    "enunciado": "Resolver $3x + 5 \\le 14$.",
                    "solucion_pasos": [
                        "Restamos $5$ a ambos lados: $3x \\le 9$.",
                        "Dividimos entre $3$ a ambos lados.",
                        "Obtenemos $x \\le 3$."
                    ]
                },
                {
                    "titulo": "¿El conjunto de valores de $x$ que cumple $x + 4 < 10$ incluye al $6$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "Restamos $4$ en ambos lados: $x < 6$.",
                        "La desigualdad indica que $x$ debe ser estrictamente menor que $6$.",
                        "Por lo tanto, $6$ no está incluido."
                    ]
                },
                {
                    "titulo": "¿Es $x > 2$ la solución de $5x > 10$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "Dividimos ambos lados entre $5$.",
                        "Como $5$ es positivo, la desigualdad se mantiene.",
                        "La inecuación equivalente es $x > 2$."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Sumar un término en un lado y restarlo en el otro.",
                "Olvidar realizar la operación en ambos lados de la desigualdad.",
                "Invertir el símbolo de desigualdad al dividir por un número positivo.",
                "Dejar la variable con coeficiente diferente de $1$ y considerar el ejercicio terminado.",
                "Sustituir el símbolo de la desigualdad por un signo de igual al final del proceso."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "ALG-GEN-INEDESP-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDESP-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDESP-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDESP-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDESP-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INEDESP-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INEDESP-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INEDESP-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDESP-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEDESP-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION": {
        "yaml": {
            "titulo": "Conjunto Solución de Inecuaciones Lineales",
            "objetivo": "Representar y determinar el conjunto de todos los valores que satisfacen una inecuación lineal.",
            "introduccion": "A diferencia de una ecuación lineal que generalmente tiene una sola solución, una inecuación lineal tiene un rango continuo de soluciones.",
            "resumen": "El conjunto solución se expresa matemáticamente utilizando notación de intervalos o representación gráfica en la recta real.",
            "explicacion": "### Definición formal\nEl conjunto solución $S$ de una inecuación en $\\mathbb{R}$ es el subconjunto de los números reales para los cuales la proposición es verdadera.\n\n### Desarrollo didáctico\nAl resolver la inecuación y llegar a formas como $x > a$ o $x \\le b$, debemos interpretar estos resultados geométricamente o con notación de conjuntos. Por ejemplo, $x > 2$ corresponde al intervalo abierto $(2, \\infty)$.",
            "procedimiento": [
                "Resolver la inecuación despejando la variable $x$.",
                "Identificar la desigualdad resultante y el límite del intervalo.",
                "Expresar el resultado en notación de intervalo, recordando usar paréntesis para desigualdades estrictas ($<, >$) y corchetes para desigualdades no estrictas ($\\le, \\ge$)."
            ],
            "ejemplos": [
                {
                    "titulo": "Notación de intervalo abierto",
                    "enunciado": "Determinar el conjunto solución de $x > -4$.",
                    "solucion_pasos": [
                        "Identificamos que la desigualdad es estricta.",
                        "El valor inferior es $-4$ y no está incluido.",
                        "El intervalo solución es $(-4, \\infty)$."
                    ]
                },
                {
                    "titulo": "Notación de intervalo cerrado",
                    "enunciado": "Encontrar el conjunto solución de $x \\le 5$.",
                    "solucion_pasos": [
                        "La desigualdad es no estricta.",
                        "El valor superior es $5$ y sí está incluido.",
                        "El intervalo solución es $(-\\infty, 5]$."
                    ]
                },
                {
                    "titulo": "¿El intervalo $[2, \\infty)$ es la solución de la inecuación $x < 2$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "La inecuación $x < 2$ indica valores estrictamente menores a $2$.",
                        "El conjunto solución debe ser $(-\\infty, 2)$.",
                        "El intervalo $[2, \\infty)$ corresponde a $x \\ge 2$."
                    ]
                },
                {
                    "titulo": "¿El intervalo $(-\\infty, -1]$ es el conjunto solución de $2x \\le -2$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "Despejamos $x$ dividiendo entre $2$.",
                        "Obtenemos $x \\le -1$.",
                        "Esto se representa mediante el intervalo $(-\\infty, -1]$."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Utilizar corchetes para desigualdades estrictas ($<, >$).",
                "Escribir siempre el infinito positivo independientemente de la dirección de la desigualdad.",
                "Usar corchetes junto al símbolo de infinito ($\\infty]$).",
                "Pensar que el conjunto solución de $x > 3$ comienza exactamente en $4$.",
                "Interpretar $(-\\infty, 2)$ y $(2, -\\infty)$ como notaciones válidas por igual."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "ALG-GEN-INECSOL-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSOL-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSOL-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSOL-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSOL-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECSOL-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECSOL-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECSOL-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSOL-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSOL-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE": {
        "yaml": {
            "titulo": "Multiplicación por Constantes Negativas",
            "objetivo": "Aplicar correctamente la regla de inversión del sentido de la desigualdad al multiplicar o dividir por números negativos.",
            "introduccion": "Una de las reglas más importantes al trabajar con inecuaciones es el cambio que ocurre al multiplicar o dividir ambos miembros por un número negativo.",
            "resumen": "Si se multiplica o divide una inecuación por un número real negativo, el sentido de la desigualdad se invierte obligatoriamente.",
            "explicacion": "### Definición formal\nSea una inecuación $A < B$. Si $k \\in \\mathbb{R}$ y $k < 0$, entonces al multiplicar por $k$ se cumple que $k \\cdot A > k \\cdot B$.\n\n### Desarrollo didáctico\nEsta regla garantiza que la proposición siga siendo verdadera. Por ejemplo, sabemos que $2 < 5$; si multiplicamos por $-1$, obtenemos $-2$ y $-5$. Para que sea cierto, debemos decir que $-2 > -5$, con lo cual hemos invertido el símbolo.",
            "procedimiento": [
                "Identificar que el coeficiente que acompaña a la variable es negativo.",
                "Dividir o multiplicar ambos miembros por dicho coeficiente negativo.",
                "Inmediatamente invertir el sentido de la desigualdad (por ejemplo, de $<$ a $>$)."
            ],
            "ejemplos": [
                {
                    "titulo": "Despeje con coeficiente negativo",
                    "enunciado": "Resolver la inecuación $-3x < 12$.",
                    "solucion_pasos": [
                        "Dividimos ambos lados por $-3$.",
                        "Al dividir por un negativo, invertimos el signo: $x > \\frac{12}{-3}$.",
                        "El resultado es $x > -4$."
                    ]
                },
                {
                    "titulo": "Multiplicación de la desigualdad por menos uno",
                    "enunciado": "Resolver $-x \\ge 7$.",
                    "solucion_pasos": [
                        "Multiplicamos ambos lados por $-1$.",
                        "Invertimos la desigualdad, obteniendo $x \\le -7$."
                    ]
                },
                {
                    "titulo": "¿El conjunto solución de $-2x > 8$ es $x > -4$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "Al dividir entre $-2$, debemos invertir la desigualdad.",
                        "De este modo, se obtiene $x < -4$.",
                        "El conjunto planteado no consideró la inversión del signo."
                    ]
                },
                {
                    "titulo": "¿Al resolver $-5x \\le -15$, la solución es $x \\ge 3$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "Dividimos ambos lados por $-5$.",
                        "Invertimos el signo de $\\le$ a $\\ge$.",
                        "Por lo tanto, obtenemos $x \\ge 3$."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Dividir por un negativo y dejar el símbolo de la desigualdad exactamente igual.",
                "Invertir el símbolo solo cuando el término independiente es negativo.",
                "Cambiar el símbolo de la desigualdad al sumar o restar un número negativo.",
                "Pensar que al invertir el signo $<$ pasa a ser $\\le$.",
                "Creer que solo la multiplicación invierte el sentido, pero no la división."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "ALG-GEN-INEMNEG-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEMNEG-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEMNEG-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEMNEG-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEMNEG-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INEMNEG-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INEMNEG-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INEMNEG-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEMNEG-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INEMNEG-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.COEFICIENTES_FRACCIONARIOS": {
        "yaml": {
            "titulo": "Inecuaciones con Coeficientes Fraccionarios",
            "objetivo": "Resolver inecuaciones lineales que involucran fracciones empleando el mínimo común múltiplo para simplificarlas.",
            "introduccion": "Cuando los términos de una inecuación incluyen coeficientes racionales, se puede utilizar el mínimo común múltiplo (MCM) de los denominadores para transformarla en una expresión entera.",
            "resumen": "Se multiplica toda la inecuación por el MCM de sus denominadores para eliminar las fracciones y proceder como en una inecuación con números enteros.",
            "explicacion": "### Definición formal\nSean $\\frac{a}{b}x + \\frac{c}{d} < \\frac{e}{f}$ inecuaciones con coeficientes fraccionarios. Al multiplicar por $m = \\text{mcm}(b, d, f)$ con $m > 0$, se obtiene una inecuación equivalente en $\\mathbb{Z}$.\n\n### Desarrollo didáctico\nAl aplicar el MCM a ambos lados de la desigualdad, simplificamos las fracciones al instante. Es vital multiplicar absolutamente todos los términos, incluso los que no son fracciones. Como el MCM siempre es positivo, el sentido de la desigualdad se mantiene.",
            "procedimiento": [
                "Identificar los denominadores presentes en la inecuación y calcular su mínimo común múltiplo (MCM).",
                "Multiplicar todos los términos de ambos lados de la inecuación por el MCM para eliminar los denominadores.",
                "Resolver la inecuación resultante utilizando el método de despeje estándar."
            ],
            "ejemplos": [
                {
                    "titulo": "Resolución de inecuación fraccionaria",
                    "enunciado": "Resolver la inecuación $\\frac{x}{2} + 1 > 3$.",
                    "solucion_pasos": [
                        "Multiplicamos toda la inecuación por $2$: $2 \\cdot \\frac{x}{2} + 2 \\cdot 1 > 2 \\cdot 3$.",
                        "Simplificamos a $x + 2 > 6$.",
                        "Restamos $2$ en ambos lados y obtenemos $x > 4$."
                    ]
                },
                {
                    "titulo": "Despeje con diferentes denominadores",
                    "enunciado": "Resolver $\\frac{x}{3} - \\frac{1}{2} \\le \\frac{x}{6}$.",
                    "solucion_pasos": [
                        "El MCM de $3, 2, 6$ es $6$.",
                        "Multiplicamos por $6$: $6(\\frac{x}{3}) - 6(\\frac{1}{2}) \\le 6(\\frac{x}{6})$.",
                        "Simplificamos: $2x - 3 \\le x$.",
                        "Restamos $x$ y sumamos $3$: $x \\le 3$."
                    ]
                },
                {
                    "titulo": "¿Al resolver $\\frac{x}{4} < \\frac{1}{2}$, la solución es $x < 1$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "El MCM es $4$.",
                        "Multiplicamos por $4$: $4(\\frac{x}{4}) < 4(\\frac{1}{2})$.",
                        "Esto resulta en $x < 2$. Por ende, la afirmación no es correcta."
                    ]
                },
                {
                    "titulo": "¿La inecuación $\\frac{2x}{5} > 2$ tiene por solución $x > 5$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "Multiplicamos ambos miembros por $5$.",
                        "Obtenemos $2x > 10$.",
                        "Dividimos por $2$ y resulta $x > 5$."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Multiplicar por el MCM solo las fracciones y olvidar los términos enteros.",
                "Invertir el sentido de la desigualdad al multiplicar por un MCM positivo.",
                "Calcular incorrectamente el mínimo común múltiplo de los denominadores.",
                "Sumar los denominadores en lugar de buscar un común denominador.",
                "Eliminar el denominador de un lado de la inecuación pero conservarlo en el otro."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "ALG-GEN-INECFRA-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECFRA-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECFRA-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECFRA-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECFRA-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECFRA-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECFRA-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECFRA-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECFRA-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECFRA-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.SIGNOS_AGRUPACION": {
        "yaml": {
            "titulo": "Inecuaciones con Signos de Agrupación",
            "objetivo": "Resolver inecuaciones lineales utilizando la propiedad distributiva para eliminar paréntesis y otros signos de agrupación.",
            "introduccion": "Muchas expresiones algebraicas dentro de inecuaciones contienen paréntesis que deben ser resueltos antes de poder aislar la incógnita.",
            "resumen": "El uso de la propiedad distributiva permite expandir las expresiones, agrupar términos semejantes y luego resolver la inecuación lineal resultante de manera estándar.",
            "explicacion": "### Definición formal\nPara expresiones de la forma $a(bx + c) \\ge d$, se aplica el axioma distributivo del producto sobre la suma: $abx + ac \\ge d$, manteniendo las propiedades del orden de los números reales.\n\n### Desarrollo didáctico\nCuando un número multiplica a un paréntesis, se debe distribuir multiplicando este número por cada término interno. Es de suma importancia considerar el signo del número multiplicador para aplicar correctamente la ley de los signos durante la distribución.",
            "procedimiento": [
                "Identificar los signos de agrupación en ambos miembros de la inecuación.",
                "Aplicar la propiedad distributiva para eliminar dichos signos.",
                "Agrupar los términos algebraicos semejantes y resolver despejando la incógnita."
            ],
            "ejemplos": [
                {
                    "titulo": "Distribución y resolución",
                    "enunciado": "Resolver $2(x - 3) > 4$.",
                    "solucion_pasos": [
                        "Distribuimos el $2$: $2x - 6 > 4$.",
                        "Sumamos $6$ a ambos lados: $2x > 10$.",
                        "Dividimos por $2$: $x > 5$."
                    ]
                },
                {
                    "titulo": "Distribución con coeficiente negativo",
                    "enunciado": "Resolver $-3(x + 2) \\le 9$.",
                    "solucion_pasos": [
                        "Aplicamos la distributiva: $-3x - 6 \\le 9$.",
                        "Sumamos $6$ en ambos lados: $-3x \\le 15$.",
                        "Dividimos por $-3$ e invertimos el símbolo: $x \\ge -5$."
                    ]
                },
                {
                    "titulo": "¿La inecuación $5(x - 1) < 5x$ tiene conjunto solución vacío?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "Distribuimos el $5$: $5x - 5 < 5x$.",
                        "Restamos $5x$ en ambos lados y obtenemos $-5 < 0$.",
                        "Como $-5$ siempre es menor a $0$, cualquier valor de $x$ satisface la inecuación. Por lo tanto, es el conjunto de los reales, no vacío."
                    ]
                },
                {
                    "titulo": "¿Es $x > 4$ la solución de $2(x + 1) > 10$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "Distribuimos el $2$: $2x + 2 > 10$.",
                        "Restamos $2$: $2x > 8$.",
                        "Al dividir por $2$, obtenemos $x > 4$."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Distribuir el factor solo al primer término dentro del paréntesis.",
                "Equivocarse con la ley de los signos al distribuir un número negativo.",
                "Sumar el número que está fuera del paréntesis en lugar de multiplicarlo.",
                "Ignorar los paréntesis y multiplicar solo el primer término por conveniencia.",
                "Invertir el sentido de la desigualdad inmediatamente al eliminar los signos de agrupación, sin que exista motivo real."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "ALG-GEN-INECSIG-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSIG-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSIG-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSIG-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSIG-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECSIG-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECSIG-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "pregunta": "...",
                "respuesta_correcta": "True"
            },
            {
                "stable_id": "ALG-GEN-INECSIG-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSIG-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            },
            {
                "stable_id": "ALG-GEN-INECSIG-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "pregunta": "...",
                "opciones": ["A", "B", "C", "D", "E"],
                "respuesta_correcta": "A"
            }
        ]
    }
}

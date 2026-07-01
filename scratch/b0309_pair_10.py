import json
import os
import yaml

topics = {
    "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA": {
        "yaml_data": {
            "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
            "titulo": "Inecuaciones con Valor Absoluto y Constante Negativa",
            "objetivo": "Resolver inecuaciones con valor absoluto que están igualadas o comparadas a una constante negativa.",
            "introduccion": "El valor absoluto de cualquier número real o expresión matemática siempre es un número no negativo (es decir, mayor o igual a cero). Por tanto, cuando nos encontramos con una inecuación donde un valor absoluto se compara con una cantidad estrictamente negativa, las soluciones adquieren propiedades particulares y directas.",
            "resumen": r"Dado que el valor absoluto nunca es negativo, una inecuación de la forma $|x| < -k$ (con $k > 0$) no tiene solución, mientras que $|x| > -k$ siempre es cierta para cualquier número real dentro del dominio de la expresión.",
            "explicacion": r"""### Definición formal
Sea $f(x)$ una expresión algebraica y $k$ una constante real tal que $k < 0$. Para inecuaciones de la forma $|f(x)| < k$ o $|f(x)| \leq k$, el conjunto solución es vacío ($\emptyset$). Para inecuaciones de la forma $|f(x)| > k$ o $|f(x)| \geq k$, el conjunto solución corresponde al dominio completo de $f(x)$ (generalmente, los números reales $\mathbb{R}$).

### Desarrollo didáctico
Al tratar con inecuaciones que contienen valor absoluto, es fundamental analizar el signo de la constante con la cual se está comparando. Sabemos por propiedad fundamental que para cualquier número real $A$, se cumple que $|A| \geq 0$.

Si nos enfrentamos a la inecuación $|x-3| < -2$, estamos buscando un número tal que su valor absoluto sea menor que $-2$. Sin embargo, como el valor absoluto de cualquier cantidad mínima es $0$, jamás podrá ser menor que un número negativo. En este escenario, deducimos inmediatamente que no existen valores para $x$ que satisfagan la inecuación.

Por el contrario, si la inecuación es $|x-3| > -2$, nos preguntamos para qué valores el valor absoluto es mayor que un número negativo. Como el valor absoluto es siempre mayor o igual a cero, cualquier valor que tome $x$ generará una cantidad no negativa, que por definición siempre será estrictamente mayor que $-2$. Así, la inecuación se cumple para todos los números reales.""",
            "procedimiento": [
                "Identificar la inecuación que presenta un valor absoluto en un miembro de la desigualdad.",
                "Aislar la expresión del valor absoluto en un lado de la desigualdad.",
                "Verificar que el otro lado de la desigualdad sea una constante estrictamente negativa.",
                r"Si la desigualdad es menor o menor o igual, establecer que la solución es el conjunto vacío ($\emptyset$).",
                r"Si la desigualdad es mayor o mayor o igual, establecer que la solución abarca todos los números reales ($\mathbb{R}$) que están en el dominio de la expresión interior."
            ],
            "ejemplos": [
                {
                    "titulo": "Desigualdad del tipo menor estricto",
                    "enunciado": r"Resuelve la inecuación $|2x + 1| < -5$.",
                    "solucion_pasos": [
                        r"Observamos que la expresión del valor absoluto, $|2x + 1|$, está aislada.",
                        "Notamos que la constante a la derecha es $-5$, un número negativo.",
                        "Como el valor absoluto no puede ser negativo, nunca será menor que $-5$.",
                        r"Concluimos que no hay números reales que cumplan esta inecuación. La solución es el conjunto vacío ($\emptyset$)."
                    ]
                },
                {
                    "titulo": "Desigualdad del tipo mayor o igual",
                    "enunciado": r"Determina el conjunto solución para la inecuación $|3x - 4| \geq -2$.",
                    "solucion_pasos": [
                        r"El valor absoluto $|3x - 4|$ ya está aislado en un lado.",
                        "Al otro lado tenemos la constante negativa $-2$.",
                        "El valor absoluto siempre es mayor o igual a cero para cualquier valor real de $x$.",
                        "Dado que $0$ y cualquier número positivo son mayores que $-2$, la desigualdad es siempre cierta.",
                        r"La solución es el conjunto de todos los números reales ($\mathbb{R}$)."
                    ]
                },
                {
                    "titulo": r"¿Tiene solución $|x + 7| < -1$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "El valor absoluto debe ser mayor o igual a cero.",
                        "Un número no negativo nunca puede ser menor que un número estrictamente negativo ($-1$).",
                        "Por lo tanto, no hay solución."
                    ]
                },
                {
                    "titulo": r"¿Es cierto que cualquier número real satisface $|5 - x| > -10$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        "La inecuación plantea que un valor absoluto debe ser mayor a un número negativo.",
                        "El valor absoluto genera siempre valores mayores o iguales a cero.",
                        "Cualquier cantidad no negativa es, por definición, mayor que $-10$.",
                        "Luego, todos los reales son solución."
                    ]
                }
            ],
            "errores_frecuentes": [
                r"Creer que se debe separar la inecuación en dos casos ($2x < -5$ y $2x > 5$) omitiendo el análisis del signo de la constante.",
                "Suponer que la solución siempre es el conjunto vacío sin revisar si el signo de la desigualdad es mayor o menor.",
                r"Afirmar que si $|x| > -3$, entonces $x > -3$ descartando valores negativos para $x$.",
                "Pensar que la expresión dentro del valor absoluto puede volverse negativa, lo que compensa la desigualdad.",
                "Olvidar que un valor absoluto puede ser exactamente cero y evaluar erróneamente inecuaciones con constantes negativas."
            ],
            "fuente": "Generado para ProfeOnline",
            "estado": "publicado"
        },
        "jsonl_data": [
            {
                "stable_id": "ALG-GEN-VACN-1",
                "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
                "tipo": "conceptual",
                "nivel": 1,
                "dificultad": "facil",
                "pregunta": r"Si $k$ es una constante negativa, ¿cuál es siempre el conjunto solución para la inecuación $|x| < k$?",
                "opciones": [
                    "Todos los números reales.",
                    "El conjunto vacío.",
                    "Solo números negativos.",
                    "Solo el cero."
                ],
                "respuesta_correcta": "El conjunto vacío.",
                "explicacion": "El valor absoluto de cualquier número es siempre mayor o igual a cero, por lo tanto, nunca puede ser estrictamente menor que un número negativo. Por esto, la inecuación carece de solución."
            },
            {
                "stable_id": "ALG-GEN-VACN-2",
                "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
                "tipo": "conceptual",
                "nivel": 1,
                "dificultad": "facil",
                "pregunta": r"¿Qué ocurre si comparamos el valor absoluto de una expresión real cualquiera y comprobamos si es mayor que un valor negativo?",
                "opciones": [
                    "Solo se cumple para valores positivos de la expresión.",
                    "La desigualdad es siempre cierta.",
                    "La desigualdad es siempre falsa.",
                    "Depende de los coeficientes de la expresión."
                ],
                "respuesta_correcta": "La desigualdad es siempre cierta.",
                "explicacion": r"Dado que el valor absoluto nunca toma valores negativos, cualquier resultado de $|f(x)|$ será mayor o igual a $0$. Esto garantiza que siempre será mayor a cualquier constante negativa."
            },
            {
                "stable_id": "ALG-GEN-VACN-3",
                "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
                "tipo": "conceptual",
                "nivel": 1,
                "dificultad": "facil",
                "pregunta": "En la resolución de inecuaciones de valor absoluto con constantes negativas, ¿qué paso procedimental es innecesario?",
                "opciones": [
                    "Analizar la dirección de la desigualdad (mayor o menor).",
                    "Separar la inecuación en dos casos distintos para resolverla algebraicamante.",
                    "Verificar si la constante en el lado derecho es negativa.",
                    "Comprobar que el valor absoluto se encuentre aislado."
                ],
                "respuesta_correcta": "Separar la inecuación en dos casos distintos para resolverla algebraicamante.",
                "explicacion": "A diferencia de las inecuaciones con constantes positivas, aquí basta con observar el signo de la constante y la desigualdad, por lo que el desglose algebraico en dos casos no procede."
            },
            {
                "stable_id": "ALG-GEN-VACN-4",
                "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
                "tipo": "reconocimiento",
                "nivel": 1,
                "dificultad": "facil",
                "pregunta": "¿Cuál de las siguientes inecuaciones ilustra el caso de un valor absoluto comparado con una constante negativa?",
                "opciones": [
                    r"$|-3x + 1| \leq 0$",
                    r"$|x + 2| > -4$",
                    r"$-|x - 5| < 2$",
                    r"$|2x| < 4$"
                ],
                "respuesta_correcta": r"$|x + 2| > -4$",
                "explicacion": r"Esta inecuación muestra un valor absoluto debidamente aislado ($|x+2|$) siendo comparado (en este caso, mayor) con un número estrictamente negativo ($-4$)."
            },
            {
                "stable_id": "ALG-GEN-VACN-5",
                "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "dificultad": "media",
                "pregunta": r"Para la inecuación $|4x - 1| \leq -7$, el conjunto solución es el conjunto vacío.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Verdadero",
                "explicacion": "Como el valor absoluto no puede ser negativo, nunca será menor o igual a $-7$, por lo que no hay solución y el conjunto solución es vacío."
            },
            {
                "stable_id": "ALG-GEN-VACN-6",
                "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "dificultad": "media",
                "pregunta": r"La inecuación $|-5x + 3| > -1$ se satisface únicamente para valores positivos de $x$.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Falso",
                "explicacion": r"La inecuación $|f(x)| > -1$ se cumple para cualquier número real que pertenezca al dominio de la expresión, ya que el valor absoluto siempre produce un número no negativo, y cualquier número $\geq 0$ es mayor que $-1$."
            },
            {
                "stable_id": "ALG-GEN-VACN-7",
                "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "dificultad": "media",
                "pregunta": r"La inecuación $|x/2 + 5| < -1/2$ no tiene solución real.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Verdadero",
                "explicacion": r"El valor absoluto de cualquier expresión siempre es $\geq 0$. Un número no negativo nunca puede ser menor que un valor negativo ($-1/2$)."
            },
            {
                "stable_id": "ALG-GEN-VACN-8",
                "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
                "tipo": "tipo_paes",
                "nivel": 3,
                "dificultad": "dificil",
                "paes_style": True,
                "pregunta": r"Determina el conjunto solución de la inecuación $|x - 5| + 3 < 1$.",
                "opciones": [
                    r"$x \in (3, 7)$",
                    r"$\emptyset$",
                    r"$\mathbb{R}$",
                    r"$x \in (-\infty, 3) \cup (7, \infty)$"
                ],
                "respuesta_correcta": r"$\emptyset$",
                "explicacion": r"Primero restamos $3$ a ambos lados para aislar el valor absoluto: $|x - 5| < -2$. Al tener un valor absoluto menor a un número negativo, deducimos de inmediato que el conjunto solución es vacío ($\emptyset$)."
            },
            {
                "stable_id": "ALG-GEN-VACN-9",
                "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
                "tipo": "tipo_paes",
                "nivel": 3,
                "dificultad": "dificil",
                "paes_style": True,
                "pregunta": r"Se sabe que para cierta constante $c$, la inecuación $|2x + 4| \geq c$ tiene como conjunto solución a todos los números reales. ¿Qué condición debe cumplir $c$ obligatoriamente?",
                "opciones": [
                    r"$c > 0$",
                    r"$c = 4$",
                    r"$c \leq 0$",
                    r"$c = 2$"
                ],
                "respuesta_correcta": r"$c \leq 0$",
                "explicacion": r"Para que la solución incluya a todos los números reales, el valor absoluto debe ser mayor o igual a un número que no restrinja ningún valor de la recta real. Sabiendo que el valor absoluto siempre resulta en $0$ o valores positivos, si $c$ es negativo o cero, cualquier número real cumplirá con $|2x + 4| \geq c$. Por consiguiente, $c \leq 0$."
            },
            {
                "stable_id": "ALG-GEN-VACN-10",
                "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.CONSTANTE_NEGATIVA",
                "tipo": "tipo_paes",
                "nivel": 3,
                "dificultad": "dificil",
                "paes_style": True,
                "pregunta": r"Si sumamos $4$ al conjunto solución de $|3x - 1| > -5$, ¿cuál es el nuevo conjunto de valores?",
                "opciones": [
                    r"Todos los números reales $\mathbb{R}$.",
                    "Solo los números mayores a $4$.",
                    "Solo los números entre $-1$ y $9$.",
                    "El conjunto vacío."
                ],
                "respuesta_correcta": r"Todos los números reales $\mathbb{R}$.",
                "explicacion": r"El conjunto solución de $|3x - 1| > -5$ es $\mathbb{R}$, puesto que cualquier valor absoluto siempre es mayor que $-5$. Si al conjunto de todos los reales se le suma una constante (traslación), el conjunto resultante sigue siendo todos los números reales, $\mathbb{R}$."
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS": {
        "yaml_data": {
            "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
            "titulo": "Inecuaciones Lineales con Incógnita en Ambos Lados",
            "objetivo": "Resolver inecuaciones lineales agrupando términos semejantes cuando la variable aparece en ambos lados de la desigualdad.",
            "introduccion": "Muchas veces, las expresiones matemáticas involucran variables distribuidas en distintos miembros de una ecuación o inecuación. Para encontrar la solución, es necesario reordenar estos términos empleando las operaciones básicas, manteniendo las propiedades fundamentales de las desigualdades.",
            "resumen": "Para resolver una inecuación lineal con incógnitas en ambos lados, se agrupan los términos con la variable de un lado y los términos constantes del otro, utilizando operaciones inversas y recordando invertir el signo de desigualdad si se multiplica o divide por un número negativo.",
            "explicacion": r"""### Definición formal
Una inecuación lineal con la incógnita en ambos lados es de la forma $ax + b < cx + d$, donde $a$, $b$, $c$ y $d$ son constantes reales con $a \neq c$, y el símbolo $<$ puede ser sustituido por $\leq$, $>$, o $\geq$. Su resolución implica la aplicación sistemática de propiedades de las desigualdades: si se suma o resta un mismo término a ambos lados, la desigualdad se mantiene.

### Desarrollo didáctico
Al enfrentar inecuaciones como $3x - 5 \geq x + 7$, el principio rector es juntar los términos que contienen $x$ y separarlos de los números puros.

Podemos optar por mover $x$ hacia el lado izquierdo, restando $x$ a ambos lados de la inecuación: $3x - x - 5 \geq 7$. Esto simplifica a $2x - 5 \geq 7$. A continuación, agrupamos las constantes sumando $5$ en ambos miembros: $2x \geq 12$. Por último, para despejar $x$, dividimos entre $2$. Como $2$ es positivo, la dirección de la desigualdad no cambia: $x \geq 6$.

Es relevante notar que si decidimos agrupar los términos de manera que el coeficiente final de la variable resulte negativo (por ejemplo, operando hacia el lado derecho para ciertas inecuaciones), al final deberemos dividir o multiplicar por dicho coeficiente. En ese caso, la regla fundamental de las desigualdades dictamina que debemos invertir el signo de la desigualdad. Por ello, a menudo resulta estratégico agrupar los términos variables donde su coeficiente resulte positivo para evitar errores en el último paso.""",
            "procedimiento": [
                "Utilizar la propiedad distributiva, si es necesario, para eliminar paréntesis en ambos lados.",
                "Agrupar todos los términos que contengan la incógnita en un lado de la desigualdad sumando o restando términos a ambos lados.",
                "Agrupar todos los términos constantes en el otro lado de la desigualdad de la misma manera.",
                r"Reducir términos semejantes para obtener una inecuación de la forma $Ax < B$ o similar.",
                "Despejar la incógnita multiplicando o dividiendo. Si se multiplica o divide por un número negativo, invertir el sentido de la desigualdad."
            ],
            "ejemplos": [
                {
                    "titulo": "Resolución directa con variable positiva",
                    "enunciado": r"Resuelve la inecuación $5x - 4 < 2x + 11$.",
                    "solucion_pasos": [
                        r"Restamos $2x$ a ambos lados para agrupar variables: $5x - 2x - 4 < 11$.",
                        r"Simplificamos los términos: $3x - 4 < 11$.",
                        r"Sumamos $4$ a ambos lados: $3x < 11 + 4$.",
                        r"Simplificamos: $3x < 15$.",
                        r"Dividimos por $3$ (que es positivo, no se invierte la desigualdad): $x < 5$."
                    ]
                },
                {
                    "titulo": "Agrupamiento que resulta en coeficiente negativo",
                    "enunciado": r"Resuelve la inecuación $2x + 9 \geq 6x - 7$.",
                    "solucion_pasos": [
                        r"Restamos $6x$ de ambos lados: $2x - 6x + 9 \geq -7$.",
                        r"Simplificamos a $-4x + 9 \geq -7$.",
                        r"Restamos $9$ de ambos lados: $-4x \geq -7 - 9$, quedando $-4x \geq -16$.",
                        r"Dividimos por $-4$. Como es negativo, invertimos el signo de $\geq$ a $\leq$.",
                        r"La solución es $x \leq 4$."
                    ]
                },
                {
                    "titulo": r"¿Es $x > -2$ la solución de $x - 3 < 3x + 1$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        r"Restamos $x$ a ambos lados: $-3 < 2x + 1$.",
                        r"Restamos $1$ a ambos lados: $-4 < 2x$.",
                        r"Dividimos entre $2$: $-2 < x$.",
                        r"Esto es equivalente a $x > -2$. La afirmación es correcta."
                    ]
                },
                {
                    "titulo": r"¿El intervalo solución de $4 - 2x \geq 8 - 4x$ incluye el número $-1$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        r"Sumamos $4x$ a ambos lados: $4 - 2x + 4x \geq 8$.",
                        r"Simplificamos: $4 + 2x \geq 8$.",
                        r"Restamos $4$ a ambos lados: $2x \geq 4$.",
                        r"Dividimos entre $2$: $x \geq 2$.",
                        r"El número $-1$ no es mayor o igual a $2$, por lo que no pertenece al conjunto solución."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Agrupar erróneamente los términos sin cambiar los signos al moverlos al otro lado de la inecuación.",
                "Olvidar invertir el signo de la desigualdad cuando se divide por un coeficiente negativo que acompaña a la variable.",
                "Sumar los coeficientes de un mismo lado pero tratarlos como si se estuvieran moviendo, duplicando la operación.",
                "Confundir un coeficiente negativo con una constante, y sumarlo en lugar de dividir al despejar la incógnita.",
                "Invertir el símbolo de desigualdad al dividir por una constante positiva si el número en el lado opuesto era negativo."
            ],
            "fuente": "Generado para ProfeOnline",
            "estado": "publicado"
        },
        "jsonl_data": [
            {
                "stable_id": "ALG-GEN-LIAL-1",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
                "tipo": "conceptual",
                "nivel": 1,
                "dificultad": "facil",
                "pregunta": "¿Cuál es el objetivo principal al resolver una inecuación lineal con incógnitas en ambos lados?",
                "opciones": [
                    "Aislar la incógnita en uno de los lados y agrupar las constantes en el otro.",
                    "Igualar ambos lados a cero para luego factorizar.",
                    "Multiplicar toda la inecuación por el denominador común de los coeficientes.",
                    "Elevar al cuadrado ambos lados para eliminar signos negativos."
                ],
                "respuesta_correcta": "Aislar la incógnita en uno de los lados y agrupar las constantes en el otro.",
                "explicacion": "El principio de resolución es reducir la inecuación agrupando los términos semejantes (variables por un lado, constantes por otro) hasta dejar la incógnita despejada."
            },
            {
                "stable_id": "ALG-GEN-LIAL-2",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
                "tipo": "conceptual",
                "nivel": 1,
                "dificultad": "facil",
                "pregunta": "Si al agrupar términos en una inecuación el coeficiente de la variable resulta ser negativo, al momento de dividir por dicho coeficiente para despejar, ¿qué regla debe aplicarse?",
                "opciones": [
                    "Se debe mantener el signo de desigualdad igual.",
                    "Se debe invertir el sentido de la desigualdad.",
                    "La inecuación se transforma en una ecuación (igualdad).",
                    "El coeficiente pasa a ser positivo, pero la variable queda negativa."
                ],
                "respuesta_correcta": "Se debe invertir el sentido de la desigualdad.",
                "explicacion": "Una propiedad fundamental de las desigualdades dicta que multiplicar o dividir ambos miembros por un número negativo requiere invertir el símbolo de la desigualdad para conservar la relación correcta."
            },
            {
                "stable_id": "ALG-GEN-LIAL-3",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
                "tipo": "conceptual",
                "nivel": 1,
                "dificultad": "facil",
                "pregunta": r"En la inecuación $ax + b < cx + d$, si pasamos $cx$ al lado izquierdo y resulta $(a-c)x + b < d$, ¿qué operación hicimos realmente en ambos miembros?",
                "opciones": [
                    r"Restar $cx$ a ambos lados de la inecuación.",
                    r"Sumar $cx$ a ambos lados de la inecuación.",
                    r"Dividir por $c$ ambos lados de la inecuación.",
                    r"Multiplicar por $x$ a ambos lados de la inecuación."
                ],
                "respuesta_correcta": r"Restar $cx$ a ambos lados de la inecuación.",
                "explicacion": "Por las propiedades aditivas, mover un término sumando a través del símbolo de desigualdad equivale a restarlo en ambos miembros."
            },
            {
                "stable_id": "ALG-GEN-LIAL-4",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
                "tipo": "reconocimiento",
                "nivel": 1,
                "dificultad": "facil",
                "pregunta": r"¿Qué expresión representa correctamente el siguiente paso tras restar $3x$ a ambos lados de la inecuación $7x - 2 > 3x + 10$?",
                "opciones": [
                    r"$4x - 2 > 10$",
                    r"$10x - 2 > 10$",
                    r"$4x > 12$",
                    r"$7x - 5x > 10$"
                ],
                "respuesta_correcta": r"$4x - 2 > 10$",
                "explicacion": r"Al restar $3x$ a $7x$ nos queda $4x$. El término constante $-2$ y el $10$ se mantienen inalterados en esta etapa inicial."
            },
            {
                "stable_id": "ALG-GEN-LIAL-5",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "dificultad": "media",
                "pregunta": r"La inecuación $5x - 3 \leq 2x + 9$ se resuelve como $x \leq 4$.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Verdadero",
                "explicacion": r"Agrupamos restando $2x$ y sumando $3$: $3x \leq 12$. Al dividir por $3$, obtenemos $x \leq 4$."
            },
            {
                "stable_id": "ALG-GEN-LIAL-6",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "dificultad": "media",
                "pregunta": r"El conjunto solución de $-3x + 5 > -5x + 1$ es $x > -2$.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Verdadero",
                "explicacion": r"Sumando $5x$ a ambos lados da $2x + 5 > 1$. Restando $5$, obtenemos $2x > -4$. Dividiendo por $2$, queda $x > -2$."
            },
            {
                "stable_id": "ALG-GEN-LIAL-7",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "dificultad": "media",
                "pregunta": r"Al resolver $x + 8 < 4x - 1$, la solución correcta es $x < 3$.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Falso",
                "explicacion": r"Restando $x$ en ambos lados y sumando $1$ resulta $9 < 3x$, o sea $3 < x$, que equivale a $x > 3$, no $x < 3$."
            },
            {
                "stable_id": "ALG-GEN-LIAL-8",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
                "tipo": "tipo_paes",
                "nivel": 3,
                "dificultad": "dificil",
                "paes_style": True,
                "pregunta": "Para qué conjunto de números reales se satisface que la mitad del número más $4$ es estrictamente mayor que el triple del número disminuido en $1$?",
                "opciones": [
                    r"$x < 2$",
                    r"$x > 2$",
                    r"$x < -2$",
                    r"$x > 5/2$"
                ],
                "respuesta_correcta": r"$x < 2$",
                "explicacion": r"Planteamos la inecuación: $\frac{x}{2} + 4 > 3x - 1$. Multiplicamos por $2$ para eliminar fracciones: $x + 8 > 6x - 2$. Restamos $x$ a ambos lados: $8 > 5x - 2$. Sumamos $2$: $10 > 5x$. Dividiendo por $5$, se obtiene $2 > x$, lo que es equivalente a $x < 2$."
            },
            {
                "stable_id": "ALG-GEN-LIAL-9",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
                "tipo": "tipo_paes",
                "nivel": 3,
                "dificultad": "dificil",
                "paes_style": True,
                "pregunta": r"Una empresa fabrica dos productos A y B. El costo en dólares de producir $x$ unidades de A es $C_A = 12x + 50$, y el costo para B es $C_B = 15x - 10$. ¿Para qué cantidad mínima de unidades $x$ (con $x \in \mathbb{Z}^{+}$) el costo del producto B supera al costo del producto A?",
                "opciones": [
                    r"$20$ unidades",
                    r"$21$ unidades",
                    r"$22$ unidades",
                    r"$19$ unidades"
                ],
                "respuesta_correcta": r"$21$ unidades",
                "explicacion": r"Buscamos cuando $C_B > C_A$, es decir, $15x - 10 > 12x + 50$. Agrupamos las $x$ restando $12x$: $3x - 10 > 50$. Sumamos $10$: $3x > 60$. Dividimos por $3$: $x > 20$. Dado que $x$ debe ser un número entero y estrictamente mayor que $20$, la cantidad mínima es $21$ unidades."
            },
            {
                "stable_id": "ALG-GEN-LIAL-10",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.INCOGNITA_AMBOS_LADOS",
                "tipo": "tipo_paes",
                "nivel": 3,
                "dificultad": "dificil",
                "paes_style": True,
                "pregunta": r"Si $m$ y $n$ son constantes positivas con $m > n$, ¿cuál es la solución de la inecuación $mx - p < nx + q$?",
                "opciones": [
                    r"$x < \frac{q + p}{m - n}$",
                    r"$x > \frac{q + p}{m - n}$",
                    r"$x < \frac{q - p}{m - n}$",
                    r"$x > \frac{p - q}{m + n}$"
                ],
                "respuesta_correcta": r"$x < \frac{q + p}{m - n}$",
                "explicacion": r"Restamos $nx$ a ambos lados: $mx - nx - p < q$. Factorizamos: $x(m - n) - p < q$. Sumamos $p$: $x(m - n) < q + p$. Ya que nos indican que $m > n$, el factor $(m - n)$ es positivo. Al dividir ambos miembros por un número positivo, la desigualdad no se invierte. El resultado final es $x < \frac{q + p}{m - n}$."
            }
        ]
    }
}

if __name__ == "__main__":
    for semantic_id, content in topics.items():
        # Crear directorios
        parts = semantic_id.split('.')
        subject, area, subtopic, subsubtopic = parts[0], parts[1], parts[2], parts[3]
        base_dir = f"docs/curriculum/{subject}/{area}/{subtopic}/{subsubtopic}"
        os.makedirs(base_dir, exist_ok=True)

        # Guardar yaml
        yaml_content = yaml.dump(content["yaml_data"], allow_unicode=True, sort_keys=False)
        with open(f"{base_dir}/contenido.yaml", "w", encoding="utf-8") as f:
            f.write(yaml_content)

        # Guardar jsonl
        with open(f"{base_dir}/ejercicios.jsonl", "w", encoding="utf-8") as f:
            for exercise in content["jsonl_data"]:
                f.write(json.dumps(exercise, ensure_ascii=False) + "\n")
    print("Files successfully generated.")

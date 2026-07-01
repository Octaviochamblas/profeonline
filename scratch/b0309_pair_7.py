import os
import json
import yaml

topics = {
    "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.MENOR_IGUAL_POSITIVO": {
        "yaml": {
            "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.MENOR_IGUAL_POSITIVO",
            "titulo": "Inecuaciones con Valor Absoluto: Caso Menor y Menor o Igual",
            "objetivo": r"Resolver inecuaciones con valor absoluto de la forma $|x| < a$ y $|x| \le a$, con $a > 0$.",
            "introduccion": "El valor absoluto de un número representa su distancia al cero en la recta numérica. Cuando decimos que el valor absoluto de una cantidad es menor o igual que un número positivo, estamos limitando qué tan lejos puede estar esa cantidad respecto al cero.",
            "resumen": r"Para resolver inecuaciones del tipo $|X| \le a$ (con $a > 0$), se aplica la propiedad que lo transforma en un sistema de dos inecuaciones simultáneas: $-a \le X \le a$.",
            "explicacion": r"""### Definición formal
Sea $x \in \mathbb{R}$ y $a \in \mathbb{R}$ tal que $a > 0$.
La inecuación con valor absoluto $|x| \le a$ es equivalente a la doble inecuación $-a \le x \le a$.
De forma análoga, $|x| < a \iff -a < x < a$.
El conjunto solución corresponde al intervalo $[-a, a]$ para la desigualdad débil, y $(-a, a)$ para la estricta.

### Desarrollo didáctico
Imagina que estás en el centro de una ciudad (el cero) y te dicen que no puedes alejarte más de $5$ kilómetros. Esto significa que puedes caminar hasta $5$ km a la derecha (positivo) o hasta $5$ km a la izquierda (negativo). En lenguaje matemático, si tu posición es $x$, entonces la distancia al centro es $|x|$, y la restricción es $|x| \le 5$.
Por lo tanto, tu posición real $x$ debe estar entre $-5$ y $5$, es decir, $-5 \le x \le 5$.
Si dentro del valor absoluto hay una expresión más compleja, como $|2x - 1| \le 3$, el principio es el mismo: lo que está adentro debe quedar atrapado entre $-3$ y $3$. Luego, se despeja la variable $x$ de esa doble desigualdad, sumando o dividiendo simultáneamente en las tres partes.""",
            "procedimiento": [
                r"Verificar que la inecuación esté en la forma $|X| \le a$ o $|X| < a$, y que la constante $a$ sea un número real positivo.",
                r"Aplicar la propiedad del valor absoluto para transformarla en una doble desigualdad: $-a \le X \le a$ (o $-a < X < a$).",
                r"Despejar la variable incógnita del término central, aplicando las operaciones inversas en todas las partes de la desigualdad al mismo tiempo.",
                r"Expresar el conjunto solución en forma de intervalo y/o gráfico."
            ],
            "ejemplos": [
                {
                    "titulo": "Inecuación básica con restricción estricta",
                    "enunciado": r"Resuelve la inecuación $|x - 3| < 4$.",
                    "solucion_pasos": [
                        r"Aplicamos la propiedad para $a = 4$: $-4 < x - 3 < 4$.",
                        r"Sumamos $3$ a todas las partes para despejar $x$: $-4 + 3 < x < 4 + 3$.",
                        r"Simplificamos obteniendo: $-1 < x < 7$.",
                        r"El conjunto solución es el intervalo $(-1, 7)$."
                    ]
                },
                {
                    "titulo": "Inecuación con coeficiente acompañando a la variable",
                    "enunciado": r"Encuentra el conjunto solución de $|2x + 1| \le 5$.",
                    "solucion_pasos": [
                        r"Utilizamos la propiedad: $-5 \le 2x + 1 \le 5$.",
                        r"Restamos $1$ en los tres miembros: $-6 \le 2x \le 4$.",
                        r"Dividimos por $2$ (positivo, por lo que se mantienen los sentidos de las desigualdades): $-3 \le x \le 2$.",
                        r"La solución es el intervalo $[-3, 2]$."
                    ]
                },
                {
                    "titulo": r"¿El número 0 pertenece al conjunto solución de $|3x - 2| \le 4$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        r"Al reemplazar $x = 0$ en la inecuación $|3x - 2| \le 4$, evaluamos la expresión.",
                        r"Calculamos: $|3(0) - 2| = |-2| = 2$.",
                        r"Como $2 \le 4$ es una afirmación verdadera, el $0$ sí pertenece al conjunto solución."
                    ]
                },
                {
                    "titulo": r"¿La solución de $|x + 2| \le -1$ es un intervalo acotado?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        r"Observamos que el valor absoluto de cualquier expresión siempre es mayor o igual a cero.",
                        r"La inecuación plantea que un valor absoluto sea menor o igual a un número negativo ($-1$).",
                        r"Esto es imposible en los números reales, por lo que el conjunto solución es vacío ($\emptyset$), no un intervalo acotado."
                    ]
                }
            ],
            "errores_frecuentes": [
                r"Asumir que $|x - 2| \le 3$ implica solamente que $x - 2 \le 3$, olvidando la restricción inferior de $-3$.",
                r"Escribir la solución de $|x| \le 4$ como $x \ge -4 \cup x \le 4$ en lugar de una intersección ($-4 \le x \le 4$).",
                r"Creer que $|-x| \le 5$ significa que $x \le -5$ en vez de $-5 \le x \le 5$.",
                r"Al resolver $-2 \le -x \le 2$, multiplicar por $-1$ y no invertir el sentido de las desigualdades.",
                r"Aplicar la propiedad $-a \le X \le a$ cuando $a$ es negativo, obteniendo intervalos inconsistentes en lugar de determinar que la solución es vacía."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "IVAMEP-GEN-CONCEPTUAL-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": r"Si $a$ es un número real positivo, ¿cuál de las siguientes expresiones es lógicamente equivalente a $|x| \le a$?",
                "opciones": [
                    r"$-a \le x \le a$",
                    r"$x \le -a$ o $x \ge a$",
                    r"$x \le a$",
                    r"$-a \le x$"
                ],
                "respuesta_correcta": 0,
                "explicacion": r"Por definición de valor absoluto, si la distancia de un número al cero es menor o igual a $a$ (con $a > 0$), entonces dicho número debe estar comprendido entre $-a$ y $a$, incluyendo ambos extremos."
            },
            {
                "stable_id": "IVAMEP-GEN-CONCEPTUAL-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": r"¿Qué representa geométricamente la inecuación $|x - c| < r$ en la recta numérica real?",
                "opciones": [
                    r"Los puntos cuya distancia al origen es menor a $r$.",
                    r"Los puntos cuya distancia al punto $c$ es mayor a $r$.",
                    r"Los puntos cuya distancia al punto $c$ es estrictamente menor a $r$.",
                    r"Los puntos cuya distancia al origen es $c$ y límite $r$."
                ],
                "respuesta_correcta": 2,
                "explicacion": r"La expresión $|x - c|$ representa la distancia entre $x$ y $c$. Por tanto, la inecuación denota a todos los números $x$ que están a una distancia menor a $r$ respecto del número $c$."
            },
            {
                "stable_id": "IVAMEP-GEN-CONCEPTUAL-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": r"¿Cuál es el conjunto solución de la inecuación $|x| \le 0$?",
                "opciones": [
                    r"El intervalo $[0, \infty)$",
                    r"El conjunto vacío $\emptyset$",
                    r"Únicamente el valor $0$",
                    r"Todos los números reales $\mathbb{R}$"
                ],
                "respuesta_correcta": 2,
                "explicacion": r"Como el valor absoluto no puede ser negativo, la única forma de cumplir $|x| \le 0$ es que sea exactamente igual a $0$. Esto ocurre solo si $x = 0$."
            },
            {
                "stable_id": "IVAMEP-GEN-RECONOC-1",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": r"Identifica cuál de las siguientes inecuaciones corresponde al caso donde se aplica la propiedad de acotación entre un negativo y un positivo, $-a < X < a$.",
                "opciones": [
                    r"$|2x + 1| > 4$",
                    r"$|5x - 3| < 2$",
                    r"$-|x + 1| > -3$",
                    r"$|x| = 5$"
                ],
                "respuesta_correcta": 1,
                "explicacion": r"La inecuación $|5x - 3| < 2$ tiene la forma $|X| < a$ con $a > 0$, lo que permite aplicar directamente la propiedad $-2 < 5x - 3 < 2$. (Notar que $-|x+1|>-3$ implica $|x+1|<3$, pero requiere un paso algebraico previo)."
            },
            {
                "stable_id": "IVAMEP-GEN-PROCBAS-1",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"La solución de la inecuación $|x - 5| \le 2$ es el intervalo $[3, 7]$.",
                "respuesta_correcta": True,
                "explicacion": r"Al aplicar la propiedad, se obtiene $-2 \le x - 5 \le 2$. Sumando $5$ en todas las partes se llega a $3 \le x \le 7$, lo cual corresponde al intervalo $[3, 7]$."
            },
            {
                "stable_id": "IVAMEP-GEN-PROCBAS-2",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"El conjunto solución de $|3x| < 9$ es $(-3, 3]$.",
                "respuesta_correcta": False,
                "explicacion": r"La desigualdad es estricta ($<$), por lo tanto los extremos no se incluyen. Al resolver se obtiene $-9 < 3x < 9 \implies -3 < x < 3$. El intervalo correcto es $(-3, 3)$ abierto en ambos lados."
            },
            {
                "stable_id": "IVAMEP-GEN-PROCBAS-3",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"La inecuación $|2 - x| \le 4$ equivale a $-2 \le x \le 6$.",
                "respuesta_correcta": True,
                "explicacion": r"Resolviendo: $-4 \le 2 - x \le 4$. Restando $2$: $-6 \le -x \le 2$. Multiplicando por $-1$ e invirtiendo las desigualdades: $6 \ge x \ge -2$, que se reordena como $-2 \le x \le 6$."
            },
            {
                "stable_id": "IVAMEP-GEN-PAES-1",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Una fábrica produce tornillos cuya longitud ideal es de $50$ mm. Para pasar el control de calidad, la diferencia entre la longitud real $L$ y la ideal no debe exceder los $0,5$ mm. ¿Cuál de los siguientes intervalos representa las longitudes aceptables para los tornillos?",
                "opciones": [
                    r"$[49.5, 50.5]$",
                    r"$(49.5, 50.5)$",
                    r"$[49.0, 51.0]$",
                    r"$[50.0, 50.5]$"
                ],
                "respuesta_correcta": 0,
                "explicacion": r"La condición plantea que $|L - 50| \le 0,5$. Resolviendo: $-0,5 \le L - 50 \le 0,5$. Sumando $50$ obtenemos $49,5 \le L \le 50,5$. El intervalo es cerrado porque el error 'no debe exceder' (es menor o igual)."
            },
            {
                "stable_id": "IVAMEP-GEN-PAES-2",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Se define el conjunto $A$ como el conjunto de todos los números reales $x$ que satisfacen $|3x - 1| \le 8$. ¿Cuántos números enteros pertenecen al conjunto $A$?",
                "opciones": [
                    r"$6$",
                    r"$5$",
                    r"$4$",
                    r"$7$"
                ],
                "respuesta_correcta": 0,
                "explicacion": r"Resolvemos la inecuación: $-8 \le 3x - 1 \le 8$. Sumamos $1$: $-7 \le 3x \le 9$. Dividimos por $3$: $-\frac{7}{3} \le x \le 3$. En decimales, esto es aproximadamente $-2,33 \le x \le 3$. Los enteros en este rango son $-2, -1, 0, 1, 2, 3$, que son en total $6$ números enteros."
            },
            {
                "stable_id": "IVAMEP-GEN-PAES-3",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Si $m$ y $n$ son las soluciones de la ecuación $|x - 2| = 5$, con $m < n$. ¿Cuál es el conjunto solución de la inecuación $|x - m| < n$?",
                "opciones": [
                    r"$( -4, 10 )$",
                    r"$( -10, 4 )$",
                    r"$( -3, 11 )$",
                    r"$( -11, 3 )$"
                ],
                "respuesta_correcta": 1,
                "explicacion": r"Primero hallamos $m$ y $n$. De $|x - 2| = 5$ obtenemos $x - 2 = 5 \implies x = 7$ o $x - 2 = -5 \implies x = -3$. Como $m < n$, entonces $m = -3$ y $n = 7$. Sustituimos en la inecuación: $|x - (-3)| < 7 \implies |x + 3| < 7$. Resolvemos: $-7 < x + 3 < 7 \implies -10 < x < 4$. Esto corresponde al intervalo $(-10, 4)$."
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.COEFICIENTES_FRACCIONARIOS": {
        "yaml": {
            "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.COEFICIENTES_FRACCIONARIOS",
            "titulo": "Inecuaciones Lineales con Coeficientes Fraccionarios",
            "objetivo": "Resolver inecuaciones lineales de primer grado que contienen fracciones, utilizando el mínimo común múltiplo para simplificar los coeficientes.",
            "introduccion": "Cuando las inecuaciones involucran fracciones, el trabajo algebraico puede volverse tedioso si se operan los números racionales directamente. Afortunadamente, existe una estrategia para transformar la inecuación en una equivalente que solo tenga números enteros.",
            "resumen": "Para resolver inecuaciones con coeficientes fraccionarios de forma óptima, se recomienda multiplicar todos los términos por el Mínimo Común Múltiplo (MCM) de los denominadores, eliminando así las fracciones.",
            "explicacion": r"""### Definición formal
Sea una inecuación lineal que contiene términos de la forma $\frac{P(x)}{q}$ donde $q \in \mathbb{Z}^*$.
Para transformar la inecuación en otra equivalente con coeficientes enteros, se multiplica cada término por el $MCM$ (Mínimo Común Múltiplo) de todos los denominadores $q_i$ presentes.
Dado que el $MCM > 0$, la multiplicación no altera el sentido de la desigualdad.

### Desarrollo didáctico
Resolver inecuaciones con fracciones no es diferente a resolver las que tienen números enteros, pero operar fracciones directamente aumenta el riesgo de cometer errores.
Por ejemplo, en la inecuación $\frac{x}{2} + \frac{1}{3} > 1$, los denominadores son $2$ y $3$. El mínimo común múltiplo entre $2$ y $3$ es $6$.
Si multiplicamos ambos lados de la inecuación por $6$, garantizamos que cada fracción se simplificará hasta convertirse en un número entero.
Veamos: $6 \cdot (\frac{x}{2} + \frac{1}{3}) > 6 \cdot 1 \implies 3x + 2 > 6$.
Ahora, la inecuación $3x + 2 > 6$ es mucho más amigable de resolver. Recuerda siempre que al multiplicar todos los términos por un número positivo (como el MCM), el sentido del signo de desigualdad ($<, >, \le, \ge$) se mantiene intacto.""",
            "procedimiento": [
                r"Identificar todos los denominadores presentes en los términos fraccionarios de la inecuación.",
                r"Calcular el Mínimo Común Múltiplo (MCM) de dichos denominadores.",
                r"Multiplicar cada uno de los términos de la inecuación en ambos lados por el MCM calculado.",
                r"Simplificar las fracciones para obtener una inecuación equivalente con coeficientes enteros.",
                r"Agrupar y despejar la incógnita de forma convencional."
            ],
            "ejemplos": [
                {
                    "titulo": "Inecuación con dos denominadores distintos",
                    "enunciado": r"Resuelve la inecuación $\frac{x}{4} - 1 \le \frac{x}{6}$.",
                    "solucion_pasos": [
                        r"Identificamos los denominadores: $4$ y $6$. Su MCM es $12$.",
                        r"Multiplicamos cada término por $12$: $12 \cdot \frac{x}{4} - 12 \cdot 1 \le 12 \cdot \frac{x}{6}$.",
                        r"Simplificamos: $3x - 12 \le 2x$.",
                        r"Agrupamos las $x$ restando $2x$ y sumando $12$ en ambos lados: $x \le 12$."
                    ]
                },
                {
                    "titulo": "Múltiples fracciones y binomios en el numerador",
                    "enunciado": r"Encuentra el conjunto solución de $\frac{2x - 1}{3} > \frac{x + 1}{5}$.",
                    "solucion_pasos": [
                        r"Los denominadores son $3$ y $5$. El MCM es $15$.",
                        r"Multiplicamos ambos lados por $15$: $15 \cdot \left( \frac{2x - 1}{3} \right) > 15 \cdot \left( \frac{x + 1}{5} \right)$.",
                        r"Simplificamos los denominadores: $5(2x - 1) > 3(x + 1)$.",
                        r"Distribuimos: $10x - 5 > 3x + 3$.",
                        r"Despejamos $x$: $7x > 8 \implies x > \frac{8}{7}$."
                    ]
                },
                {
                    "titulo": "¿Se debe invertir la desigualdad si los denominadores son todos positivos?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        r"El MCM de un conjunto de denominadores se considera siempre como un número positivo.",
                        r"Al multiplicar ambos lados de una desigualdad por un valor estrictamente mayor que cero, la propiedad de orden establece que el sentido se preserva.",
                        r"Por lo tanto, la desigualdad mantiene su orientación original."
                    ]
                },
                {
                    "titulo": "¿Es estrictamente obligatorio utilizar el MCM para resolverla?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        r"El método de multiplicar por el MCM es una estrategia muy eficiente para simplificar el proceso y evitar operar con fracciones.",
                        r"Sin embargo, es posible resolverla sumando o restando algebraicamente las fracciones directamente, obteniendo común denominador.",
                        r"Ambos métodos son matemáticamente correctos y conducen al mismo conjunto solución."
                    ]
                }
            ],
            "errores_frecuentes": [
                r"Multiplicar solo los términos fraccionarios por el MCM, olvidando multiplicar los términos que son números enteros u otros polinomios enteros.",
                r"Calcular incorrectamente el MCM multiplicando siempre los denominadores ciegamente, lo que puede generar números muy grandes y propensos a error.",
                r"Al multiplicar y simplificar, no aplicar correctamente la propiedad distributiva cuando el numerador es un binomio.",
                r"Eliminar los denominadores sumando o restando términos, confundiendo las operaciones de multiplicación requeridas.",
                r"Invertir el signo de la desigualdad al multiplicar por el MCM positivo, asumiendo falsamente que eliminar denominadores altera el orden."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "ILCOEF-GEN-CONCEPTUAL-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": r"Para eliminar los denominadores en la inecuación $\frac{x}{4} + \frac{1}{6} < 2$, ¿por qué número es más conveniente multiplicar ambos lados de la desigualdad?",
                "opciones": [
                    r"Por $2$, ya que es divisor común de los denominadores.",
                    r"Por $10$, ya que es la suma de $4$ y $6$.",
                    r"Por $12$, ya que es el Mínimo Común Múltiplo de $4$ y $6$.",
                    r"Por $24$, pero cambiando el sentido de la desigualdad."
                ],
                "respuesta_correcta": 2,
                "explicacion": r"Para eliminar las fracciones con el menor factor posible y sin alterar los números enteros, se debe multiplicar por el mínimo común múltiplo (MCM) de los denominadores $4$ y $6$, que es $12$."
            },
            {
                "stable_id": "ILCOEF-GEN-CONCEPTUAL-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": r"Si multiplicamos todos los términos de una inecuación lineal por el Mínimo Común Múltiplo de sus denominadores (el cual es positivo), ¿qué sucede con el signo de la desigualdad?",
                "opciones": [
                    r"Se invierte, de menor pasa a ser mayor o viceversa.",
                    r"Se mantiene igual, sin sufrir alteraciones.",
                    r"Se convierte en una igualdad estricta.",
                    r"Se anula el signo y se resuelve como ecuación."
                ],
                "respuesta_correcta": 1,
                "explicacion": r"Una propiedad fundamental de las desigualdades indica que multiplicar o dividir todos los miembros de una inecuación por un número positivo preserva el sentido de la desigualdad original."
            },
            {
                "stable_id": "ILCOEF-GEN-CONCEPTUAL-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": r"¿Qué es incorrecto hacer al transformar la inecuación $\frac{x-2}{3} + 1 \ge \frac{x}{2}$?",
                "opciones": [
                    r"Multiplicar todos los términos, incluido el $1$, por $6$.",
                    r"Multiplicar solo los términos fraccionarios por $6$ dejando el $+1$ intacto.",
                    r"Distribuir el factor resultante en el binomio del numerador.",
                    r"Mantener el signo $\ge$ durante la multiplicación."
                ],
                "respuesta_correcta": 1,
                "explicacion": r"Al aplicar la propiedad de multiplicación, esta afecta a TODOS los términos de la desigualdad. Ignorar los términos que no son fraccionarios, como el $+1$, altera el valor de la expresión y produce resultados erróneos."
            },
            {
                "stable_id": "ILCOEF-GEN-RECONOC-1",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": r"Dada la inecuación $\frac{x}{5} - \frac{3}{10} > x$, ¿cuál es la ecuación equivalente correcta después de multiplicar por el MCM de los denominadores?",
                "opciones": [
                    r"$2x - 3 > x$",
                    r"$2x - 3 > 10x$",
                    r"$x - 3 > 10x$",
                    r"$2x - 3 < 10x$"
                ],
                "respuesta_correcta": 1,
                "explicacion": r"El MCM de $5$ y $10$ es $10$. Al multiplicar cada término por $10$, resulta $10(\frac{x}{5}) - 10(\frac{3}{10}) > 10(x) \implies 2x - 3 > 10x$. El sentido no se invierte."
            },
            {
                "stable_id": "ILCOEF-GEN-PROCBAS-1",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"La inecuación $\frac{x}{2} - \frac{1}{4} \le 0$ tiene como conjunto solución el intervalo $(-\infty, \frac{1}{2}]$.",
                "respuesta_correcta": True,
                "explicacion": r"Multiplicamos por el MCM, que es $4$: $4(\frac{x}{2}) - 4(\frac{1}{4}) \le 4(0) \implies 2x - 1 \le 0 \implies 2x \le 1 \implies x \le \frac{1}{2}$, que se corresponde con el intervalo dado."
            },
            {
                "stable_id": "ILCOEF-GEN-PROCBAS-2",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"El conjunto solución de la inecuación $\frac{3x - 1}{2} < x$ es $x > 1$.",
                "respuesta_correcta": False,
                "explicacion": r"Al multiplicar por $2$: $3x - 1 < 2x$. Restando $2x$ y sumando $1$: $x < 1$. El sentido era menor que, por lo que la afirmación de $x > 1$ es falsa."
            },
            {
                "stable_id": "ILCOEF-GEN-PROCBAS-3",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"Si $\frac{x}{3} + 2 \ge \frac{x}{2}$, entonces $x \le 12$.",
                "respuesta_correcta": True,
                "explicacion": r"Multiplicando todos los términos por $6$ (el MCM de $3$ y $2$): $2x + 12 \ge 3x$. Restamos $2x$ en ambos lados: $12 \ge x$, lo cual es equivalente a $x \le 12$."
            },
            {
                "stable_id": "ILCOEF-GEN-PAES-1",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Un estudiante tiene una nota $x$ en su primer control. Sabe que si suma la mitad de su nota con la tercera parte de esta, el resultado es menor o igual a $5$. ¿Cuál de los siguientes intervalos representa correctamente los valores posibles de su nota, sabiendo que $x > 0$?",
                "opciones": [
                    r"$(0, 6]$",
                    r"$(0, 5]$",
                    r"$(0, 8]$",
                    r"$(0, 10]$"
                ],
                "respuesta_correcta": 0,
                "explicacion": r"Planteamos la inecuación: $\frac{x}{2} + \frac{x}{3} \le 5$. El MCM es $6$. Multiplicamos por $6$: $3x + 2x \le 30 \implies 5x \le 30 \implies x \le 6$. Como la nota debe ser mayor a $0$, el intervalo correcto es $(0, 6]$."
            },
            {
                "stable_id": "ILCOEF-GEN-PAES-2",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Si el triple de un número disminuido en su cuarta parte es mayor que la suma de sus dos terceras partes y $25$, ¿cuál es el menor entero que cumple dicha condición?",
                "opciones": [
                    r"$10$",
                    r"$11$",
                    r"$12$",
                    r"$13$"
                ],
                "respuesta_correcta": 3,
                "explicacion": r"La inecuación es: $3x - \frac{x}{4} > \frac{2x}{3} + 25$. El MCM de $4$ y $3$ es $12$. Multiplicamos por $12$: $36x - 3x > 8x + 300$. Simplificamos: $33x > 8x + 300 \implies 25x > 300 \implies x > 12$. El menor entero que es estrictamente mayor que $12$ es $13$."
            },
            {
                "stable_id": "ILCOEF-GEN-PAES-3",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Dado el sistema de restricciones para el presupuesto de un proyecto, se requiere que $\frac{P - 1000}{5} \le \frac{P}{7} + 200$. ¿Cuál es el presupuesto máximo posible $P$ en miles de pesos?",
                "opciones": [
                    r"$7000$",
                    r"$6000$",
                    r"$14000$",
                    r"$12000$"
                ],
                "respuesta_correcta": 0,
                "explicacion": r"Multiplicamos la inecuación $\frac{P - 1000}{5} \le \frac{P}{7} + 200$ por el MCM que es $35$. Obtenemos $7(P - 1000) \le 5P + 35(200) \implies 7P - 7000 \le 5P + 7000$. Restamos $5P$ y sumamos $7000$: $2P \le 14000 \implies P \le 7000$. El presupuesto máximo es de $7000$ miles de pesos."
            }
        ]
    }
}

if __name__ == "__main__":
    for sem_id, data in topics.items():
        base_name = sem_id.replace(".", "_")
        yaml_path = f"scratch/{base_name}.yaml"
        jsonl_path = f"scratch/{base_name}.jsonl"

        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(data["yaml"], f, allow_unicode=True, sort_keys=False)

        with open(jsonl_path, "w", encoding="utf-8") as f:
            for exercise in data["jsonl"]:
                f.write(json.dumps(exercise, ensure_ascii=False) + "\\n")

    print("Files successfully generated in scratch/")

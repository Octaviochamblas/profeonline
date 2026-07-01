import json
import yaml
import os

json_data = r"""
{
    "MAT.ALG.SISTEMAS_INECUACIONES.SISTEMA_SIN_SOLUCION": {
        "yaml": {
            "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.SISTEMA_SIN_SOLUCION",
            "titulo": "Sistemas de Inecuaciones Lineales sin Solución",
            "objetivo": "Identificar y resolver sistemas de inecuaciones lineales con una incógnita que no tienen solución, interpretando la intersección vacía de sus conjuntos solución.",
            "introduccion": "Al resolver un sistema de inecuaciones, buscamos los valores que satisfacen todas las desigualdades simultáneamente. Sin embargo, puede darse el caso de que las condiciones sean incompatibles, es decir, que ningún número real cumpla todas las inecuaciones al mismo tiempo. En estos casos, decimos que el sistema no tiene solución.",
            "resumen": "Un sistema de inecuaciones no tiene solución cuando la intersección de los conjuntos solución de cada inecuación individual es vacía ($S_1 \\cap S_2 = \\emptyset$).",
            "explicacion": "### Definición formal\n\nSea un sistema de dos inecuaciones lineales con una incógnita $x$:\n\n$$\\begin{cases} a_1 x + b_1 > 0 \\\\ a_2 x + b_2 < 0 \\end{cases}$$\n\nSi el conjunto solución de la primera inecuación es $S_1$ y el de la segunda es $S_2$, el conjunto solución del sistema es $S = S_1 \\cap S_2$. El sistema no tiene solución si y solo si $S_1 \\cap S_2 = \\emptyset$.\n\n### Desarrollo didáctico\n\nPara comprender visualmente por qué un sistema no tiene solución, resulta muy útil representar los intervalos en la recta numérica. Supongamos que, tras resolver cada inecuación por separado, obtenemos que $x > 5$ y al mismo tiempo $x < 2$.\n\nAl dibujar la recta numérica y marcar los valores mayores a $5$ (hacia la derecha) y los valores menores a $2$ (hacia la izquierda), observamos que las regiones sombreadas no se superponen en ningún punto. No existe ningún número real que sea simultáneamente estrictamente mayor que $5$ y estrictamente menor que $2$. Como no hay elementos en común, la intersección de los intervalos es el conjunto vacío.",
            "procedimiento": [
                "Resuelve cada inecuación del sistema de forma independiente para hallar sus respectivos conjuntos solución.",
                "Expresa el conjunto solución de cada inecuación como un intervalo o desigualdad.",
                "Representa gráficamente cada intervalo obtenido sobre una misma recta numérica.",
                "Identifica la región donde se intersecan o superponen todos los intervalos trazados.",
                "Si los intervalos no se superponen en ningún punto, concluye que la intersección es vacía y el sistema carece de solución."
            ],
            "ejemplos": [
                {
                    "titulo": "Sistema con condiciones opuestas excluyentes",
                    "enunciado": "Resuelve el siguiente sistema de inecuaciones:\n\n$\\begin{cases} 2x - 4 > 6 \\\\ -3x + 9 > 0 \\end{cases}$",
                    "solucion_pasos": [
                        "Resolvemos la primera inecuación: $2x - 4 > 6 \\implies 2x > 10 \\implies x > 5$. El intervalo es $(5, \\infty)$.",
                        "Resolvemos la segunda inecuación: $-3x + 9 > 0 \\implies -3x > -9 \\implies x < 3$. El intervalo es $(-\\infty, 3)$.",
                        "Intersecamos los intervalos: Buscamos valores de $x$ que pertenezcan simultáneamente a $(5, \\infty)$ y a $(-\\infty, 3)$.",
                        "Como $x > 5$ exige que los valores sean mayores a $5$, y $x < 3$ exige que sean menores a $3$, no hay traslape.",
                        "Conclusión: La intersección es vacía, el sistema no tiene solución ($S = \\emptyset$)."
                    ]
                },
                {
                    "titulo": "Restricciones contradictorias en un modelo de producción",
                    "enunciado": "Una fábrica requiere que la temperatura $T$ (en grados Celsius) de un proceso cumpla las siguientes condiciones por motivos de seguridad y eficiencia:\n\n$\\begin{cases} T - 150 \\ge 20 \\\\ 2T \\le 300 \\end{cases}$ \n\n¿Existe alguna temperatura que cumpla ambos requisitos?",
                    "solucion_pasos": [
                        "De la primera condición, tenemos: $T - 150 \\ge 20 \\implies T \\ge 170$. Es decir, la temperatura debe ser al menos de $170^\\circ C$.",
                        "De la segunda condición, tenemos: $2T \\le 300 \\implies T \\le 150$. Esto significa que la temperatura no puede superar los $150^\\circ C$.",
                        "Buscamos la intersección de ambos conjuntos: $[170, \\infty) \\cap (-\\infty, 150]$.",
                        "No existe ningún número real que sea mayor o igual a $170$ y, al mismo tiempo, menor o igual a $150$.",
                        "Por lo tanto, el sistema no tiene solución y no existe una temperatura que satisfaga ambos requisitos."
                    ]
                },
                {
                    "titulo": "¿Es posible que un sistema con inecuaciones que apuntan en el mismo sentido carezca de solución?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "Consideremos un sistema con dos inecuaciones de la forma $x > a$ y $x > b$.",
                        "El conjunto solución será la intersección $(a, \\infty) \\cap (b, \\infty)$.",
                        "Esta intersección siempre resultará en el intervalo $(\\max(a, b), \\infty)$, el cual nunca es vacío.",
                        "De forma análoga ocurre para inecuaciones del tipo $x < a$ y $x < b$.",
                        "Por lo tanto, si las desigualdades apuntan al mismo infinito (sin restricciones adicionales contrarias), el sistema siempre tendrá solución."
                    ]
                },
                {
                    "titulo": "¿El sistema formado por las inecuaciones $x \\ge 4$ y $x \\le 4$ carece de solución?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "El conjunto solución de la primera inecuación es $[4, \\infty)$.",
                        "El conjunto solución de la segunda inecuación es $(-\\infty, 4]$.",
                        "Al intersecar ambos intervalos, obtenemos $[4, \\infty) \\cap (-\\infty, 4]$.",
                        "El único elemento común en ambos conjuntos es el número $4$.",
                        "Por lo tanto, el sistema sí tiene solución, la cual es el conjunto unitario $S = \\{4\\}$."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Creer que si una de las inecuaciones tiene como solución todos los reales, el sistema carece de solución.",
                "Asumir que un sistema carece de solución si los límites de los intervalos son el mismo número y uno es abierto y el otro cerrado.",
                "Afirmar que un sistema no tiene solución si ambas desigualdades involucran signos negativos en la variable principal sin resolverlas primero.",
                "Pensar que la solución de un sistema incompatible es el número cero, confundiendo el conjunto vacío con el valor numérico cero.",
                "Concluir equivocadamente que un sistema sin solución significa que el planteamiento algebraico es incorrecto o inválido."
            ],
            "fuente": "Generado por IA",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "SISS-GEN-CONCEPT-1",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Un sistema de inecuaciones lineales con una incógnita no tiene solución cuando:",
                "opciones": [
                    "La intersección de los conjuntos solución de cada inecuación es el conjunto vacío.",
                    "Al menos una de las inecuaciones tiene solución vacía, sin importar la otra.",
                    "Los intervalos solución se intersecan exactamente en un punto.",
                    "La unión de los conjuntos solución de cada inecuación abarca todos los números reales."
                ],
                "respuesta_correcta": "La intersección de los conjuntos solución de cada inecuación es el conjunto vacío.",
                "explicacion": "El conjunto solución de un sistema de inecuaciones es la intersección de las soluciones de cada una de ellas. Si no hay elementos comunes, la intersección es vacía y el sistema no tiene solución."
            },
            {
                "stable_id": "SISS-GEN-CONCEPT-2",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Si al representar gráficamente las soluciones de un sistema de dos inecuaciones lineales observamos que las regiones sombreadas no se superponen en ninguna sección de la recta numérica, ¿qué podemos afirmar?",
                "opciones": [
                    "El sistema no tiene solución.",
                    "La solución es el conjunto de todos los números reales.",
                    "La solución está determinada solo por la región sombreada a la derecha.",
                    "Falta información para determinar la solución del sistema."
                ],
                "respuesta_correcta": "El sistema no tiene solución.",
                "explicacion": "Que las regiones no se superpongan significa que no comparten ningún número. Al no haber elementos en común, la intersección es nula, y el sistema carece de solución."
            },
            {
                "stable_id": "SISS-GEN-CONCEPT-3",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Sean $S_1$ y $S_2$ los conjuntos solución de dos inecuaciones que conforman un sistema. ¿En qué caso el sistema tendrá como solución el conjunto vacío?",
                "opciones": [
                    "Cuando $S_1 \\cap S_2 = \\emptyset$.",
                    "Cuando $S_1 \\cup S_2 = \\emptyset$.",
                    "Cuando $S_1 \\cap S_2 = \\{0\\}$.",
                    "Cuando uno de los conjuntos es subconjunto del otro."
                ],
                "respuesta_correcta": "Cuando $S_1 \\cap S_2 = \\emptyset$.",
                "explicacion": "El sistema busca los valores que satisfacen ambas inecuaciones simultáneamente, lo que equivale a la intersección de sus soluciones. Si esta es vacía ($\\emptyset$), el sistema no tiene solución."
            },
            {
                "stable_id": "SISS-GEN-RECON-1",
                "tipo": "reconocimiento",
                "nivel": 1,
                "enunciado": "¿Cuál de los siguientes sistemas de inecuaciones lineales no tiene solución?",
                "opciones": [
                    "$\\begin{cases} x > 5 \\\\ x < 3 \\end{cases}$",
                    "$\\begin{cases} x > 3 \\\\ x < 5 \\end{cases}$",
                    "$\\begin{cases} x \\ge 4 \\\\ x \\le 4 \\end{cases}$",
                    "$\\begin{cases} x > 2 \\\\ x > 4 \\end{cases}$"
                ],
                "respuesta_correcta": "$\\begin{cases} x > 5 \\\\ x < 3 \\end{cases}$",
                "explicacion": "En la primera opción, se exige que un número sea mayor que $5$ y simultáneamente menor que $3$, lo cual es imposible. La intersección de $(5, \\infty)$ y $(-\\infty, 3)$ es vacía."
            },
            {
                "stable_id": "SISS-GEN-PROC-1",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El sistema de inecuaciones $\\begin{cases} 2x + 1 > 7 \\\\ x - 4 < 0 \\end{cases}$ carece de solución.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Falso",
                "explicacion": "La primera inecuación se reduce a $2x > 6 \\implies x > 3$. La segunda a $x < 4$. La intersección de $x > 3$ y $x < 4$ es el intervalo $(3, 4)$, por lo que el sistema sí tiene solución."
            },
            {
                "stable_id": "SISS-GEN-PROC-2",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El sistema de inecuaciones $\\begin{cases} -x + 3 < 1 \\\\ 2x \\le 4 \\end{cases}$ no tiene solución real.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Verdadero",
                "explicacion": "La primera inecuación es $-x < -2 \\implies x > 2$. La segunda inecuación es $x \\le 2$. La intersección de $(2, \\infty)$ y $(-\\infty, 2]$ es el conjunto vacío (el $2$ no está incluido en el primer intervalo). Por lo tanto, no tiene solución."
            },
            {
                "stable_id": "SISS-GEN-PROC-3",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "Al resolver $\\begin{cases} 3(x - 1) \\ge 6 \\\\ x + 2 \\le 5 \\end{cases}$, se obtiene que la intersección de sus intervalos solución es vacía.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Falso",
                "explicacion": "Para la primera: $3x - 3 \\ge 6 \\implies 3x \\ge 9 \\implies x \\ge 3$. Para la segunda: $x \\le 3$. La intersección de $x \\ge 3$ y $x \\le 3$ es exactamente el número $3$, por lo que la intersección no es vacía."
            },
            {
                "stable_id": "SISS-GEN-PAES-1",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": true,
                "enunciado": "Se tiene el siguiente sistema de inecuaciones con la variable real $x$, donde $k$ es una constante real:\n\n$\\begin{cases} x - 2 > 4 \\\\ x + k < 0 \\end{cases}$\n\n¿Para qué conjunto de valores de $k$ el sistema NO tiene solución?",
                "opciones": [
                    "$k \\ge -6$",
                    "$k < -6$",
                    "$k \\le 6$",
                    "$k > 6$"
                ],
                "respuesta_correcta": "$k \\ge -6$",
                "explicacion": "La primera inecuación es $x > 6$. La segunda es $x < -k$. Para que el sistema no tenga solución, la intersección de $(6, \\infty)$ y $(-\\infty, -k)$ debe ser vacía. Esto ocurre si el extremo superior del segundo intervalo es menor o igual al extremo inferior del primer intervalo, es decir, $-k \\le 6$. Multiplicando por $-1$ y cambiando el sentido, obtenemos $k \\ge -6$."
            },
            {
                "stable_id": "SISS-GEN-PAES-2",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": true,
                "enunciado": "Considera el sistema de inecuaciones en $x$:\n\n$\\begin{cases} 4x - p \\ge 0 \\\\ 2x - 8 < 0 \\end{cases}$\n\nSi el sistema no tiene solución, ¿cuál es la condición necesaria que debe cumplir el parámetro real $p$?",
                "opciones": [
                    "$p \\ge 16$",
                    "$p \\le 16$",
                    "$p \\ge 4$",
                    "$p \\le 8$"
                ],
                "respuesta_correcta": "$p \\ge 16$",
                "explicacion": "De la segunda inecuación, $2x < 8 \\implies x < 4$. De la primera inecuación, $4x \\ge p \\implies x \\ge \\frac{p}{4}$. El sistema exige que $x$ esté en $[\\frac{p}{4}, \\infty) \\cap (-\\infty, 4)$. Para que no tenga solución, la intersección debe ser vacía, lo cual sucede si el límite inferior del primer intervalo es mayor o igual al límite superior del segundo: $\\frac{p}{4} \\ge 4$. Resolviendo, $p \\ge 16$."
            },
            {
                "stable_id": "SISS-GEN-PAES-3",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": true,
                "enunciado": "Un agricultor planea cercar un terreno rectangular. El perímetro debe ser estrictamente menor que $60$ metros, y al mismo tiempo, el lado mayor (cuya longitud excede al lado menor en $5$ metros) debe ser de al menos $25$ metros. ¿Es posible construir este terreno?",
                "opciones": [
                    "No, porque las inecuaciones generan un sistema sin solución.",
                    "Sí, siempre que el lado menor mida más de $15$ metros.",
                    "Sí, el lado menor puede medir exactamente $10$ metros.",
                    "No, porque el perímetro mínimo requerido es de $100$ metros."
                ],
                "respuesta_correcta": "No, porque las inecuaciones generan un sistema sin solución.",
                "explicacion": "Sea $x$ el lado menor. El lado mayor es $x + 5$. El perímetro es $2(x + x + 5) = 4x + 10$. Las condiciones son:\n1) Perímetro $< 60 \\implies 4x + 10 < 60 \\implies 4x < 50 \\implies x < 12.5$.\n2) Lado mayor $\\ge 25 \\implies x + 5 \\ge 25 \\implies x \\ge 20$.\nEl sistema es $\\begin{cases} x < 12.5 \\\\ x \\ge 20 \\end{cases}$. Este sistema no tiene solución, por lo que es imposible construir el terreno."
            }
        ]
    },
    "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.MAYOR_IGUAL_POSITIVO": {
        "yaml": {
            "semantic_id": "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.MAYOR_IGUAL_POSITIVO",
            "titulo": "Inecuaciones con Valor Absoluto del tipo |x| ≥ a, con a > 0",
            "objetivo": "Resolver inecuaciones que involucran un valor absoluto mayor o igual a una constante positiva, aplicando sus propiedades algebraicas para determinar el conjunto solución.",
            "introduccion": "El valor absoluto de un número representa su distancia al origen en la recta numérica. Cuando nos encontramos con una expresión de la forma $|x| \\ge a$, donde $a$ es un número positivo, estamos buscando todos los números reales cuya distancia a cero sea igual o mayor que $a$. Esta condición geométrica se traduce en dos direcciones opuestas sobre la recta.",
            "resumen": "La inecuación con valor absoluto $|x| \\ge a$, con $a > 0$, se separa en dos inecuaciones simples: $x \\le -a$ o $x \\ge a$. La solución es la unión de los intervalos correspondientes: $(-\\infty, -a] \\cup [a, \\infty)$.",
            "explicacion": "### Definición formal\n\nSea $x$ una expresión algebraica y $a \\in \\mathbb{R}$ tal que $a > 0$. La inecuación $|x| \\ge a$ es equivalente a la disyunción lógica:\n\n$$x \\le -a \\quad \\lor \\quad x \\ge a$$\n\nEl conjunto solución general de esta inecuación se expresa como la unión de dos intervalos:\n\n$$S = (-\\infty, -a] \\cup [a, \\infty)$$\n\nEsta propiedad se fundamenta en la definición de valor absoluto como distancia. Los valores de $x$ que satisfacen la inecuación son aquellos situados a la izquierda de $-a$ (inclusive) o a la derecha de $a$ (inclusive).\n\n### Desarrollo didáctico\n\nImagina que estás en el centro de una plaza (posición $0$) y te piden que te ubiques a una distancia de al menos $5$ metros del centro. Para cumplir esta condición, tienes dos opciones: puedes caminar $5$ metros o más hacia la izquierda, llegando a posiciones iguales o menores a $-5$; o puedes caminar $5$ metros o más hacia la derecha, alcanzando posiciones iguales o mayores a $5$.\n\nCualquier posición entre $-5$ y $5$ no cumple con la regla, ya que estarías a una distancia menor a $5$ metros del centro. Al trasladar esta idea a una expresión algebraica arbitraria $|f(x)| \\ge a$, simplemente resolvemos dos casos separados: cuando el interior del valor absoluto es muy negativo ($f(x) \\le -a$) y cuando es muy positivo ($f(x) \\ge a$). La palabra fundamental aquí es \"o\" (disyunción), lo que implica que el conjunto solución será la unión de ambos escenarios.",
            "procedimiento": [
                "Identifica la expresión de la forma $|f(x)| \\ge a$ y verifica que $a$ sea un número positivo.",
                "Aplica la propiedad del valor absoluto para separar en dos inecuaciones independientes conectadas por un \"o\": $f(x) \\le -a$ y $f(x) \\ge a$.",
                "Resuelve la primera inecuación $f(x) \\le -a$ para encontrar su conjunto solución $S_1$.",
                "Resuelve la segunda inecuación $f(x) \\ge a$ para encontrar su conjunto solución $S_2$.",
                "El conjunto solución final será la unión de ambas soluciones obtenidas: $S = S_1 \\cup S_2$."
            ],
            "ejemplos": [
                {
                    "titulo": "Resolución de una inecuación lineal con valor absoluto",
                    "enunciado": "Encuentra el conjunto solución de la inecuación $|2x - 3| \\ge 7$.",
                    "solucion_pasos": [
                        "Identificamos que la inecuación tiene la forma $|f(x)| \\ge a$, con $a = 7 > 0$.",
                        "Aplicamos la propiedad: $2x - 3 \\le -7$ o $2x - 3 \\ge 7$.",
                        "Resolvemos el primer caso: $2x - 3 \\le -7 \\implies 2x \\le -4 \\implies x \\le -2$. El intervalo es $(-\\infty, -2]$.",
                        "Resolvemos el segundo caso: $2x - 3 \\ge 7 \\implies 2x \\ge 10 \\implies x \\ge 5$. El intervalo es $[5, \\infty)$.",
                        "La solución final es la unión de ambos intervalos: $S = (-\\infty, -2] \\cup [5, \\infty)$."
                    ]
                },
                {
                    "titulo": "Despeje previo antes de aplicar la propiedad",
                    "enunciado": "Resuelve la inecuación $3|x + 1| - 4 \\ge 5$.",
                    "solucion_pasos": [
                        "Primero debemos aislar el valor absoluto. Sumamos $4$ a ambos lados: $3|x + 1| \\ge 9$.",
                        "Dividimos por $3$: $|x + 1| \\ge 3$.",
                        "Aplicamos la propiedad de $|X| \\ge a$: $x + 1 \\le -3$ o $x + 1 \\ge 3$.",
                        "Resolvemos la primera inecuación: $x + 1 \\le -3 \\implies x \\le -4$.",
                        "Resolvemos la segunda inecuación: $x + 1 \\ge 3 \\implies x \\ge 2$.",
                        "El conjunto solución es la unión: $(-\\infty, -4] \\cup [2, \\infty)$."
                    ]
                },
                {
                    "titulo": "¿El conjunto solución de $|x| \\ge 2$ incluye los números comprendidos entre -2 y 2?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "La expresión $|x| \\ge 2$ significa que la distancia de $x$ al cero debe ser mayor o igual a $2$.",
                        "Los números comprendidos estrictamente entre $-2$ y $2$ (por ejemplo, el $0$, el $1$ o el $-1.5$) tienen una distancia al cero que es menor que $2$.",
                        "Por definición, se resuelve como $x \\le -2 \\lor x \\ge 2$.",
                        "Por lo tanto, la región entre $-2$ y $2$ es justamente la parte de la recta real que no forma parte de la solución."
                    ]
                },
                {
                    "titulo": "¿Es correcto expresar la solución de $|x - 5| \\ge 3$ como una intersección de intervalos?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        "La inecuación $|x - 5| \\ge 3$ se descompone en dos condiciones disjuntas: $x - 5 \\le -3$ o $x - 5 \\ge 3$.",
                        "El conector lógico involucrado es \"o\" (disyunción), que se traduce algebraicamente en una unión de conjuntos ($\\cup$).",
                        "Si se expresara como una intersección ($\\cap$), se estarían buscando números que sean simultáneamente menores que $2$ y mayores que $8$, lo cual es el conjunto vacío.",
                        "En consecuencia, la solución debe expresarse siempre como una unión de intervalos: $(-\\infty, 2] \\cup [8, \\infty)$."
                    ]
                }
            ],
            "errores_frecuentes": [
                "Expresar la solución como una intersección de intervalos en lugar de una unión, obteniendo equivocadamente el conjunto vacío.",
                "Escribir incorrectamente la propiedad descomponiendo en $-a \\le x \\le a$, lo cual corresponde al caso del símbolo \"menor o igual\".",
                "Omitir el signo negativo al plantear la desigualdad $x \\le -a$, escribiéndola erróneamente como $x \\le a$.",
                "No cambiar el sentido de la desigualdad al plantear la parte negativa, escribiendo $x \\ge -a$ en lugar de $x \\le -a$.",
                "Olvidar incluir los corchetes cerrados en la notación de intervalos, asumiendo que la inecuación era estricta (sin el \"igual\")."
            ],
            "fuente": "Generado por IA",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "IVAMP-GEN-CONCEPT-1",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "La inecuación $|x| \\ge a$, con $a > 0$, es lógicamente equivalente a:",
                "opciones": [
                    "$x \\le -a \\lor x \\ge a$",
                    "$-a \\le x \\le a$",
                    "$x \\ge -a \\lor x \\ge a$",
                    "$x \\le -a \\land x \\ge a$"
                ],
                "respuesta_correcta": "$x \\le -a \\lor x \\ge a$",
                "explicacion": "Por propiedad del valor absoluto para inecuaciones de la forma mayor o igual, la expresión se separa en dos intervalos divergentes unidos por el conector lógico \"o\" (disyunción)."
            },
            {
                "stable_id": "IVAMP-GEN-CONCEPT-2",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "¿Qué representa geométricamente la inecuación $|x - p| \\ge k$, con $k > 0$?",
                "opciones": [
                    "Todos los números cuya distancia a $p$ es mayor o igual a $k$.",
                    "Todos los números cuya distancia a cero es mayor o igual a $k$.",
                    "Todos los números cuya distancia a $p$ es menor o igual a $k$.",
                    "Todos los números comprendidos en el intervalo $[-k, k]$ desplazado en $p$."
                ],
                "respuesta_correcta": "Todos los números cuya distancia a $p$ es mayor o igual a $k$.",
                "explicacion": "La expresión $|x - p|$ denota la distancia entre $x$ y $p$. Al establecer que es $\\ge k$, se indican los puntos en la recta que están a una distancia igual o superior a $k$ desde el punto central $p$."
            },
            {
                "stable_id": "IVAMP-GEN-CONCEPT-3",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Si la solución de una inecuación de valor absoluto está dada por $(-\\infty, -3] \\cup [3, \\infty)$, ¿cuál es la inecuación que la origina?",
                "opciones": [
                    "$|x| \\ge 3$",
                    "$|x| \\le 3$",
                    "$|x| > 3$",
                    "$|x - 3| \\ge 0$"
                ],
                "respuesta_correcta": "$|x| \\ge 3$",
                "explicacion": "El conjunto solución $(-\\infty, -3] \\cup [3, \\infty)$ equivale a los valores tales que $x \\le -3 \\lor x \\ge 3$. Esto corresponde exactamente a la definición de $|x| \\ge 3$."
            },
            {
                "stable_id": "IVAMP-GEN-RECON-1",
                "tipo": "reconocimiento",
                "nivel": 1,
                "enunciado": "Identifica cuál de las siguientes inecuaciones requiere aplicar la propiedad $|X| \\ge a \\iff X \\le -a \\lor X \\ge a$ para ser resuelta correctamente.",
                "opciones": [
                    "$|2x - 1| \\ge 4$",
                    "$|x + 5| < 2$",
                    "$|3x| \\le 9$",
                    "$-|x| \\ge 5$"
                ],
                "respuesta_correcta": "$|2x - 1| \\ge 4$",
                "explicacion": "La primera opción tiene la forma directa de un valor absoluto mayor o igual a un número positivo, por lo que requiere aplicar la propiedad que descompone en disyunción. Las de menor o igual requieren intersección."
            },
            {
                "stable_id": "IVAMP-GEN-PROC-1",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "La solución de la inecuación $|x - 2| \\ge 5$ es el intervalo $[-3, 7]$.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Falso",
                "explicacion": "Al aplicar la propiedad, obtenemos $x - 2 \\le -5 \\implies x \\le -3$ o $x - 2 \\ge 5 \\implies x \\ge 7$. La solución es la unión $(-\\infty, -3] \\cup [7, \\infty)$. El intervalo $[-3, 7]$ sería la solución de $|x - 2| \\le 5$."
            },
            {
                "stable_id": "IVAMP-GEN-PROC-2",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "Al resolver $|3x| \\ge 12$, el conjunto solución contiene al número $0$.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Falso",
                "explicacion": "La inecuación se descompone en $3x \\le -12 \\implies x \\le -4$ o $3x \\ge 12 \\implies x \\ge 4$. El conjunto solución es $(-\\infty, -4] \\cup [4, \\infty)$. El $0$ no se encuentra en esta unión."
            },
            {
                "stable_id": "IVAMP-GEN-PROC-3",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "La inecuación $2|x + 4| - 6 \\ge 0$ es equivalente a resolver $|x + 4| \\ge 3$.",
                "opciones": [
                    "Verdadero",
                    "Falso"
                ],
                "respuesta_correcta": "Verdadero",
                "explicacion": "Sumando $6$ a ambos lados obtenemos $2|x + 4| \\ge 6$. Luego, dividiendo por $2$, resulta $|x + 4| \\ge 3$. Ambas inecuaciones son equivalentes."
            },
            {
                "stable_id": "IVAMP-GEN-PAES-1",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": true,
                "enunciado": "El conjunto de todos los números reales $x$ que satisfacen la inecuación $|5 - 2x| \\ge 9$ es:",
                "opciones": [
                    "$(-\\infty, -2] \\cup [7, \\infty)$",
                    "$[-2, 7]$",
                    "$(-\\infty, -7] \\cup [2, \\infty)$",
                    "$(-\\infty, -2) \\cup (7, \\infty)$"
                ],
                "respuesta_correcta": "$(-\\infty, -2] \\cup [7, \\infty)$",
                "explicacion": "Aplicamos la propiedad: $5 - 2x \\le -9 \\lor 5 - 2x \\ge 9$. Resolviendo la primera: $-2x \\le -14 \\implies x \\ge 7$. Resolviendo la segunda: $-2x \\ge 4 \\implies x \\le -2$. La unión es $(-\\infty, -2] \\cup [7, \\infty)$."
            },
            {
                "stable_id": "IVAMP-GEN-PAES-2",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": true,
                "enunciado": "Una máquina empacadora llena bolsas de café de tal manera que el peso real de la bolsa, en gramos, difiere de $500$ gramos en $15$ gramos o más, es defectuosa y se descarta. Si $x$ representa el peso de una bolsa, ¿cuál es la inecuación que modela el peso de las bolsas que son DESCARTADAS?",
                "opciones": [
                    "$|x - 500| \\ge 15$",
                    "$|x - 500| \\le 15$",
                    "$|x - 15| \\ge 500$",
                    "$|x + 500| \\ge 15$"
                ],
                "respuesta_correcta": "$|x - 500| \\ge 15$",
                "explicacion": "El peso ideal es $500$ gramos. La diferencia entre el peso real y el ideal se expresa como $|x - 500|$. Si esta diferencia es de $15$ gramos o más, la bolsa se descarta. Esto se modela con la inecuación $|x - 500| \\ge 15$."
            },
            {
                "stable_id": "IVAMP-GEN-PAES-3",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": true,
                "enunciado": "¿Cuál de las siguientes gráficas en la recta real representa al conjunto solución de $|\\frac{x - 1}{2}| \\ge 3$?",
                "opciones": [
                    "Una recta con los intervalos $(-\\infty, -5]$ y $[7, \\infty)$ sombreados.",
                    "Una recta con el segmento continuo desde $-5$ hasta $7$ sombreado.",
                    "Una recta con los intervalos $(-\\infty, -7]$ y $[5, \\infty)$ sombreados.",
                    "Una recta con el segmento continuo desde $-7$ hasta $5$ sombreado."
                ],
                "respuesta_correcta": "Una recta con los intervalos $(-\\infty, -5]$ y $[7, \\infty)$ sombreados.",
                "explicacion": "Resolvemos la inecuación: $\\frac{x - 1}{2} \\le -3 \\lor \\frac{x - 1}{2} \\ge 3$. Multiplicando por $2$: $x - 1 \\le -6 \\lor x - 1 \\ge 6$. Sumando $1$: $x \\le -5 \\lor x \\ge 7$. Esto corresponde a la unión de los intervalos $(-\\infty, -5]$ y $[7, \\infty)$."
            }
        ]
    }
}
"""

topics = json.loads(json_data)

def create_files(base_dir="scratch"):
    os.makedirs(base_dir, exist_ok=True)
    for sem_id, data in topics.items():
        # YAML
        yaml_path = os.path.join(base_dir, f"{sem_id}.yaml")
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(data["yaml"], f, allow_unicode=True, sort_keys=False)

        # JSONL
        jsonl_path = os.path.join(base_dir, f"{sem_id}.jsonl")
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for item in data["jsonl"]:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print("Files created successfully.")

if __name__ == "__main__":
    create_files()

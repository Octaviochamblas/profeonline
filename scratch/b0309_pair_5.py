import os
import json

topics = {
    "MAT.ALG.SISTEMAS_INECUACIONES.INTERSECCION_SOLUCIONES": {
        "yaml": r"""semantic_id: MAT.ALG.SISTEMAS_INECUACIONES.INTERSECCION_SOLUCIONES
titulo: Intersección de soluciones en sistemas de inecuaciones lineales
objetivo: Determinar el conjunto solución de un sistema de inecuaciones lineales mediante la intersección de las soluciones individuales.
introduccion: Un sistema de inecuaciones lineales con una incógnita agrupa dos o más inecuaciones que deben cumplirse de manera simultánea. La solución del sistema corresponde a los valores que satisfacen todas las inecuaciones al mismo tiempo, lo que geométricamente representa la intersección de los intervalos solución de cada inecuación en la recta real.
resumen: La solución de un sistema de inecuaciones se encuentra resolviendo cada inecuación por separado y luego determinando la intersección de los conjuntos solución resultantes.
explicacion:
  - "### Definición formal\nSea un sistema de $n$ inecuaciones lineales con una incógnita $x$, cuyos conjuntos solución individuales son $S_1, S_2, \\dots, S_n$. El conjunto solución del sistema, denotado como $S_{total}$, está dado por la intersección de todos los conjuntos solución individuales: $S_{total} = S_1 \\cap S_2 \\cap \\dots \\cap S_n$. Si la intersección es vacía ($S_{total} = \\emptyset$), el sistema no tiene solución en los números reales."
  - "### Desarrollo didáctico\nPara comprender la solución de un sistema de inecuaciones, es fundamental visualizar cada inecuación como una condición independiente. Al graficar el conjunto solución de cada inecuación en una misma recta numérica, se observan zonas donde los intervalos se superponen. Esta región de superposición contiene los valores que cumplen con todas las condiciones impuestas simultáneamente. Es posible que los intervalos no se superpongan en absoluto; en tal situación, no existe ningún número real que satisfaga el sistema completo, concluyendo que el conjunto solución es el conjunto vacío."
procedimiento:
  - "Resolver cada inecuación del sistema de forma independiente, despejando la incógnita."
  - "Expresar el conjunto solución de cada inecuación en forma de intervalo o mediante representación gráfica en la recta numérica real."
  - "Determinar la intersección de todos los intervalos obtenidos, identificando la región donde se superponen todos los conjuntos solución."
  - "Expresar el resultado final como un único intervalo, unión de intervalos, o indicar que es el conjunto vacío si no hay superposición."
ejemplos:
  - titulo: "Sistema con solución acotada"
    enunciado: "Resuelva el sistema compuesto por las inecuaciones $2x - 4 < 0$ y $x + 1 \\geq 0$."
    solucion_pasos:
      - "Para la primera inecuación: $2x < 4 \\implies x < 2$. Su solución es $S_1 = ]-\\infty, 2[$."
      - "Para la segunda inecuación: $x \\geq -1$. Su solución es $S_2 = [-1, +\\infty[$."
      - "La intersección de ambos conjuntos es $S_1 \\cap S_2 = ]-\\infty, 2[ \\cap [-1, +\\infty[ = [-1, 2[$."
      - "El conjunto solución del sistema es el intervalo $[-1, 2[$."
  - titulo: "Sistema sin solución real"
    enunciado: "Determine el conjunto solución del sistema formado por $3x + 6 \\leq 0$ y $2x - 2 > 4$."
    solucion_pasos:
      - "Resolviendo la primera inecuación: $3x \\leq -6 \\implies x \\leq -2$. Solución: $S_1 = ]-\\infty, -2]$."
      - "Resolviendo la segunda inecuación: $2x > 6 \\implies x > 3$. Solución: $S_2 = ]3, +\\infty[$."
      - "La intersección es $S_1 \\cap S_2 = ]-\\infty, -2] \\cap ]3, +\\infty[ = \\emptyset$."
      - "Como no hay superposición, el sistema no tiene solución real."
  - titulo: "¿El número $0$ pertenece al conjunto solución del sistema compuesto por $x > -2$ y $x < 1$?"
    respuesta: "Sí"
    solucion_pasos:
      - "Se evalúa $x = 0$ en la primera inecuación: $0 > -2$, lo cual es verdadero."
      - "Se evalúa $x = 0$ en la segunda inecuación: $0 < 1$, lo cual es verdadero."
      - "Dado que el valor satisface ambas inecuaciones simultáneamente, pertenece al conjunto solución."
  - titulo: "¿El conjunto solución del sistema $x > 5$ y $x > 8$ es el intervalo $]5, 8[$?"
    respuesta: "No"
    solucion_pasos:
      - "La solución de la primera inecuación es el intervalo $]5, +\\infty[$."
      - "La solución de la segunda inecuación es el intervalo $]8, +\\infty[$."
      - "La intersección de ambos intervalos es la región donde ambos se superponen, es decir, los valores mayores que $8$."
      - "Por lo tanto, la solución correcta es el intervalo $]8, +\\infty[$, no $]5, 8[$."
errores_frecuentes:
  - "Unir los conjuntos solución de cada inecuación en lugar de intersectarlos para encontrar la solución del sistema."
  - "Considerar que si una de las inecuaciones no tiene solución, el sistema aún puede tener solución basándose en las demás inecuaciones."
  - "Incluir los extremos de los intervalos en la solución final del sistema cuando provienen de inecuaciones con desigualdades estrictas ($<$ o $>$)."
  - "Asumir que un sistema de dos inecuaciones siempre tendrá como solución un intervalo cerrado y acotado."
  - "Multiplicar o dividir una inecuación por un número negativo sin invertir el sentido de la desigualdad, afectando el intervalo a intersectar."
fuente: "Creación propia"
estado: publicado""",
        "jsonl": [
            {
                "id": "SIST-GEN-CONCEPT-1",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "En un sistema de dos inecuaciones lineales con una incógnita, ¿qué operación matemática entre los conjuntos solución individuales determina el conjunto solución del sistema?",
                "opciones": [
                    {"texto": "La intersección", "correcta": True},
                    {"texto": "La unión", "correcta": False},
                    {"texto": "La diferencia simétrica", "correcta": False},
                    {"texto": "La adición de intervalos", "correcta": False}
                ],
                "resolucion": "Por definición, un sistema de inecuaciones exige que todas las condiciones se cumplan simultáneamente. Matemáticamente, esto equivale a encontrar los elementos comunes, es decir, la intersección de los conjuntos solución individuales."
            },
            {
                "id": "SIST-GEN-CONCEPT-2",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Si al graficar los conjuntos solución de las inecuaciones de un sistema se observa que no comparten ningún punto en la recta numérica, ¿qué se concluye sobre la solución del sistema?",
                "opciones": [
                    {"texto": "El conjunto solución es el conjunto vacío.", "correcta": True},
                    {"texto": "La solución son todos los números reales.", "correcta": False},
                    {"texto": "El sistema tiene infinitas soluciones.", "correcta": False},
                    {"texto": "Se deben sumar los extremos de los intervalos.", "correcta": False}
                ],
                "resolucion": "Si no hay superposición, significa que no existe ningún número que satisfaga todas las inecuaciones a la vez. Por lo tanto, la intersección es nula, y el conjunto solución es el vacío ($\\emptyset$)."
            },
            {
                "id": "SIST-GEN-CONCEPT-3",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "¿Qué representa geométricamente la solución de un sistema de inecuaciones lineales?",
                "opciones": [
                    {"texto": "La región de la recta real donde se superponen todos los intervalos solución.", "correcta": True},
                    {"texto": "Todos los puntos que pertenecen al menos a un intervalo solución.", "correcta": False},
                    {"texto": "El punto medio entre los extremos de los intervalos involucrados.", "correcta": False},
                    {"texto": "Únicamente los valores enteros comunes de cada inecuación.", "correcta": False}
                ],
                "resolucion": "Geométricamente, la intersección (y por tanto la solución del sistema) corresponde a la zona de la recta numérica en la que todos los intervalos graficados se superponen."
            },
            {
                "id": "SIST-GEN-RECON-1",
                "tipo": "reconocimiento",
                "nivel": 1,
                "enunciado": "¿Cuál de las siguientes expresiones representa el conjunto solución del sistema formado por $x > 2$ y $x \\leq 5$?",
                "opciones": [
                    {"texto": "$]2, 5]$", "correcta": True},
                    {"texto": "$[2, 5[$", "correcta": False},
                    {"texto": "$]2, +\\infty[$", "correcta": False},
                    {"texto": "$]-\\infty, 5]$", "correcta": False}
                ],
                "resolucion": "La primera inecuación representa los valores estrictamente mayores a $2$ ($]2, +\\infty[$) y la segunda los menores o iguales a $5$ ($]-\\infty, 5]$). La intersección de ambos corresponde a los números entre $2$ y $5$, excluyendo el $2$ e incluyendo el $5$, es decir, el intervalo $]2, 5]$."
            },
            {
                "id": "SIST-GEN-PROC-1",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El conjunto solución del sistema compuesto por $x > 4$ y $x > 7$ es el intervalo $]4, +\\infty[$.",
                "respuesta": False,
                "resolucion": "La intersección de los intervalos $]4, +\\infty[$ y $]7, +\\infty[$ es la región donde ambos se solapan. Dado que todo número mayor que $7$ es también mayor que $4$, la intersección es estrictamente $]7, +\\infty[$. Por lo tanto, la afirmación es falsa."
            },
            {
                "id": "SIST-GEN-PROC-2",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El sistema compuesto por las inecuaciones $2x > 6$ y $x < 0$ no tiene solución en los números reales.",
                "respuesta": True,
                "resolucion": "Al resolver la primera inecuación se obtiene $x > 3$. La segunda inecuación es $x < 0$. No existen números que sean simultáneamente mayores a $3$ y menores a $0$, por lo que la intersección de $]3, +\\infty[$ y $]-\\infty, 0[$ es vacía. La afirmación es verdadera."
            },
            {
                "id": "SIST-GEN-PROC-3",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "La solución del sistema $-x \\leq -3$ y $x \\leq 5$ es el intervalo $[-3, 5]$.",
                "respuesta": False,
                "resolucion": "Al resolver la primera inecuación, al multiplicar por $-1$ se invierte la desigualdad: $x \\geq 3$. La segunda es $x \\leq 5$. La intersección entre $[3, +\\infty[$ y $]-\\infty, 5]$ es el intervalo $[3, 5]$, no $[-3, 5]$. La afirmación es falsa."
            },
            {
                "id": "SIST-GEN-PAES-1",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "¿Cuál es el conjunto solución del sistema de inecuaciones $3x - 1 \\leq 5$ y $2x + 4 > 2$?",
                "opciones": [
                    {"texto": "$]-1, 2]$", "correcta": True},
                    {"texto": "$[-1, 2]$", "correcta": False},
                    {"texto": "$]1, 2]$", "correcta": False},
                    {"texto": "$]-1, +\\infty[$", "correcta": False}
                ],
                "resolucion": "Para la primera inecuación: $3x \\leq 6 \\implies x \\leq 2$, cuyo intervalo es $]-\\infty, 2]$. Para la segunda: $2x > -2 \\implies x > -1$, con intervalo $]-1, +\\infty[$. La intersección de ambos conjuntos es $]-1, +\\infty[ \\cap ]-\\infty, 2] = ]-1, 2]$."
            },
            {
                "id": "SIST-GEN-PAES-2",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Considere el sistema de inecuaciones $x > a$ y $x < b$, donde $a$ y $b$ son constantes reales. Si se sabe que el sistema no tiene solución, ¿cuál de las siguientes relaciones es siempre verdadera?",
                "opciones": [
                    {"texto": "$a \\geq b$", "correcta": True},
                    {"texto": "$a < b$", "correcta": False},
                    {"texto": "$a = 0$", "correcta": False},
                    {"texto": "$b < 0$", "correcta": False}
                ],
                "resolucion": "El sistema plantea encontrar los valores de $x$ que estén estrictamente entre $a$ y $b$, lo cual requiere que el intervalo $]a, b[$ exista. Para que la intersección sea vacía, el límite inferior $a$ debe ser mayor o igual al límite superior $b$. Así, $a \\geq b$ garantiza que no haya superposición."
            },
            {
                "id": "SIST-GEN-PAES-3",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Un ascensor tiene una capacidad máxima de $400$ kg y un mínimo de seguridad de $50$ kg para operar. Si $x$ representa la masa transportada en kg, y por motivos de mantención se impone la restricción adicional de que la masa debe ser estrictamente menor a $350$ kg, ¿cuál es el intervalo que representa las posibles masas $x$ permitidas para que el ascensor funcione?",
                "opciones": [
                    {"texto": "$[50, 350[$", "correcta": True},
                    {"texto": "$]50, 400]$", "correcta": False},
                    {"texto": "$[50, 350]$", "correcta": False},
                    {"texto": "$]0, 350[$", "correcta": False}
                ],
                "resolucion": "La primera condición establece que $50 \\leq x \\leq 400$, que equivale a $x \\geq 50$ y $x \\leq 400$. La segunda condición adicional (por mantención) es $x < 350$. La solución se encuentra intersectando estas condiciones: $[50, 400] \\cap ]-\\infty, 350[ = [50, 350[$. Por lo tanto, el intervalo de masas permitidas es $[50, 350[$."
            }
        ]
    },
    "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.MAYOR_QUE_POSITIVO": {
        "yaml": r"""semantic_id: MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.MAYOR_QUE_POSITIVO
titulo: Inecuaciones con valor absoluto de la forma $|x| > a$ con $a > 0$
objetivo: Resolver inecuaciones que involucran valor absoluto del tipo $|x| > a$ o $|x| \geq a$, interpretando geométricamente la distancia y aplicando propiedades algebraicas.
introduccion: El valor absoluto de un número real representa su distancia al origen en la recta numérica. Cuando se plantea una inecuación del tipo $|x| > a$, donde $a$ es un número positivo, se están buscando todos los valores de $x$ cuya distancia al cero sea estrictamente mayor que $a$. Geométricamente, esto corresponde a los números que se ubican a la derecha de $a$ o a la izquierda de $-a$.
resumen: La inecuación $|x| > a$ con $a > 0$ se transforma en la disyunción lógica de dos inecuaciones lineales, $x > a \lor x < -a$, cuya solución es la unión de dos intervalos disjuntos.
explicacion:
  - "### Definición formal\nSea $x \\in \\mathbb{R}$ y un número real $a > 0$. La inecuación con valor absoluto $|x| > a$ es equivalente a la proposición lógica $x > a \\lor x < -a$. En términos de conjuntos, el conjunto solución $S$ está dado por la unión de intervalos: $S = ]-\\infty, -a[ \\cup ]a, +\\infty[$. Análogamente, para la inecuación no estricta $|x| \\geq a$, la equivalencia es $x \\geq a \\lor x \\leq -a$, y el conjunto solución corresponde a $S = ]-\\infty, -a] \\cup [a, +\\infty[$."
  - "### Desarrollo didáctico\nPara comprender esta propiedad, se puede recurrir a la definición geométrica del valor absoluto como distancia. La expresión $|x| > a$ requiere encontrar todos los puntos $x$ que se encuentren a una distancia mayor que $a$ unidades del punto central (el cero). Si partimos del cero y nos alejamos $a$ unidades en ambas direcciones, llegamos a los puntos $-a$ y $a$. Los valores cuya distancia al origen es mayor que $a$ se encuentran fuera de este segmento delimitado por $-a$ y $a$. Esto explica por qué la solución se divide en dos regiones separadas: los números muy negativos (menores que $-a$) y los números muy positivos (mayores que $a$)."
procedimiento:
  - "Identificar la expresión contenida dentro del valor absoluto y asegurarse de que la inecuación tenga la forma $|X| > a$ o $|X| \\geq a$, con $a > 0$."
  - "Aplicar la propiedad del valor absoluto para separar la inecuación original en dos inecuaciones independientes conectadas por una disyunción ('o'): $X > a$ y $X < -a$ (utilizando $\\geq$ y $\\leq$ si corresponde)."
  - "Resolver cada una de las inecuaciones lineales resultantes despejando la incógnita."
  - "Determinar el conjunto solución final uniendo los intervalos obtenidos de ambas inecuaciones, resultando en $S = S_1 \\cup S_2$."
ejemplos:
  - titulo: "Inecuación estricta básica"
    enunciado: "Resuelva la inecuación $|2x - 3| > 5$."
    solucion_pasos:
      - "Se aplica la propiedad separando en dos inecuaciones: $2x - 3 > 5 \\lor 2x - 3 < -5$."
      - "Se resuelve la primera inecuación: $2x > 8 \\implies x > 4$. Su intervalo es $]4, +\\infty[$."
      - "Se resuelve la segunda inecuación: $2x < -2 \\implies x < -1$. Su intervalo es $]-\\infty, -1[$."
      - "El conjunto solución final es la unión de ambos intervalos: $]-\\infty, -1[ \\cup ]4, +\\infty[$."
  - titulo: "Inecuación no estricta"
    enunciado: "Encuentre el conjunto solución de $|x + 4| \\geq 2$."
    solucion_pasos:
      - "Al ser no estricta, la propiedad indica: $x + 4 \\geq 2 \\lor x + 4 \\leq -2$."
      - "Resolviendo la primera inecuación: $x \\geq -2$. Esto corresponde al intervalo $[-2, +\\infty[$."
      - "Resolviendo la segunda inecuación: $x \\leq -6$. Esto corresponde al intervalo $]-\\infty, -6]$."
      - "La solución completa es la unión de ambas regiones: $]-\\infty, -6] \\cup [-2, +\\infty[$."
  - titulo: "¿El número $0$ pertenece al conjunto solución de $|x - 5| > 4$?"
    respuesta: "Sí"
    solucion_pasos:
      - "Se reemplaza $x = 0$ en la expresión dentro del valor absoluto: $|0 - 5| = |-5|$."
      - "Se calcula el valor absoluto: $|-5| = 5$."
      - "Se verifica si cumple la inecuación original evaluando la proposición resultante: $5 > 4$."
      - "Como la desigualdad $5 > 4$ es verdadera, el número $0$ efectivamente pertenece al conjunto solución."
  - titulo: "¿La inecuación $|x| > 3$ es equivalente al sistema de inecuaciones simultáneas $x > 3$ y $x < -3$?"
    respuesta: "No"
    solucion_pasos:
      - "La propiedad del valor absoluto establece que la solución es la unión, es decir, la disyunción lógica 'o' ($x > 3 \\lor x < -3$)."
      - "Un sistema simultáneo implicaría buscar números que sean mayores a $3$ y menores a $-3$ al mismo tiempo."
      - "Dado que ningún número real puede ser simultáneamente mayor a $3$ y menor a $-3$, la intersección sería el conjunto vacío."
      - "Por lo tanto, la expresión equivalente correcta es una disyunción ('o'), no un sistema simultáneo ('y')."
errores_frecuentes:
  - "Resolver la inecuación expresando $-a < X < a$, confundiendo la propiedad con la correspondiente a las inecuaciones de la forma $|X| < a$."
  - "Mantener el mismo sentido de la desigualdad al plantear el caso negativo, escribiendo $X > -a$ en lugar de $X < -a$."
  - "Intersectar los conjuntos solución de las dos inecuaciones lineales en lugar de unirlos, lo que a menudo resulta erróneamente en un conjunto vacío."
  - "Olvidar resolver ambos casos, analizando únicamente el caso directo donde el argumento del valor absoluto se asume positivo ($X > a$)."
  - "Evaluar un punto interior del intervalo intermedio $[-a, a]$ y considerarlo equivocadamente como parte de la solución."
fuente: "Creación propia"
estado: publicado""",
        "jsonl": [
            {
                "id": "VALABS-GEN-CONCEPT-1",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Según su definición geométrica, ¿cómo se interpreta la inecuación $|x| > a$, donde $a > 0$?",
                "opciones": [
                    {"texto": "Como los puntos de la recta cuya distancia al origen es estrictamente mayor que $a$.", "correcta": True},
                    {"texto": "Como los puntos de la recta cuya distancia al origen es estrictamente menor que $a$.", "correcta": False},
                    {"texto": "Como los puntos ubicados entre $-a$ y $a$, ambos inclusive.", "correcta": False},
                    {"texto": "Como los puntos cuya distancia al número $a$ es mayor a cero.", "correcta": False}
                ],
                "resolucion": "El valor absoluto $|x|$ representa la distancia desde el número $x$ hasta el cero. Por tanto, $|x| > a$ se interpreta como el conjunto de números que se encuentran a una distancia del origen mayor que $a$ unidades."
            },
            {
                "id": "VALABS-GEN-CONCEPT-2",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "¿A qué estructura lógica es equivalente la inecuación $|x| > a$ con $a > 0$?",
                "opciones": [
                    {"texto": "A la disyunción lógica $x > a \\lor x < -a$.", "correcta": True},
                    {"texto": "A la conjunción lógica $x > a \\land x < -a$.", "correcta": False},
                    {"texto": "A la doble desigualdad $-a < x < a$.", "correcta": False},
                    {"texto": "A la igualdad $x = a$ y $x = -a$.", "correcta": False}
                ],
                "resolucion": "Para que la distancia sea mayor que $a$, el número debe encontrarse a la derecha de $a$ o a la izquierda de $-a$. Esta opción alternativa se expresa lógicamente mediante una disyunción ('o'), representada por el símbolo $\\lor$."
            },
            {
                "id": "VALABS-GEN-CONCEPT-3",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "¿Qué tipo de conjunto suele representar el resultado de una inecuación de la forma $|x| \\geq a$, con $a > 0$?",
                "opciones": [
                    {"texto": "La unión de dos intervalos disjuntos e infinitos.", "correcta": True},
                    {"texto": "Un único intervalo cerrado y acotado.", "correcta": False},
                    {"texto": "El conjunto de los números reales sin considerar un único punto.", "correcta": False},
                    {"texto": "Siempre el conjunto vacío.", "correcta": False}
                ],
                "resolucion": "La solución se separa en los valores menores o iguales a $-a$ y los valores mayores o iguales a $a$. Esto corresponde a los intervalos $]-\\infty, -a]$ y $[a, +\\infty[$. Como se satisfacen con una condición u otra, el conjunto final es la unión disjunta de ambos."
            },
            {
                "id": "VALABS-GEN-RECON-1",
                "tipo": "reconocimiento",
                "nivel": 1,
                "enunciado": "¿Cuál de las siguientes expresiones es equivalente a la inecuación $|3x - 2| > 4$?",
                "opciones": [
                    {"texto": "$3x - 2 > 4 \\lor 3x - 2 < -4$", "correcta": True},
                    {"texto": "$-4 < 3x - 2 < 4$", "correcta": False},
                    {"texto": "$3x - 2 > 4 \\land 3x - 2 < -4$", "correcta": False},
                    {"texto": "$3x - 2 > 4 \\lor 3x - 2 > -4$", "correcta": False}
                ],
                "resolucion": "Aplicando la propiedad de valor absoluto $|X| > a \\iff X > a \\lor X < -a$, sustituimos $X = 3x - 2$ y $a = 4$, obteniendo directamente $3x - 2 > 4 \\lor 3x - 2 < -4$."
            },
            {
                "id": "VALABS-GEN-PROC-1",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El conjunto solución de la inecuación $|x| > 5$ corresponde al intervalo $]-5, 5[$.",
                "respuesta": False,
                "resolucion": "El intervalo $]-5, 5[$ representa los números cuya distancia al origen es menor a $5$, es decir, la solución de $|x| < 5$. La solución correcta de $|x| > 5$ es $]-\\infty, -5[ \\cup ]5, +\\infty[$. La afirmación es falsa."
            },
            {
                "id": "VALABS-GEN-PROC-2",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "La inecuación $|x + 1| \\geq 3$ incluye en su conjunto solución a los números $x = 2$ y $x = -4$.",
                "respuesta": True,
                "resolucion": "Si evaluamos $x = 2$: $|2 + 1| = |3| = 3 \\geq 3$ (verdadero). Si evaluamos $x = -4$: $|-4 + 1| = |-3| = 3 \\geq 3$ (verdadero). Ambos valores satisfacen la condición, por lo que la afirmación es verdadera."
            },
            {
                "id": "VALABS-GEN-PROC-3",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "Para resolver la inecuación $|2x| > 8$, el procedimiento correcto establece que se debe plantear el sistema simultáneo: $2x > 8$ y $2x < -8$.",
                "respuesta": False,
                "resolucion": "Un sistema simultáneo implica la conjunción ('y'), es decir, que ambas condiciones se cumplan al mismo tiempo. Ningún número puede cumplir $2x > 8$ y $2x < -8$ simultáneamente. El procedimiento correcto emplea la disyunción ('o' o unión de intervalos). Por lo tanto, la afirmación es falsa."
            },
            {
                "id": "VALABS-GEN-PAES-1",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "¿Cuál de los siguientes intervalos o uniones corresponde al conjunto solución de la inecuación $|2x - 5| \\geq 3$?",
                "opciones": [
                    {"texto": "$]-\\infty, 1] \\cup [4, +\\infty[$", "correcta": True},
                    {"texto": "$[1, 4]$", "correcta": False},
                    {"texto": "$]-\\infty, -1] \\cup [4, +\\infty[$", "correcta": False},
                    {"texto": "$]1, 4[$", "correcta": False}
                ],
                "resolucion": "Separando en dos inecuaciones: $2x - 5 \\geq 3 \\lor 2x - 5 \\leq -3$. Para la primera: $2x \\geq 8 \\implies x \\geq 4$. Para la segunda: $2x \\leq 2 \\implies x \\leq 1$. Uniendo ambos resultados obtenemos $]-\\infty, 1] \\cup [4, +\\infty[$."
            },
            {
                "id": "VALABS-GEN-PAES-2",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "En una fábrica, el diámetro $x$ de una pieza, medido en milímetros, se rechaza y desecha si la diferencia absoluta entre el diámetro y la medida estándar de $20$ mm es mayor a $0,5$ mm. ¿Cuál inecuación representa correctamente los diámetros de las piezas rechazadas?",
                "opciones": [
                    {"texto": "$|x - 20| > 0,5$", "correcta": True},
                    {"texto": "$|x - 0,5| > 20$", "correcta": False},
                    {"texto": "$|x - 20| \\leq 0,5$", "correcta": False},
                    {"texto": "$x - 20 > 0,5$", "correcta": False}
                ],
                "resolucion": "La 'diferencia absoluta' entre la medida $x$ y el estándar $20$ se escribe como $|x - 20|$. El criterio de rechazo se activa si esta diferencia es mayor estricta a la tolerancia de $0,5$. Así, la inecuación es $|x - 20| > 0,5$. Las piezas que aprueban estarían dadas por la inecuación contraria $|x - 20| \\leq 0,5$."
            },
            {
                "id": "VALABS-GEN-PAES-3",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Si $k$ es una constante real positiva, ¿cuál es el conjunto solución de la inecuación $|x - k| > 2k$?",
                "opciones": [
                    {"texto": "$]-\\infty, -k[ \\cup ]3k, +\\infty[$", "correcta": True},
                    {"texto": "$]-k, 3k[$", "correcta": False},
                    {"texto": "$]-\\infty, k[ \\cup ]3k, +\\infty[$", "correcta": False},
                    {"texto": "$]-\\infty, -k] \\cup [3k, +\\infty[$", "correcta": False}
                ],
                "resolucion": "Aplicando la propiedad $|X| > a$, se obtiene la disyunción: $x - k > 2k \\lor x - k < -2k$. Resolviendo la primera parte: $x > 3k$. Resolviendo la segunda: $x < -2k + k \\implies x < -k$. La unión de los intervalos correspondientes a $x < -k$ y $x > 3k$ es $]-\\infty, -k[ \\cup ]3k, +\\infty[$."
            }
        ]
    }
}

if __name__ == '__main__':
    for sem_id, content in topics.items():
        print(f"[{sem_id}] JSONL count: {len(content['jsonl'])}")
        print(f"[{sem_id}] YAML size: {len(content['yaml'])}")

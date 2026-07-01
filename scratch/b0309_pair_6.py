topics = {
    "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE": {
        "yaml": r"""semantic_id: MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE
titulo: Multiplicación por números negativos y despeje en inecuaciones lineales
objetivo: Comprender y aplicar la regla de inversión del sentido de la desigualdad al multiplicar o dividir por un número negativo.
introduccion: En el trabajo con inecuaciones, una de las diferencias más importantes respecto a las ecuaciones es el comportamiento ante operaciones con números negativos, lo que garantiza la conservación de las relaciones de orden.
resumen: Al resolver inecuaciones lineales, multiplicar o dividir ambos lados por un número negativo obliga a invertir el signo de desigualdad para mantener la validez de la proposición matemática.
explicacion: |
  ### Definición formal
  Dada una inecuación de la forma $a x < b$, si $a < 0$, al dividir ambos miembros por $a$ (lo que equivale a multiplicar por $1/a$, siendo $1/a < 0$), la relación de orden se invierte, resultando en $x > b/a$. En general, si $x < y$ y $c < 0$, entonces $x \cdot c > y \cdot c$.

  ### Desarrollo didáctico
  Las inecuaciones representan balanzas en desequilibrio. Cuando aplicamos una operación que preserva el orden, el desequilibrio se mantiene en la misma dirección. Sin embargo, los números negativos invierten la posición relativa de los números en la recta numérica. Por ello, una desigualdad verdadera como $2 < 5$ se transforma en $-2 > -5$ al multiplicar por $-1$. Este principio se extiende al despejar variables: si tenemos un coeficiente negativo multiplicando a la incógnita, debemos revertir la dirección de la desigualdad al pasarlo dividiendo (o multiplicando) para encontrar el intervalo solución correcto.
procedimiento:
  - Aislar el término que contiene la variable en uno de los lados de la inecuación usando sumas o restas.
  - Identificar el coeficiente que multiplica a la variable.
  - Si el coeficiente es negativo, multiplicar o dividir ambos lados por dicho coeficiente e invertir inmediatamente el sentido del signo de desigualdad.
  - Simplificar el resultado y expresar la solución en forma de intervalo o conjunto, según sea requerido.
ejemplos:
  - titulo: Despeje con coeficiente negativo simple
    enunciado: Resuelve la inecuación $-3x < 12$.
    solucion_pasos:
      - Dividimos ambos lados por $-3$.
      - Como $-3$ es negativo, invertimos el signo de menor que a mayor que.
      - Obtenemos $x > -4$.
  - titulo: Inecuación con términos compuestos
    enunciado: Encuentra el conjunto solución para $5 - 2x \geq 11$.
    solucion_pasos:
      - Restamos $5$ en ambos lados: $-2x \geq 6$.
      - Dividimos entre $-2$ y simultáneamente invertimos el signo de desigualdad.
      - La solución final es $x \leq -3$.
  - titulo: ¿Se mantiene la desigualdad?
    respuesta: "No"
    solucion_pasos:
      - Observamos la proposición: Si $-x < 4$, entonces $x < -4$.
      - Al multiplicar por $-1$, debemos invertir el signo de desigualdad.
      - El resultado correcto es $x > -4$.
  - titulo: ¿Es correcto el sentido de la desigualdad?
    respuesta: "Sí"
    solucion_pasos:
      - Evaluamos: Si $-5x \geq -15$, entonces $x \leq 3$.
      - Al dividir ambos lados entre $-5$ (número negativo), el signo $\geq$ debe cambiar a $\leq$.
      - Operando se obtiene $x \leq 3$, por lo que el proceso es correcto.
errores_frecuentes:
  - "Pasar dividiendo un número negativo sin cambiar el sentido de la desigualdad."
  - "Invertir la desigualdad al restar un número negativo en ambos lados."
  - "Cambiar el signo de la desigualdad cuando se divide por un número positivo si el otro lado es negativo."
  - "Creer que el signo de desigualdad se invierte solo al trabajar con fracciones negativas."
  - "Olvidar el signo negativo al realizar la división y además no invertir la desigualdad."
fuente: "Elaboración propia"
estado: publicado
""",
        "jsonl": [
            {
                "stable_id": "INEC-MULT-CON-1",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Si $x < y$ y $k < 0$, ¿cuál de las siguientes afirmaciones es correcta según las propiedades de las desigualdades?",
                "opciones": [
                    {"texto": "$kx < ky$", "correcta": False},
                    {"texto": "$kx > ky$", "correcta": True},
                    {"texto": "$kx \\leq ky$", "correcta": False},
                    {"texto": "$kx = ky$", "correcta": False}
                ],
                "solucion_pasos": ["Multiplicar una desigualdad por un número negativo invierte su sentido.", "Por lo tanto, $x < y$ pasa a ser $kx > ky$."]
            },
            {
                "stable_id": "INEC-MULT-CON-2",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "¿Qué ocurre con la representación en la recta numérica de una inecuación si dividimos ambos miembros por $-1$?",
                "opciones": [
                    {"texto": "Los valores se reflejan respecto al cero y el sentido de la desigualdad se mantiene igual.", "correcta": False},
                    {"texto": "Los valores se reflejan respecto al cero y el sentido de la desigualdad se invierte.", "correcta": True},
                    {"texto": "Los valores se acercan al origen pero mantienen el mismo orden.", "correcta": False},
                    {"texto": "La desigualdad deja de tener sentido geométrico.", "correcta": False}
                ],
                "solucion_pasos": ["Dividir por $-1$ cambia el signo de todos los términos, lo que geométricamente es una reflexión respecto al origen.", "Para mantener la relación de orden verdadera, el sentido de la desigualdad debe invertirse."]
            },
            {
                "stable_id": "INEC-MULT-CON-3",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "En la resolución de una inecuación, ¿cuál de las siguientes operaciones obliga a invertir el signo de desigualdad?",
                "opciones": [
                    {"texto": "Restar un número negativo a ambos lados.", "correcta": False},
                    {"texto": "Multiplicar ambos lados por el recíproco de una fracción positiva.", "correcta": False},
                    {"texto": "Dividir ambos lados entre una constante estrictamente menor que cero.", "correcta": True},
                    {"texto": "Sumar un valor absoluto a ambos lados.", "correcta": False}
                ],
                "solucion_pasos": ["Sumar o restar cualquier número no altera la desigualdad.", "Dividir por un número negativo (constante menor que cero) obliga a invertir el signo."]
            },
            {
                "stable_id": "INEC-MULT-REC-1",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE",
                "tipo": "reconocimiento",
                "nivel": 1,
                "enunciado": "Identifica la inecuación equivalente a $-4x \\geq 8$.",
                "opciones": [
                    {"texto": "$x \\geq -2$", "correcta": False},
                    {"texto": "$x \\leq -2$", "correcta": True},
                    {"texto": "$x > -2$", "correcta": False},
                    {"texto": "$x \\leq 2$", "correcta": False}
                ],
                "solucion_pasos": ["Dividimos ambos lados entre $-4$.", "Al ser $-4$ negativo, cambiamos $\\geq$ por $\\leq$.", "Resulta $x \\leq -2$."]
            },
            {
                "stable_id": "INEC-MULT-PRO-1",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "La solución de la inecuación $7 - 3x < 1$ es $x < 2$.",
                "respuesta_booleana": False,
                "solucion_pasos": ["Restamos $7$ a ambos lados: $-3x < -6$.", "Dividimos entre $-3$ e invertimos el signo: $x > 2$.", "La afirmación es falsa porque no se invirtió el signo de desigualdad."]
            },
            {
                "stable_id": "INEC-MULT-PRO-2",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "La inecuación $-\\frac{x}{2} \\geq 4$ equivale a $x \\leq -8$.",
                "respuesta_booleana": True,
                "solucion_pasos": ["Multiplicamos ambos lados por $-2$.", "Como multiplicamos por un número negativo, invertimos $\\geq$ a $\\leq$.", "Obtenemos $x \\leq -8$, por lo que es verdadero."]
            },
            {
                "stable_id": "INEC-MULT-PRO-3",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "Al resolver $5(1 - x) > 15$, se obtiene como solución el intervalo $(-\\infty, -2)$.",
                "respuesta_booleana": True,
                "solucion_pasos": ["Dividimos entre $5$ positivo (no cambia el signo): $1 - x > 3$.", "Restamos $1$: $-x > 2$.", "Multiplicamos por $-1$ e invertimos el signo: $x < -2$.", "Esto corresponde al intervalo $(-\\infty, -2)$. Es verdadero."]
            },
            {
                "stable_id": "INEC-MULT-PAE-1",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Considera la inecuación $a x + b > c$, donde $a < 0$. ¿Qué condición debe cumplirse para que el conjunto solución sea el intervalo $(-\\infty, 0)$?",
                "opciones": [
                    {"texto": "$b = c$", "correcta": True},
                    {"texto": "$b > c$", "correcta": False},
                    {"texto": "$a = b - c$", "correcta": False},
                    {"texto": "$c = 0$", "correcta": False}
                ],
                "solucion_pasos": ["Restamos $b$ en ambos lados: $a x > c - b$.", "Dividimos entre $a$. Como $a < 0$, invertimos el signo: $x < \\frac{c - b}{a}$.", "Para que el intervalo sea $(-\\infty, 0)$, necesitamos que $\\frac{c - b}{a} = 0$.", "Esto implica que $c - b = 0$, es decir, $b = c$."]
            },
            {
                "stable_id": "INEC-MULT-PAE-2",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "El conjunto solución de la inecuación $\\frac{2 - 3x}{-4} \\leq -1$ es:",
                "opciones": [
                    {"texto": "$[ -\\frac{2}{3}, \\infty )$", "correcta": False},
                    {"texto": "$( -\\infty, -\\frac{2}{3} ]$", "correcta": True},
                    {"texto": "$[ \\frac{2}{3}, \\infty )$", "correcta": False},
                    {"texto": "$( -\\infty, \\frac{2}{3} ]$", "correcta": False}
                ],
                "solucion_pasos": ["Multiplicamos ambos lados por $-4$.", "Dado que es un número negativo, cambiamos el sentido: $2 - 3x \\geq 4$.", "Restamos $2$: $-3x \\geq 2$.", "Dividimos por $-3$ e invertimos nuevamente: $x \\leq -\\frac{2}{3}$.", "El conjunto solución corresponde al intervalo $(-\\infty, -\\frac{2}{3} ]$."]
            },
            {
                "stable_id": "INEC-MULT-PAE-3",
                "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.MULTIPLICACION_NEGATIVA_DESPEJE",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Si $m < n < 0$, ¿cuál es el conjunto solución para la inecuación $(m-n)x \\leq m^2 - n^2$?",
                "opciones": [
                    {"texto": "$x \\leq m + n$", "correcta": False},
                    {"texto": "$x \\geq m + n$", "correcta": True},
                    {"texto": "$x \\geq m - n$", "correcta": False},
                    {"texto": "$x \\leq m - n$", "correcta": False}
                ],
                "solucion_pasos": ["Factorizamos el lado derecho: $(m-n)x \\leq (m-n)(m+n)$.", "Como $m < n$, se tiene que $m - n < 0$.", "Al dividir ambos lados por el factor negativo $(m-n)$, el sentido de la desigualdad se invierte.", "Resulta $x \\geq m + n$."]
            }
        ]
    },
    "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA": {
        "yaml": r"""semantic_id: MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA
titulo: Representación gráfica de sistemas de inecuaciones en la recta numérica
objetivo: Graficar e intersectar conjuntos solución de inecuaciones lineales en una misma recta numérica para determinar la solución del sistema.
introduccion: Un sistema de inecuaciones lineales se compone de varias inecuaciones que deben cumplirse simultáneamente. Su resolución requiere encontrar los valores comunes que satisfacen todas las condiciones, siendo la recta numérica la herramienta gráfica ideal para visualizar esta intersección.
resumen: La solución gráfica de un sistema de inecuaciones de una variable se obtiene trazando los intervalos solución de cada inecuación sobre una misma recta y determinando la región donde se solapan (intersección).
explicacion: |
  ### Definición formal
  Dado un sistema formado por inecuaciones $\{ I_1, I_2, \dots, I_n \}$ con conjuntos solución respectivos $S_1, S_2, \dots, S_n$, el conjunto solución del sistema $S$ es la intersección de estos conjuntos: $S = S_1 \cap S_2 \cap \dots \cap S_n$. Gráficamente, esto equivale al segmento de la recta real que está sombreado simultáneamente por todos los intervalos involucrados.

  ### Desarrollo didáctico
  Para visualizar un sistema, dibujamos una única recta real. Asignamos a cada inecuación una representación gráfica sobre ella, utilizando un círculo vacío para desigualdades estrictas ($<$ o $>$) y un círculo relleno para aquellas que incluyen la igualdad ($\leq$ o $\geq$). A partir de cada punto crítico, extendemos una línea o zona sombreada hacia la dirección que indique la desigualdad. La solución final del sistema corresponde exclusivamente a aquella parte de la recta donde todas las líneas coinciden o se superponen. Si no existe ninguna zona de superposición total, el sistema no tiene solución (conjunto vacío).
procedimiento:
  - Resolver cada inecuación del sistema por separado hasta obtener su intervalo solución.
  - Trazar una recta numérica marcando los valores críticos obtenidos.
  - Graficar sobre la recta cada intervalo con distintos trazos o alturas, prestando atención al uso de puntos abiertos (sin incluir) y cerrados (incluidos).
  - Identificar visualmente la región de la recta que está cubierta por las gráficas de todas las inecuaciones.
  - Escribir el intervalo correspondiente a esa región común como el conjunto solución del sistema.
ejemplos:
  - titulo: Sistema con solución acotada
    enunciado: Resuelve gráficamente el sistema formado por $x > 2$ y $x \leq 5$.
    solucion_pasos:
      - En la recta numérica, marcamos un círculo abierto en $2$ y sombreamos hacia la derecha.
      - Marcamos un círculo cerrado en $5$ y sombreamos hacia la izquierda.
      - La zona donde ambos sombreados coinciden es desde el $2$ (sin incluir) hasta el $5$ (incluido).
      - El conjunto solución es $(2, 5]$.
  - titulo: Sistema sin solución
    enunciado: Representa y resuelve el sistema dado por $x < -1$ y $x \geq 3$.
    solucion_pasos:
      - Dibujamos la recta numérica. Desde $-1$, con círculo abierto, sombreamos hacia la izquierda.
      - Desde $3$, con círculo cerrado, sombreamos hacia la derecha.
      - Observamos que no existe ninguna región superpuesta entre ambos gráficos.
      - El sistema no tiene solución (conjunto vacío $\emptyset$).
  - titulo: ¿Corresponde el intervalo a la intersección?
    respuesta: "Sí"
    solucion_pasos:
      - Analizamos el sistema $2x \geq 4$ y $x < 6$.
      - Resolvemos la primera: $x \geq 2$. La segunda ya está despejada: $x < 6$.
      - La representación visual de $x \geq 2$ y $x < 6$ se solapa entre el $2$ y el $6$.
      - La intersección es correcta: $[2, 6)$.
  - titulo: ¿Es correcto el gráfico resultante?
    respuesta: "No"
    solucion_pasos:
      - Sistema: $x > 0$ y $x > 4$. Se afirma que la solución es el intervalo $(0, 4)$.
      - Trazamos $x > 0$ (derecha desde $0$) y $x > 4$ (derecha desde $4$).
      - La región donde ambos coinciden inicia en $4$ y continúa hasta el infinito.
      - El conjunto solución real es $(4, \infty)$, no $(0, 4)$.
errores_frecuentes:
  - "Unir (sumar) los intervalos en lugar de buscar la zona de intersección."
  - "Confundir los puntos abiertos y cerrados al leer la intersección gráfica en los extremos."
  - "Asumir erróneamente que un sistema siempre tiene solución."
  - "Olvidar resolver las inecuaciones previamente y tratar de graficar directamente expresiones sin despejar."
  - "Identificar como solución una zona donde se cumple solo una inecuación de un sistema de tres o más."
fuente: "Elaboración propia"
estado: publicado
""",
        "jsonl": [
            {
                "stable_id": "SIST-REP-CON-1",
                "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "En la representación gráfica de un sistema de inecuaciones lineales, la solución del sistema se determina buscando:",
                "opciones": [
                    {"texto": "La unión de todos los intervalos graficados.", "correcta": False},
                    {"texto": "La zona donde se superponen simultáneamente las gráficas de todas las inecuaciones.", "correcta": True},
                    {"texto": "Los puntos donde las inecuaciones toman el valor de cero.", "correcta": False},
                    {"texto": "El segmento entre los valores más extremos de la recta.", "correcta": False}
                ],
                "solucion_pasos": ["Un sistema de inecuaciones exige que todas las condiciones se cumplan a la vez.", "Gráficamente, esto significa encontrar la región común a todos los intervalos, es decir, su intersección."]
            },
            {
                "stable_id": "SIST-REP-CON-2",
                "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "¿Qué ocurre si, al graficar dos inecuaciones en la recta numérica, sus respectivos trazos apuntan en direcciones opuestas y no se cruzan en ningún punto?",
                "opciones": [
                    {"texto": "La solución abarca todos los números reales.", "correcta": False},
                    {"texto": "La solución se determina calculando el punto medio entre ambos intervalos.", "correcta": False},
                    {"texto": "El sistema no tiene solución real.", "correcta": True},
                    {"texto": "Solo se considera válida la inecuación con el mayor conjunto de valores.", "correcta": False}
                ],
                "solucion_pasos": ["Si los trazos no se cruzan, no hay ningún valor que satisfaga ambas condiciones al mismo tiempo.", "Por lo tanto, la intersección es vacía y el sistema no tiene solución."]
            },
            {
                "stable_id": "SIST-REP-CON-3",
                "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": "Para graficar la intersección en un punto crítico donde una inecuación usa $<$ y otra usa $\\leq$, ¿qué símbolo representa correctamente ese extremo en el intervalo solución si la zona sombreada cubre desde ese punto hacia el mismo lado?",
                "opciones": [
                    {"texto": "Corchete $[$ para incluirlo.", "correcta": False},
                    {"texto": "Llaves $\\{$ $\\}$.", "correcta": False},
                    {"texto": "No importa cuál se use, ambos son válidos.", "correcta": False},
                    {"texto": "Paréntesis $($ para excluirlo.", "correcta": True}
                ],
                "solucion_pasos": ["Para que un punto sea parte de la solución de un sistema, debe cumplir TODAS las inecuaciones.", "Dado que el símbolo $<$ excluye al número, este no pertenece a ese conjunto, y por ende, no puede estar en la intersección.", "Se usa paréntesis para indicar que el punto no está incluido."]
            },
            {
                "stable_id": "SIST-REP-REC-1",
                "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA",
                "tipo": "reconocimiento",
                "nivel": 1,
                "enunciado": "Se grafican en la recta numérica las regiones $x > 1$ y $x \\leq 4$. ¿Cuál es el conjunto solución que se observa en la intersección?",
                "opciones": [
                    {"texto": "$(1, 4]$", "correcta": True},
                    {"texto": "$[1, 4]$", "correcta": False},
                    {"texto": "$(1, 4)$", "correcta": False},
                    {"texto": "$[1, 4)$", "correcta": False}
                ],
                "solucion_pasos": ["La primera condición es $x > 1$, que corresponde a un intervalo abierto en $1$.", "La segunda es $x \\leq 4$, correspondiente a un intervalo cerrado en $4$.", "La región solapada inicia en $1$ (abierto) y termina en $4$ (cerrado), es decir, $(1, 4]$."]
            },
            {
                "stable_id": "SIST-REP-PRO-1",
                "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "El sistema formado por $x \\geq -2$ y $x \\geq 3$ tiene como solución gráfica el intervalo $[-2, 3]$.",
                "respuesta_booleana": False,
                "solucion_pasos": ["Graficamos ambas condiciones: una raya hacia la derecha desde $-2$ y otra hacia la derecha desde $3$.", "La región de intersección, donde ambas rayas se superponen, comienza en $3$ hacia el infinito.", "La solución correcta es $[3, \\infty)$, por lo que la afirmación es falsa."]
            },
            {
                "stable_id": "SIST-REP-PRO-2",
                "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "Al representar el sistema de inecuaciones $-x < 5$ y $2x \\leq 12$, la intersección en la recta determina la solución $(-5, 6]$.",
                "respuesta_booleana": True,
                "solucion_pasos": ["Despejamos la primera inecuación: $-x < 5 \\Rightarrow x > -5$.", "Despejamos la segunda: $2x \\leq 12 \\Rightarrow x \\leq 6$.", "La gráfica superpone un rayo que va desde $-5$ (abierto) a la derecha, con uno que va desde $6$ (cerrado) a la izquierda.", "La intersección es exactamente el intervalo $(-5, 6]$. Es verdadero."]
            },
            {
                "stable_id": "SIST-REP-PRO-3",
                "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": "Si graficamos $x < 0$, $x > -4$ y $x \\leq 2$, la solución común corresponde al intervalo $(-4, 0)$.",
                "respuesta_booleana": True,
                "solucion_pasos": ["Graficamos las tres inecuaciones simultáneamente.", "La intersección de las dos primeras es $(-4, 0)$.", "La tercera inecuación abarca todo número menor o igual a $2$, lo cual incluye al intervalo $(-4, 0)$.", "Por tanto, la intersección de las tres es efectivamente $(-4, 0)$."]
            },
            {
                "stable_id": "SIST-REP-PAE-1",
                "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Considera el sistema de inecuaciones:\\n1) $3(x - 1) < 2x + 4$\\n2) $\\frac{x+2}{2} \\geq x - 1$\\n¿Cuál de las siguientes representaciones en notación de intervalo corresponde a la gráfica de su conjunto solución?",
                "opciones": [
                    {"texto": "$( -\\infty, 4 ]$", "correcta": True},
                    {"texto": "$( -\\infty, 7 )$", "correcta": False},
                    {"texto": "$[ 4, 7 )$", "correcta": False},
                    {"texto": "$( 4, 7 ]$", "correcta": False}
                ],
                "solucion_pasos": ["Resolvemos la primera inecuación: $3x - 3 < 2x + 4 \\Rightarrow x < 7$.", "Resolvemos la segunda: $x + 2 \\geq 2(x - 1) \\Rightarrow x + 2 \\geq 2x - 2 \\Rightarrow 4 \\geq x \\Rightarrow x \\leq 4$.", "En la recta numérica, graficamos $x < 7$ y $x \\leq 4$.", "La intersección es la región que cumple ambas. Como todos los números menores que $4$ son también menores que $7$, la solución es $(-\\infty, 4]$."]
            },
            {
                "stable_id": "SIST-REP-PAE-2",
                "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Un sistema de inecuaciones en la variable $x$ se grafica sobre una recta obteniendo que la primera inecuación cubre $[a, \\infty)$ y la segunda cubre $(-\\infty, b]$. Si se sabe que el sistema carece de solución real, ¿qué relación existe necesariamente entre $a$ y $b$?",
                "opciones": [
                    {"texto": "$a < b$", "correcta": False},
                    {"texto": "$a > b$", "correcta": True},
                    {"texto": "$a = b$", "correcta": False},
                    {"texto": "$a \\geq b$", "correcta": False}
                ],
                "solucion_pasos": ["Si $a < b$, los intervalos se solapan en $[a, b]$, luego habría solución.", "Si $a = b$, la intersección sería el único punto $x = a = b$, también habría solución.", "Para que no exista solapamiento (intersección vacía), el punto de inicio de la primera ($a$) debe ser mayor estricto que el punto de finalización de la segunda ($b$).", "Por lo tanto, la relación debe ser $a > b$."]
            },
            {
                "stable_id": "SIST-REP-PAE-3",
                "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.REPRESENTACION_RECTA",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": "Se requiere que un rectángulo tenga un perímetro inferior a $30$ cm y que su longitud sea al menos de $8$ cm. Si el ancho se denota por $y$, ¿cuál es el gráfico en la recta numérica que define los posibles valores de $y$ (considerando que el ancho debe ser positivo)?",
                "opciones": [
                    {"texto": "Un intervalo abierto desde $0$ hasta $7$: $(0, 7)$.", "correcta": True},
                    {"texto": "Un intervalo cerrado desde $0$ hasta $7$: $[0, 7]$.", "correcta": False},
                    {"texto": "Un intervalo desde $7$ al infinito: $(7, \\infty)$.", "correcta": False},
                    {"texto": "Un intervalo desde $0$ hasta $15$: $(0, 15)$.", "correcta": False}
                ],
                "solucion_pasos": ["El perímetro es $2(L + y) < 30 \\Rightarrow L + y < 15$.", "Sabemos que $L \\geq 8$. Para maximizar el ancho $y$, usamos la longitud mínima: $8 + y < 15 \\Rightarrow y < 7$.", "Además, por contexto geométrico, el ancho debe ser positivo, por lo que $y > 0$.", "La intersección de las condiciones $y > 0$ e $y < 7$ es el intervalo $(0, 7)$."]
            }
        ]
    }
}

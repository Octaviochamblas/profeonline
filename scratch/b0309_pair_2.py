topics = {
    "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.DEFINICION": {
        "yaml": r"""semantic_id: MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.DEFINICION
titulo: Definición y Propiedades de las Inecuaciones con Valor Absoluto
objetivo: Comprender la definición de inecuación con valor absoluto y aplicar sus propiedades básicas para plantear el intervalo de soluciones
introduccion: El valor absoluto representa una distancia. Cuando resolvemos inecuaciones con valor absoluto, estamos buscando todos los puntos cuya distancia a un cierto valor cumple una condición determinada, como ser menor o mayor a cierta cantidad.
resumen: Las inecuaciones con valor absoluto involucran expresiones dentro de $|x|$. Su resolución se basa en interpretar el valor absoluto como distancia y usar las propiedades fundamentales para transformarlas en inecuaciones lineales equivalentes.
explicacion: |
  ### Definición formal
  Una inecuación con valor absoluto es una desigualdad que contiene a la incógnita dentro de barras de valor absoluto. Las formas básicas son $|x| < a$, $|x| \le a$, $|x| > a$ y $|x| \ge a$, donde $a$ es un número real positivo.

  Por las propiedades del valor absoluto, estas inecuaciones se traducen de la siguiente manera:
  1. Si $|x| < a$ (con $a > 0$), entonces $-a < x < a$.
  2. Si $|x| > a$ (con $a > 0$), entonces $x < -a$ o $x > a$.

  ### Desarrollo didáctico
  Piensa en $|x|$ como la distancia desde el número $x$ hasta el cero en la recta numérica. Si decimos $|x| < 3$, estamos pidiendo todos los números cuya distancia al cero sea menor que $3$. Visualmente, esto incluye todos los números entre $-3$ y $3$.

  Por otro lado, si decimos $|x| > 3$, buscamos aquellos números que estén a una distancia mayor que $3$ del cero. Esto ocurre para números menores que $-3$ (como el $-4, -5$) y también para números mayores que $3$ (como el $4, 5$).

  Cuando la inecuación involucra una expresión más compleja, como $|x - b| < a$, esto se interpreta como "la distancia entre $x$ y $b$ es menor que $a$". Aplicar las propiedades nos permite eliminar el valor absoluto y resolver las inecuaciones resultantes como lo haríamos normalmente.
procedimiento:
  - "Identificar la expresión con valor absoluto y aislarla a un lado de la desigualdad, si es necesario."
  - "Verificar que la constante del otro lado sea positiva. Si es un número negativo y tenemos un menor que, la solución es vacía; si es mayor que, son todos los reales."
  - "Aplicar la propiedad correspondiente: transformar en una desigualdad doble si es '<' o en dos desigualdades separadas por 'o' si es '>'."
  - "Resolver la inecuación o el par de inecuaciones resultantes para encontrar el intervalo solución final."
ejemplos:
  - titulo: Inecuación de tipo menor que
    enunciado: Resolver la inecuación $|x - 2| < 5$.
    solucion_pasos:
      - "Identificamos que tiene la forma $|X| < a$, donde $X = x - 2$ y $a = 5$."
      - "Aplicamos la propiedad: $-5 < x - 2 < 5$."
      - "Sumamos 2 a todos los miembros de la desigualdad: $-5 + 2 < x - 2 + 2 < 5 + 2$."
      - "Obtenemos $-3 < x < 7$. El intervalo solución es $(-3, 7)$."
  - titulo: Inecuación de tipo mayor o igual que
    enunciado: Resolver la inecuación $|2x + 1| \ge 7$.
    solucion_pasos:
      - "Tiene la forma $|X| \ge a$, lo que se descompone en $X \le -a$ o $X \ge a$."
      - "Planteamos las dos desigualdades: $2x + 1 \le -7$ o $2x + 1 \ge 7$."
      - "Resolvemos la primera: $2x \le -8$, lo que da $x \le -4$."
      - "Resolvemos la segunda: $2x \ge 6$, lo que da $x \ge 3$."
      - "La solución final es la unión de ambos intervalos: $(-\infty, -4] \cup [3, \infty)$."
  - titulo: ¿Es correcto que $|x| < -2$ no tiene solución real?
    respuesta: "Sí"
    solucion_pasos:
      - "El valor absoluto de cualquier número real siempre es mayor o igual a cero (nunca es negativo)."
      - "Por lo tanto, la expresión $|x|$ nunca puede ser estrictamente menor que $-2$."
      - "Concluimos que no hay ningún valor real de $x$ que satisfaga la inecuación, por lo que no tiene solución en los reales."
  - titulo: ¿La inecuación $|x| > -5$ tiene como solución todos los números reales?
    respuesta: "Sí"
    solucion_pasos:
      - "Sabemos que $|x| \ge 0$ para cualquier número real $x$."
      - "Dado que $0 > -5$, se cumple que $|x| \ge 0 > -5$."
      - "Como cualquier número positivo o cero es mayor que $-5$, la inecuación es verdadera para todo $x \in \mathbb{R}$."
errores_frecuentes:
  - "Resolver $|x| > a$ escribiendo la desigualdad compuesta como $-a > x > a$, lo cual es lógicamente inconsistente."
  - "Olvidar cambiar el sentido de la desigualdad cuando se plantea el caso negativo en inecuaciones tipo mayor que."
  - "Ignorar el caso cuando la inecuación se iguala a un número negativo y proceder mecánicamente, obteniendo soluciones falsas."
  - "Tratar el valor absoluto como paréntesis y simplemente suprimirlo, escribiendo $x - 2 < 5$ como única inecuación al resolver $|x - 2| < 5$."
  - "Afirmar que la solución a $|x| < 0$ es todo número real negativo."
fuente: "Elaboración propia"
estado: publicado
""",
        "exercises": [
            {
                "stable_id": "VALABS-GEN-CONCEPT-1",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": r"¿Qué representa geométricamente la inecuación $|x| < a$ para $a > 0$ en la recta numérica?",
                "opciones": [
                    r"Todos los números cuya distancia al cero es menor que $a$.",
                    r"Todos los números cuya distancia al cero es mayor que $a$.",
                    r"Todos los números negativos menores que $a$.",
                    r"Todos los números comprendidos entre $0$ y $a$ exclusivamente."
                ],
                "respuesta_correcta": r"Todos los números cuya distancia al cero es menor que $a$.",
                "explicacion": r"El valor absoluto representa distancia. Así, $|x| < a$ indica que la distancia desde el número $x$ al cero es estrictamente menor que $a$ unidades."
            },
            {
                "stable_id": "VALABS-GEN-CONCEPT-2",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": r"Si $a$ es un número real negativo, ¿cuál es la solución de la inecuación $|x| < a$?",
                "opciones": [
                    r"El conjunto vacío, ya que una distancia no puede ser negativa.",
                    r"Todos los números reales, ya que cualquier valor absoluto es mayor que un negativo.",
                    r"El intervalo $(-a, a)$.",
                    r"Depende del valor específico de $x$."
                ],
                "respuesta_correcta": r"El conjunto vacío, ya que una distancia no puede ser negativa.",
                "explicacion": r"Como $|x| \ge 0$ para todo $x$, no puede ser menor que un número estrictamente negativo. No hay solución."
            },
            {
                "stable_id": "VALABS-GEN-CONCEPT-3",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": r"La inecuación $|x| > a$ (con $a > 0$) equivale algebraicamente a:",
                "opciones": [
                    r"$x < -a$ o $x > a$",
                    r"$-a < x < a$",
                    r"$x > -a$ y $x < a$",
                    r"$x < a$ o $x > -a$"
                ],
                "respuesta_correcta": r"$x < -a$ o $x > a$",
                "explicacion": r"Por propiedad, la distancia mayor que $a$ desde el origen se descompone en los valores situados a la derecha de $a$ o a la izquierda de $-a$."
            },
            {
                "stable_id": "VALABS-GEN-RECON-1",
                "tipo": "reconocimiento",
                "nivel": 1,
                "enunciado": r"Identifica cuál de las siguientes expresiones es una inecuación con valor absoluto que no tiene solución en el conjunto de los números reales.",
                "opciones": [
                    r"$|2x - 3| < -4$",
                    r"$|x + 5| > -2$",
                    r"$|-x| < 3$",
                    r"$|4x| \ge 0$"
                ],
                "respuesta_correcta": r"$|2x - 3| < -4$",
                "explicacion": r"Un valor absoluto nunca es menor que un número negativo. Por tanto, $|2x - 3| < -4$ no tiene solución real."
            },
            {
                "stable_id": "VALABS-GEN-PROC-1",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": r"La solución de $|x| < 4$ es el intervalo $(-4, 4)$.",
                "respuesta_correcta": True,
                "explicacion": r"Por la propiedad de $|x| < a$, la inecuación se convierte en $-4 < x < 4$, lo que corresponde al intervalo $(-4, 4)$."
            },
            {
                "stable_id": "VALABS-GEN-PROC-2",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": r"La inecuación $|x - 1| > 2$ es equivalente a la doble inecuación $-2 < x - 1 < 2$.",
                "respuesta_correcta": False,
                "explicacion": r"El símbolo de mayor que ($>$) genera una disyunción, por lo que es equivalente a $x - 1 < -2$ o $x - 1 > 2$, no a una doble inecuación acotada."
            },
            {
                "stable_id": "VALABS-GEN-PROC-3",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": r"Para resolver $|x + 2| \le 5$, el primer paso lógico es escribir $-5 \le x + 2 \le 5$.",
                "respuesta_correcta": True,
                "explicacion": r"Es la aplicación directa de la propiedad de la desigualdad del valor absoluto para inecuaciones tipo menor o igual, que se transforma en una cadena."
            },
            {
                "stable_id": "VALABS-GEN-PAES-1",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": r"¿Cuál de los siguientes intervalos es el conjunto solución de la inecuación $|x - 4| \le 6$?",
                "opciones": [
                    r"$[-2, 10]$",
                    r"$(-2, 10)$",
                    r"$(-\infty, -2] \cup [10, \infty)$",
                    r"$[2, 10]$",
                    r"$[-10, 2]$"
                ],
                "respuesta_correcta": r"$[-2, 10]$",
                "explicacion": r"Aplicamos la propiedad: $-6 \le x - 4 \le 6$. Sumando 4 a cada término obtenemos $-2 \le x \le 10$, cuyo intervalo es $[-2, 10]$."
            },
            {
                "stable_id": "VALABS-GEN-PAES-2",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": r"Si el conjunto solución de $|x| > p$ es $(-\infty, -3) \cup (3, \infty)$, ¿cuál es el valor de $p$?",
                "opciones": [
                    r"$3$",
                    r"$-3$",
                    r"$0$",
                    r"$9$",
                    r"$6$"
                ],
                "respuesta_correcta": r"$3$",
                "explicacion": r"La inecuación $|x| > p$ tiene solución $x < -p$ o $x > p$. Comparando con la solución dada $(-\infty, -3) \cup (3, \infty)$, vemos claramente que $p = 3$."
            },
            {
                "stable_id": "VALABS-GEN-PAES-3",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": r"¿Para qué valores de $k$ la inecuación $|2x + 1| \le k - 4$ posee una única solución real?",
                "opciones": [
                    r"$k = 4$",
                    r"$k < 4$",
                    r"$k = 0$",
                    r"$k > 4$",
                    r"$k = -4$"
                ],
                "respuesta_correcta": r"$k = 4$",
                "explicacion": r"Una inecuación del tipo $|A| \le B$ tiene una única solución si y solo si $B = 0$. Por tanto, se requiere $k - 4 = 0$, de lo cual se deduce que $k = 4$."
            }
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.RESOLUCION_DESPEJE": {
        "yaml": r"""semantic_id: MAT.ALG.INECUACIONES_LINEALES.RESOLUCION_DESPEJE
titulo: Resolución de Inecuaciones Lineales mediante Despeje
objetivo: Resolver inecuaciones lineales utilizando las propiedades de las desigualdades, prestando especial atención a los cambios de signo
introduccion: Resolver una inecuación lineal es muy similar a resolver una ecuación lineal. El objetivo sigue siendo aislar la incógnita. Sin embargo, en las inecuaciones hay una regla fundamental que marca la diferencia en el proceso.
resumen: El proceso de resolución de inecuaciones lineales se basa en agrupar términos semejantes y despejar la incógnita. Se aplican las mismas operaciones aritméticas que en las ecuaciones, con la única excepción de que multiplicar o dividir ambos miembros por un número negativo cambia la dirección del signo de desigualdad.
explicacion: |
  ### Definición formal
  Una inecuación lineal en una variable, tras agrupar términos, se puede reducir a la forma $ax < b$, $ax \le b$, $ax > b$ o $ax \ge b$.

  Resolverla significa encontrar todos los valores de $x$ que hacen verdadera la desigualdad. Para despejar $x$, se divide por el coeficiente $a$:
  - Si $a > 0$, la dirección de la desigualdad se mantiene. Por ejemplo, de $ax < b$ pasamos a $x < \frac{b}{a}$.
  - Si $a < 0$, la dirección de la desigualdad se invierte. Por ejemplo, de $ax < b$ pasamos a $x > \frac{b}{a}$.

  ### Desarrollo didáctico
  Imagina que tienes una desigualdad verdadera, como $4 > 2$. Si sumas o restas el mismo número a ambos lados, digamos sumamos 1, obtenemos $5 > 3$, y la desigualdad se mantiene correcta. Si multiplicamos por un positivo, digamos 2, obtenemos $8 > 4$, y también se mantiene.

  Pero mira qué sucede si multiplicamos $4 > 2$ por $-1$. Obtenemos $-4$ en la izquierda y $-2$ en la derecha. Si mantuviéramos el signo tendríamos $-4 > -2$, ¡lo cual es falso! El número $-2$ es mayor que $-4$. Por lo tanto, debemos invertir el signo: $-4 < -2$.

  Esta misma lógica aplica cuando despejamos la $x$ en una inecuación algebraicamente. Es el único "cuidado especial" que debemos tener en el despeje en comparación con las ecuaciones normales.
procedimiento:
  - "Eliminar paréntesis y simplificar términos semejantes en ambos lados de la inecuación."
  - "Agrupar todos los términos que contienen la incógnita en un lado de la inecuación (generalmente a la izquierda) y los términos constantes en el otro."
  - "Simplificar nuevamente para dejar un único término con la incógnita y un único número en el otro lado."
  - "Despejar la incógnita dividiendo ambos lados por su coeficiente. Si este coeficiente es negativo, invertir inmediatamente el símbolo de la desigualdad."
ejemplos:
  - titulo: Despeje directo sin cambio de signo
    enunciado: Resolver la inecuación $3x - 5 < 7$.
    solucion_pasos:
      - "Sumamos 5 a ambos lados para agrupar constantes: $3x < 7 + 5$."
      - "Simplificamos: $3x < 12$."
      - "Dividimos ambos lados entre 3, que es positivo (el signo no cambia): $x < \frac{12}{3}$."
      - "Obtenemos $x < 4$. La solución es el intervalo $(-\infty, 4)$."
  - titulo: Despeje con inversión de signo
    enunciado: Resolver la inecuación $2 - 4x \ge 14$.
    solucion_pasos:
      - "Restamos 2 en ambos miembros: $-4x \ge 14 - 2$."
      - "Simplificamos: $-4x \ge 12$."
      - "Dividimos ambos lados entre $-4$. Como estamos dividiendo por un número negativo, debemos invertir el signo de $\ge$ a $\le$."
      - "Calculamos $x \le \frac{12}{-4}$."
      - "Concluimos $x \le -3$. El intervalo solución es $(-\infty, -3]$."
  - titulo: ¿Se debe invertir el signo al restar un número en ambos lados?
    respuesta: "No"
    solucion_pasos:
      - "La propiedad de la suma y resta de desigualdades indica que sumar o restar cualquier número real a ambos lados no altera el sentido de la desigualdad."
      - "Por ejemplo, si tenemos $x + 5 > 2$ y restamos 5, obtenemos $x > -3$."
      - "El signo solo se invierte al multiplicar o dividir por una cantidad negativa."
  - titulo: ¿Es correcto que la solución de $-x < 5$ es $x > -5$?
    respuesta: "Sí"
    solucion_pasos:
      - "La expresión $-x < 5$ equivale a $-1 \cdot x < 5$."
      - "Para despejar $x$, dividimos ambos lados de la inecuación por $-1$."
      - "Como estamos dividiendo por un número negativo, debemos invertir el sentido del menor que al mayor que."
      - "El resultado es $x > -5$, lo cual es una proposición matemática correcta."
errores_frecuentes:
  - "No invertir el sentido de la desigualdad al dividir o multiplicar ambos miembros por un número negativo."
  - "Invertir el símbolo de desigualdad al dividir un lado negativo por un coeficiente positivo (ejemplo: de $2x < -8$ pasar a $x > -4$)."
  - "Al pasar términos sumando o restando (transposición), invertir erróneamente el signo de la desigualdad."
  - "Restar mal los coeficientes algebraicos, como operar $3x - 5x$ y escribir la inecuación sin el signo negativo del coeficiente."
  - "Pensar que un signo menor que siempre corresponde a la izquierda y un mayor que a la derecha independientemente del despeje realizado."
fuente: "Elaboración propia"
estado: publicado
""",
        "exercises": [
            {
                "stable_id": "DESPEJE-GEN-CONCEPT-1",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": r"Al resolver una inecuación lineal, ¿en qué caso específico se debe invertir el sentido de la desigualdad?",
                "opciones": [
                    r"Al multiplicar o dividir ambos miembros por un número negativo.",
                    r"Al sumar un número negativo a ambos lados.",
                    r"Al trasladar un término negativo de un lado a otro.",
                    r"Al multiplicar o dividir ambos miembros por cualquier número real."
                ],
                "respuesta_correcta": r"Al multiplicar o dividir ambos miembros por un número negativo.",
                "explicacion": r"La regla de inversión de las desigualdades únicamente aplica cuando las operaciones de multiplicación o división involucran factores estrictamente negativos."
            },
            {
                "stable_id": "DESPEJE-GEN-CONCEPT-2",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": r"Si $c < 0$ y partimos de la desigualdad verdadera $a > b$, ¿qué afirmación se cumple siempre?",
                "opciones": [
                    r"$ac < bc$",
                    r"$ac > bc$",
                    r"$a + c < b + c$",
                    r"$\frac{a}{c} > \frac{b}{c}$"
                ],
                "respuesta_correcta": r"$ac < bc$",
                "explicacion": r"Dado que multiplicamos la desigualdad $a > b$ por el número negativo $c$, el sentido de la desigualdad debe cambiar obligatoriamente a $ac < bc$."
            },
            {
                "stable_id": "DESPEJE-GEN-CONCEPT-3",
                "tipo": "conceptual",
                "nivel": 1,
                "enunciado": r"¿Qué sucede con el símbolo de desigualdad al restar un número positivo en ambos miembros de una inecuación?",
                "opciones": [
                    r"Se mantiene igual.",
                    r"Se invierte el sentido.",
                    r"Se transforma en una ecuación.",
                    r"Depende de la magnitud del número restado."
                ],
                "respuesta_correcta": r"Se mantiene igual.",
                "explicacion": r"La propiedad aditiva de las desigualdades establece que se puede sumar o restar el mismo número a ambos lados sin alterar el sentido de la desigualdad."
            },
            {
                "stable_id": "DESPEJE-GEN-RECON-1",
                "tipo": "reconocimiento",
                "nivel": 1,
                "enunciado": r"Se muestra un paso de la resolución de una inecuación. Paso 1: $-3x \ge 12$. Paso 2: $x \le -4$. ¿Es válido el razonamiento aplicado de pasar del Paso 1 al Paso 2?",
                "opciones": [
                    r"Sí, porque se dividió por $-3$ y se invirtió correctamente el signo de la desigualdad.",
                    r"No, porque al ser $12$ positivo, la desigualdad no debió invertirse.",
                    r"No, porque se debió mantener el signo mayor o igual en la respuesta final.",
                    r"Sí, porque al pasar el número $-3$ restando se cambia el signo."
                ],
                "respuesta_correcta": r"Sí, porque se dividió por $-3$ y se invirtió correctamente el signo de la desigualdad.",
                "explicacion": r"Al dividir ambos miembros por el coeficiente negativo ($-3$), el sentido de la desigualdad $\ge$ debe invertirse a $\le$."
            },
            {
                "stable_id": "DESPEJE-GEN-PROC-1",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": r"La inecuación $5x + 3 < 18$ tiene como solución $x < 3$.",
                "respuesta_correcta": True,
                "explicacion": r"Restando 3 a ambos lados: $5x < 15$. Dividiendo entre 5, obtenemos $x < 3$."
            },
            {
                "stable_id": "DESPEJE-GEN-PROC-2",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": r"La inecuación $-2x < 10$ se resuelve correctamente como $x < -5$.",
                "respuesta_correcta": False,
                "explicacion": r"Al dividir por $-2$, hay que invertir el signo de la desigualdad. Por tanto, la respuesta correcta es $x > -5$, no $x < -5$."
            },
            {
                "stable_id": "DESPEJE-GEN-PROC-3",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "enunciado": r"Para resolver $4x - 7 \ge 6x + 5$, si agrupamos las $x$ en la derecha, obtenemos una inecuación equivalente a $-12 \ge 2x$.",
                "respuesta_correcta": True,
                "explicacion": r"Restamos $4x$ de ambos lados: $-7 \ge 2x + 5$. Luego restamos 5 de ambos lados: $-12 \ge 2x$. La proposición es verdadera."
            },
            {
                "stable_id": "DESPEJE-GEN-PAES-1",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": r"¿Cuál es el conjunto solución de la inecuación $\frac{x}{3} - 1 > \frac{x}{2} + \frac{1}{6}$?",
                "opciones": [
                    r"$(-\infty, -7)$",
                    r"$(-7, \infty)$",
                    r"$(-\infty, -1)$",
                    r"$(-1, \infty)$",
                    r"$(-\infty, 1)$"
                ],
                "respuesta_correcta": r"$(-\infty, -7)$",
                "explicacion": r"Multiplicando todos los términos por 6 (el MCM): $2x - 6 > 3x + 1$. Restando $2x$ y $1$ a ambos lados: $-7 > x$, lo que equivale a $x < -7$."
            },
            {
                "stable_id": "DESPEJE-GEN-PAES-2",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": r"Dado el sistema de inecuaciones $2x - 5 < 3$ y $-3x \le 6$, ¿cuál es su conjunto solución?",
                "opciones": [
                    r"$[-2, 4)$",
                    r"$(-\infty, 4)$",
                    r"$[-2, \infty)$",
                    r"$(-2, 4]$",
                    r"No tiene solución."
                ],
                "respuesta_correcta": r"$[-2, 4)$",
                "explicacion": r"La primera inecuación $2x - 5 < 3$ se resuelve obteniendo $x < 4$. La segunda $-3x \le 6$ se resuelve dividiendo por $-3$ e invirtiendo el signo, dando $x \ge -2$. La intersección de ambas soluciones es el intervalo $[-2, 4)$."
            },
            {
                "stable_id": "DESPEJE-GEN-PAES-3",
                "tipo": "tipo_paes",
                "nivel": 3,
                "paes_style": True,
                "enunciado": r"Si $a$ y $b$ son constantes reales tales que $a < 0$ y $b > 0$, ¿cuál es la solución de la inecuación $ax + b < 0$?",
                "opciones": [
                    r"$x > -\frac{b}{a}$",
                    r"$x < -\frac{b}{a}$",
                    r"$x > \frac{b}{a}$",
                    r"$x < \frac{b}{a}$",
                    r"Falta información para determinarlo."
                ],
                "respuesta_correcta": r"$x > -\frac{b}{a}$",
                "explicacion": r"Restando $b$ de ambos lados, se tiene $ax < -b$. Como $a < 0$, al dividir ambos lados entre $a$ debemos invertir el sentido de la desigualdad, obteniendo $x > \frac{-b}{a}$ o $x > -\frac{b}{a}$."
            }
        ]
    }
}

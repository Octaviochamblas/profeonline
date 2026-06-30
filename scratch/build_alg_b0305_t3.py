import json
import os

def generate_exercises():
    YAMLS = {
        "mat-alg-suma-diferencia-identificacion-conjugados.yaml": """semantic_id: "MAT.ALG.SUMA_DIFERENCIA.IDENTIFICACION_CONJUGADOS"
titulo: "Identificación de binomios conjugados"
objetivo: "Reconocer cuándo dos binomios son conjugados (suma por diferencia) para poder aplicar la regla de la diferencia de cuadrados."
introduccion: "Antes de aplicar la magia rápida de la diferencia de cuadrados, debemos asegurarnos de que los binomios sean los adecuados. ¡No todo par de paréntesis califica!"
resumen: |
  Dos binomios son **conjugados** si tienen exactamente los mismos términos, pero difieren únicamente en el signo que los separa.
  Estructura general: $(a+b)(a-b)$ o $(a-b)(a+b)$.
explicacion: |
  Para identificar si puedes aplicar la regla de suma por diferencia, verifica tres cosas:
  1. Que ambos paréntesis contengan dos términos.
  2. Que haya un término idéntico en ambos (mismo signo y valor). En $(x+y)(x-y)$, el término $x$ es idéntico.
  3. Que haya un término que sea exactamente el opuesto aditivo en el otro (mismo valor, signo distinto). En $(x+y)(x-y)$, los términos son $+y$ y $-y$.
  
  Ejemplo válido: $(3m - 2n)(3m + 2n)$
  Ejemplo NO válido: $(3m - 2n)(2m + 3n)$ (los términos son distintos).
procedimiento: |
  Al enfrentarte a un producto de binomios:
  1. Revisa el primer término del primer binomio. ¿Aparece exactamente igual en el segundo binomio?
  2. Revisa el segundo término del primer binomio. ¿Aparece su inverso aditivo (con el signo cambiado) en el segundo binomio?
  3. Si la respuesta es sí a ambas, estás frente a una suma por su diferencia.
  4. Nota: el orden no importa por conmutatividad. $(x-4)(x+4)$ es lo mismo que $(x+4)(x-4)$ o $(4+x)(x-4)$.
ejemplos:
  - titulo: "Conjugados desordenados"
    enunciado: "¿Es $(2a + 5)(5 - 2a)$ un producto de suma por diferencia?"
    solucion_pasos:
      - "Identificamos términos: En el primero están $2a$ y $5$."
      - "En el segundo están $-2a$ y $5$."
      - "El término idéntico es $5$. El término opuesto es $2a$ y $-2a$."
      - "Sí lo es. Puede reescribirse como $(5 + 2a)(5 - 2a)$."
errores_frecuentes:
  - "Creer que $(x-y)(y-x)$ es suma por diferencia. ¡No lo es! El término $x$ y el término $y$ cambian de signo en ambos."
""",
        "mat-alg-suma-diferencia-regla-diferencia-cuadrados.yaml": """semantic_id: "MAT.ALG.SUMA_DIFERENCIA.REGLA_DIFERENCIA_CUADRADOS"
titulo: "Aplicación de la regla de diferencia de cuadrados"
objetivo: "Aplicar la regla rápida del producto de una suma por su diferencia para calcular expresiones algebraicas."
introduccion: "¡Este es probablemente el producto notable favorito de todos! Rápido, simple y sin términos centrales molestos."
resumen: |
  La regla de la suma por diferencia es:
  **"El cuadrado del término idéntico, menos el cuadrado del término que cambia de signo."**
  Fórmula: $(a+b)(a-b) = a^2 - b^2$
explicacion: |
  Al desarrollar $(a+b)(a-b)$ término a término, obtenemos $a^2 - ab + ba - b^2$.
  Los términos centrales $-ab$ y $+ba$ se anulan entre sí (su suma es cero). Por eso, el resultado siempre será un binomio, específicamente una diferencia de dos cuadrados.
procedimiento: |
  Pasos para aplicar la regla:
  1. Identifica que es una suma por diferencia.
  2. Ubica el término que NO cambia de signo (el término estable). Ése será tu $A$.
  3. Ubica el término que SÍ cambia de signo (el término opuesto). Ése será tu $B$.
  4. El resultado es $A^2 - B^2$. (¡Siempre es menos!).
ejemplos:
  - titulo: "Aplicación directa"
    enunciado: "Calcula $(y - 8)(y + 8)$."
    solucion_pasos:
      - "Término estable: $y$. Su cuadrado es $y^2$."
      - "Término que cambia: $8$. Su cuadrado es $64$."
      - "Resultado: $y^2 - 64$."
  - titulo: "Variables en ambos términos"
    enunciado: "Desarrolla $(5x + 3y^2)(5x - 3y^2)$."
    solucion_pasos:
      - "Cuadrado del primero: $(5x)^2 = 25x^2$."
      - "Cuadrado del segundo: $(3y^2)^2 = 9y^4$."
      - "Resultado: $25x^2 - 9y^4$."
errores_frecuentes:
  - "Poner un signo más en el resultado final: $(x-2)(x+2) = x^2 + 4$."
""",
        "mat-alg-suma-diferencia-representacion-area.yaml": """semantic_id: "MAT.ALG.SUMA_DIFERENCIA.REPRESENTACION_AREA"
titulo: "Representación geométrica de suma por diferencia"
objetivo: "Interpretar geométricamente el producto $(a+b)(a-b)$ mediante el cálculo de áreas."
introduccion: "¿Cómo se ve $a^2 - b^2$ geométricamente? Imagina un cuadrado grande al que le muerdes una esquina."
resumen: |
  Geométricamente, $a^2 - b^2$ representa el área de un cuadrado de lado $a$, al cual se le ha recortado un cuadrado menor de lado $b$ en una de sus esquinas.
  Esa figura resultante, en forma de "L", puede reordenarse cortándola y pegándola para formar un rectángulo perfecto de lados $(a+b)$ y $(a-b)$.
explicacion: |
  1. Partimos con un cuadrado grande de área $a^2$.
  2. Le quitamos un cuadrado en la esquina de área $b^2$. El área restante es $a^2 - b^2$.
  3. La figura que queda está formada por dos rectángulos: uno de $(a-b) \\times a$ y otro de $b \\times (a-b)$.
  4. Si tomamos el rectángulo más pequeño y lo rotamos para pegarlo al lado del más grande, encajan perfectamente formando un solo rectángulo grande.
  5. Este nuevo rectángulo tiene como base $(a+b)$ y como altura $(a-b)$. Su área es $(a+b)(a-b)$.
  6. Por lo tanto, $(a+b)(a-b) = a^2 - b^2$.
procedimiento: |
  Si te piden justificar geométricamente:
  1. Dibuja el cuadrado mayor $a^2$.
  2. Resta la esquina $b^2$.
  3. Muestra cómo las dos franjas restantes (de anchos $a-b$) se unen.
ejemplos:
  - titulo: "Cálculo visual numérico"
    enunciado: "Un terreno cuadrado de lado $10$ m pierde un área cuadrada de lado $3$ m. ¿Qué dimensiones tendrá el rectángulo equivalente construido con el resto del terreno?"
    solucion_pasos:
      - "Lado inicial $a = 10$, lado recortado $b = 3$."
      - "El rectángulo equivalente tendrá dimensiones $(10+3)$ y $(10-3)$."
      - "Es decir, $13$ m por $7$ m."
      - "Verificamos: $13 \\times 7 = 91$. Y $100 - 9 = 91$."
errores_frecuentes:
  - "No entender que la figura en forma de 'L' (gnomon) y el rectángulo largo tienen exactamente la misma área, solo están reordenados."
""",
        "mat-alg-suma-diferencia-error-signo.yaml": """semantic_id: "MAT.ALG.SUMA_DIFERENCIA.ERROR_SIGNO"
titulo: "Detección de error de signo en suma por diferencia"
objetivo: "Identificar y corregir el error común de sumar los cuadrados en lugar de restarlos."
introduccion: "¡No dejes que los signos te engañen! El resultado de una suma por su diferencia NUNCA es una suma de cuadrados."
resumen: |
  Un error clásico es resolver $(a+b)(a-b) = a^2 + b^2$.
  La realidad es que $(a+b)(a-b)$ SIEMPRE resulta en una diferencia: $a^2 - b^2$.
  La suma de cuadrados $a^2 + b^2$ NO es factorizable en los números reales mediante binomios simples (requiere números complejos).
explicacion: |
  ¿Por qué ocurre este error? Muchas veces es por hacer el proceso automático sin pensar en la regla de los signos, o por confundir $(a+b)(a-b)$ con algo parecido al cuadrado de binomio.
  Recuerda: al multiplicar el término $+b$ por el término $-b$, el producto de signos distintos da negativo ($-b^2$).
procedimiento: |
  Al auditar un resultado de suma por diferencia:
  1. Verifica que haya dos términos, ambos elevados al cuadrado.
  2. Revisa el signo entre ellos. DEBE ser un signo menos ($-$).
  3. Si hay un signo más, el desarrollo está incorrecto.
ejemplos:
  - titulo: "Auditoría simple"
    enunciado: "En un examen, un estudiante escribe $(x-7)(x+7) = x^2 + 49$. ¿Por qué está malo?"
    solucion_pasos:
      - "Porque al hacer la multiplicación final de los segundos términos: $(-7) \\cdot (+7) = -49$."
      - "El estudiante omitió la regla de signos. Lo correcto es $x^2 - 49$."
errores_frecuentes:
  - "Creer que la diferencia de cuadrados puede dar positivo si se reordena la expresión."
""",
        "mat-alg-termino-comun-identificacion-estructura.yaml": """semantic_id: "MAT.ALG.TERMINO_COMUN.IDENTIFICACION_ESTRUCTURA"
titulo: "Identificación de binomios con término común"
objetivo: "Reconocer la estructura de dos binomios que comparten exactamente un término para aplicar su regla particular."
introduccion: "¿Qué pasa si los binomios se parecen, pero no son idénticos ni conjugados? Si comparten al menos una cosa, ¡estás de suerte!"
resumen: |
  Dos binomios tienen un **término común** cuando exactamente uno de sus términos es idéntico en ambos (mismo coeficiente, misma letra, mismo exponente, mismo signo).
  Estructura general: $(x+a)(x+b)$, donde $x$ es el término común, y $a, b$ son los términos no comunes (diferentes).
explicacion: |
  Ejemplos de la estructura:
  - $(y + 5)(y - 8)$: El término común es $y$.
  - $(2m^2 - 1)(2m^2 + 7)$: El término común es $2m^2$.
  - $(x + 4)(y + 4)$: El término común es $4$ (aunque generalmente ordenamos para que el término común quede primero: $(4+x)(4+y)$).
procedimiento: |
  Para identificar este producto notable:
  1. Observa ambos binomios.
  2. Verifica si son idénticos (cuadrado de binomio). Si no, pasa al paso 3.
  3. Verifica si son suma por diferencia. Si no, pasa al paso 4.
  4. Busca un término que sea exactamente igual en ambos. Ese es tu "término común".
  5. Los otros dos términos son los "no comunes".
ejemplos:
  - titulo: "Clasificando productos"
    enunciado: "Determina si $(5p - 2)(5p + 3)$ corresponde a un producto con término común."
    solucion_pasos:
      - "El término $5p$ aparece exactamente igual en ambos paréntesis."
      - "Los otros términos son $-2$ y $+3$, que son distintos."
      - "Por lo tanto, SÍ es un producto de binomios con término común."
errores_frecuentes:
  - "Creer que $(2x+3)(3x+2)$ tiene término común. ¡No lo tiene! $2x$ es distinto de $3x$, y $3$ es distinto de $2$."
""",
        "mat-alg-termino-comun-regla-general.yaml": """semantic_id: "MAT.ALG.TERMINO_COMUN.REGLA_GENERAL"
titulo: "Aplicación de la regla de binomios con término común"
objetivo: "Aplicar la fórmula rápida para multiplicar binomios que comparten un término."
introduccion: "Multiplicar $(x+5)(x+3)$ paso a paso toma $4$ cálculos. Con la regla del término común, ¡lo harás mentalmente en $3$ pasos rápidos!"
resumen: |
  La regla para $(x+a)(x+b)$ es:
  **"El cuadrado del término común, MÁS la suma algebraica de los no comunes por el término común, MÁS el producto de los no comunes."**
  Fórmula: $(x+a)(x+b) = x^2 + (a+b)x + (ab)$
explicacion: |
  Al desarrollar $(x+a)(x+b)$ obtenemos $x^2 + xb + ax + ab$.
  Podemos factorizar el término común $x$ de los dos del medio: $x^2 + (a+b)x + ab$.
  Esta es la justificación matemática de la regla: los términos no comunes se **suman** para formar el coeficiente del término central, y se **multiplican** para formar el término independiente.
procedimiento: |
  Al calcular $(x+a)(x+b)$:
  1. Eleva el término común al cuadrado.
  2. Suma algebraicamente los términos no comunes (ej. si son $+5$ y $-3$, la suma es $2$).
  3. Multiplica esa suma por el término común.
  4. Multiplica los términos no comunes entre sí.
  5. Escribe el trinomio resultante.
ejemplos:
  - titulo: "Aplicación rápida"
    enunciado: "Desarrolla $(m + 6)(m + 4)$."
    solucion_pasos:
      - "Término común: $m$. Al cuadrado: $m^2$."
      - "No comunes: $6$ y $4$. Suma: $6+4=10$. Multiplicado por el común: $10m$."
      - "Producto de no comunes: $6 \\cdot 4 = 24$."
      - "Resultado: $m^2 + 10m + 24$."
  - titulo: "Con signos negativos"
    enunciado: "Desarrolla $(y - 7)(y - 2)$."
    solucion_pasos:
      - "Término común: $y$. Al cuadrado: $y^2$."
      - "Suma: $-7 + -2 = -9$. Por el común: $-9y$."
      - "Producto: $(-7) \\cdot (-2) = +14$."
      - "Resultado: $y^2 - 9y + 14$."
errores_frecuentes:
  - "Multiplicar los no comunes para el término central en lugar de sumarlos (ej. poner $24m$ en lugar de $10m$ en el primer ejemplo)."
""",
        "mat-alg-termino-comun-manejo-signos-no-comunes.yaml": """semantic_id: "MAT.ALG.TERMINO_COMUN.MANEJO_SIGNOS_NO_COMUNES"
titulo: "Manejo de signos en los términos no comunes"
objetivo: "Realizar correctamente las operaciones algebraicas de suma y multiplicación cuando los términos no comunes tienen distintos signos."
introduccion: "Cuando un término no común es positivo y el otro negativo, el cerebro a veces se enreda entre 'sumar' y 'multiplicar'. ¡Vamos a ordenarlo!"
resumen: |
  En el producto $(x+a)(x-b)$:
  - La **suma algebraica** de los no comunes define el coeficiente lineal: $(a - b)$. Dependiendo de cuál sea mayor en valor absoluto, el término central será positivo o negativo.
  - El **producto** de los no comunes será SIEMPRE negativo: $a \\cdot (-b) = -ab$.
explicacion: |
  Si tienes $(x - 5)(x + 2)$:
  - Para el término central, debemos hacer una **suma**: $-5 + 2 = -3$.
  - Para el último término, debemos hacer una **multiplicación**: $-5 \\cdot 2 = -10$.
  - Resultado: $x^2 - 3x - 10$.
  Debes separar mentalmente la regla de adición (quien "gana" impone su signo) de la regla de multiplicación (más por menos es menos).
procedimiento: |
  Si los signos son distintos:
  1. Para el medio: Resta los valores absolutos. Ponle el signo del número mayor.
  2. Para el final: Multiplica los valores y pon siempre signo negativo.
ejemplos:
  - titulo: "Signos opuestos, mayor positivo"
    enunciado: "Calcula $(x + 9)(x - 4)$."
    solucion_pasos:
      - "Suma de no comunes: $9 + (-4) = +5$."
      - "Producto de no comunes: $9 \\cdot (-4) = -36$."
      - "Resultado: $x^2 + 5x - 36$."
errores_frecuentes:
  - "Aplicar la regla de los signos de la multiplicación a la suma, asumiendo que el término central siempre será negativo si los signos difieren."
""",
        "mat-alg-termino-comun-caso-general-lineal.yaml": """semantic_id: "MAT.ALG.TERMINO_COMUN.CASO_GENERAL_LINEAL"
titulo: "Producto de binomios lineales no mónicos"
objetivo: "Aplicar la generalización del producto con término común cuando los binomios son del tipo $(ax+b)(cx+d)$."
introduccion: "¿Y si los coeficientes de $x$ no son $1$? ¿Y si ni siquiera son iguales? ¡Aún hay una forma sistemática de resolverlo!"
resumen: |
  El producto de dos binomios lineales generales $(ax+b)(cx+d)$ no es estrictamente un 'producto notable' tradicional, pero tiene un patrón fijo:
  **$(ax+b)(cx+d) = (ac)x^2 + (ad+bc)x + bd$**
  Esto es la aplicación formal del método FOIL (Firsts, Outers, Inners, Lasts).
explicacion: |
  1. $F$ (Primeros): $(ax)(cx) = acx^2$
  2. $O$ (Externos): $(ax)(d) = adx$
  3. $I$ (Internos): $(b)(cx) = bcx$
  4. $L$ (Últimos): $(b)(d) = bd$
  Agrupando el término de al medio (los cruzados): $(ad + bc)x$.
procedimiento: |
  Para calcular $(ax+b)(cx+d)$ mentalmente:
  1. Multiplica los primeros coeficientes para el $x^2$.
  2. Calcula 'los extremos por los medios' (producto cruzado) y súmalos: $(ax \\cdot d) + (b \\cdot cx)$.
  3. Multiplica los últimos términos (los independientes) para el final.
ejemplos:
  - titulo: "Usando patrón general"
    enunciado: "Desarrolla $(2x + 3)(4x - 1)$."
    solucion_pasos:
      - "Término en $x^2$: $2 \\cdot 4 = 8x^2$."
      - "Productos cruzados: $(2)(-1) = -2$; $(3)(4) = 12$. Suma: $10$. Así que $+10x$."
      - "Últimos: $(3)(-1) = -3$."
      - "Resultado: $8x^2 + 10x - 3$."
errores_frecuentes:
  - "Multiplicar solo los primeros y los últimos, obteniendo $(ax)(cx) + (b)(d)$, omitiendo completamente los términos cruzados."
"""
    }

    exercises = []
    
    # 1. MAT.ALG.SUMA_DIFERENCIA.IDENTIFICACION_CONJUGADOS
    sid = "MAT.ALG.SUMA_DIFERENCIA.IDENTIFICACION_CONJUGADOS"
    exercises.append({"stable_id": "SD-IC-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Para que dos binomios sean considerados 'conjugados' (o suma por su diferencia), es necesario y suficiente que:", "choices": ["A) Tengan los mismos términos, pero un signo central distinto (o uno de los términos con signo opuesto).", "B) Tengan variables distintas.", "C) Ambos sean sumas de números positivos.", "D) Tengan un solo término común."], "correct_answer": "A) Tengan los mismos términos, pero un signo central distinto (o uno de los términos con signo opuesto).", "solution_steps": "La definición de conjugado es $(A+B)$ y $(A-B)$, donde difieren solo en el signo de un término.", "paes_style": False})
    exercises.append({"stable_id": "SD-IC-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Cuál de las siguientes parejas de binomios corresponde a una suma por diferencia?", "choices": ["A) $(5x - 3)(5x + 3)$", "B) $(5x - 3)(5x - 3)$", "C) $(5x + 3)(3x - 5)$", "D) $(-5x + 3)(-5x + 3)$"], "correct_answer": "A) $(5x - 3)(5x + 3)$", "solution_steps": "El término estable es $5x$. El término que cambia es el $3$ y $-3$.", "paes_style": False})
    exercises.append({"stable_id": "SD-IC-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Identifica si la expresión $(-x - 7)(x - 7)$ es una suma por su diferencia, y si lo es, ¿cuál es el término estable?", "choices": ["A) Sí es, el término estable es $-7$.", "B) Sí es, el término estable es $x$.", "C) No es suma por diferencia, es un cuadrado de binomio.", "D) No es, no tienen términos en común."], "correct_answer": "A) Sí es, el término estable es $-7$.", "solution_steps": "Podemos reescribirlo como $(-7 - x)(-7 + x)$. El estable es $-7$. El que cambia es $x$.", "paes_style": False})
    exercises.append({"stable_id": "SD-IC-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Para que $(ax + b)(cx - d)$ sea resoluble usando la fórmula de suma por diferencia, asumiendo $a,b,c,d > 0$, ¿qué condición necesaria deben cumplir las constantes?", "choices": ["A) $a = c$ y $b = d$.", "B) $a = d$ y $b = c$.", "C) $ac = bd$.", "D) $a+c = 0$."], "correct_answer": "A) $a = c$ y $b = d$.", "solution_steps": "Deben ser los mismos términos exactos: el estable $ax$ debe igualar a $cx$ ($a=c$), y el opuesto $b$ debe igualar a $d$ ($b=d$).", "paes_style": True})

    # 2. MAT.ALG.SUMA_DIFERENCIA.REGLA_DIFERENCIA_CUADRADOS
    sid = "MAT.ALG.SUMA_DIFERENCIA.REGLA_DIFERENCIA_CUADRADOS"
    exercises.append({"stable_id": "SD-RDC-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Por qué el desarrollo de $(x+y)(x-y)$ no tiene un término central en $xy$?", "choices": ["A) Porque al sumar $-xy$ (los extremos) y $+yx$ (los internos), el resultado es $0$.", "B) Porque la multiplicación de un positivo y un negativo siempre anula la variable.", "C) Porque es una regla preestablecida sin demostración algebraica.", "D) Porque los términos centrales se dividen por $1$."], "correct_answer": "A) Porque al sumar $-xy$ (los extremos) y $+yx$ (los internos), el resultado es $0$.", "solution_steps": "Los productos cruzados son opuestos aditivos y se cancelan.", "paes_style": False})
    exercises.append({"stable_id": "SD-RDC-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "¿Cuál es el resultado de la expansión de $(2m - 5n)(2m + 5n)$?", "choices": ["A) $4m^2 - 25n^2$", "B) $4m^2 + 25n^2$", "C) $4m^2 - 10mn - 25n^2$", "D) $2m^2 - 5n^2$"], "correct_answer": "A) $4m^2 - 25n^2$", "solution_steps": "$(2m)^2 - (5n)^2 = 4m^2 - 25n^2$.", "paes_style": False})
    exercises.append({"stable_id": "SD-RDC-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Desarrolla $(\frac{1}{2}x + 3)(\frac{1}{2}x - 3)$.", "choices": ["A) $\frac{1}{4}x^2 - 9$", "B) $\frac{1}{2}x^2 - 9$", "C) $\frac{1}{4}x^2 + 9$", "D) $\frac{1}{4}x^2 - 3$"], "correct_answer": "A) $\frac{1}{4}x^2 - 9$", "solution_steps": "$(\frac{1}{2}x)^2 - (3)^2 = \frac{1}{4}x^2 - 9$.", "paes_style": False})
    exercises.append({"stable_id": "SD-RDC-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M2", "prompt": "Calcula mentalmente $102 \\cdot 98$ usando productos notables.", "choices": ["A) $9996$", "B) $10004$", "C) $9904$", "D) $9896$"], "correct_answer": "A) $9996$", "solution_steps": "$102 \\cdot 98 = (100+2)(100-2) = 100^2 - 2^2 = 10000 - 4 = 9996$.", "paes_style": True})

    # 3. MAT.ALG.SUMA_DIFERENCIA.REPRESENTACION_AREA
    sid = "MAT.ALG.SUMA_DIFERENCIA.REPRESENTACION_AREA"
    exercises.append({"stable_id": "SD-RA-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "En la representación geométrica de $a^2 - b^2$, la figura que queda tras restar el cuadrado $b^2$ tiene forma de 'L'. ¿Cómo se forma el rectángulo de $(a+b)(a-b)$ a partir de esta 'L'?", "choices": ["A) Se corta un rectángulo de base $b$ y altura $a-b$, y se traslada al otro extremo.", "B) Se le suma un cuadrado de $b^2$.", "C) Se divide a la mitad.", "D) Es imposible formar un rectángulo perfecto con una L."], "correct_answer": "A) Se corta un rectángulo de base $b$ y altura $a-b$, y se traslada al otro extremo.", "solution_steps": "Al trasladar esa pieza, se completa el rectángulo de base $a+b$ y altura $a-b$.", "paes_style": False})
    exercises.append({"stable_id": "SD-RA-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Un patio cuadrado de lado $x$ reduce su ancho en $2$ m y aumenta su largo en $2$ m. ¿Cuál es el área del nuevo patio y cómo se compara con el original?", "choices": ["A) $x^2 - 4$, es $4$ m$^2$ menor que el original.", "B) $x^2 + 4$, es $4$ m$^2$ mayor.", "C) $x^2$, es igual al original.", "D) $x^2 - 2$, es $2$ m$^2$ menor."], "correct_answer": "A) $x^2 - 4$, es $4$ m$^2$ menor que el original.", "solution_steps": "Nuevo patio: $(x-2)(x+2) = x^2 - 4$. Original: $x^2$. Diferencia es que perdió $4$.", "paes_style": False})
    exercises.append({"stable_id": "SD-RA-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Un arquitecto tiene una lámina de cartón cuadrada de lado $L$. Debe cortar un cuadrado en una esquina de lado $x$. Para calcular el área restante, decide medir los lados del cartón restante y multiplicarlos usando $(L-x)(L+x)$. ¿Es correcto este procedimiento geométricamente?", "choices": ["A) Sí, el área restante $L^2 - x^2$ puede ser reordenada como un rectángulo de lados $L-x$ y $L+x$.", "B) No, el área es solo $L^2 - x^2$, no se puede factorizar.", "C) Sí, porque $(L-x)(L+x)$ es el área de un círculo.", "D) No, el área sería $(L-x)^2$."], "correct_answer": "A) Sí, el área restante $L^2 - x^2$ puede ser reordenada como un rectángulo de lados $L-x$ y $L+x$.", "solution_steps": "Esa es justamente la justificación geométrica de la diferencia de cuadrados.", "paes_style": True})

    # 4. MAT.ALG.SUMA_DIFERENCIA.ERROR_SIGNO
    sid = "MAT.ALG.SUMA_DIFERENCIA.ERROR_SIGNO"
    exercises.append({"stable_id": "SD-ES-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Cuál de las siguientes afirmaciones explica por qué $(x+5)(x-5) = x^2 + 25$ es un resultado INCORRECTO?", "choices": ["A) Al multiplicar el $+5$ por el $-5$, el resultado debe ser obligatoriamente negativo ($-25$).", "B) Falta el término central $10x$.", "C) Falta el doble producto.", "D) La $x$ debería estar elevada a $4$."], "correct_answer": "A) Al multiplicar el $+5$ por el $-5$, el resultado debe ser obligatoriamente negativo ($-25$).", "solution_steps": "Más por menos da menos. El resultado correcto es $x^2 - 25$.", "paes_style": False})
    exercises.append({"stable_id": "SD-ES-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Señala cuál de estos polinomios NO puede factorizarse usando suma por diferencia en los números reales.", "choices": ["A) $x^2 + 16$", "B) $x^2 - 16$", "C) $25 - y^2$", "D) $m^4 - n^2$"], "correct_answer": "A) $x^2 + 16$", "solution_steps": "Es una suma de cuadrados, no una diferencia. No hay forma de que un producto de conjugados reales dé $+16$.", "paes_style": False})
    exercises.append({"stable_id": "SD-ES-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Si un alumno afirma que $a^2 + b^2 = (a-b)(a+b)$, y lo usa para resolver un sistema, ¿en qué caso particular su razonamiento defectuoso le arrojará una respuesta correcta a pesar del error?", "choices": ["A) Solo cuando $b = 0$.", "B) Cuando $a = b$.", "C) Nunca, siempre será un error catastrófico.", "D) Cuando $a$ es positivo y $b$ es negativo."], "correct_answer": "A) Solo cuando $b = 0$.", "solution_steps": "Si igualamos $a^2 + b^2 = a^2 - b^2$, obtenemos $2b^2 = 0 \\Rightarrow b = 0$. Solo en ese caso extremo el error no afecta.", "paes_style": True})

    # 5. MAT.ALG.TERMINO_COMUN.IDENTIFICACION_ESTRUCTURA
    sid = "MAT.ALG.TERMINO_COMUN.IDENTIFICACION_ESTRUCTURA"
    exercises.append({"stable_id": "TC-IE-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Qué característica define a dos binomios con 'término común'?", "choices": ["A) Tienen exactamente un término que es idéntico en ambos paréntesis.", "B) Tienen los mismos términos con distinto signo.", "C) Ningún término coincide.", "D) Comparten todos los términos."], "correct_answer": "A) Tienen exactamente un término que es idéntico en ambos paréntesis.", "solution_steps": "Esa es la definición de la estructura $(x+a)(x+b)$.", "paes_style": False})
    exercises.append({"stable_id": "TC-IE-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Indica cuál de las siguientes multiplicaciones representa un producto de binomios con un término común.", "choices": ["A) $(3y - 5)(3y + 8)$", "B) $(3y - 5)(2y + 5)$", "C) $(3y - 5)(3y - 5)$", "D) $(3y - 5)(3y + 5)$"], "correct_answer": "A) $(3y - 5)(3y + 8)$", "solution_steps": "El $3y$ es el término idéntico. $-5$ y $+8$ son los no comunes.", "paes_style": False})
    exercises.append({"stable_id": "TC-IE-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "¿Es la expresión $(x - y)(x + y)$ un caso especial de binomios con término común?", "choices": ["A) Sí, donde el término común es $x$, y los no comunes son $-y$ e $y$.", "B) No, porque no cumple la estructura general.", "C) No, porque los signos son diferentes.", "D) Sí, pero el término común es $y$."], "correct_answer": "A) Sí, donde el término común es $x$, y los no comunes son $-y$ e $y$.", "solution_steps": "Si aplicamos la regla de término común: $x^2 + (-y+y)x + (-y)(y) = x^2 + 0x - y^2 = x^2 - y^2$. Sí es un caso especial.", "paes_style": True})

    # 6. MAT.ALG.TERMINO_COMUN.REGLA_GENERAL
    sid = "MAT.ALG.TERMINO_COMUN.REGLA_GENERAL"
    exercises.append({"stable_id": "TC-RG-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Desarrolla $(m + 4)(m + 9)$ usando la regla.", "choices": ["A) $m^2 + 13m + 36$", "B) $m^2 + 36m + 13$", "C) $m^2 + 13m + 13$", "D) $m^2 + 36$"], "correct_answer": "A) $m^2 + 13m + 36$", "solution_steps": "Suma: $4+9=13$. Producto: $4 \\cdot 9=36$. Trinomio: $m^2 + 13m + 36$.", "paes_style": False})
    exercises.append({"stable_id": "TC-RG-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Calcula el término central de la expansión de $(2x^2 + 3)(2x^2 + 8)$.", "choices": ["A) $22x^2$", "B) $11x^2$", "C) $24x^2$", "D) $11x^4$"], "correct_answer": "A) $22x^2$", "solution_steps": "La suma de los no comunes es $3+8 = 11$. Se multiplica por el común $2x^2$: $11 \\cdot 2x^2 = 22x^2$.", "paes_style": False})
    exercises.append({"stable_id": "TC-RG-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Se sabe que el producto de $(x+A)(x+B)$ es $x^2 + 10x + 21$. ¿Cuáles son los valores positivos de $A$ y $B$ (sin importar el orden)?", "choices": ["A) $3$ y $7$", "B) $1$ y $21$", "C) $2$ y $5$", "D) $10$ y $21$"], "correct_answer": "A) $3$ y $7$", "solution_steps": "Buscamos dos números que sumen $10$ y multipliquen $21$. $3+7=10$, $3 \\cdot 7 = 21$.", "paes_style": True})

    # 7. MAT.ALG.TERMINO_COMUN.MANEJO_SIGNOS_NO_COMUNES
    sid = "MAT.ALG.TERMINO_COMUN.MANEJO_SIGNOS_NO_COMUNES"
    exercises.append({"stable_id": "TC-MS-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Desarrolla $(y - 6)(y + 2)$.", "choices": ["A) $y^2 - 4y - 12$", "B) $y^2 - 4y + 12$", "C) $y^2 + 4y - 12$", "D) $y^2 - 8y - 12$"], "correct_answer": "A) $y^2 - 4y - 12$", "solution_steps": "Suma: $-6 + 2 = -4$. Producto: $-6 \\cdot 2 = -12$. Resulta: $y^2 - 4y - 12$.", "paes_style": False})
    exercises.append({"stable_id": "TC-MS-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Expande $(z + 5)(z - 9)$.", "choices": ["A) $z^2 - 4z - 45$", "B) $z^2 + 4z - 45$", "C) $z^2 - 14z - 45$", "D) $z^2 - 4z + 45$"], "correct_answer": "A) $z^2 - 4z - 45$", "solution_steps": "Suma: $5 + -9 = -4$. Producto: $5 \\cdot -9 = -45$.", "paes_style": False})
    exercises.append({"stable_id": "TC-MS-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Encuentra el valor de $(p - 11)(p - 3)$.", "choices": ["A) $p^2 - 14p + 33$", "B) $p^2 - 14p - 33$", "C) $p^2 + 14p + 33$", "D) $p^2 + 8p - 33$"], "correct_answer": "A) $p^2 - 14p + 33$", "solution_steps": "Suma: $-11 + -3 = -14$. Producto: $(-11)(-3) = +33$.", "paes_style": True})

    # 8. MAT.ALG.TERMINO_COMUN.CASO_GENERAL_LINEAL
    sid = "MAT.ALG.TERMINO_COMUN.CASO_GENERAL_LINEAL"
    exercises.append({"stable_id": "TC-CGL-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Desarrolla multiplicando término a término (FOIL) el producto $(3x + 2)(4x + 1)$.", "choices": ["A) $12x^2 + 11x + 2$", "B) $12x^2 + 10x + 2$", "C) $12x^2 + 8x + 2$", "D) $7x^2 + 11x + 2$"], "correct_answer": "A) $12x^2 + 11x + 2$", "solution_steps": "F: $12x^2$. O: $3x$. I: $8x$. L: $2$. Suma de cruzados: $3x + 8x = 11x$. Total: $12x^2 + 11x + 2$.", "paes_style": False})
    exercises.append({"stable_id": "TC-CGL-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Si $(5x - 3)(2x + 7) = Ax^2 + Bx + C$, ¿cuál es el valor de $A + B + C$?", "choices": ["A) $8$", "B) $10$", "C) $39$", "D) $29$"], "correct_answer": "A) $8$", "solution_steps": "F: $10x^2 \\Rightarrow A=10$. Cruzados: $(5)(7) + (-3)(2) = 35 - 6 = 29 \\Rightarrow B=29$. L: $(-3)(7) = -21 \\Rightarrow C=-21$. $A+B+C = 10 + 29 - 21 = 39 - 21 = 18$. Espera. Evaluando en $x=1$, obtenemos $(5(1)-3)(2(1)+7) = (2)(9) = 18$. La respuesta A) 8 era incorrecta, debe ser 18. Espera, arreglaré las alternativas en el choice. ¡Ah! Voy a poner 18.", "paes_style": True})
    exercises[-1]["choices"] = ["A) $18$", "B) $10$", "C) $39$", "D) $29$"]
    exercises[-1]["correct_answer"] = "A) $18$"
    
    exercises.append({"stable_id": "TC-CGL-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "En el desarrollo de $(-2x + 5)(3x - 4)$, ¿cuál es el término de primer grado (coeficiente de $x$)?", "choices": ["A) $23x$", "B) $8x$", "C) $15x$", "D) $-7x$"], "correct_answer": "A) $23x$", "solution_steps": "Cruzados: $(-2x)(-4) = 8x$. Internos: $(5)(3x) = 15x$. Suma: $8x + 15x = 23x$.", "paes_style": True})

    # Write files
    for yaml_filename, yaml_content in YAMLS.items():
        with open(f"docs/conocimiento/contenido/{yaml_filename}", "w", encoding="utf-8") as f:
            f.write(yaml_content)
    print(f"Creados {len(YAMLS)} yamls T3...")
    
    jsonl_filename = "docs/conocimiento/ejercicios/mat-alg-productos-notables-banco-gen-3.jsonl"
    with open(jsonl_filename, "w", encoding="utf-8") as f:
        for ex in exercises:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"{jsonl_filename} con {len(exercises)} ejercicios T3")

if __name__ == "__main__":
    generate_exercises()

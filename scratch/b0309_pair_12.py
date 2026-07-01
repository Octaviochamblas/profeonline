import os

topics = {
    "MAT.ALG.INECUACIONES_LINEALES.EXPRESION_RECTA": {
        "yaml": r"""semantic_id: MAT.ALG.INECUACIONES_LINEALES.EXPRESION_RECTA
titulo: Expresión de inecuaciones lineales en la recta numérica
objetivo: representar gráficamente las soluciones de inecuaciones lineales en la recta numérica real
introduccion: La representación gráfica en la recta numérica permite visualizar el conjunto solución de una inecuación lineal, interpretando correctamente el uso de intervalos abiertos y cerrados.
resumen: Para expresar gráficamente una inecuación lineal, se ubica el punto límite en la recta y se traza un rayo hacia la dirección correspondiente. Si la desigualdad incluye el signo igual, el punto se dibuja relleno; si es estricta, el punto se dibuja vacío.
explicacion: |
  ### Definición formal
  Dada una inecuación en una variable $x$, su representación gráfica en la recta real es un intervalo que describe el conjunto solución. Sea $a \in \mathbb{R}$ un valor límite:
  - $x > a$: Semirrecta abierta a la derecha de $a$. En $a$ se utiliza un círculo sin rellenar.
  - $x \geq a$: Semirrecta cerrada a la derecha de $a$. En $a$ se utiliza un círculo relleno.
  - $x < a$: Semirrecta abierta a la izquierda de $a$. En $a$ se utiliza un círculo sin rellenar.
  - $x \leq a$: Semirrecta cerrada a la izquierda de $a$. En $a$ se utiliza un círculo relleno.

  ### Desarrollo didáctico
  Al resolver una inecuación, el resultado final es un conjunto infinito de valores. Para comprender mejor cuáles son estos valores, los dibujamos sobre una recta numérica.

  El primer paso es ubicar el número límite en la recta. Luego, observamos el símbolo de la desigualdad:
  - Si usamos mayor que ($>$) o mayor o igual que ($\geq$), trazamos una flecha que va desde el número hacia la derecha.
  - Si usamos menor que ($<$) o menor o igual que ($\leq$), trazamos una flecha que va desde el número hacia la izquierda.

  Finalmente, debemos indicar si el número límite forma parte de la solución o no mediante un pequeño círculo sobre el número:
  - Lo dibujamos vacío para $>$ y $<$, indicando que el límite no se incluye.
  - Lo dibujamos relleno para $\geq$ y $\leq$, indicando que el límite sí se incluye.
procedimiento:
  - "Resolver la inecuación lineal si aún no está despejada para obtener una forma comparativa como $x > a$ o $x \leq a$."
  - "Dibujar una recta numérica y marcar el número límite $a$."
  - "Determinar si el círculo sobre $a$ debe ir relleno para desigualdades no estrictas o vacío para desigualdades estrictas."
  - "Trazar una flecha desde $a$ hacia la derecha para valores mayores, o hacia la izquierda para valores menores."
ejemplos:
  - titulo: "Representación gráfica de x mayor o igual a 3"
    enunciado: "Representa en la recta numérica la inecuación $x \geq 3$."
    solucion_pasos:
      - "La desigualdad es $x \geq 3$."
      - "Trazamos la recta numérica y ubicamos el número $3$."
      - "Como el símbolo es $\geq$, incluimos el límite dibujando un círculo relleno en el $3$."
      - "Trazamos una flecha hacia la derecha indicando todos los valores mayores que $3$."
  - titulo: "Representación gráfica de x menor que -2"
    enunciado: "Grafica el conjunto solución de la inecuación $x < -2$ en la recta numérica."
    solucion_pasos:
      - "Tenemos la inecuación $x < -2$."
      - "Dibujamos la recta y marcamos el valor límite $-2$."
      - "Como el símbolo es $<$, el círculo sobre el $-2$ debe ir vacío."
      - "Dibujamos la flecha hacia la izquierda porque los valores son menores que $-2$."
  - titulo: "¿Círculo relleno o vacío?"
    respuesta: "Sí"
    solucion_pasos:
      - "La inecuación es $x \leq 5$."
      - "El símbolo $\leq$ indica menor o igual, por lo tanto, el $5$ es parte de la solución."
      - "Se representa con un círculo relleno en $x=5$ y una flecha a la izquierda. Efectivamente, la representación lleva círculo relleno."
  - titulo: "¿Dirección hacia la izquierda para mayores?"
    respuesta: "No"
    solucion_pasos:
      - "La inecuación es $x > 4$."
      - "El símbolo indica mayor que."
      - "Los valores mayores que un número están a la derecha de ese número en la recta numérica."
      - "Por lo tanto, la flecha debe apuntar hacia la derecha, no hacia la izquierda."
errores_frecuentes:
  - "Usar un círculo relleno cuando la desigualdad es estricta."
  - "Trazar la flecha hacia la izquierda cuando la variable es mayor al límite."
  - "Trazar la flecha hacia la derecha cuando la variable es menor al límite."
  - "Graficar el intervalo opuesto olvidando invertir el símbolo de desigualdad al dividir por un negativo previamente."
  - "Asumir que el círculo vacío incluye el número marcado en la solución."
fuente: "Creación propia"
estado: publicado""",
        "jsonl": r"""{"stable_id": "ALG-GEN-REC-1", "tipo": "conceptual", "nivel": 1, "enunciado": "¿Qué tipo de círculo se utiliza en la recta numérica para representar el símbolo $<$?", "opciones": [{"texto": "Un círculo vacío.", "correcta": true}, {"texto": "Un círculo relleno.", "correcta": false}, {"texto": "Un cuadrado relleno.", "correcta": false}, {"texto": "Una flecha hacia arriba.", "correcta": false}], "explicacion": "El símbolo $<$ indica una desigualdad estricta, lo que significa que el límite no está incluido, representándose mediante un círculo vacío."}
{"stable_id": "ALG-GEN-REC-2", "tipo": "conceptual", "nivel": 1, "enunciado": "Si una inecuación tiene como solución $x \\geq -5$, ¿hacia dónde apunta la representación en la recta numérica?", "opciones": [{"texto": "Hacia la derecha del $-5$.", "correcta": true}, {"texto": "Hacia la izquierda del $-5$.", "correcta": false}, {"texto": "Entre el $-5$ y el $0$.", "correcta": false}, {"texto": "Hacia ambos lados del $-5$.", "correcta": false}], "explicacion": "El símbolo $\\geq$ implica que la solución abarca los números mayores (hacia la derecha en la recta numérica) e incluye al $-5$."}
{"stable_id": "ALG-GEN-REC-3", "tipo": "conceptual", "nivel": 1, "enunciado": "¿Qué diferencia gráfica existe entre representar $x > 2$ y $x \\geq 2$ en la recta numérica?", "opciones": [{"texto": "En $x \\geq 2$ el círculo en el $2$ se dibuja relleno, y en $x > 2$ se dibuja vacío.", "correcta": true}, {"texto": "En $x > 2$ la flecha va a la izquierda y en $x \\geq 2$ va a la derecha.", "correcta": false}, {"texto": "No hay diferencia gráfica, ambas usan el mismo círculo relleno.", "correcta": false}, {"texto": "En $x > 2$ el círculo está relleno, y en $x \\geq 2$ está vacío.", "correcta": false}], "explicacion": "La igualdad en la inecuación incluye el punto límite, por lo que se rellena el círculo. La desigualdad estricta no incluye el punto, dejando el círculo vacío."}
{"stable_id": "ALG-GEN-REC-4", "tipo": "reconocimiento", "nivel": 1, "enunciado": "Identifica cuál de las siguientes desigualdades corresponde a un gráfico con círculo relleno en el $7$ y flecha hacia la izquierda.", "opciones": [{"texto": "$x \\leq 7$", "correcta": true}, {"texto": "$x < 7$", "correcta": false}, {"texto": "$x \\geq 7$", "correcta": false}, {"texto": "$x > 7$", "correcta": false}], "explicacion": "El círculo relleno implica inclusión y la flecha hacia la izquierda implica menores que, lo que en conjunto resulta en $\\leq$."}
{"stable_id": "ALG-GEN-REC-5", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "Para graficar la inecuación $2x < 8$, el primer paso es ubicar el $8$ en la recta numérica y dibujar un círculo vacío.", "valor_verdad": false, "explicacion": "Falso. Primero se debe resolver la inecuación, obteniendo $x < 4$. Luego se ubica el $4$ en la recta numérica, no el $8$."}
{"stable_id": "ALG-GEN-REC-6", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "La representación gráfica de la solución de $-x \\leq -3$ es una flecha hacia la derecha a partir de un círculo relleno en el $3$.", "valor_verdad": true, "explicacion": "Verdadero. Al multiplicar por $-1$, la inecuación queda $x \\geq 3$. Esto corresponde a un círculo relleno en el $3$ y valores mayores que $3$."}
{"stable_id": "ALG-GEN-REC-7", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "El intervalo $(-\\infty, 5]$ se representa en la recta numérica mediante un círculo vacío en el $5$ y una flecha hacia la izquierda.", "valor_verdad": false, "explicacion": "Falso. El corchete en el $5$ indica que el valor límite está incluido, por lo que el círculo debe estar relleno."}
{"stable_id": "ALG-GEN-REC-8", "tipo": "tipo_paes", "nivel": 3, "enunciado": "¿Qué gráfica en la recta numérica representa la solución de la inecuación $3(x - 1) - 2x > 2$?", "opciones": [{"texto": "Un círculo vacío en $x=5$ y flecha hacia la derecha.", "correcta": true}, {"texto": "Un círculo relleno en $x=5$ y flecha hacia la derecha.", "correcta": false}, {"texto": "Un círculo vacío en $x=1$ y flecha hacia la derecha.", "correcta": false}, {"texto": "Un círculo vacío en $x=5$ y flecha hacia la izquierda.", "correcta": false}], "explicacion": "Resolviendo: $3x - 3 - 2x > 2 \\Rightarrow x - 3 > 2 \\Rightarrow x > 5$. Esto corresponde a un círculo vacío en $5$ y valores mayores dirigidos a la derecha.", "paes_style": true}
{"stable_id": "ALG-GEN-REC-9", "tipo": "tipo_paes", "nivel": 3, "enunciado": "Dada la inecuación $\\frac{x}{2} + 4 \\leq 1$, ¿cuál es su representación en la recta numérica?", "opciones": [{"texto": "Un círculo relleno en $-6$ y flecha hacia la izquierda.", "correcta": true}, {"texto": "Un círculo vacío en $-6$ y flecha hacia la izquierda.", "correcta": false}, {"texto": "Un círculo relleno en $-6$ y flecha hacia la derecha.", "correcta": false}, {"texto": "Un círculo relleno en $6$ y flecha hacia la izquierda.", "correcta": false}], "explicacion": "Resolviendo $\\frac{x}{2} \\leq -3 \\Rightarrow x \\leq -6$. La solución incluye el límite con un círculo relleno y abarca los menores hacia la izquierda.", "paes_style": true}
{"stable_id": "ALG-GEN-REC-10", "tipo": "tipo_paes", "nivel": 3, "enunciado": "Si el conjunto solución de una inecuación se representa por un círculo vacío en el $4$ con la semirrecta dirigiéndose hacia los negativos, ¿qué inecuación modela esta situación?", "opciones": [{"texto": "$-2x + 10 > 2$", "correcta": true}, {"texto": "$3x - 4 > 8$", "correcta": false}, {"texto": "$x + 2 \\leq 6$", "correcta": false}, {"texto": "$x - 4 > 0$", "correcta": false}], "explicacion": "La gráfica corresponde a $x < 4$. Evaluando la opción correcta: $-2x > -8 \\Rightarrow x < 4$, al dividir por un negativo se invierte la desigualdad.", "paes_style": true}"""
    },
    "MAT.ALG.INECUACIONES_LINEALES.VERIFICACION_SOLUCION": {
        "yaml": r"""semantic_id: MAT.ALG.INECUACIONES_LINEALES.VERIFICACION_SOLUCION
titulo: Verificación de soluciones en inecuaciones lineales
objetivo: comprobar si un valor numérico específico pertenece al conjunto solución de una inecuación lineal evaluando la desigualdad
introduccion: Verificar si un número es solución de una inecuación consiste en sustituir la variable por dicho número y comprobar si la desigualdad resultante es matemáticamente correcta.
resumen: La verificación consiste en reemplazar la incógnita por el valor dado y operar aritméticamente ambos lados de la desigualdad. Si se obtiene una afirmación verdadera el número es solución; de lo contrario, no lo es.
explicacion: |
  ### Definición formal
  Dada una inecuación lineal $P(x) \diamond Q(x)$, donde $P(x)$ y $Q(x)$ son expresiones algebraicas de primer grado y $\diamond \in \{<, >, \leq, \geq\}$, un número real $a$ pertenece al conjunto solución de la inecuación si y solo si la proposición $P(a) \diamond Q(a)$ es verdadera.

  La evaluación requiere el reemplazo de la variable $x$ por el escalar $a$, seguido de la simplificación aritmética estricta de ambos miembros de la desigualdad.

  ### Desarrollo didáctico
  A diferencia de una ecuación, donde la solución suele ser un único número, una inecuación tiene un conjunto infinito de soluciones. A veces necesitamos saber si un número en particular sirve o no para una inecuación.

  Para saberlo, hacemos una prueba simple:
  En el lugar de la incógnita, colocamos el número que queremos probar. Luego realizamos todas las operaciones aritméticas que haya a cada lado del símbolo de desigualdad.

  Al final, nos quedará una comparación entre dos números, por ejemplo, $7 > 2$ o $4 \leq 1$. Si lo que leemos es verdad, entonces el número que probamos sí es una solución. Si lo que leemos es mentira, entonces el número no es una solución.
procedimiento:
  - "Sustituir la variable de la inecuación por el valor numérico a evaluar."
  - "Resolver las operaciones matemáticas en ambos lados de la desigualdad, respetando la jerarquía de las operaciones."
  - "Comparar los resultados finales utilizando el símbolo de la desigualdad original."
  - "Concluir que el número es solución si la afirmación es cierta, o que no lo es si es falsa."
ejemplos:
  - titulo: "Verificación de un valor que es solución"
    enunciado: "Verifica si $x = 4$ es solución de la inecuación $3x - 2 > 7$."
    solucion_pasos:
      - "Sustituimos $x = 4$ en la inecuación: $3(4) - 2 > 7$."
      - "Multiplicamos: $12 - 2 > 7$."
      - "Restamos: $10 > 7$."
      - "Como $10$ es mayor que $7$, la desigualdad es verdadera. Por lo tanto, $x = 4$ sí es solución."
  - titulo: "Verificación de un límite no incluido"
    enunciado: "Determina si $x = -1$ es solución de $5x + 3 < -2$."
    solucion_pasos:
      - "Sustituimos $x = -1$ en la inecuación: $5(-1) + 3 < -2$."
      - "Multiplicamos: $-5 + 3 < -2$."
      - "Sumamos: $-2 < -2$."
      - "Como $-2$ no es estrictamente menor que $-2$, la afirmación es falsa. Por lo tanto, $x = -1$ no es solución."
  - titulo: "¿Se incluye el límite en la igualdad?"
    respuesta: "Sí"
    solucion_pasos:
      - "La inecuación evaluada es $2x \leq 6$ y el valor a verificar es $x = 3$."
      - "Sustituimos $x = 3$ obteniendo: $2(3) \leq 6$."
      - "Obtenemos $6 \leq 6$. Dado que $6$ es igual a $6$, la condición se cumple."
      - "El número $x = 3$ efectivamente es solución de la inecuación."
  - titulo: "¿Cualquier número positivo es solución?"
    respuesta: "No"
    solucion_pasos:
      - "Dada la inecuación $-2x < -10$, se evalúa si $x = 2$ la cumple."
      - "Sustituyendo $x=2$ se obtiene: $-2(2) < -10$."
      - "Obtenemos $-4 < -10$. Esto es falso, ya que $-4$ es mayor que $-10$."
      - "No todos los números positivos son soluciones. En este caso, el valor no es solución."
errores_frecuentes:
  - "Creer que si se obtiene la igualdad en una desigualdad estricta, el número evaluado es solución."
  - "Resolver mal las operaciones aritméticas por errores de signos al evaluar el número."
  - "Concluir erróneamente asumiendo que un número negativo mayor en valor absoluto es mayor matemáticamente."
  - "Evaluar solo uno de los lados cuando la inecuación tiene variables en ambos miembros."
  - "Olvidar la jerarquía de las operaciones al sustituir el valor numérico en la expresión."
fuente: "Creación propia"
estado: publicado""",
        "jsonl": r"""{"stable_id": "ALG-GEN-VER-1", "tipo": "conceptual", "nivel": 1, "enunciado": "¿Qué significa que un número verifique una inecuación?", "opciones": [{"texto": "Que al sustituir la variable por el número, se obtiene una desigualdad verdadera.", "correcta": true}, {"texto": "Que al reemplazar el número, la inecuación se transforma en una ecuación.", "correcta": false}, {"texto": "Que el número es el único que puede hacer verdadera la desigualdad.", "correcta": false}, {"texto": "Que ambos lados de la inecuación dan un resultado positivo al evaluarlo.", "correcta": false}], "explicacion": "Verificar una inecuación significa comprobar que el valor reemplazado hace que la relación matemática indicada por el signo de desigualdad sea cierta."}
{"stable_id": "ALG-GEN-VER-2", "tipo": "conceptual", "nivel": 1, "enunciado": "Si al evaluar un número en una inecuación que usa el signo $\\leq$ se obtiene el resultado $5 \\leq 5$, ¿el número evaluado es solución?", "opciones": [{"texto": "Sí, porque el símbolo $\\leq$ significa menor o igual, y la igualdad es cierta.", "correcta": true}, {"texto": "No, porque $5$ no es estrictamente menor que $5$.", "correcta": false}, {"texto": "Sí, pero solo si la inecuación original tenía un signo positivo.", "correcta": false}, {"texto": "No, porque el resultado debe ser cero para ser solución.", "correcta": false}], "explicacion": "El símbolo $\\leq$ incluye la condición de igualdad. Como $5 = 5$ es verdadero, el número evaluado cumple la inecuación."}
{"stable_id": "ALG-GEN-VER-3", "tipo": "conceptual", "nivel": 1, "enunciado": "Al sustituir un número en una inecuación de la forma $P(x) > Q(x)$ y resolver, se obtiene $-3 > 1$. ¿Cuál es la conclusión correcta?", "opciones": [{"texto": "El número evaluado no es parte de la solución de la inecuación.", "correcta": true}, {"texto": "El número evaluado es la solución de la inecuación.", "correcta": false}, {"texto": "Hay un error, ya que no se pueden comparar números negativos.", "correcta": false}, {"texto": "La inecuación debe ser multiplicada por $-1$ para corregirla.", "correcta": false}], "explicacion": "La afirmación $-3 > 1$ es falsa porque un número negativo no es mayor que un positivo. Por lo tanto, el número no forma parte del conjunto solución."}
{"stable_id": "ALG-GEN-VER-4", "tipo": "reconocimiento", "nivel": 1, "enunciado": "¿Cuál de los siguientes valores es solución de la inecuación $x + 2 < 0$?", "opciones": [{"texto": "$-3$", "correcta": true}, {"texto": "$-2$", "correcta": false}, {"texto": "$0$", "correcta": false}, {"texto": "$2$", "correcta": false}], "explicacion": "Al sustituir $x = -3$, obtenemos $-3 + 2 < 0$, es decir, $-1 < 0$, lo cual es verdadero."}
{"stable_id": "ALG-GEN-VER-5", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "El valor $x = 0$ es solución de la inecuación $4x - 5 \\geq -3$.", "valor_verdad": false, "explicacion": "Falso. Al evaluar $x = 0$, queda $4(0) - 5 \\geq -3 \\Rightarrow -5 \\geq -3$. Esto es falso, ya que $-5$ es menor que $-3$."}
{"stable_id": "ALG-GEN-VER-6", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "Para la inecuación $3 - 2x < 7$, el valor $x = -1$ es una de sus soluciones.", "valor_verdad": true, "explicacion": "Verdadero. Evaluando $x = -1$: $3 - 2(-1) < 7 \\Rightarrow 3 + 2 < 7 \\Rightarrow 5 < 7$. Esto es verdadero."}
{"stable_id": "ALG-GEN-VER-7", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "Si evaluamos $x = 2$ en la inecuación $x + 4 > 2x$, obtenemos una desigualdad verdadera, por lo que $2$ es solución.", "valor_verdad": true, "explicacion": "Verdadero. Al sustituir: $2 + 4 > 2(2) \\Rightarrow 6 > 4$. Como $6$ es mayor que $4$, la desigualdad es verdadera y $x = 2$ es solución."}
{"stable_id": "ALG-GEN-VER-8", "tipo": "tipo_paes", "nivel": 3, "enunciado": "Dada la inecuación $2(x - 3) \\leq 5x + 3$, ¿cuál de los siguientes conjuntos contiene SOLO valores que son soluciones?", "opciones": [{"texto": "$\\{-3, 0, 5\\}$", "correcta": true}, {"texto": "$\\{-5, -4, -3\\}$", "correcta": false}, {"texto": "$\\{-10, 0, 10\\}$", "correcta": false}, {"texto": "$\\{-6, -5, 1\\}$", "correcta": false}], "explicacion": "Resolviendo la inecuación: $2x - 6 \\leq 5x + 3 \\Rightarrow -9 \\leq 3x \\Rightarrow x \\geq -3$. Solo el conjunto $\\{-3, 0, 5\\}$ contiene únicamente valores mayores o iguales a $-3$.", "paes_style": true}
{"stable_id": "ALG-GEN-VER-9", "tipo": "tipo_paes", "nivel": 3, "enunciado": "María afirma que $x = \\frac{1}{2}$ es solución de la inecuación $4x - 1 < x + \\frac{3}{2}$. ¿Es correcta la afirmación de María y por qué?", "opciones": [{"texto": "Sí, porque al evaluar queda $1 < 2$, lo cual es verdadero.", "correcta": true}, {"texto": "No, porque al evaluar se obtienen fracciones, y las soluciones deben ser enteras.", "correcta": false}, {"texto": "Sí, porque al resolver se obtiene $x > \\frac{5}{6}$, y $\\frac{1}{2}$ pertenece a ese rango.", "correcta": false}, {"texto": "No, porque al evaluar queda $2 < \\frac{3}{2}$, lo cual es falso.", "correcta": false}], "explicacion": "Al evaluar $x = \\frac{1}{2}$ queda $4(\\frac{1}{2}) - 1 = 2 - 1 = 1$. Y $x + \\frac{3}{2} = \\frac{1}{2} + \\frac{3}{2} = 2$. Por lo tanto queda $1 < 2$, que es verdadero.", "paes_style": true}
{"stable_id": "ALG-GEN-VER-10", "tipo": "tipo_paes", "nivel": 3, "enunciado": "Si $m$ es un número negativo, ¿qué valor(es) de $x$ satisface(n) siempre la inecuación $mx > m$?", "opciones": [{"texto": "Cualquier número menor que $1$.", "correcta": true}, {"texto": "Cualquier número mayor que $1$.", "correcta": false}, {"texto": "Cualquier número positivo.", "correcta": false}, {"texto": "Cualquier número negativo.", "correcta": false}], "explicacion": "Al dividir la inecuación $mx > m$ por $m$, que es negativo, el sentido de la desigualdad se invierte obteniendo $x < 1$. Por lo tanto, cualquier número menor que $1$ verifica la inecuación.", "paes_style": true}"""
    }
}

if __name__ == "__main__":
    print("Script executed successfully.")

import os

topics = {
    "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION": {
        "yaml": r"""semantic_id: MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION
titulo: Planteamiento de Inecuaciones
objetivo: Modelar situaciones de la vida real mediante el planteamiento de inecuaciones lineales.
introduccion: En muchas situaciones cotidianas, las restricciones no son igualdades exactas, sino límites o condiciones de "al menos", "como máximo", "mayor que" o "menor que". El planteamiento de inecuaciones nos permite representar y resolver estos escenarios de manera matemática.
resumen: Plantear una inecuación consiste en traducir una situación verbal que involucra desigualdades a una expresión algebraica, identificando la incógnita y la relación de orden correspondiente.
explicacion: |
  ### Definición formal
  Una inecuación es una expresión algebraica que relaciona variables y constantes mediante los signos de desigualdad $<$, $>$, $\leq$ o $\geq$. Modelar una situación implica definir una variable $x$ y construir una inecuación de la forma $ax + b < c$, u otra equivalente, que represente fielmente las restricciones del problema.

  ### Desarrollo didáctico
  Para plantear una inecuación, es fundamental identificar las palabras clave en el enunciado. Expresiones como "como máximo" o "a lo más" se traducen en $\leq$; "como mínimo" o "al menos" corresponden a $\geq$; "menor que" o "no supera" indican $<$; y "mayor que" o "supera" implican $>$. Al definir claramente qué representa la variable, se puede estructurar la desigualdad paso a paso.
procedimiento:
  - Leer comprensivamente el problema e identificar la incógnita principal, asignándole una letra (por ejemplo, $x$).
  - Identificar las palabras clave que determinan el tipo de desigualdad ($<, >, \leq, \geq$).
  - Relacionar los datos numéricos con la incógnita formando la expresión algebraica correspondiente a un lado de la desigualdad.
  - Escribir la inecuación completa estableciendo la relación entre la expresión obtenida y la restricción dada.
ejemplos:
  - titulo: Presupuesto para compras
    enunciado: Juan tiene $50000 para comprar cuadernos que cuestan $1500 cada uno y una mochila de $20000. ¿Cuál es la inecuación que modela la cantidad máxima de cuadernos que puede comprar?
    solucion_pasos:
      - "Sea $x$ la cantidad de cuadernos a comprar."
      - "El costo de los cuadernos es $1500x$ y el de la mochila $20000$."
      - "El costo total es $1500x + 20000$."
      - "Como tiene $50000 en total, el costo no puede superar esta cantidad ($\leq$)."
      - "La inecuación es $1500x + 20000 \leq 50000$."
  - titulo: Puntaje para aprobar
    enunciado: En un curso, la nota final se calcula sumando tres pruebas. María tiene 65 y 70 en las dos primeras. Si necesita al menos 200 puntos en total para aprobar, ¿qué inecuación representa la nota que debe obtener en la tercera prueba?
    solucion_pasos:
      - "Sea $x$ la nota de la tercera prueba."
      - "La suma de las notas es $65 + 70 + x$, es decir, $135 + x$."
      - "Necesita 'al menos' 200 puntos, lo que significa $\geq$."
      - "La inecuación resultante es $135 + x \geq 200$."
  - titulo: Identificación de la desigualdad "al menos"
    respuesta: "Sí"
    solucion_pasos:
      - "El enunciado dice: Un ascensor soporta al menos 400 kg."
      - "La expresión 'al menos' incluye el 400 y todos los valores mayores."
      - "Por lo tanto, se modela con el símbolo $\geq$."
      - "La inecuación correcta para el peso $P$ sería $P \geq 400$."
  - titulo: Identificación de la desigualdad "no supera"
    respuesta: "No"
    solucion_pasos:
      - "El enunciado dice: La velocidad de un vehículo no supera los 80 km/h."
      - "La frase 'no supera' significa que puede ser 80 o menos, lo que corresponde a $\leq$."
      - "Representarlo con $>$ sería incorrecto."
      - "La inecuación correcta para la velocidad $v$ es $v \leq 80$."
errores_frecuentes:
  - "Traducir 'a lo sumo' o 'como máximo' usando el símbolo de mayor que ($>$)."
  - "Confundir las expresiones 'menor que' ($<$) con 'menor o igual a' ($\leq$) al plantear el problema."
  - "Olvidar definir claramente qué representa la variable antes de armar la inecuación."
  - "Ignorar los valores fijos o constantes en el problema y multiplicar la variable por el total."
  - "Invertir el orden de los términos en una resta, como traducir 'la diferencia entre 5 y $x$' como $x - 5$."
fuente: "Creación propia"
estado: publicado
""",
        "jsonl": r"""{"stable_id": "PLI-GEN-1-1", "semantic_id": "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION", "type": "multiple_choice", "difficulty": 1, "question": "¿Qué símbolo de desigualdad corresponde a la frase 'como máximo'?", "options": ["$<$", "$>$", "$\leq$", "$\geq$"], "correct_answer_index": 2, "explanation": "La expresión 'como máximo' indica que un valor no puede superar un límite, pudiendo ser igual a él, lo que se representa con $\leq$."}
{"stable_id": "PLI-GEN-1-2", "semantic_id": "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION", "type": "multiple_choice", "difficulty": 1, "question": "¿Cómo se traduce matemáticamente 'al menos $x$'?", "options": ["$x <$ algo", "algo $\leq x$", "algo $\geq x$", "algo $= x$"], "correct_answer_index": 2, "explanation": "'Al menos' indica un mínimo, por lo que la cantidad debe ser mayor o igual a ese mínimo ($\geq$)."}
{"stable_id": "PLI-GEN-1-3", "semantic_id": "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION", "type": "multiple_choice", "difficulty": 1, "question": "¿Qué frase se asocia correctamente al símbolo $>$?", "options": ["A lo más", "No supera", "Es estrictamente menor a", "Es mayor a"], "correct_answer_index": 3, "explanation": "El símbolo $>$ representa 'mayor a' y es una desigualdad estricta."}
{"stable_id": "PLI-GEN-1-4", "semantic_id": "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION", "type": "multiple_choice", "difficulty": 1, "question": "Si $P$ representa el peso y 'el peso no debe exceder los 50 kg', ¿qué inecuación lo modela?", "options": ["$P < 50$", "$P > 50$", "$P \leq 50$", "$P \geq 50$"], "correct_answer_index": 2, "explanation": "'No debe exceder' significa que puede ser 50 o menos, es decir, $P \leq 50$."}
{"stable_id": "PLI-GEN-2-1", "semantic_id": "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION", "type": "true_false", "difficulty": 2, "question": "La situación 'el triple de un número aumentado en dos es a lo menos quince' se modela como $3x + 2 \geq 15$.", "correct_answer": true, "explanation": "El triple de un número es $3x$, aumentado en dos es $+ 2$. 'A lo menos quince' es $\geq 15$. Por lo tanto, es verdadero."}
{"stable_id": "PLI-GEN-2-2", "semantic_id": "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION", "type": "true_false", "difficulty": 2, "question": "La expresión 'la mitad de un número es como máximo 10' se modela como $\frac{x}{2} > 10$.", "correct_answer": false, "explanation": "'Como máximo' implica $\leq$, no $>$. La forma correcta es $\frac{x}{2} \leq 10$."}
{"stable_id": "PLI-GEN-2-3", "semantic_id": "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION", "type": "true_false", "difficulty": 2, "question": "El modelo $2x - 5 < 20$ representa 'el doble de un número disminuido en cinco es inferior a veinte'.", "correct_answer": true, "explanation": "El doble de un número ($2x$) disminuido en cinco ($- 5$) es inferior a veinte ($< 20$). Es correcto."}
{"stable_id": "PLI-GEN-3-1", "semantic_id": "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION", "type": "multiple_choice", "difficulty": 3, "paes_style": true, "question": "Un estacionamiento cobra un cargo fijo de $\$1\,000$ más $\$500$ por cada hora de uso. Si Pedro dispone de un máximo de $\$4\,000$, ¿cuál de las siguientes inecuaciones permite determinar el número máximo de horas $h$ que puede estacionar su vehículo?", "options": ["$1000 + 500h < 4000$", "$1000 + 500h \leq 4000$", "$500 + 1000h \leq 4000$", "$1000 + 500h \geq 4000$"], "correct_answer_index": 1, "explanation": "El costo se calcula como $1000 + 500h$. Como tiene 'un máximo de', el costo debe ser menor o igual a $4000$, por lo que $1000 + 500h \leq 4000$."}
{"stable_id": "PLI-GEN-3-2", "semantic_id": "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION", "type": "multiple_choice", "difficulty": 3, "paes_style": true, "question": "Una fábrica produce sillas con un costo fijo de $\$50\,000$ mensuales y un costo de producción de $\$2\,000$ por cada silla. Si el presupuesto mensual no puede superar los $\$150\,000$, ¿qué inecuación modela la cantidad $x$ de sillas que pueden producirse?", "options": ["$50000 + 2000x \leq 150000$", "$50000 + 2000x < 150000$", "$2000x - 50000 \leq 150000$", "$50000 + 2000x \geq 150000$"], "correct_answer_index": 0, "explanation": "El costo total es $50000 + 2000x$. 'No puede superar' se traduce como $\leq$. Así, $50000 + 2000x \leq 150000$."}
{"stable_id": "PLI-GEN-3-3", "semantic_id": "MAT.ALG.MODELAMIENTO_DESIGUALDADES.PLANTEAMIENTO_INECUACION", "type": "multiple_choice", "difficulty": 3, "paes_style": true, "question": "Un plan de telefonía celular ofrece $100$ minutos libres por un cargo fijo mensual de $\$8\,000$. Cada minuto adicional tiene un costo de $\$50$. Si un cliente no desea que su cuenta mensual supere los $\$12\,000$, ¿cuál inecuación permite calcular el máximo de minutos adicionales $m$ que puede hablar?", "options": ["$8000 + 50m < 12000$", "$8000 + 50(m - 100) \leq 12000$", "$8000 + 50m \leq 12000$", "$50m \leq 12000$"], "correct_answer_index": 2, "explanation": "El costo de la cuenta es el cargo fijo más el costo de los minutos adicionales. Esto es $8000 + 50m$. Como no desea superar los $12000$, la inecuación es $8000 + 50m \leq 12000$."}
"""
    },
    "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION": {
        "yaml": r"""semantic_id: MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION
titulo: Conjunto Solución de Inecuaciones Lineales
objetivo: Determinar y representar el conjunto solución de inecuaciones lineales en una variable.
introduccion: A diferencia de las ecuaciones lineales, que suelen tener una única solución, las inecuaciones lineales generalmente tienen infinitas soluciones. Estas soluciones conforman un conjunto que representa todos los valores posibles que satisfacen la desigualdad y se pueden visualizar en la recta numérica o expresar mediante intervalos.
resumen: El conjunto solución de una inecuación lineal es el intervalo de números reales que hacen verdadera la desigualdad. Se puede expresar de forma gráfica, por comprensión o mediante notación de intervalos.
explicacion: |
  ### Definición formal
  Sea una inecuación de la forma $ax + b < 0$ (o con $\leq, >, \geq$), con $a, b \in \mathbb{R}$ y $a \neq 0$. El conjunto solución $S$ es el subconjunto de $\mathbb{R}$ dado por $S = \{ x \in \mathbb{R} \mid ax + b < 0 \}$. Dependiendo del signo de la desigualdad, el conjunto solución corresponde a intervalos de la forma $(-\infty, c)$, $(-\infty, c]$, $(c, \infty)$ o $[c, \infty)$.

  ### Desarrollo didáctico
  Encontrar el conjunto solución requiere despejar la incógnita de la misma manera que en una ecuación, prestando especial atención a una regla fundamental: si se multiplica o divide la inecuación por un número negativo, el sentido de la desigualdad debe invertirse. Una vez aislada la variable (por ejemplo, $x \geq 3$), se interpreta el resultado. En la recta numérica, se usaría un punto relleno en el 3 y una flecha hacia la derecha. En notación de intervalos, se escribiría como $[3, \infty)$.
procedimiento:
  - Agrupar los términos con la variable en un lado de la desigualdad y las constantes en el otro.
  - Simplificar ambos lados sumando o restando términos semejantes.
  - Despejar la variable dividiendo o multiplicando por su coeficiente. Recordar que si el coeficiente es negativo, se debe invertir el signo de la desigualdad.
  - Expresar la solución final usando notación de intervalo, conjunto o representación gráfica según sea requerido.
ejemplos:
  - titulo: Inecuación básica
    enunciado: Encuentra el conjunto solución de la inecuación $2x - 4 > 6$.
    solucion_pasos:
      - "Sumamos 4 a ambos lados: $2x > 6 + 4$."
      - "Simplificamos: $2x > 10$."
      - "Dividimos por 2 (positivo, por lo que no cambia el signo): $x > 5$."
      - "El conjunto solución en intervalo es $(5, \infty)$."
  - titulo: Coeficiente negativo
    enunciado: Resuelve la inecuación $-3x + 1 \geq 10$.
    solucion_pasos:
      - "Restamos 1 a ambos lados: $-3x \geq 9$."
      - "Dividimos por $-3$. Como es negativo, invertimos el signo de la desigualdad: $x \leq -3$."
      - "El conjunto solución es $(-\infty, -3]$."
  - titulo: Comprobación de un intervalo solución
    respuesta: "Sí"
    solucion_pasos:
      - "Consideramos la inecuación $x + 2 < 5$."
      - "Restando 2, obtenemos $x < 3$."
      - "El intervalo correspondiente a los números estrictamente menores a 3 es $(-\infty, 3)$."
      - "Por tanto, el conjunto solución está correctamente expresado."
  - titulo: Análisis de extremo incluido
    respuesta: "No"
    solucion_pasos:
      - "Observamos la inecuación $4x \geq 8$."
      - "Al dividir por 4, resulta $x \geq 2$."
      - "Como es mayor o igual, el 2 debe estar incluido (corchete cerrado), es decir, $[2, \infty)$."
      - "Expresar la solución como $(2, \infty)$ sería incorrecto al omitir el 2."
errores_frecuentes:
  - "Olvidar invertir el signo de la desigualdad al multiplicar o dividir por un número negativo."
  - "Confundir los corchetes abiertos y cerrados al escribir la notación de intervalos."
  - "Representar gráficamente un intervalo cerrado con un círculo sin pintar (hueco)."
  - "Creer que el conjunto solución siempre está acotado por ambos lados."
  - "Sumar o restar un número negativo y erróneamente invertir el signo de la desigualdad (solo aplica a multiplicación/división)."
fuente: "Creación propia"
estado: publicado
""",
        "jsonl": r"""{"stable_id": "CSO-GEN-1-1", "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION", "type": "multiple_choice", "difficulty": 1, "question": "¿Qué intervalo representa la desigualdad $x \geq -2$?", "options": ["$(-\infty, -2)$", "$(-2, \infty)$", "$[-2, \infty)$", "$( -\infty, -2]$"], "correct_answer_index": 2, "explanation": "La desigualdad $\geq$ indica que los valores son mayores o iguales a $-2$. Por tanto, el intervalo empieza en $-2$ (incluido) y va hasta infinito: $[-2, \infty)$."}
{"stable_id": "CSO-GEN-1-2", "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION", "type": "multiple_choice", "difficulty": 1, "question": "¿Cómo se lee el intervalo $(-\infty, 4)$?", "options": ["Todos los números reales mayores a 4", "Todos los números reales menores a 4", "Todos los números reales menores o iguales a 4", "Todos los números reales mayores o iguales a 4"], "correct_answer_index": 1, "explanation": "El intervalo $(-\infty, 4)$ contiene a todos los números menores estrictamente a 4, sin incluir el 4."}
{"stable_id": "CSO-GEN-1-3", "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION", "type": "multiple_choice", "difficulty": 1, "question": "¿Qué sucede con el signo de desigualdad cuando se divide una inecuación por un número negativo?", "options": ["Permanece igual", "Desaparece", "Se invierte", "Se convierte en igualdad"], "correct_answer_index": 2, "explanation": "Por las propiedades de las desigualdades, al multiplicar o dividir por un número negativo, la dirección (sentido) de la desigualdad se invierte."}
{"stable_id": "CSO-GEN-1-4", "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION", "type": "multiple_choice", "difficulty": 1, "question": "¿Cuál es la representación gráfica de $x < 3$?", "options": ["Un círculo pintado en 3 y flecha a la derecha", "Un círculo sin pintar en 3 y flecha a la derecha", "Un círculo pintado en 3 y flecha a la izquierda", "Un círculo sin pintar en 3 y flecha a la izquierda"], "correct_answer_index": 3, "explanation": "Al ser menor estricto ($<$), no se incluye el 3 (círculo sin pintar) y son los valores menores (flecha a la izquierda)."}
{"stable_id": "CSO-GEN-2-1", "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION", "type": "true_false", "difficulty": 2, "question": "La solución de $-2x > 8$ es $x < -4$.", "correct_answer": true, "explanation": "Al dividir ambos lados por $-2$, el signo de desigualdad debe invertirse, resultando en $x < -4$. Es correcto."}
{"stable_id": "CSO-GEN-2-2", "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION", "type": "true_false", "difficulty": 2, "question": "El conjunto solución de $3x - 1 \leq 5$ es $(-\infty, 2)$.", "correct_answer": false, "explanation": "Al sumar 1 resulta $3x \leq 6$. Dividiendo por 3, $x \leq 2$. El intervalo es $(-\infty, 2]$, con corchete cerrado. Por tanto es falso."}
{"stable_id": "CSO-GEN-2-3", "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION", "type": "true_false", "difficulty": 2, "question": "El número $0$ pertenece al conjunto solución de $5 - x < 2$.", "correct_answer": false, "explanation": "Al resolver, $-x < 2 - 5 \Rightarrow -x < -3 \Rightarrow x > 3$. El número $0$ no es mayor a $3$, por lo que no pertenece."}
{"stable_id": "CSO-GEN-3-1", "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION", "type": "multiple_choice", "difficulty": 3, "paes_style": true, "question": "¿Cuál de los siguientes intervalos representa el conjunto solución de la inecuación $\frac{3 - 2x}{5} \leq 1$?", "options": ["$[-1, \infty)$", "$( -\infty, -1]$", "$[1, \infty)$", "$( -\infty, 1]$"], "correct_answer_index": 0, "explanation": "Multiplicando por 5 (positivo): $3 - 2x \leq 5$. Restando 3: $-2x \leq 2$. Dividiendo por -2 e invirtiendo el signo: $x \geq -1$. El intervalo es $[-1, \infty)$."}
{"stable_id": "CSO-GEN-3-2", "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION", "type": "multiple_choice", "difficulty": 3, "paes_style": true, "question": "Si $a < 0$, ¿cuál es el conjunto solución de la inecuación $ax + b > 0$?", "options": ["$(-\infty, \frac{-b}{a})$", "$(\frac{-b}{a}, \infty)$", "$(-\infty, \frac{b}{a})$", "$(\frac{b}{a}, \infty)$"], "correct_answer_index": 0, "explanation": "Restando $b$: $ax > -b$. Como $a < 0$, al dividir por $a$ se invierte el signo: $x < \frac{-b}{a}$. Esto corresponde al intervalo $(-\infty, \frac{-b}{a})$."}
{"stable_id": "CSO-GEN-3-3", "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.CONJUNTO_SOLUCION", "type": "multiple_choice", "difficulty": 3, "paes_style": true, "question": "Dada la inecuación $3(x - 2) - 2(x + 1) < x - 8$, ¿cuál es su conjunto solución?", "options": ["$\mathbb{R}$", "El conjunto vacío $\emptyset$", "$( -\infty, 0)$", "$( -\infty, -8)$"], "correct_answer_index": 1, "explanation": "Expandiendo: $3x - 6 - 2x - 2 < x - 8 \Rightarrow x - 8 < x - 8$. Restando $x$ en ambos lados: $-8 < -8$, lo cual es una proposición falsa para cualquier $x$. Por tanto, el conjunto solución es vacío."}
"""
    }
}

def main():
    os.makedirs("scratch", exist_ok=True)
    for semantic_id, content in topics.items():
        yaml_path = f"scratch/{semantic_id}.yaml"
        jsonl_path = f"scratch/{semantic_id}.jsonl"
        with open(yaml_path, "w", encoding="utf-8") as f:
            f.write(content["yaml"])
        with open(jsonl_path, "w", encoding="utf-8") as f:
            f.write(content["jsonl"])
    print("Files successfully generated.")

if __name__ == "__main__":
    main()

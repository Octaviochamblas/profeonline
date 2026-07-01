import os
import json

topics = {
    "MAT.ALG.INECUACIONES_LINEALES.INECUACION_SIN_SOLUCION": {
        "yaml": r"""semantic_id: MAT.ALG.INECUACIONES_LINEALES.INECUACION_SIN_SOLUCION
titulo: Inecuaciones Lineales sin Solución
objetivo: Identificar y resolver inecuaciones lineales que carecen de solución en el conjunto de los números reales.
introduccion: En el estudio de las inecuaciones lineales, existen casos donde las variables se cancelan y resulta en una falsedad lógica. Esto significa que ningún valor real satisface la desigualdad.
resumen: Una inecuación lineal no tiene solución cuando, tras simplificar, se obtiene una proposición falsa del tipo $0 > c$ o $0 \geq c$, con $c$ siendo un número real positivo.
explicacion: |
  ### Definición formal
  Sea una inecuación lineal de la forma $ax + b < cx + d$. Si $a = c$, la inecuación se reduce a $b < d$. Si la proposición matemática resultante es falsa, el conjunto solución es el conjunto vacío, denotado como $S = \emptyset$.

  ### Desarrollo didáctico
  Al resolver inecuaciones, el procedimiento estándar consiste en agrupar los términos con la variable en un lado de la desigualdad y las constantes en el otro. Cuando los coeficientes de la variable son idénticos en ambos miembros, su resta resulta en $0x$, eliminando la variable.
  En este punto, la veracidad de la inecuación depende exclusivamente de las constantes. Si la desigualdad numérica resultante es absurda (por ejemplo, $3 < 1$ o $0 \geq 5$), se concluye que no existe ningún número real $x$ que haga verdadera la expresión inicial.
procedimiento:
  - Simplificar las expresiones algebraicas en ambos lados de la inecuación.
  - Agrupar los términos con la incógnita en un miembro y las constantes en el otro.
  - Observar si los términos con la variable se anulan mutuamente, resultando en $0x$.
  - Evaluar la desigualdad numérica resultante; si es una falsedad, concluir que el conjunto solución es vacío.
ejemplos:
  - titulo: Inecuación con términos idénticos restados
    enunciado: Resolver la inecuación $2x + 5 > 2x + 8$.
    solucion_pasos:
      - Restar $2x$ en ambos lados para agrupar las variables: $2x - 2x + 5 > 8$.
      - Simplificar: $5 > 8$.
      - Como $5 > 8$ es una afirmación falsa, la inecuación original no tiene solución. $S = \emptyset$.
  - titulo: Inecuación con desarrollo de paréntesis
    enunciado: Encontrar el conjunto solución de $3(x - 2) \leq 3x - 10$.
    solucion_pasos:
      - Distribuir el $3$ en el lado izquierdo: $3x - 6 \leq 3x - 10$.
      - Restar $3x$ en ambos miembros: $-6 \leq -10$.
      - Analizar la desigualdad numérica: $-6$ no es menor o igual a $-10$, por lo tanto, es falsa.
      - Concluir que no existe solución real. $S = \emptyset$.
  - titulo: Pregunta sobre veracidad tras simplificar
    respuesta: "No"
    solucion_pasos:
      - Analizar la afirmación: si al cancelar las variables obtenemos $4 < 4$, la afirmación es falsa porque $4$ es igual a $4$, no estrictamente menor.
      - Al ser una proposición falsa, la inecuación no tiene solución.
  - titulo: Pregunta sobre conjunto solución vacío con cero
    respuesta: "Sí"
    solucion_pasos:
      - Identificar la forma de la inecuación: al restar los términos semejantes se obtiene $0 \geq 7$.
      - Comprobar que $0$ no es mayor o igual que $7$, lo que constituye una contradicción matemática.
      - Por lo tanto, es correcto afirmar que el conjunto solución es vacío.
errores_frecuentes:
  - Asumir que $0x > 5$ implica que $x$ puede tomar cualquier valor real.
  - Concluir que $x = 0$ es la solución cuando la variable se cancela al reducir términos semejantes.
  - Confundir la falsedad de la proposición numérica con un error de cálculo y forzar una solución.
  - Creer que una desigualdad estricta falsa como $2 < 2$ tiene a $x = 2$ como solución.
  - Anotar el conjunto solución como el número cero en lugar del conjunto vacío $\emptyset$.
fuente: ProfeOnline
estado: publicado
""",
        "jsonl": [
            {"id": "ILS-GEN-CONC-1", "type": "multiple_choice", "nivel": 1, "text": "¿Qué ocurre matemáticamente cuando una inecuación lineal no tiene solución?", "options": [{"text": "Se obtiene una proposición numérica falsa después de cancelar las variables.", "is_correct": True}, {"text": "El valor de la variable se vuelve infinito.", "is_correct": False}, {"text": "Se obtiene una proposición numérica verdadera como $5 = 5$.", "is_correct": False}, {"text": "La variable $x$ queda igualada a cero.", "is_correct": False}]},
            {"id": "ILS-GEN-CONC-2", "type": "multiple_choice", "nivel": 1, "text": r"Si al resolver una inecuación lineal se llega a la expresión $0x > 4$, ¿cuál es el conjunto solución?", "options": [{"text": r"El conjunto vacío $\emptyset$.", "is_correct": True}, {"text": r"Todos los números reales $\mathbb{R}$.", "is_correct": False}, {"text": "El número $4$.", "is_correct": False}, {"text": "El número $0$.", "is_correct": False}]},
            {"id": "ILS-GEN-CONC-3", "type": "multiple_choice", "nivel": 1, "text": "¿Cómo se representa el conjunto solución de una inecuación donde ninguna variable cumple la desigualdad?", "options": [{"text": r"$S = \emptyset$", "is_correct": True}, {"text": r"$S = \mathbb{R}$", "is_correct": False}, {"text": r"$S = \{0\}$", "is_correct": False}, {"text": r"$S = [0, \infty)$", "is_correct": False}]},
            {"id": "ILS-GEN-RECO-1", "type": "multiple_choice", "nivel": 1, "text": "¿Cuál de las siguientes inecuaciones carece de solución en los números reales?", "options": [{"text": "$x < x - 1$", "is_correct": True}, {"text": "$x > x - 1$", "is_correct": False}, {"text": "$2x < x + 1$", "is_correct": False}, {"text": "$x + 2 > x$", "is_correct": False}]},
            {"id": "ILS-GEN-PROC-1", "type": "true_false", "nivel": 2, "text": r"Al resolver la inecuación $5x + 2 \leq 5x - 3$, el conjunto solución es vacío.", "answer": True},
            {"id": "ILS-GEN-PROC-2", "type": "true_false", "nivel": 2, "text": "La inecuación $x + 4 > x + 4$ tiene como solución a todos los números reales.", "answer": False},
            {"id": "ILS-GEN-PROC-3", "type": "true_false", "nivel": 2, "text": "Si desarrollamos $2(x - 1) < 2x$, concluimos que no tiene solución.", "answer": False},
            {"id": "ILS-GEN-PAES-1", "type": "multiple_choice", "nivel": 3, "paes_style": True, "text": r"Dada la inecuación $3(x - 1) + 2 \geq 3x + 5$, ¿cuál es el conjunto solución?", "options": [{"text": r"$\emptyset$", "is_correct": True}, {"text": r"$\mathbb{R}$", "is_correct": False}, {"text": r"$[0, \infty)$", "is_correct": False}, {"text": r"$(-\infty, 0]$", "is_correct": False}]},
            {"id": "ILS-GEN-PAES-2", "type": "multiple_choice", "nivel": 3, "paes_style": True, "text": "Se tiene la desigualdad $ax + b < ax + c$. ¿Bajo qué condición el sistema NO tiene solución?", "options": [{"text": r"$b \geq c$", "is_correct": True}, {"text": "$b < c$", "is_correct": False}, {"text": "$a = 0$", "is_correct": False}, {"text": "$b = c$", "is_correct": False}]},
            {"id": "ILS-GEN-PAES-3", "type": "multiple_choice", "nivel": 3, "paes_style": True, "text": r"Si se evalúa la inecuación $\frac{x}{2} + 1 > \frac{x+4}{2}$, ¿qué se puede afirmar sobre su conjunto solución?", "options": [{"text": "Es el conjunto vacío, ya que resulta en $1 > 2$.", "is_correct": True}, {"text": "Son todos los reales, pues resulta en $1 > 0$.", "is_correct": False}, {"text": "El conjunto solución depende del valor de $x$.", "is_correct": False}, {"text": "El conjunto solución incluye solo a los números positivos.", "is_correct": False}]}
        ]
    },
    "MAT.ALG.INECUACIONES_LINEALES.INECUACION_TODO_REAL": {
        "yaml": r"""semantic_id: MAT.ALG.INECUACIONES_LINEALES.INECUACION_TODO_REAL
titulo: Inecuaciones Lineales con Todos los Reales como Solución
objetivo: Reconocer y resolver inecuaciones lineales cuyo conjunto solución abarca a todos los números reales.
introduccion: A veces, al simplificar una inecuación lineal, la variable desaparece dejando una afirmación matemática que es siempre cierta. En estos escenarios, cualquier valor real que tome la variable satisfará la desigualdad inicial.
resumen: Una inecuación lineal tiene como solución a todos los números reales si, al reducir sus términos, se llega a una tautología o proposición verdadera, tal como $0 \leq c$ o $c < d$, donde la relación numérica es correcta.
explicacion: |
  ### Definición formal
  Considerando una inecuación lineal $ax + b < cx + d$, si $a = c$ y la constante $b$ es estrictamente menor que $d$ ($b < d$), la expresión se transforma en una proposición lógica verdadera. Como esta verdad es independiente de la variable $x$, el conjunto solución corresponde a la totalidad de los números reales, lo cual se denota como $S = \mathbb{R}$ o $S = (-\infty, \infty)$.

  ### Desarrollo didáctico
  Al enfrentarse a una inecuación, el paso regular es trasladar todos los términos dependientes de la variable a un lado y los términos independientes al otro. Si las variables poseen los mismos coeficientes en ambos lados, se cancelan.
  El resultado es una desigualdad puramente numérica. Si esta desigualdad es lógicamente correcta (por ejemplo, $2 < 5$ o $-1 \leq 0$), indica que la relación inicial se mantiene siempre. Por consiguiente, cualquier número que se reemplace en la variable $x$ hará que la desigualdad original sea correcta.
procedimiento:
  - Desarrollar y simplificar las expresiones en ambos miembros de la inecuación.
  - Reunir los términos con la variable en un solo lado de la desigualdad.
  - Verificar si los coeficientes de las variables son iguales, causando su anulación ($0x$).
  - Evaluar la desigualdad numérica resultante; si es una proposición verdadera, concluir que la solución son todos los números reales.
ejemplos:
  - titulo: Inecuación con proposición verdadera
    enunciado: Determinar el conjunto solución de $4x - 1 < 4x + 3$.
    solucion_pasos:
      - Restar $4x$ en ambos miembros para agrupar las incógnitas: $4x - 4x - 1 < 3$.
      - Simplificar los términos algebraicos: $-1 < 3$.
      - Observar que $-1 < 3$ es una afirmación siempre verdadera.
      - Concluir que el conjunto solución abarca a todos los reales: $S = \mathbb{R}$.
  - titulo: Resolución con distribución de coeficientes
    enunciado: Resolver la inecuación $5(x + 1) \geq 5x + 5$.
    solucion_pasos:
      - Distribuir el coeficiente $5$ en el miembro izquierdo: $5x + 5 \geq 5x + 5$.
      - Restar $5x$ en ambos lados: $5 \geq 5$.
      - Analizar la proposición numérica resultante: $5$ es igual a $5$, por lo que la relación "mayor o igual" se cumple.
      - Concluir que cualquier número real satisface la inecuación: $S = \mathbb{R}$.
  - titulo: Pregunta sobre cancelación de variables con resultado verdadero
    respuesta: "Sí"
    solucion_pasos:
      - Identificar que al restar los términos con la variable obtenemos una desigualdad puramente numérica.
      - Si el resultado es una proposición lógicamente verdadera como $0 < 8$, la desigualdad se cumple sin importar el valor de la variable.
      - Por lo tanto, es correcto que la solución sean todos los números reales.
  - titulo: Pregunta sobre igualdad estricta
    respuesta: "No"
    solucion_pasos:
      - Si al reducir términos obtenemos una expresión como $7 < 7$, debemos evaluarla estrictamente.
      - El número $7$ no es menor que $7$, por lo que es falso.
      - Si la afirmación preguntaba si esto indica que la solución son todos los reales, la respuesta es negativa, pues en este caso no habría solución.
errores_frecuentes:
  - Confundir una proposición verdadera con una falsa, llegando a concluir que no hay solución.
  - Creer que porque la variable se canceló, la solución debe ser obligatoriamente $x = 0$.
  - Expresar la solución indicando "infinito" pero omitiendo que se refiere al conjunto de los números reales $\mathbb{R}$.
  - Pensar que una desigualdad del tipo $3 \geq 3$ es falsa y deducir erróneamente un conjunto vacío.
  - Tratar de despejar la variable inexistente y crear divisiones por cero como $0/0$.
fuente: ProfeOnline
estado: publicado
""",
        "jsonl": [
            {"id": "ITR-GEN-CONC-1", "type": "multiple_choice", "nivel": 1, "text": "¿Qué indica que la solución de una inecuación lineal son todos los números reales?", "options": [{"text": "Se obtiene una desigualdad numérica verdadera luego de que las variables se cancelen.", "is_correct": True}, {"text": r"La variable queda despejada como $x = \mathbb{R}$.", "is_correct": False}, {"text": "Se obtiene una desigualdad numérica falsa como $0 > 5$.", "is_correct": False}, {"text": "El coeficiente de la variable resulta ser un número positivo muy grande.", "is_correct": False}]},
            {"id": "ITR-GEN-CONC-2", "type": "multiple_choice", "nivel": 1, "text": "Si al resolver se llega a la expresión $-2 < 4$, el conjunto solución es:", "options": [{"text": r"Todos los números reales $\mathbb{R}$.", "is_correct": True}, {"text": "El conjunto vacío.", "is_correct": False}, {"text": "El intervalo $(-2, 4)$.", "is_correct": False}, {"text": "Solo los números mayores a $-2$.", "is_correct": False}]},
            {"id": "ITR-GEN-CONC-3", "type": "multiple_choice", "nivel": 1, "text": "¿Cuál es la notación matemática correcta para indicar que todos los números reales son solución?", "options": [{"text": r"$S = \mathbb{R}$", "is_correct": True}, {"text": r"$S = \emptyset$", "is_correct": False}, {"text": r"$S = \{\mathbb{R}\}$", "is_correct": False}, {"text": r"$S = \infty$", "is_correct": False}]},
            {"id": "ITR-GEN-RECO-1", "type": "multiple_choice", "nivel": 1, "text": "¿Cuál de las siguientes inecuaciones tiene como solución a todos los números reales?", "options": [{"text": "$x < x + 2$", "is_correct": True}, {"text": "$x > x + 2$", "is_correct": False}, {"text": "$2x < x + 2$", "is_correct": False}, {"text": "$x + 2 < x$", "is_correct": False}]},
            {"id": "ITR-GEN-PROC-1", "type": "true_false", "nivel": 2, "text": r"Al resolver $x - 3 \leq x + 1$, el conjunto solución abarca a todos los números reales.", "answer": True},
            {"id": "ITR-GEN-PROC-2", "type": "true_false", "nivel": 2, "text": r"La inecuación $2(x + 3) > 2x + 6$ tiene como solución a todo $\mathbb{R}$.", "answer": False},
            {"id": "ITR-GEN-PROC-3", "type": "true_false", "nivel": 2, "text": "El desarrollo de $3x - x < 2x + 1$ da como resultado que todos los reales son solución.", "answer": True},
            {"id": "ITR-GEN-PAES-1", "type": "multiple_choice", "nivel": 3, "paes_style": True, "text": r"Se tiene la inecuación lineal $ax + b \leq ax + c$. ¿Qué condición garantiza que la solución sea $\mathbb{R}$?", "options": [{"text": r"$b \leq c$", "is_correct": True}, {"text": "$b > c$", "is_correct": False}, {"text": "$b = 0$ y $c = 0$", "is_correct": False}, {"text": "$a > 0$", "is_correct": False}]},
            {"id": "ITR-GEN-PAES-2", "type": "multiple_choice", "nivel": 3, "paes_style": True, "text": r"Al simplificar $\frac{2x + 4}{2} > x$, el conjunto solución obtenido es:", "options": [{"text": r"Todos los reales $\mathbb{R}$.", "is_correct": True}, {"text": r"El conjunto vacío $\emptyset$.", "is_correct": False}, {"text": "Solo los reales positivos.", "is_correct": False}, {"text": r"El conjunto $\{2\}$.", "is_correct": False}]},
            {"id": "ITR-GEN-PAES-3", "type": "multiple_choice", "nivel": 3, "paes_style": True, "text": r"Evalúe el conjunto solución de $\pi x + 1 < \pi x + \sqrt{2}$.", "options": [{"text": r"Todos los números reales, ya que $1 < \sqrt{2}$.", "is_correct": True}, {"text": r"Conjunto vacío, pues las variables con $\pi$ se anulan.", "is_correct": False}, {"text": r"Los reales positivos, porque $\sqrt{2}$ es positivo.", "is_correct": False}, {"text": "No se puede determinar sin conocer el valor de $x$.", "is_correct": False}]}
        ]
    }
}

def generate_files():
    os.makedirs("data", exist_ok=True)
    for semantic_id, content in topics.items():
        with open(f"data/{semantic_id}.yaml", "w", encoding="utf-8") as f:
            f.write(content["yaml"])
        with open(f"data/{semantic_id}.jsonl", "w", encoding="utf-8") as f:
            for exercise in content["jsonl"]:
                f.write(json.dumps(exercise, ensure_ascii=False) + "\\n")
    print("Files successfully generated in data/ folder.")

if __name__ == "__main__":
    generate_files()

import os
import json

topics = {
    "MAT.ALG.INECUACIONES_LINEALES.SIGNOS_AGRUPACION": {
        "yaml": r"""semantic_id: MAT.ALG.INECUACIONES_LINEALES.SIGNOS_AGRUPACION
titulo: Inecuaciones Lineales con Signos de Agrupación
objetivo: Resolver inecuaciones lineales que involucren paréntesis y otros signos de agrupación mediante la aplicación correcta de las propiedades algebraicas.
introduccion: En el estudio de las desigualdades, es común encontrar expresiones matemáticas agrupadas en paréntesis o corchetes. Suprimir correctamente estos signos es un paso necesario para despejar la incógnita y encontrar el conjunto solución.
resumen: Para resolver inecuaciones lineales con signos de agrupación se requiere aplicar la propiedad distributiva y considerar los cambios de signo correspondientes, manteniendo la relación de desigualdad original.
explicacion: |
  ### Definición formal
  Una inecuación lineal con signos de agrupación es una expresión de la forma $a(bx+c) + d < e(fx+g) + h$, donde los símbolos de desigualdad pueden ser $<, >, \le, \ge$, y los parámetros numéricos requieren de la aplicación de la propiedad distributiva $p(q+r) = pq+pr$ antes de agrupar términos semejantes.

  ### Desarrollo didáctico
  Cuando se presenta una inecuación que involucra paréntesis, el primer objetivo es eliminar dichas agrupaciones. Esto se logra distribuyendo el factor externo a cada término interno. Es fundamental prestar especial atención a los signos negativos precediendo a un paréntesis, ya que alteran el signo de todos los términos contenidos en él, de acuerdo a $-(x+y) = -x-y$. Una vez suprimidos los paréntesis, se procede a reducir términos semejantes en cada lado de la desigualdad y, finalmente, se utilizan las propiedades de las desigualdades para despejar la incógnita. Recuerde que si multiplica o divide por un número negativo, el sentido de la desigualdad debe invertirse.
procedimiento:
  - "Identificar los signos de agrupación presentes en ambos lados de la inecuación."
  - "Aplicar la propiedad distributiva para multiplicar el factor externo por cada término contenido dentro del paréntesis, respetando la regla de los signos."
  - "Reducir los términos semejantes que resulten en cada miembro de la inecuación."
  - "Aplicar las propiedades aditivas y multiplicativas de las desigualdades para agrupar la incógnita en un lado y despejar su valor, recordando invertir el sentido de la desigualdad al multiplicar o dividir por un valor negativo."
ejemplos:
  - titulo: Inecuación con un paréntesis simple
    enunciado: Determine el conjunto solución de $3(x - 2) > 15$.
    solucion_pasos:
      - "Se aplica la propiedad distributiva: $3x - 6 > 15$."
      - "Se suma $6$ a ambos lados: $3x > 15 + 6$, es decir, $3x > 21$."
      - "Se divide por $3$: $x > 7$."
      - "El conjunto solución es $(7, \\infty)$."
  - titulo: Inecuación con paréntesis en ambos miembros y cambio de signos
    enunciado: Resuelva la inecuación $2(3x - 1) - (x + 4) \le 4(x + 1)$.
    solucion_pasos:
      - "Se aplica la propiedad distributiva en ambos lados, considerando que el signo negativo afecta a $(x + 4)$: $6x - 2 - x - 4 \le 4x + 4$."
      - "Se reducen los términos semejantes en el lado izquierdo: $5x - 6 \le 4x + 4$."
      - "Se agrupan los términos con incógnita a la izquierda y los constantes a la derecha: $5x - 4x \le 4 + 6$."
      - "Se simplifica y obtiene el resultado: $x \le 10$."
      - "El conjunto solución es $(-\infty, 10]$."
  - titulo: Presencia de factor negativo en la agrupación
    respuesta: Sí
    solucion_pasos:
      - "Se nota que al distribuir $-2$ en la expresión $-2(x - 3)$, se obtiene $-2x + 6$."
      - "Aplica esto para simplificar el lado izquierdo, cuidando no invertir prematuramente ninguna desigualdad antes de multiplicar o dividir toda la inecuación por un factor negativo."
      - "Agrupa términos, obteniendo el conjunto final."
  - titulo: Eliminación correcta de paréntesis múltiples
    respuesta: No
    solucion_pasos:
      - "Al observar $4 - (2x - (x + 1))$, es necesario resolver de adentro hacia afuera."
      - "Se aplica primero el signo negativo interno: $4 - (2x - x - 1)$."
      - "Simplifica dentro del paréntesis exterior: $4 - (x - 1)$."
      - "Finalmente distribuye el último negativo: $4 - x + 1 = 5 - x$."
errores_frecuentes:
  - "Al distribuir un factor negativo hacia un paréntesis, se cambia el signo del primer término interno, pero se mantiene igual el signo de los términos restantes."
  - "Si una inecuación contiene la expresión $-(x - 3)$, su eliminación correcta da como resultado $-x - 3$."
  - "Cuando se suprime un paréntesis multiplicado por un número constante positivo, se invierte el símbolo de la desigualdad."
  - "Si se presenta la expresión $2 + 3(x-1) > 0$, se debe sumar primero $2+3=5$ y luego distribuir este $5$ en el paréntesis."
  - "La propiedad distributiva se aplica únicamente a los términos que contengan a la incógnita, ignorando los términos numéricos del paréntesis."
fuente: "Generado por inteligencia artificial para ProfeOnline."
estado: publicado
""",
        "jsonl": r"""{"stable_id": "MALSIGN-GEN-CONC-1", "nivel": 1, "tipo": "conceptual", "estilo": "multiple_choice", "enunciado": "Al enfrentar una inecuación lineal de la forma $a - (bx + c) > d$, ¿cuál es el primer paso algebraico recomendado respecto a la expresión $-(bx + c)$?", "opciones": [{"texto": "Se debe multiplicar toda la inecuación por $-1$ para eliminar el paréntesis.", "correcta": false}, {"texto": "Se debe cambiar el signo solo de $bx$, dejando a $c$ sin modificar.", "correcta": false}, {"texto": "Se debe omitir el signo negativo y simplemente eliminar los paréntesis, ya que no afecta a la variable si está al medio.", "correcta": false}, {"texto": "Se debe aplicar la regla de los signos, distribuyendo el signo negativo de manera que ambos términos adquieran signos opuestos, resultando en $-bx - c$.", "correcta": true}]}
{"stable_id": "MALSIGN-GEN-CONC-2", "nivel": 1, "tipo": "conceptual", "estilo": "multiple_choice", "enunciado": "Considere la expresión $3(x - 4)$ como parte de una inecuación. La propiedad distributiva indica que el factor externo multiplicará:", "opciones": [{"texto": "Solo a la incógnita $x$.", "correcta": false}, {"texto": "A cada uno de los términos dentro del paréntesis, resultando en $3x - 12$.", "correcta": true}, {"texto": "Solo a la constante $-4$.", "correcta": false}, {"texto": "Se suma el $3$ con el término $x$, para luego restar $4$.", "correcta": false}]}
{"stable_id": "MALSIGN-GEN-CONC-3", "nivel": 1, "tipo": "conceptual", "estilo": "multiple_choice", "enunciado": "En la resolución de $x + 2(x + 1) < 4$, un estudiante erróneamente escribe $x + 2x + 1 < 4$. ¿Qué concepto omitió en este paso?", "opciones": [{"texto": "Olvidó invertir el signo de la desigualdad tras distribuir.", "correcta": false}, {"texto": "Distribuyó incorrectamente el factor $2$, aplicándolo únicamente al primer término del paréntesis en lugar de a ambos.", "correcta": true}, {"texto": "Restó incorrectamente los términos semejantes antes de distribuirlos.", "correcta": false}, {"texto": "Omitió aplicar un cambio de signos a toda la inecuación.", "correcta": false}]}
{"stable_id": "MALSIGN-GEN-RECO-1", "nivel": 1, "tipo": "reconocimiento", "estilo": "multiple_choice", "enunciado": "¿En cuál de los siguientes casos se requiere utilizar la propiedad distributiva para continuar con el despeje de la variable?", "opciones": [{"texto": "$x + (3 - x) > 0$", "correcta": false}, {"texto": "$x - 2 \\ge 5x + 1$", "correcta": false}, {"texto": "$\\frac{x}{2} < 4$", "correcta": false}, {"texto": "$4(2x - 1) \\le 8x$", "correcta": true}]}
{"stable_id": "MALSIGN-GEN-PROC-1", "nivel": 2, "tipo": "procedimiento_basico", "estilo": "true_false", "enunciado": "Para resolver $5 - (2x + 1) < x$, el desarrollo correcto del lado izquierdo de la inecuación lleva a la expresión $4 - 2x < x$.", "opciones": [{"texto": "Verdadero", "correcta": true}, {"texto": "Falso", "correcta": false}]}
{"stable_id": "MALSIGN-GEN-PROC-2", "nivel": 2, "tipo": "procedimiento_basico", "estilo": "true_false", "enunciado": "Al resolver $3(x - 2) > 3x - 6$, se concluye que el conjunto solución abarca a todos los números reales, pues se obtiene una desigualdad estrictamente verdadera.", "opciones": [{"texto": "Verdadero", "correcta": false}, {"texto": "Falso", "correcta": true}]}
{"stable_id": "MALSIGN-GEN-PROC-3", "nivel": 2, "tipo": "procedimiento_basico", "estilo": "true_false", "enunciado": "La solución a la inecuación $2(x+3) \\le -2(x-3)$ es el intervalo $(-\\infty, 0]$.", "opciones": [{"texto": "Verdadero", "correcta": true}, {"texto": "Falso", "correcta": false}]}
{"stable_id": "MALSIGN-GEN-PAES-1", "nivel": 3, "tipo": "tipo_paes", "estilo": "multiple_choice", "paes_style": true, "enunciado": "Si se resuelve la inecuación lineal $4(x - 1) - 2(x + 2) < 2x - 8$, ¿qué se puede concluir respecto a sus soluciones?", "opciones": [{"texto": "No existe ningún valor real para $x$ que cumpla la desigualdad, por lo que la solución es el conjunto vacío.", "correcta": true}, {"texto": "El conjunto solución corresponde a todos los números reales.", "correcta": false}, {"texto": "La solución se describe mediante el intervalo $(-8, \\infty)$.", "correcta": false}, {"texto": "El único valor que la satisface es $x=0$.", "correcta": false}]}
{"stable_id": "MALSIGN-GEN-PAES-2", "nivel": 3, "tipo": "tipo_paes", "estilo": "multiple_choice", "paes_style": true, "enunciado": "Se tiene la inecuación $-(3x - 2) + 5(x + 1) \\ge 3$. ¿Cuál es el conjunto que representa todas sus posibles soluciones?", "opciones": [{"texto": "$[2, \\infty)$", "correcta": false}, {"texto": "$[-2, \\infty)$", "correcta": true}, {"texto": "$(2, \\infty)$", "correcta": false}, {"texto": "$(-\\infty, -2]$", "correcta": false}]}
{"stable_id": "MALSIGN-GEN-PAES-3", "nivel": 3, "tipo": "tipo_paes", "estilo": "multiple_choice", "paes_style": true, "enunciado": "Un fabricante estima que el costo de producir $x$ unidades se rige por $C(x) = 15(x+10)$, mientras que sus ingresos están dados por $I(x) = 20(x-5)$. ¿Cuál es la menor cantidad entera de unidades que debe vender para asegurar que los ingresos superen estrictamente a los costos?", "opciones": [{"texto": "$49$", "correcta": false}, {"texto": "$50$", "correcta": false}, {"texto": "$51$", "correcta": true}, {"texto": "$55$", "correcta": false}]}
"""
    },
    "MAT.ALG.SISTEMAS_INECUACIONES.TRADUCCION_INTERVALO": {
        "yaml": r"""semantic_id: MAT.ALG.SISTEMAS_INECUACIONES.TRADUCCION_INTERVALO
titulo: Traducción de Soluciones a Notación de Intervalos
objetivo: Traducir los conjuntos solución de sistemas de inecuaciones desde notaciones de desigualdad hacia notación de intervalos y representaciones gráficas en la recta real.
introduccion: Una vez que se resuelven las inecuaciones de un sistema, la solución es el conjunto de todos los valores que cumplen simultáneamente todas las condiciones. La notación de intervalos es una herramienta estandarizada que permite comunicar estas soluciones con precisión y sin ambigüedades.
resumen: La solución de un sistema de inecuaciones lineales representa la intersección de las soluciones individuales. Esta intersección puede expresarse mediante conjuntos explícitos, gráficamente en una recta numérica o, de forma más estructurada, utilizando la notación de intervalos.
explicacion: |
  ### Definición formal
  La notación de intervalos es un sistema sintáctico empleado para describir subconjuntos conexos de la recta real $\mathbb{R}$. Un intervalo definido por desigualdades del tipo $a < x < b$ corresponde al intervalo abierto $(a, b)$, mientras que $a \le x \le b$ corresponde al intervalo cerrado $[a, b]$. Si las condiciones provienen de un sistema de inecuaciones, el conjunto solución $S$ es la intersección de los intervalos que resuelven cada inecuación, es decir, $S = I_1 \cap I_2 \cap \dots \cap I_n$.

  ### Desarrollo didáctico
  Tras resolver cada inecuación de un sistema, obtenemos desigualdades separadas, por ejemplo, $x > 2$ y $x \le 5$. El desafío consiste en unificar ambas condiciones en un solo conjunto. Resulta muy útil representar las desigualdades en una recta numérica, trazando las regiones válidas para cada una de ellas y buscando dónde se superponen. Las zonas de superposición determinan la intersección. Posteriormente, se traduce esta región a la notación de intervalos. Los corchetes indican que el punto extremo está incluido, mientras que los paréntesis indican que el extremo está excluido. Si la región se extiende indefinidamente, se utiliza el símbolo de infinito, que siempre se acompaña de un paréntesis.
procedimiento:
  - "Resolver cada inecuación del sistema de forma independiente."
  - "Representar los valores obtenidos para cada inecuación en una misma recta numérica real."
  - "Identificar gráficamente la región donde se interceptan (superponen) todas las soluciones de las inecuaciones."
  - "Escribir la región interceptada utilizando la notación de intervalos, cuidando emplear paréntesis y corchetes según el tipo de desigualdad en los extremos."
ejemplos:
  - titulo: Sistema con solución acotada
    enunciado: Exprese en notación de intervalo el conjunto solución del sistema conformado por $x > -1$ y $x \le 4$.
    solucion_pasos:
      - "La primera inecuación requiere valores estrictamente mayores a $-1$, correspondiente a $(-1, \\infty)$."
      - "La segunda inecuación exige valores menores o iguales a $4$, correspondiente a $(-\\infty, 4]$."
      - "La intersección de ambos conjuntos resulta en los valores simultáneamente mayores a $-1$ y menores o iguales a $4$."
      - "La notación final es el intervalo semiabierto $(-1, 4]$."
  - titulo: Intersección con el vacío
    enunciado: Indique el intervalo solución del sistema $x < 2$ y $x > 5$.
    solucion_pasos:
      - "Se observa que los conjuntos son $(-\\infty, 2)$ y $(5, \\infty)$."
      - "Al graficar en la recta real, las áreas sombreadas no se solapan en ningún punto."
      - "En consecuencia, no hay valores que satisfagan ambas condiciones a la vez."
      - "La solución se denota como el conjunto vacío, $\\emptyset$."
  - titulo: Traducción de una desigualdad continua
    respuesta: Sí
    solucion_pasos:
      - "Dada la expresión compuesta $0 \le x < 7$, se identifica el extremo inferior como $0$ incluido y el superior como $7$ excluido."
      - "Se traduce esto como el intervalo cerrado por la izquierda y abierto por la derecha."
      - "La notación final obtenida es $[0, 7)$."
  - titulo: Un extremo al infinito
    respuesta: No
    solucion_pasos:
      - "Se recibe el sistema formado por las condiciones simultáneas $x > 3$ y $x > 8$."
      - "La intersección de $(3, \\infty)$ y $(8, \\infty)$ es el conjunto más restrictivo."
      - "El conjunto que cumple ambas es únicamente $(8, \\infty)$."
errores_frecuentes:
  - "Utilizar un corchete al indicar el infinito en un intervalo, escribiendo, por ejemplo, $[2, \\infty]$."
  - "Al unir las condiciones de $x < 3$ y $x < -1$, concluir que la solución es el intervalo $(-1, 3)$, asumiendo incorrectamente que forma un tramo cerrado."
  - "Confundir el intervalo de intersección de $x > 2$ y $x < -3$ con la unión de intervalos, dando como respuesta $(-\\infty, -3) \cup (2, \\infty)$ en lugar del conjunto vacío."
  - "Escribir los intervalos de manera desordenada, colocando el número mayor a la izquierda y el menor a la derecha, por ejemplo, $(5, 2)$."
  - "Asumir que las desigualdades estrictas se asocian a corchetes en lugar de paréntesis."
fuente: "Generado por inteligencia artificial para ProfeOnline."
estado: publicado
""",
        "jsonl": r"""{"stable_id": "MALTRADINT-GEN-CONC-1", "nivel": 1, "tipo": "conceptual", "estilo": "multiple_choice", "enunciado": "Al traducir la condición simultánea $x > a$ y $x < b$, asumiendo $a < b$, a notación de intervalos, ¿qué símbolos se utilizan en los extremos $a$ y $b$?", "opciones": [{"texto": "Un corchete en $a$ y un paréntesis en $b$.", "correcta": false}, {"texto": "Paréntesis en ambos extremos.", "correcta": true}, {"texto": "Corchetes en ambos extremos.", "correcta": false}, {"texto": "Un paréntesis en $a$ y un corchete en $b$.", "correcta": false}]}
{"stable_id": "MALTRADINT-GEN-CONC-2", "nivel": 1, "tipo": "conceptual", "estilo": "multiple_choice", "enunciado": "La notación $(-\\infty, c]$ nos indica matemáticamente que:", "opciones": [{"texto": "El conjunto contiene a todos los números menores que $c$, sin incluir a $c$.", "correcta": false}, {"texto": "El conjunto contiene a todos los números mayores o iguales a $c$.", "correcta": false}, {"texto": "El conjunto abarca todos los números reales que son menores o iguales a $c$.", "correcta": true}, {"texto": "El conjunto carece de un límite inferior y superior definido, ya que contiene al infinito.", "correcta": false}]}
{"stable_id": "MALTRADINT-GEN-CONC-3", "nivel": 1, "tipo": "conceptual", "estilo": "multiple_choice", "enunciado": "En la recta real, la intersección de dos conjuntos es vacía cuando:", "opciones": [{"texto": "Uno de los conjuntos es un intervalo abierto y el otro es cerrado.", "correcta": false}, {"texto": "Las áreas sombreadas que representan cada condición no tienen puntos en común.", "correcta": true}, {"texto": "Ambos intervalos se extienden al infinito en la misma dirección.", "correcta": false}, {"texto": "Un intervalo está contenido completamente dentro del otro.", "correcta": false}]}
{"stable_id": "MALTRADINT-GEN-RECO-1", "nivel": 1, "tipo": "reconocimiento", "estilo": "multiple_choice", "enunciado": "Seleccione el intervalo que traduce correctamente la condición compuesta: $-3 \\le x < 5$.", "opciones": [{"texto": "$(-3, 5)$", "correcta": false}, {"texto": "$[-3, 5]$", "correcta": false}, {"texto": "$[-3, 5)$", "correcta": true}, {"texto": "$(-3, 5]$", "correcta": false}]}
{"stable_id": "MALTRADINT-GEN-PROC-1", "nivel": 2, "tipo": "procedimiento_basico", "estilo": "true_false", "enunciado": "Si la solución a un sistema exige que $x > -2$ y $x \\ge 1$, el intervalo intersección resultante es $[1, \\infty)$.", "opciones": [{"texto": "Verdadero", "correcta": true}, {"texto": "Falso", "correcta": false}]}
{"stable_id": "MALTRADINT-GEN-PROC-2", "nivel": 2, "tipo": "procedimiento_basico", "estilo": "true_false", "enunciado": "Al interceptar gráficamente los intervalos $(-\\infty, 4)$ y $(4, \\infty)$, el conjunto solución resultante es la totalidad de los números reales $\\mathbb{R}$.", "opciones": [{"texto": "Verdadero", "correcta": false}, {"texto": "Falso", "correcta": true}]}
{"stable_id": "MALTRADINT-GEN-PROC-3", "nivel": 2, "tipo": "procedimiento_basico", "estilo": "true_false", "enunciado": "El sistema formado por $x < 0$ y $x \\le 5$ posee como conjunto solución al intervalo $(-\\infty, 0)$.", "opciones": [{"texto": "Verdadero", "correcta": true}, {"texto": "Falso", "correcta": false}]}
{"stable_id": "MALTRADINT-GEN-PAES-1", "nivel": 3, "tipo": "tipo_paes", "estilo": "multiple_choice", "paes_style": true, "enunciado": "Dado el sistema de inecuaciones $2x + 1 > 5$ y $3 - x \\ge -1$, la notación en intervalo de su conjunto solución es:", "opciones": [{"texto": "$(2, 4]$", "correcta": true}, {"texto": "$[2, 4)$", "correcta": false}, {"texto": "$(2, \\infty)$", "correcta": false}, {"texto": "$[4, \\infty)$", "correcta": false}]}
{"stable_id": "MALTRADINT-GEN-PAES-2", "nivel": 3, "tipo": "tipo_paes", "estilo": "multiple_choice", "paes_style": true, "enunciado": "Un biólogo estudia el rango térmico en el que sobrevive una enzima, determinando dos condiciones: $T - 10 \\le 20$ y $2T + 5 > 25$. Si $T$ está medido en grados centígrados, ¿cuál intervalo representa todas las temperaturas factibles?", "opciones": [{"texto": "$(10, 30)$", "correcta": false}, {"texto": "$[10, 30]$", "correcta": false}, {"texto": "$(10, 30]$", "correcta": true}, {"texto": "$(5, 20]$", "correcta": false}]}
{"stable_id": "MALTRADINT-GEN-PAES-3", "nivel": 3, "tipo": "tipo_paes", "estilo": "multiple_choice", "paes_style": true, "enunciado": "Las soluciones para el sistema $x + 4 > 2x - 1$ y $2x + 3 \\le x + 5$ se pueden representar gráficamente en la recta real. ¿Qué intervalo modela dicho conjunto?", "opciones": [{"texto": "$(2, 5)$", "correcta": false}, {"texto": "$(-\\infty, 2]$", "correcta": true}, {"texto": "$(-\\infty, 5]$", "correcta": false}, {"texto": "$[2, 5)$", "correcta": false}]}
"""
    }
}

if __name__ == "__main__":
    for sem_id, data in topics.items():
        with open(f"scratch/{sem_id}.yaml", "w", encoding="utf-8") as f:
            f.write(data["yaml"])
        with open(f"scratch/{sem_id}.jsonl", "w", encoding="utf-8") as f:
            f.write(data["jsonl"])
        print(f"Generated {sem_id}.yaml and jsonl")

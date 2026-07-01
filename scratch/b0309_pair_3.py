import os
import json
import yaml

topics = {
    "MAT.ALG.SISTEMAS_INECUACIONES.RESOLUCION_INDIVIDUAL": {
        "yaml": r"""
semantic_id: MAT.ALG.SISTEMAS_INECUACIONES.RESOLUCION_INDIVIDUAL
titulo: "Sistemas de inecuaciones: resolución de cada desigualdad"
objetivo: Resolver sistemas de inecuaciones lineales determinando el conjunto solución como la intersección de las soluciones individuales.
introduccion: Un sistema de inecuaciones consiste en dos o más desigualdades que deben cumplirse al mismo tiempo. Para encontrar los valores que satisfacen el sistema, resolvemos cada inecuación por separado y luego buscamos qué valores tienen en común.
resumen: La solución de un sistema de inecuaciones se encuentra resolviendo cada desigualdad individualmente y luego intersectando los conjuntos solución resultantes.
explicacion: |
  ### Definición formal
  Un sistema de inecuaciones con una incógnita $x$ es un conjunto de inecuaciones $\{I_1(x), I_2(x), \dots, I_n(x)\}$. El conjunto solución $S$ del sistema es la intersección de los conjuntos solución individuales de cada inecuación: $S = S_1 \cap S_2 \cap \dots \cap S_n$. Si la intersección es el conjunto vacío, el sistema no tiene solución.

  ### Desarrollo didáctico
  Resolver un sistema de inecuaciones es como buscar a una persona que debe cumplir varias condiciones a la vez. Por ejemplo, debe tener más de 18 años y menos de 25. Primero determinamos quiénes cumplen la primera condición, luego quiénes cumplen la segunda, y finalmente cruzamos la información para ver quiénes cumplen ambas. En matemáticas, calculamos el intervalo solución de cada inecuación de forma independiente. Una vez que tenemos los intervalos, los graficamos en la misma recta numérica. La zona donde todas las soluciones se superponen (se intersectan) es el resultado final del sistema.
procedimiento:
  - Resolver la primera inecuación de forma independiente aplicando las propiedades de las desigualdades, obteniendo su conjunto solución.
  - Resolver la segunda inecuación de manera similar para obtener su propio conjunto solución.
  - Representar ambas soluciones en una misma recta numérica para visualizar fácilmente los valores compartidos.
  - Determinar la intersección de los conjuntos, que corresponde a la solución final del sistema.
ejemplos:
  - titulo: Sistema con intersección en un intervalo
    enunciado: Resuelve el sistema formado por las inecuaciones $2x - 4 < 0$ y $x + 1 \geq 0$.
    solucion_pasos:
      - 'Paso 1: Resolver la primera inecuación $2x - 4 < 0$.'
      - 'Paso 2: Sumar 4 a ambos lados para obtener $2x < 4$.'
      - 'Paso 3: Dividir por 2 para obtener $x < 2$. El conjunto solución es $(-\infty, 2)$.'
      - 'Paso 4: Resolver la segunda inecuación $x + 1 \geq 0$.'
      - 'Paso 5: Restar 1 a ambos lados para obtener $x \geq -1$. El conjunto solución es $[-1, \infty)$.'
      - 'Paso 6: Intersectar las soluciones: $(-\infty, 2) \cap [-1, \infty) = [-1, 2)$.'
  - titulo: Sistema con solución hacia el infinito
    enunciado: Determina el conjunto solución del sistema $3x \geq 6$ y $5 - x < 2$.
    solucion_pasos:
      - 'Paso 1: Resolver la primera inecuación: $3x \geq 6$.'
      - 'Paso 2: Dividir entre 3 para obtener $x \geq 2$. El conjunto solución es $[2, \infty)$.'
      - 'Paso 3: Resolver la segunda inecuación: $5 - x < 2$.'
      - 'Paso 4: Restar 5 a ambos lados obteniendo $-x < -3$.'
      - 'Paso 5: Multiplicar por $-1$, invirtiendo la desigualdad: $x > 3$. El conjunto es $(3, \infty)$.'
      - 'Paso 6: Intersectar ambas soluciones: $[2, \infty) \cap (3, \infty) = (3, \infty)$.'
  - titulo: Verificación de un valor en el sistema
    respuesta: Sí
    solucion_pasos:
      - 'Para que $x = 3$ sea solución, debe cumplir ambas inecuaciones.'
      - 'Verificamos en la primera inecuación $x > 2$: el valor $3 > 2$ es verdadero.'
      - 'Verificamos en la segunda inecuación $2x \leq 6$: calculamos $2(3) = 6 \leq 6$, lo cual es verdadero.'
      - 'Como cumple ambas desigualdades simultáneamente, sí es solución.'
  - titulo: ¿Tiene solución el sistema formado por $x > 5$ y $x < 2$?
    respuesta: No
    solucion_pasos:
      - 'La primera inecuación indica que $x$ pertenece al intervalo $(5, \infty)$.'
      - 'La segunda inecuación indica que $x$ pertenece al intervalo $(-\infty, 2)$.'
      - 'Al graficar en la recta, observamos que los intervalos no se cruzan en ningún punto.'
      - 'La intersección es vacía, por lo tanto, el sistema no tiene solución.'
errores_frecuentes:
  - Creer que la solución del sistema se obtiene sumando o restando las inecuaciones como si fuera un sistema de ecuaciones.
  - Considerar que la solución final es la unión de los conjuntos, en lugar de su intersección.
  - Olvidar invertir el signo de la desigualdad en una de las inecuaciones al dividir por un negativo, afectando toda la intersección final.
  - Concluir que si la primera inecuación incluye al extremo, la intersección siempre incluirá ese mismo extremo sin importar la segunda inecuación.
  - Asumir que si una inecuación da como solución todos los números reales, el sistema no tiene solución.
fuente: Elaboración propia
estado: publicado
""",
        "jsonl": r"""{"stable_id": "ALG-GEN-SISIN-1", "tipo": "conceptual", "nivel": 1, "enunciado": "En un sistema de dos inecuaciones lineales, ¿cómo se determina matemáticamente el conjunto solución final a partir de las soluciones individuales?", "opciones": [{"texto": "Se determina calculando la intersección de los conjuntos solución de cada inecuación.", "correcta": true}, {"texto": "Se determina calculando la unión de los conjuntos solución de cada inecuación.", "correcta": false}, {"texto": "Se determina sumando los límites superiores e inferiores de ambos conjuntos solución.", "correcta": false}, {"texto": "Se determina eligiendo el conjunto solución que contenga únicamente números positivos.", "correcta": false}]}
{"stable_id": "ALG-GEN-SISIN-2", "tipo": "conceptual", "nivel": 1, "enunciado": "Si al resolver de forma independiente las dos inecuaciones de un sistema se obtienen conjuntos solución disjuntos (que no se cruzan), ¿qué se puede afirmar sobre el sistema?", "opciones": [{"texto": "El sistema no tiene solución (su conjunto solución es el vacío).", "correcta": true}, {"texto": "La solución del sistema son todos los números reales.", "correcta": false}, {"texto": "La solución es simplemente el conjunto más grande.", "correcta": false}, {"texto": "Existe un error, ya que todos los sistemas de inecuaciones deben tener solución.", "correcta": false}]}
{"stable_id": "ALG-GEN-SISIN-3", "tipo": "conceptual", "nivel": 1, "enunciado": "¿Qué condición es necesaria para que un número específico pertenezca a la solución de un sistema de tres inecuaciones?", "opciones": [{"texto": "El número debe satisfacer simultáneamente las tres inecuaciones.", "correcta": true}, {"texto": "El número debe satisfacer al menos una de las tres inecuaciones.", "correcta": false}, {"texto": "El número debe satisfacer exactamente dos de las inecuaciones.", "correcta": false}, {"texto": "El número debe anular (hacer cero) todas las inecuaciones.", "correcta": false}]}
{"stable_id": "ALG-GEN-SISIN-4", "tipo": "reconocimiento", "nivel": 1, "enunciado": "Identifica cuál de las siguientes opciones representa el conjunto solución del sistema formado por $x > 0$ y $x < 4$.", "opciones": [{"texto": "$(0, 4)$", "correcta": true}, {"texto": "$[0, 4]$", "correcta": false}, {"texto": "$(-\\infty, 4)$", "correcta": false}, {"texto": "$(0, \\infty)$", "correcta": false}]}
{"stable_id": "ALG-GEN-SISIN-5", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "Para resolver el sistema formado por $x - 1 > 0$ y $2x < 10$, el primer paso es sumar 1 y dividir por 2 simultáneamente en ambas inecuaciones para luego unirlas.", "opciones": [{"texto": "Verdadero", "correcta": false}, {"texto": "Falso", "correcta": true}]}
{"stable_id": "ALG-GEN-SISIN-6", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "El sistema de inecuaciones $x \\geq 3$ y $x \\leq 3$ tiene como única solución el valor $x = 3$.", "opciones": [{"texto": "Verdadero", "correcta": true}, {"texto": "Falso", "correcta": false}]}
{"stable_id": "ALG-GEN-SISIN-7", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "Si la solución de la primera inecuación es $(-\\infty, 5]$ y de la segunda es $(2, \\infty)$, entonces la intersección de ambas es el intervalo $(2, 5]$.", "opciones": [{"texto": "Verdadero", "correcta": true}, {"texto": "Falso", "correcta": false}]}
{"stable_id": "ALG-GEN-SISIN-8", "tipo": "tipo_paes", "nivel": 3, "paes_style": true, "enunciado": "Considera el sistema de inecuaciones dado por: $3x - 2 \\leq x + 6$ y $2x + 1 > 5$. ¿Cuál es el conjunto solución del sistema?", "opciones": [{"texto": "$(2, 4]$", "correcta": true}, {"texto": "$[2, 4]$", "correcta": false}, {"texto": "$(2, 4)$", "correcta": false}, {"texto": "$(2, \\infty)$", "correcta": false}]}
{"stable_id": "ALG-GEN-SISIN-9", "tipo": "tipo_paes", "nivel": 3, "paes_style": true, "enunciado": "Para que un ascensor funcione con normalidad, el peso $P$ total de las personas (en kg) debe cumplir el sistema: $P \\geq 150$ y $P + 50 < 450$. ¿Cuál es el intervalo de pesos permitidos?", "opciones": [{"texto": "$[150, 400)$", "correcta": true}, {"texto": "$(150, 400)$", "correcta": false}, {"texto": "$[150, 450]$", "correcta": false}, {"texto": "$(150, 500]$", "correcta": false}]}
{"stable_id": "ALG-GEN-SISIN-10", "tipo": "tipo_paes", "nivel": 3, "paes_style": true, "enunciado": "Dado el sistema de inecuaciones $1 - x \\leq 3$ y $4x - 1 < 7$, ¿cuántos números enteros satisfacen ambas inecuaciones simultáneamente?", "opciones": [{"texto": "4", "correcta": true}, {"texto": "3", "correcta": false}, {"texto": "5", "correcta": false}, {"texto": "Infinitos", "correcta": false}]}"""
    },
    "MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.MENOR_QUE_POSITIVO": {
        "yaml": r"""
semantic_id: MAT.ALG.INECUACIONES_VALOR_ABSOLUTO.MENOR_QUE_POSITIVO
titulo: "Inecuaciones con valor absoluto: menor que un número positivo"
objetivo: Resolver inecuaciones con valor absoluto de la forma menor que un número positivo aplicando la propiedad de acotación.
introduccion: Cuando decimos que el valor absoluto de una cantidad es menor que un número positivo, significa que la distancia de esa cantidad al origen es más pequeña que ese número. Esto se traduce en que la cantidad original debe estar "atrapada" entre el valor negativo y el valor positivo del número.
resumen: La inecuación $|x| < a$ con $a > 0$ se resuelve transformándola en la doble desigualdad simultánea $-a < x < a$.
explicacion: |
  ### Definición formal
  Para cualquier expresión algebraica $u$ y cualquier número real constante $a > 0$, la inecuación de valor absoluto $|u| < a$ es lógicamente equivalente a la doble inecuación $-a < u < a$. Del mismo modo, si la inecuación incluye la igualdad, $|u| \leq a$ es equivalente a $-a \leq u \leq a$.

  ### Desarrollo didáctico
  Imagina que estás en el centro de una plaza (posición cero) y te dicen que debes mantenerte a una distancia menor a 5 metros de este centro. Eso significa que no puedes alejarte 5 metros hacia la derecha (valores positivos) ni 5 metros hacia la izquierda (valores negativos). Debes permanecer en la franja que va desde $-5$ hasta $5$. En términos algebraicos, esto explica por qué si $|x| < 5$, entonces obligatoriamente $-5 < x < 5$. Cuando hay una expresión más compleja dentro de las barras, como $|2x - 1| < 5$, aplicamos el mismo principio para atrapar al bloque entero $-5 < 2x - 1 < 5$, y a partir de ahí despejamos la variable.
procedimiento:
  - Identificar que la inecuación tiene la forma $|u| < a$ o $|u| \leq a$, confirmando primero que $a$ es un número estrictamente mayor que cero.
  - Reescribir la inecuación eliminando las barras de valor absoluto y formandouna doble desigualdad: $-a < u < a$ (o $-a \leq u \leq a$).
  - Despejar la variable incógnita en la parte central de la desigualdad. Toda operación (suma, resta, multiplicación o división) debe aplicarse a los tres lados simultáneamente.
  - Expresar el resultado final en notación de intervalo.
ejemplos:
  - titulo: Resolución de una inecuación básica
    enunciado: Resuelve la inecuación $|x - 2| < 5$.
    solucion_pasos:
      - 'Paso 1: Identificamos la forma $|u| < a$ con $u = x - 2$ y $a = 5$.'
      - 'Paso 2: Transformamos en doble desigualdad: $-5 < x - 2 < 5$.'
      - 'Paso 3: Para despejar $x$, sumamos 2 en las tres partes de la inecuación.'
      - 'Paso 4: Obtenemos $-5 + 2 < x < 5 + 2$, lo que da $-3 < x < 7$.'
      - 'Paso 5: La solución en forma de intervalo es $(-3, 7)$.'
  - titulo: Inecuación con coeficiente que acompaña la incógnita
    enunciado: Resuelve la inecuación $|2x + 1| \leq 7$.
    solucion_pasos:
      - 'Paso 1: Identificamos que aplica la propiedad con $a=7$ positivo: $-7 \leq 2x + 1 \leq 7$.'
      - 'Paso 2: Restamos 1 en las tres partes: $-7 - 1 \leq 2x \leq 7 - 1$.'
      - 'Paso 3: Simplificamos obteniendo $-8 \leq 2x \leq 6$.'
      - 'Paso 4: Dividimos todas las partes por 2, obteniendo $-4 \leq x \leq 3$.'
      - 'Paso 5: La solución en forma de intervalo es $[-4, 3]$.'
  - titulo: ¿Es un valor específico solución de la inecuación?
    respuesta: Sí
    solucion_pasos:
      - 'Para saber si $x=0$ es solución de $|x| < 3$, sustituimos la variable por el valor.'
      - 'Calculamos $|0|$.'
      - 'El valor absoluto de 0 es 0.'
      - 'Comparamos con la inecuación original: $0 < 3$ es una proposición verdadera, por lo tanto sí es solución.'
  - titulo: ¿Se puede aplicar la propiedad $-a < x < a$ para resolver $|x| < -4$?
    respuesta: No
    solucion_pasos:
      - 'La propiedad exige que el número al otro lado de la desigualdad sea positivo ($a > 0$).'
      - 'En este caso, se pide que un valor absoluto, que por definición es siempre mayor o igual a 0, sea estrictamente menor que un número negativo ($-4$).'
      - 'Esto es matemáticamente imposible.'
      - 'No se aplica la propiedad; la inecuación directamente no tiene solución real (conjunto vacío).'
errores_frecuentes:
  - Separar la inecuación $|x| < a$ en dos inecuaciones aisladas sin unirlas correctamente en una doble desigualdad, asumiendo $x < a$ o $x < -a$.
  - Olvidar que la constante $a$ debe ser positiva antes de aplicar la regla de transformación a doble desigualdad.
  - Resolver la inecuación ignorando completamente las barras de valor absoluto, como si solo fuera $x < a$.
  - Despejar erróneamente en la doble desigualdad operando solo en el lado derecho y dejando intacto el lado izquierdo.
  - Creer que la solución de $|x| < a$ son dos intervalos disjuntos que se alejan del origen en lugar de un único intervalo central continuo.
fuente: Elaboración propia
estado: publicado
""",
        "jsonl": r"""{"stable_id": "ALG-GEN-ABSME-1", "tipo": "conceptual", "nivel": 1, "enunciado": "¿Qué propiedad es fundamental para resolver inecuaciones de la forma $|x| < a$ cuando $a$ es un número positivo?", "opciones": [{"texto": "La inecuación se reescribe como la doble desigualdad $-a < x < a$.", "correcta": true}, {"texto": "La inecuación se reescribe como $x > a$ o $x < -a$.", "correcta": false}, {"texto": "La inecuación se resuelve elevando al cuadrado y descartando los valores negativos.", "correcta": false}, {"texto": "La inecuación solo tiene solución si $x$ es un número positivo.", "correcta": false}]}
{"stable_id": "ALG-GEN-ABSME-2", "tipo": "conceptual", "nivel": 1, "enunciado": "Al traducir la expresión matemática \"la distancia desde el número real $x$ hasta el origen es menor que $p$\" (con $p > 0$), ¿qué inecuación representa correctamente esta situación?", "opciones": [{"texto": "$|x| < p$", "correcta": true}, {"texto": "$|x| > p$", "correcta": false}, {"texto": "$x < |p|$", "correcta": false}, {"texto": "$|x| = p$", "correcta": false}]}
{"stable_id": "ALG-GEN-ABSME-3", "tipo": "conceptual", "nivel": 1, "enunciado": "En la resolución de $|2x - 3| < 5$, el uso de la doble desigualdad $-5 < 2x - 3 < 5$ asegura que:", "opciones": [{"texto": "La expresión $2x - 3$ esté simultáneamente por encima de $-5$ y por debajo de $5$.", "correcta": true}, {"texto": "La expresión $2x - 3$ tome únicamente valores positivos.", "correcta": false}, {"texto": "El resultado final consista de dos intervalos disjuntos.", "correcta": false}, {"texto": "Se elimine el signo negativo del $-5$ durante el despeje.", "correcta": false}]}
{"stable_id": "ALG-GEN-ABSME-4", "tipo": "reconocimiento", "nivel": 1, "enunciado": "Identifica cuál de las siguientes expresiones es lógicamente equivalente a $|x| \\leq 8$.", "opciones": [{"texto": "$-8 \\leq x \\leq 8$", "correcta": true}, {"texto": "$x \\leq 8$ y $x \\geq 8$", "correcta": false}, {"texto": "$x \\leq -8$ o $x \\geq 8$", "correcta": false}, {"texto": "$-8 < x < 8$", "correcta": false}]}
{"stable_id": "ALG-GEN-ABSME-5", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "Para resolver $|x + 4| < 6$, se debe transformar la inecuación a $-6 < x + 4 < 6$ y luego restar 4 en todas las partes.", "opciones": [{"texto": "Verdadero", "correcta": true}, {"texto": "Falso", "correcta": false}]}
{"stable_id": "ALG-GEN-ABSME-6", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "La solución a la inecuación $|3x| < 9$ es el intervalo $(-3, 3)$.", "opciones": [{"texto": "Verdadero", "correcta": true}, {"texto": "Falso", "correcta": false}]}
{"stable_id": "ALG-GEN-ABSME-7", "tipo": "procedimiento_basico", "nivel": 2, "enunciado": "Si resolvemos $|x - 5| < 2$, obtenemos como solución el conjunto $(-\\infty, 3) \\cup (7, \\infty)$.", "opciones": [{"texto": "Verdadero", "correcta": false}, {"texto": "Falso", "correcta": true}]}
{"stable_id": "ALG-GEN-ABSME-8", "tipo": "tipo_paes", "nivel": 3, "paes_style": true, "enunciado": "Un termómetro debe mantenerse a una temperatura óptima $T$ (en °C) que no varíe en más de 2 grados de una temperatura de referencia de 20°C, sin incluir los extremos. ¿Qué inecuación con valor absoluto y cuál es su solución para esta situación?", "opciones": [{"texto": "$|T - 20| < 2$, cuya solución es $(18, 22)$", "correcta": true}, {"texto": "$|T + 20| < 2$, cuya solución es $(-22, -18)$", "correcta": false}, {"texto": "$|T - 20| > 2$, cuya solución es $(-\\infty, 18) \\cup (22, \\infty)$", "correcta": false}, {"texto": "$|T - 2| < 20$, cuya solución es $(-18, 22)$", "correcta": false}]}
{"stable_id": "ALG-GEN-ABSME-9", "tipo": "tipo_paes", "nivel": 3, "paes_style": true, "enunciado": "¿Cuál es la suma de los valores enteros que pertenecen al conjunto solución de la inecuación $|3x - 1| \\leq 5$?", "opciones": [{"texto": "0", "correcta": true}, {"texto": "3", "correcta": false}, {"texto": "1", "correcta": false}, {"texto": "-1", "correcta": false}]}
{"stable_id": "ALG-GEN-ABSME-10", "tipo": "tipo_paes", "nivel": 3, "paes_style": true, "enunciado": "Dada la inecuación $|\\frac{x}{2} + 3| < 1$, ¿cuál de los siguientes intervalos corresponde al conjunto solución?", "opciones": [{"texto": "$(-8, -4)$", "correcta": true}, {"texto": "$(-4, -2)$", "correcta": false}, {"texto": "$(-8, 4)$", "correcta": false}, {"texto": "$(-2, 2)$", "correcta": false}]}"""
    }
}

if __name__ == "__main__":
    print("Script ran successfully. Length of topics:", len(topics))
    for k in topics:
        yaml.safe_load(topics[k]['yaml'])
        lines = topics[k]['jsonl'].strip().split('\n')
        assert len(lines) == 10, f"Expected 10 lines for {k}"
        for line in lines:
            json.loads(line)
    print("YAML and JSONL formats are valid.")

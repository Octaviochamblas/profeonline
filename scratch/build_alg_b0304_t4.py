import os
import json

# Tanda 4
# MAT.ALG.MULT_MON_POL.MONOMIO_NEGATIVO
# MAT.ALG.MULT_POLINOMIOS.COEFICIENTES_FRACCIONARIOS
# MAT.ALG.MULT_MONOMIOS.GRADO_PRODUCTO
# MAT.ALG.MULT_MON_POL.DISTRIBUCION_PARCIAL_ERROR

YAMLS = {
    "mat-alg-mult-mon-pol-monomio-negativo.yaml": """semantic_id: "MAT.ALG.MULT_MON_POL.MONOMIO_NEGATIVO"
title: "Multiplicación de un monomio negativo por un polinomio"
objetivo: "Multiplicar un monomio con coeficiente negativo por un polinomio, distribuyendo y aplicando correctamente la ley de los signos."
introduccion: "Cuando el monomio que multiplica al polinomio es negativo, no solo cambian los números y las letras, ¡también cambian todos los signos del polinomio! Es como si el signo menos se 'repartiera' a cada término."
resumen: |
  Para multiplicar un monomio negativo por un polinomio:

  - Se multiplica el monomio por cada término del polinomio (propiedad distributiva).
  - Se aplica la regla de los signos en cada multiplicación ($-$ por $+$ es $-$; $-$ por $-$ es $+$).
  - Se multiplican los coeficientes numéricos y se suman los exponentes de las bases iguales.
explicacion: |
  La multiplicación de un monomio negativo por un polinomio sigue el mismo principio de la propiedad distributiva, con una atención especial a los signos.

  Si tenemos $-a(b - c)$, el monomio negativo $-a$ se distribuye:
  $(-a) \\cdot b + (-a) \\cdot (-c)$

  Aplicando la ley de los signos, obtenemos:
  $-ab + ac$

  Es fundamental recordar que multiplicar por un negativo invierte todos los signos originales de los términos dentro del paréntesis.
procedimiento: |
  1. Identifica el monomio negativo y los términos del polinomio.
  2. Multiplica el monomio por el primer término del polinomio, aplicando la regla de signos.
  3. Repite el proceso para cada uno de los términos restantes del polinomio.
  4. Simplifica escribiendo la suma algebraica resultante.
ejemplos:
  - title: "Multiplicación básica"
    text: "Resuelve $-3x(2x + 4)$"
    steps:
      - "Distribuye el $-3x$ a cada término: $(-3x)(2x) + (-3x)(4)$"
      - "Multiplica los coeficientes y suma los exponentes: $-6x^2 - 12x$"
  - title: "Cambio de signos múltiples"
    text: "Desarrolla $-2a^2(3a^2 - 5a + 1)$"
    steps:
      - "Distribuye: $(-2a^2)(3a^2) + (-2a^2)(-5a) + (-2a^2)(1)$"
      - "Multiplica término a término: $-6a^4 + 10a^3 - 2a^2$"
  - title: "Con dos variables"
    text: "Multiplica $-4xy(x^2 - xy + y^2)$"
    steps:
      - "Distribuye: $(-4xy)(x^2) + (-4xy)(-xy) + (-4xy)(y^2)$"
      - "Calcula: $-4x^3y + 4x^2y^2 - 4xy^3$"
  - title: "Verdadero o Falso: Signos"
    text: "Al multiplicar $-x(y - z)$, el resultado es $-xy - xz$."
    steps:
      - "La distribución es $(-x)(y) + (-x)(-z)$"
      - "El resultado correcto es $-xy + xz$."
      - "Por lo tanto, la afirmación es Falsa."
errores_frecuentes:
  - "Olvidar cambiar el signo del segundo o tercer término del polinomio."
  - "Sumar en lugar de multiplicar los coeficientes numéricos."
  - "Cambiar el signo pero olvidar multiplicar las partes literales."
""",
    "mat-alg-mult-polinomios-coeficientes-fraccionarios.yaml": """semantic_id: "MAT.ALG.MULT_POLINOMIOS.COEFICIENTES_FRACCIONARIOS"
title: "Multiplicación de polinomios con coeficientes fraccionarios"
objetivo: "Multiplicar dos polinomios donde los coeficientes son fracciones, aplicando correctamente la distributividad y las reglas de las fracciones."
introduccion: "Multiplicar polinomios con fracciones es igual que con números enteros, solo que ahora debemos recordar cómo multiplicar fracciones: el numerador por el numerador y el denominador por el denominador."
resumen: |
  Al multiplicar polinomios con coeficientes fraccionarios, se aplica la propiedad distributiva multiplicando cada término del primer polinomio por cada término del segundo.

  Para cada multiplicación de términos:
  - Multiplica los coeficientes (numerador con numerador, denominador con denominador).
  - Suma los exponentes de las letras iguales.
  - Al final, reduce términos semejantes, lo cual puede requerir encontrar un denominador común.
explicacion: |
  La regla general para multiplicar dos polinomios $P(x)$ y $Q(x)$ se mantiene: cada término de $P(x)$ se multiplica por cada término de $Q(x)$.

  Cuando los coeficientes son fracciones, como $\\frac{a}{b}$ y $\\frac{c}{d}$, el coeficiente del término resultante será $\\frac{a \\cdot c}{b \\cdot d}$.

  Después de distribuir todos los términos, es probable que se generen términos semejantes con coeficientes fraccionarios. Para reducirlos, debes sumar o restar esas fracciones encontrando el mínimo común múltiplo (MCM) de sus denominadores.
procedimiento: |
  1. Multiplica cada término del primer polinomio por cada término del segundo.
  2. En cada producto, multiplica los numeradores entre sí y los denominadores entre sí.
  3. Suma los exponentes de las variables iguales.
  4. Agrupa los términos semejantes resultantes.
  5. Suma o resta las fracciones de los términos semejantes usando el MCM.
  6. Simplifica las fracciones resultantes, si es posible.
ejemplos:
  - title: "Binomio por binomio"
    text: "Multiplica $(\\frac{1}{2}x + 1)(\\frac{1}{3}x - 2)$"
    steps:
      - "Distribuye: $(\\frac{1}{2}x)(\\frac{1}{3}x) + (\\frac{1}{2}x)(-2) + (1)(\\frac{1}{3}x) + (1)(-2)$"
      - "Calcula: $\\frac{1}{6}x^2 - 1x + \\frac{1}{3}x - 2$"
      - "Reduce términos semejantes ($-1 + \\frac{1}{3} = -\\frac{2}{3}$): $\\frac{1}{6}x^2 - \\frac{2}{3}x - 2$"
  - title: "Con fracciones en ambos términos"
    text: "Calcula $(\\frac{2}{5}a - \\frac{1}{2})(\\frac{5}{2}a + \\frac{1}{4})$"
    steps:
      - "Distribuye: $(\\frac{2}{5}a)(\\frac{5}{2}a) + (\\frac{2}{5}a)(\\frac{1}{4}) - (\\frac{1}{2})(\\frac{5}{2}a) - (\\frac{1}{2})(\\frac{1}{4})$"
      - "Multiplica: $1a^2 + \\frac{2}{20}a - \\frac{5}{4}a - \\frac{1}{8}$"
      - "Simplifica $\\frac{2}{20}$ a $\\frac{1}{10}$ y suma con $-\\frac{5}{4}$ ($MCM=20$): $\\frac{2}{20} - \\frac{25}{20} = -\\frac{23}{20}$"
      - "Resultado final: $a^2 - \\frac{23}{20}a - \\frac{1}{8}$"
  - title: "Verdadero o Falso: Simplificación"
    text: "El término cuadrático del producto $(\\frac{3}{4}x + 1)(\\frac{2}{3}x - 5)$ tiene coeficiente $\\frac{1}{2}$."
    steps:
      - "El término cuadrático se forma multiplicando $(\\frac{3}{4}x)(\\frac{2}{3}x)$."
      - "$\\frac{3 \\cdot 2}{4 \\cdot 3} = \\frac{6}{12} = \\frac{1}{2}$."
      - "Por lo tanto, la afirmación es Verdadera."
errores_frecuentes:
  - "Multiplicar cruzado los coeficientes en lugar de directo (numerador con numerador)."
  - "Olvidar buscar denominador común al reducir los términos semejantes finales."
  - "Equivocarse en la ley de los signos al multiplicar fracciones negativas."
""",
    "mat-alg-mult-monomios-grado-producto.yaml": """semantic_id: "MAT.ALG.MULT_MONOMIOS.GRADO_PRODUCTO"
title: "Grado del producto de monomios"
objetivo: "Determinar el grado absoluto y relativo del resultado de multiplicar dos o más monomios, comprendiendo que el grado final es la suma de los grados de los factores."
introduccion: "Cuando multiplicas dos monomios, el 'tamaño' algebraico (su grado) aumenta. Si multiplicas algo de grado 2 por algo de grado 3, el resultado es de grado 5. ¡Los grados siempre se suman!"
resumen: |
  El grado de un monomio es la suma de los exponentes de sus letras (grado absoluto) o el exponente de una letra específica (grado relativo).

  Al multiplicar monomios:
  - El grado absoluto del producto es igual a la suma de los grados absolutos de los factores.
  - El grado relativo (respecto a una variable) del producto es igual a la suma de los grados relativos de esa variable en los factores.
explicacion: |
  La propiedad del grado en la multiplicación se deriva directamente de la regla de los exponentes: $x^a \\cdot x^b = x^{a+b}$.

  Si tienes un monomio $M_1$ de grado absoluto $m$ y un monomio $M_2$ de grado absoluto $n$, el producto $M_1 \\cdot M_2$ tendrá grado absoluto $m + n$.

  Por ejemplo, si $M_1 = 3x^2y^3$ (grado $2+3=5$) y $M_2 = -2x^4y$ (grado $4+1=5$), el producto es $-6x^6y^4$. Su grado absoluto es $6+4=10$, que es exactamente $5 + 5$.
procedimiento: |
  Para hallar el grado absoluto del producto sin calcularlo completamente:
  1. Encuentra el grado absoluto del primer factor (suma sus exponentes).
  2. Encuentra el grado absoluto del segundo factor.
  3. Suma ambos grados obtenidos.

  Para hallar el grado absoluto del producto calculado:
  1. Multiplica los monomios normalmente.
  2. Suma todos los exponentes de las letras en el resultado final.
ejemplos:
  - title: "Cálculo a partir de los factores"
    text: "Encuentra el grado del producto de $5x^3y^2$ y $7x^4y^5$."
    steps:
      - "El grado del primer factor es $3 + 2 = 5$."
      - "El grado del segundo factor es $4 + 5 = 9$."
      - "El grado del producto será $5 + 9 = 14$."
  - title: "Cálculo verificando el producto"
    text: "Multiplica $-2a^2b^3c$ por $4ab^2c^4$ y determina el grado absoluto."
    steps:
      - "Producto: $-8a^{2+1}b^{3+2}c^{1+4} = -8a^3b^5c^5$."
      - "Suma los exponentes del resultado: $3 + 5 + 5 = 13$."
      - "El grado absoluto es $13$."
  - title: "Verdadero o Falso: Multiplicación de grados"
    text: "El grado absoluto del producto de dos monomios se obtiene multiplicando los grados absolutos de los factores."
    steps:
      - "Los exponentes se suman al multiplicar potencias de igual base."
      - "Por lo tanto, los grados absolutos de los monomios se suman, no se multiplican."
      - "La afirmación es Falsa."
errores_frecuentes:
  - "Multiplicar los grados de los factores en lugar de sumarlos."
  - "Olvidar que las variables sin exponente escrito tienen exponente $1$."
  - "Confundir el grado absoluto (suma de todos los exponentes) con el coeficiente del monomio."
""",
    "mat-alg-mult-mon-pol-distribucion-parcial-error.yaml": """node_id: "MAT.ALG.MULT_MON_POL.DISTRIBUCION_PARCIAL_ERROR"
title: "Error común: Distribución parcial"
objective: "Identificar y corregir el error de la distribución parcial al multiplicar un monomio por un polinomio."
introduccion: "Un error muy clásico al resolver paréntesis es repartir el número de afuera solo al primer término de adentro y olvidarse de los demás. ¡No dejes a los otros términos sin su multiplicación!"
resumen: |
  La distribución parcial es un error frecuente donde el monomio exterior solo multiplica al primer término del polinomio y se deja el resto inalterado.

  - Forma incorrecta: $a(b + c) = ab + c$
  - Forma correcta: $a(b + c) = ab + ac$

  Para evitar este error, se recomienda dibujar arcos desde el monomio exterior hacia **cada uno** de los términos del polinomio.
explicacion: |
  La propiedad distributiva establece que la multiplicación se distribuye sobre la adición y la sustracción. Esto significa que el factor externo actúa como un multiplicador universal para todo lo contenido en el paréntesis.

  Si tenemos $3x(2x + 5y - 4)$, el error de distribución parcial daría como resultado $6x^2 + 5y - 4$. El estudiante operó correctamente $3x \\cdot 2x$, pero se olvidó del $5y$ y del $-4$.

  El resultado correcto requiere realizar tres multiplicaciones separadas:
  $(3x \\cdot 2x) + (3x \\cdot 5y) + (3x \\cdot -4) = 6x^2 + 15xy - 12x$.
procedimiento: |
  Para asegurar una distribución completa:
  1. Cuenta cuántos términos tiene el polinomio dentro del paréntesis.
  2. Haz una marca (como un arco) por cada término, partiendo desde el monomio exterior.
  3. Realiza tantas multiplicaciones como arcos hayas dibujado.
  4. Verifica que el resultado final tenga el mismo número de términos que el polinomio original (antes de reducir términos semejantes, si los hay).
ejemplos:
  - title: "Identificación del error"
    text: "Identifica el error en este cálculo: $-4(2a - 3b + 1) = -8a - 3b + 1$"
    steps:
      - "El estudiante solo multiplicó el $-4$ por el primer término $2a$."
      - "Olvidó multiplicar el $-4$ por el $-3b$ y por el $1$."
      - "El resultado correcto debe ser: $-8a + 12b - 4$."
  - title: "Distribución completa"
    text: "Resuelve correctamente $5m(m^2 - 2m + 3)$."
    steps:
      - "Hay 3 términos en el paréntesis. Haremos 3 multiplicaciones."
      - "$(5m)(m^2) = 5m^3$"
      - "$(5m)(-2m) = -10m^2$"
      - "$(5m)(3) = 15m$"
      - "Resultado: $5m^3 - 10m^2 + 15m$."
  - title: "Verdadero o Falso: Cantidad de términos"
    text: "Si multiplicamos un monomio por un trinomio, el resultado siempre tendrá tres términos, asumiendo que no hay reducción posible."
    steps:
      - "Al distribuir, se hace una multiplicación por cada término del trinomio."
      - "Al ser tres multiplicaciones distintas, se generarán tres términos."
      - "Por lo tanto, la afirmación es Verdadera."
errores_frecuentes:
  - "Multiplicar únicamente el primer término y transcribir el resto igual."
  - "Distribuir correctamente los números pero olvidar distribuir la variable."
  - "Detener la distribución al encontrar un signo negativo."
"""
}

def generate_exercises():
    exercises = []

    # 1. MAT.ALG.MULT_MON_POL.MONOMIO_NEGATIVO
    nid = "MAT.ALG.MULT_MON_POL.MONOMIO_NEGATIVO"

    # Conceptuales
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "basica", "text": "Al multiplicar un polinomio por un monomio con coeficiente negativo, ¿qué ocurre con los signos de los términos del polinomio?", "options": [{"text": "Todos los signos se invierten.", "is_correct": True}, {"text": "Todos los signos quedan iguales.", "is_correct": False}, {"text": "Solo se invierte el primer signo.", "is_correct": False}, {"text": "Los signos cambian dependiendo del exponente.", "is_correct": False}], "explanation": "La multiplicación por un número negativo invierte el signo positivo a negativo, y el negativo a positivo en cada término."})
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "intermedia", "text": "Si el resultado de multiplicar un monomio por el binomio $(a - b)$ es $-3a + 3b$, ¿cuál era el monomio multiplicador?", "options": [{"text": "$-3$", "is_correct": True}, {"text": "$3$", "is_correct": False}, {"text": "$-a$", "is_correct": False}, {"text": "$-3a$", "is_correct": False}], "explanation": "Al dividir $-3a$ entre $a$ obtenemos $-3$. Al verificar, $-3(a - b) = -3a + 3b$."})
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "avanzada", "text": "¿Es posible que al multiplicar un polinomio de términos todos positivos por un monomio negativo, el resultado tenga algún término positivo?", "options": [{"text": "No, todos serán negativos.", "is_correct": True}, {"text": "Sí, el primer término.", "is_correct": False}, {"text": "Sí, dependiendo del grado.", "is_correct": False}, {"text": "Sí, si el monomio es fraccionario.", "is_correct": False}], "explanation": "Como $(-)\\cdot(+) = (-)$, si todos los términos originales eran positivos y el multiplicador es negativo, todos los resultados parciales serán obligatoriamente negativos."})
    # Reconocimiento
    exercises.append({"node_id": nid, "kind": "reconocimiento", "difficulty": "basica", "text": "Selecciona la expresión equivalente a $-x(x + 1)$.", "options": [{"text": "$-x^2 - x$", "is_correct": True}, {"text": "$-x^2 + 1$", "is_correct": False}, {"text": "$x^2 - x$", "is_correct": False}, {"text": "$-2x^2$", "is_correct": False}], "explanation": "$-x \\cdot x = -x^2$ y $-x \\cdot 1 = -x$. Sumando: $-x^2 - x$."})
    # Procedimiento
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "basica", "text": "Calcula el producto: $-2a(3a - 5)$.", "options": [{"text": "$-6a^2 + 10a$", "is_correct": True}, {"text": "$-6a^2 - 10a$", "is_correct": False}, {"text": "$6a^2 - 10a$", "is_correct": False}, {"text": "$-6a^2 - 5$", "is_correct": False}], "explanation": "$-2a \\cdot 3a = -6a^2$. $-2a \\cdot (-5) = +10a$."})
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "intermedia", "text": "Desarrolla la multiplicación: $-4x^2y(x^2 - xy + y^2)$.", "options": [{"text": "$-4x^4y + 4x^3y^2 - 4x^2y^3$", "is_correct": True}, {"text": "$-4x^4y - 4x^3y^2 - 4x^2y^3$", "is_correct": False}, {"text": "$4x^4y - 4x^3y^2 + 4x^2y^3$", "is_correct": False}, {"text": "$-4x^4y + xy - 4x^2y^3$", "is_correct": False}], "explanation": "$(-4x^2y)(x^2) = -4x^4y$. $(-4x^2y)(-xy) = +4x^3y^2$. $(-4x^2y)(y^2) = -4x^2y^3$."})
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "avanzada", "text": "Calcula el producto y reduce: $-3m(2m - 1) - m(m + 4)$.", "options": [{"text": "$-7m^2 - m$", "is_correct": True}, {"text": "$-7m^2 + m$", "is_correct": False}, {"text": "$-5m^2 - m$", "is_correct": False}, {"text": "$-7m^2 + 7m$", "is_correct": False}], "explanation": "$-6m^2 + 3m - m^2 - 4m$. Reduciendo semejantes: $(-6-1)m^2 + (3-4)m = -7m^2 - m$."})
    # Tipo PAES
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "basica", "text": "La expresión $-2x^3(4x - 5)$ es equivalente a:", "options": [{"text": "$-8x^4 + 10x^3$", "is_correct": True}, {"text": "$-8x^4 - 10x^3$", "is_correct": False}, {"text": "$-6x^4 + 10x^3$", "is_correct": False}, {"text": "$-8x^4 - 5$", "is_correct": False}], "explanation": "Se aplica distributividad invirtiendo los signos: $-2x^3 \\cdot 4x = -8x^4$; $-2x^3 \\cdot (-5) = 10x^3$."})
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "intermedia", "text": "Si el largo de un rectángulo es $(3x^2 - 2x + 1)$ y su ancho se representa curiosamente por $-2x$ (donde $x < 0$ para que sea positivo), ¿cuál es el área de dicho rectángulo?", "options": [{"text": "$-6x^3 + 4x^2 - 2x$", "is_correct": True}, {"text": "$-6x^3 - 4x^2 - 2x$", "is_correct": False}, {"text": "$-6x^3 - 2x + 1$", "is_correct": False}, {"text": "$6x^3 - 4x^2 + 2x$", "is_correct": False}], "explanation": "Área $= (-2x)(3x^2 - 2x + 1) = -6x^3 + 4x^2 - 2x$."})
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "avanzada", "text": "Al restar la expresión $-x(x-3)$ del polinomio $2x^2 + 3x$, el resultado es:", "options": [{"text": "$3x^2$", "is_correct": True}, {"text": "$x^2 + 6x$", "is_correct": False}, {"text": "$3x^2 + 6x$", "is_correct": False}, {"text": "$x^2$", "is_correct": False}], "explanation": "El producto es $-x^2 + 3x$. Al restarlo: $(2x^2 + 3x) - (-x^2 + 3x) = 2x^2 + 3x + x^2 - 3x = 3x^2$."})

    # 2. MAT.ALG.MULT_POLINOMIOS.COEFICIENTES_FRACCIONARIOS
    nid = "MAT.ALG.MULT_POLINOMIOS.COEFICIENTES_FRACCIONARIOS"
    # Conceptuales
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "basica", "text": "Para multiplicar los términos $(\\frac{a}{b}x)$ y $(\\frac{c}{d}y)$, ¿cuál es el procedimiento correcto para los coeficientes?", "options": [{"text": "Multiplicar $a \\cdot c$ y dividirlo por $b \\cdot d$.", "is_correct": True}, {"text": "Multiplicar cruzado $a \\cdot d$ y $b \\cdot c$.", "is_correct": False}, {"text": "Encontrar el denominador común entre $b$ y $d$.", "is_correct": False}, {"text": "Sumar los numeradores y multiplicar denominadores.", "is_correct": False}], "explanation": "La multiplicación de fracciones se hace directa: numerador por numerador, y denominador por denominador."})
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "intermedia", "text": "Al multiplicar dos binomios con coeficientes fraccionarios, ¿en qué paso es generalmente necesario calcular un mínimo común múltiplo (MCM)?", "options": [{"text": "Al reducir los términos semejantes finales.", "is_correct": True}, {"text": "Al multiplicar el primer término por el primero.", "is_correct": False}, {"text": "Al multiplicar el último término por el último.", "is_correct": False}, {"text": "En todos los pasos del proceso.", "is_correct": False}], "explanation": "La multiplicación de fracciones no requiere MCM. El MCM se necesita solo al sumar o restar fracciones, es decir, al reducir los términos semejantes."})
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "avanzada", "text": "Si el producto de dos términos es $\\frac{6}{20}x^3$, ¿qué se debe hacer siempre como paso final?", "options": [{"text": "Simplificar la fracción resultante a $\\frac{3}{10}$.", "is_correct": True}, {"text": "Invertir la fracción a $\\frac{20}{6}$.", "is_correct": False}, {"text": "Restar el exponente $3$ al numerador.", "is_correct": False}, {"text": "Pasarlo a número mixto.", "is_correct": False}], "explanation": "Siempre se deben expresar los coeficientes fraccionarios en su forma irreducible, en este caso simplificando por $2$."})
    # Reconocimiento
    exercises.append({"node_id": nid, "kind": "reconocimiento", "difficulty": "basica", "text": "¿Cuál es el resultado de la multiplicación $(\\frac{1}{2}x) \\cdot (\\frac{2}{3}x)$?", "options": [{"text": "$\\frac{1}{3}x^2$", "is_correct": True}, {"text": "$\\frac{2}{5}x^2$", "is_correct": False}, {"text": "$\\frac{3}{6}x^2$", "is_correct": False}, {"text": "$\\frac{4}{3}x^2$", "is_correct": False}], "explanation": "Multiplicamos $\\frac{1 \\cdot 2}{2 \\cdot 3} = \\frac{2}{6}$, que simplificado es $\\frac{1}{3}$. Las $x$ suman grados: $x^2$."})
    # Procedimiento
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "basica", "text": "Calcula el producto: $(\\frac{1}{2}x + 1)(\\frac{1}{2}x - 1)$", "options": [{"text": "$\\frac{1}{4}x^2 - 1$", "is_correct": True}, {"text": "$\\frac{1}{4}x^2 + 1$", "is_correct": False}, {"text": "$\\frac{1}{2}x^2 - 1$", "is_correct": False}, {"text": "$x^2 - 1$", "is_correct": False}], "explanation": "Suma por su diferencia: $(\\frac{1}{2}x)^2 - (1)^2 = \\frac{1}{4}x^2 - 1$."})
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "intermedia", "text": "Calcula $(\\frac{2}{3}a - \\frac{1}{2})(\\frac{3}{4}a + 2)$", "options": [{"text": "$\\frac{1}{2}a^2 + \\frac{23}{24}a - 1$", "is_correct": True}, {"text": "$\\frac{1}{2}a^2 + \\frac{5}{12}a - 1$", "is_correct": False}, {"text": "$\\frac{1}{2}a^2 + \\frac{41}{24}a - 1$", "is_correct": False}, {"text": "$\\frac{1}{2}a^2 + a - 1$", "is_correct": False}], "explanation": "Distribuir: $(\\frac{2}{3}\\cdot\\frac{3}{4})a^2 + (\\frac{2}{3}\\cdot 2)a - (\\frac{1}{2}\\cdot\\frac{3}{4})a - (\\frac{1}{2}\\cdot 2)$. Coeficientes: $\\frac{1}{2}a^2 + \\frac{4}{3}a - \\frac{3}{8}a - 1$. Reduciendo $\\frac{4}{3} - \\frac{3}{8} = \\frac{32 - 9}{24} = \\frac{23}{24}$."})
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "avanzada", "text": "Si se multiplica $(\\frac{3}{5}x^2 - \\frac{1}{3}xy)(\\frac{5}{2}x + y)$, el coeficiente del término $x^2y$ es:", "options": [{"text": "$-\\frac{7}{30}$", "is_correct": True}, {"text": "$-\\frac{5}{6}$", "is_correct": False}, {"text": "$\\frac{3}{5}$", "is_correct": False}, {"text": "$\\frac{1}{15}$", "is_correct": False}], "explanation": "El término en $x^2y$ se forma por $(\\frac{3}{5}x^2)(y) + (-\\frac{1}{3}xy)(\\frac{5}{2}x)$. Eso es $\\frac{3}{5}x^2y - \\frac{5}{6}x^2y$. Restamos: $\\frac{3}{5} - \\frac{5}{6} = \\frac{18 - 25}{30} = -\\frac{7}{30}$."})
    # Tipo PAES
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "basica", "text": "Al desarrollar $(\\frac{x}{3} + \\frac{y}{2})^2$, el resultado correcto es:", "options": [{"text": "$\\frac{x^2}{9} + \\frac{xy}{3} + \\frac{y^2}{4}$", "is_correct": True}, {"text": "$\\frac{x^2}{9} + \\frac{y^2}{4}$", "is_correct": False}, {"text": "$\\frac{x^2}{9} + \\frac{xy}{6} + \\frac{y^2}{4}$", "is_correct": False}, {"text": "$\\frac{x^2}{6} + \\frac{xy}{5} + \\frac{y^2}{4}$", "is_correct": False}], "explanation": "Cuadrado de binomio: $(\\frac{x}{3})^2 + 2(\\frac{x}{3})(\\frac{y}{2}) + (\\frac{y}{2})^2 = \\frac{x^2}{9} + \\frac{xy}{3} + \\frac{y^2}{4}$."})
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "intermedia", "text": "El área de una lámina metálica viene dada por el producto $(\\frac{3}{2}x - \\frac{1}{4})(\\frac{2}{3}x + 2)$. Al expresar el área como polinomio, el término independiente es:", "options": [{"text": "$-\\frac{1}{2}$", "is_correct": True}, {"text": "$-\\frac{1}{4}$", "is_correct": False}, {"text": "$\\frac{1}{2}$", "is_correct": False}, {"text": "$-2$", "is_correct": False}], "explanation": "El término independiente resulta de multiplicar los términos independientes: $(-\\frac{1}{4}) \\cdot (2) = -\\frac{2}{4} = -\\frac{1}{2}$."})
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "avanzada", "text": "¿Cuál es el resultado de $(\\frac{4}{3}a - \\frac{3}{2}b)(\\frac{4}{3}a + \\frac{3}{2}b)$?", "options": [{"text": "$\\frac{16}{9}a^2 - \\frac{9}{4}b^2$", "is_correct": True}, {"text": "$\\frac{16}{9}a^2 + \\frac{9}{4}b^2$", "is_correct": False}, {"text": "$\\frac{8}{3}a^2 - \\frac{6}{2}b^2$", "is_correct": False}, {"text": "$\\frac{16}{3}a^2 - \\frac{9}{2}b^2$", "is_correct": False}], "explanation": "Es una suma por su diferencia: $(\\frac{4}{3}a)^2 - (\\frac{3}{2}b)^2 = \\frac{16}{9}a^2 - \\frac{9}{4}b^2$."})

    # 3. MAT.ALG.MULT_MONOMIOS.GRADO_PRODUCTO
    nid = "MAT.ALG.MULT_MONOMIOS.GRADO_PRODUCTO"
    # Conceptuales
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "basica", "text": "Al multiplicar dos monomios, ¿cómo se determina el grado absoluto del producto?", "options": [{"text": "Sumando los grados absolutos de ambos monomios.", "is_correct": True}, {"text": "Multiplicando los grados absolutos de ambos monomios.", "is_correct": False}, {"text": "El grado absoluto es igual al del monomio de mayor grado.", "is_correct": False}, {"text": "Restando los grados absolutos.", "is_correct": False}], "explanation": "Como las potencias de igual base se suman ($x^a \\cdot x^b = x^{a+b}$), los grados absolutos de los factores se suman."})
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "intermedia", "text": "Si un monomio es de grado absoluto $m$ y se multiplica por otro monomio de grado absoluto $n$, el resultado es un monomio de grado absoluto:", "options": [{"text": "$m + n$", "is_correct": True}, {"text": "$m \\cdot n$", "is_correct": False}, {"text": "$m^n$", "is_correct": False}, {"text": "Depende de los coeficientes.", "is_correct": False}], "explanation": "El grado del producto siempre es la suma de los grados de los factores, es decir, $m+n$."})
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "avanzada", "text": "¿Es posible que al multiplicar dos monomios de grado $3$, el resultado sea un monomio de grado $3$?", "options": [{"text": "No, el resultado siempre será de grado $6$.", "is_correct": True}, {"text": "Sí, si se cancelan algunas variables.", "is_correct": False}, {"text": "Sí, si los coeficientes son negativos.", "is_correct": False}, {"text": "No, el resultado será de grado $9$.", "is_correct": False}], "explanation": "El grado del producto es la suma exacta de los grados de los factores. $3 + 3 = 6$. No hay cancelaciones al multiplicar."})
    # Reconocimiento
    exercises.append({"node_id": nid, "kind": "reconocimiento", "difficulty": "basica", "text": "El grado absoluto del monomio $-5x^2y^3$ es $5$. ¿Cuál es el grado de multiplicarlo por $x$?", "options": [{"text": "$6$", "is_correct": True}, {"text": "$5$", "is_correct": False}, {"text": "$7$", "is_correct": False}, {"text": "$10$", "is_correct": False}], "explanation": "El monomio $x$ tiene grado $1$. El producto tendrá grado $5 + 1 = 6$."})
    # Procedimiento
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "basica", "text": "Calcula el grado absoluto del producto entre $4a^2b$ y $-3ab^4$.", "options": [{"text": "$8$", "is_correct": True}, {"text": "$7$", "is_correct": False}, {"text": "$6$", "is_correct": False}, {"text": "$9$", "is_correct": False}], "explanation": "El primer factor tiene grado $2+1=3$. El segundo factor tiene grado $1+4=5$. $3+5=8$."})
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "intermedia", "text": "Determina el grado relativo a la letra $x$ del producto de $2x^3y^5z$ y $x^n y^2$, sabiendo que $n=4$.", "options": [{"text": "$7$", "is_correct": True}, {"text": "$4$", "is_correct": False}, {"text": "$3$", "is_correct": False}, {"text": "$12$", "is_correct": False}], "explanation": "El grado relativo a $x$ es la suma de los exponentes de $x$. $3 + 4 = 7$."})
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "avanzada", "text": "El monomio $M_1 = ax^2y^b$ tiene grado absoluto $5$. El monomio $M_2 = 2x^cy^4$ tiene grado absoluto $7$. ¿Cuál es el grado absoluto del producto $M_1 \\cdot M_2$?", "options": [{"text": "$12$", "is_correct": True}, {"text": "$35$", "is_correct": False}, {"text": "$13$", "is_correct": False}, {"text": "No se puede determinar sin conocer $a, b, c$.", "is_correct": False}], "explanation": "Independiente de los valores, el grado del producto es la suma de los grados de los factores. $5 + 7 = 12$."})
    # Tipo PAES
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "basica", "text": "Si se multiplica un monomio de grado $k$ por otro monomio de grado $k+2$, el polinomio resultante es de grado:", "options": [{"text": "$2k + 2$", "is_correct": True}, {"text": "$2k$", "is_correct": False}, {"text": "$k^2 + 2k$", "is_correct": False}, {"text": "$k+2$", "is_correct": False}], "explanation": "Se suman los grados: $k + (k+2) = 2k + 2$."})
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "intermedia", "text": "Sea $P$ el producto de $3x^m y^3$ y $-2x^2 y^n$. Si el grado relativo de $x$ en $P$ es $5$ y el grado relativo a $y$ en $P$ es $7$, ¿cuál es el grado absoluto de $P$?", "options": [{"text": "$12$", "is_correct": True}, {"text": "$35$", "is_correct": False}, {"text": "$5$", "is_correct": False}, {"text": "$7$", "is_correct": False}], "explanation": "El grado absoluto es la suma de todos los grados relativos del monomio final, es decir, $5 + 7 = 12$."})
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "avanzada", "text": "Al multiplicar $n$ monomios, todos de grado $3$, el grado del producto será:", "options": [{"text": "$3n$", "is_correct": True}, {"text": "$n^3$", "is_correct": False}, {"text": "$3+n$", "is_correct": False}, {"text": "$3^n$", "is_correct": False}], "explanation": "El grado se suma $n$ veces: $3 + 3 + ... + 3$ ($n$ veces) $= 3n$."})

    # 4. MAT.ALG.MULT_MON_POL.DISTRIBUCION_PARCIAL_ERROR
    nid = "MAT.ALG.MULT_MON_POL.DISTRIBUCION_PARCIAL_ERROR"
    # Conceptuales
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "basica", "text": "El error de distribución parcial al resolver $a(b + c)$ consiste en:", "options": [{"text": "Multiplicar $a$ solo por $b$ y dejar $c$ igual.", "is_correct": True}, {"text": "Multiplicar $b$ por $c$ y luego por $a$.", "is_correct": False}, {"text": "Sumar $a$, $b$ y $c$.", "is_correct": False}, {"text": "Multiplicar $a$ por $b$ y también por $c$.", "is_correct": False}], "explanation": "El error clásico es $a(b+c) = ab+c$, olvidando multiplicar $a$ por $c$."})
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "intermedia", "text": "¿Cuál es la causa matemática del error de distribución parcial?", "options": [{"text": "Ignorar que el paréntesis agrupa todos los términos y el factor exterior aplica a toda la suma.", "is_correct": True}, {"text": "Desconocer la ley de los signos.", "is_correct": False}, {"text": "Sumar los exponentes incorrectamente.", "is_correct": False}, {"text": "No saber simplificar fracciones.", "is_correct": False}], "explanation": "El error nace de no tratar el paréntesis como un solo bloque sobre el cual se debe aplicar la propiedad distributiva a cada componente."})
    exercises.append({"node_id": nid, "kind": "conceptual", "difficulty": "avanzada", "text": "Si un estudiante desarrolla $-2x(x^2 - 3x + 1)$ y obtiene $-2x^3 - 3x + 1$, cometió un error de distribución parcial. ¿Cuántos términos debió modificar el factor $-2x$?", "options": [{"text": "$3$ términos", "is_correct": True}, {"text": "$1$ término", "is_correct": False}, {"text": "$2$ términos", "is_correct": False}, {"text": "$4$ términos", "is_correct": False}], "explanation": "Como el polinomio del paréntesis es un trinomio (3 términos), el $-2x$ debía multiplicar a cada uno de los 3."})
    # Reconocimiento
    exercises.append({"node_id": nid, "kind": "reconocimiento", "difficulty": "basica", "text": "Selecciona el desarrollo correcto que NO presenta error de distribución parcial para $5(x - 2)$.", "options": [{"text": "$5x - 10$", "is_correct": True}, {"text": "$5x - 2$", "is_correct": False}, {"text": "$x - 10$", "is_correct": False}, {"text": "$5x - 7$", "is_correct": False}], "explanation": "El $5$ multiplica tanto a $x$ como a $-2$, dando $5x - 10$."})
    # Procedimiento
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "basica", "text": "Un alumno escribió $3x(y + 2z) = 3xy + 2z$. Calcula el resultado correcto.", "options": [{"text": "$3xy + 6xz$", "is_correct": True}, {"text": "$3xy + 6z$", "is_correct": False}, {"text": "$xy + 6xz$", "is_correct": False}, {"text": "$3xy + 5xz$", "is_correct": False}], "explanation": "$3x \\cdot y = 3xy$. $3x \\cdot 2z = 6xz$."})
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "intermedia", "text": "Corrige el siguiente error: $ab(a - b) = a^2b - b$.", "options": [{"text": "$a^2b - ab^2$", "is_correct": True}, {"text": "$a^2b - ab$", "is_correct": False}, {"text": "$a^2b - b^2$", "is_correct": False}, {"text": "$a^2 - ab^2$", "is_correct": False}], "explanation": "El segundo término del resultado debe ser $(ab)(-b) = -ab^2$."})
    exercises.append({"node_id": nid, "kind": "procedimiento_basico", "difficulty": "avanzada", "text": "En el desarrollo de $-m(m^2 - m + 1)$, se obtuvo $-m^3 - m + 1$. Entre los errores cometidos, señala el resultado correcto completo.", "options": [{"text": "$-m^3 + m^2 - m$", "is_correct": True}, {"text": "$-m^3 - m^2 - m$", "is_correct": False}, {"text": "$-m^3 + m^2 + 1$", "is_correct": False}, {"text": "$-m^3 - m^2 + m$", "is_correct": False}], "explanation": "$-m \\cdot m^2 = -m^3$; $-m \\cdot -m = +m^2$; $-m \\cdot 1 = -m$."})
    # Tipo PAES
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "basica", "text": "Si $A = 2x(x+1)$ y un estudiante asegura que $A = 2x^2 + 1$, el valor de $A$ evaluado en $x=2$ según el estudiante, y el verdadero valor, son respectivamente:", "options": [{"text": "$9$ y $12$", "is_correct": True}, {"text": "$12$ y $9$", "is_correct": False}, {"text": "$9$ y $9$", "is_correct": False}, {"text": "$5$ y $12$", "is_correct": False}], "explanation": "El estudiante calcula $2(2^2) + 1 = 9$. El valor real es $2(2)(3) = 12$."})
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "intermedia", "text": "¿Cuál es la diferencia entre el resultado de la distribución correcta de $x(x - 5)$ y el resultado con error de distribución parcial $x^2 - 5$?", "options": [{"text": "$-5x + 5$", "is_correct": True}, {"text": "$5x - 5$", "is_correct": False}, {"text": "$-5x - 5$", "is_correct": False}, {"text": "$5x + 5$", "is_correct": False}], "explanation": "Correcto: $x^2 - 5x$. Incorrecto: $x^2 - 5$. Diferencia: $(x^2 - 5x) - (x^2 - 5) = x^2 - 5x - x^2 + 5 = -5x + 5$."})
    exercises.append({"node_id": nid, "kind": "tipo_paes", "difficulty": "avanzada", "text": "Dada la ecuación $3(x - 2) = 12$, un alumno con distribución parcial llega a la solución $x_1$. La solución correcta es $x_2$. ¿Cuál es el valor de $x_1 - x_2$?", "options": [{"text": "$8$", "is_correct": True}, {"text": "$2$", "is_correct": False}, {"text": "$4$", "is_correct": False}, {"text": "$14$", "is_correct": False}], "explanation": "Alumno: $3x - 2 = 12 \\Rightarrow 3x = 14 \\Rightarrow x_1 = 14/3$. Correcto: $3x - 6 = 12 \\Rightarrow 3x = 18 \\Rightarrow x_2 = 6$. $14/3 - 18/3 = -4/3$. Wait, let me re-calculate."})
    # Recalculating the advanced PAES logic
    exercises[-1]["options"] = [{"text": "$-\\frac{4}{3}$", "is_correct": True}, {"text": "$\\frac{4}{3}$", "is_correct": False}, {"text": "$-2$", "is_correct": False}, {"text": "$2$", "is_correct": False}]

    # Write files
    for yaml_filename, yaml_content in YAMLS.items():
        with open(f"docs/conocimiento/contenido/{yaml_filename}", "w", encoding="utf-8") as f:
            f.write(yaml_content)

    print("Creados 4 yamls...")

    jsonl_filename = "docs/conocimiento/ejercicios/mat-alg-multiplicacion-banco-gen-4.jsonl"
    with open(jsonl_filename, "w", encoding="utf-8") as f:
        for ex in exercises:
            f.write(json.dumps(ex, ensure_ascii=False) + "\\n")

    print(f"{jsonl_filename} con {len(exercises)} ejercicios")

if __name__ == "__main__":
    generate_exercises()

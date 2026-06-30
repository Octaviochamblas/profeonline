import json
import os

def generate_exercises():
    YAMLS = {
        "mat-alg-generalizaciones-productos-cubo-trinomio.yaml": """semantic_id: "MAT.ALG.GENERALIZACIONES_PRODUCTOS.CUBO_TRINOMIO"
titulo: "Concepto de cubo de trinomio"
objetivo: "Comprender la expansión de $(a+b+c)^3$ como una extensión de los productos notables básicos."
introduccion: "Elevar un trinomio al cubo es una tarea monumental a mano. ¿Existe una regla?"
resumen: |
  La expansión de $(a+b+c)^3$ genera 27 términos antes de agrupar.
  Fórmula agrupada:
  $(a+b+c)^3 = a^3 + b^3 + c^3 + 3(a+b)(b+c)(c+a)$
  Esta es una forma factorizada muy útil en problemas de álgebra avanzada o de olimpiadas.
explicacion: |
  El desarrollo puro completo (sin factorizar) tiene cubos puros ($a^3$), términos del tipo $3a^2b$, y un término central $6abc$.
  La identidad factorizada de Cauchy es a menudo más útil porque relaciona la suma de cubos con el producto de sumas parciales.
procedimiento: |
  En general, en educación media no se exige memorizar el desarrollo puro, pero sí saber cómo construirlo multiplicando $(a+b+c)^2 \cdot (a+b+c)$ o reconocer identidades.
ejemplos:
  - titulo: "Problema avanzado"
    enunciado: "Si $a+b+c=0$, entonces ¿a qué es igual $a^3+b^3+c^3$?"
    solucion_pasos:
      - "Usamos la identidad de Gauss o la expansión del cubo."
      - "Se deduce que $a^3+b^3+c^3 = 3abc$."
errores_frecuentes:
  - "Creer que es $a^3+b^3+c^3$ solamente."
""",
        "mat-alg-generalizaciones-productos-pascal-coeficientes.yaml": """semantic_id: "MAT.ALG.GENERALIZACIONES_PRODUCTOS.PASCAL_COEFICIENTES"
titulo: "Triángulo de Pascal y coeficientes binomiales"
objetivo: "Utilizar el Triángulo de Pascal para hallar rápidamente los coeficientes del desarrollo de $(a+b)^n$."
introduccion: "¿Quieres expandir $(a+b)^4$ o $(a+b)^5$ sin multiplicar todo? Blaise Pascal tiene un truco para ti."
resumen: |
  El **Triángulo de Pascal** es un arreglo triangular de números donde cada número (salvo los 1 de los bordes) es la suma de los dos números directamente arriba de él.
  La fila $n$ del triángulo nos da exactamente los coeficientes numéricos del desarrollo de $(a+b)^n$.
explicacion: |
  Fila 0 (para exponente 0): 1
  Fila 1 (exponente 1): 1, 1
  Fila 2 (exponente 2): 1, 2, 1 (cuadrado de binomio)
  Fila 3 (exponente 3): 1, 3, 3, 1 (cubo de binomio)
  Fila 4 (exponente 4): 1, 4, 6, 4, 1
  Fila 5 (exponente 5): 1, 5, 10, 10, 5, 1
procedimiento: |
  Para expandir $(a+b)^4$:
  1. Escribe los coeficientes de la fila 4: 1, 4, 6, 4, 1.
  2. Acompaña cada coeficiente con $a$ decreciendo su exponente (desde 4 hasta 0).
  3. Acompaña cada coeficiente con $b$ creciendo su exponente (desde 0 hasta 4).
  4. Queda: $1a^4 + 4a^3b + 6a^2b^2 + 4ab^3 + 1b^4$.
ejemplos:
  - titulo: "Fila 4"
    enunciado: "Encuentra el coeficiente de $x^2y^2$ en $(x+y)^4$."
    solucion_pasos:
      - "Mirando la fila 4: 1, 4, 6, 4, 1."
      - "El término central corresponde a exponentes iguales $x^2y^2$."
      - "Su coeficiente es 6."
errores_frecuentes:
  - "Contar la punta del triángulo como la fila 1 en lugar de la fila 0."
""",
        "mat-alg-generalizaciones-productos-binomio-newton.yaml": """semantic_id: "MAT.ALG.GENERALIZACIONES_PRODUCTOS.BINOMIO_NEWTON"
titulo: "Formalización del Binomio de Newton"
objetivo: "Comprender la fórmula general del Binomio de Newton usando combinatoria."
introduccion: "El triángulo de Pascal es genial, pero si te piden $(x+y)^{50}$, ¿dibujarás 50 filas? Isaac Newton ideó una fórmula mejor."
resumen: |
  El Teorema del Binomio establece que:
  $(a+b)^n = \sum_{k=0}^{n} \\binom{n}{k} a^{n-k} b^k$
  Donde $\\binom{n}{k} = \\frac{n!}{k!(n-k)!}$ es el número combinatorio (o coeficiente binomial), que calcula el mismo valor que aparece en el Triángulo de Pascal.
explicacion: |
  Esta fórmula nos permite encontrar cualquier término de la expansión de forma directa sin calcular los anteriores.
  Los exponentes de $a$ bajan de $n$ a $0$, los de $b$ suben de $0$ a $n$, y la suma de ambos exponentes en cada término siempre es $n$.
procedimiento: |
  Para hallar un desarrollo o un coeficiente:
  1. Identifica $n$, $a$ y $b$.
  2. Aplica la sumatoria o la fórmula del combinatorio para los coeficientes que necesites.
ejemplos:
  - titulo: "Coeficiente directo"
    enunciado: "Encuentra el coeficiente del segundo término en el desarrollo de $(x+y)^{10}$."
    solucion_pasos:
      - "El primer término es $k=0$, el segundo es $k=1$."
      - "Coeficiente: $\\binom{10}{1} = \frac{10!}{1!9!} = 10$."
      - "El término completo es $10x^9y$."
errores_frecuentes:
  - "Olvidar que $k$ empieza en 0, por lo que el 'término $m$' corresponde a $k = m-1$."
""",
        "mat-alg-generalizaciones-productos-termino-general.yaml": """semantic_id: "MAT.ALG.GENERALIZACIONES_PRODUCTOS.TERMINO_GENERAL"
titulo: "Término general en expansión binomial"
objetivo: "Calcular un término específico del desarrollo de un binomio sin tener que desarrollarlo todo."
introduccion: "¡Es hora de sacar provecho del Binomio de Newton para evitar trabajo excesivo!"
resumen: |
  El **término general** (el término que ocupa el lugar $k+1$) en el desarrollo de $(a+b)^n$ es:
  $T_{k+1} = \\binom{n}{k} a^{n-k} b^k$
explicacion: |
  El lugar del término siempre es uno más que $k$. Es decir, para encontrar el quinto término, se usa $k=4$.
procedimiento: |
  Para buscar el término $m$-ésimo:
  1. Establece $k = m - 1$.
  2. Identifica $n, a, b$ del binomio.
  3. Reemplaza en la fórmula $T_{k+1}$.
  4. Resuelve el número combinatorio y simplifica las potencias de las bases.
ejemplos:
  - titulo: "Búsqueda del 3er término"
    enunciado: "Halla el tercer término del desarrollo de $(2x - y)^4$."
    solucion_pasos:
      - "Tercer término implica $k = 2$. Además $n = 4$, $a = 2x$, $b = -y$."
      - "$T_{3} = \\binom{4}{2} (2x)^{4-2} (-y)^2$."
      - "$\\binom{4}{2} = 6$."
      - "$T_{3} = 6 (2x)^2 (y^2) = 6(4x^2)(y^2) = 24x^2y^2$."
errores_frecuentes:
  - "No aplicar la potencia de $a$ o $b$ al coeficiente numérico interno de la base (ej. decir que $(2x)^2$ es $2x^2$ en lugar de $4x^2$)."
"""
    }

    exercises = []
    
    # 1. CUBO TRINOMIO
    sid = "MAT.ALG.GENERALIZACIONES_PRODUCTOS.CUBO_TRINOMIO"
    exercises.append({"stable_id": "GP-CT-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Si sumamos $a^3 + b^3 + c^3$ y sabemos que $(a+b+c) = 0$, la identidad de Gauss para cubos nos dice que esa suma es igual a:", "choices": ["A) $3abc$", "B) $0$", "C) $(abc)^3$", "D) $-3abc$"], "correct_answer": "A) $3abc$", "solution_steps": "Propiedad conocida de olimpiadas: si $a+b+c=0$, $a^3+b^3+c^3 = 3abc$.", "paes_style": True})
    
    # 2. PASCAL
    sid = "MAT.ALG.GENERALIZACIONES_PRODUCTOS.PASCAL_COEFICIENTES"
    exercises.append({"stable_id": "GP-PC-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Usando la fila 4 del triángulo de Pascal ($1, 4, 6, 4, 1$), ¿cuál es el desarrollo de $(x-y)^4$?", "choices": ["A) $x^4 - 4x^3y + 6x^2y^2 - 4xy^3 + y^4$", "B) $x^4 + 4x^3y + 6x^2y^2 + 4xy^3 + y^4$", "C) $x^4 - y^4$", "D) $x^4 - 4xy + y^4$"], "correct_answer": "A) $x^4 - 4x^3y + 6x^2y^2 - 4xy^3 + y^4$", "solution_steps": "Los coeficientes son 1,4,6,4,1 y los signos se alternan al ser una diferencia.", "paes_style": False})

    # 3. BINOMIO NEWTON
    sid = "MAT.ALG.GENERALIZACIONES_PRODUCTOS.BINOMIO_NEWTON"
    exercises.append({"stable_id": "GP-BN-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "De acuerdo con el Teorema del Binomio, la suma de todos los coeficientes del desarrollo de $(1+1)^n$ es:", "choices": ["A) $2^n$", "B) $n!$", "C) $0$", "D) $n^2$"], "correct_answer": "A) $2^n$", "solution_steps": "$(1+1)^n = 2^n$. Y por la fórmula, esto es la suma de los combinatorios $\\binom{n}{k}$.", "paes_style": True})

    # 4. TERMINO GENERAL
    sid = "MAT.ALG.GENERALIZACIONES_PRODUCTOS.TERMINO_GENERAL"
    exercises.append({"stable_id": "GP-TG-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Halla el tercer término del desarrollo de $(x + 2)^5$.", "choices": ["A) $40x^3$", "B) $10x^3$", "C) $20x^2$", "D) $80x^2$"], "correct_answer": "A) $40x^3$", "solution_steps": "$k=2$. $\\binom{5}{2} = 10$. El término es $10 (x)^{5-2} (2)^2 = 10 x^3 (4) = 40x^3$.", "paes_style": True})

    # Write files
    for yaml_filename, yaml_content in YAMLS.items():
        with open(f"docs/conocimiento/contenido/{yaml_filename}", "w", encoding="utf-8") as f:
            f.write(yaml_content)
    print(f"Creados {len(YAMLS)} yamls T5...")
    
    jsonl_filename = "docs/conocimiento/ejercicios/mat-alg-productos-notables-banco-gen-5.jsonl"
    with open(jsonl_filename, "w", encoding="utf-8") as f:
        for ex in exercises:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"{jsonl_filename} con {len(exercises)} ejercicios T5")

if __name__ == "__main__":
    generate_exercises()

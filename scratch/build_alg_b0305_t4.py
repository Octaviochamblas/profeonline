import json
import os

def generate_exercises():
    YAMLS = {
        "mat-alg-cubo-binomio-diferencia-definicion.yaml": """semantic_id: "MAT.ALG.CUBO_BINOMIO.DIFERENCIA_DEFINICION"
titulo: "Definición de cubo de binomio (Diferencia)"
objetivo: "Comprender e interpretar algebraicamente el concepto del cubo de un binomio en su forma de diferencia $(a-b)^3$."
introduccion: "¡Elevar al cubo es subir de nivel! Pasamos de multiplicar dos veces a multiplicar tres veces."
resumen: |
  El cubo de un binomio diferencia se define como la multiplicación del binomio por sí mismo tres veces:
  $(a-b)^3 = (a-b)(a-b)(a-b)$.
  Esto es equivalente a tomar el cuadrado del binomio y multiplicarlo una vez más por $(a-b)$: $(a-b)^2 \cdot (a-b)$.
explicacion: |
  Desarrollemos $(a-b)^3$:
  1. Sabemos que $(a-b)^2 = a^2 - 2ab + b^2$.
  2. Multiplicamos esto por $(a-b)$: $(a^2 - 2ab + b^2)(a-b)$.
  3. Distribuyendo $a$: $a^3 - 2a^2b + ab^2$.
  4. Distribuyendo $-b$: $-a^2b + 2ab^2 - b^3$.
  5. Sumando: $a^3 - 3a^2b + 3ab^2 - b^3$.
procedimiento: |
  Para entender la definición:
  1. Reconoce que $(A-B)^3$ significa un factor $(A-B)$ repetido 3 veces.
  2. El desarrollo produce $4$ términos con signos que se alternan: $+ - + -$.
ejemplos:
  - titulo: "Expansión conceptual"
    enunciado: "Expresa conceptualmente qué significa $(2x - 3)^3$."
    solucion_pasos:
      - "Significa $(2x - 3)(2x - 3)(2x - 3)$."
errores_frecuentes:
  - "Pensar que $(a-b)^3 = a^3 - b^3$."
""",
        "mat-alg-cubo-binomio-regla-suma.yaml": """semantic_id: "MAT.ALG.CUBO_BINOMIO.REGLA_SUMA"
titulo: "Aplicación de la regla del cubo de binomio (Suma)"
objetivo: "Aplicar la fórmula rápida del cubo de binomio suma."
introduccion: "Multiplicar tres veces a mano es agotador. ¡Usemos la regla!"
resumen: |
  La regla para $(a+b)^3$ es:
  **"El cubo del primero, MÁS el triple del cuadrado del primero por el segundo, MÁS el triple del primero por el cuadrado del segundo, MÁS el cubo del segundo."**
  Fórmula: $(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3$
explicacion: |
  Cada término tiene grado total $3$ respecto a $a$ y $b$: $a^3$, $a^2b^1$, $a^1b^2$, $b^3$.
  Los coeficientes siguen la fila 3 del Triángulo de Pascal: $1, 3, 3, 1$.
procedimiento: |
  Para calcular $(A+B)^3$:
  1. Cubo del primero: $A^3$.
  2. $3 \cdot (A^2) \cdot B$.
  3. $3 \cdot A \cdot (B^2)$.
  4. Cubo del segundo: $B^3$.
ejemplos:
  - titulo: "Desarrollo rápido"
    enunciado: "Calcula $(x + 2)^3$."
    solucion_pasos:
      - "$(x)^3 = x^3$."
      - "$3(x)^2(2) = 6x^2$."
      - "$3(x)(2)^2 = 3(x)(4) = 12x$."
      - "$(2)^3 = 8$."
      - "Resultado: $x^3 + 6x^2 + 12x + 8$."
errores_frecuentes:
  - "Olvidar los coeficientes $3$, escribiendo erróneamente $a^3 + a^2b + ab^2 + b^3$."
""",
        "mat-alg-cubo-binomio-regla-diferencia.yaml": """semantic_id: "MAT.ALG.CUBO_BINOMIO.REGLA_DIFERENCIA"
titulo: "Aplicación de la regla del cubo de binomio (Diferencia)"
objetivo: "Aplicar la fórmula rápida del cubo de binomio diferencia."
introduccion: "Para la diferencia, la regla es la misma, ¡solo que los signos saltan!"
resumen: |
  Fórmula: $(a-b)^3 = a^3 - 3a^2b + 3ab^2 - b^3$
  Los signos se alternan: $+$, $-$, $+$, $-$.
explicacion: |
  Los términos donde la potencia de $(-b)$ es impar, resultan negativos.
  En $3a^2(-b)^1$, el resultado es negativo.
  En $3a(-b)^2$, el resultado es positivo (porque $(-b)^2 = +b^2$).
  En $(-b)^3$, el resultado es negativo.
procedimiento: |
  Calcula con los valores absolutos y coloca los signos alternados $+ - + -$.
ejemplos:
  - titulo: "Desarrollo con variables"
    enunciado: "Calcula $(y - 5)^3$."
    solucion_pasos:
      - "$(y)^3 = y^3$."
      - "$-3(y)^2(5) = -15y^2$."
      - "$+3(y)(5)^2 = 3(y)(25) = +75y$."
      - "$-(5)^3 = -125$."
      - "Resultado: $y^3 - 15y^2 + 75y - 125$."
errores_frecuentes:
  - "Poner todos los signos negativos: $a^3 - 3a^2b - 3ab^2 - b^3$."
""",
        "mat-alg-cubo-binomio-manejo-signos.yaml": """semantic_id: "MAT.ALG.CUBO_BINOMIO.MANEJO_SIGNOS"
titulo: "Manejo de signos en el cubo de binomio"
objetivo: "Dominar la determinación de signos en cubos donde ambos términos pueden ser negativos, o están invertidos."
introduccion: "¿Qué pasa si te piden $(-a-b)^3$? ¡Veamos cómo los signos juegan!"
resumen: |
  Propiedades de signos útiles para cubos:
  - $(-a-b)^3 = -(a+b)^3$
  - $(a-b)^3 = -(b-a)^3$ (¡A diferencia del cuadrado, la asimetría se mantiene!)
explicacion: |
  Al ser el exponente $3$ (impar), los signos negativos pueden factorizarse hacia afuera de la potencia.
  $[- (a+b)]^3 = (-1)^3 (a+b)^3 = -1 (a+b)^3 = -(a+b)^3$.
  Esto significa que $(-a-b)^3 = -a^3 - 3a^2b - 3ab^2 - b^3$.
procedimiento: |
  Si tienes demasiados negativos, puedes factorizar un $-1$ y elevarlo al cubo para limpiar la expresión.
ejemplos:
  - titulo: "Inversión de orden"
    enunciado: "Calcula $(2 - x)^3$."
    solucion_pasos:
      - "Aplicamos la fórmula de diferencia: $(2)^3 - 3(2)^2(x) + 3(2)(x)^2 - (x)^3$."
      - "$8 - 12x + 6x^2 - x^3$."
errores_frecuentes:
  - "Creer que $(a-b)^3 = (b-a)^3$ asumiendo que los cubos se comportan igual que los cuadrados."
""",
        "mat-alg-cubo-binomio-error-terminos-mixtos.yaml": """semantic_id: "MAT.ALG.CUBO_BINOMIO.ERROR_TERMINOS_MIXTOS"
titulo: "Detección de error por omisión de términos mixtos"
objetivo: "Identificar y corregir el error de asumir $(a+b)^3 = a^3+b^3$."
introduccion: "Al igual que con el cuadrado, no podemos simplemente repartir el exponente en la suma."
resumen: |
  El error $(a+b)^3 = a^3 + b^3$ omite dos términos completos: $3a^2b$ y $3ab^2$.
  La suma de cubos $a^3 + b^3$ SÍ existe, pero es el resultado de un producto totalmente distinto: $(a+b)(a^2 - ab + b^2)$.
explicacion: |
  Verifiquemos numéricamente: $(1+2)^3 = 3^3 = 27$.
  Si hiciéramos la forma errónea: $1^3 + 2^3 = 1 + 8 = 9$.
  Faltan $18$ unidades, que corresponden a $3(1)^2(2) + 3(1)(2)^2 = 6 + 12 = 18$.
procedimiento: |
  Si ves una expansión con solo 2 términos al cubo, está mala. Debe tener 4 términos.
ejemplos:
  - titulo: "Análisis de afirmaciones"
    enunciado: "Un estudiante dice que para calcular el volumen de un cubo de lado $(x+2)$ basta con calcular $x^3 + 8$. ¿Por qué falla?"
    solucion_pasos:
      - "El volumen es el lado al cubo: $(x+2)^3$."
      - "Al desarrollar correctamente se obtiene $x^3 + 6x^2 + 12x + 8$."
      - "El estudiante omitió el volumen de los bloques rectangulares interiores."
errores_frecuentes:
  - "Confundir la expansión de $(a+b)^3$ con la factorización de suma de cubos $a^3+b^3$."
""",
        "mat-alg-cuadrado-trinomio-regla-general.yaml": """semantic_id: "MAT.ALG.CUADRADO_TRINOMIO.REGLA_GENERAL"
titulo: "Aplicación de la regla del cuadrado de trinomio"
objetivo: "Aplicar la fórmula rápida para el cuadrado de un polinomio de 3 términos."
introduccion: "Si el binomio tiene 3 términos, la regla se alarga un poco, ¡pero la lógica es la misma!"
resumen: |
  Fórmula: $(a+b+c)^2 = a^2 + b^2 + c^2 + 2ab + 2ac + 2bc$
  La suma de los cuadrados de cada término, más el doble producto de todas las combinaciones posibles de dos términos.
explicacion: |
  Si agrupamos $[(a+b)+c]^2$ y usamos la regla del binomio, llegamos a este desarrollo que contiene $6$ términos (3 cuadrados y 3 dobles productos).
procedimiento: |
  Para desarrollar $(A+B+C)^2$:
  1. Eleva cada uno al cuadrado (todos serán positivos).
  2. Haz el doble producto de $A$ y $B$.
  3. Haz el doble producto de $A$ y $C$.
  4. Haz el doble producto de $B$ y $C$.
ejemplos:
  - titulo: "Desarrollo completo"
    enunciado: "Desarrolla $(x+y+z)^2$."
    solucion_pasos:
      - "Cuadrados: $x^2 + y^2 + z^2$."
      - "Dobles productos: $2xy + 2xz + 2yz$."
      - "Suma total: $x^2 + y^2 + z^2 + 2xy + 2xz + 2yz$."
errores_frecuentes:
  - "Olvidar uno de los tres dobles productos."
""",
        "mat-alg-cuadrado-trinomio-manejo-signos.yaml": """semantic_id: "MAT.ALG.CUADRADO_TRINOMIO.MANEJO_SIGNOS"
titulo: "Manejo de signos en el cuadrado de trinomio"
objetivo: "Determinar correctamente el signo de los dobles productos cuando hay términos negativos."
introduccion: "Los cuadrados siempre son positivos, pero los dobles productos dependen de a quién multipliques."
resumen: |
  En $(a-b-c)^2$:
  - Los cuadrados $a^2, b^2, c^2$ siempre suman en positivo.
  - El signo del doble producto se determina multiplicando los signos de los dos términos involucrados.
explicacion: |
  Para $(x-y-z)^2$:
  1. Cuadrados: $x^2 + y^2 + z^2$.
  2. Doble producto $1$ y $2$: $2(x)(-y) = -2xy$.
  3. Doble producto $1$ y $3$: $2(x)(-z) = -2xz$.
  4. Doble producto $2$ y $3$: $2(-y)(-z) = +2yz$.
procedimiento: |
  Identifica los 3 términos con sus signos antes de empezar y aplica la regla de los signos en cada doble producto.
ejemplos:
  - titulo: "Con signos negativos"
    enunciado: "Calcula $(2m - n + 3)^2$."
    solucion_pasos:
      - "Términos: $2m, -n, 3$."
      - "Cuadrados: $4m^2 + n^2 + 9$."
      - "Dobles: $2(2m)(-n) = -4mn$; $2(2m)(3) = 12m$; $2(-n)(3) = -6n$."
      - "Total: $4m^2 + n^2 + 9 - 4mn + 12m - 6n$."
errores_frecuentes:
  - "Poner los cuadrados de los términos negativos con signo menos (ej. $-n^2$)."
""",
        "mat-alg-cuadrado-trinomio-representacion-area.yaml": """semantic_id: "MAT.ALG.CUADRADO_TRINOMIO.REPRESENTACION_AREA"
titulo: "Interpretación geométrica del cuadrado de trinomio"
objetivo: "Visualizar el cuadrado de trinomio como el área de un cuadrado fraccionado en 9 regiones."
introduccion: "Un cuadrado dividido en 3 partes por lado genera 9 zonas. ¡Ahí están los términos de nuestra fórmula!"
resumen: |
  Si un cuadrado de lado $(a+b+c)$ se subdivide, obtenemos:
  - 3 cuadrados perfectos en la diagonal ($a^2, b^2, c^2$).
  - 6 rectángulos que se agrupan en pares iguales ($2ab, 2ac, 2bc$).
explicacion: |
  El área total es $(a+b+c)^2$. Al sumar las 9 áreas interiores, demostramos la fórmula algebraica.
procedimiento: |
  Para asociar un área, cuenta las piezas. Habrá siempre 3 cuadrados y 3 pares de rectángulos.
ejemplos:
  - titulo: "Suma de áreas"
    enunciado: "Si divides un lado en $1, 2$ y $x$, ¿qué áreas se forman al proyectar sobre el cuadrado?"
    solucion_pasos:
      - "Lado $= (1+2+x) = (x+3)$."
      - "Áreas diagonales: $1^2=1$, $2^2=4$, $x^2$."
      - "Áreas cruzadas (x2): $1\\cdot2 = 2$; $1\\cdot x = x$; $2\\cdot x = 2x$."
      - "Al doblarlas: $4, 2x, 4x$."
      - "Total: $x^2 + 6x + 9$. Que equivale a $(x+3)^2$."
errores_frecuentes:
  - "Pensar que un trinomio al cuadrado solo tiene 3 partes en su interior."
""",
        "mat-alg-cuadrado-trinomio-omision-productos-dobles.yaml": """semantic_id: "MAT.ALG.CUADRADO_TRINOMIO.OMISION_PRODUCTOS_DOBLES"
titulo: "Detección de error por omisión de productos dobles"
objetivo: "Evitar la tentación de simplificar $(a+b+c)^2$ a solo $a^2+b^2+c^2$."
introduccion: "Si el error de omisión era malo con binomios, ¡con trinomios omites 3 términos completos!"
resumen: |
  El desarrollo correcto tiene $6$ sumandos. Omitir los productos cruzados asumiendo que $(a+b+c)^2 = a^2+b^2+c^2$ es un error conceptual grave de distribución de potencias en sumas.
explicacion: |
  Numéricamente: $(1+1+1)^2 = 3^2 = 9$.
  Forma mala: $1^2+1^2+1^2 = 3$.
  ¡Faltan $6$ unidades! (Que son precisamente $2(1)(1) + 2(1)(1) + 2(1)(1) = 6$).
procedimiento: |
  Al auditar cálculos ajenos, cuenta cuántos términos se generaron al desarrollar un trinomio al cuadrado. Deben ser 6 antes de reducir términos semejantes.
ejemplos:
  - titulo: "Auditoría"
    enunciado: "Detecta el error en: $(x-y-1)^2 = x^2 - y^2 + 1$."
    solucion_pasos:
      - "Primero, el cuadrado de $-y$ debe ser $+y^2$."
      - "Segundo, faltan todos los productos cruzados: $-2xy$, $-2x$, $+2y$."
errores_frecuentes:
  - "Olvidar los productos cruzados."
"""
    }

    exercises = []
    
    # 1. DIFERENCIA DEFINICION
    sid = "MAT.ALG.CUBO_BINOMIO.DIFERENCIA_DEFINICION"
    exercises.append({"stable_id": "CB-DD-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Qué indica el exponente $3$ en la expresión $(x-y)^3$?", "choices": ["A) Que el binomio $(x-y)$ se multiplica por sí mismo tres veces.", "B) Que cada término debe elevarse al cubo por separado.", "C) Que el resultado tendrá siempre 3 términos.", "D) Que es el triple del binomio."], "correct_answer": "A) Que el binomio $(x-y)$ se multiplica por sí mismo tres veces.", "solution_steps": "Definición básica de potencia.", "paes_style": False})
    
    # 2. REGLA SUMA
    sid = "MAT.ALG.CUBO_BINOMIO.REGLA_SUMA"
    exercises.append({"stable_id": "CB-RS-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Desarrolla $(m+2)^3$.", "choices": ["A) $m^3 + 6m^2 + 12m + 8$", "B) $m^3 + 8$", "C) $m^3 + 2m^2 + 4m + 8$", "D) $m^3 + 3m^2 + 6m + 8$"], "correct_answer": "A) $m^3 + 6m^2 + 12m + 8$", "solution_steps": "Aplicando $a^3 + 3a^2b + 3ab^2 + b^3$ con $a=m, b=2$.", "paes_style": False})

    # 3. REGLA DIFERENCIA
    sid = "MAT.ALG.CUBO_BINOMIO.REGLA_DIFERENCIA"
    exercises.append({"stable_id": "CB-RD-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Desarrolla $(2p - 1)^3$.", "choices": ["A) $8p^3 - 12p^2 + 6p - 1$", "B) $8p^3 - 6p^2 + 6p - 1$", "C) $8p^3 - 1$", "D) $8p^3 + 12p^2 + 6p - 1$"], "correct_answer": "A) $8p^3 - 12p^2 + 6p - 1$", "solution_steps": "$(2p)^3 - 3(2p)^2(1) + 3(2p)(1)^2 - 1^3 = 8p^3 - 12p^2 + 6p - 1$.", "paes_style": False})

    # 4. MANEJO SIGNOS CUBO
    sid = "MAT.ALG.CUBO_BINOMIO.MANEJO_SIGNOS"
    exercises.append({"stable_id": "CB-MS-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "¿Es cierto que $(a-b)^3 = -(b-a)^3$?", "choices": ["A) Sí, porque la diferencia al cubo preserva el signo negativo que se factoriza al invertir el orden.", "B) No, son exactamente iguales sin el signo menos.", "C) Solo si $a=b$.", "D) No se puede saber."], "correct_answer": "A) Sí, porque la diferencia al cubo preserva el signo negativo que se factoriza al invertir el orden.", "solution_steps": "Al elevar a potencia impar, el factor $-1$ sale de la potencia: $((-1)(b-a))^3 = (-1)^3(b-a)^3 = -(b-a)^3$.", "paes_style": True})

    # 5. ERROR TERMINOS MIXTOS CUBO
    sid = "MAT.ALG.CUBO_BINOMIO.ERROR_TERMINOS_MIXTOS"
    exercises.append({"stable_id": "CB-ET-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M2", "prompt": "Al desarrollar $(x+1)^3$ un estudiante responde $x^3+1$. La diferencia numérica entre su respuesta y la respuesta correcta para $x=2$ es:", "choices": ["A) $18$", "B) $12$", "C) $6$", "D) $27$"], "correct_answer": "A) $18$", "solution_steps": "Forma correcta: $(2+1)^3 = 27$. Forma errónea: $2^3+1 = 9$. Diferencia $27-9 = 18$.", "paes_style": True})

    # 6. CUADRADO TRINOMIO REGLA
    sid = "MAT.ALG.CUADRADO_TRINOMIO.REGLA_GENERAL"
    exercises.append({"stable_id": "CT-RG-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el número de términos NO nulos y no semejantes en el desarrollo puro de $(x+y+z)^2$.", "choices": ["A) $6$", "B) $9$", "C) $3$", "D) $5$"], "correct_answer": "A) $6$", "solution_steps": "3 cuadrados perfectos y 3 dobles productos.", "paes_style": False})

    # 7. TRINOMIO MANEJO SIGNOS
    sid = "MAT.ALG.CUADRADO_TRINOMIO.MANEJO_SIGNOS"
    exercises.append({"stable_id": "CT-MS-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Si se desarrolla $(x - y - 1)^2$, ¿cuál es el coeficiente del término $xy$?", "choices": ["A) $-2$", "B) $2$", "C) $1$", "D) $-1$"], "correct_answer": "A) $-2$", "solution_steps": "El doble producto de $x$ y $-y$ es $2(x)(-y) = -2xy$. Coeficiente $-2$.", "paes_style": False})

    # 8. TRINOMIO REPRESENTACION AREA
    sid = "MAT.ALG.CUADRADO_TRINOMIO.REPRESENTACION_AREA"
    exercises.append({"stable_id": "CT-RA-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Si visualizas $(a+b+c)^2$ como un cuadrado de área, los tres cuadrados perfectos $a^2, b^2, c^2$ se ubican geométricamente:", "choices": ["A) A lo largo de la diagonal principal del cuadrado grande.", "B) Todos en una misma esquina.", "C) Formando un triángulo central.", "D) Repartidos en las 4 esquinas."], "correct_answer": "A) A lo largo de la diagonal principal del cuadrado grande.", "solution_steps": "Al cruzar las líneas en el dibujo, los cuadrados siempre quedan alineados en diagonal.", "paes_style": False})

    # 9. TRINOMIO OMISION PRODUCTOS
    sid = "MAT.ALG.CUADRADO_TRINOMIO.OMISION_PRODUCTOS_DOBLES"
    exercises.append({"stable_id": "CT-OP-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "¿Cuántos términos omite el estudiante que asume que $(x+y+z)^2 = x^2+y^2+z^2$?", "choices": ["A) Omite $3$ términos.", "B) Omite $1$ término.", "C) Omite $6$ términos.", "D) No omite ninguno."], "correct_answer": "A) Omite $3$ términos.", "solution_steps": "Faltan los 3 dobles productos ($2xy, 2xz, 2yz$).", "paes_style": True})

    # Write files
    for yaml_filename, yaml_content in YAMLS.items():
        with open(f"docs/conocimiento/contenido/{yaml_filename}", "w", encoding="utf-8") as f:
            f.write(yaml_content)
    print(f"Creados {len(YAMLS)} yamls T4...")
    
    jsonl_filename = "docs/conocimiento/ejercicios/mat-alg-productos-notables-banco-gen-4.jsonl"
    with open(jsonl_filename, "w", encoding="utf-8") as f:
        for ex in exercises:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"{jsonl_filename} con {len(exercises)} ejercicios T4")

if __name__ == "__main__":
    generate_exercises()

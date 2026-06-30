import json
import os
import textwrap

def generate_yaml(semantic_id, data):
    filename = semantic_id.replace("MAT.ALG.", "mat-alg-").replace(".", "-").replace("_", "-").lower() + ".yaml"
    filepath = os.path.join("docs", "conocimiento", "contenido", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f'semantic_id: "{semantic_id}"\n')
        for key, value in data.items():
            if isinstance(value, str) and '\n' in value:
                f.write(f'{key}: |\n')
                f.write(textwrap.indent(value, '  ') + '\n')
            elif isinstance(value, list):
                f.write(f'{key}:\n')
                for item in value:
                    if isinstance(item, dict):
                        f.write(f'  - title: "{item["title"]}"\n')
                        f.write(f'    text: "{item["text"]}"\n')
                        f.write(f'    steps:\n')
                        for step in item["steps"]:
                            f.write(f'      - "{step}"\n')
                    else:
                        f.write(f'  - "{item}"\n')
            else:
                f.write(f'{key}: "{value}"\n')
    print(f"Generado {filepath}")

def generate_exercises():
    exercises = []
    
    # 1. CUADRADO_BINOMIO.SUMA_DEFINICION
    sid = "MAT.ALG.CUADRADO_BINOMIO.SUMA_DEFINICION"
    generate_yaml(sid, {
        "titulo": "Definición del cuadrado de un binomio (Suma)",
        "objetivo": "Comprender e interpretar algebraicamente el concepto del cuadrado de un binomio en su forma de suma $(a+b)^2$.",
        "introduccion": "Elevar una suma al cuadrado aparece en muchas aplicaciones. ¿Es lo mismo sumar primero y luego elevar al cuadrado, que hacerlo al revés? ¡Vamos a definirlo formalmente!",
        "resumen": "El cuadrado de un binomio suma se define como la multiplicación del binomio por sí mismo: $(a+b)^2 = (a+b)(a+b)$.\nEsta expresión NO equivale simplemente a la suma de los cuadrados $a^2 + b^2$.",
        "explicacion": "El exponente $2$ indica que la base $(a+b)$ se usa como factor dos veces. Al aplicar la propiedad distributiva a $(a+b)(a+b)$, obtenemos cuatro términos: $a^2 + ab + ba + b^2$. Puesto que $ab$ y $ba$ son términos semejantes y equivalentes, esto se reduce a $a^2 + 2ab + b^2$.\nEsto significa que siempre que elevemos un binomio al cuadrado, aparecerá un 'término central' o doble producto que muchas veces se omite por error.",
        "procedimiento": "Para entender la definición:\n1. Identifica la expresión como una potencia con base binomio y exponente 2.\n2. Descomponla en factores repetidos: $(A+B)(A+B)$.\n3. Reconoce que desarrollar esto producirá términos cruzados.",
        "ejemplos": [
            {
                "title": "Expansión conceptual",
                "text": "Expresa conceptualmente qué significa $(3x + 5y)^2$.",
                "steps": [
                    "Identificamos que la base es $3x + 5y$.",
                    "Significa $(3x + 5y)(3x + 5y)$."
                ]
            }
        ],
        "errores_frecuentes": [
            "Pensar que el exponente se distribuye sobre la suma: $(a+b)^2 = a^2 + b^2$."
        ]
    })
    exercises.append({"stable_id": "PN-CBS-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Cuál es el significado algebraico correcto de $(m + n)^2$?", "choices": ["A) $(m + n)(m + n)$", "B) $m^2 + n^2$", "C) $2(m + n)$", "D) $m^2 + m + n + n^2$"], "correct_answer": "A) $(m + n)(m + n)$", "solution_steps": "El exponente $2$ significa multiplicar la base por sí misma dos veces.", "paes_style": False})
    exercises.append({"stable_id": "PN-CBS-CONC-2", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "¿Por qué $(a+b)^2$ no es igual a $a^2+b^2$ en general (para $a,b \\neq 0$)?", "choices": ["A) Porque falta incluir los productos cruzados $ab$ y $ba$.", "B) Porque el exponente $2$ solo afecta a la primera variable.", "C) Porque la suma se convierte en resta.", "D) Sí son iguales, es una propiedad válida."], "correct_answer": "A) Porque falta incluir los productos cruzados $ab$ y $ba$.", "solution_steps": "Al distribuir $(a+b)(a+b)$ se obtienen $a^2 + ab + ba + b^2$. El término extra es $2ab$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CBS-CONC-3", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Un estudiante calcula $(3+4)^2$ como $3^2 + 4^2 = 9 + 16 = 25$. ¿Cuál es el error en este razonamiento usando aritmética?", "choices": ["A) Ignoró que primero debe sumar $3+4=7$ y $7^2 = 49$, mostrando que falta el $2ab$ ($2 \\cdot 3 \\cdot 4 = 24$).", "B) Ningún error, $25$ es la respuesta correcta.", "C) Debió multiplicar $3 \\cdot 4 = 12$ y elevar a $2$.", "D) El cálculo de $3^2$ está mal."], "correct_answer": "A) Ignoró que primero debe sumar $3+4=7$ y $7^2 = 49$, mostrando que falta el $2ab$ ($2 \\cdot 3 \\cdot 4 = 24$).", "solution_steps": "$49 = 25 + 24$. El $24$ corresponde precisamente al $2ab$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CBS-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Identifica la expresión equivalente a multiplicar el binomio $(2x + 3)$ por sí mismo.", "choices": ["A) $(2x + 3)^2$", "B) $2(2x + 3)$", "C) $(2x)^2 + 3^2$", "D) $(2x + 3)(2x - 3)$"], "correct_answer": "A) $(2x + 3)^2$", "solution_steps": "Multiplicar algo por sí mismo se denota con el exponente $2$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CBS-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Expande $(x + 5)^2$ utilizando su definición paso a paso: $(x + 5)(x + 5)$. ¿Cuáles son los cuatro términos antes de reducir?", "choices": ["A) $x^2 + 5x + 5x + 25$", "B) $x^2 + 10x + 25$", "C) $x^2 + 25x + x + 25$", "D) $x^2 + 5x + 25$"], "correct_answer": "A) $x^2 + 5x + 5x + 25$", "solution_steps": "Distribuyendo FOIL: Firsts ($x^2$), Outers ($5x$), Inners ($5x$), Lasts ($25$).", "paes_style": False})
    exercises.append({"stable_id": "PN-CBS-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Si expandes $(3p + q)^2$ como producto, ¿cuáles son los términos semejantes que se suman al medio?", "choices": ["A) $3pq$ y $3pq$", "B) $3pq$ y $qp$", "C) $6pq$ y $6pq$", "D) $p^2$ y $q^2$"], "correct_answer": "A) $3pq$ y $3pq$", "solution_steps": "$(3p)(q) = 3pq$ y $(q)(3p) = 3pq$. Ambos son semejantes y suman $6pq$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CBS-PROC-3", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Usa la definición de cuadrado de binomio en $(a^2 + b^3)^2$ para encontrar el término de mayor grado total.", "choices": ["A) $b^6$", "B) $a^4$", "C) $a^2b^3$", "D) $a^4 + b^6$"], "correct_answer": "A) $b^6$", "solution_steps": "Los términos serán $a^4$, $a^2b^3$, $b^6$. Grados totales: 4, 5, y 6 respectivamente. El mayor es $b^6$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CBS-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M2", "prompt": "Si $(x + y)^2 = 100$ y se sabe que $x^2 + y^2 = 68$, ¿cuál es el valor del producto $xy$?", "choices": ["A) $16$", "B) $32$", "C) $10$", "D) $8$"], "correct_answer": "A) $16$", "solution_steps": "$(x+y)^2 = x^2 + 2xy + y^2 = 100$. Sabemos $x^2 + y^2 = 68$. $68 + 2xy = 100 \\Rightarrow 2xy = 32 \\Rightarrow xy = 16$.", "paes_style": True})
    exercises.append({"stable_id": "PN-CBS-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Dada la igualdad $(2x + k)^2 = 4x^2 + 12x + 9$ obtenida por definición. ¿Cuál es el valor positivo de $k$?", "choices": ["A) $3$", "B) $9$", "C) $6$", "D) $1.5$"], "correct_answer": "A) $3$", "solution_steps": "El último término es $k^2 = 9 \\Rightarrow k = 3$. Comprobación término central: $2(2x)(3) = 12x$.", "paes_style": True})
    exercises.append({"stable_id": "PN-CBS-PAES-3", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Se tiene que $P = (a + 2b)^2$. Si se expande $P$ usando la definición $(a+2b)(a+2b)$ y luego se duplica el valor de $a$ (es decir, $a$ cambia a $2a$), ¿cómo cambia el valor numérico del término central del desarrollo original?", "choices": ["A) Se duplica.", "B) Se cuadruplica.", "C) Queda igual.", "D) Se reduce a la mitad."], "correct_answer": "A) Se duplica.", "solution_steps": "El término central original es $a(2b) + (2b)a = 4ab$. Si cambiamos $a$ por $2a$, el nuevo término será $4(2a)b = 8ab$, que es el doble de $4ab$.", "paes_style": True})

    # 2. SUMA_DIFERENCIA.DEFINICION_CONJUGADOS
    sid = "MAT.ALG.SUMA_DIFERENCIA.DEFINICION_CONJUGADOS"
    generate_yaml(sid, {
        "titulo": "Definición de binomios conjugados",
        "objetivo": "Comprender el concepto de binomios conjugados y su estructura fundamental.",
        "introduccion": "¿Qué tienen de especial dos binomios que son casi iguales pero difieren solo en un signo? A esta pareja le llamamos 'conjugados'.",
        "resumen": "Dos binomios son conjugados cuando contienen exactamente los mismos términos, pero difieren únicamente en el signo que los separa en medio.\nEjemplo clásico: $(a+b)$ y $(a-b)$ son conjugados entre sí.",
        "explicacion": "La suma por su diferencia es el producto notable que surge al multiplicar dos binomios conjugados: $(A+B)(A-B)$.\nLa característica definitoria de los conjugados es que un término mantiene su signo intacto en ambos binomios (en este caso $A$), mientras que el otro término tiene signos opuestos en cada binomio ($+B$ y $-B$).\nAl multiplicarlos, la magia ocurre: los productos cruzados se cancelan ($AB - AB = 0$), dejando solo la diferencia de los cuadrados.",
        "procedimiento": "Para verificar si dos factores forman una suma por diferencia (son conjugados):\n1. Revisa que ambos binomios tengan los mismos valores absolutos (las mismas letras y números).\n2. Asegúrate de que un término tenga el mismo signo en ambos paréntesis.\n3. Asegúrate de que el otro término tenga signos contrarios (uno positivo y uno negativo).",
        "ejemplos": [
            {
                "title": "Identificando conjugados",
                "text": "¿Son $(3x + 2y)$ y $(3x - 2y)$ conjugados?",
                "steps": [
                    "Ambos tienen los términos $3x$ y $2y$.",
                    "El término $3x$ es positivo en ambos.",
                    "El término $2y$ es positivo en el primero y negativo en el segundo.",
                    "Sí son conjugados."
                ]
            }
        ],
        "errores_frecuentes": [
            "Creer que $(a-b)$ y $(b-a)$ son conjugados. ¡No lo son! Son inversos aditivos. Los conjugados deben mantener un término idéntico."
        ]
    })
    exercises.append({"stable_id": "PN-SD-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Cuál de las siguientes parejas de binomios son conjugados?", "choices": ["A) $(x + 5)$ y $(x - 5)$", "B) $(x + 5)$ y $(5 - x)$", "C) $(x - 5)$ y $(x - 5)$", "D) $(-x + 5)$ y $(x - 5)$"], "correct_answer": "A) $(x + 5)$ y $(x - 5)$", "solution_steps": "Para ser conjugados, deben tener los mismos términos y diferir solo en el signo central.", "paes_style": False})
    exercises.append({"stable_id": "PN-SD-CONC-2", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Si multiplicas dos binomios conjugados usando distribución paso a paso, ¿por qué el resultado es un binomio y no un trinomio?", "choices": ["A) Porque los productos cruzados son inversos aditivos y suman cero.", "B) Porque el término independiente se vuelve cero.", "C) Porque los cuadrados se cancelan.", "D) Porque uno de los factores es cero."], "correct_answer": "A) Porque los productos cruzados son inversos aditivos y suman cero.", "solution_steps": "Los cruzados son $+ab$ y $-ab$, cuya suma es $0$.", "paes_style": False})
    exercises.append({"stable_id": "PN-SD-CONC-3", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Considera $(-a - b)$ y $(-a + b)$. ¿Son binomios conjugados? ¿Por qué?", "choices": ["A) Sí, porque el término $-a$ es idéntico en ambos, y el término $b$ cambia de signo.", "B) No, porque empiezan con signo negativo.", "C) No, porque no forman una suma por diferencia tradicional $(a+b)(a-b)$.", "D) Sí, porque si factorizamos el signo menos, son iguales."], "correct_answer": "A) Sí, porque el término $-a$ es idéntico en ambos, y el término $b$ cambia de signo.", "solution_steps": "Cumplen la definición estricta: un término constante $(-a)$ y uno con signo alternado $(\\pm b)$.", "paes_style": False})
    exercises.append({"stable_id": "PN-SD-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El conjugado del binomio $(4m - 7n)$ es:", "choices": ["A) $(4m + 7n)$", "B) $(-4m - 7n)$", "C) $(7n - 4m)$", "D) $(-4m + 7n)$"], "correct_answer": "A) $(4m + 7n)$", "solution_steps": "Solo se cambia el signo intermedio.", "paes_style": False})
    exercises.append({"stable_id": "PN-SD-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Aplica distribución a los conjugados $(y + 8)(y - 8)$ para encontrar los términos que se cancelan.", "choices": ["A) $-8y$ y $+8y$", "B) $y^2$ y $-64$", "C) $-8y^2$ y $+8y^2$", "D) $+8$ y $-8$"], "correct_answer": "A) $-8y$ y $+8y$", "solution_steps": "Cruzados: $(y)(-8) = -8y$. $(8)(y) = 8y$.", "paes_style": False})
    exercises.append({"stable_id": "PN-SD-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Demuestra algebraicamente la multiplicación de conjugados: expande $(p + q)(p - q)$.", "choices": ["A) $p^2 - q^2$", "B) $p^2 + q^2$", "C) $p^2 - 2pq - q^2$", "D) $p^2 - 2pq + q^2$"], "correct_answer": "A) $p^2 - q^2$", "solution_steps": "$p(p) + p(-q) + q(p) + q(-q) = p^2 - pq + pq - q^2 = p^2 - q^2$.", "paes_style": False})
    exercises.append({"stable_id": "PN-SD-PROC-3", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Si el conjugado de $(3x + A)$ es $(3x - 5)$, ¿cuál es el valor de $A$?", "choices": ["A) $5$", "B) $-5$", "C) $3$", "D) $-3$"], "correct_answer": "A) $5$", "solution_steps": "El conjugado de $(3x + 5)$ es $(3x - 5)$, luego $A=5$.", "paes_style": False})
    exercises.append({"stable_id": "PN-SD-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M2", "prompt": "Sean $u$ y $v$ dos binomios conjugados tales que $u = (2x + 3)$. Si $u \\cdot v = 4x^2 - 9$, entonces la expresión $u + v$ es igual a:", "choices": ["A) $4x$", "B) $6$", "C) $4x + 6$", "D) $0$"], "correct_answer": "A) $4x$", "solution_steps": "$u = 2x+3$, luego $v = 2x-3$. Su suma es $(2x+3) + (2x-3) = 4x$.", "paes_style": True})
    exercises.append({"stable_id": "PN-SD-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Si restamos dos binomios conjugados $(ax+b) - (ax-b)$, obtenemos:", "choices": ["A) $2b$", "B) $2ax$", "C) $0$", "D) $2ax + 2b$"], "correct_answer": "A) $2b$", "solution_steps": "$ax + b - ax + b = 2b$.", "paes_style": True})
    exercises.append({"stable_id": "PN-SD-PAES-3", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "En la expresión $(x^2 - 4)$, ¿cuáles son los conjugados algebraicos cuya multiplicación genera este binomio?", "choices": ["A) $(x - 2)$ y $(x + 2)$", "B) $(x - 4)$ y $(x + 4)$", "C) $(x^2 - 2)$ y $(x^2 + 2)$", "D) $(x - 2)^2$"], "correct_answer": "A) $(x - 2)$ y $(x + 2)$", "solution_steps": "Es una diferencia de cuadrados. $x^2 - 2^2 = (x - 2)(x + 2)$.", "paes_style": True})

    # 3. TERMINO_COMUN.DEFINICION
    sid = "MAT.ALG.TERMINO_COMUN.DEFINICION"
    generate_yaml(sid, {
        "titulo": "Definición del producto de binomios con término común",
        "objetivo": "Comprender la estructura base de multiplicar dos binomios que comparten exactamente un término común.",
        "introduccion": "Ya vimos qué pasa si multiplicamos dos binomios iguales (cuadrado) y dos conjugados. ¿Qué pasa si comparten solo la mitad de la estructura? Por ejemplo: $(x+5)(x+3)$.",
        "resumen": "Un par de binomios con un 'término común' tienen la forma $(x+a)(x+b)$.\nAquí, la $x$ representa el término común (idéntico en ambos binomios), mientras que $a$ y $b$ son los términos no comunes (distintos).",
        "explicacion": "Al expandir $(x+a)(x+b)$ obtenemos cuatro partes: $x^2 + bx + ax + ab$. \nComo $bx$ y $ax$ son términos semejantes (ambos comparten la $x$), los agrupamos factorizando: $x^2 + (a+b)x + ab$.\nEsta estructura nos enseña que el coeficiente del término común en el resultado provendrá de la SUMA de los no comunes ($a+b$), y el término independiente provendrá del PRODUCTO de los no comunes ($ab$).",
        "procedimiento": "Para reconocer este producto notable:\n1. Revisa el primer término de ambos binomios. ¿Son idénticos? Ese es el término común.\n2. Revisa los segundos términos. ¿Son diferentes numéricamente? Esos son los no comunes.\n3. Entiende que el desarrollo ordenará los términos según las potencias del término común.",
        "ejemplos": [
            {
                "title": "Identificando las partes",
                "text": "En el producto $(y - 4)(y + 7)$, identifica el término común y los no comunes.",
                "steps": [
                    "El término común es $y$.",
                    "Los términos no comunes son $-4$ y $+7$."
                ]
            }
        ],
        "errores_frecuentes": [
            "Creer que $(x+a)(x+b) = x^2 + ab$, ignorando por completo la suma cruzada $(a+b)x$."
        ]
    })
    exercises.append({"stable_id": "PN-TC-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Qué caracteriza a un producto de binomios con un término común?", "choices": ["A) Ambos binomios tienen un término exactamente igual, y el otro diferente.", "B) Ambos binomios son iguales.", "C) Tienen los mismos términos con signo distinto.", "D) Tienen una variable en común pero coeficientes diferentes."], "correct_answer": "A) Ambos binomios tienen un término exactamente igual, y el otro diferente.", "solution_steps": "Como su nombre indica, comparten solo un término (ej: la variable) mientras que los números libres varían.", "paes_style": False})
    exercises.append({"stable_id": "PN-TC-CONC-2", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Al desarrollar $(x+a)(x+b)$, ¿de dónde proviene el término central $(a+b)x$?", "choices": ["A) De la suma de los productos cruzados del término común con cada término no común.", "B) De multiplicar los términos no comunes.", "C) De sumar los binomios.", "D) Del cuadrado del término común."], "correct_answer": "A) De la suma de los productos cruzados del término común con cada término no común.", "solution_steps": "$ax + bx = (a+b)x$.", "paes_style": False})
    exercises.append({"stable_id": "PN-TC-CONC-3", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "¿Puede el término común ser algo diferente a una simple variable, como por ejemplo $3x^2$?", "choices": ["A) Sí, el término común puede ser cualquier expresión algebraica idéntica en ambos paréntesis.", "B) No, siempre debe ser $x$.", "C) No, solo pueden ser variables lineales.", "D) Sí, pero no se aplica la misma fórmula."], "correct_answer": "A) Sí, el término común puede ser cualquier expresión algebraica idéntica en ambos paréntesis.", "solution_steps": "Ej: $(3x^2 + 2)(3x^2 + 5)$ es un producto con término común $3x^2$.", "paes_style": False})
    exercises.append({"stable_id": "PN-TC-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Identifica los términos no comunes en el producto $(w - 9)(w + 12)$.", "choices": ["A) $-9$ y $+12$", "B) $w$ y $-9$", "C) $9$ y $12$", "D) $w$ y $w$"], "correct_answer": "A) $-9$ y $+12$", "solution_steps": "El término común es $w$, los diferentes son los números con su signo.", "paes_style": False})
    exercises.append({"stable_id": "PN-TC-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el coeficiente del término en $x$ al expandir $(x + 6)(x - 2)$ usando la definición.", "choices": ["A) $4$", "B) $-12$", "C) $8$", "D) $12$"], "correct_answer": "A) $4$", "solution_steps": "El coeficiente lineal es la suma de los no comunes: $6 + (-2) = 4$.", "paes_style": False})
    exercises.append({"stable_id": "PN-TC-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Encuentra el producto de los términos no comunes en $(x - 5)(x - 7)$.", "choices": ["A) $35$", "B) $-35$", "C) $-12$", "D) $12$"], "correct_answer": "A) $35$", "solution_steps": "$(-5) \\cdot (-7) = 35$.", "paes_style": False})
    exercises.append({"stable_id": "PN-TC-PROC-3", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Si $(x+a)(x+b) = x^2 - 2x - 15$, ¿cuál es el valor de $a+b$?", "choices": ["A) $-2$", "B) $-15$", "C) $2$", "D) $15$"], "correct_answer": "A) $-2$", "solution_steps": "La suma $a+b$ es el coeficiente del término medio, que es $-2$.", "paes_style": False})
    exercises.append({"stable_id": "PN-TC-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M2", "prompt": "Si el término libre (independiente) de $(x+k)(x-5)$ es $-40$, ¿cuál es el coeficiente de $x$ en el resultado?", "choices": ["A) $3$", "B) $8$", "C) $-13$", "D) $13$"], "correct_answer": "A) $3$", "solution_steps": "Producto libres: $k(-5) = -40 \Rightarrow k=8$. Suma de libres (coef. lineal): $8 + (-5) = 3$.", "paes_style": True})
    exercises.append({"stable_id": "PN-TC-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "El área de un rectángulo está dada por el producto $(x+p)(x+q)$. Si el área se expresa como $x^2 + 10x + 21$, ¿cuánto vale $p^2 + q^2$ asumiendo que $p$ y $q$ son positivos?", "choices": ["A) $58$", "B) $100$", "C) $49$", "D) $9$"], "correct_answer": "A) $58$", "solution_steps": "$p+q = 10$, $pq = 21$. O buscamos los números ($7$ y $3$) y sumamos $7^2 + 3^2 = 49 + 9 = 58$, o $(p+q)^2 - 2pq = 100 - 42 = 58$.", "paes_style": True})
    exercises.append({"stable_id": "PN-TC-PAES-3", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Si un trinomio se genera a partir de binomios con término común $(x+a)(x+b)$, y resulta que $a$ y $b$ son opuestos aditivos ($b = -a$), ¿en qué otro producto notable se transforma?", "choices": ["A) Suma por su diferencia.", "B) Cuadrado de binomio.", "C) Cubo de binomio.", "D) Binomio de Newton."], "correct_answer": "A) Suma por su diferencia.", "solution_steps": "Si $b = -a$, los binomios son $(x+a)(x-a)$, que es la definición de suma por diferencia (conjugados).", "paes_style": True})

    # 4. CUBO_BINOMIO.SUMA_DEFINICION
    sid = "MAT.ALG.CUBO_BINOMIO.SUMA_DEFINICION"
    generate_yaml(sid, {
        "titulo": "Definición del cubo de un binomio (Suma)",
        "objetivo": "Comprender algebraicamente qué significa elevar un binomio al cubo y visualizar su expansión.",
        "introduccion": "Si elevar al cuadrado era multiplicar la base dos veces, el cubo significa multiplicarla tres veces. $(a+b)^3$ no es simplemente $a^3 + b^3$. ¡Veamos por qué!",
        "resumen": "El cubo de un binomio suma se define como: $(a+b)^3 = (a+b)(a+b)(a+b)$.\nTambién se puede pensar como $(a+b)^2 (a+b)$. Al desarrollarlo por completo, el resultado siempre arroja cuatro términos.",
        "explicacion": "Vamos a expandirlo usando propiedades:\n1. Ya sabemos que $(a+b)^2 = a^2 + 2ab + b^2$.\n2. Multiplicamos esto por el tercer $(a+b)$: $(a^2 + 2ab + b^2)(a + b)$.\n3. Al distribuir, obtenemos $a^3 + a^2b + 2a^2b + 2ab^2 + ab^2 + b^3$.\n4. Agrupando términos semejantes, llegamos al desarrollo canónico: $a^3 + 3a^2b + 3ab^2 + b^3$.\nAparecen términos combinados triples porque los componentes interactúan en tres dimensiones (conceptualmente, como el volumen de un cubo).",
        "procedimiento": "Para interiorizar la definición:\n1. Recuerda que el exponente 3 manda a repetir el factor tres veces.\n2. La expansión completa generará potencias descendentes para $a$ ($a^3, a^2, a^1, a^0$) y ascendentes para $b$ ($b^0, b^1, b^2, b^3$).\n3. Los coeficientes intermedios, por distribución y agrupación, siempre suman 3.",
        "ejemplos": [
            {
                "title": "Asociación por partes",
                "text": "Expresa $(2x+y)^3$ como el producto de un binomio al cuadrado por el binomio.",
                "steps": [
                    "$(2x+y)^3 = (2x+y)^2 \\cdot (2x+y)$",
                    "Esta forma es útil para evitar distribuir tres veces seguidas a ciegas."
                ]
            }
        ],
        "errores_frecuentes": [
            "Afirmar que $(a+b)^3 = a^3 + b^3$, ignorando por completo los términos centrales cruzados."
        ]
    })
    exercises.append({"stable_id": "PN-CB-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿A qué equivale algebraicamente $(m+n)^3$ según su definición básica?", "choices": ["A) $(m+n)(m+n)(m+n)$", "B) $m^3 + n^3$", "C) $3(m+n)$", "D) $(m+n)(m^2+n^2)$"], "correct_answer": "A) $(m+n)(m+n)(m+n)$", "solution_steps": "El exponente $3$ repite el factor tres veces mediante multiplicación.", "paes_style": False})
    exercises.append({"stable_id": "PN-CB-CONC-2", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Al expandir $(a+b)^3$, ¿cuántos términos aparecen antes de reducir los términos semejantes?", "choices": ["A) $8$ términos.", "B) $4$ términos.", "C) $6$ términos.", "D) $2$ términos."], "correct_answer": "A) $8$ términos.", "solution_steps": "Si multiplicas sin reducir, el primer par da 4 términos, y al multiplicar por el tercero (2) da $4 \\times 2 = 8$ términos (e.g. $a^3, a^2b, aba, \dots$).", "paes_style": False})
    exercises.append({"stable_id": "PN-CB-CONC-3", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "En la expansión final de $(a+b)^3$, que es $a^3 + 3a^2b + 3ab^2 + b^3$, ¿de dónde sale el número $3$ en los términos centrales?", "choices": ["A) De sumar tres términos semejantes que aparecen al distribuir.", "B) Porque el exponente original es $3$.", "C) De multiplicar $a$ y $b$ por $3$.", "D) Es un número aleatorio."], "correct_answer": "A) De sumar tres términos semejantes que aparecen al distribuir.", "solution_steps": "Por ejemplo, aparece $a^2b$ y también $2a^2b$ desde el producto del cuadrado de binomio. Sumados dan $3a^2b$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CB-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Otra forma válida de escribir la definición de $(x+1)^3$ es:", "choices": ["A) $(x+1)^2(x+1)$", "B) $x^3+1^3$", "C) $(x^3+1)$", "D) $(x+1)(x+2)$"], "correct_answer": "A) $(x+1)^2(x+1)$", "solution_steps": "Por propiedades de potencias, separar exponente 3 en $2$ y $1$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CB-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Si $(a+b)^2 = a^2 + 2ab + b^2$, usa esta información para calcular el producto parcial de $a \\cdot (a^2 + 2ab + b^2)$ (solo el primer paso de expandir al cubo).", "choices": ["A) $a^3 + 2a^2b + ab^2$", "B) $a^3 + 2ab^2 + b^3$", "C) $a^3 + a^2b + b^2$", "D) $a^3 + 3a^2b + 3ab^2$"], "correct_answer": "A) $a^3 + 2a^2b + ab^2$", "solution_steps": "Distribuir $a$: $a(a^2) = a^3$, $a(2ab) = 2a^2b$, $a(b^2) = ab^2$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CB-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Suma el resultado anterior con el producto parcial de $b \\cdot (a^2 + 2ab + b^2)$ para hallar la expansión total.", "choices": ["A) $a^3 + 3a^2b + 3ab^2 + b^3$", "B) $a^3 + 2a^2b + 2ab^2 + b^3$", "C) $a^3 + b^3$", "D) $a^3 + 4a^2b + 4ab^2 + b^3$"], "correct_answer": "A) $a^3 + 3a^2b + 3ab^2 + b^3$", "solution_steps": "$b(a^2) = a^2b$, sumado a $2a^2b$ da $3a^2b$. $b(2ab)=2ab^2$, sumado a $ab^2$ da $3ab^2$. Y $b(b^2)=b^3$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CB-PROC-3", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "¿Cuál es la suma de los coeficientes de los cuatro términos en la expansión final de $(a+b)^3$?", "choices": ["A) $8$", "B) $4$", "C) $6$", "D) $3$"], "correct_answer": "A) $8$", "solution_steps": "Los coeficientes son $1, 3, 3, 1$. $1+3+3+1 = 8$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CB-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Si evaluamos mentalmente $(10+2)^3$, ¿cuál es el valor que aporta el término correspondiente a $3a^2b$ en la definición expandida (donde $a=10$, $b=2$)?", "choices": ["A) $600$", "B) $120$", "C) $300$", "D) $60$"], "correct_answer": "A) $600$", "solution_steps": "$3(10^2)(2) = 3(100)(2) = 600$.", "paes_style": True})
    exercises.append({"stable_id": "PN-CB-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Si $(x+y)^3 = A$, y un estudiante por error calcula $(x^3 + y^3) = B$. ¿A qué equivale la diferencia $A - B$?", "choices": ["A) $3xy(x+y)$", "B) $3x^2y^2$", "C) $3x^2y - 3xy^2$", "D) $xy(x+y)$"], "correct_answer": "A) $3xy(x+y)$", "solution_steps": "$A - B = (x^3+3x^2y+3xy^2+y^3) - (x^3+y^3) = 3x^2y + 3xy^2 = 3xy(x+y)$.", "paes_style": True})
    exercises.append({"stable_id": "PN-CB-PAES-3", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Un cubo geométrico tiene arista $(a+b)$. Su volumen se divide en 8 bloques rectangulares. ¿Cuántos bloques tienen dimensiones $a \\times a \\times b$ (volumen $a^2b$)?", "choices": ["A) $3$", "B) $1$", "C) $6$", "D) $2$"], "correct_answer": "A) $3$", "solution_steps": "El término en la expansión es $3a^2b$, lo que significa geométricamente 3 bloques con ese volumen.", "paes_style": True})

    # 5. CUADRADO_TRINOMIO.DEFINICION
    sid = "MAT.ALG.CUADRADO_TRINOMIO.DEFINICION"
    generate_yaml(sid, {
        "titulo": "Definición del cuadrado de un trinomio",
        "objetivo": "Comprender la expansión de un trinomio al cuadrado mediante la distribución y la agrupación de términos semejantes.",
        "introduccion": "Si elevar un binomio al cuadrado produce 3 términos, ¿cuántos términos produce elevar un polinomio de 3 términos (trinomio) al cuadrado? Es hora de descubrirlo.",
        "resumen": "El cuadrado de un trinomio se define como la multiplicación de un trinomio por sí mismo: $(a+b+c)^2 = (a+b+c)(a+b+c)$.\nLa fórmula final para su desarrollo incluye el cuadrado de cada término y todos los dobles productos posibles entre ellos.",
        "explicacion": "Al expandir $(a+b+c)(a+b+c)$ aplicando propiedad distributiva extensiva (cada término por todos los del otro), se generan $3 \\times 3 = 9$ términos en total.\nLos resultados son:\n- $a(a) + a(b) + a(c) = a^2 + ab + ac$\n- $b(a) + b(b) + b(c) = ab + b^2 + bc$\n- $c(a) + c(b) + c(c) = ac + bc + c^2$\nSumando todo y agrupando términos semejantes ($ab+ba=2ab$, etc.), obtenemos: $a^2 + b^2 + c^2 + 2ab + 2ac + 2bc$.\n¡Se eleva cada término al cuadrado y se suman los dobles de todas las combinaciones posibles de a dos términos!",
        "procedimiento": "Al resolver $(a+b+c)^2$ mentalmente o paso a paso:\n1. Escribe el cuadrado de cada uno de los tres términos (siempre serán positivos).\n2. Multiplica el 1º término por el 2º, y duplícalo.\n3. Multiplica el 1º por el 3º, y duplícalo.\n4. Multiplica el 2º por el 3º, y duplícalo.\n5. Suma todos estos elementos prestando especial atención a los signos originales de cada término.",
        "ejemplos": [
            {
                "title": "Verificando los 6 términos finales",
                "text": "Expande $(x+y+z)^2$.",
                "steps": [
                    "Cuadrados: $x^2 + y^2 + z^2$",
                    "Dobles productos: $2xy + 2xz + 2yz$",
                    "Final: $x^2 + y^2 + z^2 + 2xy + 2xz + 2yz$"
                ]
            }
        ],
        "errores_frecuentes": [
            "Dejar fuera algunos de los dobles productos combinados.",
            "Olvidar elevar al cuadrado alguno de los términos principales."
        ]
    })
    exercises.append({"stable_id": "PN-CT-CONC-1", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Cuántos términos sin reducir (antes de juntar semejantes) se generan al multiplicar $(a+b+c)(a+b+c)$?", "choices": ["A) $9$", "B) $6$", "C) $3$", "D) $12$"], "correct_answer": "A) $9$", "solution_steps": "Son $3$ términos del primero multiplicados por los $3$ términos del segundo: $3 \\times 3 = 9$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CT-CONC-2", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Después de agrupar los términos semejantes, ¿cuántos términos distintos quedan en la expansión de $(a+b+c)^2$?", "choices": ["A) $6$", "B) $9$", "C) $3$", "D) $5$"], "correct_answer": "A) $6$", "solution_steps": "Quedan 3 cuadrados y 3 dobles productos (que agruparon las 6 combinaciones cruzadas), sumando 6 términos en total.", "paes_style": False})
    exercises.append({"stable_id": "PN-CT-CONC-3", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "¿A qué se deben los tres dobles productos en el desarrollo de $(x+y+z)^2$?", "choices": ["A) Al hecho de que hay tres formas posibles de combinar dos letras distintas, y la multiplicación es conmutativa ($xy=yx, xz=zx, yz=zy$).", "B) A que el trinomio se multiplica por 2.", "C) A que faltan términos por calcular.", "D) Es solo una regla de memoria."], "correct_answer": "A) Al hecho de que hay tres formas posibles de combinar dos letras distintas, y la multiplicación es conmutativa ($xy=yx, xz=zx, yz=zy$).", "solution_steps": "Las parejas son {x,y}, {x,z} y {y,z}. Al multiplicar la tabla 3x3 aparecen ambos órdenes, sumando 2 de cada uno.", "paes_style": False})
    exercises.append({"stable_id": "PN-CT-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "La parte de los cuadrados en el desarrollo de $(m+n+p)^2$ es:", "choices": ["A) $m^2 + n^2 + p^2$", "B) $(m+n+p)^2$", "C) $m^3 + n^3 + p^3$", "D) $m^2n^2p^2$"], "correct_answer": "A) $m^2 + n^2 + p^2$", "solution_steps": "El desarrollo incluye los cuadrados individuales de cada término.", "paes_style": False})
    exercises.append({"stable_id": "PN-CT-PROC-1", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el coeficiente del término $xy$ en la expansión de $(x + 2y + z)^2$.", "choices": ["A) $4$", "B) $2$", "C) $1$", "D) $8$"], "correct_answer": "A) $4$", "solution_steps": "El doble producto es $2(x)(2y) = 4xy$. El coeficiente es 4.", "paes_style": False})
    exercises.append({"stable_id": "PN-CT-PROC-2", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Halla la suma de los tres términos correspondientes a los dobles productos en la expansión de $(1 + 2 + 3)^2$.", "choices": ["A) $22$", "B) $11$", "C) $36$", "D) $14$"], "correct_answer": "A) $22$", "solution_steps": "Las parejas son $1\\cdot2$, $1\\cdot3$, $2\\cdot3$. Los dobles son $2(2) + 2(3) + 2(6) = 4 + 6 + 12 = 22$. Comprobación: $(6)^2 - (1^2+2^2+3^2) = 36 - 14 = 22$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CT-PROC-3", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Al desarrollar $(a + b - c)^2$, ¿cuál es el doble producto entre el primer y tercer término?", "choices": ["A) $-2ac$", "B) $2ac$", "C) $-ac$", "D) $2a^2c^2$"], "correct_answer": "A) $-2ac$", "solution_steps": "$2(a)(-c) = -2ac$.", "paes_style": False})
    exercises.append({"stable_id": "PN-CT-PAES-1", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Si $(a+b+c)^2 = a^2+b^2+c^2$, ¿cuál de las siguientes afirmaciones sobre los números $a, b, c$ debe ser verdadera?", "choices": ["A) $ab + ac + bc = 0$", "B) $a=0$, $b=0$, $c=0$", "C) $a, b, c$ deben ser negativos.", "D) La ecuación no tiene solución en los reales."], "correct_answer": "A) $ab + ac + bc = 0$", "solution_steps": "La expansión es cuadrados + $2(ab+ac+bc)$. Si esto es igual a los cuadrados solamente, entonces $2(ab+ac+bc) = 0$, es decir, $ab+ac+bc=0$.", "paes_style": True})
    exercises.append({"stable_id": "PN-CT-PAES-2", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Se sabe que $x+y+z = 10$ y que $xy+xz+yz = 30$. ¿Cuál es el valor numérico de $x^2+y^2+z^2$?", "choices": ["A) $40$", "B) $100$", "C) $60$", "D) $70$"], "correct_answer": "A) $40$", "solution_steps": "$(x+y+z)^2 = x^2+y^2+z^2 + 2(xy+xz+yz)$. $100 = x^2+y^2+z^2 + 2(30) \\Rightarrow 100 = x^2+y^2+z^2 + 60 \\Rightarrow x^2+y^2+z^2 = 40$.", "paes_style": True})
    exercises.append({"stable_id": "PN-CT-PAES-3", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M2", "prompt": "Para reescribir $(x+y+z)^2$ como el cuadrado de un binomio, un estudiante asocia $(x+y)$ como un solo término $W$. Al hacer $(W+z)^2 = W^2 + 2Wz + z^2$ y volver a reemplazar $W$, ¿llega al desarrollo canónico del cuadrado de un trinomio?", "choices": ["A) Sí, este método de asociación produce exactamente el mismo resultado y demuestra la equivalencia.", "B) No, faltará un doble producto.", "C) No, los signos estarán invertidos.", "D) Sí, pero no aplicará para coeficientes distintos de 1."], "correct_answer": "A) Sí, este método de asociación produce exactamente el mismo resultado y demuestra la equivalencia.", "solution_steps": "$(x+y)^2 + 2(x+y)z + z^2 = (x^2+2xy+y^2) + (2xz+2yz) + z^2$. Reordenando quedan los 6 términos correctos.", "paes_style": True})

    jsonl_filename = "docs/conocimiento/ejercicios/mat-alg-productos-notables-banco-gen-1.jsonl"
    with open(jsonl_filename, "w", encoding="utf-8") as f:
        for ex in exercises:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"Generado {jsonl_filename}")

if __name__ == "__main__":
    generate_exercises()

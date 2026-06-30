# scratch/build_b0205_t5.py
import json
import yaml
from pathlib import Path

CONTENT_DIR = Path("docs/conocimiento/contenido")
EJERCICIOS_DIR = Path("docs/conocimiento/ejercicios")

def write_yaml(filename, data):
    with open(CONTENT_DIR / f"{filename}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

def append_jsonl(filename, items):
    with open(EJERCICIOS_DIR / f"{filename}.jsonl", "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

RECURSOS = []
EJERCICIOS = []

# 1. CONCEPTO_VARIABLES INVERSAS
sid1 = "MAT.NUM.PROP_INVERSA.CONCEPTO_VARIABLES"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Comprender el concepto de variables inversamente proporcionales.",
    "introduccion": "Imagina que debes pintar tu casa. Si lo haces solo, demorarás 10 días. Si llamas a un amigo que trabaja igual que tú, ¡demorarán la mitad! A más manos, menos tiempo. Este sube y baja perfectamente coordinado es la proporción inversa.",
    "resumen": "Dos variables son inversamente proporcionales si al multiplicar una por una constante, la otra se divide por la misma constante. Su producto siempre es el mismo ($x \\cdot y = k$).",
    "explicacion": "Hablamos de **proporcionalidad inversa** cuando dos magnitudes numéricas están vinculadas de modo que el aumento de una provoca la disminución proporcional de la otra.\n\nMatemáticamente, si $x$ e $y$ son inversamente proporcionales, el producto entre ellas es constante:\n$$x \\cdot y = k$$\nSi $x$ se duplica, $y$ se reduce a la mitad. Si $x$ se divide por 3, $y$ se triplica. Es un balancín perfecto.",
    "procedimiento": ["Paso 1: Identifica las dos variables del problema.", "Paso 2: Comprueba si al aumentar una (ej. al doble), la otra lógicamente disminuye en la misma proporción (a la mitad).", "Paso 3: Si esto se cumple, son variables inversamente proporcionales."],
    "ejemplos": [
        {"titulo": "Variables de velocidad y tiempo", "enunciado": "¿Son la velocidad a la que viajas y el tiempo que demoras en llegar proporcionales?", "solucion_pasos": ["Si viajas al doble de velocidad, te demorarás la mitad del tiempo en recorrer la misma distancia.", "Como una sube y la otra baja proporcionalmente, son inversamente proporcionales."]},
        {"titulo": "¿Si una sube y la otra baja, siempre es proporción inversa?", "respuesta": "No", "solucion_pasos": ["El peso de una vela y el tiempo que lleva encendida: a más tiempo, menos peso. Pero si lleva 1 hora y pesa 50g, a las 2 horas no pesará 25g (depende de cuánto peso inicial tenía y cuánto se consume por hora). Es una función lineal decreciente, no una proporción inversa."]}
    ],
    "errores_frecuentes": ["Confundir proporción inversa con cualquier relación donde una variable disminuye mientras la otra aumenta (ej. restar de un total fijo).", "Intentar resolverlo con una regla de tres directa.", "Asumir que la suma es constante en lugar del producto."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVCONC-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué define a dos magnitudes inversamente proporcionales? (v{i})", "choices": ["A) Al aumentar una en cierto factor, la otra disminuye en el mismo factor.", "B) Si una aumenta, la otra aumenta de forma más lenta.", "C) Al restar una de la otra, el resultado es siempre cero.", "D) Ambas aumentan multiplicadas por la misma constante."], "correct_answer": "A) Al aumentar una en cierto factor, la otra disminuye en el mismo factor.", "solution_steps": "Aumento proporcional de $x$ implica reducción proporcional de $y$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PINVCONC-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El modelo matemático de dos variables $x$ e $y$ inversamente proporcionales es:", "choices": ["A) $x \\cdot y = k$", "B) $y / x = k$", "C) $x + y = k$", "D) $y - x = k$"], "correct_answer": "A) $x \\cdot y = k$", "solution_steps": "El producto es constante.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVCONC-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El número de obreros y los días que demoran en una obra son inversamente proporcionales?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Más obreros significa menos días. Al doble de obreros, mitad de días.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVCONC-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"¿En cuál de las siguientes situaciones las variables son inversamente proporcionales? (v{i})", "choices": ["A) La cantidad de llaves iguales que llenan una piscina y el tiempo que demoran en llenarla.", "B) La cantidad de litros de bencina en el estanque y la distancia que puede recorrer el vehículo.", "C) La edad de una persona y su frecuencia cardíaca en reposo.", "D) El número de horas de estudio y la calificación en una prueba."], "correct_answer": "A) La cantidad de llaves iguales que llenan una piscina y el tiempo que demoran en llenarla.", "solution_steps": "Doble de llaves = mitad de tiempo.", "paes_style": True})

# 2. CONSTANTE_PROPORCIONALIDAD INVERSA
sid2 = "MAT.NUM.PROP_INVERSA.CONSTANTE_PROPORCIONALIDAD"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Calcular la constante de proporcionalidad inversa.",
    "introduccion": "Si contratas a 3 pintores y demoran 4 días, el 'esfuerzo total' de la obra es de 12 días-pintor. Ese número global que engloba el trabajo o el tamaño total del problema no cambia por más que varíes a los trabajadores. Es nuestra nueva constante.",
    "resumen": "La constante de proporcionalidad inversa ($k$) es el valor fijo que resulta de multiplicar dos magnitudes proporcionales inversas: $k = x \\cdot y$.",
    "explicacion": "En una **proporcionalidad inversa**, el comportamiento matemático central es que el área del rectángulo formado por $x$ e $y$ siempre es la misma. \n\nSi multiplicas cualquier valor de $y$ por su correspondiente $x$, siempre obtendrás el mismo número.\n\nA este número inalterable lo llamamos **constante de proporcionalidad inversa ($k$)**.\n$$k = x \\cdot y$$",
    "procedimiento": ["Paso 1: Identifica un par de valores $(x, y)$ que correspondan entre sí.", "Paso 2: Multiplica ambas magnitudes ($x \\cdot y$).", "Paso 3: El resultado de esa multiplicación es la constante $k$."],
    "ejemplos": [
        {"titulo": "Hallando k inversa", "enunciado": "Si $4$ tractores aran un campo en $6$ horas, ¿cuál es la constante de proporcionalidad inversa?", "solucion_pasos": ["El par de valores es $x=4$ tractores, $y=6$ horas.", "Multiplicamos $x \\cdot y = 4 \\cdot 6 = 24$.", "La constante es $k=24$. (Se requieren 24 horas-tractor para arar el campo)."]},
        {"titulo": "¿Qué pasa si divido?", "respuesta": "Obtienes un número sin sentido constante.", "solucion_pasos": ["Si haces $6/4 = 1.5$. Si ahora usas 8 tractores (demorarán 3 horas), el cociente sería $3/8 = 0.375$. La división no es constante, el producto sí ($4\\cdot6=24$ y $8\\cdot3=24$)."]}
    ],
    "errores_frecuentes": ["Dividir los valores en lugar de multiplicarlos (confundir con proporción directa).", "Sumar $x+y$ para hallar la constante.", "Creer que la constante cambia si se agregan decimales."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVCONST-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En proporción inversa, ¿cómo se calcula la constante $k$? (v{i})", "choices": ["A) Multiplicando la variable independiente por la dependiente.", "B) Dividiendo la variable dependiente por la independiente.", "C) Sumando ambas variables y dividiendo por dos.", "D) Restando la menor de la mayor."], "correct_answer": "A) Multiplicando la variable independiente por la dependiente.", "solution_steps": "Por definición $k = x \\cdot y$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PINVCONST-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si $x=5$ e $y=10$ son inversamente proporcionales, ¿cuál es el valor de $k$?", "choices": ["A) $50$", "B) $2$", "C) $15$", "D) $5$"], "correct_answer": "A) $50$", "solution_steps": "$k = x \\cdot y = 5 \\cdot 10 = 50$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVCONST-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si 10 máquinas demoran 5 horas, la constante $k$ es 50?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$10 \\cdot 5 = 50$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVCONST-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un ganadero tiene forraje para alimentar a $60$ vacas durante $12$ días. Si las variables son inversamente proporcionales, ¿cuál es la constante de proporcionalidad (raciones totales)? (v{i})", "choices": ["A) $720$", "B) $5$", "C) $72$", "D) $120$"], "correct_answer": "A) $720$", "solution_steps": "$k = 60 \\cdot 12 = 720$.", "paes_style": True})

# 3. RECONOCIMIENTO_TABULAR INVERSA
sid3 = "MAT.NUM.PROP_INVERSA.RECONOCIMIENTO_TABULAR"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Reconocer una relación de proporcionalidad inversa a partir de una tabla de valores.",
    "introduccion": "¿Cómo distinguirías una tabla de proporción inversa de una tabla cualquiera donde los datos suben y bajan? La prueba ácida es multiplicar las filas.",
    "resumen": "En una tabla de proporcionalidad inversa, el producto $x \\cdot y$ en cada fila o columna debe dar exactamente el mismo resultado ($k$).",
    "explicacion": "Una **tabla de valores** puede modelar una proporcionalidad inversa. Para comprobarlo de forma matemática e irrefutable, debes multiplicar el valor de $x$ por su correspondiente valor de $y$ en cada uno de los pares de datos presentados.\n\n- Si todas las multiplicaciones arrojan el mismo número constante $k$, la tabla representa una proporción inversa.\n- Si al menos uno de los productos es distinto, la tabla NO es de proporción inversa (aunque visualmente parezca que una baja mientras la otra sube).",
    "procedimiento": ["Paso 1: Toma el primer par de datos $(x, y)$ de la tabla y multiplícalos.", "Paso 2: Repite la multiplicación para todos los demás pares.", "Paso 3: Si todos los resultados son idénticos, la tabla es inversamente proporcional."],
    "ejemplos": [
        {"titulo": "Verificando una tabla inversa", "enunciado": "La tabla tiene los pares $(2, 24)$, $(3, 16)$, $(6, 8)$. ¿Es proporción inversa?", "solucion_pasos": ["Multiplicamos par 1: $2 \\cdot 24 = 48$.", "Multiplicamos par 2: $3 \\cdot 16 = 48$.", "Multiplicamos par 3: $6 \\cdot 8 = 48$.", "Como todos los productos dan $48$, SÍ representa proporción inversa."]}
    ],
    "errores_frecuentes": ["Dividir los valores en lugar de multiplicarlos (eso prueba proporción directa).", "Solo mirar que los valores de Y bajen cuando X sube, sin hacer el cálculo aritmético.", "Asumir que si la diferencia $x-y$ es constante, es proporción inversa."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVTAB-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Para afirmar que una tabla muestra proporción inversa, se debe comprobar que: (v{i})", "choices": ["A) El producto $x \\cdot y$ sea constante en todos los pares de datos.", "B) El cociente $y/x$ sea constante en todos los pares de datos.", "C) La suma de $x+y$ sea constante.", "D) Mientras $x$ aumenta, $y$ también aumenta."], "correct_answer": "A) El producto $x \\cdot y$ sea constante en todos los pares de datos.", "solution_steps": "Es la comprobación de la constante $k$ inversa.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PINVTAB-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si una tabla tiene los pares $(4, 10)$, $(8, 5)$, $(2, z)$, y es de proporción inversa, ¿cuál es el valor de $z$?", "choices": ["A) $20$", "B) $40$", "C) $10$", "D) $15$"], "correct_answer": "A) $20$", "solution_steps": "La constante es $4\\cdot10=40$. Luego $2\\cdot z = 40 \\implies z=20$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVTAB-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿La tabla con pares $(2, 12), (3, 8), (4, 6)$ representa proporción inversa?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Todos los productos son 24.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVTAB-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al analizar el vaciado de un estanque, se midió (Diámetro de válvula cm, Minutos de vaciado): $(2, 60)$, $(3, 40)$, $(4, 30)$. ¿Es este un modelo de proporcionalidad inversa? (v{i})", "choices": ["A) Sí, porque en todos los casos el producto del diámetro por los minutos es $120$.", "B) No, porque a mayor diámetro debiera demorar más.", "C) Sí, porque el cociente $60/2 = 30$ es igual al último par.", "D) No, porque no hay un patrón en las diferencias."], "correct_answer": "A) Sí, porque en todos los casos el producto del diámetro por los minutos es $120$.", "solution_steps": "$2\\cdot60=120$, $3\\cdot40=120$, $4\\cdot30=120$.", "paes_style": True})

# 4. GRAFICO_HIPERBOLA
sid4 = "MAT.NUM.PROP_INVERSA.GRAFICO_HIPERBOLA"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Identificar y analizar el gráfico de una proporción inversa.",
    "introduccion": "A diferencia de la proporción directa que es una flecha recta y firme que cruza el plano, la proporción inversa traza una curva suave y elegante que se acerca a las paredes del plano pero jamás las toca.",
    "resumen": "El gráfico de una proporción inversa en el primer cuadrante es una curva decreciente llamada hipérbola equilátera, que nunca toca los ejes (es asintótica a los ejes X e Y).",
    "explicacion": "Una **proporcionalidad inversa** ($y = k/x$) jamás será una línea recta. Su representación gráfica es una curva que desciende de izquierda a derecha de forma pronunciada al principio y luego se aplana. \n\nEsta curva se llama rama de **hipérbola equilátera**. Sus características clave son:\n1. Es decreciente: si $x$ avanza, $y$ baja.\n2. **Nunca toca el origen $(0,0)$** ni los ejes. Esto se debe a que no se puede dividir por cero ($k/0$ no existe), y si $x=0$, $y$ no tiene valor; si $y=0$, $x$ no tiene valor.",
    "procedimiento": ["Paso 1: Observa el plano cartesiano.", "Paso 2: Comprueba que sea una curva que baja hacia la derecha (decreciente).", "Paso 3: Verifica que la curva no cruce los ejes X ni Y en el cuadrante positivo."],
    "ejemplos": [
        {"titulo": "Evaluando gráficos inversos", "enunciado": "Una gráfica muestra una línea recta diagonal que baja de $(0,10)$ a $(10,0)$. ¿Es proporción inversa?", "solucion_pasos": ["La forma es de línea recta, no curva.", "Toca los ejes (X=10 y Y=10).", "Por lo tanto, NO es proporción inversa. Es una función afín decreciente."]}
    ],
    "errores_frecuentes": ["Confundir una recta decreciente ($y = -mx+n$) con una hipérbola.", "Creer que la curva sí toca el cero si se le da suficiente tiempo.", "No asociar el nombre 'hipérbola' a este fenómeno y creer que es una parábola.", "Graficar puntos de proporción inversa y unirlos con líneas rectas creando un polígono, en vez de una curva suavizada."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVGRAF-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Visualmente, el gráfico de una proporción inversa en el primer cuadrante corresponde a: (v{i})", "choices": ["A) Una curva decreciente que no corta a los ejes coordenados.", "B) Una línea recta decreciente que corta a ambos ejes.", "C) Una línea recta que pasa por el origen $(0,0)$.", "D) Una curva con forma de U que toca el eje X."], "correct_answer": "A) Una curva decreciente que no corta a los ejes coordenados.", "solution_steps": "Es una hipérbola equilátera que se acerca asintóticamente a los ejes.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PINVGRAF-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El nombre matemático de la curva que representa la proporción inversa es:", "choices": ["A) Hipérbola", "B) Parábola", "C) Recta afín", "D) Circunferencia"], "correct_answer": "A) Hipérbola", "solution_steps": "Específicamente, rama de hipérbola equilátera.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVGRAF-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El gráfico de una proporción inversa pasa por el punto $(0,0)$?", "choices": [], "correct_answer": "Falso", "solution_steps": "Jamás toca el cero, pues implicaría dividir por cero en la ecuación $y=k/x$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVGRAF-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Si en una prueba técnica observas que la gráfica entre la Presión y el Volumen de un gas a temperatura constante forma una curva que desciende asintóticamente hacia los ejes, puedes concluir que el modelo matemático es de la forma: (v{i})", "choices": ["A) $P \\cdot V = k$", "B) $P / V = k$", "C) $P + V = k$", "D) $P = V \\cdot k$"], "correct_answer": "A) $P \\cdot V = k$", "solution_steps": "La curva asintótica decreciente es la hipérbola de la proporción inversa, cuya constante es el producto.", "paes_style": True})

# 5. MODELO_ALGEBRAICO INVERSA
sid5 = "MAT.NUM.PROP_INVERSA.MODELO_ALGEBRAICO"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Representar situaciones de proporción inversa a través de un modelo algebraico (ecuación).",
    "introduccion": "Al igual que con la directa, podemos construir una 'máquina' para la proporción inversa. Esta máquina toma el trabajo total, lo divide por lo que tengas ahora, y te dice exactamente qué pasará.",
    "resumen": "El modelo algebraico de la proporcionalidad inversa es la ecuación $y = k / x$, donde $k$ es la constante de proporcionalidad.",
    "explicacion": "Sabiendo que $x \\cdot y = k$, podemos despejar la variable dependiente $y$ dividiendo ambos lados por $x$. Así obtenemos el **modelo algebraico** de la proporción inversa:\n\n$$y = \\frac{k}{x}$$\n\nEsta ecuación nos dice que para hallar cualquier valor de $y$, debemos tomar nuestra 'cantidad total' (la constante $k$) y repartirla o dividirla entre el valor de $x$. Si $x$ crece, se divide por un número mayor, haciendo que $y$ sea más pequeño.",
    "procedimiento": ["Paso 1: Calcula la constante $k$ multiplicando un par conocido $x \\cdot y$.", "Paso 2: Escribe la ecuación sustituyendo $k$ por el número encontrado como numerador.", "Paso 3: Utiliza $y = k/x$ para calcular valores desconocidos reemplazando el valor de $x$."],
    "ejemplos": [
        {"titulo": "Construyendo el modelo inverso", "enunciado": "Si 5 obreros terminan un muro en 20 días, escribe el modelo algebraico del tiempo ($y$) en función de los obreros ($x$).", "solucion_pasos": ["Calculamos $k = 5 \\cdot 20 = 100$ (días-obrero totales).", "Planteamos la fórmula general $y = k / x$.", "El modelo es $y = 100/x$. (Si vienen 2 obreros, $100/2 = 50$ días)."]},
        {"titulo": "¿Puedo despejar x en la ecuación inversa?", "respuesta": "Sí", "solucion_pasos": ["Al igual que $y = 100/x$, se cumple que $x = 100/y$. Puedes alternar posiciones sin alterar el numerador $k$."]}
    ],
    "errores_frecuentes": ["Plantear el modelo como $y = x / k$ (el total siempre debe ser el dividendo).", "Usar el modelo $y = k \\cdot x$ (que es para proporción directa).", "Plantearlo como una resta $y = k - x$.", "Olvidar que $x$ no puede ser cero en la evaluación de la fórmula."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVMOD-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué ecuación representa adecuadamente una proporción inversa entre $x$ e $y$? (v{i})", "choices": ["A) $y = k / x$", "B) $y = k \\cdot x$", "C) $y = x / k$", "D) $y = x - k$"], "correct_answer": "A) $y = k / x$", "solution_steps": "Despejando y de $xy = k$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PINVMOD-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si en un problema $k = 300$, el modelo matemático para calcular $y$ inversamente proporcional a $x$ es:", "choices": ["A) $y = 300 / x$", "B) $y = 300x$", "C) $y = x / 300$", "D) $y = 300 - x$"], "correct_answer": "A) $y = 300 / x$", "solution_steps": "El total (300) se divide entre x.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVMOD-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El modelo $y = 1500 / x$ indica que si $x$ vale 10, $y$ valdrá 150?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$1500 / 10 = 150$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVMOD-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un grifo arroja agua llenando un depósito en $4$ horas. Si se instala un equipo que puede multiplicar la presión y caudal del agua. ¿Cuál es el modelo algebraico del tiempo $T$ en horas, según el número $N$ de grifos equivalentes que se simulen usar? (v{i})", "choices": ["A) $T = 4 / N$", "B) $T = 4N$", "C) $T = N / 4$", "D) $T = 4 - N$"], "correct_answer": "A) $T = 4 / N$", "solution_steps": "1 grifo tarda 4 horas, $k=4$. Modelo es $T = 4/N$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 5...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 5...")
    append_jsonl("mat-num-razones-banco-gen-5", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-5.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()

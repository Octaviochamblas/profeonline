# scratch/build_b0205_t9.py
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

# 1. REPRESENTACION_GRAFICA (PORCENTAJES)
sid1 = "MAT.NUM.PORCENTAJES.REPRESENTACION_GRAFICA"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Interpretar la representación gráfica de un porcentaje.",
    "introduccion": "Si ves un gráfico circular en las noticias donde la mitad está pintada de azul, sabes instantáneamente que es un 50%. Nuestro cerebro entiende los porcentajes mucho mejor cuando están dibujados como porciones de un todo.",
    "resumen": "Los porcentajes se grafican típicamente en gráficos circulares (el círculo completo es 100%) o en cuadrículas de 10x10 (donde cada cuadrito iluminado equivale a 1%).",
    "explicacion": "Visualmente, el $100\\%$ representa **el entero**. Todo dibujo que represente porcentajes asume que la figura completa vale 100.\n\n- **Cuadrícula 10x10**: Se dibuja un cuadrado dividido en 100 cuadraditos iguales. Pintar 25 cuadraditos representa el $25\\%$.\n- **Gráfico circular (torta)**: Los $360^\\circ$ del círculo representan el $100\\%$. Para saber el ángulo de un sector, multiplicas el porcentaje por $3.6$. Por ejemplo, $50\\%$ es la mitad del círculo ($180^\\circ$).\n- **Barra de progreso**: Un rectángulo largo donde rellenar la mitad es $50\\%$ y llenarlo entero es $100\\%$.",
    "procedimiento": ["Paso 1: Identifica qué figura representa el total (100%).", "Paso 2: Observa la proporción sombreada.", "Paso 3: Si es una cuadrícula de 100, cuenta los cuadros. Si es circular, estima si es la mitad (50%), un cuarto (25%), etc."],
    "ejemplos": [
        {"titulo": "Cuadrícula sombreada", "enunciado": "Hay un cuadrado de 10x10. Tiene 2 filas completas pintadas y 3 cuadritos más. ¿Qué porcentaje es?", "solucion_pasos": ["2 filas de 10 = 20 cuadritos.", "20 + 3 = 23 cuadritos.", "Como el total es 100, representa el 23%."]}
    ],
    "errores_frecuentes": ["Creer que en una cuadrícula de 5x5 cada cuadro vale 1% (cada uno vale 4%, ya que 100/25 = 4).", "Confundir el 25% en un círculo con un tercio de la torta.", "Asumir que si la figura crece de tamaño, los porcentajes cambian (el 50% de un círculo gigante sigue siendo la mitad)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCGRAF-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En un gráfico circular estándar, ¿qué ángulo le corresponde al $50\\%$? (v{i})", "choices": ["A) $180^\\circ$", "B) $90^\\circ$", "C) $50^\\circ$", "D) $360^\\circ$"], "correct_answer": "A) $180^\\circ$", "solution_steps": "Es la mitad de los 360 grados del círculo completo.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCGRAF-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si en una cuadrícula de 100 cuadrados idénticos (10x10) pinto 7 cuadrados, he representado el:", "choices": ["A) $7\\%$", "B) $70\\%$", "C) $0.7\\%$", "D) $700\\%$"], "correct_answer": "A) $7\\%$", "solution_steps": "Son 7 de 100, es decir 7%.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCGRAF-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Un gráfico de barra de progreso relleno hasta sus tres cuartas partes marca el $75\\%$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$3/4$ de 100 es 75.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCGRAF-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"En la encuesta de un colegio, se construye un gráfico circular sobre el deporte favorito. Si la sección de 'Fútbol' tiene un ángulo de $90^\\circ$ y la sección de 'Básquetbol' un ángulo de $36^\\circ$, ¿qué porcentajes del total representan respectivamente? (v{i})", "choices": ["A) Fútbol $25\\%$ y Básquetbol $10\\%$", "B) Fútbol $90\\%$ y Básquetbol $36\\%$", "C) Fútbol $50\\%$ y Básquetbol $10\\%$", "D) Fútbol $25\\%$ y Básquetbol $5\\%$"], "correct_answer": "A) Fútbol $25\\%$ y Básquetbol $10\\%$", "solution_steps": "360 grados es el 100%. Por regla de tres: $90/360 = 1/4 = 25\\%$. $36/360 = 1/10 = 10\\%$.", "paes_style": True})

# 2. REPRESENTACION_DECIMAL
sid2 = "MAT.NUM.PORCENTAJES.REPRESENTACION_DECIMAL"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Convertir porcentajes a números decimales y viceversa.",
    "introduccion": "Las calculadoras no tienen un botón mágico para los porcentajes internos, operan con decimales. Si le pides el 20%, ella silenciosamente multiplicará por 0.20.",
    "resumen": "Para convertir un porcentaje a decimal, se divide por 100 (corriendo la coma dos lugares a la izquierda). Ej: $45\\% = 0.45$. Para decimal a porcentaje, se multiplica por 100.",
    "explicacion": "Como un porcentaje es una fracción de denominador 100 ($x/100$), su **representación decimal** se obtiene simplemente ejecutando esa división.\n\n- $80\\% = 80 \\div 100 = 0.80$\n- $5\\% = 5 \\div 100 = 0.05$ (¡Atención al cero!)\n- $150\\% = 150 \\div 100 = 1.50$\n\nPara el proceso inverso (de decimal a porcentaje), haces lo contrario: multiplicar el decimal por 100 y agregar el símbolo $\%$.\n- $0.12 = 0.12 \\cdot 100 = 12\\%$.",
    "procedimiento": ["Paso 1: Toma el número del porcentaje y retira el símbolo %.", "Paso 2: Mueve el punto decimal dos posiciones hacia la izquierda.", "Paso 3: Si faltan dígitos, rellena con ceros. (Ej: $2\\% \\rightarrow 0.02$)."],
    "ejemplos": [
        {"titulo": "Conversión decimal", "enunciado": "Convierte 3.5% a número decimal.", "solucion_pasos": ["Retiramos el símbolo: 3.5", "Corremos la coma dos espacios a la izquierda: $0.035$.", "El número decimal para operar en calculadora es $0.035$."]}
    ],
    "errores_frecuentes": ["Convertir el $5\\%$ en $0.5$ (eso es el $50\\%$). Lo correcto es $0.05$.", "Creer que $100\\%$ es $100.0$ en decimal (es $1.0$).", "No saber qué hacer con porcentajes menores a 1, como $0.2\\%$ (su decimal es $0.002$)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCDEC-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Para transformar un porcentaje directamente a su valor decimal equivalente, debes: (v{i})", "choices": ["A) Dividirlo por 100.", "B) Multiplicarlo por 100.", "C) Dividirlo por 10.", "D) Agregarle un cero a la izquierda."], "correct_answer": "A) Dividirlo por 100.", "solution_steps": "Correr la coma dos lugares a la izquierda equivale a dividir por 100.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCDEC-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El número decimal equivalente a $8\\%$ es:", "choices": ["A) $0.08$", "B) $0.8$", "C) $0.008$", "D) $8.0$"], "correct_answer": "A) $0.08$", "solution_steps": "$8/100 = 0.08$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCDEC-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El número decimal $1.25$ representa el $125\\%$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$1.25 \\cdot 100 = 125\\%$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCDEC-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al ingresar a una base de datos, las tasas de interés se deben anotar en formato decimal para las fórmulas. Si un cliente tiene una tasa preferencial del $0.4\\%$ mensual, ¿qué valor exacto se debe ingresar en la base de datos? (v{i})", "choices": ["A) $0.004$", "B) $0.04$", "C) $0.4$", "D) $0.0004$"], "correct_answer": "A) $0.004$", "solution_steps": "Correr la coma de $0.4$ dos espacios a la izquierda da $0.004$.", "paes_style": True})

# 3. REPRESENTACION_FRACCIONARIA
sid3 = "MAT.NUM.PORCENTAJES.REPRESENTACION_FRACCIONARIA"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Transformar porcentajes en fracciones irreductibles y utilizarlas en cálculos.",
    "introduccion": "Trabajar el 75% de un número multiplicando por 0.75 es válido, pero ¿no es más rápido multiplicar por 3 y dividir por 4? Las fracciones irreductibles son los 'atajos ninja' de los porcentajes.",
    "resumen": "Cualquier porcentaje se puede simplificar como una fracción irreductible. Ejemplos clásicos: $50\\% = 1/2$, $25\\% = 1/4$, $20\\% = 1/5$, $75\\% = 3/4$.",
    "explicacion": "Todo porcentaje es la fracción $x/100$. Muchas veces, esa fracción se puede simplificar dividiendo numerador y denominador por un factor común.\n\nEstas **fracciones irreductibles equivalentes** te permiten hacer cálculos mentalmente mucho más rápido que usando decimales.\n- $10\\% = 10/100 = 1/10$ (dividir por 10)\n- $20\\% = 20/100 = 1/5$ (dividir por 5)\n- $25\\% = 25/100 = 1/4$ (dividir por 4)\n- $50\\% = 50/100 = 1/2$ (la mitad)\n- $75\\% = 75/100 = 3/4$ (tres cuartas partes)",
    "procedimiento": ["Paso 1: Escribe el porcentaje como fracción $x/100$.", "Paso 2: Simplifica dividiendo por 2, 5 o múltiplos de 10 hasta que sea irreductible.", "Paso 3: Utiliza esa fracción multiplicando por el numerador y dividiendo por el denominador."],
    "ejemplos": [
        {"titulo": "Uso de la fracción equivalente", "enunciado": "Calcula el 25% de 800.", "solucion_pasos": ["Sabemos que 25% es $1/4$.", "Multiplicamos $800 \\cdot (1/4)$.", "Es lo mismo que dividir por 4: $800 / 4 = 200$."]}
    ],
    "errores_frecuentes": ["Creer que $20\\%$ es $1/20$ (es $1/5$, porque $100/20 = 5$).", "Creer que $10\\%$ equivale a dividir por 100 (equivale a dividir por 10).", "Tratar de simplificar porcentajes como $17\\%$ que son primos y no se pueden simplificar (queda $17/100$)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCFRAC-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Por qué es útil conocer la representación fraccionaria irreductible de un porcentaje? (v{i})", "choices": ["A) Porque permite realizar cálculos mentales más rápidos reemplazando multiplicaciones decimales por divisiones enteras.", "B) Porque es el único formato que aceptan las calculadoras.", "C) Porque los porcentajes no pueden escribirse con decimales.", "D) Porque altera el valor del porcentaje para facilitar el problema."], "correct_answer": "A) Porque permite realizar cálculos mentales más rápidos reemplazando multiplicaciones decimales por divisiones enteras.", "solution_steps": "Atajo de cálculo mental.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCFRAC-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "La fracción irreductible correspondiente al $40\\%$ es:", "choices": ["A) $2/5$", "B) $4/10$", "C) $1/40$", "D) $4/5$"], "correct_answer": "A) $2/5$", "solution_steps": "$40/100$ simplificado por 20 es $2/5$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCFRAC-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿La fracción $3/4$ corresponde al $75\\%$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$3/4 = 75/100 = 75\\%$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCFRAC-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Si un pastel se divide y a María le toca el $60\\%$, a Juan el $20\\%$ y a Pedro el resto. ¿Qué fracción irreductible del pastel se comió Pedro? (v{i})", "choices": ["A) $1/5$", "B) $20/100$", "C) $1/4$", "D) $2/5$"], "correct_answer": "A) $1/5$", "solution_steps": "Pedro comió $100\\% - (60+20) = 20\\%$. La fracción irreductible de $20\\%$ es $20/100 = 1/5$.", "paes_style": True})

# 4. CALCULO_VALOR (el C% de algo)
sid4 = "MAT.NUM.PORCENTAJES.CALCULO_VALOR"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Calcular un porcentaje determinado de una cantidad dada.",
    "introduccion": "Si la tienda anuncia un 30% de descuento en una zapatilla de $50.000, ¿cuántos billetes te estás ahorrando exactamente? Este es el cálculo porcentual más usado en el mundo real.",
    "resumen": "Para calcular el $c\\%$ de una cantidad $N$, se multiplica $N$ por la fracción $c/100$ o por su número decimal asociado ($0.c$).",
    "explicacion": "Calcular el porcentaje de una cantidad significa encontrar esa porción específica sobre un número base.\n\nMatemáticamente, la palabra 'de' significa multiplicación. Por ende, el '$c\\%$ de $N$' se traduce como:\n$$\\text{Valor} = N \\cdot \\frac{c}{100}$$\n\nPuedes hacerlo de tres formas (elige la más cómoda para los números que tengas):\n1. Multiplicar $N \\cdot c$ y luego dividir por $100$.\n2. Convertir $c\\%$ a decimal y multiplicar: $N \\cdot 0.c$.\n3. Usar fracciones equivalentes si es un porcentaje famoso (ej. para $25\\%$, divides $N$ por $4$).",
    "procedimiento": ["Paso 1: Identifica el porcentaje a calcular ($c$) y la cantidad base ($N$).", "Paso 2: Plantea la multiplicación $N \\cdot (c/100)$.", "Paso 3: Realiza la operación (multiplica y luego divide por 100, o usa decimales)."],
    "ejemplos": [
        {"titulo": "Cálculo estándar", "enunciado": "Calcula el 15% de 400.", "solucion_pasos": ["Multiplicamos $400 \\cdot 15 = 6000$.", "Dividimos por 100: $6000 / 100 = 60$.", "El 15% de 400 es 60."]}
    ],
    "errores_frecuentes": ["Dividir la cantidad $N$ por el porcentaje $c$ (ej. $400 / 15$).", "Calcular el porcentaje pero olvidar restarlo o sumarlo si el problema preguntaba por un descuento o aumento final.", "Olvidar los ceros al multiplicar por decimales."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCCVAL-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"La expresión matemática que traduce correctamente la frase 'el $X\\%$ de $Y$' es: (v{i})", "choices": ["A) $Y \\cdot (X / 100)$", "B) $X \\cdot (Y / 100)$", "C) $X / Y \\cdot 100$", "D) Ambas A y B son correctas y arrojan el mismo resultado matemático."], "correct_answer": "D) Ambas A y B son correctas y arrojan el mismo resultado matemático.", "solution_steps": "La multiplicación es conmutativa. $X\\%$ de $Y$ = $Y\\%$ de $X$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCCVAL-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El $30\\%$ de $150$ es igual a:", "choices": ["A) $45$", "B) $30$", "C) $50$", "D) $450$"], "correct_answer": "A) $45$", "solution_steps": "$150 \\cdot 0.30 = 45$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCCVAL-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El $120\\%$ de $50$ es mayor que $50$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Al ser mayor al 100%, el resultado superará la cantidad base. ($50 \\cdot 1.2 = 60$).", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCCVAL-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una tienda liquida toda su ropa de invierno con un $45\\%$ de descuento. Si una chaqueta costaba originalmente $\$60.000$, ¿cuál es el monto que te rebajarán del precio (es decir, el valor del descuento)? (v{i})", "choices": ["A) $\$27.000$", "B) $\$33.000$", "C) $\$45.000$", "D) $\$24.000$"], "correct_answer": "A) $\$27.000$", "solution_steps": "$60.000 \\cdot 45 / 100 = 600 \\cdot 45 = 27.000$. Ojo que pregunta por la rebaja, no el precio final.", "paes_style": True})

# 5. CALCULO_PORCENTAJE (Qué % representa)
sid5 = "MAT.NUM.PORCENTAJES.CALCULO_PORCENTAJE"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Calcular qué porcentaje representa una cantidad respecto de otra (el total).",
    "introduccion": "Tuviste 24 aciertos en una prueba de 30 preguntas. ¿Qué nota te sacarás? Necesitas saber qué porcentaje de la prueba dominaste. Este es el cálculo inverso.",
    "resumen": "Para saber qué porcentaje es una Parte respecto a un Total, se divide la Parte por el Total y se multiplica por 100: $\\% = (Parte / Total) \\cdot 100$.",
    "explicacion": "Cuando la pregunta es '¿Qué porcentaje es $P$ respecto de $T$?', estamos buscando la relación entre la Parte ($P$) y el Total ($T$) llevada a una escala de 100.\n\nLa fórmula directa es:\n$$\\% = \\left( \\frac{\\text{Parte}}{\\text{Total}} \\right) \\cdot 100$$\n\nEjemplo lógico: Si la Parte es exactamente la mitad del Total, $P/T$ dará $0.5$. Al multiplicarlo por 100 obtenemos $50\\%$. \nEste cálculo es equivalente a una regla de tres: Si $T$ es el $100\\%$, entonces $P$ es a $x\\%$.",
    "procedimiento": ["Paso 1: Identifica el 'Total' (la base de referencia) y la 'Parte'.", "Paso 2: Divide la Parte por el Total.", "Paso 3: Multiplica el resultado decimal por 100 y agrégale el símbolo %."],
    "ejemplos": [
        {"titulo": "Porcentaje de aciertos", "enunciado": "Si aciertas 15 tiros de 20 intentos, ¿cuál es tu porcentaje de acierto?", "solucion_pasos": ["Parte = 15, Total = 20.", "Fracción: $15/20$.", "Multiplicamos por 100: $(15/20) \\cdot 100 = 15 \\cdot 5 = 75$.", "El porcentaje de acierto es 75%."]}
    ],
    "errores_frecuentes": ["Dividir el Total por la Parte (ej. $20/15$) obteniendo porcentajes absurdos mayores a 100% cuando no corresponde.", "Olvidar multiplicar por 100, respondiendo 'es el $0.75\\%$' en lugar de $75\\%$.", "Confundir cuál es la base (el Total) en problemas redactados confusamente (ej. 'Qué porcentaje es 50 respecto a 200')."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCCQUE-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Para determinar qué porcentaje de un curso de 40 alumnos está de cumpleaños, sabiendo que son 8 alumnos, debes calcular: (v{i})", "choices": ["A) $(8 / 40) \\cdot 100$", "B) $(40 / 8) \\cdot 100$", "C) $(8 \\cdot 40) / 100$", "D) $(40 - 8) \\cdot 100$"], "correct_answer": "A) $(8 / 40) \\cdot 100$", "solution_steps": "Parte/Total por 100.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCCQUE-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Qué porcentaje es $45$ respecto a $90$?", "choices": ["A) $50\\%$", "B) $20\\%$", "C) $45\\%$", "D) $200\\%$"], "correct_answer": "A) $50\\%$", "solution_steps": "$(45/90) \\cdot 100 = 0.5 \\cdot 100 = 50\\%$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCCQUE-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si ahorraste $\$2.000$ de un sueldo de $\$100.000$, ahorraste el $2\\%$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$(2000 / 100000) \\cdot 100 = 2$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCCQUE-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un estanque de agua de $800$ litros sufre una filtración y pierde $120$ litros durante la noche. ¿Qué porcentaje del agua original se filtró? (v{i})", "choices": ["A) $15\\%$", "B) $12\\%$", "C) $8\\%$", "D) $85\\%$"], "correct_answer": "A) $15\\%$", "solution_steps": "$(120 / 800) \\cdot 100 = 120 / 8 = 15$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 9...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 9...")
    append_jsonl("mat-num-razones-banco-gen-9", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-9.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()

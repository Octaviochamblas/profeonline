# scratch/build_b0205_t10.py
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

# 1. CALCULO_TOTAL (Dado el porcentaje)
sid1 = "MAT.NUM.PORCENTAJES.CALCULO_TOTAL"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Calcular el total (100%) conociendo el valor de un porcentaje específico.",
    "introduccion": "Si te dicen que $12.000 corresponde al 20% de un premio, ¿cuál era el premio completo? Aprender a reconstruir el pastel entero teniendo solo una rebanada es fundamental en finanzas.",
    "resumen": "Para hallar el Total ($T$) cuando se conoce que el $c\\%$ equivale a una Parte ($P$), se despeja de la fórmula básica: $T = (P / c) \\cdot 100$.",
    "explicacion": "Sabemos que el cálculo directo es $\\text{Parte} = \\text{Total} \\cdot (c/100)$. Si lo que nos falta es el **Total**, debemos despejar la ecuación:\n\n$$\\text{Total} = \\frac{\\text{Parte}}{c} \\cdot 100$$\n\nEsto se puede razonar lógicamente en dos pasos:\n1. Al dividir la Parte entre el porcentaje $c$, estás averiguando **cuánto vale el 1%**.\n2. Al multiplicar ese resultado por 100, estás descubriendo **el 100%** (el Total).",
    "procedimiento": ["Paso 1: Identifica el valor de la Parte ($P$) y a qué porcentaje equivale ($c$).", "Paso 2: Divide $P$ por $c$. Esto te da el valor del 1%.", "Paso 3: Multiplica ese resultado por 100 para obtener el Total."],
    "ejemplos": [
        {"titulo": "Adivinando el sueldo", "enunciado": "Si ahorraste $15.000 y eso corresponde al 5% de tu sueldo, ¿cuánto es tu sueldo total?", "solucion_pasos": ["Parte = $15.000, Porcentaje = 5.", "Calculamos el 1%: $15.000 / 5 = 3.000$.", "Multiplicamos por 100: $3.000 \\cdot 100 = 300.000$.", "El sueldo total es $300.000."]}
    ],
    "errores_frecuentes": ["Multiplicar la Parte por el porcentaje en lugar de dividir (ej. calcular el 5% de 15.000 en vez de usar 15.000 como base para hallar el total).", "Usar el número decimal ($0.05$) dividiendo, lo cual es matemáticamente correcto ($15000 / 0.05$), pero la gente suele confundirse al dividir por decimales. El método del 1% es más seguro."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCTOTAL-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Si conoces que una cierta cantidad $P$ representa el $C\\%$ de un total desconocido $T$, puedes encontrar el valor de $T$ mediante la operación: (v{i})", "choices": ["A) $(P / C) \\cdot 100$", "B) $(P \\cdot C) / 100$", "C) $(C / P) \\cdot 100$", "D) $P \\cdot C \\cdot 100$"], "correct_answer": "A) $(P / C) \\cdot 100$", "solution_steps": "Despejando T de la ecuación base, o pensando en hallar el 1% y luego el 100%.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCTOTAL-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si el $10\\%$ de una cantidad es $30$, el total ($100\\%$) es:", "choices": ["A) $300$", "B) $3000$", "C) $3$", "D) $33$"], "correct_answer": "A) $300$", "solution_steps": "$30 / 10 = 3$ (esto es el 1%). $3 \\cdot 100 = 300$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCTOTAL-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si $40$ representa el $20\\%$ de un número, ese número es $200$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$40 / 20 = 2$. $2 \\cdot 100 = 200$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCTOTAL-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una automotora recibe un anticipo de $\$1.500.000$ por un vehículo, lo que corresponde exactamente al $12\\%$ del valor total del auto. ¿Cuál es el precio total del vehículo? (v{i})", "choices": ["A) $\$12.500.000$", "B) $\$15.000.000$", "C) $\$1.800.000$", "D) $\$18.000.000$"], "correct_answer": "A) $\$12.500.000$", "solution_steps": "$1.500.000 / 12 = 125.000$ (eso es el $1\\%$). $125.000 \\cdot 100 = 12.500.000$.", "paes_style": True})

# 2. PORCENTAJE_DE_PORCENTAJE
sid2 = "MAT.NUM.PORCENTAJES.PORCENTAJE_DE_PORCENTAJE"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Calcular el porcentaje de un porcentaje y representarlo como un porcentaje único.",
    "introduccion": "Si hay una liquidación del 50% y sobre eso te hacen un 20% extra por ser socio, ¿es un 70% total? ¡NO! Es el 20% de lo que quedó. Entender los porcentajes encadenados evita que las tiendas te engañen.",
    "resumen": "Para calcular el $A\\%$ del $B\\%$ de una cantidad, se multiplican las fracciones correspondientes: $(A/100) \\cdot (B/100)$. Nunca se suman directamente.",
    "explicacion": "Calcular el porcentaje de otro porcentaje significa que la base referencial (el Total) ha cambiado.\n\nPor ejemplo, el $50\\%$ del $20\\%$ no es el $70\\%$. Matemáticamente, se traduce reemplazando el 'del' por una multiplicación:\n\n$$\\frac{50}{100} \\cdot \\frac{20}{100} = \\frac{1}{2} \\cdot \\frac{1}{5} = \\frac{1}{10} = 10\\%$$\n\n¡El 50% (la mitad) del 20% es lógicamente el 10% del total! \nSi quieres saber el porcentaje único, siempre multiplica las fracciones porcentuales y simplifica hasta que quede un único denominador 100.",
    "procedimiento": ["Paso 1: Escribe cada porcentaje como una fracción sobre 100.", "Paso 2: Multiplica ambas fracciones entre sí.", "Paso 3: Simplifica la fracción resultante para que el denominador vuelva a ser 100. El numerador será el porcentaje real equivalente."],
    "ejemplos": [
        {"titulo": "Porcentaje de porcentaje", "enunciado": "Calcula el 25% del 40% de una cantidad.", "solucion_pasos": ["Escribimos las fracciones: $(25/100) \\cdot (40/100)$.", "Simplificamos: $25/100$ es $1/4$. $40/100$ es $2/5$.", "Multiplicamos: $(1/4) \\cdot (2/5) = 2/20$.", "Llevamos a denominador 100 multiplicando por 5 arriba y abajo: $10/100$.", "Equivale a calcular el 10% de la cantidad original."]}
    ],
    "errores_frecuentes": ["Sumar los porcentajes (ej. creer que el 20% del 30% es un 50%).", "Multiplicar los números enteros directamente sin dividir por $100 \\cdot 100$ (ej. $20 \\cdot 30 = 600\\%$ en lugar de $6\\%$)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCPORC-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Para calcular matemáticamente a qué porcentaje único equivale el 'X% del Y%' de una cantidad, se debe: (v{i})", "choices": ["A) Multiplicar las fracciones $(X/100)$ y $(Y/100)$.", "B) Sumar los porcentajes $X + Y$.", "C) Restar el porcentaje menor del mayor.", "D) Dividir $X$ entre $Y$."], "correct_answer": "A) Multiplicar las fracciones $(X/100)$ y $(Y/100)$.", "solution_steps": "La palabra 'del' implica multiplicación de fracciones.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCPORC-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El $10\\%$ del $10\\%$ equivale a un porcentaje único del:", "choices": ["A) $1\\%$", "B) $20\\%$", "C) $100\\%$", "D) $0.1\\%$"], "correct_answer": "A) $1\\%$", "solution_steps": "$(10/100) \\cdot (10/100) = 1/10 \\cdot 1/10 = 1/100 = 1\\%$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCPORC-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El $50\\%$ del $80\\%$ es equivalente al $40\\%$ del total?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "La mitad ($50\\%$) de 80 es 40.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCPORC-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una parcela de tierra es vendida y el dueño original conserva el $30\\%$. Luego, decide ceder el $40\\%$ de lo que conservó a su hijo. ¿Qué porcentaje del total de la parcela original recibió el hijo? (v{i})", "choices": ["A) $12\\%$", "B) $70\\%$", "C) $10\\%$", "D) $40\\%$"], "correct_answer": "A) $12\\%$", "solution_steps": "$40\\%$ del $30\\%$ = $(40/100) \\cdot (30/100) = (4/10) \\cdot (3/10) = 12/100 = 12\\%$.", "paes_style": True})

# 3. CALCULO_MENTAL_DIEZ
sid3 = "MAT.NUM.PORCENTAJES.CALCULO_MENTAL_DIEZ"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Aplicar la estrategia de cálculo mental rápida para el 10% y sus múltiplos.",
    "introduccion": "No siempre tienes una calculadora a mano en el supermercado. Aprender a calcular el 10% en tu cabeza te dará superpoderes para estimar el 20%, 30% o 50% en segundos.",
    "resumen": "Para hallar el 10% de cualquier número, simplemente divídelo por 10 (córrele la coma un espacio a la izquierda). Luego, multiplica ese valor para hallar el 20%, 30%, etc.",
    "explicacion": "El **$10\\%$** es la base del cálculo mental porque equivale a la fracción $10/100$, que simplificada es $1/10$.\n\n**Regla de oro del 10%:**\nPara calcular el 10% de un número, mueve su punto decimal una posición a la izquierda.\n- El 10% de 450 es 45.\n- El 10% de 35 es 3.5.\n\nUna vez tienes el 10%, calcular múltiplos es fácil:\n- **$20\\%$**: Calcula el 10% y el resultado multiplícalo por 2.\n- **$30\\%$**: Calcula el 10% y multiplícalo por 3.\n- **$5\\%$**: Calcula el 10% y divídelo por 2 (es la mitad).",
    "procedimiento": ["Paso 1: Mueve la coma decimal un lugar a la izquierda para obtener el 10%.", "Paso 2: Si te piden el 20%, multiplica ese resultado por 2. Si es 30%, por 3, etc.", "Paso 3: Si te piden el 5%, saca la mitad del valor obtenido en el Paso 1."],
    "ejemplos": [
        {"titulo": "Cálculo en restaurante", "enunciado": "La cuenta es de $18.000. Quieres dejar un 15% de propina. ¿Cuánto es mentalmente?", "solucion_pasos": ["Calculamos el 10%: Movemos un cero. Es $1.800.", "Calculamos el 5%: Es la mitad del 10%. La mitad de 1.800 es $900$.", "Sumamos ambos: $1.800 + 900 = 2.700$ de propina."]}
    ],
    "errores_frecuentes": ["Mover la coma dos espacios en lugar de uno (eso calcula el 1%, no el 10%).", "Tratar de multiplicar directamente por 0.15 mentalmente en lugar de desglosarlo en 10% + 5%."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCMENT10-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es la estrategia de cálculo mental más eficiente para encontrar el $10\\%$ de un número? (v{i})", "choices": ["A) Desplazar la coma decimal una posición hacia la izquierda (dividir por 10).", "B) Dividir el número a la mitad y restarle 10.", "C) Desplazar la coma decimal dos posiciones a la izquierda.", "D) Multiplicar el número por 10."], "correct_answer": "A) Desplazar la coma decimal una posición hacia la izquierda (dividir por 10).", "solution_steps": "$10\\% = 1/10$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCMENT10-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El $10\\%$ de $735$ es:", "choices": ["A) $73.5$", "B) $7.35$", "C) $7350$", "D) $0.735$"], "correct_answer": "A) $73.5$", "solution_steps": "Desplazar la coma un lugar a la izquierda: $73.5$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCMENT10-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Para calcular mentalmente el $20\\%$ de $400$, es válido decir: 'El $10\\%$ es $40$, entonces el doble es $80$'?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Desglose aditivo del porcentaje: $20\\% = 2 \\cdot 10\\%$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCMENT10-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un plan de internet de $\$24.000$ tendrá un incremento del $15\\%$ a partir del próximo mes. Utilizando estrategias de cálculo mental basadas en el $10\\%$ y el $5\\%$, ¿cuánto dinero subirá el plan exactamente? (v{i})", "choices": ["A) $\$3.600$", "B) $\$2.400$", "C) $\$1.200$", "D) $\$4.800$"], "correct_answer": "A) $\$3.600$", "solution_steps": "10% de 24.000 = 2.400. 5% de 24.000 = 1.200. Suma = 3.600.", "paes_style": True})

# 4. CALCULO_MENTAL_UNO
sid4 = "MAT.NUM.PORCENTAJES.CALCULO_MENTAL_UNO"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Aplicar la estrategia de cálculo mental rápida para el 1% y porcentajes de un dígito.",
    "introduccion": "Así como el 10% es tu herramienta para porcentajes grandes, saber aislar el 1% te permite calcular cirujías exactas como un 3% o un 7% sin escribir una sola fórmula.",
    "resumen": "Para hallar el 1% de cualquier número, divídelo por 100 (córrele la coma dos espacios a la izquierda). Luego multiplica por 2, 3 o 7 según el porcentaje que necesites.",
    "explicacion": "El **$1\\%$** equivale a la fracción $1/100$.\n\n**Regla de oro del 1%:**\nPara calcular el 1% de un número, mueve su punto decimal **dos posiciones a la izquierda**.\n- El 1% de 600 es 6.\n- El 1% de 45 es 0.45.\n\nUna vez que conoces el valor de la unidad porcentual básica (el 1%), calcular porcentajes precisos como el $3\\%$ es simplemente multiplicar ese valor base por 3.\n- **$4\\%$ de 300**: El 1% es 3. Multiplico $3 \\cdot 4 = 12$.",
    "procedimiento": ["Paso 1: Mueve la coma decimal dos lugares a la izquierda para obtener el 1%.", "Paso 2: Multiplica ese resultado por el dígito del porcentaje deseado.", "Paso 3: Verifica mentalmente que el número resultante sea bastante pequeño en relación al total."],
    "ejemplos": [
        {"titulo": "Cálculo de comisión", "enunciado": "Un corredor cobra un 3% de comisión por vender un auto de $8.000.000. ¿Cuánto es la comisión?", "solucion_pasos": ["Calculamos el 1%: Movemos la coma dos espacios. Es $80.000.", "Calculamos el 3%: Multiplicamos por 3. $80.000 \\cdot 3 = 240.000$.", "La comisión es $240.000."]}
    ],
    "errores_frecuentes": ["Mover la coma un solo espacio por accidente (calculando el 10% y luego multiplicando, lo que da números gigantes).", "No saber multiplicar números con decimales resultantes mentalmente (ej. el 2% de 15 es $0.15 \\cdot 2 = 0.30$)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCMENT1-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Para hallar rápidamente el $1\\%$ de un número de forma mental, la operación equivalente es: (v{i})", "choices": ["A) Desplazar la coma decimal dos lugares a la izquierda.", "B) Desplazar la coma decimal un lugar a la izquierda.", "C) Dividir el número por 1.", "D) Multiplicarlo por 0.1."], "correct_answer": "A) Desplazar la coma decimal dos lugares a la izquierda.", "solution_steps": "Equivale a dividir por 100.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCMENT1-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El $1\\%$ de $420$ es:", "choices": ["A) $4.2$", "B) $42$", "C) $0.42$", "D) $4200$"], "correct_answer": "A) $4.2$", "solution_steps": "Correr la coma 2 espacios: $4.20$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCMENT1-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Para calcular el $3\\%$ de $500$, calculas el $1\\%$ ($5$) y lo multiplicas por $3$ ($15$)?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$1\\% = 5$. $3 \\cdot 5 = 15$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCMENT1-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un arquitecto recibe un bono del $4\\%$ sobre los ahorros de un proyecto que ascienden a $\$1.200.000$. ¿Cuánto es el valor del bono recibido? (v{i})", "choices": ["A) $\$48.000$", "B) $\$4.800$", "C) $\$480.000$", "D) $\$12.000$"], "correct_answer": "A) $\$48.000$", "solution_steps": "El 1% es 12.000. El 4% es $12.000 \\cdot 4 = 48.000$.", "paes_style": True})

# 5. AUMENTO_CONCEPTO
sid5 = "MAT.NUM.VARIACION_PORCENTUAL.AUMENTO_CONCEPTO"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Comprender el concepto de aumento porcentual y sus aplicaciones.",
    "introduccion": "Cuando te suben el sueldo, el nuevo monto es tu sueldo antiguo MÁS un pedacito extra. Un aumento porcentual es sumar un porcentaje sobre un 100% que ya tenías.",
    "resumen": "Un aumento porcentual consiste en incrementar una cantidad base ($100\\%$) agregándole un $p\\%$. El nuevo valor corresponderá al $(100 + p)\\%$ del original.",
    "explicacion": "El **aumento porcentual** ocurre cuando una cantidad inicial crece. \nExisten dos formas matemáticas de calcular un valor después de un aumento del $A\\%$:\n\n**Método de 2 pasos (Suma):**\n1. Calculas de cuánto es el aumento: $Valor \\cdot (A / 100)$\n2. Se lo sumas al valor original: $Valor + Aumento$\n\n**Método de 1 paso (Factor de variación):**\nComo tienes el 100% original y le sumas un $A\\%$, en realidad pasas a tener el $(100 + A)\\%$ del valor.\n- Si algo aumenta un $20\\%$, el nuevo precio es el $120\\%$ del original.\n- Multiplicas el original por la fracción $120/100$ (o el decimal $1.20$).",
    "procedimiento": ["Paso 1: Identifica el porcentaje de aumento ($A\\%$).", "Paso 2: Suma ese aumento al $100\\%$ base (ej. $100 + 15 = 115\\%$).", "Paso 3: Multiplica la cantidad original por el factor decimal correspondiente (ej. $1.15$) para hallar el valor final en un solo paso."],
    "ejemplos": [
        {"titulo": "Aumento de precio", "enunciado": "Un pasaje de bus de $10.000 sube un 15% en temporada alta. ¿Cuál es el nuevo precio?", "solucion_pasos": ["Método 1 paso: Nuevo precio es $100\\% + 15\\% = 115\\%$.", "Decimal asociado: $1.15$.", "Multiplicamos: $10.000 \\cdot 1.15 = 11.500$.", "El nuevo precio es $11.500."]}
    ],
    "errores_frecuentes": ["Calcular el 15% y responder que ese es el nuevo precio, olvidando sumar el valor original.", "Creer que aumentar un 100% significa que el valor queda igual (aumentar un 100% significa doblar el precio, pasando a 200%)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"AUMENTOC-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Si a una cantidad $C$ se le aplica un aumento porcentual del $20\\%$, matemáticamente es equivalente a decir que la nueva cantidad corresponde al: (v{i})", "choices": ["A) $120\\%$ de $C$.", "B) $20\\%$ de $C$.", "C) $80\\%$ de $C$.", "D) $200\\%$ de $C$."], "correct_answer": "A) $120\\%$ de $C$.", "solution_steps": "$100\\% + 20\\% = 120\\%$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"AUMENTOC-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Para aumentar un valor en un $8\\%$ en un solo paso, puedes multiplicar el valor original por el factor decimal:", "choices": ["A) $1.08$", "B) $0.08$", "C) $1.8$", "D) $0.92$"], "correct_answer": "A) $1.08$", "solution_steps": "$100\\% + 8\\% = 108\\% = 1.08$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"AUMENTOC-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Un aumento del $100\\%$ sobre el precio de un artículo significa que el artículo ahora vale el doble?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$100\\% (original) + 100\\% (aumento) = 200\\%$, que equivale a multiplicar por 2.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"AUMENTOC-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"El valor de una acción en la bolsa era de $\$800$ y experimentó un aumento del $15\\%$ durante la mañana. ¿Qué expresión permite calcular el nuevo valor de la acción en un solo paso? (v{i})", "choices": ["A) $800 \\cdot 1.15$", "B) $800 \\cdot 0.15$", "C) $800 + 0.15$", "D) $800 \\cdot 115$"], "correct_answer": "A) $800 \\cdot 1.15$", "solution_steps": "Factor de aumento: $1 + (15/100) = 1.15$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 10...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 10...")
    append_jsonl("mat-num-razones-banco-gen-10", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-10.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()

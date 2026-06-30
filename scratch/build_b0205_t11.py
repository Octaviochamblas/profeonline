# scratch/build_b0205_t11.py
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

# 1. DISMINUCION_CONCEPTO
sid1 = "MAT.NUM.VARIACION_PORCENTUAL.DISMINUCION_CONCEPTO"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Comprender el concepto de disminución porcentual y sus aplicaciones matemáticas.",
    "introduccion": "Si la batería de tu celular cae de un 100% a un 80%, experimentaste una disminución del 20%. En la vida, el valor de los autos, la población de algunas ciudades y los precios suelen experimentar disminuciones porcentuales constantes.",
    "resumen": "Una disminución porcentual consiste en restar un porcentaje $p\\%$ al $100\\%$ original. El nuevo valor corresponde al $(100 - p)\\%$ de la cantidad inicial.",
    "explicacion": "La **disminución porcentual** indica cuánto se reduce una cantidad inicial.\nAl igual que en los aumentos, existen dos métodos lógicos:\n\n**Método de 2 pasos (Resta):**\n1. Calculas el valor de la disminución: $Valor \\cdot (D / 100)$\n2. Se lo restas al valor original: $Valor - Disminución$\n\n**Método de 1 paso (Factor de variación):**\nSi al $100\\%$ le quitas un $D\\%$, te quedas con el $(100 - D)\\%$.\n- Si la cantidad disminuye un $30\\%$, significa que te quedaste con el $70\\%$ del valor original.\n- Para calcularlo rápido, multiplicas por el decimal correspondiente al nuevo porcentaje ($0.70$).",
    "procedimiento": ["Paso 1: Identifica qué porcentaje se va a disminuir ($D\\%$).", "Paso 2: Réstale ese porcentaje a 100 (ej. $100 - 30 = 70\\%$).", "Paso 3: El nuevo valor será el $70\\%$ del original. Multiplícalo por $0.70$."],
    "ejemplos": [
        {"titulo": "Caída de acciones", "enunciado": "Una acción valía $5.000 y disminuyó su valor en un 12%. ¿Cuánto vale ahora?", "solucion_pasos": ["Calculamos el nuevo porcentaje: $100\\% - 12\\% = 88\\%$.", "Multiplicamos el valor original por el factor de variación: $5.000 \\cdot 0.88$.", "Resultado: $4.400. Ese es el nuevo valor."]}
    ],
    "errores_frecuentes": ["Calcular el 12% y decir que ese es el nuevo precio (olvidar restar del total).", "Multiplicar por $1.12$ en vez de $0.88$, confundiendo disminución con aumento."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"DISMINC-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Si un artículo sufre una disminución porcentual del $25\\%$, esto significa que su nuevo valor corresponde al: (v{i})", "choices": ["A) $75\\%$ del valor original.", "B) $25\\%$ del valor original.", "C) $125\\%$ del valor original.", "D) $100\\%$ del valor original."], "correct_answer": "A) $75\\%$ del valor original.", "solution_steps": "$100\\% - 25\\% = 75\\%$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"DISMINC-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Para aplicar una disminución del $15\\%$ en un solo paso, debes multiplicar el valor original por:", "choices": ["A) $0.85$", "B) $1.15$", "C) $0.15$", "D) $8.5$"], "correct_answer": "A) $0.85$", "solution_steps": "$100\\% - 15\\% = 85\\%$, que en decimal es $0.85$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"DISMINC-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si un vehículo disminuye su precio en un $10\\%$, su nuevo valor se calcula multiplicando el precio original por $0.90$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$100\\% - 10\\% = 90\\%$, que es $0.90$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"DISMINC-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"La cantidad de bacterias en una muestra era de $4.000$. Tras aplicar un antibiótico, la población disminuyó en un $35\\%$. ¿Cuál es la expresión que determina la cantidad final de bacterias? (v{i})", "choices": ["A) $4000 \\cdot 0.65$", "B) $4000 \\cdot 0.35$", "C) $4000 - 35$", "D) $4000 \\cdot 1.35$"], "correct_answer": "A) $4000 \\cdot 0.65$", "solution_steps": "$100\\% - 35\\% = 65\\%$. El factor decimal es $0.65$.", "paes_style": True})

# 2. DESCUENTO_CONCEPTO
sid2 = "MAT.NUM.VARIACION_PORCENTUAL.DESCUENTO_CONCEPTO"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Diferenciar entre el valor del descuento y el valor final en contextos comerciales.",
    "introduccion": "Vas al mall y ves '50% de Descuento'. Tu cerebro se emociona porque sabe que pagará la mitad. El descuento es la disminución porcentual más famosa del mundo.",
    "resumen": "En el comercio, 'Descuento' se refiere al monto de dinero que te restan (el $D\\%$), mientras que 'Precio Final' o 'Precio con Descuento' es lo que efectivamente pagas (el $(100-D)\\%$).",
    "explicacion": "En problemas comerciales, es vital leer con lupa lo que se está preguntando:\n\n- **Valor del descuento (la rebaja):** Es la cantidad de dinero que NO vas a pagar. Se calcula como $\\text{Precio Original} \\cdot (D / 100)$.\n- **Precio final (lo que pagas):** Es el precio original menos la rebaja. Se calcula más rápido con el factor de disminución: $\\text{Precio Original} \\cdot ((100 - D) / 100)$.\n\nPor ejemplo, en un pantalón de $\$10.000$ con un $30\\%$ de descuento:\n- La rebaja es de $\$3.000$ ($30\\%$).\n- El precio final que te cobrará el cajero es de $\$7.000$ ($70\\%$).",
    "procedimiento": ["Paso 1: Lee si la pregunta pide 'el valor del descuento' (la rebaja) o el 'precio final' (lo que pagas).", "Paso 2: Si pide el descuento, calcula el $D\\%$ del total.", "Paso 3: Si pide el precio final, calcula el $(100 - D)\\%$ del total."],
    "ejemplos": [
        {"titulo": "Liquidación de temporada", "enunciado": "Una bicicleta vale $100.000. Tiene un 40% de descuento. ¿Cuál es el valor del descuento y cuál es el precio final?", "solucion_pasos": ["Descuento (rebaja): El 40% de 100.000. Son $40.000. Ese dinero te lo ahorras.", "Precio final: El 60% de 100.000 (ya que $100 - 40 = 60$). Son $60.000. Eso pagas en caja."]}
    ],
    "errores_frecuentes": ["Confundir el valor del descuento con el precio a pagar. (Responder que pagas $40.000 en el ejemplo anterior).", "Creer que dos descuentos consecutivos del 20% suman un 40% (no es así, el segundo descuento se aplica sobre el nuevo precio ya rebajado)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"DSCTOC-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Si un producto de precio $P$ tiene un descuento del $D\\%$, ¿qué expresión matemática representa el 'monto descontado' (la rebaja) y no el precio final? (v{i})", "choices": ["A) $P \\cdot (D / 100)$", "B) $P \\cdot ((100 - D) / 100)$", "C) $P - D$", "D) $P + (D / 100)$"], "correct_answer": "A) $P \\cdot (D / 100)$", "solution_steps": "La rebaja es simplemente el D% aplicado a P.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"DSCTOC-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "En una tienda, una chaqueta de $\$50.000$ tiene un $20\\%$ de descuento. Lo que pagas en caja (precio final) equivale al:", "choices": ["A) $80\\%$ de $\$50.000$", "B) $20\\%$ de $\$50.000$", "C) $120\\%$ de $\$50.000$", "D) $100\\%$ de $\$50.000$"], "correct_answer": "A) $80\\%$ de $\$50.000$", "solution_steps": "Pagas $100\\% - 20\\% = 80\\%$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"DSCTOC-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si compras un pasaje con un $15\\%$ de descuento, pagas el $85\\%$ de su valor original?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$100 - 15 = 85$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"DSCTOC-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un sofá está marcado con un precio de etiqueta de $\$200.000$. En caja le aplican un descuento del $30\\%$. El cajero se equivoca y, en lugar de cobrar el precio final, te cobra el 'valor del descuento'. ¿Cuánto dinero te cobró erróneamente el cajero? (v{i})", "choices": ["A) $\$60.000$", "B) $\$140.000$", "C) $\$200.000$", "D) $\$30.000$"], "correct_answer": "A) $\$60.000$", "solution_steps": "El valor del descuento es el $30\\%$ de $200.000$, lo cual es $60.000$. (El precio final correcto era $140.000$).", "paes_style": True})

# 3. CAMBIO_ABSOLUTO
sid3 = "MAT.NUM.VARIACION_PORCENTUAL.CAMBIO_ABSOLUTO"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Calcular y diferenciar el cambio absoluto en contextos de variación matemática.",
    "introduccion": "Si antes pesabas 70 kg y ahora pesas 65 kg, perdiste 5 kilos. Esos 5 kilos son tu 'cambio absoluto'. No tiene que ver con porcentajes aún, es simplemente la diferencia real en números.",
    "resumen": "El cambio absoluto es la diferencia matemática cruda entre un Valor Final y un Valor Inicial ($Variación = Final - Inicial$).",
    "explicacion": "Antes de hablar de porcentajes de crecimiento, debemos definir el **Cambio Absoluto** o **Variación Absoluta**.\n\nFórmula matemática:\n$$\\text{Cambio Absoluto} = \\text{Valor Final} - \\text{Valor Inicial}$$\n\n- Si el número da **positivo**, hubo un aumento.\n- Si el número da **negativo**, hubo una disminución.\n\nEjemplo: Si tu cuenta de ahorros pasó de tener $\$10.000$ (inicial) a $\$12.000$ (final), el cambio absoluto es $12.000 - 10.000 = +2.000$. \nEs 'absoluto' porque se expresa en la unidad original de medida (pesos, kilos, metros), no en un porcentaje.",
    "procedimiento": ["Paso 1: Identifica el Valor Inicial (el dato del pasado o el original).", "Paso 2: Identifica el Valor Final (el dato del presente o el nuevo).", "Paso 3: Resta $Final - Inicial$ para hallar la variación neta."],
    "ejemplos": [
        {"titulo": "Crecimiento poblacional", "enunciado": "En 2020 habían 500 alumnos. En 2021 habían 450. ¿Cuál es el cambio absoluto?", "solucion_pasos": ["Inicial = 500, Final = 450.", "Cambio Absoluto = $450 - 500 = -50$.", "Hubo una disminución de 50 alumnos."]}
    ],
    "errores_frecuentes": ["Restar siempre el mayor menos el menor, ignorando el orden de tiempo. (Si restas Inicial - Final te dará el signo equivocado y podrías reportar un aumento cuando fue una caída).", "Expresar el resultado con un símbolo $\%$ (el cambio absoluto NO es un porcentaje)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CAMBABS-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cómo se calcula correctamente el cambio absoluto entre dos cantidades en el tiempo? (v{i})", "choices": ["A) Valor Final menos Valor Inicial.", "B) Valor Inicial menos Valor Final.", "C) Valor Final dividido por Valor Inicial.", "D) (Valor Final menos Valor Inicial) dividido por 100."], "correct_answer": "A) Valor Final menos Valor Inicial.", "solution_steps": "La variación neta sigue la cronología Final - Inicial.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"CAMBABS-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si el precio de la bencina subió de $\$1000$ a $\$1050$, el cambio absoluto es:", "choices": ["A) $+\$50$", "B) $-\$50$", "C) $50\\%$", "D) $1.05$"], "correct_answer": "A) $+\$50$", "solution_steps": "$1050 - 1000 = 50$. No es porcentaje.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CAMBABS-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si las ventas caen de $200$ a $150$, el cambio absoluto es de $-50$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$150 - 200 = -50$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CAMBABS-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una empresa registraba una deuda de $\$12.500.000$ a principios de año. A final de año, su deuda se sitúa en $\$10.000.000$. ¿Cuál fue la variación absoluta de la deuda de la empresa? (v{i})", "choices": ["A) $-\$2.500.000$", "B) $+\$2.500.000$", "C) $-\$10.000.000$", "D) $-20\\%$"], "correct_answer": "A) $-\$2.500.000$", "solution_steps": "Final - Inicial = $10.000.000 - 12.500.000 = -2.500.000$.", "paes_style": True})

# 4. CAMBIO_RELATIVO
sid4 = "MAT.NUM.VARIACION_PORCENTUAL.CAMBIO_RELATIVO"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Calcular la variación porcentual (cambio relativo) entre dos cantidades.",
    "introduccion": "Si a un billonario se le pierden 1.000 pesos, no le importa. Si a ti se te pierden 1.000 pesos, ¡es un problema! El cambio absoluto es igual, pero el 'Cambio Relativo' (el impacto) es gigante para ti. Eso es el cambio relativo: medir el impacto respecto al origen.",
    "resumen": "El cambio relativo o variación porcentual indica qué porcentaje creció o disminuyó una cantidad. Se calcula: $((Final - Inicial) / Inicial) \\cdot 100$.",
    "explicacion": "El **Cambio Relativo** transforma la diferencia absoluta en un porcentaje respecto al Valor Inicial. Nos permite comparar justamente.\n\nFórmula fundamental:\n$$\\text{Variación } \\% = \\left( \\frac{\\text{Valor Final} - \\text{Valor Inicial}}{\\text{Valor Inicial}} \\right) \\cdot 100$$\n\n- O más simple: **$\\frac{\\text{Cambio Absoluto}}{\\text{Valor Inicial}} \\cdot 100$**\n\nSi el resultado es positivo (ej. $+15\\%$), hubo un crecimiento del 15%. Si es negativo (ej. $-10\\%$), hubo una contracción o descuento del 10%.",
    "procedimiento": ["Paso 1: Calcula el cambio absoluto ($Final - Inicial$).", "Paso 2: Divide ese cambio por el Valor Inicial.", "Paso 3: Multiplica por 100 para llevarlo a formato de porcentaje."],
    "ejemplos": [
        {"titulo": "Porcentaje de inflación", "enunciado": "Un kilo de pan costaba $1.000 y ahora cuesta $1.200. ¿Qué porcentaje aumentó?", "solucion_pasos": ["Cambio absoluto: $1200 - 1000 = 200$.", "Dividimos por el Inicial: $200 / 1000 = 0.2$.", "Multiplicamos por 100: $0.2 \\cdot 100 = 20\\%$. Aumentó un 20%."]}
    ],
    "errores_frecuentes": ["Dividir el cambio absoluto por el Valor Final en lugar del Inicial (¡Gravísimo error!).", "Restar Inicial menos Final, lo que invierte los signos de crecimiento/disminución."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CAMBREL-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En la fórmula para calcular la variación porcentual entre dos valores en el tiempo, el denominador debe ser siempre: (v{i})", "choices": ["A) El Valor Inicial.", "B) El Valor Final.", "C) El número 100.", "D) El Cambio Absoluto."], "correct_answer": "A) El Valor Inicial.", "solution_steps": "El impacto se mide respecto a cómo empezó todo (la base es el Valor Inicial).", "paes_style": False})
EJERCICIOS.append({"stable_id": f"CAMBREL-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si el precio de un bien pasa de $\$50$ a $\$100$, su variación porcentual es un aumento del:", "choices": ["A) $100\\%$", "B) $50\\%$", "C) $200\\%$", "D) $150\\%$"], "correct_answer": "A) $100\\%$", "solution_steps": "$(100 - 50) / 50 = 50 / 50 = 1$. Multiplicado por 100 = $100\\%$. (Es decir, se duplicó).", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CAMBREL-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si tus seguidores en una red social bajan de 10.000 a 8.000, tuviste una variación porcentual del $-20\\%$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$(8000 - 10000)/10000 = -2000/10000 = -0.2 = -20\\%$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CAMBREL-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una zapatilla costaba originalmente $\$40.000$. En época de rebajas bajó su precio a $\$30.000$. ¿Cuál fue el porcentaje de descuento (variación porcentual negativa) aplicado? (v{i})", "choices": ["A) $25\\%$", "B) $33.3\\%$", "C) $10\\%$", "D) $75\\%$"], "correct_answer": "A) $25\\%$", "solution_steps": "Cambio absoluto: $30.000 - 40.000 = -10.000$. Variación = $(-10.000 / 40.000) \\cdot 100 = -0.25 \\cdot 100 = -25\\%$. El descuento fue de un 25%.", "paes_style": True})

# 5. VALOR_FINAL_AUMENTO
sid5 = "MAT.NUM.VARIACION_PORCENTUAL.VALOR_FINAL_AUMENTO"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Calcular el valor final tras aplicar un aumento porcentual en un solo paso.",
    "introduccion": "Si trabajas en comercio, no tienes tiempo para calcular el impuesto (IVA) y luego sumarlo al producto a mano en la calculadora en dos pasos. Tienes que saber hacerlo multiplicando por un solo número mágico.",
    "resumen": "Para aplicar un aumento del $A\\%$ en un solo paso, debes multiplicar el Valor Inicial por el factor multiplicador: $(1 + A/100)$. Ej: Aumentar 19% es multiplicar por $1.19$.",
    "explicacion": "Profundizamos el concepto del factor de variación.\nLa fórmula para hallar el Valor Final tras un aumento del $A\\%$ es:\n\n$$\\text{Valor Final} = \\text{Valor Inicial} \\cdot \\left( 1 + \\frac{A}{100} \\right)$$\n\nEse paréntesis $(1 + A/100)$ se conoce como **factor multiplicador**.\n- Si el IVA es $19\\%$, el factor es $1 + 0.19 = 1.19$. Si multiplicas el precio neto por $1.19$, obtienes inmediatamente el precio con IVA incluido.\n- Si hay un aumento inflacionario del $4\\%$, el factor es $1 + 0.04 = 1.04$. (¡Cuidado con poner $1.4$, eso sería un $40\\%$!).",
    "procedimiento": ["Paso 1: Escribe el porcentaje de aumento como un decimal (dividiendo por 100).", "Paso 2: Súmale 1 entero a ese decimal. Este es tu factor multiplicador.", "Paso 3: Multiplica el Valor Inicial por este factor."],
    "ejemplos": [
        {"titulo": "Precio con IVA", "enunciado": "Un monitor cuesta $100.000 neto. Si el IVA es del 19%, ¿cuál es el precio bruto (final)?", "solucion_pasos": ["Convertimos 19% a decimal: $0.19$.", "Sumamos 1: El factor es $1.19$.", "Multiplicamos: $100.000 \\cdot 1.19 = 119.000$.", "El precio final es $119.000."]}
    ],
    "errores_frecuentes": ["Confundir el factor de aumento del 5% ($1.05$) con el del 50% ($1.5$).", "Multiplicar solo por $0.19$ (obteniendo el valor del impuesto y olvidando sumar el 1 inicial)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"VFAUMENTO-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es el 'factor multiplicador' para aplicar directamente un aumento del $7\\%$ a una cantidad? (v{i})", "choices": ["A) $1.07$", "B) $1.7$", "C) $0.07$", "D) $0.93$"], "correct_answer": "A) $1.07$", "solution_steps": "$1 + (7/100) = 1 + 0.07 = 1.07$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"VFAUMENTO-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si multiplicas un número por $1.25$, en realidad le estás aplicando un aumento del:", "choices": ["A) $25\\%$", "B) $1.25\\%$", "C) $125\\%$", "D) $20\\%$"], "correct_answer": "A) $25\\%$", "solution_steps": "$1.25$ equivale a $1 + 0.25$, lo que significa un aumento del 25%.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"VFAUMENTO-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El precio final de un artículo de $\$1000$ tras un alza del $6\\%$ se obtiene multiplicando $1000 \\cdot 1.06$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$1 + 0.06 = 1.06$. $1000 \\cdot 1.06 = 1060$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"VFAUMENTO-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un trabajador ganaba $\$500.000$. En su renegociación de contrato le prometen un reajuste salarial del $4.5\\%$. ¿Qué cálculo le permite obtener el monto de su nuevo sueldo final en un solo paso? (v{i})", "choices": ["A) $500.000 \\cdot 1.045$", "B) $500.000 \\cdot 1.45$", "C) $500.000 \\cdot 0.045$", "D) $500.000 + 4.5$"], "correct_answer": "A) $500.000 \\cdot 1.045$", "solution_steps": "$4.5\\% = 0.045$. Factor = $1 + 0.045 = 1.045$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 11...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 11...")
    append_jsonl("mat-num-razones-banco-gen-11", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-11.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()

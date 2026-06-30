# scratch/build_b0205_t8.py
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

# 1. ESCALA_RAZON
sid1 = "MAT.NUM.REPARTO_ESCALAS.ESCALA_RAZON"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Comprender e interpretar el concepto de escala como una razón matemática.",
    "introduccion": "¿Cómo cabe el mapa de todo un país en la pantalla de tu celular? Gracias a las escalas. Una escala es simplemente una promesa matemática: 'Por cada centímetro que veas aquí, en la vida real hay tantos más'.",
    "resumen": "Una escala es una razón entre la medida del dibujo (plano) y la medida real del objeto, expresadas en la misma unidad de medida. Se anota comúnmente como 1:E.",
    "explicacion": "Una **escala** es una aplicación directa del concepto de razón. Compara la dimensión de un objeto en una representación (mapa, maqueta, plano) con su dimensión en la realidad.\n\nFórmula fundamental de la escala:\n$$Escala = \\frac{\\text{Medida en el Plano}}{\\text{Medida en la Realidad}}$$\n\nSe suele escribir en la forma **1 : E** (por ejemplo, 1:100), lo que significa que **1 unidad** en el plano equivale a **E unidades** en la realidad. ¡Ojo! Ambas deben estar en la misma unidad de medida (si el plano está en cm, la realidad en la razón también está en cm).",
    "procedimiento": ["Paso 1: Lee la escala en el formato 1:E.", "Paso 2: Recuerda que el '1' representa el dibujo y la 'E' representa la realidad.", "Paso 3: Interpreta: '1 cm en el mapa son E cm en la vida real'."],
    "ejemplos": [
        {"titulo": "Escala de un mapa", "enunciado": "¿Qué significa que un mapa tenga escala 1:50.000?", "solucion_pasos": ["El primer número (1) es el plano. El segundo (50.000) es la realidad.", "Significa que 1 centímetro en el mapa equivale a 50.000 centímetros reales.", "(Que equivalen a 500 metros)."]},
        {"titulo": "Escala de ampliación", "enunciado": "¿Qué significa una escala 10:1 en un microscopio?", "solucion_pasos": ["Significa que el dibujo o lente muestra 10 unidades por cada 1 unidad real.", "Es una ampliación (el dibujo es más grande que la realidad)."]}
    ],
    "errores_frecuentes": ["Creer que la escala 1:100 significa que 1 cm equivale a 100 metros (son 100 centímetros, o sea 1 metro).", "Invertir los números creyendo que 100:1 es una reducción.", "Olvidar que las escalas son adimensionales (no llevan la palabra 'cm' pegada en la razón)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"ESCALACONC-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cómo se define matemáticamente una escala de representación? (v{i})", "choices": ["A) Como la razón entre la medida en el dibujo y la medida en la realidad.", "B) Como la suma de la medida del dibujo y la medida real.", "C) Como la diferencia entre el tamaño real y el plano.", "D) Como la medida real dividida por la medida en el plano."], "correct_answer": "A) Como la razón entre la medida en el dibujo y la medida en la realidad.", "solution_steps": "Plano:Realidad.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"ESCALACONC-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Una escala $1:200$ significa que:", "choices": ["A) $1$ unidad en el plano equivale a $200$ unidades en la realidad.", "B) $200$ cm en el plano equivalen a $1$ cm en la realidad.", "C) $1$ cm en el plano equivale a $200$ metros en la realidad.", "D) El objeto real es $200$ veces más pequeño."], "correct_answer": "A) $1$ unidad en el plano equivale a $200$ unidades en la realidad.", "solution_steps": "La misma unidad aplica para el antecedente y el consecuente.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"ESCALACONC-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Una escala $5:1$ se utiliza para dibujar cosas microscópicas (ampliación)?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "El dibujo es 5 veces más grande que la realidad.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"ESCALACONC-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un arquitecto menciona que su maqueta está en escala $1:50$. Si el cliente le pregunta qué significa eso en la práctica, el arquitecto debería responder correctamente que: (v{i})", "choices": ["A) Cada centímetro que mida en la maqueta representará medio metro ($50$ cm) en la casa real.", "B) Cada centímetro en la maqueta representa $50$ metros en la realidad.", "C) La maqueta es $50$ veces más grande que la casa real.", "D) Se necesitan $50$ maquetas para igualar el tamaño de la casa."], "correct_answer": "A) Cada centímetro que mida en la maqueta representará medio metro ($50$ cm) en la casa real.", "solution_steps": "1:50 significa 1 cm plano = 50 cm realidad. Y 50 cm = 0.5 metros.", "paes_style": True})

# 2. LONGITUD_PLANO
sid2 = "MAT.NUM.REPARTO_ESCALAS.LONGITUD_PLANO"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Calcular la longitud de un objeto en un plano a partir de su medida real y la escala.",
    "introduccion": "Si sabes que tu habitación mide 4 metros de largo y quieres dibujarla en un plano 1:100, ¿de cuántos centímetros debe ser la línea que traces? Convertir lo real a papel es clave en el diseño.",
    "resumen": "Para hallar la medida en el plano, divide la medida real (convertida a la unidad del plano) por el factor de escala ($E$).",
    "explicacion": "Al usar la fórmula $\\text{Escala} = \\frac{\\text{Plano}}{\\text{Realidad}}$, si queremos calcular la medida en el **Plano** despejamos:\n\n$$\\text{Plano} = \\frac{\\text{Realidad}}{E}$$\n(donde $E$ es el consecuente de la escala $1:E$).\n\n**¡Cuidado con las unidades!** Si la realidad está en kilómetros o metros, primero debes convertirla a centímetros (la unidad típica del plano) multiplicando por $100.000$ o por $100$ respectivamente, y luego hacer la división.",
    "procedimiento": ["Paso 1: Convierte la medida real a la unidad en la que vas a dibujar (generalmente centímetros).", "Paso 2: Toma la escala $1:E$ y fíjate en el número $E$.", "Paso 3: Divide la medida real (ya convertida) por $E$. Ese es tu tamaño de dibujo."],
    "ejemplos": [
        {"titulo": "Dibujando una pared", "enunciado": "Pared real de 5 metros. Escala 1:50. ¿Cuánto mide en el plano?", "solucion_pasos": ["Convertimos 5 metros a centímetros: $5 \\cdot 100 = 500$ cm.", "La escala dice $E = 50$.", "Dividimos: $500 / 50 = 10$ cm. En el plano medirás 10 cm."]}
    ],
    "errores_frecuentes": ["Dividir los metros sin convertirlos a centímetros (ej. $5/50 = 0.1$ cm).", "Multiplicar en lugar de dividir (obteniendo un plano más grande que la realidad)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"LONGPLANO-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Para encontrar la medida en un plano (escala 1:E) dada la medida real, la operación matemática correcta es: (v{i})", "choices": ["A) Dividir la medida real (en las mismas unidades) por $E$.", "B) Multiplicar la medida real por $E$.", "C) Sumar $E$ a la medida real.", "D) Elevar la medida real al cuadrado."], "correct_answer": "A) Dividir la medida real (en las mismas unidades) por $E$.", "solution_steps": "Plano = Real / E.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"LONGPLANO-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Una ruta real mide $100.000$ cm. En un mapa $1:10.000$, la ruta se dibuja con una longitud de:", "choices": ["A) $10$ cm", "B) $1$ cm", "C) $100$ cm", "D) $1.000$ cm"], "correct_answer": "A) $10$ cm", "solution_steps": "$100.000 / 10.000 = 10$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"LONGPLANO-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si un árbol mide 4 metros, en escala $1:100$ se dibuja de 4 cm?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$4m = 400cm$. $400/100 = 4cm$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"LONGPLANO-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un ingeniero debe dibujar un acueducto recto de $2.5$ km de largo en un plano con escala $1:50.000$. ¿De cuántos centímetros será el trazo que debe dibujar? (v{i})", "choices": ["A) $5$ cm", "B) $0.05$ cm", "C) $50$ cm", "D) $12.5$ cm"], "correct_answer": "A) $5$ cm", "solution_steps": "2.5 km = 2.500 m = 250.000 cm. Plano = $250.000 / 50.000 = 5$ cm.", "paes_style": True})

# 3. LONGITUD_REAL
sid3 = "MAT.NUM.REPARTO_ESCALAS.LONGITUD_REAL"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Calcular la longitud real de un objeto a partir de su medida en el plano y la escala.",
    "introduccion": "¿Alguna vez has puesto una regla sobre un mapa para calcular a cuántos kilómetros está una ciudad de otra? Ese acto tan simple encierra la matemática de revertir una escala.",
    "resumen": "Para hallar la medida real, multiplica la medida del plano por el factor de escala ($E$). El resultado estará en la misma unidad que usaste para medir el plano.",
    "explicacion": "Partiendo de $\\frac{\\text{Plano}}{\\text{Realidad}} = \\frac{1}{E}$, si despejamos la medida **Real** obtenemos:\n\n$$\\text{Realidad} = \\text{Plano} \\cdot E$$\n\nEste cálculo te devolverá un número muy grande, porque estará **en centímetros** (asumiendo que mediste el mapa con una regla en cm). Para darle sentido en la vida real, deberás convertirlo:\n- A metros: dividiendo por $100$.\n- A kilómetros: dividiendo por $100.000$.",
    "procedimiento": ["Paso 1: Mide con una regla la distancia en el plano (en cm).", "Paso 2: Multiplica esa medida por el factor $E$ de la escala $1:E$.", "Paso 3: El resultado está en centímetros reales. Conviértelo a metros (divide por 100) o a km (divide por 100.000)."],
    "ejemplos": [
        {"titulo": "Distancia entre ciudades", "enunciado": "En un mapa 1:500.000, dos ciudades están a 4 cm de distancia. ¿Cuál es su distancia real?", "solucion_pasos": ["Multiplicamos: $4 \\cdot 500.000 = 2.000.000$ cm reales.", "Convertimos a km: $2.000.000 / 100.000 = 20$ kilómetros.", "La distancia real es 20 km."]}
    ],
    "errores_frecuentes": ["Creer que el resultado de la multiplicación ya está en kilómetros.", "Dividir por la escala en lugar de multiplicar (hallando medidas microscópicas irreales).", "Equivocarse en los ceros al convertir de centímetros a kilómetros."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"LONGREAL-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Si mides una distancia en centímetros sobre un mapa con escala $1:E$, ¿qué debes hacer para conocer la distancia en la realidad? (v{i})", "choices": ["A) Multiplicar la medida obtenida por $E$, y el resultado estará en centímetros.", "B) Dividir la medida obtenida por $E$.", "C) Multiplicar la medida por $E$, y el resultado ya estará en kilómetros.", "D) Sumar $E$ a la medida obtenida."], "correct_answer": "A) Multiplicar la medida obtenida por $E$, y el resultado estará en centímetros.", "solution_steps": "Real = Plano * E, misma unidad.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"LONGREAL-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "En un plano $1:50$, una puerta mide $2$ cm de ancho. Su ancho real en centímetros es:", "choices": ["A) $100$ cm", "B) $25$ cm", "C) $0.04$ cm", "D) $50$ cm"], "correct_answer": "A) $100$ cm", "solution_steps": "$2 \\cdot 50 = 100$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"LONGREAL-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si en escala $1:1.000.000$ mides $3$ cm, la realidad son $30$ km?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$3 \\cdot 1.000.000 = 3.000.000$ cm $= 30.000$ m $= 30$ km.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"LONGREAL-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una familia revisa un plano habitacional con escala $1:150$. Si el largo del dormitorio principal en el plano es de $4$ cm, ¿cuál es el largo real del dormitorio en metros? (v{i})", "choices": ["A) $6$ metros", "B) $0.6$ metros", "C) $60$ metros", "D) $37.5$ metros"], "correct_answer": "A) $6$ metros", "solution_steps": "$4 \\cdot 150 = 600$ cm. $600 / 100 = 6$ metros.", "paes_style": True})

# 4. ESCALA_DESCONOCIDA
sid4 = "MAT.NUM.REPARTO_ESCALAS.ESCALA_DESCONOCIDA"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Calcular la escala de un plano conociendo una medida del dibujo y su equivalente real.",
    "introduccion": "Imagina que encuentras un mapa viejo sin leyenda, pero logras identificar la distancia entre dos ciudades conocidas. Con esa simple información, puedes 'desencriptar' la escala que usó el cartógrafo.",
    "resumen": "Para hallar la escala $1:E$, convierte la medida real a la misma unidad del plano y divídela por la medida del plano ($E = \\text{Realidad} / \\text{Plano}$).",
    "explicacion": "Si tenemos la medida en el **Plano** y la medida en la **Realidad**, encontrar la escala $1:E$ se reduce a despejar $E$ de la fórmula:\n\n$$E = \\frac{\\text{Realidad}}{\\text{Plano}}$$\n\n**Regla de oro:** Ambas medidas deben estar forzosamente en la **misma unidad** (sugerimos centímetros) antes de hacer la división. El resultado $E$ te dirá que la escala es $1:E$.",
    "procedimiento": ["Paso 1: Convierte la medida de la Realidad a la unidad de la medida del Plano (ej. de km a cm).", "Paso 2: Divide la Realidad por el Plano.", "Paso 3: El número resultante es el factor $E$. La escala se escribe $1:E$."],
    "ejemplos": [
        {"titulo": "Descifrando la escala", "enunciado": "Un parque de 200 metros de largo está dibujado en un papel con una longitud de 10 cm. ¿Qué escala se usó?", "solucion_pasos": ["Convertimos la realidad a cm: $200 \\text{ m} = 20.000$ cm.", "Dividimos realidad entre plano: $20.000 / 10 = 2.000$.", "El factor $E$ es 2.000. La escala del dibujo es 1:2.000."]}
    ],
    "errores_frecuentes": ["Dividir el plano por la realidad (obteniendo un número decimal absurdo como 0.0005).", "Hacer la división sin haber igualado las unidades de medida (ej. dividir 200 metros / 10 cm = 20 $\\rightarrow$ escala 1:20 es incorrecto)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"ESCALADESC-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Para descubrir el factor $E$ de una escala desconocida $1:E$, debes: (v{i})", "choices": ["A) Dividir la medida real (en cm) por la medida del plano (en cm).", "B) Dividir la medida del plano por la medida real.", "C) Multiplicar ambas medidas.", "D) Sumar ambas medidas en la misma unidad."], "correct_answer": "A) Dividir la medida real (en cm) por la medida del plano (en cm).", "solution_steps": "$E = Real/Plano$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"ESCALADESC-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si en la realidad algo mide $1.000$ cm y en el plano mide $5$ cm, la escala es:", "choices": ["A) $1:200$", "B) $1:5.000$", "C) $1:500$", "D) $1:20$"], "correct_answer": "A) $1:200$", "solution_steps": "$1.000 / 5 = 200$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"ESCALADESC-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si $2$ km reales se dibujan como $10$ cm, la escala es $1:20.000$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$2km = 200.000cm$. $200.000 / 10 = 20.000$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"ESCALADESC-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al fotocopiar un mapa original, se ha perdido la indicación de su escala. Sin embargo, se sabe que la distancia en línea recta entre la ciudad A y la ciudad B es de $40$ km. Al medir esa distancia con una regla en la fotocopia, marca exactamente $8$ cm. ¿Cuál es la nueva escala de la fotocopia? (v{i})", "choices": ["A) $1:500.000$", "B) $1:5.000$", "C) $1:50.000$", "D) $1:320.000$"], "correct_answer": "A) $1:500.000$", "solution_steps": "Real = 40 km = 4.000.000 cm. Plano = 8 cm. E = $4.000.000 / 8 = 500.000$.", "paes_style": True})

# 5. RAZON_CIEN (INICIO PORCENTAJES)
sid5 = "MAT.NUM.PORCENTAJES.RAZON_CIEN"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Comprender el porcentaje como una razón con denominador 100.",
    "introduccion": "Cuando decimos que tu teléfono tiene 100% de batería, significa que está completamente lleno. El número 100 es el 'total perfecto' inventado por la humanidad para comparar cualquier cosa de forma fácil.",
    "resumen": "Un porcentaje es simplemente una fracción cuyo denominador siempre es 100. Escribir $x\\%$ es exactamente lo mismo que escribir $x/100$.",
    "explicacion": "La palabra **porcentaje** viene del latín *per centum*, que significa literalmente 'por cada cien'.\n\nMatemáticamente, el símbolo $\%$ es una abreviatura para '$\\div 100$'. Un porcentaje es una **razón** (una fracción) donde el denominador, es decir el total de referencia, siempre es el número 100.\n- $50\\%$ significa $50/100$ (la mitad de algo).\n- $25\\%$ significa $25/100$ (la cuarta parte de algo).\n- $100\\%$ significa $100/100$ (el total completo, equivalente a 1).",
    "procedimiento": ["Paso 1: Identifica el número que acompaña al símbolo de porcentaje (%).", "Paso 2: Escribe ese número como el numerador de una fracción.", "Paso 3: Escribe el número 100 como denominador. Esa es su forma de razón."],
    "ejemplos": [
        {"titulo": "Conversión directa", "enunciado": "¿Qué significa matemáticamente un 42%?", "solucion_pasos": ["Significa que si dividimos algo en 100 partes iguales, tomamos 42 de ellas.", "En fracción se escribe $42/100$.", "Si lo divides, es $0.42$ en decimal."]}
    ],
    "errores_frecuentes": ["Creer que 100% es el número máximo que existe (se puede tener 200%, que es el doble de un total).", "Escribir $50\\%$ como la fracción $100/50$.", "Olvidar que el % es solo una notación y no un número en sí mismo para operar sin convertirlo."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCIEN-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Desde el punto de vista matemático riguroso, un porcentaje es: (v{i})", "choices": ["A) Una fracción cuyo denominador fijo es 100.", "B) Un número decimal que siempre es menor a 1.", "C) Una variable que representa una incógnita.", "D) Un número natural cualquiera."], "correct_answer": "A) Una fracción cuyo denominador fijo es 100.", "solution_steps": "$x\\% = x/100$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCIEN-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "La notación matemática equivalente a $37\\%$ es:", "choices": ["A) $37/100$", "B) $100/37$", "C) $0.037$", "D) $37 \\cdot 100$"], "correct_answer": "A) $37/100$", "solution_steps": "Definición directa de per centum.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCIEN-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El $5\\%$ de una cantidad es equivalente a la fracción $5/100$ de esa cantidad?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "5% es literalmente 5/100.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCIEN-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"En una asamblea, un orador indica que $1$ de cada $4$ asistentes está a favor de un proyecto. Si otra persona desea expresar esta misma proporción usando el lenguaje de porcentajes (razón de denominador 100), ¿qué cifra debe utilizar? (v{i})", "choices": ["A) $25\\%$", "B) $40\\%$", "C) $14\\%$", "D) $20\\%$"], "correct_answer": "A) $25\\%$", "solution_steps": "La fracción es 1/4. Amplificando para que el denominador sea 100: $(1\\cdot25)/(4\\cdot25) = 25/100 = 25\\%$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 8...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 8...")
    append_jsonl("mat-num-razones-banco-gen-8", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-8.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()

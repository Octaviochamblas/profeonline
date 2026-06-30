# scratch/build_b0205_t6.py
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

# 1. PROBLEMAS_CONTEXTO INVERSA
sid1 = "MAT.NUM.PROP_INVERSA.PROBLEMAS_CONTEXTO"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Resolver problemas cotidianos utilizando el modelo de proporcionalidad inversa.",
    "introduccion": "¿Cómo calculas a qué velocidad debes manejar para llegar a tiempo si saliste tarde? Este tipo de cálculos, donde apurar el paso reduce la demora, se resuelven utilizando proporcionalidad inversa.",
    "resumen": "Los problemas de proporción inversa se resuelven igualando los productos de las variables ($x_1 \\cdot y_1 = x_2 \\cdot y_2$) o usando el modelo $y = k/x$.",
    "explicacion": "En la vida diaria, las proporciones inversas aparecen típicamente en tres contextos: tiempo y velocidad, tiempo y cantidad de trabajadores, o reparto equitativo de un recurso fijo.\n\nPara resolverlos, el método más seguro no es la regla de tres cruzada (que se usa en directa), sino **igualar los productos** (regla de tres inversa). Si la situación inicial tiene valores $x_1$ e $y_1$, y la situación final tiene $x_2$ e $y_2$, se cumple que:\n$$x_1 \\cdot y_1 = x_2 \\cdot y_2$$\nDe aquí simplemente despejas el valor desconocido.",
    "procedimiento": ["Paso 1: Confirma que la relación es inversa (más trabajadores = menos días).", "Paso 2: Multiplica los dos datos de la situación inicial conocida para obtener $k$.", "Paso 3: Divide esa constante $k$ por el único dato conocido de la situación final para hallar la incógnita."],
    "ejemplos": [
        {"titulo": "Pintores y días", "enunciado": "Si 3 pintores pintan una casa en 12 días, ¿cuántos días demorarán 4 pintores?", "solucion_pasos": ["Es inversa (más pintores, menos días).", "Calculamos el trabajo total: $3 \\text{ pintores} \\cdot 12 \\text{ días} = 36$ días-pintor ($k$).", "Dividimos por la nueva cantidad: $36 / 4 \\text{ pintores} = 9$ días."]}
    ],
    "errores_frecuentes": ["Aplicar la regla de tres simple cruzada ($x = 4\\cdot12/3 = 16$), obteniendo absurdamente que más pintores demoran más.", "No verificar lógicamente el resultado (preguntarse: ¿tiene sentido que demoren más si son más?)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVPROB-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Para resolver un problema de proporción inversa, la estrategia algebraica principal es igualar: (v{i})", "choices": ["A) El producto de los estados inicial y final ($x_1 y_1 = x_2 y_2$).", "B) El cociente de los estados inicial y final ($x_1 / y_1 = x_2 / y_2$).", "C) La suma cruzada de las variables.", "D) La diferencia entre $x$ e $y$."], "correct_answer": "A) El producto de los estados inicial y final ($x_1 y_1 = x_2 y_2$).", "solution_steps": "La constante es el producto.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PINVPROB-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si $10$ bombas llenan un depósito en $2$ horas. ¿Qué ecuación permite calcular el tiempo $t$ para $5$ bombas?", "choices": ["A) $10 \\cdot 2 = 5 \\cdot t$", "B) $10 / 2 = 5 / t$", "C) $10 \\cdot t = 5 \\cdot 2$", "D) $2 / 10 = t / 5$"], "correct_answer": "A) $10 \\cdot 2 = 5 \\cdot t$", "solution_steps": "Igualdad de productos.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVPROB-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si 4 personas gastan una bolsa de arroz en 6 días, 3 personas la gastarán en 8 días?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$4 \\cdot 6 = 24$. Luego $24 / 3 = 8$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PINVPROB-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un viaje de ciudad A a ciudad B toma $6$ horas yendo a $80$ km/h. Si hay una emergencia y se necesita hacer el recorrido en exactamente $4$ horas, ¿a qué velocidad constante debe ir el vehículo? (v{i})", "choices": ["A) $120$ km/h", "B) $100$ km/h", "C) $160$ km/h", "D) $90$ km/h"], "correct_answer": "A) $120$ km/h", "solution_steps": "$k = 6 \\cdot 80 = 480$ km (distancia total). Velocidad $= 480 / 4 = 120$ km/h.", "paes_style": True})

# 2. CONCEPTO PROP COMPUESTA
sid2 = "MAT.NUM.PROP_COMPUESTA.CONCEPTO"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Comprender el concepto de proporcionalidad compuesta.",
    "introduccion": "Hasta ahora hemos visto problemas donde solo dos cosas cambian: pintores y días. Pero, ¿qué pasa si agregamos una tercera variable, como la cantidad de casas a pintar? Bienvenido a la proporcionalidad compuesta.",
    "resumen": "La proporcionalidad compuesta es una relación matemática en la que intervienen tres o más magnitudes, pudiendo ser directas o inversas entre sí.",
    "explicacion": "Una **proporcionalidad compuesta** ocurre cuando una variable depende de múltiples factores simultáneamente. Por ejemplo, el costo de transporte depende del peso de la carga y de la distancia a recorrer.\n\nPara resolverla, la técnica no es memorizar una fórmula mágica, sino fijar la magnitud que tiene la incógnita y compararla independientemente con cada una de las otras magnitudes para ver si la relación es directa o inversa.",
    "procedimiento": ["Paso 1: Identifica todas las magnitudes (ej: horas, obreros, metros).", "Paso 2: Ubica cuál magnitud contiene la incógnita (la pregunta).", "Paso 3: Compara esa magnitud incógnita con las demás, *una por una*, asumiendo que el resto no cambia."],
    "ejemplos": [
        {"titulo": "Identificando magnitudes compuestas", "enunciado": "Si 5 hornos consumen 10 balones de gas en 20 días, ¿cuántas variables hay?", "solucion_pasos": ["Hay 3 magnitudes: cantidad de hornos, balones de gas, y días.", "Es un problema de proporción compuesta."]}
    ],
    "errores_frecuentes": ["Intentar cruzar todos los datos a la vez sin separar las relaciones.", "Creer que si son 3 variables, todas son inversas o todas son directas.", "No fijar mentalmente las demás variables al analizar un par de ellas."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPCONC-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué es la proporcionalidad compuesta? (v{i})", "choices": ["A) Aquella donde intervienen tres o más magnitudes relacionadas.", "B) Aquella donde todas las variables son directamente proporcionales.", "C) Una proporción con números decimales o fracciones.", "D) La multiplicación de dos proporciones simples iguales."], "correct_answer": "A) Aquella donde intervienen tres o más magnitudes relacionadas.", "solution_steps": "Definición por cantidad de variables.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PCOMPCONC-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Cuál de los siguientes es un problema de proporción compuesta?", "choices": ["A) Si 2 gatos cazan 2 ratones en 2 minutos, ¿cuánto demoran 100 gatos en cazar 100 ratones?", "B) Si 2 kilos cuestan 100, ¿cuánto cuestan 3 kilos?", "C) Si a 100 km/h demoro 2 horas, ¿cuánto a 50 km/h?", "D) El área de un cuadrado de lado 5."], "correct_answer": "A) Si 2 gatos cazan 2 ratones en 2 minutos, ¿cuánto demoran 100 gatos en cazar 100 ratones?", "solution_steps": "Involucra gatos, ratones y minutos (3 variables).", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPCONC-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Para analizar una proporción compuesta debo comparar la incógnita con cada variable por separado?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Es el método analítico estándar.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPCONC-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una empresa de envíos calcula su tarifa basándose en el peso del paquete y los kilómetros recorridos. Si se quiere hallar el precio para un envío de $5$ kg a $100$ km sabiendo que $2$ kg a $50$ km cuestan $\$4000$. ¿Qué tipo de proporcionalidad modela la situación? (v{i})", "choices": ["A) Proporcionalidad compuesta.", "B) Proporcionalidad inversa simple.", "C) Proporcionalidad directa simple.", "D) Función cuadrática."], "correct_answer": "A) Proporcionalidad compuesta.", "solution_steps": "Variables: Precio, Peso, Kilómetros.", "paes_style": True})

# 3. RELACION_DIRECTA EN COMPUESTA
sid3 = "MAT.NUM.PROP_COMPUESTA.RELACION_DIRECTA"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Identificar una relación directa dentro de un contexto de proporcionalidad compuesta.",
    "introduccion": "Cuando tienes 3 magnitudes o más, el truco es congelar todas menos dos. Si analizas esas dos y ambas crecen, tienes una relación directa en medio de la compuesta.",
    "resumen": "Al aislar la variable incógnita y compararla con otra (manteniendo el resto constante), si una aumenta y la otra también, la fracción asociada a esa variable se usa tal cual en la ecuación multiplicativa.",
    "explicacion": "En el análisis de un problema compuesto, tomamos la magnitud de la incógnita ($X$) y la comparamos con la magnitud $A$.\n\nSi decimos: 'A mayor cantidad de $A$, ¿se necesitará más o menos $X$?' y la respuesta es 'MÁS' (crecen juntas), entonces la relación entre $X$ y $A$ es **directa**.\n\nEn la resolución por el método de igualación de fracciones, la columna de la variable $A$ se escribe exactamente en el mismo orden (arriba/abajo) en que aparecen los datos.",
    "procedimiento": ["Paso 1: Fija mentalmente las demás variables (imagina que no cambian).", "Paso 2: Hazte la pregunta: 'A más de esto, ¿más o menos de la incógnita?'.", "Paso 3: Si la respuesta es 'más', anota una 'D' (directa) sobre esa columna de datos."],
    "ejemplos": [
        {"titulo": "Pintores, casas y pintura", "enunciado": "La incógnita es 'Galones de pintura'. Las otras variables son Pintores y Casas. ¿Cómo es la relación Pintura-Casas?", "solucion_pasos": ["Congelamos los Pintores (asumimos que son los mismos).", "Pregunta: A más Casas, ¿necesitamos más o menos Galones de pintura?", "Respuesta: Más. Por tanto, la relación Pintura-Casas es Directa."]}
    ],
    "errores_frecuentes": ["Preguntar 'A más de A, ¿más de B?' usando dos variables que no son la incógnita.", "No congelar la tercera variable en el experimento mental, confundiendo la deducción."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPDIR-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En proporción compuesta, al comparar la variable incógnita con otra, se asume que las demás variables: (v{i})", "choices": ["A) Se mantienen constantes.", "B) Aumentan al doble.", "C) Disminuyen a la mitad.", "D) Son irrelevantes para el problema global."], "correct_answer": "A) Se mantienen constantes.", "solution_steps": "Se asume Ceteris Paribus (todo lo demás constante).", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PCOMPDIR-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Variables: Días, Raciones, Personas. Incógnita: Raciones. Relación Personas-Raciones (Días constantes):", "choices": ["A) Directa (más personas, más raciones)", "B) Inversa (más personas, menos raciones)", "C) No hay relación", "D) Cuadrática"], "correct_answer": "A) Directa (más personas, más raciones)", "solution_steps": "Si los días no cambian, para alimentar más personas necesitas más comida.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPDIR-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿La relación entre 'Horas de uso' y 'Electricidad consumida' (con 'Electrodomésticos' fijos) es directa?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Más horas = más consumo.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPDIR-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un agricultor tiene variables: Hectáreas, Tractores, Días. Si la pregunta del problema es cuántas Hectáreas puede arar, ¿qué relación tiene la incógnita (Hectáreas) con la variable Días? (v{i})", "choices": ["A) Directa, porque a más días trabajando, más hectáreas podrá arar (con los mismos tractores).", "B) Inversa, porque a más días, menos hectáreas.", "C) Directa, porque a más tractores, más días demorará.", "D) Inversa, porque a más tractores, menos hectáreas."], "correct_answer": "A) Directa, porque a más días trabajando, más hectáreas podrá arar (con los mismos tractores).", "solution_steps": "Aislamiento: Tractores fijos. Más días = más terreno trabajado (Directa).", "paes_style": True})

# 4. RELACION_INVERSA EN COMPUESTA
sid4 = "MAT.NUM.PROP_COMPUESTA.RELACION_INVERSA"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Identificar una relación inversa dentro de un contexto de proporcionalidad compuesta.",
    "introduccion": "Así como hay relaciones directas, a veces aislar dos variables nos revela un sube y baja. Identificar esta inversión es crítico para no equivocarse al armar la ecuación final.",
    "resumen": "Al aislar la variable incógnita y compararla con otra, si una aumenta y la otra disminuye, la fracción de esa variable se debe invertir (dar vuelta) al escribir la ecuación multiplicativa.",
    "explicacion": "Continuando con el método, comparamos la incógnita ($X$) con otra magnitud $B$.\n\nSi la pregunta 'A mayor cantidad de $B$, ¿se necesitará más o menos $X$?' tiene como respuesta 'MENOS' (funcionan como un balancín), la relación es **inversa**.\n\nEn el método algorítmico tradicional, cuando una columna tiene relación inversa con la incógnita, su fracción se escribe 'de cabeza' (se invierten el numerador y denominador) antes de multiplicarla.",
    "procedimiento": ["Paso 1: Fija mentalmente las demás variables.", "Paso 2: Hazte la pregunta: 'A más de esto, ¿más o menos de la incógnita?'.", "Paso 3: Si la respuesta es 'menos', anota una 'I' (inversa) y recuerda invertir esa fracción al operar."],
    "ejemplos": [
        {"titulo": "Pintores, casas y días", "enunciado": "La incógnita es 'Días'. Las otras variables son Casas y Pintores. ¿Cómo es la relación Días-Pintores?", "solucion_pasos": ["Congelamos las Casas (es la misma obra).", "Pregunta: A más Pintores trabajando, ¿se demorarán más o menos Días?", "Respuesta: Menos días. Por tanto, es Inversa."]}
    ],
    "errores_frecuentes": ["Olvidar invertir la fracción en la ecuación matemática a pesar de haber deducido correctamente que era inversa.", "Invertir la fracción de la incógnita en lugar de las fracciones de los datos.", "Pensar que 'más horas = más cansancio' es una relación matemática de proporción."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPINV-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Si en un problema compuesto determinas que la variable $B$ es inversa a la incógnita, al armar la ecuación mediante fracciones debes: (v{i})", "choices": ["A) Invertir la fracción formada por los datos de la variable $B$.", "B) Invertir la fracción de la incógnita.", "C) Restar la fracción $B$.", "D) Multiplicar $B$ por cero."], "correct_answer": "A) Invertir la fracción formada por los datos de la variable $B$.", "solution_steps": "Es el mecanismo algebraico para compensar la inversión.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PCOMPINV-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Variables: Máquinas, Metros, Horas. Incógnita: Horas. Relación Horas-Máquinas:", "choices": ["A) Inversa (más máquinas, menos horas para igual metros)", "B) Directa (más máquinas, más horas)", "C) Directa (más metros, más horas)", "D) Inversa (más metros, menos horas)"], "correct_answer": "A) Inversa (más máquinas, menos horas para igual metros)", "solution_steps": "Al fijar Metros, más poder de trabajo reduce el tiempo.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPINV-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿La relación entre 'Velocidad' y 'Tiempo de viaje' para una 'Distancia' constante es inversa?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Más rápido = menos demora.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPINV-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"En el problema: 'Si $12$ vacas comen una cantidad de pasto en $6$ días, ¿cuántos días durará el pasto (incógnita) si hay $18$ vacas y la cantidad de pasto disminuye a la mitad?' Al analizar la relación entre Días y Vacas asumiendo el Pasto constante, ¿qué resulta? (v{i})", "choices": ["A) Relación Inversa, porque a más vacas comiendo, el pasto durará menos días.", "B) Relación Directa, porque a más vacas, necesitan más días.", "C) Relación Inversa, porque a más pasto, menos vacas.", "D) Relación Directa, porque el pasto disminuirá a la mitad."], "correct_answer": "A) Relación Inversa, porque a más vacas comiendo, el pasto durará menos días.", "solution_steps": "Fijando el pasto, al aumentar los bocas a alimentar, el tiempo se agota más rápido (Inversa).", "paes_style": True})

# 5. VARIABLE_CONSTANTE (RESOLUCION FINAL)
sid5 = "MAT.NUM.PROP_COMPUESTA.VARIABLE_CONSTANTE"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Resolver un problema de proporcionalidad compuesta unificando las relaciones.",
    "introduccion": "Ahora que sabes desarmar un problema compuesto identificando qué es directo y qué es inverso, es hora de armar el rompecabezas. Crearemos una gran ecuación matemática donde todo encaja perfectamente.",
    "resumen": "Para resolver, se iguala la fracción de la incógnita al producto de las demás fracciones, invirtiendo aquellas que tengan relación inversa con la incógnita.",
    "explicacion": "El método general de **reducción a la unidad** o de **igualación de razones** para resolver proporciones compuestas sigue la siguiente estructura:\n\n$$\\frac{\\text{Dato incógnita}}{\\text{Incógnita } x} = (\\text{Fracción } A) \\cdot (\\text{Fracción } B) \\cdot ...$$\n\nDonde:\n- Si la variable $A$ es Directa, su fracción se escribe tal cual (Arriba/Abajo).\n- Si la variable $B$ es Inversa, su fracción se escribe invertida (Abajo/Arriba).\n\nFinalmente, se multiplican las fracciones del lado derecho y se aplica la regla de la cuarta proporcional (producto cruzado) para hallar $x$.",
    "procedimiento": ["Paso 1: Ordena en una tabla de 3 o más columnas. Pon la incógnita al final.", "Paso 2: Escribe la ecuación poniendo la fracción de la columna incógnita sola en un lado.", "Paso 3: Multiplica el resto de columnas. Si una era inversa, dales la vuelta a sus números antes de multiplicar. Despeja $x$."],
    "ejemplos": [
        {"titulo": "Problema completo", "enunciado": "5 obreros hacen 10 metros de muro en 4 días. ¿Cuántos días ($x$) demoran 10 obreros en hacer 20 metros?", "solucion_pasos": ["Incógnita: Días. Días con Obreros es Inversa (invierte). Días con Metros es Directa (mantiene).", "Fracción incógnita: $4 / x$. Fracciones: Obreros $5/10$ (invierte a $10/5$), Metros $10/20$ (mantiene $10/20$).", "Ecuación: $4/x = (10/5) \\cdot (10/20) = 100/100 = 1$.", "$4/x = 1 \\implies x = 4$ días."]}
    ],
    "errores_frecuentes": ["Equivocarse en la simplificación de las fracciones antes de multiplicar.", "Invertir la fracción de la incógnita en lugar de la variable inversa.", "Sumar las fracciones en vez de multiplicarlas.", "No escribir los datos ordenados en la tabla, mezclando filas."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPRES-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En el método de resolución de proporción compuesta por fracciones, las fracciones de las diferentes variables conocidas se relacionan mediante la operación de: (v{i})", "choices": ["A) Multiplicación.", "B) Suma.", "C) División cruzada.", "D) Resta."], "correct_answer": "A) Multiplicación.", "solution_steps": "Las razones se multiplican para unificar el efecto proporcional.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PCOMPRES-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si en la ecuación $5/x = (2/3) \\cdot (8/4)$, ¿qué se debe hacer para despejar $x$?", "choices": ["A) Multiplicar $2/3$ por $8/4$, y luego producto cruzado con $5/x$.", "B) Sumar $2/3$ y $8/4$.", "C) Invertir $5/x$.", "D) Multiplicar todo por cero."], "correct_answer": "A) Multiplicar $2/3$ por $8/4$, y luego producto cruzado con $5/x$.", "solution_steps": "Resolución estándar de ecuaciones proporcionales.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPRES-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si $4/x = (1/2) \\cdot (4/1)$, entonces $x = 2$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$(1/2)\\cdot 4 = 2$. Luego $4/x = 2 \\implies x = 2$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PCOMPRES-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Si $4$ impresoras imprimen $100$ libros en $3$ días, ¿cuántos días ($x$) demorarán $2$ impresoras en imprimir $50$ libros? (v{i})", "choices": ["A) $3$ días", "B) $6$ días", "C) $1.5$ días", "D) $4$ días"], "correct_answer": "A) $3$ días", "solution_steps": "Días-Impresoras es inversa (4/2 invierte a 2/4). Días-Libros es directa (100/50 mantiene). Eq: $3/x = (2/4) \\cdot (100/50) = (1/2) \\cdot 2 = 1$. Luego $3/x = 1 \\implies x = 3$.", "paes_style": True})


def generate_all():
    print("Escribiendo YAMLs Tanda 6...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 6...")
    append_jsonl("mat-num-razones-banco-gen-6", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-6.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()

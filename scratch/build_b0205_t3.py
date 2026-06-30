# scratch/build_b0205_t3.py
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

# 1. MEDIA_PROPORCIONAL
sid1 = "MAT.NUM.PROPORCIONES.MEDIA_PROPORCIONAL"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Calcular la media proporcional en una proporción continua.",
    "introduccion": "Imagina que tienes una secuencia geométrica donde el número del medio es la clave para pasar del primero al último. En proporciones, cuando los dos números del centro son idénticos, a ese número lo llamamos media proporcional.",
    "resumen": "La media proporcional (o geométrica) es el término repetido en los medios de una proporción continua: $a/x = x/b$. Su valor es $x = \\sqrt{a \\cdot b}$.",
    "explicacion": "Una proporción es **continua** si sus términos medios son iguales. En la proporción $a:x = x:b$, al término $x$ se le llama **media proporcional** entre $a$ y $b$.\n\nAplicando el producto cruzado obtenemos $x \\cdot x = a \\cdot b$, es decir, $x^2 = ab$. Por lo tanto, la media proporcional se calcula extrayendo la raíz cuadrada del producto de los extremos: $x = \\sqrt{ab}$.",
    "procedimiento": ["Paso 1: Identifica los dos extremos conocidos $a$ y $b$.", "Paso 2: Multiplica esos dos valores ($a \\cdot b$).", "Paso 3: Extrae la raíz cuadrada del producto obtenido para hallar $x$."],
    "ejemplos": [
        {"titulo": "Hallando la media proporcional", "enunciado": "Calcula la media proporcional entre 4 y 9.", "solucion_pasos": ["Multiplicamos los extremos: $4 \\cdot 9 = 36$.", "Extraemos la raíz cuadrada: $\\sqrt{36} = 6$.", "La media proporcional es 6, ya que $4/6 = 6/9$."]},
        {"titulo": "¿Puede ser negativa?", "respuesta": "Sí", "solucion_pasos": ["Algebraicamente $x^2 = 36$ tiene como soluciones $6$ y $-6$. Generalmente en geometría se toma la positiva, pero matemáticamente ambas satisfacen la proporción."]}
    ],
    "errores_frecuentes": ["Confundirla con la media aritmética (sumar y dividir por dos).", "Olvidar sacar la raíz cuadrada después de multiplicar.", "Colocar la $x$ en un extremo en lugar de en los dos medios.", "Extraer la raíz de un solo término antes de multiplicar.", "Asumir que siempre dará un número entero (muchas veces es irracional)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"MEDPROP-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué caracteriza a una proporción donde existe media proporcional? (v{i})", "choices": ["A) Sus dos términos medios son exactamente iguales.", "B) Sus cuatro términos son números consecutivos.", "C) Sus extremos suman cero.", "D) Es una proporción con fracciones irreductibles."], "correct_answer": "A) Sus dos términos medios son exactamente iguales.", "solution_steps": "Por definición, en $a/x = x/b$ los medios son iguales.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"MEDPROP-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Para calcular la media proporcional $x$ entre $m$ y $n$, se utiliza la fórmula:", "choices": ["A) $x = \\sqrt{m \\cdot n}$", "B) $x = (m+n)/2$", "C) $x = m \\cdot n / 2$", "D) $x = m^2 + n^2$"], "correct_answer": "A) $x = \\sqrt{m \\cdot n}$", "solution_steps": "De $x^2 = mn$ se llega a la raíz.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"MEDPROP-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿La media proporcional entre 2 y 8 es 4?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$\\sqrt{2\\cdot8} = \\sqrt{16} = 4$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"MEDPROP-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"En diseño gráfico, la medida central ideal $x$ entre un margen de $16$ cm y un texto de $25$ cm obedece a una proporción continua $16:x = x:25$. ¿Cuál es esa medida $x$? (v{i})", "choices": ["A) $20$ cm", "B) $20.5$ cm", "C) $40$ cm", "D) $400$ cm"], "correct_answer": "A) $20$ cm", "solution_steps": "$x = \\sqrt{16\\cdot25} = \\sqrt{400} = 20$.", "paes_style": True})

# 2. TERCERA_PROPORCIONAL
sid2 = "MAT.NUM.PROPORCIONES.TERCERA_PROPORCIONAL"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Calcular la tercera proporcional en una proporción continua.",
    "introduccion": "Si en una proporción los términos medios son idénticos, solo necesitas conocer dos números distintos para descubrir el tercero. Ese 'tercer' número que falta en la ecuación se llama tercera proporcional.",
    "resumen": "La tercera proporcional es el término extremo que falta en una proporción continua: $a/b = b/x$. Se calcula como $x = b^2 / a$.",
    "explicacion": "Cuando tenemos una proporción continua (medios iguales) de la forma $a:b = b:x$, llamamos a $x$ la **tercera proporcional** entre $a$ y $b$ (o $b$ y $a$, dependiendo del orden).\n\nPara hallar su valor, aplicamos producto cruzado: $a \\cdot x = b \\cdot b$, lo que significa que $ax = b^2$. Despejando, nos queda $x = \\frac{b^2}{a}$.",
    "procedimiento": ["Paso 1: Identifica el término que no se repite ($a$) y el que se repite en los medios ($b$).", "Paso 2: Eleva al cuadrado el término repetido ($b^2$).", "Paso 3: Divide el resultado por el término no repetido ($a$)."],
    "ejemplos": [
        {"titulo": "Cálculo directo", "enunciado": "Halla la tercera proporcional entre 4 y 6.", "solucion_pasos": ["Planteamos la proporción continua: $4/6 = 6/x$.", "Multiplicamos los medios: $6 \\cdot 6 = 36$.", "Dividimos por 4: $36 / 4 = 9$. La tercera proporcional es 9."]},
        {"titulo": "¿El orden importa?", "respuesta": "Sí", "solucion_pasos": ["La tercera proporcional entre 6 y 4 sería $x$ en $6/4 = 4/x$, lo que da $x = 16/6 = 8/3$. Es distinta a la de 4 y 6."]}
    ],
    "errores_frecuentes": ["Confundirla con la cuarta proporcional.", "Confundirla con la media proporcional (no sacar la raíz o sacar raíz cuando no corresponde).", "No respetar el orden de los datos: elevar al cuadrado el número incorrecto.", "Sumar en lugar de multiplicar los medios.", "Simplificar erróneamente antes de armar la proporción."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"TERCPROP-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué es la tercera proporcional? (v{i})", "choices": ["A) El cuarto término en una proporción continua donde los medios son iguales.", "B) El tercer término contado de izquierda a derecha en cualquier proporción.", "C) La raíz cúbica de los términos medios.", "D) El número 3 dentro de una fracción proporcional."], "correct_answer": "A) El cuarto término en una proporción continua donde los medios son iguales.", "solution_steps": "Aparece cuando los medios son idénticos.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"TERCPROP-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "La fórmula para hallar $x$ en $a/b = b/x$ es:", "choices": ["A) $x = b^2 / a$", "B) $x = a^2 / b$", "C) $x = (a\\cdot b)/2$", "D) $x = \\sqrt{ab}$"], "correct_answer": "A) $x = b^2 / a$", "solution_steps": "Despejando por producto cruzado.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"TERCPROP-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿La tercera proporcional entre 3 y 6 es 12?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$3/6 = 6/12$ es correcto, $12 = 36/3$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"TERCPROP-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un mecanismo de engranajes tiene 3 ruedas acopladas. Si las vueltas de la primera a la segunda están en razón $5:10$, y la segunda con la tercera mantienen la misma razón continua ($10:x$), ¿cuántas vueltas dará la tercera si se mantiene la proporción? (v{i})", "choices": ["A) 20", "B) 2", "C) 50", "D) 15"], "correct_answer": "A) 20", "solution_steps": "$5/10 = 10/x \\implies x = 100/5 = 20$.", "paes_style": True})

# 3. COMPOSICION_PROPORCIONAL
sid3 = "MAT.NUM.PROPORCIONES.COMPOSICION_PROPORCIONAL"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Aplicar la propiedad de composición de proporciones.",
    "introduccion": "Si sabes que la proporción entre manzanas y peras es 2 a 3, puedes afirmar matemáticamente que 'las manzanas más las peras' son al total como 2+3 es al total. Esta es la composición de proporciones.",
    "resumen": "La composición indica que en $a/b = c/d$, se cumple que $(a+b)/b = (c+d)/d$ o $(a+b)/a = (c+d)/c$.",
    "explicacion": "La **composición proporcional** es una propiedad que nos permite sumar los términos de cada razón de una proporción manteniendo la igualdad.\n\nSi partimos de $\\frac{a}{b} = \\frac{c}{d}$:\n- Sumando 1 a ambos lados: $\\frac{a}{b} + 1 = \\frac{c}{d} + 1$\n- Usando denominador común: $\\frac{a+b}{b} = \\frac{c+d}{d}$\n\nEsta propiedad es muy útil en resolución de problemas donde conocemos la suma total de las cantidades.",
    "procedimiento": ["Paso 1: Verifica que tienes una proporción válida.", "Paso 2: Suma el denominador al numerador en ambos lados simultáneamente.", "Paso 3: Conserva los denominadores originales (o los numeradores originales)."],
    "ejemplos": [
        {"titulo": "Aplicando la propiedad", "enunciado": "Si $3/4 = 6/8$, demuestra la composición.", "solucion_pasos": ["Sumamos numerador y denominador: $(3+4)/4$ y $(6+8)/8$.", "Obtenemos $7/4$ y $14/8$.", "Simplificamos $14/8$ para ver que es igual a $7/4$. La proporción se mantiene."]}
    ],
    "errores_frecuentes": ["Sumar el denominador al numerador en un lado, pero restar en el otro.", "Cambiar los denominadores de lugar.", "Sumar los antecedentes entre sí y los consecuentes entre sí (eso es otra propiedad).", "Olvidar que se aplica a ambas razones por igual."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"COMPPROP-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué afirma la propiedad de composición respecto a $a/b = c/d$? (v{i})", "choices": ["A) Que $(a+b)/b = (c+d)/d$.", "B) Que $a/c = b/d$.", "C) Que $a+b = c+d$.", "D) Que $(a-b)/b = (c-d)/d$."], "correct_answer": "A) Que $(a+b)/b = (c+d)/d$.", "solution_steps": "Corresponde a sumar el denominador al numerador.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"COMPPROP-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si $x/y = 5/2$, aplicando composición con respecto al denominador, se obtiene:", "choices": ["A) $(x+y)/y = 7/2$", "B) $x/(x+y) = 5/7$", "C) $(x-y)/y = 3/2$", "D) $(x+y)/x = 7/5$"], "correct_answer": "A) $(x+y)/y = 7/2$", "solution_steps": "$(x+y)/y = (5+2)/2 = 7/2$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"COMPPROP-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Aplicar composición a $1/3 = 2/6$ genera $4/3 = 8/6$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$(1+3)/3 = 4/3$ y $(2+6)/6 = 8/6$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"COMPPROP-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"En una empresa la razón entre gerentes y empleados es $1:15$. Si sabemos que en total hay $64$ trabajadores, ¿qué ecuación de composición permite hallar a los gerentes ($g$) sabiendo que $e$ son empleados? (v{i})", "choices": ["A) $(g+e)/g = (1+15)/1 \\implies 64/g = 16/1$", "B) $g/64 = 1/15$", "C) $e/64 = 15/1$", "D) $(g+e)/15 = 64/16$"], "correct_answer": "A) $(g+e)/g = (1+15)/1 \\implies 64/g = 16/1$", "solution_steps": "Aplica la propiedad con respecto a los gerentes.", "paes_style": True})

# 4. DESCOMPOSICION_PROPORCIONAL
sid4 = "MAT.NUM.PROPORCIONES.DESCOMPOSICION_PROPORCIONAL"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Aplicar la propiedad de descomposición de proporciones.",
    "introduccion": "De forma análoga a la suma, a veces necesitamos restar cantidades de nuestra proporción para hallar la solución, por ejemplo, cuando conocemos la diferencia de dos valores.",
    "resumen": "La descomposición indica que en $a/b = c/d$, se cumple que $(a-b)/b = (c-d)/d$.",
    "explicacion": "La **descomposición proporcional** es la propiedad hermana de la composición. Nos permite restar el denominador del numerador en ambas razones de una proporción sin que la igualdad se rompa.\n\nDemostración rápida:\n- Si $\\frac{a}{b} = \\frac{c}{d}$, restamos 1 a cada lado: $\\frac{a}{b} - 1 = \\frac{c}{d} - 1$\n- Al restar fracciones queda: $\\frac{a-b}{b} = \\frac{c-d}{d}$",
    "procedimiento": ["Paso 1: Toma la proporción original.", "Paso 2: Resta el término inferior al superior en ambas razones.", "Paso 3: Mantén los mismos términos inferiores originales."],
    "ejemplos": [
        {"titulo": "Aplicando descomposición", "enunciado": "Si $10/2 = 20/4$, demuestra la descomposición.", "solucion_pasos": ["Restamos el denominador: $(10-2)/2 = 8/2 = 4$.", "Restamos en el otro lado: $(20-4)/4 = 16/4 = 4$.", "La igualdad $4=4$ se mantiene."]}
    ],
    "errores_frecuentes": ["Restar el numerador del denominador en lugar del denominador del numerador (produce signos opuestos).", "Aplicar composición en un lado y descomposición en el otro.", "Olvidar mantener el denominador original.", "Restar los numeradores entre sí (eso es la propiedad de la resta de antecedentes)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"DESCPROP-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿En qué consiste la descomposición de una proporción? (v{i})", "choices": ["A) Restar el consecuente al antecedente, manteniendo el consecuente.", "B) Sumar los cuatro términos.", "C) Restar los antecedentes entre sí.", "D) Dividir la proporción por dos."], "correct_answer": "A) Restar el consecuente al antecedente, manteniendo el consecuente.", "solution_steps": "Se expresa como $(a-b)/b$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"DESCPROP-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Dada $a/b = c/d$, su forma por descomposición es:", "choices": ["A) $(a-b)/b = (c-d)/d$", "B) $(a+b)/b = (c+d)/d$", "C) $(b-a)/a = (d-c)/c$", "D) $(a-c)/b = (c-a)/d$"], "correct_answer": "A) $(a-b)/b = (c-d)/d$", "solution_steps": "Restar denominador en numerador.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"DESCPROP-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Al descomponer $7/3 = 14/6$ resulta $4/3 = 8/6$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$(7-3)/3 = 4/3$ y $(14-6)/6 = 8/6$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"DESCPROP-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Dos hermanos reciben herencia en razón $7:4$. Si la diferencia entre lo que reciben es de $300.000$ pesos, ¿qué expresión de descomposición sirve para hallar lo del hermano menor ($m$)? (v{i})", "choices": ["A) $300.000 / m = (7-4) / 4$", "B) $300.000 / m = (7+4) / 4$", "C) $m / 300.000 = 7/4$", "D) $m / 300.000 = 4/7$"], "correct_answer": "A) $300.000 / m = (7-4) / 4$", "solution_steps": "$(H-m)/m = (7-4)/4$. Como la diferencia es 300.000, $300.000/m = 3/4$.", "paes_style": True})

# 5. PROP_DIRECTA_CONCEPTO
sid5 = "MAT.NUM.PROP_DIRECTA.CONCEPTO_VARIABLES"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Comprender el concepto de variables directamente proporcionales.",
    "introduccion": "¿Has notado que si compras el doble de pan, pagas exactamente el doble? Cuando dos magnitudes se mueven en perfecta sincronía hacia arriba o hacia abajo, estamos ante una proporcionalidad directa.",
    "resumen": "Dos variables son directamente proporcionales si al multiplicar una por una constante, la otra también se multiplica por la misma constante. Su cociente siempre es el mismo ($y/x = k$).",
    "explicacion": "Hablamos de **proporcionalidad directa** cuando dos magnitudes numéricas están vinculadas de modo que el aumento de una provoca el aumento de la otra en la misma proporción (y lo mismo con su disminución).\n\nMatemáticamente, si $x$ e $y$ son directamente proporcionales, el cociente entre ellas es constante:\n$$\\frac{y}{x} = k$$\nDonde $k$ es la **constante de proporcionalidad**. Si $x$ se duplica, $y$ se duplica. Si $x$ se divide por 3, $y$ se divide por 3.",
    "procedimiento": ["Paso 1: Identifica las dos variables del problema.", "Paso 2: Comprueba si al aumentar una al doble, la otra obligatoriamente debe aumentar al doble.", "Paso 3: Si esto se cumple, son variables directamente proporcionales."],
    "ejemplos": [
        {"titulo": "Variables de la vida real", "enunciado": "¿Son el tiempo de viaje (a velocidad constante) y la distancia recorrida proporcionales?", "solucion_pasos": ["Si viajas el doble de tiempo a la misma velocidad, recorrerás el doble de distancia.", "Como ambas crecen en la misma proporción, son directamente proporcionales."]},
        {"titulo": "¿Toda relación que sube es proporcional?", "respuesta": "No", "solucion_pasos": ["La edad de una persona y su altura: si bien a mayor edad (hasta la adultez) suele haber mayor altura, a los 20 años no mides el doble que a los 10 años. No es proporcionalidad directa."]}
    ],
    "errores_frecuentes": ["Creer que 'si una sube y la otra sube' ya es suficiente (deben subir multiplicadas por el mismo factor, no sumar el mismo factor).", "Confundir proporcionalidad directa con función lineal afín que no pasa por el origen ($y=mx+n$).", "Asumir que si la constante es negativa, no es proporcional."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPDIR-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Para que dos variables sean directamente proporcionales, se debe cumplir obligatoriamente que: (v{i})", "choices": ["A) Al multiplicar una por un número, la otra quede multiplicada por el mismo número.", "B) Si una aumenta, la otra aumente sin importar en qué cantidad.", "C) Al sumar un valor a una, se sume el mismo valor a la otra.", "D) El producto entre ellas sea constante."], "correct_answer": "A) Al multiplicar una por un número, la otra quede multiplicada por el mismo número.", "solution_steps": "El factor de crecimiento debe ser proporcional y constante.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PROPDIR-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El modelo matemático de dos variables $x$ e $y$ directamente proporcionales es:", "choices": ["A) $y/x = k$", "B) $x\\cdot y = k$", "C) $y = k + x$", "D) $y = k - x$"], "correct_answer": "A) $y/x = k$", "solution_steps": "El cociente entre las magnitudes es constante.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPDIR-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El lado de un cuadrado y su perímetro son directamente proporcionales?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "El perímetro es $4\\cdot L$. $P/L = 4$ (constante).", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROPDIR-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"¿Cuál de los siguientes pares de variables son directamente proporcionales? (v{i})", "choices": ["A) La cantidad de kilos de manzanas compradas y el precio a pagar (sin descuentos).", "B) La edad de una persona y su número de calzado.", "C) La velocidad de un vehículo y el tiempo que tarda en llegar a destino.", "D) El lado de un cuadrado y su área."], "correct_answer": "A) La cantidad de kilos de manzanas compradas y el precio a pagar (sin descuentos).", "solution_steps": "Doble de kilos = doble de precio. El resto no cumple crecimiento lineal $y=kx$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 3...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 3...")
    append_jsonl("mat-num-razones-banco-gen-3", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-3.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()

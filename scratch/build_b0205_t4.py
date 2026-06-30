# scratch/build_b0205_t4.py
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

# 1. CONSTANTE_PROPORCIONALIDAD
sid1 = "MAT.NUM.PROP_DIRECTA.CONSTANTE_PROPORCIONALIDAD"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Calcular la constante de proporcionalidad directa.",
    "introduccion": "Si en un negocio cada alfajor cuesta $500, no importa cuántos compres, la relación 'precio dividido por alfajores' siempre dará 500. Ese número fijo es el corazón de la proporción directa.",
    "resumen": "La constante de proporcionalidad directa ($k$) es el valor fijo que resulta de dividir dos magnitudes proporcionales: $k = y/x$.",
    "explicacion": "En una **proporcionalidad directa**, aunque los valores de $x$ e $y$ cambien constantemente, su cociente jamás lo hace. Si divides cualquier valor de $y$ por su correspondiente $x$, siempre obtendrás el mismo número.\n\nA este número inalterable lo llamamos **constante de proporcionalidad ($k$)**.\n$$k = \\frac{y}{x}$$",
    "procedimiento": ["Paso 1: Identifica un par de valores $(x, y)$ que correspondan entre sí.", "Paso 2: Divide la magnitud dependiente ($y$) por la independiente ($x$).", "Paso 3: El resultado de esa división es la constante $k$."],
    "ejemplos": [
        {"titulo": "Hallando k", "enunciado": "Si $3$ horas de trabajo producen $15$ juguetes, ¿cuál es la constante de proporcionalidad?", "solucion_pasos": ["El par de valores es $x=3$ horas, $y=15$ juguetes.", "Dividimos $y/x = 15/3 = 5$.", "La constante es $k=5$. (Se producen 5 juguetes por hora)."]},
        {"titulo": "¿Qué pasa si invierto el orden?", "respuesta": "Cambia el significado", "solucion_pasos": ["Si divides $3/15 = 1/5 = 0.2$. Esta es la constante inversa ($1/k$), que indica que se demora 0.2 horas en hacer un juguete. Matemáticamente es válido, pero suele estandarizarse $y/x$."]}
    ],
    "errores_frecuentes": ["Restar los valores en lugar de dividirlos.", "Multiplicar $x \\cdot y$ en vez de dividirlos (eso es constante de proporción inversa).", "Creer que la constante cambia si uso números más grandes.", "Dividir a veces $y/x$ y a veces $x/y$ en un mismo problema."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRCONST-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"La constante de proporcionalidad directa se define como: (v{i})", "choices": ["A) El cociente constante entre dos variables proporcionales.", "B) El producto constante de dos variables.", "C) La diferencia entre las variables dependiente e independiente.", "D) El número máximo que puede tomar la variable x."], "correct_answer": "A) El cociente constante entre dos variables proporcionales.", "solution_steps": "Por definición $k = y/x$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PDIRCONST-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si $x=4$ e $y=12$ son directamente proporcionales, ¿cuál es el valor de $k$?", "choices": ["A) $3$", "B) $48$", "C) $8$", "D) $16$"], "correct_answer": "A) $3$", "solution_steps": "$k = y/x = 12/4 = 3$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRCONST-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si al comprar 2 kg pago $1000, la constante es $500/kg?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$1000 / 2 = 500$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRCONST-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una máquina envasadora procesa $240$ botellas en $8$ minutos. Si la relación es de proporción directa, ¿cuál es la constante de proporcionalidad medida en botellas por minuto? (v{i})", "choices": ["A) $30$", "B) $1920$", "C) $232$", "D) $248$"], "correct_answer": "A) $30$", "solution_steps": "$k = y/x = 240/8 = 30$.", "paes_style": True})

# 2. RECONOCIMIENTO_TABULAR
sid2 = "MAT.NUM.PROP_DIRECTA.RECONOCIMIENTO_TABULAR"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Reconocer una relación de proporcionalidad directa a partir de una tabla de valores.",
    "introduccion": "Si te entregan una hoja de cálculo con datos, ¿cómo sabes a simple vista si obedecen a una proporción directa? El secreto está en probar si todos esconden el mismo multiplicador.",
    "resumen": "En una tabla de proporcionalidad directa, la división $y/x$ en cada fila o columna debe dar exactamente el mismo resultado ($k$).",
    "explicacion": "Una **tabla de valores** representa la relación entre dos magnitudes. Para comprobar si dicha tabla modela una proporcionalidad directa, debes dividir el valor de $y$ por su correspondiente valor de $x$ en cada uno de los pares de datos presentados.\n\n- Si todas las divisiones dan el mismo resultado $k$, la tabla representa una proporción directa.\n- Si al menos uno de los resultados es distinto, la tabla NO es de proporción directa.",
    "procedimiento": ["Paso 1: Toma el primer par de datos $(x, y)$ de la tabla y divide $y$ por $x$.", "Paso 2: Repite la división para el segundo par, el tercero, y así sucesivamente.", "Paso 3: Si todos los resultados son idénticos, la tabla es directamente proporcional."],
    "ejemplos": [
        {"titulo": "Verificando una tabla", "enunciado": "La tabla tiene los pares $(2, 6)$, $(3, 9)$, $(5, 16)$. ¿Es proporción directa?", "solucion_pasos": ["Dividimos par 1: $6/2 = 3$.", "Dividimos par 2: $9/3 = 3$.", "Dividimos par 3: $16/5 = 3.2$.", "Como $3 \\neq 3.2$, la tabla NO representa proporción directa."]}
    ],
    "errores_frecuentes": ["Comprobar solo el primer par y asumir que los demás también cumplen.", "Comprobar que ambas variables crecen, pero sin verificar si el cociente es constante.", "Dividir $x/y$ en una celda e $y/x$ en la siguiente.", "Confundir con la proporción inversa (donde lo constante es el producto $x \\cdot y$)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRTAB-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Para afirmar que una tabla muestra proporción directa, es estrictamente necesario que: (v{i})", "choices": ["A) El cociente $y/x$ sea constante en todos los pares de datos.", "B) El producto $x \\cdot y$ sea el mismo en todas las filas.", "C) Los valores de $y$ siempre sean mayores que los de $x$.", "D) Las dos variables vayan aumentando de uno en uno."], "correct_answer": "A) El cociente $y/x$ sea constante en todos los pares de datos.", "solution_steps": "Es la comprobación de la constante $k$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PDIRTAB-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si una tabla tiene los pares $(1, 5)$, $(2, 10)$, $(4, z)$, y es de proporción directa, ¿cuál es el valor de $z$?", "choices": ["A) $20$", "B) $15$", "C) $40$", "D) $5$"], "correct_answer": "A) $20$", "solution_steps": "La constante es 5. Luego $z = 4 \\cdot 5 = 20$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRTAB-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿La tabla con pares $(2, 4), (4, 8), (6, 10)$ representa proporción directa?", "choices": [], "correct_answer": "Falso", "solution_steps": "Tercer par da $10/6 \\neq 2$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRTAB-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al estudiar el cobro de un plan de celular, se obtienen los datos $(Minutos, Cobro)$: $(10, 500)$, $(20, 1000)$, $(50, 2500)$. ¿Se puede modelar esta situación con una proporción directa? (v{i})", "choices": ["A) Sí, porque el cociente $Cobro/Minutos$ es constante en todos los datos registrados.", "B) No, porque no hay un cargo fijo inicial.", "C) Sí, porque a medida que aumentan los minutos también aumenta el cobro.", "D) No, porque $2500$ no es el doble de $1000$."], "correct_answer": "A) Sí, porque el cociente $Cobro/Minutos$ es constante en todos los datos registrados.", "solution_steps": "$500/10=50$, $1000/20=50$, $2500/50=50$. La constante es la misma.", "paes_style": True})

# 3. GRAFICO_RECTA_ORIGEN
sid3 = "MAT.NUM.PROP_DIRECTA.GRAFICO_RECTA_ORIGEN"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Identificar y analizar el gráfico de una proporción directa.",
    "introduccion": "Si tomas todos los puntos de una tabla de proporción directa y los dibujas en un plano cartesiano, aparecerá una figura geométrica perfecta e inconfundible que nos da información a un solo golpe de vista.",
    "resumen": "El gráfico de una proporción directa en el plano cartesiano es siempre una línea recta que pasa exactamente por el origen de coordenadas $(0,0)$.",
    "explicacion": "Una **proporcionalidad directa** siempre se representa gráficamente como una **línea recta diagonal**.\n\nLa característica más crítica es que esta recta **debe pasar por el origen** $(0,0)$. Esto tiene total sentido lógico: si no compras ningún artículo ($x=0$), no pagas nada ($y=0$). Si la recta no pasa por el origen (por ejemplo, si arranca desde más arriba en el eje Y), no es proporción directa, sino una función afín con un 'cargo fijo'.\n\nLa inclinación (pendiente) de esta recta depende del valor de la constante $k$: mientras mayor sea $k$, más empinada será la recta.",
    "procedimiento": ["Paso 1: Observa el plano cartesiano y ubica los puntos de la gráfica.", "Paso 2: Comprueba que forman una línea recta.", "Paso 3: Verifica que el origen $(0,0)$ sea parte de esa recta. Si cumple ambas, es proporción directa."],
    "ejemplos": [
        {"titulo": "Evaluando gráficos", "enunciado": "Una recta arranca en el punto $(0, 1000)$ y sube constantemente. ¿Es proporción directa?", "solucion_pasos": ["La forma es de recta.", "Pero corta al eje Y en $1000$, no en $0$.", "Por lo tanto, NO es proporción directa."]}
    ],
    "errores_frecuentes": ["Creer que cualquier recta inclinada es proporción directa, olvidando revisar si pasa por $(0,0)$.", "Pensar que una curva ascendente puede ser proporción directa.", "Confundir la pendiente de la recta con el valor de la variable $x$.", "Creer que si la recta es muy acostada (pendiente baja), deja de ser proporción directa."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRGRAF-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Visualmente, el gráfico cartesiano de una proporción directa siempre corresponde a: (v{i})", "choices": ["A) Una línea recta que pasa por el origen $(0,0)$.", "B) Una curva que nace en el origen y crece exponencialmente.", "C) Una línea recta paralela al eje X.", "D) Una recta que corta al eje Y en un valor distinto de cero."], "correct_answer": "A) Una línea recta que pasa por el origen $(0,0)$.", "solution_steps": "Característica definitoria gráfica.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PDIRGRAF-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si en un gráfico de proporción directa un punto es $(3, 12)$, la recta debe pasar por:", "choices": ["A) $(0,0)$ y $(1,4)$", "B) $(0,1)$ y $(2,8)$", "C) $(1,12)$ y $(3,0)$", "D) $(0,12)$ y $(3,0)$"], "correct_answer": "A) $(0,0)$ y $(1,4)$", "solution_steps": "El origen y el punto de $k=4$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRGRAF-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Un recibo de luz que tiene un cargo fijo mensual de $1000 formará una recta que pasa por el origen?", "choices": [], "correct_answer": "Falso", "solution_steps": "Pasará por $(0, 1000)$, no por el origen.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRGRAF-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al analizar el rendimiento de un vehículo nuevo, un alumno grafica los Litros consumidos versus Kilómetros recorridos, obteniendo una recta. Si la recta NO pasara por el origen, ¿qué significado físico absurdo implicaría? (v{i})", "choices": ["A) Que el auto consumiría combustible estando estacionado con el motor apagado ($0$ km).", "B) Que el auto no puede detenerse nunca.", "C) Que la gasolina es de baja calidad y rinde menos.", "D) Que a mayor velocidad se gasta menos combustible."], "correct_answer": "A) Que el auto consumiría combustible estando estacionado con el motor apagado ($0$ km).", "solution_steps": "El punto $(0, y)$ con $y>0$ implicaría gasto sin movimiento.", "paes_style": True})

# 4. MODELO_ALGEBRAICO
sid4 = "MAT.NUM.PROP_DIRECTA.MODELO_ALGEBRAICO"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Representar situaciones de proporción directa a través de un modelo algebraico (ecuación).",
    "introduccion": "Una vez que conoces la constante de proporcionalidad, ya no necesitas resolver regla de tres cada vez. Puedes crear una 'máquina matemática' en forma de ecuación que calcule cualquier valor de forma instantánea.",
    "resumen": "El modelo algebraico de la proporcionalidad directa es la ecuación $y = k \\cdot x$, donde $k$ es la constante de proporcionalidad.",
    "explicacion": "Al saber que $y/x = k$, podemos multiplicar a ambos lados de la igualdad por $x$ para despejar $y$. Esto nos entrega el **modelo algebraico** de la proporción:\n\n$$y = k \\cdot x$$\n\nEsta ecuación nos dice que para hallar cualquier valor de $y$ (magnitud dependiente), simplemente multiplicamos el valor de $x$ (magnitud independiente) por nuestra constante $k$. Es equivalente a una función lineal $f(x) = kx$.",
    "procedimiento": ["Paso 1: Calcula la constante $k$ dividiendo un par conocido $y/x$.", "Paso 2: Escribe la ecuación sustituyendo $k$ por el número encontrado.", "Paso 3: Utiliza $y = kx$ para encontrar valores desconocidos de forma inmediata."],
    "ejemplos": [
        {"titulo": "Construyendo el modelo", "enunciado": "Si 2 cajas pesan 10 kilos, escribe el modelo algebraico del peso en función de las cajas.", "solucion_pasos": ["Calculamos $k = 10 / 2 = 5$.", "Planteamos la fórmula general $y = k \\cdot x$.", "El modelo es $y = 5x$ (el peso es 5 veces el número de cajas)."]},
        {"titulo": "¿Puedo despejar x?", "respuesta": "Sí", "solucion_pasos": ["Del modelo $y = kx$, se deduce que $x = y / k$ si necesitamos calcular el antecedente."]}
    ],
    "errores_frecuentes": ["Plantear el modelo como $y = k + x$.", "Intercambiar variables escribiendo $x = ky$ sin adaptar el valor de la constante.", "Olvidar calcular $k$ antes de armar la ecuación final.", "Agregar un término libre (ej. $y = kx + n$), convirtiéndolo en función afín."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRMOD-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué ecuación representa adecuadamente una proporción directa entre $x$ e $y$? (v{i})", "choices": ["A) $y = k \\cdot x$", "B) $y = k / x$", "C) $y = k + x$", "D) $y = x - k$"], "correct_answer": "A) $y = k \\cdot x$", "solution_steps": "Despejando y de $y/x = k$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PDIRMOD-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si en un problema $k = 7.5$, el modelo matemático para calcular $y$ es:", "choices": ["A) $y = 7.5x$", "B) $y = 7.5/x$", "C) $y = x/7.5$", "D) $y = x + 7.5$"], "correct_answer": "A) $y = 7.5x$", "solution_steps": "Se multiplica la constante por x.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRMOD-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El modelo $y = 3x - 1$ representa una proporcionalidad directa?", "choices": [], "correct_answer": "Falso", "solution_steps": "Tiene un término libre (-1), por ende la recta no pasa por $(0,0)$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRMOD-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un grifo arroja $15$ litros de agua en $3$ minutos. Si $V$ es el volumen en litros y $t$ el tiempo en minutos, ¿qué modelo algebraico permite calcular el volumen de agua arrojado en cualquier instante $t$? (v{i})", "choices": ["A) $V = 5t$", "B) $V = 15t$", "C) $V = 3t$", "D) $V = t + 12$"], "correct_answer": "A) $V = 5t$", "solution_steps": "Primero hallamos $k = 15/3 = 5$. Luego planteamos $V = k \\cdot t \\implies V = 5t$.", "paes_style": True})

# 5. PROBLEMAS_CONTEXTO
sid5 = "MAT.NUM.PROP_DIRECTA.PROBLEMAS_CONTEXTO"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Resolver problemas cotidianos utilizando el modelo de proporcionalidad directa.",
    "introduccion": "¿Cómo calculan las constructoras el material para 100 casas si solo hicieron los planos de una? Las proporciones directas son herramientas de la vida real usadas a diario para escalar ingredientes, costos, tiempo y materiales.",
    "resumen": "Los problemas cotidianos se resuelven identificando las magnitudes, validando que al aumentar una aumenta la otra en igual factor, y aplicando regla de tres o el modelo $y=kx$.",
    "explicacion": "Para resolver un problema de la vida cotidiana usando **proporcionalidad directa**, lo más crítico es leer con cuidado para confirmar que no haya 'cargos fijos' o relaciones inversas (ej. más obreros $\\rightarrow$ menos tiempo, eso es inverso).\n\nUna vez seguros de que es directa (ej. más kilos $\\rightarrow$ más dinero; más tiempo $\\rightarrow$ más distancia), usamos la regla de tres cruzada o calculamos $k$ para despejar la incógnita. Plantear los datos en una tabla rápida mental o en papel evita cruzar los números equivocados.",
    "procedimiento": ["Paso 1: Lee el enunciado y asegúrate de que la relación crezca o decrezca simultáneamente (si duplico A, debe duplicarse B).", "Paso 2: Ordena los datos conocidos en un planteo de dos columnas.", "Paso 3: Multiplica cruzado y divide por el dato restante (cuarta proporcional) para hallar la respuesta."],
    "ejemplos": [
        {"titulo": "Ingredientes de receta", "enunciado": "Una receta para 4 personas necesita 600g de pollo. ¿Cuánto pollo se necesita para 10 personas?", "solucion_pasos": ["Confirmamos: el doble de personas requerirá el doble de pollo (es directa).", "Planteo: $4$ personas $\\rightarrow 600g$ \\n $10$ personas $\\rightarrow x$.", "Operación: $x = (10 \\cdot 600) / 4 = 6000 / 4 = 1500g$. Se necesitan 1.5 kilos."]}
    ],
    "errores_frecuentes": ["Aplicar regla de tres directa en problemas de proporción inversa (como velocidad y tiempo).", "Cruzar erróneamente los datos al armar las columnas.", "Ignorar las unidades de medida (ej. mezclar gramos con kilos en la regla de tres).", "Apurarse sin comprobar que la constante inicial era correcta."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRPROB-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es el paso fundamental antes de aplicar una regla de tres directa en un problema real? (v{i})", "choices": ["A) Comprobar lógicamente que si una magnitud se duplica, la otra también debe duplicarse obligatoriamente.", "B) Comprobar que ambas variables estén escritas en números enteros.", "C) Asegurarse de que el resultado será mayor a los datos entregados.", "D) Sumar todos los valores proporcionados."], "correct_answer": "A) Comprobar lógicamente que si una magnitud se duplica, la otra también debe duplicarse obligatoriamente.", "solution_steps": "La validación cualitativa es esencial para no confundirla con inversa o función afín.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PDIRPROB-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Situación: 'A más albañiles trabajando, menos días demoran'. ¿Se puede resolver por proporción directa?", "choices": ["A) No, porque es proporción inversa.", "B) Sí, utilizando producto cruzado.", "C) Sí, porque ambas variables cambian al mismo tiempo.", "D) No, porque no hay números en el enunciado."], "correct_answer": "A) No, porque es proporción inversa.", "solution_steps": "Si una sube y la otra baja, es inversa.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRPROB-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si 5 helados cuestan 2000, entonces 2 helados costarán 800?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$2000/5 = 400$ por helado. $2 \\cdot 400 = 800$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PDIRPROB-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una fotocopiadora industrial imprime $300$ hojas en $2$ minutos. Si la máquina no sufre alteraciones, ¿cuánto tiempo demorará exactamente en imprimir un tiraje de $1350$ hojas? (v{i})", "choices": ["A) $9$ minutos", "B) $10$ minutos", "C) $4.5$ minutos", "D) $8$ minutos"], "correct_answer": "A) $9$ minutos", "solution_steps": "$300 \\rightarrow 2 \\implies 1350 \\rightarrow x$. $x = 1350 \\cdot 2 / 300 = 2700 / 300 = 9$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 4...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 4...")
    append_jsonl("mat-num-razones-banco-gen-4", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-4.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()

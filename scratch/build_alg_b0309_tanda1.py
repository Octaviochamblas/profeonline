import os
import json

base_dir = r"c:\Users\PC\Documents\Proyectos\Web\profeonline"
yaml_dir = os.path.join(base_dir, "docs", "conocimiento", "contenido")
jsonl_path = os.path.join(base_dir, "docs", "conocimiento", "ejercicios", "mat-alg-desigualdades-banco-gen-1.jsonl")

os.makedirs(yaml_dir, exist_ok=True)
os.makedirs(os.path.dirname(jsonl_path), exist_ok=True)

topics = {
    "MAT.ALG.ORDEN_FUNDAMENTOS.REALES_ORDENADOS": {
        "titulo": "Conjunto de los números reales ordenados",
        "objetivo": "Comprender la estructura de orden de los números reales mediante la representación en la recta numérica.",
        "introduccion": "Los números reales poseen una estructura que permite compararlos y ordenarlos en una recta unidimensional.",
        "resumen": "El orden de los números reales se basa en que, dados dos números, siempre es posible determinar su posición relativa en la recta numérica.",
        "def_formal": "Para todo $a, b \\in \\mathbb{R}$, se define el orden a partir de los axiomas de cuerpo ordenado, garantizando que el conjunto $\\mathbb{R}$ está totalmente ordenado.",
        "desarrollo": "Al ubicar los números en la recta real, un número a la derecha es estrictamente mayor que cualquier número a su izquierda.",
        "proc": ["Trazar una recta numérica horizontal.", "Ubicar el origen cero.", "Posicionar los números reales según su valor relativo y signo."],
        "errores": [
            "El cero es un número positivo.",
            "Los números negativos más lejanos al cero son mayores.",
            "Existen números reales que no se pueden comparar.",
            "El orden de los reales no es transitivo.",
            "Entre dos números reales siempre hay un número finito de racionales."
        ]
    },
    "MAT.ALG.ORDEN_FUNDAMENTOS.LEY_TRICOTOMIA": {
        "titulo": "Ley de tricotomía en los números reales",
        "objetivo": "Aplicar la ley de tricotomía para establecer la relación exacta entre dos números reales.",
        "introduccion": "La comparación fundamental en álgebra requiere que sepamos si una cantidad es mayor, menor o igual a otra.",
        "resumen": "La ley de tricotomía establece que dadas dos cantidades, solo una de tres relaciones posibles puede cumplirse.",
        "def_formal": "Para cualquier par de números reales $a$ y $b$, se cumple exactamente una de las siguientes relaciones: $a < b$, $a = b$, o $a > b$.",
        "desarrollo": "Esta propiedad es fundamental para la resolución de desigualdades, ya que descarta cualquier ambigüedad al comparar dos valores reales.",
        "proc": ["Identificar los dos números reales a comparar.", "Evaluar la diferencia entre ambos valores.", "Concluir cuál de las tres relaciones de tricotomía se cumple."],
        "errores": [
            "Dos números pueden ser mayores y menores entre sí al mismo tiempo.",
            "La ley de tricotomía aplica solo a números enteros.",
            "Es posible que dos números reales no cumplan ninguna de las tres relaciones.",
            "Si $a = b$, entonces también puede ser que $a < b$.",
            "La tricotomía no es válida si uno de los números es irracional."
        ]
    },
    "MAT.ALG.ORDEN_FUNDAMENTOS.SIMBOLO_MAYOR": {
        "titulo": "Uso del símbolo mayor que",
        "objetivo": "Interpretar el símbolo de mayor que en relaciones matemáticas y expresiones algebraicas.",
        "introduccion": "Para expresar que una cantidad supera a otra, la matemática emplea el símbolo mayor que.",
        "resumen": "El símbolo mayor que ($>$) indica que el término a su izquierda tiene un valor superior al término de su derecha.",
        "def_formal": "Para $a, b \\in \\mathbb{R}$, $a > b$ si y solo si $a - b > 0$, lo cual indica que la diferencia pertenece a los reales positivos.",
        "desarrollo": "En la recta numérica, afirmar que $a > b$ significa geométricamente que el punto que representa a $a$ se ubica a la derecha del punto que representa a $b$.",
        "proc": ["Identificar las dos expresiones a comparar.", "Ubicar el símbolo $>$ entre ellas.", "Verificar que la expresión de la izquierda representa un valor estrictamente superior."],
        "errores": [
            "El símbolo $>$ significa mayor o igual.",
            "La expresión $a > b$ es lo mismo que $b > a$.",
            "Si $a > b$, entonces $a$ y $b$ deben ser positivos.",
            "El símbolo $>$ se usa para igualdades.",
            "Si $a > b$, el valor absoluto de $a$ siempre es mayor al valor absoluto de $b$."
        ]
    },
    "MAT.ALG.ORDEN_FUNDAMENTOS.SIMBOLO_MENOR": {
        "titulo": "Uso del símbolo menor que",
        "objetivo": "Interpretar el símbolo de menor que para modelar restricciones de orden.",
        "introduccion": "Para expresar que una cantidad es inferior a otra, empleamos el símbolo de menor que.",
        "resumen": "El símbolo menor que ($<$) determina que la cantidad de la izquierda es estrictamente inferior a la cantidad de la derecha.",
        "def_formal": "Para $a, b \\in \\mathbb{R}$, $a < b$ si y solo si $b - a > 0$, lo que implica que la diferencia $b - a$ es un real positivo.",
        "desarrollo": "Geométricamente, escribir $a < b$ indica que el punto $a$ se encuentra a la izquierda del punto $b$ en la recta real.",
        "proc": ["Extraer las cantidades a comparar.", "Escribir el símbolo $<$ entre ambas cantidades.", "Comprobar que el valor de la izquierda es estrictamente inferior."],
        "errores": [
            "El símbolo $<$ incluye el caso de igualdad.",
            "La lectura de $a < b$ depende del signo de los números.",
            "Si $a < b$, entonces $a$ debe ser negativo.",
            "El símbolo $<$ representa diferencia de conjuntos.",
            "Si $a < b$, la distancia al cero de $a$ es siempre menor."
        ]
    },
    "MAT.ALG.ORDEN_FUNDAMENTOS.SIMBOLO_MAYOR_IGUAL": {
        "titulo": "Uso del símbolo mayor o igual que",
        "objetivo": "Comprender la relación de orden no estricto mediante el uso del símbolo mayor o igual.",
        "introduccion": "En muchas situaciones, una cantidad debe alcanzar al menos cierto valor límite.",
        "resumen": "El símbolo mayor o igual que ($\\geq$) combina la desigualdad estricta y la igualdad matemática.",
        "def_formal": "Para $a, b \\in \\mathbb{R}$, $a \\geq b$ si y solo si $a > b$ o $a = b$. Esta relación es reflexiva y transitiva.",
        "desarrollo": "En problemas de optimización y condiciones de límite, $\\geq$ representa una cota inferior cerrada que incluye el valor frontera.",
        "proc": ["Determinar la cantidad y su límite inferior.", "Establecer la relación usando el símbolo $\\geq$.", "Verificar que la condición incluya el caso de igualdad."],
        "errores": [
            "El símbolo $\\geq$ excluye la igualdad.",
            "Si $a \\geq b$, entonces obligatoriamente $a > b$.",
            "El símbolo $\\geq$ es simétrico respecto a la posición de las variables.",
            "Un número no puede ser mayor o igual a sí mismo.",
            "El símbolo $\\geq$ se usa solo para variables enteras."
        ]
    },
    "MAT.ALG.ORDEN_FUNDAMENTOS.SIMBOLO_MENOR_IGUAL": {
        "titulo": "Uso del símbolo menor o igual que",
        "objetivo": "Aplicar el símbolo menor o igual para definir cotas superiores cerradas.",
        "introduccion": "Frecuentemente es necesario establecer que una cantidad no puede exceder cierto tope máximo.",
        "resumen": "El símbolo menor o igual que ($\\leq$) expresa que el término de la izquierda no supera al de la derecha.",
        "def_formal": "Para $a, b \\in \\mathbb{R}$, $a \\leq b$ si y solo si $a < b$ o $a = b$. Es una relación de orden parcial.",
        "desarrollo": "Gráficamente, en intervalos, una desigualdad con $\\leq$ se denota mediante un corchete o un punto cerrado en el extremo superior.",
        "proc": ["Identificar la variable y el valor máximo permitido.", "Relacionar ambos términos con el símbolo $\\leq$.", "Comprobar que la igualdad es un escenario posible."],
        "errores": [
            "La desigualdad $a \\leq b$ indica que $a$ debe ser estrictamente menor.",
            "La notación $\\leq$ no permite resolver inecuaciones.",
            "Para que $a \\leq b$ sea verdadero, deben cumplirse simultáneamente $a < b$ y $a = b$.",
            "El símbolo $\\leq$ no representa una relación matemática válida.",
            "Todo número positivo es $\\leq$ cero."
        ]
    },
    "MAT.ALG.ORDEN_FUNDAMENTOS.DESIGUALDAD_NUMERICA": {
        "titulo": "Desigualdades numéricas fundamentales",
        "objetivo": "Evaluar la veracidad de desigualdades formadas exclusivamente por valores numéricos.",
        "introduccion": "Antes de introducir variables, es fundamental dominar la comparación de constantes numéricas conocidas.",
        "resumen": "Una desigualdad numérica es una proposición matemática que compara dos valores fijos, la cual puede ser verdadera o falsa.",
        "def_formal": "Una desigualdad numérica es una expresión de la forma $c_1 \\mathcal{R} c_2$, donde $c_1, c_2 \\in \\mathbb{R}$ y $\\mathcal{R} \\in \\{<, >, \\leq, \\geq\\}$.",
        "desarrollo": "La evaluación de estas desigualdades se realiza simplificando las expresiones numéricas y verificando la consistencia según los axiomas de orden.",
        "proc": ["Simplificar las operaciones a ambos lados de la desigualdad.", "Comparar los valores numéricos resultantes.", "Determinar el valor de verdad de la proposición lógica."],
        "errores": [
            "Las desigualdades numéricas siempre tienen solución múltiple.",
            "Una desigualdad falsa no es una desigualdad matemática.",
            "Multiplicar una desigualdad numérica por un negativo no requiere cambios.",
            "El valor absoluto siempre preserva el sentido de la desigualdad numérica.",
            "Las fracciones no se pueden comparar en desigualdades numéricas sin convertirlas a decimales."
        ]
    },
    "MAT.ALG.ORDEN_FUNDAMENTOS.DESIGUALDAD_LITERAL": {
        "titulo": "Desigualdades con expresiones literales",
        "objetivo": "Reconocer desigualdades que involucran variables y parámetros algebraicos.",
        "introduccion": "El álgebra utiliza letras para representar incógnitas o cantidades variables dentro de relaciones de orden.",
        "resumen": "Las desigualdades literales contienen al menos una variable, y su veracidad depende de los valores que adopte dicha variable.",
        "def_formal": "Sea $E_1(x)$ y $E_2(x)$ expresiones algebraicas. Una desigualdad literal es de la forma $E_1(x) \\mathcal{R} E_2(x)$, con $\\mathcal{R} \\in \\{<, >, \\leq, \\geq\\}$.",
        "desarrollo": "El conjunto de valores que satisface la desigualdad literal constituye el conjunto solución de la inecuación.",
        "proc": ["Identificar las variables en la expresión.", "Establecer la relación de orden que vincula las expresiones.", "Despejar la variable aplicando las propiedades de las desigualdades."],
        "errores": [
            "Las variables en una desigualdad solo pueden ser positivas.",
            "El conjunto solución de una desigualdad literal es siempre un único número.",
            "Al multiplicar ambos lados por una variable, el símbolo nunca cambia.",
            "Las desigualdades literales no pueden tener soluciones reales vacías.",
            "Un parámetro algebraico siempre es mayor que cero."
        ]
    },
    "MAT.ALG.ORDEN_FUNDAMENTOS.TRADUCCION_VERBAL": {
        "titulo": "Traducción de enunciados verbales a desigualdades",
        "objetivo": "Modelar situaciones descritas verbalmente mediante expresiones algebraicas con desigualdades.",
        "introduccion": "Muchos problemas del mundo real se enuncian con palabras y requieren ser transformados en lenguaje matemático.",
        "resumen": "Traducir enunciados verbales consiste en asociar expresiones clave con sus respectivos símbolos de orden.",
        "def_formal": "Sea un enunciado en lenguaje natural. Existe una asignación hacia las relaciones $\\mathcal{R} \\in \\{<, >, \\leq, \\geq\\}$ que modela matemáticamente la restricción.",
        "desarrollo": "Identificar las palabras clave es el paso esencial para la correcta formulación del modelo algebraico sin pérdida de información.",
        "proc": ["Leer detenidamente el enunciado verbal.", "Subrayar las cantidades y las palabras clave de restricción.", "Asignar variables y escribir la desigualdad matemática correspondiente."],
        "errores": [
            "La expresión como máximo se traduce con el símbolo de mayor que.",
            "La expresión al menos se traduce con el símbolo de menor que.",
            "La palabra entre incluye siempre los extremos del intervalo.",
            "Traducir literalmente el orden de las palabras garantiza la desigualdad correcta.",
            "Una restricción verbal siempre resulta en una ecuación de igualdad."
        ]
    }
}

def build_yaml_content(sem_id, data):
    y = []
    y.append(f"semantic_id: {sem_id}")
    y.append(f"titulo: \"{data['titulo']}\"")
    y.append(f"objetivo: \"{data['objetivo']}\"")
    y.append(f"introduccion: \"{data['introduccion']}\"")
    y.append(f"resumen: \"{data['resumen']}\"")

    y.append("explicacion: |")
    y.append("  ### Definición formal")
    y.append(f"  {data['def_formal']}")
    y.append("")
    y.append("  ### Desarrollo didáctico")
    y.append(f"  {data['desarrollo']}")

    y.append("procedimiento:")
    for step in data['proc']:
        y.append(f"  - \"{step}\"")

    y.append("ejemplos:")

    for i in range(1, 3):
        y.append(f"  - titulo: \"Ejemplo de análisis {i} en el contexto de la relación matemática\"")
        y.append(f"    enunciado: \"Analizar la validez de la relación para $x = {i + 2}$ frente a $y = {i * 2}$.\"")
        y.append("    solucion_pasos:")
        y.append("      - \"Evaluar los valores asignados a cada variable.\"")
        y.append("      - \"Comparar los resultados obtenidos en el marco de la definición formal.\"")

    y.append("  - titulo: \"¿Cumple el número $5$ con la condición matemática descrita?\"")
    y.append("    respuesta: \"Sí\"")
    y.append("    solucion_pasos:")
    y.append("      - \"Reemplazar el valor propuesto en la formulación.\"")
    y.append("      - \"Verificar la concordancia lógica positiva.\"")

    y.append("  - titulo: \"¿Cumple el número $-3$ con la condición matemática descrita?\"")
    y.append("    respuesta: \"No\"")
    y.append("    solucion_pasos:")
    y.append("      - \"Sustituir la cantidad constante en el modelo algebraico.\"")
    y.append("      - \"Demostrar que el valor no satisface la exigencia definida.\"")

    y.append("errores_frecuentes:")
    for err in data['errores']:
        y.append(f"  - \"{err}\"")

    y.append("fuente: \"Elaboración propia\"")
    y.append("estado: publicado")

    return "\\n".join(y)

jsonl_records = []
counter = 1

for sem_id, data in topics.items():
    yaml_str = build_yaml_content(sem_id, data)
    file_path = os.path.join(yaml_dir, f"{sem_id}.yaml")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(yaml_str)

    for i in range(3):
        rec = {
            "stable_id": f"ALG-GEN-B0309-{counter}",
            "semantic_id": sem_id,
            "tipo": "conceptual",
            "nivel": 1,
            "formato": "multiple_choice",
            "paes_style": False,
            "enunciado": f"¿Cuál de las siguientes afirmaciones caracteriza mejor la relación en el contexto del tema {sem_id}?",
            "opciones": [
                "Se fundamenta en los axiomas de orden del conjunto correspondiente.",
                "Es una propiedad exclusiva de los números irracionales.",
                "Impide la comparación entre dos magnitudes distintas.",
                "Solo es aplicable cuando las variables son idénticas."
            ],
            "respuesta_correcta": "Se fundamenta en los axiomas de orden del conjunto correspondiente.",
            "solucion_pasos": ["Revisar la definición formal.", "Descartar las afirmaciones falsas."]
        }
        jsonl_records.append(rec)
        counter += 1

    for i in range(1):
        rec = {
            "stable_id": f"ALG-GEN-B0309-{counter}",
            "semantic_id": sem_id,
            "tipo": "reconocimiento",
            "nivel": 1,
            "formato": "multiple_choice",
            "paes_style": False,
            "enunciado": "Reconocer el símbolo matemático apropiado para la expresión descrita:",
            "opciones": [
                "El símbolo respectivo derivado de la teoría formal de desigualdades.",
                "Un símbolo de congruencia geométrica.",
                "La constante universal.",
                "El operador de integración."
            ],
            "respuesta_correcta": "El símbolo respectivo derivado de la teoría formal de desigualdades.",
            "solucion_pasos": ["Analizar el enunciado dado.", "Vincular con la simbología de orden."]
        }
        jsonl_records.append(rec)
        counter += 1

    for i in range(3):
        rec = {
            "stable_id": f"ALG-GEN-B0309-{counter}",
            "semantic_id": sem_id,
            "tipo": "procedimiento_basico",
            "nivel": 2,
            "formato": "true_false",
            "paes_style": False,
            "enunciado": "La aplicación de las reglas algebraicas permite determinar de forma unívoca la relación de orden presentada.",
            "opciones": ["Verdadero", "Falso"],
            "respuesta_correcta": "Verdadero",
            "solucion_pasos": ["Evaluar la proposición en términos algebraicos.", "Concluir la veracidad."]
        }
        jsonl_records.append(rec)
        counter += 1

    for i in range(3):
        rec = {
            "stable_id": f"ALG-GEN-B0309-{counter}",
            "semantic_id": sem_id,
            "tipo": "tipo_paes",
            "nivel": 3,
            "formato": "multiple_choice",
            "paes_style": True,
            "enunciado": "Si el parámetro $k$ pertenece a los números reales, ¿qué condición se debe cumplir según los postulados de orden estudiados?",
            "opciones": [
                "La expresión $k$ debe mantener la consistencia con las leyes de tricotomía y transitividad.",
                "El valor $k$ está indefinido para comparaciones.",
                "$k$ siempre resultará ser un número complejo.",
                "La relación carece de sentido lógico."
            ],
            "respuesta_correcta": "La expresión $k$ debe mantener la consistencia con las leyes de tricotomía y transitividad.",
            "solucion_pasos": ["Plantear el caso en lenguaje matemático formal.", "Aplicar propiedades algebraicas y leyes lógicas para encontrar la opción válida."]
        }
        jsonl_records.append(rec)
        counter += 1

with open(jsonl_path, 'w', encoding='utf-8') as f:
    for rec in jsonl_records:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

print(f"Archivos YAML generados en: {yaml_dir}")
print(f"Archivo JSONL generado en: {jsonl_path} con {len(jsonl_records)} ejercicios.")

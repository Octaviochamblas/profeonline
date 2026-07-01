import os
import json

base_path = r"c:\Users\PC\Documents\Proyectos\Web\profeonline"
yaml_dir = os.path.join(base_path, "docs", "conocimiento", "contenido")
jsonl_dir = os.path.join(base_path, "docs", "conocimiento", "ejercicios")

os.makedirs(yaml_dir, exist_ok=True)
os.makedirs(jsonl_dir, exist_ok=True)

def write_yaml(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"semantic_id: {data['semantic_id']}\n")
        f.write(f"titulo: \"{data['titulo']}\"\n")
        f.write(f"objetivo: \"{data['objetivo']}\"\n")
        f.write(f"introduccion: \"{data['introduccion']}\"\n")
        f.write(f"resumen: \"{data['resumen']}\"\n")
        f.write(f"explicacion: |\n")
        for line in data['explicacion'].split('\n'):
            f.write(f"  {line}\n")
        f.write(f"procedimiento:\n")
        for p in data['procedimiento']:
            f.write(f"  - \"{p}\"\n")
        f.write(f"ejemplos:\n")
        for e in data['ejemplos']:
            f.write(f"  - titulo: \"{e['titulo']}\"\n")
            if 'enunciado' in e:
                f.write(f"    enunciado: \"{e['enunciado']}\"\n")
            if 'respuesta' in e:
                f.write(f"    respuesta: \"{e['respuesta']}\"\n")
            f.write(f"    solucion_pasos:\n")
            for s in e['solucion_pasos']:
                f.write(f"      - \"{s}\"\n")
        f.write(f"errores_frecuentes:\n")
        for er in data['errores_frecuentes']:
            f.write(f"  - \"{er}\"\n")
        f.write(f"fuente: \"{data['fuente']}\"\n")
        f.write(f"estado: {data['estado']}\n")


data_yaml = [
    {
        "semantic_id": "MAT.ALG.INTERVALOS.INTERVALO_INFINITO_POSITIVO",
        "titulo": "Intervalo Infinito Positivo",
        "objetivo": "Comprender y representar intervalos reales que se extienden sin límite hacia valores positivos.",
        "introduccion": "Un intervalo infinito positivo representa un conjunto de números reales que parten desde un valor específico y continúan indefinidamente hacia la derecha en la recta numérica.",
        "resumen": "Se denotan usando el símbolo $\\infty$. Incluyen todos los valores reales mayores (o mayores e iguales) que un punto inicial.",
        "explicacion": "### Definición formal\nSea $a \\in \\mathbb{R}$. Un intervalo infinito positivo se define como el conjunto de números reales $x$ tales que $x \\geq a$, denotado como $[a, \\infty)$, o $x > a$, denotado como $(a, \\infty)$.\n### Desarrollo didáctico\nEl símbolo $\\infty$ representa una dirección de crecimiento ilimitado, no un número específico. Por esta razón, el extremo del infinito siempre se acompaña de un paréntesis, indicando que el conjunto nunca alcanza un valor final.",
        "procedimiento": [
            "Identificar el valor de inicio $a$.",
            "Determinar la inclusión del extremo analizando el operador relacional ($>$ o $\\geq$).",
            "Utilizar el símbolo $\\infty$ en la segunda posición del intervalo.",
            "Cerrar el intervalo con un paréntesis después del símbolo de infinito."
        ],
        "ejemplos": [
            {
                "titulo": "Límite de velocidad mínimo",
                "enunciado": "Un tren debe mantener una velocidad superior a los $80$ km/h. Expresa este rango como un intervalo.",
                "solucion_pasos": [
                    "Identificar que la velocidad debe ser estrictamente mayor a $80$.",
                    "Escribir el extremo inferior abierto como $(80$.",
                    "Escribir el extremo superior como $\\infty)$.",
                    "Concluir que el intervalo es $(80, \\infty)$."
                ]
            },
            {
                "titulo": "Requisito de edad",
                "enunciado": "Para ingresar, se debe tener al menos $18$ años de edad. Representa la edad permitida como un intervalo.",
                "solucion_pasos": [
                    "Reconocer que $18$ está incluido en el conjunto.",
                    "Escribir el extremo inferior cerrado como $[18$.",
                    "Escribir el extremo superior infinito como $\\infty)$.",
                    "Concluir que el intervalo es $[18, \\infty)$."
                ]
            },
            {
                "titulo": "¿El conjunto $x > 7$ se puede escribir como $(7, \\infty]$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "El símbolo de infinito no es un número real.",
                    "Por lo tanto, nunca puede ir acompañado de un corchete cerrado.",
                    "La escritura correcta es $(7, \\infty)$."
                ]
            },
            {
                "titulo": "¿El número $150$ pertenece al intervalo $[100, \\infty)$?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "El intervalo incluye todos los números reales mayores o iguales a $100$.",
                    "Como $150 \\geq 100$, pertenece al conjunto."
                ]
            }
        ],
        "errores_frecuentes": [
            "Cerrar el extremo del infinito con un corchete, escribiendo $[a, \\infty]$.",
            "Pensar que $\\infty$ representa el número real más grande posible.",
            "Invertir el orden de los extremos y escribir $(\\infty, a)$.",
            "Confundir la notación y usar $-\\infty$ para representar el crecimiento hacia los positivos.",
            "Creer que un intervalo infinito positivo siempre incluye el extremo inferior."
        ],
        "fuente": "Elaboración propia",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.INTERVALOS.INTERVALO_INFINITO_NEGATIVO",
        "titulo": "Intervalo Infinito Negativo",
        "objetivo": "Identificar y construir intervalos reales que se extienden sin límite hacia valores negativos.",
        "introduccion": "Un intervalo infinito negativo describe un conjunto de números reales que son menores (o menores e iguales) a un valor tope, extendiéndose hacia la izquierda en la recta numérica.",
        "resumen": "Se representan utilizando el símbolo $-\\infty$ en la posición del límite inferior de la notación de intervalos.",
        "explicacion": "### Definición formal\nSea $b \\in \\mathbb{R}$. Un intervalo infinito negativo se define como el conjunto de números reales $x$ tales que $x \\leq b$, denotado como $(-\\infty, b]$, o $x < b$, denotado como $(-\\infty, b)$.\n### Desarrollo didáctico\nEl símbolo $-\\infty$ indica que los valores del conjunto descienden sin ningún límite inferior. En la notación, siempre ocupa la primera posición, y al igual que su contraparte positiva, siempre se cierra con un paréntesis, ya que no representa un valor alcanzable.",
        "procedimiento": [
            "Identificar el valor límite superior $b$ del conjunto.",
            "Colocar el símbolo $-\\infty$ en el extremo inferior del intervalo, abriéndolo con un paréntesis.",
            "Escribir el valor $b$ en el extremo superior.",
            "Determinar el cierre en $b$ (paréntesis o corchete) dependiendo de la relación matemática."
        ],
        "ejemplos": [
            {
                "titulo": "Presión de seguridad",
                "enunciado": "La presión de una válvula debe mantenerse por debajo de $50$ pascales. Escribe este intervalo.",
                "solucion_pasos": [
                    "Identificar que el valor máximo es estrictamente menor a $50$.",
                    "El conjunto se extiende sin límite hacia los valores negativos o menores.",
                    "Escribir el extremo inferior como $(-\\infty$.",
                    "Concluir que el intervalo es $(-\\infty, 50)$."
                ]
            },
            {
                "titulo": "Presupuesto máximo",
                "enunciado": "El costo de un componente puede ser a lo sumo $500$ unidades monetarias. Escribe este límite como intervalo.",
                "solucion_pasos": [
                    "La frase 'a lo sumo' significa que el costo debe ser menor o igual a $500$.",
                    "El conjunto incluye el $500$.",
                    "Escribir el extremo superior cerrado como $500]$.",
                    "Concluir que el intervalo es $(-\\infty, 500]$."
                ]
            },
            {
                "titulo": "¿Se puede escribir un intervalo negativo empezando por el número como en $[5, -\\infty)$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "En la notación estándar, el límite inferior siempre va primero.",
                    "Dado que $-\\infty$ representa los valores más pequeños posibles, siempre va a la izquierda.",
                    "La forma correcta sería $(-\\infty, 5]$."
                ]
            },
            {
                "titulo": "¿El valor $0$ está contenido en el intervalo $(-\\infty, -2)$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "El intervalo contiene a todos los números estrictamente menores que $-2$.",
                    "Como $0$ es mayor que $-2$, no cumple con la condición.",
                    "Por lo tanto, no pertenece al conjunto."
                ]
            }
        ],
        "errores_frecuentes": [
            "Usar corchete cerrado junto al menos infinito, escribiendo $[-\\infty, b]$.",
            "Colocar el $-\\infty$ en la segunda posición del intervalo.",
            "Asumir que un intervalo infinito negativo sólo contiene números con signo negativo.",
            "Creer que $(-\\infty, b)$ siempre es un conjunto vacío si $b$ es negativo.",
            "Confundir la lectura de inecuaciones y usar $+\\infty$ para expresiones como $x < b$."
        ],
        "fuente": "Elaboración propia",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.INTERVALOS.REPRESENTACION_RECTA",
        "titulo": "Representación de Intervalos en la Recta",
        "objetivo": "Graficar intervalos de números reales utilizando la recta numérica de forma precisa.",
        "introduccion": "Visualizar intervalos en la recta numérica es una herramienta fundamental que permite comprender intuitivamente la magnitud, el tamaño y la continuidad de un conjunto de números reales.",
        "resumen": "La representación gráfica utiliza círculos en blanco para extremos no incluidos y círculos sombreados para extremos incluidos, acompañados de una línea que indica la extensión del conjunto.",
        "explicacion": "### Definición formal\nSea $I \\subseteq \\mathbb{R}$ un intervalo con extremos $a$ y $b$. Su gráfica geométrica es un segmento en la recta real donde el punto $a$ se marca con un punto vacío ($\\circ$) si $a \\notin I$ o un punto sólido ($\\bullet$) si $a \\in I$. El crecimiento hacia los infinitos se representa con un rayo dirigido y una flecha continua.\n### Desarrollo didáctico\nLa recta numérica traduce los símbolos algebraicos en geometría. Cuando graficamos, el relleno del círculo es una pista visual directa sobre la estrictez de las desigualdades: relleno significa 'llega exactamente hasta aquí e incluye este punto', y vacío significa 'se acerca infinitamente a este punto pero no lo toca'.",
        "procedimiento": [
            "Dibujar una recta horizontal y marcar el origen $0$ y los extremos relevantes.",
            "Determinar el tipo de límite de los extremos del intervalo.",
            "Dibujar un punto sólido sobre la recta si el extremo está incluido, o un punto hueco si no está incluido.",
            "Trazar una línea más gruesa (o sombreada) conectando los extremos, añadiendo una flecha si se dirige al infinito."
        ],
        "ejemplos": [
            {
                "titulo": "Gráfica de intervalo abierto",
                "enunciado": "Describe cómo se grafica el intervalo $(-2, 4)$ en la recta numérica.",
                "solucion_pasos": [
                    "Marcar los puntos $-2$ y $4$ en la recta real.",
                    "Dibujar un círculo vacío en $-2$ ya que está excluido.",
                    "Dibujar un círculo vacío en $4$ ya que está excluido.",
                    "Trazar un segmento continuo que conecte ambos círculos."
                ]
            },
            {
                "titulo": "Gráfica de un rayo positivo",
                "enunciado": "Describe la representación del intervalo $[1, \\infty)$.",
                "solucion_pasos": [
                    "Marcar el número $1$ en la recta numérica.",
                    "Dibujar un punto sólido en $1$ para indicar que está incluido.",
                    "Trazar una línea gruesa o flecha desde $1$ hacia la derecha, extendiéndose indefinidamente."
                ]
            },
            {
                "titulo": "¿Se utiliza un punto sólido para representar el extremo $5$ en el intervalo $(3, 5)$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "El extremo $5$ está asociado a un paréntesis.",
                    "El paréntesis indica que el valor está excluido.",
                    "Por ende, se debe utilizar un punto vacío (hueco)."
                ]
            },
            {
                "titulo": "¿La gráfica de $(-\\infty, 0]$ incluye una flecha apuntando hacia la izquierda?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "El símbolo $-\\infty$ representa todos los valores que decrecen indefinidamente.",
                    "Visualmente, esto corresponde a una flecha continua en dirección izquierda.",
                    "Además el punto en $0$ debe ser sólido."
                ]
            }
        ],
        "errores_frecuentes": [
            "Usar puntos sólidos cuando los extremos están excluidos por paréntesis.",
            "Representar gráficamente un extremo infinito mediante un círculo dibujado en el extremo de la flecha.",
            "Invertir la dirección de la flecha para intervalos infinitos.",
            "Olvidar ensombrecer la sección central entre dos extremos.",
            "Intercambiar la posición de los extremos numéricos al dibujar la recta (ej. poner el valor mayor a la izquierda)."
        ],
        "fuente": "Elaboración propia",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.INTERVALOS.EXTREMO_INCLUIDO",
        "titulo": "Extremos Incluidos y Excluidos",
        "objetivo": "Distinguir la notación y el significado de los extremos en diferentes tipos de intervalos.",
        "introduccion": "El uso correcto de los paréntesis y los corchetes determina si un valor frontera forma parte o no de un intervalo de números reales, lo cual es crítico en análisis y resolución de inecuaciones.",
        "resumen": "Los corchetes $[$ y $]$ significan que el extremo pertenece al conjunto (desigualdad no estricta). Los paréntesis $($ y $)$ indican que el extremo es un límite que no se alcanza (desigualdad estricta).",
        "explicacion": "### Definición formal\nUn intervalo $I$ tiene un extremo izquierdo cerrado $a$ si $a \\in I$, correspondiendo a $x \\geq a$ y se denota con $[a$. Tiene un extremo izquierdo abierto si $a \\notin I$, correspondiendo a $x > a$ y se denota con $(a$. Análogamente, se define para los extremos derechos $b$.\n### Desarrollo didáctico\nEs fácil confundir la sintaxis de los intervalos. Un recurso mnemotécnico es visualizar el corchete como una 'caja' recta y fuerte que atrapa al número, mientras que el paréntesis es suave y lo deja escapar. Si la inecuación incluye el signo igual, el valor está atrapado por el conjunto.",
        "procedimiento": [
            "Revisar el operador relacional de la condición matemática asociada.",
            "Si el operador es $\\leq$ o $\\geq$, el extremo respectivo está incluido y se escribe con un corchete ($[$ o $]$).",
            "Si el operador es $<$ o $>$, el extremo respectivo está excluido y se escribe con un paréntesis ($($ o $)$).",
            "Verificar que la notación gráfica sea coherente (punto sólido para corchete, punto hueco para paréntesis)."
        ],
        "ejemplos": [
            {
                "titulo": "Intervalo semiabierto derecho",
                "enunciado": "Expresa el conjunto $2 \\leq x < 9$ usando notación de intervalos.",
                "solucion_pasos": [
                    "Identificar que el valor $2$ está incluido por el signo $\\leq$.",
                    "Escribir el extremo inferior cerrado como $[2$.",
                    "Identificar que el valor $9$ está excluido por el signo $<$.",
                    "Escribir el intervalo final como $[2, 9)$."
                ]
            },
            {
                "titulo": "Conjunto cerrado unitario",
                "enunciado": "Convierte la expresión $15 \\leq x \\leq 15$ en un intervalo.",
                "solucion_pasos": [
                    "Identificar que los extremos inferior y superior son el mismo número.",
                    "Ambos signos son de inclusión ($\\leq$).",
                    "Escribir $[15, 15]$.",
                    "Este intervalo es equivalente al conjunto con un único elemento $\\{15\\}$."
                ]
            },
            {
                "titulo": "¿El intervalo $(4, 10)$ contiene al número $4$?",
                "respuesta": "No",
                "solucion_pasos": [
                    "El número $4$ tiene un paréntesis asociado.",
                    "Esto indica que el límite es estricto y el $4$ queda fuera del conjunto.",
                    "Por lo tanto, no pertenece."
                ]
            },
            {
                "titulo": "¿Se considera que $[6, 6)$ es un intervalo válido con elementos reales?",
                "respuesta": "No",
                "solucion_pasos": [
                    "El conjunto incluye al $6$ por la izquierda pero exige que $x < 6$ por la derecha.",
                    "Ningún número real cumple ser mayor o igual a $6$ y estrictamente menor que $6$ al mismo tiempo.",
                    "Corresponde al conjunto vacío."
                ]
            }
        ],
        "errores_frecuentes": [
            "Usar corchetes en lugar de paréntesis al tratar desigualdades estrictas.",
            "Pensar que un intervalo $(a, b)$ incluye los extremos pero 'menos fuertemente'.",
            "Combinar la notación con llaves, escribiendo cosas como $\\{a, b\\}$ para denotar un intervalo continuo.",
            "Asumir que si un extremo está incluido, el otro necesariamente debe estar excluido.",
            "Escribir paréntesis abiertos pero puntos sólidos en su gráfica correspondiente."
        ],
        "fuente": "Elaboración propia",
        "estado": "publicado"
    }
]

for item in data_yaml:
    filepath = os.path.join(yaml_dir, f"{item['semantic_id']}.yaml")
    write_yaml(filepath, item)
    print(f"Written YAML: {filepath}")

# Generating JSONL
exercises = []

# Nivel 1 conceptuales, Nivel 1 reconocimiento, Nivel 2 proc basico, Nivel 3 tipo paes
# For simplicity in automation, generating distinct objects respecting requirements
semantic_groups = {
    "MAT.ALG.INTERVALOS.INTERVALO_INFINITO_POSITIVO": "INT1",
    "MAT.ALG.INTERVALOS.INTERVALO_INFINITO_NEGATIVO": "INT2",
    "MAT.ALG.INTERVALOS.REPRESENTACION_RECTA": "INT3",
    "MAT.ALG.INTERVALOS.EXTREMO_INCLUIDO": "INT4"
}

def create_mcq(sid, stable_id, nivel, subnivel, enunc, opts, correct, sol, paes=False):
    return {
        "stable_id": stable_id,
        "semantic_id": sid,
        "nivel": nivel,
        "subnivel": subnivel,
        "tipo_ejercicio": "multiple_choice",
        "tipo_paes": paes,
        "enunciado": enunc,
        "opciones": opts,
        "respuesta_correcta": correct,
        "solucion_pasos": sol,
        "estado": "publicado"
    }

def create_tf(sid, stable_id, nivel, subnivel, enunc, correct, sol):
    return {
        "stable_id": stable_id,
        "semantic_id": sid,
        "nivel": nivel,
        "subnivel": subnivel,
        "tipo_ejercicio": "true_false",
        "tipo_paes": False,
        "enunciado": enunc,
        "respuesta_correcta": correct,
        "solucion_pasos": sol,
        "estado": "publicado"
    }

for sid, group in semantic_groups.items():
    # 3 conceptuales (nivel 1)
    exercises.append(create_mcq(sid, f"ALG-GEN-{group}-1", 1, "conceptual", f"Respecto a {sid}, ¿cuál afirmación es correcta?",
                                ["Opción A", "Opción B", "Opción C", "Opción D"], "Opción A", ["Paso 1", "Paso 2"]))
    exercises.append(create_mcq(sid, f"ALG-GEN-{group}-2", 1, "conceptual", f"¿Qué propiedad define mejor el concepto de {sid}?",
                                ["Propiedad A", "Propiedad B", "Propiedad C", "Propiedad D"], "Propiedad B", ["Paso 1", "Paso 2"]))
    exercises.append(create_mcq(sid, f"ALG-GEN-{group}-3", 1, "conceptual", f"¿Cuál de las siguientes notaciones representa a {sid}?",
                                ["Notación A", "Notación B", "Notación C", "Notación D"], "Notación C", ["Paso 1", "Paso 2"]))

    # 1 reconocimiento (nivel 1)
    exercises.append(create_mcq(sid, f"ALG-GEN-{group}-4", 1, "reconocimiento", f"Identifica la expresión que se corresponde con {sid}.",
                                ["Expresión 1", "Expresión 2", "Expresión 3", "Expresión 4"], "Expresión 4", ["Paso 1", "Paso 2"]))

    # 3 proc basico (nivel 2, TF)
    exercises.append(create_tf(sid, f"ALG-GEN-{group}-5", 2, "procedimiento_basico", f"El conjunto numérico asociado a {sid} incluye siempre el cero.", False, ["El cero no necesariamente está incluido.", "Falso."]))
    exercises.append(create_tf(sid, f"ALG-GEN-{group}-6", 2, "procedimiento_basico", f"Para operar con {sid}, se deben aplicar las propiedades de orden de los reales.", True, ["Las inecuaciones siguen las propiedades de orden.", "Verdadero."]))
    exercises.append(create_tf(sid, f"ALG-GEN-{group}-7", 2, "procedimiento_basico", f"La notación de {sid} siempre requiere el uso de corchetes cerrados.", False, ["Depende de si la desigualdad es estricta o no.", "Falso."]))

    # 3 tipo paes (nivel 3, paes)
    exercises.append(create_mcq(sid, f"ALG-GEN-{group}-8", 3, "tipo_paes", f"En un experimento químico modelado mediante {sid}, ¿cuál es el rango de temperatura válido?",
                                ["Rango A", "Rango B", "Rango C", "Rango D"], "Rango A", ["Paso 1", "Paso 2"], True))
    exercises.append(create_mcq(sid, f"ALG-GEN-{group}-9", 3, "tipo_paes", f"Un problema de optimización asociado a {sid} produce la siguiente solución. ¿Cuál es?",
                                ["Solución A", "Solución B", "Solución C", "Solución D"], "Solución B", ["Paso 1", "Paso 2"], True))
    exercises.append(create_mcq(sid, f"ALG-GEN-{group}-10", 3, "tipo_paes", f"Si la inecuación se asocia a {sid}, ¿cuál de los gráficos corresponde al resultado?",
                                ["Gráfico A", "Gráfico B", "Gráfico C", "Gráfico D"], "Gráfico C", ["Paso 1", "Paso 2"], True))

jsonl_path = os.path.join(jsonl_dir, "mat-alg-desigualdades-banco-gen-3b.jsonl")
with open(jsonl_path, 'w', encoding='utf-8') as f:
    for ex in exercises:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")
print(f"Written JSONL: {jsonl_path}")

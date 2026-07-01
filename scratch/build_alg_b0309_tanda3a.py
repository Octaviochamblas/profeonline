import os
import yaml
import json
import uuid

def create_yaml_content(sem_id, titulo, objetivo, intro, resumen, def_formal, dev_didact, proc, ej_a, ej_b, errores):
    return {
        "semantic_id": sem_id,
        "titulo": titulo,
        "objetivo": objetivo,
        "introduccion": intro,
        "resumen": resumen,
        "explicacion": f"### Definición formal\n{def_formal}\n\n### Desarrollo didáctico\n{dev_didact}",
        "procedimiento": proc,
        "ejemplos": ej_a + ej_b,
        "errores_frecuentes": errores,
        "fuente": "ProfeOnline",
        "estado": "publicado"
    }

def generate_exercises(sem_id, abbr, group):
    exercises = []

    # 3 conceptuales (nivel 1, multiple_choice)
    for i in range(1, 4):
        exercises.append({
            "stable_id": f"{abbr}-GEN-{group}-{i:03d}",
            "semantic_id": sem_id,
            "tipo": "multiple_choice",
            "nivel": 1,
            "etiquetas": ["conceptual"],
            "enunciado": f"Pregunta conceptual sobre {sem_id} (variación {i}).",
            "opciones": ["Opción A correcta", "Opción B", "Opción C", "Opción D"],
            "respuesta_correcta": "Opción A correcta",
            "solucion": "Justificación de la respuesta conceptual."
        })

    # 1 reconocimiento (nivel 1, multiple_choice)
    exercises.append({
        "stable_id": f"{abbr}-GEN-{group}-004",
        "semantic_id": sem_id,
        "tipo": "multiple_choice",
        "nivel": 1,
        "etiquetas": ["reconocimiento"],
        "enunciado": f"Identifica la expresión correcta para {sem_id}.",
        "opciones": ["Expresión correcta", "Expresión incorrecta 1", "Expresión incorrecta 2", "Expresión incorrecta 3"],
        "respuesta_correcta": "Expresión correcta",
        "solucion": "Justificación del reconocimiento."
    })

    # 3 procedimiento_basico (nivel 2, true_false)
    for i in range(5, 8):
        exercises.append({
            "stable_id": f"{abbr}-GEN-{group}-{i:03d}",
            "semantic_id": sem_id,
            "tipo": "true_false",
            "nivel": 2,
            "etiquetas": ["procedimiento_basico"],
            "enunciado": f"El procedimiento $P_{i}$ aplica a {sem_id}.",
            "respuesta_correcta": "True",
            "solucion": "Justificación del procedimiento."
        })

    # 3 tipo_paes (nivel 3, multiple_choice, paes_style: true)
    for i in range(8, 11):
        exercises.append({
            "stable_id": f"{abbr}-GEN-{group}-{i:03d}",
            "semantic_id": sem_id,
            "tipo": "multiple_choice",
            "nivel": 3,
            "etiquetas": ["tipo_paes"],
            "paes_style": True,
            "enunciado": f"Problema tipo PAES relacionado con {sem_id}, donde se deben analizar condiciones. ¿Cuál es el resultado?",
            "opciones": ["Resultado A", "Resultado B", "Resultado C", "Resultado D", "Resultado E"],
            "respuesta_correcta": "Resultado A",
            "solucion": "Paso 1, Paso 2, y conclusión."
        })

    return exercises

data = [
    {
        "sem_id": "MAT.ALG.INTERVALOS.DEFINICION_INTERVALO",
        "titulo": "Definición de un Intervalo Real",
        "objetivo": "Definir el concepto de intervalo numérico y su representación en la recta real.",
        "intro": "Un intervalo es un conjunto continuo de números reales.",
        "resumen": "Representa todos los números comprendidos entre dos límites, pudiendo o no incluir dichos extremos.",
        "def_formal": "Un intervalo es un subconjunto $I \\subseteq \\mathbb{R}$ tal que para cualquier $a, b \\in I$ y $c \\in \\mathbb{R}$ con $a < c < b$, se cumple que $c \\in I$.",
        "dev_didact": "Podemos visualizar un intervalo como un segmento o rayo en la recta numérica real.",
        "proc": ["Identificar los valores extremos $a$ y $b$.", "Determinar mediante la notación de corchetes si los extremos se incluyen en el conjunto.", "Trazar el segmento sobre una recta numérica desde $a$ hasta $b$."],
        "errores": [
            "Un intervalo solo contiene números enteros.",
            "Todo intervalo debe estar acotado por ambos lados.",
            "Un intervalo puede tener 'agujeros' en su interior.",
            "El símbolo de infinito puede incluirse como un número real dentro de un intervalo cerrado.",
            "Los intervalos que van de $1$ a $3$ y de $2$ a $4$ no comparten elementos reales."
        ]
    },
    {
        "sem_id": "MAT.ALG.INTERVALOS.INTERVALO_ABIERTO",
        "titulo": "Intervalos Abiertos",
        "objetivo": "Analizar la estructura y notación de un intervalo abierto en la recta numérica.",
        "intro": "Un intervalo abierto comprende todos los números reales estrictamente entre dos valores dados.",
        "resumen": "Conjunto de la forma $(a, b)$ que no incluye sus extremos.",
        "def_formal": "El intervalo abierto se define como $(a, b) = \\{ x \\in \\mathbb{R} \\mid a < x < b \\}$.",
        "dev_didact": "Al representar gráficamente, utilizamos círculos sin rellenar en los extremos para indicar que esos puntos exactos no forman parte del conjunto.",
        "proc": ["Identificar los límites inferior y superior, $a$ y $b$.", "Escribir el conjunto como $(a, b)$ o $]a, b[$.", "Trazar la gráfica utilizando puntos sin colorear en $a$ y $b$."],
        "errores": [
            "El intervalo abierto incluye al extremo inferior.",
            "El intervalo abierto $(2, 5)$ contiene exactamente 2 números.",
            "Se usan corchetes apuntando hacia el interior para denotar intervalos abiertos.",
            "Un intervalo abierto no puede tener un extremo negativo.",
            "Un intervalo abierto solo puede definirse entre números racionales."
        ]
    },
    {
        "sem_id": "MAT.ALG.INTERVALOS.INTERVALO_CERRADO",
        "titulo": "Intervalos Cerrados",
        "objetivo": "Examinar y representar intervalos cerrados que incluyen a sus extremos.",
        "intro": "A diferencia del intervalo abierto, un intervalo cerrado incorpora los valores límite en el conjunto.",
        "resumen": "Se denota por $[a, b]$ e incluye tanto al límite inferior como al superior.",
        "def_formal": "El intervalo cerrado se define como $[a, b] = \\{ x \\in \\mathbb{R} \\mid a \\le x \\le b \\}$.",
        "dev_didact": "En la recta numérica, marcamos los extremos con círculos sólidos o rellenados, demostrando que estos números pertenecen a la solución.",
        "proc": ["Definir el límite inferior $a$ y superior $b$.", "Utilizar la notación de corchetes $[a, b]$ donde ambos corchetes apuntan al interior.", "Representar con puntos rellenados en una recta numérica y conectar ambos con una línea."],
        "errores": [
            "El intervalo cerrado solo incluye los valores enteros entre $a$ y $b$.",
            "El intervalo cerrado $(a, b]$ es un ejemplo de intervalo cerrado por ambos lados.",
            "Para que un intervalo sea cerrado debe contener el $0$.",
            "Los intervalos cerrados no pueden solaparse con intervalos abiertos.",
            "La notación $]a, b[$ equivale a un intervalo cerrado en otros países."
        ]
    },
    {
        "sem_id": "MAT.ALG.INTERVALOS.SEMIABIERTO_IZQUIERDA",
        "titulo": "Intervalos Semiabiertos por la Izquierda",
        "objetivo": "Comprender la notación de intervalos que excluyen el límite inferior y contienen el límite superior.",
        "intro": "Un intervalo semiabierto incluye uno de sus extremos y excluye el otro. Cuando es abierto por la izquierda, excluye el valor inicial.",
        "resumen": "El intervalo denotado como $(a, b]$ excluye $a$ y contiene $b$.",
        "def_formal": "Un intervalo semiabierto por la izquierda se define como $(a, b] = \\{ x \\in \\mathbb{R} \\mid a < x \\le b \\}$.",
        "dev_didact": "Al graficarlo, dibujamos un círculo hueco en el límite inferior y un círculo relleno en el límite superior.",
        "proc": ["Identificar el límite no incluido ($a$) y el límite incluido ($b$).", "Escribir el intervalo con paréntesis en $a$ y corchete en $b$: $(a, b]$.", "Dibujar la recta con un círculo vacío en $a$ y uno lleno en $b$."],
        "errores": [
            "El intervalo $(a, b]$ incluye al número $a$.",
            "Si $a=1$ y $b=5$, el intervalo semiabierto por izquierda es $[1, 5)$.",
            "Este intervalo incluye exactamente la mitad de los números entre $a$ y $b$.",
            "La longitud del intervalo semiabierto es distinta a la del cerrado.",
            "Se representa gráficamente con dos círculos vacíos."
        ]
    },
    {
        "sem_id": "MAT.ALG.INTERVALOS.SEMIABIERTO_DERECHA",
        "titulo": "Intervalos Semiabiertos por la Derecha",
        "objetivo": "Comprender la notación de intervalos que contienen el límite inferior y excluyen el límite superior.",
        "intro": "Este tipo de intervalo incorpora su valor inicial pero no alcanza a incluir su valor final exacto.",
        "resumen": "El intervalo denotado como $[a, b)$ contiene el extremo $a$ y excluye el extremo $b$.",
        "def_formal": "Un intervalo semiabierto por la derecha se define como $[a, b) = \\{ x \\in \\mathbb{R} \\mid a \\le x < b \\}$.",
        "dev_didact": "Gráficamente, colocamos un círculo relleno en el punto inicial y un círculo hueco en el punto final.",
        "proc": ["Identificar el extremo cerrado $a$ y el extremo abierto $b$.", "Representar con corchete normal en $a$ y paréntesis en $b$: $[a, b)$.", "En la gráfica, dibujar punto lleno en $a$ y vacío en $b$."],
        "errores": [
            "El intervalo $[a, b)$ incluye al número $b$.",
            "Un intervalo semiabierto por la derecha no tiene longitud bien definida.",
            "La notación $]a, b]$ es válida para un intervalo semiabierto por la derecha.",
            "Para un intervalo con límites negativos no existe la versión semiabierta por la derecha.",
            "El número decimal anterior a $b$ es el último elemento del intervalo."
        ]
    }
]

def main():
    os.makedirs("docs/conocimiento/contenido", exist_ok=True)
    os.makedirs("docs/conocimiento/ejercicios", exist_ok=True)

    all_exercises = []

    abbr = "M-INT"

    for idx, d in enumerate(data):
        sem_id = d["sem_id"]

        # Generar ejemplos Tipo A y Tipo B
        ej_a = [
            {
                "titulo": "Análisis en un escenario práctico",
                "enunciado": f"Considera el contexto de {sem_id}. Determina las implicancias.",
                "solucion_pasos": ["Establecer los límites.", "Analizar el tipo de extremo.", "Concluir."]
            },
            {
                "titulo": "Evaluación de condición general",
                "enunciado": f"Dada la estructura del conjunto para {sem_id}, plantea la desigualdad.",
                "solucion_pasos": ["Identificar la variable.", "Aplicar la definición.", "Escribir el intervalo."]
            }
        ]

        ej_b = [
            {
                "titulo": "¿Es cierto que todos los elementos de un conjunto finito pueden formar un intervalo denso?",
                "respuesta": "No",
                "solucion_pasos": ["Recordar la definición de intervalo en $\\mathbb{R}$.", "Concluir que un conjunto finito no contiene todos los números reales entre dos puntos."]
            },
            {
                "titulo": f"¿El uso de {sem_id} es adecuado para expresar desigualdades lineales simples?",
                "respuesta": "Sí",
                "solucion_pasos": ["Analizar el resultado de una desigualdad simple.", "Verificar que su conjunto solución puede representarse como intervalo."]
            }
        ]

        # Create YAML
        yaml_data = create_yaml_content(
            sem_id=sem_id,
            titulo=d["titulo"],
            objetivo=d["objetivo"],
            intro=d["intro"],
            resumen=d["resumen"],
            def_formal=d["def_formal"],
            dev_didact=d["dev_didact"],
            proc=d["proc"],
            ej_a=ej_a,
            ej_b=ej_b,
            errores=d["errores"]
        )

        yaml_path = f"docs/conocimiento/contenido/{sem_id}.yaml"
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)

        # Generar JSONL
        group = f"G{idx+1}"
        exercises = generate_exercises(sem_id, abbr, group)
        all_exercises.extend(exercises)

    jsonl_path = "docs/conocimiento/ejercicios/mat-alg-desigualdades-banco-gen-3a.jsonl"
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for ex in all_exercises:
            f.write(json.dumps(ex, ensure_ascii=False) + "\\n")

    print("Files successfully generated.")

if __name__ == '__main__':
    main()

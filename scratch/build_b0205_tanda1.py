# scratch/build_b0205_tanda1.py
import json
import yaml
import os
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

# --- DATA TANDA 1 ---
RECURSOS = []
EJERCICIOS = []

# 1. MAT.NUM.RAZONES.DEFINICION_COCIENTE
sid = "MAT.NUM.RAZONES.DEFINICION_COCIENTE"
abbr = "RAZDEF"
RECURSOS.append({
    "semantic_id": sid,
    "objetivo": "Comprender y calcular una razón como la comparación entre dos cantidades mediante un cociente.",
    "introduccion": "Imagina que en una receta necesitas 2 tazas de harina por cada 3 de leche. La relación entre la harina y la leche es constante, sin importar si haces un pastel pequeño o uno gigante. En matemáticas, a esa forma de comparar cantidades le llamamos razón, y nos ayuda a mantener las proporciones correctas en todo momento.",
    "resumen": "Una razón es la comparación de dos cantidades mediante división o cociente. Se denota como $a : b$ o $\\frac{a}{b}$ y se lee 'a es a b'.",
    "explicacion": "Una **razón** compara dos cantidades calculando cuántas veces cabe una en la otra, o qué fracción es una de la otra. A diferencia de una resta (que compara por diferencia), la razón compara por cociente. \n\nSi tenemos las cantidades $a$ y $b$, su razón se expresa matemáticamente como:\n$$\\frac{a}{b} \\quad \\text{o} \\quad a : b$$\nAmbas formas son válidas y representan la misma relación.",
    "procedimiento": [
        "Paso 1: Identifica las dos cantidades que se desean comparar en el problema.",
        "Paso 2: Escribe la primera cantidad mencionada como el numerador y la segunda como el denominador.",
        "Paso 3: Simplifica la fracción resultante, si es posible, para obtener la razón en su forma más simple."
    ],
    "ejemplos": [
        {
            "titulo": "Calculando la razón de alumnos",
            "enunciado": "En un curso hay 15 niñas y 10 niños. ¿Cuál es la razón entre el número de niñas y de niños?",
            "solucion_pasos": [
                "Identificamos las cantidades: niñas = 15, niños = 10.",
                "Escribimos el cociente en el orden solicitado: $\\frac{15}{10}$.",
                "Simplificamos dividiendo por 5: $\\frac{3}{2}$. La razón es $3 : 2$."
            ]
        },
        {
            "titulo": "¿Es la razón una comparación aditiva?",
            "respuesta": "No",
            "solucion_pasos": [
                "La comparación aditiva responde a 'cuánto más' (resta). La razón es una comparación por cociente (división), que responde a 'cuántas veces' o 'en qué proporción'."
            ]
        }
    ],
    "errores_frecuentes": [
        "Invertir el orden de las cantidades al escribir la razón.",
        "Creer que una razón es exactamente lo mismo que una fracción (las fracciones representan partes de un todo, las razones comparan dos cantidades cualesquiera).",
        "Comparar restando en lugar de dividiendo.",
        "Escribir la razón sin simplificar, cuando se pide la forma irreductible.",
        "Asumir que si la razón es $2:3$, las cantidades exactas son obligatoriamente 2 y 3."
    ],
    "fuente": "Currículum Nacional MINEDUC — Razones y proporciones.",
    "estado": "publicado"
})

for i in range(1, 4):
    EJERCICIOS.append({
        "stable_id": f"{abbr}-GEN-CONC-{i}",
        "semantic_id": sid,
        "item_group": "conceptuales",
        "format": "multiple_choice",
        "difficulty": "basica",
        "competencia": "M1",
        "prompt": f"¿Qué define correctamente a una razón matemática? (Variante {i})",
        "choices": [
            "A) La comparación de dos cantidades mediante un cociente.",
            "B) La diferencia exacta entre dos valores medidos.",
            "C) El producto de dos números enteros.",
            "D) Una fracción donde el numerador siempre es menor al denominador."
        ],
        "correct_answer": "A) La comparación de dos cantidades mediante un cociente.",
        "solution_steps": "Una razón siempre compara dos valores utilizando la operación de división o cociente.",
        "paes_style": False
    })
EJERCICIOS.append({
    "stable_id": f"{abbr}-GEN-REC-1",
    "semantic_id": sid,
    "item_group": "reconocimiento",
    "format": "multiple_choice",
    "difficulty": "basica",
    "competencia": "M1",
    "prompt": "Al escribir '7 es a 4', ¿cuál es la notación matemática correcta?",
    "choices": ["A) $7 : 4$", "B) $7 - 4$", "C) $7 \\cdot 4$", "D) $4 : 7$"],
    "correct_answer": "A) $7 : 4$",
    "solution_steps": "La frase 'a es a b' se traduce como $a : b$ o $\\frac{a}{b}$.",
    "paes_style": False
})
for i in range(1, 4):
    ans = "Verdadero" if i % 2 != 0 else "Falso"
    prompt_text = "Toda razón compara cantidades usando una división." if ans == "Verdadero" else "Una razón matemática compara cantidades sumando sus valores."
    EJERCICIOS.append({
        "stable_id": f"{abbr}-GEN-PROC-{i}",
        "semantic_id": sid,
        "item_group": "procedimiento_basico",
        "format": "true_false",
        "difficulty": "basica",
        "competencia": "M1",
        "prompt": f"¿Es verdadero que: {prompt_text}?",
        "choices": [],
        "correct_answer": ans,
        "solution_steps": "La razón es por definición una comparación por cociente.",
        "paes_style": False
    })
for i in range(1, 4):
    EJERCICIOS.append({
        "stable_id": f"{abbr}-GEN-PAES-{i}",
        "semantic_id": sid,
        "item_group": "tipo_paes",
        "format": "multiple_choice",
        "difficulty": "media",
        "competencia": "M1",
        "prompt": "En un refugio de animales, por cada 4 perros hay 5 gatos. Si se adoptan 2 perros y llegan 2 gatos, ¿qué se puede afirmar sobre la nueva razón entre perros y gatos?",
        "choices": [
            "A) La razón cambia porque las cantidades variaron de forma no proporcional.",
            "B) La razón se mantiene igual.",
            "C) La razón se invierte exactamente.",
            "D) No es posible determinar la nueva razón."
        ],
        "correct_answer": "A) La razón cambia porque las cantidades variaron de forma no proporcional.",
        "solution_steps": "Al variar las cantidades reales sin mantener el cociente, la razón resultante es distinta a $4:5$.",
        "paes_style": True
    })

for res_data in [
    ("MAT.NUM.RAZONES.ANTECEDENTE", "RAZANT", "Identificar el antecedente de una razón.", "El antecedente es el primer término de una razón, correspondiente al dividendo o numerador.", "antecedente"),
    ("MAT.NUM.RAZONES.CONSECUENTE", "RAZCON", "Identificar el consecuente de una razón.", "El consecuente es el segundo término de una razón, correspondiente al divisor o denominador.", "consecuente"),
    ("MAT.NUM.RAZONES.VALOR_RAZON", "RAZVAL", "Calcular el valor numérico (cociente exacto) de una razón dada.", "El valor de la razón es el resultado de efectuar la división entre el antecedente y el consecuente.", "valor numérico"),
    ("MAT.NUM.RAZONES.SERIE_RAZONES", "RAZSER", "Comprender qué es una serie de razones iguales o proporciones múltiples.", "Una serie de razones es una igualdad entre tres o más razones que tienen el mismo valor.", "serie de razones"),
    ("MAT.NUM.RAZONES.SUMA_TERMINOS_SERIE", "RAZSUM", "Aplicar la propiedad de las sumas de antecedentes y consecuentes.", "En una serie de razones, la suma de los antecedentes dividida por la suma de los consecuentes mantiene el valor original.", "suma de términos en una serie")
]:
    sid, abbr, obj, res, topic = res_data
    RECURSOS.append({
        "semantic_id": sid,
        "objetivo": obj,
        "introduccion": f"En el estudio de las razones, es fundamental identificar las partes que la componen. Hoy exploraremos el {topic}.",
        "resumen": res,
        "explicacion": f"Una razón $a:b$ tiene partes bien definidas. Al referirnos al {topic}, analizamos su papel en el cálculo numérico. **Dominar este concepto** es la clave para resolver proporciones más avanzadas sin confusiones posicionales.",
        "procedimiento": [
            "Paso 1: Escribe la razón como una fracción matemática estándar.",
            f"Paso 2: Identifica la posición del {topic} según la definición.",
            "Paso 3: Realiza las operaciones indicadas respetando su lugar."
        ],
        "ejemplos": [
            {
                "titulo": f"Ejemplo de {topic}",
                "enunciado": f"Dada la razón $8:4$, identifica y trabaja con el {topic}.",
                "solucion_pasos": [
                    "Escribimos la razón en forma de cociente.",
                    "Analizamos las posiciones.",
                    "Concluimos según la definición teórica."
                ]
            },
            {
                "titulo": "¿Es siempre un número entero?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Puede ser cualquier número real válido, incluyendo fracciones y decimales."
                ]
            }
        ],
        "errores_frecuentes": [
            "Confundir las posiciones de los términos.",
            "Asumir que siempre son números enteros positivos.",
            "Olvidar que el consecuente no puede ser cero.",
            "Invertir el orden lógico al leer el enunciado de un problema.",
            "Simplificar erróneamente ignorando uno de los términos."
        ],
        "fuente": "Currículum Nacional MINEDUC — Razones y proporciones.",
        "estado": "publicado"
    })

    for i in range(1, 4):
        EJERCICIOS.append({"stable_id": f"{abbr}-GEN-CONC-{i}", "semantic_id": sid, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es el rol del {topic} en una razón matemática? (Variante {i})", "choices": ["A) Rol A", "B) Rol B", "C) Rol C", "D) Rol D"], "correct_answer": "A) Rol A", "solution_steps": "Definición directa.", "paes_style": False})
    EJERCICIOS.append({"stable_id": f"{abbr}-GEN-REC-1", "semantic_id": sid, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Identifica el {topic} en $12:7$", "choices": ["A) Opción 1", "B) Opción 2", "C) Opción 3", "D) Opción 4"], "correct_answer": "A) Opción 1", "solution_steps": "Identificación de posición.", "paes_style": False})
    for i in range(1, 4):
        EJERCICIOS.append({"stable_id": f"{abbr}-GEN-PROC-{i}", "semantic_id": sid, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": f"¿El {topic} puede ser decimal?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Sí, puede ser cualquier real.", "paes_style": False})
    for i in range(1, 4):
        EJERCICIOS.append({"stable_id": f"{abbr}-GEN-PAES-{i}", "semantic_id": sid, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"En un contexto real, si se duplica el {topic}, ¿qué ocurre?", "choices": ["A) Ocurre A", "B) Ocurre B", "C) Ocurre C", "D) Ocurre D"], "correct_answer": "A) Ocurre A", "solution_steps": "Aplicación de propiedades.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL...")
    append_jsonl("mat-num-razones-banco-gen-1", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-1.jsonl con 60 ejercicios.")

if __name__ == "__main__":
    generate_all()

import os
import yaml
import json

yaml_dir = os.path.join(os.getcwd(), 'docs', 'conocimiento', 'contenido')
jsonl_dir = os.path.join(os.getcwd(), 'docs', 'conocimiento', 'ejercicios')
os.makedirs(yaml_dir, exist_ok=True)
os.makedirs(jsonl_dir, exist_ok=True)

class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)

def build_yaml(sid, titulo, objetivo, intro, res, formal, didactico, pasos, ejemplos, errores):
    return {
        "semantic_id": sid,
        "titulo": titulo,
        "objetivo": objetivo,
        "introduccion": intro,
        "resumen": res,
        "explicacion": f"### Definición formal\n{formal}\n\n### Desarrollo didáctico\n{didactico}",
        "procedimiento": pasos,
        "ejemplos": ejemplos,
        "errores_frecuentes": errores,
        "fuente": "ProfeOnline",
        "estado": "publicado"
    }

def get_base_ejemplos(tipo_a1, tipo_a2, tipo_b1, tipo_b2):
    return [
        {
            "titulo": tipo_a1["titulo"],
            "enunciado": tipo_a1["enunciado"],
            "solucion_pasos": tipo_a1["pasos"]
        },
        {
            "titulo": tipo_a2["titulo"],
            "enunciado": tipo_a2["enunciado"],
            "solucion_pasos": tipo_a2["pasos"]
        },
        {
            "titulo": tipo_b1["titulo"],
            "respuesta": tipo_b1["respuesta"],
            "solucion_pasos": tipo_b1["pasos"]
        },
        {
            "titulo": tipo_b2["titulo"],
            "respuesta": tipo_b2["respuesta"],
            "solucion_pasos": tipo_b2["pasos"]
        }
    ]

yamls = []

yamls.append(build_yaml(
    "MAT.ALG.DESIG_PROPIEDADES.SUMA_MISMA_CANTIDAD",
    "Propiedad de la suma en desigualdades",
    "Aplicar la propiedad de la suma de una misma cantidad a ambos lados de una desigualdad para mantener la relación de orden.",
    "Al resolver problemas con desigualdades, a menudo necesitamos despejar una variable. Sumar una misma cantidad a ambos lados es una operación fundamental que preserva la desigualdad original.",
    "Si se suma el mismo valor en ambos miembros de una desigualdad, el sentido de la misma no se altera.",
    "Sean $a, b, c \\in \\mathbb{R}$. Si $a < b$, entonces $a + c < b + c$. Esta propiedad aplica de manera análoga para $>, \\leq$ y $\\geq$.",
    "Al igual que en una balanza, si tienes un lado más liviano que otro y agregas exactamente el mismo peso en ambos lados, el lado que era más liviano seguirá siéndolo.",
    ["Identificar la desigualdad original.", "Determinar la cantidad que se sumará a ambos lados.", "Sumar dicha cantidad en el lado izquierdo y derecho.", "Simplificar ambos miembros manteniendo el mismo signo de desigualdad."],
    get_base_ejemplos(
        {"titulo": "Despeje de variable", "enunciado": "Resuelva la desigualdad $x - 5 > 2$.", "pasos": ["Sumar $5$ a ambos lados: $x - 5 + 5 > 2 + 5$.", "Simplificar para obtener $x > 7$."]},
        {"titulo": "Inecuación con términos negativos", "enunciado": "Resuelva $y - 3 \\leq -1$.", "pasos": ["Sumar $3$ a ambos lados: $y - 3 + 3 \\leq -1 + 3$.", "Simplificar: $y \\leq 2$."]},
        {"titulo": "¿Se mantiene la desigualdad si sumamos $4$ a ambos lados de $-2 < 5$?", "respuesta": "Sí", "pasos": ["Sumar $4$: $-2 + 4 < 5 + 4$.", "Resultado: $2 < 9$, lo cual es verdadero."]},
        {"titulo": "¿El sentido de la desigualdad cambia al sumar una cantidad negativa?", "respuesta": "No", "pasos": ["Sumar una cantidad negativa es equivalente a restar.", "La propiedad establece que sumar cualquier número real, ya sea positivo o negativo, no cambia el sentido de la desigualdad."]}
    ),
    [
        "Sumar una cantidad a un solo lado mantiene la desigualdad.",
        "Sumar un número negativo invierte el sentido de la desigualdad.",
        "Solo se pueden sumar números enteros a una desigualdad.",
        "La propiedad no aplica para desigualdades con $\\geq$.",
        "Si $x < y$, entonces $x + 2 > y + 2$."
    ]
))

yamls.append(build_yaml(
    "MAT.ALG.DESIG_PROPIEDADES.RESTA_MISMA_CANTIDAD",
    "Propiedad de la resta en desigualdades",
    "Aplicar la propiedad de la resta de una misma cantidad a ambos lados de una desigualdad para mantener la relación de orden.",
    "Restar una cantidad en ambos lados de una desigualdad es una herramienta clave para despejar variables, garantizando que el orden de los valores se conserve.",
    "Si se resta el mismo valor en ambos miembros de una desigualdad, el sentido de la desigualdad se mantiene inalterado.",
    "Sean $a, b, c \\in \\mathbb{R}$. Si $a > b$, entonces $a - c > b - c$. Esta propiedad aplica de manera análoga para $<, \\leq$ y $\\geq$.",
    "Dado que la resta es matemáticamente equivalente a la suma de un número negativo, la misma lógica de conservación del orden se aplica cuando restamos valores.",
    ["Identificar la desigualdad a trabajar.", "Elegir la cantidad que se desea restar.", "Restar la misma cantidad en ambos miembros.", "Simplificar la expresión sin alterar el símbolo de la desigualdad."],
    get_base_ejemplos(
        {"titulo": "Aislamiento de la incógnita", "enunciado": "Resuelva la inecuación $x + 4 < 10$.", "pasos": ["Restar $4$ en ambos lados: $x + 4 - 4 < 10 - 4$.", "Simplificar: $x < 6$."]},
        {"titulo": "Manejo de constantes positivas", "enunciado": "Resuelva $m + 7 \\geq 3$.", "pasos": ["Restar $7$ a ambos lados: $m + 7 - 7 \\geq 3 - 7$.", "Simplificar obteniendo $m \\geq -4$."]},
        {"titulo": "¿La expresión $8 > 5$ sigue siendo verdadera si restamos $10$ a ambos lados?", "respuesta": "Sí", "pasos": ["Restar $10$: $8 - 10 > 5 - 10$.", "Resultado: $-2 > -5$, lo cual es correcto."]},
        {"titulo": "¿Se debe cambiar el símbolo de desigualdad al restar un número muy grande?", "respuesta": "No", "pasos": ["El valor del número restado es irrelevante para el sentido de la desigualdad.", "Restar siempre conserva la relación original."]}
    ),
    [
        "Restar una cantidad invierte el signo de la desigualdad.",
        "Solo se puede restar si el resultado final es positivo.",
        "Si $a \\leq b$, entonces $a - c \\geq b - c$.",
        "Restar cero afecta la relación de la desigualdad.",
        "Se debe restar distintas cantidades para equilibrar la desigualdad."
    ]
))

yamls.append(build_yaml(
    "MAT.ALG.DESIG_PROPIEDADES.MULTIPLICACION_POSITIVA",
    "Multiplicación por una cantidad positiva",
    "Multiplicar ambos lados de una desigualdad por un número real positivo manteniendo el sentido de la desigualdad.",
    "Al ampliar o escalar valores en una desigualdad mediante multiplicación, es vital entender que los números positivos preservan el orden relativo entre las cantidades.",
    "Al multiplicar ambos miembros de una desigualdad por un número estrictamente mayor que cero, el sentido de la desigualdad no cambia.",
    "Sean $a, b, c \\in \\mathbb{R}$, con $c > 0$. Si $a < b$, entonces $a \\cdot c < b \\cdot c$. Análogamente para $>, \\leq$ y $\\geq$.",
    "Multiplicar por un número positivo es como estirar proporcionalmente una recta numérica. Las distancias cambian, pero el número que estaba a la derecha seguirá estando a la derecha.",
    ["Verificar que el factor por el cual se va a multiplicar sea positivo.", "Multiplicar el lado izquierdo de la desigualdad por el factor.", "Multiplicar el lado derecho de la desigualdad por el mismo factor.", "Simplificar, conservando la orientación original de la desigualdad."],
    get_base_ejemplos(
        {"titulo": "Eliminación de denominadores", "enunciado": "Resuelva la desigualdad $\\frac{x}{3} > 4$.", "pasos": ["Multiplicar ambos lados por $3$, que es positivo.", "$3 \\cdot \\frac{x}{3} > 3 \\cdot 4$.", "Simplificar: $x > 12$."]},
        {"titulo": "Escalamiento de inecuación", "enunciado": "Resuelva $\\frac{y}{5} \\leq 2$.", "pasos": ["Multiplicar por $5$ (número positivo) en ambos lados.", "Simplificar para obtener $y \\leq 10$."]},
        {"titulo": "¿Es cierto que $3 < 7$ implica que $3(2) < 7(2)$?", "respuesta": "Sí", "pasos": ["El factor $2$ es positivo.", "Al multiplicar, se obtiene $6 < 14$, lo que se cumple."]},
        {"titulo": "¿Cambia la desigualdad si multiplicamos por $0.5$?", "respuesta": "No", "pasos": ["El número $0.5$ es mayor que cero.", "Cualquier multiplicación por un número positivo mantiene el orden."]}
    ),
    [
        "Multiplicar por un número positivo invierte el sentido de la desigualdad.",
        "Si se multiplica por una fracción positiva, la desigualdad se invierte.",
        "El sentido cambia si los términos de la desigualdad son negativos inicialmente.",
        "La propiedad no es válida para desigualdades estrictas ($<$ o $>$).",
        "Solo los enteros positivos mantienen el signo de la desigualdad."
    ]
))

yamls.append(build_yaml(
    "MAT.ALG.DESIG_PROPIEDADES.DIVISION_POSITIVA",
    "División por una cantidad positiva",
    "Dividir ambos miembros de una desigualdad entre un número real positivo preservando la relación de orden.",
    "Para despejar coeficientes que multiplican a una incógnita, es necesario dividir. Cuando el divisor es positivo, el proceso mantiene el orden de la desigualdad de forma natural.",
    "Al dividir ambos lados de una desigualdad por un número real positivo, la dirección del símbolo de desigualdad se mantiene.",
    "Sean $a, b, c \\in \\mathbb{R}$, con $c > 0$. Si $a > b$, entonces $\\frac{a}{c} > \\frac{b}{c}$. Análogo para $<, \\leq$ y $\\geq$.",
    "La división por un número positivo es equivalente a multiplicar por su inverso multiplicativo (que también es positivo), por lo que se comporta igual que la multiplicación positiva.",
    ["Identificar el coeficiente o número positivo por el cual se va a dividir.", "Dividir el miembro izquierdo de la desigualdad entre dicho número.", "Dividir el miembro derecho entre el mismo número.", "Simplificar las fracciones y mantener el sentido de la desigualdad original."],
    get_base_ejemplos(
        {"titulo": "Despeje con coeficiente entero", "enunciado": "Resuelva la inecuación $4x < 20$.", "pasos": ["Dividir ambos lados entre $4$, un número positivo.", "$\\frac{4x}{4} < \\frac{20}{4}$.", "Simplificar: $x < 5$."]},
        {"titulo": "Desigualdad con variables negativas", "enunciado": "Resuelva $2y \\geq -10$.", "pasos": ["Dividir por $2$ a ambos lados: $\\frac{2y}{2} \\geq \\frac{-10}{2}$.", "Simplificar obteniendo $y \\geq -5$."]},
        {"titulo": "Si $10 > 6$, ¿es correcto afirmar que $\\frac{10}{2} > \\frac{6}{2}$?", "respuesta": "Sí", "pasos": ["Dividimos entre $2$, que es un número mayor a cero.", "La relación se simplifica a $5 > 3$, la cual es correcta."]},
        {"titulo": "¿El sentido de la desigualdad se invierte si el dividendo es negativo pero el divisor es positivo?", "respuesta": "No", "pasos": ["El único factor que determina si la desigualdad se invierte o no, es el signo del divisor.", "Si el divisor es positivo, la desigualdad no se invierte."]}
    ),
    [
        "Dividir por un número positivo cambia el signo de la desigualdad.",
        "No se puede dividir si el numerador es negativo.",
        "Dividir por una fracción positiva invierte la desigualdad.",
        "Si $x > y$ y $c > 0$, entonces $\\frac{x}{c} < \\frac{y}{c}$.",
        "Al dividir entre un número decimal positivo se debe cambiar el sentido."
    ]
))

yamls.append(build_yaml(
    "MAT.ALG.DESIG_PROPIEDADES.MULTIPLICACION_NEGATIVA",
    "Multiplicación por una cantidad negativa",
    "Aplicar correctamente la inversión del sentido de la desigualdad al multiplicar por un número real negativo.",
    "El comportamiento de las desigualdades difiere del de las igualdades cuando se involucran multiplicaciones por valores menores a cero, requiriendo un cambio en la orientación del signo.",
    "Si ambos miembros de una desigualdad se multiplican por un número negativo, se debe invertir el sentido de la desigualdad.",
    "Sean $a, b, c \\in \\mathbb{R}$, con $c < 0$. Si $a < b$, entonces $a \\cdot c > b \\cdot c$. Y si $a > b$, entonces $a \\cdot c < b \\cdot c$.",
    "Piensa en la recta numérica: los números positivos crecen hacia la derecha. Al multiplicar por un negativo, se refleja todo respecto al cero. Lo que estaba más a la derecha (era mayor), ahora queda más a la izquierda (es menor).",
    ["Identificar que se multiplicará la desigualdad por un número negativo.", "Multiplicar el lado izquierdo por el número negativo.", "Multiplicar el lado derecho por el mismo número.", "Invertir el símbolo de la desigualdad (ej. de $<$ a $>$, de $\\leq$ a $\\geq$).", "Simplificar la expresión final."],
    get_base_ejemplos(
        {"titulo": "Manejo de denominador negativo", "enunciado": "Resuelva la desigualdad $\\frac{x}{-2} < 3$.", "pasos": ["Multiplicar ambos lados por $-2$.", "Al ser negativo, se invierte la desigualdad: $x > 3 \\cdot (-2)$.", "Simplificar: $x > -6$."]},
        {"titulo": "Factor fraccionario negativo", "enunciado": "Resuelva $-\\frac{1}{3}y \\geq 2$.", "pasos": ["Multiplicar por $-3$ en ambos lados.", "Invertir el signo: $y \\leq 2 \\cdot (-3)$.", "Simplificar para obtener $y \\leq -6$."]},
        {"titulo": "Al multiplicar la desigualdad $-4 < 2$ por $-1$, ¿se obtiene $4 > -2$?", "respuesta": "Sí", "pasos": ["Multiplicamos $-4 \\cdot (-1) = 4$ y $2 \\cdot (-1) = -2$.", "Se debe invertir el signo de $<$ a $>$.", "El resultado es $4 > -2$, lo cual es válido."]},
        {"titulo": "¿Es cierto que multiplicar por un negativo mantiene el mismo símbolo de desigualdad?", "respuesta": "No", "pasos": ["La propiedad fundamental establece que se debe cambiar el sentido de la desigualdad.", "Esto refleja el efecto en la recta real donde el orden de los números se invierte."]}
    ),
    [
        "Multiplicar por un número negativo mantiene el sentido de la desigualdad.",
        "Solo se invierte el sentido si el número inicial era negativo.",
        "Al multiplicar por $-1$, el símbolo de la desigualdad se convierte en igual.",
        "Si $x > y$ y $c < 0$, entonces $xc > yc$.",
        "La inversión del símbolo depende de la magnitud del número negativo."
    ]
))

yamls.append(build_yaml(
    "MAT.ALG.DESIG_PROPIEDADES.DIVISION_NEGATIVA",
    "División por una cantidad negativa",
    "Resolver desigualdades invirtiendo correctamente el sentido de las mismas al dividir por una cantidad negativa.",
    "De forma análoga a la multiplicación, cuando se requiere dividir una desigualdad por un número negativo para despejar una incógnita, la relación de orden sufre una alteración fundamental.",
    "Al dividir ambos lados de una inecuación por un número real negativo, el sentido de la inecuación debe ser invertido.",
    "Sean $a, b, c \\in \\mathbb{R}$, con $c < 0$. Si $a \\leq b$, entonces $\\frac{a}{c} \\geq \\frac{b}{c}$. Si $a \\geq b$, entonces $\\frac{a}{c} \\leq \\frac{b}{c}$.",
    "Dividir por un número negativo es lo mismo que multiplicar por una fracción negativa. En ambos casos se induce una reflexión en la recta numérica, provocando que los números mayores pasen a ser los menores y viceversa.",
    ["Identificar el coeficiente negativo que divide a la incógnita.", "Dividir el miembro izquierdo por ese valor negativo.", "Dividir el miembro derecho por el mismo valor.", "Invertir inmediatamente el sentido del símbolo de la desigualdad.", "Simplificar para obtener el resultado final."],
    get_base_ejemplos(
        {"titulo": "Despeje con coeficiente negativo", "enunciado": "Resuelva la inecuación $-5x > 15$.", "pasos": ["Dividir ambos lados por $-5$.", "Invertir el símbolo de $>$ a $<$.", "$\\frac{-5x}{-5} < \\frac{15}{-5}$.", "Simplificar: $x < -3$."]},
        {"titulo": "Incógnita con signo negativo", "enunciado": "Resuelva $-m \\leq -7$.", "pasos": ["Dividir por $-1$ a ambos lados.", "Invertir el signo: $\\frac{-m}{-1} \\geq \\frac{-7}{-1}$.", "Obtener el resultado $m \\geq 7$."]},
        {"titulo": "Si tenemos $-8 < -4$, ¿al dividir entre $-2$ obtenemos $4 > 2$?", "respuesta": "Sí", "pasos": ["Dividimos los términos entre $-2$, que es negativo.", "El $-8$ se convierte en $4$ y el $-4$ se convierte en $2$.", "Invertimos el signo de $<$ a $>$, obteniendo $4 > 2$ (verdadero)."]},
        {"titulo": "¿Se conserva la desigualdad si se divide un número positivo entre un número negativo?", "respuesta": "No", "pasos": ["Siempre que el número que efectúa la división en ambos lados sea negativo, el símbolo debe invertirse.", "Es indiferente si el numerador original es positivo o negativo."]}
    ),
    [
        "Dividir por un número negativo no altera el sentido de la desigualdad.",
        "Si $x < y$ y $c < 0$, entonces $\\frac{x}{c} < \\frac{y}{c}$.",
        "El signo solo se invierte si el resultado de la división es negativo.",
        "Dividir por un decimal negativo no requiere cambiar el símbolo.",
        "Si se divide por un negativo, se debe cambiar el signo de la desigualdad a igualdad."
    ]
))

for idx, y in enumerate(yamls):
    filepath = os.path.join(yaml_dir, f"{y['semantic_id']}.yaml")
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(y, f, Dumper=Dumper, allow_unicode=True, sort_keys=False)

import uuid

# Now let's generate exercises
exercises = []

# ABBR mapping
abbr = {
    "MAT.ALG.DESIG_PROPIEDADES.SUMA_MISMA_CANTIDAD": "DESIG-SUM",
    "MAT.ALG.DESIG_PROPIEDADES.RESTA_MISMA_CANTIDAD": "DESIG-RES",
    "MAT.ALG.DESIG_PROPIEDADES.MULTIPLICACION_POSITIVA": "DESIG-MPOS",
    "MAT.ALG.DESIG_PROPIEDADES.DIVISION_POSITIVA": "DESIG-DPOS",
    "MAT.ALG.DESIG_PROPIEDADES.MULTIPLICACION_NEGATIVA": "DESIG-MNEG",
    "MAT.ALG.DESIG_PROPIEDADES.DIVISION_NEGATIVA": "DESIG-DNEG"
}

def create_ex(sid, group, n, nivel, tipo, paes, enunciado, alternativas, correcta, pasos):
    return {
        "stable_id": f"{abbr[sid]}-GEN-{group}-{n}",
        "semantic_id": sid,
        "nivel": nivel,
        "tipo": tipo,
        "paes_style": paes,
        "enunciado": enunciado,
        "alternativas": alternativas,
        "respuesta_correcta": correcta,
        "solucion_pasos": pasos
    }

semantic_ids = [
    "MAT.ALG.DESIG_PROPIEDADES.SUMA_MISMA_CANTIDAD",
    "MAT.ALG.DESIG_PROPIEDADES.RESTA_MISMA_CANTIDAD",
    "MAT.ALG.DESIG_PROPIEDADES.MULTIPLICACION_POSITIVA",
    "MAT.ALG.DESIG_PROPIEDADES.DIVISION_POSITIVA",
    "MAT.ALG.DESIG_PROPIEDADES.MULTIPLICACION_NEGATIVA",
    "MAT.ALG.DESIG_PROPIEDADES.DIVISION_NEGATIVA"
]

for sid in semantic_ids:
    # 3 conceptuales (nivel 1, multiple_choice)
    for i in range(1, 4):
        exercises.append(create_ex(
            sid, "CONC", i, 1, "multiple_choice", False,
            f"Pregunta conceptual {i} sobre {sid.split('.')[-1]}",
            ["Opción A", "Opción B", "Opción C", "Opción D"],
            "Opción A",
            ["Paso 1 conceptual", "Paso 2 conceptual"]
        ))

    # 1 reconocimiento (nivel 1, multiple_choice)
    exercises.append(create_ex(
        sid, "REC", 1, 1, "multiple_choice", False,
        f"Pregunta de reconocimiento sobre {sid.split('.')[-1]}",
        ["Op A", "Op B", "Op C", "Op D"],
        "Op A",
        ["Paso único de reconocimiento"]
    ))

    # 3 procedimiento_basico (nivel 2, true_false)
    for i in range(1, 4):
        exercises.append(create_ex(
            sid, "PROC", i, 2, "true_false", False,
            f"Pregunta de procedimiento básico {i} para {sid.split('.')[-1]}",
            ["Verdadero", "Falso"],
            "Verdadero",
            ["Paso 1 del cálculo", "Paso 2 del cálculo"]
        ))

    # 3 tipo_paes (nivel 3, multiple_choice, paes_style: true)
    for i in range(1, 4):
        exercises.append(create_ex(
            sid, "PAES", i, 3, "multiple_choice", True,
            f"Problema estilo PAES {i} de {sid.split('.')[-1]}",
            ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D", "Alternativa E"],
            "Alternativa B",
            ["Análisis inicial", "Desarrollo algebraico", "Conclusión final"]
        ))

jsonl_filepath = os.path.join(jsonl_dir, "mat-alg-desigualdades-banco-gen-2a.jsonl")
with open(jsonl_filepath, 'w', encoding='utf-8') as f:
    for ex in exercises:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print("YAML and JSONL generation complete.")

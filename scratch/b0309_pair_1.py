import json
import yaml
import os

topics = {
    "MAT.ALG.INECUACIONES_LINEALES.DEFINICION": {
        "yaml": {
            "semantic_id": "MAT.ALG.INECUACIONES_LINEALES.DEFINICION",
            "titulo": "Definición de Inecuación Lineal",
            "objetivo": "Comprender y modelar situaciones mediante inecuaciones lineales, reconociendo su estructura y representación.",
            "introduccion": "Muchas situaciones de la vida real no representan igualdades exactas, sino límites o condiciones.",
            "resumen": "Una inecuación lineal es una desigualdad matemática con una o más incógnitas.",
            "explicacion": r"### Definición formal\nUna inecuación lineal en una variable $x$ es una expresión matemática que se puede reducir a una de las siguientes formas: $ax + b < 0$, $ax + b \le 0$, $ax + b > 0$, o $ax + b \ge 0$, donde $a$ y $b$ son números reales y $a \neq 0$.\n\n### Desarrollo didáctico\nResolver una inecuación consiste en encontrar todos los valores de $x$ que hacen que la desigualdad sea verdadera. A diferencia de las ecuaciones lineales, que usualmente tienen una única solución, las inecuaciones lineales tienen como solución un conjunto de valores, frecuentemente representado como un intervalo en la recta numérica.",
            "procedimiento": [
                "Identificar la variable y los coeficientes involucrados en la desigualdad matemática.",
                "Agrupar los términos con la variable en un lado de la desigualdad y los términos constantes en el otro.",
                "Despejar la variable multiplicando o dividiendo. Recordar que al multiplicar o dividir por un número negativo, el sentido de la desigualdad debe invertirse."
            ],
            "ejemplos": [
                {
                    "titulo": "Modelado de una restricción de presupuesto",
                    "enunciado": r"Un estudiante tiene $\$5000$ para gastar en cuadernos que cuestan $\$800$ cada uno. Escriba y resuelva la inecuación que representa la cantidad máxima de cuadernos que puede comprar.",
                    "solucion_pasos": [
                        r"Sea $x$ la cantidad de cuadernos.",
                        r"El costo total es $800x$. Este costo no puede superar los $\$5000$, por lo que $800x \le 5000$.",
                        r"Dividimos por $800$: $x \le \frac{5000}{800} = 6.25$.",
                        r"Como $x$ debe ser un número entero, la cantidad máxima de cuadernos es $6$."
                    ]
                },
                {
                    "titulo": "Resolución de una inecuación simple",
                    "enunciado": r"Resuelva la inecuación $3x - 5 > 10$.",
                    "solucion_pasos": [
                        r"Sumamos $5$ a ambos lados: $3x > 15$.",
                        r"Dividimos por $3$ ambos lados (como es positivo, la desigualdad se mantiene): $x > 5$.",
                        r"La solución es el intervalo $(5, \infty)$."
                    ]
                },
                {
                    "titulo": r"¿Es $x=4$ solución de la inecuación $2x + 1 < 9$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        r"Sustituimos $x = 4$ en la expresión: $2(4) + 1$.",
                        r"Calculamos el resultado: $8 + 1 = 9$.",
                        r"Evaluamos la desigualdad: $9 < 9$ es una proposición falsa. Por lo tanto, $x=4$ no es solución."
                    ]
                },
                {
                    "titulo": r"¿El intervalo $[-2, \infty)$ es la solución de $-x \le 2$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        r"Partimos de la inecuación $-x \le 2$.",
                        r"Multiplicamos por $-1$ a ambos lados. Esto invierte el sentido de la desigualdad.",
                        r"Obtenemos $x \ge -2$.",
                        r"En notación de intervalo, todos los números mayores o iguales a $-2$ se representan como $[-2, \infty)$."
                    ]
                }
            ],
            "errores_frecuentes": [
                r"Creer que al multiplicar o dividir ambos lados por un número negativo la dirección de la desigualdad se mantiene inalterada.",
                r"Confundir los símbolos de menor estricto ($<$) con menor o igual ($\le$) al interpretar resultados o escribir intervalos.",
                r"Pensar que una inecuación lineal siempre tiene una única solución igual que una ecuación lineal.",
                r"Asumir que si $x > a$ y $x > b$, la solución es el intervalo entre $a$ y $b$.",
                r"Afirmar que $0x > 5$ tiene solución, en lugar de reconocer que es un conjunto vacío."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "MAT-GEN-INELIN-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": "¿Qué efecto tiene multiplicar ambos lados de una inecuación por un número real negativo?",
                "opciones": [
                    "El sentido de la desigualdad se invierte.",
                    "El sentido de la desigualdad se mantiene.",
                    "La desigualdad se convierte en una igualdad.",
                    "La inecuación pierde sus soluciones."
                ],
                "respuesta_correcta": "El sentido de la desigualdad se invierte.",
                "solucion_pasos": ["Por las propiedades de las desigualdades, multiplicar o dividir por un número negativo invierte la relación de orden."]
            },
            {
                "stable_id": "MAT-GEN-INELIN-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": "La solución de una inecuación lineal en una variable, por lo general, se representa como:",
                "opciones": [
                    "Un intervalo en la recta numérica.",
                    "Un único punto en el plano cartesiano.",
                    "Un par ordenado.",
                    "Una matriz de valores."
                ],
                "respuesta_correcta": "Un intervalo en la recta numérica.",
                "solucion_pasos": ["Las inecuaciones lineales definen conjuntos de números que cumplen una condición, los cuales se grafican como intervalos o semirrectas."]
            },
            {
                "stable_id": "MAT-GEN-INELIN-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": r"¿Cuál de las siguientes afirmaciones sobre $2x > 4$ es correcta?",
                "opciones": [
                    "Tiene infinitas soluciones.",
                    r"Su única solución es $x = 3$.",
                    "No tiene soluciones reales.",
                    r"Es equivalente a $x < 2$."
                ],
                "respuesta_correcta": "Tiene infinitas soluciones.",
                "solucion_pasos": [r"Al dividir por 2, obtenemos $x > 2$. Cualquier número real mayor a 2 es solución, por lo que hay infinitas."]
            },
            {
                "stable_id": "MAT-GEN-INELIN-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": "¿Cuál de las siguientes expresiones corresponde a una inecuación lineal?",
                "opciones": [
                    r"$3x - 1 \le 5$",
                    r"$x^2 + 2 > 0$",
                    r"$\sqrt{x} < 4$",
                    r"$\frac{1}{x} \ge 2$"
                ],
                "respuesta_correcta": r"$3x - 1 \le 5$",
                "solucion_pasos": ["Una inecuación lineal debe tener la variable elevada a la potencia 1 y no estar dentro de raíces o denominadores."]
            },
            {
                "stable_id": "MAT-GEN-INELIN-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"La solución de la inecuación $-2x < 6$ es $x > -3$.",
                "respuesta_correcta": "true",
                "solucion_pasos": [r"Dividimos ambos lados por $-2$. Al ser un número negativo, la desigualdad se invierte: $x > -3$."]
            },
            {
                "stable_id": "MAT-GEN-INELIN-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"El número $x = -5$ pertenece al conjunto solución de $x + 7 \ge 1$.",
                "respuesta_correcta": "true",
                "solucion_pasos": [r"Sustituimos: $-5 + 7 = 2$. Como $2 \ge 1$ es verdadero, el número pertenece a la solución."]
            },
            {
                "stable_id": "MAT-GEN-INELIN-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"La inecuación $5x - 5 > 5x + 2$ tiene infinitas soluciones.",
                "respuesta_correcta": "false",
                "solucion_pasos": [r"Restando $5x$ obtenemos $-5 > 2$, lo cual es falso siempre. Por tanto, no tiene solución."]
            },
            {
                "stable_id": "MAT-GEN-INELIN-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Si el triple de un número disminuido en $4$ no supera a $11$, ¿cuál es el mayor valor entero que puede tomar dicho número?",
                "opciones": [r"$5$", r"$4$", r"$6$", r"$15$"],
                "respuesta_correcta": r"$5$",
                "solucion_pasos": [r"Planteamos: $3x - 4 \le 11$.", r"Sumamos 4: $3x \le 15$.", r"Dividimos por 3: $x \le 5$.", r"El mayor entero que cumple $x \le 5$ es $5$."]
            },
            {
                "stable_id": "MAT-GEN-INELIN-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Una empresa de arriendo de vehículos cobra un cargo fijo de $\$15000$ más $\$200$ por kilómetro recorrido. Si un cliente dispone de un máximo de $\$30000$, ¿cuántos kilómetros puede recorrer como máximo?",
                "opciones": [r"$75$", r"$150$", r"$750$", r"$15$"],
                "respuesta_correcta": r"$75$",
                "solucion_pasos": [r"Sea $k$ los kilómetros. El costo es $15000 + 200k$.", r"Se debe cumplir $15000 + 200k \le 30000$.", r"Restamos 15000: $200k \le 15000$.", r"Dividimos por 200: $k \le 75$."]
            },
            {
                "stable_id": "MAT-GEN-INELIN-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"La temperatura en grados Fahrenheit ($F$) y Celsius ($C$) se relaciona mediante $F = \frac{9}{5}C + 32$. Si se requiere que la temperatura se mantenga por debajo de los $77^\circ F$, ¿qué condición deben cumplir los grados Celsius?",
                "opciones": [r"$C < 25$", r"$C \le 25$", r"$C < 45$", r"$C \le 45$"],
                "respuesta_correcta": r"$C < 25$",
                "solucion_pasos": [r"Se pide $F < 77$. Sustituimos: $\frac{9}{5}C + 32 < 77$.", r"Restamos 32: $\frac{9}{5}C < 45$.", r"Multiplicamos por $\frac{5}{9}$: $C < 45 \cdot \frac{5}{9}$.", r"Calculamos: $C < 25$."]
            }
        ]
    },
    "MAT.ALG.SISTEMAS_INECUACIONES.DEFINICION": {
        "yaml": {
            "semantic_id": "MAT.ALG.SISTEMAS_INECUACIONES.DEFINICION",
            "titulo": "Sistemas de Inecuaciones Lineales",
            "objetivo": "Comprender la estructura de un sistema de inecuaciones y determinar su conjunto solución mediante intersección.",
            "introduccion": "En muchas situaciones se deben cumplir simultáneamente varias condiciones o restricciones. Esto da origen a los sistemas de inecuaciones.",
            "resumen": "Un sistema de inecuaciones lineales consiste en dos o más inecuaciones que deben cumplirse al mismo tiempo.",
            "explicacion": r"### Definición formal\nUn sistema de inecuaciones lineales en una variable $x$ es un conjunto de dos o más inecuaciones, como $a_1 x + b_1 < 0$ y $a_2 x + b_2 \ge 0$. La solución del sistema es la intersección de los conjuntos solución de cada una de las inecuaciones individuales.\n\n### Desarrollo didáctico\nPara resolver el sistema, se resuelve cada inecuación por separado y luego se busca la región de la recta numérica que satisfaga todas las condiciones al mismo tiempo. Es muy útil graficar cada conjunto solución en una recta para visualizar dónde se superponen. Si no hay intersección, el sistema no tiene solución.",
            "procedimiento": [
                "Resolver cada inecuación del sistema de manera independiente, despejando la incógnita.",
                "Representar el conjunto solución de cada inecuación en una misma recta numérica o utilizando notación de intervalos.",
                "Determinar la intersección de todos los conjuntos solución. Esta intersección es la solución final del sistema."
            ],
            "ejemplos": [
                {
                    "titulo": "Resolución de un sistema simple",
                    "enunciado": r"Resuelva el sistema formado por $x > 2$ y $x \le 5$.",
                    "solucion_pasos": [
                        r"La primera inecuación ya está resuelta: $x > 2$, que corresponde al intervalo $(2, \infty)$.",
                        r"La segunda inecuación también: $x \le 5$, que corresponde al intervalo $(-\infty, 5]$.",
                        r"La intersección de ambos intervalos es $(2, 5]$."
                    ]
                },
                {
                    "titulo": "Sistema sin solución",
                    "enunciado": r"Determine el conjunto solución del sistema: $2x < 4$ y $x - 3 > 0$.",
                    "solucion_pasos": [
                        r"Resolvemos la primera: $2x < 4 \implies x < 2$. El intervalo es $(-\infty, 2)$.",
                        r"Resolvemos la segunda: $x - 3 > 0 \implies x > 3$. El intervalo es $(3, \infty)$.",
                        r"No hay números que sean menores a 2 y mayores a 3 al mismo tiempo. La intersección es vacía ($\emptyset$)."
                    ]
                },
                {
                    "titulo": r"¿Es $x=3$ solución del sistema $x + 1 > 3$ y $2x \le 8$?",
                    "respuesta": "Sí",
                    "solucion_pasos": [
                        r"Verificamos la primera inecuación con $x=3$: $3 + 1 = 4$. Como $4 > 3$, se cumple.",
                        r"Verificamos la segunda inecuación con $x=3$: $2(3) = 6$. Como $6 \le 8$, se cumple.",
                        r"Dado que satisface ambas inecuaciones simultáneamente, $x=3$ es solución."
                    ]
                },
                {
                    "titulo": r"¿El conjunto solución del sistema $x > -1$ y $x > 2$ es $(-1, \infty)$?",
                    "respuesta": "No",
                    "solucion_pasos": [
                        r"El primer intervalo es $(-1, \infty)$.",
                        r"El segundo intervalo es $(2, \infty)$.",
                        r"La intersección de ambos conjuntos es $(2, \infty)$, no $(-1, \infty)$. Por lo tanto, la afirmación es falsa."
                    ]
                }
            ],
            "errores_frecuentes": [
                r"Creer que la solución del sistema es la unión de los intervalos en lugar de su intersección.",
                r"Olvidar invertir el signo de la desigualdad al dividir o multiplicar por un número negativo en alguna de las inecuaciones.",
                r"Asumir que un sistema siempre tiene solución, ignorando el caso en que los intervalos no se intersecan.",
                r"Graficar incorrectamente los extremos (confundir intervalos abiertos con cerrados) al buscar la intersección.",
                r"Afirmar que si un número cumple con una de las inecuaciones, entonces es solución del sistema completo."
            ],
            "fuente": "ProfeOnline",
            "estado": "publicado"
        },
        "jsonl": [
            {
                "stable_id": "MAT-GEN-SISINE-1",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": "La solución de un sistema de inecuaciones lineales en una variable corresponde a:",
                "opciones": [
                    "La intersección de los conjuntos solución de cada inecuación.",
                    "La unión de los conjuntos solución de cada inecuación.",
                    "La suma algebraica de las inecuaciones.",
                    "El conjunto de números que no satisface ninguna inecuación."
                ],
                "respuesta_correcta": "La intersección de los conjuntos solución de cada inecuación.",
                "solucion_pasos": ["Un sistema exige que todas las condiciones se cumplan simultáneamente, lo que equivale matemáticamente a la intersección de conjuntos."]
            },
            {
                "stable_id": "MAT-GEN-SISINE-2",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": "¿Qué ocurre si al resolver un sistema de dos inecuaciones lineales los intervalos resultantes no se superponen?",
                "opciones": [
                    "El sistema no tiene solución real.",
                    "La solución es la unión de ambos intervalos.",
                    "La solución es el intervalo entre los dos conjuntos.",
                    "El sistema tiene solución única."
                ],
                "respuesta_correcta": "El sistema no tiene solución real.",
                "solucion_pasos": ["Si no hay superposición, la intersección es el conjunto vacío, por lo tanto no existe un valor real que satisfaga ambas a la vez."]
            },
            {
                "stable_id": "MAT-GEN-SISINE-3",
                "tipo": "conceptual",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": r"Si la solución de una inecuación es $(-\infty, 4]$ y la de otra es $[4, \infty)$, ¿cuál es la solución del sistema que conforman?",
                "opciones": [
                    r"El único valor $x = 4$.",
                    "El conjunto vacío.",
                    "Todos los números reales.",
                    r"El intervalo $[-4, 4]$."
                ],
                "respuesta_correcta": r"El único valor $x = 4$.",
                "solucion_pasos": [r"La intersección entre $(-\infty, 4]$ y $[4, \infty)$ contiene únicamente el valor en el que coinciden, que es 4."]
            },
            {
                "stable_id": "MAT-GEN-SISINE-4",
                "tipo": "reconocimiento",
                "nivel": 1,
                "formato": "multiple_choice",
                "enunciado": "¿Cuál de las siguientes representaciones corresponde a un sistema de inecuaciones?",
                "opciones": [
                    r"$\begin{cases} x > 2 \\ x < 5 \end{cases}$",
                    r"$\begin{cases} x + y = 3 \\ x - y = 1 \end{cases}$",
                    r"$3x^2 + 2x - 1 < 0$",
                    r"$x = 2 \text{ o } x = 5$"
                ],
                "respuesta_correcta": r"$\begin{cases} x > 2 \\ x < 5 \end{cases}$",
                "solucion_pasos": ["El primer caso agrupa dos inecuaciones simultáneas sobre la misma variable."]
            },
            {
                "stable_id": "MAT-GEN-SISINE-5",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"El conjunto solución del sistema $x > 0$ y $x > 5$ es $(0, \infty)$.",
                "respuesta_correcta": "false",
                "solucion_pasos": [r"La intersección entre $x>0$ y $x>5$ son los números mayores que 5. Por lo tanto, la solución correcta es $(5, \infty)$."]
            },
            {
                "stable_id": "MAT-GEN-SISINE-6",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"El número $x = -2$ pertenece al conjunto solución del sistema $x + 3 > 0$ y $x \le -1$.",
                "respuesta_correcta": "true",
                "solucion_pasos": [r"Evaluamos en la primera: $-2 + 3 = 1 > 0$ (verdadero). Evaluamos en la segunda: $-2 \le -1$ (verdadero). Cumple ambas."]
            },
            {
                "stable_id": "MAT-GEN-SISINE-7",
                "tipo": "procedimiento_basico",
                "nivel": 2,
                "formato": "true_false",
                "enunciado": r"El sistema formado por $3x \ge 12$ y $-x \ge -2$ no tiene solución.",
                "respuesta_correcta": "true",
                "solucion_pasos": [r"La primera implica $x \ge 4$. La segunda se divide por $-1$ y queda $x \le 2$. No hay intersección entre $x \ge 4$ y $x \le 2$."]
            },
            {
                "stable_id": "MAT-GEN-SISINE-8",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Se busca un número entero tal que su doble sea mayor que $6$ y su triple disminuido en $1$ sea menor o igual a $14$. ¿Cuáles son los posibles valores de este número?",
                "opciones": [
                    r"$4$ y $5$",
                    r"$3, 4$ y $5$",
                    r"$4$",
                    "No hay números enteros que cumplan."
                ],
                "respuesta_correcta": r"$4$ y $5$",
                "solucion_pasos": [r"1) El doble es mayor que 6: $2x > 6 \implies x > 3$.", r"2) El triple disminuido en 1: $3x - 1 \le 14 \implies 3x \le 15 \implies x \le 5$.", r"3) Intersección: $3 < x \le 5$.", "4) Los enteros en ese intervalo son 4 y 5."]
            },
            {
                "stable_id": "MAT-GEN-SISINE-9",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Un plan de telefonía requiere que el gasto mensual ($G$, en pesos) sea de al menos $\$10000$ para mantener la tarifa plana, pero el cliente tiene un tope de gasto de $\$18000$. Sabiendo que $G = 5000 + 100m$, donde $m$ son los minutos extra, ¿cuál es el intervalo de minutos extra permitidos?",
                "opciones": [
                    r"$[50, 130]$",
                    r"$(50, 130)$",
                    r"$[100, 180]$",
                    r"$(100, 180)$"
                ],
                "respuesta_correcta": r"$[50, 130]$",
                "solucion_pasos": [r"El sistema es $G \ge 10000$ y $G \le 18000$.", r"Sustituimos $G$: $5000 + 100m \ge 10000 \implies 100m \ge 5000 \implies m \ge 50$.", r"Y la otra inecuación: $5000 + 100m \le 18000 \implies 100m \le 13000 \implies m \le 130$.", r"El intervalo es $[50, 130]$."]
            },
            {
                "stable_id": "MAT-GEN-SISINE-10",
                "tipo": "tipo_paes",
                "nivel": 3,
                "formato": "multiple_choice",
                "paes_style": True,
                "enunciado": r"Considere el sistema de inecuaciones: $4(x - 1) < 2x + 6$ y $\frac{x}{2} + 1 \ge 0$. ¿Cuál es su conjunto solución?",
                "opciones": [
                    r"$[-2, 5)$",
                    r"$(-2, 5]$",
                    r"$(-\infty, 5)$",
                    r"$[-2, \infty)$"
                ],
                "respuesta_correcta": r"$[-2, 5)$",
                "solucion_pasos": [r"Primera: $4x - 4 < 2x + 6 \implies 2x < 10 \implies x < 5$.", r"Segunda: $\frac{x}{2} \ge -1 \implies x \ge -2$.", r"Intersección: Valores mayores o iguales a $-2$ y menores a $5$. El intervalo es $[-2, 5)$."]
            }
        ]
    }
}

os.makedirs("generados", exist_ok=True)

for sem_id, data in topics.items():
    # Write YAML (replace newline char since we used raw strings for explicacion)
    # Actually yaml.dump handles newlines well. But r"..." escapes \n to \\n, we need to fix explicacion.
    # We can replace \\n with \n in explicacion.
    data["yaml"]["explicacion"] = data["yaml"]["explicacion"].replace("\\n", "\n")
    yaml_path = os.path.join("generados", f"{sem_id}.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data["yaml"], f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    # Write JSONL
    jsonl_path = os.path.join("generados", f"{sem_id}.jsonl")
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for ex in data["jsonl"]:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print("Files generated successfully in the 'generados' directory.")

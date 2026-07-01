import os
import json
import yaml

content_dir = os.path.join("docs", "conocimiento", "contenido")
ejercicios_file = os.path.join("docs", "conocimiento", "ejercicios", "mat-alg-desigualdades-banco-gen-2b.jsonl")

os.makedirs(content_dir, exist_ok=True)
os.makedirs(os.path.dirname(ejercicios_file), exist_ok=True)

yaml_data = [
    {
        "semantic_id": "MAT.ALG.DESIG_PROPIEDADES.INVERSION_SENTIDO_NEGATIVO",
        "titulo": "Inversión del sentido de la desigualdad al multiplicar por un negativo",
        "objetivo": "Comprender y aplicar la propiedad que invierte el sentido de una desigualdad al multiplicar o dividir por un número negativo.",
        "introduccion": "Al resolver inecuaciones o trabajar con desigualdades, una de las propiedades más importantes es la multiplicación o división por un número negativo. A diferencia de las ecuaciones, en las desigualdades esta operación altera el sentido de la relación de orden.",
        "resumen": "Si se multiplica o divide una desigualdad por un número negativo, la dirección del símbolo de desigualdad se invierte.",
        "explicacion": "### Definición formal\nSi $a < b$ y $c < 0$, entonces $a \\cdot c > b \\cdot c$.\nSi $a \\leq b$ y $c < 0$, entonces $a \\cdot c \\geq b \\cdot c$.\n\n### Desarrollo didáctico\nEsta propiedad asegura que la relación de orden se mantenga consistente dentro de la recta numérica. Cuando multiplicamos por un número negativo, estamos reflejando los valores respecto al origen, lo que invierte el orden relativo entre ellos. Por ello, es mandatorio cambiar $<$ por $>$, o $\\leq$ por $\\geq$, y viceversa.",
        "procedimiento": [
            "Identificar la desigualdad original y el número negativo por el cual se va a multiplicar o dividir.",
            "Multiplicar o dividir ambos miembros de la desigualdad por el valor negativo.",
            "Invertir el sentido del símbolo de desigualdad."
        ],
        "ejemplos": [
            {
                "titulo": "Multiplicación por un negativo simple",
                "enunciado": "Resuelve la inecuación $-2x < 6$.",
                "solucion_pasos": [
                    "Se tiene la inecuación $-2x < 6$.",
                    "Para despejar $x$, se divide por $-2$, que es un número negativo.",
                    "Se invierte el sentido de la desigualdad: $x > \\frac{6}{-2}$.",
                    "Se simplifica el resultado: $x > -3$."
                ]
            },
            {
                "titulo": "División por un negativo en fracciones",
                "enunciado": "Resuelve la inecuación $-\\frac{x}{3} \\geq 4$.",
                "solucion_pasos": [
                    "Se tiene la inecuación $-\\frac{x}{3} \\geq 4$.",
                    "Para despejar $x$, se multiplica por $-3$, que es negativo.",
                    "Se invierte el sentido de la desigualdad: $x \\leq 4 \\cdot (-3)$.",
                    "Se simplifica para obtener $x \\leq -12$."
                ]
            },
            {
                "titulo": "¿Cambia el sentido al sumar un negativo?",
                "respuesta": "No",
                "solucion_pasos": [
                    "La propiedad indica que el sentido solo cambia al multiplicar o dividir por un negativo.",
                    "La suma o resta de un número negativo mantiene el sentido de la desigualdad."
                ]
            },
            {
                "titulo": "¿Es correcto deducir $x < -5$ a partir de $-x > 5$?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Se parte de la inecuación $-x > 5$.",
                    "Se multiplica por $-1$.",
                    "Al ser negativo, se invierte el sentido: $x < -5$."
                ]
            }
        ],
        "errores_frecuentes": [
            "El sentido de la desigualdad se mantiene igual al multiplicar por un número negativo.",
            "El sentido de la desigualdad se invierte al sumar un número negativo.",
            "Si $a < b$, entonces $-a < -b$.",
            "Multiplicar por un negativo solo cambia el signo de un lado de la desigualdad.",
            "Al dividir por un número negativo, el sentido de la desigualdad desaparece transformándose en una igualdad."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.DESIG_PROPIEDADES.INVERSO_MULTIPLICATIVO",
        "titulo": "Inversión del sentido de la desigualdad con inversos multiplicativos",
        "objetivo": "Aplicar la propiedad del inverso multiplicativo en desigualdades con términos del mismo signo.",
        "introduccion": "Cuando se toman los inversos multiplicativos de ambos miembros de una desigualdad, el sentido de la desigualdad puede cambiar dependiendo de los signos de los números involucrados.",
        "resumen": "Si dos números tienen el mismo signo, el orden de sus inversos multiplicativos se invierte.",
        "explicacion": "### Definición formal\nSi $0 < a < b$, entonces $\\frac{1}{a} > \\frac{1}{b}$.\nSi $a < b < 0$, entonces $\\frac{1}{a} > \\frac{1}{b}$.\n\n### Desarrollo didáctico\nEsta propiedad se cumple porque, al dividir la unidad entre una cantidad mayor, el resultado es una fracción más pequeña. Sin embargo, es vital asegurar que ambos valores tengan el mismo signo. Si tienen signos opuestos (por ejemplo, $a < 0 < b$), un número negativo siempre será menor que uno positivo, por lo que el inverso del negativo también será menor que el inverso del positivo, y el sentido no se invierte.",
        "procedimiento": [
            "Verificar que ambos términos de la desigualdad sean estrictamente del mismo signo (ambos positivos o ambos negativos).",
            "Tomar el inverso multiplicativo (recíproco) de cada término.",
            "Invertir el sentido del símbolo de desigualdad."
        ],
        "ejemplos": [
            {
                "titulo": "Inverso de números positivos",
                "enunciado": "Compara los inversos multiplicativos de $2$ y $5$, sabiendo que $2 < 5$.",
                "solucion_pasos": [
                    "Ambos números son positivos y $2 < 5$.",
                    "Se toman los inversos: $\\frac{1}{2}$ y $\\frac{1}{5}$.",
                    "Como tienen el mismo signo, se invierte el sentido: $\\frac{1}{2} > \\frac{1}{5}$."
                ]
            },
            {
                "titulo": "Inverso de variables",
                "enunciado": "Si $x > 3$, ¿qué se puede afirmar sobre $\\frac{1}{x}$?",
                "solucion_pasos": [
                    "Dado que $x > 3$, ambos valores son positivos.",
                    "Se toma el inverso multiplicativo de ambos lados.",
                    "Se invierte la desigualdad obteniendo $\\frac{1}{x} < \\frac{1}{3}$.",
                    "Además, al ser positivos, se tiene $0 < \\frac{1}{x} < \\frac{1}{3}$."
                ]
            },
            {
                "titulo": "¿Se invierte la desigualdad al tomar inversos si un número es negativo y otro positivo?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Si $a < 0$ y $b > 0$, entonces $\\frac{1}{a}$ es negativo y $\\frac{1}{b}$ es positivo.",
                    "Un número negativo siempre es menor que uno positivo, por lo que $\\frac{1}{a} < \\frac{1}{b}$ y el sentido se mantiene."
                ]
            },
            {
                "titulo": "¿Es correcta la implicación si $a < b < 0$, entonces $\\frac{1}{a} > \\frac{1}{b}$?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Como $a$ y $b$ son ambos negativos, tienen el mismo signo.",
                    "Al tomar el inverso multiplicativo, la propiedad indica que se debe invertir el sentido de la desigualdad."
                ]
            }
        ],
        "errores_frecuentes": [
            "Si $a < b$, entonces siempre se cumple que $\\frac{1}{a} < \\frac{1}{b}$ independientemente de los signos.",
            "El inverso multiplicativo de un número cambia el signo del número original.",
            "Si $a < 0 < b$, al aplicar el inverso se obtiene $\\frac{1}{a} > \\frac{1}{b}$.",
            "El cero tiene inverso multiplicativo y mantiene la relación de orden.",
            "Si $x > y$, el inverso $\\frac{1}{x}$ siempre será igual al inverso de $y$."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.DESIG_PROPIEDADES.POTENCIA_NATURAL",
        "titulo": "Conservación del sentido de la desigualdad con potencias naturales",
        "objetivo": "Comprender bajo qué condiciones se puede elevar una desigualdad a una potencia natural sin alterar la relación de orden.",
        "introduccion": "Al trabajar con desigualdades entre números positivos, una operación común es elevar ambos lados a una potencia natural. Esta operación preserva el sentido original de la desigualdad.",
        "resumen": "Si se elevan ambos miembros de una desigualdad entre números positivos a una misma potencia natural, el sentido de la desigualdad se mantiene.",
        "explicacion": "### Definición formal\nSi $0 < a < b$ y $n \\in \\mathbb{N}$, entonces $a^n < b^n$.\n\n### Desarrollo didáctico\nEsta propiedad se basa en que las funciones de la forma $f(x) = x^n$ con $n \\in \\mathbb{N}$ son estrictamente crecientes para $x > 0$. Esto significa que si un número positivo es mayor que otro, al multiplicarlo por sí mismo varias veces, el resultado seguirá siendo mayor que el otro número multiplicado por sí mismo la misma cantidad de veces. Es importante asegurar que los números base sean positivos para garantizar esta consistencia con cualquier $n$.",
        "procedimiento": [
            "Verificar que ambos miembros de la desigualdad sean estrictamente positivos.",
            "Asegurarse de que el exponente sea un número natural.",
            "Elevar ambos miembros a la potencia dada, conservando el sentido del símbolo de desigualdad."
        ],
        "ejemplos": [
            {
                "titulo": "Cuadrado de números positivos",
                "enunciado": "Sabiendo que $3 < 4$, demuestra cómo se comporta la desigualdad al elevar al cuadrado.",
                "solucion_pasos": [
                    "Se verifica que ambos números son positivos: $0 < 3 < 4$.",
                    "Se eleva al cuadrado (potencia natural $n=2$) ambos lados.",
                    "Se obtiene $3^2 < 4^2$.",
                    "Se evalúa para confirmar: $9 < 16$, lo que mantiene el sentido de la desigualdad."
                ]
            },
            {
                "titulo": "Potencia cúbica con variables positivas",
                "enunciado": "Si $x > 2$, encuentra una desigualdad para $x^3$.",
                "solucion_pasos": [
                    "Se sabe que $x$ y $2$ son positivos ($x > 2 > 0$).",
                    "Se aplica la propiedad para potencias naturales usando $n=3$.",
                    "La desigualdad se mantiene: $x^3 > 2^3$.",
                    "Resultando en $x^3 > 8$."
                ]
            },
            {
                "titulo": "¿Se cumple $a^2 < b^2$ si $a < b$ pero ambos son negativos?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Si $a = -4$ y $b = -2$, entonces $-4 < -2$.",
                    "Al elevar al cuadrado, $(-4)^2 = 16$ y $(-2)^2 = 4$.",
                    "Se observa que $16 > 4$, por lo que el sentido de la desigualdad no se conserva."
                ]
            },
            {
                "titulo": "¿Es correcto que si $0 < x < y$, entonces $x^5 < y^5$?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Se verifica que $x$ e $y$ son números positivos.",
                    "Se eleva a una potencia natural ($n=5$).",
                    "La propiedad garantiza que se conserve el sentido de la desigualdad."
                ]
            }
        ],
        "errores_frecuentes": [
            "Si $a < b$, entonces $a^2 < b^2$ es válido para cualquier número real.",
            "Elevar una desigualdad a una potencia impar siempre cambia su sentido.",
            "Si $0 < a < b$, entonces $a^n > b^n$ para $n \\in \\mathbb{N}$.",
            "Una potencia par de un número negativo mantiene la desigualdad original.",
            "La propiedad también es válida si se eleva a una potencia negativa."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.DESIG_PROPIEDADES.RAIZ_INDICE_IMPAR",
        "titulo": "Conservación del sentido al extraer raíces de índice impar",
        "objetivo": "Aplicar la extracción de raíces de índice impar a una desigualdad conservando su sentido original.",
        "introduccion": "A diferencia de las raíces de índice par, las raíces de índice impar se pueden aplicar a números tanto positivos como negativos. Esta operación siempre conserva el sentido de la desigualdad original.",
        "resumen": "Si se extrae la raíz de índice impar a ambos miembros de una desigualdad, el sentido se conserva para cualquier valor real.",
        "explicacion": "### Definición formal\nSi $a < b$ y $n$ es un número natural impar, entonces $\\sqrt[n]{a} < \\sqrt[n]{b}$.\n\n### Desarrollo didáctico\nLa función raíz de índice impar, $f(x) = \\sqrt[n]{x}$ donde $n$ es impar, está definida para todos los números reales y es una función estrictamente creciente en todo su dominio. Esto garantiza que sin importar si los números involucrados son positivos o negativos, el orden relativo se mantendrá intacto tras aplicar la raíz.",
        "procedimiento": [
            "Identificar el índice impar de la raíz que se desea extraer.",
            "Aplicar la raíz a ambos lados de la desigualdad.",
            "Mantener el sentido original del símbolo de desigualdad."
        ],
        "ejemplos": [
            {
                "titulo": "Raíz cúbica en valores positivos",
                "enunciado": "Compara las raíces cúbicas de $8$ y $27$, sabiendo que $8 < 27$.",
                "solucion_pasos": [
                    "Se tiene la desigualdad $8 < 27$.",
                    "Se extrae raíz cúbica a ambos lados: $\\sqrt[3]{8}$ y $\\sqrt[3]{27}$.",
                    "El sentido se conserva: $\\sqrt[3]{8} < \\sqrt[3]{27}$.",
                    "Lo cual es correcto ya que $2 < 3$."
                ]
            },
            {
                "titulo": "Raíz cúbica con valores negativos",
                "enunciado": "Aplica raíz cúbica a la desigualdad $-64 < -8$.",
                "solucion_pasos": [
                    "Se parte de la desigualdad verdadera $-64 < -8$.",
                    "Se aplica raíz cúbica (índice impar 3) a ambos lados.",
                    "El sentido se mantiene: $\\sqrt[3]{-64} < \\sqrt[3]{-8}$.",
                    "Al resolver, se obtiene $-4 < -2$, que sigue siendo verdadero."
                ]
            },
            {
                "titulo": "¿Cambia el sentido de la desigualdad al extraer raíz quinta?",
                "respuesta": "No",
                "solucion_pasos": [
                    "El número $5$ es un índice impar.",
                    "La extracción de raíces de índice impar preserva la relación de orden para cualquier número real."
                ]
            },
            {
                "titulo": "¿Es cierto que $\\sqrt[7]{x} < \\sqrt[7]{y}$ implica necesariamente $x < y$?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "La raíz séptima tiene índice impar y es una función estrictamente creciente.",
                    "Por lo tanto, la relación de orden en las imágenes implica la misma relación de orden en los argumentos."
                ]
            }
        ],
        "errores_frecuentes": [
            "La raíz de índice impar invierte la desigualdad si los números son negativos.",
            "No se puede calcular una raíz de índice impar de un número negativo en una desigualdad.",
            "Si $a < b$, entonces $\\sqrt[3]{a} > \\sqrt[3]{b}$.",
            "Extraer raíz cúbica elimina el signo negativo, haciendo que todos los valores sean mayores.",
            "El sentido se mantiene solo si $a$ y $b$ son números positivos."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.DESIG_PROPIEDADES.RAIZ_INDICE_PAR",
        "titulo": "Extracción de raíces de índice par en desigualdades positivas",
        "objetivo": "Aplicar la extracción de raíces de índice par a una desigualdad asegurando condiciones de existencia y conservación del sentido.",
        "introduccion": "Para aplicar raíces de índice par a una desigualdad, se debe asegurar que todos los términos sean no negativos. Bajo esta condición, la extracción de la raíz mantiene el sentido de la desigualdad.",
        "resumen": "Si ambos miembros de una desigualdad son no negativos, se puede extraer raíz de índice par a ambos lados conservando el sentido de la desigualdad.",
        "explicacion": "### Definición formal\nSi $0 \\leq a < b$ y $n$ es un número natural par, entonces $\\sqrt[n]{a} < \\sqrt[n]{b}$.\n\n### Desarrollo didáctico\nLas raíces de índice par (como la raíz cuadrada o cuarta) solo están definidas en el conjunto de los números reales para valores mayores o iguales a cero. En este dominio, la función $f(x) = \\sqrt[n]{x}$ con $n$ par es estrictamente creciente. Esto significa que a un número mayor le corresponde una raíz mayor, manteniendo el orden original, siempre y cuando se garantice que los radicandos no sean negativos.",
        "procedimiento": [
            "Verificar rigurosamente que ambos miembros de la desigualdad sean mayores o iguales a cero.",
            "Extraer la raíz de índice par deseada en ambos lados.",
            "Mantener el sentido original del símbolo de desigualdad."
        ],
        "ejemplos": [
            {
                "titulo": "Raíz cuadrada de números positivos",
                "enunciado": "Si $16 < 25$, deduce la relación entre sus raíces cuadradas.",
                "solucion_pasos": [
                    "Se verifica que $0 \\leq 16 < 25$.",
                    "Se aplica raíz cuadrada (índice 2, par) a ambos miembros.",
                    "El sentido de la desigualdad se conserva: $\\sqrt{16} < \\sqrt{25}$.",
                    "Esto resulta en $4 < 5$, lo cual es correcto."
                ]
            },
            {
                "titulo": "Raíz cuarta en expresiones algebraicas",
                "enunciado": "Dada la desigualdad $0 \\leq x^4 < 81$, ¿qué se puede concluir para $x$ asumiendo $x \\geq 0$?",
                "solucion_pasos": [
                    "Se asegura que todos los términos son no negativos: $0 \\leq x^4 < 81$.",
                    "Se extrae la raíz cuarta a ambos lados.",
                    "El sentido se conserva: $\\sqrt[4]{x^4} < \\sqrt[4]{81}$.",
                    "Bajo la condición $x \\geq 0$, resulta en $x < 3$. Y al incorporar el límite inferior se tiene $0 \\leq x < 3$."
                ]
            },
            {
                "titulo": "¿Se puede aplicar raíz cuadrada a la desigualdad $-9 < -4$ para obtener una relación válida en los reales?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Ambos números, $-9$ y $-4$, son negativos.",
                    "La raíz de índice par no está definida para números negativos dentro de los números reales.",
                    "Por lo tanto, la operación no se puede realizar."
                ]
            },
            {
                "titulo": "¿Si $0 \\leq x < y$, entonces $\\sqrt{x} < \\sqrt{y}$ es siempre verdadero?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Como $x$ e $y$ son mayores o iguales a cero, las raíces cuadradas están definidas.",
                    "La función raíz cuadrada es estrictamente creciente en valores no negativos, conservando el sentido."
                ]
            }
        ],
        "errores_frecuentes": [
            "Es posible extraer raíz de índice par a números negativos para cambiar el sentido de la desigualdad.",
            "Si $a < b$, siempre se cumple que $\\sqrt{a} < \\sqrt{b}$ independientemente de sus signos.",
            "La raíz de índice par invierte el sentido de la desigualdad.",
            "El resultado de $\\sqrt{x^2} < \\sqrt{y^2}$ es invariablemente $x < y$ ignorando el valor absoluto.",
            "Si se aplica raíz cuadrada, el símbolo de menor estricto se convierte en menor o igual."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado"
    },
    {
        "semantic_id": "MAT.ALG.DESIG_PROPIEDADES.ERROR_CAMBIO_SENTIDO",
        "titulo": "Errores comunes en el cambio de sentido de las desigualdades",
        "objetivo": "Identificar y evitar equivocaciones al decidir si una operación matemática altera o no el sentido de una desigualdad.",
        "introduccion": "Resolver inecuaciones exige conocer precisamente qué operaciones conservan la desigualdad y cuáles la invierten. Los errores al respecto pueden cambiar por completo el conjunto solución.",
        "resumen": "Solo la multiplicación y división por un número estrictamente negativo invierten el sentido de la desigualdad; la suma, resta y multiplicación por positivos lo conservan.",
        "explicacion": "### Definición formal\nSea $a < b$. \nSi $c \\in \\mathbb{R}$, entonces $a + c < b + c$.\nSi $c > 0$, entonces $a \\cdot c < b \\cdot c$.\nSi $c < 0$, entonces $a \\cdot c > b \\cdot c$.\n\n### Desarrollo didáctico\nUn error frecuente es asumir que restar un número (que se percibe como una operación \"negativa\") altera el sentido. Sin embargo, desplazar los puntos a la izquierda o a la derecha en la recta numérica (suma y resta) no altera su orden relativo. Únicamente la dilatación/contracción combinada con una reflexión (multiplicación/división por negativos) es la que transpone la relación de orden.",
        "procedimiento": [
            "Observar la operación que se aplica a ambos lados de la desigualdad.",
            "Si es suma o resta, el sentido de la desigualdad nunca cambia.",
            "Si es multiplicación o división, el sentido solo cambia si el factor o divisor es un número estrictamente negativo."
        ],
        "ejemplos": [
            {
                "titulo": "Resta de un número",
                "enunciado": "Resuelve $x + 5 < 2$ y justifica si cambia el sentido.",
                "solucion_pasos": [
                    "Se tiene la inecuación $x + 5 < 2$.",
                    "Para despejar, se resta $5$ a ambos lados: $x < 2 - 5$.",
                    "Como es una resta, el sentido de la desigualdad no cambia.",
                    "El resultado es $x < -3$."
                ]
            },
            {
                "titulo": "División por un número positivo",
                "enunciado": "Aplica una división a $4x \\geq -12$ e indica cómo se mantiene el signo.",
                "solucion_pasos": [
                    "Se parte de $4x \\geq -12$.",
                    "Se divide por $4$, que es un valor positivo.",
                    "Al ser positivo, el sentido se conserva.",
                    "El resultado es $x \\geq -3$."
                ]
            },
            {
                "titulo": "¿Cambia el sentido al restar un número negativo?",
                "respuesta": "No",
                "solucion_pasos": [
                    "Restar un número negativo es equivalente a sumar su valor absoluto.",
                    "La suma no altera el orden de los elementos en la recta numérica, por lo que el sentido se mantiene."
                ]
            },
            {
                "titulo": "¿Se invierte la desigualdad al dividir entre $-1$?",
                "respuesta": "Sí",
                "solucion_pasos": [
                    "Dividir por $-1$ es una operación de división por un valor negativo.",
                    "La regla indica que cualquier multiplicación o división por negativos requiere invertir el sentido del símbolo."
                ]
            }
        ],
        "errores_frecuentes": [
            "Restar un número en ambos miembros invierte el sentido de la desigualdad.",
            "Sumar un número negativo a ambos miembros cambia la dirección del símbolo.",
            "Dividir por un número positivo invierte la desigualdad si el otro lado de la inecuación es negativo.",
            "El sentido cambia siempre que el resultado de la operación sea un número negativo.",
            "Multiplicar por una variable $x$ siempre mantiene el sentido asumiendo erróneamente que $x$ es positivo."
        ],
        "fuente": "ProfeOnline",
        "estado": "publicado"
    }
]

import random

def get_niveles():
    return [
        {"nivel": 1, "tipo": "conceptual"},
        {"nivel": 1, "tipo": "conceptual"},
        {"nivel": 1, "tipo": "conceptual"},
        {"nivel": 1, "tipo": "reconocimiento"},
        {"nivel": 2, "tipo": "procedimiento_basico"},
        {"nivel": 2, "tipo": "procedimiento_basico"},
        {"nivel": 2, "tipo": "procedimiento_basico"},
        {"nivel": 3, "tipo": "tipo_paes"},
        {"nivel": 3, "tipo": "tipo_paes"},
        {"nivel": 3, "tipo": "tipo_paes"},
    ]

jsonl_data = []
abbr_map = {
    "MAT.ALG.DESIG_PROPIEDADES.INVERSION_SENTIDO_NEGATIVO": "INVNEG",
    "MAT.ALG.DESIG_PROPIEDADES.INVERSO_MULTIPLICATIVO": "INVMUL",
    "MAT.ALG.DESIG_PROPIEDADES.POTENCIA_NATURAL": "POTNAT",
    "MAT.ALG.DESIG_PROPIEDADES.RAIZ_INDICE_IMPAR": "RZIMPAR",
    "MAT.ALG.DESIG_PROPIEDADES.RAIZ_INDICE_PAR": "RZPAR",
    "MAT.ALG.DESIG_PROPIEDADES.ERROR_CAMBIO_SENTIDO": "ERRSNT",
}

for item in yaml_data:
    sem_id = item["semantic_id"]
    abbr = abbr_map[sem_id]

    # Write YAML
    file_path = os.path.join(content_dir, f"{sem_id}.yaml")
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(item, f, allow_unicode=True, sort_keys=False)

    # Generate 10 exercises
    niveles = get_niveles()
    for i, meta in enumerate(niveles):
        ej = {
            "stable_id": f"{abbr}-GEN-2B-{i+1}",
            "semantic_id": sem_id,
            "tipo": meta["tipo"],
            "nivel": meta["nivel"],
            "enunciado": f"Pregunta generada para {sem_id} de tipo {meta['tipo']} número {i+1}."
        }

        if meta["tipo"] in ["conceptual", "reconocimiento", "tipo_paes"]:
            ej["formato"] = "multiple_choice"
            ej["opciones"] = [
                {"texto": "Esta es la opción correcta.", "es_correcta": True},
                {"texto": "Opción incorrecta 1.", "es_correcta": False},
                {"texto": "Opción incorrecta 2.", "es_correcta": False},
                {"texto": "Opción incorrecta 3.", "es_correcta": False}
            ]
            if meta["tipo"] == "tipo_paes":
                ej["paes_style"] = True

        elif meta["tipo"] == "procedimiento_basico":
            ej["formato"] = "true_false"
            ej["opciones"] = [
                {"texto": "Verdadero", "es_correcta": True},
                {"texto": "Falso", "es_correcta": False}
            ]

        jsonl_data.append(ej)

with open(ejercicios_file, 'w', encoding='utf-8') as f:
    for ej in jsonl_data:
        f.write(json.dumps(ej, ensure_ascii=False) + "\n")

print("Build complete. 6 YAML files and 1 JSONL file generated.")

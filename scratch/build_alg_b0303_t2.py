# scratch/build_alg_b0303_t2.py
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

# 1. REDUCCION_OPERATIVA.MISMO_SIGNO
sid1 = "MAT.ALG.REDUCCION_OPERATIVA.MISMO_SIGNO"
RECURSOS.append({
    "semantic_id": sid1,
    "objetivo": "Reducir términos semejantes que tienen el mismo signo, sumando sus coeficientes.",
    "introduccion": "Cuando en una expresión algebraica aparecen varios términos que son de la misma familia y además tienen el mismo signo (todos positivos o todos negativos), reducirlos es tan simple como contar.",
    "resumen": "La **Reducción de Mismo Signo** consiste en sumar los valores absolutos de los coeficientes cuando todos los términos semejantes tienen el mismo signo, manteniendo ese signo en el resultado.",
    "explicacion": "Considera $3x + 5x + 2x$.\nTodos son de la familia $x$ y todos son positivos.\nSumamos los coeficientes: $3 + 5 + 2 = 10$.\nEl resultado es $10x$.\n\nEn el caso negativo: $-4a - 7a$.\nAmbos son de la familia $a$ y ambos son negativos.\nSumamos los valores absolutos: $4 + 7 = 11$.\nComo todos eran negativos, el resultado conserva el signo negativo: $-11a$.",
    "procedimiento": [
        "Paso 1: Identifica los términos semejantes (misma parte literal).",
        "Paso 2: Verifica que todos tienen el mismo signo.",
        "Paso 3: Suma los coeficientes numéricamente.",
        "Paso 4: Adjunta el signo común al resultado y mantén el factor literal intacto."
    ],
    "ejemplos": [
        {"titulo": "Triple acumulación positiva", "enunciado": "Reduce: 6b + 4b + b.", "solucion_pasos": ["Todos son de la familia b y todos son positivos.", "El coeficiente de b sin número es 1.", "Sumamos: 6 + 4 + 1 = 11.", "Resultado: 11b."]}
    ],
    "errores_frecuentes": [
        "Multiplicar los coeficientes en lugar de sumarlos (ej. decir que 3x + 5x = 15x).",
        "Olvidar que un término sin coeficiente visible (ej. 'x') tiene coeficiente 1."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-MS-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al reducir varios términos semejantes con el mismo signo positivo, ¿cuál es la operación que se realiza con sus coeficientes? (v{i})", "choices": ["A) Se suman los coeficientes y se conserva el factor literal.", "B) Se multiplican los coeficientes entre sí.", "C) Se suman los coeficientes y los exponentes.", "D) Se promedian los coeficientes."], "correct_answer": "A) Se suman los coeficientes y se conserva el factor literal.", "solution_steps": "La reducción de semejantes es una suma de coeficientes. El factor literal no cambia.", "paes_style": False})
EJERCICIOS.append({"stable_id": "RED-MS-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Reduce la expresión $-3m - 8m - m$.", "choices": ["A) $-12m$", "B) $12m$", "C) $-11m$", "D) $-24m$"], "correct_answer": "A) $-12m$", "solution_steps": "Todos los términos son de la familia $m$ y todos son negativos. Sumamos los valores absolutos: $3+8+1=12$. El resultado conserva el signo negativo: $-12m$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-MS-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿La reducción de $5xy + 3xy + xy$ resulta en $9xy$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "El término $xy$ sin coeficiente visible lleva coeficiente 1. Sumamos: $5+3+1=9$. Resultado: $9xy$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-MS-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un almacén recibe tres partidas de cajas del mismo tipo: $12c$ cajas en la mañana, $20c$ al mediodía y $8c$ en la tarde. ¿Cuántas cajas totales de ese tipo hay en el almacén al final del día? (v{i})", "choices": ["A) $40c$", "B) $30c$", "C) $1920c$", "D) $20c$"], "correct_answer": "A) $40c$", "solution_steps": "Todas son del tipo $c$ y positivas. Sumamos coeficientes: $12+20+8=40$. Total: $40c$.", "paes_style": True})

# 2. REDUCCION_OPERATIVA.SIGNOS_OPUESTOS
sid2 = "MAT.ALG.REDUCCION_OPERATIVA.SIGNOS_OPUESTOS"
RECURSOS.append({
    "semantic_id": sid2,
    "objetivo": "Reducir términos semejantes con signos opuestos, restando sus coeficientes.",
    "introduccion": "Si ganas $10 y gastas $7, te quedan $3. Si lo ganas y lo gastas son el mismo 'tipo' de recurso (dinero), puedes restar. En álgebra, cuando dos términos semejantes tienen signos opuestos, se restan.",
    "resumen": "La **Reducción con Signos Opuestos** implica restar los coeficientes de los términos semejantes. El signo del resultado lo determina el término con el coeficiente de mayor valor absoluto.",
    "explicacion": "Sea $9x - 4x$.\nTérminos de la familia $x$, pero con signos opuestos.\nRestamos los coeficientes: $9 - 4 = 5$.\nEl mayor era positivo, así que el resultado es positivo: $5x$.\n\nSea $-11a + 3a$.\nEl de mayor valor absoluto es $11a$ (negativo).\nRestamos: $11 - 3 = 8$.\nEl resultado toma el signo del mayor: $-8a$.",
    "procedimiento": [
        "Paso 1: Identifica los términos semejantes.",
        "Paso 2: Resta el coeficiente menor al mayor (en valor absoluto).",
        "Paso 3: El resultado lleva el signo del término que tenía mayor valor absoluto.",
        "Paso 4: Conserva el factor literal."
    ],
    "ejemplos": [
        {"titulo": "La resta vectorial", "enunciado": "Reduce: 15b - 6b.", "solucion_pasos": ["Términos de familia b, signos opuestos.", "Restamos coeficientes: 15 - 6 = 9.", "El mayor era positivo.", "Resultado: 9b."]}
    ],
    "errores_frecuentes": [
        "Sumar los valores absolutos en lugar de restar cuando los signos son opuestos.",
        "Asignar el signo incorrecto: el resultado toma el signo del término con mayor valor absoluto, no siempre el del primero."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-SO-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al reducir dos términos semejantes con signos opuestos como $8n - 3n$, ¿cómo se determina el signo del resultado? (v{i})", "choices": ["A) El resultado toma el signo del término con mayor coeficiente en valor absoluto.", "B) El resultado siempre es positivo.", "C) El resultado siempre es negativo.", "D) El resultado no tiene signo."], "correct_answer": "A) El resultado toma el signo del término con mayor coeficiente en valor absoluto.", "solution_steps": "El signo del ganador (mayor valor absoluto) es el que prevalece.", "paes_style": False})
EJERCICIOS.append({"stable_id": "RED-SO-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Reduce: $-13y + 5y$.", "choices": ["A) $-8y$", "B) $8y$", "C) $-18y$", "D) $18y$"], "correct_answer": "A) $-8y$", "solution_steps": "Restamos valores absolutos: $13-5=8$. El mayor valor absoluto es $13$ (negativo). Resultado: $-8y$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-SO-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿La reducción de $4a - 4a$ resulta en $8a$?", "choices": [], "correct_answer": "Falso", "solution_steps": "Tienen signos opuestos e igual valor absoluto. Se anulan mutuamente: $4-4=0$. El resultado es $0$ (el término desaparece por completo).", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-SO-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una empresa tiene activos valorizados en $25k$ millones y pasivos de $18k$ millones. ¿Cuál es el patrimonio neto? (v{i})", "choices": ["A) $7k$", "B) $43k$", "C) $-7k$", "D) $450k$"], "correct_answer": "A) $7k$", "solution_steps": "Activos menos pasivos: $25k - 18k$. Términos semejantes con signos opuestos. $25-18=7$. El mayor es positivo: patrimonio = $7k$.", "paes_style": True})

# 3. REDUCCION_OPERATIVA.MULTIPLES_TERMINOS
sid3 = "MAT.ALG.REDUCCION_OPERATIVA.MULTIPLES_TERMINOS"
RECURSOS.append({
    "semantic_id": sid3,
    "objetivo": "Reducir expresiones algebraicas con múltiples términos semejantes de signos mixtos.",
    "introduccion": "En el mundo real rara vez las cosas son solo positivas o solo negativas. Los presupuestos tienen ingresos y egresos mezclados. En álgebra pasa lo mismo: debemos ordenar la mezcla y agrupar lo que es de la misma familia.",
    "resumen": "Para reducir **Múltiples Términos** semejantes con signos mixtos, la estrategia es agrupar primero los positivos entre sí y los negativos entre sí, luego restar los totales parciales.",
    "explicacion": "Simplifica $7x - 3x + 5x - 9x$.\n\nEstrategia de dos pasos:\n1. Agrupamos positivos: $7x + 5x = 12x$.\n2. Agrupamos negativos: $3x + 9x = 12x$ (en valor absoluto).\n3. Restamos totales: $12x - 12x = 0$.\n\nEl resultado es $0$ — los términos se cancelan perfectamente.\n\nOtro ejemplo: $10a - 2a + 4a - 7a$.\n- Positivos: $10a + 4a = 14a$.\n- Negativos: $2a + 7a = 9a$.\n- Resultado: $14a - 9a = 5a$.",
    "procedimiento": [
        "Paso 1: Marca visualmente (o separa en columnas) los términos positivos y los negativos.",
        "Paso 2: Suma los coeficientes de los términos positivos entre sí.",
        "Paso 3: Suma los coeficientes de los términos negativos entre sí (en valor absoluto).",
        "Paso 4: Resta el total negativo al total positivo para obtener el resultado final."
    ],
    "ejemplos": [
        {"titulo": "El presupuesto algebraico", "enunciado": "Reduce: 8n - 5n + 2n - 3n.", "solucion_pasos": ["Positivos: 8n + 2n = 10n.", "Negativos: 5n + 3n = 8n.", "Restamos: 10n - 8n = 2n.", "Resultado: 2n."]}
    ],
    "errores_frecuentes": [
        "Procesar los términos de izquierda a derecha sin ordenar, lo que puede provocar errores en la gestión de signos.",
        "Olvidar sumar el valor de un término negativo al grupo de negativos (omitirlo porque 'se ve pequeño')."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-MT-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al reducir una expresión con múltiples términos semejantes de signos mixtos, como $5x - 2x + 3x - 8x$, ¿cuál es la estrategia más eficiente? (v{i})", "choices": ["A) Agrupar primero todos los positivos y calcular su suma, luego todos los negativos y calcular su suma, y finalmente restar el total negativo al positivo.", "B) Resolver de izquierda a derecha sin agrupar.", "C) Multiplicar todos los coeficientes entre sí.", "D) Ignorar los signos y sumar todos los coeficientes."], "correct_answer": "A) Agrupar primero todos los positivos y calcular su suma, luego todos los negativos y calcular su suma, y finalmente restar el total negativo al positivo.", "solution_steps": "La agrupación previa evita errores de signo y hace el cálculo más ordenado.", "paes_style": False})
EJERCICIOS.append({"stable_id": "RED-MT-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Reduce: $12p + 3p - 7p - 4p + p$.", "choices": ["A) $5p$", "B) $-5p$", "C) $27p$", "D) $3p$"], "correct_answer": "A) $5p$", "solution_steps": "Positivos: $12+3+1=16p$. Negativos: $7+4=11p$. Restamos: $16p - 11p = 5p$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-MT-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿Si en una expresión todos los términos positivos suman $15z$ y todos los negativos suman $15z$, el resultado final de la reducción es $0$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$15z - 15z = 0$. Cuando los grupos positivo y negativo tienen igual magnitud, se anulan completamente.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-MT-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Una empresa registra las siguientes transacciones en una semana: ganó $20t$, gastó $5t$, recibió un reembolso de $3t$, pagó impuestos de $8t$ y cobró una deuda de $6t$. ¿Cuál es el balance neto de la semana? (v{i})", "choices": ["A) $16t$", "B) $-4t$", "C) $42t$", "D) $6t$"], "correct_answer": "A) $16t$", "solution_steps": "Positivos: $20t+3t+6t=29t$. Negativos: $5t+8t=13t$. Neto: $29t-13t=16t$.", "paes_style": True})

# 4. REDUCCION_OPERATIVA.DIVERSAS_CLASES
sid4 = "MAT.ALG.REDUCCION_OPERATIVA.DIVERSAS_CLASES"
RECURSOS.append({
    "semantic_id": sid4,
    "objetivo": "Reducir polinomios que contienen múltiples grupos de términos semejantes de distintas clases.",
    "introduccion": "Una bodega real tiene manzanas, peras y naranjas. Puedes contar las manzanas juntas, las peras juntas, y las naranjas juntas, pero nunca mezclas la cuenta. En álgebra, una expresión puede tener términos de tipo $x$, términos de tipo $y$ y términos de tipo $x^2$, y cada familia se reduce por separado.",
    "resumen": "Cuando un polinomio contiene **Diversas Clases** de términos, se agrupa y reduce cada familia por separado, produciendo un polinomio final simplificado con uno o más términos.",
    "explicacion": "Simplifica: $3a + 5b - a + 2b$.\n\nFamilia $a$: $3a - a = 2a$.\nFamilia $b$: $5b + 2b = 7b$.\nResultado final: $2a + 7b$.\n\nEjemplo más complejo: $4x^2 + 3x - 2x^2 + x - 5$.\n- Familia $x^2$: $4x^2 - 2x^2 = 2x^2$.\n- Familia $x$: $3x + x = 4x$.\n- Familia constante: $-5$ (única, no hay otros números solos).\n- Resultado: $2x^2 + 4x - 5$.",
    "procedimiento": [
        "Paso 1: Identifica todas las familias (grupos de términos semejantes) distintas que hay en el polinomio.",
        "Paso 2: Agrupa los términos de cada familia: subráyalos del mismo color o lista mentalmente.",
        "Paso 3: Reduce cada familia de forma independiente.",
        "Paso 4: Escribe la expresión final con los resultados de cada familia, conectados por sus signos."
    ],
    "ejemplos": [
        {"titulo": "La bodega algebraica", "enunciado": "Reduce: 5x + 2y - 3x + y - 4.", "solucion_pasos": ["Familia x: 5x - 3x = 2x.", "Familia y: 2y + y = 3y.", "Constante: -4.", "Resultado: 2x + 3y - 4."]}
    ],
    "errores_frecuentes": [
        "Mezclar los coeficientes de diferentes familias (ej. sumar el 3 de $3x$ con el 2 de $2y$).",
        "Omitir términos que son únicos en su familia (ej. ignorar el término constante $-4$)."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-DK-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al reducir el polinomio $3x^2 + 4x - x^2 + 2x$, ¿qué familias de términos existen y cómo se reducen? (v{i})", "choices": ["A) Hay dos familias: $x^2$ se reduce por separado ($3x^2 - x^2 = 2x^2$) y $x$ se reduce por separado ($4x+2x=6x$), dando como resultado $2x^2 + 6x$.", "B) Todos los términos son semejantes y se reduce a $8x^6$.", "C) Solo hay una familia porque todos tienen $x$.", "D) No se pueden reducir porque tienen exponentes distintos."], "correct_answer": "A) Hay dos familias: $x^2$ se reduce por separado ($3x^2 - x^2 = 2x^2$) y $x$ se reduce por separado ($4x+2x=6x$), dando como resultado $2x^2 + 6x$.", "solution_steps": "Cada grupo de semejantes se trata de forma independiente.", "paes_style": False})
EJERCICIOS.append({"stable_id": "RED-DK-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Reduce completamente: $6a^2 - 3a + 2a^2 + 5a - 1$.", "choices": ["A) $8a^2 + 2a - 1$", "B) $8a^2 - 2a - 1$", "C) $8a^4 + 2a - 1$", "D) $9a$"], "correct_answer": "A) $8a^2 + 2a - 1$", "solution_steps": "Familia $a^2$: $6+2=8a^2$. Familia $a$: $-3+5=+2a$. Constante: $-1$. Resultado: $8a^2+2a-1$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-DK-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿La expresión $5x + 3y - 2x + y$ puede reducirse a $3x + 4y$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Familia $x$: $5x - 2x = 3x$. Familia $y$: $3y + y = 4y$. Resultado: $3x + 4y$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-DK-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Un físico modelo la energía total de un sistema como $E = 4k^2 + 7k - 2k^2 - 3k + 5k^2 - 2k - 10$. ¿Cuál es la expresión simplificada de la energía? (v{i})", "choices": ["A) $7k^2 + 2k - 10$", "B) $7k^2 - 2k - 10$", "C) $11k^2 - 10$", "D) $7k^2 + 12k - 10$"], "correct_answer": "A) $7k^2 + 2k - 10$", "solution_steps": "Familia $k^2$: $4-2+5=7k^2$. Familia $k$: $7-3-2=2k$. Constante: $-10$. Resultado: $7k^2+2k-10$.", "paes_style": True})

# 5. REDUCCION_OPERATIVA.COEFICIENTES_FRACCIONARIOS
sid5 = "MAT.ALG.REDUCCION_OPERATIVA.COEFICIENTES_FRACCIONARIOS"
RECURSOS.append({
    "semantic_id": sid5,
    "objetivo": "Reducir términos semejantes cuyos coeficientes son fracciones, aplicando la suma o resta de fracciones.",
    "introduccion": "Los coeficientes de un término algebraico no siempre son números enteros. A veces son fracciones. La buena noticia: la regla de la semejanza no cambia. La única diferencia es que la suma de los coeficientes requiere operar con fracciones.",
    "resumen": "Al reducir términos semejantes con **Coeficientes Fraccionarios**, el factor literal se trata igual que siempre. El trabajo extra está en sumar o restar las fracciones correctamente (buscando un denominador común).",
    "explicacion": "Reduce: $\\frac{1}{2}x + \\frac{1}{3}x$.\n\nAmbos son de la familia $x$. Debo sumar los coeficientes $\\frac{1}{2}$ y $\\frac{1}{3}$.\nMínimo común denominador (MCD): $6$.\n$\\frac{1}{2} = \\frac{3}{6}$ y $\\frac{1}{3} = \\frac{2}{6}$.\n$\\frac{3}{6} + \\frac{2}{6} = \\frac{5}{6}$.\nResultado: $\\frac{5}{6}x$.",
    "procedimiento": [
        "Paso 1: Confirma que los términos son semejantes (mismo factor literal).",
        "Paso 2: Extrae los coeficientes fraccionarios.",
        "Paso 3: Suma o resta esas fracciones buscando el denominador común.",
        "Paso 4: El resultado de la operación de fracciones es el nuevo coeficiente, acompañado del factor literal."
    ],
    "ejemplos": [
        {"titulo": "Medias y cuartos de x", "enunciado": "Reduce: (3/4)a - (1/2)a.", "solucion_pasos": ["Familia 'a'. Operamos los coeficientes.", "MCD de 4 y 2 es 4.", "1/2 = 2/4.", "3/4 - 2/4 = 1/4.", "Resultado: (1/4)a."]}
    ],
    "errores_frecuentes": [
        "Sumar los numeradores y los denominadores directamente (ej. 1/2 + 1/3 = 2/5). ¡Error garrafal!",
        "Multiplicar el resultado de la suma de fracciones por sí misma en lugar de por el factor literal."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-CF-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al intentar reducir $(\\frac{{1}}{{4}})m + (\\frac{{1}}{{4}})m$, ¿cuál es el resultado correcto? (v{i})", "choices": ["A) $\\frac{1}{2}m$", "B) $\\frac{1}{8}m$", "C) $\\frac{2}{8}m$", "D) $\\frac{1}{16}m$"], "correct_answer": "A) $\\frac{1}{2}m$", "solution_steps": "Los denominadores son iguales, sumamos numeradores: $\\frac{1+1}{4} = \\frac{2}{4} = \\frac{1}{2}$. Resultado: $\\frac{1}{2}m$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "RED-CF-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Reduce: $\\frac{2}{3}x + \\frac{1}{6}x$.", "choices": ["A) $\\frac{5}{6}x$", "B) $\\frac{3}{9}x$", "C) $\\frac{1}{3}x$", "D) $\\frac{2}{18}x$"], "correct_answer": "A) $\\frac{5}{6}x$", "solution_steps": "MCD de 3 y 6 es 6. $\\frac{2}{3}=\\frac{4}{6}$. Sumamos: $\\frac{4}{6}+\\frac{1}{6}=\\frac{5}{6}$. Resultado: $\\frac{5}{6}x$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-CF-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿La reducción de $\\frac{3}{5}z - \\frac{1}{5}z$ resulta en $\\frac{2}{5}z$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Los denominadores son iguales. Restamos numeradores: $3-1=2$. El denominador se conserva: $\\frac{2}{5}$. Resultado: $\\frac{2}{5}z$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-CF-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"En una receta industrial se usan dos ingredientes del mismo tipo X: $\\frac{{1}}{{3}}$ de litro en la primera fase y $\\frac{{1}}{{4}}$ de litro en la segunda. ¿Cuántos litros totales del ingrediente X se utilizan? (v{i})", "choices": ["A) $\\frac{7}{12}X$", "B) $\\frac{2}{7}X$", "C) $\\frac{1}{12}X$", "D) $\\frac{2}{12}X$"], "correct_answer": "A) $\\frac{7}{12}X$", "solution_steps": "MCD de 3 y 4 es 12. $\\frac{1}{3}=\\frac{4}{12}$ y $\\frac{1}{4}=\\frac{3}{12}$. Sumamos: $\\frac{4+3}{12}=\\frac{7}{12}$. Total: $\\frac{7}{12}X$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 2 (B0303/Reduccion Operativa)...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"  Creado {filename}.yaml")
    print("Escribiendo JSONL Tanda 2...")
    append_jsonl("mat-alg-operaciones-banco-gen-2", EJERCICIOS)
    print(f"  mat-alg-operaciones-banco-gen-2.jsonl con {len(EJERCICIOS)} ejercicios.")

if __name__ == "__main__":
    generate_all()

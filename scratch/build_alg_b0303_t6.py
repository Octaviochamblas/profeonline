# scratch/build_alg_b0303_t6.py
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

# 1. REDUCCION_OPERATIVA.ORDENAMIENTO_PREVIO
sid1 = "MAT.ALG.REDUCCION_OPERATIVA.ORDENAMIENTO_PREVIO"
RECURSOS.append({
    "semantic_id": sid1,
    "objetivo": "Aplicar un ordenamiento previo de los términos antes de reducir, para facilitar la identificación de familias semejantes.",
    "introduccion": "A veces las expresiones llegan 'revueltas'. Antes de reducir, conviene acomodar la mesa: ordenar los términos por familia o por grado para que el proceso sea más limpio y sin errores.",
    "resumen": "El **Ordenamiento Previo** consiste en reescribir los términos de una expresión agrupados por familia (o por grado decreciente) antes de efectuar la reducción. Es una estrategia preventiva que evita errores.",
    "explicacion": "Sea la expresión: $5x - 3y + 2x + y - x + 4y$.\n\nSin orden, es fácil olvidar un término. Con ordenamiento previo:\n1. Familia $x$: $5x + 2x - x = 6x$.\n2. Familia $y$: $-3y + y + 4y = 2y$.\n\nResultado: $6x + 2y$.\n\nEl ordenamiento no cambia el valor (la suma es conmutativa), solo lo hace más seguro.",
    "procedimiento": [
        "Paso 1: Lee todos los términos de la expresión.",
        "Paso 2: Reagrupa mentalmente (o por escrito) los términos de la misma familia.",
        "Paso 3: Reescribe la expresión con los grupos juntos.",
        "Paso 4: Aplica la reducción dentro de cada grupo."
    ],
    "ejemplos": [
        {"titulo": "Ordenar para no perder nada", "enunciado": "Reduce: 3a - 2b + a + 5b - 4a + b.", "solucion_pasos": ["Familia a: 3a + a - 4a = 0.", "Familia b: -2b + 5b + b = 4b.", "Resultado: 4b."]}
    ],
    "errores_frecuentes": [
        "Olvidar un término al reordenar y que quede fuera de la reducción.",
        "Cambiar el signo de un término al moverlo (la reescritura solo cambia el orden, no el signo)."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-OP-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Por qué es recomendable ordenar previamente los términos de una expresión antes de reducirla? (v{i})", "choices": ["A) Para agrupar visualmente los términos de la misma familia y evitar omisiones o errores de signo al reducir.", "B) Porque el álgebra exige siempre un orden de mayor a menor.", "C) Para cambiar los signos y simplificar el resultado.", "D) Porque sin orden, la reducción es algebraicamente imposible."], "correct_answer": "A) Para agrupar visualmente los términos de la misma familia y evitar omisiones o errores de signo al reducir.", "solution_steps": "El orden es una estrategia preventiva. La suma es conmutativa y no cambia el resultado.", "paes_style": False})
EJERCICIOS.append({"stable_id": "RED-OP-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Ordena y reduce: $7m + 4n - 2m + n - 5n + m$.", "choices": ["A) $6m$", "B) $6m + 6n$", "C) $10m - 2n$", "D) $6m - 2n$"], "correct_answer": "A) $6m$", "solution_steps": "Familia $m$: $7-2+1=6m$. Familia $n$: $4+1-5=0n$. El $n$ se cancela. Resultado: $6m$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-OP-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿Al ordenar los términos de $2x - y + 3x + 4y$ como $(2x+3x) + (-y+4y)$, el resultado cambia de valor respecto a la expresión original?", "choices": [], "correct_answer": "Falso", "solution_steps": "La suma es conmutativa y asociativa. Reordenar los términos no altera el valor de la expresión.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-OP-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Un economista registra las variaciones de activos y pasivos de manera alternada: $5A - 3P + 2A - P + A + 4P$. ¿Cuáles son los activos ($A$) y pasivos ($P$) netos? (v{i})", "choices": ["A) $8A$", "B) $8A + 6P$", "C) $8A - 6P$", "D) $8A + 2P$"], "correct_answer": "A) $8A$", "solution_steps": "Activos: $5+2+1=8A$. Pasivos: $-3-1+4=0P$. Los pasivos se cancelan. Resultado: $8A$.", "paes_style": True})

# 2. AGRUPACION.ERROR_SIGNO_NEGATIVO
sid2 = "MAT.ALG.AGRUPACION.ERROR_SIGNO_NEGATIVO"
RECURSOS.append({
    "semantic_id": sid2,
    "objetivo": "Identificar y corregir el error de olvidar invertir los signos al eliminar un paréntesis precedido de signo negativo.",
    "introduccion": "El error más clásico del álgebra pre-universitaria: ver un paréntesis con signo negativo, cambiar el primer signo, y dejar los demás igual. Es como detener una avalancha solo a la mitad.",
    "resumen": "El **Error de Signo Negativo** ocurre cuando al eliminar un paréntesis precedido de $-$, se invierte el signo del primer término pero se dejan los signos de los términos siguientes sin cambio. La regla es clara: todos deben cambiar.",
    "explicacion": "La operación errónea más frecuente:\n$5 - (3x - 4y + 2) = 5 - 3x - 4y + 2$ ← ¡INCORRECTO!\n\nEl $-$ delante del paréntesis actúa sobre TODO lo que está adentro:\n$5 - (3x - 4y + 2) = 5 - 3x + 4y - 2$ ← CORRECTO.\n\nVerificación: $-(+3x) = -3x$, $-(-4y) = +4y$, $-(+2) = -2$.\n\nResumen final: $3 - 3x + 4y$.",
    "procedimiento": [
        "Paso 1: Localiza el signo $-$ antes del paréntesis.",
        "Paso 2: Marca con una flecha o subrayado CADA término dentro del paréntesis.",
        "Paso 3: Invierte uno a uno el signo de cada término marcado.",
        "Paso 4: Verifica que no quedó ningún término sin invertir."
    ],
    "ejemplos": [
        {"titulo": "Todos o ninguno", "enunciado": "Elimina y simplifica: 8 - (2x - 5y + 3z - 1).", "solucion_pasos": ["-(+2x) = -2x.", "-(-5y) = +5y.", "-(+3z) = -3z.", "-(-1) = +1.", "Resultado: 8 - 2x + 5y - 3z + 1 = 9 - 2x + 5y - 3z."]}
    ],
    "errores_frecuentes": [
        "Invertir solo el signo del primer término interior.",
        "Invertir los signos de los términos negativos y dejar los positivos 'porque ya son positivos'."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-ES-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al eliminar el paréntesis en $10 - (4a - 2b + c)$, un alumno obtiene $10 - 4a - 2b + c$. ¿Cuál fue su error? (v{i})", "choices": ["A) Invirtió el signo del primer término ($+4a$ a $-4a$) pero olvidó invertir el signo del segundo término ($-2b$ debería ser $+2b$).", "B) No invirtió ningún signo.", "C) Invirtió los signos de forma correcta.", "D) Sumó todos los coeficientes en lugar de restar."], "correct_answer": "A) Invirtió el signo del primer término ($+4a$ a $-4a$) pero olvidó invertir el signo del segundo término ($-2b$ debería ser $+2b$).", "solution_steps": "La respuesta correcta es $10-4a+2b-c$. El $-$ externo invierte absolutamente todos los signos.", "paes_style": False})
EJERCICIOS.append({"stable_id": "AGR-ES-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Elimina correctamente: $15 - (6m - 3n + 2)$.", "choices": ["A) $13 - 6m + 3n$", "B) $13 - 6m - 3n$", "C) $17 - 6m + 3n$", "D) $17 + 6m - 3n$"], "correct_answer": "A) $13 - 6m + 3n$", "solution_steps": "Invertimos todo: $15 - 6m + 3n - 2$. Constantes: $15-2=13$. Resultado: $13-6m+3n$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-ES-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿Es correcto que $-(a - b + c - d) = -a + b - c + d$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Cada signo se invierte: $-(+a)=-a$, $-(-b)=+b$, $-(+c)=-c$, $-(-d)=+d$. Resultado correcto.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-ES-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Un ingeniero debe calcular el material sobrante tras descontar el desperdicio: $M = 100 - (15t - 5 + 3w)$. ¿Cuál es la expresión simplificada del material disponible? (v{i})", "choices": ["A) $105 - 15t - 3w$", "B) $95 - 15t - 3w$", "C) $105 + 15t - 3w$", "D) $105 - 15t + 3w$"], "correct_answer": "A) $105 - 15t - 3w$", "solution_steps": "Invertimos: $-(+15t)=-15t$, $-(-5)=+5$, $-(+3w)=-3w$. Queda: $100-15t+5-3w = 105-15t-3w$.", "paes_style": True})

# 3. SUSTRACCION_POL.CAMBIO_PARCIAL_SIGNO
sid3 = "MAT.ALG.SUSTRACCION_POL.CAMBIO_PARCIAL_SIGNO"
RECURSOS.append({
    "semantic_id": sid3,
    "objetivo": "Reconocer y evitar el error de cambio parcial de signo en la sustracción de polinomios.",
    "introduccion": "Similar al error del signo negativo, pero en el contexto de la sustracción de polinomios completos. Aquí el error sucede cuando se cambia solo el signo de algunos términos del sustraendo, no de todos.",
    "resumen": "El **Cambio Parcial de Signo** es el error de invertir el signo de solo una parte de los términos del sustraendo al restar un polinomio. La regla de la sustracción exige invertir TODOS los signos del sustraendo, sin excepción.",
    "explicacion": "Calculemos $(7a + 3b - 2) - (4a - b + 5)$.\n\nOpuesto correcto del sustraendo $(4a - b + 5)$:\n$(-4a + b - 5)$.\n\nSuma correcta:\n$(7a + 3b - 2) + (-4a + b - 5) = 3a + 4b - 7$.\n\nError de cambio parcial (solo cambia el primer término):\n$(7a + 3b - 2) + (-4a - b + 5) = 3a + 2b + 3$ ← ¡MAL!\n\nDiferencia: El $-b$ del sustraendo debía convertirse en $+b$, pero al hacerlo parcialmente quedó como $-b$.",
    "procedimiento": [
        "Paso 1: Escribe el sustraendo completo.",
        "Paso 2: Identifica cuántos términos tiene. Cuenta: 1, 2, 3...",
        "Paso 3: Invierte el signo de CADA UNO de ellos, uno por uno.",
        "Paso 4: Verifica la cantidad: el opuesto debe tener exactamente el mismo número de términos."
    ],
    "ejemplos": [
        {"titulo": "El cambio incompleto", "enunciado": "Detecta el error: (10x - 4y) - (3x - 2y) = 10x - 4y - 3x - 2y = 7x - 6y.", "solucion_pasos": ["El sustraendo es (3x - 2y).", "Su opuesto es (-3x + 2y).", "El cálculo erróneo convirtió -2y en -2y en lugar de +2y.", "Resultado correcto: 10x - 4y - 3x + 2y = 7x - 2y."]}
    ],
    "errores_frecuentes": [
        "Invertir los signos de los términos con coeficiente grande y 'olvidar' el último término.",
        "Confundir el sustraendo con el minuendo al decidir cuál se invierte."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-CPS-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al realizar $(8m + 2n) - (3m - n + 4)$, un alumno obtiene $5m + n + 4$ invirtiendo parcialmente. ¿Cuál es el resultado correcto? (v{i})", "choices": ["A) $5m + 3n - 4$", "B) $5m + n + 4$", "C) $5m - n - 4$", "D) $11m + 3n + 4$"], "correct_answer": "A) $5m + 3n - 4$", "solution_steps": "Opuesto completo: $(-3m+n-4)$. Suma: $8m+2n-3m+n-4 = 5m+3n-4$. El alumno olvidó cambiar $-n$ a $+n$ y $+4$ a $-4$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "SUS-CPS-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Calcula correctamente: $(6p - 3q + 1) - (2p + q - 5)$.", "choices": ["A) $4p - 4q + 6$", "B) $4p - 4q - 6$", "C) $4p + 4q + 6$", "D) $4p - 2q + 6$"], "correct_answer": "A) $4p - 4q + 6$", "solution_steps": "Opuesto del sustraendo: $(-2p - q + 5)$. Suma: $6p-3q+1-2p-q+5 = 4p-4q+6$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-CPS-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿Al restar el trinomio $(a - b + c)$ de $(2a + 3b - c)$, el resultado es $a + 4b - 2c$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Opuesto: $(-a+b-c)$. Suma: $2a+3b-c-a+b-c = a+4b-2c$. El resultado es correcto.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-CPS-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Dos modelos de producción son $P_1 = 8k + 4l - 2$ y $P_2 = 3k - l + 7$. ¿Cuánto excede $P_1$ a $P_2$? (v{i})", "choices": ["A) $5k + 5l - 9$", "B) $5k - 5l - 9$", "C) $5k + 5l + 5$", "D) $5k + 3l - 9$"], "correct_answer": "A) $5k + 5l - 9$", "solution_steps": "Exceso = $P_1 - P_2 = (8k+4l-2)-(3k-l+7)$. Opuesto: $(-3k+l-7)$. Suma: $8k+4l-2-3k+l-7=5k+5l-9$.", "paes_style": True})

# 4. REDUCCION_OPERATIVA.IDENTIDADES_PREVIAS
sid4 = "MAT.ALG.REDUCCION_OPERATIVA.IDENTIDADES_PREVIAS"
RECURSOS.append({
    "semantic_id": sid4,
    "objetivo": "Usar identidades algebraicas simples para simplificar antes de reducir términos semejantes.",
    "introduccion": "A veces, antes de reducir, se puede aplicar una identidad algebraica conocida para reformular los términos y hacer la reducción más directa. Es como preparar los ingredientes antes de cocinar.",
    "resumen": "La estrategia de **Identidades Previas** consiste en reconocer si algún subgrupo de términos corresponde a una forma algebraica conocida (como $a + a = 2a$ o $a - a = 0$), aplicarla y simplificar el paso de reducción.",
    "explicacion": "Sea la expresión: $3n + (n + 2n) - 4n$.\n\nAntes de agrupar todo, notamos que dentro del paréntesis hay una reducción previa simple:\n$n + 2n = 3n$.\n\nAhora la expresión es: $3n + 3n - 4n$.\n\nReducimos: $6n - 4n = 2n$.\n\nOtra situación: reconocer que $(x - x)$ siempre da $0$ y eliminarlo antes de continuar, limpiando la expresión.",
    "procedimiento": [
        "Paso 1: Busca si hay subexpresiones que se pueden simplificar de inmediato (ej. término igual con mismo signo, o término que se cancela).",
        "Paso 2: Aplica esa simplificación previa.",
        "Paso 3: Con la expresión más simple, aplica la reducción estándar.",
        "Paso 4: Verifica que el resultado sea más simple que si hubieras ignorado las identidades."
    ],
    "ejemplos": [
        {"titulo": "El shortcut algebraico", "enunciado": "Reduce: 5x + (3x - 3x) + 2x.", "solucion_pasos": ["Identidad previa: 3x - 3x = 0.", "Expresión simplificada: 5x + 0 + 2x.", "Reducción: 5x + 2x = 7x."]}
    ],
    "errores_frecuentes": [
        "No notar la cancelación previa y realizar más operaciones de las necesarias.",
        "Aplicar la identidad incorrectamente (ej. creer que $2x + 3x = 5x^2$ en lugar de $5x$)."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-IP-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"¿Cuál es la ventaja de reconocer la identidad $x - x = 0$ antes de reducir la expresión completa $4a + (x - x) + 3a$? (v{i})", "choices": ["A) Permite eliminar los términos $x$ de inmediato, reduciendo la expresión a $4a + 0 + 3a = 7a$ de forma más directa.", "B) No aporta ninguna ventaja, el proceso es el mismo.", "C) Permite multiplicar los coeficientes restantes.", "D) Cambia el valor final de la expresión."], "correct_answer": "A) Permite eliminar los términos $x$ de inmediato, reduciendo la expresión a $4a + 0 + 3a = 7a$ de forma más directa.", "solution_steps": "Las identidades previas funcionan como atajos que simplifican el proceso.", "paes_style": False})
EJERCICIOS.append({"stable_id": "RED-IP-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Simplifica usando identidades previas: $7b - 2b + (5b - 5b) - b$.", "choices": ["A) $4b$", "B) $9b$", "C) $4b + 5b$", "D) $-4b$"], "correct_answer": "A) $4b$", "solution_steps": "Identidad previa: $(5b - 5b) = 0$. Expresión queda: $7b - 2b - b$. Reducimos: $7-2-1 = 4b$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-IP-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿La expresión $3x + (4y - 4y) + 2z$ se simplifica directamente a $3x + 2z$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$(4y - 4y) = 0$. La expresión se reduce a $3x + 0 + 2z = 3x + 2z$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"RED-IP-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"El costo de producción se modela como $C = 3r + (2s - 2s) + 4r + (t - t) - r + 5$. Usando identidades previas, ¿cuál es la expresión simplificada? (v{i})", "choices": ["A) $6r + 5$", "B) $6r + 4s + 5$", "C) $7r + 5$", "D) $6r$"], "correct_answer": "A) $6r + 5$", "solution_steps": "$(2s-2s)=0$ y $(t-t)=0$. Quedan: $3r+4r-r+5$. Familia $r$: $3+4-1=6r$. Constante: $5$. Resultado: $6r+5$.", "paes_style": True})

# 5. SUSTRACCION_POL.INVERSO_ADITIVO_ABSTRACTO
sid5 = "MAT.ALG.SUSTRACCION_POL.INVERSO_ADITIVO_ABSTRACTO"
RECURSOS.append({
    "semantic_id": sid5,
    "objetivo": "Comprender el inverso aditivo de un polinomio como concepto abstracto y verificar que $P + (-P) = 0$.",
    "introduccion": "El inverso aditivo es el concepto que formalmente explica qué significa 'el opuesto de un polinomio'. No es solo cambiar signos — es una operación con identidad teórica: cualquier polinomio sumado con su inverso aditivo siempre produce cero.",
    "resumen": "El **Inverso Aditivo** de un polinomio $P$ es el polinomio $-P$ tal que $P + (-P) = 0$ (el polinomio cero). Este concepto es la base formal de la sustracción algebraica, ya que $A - B = A + (-B)$.",
    "explicacion": "Definición formal: El elemento neutro de la suma polinómica es el polinomio cero ($0$). Para cada polinomio $P$, existe un único polinomio $-P$ (su inverso aditivo) tal que:\n$P + (-P) = 0$.\n\nEjemplo concreto: Si $P = ax^2 + bx + c$, entonces:\n$-P = -ax^2 - bx - c$.\nY efectivamente: $(ax^2 + bx + c) + (-ax^2 - bx - c) = 0$.\n\nEsto fundamenta por qué restar un polinomio equivale a sumar su inverso aditivo:\n$Q - P = Q + (-P)$.",
    "procedimiento": [
        "Paso 1: Dado un polinomio $P$, define $-P$ invirtiendo el signo de cada término.",
        "Paso 2: Suma $P + (-P)$ para verificar que el resultado sea el polinomio cero.",
        "Paso 3: Usa esta equivalencia para transformar cualquier sustracción en suma: $A - B = A + (-B)$.",
        "Paso 4: Resuelve la suma resultante aplicando reducción de semejantes."
    ],
    "ejemplos": [
        {"titulo": "El neutralizador algebraico", "enunciado": "Verifica que P = 2x - 3 es el inverso aditivo de Q = -2x + 3.", "solucion_pasos": ["P + Q = (2x - 3) + (-2x + 3).", "Familia x: 2x - 2x = 0.", "Constante: -3 + 3 = 0.", "Resultado: 0. Confirmado: son inversos aditivos."]}
    ],
    "errores_frecuentes": [
        "Confundir el inverso aditivo ($-P$, que suma y da cero) con el inverso multiplicativo ($\\frac{1}{P}$, que multiplica y da uno).",
        "Creer que el inverso aditivo solo existe para monomios, no para polinomios con múltiples términos."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-IA-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"¿Cuál es el inverso aditivo del polinomio $-5x^2 + 3x - 8$? (v{i})", "choices": ["A) $5x^2 - 3x + 8$", "B) $-5x^2 + 3x - 8$ (el mismo)", "C) $\\frac{1}{-5x^2+3x-8}$", "D) $5x^2 + 3x + 8$"], "correct_answer": "A) $5x^2 - 3x + 8$", "solution_steps": "El inverso aditivo se obtiene invirtiendo todos los signos: $-(-5x^2)=+5x^2$, $-(+3x)=-3x$, $-(-8)=+8$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "SUS-IA-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "¿Qué resultado siempre produce la operación $P + (-P)$ para cualquier polinomio $P$?", "choices": ["A) El polinomio cero ($0$).", "B) El doble del polinomio ($2P$).", "C) El polinomio $P$ mismo.", "D) El número $1$."], "correct_answer": "A) El polinomio cero ($0$).", "solution_steps": "Por definición del inverso aditivo, $P + (-P) = 0$ siempre, para cualquier polinomio.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-IA-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿La sustracción de polinomios $A - B$ puede expresarse equivalentemente como $A + (-B)$, donde $(-B)$ es el inverso aditivo de $B$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Esta es precisamente la definición formal de la sustracción: restar $B$ es sumar el inverso aditivo de $B$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-IA-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"En ingeniería de control, un sistema está en equilibrio cuando la señal de entrada $E$ y su inverso aditivo se anulan. Si $E = 4v - 3w + 1$, ¿cuál debe ser la señal de contrarresto para lograr el equilibrio? (v{i})", "choices": ["A) $-4v + 3w - 1$", "B) $4v - 3w + 1$", "C) $4v + 3w - 1$", "D) $-4v - 3w - 1$"], "correct_answer": "A) $-4v + 3w - 1$", "solution_steps": "El inverso aditivo de $E = 4v - 3w + 1$ es $-E = -4v + 3w - 1$. Verificamos: $E + (-E) = 0$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 6 (B0303/final)...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"  Creado {filename}.yaml")
    print("Escribiendo JSONL Tanda 6...")
    append_jsonl("mat-alg-operaciones-banco-gen-6", EJERCICIOS)
    print(f"  mat-alg-operaciones-banco-gen-6.jsonl con {len(EJERCICIOS)} ejercicios.")

if __name__ == "__main__":
    generate_all()

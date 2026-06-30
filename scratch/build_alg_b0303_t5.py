# scratch/build_alg_b0303_t5.py
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

# 1. SUSTRACCION_POL.POLINOMIO_OPUESTO
sid1 = "MAT.ALG.SUSTRACCION_POL.POLINOMIO_OPUESTO"
RECURSOS.append({
    "semantic_id": sid1,
    "objetivo": "Obtener el polinomio opuesto de un polinomio dado, invirtiendo todos sus signos.",
    "introduccion": "El opuesto de un número es el que sumado con él da cero: el opuesto de $5$ es $-5$. En álgebra, el opuesto de un polinomio completo es el polinomio con todos sus coeficientes con signo invertido.",
    "resumen": "El **Polinomio Opuesto** de $P(x)$ es $-P(x)$: se obtiene invirtiendo el signo de cada uno de los términos del polinomio original.",
    "explicacion": "Si $P = 3x^2 - 5x + 2$, entonces:\n$-P = -3x^2 + 5x - 2$.\n\nCada término cambia de signo:\n- $+3x^2 \\rightarrow -3x^2$.\n- $-5x \\rightarrow +5x$.\n- $+2 \\rightarrow -2$.\n\nImportante: Si sumamos un polinomio con su opuesto, obtenemos $0$: $P + (-P) = 0$.",
    "procedimiento": [
        "Paso 1: Escribe el polinomio original.",
        "Paso 2: Invierte el signo de cada término: $+$ pasa a $-$ y $-$ pasa a $+$.",
        "Paso 3: Verifica que el grado del polinomio opuesto sea el mismo.",
        "Paso 4: Confirma que $P + (-P) = 0$ sumando ambos."
    ],
    "ejemplos": [
        {"titulo": "El gemelo inverso", "enunciado": "Encuentra el opuesto de Q = -4a + 2b - 1.", "solucion_pasos": ["-Q = +4a - 2b + 1.", "Verificación: Q + (-Q) = (-4a+2b-1) + (4a-2b+1) = 0."]}
    ],
    "errores_frecuentes": [
        "Invertir el signo solo del primer término y dejar los demás intactos.",
        "Confundir el opuesto aditivo con el inverso multiplicativo (recíproco)."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-OP-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es el polinomio opuesto de $5x^2 - 3x + 7$? (v{i})", "choices": ["A) $-5x^2 + 3x - 7$", "B) $-5x^2 - 3x + 7$", "C) $5x^2 + 3x - 7$", "D) $-5x^2 + 3x + 7$"], "correct_answer": "A) $-5x^2 + 3x - 7$", "solution_steps": "Invertimos cada signo: $+5x^2 \\to -5x^2$, $-3x \\to +3x$, $+7 \\to -7$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "SUS-OP-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si $P = 6m - 4n + 2$, ¿cuál es $-P$?", "choices": ["A) $-6m + 4n - 2$", "B) $6m + 4n - 2$", "C) $-6m - 4n - 2$", "D) $6m - 4n - 2$"], "correct_answer": "A) $-6m + 4n - 2$", "solution_steps": "Invertimos cada signo: $6m \\to -6m$, $-4n \\to +4n$, $+2 \\to -2$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-OP-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿La suma de un polinomio y su opuesto es siempre igual a $0$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Por definición de opuesto aditivo: $P + (-P) = 0$. Cada par de términos se cancela.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-OP-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"En física, si la fuerza neta sobre un objeto es $F = 3v - 8$ y se le aplica una fuerza de reacción opuesta $-F$, ¿cuál es la fuerza resultante? (v{i})", "choices": ["A) $0$", "B) $6v - 16$", "C) $-6v + 16$", "D) $3v + 8$"], "correct_answer": "A) $0$", "solution_steps": "$F + (-F) = (3v-8) + (-3v+8) = 0$. La fuerza de reacción exacta cancela la fuerza original.", "paes_style": True})

# 2. SUSTRACCION_POL.METODO_VERTICAL
sid2 = "MAT.ALG.SUSTRACCION_POL.METODO_VERTICAL"
RECURSOS.append({
    "semantic_id": sid2,
    "objetivo": "Restar polinomios mediante el método vertical, convirtiendo la resta en suma del opuesto.",
    "introduccion": "En aritmética, restar es sumar el opuesto: $9 - 4 = 9 + (-4)$. En álgebra aplica exactamente lo mismo. Para restar verticalmente, convertimos el sustraendo en su opuesto y sumamos.",
    "resumen": "En la **Sustracción Vertical**, se escribe el minuendo arriba y el sustraendo debajo. Luego se invierte el signo de todos los términos del sustraendo y se realiza la suma columna por columna.",
    "explicacion": "Resta: $(5x^2 + 3x - 2) - (2x^2 - x + 4)$.\n\nFormato vertical:\n```\n  5x² + 3x - 2\n- 2x² -  x + 4\n─────────────\n```\n\nInvertimos los signos del sustraendo:\n```\n  5x² + 3x - 2\n+ (-2x²+ x - 4)\n─────────────\n  3x² + 4x - 6\n```\n\nResultado: $3x^2 + 4x - 6$.",
    "procedimiento": [
        "Paso 1: Escribe el minuendo en la primera fila.",
        "Paso 2: Escribe el sustraendo debajo, alineando términos semejantes.",
        "Paso 3: Invierte el signo de CADA término del sustraendo.",
        "Paso 4: Suma columna por columna como en la adición."
    ],
    "ejemplos": [
        {"titulo": "Restar cambiando de bando", "enunciado": "Resta: (7a + 5) - (3a - 2).", "solucion_pasos": ["Invertimos el sustraendo: -3a+2 → +3a+2... espera, el signo de 3a es + entonces su opuesto es -3a... ya es -3a+2... aquí ponemos +(-3a+2).", "Corregimos: sustraendo original (3a - 2). Opuesto: (-3a + 2).", "Suma: (7a+5) + (-3a+2) = 4a + 7."]}
    ],
    "errores_frecuentes": [
        "Invertir solo el signo del primer término del sustraendo.",
        "Confundir el minuendo con el sustraendo (restar al revés)."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-V-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al restar $(8x - 3) - (5x + 2)$ por el método vertical, ¿qué se hace con el sustraendo $(5x + 2)$ antes de sumar? (v{i})", "choices": ["A) Se invierte el signo de todos sus términos, convirtiéndolo en $(-5x - 2)$.", "B) Se deja igual y se suma directamente.", "C) Se multiplica por $-1$ solo el primer término.", "D) Se eleva al cuadrado cada coeficiente."], "correct_answer": "A) Se invierte el signo de todos sus términos, convirtiéndolo en $(-5x - 2)$.", "solution_steps": "Restar es sumar el opuesto. Invertimos todos los signos del sustraendo.", "paes_style": False})
EJERCICIOS.append({"stable_id": "SUS-V-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Resta verticalmente: $(6n^2 + 4n - 1) - (2n^2 - n + 3)$.", "choices": ["A) $4n^2 + 5n - 4$", "B) $4n^2 - 5n - 4$", "C) $4n^2 + 5n + 2$", "D) $8n^2 + 3n + 2$"], "correct_answer": "A) $4n^2 + 5n - 4$", "solution_steps": "Opuesto del sustraendo: $-2n^2+n-3$. Sumamos: $n^2: 6-2=4$. $n: 4+1=5$. Constante: $-1-3=-4$. Resultado: $4n^2+5n-4$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-V-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿La sustracción $(4x + 3) - (4x + 3)$ da siempre como resultado el polinomio cero?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Restar un polinomio consigo mismo: $(4x+3) + (-4x-3) = 0$. Cualquier polinomio menos sí mismo es cero.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-V-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"El ingreso de una empresa en el primer semestre fue $I = 10000p + 500$ y sus gastos fueron $G = 7000p - 200$. ¿Cuál es la utilidad neta (Ingreso - Gastos)? (v{i})", "choices": ["A) $3000p + 700$", "B) $3000p - 700$", "C) $17000p + 300$", "D) $3000p + 300$"], "correct_answer": "A) $3000p + 700$", "solution_steps": "Utilidad $= I - G = (10000p+500) - (7000p-200)$. Opuesto de $G$: $-7000p+200$. Suma: $(10000-7000)p + (500+200) = 3000p+700$.", "paes_style": True})

# 3. SUSTRACCION_POL.COEFICIENTES_FRACCIONARIOS
sid3 = "MAT.ALG.SUSTRACCION_POL.COEFICIENTES_FRACCIONARIOS"
RECURSOS.append({
    "semantic_id": sid3,
    "objetivo": "Restar polinomios con coeficientes fraccionarios, combinando la inversión de signos con la resta de fracciones.",
    "introduccion": "La resta de polinomios con fracciones combina dos habilidades: la inversión de signos del sustraendo y la operatoria con fracciones. Bien ordenadas, ambas son completamente manejables.",
    "resumen": "En la **Sustracción con Coeficientes Fraccionarios**, primero se transforma la resta en suma del opuesto (invirtiendo signos del sustraendo), y luego se suman los coeficientes fraccionarios de cada familia usando denominador común.",
    "explicacion": "Resta: $(\\frac{3}{4}x + \\frac{1}{2}) - (\\frac{1}{4}x - \\frac{1}{3})$.\n\nConvertimos en suma del opuesto:\n$(\\frac{3}{4}x + \\frac{1}{2}) + (-\\frac{1}{4}x + \\frac{1}{3})$.\n\nFamilia $x$: $\\frac{3}{4} - \\frac{1}{4} = \\frac{2}{4} = \\frac{1}{2}$.\nConstantes: $\\frac{1}{2} + \\frac{1}{3} = \\frac{3}{6} + \\frac{2}{6} = \\frac{5}{6}$.\n\nResultado: $\\frac{1}{2}x + \\frac{5}{6}$.",
    "procedimiento": [
        "Paso 1: Invierte el signo de cada término del sustraendo (convierte la resta en suma).",
        "Paso 2: Agrupa por familias de términos semejantes.",
        "Paso 3: Para cada familia, suma o resta las fracciones con denominador común.",
        "Paso 4: Simplifica las fracciones del resultado si es posible."
    ],
    "ejemplos": [
        {"titulo": "Fracciones de restar", "enunciado": "Calcula: (2/3)a - (1/6)a.", "solucion_pasos": ["Suma del opuesto: (2/3)a + (-1/6)a.", "MCD de 3 y 6 es 6.", "2/3 = 4/6.", "4/6 - 1/6 = 3/6 = 1/2.", "Resultado: (1/2)a."]}
    ],
    "errores_frecuentes": [
        "Olvidar invertir el signo del sustraendo antes de sumar las fracciones.",
        "Operar las fracciones sin buscar el denominador común."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-CF-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al calcular $(\\frac{{3}}{{5}})m - (\\frac{{1}}{{5}})m$, ¿cuál es el primer paso? (v{i})", "choices": ["A) Convertir la resta en suma del opuesto: $(\\frac{3}{5})m + (-\\frac{1}{5})m$.", "B) Multiplicar numeradores y denominadores.", "C) Restar directamente: $\\frac{3-1}{5-5} = \\frac{2}{0}$.", "D) Elevar al cuadrado ambas fracciones."], "correct_answer": "A) Convertir la resta en suma del opuesto: $(\\frac{3}{5})m + (-\\frac{1}{5})m$.", "solution_steps": "La resta siempre se convierte en suma del opuesto primero.", "paes_style": False})
EJERCICIOS.append({"stable_id": "SUS-CF-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Calcula: $(\\frac{5}{6})x - (\\frac{1}{4})x$.", "choices": ["A) $\\frac{7}{12}x$", "B) $\\frac{4}{2}x$", "C) $\\frac{1}{2}x$", "D) $\\frac{4}{24}x$"], "correct_answer": "A) $\\frac{7}{12}x$", "solution_steps": "MCD de 6 y 4 es 12. $\\frac{5}{6}=\\frac{10}{12}$, $\\frac{1}{4}=\\frac{3}{12}$. Restamos: $\\frac{10-3}{12}=\\frac{7}{12}$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-CF-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿La sustracción $\\frac{1}{2}x - \\frac{1}{2}x$ resulta en $\\frac{1}{4}x$?", "choices": [], "correct_answer": "Falso", "solution_steps": "Son semejantes con el mismo coeficiente. Resta: $\\frac{1}{2} - \\frac{1}{2} = 0$. El resultado es $0$, no $\\frac{1}{4}x$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-CF-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Una receta requiere $\\frac{{3}}{{4}}$ kg de harina del tipo A. Ya se usaron $\\frac{{1}}{{3}}$ kg. ¿Cuánto queda por agregar? (v{i})", "choices": ["A) $\\frac{5}{12}$ kg", "B) $\\frac{2}{1}$ kg", "C) $\\frac{2}{7}$ kg", "D) $\\frac{1}{6}$ kg"], "correct_answer": "A) $\\frac{5}{12}$ kg", "solution_steps": "MCD de 4 y 3 es 12. $\\frac{3}{4}=\\frac{9}{12}$, $\\frac{1}{3}=\\frac{4}{12}$. Resta: $\\frac{9-4}{12}=\\frac{5}{12}$.", "paes_style": True})

# 4. SUSTRACCION_POL.OPERACION_COMBINADA
sid4 = "MAT.ALG.SUSTRACCION_POL.OPERACION_COMBINADA"
RECURSOS.append({
    "semantic_id": sid4,
    "objetivo": "Resolver expresiones algebraicas que combinan adición y sustracción de varios polinomios.",
    "introduccion": "Las operaciones algebraicas rara vez se presentan de una en una. En una expresión real, puede haber que sumar y restar varios polinomios en secuencia. La clave es resolver en orden, convirtiendo siempre las restas en sumas del opuesto.",
    "resumen": "En una **Operación Combinada** con polinomios, se procesa cada signo entre ellos: los $+$ no alteran los signos interiores, los $-$ invierten todos los signos del polinomio que sigue.",
    "explicacion": "Simplifica: $(3x^2 - x) + (x^2 + 4) - (2x^2 - 3x + 1)$.\n\nEliminamos los agrupadores con sus reglas:\n- El $+$ no cambia nada: $3x^2 - x + x^2 + 4$.\n- El $-$ invierte el último: $-2x^2 + 3x - 1$.\n\nJuntos: $3x^2 - x + x^2 + 4 - 2x^2 + 3x - 1$.\n\nReducimos por familias:\n- $x^2$: $3 + 1 - 2 = 2x^2$.\n- $x$: $-1 + 3 = 2x$.\n- Constante: $4 - 1 = 3$.\n\nResultado: $2x^2 + 2x + 3$.",
    "procedimiento": [
        "Paso 1: Identifica todos los signos que preceden a cada paréntesis.",
        "Paso 2: Elimina los paréntesis: conserva los signos si el exterior es $+$, invierte si es $-$.",
        "Paso 3: Agrupa por familias.",
        "Paso 4: Reduce cada familia."
    ],
    "ejemplos": [
        {"titulo": "El combo algebraico", "enunciado": "Simplifica: (5a + 3) - (2a - 1) + (a + 4).", "solucion_pasos": ["+ (5a+3): 5a+3.", "- (2a-1): -2a+1.", "+ (a+4): a+4.", "Junto: 5a+3-2a+1+a+4.", "Familia a: 5-2+1=4a. Constante: 3+1+4=8.", "Resultado: 4a+8."]}
    ],
    "errores_frecuentes": [
        "Al haber múltiples signos externos, invertir solo los del primer signo negativo y olvidar los siguientes.",
        "No reducir completamente, dejando términos semejantes sin agrupar en el resultado."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-OC-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"En la expresión $(A) + (B) - (C)$, donde A, B y C son polinomios, ¿qué le ocurre a los términos de C al eliminar el paréntesis? (v{i})", "choices": ["A) Todos sus signos se invierten, porque el signo exterior es $-$.", "B) Sus signos se conservan igual que los de A y B.", "C) Se multiplican por el coeficiente de B.", "D) No cambia nada porque los paréntesis no afectan signos."], "correct_answer": "A) Todos sus signos se invierten, porque el signo exterior es $-$.", "solution_steps": "El signo $-$ exterior al paréntesis de C actúa como distribuidor, invirtiendo todos sus signos internos.", "paes_style": False})
EJERCICIOS.append({"stable_id": "SUS-OC-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Simplifica: $(4m^2 + 3m - 1) - (m^2 - 2m + 5) + (2m^2 - m)$.", "choices": ["A) $5m^2 + 4m - 6$", "B) $5m^2 - 4m - 6$", "C) $5m^2 + 4m + 6$", "D) $3m^2 + 4m - 6$"], "correct_answer": "A) $5m^2 + 4m - 6$", "solution_steps": "Eliminamos paréntesis: $4m^2+3m-1-m^2+2m-5+2m^2-m$. $m^2$: $4-1+2=5$. $m$: $3+2-1=4$. Cte: $-1-5=-6$. Resultado: $5m^2+4m-6$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-OC-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿La operación $(2x + 1) + (x - 3) - (3x - 2)$ resulta en $0$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Eliminamos: $2x+1+x-3-3x+2$. $x$: $2+1-3=0$. Cte: $1-3+2=0$. Resultado: $0$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-OC-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"El saldo de una cuenta bancaria se modifica: al saldo inicial $S = 5000t$ se suma el depósito $(2000t + 300)$ y se restan los retiros $(3000t - 100)$. ¿Cuál es el saldo final? (v{i})", "choices": ["A) $4000t + 400$", "B) $4000t - 400$", "C) $10000t + 400$", "D) $4000t + 200$"], "correct_answer": "A) $4000t + 400$", "solution_steps": "$S = 5000t + (2000t+300) - (3000t-100)$. Eliminamos: $5000t+2000t+300-3000t+100$. $t$: $5000+2000-3000=4000t$. Cte: $300+100=400$. Resultado: $4000t+400$.", "paes_style": True})

# 5. SUSTRACCION_POL.OMISION_PARENTESIS
sid5 = "MAT.ALG.SUSTRACCION_POL.OMISION_PARENTESIS"
RECURSOS.append({
    "semantic_id": sid5,
    "objetivo": "Identificar y corregir el error clásico de omitir la inversión de signos al restar un polinomio sin paréntesis.",
    "introduccion": "Uno de los errores más frecuentes en álgebra es olvidar los paréntesis al restar un polinomio. Sin ellos, el signo menos solo afecta al primer término, dejando el resto sin cambio — un error silencioso pero devastador.",
    "resumen": "La **Omisión de Paréntesis** en la sustracción genera el error de aplicar el signo $-$ solo al primer término del sustraendo y dejar los siguientes inalterados. El paréntesis es obligatorio para que el signo menos actúe sobre toda la expresión.",
    "explicacion": "Error clásico: Calcular $5x - 3x + 2$ creyendo que es $(5x) - (3x + 2)$.\n\nSin paréntesis, la expresión es: $5x - 3x + 2 = 2x + 2$.\nCon paréntesis: $5x - (3x + 2) = 5x - 3x - 2 = 2x - 2$.\n\nDos resultados distintos. La diferencia: el signo $-$ con paréntesis invierte TODOS los signos del polinomio restado, incluyendo el $+2$ final.",
    "procedimiento": [
        "Paso 1: Cuando vayas a restar un polinomio de más de un término, SIEMPRE usa paréntesis.",
        "Paso 2: Verifica que el signo $-$ esté justo antes del paréntesis que abre.",
        "Paso 3: Al eliminar el paréntesis, invierte TODOS los signos interiores.",
        "Paso 4: Si ves una resta escrita sin paréntesis, pregúntate: ¿el $-$ solo afecta al primer término o a todos?"
    ],
    "ejemplos": [
        {"titulo": "El error oculto", "enunciado": "¿Son iguales las expresiones: (A) 8a - 2a + 5 y (B) 8a - (2a + 5)?", "solucion_pasos": ["Expresión A: solo se resta 2a, el +5 queda intacto → 6a + 5.", "Expresión B: se resta el binomio completo → 8a - 2a - 5 = 6a - 5.", "Son DISTINTAS. La diferencia está en si el signo - afecta al +5 o no."]}
    ],
    "errores_frecuentes": [
        "Omitir el paréntesis al escribir una resta de un binomio o trinomio.",
        "Aplicar la inversión de signos solo al primer término y dejar los demás sin cambio."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-OP2-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"¿En cuál de las siguientes situaciones se comete el error de omisión de paréntesis? (v{i})", "choices": ["A) Escribir $10 - 2x + 3$ cuando en realidad se quería expresar $10 - (2x + 3)$.", "B) Escribir $10 - (2x + 3)$ y luego invertir todos los signos.", "C) Usar el paréntesis correctamente en $10 - (2x + 3) = 7 - 2x$.", "D) Sumar polinomios sin paréntesis."], "correct_answer": "A) Escribir $10 - 2x + 3$ cuando en realidad se quería expresar $10 - (2x + 3)$.", "solution_steps": "Sin paréntesis, el $-$ solo afecta al $2x$. El $+3$ queda positivo cuando debería ser $-3$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "SUS-OP2-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "¿Cuál es el resultado correcto de $9b - (4b - 7)$?", "choices": ["A) $5b + 7$", "B) $5b - 7$", "C) $13b - 7$", "D) $5b$"], "correct_answer": "A) $5b + 7$", "solution_steps": "Invertimos el sustraendo: $-(4b-7) = -4b+7$. Sumamos: $9b-4b+7=5b+7$. El $-7$ del sustraendo se convierte en $+7$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-OP2-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿Las expresiones $7 - x + 4$ y $7 - (x + 4)$ son equivalentes?", "choices": [], "correct_answer": "Falso", "solution_steps": "Expresión 1: $7 - x + 4 = 11 - x$. Expresión 2: $7 - x - 4 = 3 - x$. No son equivalentes porque en la segunda el $-$ invierte el signo del $4$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"SUS-OP2-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Un estudiante calcula el descuento de un precio así: $P = 1000 - 200r + 50$, pero el enunciado decía que el descuento era $(200r + 50)$. ¿Cuál es el resultado real? (v{i})", "choices": ["A) $950 - 200r$", "B) $1050 - 200r$", "C) $950 + 200r$", "D) $1000 - 200r$"], "correct_answer": "A) $950 - 200r$", "solution_steps": "El descuento correcto: $P = 1000 - (200r + 50) = 1000 - 200r - 50 = 950 - 200r$. Sin paréntesis, el estudiante habría obtenido $1050 - 200r$, un error de $\\$100$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 5 (B0303/Sustraccion Polinomios)...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"  Creado {filename}.yaml")
    print("Escribiendo JSONL Tanda 5...")
    append_jsonl("mat-alg-operaciones-banco-gen-5", EJERCICIOS)
    print(f"  mat-alg-operaciones-banco-gen-5.jsonl con {len(EJERCICIOS)} ejercicios.")

if __name__ == "__main__":
    generate_all()

# scratch/build_alg_b0303_t3.py
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

# 1. AGRUPACION.SIGNOS_AGRUPACION
sid1 = "MAT.ALG.AGRUPACION.SIGNOS_AGRUPACION"
RECURSOS.append({
    "semantic_id": sid1,
    "objetivo": "Reconocer los distintos signos de agrupación y su función en una expresión algebraica.",
    "introduccion": "Los signos de agrupación son los 'cajones' del álgebra. Indican qué operaciones deben hacerse primero y protegen a un conjunto de términos del exterior.",
    "resumen": "Los **Signos de Agrupación** son el paréntesis $()$, el corchete $[]$ y la llave $\\{\\}$. Todos cumplen la misma función: agrupar términos para que se calculen antes que las operaciones externas.",
    "explicacion": "Cuando una expresión tiene signos de agrupación anidados, la convención matemática indica resolverlos de adentro hacia afuera:\n1. Primero los **paréntesis** $(...)$.\n2. Luego los **corchetes** $[...]$.\n3. Finalmente las **llaves** $\\{...\\}$.\n\nEjemplo de lectura: $\\{3[2(x+1) - 4] + 5\\}$\n- El paréntesis contiene $x+1$ → se opera primero.\n- El corchete contiene todo lo que resulte de ese paréntesis más el $-4$.\n- La llave envuelve todo lo anterior más el $+5$.",
    "procedimiento": [
        "Paso 1: Localiza el signo de agrupación más interior (usualmente un paréntesis).",
        "Paso 2: Realiza las operaciones que contiene ese grupo.",
        "Paso 3: Sustituye el signo de agrupación y su contenido por el resultado.",
        "Paso 4: Repite el proceso con el siguiente signo de agrupación hacia afuera."
    ],
    "ejemplos": [
        {"titulo": "Cajones dentro de cajones", "enunciado": "Identifica el orden de resolución en: {5[3(a - 2) + 1] - 4}.", "solucion_pasos": ["Nivel 1 (paréntesis): (a - 2).", "Nivel 2 (corchete): [resultado × 3 + 1].", "Nivel 3 (llave): {resultado × 5 - 4}.", "Siempre desde adentro hacia afuera."]}
    ],
    "errores_frecuentes": [
        "Resolver de afuera hacia adentro en lugar de adentro hacia afuera.",
        "Confundir el tipo de agrupador creyendo que paréntesis y corchetes son operadores distintos cuando en el álgebra clásica son equivalentes."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SA-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En la expresión $\\{{2[3(x+1) - 5] + 4\\}}$, ¿en qué orden deben eliminarse los signos de agrupación? (v{i})", "choices": ["A) Primero el paréntesis, luego el corchete, finalmente la llave (de adentro hacia afuera).", "B) Primero la llave, luego el corchete, finalmente el paréntesis.", "C) Pueden resolverse en cualquier orden.", "D) Solo el paréntesis, los otros son decorativos."], "correct_answer": "A) Primero el paréntesis, luego el corchete, finalmente la llave (de adentro hacia afuera).", "solution_steps": "La convención matemática universal establece resolución de adentro hacia afuera.", "paes_style": False})
EJERCICIOS.append({"stable_id": "AGR-SA-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "¿Cuál de los siguientes es el orden correcto de los signos de agrupación de más interior a más exterior?", "choices": ["A) Paréntesis, corchete, llave.", "B) Llave, corchete, paréntesis.", "C) Corchete, paréntesis, llave.", "D) Es indistinto."], "correct_answer": "A) Paréntesis, corchete, llave.", "solution_steps": "La convención clásica ubica paréntesis en el interior, luego corchetes, y llaves al exterior.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SA-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El paréntesis, el corchete y la llave realizan exactamente la misma función matemática de agrupación?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Los tres signos agrupan términos y obligan a que se resuelvan antes que el exterior. Se diferencian visualmente para evitar confusión en expresiones anidadas, pero su función algebraica es idéntica.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SA-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un programador escribe la expresión: $resultado = \\{{(a + b) \\cdot c\\}} - d$. Según las reglas de agrupación algebraica, ¿qué operación se realiza primero? (v{i})", "choices": ["A) La suma $(a+b)$ dentro del paréntesis.", "B) La multiplicación de $c$ por $a$.", "C) La resta de $d$.", "D) La suma de todos los términos."], "correct_answer": "A) La suma $(a+b)$ dentro del paréntesis.", "solution_steps": "El paréntesis es el agrupador más interior. Su contenido se resuelve primero.", "paes_style": True})

# 2. AGRUPACION.SUPRESION_SIGNO_MAS
sid2 = "MAT.ALG.AGRUPACION.SUPRESION_SIGNO_MAS"
RECURSOS.append({
    "semantic_id": sid2,
    "objetivo": "Eliminar paréntesis precedidos de signo más sin alterar los signos de los términos interiores.",
    "introduccion": "El signo más es neutral, como una ventana de vidrio: puedes ver a través de él sin que cambie nada. Eliminar un paréntesis con signo más delante es la operación más simple del álgebra.",
    "resumen": "Al **Suprimir un Signo Más** delante de un paréntesis, los términos dentro del paréntesis conservan exactamente sus signos originales. El paréntesis desaparece y los términos quedan 'expuestos' sin ningún cambio.",
    "explicacion": "Ejemplo: $5 + (3x - 2y + 4)$.\n\nEl paréntesis va precedido de $+$. Lo quitamos:\n$5 + 3x - 2y + 4$.\n\nLos signos de $3x$, $-2y$ y $+4$ son exactamente los mismos que tenían dentro del paréntesis. El $+$ exterior no cambió nada.\n\nAsí de simple: $+(A + B - C) = A + B - C$.",
    "procedimiento": [
        "Paso 1: Verifica que hay un signo $+$ inmediatamente antes del paréntesis.",
        "Paso 2: Elimina el signo $+$ y el paréntesis.",
        "Paso 3: Escribe los términos que estaban dentro con sus signos originales.",
        "Paso 4: Continúa simplificando si hay más agrupadores."
    ],
    "ejemplos": [
        {"titulo": "La ventana transparente", "enunciado": "Suprime el paréntesis: 8a + (3b - a + 2).", "solucion_pasos": ["El signo antes del paréntesis es +.", "Eliminamos el + y el paréntesis.", "Los términos salen tal cual: 3b - a + 2.", "Expresión completa: 8a + 3b - a + 2.", "Reducimos semejantes: 7a + 3b + 2."]}
    ],
    "errores_frecuentes": [
        "Cambiar los signos interiores aunque el signo exterior sea positivo (ej. escribir $-3b$ en lugar de $+3b$).",
        "Olvidar reducir los términos semejantes que quedan tras eliminar el paréntesis."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SMP-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al eliminar el paréntesis en la expresión $+(−4a + 3b − c)$, ¿qué ocurre con los signos de los términos interiores? (v{i})", "choices": ["A) Se conservan exactamente: $-4a + 3b - c$.", "B) Todos se invierten: $+4a - 3b + c$.", "C) Solo los negativos se invierten.", "D) Todos se vuelven positivos."], "correct_answer": "A) Se conservan exactamente: $-4a + 3b - c$.", "solution_steps": "Un signo + exterior actúa como un espejo transparente: los términos salen inalterados.", "paes_style": False})
EJERCICIOS.append({"stable_id": "AGR-SMP-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Simplifica: $7x + (2x - 5y + 3)$.", "choices": ["A) $9x - 5y + 3$", "B) $9x + 5y + 3$", "C) $5x - 5y + 3$", "D) $9x + 5y - 3$"], "correct_answer": "A) $9x - 5y + 3$", "solution_steps": "Eliminamos el paréntesis (precedido de +), signos sin cambio: $7x + 2x - 5y + 3$. Reducimos: $9x - 5y + 3$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SMP-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Es correcto afirmar que $3 + (-5x + 2)$ equivale a $3 - 5x + 2 = 5 - 5x$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "El $+$ delante del paréntesis no altera los signos interiores. $-5x$ sale como $-5x$ y $+2$ sale como $+2$. Luego se reducen las constantes: $3 + 2 = 5$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SMP-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un contador registra el ingreso de una empresa como $I = 10000 + (−3000 + 5000 − 2000)$. ¿Cuál es el ingreso neto total? (v{i})", "choices": ["A) $10000$", "B) $20000$", "C) $6000$", "D) $14000$"], "correct_answer": "A) $10000$", "solution_steps": "El $+$ exterior no altera los signos: $I = 10000 - 3000 + 5000 - 2000$. Positivos: $15000$. Negativos: $5000$. Neto: $10000$.", "paes_style": True})

# 3. AGRUPACION.SUPRESION_SIGNO_MENOS
sid3 = "MAT.ALG.AGRUPACION.SUPRESION_SIGNO_MENOS"
RECURSOS.append({
    "semantic_id": sid3,
    "objetivo": "Eliminar paréntesis precedidos de signo menos, invirtiendo los signos de todos los términos interiores.",
    "introduccion": "El signo menos es un espejo invertido. Cada vez que un paréntesis tiene un signo menos delante, es como si ese menos le dijera a todos los de adentro: 'Dense vuelta'. Los positivos se vuelven negativos y los negativos se vuelven positivos.",
    "resumen": "Al **Suprimir un Signo Menos** delante de un paréntesis, **todos** los términos dentro del paréntesis cambian de signo: los $+$ se vuelven $-$ y los $-$ se vuelven $+$.",
    "explicacion": "Ejemplo: $10 - (3x - 2y + 5)$.\n\nEl paréntesis va precedido de $-$. Este $-$ invierte todos los signos interiores:\n$10 - 3x + 2y - 5$.\n\n¿Por qué? Porque el $-$ exterior se 'distribuye' sobre cada término:\n$-(+3x) = -3x$.\n$-(-2y) = +2y$.\n$-(+5) = -5$.\n\nReducimos: $(10 - 5) - 3x + 2y = 5 - 3x + 2y$.",
    "procedimiento": [
        "Paso 1: Identifica el signo $-$ delante del paréntesis.",
        "Paso 2: Elimina el $-$ y el paréntesis.",
        "Paso 3: Invierte el signo de CADA término que estaba dentro: $+$ pasa a $-$ y $-$ pasa a $+$.",
        "Paso 4: Reescribe la expresión completa y reduce los términos semejantes."
    ],
    "ejemplos": [
        {"titulo": "El espejo invertidor", "enunciado": "Elimina el paréntesis: 6a - (4b - 2a + 1).", "solucion_pasos": ["Signo exterior: -.", "Invertimos cada signo interior:", "-4b → queda +4b... espera, el signo de 4b dentro era +4b, entonces queda -4b.", "No, analicemos: -(+4b) = -4b. -(-2a) = +2a. -(+1) = -1.", "Resultado sin paréntesis: 6a - 4b + 2a - 1.", "Reducimos: 8a - 4b - 1."]}
    ],
    "errores_frecuentes": [
        "Cambiar solo el signo del primer término y dejar los demás igual.",
        "Cambiar el signo del primer término y del paréntesis mismo, omitiendo los del interior."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SME-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Al eliminar el paréntesis en la expresión $-(+2x - 5y + 3z)$, ¿qué resultado se obtiene? (v{i})", "choices": ["A) $-2x + 5y - 3z$", "B) $-2x - 5y + 3z$", "C) $+2x - 5y + 3z$", "D) $+2x + 5y - 3z$"], "correct_answer": "A) $-2x + 5y - 3z$", "solution_steps": "El $-$ exterior invierte cada signo: $-(+2x)=-2x$, $-(-5y)=+5y$, $-(+3z)=-3z$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "AGR-SME-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Elimina el paréntesis y simplifica: $9b - (4b + 2 - b)$.", "choices": ["A) $6b - 2$", "B) $6b + 2$", "C) $12b - 2$", "D) $-6b + 2$"], "correct_answer": "A) $6b - 2$", "solution_steps": "Invertimos signos internos: $9b - 4b - 2 + b$. Reducimos familia $b$: $(9-4+1)b = 6b$. Constante: $-2$. Resultado: $6b - 2$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SME-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "media", "competencia": "M1", "prompt": "¿Al eliminar el paréntesis en $5 - (x - 3)$, la expresión resultante es $5 - x + 3 = 8 - x$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "El $-$ exterior invierte los signos: $-(+x)=-x$ y $-(-3)=+3$. Queda: $5 - x + 3 = 8 - x$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SME-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"La temperatura de un reactor se modela como $T = 80 - (15 - 5t + 2)$. ¿Cuál es la expresión simplificada? (v{i})", "choices": ["A) $63 + 5t$", "B) $63 - 5t$", "C) $97 + 5t$", "D) $97 - 5t$"], "correct_answer": "A) $63 + 5t$", "solution_steps": "Invertimos signos: $-(+15)=-15$, $-(-5t)=+5t$, $-(+2)=-2$. Queda: $80 - 15 + 5t - 2$. Constantes: $80-15-2=63$. Resultado: $63+5t$.", "paes_style": True})

# 4. AGRUPACION.SUPRESION_ANIDADA
sid4 = "MAT.ALG.AGRUPACION.SUPRESION_ANIDADA"
RECURSOS.append({
    "semantic_id": sid4,
    "objetivo": "Eliminar signos de agrupación anidados (paréntesis dentro de corchetes dentro de llaves) de adentro hacia afuera.",
    "introduccion": "Imagina unas muñecas rusas: hay que abrir la más pequeña de adentro primero para llegar a la de afuera. Los signos de agrupación anidados funcionan igual: el proceso es secuencial, de lo más interior a lo más exterior.",
    "resumen": "La **Supresión Anidada** requiere eliminar los agrupadores en orden estricto: primero paréntesis, luego corchetes, luego llaves. Cada eliminación puede requerir invertir o no los signos, dependiendo del signo que antecede a cada agrupador.",
    "explicacion": "Simplifica: $\\{5a - [3a - (2a + 1)]\\}$.\n\nPaso 1 — Eliminamos el paréntesis (precedido de $-$, invertimos):\n$\\{5a - [3a - 2a - 1]\\}$.\n\nPaso 2 — Reducimos lo que quedó en el corchete:\n$\\{5a - [a - 1]\\}$.\n\nPaso 3 — Eliminamos el corchete (precedido de $-$, invertimos):\n$\\{5a - a + 1\\}$.\n\nPaso 4 — Eliminamos la llave (precedida de nada o $+$, sin cambio):\n$5a - a + 1 = 4a + 1$.",
    "procedimiento": [
        "Paso 1: Identifica el agrupador más interior (paréntesis). Mira su signo exterior.",
        "Paso 2: Elimínalo, aplicando la regla correspondiente (+ conserva, - invierte).",
        "Paso 3: Reduce términos semejantes dentro del siguiente nivel.",
        "Paso 4: Repite para el corchete y luego para la llave."
    ],
    "ejemplos": [
        {"titulo": "Las tres capas", "enunciado": "Simplifica: {4b - [2b + (b - 3)]}.", "solucion_pasos": ["Paréntesis (precedido de +, sin cambio): {4b - [2b + b - 3]}.", "Reducimos en corchete: {4b - [3b - 3]}.", "Corchete (precedido de -, invertimos): {4b - 3b + 3}.", "Llave: 4b - 3b + 3 = b + 3."]}
    ],
    "errores_frecuentes": [
        "Eliminar todos los agrupadores al mismo tiempo sin respetar el orden de adentro hacia afuera.",
        "Al eliminar un agrupador con signo $-$, invertir solo algunos signos interiores y olvidarse de otros."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-AN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"En la expresión $\\{{a - [b - (c - d)]\\}}$, si eliminamos el paréntesis primero (signo exterior $-$), ¿qué queda dentro del corchete? (v{i})", "choices": ["A) $b - c + d$", "B) $b - c - d$", "C) $b + c - d$", "D) $b + c + d$"], "correct_answer": "A) $b - c + d$", "solution_steps": "Eliminamos el paréntesis con signo $-$: $-(c-d) = -c+d$. Dentro del corchete queda $b - c + d$.", "paes_style": False})
EJERCICIOS.append({"stable_id": "AGR-AN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": "Simplifica completamente: $\\{3x - [2x - (x + 1)]\\}$.", "choices": ["A) $2x + 1$", "B) $2x - 1$", "C) $-2x + 1$", "D) $4x + 1$"], "correct_answer": "A) $2x + 1$", "solution_steps": "Paso 1 (paréntesis, $-$ exterior): $\\{3x - [2x - x - 1]\\}$. Paso 2 (reduce en corchete): $\\{3x - [x - 1]\\}$. Paso 3 (corchete, $-$ exterior): $\\{3x - x + 1\\}$. Paso 4 (llave): $2x + 1$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-AN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿La expresión $\\{a - [a - (a - 1)]\\}$ simplifica a $a - 1$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Paso 1: $\\{a - [a - a + 1]\\}$. Reduce: $\\{a - [1]\\}$. Paso 2: $\\{a - 1\\}$. Paso 3: $a - 1$.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-AN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"La factura de un servicio se calcula con $F = 100 - [20 + (F_b - 5)]$ donde $F_b = 10$. ¿Cuál es el monto de la factura? (v{i})", "choices": ["A) $75$", "B) $85$", "C) $65$", "D) $80$"], "correct_answer": "A) $75$", "solution_steps": "Sustituimos $F_b=10$: $100 - [20 + (10-5)] = 100 - [20+5] = 100 - [25] = 75$.", "paes_style": True})

# 5. AGRUPACION.SIGNO_VINCULO
sid5 = "MAT.ALG.AGRUPACION.SIGNO_VINCULO"
RECURSOS.append({
    "semantic_id": sid5,
    "objetivo": "Reconocer el signo vínculo como el que une dos miembros de una expresión algebraica compleja.",
    "introduccion": "En una ecuación o en una expresión de dos miembros, el signo que conecta ambos lados se llama signo vínculo. Es el puente algebraico. No es un agrupador, sino un separador que distingue el primer y segundo miembro.",
    "resumen": "El **Signo Vínculo** es el signo de igualdad ($=$) u operador principal que une los dos miembros de una ecuación o expresión. Indica que lo de la izquierda es equivalente o está relacionado con lo de la derecha.",
    "explicacion": "En la ecuación $3x + 2 = x - 4$, el signo $=$ es el vínculo entre el primer miembro ($3x + 2$) y el segundo miembro ($x - 4$).\n\nEn el contexto de agrupaciones, el vínculo puede ser también un operador como $+$ o $-$ que conecta dos grandes bloques. Por ejemplo:\n$[2a + 3] + [a - 1]$.\nAquí el $+$ central es el vínculo que une los dos corchetes.\n\nEl signo vínculo es clave para saber qué es primer miembro y qué es segundo miembro en una ecuación, y es fundamental al trasponer términos (regla del cambio de miembro).",
    "procedimiento": [
        "Paso 1: Identifica el operador principal de la expresión (el que más 'separa' ambos lados).",
        "Paso 2: Clasifica lo que hay a la izquierda de ese operador como primer miembro.",
        "Paso 3: Clasifica lo que hay a la derecha como segundo miembro.",
        "Paso 4: El signo vínculo define la relación entre ambos miembros y es crítico en la resolución de ecuaciones."
    ],
    "ejemplos": [
        {"titulo": "El puente entre dos mundos", "enunciado": "En la expresión 5x - 3 = 2x + 9, identifica el vínculo y los miembros.", "solucion_pasos": ["Signo vínculo: = (igual).", "Primer miembro: 5x - 3.", "Segundo miembro: 2x + 9.", "El signo = establece que ambos representan el mismo valor."]}
    ],
    "errores_frecuentes": [
        "Confundir un signo de operación interna (ej. el $+$ entre términos) con el signo vínculo principal.",
        "Modificar el signo vínculo al transponer términos de un miembro a otro."
    ],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SV-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En la ecuación $4x + 7 = 2x - 3$, ¿qué es el 'signo vínculo' y qué función cumple? (v{i})", "choices": ["A) Es el signo $=$ y establece que el primer miembro ($4x+7$) y el segundo miembro ($2x-3$) tienen el mismo valor.", "B) Es el signo $+$ en $4x + 7$ y sirve para sumar términos.", "C) Es el signo $-$ en $2x-3$ y sirve para restar.", "D) No existe signo vínculo en esa expresión."], "correct_answer": "A) Es el signo $=$ y establece que el primer miembro ($4x+7$) y el segundo miembro ($2x-3$) tienen el mismo valor.", "solution_steps": "El signo vínculo une los dos miembros de la ecuación indicando equivalencia.", "paes_style": False})
EJERCICIOS.append({"stable_id": "AGR-SV-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "En la expresión $[3a + 2] - [a - 5] = 10$, ¿cuál es el signo vínculo principal?", "choices": ["A) El signo $=$.", "B) El signo $-$ entre los corchetes.", "C) El signo $+$ dentro del primer corchete.", "D) El signo $-$ dentro del segundo corchete."], "correct_answer": "A) El signo $=$.", "solution_steps": "El $=$ es el vínculo principal: establece la igualdad entre el lado izquierdo (expresión) y el lado derecho (10).", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SV-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El signo vínculo en una ecuación puede ser alterado o eliminado sin cambiar el significado de la ecuación?", "choices": [], "correct_answer": "Falso", "solution_steps": "El signo vínculo ($=$) establece la relación de igualdad entre los miembros. Eliminarlo destruiría la ecuación. Solo puede mantenerse al realizar operaciones equivalentes en ambos lados.", "paes_style": False})
for i in range(1, 4):
    EJERCICIOS.append({"stable_id": f"AGR-SV-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un balance contable establece que Activos = Pasivos + Patrimonio. Si los activos suman $500p$ y los pasivos son $320p$, ¿cuál es el valor del patrimonio? (v{i})", "choices": ["A) $180p$", "B) $820p$", "C) $160000p$", "D) $-180p$"], "correct_answer": "A) $180p$", "solution_steps": "El signo vínculo $=$ establece: $500p = 320p + Patrimonio$. Despejando: $Patrimonio = 500p - 320p = 180p$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 3 (B0303/Agrupacion)...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"  Creado {filename}.yaml")
    print("Escribiendo JSONL Tanda 3...")
    append_jsonl("mat-alg-operaciones-banco-gen-3", EJERCICIOS)
    print(f"  mat-alg-operaciones-banco-gen-3.jsonl con {len(EJERCICIOS)} ejercicios.")

if __name__ == "__main__":
    generate_all()

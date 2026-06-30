# scratch/build_alg_b0302_t8.py
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

# 35. RAICES_CUADRADAS
sid35 = "MAT.ALG.VALORIZACION.RAICES_CUADRADAS"
RECURSOS.append({
    "semantic_id": sid35, "objetivo": "Valorizar expresiones que contienen raíces cuadradas u otros radicales.",
    "introduccion": "A veces, las fórmulas matemáticas nos obligan a buscar el origen de un número. Si una sala cuadrada tiene un área de 25 metros, ¿cuánto mide su lado? La respuesta yace en la raíz cuadrada.",
    "resumen": "Para valorizar una **Expresión con Raíces**, primero se debe **calcular completamente el valor numérico de todo lo que está dentro de la raíz** (el radicando). Una vez obtenido ese número final, se le extrae la raíz.",
    "explicacion": "Imagina la expresión $\\sqrt{b^2 - 4ac}$. (¡Te sonará conocida!).\nPara valorizarla, digamos con $a=1, b=5, c=6$:\n1. Sustituimos dentro del 'techo' de la raíz: $\\sqrt{(5)^2 - 4(1)(6)}$.\n2. Resolvemos el interior usando jerarquía. Primero potencias y multiplicaciones: $\\sqrt{25 - 24}$.\n3. Hacemos la resta: $\\sqrt{1}$.\n4. Solo al final, cuando queda un solo número bajo el techo, extraemos la raíz: $1$.\n\nRegla de hierro: **Jamás** separes una suma o resta que está bajo una raíz en dos raíces diferentes. $\\sqrt{16 + 9}$ es $\\sqrt{25} = 5$. Si lo separas como $\\sqrt{16} + \\sqrt{9}$ obtendrías $4 + 3 = 7$, lo cual es matemáticamente falso.",
    "procedimiento": ["Paso 1: Sustituye las letras por los números dentro de la raíz.", "Paso 2: Resuelve todas las operaciones bajo el techo de la raíz hasta reducirlo a un solo número.", "Paso 3: Calcula la raíz de ese número final.", "Paso 4: Si la raíz estaba multiplicando o sumando a otras cosas fuera de ella, usa ese resultado para continuar el cálculo general."],
    "ejemplos": [
        {"titulo": "El techo protector", "enunciado": "Valora la expresión \\sqrt{2x + 1} para x=4.", "solucion_pasos": ["Sustituimos la x dentro de la raíz: \\sqrt{2(4) + 1}.", "Resolvemos la multiplicación interior: \\sqrt{8 + 1}.", "Sumamos el interior: \\sqrt{9}.", "Extraemos la raíz: 3."]}
    ],
    "errores_frecuentes": ["Extraer raíces parciales de sumas (ej. decir que $\\sqrt{a^2 + b^2}$ es igual a $a + b$).", "Aplicar la raíz al primer número que ven y luego sumar el resto."],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"RAIZ-CONC-{i}", "semantic_id": sid35, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Al valorar una expresión como $\\sqrt{{x + y}}$, ¿qué principio fundamental rige el orden de las operaciones respecto al símbolo radical? (v{i})", "choices": ["A) El símbolo radical actúa como un grupo agrupador (similar a un paréntesis), obligando a resolver completamente todas las sumas y restas en su interior antes de extraer la raíz.", "B) El radical exige que se le extraiga la raíz primero a la $x$ y luego a la $y$ por separado.", "C) El radical debe resolverse al mismo tiempo que las multiplicaciones interiores.", "D) El orden no importa, siempre dará el mismo resultado."], "correct_answer": "A) El símbolo radical actúa como un grupo agrupador (similar a un paréntesis), obligando a resolver completamente todas las sumas y restas en su interior antes de extraer la raíz.", "solution_steps": "El 'techo' de la raíz encapsula toda la expresión subradical. Debes reducir todo a un solo número antes de aplicar la raíz. Separar raíces en sumas es un error fatal en matemáticas.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"RAIZ-REC-1", "semantic_id": sid35, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el valor numérico de $\\sqrt{5m - n}$ para $m = 4$ y $n = 4$.", "choices": ["A) $4$", "B) $8$", "C) $16$", "D) $2$"], "correct_answer": "A) $4$", "solution_steps": "Interior: $5(4) - 4 = 20 - 4 = 16$. Raíz de 16: $\\sqrt{16} = 4$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"RAIZ-PROC-{i}", "semantic_id": sid35, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿Si evaluamos $\\sqrt{a^2 + b^2}$ con $a = 3$ y $b = 4$, el resultado es igual a evaluar $(a + b)$ con los mismos valores?", "choices": [], "correct_answer": "Falso", "solution_steps": "Valoremos $\\sqrt{3^2 + 4^2} = \\sqrt{9 + 16} = \\sqrt{25} = 5$. Si evaluamos $a + b$ sería $3 + 4 = 7$. Dar por hecho que $\\sqrt{a^2+b^2} = a+b$ es uno de los errores más clásicos del álgebra.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"RAIZ-PAES-{i}", "semantic_id": sid35, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"La velocidad de escape de un planeta simplificado se modela como $v = \\sqrt{{2GM}}$. Si un simulador asigna $G = 8$ y $M = 9$, ¿cuál será la velocidad de escape $v$? (v{i})", "choices": ["A) $12$", "B) $144$", "C) $72$", "D) $24$"], "correct_answer": "A) $12$", "solution_steps": "Sustituimos dentro: $2(8)(9) = 16 \\cdot 9 = 144$. Ahora extraemos la raíz del interior completo: $\\sqrt{144} = 12$.", "paes_style": True})

# 36. EXPRESIONES_POTENCIAS
sid36 = "MAT.ALG.VALORIZACION.EXPRESIONES_POTENCIAS"
RECURSOS.append({
    "semantic_id": sid36, "objetivo": "Valorizar polinomios y fracciones algebraicas complejas donde las variables figuran como exponentes de otras variables o números.",
    "introduccion": "Hasta ahora las letras se mantenían en el suelo. Pero a veces, las incógnitas deciden volar y sentarse en el exponente. Esto es el corazón del crecimiento exponencial (como las pandemias o el interés compuesto).",
    "resumen": "Cuando la **Variable está en el Exponente**, la sustitución sigue la misma regla: se coloca el número en el lugar de la letra. Sin embargo, la operación resultante será calcular **cuántas veces se multiplica la base por sí misma**, según indique ese nuevo exponente numérico.",
    "explicacion": "Observa la expresión $2^x$.\nSi $x = 3$:\n1. Sustituimos la $x$ en el 'cielo': $2^{(3)}$.\n2. Esto NO es $2 \\cdot 3$. Es una potencia.\n3. Calculamos: $2 \\cdot 2 \\cdot 2 = 8$.\n\nSi la expresión es más compleja, como $3^{x+1}$ con $x=1$:\nPrimero debes resolver la suma 'en el cielo' antes de aplicar la potencia.\n- Cielo: $1 + 1 = 2$.\n- Potencia: $3^2 = 9$.",
    "procedimiento": ["Paso 1: Identifica las variables que están posicionadas como exponentes (arriba a la derecha).", "Paso 2: Sustitúyelas por su valor numérico.", "Paso 3: Si hay sumas, restas o multiplicaciones en el exponente, resuélvelas primero para tener un solo número como exponente.", "Paso 4: Desarrolla la potencia multiplicando la base base por sí misma la cantidad de veces que dicte el exponente."],
    "ejemplos": [
        {"titulo": "Elevado a la equis", "enunciado": "Valora 5^{n-2} para n=4.", "solucion_pasos": ["Sustituimos la n en el exponente: 5^{(4-2)}.", "Resolvemos la resta en el exponente: 5^2.", "Calculamos la potencia: 5 * 5 = 25."]}
    ],
    "errores_frecuentes": ["Multiplicar la base por el exponente (ej. decir que $2^3$ es $6$ en lugar de $8$).", "Aplicar la potencia antes de resolver las operaciones en el exponente (ej. en $3^{x+1}$ elevar primero a la $x$ y luego sumarle 1 al resultado general)."],
    "fuente": "Álgebra de Baldor.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"EPOT-CONC-{i}", "semantic_id": sid36, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Cuando en una expresión matemática la variable actúa como exponente (ej. $3^x$), ¿cómo altera esto la naturaleza de la operación en comparación con un coeficiente (ej. $3x$)? (v{i})", "choices": ["A) Transforma la operación de un crecimiento lineal o multiplicativo simple a un crecimiento exponencial, donde la base se multiplicará por sí misma la cantidad de veces que indique la variable.", "B) No altera en nada, son simplemente dos formas distintas de escribir una multiplicación.", "C) Transforma la operación en una suma reiterada.", "D) Obliga a que la base se invierta."], "correct_answer": "A) Transforma la operación de un crecimiento lineal o multiplicativo simple a un crecimiento exponencial, donde la base se multiplicará por sí misma la cantidad de veces que indique la variable.", "solution_steps": "Mientras que $3x$ para $x=4$ es sumar 3 cuatro veces ($3+3+3+3=12$), el modelo $3^x$ es multiplicar 3 cuatro veces ($3 \\cdot 3 \\cdot 3 \\cdot 3 = 81$).", "paes_style": False})
EJERCICIOS.append({"stable_id": f"EPOT-REC-1", "semantic_id": sid36, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": "Calcula el valor de la expresión exponencial $2^{a+b}$ si se sabe que $a=2$ y $b=3$.", "choices": ["A) $32$", "B) $10$", "C) $16$", "D) $64$"], "correct_answer": "A) $32$", "solution_steps": "Primero se consolida el exponente en el 'cielo': $a+b = 2+3 = 5$. Luego aplicamos la base a ese exponente final: $2^5 = 2 \\cdot 2 \\cdot 2 \\cdot 2 \\cdot 2 = 32$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"EPOT-PROC-{i}", "semantic_id": sid36, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "alta", "competencia": "M1", "prompt": "¿El valor de la expresión $x^x$ (una variable elevada a sí misma) evaluada en $x = 3$ es igual a $9$?", "choices": [], "correct_answer": "Falso", "solution_steps": "Evaluamos $x^x$ con $x=3$. Queda $3^3$. Eso significa $3 \\cdot 3 \\cdot 3 = 27$. Quien obtuvo 9 confundió $3^3$ con $3 \\cdot 3$ o con $3^2$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"EPOT-PAES-{i}", "semantic_id": sid36, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "alta", "competencia": "M1", "prompt": f"Un biólogo modela el crecimiento de una bacteria con la expresión poblacional $P = 100 \\cdot 2^{{t/3}}$, donde $t$ es el tiempo en horas. ¿Qué población existirá exactamente a las $9$ horas de iniciado el cultivo? (v{i})", "choices": ["A) $800$", "B) $600$", "C) $900$", "D) $1800$"], "correct_answer": "A) $800$", "solution_steps": "Sustituimos $t=9$. Exponente: $9/3 = 3$. La fórmula queda $100 \\cdot 2^3$. Resolvemos la potencia primero: $2^3 = 8$. Finalmente multiplicamos: $100 \\cdot 8 = 800$.", "paes_style": True})


def generate_all():
    print("Escribiendo YAMLs Tanda 8 (B0302/Valorizacion final)...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 8...")
    append_jsonl("mat-alg-lenguaje-banco-gen-8", EJERCICIOS)
    print("Creado mat-alg-lenguaje-banco-gen-8.jsonl con 20 ejercicios.")

if __name__ == "__main__":
    generate_all()

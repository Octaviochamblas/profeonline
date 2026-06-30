# scratch/build_b0205_t17.py
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

# 1. COMPARACION_REGIMENES
sid1 = "MAT.NUM.INTERES_COMPUESTO.COMPARACION_REGIMENES"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Comparar matemáticamente el rendimiento y los costos entre interés simple y compuesto.",
    "introduccion": "Imagina que el simple es una bicicleta y el compuesto es un auto. En la primera cuadra ambos van iguales, pero si la carrera es larga, el auto te pasará por encima.",
    "resumen": "A igual tasa y plazo, durante el primer período ($t=1$), ambos regímenes generan exactamente el mismo interés. A partir del segundo período ($t>1$), el interés compuesto SIEMPRE supera al interés simple.",
    "explicacion": "Comparar el interés simple con el compuesto es un clásico problema de la prueba:\n\n- **Si $t=1$ (Ej. el primer mes de una inversión a tasa mensual):**\n  - Interés Simple: Ganas el $10\\%$ sobre tu capital.\n  - Interés Compuesto: Ganas el $10\\%$ sobre tu capital.\n  - **Conclusión:** En $t=1$, ambos regímenes son **IGUALES**.\n\n- **Si $t>1$ (A partir del segundo mes/año):**\n  - Interés Simple: Sigues ganando el mismo $10\\%$ sobre el capital inicial (crecimiento lineal).\n  - Interés Compuesto: Ganas el $10\\%$ sobre el capital inicial MÁS los intereses del mes anterior (crecimiento exponencial).\n  - **Conclusión:** El Interés Compuesto siempre generará **MÁS DINERO** (mayor ganancia si es inversión, mayor deuda si es préstamo).",
    "procedimiento": ["Paso 1: Lee si el problema te pide comparar resultados en el primer periodo ($t=1$) o a largo plazo ($t>1$).", "Paso 2: Si $t=1$, asume que los montos son idénticos.", "Paso 3: Si $t>1$, asume que el Compuesto es matemáticamente mayor que el Simple."],
    "ejemplos": [
        {"titulo": "La carrera de los intereses", "enunciado": "Sofía invierte $100.000 al 5% simple anual. Tomás invierte $100.000 al 5% compuesto anual. ¿Quién tendrá más dinero al final del primer año y quién al final del segundo año?", "solucion_pasos": ["Año 1: Ambos tendrán $100.000 + 5.000 = 105.000. Tienen lo MISMO.", "Año 2 (Sofía): $105.000 + 5.000 = 110.000. (Creció lineal).", "Año 2 (Tomás): El 5% de $105.000 es 5.250. Él tendrá $105.000 + 5.250 = 110.250.", "Tomás gana en el año 2 debido a la capitalización."]}
    ],
    "errores_frecuentes": ["Creer que el interés compuesto siempre es mayor desde el día 1 (en el periodo 1 son exactamente iguales).", "Tratar de calcular las cifras exactas en preguntas teóricas de la PAES que solo buscan que reconozcas cuál es mayor."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"COMPREG-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Si comparamos una deuda sujeta a interés simple y otra idéntica sujeta a interés compuesto (misma tasa y capital), ¿qué ocurre matemáticamente durante el PRIMER período de tiempo ($t=1$)? (v{i})", "choices": ["A) Ambos regímenes generan exactamente la misma cantidad de interés.", "B) El interés compuesto genera mayor deuda que el simple.", "C) El interés simple genera mayor deuda que el compuesto.", "D) El interés compuesto no genera intereses en el primer período."], "correct_answer": "A) Ambos regímenes generan exactamente la misma cantidad de interés.", "solution_steps": "En t=1, el interés compuesto aún no tiene 'intereses anteriores' sobre los cuales calcular recargos, por lo que actúa igual que el simple.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"COMPREG-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "A partir del segundo período ($t>1$), la curva que representa al interés compuesto se ubicará siempre:", "choices": ["A) Por encima de la recta del interés simple.", "B) Por debajo de la recta del interés simple.", "C) Exactamente sobre la recta del interés simple.", "D) De forma paralela a la recta del interés simple."], "correct_answer": "A) Por encima de la recta del interés simple.", "solution_steps": "El crecimiento exponencial supera al lineal.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"COMPREG-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si una inversión a interés simple da $\$1.200$ en total tras 2 años, una inversión idéntica pero a interés compuesto dará más de $\$1.200$ en el mismo plazo?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Correcto. El compuesto siempre es mayor a partir de t=2.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"COMPREG-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Dos hermanos, Juan y Pedro, abren cuentas de ahorro depositando cada uno $\$500.000$. La cuenta de Juan opera bajo régimen de interés simple al $8\\%$ anual, mientras que la de Pedro opera con interés compuesto al $8\\%$ anual. Si deciden revisar sus saldos justo al cumplirse el primer año ($12$ meses), ¿qué se puede concluir con certeza matemática? (v{i})", "choices": ["A) Ambos hermanos tendrán exactamente el mismo saldo en sus cuentas.", "B) Pedro tendrá más dinero que Juan.", "C) Juan tendrá más dinero que Pedro.", "D) Pedro tendrá el doble de ganancias que Juan."], "correct_answer": "A) Ambos hermanos tendrán exactamente el mismo saldo en sus cuentas.", "solution_steps": "Como el tiempo es 1 año (t=1), y las tasas son anuales, ambos ganarán exactamente el 8% de $500.000.", "paes_style": True})

# 2. ANUALIDAD_CAPITALIZACION
sid2 = "MAT.NUM.INTERES_COMPUESTO.ANUALIDAD_CAPITALIZACION"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Comprender el concepto básico de anualidad o cuota fija como mecanismo de pago de deudas o ahorros constantes.",
    "introduccion": "A diferencia de un depósito único que dejas años en el banco, en la vida real pagamos el dividendo de la casa o guardamos dinero para la jubilación mes a mes. Esa 'cuota constante' se llama anualidad.",
    "resumen": "Una Anualidad es una sucesión de pagos, depósitos o retiros iguales que se realizan a intervalos regulares de tiempo, con interés compuesto. Si pagas el auto en 48 cuotas fijas, estás pagando una anualidad.",
    "explicacion": "El término **Anualidad** puede ser engañoso, porque **no significa necesariamente que se pague una vez al año**. Es el nombre matemático para **pagos o depósitos periódicos iguales**.\n\nEjemplos clásicos de Anualidades:\n- El pago mensual del dividendo de una casa (crédito hipotecario).\n- El descuento mensual de tu sueldo para la AFP o salud.\n- Depositar $\$50.000$ fijos cada mes en una cuenta de ahorro para el pie de una casa.\n\nEl modelamiento matemático de las anualidades mezcla la suma de muchos cálculos de interés compuesto (se usan fórmulas de series geométricas), pero conceptualmente debes reconocer que una 'cuota fija' implica que una parte del dinero paga los intereses generados ese mes, y el resto amortiza (disminuye) la deuda original.",
    "procedimiento": ["Paso 1: Identifica si el problema involucra un único movimiento de dinero (fórmula de interés compuesto tradicional) o pagos/depósitos repetitivos constantes.", "Paso 2: Si son cuotas fijas repetitivas a lo largo del tiempo, clasifícalo conceptualmente como una Anualidad."],
    "ejemplos": [
        {"titulo": "Identificando la anualidad", "enunciado": "Si depositas $2.000.000 hoy y no lo tocas en 5 años, ¿es una anualidad? Si depositas $50.000 mensuales por 5 años, ¿es una anualidad?", "solucion_pasos": ["El depósito de $2.000.000 es un pago único. NO es anualidad.", "El depósito de $50.000 mensuales es una sucesión de pagos constantes. SÍ es una anualidad (anualidad mensual)."]}
    ],
    "errores_frecuentes": ["Creer que la palabra 'Anualidad' solo se aplica a pagos que ocurren en diciembre o una vez al año.", "Tratar de calcular el monto final de depósitos sucesivos usando la fórmula simple $M = C(1+i)^t$."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"ANUAL-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En matemática financiera, ¿cuál de las siguientes situaciones corresponde conceptualmente a la definición de una 'Anualidad'? (v{i})", "choices": ["A) Pagar la cuota mensual fija de un crédito automotriz durante 36 meses.", "B) Depositar $\$1.000.000$ en un banco y dejarlo crecer por 10 años sin hacer más aportes.", "C) Pagar una compra en el supermercado con tarjeta de débito.", "D) Recibir una herencia en un solo pago de dinero."], "correct_answer": "A) Pagar la cuota mensual fija de un crédito automotriz durante 36 meses.", "solution_steps": "Una anualidad es una serie de pagos constantes y periódicos.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"ANUAL-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Es FALSO respecto al concepto de anualidad en finanzas que:", "choices": ["A) Solo pueden realizarse cobros o pagos una única vez al año.", "B) Consisten en una sucesión de pagos o depósitos iguales.", "C) Involucran intervalos regulares de tiempo (mensual, trimestral, etc).", "D) Se ven afectadas por las reglas del interés compuesto."], "correct_answer": "A) Solo pueden realizarse cobros o pagos una única vez al año.", "solution_steps": "El término 'anualidad' es genérico para cualquier pago periódico (incluso mensual o diario).", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"ANUAL-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El ahorro mensual de $\$20.000$ en una libreta para la vivienda durante $5$ años puede modelarse financieramente como una anualidad?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Sí, al ser depósitos constantes a intervalos regulares, es una anualidad.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"ANUAL-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una empresa debe comprar maquinaria y el banco le ofrece dos opciones. Opción 1: Pagar un único monto total de $\$15.000.000$ al final del año 5. Opción 2: Pagar una cuota fija de $\$2.500.000$ al final de cada año durante 5 años. ¿Qué nombre recibe el modelo matemático subyacente a la Opción 2? (v{i})", "choices": ["A) Anualidad.", "B) Interés simple.", "C) Depósito a plazo.", "D) Capitalización continua."], "correct_answer": "A) Anualidad.", "solution_steps": "La Opción 2 presenta pagos constantes y periódicos, lo cual es la definición exacta de anualidad.", "paes_style": True})

# 3. AMORTIZACION_PRESTAMO
sid3 = "MAT.NUM.INTERES_COMPUESTO.AMORTIZACION_PRESTAMO"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Entender la descomposición de una cuota de préstamo entre el pago de intereses y la amortización del capital.",
    "introduccion": "¿Has pagado una cuota de 300 lucas por tu casa y al mirar la deuda ves que solo bajó 50 lucas? No te están robando, es el proceso de amortización. Una parte es para el banco, otra parte achica la deuda.",
    "resumen": "En cada cuota fija de un crédito, una parte se destina a pagar los **Intereses** del mes (ganancia del banco) y el resto se usa para **Amortizar** (disminuir el Capital real adeudado).",
    "explicacion": "Cuando pides un préstamo bancario (como un hipotecario) y pagas una cuota fija mensual, ese dinero se divide internamente en dos pedazos:\n\n1. **Interés:** Es el costo por usar el dinero del banco ese mes. Se calcula multiplicando el Saldo Adeudado actual por la tasa de interés.\n2. **Amortización:** Es lo que sobra de la cuota después de pagar el interés. Este dinero **resta** la deuda real que tienes.\n\n**Ecuación de la Cuota:**\n$$\\text{Cuota} = \\text{Amortización} + \\text{Interés}$$\n\nAl principio de un crédito de 20 años, la deuda es tan grande que casi toda la cuota se va en pagar puros intereses (el banco se asegura su ganancia primero) y la amortización es ínfima. Al final del crédito, ocurre lo contrario.",
    "procedimiento": ["Paso 1: Reconoce que Cuota Fija NO significa que la deuda baje esa misma cantidad.", "Paso 2: Entiende que $Amortizacion = Cuota - Interes$.", "Paso 3: Solo la 'Amortización' disminuye el Saldo Insoluto (la deuda real)."],
    "ejemplos": [
        {"titulo": "Descomponiendo la cuota", "enunciado": "Debes $10.000.000. El interés de este mes es el 1% de esa deuda. Pagas una cuota de $300.000. ¿Cuánto se redujo realmente tu deuda?", "solucion_pasos": ["Calculamos el interés del mes: 1% de $10.000.000 = $100.000.", "La cuota es de $300.000. De esos, $100.000 son para pagar el interés.", "Lo que sobra es la Amortización: $300.000 - $100.000 = $200.000.", "Tu deuda bajó en $200.000. Ahora debes $9.800.000."]}
    ],
    "errores_frecuentes": ["Restarle el valor completo de la cuota al total de la deuda (ignorando que el banco cobra intereses).", "Creer que la palabra 'Amortizar' es sinónimo de 'Pagar Intereses'."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"AMORTIZ-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En el contexto del pago de un crédito con cuotas periódicas, ¿qué representa el concepto de 'Amortización'? (v{i})", "choices": ["A) La porción de la cuota que se destina exclusivamente a reducir el capital adeudado original.", "B) El total de la cuota mensual que se le transfiere al banco.", "C) La ganancia que obtiene el banco por prestar el dinero.", "D) El impuesto cobrado por el Estado en cada transacción."], "correct_answer": "A) La porción de la cuota que se destina exclusivamente a reducir el capital adeudado original.", "solution_steps": "Amortizar significa 'matar' la deuda. Es la parte que resta el saldo insoluto.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"AMORTIZ-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "La ecuación fundamental que descompone una cuota periódica de un préstamo es:", "choices": ["A) Cuota = Amortización + Interés.", "B) Cuota = Capital + Monto Final.", "C) Cuota = Amortización - Interés.", "D) Cuota = Tasa + Capital."], "correct_answer": "A) Cuota = Amortización + Interés.", "solution_steps": "El dinero de la cuota se divide en pagar el recargo (interés) y en pagar la deuda real (amortización).", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"AMORTIZ-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si pagas una cuota mensual de $\$150.000$ y el interés generado en ese mes por tu deuda fue de $\$50.000$, entonces amortizaste $\$100.000$ de capital?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$150.000$ (Cuota) - $50.000$ (Interés) = $100.000$ (Amortización).", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"AMORTIZ-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un cliente mantiene una deuda hipotecaria con un saldo actual de $\$50.000.000$. La tasa de interés del crédito es un $0.5\\%$ mensual. Si en el mes actual el cliente paga una cuota fija de $\$400.000$, ¿cuál será el nuevo saldo de su deuda para el mes siguiente tras este pago? (v{i})", "choices": ["A) $\$49.850.000$", "B) $\$49.600.000$", "C) $\$49.750.000$", "D) $\$50.150.000$"], "correct_answer": "A) $\$49.850.000$", "solution_steps": "Interés del mes: $0.5\\%$ de $50.000.000 = 250.000$. Amortización = Cuota - Interés = $400.000 - 250.000 = 150.000$. Nuevo Saldo = $50.000.000 - 150.000 = 49.850.000$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 17...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 17...")
    append_jsonl("mat-num-razones-banco-gen-17", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-17.jsonl con 30 ejercicios.")

if __name__ == "__main__":
    generate_all()

# scratch/build_b0205_t14.py
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

# 1. TASA_INTERES_REAL
sid1 = "MAT.NUM.FINANZAS_PERSONALES.TASA_INTERES_REAL"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Calcular la tasa de interés real descontando el efecto de la inflación.",
    "introduccion": "Si el banco te da un 5% de premio por guardar tu plata, pero el supermercado sube sus precios un 6% ese mismo año, en realidad perdiste dinero. El banco te dio más billetes, pero ahora esos billetes compran menos.",
    "resumen": "La Tasa de Interés Nominal es lo que promete el banco. La Tasa de Interés Real es la rentabilidad verdadera tras descontar la inflación. Fórmula aproximada: Tasa Real = Tasa Nominal - Inflación.",
    "explicacion": "Al evaluar una inversión, debes diferenciar:\n\n- **Tasa Nominal:** Es el porcentaje bruto que el banco o institución te promete pagar (Ej: $7\\%$ al año).\n- **Inflación (IPC):** Es la pérdida de poder adquisitivo del dinero (Ej: $4\\%$ al año).\n- **Tasa de Interés Real:** Es el aumento real de tu capacidad de compra.\n\nLa fórmula rápida (y aproximada para tasas pequeñas) es:\n$$\\text{Tasa Real} \\approx \\text{Tasa Nominal} - \\text{Inflación}$$\n\nSi inviertes a una tasa del $7\\%$ nominal y la inflación es del $4\\%$, tu rentabilidad real es solo del $3\\%$. Si la inflación fuera mayor a la tasa del banco, tu tasa real sería negativa.",
    "procedimiento": ["Paso 1: Identifica la Tasa Nominal (lo que te pagan).", "Paso 2: Identifica la Inflación del mismo período.", "Paso 3: Resta $Nominal - Inflacion$ para conocer la Tasa Real."],
    "ejemplos": [
        {"titulo": "Rentabilidad engañosa", "enunciado": "Un fondo mutuo rinde 8% en el año, pero la inflación fue del 10%. ¿Cuál fue la tasa real aproximada?", "solucion_pasos": ["Tasa Nominal = $8\\%$.", "Inflación = $10\\%$.", "Tasa Real = $8\\% - 10\\% = -2\\%$.", "En realidad, perdió un 2% de poder de compra."]}
    ],
    "errores_frecuentes": ["Creer que mientras la tasa del banco sea mayor a 0, siempre se está ganando dinero de verdad.", "Restar al revés (Inflación menos Nominal)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"INTREAL-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué indicador económico debe restarse a la tasa de interés nominal de una inversión para obtener la 'tasa de interés real' aproximada? (v{i})", "choices": ["A) La inflación (IPC).", "B) El Impuesto al Valor Agregado (IVA).", "C) La tasa de desempleo.", "D) El tipo de cambio (Dólar)."], "correct_answer": "A) La inflación (IPC).", "solution_steps": "La inflación es la que destruye el poder adquisitivo de los intereses ganados.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"INTREAL-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si la tasa nominal es menor que la inflación, la tasa real será:", "choices": ["A) Negativa.", "B) Cero.", "C) Positiva.", "D) Igual a la inflación."], "correct_answer": "A) Negativa.", "solution_steps": "Si $Nominal < Inflacion$, la resta $Nominal - Inflacion$ dará un número menor a cero.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"INTREAL-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si un banco te ofrece un depósito al $5\\%$ anual y la inflación anual es $2\\%$, tu tasa real aproximada de ganancia es $3\\%$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$5\\% - 2\\% = 3\\%$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"INTREAL-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una persona tiene sus ahorros en una cuenta que le otorga un $4.5\\%$ de interés nominal anual. Durante ese año, el país enfrentó una crisis con una inflación del $8.5\\%. ¿Cuál es la tasa de interés real aproximada que obtuvo el ahorrante? (v{i})", "choices": ["A) $-4.0\\%$", "B) $4.0\\%$", "C) $-13.0\\%$", "D) $13.0\\%$"], "correct_answer": "A) $-4.0\\%$", "solution_steps": "Real = Nominal - Inflación = $4.5\\% - 8.5\\% = -4.0\\%$. Perdió un $4\\%$ de poder adquisitivo.", "paes_style": True})

# 2. COTIZACION_AFP
sid2 = "MAT.NUM.FINANZAS_PERSONALES.COTIZACION_AFP"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Calcular la cotización previsional obligatoria (AFP y salud) sobre un sueldo imponible.",
    "introduccion": "¿Te ofrecieron un trabajo por $1.000.000? Cuidado, ese dinero no llegará completo a tu cuenta. El Estado exige que guardes una parte obligatoria para tu jubilación y salud. Lo que te llega se llama 'sueldo líquido'.",
    "resumen": "En Chile, de tu Sueldo Imponible se descuenta aproximadamente un 10% obligatorio para jubilación (AFP) + la comisión de la AFP (ej. 1.5%), y un 7% obligatorio para Salud (Fonasa o Isapre).",
    "explicacion": "Al firmar un contrato, tu sueldo se divide así:\n\n1. **Sueldo Imponible:** El monto base sobre el cual se calculan los descuentos.\n2. **Descuentos Legales (Cotizaciones):**\n   - **AFP (Fondo de Pensiones):** Un $10\\%$ obligatorio que va a tu cuenta individual para la vejez, más una comisión que cobra la AFP (ej: $0.6\\%$ a $1.5\\%$). En promedio, se descuenta alrededor de un $11\\%$ total.\n   - **Salud:** Un $7\\%$ obligatorio (va a Fonasa o a pagar el plan base de tu Isapre).\n   - *Seguro de Cesantía e Impuestos (si corresponde).* \n3. **Sueldo Líquido:** Es el dinero que finalmente te depositan en el banco ($Liquido = Imponible - Cotizaciones$).",
    "procedimiento": ["Paso 1: Identifica el Sueldo Imponible.", "Paso 2: Calcula el $10\\%$ para la cuenta de AFP (sin contar la comisión) multiplicando el Imponible por $0.10$.", "Paso 3: Calcula el $7\\%$ para Salud multiplicando el Imponible por $0.07$."],
    "ejemplos": [
        {"titulo": "Descuento de Salud y AFP", "enunciado": "Si tu sueldo imponible es de $800.000, ¿cuánto dinero va a tu fondo de pensión (el 10%) y cuánto a salud (7%)?", "solucion_pasos": ["Pensión (10%): $800.000 \\cdot 0.10 = 80.000$.", "Salud (7%): $800.000 \\cdot 0.07 = 56.000$.", "Total de esos dos descuentos legales: $136.000."]}
    ],
    "errores_frecuentes": ["Creer que la AFP descuenta exactamente el 10% de tu sueldo (descuenta un poco más debido a la comisión por administración).", "Pensar que el Sueldo Imponible es lo que recibirás a fin de mes."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"COTIZAFP-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué porcentaje del sueldo imponible está destinado por ley de forma exclusiva y obligatoria a la cuenta de capitalización individual (fondo para pensión), sin considerar la comisión de la AFP? (v{i})", "choices": ["A) $10\\%$", "B) $7\\%$", "C) $19\\%$", "D) $20\\%$"], "correct_answer": "A) $10\\%$", "solution_steps": "El 10% es el aporte obligatorio al fondo; el 7% es salud.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"COTIZAFP-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El dinero que finalmente recibe el trabajador en su cuenta bancaria tras pagar todas sus cotizaciones e impuestos se denomina:", "choices": ["A) Sueldo Líquido.", "B) Sueldo Imponible.", "C) Sueldo Bruto.", "D) Salario Mínimo."], "correct_answer": "A) Sueldo Líquido.", "solution_steps": "Líquido es el monto ya 'filtrado' de impuestos y cotizaciones.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"COTIZAFP-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El descuento legal obligatorio para salud en Chile corresponde al $7\\%$ del sueldo imponible?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Verdadero. El 7% se destina a Fonasa o Isapre.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"COTIZAFP-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Javier tiene un sueldo imponible de $\$900.000$. Su AFP le cobra un $1.2\\%$ de comisión por administración. Si Javier debe pagar su $10\\%$ obligatorio al fondo de pensiones, el $1.2\\%$ de comisión, y el $7\\%$ de salud, ¿cuál será su sueldo líquido asumiendo que no tiene otros descuentos? (v{i})", "choices": ["A) $\$736.200$", "B) $\$756.000$", "C) $\$810.000$", "D) $\$747.000$"], "correct_answer": "A) $\$736.200$", "solution_steps": "Suma de descuentos = $10\\% + 1.2\\% + 7\\% = 18.2\\%$. Javier recibe el $100 - 18.2 = 81.8\\%$. Sueldo líquido = $900.000 \\cdot 0.818 = 736.200$.", "paes_style": True})

# 3. PROYECCION_PREVISIONAL
sid3 = "MAT.NUM.FINANZAS_PERSONALES.PROYECCION_PREVISIONAL"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Estimar ahorros a largo plazo basados en un aporte constante (modelo simplificado).",
    "introduccion": "Si guardas una pequeña cantidad de dinero todos los meses desde que empiezas a trabajar hasta que te jubiles, el monto final no es solo la suma del dinero: la magia del interés compuesto y la constancia hacen que ese pozo crezca enormemente.",
    "resumen": "Proyectar el ahorro previsional de forma básica implica multiplicar: Aporte Mensual $\\times$ 12 meses $\\times$ Años de cotización. En la vida real, se le suma la rentabilidad del fondo.",
    "explicacion": "Una proyección simplificada (sin considerar interés ni rentabilidad, solo la acumulación lineal) nos ayuda a entender el volumen del ahorro:\n\n$$\\text{Monto Acumulado} = \\text{Aporte Mensual} \\cdot 12 \\text{ meses} \\cdot \\text{Años Trabajados}$$\n\n- **¿Por qué empezar temprano?** Un trabajador que ahorra desde los 25 a los 65 años (40 años) acumulará mucho más capital base que alguien que empieza a los 45 años, incluso si este último aporta el doble de dinero mensual. El tiempo de cotización es el factor más importante para una buena pensión futura.",
    "procedimiento": ["Paso 1: Calcula el aporte mensual ($10\\%$ de tu sueldo imponible).", "Paso 2: Multiplica por 12 para obtener tu ahorro anual.", "Paso 3: Multiplica por la cantidad de años que vas a trabajar antes de jubilar."],
    "ejemplos": [
        {"titulo": "Ahorro básico sin rentabilidad", "enunciado": "Si tu sueldo imponible será de $1.000.000 por el resto de tu vida (y aportas el 10% mensual), ¿cuánto habrás juntado en 30 años de trabajo? (Ignorando la rentabilidad).", "solucion_pasos": ["Aporte mensual: 10% de 1.000.000 = $100.000.", "Aporte anual: $100.000 \\cdot 12 = 1.200.000$.", "Aporte en 30 años: $1.200.000 \\cdot 30 = 36.000.000$.", "Tendrías $36.000.000 de capital puro (en la vida real sería mucho más gracias a las inversiones de la AFP)."]}
    ],
    "errores_frecuentes": ["Olvidar multiplicar por los 12 meses del año al hacer proyecciones a largo plazo.", "Creer que la pensión será igual a tu último sueldo (la pensión depende únicamente del total de dinero juntado en ese pozo dividido por los años que vivas como jubilado)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROYPREV-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál de los siguientes factores matemáticos tiene el mayor impacto multiplicador en el monto final de una jubilación basada en ahorro individual? (v{i})", "choices": ["A) La cantidad de años constantes en los que se aporta al fondo (tiempo).", "B) El sueldo del primer mes de trabajo.", "C) El porcentaje de impuesto a la renta.", "D) El sueldo del último mes de trabajo antes de jubilar."], "correct_answer": "A) La cantidad de años constantes en los que se aporta al fondo (tiempo).", "solution_steps": "En cualquier modelo de acumulación a largo plazo, la variable tiempo (Años) expande radicalmente el resultado gracias al interés compuesto.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PROYPREV-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Para calcular el aporte de pensión puro acumulado en un año (sin rentabilidad), se debe multiplicar el aporte mensual del trabajador por:", "choices": ["A) 12", "B) 10", "C) 100", "D) 1"], "correct_answer": "A) 12", "solution_steps": "Un año tiene 12 meses.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROYPREV-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si aportas $\$50.000$ mensuales durante 10 años, el dinero puro acumulado en tu cuenta será de $\$6.000.000$ (sin contar intereses)?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$50.000 \\cdot 12 \\cdot 10 = 600.000 \\cdot 10 = 6.000.000$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PROYPREV-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Andrés y Berta analizan sus ahorros (sin considerar rentabilidad). Andrés aportó $\$150.000$ mensuales durante $20$ años. Berta aportó $\$100.000$ mensuales durante $30$ años. ¿Cuál es la diferencia de dinero acumulado entre ambos al final de sus respectivos períodos? (v{i})", "choices": ["A) $\$0$ (Ambos juntaron lo mismo).", "B) Andrés juntó $\$10.000.000$ más que Berta.", "C) Berta juntó $\$6.000.000$ más que Andrés.", "D) Andrés juntó $\$6.000.000$ más que Berta."], "correct_answer": "A) $\$0$ (Ambos juntaron lo mismo).", "solution_steps": "Andrés: $150.000 \\cdot 12 \\cdot 20 = 1.800.000 \\cdot 20 = 36.000.000$. Berta: $100.000 \\cdot 12 \\cdot 30 = 1.200.000 \\cdot 30 = 36.000.000$. Acumularon el mismo capital base.", "paes_style": True})

# 4. INTERES_SIMPLE_CONCEPTO
sid4 = "MAT.NUM.INTERES_SIMPLE.CONCEPTO"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Comprender la diferencia entre el interés como costo de un préstamo y el interés simple como modelo matemático lineal.",
    "introduccion": "Si un amigo te presta dinero, quizás no te cobre extra. Pero los bancos no son tus amigos. Al prestarte dinero, te cobran un 'arriendo' por usarlo. Ese arriendo se llama interés.",
    "resumen": "El interés es el costo del dinero en el tiempo. En el Interés Simple, este costo se calcula SIEMPRE sobre el capital inicial prestado, sin sumar los intereses ganados anteriormente a la base de cálculo.",
    "explicacion": "El **Interés** es el porcentaje adicional que pagas por un préstamo o que ganas por una inversión.\nExisten dos grandes mundos:\n- **Interés Simple:** El interés se calcula siempre sobre el capital inicial. No varía de periodo en periodo. Es una relación lineal. (Se usa para préstamos a muy corto plazo).\n- **Interés Compuesto:** El interés de cada mes se suma al capital, y el nuevo mes se calcula sobre ese monto mayor (interés sobre interés). Se usa en los bancos y a largo plazo.\n\nEn el Interés Simple, si el capital es $\$10.000$ y el interés es $10\\%$ anual, cada año pagarás exactamente $\$1.000$ extra. No importa si pasaron 1 o 5 años, la cuota de interés es fija.",
    "procedimiento": ["Paso 1: Entiende que la base de cálculo (el Capital Inicial) en el interés simple nunca cambia.", "Paso 2: Reconoce que el crecimiento de la deuda es constante y lineal.", "Paso 3: Diferéncialo del interés compuesto, donde la base de cálculo crece exponencialmente."],
    "ejemplos": [
        {"titulo": "Comparando el simple con la realidad", "enunciado": "Si presto $1.000 con interés simple de 10% mensual, ¿cuánto dinero en intereses genero cada mes?", "solucion_pasos": ["El 10% de 1.000 es 100.", "El mes 1 genero $100.", "El mes 2 genero otros $100.", "El mes 3 genero otros $100. Es constante."]}
    ],
    "errores_frecuentes": ["Confundir el Interés Simple con el Compuesto (creyendo que el mes 2 se calcula el 10% sobre 1.100).", "Pensar que los bancos usan Interés Simple para los hipotecarios (los bancos usan compuesto para maximizar las ganancias)."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"INTSIMP-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Cuál es la principal característica teórica del Interés Simple? (v{i})", "choices": ["A) El interés se calcula siempre sobre el capital inicial, manteniéndose constante en cada período.", "B) El interés se calcula sobre el capital inicial más los intereses previamente acumulados.", "C) La tasa de interés varía aleatoriamente cada mes.", "D) Es el interés que no cobra recargos financieros."], "correct_answer": "A) El interés se calcula siempre sobre el capital inicial, manteniéndose constante en cada período.", "solution_steps": "La base de cálculo nunca cambia en el modelo simple.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"INTSIMP-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "En un régimen de interés simple, el gráfico del monto acumulado respecto al tiempo describe una línea:", "choices": ["A) Recta (crecimiento lineal).", "B) Curva exponencial.", "C) Parábola.", "D) Horizontal."], "correct_answer": "A) Recta (crecimiento lineal).", "solution_steps": "Como se suma siempre el mismo monto, es una función afín/lineal.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"INTSIMP-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿En el interés simple, los intereses ganados en el primer período generan nuevos intereses en el segundo período?", "choices": [], "correct_answer": "Falso", "solution_steps": "Esa es la definición del interés compuesto (interés sobre interés). En el simple no ocurre.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"INTSIMP-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un prestamista informal ofrece préstamos bajo la modalidad de 'interés simple' con una tasa del $5\\%$ mensual. Si un cliente toma un préstamo de $\$200.000$, ¿cuál será el comportamiento de los intereses que deberá pagar el cliente cada mes? (v{i})", "choices": ["A) Generará una deuda de $\$10.000$ extra constantes cada mes.", "B) Generará una deuda que crecerá aceleradamente mes a mes.", "C) Pagará el $5\\%$ del saldo adeudado, el cual disminuye mes a mes.", "D) Pagará $\$200.000$ el primer mes y $\$10.000$ el segundo."], "correct_answer": "A) Generará una deuda de $\$10.000$ extra constantes cada mes.", "solution_steps": "El $5\\%$ de $\$200.000$ es $\$10.000$. Al ser simple, siempre pagará esos $\$10.000$ fijos por periodo.", "paes_style": True})

# 5. CALCULO_INTERES
sid5 = "MAT.NUM.INTERES_SIMPLE.CALCULO_INTERES"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Calcular la ganancia o deuda final utilizando la fórmula de interés simple.",
    "introduccion": "¿Cómo calculamos rápidamente la deuda si pasan 5 años en un modelo lineal? Simplemente multiplicamos el interés de un año por cinco.",
    "resumen": "Fórmula Interés Simple: $I = C \\cdot i \\cdot t$. (Interés ganado = Capital $\\times$ tasa $\\times$ tiempo). Capital Final: $C_f = C + I$, o $C_f = C(1 + i \\cdot t)$. ¡La tasa y el tiempo deben estar en la misma unidad!",
    "explicacion": "La matemática del Interés Simple requiere tres variables:\n- **$C$:** Capital Inicial prestado.\n- **$i$:** Tasa de interés (escrita como decimal. Ej: $5\\% \\rightarrow 0.05$).\n- **$t$:** Tiempo o cantidad de periodos.\n\n**1. Fórmula de Ganancia (solo los intereses):**\n$$I = C \\cdot i \\cdot t$$\n*(Calcula la ganancia de 1 mes y la multiplica por los meses que pasaron).* \n\n**2. Fórmula del Capital Final (Monto Total a pagar):**\n$$C_f = C + (C \\cdot i \\cdot t) = C(1 + i \\cdot t)$$\n\n**¡Regla de Oro!** El tiempo $t$ y la tasa $i$ deben estar en el mismo 'idioma'. Si la tasa es anual y te dan el tiempo en meses, debes convertir el tiempo a años dividiendo por 12.",
    "procedimiento": ["Paso 1: Convierte la tasa a decimal (divide por 100).", "Paso 2: Asegúrate que tiempo y tasa usen la misma unidad de medida (ej. ambos en años o ambos en meses).", "Paso 3: Multiplica $Capital \\times Tasa \\times Tiempo$ para hallar la ganancia."],
    "ejemplos": [
        {"titulo": "Cálculo directo", "enunciado": "Se invierten $5.000 al 4% de interés simple anual durante 3 años. ¿Cuánto interés se ganó?", "solucion_pasos": ["C = 5000, i = 0.04 (anual), t = 3 (años).", "$I = 5000 \\cdot 0.04 \\cdot 3$.", "$I = 200 \\cdot 3 = 600$.", "Se ganaron $600 de interés."]}
    ],
    "errores_frecuentes": ["Olvidar pasar la tasa a decimal (multiplicar por 4 en vez de 0.04).", "Mezclar tasa mensual con tiempo en años sin hacer la conversión."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CALCINTS-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En la fórmula del interés simple $I = C \\cdot i \\cdot t$, ¿qué condición fundamental deben cumplir las variables 'i' y 't'? (v{i})", "choices": ["A) Ambas deben estar expresadas en la misma unidad de tiempo (ej. meses con meses).", "B) Ambas deben ser porcentajes.", "C) El tiempo 't' siempre debe estar en años, sin importar 'i'.", "D) Deben ser números enteros mayores a cero."], "correct_answer": "A) Ambas deben estar expresadas en la misma unidad de tiempo (ej. meses con meses).", "solution_steps": "Si la tasa es mensual, los períodos deben ser meses para que la fórmula tenga sentido.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"CALCINTS-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Para usar un interés del $8\\%$ en la fórmula matemática general de interés simple, el número que debes ingresar en la variable 'i' es:", "choices": ["A) $0.08$", "B) $8$", "C) $0.8$", "D) $1.08$"], "correct_answer": "A) $0.08$", "solution_steps": "$8 \\div 100 = 0.08$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CALCINTS-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El interés simple generado por $\$10.000$ al $5\\%$ anual durante $2$ años se calcula como $10000 \\cdot 0.05 \\cdot 2 = 1000$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "Exactamente, $I = C \\cdot i \\cdot t$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"CALCINTS-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un prestamista facilita $\$500.000$ a un cliente a una tasa de interés simple del $2\\%$ mensual. Si el cliente devuelve todo el dinero prestado más los intereses al cabo de $6$ meses, ¿cuánto dinero total deberá entregarle al prestamista? (v{i})", "choices": ["A) $\$560.000$", "B) $\$60.000$", "C) $\$510.000$", "D) $\$800.000$"], "correct_answer": "A) $\$560.000$", "solution_steps": "I = $500.000 \\cdot 0.02 \\cdot 6 = 60.000$. Total = Capital + Intereses = $500.000 + 60.000 = 560.000$.", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 14...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 14...")
    append_jsonl("mat-num-razones-banco-gen-14", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-14.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()

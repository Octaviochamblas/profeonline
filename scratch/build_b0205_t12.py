# scratch/build_b0205_t12.py
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

# 1. VALOR_FINAL_DESCUENTO
sid1 = "MAT.NUM.VARIACION_PORCENTUAL.VALOR_FINAL_DESCUENTO"
RECURSOS.append({
    "semantic_id": sid1, "objetivo": "Calcular el valor final tras aplicar un descuento porcentual en un solo paso.",
    "introduccion": "¿Apurado en la caja de la tienda? No calcules cuánto dinero te ahorras para luego restarlo. Calcula directamente lo que debes pagar multiplicando por el porcentaje complementario.",
    "resumen": "Para aplicar un descuento del $D\\%$ en un solo paso, multiplica el Valor Inicial por el factor complementario: $(1 - D/100)$. Ej: Descuento del 20% es multiplicar por $0.80$.",
    "explicacion": "Al igual que con el aumento, existe un **factor multiplicador** para los descuentos. Si a un total del $100\\%$ le quitas un descuento $D\\%$, lo que pagarás realmente es el $(100 - D)\\%$.\n\nLa fórmula directa para el Valor Final con descuento es:\n$$\\text{Valor Final} = \\text{Valor Inicial} \\cdot \\left( 1 - \\frac{D}{100} \\right)$$\n\n- Si te hacen un $20\\%$ de descuento, pagas el $80\\%$. El factor es $1 - 0.20 = 0.80$.\n- Si la liquidación es del $45\\%$, pagas el $55\\%$. Multiplicas por $0.55$.",
    "procedimiento": ["Paso 1: Identifica el porcentaje de descuento ($D\\%$).", "Paso 2: Resta ese porcentaje a 100 para saber qué porcentaje sí vas a pagar.", "Paso 3: Convierte ese número a decimal y multiplica por el precio original."],
    "ejemplos": [
        {"titulo": "Zapatillas en oferta", "enunciado": "Zapatillas de $60.000 con 30% de descuento. ¿Cuánto pagas en caja?", "solucion_pasos": ["Si el descuento es 30%, pagamos el 70%.", "El factor decimal es $0.70$.", "Multiplicamos: $60.000 \\cdot 0.70 = 42.000$.", "El precio final es $42.000."]}
    ],
    "errores_frecuentes": ["Multiplicar por $0.30$ y creer que ese es el precio a pagar (eso es el dinero que te ahorras).", "Dividir el precio por el porcentaje de descuento."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"VFDSCTO-GEN-CONC-{i}", "semantic_id": sid1, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"¿Qué factor multiplicador debes utilizar para calcular en un solo paso el precio final de un artículo con un $15\\%$ de rebaja? (v{i})", "choices": ["A) $0.85$", "B) $1.15$", "C) $0.15$", "D) $8.5$"], "correct_answer": "A) $0.85$", "solution_steps": "$100\\% - 15\\% = 85\\% = 0.85$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"VFDSCTO-GEN-REC-1", "semantic_id": sid1, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Si multiplicas el precio de un vuelo por $0.60$, estás aplicando un descuento del:", "choices": ["A) $40\\%$", "B) $60\\%$", "C) $0.6\\%$", "D) $4\\%$"], "correct_answer": "A) $40\\%$", "solution_steps": "Si pagas el 60%, significa que te descontaron el $100\\% - 60\\% = 40\\%$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"VFDSCTO-GEN-PROC-{i}", "semantic_id": sid1, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El precio final tras un descuento del $5\\%$ se obtiene multiplicando por $0.95$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$100 - 5 = 95$. Factor $0.95$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"VFDSCTO-GEN-PAES-{i}", "semantic_id": sid1, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un televisor tiene un precio de lista de $\$350.000$. La tienda ofrece un descuento del $18\\%$ por pago al contado. ¿Qué expresión permite hallar el dinero exacto que el cliente deberá entregar a la cajera? (v{i})", "choices": ["A) $350.000 \\cdot 0.82$", "B) $350.000 \\cdot 0.18$", "C) $350.000 \\cdot 1.18$", "D) $350.000 \\cdot 1.82$"], "correct_answer": "A) $350.000 \\cdot 0.82$", "solution_steps": "Paga el $100 - 18 = 82\\%$. Factor $= 0.82$.", "paes_style": True})

# 2. PORCENTAJES_SUCESIVOS
sid2 = "MAT.NUM.VARIACION_PORCENTUAL.PORCENTAJES_SUCESIVOS"
RECURSOS.append({
    "semantic_id": sid2, "objetivo": "Calcular el impacto real de aplicar aumentos y descuentos de manera sucesiva.",
    "introduccion": "Las vitrinas anuncian '¡Liquidación! 50% + 20% extra con tarjeta'. ¿Significa eso un 70% de descuento? Lamento decepcionarte: el comercio jamás sumaría así los descuentos. Aprende a calcular el verdadero descuento.",
    "resumen": "Los porcentajes sucesivos NO se suman ni restan linealmente. Se calculan multiplicando encadenadamente sus factores de variación. Ej: $+10\\%$ y luego $-10\\%$ no devuelve el precio original.",
    "explicacion": "Cuando ocurren variaciones en cadena (un descuento tras otro, o un aumento seguido de una caída), **cada variación se aplica sobre el nuevo saldo**, no sobre el precio original.\n\nEl método infalible es multiplicar el Valor Inicial por cada factor sucesivo:\n$$\\text{Final} = \\text{Inicial} \\cdot \\text{Factor}_1 \\cdot \\text{Factor}_2$$\n\n**Ejemplo del '50% + 20% extra':**\n- Primer factor (descuento 50%): pagas el $50\\%$ ($0.50$).\n- Segundo factor (descuento 20%): pagas el $80\\%$ ($0.80$).\n- Multiplicación conjunta: $0.50 \\cdot 0.80 = 0.40$.\nAl final terminas pagando el $40\\%$ del producto, lo que equivale a un **descuento real del $60\\%$**, no del $70\\%$.",
    "procedimiento": ["Paso 1: Convierte cada aumento o descuento en su 'factor multiplicador' individual.", "Paso 2: Multiplica todos los factores entre sí. Esto te dará un 'Factor Único'.", "Paso 3: Analiza el Factor Único para ver si quedó arriba o debajo de 1. (Ej. $0.40$ significa que pagas el 40%, o sea ahorras el 60%)."],
    "ejemplos": [
        {"titulo": "Aumentar y descontar lo mismo", "enunciado": "Un producto sube 20% y al mes siguiente baja 20%. ¿Queda en el precio original?", "solucion_pasos": ["Factor aumento: $1.20$. Factor baja: $0.80$.", "Multiplicamos: $1.20 \\cdot 0.80 = 0.96$.", "El factor final es $0.96$, lo que significa que el producto final quedó con un descuento real del 4% (¡es más barato que al principio!)."]}
    ],
    "errores_frecuentes": ["Sumar algebraicamente los porcentajes (creer que $+10\\%$ y $-10\\%$ da $0\\%$).", "Aplicar ambos descuentos sobre el Valor Inicial por separado y luego sumarlos."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCSUC-GEN-CONC-{i}", "semantic_id": sid2, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Si una tienda ofrece un descuento del $30\\%$ y un $10\\%$ adicional sobre el precio ya rebajado, el descuento único real es: (v{i})", "choices": ["A) Un $37\\%$ de descuento real.", "B) Un $40\\%$ de descuento real.", "C) Un $20\\%$ de descuento real.", "D) Un $30\\%$ de descuento real."], "correct_answer": "A) Un $37\\%$ de descuento real.", "solution_steps": "Factores: $0.70 \\cdot 0.90 = 0.63$. Pagas el 63%, el descuento real es $100 - 63 = 37\\%$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"PORCSUC-GEN-REC-1", "semantic_id": sid2, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Un aumento del $20\\%$ seguido de un descuento del $20\\%$ equivale a multiplicar el precio inicial por:", "choices": ["A) $0.96$", "B) $1.00$", "C) $1.04$", "D) $0.80$"], "correct_answer": "A) $0.96$", "solution_steps": "$1.20 \\cdot 0.80 = 0.96$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCSUC-GEN-PROC-{i}", "semantic_id": sid2, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Aplicar dos descuentos sucesivos del $50\\%$ significa que el producto es gratis?", "choices": [], "correct_answer": "Falso", "solution_steps": "$0.50 \\cdot 0.50 = 0.25$. Pagas el 25% del precio (un 75% de descuento real).", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"PORCSUC-GEN-PAES-{i}", "semantic_id": sid2, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Una empresa importadora sufre un aumento del $10\\%$ en los costos de envío y luego, por aranceles aduaneros, el nuevo total sufre otro aumento del $15\\%. ¿Cuál es el factor multiplicador único que debe aplicar al costo original para obtener el costo final? (v{i})", "choices": ["A) $1.265$", "B) $1.25$", "C) $0.25$", "D) $1.015$"], "correct_answer": "A) $1.265$", "solution_steps": "Factores: $1.10 \\cdot 1.15 = 1.265$. (Aumento real de 26.5%).", "paes_style": True})

# 3. IVA (Impuesto al Valor Agregado)
sid3 = "MAT.NUM.VARIACION_PORCENTUAL.IVA"
RECURSOS.append({
    "semantic_id": sid3, "objetivo": "Aplicar y despejar el Impuesto al Valor Agregado (IVA) en operaciones comerciales.",
    "introduccion": "Todo lo que compras en una tienda formal ya trae el IVA escondido. El gobierno recauda el 19% extra sobre el precio original (neto). ¿Sabrías cómo 'quitarle' ese IVA a un producto para saber cuánto gana realmente el vendedor?",
    "resumen": "El IVA en Chile es del $19\\%$. El Precio Neto no tiene IVA. El Precio Bruto incluye el IVA. Fórmulas: $Bruto = Neto \\cdot 1.19$. $Neto = Bruto / 1.19$.",
    "explicacion": "El **IVA (Impuesto al Valor Agregado)** es un aumento porcentual estándar fijado por el Estado (en Chile, 19%).\n\nTérminos comerciales:\n- **Precio Neto:** Valor real del producto sin impuestos (es el $100\\%$ base).\n- **Valor del IVA:** Monto de dinero que va al gobierno ($19\\%$ del neto).\n- **Precio Bruto (Final):** Lo que pagas en caja ($119\\%$ del neto).\n\n**Para agregar el IVA:**\nMultiplicas el precio neto por $1.19$ (es un aumento porcentual).\n**Para 'sacarle' el IVA a un precio final:**\nComo $Bruto = Neto \\cdot 1.19$, entonces $Neto = Bruto \\div 1.19$. (¡Nunca calcules el 19% del bruto para restarlo, eso matemáticamente está mal porque la base era el neto!).",
    "procedimiento": ["Paso 1: Identifica si el dato dado es el Neto (sin impuesto) o el Bruto (con impuesto ya metido).", "Paso 2: Si te dan el Neto y piden el Bruto, multiplica por $1.19$.", "Paso 3: Si te dan el Bruto (lo pagado en caja) y piden el Neto, divide por $1.19$."],
    "ejemplos": [
        {"titulo": "Despejando el Neto", "enunciado": "Pagas $11.900 por un audífono. ¿Cuánto es el precio neto sin IVA?", "solucion_pasos": ["11.900 es el Precio Bruto.", "Para hallar el neto, dividimos por el factor 1.19.", "$11.900 / 1.19 = 10.000$.", "El precio sin IVA era $10.000. (El Estado se llevó $1.900)."]}
    ],
    "errores_frecuentes": ["Creer que si un producto cuesta $10.000 bruto, el IVA es $1.900 (Falso, el IVA se calcula sobre el neto, en este caso sería $10.000 / 1.19 = 8.403$, y el IVA es $1.597$).", "Restar el 19% del Precio Bruto para intentar hallar el Neto."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"IVA-GEN-CONC-{i}", "semantic_id": sid3, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Si conoces el 'Precio Bruto' (final con IVA) de un artículo y deseas conocer su 'Precio Neto' (sin IVA del $19\\%$), la operación correcta es: (v{i})", "choices": ["A) Dividir el Precio Bruto por $1.19$.", "B) Multiplicar el Precio Bruto por $0.81$.", "C) Calcular el $19\\%$ del Precio Bruto y restárselo.", "D) Dividir el Precio Bruto por $0.19$."], "correct_answer": "A) Dividir el Precio Bruto por $1.19$.", "solution_steps": "Despejando de $Bruto = Neto \\cdot 1.19$.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"IVA-GEN-REC-1", "semantic_id": sid3, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El factor multiplicador para agregar el IVA ($19\\%$) al precio neto de forma directa es:", "choices": ["A) $1.19$", "B) $0.19$", "C) $1.81$", "D) $19.0$"], "correct_answer": "A) $1.19$", "solution_steps": "$1 + 0.19 = 1.19$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"IVA-GEN-PROC-{i}", "semantic_id": sid3, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Si un libro cuesta $\$5.000$ neto, su precio bruto con IVA del $19\\%$ es $\$5.950$?", "choices": [], "correct_answer": "Verdadero", "solution_steps": "$5000 \\cdot 1.19 = 5950$.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"IVA-GEN-PAES-{i}", "semantic_id": sid3, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Un empresario factura la venta de insumos. En la boleta, el Total Pagado (Precio Bruto) es de $\$238.000$. ¿Cuánto fue el monto exacto del impuesto IVA (en pesos) que deberá declarar el empresario por esa venta? (Asuma IVA $19\\%$). (v{i})", "choices": ["A) $\$38.000$", "B) $\$45.220$", "C) $\$200.000$", "D) $\$19.000$"], "correct_answer": "A) $\$38.000$", "solution_steps": "Neto = $238.000 / 1.19 = 200.000$. Monto IVA = Bruto - Neto = $238.000 - 200.000 = 38.000$. (Notar que si sacaban el 19% del bruto daba la opción trampa B).", "paes_style": True})

# 4. TIPOS_GASTO (FINANZAS PERSONALES)
sid4 = "MAT.NUM.FINANZAS_PERSONALES.TIPOS_GASTO"
RECURSOS.append({
    "semantic_id": sid4, "objetivo": "Clasificar los gastos personales en fijos, variables e imprevistos para la elaboración de un presupuesto.",
    "introduccion": "¿A dónde se fue mi sueldo? Para tomar el control de tu dinero, lo primero es etiquetar las salidas. No es lo mismo pagar el arriendo mensual que comprarte un café por antojo.",
    "resumen": "Los gastos se dividen en Fijos (obligatorios e ineludibles mes a mes), Variables (necesarios pero su monto y frecuencia cambia) e Imprevistos (emergencias fuera de control).",
    "explicacion": "En educación financiera, armar un presupuesto requiere conocer tus tipos de egresos (salidas de dinero):\n\n- **Gasto Fijo:** Son aquellos de los que no puedes escapar a corto plazo y su monto suele ser conocido. Ejemplos: El arriendo o dividendo, la mensualidad del colegio, cuota de un préstamo. Deben ser tu prioridad número 1.\n- **Gasto Variable:** Son gastos cotidianos y necesarios, pero cuyo valor o frecuencia lo decides tú. Ejemplos: Compras en el supermercado, salir a comer, cuentas de servicios (luz/agua fluctúan según tu consumo), ropa.\n- **Gasto Imprevisto:** Son urgencias que rompen el presupuesto normal. Ejemplos: Una enfermedad, una reparación mecánica del auto, una multa de tránsito.",
    "procedimiento": ["Paso 1: Analiza si el gasto se repite obligatoriamente cada mes. Si sí, es Fijo.", "Paso 2: Si el gasto depende de tu estilo de vida o consumo mes a mes, es Variable.", "Paso 3: Si es una emergencia sorpresiva que no planificaste, es Imprevisto."],
    "ejemplos": [
        {"titulo": "Clasificando la boleta de la luz", "enunciado": "¿Qué tipo de gasto es la cuenta de electricidad de la casa?", "solucion_pasos": ["Aunque llega todos los meses, el monto cambia dependiendo de si dejas las luces prendidas o apagas la estufa.", "Por lo tanto, es un gasto Variable."]}
    ],
    "errores_frecuentes": ["Creer que la cuenta del supermercado es un Gasto Fijo porque 'hay que comer' (la comida es necesaria, pero el gasto es variable porque puedes elegir comer arroz o caviar).", "Confundir un Gasto Variable (ir al cine) con un Imprevisto."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"GASTOS-GEN-CONC-{i}", "semantic_id": sid4, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"En el diseño de un presupuesto familiar mensual, el pago de la cuota del dividendo hipotecario de la casa clasifica como: (v{i})", "choices": ["A) Gasto Fijo.", "B) Gasto Variable.", "C) Gasto Imprevisto.", "D) Ingreso Fijo."], "correct_answer": "A) Gasto Fijo.", "solution_steps": "Es un compromiso financiero obligatorio con un monto estable cada mes.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"GASTOS-GEN-REC-1", "semantic_id": sid4, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "Una visita de urgencia a la clínica dental tras la caída de una tapadura se clasifica como:", "choices": ["A) Gasto Imprevisto.", "B) Gasto Fijo.", "C) Gasto Variable.", "D) Gasto Hormiga."], "correct_answer": "A) Gasto Imprevisto.", "solution_steps": "Es una emergencia no planificada.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"GASTOS-GEN-PROC-{i}", "semantic_id": sid4, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿El dinero gastado en salir a restaurantes todos los fines de semana se considera un gasto fijo porque ocurre todas las semanas?", "choices": [], "correct_answer": "Falso", "solution_steps": "Es un gasto variable, ya que tú tienes control sobre él y puedes decidir no hacerlo el mes siguiente.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"GASTOS-GEN-PAES-{i}", "semantic_id": sid4, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Martina está analizando sus finanzas para reducir deudas. Ella anota: Arriendo ($\$350.000$), Supermercado ($\$120.000$), Plan de celular ($\$15.000$) y Salidas al cine ($\$40.000$). Si Martina decide recortar exclusivamente sus 'gastos variables' a la mitad, ¿cuánto dinero ahorrará este mes? (v{i})", "choices": ["A) $\$80.000$", "B) $\$262.500$", "C) $\$20.000$", "D) $\$175.000$"], "correct_answer": "A) $\$80.000$", "solution_steps": "Fijos: Arriendo y Celular (contratos). Variables: Supermercado ($120.000$) y Cine ($40.000$). Total variables: $160.000$. La mitad es $80.000$.", "paes_style": True})

# 5. TIPOS_INGRESO (FINANZAS PERSONALES)
sid5 = "MAT.NUM.FINANZAS_PERSONALES.TIPOS_INGRESO"
RECURSOS.append({
    "semantic_id": sid5, "objetivo": "Identificar y clasificar diferentes tipos de ingresos personales.",
    "introduccion": "El dinero puede llegar a tu bolsillo por distintas vías. Entender si ese dinero es seguro (un sueldo) o depende de tu esfuerzo mes a mes (una comisión) cambia por completo cómo debes planificar tu vida.",
    "resumen": "Los ingresos pueden ser Fijos (sueldo base asegurado) o Variables (comisiones por venta, horas extras, ganancias de negocios independientes o bonos de acciones).",
    "explicacion": "Al armar un presupuesto, los **ingresos (entradas de dinero)** dictan tu nivel de vida. Se dividen en:\n\n- **Ingresos Fijos:** Dinero que recibes regularmente y cuyo monto es seguro y predecible. El mejor ejemplo es el **salario o sueldo base** mensual de un empleado contratado, o una pensión de jubilación.\n- **Ingresos Variables:** Dinero que puede cambiar de mes a mes o no estar garantizado.\n  - **Comisión:** Dinero extra que se paga por lograr metas de ventas.\n  - **Horas Extras:** Dinero por trabajar más allá del horario fijo.\n  - **Honorarios / Freelance:** Ingresos de un trabajador independiente (un mes puede tener muchos clientes y otro mes ninguno).\n  - **Dividendos e Intereses:** Ganancias variables por tener acciones en empresas o dinero invertido en depósitos a plazo.",
    "procedimiento": ["Paso 1: Analiza la fuente del dinero.", "Paso 2: Si el monto está garantizado por contrato cada mes independiente del rendimiento, es Fijo.", "Paso 3: Si el monto depende de cuántas ventas hiciste, o cómo le fue al negocio, es Variable."],
    "ejemplos": [
        {"titulo": "Sueldo mixto", "enunciado": "Un vendedor gana $500.000 base + 5% por cada venta que haga. ¿Qué tipo de ingresos tiene?", "solucion_pasos": ["Los $500.000 son Ingreso Fijo, cuenta con ellos sí o sí.", "El 5% de ventas es una Comisión, por ende, es Ingreso Variable. Su presupuesto mensual debe basarse en lo fijo para no endeudarse."]}
    ],
    "errores_frecuentes": ["Creer que porque un mes te fue muy bien como independiente (ganando mucho), pasaste a tener un ingreso fijo alto.", "Confundir un ingreso variable como un 'bono esporádico' con algo fijo con lo que pagar deudas."],
    "fuente": "Currículum Nacional MINEDUC.", "estado": "publicado"
})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"INGRESOS-GEN-CONC-{i}", "semantic_id": sid5, "item_group": "conceptuales", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": f"Un trabajador independiente que emite boletas de honorarios según los clientes que atienda cada mes percibe principalmente ingresos de tipo: (v{i})", "choices": ["A) Ingreso Variable.", "B) Ingreso Fijo.", "C) Salario Base.", "D) Dividendo Accionario."], "correct_answer": "A) Ingreso Variable.", "solution_steps": "Como el flujo de clientes cambia, no hay un monto mensual garantizado.", "paes_style": False})
EJERCICIOS.append({"stable_id": f"INGRESOS-GEN-REC-1", "semantic_id": sid5, "item_group": "reconocimiento", "format": "multiple_choice", "difficulty": "basica", "competencia": "M1", "prompt": "El dinero extra que recibe un vendedor asociado a superar sus metas mensuales de venta se denomina:", "choices": ["A) Comisión.", "B) Salario Base.", "C) Gasto Variable.", "D) Dividendo."], "correct_answer": "A) Comisión.", "solution_steps": "La comisión es un premio o porcentaje de las ventas.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"INGRESOS-GEN-PROC-{i}", "semantic_id": sid5, "item_group": "procedimiento_basico", "format": "true_false", "difficulty": "basica", "competencia": "M1", "prompt": "¿Un dividendo anual ganado por tener acciones de una empresa tecnológica es un ingreso fijo y seguro?", "choices": [], "correct_answer": "Falso", "solution_steps": "Los dividendos dependen de las utilidades de la empresa ese año, por ende son ingresos variables de inversión.", "paes_style": False})
for i in range(1, 4): EJERCICIOS.append({"stable_id": f"INGRESOS-GEN-PAES-{i}", "semantic_id": sid5, "item_group": "tipo_paes", "format": "multiple_choice", "difficulty": "media", "competencia": "M1", "prompt": f"Julio es asesor comercial. Tiene un sueldo base de $\$450.000$ y recibe $\$25.000$ adicionales por cada nuevo cliente que capte. Si en el mes logró captar $8$ clientes, ¿cuánto dinero provino estrictamente de ingresos variables? (v{i})", "choices": ["A) $\$200.000$", "B) $\$650.000$", "C) $\$450.000$", "D) $\$475.000$"], "correct_answer": "A) $\$200.000$", "solution_steps": "Ingreso Variable (comisiones) = $8 \\cdot 25.000 = 200.000$. (Los $450.000$ son fijos).", "paes_style": True})

def generate_all():
    print("Escribiendo YAMLs Tanda 12...")
    for r in RECURSOS:
        filename = r["semantic_id"].lower().replace(".", "-").replace("_", "-")
        write_yaml(filename, r)
        print(f"Creado {filename}.yaml")

    print("Escribiendo JSONL Tanda 12...")
    append_jsonl("mat-num-razones-banco-gen-12", EJERCICIOS)
    print("Creado mat-num-razones-banco-gen-12.jsonl con 50 ejercicios.")

if __name__ == "__main__":
    generate_all()
